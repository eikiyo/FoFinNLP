"""
Location: paper-a/paper/checks_cite.py
Purpose: The `citations verified` gate line -- every cited key is defined in the .bib AND carries a
         stable identifier that appears in the verified record set -- plus the traceability matcher's
         own two-armed selftest. Split out of verify_paper.py at its 300-LOC budget.
Functions: check_citations(), _traceable(), _traceable_selftest()
Calls: out/related_work.md and out/novelty_audit.md (the record set), anthology.bib, custom.bib
Imports: re, sys, pathlib

HERE/ROOT/TEX are module constants for the same reason checks_geometry's are: a positive control has
to be able to point the gate at a temp tree without the gate reading the real one behind its back.
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

TEX = HERE / "main.tex"

IDENT = r"arXiv:([\d.]+)|aclanthology\.org/([\w.\-]+)/|(?:doi\s*=\s*\{|doi\.org/)(10\.[^}\s,]+)"

# (key, bib entry, the identifier that must be found) -- the selftest's table, at module scope so the
# function stays inside its line budget and so a reader can see the covered identifier TYPES at once.
TRACE_CASES = [("a", "@x{a,\n  eprint = {arXiv:2104.02145}\n}", "2104.02145"),
               ("b", "@x{b,\n  url = {https://aclanthology.org/J08-4004/}\n}", "J08-4004"),
               ("c", "@x{c,\n  doi = {10.1145/1852102.1852106}\n}", "10.1145/1852102.1852106")]


def check_citations(fail) -> str:
    groups = set(re.findall(r"\\cite[tp]?\{([^}]*)\}", TEX.read_text()))
    keys = {k.strip() for g in groups for k in g.split(",")}
    bib = "\n".join(p.read_text() for p in (HERE / "anthology.bib", HERE / "custom.bib"))
    undefined = keys - set(re.findall(r"@\w+\{([^,]+),", bib))
    if undefined:
        fail(f"cited keys with no bib entry: {sorted(undefined)}")
    audit = ((ROOT / "out" / "related_work.md").read_text()
             + (ROOT / "out" / "novelty_audit.md").read_text()).replace(" ", "")
    bad = [k for k in sorted(keys) if not _traceable(k, bib, audit)]
    if bad:
        fail(f"citations not traceable to the verified record set: {bad}")
    return f"{len(keys)} citations, every one defined in the .bib and present in the audit files"


def _traceable(key: str, bib: str, audit: str) -> bool:
    """A cited key is traceable when a stable identifier in its bib entry also appears in the
    verified record set.

    DOIs count. They did not at first, and the rule rejected a correctly verified ACM journal
    citation for the sole reason that it is not on arXiv and not in the ACL Anthology: the
    identifier was real, present in both files, and simply of a type the pattern could not
    express. A rule stricter than the thing it is checking turns correct work into a red line,
    which is the same defect as passing incorrect work, only harder to notice because it looks
    like rigour."""
    entry = re.search(re.escape(key) + r",(.*?)\n}", bib, re.S)
    ident = re.search(IDENT, (entry and entry.group(1)) or "")
    token = next((g for g in ident.groups() if g), None) if ident else None
    return bool(token) and token.replace(" ", "") in audit


def _traceable_selftest() -> None:
    """Both arms, on all three identifier types. A matcher that accepted everything would pass a
    can-it-find-a-DOI test while certifying nothing, so each type is also shown to go RED when its
    identifier is absent from the record set."""
    for key, bib, tok in TRACE_CASES:
        assert _traceable(key, bib, f"...{tok}..."), f"{key}: {tok} is present and must trace"
        assert not _traceable(key, bib, "an unrelated record set"), \
            f"{key}: {tok} is absent from the audit and must NOT trace"
    assert not _traceable("d", "@x{d,\n  note = {no identifier at all}\n}", "anything"), \
        "an entry carrying no stable identifier must never be reported as traceable"
    print("  _traceable selftest PASS - arXiv, ACL and DOI each trace when present in the record "
          "set, each fail when absent, and an entry with no identifier never passes")
