"""
Location: paper-a/analysis/quotematch.py
Purpose: Decide whether a stored validating quote is PRESENT in a given text, and say WHY when it
         is not. Split out of oracle_audit because the same decision is needed in three places --
         the window check, the source-document check, and the EDGAR probe of items with no local
         full text -- and because the previous inline version could not succeed on some inputs at
         all, so it reported a property of itself as a finding about the data.
Functions: spans(), tail_variant(), find_span(), present(), selftest()
Calls: oracle_audit.norm (the ONE normaliser, so matching and resolution cannot disagree)
Imports: re, typing
"""

import re
from typing import List, Optional, Tuple

import oracle_audit as OA

# A validating quote is sometimes a COMPOSITE: several contiguous spans of the source, separated
# because the evidence is not contiguous in the document. Three conventions are in use, and all
# three mean "these spans are each present", never "this exact string is present":
#   ...   an ellipsis, for an abridged single passage;
#   |     a pipe, for two citations from different parts of one filing (the internal-inconsistency
#         tasks quote a capitalisation table AND a balance sheet);
#   [ ]   a bracketed editorial interpolation, words the annotator INSERTED for readability
#         ('[if] converted'). By the convention's own meaning the bracketed text is NOT in the
#         source, so it separates two source spans exactly as an ellipsis does.
SEP = r"\s*(?:\.\.\.|…|\||\[[^\]]*\])\s*"

# A span shorter than this is a connective, not evidence: ', the cash value' and 'participate' are
# fragments of an abridged passage whose substance lives in its longer spans. So a composite is
# judged on its SUBSTANTIVE spans. The floor never refuses a check outright -- when a quote has no
# substantive span at all, every span it does have is required, because they are all the evidence
# there is. That is how `<item>06b</item>` (16 characters, and exactly the evidence a Form D task
# rests on) stays checked, while an ellipsis-abridged clause is not failed on its punctuation.
SHORT_SPAN = 40

# When EVERY span is short, they must also land inside one passage of this many characters. A
# 64,000-character filing contains '$0.51' by chance; two such hits pages apart are two
# coincidences, not a located quote. Sized to a long paragraph or a flattened table block.
PROXIMITY = 1200


def spans(quote: str) -> List[str]:
    """The contiguous spans a validating quote asserts are present.

    A single-element list for an ordinary quote. The raw joined string is never matched for a
    composite: it contains a separator that appears nowhere in any source document, so matching it
    cannot succeed, and a check that cannot succeed reports its own construction as a defect in
    the data. That is how five items whose evidence was fully inside the window came to be counted
    as evidence that fell outside it."""
    return [p.strip() for p in re.split(SEP, quote or "") if p.strip()]


def tail_variant(span: str) -> Optional[str]:
    """The span minus a trailing partial word, or None when that is not a meaningful variant.

    Some quotes are truncated at a storage limit and end mid-word ('if all shares o'), so the
    stored text is not a substring of its own source. Dropping the final token rescues those. It is
    a FALLBACK, never the primary form: applied unconditionally it fires on 423 of 470 quotes and
    silently shortens the needle on almost every check in the corpus, which weakens a presence
    verdict everywhere to rescue a handful of cases."""
    body = span.rstrip()
    cut = body.rfind(" ")
    if cut <= 0:
        return None
    short = body[:cut]
    return short if len(short) >= 12 else None


def find_span(span: str, hay_norm: str) -> Tuple[bool, bool]:
    """(found, via_tail_variant) for one span against already-normalised text."""
    if OA.norm(span) in hay_norm:
        return True, False
    tail = tail_variant(span)
    if tail and OA.norm(tail) in hay_norm:
        return True, True
    return False, False


def locate(span: str, hay_norm: str) -> List[int]:
    """Every offset at which a span occurs. Used only to test proximity, so all hits are needed --
    the nearest pairing is what matters, not the first."""
    needle = OA.norm(span)
    if not needle:
        return []
    out, i = [], hay_norm.find(needle)
    while i != -1:
        out.append(i)
        i = hay_norm.find(needle, i + 1)
    return out


