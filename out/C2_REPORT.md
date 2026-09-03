# C2 diagnostic - is wobble a property of the item or of the model?

**Paper A only.** Data: Probity tag `v1.3.1`, read from disk. Arm: **legacy (temperature 0.7)** and nothing else -- no number here derives from the 0.1 arm or from any cross-arm comparison.

Regenerate: `python3 analysis/run_all.py`. Every figure quoted here is mapped to its file and computation in `NUMBERS.md`.

---

## 1. Pre-registered analysis (written before any coefficient was computed)

**Arm:** `legacy (temperature 0.7)` and nothing else. Inside Probity the published 0.7 sweep is the LEGACY, UNSUFFIXED namespace (`leaves/*/scored.json`), represented internally by the sentinel `None`. The literal float `0.7` selects `scored_t07.json`, a different 2-model Kaggle cross-machine control, so the arm is declared once in `analysis/config.py` and a fail-closed guard rejects any opened path containing `_t01` / `t07`.

**Unit.** The leaf, not the document category. 60 leaves, 12 models, one wobble rate per cell. Categories are a descriptive layer, never the statistical unit.

**Primary test (one, named in advance).** The MEDIAN pairwise Spearman rho on the ACTIVE SUBSET (leaves with non-zero wobble in at least one model), over the models not excluded by the tie rule, compared against a permutation null built from the same models, the same leaves and the same tie structure. Everything else in this report is a named secondary or a control and is labelled as such.

**Definitions, fixed in advance.**

| Quantity | Definition |
|---|---|
| wobble rate of a cell | flipped items / measured items, where an item is measured iff it recorded at least one valid run |
| dropped cell | the benchmark's own `reliability.measurable == False`, i.e. `parse_failures/runs > 0.30` or fewer than 2 valid runs (`engine/scorer.py`) |
| tie fraction | share of a model's leaf values that occur more than once in that same vector |
| active subset | leaves with non-zero wobble in >= 1 model |
| common subset | leaves retained (not dropped, not absent) for all 12 models |
| capability split | sort models by aggregate 0.7 wobble, cut at the LARGEST gap between consecutive values |
| permutation null | 1000 permutations, seed `20260728`; each model's observed values are permuted among its own positions, preserving its exact tie structure and n |

**Pre-registered thresholds.** tie exclusion > `0.8` · "tight" IQR <= `0.4` · "indistinguishable from the null" within `0.05` · a stratum needs >= `4` defined pairs to be called a distribution.

### 1.1 Declared deviations and disclosures

| # | What | Why |
|---|---|---|
| D1 | The pre-registration was authored after inspecting the matrix's SHAPE (cell coverage, per-model zero counts, per-model aggregate wobble) but before computing any correlation coefficient, any subset distribution or any null. | Honest disclosure. Those shape facts are what made the tie control's design concrete; none of them is a coefficient. |
| D2 | The brief says six of the twelve models are served through a routing layer. On disk it is 7. | `engine/preflight.py:LINEUP` is the repo's declared label -> client map and is used as written. The disagreement is reported, not silently resolved. |
| D3 | Tie-based exclusion for the headline uses each model's tie fraction on its FULL 60-leaf vector, as the brief words it ("the model's leaf vector"). The active-subset tie fractions are reported beside it and the headline is re-run under active-subset exclusion as a named sensitivity. | The literal reading is the stricter one; the alternative is shown so the choice is visible rather than load-bearing and hidden. |
| D4 | Top-10 concentration is reported on both the rate mass and the flipped-item mass. | Both derive from the two mandated matrices; 'mass' is ambiguous between them, so neither is hidden. |
| D5 | Six leaves' answer types are judgement calls (declared type `date` or `string`); each is justified in `answer_types.md` and re-listed in Q10. | The brief permits judgement where mechanical classification is impossible. |

## 2. Provenance and coverage (the scope rule, verified rather than asserted)

