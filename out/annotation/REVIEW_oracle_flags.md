# Model-flagged oracle review (Block 3a)

> STATUS: settled - all 7 flags adjudicated by the author - generated for 12 configurations

Every item below is one where the configurations' modal answers agree with each other and differ from the stored oracle label. **This is a worklist, not a finding.** The models flag; they do not decide. A flag becomes an error only when the author has read the source document and upheld it, and the counts of upheld and rejected flags are reported whichever way they come out.

- flags raised: **7** (4 unanimous, 3 with one dissenter)
- of the unanimous, **0** also clear the run floor: every configuration held its answer on at least 18 of its 20 runs. Across the flags the weakest configuration's own support ranges from 5 to 17 runs. The rest are listed too, marked, because agreement between configurations that each barely preferred their answer is the weaker claim and the author needs to see which is which.
- tasks touched: 5
- flags upheld: **0**
- flags rejected: **0**
- flags excluded: **7**

## 1. `preference_seniority` / `878720_000089843001500356` (unanimous)

- models say: **stacked**
- oracle says: **pari-passu**
- runs backing the models' answer: 235 of 237 (99.2%)
- source: https://www.sec.gov/Archives/edgar/data/878720/000089843001500356/dex41.txt
- stored validating quote: nally, prior to June 1, 2002, the Series B Preferred Stock shall rank pari passu with the Series A Preferred Stock and the Series C Preferred Stock as to liquidation, and shall be senior to or pari pa
- verdict: **excluded** (basis: examined)
- adjudication note: window states both readings, split by a June 2002 date; the task carries no as-of date, so neither label is wrong

## 2. `participation_type` / `1722271_000091205720000111` (unanimous)

- models say: **capped**
- oracle says: **participating**
- runs backing the models' answer: 228 of 237 (96.2%)
- source: https://www.sec.gov/Archives/edgar/data/1722271/000091205720000111/
- stored validating quote: after the payment in full of all preferential amounts ... the remaining assets ... shall be distributed among the holders of the shares of Preferred Stock and Common Stock, pro rata based on the numbe
- verdict: **excluded** (basis: examined)
- adjudication note: the same sentence the oracle anchored on carries an explicit 3x Maximum Participation Amount proviso

## 3. `preference_seniority` / `1585521_000119312519083351` (unanimous)

- models say: **stacked**
- oracle says: **pari-passu**
- runs backing the models' answer: 224 of 226 (99.1%)
- source: https://www.sec.gov/Archives/edgar/data/1585521/000119312519083351/d642624dex31.htm
- stored validating quote: the Series D Preferred Stock shall be distributed among them on a pro rata basis according to the respective amounts which would otherwise be payable upon such distribution if all amounts payable with
- verdict: **excluded** (basis: examined)
- adjudication note: window carries both tell-tales: the pro rata phrase the label anchored on governs pro-ration within the Series B/C/D tier, while the clause placing Series A after them is truncated mid-sentence, so the window does not fix the ranking

## 4. `liquidation_preference_multiple` / `1479290_000119312514020967` (unanimous)

- models say: **other**
- oracle says: **1x**
- runs backing the models' answer: 220 of 229 (96.1%)
- source: _no URL recorded_
- stored validating quote: entitled to receive one (1) times the original issue price, or $22.425 per share, plus all declared and unpaid divide
- verdict: **excluded** (basis: examined)
- adjudication note: one sentence states one (1) times for Series E-1 to E-4 and one and one-half (1.5) times for Series E-5; the question names no series and the answer space defines other as a multiple outside 1x, 2x and 3x, so 1x and other are each supported

## 5. `price_per_share` / `mobile_systems_s1` (11/12)

- models say: **2.0**
- oracle says: **0.2**
- runs backing the models' answer: 220 of 239 (92.1%)
- source: _no URL recorded_
- stored validating quote: shares of common stock under our 2007 Stock Option/Stock Issuance Plan, as amended, at a purchase price of $0.20 per share for an aggregate consideration of $2,400. The issuance and sale of these secu
- verdict: **excluded** (basis: examined)
- adjudication note: window carries a $2.00 Series A-1 preferred price and a $0.20 common-stock plan price and the question does not name the round, so the window does not fix which issuance is asked about

## 6. `flag_uncapped_participation` / `1604950_000119312517316695` (11/12)

- models say: **no**
- oracle says: **yes**
- runs backing the models' answer: 220 of 236 (93.2%)
- source: _no URL recorded_
- stored validating quote: referred Stock, the remaining assets of the Corporation available for distribution to its stockholders shall be distributed among the holders of the shares of Preferred Stock and Common Stock, pro rat
- verdict: **excluded** (basis: examined)
- adjudication note: window states a three (3) times Preferred Maximum Participation Amount, but whether a defined term of that name caps the participation requires tracing the conditional threshold against figures defined elsewhere, so the excerpt as windowed supports both readings

## 7. `flag_uncapped_participation` / `1722271_000091205720000111` (11/12)

- models say: **no**
- oracle says: **yes**
- runs backing the models' answer: 220 of 234 (94.0%)
- source: _no URL recorded_
- stored validating quote: s 2.1 or 2.2 above, the remaining assets of the Corporation available for distribution to its stockholders shall be distributed among the holders of the shares of Preferred Stock and Common Stock, pro
- verdict: **excluded** (basis: examined)
- adjudication note: same filing and same three (3) times Maximum Participation Amount proviso already examined under the participation_type flag on this filing; excluded on the same basis
