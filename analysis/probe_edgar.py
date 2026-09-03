"""
Location: paper-a/analysis/probe_edgar.py
Purpose: BLOCK 2a. For every repair candidate with no source document held locally, fetch the
         filing the oracle item cites and decide whether its validating quote is present there.
         Read-only, public, keyless: GET against sec.gov Archives, nothing is written to the
         benchmark. Answers exactly one question per item -- repairable, unrepairable, or unknown --
         and the pre-registered threshold is applied to the total, not renegotiated against it.
Functions: candidates(), fetch(), probe_one(), run(), selftest()
Calls: engine/edgar.fetch_clean (probity's own fetcher, reused), quotematch.present
Imports: json, sys, time, urllib.error, pathlib, typing, config, oracle_audit, quotematch
"""

import importlib.util
import json
import sys
import time
import urllib.error
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import config
import oracle_audit as OA
import quotematch

PAUSE = 0.4              # SEC asks for <10 req/s; four documents does not need to go near that


def edgar_module():
    """probity's own EDGAR fetcher, imported read-only. Reused rather than re-implemented: it
    already carries the User-Agent SEC requires and the tag-stripping the corpus was built with,
    so a quote is matched against text normalised the SAME way the stored windows were."""
    root = config.probity_root()
    spec = importlib.util.spec_from_file_location("probity_edgar", root / "engine" / "edgar.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def candidates(rows: List[Dict[str, Any]], buckets: Dict[Tuple[str, str], str]
               ) -> List[Dict[str, Any]]:
    """Items worth fetching: evidence genuinely absent from the window AND no local source.

    Computational items are excluded by construction. Their window already contains every operand,
    so there is nothing a wider window could add; fetching them would spend requests to confirm a
    document we do not need. That exclusion is the whole reason this probe is four requests rather
    than twenty-six."""
    return [r for r in rows
            if buckets.get((r["leaf"], r["item"])) == "evidence-absent"
            and r["source_state"] == "not-checkable"]


def probe_one(row: Dict[str, Any], quote: str, url: Optional[str], fetch) -> Dict[str, Any]:
    """One item's verdict, with the reason attached. A retrieval failure is 'unknown', never
    'unrepairable' -- a document we could not read is not a document that lacks the quote, and
    collapsing the two would let a network error masquerade as a finding about the corpus."""
    out = {"leaf": row["leaf"], "item": row["item"], "url": url or "",
           "verdict": "unknown", "reason": "", "chars": 0}
    if not url:
        out["reason"] = "no source URL recorded on the oracle item"
        return out
    try:
        text = fetch(url)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
        out["reason"] = f"retrieval failed: {type(exc).__name__}: {exc}"
        return out
    out["chars"] = len(text)
    if len(text) < 500:
        out["reason"] = f"retrieved document is only {len(text)} chars; treating as a failed fetch"
        return out
    ok, why, _ = quotematch.present(quote, OA.norm(text))
    out["reason"] = why
    out["verdict"] = {True: "repairable", False: "unrepairable", None: "unknown"}[ok]
    return out


def run(rows: List[Dict[str, Any]], buckets: Dict[Tuple[str, str], str],
        index: Dict[str, Dict[Tuple[str, str], str]], fetch=None) -> Dict[str, Any]:
    """Probe every candidate and return the counts the pre-registered threshold is applied to."""
    fetch = fetch or edgar_module().fetch_clean
    targets = candidates(rows, buckets)
    results = []
    for i, r in enumerate(targets):
        key = (r["leaf"], r["item"])
        results.append(probe_one(r, index["quote"].get(key, ""), index["url"].get(key), fetch))
        if i + 1 < len(targets):
            time.sleep(PAUSE)
    counts = {v: sum(1 for x in results if x["verdict"] == v)
              for v in ("repairable", "unrepairable", "unknown")}
    return {"results": results, "counts": counts, "n_probed": len(targets)}


def selftest() -> str:
    """Prove the probe classifies BOTH ways and refuses to call a network failure a finding.
    Runs entirely on injected fetchers: a selftest that needed the network could not be trusted to
    fail for the reason it claims."""
    row = {"leaf": "L", "item": "i", "source_state": "not-checkable"}
    hit = probe_one(row, "the holders of Series A Preferred Stock shall be entitled",
                    "http://x", lambda u: "x " * 300 + "the holders of Series A Preferred Stock "
                                                       "shall be entitled to receive")
    assert hit["verdict"] == "repairable", hit
    miss = probe_one(row, "a clause that is nowhere in this filing whatsoever, verbatim",
                     "http://x", lambda u: "y " * 400)
    assert miss["verdict"] == "unrepairable" and "not found" in miss["reason"], miss

    def boom(_):
        raise urllib.error.URLError("connection refused")
    dead = probe_one(row, "anything at all in this quote here", "http://x", boom)
    assert dead["verdict"] == "unknown" and "retrieval failed" in dead["reason"], \
        f"a network failure must be UNKNOWN, never unrepairable: {dead}"
    tiny = probe_one(row, "anything at all in this quote here", "http://x", lambda u: "err")
    assert tiny["verdict"] == "unknown", f"a truncated fetch must be UNKNOWN: {tiny}"
    nourl = probe_one(row, "q", None, lambda u: "text")
    assert nourl["verdict"] == "unknown" and "no source URL" in nourl["reason"], nourl

    picked = candidates([{"leaf": "L", "item": "a", "source_state": "not-checkable"},
                         {"leaf": "L", "item": "b", "source_state": "not-checkable"},
                         {"leaf": "L", "item": "c", "source_state": "verified-present"}],
                        {("L", "a"): "evidence-absent", ("L", "b"): "computational",
                         ("L", "c"): "evidence-absent"})
    assert [p["item"] for p in picked] == ["a"], \
        f"only evidence-absent items with no local source may be fetched: {picked}"
    return ("probe_edgar selftest PASS - a present quote reads repairable, an absent one "
            "unrepairable, and a refused connection, a truncated body and a missing URL all read "
            "unknown rather than being counted as evidence; computational items are never fetched")