- Every manifest written by this arm was read: **640 found**, 80 cells have none. Full coverage on 10 of 12 models; partial on `deepseek-v4f` (2/60), `gemma3-1b` (38/60) -- the two earliest-run labels, from before the manifest step existed. That is a documentation gap, not a provenance gap: their run artefacts sit in the same unsuffixed namespace, which is what the arm is defined by.
- Temperatures those manifests state: `0.7` x640. n_runs they state: `20` x640.
- Cells: **720** (12 models x 60 leaves). Absent: 0. Dropped by the >30% unparseable rule: **0**.
- Instrument check, run before any number was trusted: selftest PASS - vectorised rho matches scipy.spearmanr on all 66 defined pairs (max |delta| 1.11e-16); permutation preserves the tie multiset.

> The manifest check is a POSITIVE control, not a formality: it could have detected the wrong arm (it reports the temperatures it actually saw, not a boolean), and 0.1 would have shown up in that list.

## 3. The wobble matrix (brief 4a)

Files: `out/tables/wobble_matrix.csv` (12 x 60 rates) and `out/tables/n_and_dropped_matrix.csv` (per cell: n_items, n_instances, n_runs recorded, flipped, wobble, dropped, absent, parse-failure rate). Every number below derives from these two and nothing else.

| Model | Serving | Aggregate wobble | Leaves at exactly 0 | Measured items | Flipped items | Dropped cells |
|---|---|---|---|---|---|---|
| `gemma3-1b` | local | 42.43% | 8 | 469 | 199 | 0 |
| `deepseek-v4f` | direct | 5.74% | 42 | 470 | 27 | 0 |
| `deepseek-v4p` | direct | 4.48% | 45 | 469 | 21 | 0 |
| `gemma4-31b-or` | routed | 2.99% | 53 | 469 | 14 | 0 |
| `mistral-large-or` | routed | 3.19% | 48 | 470 | 15 | 0 |
| `minimax-m2.5-or` | routed | 7.45% | 42 | 470 | 35 | 0 |
| `llama3.3-70b-or` | routed | 3.20% | 51 | 469 | 15 | 0 |
| `gemma3-1b-qat` | local | 33.83% | 10 | 470 | 159 | 0 |
| `gemini3-flash-or` | routed | 2.56% | 49 | 469 | 12 | 0 |
| `haiku-4.5-direct` | direct | 2.78% | 51 | 468 | 13 | 0 |
| `gpt-oss-120b-or` | routed | 6.18% | 40 | 469 | 29 | 0 |
| `gpt5-mini-or` | routed | 5.53% | 46 | 470 | 26 | 0 |

- Leaves with zero wobble in **all 12** models: **3** (`participation_cap`, `note_principal`, `convert_vs_preference_decision`).
- Leaves with non-zero wobble in at least one model (**the active subset**): **57** of 60.

## 4. Pairwise rank correlation (brief 4b)

All 66 unordered model pairs. Per-pair rho, tau-b, n and both sides' tie fractions are in `out/tables/pairs_*.csv` -- every coefficient, including the inconvenient ones. Distribution summaries (`out/tables/distributions.csv`):

| Distribution | pairs | defined | undefined | median rho | Q1 | Q3 | IQR | min | max | note |
|---|---|---|---|---|---|---|---|---|---|---|
| pre-registered primary - tie-filtered models, active subset | 0 | 0 | 0 | — | — | — | — | — | — | null median —, null 97.5th —, p=— · the one pre-registered test |
| tie-filtered models, full 60 leaves | 0 | 0 | 0 | — | — | — | — | — | — | null median —, null 97.5th —, p=— · secondary |
| **REPORTED** all 12 models, active subset | 66 | 66 | 0 | 0.296 | 0.210 | 0.405 | 0.195 | -0.165 | 0.640 | null median -0.004, null 97.5th 0.036, p=0.0010 · control |
| all 12 models, full 60 leaves | 66 | 66 | 0 | 0.301 | 0.228 | 0.410 | 0.183 | -0.110 | 0.647 | null median -0.005, null 97.5th 0.036, p=0.0010 · control |
| all 12 models, common subset | 66 | 66 | 0 | 0.301 | 0.228 | 0.410 | 0.183 | -0.110 | 0.647 | null median -0.005, null 97.5th 0.036, p=0.0010 · control (5c) |

Model set surviving the tie rule: **1 of 12** (`gemma3-1b-qat`), giving 0 pairs.

