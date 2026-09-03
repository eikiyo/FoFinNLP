# STAGE3_REPORT.md - Paper A stage 3

> STATUS: DONE - steps 1a-1d, 2 (pre-registration only), 3, 4 - run 2026-07-29

Arm: **legacy (temperature 0.7)**. No number here derives from the 0.1 arm or any cross-arm comparison. Regenerate everything with `python3 analysis/run_all.py`.

**Step 0 (the novelty gate) ran first and cleared.** Neither trigger condition fired; the full audit, with 27 verified records, is `out/novelty_audit.md`. Read it before this file - it changes what the numbers below are allowed to be used for.

**Controls that gate this run** (it aborts rather than produce partial output if any fail):

- `conservative selftest PASS - floor excludes small categories, conservative < point, flat data collapses to 1, degenerate input returns None`
- `fold selftest PASS - both structural bounds correct at p=0/0.5/1, lower bound symmetric and dominated by the upper, n=1 is a real zero, n=0 refused`
- `folddiag selftest PASS - detects a real fold, refuses a flat one, deciles partition exactly, empty decile returns None, residual vanishes on structural data`
- `fold round-trip PASS - per-item flags reproduce all 720 published wobble cells exactly, so p is joined to the right oracle field`

That last one is the load-bearing control for everything in step 1b/1c: the per-item reconstruction is only trustworthy because it reproduces all 720 published wobble cells exactly. It failed on its first run (two cells), which is how a real defect was found - the benchmark keys measurability on the MINIMUM valid-run count across every scorable field, so an item whose target field has plenty of runs is still excluded when a sibling field recorded none. Using the target field alone had inflated two cells' wobble.

---

## Step 1a - Conservative worst-category ratios

Every ratio below is built from the same two Wilson bounds, so they are directly comparable. `conservative` is the **selection-robust** form: the largest Wilson LOWER bound over that model's estimable categories, divided by the Wilson UPPER bound of its mean. Taking the point-estimate winner and then quoting its lower bound is exposed to the winner's curse - the category that looks worst is partly the one that got lucky - so that variant is reported beside it, never as the headline. `excl worst` removes the worst category's own items from the mean's denominator, because otherwise the worst category sits inside the quantity it is being compared against.

| model | mean | mean 95% CI | worst category (point) | worst rate | worst 95% CI | 2nd worst | point ratio | **conservative** | excl worst |
|---|---|---|---|---|---|---|---|---|---|
| gemma3-1b | 0.4243 | 0.3804-0.4695 | cap_table | 0.9697 | 0.8468-0.9946 | exit_waterfall 0.7500 | 2.29x | **1.80x** | 1.97x |
| deepseek-v4f | 0.0574 | 0.0398-0.0823 | regulatory | 0.1481 | 0.0592-0.3248 | exit_waterfall 0.1250 | 2.58x | **0.72x** | 0.77x |
| deepseek-v4p | 0.0448 | 0.0295-0.0675 | exit_waterfall | 0.1250 | 0.0224-0.4709 | convertibles 0.0745 | 2.79x | **0.54x** | 0.55x |
| gemma4-31b-or | 0.0299 | 0.0179-0.0495 | exit_waterfall | 0.5000 | 0.2152-0.7848 | cap_table 0.1212 | 16.75x | **4.35x** | 5.45x |
| mistral-large-or | 0.0319 | 0.0194-0.0520 | exit_waterfall | 0.2500 | 0.0715-0.5907 | regulatory 0.0741 | 7.83x | **1.38x** | 1.50x |
| minimax-m2.5-or | 0.0745 | 0.0540-0.1018 | exit_waterfall | 0.3750 | 0.1368-0.6943 | regulatory 0.2963 | 5.04x | **1.56x** | 1.65x |
| llama3.3-70b-or | 0.0320 | 0.0195-0.0521 | exit_waterfall | 0.3750 | 0.1368-0.6943 | cap_table 0.0909 | 11.72x | **2.63x** | 3.04x |
| gemma3-1b-qat | 0.3383 | 0.2970-0.3822 | exit_waterfall | 0.7500 | 0.4093-0.9285 | cap_table 0.6970 | 2.22x | **1.38x** | 1.40x |
| gemini3-flash-or | 0.0256 | 0.0147-0.0442 | exit_waterfall | 0.1250 | 0.0224-0.4709 | cap_table 0.0606 | 4.89x | **0.51x** | 0.53x |
| haiku-4.5-direct | 0.0278 | 0.0163-0.0469 | exit_waterfall | 0.5000 | 0.2152-0.7848 | cap_table 0.0909 | 18.00x | **4.58x** | 5.85x |
| gpt-oss-120b-or | 0.0618 | 0.0434-0.0874 | exit_waterfall | 0.2500 | 0.0715-0.5907 | cap_table 0.1515 | 4.04x | **0.82x** | 0.85x |
| gpt5-mini-or | 0.0553 | 0.0380-0.0798 | exit_waterfall | 0.5000 | 0.2152-0.7848 | regulatory 0.1481 | 9.04x | **2.70x** | 3.03x |

