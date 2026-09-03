"""
Location: paper-a/paper/checks_pdfset.py
Purpose: W4a -- there must be exactly ONE PDF a human could plausibly submit, enumerated as a CLASS
         rather than as the pair of paths that happened to exist when the rule was written.
         Usage:  python3 paper/checks_pdfset.py [selftest]   (also called by verify_paper.py)
Functions: submittable(), facts(), check_one_pdf(), zip_pdfs(), check_zip_pdfs(), selftest()
Calls: pdfinfo, paper.zip -- READ ONLY
Imports: hashlib, re, subprocess, sys, zipfile, pathlib

The previous version compared `.lmk/main.pdf` against `paper/main.pdf` and nothing else, while its
docstring claimed "exactly one PDF a human could plausibly submit". Four existed in `paper/` at the
time: a 16-page stale build, an 11-page older one, and an 8-page venue-named one that carried no
appendix. The gate reported on a category while checking a pair, which is the most dangerous kind of
green -- it reads as coverage. This version globs the class and names every candidate it finds.
"""

import hashlib
import re
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# Excluded by NAME, not by relying on glob being non-recursive: a future reader has to be able to see
# which directories are deliberately out of scope. `audit/` holds main_marked.pdf (D4.6) and the
# cached reference PDFs, none of which is a submission candidate; the build dirs hold the artifact
# the candidate is compared AGAINST.
# `.lmk` is the ONE canonical build directory, and it is skipped because the gate compares every
# candidate AGAINST `.lmk/main.pdf` — scanning it would compare it to itself. `.build` was in this set
# too and has been removed, along with the abandoned 8-page build it held (hashes in
# audit/deletions.md): an exemption is weaker than a deletion. But see submittable() — the exemption
# was NOT what hid that file, the non-recursive walk was, and the walk is the part that mattered.
# Add nothing to this set without asking what the addition would hide, and never assume a name in
# here is the reason something was missed.
SKIP_DIRS = {".lmk", "__pycache__", ".refactor-dedup", "audit", "figures", "out"}
CANON = HERE / ".lmk" / "main.pdf"


def submittable() -> list:
    """Every PDF at the tree root or anywhere under paper/ that a human could mistake for the
    submission, minus the named directories.

    RECURSIVE, and that is the fix. This used to be `d.glob("*.pdf")` over exactly two directories,
    which meant a PDF one level down was never enumerated at all — `paper/.build/main.pdf`, an
    abandoned 8-page build, was invisible to the gate whose entire purpose is to prove exactly one
    submittable PDF exists. The author found it and read the cause as the `.build` entry in SKIP_DIRS;
    the control written to prove that fix showed SKIP_DIRS was never even reached, so the exemption
    was not the mechanism and removing it alone would have changed nothing. A non-recursive walk does
    not exempt one directory, it exempts every directory, and that is a far wider hole than the one
    reported. Both were fixed: the directory is deleted, and the walk now descends."""
    out = [p for p in sorted(ROOT.glob("*.pdf"))] if ROOT.name not in SKIP_DIRS else []
    out += [p for p in sorted(HERE.rglob("*.pdf"))
            if not (set(p.relative_to(HERE).parts[:-1]) & SKIP_DIRS)]
    return out


def facts(p: Path) -> dict:
    r = subprocess.run(["pdfinfo", str(p)], capture_output=True, text=True)
    m = re.search(r"^Pages:\s+(\d+)", r.stdout, re.M)
    return {"path": str(p.relative_to(ROOT)), "pages": int(m.group(1)) if m else -1,
            "kb": p.stat().st_size // 1024, "mtime": p.stat().st_mtime,
            "sha": hashlib.sha256(p.read_bytes()).hexdigest()}


def check_one_pdf(fail) -> str:
    """Exactly one distinct PDF by hash, and it must be the current build."""
    cands = submittable()
    if not cands:
        fail("no PDF exists at the tree root or in paper/ -- there is nothing to submit")
        return "NO PDF"
    rows = [facts(p) for p in cands]
    by_hash = {}
    for r in rows:
        by_hash.setdefault(r["sha"], []).append(r)
    if len(by_hash) > 1:
        named = "; ".join(f"{r['path']} ({r['pages']}pp, {r['kb']}KB, "
                          f"{__import__('time').strftime('%Y-%m-%d %H:%M', __import__('time').localtime(r['mtime']))})"
                          for r in sorted(rows, key=lambda x: x["path"]))
        fail(f"{len(by_hash)} DIFFERENT PDFs could be submitted, so whichever is uploaded is a "
             f"guess: {named}")
        return f"{len(by_hash)} DIVERGENT PDFs"
    if CANON.exists():
        canon = hashlib.sha256(CANON.read_bytes()).hexdigest()
        if canon not in by_hash:
            fail(f"the only submittable PDF ({rows[0]['path']}, {rows[0]['pages']}pp) is NOT the "
                 f"current build .lmk/main.pdf -- it is a stale copy of something else")
            return "STALE"
    n = len(rows)
    return (f"{n} file{'s' if n > 1 else ''} at root/paper, ONE distinct PDF "
            f"({rows[0]['pages']}pp, {rows[0]['kb']}KB), identical to the current build")


def zip_pdfs(z: Path) -> dict:
    """The PDFs inside paper.zip, split into paper-shaped and expected exhibits."""
    with zipfile.ZipFile(z) as f:
        names = [n for n in f.namelist() if n.lower().endswith(".pdf")]
        blobs = {n: hashlib.sha256(f.read(n)).hexdigest() for n in names}
    paperish = [n for n in names if "/" not in n or re.match(r"^(main|paper)", Path(n).name, re.I)]
    return {"all": names, "paper_shaped": paperish, "hashes": blobs}


