"""
Location: paper-a/paper/figpanels.py
Purpose: The individual axes of Figure 1, split out of make_figures.py when that file passed its
         300-line budget. One panel per function; make_figures owns layout, width assertion and
         saving, so a panel never decides how large the figure is or where it is written.
Functions: panel_label(), grid(), trim_ticks(), grid_x(), panel_contamination(),
           panel_p_distribution(), panel_frontier()
Calls: tablekit.read_csv
Imports: pathlib, tablekit
"""

from pathlib import Path

import tablekit as K

# Offset in points for a value label above its mark, and the error-bar cap half-width it has to
# clear. 0.03in is 2.16pt, so a label must stand off by more than CAP + 2.16 to satisfy the
# clearance rule; 7 leaves a measured margin rather than sitting on the threshold.
CAP = 2.4
LABEL_GAP = 7

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "out" / "tables" / "clean"

# Imported from the ONE style module rather than redeclared: a second copy of a colour is how two
# panels of one figure come to disagree about what "the rule colour" is.
from figstyle import COL, CONCEPT, FS, HATCH, INTERVAL, LABEL_BOX, LW   # noqa: E402


def panel_label(ax, text: str) -> None:
    """Draw nothing when the caller passes no letter.

    The panels used to hardcode their own. A panel's letter is a fact about where it sits in a
    figure, not about the panel, so panel_p_distribution announced itself as "(a)" while occupying
    slot (b) of Figure 1 and the caller's "(b)" landed on top of it. The overprint check caught
    two letters inside the same 9pt box; nothing else would have."""
    if not text:
        return
    # Clear of the axes on BOTH axes. At (-0.16, 1.04) the letter sat level with the topmost y
    # tick label and overlapped a four-digit one; the extra height costs nothing and the extra
    # width is inside the margin the tick labels already need.
    ax.text(-0.185, 1.07, text, transform=ax.transAxes, fontsize=FS["panel"], fontweight="bold",
            va="bottom", ha="left")


def grid(ax) -> None:
    ax.grid(axis="y", color=COL["grid"], alpha=0.4, linewidth=LW["grid"])
    ax.set_axisbelow(True)


def trim_ticks(ax) -> None:
    """Drop ticks that fall outside the axis limits.

    Matplotlib's locator picks round numbers for the DATA range and keeps the one just past the
    limit: a histogram topping out at 355 gets a tick at 400, which is not drawn inside the axes
    but whose text artist still exists, positioned above the canvas. The overlap gate reports it
    as CLIPPED-TOP and the saved figure carries the extra height, which then costs the figure its
    column width. Derived from the limits, so it cannot go stale the way a hand-set tick list can."""
    for axis, lim in ((ax.xaxis, ax.get_xlim()), (ax.yaxis, ax.get_ylim())):
        keep = [t for t in axis.get_ticklocs() if lim[0] - 1e-12 <= t <= lim[1] + 1e-12]
        if len(keep) != len(axis.get_ticklocs()):
            axis.set_ticks(keep)


def grid_x(ax) -> None:
    """The same rule for a horizontal-bar panel: the grid belongs on the VALUE axis, which is x
    once the bars are horizontal. Kept beside grid() rather than parameterised, because every call
    site knows which of the two it wants and a boolean argument reads as if it might not."""
    ax.grid(axis="x", color=COL["grid"], alpha=0.4, linewidth=LW["grid"])
    ax.set_axisbelow(True)


BUCKET_LABEL = {"clean": "clean", "computational": "computational",
                "evidence-absent": "evidence\nabsent",
                "quote-absent-from-source": "label\nuntraceable"}
BUCKET_ORDER = ("clean", "computational", "evidence-absent", "quote-absent-from-source")


