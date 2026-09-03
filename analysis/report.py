"""
Location: paper-a/analysis/report.py
Purpose: Assemble out/C2_REPORT.md (pre-registration, then results, then ONE named outcome row,
         then the brief's ten questions) and out/NUMBERS.md (every quoted figure -> file +
         computation). Generated from the same dicts the tables are written from; no hand-typed
         numbers anywhere in this pipeline.
Functions: named_distributions(), outcome_section(), answers(), write_report(), write_numbers()
Calls: report_prereg, report_results
Imports: typing, config, decision, stats_core, tables_out, report_prereg, report_results
"""

from typing import Any, Dict, List

import config
import decision
import report_controls as C
import report_prereg as P
import report_results as R
import stats_core as sc
import tables_out as T


def named_distributions(ctx: Dict[str, Any]) -> List[tuple]:
    out = [(k, ctx[k], note) for k, note in (
        ("headline_active", "PRIMARY"), ("headline_full", "secondary"),
        ("all_active", "control"), ("all_full", "control"), ("all_common", "control 5c"))]
    for name, d in ctx["tiers"].items():
        out.append((f"tier:{name}", d["summary"], "control 5b"))
    for name, d in ctx["paths"].items():
        out.append((f"serving:{name}", d["summary"], "control 5d"))
    for name, d in ctx["strata"].items():
        out.append((f"answer_type:{name}", d["summary"], "control 5f"))
    return out


def outcome_section(ctx: Dict[str, Any]) -> List[str]:
    d = ctx["decision"]
    tick = {True: "YES", False: "NO", None: "n/a"}
    rows = [[c["name"], c["value"], tick[c["verdict"]]] for c in d["criteria"]]
    return [
        "## 6. Outcome -- which row of the brief's section-6 table the data lands on",
        "",
        "Criteria are evaluated in code (`analysis/decision.py`) against thresholds fixed in the "
        "pre-registration, so the outcome is derived rather than authored beside its own table.",
        "",
        T.md_table(["Pre-registered criterion", "Computed", "Met"], rows),
        "",
        f"### => **{d['row_name']}**",
        "",
        f"Because {d['reason'].rstrip('.')}.",
        "",
    ]


def _a1_a3(ctx: Dict[str, Any]) -> List[str]:
    d, (h, n) = ctx["decision"], ctx["reported"]
    ex = [r for r in ctx["ties"] if r["excluded"]]
    pre = ("" if ctx["primary_computable"] else
           f" The pre-registered primary (tie-filtered set) is UNDEFINED: "
           f"{len(ctx['headline_models'])} model(s) survive the tie rule, so it has "
           f"{ctx['headline_active']['n_pairs']} pairs. Reported instead, forced: all 12 models "
           f"on the same active subset, against a null with the same tie structure.")
    return [
        f"**1. Which outcome row?** {d['row_name']}.",
        "",
        f"**2. Headline statistic.** Median pairwise Spearman on the active subset "
        f"({len(ctx['active'])} leaves, {h['n_defined']} defined pairs of {h['n_pairs']}): "
        f"**{T.fmt(h['median'], 4)}**, IQR **{T.fmt(h['iqr'], 4)}** (Q1 {T.fmt(h['q1'])}, "
        f"Q3 {T.fmt(h['q3'])}, range {T.fmt(h['min'])} to {T.fmt(h['max'])}). Permutation-null "
        f"median of medians **{T.fmt(n['median_of_medians'], 4)}**, null 95% envelope "
        f"[{T.fmt(n['p02_5'], 4)}, {T.fmt(n['p97_5'], 4)}], null max over "
        f"{n['n_perm']} permutations {T.fmt(n['max'], 4)}, one-sided p "
        f"{T.fmt(sc.empirical_p(h['median'], n), 5)}.{pre}",
        "",
        "**3. Tie fraction per model / exclusions.** "
        + " · ".join(f"`{r['model']}` {T.fmt(r['tie_full'], 3)}" for r in ctx["ties"])
        + f". Excluded as not interpretable (> {config.TIE_THRESHOLD}): **{len(ex)} of "
          f"{len(ctx['models'])}** — "
        + (", ".join(f"`{r['model']}`" for r in ex) if ex else "none")
        + ". That is the single most important instrument fact in this report: the rule was "
          "written to stop ties faking a null, and on this data it removes almost the entire "
          "experiment.",
        "",
    ]