> **Deviation, forced.** The pre-registered primary is UNDEFINED on this data: the tie rule (> 0.8) excludes 11 of 12 models, leaving 1 and therefore 0 pairs. The reported headline is the SAME test on all 12 models over the same active subset, scored against a null carrying this data's exact tie structure. This substitution is forced by the rule collapsing, not chosen after inspecting results; the excluded-set result is reported beside it.

Figures: `out/figures/rho_heatmap.png` (models x models), `out/figures/rho_vs_null.png` (the reported headline vs its null), `out/figures/wobble_heatmap.png` (models x leaves).

## 5a. Tie mass -- the control most likely to decide this

| Model | Tie fraction (60) | Zeros (60) | Distinct values (60) | Tie fraction (active) | Zeros (active) | Headline (> 0.8) |
|---|---|---|---|---|---|---|
| `gemma3-1b` | 0.817 | 13.3% | 22 | 0.807 | 8.8% | **EXCLUDED** |
| `deepseek-v4f` | 0.917 | 70.0% | 12 | 0.912 | 68.4% | **EXCLUDED** |
| `deepseek-v4p` | 0.883 | 75.0% | 11 | 0.877 | 73.7% | **EXCLUDED** |
| `gemma4-31b-or` | 0.883 | 88.3% | 8 | 0.877 | 87.7% | **EXCLUDED** |
| `mistral-large-or` | 0.883 | 80.0% | 10 | 0.877 | 78.9% | **EXCLUDED** |
| `minimax-m2.5-or` | 0.933 | 70.0% | 11 | 0.930 | 68.4% | **EXCLUDED** |
| `llama3.3-70b-or` | 0.917 | 85.0% | 8 | 0.912 | 84.2% | **EXCLUDED** |
| `gemma3-1b-qat` | 0.783 | 16.7% | 24 | 0.772 | 12.3% | kept |
| `gemini3-flash-or` | 0.917 | 81.7% | 9 | 0.912 | 80.7% | **EXCLUDED** |
| `haiku-4.5-direct` | 0.917 | 85.0% | 8 | 0.912 | 84.2% | **EXCLUDED** |
| `gpt-oss-120b-or` | 0.817 | 66.7% | 16 | 0.807 | 64.9% | **EXCLUDED** |
| `gpt5-mini-or` | 0.850 | 76.7% | 12 | 0.842 | 75.4% | **EXCLUDED** |

Sensitivity (D3): excluding on the ACTIVE-subset tie fraction instead would exclude 11 models (`gemma3-1b`, `deepseek-v4f`, `deepseek-v4p`, `gemma4-31b-or`, `mistral-large-or`, `minimax-m2.5-or`, `llama3.3-70b-or`, `gemini3-flash-or`, `haiku-4.5-direct`, `gpt-oss-120b-or`, `gpt5-mini-or`).

## 5b. Capability stratification

Split rule: largest gap between consecutive aggregate-wobble values. Sorted: `gemini3-flash-or` 2.56% · `haiku-4.5-direct` 2.78% · `gemma4-31b-or` 2.99% · `mistral-large-or` 3.19% · `llama3.3-70b-or` 3.20% · `deepseek-v4p` 4.48% · `gpt5-mini-or` 5.53% · `deepseek-v4f` 5.74% · `gpt-oss-120b-or` 6.18% · `minimax-m2.5-or` 7.45% · `gemma3-1b-qat` 33.83% · `gemma3-1b` 42.43%. Largest gap = **26.38 points**, so the threshold is **20.64%**: low = `gemma3-1b-qat`, `gemma3-1b`; frontier = the other 10.

| Group | members | pairs | defined | median rho | IQR | null median | null 97.5 | p | note |
|---|---|---|---|---|---|---|---|---|---|
| frontier | 10 | 45 | 45 | 0.358 | 0.148 | -0.007 | 0.046 | 0.0010 |  |
| low | 2 | 1 | 1 | 0.406 | 0.000 | -0.004 | 0.275 | 0.0020 | too few pairs for a distribution |
| ACROSS | — | 20 | 20 | 0.195 | 0.146 | 0.003 | 0.068 | 0.0010 |  |