def panel_contamination(ax, label: str = None) -> None:
    """Wobble by provenance group, with Wilson intervals. This is the paper's claim, so it is the
    first thing the figure says.

    Groups ordered by what the window supplies rather than by effect size: a reader should be able
    to read the ladder as a mechanism (the less the window contains, the more the model wavers) and
    not as a sorted bar chart, which would suggest the ordering was discovered rather than
    predicted. The untraceable-label group is drawn even though its interval crosses the clean
    rate, because a group shown only when it comes out positive is not a measurement."""
    rows = {r["group"]: r for r in K.read_csv(SRC.parent / "bucket_wobble.csv")}
    missing = [g for g in BUCKET_ORDER if g not in rows]
    if missing:
        raise SystemExit(f"bucket_wobble.csv is missing {missing} -- refusing to draw a "
                         f"contamination panel that silently omits a group")
    xs = range(len(BUCKET_ORDER))
    vals = [float(rows[g]["wobble"]) for g in BUCKET_ORDER]
    lo = [float(rows[g]["wobble"]) - float(rows[g]["lo"]) for g in BUCKET_ORDER]
    hi = [float(rows[g]["hi"]) - float(rows[g]["wobble"]) for g in BUCKET_ORDER]
    # The clean bar keeps the clean colour and the three flagged groups the flagged one, hatched,
    # so this panel and the repair panel beside it say the same thing with the same ink. Position
    # already carries the ladder; hatch carries the group in greyscale; colour is third.
    ax.bar(list(xs), vals, width=0.62,
           color=[CONCEPT["clean"] if g == "clean" else CONCEPT["flagged"] for g in BUCKET_ORDER],
           hatch=["" if g == "clean" else HATCH["flagged"] for g in BUCKET_ORDER],
           edgecolor="white", linewidth=0.4, zorder=2)
    ax.errorbar(list(xs), vals, yerr=[lo, hi], fmt="none", ecolor=INTERVAL,
                elinewidth=LW["interval"], capsize=CAP, zorder=4)
    ax.axhline(vals[0], color=COL["rule"], linestyle=":", linewidth=LW["rule"], zorder=1)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([BUCKET_LABEL[g] for g in BUCKET_ORDER], fontsize=FS["annot"])
    ax.set_ylabel("wobble", labelpad=7)
    ax.set_ylim(0, max(float(rows[g]["hi"]) for g in BUCKET_ORDER) * 1.18)
    for x, g in zip(xs, BUCKET_ORDER):
        # Offset in POINTS, not wobble: a data-unit offset resizes with the axis, and at 0.018
        # these labels rested on the interval caps they sit above.
        ax.annotate(f"n={rows[g]['items']}", xy=(x, float(rows[g]["hi"])),
                    xytext=(0, LABEL_GAP), textcoords="offset points", ha="center", va="bottom",
                    fontsize=FS["annot"])
    grid(ax)
    panel_label(ax, label)


def panel_p_distribution(ax, label: str = None) -> None:
    """The distribution of per-item correct rate p. Two bars dwarf the rest and that asymmetry IS
    the message, so the y-axis stays LINEAR: a log axis would make the corpus look balanced when
    the whole point of the panel is that it is not."""
    rows = K.read_csv(SRC / "item_p_distribution.csv")
    n = sum(int(r["n_items"]) for r in rows)
    lo = [float(r["bin_lo"]) for r in rows]
    cnt = [int(r["n_items"]) for r in rows]
    # The band count is READ, not re-derived. Summed here AND in the analysis, the two arithmetics
    # disagreed (112 pairs on the panel against 92 in the prose; np.linspace edges are
    # 0.30000000000000004 and 0.7000000000000001). One source, one number.
    band_rows = K.read_csv(SRC / "observable_band.csv")
    closed = next(r for r in band_rows if r["reading"] == "closed")
    band = int(closed["n_pairs"])
    if int(closed["n_total"]) != n:
        raise SystemExit(f"observable_band.csv counts {closed['n_total']} pairs but the "
                         f"distribution holds {n} -- the two artifacts describe different data")
    ax.axvspan(0.3, 0.7, color=COL["band"], zorder=0)
    ax.bar(lo, cnt, width=0.1, align="edge", color=COL["single"], edgecolor="white",
           linewidth=0.4, zorder=2)
    ax.set_xlim(0, 1)
    # The first x tick label is LEFT-aligned so it clears the y axis's own "0" in the corner.
    # Dropping the tick would hide where the distribution starts, which is the more expensive fix.
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    # Just enough headroom for the label. Raising it to 1.38 to fit a second annotation line took
    # the axis to 6000 and left the 4,408 bar looking mid-sized, which drains the one thing this
    # panel exists to show. The second line moved to the caption instead.
    ax.set_ylim(0, max(cnt) * 1.16)
    ax.set_xlabel("per-item correct rate $p$")
    ax.set_ylabel("model-item pairs")
    # Right-aligned at the axis edge, so it grows LEFTWARDS over empty plot area instead of past
    # the canvas. Text that overruns the canvas widens the saved file, which then gets scaled DOWN
    # to the column and drags every glyph under the 7pt floor.
    # 86.8% is the share with p >= 0.9, while Section 3 quotes 84.7% for the narrower p = 1. Two
    # true numbers about two different sets read as a contradiction unless something says which set
    # is on the chart; the caption does, because a second line here costs the panel its point.
    ax.annotate(f"{cnt[-1]:,} ({100 * cnt[-1] / n:.1f}%)", xy=(1.0, cnt[-1]),
                xytext=(0, LABEL_GAP), textcoords="offset points", ha="right", va="bottom",
                fontsize=FS["annot"])
    ax.annotate(f"{cnt[0]:,}", xy=(0.05, cnt[0]), xytext=(0.05, max(cnt) * 0.16),
                ha="center", fontsize=FS["annot"])
    # No leader line: in a HISTOGRAM a stroke running from the caption to y=0 is what a bar looks
    # like, and at print size it read as a ~1,900-count spike at p=0.5. Every gate passed it (a
    # line, colliding with nothing); only the render showed it. The band does the pointing.
    ax.text(0.5, max(cnt) * 0.58, f"observable band:\n{band} pairs ({100 * band / n:.1f}%)",
            ha="center", va="center", fontsize=FS["annot"])
    trim_ticks(ax)
    ax.get_xticklabels()[0].set_ha("left")
    grid(ax)
    panel_label(ax, label)


