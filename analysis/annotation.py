"""
Location: paper-a/analysis/annotation.py
Purpose: STEP 5a. Build the stratified re-annotation sample, the protocol, and an empty scoring
         sheet, so the agreement study is a short mechanical task rather than a week-two blocker.
         This module PREPARES the study; it does not and cannot produce an agreement number --
         that requires a human annotator and the report says so plainly.
Functions: stratified_sample(), write_sample(), write_protocol(), write_sheet(),
           _reading_entry(), write_reading_pack()
Calls: none (pure over leaf metadata + oracle files)
Imports: csv, json, pathlib, typing, numpy, config, tables_out
"""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Sequence

import numpy as np

import config
import tables_out as T

SAMPLE_FRACTION = 0.20
SEED = 20260729


def stratified_sample(leaves: List[Dict[str, Any]], answer_types: Dict[str, str],
                      fraction: float = SAMPLE_FRACTION, seed: int = SEED) -> List[Dict[str, Any]]:
    """A 20% leaf sample stratified by (category, answer type), drawn with a fixed seed so the
    sample is reproducible and cannot be re-drawn until it looks convenient.

    Every stratum contributes at least one leaf where the rounding would otherwise drop it: a
    sample that silently omits the small categories cannot support a claim about the whole
    benchmark, and the small categories are exactly where a lone annotator is most likely to have
    drifted."""
    rng = np.random.default_rng(seed)
    strata: Dict[tuple, List[Dict[str, Any]]] = {}
    for l in leaves:
        strata.setdefault((l["family"], answer_types.get(l["leaf"])), []).append(l)
    target = max(1, round(len(leaves) * fraction))
    picked: List[Dict[str, Any]] = []
    for key in sorted(strata, key=lambda k: (str(k[0]), str(k[1]))):
        pool = sorted(strata[key], key=lambda l: l["leaf"])
        n = max(1, round(len(pool) * fraction))
        idx = rng.permutation(len(pool))[:n]
        picked += [pool[i] for i in sorted(idx)]
    # If per-stratum rounding overshot the global target, drop from the LARGEST strata first so
    # every stratum keeps representation.
    while len(picked) > target + 2:
        counts: Dict[tuple, int] = {}
        for l in picked:
            counts[(l["family"], answer_types.get(l["leaf"]))] = \
                counts.get((l["family"], answer_types.get(l["leaf"])), 0) + 1
        big = max(counts, key=lambda k: counts[k])
        if counts[big] <= 1:
            break
        for i, l in enumerate(picked):
            if (l["family"], answer_types.get(l["leaf"])) == big:
                picked.pop(i)
                break
    return picked


def _items_of(leaf: Dict[str, Any]) -> List[Dict[str, Any]]:
    path = config.probity_root() / leaf["rel"] / "oracle.jsonl"
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def write_sample(sample: List[Dict[str, Any]], answer_types: Dict[str, str],
                 out_dir: Path, n_total_leaves: int) -> Dict[str, Any]:
    """The sample manifest: which leaves, which strata, how many items each carries."""
    rows, total = [], 0
    for l in sample:
        n = len(_items_of(l))
        total += n
        rows.append([l["leaf"], l["family"], answer_types.get(l["leaf"]), l["field"],
                     l.get("ref", ""), str(n)])
    path = out_dir / "sample.csv"
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["leaf", "category", "answer_type", "field", "ref", "n_items"])
        w.writerows(rows)
    return {"n_leaves": len(sample), "n_items": total, "path": path, "rows": rows,
            "n_total_leaves": n_total_leaves}


def write_sheet(sample: List[Dict[str, Any]], out_dir: Path) -> Path:
    """An EMPTY scoring sheet, one row per item, with the original label withheld.

    The original answer is deliberately NOT in this file. If the re-annotator can see it, the
    exercise measures agreement with a prompt, not agreement between two independent readings --
    the label has to be joined back in afterwards from oracle.jsonl by leaf + item id."""
    path = out_dir / "scoring_sheet.csv"
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["leaf", "item_id", "field", "annotator_answer", "undeterminable",
                    "notes", "minutes_spent"])
        for l in sorted(sample, key=lambda x: x["leaf"]):
            for item in _items_of(l):
                w.writerow([l["leaf"], item.get("id", ""), l["field"], "", "", "", ""])
    return path


def _reading_entry(leaf: Dict[str, Any], item: Dict[str, Any], task: Dict[str, Any],
                   window: str, url: str, row_id: str) -> str:
    """One item's reading material, as markdown. Carries the question, the answer space and the
    text the model was shown, and carries NEITHER the stored label NOR its validating quote.

    Both omissions are load-bearing. The label is obvious. The quote is not: a validating quote
    usually states the answer in words, so pasting it beside the question would turn an
    independent reading into a proofread of the original."""
    spec = (task.get("fields") or {}).get(leaf["field"], {})
    values = spec.get("values")
    answer_space = (f"one of: {', '.join(map(str, values))}" if values
                    else f"{spec.get('type', 'string')} value")
    return "\n".join([
        f"### {row_id} · {leaf['leaf']} · {item.get('id', '')}",
        f"**Question.** {task.get('description', leaf['leaf'])}",
        f"**Field.** `{leaf['field']}` -- {spec.get('description', '(no field description)')}",
        f"**Answer.** {answer_space}, or mark `undeterminable` and leave it blank.",
        f"**Source.** {url or '(no source URL recorded)'}",
        "", "**Text shown to the model:**", "", "```", window.strip() or "(NO WINDOW STORED)",
        "```", ""])


