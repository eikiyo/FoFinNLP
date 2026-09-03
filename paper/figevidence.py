"""
Location: paper-a/paper/figevidence.py
Purpose: The three exhibits that carry the paper's evidence chain: who wobbles (the lineup), the
         association and the repair that failed to explain it, and the transfer result against the
         null that makes it legible. Split from figpanels.py, which holds the observability panels
         and was at its line budget.
Functions: panel_lineup(), panel_lineup_tail(), panel_repair(), panel_transfer_null()
Calls: tablekit.read_csv/display_name/SERVING/SMALL, figstyle constants, figpanels.grid
Imports: pathlib, tablekit, figpanels, figstyle
"""

from pathlib import Path

import figpanels as FP
import tablekit as K
from figstyle import COL, CONCEPT, FS, HATCH, INTERVAL, LABEL_BOX, LW

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "out" / "tables"

# Where the broken x-axis resumes. Read as: everything below BREAK_LO is drawn on the wide left
# panel at its own scale, the two configurations above it on a narrow right panel. A break, not a
# log axis: a log axis would compress an order-of-magnitude difference into a visual inch and the
# difference is the thing the panel exists to show.
#
# It has to clear the widest Wilson UPPER BOUND, not the widest point estimate, plus room for the
# value label after it. At 0.085 it cleared the largest wobble (0.069) and cut off the interval
# above it; the two topmost value labels then fell outside their own axes and were painted over by
# the tail panel's white background. Every engine gate passed -- clipping is measured against the
# CANVAS, and text hidden by a sibling axes is still on the canvas. Only looking at the rendered
# figure showed it. HEADROOM is the multiple of the widest upper bound the panel must hold.
BREAK_LO = 0.145
HEADROOM = 1.42
TAIL = (0.25, 0.58)
# Share of the tail panel's range a 7pt value label occupies after the widest interval.
TAIL_LABEL = 0.28


def _lineup_rows():
    rows = sorted(K.read_csv(SRC / "clean" / "model_summary.csv"),
                  key=lambda r: float(r["aggregate_wobble"]))
    small = [r for r in rows if r["model"] in K.SMALL]
    if len(small) != len(K.SMALL):
        raise SystemExit(f"model_summary.csv holds {len(small)} of the {len(K.SMALL)} 1B "
                         "configurations; the lineup would silently drop the group the panel "
                         "is about")
    hi_max = max(float(r["wilson_hi"]) for r in rows if r["model"] not in K.SMALL)
    if hi_max * HEADROOM > BREAK_LO:
        raise SystemExit(f"the widest frontier interval reaches {hi_max:.4f} and needs "
                         f"{hi_max * HEADROOM:.4f} of axis with its value label; the break sits "
                         f"at {BREAK_LO}. Raise BREAK_LO -- a panel that cuts off an interval "
                         "reports a narrower one than the data supports")
    small_lo = min(float(r["wilson_lo"]) for r in small)
    small_hi = max(float(r["wilson_hi"]) for r in small)
    room = TAIL[1] - TAIL_LABEL * (TAIL[1] - TAIL[0])
    if small_lo < TAIL[0] or small_hi > room:
        raise SystemExit(f"the 1B intervals span [{small_lo:.4f}, {small_hi:.4f}] and the tail "
                         f"panel holds [{TAIL[0]}, {room:.4f}] once its value labels are "
                         "allowed for; widen TAIL rather than draw an interval that runs off "
                         "its own axis")
    return rows


def _bars(ax, rows, y, insight):
    """Bars plus Wilson intervals for one panel of the broken axis. `insight` marks the rows the
    panel is drawing attention to; everything else recedes, which is the engine's
    highlight_insight rule applied by hand because the two panels share one highlight."""
    vals = [float(r["aggregate_wobble"]) for r in rows]
    lo = [v - float(r["wilson_lo"]) for v, r in zip(vals, rows)]
    hi = [float(r["wilson_hi"]) - v for v, r in zip(vals, rows)]
    # ONE fill colour. The 1B group sits on its own panel across an axis break, which is position
    # -- the strongest encoding there is -- and carries a hatch on top of that. A separate colour
    # for it was a fourth accent that cleared only 3.1:1 against the page, and it was buying a
    # distinction two stronger encodings had already made.
    colors = [CONCEPT["clean"] for _r in rows]
    hatches = [HATCH["flagged"] if r["model"] in K.SMALL else "" for r in rows]
    for yi, v, c, h in zip(y, vals, colors, hatches):
        ax.barh(yi, v, height=0.62, color=c, hatch=h, edgecolor="white", linewidth=0.4, zorder=2)
    ax.errorbar(vals, list(y), xerr=[lo, hi], fmt="none", ecolor=INTERVAL,
                elinewidth=LW["interval"], capsize=1.6, zorder=4)
    return vals, hi


