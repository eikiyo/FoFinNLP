# AUDIT_CONTAMINATION.md — the §0 gate

> STATUS: DONE · Paper A · run 2026-07-29 · arm: legacy (temperature 0.7) · probity v1.3.1

## The question

`out/annotation/oracle_audit.json` flags **36 of 470 items**
across 60 tasks, in two modes:

| failure mode | items |
|---|---|
| validating quote not inside the window the model is shown | 34 |
| validating quote NOT found in the source document | 5 |

An item whose answer sits outside the window the model is shown cannot be answered from that
window, whatever the model then does. If wobble is systematically higher on those items, every
headline number in this paper is partly a measurement of a defect in our own resource rather than
a property of the models. Whether the missing evidence is what *destabilises* them is a separate
question, registered as a falsifiable prediction and tested by re-windowing; it failed, and the
paper reports the association as correlational only. This file ships with the artifact, so it
states that the way the paper does rather than asserting a mechanism the experiment did not
support.

Flagged items by task:

| task | items flagged |
|---|---|
| current_ownership_pct | 9 |
| multi_round_stacked_dilution | 5 |
| investor_ownership_pct | 4 |
| liquidation_waterfall_payout | 4 |
| participation_type | 3 |
| founder_ownership_pct | 3 |
| option_pool_shuffle | 3 |
| convert_vs_preference_decision | 2 |
| round_size | 1 |
| employee_pool_pct | 1 |
| securities_exemption | 1 |

## Controls, run before anything was read

- identity PASS - re-counting all items through the partition code reproduces all 720 published cells exactly (wobble and majority accuracy)
- partition PASS - clean + flagged + 84 author-excluded = published counts in all 720 cells
- join: **36 flagged ids matched** to their positional index across
  11 tasks, with 60 tasks
  audited in total. A zero-overlap join is fatal in this module rather than a null result: a
  partition that matched nothing would report "no contamination" for the most reassuring possible
  reason, which is that it compared nothing.
- reliability PASS - the item-partition path reproduces all 12 published split-half values exactly, so the clean-only figure differs only by the item set

The identity check matters more than it looks. It runs the *same* counting code that produces the
clean-only numbers over the *whole* item set, and requires it to reproduce all 720 published cells
exactly, in wobble and in majority accuracy. A partition bug would otherwise be indistinguishable
from a finding.

## Result

Wobble on flagged items is **HIGHER** than on clean items: 0.2546 (110/432) versus 0.0874 (447/5116). The difference is **+0.1673**, Wilson 95% interval [0.1276, 0.2110], which EXCLUDES zero. 8 of 12 model configurations show a difference excluding zero on their own.

**The clean-only numbers become the paper's headline numbers.** All-item figures move to the appendix. Section 2 reports the audit, the exclusion, and the delta, in the main text.

### Per configuration

