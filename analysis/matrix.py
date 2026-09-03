"""
Location: paper-a/analysis/matrix.py
Purpose: Build the two matrices every later number derives from (brief 4a): models x leaves wobble
         rates, and the parallel n_items / n_runs / dropped matrix. Also proves, from the arm's own
         manifests, that the arm being read really is temperature 0.7.
Functions: load_cells(), arm_provenance(), write_matrices()
Calls: probity results/aggregate.py + engine/coverage.py (read-only)
Imports: json, csv, pathlib, typing, config
"""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import config


def _cell(res: Dict[str, Any], field: str, agg) -> Dict[str, Any]:
    """One (model, leaf) cell reduced to the counts the brief asks for. `dropped` is the
    benchmark's OWN >30%-unparseable rule (engine/scorer.py `measurable`), mirrored not redefined."""
    rel = res.get("reliability", {})
    dropped = not rel.get("measurable", True)
    flags = agg.per_item_flips(res, field)
    measured = [f for f in flags if f is not None]
    flipped = sum(1 for f in measured if f)
    return {
        "dropped": dropped,
        "flipped": flipped,
        "n_items": len(measured),
        "n_instances": res.get("accuracy", {}).get("n_instances", 0),
        "parse_failure_rate": rel.get("parse_failure_rate"),
        "valid_run_count": rel.get("valid_run_count"),
        "wobble": (flipped / len(measured)) if (measured and not dropped) else None,
    }


def load_cells() -> Tuple[List[str], List[Dict[str, Any]], Dict[str, Dict[str, Dict[str, Any]]]]:
    """(models, leaves, cells[model][leaf]) for the declared arm. Leaves come from the REGISTRY,
    never a directory listing; the lineup is the benchmark's declared editorial list, never a
    heuristic over whatever labels happen to sit in a scored file."""
    agg = config.aggregate_module()
    models = agg.canonical_lineup()
    leaves = []
    cells: Dict[str, Dict[str, Dict[str, Any]]] = {m: {} for m in models}
    opened: List[Path] = []
    for entry in agg.built_leaves():
        name = Path(entry["leaf"]).name
        leaves.append({"leaf": name, "rel": entry["leaf"], "field": entry["field"],
                       "family": entry["family"], "ref": entry["ref"],
                       "type": entry["type"], "stakes": entry.get("stakes")})
        opened.append(config.probity_root() / entry["leaf"] /
                      agg.coverage.scored_filename(config.ARM))
        scored = agg.leaf_scored(entry["leaf"], config.ARM) or {}
        for m in models:
            res = scored.get(m)
            cells[m][name] = ({"dropped": True, "flipped": 0, "n_items": 0, "n_instances": 0,
                               "parse_failure_rate": None, "valid_run_count": None,
                               "wobble": None, "absent": True}
                              if res is None else dict(_cell(res, entry["field"], agg),
                                                       absent=False))
    config.assert_arm_clean(opened)
    return models, leaves, cells


def load_accuracy(models: List[str], leaves: List[Dict[str, Any]]
                  ) -> Dict[str, Dict[str, Any]]:
    """Per-cell MAJORITY accuracy from the same scored.json this arm's wobble comes from -- needed
    for step 4a (is wobble just difficulty?). Read here rather than in the analysis module so that
    scored.json is opened in exactly one place and the arm guard covers it."""
    agg = config.aggregate_module()
    out: Dict[str, Dict[str, Any]] = {m: {} for m in models}
    opened: List[Path] = []
    for entry in leaves:
        # `rel` is the leaf's path, `leaf` is its basename. Passing the basename to leaf_scored
        # silently returns nothing and every accuracy becomes None -- the same basename/path
        # confusion that broke the stage-1 provenance probe.
        rel = entry.get("rel", entry["leaf"])
        opened.append(config.probity_root() / rel / agg.coverage.scored_filename(config.ARM))
        scored = agg.leaf_scored(rel, config.ARM) or {}
        for m in models:
            res = scored.get(m)
            acc = (res or {}).get("accuracy", {})
            out[m][Path(entry["leaf"]).name] = (
                acc.get("accuracy_majority")
                if res is not None and acc.get("n_measurable", 0) > 0 else None)
    config.assert_arm_clean(opened)
    matched = sum(1 for m in models for v in out[m].values() if v is not None)
    if matched == 0:
        raise SystemExit("accuracy join matched 0 of "
                         f"{len(models) * len(leaves)} cells -- the join is broken (check the "
                         "leaf path key), not the data")
    return out