def write_reading_pack(sample: List[Dict[str, Any]], out_dir: Path, windows: Dict[Any, str],
                       urls: Dict[Any, str], tasks: Dict[str, Dict[str, Any]]) -> Path:
    """The material the protocol promises the annotator and the pack did not contain.

    blind_pack.csv names 154 items by id and says nothing about what to read, so the sitting began
    with resolving 154 identifiers to documents by hand. The protocol pointed at
    `corpus/questions/`, which does not exist in the benchmark.

    Order is READ from blind_pack.csv, never rebuilt. The pack is deliberately shuffled by seed so
    the annotator does not work through one task in a block, and the first draft of this function
    regenerated the order by sorting instead: every entry would have carried a correct-looking row
    id and another item's document. The pack file is the one source of order."""
    pack = out_dir / "blind_pack.csv"
    if not pack.exists():
        raise SystemExit(f"{pack} is absent; the reading pack must follow its order, not invent one")
    by_key = {(l["leaf"], str(i.get("id", ""))): (l, i)
              for l in sample for i in _items_of(l)}
    out, n, missing = [], 0, []
    for row in csv.DictReader(pack.open()):
        key = (row["leaf"], str(row["item_id"]))
        if key not in by_key:
            missing.append(row["row_id"])
            continue
        leaf, item = by_key[key]
        out.append(_reading_entry(leaf, item, tasks[leaf["leaf"]], windows.get(key, ""),
                                  urls.get(key, ""), row["row_id"]))
        n += 1
    if missing:
        raise SystemExit(f"{len(missing)} pack rows have no item record ({missing[:5]}); a reading "
                         f"pack missing entries would silently shorten the sitting")
    path = out_dir / "READING_PACK.md"
    path.write_text("\n".join(
        [f"# Blind reading pack -- {n} items", "",
         "One entry per row of `blind_pack.csv`, in the same order and under the same `row_id`.",
         "Answer in the CSV, not here. Neither the stored label nor its validating quote appears",
         "in this file; if you find either, stop, because the reading is no longer blind.", ""]
        + out))
    return path


