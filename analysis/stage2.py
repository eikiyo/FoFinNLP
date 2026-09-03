"""
Location: paper-a/analysis/stage2.py
Purpose: Compute every stage-2 quantity in the brief's order -- step 1 (the ceiling) FIRST, because
         it recalibrates the reading of everything after it -- and hand a single context dict to
         the report writer. Orchestration only; every computation lives in its own module.
Functions: compute(), _step1(), _step2(), _step3(), _step4(), write_tables()
Calls: splithalf, transfer, categories, predictors, robustness, annotation, answer_space
Imports: csv, statistics, typing, pathlib, config, tables_out + the stage-2 modules
"""

import csv
import statistics
from pathlib import Path
from typing import Any, Dict, List

import analyses as an
import annotation
import answer_space
import categories
import config
import matrix
import predictors
import robustness
import splithalf
import stats_core as sc
import tables_out as T
import transfer

N_BOOTSTRAP = 2000
BOOT_SEED = 20260729
N_RANDOM_SPLITS = 40
TRANSFER_KS = (5, 10, 20)


def _step1(ctx: Dict[str, Any]) -> None:
    """The measurement ceiling. Runs first; every later reading is relative to it."""
    models, leaves, cells, active = ctx["models"], ctx["leaves"], ctx["cells"], ctx["active"]
    sp = splithalf.split_cells(models, leaves)
    ctx["roundtrip"] = splithalf.roundtrip_check(models, ctx["names"], sp["full"], cells)
    ctx["halves"] = sp
    rows = splithalf.reliability_rows(models, active, sp, cells)
    ctx["reliability"] = rows
    rf = {r["model"]: r["r_full"] for r in rows}
    defined = [r["r_full"] for r in rows if r["r_full"] is not None]
    ctx["median_r_half"] = statistics.median([r["r_half"] for r in rows
                                              if r["r_half"] is not None])
    ctx["median_r_full"] = statistics.median(defined)
    ctx["n_reliability_defined"] = len(defined)
    ctx["reliability_null"] = splithalf.reliability_null(sp, models, active, 1000,
                                                         config.PERM_SEED)
    act_leaves = [l for l in leaves if l["leaf"] in set(active)]
    ctx["repeated_split"] = splithalf.repeated_split_reliability(
        models, act_leaves, [l["leaf"] for l in act_leaves], N_RANDOM_SPLITS, BOOT_SEED)
    ctx["nonzero_reliability"] = _nonzero_reliability(models, active, cells, sp)
    pairs = sc.all_pairs(models, {m: [cells[m][n]["wobble"] for n in active] for m in models})
    corrected = []
    for p in pairs:
        v, note = splithalf.disattenuate(p["rho"], rf[p["model_a"]], rf[p["model_b"]])
        p["rho_corrected"], p["correction_note"] = v, note
        if v is not None:
            corrected.append(v)
    ctx["pairs_corrected"] = pairs
    ctx["observed_median"] = statistics.median([p["rho"] for p in pairs
                                                if p["rho"] is not None])
    ctx["corrected_median"] = statistics.median(corrected) if corrected else None
    ctx["n_corrected"] = len(corrected)
    ctx["n_over_one"] = sum(1 for p in pairs if p["correction_note"])
    ctx["pct_of_ceiling"] = 100 * ctx["observed_median"] / ctx["median_r_full"]
    ctx["ceiling_row"] = ("high" if ctx["median_r_full"] >= 0.70
                          else "middling" if ctx["median_r_full"] >= 0.40 else "low")


def _nonzero_reliability(models, active, cells, sp) -> List[Dict[str, Any]]:
    """SENSITIVITY (declared): reliability restricted to each model's OWN non-zero leaves. The
    headline reliability is partly the instrument re-finding the same zeros; this asks the harder
    question -- can it RANK the leaves that actually move? It can only weaken the ceiling claim,
    which is why it is reported."""
    out = []
    for m in models:
        idx = [n for n in active if (cells[m][n]["wobble"] or 0) > 0]
        if len(idx) < 5:
            out.append({"model": m, "n": len(idx), "r_half": None, "r_full": None,
                        "note": "fewer than 5 non-zero leaves - not estimable"})
            continue
        st = sc.pair_stats([sp["A"][m][n] for n in idx], [sp["B"][m][n] for n in idx])
        out.append({"model": m, "n": len(idx), "r_half": st["rho"],
                    "r_full": splithalf.spearman_brown(st["rho"]), "note": ""})
    return out


