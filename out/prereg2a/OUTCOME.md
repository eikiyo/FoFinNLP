# OUTCOME_2a.md — the prospective test could not be built, and why that is itself the result

> STATUS: RESOLVED · 2026-07-29 · **no model was run · no document was fetched · $0 spent · probity untouched**

`PREREG_2a.md` committed, in advance and in writing, to reporting a negative outcome as prominently
as a positive one. This is that report. It arrives four days before the 2026-08-02 hard stop.

**Result: the target items cannot be constructed from the existing corpus.** Not "they were built
and the models were stable on them" — the items do not exist to build. That is a different and
more interesting finding, and it explains step 1c.

---

## What was tested

The pre-registration targeted **item properties**, not a category: a multi-step computation rather
than a lookup, a plausible near-miss, and an operative quantity appearing in more than one role.
Three concrete leaf designs met that specification. All three were mined against the 949 unique SEC
documents already on disk.

### Candidate A — preference amount per share (multiple × Original Issue Price)

Genuinely new: `liquidation_preference_multiple` exists as an enum *extraction*; computing the
resulting *amount* does not. Mining found 17 documents stating both a multiple and a dollar price.

Then the gates ran, and this is where the result is:

| Stage | Surviving |
|---|---|
| documents on disk | 949 |
| state both a multiple and a dollar Original Issue Price | 17 |
| after multi-value ambiguity exclusion (one charter stated **7** different Original Issue Prices) | 8 |
| after duplicate-provision exclusion | 7 |
| **after semantic-role checking** | **1** |

**Six of the seven were the wrong kind of clause.** The phrase "N times the Original Issue Price"
appears constantly in these charters, but almost never as an amount payable:

| document | what the clause actually is |
|---|---|
| 1556898 | "…have received two times the Original Issue Price **(the 'Participation Cap')**" |
| 1722271 | "…shall exceed three times the Original Issue Price **(the 'Maximum Participation Amount')**" |
| 1062195 | a participation ceiling, and its amount explicitly "**include[s] … any dividends paid thereon**" |
| 1490660 | a conditional threshold that switches holders to pro-rata treatment |
| 1625278 | an **IPO conversion condition** — "if the initial public offering price is less than two times…" |
| v015342 | a **Qualified IPO** price threshold |

`participation_cap` **is already a leaf in this benchmark.** Six of seven candidates would have
rebuilt an existing leaf under a wrong label — measuring participation caps while calling the
result a liquidation preference. Only a reading of the clause text catches that; every numeric
check passed.

The single survivor (1780201) is a genuine preference, and still unusable: its amount is
**two-branch and date-dependent** — "two times the original issue price … until August 28, 2022 **or**
… the original issue price plus 15% per annum accruing … thereafter". There is no single correct
answer without fixing a date.

### Candidate B — conversion price from a valuation cap and a discount

**Zero documents** carry a valuation cap, a discount rate and a price in the same window. 23 state
a discount alone; 14 state a discount and a price with no cap. The canonical cap-versus-discount
computation is not present in this corpus.

### Candidate E — note principal plus accrued interest

13 documents place a principal and a rate in one window, before any role or ambiguity gating, and
the extractions are visibly unclean (a "principal" of 13.5, a truncated "118,"). It would not reach
a usable leaf, and it needs a term or maturity date that is usually stated elsewhere in the filing.

---

## Which pre-registered outcome this is

Neither, exactly — and the pre-registration should have anticipated a third. It committed to
"the new leaves land in the zone" versus "a deliberate attempt to construct them failed". What
happened is one step earlier: **the attempt failed at construction, not at measurement.** No model
was ever asked anything.

That distinction must be stated honestly in the paper. We did **not** demonstrate that
silently-unstable-but-correct clauses fail to exist. We demonstrated that **this corpus cannot
express the items that would test for them**, which is a claim about source documents, not models.

## Why this is worth a paragraph in the paper

It explains step 1c rather than merely restating it. The item pool is bimodal at p = 1 — 83.3% of
measurements are answered correctly on every run — and the reason is now visible in the source
material: **venture-financing charters state their operative facts as single, explicitly-labelled
values.** "Original Issue Price shall mean $0.25." "The Series B Preferred shall not be redeemable."
The multi-step arithmetic that would place a model in the interior of the correct-rate distribution
is not in the documents; it lives in the spreadsheets analysts build *from* the documents.

So the honest limitation sentence, which is stronger than the one step 1c alone supported:

> We did not observe clauses that models answer correctly yet unstably. Our item pool could not
> have contained them: the documents state operative terms as single labelled values, and a
> deliberate search for multi-step computable items across 949 filings yielded one usable
> candidate, itself date-dependent.

## Recommendation

**Abandon 2a and write on the existing 60 leaves.** Reasons, in order:

1. The items do not exist in the corpus. This is not a budget or a scheduling problem.
2. Sourcing *new* documents to order would put fresh leaves into a permanently public benchmark
   four days before the sourcing deadline. The pre-registration is explicit that the benchmark's
   credibility outranks this submission.
3. Re-specifying the target property now — after seeing that the first specification failed — is
   exactly what pre-registration exists to prevent. If we want a different property, it gets a new
   pre-registration and a later paper.
4. The 13 remaining days are better spent on the annotation sitting, which blocks regardless.

**Cost of reaching this conclusion: zero API calls, zero dollars, zero new documents, and the
probity tree still clean at `v1.3.1`.** That is the pre-registration working as intended — the
expensive part was never launched, because the cheap part was run first.
