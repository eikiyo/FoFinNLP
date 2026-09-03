"""
Location: paper-a/analysis/contam_tables.py
Purpose: Write the §0 gate's CSVs. Two families: the contamination evidence itself
         (out/tables/contamination_*.csv), and a full CLEAN-ONLY mirror of every table the paper's
         exhibits read from (out/tables/clean/*.csv), written with the SAME headers as the
         all-item originals so `paper/make_tables.py` reads one shape from either directory.
Functions: write_contamination(), write_delta(), write_clean_mirror(), headline_deltas()
Calls: tables_out.write_csv (the one shared CSV writer), categories.wilson
Imports: pathlib, typing, categories, tables_out
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import categories
import tables_out as T

CONTAM_HEADER = ["model", "flagged_flipped", "flagged_items", "flagged_wobble", "flagged_lo",
                 "flagged_hi", "clean_flipped", "clean_items", "clean_wobble", "clean_lo",
                 "clean_hi", "difference", "difference_lo", "difference_hi", "excludes_zero"]


def write_contamination(rows: List[Dict[str, Any]], t: Path) -> Path:
    """The evidence table: per model and pooled, wobble on flagged vs clean items with Wilson
    intervals on both and on the difference. `n` rides on every row so a wide interval can be read
    as NO POWER rather than NO EFFECT."""
    return T.write_csv(t / "contamination_by_model.csv", CONTAM_HEADER,
                       [[r["model"], r["k_flagged"], r["n_flagged"], T.fmt(r["w_flagged"], 6),
                         T.fmt(r["lo_flagged"], 6), T.fmt(r["hi_flagged"], 6),
                         r["k_clean"], r["n_clean"], T.fmt(r["w_clean"], 6),
                         T.fmt(r["lo_clean"], 6), T.fmt(r["hi_clean"], 6),
                         T.fmt((r["diff"] or {}).get("d"), 6),
                         T.fmt((r["diff"] or {}).get("lo"), 6),
                         T.fmt((r["diff"] or {}).get("hi"), 6),
                         int(bool((r["diff"] or {}).get("excludes_zero")))] for r in rows])


def task_rows(leaves: List[Dict[str, Any]], gate: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Per task: how many items it has, how many the audit flagged, and how many survive. The
    per-model tables cannot show this, and it turned out to be the most consequential thing the
    gate found -- the defect is CONCENTRATED, not scattered, and nine tasks lose every item."""
    keep = gate["keep"]
    out = []
    for l in leaves:
        n = len(keep["clean"][l["leaf"]]) + len(keep["flagged"][l["leaf"]])
        out.append({"leaf": l["leaf"], "family": l["family"], "n_items": n,
                    "n_flagged": len(keep["flagged"][l["leaf"]]),
                    "n_clean": len(keep["clean"][l["leaf"]])})
    return out


def category_counts(rows: List[Dict[str, Any]]) -> List[List[Any]]:
    """Tasks per category, before and after the exclusion. This is what Table 3's column headers
    have to carry, and what decides which categories are still estimable."""
    fams = sorted({r["family"] for r in rows})
    return [[f, sum(1 for r in rows if r["family"] == f),
             sum(1 for r in rows if r["family"] == f and r["n_clean"] > 0),
             sum(r["n_items"] for r in rows if r["family"] == f),
             sum(r["n_clean"] for r in rows if r["family"] == f)] for f in fams]


def write_tasks(rows: List[Dict[str, Any]], t: Path) -> Path:
    return T.write_csv(t / "contamination_by_task.csv",
                       ["leaf", "family", "n_items", "n_flagged", "n_clean", "wiped_out"],
                       [[r["leaf"], r["family"], r["n_items"], r["n_flagged"], r["n_clean"],
                         int(r["n_clean"] == 0 and r["n_items"] > 0)] for r in rows])


def write_categories(rows: List[Dict[str, Any]], t: Path) -> Path:
    return T.write_csv(t / "contamination_by_category.csv",
                       ["category", "tasks_all", "tasks_clean", "items_all", "items_clean"],
                       category_counts(rows))


