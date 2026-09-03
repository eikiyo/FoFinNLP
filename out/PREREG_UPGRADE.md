# PREREG_UPGRADE.md — thresholds fixed before the probe runs

**Written 2026-07-29T03:29:07Z.** Arm: temperature 0.7 only, legacy unsuffixed namespace.
`config.assert_arm_clean` guards every path opened.

This file is written **before** the EDGAR probe of Block 2a and is **not edited afterwards**.
Its purpose is narrow and specific: a probe yield is a single number, and once it is known there
is always a defensible-sounding reading of it that favours whichever decision was already
preferred. Fixing the rule first is what makes the eventual decision evidence rather than
preference. If any line below is later found to be wrong, the correction goes in a **new**
dated section at the bottom, with the original left standing.

---

## State at the moment of writing (post Block 0, so the thresholds bind against real numbers)

The audit's source-document lookup was repaired in Block 0: it resolved documents by
`<item_id>.txt` while they are stored under company or accession prefixes, so 150 of 470 items
were never opened and their quote-presence check silently did not run.

| Quantity | Before Block 0 | After Block 0 |
|---|---|---|
| Items the audit could open | 320 / 470 | **421 / 470** |
| Flagged items | 46 | **44** |
| Clean items | 424 | **426** |
| Pooled wobble, flagged | 0.226 | **0.2348** [0.2007, 0.2728], n=528 |
| Pooled wobble, clean | 0.0866 | **0.0864** [0.0790, 0.0944], n=5104 |
| Paired difference | 0.140 [0.106, 0.177] | **0.1484** [0.1134, 0.1872] |

Of the 44 flagged items, 42 carry a quote falling outside the window the model is shown. Their
status going into the probe:

- **5** repairable now: quote present in a full document held locally, outside the window.
- **11** not repairable by widening: we hold the full document and the quote is not in it.
- **26** unknown: no local full text, so repairability cannot be determined without a fetch.

## The go/no-go rule

**Run the repair experiment if and only if the probe yields 10 or more repairable items in
total** (the 5 already known plus those the probe converts). At 9 or fewer, the repair
experiment is dropped, the paid re-run is not launched, and Block 2 reduces to reporting the
probe outcome and the unrepairable items.

"Repairable" is defined now, not later: the item's validating quote appears verbatim (under
`oracle_audit.norm`, with `quote_fragments` handling abridged and truncated quotes) in a source
document we can open, **and** it currently falls outside the window shown to the model. An item
whose quote is absent from a document we hold is not repairable and does not count toward the
threshold, however the retrieval turns out.

## The prediction

Re-windowed items will show wobble **closer to the clean-item rate (0.086) than to the flagged
rate (0.235)**. Stated as a falsifiable threshold: the repaired-condition pooled wobble will fall
below the midpoint of those two rates, **0.161**.

The mechanism under test is that an item whose answer is not inside its window cannot be answered
from that window, so the model guesses, and guessing is maximally unstable. If that is the cause,
putting the answer inside the window removes it.

## Commitment to report a failure

If the repaired-condition wobble does **not** fall below 0.161, that is reported in the main text
as a failed prediction, with the observed value and its interval, and the causal claim is
withdrawn. The contamination finding would then stand as correlational only, and §4 says so in
those words. A null here is publishable and is not a reason to reframe the comparison after the
fact, to re-slice the items, or to move the threshold.

Two further commitments, so that a partial result cannot be presented as a whole one:

1. The paired analysis is **within-item and within-model**. Every repaired item contributes its
   own before/after pair; no item enters one condition and not the other.
2. The repair covers only the repairable subset, never all 44 flagged items. Every statement
   about it names the subset size. The 11 items whose quote is absent from a document we hold are
   reported separately as **oracle-provenance failures**, not as windowing failures, and are never
   folded into the windowing count.

## What is NOT pre-registered here

The permutation null, bootstrap, RBO, accuracy-matched and serving-path analyses of Block 1 run
on data already collected and are not gated by any threshold in this file. They are reported in
full whichever way they come out.

---

# CORRECTION 1 — 2026-07-29, written BEFORE the probe was run

Everything above stands as written. Three things in it are wrong or incomplete, and the
corrections are recorded here rather than edited in, so that what was fixed in advance and what
was learned afterwards stay distinguishable.

## 1.1 The state table above mis-transcribes two counts

The line "5 repairable now / 11 not repairable by widening / 26 unknown" carries figures from the
investigation that preceded Block 0, not from the post-Block-0 audit the table claims to describe.
Recomputed from the same audit the table's other rows come from:

| | as written above | actual, post Block 0 |
|---|---|---|
| repairable now | 5 | **10** |
| not repairable by widening | 11 | **6** |
| unknown, no local full text | 26 | 26 (correct) |

**The threshold of 10 is not touched.** Only the inputs it is applied to are corrected. The
parenthetical "(the 5 already known plus those the probe converts)" describes arithmetic over a
wrong figure; the operative rule is and remains the total count of repairable items.

## 1.2 The window check was measuring its own shape on some items

Auditing the rejections rather than the pass rate found that the matcher could not succeed on
certain inputs at all. A validating quote is sometimes a COMPOSITE of several source spans, joined
by an ellipsis, by a pipe, or split by a bracketed editorial interpolation. The old matcher fell
back to testing the raw joined string, which contains a separator that appears in no source
document, so those items were guaranteed to fail. Eight items were flagged for the matcher's
construction rather than for anything about the corpus.

`analysis/quotematch.py` replaces the inline matcher, matches spans rather than the joined string,
returns a specific reason for every rejection, and reports NOT-CHECKABLE separately from ABSENT.
Effect on the partition: **44 flagged / 426 clean becomes 36 flagged / 434 clean.** Every one of
the eight changes is a false rejection cleared; none went the other way. Pooled flagged wobble
rises from 0.2348 to **0.2546** and the difference against clean from 0.1484 to **0.1671**
[0.1275, 0.2109], which is the direction the mechanism predicts when items that were never
defective are removed from the defective group.

## 1.3 The flag conflated two populations, and the repair target is the smaller one

"The validating quote is not in the window" has two causes that need separating:

- **evidence-absent (17 items)** — the window genuinely does not contain what is needed. This is
  the provenance failure the paper is about, and the only population re-windowing can repair.
- **computational (17 items)** — every operand IS in the window and the stored quote is the
  annotator's own derivation, so no verbatim span could exist. All 17 are ownership-percentage
  items whose window supplies both numerator and denominator. Widening these repairs nothing.

Measured separately against the clean rate of 0.0875 [0.0801, 0.0955]:

| group | items | wobble | 95% CI | difference vs clean |
|---|---|---|---|---|
| evidence-absent | 17 | **0.3382** | [0.2768, 0.4056] | +0.2507 [+0.1888, +0.3185] |
| computational | 17 | **0.1863** | [0.1388, 0.2453] | +0.0988 [+0.0507, +0.1583] |
| quote absent from source | 2 | 0.1250 | [0.0434, 0.3100] | +0.0375 [-0.0444, +0.2227] |

Five items have a quote absent from a source document we hold. Three of those five are ALSO
evidence-absent in their window and are counted there, because the groups are built to partition
and an item counted twice would inflate both. The two remaining are items whose window is
self-sufficient even though the label's own citation could not be traced, and they are the row
above. Their interval includes zero, which is a result and not a gap: an untraceable LABEL does
not destabilise a model when the WINDOW still contains the answer. It is reported as a claim
tested and not supported.

This taxonomy was **not pre-registered**. It was found while auditing the flag and is reported as
what it is: an exploratory split, discovered after seeing the data, whose groups were fixed before
any of the three wobble figures above were computed. It is stated here, before the probe, so that
the repair experiment's target is on the record in advance rather than chosen once its result is
known. The repair experiment applies to the evidence-absent group ONLY; a computational item is
not a windowing failure and entering one into the repair would inflate the effect by construction.

## 1.4 The prediction is applied as written, and is now the stricter test

The prediction above fixes 0.161, taken as the midpoint of 0.086 and 0.235. On the corrected
numbers the same midpoint rule would give 0.213. **The threshold is NOT moved to 0.213.** The
repaired-condition wobble must fall below **0.161** as originally written, which is the harder
test of the two, and it is the one that will be reported.

## 1.5 Probe outcome and the threshold decision

The taxonomy shrinks the probe from 26 items to 4: the other 22 are either computational (17,
nothing to fetch) or already resolved locally (5). The 4 are the `liquidation_waterfall_payout`
items, all citing one Connecture fairness-opinion exhibit.

Probed 2026-07-29, one document, read-only public GET: **4 repairable, 0 unrepairable, 0 unknown.**
The values sit in a flattened valuation chart about 8,100 characters into the filing, all four
within one passage. Because both spans are short, presence was additionally required to be
co-located rather than two chance hits in a 64,309-character document.

**Repairable total: 10 held locally + 4 from the probe = 14, against a floor of 10. The threshold
clears and the repair experiment runs.** The scope is the evidence-absent group: 14 repairable of
17, with 3 unrepairable (`participation_type`, quote absent from the document we hold) reported as
oracle-provenance failures and never folded into the windowing count, exactly as committed above.
