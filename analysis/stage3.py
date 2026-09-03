"""
Location: paper-a/analysis/stage3.py
Purpose: Compute every stage-3 quantity in the brief's order -- 1a conservative ratios, 1b the fold
         decomposition, 1c the empty zone, 1d worst-on-mean -- and hand one context dict to the
         report writer. Orchestration only; every computation lives in its own module.
Functions: compute(), _one_a(), _one_bc(), _one_gap1(), _zone(), write_tables() + one _t_*
           writer per table
Calls: conservative, fold, folddiag, flagged_profile, oracle_audit, robustness, tables_out
Imports: pathlib, typing, config, conservative, flagged_profile, fold, folddiag, oracle_audit,
         robustness, tables_out
"""

from pathlib import Path
from typing import Any, Dict, List

import config
import conservative
import flagged_profile
import fold
import folddiag
import oracle_audit
import robustness
import block0d
import stratified
import tables_out as T

STRICT_FLOORS = (3, 5)      # 1a reports the default floor and the stricter sensitivity


def compute(s2: Dict[str, Any]) -> Dict[str, Any]:
    """`s2` is the stage-2 context: models, leaves, cells, names, cat_cells, accuracy, agg_wobble."""
    ctx: Dict[str, Any] = {"models": s2["models"], "names": s2["names"], "leaves": s2["leaves"],
                           "cons_selftest": conservative.selftest(),
                           "fold_selftest": fold.selftest(),
                           "folddiag_selftest": folddiag.selftest(),
                           "numparse_selftest": flagged_profile.numparse.selftest(),
                           "profile_selftest": flagged_profile.selftest(),
                           "stratified_selftest": stratified.selftest()}
    _one_a(ctx, s2)
    _one_bc(ctx, s2)
    _one_gap1(ctx, s2)
    return ctx


def _one_a(ctx: Dict[str, Any], s2: Dict[str, Any]) -> None:
    """1a (conservative ratios) and 1d (the same claim as a regression, no shared denominator)."""
    models, names = s2["models"], s2["names"]
    totals = conservative.model_totals(models, names, s2["cells"])
    ctx["totals"] = totals
    ctx["cons"] = {f: conservative.conservative_rows(models, s2["cat_cells"], totals, f)
                   for f in STRICT_FLOORS}
    ctx["survivors"] = {f: conservative.survivors(ctx["cons"][f]) for f in STRICT_FLOORS}
    front = s2["frontier"]
    ctx["regressions"] = [
        conservative.worst_on_mean(ctx["cons"][3], "point_rate", None, "all 12 models"),
        conservative.worst_on_mean(ctx["cons"][3], "point_rate", front, "frontier only"),
        conservative.worst_on_mean(ctx["cons"][3], "robust_lo", None, "all 12 models"),
        conservative.worst_on_mean(ctx["cons"][3], "robust_lo", front, "frontier only")]
    ctx["worst_on_mean"] = ctx["regressions"][0]
    ctx["worst_on_mean_frontier"] = ctx["regressions"][1]
    ctx["best_absolute"] = conservative.best_models_absolute(ctx["cons"][3], 3)


def _one_bc(ctx: Dict[str, Any], s2: Dict[str, Any]) -> None:
    """1b (the fold decomposition) and 1c (why the empty zone is empty)."""
    models, names = s2["models"], s2["names"]
    col = fold.collect(models, s2["leaves"])
    ctx["fold_roundtrip"] = fold.roundtrip_check(models, names, col["per_cell"], s2["cells"])
    rows = fold.leaf_rows(models, col["per_cell"], s2["leaf_means"])
    ctx["fold_rows"] = rows
    ctx["pooled_p"] = folddiag.pooled_p(models, names, col["per_cell"])
    ctx["p_buckets"] = folddiag.p_bucket_flips(models, names, col["per_cell"])
    ctx["frontier"] = folddiag.decile_frontier(rows)
    ctx["fold_test"] = folddiag.fold_test(rows, "observed")
    ctx["fold_test_structural"] = folddiag.fold_test(rows, "structural")
    ctx["surviving"] = folddiag.surviving_fraction(rows)
    ctx["zone"] = _zone(rows, s2)
    ctx["per_cell"] = col["per_cell"]


