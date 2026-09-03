"""
Location: paper-a/analysis/repair_local_check.py
Purpose: The two local configurations were absent from ollama when the repair sweep ran and had to
         be re-pulled. A re-pulled tag is not necessarily the build that produced the published 0.7
         arm, so this re-runs them on the ORIGINAL windows and asks whether the stored results
         reproduce. If they do not, the repaired-vs-original comparison for those two configurations
         would confound a window change with a model change, and they are excluded and named.
         Usage:  python3 analysis/repair_local_check.py
Functions: rerun_original(), compare(), main()
Calls: repair_run.engine/client_for, fold.item_rates, harness.run_harness
Imports: json, sys, pathlib, config, fold, repair_run
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config                        # noqa: E402
import fold                          # noqa: E402
import repair_analysis as RA         # noqa: E402
import repair_run as RR              # noqa: E402
import mode_stability as MS          # noqa: E402
import repair_windows as RW          # noqa: E402
import tables_out as T               # noqa: E402

CHECK = config.PAPER_ROOT / "out" / "repair" / "control"
LOCAL = ("gemma3-1b", "gemma3-1b-qat")
# Equivalence is judged against a RESAMPLING NULL, not an agreement floor.
#
# The floor was 0.90, chosen with no reference to how unstable these configurations are. It is the
# wrong instrument: gemma3-1b's published wobble is 0.383, so two independent 20-run samples
# disagree about the modal answer on a good share of items with nothing whatever changed. Applied
# here it excluded gemma3-1b at 12/14 and admitted gemma3-1b-qat at 13/14 -- and the calibrated
# test then showed 2 observed mode changes against 3.84 +- 1.20 expected from resampling the SAME
# model (z = -1.53), i.e. BETTER agreement than chance predicts. The floor was measuring the
# model's own instability and calling it a changed build.
#
# It would also have biased the experiment in a specific direction: dropping the highest-wobble
# configuration from the repaired condition lowers the pooled repaired wobble and pushes the
# result toward meeting the registered threshold.
Z_MAX = 2.0


def rerun_original(label: str, model_id: str, engine_mods) -> Dict[str, Any]:
    """The same fourteen items, ORIGINAL windows, twenty runs, into a control namespace."""
    runner, harness, _preflight, _scorer = engine_mods
    client = RR.client_for("ollama", model_id, runner)
    out = {}
    for leaf_name, (leaf_dir, task, field) in sorted(RR.build_leaves(runner).items()):
        full, _ = runner.load_instances(leaf_dir, field)
        repaired_ids = {p.stem for p in (RW.DEST / leaf_name).glob("*.txt")}
        subset = [(i, t) for (i, t) in full if i["id"] in repaired_ids]
        if not subset:
            continue
        ckpt = CHECK / leaf_name / f"{label}.jsonl"
        ckpt.parent.mkdir(parents=True, exist_ok=True)
        for _ in range(RR.MAX_REFILL + 1):
            runs, _ = harness.run_harness(client, task, subset, n_runs=20, temperature=0.7,
                                          checkpoint_file=str(ckpt), model_label=label,
                                          max_workers=2)
            if RR.drop_nulls(ckpt) == 0:
                break
        out[leaf_name] = RA.condition_rows(task, subset, runs, field)
    return out


def compare(label: str, control: Dict[str, Any], engine_mods) -> List[Dict[str, Any]]:
    """Stored original vs freshly re-run original, per item, on the MODAL answer."""
    runner = engine_mods[0]
    rows = []
    for leaf_name, (leaf_dir, task, field) in sorted(RR.build_leaves(runner).items()):
        full, _ = runner.load_instances(leaf_dir, field)
        stored = RA.condition_rows(task, full,
                                   RA.read_runs(leaf_dir / f"runs_{label}.jsonl"), field)
        for iid, fresh in control.get(leaf_name, {}).items():
            old = stored.get(iid)
            if old is None or old["flipped"] is None or fresh["flipped"] is None:
                continue
            rows.append({"model": label, "leaf": leaf_name, "item": iid,
                         "stored_modal": old["modal"], "fresh_modal": fresh["modal"],
                         "agree": int(old["modal"] == fresh["modal"]),
                         "stored_dispersion": old["dispersion"],
                         "fresh_dispersion": fresh["dispersion"]})
    return rows


def stored_values(label, rows, engine_mods):
    """The stored per-run values for each checked item, which ARE the null's distribution."""
    import splithalf
    runner = engine_mods[0]
    scorer, _, _ = splithalf.engine_modules()
    want = {(r["leaf"], r["item"]) for r in rows}
    vals = {}
    for leaf_name, (leaf_dir, task, field) in sorted(RR.build_leaves(runner).items()):
        full, _ = runner.load_instances(leaf_dir, field)
        by = {}
        for rec in RA.read_runs(leaf_dir / f"runs_{label}.jsonl"):
            by.setdefault(rec["instance_idx"], []).append(rec)
        for idx, (inst, _t) in enumerate(full):
            if (leaf_name, inst["id"]) not in want:
                continue
            v = scorer._values_for(by.get(idx, []), field)
            if v:
                vals[f"{leaf_name}/{inst['id']}"] = v
    return vals


def main() -> Dict[str, Any]:
    mods = RR.engine()
    lineup = {l[0]: l[2] for l in mods[2].LINEUP}
    allrows, verdicts = [], {}
    for label in LOCAL:
        print(f"  === {label} control on ORIGINAL windows ===", flush=True)
        rows = compare(label, rerun_original(label, lineup[label], mods), mods)
        allrows += rows
        agree = sum(r["agree"] for r in rows)
        changes = len(rows) - agree
        cal = MS.calibrate(changes, stored_values(label, rows, mods))
        verdicts[label] = {"n": len(rows), "agree": agree, "changes": changes,
                           "expected": cal["expected"], "sd": cal["sd"], "z": cal["z"],
                           "equivalent": bool(rows) and cal["consistent"]}
        print(f"      {changes} mode changes over {len(rows)} items; resampling the SAME model "
              f"expects {cal['expected']:.2f} +- {cal['sd']:.2f}"
              + (f", z={cal['z']:+.2f}" if cal["z"] is not None else ""))
        print(f"      -> {'CONSISTENT with the published build, may be paired' if verdicts[label]['equivalent'] else 'INCONSISTENT: the build differs, exclude and say so'}")
    T.write_csv(config.out_paths()["tables"] / "repair_local_control.csv",
                ["model", "leaf", "item", "stored_modal", "fresh_modal", "agree",
                 "stored_dispersion", "fresh_dispersion"],
                [[r[k] for k in ("model", "leaf", "item", "stored_modal", "fresh_modal", "agree",
                                 "stored_dispersion", "fresh_dispersion")] for r in allrows])
    (config.out_paths()["out"] / "repair_local_control.json").write_text(
        json.dumps(verdicts, indent=1))
    return verdicts


if __name__ == "__main__":
    main()
