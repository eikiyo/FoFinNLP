"""
Location: paper-a/analysis/repair_analysis.py
Purpose: Block 2c. Score the repair experiment against the threshold registered in
         PREREG_UPGRADE.md before any of it was run: does the repaired-condition pooled wobble
         fall below 0.161, the midpoint of the clean rate and the flagged rate? Paired
         within-item and within-model, so no item enters one condition and not the other.
         Usage:  python3 analysis/repair_analysis.py
Functions: condition_rows(), paired_cells(), summarise(), main()
Calls: fold.item_rates (the paper's own per-item flip definition), categories.wilson,
       contamination.newcombe
Imports: json, sys, pathlib, config, fold, categories, contamination, repair_windows, repair_run
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

import categories                    # noqa: E402
import config                        # noqa: E402
import contamination                 # noqa: E402
import fold                          # noqa: E402
import repair_run as RR              # noqa: E402
import repair_windows as RW          # noqa: E402
import tables_out as T               # noqa: E402

# Registered in PREREG_UPGRADE.md before the probe ran, as the midpoint of the clean rate (0.086)
# and the flagged rate (0.235). Read here as a constant and never recomputed from current data:
# a threshold rederived from the numbers it judges is not a threshold.
THRESHOLD = 0.161


def read_runs(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def condition_rows(task, instances, runs, field) -> Dict[str, Dict[str, Any]]:
    """Per-item rows keyed by ITEM ID, using the paper's own flip definition.

    Keyed by id rather than by position because the two conditions do not share a positional
    index: the repaired condition holds only the fourteen repaired items, the original holds all
    of its leaf's. Pairing on position would silently compare one item's before to another
    item's after."""
    rows = fold.item_rates(task, instances, runs, field)
    return {instances[r["item"]][0]["id"]: r for r in rows if r["item"] < len(instances)}


CONTROL = config.PAPER_ROOT / "out" / "repair" / "control"
LOCAL = ("gemma3-1b", "gemma3-1b-qat")


def before_rows(label, leaf_name, leaf_dir, task, full, rep, field):
    """The BEFORE condition, taken from the build that also produced the AFTER condition.

    For the ten hosted configurations that is the published arm's stored runs. For the two locally
    served ones it is out/repair/control/: those models were absent from ollama and had to be
    re-obtained, and the run manifest records no model digest, so the published arm's build cannot
    be identified. Pairing a repaired window measured on today's build against an original window
    measured on an unknown one would put a possible model change inside the effect being measured.

    Re-running the original window on the SAME build removes the confound outright, which is why
    the answer to an unverifiable build is to re-run rather than to drop the configuration. The two
    1B models carry by far the highest wobble in the lineup, so dropping them would lower the
    pooled repaired rate and push the result toward the registered threshold."""
    if label in LOCAL:
        return condition_rows(task, rep, read_runs(CONTROL / leaf_name / f"{label}.jsonl"), field)
    return condition_rows(task, full, read_runs(leaf_dir / f"runs_{label}.jsonl"), field)


def paired_cells(engine_mods) -> List[Dict[str, Any]]:
    """One row per (leaf, item, configuration) measured in BOTH conditions."""
    runner, _harness, preflight, _scorer = engine_mods
    leaves = RR.build_leaves(runner)
    out = []
    for leaf_name, (leaf_dir, task, field) in sorted(leaves.items()):
        full, _ = runner.load_instances(leaf_dir, field)
        rep = RR.repaired_instances(leaf_dir, field, runner)
        for label, _kind, _mid in preflight.LINEUP:
            before = before_rows(label, leaf_name, leaf_dir, task, full, rep, field)
            after = condition_rows(task, rep,
                                   read_runs(RR.RESULTS / leaf_name / f"{label}.jsonl"), field)
            for iid, a in after.items():
                b = before.get(iid)
                if b is None or b["flipped"] is None or a["flipped"] is None:
                    continue
                out.append({"leaf": leaf_name, "item": iid, "model": label,
                            "before_flipped": int(b["flipped"]), "before_n": b["n"],
                            "after_flipped": int(a["flipped"]), "after_n": a["n"],
                            "before_dispersion": b["dispersion"],
                            "after_dispersion": a["dispersion"]})
    return out


