# Answer-space classification (brief 5f)

Arm: **legacy (temperature 0.7)**. 60 leaves. 55 classified mechanically from the leaf's own `TASK["fields"]`, 5 by judgement (each justified below and re-listed in the report's question 10).

Counts: **binary** 22 · **categorical** 6 · **multi_part** 3 · **numeric** 29

| Leaf | Family | Answer type | Basis | Justification | Real oracle values |
|---|---|---|---|---|---|
| `acceleration_trigger` | founder_equity | **binary** | mechanical | TASK field type is `enum` with 2 declared values: single-trigger, double-trigger. | double-trigger · double-trigger · double-trigger |
| `cliff_present` | founder_equity | **binary** | mechanical | TASK field type is `enum` with 2 declared values: yes, no. | yes · yes · yes |
| `convert_vs_preference_decision` | exit_waterfall | **binary** | mechanical | TASK field type is `enum` with 2 declared values: convert, take-preference. | convert · take-preference |
| `dividend_cumulative` | priced_equity | **binary** | mechanical | TASK field type is `enum` with 2 declared values: cumulative, non-cumulative. | cumulative · cumulative · cumulative |
| `drag_along` | rights_governance | **binary** | mechanical | TASK field type is `enum` with 2 declared values: yes, no. | yes · yes · yes |
| `flag_full_ratchet` | risk_flag | **binary** | mechanical | TASK field type is `enum` with 2 declared values: yes, no. | yes · yes · yes |
| `flag_internal_inconsistency` | risk_flag | **binary** | mechanical | TASK field type is `bool` (two states). | False · False · True |
| `flag_missing_pro_rata` | risk_flag | **binary** | mechanical | TASK field type is `bool` (two states). | True · True · False |
| `flag_offmarket_liqpref` | risk_flag | **binary** | mechanical | TASK field type is `enum` with 2 declared values: yes, no. | yes · yes · yes |
| `flag_uncapped_participation` | risk_flag | **binary** | mechanical | TASK field type is `enum` with 2 declared values: yes, no. | yes · yes · yes |
| `fully_diluted_basis` | cap_table | **binary** | mechanical | TASK field type is `enum` with 2 declared values: fully-diluted, issued-outstanding. | fully-diluted · fully-diluted · fully-diluted |
| `information_rights` | rights_governance | **binary** | mechanical | TASK field type is `enum` with 2 declared values: yes, no. | yes · yes · yes |
| `pre_vs_post_money` | priced_equity | **binary** | mechanical | TASK field type is `enum` with 2 declared values: pre-money, post-money. | pre-money · pre-money · pre-money |
| `preference_seniority` | priced_equity | **binary** | mechanical | TASK field type is `enum` with 2 declared values: pari-passu, stacked. | stacked · stacked · stacked |
| `pro_rata_rights` | rights_governance | **binary** | mechanical | TASK field type is `enum` with 2 declared values: yes, no. | yes · yes · yes |
| `protective_provisions` | rights_governance | **binary** | mechanical | TASK field type is `enum` with 2 declared values: yes, no. | yes · yes · yes |
| `redemption_rights` | priced_equity | **binary** | mechanical | TASK field type is `enum` with 2 declared values: yes, no. | yes · yes · yes |
| `rofr_cosale` | rights_governance | **binary** | mechanical | TASK field type is `enum` with 2 declared values: yes, no. | yes · yes · yes |
| `safe_mfn_present` | convertibles | **binary** | mechanical | TASK field type is `enum` with 2 declared values: yes, no. | yes · yes · yes |
| `safe_pre_post` | convertibles | **binary** | mechanical | TASK field type is `enum` with 2 declared values: post-money, pre-money. | post-money · post-money · post-money |
| `safe_pro_rata_side_letter` | convertibles | **binary** | mechanical | TASK field type is `enum` with 2 declared values: yes, no. | yes · yes · yes |
| `vesting_acceleration` | rights_governance | **binary** | mechanical | TASK field type is `enum` with 2 declared values: yes, no. | yes · yes · yes |
| `antidilution_base` | priced_equity | **categorical** | mechanical | TASK field type is `enum` with 3 declared values: broad-based, narrow-based, n/a. | broad-based · broad-based · broad-based |
| `antidilution_type` | priced_equity | **categorical** | mechanical | TASK field type is `enum` with 5 declared values: full-ratchet, weighted-average, broad-based, narrow-based, none. | weighted-average · full-ratchet · weighted-average |
| `liquidation_preference_multiple` | priced_equity | **categorical** | mechanical | TASK field type is `enum` with 5 declared values: non-participating, 1x, 2x, 3x, other. | 1x · 1x · 1x |
| `participation_type` | priced_equity | **categorical** | mechanical | TASK field type is `enum` with 3 declared values: participating, non-participating, capped. | non-participating · non-participating · participating |
| `safe_cap_vs_discount_applies` | convertibles | **categorical** | mechanical | TASK field type is `enum` with 3 declared values: cap, discount, both-mfn. | discount · both-mfn · both-mfn |
| `securities_exemption` | regulatory | **categorical** | mechanical | TASK field type is `enum` with 5 declared values: 506b, 506c, 504, reg-a, other. | 506b · 506b · 506b |
| `s1_risk_factors` | regulatory | **multi_part** | judgement | declared type `string`; the answer is a sentence-length heading reproduced as a unit. | Our limited operating history makes it difficult to evaluate our curre · If we do not respond appropriately, the evolution of the automotive in · Fluctuating economic conditions make it difficult to predict revenue f |
| `s1_use_of_proceeds` | regulatory | **multi_part** | judgement | declared type `string`; the answer is an open-vocabulary multi-word span scored as a unit ('working capital and general corporate purposes') -- no closed option set and no scalar, and the known failure mode is returning a longer correct-in-substance span. | general corporate purposes · research and development activities · advance our current liver programs |
| `vesting_schedule` | founder_equity | **multi_part** | judgement | declared type `string`; every oracle value carries TWO components that must both be right (term and cliff: '4yr/1yr-cliff', '1.5yr/no-cliff'). | 4yr/1yr-cliff · 4yr/1yr-cliff · 1.5yr/no-cliff |
| `auto_conversion_trigger` | priced_equity | **numeric** | mechanical | TASK field type is `number`. | 30000000 · 30000000 · 100000000 |
| `board_seats_investor` | rights_governance | **numeric** | mechanical | TASK field type is `number`. | 3 · 1 · 3 |
| `conversion_ratio` | priced_equity | **numeric** | mechanical | TASK field type is `number`. | 1 · 2 · 100 |
| `current_ownership_pct` | cap_table | **numeric** | mechanical | TASK field type is `number`. | 6.0 · 11.0 · 2.4 |
| `dividend_rate_pct` | priced_equity | **numeric** | mechanical | TASK field type is `number`. | 6 · 8.0 · 10 |
| `employee_pool_pct` | cap_table | **numeric** | mechanical | TASK field type is `number`. | 9.5 |
| `exercise_window` | founder_equity | **numeric** | judgement | declared type `string`; oracle values are a single quantity with one unit (30/85/90/90/180 days) -- one ordered scalar, not a closed option set. | 30 days · 85 days · 90 days |
| `financial_statement_qa` | regulatory | **numeric** | mechanical | TASK field type is `number`. | 1123118 · 17541 · 22786 |
| `form_d_fields` | regulatory | **numeric** | mechanical | TASK field type is `number`. | 2,366,532 · 70,227,931.85 |
| `founder_ownership_pct` | cap_table | **numeric** | mechanical | TASK field type is `number`. | 6.0 · 8.6 · 2.4 |
| `investor_ownership_pct` | cap_table | **numeric** | mechanical | TASK field type is `number`. | 16.3 · 11.0 · 5.3 |
| `liquidation_waterfall_payout` | exit_waterfall | **numeric** | mechanical | TASK field type is `number`. | 0.51 · 0.42 · 0.39 |
| `multi_round_stacked_dilution` | cap_table | **numeric** | mechanical | TASK field type is `number`. | 32.89 · 2.09 · 28.82 |
| `note_discount` | convertibles | **numeric** | mechanical | TASK field type is `number`. | 20.0 · 25.0 · 50.0 |
| `note_interest_rate` | convertibles | **numeric** | mechanical | TASK field type is `number`. | 0.28 · 10.0 · 10.0 |
| `note_maturity_date` | convertibles | **numeric** | judgement | declared type `date`; oracle values are single ISO dates (2005-03-31, 2026-12-31) -- one ordered scalar from an unbounded space, canonicalised by engine/normalize.py, so it behaves like a numeric extraction rather than a choice among options. | 2005-03-31 · 2015-03-04 · 2026-12-31 |
| `note_principal` | convertibles | **numeric** | mechanical | TASK field type is `number`. | 400000 · 17364375 · 12500 |
| `note_qualified_financing_threshold` | convertibles | **numeric** | mechanical | TASK field type is `number`. | 40000000 · 10000000 |
| `note_valuation_cap` | convertibles | **numeric** | mechanical | TASK field type is `number`. | 125000000 · 25000000 · 90000000 |
| `option_pool_shuffle` | cap_table | **numeric** | mechanical | TASK field type is `number`. | 0.909 · 0.24 · 0.6956 |
| `option_strike_409a` | founder_equity | **numeric** | mechanical | TASK field type is `number`. | 0.03 · 0.25 · 0.61 |
| `participation_cap` | priced_equity | **numeric** | mechanical | TASK field type is `number`. | 3.5 · 3 · 3 |
| `per_investor_allocation` | priced_equity | **numeric** | mechanical | TASK field type is `number`. | 4000000 · 9418200 · 1650000 |
| `post_money_valuation` | priced_equity | **numeric** | mechanical | TASK field type is `number`. | 68000000 · 275000000 · 5000000 |
| `preference_stack_payout` | exit_waterfall | **numeric** | mechanical | TASK field type is `number`. | 58.9 · 19.7 |
| `price_per_share` | priced_equity | **numeric** | mechanical | TASK field type is `number`. | 3.63 · 1000.0 · 1.3 |
| `round_size` | priced_equity | **numeric** | mechanical | TASK field type is `number`. | 21272455 · 5000000 · 3728926 |
| `safe_discount_rate` | convertibles | **numeric** | mechanical | TASK field type is `number`. | 20 · 20 · 20 |
| `safe_valuation_cap` | convertibles | **numeric** | mechanical | TASK field type is `number`. | 15000000 · 20000000 · 30000000 |
