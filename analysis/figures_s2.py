"""
Location: paper-a/analysis/figures_s2.py
Purpose: The four stage-2 figures: the ceiling (observed vs corrected vs per-model reliability),
         the transfer curve against its chance baseline, the model x category heatmap with n
         annotated on every cell, and the leaf-level wobble-vs-accuracy scatter. Drawn from the
         same dicts the stage-2 tables are written from, so a figure cannot disagree with a table.
Functions: ceiling(), transfer_curve(), category_heatmap(), wobble_accuracy_scatter(), all_figures()
Calls: matplotlib (Agg)
Imports: pathlib, typing, numpy, matplotlib
"""

from pathlib import Path
from typing import Any, Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402


def _short(label: str) -> str:
    return label.replace("-or", "").replace("-direct", "")[:16]


def ceiling(ctx: Dict[str, Any], out: Path) -> Path:
    rows = sorted(ctx["reliability"], key=lambda r: -(r["r_full"] or 0))
    names = [_short(r["model"]) for r in rows]
    vals = [r["r_full"] or 0 for r in rows]
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.bar(range(len(vals)), vals, color="#4C72B0", label="split-half reliability (r_full)")
    ax.axhline(ctx["median_r_full"], color="#C44E52", ls="--",
               label=f"median ceiling {ctx['median_r_full']:.3f}")
    ax.axhline(ctx["observed_median"], color="#55A868", ls="-",
               label=f"observed cross-model rho {ctx['observed_median']:.3f}")
    ax.axhline(ctx["corrected_median"], color="#55A868", ls=":",
               label=f"disattenuated rho {ctx['corrected_median']:.3f}")
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Spearman rho")
    ax.set_ylim(0, 1.05)
    ax.set_title("Measurement ceiling: what agreement was even possible\n"
                 f"observed sits at {ctx['pct_of_ceiling']:.0f}% of the median ceiling")
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    fig.savefig(out, dpi=170)
    plt.close(fig)
    return out


def transfer_curve(ctx: Dict[str, Any], ks, out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8, 5))
    # The two medians can coincide exactly. Drawing them with the same style would hide one line
    # completely under the other while the legend still promised two -- so the frontier line is
    # drawn thick underneath and the all-model line dashed on top, and if they do coincide the
    # figure says so rather than leaving the reader to wonder which line they are looking at.
    styles = (("frontier-only (headline)", "frontier", "#4C72B0", "o-", 4.0, 1.0),
              ("all 12 models", "all", "#C44E52", "s--", 1.6, 0.95))
    for label, key, colour, style, width, alpha in styles:
        med = [ctx["transfer"][k][key]["median"] for k in ks]
        q1 = [ctx["transfer"][k][key]["q1"] for k in ks]
        q3 = [ctx["transfer"][k][key]["q3"] for k in ks]
        ax.plot(ks, med, style, color=colour, label=label, lw=width, alpha=alpha, ms=7)
        ax.fill_between(ks, q1, q3, color=colour, alpha=0.10)
    same = all(abs(ctx["transfer"][k]["frontier"]["median"]
                   - ctx["transfer"][k]["all"]["median"]) < 1e-9 for k in ks)
    if same:
        ax.text(ks[0], 0.93, "the two medians COINCIDE at every k\n(the 1B models do not move it)",
                fontsize=8, color="#333333")
    ax.plot(ks, [ctx["transfer"][k]["frontier"]["chance"] for k in ks], "^:",
            color="#555555", label="chance baseline (per-pair effective k)", lw=1.8, ms=7)
    ax.set_xticks(list(ks))
    ax.set_xlabel("k (model A's top-k unstable leaves, sought in B's top-2k)")
    ax.set_ylabel("share of A's top-k found in B's top-2k")
    ax.set_ylim(0, 1)
    ax.set_title("Transfer: does knowing one model's weak clauses predict another's?\n"
                 "shaded band = IQR across ordered pairs")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out, dpi=170)
    plt.close(fig)
    return out


def category_heatmap(ctx: Dict[str, Any], out: Path) -> Path:
    cats = sorted({l["family"] for l in ctx["leaves"]})
    models = sorted(ctx["models"], key=lambda m: ctx["agg_wobble"][m])
    mat = np.array([[(ctx["cat_cells"][m][c]["rate"] or 0.0) for c in cats] for m in models])
    fig, ax = plt.subplots(figsize=(11, 6.4))
    im = ax.imshow(mat, cmap="magma_r", aspect="auto", vmin=0, vmax=float(mat.max() or 1))
    ax.set_xticks(range(len(cats)))
    ax.set_xticklabels(cats, rotation=35, ha="right", fontsize=8)
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels([_short(m) for m in models], fontsize=8)
    for i, m in enumerate(models):
        for j, c in enumerate(cats):
            v = ctx["cat_cells"][m][c]
            ax.text(j, i, f"{v['measured']}", ha="center", va="center", fontsize=6,
                    color="white" if mat[i, j] > mat.max() * 0.55 else "#333333")
    ax.set_title("Wobble by model x category (cell label = measured items, n)\n"
                 "models ordered by aggregate wobble; see CSV for Wilson intervals")
    fig.colorbar(im, ax=ax, shrink=0.85, label="wobble rate")
    fig.tight_layout()
    fig.savefig(out, dpi=170)
    plt.close(fig)
    return out


def wobble_accuracy_scatter(ctx: Dict[str, Any], out: Path) -> Path:
    rows = [r for r in ctx["leaf_means"]
            if r["mean_wobble"] is not None and r["mean_accuracy"] is not None]
    x = [r["mean_accuracy"] for r in rows]
    y = [r["mean_wobble"] for r in rows]
    wa, nm = ctx["wobble_vs_accuracy"], ctx["nightmare"]
    fig, ax = plt.subplots(figsize=(8, 5.6))
    ax.scatter(x, y, s=26, color="#4C72B0", alpha=0.75, edgecolor="none")
    ax.axvline(nm["threshold_accuracy"], color="#C44E52", ls="--", lw=1)
    ax.axhline(nm["threshold_wobble"], color="#C44E52", ls="--", lw=1)
    ax.text(nm["threshold_accuracy"] + 0.005, nm["threshold_wobble"] + 0.02,
            f"pre-registered 'deployment nightmare' quadrant\nn = {nm['n']}",
            fontsize=8, color="#C44E52")
    ax.set_xlabel("leaf mean majority accuracy across models")
    ax.set_ylabel("leaf mean wobble across models")
    ax.set_title("Is instability just difficulty?\n"
                 f"Spearman = {wa['rho']:.3f} over n = {wa['n']} leaves "
                 f"({100 * wa['rho'] ** 2:.0f}% shared variance)")
    fig.tight_layout()
    fig.savefig(out, dpi=170)
    plt.close(fig)
    return out


def all_figures(ctx: Dict[str, Any], ks, d: Path) -> List[Path]:
    return [ceiling(ctx, d / "ceiling.png"),
            transfer_curve(ctx, ks, d / "transfer_curve.png"),
            category_heatmap(ctx, d / "model_x_category.png"),
            wobble_accuracy_scatter(ctx, d / "wobble_vs_accuracy.png")]
