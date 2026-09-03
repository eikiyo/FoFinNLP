# novelty_audit.md — what already exists, and what Paper A may therefore claim

> STATUS: DONE · Paper A stage 3 step 0 · run 2026-07-29

**Method.** Five questions, not five keyword strings. Searched across arXiv, the ACL Anthology,
OpenReview and the open web. **Every record below was then resolved through the arXiv API
(`export.arxiv.org/api/query?id_list=…`) or the ACL Anthology page itself** — titles, full author
lists, dates, and the `comment`/`journal_ref` fields that carry the venue. A search snippet was
never accepted as verification, because a fabricated or mis-venued citation is an unrecoverable
desk reject. 27 records verified. Where a paper's abstract was insufficient to answer the question
that actually matters, the full text was fetched and the decisive sentence quoted.

**Search bound (stated so the negative results are falsifiable).** arXiv + ACL Anthology +
OpenReview + open web, run 2026-07-29, English only. A negative below means *not found by this
search*, never "does not exist".

---

## Q1 — Has anyone measured run-to-run instability as an evaluation axis in its own right?

### Verdict: **PRECEDENTED.** Strongly, repeatedly, and at venue.

| Work | Record | What it establishes |
|---|---|---|
| Atil, Aykent, Chittams, Fu, Passonneau, Radcliffe, Rajagopal, Sloan, Tudrej, Ture, Wu, Xu, Baldwin — *Non-Determinism of "Deterministic" LLM System Settings in Hosted Environments* | `2025.eval4nlp-1.12` (Eval4NLP @ ACL 2025); arXiv 2408.04667v5 | 5 API LLMs × 8 tasks × 10 runs at temperature 0 with a fixed seed. Introduces TARr@N / TARa@N. Accuracy varies up to 15% across runs; best-to-worst gap up to 70% |
| Song, Wang, Li, Lin — *The Good, The Bad, and The Greedy: Evaluation of LLMs Should Not Ignore Non-Determinism* | `2025.naacl-long.211` (NAACL 2025, long) | Non-determinism as a first-class evaluation concern; greedy vs sampling; alignment reduces sampling variance |
| Potamitis, Ramani, Arora, Kuchhal, Klein, Arora — *ReasonBENCH: Benchmarking the (In)Stability of LLM Reasoning* | arXiv 2512.07795v2 (2025-12-08, rev 2026-05-30) | 30 independent trials × 10 strategies × 12 models × 6 tasks, T ∈ {0, 0.35, 0.7}. "a single observed score can silently misrank systems" |
| Blackwell, Barry, Cohn — *Towards Reproducible LLM Evaluation: Quantifying Uncertainty in LLM Benchmark Scores* | arXiv 2410.03492v2 | Few benchmark studies quantify uncertainty; proposes a cheap method |
| Yuan, Li, Ding, Xie, Li, Zhao, Wan, Shi, Hu, Liu — *Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference* | arXiv 2506.09501v2 | Batch size / GPU count / GPU version shift outputs; up to 9% accuracy variation; root cause is non-associative floating point |
| D'Amario, Daniel, Zanetti, Edamadaka, Alaparthy, Tarkoff — *Measuring Stability Beyond Accuracy in Small Open-Source Medical LLMs for Pediatric Endocrinology* | arXiv 2601.11567v1; Reproducible AI workshop, AAAI 2026 | Stability measured as its own axis in a high-stakes domain. **"high consistency across the model response is not an indicator of correctness"** |

**The sentence Paper A must not write:** any variant of *"we introduce run-to-run answer
instability as an evaluation dimension distinct from accuracy"*, or *"instability has been
overlooked"*.

**The sentence it can write:** *"Run-to-run instability is now an established evaluation axis
(Atil et al., 2025; Song et al., 2025; Potamitis et al., 2025). We take it as given and ask a
question that axis has not yet been turned on: how instability distributes across clause types
within a single high-stakes document domain."*

---

## Q2 — Has anyone reported that instability varies by subtype, and that the aggregate hides it?