| configuration | flagged wobble | 95% CI | n | clean wobble | 95% CI | n | difference | 95% CI | excludes 0 |
|---|---|---|---|---|---|---|---|---|---|
| gemma3-1b | 0.9167 | [0.7817, 0.9713] | 36 | 0.3803 | [0.3354, 0.4273] | 426 | 0.5364 | [0.3935, 0.6070] | yes |
| deepseek-v4f | 0.1111 | [0.0441, 0.2531] | 36 | 0.0539 | [0.0362, 0.0795] | 427 | 0.0572 | [-0.0145, 0.2004] | no |
| deepseek-v4p | 0.0278 | [0.0049, 0.1417] | 36 | 0.0469 | [0.0306, 0.0714] | 426 | -0.0192 | [-0.0526, 0.0959] | no |
| gemma4-31b-or | 0.2222 | [0.1172, 0.3808] | 36 | 0.0141 | [0.0065, 0.0304] | 426 | 0.2081 | [0.1018, 0.3669] | yes |
| mistral-large-or | 0.0833 | [0.0287, 0.2183] | 36 | 0.0281 | [0.0161, 0.0485] | 427 | 0.0552 | [-0.0030, 0.1907] | no |
| minimax-m2.5-or | 0.1389 | [0.0608, 0.2866] | 36 | 0.0679 | [0.0477, 0.0958] | 427 | 0.0710 | [-0.0119, 0.2201] | no |
| llama3.3-70b-or | 0.1944 | [0.0975, 0.3503] | 36 | 0.0188 | [0.0095, 0.0366] | 426 | 0.1757 | [0.0771, 0.3318] | yes |
| gemma3-1b-qat | 0.6944 | [0.5314, 0.8200] | 36 | 0.3091 | [0.2672, 0.3545] | 427 | 0.3853 | [0.2161, 0.5177] | yes |
| gemini3-flash-or | 0.0833 | [0.0287, 0.2183] | 36 | 0.0211 | [0.0112, 0.0397] | 426 | 0.0622 | [0.0046, 0.1975] | yes |
| haiku-4.5-direct | 0.1944 | [0.0975, 0.3503] | 36 | 0.0141 | [0.0065, 0.0305] | 425 | 0.1803 | [0.0820, 0.3363] | yes |
| gpt-oss-120b-or | 0.2222 | [0.1172, 0.3808] | 36 | 0.0469 | [0.0306, 0.0714] | 426 | 0.1753 | [0.0674, 0.3347] | yes |
| gpt5-mini-or | 0.1667 | [0.0787, 0.3189] | 36 | 0.0468 | [0.0305, 0.0712] | 427 | 0.1198 | [0.0285, 0.2729] | yes |
| POOLED | 0.2546 | [0.2158, 0.2977] | 432 | 0.0874 | [0.0799, 0.0954] | 5116 | 0.1673 | [0.1276, 0.2110] | yes |

The comparison assumes the two partitions are independent samples. They are not fully independent:
both come from the same runs of the same models over the same corpus. Newcombe's interval on
independent proportions is the conservative standard choice here, and the dependence is disclosed
rather than corrected away.

## Where the defect concentrates

**8 of the 60 tasks lose every item.**
The flagged items are not spread thinly across the corpus. They fall almost entirely on tasks
that are small and computational, and on those tasks they take everything:

| task | category | items | flagged | retained |
|---|---|---|---|---|
| current_ownership_pct | cap_table | 9 | 9 | 0 |
| founder_ownership_pct | cap_table | 3 | 3 | 0 |
| investor_ownership_pct | cap_table | 4 | 4 | 0 |
| employee_pool_pct | cap_table | 1 | 1 | 0 |
| option_pool_shuffle | cap_table | 3 | 3 | 0 |
| multi_round_stacked_dilution | cap_table | 5 | 5 | 0 |
| liquidation_waterfall_payout | exit_waterfall | 4 | 4 | 0 |
| convert_vs_preference_decision | exit_waterfall | 2 | 2 | 0 |
| round_size | priced_equity | 10 | 1 | 9 |
| participation_type | priced_equity | 17 | 3 | 14 |
| securities_exemption | regulatory | 10 | 1 | 9 |

Tasks per category, before and after:

| category | tasks (all) | tasks (clean) | items (all) | items (clean) |
|---|---|---|---|---|
| cap_table | 7 | 1 | 33 | 8 |
| convertibles | 12 | 12 | 95 | 95 |
| exit_waterfall | 3 | 1 | 8 | 2 |
| founder_equity | 5 | 5 | 46 | 46 |
| priced_equity | 16 | 16 | 139 | 135 |
| regulatory | 5 | 5 | 27 | 26 |
| rights_governance | 7 | 7 | 78 | 78 |
| risk_flag | 5 | 5 | 37 | 37 |

Two things follow, and both belong in the paper.

**First, the mechanism is legible.** The wiped tasks are cap-table and waterfall computations:
ownership percentages, option-pool shuffles, stacked dilution, liquidation waterfalls. Those
answers are not stated anywhere in a document. They are computed from numbers that sit in
different places in a filing, so a single windowed provision cannot contain the validating quote
by construction. The extraction tasks, where the answer is a labelled value inside one clause,
are almost untouched. This is a defect in how the corpus windows COMPUTATIONAL items, not a
scattering of clerical errors, and saying so is more useful to a successor benchmark than the
count is.

