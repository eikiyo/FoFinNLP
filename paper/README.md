# Probity paper source — FinNLP 2026

Upload `paper.zip` to Overleaf and compile. Nothing needs editing.

## Compiling

Overleaf: set the compiler to **pdfLaTeX** and the main document to `main.tex`. The
`final` option is set, so the output is the camera-ready version: byline, no line numbers. Locally:

```
latexmk -pdf main.tex
```

Use `latexmk`, or run pdflatex **four** times by hand:

```
pdflatex main && bibtex main && pdflatex main && pdflatex main && pdflatex main
```

Four is not defensive rounding, it is measured. With three pdflatex passes the document compiles
with no error, no warning and the right page count, but `lineno` has not converged: four review
line numbers are still printed on top of body text, one of them across a figure label. The fourth
pass removes all four. `verify_paper.py` checks for exactly this, and it is the only check in the
file that has ever separated two builds of identical source.

Packages beyond the ACL defaults: `booktabs`, `siunitx`, `graphicx`, `multirow`, `xcolor`.
Nothing else, deliberately: every added package is a compile risk on a machine that is not this
one.

## Regenerating the exhibits

Every number in `main.tex` and in every table and figure comes from `../out/tables/*.csv`.
None is typed by hand.

```
python3 make_tables.py     # -> tables/*.tex     (5 fragments)
python3 make_figures.py    # -> figures/*.pdf    (2 vector figures)
python3 verify_paper.py    # runs the acceptance test, exits non-zero on any failure
```

Both generators are **idempotent**: re-running them on unchanged input produces a zero byte diff.
That is the test that matters for a committed generated file, because a generator that *can* be
right is not the same as a committed copy that still *is* right.

To rebuild the CSVs themselves, from the frozen benchmark:

```
python3 ../analysis/run_all.py     # the full pipeline
python3 ../analysis/gate0.py       # the provenance-contamination gate, out/tables/{all,clean}/
```

## Which numbers the paper reports

The provenance audit in `../out/AUDIT_CONTAMINATION.md` found that 46 of 470 items cannot be
answered from the window the model is shown, and that wobble on those items is materially higher.
The paper's headline numbers are therefore computed on the 424 audited items, read from
`out/tables/clean/`. The pre-exclusion figures are in `out/tables/all/` and appear in the paper as
Table 5.

## Layout

```
main.tex                 the paper
acl.sty, acl_natbib.bst  official ACL style files, unmodified
anthology.bib            ACL Anthology entries, fetched from aclanthology.org
custom.bib               arXiv entries, fetched from the arXiv API
tables/*.tex             generated, \input by main.tex
figures/*.pdf            generated, vector
tablekit.py              shared LaTeX primitives for make_tables.py
verify_paper.py          the acceptance test
```

## Before submitting

- Complete the Responsible NLP Checklist, including the generative-AI disclosure. The
  Acknowledgements paragraph in `main.tex` states that AI assistance was used for analysis code and
  drafting; the checklist entry must match it.
- Replace the artifact sentence in Section 5 with the anonymised artifact URL from the submission
  form. Do not cite a named repository in a review submission.
- Re-run `verify_paper.py` after any edit. It checks the page count, anonymity, the exhibit budget,
  the 7pt floor, that every quoted number is a rounding of a generated value, that every citation
  resolves to a verified record, and the prose rules.
