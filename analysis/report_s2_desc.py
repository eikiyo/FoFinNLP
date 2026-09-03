"""
Location: paper-a/analysis/report_s2_desc.py
Purpose: STAGE2_REPORT sections 2 and 3 -- transfer (the practitioner-facing number) and the
         descriptive category + predictor layer. Both verdicts are derived: the transfer caveat is
         computed from the truncation counts, and the answer-type-vs-category question is settled
         by comparing two nested adjusted-R^2 deltas rather than by assertion.
Functions: transfer_section(), category_section(), predictor_section()
Calls: none (pure over the stage-2 context)
Imports: typing, tables_out
"""

from typing import Any, Dict, List

import tables_out as T

KS = (5, 10, 20)


def _transfer_rows(ctx: Dict[str, Any]) -> List[List[str]]:
    rows = []
    for k in KS:
        for label, key in (("frontier-only", "frontier"), ("all 12 models", "all")):
            s = ctx["transfer"][k][key]
            rows.append([str(k), label, str(s["n_defined"]), T.fmt(s["median"], 3),
                         T.fmt(s["iqr"], 3), T.fmt(s["chance"], 3), T.fmt(s["median_lift"], 3),
                         T.fmt(s.get("k_eff_a"), 1), str(s["n_truncated"])])
    return rows


def transfer_section(ctx: Dict[str, Any]) -> List[str]:
    h = ctx["transfer"][10]["frontier"]
    k5 = ctx["transfer"][5]["frontier"]
    return [
        "## Step 2 - Transfer: the number a practitioner can act on",
        "",
        "**Computed.** For every ORDERED model pair, the share of A's top-k unstable leaves that "
        "fall inside B's top-2k. Ordered rather than symmetrised, because the relation genuinely "
        "differs by direction when two models have different numbers of non-zero leaves. Where a "
        "model has fewer than k non-zero leaves, only its non-zero entries are used and the "
        "truncation is recorded -- padding with zeros would rank arbitrary stable leaves and "
        "manufacture overlap. The chance line is recomputed per pair from the EFFECTIVE k.",
        "",
        T.md_table(["k", "set", "pairs", "median", "IQR", "chance", "lift", "median k_eff",
                    "truncated"], _transfer_rows(ctx)),
        "",
        "### What step 2 decides",
        "",
        f"> **{100 * h['median']:.0f}% against a {100 * h['chance']:.0f}% chance line** "
        f"(k = 10, frontier-only, n = {h['n_defined']} ordered pairs) -- a "
        f"{h['median'] / h['chance']:.1f}x lift.",
        "",
        "**In plain language, as a practitioner would read it:** *if you know which ten clause "
        "types one frontier model answers least reliably, half of them will sit in another "
        "frontier model's twenty least reliable -- about twice what guessing would give you.*",
        "",
        f"**The caveat that must travel with that sentence:** {h['n_truncated']} of "
        f"{h['n_defined']} pairs were truncated, because at this arm most frontier models do not "
        f"HAVE ten unstable leaves (median effective k = {T.fmt(h.get('k_eff_a'), 1)}). The k = 10 "
        f"row is really a 'top ~{T.fmt(h.get('k_eff_a'), 0)}'. The k = 5 row "
        f"({100 * k5['median']:.0f}% vs {100 * k5['chance']:.0f}% chance, "
        f"{k5['n_truncated']}/{k5['n_defined']} truncated) is the cleaner claim, and the two "
        "should be reported together rather than the larger lift alone.",
        "",
    ]


def _category_rows(ctx: Dict[str, Any]) -> List[List[str]]:
    m0 = ctx["models"][0]
    return [[c, str(ctx["cat_cells"][m0][c]["n_leaves"]),
             "yes" if ctx["cat_cells"][m0][c]["estimable"] else "**not estimable**"]
            for c in sorted({l["family"] for l in ctx["leaves"]})]


def _ratio_rows(ctx: Dict[str, Any]) -> List[List[str]]:
    return [[f"`{r['model']}`", T.fmt(r["mean"], 4), r["worst_cat"] or "-", T.fmt(r["worst"], 4),
             f"[{T.fmt(r.get('worst_lo'), 3)}, {T.fmt(r.get('worst_hi'), 3)}]",
             T.fmt(r["ratio"], 2)] for r in sorted(ctx["ratios"], key=lambda r: r["mean"])]


def _ratio_verdict(ctx: Dict[str, Any]) -> str:
    w = ctx["worst_vs_capability"]
    if w is None:
        return "That comparison is undefined."
    if w > 0.2:
        return (f"That is POSITIVE ({T.fmt(w, 3)}): worse models do have worse worst-categories, "
                "so the ratio relationship is not purely mechanical. But it is far weaker than "
                "the ratio correlation implies, and the honest reading is that the ratio grows "
                "mainly because the MEAN falls faster than the worst category does.")
    return ("That is near zero, so the worst category barely tracks capability and the ratio "
            "relationship is largely a denominator artefact. Report the ratio itself, not the "
            "correlation.")