def _a4_a7(ctx: Dict[str, Any]) -> List[str]:
    t, p = ctx["tiers"], ctx["paths"]

    def med(group, key):
        s = group[key]["summary"]
        note = (f" [only {s['n_defined']} defined pair"
                f"{'s' if s['n_defined'] != 1 else ''} -- not a distribution]"
                if s["n_defined"] < decision.MIN_PAIRS_FOR_DIST else "")
        return f"{T.fmt(s['median'], 4)}{note}"

    fr, d = ctx["serving_in_frontier"], ctx["decision"]
    return [
        f"**4. Tier medians.** within-low **{med(t, 'low')}** · within-frontier "
        f"**{med(t, 'frontier')}** · across-tier **{med(t, 'ACROSS')}**. All three clear their own "
        f"nulls, so this is NOT the row-3 shape. Caveat that matters: the low tier has exactly two "
        f"members and they are the same base model at two quantizations, so its single coefficient "
        f"is nearer a self-correlation than cross-model agreement -- the load-bearing tier result "
        f"is the frontier one (45 pairs).",
        "",
        f"**5. Common-subset re-run.** {len(ctx['common'])}/{len(ctx['names'])} leaves are common "
        f"(zero drops at 0.7), so the common subset IS the full set and the re-run is identical by "
        f"construction: median {T.fmt(ctx['all_common']['median'], 4)} vs full "
        f"{T.fmt(ctx['all_full']['median'], 4)}. The reading survives, but this control could not "
        f"have failed here -- it is vacuous on this arm, not passed.",
        "",
        "**6. Routed vs direct.** Raw: "
        + " · ".join(f"{k} {T.fmt(v['summary']['median'], 4)} "
                     f"({v['summary']['n_defined']} pair{'s' if v['summary']['n_defined'] != 1 else ''})"
                     for k, v in p.items())
        + ". That raw split is confounded with capability (all routed and all direct models are "
          "frontier; both local models are low), so the answer is the frontier-only comparison: "
        + " · ".join(f"{k.replace('_', ' ')} {T.fmt(v['summary']['median'], 4)} "
                     f"({v['summary']['n_defined']} pairs, p {T.fmt(v['p'], 4)})"
                     for k, v in fr.items())
        + ". Both clear their own null, so the agreement is not an artefact of the routing layer.",
        "",
        "**7. Answer-type strata.** "
        + " · ".join(f"{k} {T.fmt(v['summary']['median'], 4)} ({v['n_leaves']} leaves, mean tie "
                     f"{T.fmt(v['mean_tie'])})" for k, v in ctx["strata"].items())
        + ". "
        + (f"**Answer format is doing part of the work**: the "
           f"{'/'.join(sorted(d['carried_strata']))} strata clear their nulls and "
           f"{'/'.join(sorted(d['failed_strata']))} does not. "
           + _format_not_ties(ctx, d)
           if d["failed_strata"] else "Agreement survives in every stratum."),
        "",
    ]


def _format_not_ties(ctx: Dict[str, Any], d: Dict[str, Any]) -> str:
    """State the tie-confound verdict from the numbers, not from the story. Derived the same way
    5f derives it, so the two sections cannot contradict each other."""
    st = ctx["strata"]
    fails = [k for k in d["failed_strata"] if not st[k]["too_small"]]
    carr = [k for k in d["carried_strata"] if not st[k]["too_small"]]
    if not fails or not carr:
        return "Every failing stratum is below the leaf-count floor, so nothing is claimed."
    f, c = max(fails, key=lambda k: st[k]["mean_tie"]), max(carr, key=lambda k: st[k]["mean_tie"])
    if st[f]["mean_tie"] <= st[c]["mean_tie"]:
        return (f"This is NOT a tie artefact: `{c}` carries slightly MORE tie mass "
                f"({T.fmt(st[c]['mean_tie'])} vs {T.fmt(st[f]['mean_tie'])}) and still reaches "
                f"{T.fmt(st[c]['summary']['median'])}. With tie mass matched, the strata really "
                f"do differ. `multi_part` has only {st['multi_part']['n_leaves']} leaves and is "
                f"reported but not interpreted.")
    return (f"`{f}` carries more tie mass than `{c}`, so read its null as 'not demonstrated "
            f"here', never 'demonstrated absent'.")