def _step2(ctx: Dict[str, Any]) -> None:
    rows = transfer.transfer_rows(ctx["models"], ctx["active"], ctx["cells"], TRANSFER_KS)
    ctx["transfer_rows"] = rows
    ctx["transfer"] = {
        k: {"frontier": transfer.summarise_transfer(rows, k, ctx["frontier"]),
            "all": transfer.summarise_transfer(rows, k, None)} for k in TRANSFER_KS}


def _step3(ctx: Dict[str, Any]) -> None:
    models, leaves, cells = ctx["models"], ctx["leaves"], ctx["cells"]
    ctx["cat_cells"] = categories.category_cells(models, leaves, cells)
    ctx["cat_selftest"] = categories.selftest()
    ctx["ratios"] = categories.model_ratios(models, ctx["cat_cells"], ctx["agg_wobble"])
    ok = [r for r in ctx["ratios"] if r["ratio"] is not None]
    ctx["ratio_median"] = statistics.median([r["ratio"] for r in ok])
    ctx["ratio_vs_capability"] = sc.pair_stats([r["mean"] for r in ok],
                                               [r["ratio"] for r in ok])["rho"]
    # Same question without the shared denominator: does the WORST category itself track
    # capability? If not, the ratio relationship is largely mechanical and must be said so.
    ctx["worst_vs_capability"] = sc.pair_stats([r["mean"] for r in ok],
                                               [r["worst"] for r in ok])["rho"]
    ctx["indistinguishable"] = {m: categories.indistinguishable_pairs(ctx["cat_cells"], m)
                                for m in models}
    feats = predictors.leaf_features(leaves, ctx["answer_types"])
    mw = {r["leaf"]: r["mean_wobble"] for r in ctx["leaf_means"]}
    base = ["is_numeric", "is_binary", "is_multi", "n_items", "clause_chars"]
    ctx["fit"] = predictors.fit_report(feats, mw, base)
    cats = predictors.category_dummies(feats)
    ctx["nested_category"] = predictors.nested_comparison(feats, mw, base, cats)
    ctx["nested_answer"] = predictors.nested_comparison(
        feats, mw, ["n_items", "clause_chars"] + cats, ["is_numeric", "is_binary", "is_multi"])


def _step4(ctx: Dict[str, Any]) -> None:
    models, names, cells = ctx["models"], ctx["names"], ctx["cells"]
    ctx["wobble_vs_accuracy"] = robustness.wobble_vs_accuracy(ctx["leaf_means"])
    ctx["nightmare"] = robustness.nightmare_leaves(ctx["leaf_means"])
    hi = [r for r in ctx["leaf_means"] if (r["mean_accuracy"] or 0) >= robustness.HIGH_ACC]
    ctx["high_acc_leaves"] = {
        "n": len(hi),
        "max_wobble": max((r["mean_wobble"] for r in hi), default=None),
        "top": sorted(hi, key=lambda r: -(r["mean_wobble"] or 0))[:5]}
    ctx["bootstrap"] = robustness.bootstrap_median(models, ctx["active"], cells,
                                                   N_BOOTSTRAP, BOOT_SEED)
    ctx["lomo"] = robustness.leave_one_out(models, ctx["active"], cells)
    ctx["weighting"] = robustness.weighting_sensitivity(models, names, cells)
    ctx["weighting_rho"] = robustness.rank_agreement(ctx["weighting"], "item_weighted",
                                                     "leaf_equal")


def compute(base: Dict[str, Any]) -> Dict[str, Any]:
    """Everything stage 2 needs, in the brief's order. `base` is the stage-1 context."""
    ctx = {k: base[k] for k in ("models", "leaves", "cells", "names", "active", "agg_wobble")}
    ctx["answer_types"] = base["answer_type"]
    ctx["frontier"] = base["split"]["frontier"]
    ctx["accuracy"] = matrix.load_accuracy(ctx["models"], ctx["leaves"])
    ctx["leaf_means"] = robustness.leaf_means(ctx["models"], ctx["names"], ctx["cells"],
                                              ctx["accuracy"])
    _step1(ctx)
    _step2(ctx)
    _step3(ctx)
    _step4(ctx)
    return ctx


_w = T.write_csv          # shared writer, extracted to tables_out when stage 3 needed it too


