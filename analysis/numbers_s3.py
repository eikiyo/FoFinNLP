"""
Location: paper-a/analysis/numbers_s3.py
Purpose: The stage-3 half of NUMBERS.md -- every figure the stage-3 report or the narration quotes,
         mapped to the file and the computation that produced it. Separate module so report.py
         stays inside the LOC budget and so the mapping is written next to nothing else.
Functions: rows()
Calls: none (pure over the stage-3 context)
Imports: typing, tables_out
"""

from typing import Any, Dict, List

import tables_out as T

TB = "out/tables/"


def _ratio_rows(s3: Dict[str, Any]) -> List[List[str]]:
    a, b = s3["survivors"][3], s3["survivors"][5]
    return [
        ["median worst-to-mean ratio, point estimates", T.fmt(a["median_point"], 4),
         TB + "conservative_ratio_min3.csv",
         "median over 12 models of (worst estimable category rate / aggregate wobble)"],
        ["median worst-to-mean ratio, CONSERVATIVE", T.fmt(a["median_cons"], 4),
         TB + "conservative_ratio_min3.csv",
         "median of (largest Wilson lower bound over categories / Wilson upper bound of the mean); "
         "selection-robust, so not exposed to the winner's curse"],
        ["models above 2x, point estimates", f"{a['n_over_bar_point']}/12",
         TB + "conservative_ratio_min3.csv", "count of models whose point ratio exceeds 2"],
        ["models above 2x, conservative", f"{a['n_over_bar']}/12",
         TB + "conservative_ratio_min3.csv", "count of models whose conservative ratio exceeds 2"],
        ["median conservative ratio, 5-leaf floor", T.fmt(b["median_cons"], 4),
         TB + "conservative_ratio_min5.csv",
         "same computation with categories of fewer than 5 leaves excluded (removes exit_waterfall)"],
        ["models above 2x, conservative, 5-leaf floor", f"{b['n_over_bar']}/12",
         TB + "conservative_ratio_min5.csv", "count at the stricter estimability floor"],
    ]


def _regression_rows(s3: Dict[str, Any]) -> List[List[str]]:
    out = []
    for k in s3["regressions"]:
        if "error" in k:
            continue
        out.append([f"worst-on-mean slope ({k['y']}, {k['label']})", T.fmt(k["slope"], 4),
                    TB + "worst_on_mean_regression.csv",
                    f"OLS of worst-category wobble on mean wobble over n={k['n']} models; "
                    f"95% CI {T.fmt(k['lo'], 4)} to {T.fmt(k['hi'], 4)}, R2 {T.fmt(k['r2'], 4)}"])
    a = s3["worst_on_mean"]
    out.append(["worst-on-mean intercept (all 12 models)", T.fmt(a["intercept"], 4),
                TB + "worst_on_mean_regression.csv",
                "the term that makes the RATIO grow as mean wobble goes to zero; 95% CI "
                f"{T.fmt(a['intercept_lo'], 4)} to {T.fmt(a['intercept_hi'], 4)}"])
    return out


def _fold_rows(s3: Dict[str, Any]) -> List[List[str]]:
    sv, ft = s3["surviving"], s3["fold_test"]
    zero = next(r for r in s3["p_buckets"] if r["bucket"].startswith("p=0"))
    return [
        ["rho(leaf wobble, leaf accuracy), observed", T.fmt(sv["rho_observed"], 4),
         TB + "fold_decomposition.csv",
         "Spearman over 60 leaves; reproduces the stage-2 value exactly"],
        ["rho(residual, accuracy), calibrated model", T.fmt(sv["rho_residual_cal"], 4),
         TB + "fold_decomposition.csv",
         "residual after subtracting the per-item-p prediction whose always-wrong flip rate is "
         "estimated LEAVE-ONE-LEAF-OUT; the primary answer to 'is it mechanical'"],
        ["rho(residual, accuracy), lower-bound model", T.fmt(sv["rho_residual_min"], 4),
         TB + "fold_decomposition.csv",
         "residual after subtracting 1 - p^n - (1-p)^n; parameter-free, no definitional component"],
        ["rho(residual, accuracy), upper-bound model", T.fmt(sv["rho_residual_max"], 4),
         TB + "fold_decomposition.csv", "residual after subtracting 1 - p^n"],
        ["quadratic term, wobble ~ accuracy + accuracy^2", T.fmt(ft["quad_beta"], 4),
         TB + "fold_decomposition.csv",
         f"positive, so NOT folded; 95% CI {T.fmt(ft['quad_lo'], 4)} to {T.fmt(ft['quad_hi'], 4)}; "
         f"accuracy range covered {T.fmt(ft['acc_min'], 3)}-{T.fmt(ft['acc_max'], 3)}"],
        ["flip rate among always-wrong items", T.fmt(zero["flip_rate"], 4),
         TB + "p_bucket_flip_rates.csv",
         f"{zero['n_flipped']} of {zero['n_items']} items at p=0 flip; the lower-bound model "
         "predicts 0 and the upper-bound model predicts 1, so this locates reality between them"],
    ]


def _zone_rows(s3: Dict[str, Any]) -> List[List[str]]:
    p, z = s3["pooled_p"], s3["zone"]
    return [
        ["item-measurements pooled", f"{p['n_items']}", TB + "item_p_distribution.csv",
         "12 models x 60 leaves, items with at least one valid run across every scorable field"],
        ["share of items at exactly p = 1", T.fmt(p["frac_one"], 4),
         TB + "item_p_distribution.csv", "answered correctly on every run"],
        ["share of items at exactly p = 0", T.fmt(p["frac_zero"], 4),
         TB + "item_p_distribution.csv", "answered incorrectly on every run"],
        ["share of items with 0.3 <= p <= 0.7", T.fmt(p["frac_mid"], 4),
         TB + "item_p_distribution.csv",
         "the only band where an item can flip while its majority answer stays correct"],
        ["leaves at accuracy >= 0.9", str(z["n_high_accuracy_leaves"]),
         TB + "accuracy_decile_frontier.csv", "count of leaves in the top accuracy region"],
        ["max OBSERVED wobble at accuracy >= 0.9", T.fmt(z["max_observed"], 4),
         TB + "accuracy_decile_frontier.csv", "the empirical frontier in that region"],
        ["max STRUCTURALLY REACHABLE wobble at accuracy >= 0.9", T.fmt(z["max_structural"], 4),
         TB + "accuracy_decile_frontier.csv",
         f"the most those leaves' item structure could produce, against a threshold of "
         f"{z['threshold_wobble']} -- so the region was unreachable before any model was run"],
    ]


def rows(s3: Dict[str, Any]) -> List[List[str]]:
    return (_ratio_rows(s3) + _regression_rows(s3) + _fold_rows(s3) + _zone_rows(s3)
            + [["items in the blind annotation pack", str(s3["blind"]["n_rows"]),
                "out/annotation/blind_pack.csv",
                f"{s3['blind']['n_leaves']} leaves, labels withheld, order randomised under seed "
                f"{s3['blind']['seed']}"],
               ["annotation agreement", s3["agreement"].get("status", "NOT RUN"),
                "out/annotation/agreement_result.json",
                "the sitting has not happened; the scorer refuses to report a number on an "
                "unfilled sheet rather than scoring empty against empty"]])