def proximate(parts: List[str], hay_norm: str, window: int = PROXIMITY) -> Tuple[bool, str]:
    """Do all-short spans occur close enough together to be ONE passage rather than coincidences?

    A five-character span like '$0.51' appears somewhere in any long valuation document by chance,
    so a set of short spans matching in a 64,000-character filing is not evidence that the item's
    evidence is there. Requiring them inside one window converts a lucky pair of hits into a
    located passage. Applied ONLY when no span reaches the evidence floor: a long span identifies
    its own location, and demanding proximity of a genuinely abridged quote whose spans are pages
    apart would reject a correct quote for being long."""
    hits = [locate(p, hay_norm) for p in parts]
    if any(not h for h in hits):
        return False, "a span does not occur at all"
    for anchor in hits[0]:
        if all(any(abs(x - anchor) <= window for x in h) for h in hits):
            return True, f"all spans within {window} characters of one another"
    spread = max(max(h) for h in hits) - min(min(h) for h in hits)
    return False, (f"spans occur but span {spread} characters, beyond the {window}-character "
                   f"passage window, so they are separate coincidences rather than one location")


def required_spans(parts: List[str]) -> Tuple[List[str], bool]:
    """The spans a verdict may rest on, and whether the floor was reached.

    Substantive spans when there are any, otherwise every span. The fallback is what keeps the
    rule from quietly becoming unsatisfiable: a quote made entirely of short spans would otherwise
    have nothing to check, and 'nothing to check' would be reported as though the corpus, rather
    than the rule, were at fault."""
    subs = [p for p in parts if len(p) >= SHORT_SPAN]
    return (subs, True) if subs else (parts, False)


def present(quote: str, hay_norm: str) -> Tuple[Optional[bool], str, Optional[int]]:
    """(verdict, reason, shortest span judged). Verdict None means NOT CHECKABLE, which is a
    different fact from False and is never counted as a failure.

    The reason is returned per call rather than logged as a count, because a rejection reported
    only as a count cannot be audited, and every defect this module was written to repair
    announced itself in the reason it would have printed."""
    parts = spans(quote)
    if not parts:
        return None, "no validating quote stored", None
    req, substantive = required_spans(parts)
    shortest = min(len(p) for p in req)
    for i, p in enumerate(req, 1):
        found, _ = find_span(p, hay_norm)
        if not found:
            where = f"span {i} of {len(req)}" if len(req) > 1 else "the quote"
            return False, f"{where} not found: {p[:60]!r}", shortest
    kind = f"all {len(req)} span(s) present" if len(parts) > 1 else "quote present"
    if not substantive and len(req) > 1:
        near, why = proximate(req, hay_norm)
        if not near:
            return False, f"every span is short and they are not one passage: {why}", shortest
        kind += (f"; no span reaches the {SHORT_SPAN}-char evidence floor, so every span was "
                 f"required and checked for proximity ({why})")
    elif not substantive:
        kind += (f"; the single span is {shortest} chars, below the {SHORT_SPAN}-char "
                 f"evidence floor")
    elif len(req) < len(parts):
        kind += f"; {len(parts) - len(req)} sub-{SHORT_SPAN}-char connective span(s) not required"
    return True, kind, shortest


HAY = ("The Company had 94,318,590 shares issued and outstanding, actual, as shown, "
       "and the balance sheet reports 94,191,508 shares as of December 31, 2020.")


def _st_verdicts() -> None:
    """Present, absent, and not-checkable must be three distinguishable outcomes, each with a
    reason that names its cause rather than only counting it."""
    hay = OA.norm(HAY)
    ok, why, _ = present("94,318,590 shares issued and outstanding, actual", hay)
    assert ok is True, why
    bad, why, _ = present("100,000,000 shares issued and outstanding, actual", hay)
    assert bad is False and "not found" in why, f"a genuinely absent quote must be False: {why}"
    assert "100,000,000" in why, f"the reason must name what was missing, not just count it: {why}"
    none_v, why, _ = present("", hay)
    assert none_v is None, f"an empty quote is NOT CHECKABLE, never a failure: {why}"


