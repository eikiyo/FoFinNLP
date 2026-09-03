"""
Location: paper-a/paper/table_appendix.py
Purpose: The appendix exhibits that do not fit main-text tables: the unit comparison behind ranking
         items rather than tasks, the two robustness splits, and the model-flag worklist the author
         adjudicates. Separate from make_tables.py because that file is at its 300-line budget.
         Every number arrives from a generated CSV; none is typed here or into a caption.
Functions: table7_tasklevel(), table8_serving(), table9_loo(), table10_flags(),
           selftest()
Calls: tablekit (LaTeX primitives), reads out/tables/*.csv and out/annotation/model_flags.csv
Imports: sys, pathlib, typing, tablekit
"""

import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

import tablekit as K                                             # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "out" / "tables"
FLAGS = ROOT / "out" / "annotation" / "model_flags.csv"
PENDING = "not yet adjudicated"


def _unit_rows(path: Path, unit: str) -> List[List[str]]:
    """One row per k for one unit. The two units share a row shape so a reader compares down a
    column rather than across two tables with different headers."""
    out = []
    for r in K.read_csv(path):
        out.append([unit if r["k"] == "3" else "", r["k"], r["n_items"],
                    f"{r['n_truncated']}/{r['n_pairs']}", K.num(r["mean"]),
                    K.num(r["chance"]), K.num(r["ratio"], "ratio"),
                    r["p_mean"].replace("<", "$<$")])
    return out


def table7_tasklevel() -> str:
    """The unit comparison. Both blocks come from the same statistic on the same clean population,
    so the only difference between them is what an item is."""
    items, tasks = _unit_rows(SRC / "transfer_items.csv", "items"), \
        _unit_rows(SRC / "transfer_tasks.csv", "tasks")
    body = K.tabular(
        "l S[table-format=1.0] S[table-format=3.0] c S[table-format=1.3] "
        "S[table-format=1.3] S[table-format=2.2] r",
        ["Unit", "{$k$}", "{Units}", "Trunc.", "{Mean}", "{Chance}", "{Ratio}", "Perm. $p$"],
        [items, tasks])
    n_tasks, n_items = tasks[0][2], items[0][2]
    return K.table_env(
        body,
        f"Transfer at every $k$ under both ranking units, over the same {n_items} clean items "
        f"grouped into {n_tasks} tasks and the same ten frontier configurations, 90 ordered pairs "
        "each. A task's score is the share of its items that flip. Trunc. counts pairs where one "
        "side had fewer than $k$ non-zero units, so its top-$k$ was cut short rather than padded. "
        "Chance is recomputed per pair from the effective $k$ after truncation, which is why the "
        "coarser unit carries a chance line an order of magnitude higher and a correspondingly "
        "smaller ratio at the same permutation $p$. $p$ is over 2{,}000 permutations that shuffle "
        "each configuration's values among its own positions.",
        "tab:tasklevel", star=True)


PATH_LABEL = {"direct-direct": "both directly served", "mixed": "one of each",
              "routed-routed": "both routed"}


def table8_serving() -> str:
    """The serving-path split. Its own table, not a block under a shared header: the leave-one-out
    rows carry different quantities, and stacking them under one header put a hits count in a
    column headed Median. Nothing warned, because a wrong number in a right-shaped cell compiles."""
    rows = [[PATH_LABEL[r["pairing"]], r["n_pairs"], K.num(r["mean"]), K.num(r["median"]),
             r["n_pairs_cross_family"], K.num(r["mean_cross_family"])]
            for r in K.read_csv(SRC / "transfer_serving_path.csv")]
    body = K.tabular(
        "l S[table-format=2.0] S[table-format=1.3] S[table-format=1.3] S[table-format=2.0] "
        "S[table-format=1.3]",
        ["Pairing", "{Pairs}", "{Mean}", "{Median}", "{Cross-fam.}", "{Mean}"],
        [rows], tabcolsep="4pt")
    return K.table_env(
        body, "Transfer at $k = 5$ by how each side of a pair is served, on the clean population. "
        "The two rightmost columns repeat the split after the two same-family configurations are "
        "removed, which is the check that the directly served result is not one model agreeing "
        "with its own sibling. Six ordered pairs from three configurations is the narrowest result "
        "in the paper and is reported as underpowered wherever it appears.",
        # Full width: six columns and a spelled-out pairing label ran 48pt past the 219pt column,
        # measured from the compiler, and a table that overfulls prints into its neighbour.
        "tab:serving", star=True)


