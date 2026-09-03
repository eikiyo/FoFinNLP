"""
Location: paper-a/analysis/splithalf.py
Purpose: STEP 1, the measurement ceiling. Recompute the wobble matrix twice from the RAW runs --
         odd runs and even runs -- using the benchmark's OWN scorer, then correlate each model's
         half-A leaf vector against its half-B vector. That is the instrument's split-half
         reliability, and it is what tells us whether 0.2964 is modest or near-maximal.
Functions: engine_modules(), leaf_runs(), split_cells(), spearman_brown(), disattenuate(),
           reliability_rows(), reliability_null(), roundtrip_check()
Calls: probity engine/scorer.py, engine/runner.py, engine/coverage.py, results/aggregate.py
Imports: importlib, json, sys, pathlib, typing, numpy, config, stats_core
"""

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

import config
import stats_core as sc

_CACHE: Dict[str, Any] = {}


def engine_modules():
    """The benchmark's own scorer/runner/coverage. Imported, never re-implemented: the flip rule
    (`consistency < 1.0` over the per-field mode) and the measurability rule live in exactly one
    place and a hand-rolled copy is a logged failure in this project."""
    if "mods" in _CACHE:
        return _CACHE["mods"]
    root = config.probity_root()
    for p in (str(root / "engine"), str(root)):
        if p not in sys.path:
            sys.path.insert(0, p)
    import coverage, runner, scorer          # noqa: E401  (probity's engine package)
    _CACHE["mods"] = (scorer, runner, coverage)
    return _CACHE["mods"]


def _task_of(leaf_rel: str):
    spec = importlib.util.spec_from_file_location(
        "t_" + Path(leaf_rel).name, config.probity_root() / leaf_rel / "task.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TASK


def leaf_runs(leaf_rel: str, label: str) -> Tuple[List[Dict[str, Any]], Path]:
    """Raw run records for one cell IN THE DECLARED ARM. The path comes from the benchmark's own
    `coverage.checkpoint_path` + `artifact_suffix(ARM)`, never a hardcoded `runs_<label>.jsonl`,
    so the arm sentinel governs which file is opened."""
    _, _, coverage = engine_modules()
    path = coverage.checkpoint_path(config.probity_root() / leaf_rel, label,
                                    coverage.artifact_suffix(config.ARM))
    if not path.exists():
        return [], path
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()], path


def _score(task, instances, runs, field, agg) -> Optional[float]:
    """Wobble for one cell from a run list, via the ENGINE's scorer. None when the benchmark's own
    measurability rule rejects the cell or nothing was measured -- never 0.0, which would read as
    'perfectly stable' and is the opposite of 'not measured'."""
    scorer, _, _ = engine_modules()
    rel = scorer.score_runs(task, instances, runs)
    if not rel.get("measurable", False):
        return None
    acc = scorer.score_accuracy(task, instances, runs)
    flags = agg.per_item_flips({"accuracy": acc, "reliability": rel}, field)
    measured = [f for f in flags if f is not None]
    if not measured:
        return None
    return sum(1 for f in measured if f) / len(measured)