## 5c. Dropped-leaf accounting

- Dropped cells (>30% unparseable): **0** of 720. Absent cells: 0.
- Per family: cap_table 0, convertibles 0, exit_waterfall 0, founder_equity 0, priced_equity 0, regulatory 0, rights_governance 0, risk_flag 0
- Common subset (leaves retained for all 12 models): **60** of 60.

> **This control is VACUOUS on this arm, not passed.** At temperature 0.7 the benchmark drops nothing, so the common subset is identical to the full set by construction and the re-run cannot disagree with the full-intersection version. It is reported because a control that could not fire must be named as such rather than counted as evidence. (Parse failures exist -- they just never reach the 30% gate on any cell; per-cell rates are in `n_and_dropped_matrix.csv`.)

## 5d. Serving-layer confound

Serving path per model is parsed from `engine/preflight.py:LINEUP`, the repo's declared label -> client map -- not inferred from the `-or` filename suffix. Counts: **direct** 3 · **local** 2 · **routed** 7. (The brief says six routed; on disk it is 7 -- deviation D2.)

| Group | members | pairs | defined | median rho | IQR | null median | p |
|---|---|---|---|---|---|---|---|
| direct | `deepseek-v4f`, `deepseek-v4p`, `haiku-4.5-direct` | 3 | 3 | 0.330 | 0.040 | -0.010 | 0.0010 |
| local | `gemma3-1b`, `gemma3-1b-qat` | 1 | 1 | 0.406 | 0.000 | -0.004 | 0.0020 |
| routed | `gemini3-flash-or`, `gemma4-31b-or`, `gpt-oss-120b-or`, `gpt5-mini-or`, `llama3.3-70b-or`, `minimax-m2.5-or`, `mistral-large-or` | 21 | 21 | 0.410 | 0.152 | -0.008 | 0.0010 |
| DIFFERENT | — | 41 | 41 | 0.237 | 0.141 | -0.002 | 0.0010 |

> **The raw split above is confounded and must not be read on its own.** Every routed and every direct model in this lineup sits in the FRONTIER tier, and both local models sit in the LOW tier. So `DIFFERENT` is where all 20 low-vs-frontier pairs live, and its lower median is mostly the capability effect from 5b re-appearing, not a serving effect. The `local` row is a single pair -- and it is the same base model at two quantizations, so it is closer to a self-correlation than to cross-model agreement.

Isolating serving from capability, WITHIN the frontier tier only:

| Frontier-only group | pairs | defined | median rho | IQR | null median | p |
|---|---|---|---|---|---|---|
| same path | 24 | 24 | 0.399 | 0.154 | -0.009 | 0.0010 |
| different path | 21 | 21 | 0.295 | 0.184 | -0.005 | 0.0010 |

## 5e. Permutation null (what turns a number into a claim)

1000 permutations, seed `20260728`, on the same models and the same leaves as the reported headline. Each model's observed values are permuted among its OWN positions, so the null carries this data's exact tie structure and exact n; only the pairing between models is destroyed.

> This is why the tie problem does not invalidate the result: heavy tie mass depresses Spearman in the OBSERVED data and in the NULL by exactly the same mechanism, because the null is built by permuting the same values. Ties cost power, they do not manufacture the gap between the two.

| Quantity | Value |
|---|---|
| observed median rho (reported headline) | 0.2964 |
| null median of medians | -0.0044 |
| null 95% envelope of the median | [-0.0444, 0.0362] |
| null max median over all permutations | 0.0818 |
| one-sided permutation p | 0.00100 |

## 5f. Answer-space strata

Per-leaf classification with justifications: `out/answer_types.md`. Distributions are computed on the active subset, restricted to each stratum's leaves. `mean tie` is the average tie fraction INSIDE that stratum -- reported because a low stratum median has two possible causes (no agreement, or an estimator that cannot see agreement through the ties) and only this column separates them.