def check_zip_pdfs(fail) -> str:
    """4a.4 -- the bundle must carry no compiled paper, and every exhibit must match its original.

    Stated as two rules rather than "no more than one PDF": the zip legitimately carries five figure
    PDFs and five greyscale proofs, because the paper cannot compile without the figures and the
    proofs are evidence about them. What must NOT be in a source bundle is a compiled paper, which
    is a second answer to "which file is the submission"."""
    z = HERE / "paper.zip"
    if not z.exists():
        fail("paper.zip does not exist")
        return "NO ZIP"
    info = zip_pdfs(z)
    if info["paper_shaped"]:
        fail(f"paper.zip carries a compiled paper: {info['paper_shaped']} -- a source bundle with a "
             f"PDF in it gives a reviewer two candidates")
        return "PAPER PDF IN ZIP"
    drift, missing = [], []
    for n, h in info["hashes"].items():
        # Mirror checks_bundle.build()'s own path construction: it writes out/figures/<rest> into the
        # zip as audit/<rest>, keeping the greyscale/ level. Mapping to out/figures/<basename> drops
        # that level, and the first version of this check reported five false drifts because of it --
        # the failure named the five files, which is how it was found.
        src = (ROOT / "out" / "figures" / n[len("audit/"):]) if n.startswith("audit/") else (HERE / n)
        if not src.exists():
            missing.append(f"{n} (no source at {src.relative_to(ROOT)})")
        elif hashlib.sha256(src.read_bytes()).hexdigest() != h:
            drift.append(n)
    if missing:
        fail(f"{len(missing)} PDF(s) in paper.zip have no source on disk to compare against, so "
             f"this check cannot verify them: {missing[:4]}")
        return "ZIP SOURCE MISSING"
    if drift:
        fail(f"{len(drift)} PDF(s) in paper.zip do not match the file on disk: {drift[:4]}")
        return "ZIP EXHIBIT DRIFT"
    return (f"paper.zip: 0 compiled papers, {len(info['all'])} exhibit PDFs, every one "
            f"byte-identical to its source on disk")


def selftest() -> str:
    """4a.3 -- both controls, on a real copy of the tree rather than on a mock."""
    import shutil
    import tempfile
    seen = []

    def fail(msg):
        seen.append(msg)

    # NEGATIVE control first: the tree as it stands must pass.
    seen.clear()
    out = check_one_pdf(fail)
    assert not seen, f"the real tree must pass, got: {seen}"
    assert "ONE distinct PDF" in out, out
    real = submittable()
    assert real, "the real tree must contain at least one candidate, or the arm below is empty"

    with tempfile.TemporaryDirectory() as d:
        # POSITIVE control: plant a DIVERGENT PDF beside the real one; the gate must fail and name it.
        plant = real[0].parent / "_selftest_divergent.pdf"
        try:
            plant.write_bytes(real[0].read_bytes() + b"\n% divergent\n")
            seen.clear()
            check_one_pdf(fail)
            assert seen, "a divergent PDF beside the submission was NOT detected"
            assert "_selftest_divergent.pdf" in seen[0], f"the failure must name it: {seen[0]}"
            assert "DIFFERENT PDFs" in seen[0], seen[0]
        finally:
            plant.unlink(missing_ok=True)

        # And a byte-IDENTICAL copy must pass, or the gate is just counting files.
        twin = real[0].parent / "_selftest_twin.pdf"
        try:
            shutil.copy2(real[0], twin)
            seen.clear()
            res = check_one_pdf(fail)
            assert not seen, f"a byte-identical copy must pass, got: {seen}"
            assert "ONE distinct PDF" in res, res
        finally:
            twin.unlink(missing_ok=True)

        # The class, not the instance: a PDF at the TREE ROOT must be seen too, not only paper/.
        rootplant = ROOT / "_selftest_root.pdf"
        try:
            rootplant.write_bytes(real[0].read_bytes() + b"\n% root\n")
            seen.clear()
            check_one_pdf(fail)
            assert seen and "_selftest_root.pdf" in seen[0], \
                f"a divergent PDF at the tree root must be enumerated: {seen}"
        finally:
            rootplant.unlink(missing_ok=True)

        # audit/ must be EXCLUDED: main_marked.pdf is deliberately different and is not a candidate.
        marked = ROOT / "audit" / "main_marked.pdf"
        if marked.exists():
            seen.clear()
            check_one_pdf(fail)
            assert not seen, f"audit/main_marked.pdf must not be treated as a candidate: {seen}"
    seen.clear()
    zres = check_zip_pdfs(fail)
    assert not seen, f"the real zip must pass: {seen}"
    return (f"checks_pdfset selftest PASS - the real tree passes with {len(real)} candidate(s), a "
            f"divergent PDF planted in paper/ AND one planted at the tree root are both detected and "
            f"named, a byte-identical copy passes, audit/main_marked.pdf is correctly not a "
            f"candidate, and the zip check passes on the real bundle ({zres[:60]})")


if __name__ == "__main__":
    if "selftest" in sys.argv[1:]:
        print(selftest())
    else:
        bad = []
        print(check_one_pdf(bad.append))
        print(check_zip_pdfs(bad.append))
        for b in bad:
            print("FAIL:", b)
        sys.exit(1 if bad else 0)