def panel_lineup(ax_main, ax_tail) -> None:
    """Twelve configurations ascending by wobble across a broken x-axis.

    Position carries the ordering, hatch carries the group and colour is third, so the panel reads
    the same in greyscale. The two 1B configurations sit an order of magnitude out; the break is
    drawn rather than a log axis, because compressing that gap would delete the finding."""
    rows = _lineup_rows()
    gap = 0.7                              # a space between the groups, not a rule: the axis break
    y = [i + (gap if r["model"] in K.SMALL else 0) for i, r in enumerate(rows)]
    for ax, keep in ((ax_main, lambda r: r["model"] not in K.SMALL),
                     (ax_tail, lambda r: r["model"] in K.SMALL)):
        sub = [(yi, r) for yi, r in zip(y, rows) if keep(r)]
        vals, hi = _bars(ax, [r for _, r in sub], [yi for yi, _ in sub], keep)
        for (yi, _r), v, h in zip(sub, vals, hi):
            ax.annotate(f"{v:.3f}", xy=(v + h, yi), xytext=(4, 0), textcoords="offset points",
                        va="center", fontsize=FS["annot"], color=COL["single"])
        ax.set_ylim(-0.8, max(y) + 0.8)
        FP.grid_x(ax)
    ax_main.set_xlim(0, BREAK_LO)
    ax_tail.set_xlim(*TAIL)
    ax_main.set_yticks(y)
    ax_main.set_yticklabels([K.display_name(r["model"]).replace(r"\_", "_") for r in rows],
                            fontsize=FS["annot"])
    ax_tail.set_yticks([])
    ax_tail.spines["left"].set_visible(False)
    _break_marks(ax_main, ax_tail)
    # The groups are named in the AXIS LABELS rather than annotated inside the panels. Annotated,
    # the "two 1B" caption landed on the 0.383 value label it was pointing at. The naming is only
    # accurate because _lineup_rows refuses to draw a break that a frontier configuration crosses.
    ax_main.set_xlabel("wobble (frontier)", labelpad=9)
    ax_tail.set_xlabel("(1B)", labelpad=9)
    ax_main.set_xticks([0, 0.04, 0.08, 0.12])
    ax_tail.set_xticks([0.3, 0.4, 0.5])


def _break_marks(ax_main, ax_tail) -> None:
    """The two slashes that say the axis is not continuous. Without them a reader takes the right
    panel's bars as adjacent to the left panel's and reads the gap as small."""
    kw = dict(transform=ax_main.transAxes, color=COL["rule"], clip_on=False,
              linewidth=LW["spine"], zorder=6)
    ax_main.plot([1.0, 1.0], [-0.018, 0.018], **kw)
    ax_main.plot([1.012, 1.028], [-0.03, 0.03], **kw)
    kw["transform"] = ax_tail.transAxes
    ax_tail.plot([-0.028, -0.012], [-0.03, 0.03], **kw)


REPAIR_LABEL = {"before": "original\nwindow", "after": "re-cut\nwindow"}


def panel_repair(ax, threshold: float, label: str = None) -> None:
    """The pre-registered repair, and the line that says it changed nothing.

    The heavy dashed rule is the NO-CHANGE level: where the repaired bar would sit if re-windowing
    had done nothing at all. The repaired bar's interval is the interval on the CHANGE, mapped
    onto the same axis, so a reader can see it reach back across the no-change line. That is what
    a null looks like, drawn rather than described."""
    rows = {r["task"]: r for r in K.read_csv(SRC / "repair_by_task.csv")}
    pooled = rows.get("POOLED")
    if pooled is None:
        raise SystemExit("repair_by_task.csv has no POOLED row; refusing to draw a repair panel "
                         "from the per-task rows alone, which are not the registered test")
    before, after = float(pooled["before_wobble"]), float(pooled["after_wobble"])
    d_lo, d_hi = float(pooled["difference_lo"]), float(pooled["difference_hi"])
    xs = [0, 1]
    # BOTH bars in the flagged colour: drawing the repaired one clean would say, in the paper's own
    # visual vocabulary, that re-windowing made those items clean. Hatch carries the condition.
    ax.bar(xs, [before, after], width=0.5, color=CONCEPT["flagged"],
           hatch=["", HATCH["after"]], edgecolor="white", linewidth=0.4, zorder=2)
    # The interval on the CHANGE, drawn on the repaired bar.
    ax.errorbar([1], [after], yerr=[[after - (before - d_hi)], [(before - d_lo) - after]],
                fmt="none", ecolor=INTERVAL, elinewidth=LW["interval"], capsize=2.8, zorder=6)
    # The heaviest mark, drawn ABOVE the bars: the null is the finding, so the no-change level and
    # the interval crossing it should be seen first. It was the other way round.
    ax.axhline(before, color=COL["observed"], linestyle=(0, (4, 2)), linewidth=LW["null"], zorder=5)
    ax.axhline(threshold, color=COL["rule"], linestyle=":", linewidth=LW["rule"], zorder=3)
    ax.text(1.52, before, "no change", fontsize=FS["annot"], color=COL["observed"],
            va="bottom", ha="right", bbox=dict(LABEL_BOX))
    # Between the bars, on two lines. Right-aligned beside "no change" it printed ACROSS the
    # re-cut bar, whose top (0.208) is above the threshold: the only clear space at this height is
    # the gap between the two bars, and one line does not fit in it.
    ax.text(0.5, threshold + 0.004, f"registered\n{threshold:.3f}", fontsize=FS["annot"],
            color=COL["single"], va="bottom", ha="center", linespacing=1.15,
            bbox=dict(LABEL_BOX))
    ax.set_xticks(xs)
    ax.set_xticklabels([REPAIR_LABEL["before"], REPAIR_LABEL["after"]], fontsize=FS["annot"])
    ax.set_xlim(-0.55, 1.55)
    ax.set_ylabel("wobble", labelpad=7)
    # Top-left, above the bars. Placed at the axis floor it printed ON the original-window bar,
    # which the collision gate reports as TEXT-ON-BAR and a reader sees as a label belonging to
    # that one bar rather than to the comparison.
    ax.annotate(f"change {float(pooled['difference']):+.3f}\n"
                f"[{d_lo:+.3f}, {d_hi:+.3f}]", xy=(0.5, 0), xytext=(0.02, 0.99),
                textcoords="axes fraction", fontsize=FS["annot"], ha="left", va="top")
    FP.grid(ax)
    FP.panel_label(ax, label)


