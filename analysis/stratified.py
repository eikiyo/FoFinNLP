"""
Location: paper-a/analysis/stratified.py
Purpose: Camera-ready T4-T7. The flagged-vs-clean contrast per answer-type stratum (pooled /
         numeric / non-numeric) and per configuration set (all 12 / frontier 10), with an
         item-level bootstrap interval beside Wilson and graded dispersion beside binary wobble.
         Answers reviewer ncjD (answer-type and difficulty confound, clustering-blind CIs, 1B
         models carrying the effect) and taFL (severity-blind binary wobble) from ONE tidy frame.
Functions: stratified_contrast(), _emit(), write_stratified(), selftest()
Calls: flagged_profile.rate/_flat (reused), contamination.newcombe, config.PERM_SEED
Imports: pathlib, typing, numpy, config, contamination, flagged_profile, tables_out
"""

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

import config
import contamination as C
import flagged_profile as FP
import tables_out as T

STRATA: Tuple[Tuple[str, Callable], ...] = (
    ("pooled", lambda r: True),
    ("numeric", lambda r: r["answer_type"] == "numeric"),
    ("non-numeric", lambda r: r["answer_type"] != "numeric"))

# The three causes behind the single flag (Section 3 of the paper); order is report order.
FAILURE_STRATA = ("evidence-absent", "computational", "quote-absent-from-source")

STRAT_COLS = ("config_set", "stratum", "group", "items", "pairs", "flips", "wobble",
              "w_lo", "w_hi", "boot_lo", "boot_hi", "dispersion", "disp_boot_lo",
              "disp_boot_hi", "acc_n", "accuracy", "a_lo", "a_hi", "newcombe")
STRAT_HEAD = list(STRAT_COLS[:-1]) + ["newcombe_d", "newcombe_lo", "newcombe_hi",
                                      "newcombe_excludes_zero"]


def _boot(rows: Sequence[Dict[str, Any]], rng, n_boot: int) -> Dict[str, Any]:
    """Item-resampled pooled wobble and dispersion draws. Items are the resampling unit because
    the flagged model-item pairs are items crossed with configurations: a pair-level interval
    treats 12 measurements of one item as independent draws and they are not."""
    pairs = np.array([r["pairs"] for r in rows], dtype=float)
    flips = np.array([r["flips"] for r in rows], dtype=float)
    disp = np.array([float(r.get("disp", 0.0)) for r in rows], dtype=float)
    idx = rng.integers(0, len(rows), size=(n_boot, len(rows)))
    p = pairs[idx].sum(axis=1)
    safe = np.where(p > 0, p, 1.0)
    return {"wobble": np.where(p > 0, flips[idx].sum(axis=1) / safe, np.nan),
            "dispersion": np.where(p > 0, disp[idx].sum(axis=1) / safe, np.nan)}


def _pct(draws) -> Tuple[float, float]:
    return (float(np.nanpercentile(draws, 2.5)), float(np.nanpercentile(draws, 97.5)))


def _group_row(cset: str, sname: str, group: str, r_: Dict[str, Any],
               b_: Dict[str, Any]) -> Dict[str, Any]:
    (blo, bhi), (dlo, dhi) = _pct(b_["wobble"]), _pct(b_["dispersion"])
    return {"config_set": cset, "stratum": sname, "group": group, **r_,
            "boot_lo": blo, "boot_hi": bhi, "disp_boot_lo": dlo, "disp_boot_hi": dhi}


def _diff_row(cset: str, sname: str, a: Dict[str, Any], b: Dict[str, Any],
              w_diff, d_diff) -> Dict[str, Any]:
    (wlo, whi), (ddlo, ddhi) = _pct(w_diff), _pct(d_diff)
    return {"config_set": cset, "stratum": sname, "group": "difference",
            **{k: None for k in ("items", "pairs", "flips", "acc_n", "w_lo", "w_hi",
                                 "accuracy", "a_lo", "a_hi")},
            "wobble": a["wobble"] - b["wobble"],
            "dispersion": a["dispersion"] - b["dispersion"],
            "boot_lo": wlo, "boot_hi": whi, "disp_boot_lo": ddlo, "disp_boot_hi": ddhi,
            "newcombe": C.newcombe(a["flips"], a["pairs"], b["flips"], b["pairs"])}


def stratified_contrast(rows_by_set: Sequence[Tuple[str, Sequence[Dict[str, Any]]]],
                        n_boot: int = 2000, seed: Optional[int] = None
                        ) -> List[Dict[str, Any]]:
    """One tidy frame: three rows (flagged, clean, difference) per populated stratum per
    configuration set. A stratum one side of the contrast does not populate is SKIPPED, never
    reported as zero. Seeded once for the whole frame: deterministic for fixed input and draws."""
    rng = np.random.default_rng(config.PERM_SEED if seed is None else seed)
    out: List[Dict[str, Any]] = []
    for cset, rows in rows_by_set:
        for sname, pred in STRATA:
            sub = [r for r in rows if pred(r)]
            _emit(out, cset, sname, [r for r in sub if r["flagged"]],
                  [r for r in sub if not r["flagged"]], rng, n_boot)
    # Failure-type strata (camera-ready fix 1.1), pooled configuration set only: the flagged
    # side is one failure group, the comparator is the WHOLE clean set, because a failure type
    # is a property of flagged items and induces no split of the clean ones. Appended after the
    # answer-type loop so the rng stream consumed by the published strata is byte-identical to
    # the one that produced them; a draw order change would silently move every interval.
    rows_all = dict(rows_by_set).get("all", [])
    cl = [r for r in rows_all if not r["flagged"]]
    for fname in FAILURE_STRATA:
        _emit(out, "all", fname,
              [r for r in rows_all if r["flagged"] and r.get("failure") == fname], cl,
              rng, n_boot)
    return out