| Answer type | leaves | pairs | defined | median rho | IQR | mean tie | null median | null 97.5 | p | note |
|---|---|---|---|---|---|---|---|---|---|---|
| binary | 21 | 66 | 66 | 0.028 | 0.434 | 0.825 | -0.053 | 0.043 | 0.0390 | **does NOT clear its own null** |
| categorical | 6 | 66 | 55 | 0.429 | 0.559 | 0.625 | 0.017 | 0.220 | 0.0010 |  |
| multi_part | 3 | 66 | 55 | 0.000 | 1.366 | 0.472 | 0.000 | 0.500 | 0.8492 | n<4 leaves - not a distribution · **does NOT clear its own null** |
| numeric | 27 | 66 | 66 | 0.444 | 0.276 | 0.852 | -0.003 | 0.051 | 0.0010 |  |

> **This is the answer to the brief's question 7, and it is not the comfortable one.** Agreement is carried by the **categorical/numeric** strata and does NOT clear its own null on **binary/multi_part**. So answer FORMAT is part of what the headline is measuring, not clause type alone. The brief says either answer is publishable but not knowing which is not -- this is the which.

> Is that just the tie problem again, one level down? **No.** `numeric` carries MORE tie mass (0.852 vs 0.825) and still reaches 0.444, while `binary` sits at 0.028. With tie mass effectively matched, the gap between the strata is a real difference in cross-model agreement, not the estimator's blind spot.

## 4c. Concentration -- the tie-immune route

Set overlap does not care how many leaves are tied at zero, so it answers the same question without Spearman's tie penalty. Padding is removed: for a model with fewer than 10 non-zero leaves only its non-zero entries count.

| Model | non-zero leaves | top-10 that are non-zero | top-10 share of rate mass | top-10 share of flipped items | top 5 leaves |
|---|---|---|---|---|---|
| `gemma3-1b` | 52 | 10 | 37.7% | 29.1% | `current_ownership_pct`, `employee_pool_pct`, `founder_ownership_pct`, `fully_diluted_basis`, `investor_ownership_pct` |
| `deepseek-v4f` | 18 | 10 | 78.2% | 66.7% | `option_pool_shuffle`, `liquidation_preference_multiple`, `securities_exemption`, `flag_missing_pro_rata`, `liquidation_waterfall_payout` |
| `deepseek-v4p` | 15 | 10 | 85.0% | 76.2% | `form_d_fields`, `safe_cap_vs_discount_applies`, `liquidation_waterfall_payout`, `board_seats_investor`, `conversion_ratio` |
| `gemma4-31b-or` | 7 | 7 | 100.0% | 100.0% | `liquidation_waterfall_payout`, `option_pool_shuffle`, `board_seats_investor`, `current_ownership_pct`, `s1_use_of_proceeds` |
| `mistral-large-or` | 12 | 10 | 94.5% | 86.7% | `liquidation_waterfall_payout`, `exercise_window`, `option_pool_shuffle`, `board_seats_investor`, `financial_statement_qa` |
| `minimax-m2.5-or` | 18 | 10 | 85.0% | 68.6% | `employee_pool_pct`, `option_pool_shuffle`, `liquidation_waterfall_payout`, `preference_stack_payout`, `board_seats_investor` |
| `llama3.3-70b-or` | 9 | 9 | 100.0% | 100.0% | `liquidation_waterfall_payout`, `option_pool_shuffle`, `form_d_fields`, `board_seats_investor`, `multi_round_stacked_dilution` |
| `gemma3-1b-qat` | 50 | 10 | 40.8% | 27.7% | `current_ownership_pct`, `employee_pool_pct`, `flag_internal_inconsistency`, `founder_ownership_pct`, `liquidation_waterfall_payout` |
| `gemini3-flash-or` | 11 | 10 | 97.5% | 91.7% | `option_pool_shuffle`, `liquidation_waterfall_payout`, `post_money_valuation`, `flag_internal_inconsistency`, `per_investor_allocation` |
| `haiku-4.5-direct` | 9 | 9 | 100.0% | 100.0% | `liquidation_waterfall_payout`, `founder_ownership_pct`, `option_pool_shuffle`, `s1_use_of_proceeds`, `drag_along` |
| `gpt-oss-120b-or` | 20 | 10 | 80.5% | 65.5% | `employee_pool_pct`, `option_pool_shuffle`, `liquidation_waterfall_payout`, `financial_statement_qa`, `investor_ownership_pct` |
| `gpt5-mini-or` | 14 | 10 | 91.1% | 80.8% | `liquidation_waterfall_payout`, `option_pool_shuffle`, `board_seats_investor`, `s1_use_of_proceeds`, `conversion_ratio` |

