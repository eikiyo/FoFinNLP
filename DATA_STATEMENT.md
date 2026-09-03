# Data statement — Probity

Every number here was recounted from the files in this repository by
`paper-a/audit/ds_facts.py`, not copied from the paper. Each value carries its source. Where the
repository does not establish a fact, the section says `UNRESOLVED` and names the decision needed
rather than filling the gap with a plausible value.

Scope: the **legacy arm** (unsuffixed artifacts; temperature 0.7), which is the arm the paper
reports. The `_t01` and `_t07` namespaces are different experiments and are excluded throughout.

---

## 1. Curation rationale

Probity asks language models to read venture-financing documents and answer questions whose answers
carry money: what a share price is, what a preferred holder receives in a liquidation waterfall,
what a founder's ownership is after a round. These were chosen because the answer is a number a
founder or an investor could act on, and because a changed answer between two identical calls is
not a presentation defect — it is a different allocation of a company.

Task types are the 8 families in `engine/registry.json`: `priced_equity` (16 tasks),
`convertibles` (12), `cap_table` (7), `rights_governance` (7), `founder_equity` (5),
`regulatory` (5), `risk_flag` (5), `exit_waterfall` (3). Counts derived from `engine/registry.json`
with `tier == "built"`, and they sum to the 60 built tasks. The unfiltered registry holds 67 leaves;
the other 7 are `tier == "v2"` and are not part of this release.

## 2. Source and provenance

One document class: **public filings retrieved from the U.S. SEC EDGAR system.**

| fact | value | source |
|---|---|---|
| distinct source filings | 965 | `leaves/*/corpus/full/*.txt` stems |
| distinct filer CIKs | 863 | first field of each stem |
| full filing texts stored | 1,145 files, 60.52 MB | `leaves/*/corpus/full/` |
| windowed extracts stored | 524 files, 0.76 MB | `leaves/*/corpus/questions/` |
| acquisition method | EDGAR full-text search, then the Archives document URL | `engine/edgar.py:23,39` |

Item identifiers are `CIK_accession` (e.g. `1076103_000091476003000217`), so every item states which
filing it came from and can be re-fetched from
`https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/`.

Two artifacts per item: the **full document** as retrieved, and the **windowed extract** actually
shown to the model. The distinction is the paper's subject — an item whose answer is not inside its
window is defective regardless of how stably a model answers it.

## 3. Licensing and redistribution

**UNRESOLVED — under what licence, if any, is the corpus of retrieved SEC filing text
redistributed?** This section states what the repository establishes and stops there. It asserts no
redistribution right and denies none, and it draws no legal conclusion in either direction.

Three facts, each with a pointer:

1. **`LICENSE` is the MIT License, and by its own text it covers software.** It grants permission to
   deal in "the Software" and says nothing about data (`LICENSE:1-21`). The packaging metadata
   repeats the same declaration for the software (`pyproject.toml:11`, `pyproject.toml:15`).
2. **No data licence exists anywhere in the repository.** There is no second licence file, no licence
   header on any corpus file, no `CITATION.cff`, and no redistribution statement for the data in
   `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` or
   `pyproject.toml`. Searching every repository-level document for `public domain`, `CC0`, `CC-BY`,
   `Creative Commons` and `data licence` returns exactly one hit — this sentence. (76 of the corpus
   filings contain one of those phrases in their own text. A filing that discusses public-domain
   material is not a licence grant over the filing, and an earlier draft of this section said the
   search "returns nothing", which was false as written.)
3. **An SEC filing is authored by the filer and hosted by a government system.** The document is the
   company's; the system that serves it is the government's. Government-works rules therefore do not
   automatically apply, and this document does not say whether any of them apply at all.

**The question is open over material that is already distributed.** All 1,145 full filing texts,
60.52 MB, are tracked under `leaves/*/corpus/full/`, and this repository is public. An earlier draft
described a narrower "safe subset" that the repository does not implement; that sentence was wrong
and is replaced by this one.

**What a re-user can rely on:** the windowed extracts, the oracle labels, the validating quotes, the
audit outputs and the code are released under the licences this repository states; the retrieved full
filing texts carry no asserted licence.

**We do not assert a redistribution right for the retrieved filing texts.**

A re-user who prefers to stay clear of the open question can work from the windowed extracts, the
labels, the validating quotes, the audit outputs and the code alone. That subset reproduces every
table and figure in the paper, because the generators read the committed audit output rather than the
corpus. The full texts are needed only to *re-run* the provenance audit's source-document check
(`paper-a/analysis/oracle_audit.py`, `paper-a/analysis/fulltext.py`) and the window-repair analysis
(`paper-a/analysis/repair_windows.py`).

## 4. Personal and identifying data

The corpus is corporate rather than personal, but it is not free of names.

