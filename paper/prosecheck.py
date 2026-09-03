"""
Location: paper-a/paper/prosecheck.py
Purpose: The writing-spec prose rules and the matching against main.tex. Split out of
         verify_paper.py to keep that file inside its LOC budget; the banned list and the
         Limitations topic list live here beside the code that applies them.
Functions: body(), banned_hits(), internal_words(), dashes(), missing_topics(), mechanism_hits(),
           mechanism_hits_in(), full_scope(), inputs(), second_reader_hits(), cacioli_gaps()
Calls: none. The selftest arms live in proseselftest.py (same split as leakscan/leakselftest);
       `python3 paper/prosecheck.py` still runs them, so the documented command is unchanged.
Imports: re, pathlib, typing
"""

import re
from pathlib import Path
from typing import Dict, List

BANNED = [r"we are the first", r"to the best of our knowledge, the first", r"first benchmark",
          r"has been overlooked", r"we introduce run-to-run", r"we introduce split-half",
          r"we propose reporting worst-slice", r"we introduce the worst-category",
          r"understates its worst clause type by", r"the gap grows as models improve",
          r"instability is not merely difficulty", r"never produce silently", r"novel\b",
          r"significant\b", r"crucial\b", r"notably\b", r"importantly\b", r"it is worth noting",
          r"we hope", r"shed light on", r"pave the way", r"delve",
          # Single-author paper. "The authors" is therefore either wrong about its own authorship or
          # a vague reference to someone else's, and it sat in the disclosure paragraph -- the one
          # paragraph a reviewer reads for honesty. Plural-by-default is also a model-prose tell.
          # Safe as an outright ban here because this paper names its sources ("Yagubyan reports")
          # rather than saying "the authors of", so there is no legitimate use to false-red.
          r"\bthe authors\b"]

# Each Limitations item the spec requires, keyed by a phrase that must survive rewording. Keep
# these SHORT: a long pattern is one editing pass away from being broken by a rewrite, and a
# limitation that is present but unmatched reads exactly like one that was dropped.
LIMIT_TOPICS: Dict[str, str] = {
    "single annotator": r"single annotator produced every oracle label",
    "temperature": r"single temperature",
    "routing": r"served through a commercial routing layer",
    "quantization": r"quantizations of one base model",
    "unbalanced categories": r"task counts are unbalanced",
    "shared denominator": r"computed from the same 20 responses",
    "english/US only": r"English-only and drawn from United States",
    "corpus size": r"is a small corpus"}

DASHES = ("---", "—", "–")


def body(tex: str) -> str:
    """Everything after \\begin{document}, with runs of whitespace collapsed to single spaces.

    The collapse is the point. main.tex is hard-wrapped, so every multi-word pattern above is one
    edit away from being split by a line break: rewriting a neighbouring sentence reflowed
    'quantizations of one base model' across two lines and the topic check reported it missing
    while it sat there in plain sight. Matching the raw file measures the line wrapping, not the
    prose."""
    return re.sub(r"\s+", " ", tex.split(r"\begin{document}", 1)[1])


def banned_hits(text: str) -> List[str]:
    return [b for b in BANNED if re.search(b, text, re.I)]


# The three phrasings the repair's null retired, banned in the abstract and Section 2 and nowhere
# else. Section 1 may still say an item is unanswerable by construction, because that is a claim
# about the WINDOW (true and measured: 0 of 8 numeric repairable items had their answer inside it)
# and not about what destabilises the model. Only literal phrases are mechanised here. "Any
# sentence asserting that windowing causes instability" is a semantic judgement no regex can make,
# and a pattern pretending to make it would report a number nobody should trust; it stays a human
# read and is named as one rather than faked.
MECHANISM_BANNED = [r"unanswerable by construction", r"forces the model to guess",
                    r"guessing is maximally unstable"]


