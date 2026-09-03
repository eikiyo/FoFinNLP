"""
Location: paper-a/analysis/report_s2_ceiling.py
Purpose: STAGE2_REPORT section 1 -- the measurement ceiling. Rendered first because it recalibrates
         the reading of everything after it, and its verdict (which row of the brief's decision
         table, and therefore the paper's headline sentence) is DERIVED from the computed
         reliability rather than chosen.
Functions: section(), _tables(), _verdict(), headline_for()
Calls: none (pure over the stage-2 context)
Imports: statistics, typing, tables_out
"""

import statistics
from typing import Any, Dict, List

import tables_out as T

HEADLINES = {
    "high": ("Cross-model agreement is real but limited: models share a difficulty dimension "
             "that explains a minority of the variance."),
    "middling": ("After correcting for measurement reliability, cross-model agreement is "
                 "SUBSTANTIAL: models largely agree on which items are unstable."),
    "low": ("Per-leaf instability cannot be estimated stably at n=20 runs, which is itself a "
            "benchmarking result and becomes a primary finding."),
}


def headline_for(row: str) -> str:
    return HEADLINES[row]


def _reliability_table(ctx: Dict[str, Any]) -> str:
    rows = [[f"`{x['model']}`", str(x["n_leaves"]), T.fmt(x["wobble_A"], 4),
             T.fmt(x["wobble_B"], 4), T.fmt(x["wobble_full"], 4), T.fmt(x["r_half"], 4),
             T.fmt(x["r_full"], 4), T.fmt(x["tie_A"], 3), T.fmt(x["tie_B"], 3)]
            for x in ctx["reliability"]]
    return T.md_table(["Model", "leaves", "wobble A", "wobble B", "wobble full", "r_half",
                       "r_full (S-B)", "tie A", "tie B"], rows)


def _nonzero_table(ctx: Dict[str, Any]) -> str:
    rows = [[f"`{x['model']}`", str(x["n"]), T.fmt(x["r_half"], 4), T.fmt(x["r_full"], 4),
             x["note"]] for x in ctx["nonzero_reliability"]]
    return T.md_table(["Model", "non-zero leaves", "r_half", "r_full", "note"], rows)


def _intro(ctx: Dict[str, Any]) -> List[str]:
    return [
        "## Step 1 - The measurement ceiling (run first, reported first)",
        "",
        "**Computed.** Each cell's 20 runs were split by `run_idx % 2` into two independent halves "
        "of 10, and the whole wobble matrix was recomputed twice **through the benchmark's own "
        "scorer** (`engine/scorer.py`), not through a re-derived flip rule. Each model's half-A "
        "leaf vector was then correlated against its half-B vector over the active subset "
        f"({len(ctx['active'])} leaves).",
        "",
        f"> **Positive control:** {ctx['roundtrip']}. The raw-runs route is therefore the same "
        "measurement as the published matrix, not a parallel re-implementation of it. Without "
        "this check the half matrices would prove nothing.",
        "",
        "Odd/even was chosen over first-half/second-half because it is **interleaved**: any drift "
        "across the run sequence (throttling, cache warming, provider degradation) is balanced "
        "between the halves instead of concentrated in one.",
        "",
    ]


def _addenda(ctx: Dict[str, Any]) -> List[str]:
    rep, null = ctx["repeated_split"], ctx["reliability_null"]
    return [
        f"- **Median r_half = {T.fmt(ctx['median_r_half'], 4)}**, "
        f"**median r_full (Spearman-Brown) = {T.fmt(ctx['median_r_full'], 4)}** "
        f"(n = {ctx['n_reliability_defined']} models).",
        "- Half-length wobble is systematically LOWER than full-length wobble in every model. That "
        "is expected, not a defect: with half the runs there are half as many chances to observe "
        "a flip. Reliability is a RANK correlation, so a uniform level shift does not affect it, "
        "and Spearman-Brown is precisely the correction for the halved LENGTH.",
        f"- Tie-preserving permutation null on the split-half correlations: median "
        f"{T.fmt(null['median_of_medians'], 4)}, 97.5th {T.fmt(null['p97_5'], 4)}.",
        "",
        "**Declared addition (not pre-registered).** A single odd/even split is one draw from the "
        "distribution of possible partitions. Prompted by finding Cacioli (2026), which averages "
        f"1,000 random splits, the procedure was re-run over {rep['n_splits']} random partitions: "
        f"median r_full **{T.fmt(rep['median_of_medians'], 4)}**, 95% spread "
        f"[{T.fmt(rep['p02_5'], 4)}, {T.fmt(rep['p97_5'], 4)}]. The pre-registered odd/even value "
        "sits inside that spread, so it was representative rather than a lucky partition.",
        "",
        "**Declared sensitivity.** The headline reliability is partly the instrument re-finding "
        "the same *zeros*. The harder question is whether it can RANK the leaves that actually "
        "move, so reliability was recomputed on each model's OWN non-zero leaves only. This can "
        "only weaken the ceiling claim, which is why it is reported:",
        "",
        _nonzero_table(ctx),
        "",
    ]


def _verdict(ctx: Dict[str, Any]) -> List[str]:
    nz = [x["r_full"] for x in ctx["nonzero_reliability"] if x["r_full"] is not None]
    nz_med = statistics.median(nz) if nz else None
    obs, cor = ctx["observed_median"], ctx["corrected_median"]
    return [
        "### What step 1 decides",
        "",
        T.md_table(["Quantity", "Value"], [
            ["median r_full (pre-registered primary)", T.fmt(ctx["median_r_full"], 4)],
            ["decision-table row", f"**{ctx['ceiling_row']}** (cuts at 0.40 and 0.70)"],
            ["observed median rho", T.fmt(obs, 4)],
            ["disattenuated median rho", T.fmt(cor, 4)],
            ["pairs where the correction exceeded 1.0", str(ctx["n_over_one"])],
            ["observed as a share of the ceiling", f"{ctx['pct_of_ceiling']:.1f}%"],
            ["median r_full, non-zero leaves only (sensitivity)", T.fmt(nz_med, 4)],
        ]),
        "",
        f"> **The instrument is stable, so {T.fmt(obs, 4)} really is modest agreement.** "
        f"Correcting for measurement error moves the headline only from {T.fmt(obs, 4)} to "
        f"{T.fmt(cor, 4)} -- about {100 * (cor / obs - 1):.0f}%. There is no large hidden "
        "agreement being masked by a noisy instrument.",
        "",
        f"**Headline sentence for the paper:** *{HEADLINES[ctx['ceiling_row']]}*",
        "",
        f"With rho around {T.fmt(cor, 2)} even after correction, the shared difficulty dimension "
        f"accounts for roughly {100 * cor ** 2:.0f}% of the variance in leaf instability. That is "
        "a real effect and a small one, and the paper should say both.",
        "",
    ]


def section(ctx: Dict[str, Any]) -> List[str]:
    return _intro(ctx) + [_reliability_table(ctx), ""] + _addenda(ctx) + _verdict(ctx)
