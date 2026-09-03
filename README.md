# Probity

Artifact for “What the Window Does Not Contain: Auditing Provenance in a Document-Grounded
Instability Benchmark”, accepted at FinNLP 2026 (EMNLP workshop). Seyed Mosayeb Alam,
KTH Royal Institute of Technology. The tree is the audited snapshot the paper's numbers are
verified against; the full working repository, including the 60.5 MB of full filing texts this
snapshot omits for size, is at https://github.com/eikiyo/probity. Anthology entry to follow
after the workshop (October 2026).

## Reproduce Table 1 (target: under 15 minutes, most of it LaTeX)

    python3 paper/make_tables.py          # regenerates every paper/tables/*.tex from out/tables/*.csv
    cd paper && latexmk -pdf main.tex     # builds the paper

`make_tables.py` refuses to write a table whose numbers are missing from the generated CSVs; a
successful run has already checked the committed tables against the data.

## Verify the whole paper

    cd paper && python3 verify_paper.py

Runs every gate the camera-ready is held to: page budget, the byline, exhibit budget, figure fonts and
vector-ness, overprint detection, table-generator agreement, every decimal in the prose against the
CSVs, citation resolution, the prose rules, and the single-annotator language rule.

## Re-derive the numbers from the raw responses

    python3 analysis/oracle_audit.py      # provenance audit (needs the full filing texts, see below)
    python3 analysis/block3a.py           # the analysis blocks that write out/tables/

## What is here, and what is not

| present | absent, and why |
|---|---|
| `engine/`: the harness and task registry | development history (this tree is a snapshot) |
| `leaves/*/oracle.jsonl`: every label with its validating quote | CI, packaging, demo recordings |
| `leaves/*/corpus/questions/`: the windowed extract each model saw | `leaves/*/corpus/full/`: the full filing texts (60.5 MB); the paper's data statement describes them and they are part of the full release, omitted here for size |
| `leaves/*/runs_*.jsonl`: the responses the paper analyses | every artifact of a second, unreported temperature arm |
| `analysis/`, `out/`, `paper/`: the full path from responses to tables | |

`DATA_STATEMENT.md` is the full data statement, including two questions it records as UNRESOLVED.