### Sensitivity: a stricter 5-leaf floor

| floor | median point ratio | median conservative ratio | models > 2x (point) | models > 2x (conservative) |
|---|---|---|---|---|
| 3 leaves | 4.96 | 1.47 | 12/12 | 4/12 |
| 5 leaves | 2.51 | 0.74 | 11/12 | 0/12 |

Models still above 2x conservatively (3-leaf floor): gemma4-31b-or, llama3.3-70b-or, haiku-4.5-direct, gpt5-mini-or.

**What this decides.** The spine does not survive in its current form.

At the estimability floor the benchmark already uses (3 leaves), the median worst-to-mean ratio falls from **4.96x** on point estimates to **1.47x** at the bounds, and the number of models clearing 2x falls from **12/12** to **4/12**.

At a 5-leaf floor it collapses completely: median **0.74x** - below 1 - and **0/12** models clear 2x. The reason is not subtle. `exit_waterfall` has 3 leaves and is the worst category for most models; raising the floor removes it, and with it the entire effect. The paper's headline currently rests on a single 3-leaf category.

So the sentence *"a model's headline wobble understates its worst clause type by a median of 4.96x"* cannot be written. What the data supports is weaker and must be stated at the bound: for 4 of 12 models, the worst estimable clause type is at least twice the headline even after both numbers are read as pessimistically as the intervals permit. For the rest, the intervals are too wide to assert it.

---

## Step 1b - The wobble-accuracy fold test

Stage 2 reported Spearman(leaf wobble, leaf accuracy) = -0.5516 over 60 leaves and flagged that part of it must be mechanical, since both are computed from the same runs. This decomposes it.

### Is it folded?

Fitting wobble ~ accuracy + accuracy^2 gives a quadratic term of 1.740 (0.844 to 2.636). That is POSITIVE - convex - where a fold would be negative. **Not folded.**

But that verdict is bounded by coverage, and the bound matters: leaf accuracy in this corpus runs only from 0.444 to 1.000. The fold's left arm - the low-accuracy region where wobble should fall again - is barely sampled. Run on the structural prediction itself the quadratic is 0.542 (-0.020 to 1.103), which also does not fold over this range. So the honest statement is that the fold is not observable here, not that it was tested and refuted.

### How much of the correlation is mechanical?

The two structural models differ only on items the model gets ALWAYS WRONG: one says a wrong model is wrong the same way every run, the other says it is wrong a different way each run. That is measurable rather than assumable, and measuring it is what fixes the answer:

| items | n | flipped | observed flip rate | lower bound predicts | upper bound predicts |
|---|---|---|---|---|---|
| p=0 (always wrong) | 503 | 129 | 0.2565 | 0.00 | 1.00 |
| 0<p<1 (mixed) | 436 | 436 | 1.0000 | - | - |
| p=1 (always right) | 4693 | 0 | 0.0000 | 0.00 | 0.00 |

Only the first row carries information. The other two are definitional - an item with a mix of right and wrong runs has by definition produced two different answers and so has flipped, and an item answered correctly every time cannot have. They are reported anyway because they are a genuine control: had either deviated, the join would be broken.

Among the 503 always-wrong items, 129 flip - **0.2565**. Reality sits about a quarter of the way from the lower bound to the upper. Models that are wrong are usually wrong the same way, but not always.

| structural model | what it assumes about wrong runs | rho(structural, accuracy) | rho(residual, accuracy) |
|---|---|---|---|
| lower bound | all wrong runs give the SAME answer | -0.3114 | -0.4990 |
| **calibrated (primary)** | measured: always-wrong items flip at the corpus rate, estimated leave-one-leaf-out | **-0.5917** | **0.0875** |
| upper bound | every wrong run gives a DIFFERENT answer | -0.9302 | 0.6049 |

**What this decides. Concede. The difficulty objection lands, and the paper must stop using this correlation as evidence.**

Under the calibrated model the structural component alone tracks accuracy at -0.5917 - slightly MORE negative than the observed -0.5516 - and the residual is 0.0875, which is nothing. Essentially none of the correlation survives once each leaf's distribution of per-item correct rates is known.

The one honest qualification, stated because it cuts against this conclusion: the calibrated model contains a definitional component (interior-p items have flipped by construction), so this decomposition is closer to an identity than to an independent test. The parameter-free lower-bound model, which has no definitional component at all, leaves -0.4990 of the -0.5516 intact. The gap between those two answers IS the definitional part.