- Strict intersection of all 12 top-10 sets: **1** leaf/leaves (`liquidation_waterfall_payout`); union 39.
- Pairwise overlap across the 66 pairs: median **4.0** shared leaves (min 1, max 7), median Jaccard 0.250.

Leaves appearing in the most models' top-10 (the shape a shared difficulty dimension would take if it existed):

| Leaf | models (of 12) |
|---|---|
| `liquidation_waterfall_payout` | 12 |
| `option_pool_shuffle` | 11 |
| `board_seats_investor` | 8 |
| `liquidation_preference_multiple` | 7 |
| `s1_use_of_proceeds` | 7 |
| `financial_statement_qa` | 5 |
| `current_ownership_pct` | 4 |
| `employee_pool_pct` | 4 |
| `flag_internal_inconsistency` | 4 |
| `conversion_ratio` | 3 |
| `founder_ownership_pct` | 3 |
| `participation_type` | 3 |

## 6. Outcome -- which row of the brief's section-6 table the data lands on

Criteria are evaluated in code (`analysis/decision.py`) against thresholds fixed in the pre-registration, so the outcome is derived rather than authored beside its own table.

| Pre-registered criterion | Computed | Met |
|---|---|---|
| the PRE-REGISTERED primary (tie-filtered headline set) is computable | NO - the tie rule leaves fewer than two models, so it has zero pairs | NO |
| reported median above its own permutation null (97.5th pct of the null median) | 0.2964 vs 0.0362 | YES |
| reported median indistinguishable from the null median (within 0.05) | gap to null median = 0.3008 | NO |
| IQR tight (<= 0.4) | 0.1951 | YES |
| above the null on the full 60-leaf set (all 12 models) | 0.3014 | YES |
| above the null on the active subset (all 12 models) | 0.2964 | YES |
| above the null on the common subset (all 12 models) | 0.3014 | YES |
| group 'frontier' median above its own null | 0.3584 | YES |
| group 'low' median above its own null | 0.4060  [1 defined pair(s) - not a distribution] | n/a |
| group 'ACROSS' median above its own null | 0.1950 | YES |
| answer-type stratum 'binary' median above its own null | 0.0280 | NO |
| answer-type stratum 'categorical' median above its own null | 0.4287 | YES |
| answer-type stratum 'multi_part' median above its own null | 0.0000 | NO |
| answer-type stratum 'numeric' median above its own null | 0.4443 | YES |

### => **Row 1 - the paper as originally briefed (task properties, not model identity, drive instability)**

Because the reported median clears a permutation null built with this data's exact tie structure, with a tight IQR, and holds inside both capability tiers and across them. It is QUALIFIED: the agreement is carried by the categorical/numeric strata and does NOT clear its own null on the binary/multi_part stratum, so answer format is part of what is being measured - see 5f before writing the thesis sentence.

## 7. The brief's ten questions

**1. Which outcome row?** Row 1 - the paper as originally briefed (task properties, not model identity, drive instability).

**2. Headline statistic.** Median pairwise Spearman on the active subset (57 leaves, 66 defined pairs of 66): **0.2964**, IQR **0.1951** (Q1 0.210, Q3 0.405, range -0.165 to 0.640). Permutation-null median of medians **-0.0044**, null 95% envelope [-0.0444, 0.0362], null max over 1000 permutations 0.0818, one-sided p 0.00100. The pre-registered primary (tie-filtered set) is UNDEFINED: 1 model(s) survive the tie rule, so it has 0 pairs. Reported instead, forced: all 12 models on the same active subset, against a null with the same tie structure.

