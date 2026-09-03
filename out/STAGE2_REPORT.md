# STAGE 2 REPORT - Paper A: ceiling, transfer, description, and the two attacks

**Arm:** legacy (temperature 0.7) only. Probity `v1.3.1`, read from disk. No number here derives from the 0.1 arm or from any cross-arm comparison.

Continues the C2 diagnostic (`out/C2_REPORT.md`), which returned Row 1. Pre-registration for this stage: `DESIGN-stage2.md`, written before any stage-2 coefficient was computed. Regenerate everything: `python3 analysis/run_all.py`.

---

## Step 1 - The measurement ceiling (run first, reported first)

**Computed.** Each cell's 20 runs were split by `run_idx % 2` into two independent halves of 10, and the whole wobble matrix was recomputed twice **through the benchmark's own scorer** (`engine/scorer.py`), not through a re-derived flip rule. Each model's half-A leaf vector was then correlated against its half-B vector over the active subset (57 leaves).

> **Positive control:** round-trip PASS - the engine's scorer over raw runs reproduces all 720 published cells exactly. The raw-runs route is therefore the same measurement as the published matrix, not a parallel re-implementation of it. Without this check the half matrices would prove nothing.

Odd/even was chosen over first-half/second-half because it is **interleaved**: any drift across the run sequence (throttling, cache warming, provider degradation) is balanced between the halves instead of concentrated in one.

| Model | leaves | wobble A | wobble B | wobble full | r_half | r_full (S-B) | tie A | tie B |
|---|---|---|---|---|---|---|---|---|
| `gemma3-1b` | 57 | 0.3706 | 0.4063 | 0.4650 | 0.7259 | 0.8412 | 0.684 | 0.789 |
| `deepseek-v4f` | 57 | 0.0463 | 0.0455 | 0.0598 | 0.7707 | 0.8705 | 0.912 | 0.912 |
| `deepseek-v4p` | 57 | 0.0393 | 0.0318 | 0.0472 | 0.7000 | 0.8236 | 0.860 | 0.860 |
| `gemma4-31b-or` | 57 | 0.0384 | 0.0418 | 0.0462 | 0.9994 | 0.9997 | 0.912 | 0.877 |
| `mistral-large-or` | 57 | 0.0383 | 0.0359 | 0.0442 | 0.8597 | 0.9246 | 0.895 | 0.895 |
| `minimax-m2.5-or` | 56 | 0.0852 | 0.0637 | 0.1065 | 0.8211 | 0.9017 | 0.911 | 0.860 |
| `llama3.3-70b-or` | 57 | 0.0436 | 0.0405 | 0.0519 | 0.9301 | 0.9638 | 0.965 | 0.895 |
| `gemma3-1b-qat` | 57 | 0.3537 | 0.3665 | 0.4136 | 0.8055 | 0.8923 | 0.807 | 0.789 |
| `gemini3-flash-or` | 57 | 0.0311 | 0.0293 | 0.0372 | 0.7112 | 0.8312 | 0.912 | 0.877 |
| `haiku-4.5-direct` | 57 | 0.0349 | 0.0427 | 0.0427 | 0.8592 | 0.9243 | 0.877 | 0.912 |
| `gpt-oss-120b-or` | 57 | 0.0512 | 0.0673 | 0.0827 | 0.6343 | 0.7762 | 0.842 | 0.842 |
| `gpt5-mini-or` | 57 | 0.0618 | 0.0538 | 0.0681 | 0.8770 | 0.9345 | 0.860 | 0.895 |

- **Median r_half = 0.8133**, **median r_full (Spearman-Brown) = 0.8970** (n = 12 models).
- Half-length wobble is systematically LOWER than full-length wobble in every model. That is expected, not a defect: with half the runs there are half as many chances to observe a flip. Reliability is a RANK correlation, so a uniform level shift does not affect it, and Spearman-Brown is precisely the correction for the halved LENGTH.
- Tie-preserving permutation null on the split-half correlations: median -0.0087, 97.5th 0.0863.

**Declared addition (not pre-registered).** A single odd/even split is one draw from the distribution of possible partitions. Prompted by finding Cacioli (2026), which averages 1,000 random splits, the procedure was re-run over 40 random partitions: median r_full **0.8992**, 95% spread [0.8836, 0.9249]. The pre-registered odd/even value sits inside that spread, so it was representative rather than a lucky partition.

