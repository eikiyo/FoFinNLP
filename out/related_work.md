# Related work — verified citations (Paper A, step 5b)

> **Verification method.** Every arXiv entry below was resolved through the **arXiv API**
> (`export.arxiv.org/api/query?id_list=…`), which returns the authoritative title, author list and
> submission date — not a search-engine snippet. The one non-arXiv entry was resolved against the
> **ACL Anthology** record. Nothing here is cited from memory. Where a claim could not be sourced,
> it is written `[NO SOURCE FOUND]` rather than filled in.
>
> **Counts:** 11 citations sought across the five areas, **11 verified**, 0 unverifiable, 0 written
> from memory. This is a working bibliography for the paper's related-work section, not the section
> itself.

---

## ⚠ 0. THE DIRECTLY ADJACENT PRIOR RESULT — read this first

**Cacioli, Jon-Paul (2026). *Beyond the Mean: Within-Model Reliable Change Detection for LLM
Evaluation.* arXiv:2604.27405, submitted 2026-04-30. Single author, independent researcher.
7 pages. Self-described as a pre-registered study. Not peer-reviewed at the time of writing.**

**What it claims.** Aggregate accuracy improvements between model versions mask large, bidirectional
item-level movement: "the aggregate accuracy gain is the net residual of opposing item-level
movements." It adapts the Reliable Change Index from clinical psychology, over 2,000 MMLU-Pro items,
K=10 samples per item, **at temperature 0.7**, across two model pairs (Llama 3 → 3.1, Qwen 2.5 → 3).

**Why it matters to Paper A — two separate reasons, both serious.**

**(a) It uses Paper A's step-1 method already.** It estimates reliability "via 1,000 random
split-halves of K=10 into two halves of 5. Spearman-Brown corrected," reporting coefficients of
.966–.996. That is exactly the split-half + Spearman-Brown procedure this stage ran. **Paper A
cannot present split-half reliability of an LLM instability measure as a methodological
contribution.** It is a sound and now-precedented control, and it must cite this paper when using
it. Our median r_full of 0.8970 is lower than their .966–.996, which is expected: they split K=10
per item within a single benchmark, we split K=20 per item and then correlate at the LEAF level
across 60 heterogeneous leaves.

**(b) Its headline cross-model number points the OTHER WAY from ours.** "The cross-pair item-level
RCI correlation was near zero (r=.11, p=.019, n=431 shared analysable items). The items that changed
reliably for Llama are almost entirely different from those that changed for Qwen."

**The distinction Paper A must draw, precisely and early.** These are different constructs and the
paper is not scooped — but only if the difference is stated explicitly and up front:

| | Cacioli 2026 | Paper A |
|---|---|---|
| Quantity correlated | **Change** in an item's correctness between two model VERSIONS (RCI) | **Instability** of an item within a single fixed model (run-to-run flip rate) |
| What is being compared | Two model *pairs* (Llama-pair vs Qwen-pair) | 66 model *pairs* drawn from 12 models |
| Unit | MMLU-Pro item | Probity leaf (a clause type), aggregated over its items |
| Domain | General knowledge / reasoning | Structured financial-instrument extraction |
| Result | r = .11, near zero | rho = 0.2964, p = 0.0010, 95% CI [0.114, 0.458] |

A version-to-version *change* score and a within-model *instability* score are genuinely different
measurements, and there is no contradiction in one transferring across models while the other does
not. **But a reviewer who knows this paper will ask, and "they measured something else" has to be
demonstrated rather than asserted.** Recommended handling: cite it in the introduction as the
closest prior work, state the construct difference in one table like the one above, and note that
the two findings are compatible and even complementary — instability transfers, version-change does
not.

**Honest caveat about its weight.** It is a 7-page single-author arXiv preprint with no peer review
at the time of writing, so it does not settle the question. It does, however, establish priority on
the method and it will be found by any reviewer who searches the obvious terms.

---

## 1. Self-consistency and sampling-based decoding

**Wang, Xuezhi et al. (2022/2023). *Self-Consistency Improves Chain of Thought Reasoning in Language
Models.* arXiv:2203.11171. 8 authors. Published at ICLR 2023.**
*Claim:* replacing greedy decoding with sampling multiple reasoning paths and taking a majority vote
substantially improves reasoning accuracy (GSM8K +17.9%, SVAMP +11.0%, AQuA +12.2%).
*Relation:* this is the paper that made run-to-run variation **useful** — the field's default framing
is that sampling diversity is a resource to be marginalised over. Paper A studies the same underlying
variation as a **liability** in a setting where a single extraction is acted on and there is no
majority vote to hide behind. Cite to establish that the phenomenon is well known and that our
framing, not our observation, is what differs.

