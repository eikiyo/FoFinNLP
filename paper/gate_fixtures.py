"""
Location: paper-a/paper/gate_fixtures.py
Purpose: W4b -- build the deliberately-BAD artifacts a positive control needs: a PDF with sans-serif
         text, one with 5pt text, one with two words printed on top of each other. Small, real PDFs
         compiled by pdflatex, so a geometry gate is proven to fire on a real file rather than on a
         mock of one.
         Usage:  imported by gate_controls.py; `python3 paper/gate_fixtures.py` builds them to /tmp
Functions: compile_tex(), sans_pdf(), tiny_font_pdf(), overprint_pdf(), leak_pdf(),
           available()
Calls: pdflatex
Imports: shutil, subprocess, pathlib

A mock cannot prove a gate that reads a PDF. These fixtures are the smallest real documents that
carry the defect each gate exists to catch, so the control exercises the same extraction path as the
gate's production input.
"""

import contextlib
import shutil
import subprocess
import tempfile
from pathlib import Path

# The real paper directory, the SOURCE the harness copies from. Needed here because tmp_paper() and
# _tex_with() moved in with the rest of the plumbing; without it they raised NameError, which the
# control harness reported as "the control raised NameError" rather than as a pass — a crash recorded
# as not-fired is exactly what that rule is for.
HERE = Path(__file__).resolve().parent

PREAMBLE = r"\documentclass[10pt]{article}\pagestyle{empty}"


def available() -> bool:
    return bool(shutil.which("pdflatex"))


def compile_tex(body: str, out: Path, name: str, extra: str = "") -> Path:
    """Compile a fragment to <out>/<name>.pdf. Returns the path, or raises with the log's tail."""
    out.mkdir(parents=True, exist_ok=True)
    tex = out / f"{name}.tex"
    tex.write_text(f"{PREAMBLE}\n{extra}\n\\begin{{document}}\n{body}\n\\end{{document}}\n")
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex.name],
                       cwd=out, capture_output=True, text=True)
    pdf = out / f"{name}.pdf"
    if not pdf.exists():
        tail = "\n".join(r.stdout.strip().splitlines()[-12:])
        raise RuntimeError(f"fixture {name} did not compile:\n{tail}")
    return pdf


def sans_pdf(out: Path) -> Path:
    """Text in a sans-serif family ONLY: the defect `figures vector + serif` exists to catch.

    The whole document has to be sans. A first version set one span in Helvetica and left the rest
    in CMR10, so the file embedded a serif font too and the gate passed it -- a fixture that does not
    actually carry the defect turns a positive control into a second negative one."""
    return compile_tex(r"A sans serif label 0.42", out, "sans",
                       extra=r"\usepackage{helvet}\renewcommand{\familydefault}{\sfdefault}")


def tiny_font_pdf(out: Path) -> Path:
    """5pt text, under the 7pt floor."""
    return compile_tex(r"{\fontsize{5}{6}\selectfont five point text 0.42}", out, "tiny")


def overprint_pdf(out: Path) -> Path:
    """Two words printed at the same position, which is what an overlap check must see.

    `\rlap` alone did not do it: pdflatex set the two words on consecutive lines, so the fixture
    carried no overlap and the control was silently vacuous. A zero-width `\makebox` on a
    `\noindent` line puts the second word's box on top of the first's."""
    return compile_tex(r"\noindent\makebox[0pt][l]{OVERPRINTEDAAA}OVERPRINTEDBBB", out, "overprint")


def leak_pdf(out: Path) -> Path:
    """Carries the anonymous byline AND a de-anonymising affiliation string, so the anonymity gate
    has something to find. The byline has to be present too, or the control would fire on the
    missing-byline arm and prove nothing about leak detection."""
    return compile_tex(r"Anonymous ACL submission\\par Example Institute of Technology University", out, "leak")


if __name__ == "__main__":
    d = Path("/tmp/gate_fixtures")
    if not available():
        raise SystemExit("pdflatex not on PATH; fixtures cannot be built")
    for f in (sans_pdf, tiny_font_pdf, overprint_pdf, leak_pdf):
        print(f.__name__, "->", f(d))


# --- harness plumbing, used by gate_controls -------------------------------------------------
# These live beside the fixtures rather than in gate_controls.py because they are the same concern:
# building a disposable copy of the tree and pointing a gate at it. Moved here when gate_controls
# crossed its 300-LOC budget, which is the reason to split and not a reason to relax the budget.

FIX = Path(tempfile.gettempdir()) / "gate_fixtures"


@contextlib.contextmanager
def patched(*triples):
    """Temporarily set module attributes, restoring them even if the check raises."""
    saved = [(m, a, getattr(m, a)) for m, a, _ in triples]
    try:
        for m, a, v in triples:
            setattr(m, a, v)
        yield
    finally:
        for m, a, v in saved:
            setattr(m, a, v)


def tmp_paper(d: Path, *keep) -> Path:
    """A partial copy of paper/ in `d`, carrying only what the gate under control needs."""
    out = d / "paper"
    out.mkdir(parents=True, exist_ok=True)
    for name in keep:
        src = HERE / name
        dst = out / name
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    return out


def _tex_with(d: Path, edit) -> Path:
    p = d / "main.tex"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(edit((HERE / "main.tex").read_text()))
    return p