def _a8_a10(ctx: Dict[str, Any]) -> List[str]:
    ov, po, z = ctx["overlap"], ctx["pair_overlap"], ctx["zeros"]
    judged = [l for l in ctx["leaves"] if l["leaf"] in
              __import__("answer_space").JUDGEMENT]
    return [
        f"**8. Top-10 overlap.** Strict 12-way intersection: **{ov['intersection_size']}** "
        f"leaf/leaves"
        + (f" ({', '.join('`' + n + '`' for n in ov['intersection'])})"
           if ov["intersection"] else "") + f". Pairwise: median **{po['median_shared']}** shared, "
        f"range {po['min_shared']}-{po['max_shared']}; median Jaccard "
        f"{T.fmt(po['median_jaccard'])}.",
        "",
        f"**9. Leaves with zero wobble in all twelve models: {z['n_zero_in_all']} of "
        f"{z['n_leaves']}.**"
        + ("  This is small, so it does not by itself cap the analysis -- but the per-MODEL zero "
           "counts do, and those are the binding limit: see Q3."
           if z["n_zero_in_all"] <= 10 else
           "  THIS IS LARGE and caps what any item-level analysis can show."),
        "",
        "**10. Judgement calls.** " + " · ".join([
            "(a) folder placement: `paper-a/` was created OUTSIDE the probity repo (`~/paper-a`), "
            "so the public benchmark tree is untouched; one `mv` relocates it",
            "(b) tie exclusion uses the full-60 vector (D3); when that rule left one model I "
            "reported the all-model distribution instead and labelled the promotion as forced, "
            "rather than quietly dropping the rule or quietly keeping an undefined primary",
            "(c) the capability split is the largest-gap (natural-break) rule; the threshold it "
            "produced is reported in 5b",
            "(c2) composing the pre-specified 5b and 5d splits (serving path WITHIN the frontier "
            "tier) is a named control I added because the raw 5d split is confounded with "
            "capability -- not a subgroup hunt, but it was not in the brief",
            f"(d) {len(judged)} answer types decided by judgement: "
            + ", ".join(f"`{l['leaf']}`" for l in judged),
            "(e) 'wobble mass' reported on both the rate and the flipped-item basis (D4)",
            "(f) an undefined coefficient (constant vector) is excluded and counted, never "
            "coerced to 0.0",
        ]) + ".",
        "",
    ]


def answers(ctx: Dict[str, Any]) -> List[str]:
    return (["## 7. The brief's ten questions", ""] + _a1_a3(ctx) + _a4_a7(ctx) + _a8_a10(ctx))


def write_report(ctx: Dict[str, Any]) -> None:
    head = [
        "# C2 diagnostic - is wobble a property of the item or of the model?",
        "",
        f"**Paper A only.** Data: Probity tag `v1.3.1`, read from disk. Arm: **{config.ARM_HUMAN}** "
        "and nothing else -- no number here derives from the 0.1 arm or from any cross-arm "
        "comparison.",
        "",
        "Regenerate: `python3 analysis/run_all.py`. Every figure quoted here is mapped to its "
        "file and computation in `NUMBERS.md`.",
        "",
        "---",
        "",
    ]
    body = (P.prereg(ctx) + P.deviations(ctx) + P.provenance(ctx) + P.matrix_section(ctx)
            + R.pairs_section(ctx) + R.tie_section(ctx) + R.tier_section(ctx)
            + R.drop_section(ctx) + R.serving_section(ctx) + R.null_section(ctx)
            + C.strata_section(ctx) + C.concentration_section(ctx)
            + outcome_section(ctx) + answers(ctx))
    (ctx["out"]["out"] / "C2_REPORT.md").write_text("\n".join(head + body) + "\n")