`[NO SOURCE FOUND]` — no prior work was located that studies self-consistency-style sampling
variation specifically as a *deployment risk* for single-shot structured extraction. If the paper
claims novelty anywhere, this is the defensible place.

---

## 2. Non-determinism and reproducibility of LLM inference, including serving-stack causes

**Zhu, Zhenting et al. (2026). *Demystifying Numerical Instability in LLM Inference: Achieving
Reproducible Inference for Mission-Critical Tasks with HEAL.* arXiv:2606.21023.**
*Claim:* characterises numerical sources of non-reproducibility in inference and proposes mitigation.
*Relation:* supplies the mechanism-level account of *why* wobble exists at all. Paper A measures the
consequence at task level and does not need to explain the cause, but must not appear unaware of it.

**Khatchadourian, Raffi et al. (2025). *LLM Output Drift: Cross-Provider Validation & Mitigation for
Financial Workflows.* arXiv:2511.07585. To appear in AI4F @ ACM ICAIF '25.**
*Claim:* identical open-weight models show cross-provider output discrepancies attributable to
templates, quantization and serving stacks, specifically in financial workflows.
*Relation:* **the closest paper by domain and by concern**, and the direct precedent for Paper A's
stage-1 serving-layer control. It establishes that the routing/serving confound is real and must be
addressed — which is exactly what our frontier-only same-path vs different-path comparison does.
Cite it where that control is introduced.

**"Defeating Nondeterminism in LLM Inference" (Thinking Machines, 2025).**
*Claim:* the apparent non-determinism of temperature-zero inference is driven primarily by the
**batch-size dependence of reduction kernels**, not by floating-point non-associativity alone;
batch-invariant kernels can produce bit-identical outputs across repeated runs.
*Relation:* the standard reference for the serving-stack mechanism.
⚠ **Verification status: NOT verified to the same standard as the entries above.** It is a company
blog post, not an indexed paper, and it was seen here only through secondary coverage. **Locate and
read the primary post before citing it, and cite it as a blog post, not as a paper.** Do not put it
in the bibliography on the strength of this line.

---

## 3. Benchmark aggregation critiques — why single headline scores mislead

**Liang, Percy et al. (2022). *Holistic Evaluation of Language Models.* arXiv:2211.09110. 50 authors
(Stanford CRFM).**
*Claim:* models should be evaluated across many explicit dimensions (accuracy, calibration,
robustness, fairness, efficiency…) rather than collapsed to one number.
*Relation:* the canonical citation for "one score hides the thing you care about." Paper A adds a
dimension HELM does not cover — run-to-run stability at item level — and the worst-category-to-mean
ratio (median 4.96x) is a concrete instance of exactly HELM's argument.

**Miller, Evan (2024). *Adding Error Bars to Evals: A Statistical Approach to Language Model
Evaluations.* arXiv:2411.00640.**
*Claim:* eval results are statistical estimates and should be reported with uncertainty.
*Relation:* the direct justification for stage 2's bootstrap interval and the Wilson intervals on
every category cell. Cite wherever we defend reporting an interval instead of a point.

**Zhou, Hongli et al. (2025). *Lost in Benchmarks? Rethinking Large Language Model Benchmarking with
Item Response Theory.* arXiv:2505.15055. 13 authors. Accepted to AAAI 2026 (Oral).**
*Claim:* applies IRT to LLM benchmarking, treating items as having their own difficulty/
discrimination parameters rather than being interchangeable.
*Relation:* the closest *methodological* neighbour — it is the other serious attempt to treat
benchmark items as psychometric objects. **A reviewer may reasonably ask why Paper A does not use
IRT.** Have an answer ready: IRT models item difficulty for a correctness response, whereas our
quantity is within-item variance at fixed model, which is a different latent construct. This should
be a sentence in related work, not a footnote.

**Kiela, Douwe et al. (2021). *Dynabench: Rethinking Benchmarking in NLP.* arXiv:2104.14337.
19 authors. NAACL 2021.**
*Claim:* static benchmarks saturate and mislead; benchmarking should be dynamic and adversarial.
*Relation:* background for "the benchmark is the problem" framing. Secondary.

