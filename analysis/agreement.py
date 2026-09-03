"""
Location: paper-a/analysis/agreement.py
Purpose: STAGE 3 step 3. Build the BLIND re-annotation pack (labels withheld, order randomised)
         and score it in one command once the sheet comes back: agreement, Cohen's kappa where
         kappa is meaningful, and the disagreement list the adjudication rule operates on.
Functions: write_blind_pack(), write_adjudication(), cohens_kappa(), _canon(), score_sheet(),
           selftest(), main()
Calls: probity engine/normalize.py (reused for canonicalisation), annotation, splithalf
Imports: csv, json, sys, collections, pathlib, typing, numpy, config, annotation, tables_out
"""

import csv
import re
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

import annotation
import config
import tables_out as T

BLIND_SEED = 20260729
KAPPA_TYPES = ("binary", "categorical")   # kappa is only meaningful on a small category space


def write_blind_pack(sample: List[Dict[str, Any]], answer_types: Dict[str, str], out_dir: Path,
                     seed: int = BLIND_SEED) -> Dict[str, Any]:
    """The pack the second reading is actually done on: one row per item, ORIGINAL LABEL ABSENT,
    rows shuffled so the re-annotator never works through one leaf in a block.

    Order matters more than it looks. Reading 8 items of one clause type in sequence lets the
    second reading anchor on the first, which inflates agreement exactly where the paper needs it
    to be honest. `row_id` is a stable join key so the labels can be re-attached afterwards; the
    leaf is still shown because the item cannot be answered without knowing which document it is."""
    rows = []
    for leaf in sorted(sample, key=lambda x: x["leaf"]):
        for item in annotation._items_of(leaf):
            rows.append([leaf["leaf"], item.get("id", ""), leaf["field"],
                         answer_types.get(leaf["leaf"], ""), "", "", "", ""])
    order = np.random.default_rng(seed).permutation(len(rows))
    shuffled = [[f"R{i + 1:04d}"] + rows[j] for i, j in enumerate(order)]
    path = out_dir / "blind_pack.csv"
    T.write_csv(path, ["row_id", "leaf", "item_id", "field", "answer_type", "annotator_answer",
                       "undeterminable", "notes", "minutes_spent"], shuffled)
    return {"path": path, "n_rows": len(shuffled), "seed": seed,
            "n_leaves": len(sample),
            "leaves": sorted({r[1] for r in shuffled})}


def _canon(value: Any, ftype: str) -> Any:
    """Canonicalise a written answer the same way the benchmark canonicalises a model's answer, so
    '1.0x' and '1x' are one reading and not a disagreement. Reused from probity, never re-derived."""
    import normalize
    try:
        return normalize.canonical(value, ftype)
    except Exception:
        return None


