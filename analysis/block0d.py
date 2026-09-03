"""
Location: paper-a/analysis/block0d.py
Purpose: Entry point for the window-failure TAXONOMY and the Block 2a probe. Splits the items whose
         validating quote is not in their window into the two populations the single flag conflated
         -- evidence genuinely absent versus an answer that must be COMPUTED from operands the
         window does supply -- measures wobble in each against the clean rate, and probes the
         remaining unresolved items against EDGAR. Writes out/tables/window_buckets.csv and
         out/tables/bucket_wobble.csv.  Usage:  python3 analysis/block0d.py [--probe]
Functions: buckets(), failure_labels(), bucket_wobble(), main()
Calls: oracle_audit, windowability, contamination, matrix, fold, categories, probe_edgar
Imports: sys, json, pathlib, typing
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

import categories                  # noqa: E402
import adjudication as ADJ
import config                      # noqa: E402
import contamination as C          # noqa: E402
import fold                        # noqa: E402
import matrix                      # noqa: E402
import oracle_audit as OA          # noqa: E402
import probe_edgar                 # noqa: E402
import quotematch                  # noqa: E402
import repair_windows as RW        # noqa: E402
import tables_out as T             # noqa: E402
import windowability as W          # noqa: E402

# Groups reported separately because they are different failures with different repairs. Pooling
# them was the defect: a computation effect and a provenance effect were being read as one number.
GROUPS = ("computational", "evidence-absent", "quote-absent-from-source")


def buckets(rows: List[Dict[str, Any]], index) -> Dict[Tuple[str, str], str]:
    """(leaf, item) -> bucket, for every item whose quote is not verbatim in its window."""
    return {(c["leaf"], c["item"]): c["bucket"]
            for c in W.classify_rows(rows, index["window"], index["quote"])}


def _keep(names, ids, pred) -> Dict[str, set]:
    """Positional index sets, built the SAME way contamination.keep_sets builds them, so a bucket
    and the published partition cannot disagree about which position an item occupies."""
    return {n: {i for i, iid in enumerate(ids.get(n, [])) if pred(n, iid)} for n in names}


def failure_labels(rows, bk) -> Dict[Tuple[str, str], str]:
    """(leaf, item) -> failure group. The ONE derivation of an item's group: group_sets and the
    stratified frame both read it, so two artifacts cannot disagree about where an item sits.
    Author-excluded items get a label no reported group matches, so the clean set (defined by
    exclusion from every other group) drops them instead of quietly absorbing them; an item
    already bucketed by its window is not re-labelled by its source, which would count it twice."""
    label = {(n, i): "author-excluded" for n, items in ADJ.exclusions().items() for i in items}
    label.update({k: v for k, v in bk.items() if k not in label})
    absent = {(r["leaf"], r["item"]) for r in rows if r["quote_in_full"] is False}
    label.update({k: "quote-absent-from-source" for k in absent if k not in label})
    return label


def group_sets(names, ids, rows, bk) -> Dict[str, Dict[str, set]]:
    """The four positional index sets, built to PARTITION. Clean is defined by exclusion from
    every other group; the labelling rules live in failure_labels."""
    label = failure_labels(rows, bk)
    sets = {"clean": _keep(names, ids, lambda n, i: (n, i) not in label)}
    for g in GROUPS:
        sets[g] = _keep(names, ids, lambda n, i, g=g: label.get((n, i)) == g)
    return sets


def bucket_wobble(models, leaves, rows, bk) -> List[Dict[str, Any]]:
    """Wobble per group with a Wilson interval, and Newcombe against the clean rate. The
    quote-absent-from-source group is carried even though it is expected to be null: a group
    reported only when it comes out positive is not a measurement."""
    names = [l["leaf"] for l in leaves]
    ids = C.oracle_ids(leaves)
    per_cell = fold.collect(models, leaves)["per_cell"]
    sets = group_sets(names, ids, rows, bk)

    def counts(keep):
        sub = C.subset_cells(models, names, per_cell, keep)
        return (sum(sub[m][n]["flipped"] for m in models for n in names),
                sum(sub[m][n]["n_items"] for m in models for n in names))

    base = counts(sets["clean"])
    out = []
    for g, keep in sets.items():
        k, n = counts(keep)
        lo, hi = categories.wilson(k, n) if n else (None, None)
        d = C.newcombe(k, n, *base) if (g != "clean" and n) else None
        out.append({"group": g, "items": sum(len(v) for v in keep.values()), "pairs": n,
                    "flipped": k, "wobble": (k / n) if n else None, "lo": lo, "hi": hi,
                    "diff": d["d"] if d else None, "diff_lo": d["lo"] if d else None,
                    "diff_hi": d["hi"] if d else None,
                    "excludes_zero": int(d["excludes_zero"]) if d else ""})
    whole = counts({n: set(range(len(ids.get(n, [])))) for n in names})[1]
    # The author-excluded items are counted back in for the partition test only. They belong to no
    # reported group, but they are still items in the corpus, and a check that quietly lowered its
    # own denominator to match would stop being able to detect an item that fell out for any OTHER
    # reason -- which is the one thing this check exists to do.
    ex_sets = {n: {i for i, iid in enumerate(ids.get(n, []))
                   if iid in ADJ.exclusions().get(n, set())} for n in names}
    n_excluded = counts(ex_sets)[1]
    if sum(r["pairs"] for r in out) + n_excluded != whole:
        raise SystemExit(f"BUCKETS DO NOT PARTITION: groups sum to "
                         f"{sum(r['pairs'] for r in out) + n_excluded} "
                         f"pairs, corpus has {whole}. An item is in two groups or in none.")
    # Sensitivity, not a partition member: the evidence-absent group WITHOUT the 4 items
    # Appendix C reclassifies as computational. Reported so a reader who rejects our choice to
    # keep them in the group can see the rate their removal produces. Added after the partition
    # check on purpose; counting it there would double-count its 13 items.
    label = failure_labels(rows, bk)
    keep13 = _keep(names, ids, lambda n, i: label.get((n, i)) == "evidence-absent"
                   and (n, i) not in RW.NOT_REPAIRABLE)
    k13, n13 = counts(keep13)
    if n13 == 0:
        raise SystemExit("SENSITIVITY GROUP EMPTY: evidence-absent minus the 4 reclassified "
                         "items measured no pairs; the exclusion list no longer matches the "
                         "bucket table.")
    lo13, hi13 = categories.wilson(k13, n13)
    d13 = C.newcombe(k13, n13, *base)
    out.append({"group": "evidence-absent-excl-reclassified",
                "items": sum(len(v) for v in keep13.values()), "pairs": n13, "flipped": k13,
                "wobble": k13 / n13, "lo": lo13, "hi": hi13, "diff": d13["d"],
                "diff_lo": d13["lo"], "diff_hi": d13["hi"],
                "excludes_zero": int(d13["excludes_zero"])})
    return out


def main(do_probe: bool = False) -> Dict[str, Any]:
    print(quotematch.selftest())
    print(W.selftest())
    print(probe_edgar.selftest())
    t = config.out_paths()["tables"]
    models, leaves, cells = matrix.load_cells()
    rows = OA.audit_all()
    index = OA.corpus_index()
    bk = buckets(rows, index)
    by_row = {(r["leaf"], r["item"]): r for r in rows}
    T.write_csv(t / "window_buckets.csv",
                ["leaf", "item", "answer", "bucket", "source_state", "reason"],
                [[k[0], k[1], str(by_row[k]["answer"])[:40], v, by_row[k]["source_state"],
                  by_row[k]["window_reason"][:110]] for k, v in sorted(bk.items())])
    wob = bucket_wobble(models, leaves, rows, bk)
    T.write_csv(t / "bucket_wobble.csv",
                ["group", "items", "pairs", "flipped", "wobble", "lo", "hi",
                 "diff", "diff_lo", "diff_hi", "excludes_zero"],
                [[r.get(c, "") for c in ("group", "items", "pairs", "flipped", "wobble", "lo",
                                         "hi", "diff", "diff_lo", "diff_hi", "excludes_zero")]
                 for r in wob])
    for r in wob:
        d = "" if r.get("diff") is None else (f"  vs clean {r['diff']:+.4f} "
                                              f"[{r['diff_lo']:+.4f}, {r['diff_hi']:+.4f}]")
        print(f"  {r['group']:26s} items={r['items']:3d} pairs={r['pairs']:5d} "
              f"wobble={r['wobble']:.4f} [{r['lo']:.4f}, {r['hi']:.4f}]{d}")
    probe = None
    if do_probe:
        probe = probe_edgar.run(rows, bk, index)
        (config.out_paths()["out"] / "prereg2a" / "probe_result.json").parent.mkdir(
            parents=True, exist_ok=True)
        (config.out_paths()["out"] / "prereg2a" / "probe_result.json").write_text(
            json.dumps(probe, indent=1))
        print(f"\nPROBE: {probe['n_probed']} fetched -> {probe['counts']}")
        for r in probe["results"]:
            print(f"  {r['leaf'][:28]:28s} {r['item'][:26]:26s} {r['verdict']:12s} "
                  f"{r['chars']:>7} chars  {r['reason'][:60]}")
    return {"buckets": bk, "wobble": wob, "probe": probe}


if __name__ == "__main__":
    main(do_probe="--probe" in sys.argv)