---

## 4. LLM evaluation in finance and law

**Xie, Qianqian et al. (2024). *FinBen: A Holistic Financial Benchmark for Large Language Models.*
arXiv:2402.12659. 34 authors. NeurIPS 2024 Datasets & Benchmarks Track.**
*Claim:* 36 datasets across 24 financial tasks and 21 models; LLMs do well on information extraction
and textual analysis, poorly on advanced reasoning, generation and forecasting.
*Relation:* **the lineage paper for this venue** and the obvious "why another financial benchmark?"
challenge. The answer must be sharp: FinBen reports aggregate accuracy per task; it does not report
run-to-run stability at all. Paper A measures an axis FinBen leaves entirely unmeasured, on a
narrower, deeper corpus. Cite in the first paragraph.

**Magesh, Varun et al. (2024). *Hallucination-Free? Assessing the Reliability of Leading AI Legal
Research Tools.* arXiv:2405.20362.**
*Claim:* commercial legal-research AI tools hallucinate at material rates despite reliability claims.
*Relation:* the strongest available evidence that in high-stakes document domains, *reliability
claims outrun measured reliability* — the practitioner motivation for Paper A. Cite in the
introduction where the stakes are set.

---

## 5. Annotation quality and ground-truth construction

**Artstein, Ron and Massimo Poesio (2008). *Survey Article: Inter-Coder Agreement for Computational
Linguistics.* Computational Linguistics 34(4), pp. 555–596.** (Verified via ACL Anthology J08-4004.)
*Claim:* the standard survey of agreement coefficients for NLP, including which coefficient suits
which annotation structure.
*Relation:* the methodological authority for step 5a. Cite it for the choice of Cohen's kappa and
for the treatment of categorical vs continuous fields.

**Bowman, Samuel R. and George Dahl (2021). *What Will it Take to Fix Benchmarking in Natural
Language Understanding?* arXiv:2104.02145. NAACL 2021.**
*Claim:* benchmark validity depends on annotation quality and on the construct actually being
measured, not on leaderboard movement.
*Relation:* the citation for why a solo-annotated benchmark must report agreement at all — the
justification for doing step 5a rather than arguing it is unnecessary.

---

## 6. Rank similarity measures

**Webber, William, Alistair Moffat and Justin Zobel (2010). *A Similarity Measure for Indefinite
Rankings.* ACM Transactions on Information Systems 28(4), article 20, pp. 20:1–20:38, November
2010. doi:10.1145/1852102.1852106.** (Verified 2026-07-29 against the authors' own institutional
record at people.eng.unimelb.edu.au/ammoffat/abstracts/wmz10acmtois.html, which states "ACM Trans.
Information Systems, 28(4):20.1-20.38, November 2010". The ACM DL page itself returns 403 to an
unauthenticated fetch, so the publisher page was NOT the verification source and is not claimed as
one.)
*Claim:* proposes rank-biased overlap (RBO), a similarity measure for rankings that may be
incomplete, of unequal length, and non-conjoint. RBO is top-weighted via a geometric user model
with parameter *p*, and is defined for prefixes, so it is well behaved when the two rankings are
truncated at a depth shallower than the full list.
*Relation:* the citation for step 1d. The paper's transfer statistic is an overlap at *k*, which
is undefined in the presence of ties and truncation; RBO is the measure that survives both, and
its prefix formulation is why the maximum attainable value at a finite depth is the weight covered
by that depth rather than 1.0. Cited for the measure only, not for any empirical result.

---

## What was searched for and NOT found

- **`[NO SOURCE FOUND]`** — no prior work reporting **item-level run-to-run instability correlated
  across a lineup of a dozen models**. Cacioli 2026 is the nearest, and it correlates version-change
  rather than instability, over two model pairs rather than twelve models. On the evidence gathered,
  Paper A's specific claim appears unclaimed.
- **`[NO SOURCE FOUND]`** — no prior work applying split-half reliability to a *financial* extraction
  benchmark specifically.
- **Caveat on the strength of both statements.** These are negative results from a bounded search
  (arXiv + web search, 2026-07-29). Absence of evidence here is weak evidence of absence, and a
  systematic search of the ACL Anthology and ICAIF/FinNLP proceedings should be run before any
  novelty claim is written into the paper. **Do not write "we are the first" on the strength of this
  document.**