def panel_frontier(ax, label: str = None) -> None:
    """Observed against structurally reachable wobble, by accuracy decile."""
    rows = [r for r in K.read_csv(SRC / "accuracy_decile_frontier.csv") if int(r["n_leaves"])]
    x = [float(r["accuracy_decile"].split("-")[0]) + 0.05 for r in rows]
    obs = [float(r["max_observed_wobble"]) for r in rows]
    stru = [float(r["max_structural_wobble"]) for r in rows]
    ax.plot(x, obs, marker="o", markersize=3.2, color=COL["observed"], linewidth=LW["series"],
            linestyle="-", zorder=3, label="observed max")
    ax.plot(x, stru, marker="s", markersize=3.0, color=COL["flagged"], linewidth=LW["series"],
            linestyle="--", zorder=3, label="structural max")
    ax.axhline(0.30, color=COL["rule"], linestyle=":", linewidth=LW["rule"], zorder=1)
    # No task in the corpus is below 0.6 accurate, so the axis starts at the data rather than at
    # zero. Held at 0 to 1 the four deciles were squeezed into the right third of the panel and the
    # shape of both curves was unreadable. The y axis still starts at zero, which is the axis where
    # a truncated origin would misstate a magnitude; the caption states the omitted range.
    lo = min(x) - 0.07
    ax.set_xlim(lo, 1.0)
    ax.set_ylim(0, 0.42)
    # Masked: this label names the rule it sits on, and unmasked it cleared it by only 0.0177in.
    ax.text(lo + 0.01, 0.318, "stage-2 threshold 0.30", fontsize=FS["annot"],
            color=COL["single"], bbox=dict(LABEL_BOX))
    # The style rule prefers direct labels; this is the measured exception. Three anchors were
    # tried and each collides -- a 7pt label is 0.55in of a 2.6in x 1.0in panel with two crossing
    # series, so above the first point it ends under its own curve (which climbs 0.15in across the
    # label while the label stands off 0.10in) and below either peak it lands on the other series
    # (the band is 0.13-0.25in and the label needs 0.16in plus room for the curves to move). The
    # clear space is the upper right, and only a legend can use it. figclearance measures its
    # text against the data like any other label.
    ax.legend(frameon=False, loc="upper right", fontsize=FS["annot"], handletextpad=0.4,
              borderpad=0.0, labelspacing=0.25, borderaxespad=0.15, handlelength=1.6)
    ax.set_xlabel("task accuracy (decile midpoint)")
    ax.set_ylabel("wobble")
    grid(ax)
    panel_label(ax, label)
