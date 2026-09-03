# Blind reading pack -- 154 items

One entry per row of `blind_pack.csv`, in the same order and under the same `row_id`.
Answer in the CSV, not here. Neither the stored label nor its validating quote appears
in this file; if you find either, stop, because the reading is no longer blind.

### R0001 · board_seats_investor · 0001047469-09-010296_a2195611zex-4_1
**Question.** Extract the number of board seats an investor has the right to designate (5.1).
**Field.** `board_seats_investor` -- the number of board seats the investor/investor class may designate
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
eholders to so nominate such additional designees and (y) designate such additional designees nominated by the KKR Shareholders to fill such newly-created vacancies. Each such designee whom the KKR Shareholders shall actually nominate pursuant to this Section 2.1(c) and is thereafter elected to the Board to serve as a Director shall be referred to herein as a “ KKR Designee ”.  In addition, in the event that the KKR Shareholders have the right to designate only one Director   5   pursuant to this Section 2.1(b), then the KKR Shareholders shall also have the right to designate one additional individual (an “ Observer ”) to attend all Board meetings; provided , that such Observer shall not have the right to participate in any vote, consent or other action of the Board or its committees.   (c)            Following the Closing Date, so long as the Goldman Shareholders collectively beneficially own, directly or indirectly, at least 5% of the then outstanding shares of Common Stock, the Goldman Shareholders shall have the right, but not the obligation, to nominate to the Board one designee.  In addition, so long as the Goldman Shareholders are entitled to nominate one Director, the Goldman Shareholders shall have the right to designate one Observer to attend all meetings of the Board; provided , that, such Observer shall not have the right to participate in any
```

### R0002 · fully_diluted_basis · ignentertainment_ex
**Question.** Classify capitalization definition as fully-diluted or issued-outstanding basis (3.4).
**Field.** `fully_diluted_basis` -- Whether cap is computed on fully-diluted or issued-outstanding basis.
**Answer.** one of: fully-diluted, issued-outstanding, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1101547/000104746905019338/a2158851zex-4_02.htm

**Text shown to the model:**

```
y provision of this Agreement calls for any calculation based on a number of shares of Common Stock issued and outstanding or held by a Stockholder, the number of shares deemed to be issued and outstanding or held by that Stockholder, as applicable, shall be the total number of shares of Common Stock then issued and outstanding or owned by the Stockholder, as applicable, on a Fully-Diluted basis. Section 1.4 Defined Terms . The following capitalized terms, as used in this Agreement, shall have the meanings set forth below. An &#147; Affiliate &#148; of any Person means a Person that, directly or indirectly, through one or more intermediarie
```

### R0003 · option_strike_409a · 0001125282-06-006236_0p03
**Question.** Extract the stock option exercise price per share from a grant agreement (6.4).
**Field.** `option_strike_409a` -- the exercise price (strike price) per share of the granted option
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
TARGET GRANT: the option grant stated to have an exercise price of $0.03 per share (see below).

ice of $0.25 per share.         • On April 27, 2004, we granted options to fourteen of our employees to purchase an aggregate of 509,300 shares of our common stock under our Amended and Restated Stock Option Plan at an exercise price of $0.25 per share.         • On April 30, 2004, we issued 200,000 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $0.03 per share.         • On August 5, 2004, we granted options to seven of our employees to purchase an aggregate of 137,000 shares of our common stock under our Amended and Restated Stock Option Plan at an exercise price of $0.25 per share. II-2 Back to Contents   • On August 16, 2004, we issued 3,000 shares, 3,124 shares and 5,000 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $0.60 per share, $0.25 per share and $1.00 per share, respectively.         • On September 29, 2004, we issued 875 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $0.25 per share.         • On October 26, 2004, we granted options to 12 of our employees to purchase an aggregate of 325,750 shares of our common stock under our Amended and Restated Stock
```

### R0004 · safe_pre_post · 1657493_000121390021028831
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1657493/000121390021028831/ea141441ex5-4_rentberryinc.htm

**Text shown to the model:**

```
EX1A-5 VOTG TRST 3 ea141441ex5-4_rentberryinc.htm FORM OF 2021 SAFE NOTE AND VOTING AGREEMENT Exhibit 5.4   THIS INSTRUMENT AND ANY SECURITIES ISSUABLE PURSUANT HERETO HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE “ SECURITIES ACT ”), OR UNDER THE SECURITIES LAWS OF CERTAIN STATES. THESE SECURITIES MAY NOT BE OFFERED, SOLD OR OTHERWISE TRANSFERRED, PLEDGED OR HYPOTHECATED EXCEPT AS PERMITTED IN THIS SAFE AND UNDER THE ACT AND APPLICABLE STATE SECURITIES LAWS PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT OR AN EXEMPTION THEREFROM.   RENTBERRY, INC.   SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by __________ , (the “ Investor ”) of $_________ (the “ Purchase Amount ”) on or about March 23, 2021, RENTBERRY, INC. , a Delaware corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   The “ Pre-Money Valuation Cap ” is $15,000,000.   The “ Discount Rate ” is 20%.   See Section 2 for certain additional defined terms.   1. Events   (a) Next Equity Financing . If there is a Next Equity Financing before the expiration or termination of this Safe, on the initial closing of such Next Equity Financing, this Safe will automatically convert into the number of shares of Safe Preferred Stock equal to the Purchase Amount divided by the Conversion Price.   In connection with the automatic conversion of this Safe into shares of Safe Preferred Stock, the Investor will execute and deliver to the Company all of the transaction documents related to the Next Equity Financing; provided, that such documents are the same documents to be entered into with the purchasers of Standard Preferred Stock, with appropriate variations for the Safe Preferred Stock if applicable, and provided further, that such documents have customary exceptions to any drag-along applicable to the Investor, including, without limitation, limited representations and warranties and limited liability and indemnification obligations on the part of the Investor.   (b) Liquidity Event . If there is a Liquidity Event before the termination of this Safe, the Investor will automatically receive, immediately prior to or concurrent with the consummation of such Liquidity Event, a number of shares of Common Stock equal to the Purchase Amount divided by the Liquidity Price (the “ Liquidity Event Shares ”).   (c) Safe Expiration Conversion . If the Next Equity Financing Conversion has not occurred prior to December 31, 202
```

### R0005 · option_strike_409a · 0001193125-11-194811_7p5
**Question.** Extract the stock option exercise price per share from a grant agreement (6.4).
**Field.** `option_strike_409a` -- the exercise price (strike price) per share of the granted option
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
TARGET GRANT: the option grant stated to have an exercise price of $7.50 per share (see below).

rities were deemed to be exempt from registration pursuant to Rule 701 promulgated under the Securities Act as transactions pursuant to a compensatory benefit plan approved by the registrant’s board of directors.     •   On May 4, 2011, we granted options under our 2007 Stock Option/Stock Issuance Plan, as amended, to purchase 130,500 shares of our common stock to our employees, directors and consultants, having and exercise price of $7.50 per share for an aggregate exercise price of $978,750. The issuance and sale of these securities were deemed to be exempt from registration pursuant to Rule 701 promulgated under the Securities Act as transactions pursuant to a compensatory benefit plan approved by the registrant’s board of directors.     •   On May 17, 2011, we sold and issued 1,500 shares of common stock pursuant to an option exercise by the holder of a stock option issued under our 2007 Stock Option/Stock Issuance Plan, as amended, at a purchase price of $0.61 per share for an aggregate consideration of $915. The issuance and sale of these securities were deemed to be exempt from registration pursuant to Rule 701 promulgated under the Securities Act as transactions pursuant to a compensatory benefit plan approved by the registrant’s board of directors.     •   On May 27, 2011, we sold and issued 15,000 shares of common stock p
```

### R0006 · safe_pre_post · 1777274_000121390020033888
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1777274/000121390020033888/ea128838ex3-1_oraclehealth.htm

**Text shown to the model:**

```
EX1A-3 HLDRS RTS 5 ea128838ex3-1_oraclehealth.htm FORM OF SIMPLE AGREEMENT FOR FUTURE EQUITY (SAFE) Exhibit 3.1   Version 1.1   POST-MONEY VALUATION CAP   THIS INSTRUMENT AND ANY SECURITIES ISSUABLE PURSUANT HERETO HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE “ SECURITIES ACT ”), OR UNDER THE SECURITIES LAWS OF CERTAIN STATES. THESE SECURITIES MAY NOT BE OFFERED, SOLD OR OTHERWISE TRANSFERRED, PLEDGED OR HYPOTHECATED EXCEPT AS PERMITTED IN THIS SAFE AND UNDER THE ACT AND APPLICABLE STATE SECURITIES LAWS PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT OR AN EXEMPTION THEREFROM.   Oracle Health, inc.   SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by [Investor Name] (the “ Investor ”) of $[_____________] (the “ Purchase Amount ”) on or about [Date of Safe], Oracle Health, Inc., a Delaware corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   This Safe is one of the forms available at http://ycombinator.com/documents and the Company and the Investor agree that neither one has modified the form, except to fill in blanks and bracketed terms.   The “ Post-Money Valuation Cap ” is $[_____________]. See Section 2 for certain additional defined terms.   1.  Events   (a)  Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the greater of: (1) the number of shares of Standard Preferred Stock equal to the Purchase Amount divided by the lowest price per share of the Standard Preferred Stock; or (2) the number of sh
```

### R0007 · option_strike_409a · 0001125282-06-006236_0p25
**Question.** Extract the stock option exercise price per share from a grant agreement (6.4).
**Field.** `option_strike_409a` -- the exercise price (strike price) per share of the granted option
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
TARGET GRANT: the option grant stated to have an exercise price of $0.25 per share (see below).

volved in the sales and the certificates representing the securities sold and issued contain legends restricting the transfer of the securities without registration under the Securities Act or an applicable exemption from registration.   • On August 21, 2003, we granted options to six of our employees to purchase an aggregate of 15,500 shares of our common stock under our Amended and Restated Stock Option Plan at an exercise price of $0.25 per share.         • On October 1, 2003, we issued 750 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $0.25 per share.         • On October 9, 2003, we issued 5,000 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $0.60 per share.         • On October 28, 2003, we granted options to ten of our employees to purchase an aggregate of 35,000 shares of our common stock under our Amended and Restated Stock Option Plan at an exercise price of $0.25 per share.         • On December 4, 2003, we issued 1,000 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $0.60 per share.         • On December 19, 2003, we granted options to ten of our employee
```

### R0008 · safe_valuation_cap · 2010788_000149315224005725_cap
**Question.** Extract the valuation cap from a SAFE agreement (2.1.1)
**Field.** `safe_valuation_cap` -- the valuation cap in dollars as a bare integer (no $ or commas)
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
, INC.   SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the investment by ____ (the “ Investor ”) of $800,000 (the “ Purchase Amount ”) as of ___, 2023, Invizyne Technologies, Inc., a Nevada corporation (the “ Company ”), issues to the Investor the right to certain equity securities of the Company, subject to the terms and conditions described below.   The “ Pre-Money Valuation Cap ” is one-hundred million dollars ($100,000,000.00)   The “ Discount Rate ” is 80.00%.   See Section 2 for certain additional defined terms.   1. Events   (a) Equity Financing . If there is and upon the first Equity Financing after the making of this SAFE and before the termination of this SAFE, on the initial closing of such Equity Financing, this SAFE will automatically convert into the number of Next Round Equity equal to the Purchase Amount divided by the Conversion Price.   In connection with the automatic conversion of this SAFE into Next Round Equity pursuant to this Section 1(a), the Investor will agree to and execute and deliver to the Company all the transaction documents related to the Equity Financing; provided, that such documents (i) are the same documents to be entered into with the purchasers of Next Round Equity, with appropriate variations to the extent required by this SAFE, and (ii) have customary exceptions to an
```

### R0009 · option_strike_409a · 0001125282-06-007804_2p0
**Question.** Extract the stock option exercise price per share from a grant agreement (6.4).
**Field.** `option_strike_409a` -- the exercise price (strike price) per share of the granted option
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
TARGET GRANT: the option grant stated to have an exercise price of $2.00 per share (see below).

at an exercise price of $2.50 per share.         • On March 7, 2006, we issued 250 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $0.50 per share.   II-3 Back to Contents   • On April 10, 2006, we issued 1,000 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $2.00 per share.         • On April 26, 2006, we granted options to 38 of our employees to purchase an aggregate of 353,375 shares of our common stock under our Amended and Restated Stock Option Plan at an exercise price of $22.00 per share.         • On May 24, 2006, we issued 625 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $0.50 per share.         • On June 9, 2006, we issued 500 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $0.50 per share.         • On July 13, 2006, we issued 1,500 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $2.00 per share.         • On July 18, 2006, we granted options to two of our employees to purchase an
```

### R0010 · cliff_present · 0000020740-17-000006_a201610kex1012
**Question.** Classify whether a vesting schedule includes a cliff blockage period (6.2).
**Field.** `cliff_present` -- yes if the schedule has a cliff blockage period, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
incorporated herein as though set forth herein in full. Capitalized terms used herein and not otherwise defined herein shall have the respective meanings specified in the Plan. Section 1 Restricted Stock Unit Award . The Company hereby awards to the Participant as of the Award Date,      Restricted Stock Units (the “ Units ”). Subject to Section 3 of this Agreement, twenty-five percent (25%) of such Units shall vest on each anniversary of the Award Date until all of such Units have vested; provided that, except as expressly provided in Section 3 of this Agreement, in the event that the Participant ceases to be an employee of the Company and all of its subsidiaries, he or she shall forfeit any Units which have not previously vested. Subject to Section 3 of this Agreement, promptly after such vesting the Company shall issue to the Participant one (1) share of Common Stock for each vested Unit, which payment shall in all events occur not later than the fifteenth day of the third calendar month following the date on which such Units vest. The Units shall not be transferable by the Participant by means of sale, assignment, exchange, pledge, gift, operation of law or otherwise. Section 2 Voting and Dividend Rights . Until the issuance of Common Stock to the Participant as provided in Section 1 of this Agreement, the Partici
```

### R0011 · flag_internal_inconsistency · ignentertainment_inconsistent
**Question.** Flag whether two real share-count citations in the same filing are numerically consistent (8.6).
**Field.** `flag_internal_inconsistency` -- true if the two cited share counts differ, false if they match
**Answer.** bool value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1101547/000104746905019338/a2158851zs-1.htm

**Text shown to the model:**

```
Citation A (Capitalization table (actual column)): "20,392,610 shares issued and outstanding, actual"

Citation B (Prospectus summary basis statement): "which includes 20,824,068 shares outstanding as of March 31, 2005"
```

### R0012 · securities_exemption · 1804648
**Question.** Classify which Securities Act exemption a Form D filing claimed (7.1).
**Field.** `securities_exemption` -- The federal exemption claimed in the Form D filing.
**Answer.** one of: 506b, 506c, 504, reg-a, other, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1804648/000180464820000004/primary_doc.xml

**Text shown to the model:**

```
<entityName>Material Impact Fund II, L.P.</entityName>
        <issuerAddress>
            <street1>131 Dartmouth Street</street1>
            <street2>Floor 3</street2>
            <city>Boston</city>
            <stateOrCountry>MA</stateOrCountry>
            <stateOrCountryDescription>MASSACHUSETTS</stateOrCountryDescription>
            <zipCode>02116</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>(617) 286-2577</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Limited Partnership</entityType>
        <yearOfInc>
            <withinFiveYears>true</withinFiveYears>
            <value>2020</value>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>N/A</firstName>
                <lastName>Material Impact Partners II, LLC</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o Material Impact</street1>
                <street2>131 Dartmouth Street, Floor 3</street2>
                <city>Boston</city>
                <stateOrCountry>MA</stateOrCountry>
                <stateOrCountryDescription>MASSACHUSETTS</stateOrCountryDescription>
                <zipCode>02116</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification>General Partner of the Issuer (the &quot;General Partner&quot;)</relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Carmichael</firstName>
                <lastName>Roberts</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o Material Impact</street1>
                <street2>131 Dartmouth Street, Floor 3</street2>
                <city>Boston</city>
                <stateOrCountry>MA</stateOrCountry>
                <stateOrCountryDescription>MASSACHUSETTS</stateOrCountryDescription>
                <zipCode>02116</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification>Managing Member of the General Partner</relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Adam</firstName>
                <lastName>Sharkawy</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o Material Impact</street1>
                <street2>131 Dartmouth Street, Floor 3</street2>
                <city>Boston</city>
                <stateOrCountry>MA</stateOrCountry>
                <stateOrCountryDescription>MASSACHUSETTS</stateOrCountryDescription>
                <zipCode>02116</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification>Managing Member of the General Partner</relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Pooled Investment Fund</industryGroupType>
            <investmentFundInfo>
                <investmentFundType>Venture Capital Fund</investmentFundType>
                <is40Act>false</is40Act>
            </investmentFundInfo>
        </industryGroup>
        <issuerSize>
            <revenueRange>Not Applicable</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06c</item>
            <item>3C</item>
            <item>3C.7</item>
        </federalExemptionsExclusions>
```

### R0013 · preference_seniority · 878720_000089843001500356
**Question.** Classify multi-series preferred liquidation seniority as pari-passu or stacked (1.3.4).
**Field.** `preference_seniority` -- Whether preferred series rank equally (pari-passu) or in a seniority order (stacked).
**Answer.** one of: pari-passu, stacked, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/878720/000089843001500356/dex41.txt

**Text shown to the model:**

```
r winding up of the Corporation, whether voluntary or involuntary, the holders of Series B Preferred Stock shall be entitled to receive with respect to each share, out of the assets of the Corporation, whether such assets are stated capital or surplus of any nature, an amount equal to One Hundred Dollars ($100.00) per share (the "Series B Preferred Liquidation Preference"), and no more, before any ----------------------------------------- payment shall be made or any assets distributed to the holders of Common Stock. Additionally, prior to June 1, 2002, the Series B Preferred Stock shall rank pari passu with the Series A Preferred Stock and the Series C Preferred Stock as to liquidation, and shall be senior to or pari passu with any other Preferred Stock issued by the Corporation subsequent to the date of issuance of the Series B Preferred Stock. After June 1, 2002, as to liquidation, (a) the Series A Preferred Stock shall be senior with respect to liquidation to the Series B Preferred Stock and the Series C Preferred Stock, (b) the Series B Preferred Stock shall rank pari passu with the Series C Preferred Stock, and (c) the Series B Preferred Stock and the Series C Preferred Stock shall be pari pa
```

### R0014 · board_seats_investor · 0001437749-22-001514_ex_325546
**Question.** Extract the number of board seats an investor has the right to designate (5.1).
**Field.** `board_seats_investor` -- the number of board seats the investor/investor class may designate
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
twithstanding anything in the Investment Agreements to the contrary, the Company will issue and sell to BDI at the Closing, and BDI will purchase, 2,400,000 shares of Common Stock, at a purchase price of $5.00 per share for an aggregate purchase price of $12,000,000, which shares will represent approximately 37.5% of the issued and outstanding shares of capital stock of the Company immediately following the Closing. BDI will have the right to designate one member of the Company's Board of Directors. Effective as of the Closing, the Company, BDI, and the other stockholders party thereto will enter into (i) an Amended and Restated Investors' Rights Agreement, substantially in the form attached hereto as Exhibit A, (ii) an Amended and Restated Voting Agreement, substantially in the form attached hereto as Exhibit B. and (iii) an Amended and Restated Right of First Refusal and Co-Sale Agreement, substantially in the form attached hereto as Exhibit C.   Except as amended by this letter agreement, the Investment Agreements shall remain in full force and effect in accordance with its terms. This letter agreement shall be governed by the laws of the State of Delaware, without giving effect to its conflicts of laws principles. This letter agreement may be executed in counterparts, each of which shall be deemed an original, but all of which when taken tog
```

### R0015 · round_size · 1651590
**Question.** Extract the total aggregate financing round size in dollars (1.2.1).
**Field.** `round_size` -- total aggregate dollar amount raised in the equity financing round
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1651590/000165159015000001/primary_doc.xml

**Text shown to the model:**

```
<entityName>Link Labs, Inc.</entityName>
        <issuerAddress>
            <street1>130 HOLIDAY COURT</street1>
            <street2>SUITE 100</street2>
            <city>ANNAPOLIS</city>
            <stateOrCountry>MD</stateOrCountry>
            <stateOrCountryDescription>MARYLAND</stateOrCountryDescription>
            <zipCode>21401</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>202-524-1390</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <withinFiveYears>true</withinFiveYears>
            <value>2015</value>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Brian</firstName>
                <middleName>E.</middleName>
                <lastName>Ray</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>130 Holiday Court</street1>
                <street2>Suite 100</street2>
                <city>Annapolis</city>
                <stateOrCountry>MD</stateOrCountry>
                <stateOrCountryDescription>MARYLAND</stateOrCountryDescription>
                <zipCode>21401</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Robert</firstName>
                <middleName>B.</middleName>
                <lastName>Proctor</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>130 Holiday Court</street1>
                <street2>Suite 100</street2>
                <city>Annapolis</city>
                <stateOrCountry>MD</stateOrCountry>
                <stateOrCountryDescription>MARYLAND</stateOrCountryDescription>
                <zipCode>21401</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Christopher</firstName>
                <middleName>G.</middleName>
                <lastName>College</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>130 Holiday Court</street1>
                <street2>Suite 100</street2>
                <city>Annapolis</city>
                <stateOrCountry>MD</stateOrCountry>
                <stateOrCountryDescription>MARYLAND</stateOrCountryDescription>
                <zipCode>21401</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Other Technology</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>Decline to Disclose</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06b</item>
        </federalExemptionsExclusions>
        <typeOfFiling>
            <newOrAmendment>
                <isAmendment>false</isAmendment>
            </newOrAmendment>
            <dateOfFirstSale>
                <value>2015-08-20</value>
            </dateOfFirstSale>
        </typeOfFiling>
        <durationOfOffering>
            <moreThanOneYear>false</moreThanOneYear>
        </durationOfOffering>
        <typesOfSecuritiesOffered>
            <isEquityType>true</isEquityType>
            <isSecurityToBeAcquiredType>true</isSecurityToBeAcquiredType>
            <isOtherType>true</isOtherType>
            <descriptionOfOtherType>The equity being offered is in the form of Series A Preferred Stock.  A portion of this equity has been issued upon the conversion of convertible notes.</descriptionOfOtherType>
        </typesOfSecuritiesOffered>
        <businessCombinationTransaction>
            <isBusinessCombinationTransaction>false</isBusinessCombinationTransaction>
            <clarificationOfResponse></clarificationOfResponse>
        </businessCombinationTransaction>
        <minimumInvestmentAccepted>0</minimumInvestmentAccepted>
        <salesCompensationList></salesCompensationList>
        <offeringSalesAmounts>
            <totalOfferingAmount>7263112</totalOfferingAmount>
            <totalAmountSold>5787732</totalAmountSold>
            <totalRemaining>1475380</totalRemaining>
```

