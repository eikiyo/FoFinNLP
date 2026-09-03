"""
Location: paper-a/paper/gate_controls.py
Purpose: W4b.3 -- a POSITIVE CONTROL for every gate in verify_paper.CHECKS. Each control plants the
         exact defect its gate exists to catch and requires the gate to fail; a gate that stays green
         on its own defect is reported as NO CONTROL rather than counted as passing.
         Usage:  python3 paper/gate_controls.py [selftest]
Functions: patched(), tmp_paper(), mutate_*(), CONTROLS, run_all(), selftest()
Calls: verify_paper.CHECKS, gate_fixtures (deliberately-bad PDFs), the real tree -- READ ONLY
Imports: contextlib, re, shutil, subprocess, sys, tempfile, pathlib, verify_paper, checks_geometry

Eighteen green lines say nothing about whether eighteen gates work. Before this file, three of the
eighteen were exercised by a selftest that called the check itself; the rest were covered only
indirectly, through a helper, or not at all. Building the controls found two real defects on the
first run: the serif test matched `NimbusSanL` (Nimbus SANS) and would have passed a figure typeset
entirely in a sans face, and the overprint fixture's first version did not overlap, which would have
made its control silently vacuous.

Nothing here writes to the real tree. Every mutation happens in a temp copy, and the module constants
the gate reads are patched to point at it for the duration of one check.
"""

import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import verify_paper as V          # noqa: E402
import checks_geometry as G       # noqa: E402
import checks_prose as R          # noqa: E402
import checks_cite as C           # noqa: E402
import gate_fixtures as F         # noqa: E402
from gate_fixtures import FIX, patched, tmp_paper, _tex_with   # noqa: E402

# --- one mutation per gate ---------------------------------------------------------------------
def m_fresh(d):
    pdf = d / "main.pdf"
    shutil.copy2(HERE / ".lmk" / "main.pdf", pdf)
    import os
    os.utime(pdf, (0, (HERE / "main.tex").stat().st_mtime - 3600))
    return [(V, "PDF", pdf)]


def m_pages(d):
    shutil.copy2(HERE / ".lmk" / "main.pdf", d / "main.pdf")
    aux = (HERE / ".lmk" / "main.aux").read_text()
    (d / "main.aux").write_text(re.sub(r"(\\newlabel\{mainend\}\{\{[^}]*\}\{)\d+", r"\g<1>9", aux))
    return [(V, "PDF", d / "main.pdf")]


def m_anonymous(d):
    """TWO arms, because the gate now has two: a literal affiliation list and the derived identity
    tokens. The fixture carries one of each, and the selftest requires both messages.

    The identity token is read from the deriver and written into a temp PDF that lives under
    /tmp and is never printed to a log."""
    sys.path.insert(0, str(HERE.parent / "audit"))
    import leaktokens as LT
    root = HERE.parents[4]
    toks = sorted({t for t in LT.tokens(root) | LT._env_identity(root)
                   if len(t) >= 6 and t.isalpha()}, key=len, reverse=True)
    if not toks:
        raise RuntimeError("no identity token long enough to plant; the derived arm cannot be "
                           "controlled and must not be reported as controlled")
    F.compile_tex(f"Anonymous ACL submission\\par Example University {toks[0]}", FIX, "leak2")
    # THIRD arm: the heading check reads the SOURCE, not the PDF, so a PDF fixture cannot exercise it.
    # Added when the author found a real Acknowledgements section in the anonymous submission after
    # eighteen gates went green -- an arm with no control is a line in a report, not a check.
    tex = _tex_with(d, lambda t: t.replace(r"\section*{Use of generative AI}",
                                          r"\section*{Acknowledgements}"))
    return [(V, "PDF", FIX / "leak2.pdf"), (V, "TEX", tex)]


def m_exhibits(d):
    return [(V, "TEX", _tex_with(d, lambda t: t.replace(
        r"\input{tables/", r"\input{tables/table1_lineup}\input{tables/", 1)))]


def m_vrules(d):
    p = tmp_paper(d, "tables")
    t = next(p.joinpath("tables").glob("table*.tex"))
    t.write_text(re.sub(r"(\\begin\{tabular\}\{)([^}]*)(\})", r"\1l|\2\3", t.read_text(), count=1))
    return [(V, "HERE", p)]


def m_numbers(d):
    return [(V, "TEX", _tex_with(d, lambda t: t.replace("\\section{Conclusion}",
                                                        "The rate was 0.123456. \\section{Conclusion}")))]


