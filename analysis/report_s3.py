"""
Location: paper-a/analysis/report_s3.py
Purpose: STAGE3_REPORT.md sections for step 1a (conservative ratios) and step 1d (worst-on-mean).
         Every section opens with what was computed and closes with what it DECIDES.
Functions: header(), step_1a(), step_1d()
Calls: none (pure over the stage-3 context)
Imports: typing, config, tables_out
"""

from typing import Any, Dict, List

import config
import tables_out as T


def header(ctx: Dict[str, Any]) -> List[str]:
    return [
        "# STAGE3_REPORT.md - Paper A stage 3",
        "",
        "> STATUS: DONE - steps 1a-1d, 2 (pre-registration only), 3, 4 - run 2026-07-29",
        "",
        f"Arm: **{config.ARM_HUMAN}**. No number here derives from the 0.1 arm or any cross-arm "
        "comparison. Regenerate everything with `python3 analysis/run_all.py`.",
        "",
        "**Step 0 (the novelty gate) ran first and cleared.** Neither trigger condition fired; the "
        "full audit, with 27 verified records, is `out/novelty_audit.md`. Read it before this file "
        "- it changes what the numbers below are allowed to be used for.",
        "",
        "**Controls that gate this run** (it aborts rather than produce partial output if any "
        "fail):",
        "",
        f"- `{ctx['cons_selftest']}`",
        f"- `{ctx['fold_selftest']}`",
        f"- `{ctx['folddiag_selftest']}`",
        f"- `{ctx['fold_roundtrip']}`",
        "",
        "That last one is the load-bearing control for everything in step 1b/1c: the per-item "
        "reconstruction is only trustworthy because it reproduces all 720 published wobble cells "
        "exactly. It failed on its first run (two cells), which is how a real defect was found - "
        "the benchmark keys measurability on the MINIMUM valid-run count across every scorable "
        "field, so an item whose target field has plenty of runs is still excluded when a sibling "
        "field recorded none. Using the target field alone had inflated two cells' wobble.",
        "",
        "---",
        "",
    ]


def _verdict_1a(ctx: Dict[str, Any]) -> List[str]:
    s3, s5 = ctx["survivors"][3], ctx["survivors"][5]
    return [
        "**What this decides.** The spine does not survive in its current form.",
        "",
        f"At the estimability floor the benchmark already uses (3 leaves), the median "
        f"worst-to-mean ratio falls from **{T.fmt(s3['median_point'], 2)}x** on point estimates to "
        f"**{T.fmt(s3['median_cons'], 2)}x** at the bounds, and the number of models clearing 2x "
        f"falls from **{s3['n_over_bar_point']}/12** to **{s3['n_over_bar']}/12**.",
        "",
        f"At a 5-leaf floor it collapses completely: median **{T.fmt(s5['median_cons'], 2)}x** - "
        f"below 1 - and **{s5['n_over_bar']}/12** models clear 2x. The reason is not subtle. "
        "`exit_waterfall` has 3 leaves and is the worst category for most models; raising the "
        "floor removes it, and with it the entire effect. The paper's headline currently rests on "
        "a single 3-leaf category.",
        "",
        "So the sentence *\"a model's headline wobble understates its worst clause type by a "
        "median of 4.96x\"* cannot be written. What the data supports is weaker and must be stated "
        f"at the bound: for {s3['n_over_bar']} of 12 models, the worst estimable clause type is at "
        "least twice the headline even after both numbers are read as pessimistically as the "
        "intervals permit. For the rest, the intervals are too wide to assert it.",
        "",
    ]


def step_1a(ctx: Dict[str, Any]) -> List[str]:
    rows = ctx["cons"][3]
    body = [
        "## Step 1a - Conservative worst-category ratios",
        "",
        "Every ratio below is built from the same two Wilson bounds, so they are directly "
        "comparable. `conservative` is the **selection-robust** form: the largest Wilson LOWER "
        "bound over that model's estimable categories, divided by the Wilson UPPER bound of its "
        "mean. Taking the point-estimate winner and then quoting its lower bound is exposed to the "
        "winner's curse - the category that looks worst is partly the one that got lucky - so that "
        "variant is reported beside it, never as the headline. `excl worst` removes the worst "
        "category's own items from the mean's denominator, because otherwise the worst category "
        "sits inside the quantity it is being compared against.",
        "",
        T.md_table(
            ["model", "mean", "mean 95% CI", "worst category (point)", "worst rate",
             "worst 95% CI", "2nd worst", "point ratio", "**conservative**", "excl worst"],
            [[r["model"], T.fmt(r["mean"], 4),
              f"{T.fmt(r['mean_lo'], 4)}-{T.fmt(r['mean_hi'], 4)}", r["point_cat"] or "-",
              T.fmt(r["point_rate"], 4),
              f"{T.fmt(r['point_lo'], 4)}-{T.fmt(r['point_hi'], 4)}",
              f"{r['second_cat'] or '-'} {T.fmt(r['second_rate'], 4)}",
              f"{T.fmt(r['point_ratio'], 2)}x", f"**{T.fmt(r['cons_ratio'], 2)}x**",
              f"{T.fmt(r['cons_ratio_excl'], 2)}x"] for r in rows]),
        "",
        "### Sensitivity: a stricter 5-leaf floor",
        "",
        T.md_table(["floor", "median point ratio", "median conservative ratio",
                    "models > 2x (point)", "models > 2x (conservative)"],
                   [[f"{f} leaves", T.fmt(s['median_point'], 2), T.fmt(s['median_cons'], 2),
                     f"{s['n_over_bar_point']}/12", f"{s['n_over_bar']}/12"]
                    for f, s in ctx["survivors"].items()]),
        "",
        f"Models still above 2x conservatively (3-leaf floor): "
        f"{', '.join(ctx['survivors'][3]['models_over_bar']) or 'none'}.",
        "",
    ]
    return body + _verdict_1a(ctx)