### R0016 · information_rights · 0000950134-08-014307_f42787exv10w2
**Question.** Classify whether a document grants investors a live financial-reporting/information right (5.3).
**Field.** `information_rights` -- yes if a live obligation to deliver financials to investors exists, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
95131       Re:   Securities Purchase Agreement dated as of October 2, 2006 (the “2006 Securities     Purchase Agreement”) among Bell Microproducts Inc. (the “Company”) and The Teachers’ Retirement System of Alabama and The Employees’ Retirement System of Alabama (collectively “2006 Investor”) Gentlemen and Ladies, The 2006 Investor (a) understands and acknowledges that the Company is in the process of restating its financial statements and that the Company has been and will be unable to timely deliver the various financial statements and SEC reports as required in the 2006 Securities Purchase Agreement; (b) agrees that the Company shall have until December 31, 2008 to deliver the 2006 annual financial statements, March 31, 2009 to deliver the 2007 annual financial statements, and June 30, 2009 to deliver the 2008 annual financial statements; (c) waives any defaults which may otherwise arise or result from the failure to timely deliver each such financial statement and the related SEC report for time periods prior to the due date therefor set forth in clause (b) above; (d) waives any defaults which may otherwise arise or result from any representation or warranty made or deemed made with respect to the previously delivered financial statements which are the subject of the restatement and the related SEC reports; and (e
```

### R0017 · round_size · 1597815
**Question.** Extract the total aggregate financing round size in dollars (1.2.1).
**Field.** `round_size` -- total aggregate dollar amount raised in the equity financing round
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1597815/000159781514000002/primary_doc.xml

**Text shown to the model:**

```
<entityName>Handybook, Inc.</entityName>
        <issuerAddress>
            <street1>350 SEVENTH AVENUE, SUITE 1604</street1>
            <city>NEW YORK</city>
            <stateOrCountry>NY</stateOrCountry>
            <stateOrCountryDescription>NEW YORK</stateOrCountryDescription>
            <zipCode>10001</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>(617) 910-4813</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <withinFiveYears>true</withinFiveYears>
            <value>2012</value>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Oisin</firstName>
                <lastName>Hanrahan</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>350 Seventh Avenue, Suite 1604</street1>
                <city>New York</city>
                <stateOrCountry>NY</stateOrCountry>
                <stateOrCountryDescription>NEW YORK</stateOrCountryDescription>
                <zipCode>10001</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Umang</firstName>
                <lastName>Dua</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>350 Seventh Avenue, Suite 1604</street1>
                <city>New York</city>
                <stateOrCountry>NY</stateOrCountry>
                <stateOrCountryDescription>NEW YORK</stateOrCountryDescription>
                <zipCode>10001</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Other Technology</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>Decline to Disclose</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06b</item>
        </federalExemptionsExclusions>
        <typeOfFiling>
            <newOrAmendment>
                <isAmendment>true</isAmendment>
                <previousAccessionNumber>0001597815-14-000001</previousAccessionNumber>
            </newOrAmendment>
            <dateOfFirstSale>
                <value>2014-01-14</value>
            </dateOfFirstSale>
        </typeOfFiling>
        <durationOfOffering>
            <moreThanOneYear>false</moreThanOneYear>
        </durationOfOffering>
        <typesOfSecuritiesOffered>
            <isEquityType>true</isEquityType>
        </typesOfSecuritiesOffered>
        <businessCombinationTransaction>
            <isBusinessCombinationTransaction>true</isBusinessCombinationTransaction>
            <clarificationOfResponse></clarificationOfResponse>
        </businessCombinationTransaction>
        <minimumInvestmentAccepted>0</minimumInvestmentAccepted>
        <salesCompensationList></salesCompensationList>
        <offeringSalesAmounts>
            <totalOfferingAmount>3728926</totalOfferingAmount>
            <totalAmountSold>3728926</totalAmountSold>
            <totalRemaining>0</totalRemaining>
```

### R0018 · cliff_present · 0001299933-05-001251_exhibit2
**Question.** Classify whether a vesting schedule includes a cliff blockage period (6.2).
**Field.** `cliff_present` -- yes if the schedule has a cliff blockage period, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
EX-10.43 3 exhibit2.htm EX-10.43 EX-10.43 PLATO LEARNING, INC. BOARD OF DIRECTORS DIRECTORS COMPENSATION PLAN At the January 18, 2005 Board of Directors Meeting, the Board approved compensation for outside Directors as follows. Stock Option Grant and Cash Payment — New Directors Initiation:   •   15,000 Stock Options Grant @ FMV as of close of business on the date of election to the Board of Directors to vest immediately.   •   Prorated Cash payment ($20,000/12 X number of months remaining until the next Annual Meeting). Restricted Stock Award, Stock Option Grant & Cash Payment — Continuing Directors Annual Retainer & Meeting Preparations:   •   1,000 shares Restricted Stock Award @ FMV as of close of business on the date of the Annual Meeting to vest immediately with restrictions to lapse the earlier of five years, retirement or resignation from the Board of Directors [relates to director year going forward].   •   10,000 Stock Options Grant @ FMV as of close of business on the date of the Annual Meeting to vest immediately [relates to director year going forward].   •   $20,000 to be paid as soon as possible after the date of the Annual Meeting (except to Non-Employee Chairman of the Board, see below) [relates to director year going forward]. Cash and Stock Option Grant — for Non-Employee Chairman of
```

### R0019 · safe_cap_vs_discount_applies · creci_both_mfn
**Question.** Classify whether a SAFE uses cap, discount, or both-MFN for conversion pricing (2.1.3).
**Field.** `safe_cap_vs_discount_applies` -- Whether the SAFE's conversion price uses cap-only, discount-only, or both with MFN.
**Answer.** one of: cap, discount, both-mfn, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
resulting entity or (iii) a sale, lease or other disposition of all or substantially all of the assets of the Company.   “Company Capitalization” is calculated as of immediately prior to the Equity Financing and (without double-counting):   ● Includes all shares of Capital Stock issued and outstanding;   ● Includes all Converting Securities;   ● Includes all (i) issued and outstanding Options and (ii) Promised Options;   ● Includes the Unissued Option Pool; and   - 2 -     POST-MONEY VALUATION CAP WITH DISCOUNT   “ Conversion Price ” means either: (1) the Safe Price or (2) the Discount Price, whichever calculation results in a greater number of shares of Safe Preferred Stock.   “ Converting Securities ” includes this Safe and other convertible securities issued by the Company, including but not limited to: (i) other Safes; (ii) convertible promissory notes and other convertible debt instruments; and (iii) convertible securities that have the right to convert into shares of Capital Stock.   “ Discount Price ” means the price per share of the Standard Preferred Stock sold in the Equity Financing multiplied by the Discount Rate.   “ Dissolution Event ” means (i) a voluntary termination of operations, (ii) a general assignment for the benefit of the Company’s creditors or (iii) any other liquidation, dissolution or winding up of the Company ( excluding a Liquidity Event), whether voluntary or involuntary.   “ Dividend Amount ” means, with respect to any date on which the Company pays a dividend on its outstanding Common Stock, the amount of such dividend that is paid per share of Common Stock multiplied by (x) the Purchase Amount divided by (y) the Liquidity Price (treating the dividend date as a Liquidity Event solely for purposes of calculating such Liquidity Price).   “ Equity Financing ” means a bona fide transaction or series of transactions with the principal purpose of raising capital, pursuant to which the Company issues and sells Preferred Stock at a fixed valuation, including but not limited to, a pre-money or post-mo
```

### R0020 · vesting_schedule · 0001558370-21-008713_giii-20210628x8k
**Question.** Extract and normalize vesting schedule to canonical string format (6.1).
**Field.** `vesting_schedule` -- Normalized vesting schedule: e.g. '4yr/1yr-cliff', '3yr/no-cliff', '4yr/cliff'.
**Answer.** string value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
rowth company ☐ ​ If an emerging growth company, indicate by check mark if the registrant has elected not to use the extended transition period for complying with any new or revised financial accounting standards provided pursuant to Section 13(a) of the Exchange Act. ☐ ​ Item 1.01 Entry into a Material Definitive Agreement. ​ In March 2021, the Compensation Committee (the “Compensation Committee”) of the Board of Directors of G-III Apparel Group, Ltd. (the “Company”) awarded time-based restricted stock units with three-year cliff-vesting (“Cliff-Vesting RSUs”), pursuant to the Company’s 2015 Long-Term Incentive Plan, as amended (the “2015 Plan”), to the named executive officers of the Company (the “Named Executive Officers”) in the amounts shown under the heading “Cliff-Vesting RSUs Awarded in March 2021” in the table below. The Compensation Committee awarded Cliff-Vesting RSUs because setting meaningful long-term performance conditions was, at the time of the awards, impracticable due to the severe disruptions to the Company’s business caused by the COVID-19 pandemic and the resulting
```

### R0021 · information_rights · 0000950123-20-004953_filename4
**Question.** Classify whether a document grants investors a live financial-reporting/information right (5.3).
**Field.** `information_rights` -- yes if a live obligation to deliver financials to investors exists, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
ares held by it in compliance with SEC Rule 144(b)(1)(i) or (ii) holds one percent (1%) or less of the Company’s outstanding Common Shares and all Registrable Securities held by such Holder (together with any Affiliate of the Holder with whom such Holder must aggregate its sales under SEC Rule 144) can be sold in any three (3) month period without registration in compliance with SEC Rule 144. 3. Information Rights . 3.1 Delivery of Financial Statements . (a) The Company shall deliver to each Major Investor, as soon as practicable, but in any event within 90 days after the end of each fiscal year of the Company, audited financial statements of the Company for and as at the end of such fiscal year (including a consolidated balance sheet of the Company as at the end of such financial year, and consolidated statements of income, retained earnings and changes in cash flow of the Company for such year, setting forth in each case in comparative form the corresponding figures for the previous financial year), prepared in accordance with GAAP, consistently applied, and accompanied by an audit report by regionally recognized independent auditing firm selected by the Board. (b) The Company shall deliver to each Major Investor, as soon as practicable, but in any event within 30 days after the end of each fiscal quarter of the Company, unaudited f
```

### R0022 · convert_vs_preference_decision · example5_take_preference
**Question.** Decide convert-vs-take-preference in a real acquisition scenario (4.4).
**Field.** `convert_vs_preference_decision` -- whether the investor should convert to common or take their preference
**Answer.** one of: convert, take-preference, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1680084/000121390017000472/fc2016a1ex99i_snapwire.htm

**Text shown to the model:**

```
Investor has purchased an Agreement for Future Equity for $100,000. The Valuation Cap is $6,000,000. &#9679; Another entity proposes to acquire the company for cash consideration of $200,000. The company&rsquo;s fully-diluted outstanding capital stock immediately prior to the acquisition, including 795,000 outstanding options but excluding any unallocated shares in the option pool, is 10,795,000 shares. The investor can choose to have the Agreement for Future Equity purchase amount returned, or convert the Agreement for Future Equity into shares of common stock and participate pro rata in the cash consideration with the other common stockholders. The Agreement for Future Equity would convert into 179,920 shares of common stock, based on the &ldquo;Liquidity Price&rdquo; of $0.5558 per share (the Liquidity Price is calculated by dividing 6,000,000 by 10,795,000). When the $200,000 deal consideration is allocated pro rata among all of the common stockholders, including the investor (and assuming: (1) the outstanding options are all exercised; (2) there is no outstanding debt; and (3) for purposes of this example, there is only the one outstanding Agreement for Future Equity), the investor would receive approximately $3,274. This dollar amount is calculated by dividing the $200,000 deal consideration among 10,974,920 shares of outstanding common stock, resulting in $0.0182 per share (179,920 shares multiplied by $0.0182 = $3,274.54). Since this amount is considerably less than the $100,000 purchase amount,
```

### R0023 · flag_internal_inconsistency · hyrecar_inconsistent
**Question.** Flag whether two real share-count citations in the same filing are numerically consistent (8.6).
**Field.** `flag_internal_inconsistency` -- true if the two cited share counts differ, false if they match
**Answer.** bool value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1713832/000121390019013300/f424b4071819_hyrecarinc.htm

**Text shown to the model:**

```
Citation A (Capitalization table (actual column, as of March 31, 2019)): "12,191,508 shares issued and outstanding, actual"

Citation B (Prospectus summary basis statement): "be outstanding immediately after this offering is based on 12,331,348 shares of our common stock outstanding as of July 18, 2019"
```

### R0024 · liquidation_preference_multiple · 1274991_000119312510075918
**Question.** Classify liquidation preference multiple (1x, 2x, 3x, other, non-participating) (leaf 1.3.1).
**Field.** `liquidation_preference_multiple` -- How many times the OIP the preferred holder receives upon liquidation.
**Answer.** one of: non-participating, 1x, 2x, 3x, other, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
ries A-2 Preferred after the filing date hereof) (the “Series A-2 Liquidation Amount”), plus an amount equal to all declared and unpaid dividends on such share of Series A-2 Preferred; (iii) with respect to the Series A Preferred, each holder of Series A Preferred shall not receive pursuant to Section 3(c) above and this Section 3(d) an aggregate amount per share of Series A Preferred that is greater than the sum of three (3) times the Original Issue Price of the Series A Preferred plus an amount equal to all declared and unpaid dividends on such share of Series A Preferred; (iv) with respect to the Series B Preferred, each holder of Series B Preferred shall not receive pursuant to Section 3(c) above and this Section 3(d) an aggregate amount per share of Series B Preferred that is greater than the sum of three (3) times the Original Issue Price of the Series B Preferred plus an amount equal to all declared and unpaid dividends on such share of Series B Preferred; (v) with respect to the Series C Preferred, each holder of Series C Preferred shall not receive pursuant to Section 3(c) above and this Section 3(d) an aggregate amount per share of Series C Preferred that is greater than the sum of three (3) times the Original Issue Price of the Series C Preferred plus an amount equal to all declared and unpaid div
```

### R0025 · form_d_fields · 1456554_000145655410000002
**Question.** Extract the Total Amount Sold field value from a real Form D filing (7.2).
**Field.** `form_d_field_value` -- The extracted Total Amount Sold dollar value from the Form D.
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1456554/000145655410000002/primary_doc.xml

**Text shown to the model:**

```
onse>Series B-1 Preferred Stock Total Offering of $2,380,000,Total Amount Sold $2,366,532 and Total Remaining to be Sold is $13,468. Series C Preferred Stock Total Offering of $8,120,000,Total Amount Sold $7,031,999 and Total Remaining to
```

### R0026 · fully_diluted_basis · actelis_ex
**Question.** Classify capitalization definition as fully-diluted or issued-outstanding basis (3.4).
**Field.** `fully_diluted_basis` -- Whether cap is computed on fully-diluted or issued-outstanding basis.
**Answer.** one of: fully-diluted, issued-outstanding, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1141284/000121390022020064/fs12022ex10-7_actelisnet.htm

**Text shown to the model:**

```
forth in Exhibit A (the &ldquo; Purchased Shares &rdquo;), at an aggregate purchase price for the Preferred A Shares not to exceed US$ 3,000,000 (the &ldquo; Purchase Price &rdquo;) at a price per share equal to US$0.01308 (the &ldquo; PPS &rdquo;) reflecting a pre-money valuation of the Company (on a fully-diluted basis) of US$1,687,500 and constituting immediately after the Closing (assuming the maximum Purchase Price was paid) 64.29% of the Company&rsquo;s capital Stock, on an as converted and fully diluted basis (after reserving the New Pool (as defined below)).
```

### R0027 · cliff_present · 0001144204-15-053727_v419640_ex10-1
**Question.** Classify whether a vesting schedule includes a cliff blockage period (6.2).
**Field.** `cliff_present` -- yes if the schedule has a cliff blockage period, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
to inform you that you will be promoted from Sr. Vice President, Operations to Chief Operating Officer, effective September 1, 2015. This is a Section 16 Officer position and the annual rate of pay will be $287,040. In addition, you will be granted an option to purchase 50,000 shares of Atossa Genetics common stock at the closing price on the date approved by the board, which vests over four years of employment with no cliff.   In your time with Atossa, you have quickly demonstrated your work ethic, dedication, and your superb qualifications. We have faith that you will continue to excel in your new position and hope that you continue to develop your potential here at Atossa Genetics.   Congratulations on this promotion, and we look forward to your contributions in your new position.   Thank you for being such a valuable asset to Atossa Genetics and for your loyal service.   Sincerely, /s/ Steven C. Quay, MD, PHD, FCAP Steven C. Quay, MD, PHD, FCAP CEO and President   /s/ Scott Youmans   09/01/2015 Acknowledgement of receipt – Scott Youmans   Date
```

### R0028 · investor_ownership_pct · uber_pif_investor
**Question.** Compute a named institutional investor's ownership percentage from raw S-1 share counts (3.2.2).
**Field.** `investor_ownership_pct` -- the computed investor ownership percentage as a bare decimal (e.g., 16.3)
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1543151/000119312519103850/d647752ds1.htm

**Text shown to the model:**

```
From Uber Technologies, Inc.'s S-1 registration statement, "Security Ownership of Certain Beneficial Owners and Management" table, "5% Stockholders and Selling Stockholders" section (Shares Beneficially Owned Before the Offering):

Applicable percentage ownership before the offering is based on 1,362,500 thousand shares of common stock outstanding as of March 31, 2019.

Name of Beneficial Owner: The Public Investment Fund
Shares (in thousands): 72,841
```

### R0029 · safe_cap_vs_discount_applies · rentberry_both_mfn
**Question.** Classify whether a SAFE uses cap, discount, or both-MFN for conversion pricing (2.1.3).
**Field.** `safe_cap_vs_discount_applies` -- Whether the SAFE's conversion price uses cap-only, discount-only, or both with MFN.
**Answer.** one of: cap, discount, both-mfn, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
the Next Equity Financing and (without double-counting):   ● Includes all shares of Capital Stock issued and outstanding;   ● Includes all Converting Securities;   ● Includes all (i) issued and outstanding Options and (ii) Promised Options;   ● Includes the Unissued Option Pool; and   ● Excludes, notwithstanding the foregoing, any increases to the Unissued Option Pool (except to the extent necessary to cover Promised Options that exceed the Unissued Option Pool) in connection with the Next Equity Financing.   “ Conversion Price ” means the either: (1) the Safe Price or (2) the Discount Price, whichever calculation results in a greater number of shares of Safe Preferred Stock.   “ Converting Securities ” includes this Safe and other convertible securities issued by the Company, including but not limited to: (i) other Safes; (ii) convertible promissory notes and other convertible debt instruments; and (iii) convertible securities that have the right to convert into shares of Capital Stock.   “ Discount Price ” means the price per share of the Standard Preferred Stock sold in the Next Equity Financing multiplied by the difference between one and the decimal version of the Discount Rate.   “ Dissolution Event ” means (i) a voluntary termination of operations, (ii) a general assignment for the benefit of the Company’s creditors or (iii) any other liquidation, dissolution or winding up of the Company (excluding a Liquidity Event), whether voluntary or involuntary.   “ Initial Public Offering ” means the closing of the Company’s first firm commitment underwritten initial public offering of Common Stock pursuant to a registration statement filed under the Securities Act.   “ Liquidity Capitalization ” is calculated as of immediately prior to the Liquidity Event (or, solely for purposes of determining the Liquidity Price in connection with a Safe Expiration Conversion, as of immediately prior to such Safe Expiration Conversion), and (without double- counting):   ● Includes all shares of Capital Stock issued and outstanding;   ● Incl
```

### R0030 · option_strike_409a · 0001125282-06-006236_11p0
**Question.** Extract the stock option exercise price per share from a grant agreement (6.4).
**Field.** `option_strike_409a` -- the exercise price (strike price) per share of the granted option
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
TARGET GRANT: the option grant stated to have an exercise price of $11.00 per share (see below).

0.25 per share. II-3 Back to Contents   • On April 10, 2006, we issued 2,000 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $1.00 per share.         • On April 26, 2006, we granted options to 38 of our employees to purchase an aggregate of 706,750 shares of our common stock under our Amended and Restated Stock Option Plan at an exercise price of $11.00 per share.         • On May 24, 2006, we issued 1,250 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $0.25 per share.         • On June 9, 2006, we issued 1,000 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $0.25 per share.         • On July 13, 2006, we issued 3,000 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $1.00 per share.         • On July 18, 2006, we granted options to two of our employees to purchase an aggregate of 252,000 shares of our common stock under our Amended and Restated Stock Option Plan at an exercise price of $11.00 per share.         • On August 11, 2006, we issued 2,480,894 shares of our common stock upon
```

### R0031 · safe_cap_vs_discount_applies · complete_both_mfn
**Question.** Classify whether a SAFE uses cap, discount, or both-MFN for conversion pricing (2.1.3).
**Field.** `safe_cap_vs_discount_applies` -- Whether the SAFE's conversion price uses cap-only, discount-only, or both with MFN.
**Answer.** one of: cap, discount, both-mfn, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
ach case calculated on an as-converted to Common Stock basis):   ● Includes all shares of Capital Stock issued and outstanding;   ● Includes all Converting Securities;   ● Includes all (i) issued and outstanding Options and (ii) Promised Options; and   ● Includes the Unissued Option Pool, except that any increase to the Unissued Option Pool in connection with the Equity Financing shall only be included to the extent that the number of Promised Options exceeds the Unissued Option Pool prior to such increase.   “ Conversion Price ” means the either: (1) the Safe Price or (2) the Discount Price, whichever calculation results in a greater number of shares of Common Stock.   2     “ Converting Securities ” includes this Safe and other convertible securities issued by the Company, including but not limited to: (i) other Safes; (ii) convertible promissory notes and other convertible debt instruments; and (iii) convertible securities that have the right to convert into shares of Capital Stock.   “ Direct Listing ” means the Company’s initial listing of its Common Stock (other than shares of Common Stock not eligible for resale under Rule 144 under the Securities Act) on a national securities exchange by means of an effective registration statement on Form S-1 filed by the Company with the SEC that registers shares of existing capital stock of the Company for resale, as approved by the Company’s board of directors. For the avoidance of doubt, a Direct Listing shall not be deemed to be an underwritten offering and shall not involve any underwriting services. “ Discount Price ” means the price per share of the Common Stock sold in the Equity Financing multiplied by the Discount Rate.   “ Dissolution Event ” means (i) a voluntary termination of operations, (ii) a general assignment for the benefit of the Company’s creditors or (iii) any other liquidation, dissolution or winding up of the Company ( excluding a Liquidity Event), whether voluntary or involuntary.   “ Dividend Amount ” means, with respect to any date on which the Company p
```

### R0032 · investor_ownership_pct · uber_benchmark_investor
**Question.** Compute a named institutional investor's ownership percentage from raw S-1 share counts (3.2.2).
**Field.** `investor_ownership_pct` -- the computed investor ownership percentage as a bare decimal (e.g., 16.3)
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1543151/000119312519103850/d647752ds1.htm

**Text shown to the model:**

```
From Uber Technologies, Inc.'s S-1 registration statement, "Security Ownership of Certain Beneficial Owners and Management" table, "5% Stockholders and Selling Stockholders" section (Shares Beneficially Owned Before the Offering):

Applicable percentage ownership before the offering is based on 1,362,500 thousand shares of common stock outstanding as of March 31, 2019.

Name of Beneficial Owner: Entities affiliated with Benchmark Capital Partners
Shares (in thousands): 150,079
```

### R0033 · vesting_schedule · 0000020740-17-000006_a201610kex1012
**Question.** Extract and normalize vesting schedule to canonical string format (6.1).
**Field.** `vesting_schedule` -- Normalized vesting schedule: e.g. '4yr/1yr-cliff', '3yr/no-cliff', '4yr/cliff'.
**Answer.** string value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
s pursuant to the Company’s 2014 Incentive Plan (the “Plan”). Applicable provisions of the Plan are incorporated herein as though set forth herein in full. Capitalized terms used herein and not otherwise defined herein shall have the respective meanings specified in the Plan. Section 1 Restricted Stock Unit Award . The Company hereby awards to the Participant as of the Award Date,      Restricted Stock Units (the “ Units ”). Subject to Section 3 of this Agreement, twenty-five percent (25%) of such Units shall vest on each anniversary of the Award Date until all of such Units have vested; provided that, except as expressly provided in Section 3 of this Agreement, in the event that the Participant ceases to be an employee of the Company and all of its subsidiaries, he or she shall forfeit any Units which have not previously vested. Subject to Section 3 of this Agreement, promptly after such vesting the Company shall issue to the Participant one (1) share of Common Stock for each vested Unit, which payment shall in all events occur not later than the fifteenth day of the third calendar
```

### R0034 · securities_exemption · 1102449
**Question.** Classify which Securities Act exemption a Form D filing claimed (7.1).
**Field.** `securities_exemption` -- The federal exemption claimed in the Form D filing.
**Answer.** one of: 506b, 506c, 504, reg-a, other, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1102449/000110244915000001/primary_doc.xml

**Text shown to the model:**

```
<entityName>ACCELERATED I/O INC</entityName>
        <issuerAddress>
            <street1>7633 E 63RD PLACE</street1>
            <street2>SUITE 300</street2>
            <city>TULSA</city>
            <stateOrCountry>OK</stateOrCountry>
            <stateOrCountryDescription>OKLAHOMA</stateOrCountryDescription>
            <zipCode>74133</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>800-691-8580</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <edgarPreviousNameList>
            <previousName>ACCELERATED I O INC</previousName>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <overFiveYears>true</overFiveYears>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Joseph</firstName>
                <middleName>D</middleName>
                <lastName>Doll</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>4221 W 136th Ave</street1>
                <city>Broomfield</city>
                <stateOrCountry>CO</stateOrCountry>
                <stateOrCountryDescription>COLORADO</stateOrCountryDescription>
                <zipCode>80023</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Gerald</firstName>
                <middleName>R</middleName>
                <lastName>Ferguson</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>7633 E 63rd Place</street1>
                <street2>Suite 300</street2>
                <city>Tulsa</city>
                <stateOrCountry>OK</stateOrCountry>
                <stateOrCountryDescription>OKLAHOMA</stateOrCountryDescription>
                <zipCode>74133</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Francisco</firstName>
                <lastName>Schipperheijn</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>613 Cricket Court</street1>
                <city>Edmondton</city>
                <stateOrCountry>A0</stateOrCountry>
                <stateOrCountryDescription>ALBERTA, CANADA</stateOrCountryDescription>
                <zipCode>T5T 2B2</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Other Technology</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>$1 - $1,000,000</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06b</item>
        </federalExemptionsExclusions>
```

### R0035 · board_seats_investor · 0001104659-17-048201_a17-18633_1ex10d6_pjc
**Question.** Extract the number of board seats an investor has the right to designate (5.1).
**Field.** `board_seats_investor` -- the number of board seats the investor/investor class may designate
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
ent, then Opal Sheppard shall be entitled to nominate a new individual to serve as a member of the Board and the Board shall fill the vacancy created by such departed Designated Director with such nominated individual, provided that such nominated individual satisfies the requirements set forth in Section 2.4.  Any such nominated individual shall be deemed to be the Designated Director hereunder.  For so long as (x) PJC has the right to designate three (3) directors pursuant to the Board Rights Agreement among Emergent, PJC and the Investors party thereto, dated as of the date hereof (the “ PJC Board Rights Agreement ”) and (y) Opal Sheppard and/or any Affiliates or Related Funds thereof, in the aggregate, beneficially own (without duplication) at least 15.00% (the “ Specified Percentage ”) of the original principal amount of the New Senior Notes issued by Emergent to Opal Sheppard on the Closing Date (the “ Opal Sheppard New Senior Notes ”), Opal Sheppard shall have the right to designate a Designated Director as provided in the first sentence of this Section 2.2, and the Board shall, subject to Section 2.4 below, recommend at each meeting of stockholders at which a Designated Director is to be elected to include a Designated Director as one of the Board’s nominees for election to the Board or to fill a vacancy left by a departed Des
```

### R0036 · vesting_schedule · 1452751_000119312513403444
**Question.** Extract and normalize vesting schedule to canonical string format (6.1).
**Field.** `vesting_schedule` -- Normalized vesting schedule: e.g. '4yr/1yr-cliff', '3yr/no-cliff', '4yr/cliff'.
**Answer.** string value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
urer. The Company may modify its employee benefits from time to time in its discretion.   4. Equity Awards. Subject to approval by the Board, the Company shall grant you an option under the 2008 Equity Incentive Plan (the “ Equity Plan ”) to purchase 1,884,850 shares of the Company’s Common Stock (the “ Option ”) at fair market value as determined by the Board as of the date of grant. The Option will be governed in full by the Equity Plan and your grant agreement. Your grant agreement for the Option will include a four-year vesting schedule subject to your Continuous Service (as defined in the Equity Plan), under which (i) twenty-five percent (25%) of the shares subject to the Option will vest on the one year anniversary of your vesting commencement date, and (ii) the remaining unvested shares shall vest in monthly installments equal to 1/48 th of all shares beginning with the first monthly anniversary of the initial vesting tranche and continuing on a monthly basis thereafter. Suresh Vasudevan December 28, 2010 Page 3   In addition, if the Company is subject to a Change in Control (as defined in Section 9(b)) and you remai
```

### R0037 · board_seats_investor · 0001047469-03-010357_a2106288zex-4_8
**Question.** Extract the number of board seats an investor has the right to designate (5.1).
**Field.** `board_seats_investor` -- the number of board seats the investor/investor class may designate
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
dment but not defined herein shall have the meanings ascribed to them in the Agreement.         2.     Amendment of Section 4.1(c).     Section 4.1(c) of the Agreement is hereby amended by deleting such section in its entirety substituting in lieu thereof the following:         "(c) At all times during the term of this Agreement that Rakepoll's Interest is:           (i)  50% or above of Rakepoll's Initial Interest, Rakepoll shall have the right to designate for nomination and approval three Investor Directors, provided, that one of such nominees shall be an independent director; the Management Directors shall have the right to designate for nomination and approval two Management Directors; and the five Independent Directors shall be designated for nomination and approval jointly by the Management Directors and the Investor Directors;         (ii)  25% or above but less than 50% of Rakepoll's Initial Interest, Rakepoll shall have the right to designate for nomination and approval two Investor Directors; and there shall be six Independent Directors who shall be designated for nomination and approval jointly by the Management Directors and the Investor Directors;         (iii)  10% or above but less than 25% of Rakepoll's Initial Interest, Rakepoll shall have the right to designate for nomination and approval one Investor Director; the Management Directors shall have the right to designate for
```

### R0038 · safe_pre_post · 1851491_000157587226000456
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1851491/000157587226000456/amass029_ex10-1.htm

**Text shown to the model:**

```
EX-10.1 2 amass029_ex10-1.htm EXHIBIT 10.1 Exhibit 10.1     POST-MONEY VALUATION CAP   THIS INSTRUMENT AND ANY SECURITIES ISSUABLE PURSUANT HERETO HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE “ SECURITIES ACT ”), OR UNDER THE SECURITIES LAWS OF CERTAIN STATES. THESE SECURITIES MAY NOT BE OFFERED, SOLD OR OTHERWISE TRANSFERRED, PLEDGED OR HYPOTHECATED EXCEPT AS PERMITTED IN THIS SAFE AND UNDER THE ACT AND APPLICABLE STATE SECURITIES LAWS PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT OR AN EXEMPTION THEREFROM.     AFTERDREAM, Inc   SAFE Amendment 2 (Simple Agreement for Future Equity)   THIS FURTHER AMENDS the SAFE AGREEMENT THAT in exchange for the payment by Amass Brands, Inc. (the “ Investor ”) of $1,735,000 (the “ Purchase Amount ”) on or after June 25 th , AFTERDREAM, Inc a Delaware corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   This Safe is one of the forms available at http://ycombinator.com/documents and the Company and the Investor agree that neither one has modified the form, except to fill in blanks and bracketed terms.   The “ Post-Money Valuation Cap ” is $7,500,000. See Section 2 for certain additional defined terms.   1. Events   (a) Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the greater of: (1) the number of shares of Standard Preferred Stock equal to the Purchase Amount divided by the lowest price per share of the Standard Preferred Stock; or (2) t
```

### R0039 · safe_cap_vs_discount_applies · flowhub_cap_only
**Question.** Classify whether a SAFE uses cap, discount, or both-MFN for conversion pricing (2.1.3).
**Field.** `safe_cap_vs_discount_applies` -- Whether the SAFE's conversion price uses cap-only, discount-only, or both with MFN.
**Answer.** one of: cap, discount, both-mfn, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
b Holdings, LLC a Colorado limited liability company (the “ Company ”), hereby issues to the Investor the right to certain of the Company’s Units, subject to the terms set forth below.

The “ Valuation Cap ” is $35,000,000. See Section 2 for certain additional defined terms.

1.
Events

(a)      Equity Financing . If there is an Equity Financing before the expiration or termination of this instrument, the Company will automatically issue to the Investor either: (1) a number of Standard Preferred Units equal to the Purchase Amount divided by the price per share of the Standard Preferred Units, if the pre-money valuation is less than or equal to the Valuation Cap; or (2) a number of Safe Preferred Units equal to the Purchase Amount divided by the Safe Price, if the pre-money valuation is greater than the Valuation Cap.

In connection with the issuance of Standard Preferred Units or Safe Preferred Units, as applicable, by the Company to the Investor pursuant to this Section 1(a), the Investor will execute and deliver to the Company all transaction documents related to the Equity Financing; provided, that such documents are the same documents to be entered into with the purchasers of Standard Preferred Units, with appropriate variations for the Safe Preferred Units if applicable, and provided further, that such documents have customary exceptions to any drag-along applicable to the Investor.

(b)      Liquidity Event . If there is a Liquidity Event before the expiration or termination of this instrument, the Investor will, at its option, either (i) receive a cash payment equal to the Purchase Amount (subject to the following paragraph) or (ii) automatically receive from the Company a number of Common Units equal to the Purchase Amount divided by the Liquidity Price, if the Investor fails to select the cash option.

In connection with Section (b)(i), the Purchase Amount will be due and payable by the Company to the Investor immediately prior to, or concurrent with, the consummation of the Liquidity Event. If there are not enough funds to
```

### R0040 · securities_exemption · 1902507
**Question.** Classify which Securities Act exemption a Form D filing claimed (7.1).
**Field.** `securities_exemption` -- The federal exemption claimed in the Form D filing.
**Answer.** one of: 506b, 506c, 504, reg-a, other, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1902507/000190250722000003/primary_doc.xml

**Text shown to the model:**

```
<entityName>NextView Ventures V, L.P.</entityName>
        <issuerAddress>
            <street1>C/O NEXTVIEW MANAGEMENT COMPANY, LLC</street1>
            <street2>179 LINCOLN STREET, SUITE 404</street2>
            <city>BOSTON</city>
            <stateOrCountry>MA</stateOrCountry>
            <stateOrCountryDescription>MASSACHUSETTS</stateOrCountryDescription>
            <zipCode>02111</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>6173147202</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Limited Partnership</entityType>
        <yearOfInc>
            <withinFiveYears>true</withinFiveYears>
            <value>2021</value>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>N/A</firstName>
                <lastName>NextView Capital Partners V, LLC</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o NextView Management Company, LLC</street1>
                <street2>179 Lincoln Street, Suite 404</street2>
                <city>Boston</city>
                <stateOrCountry>MA</stateOrCountry>
                <stateOrCountryDescription>MASSACHUSETTS</stateOrCountryDescription>
                <zipCode>02111</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification>General Partner of the Issuer (the &quot;General Partner&quot;)</relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>David</firstName>
                <lastName>Beisel</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o NextView Management Company, LLC</street1>
                <street2>179 Lincoln Street, Suite 404</street2>
                <city>Boston</city>
                <stateOrCountry>MA</stateOrCountry>
                <stateOrCountryDescription>MASSACHUSETTS</stateOrCountryDescription>
                <zipCode>02111</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification>Managing Member of the General Partner</relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Robert</firstName>
                <lastName>Go</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o NextView Management Company, LLC</street1>
                <street2>179 Lincoln Street, Suite 404</street2>
                <city>Boston</city>
                <stateOrCountry>MA</stateOrCountry>
                <stateOrCountryDescription>MASSACHUSETTS</stateOrCountryDescription>
                <zipCode>02111</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification>Managing Member of the General Partner</relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Lee</firstName>
                <lastName>Hower</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o NextView Managment Company, LLC</street1>
                <street2>179 Lincoln Street, Suite 404</street2>
                <city>Boston</city>
                <stateOrCountry>MA</stateOrCountry>
                <stateOrCountryDescription>MASSACHUSETTS</stateOrCountryDescription>
                <zipCode>02111</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification>Managing Member of the General Partner</relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Melody</firstName>
                <lastName>Koh</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o NextView Management Company, LLC</street1>
                <street2>179 Lincoln Street, Suite 404</street2>
                <city>Boston</city>
                <stateOrCountry>MA</stateOrCountry>
                <stateOrCountryDescription>MASSACHUSETTS</stateOrCountryDescription>
                <zipCode>02111</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification>Managing Member of the General Partner</relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Stephanie</firstName>
                <lastName>Palmeri</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o NextView Management Company, LLC</street1>
                <street2>179 Lincoln Street, Suite 404</street2>
                <city>Boston</city>
                <stateOrCountry>MA</stateOrCountry>
                <stateOrCountryDescription>MASSACHUSETTS</stateOrCountryDescription>
                <zipCode>02111</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification>Managing Member of the General Partner</relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Pooled Investment Fund</industryGroupType>
            <investmentFundInfo>
                <investmentFundType>Venture Capital Fund</investmentFundType>
                <is40Act>false</is40Act>
            </investmentFundInfo>
        </industryGroup>
        <issuerSize>
            <revenueRange>Not Applicable</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06c</item>
            <item>3C</item>
            <item>3C.7</item>
        </federalExemptionsExclusions>
```

### R0041 · preference_seniority · 1341470_000119312509004895
**Question.** Classify multi-series preferred liquidation seniority as pari-passu or stacked (1.3.4).
**Field.** `preference_seniority` -- Whether preferred series rank equally (pari-passu) or in a seniority order (stacked).
**Answer.** one of: pari-passu, stacked, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1341470/000119312509004895/dex31.htm

**Text shown to the model:**

```
der this subsection 3(a) is hereinafter referred to as the “ Series C Liquidation Amount .” Notwithstanding anything herein to the contrary, while any shares of Series C Preferred Stock are outstanding, the Corporation shall not establish any Senior Preferred Stock without the prior affirmative vote of holders of a majority of the shares of Series C Preferred Stock. “ Junior Preferred Stock ” shall mean any class or series of preferred stock of the Corporation, including, but not limited to, the Series A Preferred Stock and the Series B Preferred Stock, ranking junior to the Series C Preferred Stock in respect of the right to receive assets upon the liquidation, dissolution or winding up of the affairs of the Corporation. “ Senior Preferred Stock ” shall mean any class or series of preferred stock of the Corporation ranking senior to the Series C Preferred Stock in respect of the right to receive assets upon the liquidation, dissolution or winding up of the affairs of the Corporation. (b) (i) For purposes of this Section 3, a “ Liquidation Event ” shall include (A) a sale of assets of the Corporation that are material to the ongoing operations of the Corporation, (B) the closing of the sale
```

### R0042 · liquidation_preference_multiple · 1062195_000110465903012203
**Question.** Classify liquidation preference multiple (1x, 2x, 3x, other, non-participating) (leaf 1.3.1).
**Field.** `liquidation_preference_multiple` -- How many times the OIP the preferred holder receives upon liquidation.
**Answer.** one of: non-participating, 1x, 2x, 3x, other, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
s of the record date fixed for the determination of holders of Common Stock entitled to receive such distribution; UNTIL SUCH TIME AS: (x) in the case of the Series A Preferred Stock, each holder of then outstanding Series A Preferred Stock shall have received, in distributions made in connection with such liquidation, dissolution or winding up, an aggregate amount per share of Series A Preferred Stock held equal to three (3) times the Original Issue Price for the Series A Preferred Stock (such aggregate dollar amount to include all amounts previously paid to such holder pursuant to the liquidation preference of the Series A Preferred Stock including without limitation any dividends paid thereon), (y) in the case of the Series B Preferred Stock, each holder of then outstanding Series B Preferred Stock shall have received, in distributions made in connection with such liquidation, dissolution or winding up, an aggregate amount per share of Series B Preferred Stock held equal to three (3) times the Original Issue Price for the Series B Preferred Stock (such aggregate dollar amount to include all amounts previously paid to such holder pursuant to the liquidation preference of the Series B Preferred Stock including without limitation any dividends paid thereon), and (z) in the case of the Series C Preferred Stoc
```

### R0043 · safe_cap_vs_discount_applies · taoweave_both_mfn
**Question.** Classify whether a SAFE uses cap, discount, or both-MFN for conversion pricing (2.1.3).
**Field.** `safe_cap_vs_discount_applies` -- Whether the SAFE's conversion price uses cap-only, discount-only, or both with MFN.
**Answer.** one of: cap, discount, both-mfn, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
o the extent that the number of Promised Options exceeds the Unissued Option Pool prior to such increase.   “Control ” has the meaning given in section 1124 of the UK Corporation Tax Act 2010, and “ Change of Control ” shall be construed accordingly in relation to the Company except where following completion of the Change of Control the shareholders and the proportion of Shares held by each of them are the same as the shareholders and their shareholdings in the Company immediately prior to the Change of Control.   “Conversion Price ” means either (1) the Safe Price or (2) the Discount Price, whichever calculation results in the greater number of Safe Shares.   “Converting Securities ” includes this Safe and other convertible securities issued by the Company, including but not limited to: (i) other Safes; (ii) convertible promissory notes and other convertible debt instruments; and (iii) convertible securities that have the right to convert into Shares.   “Deferred Shares ” means deferred shares in the capital of the Company carrying no voting rights and the right to participate in dividends and returns of capital only up to a nominal amount.   “Direct Listing ” means the Company’s initial listing of its Shares or securities representing those Shares (including without limitation depositary interests, American depositary receipts, American depositary shares and/or other instruments) on the NASDAQ Stock Market of the NASDAQ OMX Group Inc. or the New York Stock Exchange or the Official List of the United Kingdom Financial Conduct Authority or the AIM Market operated by the London Stock Exchange Plc or any other recognized investment exchange (as defined in section 285 of the Financial Services and Markets Act 2000). For the avoidance of doubt, a Direct Listing will not be deemed to be an underwritten offering and will not involve any underwriting services.   “Discount Price ” means the lowest price per share of the Senior Shares issued in the Equity Financing multiplied by the Discount Rate.   “Dissolution Event ” means (i) a volunt
```

### R0044 · liquidation_preference_multiple · 1447362_000114036119009024
**Question.** Classify liquidation preference multiple (1x, 2x, 3x, other, non-participating) (leaf 1.3.1).
**Field.** `liquidation_preference_multiple` -- How many times the OIP the preferred holder receives upon liquidation.
**Answer.** one of: non-participating, 1x, 2x, 3x, other, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
ificant Holders ” shall have the meaning set forth in Section 4.1.   (mm)            “ Threshold Event ” shall mean a Liquidation Event or Deemed Liquidation Event (each as defined in the Certificate of Incorporation) pursuant to which (i) the holders of Series E-1 Preferred Stock would receive at the initial closing of such Liquidation Event or Deemed Liquidation Event consideration having a value equal to at least three (3) times the Original Issue Price (as defined in the Certificate of Incorporation) of the Series E-1 Preferred Stock, (ii) the holders of Series E-2 Preferred Stock would receive at the initial closing of such Liquidation Event or Deemed Liquidation Event consideration having a value equal to at least three (3) times the Original Issue Price of the Series E-2 Preferred Stock, (iii) the holders of Series E-3 Preferred Stock would receive at the initial closing of such Liquidation Event or Deemed Liquidation Event consideration having a value equal to at least three (3) times the Original Issue Price of the Series E-3 Preferred Stock, (iv) the holders of Series E-2A Preferred Stock would receive at the initial closing of the Liquidation Event or Deemed Liquidation Event consideration having a value equal to at least three (3) times the Original Issue Price of the Series E-2A Preferred Stock,
```

### R0045 · investor_ownership_pct · uber_sb_cayman_investor
**Question.** Compute a named institutional investor's ownership percentage from raw S-1 share counts (3.2.2).
**Field.** `investor_ownership_pct` -- the computed investor ownership percentage as a bare decimal (e.g., 16.3)
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1543151/000119312519103850/d647752ds1.htm

**Text shown to the model:**

```
From Uber Technologies, Inc.'s S-1 registration statement, "Security Ownership of Certain Beneficial Owners and Management" table, "5% Stockholders and Selling Stockholders" section (Shares Beneficially Owned Before the Offering):

Applicable percentage ownership before the offering is based on 1,362,500 thousand shares of common stock outstanding as of March 31, 2019.

Name of Beneficial Owner: SB Cayman 2 Ltd. (SoftBank-affiliated investment vehicle)
Shares (in thousands): 222,228
```

### R0046 · securities_exemption · 1444307
**Question.** Classify which Securities Act exemption a Form D filing claimed (7.1).
**Field.** `securities_exemption` -- The federal exemption claimed in the Form D filing.
**Answer.** one of: 506b, 506c, 504, reg-a, other, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1444307/000149315223019301/primary_doc.xml

**Text shown to the model:**

```
<entityName>ONCOSEC MEDICAL Inc</entityName>
        <issuerAddress>
            <street1>820 BEAR TAVERN ROAD</street1>
            <city>EWING</city>
            <stateOrCountry>NJ</stateOrCountry>
            <stateOrCountryDescription>NEW JERSEY</stateOrCountryDescription>
            <zipCode>08628</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>855-662-6732</issuerPhoneNumber>
        <jurisdictionOfInc>NEVADA</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <previousName>NetVentory Solutions, Inc.</previousName>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <overFiveYears>true</overFiveYears>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Robert</firstName>
                <middleName>H.</middleName>
                <lastName>Arch</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>820 Bear Tavern Road</street1>
                <city>Ewing</city>
                <stateOrCountry>NJ</stateOrCountry>
                <stateOrCountryDescription>NEW JERSEY</stateOrCountryDescription>
                <zipCode>08628</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>George</firstName>
                <lastName>Chi</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>820 Bear Tavern Road</street1>
                <city>Ewing</city>
                <stateOrCountry>NJ</stateOrCountry>
                <stateOrCountryDescription>NEW JERSEY</stateOrCountryDescription>
                <zipCode>08628</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Linda</firstName>
                <lastName>Shi</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>820 Bear Tavern Road</street1>
                <city>Ewing</city>
                <stateOrCountry>NJ</stateOrCountry>
                <stateOrCountryDescription>NEW JERSEY</stateOrCountryDescription>
                <zipCode>08628</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Chao</firstName>
                <lastName>Zhou</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>820 Bear Tavern Road</street1>
                <city>Ewing</city>
                <stateOrCountry>NJ</stateOrCountry>
                <stateOrCountryDescription>NEW JERSEY</stateOrCountryDescription>
                <zipCode>08628</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Herbert</firstName>
                <middleName>Kim</middleName>
                <lastName>Lyerly</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>820 Bear Tavern Road</street1>
                <city>Ewing</city>
                <stateOrCountry>NJ</stateOrCountry>
                <stateOrCountryDescription>NEW JERSEY</stateOrCountryDescription>
                <zipCode>08628</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Kevin</firstName>
                <middleName>R</middleName>
                <lastName>Smith</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>820 Bear Tavern Road</street1>
                <city>Ewing</city>
                <stateOrCountry>NJ</stateOrCountry>
                <stateOrCountryDescription>NEW JERSEY</stateOrCountryDescription>
                <zipCode>08628</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Joon</firstName>
                <lastName>Kim</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>820 Bear Tavern Road</street1>
                <city>Ewing</city>
                <stateOrCountry>NJ</stateOrCountry>
                <stateOrCountryDescription>NEW JERSEY</stateOrCountryDescription>
                <zipCode>08628</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Stephany</firstName>
                <lastName>Foster</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>820 Bear Tavern Road</street1>
                <city>Ewing</city>
                <stateOrCountry>NJ</stateOrCountry>
                <stateOrCountryDescription>NEW JERSEY</stateOrCountryDescription>
                <zipCode>08628</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Biotechnology</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>Decline to Disclose</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06b</item>
        </federalExemptionsExclusions>
```

### R0047 · securities_exemption · 1795387
**Question.** Classify which Securities Act exemption a Form D filing claimed (7.1).
**Field.** `securities_exemption` -- The federal exemption claimed in the Form D filing.
**Answer.** one of: 506b, 506c, 504, reg-a, other, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1795387/000179538720000001/primary_doc.xml

**Text shown to the model:**

```
<entityName>Brewer Lane Ventures Fund I, L.P.</entityName>
        <issuerAddress>
            <street1>c/o Brewer Lane Ventures</street1>
            <street2>8 Hidden Road</street2>
            <city>Weston</city>
            <stateOrCountry>MA</stateOrCountry>
            <stateOrCountryDescription>MASSACHUSETTS</stateOrCountryDescription>
            <zipCode>02493</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>(508) 414-9070</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Limited Partnership</entityType>
        <yearOfInc>
            <withinFiveYears>true</withinFiveYears>
            <value>2019</value>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>N/A</firstName>
                <lastName>Brewer Lane Ventures Fund I GP, LLC</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o Brewer Lane Ventures</street1>
                <street2>8 Hidden Road</street2>
                <city>Weston</city>
                <stateOrCountry>MA</stateOrCountry>
                <stateOrCountryDescription>MASSACHUSETTS</stateOrCountryDescription>
                <zipCode>02493</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification>General Partner of the Issuer (the &quot;General Partner&quot;)</relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>John</firstName>
                <lastName>Kim</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o Brewer Lane Ventures</street1>
                <street2>8 Hidden Road</street2>
                <city>Weston</city>
                <stateOrCountry>MA</stateOrCountry>
                <stateOrCountryDescription>MASSACHUSETTS</stateOrCountryDescription>
                <zipCode>02493</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification>Managing Member of the General Partner</relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Pooled Investment Fund</industryGroupType>
            <investmentFundInfo>
                <investmentFundType>Venture Capital Fund</investmentFundType>
                <is40Act>false</is40Act>
            </investmentFundInfo>
        </industryGroup>
        <issuerSize>
            <revenueRange>Not Applicable</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06c</item>
            <item>3C</item>
            <item>3C.7</item>
        </federalExemptionsExclusions>
```

### R0048 · securities_exemption · 1947170
**Question.** Classify which Securities Act exemption a Form D filing claimed (7.1).
**Field.** `securities_exemption` -- The federal exemption claimed in the Form D filing.
**Answer.** one of: 506b, 506c, 504, reg-a, other, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1947170/000194717022000001/primary_doc.xml

**Text shown to the model:**

```
<entityName>Devorto Corp</entityName>
        <issuerAddress>
            <street1>237 W 24TH STREET</street1>
            <city>NORFOLK</city>
            <stateOrCountry>VA</stateOrCountry>
            <stateOrCountryDescription>VIRGINIA</stateOrCountryDescription>
            <zipCode>23517</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>(757) 416-8312</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <withinFiveYears>true</withinFiveYears>
            <value>2021</value>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Justin</firstName>
                <middleName>Michael</middleName>
                <lastName>Selfridge</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>237 W 24th Street</street1>
                <city>Norfolk</city>
                <stateOrCountry>VA</stateOrCountry>
                <stateOrCountryDescription>VIRGINIA</stateOrCountryDescription>
                <zipCode>23517</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Other Technology</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>No Revenues</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06b</item>
        </federalExemptionsExclusions>
```

### R0049 · safe_pre_post · 837852_000110465921011524
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/837852/000110465921011524/tm215180d1_ex10-1.htm

**Text shown to the model:**

```
ch written determination, this Safe shall convert into Ordinary Shares equal to the Purchase Amount divided by such Fair Value as determined by the Expert Valuer.   The Expert Valuer shall act as experts and not as arbitrators and their determination shall be final and binding on the parties (in the absence of fraud or manifest error). The Company will give the Expert Valuer access to all accounting records or other relevant documents of the Company subject to the Expert Valuer agreeing to such confidentiality provisions as the Company may reasonably impose.   Following any such valuation process and conversion, both the Company and the Investor shall work expeditiously to issue Capital Shares to the Investor.   (c) Liquidity Event . If there is a Liquidity Event before the termination of this Safe, this Safe will automatically be entitled (subject to the liquidation priority set forth in Section 1(e) below) to receive a portion of Proceeds, due and payable to the Investor immediately prior to, or concurrent with, the consummation of such Liquidity Event, equal to the Purchase Amount (the “ Cash-Out Amount ”). If any of the Company’s securityholders are given a choice as to the form and amount of Proceeds to be received in a Liquidity Event, the Investor will be given the same choice, provided that the Investor may not choose to receive a form of consideration that the Investor would be ineligible to receive as a result of the Investor’s failure to satisfy any requirement or limitation generally applicable to the Company’s securityholders, or under any applicable laws.     PRE-MONEY VALUATION CAP     Notwithstanding the foregoing, in connection with a Change of Control intended to qualify as a tax-free reorganization, the Company may reduce the cash portion of Proceeds payable to the Investor by the amount determined by its board of directors in good faith for such Change of Control to qualify as a share reorganization for HM Revenue & Customs purposes, provided that such reduction (A) does not reduce the total Proceeds payable to such Investor and (B) is applied in the same manner and on a pro rata basis to all securityholders who have equal priority to the Investor under Section 1(e).   (d) Dissolution Event . If there is a Dissolution Event before the termination of this Safe, the Investor will automatically be entitled (subject to the liquidation priority set forth in Section 1(e) below) to receive a portion of Proceeds equal to the Cash-Out Amount, due and payable to the Investor immediately prior to the consummation of the Dissolution Event.   (e) Liquidation Priority . In a Liquidity Event or Dissolution Event, this Safe is intended to operate like Ordinary Shares. The Investor’s right to receive its Cash-Out Amount is:   (i)       Junior to payment of outstanding indebtedness and creditor claims, including contractual claims for payment; and   (ii)      On par with payments for other Safes and/or Ordinary Shares and if the applicable Proceeds are insufficient to permit full payments to the Investor and such other Safes and/or Ordinary Shares, the applicable Proceeds will be distributed pro rata to the Investor and such other Safes and
```

### R0050 · preference_seniority · 1123195_000112319502000020
**Question.** Classify multi-series preferred liquidation seniority as pari-passu or stacked (1.3.4).
**Field.** `preference_seniority` -- Whether preferred series rank equally (pari-passu) or in a seniority order (stacked).
**Answer.** one of: pari-passu, stacked, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1123195/000112319502000020/amendment.txt

**Text shown to the model:**

```
y common stock or any other class or series of capital stock ranking junior to the Series A Preferred Stock, an amount in cash per outstanding share of the Series A Preferred Stock equal to $1.00 (the "Series A Liquidation Preference"). If the assets of the Corporation are not sufficient to pay in full the Series A Liquidation Preference payable to the holders of outstanding shares of Series A Preferred Stock and the liquidation preference of all other securities that rank pari passu with the Series A Preferred Stock, then the holders of all such shares shall share ratably in such distribution of assets in proportion to the amount which would be payable on such distribution if the Series A Liquidation Preference to which the holders of outstanding shares of Series A Preferred Stock and the liquidation preferences to which the holders of other securities that rank pari passu with the Series A Preferred Stock are entitled were paid in full. Upon any such liquidation, dissolution or winding up of the Corporation, after the holders of Series A Preferred Stock shall have been paid in full their Series A Liquidation Preference, the holders of shares of Series A Pref
```

### R0051 · fully_diluted_basis · actelis_body
**Question.** Classify capitalization definition as fully-diluted or issued-outstanding basis (3.4).
**Field.** `fully_diluted_basis` -- Whether cap is computed on fully-diluted or issued-outstanding basis.
**Answer.** one of: fully-diluted, issued-outstanding, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1141284/000121390022020064/fs12022_actelisnet.htm

**Text shown to the model:**

```
ertible Preferred Shares &#x00a0; $ 5,585 &#x00a0; &#x00a0; &#x00a0; &#x00a0; &#x00a0; &#x00a0; &#x00a0; Capital Deficiency: &#x00a0; &#x00a0; &#x00a0; &#x00a0; &#x00a0; &#x00a0; &#x00a0; &#x00a0; &#x00a0; &#x00a0; Common stock, $0.000001 par value; 506,428,470 shares authorized; 94,318,590 shares issued and outstanding, actual; &#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0; shares authorized and &#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0;&#x00a0; issued and outstanding, pro form
```

### R0052 · board_seats_investor · 0001104659-17-048201_a17-18633_1ex10d6_opal
**Question.** Extract the number of board seats an investor has the right to designate (5.1).
**Field.** `board_seats_investor` -- the number of board seats the investor/investor class may designate
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
“Investor” as defined in the Master Transaction Agreement. Capitalized terms used in this Agreement and not otherwise defined herein shall have the meanings assigned to them in the Master Transaction Agreement; and   WHEREAS, in connection with the Opal Sheppard acquisition of equity securities of Emergent upon the Closing of the Transactions described in the Master Transaction Agreement, Emergent desires to permit Opal Sheppard to designate one (1) director to the board of directors of Emergent (the “ Board ”).   NOW, THEREFORE, in consideration of the mutual covenants and promises contained herein and for other good and valuable consideration, the receipt and adequacy of which are hereby acknowledged, Emergent and Opal Sheppard agree as follows:   SECTION 1.                             Defined Terms .   “ Related Fund ” means, with respect to any Person, any fund, account or investment vehicle that is controlled or managed by (i) such Person, (ii) an Affiliate of such Person or (iii) the same investment manager, advisor or subadvisor as such Person or an Affiliate of such investment manager, advisor or subadvisor.   SECTION 2.                             Designation of Director .   2.1                                On the Closing Date, James Hua (the “ Designated Director ”) shall be added to the Board to fill an existing va
```

### R0053 · securities_exemption · 1981408
**Question.** Classify which Securities Act exemption a Form D filing claimed (7.1).
**Field.** `securities_exemption` -- The federal exemption claimed in the Form D filing.
**Answer.** one of: 506b, 506c, 504, reg-a, other, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1981408/000198140823000001/primary_doc.xml

**Text shown to the model:**

```
<entityName>McBride Sisters Collections, Inc.</entityName>
        <issuerAddress>
            <street1>6114 LA SALLE AVENUE, SUITE 280</street1>
            <city>OAKLAND</city>
            <stateOrCountry>CA</stateOrCountry>
            <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
            <zipCode>94611</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>831-915-8016</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <issuerPreviousNameList>
            <previousName>McBride Sisters Collections</previousName>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <overFiveYears>true</overFiveYears>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Robin</firstName>
                <lastName>McBride</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>6114 La Salle Ave #280</street1>
                <city>Oakland</city>
                <stateOrCountry>CA</stateOrCountry>
                <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
                <zipCode>94611</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Andrea</firstName>
                <lastName>McBride</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>6114 La Salle Ave #280</street1>
                <city>Oakland</city>
                <stateOrCountry>CA</stateOrCountry>
                <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
                <zipCode>94611</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
                <relationship>Promoter</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Richelieu</firstName>
                <lastName>Dennis</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>6114 La Salle Ave #280</street1>
                <city>Oakland</city>
                <stateOrCountry>CA</stateOrCountry>
                <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
                <zipCode>94611</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Alain</firstName>
                <lastName>Barbet</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>6114 La Salle Ave #280</street1>
                <city>Oakland</city>
                <stateOrCountry>CA</stateOrCountry>
                <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
                <zipCode>94611</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Other</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>Decline to Disclose</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06b</item>
        </federalExemptionsExclusions>
```

### R0054 · fully_diluted_basis · sybari_ex
**Question.** Classify capitalization definition as fully-diluted or issued-outstanding basis (3.4).
**Field.** `fully_diluted_basis` -- Whether cap is computed on fully-diluted or issued-outstanding basis.
**Answer.** one of: fully-diluted, issued-outstanding, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1139764/000095012304006427/y96720exv3w1.txt

**Text shown to the model:**

```
an amount determined by multiplying the Applicable Conversion Value by a fraction: (1) the numerator of which shall be (a) the number of shares of Common Stock outstanding immediately prior to the issuance of such additional shares of Common Stock (calculated on a fully diluted basis assuming the conversion of all outstanding Series B Preferred Stock and the conversion or exercise of all outstanding securities then convertible or exercisable for Common Stock), plus (b) the number of shares of Common Stock which the net aggregate consideration, if any, received by the Corporation for the total nu
```

### R0055 · liquidation_preference_multiple · 1236997_000106299308001834
**Question.** Classify liquidation preference multiple (1x, 2x, 3x, other, non-participating) (leaf 1.3.1).
**Field.** `liquidation_preference_multiple` -- How many times the OIP the preferred holder receives upon liquidation.
**Answer.** one of: non-participating, 1x, 2x, 3x, other, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
a) Authorized (Continued)       In the event of any liquidation, dissolution or winding up of the Corporation, whether voluntary or involuntary, the holders of the Class C Voting Preferred shares are entitled to receive, in preference to any distribution of any of the assets or surplus funds of the Corporation to the holders of any other shares of any series or classes of stock an amount per Preferred share equal to one (1) times the original issue price of US$1.19 per Preferred share (as adjusted for any stock dividends, combinations or splits) ("Original Issue Price"), plus all declared but unpaid dividends.       In the event of any liquidation, dissolution or winding up of the Corporation, whether voluntary or involuntary, the holders of the Class B Voting Preferred shares are entitled to receive, subject to the prior rights of the Class C Voting Preferred shares as set forth above in preference to any distribution of any of the assets or surplus funds of the Corporation to the holders of any other shares of any series or classes of stock an amount per Preferred share equal to one (1) times the original issue price of US$1.40 per Preferred share (as adjusted for any stock dividends, combinations or splits) ("Original Issue Price"), plus all declared but unpaid dividends.       In the event of any liqui
```

### R0056 · s1_use_of_proceeds · civitas
**Question.** Extract the primary stated use of IPO proceeds from a real S-1/424B4 filing (7.3).
**Field.** `s1_use_of_proceeds` -- the primary stated use of proceeds, as an exact verbatim phrase copied from the text
**Answer.** string value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1608638/000119312514340497/d729354ds1a.htm

**Text shown to the model:**

```
and Exchange Commission (the &#147;SEC&#148;), and under SEC rules, is currently a voluntary filer. We intend to use the net proceeds from the sale of common stock by us in this offering to redeem all of the senior notes. Upon completion of that redemption, NMHI will cease to be a voluntary filer and will cease filing reports with the SEC. 8 Table of Contents Corporate Structure The chart below sets forth our current corporate structure and gives effect to the issuance of the shares in this offering. The ownership
```

### R0057 · information_rights · 0000950134-06-004765_c01111s1exv4w4
**Question.** Classify whether a document grants investors a live financial-reporting/information right (5.3).
**Field.** `information_rights` -- yes if a live obligation to deliver financials to investors exists, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
EX-4.4 6 c01111s1exv4w4.htm WAIVER TO INVESTORS' RIGHTS AGREEMENT exv4w4   Exhibit 4.4 March 30, 2005 Ms. Paula J. Norbom Vice President, Finance Restore Medical Inc. 2800 Patton Road St. Paul, MN 55113      Re:       Delivery of Audited Financial Statements Dear Ms. Norbom:      Reference is made to that certain Investors’ Rights Agreement dated as of January 28, 2004, as amended by that certain First Amendment to Investors’ Rights Agreement dated as of March 17, 2005 (as further amended, restated, modified or supplemented from time to time, the “ Investors’ Rights Agreement ”) by and among Restore Medical Inc., a Delaware corporation (f/k/a Restore Medical, Inc., a Minnesota corporation) (the “ Company ”), the investors and other stockholders of the Company listed on Schedule A thereto (the “ Investors ”) and the holders of the Company’s capital stock listed on Schedule B thereto (the “ Founders ”). Unless otherwise defined herein, capitalized terms
```

### R0058 · fully_diluted_basis · castlebio_body
**Question.** Classify capitalization definition as fully-diluted or issued-outstanding basis (3.4).
**Field.** `fully_diluted_basis` -- Whether cap is computed on fully-diluted or issued-outstanding basis.
**Answer.** one of: fully-diluted, issued-outstanding, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1447362/000114036120014751/nt10012655x7_424b4.htm

**Text shown to the model:**

```
3; &#8203; &#8203; &#8203; Preferred stock, par value $0.001 per share; 10,000,000 shares authorized, no shares issued and outstanding, actual and as adjusted. &#8203; &#8203; &#8212; &#8203; &#8203; &#8212; Common stock, par value $0.001 per share, 200,000,000 shares authorized, 17,203,496 shares issued and outstanding, actual; and 200,000,000 shares authorized, 19,203,496 shares issued and outstanding, as adjusted &#8203; &#8203; 17 &#8203; &#8203; 19 Additional paid-in capital &#8203; &#8203; 139,559 &#8203; &#8203; 208,642 Accumulated deficit &#8203; &#8203; (51,642 )
```

### R0059 · flag_internal_inconsistency · actelis_consistent
**Question.** Flag whether two real share-count citations in the same filing are numerically consistent (8.6).
**Field.** `flag_internal_inconsistency` -- true if the two cited share counts differ, false if they match
**Answer.** bool value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1141284/000121390022020064/fs12022_actelisnet.htm

**Text shown to the model:**

```
Citation A (Capitalization table (actual column)): "94,318,590 shares issued and outstanding, actual"

Citation B (Balance sheet as of December 31, 2021): "94,318,590 and 94,191,508 shares issued and outstanding as of December&#x00a0;31, 2021, and 2020, respectively"
```

### R0060 · safe_cap_vs_discount_applies · snm_discount_only
**Question.** Classify whether a SAFE uses cap, discount, or both-MFN for conversion pricing (2.1.3).
**Field.** `safe_cap_vs_discount_applies` -- Whether the SAFE's conversion price uses cap-only, discount-only, or both with MFN.
**Answer.** one of: cap, discount, both-mfn, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
ED UNDER THE ACT AND APPLICABLE STATE SECURITIES LAWS PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT OR AN EXEMPTION THEREFROM.   SNM GLOBAL HOLDINGS, INC.   SAFE   (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by _______________________________ (the “ Investor ”) of $________________ (the “ Purchase Amount ”) on or about _____________, SNM Global Holdings, Inc., a Nevada corporation (the “ Company ”), hereby issues to the Investor the right to certain shares of the Company’s capital stock, subject to the terms set forth below.   The “ Discount Rate ” is fifty percent (50%).   See Section 2 for certain additional defined terms.   1.       Events   (a)  Equity Financing . If there is an Equity Financing before the expiration or termination of this instrument, the Company will automatically issue to the Investor a number of shares of Safe Stock equal to the Purchase Amount divided by the Discount Price. For every two (2) Safe Stock shares issued per the terms of this Agreement, the Investor shall also be issued one (1) warrant with an exercise price equal to the Discount Price.     In connection with the issuance of Safe Stock by the Company to the Investor pursuant to this Section 1(a):   (i) The Investor will execute and deliver to the Company all transaction documents related to the Equity Financing; provided, that such documents are the same documents to be entered into with the purchasers of Common Stock, with appropriate variations for the Common Stock if applicable, and provided further, that such documents have customary exceptions to any drag-along applicable to the Investor, including, without limitation, limited representations and warranties and limited liability and indemnification obligations on the part of the Investor; and   (ii) The Investor and the Company will execute a Pro Rata Rights Agreement, unless the Investor is already included in such rights in the transaction documents related to the Equity Financing.    (b)  Liquidity
```

### R0061 · safe_pre_post · 1821951_000121390022000982
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1821951/000121390022000982/ea153649ex3-1_creciinc.htm

**Text shown to the model:**

```
EX1A-3 HLDRS RTS 5 ea153649ex3-1_creciinc.htm FORM OF SAFES Exhibit 3.1   POST-MONEY VALUATION CAP WITH DISCOUNT   THIS INSTRUMENT AND ANY SECURITIES ISSUABLE PURSUANT HERETO HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE “ SECURITIES ACT ”), OR UNDER THE SECURITIES LAWS OF CERTAIN STATES. THESE SECURITIES MAY NOT BE OFFERED, SOLD OR OTHERWISE TRANSFERRED, PLEDGED OR HYPOTHECATED EXCEPT AS PERMITTED IN THIS SAFE AND UNDER THE ACT AND APPLICABLE STATE SECURITIES LAWS PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT OR AN EXEMPTION THEREFROM.   CRECI INC.   SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by [NAME] (the “ Investor ”) of [AMOUNT] ( $__________ ) (the “ Purchase Amount ”) on or about [DATE], CRECI INC. , a Delaware corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   This Safe is based on one of the forms available at http://ycombinator.com/documents, modified as agreed by Investor and the Company.   The “ Post-Money Valuation Cap ” is Two Million U.S. Dollars ($2,000,000) .   The “ Discount Rate ” is Eighty Percent (80%) .   See Section 2 for certain additional defined terms.   1. Events   (a) Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the number of shares of Safe Preferred Stock equal to the Purchase Amount divided by the Conversion Price.   In connection with the automatic conversion of this Safe into shares of Safe Preferred Sto
```

### R0062 · securities_exemption · 1498738
**Question.** Classify which Securities Act exemption a Form D filing claimed (7.1).
**Field.** `securities_exemption` -- The federal exemption claimed in the Form D filing.
**Answer.** one of: 506b, 506c, 504, reg-a, other, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1498738/000149873814000005/primary_doc.xml

**Text shown to the model:**

```
<entityName>VoCare, Inc.</entityName>
        <issuerAddress>
            <street1>8888 KEYSTONE CROSSING</street1>
            <street2>SUITE 1300</street2>
            <city>INDIANAPOLIS</city>
            <stateOrCountry>IN</stateOrCountry>
            <stateOrCountryDescription>INDIANA</stateOrCountryDescription>
            <zipCode>46240</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>(317) 973-1003</issuerPhoneNumber>
        <jurisdictionOfInc>INDIANA</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <withinFiveYears>true</withinFiveYears>
            <value>2009</value>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Steven</firstName>
                <middleName>R</middleName>
                <lastName>Peabody</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>8888 Keystone Crossing</street1>
                <street2>Suite 1300</street2>
                <city>Indianapolis</city>
                <stateOrCountry>IN</stateOrCountry>
                <stateOrCountryDescription>INDIANA</stateOrCountryDescription>
                <zipCode>46240</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
                <relationship>Promoter</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Other Health Care</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>Decline to Disclose</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06c</item>
        </federalExemptionsExclusions>
```

### R0063 · s1_use_of_proceeds · hyrecar
**Question.** Extract the primary stated use of IPO proceeds from a real S-1/424B4 filing (7.3).
**Field.** `s1_use_of_proceeds` -- the primary stated use of proceeds, as an exact verbatim phrase copied from the text
**Answer.** string value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1713832/000121390019013300/f424b4071819_hyrecarinc.htm

**Text shown to the model:**

```
$11,121,250 if the underwriter&rsquo;s option to purchase additional shares is exercised in full). We intend to use the net proceeds to us from this offering for general corporate purposes, including working capital, sales, customer support, technology and marketing activities, and general and administrative matters. See &ldquo;Use of Proceeds&rdquo; for more information. Nasdaq Capital Market symbol &ldquo;HYRE.&rdquo; Risk factors This investment involves a high degree of risk. You should read the descriptio
```

### R0064 · vesting_schedule · 0001451809-24-000052_ex1034offerofemployment-sa
**Question.** Extract and normalize vesting schedule to canonical string format (6.1).
**Field.** `vesting_schedule` -- Normalized vesting schedule: e.g. '4yr/1yr-cliff', '3yr/no-cliff', '4yr/cliff'.
**Answer.** string value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
of Directors of MegaChips (the "MegaChips Board"), you will be granted an option to purchase 16,000 shares of MegaChips common stock (the "MegaChips Option"). The MegaChips Option will be granted under the MegaChips Equity Plan (the "MegaChips Equity Plan") and will be governed by and subject to the terms and conditions of the MegaChips Equity Plan and the applicable stock option grant notice and option agreement thereunder ("Option Documents"). Subject to applicable laws, the MegaChips Option will be subject to a four-year vesting schedule with no cliff, provided that you are continuously employed with the Company and/or MegaChips on each applicable vesting date. The Company plans to adopt a profit sharing plan for 2017 and 2018. If you are an employee in good standing at the time it is adopted and otherwise meet the eligibility criteria for participation in the plan at such time, you will be eligible to participate in such plan. Based on current projections, which may change based on business operating results in the future, it is expected that your interest in such plan would be 3%. The Company may c
```

### R0065 · fully_diluted_basis · hyrecar_body
**Question.** Classify capitalization definition as fully-diluted or issued-outstanding basis (3.4).
**Field.** `fully_diluted_basis` -- Whether cap is computed on fully-diluted or issued-outstanding basis.
**Answer.** one of: fully-diluted, issued-outstanding, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1713832/000121390019013300/f424b4071819_hyrecarinc.htm

**Text shown to the model:**

```
s. As of March 31, 2019 Actual As Adjusted (unaudited) (in thousands, except share and per share data) Cash, cash equivalents and short-term investments $ 6,338,871 $ 15,963,871 Stockholders&rsquo; equity: Common stock, par value $0.00001 per share; 50,000,000 shares authorized, 12,191,508 shares issued and outstanding, actual; 50,000,000 shares authorized, 15,691,508 shares issued and outstanding, as adjusted 122 157 Preferred stock, par value $0.00001 per share; 15,000,000 shares authorized, no shares issued and outstanding, actual and as adjusted &mdash; &mdash; Additi
```

### R0066 · flag_internal_inconsistency · castlebio_inconsistent
**Question.** Flag whether two real share-count citations in the same filing are numerically consistent (8.6).
**Field.** `flag_internal_inconsistency` -- true if the two cited share counts differ, false if they match
**Answer.** bool value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1447362/000114036120014751/nt10012655x7_424b4.htm

**Text shown to the model:**

```
Citation A (Capitalization table (actual column)): "17,203,496 shares issued and outstanding, actual"

Citation B (Beneficial-ownership table 'Before Offering' basis): "is based on 17,360,096 shares of common stock outstanding as of May 29, 2020"
```

### R0067 · vesting_schedule · 0001516513-23-000036_ex-107xcraigoverpeckofferl
**Question.** Extract and normalize vesting schedule to canonical string format (6.1).
**Field.** `vesting_schedule` -- Normalized vesting schedule: e.g. '4yr/1yr-cliff', '3yr/no-cliff', '4yr/cliff'.
**Answer.** string value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
EX-10.7 2 ex-107xcraigoverpeckofferl.htm EX-10.7 Document Exhibit 10.7 April 27, 2023 Craig Overpeck Dear Craig, We are excited to offer you a spot on our growing team at Doximity. Here are the details you likely care about most: Title        SVP, Commercial Operations Start Date     May 16, 2023 Annual Salary     $300,000 Equity Grants    $4M 4yr RSU, vests qtrly, no cliff $4M 4yr PSU, vests annually based on % to (stretch) goal Benefits        Health insurance, 401k, Discretionary Time Off & more* The equity grants in this offer letter will be granted upon your conversion from consultant to employee and will replace all previously issued grants. For the avoidance of doubt, the Services Agreement between you and Doximity dated as of November 18, 2022, and the equity grants associated therewith (except for the first vest tranche of May 15, 2023), will be terminated and of no further force or effect (except for those terms
```

### R0068 · safe_cap_vs_discount_applies · parker_both_mfn
**Question.** Classify whether a SAFE uses cap, discount, or both-MFN for conversion pricing (2.1.3).
**Field.** `safe_cap_vs_discount_applies` -- Whether the SAFE's conversion price uses cap-only, discount-only, or both with MFN.
**Answer.** one of: cap, discount, both-mfn, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
(on an as-converted basis) issued and outstanding, assuming exercise or conversion of all outstanding vested and unvested options, warrants and other convertible securities, but excluding (A) this instrument, (B) all other Safes, and (C) convertible promissory notes; and ( 2 ) all shares of Common Stock reserved and available for future grant under any equity incentive or similar plan of the Company, and/or any equity incentive or similar plan to be created or increased in connection with the Equity Financing.   “ Conversion Price ” means either: (1) the Safe Price or (2) the Discount Price, whichever calculation results in a greater number of shares of Safe Preferred Stock.   “ Discount Price ” means the price per share of the Standard Preferred Stock sold in the Equity Financing multiplied by the Discount Rate.   “ Distribution ” means the transfer to holders of Capital Stock by reason of their ownership thereof of cash or other property without consideration whether by way of dividend or otherwise, other than dividends on Common Stock payable in Common Stock, or the purchase or redemption of Capital Stock by the Company or its subsidiaries for cash or property other than: (i) repurchases of Common Stock held by employees, officers, directors or consultants of the Company or its subsidiaries pursuant to an agreement providing, as applicable, a right of first refusal or a right to repurchase shares upon termination of such service provider’s employment or services; or (ii) repurchases of Capital Stock in connection with the settlement of disputes with any stockholder.   - 2 -     “ Dissolution Event ” means (i) a voluntary termination of operations, (ii) a general assignment for the benefit of the Company’s creditors or (iii) any other liquidation, dissolution or winding up of the Company ( excluding a Liquidity Event), whether voluntary or involuntary.   “ Equity Financing ” means a bona fide transaction or series of transactions with the principal purpose of raising capital, pursuant to which the Company issues and sell
```

### R0069 · cliff_present · 0001144204-18-050119_tv502422_10k
**Question.** Classify whether a vesting schedule includes a cliff blockage period (6.2).
**Field.** `cliff_present` -- yes if the schedule has a cliff blockage period, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
der the 2017 Plan, and no shares were available for grant under the 2007 Plan. All incentive stock award grants prior to the adoption of the 2017 Plan on November 21, 2017 were made under the 2007 Plan, and all incentive stock award grants after the adoption of the 2017 Plan on November 21, 2017 were made under the 2017 Plan.   The majority of awards issued under the Plan vest immediately or over three years, with a one year cliff vesting period, and have a term of ten years. Stock-based compensation cost is measured at the grant date, based on the fair value of the awards that are ultimately expected to vest, and recognized on a straight-line basis over the requisite service period, which is generally the vesting period.   The following table summarizes vested and unvested stock option activity:       All Options     Vested Options     Unvested Options       Shares     Weighted Average Exercise Price     Shares     Weighted Average Exercise Price     Shares     Weighted Average Exercise Price   Outstanding at July 1, 2016     2,717,193       1.16       2,517,333       1.17       199,860       1.06   Granted     630,117       1.11       542,000       1.12       88,117       1.05   Options vesting     -       -       152,518       1.04       (152,518 )     1.04   Exercised     -       -       -       -       -       -   Forfeite
```

### R0070 · safe_valuation_cap · 1811623_000110465922070160_cap
**Question.** Extract the valuation cap from a SAFE agreement (2.1.1)
**Field.** `safe_valuation_cap` -- the valuation cap in dollars as a bare integer (no $ or commas)
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
Inc.   SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by Amar Foundation (the “ Investor ”) of $5,000,000 (the “ Purchase Amount ”) on or about March 19, 2021, PaxMedica, Inc., a Delaware corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   The “ Post-Money Valuation Cap ” is $150,000,000.00.   The “ Discount Rate ” is 50%.   See Section 2 for certain additional defined terms.   1.        Events   (a)     Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the number of shares of Safe Capital Stock equal to the Purchase Amount divided by the Conversion Price.   In connection with the automatic conversion of this Safe into shares of Safe Capital Stock, the Investor will execute and deliver to the Company all of the transaction documents related to the Equity Financing; provided, that such documents (i) are the same documents to be entered into with the purchasers of Standard Capital Stock, with appropriate variations for the Safe Capital Stock if applicable, and (ii) have customary exceptions to any drag-along applicable to the Investor, including
```

### R0071 · round_size · 1981408
**Question.** Extract the total aggregate financing round size in dollars (1.2.1).
**Field.** `round_size` -- total aggregate dollar amount raised in the equity financing round
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1981408/000198140823000001/primary_doc.xml

**Text shown to the model:**

```
<entityName>McBride Sisters Collections, Inc.</entityName>
        <issuerAddress>
            <street1>6114 LA SALLE AVENUE, SUITE 280</street1>
            <city>OAKLAND</city>
            <stateOrCountry>CA</stateOrCountry>
            <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
            <zipCode>94611</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>831-915-8016</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <issuerPreviousNameList>
            <previousName>McBride Sisters Collections</previousName>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <overFiveYears>true</overFiveYears>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Robin</firstName>
                <lastName>McBride</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>6114 La Salle Ave #280</street1>
                <city>Oakland</city>
                <stateOrCountry>CA</stateOrCountry>
                <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
                <zipCode>94611</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Andrea</firstName>
                <lastName>McBride</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>6114 La Salle Ave #280</street1>
                <city>Oakland</city>
                <stateOrCountry>CA</stateOrCountry>
                <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
                <zipCode>94611</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
                <relationship>Promoter</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Richelieu</firstName>
                <lastName>Dennis</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>6114 La Salle Ave #280</street1>
                <city>Oakland</city>
                <stateOrCountry>CA</stateOrCountry>
                <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
                <zipCode>94611</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Alain</firstName>
                <lastName>Barbet</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>6114 La Salle Ave #280</street1>
                <city>Oakland</city>
                <stateOrCountry>CA</stateOrCountry>
                <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
                <zipCode>94611</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Other</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>Decline to Disclose</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06b</item>
        </federalExemptionsExclusions>
        <typeOfFiling>
            <newOrAmendment>
                <isAmendment>false</isAmendment>
            </newOrAmendment>
            <dateOfFirstSale>
                <value>2022-10-11</value>
            </dateOfFirstSale>
        </typeOfFiling>
        <durationOfOffering>
            <moreThanOneYear>false</moreThanOneYear>
        </durationOfOffering>
        <typesOfSecuritiesOffered>
            <isOptionToAcquireType>true</isOptionToAcquireType>
            <isSecurityToBeAcquiredType>true</isSecurityToBeAcquiredType>
        </typesOfSecuritiesOffered>
        <businessCombinationTransaction>
            <isBusinessCombinationTransaction>false</isBusinessCombinationTransaction>
            <clarificationOfResponse></clarificationOfResponse>
        </businessCombinationTransaction>
        <minimumInvestmentAccepted>0</minimumInvestmentAccepted>
        <salesCompensationList></salesCompensationList>
        <offeringSalesAmounts>
            <totalOfferingAmount>25500000</totalOfferingAmount>
            <totalAmountSold>14040000</totalAmountSold>
            <totalRemaining>11460000</totalRemaining>
```

### R0072 · round_size · 1601118
**Question.** Extract the total aggregate financing round size in dollars (1.2.1).
**Field.** `round_size` -- total aggregate dollar amount raised in the equity financing round
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1601118/000160111814000001/primary_doc.xml

**Text shown to the model:**

```
<entityName>BEYONDCORE, INC.</entityName>
        <issuerAddress>
            <street1>983 SHOAL DRIVE</street1>
            <city>SAN MATEO</city>
            <stateOrCountry>CA</stateOrCountry>
            <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
            <zipCode>94404</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>650-430-0355</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <overFiveYears>true</overFiveYears>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Arijit</firstName>
                <lastName>Sengupta</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o BeyondCore, Inc.</street1>
                <street2>983 Shoal Drive</street2>
                <city>San Mateo</city>
                <stateOrCountry>CA</stateOrCountry>
                <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
                <zipCode>94404</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Other Technology</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>Decline to Disclose</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06b</item>
        </federalExemptionsExclusions>
        <typeOfFiling>
            <newOrAmendment>
                <isAmendment>false</isAmendment>
            </newOrAmendment>
            <dateOfFirstSale>
                <value>2014-02-12</value>
            </dateOfFirstSale>
        </typeOfFiling>
        <durationOfOffering>
            <moreThanOneYear>false</moreThanOneYear>
        </durationOfOffering>
        <typesOfSecuritiesOffered>
            <isEquityType>true</isEquityType>
            <isOtherType>true</isOtherType>
            <descriptionOfOtherType>Series A Preferred Stock and the common stock issuable upon conversion thereof.</descriptionOfOtherType>
        </typesOfSecuritiesOffered>
        <businessCombinationTransaction>
            <isBusinessCombinationTransaction>false</isBusinessCombinationTransaction>
            <clarificationOfResponse></clarificationOfResponse>
        </businessCombinationTransaction>
        <minimumInvestmentAccepted>0</minimumInvestmentAccepted>
        <salesCompensationList></salesCompensationList>
        <offeringSalesAmounts>
            <totalOfferingAmount>10155142</totalOfferingAmount>
            <totalAmountSold>8881213</totalAmountSold>
            <totalRemaining>1273929</totalRemaining>
```

### R0073 · safe_valuation_cap · 746210_000143774926019366_cap
**Question.** Extract the valuation cap from a SAFE agreement (2.1.1)
**Field.** `safe_valuation_cap` -- the valuation cap in dollars as a bare integer (no $ or commas)
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
ment Amount ”) on or about the date of this Safe, MANAKO LABS LTD , a company incorporated in England and Wales with company number 17048521 and whose registered office is at 71-75 Shelton Street, Covent Garden, London, United Kingdom, WC2H 9JQ (the “ Company ”), grants the Investor the right to subscribe for certain shares in the capital of the Company, subject to the terms below.   The “ Post-Money Valuation Cap ” is $40,000,000.   The “ Discount Rate ” is 80% (representing a 20% discount to the price per share of the Senior Shares in the Equity Financing).   Condition to Effectiveness   This Safe is conditional on the concurrent execution and delivery by the Company and the Investor of the Technology License and Distribution Agreement dated on or about the date of this Safe (the "TLDA"). This Safe shall not take effect and the Investment Amount shall not be due and payable until the TLDA has been duly executed and delivered by both the Company and the Investor. If the TLDA has not been executed and delivered by both parties within five (5) days of the date of this Safe, either party may terminate this Safe by written notice to the other, whereupon this Safe shall be of no further force or effect and neither party shall have any further obligation to the other, save that the confidentiality obligations set out
```

### R0074 · safe_pre_post · 1838987_000121390024014892
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1838987/000121390024014892/ea193922ex10-1_complete.htm

**Text shown to the model:**

```
EX-10.1 2 ea193922ex10-1_complete.htm FORM OF SAFE (2024) Exhibit 10.1   THIS INSTRUMENT AND ANY SECURITIES ISSUABLE PURSUANT HERETO HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE “ SECURITIES ACT ”), OR UNDER THE SECURITIES LAWS OF CERTAIN STATES. THESE SECURITIES MAY NOT BE OFFERED, SOLD OR OTHERWISE TRANSFERRED, PLEDGED OR HYPOTHECATED EXCEPT AS PERMITTED IN THIS SAFE AND UNDER THE ACT AND APPLICABLE STATE SECURITIES LAWS PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT OR AN EXEMPTION THEREFROM.   COMPLETE SOLARIA, INC.   SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by RODGERS FAMILY FREEDOM AND FREE MARKETS CHARITABLE TRUST (the “ Investor ”) of $_________________ (the “ Purchase Amount ”) on or about ___________________, and COMPLETE SOLARIA, INC., a Delaware corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   The “ Pre-Money Valuation Cap ” is $ 53,540,000.00 ($1.24/share) The “ Discount Rate ” is 80%. See Section 2 for certain additional defined terms. 1. Events   (a) Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the number of shares of Common Stock equal to the Purchase Amount divided by the Conversion Price.   In connection with the automatic conversion of this Safe into shares of Common Stock, the Investor will execute and deliver to the Company all of the transaction documents related to the Equity Financing; provided, that such documents (i) are the same documents to be entered into with the other purchasers of Common Stock, with appropriate variations for the Common Stock if applicable, and (ii) have customary exceptions to any drag-along applicable to the Investor, including (without limitation) limited representations, warranties, liability and indemnification obligations for the Investor.   (b) Liquidity Event . If there is a Liquidity Event before the termination of this Safe, this Safe will automatically be entitled (subject to the liquidation priority set forth in Section 1(d) below) to receive a portion of Proceeds, due and payable to the Investor immediately prior to, or concurrent with, the consummation of such Liquidity Event, equal to the greater of (i) the Purchase Amount (the “ Cash-Out Amount ”) or (ii) the amount payable on the number of shares of Common Stock equal to the Purchase Amount divided by the Liquidity Price (the “ Conver
```

### R0075 · preference_seniority · 1477449_000155837016008265
**Question.** Classify multi-series preferred liquidation seniority as pari-passu or stacked (1.3.4).
**Field.** `preference_seniority` -- Whether preferred series rank equally (pari-passu) or in a seniority order (stacked).
**Answer.** one of: pari-passu, stacked, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1477449/000155837016008265/tdoc-20160629ex992f60bc1.htm

**Text shown to the model:**

```
$ 10.0994    1.0000      Subject to limited exceptions, the conversion price for each series of the Preferred Stock was subject to an adjustment to reduce dilution in the event that the Company issued additional equity securities at a purchase price less than the applicable conversion price for such series of the Preferred Stock.   Liquidation Rights   In the event of any voluntary or involuntary liquidation, dissolution or winding up of the Company, the assets of the Company available for distribution will be distributed to the Company’s stockholders in the following order of priority:   · The Series B Stockholders are entitled to receive a preference of $49.5 million prior to the Series A Stockholders receiving any distributions.   · The Series A Preferred stockholders are entitled to receive a distribution of approximately $2.0 million, after which the Common and Series B preferred stockholders share the remaining proceeds pari passu up to the participation cap, after which the remaining proceeds are distributed to the common stockholders.   · The holders of Series B Preferred Stock will reach a participation ca
```

### R0076 · preference_stack_payout · series_b
**Question.** Compute a named preferred series' total payout (preference + accrued dividends) (4.3).
**Field.** `preference_stack_payout` -- target series' liquidation preference plus accrued dividends, in $ millions
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1211759/000119312518039721/d516937dex99c3.htm

**Text shown to the model:**

```
TARGET SERIES: Series B Preferred Stock

Total Projected Preferred Stock as of 12/31/17: $(78.6) million, consisting of: Series A Preferred Stock liquidation preference of $52.0 million plus projected accrued dividends as of 12/31/17 of $6.9 million; and Series B Preferred Stock liquidation preference of $17.5 million plus projected accrued dividends as of 12/31/17 of $2.2 million.
```

### R0077 · safe_cap_vs_discount_applies · sos_both_mfn
**Question.** Classify whether a SAFE uses cap, discount, or both-MFN for conversion pricing (2.1.3).
**Field.** `safe_cap_vs_discount_applies` -- Whether the SAFE's conversion price uses cap-only, discount-only, or both with MFN.
**Answer.** one of: cap, discount, both-mfn, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
series of related transactions in which the holders of the voting securities of the Company outstanding immediately prior to such transaction or series of related transactions retain, immediately after such transaction or series of related transactions, at least a majority of the total voting power represented by the outstanding voting securities of the Company or such other surviving or resulting entity or (iii) a sale, lease or other disposition of all or substantially all of the assets of the Company.     “ Conversion Price ” means the either: (1) the Safe Price or (2) the Discount Price, whichever calculation results in a greater number of shares of Safe Common Stock. “ Discount Price ” means the price per share of the Standard Common Stock sold in the Equity Financing multiplied by the Discount Rate. “ Distribution ” means the transfer to holders of Capital Stock by reason of their ownership thereof of cash or other property without consideration whether by way of dividend or otherwise, other than dividends on Common Stock payable in Common Stock, or the purchase or redemption of Capital Stock by the Company or its subsidiaries for cash or property other than: (i) repurchases of Common Stock held by employees, officers, directors or consultants of the Company or its subsidiaries pursuant to an agreement providing, as applicable, a right of first refusal or a right to repurchase shares upon termination of such service provider’s employment or services; or (ii) repurchases of Capital Stock in connection with the settlement of disputes with any stockholder.   “ Dissolution Event ” means (i) a voluntary termination of operations, (ii) a general assignment for the benefit of the Company’s creditors or (iii) any other liquidation, dissolution or winding up of the Company ( excluding a Liquidity Event), whether voluntary or involuntary. “ Equity Financing ” means a bona fide transaction or series of transactions with the principal purpose of raising capital, pursuant to which the Company issues and sells Preferred Stock
```

### R0078 · liquidation_preference_multiple · 1538716_000119312519245313
**Question.** Classify liquidation preference multiple (1x, 2x, 3x, other, non-participating) (leaf 1.3.1).
**Field.** `liquidation_preference_multiple` -- How many times the OIP the preferred holder receives upon liquidation.
**Answer.** one of: non-participating, 1x, 2x, 3x, other, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
underwritten public offering registered under the Act at a price per share that is less than two times the Original Issue Price of the Series G Preferred Stock, each share of Series G Preferred Stock shall automatically be converted into shares of Common Stock at a Conversion Price equal to the product of (x) (i) the price per share of the Corporation’s Common Stock in the Qualified Public Offering, divided by (ii) two (2) times the Original Issue Price of the Series G Preferred Stock (as appropriately adjusted for stock dividends, combinations or splits) and (y) the Original Issue Price of the Series G Preferred Stock. (A) If a Qualified Public Offering occurs on or before December 15, 2019 and the High End Range Price (as defined below) is less than two (2) times the Original Issue Price of the Series G Preferred Stock, each share of Series G Preferred Stock shall automatically be converted into shares of Common Stock at a Conversion Price equal to the product of (x) (i) the High End Range Price, divided by (ii) two (2) times the Original Issue Price of the Series G Preferred Stock and (y) the Original Issue Price of the Series G Preferred Stock (in each case as appropriately adjusted for stock dividends, combinations or splits after the Effective Time). The “ High End Range Price ” shall mean the price per share of the Corporation’s
```

### R0079 · cliff_present · 0001104659-09-039164_a09-16464_1ex10d1
**Question.** Classify whether a vesting schedule includes a cliff blockage period (6.2).
**Field.** `cliff_present` -- yes if the schedule has a cliff blockage period, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
of any other equity award granted after the Effective Date under the Company Incentive Plan or any successor plan (“Future Equity Award”) that is outstanding and unvested at the time of such termination but that would, but for a termination of employment, have vested during the Severance Period shall vest as of the date of such termination of employment; provided ; however , that, for purposes of this provision, the Cliff Vesting Award and each Future Equity Award that vests at the end of a multi-year period (“Future Cliff Vesting Award”) shall be treated as though it vested annually pro rata over its vesting period ( e.g. , if the date of termination occurred between the one and two-year anniversaries of the Effective Date, 75% of Company RSUs subject to the Cliff Vesting Award would vest on the date of termination and if the date of termination occurred following the two-year anniversary of the Effective Date, all of the Company RSUs subject to the Cliff Vesting Award would vest on the date of termination); provided , further , however , that any Company RSUs that would vest under this provision but for the fact that outstanding performance conditions have not been satisfied shall vest only if, and at such point as, such performance conditions are satisfied.”   b.                                       Section 2 shal
```

### R0080 · preference_seniority · 1076103_000091476003000217
**Question.** Classify multi-series preferred liquidation seniority as pari-passu or stacked (1.3.4).
**Field.** `preference_seniority` -- Whether preferred series rank equally (pari-passu) or in a seniority order (stacked).
**Answer.** one of: pari-passu, stacked, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1076103/000091476003000217/i49644_x31.txt

**Text shown to the model:**

```
ding Business Day. Without the consent of the Holders of 75% of the outstanding shares of the Series D Preferred Stock, the Corporation may not issue any equity securities ranking senior to, or on a parity with, the Series D Preferred Stock. Without the consent of the Holders of 75% of the outstanding shares of the Series C Preferred Stock, the Corporation may not issue any equity securities ranking senior to, or on a parity with, the Series C Preferred Stock. 2. LSA Event. (a) Liquidation Preference and LSA Event. The Shares of Series E Preferred Stock shall rank senior to the Series D Preferred Stock, Series C Preferred Stock, Junior Preferred Stock and Junior Securities as to Liquidation Preference. The shares of Series D Preferred Stock shall rank senior to the Series C Preferred Stock, Junior Preferred Stock and Junior Securities as to Liquidation Preference. The shares of Series C Preferred Stock shall rank senior to the Junior Preferred Stock and Junior Securities as to Liquidation Preference. The shares of Series A Preferred Stock and Series B Preferred Stock shall rank equally as to each other, and senior to the Junior Securities, as to Liquidation
```

### R0081 · form_d_fields · 1549044_000154904412000001
**Question.** Extract the Total Amount Sold field value from a real Form D filing (7.2).
**Field.** `form_d_field_value` -- The extracted Total Amount Sold dollar value from the Form D.
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1549044/000154904412000001/primary_doc.xml

**Text shown to the model:**

```
ning>0</totalRemaining>
            <clarificationOfResponse>Total Offering Amount: $70,227,931.85; Total Amount Sold: $70,227,931.85; Total Remaining to be Sold: $0.
Total Amount Sold included $10,227,942.44 cancellation of indebtedness.</clarificationOfResponse>
        </offeringSalesAmounts>
        <investors>
            <has
```

### R0082 · vesting_schedule · 1108271_000119312504159873
**Question.** Extract and normalize vesting schedule to canonical string format (6.1).
**Field.** `vesting_schedule` -- Normalized vesting schedule: e.g. '4yr/1yr-cliff', '3yr/no-cliff', '4yr/cliff'.
**Answer.** string value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
h full calendar month thereafter until the First New Grant is fully vested;   (b) Second New Grant. The Company granted you an option to purchase six hundred fifty thousand (650,000) shares of the Company’s Common Stock (the “Second New Grant”) at a per share price of twenty cents ($0.20), which is the fair market value of the Common Stock as of March 4, 2004 as determined by the Board. The Second New Grant is governed by the terms and conditions of the Plan and your stock option grant agreement, which includes an eighteen (18) month vesting schedule, contingent upon your continued employment as CEO, pursuant to which one-eighteenth (1/18 th ) of the shares will vest as of July 31, 2004, and on the last day of each full calendar month thereafter until the Second New Grant is fully vested;   (c) Third New Grant. The Company granted you an option to purchase five hundred thousand (500,000) shares of the Company’s Common Stock (the “Third New Grant”) at a per share price of twenty cents ($0.20), which is the fair market value of the Common Stock as of March 4, 2004 as determined by the Board. The Third
```

### R0083 · round_size · 1887997
**Question.** Extract the total aggregate financing round size in dollars (1.2.1).
**Field.** `round_size` -- total aggregate dollar amount raised in the equity financing round
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1887997/000188799721000001/primary_doc.xml

**Text shown to the model:**

```
<entityName>POSEIDON MEDICAL INC.</entityName>
        <issuerAddress>
            <street1>1125 NW 132 AVENUE</street1>
            <city>PEMBROKE PINES</city>
            <stateOrCountry>FL</stateOrCountry>
            <stateOrCountryDescription>FLORIDA</stateOrCountryDescription>
            <zipCode>33028</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>19546550391</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <withinFiveYears>true</withinFiveYears>
            <value>2019</value>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Horace</firstName>
                <middleName>Richard</middleName>
                <lastName>Davis</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>1125 NW 132 Ave</street1>
                <city>Pembroke Pines</city>
                <stateOrCountry>FL</stateOrCountry>
                <stateOrCountryDescription>FLORIDA</stateOrCountryDescription>
                <zipCode>33028</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Other Health Care</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>Decline to Disclose</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06b</item>
        </federalExemptionsExclusions>
        <typeOfFiling>
            <newOrAmendment>
                <isAmendment>false</isAmendment>
            </newOrAmendment>
            <dateOfFirstSale>
                <value>2021-09-30</value>
            </dateOfFirstSale>
        </typeOfFiling>
        <durationOfOffering>
            <moreThanOneYear>true</moreThanOneYear>
        </durationOfOffering>
        <typesOfSecuritiesOffered>
            <isEquityType>true</isEquityType>
            <isOptionToAcquireType>true</isOptionToAcquireType>
        </typesOfSecuritiesOffered>
        <businessCombinationTransaction>
            <isBusinessCombinationTransaction>false</isBusinessCombinationTransaction>
            <clarificationOfResponse></clarificationOfResponse>
        </businessCombinationTransaction>
        <minimumInvestmentAccepted>0</minimumInvestmentAccepted>
        <salesCompensationList></salesCompensationList>
        <offeringSalesAmounts>
            <totalOfferingAmount>12085780</totalOfferingAmount>
            <totalAmountSold>6085780</totalAmountSold>
            <totalRemaining>6000000</totalRemaining>
```

### R0084 · preference_seniority · 932699_000093269916000092
**Question.** Classify multi-series preferred liquidation seniority as pari-passu or stacked (1.3.4).
**Field.** `preference_seniority` -- Whether preferred series rank equally (pari-passu) or in a seniority order (stacked).
**Answer.** one of: pari-passu, stacked, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/932699/000093269916000092/exhibit1092stockholerscons.htm

**Text shown to the model:**

```
w Securities to be an “Exempt Issuance” pursuant to the Series A Certificate, and (c) the Holders waive all adjustments to the Conversion Price (as such term is defined in the Series A Certificate), and all other antidilution protections set forth in the Series A Certificate with respect to the issuance of the New Securities.      2.    That, notwithstanding any provisions of the Series A Certificate to the contrary, all of which provisions are hereby waived, the Series D Preferred Stock, the Series D-2 Preferred Stock and the Series D-3 Preferred Stock shall rank senior to the Series A Preferred Stock in liquidation preference, and as otherwise stated in the Series D Certificate, the Series D-2 Certificate and the Series D-3 Certificate. Without limiting the generality of the foregoing, the Holders covenant and agree that, after the payment an amount equal to the Stated Value (as such term is defined in the Series A Certificate), plus any accrued and unpaid dividends thereon and any other fees then due and owing thereon under the Series A Certificate, for each share of Series A Preferred Stock, the remaining assets of the Company available for distribution
```

### R0085 · vesting_schedule · 0001104659-09-054183_a09-26145_18k
**Question.** Extract and normalize vesting schedule to canonical string format (6.1).
**Field.** `vesting_schedule` -- Normalized vesting schedule: e.g. '4yr/1yr-cliff', '3yr/no-cliff', '4yr/cliff'.
**Answer.** string value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
eleration of all of his outstanding stock options or restricted stock awards, and (iii) payments of premiums for continued health insurance coverage under COBRA for up to 12 months, all of which are subject to Mr. Martin’s execution of a binding release of claims.   If the Company terminates Mr. Martin without Cause or if Mr. Martin resigns with Good Reason not in connection with the Change of Control event,  then Mr. Martin will be entitled to: (i) a continuation of his base salary for a period of 12 months, (ii) waiver of one-year cliff vesting requirement for any options that have not reached the one-year vesting cliff date and a credit for vesting on his termination date equal to 1/48 th  of the option shares multiplied by each full month of his employment with the Company since the vesting commencement date of the option, and (iii) payments of premiums for continued health insurance coverage under COBRA for up to 12 months, all of which are subject to Mr. Martin’s execution of a binding release of claims.   CFO Agreement with Morgan Brown.   The CFO Agreement provides Mr. Brown with
```

### R0086 · safe_pre_post · 2084032_000121390026025748
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/2084032/000121390026025748/ea025686308ex10-2.htm

**Text shown to the model:**

```
EX-10.2 6 ea025686308ex10-2.htm FORM OF SAFE Exhibit 10.2   POST-MONEY VALUATION CAP   THIS INSTRUMENT AND ANY SECURITIES ISSUABLE PURSUANT HERETO HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE “ SECURITIES ACT ”), OR UNDER THE SECURITIES LAWS OF CERTAIN STATES. THESE SECURITIES MAY NOT BE OFFERED, SOLD OR OTHERWISE TRANSFERRED, PLEDGED OR HYPOTHECATED EXCEPT AS PERMITTED IN THIS SAFE AND UNDER THE ACT AND APPLICABLE STATE SECURITIES LAWS PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT OR AN EXEMPTION THEREFROM.   Salspera, INC.   SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by NAME ______________ (the “ Investor ”) of $XXXXX _________ (the “ Purchase Amount ”) on or about [ Date of Safe ], Salspera, Inc. a Delaware corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   This Safe is one of the forms available at http://ycombinator.com/documents and the Company and the Investor agree that neither one has modified the form, except to fill in blanks and bracketed terms.   The “ Post-Money Valuation Cap ” is $ 55 Million. See Section 2 for certain additional defined terms.   1. Events   (a) Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the greater of: (1) the number of shares of Standard Preferred Stock equal to the Purchase Amount divided by the lowest price per share of the Standard Preferred Stock; or (2) the number of shares of Saf
```

### R0087 · s1_use_of_proceeds · castlebio
**Question.** Extract the primary stated use of IPO proceeds from a real S-1/424B4 filing (7.3).
**Field.** `s1_use_of_proceeds` -- the primary stated use of proceeds, as an exact verbatim phrase copied from the text
**Answer.** string value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1447362/000114036120014751/nt10012655x7_424b4.htm

**Text shown to the model:**

```
an for the use of the net proceeds from this offering, or any significant portion thereof. However, we intend to use the net proceeds from this offering, together with our existing cash and cash equivalents, to further support and increase our research and development activities, including those to support the development of our product pipeline, to expand our commercial organization including our sales force and for working capital and other general corporate purposes. We may also use a portion of our net proceeds to co-develop, acquire or invest in products, technologies
```

### R0088 · information_rights · 0001628280-21-019876_exhibit102-sx1
**Question.** Classify whether a document grants investors a live financial-reporting/information right (5.3).
**Field.** `information_rights` -- yes if a live obligation to deliver financials to investors exists, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
EX-10.2 9 exhibit102-sx1.htm EX-10.2 Document Exhibit 10.2 AMENDMENT OF INVESTORS’ RIGHTS AGREEMENT This Amendment of Investors’ Rights Agreement (this “ Amendment ”) is made as of June 19, 2015 and amends the Investors’ Rights Agreement, dated January 30, 2015, among NerdWallet, Inc. (the “ Company ”) and the other parties thereto (the “ Agreement ”). Under Section 3.1(a) of the Agreement, the Company shall deliver to each Major Investor within one hundred twenty (120) days (the “ Delivery Period ”) after the end of each fiscal year of the Company: a balance sheet as of the end of such year; statements of income and of cash flows for such year; and a statement of stockholders’ equity as of the end of such year, all such financial statements audited and certified by independent public accountants of nationally recognized standing selected by the Company. Under Section 6.6 of the Agreement, any term of the Agreement may be amended with the written consent of the Compa
```