def headline_deltas(gate: Dict[str, Any], rb: Dict[str, Any],
                    models: Sequence[str], tasks: List[Dict[str, Any]]) -> List[List[Any]]:
    """Every number the paper quotes, in both readings. Built as one list so the audit document and
    the CSV cannot disagree: the markdown renders these rows, it does not recompute them."""
    A, C = gate["all_items"], gate["clean_only"]
    da, dc = rb["all"]["diag"], rb["clean"]["diag"]
    ca, cc = rb["all"]["cons"], rb["clean"]["cons"]
    out: List[List[Any]] = [
        ["items in the analysis", sum(r["n_items"] for r in tasks),
         sum(r["n_clean"] for r in tasks), "count"],
        ["tasks with at least one item in the analysis", sum(1 for r in tasks if r["n_items"]),
         sum(1 for r in tasks if r["n_clean"]), "count"],
        ["model-item pairs measured", da["pooled_p"]["n_items"], dc["pooled_p"]["n_items"],
         "count"]]
    for m in sorted(models, key=lambda x: A["agg"][x]):
        out.append([f"aggregate wobble: {m}", A["agg"][m], C["agg"][m], "rate"])
    for k in (5, 10):
        for field, unit in (("median", "rate"), ("chance", "rate"), ("median_lift", "rate"),
                            ("n_truncated", "count")):
            out.append([f"transfer k={k} frontier-only: {field}",
                        A["transfer"][k][field], C["transfer"][k][field], unit])
    out += [["active tasks (non-zero wobble in >=1 model)", len(A["active"]), len(C["active"]),
             "count"],
            ["split-half reliability, median r_full",
             _med([r["r_full"] for r in rb["all"]["rel"]]),
             _med([r["r_full"] for r in rb["clean"]["rel"]]), "correlation"],
            # Three DIFFERENT quantities that a careless sentence merges into one. Answered
            # IDENTICALLY on all runs is the complement of wobble and includes items answered
            # identically and wrongly. Answered CORRECTLY on all runs is p=1. Answered WRONGLY on
            # all runs is p=0. Naming each one separately is the only way the prose can quote the
            # one it means.
            ["share answered identically on all runs (1 - wobble)",
             1 - _pool(gate, "cells_all"), 1 - _pool(gate, "cells_clean"), "share"],
            ["share answered correctly on all runs (p=1)",
             da["pooled_p"]["frac_one"], dc["pooled_p"]["frac_one"], "share"],
            ["share answered wrong on all runs (p=0)",
             da["pooled_p"]["frac_zero"], dc["pooled_p"]["frac_zero"], "share"],
            # The observable band has ONE definition in this project and ONE implementation:
            # folddiag.band_count, an exact CLOSED test 0.3 <= p <= 0.7 over the p values. It was
            # previously summed from histogram bins, whose linspace edges are 0.30000000000000004
            # and 0.7000000000000001, so the count silently included the pairs at exactly p=0.7 and
            # dropped those at exactly p=0.3 while both the prose and the figure claimed the
            # half-open predicate. Figure 1(a) reads this same field.
            ["pairs in the observable band 0.3 <= p <= 0.7", _band(da["pooled_p"]),
             _band(dc["pooled_p"]), "count"],
            ["share in the observable band 0.3 <= p <= 0.7",
             _band(da["pooled_p"]) / da["pooled_p"]["n_items"],
             _band(dc["pooled_p"]) / dc["pooled_p"]["n_items"], "share"],
            # The half-open reading, reported beside it so a claim that turns on which endpoint is
            # open is visible as such rather than resting on how a float rounded.
            ["pairs in the band under the half-open reading 0.3 <= p < 0.7",
             da["pooled_p"]["band_n_halfopen"], dc["pooled_p"]["band_n_halfopen"], "count"],
            ["tasks at accuracy >= 0.9", _hi(da)["n_leaves"], _hi(dc)["n_leaves"], "count"],
            ["max structurally reachable wobble at accuracy >= 0.9",
             _hi(da)["max_structural"], _hi(dc)["max_structural"], "rate"],
            ["max observed wobble at accuracy >= 0.9",
             _hi(da)["max_observed"], _hi(dc)["max_observed"], "rate"],
            ["wobble-accuracy rho", da["rho"]["rho"], dc["rho"]["rho"], "correlation"],
            ["residual rho after structural decomposition (calibrated)",
             da["surviving"]["rho_residual_cal"], dc["surviving"]["rho_residual_cal"],
             "correlation"],
            ["conservative worst-to-mean ratio, median (3-task floor)",
             ca[3]["median_cons"], cc[3]["median_cons"], "ratio"],
            ["models above 2x at the bound (3-task floor)",
             ca[3]["n_over_2x"], cc[3]["n_over_2x"], "count"],
            ["conservative worst-to-mean ratio, median (5-task floor)",
             ca[5]["median_cons"], cc[5]["median_cons"], "ratio"],
            ["capability gradient slope, frontier only",
             ca["gradient"][1]["slope"], cc["gradient"][1]["slope"], "slope"],
            ["capability gradient R2, frontier only",
             ca["gradient"][1]["r2"], cc["gradient"][1]["r2"], "r2"]]
    return out


