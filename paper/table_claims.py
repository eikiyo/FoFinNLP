"""
Location: paper-a/paper/table_claims.py
Purpose: The bottom block of Table 2 -- every claim tested against this benchmark and not
         supported by it, the pre-registered repair among them. Split out of make_tables.py when
         merging the two tables took that file past its 300-line budget.
Functions: repair_row(), conservative_rows(), claims_block()
Calls: tablekit, table_repair.registered_threshold
Imports: pathlib, tablekit, table_repair
"""

from pathlib import Path
from typing import Any, Dict, List

import table_repair as R
import tablekit as K

SRC = Path(__file__).resolve().parent.parent / "out" / "tables"
# Column widths as a share of \textwidth. The block is drawn full width because four paragraph
# columns inside 3.05 inches force a token like "Correct-but-unstable" wider than its own column,
# and an overfull box in a p{} column prints into its neighbour.
WIDTHS = ("0.27", "0.15", "0.36", "0.15")


def _math(text: str) -> str:
    return K.ci_math(*text.strip("[]").split(", "))


def repair_row() -> List[str]:
    """The registered prediction, reported as a claim that failed. It leads the block because it
    is the paper's own prediction rather than a reader's: a list of other people's expectations
    with our own left off it would be a selective list."""
    rep = {r["task"]: r for r in K.read_csv(SRC / "repair_by_task.csv")}["POOLED"]
    thr = R.registered_threshold()
    return ["Re-windowing lowers wobble to the registered level",
            f"{K.num(rep['after_wobble'])} after, {K.num(rep['before_wobble'])} before",
            f"change {K.num(rep['difference'])} "
            f"{_math(K.ci(rep['difference_lo'], rep['difference_hi']))} contains zero, and "
            f"{K.num(rep['after_wobble'])} exceeds the registered {thr:.3f}",
            "not supported"]


def conservative_rows() -> List[List[str]]:
    """The four claims a reader of the aggregate numbers would most reasonably expect to hold."""
    c = K.read_csv(SRC / "clean" / "conservative_summary.csv")[0]
    d = {r["quantity"]: r for r in K.read_csv(SRC / "contamination_delta.csv")}
    rho = K.num(d["wobble-accuracy rho"]["clean_only"], "rho")
    res = K.num(d["residual rho after structural decomposition (calibrated)"]["clean_only"], "rho")
    ceil = K.num(d["max structurally reachable wobble at accuracy >= 0.9"]["clean_only"])
    return [
        ["Worst category runs $N\\times$ the mean",
         f"median {K.num(c['median_point_ratio'], 'ratio')}$\\times$",
         f"{K.num(c['median_conservative_ratio'], 'ratio')}$\\times$ at the Wilson bounds; "
         f"{c['n_models_above_2x']}/12 above $2\\times$", "not supported"],
        ["The gap grows as models improve",
         f"slope {K.num(c['gradient_slope_frontier'], 'slope')}",
         f"intercept {_math(K.ci(c['gradient_intercept_lo'], c['gradient_intercept_hi']))} "
         f"contains zero ($R^2$ {K.num(c['gradient_r2_frontier'], 'r2')}, "
         f"$n$ = {c['n_models_frontier']})", "not supported"],
        ["Instability is not merely difficulty", f"$\\rho = {rho}$",
         f"residual $\\rho = {res}$ after the structural term", "conceded"],
        ["Correct-but-unstable answers do not occur", "0 tasks observed",
         f"ceiling {ceil} $<$ 0.30 threshold", "unreachable by construction"]]


def claims_block() -> str:
    """The tabular. \\raggedright inside each p{} column: justified, a two-word cell in a narrow
    column stretches its single space across the full width, and the rendered page printed
    "unreachable    by construction". No warning fires for that, because the box is not overfull,
    it is underfull, and underfull is not an error."""
    rag = "".join(f">{{\\raggedright\\arraybackslash}}p{{{w}\\textwidth}} " for w in WIDTHS)
    return K.tabular(rag.strip(),
                     ["Claim tested", "Point estimate", "Under the conservative reading", "Status"],
                     [[repair_row()] + conservative_rows()], tabcolsep="4pt")


def table4_claims() -> str:
    """The claims block as a table of its own. It rode under Table 2's caption while the paper was
    four pages; at eight there is room, and merging cost the block the one thing it needs, which is
    a caption saying what the conservative reading is. Full width for the same reason the block was
    always full width: four paragraph columns inside 3.05 inches force a token wider than its own
    column."""
    return K.table_env(
        claims_block(),
        "Claims tested against this benchmark and not supported by it, our own pre-registered "
        "prediction first. \\emph{Point estimate} is the number a reader of the aggregate would "
        "quote; \\emph{under the conservative reading} is what survives attacking it. For the "
        "worst-category claim that means the largest Wilson lower bound over estimable categories "
        "against the Wilson upper bound of the mean, which avoids selecting a category on the same "
        "data used to score it. \\emph{Conceded} marks a claim we do not make; \\emph{unreachable "
        "by construction} marks one this corpus cannot test at all, for the reason given in "
        "Section~\\ref{sec:instrument}.",
        "tab:claims", star=True, size=r"\footnotesize")


def selftest() -> str:
    """The block must carry EVERY claim, and the repair must be one of them. A merged table that
    quietly dropped a row would look complete: the reader cannot count what is not there."""
    rows = [repair_row()] + conservative_rows()
    assert len(rows) == 5, f"five claims are tested and not supported; the block has {len(rows)}"
    assert all(len(r) == len(WIDTHS) for r in rows), "every row must fill every column"
    assert "registered" in rows[0][2], f"the repair row must name the threshold: {rows[0]}"
    assert sum(1 for r in rows if r[3] == "not supported") == 3, \
        f"three rows are outright unsupported: {[r[3] for r in rows]}"
    body = claims_block()
    assert "midrule" in body and "\\\\" in body, "the block must be a real booktabs tabular"
    assert "|" not in body, "no vertical rules"
    return (f"table_claims selftest PASS - {len(rows)} claims, the registered repair among them, "
            f"each filling all {len(WIDTHS)} columns, rendered as a booktabs tabular with no "
            "vertical rules")


if __name__ == "__main__":
    print(selftest())
