"""
Location: paper-a/paper/figproof.py
Purpose: The three proofs a validator cannot give, because each one is about the figure OUTSIDE
         the process that drew it: what it looks like with the colour taken away, what its
         smallest glyph measures at the size it is printed, and how it sits on the page it lands
         on. Every one is produced from the SHIPPED PDF, never from the figure in memory.
         Usage:  python3 paper/figproof.py [selftest]
Functions: greyscale(), chroma(), printed_sizes(), render(), figure_pages(), proofs(), selftest()
Calls: ghostscript (vector greyscale), PyMuPDF (raster + span sizes)
Imports: subprocess, pathlib, fitz
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from figstyle import COLPT                                       # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIGS = HERE / "figures"
OUT = ROOT / "out" / "figures"
FLOOR_PT = 7.0
PRINT_DPI = 300
PAGE_DPI = 150


def greyscale(src: Path, dest: Path) -> Path:
    """A vector greyscale copy, via ghostscript's colour-conversion device.

    Rasterising to grey and re-wrapping would prove nothing about a vector figure: it is the
    vector content a printer separates, so the conversion has to happen in that space."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite",
                    "-sColorConversionStrategy=Gray", "-dProcessColorModel=/DeviceGray",
                    "-dOverrideICC", f"-sOutputFile={dest}", str(src)],
                   check=True, capture_output=True, timeout=120)
    return dest


def chroma(pdf: Path, dpi: int = 150) -> int:
    """The largest channel spread in the rendered page: 0 iff every pixel is a true grey.

    The claim "this is the greyscale proof" is worth exactly as much as a check that the file is
    actually grey. A conversion that silently no-ops leaves a colour figure sitting in a folder
    called greyscale, which is worse than not shipping one."""
    import fitz
    doc = fitz.open(pdf)
    try:
        pix = doc[0].get_pixmap(dpi=dpi, colorspace=fitz.csRGB)
        buf = pix.samples
        return max(max(buf[i], buf[i + 1], buf[i + 2]) - min(buf[i], buf[i + 1], buf[i + 2])
                   for i in range(0, len(buf), 3))
    finally:
        doc.close()


def printed_sizes(pdf: Path) -> tuple:
    """(smallest authored span, printed size, scale) for one figure PDF.

    Read off the SHIPPED file's own text spans rather than from the generator's font constants.
    Those are different numbers whenever a glyph is drawn at a size no constant names, and the
    constant is the intention while the span is the artifact."""
    import fitz
    doc = fitz.open(pdf)
    try:
        sizes = [s["size"] for p in doc for b in p.get_text("dict")["blocks"]
                 for l in b.get("lines", []) for s in l["spans"] if s["text"].strip()]
        scale = COLPT / doc[0].rect.width
    finally:
        doc.close()
    if not sizes:
        raise SystemExit(f"{pdf.name}: zero text spans parsed. The font floor cannot be measured "
                         "against an empty parse, and an empty parse reports no violation.")
    return min(sizes), min(sizes) * scale, scale


def render(pdf: Path, dest: Path, dpi: int, page: int = 0) -> Path:
    """One page as a PNG at a stated dpi. The print-size proof and the on-page proof are the same
    operation at two resolutions and two sources, so they are one function."""
    import fitz
    dest.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf)
    try:
        doc[page].get_pixmap(dpi=dpi).save(dest)
    finally:
        doc.close()
    return dest


def figure_pages(main_pdf: Path) -> list:
    """The 1-based pages carrying a figure, found by their CAPTIONS.

    Derived from the document rather than listed here: a figure that moves to another page during
    a re-flow would otherwise be proved on the page it used to be on. Matched on "Figure N:" with
    the colon, which is the caption; a bare "Figure 3" is a cross-reference in the prose, and
    keying on that reported seven figure-bearing pages in a document with five figures."""
    import fitz
    import re
    doc = fitz.open(main_pdf)
    try:
        return sorted({i + 1 for i, p in enumerate(doc)
                       if re.search(r"Figure\s+\d+:", p.get_text())})
    finally:
        doc.close()