def cohens_kappa(a: Sequence[Any], b: Sequence[Any]) -> Dict[str, Any]:
    """Cohen's kappa over paired categorical labels.

    Returned with its own health warning: when nearly every item has a distinct value (free numeric
    fields), expected agreement goes to zero and kappa collapses onto the raw agreement rate, where
    it adds nothing and implies a rigour it does not have. `applicable` says whether the category
    space is small enough for the statistic to mean what readers think it means."""
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    n = len(pairs)
    if n == 0:
        return {"n": 0, "kappa": None, "po": None, "pe": None, "reason": "no scorable pairs"}
    po = sum(1 for x, y in pairs if x == y) / n
    ca, cb = Counter(x for x, _ in pairs), Counter(y for _, y in pairs)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in set(ca) | set(cb))
    n_cat = len(set(ca) | set(cb))
    if pe >= 1.0:
        return {"n": n, "kappa": None, "po": po, "pe": pe, "n_categories": n_cat,
                "applicable": False, "reason": "expected agreement is 1: every label identical"}
    return {"n": n, "kappa": (po - pe) / (1 - pe), "po": po, "pe": pe, "n_categories": n_cat,
            "applicable": bool(n_cat <= max(2, n // 4)), "reason": ""}


def primed_items(sample: List[Dict[str, Any]], tasks: Dict[str, Dict[str, Any]],
                 out_dir: Path) -> List[Dict[str, Any]]:
    """Items whose own answer is visible in the notation guide the annotator must be shown.

    A free-text canonical-format field documents itself by example ("e.g. '4yr/1yr-cliff'"), and
    those examples are drawn from the real answer space, so for a few items the example IS the
    label. An annotator who follows the notation guide agrees with the oracle for free on exactly
    those items.

    Deleting the examples is the wrong repair: without the notation an annotator writes "4 years,
    1 year cliff" and the scorer counts a disagreement that is orthographic, not substantive. So
    the items are ENUMERATED here instead, before the sitting, and agreement is reported both with
    and without them. Declared in advance it is a caveat; found afterwards it would be a
    post-hoc exclusion."""
    hits = []
    for leaf in sample:
        spec = (tasks[leaf["leaf"]].get("fields") or {}).get(leaf["field"], {})
        guide = str(spec.get("description", ""))
        if spec.get("values"):
            continue                      # an enum lists EVERY option, so it privileges none
        for item in annotation._items_of(leaf):
            ans = item.get(leaf["field"])
            if ans in (None, "") or isinstance(ans, bool):
                continue
            if re.search(rf"(?<![\d.]){re.escape(str(ans))}(?![\d.])", guide):
                hits.append({"leaf": leaf["leaf"], "item_id": str(item.get("id", "")),
                             "field": leaf["field"], "answer": ans, "guide": guide})
    T.write_csv(out_dir / "primed_items.csv", ["leaf", "item_id", "field", "answer", "guide"],
                [[h[k] for k in ("leaf", "item_id", "field", "answer", "guide")] for h in hits])
    return hits


def _oracle_labels(leaves: List[Dict[str, Any]]) -> Dict[Tuple[str, str], Any]:
    out = {}
    for leaf in leaves:
        for item in annotation._items_of(leaf):
            out[(leaf["leaf"], str(item.get("id", "")))] = item.get(leaf["field"])
    return out


def score_sheet(sheet: Path, leaves: List[Dict[str, Any]], answer_types: Dict[str, str],
                field_types: Dict[str, str]) -> Dict[str, Any]:
    """Score a RETURNED blind pack. Refuses to report anything if nothing was filled in.

    That refusal is the point: an unfilled sheet scored naively gives perfect agreement of empty
    against empty and would print a confident kappa of 1.0 for a sitting that never happened."""
    if not sheet.exists():
        # The name only, never the absolute path: this refusal record ships in the release, and a
        # local filesystem path in a released artifact is a machine fingerprint (guardrail: strip
        # internal ids from anything that leaves the repo).
        return {"status": "NOT RUN", "reason": f"{sheet.name} does not exist", "n_filled": 0}
    rows = list(csv.DictReader(sheet.open()))
    filled = [r for r in rows if (r.get("annotator_answer") or "").strip()
              or (r.get("undeterminable") or "").strip()]
    if not filled:
        return {"status": "NOT RUN", "n_rows": len(rows), "n_filled": 0,
                "reason": "the sheet exists but no row carries a second reading"}
    truth = _oracle_labels(leaves)
    return _compare(filled, rows, truth, answer_types, field_types)


def _compare(filled, rows, truth, answer_types, field_types) -> Dict[str, Any]:
    """Pair each filled row against its withheld original and split by answer type."""
    paired, missing, disagreements = [], 0, []
    for r in filled:
        key = (r["leaf"], str(r["item_id"]))
        if key not in truth:
            missing += 1
            continue
        ftype = field_types.get(r["leaf"], "string")
        orig = _canon(truth[key], ftype)
        new = (None if (r.get("undeterminable") or "").strip()
               else _canon(r["annotator_answer"], ftype))
        paired.append({"row_id": r.get("row_id", ""), "leaf": r["leaf"], "item_id": r["item_id"],
                       "answer_type": answer_types.get(r["leaf"], ""), "original": orig,
                       "second": new, "agree": bool(orig == new)})
        if orig != new:
            disagreements.append(paired[-1])
    overall = cohens_kappa([p["original"] for p in paired], [p["second"] for p in paired])
    strata = {}
    for at in sorted({p["answer_type"] for p in paired}):
        sub = [p for p in paired if p["answer_type"] == at]
        strata[at] = dict(cohens_kappa([p["original"] for p in sub], [p["second"] for p in sub]),
                          kappa_meaningful=(at in KAPPA_TYPES))
    return {"status": "SCORED", "n_rows": len(rows), "n_filled": len(filled),
            "n_paired": len(paired), "n_unmatched": missing,
            "agreement": (sum(1 for p in paired if p["agree"]) / len(paired)) if paired else None,
            "overall": overall, "by_answer_type": strata,
            "n_disagreements": len(disagreements), "disagreements": disagreements}


def write_result(res: Dict[str, Any], out_dir: Path) -> Path:
    """Write the disagreement list adjudication operates on. Written even when nothing was filled,
    so the artefact records HONESTLY that the sitting has not happened."""
    path = out_dir / "agreement_result.csv"
    T.write_csv(path, ["row_id", "leaf", "item_id", "answer_type", "original_label",
                       "second_reading", "agree"],
                [[d["row_id"], d["leaf"], d["item_id"], d["answer_type"], d["original"],
                  d["second"], int(d["agree"])] for d in res.get("disagreements", [])])
    (out_dir / "agreement_result.json").write_text(json.dumps(
        {k: v for k, v in res.items() if k != "disagreements"}, indent=1, default=str))
    return path


def selftest() -> str:
    """Prove kappa on inputs whose answer is known in closed form, in BOTH directions, and prove
    the empty-sheet refusal. A scorer that has only been run on a filled sheet has not been shown
    to refuse an unfilled one -- and that refusal is the whole safety property."""
    perfect = cohens_kappa(["a", "b", "a", "b"], ["a", "b", "a", "b"])
    assert abs(perfect["kappa"] - 1.0) < 1e-12, f"identical labels must give kappa 1: {perfect}"
    opposite = cohens_kappa(["a", "a", "b", "b"], ["b", "b", "a", "a"])
    assert opposite["kappa"] < -0.9, f"systematic inversion must give kappa near -1: {opposite}"
    half = cohens_kappa(["a", "a", "b", "b"], ["a", "b", "a", "b"])
    assert abs(half["kappa"]) < 1e-12, f"chance-level agreement must give kappa 0: {half}"
    allsame = cohens_kappa(["a", "a"], ["a", "a"])
    assert allsame["kappa"] is None and not allsame["applicable"], \
        "a single-category space must refuse a kappa, not report 1.0"
    uniq = cohens_kappa([str(i) for i in range(40)], [str(i) for i in range(40)])
    assert uniq["po"] == 1.0 and not uniq["applicable"], \
        "40 distinct values over 40 items must be flagged as NOT kappa-applicable"
    empty = score_sheet(Path("/nonexistent/blind_pack_filled.csv"), [], {}, {})
    assert empty["status"] == "NOT RUN", "a missing sheet must report NOT RUN, never a score"
    return ("agreement selftest PASS - kappa correct at 1/0/-1, refuses a single-category space, "
            "flags all-distinct labels as not kappa-applicable, and reports NOT RUN on no sheet")


def main() -> None:
    """`python3 analysis/agreement.py score` -- the one command that scores a returned pack."""
    print(selftest())
    if len(sys.argv) > 1 and sys.argv[1] == "score":
        import run_all
        ctx = run_all.build_context()
        d = config.out_paths()["out"] / "annotation"
        leaves = annotation.stratified_sample(ctx["leaves"], ctx["answer_type"])
        ftypes = {l["leaf"]: l.get("type", "string") for l in ctx["leaves"]}
        res = score_sheet(d / "blind_pack_filled.csv", leaves, ctx["answer_type"], ftypes)
        write_result(res, d)
        print(json.dumps({k: v for k, v in res.items() if k != "disagreements"},
                         indent=1, default=str))


if __name__ == "__main__":
    main()
