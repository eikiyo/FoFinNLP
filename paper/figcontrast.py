"""
Location: paper-a/paper/figcontrast.py
Purpose: The two COLOUR checks no engine gate performs, measured off the drawn figure. The engine
         holds a concept colour against the page; it never asks what a hatch stroke looks like
         against the fill it is drawn ON, or whether an error bar is visible where it crosses a
         bar. Both are contrasts between two INK colours, and both were failing here: the grey
         error bars sat at 1.06:1 against the flagged fill, which is the least visible element in
         a figure whose intervals are the evidence.
Functions: to_hex(), ratio(), grey(), greyscale_violations(), hatch_violations(),
           interval_violations(), selftest()
Calls: figgate.engine() for the WCAG contrast formula (never re-implemented here)
Imports: matplotlib, figgate
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib                                                # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                  # noqa: E402
from matplotlib.colors import to_rgba                            # noqa: E402
from matplotlib.patches import Patch                             # noqa: E402

import figgate as G                                              # noqa: E402

# 3:1 is the WCAG threshold for NON-TEXT contrast (graphical objects and UI components,
# SC 1.4.11). A hatch and an error bar are exactly that: marks that must be distinguishable from
# what they sit on. Text is held to 4.5:1 elsewhere, by verify_palette on figstyle.TEXT_COL.
MIN_INK = 3.0
# Luminance step at which two greys stop being one grey on a printed page. 0.06 puts clean
# (0.173) and flagged (0.152) in the SAME bucket, which is the honest reading: they are one grey
# in a black-and-white print, and every panel that contrasts them separates them by hatch.
JND = 0.06


def to_hex(c) -> str:
    """Any matplotlib colour spec, composited onto white, as '#rrggbb'.

    Compositing matters: a 40%-alpha grid line is not its own colour, it is the colour a reader
    sees, and measuring the declared one would report a contrast nobody experiences."""
    r, g, b, a = to_rgba(c)
    r, g, b = (a * ch + (1 - a) * 1.0 for ch in (r, g, b))
    return "#{:02x}{:02x}{:02x}".format(*(round(ch * 255) for ch in (r, g, b)))


def ratio(c1, c2) -> float:
    """WCAG contrast between two arbitrary colour specs. The formula is the engine's; this wrapper
    only normalises the two arguments, because a second copy of a luminance formula is how two
    checks in one repo come to disagree about the same pair of colours."""
    return G.engine()["contrast"](to_hex(c1), to_hex(c2))


def hatch_violations(fig) -> list:
    """Every hatched patch whose stroke does not clear MIN_INK against its own fill.

    matplotlib draws a hatch in the patch's EDGE colour, so the pair being measured is
    (edgecolor, facecolor) on the same artist. Below 3:1 the pattern stops reading as a category
    and starts reading as texture noise at column width, which is the failure mode that makes a
    reader take two hatched bars for one."""
    out = []
    for p in fig.findobj(Patch):
        hatch = p.get_hatch()
        if not hatch:
            continue
        stroke, fill = to_hex(p.get_edgecolor()), to_hex(p.get_facecolor())
        r = ratio(stroke, fill)
        if r < MIN_INK:
            out.append(f"hatch {hatch!r} stroke {stroke} on fill {fill}: "
                       f"{r:.2f}:1 < {MIN_INK}:1")
    return out


def grey(c) -> float:
    """Relative luminance, which is what a greyscale print keeps."""
    return G.engine()["_lum"](to_hex(c))


def greyscale_violations(fig) -> list:
    """Two patch styles that a reader can tell apart in colour but not in grey.

    The encoding law is that every categorical distinction survives greyscale. Stated as a
    countable property: the number of distinct (fill, hatch) styles must not DROP when fill is
    replaced by its luminance. It does not require the fills to differ in grey -- clean and flagged
    sit at 4.70:1 and 5.19:1 against the page and are near-identical greys on purpose -- it
    requires that wherever they do collapse, a hatch is carrying the distinction instead."""
    out = []
    for i, ax in enumerate(fig.get_axes()):
        styles, greys = set(), {}
        for p in ax.patches:
            if id(p) == id(ax.patch) or not p.get_visible() or to_rgba(p.get_facecolor())[3] < .05:
                continue
            fill, hatch = to_hex(p.get_facecolor()), p.get_hatch() or ""
            styles.add((fill, hatch))
            greys.setdefault((round(grey(fill) / JND), hatch), set()).add(fill)
        merged = [v for v in greys.values() if len(v) > 1]
        if merged:
            out.append(f"axes {i}: {len(styles)} styles collapse to {len(greys)} in greyscale; "
                       + "; ".join(f"{sorted(m)} share a grey and a hatch" for m in merged))
    return out


def _bars(fig):
    """Filled rectangles with an area, in display coordinates. Excludes the axes patch and the
    figure patch, which are the white background and would report every error bar as crossing
    something."""
    boxes = []
    for ax in fig.get_axes():
        skip = {id(ax.patch), id(fig.patch)}
        for p in ax.findobj(Patch):
            if id(p) in skip or not p.get_visible():
                continue
            bb = p.get_window_extent()
            if bb.width > 1 and bb.height > 1 and to_rgba(p.get_facecolor())[3] > 0.05:
                boxes.append((bb, to_hex(p.get_facecolor())))
    return boxes


def _interval_lines(fig):
    """Every error-bar segment as (display bbox, stroke colour).

    Taken from the errorbar CONTAINERS rather than from every line in the axes, so an axis spine
    or a series line is not mistaken for an interval. The bar-line collections carry the whiskers
    and the cap lines the caps; both are the interval."""
    out = []
    for ax in fig.get_axes():
        for cont in ax.containers:
            if not hasattr(cont, "has_xerr"):
                continue
            caps, bars = cont.lines[1], cont.lines[2]
            for lc in bars:
                for seg in lc.get_segments():
                    pts = ax.transData.transform(seg)
                    out.append((matplotlib.transforms.Bbox(
                        [[min(pts[:, 0]), min(pts[:, 1])],
                         [max(pts[:, 0]), max(pts[:, 1])]]), to_hex(lc.get_color()[0])))
            for cap in caps:
                # The MARKER EDGE, not get_color(). A cap is a '_' marker with linestyle None, so
                # its Line2D `color` is whatever the property cycle handed it -- C0 blue here --
                # while the ink a reader sees is the marker edge, which carries ecolor. Measuring
                # get_color() reported every cap in this paper as default-blue and would have had
                # me "fix" a colour that is never drawn.
                out.append((cap.get_window_extent(), to_hex(cap.get_markeredgecolor())))
    return out


def interval_violations(fig) -> list:
    """Every (interval, fill) pair the interval is drawn ACROSS that falls under MIN_INK.

    Geometric, not declared: the pairs are found by intersecting each error-bar segment's box with
    each filled patch's box, so a figure cannot pass by asserting its intervals sit clear of the
    bars. An interval is this paper's evidence; it may not be the faintest ink on the page."""
    fig.canvas.draw()
    seen, out = set(), []
    for line_bb, stroke in _interval_lines(fig):
        for bar_bb, fill in _bars(fig):
            if not line_bb.overlaps(bar_bb):
                continue
            r = ratio(stroke, fill)
            key = (stroke, fill)
            if r < MIN_INK and key not in seen:
                seen.add(key)
                out.append(f"error bar {stroke} crosses fill {fill}: {r:.2f}:1 < {MIN_INK}:1")
    return out


