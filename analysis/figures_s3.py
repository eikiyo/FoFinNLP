"""
Location: paper-a/analysis/figures_s3.py
Purpose: STAGE 3 figures. Three, each carrying a result that a table states less legibly: the
         point-vs-conservative ratio collapse, the bimodal per-item correct rate, and the
         wobble-accuracy relationship with its structural component drawn beside it.
Functions: ratio_collapse(), p_histogram(), fold_scatter(), all_figures()
Calls: none
Imports: pathlib, typing, matplotlib, numpy
"""

from pathlib import Path
from typing import Any, Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import numpy as np                       # noqa: E402

BAR = 2.0


def ratio_collapse(rows: List[Dict[str, Any]], path: Path) -> Path:
    """Point ratio against conservative ratio, per model, on a log axis. The gap between the two
    markers IS the finding: how much of the headline is interval width rather than effect."""
    ok = [r for r in rows if r["point_ratio"] is not None and r["cons_ratio"] is not None]
    ok = sorted(ok, key=lambda r: -r["point_ratio"])
    y = np.arange(len(ok))
    fig, ax = plt.subplots(figsize=(9, 5.2))
    for i, r in enumerate(ok):
        ax.plot([r["cons_ratio"], r["point_ratio"]], [i, i], color="#bbbbbb", lw=1.4, zorder=1)
    ax.scatter([r["point_ratio"] for r in ok], y, s=54, color="#c0392b", zorder=3,
               label="point estimate")
    ax.scatter([r["cons_ratio"] for r in ok], y, s=54, marker="D", color="#2c3e50", zorder=3,
               label="conservative (Wilson lo / Wilson hi)")
    ax.axvline(BAR, color="#e67e22", ls="--", lw=1.2, label=f"{BAR:g}x bar")
    ax.axvline(1.0, color="#7f8c8d", ls=":", lw=1.2, label="1x (no gap)")
    ax.set_yticks(y, [r["model"] for r in ok], fontsize=8)
    ax.set_xscale("log")
    ax.set_xlabel("worst-category wobble / mean wobble (log scale)")
    ax.set_title("Step 1a: the worst-to-mean ratio under a conservative reading", fontsize=11)
    # Rows are sorted largest-ratio-first, and matplotlib puts index 0 at the BOTTOM, so the
    # extreme points sit bottom-right -- exactly where a default legend lands and hides them.
    ax.legend(fontsize=8, loc="upper right", framealpha=0.95)
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def p_histogram(pooled: Dict[str, Any], path: Path) -> Path:
    """The pooled per-item correct rate. The two towers at 0 and 1 are the whole 1c argument."""
    edges, hist = pooled["edges"], pooled["hist"]
    centres = [(edges[i] + edges[i + 1]) / 2 for i in range(len(hist))]
    fig, ax = plt.subplots(figsize=(8, 4.4))
    ax.bar(centres, hist, width=0.092, color="#2c3e50", edgecolor="white")
    ax.set_xlabel("per-item correct rate p across the 20 runs")
    ax.set_ylabel("items")
    ax.set_title(f"Step 1c: per-item correct rate is strongly bimodal "
                 f"({pooled['n_items']:,} items; {100 * pooled['frac_one']:.1f}% at p=1, "
                 f"{100 * pooled['frac_zero']:.1f}% at p=0)", fontsize=10)
    ax.annotate("only items near the middle\ncan flip while staying correct",
                xy=(0.5, max(hist) * 0.10), xytext=(0.32, max(hist) * 0.55), fontsize=8,
                ha="center", arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.2),
                color="#c0392b")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def fold_scatter(rows: List[Dict[str, Any]], path: Path) -> Path:
    """Observed leaf wobble against accuracy, with the calibrated structural prediction drawn on
    the same axes. The two clouds sitting on top of each other is the 1b concession, visually."""
    ok = [r for r in rows if r["accuracy"] is not None and r["observed"] is not None
          and r.get("structural_cal") is not None]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter([r["accuracy"] for r in ok], [r["observed"] for r in ok], s=46,
               color="#c0392b", label="observed wobble", zorder=3)
    ax.scatter([r["accuracy"] for r in ok], [r["structural_cal"] for r in ok], s=34,
               marker="x", color="#2c3e50", label="predicted from per-item p alone", zorder=2)
    for r in ok:
        ax.plot([r["accuracy"]] * 2, [r["observed"], r["structural_cal"]], color="#cccccc",
                lw=0.8, zorder=1)
    ax.set_xlabel("leaf mean majority accuracy")
    ax.set_ylabel("leaf mean wobble")
    ax.set_title("Step 1b: wobble is almost entirely predicted by the per-item correct rate",
                 fontsize=11)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def all_figures(ctx: Dict[str, Any], figdir: Path) -> Dict[str, Path]:
    return {"ratio_collapse": ratio_collapse(ctx["cons"][3], figdir / "ratio_collapse.png"),
            "item_p": p_histogram(ctx["pooled_p"], figdir / "item_p_distribution.png"),
            "fold": fold_scatter(ctx["fold_rows"], figdir / "fold_decomposition.png")}