def m_citations(d):
    # C, not V: the check moved to checks_cite.py and reads that module's TEX. Patching the old
    # module left the control silently vacuous, and the selftest is the only reason that was visible.
    return [(C, "TEX", _tex_with(d, lambda t: t.replace(
        "\\section{Conclusion}", "See \\citep{no-such-key-at-all}. \\section{Conclusion}")))]


def m_prose(d):
    """TWO arms, because the gate reads two scopes: a banned phrase in main.tex's own body, and an
    em-dash inside an \\input-ed appendix section. The second arm is the defect that shipped -- four
    `---` sat in sections/data_statement.tex under a green "no em-dash" line -- so a control that
    only plants in main.tex would certify the narrow scope all over again."""
    p = tmp_paper(d, "sections")
    (p / "main.tex").write_text((HERE / "main.tex").read_text().replace(
        "\\section{Conclusion}", "We are the first to measure this. \\section{Conclusion}"))
    s = p / "sections" / "data_statement.tex"
    s.write_text(s.read_text().replace("The corpus is corporate.",
                                       "The corpus is corporate --- entirely.", 1))
    return [(R, "TEX", p / "main.tex"), (R, "HERE", p)]


def m_second_reader(d):
    """Was "own selftest" while the gate's scope lived inside prosecheck. Now that the scope is a
    module constant it can be pointed at a temp tree, so the phrase is planted in the appendix
    section -- the file the rule was written for -- instead of trusting a predicate-level arm."""
    p = tmp_paper(d, "sections")
    (p / "main.tex").write_text((HERE / "main.tex").read_text())
    s = p / "sections" / "data_statement.tex"
    s.write_text(s.read_text().replace(
        "The corpus is corporate.", "Labels were resolved by discussion. The corpus is corporate.", 1))
    return [(R, "TEX", p / "main.tex"), (R, "HERE", p)]


def m_figures_sans(d):
    p = tmp_paper(d, "figstyle.py")
    (p / "figures").mkdir(exist_ok=True)
    shutil.copy2(FIX / "sans.pdf", p / "figures" / "fig_sans.pdf")
    return [(G, "HERE", p)]


def m_min_font(d):
    p = tmp_paper(d, "figstyle.py")
    (p / "figures").mkdir(exist_ok=True)
    shutil.copy2(FIX / "tiny.pdf", p / "figures" / "fig_tiny.pdf")
    return [(G, "HERE", p)]


def m_overprint(d):
    return [(G, "PDF", FIX / "overprint.pdf")]


def m_tables_current(d):
    p = tmp_paper(d, "tables")
    t = sorted(p.joinpath("tables").glob("table*.tex"))[0]
    t.write_text(t.read_text().replace("&", "& 999 ", 1))
    return [(G, "HERE", p)]


def m_figures_covered(d):
    p = tmp_paper(d, "figures", "main.tex")
    shutil.copy2(FIX / "tiny.pdf", p / "figures" / "fig_never_included.pdf")
    return [(G, "HERE", p)]


# name -> (mutation, or None when the gate's own selftest already drives it to RED)
CONTROLS = {
    "build is current": m_fresh,
    "page count": m_pages,
    "anonymity": m_anonymous,
    "exhibit budget": m_exhibits,
    "no vertical rules": m_vrules,
    "figures vector + serif": m_figures_sans,
    "7pt floor": m_min_font,
    "no overprinted text": m_overprint,
    "tables match generator": m_tables_current,
    "figures covered": m_figures_covered,
    "numbers backed by CSV": m_numbers,
    "citations verified": m_citations,
    "prose rules": m_prose,
    "single-annotator language": m_second_reader,
    "artifact pointer": None,
    "one submittable PDF": None,
    "no paper PDF in the zip": None,
    "paper.zip": None,
}
# Why a None is acceptable, per gate. Each names the selftest arm that already drives it RED.
OWN_SELFTEST = {
    "artifact pointer": "checks_bundle.selftest drives the pointer count both ways",
    "one submittable PDF": "checks_pdfset.selftest plants a divergent PDF in paper/ and at the tree "
                           "root, and a byte-identical twin",
    "no paper PDF in the zip": "checks_pdfset.selftest runs check_zip_pdfs on the real bundle and its "
                               "source-mismatch arm",
    "paper.zip": "checks_bundle.selftest builds a zip missing an asset and requires compiles_clean "
                 "and imports_resolve to reject it",
}