def _one_gap1(ctx: Dict[str, Any], s2: Dict[str, Any]) -> None:
    """GAP 1. The repair null removes windowing as the established mechanism, so the flagged
    population has to be characterised rather than explained: accuracy answers the competing
    "they are simply harder" reading, composition says where the flags concentrate, and whether
    the window STATES the answer is a second candidate property, computed without reference to
    the validating quote and therefore independent of the flag itself."""
    audit = oracle_audit.audit_all()
    ctx["profile_rows"] = flagged_profile.item_rows(
        s2["leaves"], audit, ctx["per_cell"], s2["models"], s2["answer_types"])
    # Camera-ready T4-T7: the same items re-measured over the frontier set alone, then the
    # stratified frame over both configuration sets. Re-measuring through item_rows rather than
    # subtracting the 1B rows keeps one code path for every pairs/flips count in the section.
    rows_frontier = flagged_profile.item_rows(
        s2["leaves"], audit, ctx["per_cell"], list(s2["frontier"]), s2["answer_types"])
    # Camera-ready fix 1.1: each flagged row carries its failure group, from the SAME
    # derivation bucket_wobble.csv reports, so the stratified frame and the bucket table
    # cannot disagree about which group an item is in.
    fail = block0d.failure_labels(audit, block0d.buckets(audit, oracle_audit.corpus_index()))
    for r in (*ctx["profile_rows"], *rows_frontier):
        r["failure"] = fail.get((r["leaf"], r["item"]), "")
    ctx["stratified"] = stratified.stratified_contrast(
        [("all", ctx["profile_rows"]), ("frontier", rows_frontier)])


def _zone(rows: List[Dict[str, Any]], s2: Dict[str, Any]) -> Dict[str, Any]:
    """The empty high-accuracy/high-wobble zone, with the structural question attached: at accuracy
    >= 0.9, what is the most wobble the item pool could even produce? If the structural maximum
    sits below the threshold, the zone is empty BY CONSTRUCTION and the paper reports a limitation
    of the item pool, not a finding about models. Those are opposite sentences."""
    hi = [r for r in rows if (r["accuracy"] or 0) >= robustness.HIGH_ACC]
    obs = [r["observed"] for r in hi if r["observed"] is not None]
    stru = [r["structural"] for r in hi if r["structural"] is not None]
    reach = max(stru, default=0.0)
    return {"threshold_accuracy": robustness.HIGH_ACC, "threshold_wobble": robustness.HIGH_WOBBLE,
            "n_high_accuracy_leaves": len(hi), "max_observed": max(obs, default=None),
            "max_structural": reach, "reachable": bool(reach >= robustness.HIGH_WOBBLE),
            "n_in_zone": s2["nightmare"]["n"]}


CONS_HEADER = ["model", "mean_wobble", "mean_wilson_lo", "mean_wilson_hi", "point_worst_category",
               "point_worst_rate", "point_worst_lo", "point_worst_hi", "second_worst_category",
               "second_worst_rate", "robust_worst_category", "robust_worst_lo", "point_ratio",
               "conservative_ratio", "conservative_ratio_point_selected",
               "conservative_ratio_excl_worst", "n_estimable_categories"]


def _cons_row(r: Dict[str, Any]) -> List[Any]:
    return [r["model"], T.fmt(r["mean"], 6), T.fmt(r["mean_lo"], 6), T.fmt(r["mean_hi"], 6),
            r["point_cat"] or "", T.fmt(r["point_rate"], 6), T.fmt(r["point_lo"], 6),
            T.fmt(r["point_hi"], 6), r["second_cat"] or "", T.fmt(r["second_rate"], 6),
            r["robust_cat"] or "", T.fmt(r["robust_lo"], 6), T.fmt(r["point_ratio"], 4),
            T.fmt(r["cons_ratio"], 4), T.fmt(r["cons_ratio_point"], 4),
            T.fmt(r["cons_ratio_excl"], 4), r["n_estimable"]]