### R0089 · investor_ownership_pct · uber_alphabet_investor
**Question.** Compute a named institutional investor's ownership percentage from raw S-1 share counts (3.2.2).
**Field.** `investor_ownership_pct` -- the computed investor ownership percentage as a bare decimal (e.g., 16.3)
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1543151/000119312519103850/d647752ds1.htm

**Text shown to the model:**

```
From Uber Technologies, Inc.'s S-1 registration statement, "Security Ownership of Certain Beneficial Owners and Management" table, "5% Stockholders and Selling Stockholders" section (Shares Beneficially Owned Before the Offering):

Applicable percentage ownership before the offering is based on 1,362,500 thousand shares of common stock outstanding as of March 31, 2019.

Name of Beneficial Owner: Entities affiliated with Alphabet Inc.
Shares (in thousands): 71,097
```

### R0090 · s1_use_of_proceeds · veritone
**Question.** Extract the primary stated use of IPO proceeds from a real S-1/424B4 filing (7.3).
**Field.** `s1_use_of_proceeds` -- the primary stated use of proceeds, as an exact verbatim phrase copied from the text
**Answer.** string value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1615165/000119312518194741/d757366d424b4.htm

**Text shown to the model:**

```
JMP Securities. See &#147;Plan of Distribution&#148; on page 11 of this prospectus. Use of Proceeds We intend to use the net proceeds from this offering for working capital and general corporate purposes, including research and development expenses, sales and marketing expenses, general and administrative expenses and capital expenditures. See &#147;Use of Proceeds&#148; on page 8 of this prospectus. Risk Factors See &#147;Risk Factors&#148; beginning on page 6 of this prospectus and in the documen
```

