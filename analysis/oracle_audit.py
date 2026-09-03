"""
Location: paper-a/analysis/oracle_audit.py
Purpose: STEP 3, the half that needs no human. A MECHANICAL audit of the oracle: does each stored
         validating quote actually appear in its source document, and does the windowed provision
         the model sees actually contain that quote? Pure string matching -- no judgement, so it is
         not a second reading and cannot substitute for one. It finds defects a human re-reading
         would also find, cheaply, and narrows what the sitting has to look at.
Functions: leaf_items(), norm(), audit_item(), audit_all(), summarise(), write_report(), selftest()
Calls: config.aggregate_module() (the benchmark's own leaf list), read-only over leaves/
Imports: json, re, pathlib, typing, collections, config, tables_out
"""

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

import config
import tables_out as T


def norm(s: str) -> str:
    """Collapse whitespace and normalise the typographic characters SEC filings use inconsistently.
    A quote that differs from its source only by a curly apostrophe or a doubled space is NOT a
    grounding failure, and reporting it as one would be a false RED -- which discards real data
    exactly as silently as a false green invents it."""
    s = (s.replace("’", "'").replace("‘", "'").replace("“", '"')
          .replace("”", '"').replace("–", "-").replace("—", "-")
          .replace("−", "-").replace("\xa0", " "))
    return re.sub(r"\s+", " ", s).strip().lower()


def leaf_items(rel: str) -> List[Dict[str, Any]]:
    path = config.probity_root() / rel / "oracle.jsonl"
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def _read(p: Path) -> Optional[str]:
    return p.read_text(errors="ignore") if p.exists() else None


def corpus_index() -> Dict[str, Dict[tuple, str]]:
    """(leaf, item) -> its window text, its validating quote, and its recorded source URL.

    One loader, because every consumer of the audit needs the same three things and each of them
    reading the corpus its own way is how two callers come to disagree about what an item is. The
    URL is read from BOTH field names in use across leaves: guessing one returns None for every
    leaf that uses the other, which would silently empty the probe's work list."""
    out = {"window": {}, "quote": {}, "url": {}}
    for entry in config.aggregate_module().built_leaves():
        rel = entry["leaf"]
        leaf = Path(rel).name
        for item in leaf_items(rel):
            iid = str(item.get("id", ""))
            key = (leaf, iid)
            out["window"][key] = _read(config.probity_root() / rel / "corpus" / "questions"
                                       / f"{iid}.txt") or ""
            out["quote"][key] = item.get("validating_quote") or item.get("anchor") or ""
            out["url"][key] = item.get("url") or item.get("source_url") or ""
    return out


_SHARED: Dict[str, Path] = {}


def shared_full(name: str) -> Optional[Path]:
    """Find a full source document ANYWHERE in the corpus, not just under its own leaf.

    Leaves deliberately reuse each other's `corpus/full` -- `dividend_cumulative` ships an EMPTY
    full/ directory and borrows every document. Searching only the item's own leaf reported 65
    perfectly present documents as missing: a false RED, which discards real data exactly as
    silently as a false green invents it. The checker had to be fixed before its output could be
    read, not after."""
    if not _SHARED:
        for p in sorted((config.probity_root() / "leaves").glob("*/corpus/full/*.txt")):
            _SHARED.setdefault(p.name, p)
    return _SHARED.get(name)


def audit_item(rel: str, field: str, item: Dict[str, Any]) -> Dict[str, Any]:
    """Three checks per item, each of which can only be RED for a real reason:
       1. the validating quote appears verbatim in the FULL source document;
       2. the quote appears in the WINDOW the model is actually shown;
       3. the recorded answer is a value, not blank.
    A quote that grounds nothing is the failure mode this exists to catch."""
    import fulltext                    # lazy: fulltext imports norm() from this module
    import quotematch                  # lazy: quotematch imports norm() from this module
    iid = str(item.get("id", ""))
    base = config.probity_root() / rel / "corpus"
    win = _read(base / "questions" / f"{iid}.txt")
    quote = item.get("validating_quote") or item.get("anchor") or ""
    nq = norm(quote)
    # Resolve the backing document by VERIFIED CONTENT, not by filename. Looking it up as
    # `<item_id>.txt` found nothing for 150 of 470 items, because documents are stored under a
    # company or accession prefix, and the quote-presence check below then silently did not run on
    # any of them. A check that does not run is not a check that passed.
    fp, route = fulltext.resolve(iid, win, fulltext.pool(config.probity_root())) if win else (None, "no-window")
    full = _read(fp) if fp else None
    row = {"leaf": Path(rel).name, "item": iid, "field": field, "full_retained": full is not None,
           "answer": item.get(field), "has_quote": bool(nq),
           "full_found": full is not None, "window_found": win is not None,
           "source_route": route, "source_state": "not-checkable",
           "n_spans": len(quotematch.spans(quote)), "min_span": None,
           "full_reason": "", "window_reason": "",
           "quote_in_full": None, "quote_in_window": None, "issues": []}
    _check_quote(row, quote, nq, full, win, quotematch)
    if row["answer"] in (None, ""):
        row["issues"].append("oracle answer is blank")
    return row


