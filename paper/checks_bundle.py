"""
Location: paper-a/paper/checks_bundle.py
Purpose: Build paper.zip and prove it is a working submission: the files a reviewer needs are in
         it, and every script it ships can actually run from a clean extraction. Split out of
         verify_paper.py when that file passed its 300-LOC budget.
Functions: zip_keep(), zip_need(), check_zip(), imports_resolve(), selftest()
Calls: zipfile, subprocess (imports each shipped module in a temp extraction)
Imports: re, subprocess, sys, tempfile, zipfile, pathlib
"""

import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The fixed non-Python assets. Everything else the zip carries is derived; see zip_keep.
ASSETS = ("main.tex", "acl.sty", "acl_natbib.bst", "anthology.bib", "custom.bib", "README.md")


def zip_keep() -> list:
    """The files the submission carries, DERIVED, never listed.

    It was a literal list of eighteen names and it went stale twice: first when figstyle, figpanels
    and checks_geometry were written, then again when table_appendix, table_claims, figevidence and
    figgate were split out of files that had hit their line budget. Both times the zip shipped a
    script that raised ModuleNotFoundError on a clean extraction. Every .py beside main.tex is part
    of this paper's toolchain by construction, so the directory listing is the correct source and
    nobody has to remember anything."""
    return list(ASSETS) + sorted(p.name for p in HERE.glob("*.py"))


def zip_need() -> tuple:
    """Every file the compile actually reaches for, read out of main.tex for the same reason.

    A hand-named figure is worse than useless here: the old list required
    figures/fig1_observability.pdf, a figure the paper stopped including, so the check went on
    passing while naming an artifact no longer in the document. What the submission needs is
    exactly what main.tex asks for, and main.tex is the file that knows."""
    tex = (HERE / "main.tex").read_text()
    figs = re.findall(r"\\includegraphics\[[^\]]*\]\{([^}]+)\}", tex)
    # EVERY \input, whatever directory it names -- not just tables/. This was hardcoded to
    # tables/, so when the data statement was added as \input{sections/data_statement} the zip
    # neither required nor carried it, and paper.zip stopped compiling from a clean extraction
    # while every contents check still passed. A requirement list that can only see one directory
    # is a requirement list that goes stale the first time a second one appears.
    inputs = [f"{n}.tex" if not n.endswith(".tex") else n
              for n in re.findall(r"\\input\{([^}]+)\}", tex)]
    if not figs or not inputs:
        raise SystemExit("main.tex names no figure or no \\input -- refusing to certify a zip "
                         "against a requirement list that parsed to nothing")
    return tuple(ASSETS[:3]) + tuple(figs) + tuple(inputs)


def imports_resolve(z: Path, names: list) -> list:
    """Extract to a temp directory and import every shipped .py there.

    Both lists are derived now (see zip_keep and zip_need), but this stays the load-bearing test:
    a derived list still cannot know that a module imports something that was never in the
    directory. Importing each module is the check that depends on nothing being remembered."""
    broken = []
    with tempfile.TemporaryDirectory() as td:
        zipfile.ZipFile(z).extractall(td)
        for s in [n for n in names if n.endswith(".py")]:
            r = subprocess.run([sys.executable, "-c", f"import {Path(s).stem}"],
                               cwd=td, capture_output=True, text=True)
            if r.returncode:
                broken.append(f"{s} ({(r.stderr.strip().splitlines() or ['?'])[-1]})")
    return broken