def _probe(hatch_fill, bar_fill, ecolor):
    """One bar with a hatch and an error bar drawn through it. The fixture both checks are driven
    on, so a selftest arm differs from its opposite by a colour and nothing else."""
    fig, ax = plt.subplots(figsize=(2.0, 1.5))
    ax.bar([0], [1.0], color=bar_fill, hatch="///", edgecolor=hatch_fill, linewidth=0.4)
    ax.errorbar([0], [0.6], yerr=[[0.3], [0.3]], fmt="none", ecolor=ecolor, capsize=3)
    ax.set_ylim(0, 1.4)
    fig.canvas.draw()
    return fig


def _grey_arm() -> None:
    """Greyscale, both arms. The SAME two fills pass when a hatch carries the distinction and fail
    when nothing does, so the check measures the encoding rather than the palette."""
    bad = plt.figure(figsize=(2.0, 1.5))
    ax = bad.add_subplot()
    ax.bar([0, 1], [1, 2], color=["#4477AA", "#CC3311"])
    assert greyscale_violations(bad), \
        "two fills one grey apart with no hatch between them must be caught"
    plt.close(bad)
    ok = plt.figure(figsize=(2.0, 1.5))
    ax = ok.add_subplot()
    ax.bar([0], [1], color="#4477AA")
    ax.bar([1], [2], color="#CC3311", hatch="///", edgecolor="white")
    assert greyscale_violations(ok) == [], "and the same pair must PASS once hatched"
    plt.close(ok)


def _geometry_arm() -> None:
    """An interval that does NOT cross a bar must not be reported against it, or the check would be
    a palette comparison wearing a figure's clothes."""
    fig = plt.figure(figsize=(2.0, 1.5))
    ax = fig.add_subplot()
    ax.bar([0], [0.3], color="#4477AA")
    ax.errorbar([0], [1.0], yerr=[[0.05], [0.05]], fmt="none", ecolor="#666666")
    ax.set_ylim(0, 1.4)
    fig.canvas.draw()
    assert interval_violations(fig) == [], \
        "an interval drawn clear of every fill has no fill to be measured against"
    plt.close(fig)


def selftest() -> str:
    """Both arms of both checks. A checker proved only on a violation can be one that flags
    everything; a checker proved only on a clean figure can be one that flags nothing. Each arm
    below differs from its opposite in exactly one colour."""
    assert abs(ratio("#FFFFFF", "#000000") - 21.0) < 0.01, "the contrast wrapper must be WCAG"
    assert abs(ratio("#AA3377", "#FFFFFF") - 6.09) < 0.01, "and agree with the engine's number"
    # Alpha compositing: a 40% black line on white is #999999, at 2.85:1, not black at 21:1.
    assert abs(ratio((0, 0, 0, 0.4), "#FFFFFF") - 2.85) < 0.02, "alpha must be composited"

    bad = _probe("#FFFFFF", "#EE7733", "#666666")     # white hatch on light orange: 2.87:1
    hits = hatch_violations(bad)
    assert hits and "2.87" in hits[0], f"a 2.87:1 hatch must be caught by number: {hits}"
    assert interval_violations(bad), "a #666666 interval on an #EE7733 fill must be caught"
    plt.close(bad)

    good = _probe("#FFFFFF", "#CC3311", "#000000")    # white on 5.19:1, black interval at 4.05:1
    assert hatch_violations(good) == [], "a 5.19:1 hatch must PASS -- the check must discriminate"
    assert interval_violations(good) == [], "a black interval on #CC3311 must PASS"
    plt.close(good)

    _geometry_arm()

    _grey_arm()
    return (f"figcontrast selftest PASS - hatch and interval contrast measured off the drawn "
            f"figure at the {MIN_INK}:1 non-text threshold; each check fires on a real violation, "
            f"stays quiet on a compliant one, and the interval check is geometric (an interval "
            f"clear of the bars is not reported against them); a colour distinction that "
            f"survives greyscale only through a hatch is proved both ways")


if __name__ == "__main__":
    print(selftest())
