# FLAG_EVIDENCE.md — the source text behind each of the 7 model flags

> STATUS: settled · prepared 2026-08-02 · adjudicated by the author 2026-08-02 · all 7 excluded, basis `examined`

Companion to `REVIEW_oracle_flags.md` (the worklist) and `ADJUDICATION.md` (who decides — the author,
rule 3: a document supporting both readings means *excluded*, not "pick the original").

Why this file exists: `model_flags.csv` records 5 of the 7 as
`adjudication_basis = blanket` — "excluded under a blanket decision covering all seven flags; this
item's text was NOT individually adjudicated". The paper's own provenance checklist, item (5), says
**"emit a specific reason per rejection, since a rejection reported only as a count cannot be
audited"**. Five of seven currently have no per-item reason. This file supplies the text so each can
get one.

Every quote below is a verbatim span from the document on disk (or, for the one item with no local
full text, from the SEC copy fetched 2026-08-02 and named). The **window** column matters
independently of the full document: the model only ever saw the window, so an item can be an oracle
error (the window supports the models) or an item-construction defect (the window supports neither),
and those are different verdicts.

---

## Already examined — recorded, not re-opened

| # | leaf / item | verdict | basis |
|---|---|---|---|
| 1 | `preference_seniority` / `878720_…356` (Right Start) | excluded | window states both readings, split by a June 2002 date; the task carries no as-of date |
| 2 | `participation_type` / `1722271_…111` (Akouos) | excluded | the sentence the oracle anchored on carries an explicit 3× Maximum Participation Amount proviso |

**Item 2 is load-bearing for items 6 and 7 below** and is the reason this file exists: the 3× cap
found there is the *same clause* that decides `flag_uncapped_participation` on the *same filing*.

---

## 3. `preference_seniority` / `1585521_000119312519083351` — Zoom Video Communications

- oracle **pari-passu** · models **stacked** (12/12, 224/226 runs)
- no full text on disk; SEC copy fetched 2026-08-02 from the URL in the oracle record

Section 3(a)(i), verbatim: the holders of Series B, C and D

> "shall be entitled to receive, **prior and in preference to any Distribution** of any of the assets
> of the Corporation **to the holders of the Series A Preferred Stock** or the holders of Class A
> Common Stock or Class B Common Stock…"

Section 3(a)(ii), verbatim: the holders of Series A

> "shall be entitled to receive, out of the remaining assets of the Corporation legally available
> **after** the holders of the Series B Preferred Stock, the holders of the Series C Preferred Stock
> and the holders of the Series D Preferred Stock **have been paid or set aside**…"

**What the window contained.** Both tell-tales. The phrase the oracle anchored on — "distributed
among them on a pro rata basis" — is present, but it governs only pro-ration *within* the B/C/D tier
when assets are short, which happens under a stacked structure too. The window also carries
"…out of the remaining assets … after the holders of the Series B … Series C … and", truncated
mid-clause.

**Against the task's own taxonomy.** `stacked` = "a senior series is paid its full liquidation
preference FIRST, before any junior series receives anything. Tell-tale: … one series' preference
paid 'prior to' another series receiving any distribution." The charter uses that exact
construction. `pari-passu` = "no series is paid before another" — false here for A against B/C/D.

**The counter-case, stated fairly.** B, C and D *are* pari passu with one another, and the window
truncates the "after" clause mid-sentence, so a reader could call the window under-specified rather
than the label wrong.

---

## 4. `liquidation_preference_multiple` / `1479290_000119312514020967` — Revance Therapeutics

- oracle **1x** · models **other** (12/12, 220/229 runs)

The window (one sentence, both values inside it):

> "the holders of the Series E-1, E-2, E-3 and E-4 convertible preferred stock are entitled to
> receive **one (1) times** the original issue price, or $22.425 per share … while the holders of
> the Series E-5 convertible preferred stock are entitled to receive **one and one-half (1.5) times**
> the original issue price, or $33.6375 per share…"

The task asks for "the liquidation preference MULTIPLE" and **names no series**. Its answer space
defines `other` as "a multiple other than 1x, 2x, or 3x (**e.g., 1.5x**…)". So `1x` and `other` are
each fully supported by the same window.

This is `ADJUDICATION.md` rule 3 on its face — two readings, both supported, no way to choose from
the document. It is also the multi-value-in-one-excerpt class the project already logged.

---

## 5. `price_per_share` / `mobile_systems_s1` — WhiteGlove Health

- oracle **0.2** · models **2.0** (11/12, 220/239 runs)
- no URL in the oracle record and no full text on disk; the window is all that exists

The task: "extract the PRICE PER SHARE **of the preferred stock** in **a priced equity financing
round**, as a bare decimal."

The window contains exactly one preferred-stock financing price and one common-stock price:

> "we sold 873,852 shares of **Series A-1 Preferred Stock at a price of $2.00 per share** for gross
> proceeds of approximately $1.75 million pursuant to that certain Series A-1 Preferred Stock
> Purchase Agreement…"

> "we sold and issued an aggregate of 12,000 shares of **common stock** under our 2007 Stock
> Option/Stock Issuance Plan, as amended, at a **purchase price of $0.20 per share** for an
> aggregate consideration of $2,400 … exempt … pursuant to Rule 701 … a compensatory benefit plan"

