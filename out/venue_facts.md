# Venue facts — FinNLP 2026 (Paper A, step 5c)

> Every line below was fetched from a live page on **2026-07-29** and is reported with its source.
> Where a page does not state something, it is recorded as **NOT STATED** rather than inferred from
> convention. Nothing here is from memory.
>
> **Primary source:** the FinNLP 2026 workshop site — https://sigfintech.github.io/finnlp2026/
> (also listed on the ACL Member Portal). FinNLP 2026 is the **11th** workshop in the series and is
> **co-located with EMNLP 2026**.

## The facts you asked for

| # | Question | Answer | Source |
|---|---|---|---|
| 1 | Long paper page limit | **8 pages**, excluding references | FinNLP 2026 site |
| 1 | Short paper page limit | **4 pages**, excluding references | FinNLP 2026 site |
| 1 | Demo paper page limit | **4 pages**, excluding references | FinNLP 2026 site |
| 2 | Anonymous submission? | **Yes** — "All direct submissions must be anonymized." | FinNLP 2026 site |
| 2 | Anonymity *period* rules | **NOT STATED** on the workshop page. The ARR policy states submissions "remain anonymous during peer review" and that "authors are free to post and discuss non-anonymous preprints at any time" — but gives no fixed embargo window on that page | FinNLP 2026 site; https://aclrollingreview.org/anonymity |
| 3 | Identifying repo link permitted in a submission? | **NOT STATED** on either page. The workshop's Open Research Policy encourages public code release **after acceptance**, which is not the same permission | FinNLP 2026 site; ARR anonymity page |
| 4 | AI-assistance disclosure | **Required.** Generative AI tools do not qualify for authorship; their use for **writing or coding**, and its scope, must be disclosed in the **Responsible NLP Checklist**, with details in the **Acknowledgements** section | ACL / ARR call for papers |
| 5 | Template | **The ACL Template MUST be used.** Exact version number **NOT STATED** on the page | FinNLP 2026 site |
| 6 | Submission mechanics | **OpenReview** — https://openreview.net/group?id=EMNLP/2026/Workshop/FinNLP | FinNLP 2026 site |
| 6 | ARR route available? | **Yes** — "Pre-reviewed ARR commitment" for papers already reviewed via ACL Rolling Review, as an alternative to direct submission | FinNLP 2026 site |

## All deadlines (source: FinNLP 2026 site)

| Milestone | Date |
|---|---|
| Submission system opens | 2026-07-01 |
| **Direct paper submission** | **2026-08-11 (AoE)** |
| ARR commitment | 2026-08-27 (AoE) |
| Author notification | 2026-09-01 |
| Camera-ready | 2026-09-10 |
| Proceedings due to EMNLP | 2026-09-25 |
| Workshop day | 2026-10-28 |

## What this means for Paper A — three consequences that change the work

**1. Eight pages is the binding constraint, and this analysis does not fit in it.**
Stage 1 plus stage 2 have produced far more than eight pages of material. The page limit forces a
choice about what is a *finding* and what is an *appendix table*, and that choice should be made
before drafting rather than by cutting at the end. On current results the load-bearing content is:
the ceiling (step 1), the headline with its interval, the transfer number, the answer-format
contrast, and the difficulty concession. Everything else is appendix.

**2. Anonymity vs the public repository — resolve this before submitting, do not guess.**
Direct submissions must be anonymized, and the probity repository is public and identifying
(`github.com/eikiyo/probity`, tag `v1.3.1`). **Neither page states whether an identifying repo link
may appear in an anonymous submission.** Both plausible readings have real cost: linking may breach
anonymity; not linking weakens a paper whose whole argument is reproducibility. **Do not resolve
this by inference.** Either prepare an anonymised artefact (an anonymous mirror or an OpenReview
supplementary upload) as the default safe path, or email the workshop organisers and get the answer
in writing. This is a genuine open item, not a formality.

**3. The AI-disclosure requirement applies to this work directly and is not optional.**
The analysis in `paper-a/` was written with substantial AI assistance (Claude), and the requirement
explicitly covers **coding as well as writing**. That must appear in the Responsible NLP Checklist
with details in the Acknowledgements. It is straightforward to comply with and damaging to omit.

## Route choice: direct vs ARR

The direct deadline (**2026-08-11**) is **13 days** from today. The ARR commitment route (2026-08-27)
is only available for work *already reviewed* through ACL Rolling Review, so it is not a way to buy
16 more days for a paper that has not entered ARR. **Treat 2026-08-11 as the deadline.**

Against that date, the known blocking item is the annotation agreement study (`out/annotation/`),
which is prepared but not run, and which has no statistical substitute.

## Not checked

- The exact ACL template version (the page says "the ACL Template" without a version). Pull the
  current package from the ACL style-files repository at drafting time rather than reusing an old
  local copy.
- Whether the workshop has any topic-fit statement that would exclude a benchmark-methods paper.
  **NOT CHECKED** — worth one look at the call's topic list before committing to the venue.
