"""
Location: paper-a/analysis/block2b_cost.py
Purpose: Cost and call-count estimate for the Block 2b repair run, BEFORE anything is launched.
         The brief requires the estimate to be reported and authorisation obtained; this produces
         it from the real repairable set, the engine's real call unit, and the measured per-call
         spend of the runs already made, so no number in the request is typed from memory.
         Usage:  python3 analysis/block2b_cost.py
Functions: repairable_items(), per_call_costs(), estimate(), main()
Calls: block0d.buckets, config.probity_root, config.serving_paths
Imports: csv, json, sys, pathlib, config, block0d
"""

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config                        # noqa: E402

N_RUNS = 20                          # engine/runner.py:41, read not assumed -- asserted in main()
# The three participation_type items are verified-absent from the source document we hold. Widening
# the window cannot repair an item whose quote is in no document, so they are excluded from the
# repair target by PREREG_UPGRADE section 1.3 and from this estimate.
UNREPAIRABLE_BUCKET = "quote-absent-from-source"


def repairable_items(path: Path) -> list:
    """The repair targets, taken from repair_windows.targets() -- the ONE definition.

    This held a second copy of the filter and went on reporting 14 after four computational items
    were excluded from the repair set. The count decides whether the experiment runs at all
    against the registered threshold of 10, so two places computing it differently is exactly the
    kind of disagreement that gets published."""
    import repair_windows
    return repair_windows.targets()


def per_call_costs(ledger: Path) -> dict:
    """Measured dollars per call per configuration, from the runs already paid for.

    Per configuration, never pooled. The measured spread across the lineup is more than tenfold,
    so a single mean would understate the expensive models and overstate the cheap ones in a
    number whose only purpose is to let someone decide whether to authorise the spend."""
    out = {}
    for line in ledger.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        spend, recorded = r.get("measured_spend_usd"), r.get("recorded")
        if spend and recorded:
            out[r["label"]] = spend / recorded
    return out


def estimate(n_items: int, labels: list, costs: dict) -> dict:
    """Calls and dollars, with the unpriced configurations named rather than silently dropped.

    A configuration with no measured spend is not free: it is unmeasured. Folding it in at zero
    would produce a total that reads like a full accounting and is not one."""
    per_config = n_items * N_RUNS
    priced = [l for l in labels if l in costs]
    unpriced = [l for l in labels if l not in costs]
    subtotal = {l: per_config * costs[l] for l in priced}
    return {"n_items": n_items, "n_runs": N_RUNS, "n_configs": len(labels),
            "calls_per_config": per_config, "total_calls": per_config * len(labels),
            "priced_configs": priced, "unpriced_configs": unpriced,
            "per_config_usd": subtotal, "priced_total_usd": sum(subtotal.values()),
            "priced_calls": per_config * len(priced),
            "unpriced_calls": per_config * len(unpriced)}


def main() -> dict:
    root = config.probity_root()
    runner = (root / "engine" / "runner.py").read_text()
    declared = next((int(l.split("=")[1]) for l in runner.splitlines()
                     if l.startswith("N_RUNS")), None)
    if declared != N_RUNS:
        raise SystemExit(f"engine/runner.py declares N_RUNS={declared}, this estimate assumes "
                         f"{N_RUNS}; the estimate would be wrong by a factor of "
                         f"{(declared or 0) / N_RUNS:.2f}")
    out = config.out_paths()
    items = repairable_items(out["tables"] / "window_buckets.csv")
    costs = per_call_costs(root / "results" / "run_ledger.jsonl")
    labels = sorted(config.serving_paths())
    est = estimate(len(items), labels, costs)
    est["tasks"] = sorted({r["leaf"] for r in items})
    est["items"] = [f"{r['leaf']}/{r['item']}" for r in items]
    print(f"repairable items: {est['n_items']} across {len(est['tasks'])} tasks")
    for t in est["tasks"]:
        print(f"    {t}: {sum(1 for r in items if r['leaf'] == t)}")
    print(f"\ncall unit: one call per item per run (engine/coverage.py expected_calls)")
    print(f"  {est['n_items']} items x {N_RUNS} runs x {est['n_configs']} configs "
          f"= {est['total_calls']:,} calls")
    print(f"\nmeasured $/call, per configuration (from results/run_ledger.jsonl):")
    for l in est["priced_configs"]:
        print(f"    {l:<22} ${costs[l]:.6f}/call  ->  ${est['per_config_usd'][l]:.4f}")
    print(f"\n  priced:   {est['priced_calls']:,} calls  ${est['priced_total_usd']:.2f}")
    # "No measured spend" is two different things and reporting them as one hides the only line
    # that carries a real decision. A locally served model costs no cash whatever it costs in
    # time; a paid endpoint with no ledger row is unmeasured, which is not the same as free.
    paths = config.serving_paths()
    by_path = {}
    for l in est["unpriced_configs"]:
        by_path.setdefault(paths[l], []).append(l)
    est["unpriced_by_path"] = by_path
    for path, labels_p in sorted(by_path.items()):
        cash = "no cash cost, local compute" if path == "local" else \
               "PAID endpoint with no measured spend in the ledger -- cost UNKNOWN"
        print(f"  {path:<8} {len(labels_p) * est['calls_per_config']:>5,} calls  "
              f"{', '.join(labels_p)}\n           {cash}")
    # An upper bound, not a guess. Every unpriced PAID call is charged at the most expensive rate
    # anywhere in the measured lineup, so the true cost cannot exceed this figure. A bound that
    # can only be too high is the right shape for an authorisation request; a central estimate
    # that could be too low is not.
    worst = max(costs.values())
    unpriced_paid = sum(len(v) for k, v in by_path.items() if k != "local") * est["calls_per_config"]
    est["worst_case_usd"] = est["priced_total_usd"] + unpriced_paid * worst
    est["worst_case_rate"] = worst
    est["bills_anthropic_direct"] = [l for l in labels if paths[l] == "direct"
                                     and "haiku" in l or "claude" in l]
    print(f"\n  WORST CASE: ${est['worst_case_usd']:.2f}  "
          f"(every unpriced paid call charged at the lineup's dearest measured rate, "
          f"${worst:.6f}/call)")
    if est["bills_anthropic_direct"]:
        print(f"  NOTE: {', '.join(est['bills_anthropic_direct'])} bills api.anthropic.com "
              f"directly and needs its own explicit approval, separate from the dollar total.")
    (out["out"] / "block2b_estimate.json").write_text(json.dumps(est, indent=1))
    return est


if __name__ == "__main__":
    main()
