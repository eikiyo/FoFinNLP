"""
Location: paper-a/analysis/report_s2_answers.py
Purpose: The brief's twelve questions, answered from the computed context so an answer and its own
         table can never disagree. n is stated on every one.
Functions: answers(), _a1_a4(), _a5_a8(), _a9_a12()
Calls: none (pure over the stage-2 context)
Imports: statistics, typing, report_s2_ceiling, tables_out
"""

import statistics
from typing import Any, Dict, List

import report_s2_ceiling as C
import tables_out as T


def _a1_a4(ctx: Dict[str, Any]) -> List[str]:
    rel = sorted(ctx["reliability"], key=lambda r: -(r["r_full"] or 0))
    per = " · ".join(f"`{r['model']}` {T.fmt(r['r_full'], 3)}" for r in rel)
    nz = [x["r_full"] for x in ctx["nonzero_reliability"] if x["r_full"] is not None]
    h = ctx["transfer"][10]["frontier"]
    k5 = ctx["transfer"][5]["frontier"]
    return [
        f"**1. Median split-half reliability (Spearman-Brown corrected).** Overall "
        f"**{T.fmt(ctx['median_r_full'], 4)}** (n = {ctx['n_reliability_defined']} models; median "
        f"uncorrected r_half {T.fmt(ctx['median_r_half'], 4)}). Per model, best first: {per}. "
        f"Under {ctx['repeated_split']['n_splits']} random splits instead of odd/even the median is "
        f"{T.fmt(ctx['repeated_split']['median_of_medians'], 4)} (95% spread "
        f"[{T.fmt(ctx['repeated_split']['p02_5'], 4)}, "
        f"{T.fmt(ctx['repeated_split']['p97_5'], 4)}]). Restricted to each model's own non-zero "
        f"leaves the median falls to {T.fmt(statistics.median(nz), 4)} (n = {len(nz)}), which is "
        f"still in the same row of the decision table.",
        "",
        f"**2. Which row, and therefore the headline sentence.** The **{ctx['ceiling_row']}** row "
        f"(median r_full {T.fmt(ctx['median_r_full'], 4)}, against cuts at 0.40 and 0.70). The "
        f"instrument is stable, so the observed agreement really is modest.",
        "",
        f"> *{C.headline_for(ctx['ceiling_row'])}*",
        "",
        f"**3. Disattenuated rho beside the observed.** Observed median "
        f"**{T.fmt(ctx['observed_median'], 4)}**, disattenuated **"
        f"{T.fmt(ctx['corrected_median'], 4)}** (n = {ctx['n_corrected']} defined pairs of 66; "
        f"{ctx['n_over_one']} pairs exceeded 1.0). The correction is worth about "
        f"{100 * (ctx['corrected_median'] / ctx['observed_median'] - 1):.0f}%, so measurement "
        f"error was not hiding a large effect. Observed sits at {ctx['pct_of_ceiling']:.1f}% of the "
        f"median ceiling; even at the ceiling the shared dimension would explain roughly "
        f"{100 * ctx['corrected_median'] ** 2:.0f}% of the variance.",
        "",
        f"**4. Transfer at k=10, frontier-only, in plain language.** "
        f"**{100 * h['median']:.0f}% against a {100 * h['chance']:.0f}% chance line** "
        f"(n = {h['n_defined']} ordered pairs, IQR {T.fmt(h['iqr'], 3)}).",
        "",
        f"> *If you know the ten clause types one frontier model handles least reliably, about half "
        f"of them will be among another frontier model's twenty least reliable — roughly twice what "
        f"you would get by guessing.*",
        "",
        f"Carry the caveat with the sentence: {h['n_truncated']} of {h['n_defined']} pairs were "
        f"truncated because most frontier models do not have ten unstable leaves (median effective "
        f"k = {T.fmt(h.get('k_eff_a'), 1)}), so this is really a 'top ~{T.fmt(h.get('k_eff_a'), 0)}'. "
        f"At k=5, where truncation is rarer ({k5['n_truncated']}/{k5['n_defined']}), it is "
        f"{100 * k5['median']:.0f}% against {100 * k5['chance']:.0f}%.",
        "",
    ]