**3. Tie fraction per model / exclusions.** `gemma3-1b` 0.817 · `deepseek-v4f` 0.917 · `deepseek-v4p` 0.883 · `gemma4-31b-or` 0.883 · `mistral-large-or` 0.883 · `minimax-m2.5-or` 0.933 · `llama3.3-70b-or` 0.917 · `gemma3-1b-qat` 0.783 · `gemini3-flash-or` 0.917 · `haiku-4.5-direct` 0.917 · `gpt-oss-120b-or` 0.817 · `gpt5-mini-or` 0.850. Excluded as not interpretable (> 0.8): **11 of 12** — `gemma3-1b`, `deepseek-v4f`, `deepseek-v4p`, `gemma4-31b-or`, `mistral-large-or`, `minimax-m2.5-or`, `llama3.3-70b-or`, `gemini3-flash-or`, `haiku-4.5-direct`, `gpt-oss-120b-or`, `gpt5-mini-or`. That is the single most important instrument fact in this report: the rule was written to stop ties faking a null, and on this data it removes almost the entire experiment.

**4. Tier medians.** within-low **0.4060 [only 1 defined pair -- not a distribution]** · within-frontier **0.3584** · across-tier **0.1950**. All three clear their own nulls, so this is NOT the row-3 shape. Caveat that matters: the low tier has exactly two members and they are the same base model at two quantizations, so its single coefficient is nearer a self-correlation than cross-model agreement -- the load-bearing tier result is the frontier one (45 pairs).

**5. Common-subset re-run.** 60/60 leaves are common (zero drops at 0.7), so the common subset IS the full set and the re-run is identical by construction: median 0.3014 vs full 0.3014. The reading survives, but this control could not have failed here -- it is vacuous on this arm, not passed.

**6. Routed vs direct.** Raw: direct 0.3305 (3 pairs) · local 0.4060 (1 pair) · routed 0.4100 (21 pairs) · DIFFERENT 0.2370 (41 pairs). That raw split is confounded with capability (all routed and all direct models are frontier; both local models are low), so the answer is the frontier-only comparison: same path 0.3985 (24 pairs, p 0.0010) · different path 0.2949 (21 pairs, p 0.0010). Both clear their own null, so the agreement is not an artefact of the routing layer.

**7. Answer-type strata.** binary 0.0280 (21 leaves, mean tie 0.825) · categorical 0.4287 (6 leaves, mean tie 0.625) · multi_part 0.0000 (3 leaves, mean tie 0.472) · numeric 0.4443 (27 leaves, mean tie 0.852). **Answer format is doing part of the work**: the categorical/numeric strata clear their nulls and binary/multi_part does not. This is NOT a tie artefact: `numeric` carries slightly MORE tie mass (0.852 vs 0.825) and still reaches 0.444. With tie mass matched, the strata really do differ. `multi_part` has only 3 leaves and is reported but not interpreted.

**8. Top-10 overlap.** Strict 12-way intersection: **1** leaf/leaves (`liquidation_waterfall_payout`). Pairwise: median **4.0** shared, range 1-7; median Jaccard 0.250.

**9. Leaves with zero wobble in all twelve models: 3 of 60.**  This is small, so it does not by itself cap the analysis -- but the per-MODEL zero counts do, and those are the binding limit: see Q3.

**10. Judgement calls.** (a) folder placement: `paper-a/` was created OUTSIDE the probity repo (`~/paper-a`), so the public benchmark tree is untouched; one `mv` relocates it · (b) tie exclusion uses the full-60 vector (D3); when that rule left one model I reported the all-model distribution instead and labelled the promotion as forced, rather than quietly dropping the rule or quietly keeping an undefined primary · (c) the capability split is the largest-gap (natural-break) rule; the threshold it produced is reported in 5b · (c2) composing the pre-specified 5b and 5d splits (serving path WITHIN the frontier tier) is a named control I added because the raw 5d split is confounded with capability -- not a subgroup hunt, but it was not in the brief · (d) 6 answer types decided by judgement: `note_maturity_date`, `vesting_schedule`, `exercise_window`, `form_d_fields`, `s1_use_of_proceeds`, `s1_risk_factors` · (e) 'wobble mass' reported on both the rate and the flipped-item basis (D4) · (f) an undefined coefficient (constant vector) is excluded and counted, never coerced to 0.0.

