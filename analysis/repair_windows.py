"""
Location: paper-a/analysis/repair_windows.py
Purpose: Block 2b, the UNPAID half. Re-window the 14 repairable evidence-absent items so the
         validating quote falls inside the text the model is shown, and PROVE it does using the
         same matcher the audit uses. Writes to a separate namespace; the original condition is
         never touched, because the paired analysis needs both.
         Usage:  python3 analysis/repair_windows.py
Functions: norm_map(), quote_raw_range(), repair(), write_all(), selftest(), main()
Calls: oracle_audit.norm/corpus_index, fulltext.pool/resolve, quotematch.present/spans/locate
Imports: csv, re, sys, pathlib, config, oracle_audit, fulltext, quotematch
"""

import csv
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config                        # noqa: E402
import fulltext                      # noqa: E402
import oracle_audit as OA            # noqa: E402
import probe_edgar                   # noqa: E402
import quotematch                    # noqa: E402

DEST = config.PAPER_ROOT / "out" / "repair" / "windows"
# The repaired window is cut to the SAME length as the original. Widening it would confound the
# repair with extra context: an item that improves could have improved because the evidence is now
# present, or merely because the model was given more to read. Equal length isolates provenance.
PAD = 0


def norm_map(s: str) -> Tuple[str, List[int]]:
    """OA.norm's output plus, for each normalised character, its index in the raw string.

    Needed because quotematch works on normalised text and a window has to be cut from raw text.
    The result is ASSERTED equal to OA.norm(s) on every call: this function mirrors a normaliser
    it does not own, and a mirror that silently drifts from its original would cut windows around
    the wrong offsets while every check downstream still passed."""
    out, idx = [], []
    for i, ch in enumerate(s):
        c = {"’": "'", "‘": "'", "“": '"', "”": '"',
             "–": "-", "—": "-", "−": "-", "\xa0": " "}.get(ch, ch)
        if c.isspace():
            if out and out[-1] == " ":
                continue
            out.append(" ")
        else:
            out.append(c.lower())
        idx.append(i)
    # Mirror .strip() on the collapsed text, keeping the map aligned.
    lo, hi = 0, len(out)
    while lo < hi and out[lo] == " ":
        lo += 1
    while hi > lo and out[hi - 1] == " ":
        hi -= 1
    text, offs = "".join(out[lo:hi]), idx[lo:hi]
    if text != OA.norm(s):
        raise SystemExit("norm_map has drifted from oracle_audit.norm; the offset map would be "
                         "wrong and every repaired window cut from it would be silently misplaced")
    return text, offs


def quote_raw_range(quote: str, raw: str) -> Optional[Tuple[int, int]]:
    """Raw-text range covering every span the matcher REQUIRES, or None if any is absent.

    Uses quotematch.required_spans so the definition of 'the quote is here' is the audit's, not a
    second one written for this file. A composite quote is several spans; the range spans them
    all, so the repaired window contains the whole composite rather than its first fragment."""
    ntext, offs = norm_map(raw)
    parts = quotematch.spans(quote)
    if not parts:
        return None
    req, _ = quotematch.required_spans(parts)
    lo, hi = None, None
    for p in req:
        # locate() normalises the span itself, so it takes the RAW span. It also lacks the
        # trailing-word fallback find_span() applies, so a span the audit accepts only via its
        # tail variant would be reported absent here: the item would be dropped from the repair
        # for a reason the audit does not recognise. Mirror the fallback rather than diverge.
        needle, hits = p, quotematch.locate(p, ntext)
        if not hits:
            alt = quotematch.tail_variant(p)
            if alt:
                needle, hits = alt, quotematch.locate(alt, ntext)
        if not hits:
            return None
        start = hits[0]
        end = start + len(OA.norm(needle))
        lo = start if lo is None else min(lo, start)
        hi = end if hi is None else max(hi, end)
    if lo is None or hi > len(offs):
        return None
    return offs[lo], offs[min(hi, len(offs) - 1)] + 1