def _hi(diag: Dict[str, Any]) -> Dict[str, Any]:
    return [r for r in diag["frontier"] if r["decile"] == "0.9-1.0"][0]


def _pool(gate: Dict[str, Any], key: str) -> float:
    """Pooled wobble over every configuration and every task in one reading: total unstable items
    over total measured items. Counts summed, never per-model rates averaged."""
    cells = gate[key]
    f = sum(c["flipped"] for m in cells for c in [cells[m][n] for n in cells[m]])
    k = sum(c["n_items"] for m in cells for c in [cells[m][n] for n in cells[m]])
    return f / k if k else 0.0


def _band(pooled: Dict[str, Any]) -> int:
    """Pairs in the observable band, from `folddiag.band_count` -- the ONE definition, computed
    from the p values rather than from histogram bins whose linspace edges are 0.30000000000000004
    and 0.7000000000000001. Figure 1(a) reads the same field, so the figure's annotation and the
    paper's prose cannot disagree about the band."""
    return pooled["band_n"]


def _med(vals: Sequence[Optional[float]]) -> Optional[float]:
    ok = sorted(v for v in vals if v is not None)
    if not ok:
        return None
    mid = len(ok) // 2
    return ok[mid] if len(ok) % 2 else (ok[mid - 1] + ok[mid]) / 2


def write_delta(rows: List[List[Any]], t: Path) -> Path:
    return T.write_csv(t / "contamination_delta.csv",
                       ["quantity", "all_items", "clean_only", "delta", "unit"],
                       [[q, _f(a, u), _f(b, u), _f(_sub(b, a), u), u] for q, a, b, u in rows])


def _sub(a, b):
    return (a - b) if isinstance(a, (int, float)) and isinstance(b, (int, float)) else None


def _f(v, unit: str) -> str:
    if v is None:
        return ""
    return str(int(v)) if unit == "count" else T.fmt(float(v), 6)


def write_mirror(models: Sequence[str], leaves: List[Dict[str, Any]], cells, C, side,
                 t: Path, sub: str) -> Dict[str, Path]:
    """One reading of every table the exhibits read, under out/tables/<sub>/, with identical
    headers on both readings. `make_tables.py` then takes ONE directory argument and the choice of
    headline reading is a PATH, not a branch through the table code -- so the appendix's all-item
    exhibits and the main text's clean-only exhibits are produced by the same lines."""
    d = t / sub
    d.mkdir(parents=True, exist_ok=True)
    names = [l["leaf"] for l in leaves]
    out = {"model_summary": T.write_csv(
        d / "model_summary.csv",
        ["model", "cells_present", "cells_dropped", "leaves_zero_wobble", "aggregate_wobble",
         "total_measured_items", "total_flipped_items", "wilson_lo", "wilson_hi", "accuracy"],
        [_summary_row(m, names, cells, C["agg"][m]) for m in models])}
    out["categories"] = T.write_csv(
        d / "model_x_category_wilson.csv",
        ["model", "category", "n_leaves", "flipped_items", "measured_items", "rate", "wilson_lo",
         "wilson_hi", "estimable"],
        [[m, c, v["n_leaves"], v["flipped"], v["measured"], T.fmt(v["rate"], 6),
          T.fmt(v["lo"], 6), T.fmt(v["hi"], 6), int(v["estimable"])]
         for m in models for c, v in sorted(C["cat"][m].items())])
    out["transfer"] = T.write_csv(
        d / "transfer_summary.csv",
        ["k", "n_pairs", "median", "q1", "q3", "iqr", "chance", "median_lift", "k_eff_a",
         "k_eff_b", "n_truncated", "n_models"],
        [[k, C["transfer"][k]["n_defined"], T.fmt(C["transfer"][k]["median"], 6),
          T.fmt(C["transfer"][k]["q1"], 6), T.fmt(C["transfer"][k]["q3"], 6),
          T.fmt(C["transfer"][k]["iqr"], 6), T.fmt(C["transfer"][k]["chance"], 6),
          T.fmt(C["transfer"][k]["median_lift"], 6), T.fmt(C["transfer"][k]["k_eff_a"], 1),
          T.fmt(C["transfer"][k]["k_eff_b"], 1), C["transfer"][k]["n_truncated"],
          C["transfer"][k]["n_models"]] for k in (5, 10)])
    out.update(_write_diag(side, d))
    return out


