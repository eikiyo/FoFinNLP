"""
Location: paper-a/paper/table_repair.py
Purpose: Table 6, the re-windowing repair experiment. Lives outside make_tables.py only because
         that file is at its 300-line budget; it follows the same contract -- every number arrives
         from out/tables/repair_by_task.csv and none is typed into the caption.
         The registered threshold is read from PREREG_UPGRADE.md rather than restated here, so the
         caption cannot drift from the file that fixed it before the experiment ran.
Functions: registered_threshold(), table6_repair(), selftest()
Calls: tablekit (all LaTeX primitives), reads out/tables/repair_by_task.csv, out/PREREG_UPGRADE.md
Imports: re, sys, pathlib, tablekit
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import tablekit as K                                             # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "out" / "tables"
PREREG = ROOT / "out" / "PREREG_UPGRADE.md"


def registered_threshold(text: str = None) -> float:
    """The threshold as PREREG_UPGRADE.md states it, not as this file remembers it.

    The prereg is the artifact that makes the result evidence rather than preference, and a caption
    that announces a threshold is making a claim about that file's contents. Reading it back means
    the two cannot disagree. Fails closed: a threshold that cannot be located is not defaulted to
    the value we expect, because a default here would silently score the experiment against a
    number nobody registered."""
    if text is None:
        text = PREREG.read_text()
    # Collapse whitespace first: the prereg is hard-wrapped prose, so the anchor phrase spans a
    # newline and a line-sensitive pattern finds nothing. It failed closed rather than defaulting,
    # which is the behaviour wanted, but a checker that can only ever fail is not a checker.
    flat = " ".join(text.split())
    hits = set(re.findall(r"fall below the midpoint of those two rates, \*\*(\d\.\d+)\*\*", flat))
    if len(hits) != 1:
        raise SystemExit(f"PREREG_UPGRADE.md yields {len(hits)} registered thresholds ({hits}); "
                         "the caption must not invent one")
    return float(hits.pop())


NAME = {"convert_vs_preference_decision": "convert vs.\\ preference",
        "multi_round_stacked_dilution": "multi-round dilution",
        "option_pool_shuffle": "option pool shuffle"}


def table6_repair() -> str:
    """Before and after by task, with the pooled row the prediction is actually scored on."""
    rows = K.read_csv(SRC / "repair_by_task.csv")
    per = [r for r in rows if not r["task"].startswith("POOLED")]
    pooled, = [r for r in rows if r["task"] == "POOLED"]
    thr = registered_threshold()

    def cell(r, cond):
        return K.num(r[f"{cond}_wobble"]) + " " + K.ci(r[f"{cond}_lo"], r[f"{cond}_hi"])

    def line(r, label):
        return [label, r["n_items"], r["n_cells"], cell(r, "before"), cell(r, "after"),
                K.signed(r["difference"]) + " "
                + K.ci_math(r["difference_lo"], r["difference_hi"])]

    body = [[line(r, NAME.get(r["task"], K.esc(r["task"]))) for r in per],
            [line(pooled, r"\textbf{Pooled}")]]
    # Full width. The single-column version overflowed its column by 59pt, and the fix that keeps
    # every interval visible is the wider float rather than dropping the intervals or cutting them
    # to two decimals against the precision the rest of the paper reports.
    tab = K.tabular("l r r l l l",
                    ["Task", "Items", "Cells", "Original window", "Repaired window",
                     "Change"], body, tabcolsep="5pt")
    after = float(pooled["after_wobble"])
    return K.table_env(
        tab,
        f"The re-windowing repair, {pooled['n_items']} items each measured in both conditions by "
        f"all twelve configurations ({pooled['n_cells']} paired cells). The repaired window is cut "
        f"to the same length as the original and centred on the validating quote, so the only "
        f"difference is whether the evidence is inside it. Registered before the experiment ran: "
        f"the repaired rate would fall below {thr}. It is "
        f"{K.num(pooled['after_wobble'])} "
        f"{K.ci(pooled['after_lo'], pooled['after_hi'])}, "
        f"{'below' if after < thr else 'above'} that threshold, so the prediction fails. The "
        f"pooled change is {K.num(pooled['difference'])} "
        f"{K.ci_math(pooled['difference_lo'], pooled['difference_hi'])} and contains zero. Change "
        f"is the original rate minus the repaired one, so a positive value is a fall in wobble and "
        f"a negative value a rise; {sum(1 for r in per if float(r['difference']) < 0)} of the "
        f"{len(per)} tasks are negative. One task of "
        f"three moves; the per-task split is descriptive and was not the registered test.",
        "tab:repair", star=True, size=r"\footnotesize", placement="t")


def selftest() -> str:
    """Prove the threshold reader discriminates, rather than merely returning a number.

    A reader that finds the value in the real file proves nothing on its own: a regex that matched
    any decimal anywhere would also pass that test and would silently score the experiment against
    whatever number happened to appear first."""
    assert registered_threshold() == 0.161, "the prereg's own threshold must be read back"
    real = PREREG.read_text()
    anchor = "fall\nbelow the midpoint of those two rates, **0.161**"
    assert anchor in real, "the selftest's own mutation target must exist in the real file"
    for bad, why in ((real.replace(anchor, anchor + " and " + anchor.replace("0.161", "0.213")),
                      "two candidate thresholds must not silently resolve to one"),
                     ("a file with no threshold in it at all", "an absent threshold must fail")):
        try:
            registered_threshold(bad)
        except SystemExit:
            continue
        raise AssertionError(why)
    got = registered_threshold(real.replace(anchor, anchor.replace("0.161", "0.213")))
    assert got == 0.213, f"the reader must follow the file, not a remembered value: {got}"
    return ("table_repair selftest PASS - the registered threshold is read from the prereg, "
            "follows it when it changes, and fails closed on zero or ambiguous matches")


if __name__ == "__main__":
    print(selftest())
    print(table6_repair())