### Verdict: **PRECEDENTED in domain-general form. NOT precedented for instability in a legal or financial-document domain.**

This is the paper's actual claim, so it gets the most space. The brief instructed me to assume the
general form is not novel and find out precisely who made it. That instruction was correct.

**The closest prior work — and it is closer than expected:**

**Yagubyan — *The Coin Flip Judge? Reliability and Bias in LLM-as-a-Judge Evaluation.*** arXiv
2606.13685 (2026-04-23, 24 pages, single author, **no venue in the record — an unreviewed
preprint**). 50 pairwise + 50 pointwise trials per question at t=1.0, 29 question-response pairs
across 10 categories. Verified from the full text:

- Per-category flip rates: *"Coding: High inconsistency for GPT-4o-mini (39%) but moderate for
  GPT-4.1-mini (22%)"*; *"Knowledge/Roleplay: Consistently low flip rates (<5%) for both judges"*.
- **A worst-vs-mean instability comparison already exists in the literature**: coding at 39%
  against an overall mean of 13.3% — roughly 3×. That is structurally the same shape as Paper A's
  headline.
- It also anticipates the difficulty confound: *"High-flip-rate questions (FR ≥10%) exhibit
  substantial instability (mean FR = 23.6%)"* while *"easy questions show near-deterministic
  behavior (2.9%)"*.
- And it makes a reporting recommendation: 20 trials at t=0, dual-mode evaluation, ≥2 judges,
  report Cohen's κ and ICC.

**This is the single most consequential finding of the audit.** It does not scoop Paper A, but it
removes "worst category is N× the mean" from the list of things Paper A may present as a new
observation. What separates them is real and must be stated in the related-work section, early:

| | Coin Flip Judge | Paper A |
|---|---|---|
| What is unstable | An LLM **judge's verdict** on other models' outputs | A model's **own substantive answer** to a domain question |
| Consequence of a flip | A benchmark ranking moves | A different equity split is reported to a user |
| Categories | Generic capability buckets (coding, knowledge, roleplay) | Clause types in venture-financing documents |
| Scale | 29 question-response pairs, 2 judges | 60 leaves, 12 models, 20 runs each (14,400 model-item measurements) |
| Instrument calibration | none | split-half reliability + disattenuation |
| Status | unreviewed preprint | — |

**Supporting domain-general precedent:**

- **Atil et al.** (record above) report stability **per task** and state which tasks are stable:
  *"The high-performance for the navigation task indicate that leaderboards on this task can be
  expected to be more reliable. On the other hand, the more scattered results for the college math
  and professional accounting tasks indicate that results reported on these tasks might not be as
  robust."* And: *"Notably, there are 5-15% differences on some tasks."*
- **ReasonBENCH** builds the aggregate-hides-it point into its design: *"The suite intentionally
  mixes mathematical reasoning, code generation, multi-hop QA, scientific problem-solving, and
  creative writing … because instability can be hidden by any single benchmark or domain."*
- Guerra-Solano & Li — *Persona Non Grata: LLM Persona-Driven Generations in MCQA are Unstable in
  Distinct Dimensions* (arXiv 2607.00937, under review at ARR): instability decomposed by dimension.
- Ajayi, Chowdhury, Lazar — *Incoherent Values?* (arXiv 2606.21102): a 30-point gap between the
  weakest and strongest value categories (50 points for reasoning models).
- Dev, Sloan, Kavner, Kong, Sandler — *Judge Reliability Harness* (arXiv 2603.05399, Agents in the
  Wild workshop @ ICLR 2026): *"no judge evaluated is uniformly reliable"*, reliability varies by
  task and perturbation family.
- Shergadwala — *The Stability Trap* (arXiv 2601.11783): high verdict agreement masks inconsistent
  reasoning.
- Camuffo, Gambardella, Kazemi, Malachowski, Pandey — *Variance-Aware LLM Annotation for Strategy
  Research* (arXiv 2601.02370): variance sources and a measurement protocol.