Either way the paper's position is the same, and it is the conservative one: leaf wobble and leaf accuracy are two summaries of the same per-item outcome distribution, so their correlation is not evidence for anything and should not be presented as if it were. Drop it from the results and state the relationship as a limitation. The category-level comparison is a different question and is unaffected by this - but it now has to carry the paper alone.

---

## Step 1c - Why is the empty zone empty?

Stage 2 found zero leaves at accuracy >= 0.9 and wobble >= 0.3, and refused to move the threshold. Two explanations were available and they are opposite sentences: models never produce silently-unstable-but-correct clauses, or this item pool cannot express one.

### The pooled per-item correct rate

| quantity | value |
|---|---|
| items pooled over all 12 models x 60 leaves | 5,632 |
| mean per-item correct rate | 0.8781 |
| share at exactly p = 1 | 83.3% |
| share at exactly p = 0 | 8.9% |
| share strictly between | 7.7% |
| share in the mid band 0.3 <= p <= 0.7 | 2.0% |

**Strongly bimodal.** Five sixths of all measurements are items the model answers correctly on every single run. Only one item in fifty sits anywhere near the middle, which is the only region where an item can flip while staying mostly correct.

### The empirical frontier, by accuracy decile

| accuracy decile | leaves | max observed wobble | max structurally reachable |
|---|---|---|---|
| 0.0-0.1 | 0 | — | — |
| 0.1-0.2 | 0 | — | — |
| 0.2-0.3 | 0 | — | — |
| 0.3-0.4 | 0 | — | — |
| 0.4-0.5 | 1 | 0.6111 | 0.1835 |
| 0.5-0.6 | 1 | 0.6667 | 0.3075 |
| 0.6-0.7 | 3 | 0.1944 | 0.1106 |
| 0.7-0.8 | 3 | 0.2593 | 0.1958 |
| 0.8-0.9 | 17 | 0.3333 | 0.1755 |
| 0.9-1.0 | 35 | 0.1667 | 0.1154 |

**What this decides. It is a fact about the item pool, not about models.**

Of the 35 leaves at accuracy >= 0.9, the most unstable reaches 0.1667 wobble - and the most that the structure of those leaves' items could produce is 0.1154, against a threshold of 0.3. The region was unreachable before any model was run. The paper must therefore write the limitation sentence, not the finding sentence: *we did not observe clauses that models answer correctly yet unstably, and our item pool could not have contained them at this threshold.*

One nuance worth keeping, because it points at where such items would be found: at high accuracy the observed maximum (0.1667) EXCEEDS the structural maximum (0.1154). Real instability above the mechanical floor does exist there. It is simply an order of magnitude smaller than the threshold stage 2 fixed in advance. That is the direct motivation for the prospective test in `out/PREREG_2a.md`, and it is why that test is worth running at all.

---

## Step 1d - Does the ratio really grow with capability?

The stage-2 evidence for *"the gap grows as models improve"* was a correlation between mean wobble and a ratio that has mean wobble in its denominator. This restates it with no shared term: regress worst-category wobble directly on mean wobble. A slope BELOW 1 would mean the worst category falls more slowly than the mean, which is the claim.

| outcome | model set | n | slope | slope 95% CI | intercept | intercept 95% CI | R2 |
|---|---|---|---|---|---|---|---|
| point_rate | all 12 models | 12 | 1.604 | 0.926 to 2.281 | 0.2448 | 0.1348 to 0.3548 | 0.683 |
| point_rate | frontier only | 10 | -0.636 | -6.912 to 5.641 | 0.3428 | 0.0478 to 0.6379 | 0.005 |
| robust_lo | all 12 models | 12 | 1.695 | 1.305 to 2.084 | 0.0446 | -0.0187 to 0.1079 | 0.879 |
| robust_lo | frontier only | 10 | -0.078 | -3.203 to 3.046 | 0.1237 | -0.0232 to 0.2705 | 0.000 |

### The absolute numbers, which the paper must quote beside every ratio

| model (3 most stable) | mean wobble | worst category | worst wobble | worst 95% CI | ratio |
|---|---|---|---|---|---|
| gemini3-flash-or | 0.0256 | exit_waterfall | 0.1250 | 0.0224-0.4709 | 4.89x |
| haiku-4.5-direct | 0.0278 | exit_waterfall | 0.5000 | 0.2152-0.7848 | 18.00x |
| gemma4-31b-or | 0.0299 | exit_waterfall | 0.5000 | 0.2152-0.7848 | 16.75x |