**Declared sensitivity.** The headline reliability is partly the instrument re-finding the same *zeros*. The harder question is whether it can RANK the leaves that actually move, so reliability was recomputed on each model's OWN non-zero leaves only. This can only weaken the ceiling claim, which is why it is reported:

| Model | non-zero leaves | r_half | r_full | note |
|---|---|---|---|---|
| `gemma3-1b` | 52 | 0.6648 | 0.7987 |  |
| `deepseek-v4f` | 18 | 0.5042 | 0.6704 |  |
| `deepseek-v4p` | 15 | 0.3655 | 0.5353 |  |
| `gemma4-31b-or` | 7 | 0.8829 | 0.9378 |  |
| `mistral-large-or` | 12 | 0.3381 | 0.5053 |  |
| `minimax-m2.5-or` | 18 | 0.8195 | 0.9008 |  |
| `llama3.3-70b-or` | 9 | 0.6783 | 0.8083 |  |
| `gemma3-1b-qat` | 50 | 0.7464 | 0.8548 |  |
| `gemini3-flash-or` | 11 | 0.0391 | 0.0752 |  |
| `haiku-4.5-direct` | 9 | 0.5570 | 0.7155 |  |
| `gpt-oss-120b-or` | 20 | 0.1375 | 0.2417 |  |
| `gpt5-mini-or` | 14 | 0.7122 | 0.8319 |  |

### What step 1 decides

| Quantity | Value |
|---|---|
| median r_full (pre-registered primary) | 0.8970 |
| decision-table row | **high** (cuts at 0.40 and 0.70) |
| observed median rho | 0.2964 |
| disattenuated median rho | 0.3272 |
| pairs where the correction exceeded 1.0 | 0 |
| observed as a share of the ceiling | 33.0% |
| median r_full, non-zero leaves only (sensitivity) | 0.7571 |

> **The instrument is stable, so 0.2964 really is modest agreement.** Correcting for measurement error moves the headline only from 0.2964 to 0.3272 -- about 10%. There is no large hidden agreement being masked by a noisy instrument.

**Headline sentence for the paper:** *Cross-model agreement is real but limited: models share a difficulty dimension that explains a minority of the variance.*

With rho around 0.33 even after correction, the shared difficulty dimension accounts for roughly 11% of the variance in leaf instability. That is a real effect and a small one, and the paper should say both.

---

## Step 2 - Transfer: the number a practitioner can act on

**Computed.** For every ORDERED model pair, the share of A's top-k unstable leaves that fall inside B's top-2k. Ordered rather than symmetrised, because the relation genuinely differs by direction when two models have different numbers of non-zero leaves. Where a model has fewer than k non-zero leaves, only its non-zero entries are used and the truncation is recorded -- padding with zeros would rank arbitrary stable leaves and manufacture overlap. The chance line is recomputed per pair from the EFFECTIVE k.

| k | set | pairs | median | IQR | chance | lift | median k_eff | truncated |
|---|---|---|---|---|---|---|---|---|
| 5 | frontier-only | 90 | 0.600 | 0.200 | 0.175 | 0.425 | 5.0 | 27 |
| 5 | all 12 models | 132 | 0.600 | 0.200 | 0.175 | 0.425 | 5.0 | 33 |
| 10 | frontier-only | 90 | 0.500 | 0.193 | 0.228 | 0.281 | 10.0 | 84 |
| 10 | all 12 models | 132 | 0.500 | 0.179 | 0.254 | 0.242 | 10.0 | 108 |
| 20 | frontier-only | 90 | 0.500 | 0.167 | 0.228 | 0.248 | 13.0 | 90 |
| 20 | all 12 models | 132 | 0.500 | 0.299 | 0.254 | 0.193 | 14.5 | 128 |

### What step 2 decides

> **50% against a 23% chance line** (k = 10, frontier-only, n = 90 ordered pairs) -- a 2.2x lift.

**In plain language, as a practitioner would read it:** *if you know which ten clause types one frontier model answers least reliably, half of them will sit in another frontier model's twenty least reliable -- about twice what guessing would give you.*

**The caveat that must travel with that sentence:** 84 of 90 pairs were truncated, because at this arm most frontier models do not HAVE ten unstable leaves (median effective k = 10.0). The k = 10 row is really a 'top ~10'. The k = 5 row (60% vs 18% chance, 27/90 truncated) is the cleaner claim, and the two should be reported together rather than the larger lift alone.