**Second, it explains the transfer result the paper was going to lead with.**
`liquidation_waterfall_payout` was in all twelve configurations' top-10 most unstable tasks. It is
one of the nine that vanish. What looked like models agreeing about which clause types are hard
was, in part, models agreeing about which items were unanswerable.

The exclusion therefore reduces the analysed corpus to
**427 items over 52 tasks**.
The benchmark still ships 463 items over
60 tasks. Those are different numbers and the paper must use
each in its own place: the resource is the larger one, the headline analysis is the smaller one.

## Delta on every headline number

| quantity | all items | clean only | delta |
|---|---|---|---|
| items in the analysis | 463 | 427 | -36 |
| tasks with at least one item in the analysis | 60 | 52 | -8 |
| model-item pairs measured | 5548 | 5116 | -432 |
| aggregate wobble: gemini3-flash-or | 0.025974 | 0.021127 | -0.004847 |
| aggregate wobble: haiku-4.5-direct | 0.028200 | 0.014118 | -0.014082 |
| aggregate wobble: gemma4-31b-or | 0.030303 | 0.014085 | -0.016219 |
| aggregate wobble: mistral-large-or | 0.032397 | 0.028103 | -0.004294 |
| aggregate wobble: llama3.3-70b-or | 0.032468 | 0.018779 | -0.013688 |
| aggregate wobble: deepseek-v4p | 0.045455 | 0.046948 | 0.001494 |
| aggregate wobble: gpt5-mini-or | 0.056156 | 0.046838 | -0.009317 |
| aggregate wobble: deepseek-v4f | 0.058315 | 0.053864 | -0.004451 |
| aggregate wobble: gpt-oss-120b-or | 0.060606 | 0.046948 | -0.013658 |
| aggregate wobble: minimax-m2.5-or | 0.073434 | 0.067916 | -0.005518 |
| aggregate wobble: gemma3-1b-qat | 0.339093 | 0.309133 | -0.029959 |
| aggregate wobble: gemma3-1b | 0.422078 | 0.380282 | -0.041796 |
| transfer k=5 frontier-only: median | 0.600000 | 0.400000 | -0.200000 |
| transfer k=5 frontier-only: chance | 0.175439 | 0.200000 | 0.024561 |
| transfer k=5 frontier-only: median_lift | 0.424561 | 0.200000 | -0.224561 |
| transfer k=5 frontier-only: n_truncated | 27 | 42 | 15 |
| transfer k=10 frontier-only: median | 0.500000 | 0.400000 | -0.100000 |
| transfer k=10 frontier-only: chance | 0.228070 | 0.220000 | -0.008070 |
| transfer k=10 frontier-only: median_lift | 0.280702 | 0.202222 | -0.078480 |
| transfer k=10 frontier-only: n_truncated | 84 | 90 | 6 |
| active tasks (non-zero wobble in >=1 model) | 57 | 50 | -7 |
| split-half reliability, median r_full | 0.903950 | 0.903488 | -0.000462 |
| share answered identically on all runs (1 - wobble) | 0.899603 | 0.912627 | 0.013024 |
| share answered correctly on all runs (p=1) | 0.845530 | 0.860438 | 0.014908 |
| share answered wrong on all runs (p=0) | 0.076784 | 0.062940 | -0.013845 |
| pairs in the observable band 0.3 <= p <= 0.7 | 109 | 99 | -10 |
| share in the observable band 0.3 <= p <= 0.7 | 0.019647 | 0.019351 | -0.000296 |
| pairs in the band under the half-open reading 0.3 <= p < 0.7 | 93 | 85 | -8 |
| tasks at accuracy >= 0.9 | 36 | 35 | -1 |
| max structurally reachable wobble at accuracy >= 0.9 | 0.115363 | 0.115363 | 0.000000 |
| max observed wobble at accuracy >= 0.9 | 0.166667 | 0.166667 | 0.000000 |
| wobble-accuracy rho | -0.603413 | -0.487007 | 0.116406 |
| residual rho after structural decomposition (calibrated) | 0.050330 | 0.188565 | 0.138235 |
| conservative worst-to-mean ratio, median (3-task floor) | 1.467466 | 0.600819 | -0.866647 |
| models above 2x at the bound (3-task floor) | 4 | 0 | -4 |
| conservative worst-to-mean ratio, median (5-task floor) | 0.739944 | 0.600819 | -0.139126 |
| capability gradient slope, frontier only | -0.635635 | 3.428742 | 4.064378 |
| capability gradient R2, frontier only | 0.004901 | 0.679773 | 0.674872 |