def repair(raw: str, quote: str, target_len: int) -> Tuple[Optional[str], str]:
    """A window of target_len raw characters centred on the quote, or None with a named reason.

    Fails closed. A repaired window whose quote the matcher still cannot find is not written at
    all: emitting one would put an item into the repaired condition that was never repaired, and
    the paired analysis would read the difference as an effect."""
    rng = quote_raw_range(quote, raw)
    if rng is None:
        return None, "the quote's required spans are not all present in the source document"
    lo, hi = rng
    need = max(target_len, hi - lo)
    slack = need - (hi - lo)
    start = max(0, lo - slack // 2)
    win = raw[start:start + need]
    ok, why, _ = quotematch.present(quote, OA.norm(win))
    if ok is not True:
        return None, f"repaired window still does not contain the quote: {why}"
    return win, f"quote at raw {lo}-{hi}, window {start}-{start + len(win)} ({len(win)} chars)"


# Items the classifier put in evidence-absent that are COMPUTATIONAL, and so were never repair
# targets under PREREG_UPGRADE: their windows already carry a complete labelled derivation.
# Verified by arithmetic on the window's own operands, independently of any model output:
#   col1  (124.3 - 0.3 - 32.6 - 78.6) / 25.2 = 0.5079  oracle 0.51
#   col2  (122.0 - 0.3 - 32.6 - 78.6) / 25.2 = 0.4167  oracle 0.42
#   col4  (122.6 - 0.3 - 32.6 - 78.6) / 25.2 = 0.4405  oracle 0.44
#   col3  (121.2 - 0.3 - 32.6 - 78.6) / 25.2 = 0.3849  oracle 0.39 (rounds to 0.38; see below)
# The classifier reads operands out of the stored QUOTE, and for these the quote is a pointer to a
# table ("Implied Per Share Reference Range ... $0.51") naming no operand at all, so it had nothing
# to test and defaulted to evidence-absent. Re-windowing them REPLACED the derivation with raw deck
# text and destroyed the operands. It is listed explicitly rather than fixed in the classifier
# because the general rule tried first (quote names no operand -> undetermined) reclassified 12
# items, 8 of which had repaired correctly: a false RED on good data is the same defect in the
# other direction.
# col3's oracle answer does not match its own window's arithmetic to 2dp. That is an oracle
# question, not a windowing one, and it is left for the Block 3a flag list.
NOT_REPAIRABLE = {("liquidation_waterfall_payout", i) for i in
                  ("col1_selected_companies_ltm", "col2_selected_companies_fy17e",
                   "col3_selected_companies_fy18e", "col4_discounted_cash_flow")}


def targets() -> List[Dict[str, str]]:
    """The repairable items, read from the audit's own bucket table, minus the computational ones
    the classifier could not recognise."""
    path = config.out_paths()["tables"] / "window_buckets.csv"
    return [r for r in csv.DictReader(path.open())
            if r["bucket"] == "evidence-absent" and r["source_state"] != "verified-absent"
            and (r["leaf"], r["item"]) not in NOT_REPAIRABLE]


CACHE = config.PAPER_ROOT / "out" / "repair" / "sources"


def source_text(leaf: str, item: str, window: str, url: str, docs) -> Tuple[Optional[str], str]:
    """The full document, from the local pool if held, otherwise fetched once and CACHED.

    Four of the fourteen are the items the Block 2a probe fetched. The probe read them, decided
    they were repairable, and kept nothing, so the text that established the count was gone by the
    time the repair needed it. Caching makes the repair reproducible offline and means the SEC is
    asked once rather than once per re-run."""
    doc, how = fulltext.resolve(item, window, docs)
    if doc is not None:
        return doc.read_text(errors="ignore"), f"local:{doc.name}"
    cached = CACHE / leaf / f"{item}.txt"
    if cached.exists():
        return cached.read_text(errors="ignore"), f"cache:{cached.name}"
    if not url:
        return None, f"unresolved locally ({how}) and no source URL recorded"
    import time
    import urllib.error
    try:
        text = probe_edgar.edgar_module().fetch_clean(url)
        time.sleep(0.4)                       # SEC asks for well under 10 req/s
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
        return None, f"unresolved locally and fetch failed: {type(exc).__name__}: {exc}"
    if len(text) < 500:
        return None, f"fetched document is only {len(text)} chars; treating as a failed fetch"
    cached.parent.mkdir(parents=True, exist_ok=True)
    cached.write_text(text)
    return text, f"fetched:{len(text)} chars, cached"


def write_all(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Write each repaired window under out/repair/windows/, never into the benchmark tree."""
    idx = OA.corpus_index()
    docs = fulltext.pool(config.probity_root())
    out = []
    for r in rows:
        key = (r["leaf"], r["item"])
        window, quote = idx["window"].get(key, ""), idx["quote"].get(key, "")
        raw, origin = source_text(r["leaf"], r["item"], window, idx["url"].get(key, ""), docs)
        if raw is None:
            out.append(dict(r, repaired="no", reason=origin))
            continue
        win, why = repair(raw, quote, len(window))
        if win is None:
            out.append(dict(r, repaired="no", reason=why))
            continue
        dest = DEST / r["leaf"] / f"{r['item']}.txt"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(win)
        out.append(dict(r, repaired="yes", reason=why, orig_len=str(len(window)),
                        new_len=str(len(win)), source=origin))
    return out


def selftest() -> str:
    """Prove the offset map and the fail-closed branch, on text whose answer is known."""
    raw = "The  Quick Brown “Fox” jumps over the lazy dog and then keeps running onward."
    ntext, offs = norm_map(raw)
    assert ntext == OA.norm(raw), "the map must reproduce the real normaliser exactly"
    assert len(offs) == len(ntext), "one raw offset per normalised character"
    i = ntext.index("brown")
    assert raw[offs[i]:offs[i] + 5].lower() == "brown", \
        f"offset must land on the raw token, got {raw[offs[i]:offs[i] + 5]!r}"
    win, why = repair(raw, "jumps over the lazy dog", 30)
    assert win is not None and "jumps over the lazy dog" in win, f"a present quote repairs: {why}"
    assert len(win) >= len("jumps over the lazy dog"), "the window must contain the whole quote"
    bad, why2 = repair(raw, "this sentence is nowhere in the source text at all", 30)
    assert bad is None and "not all present" in why2, f"an absent quote must fail closed: {why2}"
    return ("repair_windows selftest PASS - the offset map reproduces the real normaliser and "
            "lands on raw tokens, a present quote yields a window containing it, and an absent "
            "quote writes nothing and says why")


def main() -> List[Dict[str, str]]:
    print(selftest())
    rows = targets()
    print(f"  {len(rows)} repairable items from the audit's bucket table")
    out = write_all(rows)
    done = [r for r in out if r["repaired"] == "yes"]
    for r in out:
        mark = "ok " if r["repaired"] == "yes" else "FAIL"
        print(f"  {mark} {r['leaf'][:26]:<26} {r['item'][:22]:<22} {r['reason'][:60]}")
    T = __import__("tables_out")
    T.write_csv(config.out_paths()["tables"] / "repair_manifest.csv",
                ["leaf", "item", "repaired", "orig_len", "new_len", "source", "reason"],
                [[r["leaf"], r["item"], r["repaired"], r.get("orig_len", ""),
                  r.get("new_len", ""), r.get("source", ""), r["reason"]] for r in out])
    print(f"\n  {len(done)}/{len(rows)} windows repaired and verified, written under "
          f"{DEST.relative_to(config.PAPER_ROOT)}")
    return out


if __name__ == "__main__":
    main()