# A gate with independent arms is only controlled when EVERY arm fires: one firing proves the other
# nothing. Keyed by gate, valued by a substring that must appear in the messages -- derived from here
# rather than hardcoded in the selftest, so adding an arm cannot be forgotten in one of two places.
MULTI_ARM = {
    "anonymity": ("de-anonymising strings", "identity tokens", "anonymity-hostile section heading"),
    "prose rules": ("banned phrasing", "em-dash"),
}


def scope_drift(check_fn, triples) -> str:
    """The invariant a refactor breaks silently: a control must patch the module that DEFINES the
    gate it controls.

    When `check_citations` moved to checks_cite.py with its own TEX constant, its control kept
    patching verify_paper.TEX — so the planted defect went into a file the gate no longer opened and
    the harness reported "stayed green on its own defect", which is indistinguishable from a broken
    gate. `patched()` cannot catch it: the attribute still EXISTS on the old module, it is simply not
    the one being read. Returns a reason string when the invariant is violated, else ""."""
    owner = getattr(check_fn, "__module__", None)
    patched_mods = {getattr(m, "__name__", None) for m, _, _ in triples}
    if owner and patched_mods and owner not in patched_mods:
        return (f"control patches {sorted(m for m in patched_mods if m)} but the gate is defined in "
                f"{owner} — the planted defect lands where the gate never looks")
    return ""


def run_all() -> list:
    if not FIX.joinpath("sans.pdf").exists():
        if not F.available():
            raise SystemExit("pdflatex not on PATH: the PDF fixtures cannot be built, so five "
                             "controls cannot run. Refusing to report partial coverage as coverage.")
        for fn in (F.sans_pdf, F.tiny_font_pdf, F.overprint_pdf, F.leak_pdf):
            fn(FIX)
    out = []
    for name, fn in V.CHECKS:
        mut = CONTROLS.get(name, "MISSING")
        if mut == "MISSING":
            out.append({"gate": name, "control": "NO CONTROL",
                        "why": "no entry in CONTROLS -- this gate was added after the harness"})
            continue
        if mut is None:
            out.append({"gate": name, "control": "own selftest", "why": OWN_SELFTEST[name],
                        "fired": True})
            continue
        seen = []
        with tempfile.TemporaryDirectory() as d:
            try:
                triples = mut(Path(d))
                drift = scope_drift(fn, triples)
                if drift:
                    out.append({"gate": name, "control": "planted defect", "fired": False,
                                "why": f"SCOPE DRIFT: {drift}"})
                    continue
                with patched(*triples):
                    fn(seen.append)
            except Exception as e:               # a crash is not a pass
                out.append({"gate": name, "control": "planted defect", "fired": False,
                            "why": f"the control raised {type(e).__name__}: {e}"[:180]})
                continue
        row = {"gate": name, "control": "planted defect", "fired": bool(seen),
               "message": (seen[0] if seen else "")[:150]}
        if name in MULTI_ARM:
            row["both_arms"] = all(any(k in m for m in seen) for k in MULTI_ARM[name])
            row["arms"] = len(seen)
        out.append(row)
    return out


def selftest() -> str:
    """Every gate must have a control, and every control must make its gate go RED."""
    rows = run_all()
    assert len(rows) == len(V.CHECKS), f"{len(rows)} controls for {len(V.CHECKS)} gates"
    # A gate with independent arms is only controlled when every arm fires; one firing proves the
    # other nothing. The roster comes from MULTI_ARM so a new arm cannot be added in one place only.
    for gate in MULTI_ARM:
        r = next((x for x in rows if x["gate"] == gate), None)
        assert r and r.get("both_arms"), \
            f"the {gate} control must fire every arm {MULTI_ARM[gate]}, got {r}"
    missing = [r["gate"] for r in rows if r["control"] == "NO CONTROL"]
    dead = [f"{r['gate']}: {r.get('why') or 'stayed green on its own defect'}"
            for r in rows if not r.get("fired")]
    assert not missing, f"gates with no control: {missing}"
    assert not dead, "controls that did not fire:\n  " + "\n  ".join(dead)
    planted = sum(1 for r in rows if r["control"] == "planted defect")
    return (f"gate_controls selftest PASS - all {len(rows)} gates have a control; {planted} were "
            f"driven RED by a defect planted in a temp copy of the tree, and "
            f"{len(rows) - planted} are driven RED by their own module's selftest")


if __name__ == "__main__":
    if "selftest" in sys.argv[1:]:
        print(selftest())
    else:
        for r in run_all():
            mark = "RED  " if r.get("fired") else "GREEN"
            print(f"{mark} {r['gate']:28} {r['control']:16} "
                  f"{(r.get('message') or r.get('why') or '')[:90]}")