### R0091 · flag_internal_inconsistency · castlebio_consistent
**Question.** Flag whether two real share-count citations in the same filing are numerically consistent (8.6).
**Field.** `flag_internal_inconsistency` -- true if the two cited share counts differ, false if they match
**Answer.** bool value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1447362/000114036120014751/nt10012655x7_424b4.htm

**Text shown to the model:**

```
Citation A (Capitalization table (actual column)): "17,203,496 shares issued and outstanding, actual"

Citation B (Dilution section basis statement): "is based on 17,203,496 shares of common stock outstanding as of March 31, 2020"
```

### R0092 · preference_seniority · 1585521_000119312519083351
**Question.** Classify multi-series preferred liquidation seniority as pari-passu or stacked (1.3.4).
**Field.** `preference_seniority` -- Whether preferred series rank equally (pari-passu) or in a seniority order (stacked).
**Answer.** one of: pari-passu, stacked, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1585521/000119312519083351/d642624dex31.htm

**Text shown to the model:**

```
the event that the assets legally available for distribution are insufficient to pay the holders of shares of the Series B Preferred Stock, the holders of shares of the Series C Preferred Stock and the holders of shares of the Series D Preferred Stock the amount to which they shall be entitled under this Subsection 3(a)(i) in full, then the full amount legally available for distribution to the holders of shares of the Series B Preferred Stock, the holders of shares of the Series C Preferred Stock and the holders of shares of the Series D Preferred Stock shall be distributed among them on a pro rata basis according to the respective amounts which would otherwise be payable upon such distribution if all amounts payable with respect to such shares were paid in full. (ii)    In the event of any liquidation, dissolution or winding up of the Corporation, either voluntary or involuntary, including any Liquidation Event (as defined below), (i) the holders of the Series A Preferred Stock shall be entitled to receive, out of the remaining assets of the Corporation legally available after the holders of the Series B Preferred Stock, the holders of the Series C Preferred Stock and
```

