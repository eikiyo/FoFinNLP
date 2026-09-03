"""
Location: paper-a/analysis/report_s2_robust.py
Purpose: STAGE2_REPORT section 4 (the four robustness checks), section 5 (the prepared annotation
         study and the two research deliverables), and the assembly of the whole report.
Functions: difficulty_section(), precision_section(), sensitivity_section(), step5(), write()
Calls: none (pure over the stage-2 context)
Imports: pathlib, typing, config, report_s2_ceiling, report_s2_desc, tables_out
"""

from pathlib import Path
from typing import Any, Dict, List

import config
import report_s2_ceiling as C
import report_s2_answers as A
import report_s2_desc as D
import tables_out as T


def _nightmare_verdict(nm: Dict[str, Any], ha: Dict[str, Any]) -> str:
    if nm["n"] > 0:
        return (f"> {nm['n']} leaves are both high-accuracy and high-wobble. These are the "
                "deployment cases the paper is about and the best concrete examples available.")
    return (f"> **Zero, at the threshold fixed in advance -- an inconvenient result, reported as "
            f"found.** The brief expected these to be the paper's best concrete examples; at this "
            f"arm they do not exist. Of the {ha['n']} leaves models answer correctly at least 90% "
            f"of the time, the MOST unstable reaches only {T.fmt(ha['max_wobble'], 4)} wobble. No "
            "threshold was searched for one that would produce examples. The five nearest misses "
            "are listed below purely descriptively, so a reader can see where the boundary sits.")


def difficulty_section(ctx: Dict[str, Any]) -> List[str]:
    wa, nm, ha = ctx["wobble_vs_accuracy"], ctx["nightmare"], ctx["high_acc_leaves"]
    shared = 100 * wa["rho"] ** 2
    return [
        "## Step 4 - Supporting analyses that pre-empt specific attacks",
        "",
        "### 4a. Is wobble just item difficulty?",
        "",
        f"Spearman(per-leaf mean wobble, per-leaf mean majority accuracy) = "
        f"**{T.fmt(wa['rho'], 4)}** (Kendall tau {T.fmt(wa['tau'], 4)}, n = {wa['n']} leaves).",
        "",
        f"> **The objection has force and the paper must concede it.** A correlation of "
        f"{T.fmt(wa['rho'], 3)} means roughly {shared:.0f}% of the variance in leaf instability is "
        f"shared with difficulty. The defensible claim is the narrow one: instability is PARTLY, "
        f"but not wholly, item difficulty -- about {100 - shared:.0f}% of the variance is not "
        "shared. A caveat cutting the other way: wobble and accuracy are computed from the SAME "
        "runs, so part of this correlation is mechanical rather than substantive.",
        "",
        f"**High-accuracy AND high-wobble leaves (pre-registered thresholds: accuracy >= "
        f"{nm['threshold_accuracy']}, wobble >= {nm['threshold_wobble']}): {nm['n']}.**",
        "",
        _nightmare_verdict(nm, ha),
        "",
        T.md_table(["Leaf (nearest misses, descriptive)", "mean wobble", "mean accuracy"],
                   [[f"`{r['leaf']}`", T.fmt(r["mean_wobble"], 4), T.fmt(r["mean_accuracy"], 4)]
                    for r in ha["top"]]),
        "",
    ]


def precision_section(ctx: Dict[str, Any]) -> List[str]:
    bs = ctx["bootstrap"]
    return [
        "### 4b. Bootstrap interval on the headline",
        "",
        f"Percentile bootstrap over LEAVES, {bs['n_boot']} replicates, fixed seed: median rho "
        f"**{T.fmt(bs['median'], 4)}**, **95% CI [{T.fmt(bs['lo'], 4)}, {T.fmt(bs['hi'], 4)}]** "
        f"(resampling {bs['n_leaves_resampled']} leaves; the worst replicate left "
        f"{bs['max_undefined_pairs_in_a_replicate']} pairs undefined, counted rather than "
        "silently dropped).",
        "",
        "> The permutation null said *not zero*. This says *not precise*. The interval excludes "
        "zero comfortably but spans a factor of four, so the paper can claim the effect exists "
        "and cannot claim its size to two decimals. Quote the interval wherever the point "
        "estimate appears.",
        "",
    ]


