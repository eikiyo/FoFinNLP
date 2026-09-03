"""
Location: paper-a/analysis/rbo.py
Purpose: BLOCK 1d. Rank-biased overlap (Webber, Moffat and Zobel 2010) between two item rankings.
         Answers the objection top-k invites: RBO is defined for rankings of UNEQUAL length and
         weights by rank rather than cutting at a threshold, so it cannot be an artefact of where
         the cut was placed. Truncated, never extrapolated -- the RBO_EXT residual assumes the
         unseen tail resembles the seen part, which is exactly the assumption under test.
Functions: rbo_at(), weight_covered(), pair_rbo(), selftest()
Calls: none (pure)
Imports: typing
"""

from typing import Dict, List, Optional, Sequence

# Expected viewing depth is 1/(1-p), so p=0.9 concentrates the weight on about the first ten
# ranks. Chosen because the frontier configurations carry between 6 and 30 unstable items, so a
# deeper p would spend most of its weight on ranks that do not exist for half the lineup, and a
# shallower one would ask a question the top-5 statistic already answers.
P_DEFAULT = 0.9


def rbo_at(a: Sequence[str], b: Sequence[str], p: float = P_DEFAULT,
           depth: Optional[int] = None) -> float:
    """Truncated RBO to `depth`, defaulting to the longer ranking.

        RBO = (1 - p) * SUM_{d=1..depth} p^(d-1) * |A_1:d INTERSECT B_1:d| / d

    Beyond a list's own length its prefix simply stops growing, which is how a short ranking is
    compared with a long one without padding it: padding would invent agreement at ranks the
    model never produced, and that is the failure this statistic exists to avoid."""
    depth = depth or max(len(a), len(b))
    if depth <= 0:
        return 0.0
    sa, sb, total = set(), set(), 0.0
    for d in range(1, depth + 1):
        if d <= len(a):
            sa.add(a[d - 1])
        if d <= len(b):
            sb.add(b[d - 1])
        total += (p ** (d - 1)) * len(sa & sb) / d
    return (1 - p) * total


def weight_covered(depth: int, p: float = P_DEFAULT) -> float:
    """Share of RBO's total weight that a ranking of this depth can carry.

    Reported with every RBO value: a truncated RBO is bounded above by this number, so a score of
    0.30 at 60% coverage and one at 99% coverage are not the same measurement, and printing them
    in one column without it would make a short ranking look like a disagreeing one."""
    return sum((1 - p) * p ** (d - 1) for d in range(1, max(depth, 0) + 1))


def max_rbo(len_a: int, len_b: int, p: float = P_DEFAULT) -> float:
    """The HIGHEST score two rankings of these lengths can reach: the shorter one is a prefix of
    the longer.

    A truncated RBO cannot reach 1.0 -- two identical rankings of length 20 score 0.878 at p=0.9,
    because the remaining weight sits at ranks neither list has. Reporting a raw RBO without this
    ceiling makes a SHORT ranking indistinguishable from a DISAGREEING one, which would turn the
    six-unstable-item configurations into apparent outliers purely for being small."""
    order = [str(i) for i in range(max(len_a, len_b))]
    return rbo_at(order[:len_a], order[:len_b], p)


def ranking(vec: Dict[str, float]) -> List[str]:
    """A model's items ordered by instability, NON-ZERO only and ties broken by key.

    Zero-dispersion items are unranked by construction: a model that never wavered on an item has
    expressed no order over it, and admitting them would let two models agree by sharing the same
    alphabetically-first stable item."""
    return [k for k, v in sorted(vec.items(), key=lambda kv: (-kv[1], kv[0])) if v > 0]


def pair_rbo(vecs: Dict[str, Dict[str, float]], models: Sequence[str],
             p: float = P_DEFAULT) -> List[Dict[str, object]]:
    """RBO for every unordered pair, with each side's depth and the weight the shorter one covers.
    Unordered because RBO is symmetric, unlike the directed top-k transfer."""
    ranks = {m: ranking(vecs[m]) for m in models}
    out = []
    for i, a in enumerate(models):
        for b in list(models)[i + 1:]:
            la, lb = len(ranks[a]), len(ranks[b])
            ceiling = max_rbo(la, lb, p)
            raw = rbo_at(ranks[a], ranks[b], p)
            out.append({"model_a": a, "model_b": b, "rbo": raw, "depth_a": la, "depth_b": lb,
                        "ceiling": ceiling, "normalised": (raw / ceiling) if ceiling else None,
                        "weight_covered": weight_covered(min(la, lb), p), "p": p})
    return out


def _st_weights() -> float:
    """The ceiling, the depth-weight curve, and the exclusion of unranked items."""
    assert weight_covered(0) == 0.0, "zero depth covers no weight"
    w10 = weight_covered(10)
    assert 0.6 < w10 < 0.7, f"p=0.9 must put about two thirds of its weight in the top ten: {w10}"
    assert weight_covered(60) > w10, "more depth must cover more weight"
    assert ranking({"a": 0.5, "b": 0.0, "c": 0.9}) == ["c", "a"], \
        "zero-dispersion items must be unranked, not ordered alphabetically into the tail"
    return w10


def selftest() -> str:
    """Prove RBO on cases whose value is known by construction, in both directions."""
    w10 = _st_weights()
    x = [f"i{n}" for n in range(20)]
    # A truncated RBO cannot reach 1.0: its ceiling is the weight the depth covers. Asserting 1.0
    # here would be asserting a property the statistic does not have.
    assert abs(rbo_at(x, x) - weight_covered(20)) < 1e-12, \
        f"identical rankings must score exactly the covered weight: {rbo_at(x, x)}"
    assert abs(rbo_at(x, x) - max_rbo(20, 20)) < 1e-12, "and that IS the pair's ceiling"
    assert abs(rbo_at(x, x) / max_rbo(20, 20) - 1.0) < 1e-12, \
        "so the normalised score of an identical pair is 1.0"
    y = [f"j{n}" for n in range(20)]
    assert rbo_at(x, y) == 0.0, f"disjoint rankings must score 0.0: {rbo_at(x, y)}"

    # Order matters, and matters MORE at the top: swapping ranks 1 and 2 must cost more than
    # swapping 10 and 11, or the statistic is not rank-biased at all and p is doing nothing.
    top = list(x)
    top[0], top[1] = top[1], top[0]
    deep = list(x)
    deep[9], deep[10] = deep[10], deep[9]
    assert rbo_at(x, top) < rbo_at(x, deep), \
        f"a top swap must cost more than a deep one: {rbo_at(x, top)} vs {rbo_at(x, deep)}"

    # Unequal lengths: a short ranking that is a PREFIX of a long one must score high but below
    # 1.0, because the long one asserts an order the short one never made.
    pref = rbo_at(x[:5], x)
    assert 0.0 < pref < 1.0, f"a prefix must score between 0 and 1: {pref}"
    assert pref > rbo_at(x[:5], y), "a prefix must beat a disjoint ranking"

    # An EMPTY ranking is 0.0 and must not raise: a configuration with no unstable item at all is
    # a real possibility, and a crash there would be read as a missing row rather than a zero.
    assert rbo_at([], x) == 0.0 and rbo_at([], []) == 0.0, "an empty ranking must score 0.0"

    return (f"rbo selftest PASS - identical rankings score their depth's covered weight (which is "
            f"the pair ceiling, so normalised 1.0) and disjoint ones 0.0, a top-rank swap costs "
            f"more than a deep one, a prefix of a longer ranking scores between them, an empty "
            f"ranking is 0.0 rather than an error, and p={P_DEFAULT} covers {w10:.3f} of its "
            f"weight in the top ten")
