"""
Location: paper-a/paper/tablekit.py
Purpose: The shared LaTeX table primitives make_tables.py assembles from. One place decides how a
         number is formatted, how a cell is escaped, and how a booktabs environment is opened and
         closed, so no fragment can disagree with another about a decimal place or a rule style.
Functions: read_csv(), num(), ci(), esc(), display_name(), tabular(), table_env(), write()
Calls: none
Imports: csv, pathlib, typing
"""

import csv
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

# Decimal places, fixed per quantity type. Consistency within a column is a paper rule, so it is
# enforced by a lookup rather than by remembering at each call site.
DP = {"wobble": 3, "accuracy": 3, "rate": 3, "ratio": 2, "rho": 3, "slope": 2, "r2": 3, "ci": 3}

# Lineup metadata, shared by the tables and the figures. It lived in make_tables until Figure 1
# needed the same two facts; a second copy beside the first is how a table and a figure about the
# same twelve configurations come to disagree about which of them are frontier.
# label -> serving path, parsed once from the benchmark's own preflight lineup by the analysis
# pipeline and mirrored here as data rather than re-derived from the "-or" naming convention.
SERVING = {"gemma3-1b": "local", "gemma3-1b-qat": "local", "deepseek-v4f": "direct",
           "deepseek-v4p": "direct", "haiku-4.5-direct": "direct", "gemma4-31b-or": "routed",
           "mistral-large-or": "routed", "minimax-m2.5-or": "routed", "llama3.3-70b-or": "routed",
           "gemini3-flash-or": "routed", "gpt-oss-120b-or": "routed", "gpt5-mini-or": "routed"}
GAP_AFTER = "minimax-m2.5-or"      # the order-of-magnitude break; shown as a rule, not a sentence
SMALL = ("gemma3-1b", "gemma3-1b-qat")     # the two 1B configurations, on the far side of the gap


def read_csv(path: Path) -> List[Dict[str, str]]:
    with open(path) as f:
        return list(csv.DictReader(f))


def num(v: Any, kind: str = "wobble", dash: str = "{--}") -> str:
    """A number at its column's fixed precision, or an explicit dash. An empty cell is NEVER
    rendered as 0: 'not measured' and 'measured as zero' are different facts and a table that
    conflates them lies about the corpus."""
    if v is None or v == "" or v == "—":
        return dash
    return f"{float(v):.{DP.get(kind, 3)}f}"


def signed(v: Any, kind: str = "wobble", dash: str = "{--}") -> str:
    """A number for a TEXT column, carrying a real minus instead of a hyphen.

    An S column gets this for free from siunitx; an `l` column does not, so the repair table's
    Change column printed "-0.083" with a hyphen while its own caption, built through ci_math,
    printed a proper minus two lines below. Nothing warns: a hyphen is a valid character and the
    box is neither over- nor underfull. In print it reads as a typo in a column whose whole job is
    to show a sign."""
    s = num(v, kind, dash)
    return f"$-${s[1:]}" if s.startswith("-") else s


def ci(lo: Any, hi: Any, kind: str = "ci") -> str:
    if lo in (None, "", "—") or hi in (None, "", "—"):
        return "{--}"
    return f"[{float(lo):.{DP[kind]}f}, {float(hi):.{DP[kind]}f}]"


def ci_math(lo: Any, hi: Any, kind: str = "ci") -> str:
    """An interval for CAPTION prose, whose bounds are in math mode but whose brackets and comma
    are not.

    Two reasons, both learned from the compiler. A negative bound needs math mode or its minus
    renders as a hyphen, which reads as a typo in print. But wrapping the WHOLE interval makes it
    one unbreakable atom, and inside a narrow paragraph column an unbreakable atom is an overfull
    box that prints into the neighbouring column. Splitting at the comma gives LaTeX a break point
    and keeps the glyphs right."""
    s = ci(lo, hi, kind)
    if s == "{--}":
        return s
    a, b = s.strip("[]").split(", ")
    return f"[${a}$, ${b}$]"


