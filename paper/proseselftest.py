"""
Location: paper-a/paper/proseselftest.py
Purpose: The proof that the prose rules actually fire. Split from prosecheck.py at its 300-LOC
         budget, following the leakscan.py/leakselftest.py split already used in this tree. Every arm
         asserts BOTH directions -- fires on a violation, silent on the paper's real sentences --
         because a rule relaxed to stop a false red is only safe if it still goes red on the real
         thing.
Functions: selftest()
Calls: prosecheck.{banned_hits,internal_words,dashes,mechanism_hits,missing_topics,body,
       second_reader_hits,cacioli_gaps} -- the vocabulary lives there
Imports: pathlib, prosecheck
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from prosecheck import (BANNED, MECHANISM_BANNED, LIMIT_TOPICS, SECOND_READER, banned_hits,  # noqa: E402
                        internal_words, dashes, mechanism_hits, missing_topics, body,
                        second_reader_hits, cacioli_gaps, full_scope, inputs)


def selftest() -> str:
    """Prove each rule fires on a violation AND stays quiet on clean text. A relaxation made to
    stop a false red is only safe if the rule still goes red on the real thing, so both arms are
    asserted for every rule rather than just the convenient one."""
    doc = r"\begin{document}" + " A clean sentence about tasks and configurations. "
    assert banned_hits(doc) == [] and not internal_words(doc) and dashes(doc) == []
    assert banned_hits("this is a novel result") == [r"novel\b"], "a banned word must be caught"
    assert internal_words("the leaf was scored"), "'leaf' must be caught"
    # The mechanism ban, now document-wide, proved in BOTH directions in every section it used to
    # be blind to. A checker that never fires is the failure this one was written to fix: the style
    # list said "0 of 22 banned phrases" for a paper whose title carried a retired mechanism claim,
    # because that phrase had never been on any list.
    doc = ("\\begin{document} \\begin{abstract} A is B. \\end{abstract} "
           "\\section{Introduction} P is Q. \\section{The benchmark} C is D. "
           "\\section{Conclusion} E is F. \\end{document}")
    assert mechanism_hits(doc) == [], "clean prose must not fire"
    for where, clean in (("Introduction", "P is Q."), ("The benchmark", "C is D."),
                         ("Conclusion", "E is F."), ("abstract", "A is B.")):
        hit = mechanism_hits(doc.replace(clean, "It is unanswerable by construction."))
        assert hit == [MECHANISM_BANNED[0]], f"the ban must reach the {where}, got {hit}"
    assert mechanism_hits(doc.replace("A is B.", "This forces the model to guess.")) == \
        [MECHANISM_BANNED[1]], "and must name which phrase fired"
    # The legitimate sentence the loose-regex version of this check would have destroyed. It must
    # stay green, or the gate's cheapest path to passing is deleting a true statement.
    ok = doc.replace("A is B.", "Whether the evidence causes the instability was registered as a "
                     "falsifiable prediction, and it failed.")
    assert mechanism_hits(ok) == [], "a negated causal frame is permitted and must not fire"
    # SystemExit IS the pass condition here, so it is recorded and asserted on rather than
    # swallowed: the call must fail closed on a document whose body parsed to nothing.
    failed_closed = False
    try:
        mechanism_hits("\\section{Nothing} x")
    except SystemExit:
        failed_closed = True
    assert failed_closed, "a document with no body must fail closed, not return no hits"
    # Cacioli: distinguished, merely cited, and absent section must read differently.
    good = ("\\section{Related work} Cacioli measures the change in correctness; we measure "
            "instability, so they are different constructs. \\section{Next}")
    assert cacioli_gaps(good) == [], "a real distinction must pass"
    assert "construct" in cacioli_gaps(good.replace("different constructs", "different things")), \
        "a bare citation without the construct contrast must not pass"
    assert cacioli_gaps("\\section{Nothing} x") == ["no section"], \
        "a missing related-work section must never read as satisfied"
    assert dashes("a---b") == ["'---'"], "an em-dash must be caught"
    # The second-reader rule, both arms. The NEGATIVE arm matters more than the positive one here:
    # these are real sentences from the paper and the data statement, every one of them true, and a
    # rule that fired on any of them would be an instruction to delete an honest limitation.
    for legit in ("One annotator produced every label.",
                  "a single annotator produced every oracle label",
                  "There is no second reading and this paper reports no inter- or intra-annotator "
                  "agreement coefficient.",
                  "released so a second reader can be run by anyone",
                  "which makes a label traceable to a document, not a substitute for a second "
                  "annotator",
                  "only an independent reader yields inter-annotator agreement",
                  "the result is intra-annotator agreement and must be reported in those words",
                  "the 7 items removed at adjudication were removed by the same person"):
        assert second_reader_hits(legit) == [], f"a true sentence must not fire: {legit!r}"
    for violation, why in (("Two annotators labelled every item.", "plural annotators"),
                           ("inter-annotator agreement was 0.81", "a reported coefficient value"),
                           ("we report Cohen's kappa of 0.79", "a named statistic"),
                           ("every item was double-annotated", "double annotation"),
                           ("a second annotator confirmed the label", "a second reader acting"),
                           ("disagreements were resolved by discussion", "two people conferring"),
                           ("we use consensus labels", "consensus implies two readers")):
        assert second_reader_hits(violation), f"must fire on {why}: {violation!r}"
    assert second_reader_hits("inter-annotator agreement was 0.81") == \
        [r"(?:inter|intra)-annotator agreement (?:was|of|is|reached)\s*[0-9.]"], \
        "and must name which pattern fired, not merely that something did"
    # Wrapped across a line break: present, and must be found.
    wrapped = body(r"\begin{document}" + "\nTwo are quantizations of one base\nmodel, so.\n")
    assert missing_topics(wrapped) != [] , "the other seven topics are genuinely absent here"
    assert "quantization" not in missing_topics(wrapped), \
        "a topic split by a line break must still be found"
    # Genuinely absent: the relaxation above must not have made this permissive.
    assert "quantization" in missing_topics(body(r"\begin{document}" + "\nnothing here.\n")), \
        "an absent topic must still be reported missing"
    return (f"prosecheck selftest PASS - banned words, 'leaf' and dashes each fire on a violation "
            f"and stay quiet on clean text; a topic split by a line break is found, an absent one "
            f"is still reported; and the {len(SECOND_READER)} second-reader patterns fire on 7 "
            f"assertions that a second reader existed while staying silent on all 8 of the paper's "
            f"real, true single-annotator sentences")


if __name__ == "__main__":
    print(selftest())
