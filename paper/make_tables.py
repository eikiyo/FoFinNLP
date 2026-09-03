"""
Location: paper-a/paper/make_tables.py
Purpose: Generate every LaTeX table fragment in paper/tables/ from out/tables/*.csv. No number in
         main.tex is typed by hand; every one arrives through here. Re-running must produce a zero
         byte diff, which is the load-bearing test for a committed generated artifact.
         Usage:  python3 paper/make_tables.py
Functions: table1_lineup(), _lineup_caption(), _transfer_block(), table2_transfer(),
           table3_categories(), table5_audit(), tables(), main()
           (table6_repair lives in table_repair.py, Table 2's claims block in table_claims.py and
           the three appendix exhibits in table_appendix.py; this file is at its line budget and
           each was split out when it passed 300 lines)
Calls: tablekit (all LaTeX primitives), table_appendix, table_claims, table_repair;
       reads out/tables/{clean,all}
Imports: pathlib, sys, tablekit, table_appendix, table_claims, table_repair
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import table_appendix as TA                                      # noqa: E402
import table_claims as TC                                        # noqa: E402
import table_repair as R                                         # noqa: E402
import table_stratified as TS                                    # noqa: E402
import tablekit as K                                             # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "out" / "tables"
DEST = Path(__file__).resolve().parent / "tables"

# Shared with the figures, so they cannot disagree about which configurations are frontier.
SERVING, GAP_AFTER = K.SERVING, K.GAP_AFTER


def table1_lineup() -> str:
    """Twelve configurations ascending by wobble, split by a single midrule at the capability gap.
    The clean-only reading is the headline because the §0 gate fired."""
    rows = sorted(K.read_csv(SRC / "clean" / "model_summary.csv"),
                  key=lambda r: float(r["aggregate_wobble"]))
    cut = next(i for i, r in enumerate(rows) if r["model"] == GAP_AFTER) + 1
    # Wobble and its interval have MOVED to Figure 1, where twelve values with twelve intervals
    # are read at a glance instead of scanned down a column. What is left here is what a chart
    # cannot carry: the serving path, and the two counts the ratio is formed from.
    body = [[K.display_name(r["model"]), SERVING[r["model"]],
             r["total_measured_items"], r["total_flipped_items"],
             K.num(r["accuracy"], "accuracy")] for r in rows]
    # No bold here, deliberately. The style rule allows at most one emphasised number per table and
    # this table has none: its message is the SPLIT, which the midrule already carries. Bolding the
    # largest count would point at the worst configuration, which is not the reader's takeaway.
    tab = K.tabular(
        "l l S[table-format=3.0] S[table-format=3.0] S[table-format=1.3]",
        ["Model", "Serving", "{Items}", "{Unstable}", "{Acc.}"],
        [body[:cut], body[cut:]], tabcolsep="3pt")
    # Read from the rows, never typed. This caption said "424 items (51 of 60 tasks)" for a day
    # after the audit repartitioned the corpus, while the column beside it printed denominators of
    # 432 to 434: a hardcoded string inside a GENERATED file, which is the worst place for one
    # because everything about its surroundings says the number was computed. The numbers-backed
    # check did not catch it either, since it scans decimals and these are integers.
    n_items = max(int(r["total_measured_items"]) for r in rows)
    n_tasks = max(int(r["cells_present"]) for r in rows)
    n_dropped = max(int(r["cells_dropped"]) for r in rows)
    return K.table_env(tab, _lineup_caption(n_items, n_tasks, n_dropped), "tab:lineup",
                       size=r"\scriptsize")


def _lineup_caption(n_items: int, n_tasks: int, n_dropped: int) -> str:
    """Three lines. What this caption used to carry about wobble and its intervals now belongs to
    Figure 1's caption; repeating it would put one definition in two places, where they drift."""
    return (f"Twelve configurations on the {n_items} items that pass the provenance audit "
            f"({n_tasks - n_dropped} of {n_tasks} tasks retain at least one item), 20 runs per "
            "item at temperature 0.7. \\emph{Unstable} counts items whose answer is not identical "
            "across all 20 runs; accuracy is majority-vote correctness over the same runs. "
            "Wobble, the ratio of the two counts, is Figure~\\ref{fig:lineup}. The rule marks the "
            "order-of-magnitude gap; the two 1B rows are quantizations of one base model, so the "
            "twelve configurations span eleven distinct models.")


