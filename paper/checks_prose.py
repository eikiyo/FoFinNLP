"""
Location: paper-a/paper/checks_prose.py
Purpose: The two prose gate lines -- `prose rules` and `single-annotator language` -- as gate
         functions over the rules vocabulary in prosecheck.py. Split out of verify_paper.py (which
         hit its 300-LOC budget) and prosecheck.py, following the checks_*.py convention already
         used by checks_geometry / checks_bundle / checks_pdfset.
Functions: check_prose(), check_second_reader()
Calls: prosecheck.{body,full_scope,mechanism_hits_in,banned_hits,dashes,missing_topics,
       internal_words,cacioli_gaps,second_reader_hits} -- the rules live there, not here
Imports: sys, pathlib, prosecheck

`prosecheck.py` owns WHAT is banned (the phrase lists and the predicates, each with both selftest
arms). This file owns WHERE each ban is enforced, which is the half that was wrong: every rule but
one read main.tex's own bytes, so `sections/data_statement.tex` was exempt from four of them and
shipped four `---` and the internal word "leaves" into the compiled PDF under a green
"no em-dash" line. HERE and TEX are module constants so a positive control can patch them, the same
way checks_geometry's are patched.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import prosecheck as W          # noqa: E402

TEX = HERE / "main.tex"


def check_prose(fail) -> str:
    """Every prose rule over the SUBMITTED prose: main.tex's body plus every \\input-ed section.

    Limitations topics deliberately stay narrow (body only). They are a requirement ON the main-text
    Limitations section, so satisfying one from an appendix mention would be a false green rather
    than a wider check. The other four rules ask "does this string appear in the submitted prose",
    and an \\input-ed section IS submitted prose -- `check_second_reader` below already read the wide
    scope for exactly that reason, and the reasoning was never carried across to its siblings."""
    tex = TEX.read_text()
    body = W.body(tex)
    wide = W.full_scope(HERE, TEX)
    for msg, hits in (("retired mechanism claim anywhere in the document",
                       W.mechanism_hits_in(wide)),
                      ("banned phrasing present", W.banned_hits(wide)),
                      ("em-dash or en-dash present", W.dashes(wide)),
                      ("Limitations does not cover", W.missing_topics(body))):
        if hits:
            fail(f"{msg}: {hits}")
    if W.internal_words(wide):
        fail("the internal word 'leaf' appears in the paper")
    gaps = W.cacioli_gaps(tex)
    if gaps:
        fail(f"Cacioli is not distinguished in the related-work section; missing: {gaps}")
    return (f"0 of {len(W.BANNED)} banned phrases and 0 of {len(W.MECHANISM_BANNED)} retired "
            f"mechanism claims, 0 uses of 'leaf', no em-dash, across {len(wide)} chars of main-text "
            f"body plus every \\input-ed section; all {len(W.LIMIT_TOPICS)} Limitations topics "
            "present in the main text, Cacioli distinguished by construct in related work")


def check_second_reader(fail) -> str:
    """Its own gate line rather than a clause inside the prose check, because a reviewer of this
    repo should be able to see the single-annotator claim pass or fail on its own row."""
    wide = W.full_scope(HERE, TEX)
    hits = W.second_reader_hits(wide)
    if hits:
        fail(f"a phrase implying a second reader existed: {hits}")
    return (f"0 of {len(W.SECOND_READER)} second-reader phrasings across {len(wide)} chars of "
            "main-text body plus every \\input-ed appendix section")
