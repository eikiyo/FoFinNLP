"""
Location: paper-a/analysis/adjudication.py
Purpose: Read the author's verdicts on the model-flag worklist. Block 3a enumerates items where
         every configuration contradicts the oracle; the AUTHOR decides what happens to each, and
         this module is the only place that decision enters the analysis. Split out of
         contamination.py, which was at its 300-line budget.
Functions: exclusions(), summary(), selftest()
Calls: config.out_paths()
Imports: csv, pathlib, typing, config
"""

import csv
from pathlib import Path
from typing import Dict, List, Set

import config

REL = "annotation/model_flags.csv"
NEED = ("leaf", "item", "adjudication")
EXCLUDED = "excluded"


def _rows(path: Path = None) -> List[Dict[str, str]]:
    """Absent file means no adjudication has happened yet, which is a legitimate state and reads
    as empty. A file whose schema has drifted is NOT: a column this code cannot find would drop
    every verdict silently and the corpus would be reported as adjudicated when it was not."""
    path = path or (config.out_paths()["out"] / REL)
    if not path.exists():
        return []
    with open(path) as f:
        rows = list(csv.DictReader(f))
    if rows and not set(NEED) <= set(rows[0]):
        raise SystemExit(f"{path} is missing {sorted(set(NEED) - set(rows[0]))} -- refusing to "
                         "run an adjudication filter against a file it cannot read")
    return rows


def exclusions(path: Path = None) -> Dict[str, Set[str]]:
    """leaf -> item ids the author excluded. Keyed on (leaf, item) because one filing can carry a
    flag on two different provisions, and a verdict on one of them says nothing about the other."""
    out: Dict[str, Set[str]] = {}
    for r in _rows(path):
        if r["adjudication"].strip().lower() == EXCLUDED:
            out.setdefault(r["leaf"], set()).add(r["item"])
    return out


def summary(path: Path = None) -> Dict[str, int]:
    """Counts for the paper: raised, and what became of each. Every verdict is reported, including
    the ones that leave the corpus unchanged, because a worklist that only reports its exclusions
    is describing its outcome rather than its input."""
    rows = _rows(path)
    verdicts = [r["adjudication"].strip().lower() for r in rows]
    basis = [r.get("adjudication_basis", "").strip().lower() for r in rows]
    return {"raised": len(rows),
            "excluded": sum(1 for v in verdicts if v == EXCLUDED),
            "upheld": sum(1 for v in verdicts if v == "upheld"),
            "rejected": sum(1 for v in verdicts if v == "rejected"),
            "pending": sum(1 for v in verdicts if not v),
            "examined": sum(1 for b in basis if b == "examined"),
            "blanket": sum(1 for b in basis if b == "blanket"),
            "items": len({(r["leaf"], r["item"]) for r in rows})}


def selftest(tmp: Path = None) -> str:
    """Both arms plus the schema guard. A reader that returns empty on everything would pass a
    can-it-read-an-unadjudicated-file test while silently discarding every verdict."""
    tmp = tmp or Path(config.out_paths()["out"] / "_adjudication_selftest")
    tmp.mkdir(parents=True, exist_ok=True)
    good = tmp / "good.csv"
    good.write_text("leaf,item,adjudication,adjudication_basis\n"
                    "a,1,excluded,examined\n"
                    "a,2,rejected,examined\n"
                    "b,1,excluded,blanket\n"
                    "b,3,,\n")
    got = exclusions(good)
    assert got == {"a": {"1"}, "b": {"1"}}, f"only excluded rows may be dropped, got {got}"
    assert "2" not in got.get("a", set()), "a rejected flag must NOT drop its item"
    s = summary(good)
    assert (s["raised"], s["excluded"], s["rejected"], s["pending"]) == (4, 2, 1, 1), s
    assert (s["examined"], s["blanket"], s["items"]) == (2, 1, 4), s
    assert exclusions(tmp / "does_not_exist.csv") == {}, "an absent file is not an error"
    bad = tmp / "bad.csv"
    bad.write_text("leaf,item,verdict\na,1,excluded\n")
    try:
        exclusions(bad)
        raise AssertionError("a file missing the adjudication column must fail closed")
    except SystemExit as exc:
        assert "adjudication" in str(exc), f"and must name the column: {exc}"
    for f in (good, bad):
        f.unlink()
    tmp.rmdir()
    return ("adjudication selftest PASS - only excluded verdicts drop an item, a rejected flag "
            "keeps its item, an absent file reads empty, and a drifted schema fails closed")


if __name__ == "__main__":
    print(selftest())