def _transfer_block() -> tuple:
    """Item-level transfer at each k, read from the MEAN-based file. The median lives in the
    appendix: it takes values in multiples of 1/k, most pairs share nothing, and its own null is
    0.000 at every percentile, so it separates only zero from non-zero. The mean is the statistic
    the paper's claim is made on and so it is the one printed here."""
    rows = K.read_csv(SRC / "transfer_items.csv")
    # No Pairs column: it reads 90 on every row, so it is width spent on a constant. The caption
    # states it once. Dropping it is what lets the table hold a single column at \scriptsize.
    body = [[r["k"], K.num(r["mean"]), K.num(r["chance"]),
             K.num(r["ratio"], "ratio"), r["p_mean"].replace("<", "$<$"),
             K.ci_tight(r["boot_mean_lo"], r["boot_mean_hi"]),
             f"{r['n_truncated']}/{r['n_pairs']}"] for r in rows]
    # The one emphasised number in the paper: the pre-specified k, in a plain `c` column, because
    # siunitx parses an `S` cell as a number and a font command inside it is not one.
    hit = next(i for i, r in enumerate(rows) if int(r["k"]) == 5)
    body[hit][1] = r"\textbf{" + body[hit][1] + "}"
    # Read, never typed. This caption carried a hardcoded "432 clean items" while the column beside
    # it was computed, and the adjudication exclusion moved the real figure to 425 without touching
    # the literal. numcheck passed it: 432 is a correct rounding of something, somewhere.
    n_items = {int(r["n_items"]) for r in rows}
    n_pairs = {int(r["n_pairs"]) for r in rows}
    assert len(n_items) == 1 and len(n_pairs) == 1, \
        f"every k must run on one population: items {n_items}, pairs {n_pairs}"
    return (K.tabular(
        "S[table-format=1.0] c S[table-format=1.3] S[table-format=2.2] r c r",
        ["{$k$}", "{Mean}", "{Chance}", "{Ratio}", "$p$", "95\\% CI", "Trunc."],
        [body], tabcolsep="2pt"), len(rows), n_items.pop(), n_pairs.pop())


def table2_transfer() -> str:
    """The transfer statistic at every k the corpus supports. The claims block rode under this
    caption while the paper was four pages and is Table~\\ref{tab:claims} now that there is room:
    one caption cannot say what both blocks are without saying neither well."""
    top, n_k, n_items, n_pairs = _transfer_block()
    return K.table_env(
        top,
        "Cross-model transfer of instability, frontier configurations only (10 models, "
        f"{n_pairs} ordered pairs, {n_items} clean items), at each of the {n_k} values of $k$ the "
        "corpus supports. Each pair asks what share of configuration $A$'s $k$ least-stable "
        "\\emph{items} fall inside $B$'s $2k$ least-stable. \\emph{Chance} is the expected share "
        "under the effective $k$ after truncation, \\emph{Ratio} is observed hits over expected, "
        "and the permutation $p$ is over 2{,}000 shuffles of each configuration's own values. The "
        "interval is a bootstrap over the ten \\emph{configurations}, not the 90 pairs, which are "
        "not independent. \\emph{Trunc.} counts pairs where a configuration had fewer than $k$ "
        "unstable items and the set was truncated rather than padded. $k=5$ is the pre-specified "
        "value. The claims this benchmark could not support are Table~\\ref{tab:claims}.",
        # Single column, deliberately. Eight narrow numeric columns fit inside 219pt at \scriptsize,
        # and a full-width float costs roughly twice the page area of a single-column one. The
        # claims table beside it genuinely needs the width; this one never did.
        "tab:transfer", star=False, size=r"\scriptsize")