A 5x between 2.5% and 12.5% reads nothing like a 5x between 10% and 50%, and a reviewer outside the project will ask which one it is. For the three most stable models it is the former: headline wobble of 2.6-3.0%, worst-category wobble of 12.5-50%, on categories of 3 leaves whose intervals run from roughly 0.02 to 0.78. Those intervals are the finding as much as the point estimates are.

**What this decides. The claim is not supported, and the stage-2 version of it was an artefact of two models.**

Across all 12 models the slope is 1.60 (0.93 to 2.28) - above 1, not below it, so worst-category wobble falls FASTER in absolute terms than the mean does, which is the opposite of the hypothesis. The ratio nevertheless grows as models improve, and the table shows why: the intercept is 0.245 (0.135 to 0.355), safely above zero, so as mean wobble goes to zero the ratio goes to infinity by arithmetic. A ratio driven by a positive intercept is a different sentence from "the worst category resists improvement".

And on the pre-registered frontier split - the 10 models excluding the two 1B ones - the relationship disappears entirely: slope -0.64 (-6.91 to 5.64), R2 = 0.005. The whole association across 12 models is carried by two low-tier models sitting an order of magnitude away from the other ten. Among the models anyone would actually deploy, worst-category wobble is unrelated to headline wobble.

This is not a weaker version of the claim. It is the absence of the claim, and it was found only because the regression was run on a pre-registered subset rather than on all twelve points at once.

---

## Step 2 - The prospective test (pre-registration only; NOTHING was run)

No new runs were launched and no new leaves were built. The hypothesis, the design, the cost estimate and BOTH committed outcomes are written down in advance in `out/PREREG_2a.md`, which is timestamped before any call is made. Launching it needs explicit approval, and the 2026-08-02 sourcing deadline in the brief still governs.

Step 1c changed what this test is for. The empty zone is unreachable in the current item pool by construction, so a deliberate attempt to construct items inside it is no longer a nice-to-have example hunt - it is the only way to tell an item-pool limitation from a claim about models, and the pre-registration says so.

## Step 3 - Annotation agreement

**Prepared, NOT RUN - and it is still the single blocking item.** The blind pack is now built and the scorer is written, so the remaining work is a sitting, not a project:

- `out/annotation/blind_pack.csv` - one row per item, original label withheld, order randomised under a fixed seed so the second reading cannot anchor on a run of items from one clause type.
- `out/annotation/ADJUDICATION.md` - the protocol, the worked adjudication rule, and who decides.
- `python3 analysis/agreement.py score` - the one command. It joins the withheld labels back by `row_id`, reports raw agreement and Cohen's kappa per answer-type stratum, and writes the disagreement list.

The scorer refuses to report a number on an unfilled sheet rather than scoring empty against empty and printing a confident kappa of 1.0. Whatever comes back is reported; a low kappa is survivable and an absent one is not. If the second reading is by the same person it is reported as INTRA-annotator agreement, which is a weaker claim, and the paper must say so in those words.

## Step 4 - Scope lock

`out/SCOPE.md` carries the page allocation and the kill list. It was rewritten after these results rather than before: two of the three results sections the brief proposed no longer have a result to carry, so an allocation written in advance would have budgeted pages to findings that did not survive.

---

## What stage 3 leaves the paper able to claim

| claim the paper wanted | status after stage 3 | what survives |
|---|---|---|
| worst clause type is ~5x the headline | **not supported at the bound** | median conservative ratio 1.47x; 4/12 models above 2x |
| the gap grows as models improve | **not supported** | absent among the 10 frontier models (R2 = 0.005) |
| instability is not just difficulty | **conceded** | residual rho 0.087 under the calibrated model |
| silently-unstable-but-correct clauses do not exist | **restated as a limitation** | unreachable by construction: structural max 0.115 vs threshold 0.3 |
| the instrument is stable | **holds** (stage 2) | median split-half r_full 0.8970, unaffected by anything here |
| clause-level instability is measurable in this domain | **holds** | 720 cells, 14,400 model-item measurements, round-trip verified |

Three of the four load-bearing claims did not survive contact with a conservative reading. That is an uncomfortable result to report thirteen days out, and it is the correct one: every one of them would have been found by a reviewer instead, and two of them (the frontier-only regression, the structural decomposition) are exactly the checks a competent referee runs first.

What remains is narrower and defensible: a benchmark and an instrument for clause-level answer instability in venture-financing documents, calibrated against its own measurement ceiling, showing that instability concentrates in identifiable clause types - reported with intervals wide enough that the honest headline is the concentration itself, not a multiplier. Whether that is enough for eight pages at FinNLP is a judgement for Eikiyo, and `out/SCOPE.md` sets out what it looks like if the answer is yes.

