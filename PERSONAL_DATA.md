# Personal data in this corpus

Companion to `DATA_STATEMENT.md`. It states what personal data the released filing texts contain,
how it got there, and what has and has not been done about it. Every count below was produced by a
script in the paper's audit directory and can be reproduced; none is an estimate.

---

## 1. What is present

**758 of the 1,123 plain-text filing documents (67.5%) carry at least one conformed signature with a
name** — the `/s/ Jane Q. Public` convention EDGAR uses in place of a wet signature. Across the
corpus there are **3,341** `/s/` markers, **3,217** of them followed by a parsable name. Three
documents are unsigned templates whose markers are blank (`By: /s/ By: /s/ Name: Title:`).

Signatories are the officers, directors, investors and occasionally the notaries who executed the
instrument. Names also appear outside signature blocks: in compensation tables, in
designated-director clauses, and typed underneath the conformed signature. **2,768 of the 3,341
blocks have their signed name appear again elsewhere in the same document.**

Measured by `paper-a/audit/sigblocks.py`, which reports both counts and their definitions, because
the looser test used earlier ( `/s/` followed by any word character) returned 759 by matching the
word "By" in an unsigned template as though it were a person.

## 2. How it got there, and what has not been done

The documents were retrieved **as published** from the SEC's EDGAR system and stored unchanged.
**No redaction, masking or pseudonymisation has been applied, and none is claimed.** The text you
read in this repository is the text the SEC serves at `sec.gov`, whitespace-collapsed by the HTML
extraction and otherwise untouched.

We do not assert a right to redistribute the filing texts, and we do not assert that we lack one.
See `DATA_STATEMENT.md` §3 for the licensing position, which is deliberately left open.

## 3. What the derived artifacts contain — verified, not asserted

The claim worth checking is that no personal name is **aggregated or indexed** anywhere in the
artifacts the pipeline produces, as opposed to appearing incidentally inside a verbatim excerpt.
`paper-a/audit/namescan.py` tests it by deriving all **1,430** distinct signed names and scanning
every derived artifact for them:

| artifact group | files scanned | files containing a signed name |
|---|---|---|
| generated LaTeX tables | 10 | **0** |
| figures (PDF, text extracted) | 5 | **0** |
| the compiled paper (PDF) | 1 | **0** |
| derived `out/` tree | 195 | **1** (below) |
| `NUMBERS.md` | 1 | **0** |
| results store | 26 | **0** |
| model response files | 2,428 | **0** |
| manifests and scorecards | 2,386 | **0** |
| oracle annotation (not a derived artifact) | 60 | **0** |

**Nothing aggregates or indexes names.** There is no list of people, no name column, and no
name-keyed record anywhere in the pipeline's output. No model response reproduced a signatory's
name, across 2,428 response files.

**Where the measurement itself is the exception, stated rather than left to be discovered.** The
instrument that produced the 758 figure necessarily builds what the sentence above says does not
exist: a JSON index of 3,217 parsed names with byte offsets, and a flat pool of the 1,430 distinct
names. Those two files are **not released and not committed to version control** — they are
`.gitignore`d in the working repository, because a name index in git history cannot be taken back.
The scripts that build them are tracked, so any reader with the corpus regenerates both in one
command and can re-derive every number here. The measurer is versioned; the list of people is not.

**The one exception, named rather than glossed.** `out/annotation/READING_PACK.md` is the blind
reading pack for the 154-item self-adjudication, and it reproduces **verbatim** the window text each
model was shown. Five signed names occur inside those excerpts, two of them inside a conformed
signature (`/s/ Steven C. Quay`, `/s/ Scott Youmans`) and three in the body of a filing — an
executive-compensation table and a designated-director clause. That file aggregates *excerpts*, not
names, and it exists so a reviewer can verify the re-read was actually blind. It is reported here
rather than removed, because removing it would remove the evidence for a claim the paper makes about
its own annotation procedure.

A scan for a negative is only worth its positive control, so `namescan.py` plants a real name and
requires it to be found in plain text, in a U+00A0-joined form, inside a JSON string, and in a
freshly compiled PDF read back through `pdftotext`, before any clean result counts. One file was not
scanned at all and is listed as such: `out/repair/local.log` is zero bytes.

## 4. The windowed extracts shown to models

The benchmark shows each model a windowed extract, not a whole filing. **6 of the 470 windows in use
contain a named conformed signature** (8 of the 524 window files on disk). Those six are not edited:
they are the exact inputs every measured response was produced against, and changing one would
invalidate the results measured on it.

## 5. Removal requests

A removal process exists. If you are named in one of these documents and want the document removed
from this repository, it will be removed on request, and the affected items will be marked withdrawn
rather than silently dropped.

**The contact address is supplied on publication.** It is withheld here because this repository is
under double-blind review and an address would identify the author. This is the only place in this
document where something is deliberately omitted.

## 6. What this document does not do

- It does not offer a legal opinion. `DATA_STATEMENT.md` §3 states the facts about licensing and
  declines the conclusion, and the same applies to personal data.
- It does not claim the data is anonymous, de-identified, or minimised. It is none of those.
- It does not claim redaction would fix anything. It was measured: 2,768 of 3,341 signed names recur
  outside their own signature block, so masking the blocks would leave most of those names in place.
- It does not claim the paper draws conclusions about any named person. It draws none — but 39
  `flag_*` items do characterise a **named company's** terms, and `DATA_STATEMENT.md` §10 states that
  plainly and retracts the earlier sentence that denied it.

---

*Counts in this file are reproduced by `python3 audit/sigblocks.py`, `python3 audit/namescan.py` and
`python3 audit/redaction_impact.py` in the paper's audit directory.*
