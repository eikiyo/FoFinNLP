"""
Location: paper-a/analysis/decision.py
Purpose: Turn the computed distributions into ONE named row of the brief's section-6 outcome
         table, by evaluating pre-registered criteria in code. The outcome is DERIVED, never
         hand-typed beside its own table. Each distribution is scored against ITS OWN permutation
         null (same models, same leaves, same tie structure) -- never a borrowed one.
Functions: above(), criteria(), decide()
Calls: none (pure over summary/null dicts)
Imports: typing
"""

from typing import Any, Dict, List, Optional, Tuple

# Pre-registered thresholds, declared before any coefficient was looked at and reported in the
# output, so a reader can disagree with the threshold rather than with a hidden judgement.
TIGHT_IQR = 0.40          # IQR at or below this counts as "tight"
NEAR_NULL_MARGIN = 0.05   # within this of the null median counts as "indistinguishable"
MIN_PAIRS_FOR_DIST = 4    # below this a group is reported but cannot carry a distribution

Pair = Tuple[Dict[str, Any], Dict[str, Any]]   # (summary, its own null)


def above(pair: Optional[Pair]) -> Optional[bool]:
    """Is the observed median above this distribution's own permutation null (97.5th percentile of
    the null median)? None when undefined -- an unanswerable question is not a False."""
    if not pair:
        return None
    summary, null = pair
    if summary.get("median") is None or null.get("p97_5") is None:
        return None
    if summary.get("n_defined", 0) < MIN_PAIRS_FOR_DIST:
        return None
    return summary["median"] > null["p97_5"]


def _row(name: str, value: str, verdict: Optional[bool]) -> Dict[str, Any]:
    return {"name": name, "value": value, "verdict": verdict}


def criteria(reported: Pair, subsets: Dict[str, Pair], tiers: Dict[str, Pair],
             primary_computable: bool, strata: Dict[str, Pair]) -> List[Dict[str, Any]]:
    """Every named criterion with its computed value and verdict, printed in full."""
    s, n = reported
    out = [_row("the PRE-REGISTERED primary (tie-filtered headline set) is computable",
                "yes" if primary_computable else
                "NO - the tie rule leaves fewer than two models, so it has zero pairs",
                primary_computable)]
    if s["median"] is not None:
        gap = abs(s["median"] - n["median_of_medians"])
        out += [
            _row("reported median above its own permutation null (97.5th pct of the null median)",
                 f"{s['median']:.4f} vs {n['p97_5']:.4f}", above(reported)),
            _row(f"reported median indistinguishable from the null median "
                 f"(within {NEAR_NULL_MARGIN})",
                 f"gap to null median = {gap:.4f}", gap <= NEAR_NULL_MARGIN),
            _row(f"IQR tight (<= {TIGHT_IQR})", f"{s['iqr']:.4f}", s["iqr"] <= TIGHT_IQR),
        ]
    for key, label in (("all_full", "full 60-leaf set"), ("all_active", "active subset"),
                       ("all_common", "common subset")):
        p = subsets.get(key)
        val = "undefined" if not p or p[0]["median"] is None else f"{p[0]['median']:.4f}"
        out.append(_row(f"above the null on the {label} (all 12 models)", val, above(p)))
    for name, group in (("group", tiers), ("answer-type stratum", strata)):
        for key, p in group.items():
            ok = p[0]["n_defined"] >= MIN_PAIRS_FOR_DIST
            val = ("undefined" if p[0]["median"] is None else f"{p[0]['median']:.4f}") + \
                  ("" if ok else f"  [{p[0]['n_defined']} defined pair(s) - not a distribution]")
            out.append(_row(f"{name} '{key}' median above its own null", val, above(p)))
    return out


def decide(reported: Pair, subsets: Dict[str, Pair], tiers: Dict[str, Pair],
           primary_computable: bool, strata: Dict[str, Pair]) -> Dict[str, Any]:
    """Name exactly ONE row of the brief's section-6 table, with the chain that produced it."""
    crit = criteria(reported, subsets, tiers, primary_computable, strata)
    sub_verdicts = {k: above(v) for k, v in subsets.items()}
    defined = [v for v in sub_verdicts.values() if v is not None]
    reversal = len(set(defined)) > 1
    s = reported[0]
    is_above = above(reported)
    tight = s["iqr"] is not None and s["iqr"] <= TIGHT_IQR
    tier_v = {t: above(p) for t, p in tiers.items()}
    across = tier_v.get("ACROSS")

    strat_v = {k: above(p) for k, p in strata.items()}
    failed_strata = [k for k, v in strat_v.items() if v is False]
    carried = [k for k, v in strat_v.items() if v is True]
    qualifier = ("" if not failed_strata else
                 f" It is QUALIFIED: the agreement is carried by the "
                 f"{'/'.join(sorted(carried))} strata and does NOT clear its own null on the "
                 f"{'/'.join(sorted(failed_strata))} stratum, so answer format is part of what is "
                 f"being measured - see 5f before writing the thesis sentence.")

    if reversal:
        row, why = 4, ("the above-the-null verdict is NOT stable across the full / active / common "
                       "subsets, so the measurement pipeline is doing the work")
    elif is_above and across is False:
        row, why = 3, ("models agree within a capability tier but the across-tier distribution "
                       "does not clear its own null")
    elif is_above and tight and all(v is not False for v in tier_v.values()):
        row, why = 1, ("the reported median clears a permutation null built with this data's exact "
                       "tie structure, with a tight IQR, and holds inside both capability tiers "
                       "and across them." + qualifier)
    elif is_above:
        row, why = 1, ("the reported median clears its own permutation null, though not every "
                       "secondary criterion is clean - see the criteria table." + qualifier)
    elif is_above is None:
        row, why = 4, ("no distribution in this analysis is computable, which is a fact about the "
                       "measurement, not about the models")
    else:
        row, why = 2, ("the reported median does not clear its own permutation null after the tie, "
                       "drop and subset controls")
    names = {1: "Row 1 - the paper as originally briefed (task properties, not model identity, "
                "drive instability)",
             2: "Row 2 - instability does not transfer across models",
             3: "Row 3 - models converge on what is hard as capability rises",
             4: "Row 4 - STOP: a methods finding about the measurement pipeline"}
    return {"row": row, "row_name": names[row], "reason": why, "criteria": crit,
            "reversal": reversal, "subset_verdicts": sub_verdicts, "tier_verdicts": tier_v,
            "stratum_verdicts": strat_v, "failed_strata": failed_strata,
            "carried_strata": carried, "primary_computable": primary_computable}
