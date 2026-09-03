"""
Location: paper-a/paper/numcheck.py
Purpose: NOT `numbers` -- that name is a stdlib module matplotlib imports, and this
         file sits on sys.path[0] for every script here, so it would shadow it.
         Match figures quoted in the prose against the generated CSVs. Split out of verify_paper.py
         when the interval-pair check took that file over its LOC budget; the file-reading and
         rounding rules live here so the acceptance test stays a readable list of checks.
Functions: csv_rows(), csv_values(), backed(), intervals(), unpaired(), selftest()
Calls: none
Imports: re, pathlib, typing
"""

import re
from pathlib import Path
from typing import Any, Iterable, List, Sequence, Set, Tuple

IV_RE = re.compile(r"\[(-?\d*\.\d+),\s*(-?\d*\.\d+)\]")
COMMENT_RE = re.compile(r"(?m)^\s*%.*")


def _floats(line: str) -> List[float]:
    """Every parseable number in one CSV line. A non-numeric cell (a model name, an em dash for a
    value that was never measured) is skipped rather than coerced: turning 'not measured' into a
    number is the one failure this whole module exists to prevent."""
    out = []
    for cell in line.split(","):
        # A permutation p that no draw reached is stored as the resolution bound it really is,
        # "< 0.00050", not as a fabricated tail. The bound IS a generated value and the prose
        # quotes it, so the comparator is stripped and the number read. Dropping the cell instead
        # made the checker report a figure as unbacked while its own CSV held it, which is a
        # false red: it would have been "fixed" by deleting a true number from the paper.
        cell = re.sub(r"^\s*[<>]\s*", "", cell)
        try:
            out.append(float(cell))
        except ValueError:
            # Deliberate and total: a CSV row legitimately mixes labels and em dashes with numbers,
            # and "this cell is not a number" is the normal case, not an error. The failure this
            # guards against is the opposite one, coercing an unmeasured cell into a value, which
            # is why nothing is appended here rather than a 0.
            continue
    return out


def csv_rows(paths: Iterable[Path]) -> List[List[float]]:
    """One entry per data row, holding that row's numbers. Row structure is preserved because an
    interval is a PAIR: it is a claim about two numbers standing together, and flattening the rows
    would discard exactly the evidence that makes the claim checkable."""
    return [nums for p in paths for line in p.read_text().splitlines()[1:]
            if (nums := _floats(line))]


def csv_values(rows: Sequence[Sequence[float]]) -> Set[float]:
    """Every generated value, plus its percentage and complement-percentage forms, since a share
    stored as 0.018110 is quoted in the prose as 1.8."""
    flat = {v for r in rows for v in r}
    return flat | {100 * v for v in flat} | {100 * (1 - v) for v in flat}


def backed(q: str, values: Set[float]) -> bool:
    """True when some generated value rounds to `q` at the precision `q` states.

    String equality here red-flagged fourteen correct numbers, because the prose quotes 0.087 where
    the CSV holds 0.086614. A gate that rejects correct data is as damaging as one that accepts
    wrong data, so the comparison happens at the claimed precision."""
    dp = len(q.split(".")[1]) if "." in q else 0
    return any(f"{v:.{dp}f}" == q for v in values)


def intervals(tex: str) -> List[Tuple[str, str]]:
    return IV_RE.findall(COMMENT_RE.sub("", tex))


def unpaired(ivs: Sequence[Tuple[str, str]], rows: Sequence[Sequence[float]]) -> List[str]:
    """Intervals whose two bounds never co-occur in a single generated row.

    Asking only whether each figure appears SOMEWHERE among the values is a containment test
    wearing a correctness test's clothes. It passed [0.194, 0.263] for a flagged-item interval
    whose real lower bound is 0.193, because 0.194 happens to be the transfer chance baseline
    elsewhere in the corpus. Requiring both bounds to come from the SAME row is much harder to
    satisfy by coincidence, and the pairing is what the prose actually asserts."""
    bad = []
    for lo, hi in ivs:
        if not any(_has(r, lo) and _has(r, hi) for r in rows):
            bad.append(f"[{lo}, {hi}]")
    return bad


def _has(row: Sequence[float], q: str) -> bool:
    dp = len(q.split(".")[1])
    return any(f"{v:.{dp}f}" == q for v in row)


def selftest() -> str:
    """Prove the pair rule catches the exact miss that motivated it, and that it still accepts a
    correct interval. A rule shown to pass good input but never shown to reject bad input has not
    been demonstrated to discriminate at all."""
    rows = [[0.226449, 0.193494, 0.263184], [0.400, 0.194, 0.196]]
    assert unpaired([("0.193", "0.263")], rows) == [], "the true pair must be accepted"
    # The shipped bug: 0.194 IS in the corpus, on a different row, so a containment test passes it.
    assert backed("0.194", csv_values(rows)), "containment alone accepts the wrong bound"
    assert unpaired([("0.194", "0.263")], rows) == ["[0.194, 0.263]"], \
        "a bound borrowed from another row must be rejected"
    assert unpaired([("0.193", "0.999")], rows) == ["[0.193, 0.999]"], "an invented bound is unpaired"
    assert backed("0.226", csv_values(rows)) and not backed("0.987654", csv_values(rows))
    assert backed("1.8", csv_values([[0.018110]])), "a share quoted as a percentage must match"
    assert _floats("gemma3-1b,49,0.5664,—") == [49.0, 0.5664], "a dash is skipped, never read as 0"
    assert intervals("x [0.1, 0.2] y\n% [9.9, 9.9]\n") == [("0.1", "0.2")], "comments are ignored"
    # Both directions on the comparator. A bounded p is READ, because the bound is the value the
    # analysis produced and the prose quotes; a cell that merely starts with a letter is still not
    # a number, so stripping "<" must not become a licence to parse anything.
    assert _floats("5,< 0.00050,0.4") == [5.0, 0.00050, 0.4], "a bounded p must be read"
    assert _floats("k,n/a,< abc") == [], "stripping a comparator must not coerce a non-number"
    return ("numcheck selftest PASS - the pair rule rejects a bound borrowed from another row, "
            "accepts the true pair, skips unmeasured cells, reads a bounded p without coercing a "
            "non-number, and ignores commented-out TeX")


if __name__ == "__main__":
    # Running this file standalone used to print nothing and exit 0. The writing spec lists it as
    # a check that must pass, and a module that passes by having no entry point is the same green
    # as a module that ran and found nothing wrong. It now runs its own selftest and says so.
    print(selftest())
