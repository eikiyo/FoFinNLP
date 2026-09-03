"""
Location: paper-a/analysis/windowability.py
Purpose: Separate the two populations the window check collapses together. "The validating quote is
         not verbatim in the window" has two very different causes: the evidence is genuinely
         missing (a provenance failure, repairable by re-windowing), or the item is COMPUTATIONAL --
         every operand is in the window and the stored quote is the annotator's own derivation, so
         no verbatim span could ever exist. Both are unstable, for unrelated reasons, and reporting
         them as one number would attribute a computation effect to a provenance defect.
Functions: numeric_tokens(), norm_num(), answer_present(), operands_present(), classify(),
           classify_rows(), selftest()
Calls: oracle_audit.norm (the ONE normaliser)
Imports: re, typing
"""

import re
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

import oracle_audit as OA

# A number as it appears in a filing: optional currency, thousands separators, optional decimals.
NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
# Below this a token is not evidence of anything -- '0', '1' and '2' occur in every document.
MIN_NUM = 3


def norm_num(tok: str) -> str:
    """A numeric token in one canonical form, so '1,362,500' and '1362500' compare equal, and
    '2.40' and '2.4' do too. Trailing-zero stripping matters: a percentage stored as 2.40 and
    printed as 2.4 is the same number, and treating it as absent would invent a provenance
    failure out of a formatting choice."""
    t = tok.replace(",", "")
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    return t or "0"


def all_numbers(text: str) -> Set[str]:
    """Every number in a text, canonicalised. No floor: used when looking for ONE known value,
    where a short token is not noise but the thing being sought."""
    return {norm_num(m.group()) for m in NUM.finditer(text or "")}


def numeric_tokens(text: str) -> Set[str]:
    """Every number, canonicalised, minus tokens too short to identify anything. The floor belongs
    here and ONLY here: it keeps '(i)' and 'section 12' out of an OPERAND set, where a coincidental
    match would wrongly certify a window as self-sufficient. Applied to an answer lookup it would
    instead blind the search to every small value -- a 2.4% answer would be unfindable, and the
    item would be reported as computational when its answer is stated outright."""
    return {n for n in all_numbers(text) if len(n.replace(".", "")) >= MIN_NUM}


def answer_present(answer: Any, window: str) -> Optional[bool]:
    """Is the oracle's own answer stated OUTRIGHT in the window? None when that cannot be decided.

    Only NUMERIC answers are decidable this way. A categorical answer is a label from a small
    enum, and its word almost always occurs in a window that discusses the choice at all: a
    convert-or-take-preference scenario contains the word 'convert' in the sentence offering the
    option, and a participation clause contains 'participate' while saying the opposite. Reading
    that as 'the answer is stated' would certify the most ambiguous items in the corpus as the
    least ambiguous. Undecidable is reported as undecidable."""
    if answer in (None, "") or isinstance(answer, bool):
        return None                       # a boolean is a judgement, never a literal in the text
    if isinstance(answer, (int, float)):
        return norm_num(str(answer)) in all_numbers(window)
    return None


def operands_present(quote: str, answer: Any, window: str) -> Tuple[bool, Set[str]]:
    """Are the quote's numbers -- other than the answer itself -- all in the window?

    This is what distinguishes a computational item from a missing one. The annotator's derivation
    ('33,184 thousand shares of 1,362,500 thousand total = 2.4%') names its inputs, and when every
    input is in the window the model was given everything it needed and had to do arithmetic, not
    guess. Returns the missing tokens so a rejection can name them."""
    ans = {norm_num(str(answer))} if isinstance(answer, (int, float)) and \
        not isinstance(answer, bool) else set()
    need = numeric_tokens(quote) - ans
    have = numeric_tokens(window)
    missing = need - have
    return (bool(need) and not missing), missing


def classify(answer: Any, quote: str, window: str) -> Tuple[str, str]:
    """(bucket, reason) for one item whose quote is not verbatim in its window.

    Ordered most-informative first: an answer stated outright settles it, then a fully-supplied
    derivation, and only when neither holds is the evidence genuinely absent."""
    if answer_present(answer, window):
        return ("answer-stated",
                "the oracle answer appears in the window; only the stored quote's WORDING differs")
    ok, missing = operands_present(quote, answer, window)
    if ok:
        return ("computational",
                "every operand of the stored derivation is in the window; the answer must be "
                "computed, not located, so no verbatim span can exist")
    if missing:
        return ("evidence-absent",
                f"operands absent from the window: {sorted(missing)[:4]}")
    return ("evidence-absent",
            "neither the answer nor any operand of the stored quote is in the window")


