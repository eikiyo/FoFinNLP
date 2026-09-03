"""
Location: paper-a/analysis/report_s3b.py
Purpose: STAGE3_REPORT.md sections for step 1b (the fold decomposition) and step 1c (why the empty
         zone is empty), plus assembly of the whole stage-3 report.
Functions: step_1b(), step_1c(), closing(), write()
Calls: none (pure over the stage-3 context)
Imports: pathlib, typing, report_s3, tables_out
"""

from pathlib import Path
from typing import Any, Dict, List

import report_s3 as R
import tables_out as T


def _bracket_table(sv: Dict[str, Any]) -> str:
    return T.md_table(
        ["structural model", "what it assumes about wrong runs", "rho(structural, accuracy)",
         "rho(residual, accuracy)"],
        [["lower bound", "all wrong runs give the SAME answer", T.fmt(sv["rho_structural_min"], 4),
          T.fmt(sv["rho_residual_min"], 4)],
         ["**calibrated (primary)**", "measured: always-wrong items flip at the corpus rate, "
          "estimated leave-one-leaf-out", f"**{T.fmt(sv['rho_structural_cal'], 4)}**",
          f"**{T.fmt(sv['rho_residual_cal'], 4)}**"],
         ["upper bound", "every wrong run gives a DIFFERENT answer",
          T.fmt(sv["rho_structural_max"], 4), T.fmt(sv["rho_residual_max"], 4)]])


def step_1b(ctx: Dict[str, Any]) -> List[str]:
    sv, ft, fs = ctx["surviving"], ctx["fold_test"], ctx["fold_test_structural"]
    pb = {r["bucket"]: r for r in ctx["p_buckets"]}
    zero = pb["p=0 (always wrong)"]
    return [
        "## Step 1b - The wobble-accuracy fold test",
        "",
        f"Stage 2 reported Spearman(leaf wobble, leaf accuracy) = "
        f"{T.fmt(sv['rho_observed'], 4)} over {sv['n']} leaves and flagged that part of it must be "
        "mechanical, since both are computed from the same runs. This decomposes it.",
        "",
        "### Is it folded?",
        "",
        f"Fitting wobble ~ accuracy + accuracy^2 gives a quadratic term of "
        f"{T.fmt(ft['quad_beta'], 3)} ({T.fmt(ft['quad_lo'], 3)} to {T.fmt(ft['quad_hi'], 3)}). "
        "That is POSITIVE - convex - where a fold would be negative. **Not folded.**",
        "",
        f"But that verdict is bounded by coverage, and the bound matters: leaf accuracy in this "
        f"corpus runs only from {T.fmt(ft['acc_min'], 3)} to {T.fmt(ft['acc_max'], 3)}. The fold's "
        "left arm - the low-accuracy region where wobble should fall again - is barely sampled. "
        f"Run on the structural prediction itself the quadratic is {T.fmt(fs['quad_beta'], 3)} "
        f"({T.fmt(fs['quad_lo'], 3)} to {T.fmt(fs['quad_hi'], 3)}), which also does not fold over "
        "this range. So the honest statement is that the fold is not observable here, not that it "
        "was tested and refuted.",
        "",
        "### How much of the correlation is mechanical?",
        "",
        "The two structural models differ only on items the model gets ALWAYS WRONG: one says a "
        "wrong model is wrong the same way every run, the other says it is wrong a different way "
        "each run. That is measurable rather than assumable, and measuring it is what fixes the "
        "answer:",
        "",
        T.md_table(["items", "n", "flipped", "observed flip rate", "lower bound predicts",
                    "upper bound predicts"],
                   [[r["bucket"], r["n_items"], r["n_flipped"], T.fmt(r["flip_rate"], 4),
                     T.fmt(r["predicted_lo"], 2) if r["predicted_lo"] is not None else "-",
                     T.fmt(r["predicted_hi"], 2) if r["predicted_hi"] is not None else "-"]
                    for r in ctx["p_buckets"]]),
        "",
        f"Only the first row carries information. The other two are definitional - an item with a "
        "mix of right and wrong runs has by definition produced two different answers and so has "
        "flipped, and an item answered correctly every time cannot have. They are reported anyway "
        "because they are a genuine control: had either deviated, the join would be broken.",
        "",
        f"Among the {zero['n_items']} always-wrong items, {zero['n_flipped']} flip - "
        f"**{T.fmt(zero['flip_rate'], 4)}**. Reality sits about a quarter of the way from the "
        "lower bound to the upper. Models that are wrong are usually wrong the same way, but not "
        "always.",
        "",
        _bracket_table(sv),
        "",
    ] + _verdict_1b(sv)


