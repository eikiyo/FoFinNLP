"""
Location: paper-a/paper/table_stratified.py
Purpose: Camera-ready Table (tab:stratified), answering the reviews directly: the flagged-vs-clean
         contrast stratified by answer type and by configuration set (ncjD: answer-type confound,
         the two 1B configurations), an item-level bootstrap beside Newcombe (ncjD: clustering),
         and graded dispersion beside binary wobble (taFL: severity). Reads
         out/tables/stratified_contrast.csv, written by analysis/stratified.py.
Functions: table11_stratified(), selftest()
Calls: tablekit (num, signed, ci, ci_math, tabular, table_env, read_csv)
Imports: pathlib, tablekit
"""

from pathlib import Path

import tablekit as K

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "out" / "tables"

WOBBLE_ROWS = tuple((cs, st) for cs in ("all", "frontier")
                    for st in ("pooled", "numeric", "non-numeric"))

# CSV stratum name -> printed row label. The paper calls the third group by what failed (the
# label), not by where the quote was looked for.
FAILURE_ROWS = (("evidence-absent", "evidence-absent"), ("computational", "computational"),
                ("quote-absent-from-source", "label-untraceable"))


def _cm(lo, hi) -> str:
    """Tight math interval for the difference columns: leading zeros dropped to match the
    Flagged/Clean cells, no inner space (inside a cell there is no line to break), and a
    negative bound's minus in math mode so it prints as a minus, not a hyphen."""
    if lo in (None, "") or hi in (None, ""):
        return "{--}"

    def one(v):
        t = f"{float(v):.3f}"
        sign = "$-$" if t.startswith("-") else ""
        return sign + t.lstrip("-").lstrip("0")
    return f"[{one(lo)},{one(hi)}]"


def _cell(r, field, lo, hi) -> str:
    return f"{K.num(r[field])} {K.ci_tight(r[lo], r[hi])}"


def _wobble_row(rows, cs, st, label=None):
    f, c = rows[(cs, st, "flagged")], rows[(cs, st, "clean")]
    d = rows[(cs, st, "difference")]
    return ["wobble", label or st, "12" if cs == "all" else "10", f"{f['items']}/{c['items']}",
            _cell(f, "wobble", "boot_lo", "boot_hi"), _cell(c, "wobble", "boot_lo", "boot_hi"),
            f"{K.signed(d['wobble'])} {_cm(d['newcombe_lo'], d['newcombe_hi'])}",
            _cm(d["boot_lo"], d["boot_hi"])]


def _disp_row(rows, cs):
    f, c = rows[(cs, "pooled", "flagged")], rows[(cs, "pooled", "clean")]
    d = rows[(cs, "pooled", "difference")]
    return ["disp.", "pooled", "12" if cs == "all" else "10",
            f"{f['items']}/{c['items']}",
            _cell(f, "dispersion", "disp_boot_lo", "disp_boot_hi"),
            _cell(c, "dispersion", "disp_boot_lo", "disp_boot_hi"), "{--}",
            f"{K.signed(d['dispersion'])} " + _cm(d["disp_boot_lo"], d["disp_boot_hi"])]


CAPTION = (
    "The flagged-against-clean contrast, stratified. Brackets on the Flagged and Clean cells are "
    "95\\% intervals from a bootstrap over \\emph{items} (2{,}000 draws, resampling flagged and "
    "clean items independently; narrower than Wilson where items are homogeneous, degenerate "
    "at $n = 2$), the resampling unit because each item contributes one pair per "
    "configuration and those pairs are not independent; the difference column carries the "
    "Newcombe interval on the two Wilson intervals beside the item-bootstrap interval for the "
    "same difference. \\emph{Cfg.} 12 is every configuration, 10 drops the two 1B "
    "configurations. The three failure-type rows split the flagged items by cause "
    "(Section~\\ref{sec:benchmark}), each against the whole clean set, pooled configurations "
    "only. Newcombe's method applies to proportions; dispersion is a mean, so its difference "
    "carries the bootstrap interval only. \\emph{Dispersion} is the share of runs "
    "disagreeing with the modal answer, averaged over the same model-item pairs as wobble. The "
    "numeric stratum holds 83.3\\% of the flags; the non-numeric flagged group has 6 items "
    "and the label-untraceable group 2, reported for completeness, not weight.")


def table11_stratified() -> str:
    rows = {(r["config_set"], r["stratum"], r["group"]): r
            for r in K.read_csv(SRC / "stratified_contrast.csv")}
    blocks = [[_wobble_row(rows, cs, st) for cs, st in WOBBLE_ROWS],
              [_wobble_row(rows, "all", st, label) for st, label in FAILURE_ROWS],
              [_disp_row(rows, cs) for cs in ("all", "frontier")]]
    tab = K.tabular("l l r r r r r r",
                    ["", "Stratum", "Cfg.", "f/c", "Flagged", "Clean",
                     r"$\Delta$ (Newc.)", r"$\Delta$ (boot)"],
                    blocks, tabcolsep="2.5pt")
    return K.table_env(tab, CAPTION, "tab:stratified", star=True)


def _fixture_rows():
    base = {"items": "3", "wobble": "0.25", "boot_lo": "0.10", "boot_hi": "0.40",
            "dispersion": "0.12", "disp_boot_lo": "0.05", "disp_boot_hi": "0.20",
            "newcombe_lo": "0.05", "newcombe_hi": "0.30"}
    out = {}
    for cs in ("all", "frontier"):
        for st in ("pooled", "numeric", "non-numeric"):
            for g in ("flagged", "clean"):
                out[(cs, st, g)] = dict(base)
            out[(cs, st, "difference")] = dict(base, wobble="-0.03", dispersion="-0.01")
    for st, _ in FAILURE_ROWS:
        for g in ("flagged", "clean"):
            out[("all", st, g)] = dict(base)
        out[("all", st, "difference")] = dict(base, wobble="0.15", dispersion="0.02")
    return out


def selftest() -> str:
    """The two rendering rules a silent regression would break: a negative difference must carry
    a math minus, never a hyphen, and an absent value must render as a dash, never as 0."""
    rows = _fixture_rows()
    w = _wobble_row(rows, "all", "numeric")
    assert w[6].startswith("$-$"), f"negative difference needs a math minus: {w[6]}"
    assert w[1] == "numeric" and w[2] == "12" and w[3] == "3/3", w[:4]
    d = _disp_row(rows, "frontier")
    assert d[6] == "{--}" and d[2] == "10", "dispersion has no Newcombe column and 10 configs"
    fr = _wobble_row(rows, "all", "quote-absent-from-source", "label-untraceable")
    assert fr[1] == "label-untraceable" and fr[2] == "12", \
        "a failure row prints the paper's name for the group, on the pooled set"
    assert _cm("-0.044", "0.223") == "[$-$.044,.223]", _cm("-0.044", "0.223")
    assert _cm("0.128", "0.211") == "[.128,.211]", _cm("0.128", "0.211")
    rows[("all", "pooled", "flagged")]["wobble"] = None
    assert K.num(None) == "{--}", "an absent value must render as a dash, never 0"
    return ("table_stratified selftest PASS - math minus on negative differences, dash on the "
            "empty Newcombe cell and on absent values, failure rows under the paper's label on "
            "the pooled set, row shape stable")


if __name__ == "__main__":
    print(selftest())