def _summary_row(m: str, names: Sequence[str], cells, agg: float) -> List[Any]:
    flipped = sum(cells[m][n]["flipped"] for n in names)
    items = sum(cells[m][n]["n_items"] for n in names)
    maj = sum(cells[m][n]["n_majority"] for n in names)
    lo, hi = categories.wilson(flipped, items)
    return [m, sum(1 for n in names if not cells[m][n]["absent"]),
            sum(1 for n in names if cells[m][n]["dropped"]),
            sum(1 for n in names if (cells[m][n]["wobble"] or 0) == 0),
            T.fmt(agg, 6), items, flipped, T.fmt(lo, 6), T.fmt(hi, 6),
            T.fmt(maj / items if items else None, 6)]


def _write_diag(side: Dict[str, Any], d: Path) -> Dict[str, Path]:
    diag, rel, cons = side["diag"], side["rel"], side["cons"]
    p = diag["pooled_p"]
    return {
        "p_dist": T.write_csv(
            d / "item_p_distribution.csv", ["bin_lo", "bin_hi", "n_items", "share"],
            [[T.fmt(p["edges"][i], 2), T.fmt(p["edges"][i + 1], 2), h, T.fmt(h / p["n_items"], 6)]
             for i, h in enumerate(p["hist"])]),
        # The band count as its OWN artifact, so the figure annotates the number the prose quotes
        # instead of re-summing the histogram. Re-deriving it twice is how the panel came to
        # annotate a different count from its own caption; the fix is one source, not two careful
        # copies of the same arithmetic.
        # The always-correct and always-wrong rows are here for the same reason the band rows are:
        # the paper quotes all four shares, and each one has to come from a file rather than from
        # arithmetic done once in prose and never again. Without them the observability sentence
        # was carrying two figures that matched no artifact, and the numbers gate passed it because
        # those same decimals happen to occur elsewhere as unrelated quantities.
        "band": T.write_csv(
            d / "observable_band.csv", ["reading", "lo", "hi", "n_pairs", "n_total", "share"],
            [["closed", "0.3", "0.7", p["band_n"], p["n_items"],
              T.fmt(p["band_n"] / p["n_items"], 6)],
             ["half-open", "0.3", "0.7", p["band_n_halfopen"], p["n_items"],
              T.fmt(p["band_n_halfopen"] / p["n_items"], 6)],
             ["always correct", "1.0", "1.0", p["n_one"], p["n_items"], T.fmt(p["frac_one"], 6)],
             ["always wrong", "0.0", "0.0", p["n_zero"], p["n_items"],
              T.fmt(p["frac_zero"], 6)]]),
        "frontier": T.write_csv(
            d / "accuracy_decile_frontier.csv",
            ["accuracy_decile", "n_leaves", "max_observed_wobble", "max_structural_wobble",
             "mean_observed_wobble"],
            [[r["decile"], r["n_leaves"], T.fmt(r["max_observed"], 6),
              T.fmt(r["max_structural"], 6), T.fmt(r["mean_observed"], 6)]
             for r in diag["frontier"]]),
        "reliability": T.write_csv(
            d / "split_half_reliability.csv", ["model", "n_leaves", "r_half", "r_full", "note"],
            [[r["model"], r["n_leaves"], T.fmt(r["r_half"], 6), T.fmt(r["r_full"], 6), r["reason"]]
             for r in rel]),
        "conservative": T.write_csv(
            d / "conservative_summary.csv",
            ["floor", "median_point_ratio", "median_conservative_ratio", "n_models_above_2x",
             "gradient_slope_all", "gradient_r2_all", "gradient_slope_frontier",
             "gradient_slope_frontier_lo", "gradient_slope_frontier_hi", "gradient_r2_frontier",
             "gradient_intercept_frontier", "gradient_intercept_lo", "gradient_intercept_hi",
             "n_models_frontier"],
            [[f, T.fmt(cons[f]["median_point"], 4), T.fmt(cons[f]["median_cons"], 4),
              cons[f]["n_over_2x"], T.fmt(cons["gradient"][0]["slope"], 4),
              T.fmt(cons["gradient"][0]["r2"], 4), T.fmt(cons["gradient"][1]["slope"], 4),
              T.fmt(cons["gradient"][1]["lo"], 4), T.fmt(cons["gradient"][1]["hi"], 4),
              T.fmt(cons["gradient"][1]["r2"], 4), T.fmt(cons["gradient"][1]["intercept"], 4),
              T.fmt(cons["gradient"][1]["intercept_lo"], 4),
              T.fmt(cons["gradient"][1]["intercept_hi"], 4), cons["gradient"][1]["n"]]
             for f in (3, 5)])}