| fact | value | source |
|---|---|---|
| distinct company names in the oracle | 313 | `leaves/*/oracle.jsonl:company` |
| items carrying a `company` field | all 470 | same |
| items carrying a `validating_quote` | 470 of 470 | `leaves/*/oracle.jsonl:validating_quote` |

Company names, filer CIKs and accession numbers are retained deliberately: they are what makes a
label auditable, and they identify **companies**, not private individuals.

Full filing texts under `leaves/*/corpus/full/` are stored **as retrieved and unredacted**. This is
counted rather than assumed: **758 of the 1,123 `.txt` documents (67.5%) carry an `/s/` signature
block with a name**, the EDGAR convention for a signed name, so the majority carry the name of at
least one officer, director or counsel. Across the corpus there are 3,341 `/s/` markers, 3,217 of
them followed by a parsable name; three documents are unsigned templates whose markers are blank. No
redaction or named-entity removal was applied, and none is claimed.

The definition matters and is stated: the count is of documents with a **named** conformed signature,
measured by `paper-a/audit/sigblocks.py`. A looser test — `/s/` followed by any word character —
returns 759, because in one unsigned template (`By: /s/ By: /s/ Name: Title:`) it matches the word
"By" as though it were a person. `PERSONAL_DATA.md` carries the full accounting, including a verified
scan showing that no derived artifact in the pipeline aggregates or indexes any of these names.

**UNRESOLVED — are unredacted officer and signatory names inside the full filing texts acceptable in
the released artifact, given those documents are already public at sec.gov?** This is a distribution
question, not a discovery question: the names are public. No position is taken here in either
direction. What has been measured, rather than assumed, is what a redaction would achieve: 2,768 of
the 3,341 signature blocks have their signed name appear again elsewhere in the same document, so
masking the blocks would leave most of those names in place (`paper-a/audit/redaction_impact.md`).

## 5. Language and jurisdiction

English only. United States only: SEC filings under U.S. securities law, using U.S. venture
financing instruments and terminology. Findings do not transfer to other jurisdictions' instruments
without re-annotation, and the benchmark makes no claim that they do.

## 6. Annotation

**One annotator produced every label.** There is no second reading, and the paper reports no
inter-annotator agreement coefficient. That is a structural limitation of the resource, stated
plainly, not mitigated.

| fact | value | source |
|---|---|---|
| annotators | 1 | `paper-a/out/annotation/PROTOCOL.md` |
| protocol | documented, released | `paper-a/out/annotation/PROTOCOL.md` |
| adjudication rule | documented, released | `paper-a/out/annotation/ADJUDICATION.md` |
| items author-excluded at adjudication | 7 | `paper-a/analysis/adjudication.py:exclusions()` |
| blind re-annotation pack | 154 items over 19 leaves, released, **not executed** | `paper-a/out/annotation/blind_pack.csv` |
| agreement coefficient | none exists | `agreement_result.json`: `"status": "NOT RUN"`, `n_filled: 0` |

Two things follow from one annotator that are easy to state loosely, so they are stated exactly:

- **The 7 adjudication exclusions are self-adjudicated.** The items removed at adjudication were
  removed by the same person who produced the labels. There is no independent arbiter in that step,
  and `ADJUDICATION.md:96` records who decides for that reason. (The anonymous review mirror neutralised that
  line to "the author"; this camera-ready tree carries the named version.)
- **A future agreement number would be intra-annotator unless the reader is independent.**
  `ADJUDICATION.md:69` binds this in advance: if the prepared pack is re-read by the person who
  produced the original oracle, the result is *intra*-annotator agreement and must be reported in
  those words. Only a genuinely independent reader yields *inter*-annotator agreement. Releasing the
  pack does not make the eventual number the stronger of the two.

The blind re-annotation pack, its protocol and its adjudication rule are released so that a second
reader can be run by anyone. It has not been run. `PROTOCOL.md` states its own status as "PREPARED,
NOT RUN", `ADJUDICATION.md` records that "the sitting has **not** happened", and
`agreement_result.json` carries `"status": "NOT RUN"` with `n_filled: 0`. Nothing in this repository
or the paper reports an agreement statistic, and no phrase should be read as implying a second
reader existed.

The prepared sample is 19 of 60 leaves (32%), not the 20% originally planned, because the benchmark
has 19 distinct (category × answer-type) strata and at 12 leaves seven strata would have been
represented by nothing — the small strata being where a lone annotator is most likely to have
drifted (`PROTOCOL.md:24`).

Every label carries a **validating quote**, and an automated provenance audit resolves each label's
source document by content and checks that the quote appears in it. That audit is a substitute for
neither a second annotator nor an agreement coefficient; it checks that a label is traceable to a
document, not that a second person would have assigned it.

