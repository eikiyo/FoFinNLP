"""
Location: paper-a/analysis/triage.py
Purpose: STEP 3 support. Rank the 154 sampled items by how likely the ORACLE is wrong, using the
         12 models' answers ALREADY on disk. This is triage, never validation: an LLM reading
         cannot certify ground truth for a paper that measures LLM behaviour on the same items.
         It only decides the ORDER a human reads them in, and that ordering is worth having --
         convergent model disagreement is where oracle errors actually live.
Functions: item_view(), collect_views(), score_suspicion(), write_worklist(), selftest()
Calls: fold (per-item extraction), splithalf (engine modules), config
Imports: collections, typing, pathlib, config, fold, splithalf, tables_out
"""

from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import config
import fold
import splithalf
import tables_out as T

CONSISTENT = 0.90       # a model "settled" on an answer if its modal value holds this often


def item_view(task, instances, runs, field: str) -> List[Dict[str, Any]]:
    """Per item of one (leaf, model) cell: the model's MODAL answer, how consistently it gave it,
    and the oracle's value. The modal answer is what a deployment would actually see."""
    scorer, _, _ = splithalf.engine_modules()
    import normalize
    fspec = task["fields"][field]
    by_inst = scorer._runs_by_instance(runs)
    out = []
    for idx, (_inst, truth) in enumerate(instances):
        vals = scorer._values_for(by_inst.get(idx, []), field)
        if not vals:
            out.append({"item": idx, "modal": None, "consistency": None, "truth": None})
            continue
        modal, count = Counter(vals).most_common(1)[0]
        out.append({"item": idx, "modal": modal, "consistency": count / len(vals),
                    "truth": normalize.canonical(truth.get(field), fspec["type"]) if truth else None})
    return out


def collect_views(models: Sequence[str], leaves: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Every sampled leaf's items, as seen by all 12 models. One pass over the runs files."""
    _, runner, _ = splithalf.engine_modules()
    per_leaf: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
    opened = []
    for entry in leaves:
        task = splithalf._task_of(entry["rel"])
        instances, _ = runner.load_instances(config.probity_root() / entry["rel"], entry["field"])
        per_leaf[entry["leaf"]] = {}
        for m in models:
            runs, path = splithalf.leaf_runs(entry["rel"], m)
            opened.append(path)
            per_leaf[entry["leaf"]][m] = (item_view(task, instances, runs, entry["field"])
                                          if runs else [])
    config.assert_arm_clean(opened)
    return per_leaf


def score_suspicion(per_leaf, models: Sequence[str], leaves: List[Dict[str, Any]]
                    ) -> List[Dict[str, Any]]:
    """Per item: how many models settled on an answer, how many settled on the SAME wrong answer,
    and what that answer was.

    The signal is CONVERGENT disagreement. One model differing from the oracle is a model being
    wrong -- that is the phenomenon the paper studies. Eleven models independently settling on the
    same value the oracle does not have is a different thing, and the cheapest explanation is that
    the oracle is wrong. Ranking by it is not evidence of anything; it decides reading order."""
    rows = []
    for entry in leaves:
        views = per_leaf[entry["leaf"]]
        n_items = max((len(v) for v in views.values()), default=0)
        for i in range(n_items):
            settled = [views[m][i] for m in models
                       if i < len(views[m]) and views[m][i]["modal"] is not None
                       and (views[m][i]["consistency"] or 0) >= CONSISTENT]
            if not settled:
                continue
            truth = next((s["truth"] for s in settled if s["truth"] is not None), None)
            wrong = [s for s in settled if s["modal"] != truth]
            alt = Counter(str(s["modal"]) for s in wrong).most_common(1)
            rows.append({
                "leaf": entry["leaf"], "item": i, "field": entry["field"], "oracle": truth,
                "n_settled": len(settled), "n_disagree": len(wrong),
                "top_alternative": alt[0][0] if alt else "",
                "n_on_alternative": alt[0][1] if alt else 0,
                "convergence": (alt[0][1] / len(settled)) if alt else 0.0})
    rows.sort(key=lambda r: (-r["n_on_alternative"], -r["convergence"]))
    return rows


def write_worklist(rows: List[Dict[str, Any]], out_dir: Path, top: int = 40) -> Dict[str, Any]:
    """The reading order, plus a RANDOM control block.

    The control matters: reading only the suspicious items measures the instrument, not the data.
    A human who reads 40 flagged items and 20 unflagged ones can tell a real oracle-error rate from
    a checker that flags everything -- a positive control needs a negative control beside it."""
    out_dir.mkdir(parents=True, exist_ok=True)
    flagged = [r for r in rows if r["n_on_alternative"] >= 2][:top]
    keys = {(r["leaf"], r["item"]) for r in flagged}
    rest = [r for r in rows if (r["leaf"], r["item"]) not in keys]
    control = rest[:: max(1, len(rest) // 20)][:20] if rest else []
    T.write_csv(out_dir / "oracle_triage.csv",
                ["priority", "block", "leaf", "item", "field", "oracle_says", "models_settled",
                 "models_disagreeing", "top_alternative", "models_on_alternative", "convergence",
                 "oracle_correct", "corrected_value", "notes"],
                [[i + 1, block, r["leaf"], r["item"], r["field"], str(r["oracle"])[:40],
                  r["n_settled"], r["n_disagree"], r["top_alternative"][:40],
                  r["n_on_alternative"], T.fmt(r["convergence"], 3), "", "", ""]
                 for i, (block, r) in enumerate(
                     [("FLAGGED", r) for r in flagged] + [("CONTROL (random)", r) for r in control])])
    return {"n_items_scored": len(rows), "n_flagged": len(flagged),
            "n_control": len(control),
            "n_unanimous_against_oracle": sum(
                1 for r in rows if r["n_settled"] >= 8 and r["n_disagree"] == r["n_settled"]),
            "top": flagged[:8]}


def selftest() -> str:
    """Prove the suspicion score fires on convergent disagreement and stays quiet otherwise."""
    leaves = [{"leaf": "L", "rel": "leaves/L", "field": "f"}]
    models = ["a", "b", "c"]

    def mk(modal, truth="T"):
        return {"item": 0, "modal": modal, "consistency": 1.0, "truth": truth}
    conv = {"L": {m: [mk("X")] for m in models}}
    r = score_suspicion(conv, models, leaves)[0]
    assert r["n_on_alternative"] == 3 and r["convergence"] == 1.0, \
        f"three models converging on one non-oracle answer must score maximally: {r}"
    agree = {"L": {m: [mk("T")] for m in models}}
    r2 = score_suspicion(agree, models, leaves)[0]
    assert r2["n_disagree"] == 0 and r2["n_on_alternative"] == 0, \
        f"models agreeing with the oracle must not be flagged: {r2}"
    split = {"L": {"a": [mk("X")], "b": [mk("Y")], "c": [mk("T")]}}
    r3 = score_suspicion(split, models, leaves)[0]
    assert r3["n_on_alternative"] == 1, \
        f"models disagreeing with each other is model error, not oracle error: {r3}"
    noisy = {"L": {m: [dict(mk("X"), consistency=0.5)] for m in models}}
    assert score_suspicion(noisy, models, leaves) == [], \
        "unsettled models must not vote -- an unstable answer is not evidence about the oracle"
    return ("triage selftest PASS - fires on convergent disagreement, silent when models match the "
            "oracle, discounts models that disagree with each other, ignores unsettled answers")