def _check_quote(row, quote, nq, full, win, quotematch) -> None:
    """The two presence checks, each recording its own reason. Kept apart from the row assembly
    above so the state machine is readable: three verdicts, two haystacks, and a NOT-CHECKABLE
    that must never be counted as a failure."""
    if not nq:
        row["issues"].append("no validating quote or anchor stored")
        row["source_state"] = "no-quote"
        return
    if full is None:
        # NOT an issue, but NOT a pass either. This is the third state the old lookup collapsed
        # into silence: we could not open a source document for this item, so we do not know
        # whether its quote is present. `url` preserves provenance to SEC for a later fetch.
        row["source_state"] = "not-checkable"
    else:
        ok, why, span = quotematch.present(quote, norm(full))
        row.update(quote_in_full=ok, full_reason=why, min_span=span)
        row["source_state"] = {True: "verified-present", False: "verified-absent",
                               None: "not-checkable"}[ok]
        if ok is False:
            row["issues"].append("validating quote NOT found in the source document")
    if win is None:
        row["issues"].append("windowed question file missing from corpus/questions")
        return
    ok, why, span = quotematch.present(quote, norm(win))
    row.update(quote_in_window=ok, window_reason=why)
    row["min_span"] = span if row["min_span"] is None else row["min_span"]
    if ok is False:
        row["issues"].append("validating quote not inside the window the model is shown")


def audit_all() -> List[Dict[str, Any]]:
    agg = config.aggregate_module()
    rows = []
    for entry in agg.built_leaves():
        rel, field = entry["leaf"], entry["field"]
        for item in leaf_items(rel):
            rows.append(audit_item(rel, field, item))
    if not rows:
        raise SystemExit("oracle audit produced 0 rows -- the probe is broken, not the data")
    return rows


def summarise(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    issues = Counter(i for r in rows for i in r["issues"])
    clean = [r for r in rows if not r["issues"]]
    by_leaf = Counter(r["leaf"] for r in rows if r["issues"])
    return {"n_items": len(rows), "n_clean": len(clean), "n_with_issues": len(rows) - len(clean),
            "issues": dict(issues.most_common()),
            "leaves_with_issues": dict(by_leaf.most_common()),
            "n_leaves": len({r["leaf"] for r in rows})}


def write_report(rows: List[Dict[str, Any]], summ: Dict[str, Any], out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    # The REASON columns ride with the verdicts. A rejection reported only as a count cannot be
    # audited, and every matcher defect found so far announced itself in the reason it printed.
    T.write_csv(out_dir / "oracle_audit.csv",
                ["leaf", "item", "field", "answer", "source_route", "source_state", "n_spans",
                 "min_span", "quote_in_full", "quote_in_window", "window_reason", "issues"],
                [[r["leaf"], r["item"], r["field"], str(r["answer"])[:60],
                  r["source_route"], r["source_state"], r["n_spans"], r["min_span"] or "",
                  "" if r["quote_in_full"] is None else int(r["quote_in_full"]),
                  "" if r["quote_in_window"] is None else int(r["quote_in_window"]),
                  r["window_reason"][:120],
                  "; ".join(r["issues"])] for r in rows])
    (out_dir / "oracle_audit.json").write_text(json.dumps(summ, indent=1))
    return out_dir / "oracle_audit.csv"


def selftest() -> str:
    """Prove each check can fire, and prove normalisation does NOT manufacture a failure. A checker
    that reports absence is trustworthy only if it can detect presence."""
    assert norm("The  “Original Issue”") == 'the "original issue"', norm("The  “Original Issue”")
    assert norm("a’b") == "a'b", "curly apostrophes must normalise, not fail"
    good = audit_item.__doc__ is not None
    assert good, "audit_item must stay documented"
    fake = {"id": "__nope__", "validating_quote": "zzz", "f": "v"}
    r = audit_item("leaves/redemption_rights", "f", fake)
    assert r.get("full_retained") is False, "an unretained full document must be recorded"
    assert not any("missing from corpus/full" in i for i in r["issues"]), \
        "an unretained full document is a storage fact, NOT an oracle defect - must not be an issue"
    real = shared_full("1725255_000110465920135025.txt")
    assert real is not None, "the shared-corpus lookup must FIND a document that exists"
    blank = {"id": "__nope__", "validating_quote": "", "f": ""}
    rb = audit_item("leaves/redemption_rights", "f", blank)
    assert "no validating quote or anchor stored" in rb["issues"], "a missing quote must be caught"
    assert "oracle answer is blank" in rb["issues"], "a blank answer must be caught"
    import quotematch
    el = quotematch.spans("(i) the Maximum Participation Amount plus any Series A Dividends "
                          "... and (ii) the amount such holder would have received if all shares")
    assert len(el) == 2, f"an ellipsis quote must split into its contiguous spans: {el}"
    assert not any("..." in f for f in el), "no span may still contain the separator"
    return ("oracle_audit selftest PASS - normalisation absorbs typography without inventing a "
            "failure, and missing-document / missing-quote / blank-answer all fire")


def main() -> Dict[str, Any]:
    """Regenerate oracle_audit.csv and oracle_audit.json from the current matcher.

    There was no entry point, so after the Block 0d matcher repair the CSV was rewritten by the
    callers that needed it and the JSON was not. It went on reporting the pre-repair partition,
    46 of 470, while the report that CITES it said 36 of 470. Two committed artifacts stating
    different values for one number, with the wrong one named as the other's source."""
    print(selftest())
    rows = audit_all()
    summ = summarise(rows)
    path = write_report(rows, summ, config.out_paths()["out"] / "annotation")
    print(f"  {summ['n_with_issues']} of {summ['n_items']} items flagged, "
          f"{summ['n_clean']} clean, across {summ['n_leaves']} tasks")
    print(f"  written: {path.name}, oracle_audit.json")
    return summ


if __name__ == "__main__":
    main()
