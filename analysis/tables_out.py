"""
Location: paper-a/analysis/tables_out.py
Purpose: Write every generated table (brief 8.2) and the small markdown-rendering helpers the
         report uses, so a number is formatted in exactly ONE place and the report can never
         disagree with the CSV it claims to summarise.
Functions: fmt(), pct(), write_pairs(), write_distributions(), write_ties(),
           write_concentration(), write_matrix_summary(), md_dist_row(), md_table(),
           check_markdown_tables(), check_quoted_figures()
Calls: none
Imports: csv, re, pathlib, typing
"""

import csv
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence


def fmt(v: Optional[float], nd: int = 3) -> str:
    return "—" if v is None else f"{v:.{nd}f}"


def pct(v: Optional[float], nd: int = 1) -> str:
    return "—" if v is None else f"{100 * v:.{nd}f}%"


def md_cell(text: Any) -> str:
    """Escape a table cell. An unescaped pipe in ANY cell silently splits the row into extra
    columns and the whole table stops rendering -- so escaping happens HERE, once, rather than
    depending on every call site remembering. Already-escaped pipes are left alone."""
    return str(text).replace("\\|", "\x00").replace("|", "\\|").replace("\x00", "\\|")


def md_table(header: Sequence[str], rows: Iterable[Sequence[str]]) -> str:
    out = ["| " + " | ".join(md_cell(h) for h in header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(md_cell(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def md_dist_row(name: str, s: Dict[str, Any], extra: str = "") -> List[str]:
    return [name, str(s["n_pairs"]), str(s["n_defined"]), str(s["n_undefined"]),
            fmt(s["median"]), fmt(s["q1"]), fmt(s["q3"]), fmt(s["iqr"]),
            fmt(s["min"]), fmt(s["max"]), extra]


DIST_HEADER = ["Distribution", "pairs", "defined", "undefined", "median rho", "Q1", "Q3",
               "IQR", "min", "max", "note"]


def write_csv(path: Path, header: Sequence[str], rows: Iterable[Sequence[Any]]) -> Path:
    """The one header-plus-rows CSV writer every stage shares. Extracted when stage 3 needed a
    second copy of it -- rule of two, and the clone gate caught the paste before it committed."""
    with open(path, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(list(header))
        wr.writerows(rows)
    return path


def write_pairs(rows: List[Dict[str, Any]], path: Path, subset_label: str) -> Path:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["subset", "model_a", "model_b", "n_leaves", "spearman_rho", "kendall_tau",
                    "tie_fraction_a", "tie_fraction_b", "undefined_reason"])
        for r in rows:
            w.writerow([subset_label, r["model_a"], r["model_b"], r["n"],
                        "" if r["rho"] is None else f"{r['rho']:.6f}",
                        "" if r["tau"] is None else f"{r['tau']:.6f}",
                        fmt(r["tie_a"], 4), fmt(r["tie_b"], 4), r.get("reason") or ""])
    return path


def write_distributions(named: List[tuple], path: Path) -> Path:
    """named = [(label, summary_dict, note), ...] -- every distribution the report quotes."""
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["distribution", "n_pairs", "n_defined", "n_undefined", "median_rho",
                    "q1", "q3", "iqr", "min", "max", "note"])
        for label, s, note in named:
            w.writerow([label, s["n_pairs"], s["n_defined"], s["n_undefined"],
                        "" if s["median"] is None else f"{s['median']:.6f}",
                        "" if s["q1"] is None else f"{s['q1']:.6f}",
                        "" if s["q3"] is None else f"{s['q3']:.6f}",
                        "" if s["iqr"] is None else f"{s['iqr']:.6f}",
                        "" if s["min"] is None else f"{s['min']:.6f}",
                        "" if s["max"] is None else f"{s['max']:.6f}", note])
    return path


def write_ties(rows: List[Dict[str, Any]], path: Path) -> Path:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "tie_fraction_full60", "zero_fraction_full60", "n_distinct_full60",
                    "tie_fraction_active", "zero_fraction_active", "excluded_from_headline"])
        for r in rows:
            w.writerow([r["model"], fmt(r["tie_full"], 4), fmt(r["zero_full"], 4),
                        r["n_distinct_full"], fmt(r["tie_active"], 4), fmt(r["zero_active"], 4),
                        int(r["excluded"])])
    return path


def write_concentration(rows: List[Dict[str, Any]], path: Path) -> Path:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "n_leaves", "n_nonzero_leaves", "top10_nonzero",
                    "top10_share_of_rate_mass", "top10_share_of_flipped_items", "top10_leaves"])
        for r in rows:
            w.writerow([r["model"], r["n_leaves"], r["n_nonzero"], r["top_k_nonzero"],
                        fmt(r["share_of_rate_mass"], 4), fmt(r["share_of_item_mass"], 4),
                        ";".join(r["top_k"])])
    return path


def write_matrix_summary(models: List[str], leaves: List[Dict[str, Any]], cells,
                         agg_wobble: Dict[str, float], path: Path) -> Path:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "cells_present", "cells_dropped", "leaves_zero_wobble",
                    "aggregate_wobble", "total_measured_items", "total_flipped_items"])
        for m in models:
            names = [l["leaf"] for l in leaves]
            w.writerow([m, sum(1 for n in names if not cells[m][n]["absent"]),
                        sum(1 for n in names if cells[m][n]["dropped"]),
                        sum(1 for n in names if (cells[m][n]["wobble"] or 0) == 0),
                        f"{agg_wobble[m]:.6f}",
                        sum(cells[m][n]["n_items"] for n in names),
                        sum(cells[m][n]["flipped"] for n in names)])
    return path