### R0093 · information_rights · 0001193125-11-204682_dex402
**Question.** Classify whether a document grants investors a live financial-reporting/information right (5.3).
**Field.** `information_rights` -- yes if a live obligation to deliver financials to investors exists, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
h Purchaser’s knowledge of a Founder’s or selling Purchaser’s violation of the co-sale rights hereunder.   20 3.7 Termination . The right of first refusal and co-sale rights, each with respect to sales by Founders or Purchasers, set forth in this Section 3 shall terminate upon the earlier of (a) the effective date of the Company’s IPO, (b) the closing date of an Acquisition or (c) fifteen years from the date hereof. 4. Information Rights . 4.1 Annual Financial Information . The Company shall deliver to each Holder of at least five percent (5%) of the Registrable Securities (each, an “ Information Rights Holder ”) within ninety (90) days after the end of each fiscal year, income, stockholders’ equity and cash flow statements of the Company for such year, and a balance sheet of the Company as of the end of such year, such year-end financial reports to be in reasonable detail, prepared in accordance with generally accepted accounting principles (“ GAAP ”), and certified by independent public accountants of national standing selected by the Company’s Board of Directors. 4.2 Quarterly Financial Information . The Company shall deliver to each Information Rights Holder within forty-five (45) days after the end of each quarter (except the last quarter of the fiscal year), an unaudited quarterly report including a balance sheet,
```

### R0094 · cliff_present · 0001451809-24-000052_ex1034offerofemployment-sa
**Question.** Classify whether a vesting schedule includes a cliff blockage period (6.2).
**Field.** `cliff_present` -- yes if the schedule has a cliff blockage period, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
(the "MegaChips Option"). The MegaChips Option will be granted under the MegaChips Equity Plan (the "MegaChips Equity Plan") and will be governed by and subject to the terms and conditions of the MegaChips Equity Plan and the applicable stock option grant notice and option agreement thereunder ("Option Documents"). Subject to applicable laws, the MegaChips Option will be subject to a four-year vesting schedule with no cliff, provided that you are continuously employed with the Company and/or MegaChips on each applicable vesting date. The Company plans to adopt a profit sharing plan for 2017 and 2018. If you are an employee in good standing at the time it is adopted and otherwise meet the eligibility criteria for participation in the plan at such time, you will be eligible to participate in such plan. Based on current projections, which may change based on business operating results in the future, it is expected that your interest in such plan would be 3%. The Company may change such percentage in its discretion. Further details regarding this plan will be communicated to you at a later date. Your employment is contingent upon completion of your 1-9 form and on providing SiTime with the appropriate documentation to establish your identity and authorization to legally work in the United States. Please bring
```

### R0095 · liquidation_preference_multiple · 1904616_000121390023031361
**Question.** Classify liquidation preference multiple (1x, 2x, 3x, other, non-participating) (leaf 1.3.1).
**Field.** `liquidation_preference_multiple` -- How many times the OIP the preferred holder receives upon liquidation.
**Answer.** one of: non-participating, 1x, 2x, 3x, other, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
on or winding up of the Corporation or any Deemed Liquidation Event (as defined below), before any payment shall be made to the holders of Common Stock by reason of their ownership thereof, the holders of shares of Series A Preferred Stock and Series B Preferred Stock then outstanding shall be entitled to be paid out of the funds and assets available for distribution to its stockholders, an amount per share equal to two (2) times the Original Issue Price (as defined below) for the Series A Preferred Stock or Series B Preferred Stock, as applicable, plus all cumulative and unpaid dividends (the " Liquidation Preference"). After the payment of the Liquidation Preference to the holders of the Series A Preferred Stock and holders of Series B Preferred Stock, the remaining assets shall be distributed ratably to the holders of the Common Stock. If upon any such liquidation, dissolution or winding up or Deemed Liquidation Event of the Corporation, the funds and assets available for distribution to the stockholders of the Corporation shall be insufficient to pay the holders of shares of Series A Preferred Stock and Series B Preferred Stock the full amount to which they are entitled under this Section 1.1, the holders of shares of Series A Preferred Stock and Series B Preferred Stock shall share ratably in any distribution of the funds and asset
```

### R0096 · round_size · 1436444
**Question.** Extract the total aggregate financing round size in dollars (1.2.1).
**Field.** `round_size` -- total aggregate dollar amount raised in the equity financing round
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1436444/000143644409000002/primary_doc.xml

**Text shown to the model:**

```
<entityName>TIGO ENERGY INC</entityName>
        <issuerAddress>
            <street1>170 KNOWLES DRIVE</street1>
            <street2></street2>
            <city>LOS GATOS</city>
            <stateOrCountry>CA</stateOrCountry>
            <zipCode>95032</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>408-364-0150</issuerPhoneNumber>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <jurisdictionOfInc>CALIFORNIA</jurisdictionOfInc>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <withinFiveYears>true</withinFiveYears>
            <value>2007</value>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Ron</firstName>
                <middleName></middleName>
                <lastName>Hadar</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>170 Knowles Drive</street1>
                <street2></street2>
                <city>Los Gatos</city>
                <stateOrCountry>CA</stateOrCountry>
                <zipCode>95032</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Shmuel</firstName>
                <middleName></middleName>
                <lastName>Arditi</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>170 Knowles Drive</street1>
                <street2></street2>
                <city>Los Gatos</city>
                <stateOrCountry>CA</stateOrCountry>
                <zipCode>95032</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Shirish</firstName>
                <middleName></middleName>
                <lastName>Sathaye</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>2500 Sand Hill Road</street1>
                <street2>Suite 200</street2>
                <city>Menlo Park</city>
                <stateOrCountry>CA</stateOrCountry>
                <zipCode>94025</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>John</firstName>
                <middleName></middleName>
                <lastName>Hull</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>5550 SW Macadam Ave.</street1>
                <street2>Suite 300</street2>
                <city>Portland</city>
                <stateOrCountry>OR</stateOrCountry>
                <zipCode>97239</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Other Technology</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>No Revenues</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06</item>
        </federalExemptionsExclusions>
        <typeOfFiling>
            <newOrAmendment>
                <isAmendment>true</isAmendment>
                <previousAccessionNumber>9999999997-08-026469</previousAccessionNumber>
            </newOrAmendment>
            <dateOfFirstSale>
                <value>2008-05-14</value>
            </dateOfFirstSale>
        </typeOfFiling>
        <durationOfOffering>
            <moreThanOneYear>false</moreThanOneYear>
        </durationOfOffering>
        <typesOfSecuritiesOffered>
            <isEquityType>true</isEquityType>
            <isOptionToAcquireType>true</isOptionToAcquireType>
            <isSecurityToBeAcquiredType>true</isSecurityToBeAcquiredType>
            <isOtherType>true</isOtherType>
            <descriptionOfOtherType>Series A Preferred Stock; Warrant for Series A Preferred Stock; Common Stock on Conversion of Series A Preferred Stock</descriptionOfOtherType>
        </typesOfSecuritiesOffered>
        <businessCombinationTransaction>
            <isBusinessCombinationTransaction>false</isBusinessCombinationTransaction>
            <clarificationOfResponse></clarificationOfResponse>
        </businessCombinationTransaction>
        <minimumInvestmentAccepted>6600</minimumInvestmentAccepted>
        <salesCompensationList></salesCompensationList>
        <offeringSalesAmounts>
            <totalOfferingAmount>7661116</totalOfferingAmount>
            <totalAmountSold>7661116</totalAmountSold>
            <totalRemaining>0</totalRemaining>
```

### R0097 · information_rights · 0001193125-06-212415_dex991
**Question.** Classify whether a document grants investors a live financial-reporting/information right (5.3).
**Field.** `information_rights` -- yes if a live obligation to deliver financials to investors exists, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
EX-99.1 2 dex991.htm FORM OF RESTRICTED STOCK AGREEMENT Form of Restricted Stock Agreement Exhibit 99.1 SPEEDWAY MOTORSPORTS, INC. 2004 STOCK INCENTIVE PLAN RESTRICTED STOCK AGREEMENT This Restricted Stock Agreement is entered into as of < Date Granted> between SPEEDWAY MOTORSPORTS, INC., a Delaware corporation (the “Company”), and <Name> (the “Recipient”). WHEREAS , the Company has established the Speedway Motorsports, Inc. 2004 Stock Incentive Plan (the “Plan”), pursuant to which the Company may, from time to time, make grants of restricted shares of the Company’s Common Stock, par value $.01 per share (the “Common Stock”), to eligible employees and other individuals providing services to the Company and its Subsidiaries (as defined in the Plan); and WHEREAS , in consideration for the Recipient’s service to the Company and/or its Subsidiaries, the Company has determined to grant the Recipient restricted shares of the Company’s Common Stock
```

### R0098 · safe_pre_post · 2010788_000149315224005725
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/2010788/000149315224005725/ex4-2.htm

**Text shown to the model:**

```
EX-4.2 5 ex4-2.htm   Exhibit 4.2   THIS INSTRUMENT AND ANY SECURITIES ISSUABLE PURSUANT HERETO HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE “ SECURITIES ACT ”), OR UNDER THE SECURITIES LAWS OF CERTAIN STATES. THESE SECURITIES MAY NOT BE OFFERED, SOLD OR OTHERWISE TRANSFERRED, PLEDGED OR HYPOTHECATED EXCEPT AS PERMITTED IN THIS SAFE AND UNDER THE ACT AND APPLICABLE STATE SECURITIES LAWS PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT OR AN EXEMPTION THEREFROM.   SAFE No. 2023-01   INVIZYNE TECHNOLOGIES, INC.   SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the investment by ____ (the “ Investor ”) of $800,000 (the “ Purchase Amount ”) as of ___, 2023, Invizyne Technologies, Inc., a Nevada corporation (the “ Company ”), issues to the Investor the right to certain equity securities of the Company, subject to the terms and conditions described below.   The “ Pre-Money Valuation Cap ” is one-hundred million dollars ($100,000,000.00)   The “ Discount Rate ” is 80.00%.   See Section 2 for certain additional defined terms.   1. Events   (a) Equity Financing . If there is and upon the first Equity Financing after the making of this SAFE and before the termination of this SAFE, on the initial closing of such Equity Financing, this SAFE will automatically convert into the number of Next Round Equity equal to the Purchase Amount divided by the Conversion Price.   In connection with the automatic conversion of this SAFE into Next Round Equity pursuant to this Section 1(a), the Investor will agree to and execute and deliver to the Company all the transaction documents related to the Equity Financing; provided, that such documents (i) are the same documents to be entered into with the purchasers of Next Round Equity, with appropriate variations to the extent required by this SAFE, and (ii) have customary exceptions to any drag-along applicable to the Investor, including (without limitation) limited representations, warranties, liability and indemnification obligations of or by the Investor.   (b) Liquidity Event . If there is a Liquidity Event before the termination of this SAFE, this SAFE will automatically be entitled (subject to the liquidation priority set forth in Section 1(d) below) to receive a portion of the Proceeds, due and payable to the Investor immediately prior to, or concurrent with, the consummation of such Liquidity Event, equal to the Purchase Amount.   (c) Dissolution Event . If there is a Dissolution Event before the t
```

### R0099 · board_seats_investor · 0000950134-07-010103_d46152e8vk_mdp
**Question.** Extract the number of board seats an investor has the right to designate (5.1).
**Field.** `board_seats_investor` -- the number of board seats the investor/investor class may designate
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
holders agreement, we entered into a director nomination agreement with certain of our investors. The director nomination agreement became effective on April 27, 2007 upon the completion of the initial public offering and gives certain investors that are party thereto the right to designate certain nominees for election to our Board of Directors. In particular, an affiliate of Madison Dearborn Partners, LLC, or MDP, will have the right to designate up to five nominees for election to our Board of Directors, the Mitchell investors will have the right to designate two nominees for election to our Board of Directors, Quadrangle Capital Partners LP, or Quadrangle, will have the right to designate one nominee for election to our Board of Directors and Syufy Enterprises LP, or Syufy, will have the right to designate one nominee for election to our Board of Directors. The rights of a party to nominate directors terminates if such party no longer beneficially owns a specified percentage of our common stock although certain parties may continue to have certain board observer rights so long as such party continues to hold a minimum percentage of our common stock. Under the director nomination agreement, at least one nominee of the Mitchell investors, at least three nominees of MDP, and the nominee of Quadrangle is required to be an independent director so long
```

### R0100 · safe_pre_post · 1158780_000121390025023733
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1158780/000121390025023733/ea0234319-8k_pluriinc.htm

**Text shown to the model:**

```
n Shares on the Nasdaq Capital Market or the Tel Aviv Stock Exchange, subject to certain limitations and restrictions for a period commencing on the date of closing of the Kokomodo Transaction and ending on the earlier of (i) 36 months, (ii) the time when the Seller holder holds less than 10% of the outstanding shares of the Company or (iii) the occurrence of a breach of the Company’s commitment to register the Consideration Shares under the Securities Act of 1933, as amended (the “Securities Act”).   Additionally, the Share Purchase Agreement provides for a $1,500,000 breakup fee (the “Breakup Fee”), as a sole remedy (except for cases of fraud) in the event that the Kokomodo transaction under the Share Purchase Agreement is not consummated by May 23, 2025, as may be extended under certain terms by additional 90 days, but no later than July 23, 2025, for any reason other than due to certain defaults, breaches and/or the failure to perform certain undertakings by the Seller, as further described in the Share Purchase Agreement (provided that a termination notice and cure periods were provided in accordance with its terms thereof). The Breakup Fee shall be paid as follows: $1,000,000 shall be payable to Seller in consideration for the sale of the most senior class Company shares held by Seller, reflecting a valuation of $6,000,000; and $500,000 shall be invested in the Company by form of a Simple Agreement For Future Equity (“SAFE”), providing a 20% discount of the price per share set in connection with a trigger event for conversion of the SAFE into equity of Kokomodo and a pre-money valuation cap of $5,500,000 in connection with such conversion.   1     The closing of the Kokomodo Transaction is subject to, among other conditions, the completion of customary closing conditions, compliance with any regulatory and corporate approvals, including receipt of shareholder approval.   The securities issued with respect to the Kokomodo Transaction are exempt from the registration requirements of the Securities Act, pursuant to Section 4(a)(2) of the Securities Act and/or Rule 903 of Regulation S promulgated thereunder. The securities have not been registered under the Securities Act and may not be sold in the United States absent registration or an exemption from registration.   This Current Report on Form 8-K shall not constitute an offer to sell or the solicitation of an offer to buy nor shall there be any sale of these securities in any state or jurisdiction in which such offer, solicitation or sale would be unlawful prior to registration or qualification under the securities laws of any such state or jurisdiction.   The foregoing descriptions of the Share Purchase Agreement, Assignment Agreement and Leak-Out Agreement are qualified in their entirety by reference to the full text of the form of Share Purchase Agreement, form of Assignment Agreement and form of Leak-Out Agreement, copies of which are filed as 10.1, 10.2, and 99.1, respectively.   Item 3.02 Unregistered Sales of Equity Securities.   The response to this item is included in Item 1.01, Entry into a Material Definitive Agreement, and is incorporated herein in its entirety.   Item 9.01 F
```

### R0101 · preference_seniority · 745788_000114420408016648
**Question.** Classify multi-series preferred liquidation seniority as pari-passu or stacked (1.3.4).
**Field.** `preference_seniority` -- Whether preferred series rank equally (pari-passu) or in a seniority order (stacked).
**Answer.** one of: pari-passu, stacked, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/745788/000114420408016648/v107630_8k.htm

**Text shown to the model:**

```
ock (the “Certificate of Designation”), which became effective upon filing with the Secretary of State of Delaware on March 14, 2008. The following description of the Series A Stock and the Series B Stock is only a summary and is qualified in its entirety by the complete description of the terms set forth in the Certificate of Designation filed with this report as Exhibit 3.1 and incorporated herein by reference. Series A Convertible Preferred Stock   Liquidation Preference.   In the event of a liquidation, bankruptcy, dissolution or similar proceeding, the holders of the Series A Stock shall rank pari passu with the Series B Stock and shall receive an amount equal to 100% of the original offering price plus any accrued but unpaid dividends (the “Series A Liquidation Preference”). In the event that the Company is unable to lawfully pay the Series A Liquidation Preference and Series B Liquidation Preference (as defined below), the Series A Stock shall receive a pro rata share of the assets with the Series B Stock. After payment of the Series A Liquidation Preference and Series B Liquidation Preference, the Series A Stock shall then be entitled to receive their p
```

### R0102 · securities_exemption · 1597815
**Question.** Classify which Securities Act exemption a Form D filing claimed (7.1).
**Field.** `securities_exemption` -- The federal exemption claimed in the Form D filing.
**Answer.** one of: 506b, 506c, 504, reg-a, other, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1597815/000159781514000002/primary_doc.xml

**Text shown to the model:**

```
<entityName>Handybook, Inc.</entityName>
        <issuerAddress>
            <street1>350 SEVENTH AVENUE, SUITE 1604</street1>
            <city>NEW YORK</city>
            <stateOrCountry>NY</stateOrCountry>
            <stateOrCountryDescription>NEW YORK</stateOrCountryDescription>
            <zipCode>10001</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>(617) 910-4813</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <withinFiveYears>true</withinFiveYears>
            <value>2012</value>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Oisin</firstName>
                <lastName>Hanrahan</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>350 Seventh Avenue, Suite 1604</street1>
                <city>New York</city>
                <stateOrCountry>NY</stateOrCountry>
                <stateOrCountryDescription>NEW YORK</stateOrCountryDescription>
                <zipCode>10001</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Umang</firstName>
                <lastName>Dua</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>350 Seventh Avenue, Suite 1604</street1>
                <city>New York</city>
                <stateOrCountry>NY</stateOrCountry>
                <stateOrCountryDescription>NEW YORK</stateOrCountryDescription>
                <zipCode>10001</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Other Technology</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>Decline to Disclose</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06b</item>
        </federalExemptionsExclusions>