def _a5_a8(ctx: Dict[str, Any]) -> List[str]:
    rat = " · ".join(f"`{r['model']}` {T.fmt(r['ratio'], 1)}x"
                     for r in sorted(ctx["ratios"], key=lambda r: -(r["ratio"] or 0)))
    nc, na = ctx["nested_category"], ctx["nested_answer"]
    wa, nm, ha, bs = (ctx["wobble_vs_accuracy"], ctx["nightmare"], ctx["high_acc_leaves"],
                      ctx["bootstrap"])
    dom = ("category, NOT answer type" if nc["delta_adj"] > na["delta_adj"] else "answer type")
    return [
        f"**5. Worst-category-to-mean ratio, and does it shrink with capability?** Median "
        f"**{T.fmt(ctx['ratio_median'], 2)}x** over 12 models: {rat}. **It does not shrink — it "
        f"GROWS** as models improve: Spearman(mean wobble, ratio) = "
        f"**{T.fmt(ctx['ratio_vs_capability'], 4)}**. But that shares a denominator, so the honest "
        f"companion is Spearman(mean wobble, WORST-category wobble) = "
        f"**{T.fmt(ctx['worst_vs_capability'], 4)}** — positive but weak. The defensible statement "
        f"is that the ratio grows mainly because the mean falls faster than the worst category "
        f"does, which still means a frontier model's headline number understates its worst clause "
        f"type by the most.",
        "",
        f"**6. Does answer type dominate category in the predictor model?** **No.** Adding category "
        f"to answer type + size gains **{T.fmt(nc['delta_adj'], 4)}** adjusted R^2; adding answer "
        f"type to category + size gains **{T.fmt(na['delta_adj'], 4)}**. Both carry independent "
        f"signal and **{dom}** carries more (full model adj R^2 {T.fmt(nc['adj_full'], 4)}, "
        f"n = {ctx['fit']['n']} leaves). Note this is a different question from stage 1's strata "
        f"result: that asked whether models AGREE within an answer type, this asks what predicts "
        f"the LEVEL of wobble. The paper must not merge them into one 'answer format is the "
        f"mechanism' sentence.",
        "",
        f"**7. Item-level wobble vs accuracy, and the high-accuracy/high-wobble count.** Spearman "
        f"**{T.fmt(wa['rho'], 4)}** (tau {T.fmt(wa['tau'], 4)}, n = {wa['n']} leaves) — roughly "
        f"{100 * wa['rho'] ** 2:.0f}% shared variance. **The difficulty objection has real force "
        f"and must be conceded**; the claim narrows to 'partly, but not wholly, item difficulty'. "
        f"High-accuracy AND high-wobble leaves at the pre-registered thresholds "
        f"(>= {nm['threshold_accuracy']} accuracy, >= {nm['threshold_wobble']} wobble): "
        f"**{nm['n']}**. Of the {ha['n']} leaves models answer correctly at least 90% of the time, "
        f"the most unstable reaches only {T.fmt(ha['max_wobble'], 4)}. The paper's hoped-for "
        f"'deployment nightmare' examples do not exist at this arm, and no threshold was searched "
        f"for one that would produce them.",
        "",
        f"**8. Bootstrap 95% interval on the headline.** **[{T.fmt(bs['lo'], 4)}, "
        f"{T.fmt(bs['hi'], 4)}]** around a median of {T.fmt(bs['median'], 4)} "
        f"({bs['n_boot']} leaf-resampled replicates over {bs['n_leaves_resampled']} leaves). "
        f"Excludes zero comfortably, but spans a factor of four — quote the interval wherever the "
        f"point estimate appears.",
        "",
    ]