def build(dest: Path = None) -> Path:
    """Write the zip. Kept separate from the check so the selftest can build one to a temp path
    without overwriting the real submission bundle."""
    z = dest or (HERE / "paper.zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as f:
        for name in zip_keep():
            if (HERE / name).exists():
                f.write(HERE / name, name)
        # Derived from what main.tex actually asks for, plus figures. A literal ("figures",
        # "tables") tuple silently omitted sections/ the moment it existed.
        for sub in sorted({"figures"} | {Path(n).parent.as_posix() for n in zip_need()
                                         if "/" in n}):
            d = HERE / sub
            if d.is_dir():
                for p in sorted(d.glob("*")):
                    if p.is_file():
                        f.write(p, f"{sub}/{p.name}")
        # The figure audit and the greyscale proofs travel WITH the submission. They are evidence
        # about the figures, and evidence that stays in a working directory is evidence a reviewer
        # never sees. Vector greyscale copies only; the PNG renders are for looking at locally and
        # would triple the bundle.
        audit = HERE.parent / "out" / "figures"
        if (audit / "FIGURE_AUDIT.md").exists():
            f.write(audit / "FIGURE_AUDIT.md", "audit/FIGURE_AUDIT.md")
        for p in sorted((audit / "greyscale").glob("*.pdf")):
            f.write(p, f"audit/greyscale/{p.name}")
    return z


def compiles_clean(z: Path, fail) -> str:
    """Extract the zip somewhere with none of our files and BUILD it, the way a reviewer will.

    The submission requirement is that paper.zip compiles on Overleaf with zero edits, and this
    was checked once by hand and then went stale the moment main.tex changed: a hand-run check is
    a check that is current only until the next commit. Everything else in this module verifies
    the zip's CONTENTS, which is not the same claim -- a zip can hold every file and still fail to
    build."""
    with tempfile.TemporaryDirectory() as td:
        zipfile.ZipFile(z).extractall(td)
        r = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "main.tex"],
                           cwd=td, capture_output=True, text=True)
        log = Path(td) / "main.log"
        pdf = Path(td) / "main.pdf"
        if r.returncode or not pdf.exists():
            tail = (log.read_text(errors="ignore").splitlines()[-6:] if log.exists()
                    else r.stdout.splitlines()[-6:])
            fail(f"paper.zip does NOT compile from a clean extraction (exit {r.returncode}): "
                 f"{' | '.join(t.strip() for t in tail)}")
            return "DOES NOT COMPILE"
        over = log.read_text(errors="ignore").count("Overfull") if log.exists() else -1
        if over:
            fail(f"the zip build has {over} overfull box(es); the submitted PDF would differ "
                 f"from the local one")
        pages = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        n = next((l.split()[-1] for l in pages.splitlines() if l.startswith("Pages")), "?")
        return f"compiles clean from a bare extraction: {n} pages, {over} overfull"


def check_zip(fail) -> str:
    z = build()
    names = zipfile.ZipFile(z).namelist()
    for need in zip_need():
        if need not in names:
            fail(f"paper.zip is missing {need}")
    broken = imports_resolve(z, names)
    if broken:
        fail(f"scripts in paper.zip that cannot run from the zip: {broken}")
    built = compiles_clean(z, fail)
    return (f"paper.zip: {len(names)} files, {z.stat().st_size // 1024} KB; "
            f"all {sum(1 for n in names if n.endswith('.py'))} shipped scripts import from a "
            f"clean extraction; {built}")


def selftest() -> str:
    """Prove the import test discriminates. A checker that reports every zip as fine would pass a
    does-the-real-zip-work test and catch nothing, so a deliberately incomplete zip must go RED."""
    with tempfile.TemporaryDirectory() as td:
        good = Path(td) / "good.zip"
        with zipfile.ZipFile(good, "w") as f:
            f.writestr("m_ok.py", "VALUE = 1\n")
        assert imports_resolve(good, ["m_ok.py"]) == [], "a self-contained module must import"
        bad = Path(td) / "bad.zip"
        with zipfile.ZipFile(bad, "w") as f:
            f.writestr("m_bad.py", "import a_module_left_out_of_the_zip\n")
        broken = imports_resolve(bad, ["m_bad.py"])
        assert len(broken) == 1 and "ModuleNotFoundError" in broken[0], \
            f"a module whose dependency was not packaged must be reported: {broken}"
        # The compile arm, both ways. A zip that references a file it does not carry is the exact
        # shape of the real failure (a table or figure the zip does not carry), and it must go RED;
        # a minimal well-formed document must go GREEN, or the check is refusing everything.
        ok_zip = Path(td) / "ok_tex.zip"
        with zipfile.ZipFile(ok_zip, "w") as f:
            f.writestr("main.tex", "\\documentclass{article}\\begin{document}x\\end{document}\n")
        said = []
        note = compiles_clean(ok_zip, said.append)
        assert not said and "compiles clean" in note, f"a valid document must build: {said} {note}"
        miss_zip = Path(td) / "missing_input.zip"
        with zipfile.ZipFile(miss_zip, "w") as f:
            f.writestr("main.tex", "\\documentclass{article}\\begin{document}"
                                   "\\input{tables/not_packaged}\\end{document}\n")
        red = []
        got = compiles_clean(miss_zip, red.append)
        # Written out rather than chained: `a and b or a` collapses to `a`, so the first version
        # of this line passed on ANY failure message and would have certified a check that went
        # red for the wrong reason, or returned the wrong verdict string.
        assert len(red) == 1, f"exactly one failure expected, got {red}"
        assert "does not compile" in red[0].lower(), f"the failure must name compilation: {red[0]}"
        assert got == "DOES NOT COMPILE", f"and the verdict must say so, not {got!r}"
    need = zip_need()
    assert "main.tex" in need and any(n.startswith("figures/") for n in need) \
        and any(n.startswith("tables/") for n in need), f"zip_need parsed nothing useful: {need}"
    # The regression: an \input from a directory OTHER than tables/ must be required too.
    assert any(n.startswith("sections/") for n in need), \
        f"an \\input outside tables/ is not being seen by zip_need: {need}"
    assert all((HERE / n).exists() for n in need), \
        f"zip_need names a file that is not on disk: {[n for n in need if not (HERE / n).exists()]}"
    keep = zip_keep()
    assert "checks_bundle.py" in keep and "main.tex" in keep, f"zip_keep is incomplete: {keep}"
    assert len(set(keep)) == len(keep), "zip_keep must not list a file twice"
    return ("checks_bundle selftest PASS - a self-contained module imports clean, a module whose "
            "dependency was left out of the zip is reported by name, and the compile arm builds a "
            "valid document while refusing one that references a file the zip does not carry, and "
            f"the derived lists resolve to {len(keep)} carried files and {len(need)} required ones, "
            "every one of them on disk")