def _table_blocks(text: str) -> List[List[str]]:
    blocks, cur = [], []
    for line in text.split("\n"):
        if line.strip().startswith("|"):
            cur.append(line)
        elif cur:
            blocks.append(cur)
            cur = []
    return blocks + ([cur] if cur else [])


def mixed_width_tables(text: str) -> List[str]:
    """THE decision. Returns one message per table whose rows disagree on column count (escaped
    pipes do not count as separators). Empty list = every table renders."""
    out = []
    for block in _table_blocks(text):
        widths = {r.replace("\\|", "").count("|") for r in block}
        if len(widths) > 1:
            out.append(f"table with mixed column counts {sorted(widths)}: {block[0][:70]}")
    return out


def _selftest_markdown_check() -> None:
    """Truth table on the SAME function the gate calls -- it must go GREEN on a good document and
    RED on a bad one. A check that only ever saw good input has not been shown to discriminate."""
    good = "# t\n\n" + md_table(["a", "b"], [["1", "2"], ["3", "4"]]) + "\n"
    assert mixed_width_tables(good) == [], "selftest FALSE-RED: a valid table was rejected"
    assert mixed_width_tables(good + "| 5 | 6 | 7 |\n"), "selftest FALSE-GREEN: bad row not caught"
    assert mixed_width_tables("# t\n\n" + md_table(["a", "b"], [["x|y", "2"]])) == [], \
        "selftest: an escaped pipe inside a cell must NOT be read as a column separator"
    assert "\\|" in md_table(["x"], [["a|b"]]), "selftest: md_cell failed to escape a pipe"


def check_markdown_tables(paths: List[Path]) -> str:
    """Fail closed if any generated document contains a table that will not render. An unescaped
    pipe raises nothing -- it silently splits the row and the table turns to garbage, which is
    exactly what a human proof-read skims past. So this runs in the pipeline, not by hand, and
    runs its own truth-table selftest first so a clean result means it looked."""
    _selftest_markdown_check()
    bad = [f"{p.name}: {m}" for p in paths for m in mixed_width_tables(p.read_text())]
    if bad:
        raise SystemExit("MARKDOWN TABLE CHECK FAILED:\n  " + "\n  ".join(bad))
    n = sum(len(b) for p in paths for b in _table_blocks(p.read_text()))
    return f"{len(paths)} documents, {n} table rows, all render (selftest: green on good, red on bad)"


def _quoted_figures(text: str) -> set:
    """Decimal figures a document asserts. A digit run preceded by a word character or hyphen is
    part of a name (`temperature-0.7`, `v1.3.1`), not a quoted result -- excluded, or the check
    reports findings about its own regex instead of about the data."""
    # U+2212 MINUS SIGN and en-dash render like a hyphen but are different codepoints; a document
    # that quotes "-0.5516" and one that quotes "−0.5516" mean the same figure and must compare
    # equal, or the gate reds on typography instead of on facts.
    text = text.replace("−", "-").replace("–", "-")
    # The optional sign is INSIDE the group so a signed figure is checked with its sign; the
    # lookbehind still rejects a hyphen used as a name separator (`temperature-0.7`, `v1.3.1`),
    # because there the character before the hyphen is a word character.
    return {m.group(1) for m in re.finditer(r"(?<![\w.-])(-?\d+\.\d+)(?!\.?\d)(?!\w)", text)}


def check_quoted_figures(hand_written: List[Path], generated: List[Path]) -> str:
    """Fail closed if a hand-written document quotes a decimal figure that appears nowhere in the
    generated output. Narration drifts from data silently; this makes it loud."""
    _selftest_quoted_figures()
    known = set()
    for g in generated:
        known |= _quoted_figures(g.read_text())
        known |= {v.rstrip("0").rstrip(".") for v in _quoted_figures(g.read_text())}
    bad = [f"{p.name}: {v}" for p in hand_written
           for v in sorted(_quoted_figures(p.read_text()))
           if v not in known and v.rstrip("0").rstrip(".") not in known]
    if bad:
        raise SystemExit("UNBACKED FIGURE IN NARRATION:\n  " + "\n  ".join(bad))
    n = sum(len(_quoted_figures(p.read_text())) for p in hand_written)
    return f"{n} figures quoted in narration, all present in generated output"


def _selftest_quoted_figures() -> None:
    """Must go GREEN on a backed figure and RED on an invented one, and must not mistake a version
    string or a hyphenated name for a quoted result."""
    gen = "| median | 0.2964 |\n| p | 0.00100 |\n"
    assert _quoted_figures(gen) == {"0.2964", "0.00100"}, "selftest: figure extraction wrong"
    assert _quoted_figures("temperature-0.7 arm, tag v1.3.1") == set(), \
        "selftest FALSE-RED: a hyphenated name or version string read as a quoted figure"
    assert "0.2964" in _quoted_figures("the median was 0.2964."), \
        "selftest FALSE-GREEN: a real quoted figure was not seen"
    assert "-0.5516" in _quoted_figures("rho = -0.5516 over 60 leaves"), \
        "selftest: a signed figure must be extracted WITH its sign"
    assert _quoted_figures("rho = −0.5516") == _quoted_figures("rho = -0.5516"), \
        "selftest: a Unicode minus and an ASCII hyphen-minus must compare equal"