def mechanism_scope(tex: str) -> str:
    """The WHOLE document, which is where the final brief puts the ban: "no causal windowing claim
    survives anywhere".

    It used to be the abstract plus Section 2, because Section 1 carried a legitimate use of one
    banned phrase and running the check everywhere would have made deleting a true sentence the
    cheapest way to green. That sentence is now rewritten, so the narrow scope has outlived the
    thing it protected and a scope kept past its reason is a gate that no longer checks what its
    name says.

    Only the three literal phrases are enforced here. The brief also bans "any sentence asserting
    windowing causes instability", which is a semantic property no regex decides: the abstract
    contains the word "causes" inside "whether the missing evidence causes the instability was
    registered as a falsifiable prediction ... and it failed", a sentence the paper needs. A
    pattern loose enough to catch a real causal assertion would reject that one, and a false red
    that deletes a true sentence costs more than the check is worth. That half is enforced by
    reading, and this docstring says so rather than letting the green imply otherwise."""
    flat = re.sub(r"\s+", " ", tex)
    body = re.findall(r"\\begin\{document\}(.*?)\\end\{document\}", flat)
    if not body:
        raise SystemExit("cannot locate the document body in main.tex -- refusing to certify a "
                         "language rule against a region that parsed to nothing")
    return body[0]


def mechanism_hits_in(scope: str) -> List[str]:
    """The predicate, over a scope the caller chose. Split out so the widened scope (body plus every
    \\input-ed section) reuses one definition of the ban instead of a second copy of the loop."""
    return [b for b in MECHANISM_BANNED if re.search(b, scope, re.I)]


def mechanism_hits(tex: str) -> List[str]:
    return mechanism_hits_in(mechanism_scope(tex))


# A single annotator produced every label, so no sentence anywhere may imply a second reader
# existed. The hard part is that the paper says several TRUE things containing the same words --
# "no second reading", "a second reader can be run by anyone", "not a substitute for a second
# annotator", "reports no inter- or intra-annotator agreement coefficient" -- and a rule that fired
# on those would make deleting a true sentence the cheapest way to green. So every pattern requires
# an ASSERTION that a second reader existed or acted: a plural annotator, a reported coefficient
# VALUE, a named agreement statistic, or a second reader taking an action. selftest asserts every
# one of those legitimate sentences stays quiet.
SECOND_READER = [
    r"\btwo annotators\b", r"\bboth annotators\b", r"\bthe annotators\b", r"\bour annotators\b",
    r"\bannotators (?:agreed|disagreed|were)\b",
    r"(?:inter|intra)-annotator agreement (?:was|of|is|reached)\s*[0-9.]",
    r"\bcohen'?s kappa\b", r"\bkrippendorff\b", r"\bfleiss\b", r"\bscott'?s pi\b",
    r"\bdouble[- ]annotated\b", r"\bdoubly annotated\b", r"\bindependently annotated by\b",
    r"\ba second (?:annotator|reader) (?:produced|labelled|labeled|read|reviewed|confirmed|"
    r"agreed|checked|verified)",
    r"\bsecond annotator's\b", r"\bresolved by discussion\b",
    r"\bconsensus (?:label|annotation|answer)s?\b",
    r"\badjudicated by (?:a|the) (?:second|third|independent)\b"]


def full_scope(paper_dir, tex_path=None) -> str:
    """main.tex's body PLUS every \\input-ed section, flattened.

    The existing rules read main.tex alone, which is the file's own bytes -- so an \\input-ed
    appendix section is invisible to them. That was harmless while every \\input was a generated
    table, and stopped being harmless when the data statement arrived as sections/data_statement.tex:
    the one document in this submission most likely to word the annotation limitation loosely was the
    one document no prose rule could see. Tables stay out of scope (their captions are generated),
    so this is deliberately sections/ only, and the count is reported so a silent zero is visible.

    `tex_path` exists so a caller that has already resolved the main file (and a positive control
    that plants its defect in a temp copy) reads the SAME bytes the rest of the gate reads. Defaulting
    it to paper_dir/main.tex would silently ignore a patched path and make that control vacuous."""
    tex_path = tex_path or paper_dir / "main.tex"
    parts = [body(tex_path.read_text())]
    parts += [re.sub(r"\s+", " ", p.read_text()) for p in inputs(paper_dir, tex_path)]
    return " ".join(parts)