def table9_loo() -> str:
    """Each frontier configuration dropped in turn. The check that no single configuration is
    carrying the effect."""
    rows = [[("full lineup" if r["dropped"] == "(none)" else K.display_name(r["dropped"])),
             r["n_models"], K.num(r["mean"]), r["hits"], K.num(r["ratio"], "ratio")]
            for r in K.read_csv(SRC / "transfer_leave_one_out.csv")]
    body = K.tabular("l S[table-format=2.0] S[table-format=1.3] S[table-format=3.0] "
                     "S[table-format=2.2]",
                     ["Configuration dropped", "{Left}", "{Mean}", "{Hits}", "{Ratio}"],
                     [rows[:1], rows[1:]], tabcolsep="4pt")
    return K.table_env(
        body, "Transfer at $k = 5$ with each frontier configuration dropped in turn, on the clean "
        "population. Left is how many configurations remain, Hits the total shared items over the "
        "ordered pairs among them, and Ratio those hits against the chance expectation recomputed "
        "for that lineup. The first row above the rule is the full lineup, so every row below it "
        "is read against that one.",
        "tab:loo")


def _flag_rows() -> List[List[str]]:
    """Ranked by run support, which is what the brief for this exhibit asks a reader to weigh."""
    rows = sorted(K.read_csv(FLAGS), key=lambda r: -float(r["support"]))
    return [[K.display_name(r["leaf"]), K.esc(r["oracle"]), K.esc(r["consensus_answer"]),
             f"{r['runs_backing']}/{r['runs_total']}", r["min_modal_n"],
             "yes" if r["unanimous"] == "True" else "no",
             K.esc(r["adjudication"]) if r["adjudication"] else PENDING] for r in rows]


def table10_flags() -> str:
    """The model-flag worklist. The adjudication column is rendered from the file, so filling it in
    is the only action needed to publish the verdicts: nothing about a verdict is written here."""
    rows = _flag_rows()
    done = [r for r in rows if r[-1] != PENDING]
    settled = (f"Of the {len(rows)}, {len(done)} have been adjudicated against the source filing."
               if done else "None has been adjudicated at the time of writing; the column is "
               "printed empty rather than omitted, so a reader can see the worklist is open.")
    body = K.tabular("l l l c S[table-format=2.0] c l",
                     ["Task", "Oracle", "Models say", "Runs", "{Floor}", "Unan.", "Adjudication"],
                     [rows], tabcolsep="4pt")
    return K.table_env(
        body, "Items where the configurations' modal answers agree with each other and contradict "
        f"the stored oracle label, ranked by run support. {settled} Runs is the number of the "
        "responses across all twelve configurations backing the models' answer. Floor is the "
        "weakest single configuration's own support out of 20 runs, carried as a column rather "
        "than applied as a filter: requiring every configuration to hold its answer on at least 18 "
        "of 20 admits none of these, and a criterion that empties the table is a result about the "
        "criterion. Unan. marks the items where all twelve configurations produced the same "
        "normalised answer. A flag is a candidate for human review and never a correction; no "
        "label changes until the author has read the filing and upheld it.",
        "tab:flags", star=True)


def tables() -> tuple:
    """The roster this module contributes, in the shape make_tables.tables() uses."""
    return (("table7_tasklevel", table7_tasklevel), ("table8_serving", table8_serving),
            ("table9_loo", table9_loo), ("table10_flags", table10_flags))


def selftest() -> str:
    """Each table must carry every row its source holds. A silently short appendix table is the
    same defect as a silently short main-text one, and nobody proofreads an appendix."""
    n_flags = len(K.read_csv(FLAGS))
    assert len(_flag_rows()) == n_flags, "the flag table must carry every flag raised"
    bodies = {n: fn() for n, fn in tables()}
    for name, body in bodies.items():
        assert "|" not in body.split("caption")[0], f"{name} has a vertical rule"
        assert "midrule" in body, f"{name} is not a booktabs tabular"
    n_k = len(K.read_csv(SRC / "transfer_tasks.csv"))
    assert bodies["table7_tasklevel"].count(r"\\") >= 2 * n_k, \
        "the unit comparison must print both units at every k"
    return (f"table_appendix selftest PASS - {len(bodies)} tables, {n_flags} flags carried, "
            f"both units at {n_k} values of k, no vertical rules")


if __name__ == "__main__":
    print(selftest())
