# PREREG_2a.md — the prospective test, registered before any call is made

> STATUS: REGISTERED · written 2026-07-29 · **nothing has been run** · launching requires explicit approval

This file is written **before** any new leaf is built and before any new model call is made. It
exists so that the outcome cannot be reinterpreted after it is known. Both outcomes are committed
below, in writing, with equal prominence.

---

## Why this test, and why it is not confirmatory data collection

Building more `exit_waterfall` leaves would be collecting data in the exact place an effect was
already observed, after observing it. That is confirmatory and a reviewer is entitled to say so.
**It is not what this is.**

Step 1c changed what this test is *for*, and made it necessary rather than optional. Stage 2 found
zero leaves at accuracy ≥ 0.9 and wobble ≥ 0.3, and refused to move the threshold. Step 1c now
shows that region was **unreachable by construction**: the pooled per-item correct rate is strongly
bimodal (83.3% of the 5,632 item-measurements sit at exactly p = 1, 8.9% at exactly p = 0, and only
2.0% anywhere in the band 0.3 ≤ p ≤ 0.7), and across the 35 leaves at accuracy ≥ 0.9 the most
wobble the item structure could produce is 0.115 against a threshold of 0.30.

So the current corpus cannot distinguish two very different claims:

- **models never produce clauses they answer correctly yet unstably**, versus
- **this item pool contains no clause that could express one.**

Only new items designed against the mechanism can separate them. That is a test of a mechanism
identified *before* the data is collected, not an expansion of a category that looked bad.

---

## The hypothesis, registered

> **H1.** Clause types exist on which frontier models are highly accurate (≥ 0.9 majority accuracy)
> and still unstable (≥ 0.2 wobble). They can be constructed deliberately by targeting item
> properties that put a model's per-run correct rate in the interior of [0, 1] while keeping its
> majority answer right.

The wobble threshold is **0.2**, not stage 2's 0.3. Stated plainly: this is a *relaxation* of the
stage-2 threshold, declared in advance and never to be re-tuned afterwards. The justification is
mechanical rather than convenient — at n = 20 runs an item needs a per-run correct rate below
roughly 0.99 to flip at all, and 0.2 leaf-level wobble already means one item in five is unstable,
which is far past a level any practitioner would accept in a document that decides equity. If the
new leaves land between 0.2 and 0.3, that is reported as a **partial** result against the stage-2
threshold, not silently as a success.

## What is targeted: item properties, not a category

Explicitly **not** `exit_waterfall`, and not any category chosen because it currently looks worst.
The targets are the item properties that step 1b/1c identify as producing interior per-run correct
rates:

1. **A multi-step computation rather than a lookup.** The answer must be derived from two or more
   numbers in the clause (e.g. a conversion price from a cap and a discount), not read off it.
   Single-lookup items dominate the p = 1 spike.
2. **A plausible near-miss.** The clause must admit a specific, defensible wrong answer a competent
   reader could produce — pre-money vs post-money, gross vs net proceeds, as-converted vs
   as-issued. Items where the only alternative to the right answer is nonsense sit at p = 1.
3. **The operative quantity appearing more than once in different roles**, so that selecting the
   correct occurrence is itself a step.

These properties are recorded per leaf at build time, before any model is run, so the analysis can
report which property produced which behaviour.

## Design, fixed in advance

- **4 to 6 new leaves.** No more, no fewer, decided now.
- Documents sourced through the existing `source.py` path. Same oracle protocol as the existing 60:
  a human separates the question from the answer, undeterminable items are **excluded, never
  guessed**, and quote provenance is recorded.
- **Full lineup: 12 models × new leaves × 20 runs at temperature 0.7**, through the existing
  harness and the existing scorer. Not a side script. The new cells must be indistinguishable in
  provenance from the existing 720, and the same `manifest_*.json` files must be written.
- The new leaves enter the public benchmark permanently. They are built to that standard or not
  at all.

## Cost estimate, computed from the corpus rather than guessed

The existing arm holds 470 oracle items across 60 leaves (mean 7.83 per leaf, median 7, range
1–19) and 112,800 recorded runs.

| Scale | Calls = leaves × 12 models × items × 20 runs |
|---|---|
| 4 leaves, at the median 7 items | **6,720** |
| 6 leaves, at the median 7 items | **10,080** |
| 6 leaves, at the mean 7.83 items | **11,275** |

So the launch is a **6,700–11,300 call** job, roughly 6–10% of the runs already in the arm. Per-call
cost is not stated here because it depends on document length and on the routed/direct split, and
an invented dollar figure would be exactly the kind of authored-not-measured number this project
logs as a defect. **The launch procedure is therefore: build the leaves, run ONE model × ONE leaf,
read the actual token counts off the manifest, multiply, and report that figure to Eikiyo before
the remaining 11 models are launched.**

## Both outcomes, committed now, with equal prominence

| Outcome | What the paper says |
|---|---|
| **The new leaves land in the high-accuracy high-wobble zone** | Concrete deployment examples exist. This becomes the paper's strongest section: named clause types, with the item properties that produce them, that a practitioner can check against their own pipeline |
| **They do not** | A deliberate, mechanism-targeted attempt to construct silently-unstable-but-correct items **failed**. In this domain instability and error co-occur: a model that flips is usually also a model that is wrong, and the deployment risk is therefore more visible than feared. This is a clean, quotable negative result and it gets the same page budget and the same prominence as the positive one would have |

**This commitment is the point of the file.** The second outcome will be reported as a result, not
as an appendix note, not as "we also tried", and not omitted. It is arguably the more useful
finding for a practitioner, because it says the failure mode is detectable by checking correctness.

A third outcome is possible and is also committed: the new leaves land **between** 0.2 and 0.3
wobble at high accuracy. That is reported as partial support, with the stage-2 threshold of 0.3
quoted beside it so the reader can apply the stricter bar themselves.

## The hard stop

If sourcing and oracle construction are **not complete by 2026-08-02**, this is abandoned and the
paper is written on the existing 60 leaves.

Rushed leaves enter the public benchmark permanently and every later paper inherits their
provenance. **The benchmark's credibility outranks this submission.** If the deadline is missed it
is said plainly in the stage-4 report, and the paper reports the step-1c limitation instead — which
is a legitimate finding on its own and needs no new data.

## What will NOT be run

- No new `exit_waterfall` leaves.
- No expansion of any category because it currently looks worst.
- No re-run of existing leaves at new settings — that is Paper B territory and breaches the arm rule.
- No added models. Twelve is enough; each addition re-opens every table in the paper.
