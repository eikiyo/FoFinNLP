"""
Location: paper-a/analysis/report_prereg.py
Purpose: The parts of C2_REPORT.md that must come BEFORE any result (brief 7): the pre-registered
         analysis, the declared deviations, and the provenance/coverage evidence that the arm being
         read really is the published temperature-0.7 one.
Functions: prereg(), deviations(), provenance(), matrix_section()
Calls: none (pure over the context dict)
Imports: typing, config, decision, tables_out
"""

from typing import Any, Dict, List

import config
import decision
import tables_out as T


def prereg(ctx: Dict[str, Any]) -> List[str]:
    return [
        "## 1. Pre-registered analysis (written before any coefficient was computed)",
        "",
        f"**Arm:** `{config.ARM_HUMAN}` and nothing else. Inside Probity the published 0.7 sweep "
        "is the LEGACY, UNSUFFIXED namespace (`leaves/*/scored.json`), represented internally by "
        "the sentinel `None`. The literal float `0.7` selects `scored_t07.json`, a different "
        "2-model Kaggle cross-machine control, so the arm is declared once in `analysis/config.py` "
        "and a fail-closed guard rejects any opened path containing `_t01` / `t07`.",
        "",
        "**Unit.** The leaf, not the document category. 60 leaves, 12 models, one wobble rate per "
        "cell. Categories are a descriptive layer, never the statistical unit.",
        "",
        "**Primary test (one, named in advance).** The MEDIAN pairwise Spearman rho on the ACTIVE "
        "SUBSET (leaves with non-zero wobble in at least one model), over the models not excluded "
        "by the tie rule, compared against a permutation null built from the same models, the same "
        "leaves and the same tie structure. Everything else in this report is a named secondary or "
        "a control and is labelled as such.",
        "",
        "**Definitions, fixed in advance.**",
        "",
        T.md_table(["Quantity", "Definition"], [
            ["wobble rate of a cell", "flipped items / measured items, where an item is measured "
             "iff it recorded at least one valid run"],
            ["dropped cell", "the benchmark's own `reliability.measurable == False`, i.e. "
             "`parse_failures/runs > 0.30` or fewer than 2 valid runs (`engine/scorer.py`)"],
            ["tie fraction", "share of a model's leaf values that occur more than once in that "
             "same vector"],
            ["active subset", "leaves with non-zero wobble in >= 1 model"],
            ["common subset", "leaves retained (not dropped, not absent) for all 12 models"],
            ["capability split", "sort models by aggregate 0.7 wobble, cut at the LARGEST gap "
             "between consecutive values"],
            ["permutation null", f"{config.N_PERMUTATIONS} permutations, seed "
             f"`{config.PERM_SEED}`; each model's observed values are permuted among its own "
             "positions, preserving its exact tie structure and n"],
        ]),
        "",
        "**Pre-registered thresholds.** tie exclusion > "
        f"`{config.TIE_THRESHOLD}` · \"tight\" IQR <= `{decision.TIGHT_IQR}` · "
        f"\"indistinguishable from the null\" within `{decision.NEAR_NULL_MARGIN}` · a stratum "
        f"needs >= `{decision.MIN_PAIRS_FOR_DIST}` defined pairs to be called a distribution.",
        "",
    ]


def deviations(ctx: Dict[str, Any]) -> List[str]:
    return [
        "### 1.1 Declared deviations and disclosures",
        "",
        T.md_table(["#", "What", "Why"], [
            ["D1", "The pre-registration was authored after inspecting the matrix's SHAPE "
                   "(cell coverage, per-model zero counts, per-model aggregate wobble) but before "
                   "computing any correlation coefficient, any subset distribution or any null.",
                   "Honest disclosure. Those shape facts are what made the tie control's design "
                   "concrete; none of them is a coefficient."],
            ["D2", "The brief says six of the twelve models are served through a routing layer. "
                   f"On disk it is {sum(1 for v in ctx['serving'].values() if v == 'routed')}.",
                   "`engine/preflight.py:LINEUP` is the repo's declared label -> client map and "
                   "is used as written. The disagreement is reported, not silently resolved."],
            ["D3", "Tie-based exclusion for the headline uses each model's tie fraction on its "
                   "FULL 60-leaf vector, as the brief words it (\"the model's leaf vector\"). The "
                   "active-subset tie fractions are reported beside it and the headline is "
                   "re-run under active-subset exclusion as a named sensitivity.",
                   "The literal reading is the stricter one; the alternative is shown so the "
                   "choice is visible rather than load-bearing and hidden."],
            ["D4", "Top-10 concentration is reported on both the rate mass and the flipped-item "
                   "mass.", "Both derive from the two mandated matrices; 'mass' is ambiguous "
                            "between them, so neither is hidden."],
            ["D5", "Six leaves' answer types are judgement calls (declared type `date` or "
                   "`string`); each is justified in `answer_types.md` and re-listed in Q10.",
                   "The brief permits judgement where mechanical classification is impossible."],
        ]),
        "",
    ]