---

## Step 3 - The descriptive category layer

**Computed.** A model x category matrix of wobble with **Wilson score intervals** -- not the normal approximation, because most cells here sit near zero, where a normal interval on 0/n returns [0, 0] and asserts certainty. Item counts are summed and the rate formed from the totals; per-leaf rates are never averaged, which would weight a 3-item leaf like a 30-item one. Instrument check: categories selftest PASS - Wilson correct at 0/n, n/n, symmetric, n=0 refused; the estimability floor counts contributing tasks and refuses an emptied category.

Full matrix with n and both interval bounds on every cell: `out/tables/model_x_category_wilson.csv`.

| Category | leaves | estimable (>= 3 leaves) |
|---|---|---|
| cap_table | 7 | yes |
| convertibles | 12 | yes |
| exit_waterfall | 3 | yes |
| founder_equity | 5 | yes |
| priced_equity | 16 | yes |
| regulatory | 5 | yes |
| rights_governance | 7 | yes |
| risk_flag | 5 | yes |

### Worst-category ratio - the evidence for the deployment recommendation

| Model | mean wobble | worst category | worst wobble | 95% CI | ratio |
|---|---|---|---|---|---|
| `gemini3-flash-or` | 0.0256 | exit_waterfall | 0.1250 | [0.022, 0.471] | 4.89 |
| `haiku-4.5-direct` | 0.0278 | exit_waterfall | 0.5000 | [0.215, 0.785] | 18.00 |
| `gemma4-31b-or` | 0.0299 | exit_waterfall | 0.5000 | [0.215, 0.785] | 16.75 |
| `mistral-large-or` | 0.0319 | exit_waterfall | 0.2500 | [0.071, 0.591] | 7.83 |
| `llama3.3-70b-or` | 0.0320 | exit_waterfall | 0.3750 | [0.137, 0.694] | 11.72 |
| `deepseek-v4p` | 0.0448 | exit_waterfall | 0.1250 | [0.022, 0.471] | 2.79 |
| `gpt5-mini-or` | 0.0553 | exit_waterfall | 0.5000 | [0.215, 0.785] | 9.04 |
| `deepseek-v4f` | 0.0574 | regulatory | 0.1481 | [0.059, 0.325] | 2.58 |
| `gpt-oss-120b-or` | 0.0618 | exit_waterfall | 0.2500 | [0.071, 0.591] | 4.04 |
| `minimax-m2.5-or` | 0.0745 | exit_waterfall | 0.3750 | [0.137, 0.694] | 5.04 |
| `gemma3-1b-qat` | 0.3383 | exit_waterfall | 0.7500 | [0.409, 0.929] | 2.22 |
| `gemma3-1b` | 0.4243 | cap_table | 0.9697 | [0.847, 0.995] | 2.29 |

