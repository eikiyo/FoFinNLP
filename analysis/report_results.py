"""
Location: paper-a/analysis/report_results.py
Purpose: The results half of C2_REPORT.md -- the pairwise distributions, every section-5 control,
         and the tie-immune concentration route. Rendered from the same dicts the CSVs are written
         from, so a quoted number and its table cannot disagree.
Functions: pairs_section(), tie_section(), tier_section(), drop_section(), serving_section(),
           null_section()   (5f + 4c live in report_controls.py)
Calls: none (pure over the context dict)
Imports: typing, config, decision, stats_core, tables_out
"""

from typing import Any, Dict, List

import config
import decision
import stats_core as sc
import tables_out as T


def _dist_rows(ctx: Dict[str, Any]) -> List[List[str]]:
    n, rep = ctx["nulls"], ctx["reported_key"]
    rows = []
    for label, key, note in (
        ("pre-registered primary - tie-filtered models, active subset", "headline_active",
         "the one pre-registered test"),
        ("tie-filtered models, full 60 leaves", "headline_full", "secondary"),
        ("all 12 models, active subset", "all_active", "control"),
        ("all 12 models, full 60 leaves", "all_full", "control"),
        ("all 12 models, common subset", "all_common", "control (5c)"),
    ):
        s = ctx[key]
        p = sc.empirical_p(s["median"], n[key]) if key in n else None
        extra = (f"null median {T.fmt(n[key]['median_of_medians'])}, null 97.5th "
                 f"{T.fmt(n[key]['p97_5'])}, p={T.fmt(p, 4) if p else '—'} · {note}")
        rows.append(T.md_dist_row(("**REPORTED** " if key == rep else "") + label, s, extra))
    return rows


def pairs_section(ctx: Dict[str, Any]) -> List[str]:
    hm = ctx["headline_models"]
    lines = [
        "## 4. Pairwise rank correlation (brief 4b)",
        "",
        f"All {len(ctx['rows_full'])} unordered model pairs. Per-pair rho, tau-b, n and both sides' "
        "tie fractions are in `out/tables/pairs_*.csv` -- every coefficient, including the "
        "inconvenient ones. Distribution summaries (`out/tables/distributions.csv`):",
        "",
        T.md_table(T.DIST_HEADER, _dist_rows(ctx)),
        "",
        f"Model set surviving the tie rule: **{len(hm)} of 12** "
        f"({', '.join('`' + m + '`' for m in hm) or 'none'}), giving "
        f"{ctx['headline_active']['n_pairs']} pairs.",
        "",
    ]
    if ctx["promotion_note"]:
        lines += [f"> **Deviation, forced.** {ctx['promotion_note']}", ""]
    return lines + [
        "Figures: `out/figures/rho_heatmap.png` (models x models), "
        "`out/figures/rho_vs_null.png` (the reported headline vs its null), "
        "`out/figures/wobble_heatmap.png` (models x leaves).",
        "",
    ]


def tie_section(ctx: Dict[str, Any]) -> List[str]:
    rows = [[f"`{r['model']}`", T.fmt(r["tie_full"], 3), T.pct(r["zero_full"]),
             str(r["n_distinct_full"]), T.fmt(r["tie_active"], 3), T.pct(r["zero_active"]),
             "**EXCLUDED**" if r["excluded"] else "kept"] for r in ctx["ties"]]
    alt = [r["model"] for r in ctx["ties"]
           if r["tie_active"] is not None and r["tie_active"] > config.TIE_THRESHOLD]
    return [
        "## 5a. Tie mass -- the control most likely to decide this",
        "",
        T.md_table(["Model", "Tie fraction (60)", "Zeros (60)", "Distinct values (60)",
                    "Tie fraction (active)", "Zeros (active)",
                    f"Headline (> {config.TIE_THRESHOLD})"], rows),
        "",
        f"Sensitivity (D3): excluding on the ACTIVE-subset tie fraction instead would exclude "
        f"{len(alt)} models ({', '.join('`' + m + '`' for m in alt) or 'none'}).",
        "",
    ]


def tier_section(ctx: Dict[str, Any]) -> List[str]:
    sp = ctx["split"]
    order = " · ".join(f"`{m}` {T.pct(v, 2)}" for m, v in sp["sorted"])
    rows = []
    for name, d in ctx["tiers"].items():
        s = d["summary"]
        rows.append([name, str(len(d["members"])) if name != "ACROSS" else "—",
                     str(s["n_pairs"]), str(s["n_defined"]), T.fmt(s["median"]), T.fmt(s["iqr"]),
                     T.fmt(d["null"]["median_of_medians"]), T.fmt(d["null"]["p97_5"]),
                     T.fmt(d["p"], 4),
                     "too few pairs for a distribution"
                     if s["n_defined"] < decision.MIN_PAIRS_FOR_DIST else ""])
    return [
        "## 5b. Capability stratification",
        "",
        f"Split rule: largest gap between consecutive aggregate-wobble values. Sorted: {order}. "
        f"Largest gap = **{100 * sp['largest_gap']:.2f} points**, so the threshold is "
        f"**{T.pct(sp['threshold'], 2)}**: low = "
        f"{', '.join('`' + m + '`' for m in sp['low'])}; frontier = the other "
        f"{len(sp['frontier'])}.",
        "",
        T.md_table(["Group", "members", "pairs", "defined", "median rho", "IQR", "null median",
                    "null 97.5", "p", "note"], rows),
        "",
        "",
    ]