def proofs(main_pdf: Path = None) -> str:
    """All three proofs over every shipped figure, plus the on-page render. Raises on any figure
    that is not grey after conversion or whose smallest glyph prints under the floor."""
    figs = sorted(FIGS.glob("*.pdf"))
    if not figs:
        raise SystemExit("no figures to prove; refusing to report a clean proof over nothing")
    notes = []
    for f in figs:
        g = greyscale(f, OUT / "greyscale" / f"{f.stem}_grey.pdf")
        spread = chroma(g)
        if spread:
            raise SystemExit(f"{g.name} still carries colour (channel spread {spread}); the "
                             "greyscale proof would be a colour figure in a grey folder")
        render(g, OUT / "greyscale" / f"{f.stem}_grey.png", PAGE_DPI)
        authored, printed, scale = printed_sizes(f)
        if printed < FLOOR_PT:
            raise SystemExit(f"{f.name}: smallest glyph is {authored:.2f}pt authored and prints "
                             f"at {printed:.3f}pt (scale {scale:.4f}), under the {FLOOR_PT}pt "
                             "floor")
        render(f, OUT / "print300" / f"{f.stem}_300dpi.png", PRINT_DPI)
        notes.append(f"{f.stem}: grey clean, {authored:.2f}pt -> {printed:.3f}pt at scale "
                     f"{scale:.4f}")
    pages = figure_pages(main_pdf) if main_pdf and main_pdf.exists() else []
    for p in pages:
        render(main_pdf, OUT / "inpage150" / f"page{p:02d}.png", PAGE_DPI, page=p - 1)
    return (f"figproof: {len(figs)} figures -- greyscale vector proofs written and verified "
            f"chroma-free, {PRINT_DPI}dpi print-size renders written, smallest printed glyph "
            f"{min(printed_sizes(f)[1] for f in figs):.3f}pt (floor {FLOOR_PT}); "
            f"{len(pages)} figure-bearing pages rendered at {PAGE_DPI}dpi\n  "
            + "\n  ".join(notes))


def selftest() -> str:
    """The chroma detector must go RED on a colour page and GREEN on a grey one, or "the proofs
    are grey" is an assertion about a folder name. Driven on a two-page PDF built here, so it
    needs neither ghostscript's success nor a figure to already exist."""
    import fitz
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    tmp = Path(subprocess.run(["mktemp", "-d"], capture_output=True, text=True,
                              check=True).stdout.strip())
    fig, ax = plt.subplots(figsize=(1.5, 1.0))
    ax.bar([0, 1], [1, 2], color=["#CC3311", "#4477AA"])
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["a", "b"], fontsize=7)
    colour = tmp / "colour.pdf"
    fig.savefig(colour, format="pdf")
    plt.close(fig)
    assert chroma(colour) > 30, "a red-and-blue figure must read as coloured"
    grey_pdf = greyscale(colour, tmp / "grey.pdf")
    assert chroma(grey_pdf) == 0, "and its greyscale copy must read as a true grey"
    authored, printed, scale = printed_sizes(colour)
    assert abs(authored - 7.0) < 0.5, f"the span size is read off the file: {authored}"
    doc = fitz.open(colour)
    assert abs(scale - COLPT / doc[0].rect.width) < 1e-9, "the scale is the column over the file"
    doc.close()
    png = render(colour, tmp / "r.png", 300)
    assert png.stat().st_size > 1000, "a 300dpi render must produce a real image"
    return ("figproof selftest PASS - the chroma detector separates a colour page from a grey "
            "one (both arms), greyscale conversion is verified rather than assumed, span sizes "
            "and the column scale are read off the written file, and a 300dpi render lands")


if __name__ == "__main__":
    if "selftest" in sys.argv[1:]:
        print(selftest())
    else:
        print(proofs(HERE / "main.pdf"))