def _st_composite() -> None:
    """The load-bearing arm: a real corpus composite whose JOINED string appears nowhere. This is
    what the previous implementation matched, so this test is red against it, which is the only
    way the repair is demonstrated rather than asserted."""
    hay = OA.norm(HAY)
    comp = "94,318,590 shares issued and outstanding, actual | 94,191,508 shares as of December 31"
    assert OA.norm(comp) not in hay, "fixture is wrong: the joined composite must NOT appear"
    ok, why, _ = present(comp, hay)
    assert ok is True, f"a composite whose spans are all present must PASS: {why}"
    absent = "777,777,777 shares reserved for issuance under the 2019 equity incentive plan"
    ok, why, _ = present(f"94,318,590 shares issued and outstanding, actual | {absent}", hay)
    assert ok is False and "span 2 of 2" in why and "777,777,777" in why, \
        f"a partly-absent composite must fail, naming the missing span: {why}"


def _st_conventions() -> None:
    """Storage truncation and editorial interpolation are QUOTING CONVENTIONS. Failing an item on
    either reports the annotator's notation as a defect in the corpus."""
    trunc = OA.norm("would have received if all shares of Preferred Stock had converted")
    ok, why, _ = present("would have received if all shares o", trunc)
    assert ok is True, f"a truncated quote must still match via its tail variant: {why}"
    assert tail_variant("oneword") is None, "a single token has no meaningful tail variant"
    assert spans("the cash value [if] converted into shares") == \
        ["the cash value", "converted into shares"], spans("the cash value [if] converted into")
    interp = OA.norm("the cash value converted into shares of Class A Common Stock")
    ok, why, _ = present("the cash value [if] converted into shares", interp)
    assert ok is True, f"an interpolated quote must not fail on the interpolation: {why}"


def _st_short_spans() -> None:
    """A short span is judged, never refused, but a set of them must be ONE passage: '$124.3'
    turns up by chance in any long filing, so scattered hits are coincidences, not a location."""
    short_hay = OA.norm("Implied Total Enterprise Value: $124.3 million, and no range is stated.")
    ok, why, _ = present("Implied Per Share Reference Range ... $0.51", short_hay)
    assert ok is False and "not found" in why, \
        f"an all-short composite whose evidence is absent must still FAIL: {why}"
    ok, why, _ = present("Implied Total Enterprise Value ... $124.3", short_hay)
    assert ok is True and "proximity" in why, \
        f"an all-short composite present in ONE passage must pass, noting proximity: {why}"
    scattered = OA.norm("Implied Total Enterprise Value of the segment. " + ("filler text " * 400)
                        + " a reference price of $124.3 per unit was noted.")
    ok, why, _ = present("Implied Total Enterprise Value ... $124.3", scattered)
    assert ok is False and "not one passage" in why, \
        f"short spans pages apart must NOT count as the quote being present: {why}"
    assert proximate(["alpha", "omega"], OA.norm("alpha " + "x " * 50 + " omega"))[0] is True, \
        "two short spans inside one passage must read as proximate"
    xml = OA.norm("<offeringData><item>06b</item></offeringData>")
    ok, why, n = present("<item>06b</item>", xml)
    assert ok is True and n == 16, f"a short but real single-span quote must PASS: {why}"
    assert present("<item>06c</item>", xml)[0] is False, \
        "and the same check must still detect the WRONG short element"


def selftest() -> str:
    """Prove the matcher BOTH ways, and prove it goes red on the corruption already in the data."""
    _st_verdicts()
    _st_composite()
    _st_conventions()
    _st_short_spans()
    return ("quotematch selftest PASS - present/absent/not-checkable are three outcomes with named "
            "reasons, a composite passes on its spans and fails naming the missing one, truncation "
            "and editorial interpolation are handled as the conventions they are, and short spans "
            "are judged but required to form one passage rather than scattered coincidences")