def _t_fold(ctx: Dict[str, Any], t: Path) -> None:
    T.write_csv(t / "fold_decomposition.csv",
                ["leaf", "n_models", "mean_accuracy", "observed_wobble", "structural_lo",
                 "structural_hi", "residual_vs_lo", "residual_vs_hi"],
                [[r["leaf"], r["n_models"], T.fmt(r["accuracy"], 6), T.fmt(r["observed"], 6),
                  T.fmt(r["structural"], 6), T.fmt(r["structural_max"], 6),
                  T.fmt(r["residual"], 6), T.fmt(r["residual_max"], 6)]
                 for r in ctx["fold_rows"]])


def _t_pdist(ctx: Dict[str, Any], t: Path) -> None:
    p = ctx["pooled_p"]
    T.write_csv(t / "item_p_distribution.csv", ["bin_lo", "bin_hi", "n_items", "share"],
                [[T.fmt(p["edges"][i], 2), T.fmt(p["edges"][i + 1], 2), h,
                  T.fmt(h / p["n_items"], 6)] for i, h in enumerate(p["hist"])])


def _t_frontier(ctx: Dict[str, Any], t: Path) -> None:
    T.write_csv(t / "accuracy_decile_frontier.csv",
                ["accuracy_decile", "n_leaves", "max_observed_wobble", "max_structural_wobble",
                 "mean_observed_wobble"],
                [[r["decile"], r["n_leaves"], T.fmt(r["max_observed"], 6),
                  T.fmt(r["max_structural"], 6), T.fmt(r["mean_observed"], 6)]
                 for r in ctx["frontier"]])


def _t_pbuckets(ctx: Dict[str, Any], t: Path) -> None:
    T.write_csv(t / "p_bucket_flip_rates.csv",
                ["bucket", "n_items", "n_flipped", "observed_flip_rate",
                 "predicted_lower_bound_model", "predicted_upper_bound_model"],
                [[r["bucket"], r["n_items"], r["n_flipped"], T.fmt(r["flip_rate"], 6),
                  T.fmt(r["predicted_lo"], 4), T.fmt(r["predicted_hi"], 4)]
                 for r in ctx["p_buckets"]])


def _t_regression(ctx: Dict[str, Any], t: Path) -> None:
    T.write_csv(t / "worst_on_mean_regression.csv",
                ["outcome", "model_set", "n_models", "slope", "slope_se", "slope_ci_lo",
                 "slope_ci_hi", "intercept", "intercept_ci_lo", "intercept_ci_hi", "r2",
                 "slope_below_one"],
                [[k["y"], k["label"], k["n"], T.fmt(k["slope"], 6), T.fmt(k["se"], 6),
                  T.fmt(k["lo"], 6), T.fmt(k["hi"], 6), T.fmt(k["intercept"], 6),
                  T.fmt(k["intercept_lo"], 6), T.fmt(k["intercept_hi"], 6), T.fmt(k["r2"], 6),
                  int(k["slope_below_one"])] for k in ctx["regressions"] if "error" not in k])


def write_tables(ctx: Dict[str, Any], t: Path) -> None:
    for floor in STRICT_FLOORS:
        T.write_csv(t / f"conservative_ratio_min{floor}.csv", CONS_HEADER,
                    [_cons_row(r) for r in ctx["cons"][floor]])
    for writer in (_t_fold, _t_pdist, _t_frontier, _t_pbuckets, _t_regression):
        writer(ctx, t)
    ctx["profile"] = flagged_profile.write_all(ctx["profile_rows"], ctx["leaves"], t,
                                               config.out_paths()["out"])
    stratified.write_stratified(ctx["stratified"], t)
