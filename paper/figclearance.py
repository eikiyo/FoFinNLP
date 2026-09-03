"""
Location: paper-a/paper/figclearance.py
Purpose: The GEOMETRY check no engine gate performs. validate() and validate_collision_physics()
         test whether two things OVERLAP; neither asks how close a label sits to the mark it
         labels once they have stopped overlapping. layout-math.md fixes the minimum at 0.03in for
         a data label and 0.1in for a panel label, and a label 0.005in off a bar is touching it on
         the printed page even though no gate reports a collision.
Functions: estimate_text_width_inches(), annotations(), clearance(), marks(),
           clearance_violations(), width_violations(), selftest()
Calls: matplotlib artist geometry only
Imports: re, matplotlib
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib                                                # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                  # noqa: E402
from matplotlib.colors import to_rgba                            # noqa: E402
from matplotlib.text import Annotation, Text                     # noqa: E402
from matplotlib.transforms import Bbox                           # noqa: E402

# layout-math.md: "Data labels <-> data points 0.03in offset", "Panel label (a,b) <-> axes 0.1in
# outside bounds". Named here rather than inlined at the comparison so the two thresholds are
# visible in one place and a reader can see which one a violation was measured against.
CLEAR_DATA_IN = 0.03
CLEAR_PANEL_IN = 0.10
MAX_LABEL_FRAC = 0.8
PANEL = re.compile(r"^\([a-z]\)$")
NO_LINE = (None, "None", "none", " ", "")


def estimate_text_width_inches(text: str, fontsize_pt: float) -> float:
    """layout-math.md's estimator, reproduced exactly as that document defines it. Used ALONGSIDE
    the rendered width rather than instead of it: the estimate assumes 0.6em per character, which
    a proportional serif does not honour, so the check takes whichever is larger."""
    return max((len(line) for line in text.splitlines()), default=0) * (fontsize_pt / 72) * 0.6


def annotations(ax):
    """The texts a caller PLACED, which is what the clearance rule is about.

    `ax.texts` holds exactly those: tick labels, axis labels and the title live on the axis and
    the axes, not in this list, so the check cannot drown in the hundreds of tick-label-to-spine
    gaps that are 0 by design and mean nothing.

    Legend entries are included. A legend inside the axes is the commonest way a figure ends up
    with text on top of data, and leaving it out would mean the one placement most likely to
    collide was the one placement never measured."""
    leg = ax.get_legend()
    return list(ax.texts) + (list(leg.get_texts()) if leg else [])


def clearance(a: Bbox, b: Bbox, dpi: float) -> float:
    """Gap between two DISPLAY boxes, in inches. Zero when they overlap, which is the collision
    case and is the same violation: a label ON its mark and a label 0.001in off it read identically.

    Display units are pixels at the figure's dpi, NOT points. Dividing by 72 instead of by dpi
    reported every gap 2.8x larger than it is at this paper's dpi of 200, which is a checker too
    LENIENT to catch what it exists to catch -- a false green manufactured by a unit."""
    dx = max(b.x0 - a.x1, a.x0 - b.x1, 0.0)
    dy = max(b.y0 - a.y1, a.y0 - b.y1, 0.0)
    return (dx ** 2 + dy ** 2) ** 0.5 / dpi


def _pad(box: Bbox, pts: float, dpi: float) -> Bbox:
    d = pts / 72.0 * dpi / 2.0
    return Bbox([[box.x0 - d, box.y0 - d], [box.x1 + d, box.y1 + d]])


def _spans(pts) -> list:
    """Per-SEGMENT boxes along a polyline. The union box of a curve covers the empty area under
    it, so measuring against it reports a label in clear space as touching the line: the first
    version of this module read 'observed max', placed 6pt off its own first data point, as a
    zero-gap collision with a curve that is nowhere near it."""
    if len(pts) < 2:
        return [Bbox([[p[0], p[1]], [p[0], p[1]]]) for p in pts]
    return [Bbox([[min(a[0], b[0]), min(a[1], b[1])], [max(a[0], b[0]), max(a[1], b[1])]])
            for a, b in zip(pts[:-1], pts[1:])]


def _line_marks(ln, dpi: float) -> list:
    """A Line2D as the marks a reader sees: its segments, or its markers when it draws no line."""
    pts = ln.get_transform().transform(ln.get_xydata())
    if not len(pts):
        return []
    ms = 0.0 if ln.get_marker() in NO_LINE else ln.get_markersize()
    if ln.get_linestyle() in NO_LINE:
        return [_pad(Bbox([[p[0], p[1]], [p[0], p[1]]]), max(ms, 1.0), dpi) for p in pts]
    return [_pad(b, ms, dpi) for b in _spans(pts)]


def _coll_marks(c, dpi: float) -> list:
    """A Collection as its segments (an error bar, a hairline) or its markers (a scatter). Same
    reason as _line_marks: an error-bar collection's union box spans every bar in the panel, and
    every value label inside that rectangle was being reported against it."""
    if hasattr(c, "get_segments") and c.get_segments():
        out = []
        for seg in c.get_segments():
            out += _spans(c.get_transform().transform(seg))
        return out
    off = c.get_offsets()
    if off is not None and len(off):
        sizes = list(c.get_sizes()) or [16.0]
        pts = c.get_offset_transform().transform(off)
        return [_pad(Bbox([[p[0], p[1]], [p[0], p[1]]]),
                     sizes[i % len(sizes)] ** 0.5, dpi) for i, p in enumerate(pts)]
    return [c.get_window_extent()]


def marks(ax, skip_ids, dpi: float) -> list:
    """Every data mark in the axes, as fine-grained display boxes.

    Spines, grid lines and the axes background are excluded because they are the frame, not the
    data. So is anything at zorder <= 0: a highlight band is drawn BEHIND every mark on purpose,
    and a caption placed inside it is using it, not colliding with it."""
    out = []
    for p in ax.patches:
        if id(p) not in skip_ids and p.get_visible() and p.get_zorder() > 0:
            out.append(p.get_window_extent())
    for ln in ax.lines:
        if id(ln) not in skip_ids and ln.get_visible() and ln.get_zorder() > 0:
            out += _line_marks(ln, dpi)
    for c in ax.collections:
        if id(c) not in skip_ids and c.get_visible() and c.get_zorder() > 0:
            out += _coll_marks(c, dpi)
    return out


def glyph_box(t) -> Bbox:
    """The box the GLYPHS occupy.

    Annotation.get_window_extent() bounds the text AND its arrow, so a caption with a leader line
    reports a box reaching all the way down to the point it points at -- 120 display units tall for
    two lines of 7pt -- and every mark under the leader reads as a collision with the label. The
    base Text implementation is called explicitly to get the text alone."""
    return Text.get_window_extent(t)


def _mask(t) -> bool:
    """True when the text carries an opaque background box.

    A reference-line label is SUPPOSED to sit on its rule -- that is what makes it that rule's
    label -- and layout-math's answer is a background box in the figure colour so the rule does not
    run through the glyphs. A masked label has therefore satisfied the rule, not evaded it."""
    bb = t.get_bbox_patch()
    return bool(bb) and to_rgba(bb.get_facecolor())[3] >= 0.9


def clearance_violations(fig) -> list:
    """Every placed text closer to a data mark than its threshold allows, with the measured gap.

    An annotation's own arrow is excluded from its nearest-element search: an arrow that touches
    the point it points at is the arrow working."""
    fig.canvas.draw()
    out = []
    for ax in fig.get_axes():
        for t in annotations(ax):
            if not t.get_text().strip():
                continue
            panel = bool(PANEL.match(t.get_text().strip()))
            floor = CLEAR_PANEL_IN if panel else CLEAR_DATA_IN
            skip = {id(t.arrow_patch)} if isinstance(t, Annotation) and t.arrow_patch else set()
            boxes = marks(ax, skip, fig.dpi)
            if not boxes or (_mask(t) and not panel):
                continue
            gap = min(clearance(glyph_box(t), m, fig.dpi) for m in boxes)
            if gap < floor:
                out.append(f"{'panel label' if panel else 'label'} "
                           f"{t.get_text().replace(chr(10), ' / ')[:34]!r}: "
                           f"{gap:.4f}in < {floor}in")
    return out


def width_violations(fig) -> list:
    """Every placed text wider than MAX_LABEL_FRAC of the axes it sits in.

    Both widths are computed and the larger is used. The estimator in layout-math.md is a
    fixed-pitch approximation and under-reads a proportional serif at capital letters; the rendered
    width is exact but exists only after a draw. Taking the max fails closed on either."""
    fig.canvas.draw()
    out = []
    for ax in fig.get_axes():
        ax_in = ax.get_window_extent().width / fig.dpi
        for t in annotations(ax):
            txt = t.get_text().strip()
            if not txt:
                continue
            wide = max(estimate_text_width_inches(txt, t.get_fontsize()),
                       glyph_box(t).width / fig.dpi)
            if wide > MAX_LABEL_FRAC * ax_in:
                out.append(f"label {txt.splitlines()[0][:30]!r}: {wide:.3f}in > "
                           f"{MAX_LABEL_FRAC:.0%} of a {ax_in:.3f}in axis")
    return out


def _probe(label_y, ax_w=2.0, dpi=200):
    fig, ax = plt.subplots(figsize=(ax_w, 1.5), dpi=dpi)
    ax.bar([0], [1.0], color="#4477AA")
    ax.set_ylim(0, 1.6)
    ax.text(0, label_y, "n=42", ha="center", va="bottom", fontsize=7)
    fig.canvas.draw()
    return fig, ax


def _unit_arm() -> None:
    """The unit and geometry arms: a gap in inches must not depend on the figure's dpi, and a
    label in the empty space under a curve must not be reported against that curve."""
    a = Bbox([[0, 0], [100, 100]])
    assert abs(clearance(a, Bbox([[110, 0], [200, 100]]), 200) - 0.05) < 1e-9, \
        "10 display units at 200 dpi is 0.05in"
    assert abs(clearance(a, Bbox([[110, 0], [200, 100]]), 100) - 0.10) < 1e-9, \
        "the SAME box gap is 0.10in at 100 dpi -- dividing by a constant 72 would call both 0.139"
    assert clearance(a, Bbox([[50, 50], [150, 150]]), 200) == 0.0, "overlapping boxes: zero gap"
    fig, ax = plt.subplots(figsize=(2.0, 1.5), dpi=200)
    ax.plot([0, 1, 2], [0, 1, 2], color="#2c3e50")          # a rising line; below it is empty
    ax.text(1.6, 0.2, "clear", fontsize=7)
    fig.canvas.draw()
    assert clearance_violations(fig) == [], \
        "a label under a rising line is in empty space; the line's UNION box says otherwise"
    plt.close(fig)


def _arrow_arm() -> None:
    """An annotation with a leader line must be measured on its GLYPHS. The fixture places the
    caption in clear space and points it at a bar; the whole-annotation box would span the leader
    and read as a collision with the very bar the caption is about."""
    fig, ax = plt.subplots(figsize=(2.0, 1.5), dpi=200)
    ax.bar([0], [0.2], color="#4477AA")
    ax.set_ylim(0, 1.6)
    ax.annotate("caption", xy=(0, 0.2), xytext=(0, 1.2), ha="center", fontsize=7,
                arrowprops=dict(arrowstyle="-", color="#333333"))
    fig.canvas.draw()
    assert clearance_violations(fig) == [], \
        "a caption 1.0 data units clear of its bar collides with nothing but its own leader"
    plt.close(fig)


def selftest() -> str:
    """Both arms of both checks, plus the two exemptions and the unit arm, each driven on a
    fixture that differs from its opposite in one number."""
    assert abs(estimate_text_width_inches("abcd", 7) - 4 * 7 / 72 * 0.6) < 1e-9, "the doc formula"
    assert estimate_text_width_inches("ab\nabcdef", 7) > estimate_text_width_inches("ab", 7), \
        "a multi-line label is as wide as its LONGEST line, not its first"
    _unit_arm()
    _arrow_arm()

    tight, _ = _probe(1.001)                      # label essentially resting on the bar top
    hits = clearance_violations(tight)
    assert hits and "n=42" in hits[0], f"a label touching its bar must be caught: {hits}"
    plt.close(tight)
    clear, _ = _probe(1.20)                       # the same label, moved up
    assert clearance_violations(clear) == [], "a well-cleared label must PASS"
    plt.close(clear)

    # A masked reference-line label is exempt; the SAME label without the mask is not.
    masked, ax = _probe(1.001)
    ax.texts[0].set_bbox(dict(facecolor="white", edgecolor="none", pad=0.5))
    masked.canvas.draw()
    assert clearance_violations(masked) == [], "an opaquely-masked label satisfies the rule"
    ax.texts[0].set_bbox(dict(facecolor="white", edgecolor="none", alpha=0.3, pad=0.5))
    masked.canvas.draw()
    assert clearance_violations(masked), "a see-through box is not a mask and must still fail"
    plt.close(masked)

    wide, ax = _probe(1.3, ax_w=1.2)
    ax.texts[0].set_text("a label far too long for this axis")
    wide.canvas.draw()
    assert width_violations(wide), "a label wider than 80% of its axis must be caught"
    ax.texts[0].set_text("n=42")
    wide.canvas.draw()
    assert width_violations(wide) == [], "and a short one on the same axis must PASS"
    plt.close(wide)
    return (f"figclearance selftest PASS - gaps measured in inches at the figure's OWN dpi and "
            f"against per-segment marks; a label resting on its bar fires at {CLEAR_DATA_IN}in, a "
            f"cleared one, one in the empty space under a curve and one on its own leader line pass, an opaque mask exempts a "
            f"reference label while a see-through box does not, and the width check fires and "
            f"clears on the same axis")


if __name__ == "__main__":
    print(selftest())
