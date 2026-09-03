"""
Location: paper-a/analysis/repair_run.py
Purpose: Block 2b, the PAID half. Re-run the 14 repaired items across the twelve configurations at
         temperature 0.7, writing to out/repair/results/ -- entirely outside the benchmark tree, so
         the original condition is untouched and both conditions survive for the paired analysis.
         Reuses probity's own harness, task, clients and scorer: a re-implemented prompt would make
         the repaired condition incomparable to the one it is measured against.
         Usage:  python3 analysis/repair_run.py --probe     (one config, one item, two runs)
                 python3 analysis/repair_run.py --go        (the full sweep)
Functions: repaired_instances(), run_config(), main()
Calls: probity engine/runner.load_instances, engine/harness.run_harness, engine/preflight.LINEUP
Imports: argparse, json, sys, pathlib, config, repair_windows
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config                        # noqa: E402
import repair_windows as RW          # noqa: E402

TEMPERATURE = 0.7                    # the ONLY arm this file may run; asserted, never defaulted
RESULTS = config.PAPER_ROOT / "out" / "repair" / "results"


def engine():
    """probity's own modules, imported from the frozen benchmark. Nothing here is re-implemented."""
    root = config.probity_root()
    for sub in ("engine", "results"):
        if str(root / sub) not in sys.path:
            sys.path.insert(0, str(root / sub))
    import harness, preflight, runner, scorer                     # noqa: E401
    return runner, harness, preflight, scorer


def client_for(kind: str, model_id: str, runner):
    """The client the SWEEP would build, via runner's own factories.

    Not preflight.build_client: that one drops model_id for the deepseek branch and returns
    DeepSeekClient() with its default. deepseek-v4f and deepseek-v4p would then have been the
    same model called twice under two labels, and the repaired condition would carry two
    identical columns that the paired analysis would read as two independent configurations."""
    sets = {"openrouter": runner.openrouter_model_set, "anthropic": runner.anthropic_model_set,
            "deepseek": runner.deepseek_model_set}
    if kind in sets:
        (_label, _ollama, factory), = sets[kind](kind, model_id)
        return factory()
    from models import OllamaClient
    return OllamaClient(model_id)


def repaired_instances(leaf_dir: Path, field: str, runner) -> List:
    """The benchmark's own instances, with the repaired window substituted, KEEPING ONLY the
    repaired items.

    Built from runner.load_instances so the instance shape, the field key and the oracle pairing
    are the benchmark's. Only the document text differs, which is exactly the intervention under
    test: same item, same question, same ground truth, evidence now inside the window."""
    instances, _ = runner.load_instances(leaf_dir, field)
    out = []
    for inst, truth in instances:
        repaired = RW.DEST / leaf_dir.name / f"{inst['id']}.txt"
        if repaired.exists():
            out.append(({**inst, "document": repaired.read_text()}, truth))
    return out


MAX_REFILL = 3
# Concurrency per leaf. The benchmark's own sweep ran leaf-parallelism 10 x workers-per-leaf 4,
# so 40 calls in flight against the same providers; this file runs leaves sequentially, so the
# whole budget goes into one leaf. Local models get far less: a single GPU saturates early and a
# large worker count only competes for the same KV cache.
WORKERS = {"openrouter": 16, "anthropic": 12, "deepseek": 12, "ollama": 4}


def drop_nulls(ckpt: Path) -> int:
    """Remove records whose call produced nothing, so the harness sees them as holes again.

    An empty response is recorded with parsed=None and NO error field, and coverage.recorded_keys
    counts any (instance, run) key it finds regardless of what that record contains. So a call
    that returned an empty string is indistinguishable from a completed one to every resume and
    backfill path in the benchmark: the hole is permanent and invisible, and the only symptom is
    a smaller denominator in the wobble for that item. The first probe here hit three of them in
    six calls on a cold model, and a re-run produced nine clean records from the same code, so
    they are transient rather than structural -- which is precisely why they must be refilled
    rather than reasoned about."""
    if not ckpt.exists():
        return 0
    rows = [json.loads(l) for l in ckpt.read_text().splitlines() if l.strip()]
    keep = {}
    for r in rows:                       # last write wins, matching the resume-safe reader
        keep[(r["instance_idx"], r["run_idx"])] = r
    good = [r for r in keep.values() if r.get("parsed") is not None]
    dropped = len(keep) - len(good)
    ckpt.write_text("".join(json.dumps(r) + "\n" for r in good))
    return dropped


