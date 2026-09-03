"""
Location: paper-a/analysis/numbers_s2.py
Purpose: The stage-2 half of NUMBERS.md -- every figure the stage-2 report or the narration quotes,
         mapped to the file and the computation that produced it. Separate module so report.py
         stays inside the LOC budget and so the mapping is written next to nothing else.
Functions: rows()
Calls: none (pure over the stage-2 context)
Imports: typing, tables_out
"""

from typing import Any, Dict, List

import tables_out as T

TB = "out/tables/"


def _ceiling_rows(s2: Dict[str, Any]) -> List[List[str]]:
    rep = s2["repeated_split"]
    return [
        ["median split-half r_half", T.fmt(s2["median_r_half"], 4), TB + "split_half_reliability.csv",
         "median over 12 models of Spearman(half-A leaf vector, half-B leaf vector), runs split by "
         "run_idx % 2, scored by the benchmark's own engine/scorer.py"],
        ["median split-half r_full (Spearman-Brown)", T.fmt(s2["median_r_full"], 4),
         TB + "split_half_reliability.csv", "2r/(1+r) applied per model, then the median"],
        ["ceiling decision row", s2["ceiling_row"], "analysis/stage2.py",
         "cuts at 0.40 and 0.70 on median r_full, fixed in DESIGN-stage2.md"],
        ["disattenuated median rho", T.fmt(s2["corrected_median"], 4),
         TB + "disattenuated_pairs.csv",
         "median of rho_observed / sqrt(r_full_A * r_full_B), computed PER PAIR then summarised"],
        ["pairs whose correction exceeded 1.0", str(s2["n_over_one"]),
         TB + "disattenuated_pairs.csv", "count of non-empty note column"],
        ["observed as a share of the ceiling", f"{s2['pct_of_ceiling']:.1f}%", TB + "distributions.csv",
         "100 * observed median rho / median r_full"],
        ["repeated-split median r_full", T.fmt(rep["median_of_medians"], 4), "analysis/splithalf.py",
         f"{rep['n_splits']} random partitions of each cell's runs; median of the per-split medians"],
        ["repeated-split 95% spread", f"{T.fmt(rep['p02_5'], 4)} to {T.fmt(rep['p97_5'], 4)}",
         "analysis/splithalf.py", "2.5th and 97.5th percentiles of the per-split medians"],
    ]


def _transfer_rows(s2: Dict[str, Any], ks) -> List[List[str]]:
    out = []
    for k in ks:
        for label, key in (("frontier-only", "frontier"), ("all 12", "all")):
            s = s2["transfer"][k][key]
            out.append([f"transfer at k={k}, {label}", T.fmt(s["median"], 4), TB + "transfer.csv",
                        f"median over {s['n_defined']} ordered pairs of |A top-{k} within B "
                        f"top-{2 * k}| / |A top-{k}|, k truncated to non-zero leaves"])
            out.append([f"chance baseline at k={k}, {label}", T.fmt(s["chance"], 4),
                        TB + "transfer.csv",
                        "median per-pair effective |B top-2k| / active subset size"])
    return out


def _desc_rows(s2: Dict[str, Any]) -> List[List[str]]:
    f = s2["fit"]
    return [
        ["median worst-category-to-mean ratio", T.fmt(s2["ratio_median"], 4),
         TB + "worst_category_ratio.csv",
         "per model, worst estimable category rate / aggregate wobble; then the median"],
        ["Spearman(mean wobble, worst/mean ratio)", T.fmt(s2["ratio_vs_capability"], 4),
         TB + "worst_category_ratio.csv", "over 12 models -- SHARES A DENOMINATOR, see next row"],
        ["Spearman(mean wobble, worst-category wobble)", T.fmt(s2["worst_vs_capability"], 4),
         TB + "worst_category_ratio.csv",
         "the same question without the shared denominator, over 12 models"],
        ["predictor model R^2", T.fmt(f["r2"], 4), TB + "predictor_model.csv",
         f"OLS of per-leaf mean wobble on answer type + n_items + clause length, n={f['n']} leaves"],
        ["predictor model adjusted R^2", T.fmt(f["adj_r2"], 4), TB + "predictor_model.csv",
         "R^2 penalised for the parameter count"],
        ["adj R^2 gain from adding category", T.fmt(s2["nested_category"]["delta_adj"], 4),
         TB + "predictor_model.csv", "adj R^2(answer type + size + category) - adj R^2(answer "
         "type + size)"],
        ["adj R^2 gain from adding answer type", T.fmt(s2["nested_answer"]["delta_adj"], 4),
         TB + "predictor_model.csv", "adj R^2(size + category + answer type) - adj R^2(size + "
         "category)"],
    ]


def _robust_rows(s2: Dict[str, Any]) -> List[List[str]]:
    wa, nm, bs, ha = (s2["wobble_vs_accuracy"], s2["nightmare"], s2["bootstrap"],
                      s2["high_acc_leaves"])
    lomo = s2["lomo"]
    base = s2["observed_median"]
    worst = max(lomo, key=lambda r: abs(r["median"] - base))
    return [
        ["Spearman(leaf mean wobble, leaf mean accuracy)", T.fmt(wa["rho"], 4),
         TB + "leaf_wobble_vs_accuracy.csv",
         f"over n={wa['n']} leaves, each averaged across the models where it is defined"],
        ["high-accuracy AND high-wobble leaves", str(nm["n"]), TB + "leaf_wobble_vs_accuracy.csv",
         f"count with mean accuracy >= {nm['threshold_accuracy']} AND mean wobble >= "
         f"{nm['threshold_wobble']} (thresholds fixed in DESIGN-stage2.md)"],
        ["leaves with mean accuracy >= 0.90", str(ha["n"]), TB + "leaf_wobble_vs_accuracy.csv",
         "count; their maximum wobble is the next row"],
        ["max wobble among high-accuracy leaves", T.fmt(ha["max_wobble"], 4),
         TB + "leaf_wobble_vs_accuracy.csv", "shows where the pre-registered quadrant boundary sits"],
        ["bootstrap median rho", T.fmt(bs["median"], 4), "analysis/robustness.py",
         f"{bs['n_boot']} leaf-resampled replicates, fixed seed"],
        ["bootstrap 95% CI", f"{T.fmt(bs['lo'], 4)} to {T.fmt(bs['hi'], 4)}",
         "analysis/robustness.py", "2.5th and 97.5th percentiles of the replicate medians"],
        ["largest leave-one-model-out shift", f"{worst['median'] - base:+.4f}",
         TB + "leave_one_out.csv", f"dropping `{worst['dropped']}`; 12 recomputations"],
        ["Spearman(item-weighted, leaf-equal ordering)", T.fmt(s2["weighting_rho"], 4),
         TB + "weighting_sensitivity.csv", "over 12 models -- does the weighting choice reorder "
         "capability?"],
    ]


def rows(s2: Dict[str, Any], ks, ann: Dict[str, Any]) -> List[List[str]]:
    out = _ceiling_rows(s2) + _transfer_rows(s2, ks) + _desc_rows(s2) + _robust_rows(s2)
    out.append(["annotation sample size", f"{ann['n_leaves']} leaves / {ann['n_items']} items",
                "out/annotation/sample.csv",
                "stratified 20% of leaves by (category x answer type), fixed seed"])
    return out