```

### R0103 · round_size · 1520726
**Question.** Extract the total aggregate financing round size in dollars (1.2.1).
**Field.** `round_size` -- total aggregate dollar amount raised in the equity financing round
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1520726/000152072613000001/primary_doc.xml

**Text shown to the model:**

```
<entityName>ShopTap, Inc.</entityName>
        <issuerAddress>
            <street1>49 Geary Street, Suite 238</street1>
            <city>SAN FRANCISCO</city>
            <stateOrCountry>CA</stateOrCountry>
            <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
            <zipCode>94108</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>650-766-2294</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <edgarPreviousNameList>
            <previousName>ShopTap.com</previousName>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <withinFiveYears>true</withinFiveYears>
            <value>2011</value>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Tim</firstName>
                <lastName>Weingarten</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>49 Geary Street, Suite 238</street1>
                <city>San Francisco</city>
                <stateOrCountry>CA</stateOrCountry>
                <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
                <zipCode>94108</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Pat</firstName>
                <lastName>McVeigh</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>44 Anderson Way</street1>
                <city>Menlo Park</city>
                <stateOrCountry>CA</stateOrCountry>
                <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
                <zipCode>94025</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Alex</firstName>
                <lastName>Gurevich</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>101 Spear Street, Suite 255</street1>
                <city>San Francisco</city>
                <stateOrCountry>CA</stateOrCountry>
                <stateOrCountryDescription>CALIFORNIA</stateOrCountryDescription>
                <zipCode>94105</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Other Technology</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>Decline to Disclose</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06b</item>
        </federalExemptionsExclusions>
        <typeOfFiling>
            <newOrAmendment>
                <isAmendment>true</isAmendment>
                <previousAccessionNumber>0001520726-11-000001</previousAccessionNumber>
            </newOrAmendment>
            <dateOfFirstSale>
                <value>2011-09-01</value>
            </dateOfFirstSale>
        </typeOfFiling>
        <durationOfOffering>
            <moreThanOneYear>true</moreThanOneYear>
        </durationOfOffering>
        <typesOfSecuritiesOffered>
            <isEquityType>true</isEquityType>
            <isDebtType>true</isDebtType>
            <isSecurityToBeAcquiredType>true</isSecurityToBeAcquiredType>
            <isOtherType>true</isOtherType>
            <descriptionOfOtherType>Sale of Series A Preferred Stock and conversion of convertible promissory notes into Series A Preferred Stock, and the underlying
Common Stock upon the conversion of Series A Preferred Stock.</descriptionOfOtherType>
        </typesOfSecuritiesOffered>
        <businessCombinationTransaction>
            <isBusinessCombinationTransaction>false</isBusinessCombinationTransaction>
            <clarificationOfResponse></clarificationOfResponse>
        </businessCombinationTransaction>
        <minimumInvestmentAccepted>0</minimumInvestmentAccepted>
        <salesCompensationList></salesCompensationList>
        <offeringSalesAmounts>
            <totalOfferingAmount>6000000</totalOfferingAmount>
            <totalAmountSold>5500000</totalAmountSold>
            <totalRemaining>500000</totalRemaining>
```

### R0104 · safe_valuation_cap · 1838987_000121390024014892_cap
**Question.** Extract the valuation cap from a SAFE agreement (2.1.1)
**Field.** `safe_valuation_cap` -- the valuation cap in dollars as a bare integer (no $ or commas)
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
S THAT in exchange for the payment by RODGERS FAMILY FREEDOM AND FREE MARKETS CHARITABLE TRUST (the “ Investor ”) of $_________________ (the “ Purchase Amount ”) on or about ___________________, and COMPLETE SOLARIA, INC., a Delaware corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   The “ Pre-Money Valuation Cap ” is $ 53,540,000.00 ($1.24/share) The “ Discount Rate ” is 80%. See Section 2 for certain additional defined terms. 1. Events   (a) Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the number of shares of Common Stock equal to the Purchase Amount divided by the Conversion Price.   In connection with the automatic conversion of this Safe into shares of Common Stock, the Investor will execute and deliver to the Company all of the transaction documents related to the Equity Financing; provided, that such documents (i) are the same documents to be entered into with the other purchasers of Common Stock, with appropriate variations for the Common Stock if applicable, and (ii) have customary exceptions to any drag-along applicable to the Investor, including (without limitation) limi
```

### R0105 · round_size · 1260990
**Question.** Extract the total aggregate financing round size in dollars (1.2.1).
**Field.** `round_size` -- total aggregate dollar amount raised in the equity financing round
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1260990/000157093414000003/primary_doc.xml

**Text shown to the model:**

```
<entityName>GTX INC /DE/</entityName>
        <issuerAddress>
            <street1>175 TOYOTA PLAZA</street1>
            <street2>7TH FLOOR</street2>
            <city>MEMPHIS</city>
            <stateOrCountry>TN</stateOrCountry>
            <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
            <zipCode>38103</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>901-523-9700</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <overFiveYears>true</overFiveYears>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Mitchell</firstName>
                <middleName>S.</middleName>
                <lastName>Steiner</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Marc</firstName>
                <middleName>S.</middleName>
                <lastName>Hanover</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>James</firstName>
                <middleName>T.</middleName>
                <lastName>Dalton</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Henry</firstName>
                <middleName>P.</middleName>
                <lastName>Doggrell</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>J.</firstName>
                <middleName>R.</middleName>
                <lastName>Hyde, III</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Kenneth</firstName>
                <middleName>S.</middleName>
                <lastName>Robinson</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>J.</firstName>
                <middleName>Kenneth</middleName>
                <lastName>Glass</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Michael</firstName>
                <middleName>G.</middleName>
                <lastName>Carter</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Barrington</firstName>
                <middleName>J.A.</middleName>
                <lastName>Furr</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Biotechnology</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>Decline to Disclose</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06b</item>
        </federalExemptionsExclusions>
        <typeOfFiling>
            <newOrAmendment>
                <isAmendment>true</isAmendment>
                <previousAccessionNumber>0001570934-14-000002</previousAccessionNumber>
            </newOrAmendment>
            <dateOfFirstSale>
                <value>2014-03-06</value>
            </dateOfFirstSale>
        </typeOfFiling>
        <durationOfOffering>
            <moreThanOneYear>false</moreThanOneYear>
        </durationOfOffering>
        <typesOfSecuritiesOffered>
            <isEquityType>true</isEquityType>
            <isOptionToAcquireType>true</isOptionToAcquireType>
            <isSecurityToBeAcquiredType>true</isSecurityToBeAcquiredType>
        </typesOfSecuritiesOffered>
        <businessCombinationTransaction>
            <isBusinessCombinationTransaction>false</isBusinessCombinationTransaction>
            <clarificationOfResponse></clarificationOfResponse>
        </businessCombinationTransaction>
        <minimumInvestmentAccepted>0</minimumInvestmentAccepted>
        <salesCompensationList></salesCompensationList>
        <offeringSalesAmounts>
            <totalOfferingAmount>21272455</totalOfferingAmount>
            <totalAmountSold>21272455</totalAmountSold>
            <totalRemaining>0</totalRemaining>
```

### R0106 · safe_valuation_cap · 1900520_000121390024095442_cap
**Question.** Extract the valuation cap from a SAFE agreement (2.1.1)
**Field.** `safe_valuation_cap` -- the valuation cap in dollars as a bare integer (no $ or commas)
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by [________] (the “ Investor ”) of $[________] (the “ Purchase Amount ”) on or about August 27, 2024, Lomond Therapeutics, Inc., a Delaware corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   The “ Post-Money Valuation Cap ” is $100,000,000. See Section 2 for certain additional defined terms.   The “ Discount Rate ” is 90%.   See Section 2 for certain additional defined terms.   1. Events   (a) Equity Financing(s) .   (i) If there is a Qualified Equity Financing before the termination of this Safe, on the initial closing of such Qualified Equity Financing, this Safe will automatically convert into the number of shares of Safe Capital Stock equal to the Purchase Amount divided by the Conversion Price.   (ii) If there is a Non-Qualified Equity Financing before the termination of this Safe, the Company shall provide 10 business days’ written notice (which may be via e-mail) to Investor prior to the initial closing of such Non-Qualified Equity Financing, and the Majority-in-Interest (as defined below) may, at their sole discretion by providing written notice (which may be via e-mail) to the Company within 5 business days’ of r
```

### R0107 · information_rights · 0000898173-20-000007_orly-20191231ex101926dba
**Question.** Classify whether a document grants investors a live financial-reporting/information right (5.3).
**Field.** `information_rights` -- yes if a live obligation to deliver financials to investors exists, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
EX-10.19 3 orly-20191231ex101926dba.htm FORM OF DIRECTOR RESTRICTED STOCK AGREEMENT orly_4Q2019_Ex10_19 Exhibit 10.19 – Form of Director Restricted Stock Agreement   O’REILLY AUTOMOTIVE, INC.   2017 INCENTIVE AWARD PLAN    DIRECTOR RESTRICTED STOCK AGREEMENT     This Restricted Stock Award Agreement (this “ Restricted Stock Agreement ”), dated as of [ ], 2020 (the “ Date of Grant ”), is made by and between O’Reilly Automotive, Inc., a Missouri corporation (the “ Company ”) and [              ] (the “ Director ”).  Capitalized terms not defined herein shall have the meaning ascribed to them in the O’Reilly Automotive, Inc. 2017 Incentive Award Plan (as amended from time to time, the “ Plan ”).  Where the context permits, references to the Company shall include any successor to the Company. 1. Grant of Restricted Stock .  The Company hereby grants to the Director ________ Shares (such Shares, the “ Restricted Stock ”), subject to all of the terms and conditions
```

### R0108 · convert_vs_preference_decision · example4_convert
**Question.** Decide convert-vs-take-preference in a real acquisition scenario (4.4).
**Field.** `convert_vs_preference_decision` -- whether the investor should convert to common or take their preference
**Answer.** one of: convert, take-preference, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1680084/000121390017000472/fc2016a1ex99i_snapwire.htm

**Text shown to the model:**

```
Investor has purchased an Agreement for Future Equity for $100,000. The Valuation Cap is $10,000,000. &#9679; Another entity proposes to acquire the company for cash consideration of $50,000,000. The company&rsquo;s fully-diluted outstanding capital stock immediately prior to the acquisition, including 1,500,000 outstanding options but excluding any unallocated shares in the option pool, is 11,500,000 shares. The investor can choose to have the Agreement for Future Equity purchase amount returned, or convert the Agreement for Future Equity into shares of common stock and receive the cash consideration with the other common stockholders. The Agreement for Future Equity would convert into 115,008 shares of common stock, based on the &ldquo;Liquidity Price&rdquo; of $0.8695 per share (the Liquidity Price is calculated by dividing 10,000,000 by 11,500,000). When the $50,000,000 deal consideration is allocated pro rata among all of the common stockholders, including the investor (and assuming the outstanding options are all exercised), the investor would receive approximately $495,074. Since this amount is considerably more than the $100,000 purchase amount,
```

### R0109 · safe_pre_post · 1486452_000168316824001414
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1486452/000168316824001414/maison_ex0612.htm

**Text shown to the model:**

```
EX1A-6 MAT CTRCT 6 maison_ex0612.htm SIMPLE AGREEMENT FOR FUTURE EQUITY ISSUED TO MAISON LUXE, INC. BY IMPOSSIBLE DIAMOND, INC. DATED APRIL 13, 2021, FOR $50,000 Exhibit 6.12   THIS INSTRUMENT AND ANY SECURITIES ISSUABLE PURSUANT HERETO HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE “ SECURITIES ACT ”), OR UNDER THE SECURITIES LAWS OF CERTAIN STATES. THESE SECURITIES MAY NOT BE OFFERED, SOLD OR OTHERWISE TRANSFERRED, PLEDGED OR HYPOTHECATED EXCEPT AS PERMITTED IN THIS SAFE AND UNDER THE ACT AND APPLICABLE STATE SECURITIES LAWS PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT OR AN EXEMPTION THEREFROM.   IMPOSSIBLE DIAMOND, INC.   SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by MAISON LUXE, INC. (the “ Investor ”) of $$50,000 (the “ Purchase Amount ”) on or about APRIL 13, 2021, Impossible Diamond, Inc., a Delaware benefit corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   This Safe is one of the forms available at http://ycombinator.com/documents and the Company and the Investor agree that neither one has modified the form, except to fill in blanks and bracketed terms.   The “ Post-Money Valuation Cap ” is $20,000,000.   The “ Discount Rate ” is 80%.   See Section 2 for certain additional defined terms. 1. Events   (a) Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the number of shares of Safe Preferred Stock equal to the Purchase Amount divided by the Conversion Price.   In connection with the automatic conversion of this Safe into shares of Safe Preferred Stock, the Investor will execute and deliver to the Company all of the transaction documents related to the Equity Financing; provided, that such documents (i) are the same documents to be entered into with the purchasers of Standard Preferred Stock, with appropriate variations for the Safe Preferred Stock if applicable, and (ii) have customary exceptions to any drag-along applicable to the Investor, including (without limitation) limited representations, warranties, liability and indemnification obligations for the Investor.   (b) Liquidity Event . If there is a Liquidity Event before the termination of this Safe, this Safe will automatically be entitled (subject to the liquidation priority set forth in Section 1(d) below) to receive a portion of Proceeds, due and payable to the Investor immediately prior to, or concurrent with, the consummation of such Liquidity Event, equal to the greater of (i) the Purchase Amount (the “ Cash-Out Amount ”) or (ii) the amount payable on the number of shares of Common Stock equal to the Purchase Amount divided by the Liquidity P
```

### R0110 · safe_cap_vs_discount_applies · maison_both_mfn
**Question.** Classify whether a SAFE uses cap, discount, or both-MFN for conversion pricing (2.1.3).
**Field.** `safe_cap_vs_discount_applies` -- Whether the SAFE's conversion price uses cap-only, discount-only, or both with MFN.
**Answer.** one of: cap, discount, both-mfn, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
ach case calculated on an as-converted to Common Stock basis):     • Includes all shares of Capital Stock issued and outstanding;   • Includes all Converting Securities;   • Includes all (i) issued and outstanding Options and (ii) Promised Options; and • Includes the Unissued Option Pool, except that any increase to the Unissued Option Pool in connection with the Equity Financing shall only be included to the extent that the number of Promised Options exceeds the Unissued Option Pool prior to such increase.   “ Conversion Price ” means the either: (1) the Safe Price or (2) the Discount Price, whichever calculation results in a greater number of shares of Safe Preferred Stock.   “ Converting Securities ” includes this Safe and other convertible securities issued by the Company, including but not limited to: (i) other Safes; (ii) convertible promissory notes and other convertible debt instruments; and (iii) convertible securities that have the right to convert into shares of Capital Stock.   “ Direct Listing ” means the Company’s initial listing of its Common Stock (other than shares of Common Stock not eligible for resale under Rule 144 under the Securities Act) on a national securities exchange by means of an effective registration statement on Form S-1 filed by the Company with the SEC that registers shares of existing capital stock of the Company for resale, as approved by the Company’s board of directors. For the avoidance of doubt, a Direct Listing shall not be deemed to be an underwritten offering and shall not involve any underwriting services.   “ Discount Price ” means the price per share of the Standard Preferred Stock sold in the Equity Financing multiplied by the Discount Rate.   “ Dissolution Event ” means (i) a voluntary termination of operations, (ii) a general assignment for the benefit of the Company’s creditors or (iii) any other liquidation, dissolution or winding up of the Company ( excluding a Liquidity Event), whether voluntary or involuntary.   “ Dividend Amount ” means, with respect to any date on whi
```

### R0111 · safe_pre_post · 746210_000143774926019366
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/746210/000143774926019366/ex_971836.htm

**Text shown to the model:**

```
EX-10.3 5 ex_971836.htm EXHIBIT 10.3 SIMPLE AGREEMENT FOR FUTURE EQUITY ex_971836.htm   EXHIBIT 10.3   THIS INSTRUMENT AND ANY SECURITIES ISSUABLE PURSUANT HERETO HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE “ SECURITIES ACT ”), OR UNDER THE SECURITIES LAWS OF CERTAIN STATES. THESE SECURITIES MAY NOT BE OFFERED, SOLD OR OTHERWISE TRANSFERRED, PLEDGED OR HYPOTHECATED EXCEPT AS PERMITTED IN THIS SAFE AND UNDER THE ACT AND APPLICABLE STATE SECURITIES LAWS PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT OR AN EXEMPTION THEREFROM.   MANAKO LABS LTD   SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by TAOWEAVE, INC. , a Delaware corporation, with its principal place of business at 110 16th Street, Suite 1400 #1024, Denver, CO 80202, United States (the “ Investor ”) of $1,000,000 (the “ Investment Amount ”) on or about the date of this Safe, MANAKO LABS LTD , a company incorporated in England and Wales with company number 17048521 and whose registered office is at 71-75 Shelton Street, Covent Garden, London, United Kingdom, WC2H 9JQ (the “ Company ”), grants the Investor the right to subscribe for certain shares in the capital of the Company, subject to the terms below.   The “ Post-Money Valuation Cap ” is $40,000,000.   The “ Discount Rate ” is 80% (representing a 20% discount to the price per share of the Senior Shares in the Equity Financing).   Condition to Effectiveness   This Safe is conditional on the concurrent execution and delivery by the Company and the Investor of the Technology License and Distribution Agreement dated on or about the date of this Safe (the "TLDA"). This Safe shall not take effect and the Investment Amount shall not be due and payable until the TLDA has been duly executed and delivered by both the Company and the Investor. If the TLDA has not been executed and delivered by both parties within five (5) days of the date of this Safe, either party may terminate this Safe by written notice to the other, whereupon this Safe shall be of no further force or effect and neither party shall have any further obligation to the other, save that the confidentiality obligations set out in the Side Letter shall survive such termination for a period of two (2) years.   See Section   2 for certain additional defined terms.   1.           Events   (a)          Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the number of Safe Shares equal to the Investment Amount divided by the Conversion Price, in each case rounded to the nearest whole share.   In connection with the automatic conversion of this Safe into Safe Shares the Investor will execute and deliver to the Company all of the transaction documents relat
```

### R0112 · safe_valuation_cap · 1486452_000168316824001414_cap
**Question.** Extract the valuation cap from a SAFE agreement (2.1.1)
**Field.** `safe_valuation_cap` -- the valuation cap in dollars as a bare integer (no $ or commas)
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
ond, Inc., a Delaware benefit corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   This Safe is one of the forms available at http://ycombinator.com/documents and the Company and the Investor agree that neither one has modified the form, except to fill in blanks and bracketed terms.   The “ Post-Money Valuation Cap ” is $20,000,000.   The “ Discount Rate ” is 80%.   See Section 2 for certain additional defined terms. 1. Events   (a) Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the number of shares of Safe Preferred Stock equal to the Purchase Amount divided by the Conversion Price.   In connection with the automatic conversion of this Safe into shares of Safe Preferred Stock, the Investor will execute and deliver to the Company all of the transaction documents related to the Equity Financing; provided, that such documents (i) are the same documents to be entered into with the purchasers of Standard Preferred Stock, with appropriate variations for the Safe Preferred Stock if applicable, and (ii) have customary exceptions to any drag-along applicable to the Investor, including (withou
```

### R0113 · vesting_schedule · 1293310_000119312512306440
**Question.** Extract and normalize vesting schedule to canonical string format (6.1).
**Field.** `vesting_schedule` -- Normalized vesting schedule: e.g. '4yr/1yr-cliff', '3yr/no-cliff', '4yr/cliff'.
**Answer.** string value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
scribed herein (“Previous Double Trigger Acceleration”), the vesting acceleration described in this letter agreement will supersede and replace in its entirety any such Previous Double Trigger Acceleration. In the event that an option granted to you under the Plan has vesting acceleration that is not triggered by a Double Trigger, such vesting acceleration remains in full force and effect. Example of Double Trigger Acceleration : You have an option for 10,000 shares of the Company’s Common Stock. This option has a four-year vesting schedule, with a 12-month cliff, so that 25% of the shares become vested upon your completion of 12 months of service from the vesting commencement date of the option, and 1/48 th of the shares become vested upon your completion of each month of service thereafter. The Double Trigger occurs when you have completed ten months of service from this option’s vesting commencement date. In accordance with this Section 1, to calculate the vesting acceleration, pursuant to Section 1(a), you must first receive monthly vesting credit to become vested in 10/48 th of 10,000 shares or 2,083 shares
```

### R0114 · cliff_present · 0001503707-23-000002_ltipformfinalforedgar
**Question.** Classify whether a vesting schedule includes a cliff blockage period (6.2).
**Field.** `cliff_present` -- yes if the schedule has a cliff blockage period, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
rein and not otherwise defined will have the meanings assigned to such terms in the Plan. Unless vesting is accelerated in the discretion of the Board, and subject to the treatment described in the Terms and Conditions in the event of certain terminations of Grantee’s employment or engagement or a Change in Control, the Award will vest and be paid in cash, subject to required withholdings, on December 31, 2025 (the “Cliff Vesting Date”), provided that Grantee is still employed or engaged by the Company on such date. Twenty-five percent (25%) of the Award will be a “Retentive Award,” which will vest on the Vesting Date, without regard to achievement of the Performance Goal, based on Grantee’s continuous employment or engagement by the Company through the Vesting Date. The remaining seventy-five percent (75%) of the Award will be a “Performance-Based Award,” which will vest on the Vesting Date if and to the extent the Performance Goal is achieved, and based on Grantee’s continuous employment or engagement by the Company through the Vesting Date. (Signatures Follow) IN WITNESS WHEREOF , NorthStar Healthcare Income, Inc., acting by and through its duly authorized officers, and Grantee have caused this Award Agreement to be executed as of the Grant Date. This Award Agreement may be executed in two or more counterparts, ea
```

### R0115 · safe_valuation_cap · 2036444_000121390025123767_cap
**Question.** Extract the valuation cap from a SAFE agreement (2.1.1)
**Field.** `safe_valuation_cap` -- the valuation cap in dollars as a bare integer (no $ or commas)
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
FE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by Yek Tiew Ming (the “ Investor ”) of SGD50,000 dollar (the “ Purchase Amount ”) on or about 12 Jun 2024, NEO AERONAUTICS PTE LTD, a Singapore corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Share, subject to the terms described below.   The “ Pre-Money Valuation Cap ” is USD$30,000,000 dollar.   The “ Discount Rate ” is 50%.   See Section 2 for certain additional defined terms.   1. Events   (a)  Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the number of shares of Safe Share equal to the Purchase Amount divided by the Conversion Price.   In connection with the automatic conversion of this Safe into shares of Safe Share, the Investor will execute and deliver to the Company all of the transaction documents related to the Equity Financing; provided, that such documents (i) are the same documents to be entered into with the purchasers of Standard Share, with appropriate variations for the Safe Share if applicable, and (ii) have customary exceptions to any drag-along applicable to the Investor, including (without limitation) limited represen
```

### R0116 · cliff_present · 0000790816-14-000054_bdn8k-annualawards_031414
**Question.** Classify whether a vesting schedule includes a cliff blockage period (6.2).
**Field.** `cliff_present` -- yes if the schedule has a cliff blockage period, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
m of a $250,000 cash payment and 24,424 time-vested restricted shares. Annual Incentive Awards The table below sets forth the annual incentives, which are payable in cash, awarded to each of the following executives: Name Annual Incentive Gerard H. Sweeney $1,200,000 H. Jeffrey DeVuono $323,000 George D. Johnstone $244,000 Brad A. Molotsky $271,000 Thomas E. Wirth $264,000 Long-Term Equity Awards: Performance Units; Cliff-Vesting Restricted Shares The table below sets forth the equity-based long-term incentives awarded to each of the following executives. Two-thirds of these awards (by value) were in the form of restricted performance share units (“Performance Units”) and one-third of these awards (by value) were in the form of time-vested restricted common shares (“Cliff-Vesting Restricted Shares”) as indicated in the table below. Name Performance Units (#) Cliff-Vesting Restricted Shares (#) Gerard H. Sweeney 61,720 41,452 H. Jeffrey DeVuono 17,873 12,004 George D. Johnstone 13,115 8,808 Brad A. Molotsky 18,002 12,090 Thomas E. Wirth 16,525 11,099 2 Performance Units . Performance units represent the right to earn common shares. The number of common shares, if any, deliverable to award recipients depends on our performance based on our total return to shareholders during the three-year period Measurement Period that commenced o
```

### R0117 · safe_pre_post · 2036444_000121390025123767
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/2036444/000121390025123767/ea026659901ex10-4_neo.htm

**Text shown to the model:**

```
EX-10.4 8 ea026659901ex10-4_neo.htm SAFE AGREEMENT ENTERED BY AND BETWEEN NEO AERONAUTICS PTE LTD AND YEK TIEW MING DATED JUNE 12, 2024 Exhibit 10.4   NEO AERONAUTICS PTE LTD UEN 201811847K   THIS INSTRUMENT AND ANY SECURITIES ISSUABLE PURSUANT HERETO HAVE NOT BEEN REGISTERED UNDER THE SECURITIES LAW OF ANY COUNTRY. THESE SECURITIES MAY NOT BE OFFERED, SOLD OR OTHERWISE TRANSFERRED, PLEDGED OR HYPOTHECATED EXCEPT AS PERMITTED IN THIS SAFE AND UNDER SECURITIES LAWS IN THE COUNTRY IN WHICH SUCH TREATMENT IS BEING COMTEMPLATED   SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by Yek Tiew Ming (the “ Investor ”) of SGD50,000 dollar (the “ Purchase Amount ”) on or about 12 Jun 2024, NEO AERONAUTICS PTE LTD, a Singapore corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Share, subject to the terms described below.   The “ Pre-Money Valuation Cap ” is USD$30,000,000 dollar.   The “ Discount Rate ” is 50%.   See Section 2 for certain additional defined terms.   1. Events   (a)  Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the number of shares of Safe Share equal to the Purchase Amount divided by the Conversion Price.   In connection with the automatic conversion of this Safe into shares of Safe Share, the Investor will execute and deliver to the Company all of the transaction documents related to the Equity Financing; provided, that such documents (i) are the same documents to be entered into with the purchasers of Standard Share, with appropriate variations for the Safe Share if applicable, and (ii) have customary exceptions to any drag-along applicable to the Investor, including (without limitation) limited representations, warranties, liability and indemnification obligations for the Investor.   (b)  Liquidity Event . If there is a Liquidity Event before the termination of this Safe, this Safe will automatically be entitled (subject to the liquidation priority set forth in Section 1(d) below) to receive a portion of Proceeds, due and payable to the Investor immediately prior to, or concurrent with, the consummation of such Liquidity Event, equal to the greater of (i) the Purchase Amount (the “ Cash-Out Amount ”) or (ii) the amount payable on the number of shares of Ordinary Share equal to the Purchase Amount divided by the Liquidity Price (the “ Conversion Am
```

