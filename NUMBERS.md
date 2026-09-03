# NUMBERS.md - every quoted figure, its file, and its computation

Arm: legacy (temperature 0.7). Regenerate everything with `python3 analysis/run_all.py`.

## Stage 1 - the C2 diagnostic

| Figure | Value | File | Computation |
|---|---|---|---|
| median pairwise Spearman, reported headline | 0.2964 | out/tables/distributions.csv (row `all_active`) | median of `spearman_rho` over the reported pair set on the active subset |
| IQR, reported headline | 0.1951 | out/tables/distributions.csv | Q3 - Q1 |
| models excluded by the tie rule | 11 | out/tables/tie_fractions.csv | count of rows with excluded_from_headline=1 |
| permutation-null median | -0.0044 | out/tables/permutation_null.json | median of 1000 per-permutation medians, seed 20260728 |
| null 97.5th percentile | 0.0362 | out/tables/permutation_null.json | 97.5th percentile of the null median distribution |
| null 2.5th percentile | -0.0444 | out/tables/permutation_null.json | 2.5th percentile of the null median distribution |
| null max median over all permutations | 0.0818 | out/tables/permutation_null.json | largest of the 1000 per-permutation medians |
| one-sided p | 0.00100 | out/tables/permutation_null.json | (#null medians >= observed + 1) / (n_perm + 1) |
| tie fraction per model | see table | out/tables/tie_fractions.csv | share of a model's 60 leaf values occurring more than once |
| aggregate wobble per model | see table | out/tables/model_summary.csv | sum(flipped items) / sum(measured items) over all 60 leaves |
| leaves zero in all 12 models | 3 | out/tables/wobble_matrix.csv | count of columns where every row is 0 |
| active subset size | 57 | out/tables/wobble_matrix.csv | columns with at least one non-zero cell |
| dropped cells | 0 | out/tables/n_and_dropped_matrix.csv | rows with dropped=1 (scorer `measurable` false) |
| common subset size | 60 | out/tables/n_and_dropped_matrix.csv | leaves with dropped=0 for all 12 models |
| top-10 intersection | 1 | out/tables/concentration_top10.csv | strict intersection of the 12 non-zero top-10 sets |
| median pairwise top-10 overlap | 4.0 | out/tables/concentration_top10.csv | median size of the intersection of two models' top-10 sets, over the 66 pairs |
| median pairwise top-10 Jaccard | 0.250 | out/tables/concentration_top10.csv | median of \|A and B\| / \|A or B\| over the 66 top-10 set pairs |
| most-shared leaf and its model count | `liquidation_waterfall_payout` in 12 | out/tables/concentration_top10.csv | leaf appearing in the most models' top-10 sets |
| routed models on disk | 7 | probity/engine/preflight.py:LINEUP | count of entries whose client is `openrouter` |
| median rho, group `frontier` | 0.3584 | out/tables/distributions.csv | median over the 45 defined pairs in that group |
| median rho, group `low` | 0.4060 | out/tables/distributions.csv | median over the 1 defined pairs in that group |
| median rho, group `ACROSS` | 0.1950 | out/tables/distributions.csv | median over the 20 defined pairs in that group |
| median rho, group `direct` | 0.3305 | out/tables/distributions.csv | median over the 3 defined pairs in that group |
| median rho, group `local` | 0.4060 | out/tables/distributions.csv | median over the 1 defined pairs in that group |
| median rho, group `routed` | 0.4100 | out/tables/distributions.csv | median over the 21 defined pairs in that group |
| median rho, group `DIFFERENT` | 0.2370 | out/tables/distributions.csv | median over the 41 defined pairs in that group |
| median rho, frontier-only serving `same path` | 0.3985 | out/tables/distributions.csv | median over the 24 defined pairs, both members in the frontier tier (isolates serving from capability) |
| median rho, frontier-only serving `different path` | 0.2949 | out/tables/distributions.csv | median over the 21 defined pairs, both members in the frontier tier (isolates serving from capability) |
| median rho, answer-type stratum `binary` | 0.0280 | out/tables/distributions.csv | median over the 66 defined pairs, restricted to that stratum's 21 leaves (mean tie 0.825) |
| median rho, answer-type stratum `categorical` | 0.4287 | out/tables/distributions.csv | median over the 55 defined pairs, restricted to that stratum's 6 leaves (mean tie 0.625) |
| median rho, answer-type stratum `multi_part` | 0.0000 | out/tables/distributions.csv | median over the 55 defined pairs, restricted to that stratum's 3 leaves (mean tie 0.472) |
| median rho, answer-type stratum `numeric` | 0.4443 | out/tables/distributions.csv | median over the 66 defined pairs, restricted to that stratum's 27 leaves (mean tie 0.852) |

## Stage 2 - ceiling, transfer, description, robustness

| Figure | Value | File | Computation |
|---|---|---|---|
| median split-half r_half | 0.8133 | out/tables/split_half_reliability.csv | median over 12 models of Spearman(half-A leaf vector, half-B leaf vector), runs split by run_idx % 2, scored by the benchmark's own engine/scorer.py |
| median split-half r_full (Spearman-Brown) | 0.8970 | out/tables/split_half_reliability.csv | 2r/(1+r) applied per model, then the median |
| ceiling decision row | high | analysis/stage2.py | cuts at 0.40 and 0.70 on median r_full, fixed in DESIGN-stage2.md |
| disattenuated median rho | 0.3272 | out/tables/disattenuated_pairs.csv | median of rho_observed / sqrt(r_full_A * r_full_B), computed PER PAIR then summarised |
| pairs whose correction exceeded 1.0 | 0 | out/tables/disattenuated_pairs.csv | count of non-empty note column |
| observed as a share of the ceiling | 33.0% | out/tables/distributions.csv | 100 * observed median rho / median r_full |
| repeated-split median r_full | 0.8992 | analysis/splithalf.py | 40 random partitions of each cell's runs; median of the per-split medians |
| repeated-split 95% spread | 0.8836 to 0.9249 | analysis/splithalf.py | 2.5th and 97.5th percentiles of the per-split medians |
| transfer at k=5, frontier-only | 0.6000 | out/tables/transfer.csv | median over 90 ordered pairs of \|A top-5 within B top-10\| / \|A top-5\|, k truncated to non-zero leaves |
| chance baseline at k=5, frontier-only | 0.1754 | out/tables/transfer.csv | median per-pair effective \|B top-2k\| / active subset size |
| transfer at k=5, all 12 | 0.6000 | out/tables/transfer.csv | median over 132 ordered pairs of \|A top-5 within B top-10\| / \|A top-5\|, k truncated to non-zero leaves |
| chance baseline at k=5, all 12 | 0.1754 | out/tables/transfer.csv | median per-pair effective \|B top-2k\| / active subset size |
| transfer at k=10, frontier-only | 0.5000 | out/tables/transfer.csv | median over 90 ordered pairs of \|A top-10 within B top-20\| / \|A top-10\|, k truncated to non-zero leaves |
| chance baseline at k=10, frontier-only | 0.2281 | out/tables/transfer.csv | median per-pair effective \|B top-2k\| / active subset size |
| transfer at k=10, all 12 | 0.5000 | out/tables/transfer.csv | median over 132 ordered pairs of \|A top-10 within B top-20\| / \|A top-10\|, k truncated to non-zero leaves |
| chance baseline at k=10, all 12 | 0.2544 | out/tables/transfer.csv | median per-pair effective \|B top-2k\| / active subset size |
| transfer at k=20, frontier-only | 0.5000 | out/tables/transfer.csv | median over 90 ordered pairs of \|A top-20 within B top-40\| / \|A top-20\|, k truncated to non-zero leaves |
| chance baseline at k=20, frontier-only | 0.2281 | out/tables/transfer.csv | median per-pair effective \|B top-2k\| / active subset size |
| transfer at k=20, all 12 | 0.5000 | out/tables/transfer.csv | median over 132 ordered pairs of \|A top-20 within B top-40\| / \|A top-20\|, k truncated to non-zero leaves |
| chance baseline at k=20, all 12 | 0.2544 | out/tables/transfer.csv | median per-pair effective \|B top-2k\| / active subset size |
| median worst-category-to-mean ratio | 4.9606 | out/tables/worst_category_ratio.csv | per model, worst estimable category rate / aggregate wobble; then the median |
| Spearman(mean wobble, worst/mean ratio) | -0.7063 | out/tables/worst_category_ratio.csv | over 12 models -- SHARES A DENOMINATOR, see next row |
| Spearman(mean wobble, worst-category wobble) | 0.4000 | out/tables/worst_category_ratio.csv | the same question without the shared denominator, over 12 models |
| predictor model R^2 | 0.2078 | out/tables/predictor_model.csv | OLS of per-leaf mean wobble on answer type + n_items + clause length, n=60 leaves |
| predictor model adjusted R^2 | 0.1345 | out/tables/predictor_model.csv | R^2 penalised for the parameter count |
| adj R^2 gain from adding category | 0.2210 | out/tables/predictor_model.csv | adj R^2(answer type + size + category) - adj R^2(answer type + size) |
| adj R^2 gain from adding answer type | 0.1128 | out/tables/predictor_model.csv | adj R^2(size + category + answer type) - adj R^2(size + category) |
| Spearman(leaf mean wobble, leaf mean accuracy) | -0.5516 | out/tables/leaf_wobble_vs_accuracy.csv | over n=60 leaves, each averaged across the models where it is defined |
| high-accuracy AND high-wobble leaves | 0 | out/tables/leaf_wobble_vs_accuracy.csv | count with mean accuracy >= 0.9 AND mean wobble >= 0.3 (thresholds fixed in DESIGN-stage2.md) |
| leaves with mean accuracy >= 0.90 | 35 | out/tables/leaf_wobble_vs_accuracy.csv | count; their maximum wobble is the next row |
| max wobble among high-accuracy leaves | 0.1667 | out/tables/leaf_wobble_vs_accuracy.csv | shows where the pre-registered quadrant boundary sits |
| bootstrap median rho | 0.2963 | analysis/robustness.py | 2000 leaf-resampled replicates, fixed seed |
| bootstrap 95% CI | 0.1144 to 0.4584 | analysis/robustness.py | 2.5th and 97.5th percentiles of the replicate medians |
| largest leave-one-model-out shift | +0.0341 | out/tables/leave_one_out.csv | dropping `gemma3-1b`; 12 recomputations |
| Spearman(item-weighted, leaf-equal ordering) | 0.9790 | out/tables/weighting_sensitivity.csv | over 12 models -- does the weighting choice reorder capability? |
| annotation sample size | 19 leaves / 154 items | out/annotation/sample.csv | stratified 20% of leaves by (category x answer type), fixed seed |

## Stage 3 - conservative ratios, the fold decomposition, the empty zone

| Figure | Value | File | Computation |
|---|---|---|---|
| median worst-to-mean ratio, point estimates | 4.9606 | out/tables/conservative_ratio_min3.csv | median over 12 models of (worst estimable category rate / aggregate wobble) |
| median worst-to-mean ratio, CONSERVATIVE | 1.4675 | out/tables/conservative_ratio_min3.csv | median of (largest Wilson lower bound over categories / Wilson upper bound of the mean); selection-robust, so not exposed to the winner's curse |
| models above 2x, point estimates | 12/12 | out/tables/conservative_ratio_min3.csv | count of models whose point ratio exceeds 2 |
| models above 2x, conservative | 4/12 | out/tables/conservative_ratio_min3.csv | count of models whose conservative ratio exceeds 2 |
| median conservative ratio, 5-leaf floor | 0.7399 | out/tables/conservative_ratio_min5.csv | same computation with categories of fewer than 5 leaves excluded (removes exit_waterfall) |
| models above 2x, conservative, 5-leaf floor | 0/12 | out/tables/conservative_ratio_min5.csv | count at the stricter estimability floor |
| worst-on-mean slope (point_rate, all 12 models) | 1.6036 | out/tables/worst_on_mean_regression.csv | OLS of worst-category wobble on mean wobble over n=12 models; 95% CI 0.9262 to 2.2810, R2 0.6828 |
| worst-on-mean slope (point_rate, frontier only) | -0.6356 | out/tables/worst_on_mean_regression.csv | OLS of worst-category wobble on mean wobble over n=10 models; 95% CI -6.9122 to 5.6409, R2 0.0049 |
| worst-on-mean slope (robust_lo, all 12 models) | 1.6948 | out/tables/worst_on_mean_regression.csv | OLS of worst-category wobble on mean wobble over n=12 models; 95% CI 1.3051 to 2.0845, R2 0.8790 |
| worst-on-mean slope (robust_lo, frontier only) | -0.0784 | out/tables/worst_on_mean_regression.csv | OLS of worst-category wobble on mean wobble over n=10 models; 95% CI -3.2029 to 3.0461, R2 0.0003 |
| worst-on-mean intercept (all 12 models) | 0.2448 | out/tables/worst_on_mean_regression.csv | the term that makes the RATIO grow as mean wobble goes to zero; 95% CI 0.1348 to 0.3548 |
| rho(leaf wobble, leaf accuracy), observed | -0.5516 | out/tables/fold_decomposition.csv | Spearman over 60 leaves; reproduces the stage-2 value exactly |
| rho(residual, accuracy), calibrated model | 0.0875 | out/tables/fold_decomposition.csv | residual after subtracting the per-item-p prediction whose always-wrong flip rate is estimated LEAVE-ONE-LEAF-OUT; the primary answer to 'is it mechanical' |
| rho(residual, accuracy), lower-bound model | -0.4990 | out/tables/fold_decomposition.csv | residual after subtracting 1 - p^n - (1-p)^n; parameter-free, no definitional component |
| rho(residual, accuracy), upper-bound model | 0.6049 | out/tables/fold_decomposition.csv | residual after subtracting 1 - p^n |
| quadratic term, wobble ~ accuracy + accuracy^2 | 1.7400 | out/tables/fold_decomposition.csv | positive, so NOT folded; 95% CI 0.8437 to 2.6363; accuracy range covered 0.444-1.000 |
| flip rate among always-wrong items | 0.2565 | out/tables/p_bucket_flip_rates.csv | 129 of 503 items at p=0 flip; the lower-bound model predicts 0 and the upper-bound model predicts 1, so this locates reality between them |
| item-measurements pooled | 5632 | out/tables/item_p_distribution.csv | 12 models x 60 leaves, items with at least one valid run across every scorable field |
| share of items at exactly p = 1 | 0.8333 | out/tables/item_p_distribution.csv | answered correctly on every run |
| share of items at exactly p = 0 | 0.0893 | out/tables/item_p_distribution.csv | answered incorrectly on every run |
| share of items with 0.3 <= p <= 0.7 | 0.0195 | out/tables/item_p_distribution.csv | the only band where an item can flip while its majority answer stays correct |
| leaves at accuracy >= 0.9 | 35 | out/tables/accuracy_decile_frontier.csv | count of leaves in the top accuracy region |
| max OBSERVED wobble at accuracy >= 0.9 | 0.1667 | out/tables/accuracy_decile_frontier.csv | the empirical frontier in that region |
| max STRUCTURALLY REACHABLE wobble at accuracy >= 0.9 | 0.1154 | out/tables/accuracy_decile_frontier.csv | the most those leaves' item structure could produce, against a threshold of 0.3 -- so the region was unreachable before any model was run |
| items in the blind annotation pack | 154 | out/annotation/blind_pack.csv | 19 leaves, labels withheld, order randomised under seed 20260729 |
| annotation agreement | NOT RUN | out/annotation/agreement_result.json | the sitting has not happened; the scorer refuses to report a number on an unfilled sheet rather than scoring empty against empty |

