"""
Location: paper-a/paper/pdfcheck.py
Purpose: Geometric and font facts about a compiled PDF, for verify_paper.py to assert on. Split out
         when the acceptance test crossed its LOC budget; keeping the parsing here leaves
         verify_paper.py as a readable list of checks.
Functions: run(), words(), overprints(), section_page(), page_count(), embedded_fonts(),
           scaled_tables(), selftest()
Calls: PyMuPDF (fitz) for word boxes; pdftotext / pdffonts / pdfinfo (poppler) for text and fonts
Imports: re, subprocess, pathlib, typing
"""

import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

MIN_X = 1.0          # horizontal overlap below this is kerning or a touching bounding box
MIN_Y_FRAC = 0.5     # vertical overlap must cover half the shorter word to count as one line

Word = Tuple[float, float, float, float, str]


def run(*cmd) -> str:
    return subprocess.run([str(c) for c in cmd], capture_output=True, text=True,
                          check=True).stdout


def words(pdf: Path) -> List[List[Word]]:
    """Per page, every word as (x0, y0, x1, y1, text).

    PyMuPDF, not `pdftotext -bbox`. Poppler's bbox mode aborts on the pdflatex build of this
    document (`std::out_of_range` out of a font table) and emits ZERO words while still exiting 0.
    A collision detector handed an empty word list reports "no collisions" with total confidence,
    which is the precise false green this module exists to prevent, so an empty parse is fatal
    here rather than merely unlikely."""
    import fitz                                                          # PyMuPDF
    doc = fitz.open(pdf)
    try:
        pages = [[(w[0], w[1], w[2], w[3], w[4]) for w in page.get_text("words")] for page in doc]
    finally:
        doc.close()
    if not any(pages):
        raise SystemExit(f"pdfcheck: extracted 0 words from {pdf}. The parser is broken, not the "
                         "document; refusing to certify a clean page out of an empty parse.")
    return pages


def _collisions(page: Sequence[Word], pno: int) -> List[str]:
    """Word pairs overlapping in BOTH axes, i.e. text printed on top of text.

    A sweep over words sorted by top edge, not a y-band bucket. Bucketing rounds two words on one
    visual line into two different buckets whenever they straddle a boundary, and then never
    compares them: a false GREEN manufactured by the indexing scheme rather than by the page."""
    ws = sorted(page, key=lambda w: w[1])
    out = []
    for i, (ax0, ay0, ax1, ay1, aw) in enumerate(ws):
        for bx0, by0, bx1, by1, bw in ws[i + 1:]:
            if by0 >= ay1:
                break                       # sorted by top edge, so no later word can overlap this
            dy = min(ay1, by1) - max(ay0, by0)
            dx = min(ax1, bx1) - max(ax0, bx0)
            if dx > MIN_X and dy > MIN_Y_FRAC * min(ay1 - ay0, by1 - by0):
                out.append(f"p{pno}: {aw!r} over {bw!r} ({dx:.1f}x{dy:.1f}pt)")
    return out


def overprints(pdf: Path) -> Dict[str, Any]:
    """Every overlapping word pair in the document.

    This exists because the pdflatex build printed the review-mode line number 265 through a table
    header. The table was not overfull, no warning fired, and the only evidence was the rendered
    page. A compile that reports no errors is not a page that reads correctly."""
    pages = words(pdf)
    hits: List[str] = []
    for pno, page in enumerate(pages, 1):
        hits += _collisions(page, pno)
    return {"hits": hits, "n_words": sum(len(p) for p in pages), "n_pages": len(pages)}


def section_page(pdf: Path, heading: str, n_pages: int) -> int:
    """First page carrying `heading` AS A HEADING, or 0 if absent. 0 is returned rather than a
    default page so a caller cannot mistake 'not found' for 'found on page 1'.

    A substring test is wrong here and was: it read the ordinary sentence "a defect we first
    shipped and report in Limitations" on page 3 as the start of the Limitations section, and
    reported main content ending five pages before it does. That is a false RED, which costs the
    same as a false green -- acted on, it would have had me cut a paper that already fitted. An
    unnumbered ACL section heading prints alone on its line, so the line must BE the heading."""
    for p in range(1, n_pages + 1):
        if heading_on_page(run("pdftotext", "-f", p, "-l", p, pdf, "-"), heading):
            return p
    return 0


def heading_on_page(text: str, heading: str) -> bool:
    """True when `heading` occupies a line of its own in `text`. Split out so the selftest can
    drive it on the exact page text that produced the false red, without needing a PDF."""
    return bool(re.search(rf"^\s*{re.escape(heading)}\s*$", text, re.M))


