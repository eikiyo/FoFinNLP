"""
Location: paper-a/analysis/block3a.py
Purpose: BLOCK 3a entry point. Builds the model-flagged oracle review worklist and writes it to
         out/annotation/oracle_flags.csv plus a REVIEW.md the author works through. The models
         propose candidates; the author adjudicates each against the source document. That
         distinction is the whole reason this is admissible alongside section 2's argument that a
         model-written answer key can be wrong in the ways the model under test is wrong.
         Usage:  python3 analysis/block3a.py
Functions: build(), write_review(), main()
Calls: oracle_flags, fold, matrix, contamination, oracle_audit
Imports: sys, pathlib, typing
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config                      # noqa: E402
import contamination as C          # noqa: E402
import fold                        # noqa: E402
import matrix                      # noqa: E402
import oracle_audit as OA          # noqa: E402
import oracle_flags as OF          # noqa: E402
import tables_out as T             # noqa: E402

COLS = ("leaf", "item", "unanimous", "strict", "consensus_answer", "oracle", "n_agree",
        "n_models", "runs_backing", "runs_total", "support", "min_modal_n", "meets_run_floor",
        "url")
# The author-facing worklist, in the brief's own column order, ending in two EMPTY columns. They
# are empty because nothing here may fill them: a flag is a question put to a human, and a file
# that shipped with a verdict already in it would be a model writing the answer key, which is the
# practice section 2 argues against.
FLAG_COLS = ("item", "leaf", "oracle", "consensus_answer", "runs_backing", "runs_total",
             "support", "unanimous", "strict", "min_modal_n", "url", "quote")
ADJUDICATION = ("adjudication", "adjudication_note", "adjudication_basis")


def carried_verdicts(path) -> dict:
    """(leaf, item) -> the author's verdict columns already on disk.

    This generator rewrites model_flags.csv on every run, and the file is the ONLY place the
    author's adjudication lives. Writing blanks over it destroyed a completed adjudication once,
    silently: every downstream number then reported the pre-adjudication corpus while the pipeline
    printed green. A verdict is hand-made and irreplaceable, so it is read back and carried
    forward, and a flag that vanishes while holding one is a hard error rather than a quiet loss.
    Keyed on (leaf, item) because one filing can carry a flag on two different provisions."""
    if not path.exists():
        return {}
    import csv
    with open(path) as f:
        rows = list(csv.DictReader(f))
    return {(r["leaf"], r["item"]): {c: r.get(c, "") for c in ADJUDICATION}
            for r in rows if any(r.get(c, "").strip() for c in ADJUDICATION)}


def build() -> Dict[str, Any]:
    """The worklist, over ALL items rather than clean-only: a label error is exactly as worth
    finding on an item the provenance audit already flagged, and excluding those would hide the
    overlap between the two failure modes, which is itself a result."""
    models, leaves, cells = matrix.load_cells()
    names = [l["leaf"] for l in leaves]
    per_cell = fold.collect(models, leaves)["per_cell"]
    rows = OF.flag_rows(models, names, per_cell, C.oracle_ids(leaves), OA.corpus_index())
    return {"rows": rows, "summary": OF.summarise(rows), "n_models": len(models)}


def _verdict_lines(r: Dict[str, Any], held: dict) -> List[str]:
    """One item's verdict rendered from the carried CSV columns, or the open checkboxes while the
    author has not ruled. The CSV stays the single source of truth; this document mirrors it, so a
    worklist regenerated after the sitting shows the sitting instead of reopening it. Before this,
    the CSV said `excluded` while this file still printed empty checkboxes under an `awaiting
    author adjudication` header: two artifacts about the same fact, disagreeing."""
    v = held.get((r["leaf"], r["item"]), {})
    if not v.get("adjudication", "").strip():
        return ["- [ ] upheld (the oracle label is wrong)  ",
                "  [ ] rejected (the oracle label is right)  ",
                "  adjudication note: ", ""]
    return [f"- verdict: **{v['adjudication']}** (basis: "
            f"{v.get('adjudication_basis', '').strip() or 'unstated'})",
            f"- adjudication note: {v.get('adjudication_note', '').strip()}", ""]


def _review_header(summary: Dict[str, Any], n_models: int, verdicts: List[str],
                   settled: bool) -> List[str]:
    """The document's front matter: status line and summary bullets. The status flips to settled,
    and the placeholder counts become real ones, only when EVERY flag carries a verdict -- a
    partially adjudicated worklist keeps saying WIP rather than describing the finished sitting
    it has not had."""
    status = (f"> STATUS: settled - all {len(verdicts)} flags adjudicated by the author - "
              f"generated for {n_models} configurations" if settled else
              f"> STATUS: WIP - awaiting author adjudication - generated for {n_models} "
              f"configurations")
    return ["# Model-flagged oracle review (Block 3a)", "", status, "",
            "Every item below is one where the configurations' modal answers agree with each "
            "other and differ from the stored oracle label. **This is a worklist, not a "
            "finding.** The models flag; they do not decide. A flag becomes an error only when "
            "the author has read the source document and upheld it, and the counts of upheld "
            "and rejected flags are reported whichever way they come out.", "",
            f"- flags raised: **{summary['flags_raised']}** "
            f"({summary['unanimous']} unanimous, {summary['near_miss']} with one dissenter)",
            f"- of the unanimous, **{summary['strict']}** also clear the run floor: every "
            f"configuration held its answer on at least {summary['run_floor']} of its 20 runs. "
            f"Across the flags the weakest configuration's own support ranges from "
            f"{summary['weakest_support']} to {summary['weakest_support_max']} runs. The rest "
            f"are listed too, marked, because agreement between configurations that each barely "
            f"preferred their answer is the weaker claim and the author needs to see which is "
            f"which.",
            f"- tasks touched: {summary['leaves_touched']}",
            (f"- flags upheld: **{verdicts.count('upheld')}**" if settled else
             "- flags upheld: _to be completed by the author_"),
            (f"- flags rejected: **{verdicts.count('rejected')}**" if settled else
             "- flags rejected: _to be completed by the author_"),
            *([f"- flags excluded: **{verdicts.count('excluded')}**"] if settled else []), ""]


def write_review(rows: List[Dict[str, Any]], summary: Dict[str, Any], out_dir: Path,
                 n_models: int, held: dict = None) -> Path:
    """The author-facing document. One section per flag, each carrying the source URL and the
    stored quote, because adjudicating a label means reading the source, and a worklist that makes
    the reviewer go and find the document is a worklist that does not get used."""
    held = held or {}
    verdicts = [held.get((r["leaf"], r["item"]), {}).get("adjudication", "").strip()
                for r in rows]
    settled = bool(rows) and all(verdicts)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "REVIEW_oracle_flags.md"
    lines = _review_header(summary, n_models, verdicts, settled)
    for i, r in enumerate(rows, 1):
        kind = "unanimous" if r["unanimous"] else f"{r['n_agree']}/{r['n_models']}"
        lines += [f"## {i}. `{r['leaf']}` / `{r['item']}` ({kind})", "",
                  f"- models say: **{r['consensus_answer']}**",
                  f"- oracle says: **{r['oracle']}**",
                  f"- runs backing the models' answer: {r['runs_backing']} of {r['runs_total']} "
                  f"({r['support']:.1%})",
                  f"- source: {r['url'] or '_no URL recorded_'}",
                  f"- stored validating quote: {r['quote'] or '_none_'}",
                  *_verdict_lines(r, held)]
    path.write_text("\n".join(lines))
    return path


def main() -> Dict[str, Any]:
    print(OF.selftest())
    res = build()
    out = config.out_paths()["out"] / "annotation"
    out.mkdir(parents=True, exist_ok=True)
    T.write_csv(out / "oracle_flags.csv", list(COLS),
                [[r[c] for c in COLS] for r in res["rows"]])
    # Same rows, two views. The diagnostic dump above keeps every column the computation produced;
    # this is the sheet the author fills in. Written from ONE `res["rows"]` so the two files cannot
    # come to disagree about how many flags there are.
    flags = out / "model_flags.csv"
    held = carried_verdicts(flags)
    fresh = {(r["leaf"], r["item"]) for r in res["rows"]}
    orphaned = sorted(set(held) - fresh)
    if orphaned:
        raise SystemExit(f"{len(orphaned)} adjudicated flags are no longer raised by this run: "
                         f"{orphaned[:5]} -- refusing to write a worklist that would drop a "
                         "verdict the author cannot reproduce. Reconcile by hand.")
    T.write_csv(flags, list(FLAG_COLS) + list(ADJUDICATION),
                [[r[c] for c in FLAG_COLS]
                 + [held.get((r["leaf"], r["item"]), {}).get(c, "") for c in ADJUDICATION]
                 for r in res["rows"]])
    if held:
        print(f"  carried {len(held)} author verdict(s) forward into model_flags.csv")
    path = write_review(res["rows"], res["summary"], out, res["n_models"], held)
    s = res["summary"]
    print(f"  flags raised: {s['flags_raised']} ({s['unanimous']} unanimous, "
          f"{s['near_miss']} near-miss; {s['strict']} strict at the "
          f"{s['run_floor']}/20 run floor) across {s['leaves_touched']} tasks")
    for r in res["rows"][:12]:
        print(f"    {r['leaf'][:26]:26s} {r['item'][:22]:22s} "
              f"models={str(r['consensus_answer'])[:18]:18s} "
              f"oracle={str(r['oracle'])[:18]:18s} {r['runs_backing']:4d} runs "
              f"({'unanimous' if r['unanimous'] else str(r['n_agree']) + '/' + str(r['n_models'])})")
    print(f"  written: {path}")
    return res


if __name__ == "__main__":
    main()
