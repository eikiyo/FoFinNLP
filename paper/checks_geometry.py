"""
Location: paper-a/paper/checks_geometry.py
Purpose: The acceptance checks that measure the RENDERED artifact's geometry rather than its text:
         are the figures vector and serif, does every glyph clear the 7pt floor at printed size,
         does any word print on top of another. Split out of verify_paper.py when that file passed
         its 300-LOC budget; the checks are unchanged and still take the same `fail` callback, so
         verify_paper's CHECKS table is the only thing that knows where they live.
Functions: check_figures(), smallest_size(), check_min_font(), check_tables_current(),
           check_no_overprint(), selftest()
Calls: pdfcheck.embedded_fonts, pdfcheck.scaled_tables, pdfcheck.overprints,
       figproof.printed_sizes (the shipped file's own text spans)
Imports: re, sys, pathlib, figproof, pdfcheck
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import figproof as FP                                            # noqa: E402
import pdfcheck as P                                             # noqa: E402

HERE = Path(__file__).resolve().parent
PDF = Path(os.environ.get("PAPER_PDF", HERE / ".lmk" / "main.pdf"))
FLOOR_PT = 7.0
COLPT = 219.086                                   # \the\columnwidth, measured from the compiled doc


def check_figures(fail) -> str:
    out = []
    for f in sorted((HERE / "figures").glob("*")):
        if f.suffix != ".pdf":
            fail(f"{f.name} is not a vector PDF")
            continue
        fonts = P.embedded_fonts(f)
        if any("Type 3" in l for l in fonts):
            fail(f"{f.name} embeds a Type 3 font; pdf.fonttype must be 42")
        # `Nimbus` alone matched NimbusSanL-Regu -- Nimbus SANS -- so a figure typeset entirely in a
        # sans face passed the serif test. Found by building a genuinely sans fixture as a positive
        # control for this gate (paper/gate_fixtures.py) and watching the gate accept it. The family
        # this project actually ships is Nimbus Roman, so the pattern names the serif variants and
        # excludes the sans one explicitly rather than matching the foundry.
        if not any(re.search(r"Times|Nimbus(?!San)|DejaVuSerif|STIX", l) for l in fonts):
            fail(f"{f.name} embeds no serif font: {[l.split()[0] for l in fonts]}")
        out.append(f"{f.name}: {len(fonts)} fonts, no Type 3")
    return "; ".join(out)


def smallest_size(fail, src: str = None):
    """The smallest authored point size, read from figstyle.py because that is where FS lives.

    It was read from make_figures.py until the constants moved there, after which the regex
    matched nothing, `min()` raised on the empty sequence, and the exception took the whole run
    down five checks early. A block of checks that stops printing looks exactly like a block that
    passed, so an unreadable source is now this check's own explicit failure.

    `src` is a parameter so the failure arm can be exercised by passing a string, rather than by
    a selftest that writes a decoy file next to the real one."""
    if src is None:
        src = (HERE / "figstyle.py").read_text()
    sizes = [int(v) for v in re.findall(r'"(?:axis|tick|annot|panel)": (\d+)', src)]
    if not sizes:
        fail("figstyle.py defines no FS sizes this check can read; the font floor was "
             "checked against nothing (did the constants move again?)")
        return None
    return min(sizes)


def check_min_font(fail) -> str:
    """The 7pt floor at the size things are PRINTED, not authored.

    The scale comes from each figure's OWN written width, not from the generator's COLWIDTH
    constant. Those are different numbers: savefig crops to the real ink, so a long tick label
    pushes the saved file past its authored size. This check previously divided by the constant
    and certified fig2 at 7.003pt while the shipped file printed at 6.899pt. It was measuring the
    intention rather than the artifact, which is the one thing a verifier must never do.

    The same error, one level down, survived that fix: the SIZE was still the smallest constant in
    figstyle, and no constant names the size mathtext gives a subscript. figA1's legend read
    "$r_{1/2}$", whose "1/2" set at 0.7 of 7pt and printed at 4.90pt while this check reported
    7.17. The size now comes from the shipped file's own text spans, so a glyph no constant
    predicts is measured like any other. The authored constant is still read, purely to report the
    two side by side when they disagree."""
    authored = smallest_size(fail)
    figs = sorted((HERE / "figures").glob("*.pdf"))
    if not figs:
        fail("no figure PDFs found; the font floor was checked against nothing")
    notes = []
    for f in figs:
        span, printed, scale = FP.printed_sizes(f)
        if printed < FLOOR_PT:
            fail(f"{f.name}: smallest glyph is {span:.2f}pt in the file and prints at "
                 f"{printed:.3f}pt, under the {FLOOR_PT}pt floor (scale {scale:.4f})")
        if authored and span < authored - 0.01:
            notes.append(f"{f.name} {span:.2f}pt (BELOW the {authored}pt constant) -> "
                         f"{printed:.3f}pt")
        else:
            notes.append(f"{f.name} {span:.2f}pt -> {printed:.3f}pt")
    for name, pt in P.scaled_tables(HERE / "tables"):
        if pt < FLOOR_PT:
            fail(f"{name} scaled to {pt:.2f}pt, under the {FLOOR_PT}pt floor")
        notes.append(f"{name} -> {pt:.2f}pt")
    return "; ".join(notes)


def check_tables_current(fail) -> str:
    """Re-run the table generator and require a zero-character diff against what is committed.

    Testing that the generator CAN be right proves nothing about the files actually in the build.
    Two captions in paper/tables were hardcoded strings sitting inside generated files, and went on
    stating a superseded partition (424 items, 46 flagged) while the columns beside them printed
    the current one. Every other check passed: the numbers-backed check scans decimals and these
    were integers, and nothing else compares a committed artifact to what its generator makes now.

    Nothing is written. The generator's functions are called for their return values and compared
    in memory, so a failing run cannot repair the defect it exists to report."""
    import make_tables as M
    stale, roster = [], M.tables()
    # The count is derived, not typed. It read "all 5 committed tables" for a run that had just
    # compared six, which is a coverage claim the check was in no position to make: a hardcoded
    # total cannot go stale loudly, so it under-reported exactly when a table had been added.
    on_disk = {p.stem for p in (HERE / "tables").glob("table*.tex")}
    uncovered = on_disk - {n for n, _ in roster}
    if uncovered:
        fail(f"tables committed but absent from make_tables.tables(), so nothing checks them: "
             f"{sorted(uncovered)}")
    for name, fn in roster:
        path = HERE / "tables" / f"{name}.tex"
        if not path.exists():
            stale.append(f"{name}.tex is missing entirely")
            continue
        if path.read_text().strip() != fn().strip():
            stale.append(f"{name}.tex differs from what make_tables.py produces now")
    if stale:
        fail("; ".join(stale) + " -- re-run python3 paper/make_tables.py")
    return (f"all {len(roster)} committed tables are byte-identical to a fresh generator run, and "
            f"every table*.tex on disk is covered by the generator's roster")


def check_figures_covered(fail) -> str:
    """Every figure*.pdf on disk must be in the generator's roster and included by main.tex.

    The table roster check earned this one. Figures had the identical hole and it was occupied:
    three PDFs from superseded layouts sat in paper/figures, were packaged into paper.zip, and
    PASSED the vector and 7pt checks, because those checks measure whatever files they are handed.
    A green from a check that ran over an artifact nothing generates and nothing includes is a
    green about the wrong thing. Both directions, so a figure the paper includes but the roster
    does not build is as loud as one left behind."""
    import make_figures as F
    roster = {n if n.endswith(".pdf") else f"{n}.pdf" for n, _ in F.figures()}
    on_disk = {p.name for p in (HERE / "figures").glob("*.pdf")}
    used = set(re.findall(r"\\includegraphics\[[^\]]*\]\{figures/([^}]+)\}",
                          (HERE / "main.tex").read_text()))
    for msg, names in (("figures on disk that no generator builds", on_disk - roster),
                       ("figures the generator builds that main.tex never includes", roster - used),
                       ("figures main.tex includes that are not on disk", used - on_disk)):
        if names:
            fail(f"{msg}: {sorted(names)}")
    return (f"{len(roster)} generated figures, every one included by main.tex, and no unbuilt "
            f"PDF left in paper/figures")


def check_no_overprint(fail) -> str:
    r = P.overprints(PDF)
    if r["hits"]:
        fail(f"{len(r['hits'])} overprinted word pairs: {r['hits'][:6]}")
    return f"{r['n_words']} words over {r['n_pages']} pages, none printed on top of another"


TIMES_RE = r"NimbusRomNo9L|TeXGyreTermes|TimesNewRoman|Times-Roman|STIXGeneral"


def has_times(fonts) -> bool:
    """Is a Times-family text face embedded at all? The regression this guards: main.tex without
    the template's font block ships the whole paper in Computer Modern, which the venue's
    aclpubcheck rejects as a wrong main font. CM stays legal in MATH (CMMI/CMSY and math-mode
    CMR digits survive under `times`), so the check asks for the presence of a Times face, not
    the absence of CM."""
    return any(re.search(TIMES_RE, l) for l in fonts)


def check_main_font(fail) -> str:
    fonts = P.embedded_fonts(PDF)
    if not fonts:
        fail(f"{PDF.name}: pdffonts returned no fonts; the check measured nothing")
        return ""
    if not has_times(fonts):
        fail(f"{PDF.name} embeds no Times-family text face (venue requirement); "
             f"got {[l.split()[0] for l in fonts[:6]]} -- is the template font block in main.tex?")
    n = sum(1 for l in fonts if re.search(TIMES_RE, l))
    return f"{n} Times-family faces among {len(fonts)} embedded fonts"


def selftest() -> str:
    """Prove the font-size reader BOTH finds the real sizes and reports their absence.

    One arm alone is not enough. A reader that returns None on everything would pass a
    can-it-report-absence test while certifying nothing, which is the failure that produced this
    module: absence was indistinguishable from a clean run."""
    got = []
    real = smallest_size(got.append)
    assert real is not None and not got, f"the real figstyle.py must yield sizes, got {real} {got}"
    assert real == 7, f"the floor is set by the smallest FS entry, expected 7 got {real}"
    missing = []
    assert smallest_size(missing.append, "# the constants moved\n") is None, \
        "a source with no FS dict must report None, not raise and not return a number"
    assert missing and "no FS sizes" in missing[0], f"and must say why, got {missing}"
    # The exact regression: make_figures.py no longer holds FS, so reading it must be a NAMED
    # failure rather than a crash. Asserted against the real file, not a fixture of one.
    moved = []
    assert smallest_size(moved.append, (HERE / "make_figures.py").read_text()) is None, \
        "make_figures.py must no longer be a source of FS sizes; if it is, they are duplicated"
    assert not has_times(["IOZDNS+CMR10   Type 1  yes", "EDFLQW+CMMI10  Type 1  yes"]), \
        "a CM-only font list must read as missing Times, or the font gate certifies nothing"
    assert has_times(["NJPQDJ+NimbusRomNo9L-Regu  Type 1  yes"]), "the real face must pass"
    assert not has_times([]), "an empty list must not pass"
    return ("checks_geometry selftest PASS - the size reader finds 7pt in the real figstyle, "
            "reports a named failure on a source without FS, confirms make_figures no longer "
            "carries a second copy of the sizes, and the Times gate goes red on a CM-only list")


if __name__ == "__main__":
    print(selftest())
