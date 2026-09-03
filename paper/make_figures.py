"""
Location: paper-a/paper/make_figures.py
Purpose: Generate paper/figures/*.pdf from out/tables/*.csv. Vector PDF only, serif to match the
         body text, Tol-bright palette, every series carrying a marker, a hatch or a position
         before it carries a colour so the figures survive a black-and-white print. Nothing
         default: matplotlib is never allowed to auto-assign a colour or a size. Every figure
         passes figgate (the visual-intelligence engine's validators) before it is written.
         Usage:  python3 paper/make_figures.py
Functions: fig1_lineup(), fig2_contamination(), fig3_transfer(), fig4_observability(),
           figA1_reliability(), figures(), write(), main()
           Each figN returns a figgate.Build (the drawn figure plus its gate arguments); write()
           gates it and writes the PDF, so figaudit can audit the identical object that ships.
Calls: tablekit.read_csv, figgate.gate, figaudit.manual_checks, figpanels, figevidence
Imports: sys, pathlib, matplotlib, tablekit, figgate, figpanels, figevidence
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib                                                # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                  # noqa: E402

import tablekit as K                                             # noqa: E402
import figevidence as FE                                         # noqa: E402
import figgate as G
import figscript as SG                                              # noqa: E402
import figpanels as FP                                           # noqa: E402
import pdfcheck as P                                             # noqa: E402
import figaudit as FA                                            # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "out" / "tables" / "clean"
DEST = Path(__file__).resolve().parent / "figures"

# Every visual constant lives in figstyle, imported by BOTH this module and figpanels.
from figstyle import COL, COLPT, COLWIDTH, CONCEPT, FS, LABEL_BOX, LW   # noqa: E402
from figstyle import TEXT_COL, WIDTH_FLOOR                                          # noqa: E402
from figstyle import apply as style                                                 # noqa: E402

# The registered repair threshold, read from the pre-registration by the module that already
# parses it, never restated here. A threshold typed into a figure is a threshold that can drift
# from the document that fixed it.
from table_repair import registered_threshold                                       # noqa: E402


def fig1_lineup() -> Path:
    """Who wobbles. Twelve configurations across a broken axis, which replaces the wobble columns
    Table 1 used to carry."""
    # 3.3in tall for twelve rows. At 2.55 the rows were 11pt apart and the 7pt value labels at the
    # bar ends overlapped each other; the height is set by the row count and the font floor, not
    # chosen. A shorter figure would have to drop the values, and Table 1 no longer carries them.
    fig, axes = plt.subplots(1, 2, figsize=(COLWIDTH["fig1_lineup.pdf"], 3.3),
                             gridspec_kw={"width_ratios": [3.0, 1.0], "wspace": 0.09})
    FE.panel_lineup(axes[0], axes[1])
    fig.subplots_adjust(left=0.30, right=0.90, top=0.985, bottom=0.135)
    # The tail panel is a magnified SEGMENT of a broken axis and starts at 0.27, which is a
    # truncation and is declared as one. It carries three ticks, so the engine's tick-density
    # floor needs no relaxation.
    return G.Build(fig, "fig1_lineup.pdf", "clean/model_summary.csv",
                   {"clean": CONCEPT["clean"]}, allow_truncation=(False, True))


def fig2_contamination() -> Path:
    """The paper's central exhibit: the association, and the repair that did not explain it.
    Both panels are on the wobble scale, so the reader compares them without converting."""
    # STACKED, not side by side. Side by side, panel (a)'s four category labels overlapped each
    # other at half width and the panel letters landed on the neighbouring axis's ticks: a
    # four-category ladder needs the whole column. Stacking also lets align_panel_axes do
    # something a reader can use, since the two panels then share a vertical scale.
    fig, axes = plt.subplots(2, 1, figsize=(COLWIDTH["fig2_contamination.pdf"], 3.35))
    FP.panel_contamination(axes[0], "(a)")
    FE.panel_repair(axes[1], registered_threshold(), "(b)")
    G.engine()["align_panel_axes"](list(axes), shared="y")
    fig.subplots_adjust(hspace=0.60, left=0.19, right=0.985, top=0.95, bottom=0.145)
    return G.Build(fig, "fig2_contamination.pdf", "bucket_wobble.csv + repair_by_task.csv",
                   {"clean": CONCEPT["clean"], "flagged": CONCEPT["flagged"],
                    "observed": CONCEPT["observed"]})


def fig3_transfer() -> Path:
    """The strongest positive result, against the null that makes it a result."""
    fig, ax = plt.subplots(figsize=(COLWIDTH["fig3_transfer.pdf"], 1.95))
    FE.panel_transfer_null(ax)
    fig.subplots_adjust(left=0.175, right=0.985, top=0.93, bottom=0.26)
    return G.Build(fig, "fig3_transfer.pdf", "transfer_null_draws.csv + transfer_items.csv",
                   {"observed": CONCEPT["observed"], "null": CONCEPT["null"]})


def fig4_observability() -> Path:
    """What the instrument can resolve: where measurements sit, and the ceiling above them."""
    fig, axes = plt.subplots(2, 1, figsize=(COLWIDTH["fig4_observability.pdf"], 3.5))
    FP.panel_p_distribution(axes[0], "(a)")
    FP.panel_frontier(axes[1], "(b)")
    fig.subplots_adjust(hspace=0.70, left=0.205, right=0.985, top=0.93, bottom=0.115)
    return G.Build(fig, "fig4_observability.pdf",
                   "clean/item_p_distribution.csv + clean/accuracy_decile_frontier.csv",
                   {"observed": CONCEPT["observed"], "flagged": CONCEPT["flagged"]})


def figA1_reliability() -> Path:
    """Half-length and corrected reliability per configuration, connected by a hairline. A dot
    plot, not bars: the quantity is a correlation, and a bar from zero implies a ratio scale."""
    rows = sorted(K.read_csv(SRC / "split_half_reliability.csv"),
                  key=lambda r: float(r["r_full"]))
    y = range(len(rows))
    half = [float(r["r_half"]) for r in rows]
    full = [float(r["r_full"]) for r in rows]
    med = sorted(full)[len(full) // 2 - 1:len(full) // 2 + 1]
    fig, ax = plt.subplots(figsize=(COLWIDTH["figA1_reliability.pdf"], 2.5))
    for i, (a, b) in enumerate(zip(half, full)):
        ax.plot([a, b], [i, i], color=COL["grid"], linewidth=LW["grid"], zorder=1)
    # The open circles draw ON TOP of the filled diamonds, zorder 4 against 3. Two configurations
    # have r_half = r_full = 1 exactly, so their two markers coincide; drawn underneath, the circle
    # vanished and those rows read as missing data rather than as a perfect correlation.
    # No subscript: mathtext sets one at 0.7 of its base, so "$r_{1/2}$" at 7pt printed at 4.90pt
    # while check_min_font read the authored constant and passed it. Both ends are fixed.
    h_full = ax.scatter(full, y, marker="D", s=10, color=COL["flagged"], zorder=3,
                        label="Spearman-Brown $r$")
    h_half = ax.scatter(half, y, marker="o", s=11, facecolors="none", edgecolors=COL["observed"],
                        linewidths=0.8, zorder=4, label="observed half-length $r$")
    ax.axvline(sum(med) / 2, color=COL["rule"], linestyle=":", linewidth=LW["rule"], zorder=2)
    ax.text(sum(med) / 2 - 0.008, -0.55, f"median {sum(med) / 2:.3f}",
            fontsize=FS["annot"], color=COL["single"], ha="right", bbox=dict(LABEL_BOX))
    ax.set_yticks(list(y))
    ax.set_yticklabels([K.display_name(r["model"]).replace(r"\_", "_") for r in rows],
                       fontsize=FS["annot"])
    ax.set_xlabel("split-half reliability")
    ax.set_xlim(0.55, 1.02)
    ax.set_ylim(-0.9, len(rows) - 0.3)
    # A legend, not direct labels: every configuration's two markers sit close together near the
    # right edge, so the two labels landed on each other. The style rule bans a legend only where
    # direct labelling fits. Handles are passed explicitly because legend order otherwise follows
    # creation order (diamonds first, for a drawing reason) and would print the corrected value
    # above the observed one it derives from.
    ax.legend([h_half, h_full], ["observed half-length $r$", "Spearman-Brown $r$"],
              frameon=False, loc="upper left", fontsize=FS["annot"], handletextpad=0.25,
              borderpad=0.0, labelspacing=0.25, borderaxespad=0.2)
    FP.trim_ticks(ax)
    ax.grid(axis="x", color=COL["grid"], alpha=0.4, linewidth=LW["grid"])
    ax.set_axisbelow(True)
    # Explicit margins. This figure previously leaned on bbox_inches="tight" to make room for the
    # model names, which works for the WRITTEN file but leaves them hanging off the in-memory
    # canvas, where the clipping gate correctly reports five of them as running off the edge.
    fig.subplots_adjust(left=0.30, right=0.985, top=0.965, bottom=0.155)
    return G.Build(fig, "figA1_reliability.pdf", "clean/split_half_reliability.csv",
                   {"observed": CONCEPT["observed"], "flagged": CONCEPT["flagged"]})


def write(b) -> Path:
    """Vector PDF, always, and only after every applicable engine gate has passed.

    The suffix is asserted rather than trusted to the call site: a raster figure in an ACL
    submission reads as carelessness. `source` names the CSV the figure is drawn from and is
    written into the PDF's own metadata, so provenance is machine-readable off the shipped file
    rather than a claim in a comment."""
    fig, name, source = b.fig, b.name, b.source
    if not name.endswith(".pdf"):
        raise ValueError(f"figures must be vector PDF, got {name!r}")
    print(f"    {G.gate(fig, name, FS, b.concepts, TEXT_COL, b.allow_truncation, b.min_ticks)}")
    for label, hits in FA.manual_checks(fig).items():
        if hits:
            raise SystemExit(f"{name}: {label} -- " + "; ".join(hits))
    DEST.mkdir(parents=True, exist_ok=True)
    path = DEST / name
    # CreationDate suppressed so re-running is byte-identical. For a committed generated artifact
    # the load-bearing test is not "the generator works" but "re-running it changes nothing", and a
    # wall-clock timestamp inside the file makes that test impossible to run.
    #
    # Written via a temp file and moved into place only when the bytes differ. An unconditional
    # save moves the mtime every run, which made the compiled PDF read as stale to an mtime-based
    # freshness check while latexmk, comparing content, correctly reported nothing to do.
    tmp = path.with_suffix(".pdf.tmp")
    fig.savefig(tmp, format="pdf",
                metadata={"CreationDate": None, "Subject": f"generated from out/tables/{source}",
                          "Creator": "paper/make_figures.py"})
    plt.close(fig)
    if path.exists() and path.read_bytes() == tmp.read_bytes():
        tmp.unlink()
    else:
        tmp.replace(path)
    _assert_width(path)
    return path


def _assert_width(path: Path) -> float:
    """Refuse to ship a figure the column will have to shrink.

    Measured off the WRITTEN file, because the authored figsize is not the saved width once
    bbox_inches crops to the real ink. A figure wider than the column is scaled down by
    \\includegraphics and takes every glyph in it below the 7pt floor, silently: no warning fires,
    the compile is clean, and only arithmetic on the two widths shows it."""
    w = P.pdf_width(path)
    if w > COLPT or w < WIDTH_FLOOR * COLPT:
        want = COLWIDTH[path.name] * COLPT / w
        raise SystemExit(
            f"{path.name} saved at {w:.2f}pt against a {COLPT:.2f}pt column "
            f"(printed scale {COLPT / w:.4f}). Set COLWIDTH[{path.name!r}] near {want:.3f}.")
    return w


def figures() -> tuple:
    """The ONE roster. Derived from here by the generator, the freshness check and the count in
    every message, so a figure added without registering it is loud rather than invisible."""
    return (("fig1_lineup", fig1_lineup), ("fig2_contamination", fig2_contamination),
            ("fig3_transfer", fig3_transfer), ("fig4_observability", fig4_observability),
            ("figA1_reliability", figA1_reliability))


def main() -> None:
    style()
    print(f"  {G.selftest()}")
    # The engine's STATIC checker, run on the build scripts before any of them executes, which is
    # the order its own docstring asks for. It raises on four of the five; every class it raises is
    # declared inapplicable in figgate.SCRIPT_EXEMPT with the reason, and anything else propagates.
    print(f"  {SG.selftest()}")
    for _name, fn in figures():
        p = write(fn())
        print(f"  wrote {p.relative_to(ROOT)}  ({p.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