def write_protocol(info: Dict[str, Any], out_dir: Path, answer_types: Dict[str, str]) -> Path:
    """The protocol a reviewer will ask to see, written so the study is repeatable by someone who
    was not in the room."""
    strata = sorted({(r[1], r[2]) for r in info["rows"]})
    body = [
        "# Annotation agreement protocol (Paper A, step 5a)",
        "",
        "> **Status: PREPARED, NOT RUN.** This document, `sample.csv` and `scoring_sheet.csv` are "
        "ready to execute. **No agreement coefficient exists yet.** Until a second reading is "
        "completed, the paper has no inter- or intra-annotator agreement figure and must not "
        "claim one.",
        "",
        "## Why this exists",
        "",
        "Every oracle label in Probity was produced by a single annotator. At ACL-family venues "
        "an unreported agreement figure on a solo-built dataset is among the most common "
        "rejection causes, independent of how good the labels actually are. This is the cheapest "
        "available fix.",
        "",
        "## Which study to run (strongest available first)",
        "",
        T.md_table(["Option", "What it measures", "Strength", "Cost"], [
            ["1. Second annotator on this sample", "INTER-annotator agreement (Cohen's kappa)",
             "Strongest; what reviewers expect", "One person, one sitting"],
            ["2. Blind re-annotation by the original annotator after a delay",
             "INTRA-annotator agreement", "Real and honest, but weaker -- must be labelled "
             "intra-, never inter-", "No second person needed"],
            ["3. Documented protocol + quote-level provenance only", "Neither",
             "Weakest; a supplement, never the whole answer", "Already done"],
        ]),
        "",
        "Whichever is run, the paper states which option, on what sample, with what result, and "
        "what the exclusion criterion was.",
        "",
        "## The sample",
        "",
        f"- **{info['n_leaves']} leaves** ({100 * info['n_leaves'] / info['n_total_leaves']:.0f}% "
        f"of {info['n_total_leaves']}), **{info['n_items']} items** in total.",
        f"- Stratified by (category x answer type) across **{len(strata)} strata**, fixed seed "
        f"`{SEED}`, so it is reproducible and was not redrawn.",
        "",
        f"> **Deviation from the brief, stated plainly.** The brief asked for a 20% sample "
        f"(~12 leaves). This sample is {info['n_leaves']} leaves "
        f"({100 * info['n_leaves'] / info['n_total_leaves']:.0f}%) because the benchmark has "
        f"{len(strata)} distinct (category x answer type) strata and **every stratum contributes "
        f"at least one leaf** -- at 12 leaves, {len(strata) - 12} strata would be represented by "
        "nothing at all. The small strata are exactly where a lone annotator is most likely to "
        "have drifted, and an agreement figure that never looked at them cannot support a claim "
        "about the benchmark as a whole. If annotator time is the binding constraint, drop leaves "
        "from the LARGEST strata first and report the reduced coverage -- do not drop a stratum "
        "entirely.",
        "- Manifest: `sample.csv`. Answer sheet: `blind_pack.csv`. Reading material: "
        "`READING_PACK.md`. Declared caveats: `primed_items.csv`.",
        "",
        "## Procedure",
        "",
        "1. The annotator receives, per item, ONLY the question and the text the model was shown, "
        "never the existing label. Both are in `READING_PACK.md`, one entry per row of "
        "`blind_pack.csv` under the same `row_id` and in the same (shuffled) order; answers go in "
        "the CSV. An earlier draft pointed at `corpus/questions/`, which does not exist in the "
        "benchmark, and the pack named 154 item ids without saying what to read.",
        "1b. 79 of the 154 items carry no source URL, so for those the stored window IS the "
        "document. Where a window does not settle the question, that is an `undeterminable` "
        "answer and a finding about the corpus, not a gap in the pack.",
        "2. The annotator fills `annotator_answer` using the leaf's declared field type and the "
        "same normalisation the benchmark uses (`engine/normalize.py`), so a disagreement is "
        "never merely a formatting difference.",
        "3. Where the document does not determine an answer, the annotator sets "
        "`undeterminable = 1` and leaves the answer blank. **This is a real outcome, not a "
        "failure** -- see exclusions.",
        "4. Only after all items are complete, join to `oracle.jsonl` on (leaf, item_id) and "
        "compute agreement.",
        "",
        "## Scoring",
        "",
        "- Compare on the **normalised** value, per field type, using `engine/normalize.py` -- "
        "the same canonicalisation the scorer applies, so this measures label agreement and not "
        "string formatting.",
        "- Report **Cohen's kappa** for categorical and binary fields. For numeric fields report "
        "exact-match agreement AND the count of disagreements, since kappa on a continuous field "
        "is not meaningful.",
        "- Report agreement **overall and per answer type**, because the answer types are treated "
        "separately everywhere else in this paper and a single pooled kappa would hide exactly "
        "the contrast the paper is about.",
        "",
        "## Adjudication",
        "",
        "1. Disagreements are resolved by a third reading of the source document by both parties "
        "together, and the resolution is recorded with the clause it rests on.",
        "2. **The adjudicated label does NOT silently replace the oracle.** Any correction is a "
        "separate, listed change; the paper reports agreement on the ORIGINAL labels (that is the "
        "number reviewers want) and notes separately how many corrections adjudication produced.",
        "3. If adjudication changes any label, the affected leaf is re-scored and the effect on "
        "the headline is reported. Silently improving the oracle and re-running is how an "
        "agreement study becomes a way to launder the dataset.",
        "",
        "## Exclusion criterion for undeterminable items",
        "",
        "An item is excluded only if BOTH readers mark it undeterminable, and every exclusion is "
        "reported with its leaf and the reason. A one-sided `undeterminable` is a DISAGREEMENT, "
        "not an exclusion -- dropping it would quietly inflate the agreement figure, which is the "
        "single most common way this study is done wrong.",
        "",
        "**This exclusion can never fire, and saying so is part of the protocol.** Every one of "
        "the 154 items carries an oracle label, so the original reader marked none of them "
        "undeterminable and no item can be undeterminable on BOTH sides. Expect zero exclusions; "
        "every `undeterminable` mark will score as a disagreement. A criterion that cannot "
        "succeed would otherwise be reported as a finding about the corpus.",
        "",
        "## Items whose answer is visible in the notation guide",
        "",
        "Free-text fields document their format by example, and for 4 of the 154 items that "
        "example IS the stored label (`vesting_schedule` x3, `investor_ownership_pct` x1). They "
        "are listed in `primed_items.csv`, generated BEFORE the sitting. Agreement is reported "
        "both with and without them. Removing the examples instead would turn substantive "
        "agreement into orthographic disagreement, which is the worse error.",
        "",
        "## Reporting template",
        "",
        f"> Agreement was assessed on a stratified {100 * SAMPLE_FRACTION:.0f}% sample of the "
        f"benchmark ({info['n_leaves']} of 60 leaves, {info['n_items']} items) by [inter- / "
        "intra-] annotator re-annotation. Cohen's kappa was [K] overall ([K] categorical, [K] "
        "binary); numeric fields agreed exactly on [N] of [M] items. [X] items were excluded as "
        "undeterminable by both readers. Adjudication produced [Y] label corrections, which are "
        "listed in the appendix and [did / did not] change the headline result.",
        "",
    ]
    path = out_dir / "PROTOCOL.md"
    path.write_text("\n".join(body) + "\n")
    return path