def _emit(out: List[Dict[str, Any]], cset: str, sname: str, fl, cl, rng, n_boot: int) -> None:
    """Three rows (flagged, clean, difference) for one stratum, or none: a stratum either side
    of the contrast does not populate is SKIPPED, never reported as zero."""
    if not fl or not cl:
        return
    bf, bc = _boot(fl, rng, n_boot), _boot(cl, rng, n_boot)
    a, b = FP.rate(fl), FP.rate(cl)
    out.append(_group_row(cset, sname, "flagged", a, bf))
    out.append(_group_row(cset, sname, "clean", b, bc))
    out.append(_diff_row(cset, sname, a, b, bf["wobble"] - bc["wobble"],
                         bf["dispersion"] - bc["dispersion"]))


def write_stratified(strat: List[Dict[str, Any]], tables: Path) -> Path:
    return T.write_csv(tables / "stratified_contrast.csv", STRAT_HEAD,
                       [FP._flat(r, STRAT_COLS) for r in strat])


def _fixture() -> List[Dict[str, Any]]:
    def row(leaf, flagged, atype, pairs, flips, disp, ok, failure=""):
        return {"leaf": leaf, "item": f"{leaf}-{flagged}-{flips}", "answer_type": atype,
                "flagged": flagged, "pairs": pairs, "flips": flips, "disp": disp,
                "maj_n": pairs, "maj_ok": ok, "failure": failure}
    return [row("a", 1, "numeric", 10, 9, 4.5, 2, "evidence-absent"),
            row("a", 1, "numeric", 10, 8, 4.0, 3, "computational"),
            row("b", 0, "numeric", 10, 1, 0.2, 9), row("b", 0, "numeric", 10, 0, 0.0, 10),
            row("c", 0, "binary", 10, 0, 0.0, 10)]


def selftest() -> str:
    """Closed-form point estimates, seeded determinism, a difference that must exclude zero on a
    gross contrast, and the two refusal arms: an unpopulated stratum yields NO row, and a
    single-sided stratum (no flagged items) yields no row rather than a zero; failure-type
    strata score against the whole clean set, appear for the pooled configuration set only,
    and an empty failure group is skipped."""
    fx = _fixture()
    frame = stratified_contrast([("all", fx)], n_boot=500, seed=7)
    strata = {(r["stratum"], r["group"]) for r in frame}
    assert ("non-numeric", "flagged") not in strata, \
        "non-numeric has no flagged item; the stratum must be skipped, not scored"
    pooled = {r["group"]: r for r in frame if r["stratum"] == "pooled"}
    assert abs(pooled["flagged"]["wobble"] - 0.85) < 1e-12, pooled["flagged"]
    assert abs(pooled["flagged"]["dispersion"] - 0.425) < 1e-12, pooled["flagged"]
    assert abs(pooled["clean"]["wobble"] - (1 / 30)) < 1e-12, pooled["clean"]
    d = pooled["difference"]
    assert d["newcombe"]["excludes_zero"], "a 0.85-vs-0.03 split must exclude zero (Newcombe)"
    assert d["boot_lo"] > 0, f"the item bootstrap must also exclude zero here: {d['boot_lo']}"
    assert pooled["flagged"]["boot_lo"] <= pooled["flagged"]["wobble"] \
        <= pooled["flagged"]["boot_hi"], "the interval must contain the point estimate"
    again = stratified_contrast([("all", fx)], n_boot=500, seed=7)
    assert frame == again or all(
        a == b or all(a.get(k) == b.get(k) or abs((a.get(k) or 0) - (b.get(k) or 0)) < 1e-15
                      for k in a) for a, b in zip(frame, again)), "same seed must reproduce"
    numeric = {r["group"]: r for r in frame if r["stratum"] == "numeric"}
    assert numeric["clean"]["items"] == 2, "the binary item must be outside the numeric stratum"
    ea = {r["group"]: r for r in frame if r["stratum"] == "evidence-absent"}
    assert abs(ea["flagged"]["wobble"] - 0.9) < 1e-12, ea["flagged"]
    assert ea["clean"]["items"] == 3, \
        "a failure stratum's comparator is the WHOLE clean set, binary item included"
    assert ("quote-absent-from-source", "flagged") not in strata, \
        "a failure group with no member must be skipped, not scored"
    assert not any(r["config_set"] == "frontier" and r["stratum"] == "evidence-absent"
                   for r in frame), "failure strata are pooled-set only"
    # The published strata must not move when the failure strata are appended: their rows are
    # drawn from the rng stream FIRST, so equality against the pre-addition closed forms above
    # is the guard; this asserts the frame still starts with them in order.
    assert [(r["config_set"], r["stratum"], r["group"]) for r in frame[:3]] == \
        [("all", "pooled", "flagged"), ("all", "pooled", "clean"), ("all", "pooled", "difference")]
    return ("stratified selftest PASS - closed-form wobble and dispersion, Newcombe and item "
            "bootstrap both exclude zero on a gross contrast, intervals contain their point, an "
            "unpopulated stratum is skipped rather than scored, failure strata score against the "
            "whole clean set on the pooled configuration set only, and a fixed seed "
            "reproduces the frame exactly")


if __name__ == "__main__":
    print(selftest())