def ci_tight(lo: Any, hi: Any, kind: str = "ci") -> str:
    """The same interval with its leading zeros dropped, for the matrix table where eight of them
    share one text width. Dropping a leading zero on a quantity the caption states is a proportion
    costs no information and buys about a fifth of the table's width, which is the difference
    between a readable 8pt matrix and one set below the 7pt floor."""
    if lo in (None, "", "—") or hi in (None, "", "—"):
        return "{--}"
    a, b = (f"{float(v):.{DP[kind]}f}".lstrip("0") for v in (lo, hi))
    return f"[{a},{b}]"


def join_and(items: Sequence[str]) -> str:
    """'a' / 'a and b' / 'a, b and c'. A plain comma join reads as a broken sentence at exactly two
    items, which is the count this corpus produces: 'cap table, exit waterfall fall below'. The
    empty case returns empty and the CALLER must branch on it, because a sentence built around a
    list of nothing asserts something about nothing."""
    items = list(items)
    if len(items) <= 1:
        return items[0] if items else ""
    return ", ".join(items[:-1]) + " and " + items[-1]


def esc(text: str) -> str:
    """LaTeX-escape a literal string. Model labels carry underscores and hyphens; an unescaped
    underscore is a compile error, which is the cheapest possible failure and still worth removing
    from the loop."""
    for a, b in (("\\", r"\textbackslash{}"), ("_", r"\_"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("$", r"\$"), ("{", r"\{"), ("}", r"\}")):
        text = text.replace(a, b)
    return text


def display_name(label: str) -> str:
    """The benchmark's internal label minus its serving suffix. The suffix is redundant beside a
    Serving column and reads as noise in a printed table; the mapping is stripping, never
    renaming, so the artifact's identifiers remain recoverable."""
    for suffix in ("-or", "-direct"):
        if label.endswith(suffix):
            return esc(label[: -len(suffix)])
    return esc(label)


def display_category(family: str) -> str:
    return esc(family.replace("_", " "))


def tabular(colspec: str, header: Sequence[str], blocks: Sequence[Sequence[Sequence[str]]],
            tabcolsep: Optional[str] = None) -> str:
    """A booktabs tabular. `blocks` is a list of row-groups; a midrule separates consecutive
    groups, which is how the order-of-magnitude gap in Table 1 is shown without a sentence.
    No vertical rule is emitted anywhere, because the column spec is the only place one could
    appear and every caller passes one built here."""
    if "|" in colspec:
        raise ValueError(f"vertical rule in column spec {colspec!r} -- forbidden by the style rules")
    out = []
    if tabcolsep:
        out.append(f"\\setlength{{\\tabcolsep}}{{{tabcolsep}}}")
    out += [f"\\begin{{tabular}}{{{colspec}}}", "\\toprule",
            " & ".join(header) + r" \\", "\\midrule"]
    for i, block in enumerate(blocks):
        if i:
            out.append("\\midrule")
        out += [" & ".join(r) + r" \\" for r in block]
    out += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(out)


def table_env(body: str, caption: str, label: str, star: bool = False,
              size: str = r"\footnotesize", placement: str = "t",
              shrink: Optional[float] = None) -> str:
    """`shrink` scales the tabular to that fraction of the column width via graphicx.

    It exists for one reason. In ACL's `review` mode the `lineno` package prints a line number in
    the margin, and where a float happens to sit at that number's height, the number lands ON the
    table: the pdflatex build printed "265" through Table 2's last header cell. The table was not
    overfull, so no warning fired and only the rendered page showed it. Pulling the table's edges
    in by a few points moves it out of the number's path. The scale is checked against the 7pt
    floor by verify_paper.py, not assumed safe."""
    env = "table*" if star else "table"
    if shrink:
        body = f"\\resizebox{{{shrink}\\columnwidth}}{{!}}{{%\n{body}}}"
    return "\n".join([f"\\begin{{{env}}}[{placement}]", r"\centering", size, body,
                      f"\\caption{{{caption}}}", f"\\label{{{label}}}", f"\\end{{{env}}}", ""])


def write(path: Path, text: str) -> Path:
    """Write only when the bytes actually differ.

    An unconditional write moves the mtime on every run, so re-generating a table that came out
    identical made the compiled PDF look stale to any mtime-based check while latexmk, which
    compares content, correctly reported nothing to do. The freshness check then failed on a
    build that was entirely current. A generator that rewrites identical bytes is claiming a
    change it did not make, and everything downstream that trusts mtimes inherits the claim."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text() == text:
        return path
    path.write_text(text)
    return path


def selftest() -> str:
    """Prove the formatters on the cases that would otherwise ship a wrong table: a missing value
    must not become 0, precision must follow the column, and a vertical rule must be refused."""
    assert num("") == "{--}" and num(None) == "{--}", "a missing value must never render as a number"
    assert num("0.0299", "wobble") == "0.030", "wobble is 3 decimals"
    assert num("4.9606", "ratio") == "4.96", "ratios are 2 decimals"
    assert num(0) == "0.000", "a measured zero must render as 0.000, not as a dash"
    # 0.0065 renders as 0.006, not 0.007: the nearest double to 0.0065 is below it, so Python's
    # format rounds down. Asserting the arithmetically-expected 0.007 here was a false RED about
    # IEEE-754, not about the formatter, and pinning the ACTUAL behaviour is what makes this a
    # control rather than a wish.
    assert ci("0.0065", "0.0306") == "[0.006, 0.031]", ci("0.0065", "0.0306")
    assert ci("0.0064999", "0.03061") == "[0.006, 0.031]", "rounding must be at the third decimal"
    assert ci("", "0.03") == "{--}", "half an interval is no interval"
    assert ci_tight("0.0654", "0.3061") == "[.065,.306]", ci_tight("0.0654", "0.3061")
    assert ci_tight("0.0", "1.0") == "[.000,1.000]", "a bound of 1 must keep its integer part"
    assert ci_tight("", "1.0") == "{--}", "the tight form must refuse a half interval too"
    assert esc("gpt-oss_120b") == r"gpt-oss\_120b", esc("gpt-oss_120b")
    assert display_name("haiku-4.5-direct") == "haiku-4.5", display_name("haiku-4.5-direct")
    assert display_name("gemma3-1b-qat") == "gemma3-1b-qat", "a non-suffix must not be stripped"
    assert join_and(["a", "b"]) == "a and b", join_and(["a", "b"])
    assert join_and(["a", "b", "c"]) == "a, b and c", join_and(["a", "b", "c"])
    assert join_and(["a"]) == "a" and join_and([]) == "", "one item and none are both handled"
    refused = False
    try:
        tabular("l|r", ["a", "b"], [[["1", "2"]]])
    except ValueError:
        # The ValueError IS the expected outcome of this negative control: `tabular` must refuse a
        # vertical rule. Recording it in a flag rather than swallowing it keeps the assertion below
        # able to fail if the refusal ever stops happening.
        refused = True
    assert refused, "a vertical rule must be refused, not emitted"
    t = tabular("lr", ["a", "b"], [[["1", "2"]], [["3", "4"]]])
    assert t.count("midrule") == 2 and "toprule" in t and "bottomrule" in t, t
    assert signed("-0.083") == "$-$0.083", f"a negative must carry a math minus: {signed('-0.083')}"
    assert signed("0.058") == "0.058", "a positive must not be decorated"
    assert signed("") == "{--}", "an unmeasured value stays a dash, never a signed zero"
    return ("tablekit selftest PASS - missing stays missing, precision follows the column, "
            "escaping is real, suffix stripping is exact, a negative in a text column carries a math minus, "
            "vertical rules are refused")