def panel_transfer_null(ax, k: int = 5) -> None:
    """The observed transfer against the permutation null it has to beat.

    The null is drawn as its 2,000 draws rather than as an interval, because the claim is that the
    observed value is nowhere near the distribution and a reader should be able to see the whole
    distribution end before the observed rule begins."""
    draws = [float(r["value"]) for r in K.read_csv(SRC / "transfer_null_draws.csv")
             if int(r["k"]) == k and r["statistic"] == "mean"]
    obs_row = next(r for r in K.read_csv(SRC / "transfer_items.csv") if int(r["k"]) == k)
    p = next(r["p_permutation"] for r in K.read_csv(SRC / "transfer_null.csv")
             if int(r["k"]) == k and r["statistic"] == "mean")
    if not draws:
        raise SystemExit("transfer_null_draws.csv holds no mean draws; the panel would plot an "
                         "empty null and the observed value would look unopposed for the wrong "
                         "reason")
    obs, ratio = float(obs_row["mean"]), float(obs_row["ratio"])
    lo, hi = float(obs_row["boot_mean_lo"]), float(obs_row["boot_mean_hi"])
    ax.hist(draws, bins=28, color=CONCEPT["null"], edgecolor="white", linewidth=0.3, zorder=2)
    # Headroom first, then every annotation is a fraction of the FINAL height. Against the
    # histogram's own top the three captions stacked, all wanting the same upper band.
    top = ax.get_ylim()[1] * 1.42
    ax.set_ylim(0, top)
    # OBSERVED, not clean: this is the bootstrap on the observed transfer, drawn across the null
    # histogram, where the clean blue reached 1.65:1 and the observed slate reaches 3.87:1.
    ax.plot([lo, hi], [top * 0.30] * 2, color=CONCEPT["observed"], linewidth=1.6,
            solid_capstyle="butt", zorder=3)
    for x in (lo, hi):
        ax.plot([x, x], [top * 0.272, top * 0.328], color=CONCEPT["observed"],
                linewidth=LW["rule"], zorder=3)
    ax.axvline(obs, color=CONCEPT["observed"], linewidth=1.4, zorder=5)
    ax.annotate(f"permutation null\n({len(draws):,} shuffles)", xy=(max(draws), top * 0.97),
                xytext=(6, 0), textcoords="offset points", ha="left", va="top",
                fontsize=FS["annot"], color=COL["single"])
    ax.annotate(f"observed {obs:.3f}\n{ratio:.1f}$\\times$ chance, $p$ {p}",
                xy=(obs, top * 0.66), xytext=(-5, 0), textcoords="offset points",
                ha="right", va="top", fontsize=FS["annot"], color=CONCEPT["observed"])
    # Plain "%", not the LaTeX escape. matplotlib is not running under usetex here, so a
    # backslash-percent prints the backslash: the figure read "95\\%" on the page.
    # Two lines, ending just before the observed rule. One line starting at the span's left end
    # ran straight through the rule, which is the figure's most important mark.
    ax.annotate("model-level\nbootstrap 95%", xy=(obs - 0.006, top * 0.30), xytext=(0, -5),
                textcoords="offset points", ha="right", va="top", fontsize=FS["annot"],
                color=CONCEPT["observed"], linespacing=1.15)
    ax.set_xlim(0, 0.31)
    # No tick at 0: the "0.0" label and the y-axis "0" share the corner pixel, which the
    # overlap gate reports and a reader sees as a smudge. Three ticks still fix the scale.
    ax.set_xticks([0.1, 0.2, 0.3])
    ax.set_xlabel(f"mean transfer at $k={k}$", labelpad=7)
    ax.set_ylabel("permutations", labelpad=7)
    FP.trim_ticks(ax)
    FP.grid(ax)
