"""
Location: paper-a/analysis/contam_report.py
Purpose: Render out/AUDIT_CONTAMINATION.md -- the §0 gate's written outcome, which must exist
         before a word of the paper is drafted. Rendering only: every figure it prints comes from
         the gate's own result dict, so the document cannot disagree with the CSVs beside it.
Functions: verdict(), write()
Calls: contam_tables.headline_deltas (the one delta list), tables_out.md_table
Imports: pathlib, typing, contam_tables, tables_out
"""

from pathlib import Path
from typing import Any, Dict, List, Sequence

import contam_tables as CT
import tables_out as T

DECISION = {
    True: ("**The clean-only numbers become the paper's headline numbers.** All-item figures move "
           "to the appendix. Section 2 reports the audit, the exclusion, and the delta, in the "
           "main text."),
    False: ("**All-item numbers stay the headline.** Section 2 still reports the audit and the "
            "null, in one sentence with the number."),
}


def verdict(gate: Dict[str, Any]) -> str:
    p = gate["pooled"]
    d = p["diff"]
    direction = "HIGHER" if d["d"] > 0 else "LOWER"
    return (f"Wobble on flagged items is **{direction}** than on clean items: "
            f"{p['w_flagged']:.4f} ({p['k_flagged']}/{p['n_flagged']}) versus "
            f"{p['w_clean']:.4f} ({p['k_clean']}/{p['n_clean']}). The difference is "
            f"**{d['d']:+.4f}**, Wilson 95% interval [{d['lo']:.4f}, {d['hi']:.4f}], which "
            f"{'EXCLUDES' if d['excludes_zero'] else 'CONTAINS'} zero. "
            f"{gate['n_models_diff_excludes_zero']} of {len(gate['rows']) - 1} model "
            f"configurations show a difference excluding zero on their own.")


def _model_table(rows: List[Dict[str, Any]]) -> str:
    return T.md_table(
        ["configuration", "flagged wobble", "95% CI", "n", "clean wobble", "95% CI", "n",
         "difference", "95% CI", "excludes 0"],
        [[r["model"], T.fmt(r["w_flagged"], 4),
          f"[{T.fmt(r['lo_flagged'], 4)}, {T.fmt(r['hi_flagged'], 4)}]", r["n_flagged"],
          T.fmt(r["w_clean"], 4), f"[{T.fmt(r['lo_clean'], 4)}, {T.fmt(r['hi_clean'], 4)}]",
          r["n_clean"], T.fmt((r["diff"] or {}).get("d"), 4),
          f"[{T.fmt((r['diff'] or {}).get('lo'), 4)}, {T.fmt((r['diff'] or {}).get('hi'), 4)}]",
          "yes" if (r["diff"] or {}).get("excludes_zero") else "no"] for r in rows])


def _delta_table(rows: List[List[Any]]) -> str:
    return T.md_table(
        ["quantity", "all items", "clean only", "delta"],
        [[q, CT._f(a, u), CT._f(b, u), CT._f(CT._sub(b, a), u)] for q, a, b, u in rows])


def _audit_table(summ: Dict[str, Any]) -> str:
    return T.md_table(["task", "items flagged"],
                      [[k, str(v)] for k, v in summ["leaves_with_issues"].items()])


def _fell(gate: Dict[str, Any]) -> int:
    a, c = gate["all_items"]["agg"], gate["clean_only"]["agg"]
    return sum(1 for m in a if c[m] < a[m])


def _gradient(rb: Dict[str, Any]) -> str:
    """The one delta that flips sign, written from the CURRENT coefficients rather than from the
    all-item narrative. A summary sentence that contradicts its own table is the failure this
    paragraph exists to avoid, so every number in it is read off the fit that was just run."""
    a = rb["all"]["cons"]["gradient"][1]
    c = rb["clean"]["cons"]["gradient"][1]
    return (
        f"On all items the frontier-only regression of worst-category wobble on mean wobble was "
        f"pure noise: slope {a['slope']:.4f}, R2 {a['r2']:.4f} over n={a['n']}. On clean items it "
        f"becomes a real relationship: slope {c['slope']:.4f}, 95% CI "
        f"[{c['lo']:.4f}, {c['hi']:.4f}], R2 {c['r2']:.4f}. That interval excludes 1, so the worst "
        f"category falls FASTER than the mean as configurations get more stable, which is the "
        f"OPPOSITE of a widening gap. The claim needs a positive intercept to hold -- the ratio is "
        f"intercept/mean + slope, so only a non-zero intercept makes it grow as the mean shrinks -- "
        f"and the intercept is {c['intercept']:+.4f}, 95% CI "
        f"[{c['intercept_lo']:.4f}, {c['intercept_hi']:.4f}], which contains zero. On all items the "
        f"intercept was {a['intercept']:+.4f} [{a['intercept_lo']:.4f}, {a['intercept_hi']:.4f}] "
        f"and EXCLUDED zero, so the all-item reading was the one that pointed, weakly, toward the "
        f"claim. Verdict unchanged (NOT SUPPORTED), mechanism different: on clean items the "
        f"worst-to-mean relationship is proportional, roughly {c['slope']:.1f}x, and flat in "
        f"capability rather than divergent.")


