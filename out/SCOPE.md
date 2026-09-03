# SCOPE.md — what the 8 pages carry

> STATUS: **ACCEPTED by Eikiyo 2026-07-29** · FinNLP 2026, 8 pages excluding references, deadline 2026-08-11
>
> Both decisions taken: the **resource-and-measurement framing** below is the paper we are writing,
> and **2a is approved to proceed** (mining underway; see `out/prereg2a/`). The allocation in this
> file is therefore live, not proposed — with the one contingency already noted in §"What is still
> missing": if 2a lands, ~0.5 pages move from §4 to §6.

Written **after** steps 0–1 rather than before them, deliberately. The brief's proposed allocation
budgeted 2 pages to "worst vs mean" and 1 to "mechanism". Step 1a weakened the first and steps
1b/1d removed the second. An allocation written in advance would have reserved three of eight pages
for findings that did not survive.

---

## First, the honest question: is there a paper?

Three of four load-bearing claims did not survive stage 3.

- The 4.96× worst-to-mean ratio is **1.47×** at the bounds, and **below 1** if the estimability
  floor rises from 3 leaves to 5.
- "The gap grows as models improve" is **absent** among the 10 frontier models (R² = 0.005); the
  whole association came from two 1B models.
- The wobble–accuracy correlation is **conceded** as mechanical.

**My assessment: yes, there is a paper, but it is a different one — a resource-and-measurement
paper, not a finding paper.** What survives is a benchmark of venture-financing documents that no
one else has built (novelty audit Q3), an instability axis applied to it, a measured instrument
ceiling, and a demonstration that instability concentrates in identifiable clause types with
intervals honestly stated. FinNLP explicitly solicits *datasets, benchmarks and evaluations*. A
resource paper that reports its own null results credibly is a normal, acceptable FinNLP
contribution. A finding paper resting on 1.47× would not survive review.

The risk is the opposite of the one we started with. It is no longer "will a reviewer catch the
weakness" — the weaknesses are now in the paper on purpose. It is "is the residual contribution
large enough for eight pages", and that is Eikiyo's call. The allocation below assumes yes.

---

## Proposed allocation

| § | Section | Pages | Carries |
|---|---|---|---|
| 1 | Intro | 1.0 | The domain argument: an answer that flips changes who owns what. The contribution stated as resource + measurement, not as discovery |
| 2 | Related work | 1.0 | **The positioning from the novelty audit.** Instability-as-an-axis (Atil 2025; Song 2025; ReasonBENCH) taken as given. Yagubyan (2026) distinguished explicitly — judge verdicts vs substantive answers. ContractEval distinguished — per-clause *correctness*, single run. Cacioli distinguished — version change vs within-model instability |
| 3 | Benchmark and method | 1.5 | The corpus, the oracle protocol, **the annotation agreement figure**, the wobble definition, the 12-model lineup, the measurement ceiling in one sentence |
| 4 | Result 1: clause-level concentration | 1.75 | The conservative ratio table, absolute numbers beside every ratio, the model × category figure with n per cell, and the 3-leaf estimability problem stated in the text rather than the appendix |
| 5 | Result 2: transfer | 1.25 | 50% vs 23% chance at k=10, 60% vs 18% at k=5, frontier-only, **with the truncation caveat and median effective k in the same table** |
| 6 | What instability is *not* | 0.75 | The two concessions as results: wobble is predicted by the per-item correct rate, and the high-accuracy/high-wobble region was unreachable by construction. Written as findings about measurement, because that is what they are |
| 7 | Recommendation + conclusion | 0.75 | The reporting standard, concrete enough to adopt, positioned against Atil's max–min recommendation rather than as a new idea |
| — | Limitations | free | Ceiling, single arm, single annotator, serving layer, 3-leaf categories, item-pool bounds, the frontier-only null |
| | **Total** | **8.0** | |

Changes from the brief's proposal, with reasons:

- **Related work up from 1.75 shared with intro to 1.0 standalone.** The audit found a direct
  precedent for the paper's headline construct. Positioning is now the single largest rejection
  risk, and it cannot be done in three sentences.
- **Method up from 1.25 to 1.5.** The benchmark is now the contribution, so it gets the space. The
  annotation agreement figure lands here.
- **Result 1 down from 2.0 to 1.75.** A weaker claim needs fewer pages, not more.
- **Result 2 up from 1.0 to 1.25.** It is now one of only two surviving positive results.
- **"Result 3: mechanism" (1.0) replaced by "What instability is not" (0.75).** There is no
  mechanism result. There are two well-evidenced concessions, and they are worth publishing.

---

## Kill list

Killed, agreeing with the brief:

| Analysis | Treatment | Why |
|---|---|---|
| Full split-half reliability table | One sentence + number, cite Cacioli (2026), table to appendix | Novelty audit Q4: psychometric reliability on LLM evaluation is **precedented**. It is a control, not a contribution |
| Leave-one-out over models | One sentence | Confirms nothing moved |
| Weighting sensitivity | One sentence | Confirms the ordering is not an artefact of item- vs leaf-weighting |
| 66-pair ρ distribution figure | Killed; the median and IQR suffice | A figure that says what one number says |

Killed, **added** by stage 3 because the result changed:

| Analysis | Treatment | Why |
|---|---|---|
| Wobble–accuracy correlation as a *result* | Moved to §6 and to limitations | Step 1b: the residual under the calibrated model is +0.09. It is not evidence of anything |
| "The gap grows as models improve" | **Cut entirely** | Step 1d: absent among frontier models (R² = 0.005). Two low-tier models carried it |
| The 4.96× headline figure | Replaced by the conservative table | Step 1a. The point estimate cannot be the headline |
| Nightmare-leaf count as a finding | Restated as a limitation in §6 | Step 1c: unreachable by construction |

**Defended against the brief — one disagreement.** The brief proposed killing the stage-1
answer-type strata to a single sentence, on the grounds that stage 2 showed category dominates for
the level question. That was right when it was written and is now wrong. Step 1c shows answer type
governs **where items sit in the p distribution**, which is the mechanism behind the item-pool
bound in §6 — the reason 83.3% of measurements sit at p = 1 is that most items are single-lookup
binary or numeric reads. It needs **two sentences in §6**, not zero, or the limitation has no
explanation and reads as an excuse. Still killed as a standalone results subsection.

Every killed analysis still ships in the public artefact (`out/tables/`, `out/STAGE2_REPORT.md`,
`out/STAGE3_REPORT.md`). Killing means it does not consume a page, not that it disappears.

---

## What is still missing before drafting

1. **The annotation agreement figure.** Blind pack and scorer are ready; the sitting has not
   happened. It is one number and it blocks §3.
2. **The 2a decision.** If it runs and lands, §6 becomes a positive result and the allocation
   shifts ~0.5 pages from §4 to §6. If it does not run by 2026-08-02, §6 stands as written.
3. **Eikiyo's call on the framing** — resource-and-measurement paper, per the top of this file.