### R0118 · information_rights · 0000945841-07-000055_restrstockagreement
**Question.** Classify whether a document grants investors a live financial-reporting/information right (5.3).
**Field.** `information_rights` -- yes if a live obligation to deliver financials to investors exists, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
EX-10.3 5 restrstockagreement.htm FORM OF RESTRICTED STOCK AGREEMENT 2007 Form of Restricted Stock Agreement 2007 EXHIBIT 10.3   RESTRICTED STOCK AGREEMENT   (PURSUANT TO THE TERMS OF THE   POOL CORPORATION   2007 LONG-TERM INCENTIVE PLAN)     This RESTRICTED STOCK AGREEMENT (this "Restricted Stock Agreement") is between Pool Corporation, a Delaware corporation ("Company"), and _____________("Recipient"), and is dated as of the date set forth immediately above the signatures below.   1.   Grant of Restricted Stock . The Company hereby grants to Recipient all rights, title and interest in the record and beneficial ownership of ________ shares (the "Restricted Stock" or the “Incentive”) of common stock, $.001 par value per share, of Company ("Common Stock") subject to the conditions described in Paragraphs 4 and 5 as well as the other provisions of this Restricted Stock Agreement. The Restricted Stock is granted pursuant to and to implement in part Pool Co
```

### R0119 · preference_stack_payout · series_a
**Question.** Compute a named preferred series' total payout (preference + accrued dividends) (4.3).
**Field.** `preference_stack_payout` -- target series' liquidation preference plus accrued dividends, in $ millions
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1211759/000119312518039721/d516937dex99c3.htm

**Text shown to the model:**

```
TARGET SERIES: Series A Preferred Stock

Total Projected Preferred Stock as of 12/31/17: $(78.6) million, consisting of: Series A Preferred Stock liquidation preference of $52.0 million plus projected accrued dividends as of 12/31/17 of $6.9 million; and Series B Preferred Stock liquidation preference of $17.5 million plus projected accrued dividends as of 12/31/17 of $2.2 million.
```

### R0120 · s1_use_of_proceeds · axcella
**Question.** Extract the primary stated use of IPO proceeds from a real S-1/424B4 filing (7.3).
**Field.** `s1_use_of_proceeds` -- the primary stated use of proceeds, as an exact verbatim phrase copied from the text
**Answer.** string value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1633070/000104746920003070/a2241647z424b4.htm

**Text shown to the model:**

```
ter deducting underwriting discounts and commissions and estimated offering expenses payable by us. We intend to use the net proceeds from this offering, together with our existing cash and cash equivalents, to advance our current liver programs, including our planned IND filing for AXA1665 and ensuing initiation of a Clinical Trial and our planned IND filing for AXA1125 in adults and pediatric patients and ensuing initiation of Clinical Trials; to advance our product candidate AXA4010, including the conclusion of our ongoing Clinical Stud
```

### R0121 · information_rights · 0001193125-15-060049_d836724dex1031
**Question.** Classify whether a document grants investors a live financial-reporting/information right (5.3).
**Field.** `information_rights` -- yes if a live obligation to deliver financials to investors exists, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
EX-10.31 2 d836724dex1031.htm EX-10.31 EX-10.31 Exhibit 10.31 HURON CONSULTING GROUP INC. 2012 OMNIBUS INCENTIVE PLAN RESTRICTED STOCK AGREEMENT This RESTRICTED STOCK AGREEMENT (this “ Restricted Stock Agreement ”) is made and entered into as of                     , 20        (the “ Date of Grant ”), by and between Huron Consulting Group Inc., a Delaware corporation (“ Huron ”), and you (the “ Recipient ”). BY ACCEPTING THE TERMS AND CONDITIONS OF THIS RESTRICTED STOCK AGREEMENT BELOW, YOU ARE ALSO GRANTING TO HURON AN IRREVOCABLE PROXY TO VOTE THE SHARES OF RESTRICTED STOCK UNTIL THEY VEST. FOR MORE INFORMATION SEE SECTION 6 AND THE IRREVOCABLE PROXY BELOW. WHEREAS, pursuant to Huron’s Stock Ownership Participation Program (the “ Program ”) which is operated under the Huron Consulting Group Inc. 2012 Omnibus Incentive Plan (the “ Plan ”), the Recipient elected to purchase shares of Common Stock (the “ Acquisition Shares ”) and to receive in accordance with the Program a grant of Restricted Stock (as defined below) in a number
```

### R0122 · safe_pre_post · 1900520_000121390024095442
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1900520/000121390024095442/ea021976201ex4-2_lomond.htm

**Text shown to the model:**

```
EX-4.2 7 ea021976201ex4-2_lomond.htm FORM OF SIMPLE AGREEMENT FOR FUTURE EQUITY, DATED AUGUST 27, 2024 Exhibit 4.2   THIS INSTRUMENT AND ANY SECURITIES ISSUABLE PURSUANT HERETO HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE “ SECURITIES ACT ”), OR UNDER THE SECURITIES LAWS OF CERTAIN STATES. THESE SECURITIES MAY NOT BE OFFERED, SOLD OR OTHERWISE TRANSFERRED, PLEDGED OR HYPOTHECATED EXCEPT AS PERMITTED IN THIS SAFE AND UNDER THE ACT AND APPLICABLE STATE SECURITIES LAWS PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT OR AN EXEMPTION THEREFROM.   LOMOND THERAPEUTICS, INC. SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by [________] (the “ Investor ”) of $[________] (the “ Purchase Amount ”) on or about August 27, 2024, Lomond Therapeutics, Inc., a Delaware corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   The “ Post-Money Valuation Cap ” is $100,000,000. See Section 2 for certain additional defined terms.   The “ Discount Rate ” is 90%.   See Section 2 for certain additional defined terms.   1. Events   (a) Equity Financing(s) .   (i) If there is a Qualified Equity Financing before the termination of this Safe, on the initial closing of such Qualified Equity Financing, this Safe will automatically convert into the number of shares of Safe Capital Stock equal to the Purchase Amount divided by the Conversion Price.   (ii) If there is a Non-Qualified Equity Financing before the termination of this Safe, the Company shall provide 10 business days’ written notice (which may be via e-mail) to Investor prior to the initial closing of such Non-Qualified Equity Financing, and the Majority-in-Interest (as defined below) may, at their sole discretion by providing written notice (which may be via e-mail) to the Company within 5 business days’ of receipt of the Company’s notice, elect to convert the Purchase Amounts of all then-outstanding Safes with the same “Post-Money Valuation Cap” as this Safe into the number of shares of Safe Capital Stock equal to the Purchase Amount divided the Conversion Price.   In connection with the automatic conversion of this Safe into shares of Safe Capital Stock, the Investor will execute and deliver to the Company all of the transaction documents related to the Equity Financing; provided, that such documents (i) are the same documents to be entered into with the purchasers of such Capital Stock, with appropriate variations for the Safe Capital Stock, if applic
```

### R0123 · safe_cap_vs_discount_applies · gardedam_cap_only
**Question.** Classify whether a SAFE uses cap, discount, or both-MFN for conversion pricing (2.1.3).
**Field.** `safe_cap_vs_discount_applies` -- Whether the SAFE's conversion price uses cap-only, discount-only, or both with MFN.
**Answer.** one of: cap, discount, both-mfn, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
Delaware corporation (the “ Company ”), hereby issues to the Investor the right to certain shares of the Company’s capital stock, subject to the terms set forth below.
 
The “ Valuation Cap ” is $4,000,000.  See Section 2 for certain additional defined terms.
 
1.       Events
 
(a)       Equity Financing . If there is an Equity Financing or before the expiration or termination of this instrument, the Company will automatically issue to the Investor a number of shares of Common Stock in the resulting legal entity equal to the Purchase Amount divided by the price per share of the Common Stock, if the pre-money valuation is less than or equal to the Valuation Cap.
 
In connection with the issuance of Common Stock by the Company to the Investor pursuant to this Section 1(a):
 
(i)      The Investor will execute and deliver to the Company all transaction documents related to the Equity Financing; provided, that such documents are the same documents to be entered into with the purchasers of Common Stock, and provided further, that such documents have customary exceptions to any drag-along applicable to the Investor, including, without limitation, limited representations and warranties and limited liability and indemnification obligations on the part of the Investor; and
 
(ii)      The Investor and the Company will execute a Pro Rata Rights Agreement, unless the Investor is already included in such rights in the transaction documents related to the Equity Financing.
 
(b)       Merger . If there is an Merger, comprising either a Reverse Takeover or an IPO, or before the expiration or termination of this instrument, the Company will automatically issue to the Investor a number of shares of Common Stock of the merged or public entity equal to the Purchase Amount divided by the price per share of the Common Stock, if the pre-money valuation is less than or equal to the Valuation Cap.
 
