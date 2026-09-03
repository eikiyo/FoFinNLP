"""
Location: paper-a/analysis/prospect.py
Purpose: STEP 2a, candidate mining ONLY. Find documents in the EXISTING shared corpus that can carry
         a multi-step-computation item (the pre-registered target property), extract the inputs with
         verbatim anchors, compute the answer deterministically, and FAIL CLOSED on any document
         where more than one reading is available. Emits an oracle sheet for a human to sign off.
         It does NOT write into the probity tree and does NOT run any model.
Functions: corpus_docs(), find_multiples(), find_oips(), window(), candidates(), write_sheet()
Calls: none (reads the probity corpus read-only)
Imports: re, pathlib, typing, config, tables_out
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import config
import tables_out as T

WORD_NUM = {"one": 1.0, "two": 2.0, "three": 3.0, "four": 4.0, "1": 1.0, "2": 2.0, "3": 3.0}

MULT = re.compile(
    r"\b(one|two|three|four|1|2|3|4)(?:\s*\(\s*\d\s*\))?\s*(?:times|x)\s+"
    r"the\s+(?:then[-\s]applicable\s+)?Original\s+Issue\s+Price", re.I)
OIP = re.compile(r"Original\s+Issue\s+Price[^.]{0,140}?\$\s?([\d,]+\.\d{2,6})", re.I)
WINDOW_BEFORE, WINDOW_AFTER = 470, 520


def corpus_docs() -> Dict[str, Path]:
    """Every unique full document already on disk. The corpus is SHARED across leaves (leaves reuse
    each other's `corpus/full`), so a new leaf needs no new fetching -- which is the whole reason
    the 2026-08-02 sourcing deadline is reachable."""
    out: Dict[str, Path] = {}
    for p in sorted((config.probity_root() / "leaves").glob("*/corpus/full/*.txt")):
        out.setdefault(p.name, p)
    return out


def find_multiples(text: str) -> List[Tuple[float, str]]:
    """Every distinct liquidation multiple stated in the document, with its verbatim phrase."""
    seen: Dict[float, str] = {}
    for m in MULT.finditer(text):
        val = WORD_NUM.get(m.group(1).lower())
        if val is not None:
            seen.setdefault(val, m.group(0))
    return sorted(seen.items())


def find_oips(text: str) -> List[Tuple[float, str]]:
    """Every distinct dollar Original Issue Price stated, with its verbatim phrase."""
    seen: Dict[float, str] = {}
    for m in OIP.finditer(text):
        try:
            val = float(m.group(1).replace(",", ""))
        except ValueError:
            continue
        seen.setdefault(val, m.group(0))
    return sorted(seen.items())


def window(text: str, anchor: str) -> Optional[str]:
    """The provision window the model would see -- same shape as the existing leaves' `window_on`."""
    i = text.lower().find(anchor.lower()[:60])
    if i < 0:
        return None
    return text[max(0, i - WINDOW_BEFORE): i + len(anchor) + WINDOW_AFTER]


ROLE_EXCLUDE = {
    "participation cap": r"[Pp]articipation\s+Cap",
    "maximum participation amount": r"Maximum\s+Participation\s+Amount",
    "IPO / conversion threshold": r"[Qq]ualified\s+(?:IPO|[Pp]ublic\s+[Oo]ffering)|initial\s+public"
                                  r"\s+offering\s+price|automatically\s+converted|[Cc]onversion\s+"
                                  r"[Pp]rice\s+shall",
    "a ceiling or condition, not an amount": r"until\s+such\s+time\s+as|shall\s+have\s+received|"
                                             r"would\s+result\s+in|not\s+less\s+than|shall\s+exceed",
    "answer folds in accrued dividends": r"includ\w*\s+(?:without\s+limitation\s+)?any\s+dividends|"
                                         r"plus\s+(?:all\s+)?accrued",
}
ROLE_REQUIRE = (r"prior\s+and\s+in\s+preference\s+to|before\s+any\s+(?:payment|distribution)|"
                r"[Ll]iquidation\s+[Pp]reference|entitled\s+to\s+receive[^.]{0,80}amount\s+per\s+share")


def role_check(win: str) -> Tuple[bool, str]:
    """Is this clause actually a LIQUIDATION PREFERENCE AMOUNT, or merely a place where the phrase
    'N times the Original Issue Price' happens to appear?

    This gate exists because the surface pattern is overwhelmingly used for something else. Of the
    first seven documents that passed every numeric check, SIX turned out to be a participation cap
    ('the Participation Cap', 'the Maximum Participation Amount'), a Qualified-IPO price threshold,
    or an IPO conversion condition -- and `participation_cap` is ALREADY a leaf, so shipping them
    would have rebuilt an existing leaf under a wrong label. A keyword match is a candidate, never
    proof: the clause has to say what it is."""
    for label, pat in ROLE_EXCLUDE.items():
        if re.search(pat, win):
            return False, label
    if not re.search(ROLE_REQUIRE, win):
        return False, "no liquidation-preference language in the window"
    return True, ""


def _verdict(mults, oips) -> Tuple[str, str]:
    """FAIL CLOSED on ambiguity. A charter routinely states an Original Issue Price for each series;
    if two readings are available the item is not a measurement, it is a coin toss with a quote
    attached. Excluded with a specific reason so the rejections can be audited -- a counting-only
    gate cannot be checked, and a false REJECT discards real data as silently as a false accept."""
    if not mults and not oips:
        return "EXCLUDE", "no multiple and no dollar original issue price found"
    if not mults:
        return "EXCLUDE", "an original issue price is stated but no liquidation multiple"
    if not oips:
        return "EXCLUDE", "a liquidation multiple is stated but no dollar original issue price"
    if len(mults) > 1:
        return "EXCLUDE", (f"{len(mults)} distinct multiples stated "
                           f"({', '.join(str(m) for m, _ in mults)}) - which series is meant is "
                           "ambiguous from the window")
    if len(oips) > 1:
        return "EXCLUDE", (f"{len(oips)} distinct original issue prices stated "
                           f"({', '.join(f'${v}' for v, _ in oips)}) - multi-series document, the "
                           "pairing is ambiguous")
    return "CANDIDATE", ""


def candidates(docs: Dict[str, Path]) -> List[Dict[str, Any]]:
    """One row per document, kept or excluded, ALWAYS with a reason. Every row is emitted so the
    exclusions can be read; a miner that reports only its survivors cannot be audited."""
    rows = []
    for name, path in docs.items():
        text = path.read_text(errors="ignore")
        mults, oips = find_multiples(text), find_oips(text)
        verdict, reason = _verdict(mults, oips)
        row = {"doc": name, "verdict": verdict, "reason": reason,
               "n_multiples": len(mults), "n_oips": len(oips), "multiple": None,
               "oip": None, "answer": None, "multiple_quote": "", "oip_quote": "",
               "window_chars": 0}
        if verdict == "CANDIDATE":
            (mv, mq), (ov, oq) = mults[0], oips[0]
            win = window(text, mq)
            row.update({"multiple": mv, "oip": ov, "answer": round(mv * ov, 6),
                        "multiple_quote": mq, "oip_quote": oq,
                        "window_chars": len(win or "")})
            if not win:
                row.update(verdict="EXCLUDE",
                           reason="the multiple's phrase could not be located for windowing")
            else:
                ok, why = role_check(win)
                if not ok:
                    row.update(verdict="EXCLUDE",
                               reason=f"wrong semantic role: {why} - the phrase appears, but the "
                                      "clause is not a liquidation preference amount")
        rows.append(row)
    return sorted(rows, key=lambda r: (r["verdict"] != "CANDIDATE", r["doc"]))


def dedupe_by_provision(rows: List[Dict[str, Any]], docs: Dict[str, Path]) -> int:
    """Demote candidates that restate the SAME provision as an earlier one.

    Two SEC filings by one registrant for one transaction are not two measurements. They are not
    byte-identical -- an 8-K and its exhibit differ in wrapper -- so a hash comparison misses them;
    what identifies them is the operative clause appearing verbatim in both. Found live: v015342
    and v016071_8-k, same Nevada registrant (file 0-25853), same clause, both computing to $4.50.
    Counting both would inflate n and double-weight one legal fact."""
    keep = [r for r in rows if r["verdict"] == "CANDIDATE"]
    texts = {r["doc"]: docs[r["doc"]].read_text(errors="ignore") for r in keep}
    seen: List[str] = []
    dropped = 0
    for r in keep:
        probe = " ".join(r["multiple_quote"].split())[:80]
        dup = next((s for s in seen
                    if probe and probe in " ".join(texts[s].split())
                    and abs((r["answer"] or 0) - (next(
                        k["answer"] for k in keep if k["doc"] == s) or 0)) < 1e-9), None)
        if dup:
            r.update(verdict="EXCLUDE",
                     reason=f"restates the same provision as {dup} (same operative clause and "
                            "the same computed answer) - duplicate filing, not a second item")
            dropped += 1
        else:
            seen.append(r["doc"])
    return dropped


def write_sheet(rows: List[Dict[str, Any]], out_dir: Path) -> Dict[str, Any]:
    """The ORACLE VERIFICATION sheet. Deterministic arithmetic is not a ground truth: a human must
    confirm that the extracted multiple and price are the operative ones for the series in question
    before any of this enters the benchmark. `oracle_ok` is the column Eikiyo fills."""
    out_dir.mkdir(parents=True, exist_ok=True)
    keep = [r for r in rows if r["verdict"] == "CANDIDATE"]
    T.write_csv(out_dir / "candidates_2a.csv",
                ["doc", "verdict", "reason", "n_multiples", "n_oips", "multiple", "oip",
                 "computed_answer", "multiple_quote", "oip_quote", "window_chars"],
                [[r["doc"], r["verdict"], r["reason"], r["n_multiples"], r["n_oips"],
                  T.fmt(r["multiple"], 2), T.fmt(r["oip"], 6), T.fmt(r["answer"], 6),
                  r["multiple_quote"], r["oip_quote"], r["window_chars"]] for r in rows])
    T.write_csv(out_dir / "oracle_sheet_2a.csv",
                ["doc", "multiple_quote", "oip_quote", "multiple", "oip", "computed_answer",
                 "oracle_ok", "corrected_answer", "notes"],
                [[r["doc"], r["multiple_quote"], r["oip_quote"], T.fmt(r["multiple"], 2),
                  T.fmt(r["oip"], 6), T.fmt(r["answer"], 6), "", "", ""] for r in keep])
    reasons: Dict[str, int] = {}
    for r in rows:
        if r["verdict"] == "EXCLUDE":
            reasons[r["reason"].split(" (")[0].split(" -")[0]] = 1 + reasons.get(
                r["reason"].split(" (")[0].split(" -")[0], 0)
    return {"n_docs": len(rows), "n_candidates": len(keep),
            "n_excluded": len(rows) - len(keep), "exclusion_reasons": reasons,
            "distinct_answers": len({r["answer"] for r in keep})}


def selftest() -> str:
    """Prove the ambiguity gate REJECTS the multi-series case it exists for, and ACCEPTS a clean
    one. A gate proven only on good input has not been proven at all."""
    clean = "the Original Issue Price of $1.50 per share ... two times the Original Issue Price"
    assert _verdict(find_multiples(clean), find_oips(clean))[0] == "CANDIDATE", \
        "a single-series document must be accepted"
    multi = ("Series A Original Issue Price of $1.50 per share; the Series B Original Issue Price "
             "of $2.75 per share ... two times the Original Issue Price")
    v, why = _verdict(find_multiples(multi), find_oips(multi))
    assert v == "EXCLUDE" and "ambiguous" in why, f"a two-series document must be excluded: {why}"
    two_mult = ("Original Issue Price of $1.50 ... two times the Original Issue Price ... "
                "three times the Original Issue Price")
    assert _verdict(find_multiples(two_mult), find_oips(two_mult))[0] == "EXCLUDE", \
        "two distinct multiples must be excluded"
    assert _verdict([], [])[0] == "EXCLUDE", "an empty document must be excluded, never accepted"
    assert _verdict([(2.0, "q")], [])[1].startswith("a liquidation multiple"), \
        "each rejection must carry a SPECIFIC reason, not a bare count"
    # The role gate is proven against the REAL corpus text it was written for, verbatim, not an
    # invented example -- a gate that only rejects a strawman has not been shown to work.
    real_cap = ("until, with respect to each series of Preferred Stock, the holders thereof have "
                "received two times the Original Issue Price applicable to such series of "
                "Preferred Stock (the “ Participation Cap ”)")
    real_max = ("shall exceed three (3) times the Original Issue Price applicable to such series "
                "of Preferred Stock ... (the “ Maximum Participation Amount ”)")
    real_ipo = ("for a price per share of not less than three (3) times the original issue price "
                "per share of the Series A Preferred Stock ($1.50 per share) ... (a \"Qualified "
                "IPO\")")
    for name, txt in (("1556898 participation cap", real_cap),
                      ("1722271 maximum participation amount", real_max),
                      ("v015342 qualified-IPO threshold", real_ipo)):
        ok, why = role_check(txt)
        assert not ok, f"the role gate must REJECT the real {name}, but it passed"
    real_pref = ("the holders of the Series B Preferred Stock are entitled to receive out of the "
                 "available assets of the corporation, prior and in preference to any distribution "
                 "to the holders of Series A and common stock an amount per share equal to two "
                 "times the original issue price of $1.00 per share")
    ok, why = role_check(real_pref)
    assert ok, f"the role gate must ACCEPT a real liquidation preference clause, but rejected: {why}"
    return ("prospect selftest PASS - accepts a clean single-series document, rejects two-series "
            "and two-multiple documents by name, rejects the empty case, reasons are specific")