def classify_rows(rows: Sequence[Dict[str, Any]], windows: Dict[str, str],
                  quotes: Dict[str, str]) -> List[Dict[str, Any]]:
    """Classify every row whose window check came back False. Rows are keyed by (leaf, item)."""
    out = []
    for r in rows:
        if r.get("quote_in_window") is not False:
            continue
        key = (r["leaf"], r["item"])
        bucket, why = classify(r.get("answer"), quotes.get(key, ""), windows.get(key, ""))
        out.append(dict(r, bucket=bucket, bucket_reason=why))
    return out


UBER_WIN = ("Applicable percentage ownership is based on 1,362,500 thousand shares of common "
            "stock outstanding. Name of Beneficial Owner: Ryan Graves Shares (in thousands): "
            "33,184")
UBER_Q = "Ryan Graves: 33,184 thousand shares of 1,362,500 thousand total = 2.4%"


def _st_buckets() -> None:
    """The load-bearing case: a window supplying both operands of a percentage must NOT be called
    a provenance failure. Calling it one attributes an arithmetic effect to a defect in the
    resource, which is the exact misreading this module exists to prevent. Removing an operand
    must flip it, or the classifier is not discriminating, only agreeing."""
    b, why = classify(2.4, UBER_Q, UBER_WIN)
    assert b == "computational", f"both operands present must read as computational: {b} / {why}"
    b2, why2 = classify(2.4, UBER_Q, UBER_WIN.replace("33,184", "redacted"))
    assert b2 == "evidence-absent", f"removing an operand must flip the bucket: {b2}"
    assert "33184" in why2, f"the reason must name the missing operand: {why2}"
    b3, _ = classify(2.4, UBER_Q, UBER_WIN + " representing 2.4% of the outstanding shares.")
    assert b3 == "answer-stated", f"a stated answer must be recognised: {b3}"


def _st_categorical() -> None:
    """A categorical answer whose WORD appears in the window is not thereby stated: the word sits
    in the sentence offering the choice. Certifying that would mark the corpus's most ambiguous
    items as its least ambiguous."""
    b4, _ = classify("convert", "the investor would elect to convert",
                     "the investor can have the amount returned, or convert into shares")
    assert b4 == "evidence-absent", f"a categorical word in the scenario is not the answer: {b4}"
    assert answer_present("convert", "or convert into shares") is None, \
        "a categorical answer must be UNDECIDABLE by literal presence, not True"
    b5, _ = classify("capped", "holders receive three times", "no such language appears here")
    assert b5 == "evidence-absent", f"a categorical answer genuinely absent: {b5}"
    assert answer_present(True, "anything") is None, \
        "a boolean answer is a judgement and must not be looked up as a literal"


def _st_formatting() -> None:
    """Formatting must manufacture a failure in neither direction, and the operand floor must not
    leak into the answer lookup, where a small value is the thing being sought rather than noise."""
    assert norm_num("1,362,500") == norm_num("1362500") == "1362500", "separators must normalise"
    assert norm_num("2.40") == norm_num("2.4") == "2.4", "trailing zeros must normalise"
    assert answer_present(2.4, "the figure is 2.40 percent") is True, \
        "a differently-formatted answer must still be found"
    assert "12" not in numeric_tokens("section 12 of the Act"), \
        "a token below the identifying floor must not count as an operand"
    assert "2.4" in all_numbers("the figure is 2.4 percent"), \
        "the answer lookup must NOT inherit the operand floor, or small answers become invisible"


def selftest() -> str:
    """Prove the buckets separate on the REAL shapes in the corpus, not on invented ones."""
    _st_buckets()
    _st_categorical()
    _st_formatting()
    return ("windowability selftest PASS - a window supplying both operands reads as computational "
            "and flips to evidence-absent when one is removed (naming it), a numeric answer stated "
            "outright is recognised while a categorical one is held undecidable, and formatting "
            "differences manufacture a failure in neither direction")
