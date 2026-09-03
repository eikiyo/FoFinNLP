"""
Location: paper-a/analysis/block1.py
Purpose: BLOCK 1 entry point. Item-level transfer at every k the corpus can support, each with its
         permutation null and a model-level bootstrap, written to out/tables/transfer_items.csv and
         out/tables/transfer_null.csv. Reports k=3 and k=4 alongside the pre-specified k=5 because
         the median moves from 0.000 to 0.200 across them, and a headline that depends on k is a
         fact about the statistic that has to be printed next to the statistic.
         Usage:  python3 analysis/block1.py [--perm N]
Functions: build(), run_k(), main()
Calls: transfer_items, contamination, oracle_audit, fold, matrix, analyses
Imports: json, sys, pathlib, typing
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analyses as an              # noqa: E402
import config                      # noqa: E402
import contamination as C          # noqa: E402
import fold                        # noqa: E402
import matrix                      # noqa: E402
import oracle_audit as OA          # noqa: E402
import rbo                         # noqa: E402
import statistics                  # noqa: E402
import tables_out as T             # noqa: E402
import transfer_items as TI        # noqa: E402
import transfer_robust as TR       # noqa: E402

KS = (3, 4, 5)
FIELDS = ("k", "median", "mean", "hits", "expected", "ratio", "n_pairs_sharing", "chance",
          "n_truncated", "n_pairs", "k_eff_a", "k_eff_b", "n_items")
STATS = ("median", "mean", "hits")


def build(population: str = "clean") -> Dict[str, Any]:
    """The item matrix every Block 1 statistic runs on. Clean by default, because that is the
    paper's headline reading; the flagged items are the subject of Block 2, not of this one.

    `population` exists so the before-the-audit contrast is produced by THIS code path rather than
    by a separate calculation. The paper quotes both numbers side by side, and a number computed
    once by hand at the console is not reproducible by anyone reading the repository: it was quoted
    in the draft for a day before the numbers-backed check found no CSV that rounds to it."""
    models, leaves, cells = matrix.load_cells()
    names = [l["leaf"] for l in leaves]
    frontier = an.capability_split(an.aggregate_wobble(models, names, cells))["frontier"]
    ids = C.oracle_ids(leaves)
    keep = C.keep_sets(names, C.flagged_index(OA.audit_all()), ids)
    # "all" is clean + flagged, which is every item MINUS the ones the author excluded after
    # adjudicating a model flag. It was keep=None (no filter at all) while no exclusion existed;
    # once one does, the before-the-audit contrast has to run on the same corpus as the after, or
    # the difference between them is partly the exclusion rather than the audit.
    keep["all"] = {n: keep["clean"][n] | keep["flagged"][n] for n in names}
    if population not in ("all", "clean", "flagged"):
        raise SystemExit(f"unknown population {population!r}; expected all, clean or flagged")
    per_cell = fold.collect(models, leaves)["per_cell"]
    keys, icells = TI.item_cells(models, names, per_cell, keep[population])
    if not keys:
        raise SystemExit(f"no {population} items survived the join -- refusing to report a "
                         "transfer statistic computed over an empty item set")
    return {"models": models, "frontier": frontier, "keys": keys, "cells": icells,
            "accuracy": TR.item_accuracy(models, names, per_cell, keys),
            "serving": config.serving_paths(),
            "family": config.model_families()}


def write_population_contrast(ctx_clean: Dict[str, Any], k: int) -> List[Dict[str, Any]]:
    """The same transfer statistic on both populations, one row each, from one code path.

    This is what licenses the claim that the audit exclusion removes about a quarter of the
    apparent sharing. Both rows must come from the same function or the difference is partly a
    difference between two calculations; the inflation figure was quoted from a console session
    before this existed, and no generated file contained it."""
    rows = []
    for pop, ctx in (("all", build("all")), ("clean", ctx_clean)):
        obs = TI.observed(ctx["models"], ctx["keys"], ctx["cells"], ctx["frontier"], k)
        rows.append({"population": pop, "k": k, "n_items": len(ctx["keys"]),
                     "mean": obs["mean"], "hits": obs["hits"], "expected": obs["expected"],
                     "ratio": obs["ratio"], "median": obs["median"], "chance": obs["chance"]})
    a, c = rows[0]["mean"], rows[1]["mean"]
    rows.append({"population": "inflation", "k": k, "n_items": "",
                 "mean": a - c, "hits": "", "expected": "",
                 "ratio": (a / c) if c else "", "median": "",
                 "chance": (a - c) / a if a else ""})
    T.write_csv(config.out_paths()["tables"] / "transfer_population.csv",
                ["population", "k", "n_items", "mean", "hits", "expected", "ratio", "median",
                 "chance"],
                [[r[f] for f in ("population", "k", "n_items", "mean", "hits", "expected",
                                 "ratio", "median", "chance")] for r in rows])
    return rows


def write_task_level(t: Path, ctx: Dict[str, Any], n_perm: int = 2000
                     ) -> List[Dict[str, Any]]:
    """The same statistic over TASKS instead of items, which is the comparison that chose the unit.

    The main text justifies ranking items by how much the task-level version truncates, and a
    justification whose numbers exist only in the prose cannot be audited. Routed through the same
    TI.observed as the headline, so the two readings differ by the unit and by nothing else."""
    by_task: Dict[str, List[str]] = {}
    for key in ctx["keys"]:
        by_task.setdefault(key.split("::")[0], []).append(key)
    keys = sorted(by_task)
    if not keys:
        raise SystemExit("no task measured by every frontier configuration -- refusing to report "
                         "a task-level transfer statistic over an empty set")
    # Aggregated from the SAME clean item cells the headline runs on, not reloaded from the raw
    # matrix: a task-level number built off all 60 tasks would differ from the item-level one by
    # the audit exclusion as well as by the unit, and the exhibit exists to isolate the unit.
    tcells = {m: {n: {"wobble": sum(ctx["cells"][m][x]["wobble"] > 0 for x in xs) / len(xs)}
                  for n, xs in by_task.items()} for m in ctx["models"]}
    rows = []
    for k in KS:
        obs = TI.observed(ctx["models"], keys, tcells, ctx["frontier"], k)
        # With its own null. The task-level ratio is far smaller than the item-level one, and a
        # reader is owed the means to tell a smaller effect from a coarser unit with a much higher
        # chance line. Same permutation, same seed, same code path as the headline.
        null = TI.permutation_null(ctx["models"], keys, tcells, ctx["frontier"], k, n_perm=n_perm)
        rows.append(dict(obs, k=k, **{f"p_{s}": TI.empirical_p(obs[s], null[s]["values"])
                                      for s in STATS}))
    T.write_csv(t / "transfer_tasks.csv", list(FIELDS) + [f"p_{s}" for s in STATS],
                [[r.get(f, "") for f in list(FIELDS) + [f"p_{s}" for s in STATS]] for r in rows])
    return rows


def robustness(ctx: Dict[str, Any], rows: List[Dict[str, Any]], k: int) -> Dict[str, Any]:
    """Blocks 1d to 1g at one k, all four together: each one alone is a number, and the reading
    only holds if the effect survives every one of them."""
    vecs = {m: {x: ctx["cells"][m][x]["wobble"] for x in ctx["keys"]} for m in ctx["frontier"]}
    pairs = rbo.pair_rbo(vecs, ctx["frontier"])
    bins = TR.strata(ctx["keys"], ctx["accuracy"])
    return {"rbo_pairs": pairs,
            "rbo_median": statistics.median([p["rbo"] for p in pairs]),
            "rbo_median_normalised": statistics.median([p["normalised"] for p in pairs
                                                        if p["normalised"] is not None]),
            "strata": TR.accuracy_matched(ctx["cells"], ctx["frontier"], bins, k),
            "paths": TR.path_split(rows, ctx["serving"], k, ctx["family"]),
            "loo": TR.leave_one_out(ctx["keys"], ctx["cells"], ctx["frontier"], k)}


def run_k(ctx: Dict[str, Any], k: int, n_perm: int, n_boot: int) -> Dict[str, Any]:
    """Observed, null and bootstrap for one k, always together: an observed value without its null
    is not a result, and the null is what makes a median of 0.200 on a five-item set legible."""
    obs = TI.observed(ctx["models"], ctx["keys"], ctx["cells"], ctx["frontier"], k)
    null = TI.permutation_null(ctx["models"], ctx["keys"], ctx["cells"], ctx["frontier"], k,
                               n_perm=n_perm)
    boot = TI.model_bootstrap(obs["rows"], ctx["frontier"], k, n_boot=n_boot)
    return {"k": k, "obs": obs, "null": null, "boot": boot,
            "p": {s: TI.empirical_p(obs[s], null[s]["values"]) for s in STATS}}


def main(n_perm: int = 2000, n_boot: int = 2000) -> List[Dict[str, Any]]:
    print(TI.selftest())
    ctx = build()
    print(f"  frontier: {len(ctx['frontier'])} configurations; clean items measurable by every "
          f"configuration: {len(ctx['keys'])}")
    out = [run_k(ctx, k, n_perm, n_boot) for k in KS]
    t = config.out_paths()["tables"]
    T.write_csv(t / "transfer_items.csv",
                list(FIELDS) + ["p_median", "p_mean", "p_hits",
                                "boot_median_lo", "boot_median_hi", "boot_mean_lo", "boot_mean_hi"],
                [[r["k"] if f == "k" else r["obs"].get(f, "") for f in FIELDS]
                 + [r["p"][s] for s in STATS]
                 + [r["boot"]["median"]["lo"], r["boot"]["median"]["hi"],
                    r["boot"]["mean"]["lo"], r["boot"]["mean"]["hi"]] for r in out])
    T.write_csv(t / "transfer_null.csv",
                ["k", "statistic", "observed", "null_median", "null_p95", "null_p97_5",
                 "null_max", "n_perm", "p_permutation"],
                [[r["k"], s, r["obs"][s], r["null"][s]["median"], r["null"][s]["p95"],
                  r["null"][s]["p97_5"], r["null"][s]["max"], r["null"]["n_perm"], r["p"][s]]
                 for r in out for s in STATS])
    # The null's own DRAWS, not only its percentiles. A figure that shows an observed value
    # against a null has to draw the null's shape, and four order statistics cannot be drawn:
    # summarising here and re-simulating in the figure would put two different nulls in one paper.
    T.write_csv(t / "transfer_null_draws.csv", ["k", "statistic", "draw", "value"],
                [[r["k"], s, i, v] for r in out for s in STATS
                 for i, v in enumerate(r["null"][s]["values"])])
    (config.out_paths()["out"] / "block1_transfer.json").write_text(json.dumps(
        [{"k": r["k"], "observed": {f: r["obs"].get(f) for f in FIELDS},
          "null": {s: {f: r["null"][s][f] for f in ("median", "p95", "p97_5", "max")}
                   for s in STATS},
          "n_perm": r["null"]["n_perm"], "seed": r["null"]["seed"],
          "bootstrap": r["boot"], "p_permutation": r["p"]} for r in out], indent=1))
    rb = robustness(ctx, out[-1]["obs"]["rows"], KS[-1])
    write_robustness(t, rb, KS[-1])
    tl = write_task_level(t, ctx, n_perm)
    print("  task level: " + "; ".join(
        f"k={r['k']} truncated {r['n_truncated']}/{r['n_pairs']}" for r in tl))
    pop = write_population_contrast(ctx, KS[-1])
    print(f"  population contrast at k={KS[-1]}: "
          + "; ".join(f"{r['population']} mean {float(r['mean']):.4f}"
                      + (f" ratio {float(r['ratio']):.2f}x" if r["ratio"] != "" else "")
                      for r in pop))
    report(out, rb)
    return {"transfer": out, "robustness": rb}


def report(out: List[Dict[str, Any]], rb: Dict[str, Any]) -> None:
    """Print every statistic and every check. Separated from main so the writing of the tables and
    the reading of them are not one 60-line block in which a missing line is invisible."""
    for r in out:
        o, n, b = r["obs"], r["null"], r["boot"]
        print(f"  k={r['k']}  truncated {o['n_truncated']}/{o['n_pairs']}  "
              f"pairs sharing at least one item {o['n_pairs_sharing']}/{o['n_pairs']}")
        for stat in ("median", "mean"):
            print(f"       {stat:6s} {o[stat]:.4f}  boot [{b[stat]['lo']:.4f}, "
                  f"{b[stat]['hi']:.4f}]  null {n[stat]['median']:.4f} "
                  f"p95 {n[stat]['p95']:.4f}  p={r['p'][stat]}")
        print(f"       hits   {o['hits']} vs {o['expected']:.2f} expected = "
              f"{o['ratio']:.2f}x  null {n['hits']['median']:.1f} "
              f"p95 {n['hits']['p95']:.1f}  p={r['p']['hits']}")
    print(f"\n  1d RBO p={rbo.P_DEFAULT}: median {rb['rbo_median']:.4f}, "
          f"normalised {rb['rbo_median_normalised']:.4f} over {len(rb['rbo_pairs'])} pairs")
    print("  1e accuracy-matched:")
    for s in rb["strata"]:
        print(f"       {s['stratum']}  n={s['n_items']:3d}  " +
              (f"mean {s['mean']:.4f}  {s['hits']} hits vs {s['expected']:.2f} = "
               f"{s['ratio']:.2f}x" if s["usable"] else f"NOT USABLE: {s['reason']}"))
    print("  1f serving path:")
    for p in rb["paths"]:
        xf = ("n/a" if p["mean_cross_family"] is None
              else f"{p['mean_cross_family']:.4f} (n={p['n_pairs_cross_family']})")
        print(f"       {p['pairing']:18s} n={p['n_pairs']:3d}  mean {p['mean']:.4f}  "
              f"cross-family {xf}")
    print("  1g leave-one-out (mean, hits ratio):")
    for r in rb["loo"]:
        print(f"       drop {r['dropped']:22s} mean {r['mean']:.4f}  {r['ratio']:.2f}x")


def write_robustness(t: Path, rb: Dict[str, Any], k: int) -> None:
    """One CSV per check. Separate files because they answer separate objections and a reader
    chasing one of them should not have to parse the other three."""
    T.write_csv(t / "transfer_rbo.csv",
                ["model_a", "model_b", "rbo", "normalised", "ceiling", "depth_a", "depth_b",
                 "weight_covered", "p"],
                [[p[c] for c in ("model_a", "model_b", "rbo", "normalised", "ceiling", "depth_a",
                                 "depth_b", "weight_covered", "p")] for p in rb["rbo_pairs"]])
    T.write_csv(t / "transfer_accuracy_matched.csv",
                ["stratum", "n_items", "usable", "mean", "median", "hits", "expected", "ratio",
                 "n_pairs_sharing", "reason"],
                [[s.get(c, "") for c in ("stratum", "n_items", "usable", "mean", "median", "hits",
                                         "expected", "ratio", "n_pairs_sharing", "reason")]
                 for s in rb["strata"]])
    T.write_csv(t / "transfer_serving_path.csv",
                ["pairing", "n_pairs", "mean", "median", "n_pairs_cross_family",
                 "mean_cross_family"],
                [[p["pairing"], p["n_pairs"], p["mean"], p["median"],
                  p["n_pairs_cross_family"], p["mean_cross_family"]] for p in rb["paths"]])
    T.write_csv(t / "transfer_leave_one_out.csv",
                ["dropped", "n_models", "mean", "hits", "ratio"],
                [[r["dropped"], r["n_models"], r["mean"], r["hits"], r["ratio"]]
                 for r in rb["loo"]])


if __name__ == "__main__":
    argv = sys.argv
    perm = int(argv[argv.index("--perm") + 1]) if "--perm" in argv else 2000
    main(n_perm=perm)