(c)       Liquidity Event .  If there is a Liquidity Event before the expiration or termination of this instrument, the Investor will, at its option, either (
```

### R0124 · cliff_present · 0001299933-11-000951_htm_41195
**Question.** Classify whether a vesting schedule includes a cliff blockage period (6.2).
**Field.** `cliff_present` -- yes if the schedule has a cliff blockage period, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
ications pursuant to Rule 13e-4(c) under the Exchange Act (17 CFR 240.13e-4(c)) Top of the Form Item 5.02 Departure of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers. On March 23, 2011, the Human Resources Committee of the Board of Directors of Viad Corp (the "Company") modified the form of the Restricted Stock Agreement (five-year cliff vesting) for executives, the Restricted Stock Agreement (three-year cliff vesting) for executives, the Restricted Stock Units Agreement, and the Performance Unit Agreement, pursuant to the 2007 Viad Corp Omnibus Incentive Plan. The modification provided that upon termination of employment, the executive will forfeit vesting of the stock or units, as the case may be, if the executive does not sign the Company’s separation and release agreement, upon the Company’s request. A copy of the form of the Restricted Stock Agreement (five-year cliff vesting) for executives, the Restricted Stock Agreement (three-year cliff vesting) for executives, the Restricted Stock Units Agreement and the Performance Unit Agreement, effective as of March 23, 2011, are attached hereto as Exhibits 10.A, 10.B, 10.C and 10.D, respectively, and are incorporated herein by reference. Item 9.01 Financial Statements and Exhibits. (d) Exhibits
```

### R0125 · fully_diluted_basis · ignentertainment_body
**Question.** Classify capitalization definition as fully-diluted or issued-outstanding basis (3.4).
**Field.** `fully_diluted_basis` -- Whether cap is computed on fully-diluted or issued-outstanding basis.
**Answer.** one of: fully-diluted, issued-outstanding, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1101547/000104746905019338/a2158851zs-1.htm

**Text shown to the model:**

```
615 &#151; Stockholders' equity: Preferred stock, $0.0001 par value per share (assuming this offering is completed on September 30, 2005): 40,000,000 shares authorized; and 5,000,000 shares, as adjusted &#151; &#151; Common stock, $0.0001 par value: 28,000,000 shares authorized and 20,392,610 shares issued and outstanding, actual; and 100,000,000 shares authorized and shares issued and outstanding, as adjusted 12 Additional paid-in capital 30,464 Deferred stock-based compensation (5,211 ) Accumulated other comprehensive loss (24 ) Accumulated deficit (23,262 ) Total stockhol
```

### R0126 · safe_pre_post · 1386049_000109690621002893
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1386049/000109690621002893/byoc_ex10z1.htm

**Text shown to the model:**

```
EX-10.1 2 byoc_ex10z1.htm SIMPLE AGREEMENT FOR FUTURE EQUITY BETWEEN THE COMPANY AND CITYFREIGHTER, INC., DATED NOVEMBER 18, 2021, IN THE PRINCIPAL AMOUNT OF $250,000 SAFE Beyond Commerce Exhibit 10.1   POST-MONEY VALUATION CAP   THIS INSTRUMENT AND ANY SECURITIES ISSUABLE PURSUANT HERETO HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE “ SECURITIES ACT ”), OR UNDER THE SECURITIES LAWS OF CERTAIN STATES. THESE SECURITIES MAY NOT BE OFFERED, SOLD OR OTHERWISE TRANSFERRED, PLEDGED OR HYPOTHECATED EXCEPT AS PERMITTED IN THIS SAFE AND UNDER THE ACT AND APPLICABLE STATE SECURITIES LAWS PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT OR AN EXEMPTION THEREFROM.   CITYFREIGHTER INC. SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by Beyond Commerce Inc. (the “ Investor ”) of $250,000 (the “ Purchase Amount ”), Cityfreighter Inc., a Delaware corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below. the 2GP Group LLC   This Safe is one of the forms available at http://ycombinator.com/documents and the Company and the Investor agree that neither one has modified the form, except to fill in blanks and bracketed terms.   The “ Post-Money Valuation Cap ” is $7,500,000. See Section 2 for certain additional defined terms.   1. Events     (a) Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the greater of: (1) the number of shares of Standard Preferred Stock equal to the Purchase Amount divided by the lowest price per share of the Standard Preferred Stock; or (2) the number of shares of Safe Preferred
```

### R0127 · cliff_present · 0001104659-09-054183_a09-26145_18k
**Question.** Classify whether a vesting schedule includes a cliff blockage period (6.2).
**Field.** `cliff_present` -- yes if the schedule has a cliff blockage period, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
premiums for continued health insurance coverage under COBRA for up to 12 months, all of which are subject to Mr. Martin’s execution of a binding release of claims.   If the Company terminates Mr. Martin without Cause or if Mr. Martin resigns with Good Reason not in connection with the Change of Control event,  then Mr. Martin will be entitled to: (i) a continuation of his base salary for a period of 12 months, (ii) waiver of one-year cliff vesting requirement for any options that have not reached the one-year vesting cliff date and a credit for vesting on his termination date equal to 1/48 th  of the option shares multiplied by each full month of his employment with the Company since the vesting commencement date of the option, and (iii) payments of premiums for continued health insurance coverage under COBRA for up to 12 months, all of which are subject to Mr. Martin’s execution of a binding release of claims.   CFO Agreement with Morgan Brown.   The CFO Agreement provides Mr. Brown with certain severance and change in control benefits.  If the Company terminates Mr. Brown without Cause or if Mr. Brown resigns with Good Reason immediately prior to or within 12 months following a Change of Control,  as those terms are defined in the CFO Agreement, then Mr. Brown will be entitled to: (i) a lump sum payment equal to nine mo
```

### R0128 · board_seats_investor · 0001193125-12-119900_d267119dex43_quantum
**Question.** Extract the number of board seats an investor has the right to designate (5.1).
**Field.** `board_seats_investor` -- the number of board seats the investor/investor class may designate
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
tional Board Seat that is to be created by increasing the size of the Board of Directors pursuant to this Section 2.1 , the Company shall send notice to such Sponsor Stockholder thirty (30) days prior to the deadline by which the Board of Directors is to be expanded pursuant to this Section 2.1 . 2.2 Initial Board Seats . The Initial Board Seats shall be filled by director nominees designated as set forth below. (i) Quantum Designee . One (1) nominee designated solely by Quantum, which nominee shall initially be S. Wil Vanloh, Jr., provided , however , that the right of Quantum to designate a nominee to fill an Initial Board Seat shall lapse upon the occurrence of a Quantum Termination Event; (ii) Tribal Designee . One (1) nominee designated solely by the Tribal Company, which nominee shall initially be [ · ], provided , however , that the right of the Tribal Company to designate a nominee to fill an Initial Board Seat shall lapse upon the occurrence of a Tribal Termination Event; (iii) Ute Energy LLC Designee . One (1) nominee designated by the board of managers of Ute Energy LLC, which nominee shall be an Independent Designee and otherwise qualified under the applicable listing standards of the New York Stock Exchange (or, if different, the listing exchange on which the Common Stock is traded) to serve as a membe
```

### R0129 · preference_seniority · 1113481_000111348114000003
**Question.** Classify multi-series preferred liquidation seniority as pari-passu or stacked (1.3.4).
**Field.** `preference_seniority` -- Whether preferred series rank equally (pari-passu) or in a seniority order (stacked).
**Answer.** one of: pari-passu, stacked, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1113481/000111348114000003/exhibit993rempex.htm

**Text shown to the model:**

```
ding a consolidation or merger and conveyance of substantially all of the assets of the Company, the holders of Series A and Series B preferred stock have a preference in liquidation over the common shareholders of $1.00 and $1.05 per share, respectively, (subject to appropriate adjustment in the event of any stock dividend, stock split, reclassification or other similar recapitalization affecting such shares), plus any declared and unpaid dividends. If the assets of the Company are not sufficient to fulfill the Series A and Series B liquidation amount, the Series A and Series B stockholders will share ratably in the distribution of the assets on a pro rata basis on the liquidation amount. After the payment of the full liquidation preferences of the Series A and Series B preferred shareholders, as noted above, the assets of the Company legally available for distribution, if any, shall be distributed ratably to the holders of the common stock and Series A and Series B preferred stock on an as-if-converted to common stock basis, provided that the aggregate amount which the preferred shareholders are entitled to receive shall not exceed the M
```

### R0130 · liquidation_preference_multiple · 1283259_000149315225016953
**Question.** Classify liquidation preference multiple (1x, 2x, 3x, other, non-participating) (leaf 1.3.1).
**Field.** `liquidation_preference_multiple` -- How many times the OIP the preferred holder receives upon liquidation.
**Answer.** one of: non-participating, 1x, 2x, 3x, other, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
to be paid out of the assets of the Corporation available for distribution to its stockholders or, in the case of a Deemed Liquidation Event (as defined below), out of the consideration payable to stockholders in such Deemed Liquidation Event or the Available Proceeds (as defined below), before any payment shall be made to the holders of Common Stock by reason of their ownership thereof, an amount per share equal to one (1) times the Original Issue Price, plus any dividends declared but unpaid thereon. If upon any such liquidation, dissolution or winding up of the Corporation or Deemed Liquidation Event, the assets of the Corporation available for distribution to its stockholders shall be insufficient to pay the holders of shares of Preferred Stock the full amount to which they shall be entitled under this Section 2.1 , the holders of shares of Preferred Stock shall share ratably in any distribution of the assets available for distribution in proportion to the respective amounts which would otherwise be payable in respect of the shares held by them upon such distribution if all amounts payable on or with respect to such shares were paid in full. The amount which a holder of a share of Preferred Stock is entitled to receive under this Section 2.1 is hereinafter referred to as the “ Liquidation Amount. ””
```

### R0131 · safe_cap_vs_discount_applies · lomond_both_mfn
**Question.** Classify whether a SAFE uses cap, discount, or both-MFN for conversion pricing (2.1.3).
**Field.** `safe_cap_vs_discount_applies` -- Whether the SAFE's conversion price uses cap-only, discount-only, or both with MFN.
**Answer.** one of: cap, discount, both-mfn, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
(without double-counting, in each case calculated on an as-converted to Common Stock basis):   ● Includes all shares of Capital Stock issued and outstanding;   ● Includes all (i) issued and outstanding Options and (ii) Promised Options; and   ● Includes the Unissued Option Pool, except that any increase to the Unissued Option Pool in connection with the Equity Financing will only be included to the extent that the number of Promised Options exceeds the Unissued Option Pool prior to such increase.   - 2 -      “ Conversion Price ” means the either: (1) the Safe Price or (2) the Discount Price, whichever calculation results in a greater number of shares of the applicable Safe Capital Stock.   “ Converting Securities ” includes this Safe and other convertible securities issued by the Company, including but not limited to: (i) other Safes; (ii) convertible promissory notes and other convertible debt instruments; and (iii) convertible securities that have the right to convert into shares of Capital Stock.   “ Direct Listing ” means the Company’s initial listing of its Common Stock (other than Common Stock not eligible for resale under Rule 144 under the Securities Act) on a national securities exchange by means of an effective registration statement on Form S-1 filed by the Company with the SEC that registers existing Capital Stock of the Company for resale, as approved by the Company’s board of directors. For the avoidance of doubt, a Direct Listing shall not be deemed to be an underwritten offering and shall not involve any underwriting services.   “ Discount Price ” means the lowest price per share of the Capital Stock sold in the Equity Financing multiplied by the Discount Rate.   “ Dissolution Event ” means (i) a voluntary termination of operations, (ii) a general assignment for the benefit of the Company’s creditors or (iii) any other liquidation, dissolution or winding up of the Company ( excluding a Liquidity Event), whether voluntary or involuntary.   “ Dividend Amount ” means, with respect to any date on which the Comp
```

### R0132 · board_seats_investor · 0000950134-07-010103_d46152e8vk_mdp_old
**Question.** Extract the number of board seats an investor has the right to designate (5.1).
**Field.** `board_seats_investor` -- the number of board seats the investor/investor class may designate
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
and John W. Madigan. In connection with the completion of the initial public offering, the parties to the stockholders agreement agreed to terminate the stockholders agreement as of April 27, 2007 in connection with the director nomination agreement disclosed in Item 1.01 that was entered into by certain of our investors.      Under the stockholders agreement, the size of our Board of Directors was set at fourteen. MDP had the right to designate up to nine of the nominees for election to our Board of Directors as long as it continued to beneficially own at least 5% of our common stock. The Mitchell investors had the right to designate up to two nominees for election to our Board of Directors as long as they continued to beneficially own at least 9% of our common stock and continued to have the right to designate one nominee for election to our Board of Directors if they beneficially owned less than 9% but more than 3% of our common stock. If the Mitchell investors beneficially owned less than 3% of our common stock but more than 2% of our common stock, they would have continued to have certain board observer rights. Quadrangle had the right to designate one nominee for election to our Board of Directors as long as they continued to beneficially own at least 3% of our common stock provided that at the time Quadrangle no longer     had rights to designate
```

### R0133 · round_size · 1880063
**Question.** Extract the total aggregate financing round size in dollars (1.2.1).
**Field.** `round_size` -- total aggregate dollar amount raised in the equity financing round
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1880063/000188006321000002/primary_doc.xml

**Text shown to the model:**

```
<entityName>Outerspace Ops, Inc.</entityName>
        <issuerAddress>
            <street1>350 STARKE RD., SUITE 100</street1>
            <city>CARLSTADT</city>
            <stateOrCountry>NJ</stateOrCountry>
            <stateOrCountryDescription>NEW JERSEY</stateOrCountryDescription>
            <zipCode>07072</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>(201) 559-9466</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <withinFiveYears>true</withinFiveYears>
            <value>2019</value>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>RICKY</firstName>
                <lastName>CHOI</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>C/O OUTERSPACE OPS, INC.</street1>
                <street2>350 STARKE RD., SUITE 100</street2>
                <city>CARLSTADT</city>
                <stateOrCountry>NJ</stateOrCountry>
                <stateOrCountryDescription>NEW JERSEY</stateOrCountryDescription>
                <zipCode>07072</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification>CHIEF EXECUTIVE OFFICER</relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>PHILIP</firstName>
                <lastName>MOLDAVSKI</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>C/O OUTERSPACE OPS, INC.</street1>
                <street2>350 STARKE RD., SUITE 100</street2>
                <city>CARLSTADT</city>
                <stateOrCountry>NJ</stateOrCountry>
                <stateOrCountryDescription>NEW JERSEY</stateOrCountryDescription>
                <zipCode>07072</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification>PRESIDENT</relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>ALEX</firstName>
                <lastName>PESSALA</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>C/O OUTERSPACE OPS, INC.</street1>
                <street2>350 STARKE RD., SUITE 100</street2>
                <city>CARLSTADT</city>
                <stateOrCountry>NJ</stateOrCountry>
                <stateOrCountryDescription>NEW JERSEY</stateOrCountryDescription>
                <zipCode>07072</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification>SECRETARY</relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>JOHN</firstName>
                <lastName>VICKERS</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>C/O OUTERSPACE OPS, INC.</street1>
                <street2>350 STARKE RD., SUITE 100</street2>
                <city>CARLSTADT</city>
                <stateOrCountry>NJ</stateOrCountry>
                <stateOrCountryDescription>NEW JERSEY</stateOrCountryDescription>
                <zipCode>07072</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Other Technology</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>Decline to Disclose</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06b</item>
        </federalExemptionsExclusions>
        <typeOfFiling>
            <newOrAmendment>
                <isAmendment>false</isAmendment>
            </newOrAmendment>
            <dateOfFirstSale>
                <value>2020-12-09</value>
            </dateOfFirstSale>
        </typeOfFiling>
        <durationOfOffering>
            <moreThanOneYear>false</moreThanOneYear>
        </durationOfOffering>
        <typesOfSecuritiesOffered>
            <isEquityType>true</isEquityType>
            <isOptionToAcquireType>true</isOptionToAcquireType>
            <isSecurityToBeAcquiredType>true</isSecurityToBeAcquiredType>
        </typesOfSecuritiesOffered>
        <businessCombinationTransaction>
            <isBusinessCombinationTransaction>false</isBusinessCombinationTransaction>
            <clarificationOfResponse></clarificationOfResponse>
        </businessCombinationTransaction>
        <minimumInvestmentAccepted>1</minimumInvestmentAccepted>
        <salesCompensationList></salesCompensationList>
        <offeringSalesAmounts>
            <totalOfferingAmount>7236095</totalOfferingAmount>
            <totalAmountSold>5300600</totalAmountSold>
            <totalRemaining>1935495</totalRemaining>
```

### R0134 · liquidation_preference_multiple · 1883085_000188308524000060
**Question.** Classify liquidation preference multiple (1x, 2x, 3x, other, non-participating) (leaf 1.3.1).
**Field.** `liquidation_preference_multiple` -- How many times the OIP the preferred holder receives upon liquidation.
**Answer.** one of: non-participating, 1x, 2x, 3x, other, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
ng into the following number of Class A Shares, based on the volume weighted average trading price of the Class A Shares for the thirty (30) trading days immediately preceding the date of a written notice to the holders of the Preferred Shares of the Company’s election to so automatically convert all then outstanding Preferred Shares (“30-Day VWAP Average”): (a) if the 30-Day VWAP Average is equal to or greater than two (2) times the Original Issue Price (subject to adjustment only as provided in Article 9), one (1) Class A Share, or (b) if the 30-Day VWAP Average is less than two (2) times the Original Issue Price but greater than 25% of the Original Issue Price (in each case subject to adjustment only as provided in Article 9), a number of Class A Shares equal to (a) two (2) times the Original Issue Price (subject to adjustment only as provided in Article 9) divided by (b) the 30-Day VWAP Average (in each case, without consideration and without need for further action by the Company or the relevant holder of such Preferred Shares). All shareholders of record of Preferred Shares shall be sent written notice of the Company’s election to require conversion of the Preferred Shares and the time of mandatory conversion, on or before the time of the designated mandatory conversion, together with all information necessary to allow the convers
```

### R0135 · liquidation_preference_multiple · 1479290_000119312514020967
**Question.** Classify liquidation preference multiple (1x, 2x, 3x, other, non-participating) (leaf 1.3.1).
**Field.** `liquidation_preference_multiple` -- How many times the OIP the preferred holder receives upon liquidation.
**Answer.** one of: non-participating, 1x, 2x, 3x, other, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
ing liquidation preference, ranking, and conversion rights, such that shares of Series E-1, E-2, E-3 and E-4 convertible preferred stock are valued at less than shares of Series E-5 convertible preferred stock. In the event of any liquidation, dissolution, or winding up of the Company, either voluntary or involuntary, the holders of the Series E-1, E-2, E-3 and E-4 convertible preferred stock are entitled to receive one (1) times the original issue price, or $22.425 per share, plus all declared and unpaid dividends on such shares, while the holders of the Series E-5 convertible preferred stock are entitled to receive one and one-half (1.5) times the original issue price, or $33.6375 per share, plus all declared and unpaid dividends on such shares. If, upon the occurrence of a liquidation event, the assets and funds distributed among the holders of convertible preferred stock are insufficient to permit the payment to such holders of their full preferential amount, then the holders of the Series E-5   FIVE PALO ALTO SQUARE, 3000 EL CAMINO REAL, PALO ALTO, CA 94306-2155 T: (650) 843-5000 F: (650) 849-7400 WWW.COOLEY.COM   Jeffrey P. Riedler January 27, 2014 Page Three   convertible preferred stock are entitled to receive any distribution of assets prior and in preference to holders of the Series E-1, E-2, E-3
```

### R0136 · safe_cap_vs_discount_applies · neo_aero_both_mfn
**Question.** Classify whether a SAFE uses cap, discount, or both-MFN for conversion pricing (2.1.3).
**Field.** `safe_cap_vs_discount_applies` -- Whether the SAFE's conversion price uses cap-only, discount-only, or both with MFN.
**Answer.** one of: cap, discount, both-mfn, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
h case calculated on an as-converted to Ordinary Share basis):   ● Includes all shares of Capital Share issued and outstanding;   ● Includes all Converting Securities;   ● Includes all (i) issued and outstanding Options and (ii) Promised Options; and   ● Includes the Unissued Option Pool, except that any increase to the Unissued Option Pool in connection with the Equity Financing shall only be included to the extent that the number of Promised Options exceeds the Unissued Option Pool prior to such increase.   “ Conversion Price ” means the either: (1) the Safe Price or (2) the Discount Price, whichever calculation results in a greater number of shares of Safe Share.   “ Converting Securities ” includes this Safe and other convertible securities issued by the Company, including but not limited to: (i) other Safes; (ii) convertible promissory notes and other convertible debt instruments; and (iii) convertible securities that have the right to convert into shares of Capital Share.   “ Direct Listing ” means the Company’s initial listing of its Ordinary Share on a national securities exchange by means of an effective registration statement by the Company that registers shares of existing capital share of the Company for resale, as approved by the Company’s board of directors. For the avoidance of doubt, a Direct Listing shall not be deemed to be an underwritten offering and shall not involve any underwriting services.   “ Discount Price ” means the price per share of the Standard Share sold in the Equity Financing multiplied by the Discount Rate.   “ Dissolution Event ” means (i) a voluntary termination of operations, (ii) a general assignment for the benefit of the Company’s creditors or (iii) any other liquidation, dissolution or winding up of the Company ( excluding a Liquidity Event), whether voluntary or involuntary.   “ Dividend Amount ” means, with respect to any date on which the Company pays a dividend on its outstanding Ordinary Share, the amount of such dividend that is paid per share of Ordinary Share multiplied by
```

### R0137 · cliff_present · 0001516513-23-000036_ex-107xcraigoverpeckofferl
**Question.** Classify whether a vesting schedule includes a cliff blockage period (6.2).
**Field.** `cliff_present` -- yes if the schedule has a cliff blockage period, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
EX-10.7 2 ex-107xcraigoverpeckofferl.htm EX-10.7 Document Exhibit 10.7 April 27, 2023 Craig Overpeck Dear Craig, We are excited to offer you a spot on our growing team at Doximity. Here are the details you likely care about most: Title        SVP, Commercial Operations Start Date     May 16, 2023 Annual Salary     $300,000 Equity Grants    $4M 4yr RSU, vests qtrly, no cliff $4M 4yr PSU, vests annually based on % to (stretch) goal Benefits        Health insurance, 401k, Discretionary Time Off & more* The equity grants in this offer letter will be granted upon your conversion from consultant to employee and will replace all previously issued grants. For the avoidance of doubt, the Services Agreement between you and Doximity dated as of November 18, 2022, and the equity grants associated therewith (except for the first vest tranche of May 15, 2023), will be terminated and of no further force or effect (except for those terms that survive as set forth in the Services Agreement) on your start date. Some less exciting, but equally important components of this offer: • This offer is contingent upon clearance of background and/or reference checks. • We expect you can legally work in the United States and will need documentation proving so within 3 business days of
```

### R0138 · preference_seniority · 1556898_000119312517274422
**Question.** Classify multi-series preferred liquidation seniority as pari-passu or stacked (1.3.4).
**Field.** `preference_seniority` -- Whether preferred series rank equally (pari-passu) or in a seniority order (stacked).
**Answer.** one of: pari-passu, stacked, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1556898/000119312517274422/d167766dex31a.htm

**Text shown to the model:**

```
dividends, on each share of the Preferred Stock held by them, or (2) such amount per share as would have been payable had all shares of such series of Preferred Stock been converted into Common Stock pursuant to Section C.5 immediately prior to such Liquidation Event. If, upon the occurrence of such Liquidation Event, the proceeds thus distributed among the holders of Preferred Stock shall be insufficient to permit the payment to such holders of the full aforesaid preferential amount, then the entire proceeds legally available for distribution shall be distributed ratably among the holders of Preferred Stock in proportion to the preferential amount each such holder is otherwise entitled to receive. For purposes of this Certificate of Incorporation (the “ Certificate ”), the “ Original Issue Price ” shall mean $0.25 per share of Series Seed Preferred Stock, $1.00 per share of Series A Preferred Stock, and $2.00 per share of Series B Preferred Stock, each as adjusted for any stock dividends, stock splits, stock combinations, recapitalizations or similar events with respect to such shares. (b) After payment to the holders of Preferred Stock of the preferential amounts required by
```

### R0139 · information_rights · 0000950123-14-010038_filename6
**Question.** Classify whether a document grants investors a live financial-reporting/information right (5.3).
**Field.** `information_rights` -- yes if a live obligation to deliver financials to investors exists, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
nts need not include footnotes, but otherwise shall comply with U.S. generally accepted accounting principles), together with a current capitalization schedule, except that in the case of any month that is also the end of a fiscal quarter, such financial statements shall be prepared on both a monthly and quarterly basis;   Entellus Medical, Inc.: Fifth Amended and Restated Investors Rights Agreement    Page 1 1.3.2. deliver the following annual financial statements to each Major Investor as soon as available but in any event within 120 days after the end of each fiscal year: a balance sheet of the Company, as of the end of such fiscal year, together with the related statements of operations, retained earnings and cash flow for such fiscal year, all in reasonable detail and duly certified by the Accountants, who shall have given the Company an opinion, unqualified as to the scope of the audit, regarding such statements; 1.3.3. (a) at least 30 days before the beginning of each fiscal year, ensure that management prepares and submits to the Board, and the Board approves (with such changes as the Board wishes to make), the operating plan and budget for the upcoming year, and that such approved budget is delivered to each Major Investor on or before 45 days after the beginning of such upcoming fiscal year, and (b) within 30 days after the end of each m
```

### R0140 · safe_valuation_cap · 1657493_000121390021028831_cap
**Question.** Extract the valuation cap from a SAFE agreement (2.1.1)
**Field.** `safe_valuation_cap` -- the valuation cap in dollars as a bare integer (no $ or commas)
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
Y, INC.   SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by __________ , (the “ Investor ”) of $_________ (the “ Purchase Amount ”) on or about March 23, 2021, RENTBERRY, INC. , a Delaware corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   The “ Pre-Money Valuation Cap ” is $15,000,000.   The “ Discount Rate ” is 20%.   See Section 2 for certain additional defined terms.   1. Events   (a) Next Equity Financing . If there is a Next Equity Financing before the expiration or termination of this Safe, on the initial closing of such Next Equity Financing, this Safe will automatically convert into the number of shares of Safe Preferred Stock equal to the Purchase Amount divided by the Conversion Price.   In connection with the automatic conversion of this Safe into shares of Safe Preferred Stock, the Investor will execute and deliver to the Company all of the transaction documents related to the Next Equity Financing; provided, that such documents are the same documents to be entered into with the purchasers of Standard Preferred Stock, with appropriate variations for the Safe Preferred Stock if applicable, and provided further, that such documents have customary exceptions
```

### R0141 · preference_seniority · 1092283_000119312505071414
**Question.** Classify multi-series preferred liquidation seniority as pari-passu or stacked (1.3.4).
**Field.** `preference_seniority` -- Whether preferred series rank equally (pari-passu) or in a seniority order (stacked).
**Answer.** one of: pari-passu, stacked, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1092283/000119312505071414/d8k.htm

**Text shown to the model:**

```
o receive dividends at the rate of 8% per annum of the original purchase price thereof when, as and if declared by the Board of Directors out of funds legally available for the payment of dividends. Preferred dividends on a share of Series C Preferred Stock shall accrue and shall be cumulative whether or not declared from the date of issue of such share of Series C Preferred Stock, whether or not the Company has earnings, whether or not there are funds legally available for the payment of such dividends, and whether or not such dividends are declared.   The Series C Preferred Stock ranks senior to the Series B Preferred Stock, the Company’s common stock and to each other class of capital stock of the Company or series of preferred stock of the Company subsequently established by the board of directors, the terms of which do not expressly provide that such class or series ranks senior to, or on a parity with, the Series C Preferred Stock as to dividend rights and rights on liquidation, winding-up and dissolution of the Company. In the event of any liquidation, dissolution or winding-up of the Company, after payment or distribution of the assets of the Comp
```

### R0142 · option_strike_409a · 0001193125-11-194811_0p61
**Question.** Extract the stock option exercise price per share from a grant agreement (6.4).
**Field.** `option_strike_409a` -- the exercise price (strike price) per share of the granted option
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
TARGET GRANT: the option grant stated to have an exercise price of $0.61 per share (see below).

es were deemed to be exempt from registration pursuant to Rule 701 promulgated under the Securities Act as transactions pursuant to a compensatory benefit plan approved by the registrant’s board of directors.     •   On February 2, 2011, we granted options under our 2007 Stock Option/Stock Issuance Plan, as amended, to purchase 113,000 shares of our common stock to our employees, directors and consultants, having an exercise price of $0.61 per share for an aggregate exercise price of $68,930. The issuance and sale of these securities were deemed to be exempt from registration pursuant to Rule 701 promulgated under the Securities Act as transactions pursuant to a compensatory benefit plan approved by the registrant’s board of directors.     •   On February 15, 2011, we entered into a Note Purchase Agreement, pursuant to which we issued to promissory notes with an aggregate principal amount of $2,500,000. The notes bear interest at the lesser of 13% per annum or the maximum rate allowed under applicable law. The sale of these notes was exempt from registration under Section 4(2) of the Securities Act, as a sale not involving a public offering.     •   On March 1, 2011, we sold and issued an aggregate of 2,000 shares of common stock pursuant to an option exercise by the holder of a stock option issued under our 2007 Stock Option/Stock
```

### R0143 · board_seats_investor · 0001193125-12-119900_d267119dex43_tribal
**Question.** Extract the number of board seats an investor has the right to designate (5.1).
**Field.** `board_seats_investor` -- the number of board seats the investor/investor class may designate
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
es designated as set forth below. (i) Quantum Designee . One (1) nominee designated solely by Quantum, which nominee shall be an Independent Designee, provided , however , that the right of Quantum to designate a nominee to fill an Additional Board Seat shall lapse at such time that the Quantum Stockholders, in the aggregate, cease to hold at least twenty-five percent (25%) of the then-outstanding Common Stock; (ii) Tribal Designees . Two (2) nominees designated solely by the Tribal Company, which nominees shall be Independent Designees, provided , however , that the right of the Tribal Company to designate nominees to fill Additional Board Seats shall (A) be reduced from two (2) to one (1) at such time that the Tribal Stockholders, in the aggregate, cease to hold at least twenty-five percent (25%) of the then-outstanding Common Stock and (B) lapse upon the occurrence of a Tribal Termination Event; and (iii) Company Designee . One (1) nominee designated by the Board of Directors, which nominee shall be an Independent Designee. 2.4 Failure to Timely Designate Director for Additional Board Seat . If a Sponsor Stockholder fails to designate a nominee to fill an Additional Board Seat by the time such Additional Board Seat is created pursuant to Section 2.1 of this Agreement, the Board of Directors shall have the right
```

### R0144 · fully_diluted_basis · emageon_ex
**Question.** Classify capitalization definition as fully-diluted or issued-outstanding basis (3.4).
**Field.** `fully_diluted_basis` -- Whether cap is computed on fully-diluted or issued-outstanding basis.
**Answer.** one of: fully-diluted, issued-outstanding, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1121439/000095014405000529/g89998a2exv10w15xay.txt

**Text shown to the model:**

```
ockholders and Investors shall vote their shares of capital stock of Company for a Board of Directors consisting of nine (9) directors. For so long as the outstanding Shares of Series A Preferred constitute five percent (5%) or more of the Company's outstanding capital stock (on a fully diluted basis), the Series A Investors, voting separately as a class, shall have the right to elect one (1) director (the "Series A Director") (and to fill any vacancies with respect thereto) by a vote of a majority of the then outstanding shares of Series A Preferred. In connection ther
```

### R0145 · vesting_schedule · 0001144204-15-053727_v419640_ex10-1
**Question.** Extract and normalize vesting schedule to canonical string format (6.1).
**Field.** `vesting_schedule` -- Normalized vesting schedule: e.g. '4yr/1yr-cliff', '3yr/no-cliff', '4yr/cliff'.
**Answer.** string value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
ss at Atossa Genetics is our people and the effort and talent they bring to the workplace. In recognition of this importance, we are pleased to inform you that you will be promoted from Sr. Vice President, Operations to Chief Operating Officer, effective September 1, 2015. This is a Section 16 Officer position and the annual rate of pay will be $287,040. In addition, you will be granted an option to purchase 50,000 shares of Atossa Genetics common stock at the closing price on the date approved by the board, which vests over four years of employment with no cliff.   In your time with Atossa, you have quickly demonstrated your work ethic, dedication, and your superb qualifications. We have faith that you will continue to excel in your new position and hope that you continue to develop your potential here at Atossa Genetics.   Congratulations on this promotion, and we look forward to your contributions in your new position.   Thank you for being such a valuable asset to Atossa Genetics and for your loyal service.   Sincerely, /s/ Steven C. Quay, MD, PHD, FCAP Steven C. Quay, MD, PHD, FCAP CEO and President   /s/ S
```

### R0146 · safe_cap_vs_discount_applies · paxmedica_both_mfn
**Question.** Classify whether a SAFE uses cap, discount, or both-MFN for conversion pricing (2.1.3).
**Field.** `safe_cap_vs_discount_applies` -- Whether the SAFE's conversion price uses cap-only, discount-only, or both with MFN.
**Answer.** one of: cap, discount, both-mfn, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
sposition of all or substantially all of the assets of the Company.   “ Company Capitalization ” is calculated as of immediately prior to the Equity Financing and (without double-counting, in each case calculated on an as-converted to Common Stock basis):   ·          Includes all shares of Capital Stock issued and outstanding; ·          Includes all Converting Securities; ·          Includes all (i) issued and outstanding Options and (ii) Promised Options; and ·          Includes the Unissued Option Pool.   “ Conversion Price ” means the either: (1) the Safe Price or (2) the Discount Price, whichever calculation results in a greater number of shares of Safe Capital Stock.   “ Converting Securities ” includes this Safe and other convertible securities issued by the Company, including but not limited to: (i) other Safes; (ii) convertible promissory notes and other convertible debt instruments; and (iii) convertible securities that have the right to convert into shares of Capital Stock.   - 2 -     “ Discount Price ” means the price per share of the Standard Capital Stock sold in the Equity Financing multiplied by the Discount Rate.   “ Dissolution Event ” means (i) a voluntary termination of operations, (ii) a general assignment for the benefit of the Company’s creditors or (iii) any other liquidation, dissolution or winding up of the Company ( excluding a Liquidity Event), whether voluntary or involuntary.   “ Dividend Amount ” means, with respect to any date on which the Company pays a dividend on its outstanding Common Stock, the amount of such dividend that is paid per share of Common Stock multiplied by (x) the Purchase Amount divided by (y) the Liquidity Price (treating the dividend date as a Liquidity Event solely for purposes of calculating such Liquidity Price).   “ Equity Financing ” means a bona fide transaction or series of transactions with the principal purpose of raising capital, pursuant to which the Company issues and sells (i) Common Stock in a Qualifying IPO or (ii) Preferred Stock, in each case at a fixe
```

### R0147 · securities_exemption · 1260990
**Question.** Classify which Securities Act exemption a Form D filing claimed (7.1).
**Field.** `securities_exemption` -- The federal exemption claimed in the Form D filing.
**Answer.** one of: 506b, 506c, 504, reg-a, other, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1260990/000157093414000003/primary_doc.xml

**Text shown to the model:**

```
<entityName>GTX INC /DE/</entityName>
        <issuerAddress>
            <street1>175 TOYOTA PLAZA</street1>
            <street2>7TH FLOOR</street2>
            <city>MEMPHIS</city>
            <stateOrCountry>TN</stateOrCountry>
            <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
            <zipCode>38103</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>901-523-9700</issuerPhoneNumber>
        <jurisdictionOfInc>DELAWARE</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <overFiveYears>true</overFiveYears>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Mitchell</firstName>
                <middleName>S.</middleName>
                <lastName>Steiner</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Marc</firstName>
                <middleName>S.</middleName>
                <lastName>Hanover</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>James</firstName>
                <middleName>T.</middleName>
                <lastName>Dalton</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Henry</firstName>
                <middleName>P.</middleName>
                <lastName>Doggrell</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>J.</firstName>
                <middleName>R.</middleName>
                <lastName>Hyde, III</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Kenneth</firstName>
                <middleName>S.</middleName>
                <lastName>Robinson</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>J.</firstName>
                <middleName>Kenneth</middleName>
                <lastName>Glass</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Michael</firstName>
                <middleName>G.</middleName>
                <lastName>Carter</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Barrington</firstName>
                <middleName>J.A.</middleName>
                <lastName>Furr</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>c/o GTx, Inc.,</street1>
                <street2>175 Toyota Plaza, 7th Floor</street2>
                <city>Memphis</city>
                <stateOrCountry>TN</stateOrCountry>
                <stateOrCountryDescription>TENNESSEE</stateOrCountryDescription>
                <zipCode>38103</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Director</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Biotechnology</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>Decline to Disclose</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06b</item>
        </federalExemptionsExclusions>
```

### R0148 · information_rights · 0000950123-09-064388_f53797orexv4w2
**Question.** Classify whether a document grants investors a live financial-reporting/information right (5.3).
**Field.** `information_rights` -- yes if a live obligation to deliver financials to investors exists, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
s shall make such examinations, in accordance with generally accepted auditing standards, as will enable them to give such reports or opinions with respect to the financial statements of the Company as will satisfy the requirements of the Commission in effect at such time with respect to reports or opinions of accountants.       3.3 Furnishing of Financial Statements and Information. The Company will:            (a) Deliver to each Major Investor as soon as available, but in any event within forty-five (45) days after the end of each of the first three (3) quarters of each fiscal year of the Company, an unaudited balance sheet of the Company, together with the related statements of operations, retained earnings and cash flow statements for such quarter ( provided, however, that such statements need not include footnotes, but otherwise shall comply with generally accepted accounting principles (subject to normal year-end adjustments)) which financial statements shall compare the financial information contained therein with the Company’s operating plan and budget for such period.            (b) Deliver to each Investor as soon as available, but in any event within ninety (90) days after the end of each fiscal year, a balance sheet of the Company, as of the end of such fiscal year, together with the related statements of operations
```

### R0149 · cliff_present · 0001558370-21-008713_giii-20210628x8k
**Question.** Classify whether a vesting schedule includes a cliff blockage period (6.2).
**Field.** `cliff_present` -- yes if the schedule has a cliff blockage period, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
ransition period for complying with any new or revised financial accounting standards provided pursuant to Section 13(a) of the Exchange Act. ☐ ​ Item 1.01 Entry into a Material Definitive Agreement. ​ In March 2021, the Compensation Committee (the “Compensation Committee”) of the Board of Directors of G-III Apparel Group, Ltd. (the “Company”) awarded time-based restricted stock units with three-year cliff-vesting (“Cliff-Vesting RSUs”), pursuant to the Company’s 2015 Long-Term Incentive Plan, as amended (the “2015 Plan”), to the named executive officers of the Company (the “Named Executive Officers”) in the amounts shown under the heading “Cliff-Vesting RSUs Awarded in March 2021” in the table below. The Compensation Committee awarded Cliff-Vesting RSUs because setting meaningful long-term performance conditions was, at the time of the awards, impracticable due to the severe disruptions to the Company’s business caused by the COVID-19 pandemic and the resulting inability to provide guidance concerning the Company’s financial results. ​ In June 2021, following stabilization of the Company’s business and its resumption of public reporting of guidance concerning its financial results, the Compensation Committee determined to restructure the Cliff-Vesting RSUs granted to the Named Executive Officers in March 2021 to be
```

### R0150 · round_size · 1498738
**Question.** Extract the total aggregate financing round size in dollars (1.2.1).
**Field.** `round_size` -- total aggregate dollar amount raised in the equity financing round
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1498738/000149873814000005/primary_doc.xml

**Text shown to the model:**

```
<entityName>VoCare, Inc.</entityName>
        <issuerAddress>
            <street1>8888 KEYSTONE CROSSING</street1>
            <street2>SUITE 1300</street2>
            <city>INDIANAPOLIS</city>
            <stateOrCountry>IN</stateOrCountry>
            <stateOrCountryDescription>INDIANA</stateOrCountryDescription>
            <zipCode>46240</zipCode>
        </issuerAddress>
        <issuerPhoneNumber>(317) 973-1003</issuerPhoneNumber>
        <jurisdictionOfInc>INDIANA</jurisdictionOfInc>
        <issuerPreviousNameList>
            <value>None</value>
        </issuerPreviousNameList>
        <edgarPreviousNameList>
            <value>None</value>
        </edgarPreviousNameList>
        <entityType>Corporation</entityType>
        <yearOfInc>
            <withinFiveYears>true</withinFiveYears>
            <value>2009</value>
        </yearOfInc>
    </primaryIssuer>
    <relatedPersonsList>
        <relatedPersonInfo>
            <relatedPersonName>
                <firstName>Steven</firstName>
                <middleName>R</middleName>
                <lastName>Peabody</lastName>
            </relatedPersonName>
            <relatedPersonAddress>
                <street1>8888 Keystone Crossing</street1>
                <street2>Suite 1300</street2>
                <city>Indianapolis</city>
                <stateOrCountry>IN</stateOrCountry>
                <stateOrCountryDescription>INDIANA</stateOrCountryDescription>
                <zipCode>46240</zipCode>
            </relatedPersonAddress>
            <relatedPersonRelationshipList>
                <relationship>Executive Officer</relationship>
                <relationship>Director</relationship>
                <relationship>Promoter</relationship>
            </relatedPersonRelationshipList>
            <relationshipClarification></relationshipClarification>
        </relatedPersonInfo>
    </relatedPersonsList>
    <offeringData>
        <industryGroup>
            <industryGroupType>Other Health Care</industryGroupType>
        </industryGroup>
        <issuerSize>
            <revenueRange>Decline to Disclose</revenueRange>
        </issuerSize>
        <federalExemptionsExclusions>
            <item>06c</item>
        </federalExemptionsExclusions>
        <typeOfFiling>
            <newOrAmendment>
                <isAmendment>true</isAmendment>
                <previousAccessionNumber>0001498738-10-000001</previousAccessionNumber>
            </newOrAmendment>
            <dateOfFirstSale>
                <value>2010-07-12</value>
            </dateOfFirstSale>
        </typeOfFiling>
        <durationOfOffering>
            <moreThanOneYear>false</moreThanOneYear>
        </durationOfOffering>
        <typesOfSecuritiesOffered>
            <isEquityType>true</isEquityType>
        </typesOfSecuritiesOffered>
        <businessCombinationTransaction>
            <isBusinessCombinationTransaction>false</isBusinessCombinationTransaction>
            <clarificationOfResponse></clarificationOfResponse>
        </businessCombinationTransaction>
        <minimumInvestmentAccepted>10000</minimumInvestmentAccepted>
        <salesCompensationList></salesCompensationList>
        <offeringSalesAmounts>
            <totalOfferingAmount>25000000</totalOfferingAmount>
            <totalAmountSold>5000000</totalAmountSold>
            <totalRemaining>20000000</totalRemaining>
```

### R0151 · safe_pre_post · 1811623_000110465922070160
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1811623/000110465922070160/tm2135343d4_ex10-8.htm

**Text shown to the model:**

```
EX-10.8 3 tm2135343d4_ex10-8.htm EXHIBIT 10.8   Exhibit 10.8   THIS INSTRUMENT AND ANY SECURITIES ISSUABLE PURSUANT HERETO HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE “ SECURITIES ACT ”), OR UNDER THE SECURITIES LAWS OF CERTAIN STATES. THESE SECURITIES MAY NOT BE OFFERED, SOLD OR OTHERWISE TRANSFERRED, PLEDGED OR HYPOTHECATED EXCEPT AS PERMITTED IN THIS SAFE AND UNDER THE ACT AND APPLICABLE STATE SECURITIES LAWS PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT OR AN EXEMPTION THEREFROM.   PaxMedica, Inc.   SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by Amar Foundation (the “ Investor ”) of $5,000,000 (the “ Purchase Amount ”) on or about March 19, 2021, PaxMedica, Inc., a Delaware corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   The “ Post-Money Valuation Cap ” is $150,000,000.00.   The “ Discount Rate ” is 50%.   See Section 2 for certain additional defined terms.   1.        Events   (a)     Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the number of shares of Safe Capital Stock equal to the Purchase Amount divided by the Conversion Price.   In connection with the automatic conversion of this Safe into shares of Safe Capital Stock, the Investor will execute and deliver to the Company all of the transaction documents related to the Equity Financing; provided, that such documents (i) are the same documents to be entered into with the purchasers of Standard Capital Stock, with appropriate variations for the Safe Capital Stock if applicable, and (ii) have customary exceptions to any drag-along applicable to the Investor, including (without limitation) limited representations, warranties, liability and indemnification obligations for the Investor.   (b)     Liquidity Event . If there is a Liquidity Event before the termination of this Safe, the Investor will automatically be entitled (subject to the liquidation priority set forth in Section 1(d) below) to receive a portion of Proceeds, due and payable to the Investor immediately prior to, or concurrent with, the consummation of such Liquidity Event, equal to the greater of (i) the Purchase Amount (the “ Cash-Out Amount ”) or (ii) the amount payable on the number of shares of Common Stock equal to the Purchase Amount divided by
```

### R0152 · safe_pre_post · 1937891_000149315226027213
**Question.** Classify a SAFE's valuation cap as pre-money or post-money (2.1.4).
**Field.** `safe_cap_type` -- Whether the SAFE valuation cap is pre-money or post-money.
**Answer.** one of: post-money, pre-money, or mark `undeterminable` and leave it blank.
**Source.** https://www.sec.gov/Archives/edgar/data/1937891/000149315226027213/ex10-1.htm

**Text shown to the model:**

```
EX-10.1 2 ex10-1.htm EX-10.1   Exhibit 10.1   THIS INSTRUMENT AND ANY SECURITIES ISSUABLE PURSUANT HERETO HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE “ SECURITIES ACT ”), OR UNDER THE SECURITIES LAWS OF CERTAIN STATES. THESE SECURITIES MAY NOT BE OFFERED, SOLD OR OTHERWISE TRANSFERRED, PLEDGED OR HYPOTHECATED EXCEPT AS PERMITTED IN THIS SAFE AND UNDER THE ACT AND APPLICABLE STATE SECURITIES LAWS PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT OR AN EXEMPTION THEREFROM.   ETRONIUM AI INC.   SAFE (Simple Agreement for Future Equity)   THIS CERTIFIES THAT in exchange for the payment by AMC Robotics Corporation (the “ Investor ”) of $500,000 (the “ Purchase Amount ”) on or about ____, 2026, Etronium AI Inc., a North Carolina corporation (the “ Company ”), issues to the Investor the right to certain shares of the Company’s Capital Stock, subject to the terms described below.   The “ Post-Money Valuation Cap ” is $______. See Section 2 for certain additional defined terms.     1. Events   (a) Equity Financing . If there is an Equity Financing before the termination of this Safe, on the initial closing of such Equity Financing, this Safe will automatically convert into the greater of: (1) the number of shares of Standard Preferred Stock equal to the Purchase Amount divided by the lowest price per share of the Standard Preferred Stock; or (2) the number of shares of Safe Preferred Stock equal to the Purchase Amount divided by the Safe Price.   In connection with the automatic conversion of this Safe into shares of Standard Preferred Stock or Safe Preferred Stock, the Investor will execute and deliver to the Company all of the transaction documents related to the Equity Financing; provided, that such documents (i) are the same documents to be entered into with the purchasers of Standard Preferred Stock, with appropriate variations for the Safe Preferred Stock if applicable, and (ii) have customary exceptions to any drag-along applicable to the Investor, including (without limitation) limited representations, warranties, liability and indemnification obligations for the Investor.   (b) Liquidity Event . If there is a Liquidity Event before the termination of this Safe, the Investor will automatically be entitled (subject to the liquidation priority set forth in Section 1(d) below) to receive a portion of Proceeds, due and payable to the Investor immediately prior to, or concurrent with, the consummation of such Liquidity Event, equal to the greater of (i) t
```

### R0153 · information_rights · 0001193125-07-042724_dex101
**Question.** Classify whether a document grants investors a live financial-reporting/information right (5.3).
**Field.** `information_rights` -- yes if a live obligation to deliver financials to investors exists, else no.
**Answer.** one of: yes, no, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
EX-10.1 2 dex101.htm TSFG AMENDED AND RESTATED RESTRICTED STOCK AGREEMENT PLAN TSFG Amended and Restated Restricted Stock Agreement Plan Exhibit 10.1 AMENDMENT 1 TO THE SOUTH FINANCIAL GROUP’S AMENDED AND RESTATED RESTRICTED STOCK AGREEMENT PLAN This Amendment 1 (this “Amendment”) to The South Financial Group Amended and Restated Restricted Stock Agreement Plan (the “Plan”) is made by The South Financial Group, to be effective as of the date hereof. Capitalized terms not otherwise defined in this Amendment have the meanings assigned to them in the Plan. The third and fourth sentences of Section 1 of the Plan are hereby deleted and replaced with the following: Subject to adjustment in accordance with the provisions of Section 8 hereof, the total amount of Shares which may be issued pursuant to Restricted Stock Agreements under the Plan shall not exceed in the aggregate 500,000 Shares. This limitation of 500,000 Shares shall be calculated as of the date hereof, and
```

### R0154 · option_strike_409a · 0001125282-06-006236_1p25
**Question.** Extract the stock option exercise price per share from a grant agreement (6.4).
**Field.** `option_strike_409a` -- the exercise price (strike price) per share of the granted option
**Answer.** number value, or mark `undeterminable` and leave it blank.
**Source.** (no source URL recorded)

**Text shown to the model:**

```
TARGET GRANT: the option grant stated to have an exercise price of $1.25 per share (see below).

2005, we issued 1,000 shares and 625 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $0.60 per share and $3.75 per share, respectively.         • On January 3, 2006, we granted options to fifteen of our employees to purchase an aggregate of 57,500 shares of our common stock under our Amended and Restated Stock Option Plan at an exercise price of $1.25 per share.         • On March 7, 2006, we issued 500 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $0.25 per share. II-3 Back to Contents   • On April 10, 2006, we issued 2,000 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $1.00 per share.         • On April 26, 2006, we granted options to 38 of our employees to purchase an aggregate of 706,750 shares of our common stock under our Amended and Restated Stock Option Plan at an exercise price of $11.00 per share.         • On May 24, 2006, we issued 1,250 shares of our common stock upon the exercise of options granted under our Amended and Restated Stock Option Plan at an exercise price of $0.25 per share.         • On June 9, 2006, we issued 1,000 shares of our common s
```