**The wider disaggregated-evaluation lineage Paper A sits inside (all precedent, none about instability):**
Ribeiro, Wu, Guestrin, Singh — *CheckList* (arXiv 2005.04118, **ACL 2020**); Mitchell, Wu, Zaldivar,
Barnes, Vasserman, Hutchinson, Spitzer, Raji, Gebru — *Model Cards for Model Reporting* (arXiv
1810.03993, **FAT\* '19**, doi 10.1145/3287560.3287596); Liang, Bommasani, Lee, Tsipras, Soylu et al.
— *Holistic Evaluation of Language Models* (arXiv 2211.09110, **TMLR 2023**).

**The comparable-domain half — and this is where the gate turns:**

**Liu, Li, Ma, Zhao, Du — *ContractEval: Benchmarking LLMs for Clause-Level Legal Risk
Identification in Commercial Contracts.*** arXiv 2508.03080; `2025.nllp-1.19` (NLLP workshop 2025).
This is the nearest neighbour in document type, and it does report per-category variation:
*"Model performance varies across legal categories, with significantly lower correctness in less
common or longer clauses."* Verified from the full text, the decisive facts:

- **Each item is evaluated once.** No temperature, seed, or repeated-sampling protocol is described.
- **It measures no run-to-run instability at all** — only single-point F1 / F2 / Jaccard.
- Its per-category finding is about **correctness**, not stability.
- Corpus is CUAD-derived (EDGAR commercial contracts: licensing, IP, NDAs, M&A). **No venture
  financing documents.**

So the clause-level *correctness* disaggregation exists in a comparable domain; the clause-level
*instability* disaggregation does not.

**The sentence Paper A must not write:** *"we are the first to show that aggregate scores hide
category-level variation"*, or *"we introduce the worst-category-to-mean ratio"*.

**The sentence it can write:** *"That instability concentrates unevenly across task categories is
established for general capability buckets (Atil et al., 2025; Potamitis et al., 2025) and for
LLM-judge verdicts, where the worst category runs roughly 3× the mean (Yagubyan, 2026). What has
not been measured is whether the same holds for the clause types of a legal-financial document,
where per-clause correctness disaggregation exists (Liu et al., 2025) but is computed from a single
run per item and therefore cannot see instability at all."*

---

## Q3 — Does a benchmark already exist for LLM performance on venture-financing documents?

### Verdict: **NO PRIOR WORK FOUND** (bounded by the search above). The closest neighbours are named below and none of them is this.

| Work | Record | Why it is not this |
|---|---|---|
| Chen, Ternasky, Kwesi, Griffin, Yin, Salifu, Amoaba, Mu, Alican, Ihlamur — *VCBench: Benchmarking LLMs in Venture Capital* | arXiv 2509.14448 (2025-09-17, rev 2026-05-05) | **The nearest name, the furthest task.** Predicts *founder success* from 9,000 anonymised founder profiles. No legal documents, no term sheets, no cap tables, no instability measurement |
| Wang, Scardigli, Tang, Chen, Levkin, Chen, Ball, Woodside, Zhang, Hendrycks — *MAUD* | arXiv 2301.00876v3, **EMNLP 2023** | Closest *document* type: merger agreements, expert-annotated deal points, 39k+ examples. M&A, not venture financing; accuracy only, single-pass |
| Liu et al. — *ContractEval* | `2025.nllp-1.19` | CUAD/EDGAR commercial contracts; no venture financing; no instability |
| Guha, Nyarko, Ho, Ré, Chilton et al. (40 authors) — *LegalBench* | arXiv 2308.11462 | 162 legal-reasoning tasks; incorporates MAUD; no venture-financing instrument tasks, no instability axis |
| CUAD; ContractNLI | (via LegalBench / LegalBench-RAG) | Commercial contracts and NDAs |
| Xie, Han, Chen, Xiang, Zhang et al. — *FinBen* / PIXIU | arXiv 2402.12659 | 36 datasets, 24 financial tasks; public-market filings and market data. Hosted the first financial-LLM shared task at FinNLP-AgentScen @ IJCAI-2024 |
| FinanceBench; SECQUE; FinSheet-Bench; FinVerBench | — | Public filings, SEC documents, spreadsheets. Public markets, not private-market financing instruments |

Nothing found evaluates LLMs on term sheets, SAFEs, convertible notes, certificates of
incorporation, or cap-table waterfalls — and nothing found measures answer instability on any of
them.

**What Paper A can claim:** the domain is open. Phrase it as a bounded negative — *"we are not
aware of a benchmark evaluating LLMs on venture-financing instruments; the nearest work is VCBench
(founder-outcome prediction, not documents) and MAUD (merger agreements, single-pass accuracy)"* —
never as *"the first benchmark of its kind"*.

---

## Q4 — Has anyone applied split-half reliability or psychometric instrument analysis to LLM evaluation?

### Verdict: **PRECEDENTED.** The ceiling analysis is a **control**, exactly as the brief assumed. Not a contribution.

| Work | Record | What it establishes |
|---|---|---|
| Cacioli — *Beyond the Mean: Within-Model Reliable Change Detection for LLM Evaluation* | arXiv 2604.27405 (2026-04-30, **7 pages, single author, pre-registered, no venue**) | Reliable Change Index from clinical psychology; 2,000 MMLU-Pro items, K=10 at T=0.7; split-half cross-validation over 1,000 splits |
| Contreras — *An LLM-Native Psychometric Instrument Reveals a Self-Report–Behavior Gap Across 25 Models* | arXiv 2606.09843 (rev 2026-07-07) | Split-half, Spearman-Brown corrected, odd-even items, applied to LLMs |
| Ye, Jin, Xie, Zhang, Song — *Large Language Model Psychometrics: A Systematic Review of Evaluation, Validation, and Enhancement* | arXiv 2505.08245 (rev 2026-03-11), **400+ references** | The field exists and has been surveyed. Reliability/validity framing is standard vocabulary |

Item Response Theory, Cronbach's α, Generalizability Theory and Many-Facet Rasch Measurement are
all already in use for LLM evaluation.

**The sentence Paper A must not write:** *"we introduce split-half reliability to LLM evaluation"*,
or any framing of the ceiling as methodologically novel.

**The sentence it can write:** *"Following standard psychometric practice, now established for LLM
evaluation (Ye et al., 2025) and applied to item-level LLM comparison by Cacioli (2026), we
estimate the instrument's split-half reliability before interpreting any correlation as small."*
One sentence and a number. This is what §Step 4's kill list already proposed, and the audit
confirms the kill is correct.

**A note that cuts the other way, in Paper A's favour.** Cacioli reports near-zero cross-model item
agreement and 79%/72% of items showing no reliable change — a result pointing away from Paper A's.
It correlates *version-to-version change* across two within-family model pairs; Paper A measures
*within-model instability* across twelve independent models. Different quantity, different design.
That distinction has to be drawn explicitly and early or a reviewer will assume a contradiction.

---

## Q5 — Has anyone quantified worst-slice versus mean performance as a reporting recommendation?

### Verdict: **PRECEDENTED**, under at least three different vocabularies.

| Work | Record | The recommendation already made |
|---|---|---|
| Sagawa, Koh, Hashimoto, Liang — *Distributionally Robust Neural Networks for Group Shifts* | arXiv 1911.08731 | Worst-group accuracy as the object of interest rather than the average. The entire GroupDRO literature follows |
| Mitchell et al. — *Model Cards* | arXiv 1810.03993, FAT\* '19 | Disaggregated reporting as a documentation standard: performance broken out by group and by intersection |
| Liang et al. — *HELM* | arXiv 2211.09110, TMLR 2023 | Report the scenario × metric matrix, not a single number |
| Atil et al. | `2025.eval4nlp-1.12` | **"We encourage reporting maximum-minimum scores across runs to have a more robust comparison of models."** The closest existing recommendation to Paper A's, and it is about instability specifically |
| Yagubyan | arXiv 2606.13685 | Flag questions with flip rate >20% as uncertain; ≥20 trials; report κ and ICC |

**The sentence Paper A must not write:** *"we propose reporting worst-slice alongside the mean"* as
though the idea were new.

**The sentence it can write:** *"Worst-group reporting is long established for accuracy under
subpopulation shift (Sagawa et al., 2020) and for documentation (Mitchell et al., 2019). Atil et al.
(2025) extend the principle to stability by recommending max–min across runs. We give that
recommendation a concrete, domain-grounded magnitude: in this corpus the worst clause type runs
[N]× the headline, so a single stability number is not a safe summary for deployment."*

---

## Summary table

| Element of Paper A | Novel? | Prior work | What we can still claim |
|---|---|---|---|
| Instability as an evaluation axis | **No** | Atil 2025 (Eval4NLP); Song 2025 (NAACL); ReasonBENCH 2025 | Take as given; cite; build on |
| Aggregate hides per-category instability | **No, domain-general** | Yagubyan 2026 (~3× on judge verdicts); Atil 2025 (per-task); ReasonBENCH 2025 | Cannot claim the insight. Can claim the first measurement of it on a legal-financial document corpus |
| Worst-to-mean instability *ratio* as a quantity | **No** | Yagubyan 2026 (39% vs 13.3%) | Cannot claim the construct. Can claim the magnitude, the calibration, and the domain |
| Clause-level disaggregation in contracts | **No, for accuracy** | ContractEval (NLLP 2025) | Can claim the extension from correctness to **stability** — ContractEval runs each item once and structurally cannot see it |
| Venture-financing document benchmark | **Not found** | VCBench (founder profiles, not documents); MAUD (M&A) | Bounded negative. The corpus and the task are open |
| Split-half reliability / ceiling | **No** | Cacioli 2026; Contreras 2026; Ye 2025 (survey) | A control. One sentence, one number, cite, appendix |
| Worst-slice reporting recommendation | **No** | Sagawa 2020; Mitchell 2019; HELM 2023; Atil 2025 | Can give it a domain-grounded magnitude and a concrete adoption rule |
| Instability where the answer decides equity ownership | **Not found** | — | The genuine open space, and it is a consequence argument rather than a method argument |

---

## The gate

The brief specified two trigger conditions. Both were tested against the evidence above.

**Trigger 1 — "the core claim is fully precedented in a domain-general form AND in a comparable
domain."** Requires *both*. **NOT MET.**
- Domain-general half: **met.** Yagubyan (2026) reports a worst-category-to-mean instability ratio;
  Atil et al. (2025) report per-task stability variation and a max–min reporting recommendation;
  ReasonBENCH designs around instability being hidden by any single benchmark.
- Comparable-domain half: **not met.** The nearest work in a comparable domain, ContractEval,
  evaluates each item exactly once and measures no instability of any kind. Its per-clause finding
  concerns correctness. No legal or financial document benchmark was found that measures run-to-run
  instability, disaggregated or otherwise.

**Trigger 2 — "a benchmark already exists that measures instability on venture-financing
documents." NOT MET.** No venture-financing document benchmark was found at all, with or without an
instability axis. VCBench occupies the name and not the task.

**Neither trigger fires, so the gate clears** and stages 1–4 proceed. This is the outcome the brief
predicted as most likely and pre-authorised: the general claim is precedented, the domain is not,
and the reliability axis applied to this domain is not.

**But the audit changes the positioning more than "gate cleared" suggests, and that is the finding
worth carrying forward.** Before this search the plan was to headline a worst-to-mean ratio.
That construct now has a direct precedent (Yagubyan, 2026) that Paper A must cite in its own
related-work section, on its own initiative, and distinguish in the first page rather than the
last. The defensible contribution is no longer *the shape of the result*. It is the **consequence
domain plus the calibration**: the same shape, measured on documents where a flipped answer changes
who owns what, against an instrument whose reliability was established first rather than assumed.

A paper that correctly places itself in a crowded literature is accepted. This audit is what makes
that placement possible, and finding Yagubyan now — rather than in a review — is the entire return
on running step 0 before step 1.