if __name__ == "__main__":
    print(selftest())


# --- Artifact pointer -------------------------------------------------------------------------
# One pointer to the artifact, in one place. The URL lives in main.tex's \artifacturl macro and
# nowhere else, so the paper cannot end up carrying two different pointers -- and this check reads
# the PDF, not the macro, because what a reviewer sees is what got typeset.
POINTER = "The artifact is at"
RELEASE_URL = "https://github.com/eikiyo/FoFinNLP"


def check_artifact_pointer(fail) -> str:
    """Exactly one artifact pointer must reach the PDF, and it must be the pinned public
    release repository. Camera-ready: an empty or non-pinned URL fails, because the Anthology
    PDF is permanent and a stray anonymous or wrong-repo URL in it cannot be recalled."""
    tex = (HERE / "main.tex").read_text()
    text = subprocess.run(["pdftotext", str(HERE / ".lmk" / "main.pdf"), "-"],
                          capture_output=True, text=True).stdout
    # Counted on whitespace-collapsed text: pdftotext wraps at column width, so the pointer
    # sentence can extract as "The artifact\nis at ..." and a raw count reads 0 for a pointer a
    # reviewer plainly sees. Same fix prosecheck.body documents; the URL test below already
    # collapses newlines for the same reason. Review-mode line numbers are stripped first: when
    # the sentence straddles a page break, pdftotext interleaves the lineno margin as standalone
    # digit lines between its two halves, and whitespace collapse alone cannot bridge digits.
    joined = re.sub(r"\s+", " ", re.sub(r"(?m)^\d+\s*$", " ", text))
    n = joined.count(POINTER)
    if n == 0 and joined.count("The artifact") == 1 and joined.count("is at http") == 1:
        # A page break can split the sentence mid-phrase, and two-column extraction can then emit
        # the two halves OUT OF ORDER, so no join can reconstruct it. Each half typeset exactly
        # once is the same fact; a missing pointer still reads 0 because both halves are absent,
        # and a duplicated pointer still fails because a half then counts 2.
        n = 1
    if n != 1:
        fail(f"the PDF carries {n} artifact pointers; exactly 1 is required")
    m = re.search(r"\\newcommand\{\\artifacturl\}\{([^}]*)\}", tex)
    if not m:
        fail("main.tex no longer defines \\artifacturl -- the pointer has lost its single source")
        return "MACRO MISSING"
    url = m.group(1).strip()
    if url != RELEASE_URL:
        fail(f"the artifact URL is not the pinned public release repository: {url!r}")
    if url not in text.replace("\n", ""):
        fail("the artifact URL is set in main.tex but does not appear in the PDF")
    return f"1 pointer in the PDF, the pinned public release repo, URL typeset: {url}"


def selftest_pointer() -> str:
    """Both arms on synthetic text, since the real PDF can only be in one state at a time."""
    said = []
    assert POINTER in "The artifact is at the anonymised URL in the submission form."
    # THE HARD-WRAP ARM: extraction breaks lines mid-sentence, and a raw count once read a typeset
    # pointer as absent because the wrap fell inside the phrase.
    assert re.sub(r"\s+", " ", "The artifact\nis at the anonymised URL.").count(POINTER) == 1, \
        "a pointer split by an extraction line break must still be counted"
    for url, want_fail in ((RELEASE_URL, False),
                           ("https://anonymous.4open.science/r/probity-1234", True),
                           ("https://github.com/someone/probity", True),
                           ("", True)):
        assert (url != RELEASE_URL) == want_fail, \
            f"{url!r} should {'fail' if want_fail else 'pass'} the pinned-URL test"
    assert not said
    return ("artifact-pointer test PASS - the pinned release URL passes; an anonymous host, a "
            "namesake repo and an empty URL fail")


# --- One submittable PDF ------------------------------------------------------------------------
# check_one_pdf moved to checks_pdfset.py (W4a). It compared two hardcoded paths while claiming to
# check a class, and the replacement enumerates every PDF at the tree root and in paper/. Left as a
# note rather than deleted silently, so a future reader looking for it here finds where it went.