def run_config(label: str, kind: str, model_id: str, leaves: Dict[str, Any], n_runs: int,
               engine_mods) -> Dict[str, Any]:
    """One configuration over every repaired leaf. Fails closed on temperature."""
    runner, harness, preflight, scorer = engine_mods
    if TEMPERATURE != 0.7:
        raise SystemExit(f"this file may only run the 0.7 arm; TEMPERATURE is {TEMPERATURE}")
    client = client_for(kind, model_id, runner)
    rows, total = {}, 0
    for leaf_name, (leaf_dir, task, field) in leaves.items():
        instances = repaired_instances(leaf_dir, field, runner)
        if not instances:
            continue
        ckpt = RESULTS / leaf_name / f"{label}.jsonl"
        ckpt.parent.mkdir(parents=True, exist_ok=True)
        refilled = 0
        for attempt in range(MAX_REFILL + 1):
            runs, _ = harness.run_harness(client, task, instances, n_runs=n_runs,
                                          temperature=TEMPERATURE, checkpoint_file=str(ckpt),
                                          model_label=label, max_workers=WORKERS.get(kind, 4))
            n = drop_nulls(ckpt)
            refilled += n
            if n == 0:
                break
            print(f"      {leaf_name}: {n} empty responses dropped, refilling "
                  f"(attempt {attempt + 1}/{MAX_REFILL})", flush=True)
        else:
            print(f"      {leaf_name}: STILL SHORT after {MAX_REFILL} refills -- this cell is "
                  f"incomplete and must not be reported as measured", flush=True)
        rows[leaf_name] = {"n_items": len(instances), "n_runs": n_runs, "refilled": refilled,
                           "complete": len([r for r in ckpt.read_text().splitlines()
                                            if r.strip()]) == len(instances) * n_runs,
                           "reliability": scorer.score_runs(task, instances, runs),
                           "accuracy": scorer.score_accuracy(task, instances, runs)}
        total += len(instances) * n_runs
    return {"label": label, "client": kind, "model_id": model_id,
            "temperature": TEMPERATURE, "calls": total, "leaves": rows}


def build_leaves(runner) -> Dict[str, Any]:
    """The four leaves that own a repaired item, with their task and field."""
    agg = config.aggregate_module()
    out = {}
    for entry in agg.built_leaves():
        name = Path(entry["leaf"]).name
        if not (RW.DEST / name).exists():
            continue
        leaf_dir = config.probity_root() / entry["leaf"]
        out[name] = (leaf_dir, runner._load_task(leaf_dir), entry["field"])
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true", help="one config, one leaf, two runs")
    ap.add_argument("--go", action="store_true", help="the full sweep")
    a = ap.parse_args()
    if not (a.probe or a.go):
        raise SystemExit("pass --probe or --go; this file never runs a paid sweep by default")
    mods = engine()
    runner, _, preflight, _ = mods
    leaves = build_leaves(runner)
    n_items = sum(len(list((RW.DEST / n).glob("*.txt"))) for n in leaves)
    print(f"  {n_items} repaired items across {len(leaves)} leaves: {', '.join(sorted(leaves))}")
    lineup = preflight.LINEUP
    if a.probe:
        # The cheapest routed model, one leaf, two runs. Proves the plumbing before any bulk spend.
        label, kind, model_id = next(l for l in lineup if l[0] == "gpt-oss-120b-or")
        one = {k: v for k, v in list(leaves.items())[:1]}
        res = run_config(label, kind, model_id, one, 2, mods)
        print(json.dumps(res, indent=1)[:1200])
        return
    out = []
    for label, kind, model_id in lineup:
        print(f"\n  === {label} ({kind}) ===", flush=True)
        res = run_config(label, kind, model_id, leaves, 20, mods)
        out.append(res)
        print(f"      {res['calls']} calls", flush=True)
        (RESULTS / "summary.json").write_text(json.dumps(out, indent=1))
    print(f"\n  {sum(r['calls'] for r in out)} calls across {len(out)} configurations")


if __name__ == "__main__":
    main()