def provenance(ctx: Dict[str, Any]) -> List[str]:
    p, d = ctx["provenance"], ctx["drops"]
    temps = ", ".join(f"`{k}` x{v}" for k, v in sorted(p["temperatures_seen"].items()))
    runs = ", ".join(f"`{k}` x{v}" for k, v in sorted(p["n_runs_declared"].items()))
    partial = sorted((m, c) for m, c in p["per_model"].items() if c < len(ctx["leaves"]))
    return [
        "## 2. Provenance and coverage (the scope rule, verified rather than asserted)",
        "",
        f"- Every manifest written by this arm was read: **{p['manifests_found']} found**, "
        f"{p['manifests_absent']} cells have none. Full coverage on "
        f"{sum(1 for c in p['per_model'].values() if c == len(ctx['leaves']))} of 12 models; "
        "partial on " + (", ".join(f"`{m}` ({c}/{len(ctx['leaves'])})" for m, c in partial)
                         or "none")
        + " -- the two earliest-run labels, from before the manifest step existed. That is a "
          "documentation gap, not a provenance gap: their run artefacts sit in the same "
          "unsuffixed namespace, which is what the arm is defined by.",
        f"- Temperatures those manifests state: {temps}. n_runs they state: {runs}.",
        f"- Cells: **{d['n_cells']}** (12 models x 60 leaves). Absent: "
        f"{sum(v['absent'] for v in d['per_model'].values())}. "
        f"Dropped by the >30% unparseable rule: **{d['total_dropped_cells']}**.",
        f"- Instrument check, run before any number was trusted: {ctx['selftest']}.",
        "",
        "> The manifest check is a POSITIVE control, not a formality: it could have detected the "
        "wrong arm (it reports the temperatures it actually saw, not a boolean), and 0.1 would "
        "have shown up in that list.",
        "",
    ]


def matrix_section(ctx: Dict[str, Any]) -> List[str]:
    rows = []
    for m in ctx["models"]:
        cs = [ctx["cells"][m][n] for n in ctx["names"]]
        rows.append([f"`{m}`", ctx["serving"][m], T.pct(ctx["agg_wobble"][m], 2),
                     str(sum(1 for c in cs if (c["wobble"] or 0) == 0)),
                     str(sum(c["n_items"] for c in cs)),
                     str(sum(c["flipped"] for c in cs)),
                     str(sum(1 for c in cs if c["dropped"]))])
    return [
        "## 3. The wobble matrix (brief 4a)",
        "",
        "Files: `out/tables/wobble_matrix.csv` (12 x 60 rates) and "
        "`out/tables/n_and_dropped_matrix.csv` (per cell: n_items, n_instances, n_runs recorded, "
        "flipped, wobble, dropped, absent, parse-failure rate). Every number below derives from "
        "these two and nothing else.",
        "",
        T.md_table(["Model", "Serving", "Aggregate wobble", "Leaves at exactly 0", "Measured items",
                    "Flipped items", "Dropped cells"], rows),
        "",
        f"- Leaves with zero wobble in **all 12** models: **{ctx['zeros']['n_zero_in_all']}** "
        f"({', '.join('`' + n + '`' for n in ctx['zeros']['zero_in_all_models']) or 'none'}).",
        f"- Leaves with non-zero wobble in at least one model (**the active subset**): "
        f"**{ctx['zeros']['n_nonzero_in_at_least_one']}** of {ctx['zeros']['n_leaves']}.",
        "",
    ]
