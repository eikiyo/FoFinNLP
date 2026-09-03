"""
Location: paper-a/paper/verify_paper.py
Purpose: RUN the acceptance test. Every item in the writing spec's checklist is checked here by
         executing something, never by asserting it. Exits non-zero if any check fails, and prints
         what it measured rather than a bare PASS, so a green line can be audited.
         Usage:  python3 paper/verify_paper.py        (PAPER_PDF=<path> to check another build)
Functions: one check_* per checklist item, plus main() and selftest()
Calls: checks_geometry (rendered geometry), numcheck (figures vs CSVs), prosecheck (writing rules)
Imports: os, re, sys, pathlib, checks_bundle, checks_pdfset, checks_geometry, pdfcheck,
         numcheck, prosecheck
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numcheck as N                                              # noqa: E402
import prosecheck as W                                           # noqa: E402
import pdfcheck as P                                             # noqa: E402
import checks_geometry as G                                      # noqa: E402
import checks_bundle as B                                        # noqa: E402
import checks_pdfset as S                                        # noqa: E402
import checks_cite as C                                          # noqa: E402
import checks_prose as R                                         # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# Which compiled PDF to check. Overridable so the SAME test can be pointed at the pdflatex build
# and at any other engine's: a green from one toolchain is a green from that toolchain only.
PDF = Path(os.environ.get("PAPER_PDF", HERE / ".lmk" / "main.pdf"))
STALE_GRACE = 2.0        # seconds; staleness that matters is minutes, not write-ordering jitter
TEX = HERE / "main.tex"
FLOOR_PT = 7.0
MAIN_PAGES = 9  # camera-ready budget: ACL grants accepted papers one extra content page over the
                # 8-page submission limit (verified against EMNLP/ACL policy 2026-09-03)



def check_fresh(fail) -> str:
    """The PDF under test must be newer than everything it is built from.

    Run with no PAPER_PDF, this file used to default to a build directory that another engine had
    written hours earlier. Every check then passed, on a PDF that was not the current document: an
    eleven-out-of-eleven green certifying an artifact nobody had rebuilt. Nothing else here can
    catch that, because each check is perfectly correct about the file it was handed."""
    if not PDF.exists():
        fail(f"{PDF} does not exist; build it before verifying")
        return "no PDF"
    # W.inputs, not a hand-listed roster: sections/*.tex arrived after this list was written, so an
    # edited appendix section left this gate certifying a PDF built before the edit. Derived from
    # main.tex's own \input lines, it cannot fall behind the document again.
    srcs = ([TEX] + W.inputs(HERE, TEX) + sorted((HERE / "tables").glob("*.tex"))
            + sorted((HERE / "figures").glob("*.pdf")))
    newest = max(srcs, key=lambda p: p.stat().st_mtime)
    lag = newest.stat().st_mtime - PDF.stat().st_mtime
    if lag > STALE_GRACE:
        fail(f"{PDF.name} is {lag:.0f}s older than {newest.name}; it is a stale build, rebuild it")
        # Not the same sentence as the pass case. A summary line reading "newer than all 17 sources"
        # on a row marked FAIL is a line that contradicts its own verdict.
        return f"STALE: {PDF.parent.name}/{PDF.name} predates {newest.name} by {lag:.0f}s"
    return f"{PDF.parent.name}/{PDF.name} is newer than all {len(srcs)} sources (by {-lag:.0f}s)"


def check_pages(fail) -> str:
    """Main content is everything before Limitations. The appendix and the references are
    unlimited and do not count, so only the first number was ever a constraint.

    The 4-page short-paper limit was waived on 2026-07-29 while this was a short paper. The
    final brief moves the submission to a LONG paper, where the limit is 8 and the paper fits
    inside it, so the waiver is withdrawn and this FAILS again. A limit that is actually met
    should be enforced: a waiver kept past the condition that justified it is a gate asserting a
    falsehood.

    Two independent readings. \\label{mainend} sits at the last word of the Conclusion, so LaTeX
    itself reports the page main content ends on; pdftotext separately finds where Limitations
    starts. They are not the same quantity: Limitations may open the page after the Conclusion
    ends, or lower down the same page, so the consistency rule is that it starts on the end page or
    the one after it. Requiring equality was wrong and failed a paper that fitted."""
    total = P.page_count(PDF)
    first = P.section_page(PDF, "Limitations", total)
    aux = (PDF.parent / "main.aux")
    m = re.search(r"\\newlabel\{mainend\}\{\{[^}]*\}\{(\d+)\}", aux.read_text()) if aux.exists() else None
    if not m:
        fail("no \\label{mainend} in main.aux; the page limit cannot be measured from the source")
    if not first:
        fail("Limitations section not found in the PDF at all")
        return f"main content boundary not found in a {total}-page PDF"
    ends = int(m.group(1)) if m else first
    if m and not ends <= first <= ends + 1:
        fail(f"the mainend label says the Conclusion ends on page {ends}, but Limitations starts "
             f"on page {first}; those cannot both be true")
    if ends > MAIN_PAGES:
        fail(f"main content ends on page {ends}, over the {MAIN_PAGES}-page ACL long-paper limit")
    return (f"main content ends on page {ends} of {total}, within the {MAIN_PAGES}-page long-paper "
            f"limit; Limitations starts on page {first}, which is consistent with it")


def check_anonymous(fail) -> str:
    """Camera-ready inverse of the submission-era anonymity check (git history holds that one):
    the byline must be PRESENT and every anonymity artifact gone. Each old assertion is here,
    inverted. Byline values pinned in audit/deanonymisation_plan.md from the ORCID record and
    the KTH profile page. No standalone-digit scan for review line numbers: table cells extract
    as bare 3-digit lines in the final build too, and [final] is the mechanism that removes the
    margin numbers, so asserting the option asserts the absence."""
    tex = TEX.read_text()
    text = P.run("pdftotext", PDF, "-")
    page1 = re.sub(r"\s+", " ", P.run("pdftotext", "-f", "1", "-l", "1", PDF, "-"))
    if "[final]" not in tex:
        fail("acl.sty is not loaded with the [final] option")
    if "[review]" in tex:
        fail("the [review] option is still present in main.tex")
    for s in ("Seyed Mosayeb Alam", "KTH Royal Institute of Technology", "smalam@kth.se"):
        if s not in page1:
            fail(f"page 1 is missing the byline element: {s}")
    if page1.count("Seyed Mosayeb Alam") != 1:
        fail(f"the byline name must appear exactly once on page 1, "
             f"found {page1.count('Seyed Mosayeb Alam')}")
    for s in ("anonymous acl submission", "anonymous.4open", "anonymised url"):
        if s in text.lower():
            fail(f"anonymity artifact still in the PDF: {s}")
    if not re.search(r"\\section\*\{Acknowledgments\}", tex):
        fail("the Acknowledgments section is missing (added at camera-ready)")
    return ("final mode on, byline Seyed Mosayeb Alam / KTH Royal Institute of Technology / "
            "smalam@kth.se exactly once on page 1, no anonymity artifacts in the PDF")


EXHIBIT_BUDGET = 8  # camera-ready: +1 for the stratified-contrast table the reviews asked for


def check_exhibits(fail) -> str:
    """A cap on main-text exhibits, expressed as a floor as well as a ceiling.

    The budget was 3 while the main text had to fit 4 pages, then 4 when that limit was waived,
    then 6 when the gap-closing brief named the exhibit set. It is 7 now because the final brief
    names it again for a long paper: four figures (the lineup, contamination and repair, transfer
    against its null, and observability) and three tables (the configurations, transfer, and the
    claims not supported, which no longer share a caption). Each move rewrites the gate to a
    premise that legitimately changed, which is the one reason to move one; moving it because a
    diff failed it would not be. The equality test is kept in BOTH directions, so silently
    dropping a figure is as loud as adding one."""
    body, appendix = TEX.read_text().split(r"\appendix", 1)
    main_ex = len(re.findall(r"\\input\{tables/|\\begin\{figure", body))
    app_ex = len(re.findall(r"\\input\{tables/|\\begin\{figure", appendix))
    if main_ex != EXHIBIT_BUDGET:
        fail(f"main text has {main_ex} exhibits, the budget is exactly {EXHIBIT_BUDGET}")
    return (f"{main_ex} main-text exhibits (budget {EXHIBIT_BUDGET}, raised from 3 when the "
            f"4-page limit was waived), {app_ex} appendix exhibits (unlimited)")


def check_no_vrules(fail) -> str:
    specs = [m for f in sorted((HERE / "tables").glob("*.tex"))
             for m in re.findall(r"\\begin\{tabular\}\{([^}]*)\}", f.read_text())]
    bad = [s for s in specs if "|" in s]
    if bad:
        fail(f"vertical rule in a column spec: {bad}")
    return f"{len(specs)} tabular column specs, none contains a vertical rule"


def check_numbers_backed(fail) -> str:
    """Every decimal figure in the prose must be a correct ROUNDING of some generated value.

    A string-equality version red-flagged fourteen correct numbers, because prose quotes 0.087
    where the CSV holds 0.086614. A gate that rejects correct data is as damaging as one that
    accepts wrong data, so the comparison is made at the precision the prose claims. Percentages
    and complements are matched too: a share stored as 0.018110 is quoted as 1.8."""
    sys.path.insert(0, str(ROOT / "analysis"))
    import tables_out as T
    gen = sorted((ROOT / "out" / "tables").rglob("*.csv"))
    tex = re.sub(r"(?m)^\s*%.*", "", TEX.read_text())
    rows = N.csv_rows(gen)
    values = N.csv_values(rows)
    quoted = sorted(T._quoted_figures(tex), key=float)
    missing = [q for q in quoted if not N.backed(q, values)]
    if missing:
        fail(f"figures in main.tex that no generated value rounds to: {missing}")
    # Negative control: without it, a bug that made `values` match everything would print green.
    if N.backed("0.987654", values):
        fail("the negative control value is present in the data; pick another")
    ivs = N.intervals(tex)
    if not ivs:
        fail("no intervals found in the prose; the pair check ran against nothing")
    bad = N.unpaired(ivs, rows)
    if bad:
        fail(f"intervals whose two bounds never co-occur in one generated row: {bad}")
    return (f"{len(quoted)} decimal figures in the prose, every one a correct rounding of a value "
            f"in {len(gen)} generated CSVs; {len(ivs)} intervals matched as ROW PAIRS "
            f"(negative control 0.987654 correctly absent)")


# The citation gate lives in checks_cite.py; the two prose gates live in checks_prose.py, with their own HERE/TEX so a control can patch the
# scope they read. prosecheck.py stays the rules vocabulary; checks_prose.py decides where each rule
# is enforced, which is the half that had the defect.

CHECKS = [("build is current", check_fresh), ("page count", check_pages), ("camera-ready byline", check_anonymous),
          ("exhibit budget", check_exhibits), ("no vertical rules", check_no_vrules),
          ("figures vector + serif", G.check_figures), ("main font Times", G.check_main_font),
          ("7pt floor", G.check_min_font),
          ("no overprinted text", G.check_no_overprint),
          ("tables match generator", G.check_tables_current),
          ("figures covered", G.check_figures_covered),
          ("numbers backed by CSV", check_numbers_backed), ("citations verified", C.check_citations),
          ("prose rules", R.check_prose), ("single-annotator language", R.check_second_reader),
          ("artifact pointer", B.check_artifact_pointer),
          ("one submittable PDF", S.check_one_pdf), ("paper.zip", B.check_zip),
          # AFTER paper.zip, which is what BUILDS the bundle. Ordered before it, this check failed
          # with "paper.zip does not exist" on any tree where the zip had not been built yet -- a
          # fresh clone, which is exactly the environment a reviewer runs it in.
          ("no paper PDF in the zip", S.check_zip_pdfs)]


def main() -> int:
    """Each check's own failure list decides its own verdict.

    The first version scanned a SHARED failure list for the check's name and, because a failure
    message never contains it, printed `ok` beside a check that had just failed. A verifier that
    prints ok on a failing check is the exact defect this file exists to prevent."""
    failed = []
    for name, fn in CHECKS:
        mine = []
        # A check that raises used to take the whole run down with it, so the checks after it
        # printed nothing at all. Nothing printed reads exactly like nothing wrong: check_min_font
        # raised on an empty regex match and the last five checks silently never ran. An
        # exception is now that check's own FAIL and the run continues.
        try:
            note = fn(mine.append)
        except Exception as e:                                    # noqa: BLE001
            mine.append(f"the check itself raised {type(e).__name__}: {e}")
            note = "CRASHED - see below; this is a failure, not a skip"
        print(f"  {'FAIL' if mine else 'ok  '}  {name:<24} {note}")
        for m in mine:
            print(f"          !! {m}")
        failed += [name] if mine else []
    print(f"\n{len(CHECKS) - len(failed)}/{len(CHECKS)} checks pass"
          + (f"; FAILED: {', '.join(failed)}" if failed else ""))
    return 1 if failed else 0


def selftest() -> None:
    """Prove the reporter goes RED, and that the geometry helpers discriminate."""
    print(" ", P.selftest())
    print(" ", G.selftest())
    print(" ", B.selftest())
    C._traceable_selftest()
    global CHECKS
    saved, CHECKS = CHECKS, [("planted", lambda fail: (fail("planted"), "planted")[1])]
    try:
        assert main() == 1, "a failing check must produce a non-zero exit code"
        # A raising check must be RED, not fatal. Without this the run stops at the exception and
        # every later check goes unreported, which is how five checks once passed by not running.
        def _boom(fail):
            raise RuntimeError("planted explosion")
        CHECKS = [("planted crash", _boom), ("planted ok", lambda fail: "fine")]
        assert main() == 1, "a check that RAISES must be reported as a failure, not abort the run"
    finally:
        CHECKS = saved
    print("  verify_paper selftest PASS - a planted failure prints FAIL and exits non-zero, and a "
          "planted crash is reported as that check's failure while the checks after it still run")


if __name__ == "__main__":
    sys.exit(selftest() or main() if "--selftest" in sys.argv else main())
