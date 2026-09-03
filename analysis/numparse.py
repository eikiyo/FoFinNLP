"""
Location: paper-a/analysis/numparse.py
Purpose: Read the numeric VALUES a passage states, not the digit strings it contains. A filing
         writes sixty-eight million dollars as "$68 Million", a share count as "1,362,500
         thousand" and a board seat as "one member", so a literal substring test for 68000000
         finds nothing and reports a stated answer as absent. That false rejection is what this
         module exists to prevent; windowability.norm_num stays the single canonical form.
Functions: literal(), scaled(), spelled(), values(), states(), selftest()
Calls: windowability.norm_num (the ONE numeric canonicaliser, never re-derived)
Imports: re, typing, windowability
"""

import re
from typing import Any, List, Optional, Set

import windowability as W

# Spelled-out numerals a filing actually uses. Deliberately small: every word here is a word a
# drafter writes INSTEAD of a digit, so adding a near-miss ("several", "a majority of") would
# invent a value the document does not state.
UNITS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
         "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
         "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
         "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
         "seventy": 70, "eighty": 80, "ninety": 90}
SCALE = {"hundred": 100, "thousand": 1000, "million": 1000000, "billion": 1000000000}
TOKEN = re.compile(r"[A-Za-z]+|\d[\d,]*(?:\.\d+)?")


def literal(token: str) -> Optional[float]:
    """The value of a digit token, or None when the token is a word."""
    try:
        return float(token.replace(",", ""))
    except ValueError:
        return None


def scaled(tokens: List[str], i: int, value: float) -> Optional[float]:
    """The value implied by a digit token followed by a scale word: 68 "Million" -> 68000000.

    Both readings are kept by the caller, never just the scaled one. "1,362,500 thousand shares"
    is a table written in thousands, and the quantity meant may be either the printed figure or
    the multiplied one; deciding for the document would manufacture a value it does not state."""
    nxt = tokens[i + 1].lower() if i + 1 < len(tokens) else ""
    return value * SCALE[nxt] if nxt in SCALE else None


def spelled(tokens: List[str]) -> Set[float]:
    """Every value written out in words. "one hundred" is 100, "twenty" is 20, and a run ends at
    the first token that is neither a unit nor a scale word."""
    out: Set[float] = set()
    acc, seen = 0.0, False
    for tok in tokens:
        low = tok.lower()
        if low in UNITS:
            acc, seen = acc + UNITS[low], True
        elif low in SCALE and seen:
            acc = (acc or 1) * SCALE[low]
            out.add(acc)
        else:
            if seen:
                out.add(acc)
            acc, seen = 0.0, False
    if seen:
        out.add(acc)
    return out


def values(text: str, words: bool = True) -> Set[str]:
    """Every numeric value the text states, canonicalised by windowability.norm_num.

    `words=False` drops the spelled-numeral pass. That switch is not decoration: "one" and "five"
    occur in prose that states no quantity ("one of the parties"), so a small integer answer can
    be matched by a coincidence. Running the analysis both ways is the only way to show a finding
    does not rest on that, and the sensitivity arm is reported beside the headline."""
    tokens = TOKEN.findall(text or "")
    found: Set[float] = set()
    for i, tok in enumerate(tokens):
        val = literal(tok)
        if val is None:
            continue
        found.add(val)
        mult = scaled(tokens, i, val)
        if mult is not None:
            found.add(mult)
    if words:
        found |= spelled(tokens)
    return {W.norm_num(str(v)) for v in found}


def states(answer: Any, text: str, words: bool = True) -> Optional[bool]:
    """Tri-state: does the text state this answer outright? None means UNDECIDABLE, not False.

    Only a numeric answer is decidable this way, for the reason windowability.answer_present
    already gives: a categorical answer's word sits in the sentence offering the choice, so
    reading its presence as 'the answer is stated' would certify the corpus's most ambiguous
    items as its least ambiguous. An undecidable item is reported as undecidable and never
    silently counted as a failure."""
    if answer in (None, "") or isinstance(answer, bool) or not isinstance(answer, (int, float)):
        return None
    return W.norm_num(str(answer)) in values(text, words=words)


def _st_surface_forms() -> None:
    """The seven shapes this module was written against, taken from the corpus and not invented.
    Each is a value a literal digit-string search reports as absent."""
    cases = [("at a Post-Money Valuation of $68 Million", 68000000),
             ("convertible into one hundred shares of Common Stock", 100),
             ("will have the right to designate up to five nominees", 5),
             ("the first Qualified Financing of at least $10 million", 10000000),
             ("the Discount Rate is Eighty Percent (80%)", 80),
             ("convertible into one fully paid and nonassessable share", 1),
             ("based on 1,362,500 thousand shares of common stock", 1362500000)]
    for text, want in cases:
        assert states(want, text) is True, f"{want} is stated by {text!r} and was not found"


def _st_negative() -> None:
    """The other arm. A parser generous enough to read '$68 Million' must still refuse a value the
    passage does not state, or it certifies every window and discriminates nothing."""
    assert states(68000000, "at a post-money valuation of $75 million") is False, \
        "a different value must not match"
    assert states(0.909, "issue and sell 2,500,000 shares of Series AA Preferred at $0.24") \
        is False, "an answer from another item's window must not match"
    assert states(100, "convertible into shares of Common Stock") is False, \
        "a scale word with no unit before it states nothing"
    assert states(True, "one share") is None and states(None, "one") is None, \
        "a boolean or blank answer is UNDECIDABLE, never False"
    assert states("convert", "the investor may convert") is None, \
        "a categorical answer stays undecidable, as windowability.answer_present holds"


def _st_words_switch() -> None:
    """The sensitivity switch must actually change the reading, or reporting it proves nothing."""
    assert states(5, "designate up to five nominees", words=True) is True
    assert states(5, "designate up to five nominees", words=False) is False, \
        "words=False must drop the spelled-numeral pass, or the sensitivity arm is a no-op"
    assert states(68000000, "$68 Million", words=False) is True, \
        "the scale-word pass is not the word pass and must survive words=False"


def selftest() -> str:
    _st_surface_forms()
    _st_negative()
    _st_words_switch()
    return ("numparse selftest PASS - reads the seven real surface forms a digit-string search "
            "misses, refuses a value the passage does not state (including another item's "
            "answer), holds a categorical or boolean answer undecidable rather than False, and "
            "the words=False sensitivity switch demonstrably changes the reading")


if __name__ == "__main__":
    print(selftest())