def table3_categories() -> str:
    """The full matrix. Eight categories will not fit one text width beside their intervals at a
    legible size, so the categories are split into two stacked blocks of four rather than the type
    being shrunk below 7pt. Same exhibit, same rows, half the width."""
    rows = K.read_csv(SRC / "clean" / "model_x_category_wilson.csv")
    cats = sorted({r["category"] for r in rows})
    order = [r["model"] for r in sorted(K.read_csv(SRC / "clean" / "model_summary.csv"),
                                        key=lambda r: float(r["aggregate_wobble"]))]
    by = {(r["model"], r["category"]): r for r in rows}
    n_tasks = {c: by[(order[0], c)]["n_leaves"] for c in cats}
    half = len(cats) // 2
    blocks, headers = [], []
    for group in (cats[:half], cats[half:]):
        headers.append(["Model"] + [f"{K.display_category(c)} ({n_tasks[c]})" for c in group])
        blocks.append([[K.display_name(m)]
                       + [f"{K.num(by[(m, c)]['rate'])} "
                          f"{K.ci_tight(by[(m, c)]['wilson_lo'], by[(m, c)]['wilson_hi'])}"
                          for c in group] for m in order])
    panels = "\n\n\\vspace{4pt}\n\n".join(
        K.tabular("l" + "c" * half, h, [b], tabcolsep="4pt") for h, b in zip(headers, blocks))
    low = [f"\\emph{{{K.display_category(c)}}}" for c in cats if int(n_tasks[c]) < 3]
    return K.table_env(
        panels,
        "Wobble by configuration and clause category on the audited corpus, each rate followed by "
        "its Wilson 95\\% interval with leading zeros dropped. The eight categories are split "
        "across two panels; every panel lists all twelve configurations, ordered by aggregate "
        "wobble. Parenthesised numbers are the tasks each category retains after the provenance "
        f"exclusion. {_floor_note(low)} Intervals overlap almost everywhere, which is why no "
        "ordering between categories is asserted in the text.",
        "tab:categories", star=True, size=r"\scriptsize", placement="t")


def _floor_note(low: list) -> str:
    """The sentence about categories under the estimability floor, agreeing with how many there
    are. The zero case is a real branch and not defensive padding: if a future corpus put every
    category over the floor, a single template would emit ' fall below the three-task estimability
    floor', a sentence with no subject making a claim about nothing."""
    if not low:
        return "Every category clears the three-task estimability floor."
    if len(low) == 1:
        return (f"{low[0]} falls below the three-task estimability floor and is shown for "
                "completeness only: no worst-category claim in this paper uses it.")
    return (f"{K.join_and(low)} fall below the three-task estimability floor and are shown for "
            "completeness only: no worst-category claim in this paper uses them.")


AUDIT_KEEP = ["items in the analysis", "tasks with at least one item in the analysis",
              "model-item pairs measured", "active tasks (non-zero wobble in >=1 model)",
              "split-half reliability, median r_full",
              "share answered correctly on all runs (p=1)",
              "share in the observable band 0.3 <= p <= 0.7",
              "max structurally reachable wobble at accuracy >= 0.9",
              "transfer k=5 frontier-only: median", "transfer k=5 frontier-only: chance",
              "transfer k=10 frontier-only: median", "wobble-accuracy rho"]
AUDIT_LABEL = {"items in the analysis": "Items",
               "tasks with at least one item in the analysis": "Tasks",
               "model-item pairs measured": "Model-item pairs",
               "active tasks (non-zero wobble in >=1 model)": "Tasks with non-zero wobble",
               "split-half reliability, median r_full": "Split-half reliability",
               "share answered correctly on all runs (p=1)": "Share at $p=1$",
               "share in the observable band 0.3 <= p <= 0.7": "Share in $0.3 \\le p \\le 0.7$",
               "max structurally reachable wobble at accuracy >= 0.9":
                   "Structural ceiling, acc.\\ $\\ge 0.9$",
               "transfer k=5 frontier-only: median": "Transfer $k=5$, median",
               "transfer k=5 frontier-only: chance": "Transfer $k=5$, chance",
               "transfer k=10 frontier-only: median": "Transfer $k=10$, median",
               "wobble-accuracy rho": "Wobble-accuracy $\\rho$"}