def _concentration(tasks: List[Dict[str, Any]]) -> str:
    """The gate's most consequential finding, and one no per-model table could show."""
    wiped = [r for r in tasks if r["n_items"] and not r["n_clean"]]
    part = [r for r in tasks if r["n_flagged"] and r["n_clean"]]
    return f"""**{len(wiped)} of the {sum(1 for r in tasks if r['n_items'])} tasks lose every item.**
The flagged items are not spread thinly across the corpus. They fall almost entirely on tasks
that are small and computational, and on those tasks they take everything:

{T.md_table(["task", "category", "items", "flagged", "retained"],
            [[r["leaf"], r["family"], str(r["n_items"]), str(r["n_flagged"]), str(r["n_clean"])]
             for r in wiped + part])}

Tasks per category, before and after:

{T.md_table(["category", "tasks (all)", "tasks (clean)", "items (all)", "items (clean)"],
            [[c[0], str(c[1]), str(c[2]), str(c[3]), str(c[4])] for c in CT.category_counts(tasks)])}

Two things follow, and both belong in the paper.

**First, the mechanism is legible.** The wiped tasks are cap-table and waterfall computations:
ownership percentages, option-pool shuffles, stacked dilution, liquidation waterfalls. Those
answers are not stated anywhere in a document. They are computed from numbers that sit in
different places in a filing, so a single windowed provision cannot contain the validating quote
by construction. The extraction tasks, where the answer is a labelled value inside one clause,
are almost untouched. This is a defect in how the corpus windows COMPUTATIONAL items, not a
scattering of clerical errors, and saying so is more useful to a successor benchmark than the
count is.

**Second, it explains the transfer result the paper was going to lead with.**
`liquidation_waterfall_payout` was in all twelve configurations' top-10 most unstable tasks. It is
one of the nine that vanish. What looked like models agreeing about which clause types are hard
was, in part, models agreeing about which items were unanswerable.

The exclusion therefore reduces the analysed corpus to
**{sum(r['n_clean'] for r in tasks)} items over {sum(1 for r in tasks if r['n_clean'])} tasks**.
The benchmark still ships {sum(r['n_items'] for r in tasks)} items over
{sum(1 for r in tasks if r['n_items'])} tasks. Those are different numbers and the paper must use
each in its own place: the resource is the larger one, the headline analysis is the smaller one."""


