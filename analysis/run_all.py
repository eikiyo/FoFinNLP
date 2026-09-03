"""
Location: paper-a/analysis/run_all.py
Purpose: THE entry point (brief 8.5). Regenerates every table, figure and document deterministically
         from the frozen temperature-0.7 arm on disk. No manual steps, no hand-typed numbers.
         Usage:  python3 analysis/run_all.py      (optionally PROBITY_ROOT=/path)
Functions: build_context(), main()
Calls: matrix, answer_space, analyses, stats_core, concentration, decision, figures, report
Imports: json, sys, pathlib, numpy
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import agreement              # noqa: E402
import analyses as an          # noqa: E402
import answer_space            # noqa: E402
import concentration as conc   # noqa: E402
import config                  # noqa: E402
import decision                # noqa: E402
import figures                 # noqa: E402
import figures_s2              # noqa: E402
import figures_s3              # noqa: E402
import matrix                  # noqa: E402
import oracle_audit            # noqa: E402
import report                  # noqa: E402
import report_s2_robust        # noqa: E402
import report_s3_close         # noqa: E402
import report_s3b              # noqa: E402
import stage2                  # noqa: E402
import stage3                  # noqa: E402
import stats_core as sc        # noqa: E402
import triage                  # noqa: E402
import tables_out as T         # noqa: E402


def _dist(models, leaf_names, cells, keep=None):
    ms = keep or models
    rows = sc.all_pairs(ms, an.vectors(ms, leaf_names, cells))
    return rows, sc.summarise(rows)



def _load_leaf_task(leaf):
    """One leaf's task record via the benchmark's own loader. Imported inside the function:
    engine/ only joins sys.path once build_context has run."""
    root = config.probity_root()
    for sub in ("engine", "results"):
        if str(root / sub) not in sys.path:
            sys.path.insert(0, str(root / sub))
    import runner
    return runner._load_task(root / leaf["rel"])

def build_context() -> dict:
    out = config.out_paths()
    models, leaves, cells = matrix.load_cells()
    names = [l["leaf"] for l in leaves]
    ctx = {"models": models, "leaves": leaves, "cells": cells, "names": names, "out": out}
    ctx["provenance"] = matrix.arm_provenance(models, leaves)
    ctx["files"] = matrix.write_matrices(models, leaves, cells, out["tables"])
    ctx["answer_types_path"], ctx["answer_type"] = answer_space.write_answer_types(
        leaves, out["out"])

    ctx["active"] = an.active_subset(models, names, cells)
    ctx["common"] = an.common_subset(models, names, cells)
    ctx["agg_wobble"] = an.aggregate_wobble(models, names, cells)
    ctx["split"] = an.capability_split(ctx["agg_wobble"])
    ctx["drops"] = an.drop_accounting(models, leaves, cells)
    ctx["serving"] = config.serving_paths()
    ctx["zeros"] = conc.zero_leaf_counts(models, names, cells)

    vfull = an.vectors(models, names, cells)
    vact = an.vectors(models, ctx["active"], cells)
    ctx["ties"] = an.tie_table(models, vfull, vact)
    ctx["excluded"] = [r["model"] for r in ctx["ties"] if r["excluded"]]
    ctx["headline_models"] = [m for m in models if m not in ctx["excluded"]]

    mat_act = an.complete_matrix(models, ctx["active"], cells)
    ctx["selftest"] = sc.selftest(mat_act, models)

    for key, subset in (("full", names), ("active", ctx["active"]), ("common", ctx["common"])):
        rows, summ = _dist(models, subset, cells)
        ctx[f"rows_{key}"], ctx[f"all_{key}"] = rows, summ
    ctx["rows_headline"], ctx["headline_active"] = _dist(
        models, ctx["active"], cells, keep=ctx["headline_models"])
    ctx["rows_headline_full"], ctx["headline_full"] = _dist(
        models, names, cells, keep=ctx["headline_models"])

    ctx["nulls"] = _nulls(ctx, cells)
    ctx["tiers"] = _grouped(ctx, {m: ("low" if m in ctx["split"]["low"] else "frontier")
                                  for m in models}, "tier")
    ctx["paths"] = _grouped(ctx, ctx["serving"], "serving")
    ctx["strata"] = an.strata_pairs(models, ctx["active"], cells, ctx["answer_type"])
    ctx["strata_nulls"] = _strata_nulls(ctx, cells)
    ctx["serving_in_frontier"] = _serving_in_frontier(ctx)
    ctx["conc"] = conc.concentration_rows(models, names, cells)
    ctx["overlap"] = conc.overlap(ctx["conc"])
    ctx["pair_overlap"] = conc.pairwise_overlap(ctx["conc"])
    ctx["leaf_hits"] = conc.leaf_hit_counts(ctx["conc"])
    _resolve_headline(ctx)
    ctx["decision"] = decision.decide(
        ctx["reported"],
        {k: (ctx[k], ctx["nulls"][k]) for k in ("all_full", "all_active", "all_common")},
        {name: (d["summary"], d["null"]) for name, d in ctx["tiers"].items()},
        ctx["primary_computable"],
        {k: (s["summary"], ctx["strata_nulls"][k]) for k, s in ctx["strata"].items()
         if ctx["strata_nulls"].get(k)})
    return ctx


def _resolve_headline(ctx: dict) -> None:
    """
    Which distribution the outcome is read off, and WHY.

    The pre-registered primary is the tie-filtered set. If the tie rule leaves fewer than two
    models it produces ZERO pairs and the primary is undefined -- not null, undefined. In that
    case the all-model active-subset distribution is reported instead, and the promotion is
    recorded as FORCED BY THE RULE COLLAPSING, never as a choice made after seeing which looked
    better (brief section 7: no promoting a secondary because it reads well). The substitute is
    defensible on its own terms because its permutation null is built from the SAME tie structure,
    which is the principled version of the control the exclusion rule approximates.
    """
    ctx["primary_computable"] = len(ctx["headline_models"]) >= 2
    if ctx["primary_computable"]:
        ctx["reported_key"], ctx["promotion_note"] = "headline_active", ""
    else:
        ctx["reported_key"] = "all_active"
        ctx["promotion_note"] = (
            f"The pre-registered primary is UNDEFINED on this data: the tie rule "
            f"(> {config.TIE_THRESHOLD}) excludes {len(ctx['excluded'])} of "
            f"{len(ctx['models'])} models, leaving {len(ctx['headline_models'])} and therefore "
            f"{ctx['headline_active']['n_pairs']} pairs. The reported headline is the SAME test "
            f"on all 12 models over the same active subset, scored against a null carrying this "
            f"data's exact tie structure. This substitution is forced by the rule collapsing, "
            f"not chosen after inspecting results; the excluded-set result is reported beside it.")
    ctx["reported"] = (ctx[ctx["reported_key"]], ctx["nulls"][ctx["reported_key"]])
    ctx["reported_rows"] = (ctx["rows_headline"] if ctx["primary_computable"]
                            else ctx["rows_active"])


def _nulls(ctx, cells) -> dict:
    """One permutation run per (model set x leaf subset); every pair-subset verdict is scored
    against a null built from the SAME models and the SAME leaves, never a borrowed one."""
    models, out = ctx["models"], {}
    idx = sc.pair_index(models)
    runs = {}
    for key, subset in (("full", ctx["names"]), ("active", ctx["active"]),
                        ("common", ctx["common"])):
        mat = an.complete_matrix(models, subset, cells)
        runs[key] = sc.permutation_rhos(mat, config.N_PERMUTATIONS, config.PERM_SEED)
        out[f"all_{key}"] = sc.null_summary(runs[key])
    hcols = [idx[(a, b)] for (a, b) in idx
             if a in ctx["headline_models"] and b in ctx["headline_models"]]
    out["headline_active"] = sc.null_summary(runs["active"], hcols)
    out["headline_full"] = sc.null_summary(runs["full"], hcols)
    ctx["_perm_runs"], ctx["_pair_idx"] = runs, idx
    return out


def _grouped(ctx, group: dict, kind: str) -> dict:
    """Within-group and cross-group pair distributions on the active subset, each with its own
    null built from the same permutation run restricted to the same columns."""
    idx, runs = ctx["_pair_idx"], ctx["_perm_runs"]["active"]
    res = {}
    for name in sorted(set(group.values())) + (["ACROSS"] if kind == "tier" else ["DIFFERENT"]):
        if name in ("ACROSS", "DIFFERENT"):
            keep = [(a, b) for (a, b) in idx if group[a] != group[b]]
        else:
            keep = [(a, b) for (a, b) in idx if group[a] == name and group[b] == name]
        rows = [r for r in ctx["rows_active"]
                if (r["model_a"], r["model_b"]) in set(keep)]
        res[name] = {"rows": rows, "summary": sc.summarise(rows),
                     "null": sc.null_summary(runs, [idx[p] for p in keep]),
                     "members": sorted({m for m, g in group.items() if g == name})}
        res[name]["p"] = sc.empirical_p(res[name]["summary"]["median"], res[name]["null"])
    return res


def _serving_in_frontier(ctx) -> dict:
    """5d with the capability confound removed: same-path vs different-path among frontier
    models only. Both splits are pre-specified in the brief, so composing them is a named
    control, not a subgroup hunt."""
    tier = {m: ("low" if m in ctx["split"]["low"] else "frontier") for m in ctx["models"]}
    groups = an.serving_within_tier(ctx["rows_active"], ctx["serving"], tier, "frontier")
    idx, runs = ctx["_pair_idx"], ctx["_perm_runs"]["active"]
    out = {}
    for name, rows in groups.items():
        cols = [idx[(r["model_a"], r["model_b"])] for r in rows]
        null = sc.null_summary(runs, cols)
        summ = sc.summarise(rows)
        out[name] = {"rows": rows, "summary": summ, "null": null,
                     "p": sc.empirical_p(summ["median"], null)}
    return out


def _strata_nulls(ctx, cells) -> dict:
    out = {}
    for kind, s in ctx["strata"].items():
        if len(s["leaves"]) < 3:
            out[kind] = None
            continue
        mat = an.complete_matrix(ctx["models"], s["leaves"], cells)
        rhos = sc.permutation_rhos(mat, config.N_PERMUTATIONS, config.PERM_SEED)
        null = sc.null_summary(rhos)
        out[kind] = dict(null, p=sc.empirical_p(s["summary"]["median"], null))
    return out


def main() -> None:
    ctx = build_context()
    out = ctx["out"]
    t = out["tables"]
    T.write_pairs(ctx["rows_full"], t / "pairs_full60.csv", "full_60_leaves")
    T.write_pairs(ctx["rows_active"], t / "pairs_active.csv", "active_subset")
    T.write_pairs(ctx["rows_common"], t / "pairs_common.csv", "common_subset")
    T.write_pairs(ctx["rows_headline"], t / "pairs_headline_active.csv", "headline_active")
    T.write_ties(ctx["ties"], t / "tie_fractions.csv")
    T.write_concentration(ctx["conc"], t / "concentration_top10.csv")
    T.write_matrix_summary(ctx["models"], ctx["leaves"], ctx["cells"], ctx["agg_wobble"],
                           t / "model_summary.csv")
    T.write_distributions(report.named_distributions(ctx), t / "distributions.csv")
    (t / "permutation_null.json").write_text(json.dumps(
        {k: {kk: vv for kk, vv in v.items() if kk not in ("medians", "pooled_sample")}
         for k, v in ctx["nulls"].items()}, indent=1))

    f = out["figures"]
    figures.rho_heatmap(ctx["models"], ctx["rows_active"], f / "rho_heatmap.png",
                        f"Pairwise Spearman rho over the active subset "
                        f"({len(ctx['active'])} leaves) - {config.ARM_HUMAN}", ctx["excluded"])
    figures.rho_vs_null([r["rho"] for r in ctx["reported_rows"] if r["rho"] is not None],
                        ctx["reported"][1], f / "rho_vs_null.png",
                        f"REPORTED HEADLINE ({ctx['reported_key']}) vs its tie-preserving "
                        f"permutation null")
    figures.wobble_heatmap(ctx["models"], ctx["names"], ctx["cells"],
                           f / "wobble_heatmap.png",
                           f"Wobble rate by model x leaf - {config.ARM_HUMAN} "
                           f"(green = dropped/absent)")
    report.write_report(ctx)

    # ---- STAGE 2 -------------------------------------------------------------------
    s2 = stage2.compute(ctx)
    ctx["stage2"] = s2
    stage2.write_tables(s2, t)
    ann = stage2.write_annotation(s2, out["out"])
    ctx["annotation_info"] = ann
    report_s2_robust.write(s2, ann, stage2.annotation.SAMPLE_FRACTION, out["out"])
    figures_s2.all_figures(s2, stage2.TRANSFER_KS, f)

    # ---- STAGE 3 -------------------------------------------------------------------
    s3 = stage3.compute(s2)
    ctx["stage3"] = s3
    stage3.write_tables(s3, t)
    d = out["out"] / "annotation"
    s3["blind"] = agreement.write_blind_pack(
        stage2.annotation.stratified_sample(ctx["leaves"], ctx["answer_type"]),
        ctx["answer_type"], d)
    s3["agreement"] = agreement.score_sheet(
        d / "blind_pack_filled.csv",
        stage2.annotation.stratified_sample(ctx["leaves"], ctx["answer_type"]),
        ctx["answer_type"], {l["leaf"]: l.get("type", "string") for l in ctx["leaves"]})
    agreement.write_result(s3["agreement"], d)
    _samp = stage2.annotation.stratified_sample(ctx["leaves"], ctx["answer_type"])
    # Reading material and declared caveats regenerate with everything else; left as one-offs they
    # would drift from the pack the moment the sample or seed changed.
    _tasks = {l["leaf"]: _load_leaf_task(l) for l in _samp}
    _cidx = oracle_audit.corpus_index()
    s3["reading_pack"] = str(stage2.annotation.write_reading_pack(
        _samp, d, _cidx["window"], _cidx["url"], _tasks))
    s3["primed_items"] = agreement.primed_items(_samp, _tasks, d)
    _views = triage.collect_views(ctx["models"], _samp)
    s3["triage"] = triage.write_worklist(
        triage.score_suspicion(_views, ctx["models"], _samp), d)
    ao = oracle_audit.audit_all()
    s3["oracle_audit"] = oracle_audit.summarise(ao)
    oracle_audit.write_report(ao, s3["oracle_audit"], d)
    report_s3b.write(s3, report_s3_close.closing(s3, s3["agreement"]), out["out"])
    figures_s3.all_figures(s3, f)

    report.write_numbers(ctx)
    gen = [out["out"] / "C2_REPORT.md", out["out"] / "answer_types.md",
           out["out"] / "STAGE2_REPORT.md", out["out"] / "annotation" / "PROTOCOL.md",
           out["out"] / "STAGE3_REPORT.md", config.PAPER_ROOT / "NUMBERS.md"]
    # The figure gate is scoped to the two documents that NARRATE OUR RESULTS. It is deliberately
    # NOT pointed at novelty_audit.md / PREREG_2a.md / SCOPE.md / ADJUDICATION.md: those quote
    # other papers' figures, arXiv identifiers and page budgets, none of which our tables can back.
    # Pointing it there produced a page of false reds (`2508.03080` reads as a decimal), and a gate
    # that cries wolf on its own reference list gets switched off. Those four are cross-checked by
    # hand instead, and the report says so rather than implying machine coverage that is not there.
    hand = [p for p in (config.PAPER_ROOT / "FINDINGS.md", config.PAPER_ROOT / "README.md")
            if p.exists()]
    print(f"\ntable check:  {T.check_markdown_tables(gen + hand)}")
    print(f"figure check: {T.check_quoted_figures(hand, gen)}")
    print(f"OUTCOME: {ctx['decision']['row_name']}")
    print(f"report: {out['out'] / 'C2_REPORT.md'}")


if __name__ == "__main__":
    main()
