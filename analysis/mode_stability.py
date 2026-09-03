"""
Location: paper-a/analysis/mode_stability.py
Purpose: How often would a model's MODAL answer change between two independent 20-run samples,
         with no change to the model at all? Needed because the local configurations had to be
         re-pulled, and "the modal answer reproduced on 12 of 14 items" means nothing until it is
         compared against what resampling the SAME model would produce. An unstable model changes
         its mode by chance; a fixed agreement floor cannot tell that from changed weights.
         Usage:  python3 analysis/mode_stability.py
Functions: mode_change_prob(), expected_changes(), calibrate(), selftest()
Calls: none (pure resampling over the stored per-run values)
Imports: collections, random, typing
"""

from collections import Counter
from typing import Any, Dict, List, Sequence

SEED = 20260729
DRAWS = 4000


def mode_change_prob(values: Sequence[Any], n_draws: int = DRAWS, seed: int = SEED) -> float:
    """P(a fresh n-run sample from this item's own distribution has a different mode).

    The stored 20 values ARE the empirical distribution of what this model says about this item,
    so resampling them with replacement is the null: same model, same item, new sample. A tie in
    the resample is counted as a change, matching Counter.most_common's arbitrary tie-break, which
    is what the comparison being calibrated would also see."""
    vals = list(values)
    if not vals:
        return 0.0
    base = Counter(vals).most_common(1)[0][0]
    rng = __import__("random").Random(seed)
    n, changed = len(vals), 0
    for _ in range(n_draws):
        draw = [vals[rng.randrange(n)] for _ in range(n)]
        if Counter(draw).most_common(1)[0][0] != base:
            changed += 1
    return changed / n_draws


def expected_changes(per_item_values: Dict[str, Sequence[Any]]) -> Dict[str, Any]:
    """Expected count of mode changes across items, and the per-item probabilities.

    The expected count is a sum of independent Bernoulli probabilities, so its variance is the
    sum of p(1-p) -- reported, because a bare expectation invites comparing an observed integer to
    a mean with no sense of the spread."""
    ps = {k: mode_change_prob(v) for k, v in per_item_values.items()}
    exp = sum(ps.values())
    var = sum(p * (1 - p) for p in ps.values())
    return {"n_items": len(ps), "expected": exp, "sd": var ** 0.5, "per_item": ps}


def calibrate(observed_changes: int, per_item_values: Dict[str, Sequence[Any]]) -> Dict[str, Any]:
    """Is the observed number of mode changes consistent with resampling the same model?

    Reported as a z-score against the resampling null, not against a chosen agreement floor. The
    floor this replaces was 0.90, picked with no reference to how unstable these models are: on a
    configuration whose published wobble is 0.38, two independent samples disagree on the mode for
    a good share of items with nothing wrong at all, and the floor would call that a changed
    build every time."""
    e = expected_changes(per_item_values)
    if e["sd"] == 0:
        # Zero variance means the null admits exactly one outcome, so consistency is equality --
        # NOT an automatic pass. Returning True on a None z-score made an impossible observation
        # (ten mode changes across items that cannot change) report as consistent: a degenerate
        # input turning the comparison vacuous, which the selftest caught before it was used.
        return {**e, "observed": observed_changes, "z": None,
                "consistent": abs(observed_changes - e["expected"]) < 1e-9}
    z = (observed_changes - e["expected"]) / e["sd"]
    return {**e, "observed": observed_changes, "z": z,
            # Two sigma, stated in advance rather than after seeing z.
            "consistent": abs(z) <= 2.0}


def selftest() -> str:
    """A stable item must almost never change its mode; a split one often must."""
    stable = mode_change_prob(["a"] * 20)
    assert stable == 0.0, f"a unanimous item cannot change its mode, got {stable}"
    near = mode_change_prob(["a"] * 19 + ["b"])
    assert near < 0.05, f"a 19-1 item should rarely flip its mode, got {near}"
    split = mode_change_prob(["a"] * 10 + ["b"] * 10)
    assert split > 0.3, f"a 10-10 item must flip its mode often, got {split}"
    c = calibrate(0, {"i": ["a"] * 20})
    assert c["consistent"], "zero changes on a stable set must be consistent"
    c2 = calibrate(10, {f"i{i}": ["a"] * 20 for i in range(10)})
    assert not c2["consistent"], "ten changes where none are possible must be inconsistent"
    return ("mode_stability selftest PASS - unanimous items never change mode, 19-1 items rarely, "
            "10-10 items often, and the calibration flags impossible change counts")


if __name__ == "__main__":
    print(selftest())