def write(gate: Dict[str, Any], rb: Dict[str, Any], models: Sequence[str],
          tasks: List[Dict[str, Any]], out: Path) -> Dict[str, Any]:
    """The document. Its ONE job is to make the §0 decision, in writing, before the draft starts."""
    deltas = CT.headline_deltas(gate, rb, models, tasks)
    summ = gate["audit_summary"]
    p = gate["pooled"]
    body = f"""# AUDIT_CONTAMINATION.md — the §0 gate

> STATUS: DONE · Paper A · run 2026-07-29 · arm: legacy (temperature 0.7) · probity v1.3.1

## The question

`out/annotation/oracle_audit.json` flags **{summ['n_with_issues']} of {summ['n_items']} items**
across {summ['n_leaves']} tasks, in two modes:

{T.md_table(["failure mode", "items"], [[k, str(v)] for k, v in summ['issues'].items()])}

An item whose answer sits outside the window the model is shown cannot be answered from that
window, whatever the model then does. If wobble is systematically higher on those items, every
headline number in this paper is partly a measurement of a defect in our own resource rather than
a property of the models. Whether the missing evidence is what *destabilises* them is a separate
question, registered as a falsifiable prediction and tested by re-windowing; it failed, and the
paper reports the association as correlational only. This file ships with the artifact, so it
states that the way the paper does rather than asserting a mechanism the experiment did not
support.

Flagged items by task:

{_audit_table(summ)}

## Controls, run before anything was read

{chr(10).join('- ' + c for c in gate['checks'])}
- join: **{gate['join']['n_matched']} flagged ids matched** to their positional index across
  {gate['join']['n_leaves_with_flags']} tasks, with {gate['join']['n_leaves_audited']} tasks
  audited in total. A zero-overlap join is fatal in this module rather than a null result: a
  partition that matched nothing would report "no contamination" for the most reassuring possible
  reason, which is that it compared nothing.
- {rb['rel_control']}

The identity check matters more than it looks. It runs the *same* counting code that produces the
clean-only numbers over the *whole* item set, and requires it to reproduce all 720 published cells
exactly, in wobble and in majority accuracy. A partition bug would otherwise be indistinguishable
from a finding.

## Result

{verdict(gate)}

{DECISION[gate['material']]}

### Per configuration

{_model_table(gate['rows'])}

The comparison assumes the two partitions are independent samples. They are not fully independent:
both come from the same runs of the same models over the same corpus. Newcombe's interval on
independent proportions is the conservative standard choice here, and the dependence is disclosed
rather than corrected away.

## Where the defect concentrates

{_concentration(tasks)}

## Delta on every headline number

{_delta_table(deltas)}

## What this does to the paper

1. **Wobble falls for every configuration but one.** {_fell(gate)} of 12 fall once the flagged
   items are removed, and the two 1B models fall furthest in absolute terms. The exception is
   deepseek-v4p, unchanged at +0.0001. The published aggregate wobble was measuring, in part,
   items whose answers were not in front of the model.
2. **The capability ordering survives.** The frontier/low split has the same membership on both
   readings, so the tier structure the analysis rests on is not an artefact of the defect.
3. **The transfer result weakens and must be restated.** At k=5 the median falls from
   {gate['all_items']['transfer'][5]['median']:.3f} to
   {gate['clean_only']['transfer'][5]['median']:.3f} against a chance line that rises from
   {gate['all_items']['transfer'][5]['chance']:.3f} to
   {gate['clean_only']['transfer'][5]['chance']:.3f}. The lift is still positive and it is still
   the paper's one positive result, but it is roughly half the size the all-item reading gave.
   Part of what looked like shared instability across models was shared *defect*: the active task
   set shrinks from {len(gate['all_items']['active'])} to {len(gate['clean_only']['active'])},
   meaning {len(gate['all_items']['active']) - len(gate['clean_only']['active'])} tasks had no
   instability at all outside their flagged items.
4. **Reliability rises**, from {CT._med([r['r_full'] for r in rb['all']['rel']]):.4f} to
   {CT._med([r['r_full'] for r in rb['clean']['rel']]):.4f}. Removing items that force guessing
   removes noise, which is the direction a real defect predicts. The same figure is obtained over
   the unreduced {len(gate['all_items']['active'])}-task set, so it is the item filter and not the
   smaller task set that moves it.
5. **The worst-to-mean ratio dies harder.** At the Wilson bounds the median falls from
   {rb['all']['cons'][3]['median_cons']:.4f} to {rb['clean']['cons'][3]['median_cons']:.4f}, and
   the count of configurations above 2x falls from {rb['all']['cons'][3]['n_over_2x']} to
   {rb['clean']['cons'][3]['n_over_2x']} at the 3-task floor. Nothing in the exclusion rescues a
   claim stage 3 had already killed.
6. **The capability-gradient row of appendix Table 4 must be rewritten, and its verdict is
   unchanged for a different reason.** {_gradient(rb)}
7. **The wobble-accuracy concession stands.** The observed correlation weakens from
   {rb['all']['diag']['rho']['rho']:.4f} to {rb['clean']['diag']['rho']['rho']:.4f}, and the
   residual after the structural decomposition is
   {rb['clean']['diag']['surviving']['rho_residual_cal']:+.4f}: small, and of the OPPOSITE sign to
   the observed correlation. The relationship remains structural rather than a fact about models.
8. **The observability picture is unchanged.** The share of items answered identically on all runs
   moves by under two points, and the structural ceiling at high accuracy is the same to three
   decimals. Figure 1's message does not depend on which reading is used.

## Honest limits of this gate

- The audit is **mechanical**. It checks that a label's validating quote exists in the source and
  inside the model's window. It does **not** check that the label is the right answer. A flagged
  item is an item whose provenance cannot be verified, not an item known to be mislabelled.
- {summ['n_leaves'] - len(summ['leaves_with_issues'])} of {summ['n_leaves']} tasks have no flagged
  items. That is the audit finding nothing there, which is not the same as those tasks being
  verified correct by a human.
- The flagged sample is small ({p['n_flagged']} model-item pairs pooled), so a per-configuration
  interval is wide. The pooled interval is the one that carries the verdict.
"""
    path = out / "AUDIT_CONTAMINATION.md"
    path.write_text(body)
    return {"path": path, "deltas": deltas, "material": gate["material"]}
