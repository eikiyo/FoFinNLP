# ADJUDICATION.md — how the blind re-annotation is run and how disagreements are settled

> STATUS: READY TO RUN · written 2026-07-29 · the sitting has **not** happened

Companion to `PROTOCOL.md` (which defines how an item is answered). This file covers the second
reading: how it is administered blind, and what happens when the two readings differ.

---

## What exists now

| File | What it is |
|---|---|
| `blind_pack.csv` | **The pack the sitting is done on.** 154 rows, one per item, across 19 leaves. Original labels are **absent**. Row order is randomised under a fixed seed (20260729) |
| `sample.csv` | The stratified sample manifest — which leaves, which strata, how many items each |
| `PROTOCOL.md` | How to answer an item, and what counts as undeterminable |
| `scoring_sheet.csv` | The earlier leaf-ordered sheet. Superseded by `blind_pack.csv` for the actual sitting; kept, not deleted |

**Why the order is randomised.** Reading eight items of one clause type in a block lets the second
reading anchor on the first — the second item is answered partly by consistency with the first
rather than from the document. That inflates agreement exactly where the paper needs it to be
honest. Verified on the generated file: consecutive rows share a leaf in **5 of 153** adjacent
pairs in the blind pack, against **135 of 153** in the leaf-ordered sheet. `row_id` is a stable
join key so labels are re-attached afterwards; the leaf name stays visible because the item cannot
be answered without knowing which document it refers to.

---

## Running the sitting

1. Open `blind_pack.csv`. Do **not** open `oracle.jsonl` or any file containing the original
   answers, and do not consult the first reading's notes.
2. For each row, answer from the source document following `PROTOCOL.md`. Fill `annotator_answer`.
3. If the item cannot be determined from the document, put any non-empty mark in `undeterminable`
   and leave `annotator_answer` blank. **Do not guess.** An undeterminable item is a finding, and
   the original protocol excludes rather than guesses such items too.
4. Record `minutes_spent` per row, or per session if per-row is impractical. This is not decorative:
   a reviewer asks what a re-annotation costs, and it is the only evidence for the claim that the
   protocol is operable by someone else.
5. Save as **`blind_pack_filled.csv`** in this directory.
6. Run:

```bash
python3 analysis/agreement.py score
```

That writes `agreement_result.csv` (the disagreement list) and `agreement_result.json` (the
summary). It refuses to report anything if no row carries a second reading — an unfilled sheet
scored naively would compare empty against empty and print a confident κ of 1.0 for a sitting that
never happened.

---

## What is reported, and how

- **Raw agreement** is the primary figure: the proportion of paired items where both readings
  canonicalise to the same value, using the benchmark's own `normalize.canonical`, so `1.0x` and
  `1x` are one reading rather than a disagreement.
- **Cohen's κ is reported per answer-type stratum, and only labelled meaningful where it is.** On
  binary and categorical fields the category space is small and κ behaves as readers expect. On
  free numeric fields nearly every item has a distinct value, expected agreement collapses toward
  zero, and κ converges on the raw agreement rate while implying a rigour it does not have. The
  scorer flags this per stratum (`applicable`) rather than printing one headline κ over
  incompatible fields. **This is a judgement call and it is declared here rather than buried.**
- **Whatever comes back is reported.** A low κ is survivable; an absent κ is not.

## Intra- versus inter-annotator — the honest label

If the second reading is done by **the same person** who produced the original oracle, the result
is **intra-annotator agreement** and must be called that in the paper, in those words. It bounds
transcription and protocol stability, and it says nothing about whether a second qualified reader
would agree. It is the weaker claim and must not be presented as the stronger one.

Only a genuinely independent second reader yields **inter-annotator** agreement. If one is
available in the remaining time, that is materially better and worth the delay.

## The adjudication rule, worked

Disagreements are resolved **after** the agreement figure is computed and reported. The reported κ
is always the pre-adjudication one. Adjudicating first and then reporting agreement would report a
number for a process that did not happen.

For each row in `agreement_result.csv`, in this order:

1. **Protocol-resolvable.** Re-read `PROTOCOL.md`. If it already determines the answer and one
   reading simply failed to apply it, the protocol wins. → correct the oracle, record the reason.
2. **Transcription.** If the two readings agree in substance and differ in form beyond what
   canonicalisation absorbs (units, sign convention, a stated basis), the oracle is corrected to
   the canonical form. → **the protocol is also amended** so the ambiguity cannot recur.
3. **Genuinely ambiguous in the source.** If the document supports both readings, the item is
   **excluded** and the exclusion is reported with its count. It is not resolved by picking the
   original. An item two careful readings answer differently is not a measurement.
4. **Substantive disagreement, protocol silent.** Escalate to Eikiyo, who decides. The decision and
   its reason are recorded in this file.

**Who decides: Eikiyo.** Not the annotator, and not whichever reading came first. Recorded here
because "who adjudicates" is a question reviewers ask and an absent answer looks like the original
label was privileged by default.

## What happens if agreement is poor

No threshold is set in advance for "poor", because a pre-set threshold invites the sample to be
re-cut until it is cleared. Instead the response is fixed by shape:

- **Poor on one stratum** (e.g. multi-part answers): report per stratum, and either exclude that
  stratum from the headline analyses or discuss it explicitly as a bound on those leaves.
- **Poor across the board**: this is a finding about the benchmark and it is reported as one. The
  paper's claims are then bounded by it, and the bound is stated in the abstract, not the appendix.
- **Many undeterminable marks**: the protocol is under-specified. Report the rate and treat it as a
  limitation on item construction.

In every branch the number is published. The one outcome ruled out in advance is not reporting it.
