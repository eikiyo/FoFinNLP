# Annotation agreement protocol (Paper A, step 5a)

> **Status: PREPARED, NOT RUN.** This document, `sample.csv` and `scoring_sheet.csv` are ready to execute. **No agreement coefficient exists yet.** Until a second reading is completed, the paper has no inter- or intra-annotator agreement figure and must not claim one.

## Why this exists

Every oracle label in Probity was produced by a single annotator. At ACL-family venues an unreported agreement figure on a solo-built dataset is among the most common rejection causes, independent of how good the labels actually are. This is the cheapest available fix.

## Which study to run (strongest available first)

| Option | What it measures | Strength | Cost |
|---|---|---|---|
| 1. Second annotator on this sample | INTER-annotator agreement (Cohen's kappa) | Strongest; what reviewers expect | One person, one sitting |
| 2. Blind re-annotation by the original annotator after a delay | INTRA-annotator agreement | Real and honest, but weaker -- must be labelled intra-, never inter- | No second person needed |
| 3. Documented protocol + quote-level provenance only | Neither | Weakest; a supplement, never the whole answer | Already done |

Whichever is run, the paper states which option, on what sample, with what result, and what the exclusion criterion was.

## The sample

- **19 leaves** (32% of 60), **154 items** in total.
- Stratified by (category x answer type) across **19 strata**, fixed seed `20260729`, so it is reproducible and was not redrawn.

> **Deviation from the brief, stated plainly.** The brief asked for a 20% sample (~12 leaves). This sample is 19 leaves (32%) because the benchmark has 19 distinct (category x answer type) strata and **every stratum contributes at least one leaf** -- at 12 leaves, 7 strata would be represented by nothing at all. The small strata are exactly where a lone annotator is most likely to have drifted, and an agreement figure that never looked at them cannot support a claim about the benchmark as a whole. If annotator time is the binding constraint, drop leaves from the LARGEST strata first and report the reduced coverage -- do not drop a stratum entirely.
- Manifest: `sample.csv`. Answer sheet: `blind_pack.csv`. Reading material: `READING_PACK.md`. Declared caveats: `primed_items.csv`.

## Procedure

1. The annotator receives, per item, ONLY the question and the text the model was shown, never the existing label. Both are in `READING_PACK.md`, one entry per row of `blind_pack.csv` under the same `row_id` and in the same (shuffled) order; answers go in the CSV. An earlier draft pointed at `corpus/questions/`, which does not exist in the benchmark, and the pack named 154 item ids without saying what to read.
1b. 79 of the 154 items carry no source URL, so for those the stored window IS the document. Where a window does not settle the question, that is an `undeterminable` answer and a finding about the corpus, not a gap in the pack.
2. The annotator fills `annotator_answer` using the leaf's declared field type and the same normalisation the benchmark uses (`engine/normalize.py`), so a disagreement is never merely a formatting difference.
3. Where the document does not determine an answer, the annotator sets `undeterminable = 1` and leaves the answer blank. **This is a real outcome, not a failure** -- see exclusions.
4. Only after all items are complete, join to `oracle.jsonl` on (leaf, item_id) and compute agreement.

## Scoring

- Compare on the **normalised** value, per field type, using `engine/normalize.py` -- the same canonicalisation the scorer applies, so this measures label agreement and not string formatting.
- Report **Cohen's kappa** for categorical and binary fields. For numeric fields report exact-match agreement AND the count of disagreements, since kappa on a continuous field is not meaningful.
- Report agreement **overall and per answer type**, because the answer types are treated separately everywhere else in this paper and a single pooled kappa would hide exactly the contrast the paper is about.

## Adjudication

1. Disagreements are resolved by a third reading of the source document by both parties together, and the resolution is recorded with the clause it rests on.
2. **The adjudicated label does NOT silently replace the oracle.** Any correction is a separate, listed change; the paper reports agreement on the ORIGINAL labels (that is the number reviewers want) and notes separately how many corrections adjudication produced.
3. If adjudication changes any label, the affected leaf is re-scored and the effect on the headline is reported. Silently improving the oracle and re-running is how an agreement study becomes a way to launder the dataset.

## Exclusion criterion for undeterminable items

An item is excluded only if BOTH readers mark it undeterminable, and every exclusion is reported with its leaf and the reason. A one-sided `undeterminable` is a DISAGREEMENT, not an exclusion -- dropping it would quietly inflate the agreement figure, which is the single most common way this study is done wrong.

**This exclusion can never fire, and saying so is part of the protocol.** Every one of the 154 items carries an oracle label, so the original reader marked none of them undeterminable and no item can be undeterminable on BOTH sides. Expect zero exclusions; every `undeterminable` mark will score as a disagreement. A criterion that cannot succeed would otherwise be reported as a finding about the corpus.

## Items whose answer is visible in the notation guide

Free-text fields document their format by example, and for 4 of the 154 items that example IS the stored label (`vesting_schedule` x3, `investor_ownership_pct` x1). They are listed in `primed_items.csv`, generated BEFORE the sitting. Agreement is reported both with and without them. Removing the examples instead would turn substantive agreement into orthographic disagreement, which is the worse error.

## Reporting template

> Agreement was assessed on a stratified 20% sample of the benchmark (19 of 60 leaves, 154 items) by [inter- / intra-] annotator re-annotation. Cohen's kappa was [K] overall ([K] categorical, [K] binary); numeric fields agreed exactly on [N] of [M] items. [X] items were excluded as undeterminable by both readers. Adjudication produced [Y] label corrections, which are listed in the appendix and [did / did not] change the headline result.