def write_tables(ctx: Dict[str, Any], t: Path) -> None:
    _w(t / "split_half_reliability.csv",
       ["model", "n_leaves", "wobble_half_A", "wobble_half_B", "wobble_full", "r_half", "r_full",
        "tie_A", "tie_B", "zero_A", "zero_B", "undefined_reason"],
       [[r["model"], r["n_leaves"], T.fmt(r["wobble_A"], 6), T.fmt(r["wobble_B"], 6),
         T.fmt(r["wobble_full"], 6), T.fmt(r["r_half"], 6), T.fmt(r["r_full"], 6),
         T.fmt(r["tie_A"], 4), T.fmt(r["tie_B"], 4), T.fmt(r["zero_A"], 4),
         T.fmt(r["zero_B"], 4), r["reason"]] for r in ctx["reliability"]])
    _w(t / "disattenuated_pairs.csv",
       ["model_a", "model_b", "n_leaves", "rho_observed", "rho_corrected", "note"],
       [[p["model_a"], p["model_b"], p["n"], T.fmt(p["rho"], 6),
         T.fmt(p["rho_corrected"], 6), p["correction_note"]] for p in ctx["pairs_corrected"]])
    _w(t / "transfer.csv",
       ["k", "from", "to", "k_effective_a", "k_effective_b", "hits", "rate", "chance", "lift",
        "truncated_a", "truncated_b"],
       [[r["k"], r["from"], r["to"], r.get("k_effective_a", ""), r.get("k_effective_b", ""),
         r.get("hits", ""), T.fmt(r.get("rate"), 6), T.fmt(r.get("chance"), 6),
         T.fmt(r.get("lift"), 6), int(bool(r.get("truncated_a"))),
         int(bool(r.get("truncated_b")))] for r in ctx["transfer_rows"]])
    cats = sorted({l["family"] for l in ctx["leaves"]})
    _w(t / "model_x_category_wilson.csv",
       ["model", "category", "n_leaves", "flipped_items", "measured_items", "rate",
        "wilson_lo", "wilson_hi", "estimable"],
       [[m, c, v["n_leaves"], v["flipped"], v["measured"], T.fmt(v["rate"], 6),
         T.fmt(v["lo"], 6), T.fmt(v["hi"], 6), int(v["estimable"])]
        for m in ctx["models"] for c, v in ((c, ctx["cat_cells"][m][c]) for c in cats)])
    _w(t / "worst_category_ratio.csv",
       ["model", "mean_wobble", "worst_category", "worst_wobble", "worst_lo", "worst_hi",
        "ratio", "n_estimable_categories"],
       [[r["model"], T.fmt(r["mean"], 6), r["worst_cat"] or "", T.fmt(r["worst"], 6),
         T.fmt(r.get("worst_lo"), 6), T.fmt(r.get("worst_hi"), 6), T.fmt(r["ratio"], 4),
         r["n_estimable"]] for r in ctx["ratios"]])
    _w(t / "predictor_model.csv", ["term", "beta", "se", "ci_lo", "ci_hi", "crosses_zero"],
       [[c["name"], T.fmt(c["beta"], 8), T.fmt(c["se"], 8), T.fmt(c["lo"], 8),
         T.fmt(c["hi"], 8), int(c["crosses_zero"])] for c in ctx["fit"]["coefs"]])
    _w(t / "leaf_wobble_vs_accuracy.csv",
       ["leaf", "mean_wobble", "n_models_wobble", "mean_accuracy", "n_models_accuracy"],
       [[r["leaf"], T.fmt(r["mean_wobble"], 6), r["n_models_wobble"],
         T.fmt(r["mean_accuracy"], 6), r["n_models_accuracy"]] for r in ctx["leaf_means"]])
    _w(t / "leave_one_out.csv",
       ["dropped_model", "n_models", "n_pairs", "n_defined", "median_rho", "iqr"],
       [[r["dropped"], r["n_models"], r["n_pairs"], r["n_defined"], T.fmt(r["median"], 6),
         T.fmt(r["iqr"], 6)] for r in ctx["lomo"]])
    _w(t / "weighting_sensitivity.csv",
       ["model", "item_weighted", "leaf_equal", "n_leaves", "n_items"],
       [[r["model"], T.fmt(r["item_weighted"], 6), T.fmt(r["leaf_equal"], 6), r["n_leaves"],
         r["n_items"]] for r in ctx["weighting"]])


def write_annotation(ctx: Dict[str, Any], out: Path) -> Dict[str, Any]:
    d = out / "annotation"
    d.mkdir(parents=True, exist_ok=True)
    sample = annotation.stratified_sample(ctx["leaves"], ctx["answer_types"])
    info = annotation.write_sample(sample, ctx["answer_types"], d, len(ctx["leaves"]))
    annotation.write_sheet(sample, d)
    annotation.write_protocol(info, d, ctx["answer_types"])
    return info