def summarise(cells: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Pooled wobble in each condition, their difference, and the registered verdict."""
    n = len(cells)
    kb = sum(c["before_flipped"] for c in cells)
    ka = sum(c["after_flipped"] for c in cells)
    wb, wa = (kb / n if n else None), (ka / n if n else None)
    lo_b, hi_b = categories.wilson(kb, n) or (None, None)
    lo_a, hi_a = categories.wilson(ka, n) or (None, None)
    diff = contamination.newcombe(kb, n, ka, n)
    return {"n_cells": n, "n_items": len({c["item"] for c in cells}),
            "n_models": len({c["model"] for c in cells}),
            "before_flipped": kb, "before_wobble": wb, "before_lo": lo_b, "before_hi": hi_b,
            "after_flipped": ka, "after_wobble": wa, "after_lo": lo_a, "after_hi": hi_a,
            "difference": diff, "threshold": THRESHOLD,
            # The verdict is the interval's position, not the point estimate alone. A point below
            # the threshold whose interval straddles it has not met a falsifiable prediction.
            "meets_threshold": (wa is not None and wa < THRESHOLD),
            "interval_below_threshold": (hi_a is not None and hi_a < THRESHOLD)}


def by_task(cells: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Per-task rows plus a POOLED row, so the paper's table is formatted from data rather than
    from a per-task figure retyped into a caption.

    The per-task split is descriptive and is NOT the registered test: the prediction is on the
    pooled rate and is scored there. It is reported because one task moves and two do not, and a
    pooled null that hides a split inside it would be a less honest null than one that shows it."""
    # POOLED_COMPLETE is the sensitivity reading over cells with all 20 responses in BOTH
    # conditions. It is written as data rather than quoted from a console because the paper states
    # it, and the numbers check cannot tell a figure backed by its own row from one that coincides
    # with an unrelated value elsewhere: 0.187 is also the cross-model transfer mean, so quoting it
    # without its own row would have passed that check while being backed by nothing relevant.
    groups = {"POOLED": cells,
              "POOLED_COMPLETE": [c for c in cells if c["before_n"] == 20 and c["after_n"] == 20]}
    rows = []
    for leaf in sorted({c["leaf"] for c in cells}) + list(groups):
        sub = groups.get(leaf) or [c for c in cells if c["leaf"] == leaf]
        s = summarise(sub)
        d = s["difference"] or {}
        rows.append({"task": leaf, "n_items": s["n_items"], "n_cells": s["n_cells"],
                     "before_wobble": s["before_wobble"], "before_lo": s["before_lo"],
                     "before_hi": s["before_hi"], "after_wobble": s["after_wobble"],
                     "after_lo": s["after_lo"], "after_hi": s["after_hi"],
                     "difference": d.get("d"), "difference_lo": d.get("lo"),
                     "difference_hi": d.get("hi")})
    return rows


def main() -> Dict[str, Any]:
    mods = RR.engine()
    cells = paired_cells(mods)
    if not cells:
        raise SystemExit("no paired cells: the repaired condition has produced nothing yet, and "
                         "an empty pairing must never be reported as a null result")
    s = summarise(cells)
    t = config.out_paths()["tables"]
    cols = ["task", "n_items", "n_cells", "before_wobble", "before_lo", "before_hi",
            "after_wobble", "after_lo", "after_hi", "difference", "difference_lo",
            "difference_hi"]
    T.write_csv(t / "repair_by_task.csv", cols,
                [[r[c] for c in cols] for r in by_task(cells)])
    T.write_csv(t / "repair_paired.csv",
                ["leaf", "item", "model", "before_flipped", "before_n", "after_flipped",
                 "after_n", "before_dispersion", "after_dispersion"],
                [[c[k] for k in ("leaf", "item", "model", "before_flipped", "before_n",
                                 "after_flipped", "after_n", "before_dispersion",
                                 "after_dispersion")] for c in cells])
    (config.out_paths()["out"] / "block2c_result.json").write_text(json.dumps(s, indent=1))
    d = s["difference"] or {}
    print(f"  paired cells: {s['n_cells']} ({s['n_items']} items x {s['n_models']} configurations)")
    print(f"  BEFORE (original window): {s['before_flipped']}/{s['n_cells']} = "
          f"{s['before_wobble']:.4f}  [{s['before_lo']:.4f}, {s['before_hi']:.4f}]")
    print(f"  AFTER  (repaired window): {s['after_flipped']}/{s['n_cells']} = "
          f"{s['after_wobble']:.4f}  [{s['after_lo']:.4f}, {s['after_hi']:.4f}]")
    if d:
        # contamination.newcombe names the point estimate `d`, not `difference`. Reading the key
        # that is actually returned rather than the one this file would have called it.
        print(f"  difference (before - after): {d['d']:+.4f} [{d['lo']:.4f}, {d['hi']:.4f}] "
              f"(Newcombe), {'excludes' if d['excludes_zero'] else 'includes'} zero")
    print(f"\n  REGISTERED THRESHOLD {THRESHOLD}: repaired wobble "
          f"{'BELOW -> prediction met' if s['meets_threshold'] else 'NOT below -> PREDICTION FAILED'}"
          f"; its interval {'also lies' if s['interval_below_threshold'] else 'does NOT lie'} "
          f"entirely below the threshold")
    return s


if __name__ == "__main__":
    main()