## What this does to the paper

1. **Wobble falls for every configuration but one.** 11 of 12 fall once the flagged
   items are removed, and the two 1B models fall furthest in absolute terms. The exception is
   deepseek-v4p, unchanged at +0.0001. The published aggregate wobble was measuring, in part,
   items whose answers were not in front of the model.
2. **The capability ordering survives.** The frontier/low split has the same membership on both
   readings, so the tier structure the analysis rests on is not an artefact of the defect.
3. **The transfer result weakens and must be restated.** At k=5 the median falls from
   0.600 to
   0.400 against a chance line that rises from
   0.175 to
   0.200. The lift is still positive and it is still
   the paper's one positive result, but it is roughly half the size the all-item reading gave.
   Part of what looked like shared instability across models was shared *defect*: the active task
   set shrinks from 57 to 50,
   meaning 7 tasks had no
   instability at all outside their flagged items.
4. **Reliability rises**, from 0.9039 to
   0.9035. Removing items that force guessing
   removes noise, which is the direction a real defect predicts. The same figure is obtained over
   the unreduced 57-task set, so it is the item filter and not the
   smaller task set that moves it.
5. **The worst-to-mean ratio dies harder.** At the Wilson bounds the median falls from
   1.4675 to 0.6008, and
   the count of configurations above 2x falls from 4 to
   0 at the 3-task floor. Nothing in the exclusion rescues a
   claim stage 3 had already killed.
6. **The capability-gradient row of appendix Table 4 must be rewritten, and its verdict is
   unchanged for a different reason.** On all items the frontier-only regression of worst-category wobble on mean wobble was pure noise: slope -0.6356, R2 0.0049 over n=10. On clean items it becomes a real relationship: slope 3.4287, 95% CI [1.7980, 5.0595], R2 0.6798. That interval excludes 1, so the worst category falls FASTER than the mean as configurations get more stable, which is the OPPOSITE of a widening gap. The claim needs a positive intercept to hold -- the ratio is intercept/mean + slope, so only a non-zero intercept makes it grow as the mean shrinks -- and the intercept is -0.0163, 95% CI [-0.0818, 0.0491], which contains zero. On all items the intercept was +0.3428 [0.0478, 0.6379] and EXCLUDED zero, so the all-item reading was the one that pointed, weakly, toward the claim. Verdict unchanged (NOT SUPPORTED), mechanism different: on clean items the worst-to-mean relationship is proportional, roughly 3.4x, and flat in capability rather than divergent.
7. **The wobble-accuracy concession stands.** The observed correlation weakens from
   -0.6034 to -0.4870, and the
   residual after the structural decomposition is
   +0.1886: small, and of the OPPOSITE sign to
   the observed correlation. The relationship remains structural rather than a fact about models.
8. **The observability picture is unchanged.** The share of items answered identically on all runs
   moves by under two points, and the structural ceiling at high accuracy is the same to three
   decimals. Figure 1's message does not depend on which reading is used.

## Honest limits of this gate

- The audit is **mechanical**. It checks that a label's validating quote exists in the source and
  inside the model's window. It does **not** check that the label is the right answer. A flagged
  item is an item whose provenance cannot be verified, not an item known to be mislabelled.
- 49 of 60 tasks have no flagged
  items. That is the audit finding nothing there, which is not the same as those tasks being
  verified correct by a human.
- The flagged sample is small (432 model-item pairs pooled), so a per-configuration
  interval is wide. The pooled interval is the one that carries the verdict.