## 7. Exclusions

Three layers, in order. All three are needed to arrive at the paper's population, and the codebase
has previously had two artifacts disagree about it (`paper-a/analysis/flagged_profile.py:63`).

| stage | rule | items removed | remaining |
|---|---|---|---|
| — | corpus as annotated | — | 470 |
| provenance audit | `issues` non-empty in `oracle_audit.csv` | 36 | 434 |
| author adjudication | `adjudication == "excluded"` | 7 | **427** |

The 36 audit flags break down as: 31 "quote not inside the window", 3 both "not found in the source
document" and "not inside the window", 2 "not found in the source document"
(`paper-a/out/annotation/oracle_audit.csv:issues`).

Of the 60 tasks, **52 retain at least one item**; 8 lose every item and drop out
(`current_ownership_pct`, `founder_ownership_pct`, `investor_ownership_pct`, `employee_pool_pct`,
`option_pool_shuffle`, `multi_round_stacked_dilution`, `liquidation_waterfall_payout`,
`convert_vs_preference_decision`).

Audit coverage is reported three ways rather than as a pass rate: `verified-present` 416,
`not-checkable` 49, `verified-absent` 5 (`oracle_audit.csv:source_state`).

**The audit's own two defects are reported, not quietly repaired.** Its source lookup resolved
documents by item identifier while they are stored under company and accession prefixes, so 150 of
470 items were never opened and their quote check silently did not run; and its quote matcher tested
the raw text of composite quotes, flagging 8 items for the matcher's own construction. Both are
fixed, both moved published numbers, and the current artifact shows 49 unresolved rather than 150.

## 8. Model configurations and responses

| fact | value | source |
|---|---|---|
| configurations analysed | 12 | `paper-a/out/tables/model_summary.csv` |
| distinct base models | 11 | two rows are quantizations of one 1B base |
| serving paths | 3 — local (2), direct (3), routed (7) | `paper-a/analysis/config.py:serving_paths()` |
| samples per item | 20 | 9,400 lines per config ÷ 470 items |
| temperature | 0.7 | `paper-a/analysis/config.py:ARM_HUMAN` |
| responses collected | 112,800 | counted: 12 × 60 leaves × `runs_<config>.jsonl` |
| responses analysed | 111,800 | 112,800 minus 1,000 with `parsed == null` |

Both response counts were recounted from the raw files. The 112,800 figure is exact (12 × 20 × 470).
The analysed figure was derived twice independently — from the raw records, and from
`n_and_dropped_matrix.csv` as `sum(n_runs) − sum(n_runs × parse_failure_rate)` — and both give
111,800.

## 9. Intended use and out of scope

Probity is an **evaluation instrument for measuring answer instability**. It is:

- **not legal advice**, and not a substitute for counsel reading a document;
- **not a compliance tool**, and not validated for any regulatory purpose;
- **not a basis for a financing decision.** The paper's central finding is that these models return
  different answers to the same question about the same document. Acting on any single answer is
  precisely what the benchmark shows to be unsafe;
- **not a general legal-reasoning benchmark.** It covers U.S. venture-financing instruments only.

## 10. Ethical considerations and foreseeable misuse

- **A high score does not mean a model is safe to use on real deals.** Stability is not correctness,
  and the corpus measures a narrow slice of one jurisdiction's instruments.
- **The corpus is small enough to overfit.** 470 items over 60 tasks is an instrument, not a
  training set; tuning on it and reporting the result as capability would be misuse.
- **Company names are real, and 39 labels do characterise a named company's terms.** An earlier
  draft of this bullet said "nothing here is a statement about any named company's filings". That
  was false and is retracted. The five `flag_*` tasks record exactly such statements — 39 items
  carrying values like `flag_offmarket_liqpref`, `flag_full_ratchet`, `flag_uncapped_participation`,
  `flag_missing_pro_rata` and `flag_internal_inconsistency` against the filings of named companies.
  What is true is narrower, and is what we assert: each flag is one annotator's reading of one
  clause in one filing, recorded with a validating quote from that document's own text. It is not a
  claim about the company's conduct, its present-day terms, or its valuation; the paper draws no
  conclusion about any company; and anyone disputing a flag can check the quote against the filing.
  Characterisations such as "off-market" are terms of art applied to a clause, not a judgement of
  the filer.
- **Single-annotator labels can be wrong.** Every label ships with its validating quote and its
  source filing precisely so that a disagreeing reader can check the record instead of being asked
  to trust it.

## 11. Licences shipped

| artifact | licence | file |
|---|---|---|
| code | MIT | `LICENSE` |
| data | **UNRESOLVED** — see §3 | none exists |

The `LICENSE` copyright line names the author. The anonymous review mirror stripped it;
this camera-ready tree restores it.
