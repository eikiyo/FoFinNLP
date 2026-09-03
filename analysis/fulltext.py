"""
Location: paper-a/analysis/fulltext.py
Purpose: Resolve WHICH full source document backs a corpus item, and PROVE the resolution instead
         of trusting a filename. The audit previously looked a document up as `<item_id>.txt`, but
         documents are stored under a company or accession prefix, so for 150 of 470 items it found
         nothing and silently skipped the quote-presence check entirely. That missing third state
         is what this module exists to make visible.
Functions: pool(), norm_text(), window_core(), resolve(), selftest()
Calls: oracle_audit.norm (the ONE normaliser, so resolution and quote-matching cannot disagree)
Imports: functools, pathlib, typing
"""

from pathlib import Path
from typing import Dict, Optional, Tuple

import oracle_audit as OA

# Chars of the window's interior used as the resolution probe. Taken from a quarter of the way in
# rather than the start: windows often open with a boilerplate heading shared by many filings from
# the same issuer, and matching on that would resolve to the wrong document with full confidence.
CORE = 300
CORE_MIN = 60

_NORM: Dict[Path, str] = {}


_POOL: Dict[str, Path] = {}


def pool(root: Path) -> Dict[str, Path]:
    """Every full source document in the corpus, keyed by filename. Leaves deliberately share each
    other's `corpus/full`, so the pool spans all leaves rather than the item's own. Built once:
    the audit resolves 470 items and re-globbing a 949-file tree per item is pure waste."""
    if not _POOL:
        _POOL.update({p.name: p for p in sorted(root.glob("leaves/*/corpus/full/*.txt"))})
    return _POOL


def norm_text(path: Path) -> str:
    """Normalised document text, memoised. 1,123 documents and 55 MB: normalising per candidate
    per item would make the content scan quadratic in the corpus for no gain."""
    if path not in _NORM:
        _NORM[path] = OA.norm(path.read_text(errors="ignore"))
    return _NORM[path]


def window_core(window: str) -> str:
    """The slice of the window used to prove a candidate document is the right one."""
    w = OA.norm(window)
    core = w[len(w) // 4: len(w) // 4 + CORE]
    return core if len(core) >= CORE_MIN else w


def resolve(iid: str, window: str, docs: Dict[str, Path]) -> Tuple[Optional[Path], str]:
    """The document backing this item, plus HOW it was found.

    Every route is verified by content: the window is a verbatim extract of its source, so a
    candidate is accepted only when the window's interior actually appears in it. That check also
    applies to the exact-name route, which the old lookup trusted blind -- a filename that happens
    to match is not evidence, and accepting one silently pointed the quote check at the wrong
    document. Returns (None, 'unresolved') when nothing verifies, which is a REPORTABLE state and
    not the same fact as 'the quote is absent'."""
    core = window_core(window)
    if not core:
        return None, "no-window"
    seen = set()
    for name in _candidates(iid, docs):
        p = docs[name]
        seen.add(p)
        if core in norm_text(p):
            return p, "by-name" if name == f"{iid}.txt" else "by-prefix"
    for p in docs.values():                       # last resort: the corpus is small enough to scan
        if p not in seen and core in norm_text(p):
            return p, "by-content"
    return None, "unresolved"


def _candidates(iid: str, docs: Dict[str, Path]):
    """Exact name first, then progressively shorter prefixes: `uber_ryan_graves` may be backed by
    `uber.txt`. Ordered longest-first so the most specific document wins."""
    exact = f"{iid}.txt"
    if exact in docs:
        yield exact
    parts = iid.split("_")
    for n in range(len(parts) - 1, 0, -1):
        cand = "_".join(parts[:n]) + ".txt"
        if cand in docs and cand != exact:
            yield cand


def selftest(root: Path) -> str:
    """Prove the resolver on the real corpus, including the case that FAILS under the old rule.

    A repair is only demonstrated by input the previous version got wrong, so the third assertion
    below is the load-bearing one: it requires at least one item that the bare `<item_id>.txt`
    lookup could not have found."""
    docs = pool(root)
    assert len(docs) > 500, f"pool looks wrong: {len(docs)} documents"
    qs = sorted(root.glob("leaves/*/corpus/questions/*.txt"))
    assert qs, "no window files found; the resolver was tested against nothing"

    routes = {"by-name": 0, "by-prefix": 0, "by-content": 0, "unresolved": 0, "no-window": 0}
    for q in qs[:120]:
        _, how = resolve(q.stem, q.read_text(errors="ignore"), docs)
        routes[how] += 1
    assert routes["by-name"] > 0, "no item resolved by its own name; the fast path is broken"
    assert routes["by-prefix"] + routes["by-content"] > 0, (
        "no item resolved by any route other than its own filename, so this fix repairs nothing "
        "-- the old lookup would have scored identically and the bug is not demonstrated")

    # A name that exists but whose content does not match must be REFUSED, not accepted. This is
    # the behaviour the old lookup lacked: it returned the file whose name matched, full stop.
    fake = dict(docs)
    victim = qs[0]
    wrong = next(p for n, p in docs.items() if window_core(victim.read_text(errors="ignore"))
                 not in norm_text(p))
    fake[f"{victim.stem}.txt"] = wrong
    p, how = resolve(victim.stem, victim.read_text(errors="ignore"), fake)
    assert how != "by-name" or p != wrong, (
        "a filename match with non-matching content was accepted; resolution is not verified")

    # And an item with no backing document must come back unresolved, never quietly wrong.
    p, how = resolve("nonexistent_item_xyz", "text that appears in no filing at all " * 20, docs)
    assert p is None and how == "unresolved", f"expected unresolved, got {how}"
    return (f"fulltext selftest PASS - {len(docs)} documents; of 120 windows probed "
            f"{routes['by-name']} resolved by name, {routes['by-prefix']} by prefix, "
            f"{routes['by-content']} by content, {routes['unresolved']} unresolved; a "
            f"content-mismatched filename is refused and a missing document reports unresolved")