def pdf_width(pdf: Path) -> float:
    """Width of page 1 in points, taken off the written file.

    The authored figsize is NOT this number once savefig crops to the real ink, and it is this
    number, not the constant in the generator, that decides how far \\includegraphics scales a
    figure and therefore what size its smallest glyph prints at."""
    import fitz                                                          # PyMuPDF
    doc = fitz.open(pdf)
    try:
        return doc[0].rect.width
    finally:
        doc.close()


def page_count(pdf: Path) -> int:
    return int(re.search(r"^Pages:\s+(\d+)", run("pdfinfo", pdf), re.M).group(1))


def embedded_fonts(pdf: Path) -> List[str]:
    return [l for l in run("pdffonts", pdf).splitlines()[2:] if l.strip()]


BASE_PT = {"small": 10, "footnotesize": 9, "scriptsize": 8}


def scaled_tables(tables: Path) -> List[Tuple[str, float]]:
    """(filename, printed point size) for every table fragment wrapped in a \\resizebox. A table
    scaled to fit is still subject to the same 7pt floor as a figure, and the only way to know its
    printed size is to multiply its declared size by the scale."""
    out = []
    for f in sorted(tables.glob("*.tex")):
        text = f.read_text()
        m = re.search(r"\\resizebox\{([\d.]+)\\columnwidth\}", text)
        if not m:
            continue
        size = re.search(r"\\(footnotesize|scriptsize|small)\b", text)
        base = BASE_PT[size.group(1)] if size else BASE_PT["footnotesize"]
        out.append((f.name, base * float(m.group(1))))
    return out


def selftest() -> str:
    """Prove the collision detector fires on a real overlap and stays quiet on the three shapes
    that look like one, since a detector that never goes red is indistinguishable from a clean
    document, and one that fires on kerning would be silenced within a day."""
    adjacent = [(10.0, 5.0, 20.0, 12.0, "a"), (20.0, 5.0, 30.0, 12.0, "b")]
    assert _collisions(adjacent, 1) == [], "touching words must NOT count as overprinted"
    overlap = [(10.0, 5.0, 25.0, 12.0, "Trunc."), (18.0, 5.0, 28.0, 12.0, "265")]
    hits = _collisions(overlap, 4)
    assert hits and "265" in hits[0], f"a real overlap must be caught: {hits}"
    stacked = [(10.0, 5.0, 25.0, 12.0, "a"), (18.0, 40.0, 28.0, 47.0, "b")]
    assert _collisions(stacked, 1) == [], "same x range on DIFFERENT lines must not be reported"
    # A superscript shares a wide x range with its base and touches it vertically. Requiring the
    # overlap to cover half the shorter box is what separates it from a collision.
    supers = [(10.0, 100.0, 20.0, 110.0, "n"), (14.0, 96.0, 23.0, 101.0, "2")]
    assert _collisions(supers, 1) == [], "a superscript grazing its base is not an overprint"
    # The bucket bug this sweep replaces: one visual line whose two words straddle a rounding
    # boundary. A y/BAND bucket files them separately and never compares them.
    straddle = [(10.0, 101.9, 25.0, 109.0, "x"), (18.0, 102.1, 28.0, 109.2, "y")]
    assert _collisions(straddle, 2), "a collision must still be caught across a bucket boundary"
    # Heading detection, against the REAL sentence that broke it rather than an invented one. A
    # substring test read this line as the start of the Limitations section and put the end of the
    # main content on page 3 of an 8-page body.
    prose = ("each corrects a defect we first shipped and report in\nLimitations: sources are "
             "resolved by verified content\n")
    assert not heading_on_page(prose, "Limitations"), \
        "the word inside a sentence must NOT read as a section heading"
    assert heading_on_page("some text\nLimitations\nA single annotator", "Limitations"), \
        "the real heading, alone on its line, must still be found"
    assert not heading_on_page("Limitations of the method\n", "Limitations"), \
        "a heading-like line with trailing words is not the heading"
    return ("pdfcheck selftest PASS - collision fires on a real overlap and across a bucket "
            "boundary, ignores adjacency, stacking and superscripts, and heading detection "
            "separates a real section heading from the same word inside a sentence")


if __name__ == "__main__":
    # Running this file standalone used to print nothing and exit 0. The writing spec lists it as
    # a check that must pass, and a module that passes by having no entry point is the same green
    # as a module that ran and found nothing wrong. It now runs its own selftest and says so.
    print(selftest())