def table5_audit() -> str:
    """Both readings side by side. A reviewer must be able to check that the exclusion did not
    select the numbers, so the pre-exclusion figures stay in the paper rather than in a repo.

    The flagged count is read from the audit's own JSON. Typed into this caption, it said 46 of
    470 after the matcher repair had made it 36, in a caption otherwise built from live values.

    The first column is headed incl. flagged, never all items: both columns already drop the 7
    adjudicated items, so its 463 is not the data statement's 470 (author review, 2026-08-05)."""
    import json
    a = json.loads((ROOT / "out" / "annotation" / "oracle_audit.json").read_text())
    d = {r["quantity"]: r for r in K.read_csv(SRC / "contamination_delta.csv")}
    p = {r["model"]: r for r in K.read_csv(SRC / "contamination_by_model.csv")}["POOLED"]
    ki = d["items in the analysis"]
    n_adj = a["n_items"] - int(ki["all_items"])
    body = [[AUDIT_LABEL[q], _flex(d[q]["all_items"]), _flex(d[q]["clean_only"])]
            for q in AUDIT_KEEP]
    # 3.5pt, from 4pt: the incl.-flagged header is 2.3pt wider than the all-items one it replaced,
    # and the six column gaps at 0.5pt less absorb exactly that without touching any cell.
    tab = K.tabular("l r r", ["Quantity", "Incl.\\ flagged", "Audited"], [body],
                    tabcolsep="3.5pt")
    return K.table_env(
        tab,
        f"Every headline quantity under both readings. The provenance audit flags "
        f"{a['n_with_issues']} of {a['n_items']} items. Both columns drop the {n_adj} items "
        f"removed at author adjudication: \\emph{{incl.\\ flagged}} keeps the "
        f"{a['n_with_issues']} flagged items and \\emph{{audited}} excludes them, so their item "
        f"rows read {_flex(ki['all_items'])} and {_flex(ki['clean_only'])}. "
        f"Pooled over all twelve configurations, wobble on flagged items is "
        f"{K.num(p['flagged_wobble'])} "
        f"{K.ci(p['flagged_lo'], p['flagged_hi'])} against {K.num(p['clean_wobble'])} "
        f"{K.ci(p['clean_lo'], p['clean_hi'])} on the rest, a difference of "
        f"{K.num(p['difference'])} {K.ci(p['difference_lo'], p['difference_hi'])}, computed by "
        f"Newcombe's method on the two Wilson intervals. The interval excludes zero, so the "
        f"audited reading is the paper's headline and this table is the record of what that "
        f"choice moved.",
        # [htbp] rather than [t], and it changed nothing: this table still takes a page of its own.
        # Both appendix tables ahead of it are full-width floats that claim the top of the page, and
        # the appendix text ends before there is a column bottom left to use, so the float is
        # deferred until a fresh page and then centred on it. The permissive specifier is kept
        # because it costs nothing and will place the table if the appendix ever grows, but it is
        # not a fix, and the layout it produces today is a table alone on the last page.
        "tab:audit", size=r"\footnotesize", placement="htbp")


def _math(interval: str) -> str:
    """Deprecated shim: tablekit.ci_math is the ONE implementation, now that a second table needs
    it. Kept only because this caller already holds a formatted interval string rather than its
    two bounds."""
    lo, hi = interval.strip("[]").split(", ")
    return K.ci_math(lo, hi)


def _flex(v: str) -> str:
    """Counts as integers, everything else at three decimals. The column mixes both, so the choice
    is made per value from the CSV's own magnitude rather than by a per-row flag."""
    f = float(v)
    return str(int(f)) if f == int(f) and abs(f) >= 1 else f"{f:.3f}"


def tables() -> tuple:
    """The ONE roster of generated tables: every consumer reads it rather than keeping a copy.

    checks_geometry.check_tables_current held its own list of five and went on reporting "all 5
    committed tables are byte-identical" after a sixth was added, so the new table was generated,
    committed and never checked. A hand-maintained list can only catch what someone remembered to
    add to it, which is the same defect the zip's import check was written to remove."""
    return (("table1_lineup", table1_lineup), ("table2_transfer", table2_transfer),
            ("table3_categories", table3_categories), ("table4_claims", TC.table4_claims),
            ("table5_audit", table5_audit), ("table6_repair", R.table6_repair),
            ("table11_stratified", TS.table11_stratified)) + TA.tables()


def main() -> None:
    print(K.selftest())
    print(R.selftest())
    print(TA.selftest())
    print(TS.selftest())
    for name, fn in tables():
        path = K.write(DEST / f"{name}.tex", fn())
        print(f"  wrote {path.relative_to(ROOT)}  ({len(path.read_text().splitlines())} lines)")


if __name__ == "__main__":
    main()