def drop_section(ctx: Dict[str, Any]) -> List[str]:
    d = ctx["drops"]
    vac = d["total_dropped_cells"] == 0
    lines = [
        "## 5c. Dropped-leaf accounting",
        "",
        f"- Dropped cells (>30% unparseable): **{d['total_dropped_cells']}** of {d['n_cells']}. "
        f"Absent cells: {sum(v['absent'] for v in d['per_model'].values())}.",
        f"- Per family: " + (", ".join(f"{k} {v}" for k, v in sorted(d["per_family"].items()))
                             or "none"),
        f"- Common subset (leaves retained for all 12 models): **{len(ctx['common'])}** of "
        f"{len(ctx['names'])}.",
        "",
    ]
    if vac:
        lines += [
            "> **This control is VACUOUS on this arm, not passed.** At temperature 0.7 the "
            "benchmark drops nothing, so the common subset is identical to the full set by "
            "construction and the re-run cannot disagree with the full-intersection version. "
            "It is reported because a control that could not fire must be named as such rather "
            "than counted as evidence. (Parse failures exist -- they just never reach the 30% "
            "gate on any cell; per-cell rates are in `n_and_dropped_matrix.csv`.)",
            "",
        ]
    return lines


def serving_section(ctx: Dict[str, Any]) -> List[str]:
    counts: Dict[str, int] = {}
    for v in ctx["serving"].values():
        counts[v] = counts.get(v, 0) + 1
    rows = []
    for name, d in ctx["paths"].items():
        s = d["summary"]
        rows.append([name, ", ".join(f"`{m}`" for m in d["members"]) or "—", str(s["n_pairs"]),
                     str(s["n_defined"]), T.fmt(s["median"]), T.fmt(s["iqr"]),
                     T.fmt(d["null"]["median_of_medians"]), T.fmt(d["p"], 4)])
    fr = ctx["serving_in_frontier"]
    frows = [[k.replace("_", " "), str(v["summary"]["n_pairs"]), str(v["summary"]["n_defined"]),
              T.fmt(v["summary"]["median"]), T.fmt(v["summary"]["iqr"]),
              T.fmt(v["null"]["median_of_medians"]), T.fmt(v["p"], 4)] for k, v in fr.items()]
    return [
        "## 5d. Serving-layer confound",
        "",
        "Serving path per model is parsed from `engine/preflight.py:LINEUP`, the repo's declared "
        "label -> client map -- not inferred from the `-or` filename suffix. Counts: "
        + " · ".join(f"**{k}** {v}" for k, v in sorted(counts.items())) + ". "
        f"(The brief says six routed; on disk it is {counts.get('routed', 0)} -- deviation D2.)",
        "",
        T.md_table(["Group", "members", "pairs", "defined", "median rho", "IQR", "null median",
                    "p"], rows),
        "",
        "> **The raw split above is confounded and must not be read on its own.** Every routed and "
        "every direct model in this lineup sits in the FRONTIER tier, and both local models sit in "
        "the LOW tier. So `DIFFERENT` is where all 20 low-vs-frontier pairs live, and its lower "
        "median is mostly the capability effect from 5b re-appearing, not a serving effect. The "
        "`local` row is a single pair -- and it is the same base model at two quantizations, so it "
        "is closer to a self-correlation than to cross-model agreement.",
        "",
        "Isolating serving from capability, WITHIN the frontier tier only:",
        "",
        T.md_table(["Frontier-only group", "pairs", "defined", "median rho", "IQR", "null median",
                    "p"], frows),
        "",
    ]


def null_section(ctx: Dict[str, Any]) -> List[str]:
    obs, n = ctx["reported"][0]["median"], ctx["reported"][1]
    p = sc.empirical_p(obs, n)
    return [
        "## 5e. Permutation null (what turns a number into a claim)",
        "",
        f"{config.N_PERMUTATIONS} permutations, seed `{config.PERM_SEED}`, on the same models and "
        "the same leaves as the reported headline. Each model's observed values are permuted among "
        "its OWN positions, so the null carries this data's exact tie structure and exact n; only "
        "the pairing between models is destroyed.",
        "",
        "> This is why the tie problem does not invalidate the result: heavy tie mass depresses "
        "Spearman in the OBSERVED data and in the NULL by exactly the same mechanism, because the "
        "null is built by permuting the same values. Ties cost power, they do not manufacture the "
        "gap between the two.",
        "",
        T.md_table(["Quantity", "Value"], [
            ["observed median rho (reported headline)", T.fmt(obs, 4)],
            ["null median of medians", T.fmt(n["median_of_medians"], 4)],
            ["null 95% envelope of the median", f"[{T.fmt(n['p02_5'], 4)}, "
                                                f"{T.fmt(n['p97_5'], 4)}]"],
            ["null max median over all permutations", T.fmt(n["max"], 4)],
            ["one-sided permutation p", T.fmt(p, 5) if p else "—"],
        ]),
        "",
    ]