def _abs_table(ctx: Dict[str, Any]) -> str:
    return T.md_table(
        ["model (3 most stable)", "mean wobble", "worst category", "worst wobble",
         "worst 95% CI", "ratio"],
        [[b["model"], T.fmt(b["mean"], 4), b["point_cat"] or "-", T.fmt(b["point_rate"], 4),
          f"{T.fmt(b['point_lo'], 4)}-{T.fmt(b['point_hi'], 4)}", f"{T.fmt(b['point_ratio'], 2)}x"]
         for b in ctx["best_absolute"]])


def step_1d(ctx: Dict[str, Any]) -> List[str]:
    a, f = ctx["worst_on_mean"], ctx["worst_on_mean_frontier"]
    return [
        "## Step 1d - Does the ratio really grow with capability?",
        "",
        "The stage-2 evidence for *\"the gap grows as models improve\"* was a correlation between "
        "mean wobble and a ratio that has mean wobble in its denominator. This restates it with no "
        "shared term: regress worst-category wobble directly on mean wobble. A slope BELOW 1 would "
        "mean the worst category falls more slowly than the mean, which is the claim.",
        "",
        T.md_table(["outcome", "model set", "n", "slope", "slope 95% CI", "intercept",
                    "intercept 95% CI", "R2"],
                   [[k["y"], k["label"], k["n"], T.fmt(k["slope"], 3),
                     f"{T.fmt(k['lo'], 3)} to {T.fmt(k['hi'], 3)}", T.fmt(k["intercept"], 4),
                     f"{T.fmt(k['intercept_lo'], 4)} to {T.fmt(k['intercept_hi'], 4)}",
                     T.fmt(k["r2"], 3)] for k in ctx["regressions"] if "error" not in k]),
        "",
        "### The absolute numbers, which the paper must quote beside every ratio",
        "",
        _abs_table(ctx),
        "",
        "A 5x between 2.5% and 12.5% reads nothing like a 5x between 10% and 50%, and a reviewer "
        "outside the project will ask which one it is. For the three most stable models it is the "
        "former: headline wobble of 2.6-3.0%, worst-category wobble of 12.5-50%, on categories of "
        "3 leaves whose intervals run from roughly 0.02 to 0.78. Those intervals are the finding "
        "as much as the point estimates are.",
        "",
        "**What this decides. The claim is not supported, and the stage-2 version of it was an "
        "artefact of two models.**",
        "",
        f"Across all 12 models the slope is {T.fmt(a['slope'], 2)} "
        f"({T.fmt(a['lo'], 2)} to {T.fmt(a['hi'], 2)}) - above 1, not below it, so worst-category "
        "wobble falls FASTER in absolute terms than the mean does, which is the opposite of the "
        "hypothesis. The ratio nevertheless grows as models improve, and the table shows why: the "
        f"intercept is {T.fmt(a['intercept'], 3)} "
        f"({T.fmt(a['intercept_lo'], 3)} to {T.fmt(a['intercept_hi'], 3)}), safely above zero, so "
        "as mean wobble goes to zero the ratio goes to infinity by arithmetic. A ratio driven by a "
        "positive intercept is a different sentence from \"the worst category resists improvement\".",
        "",
        f"And on the pre-registered frontier split - the 10 models excluding the two 1B ones - the "
        f"relationship disappears entirely: slope {T.fmt(f['slope'], 2)} "
        f"({T.fmt(f['lo'], 2)} to {T.fmt(f['hi'], 2)}), R2 = {T.fmt(f['r2'], 3)}. The whole "
        "association across 12 models is carried by two low-tier models sitting an order of "
        "magnitude away from the other ten. Among the models anyone would actually deploy, worst-"
        "category wobble is unrelated to headline wobble.",
        "",
        "This is not a weaker version of the claim. It is the absence of the claim, and it was "
        "found only because the regression was run on a pre-registered subset rather than on all "
        "twelve points at once.",
        "",
    ]
