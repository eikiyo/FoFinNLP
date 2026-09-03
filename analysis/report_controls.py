"""
Location: paper-a/analysis/report_controls.py
Purpose: The two report sections that answer the brief's hardest questions -- 5f (does agreement
         survive within answer-type strata, and is a failing stratum just the tie problem again?)
         and 4c (the tie-immune concentration route). Split out of report_results.py to stay
         inside the LOC budget.
Functions: strata_section(), concentration_section()
Calls: none (pure over the context dict)
Imports: typing, config, tables_out
"""

from typing import Any, Dict, List

import config
import tables_out as T


def _strata_rows(ctx: Dict[str, Any]) -> List[List[str]]:
    rows = []
    for kind, s in ctx["strata"].items():
        nl = ctx["strata_nulls"].get(kind)
        note = "n<4 leaves - not a distribution" if s["too_small"] else ""
        if nl and s["summary"]["median"] is not None and s["summary"]["median"] <= nl["p97_5"]:
            note = (note + " · " if note else "") + "**does NOT clear its own null**"
        rows.append([kind, str(s["n_leaves"]), str(s["summary"]["n_pairs"]),
                     str(s["summary"]["n_defined"]), T.fmt(s["summary"]["median"]),
                     T.fmt(s["summary"]["iqr"]), T.fmt(s["mean_tie"]),
                     T.fmt(nl["median_of_medians"]) if nl else "—",
                     T.fmt(nl["p97_5"]) if nl else "—", T.fmt(nl["p"], 4) if nl else "—", note])
    return rows


def _q7_verdict(d: Dict[str, Any]) -> List[str]:
    return [
        f"> **This is the answer to the brief's question 7, and it is not the comfortable one.** "
        f"Agreement is carried by the **{'/'.join(sorted(d['carried_strata']))}** strata and does "
        f"NOT clear its own null on **{'/'.join(sorted(d['failed_strata']))}**. So answer FORMAT "
        f"is part of what the headline is measuring, not clause type alone. The brief says either "
        f"answer is publishable but not knowing which is not -- this is the which.",
        "",
    ]


def _tie_confound_check(ctx: Dict[str, Any], d: Dict[str, Any]) -> List[str]:
    """The obvious rival explanation for a failing stratum -- that its ties simply hide the signal
    -- is TESTED against that stratum's own tie mass rather than asserted in either direction."""
    st = ctx["strata"]
    fails = [k for k in d["failed_strata"] if not st[k]["too_small"]]
    carr = [k for k in d["carried_strata"] if not st[k]["too_small"]]
    if not fails:
        return ["> Every stratum that failed is below the leaf-count floor, so nothing is claimed "
                "about it in either direction.", ""]
    if not carr:
        return []
    fail = max(fails, key=lambda k: st[k]["mean_tie"])
    carry = max(carr, key=lambda k: st[k]["mean_tie"])
    if st[fail]["mean_tie"] <= st[carry]["mean_tie"]:
        verdict = (f"**No.** `{carry}` carries MORE tie mass ({T.fmt(st[carry]['mean_tie'])} vs "
                   f"{T.fmt(st[fail]['mean_tie'])}) and still reaches "
                   f"{T.fmt(st[carry]['summary']['median'])}, while `{fail}` sits at "
                   f"{T.fmt(st[fail]['summary']['median'])}. With tie mass effectively matched, "
                   f"the gap between the strata is a real difference in cross-model agreement, "
                   f"not the estimator's blind spot.")
    else:
        verdict = (f"**Possibly.** `{fail}` carries more tie mass ({T.fmt(st[fail]['mean_tie'])} "
                   f"vs {T.fmt(st[carry]['mean_tie'])}), so read its null result as 'not "
                   f"demonstrated here', never as 'demonstrated absent'.")
    return [f"> Is that just the tie problem again, one level down? {verdict}", ""]


def strata_section(ctx: Dict[str, Any]) -> List[str]:
    d = ctx["decision"]
    lines = [
        "## 5f. Answer-space strata",
        "",
        "Per-leaf classification with justifications: `out/answer_types.md`. Distributions are "
        "computed on the active subset, restricted to each stratum's leaves. `mean tie` is the "
        "average tie fraction INSIDE that stratum -- reported because a low stratum median has "
        "two possible causes (no agreement, or an estimator that cannot see agreement through the "
        "ties) and only this column separates them.",
        "",
        T.md_table(["Answer type", "leaves", "pairs", "defined", "median rho", "IQR",
                    "mean tie", "null median", "null 97.5", "p", "note"], _strata_rows(ctx)),
        "",
    ]
    if d["failed_strata"]:
        lines += _q7_verdict(d) + _tie_confound_check(ctx, d)
    return lines


def _conc_rows(ctx: Dict[str, Any]) -> List[List[str]]:
    return [[f"`{r['model']}`", str(r["n_nonzero"]), str(r["top_k_nonzero"]),
             T.pct(r["share_of_rate_mass"]), T.pct(r["share_of_item_mass"]),
             ", ".join("`" + n + "`" for n in r["top_k"][:5])] for r in ctx["conc"]]


def concentration_section(ctx: Dict[str, Any]) -> List[str]:
    ov, po = ctx["overlap"], ctx["pair_overlap"]
    return [
        "## 4c. Concentration -- the tie-immune route",
        "",
        "Set overlap does not care how many leaves are tied at zero, so it answers the same "
        "question without Spearman's tie penalty. Padding is removed: for a model with fewer than "
        f"{config.TOP_K} non-zero leaves only its non-zero entries count.",
        "",
        T.md_table(["Model", "non-zero leaves", "top-10 that are non-zero",
                    "top-10 share of rate mass", "top-10 share of flipped items",
                    "top 5 leaves"], _conc_rows(ctx)),
        "",
        f"- Strict intersection of all 12 top-10 sets: **{ov['intersection_size']}** leaf/leaves"
        + (f" ({', '.join('`' + n + '`' for n in ov['intersection'])})"
           if ov["intersection"] else "") + f"; union {ov['union_size']}.",
        f"- Pairwise overlap across the 66 pairs: median **{po['median_shared']}** shared leaves "
        f"(min {po['min_shared']}, max {po['max_shared']}), median Jaccard "
        f"{T.fmt(po['median_jaccard'])}.",
        "",
        "Leaves appearing in the most models' top-10 (the shape a shared difficulty dimension "
        "would take if it existed):",
        "",
        T.md_table(["Leaf", "models (of 12)"],
                   [[f"`{n}`", str(c)] for n, c in ctx["leaf_hits"][:12]]),
        "",
    ]