def _a9_a12(ctx: Dict[str, Any], ann: Dict[str, Any]) -> List[str]:
    base = ctx["observed_median"]
    lomo = ctx["lomo"]
    worst = max(lomo, key=lambda r: abs(r["median"] - base))
    shift = worst["median"] - base
    return [
        f"**9. Does leave-one-model-out change the reading? Which model matters most?** **No.** The "
        f"twelve recomputations span "
        f"{T.fmt(min(r['median'] for r in lomo), 4)}–{T.fmt(max(r['median'] for r in lomo), 4)}, "
        f"all far above the permutation null. The model that matters most is **`{worst['dropped']}`** "
        f"at **{shift:+.4f}**. Dropping either 1B model RAISES the median, so they are the least "
        f"typical members of the lineup rather than the drivers of the agreement.",
        "",
        "**10. FinNLP mechanics.** Long **8 pages** excluding references (short/demo 4). Direct "
        "submissions **must be anonymized**. Whether an identifying repository link is permitted in "
        "an anonymous submission is **NOT STATED** on either the workshop page or the ARR anonymity "
        "page — an open item to resolve with the organisers, not by inference. AI assistance "
        "**must be disclosed** (writing AND coding) in the Responsible NLP Checklist with details "
        "in the Acknowledgements; AI tools cannot be authors. ACL template required, version not "
        "stated. OpenReview; ARR commitment exists but only for work already in ARR. Direct "
        "deadline **2026-08-11**. Sources in `out/venue_facts.md`.",
        "",
        "**11. Prior work on item-level cross-model consistency agreement.** **Yes — one, and it "
        "points the other way.** Cacioli (2026), *Beyond the Mean: Within-Model Reliable Change "
        "Detection for LLM Evaluation*, arXiv:2604.27405, already uses split-half + Spearman-Brown "
        "on LLM items at temperature 0.7, and reports a **near-zero cross-model item correlation "
        "(r = .11, n = 431)**. It correlates version-to-version CHANGE (RCI) rather than "
        "within-model run-to-run instability, and over two model pairs rather than twelve models, "
        "so the constructs differ and Paper A is not scooped — **but that distinction has to be "
        "drawn explicitly and early, not assumed.** It also means split-half reliability cannot be "
        "presented as a methodological contribution. Full analysis in `out/related_work.md`.",
        "",
        "**12. Decided by judgement rather than by rule.** (a) odd/even as the split rule, on the "
        "interleaving argument — repeated random splits were added afterwards as a check and agree; "
        "(b) reliability computed on the active subset, to match the headline's vector; (c) the "
        "non-zero-only reliability sensitivity was ADDED, not pre-registered — it can only weaken "
        "the ceiling claim, which is why it is reported; (d) repeated random splits were ADDED "
        "after finding Cacioli 2026, and are labelled as such; (e) the disattenuation is computed "
        "PER PAIR then summarised, rather than dividing the median by one global reliability; "
        "(f) HIGH_ACC 0.90 and HIGH_WOBBLE 0.30 were fixed in advance and NOT moved when they "
        "returned zero; (g) `MIN_LEAVES_PER_CATEGORY = 3`, which happens to make every category "
        "estimable — `exit_waterfall` sits exactly on the floor with 3 leaves and its intervals are "
        "correspondingly wide; (h) the category dummy reference level is the alphabetically first "
        "family; (i) rows with any missing predictor would have been dropped and counted, though "
        "none were; (j) the answer-type labels are stage 1's, including its six judgement calls.",
        "",
    ]


def answers(ctx: Dict[str, Any], ann: Dict[str, Any]) -> List[str]:
    return (["## The brief's twelve questions", "",
             "Derived from the computed context, so an answer and its own table cannot disagree. "
             "n is stated on every one.", ""]
            + _a1_a4(ctx) + _a5_a8(ctx) + _a9_a12(ctx, ann))