def category_section(ctx: Dict[str, Any]) -> List[str]:
    m0 = ctx["models"][0]
    return [
        "## Step 3 - The descriptive category layer",
        "",
        "**Computed.** A model x category matrix of wobble with **Wilson score intervals** -- not "
        "the normal approximation, because most cells here sit near zero, where a normal interval "
        "on 0/n returns [0, 0] and asserts certainty. Item counts are summed and the rate formed "
        "from the totals; per-leaf rates are never averaged, which would weight a 3-item leaf like "
        f"a 30-item one. Instrument check: {ctx['cat_selftest']}.",
        "",
        "Full matrix with n and both interval bounds on every cell: "
        "`out/tables/model_x_category_wilson.csv`.",
        "",
        T.md_table(["Category", "leaves", "estimable (>= 3 leaves)"], _category_rows(ctx)),
        "",
        "### Worst-category ratio - the evidence for the deployment recommendation",
        "",
        T.md_table(["Model", "mean wobble", "worst category", "worst wobble", "95% CI", "ratio"],
                   _ratio_rows(ctx)),
        "",
        f"- Median worst-to-mean ratio: **{T.fmt(ctx['ratio_median'], 2)}x**. A model's headline "
        "wobble understates its worst clause type by roughly that factor.",
        f"- Spearman(mean wobble, ratio) = **{T.fmt(ctx['ratio_vs_capability'], 4)}**: the ratio "
        "GROWS as models get better -- so the headline number is *most* misleading for the models "
        "a practitioner is most likely to deploy.",
        f"- **But that correlation shares a denominator** (the mean is the ratio's divisor), so "
        "some inverse relationship is mechanical. The same question without the shared term: "
        f"Spearman(mean wobble, WORST-category wobble) = "
        f"**{T.fmt(ctx['worst_vs_capability'], 4)}**. " + _ratio_verdict(ctx),
        "",
        f"> Every pair of category cells whose Wilson intervals overlap is **statistically "
        f"indistinguishable and must not be ordered in prose**. For `{m0}` alone, "
        f"{len(ctx['indistinguishable'][m0])} category pairs overlap; the full set is derivable "
        "from the interval columns in the CSV.",
        "",
    ]


def _answer_vs_category(nc: Dict[str, Any], na: Dict[str, Any]) -> str:
    if nc["delta_adj"] > na["delta_adj"]:
        return (f"> **No -- answer type does NOT dominate.** Category adds "
                f"{T.fmt(nc['delta_adj'], 4)} adjusted R^2 on top of answer type and size, while "
                f"answer type adds only {T.fmt(na['delta_adj'], 4)} on top of category and size. "
                "Both blocks carry independent signal and category carries more. This is a "
                "DIFFERENT question from stage 1's strata result, which asked whether models "
                "AGREE within an answer type; this asks what predicts the LEVEL of wobble. A "
                "sentence claiming answer type is the mechanism would overstate what this shows.")
    return (f"> **Yes -- answer type dominates.** It adds {T.fmt(na['delta_adj'], 4)} adjusted "
            f"R^2 on top of category and size, while category adds {T.fmt(nc['delta_adj'], 4)} on "
            "top of answer type. Category is largely redundant once answer type is known.")


def predictor_section(ctx: Dict[str, Any]) -> List[str]:
    f, nc, na = ctx["fit"], ctx["nested_category"], ctx["nested_answer"]
    coefs = [[c["name"], T.fmt(c["beta"], 6), f"[{T.fmt(c['lo'], 6)}, {T.fmt(c['hi'], 6)}]",
              "crosses 0" if c["crosses_zero"] else "**excludes 0**"] for c in f["coefs"]]
    return [
        "### Item-level predictors (DESCRIPTIVE - not a predictive model)",
        "",
        f"OLS on per-leaf mean wobble across models, **n = {f['n']} leaves**, {f['p']} parameters. "
        f"R^2 = {T.fmt(f['r2'], 4)}, **adjusted R^2 = {T.fmt(f['adj_r2'], 4)}**. With 60 leaves "
        "this describes the sample; it does not predict out of sample and is not presented as if "
        "it does.",
        "",
        T.md_table(["Term", "beta", "95% CI", "verdict"], coefs),
        "",
        "**Does answer type dominate category?** Nested adjusted-R^2 comparison, which (unlike "
        "R^2) can fall when a block adds only noise:",
        "",
        T.md_table(["Base", "+ block", "adj R^2 base", "adj R^2 full", "delta"], [
            ["answer type + size", "category", T.fmt(nc["adj_base"], 4),
             T.fmt(nc["adj_full"], 4), T.fmt(nc["delta_adj"], 4)],
            ["size + category", "answer type", T.fmt(na["adj_base"], 4),
             T.fmt(na["adj_full"], 4), T.fmt(na["delta_adj"], 4)],
        ]),
        "",
        _answer_vs_category(nc, na),
        "",
    ]