def split_cells(models: List[str], leaves: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Two full wobble matrices -- odd runs and even runs -- plus the full-run recomputation used
    as a round-trip control. One read of each runs file serves all three."""
    _, runner, _ = engine_modules()
    agg = config.aggregate_module()
    halves: Dict[int, Dict[str, Dict[str, Optional[float]]]] = {0: {m: {} for m in models},
                                                                1: {m: {} for m in models}}
    full: Dict[str, Dict[str, Optional[float]]] = {m: {} for m in models}
    opened: List[Path] = []
    for entry in leaves:
        task = _task_of(entry["rel"])
        instances, _ = runner.load_instances(config.probity_root() / entry["rel"], entry["field"])
        for m in models:
            runs, path = leaf_runs(entry["rel"], m)
            opened.append(path)
            for parity in (0, 1):
                sub = [r for r in runs if r.get("run_idx", 0) % 2 == parity]
                halves[parity][m][entry["leaf"]] = (_score(task, instances, sub, entry["field"],
                                                           agg) if sub else None)
            full[m][entry["leaf"]] = (_score(task, instances, runs, entry["field"], agg)
                                      if runs else None)
    config.assert_arm_clean(opened)
    return {"A": halves[0], "B": halves[1], "full": full, "n_files": len(opened)}


def roundtrip_check(models: List[str], names: List[str], full_recomputed, published) -> str:
    """POSITIVE CONTROL: the full-run path through the engine's scorer must reproduce the published
    scored.json matrix exactly. If it does not, the split-half matrices are not trustworthy either
    and the run stops -- this is the only evidence that the raw-runs route is the same measurement."""
    diffs = []
    for m in models:
        for n in names:
            a, b = full_recomputed[m][n], published[m][n]["wobble"]
            if a is None and b is None:
                continue
            if a is None or b is None or abs(a - b) > 1e-12:
                diffs.append(f"{m}/{n}: recomputed {a} vs published {b}")
    if diffs:
        raise SystemExit("ROUND-TRIP FAILED - the raw-runs path does not reproduce the published "
                         "matrix:\n  " + "\n  ".join(diffs[:10]))
    return (f"round-trip PASS - the engine's scorer over raw runs reproduces all "
            f"{len(models) * len(names)} published cells exactly")


def spearman_brown(r: Optional[float]) -> Optional[float]:
    """Step a half-length reliability up to full-length: r_full = 2r / (1 + r). Undefined for
    r <= -1. A NEGATIVE r is returned as-is after the formula rather than clipped, because a
    negative reliability is a real (and damning) statement about the instrument."""
    if r is None or r <= -1.0:
        return None
    return 2 * r / (1 + r)


def disattenuate(rho: Optional[float], r_a: Optional[float],
                 r_b: Optional[float]) -> Tuple[Optional[float], str]:
    """Classical correction for attenuation. Returns (value, note). Never clips: a value above 1
    means the correction has hit its limit and the reliabilities cannot support a point estimate,
    which is information, not something to hide behind a min()."""
    if rho is None or r_a is None or r_b is None:
        return None, "undefined: a reliability or the observed rho is undefined"
    if r_a <= 0 or r_b <= 0:
        return None, "undefined: a reliability is <= 0, so the correction has no real square root"
    val = rho / float(np.sqrt(r_a * r_b))
    return val, (">1 - correction at its limit; reliability too low to support a point estimate"
                 if val > 1 else "")


def reliability_rows(models: List[str], names: Sequence[str], cells: Dict[str, Any],
                     published: Dict[str, Dict[str, Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Per model: both half wobble levels, the published full level, r_half, r_full, and the tie
    fractions of BOTH half-vectors -- because halving the runs pushes more leaves to exactly zero,
    and a reliability depressed by ties would understate the ceiling and over-correct everything
    downstream (sad-path 4)."""
    rows = []
    for m in models:
        va = [cells["A"][m][n] for n in names]
        vb = [cells["B"][m][n] for n in names]
        st = sc.pair_stats(va, vb)
        r_full = spearman_brown(st["rho"])
        defined = [(x, y) for x, y in zip(va, vb) if x is not None and y is not None]
        rows.append({
            "model": m, "n_leaves": len(defined),
            "wobble_A": _mean([x for x, _ in defined]), "wobble_B": _mean([y for _, y in defined]),
            "wobble_full": _mean([published[m][n]["wobble"] for n in names
                                  if published[m][n]["wobble"] is not None]),
            "r_half": st["rho"], "r_full": r_full, "reason": st.get("reason") or "",
            "tie_A": sc.tie_fraction(va), "tie_B": sc.tie_fraction(vb),
            "zero_A": sc.zero_fraction(va), "zero_B": sc.zero_fraction(vb),
        })
    return rows


def _mean(vals: Sequence[Optional[float]]) -> Optional[float]:
    v = [x for x in vals if x is not None]
    return (sum(v) / len(v)) if v else None


def repeated_split_reliability(models: List[str], leaves: List[Dict[str, Any]],
                               names: Sequence[str], n_splits: int, seed: int) -> Dict[str, Any]:
    """DECLARED ADDITION (not in the pre-registration; prompted by finding Cacioli 2026, which
    averages 1,000 random split-halves rather than taking one).

    A single odd/even split is ONE draw from the distribution of possible splits, so its
    reliability could be a lucky or unlucky partition. This re-runs the whole split over
    `n_splits` random partitions of each cell's runs and reports the spread. The pre-registered
    odd/even value stays the headline; this says whether that value was representative."""
    _, runner, _ = engine_modules()
    agg = config.aggregate_module()
    rng = np.random.default_rng(seed)
    per_split: List[Dict[str, Optional[float]]] = []
    prepared = [(e, _task_of(e["rel"]),
                 runner.load_instances(config.probity_root() / e["rel"], e["field"])[0])
                for e in leaves]
    runs_cache = {(e["leaf"], m): leaf_runs(e["rel"], m)[0] for e, _, _ in prepared for m in models}
    for _ in range(n_splits):
        va: Dict[str, List[Optional[float]]] = {m: [] for m in models}
        vb: Dict[str, List[Optional[float]]] = {m: [] for m in models}
        for entry, task, instances in prepared:
            for m in models:
                runs = runs_cache[(entry["leaf"], m)]
                idxs = sorted({r["run_idx"] for r in runs})
                half = set(rng.permutation(idxs)[: len(idxs) // 2].tolist())
                a = [r for r in runs if r["run_idx"] in half]
                b = [r for r in runs if r["run_idx"] not in half]
                va[m].append(_score(task, instances, a, entry["field"], agg) if a else None)
                vb[m].append(_score(task, instances, b, entry["field"], agg) if b else None)
        keep = [i for i, n in enumerate(names) if n in set(names)]
        row = {}
        for m in models:
            st = sc.pair_stats([va[m][i] for i in keep], [vb[m][i] for i in keep])
            row[m] = spearman_brown(st["rho"])
        per_split.append(row)
    out = {}
    for m in models:
        vals = [s[m] for s in per_split if s[m] is not None]
        out[m] = {"n_splits": len(vals),
                  "mean": float(np.mean(vals)) if vals else None,
                  "p02_5": float(np.percentile(vals, 2.5)) if vals else None,
                  "p97_5": float(np.percentile(vals, 97.5)) if vals else None}
    meds = [float(np.median([s[m] for m in models if s[m] is not None])) for s in per_split]
    return {"per_model": out, "n_splits": n_splits,
            "median_of_medians": float(np.median(meds)),
            "p02_5": float(np.percentile(meds, 2.5)), "p97_5": float(np.percentile(meds, 97.5))}


def reliability_null(cells: Dict[str, Any], models: List[str], names: Sequence[str],
                     n_perm: int, seed: int) -> Dict[str, Any]:
    """Tie-preserving null for the split-half correlations: permute each model's half-A values
    among its OWN positions and re-correlate against its unpermuted half-B. Same principle as the
    stage-1 null -- destroy only the leaf-to-leaf pairing, keep ties and n exactly."""
    rng = np.random.default_rng(seed)
    meds = []
    cols = {m: ([cells["A"][m][n] for n in names], [cells["B"][m][n] for n in names])
            for m in models}
    for _ in range(n_perm):
        vals = []
        for m in models:
            a, b = cols[m]
            idx = [i for i, (x, y) in enumerate(zip(a, b)) if x is not None and y is not None]
            if len(idx) < 3:
                continue
            pa = list(rng.permutation([a[i] for i in idx]))
            st = sc.pair_stats(pa, [b[i] for i in idx])
            if st["rho"] is not None:
                vals.append(st["rho"])
        if vals:
            meds.append(float(np.median(vals)))
    arr = np.array(meds) if meds else np.array([np.nan])
    return {"n_perm": len(meds), "median_of_medians": float(np.median(arr)),
            "p02_5": float(np.percentile(arr, 2.5)), "p97_5": float(np.percentile(arr, 97.5)),
            "max": float(np.max(arr)), "medians": arr}