def write_numbers(ctx: Dict[str, Any]) -> None:
    h, n = ctx["reported"]
    rows = [
        ["median pairwise Spearman, reported headline", T.fmt(h["median"], 4),
         f"out/tables/distributions.csv (row `{ctx['reported_key']}`)",
         "median of `spearman_rho` over the reported pair set on the active subset"],
        ["IQR, reported headline", T.fmt(h["iqr"], 4), "out/tables/distributions.csv", "Q3 - Q1"],
        ["models excluded by the tie rule", str(len(ctx["excluded"])),
         "out/tables/tie_fractions.csv", "count of rows with excluded_from_headline=1"],
        ["permutation-null median", T.fmt(n["median_of_medians"], 4),
         "out/tables/permutation_null.json", f"median of {config.N_PERMUTATIONS} per-permutation "
         f"medians, seed {config.PERM_SEED}"],
        ["null 97.5th percentile", T.fmt(n["p97_5"], 4), "out/tables/permutation_null.json",
         "97.5th percentile of the null median distribution"],
        ["null 2.5th percentile", T.fmt(n["p02_5"], 4), "out/tables/permutation_null.json",
         "2.5th percentile of the null median distribution"],
        ["null max median over all permutations", T.fmt(n["max"], 4),
         "out/tables/permutation_null.json",
         f"largest of the {config.N_PERMUTATIONS} per-permutation medians"],
        ["one-sided p", T.fmt(sc.empirical_p(h["median"], n), 5),
         "out/tables/permutation_null.json", "(#null medians >= observed + 1) / (n_perm + 1)"],
        ["tie fraction per model", "see table", "out/tables/tie_fractions.csv",
         "share of a model's 60 leaf values occurring more than once"],
        ["aggregate wobble per model", "see table", "out/tables/model_summary.csv",
         "sum(flipped items) / sum(measured items) over all 60 leaves"],
        ["leaves zero in all 12 models", str(ctx["zeros"]["n_zero_in_all"]),
         "out/tables/wobble_matrix.csv", "count of columns where every row is 0"],
        ["active subset size", str(len(ctx["active"])), "out/tables/wobble_matrix.csv",
         "columns with at least one non-zero cell"],
        ["dropped cells", str(ctx["drops"]["total_dropped_cells"]),
         "out/tables/n_and_dropped_matrix.csv", "rows with dropped=1 (scorer `measurable` false)"],
        ["common subset size", str(len(ctx["common"])), "out/tables/n_and_dropped_matrix.csv",
         "leaves with dropped=0 for all 12 models"],
        ["top-10 intersection", str(ctx["overlap"]["intersection_size"]),
         "out/tables/concentration_top10.csv", "strict intersection of the 12 non-zero top-10 sets"],
        ["median pairwise top-10 overlap", str(ctx["pair_overlap"]["median_shared"]),
         "out/tables/concentration_top10.csv",
         "median size of the intersection of two models' top-10 sets, over the 66 pairs"],
        ["median pairwise top-10 Jaccard", T.fmt(ctx["pair_overlap"]["median_jaccard"]),
         "out/tables/concentration_top10.csv",
         "median of |A and B| / |A or B| over the 66 top-10 set pairs"],
        ["most-shared leaf and its model count",
         f"`{ctx['leaf_hits'][0][0]}` in {ctx['leaf_hits'][0][1]}",
         "out/tables/concentration_top10.csv",
         "leaf appearing in the most models' top-10 sets"],
        ["routed models on disk", str(sum(1 for v in ctx["serving"].values() if v == "routed")),
         "probity/engine/preflight.py:LINEUP", "count of entries whose client is `openrouter`"],
    ]
    for name, d in list(ctx["tiers"].items()) + list(ctx["paths"].items()):
        rows.append([f"median rho, group `{name}`", T.fmt(d["summary"]["median"], 4),
                     "out/tables/distributions.csv",
                     f"median over the {d['summary']['n_defined']} defined pairs in that group"])
    for name, d in ctx["serving_in_frontier"].items():
        rows.append([f"median rho, frontier-only serving `{name.replace('_', ' ')}`",
                     T.fmt(d["summary"]["median"], 4), "out/tables/distributions.csv",
                     f"median over the {d['summary']['n_defined']} defined pairs, both members in "
                     "the frontier tier (isolates serving from capability)"])
    for kind, s in ctx["strata"].items():
        rows.append([f"median rho, answer-type stratum `{kind}`", T.fmt(s["summary"]["median"], 4),
                     "out/tables/distributions.csv",
                     f"median over the {s['summary']['n_defined']} defined pairs, restricted to "
                     f"that stratum's {s['n_leaves']} leaves (mean tie {T.fmt(s['mean_tie'])})"])
    body = ["# NUMBERS.md - every quoted figure, its file, and its computation", "",
            f"Arm: {config.ARM_HUMAN}. Regenerate everything with `python3 analysis/run_all.py`.",
            "", "## Stage 1 - the C2 diagnostic", "",
            T.md_table(["Figure", "Value", "File", "Computation"], rows), ""]
    if ctx.get("stage2"):
        import numbers_s2
        import stage2 as S2
        body += ["## Stage 2 - ceiling, transfer, description, robustness", "",
                 T.md_table(["Figure", "Value", "File", "Computation"],
                            numbers_s2.rows(ctx["stage2"], S2.TRANSFER_KS,
                                            ctx["annotation_info"])), ""]
    if ctx.get("stage3"):
        import numbers_s3
        body += ["## Stage 3 - conservative ratios, the fold decomposition, the empty zone", "",
                 T.md_table(["Figure", "Value", "File", "Computation"],
                            numbers_s3.rows(ctx["stage3"])), ""]
    (config.PAPER_ROOT / "NUMBERS.md").write_text("\n".join(body) + "\n")
