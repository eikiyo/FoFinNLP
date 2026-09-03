"""
Location: paper-a/analysis/report_s3_close.py
Purpose: STAGE3_REPORT.md closing sections -- steps 2 (pre-registration only), 3 (annotation) and
         4 (scope lock) as pointers to their own documents, plus the consolidated verdict on what
         stage 3 leaves the paper able to claim.
Functions: closing()
Calls: none (pure over the stage-3 context + the annotation status)
Imports: typing, tables_out
"""

from typing import Any, Dict, List

import tables_out as T


def _status_table(ctx: Dict[str, Any], ann: Dict[str, Any]) -> str:
    s3, sv, z = ctx["survivors"][3], ctx["surviving"], ctx["zone"]
    f = ctx["worst_on_mean_frontier"]
    return T.md_table(
        ["claim the paper wanted", "status after stage 3", "what survives"],
        [["worst clause type is ~5x the headline",
          "**not supported at the bound**",
          f"median conservative ratio {T.fmt(s3['median_cons'], 2)}x; "
          f"{s3['n_over_bar']}/12 models above 2x"],
         ["the gap grows as models improve", "**not supported**",
          f"absent among the 10 frontier models (R2 = {T.fmt(f['r2'], 3)})"],
         ["instability is not just difficulty", "**conceded**",
          f"residual rho {T.fmt(sv['rho_residual_cal'], 3)} under the calibrated model"],
         ["silently-unstable-but-correct clauses do not exist",
          "**restated as a limitation**",
          f"unreachable by construction: structural max {T.fmt(z['max_structural'], 3)} "
          f"vs threshold {z['threshold_wobble']}"],
         ["the instrument is stable", "**holds** (stage 2)",
          "median split-half r_full 0.8970, unaffected by anything here"],
         ["clause-level instability is measurable in this domain", "**holds**",
          "720 cells, 14,400 model-item measurements, round-trip verified"]])


def closing(ctx: Dict[str, Any], ann: Dict[str, Any]) -> List[str]:
    return [
        "## Step 2 - The prospective test (pre-registration only; NOTHING was run)",
        "",
        "No new runs were launched and no new leaves were built. The hypothesis, the design, the "
        "cost estimate and BOTH committed outcomes are written down in advance in "
        "`out/PREREG_2a.md`, which is timestamped before any call is made. Launching it needs "
        "explicit approval, and the 2026-08-02 sourcing deadline in the brief still governs.",
        "",
        "Step 1c changed what this test is for. The empty zone is unreachable in the current item "
        "pool by construction, so a deliberate attempt to construct items inside it is no longer a "
        "nice-to-have example hunt - it is the only way to tell an item-pool limitation from a "
        "claim about models, and the pre-registration says so.",
        "",
        "## Step 3 - Annotation agreement",
        "",
        _annotation_status(ann),
        "",
        "## Step 4 - Scope lock",
        "",
        "`out/SCOPE.md` carries the page allocation and the kill list. It was rewritten after these "
        "results rather than before: two of the three results sections the brief proposed no "
        "longer have a result to carry, so an allocation written in advance would have budgeted "
        "pages to findings that did not survive.",
        "",
        "---",
        "",
        "## What stage 3 leaves the paper able to claim",
        "",
        _status_table(ctx, ann),
        "",
        "Three of the four load-bearing claims did not survive contact with a conservative reading. "
        "That is an uncomfortable result to report thirteen days out, and it is the correct one: "
        "every one of them would have been found by a reviewer instead, and two of them "
        "(the frontier-only regression, the structural decomposition) are exactly the checks a "
        "competent referee runs first.",
        "",
        "What remains is narrower and defensible: a benchmark and an instrument for clause-level "
        "answer instability in venture-financing documents, calibrated against its own measurement "
        "ceiling, showing that instability concentrates in identifiable clause types - reported "
        "with intervals wide enough that the honest headline is the concentration itself, not a "
        "multiplier. Whether that is enough for eight pages at FinNLP is a judgement for Eikiyo, "
        "and `out/SCOPE.md` sets out what it looks like if the answer is yes.",
        "",
    ]


def _annotation_status(ann: Dict[str, Any]) -> str:
    if ann.get("status") == "SCORED":
        return (f"Scored: {ann['n_paired']} paired items, agreement "
                f"{T.fmt(ann.get('agreement'), 4)}, {ann['n_disagreements']} disagreements. "
                "Full result in `out/annotation/agreement_result.csv`.")
    return ("**Prepared, NOT RUN - and it is still the single blocking item.** The blind pack is "
            "now built and the scorer is written, so the remaining work is a sitting, not a "
            "project:\n\n"
            "- `out/annotation/blind_pack.csv` - one row per item, original label withheld, order "
            "randomised under a fixed seed so the second reading cannot anchor on a run of items "
            "from one clause type.\n"
            "- `out/annotation/ADJUDICATION.md` - the protocol, the worked adjudication rule, and "
            "who decides.\n"
            "- `python3 analysis/agreement.py score` - the one command. It joins the withheld "
            "labels back by `row_id`, reports raw agreement and Cohen's kappa per answer-type "
            "stratum, and writes the disagreement list.\n\n"
            "The scorer refuses to report a number on an unfilled sheet rather than scoring empty "
            "against empty and printing a confident kappa of 1.0. Whatever comes back is reported; "
            "a low kappa is survivable and an absent one is not. If the second reading is by the "
            "same person it is reported as INTRA-annotator agreement, which is a weaker claim, and "
            "the paper must say so in those words.")
