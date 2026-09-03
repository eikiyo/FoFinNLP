"""
Location: paper-a/analysis/figures.py
Purpose: The three figures the brief asks for (section 8.3): models x models rho heatmap, the
         observed rho histogram against the permutation null, and the models x leaves wobble
         heatmap. Every figure is drawn from the same dicts the tables are written from.
Functions: rho_heatmap(), rho_vs_null(), wobble_heatmap()
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
    return label.replace("-direct", "").replace("-or", "")


def rho_heatmap(models: List[str], rows: List[Dict[str, Any]], out: Path,
                title: str, excluded: List[str]) -> Path:
    """Symmetric rho matrix. An undefined pair is drawn as a hatched blank rather than as 0.0 --
    painting an undefined coefficient as no-correlation is the visual form of the same lie."""
    n = len(models)
    idx = {m: i for i, m in enumerate(models)}
    mat = np.full((n, n), np.nan)
    for r in rows:
        if r["rho"] is not None:
            mat[idx[r["model_a"]], idx[r["model_b"]]] = r["rho"]
            mat[idx[r["model_b"]], idx[r["model_a"]]] = r["rho"]
    np.fill_diagonal(mat, 1.0)
    fig, ax = plt.subplots(figsize=(9.0, 7.6))
    cmap = plt.get_cmap("RdBu_r").copy()
    cmap.set_bad("#dddddd")
    im = ax.imshow(np.ma.masked_invalid(mat), cmap=cmap, vmin=-1, vmax=1)
    labels = [(_short(m) + (" *" if m in excluded else "")) for m in models]
    ax.set_xticks(range(n), labels, rotation=55, ha="right", fontsize=8)
    ax.set_yticks(range(n), labels, fontsize=8)
    for i in range(n):
        for j in range(n):
            if not np.isnan(mat[i, j]) and i != j:
                ax.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center", fontsize=6.2,
                        color="black" if abs(mat[i, j]) < 0.55 else "white")
    ax.set_title(title, fontsize=10)
    fig.colorbar(im, ax=ax, shrink=0.8, label="Spearman rho")
    fig.text(0.01, 0.01, "* tie fraction > 0.80 - coefficients not interpretable; "
                         "grey = undefined (constant vector)", fontsize=7)
    fig.tight_layout()
    fig.savefig(out, dpi=170)
    plt.close(fig)
    return out


def rho_vs_null(observed: List[float], null: Dict[str, Any], out: Path, title: str) -> Path:
    """Observed pairwise rho against the permutation null. Both the null's PAIRWISE spread (what a
    single pair could look like by chance) and its MEDIAN distribution (what the headline statistic
    could look like by chance) are drawn -- they answer different questions and conflating them is
    how a wide-but-centred observed distribution gets called significant."""
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.3))
    ax = axes[0]
    ax.hist(null["pooled_sample"], bins=40, density=True, color="#bbbbbb",
            label=f"permutation null, pairwise (n={len(null['pooled_sample'])})")
    ax.hist(observed, bins=20, density=True, color="#1f77b4", alpha=0.75,
            label=f"observed pairs (n={len(observed)})")
    ax.axvline(float(np.median(observed)), color="#d62728", lw=2,
               label=f"observed median {np.median(observed):.3f}")
    ax.set_xlabel("Spearman rho"), ax.set_ylabel("density")
    ax.set_title("Observed pairs vs the pairwise null", fontsize=10)
    ax.legend(fontsize=7)
    ax = axes[1]
    ax.hist(null["medians"], bins=40, density=True, color="#bbbbbb",
            label=f"null distribution of the MEDIAN ({null['n_perm']} permutations)")
    ax.axvline(float(np.median(observed)), color="#d62728", lw=2,
               label=f"observed median {np.median(observed):.3f}")
    ax.axvline(null["p97_5"], color="#333333", ls="--", lw=1,
               label=f"null 97.5th pct {null['p97_5']:.3f}")
    ax.set_xlabel("median pairwise Spearman rho"), ax.set_ylabel("density")
    ax.set_title("The primary test", fontsize=10)
    ax.legend(fontsize=7)
    fig.suptitle(title, fontsize=11)
    fig.tight_layout()
    fig.savefig(out, dpi=170)
    plt.close(fig)
    return out


def wobble_heatmap(models: List[str], leaf_names: List[str], cells, out: Path,
                   title: str) -> Path:
    """The raw matrix. Leaves ordered by mean wobble so any shared difficulty dimension would show
    as vertical banding; models ordered as declared."""
    order = sorted(leaf_names,
                   key=lambda n: -np.nanmean([cells[m][n]["wobble"] if cells[m][n]["wobble"]
                                              is not None else np.nan for m in models]))
    mat = np.array([[cells[m][n]["wobble"] if cells[m][n]["wobble"] is not None else np.nan
                     for n in order] for m in models], float)
    fig, ax = plt.subplots(figsize=(15.5, 4.6))
    cmap = plt.get_cmap("magma_r").copy()
    cmap.set_bad("#66c2a5")
    im = ax.imshow(np.ma.masked_invalid(mat), aspect="auto", cmap=cmap, vmin=0, vmax=1)
    ax.set_yticks(range(len(models)), [_short(m) for m in models], fontsize=8)
    ax.set_xticks(range(len(order)), order, rotation=90, fontsize=5.4)
    ax.set_title(title, fontsize=10)
    fig.colorbar(im, ax=ax, shrink=0.85, label="wobble rate (flipped items / measured items)")
    fig.tight_layout()
    fig.savefig(out, dpi=170)
    plt.close(fig)
    return out