def _verdict_1b(sv: Dict[str, Any]) -> List[str]:
    return [
        "**What this decides. Concede. The difficulty objection lands, and the paper must stop "
        "using this correlation as evidence.**",
        "",
        f"Under the calibrated model the structural component alone tracks accuracy at "
        f"{T.fmt(sv['rho_structural_cal'], 4)} - slightly MORE negative than the observed "
        f"{T.fmt(sv['rho_observed'], 4)} - and the residual is "
        f"{T.fmt(sv['rho_residual_cal'], 4)}, which is nothing. Essentially none of the "
        "correlation survives once each leaf's distribution of per-item correct rates is known.",
        "",
        "The one honest qualification, stated because it cuts against this conclusion: the "
        "calibrated model contains a definitional component (interior-p items have flipped by "
        "construction), so this decomposition is closer to an identity than to an independent "
        "test. The parameter-free lower-bound model, which has no definitional component at all, "
        f"leaves {T.fmt(sv['rho_residual_min'], 4)} of the {T.fmt(sv['rho_observed'], 4)} intact. "
        "The gap between those two answers IS the definitional part.",
        "",
        "Either way the paper's position is the same, and it is the conservative one: leaf wobble "
        "and leaf accuracy are two summaries of the same per-item outcome distribution, so their "
        "correlation is not evidence for anything and should not be presented as if it were. Drop "
        "it from the results and state the relationship as a limitation. The category-level "
        "comparison is a different question and is unaffected by this - but it now has to carry "
        "the paper alone.",
        "",
    ]


def step_1c(ctx: Dict[str, Any]) -> List[str]:
    p, z = ctx["pooled_p"], ctx["zone"]
    return [
        "## Step 1c - Why is the empty zone empty?",
        "",
        f"Stage 2 found zero leaves at accuracy >= {z['threshold_accuracy']} and wobble >= "
        f"{z['threshold_wobble']}, and refused to move the threshold. Two explanations were "
        "available and they are opposite sentences: models never produce silently-unstable-but-"
        "correct clauses, or this item pool cannot express one.",
        "",
        "### The pooled per-item correct rate",
        "",
        T.md_table(["quantity", "value"],
                   [["items pooled over all 12 models x 60 leaves", f"{p['n_items']:,}"],
                    ["mean per-item correct rate", T.fmt(p["mean"], 4)],
                    ["share at exactly p = 1", T.pct(p["frac_one"], 1)],
                    ["share at exactly p = 0", T.pct(p["frac_zero"], 1)],
                    ["share strictly between", T.pct(p["frac_interior"], 1)],
                    ["share in the mid band 0.3 <= p <= 0.7", T.pct(p["frac_mid"], 1)]]),
        "",
        "**Strongly bimodal.** Five sixths of all measurements are items the model answers "
        "correctly on every single run. Only one item in fifty sits anywhere near the middle, "
        "which is the only region where an item can flip while staying mostly correct.",
        "",
        "### The empirical frontier, by accuracy decile",
        "",
        T.md_table(["accuracy decile", "leaves", "max observed wobble",
                    "max structurally reachable"],
                   [[r["decile"], r["n_leaves"], T.fmt(r["max_observed"], 4),
                     T.fmt(r["max_structural"], 4)] for r in ctx["frontier"]]),
        "",
        f"**What this decides. It is a fact about the item pool, not about models.**",
        "",
        f"Of the {z['n_high_accuracy_leaves']} leaves at accuracy >= {z['threshold_accuracy']}, "
        f"the most unstable reaches {T.fmt(z['max_observed'], 4)} wobble - and the most that the "
        f"structure of those leaves' items could produce is {T.fmt(z['max_structural'], 4)}, "
        f"against a threshold of {z['threshold_wobble']}. The region was unreachable before any "
        "model was run. The paper must therefore write the limitation sentence, not the finding "
        "sentence: *we did not observe clauses that models answer correctly yet unstably, and our "
        "item pool could not have contained them at this threshold.*",
        "",
        f"One nuance worth keeping, because it points at where such items would be found: at high "
        f"accuracy the observed maximum ({T.fmt(z['max_observed'], 4)}) EXCEEDS the structural "
        f"maximum ({T.fmt(z['max_structural'], 4)}). Real instability above the mechanical floor "
        "does exist there. It is simply an order of magnitude smaller than the threshold stage 2 "
        "fixed in advance. That is the direct motivation for the prospective test in "
        "`out/PREREG_2a.md`, and it is why that test is worth running at all.",
        "",
    ]


def write(ctx: Dict[str, Any], extra: List[str], out: Path) -> Path:
    lines = (R.header(ctx) + R.step_1a(ctx) + ["---", ""] + step_1b(ctx) + ["---", ""]
             + step_1c(ctx) + ["---", ""] + R.step_1d(ctx) + ["---", ""] + extra)
    path = out / "STAGE3_REPORT.md"
    path.write_text("\n".join(lines) + "\n")
    return path