The oracle's stored anchor is "purchase price of $0.20 per share" — the **common-stock option-plan**
issuance, not a preferred financing round. On the task as written the answer is 2.0.

**The counter-case, stated fairly.** The window holds several dollar figures, so one could call it
ambiguous — but only one of them is a preferred-stock price, which is what the question asks for.

---

## 6. `flag_uncapped_participation` / `1604950_000119312517316695` — scPharmaceuticals

- oracle **yes** (uncapped) · models **no** (11/12, 220/236 runs)

Section 2.2, verbatim, and **this sentence is inside the window the model was shown**:

> "…the remaining assets … shall be distributed among the holders of the shares of Preferred Stock
> and Common Stock, pro rata … **provided, however, that (x) if the aggregate amount … which the
> holders of Preferred Stock are entitled to receive under Subsections 2.1 and 2.2 shall exceed
> three (3) times the Series A Original Issue Price per share** … or **three (3) times the Series B
> Original Issue Price** per share … (the "**Preferred Maximum Participation Amount**"), each holder
> of Preferred Stock shall be entitled to receive … the greater of (i) the applicable Preferred
> Maximum Participation Amount and (ii) the amount such holder would have received if all shares of
> Preferred Stock had been converted into Common Stock…"

The task's taxonomy puts this in `no` explicitly: `no` covers "(2) **CAPPED participation** (preference
+ participation up to a cap, **e.g. 'until stockholders have received 3x their investment'**)".

**The counter-case, and it is a real one.** `participation_type/source.py` warns in this project's own
words that a defined term named "Maximum Participation Amount" "SOUNDS like it means capped
participation" but that classifying it correctly "requires tracing through a conditional threshold and
comparing it against the ACTUAL dollar figures defined elsewhere" (the Pfenex item). That warning is
about whether the cap *binds*. Here the cap is stated as a multiple of the OIP rather than a
cross-referenced dollar figure, so no arithmetic elsewhere is needed to see it — but the warning is
why this is your call and not a lookup.

---

## 7. `flag_uncapped_participation` / `1722271_000091205720000111` — Akouos

- oracle **yes** (uncapped) · models **no** (11/12, 220/234 runs)

Section 2.3, verbatim, **inside the window the model was shown**:

> "…provided, however, that if the aggregate amount which the holders of any series of Preferred
> Stock are entitled to receive under Subsections 2.1, 2.2 and 2.3 **shall exceed three (3) times the
> Original Issue Price** applicable to such series of Preferred Stock … (the "**Maximum Participation
> Amount**"), each holder … shall be entitled to receive … the greater of (i) the Maximum
> Participation Amount and (ii) the amount such holder would have received if all shares of Preferred
> Stock had been converted into Common Stock…"

**This is the same filing and the same proviso already examined under item 2**, where the recorded
basis reads: "the same sentence the oracle anchored on carries an explicit 3x Maximum Participation
Amount proviso." Taking that finding as given, the two oracle labels on this one filing disagree with
each other: `participation_type` was excluded *because* a 3× cap exists, while
`flag_uncapped_participation` still asserts the participation is **uncapped**.

---

## What is at stake in the paper

The current text, `main.tex` L202–212 (page 3 of the PDF), reads:

> "The author adjudicated all 7 as **excluded**: none upheld as an oracle error, none rejected as an
> oracle vindication, **the task as written admitting both readings in each case**. No label was
> changed, and the 7 items leave every reported population, which is why the headline counts are 427
> items over 52 tasks rather than 434."

"The task as written admitting both readings in each case" is a claim about all seven. Items 5, 6 and
7 do not obviously fit it: in each, the task's own written taxonomy or field definition appears to
select the models' answer. If any of those three is upheld rather than excluded, that sentence is
false as printed and must be rewritten, `Table 10`'s adjudication column changes, and
`PROTOCOL.md` §3 requires the affected leaf to be re-scored with the effect on the headline reported.

## Resolution (2026-08-02)

The author read each item above against this evidence, with the models'-right case stated per item,
and ruled on every one individually: **all 7 excluded, none upheld, none rejected**, each with a
per-item reason now recorded in `model_flags.csv` (`adjudication_basis = examined` on all 7; the
`blanket` basis no longer exists). The three items flagged above as candidate oracle errors were
each excluded as under-determined by the task as written rather than upheld:

- **Flag 5 (WhiteGlove)** — the window holds a $2.00 preferred price and a $0.20 common-stock plan
  price and the question does not fix which issuance is asked about.
- **Flag 6 (scPharmaceuticals)** — the 3x proviso is in the window, but whether a defined term named
  Maximum Participation Amount binds requires tracing the conditional threshold against issue-price
  figures defined elsewhere (the Pfenex caveat, `participation_type/task.py`).
- **Flag 7 (Akouos)** — same filing and same proviso as flag 2; excluded on the same basis, which
  also removes the apparent contradiction between the two labels on this filing (both items are now
  out of the corpus, so neither label is asserted by any reported number).

No label changed and the exclusion set is identical to the pre-existing one, so the corpus stays
**427 items / 52 tasks** and no re-score is required (`adjudication.exclusions()` verified
unchanged). The paper edit this forced: the Limitations paragraph that described a "blanket
decision without individual textual adjudication" now describes the per-item readings.
Pre-fix column preserved at `model_flags_pre_adjudication_2026-08-02.csv` (the file as it stood
before the five verdicts were recorded, kept so the before-state stays auditable).