def inputs(paper_dir, tex_path=None) -> List[Path]:
    """Every sections/*.tex file main.tex \\input-s, resolved and proven present.

    One definition, three callers: the prose scope, the single-annotator scope, and the FRESHNESS
    check. The third is why this is a function. check_fresh compared the PDF against a hand-listed
    roster (main.tex + tables/*.tex + figures/*.pdf) that predated sections/, so editing an appendix
    section left the gate reporting "newer than all sources" about a PDF that did not contain the
    edit -- the exact failure its own docstring says nothing else can catch. A roster that has to be
    remembered is a roster that goes stale; deriving it from the document cannot."""
    tex_path = tex_path or paper_dir / "main.tex"
    out = []
    for name in re.findall(r"\\input\{(sections/[^}]+)\}", tex_path.read_text()):
        p = paper_dir / (name if name.endswith(".tex") else name + ".tex")
        if not p.exists():
            raise SystemExit(f"main.tex inputs {name} but it is not on disk -- refusing to certify "
                             "a check against a scope that is missing a file it names")
        out.append(p)
    return out


def second_reader_hits(text: str) -> List[str]:
    return [b for b in SECOND_READER if re.search(b, text, re.I)]


# The gate FUNCTIONS that enforce these rules live in checks_prose.py. This file is the vocabulary:
# what is banned, and a selftest proving each predicate fires on a violation and stays quiet on
# clean text. Where each ban applies is a separate decision, and keeping it in a separate file is
# what made it possible to see that four rules were being enforced over a narrower scope than one.


CACIOLI_TERMS = ("cacioli", "change", "instability", "construct")


def cacioli_gaps(tex: str) -> List[str]:
    """What the related-work section is missing for the nearest prior result to count as
    DISTINGUISHED rather than merely cited.

    This lived in verify_paper as "Cacioli appears on page 1", which was true only while related
    work was folded into the introduction. Promoting it to its own section moved the text to page 2
    and the check went red on a paper that had just done what the brief asked: a rule keyed on
    where a sentence landed, not on what it said. Keyed on the construct contrast instead, it
    survives the layout moving again. Returns ["no section"] when the section itself is absent, so
    a missing section can never read as a satisfied rule."""
    rel = re.search(r"\\section\{Related work\}(.*?)\\section\{", tex, re.S)
    if not rel:
        return ["no section"]
    low = rel.group(1).lower()
    return [w for w in CACIOLI_TERMS if w not in low]


def internal_words(text: str) -> bool:
    """True if the internal term for a task leaks into the paper.

    It over-matches ON PURPOSE: "leaves" as an ordinary verb trips it too, and it fired once on
    "dropping each configuration in turn leaves the ratio between 7.9 and 10.4". No regex can tell
    that verb from the noun, and the two readings sit one word apart in a paper whose subject is a
    tree of tasks. The word was reworded rather than the rule narrowed, because the cost of
    avoiding one English verb is nothing and the cost of the jargon reaching a reviewer is a page
    of confusion. If a future sentence genuinely needs the verb, rewrite the sentence."""
    return bool(re.search(r"\bleaf|\bleaves\b", text, re.I))


def dashes(text: str) -> List[str]:
    return [repr(d) for d in DASHES if d in text]


def missing_topics(text: str) -> List[str]:
    return [n for n, pat in LIMIT_TOPICS.items() if not re.search(pat, text, re.I)]


if __name__ == "__main__":
    # Running this file standalone used to print nothing and exit 0. The writing spec lists it as
    # a check that must pass, and a module that passes by having no entry point is the same green
    # as a module that ran and found nothing wrong. The arms live in proseselftest.py (same split as
    # leakscan.py/leakselftest.py); this entry point still runs them so the command is unchanged.
    from proseselftest import selftest
    print(selftest())