def _n_runs_recorded(agg, rel: str, label: str) -> int:
    """Distinct (instance_idx, run_idx) keys on disk for this cell -- deduped, because these
    checkpoints are append-only and a resumed run legitimately repeats a key."""
    leaf_dir = config.probity_root() / rel
    path = agg.coverage.checkpoint_path(leaf_dir, label,
                                        agg.coverage.artifact_suffix(config.ARM))
    return len(agg.coverage.recorded_keys(path))


def arm_provenance(models: List[str], leaves: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Positive control on the SCOPE rule: read every manifest this arm wrote and confirm each one
    states temperature 0.7. A check that reports "right arm" is only trustworthy if it could have
    detected the wrong one, so the temperatures actually seen are reported, not just a boolean.
    Cells whose manifest predates the manifest feature are counted, never assumed.
    """
    agg = config.aggregate_module()
    suffix = agg.coverage.artifact_suffix(config.ARM)
    temps: Dict[str, int] = {}
    n_runs_declared: Dict[str, int] = {}
    found = missing = 0
    per_model: Dict[str, int] = {m: 0 for m in models}
    for entry in leaves:
        for m in models:
            p = config.probity_root() / entry["rel"] / f"manifest_{suffix}{m}.json"
            if not p.exists():
                missing += 1
                continue
            found += 1
            per_model[m] += 1
            man = json.loads(p.read_text())
            temps[str(man.get("temperature"))] = temps.get(str(man.get("temperature")), 0) + 1
            k = str(man.get("n_runs"))
            n_runs_declared[k] = n_runs_declared.get(k, 0) + 1
    # A check that reports ABSENCE is only trustworthy if it can detect PRESENCE. Finding zero
    # manifests across every cell means this probe is broken (a wrong path root), not that the
    # arm is undocumented -- fail closed rather than print a confident "0 found".
    if found == 0:
        raise SystemExit("provenance probe found 0 manifests across all cells -- the probe is "
                         "broken (check the leaf path root), not the data")
    return {"manifests_found": found, "manifests_absent": missing, "per_model": per_model,
            "temperatures_seen": temps, "n_runs_declared": n_runs_declared}


def write_matrices(models, leaves, cells, tables: Path) -> Dict[str, Path]:
    """The two files of brief 4a. Everything downstream derives from these and nothing else."""
    agg = config.aggregate_module()
    names = [l["leaf"] for l in leaves]
    wob = tables / "wobble_matrix.csv"
    with open(wob, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model"] + names)
        for m in models:
            w.writerow([m] + ["" if cells[m][n]["wobble"] is None
                              else f"{cells[m][n]['wobble']:.6f}" for n in names])
    meta = tables / "n_and_dropped_matrix.csv"
    with open(meta, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "leaf", "family", "field", "n_items", "n_instances", "n_runs",
                    "flipped", "wobble", "dropped", "absent", "parse_failure_rate"])
        for m in models:
            for l in leaves:
                c = cells[m][l["leaf"]]
                w.writerow([m, l["leaf"], l["family"], l["field"], c["n_items"],
                            c["n_instances"], _n_runs_recorded(agg, l["rel"], m), c["flipped"],
                            "" if c["wobble"] is None else f"{c['wobble']:.6f}",
                            int(c["dropped"]), int(c["absent"]),
                            "" if c["parse_failure_rate"] is None
                            else f"{c['parse_failure_rate']:.6f}"])
    return {"wobble_matrix": wob, "n_and_dropped_matrix": meta}