- Median worst-to-mean ratio: **4.96x**. A model's headline wobble understates its worst clause type by roughly that factor.
- Spearman(mean wobble, ratio) = **-0.7063**: the ratio GROWS as models get better -- so the headline number is *most* misleading for the models a practitioner is most likely to deploy.
- **But that correlation shares a denominator** (the mean is the ratio's divisor), so some inverse relationship is mechanical. The same question without the shared term: Spearman(mean wobble, WORST-category wobble) = **0.4000**. That is POSITIVE (0.400): worse models do have worse worst-categories, so the ratio relationship is not purely mechanical. But it is far weaker than the ratio correlation implies, and the honest reading is that the ratio grows mainly because the MEAN falls faster than the worst category does.

> Every pair of category cells whose Wilson intervals overlap is **statistically indistinguishable and must not be ordered in prose**. For `gemma3-1b` alone, 13 category pairs overlap; the full set is derivable from the interval columns in the CSV.

### Item-level predictors (DESCRIPTIVE - not a predictive model)

OLS on per-leaf mean wobble across models, **n = 60 leaves**, 6 parameters. R^2 = 0.2078, **adjusted R^2 = 0.1345**. With 60 leaves this describes the sample; it does not predict out of sample and is not presented as if it does.

| Term | beta | 95% CI | verdict |
|---|---|---|---|
| intercept | 0.210030 | [0.071250, 0.348810] | **excludes 0** |
| is_numeric | -0.020307 | [-0.133020, 0.092405] | crosses 0 |
| is_binary | -0.115260 | [-0.226580, -0.003940] | **excludes 0** |
| is_multi | -0.007568 | [-0.171075, 0.155939] | crosses 0 |
| n_items | 0.003486 | [-0.006403, 0.013374] | crosses 0 |
| clause_chars | -0.000055 | [-0.000097, -0.000013] | **excludes 0** |

**Does answer type dominate category?** Nested adjusted-R^2 comparison, which (unlike R^2) can fall when a block adds only noise:

| Base | + block | adj R^2 base | adj R^2 full | delta |
|---|---|---|---|---|
| answer type + size | category | 0.1345 | 0.3555 | 0.2210 |
| size + category | answer type | 0.2426 | 0.3555 | 0.1128 |

> **No -- answer type does NOT dominate.** Category adds 0.2210 adjusted R^2 on top of answer type and size, while answer type adds only 0.1128 on top of category and size. Both blocks carry independent signal and category carries more. This is a DIFFERENT question from stage 1's strata result, which asked whether models AGREE within an answer type; this asks what predicts the LEVEL of wobble. A sentence claiming answer type is the mechanism would overstate what this shows.

---

## Step 4 - Supporting analyses that pre-empt specific attacks

### 4a. Is wobble just item difficulty?

Spearman(per-leaf mean wobble, per-leaf mean majority accuracy) = **-0.5516** (Kendall tau -0.4043, n = 60 leaves).

> **The objection has force and the paper must concede it.** A correlation of -0.552 means roughly 30% of the variance in leaf instability is shared with difficulty. The defensible claim is the narrow one: instability is PARTLY, but not wholly, item difficulty -- about 70% of the variance is not shared. A caveat cutting the other way: wobble and accuracy are computed from the SAME runs, so part of this correlation is mechanical rather than substantive.

**High-accuracy AND high-wobble leaves (pre-registered thresholds: accuracy >= 0.9, wobble >= 0.3): 0.**

> **Zero, at the threshold fixed in advance -- an inconvenient result, reported as found.** The brief expected these to be the paper's best concrete examples; at this arm they do not exist. Of the 35 leaves models answer correctly at least 90% of the time, the MOST unstable reaches only 0.1667 wobble. No threshold was searched for one that would produce examples. The five nearest misses are listed below purely descriptively, so a reader can see where the boundary sits.

| Leaf (nearest misses, descriptive) | mean wobble | mean accuracy |
|---|---|---|
| `s1_risk_factors` | 0.1667 | 0.9000 |
| `securities_exemption` | 0.1333 | 0.9417 |
| `exercise_window` | 0.1333 | 0.9667 |
| `flag_internal_inconsistency` | 0.1333 | 0.9167 |
| `pre_vs_post_money` | 0.1316 | 0.9035 |

### 4b. Bootstrap interval on the headline

Percentile bootstrap over LEAVES, 2000 replicates, fixed seed: median rho **0.2963**, **95% CI [0.1144, 0.4584]** (resampling 57 leaves; the worst replicate left 11 pairs undefined, counted rather than silently dropped).

> The permutation null said *not zero*. This says *not precise*. The interval excludes zero comfortably but spans a factor of four, so the paper can claim the effect exists and cannot claim its size to two decimals. Quote the interval wherever the point estimate appears.

### 4c. Leave-one-model-out

| Model dropped | pairs | median rho | shift |
|---|---|---|---|
| `mistral-large-or` | 55 | 0.2787 | -0.0176 |
| `llama3.3-70b-or` | 55 | 0.2787 | -0.0176 |
| `gpt5-mini-or` | 55 | 0.2787 | -0.0176 |
| `deepseek-v4f` | 55 | 0.2890 | -0.0073 |
| `gemma4-31b-or` | 55 | 0.2890 | -0.0073 |
| `minimax-m2.5-or` | 55 | 0.2949 | -0.0015 |
| `gpt-oss-120b-or` | 55 | 0.2949 | -0.0015 |
| `gemini3-flash-or` | 55 | 0.2978 | +0.0015 |
| `deepseek-v4p` | 55 | 0.3044 | +0.0081 |
| `haiku-4.5-direct` | 55 | 0.3044 | +0.0081 |
| `gemma3-1b-qat` | 55 | 0.3183 | +0.0219 |
| `gemma3-1b` | 55 | 0.3305 | +0.0341 |

> The largest shift is **+0.0341** (dropping `gemma3-1b`), so no single model carries the result. All twelve recomputations stay far above the permutation null. Note the direction: dropping either 1B model RAISES the median, consistent with them being the least typical members of the lineup rather than the drivers of the agreement.

### 4d. Item-count weighting

Spearman between the item-weighted ordering (what the benchmark reports) and the leaf-equal ordering = **0.9790** over 12 models. The two weightings order the models almost identically, so the stage-1 capability split does not rest on the weighting choice and the reading is unchanged.

---

## Step 5 - The two attacks statistics cannot answer

### 5a. Annotation agreement

**PREPARED, NOT RUN.** A stratified 20% sample of **19 leaves / 154 items** is drawn with a fixed seed, alongside the protocol and a blank scoring sheet: `out/annotation/`.

> **The paper has no agreement figure yet, and this stage did not produce one.** It is a blocking item, not a completed one. The materials reduce it to a single sitting; they do not substitute for it. The scoring sheet deliberately withholds the original label, because a re-annotator who can see it measures agreement with a prompt rather than two independent readings.

### 5b. Related work

`out/related_work.md` -- every citation verified against a live record (arXiv API or the ACL Anthology), each with its claim and its relation to this paper. **One directly adjacent prior result exists and it points the other way.** After the ceiling, that is the most important finding in this stage; it is discussed in full there.

### 5c. Venue mechanics

`out/venue_facts.md` -- fetched from the live call for papers with the URL beside every fact, and NOT STATED recorded where the page is silent rather than inferred from convention.

---

## The brief's twelve questions

Derived from the computed context, so an answer and its own table cannot disagree. n is stated on every one.

**1. Median split-half reliability (Spearman-Brown corrected).** Overall **0.8970** (n = 12 models; median uncorrected r_half 0.8133). Per model, best first: `gemma4-31b-or` 1.000 · `llama3.3-70b-or` 0.964 · `gpt5-mini-or` 0.934 · `mistral-large-or` 0.925 · `haiku-4.5-direct` 0.924 · `minimax-m2.5-or` 0.902 · `gemma3-1b-qat` 0.892 · `deepseek-v4f` 0.870 · `gemma3-1b` 0.841 · `gemini3-flash-or` 0.831 · `deepseek-v4p` 0.824 · `gpt-oss-120b-or` 0.776. Under 40 random splits instead of odd/even the median is 0.8992 (95% spread [0.8836, 0.9249]). Restricted to each model's own non-zero leaves the median falls to 0.7571 (n = 12), which is still in the same row of the decision table.

**2. Which row, and therefore the headline sentence.** The **high** row (median r_full 0.8970, against cuts at 0.40 and 0.70). The instrument is stable, so the observed agreement really is modest.

> *Cross-model agreement is real but limited: models share a difficulty dimension that explains a minority of the variance.*

**3. Disattenuated rho beside the observed.** Observed median **0.2964**, disattenuated **0.3272** (n = 66 defined pairs of 66; 0 pairs exceeded 1.0). The correction is worth about 10%, so measurement error was not hiding a large effect. Observed sits at 33.0% of the median ceiling; even at the ceiling the shared dimension would explain roughly 11% of the variance.

**4. Transfer at k=10, frontier-only, in plain language.** **50% against a 23% chance line** (n = 90 ordered pairs, IQR 0.193).

> *If you know the ten clause types one frontier model handles least reliably, about half of them will be among another frontier model's twenty least reliable — roughly twice what you would get by guessing.*

Carry the caveat with the sentence: 84 of 90 pairs were truncated because most frontier models do not have ten unstable leaves (median effective k = 10.0), so this is really a 'top ~10'. At k=5, where truncation is rarer (27/90), it is 60% against 18%.

**5. Worst-category-to-mean ratio, and does it shrink with capability?** Median **4.96x** over 12 models: `haiku-4.5-direct` 18.0x · `gemma4-31b-or` 16.8x · `llama3.3-70b-or` 11.7x · `gpt5-mini-or` 9.0x · `mistral-large-or` 7.8x · `minimax-m2.5-or` 5.0x · `gemini3-flash-or` 4.9x · `gpt-oss-120b-or` 4.0x · `deepseek-v4p` 2.8x · `deepseek-v4f` 2.6x · `gemma3-1b` 2.3x · `gemma3-1b-qat` 2.2x. **It does not shrink — it GROWS** as models improve: Spearman(mean wobble, ratio) = **-0.7063**. But that shares a denominator, so the honest companion is Spearman(mean wobble, WORST-category wobble) = **0.4000** — positive but weak. The defensible statement is that the ratio grows mainly because the mean falls faster than the worst category does, which still means a frontier model's headline number understates its worst clause type by the most.

**6. Does answer type dominate category in the predictor model?** **No.** Adding category to answer type + size gains **0.2210** adjusted R^2; adding answer type to category + size gains **0.1128**. Both carry independent signal and **category, NOT answer type** carries more (full model adj R^2 0.3555, n = 60 leaves). Note this is a different question from stage 1's strata result: that asked whether models AGREE within an answer type, this asks what predicts the LEVEL of wobble. The paper must not merge them into one 'answer format is the mechanism' sentence.

**7. Item-level wobble vs accuracy, and the high-accuracy/high-wobble count.** Spearman **-0.5516** (tau -0.4043, n = 60 leaves) — roughly 30% shared variance. **The difficulty objection has real force and must be conceded**; the claim narrows to 'partly, but not wholly, item difficulty'. High-accuracy AND high-wobble leaves at the pre-registered thresholds (>= 0.9 accuracy, >= 0.3 wobble): **0**. Of the 35 leaves models answer correctly at least 90% of the time, the most unstable reaches only 0.1667. The paper's hoped-for 'deployment nightmare' examples do not exist at this arm, and no threshold was searched for one that would produce them.

**8. Bootstrap 95% interval on the headline.** **[0.1144, 0.4584]** around a median of 0.2963 (2000 leaf-resampled replicates over 57 leaves). Excludes zero comfortably, but spans a factor of four — quote the interval wherever the point estimate appears.

**9. Does leave-one-model-out change the reading? Which model matters most?** **No.** The twelve recomputations span 0.2787–0.3305, all far above the permutation null. The model that matters most is **`gemma3-1b`** at **+0.0341**. Dropping either 1B model RAISES the median, so they are the least typical members of the lineup rather than the drivers of the agreement.

**10. FinNLP mechanics.** Long **8 pages** excluding references (short/demo 4). Direct submissions **must be anonymized**. Whether an identifying repository link is permitted in an anonymous submission is **NOT STATED** on either the workshop page or the ARR anonymity page — an open item to resolve with the organisers, not by inference. AI assistance **must be disclosed** (writing AND coding) in the Responsible NLP Checklist with details in the Acknowledgements; AI tools cannot be authors. ACL template required, version not stated. OpenReview; ARR commitment exists but only for work already in ARR. Direct deadline **2026-08-11**. Sources in `out/venue_facts.md`.

**11. Prior work on item-level cross-model consistency agreement.** **Yes — one, and it points the other way.** Cacioli (2026), *Beyond the Mean: Within-Model Reliable Change Detection for LLM Evaluation*, arXiv:2604.27405, already uses split-half + Spearman-Brown on LLM items at temperature 0.7, and reports a **near-zero cross-model item correlation (r = .11, n = 431)**. It correlates version-to-version CHANGE (RCI) rather than within-model run-to-run instability, and over two model pairs rather than twelve models, so the constructs differ and Paper A is not scooped — **but that distinction has to be drawn explicitly and early, not assumed.** It also means split-half reliability cannot be presented as a methodological contribution. Full analysis in `out/related_work.md`.

**12. Decided by judgement rather than by rule.** (a) odd/even as the split rule, on the interleaving argument — repeated random splits were added afterwards as a check and agree; (b) reliability computed on the active subset, to match the headline's vector; (c) the non-zero-only reliability sensitivity was ADDED, not pre-registered — it can only weaken the ceiling claim, which is why it is reported; (d) repeated random splits were ADDED after finding Cacioli 2026, and are labelled as such; (e) the disattenuation is computed PER PAIR then summarised, rather than dividing the median by one global reliability; (f) HIGH_ACC 0.90 and HIGH_WOBBLE 0.30 were fixed in advance and NOT moved when they returned zero; (g) `MIN_LEAVES_PER_CATEGORY = 3`, which happens to make every category estimable — `exit_waterfall` sits exactly on the floor with 3 leaves and its intervals are correspondingly wide; (h) the category dummy reference level is the alphabetically first family; (i) rows with any missing predictor would have been dropped and counted, though none were; (j) the answer-type labels are stage 1's, including its six judgement calls.