def sensitivity_section(ctx: Dict[str, Any]) -> List[str]:
    base = ctx["observed_median"]
    lomo = sorted(ctx["lomo"], key=lambda r: r["median"])
    worst = max(abs(r["median"] - base) for r in lomo)
    who = max(lomo, key=lambda r: abs(r["median"] - base))
    stable = ("no single model carries the result" if worst < 0.05 else
              "ONE MODEL MATERIALLY MOVES THE RESULT and that belongs in the paper")
    rho = ctx["weighting_rho"]
    weigh = ("The two weightings order the models almost identically, so the stage-1 capability "
             "split does not rest on the weighting choice and the reading is unchanged."
             if rho is not None and rho > 0.9 else
             "The two weightings order the models differently, so the capability split DOES rest "
             "on the weighting choice and both must be reported in the paper.")
    return [
        "### 4c. Leave-one-model-out",
        "",
        T.md_table(["Model dropped", "pairs", "median rho", "shift"],
                   [[f"`{r['dropped']}`", str(r["n_pairs"]), T.fmt(r["median"], 4),
                     f"{r['median'] - base:+.4f}"] for r in lomo]),
        "",
        f"> The largest shift is **{worst:+.4f}** (dropping `{who['dropped']}`), so {stable}. All "
        "twelve recomputations stay far above the permutation null. Note the direction: dropping "
        "either 1B model RAISES the median, consistent with them being the least typical members "
        "of the lineup rather than the drivers of the agreement.",
        "",
        "### 4d. Item-count weighting",
        "",
        f"Spearman between the item-weighted ordering (what the benchmark reports) and the "
        f"leaf-equal ordering = **{T.fmt(rho, 4)}** over {len(ctx['weighting'])} models. " + weigh,
        "",
    ]


def step5(ctx: Dict[str, Any], ann: Dict[str, Any], frac: float) -> List[str]:
    return [
        "## Step 5 - The two attacks statistics cannot answer",
        "",
        "### 5a. Annotation agreement",
        "",
        f"**PREPARED, NOT RUN.** A stratified {int(100 * frac)}% sample of **{ann['n_leaves']} "
        f"leaves / {ann['n_items']} items** is drawn with a fixed seed, alongside the protocol and "
        "a blank scoring sheet: `out/annotation/`.",
        "",
        "> **The paper has no agreement figure yet, and this stage did not produce one.** It is a "
        "blocking item, not a completed one. The materials reduce it to a single sitting; they do "
        "not substitute for it. The scoring sheet deliberately withholds the original label, "
        "because a re-annotator who can see it measures agreement with a prompt rather than two "
        "independent readings.",
        "",
        "### 5b. Related work",
        "",
        "`out/related_work.md` -- every citation verified against a live record (arXiv API or the "
        "ACL Anthology), each with its claim and its relation to this paper. **One directly "
        "adjacent prior result exists and it points the other way.** After the ceiling, that is "
        "the most important finding in this stage; it is discussed in full there.",
        "",
        "### 5c. Venue mechanics",
        "",
        "`out/venue_facts.md` -- fetched from the live call for papers with the URL beside every "
        "fact, and NOT STATED recorded where the page is silent rather than inferred from "
        "convention.",
        "",
    ]


def write(ctx: Dict[str, Any], ann: Dict[str, Any], frac: float, out: Path) -> Path:
    body = [
        "# STAGE 2 REPORT - Paper A: ceiling, transfer, description, and the two attacks",
        "",
        f"**Arm:** {config.ARM_HUMAN} only. Probity `v1.3.1`, read from disk. No number here "
        "derives from the 0.1 arm or from any cross-arm comparison.",
        "",
        "Continues the C2 diagnostic (`out/C2_REPORT.md`), which returned Row 1. Pre-registration "
        "for this stage: `DESIGN-stage2.md`, written before any stage-2 coefficient was computed. "
        "Regenerate everything: `python3 analysis/run_all.py`.",
        "",
        "---",
        "",
    ]
    body += C.section(ctx) + ["---", ""]
    body += D.transfer_section(ctx) + ["---", ""]
    body += D.category_section(ctx) + D.predictor_section(ctx) + ["---", ""]
    body += difficulty_section(ctx) + precision_section(ctx) + sensitivity_section(ctx)
    body += ["---", ""] + step5(ctx, ann, frac) + ["---", ""] + A.answers(ctx, ann)
    path = out / "STAGE2_REPORT.md"
    path.write_text("\n".join(body) + "\n")
    return path
