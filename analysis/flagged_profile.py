"""
Location: paper-a/analysis/flagged_profile.py
Purpose: GAP 1. The repair null says windowing is not the mechanism, so this asks what flagged
         items actually ARE: are they simply harder (accuracy), what answer types and clause
         categories do they concentrate in, which tasks the exclusion removes outright, and
         whether "the answer is stated in the window" -- a mechanical property computed WITHOUT
         reference to the validating quote, and therefore independent of the audit's flag --
         tracks instability better than the flag does.
Functions: bucket(), item_rows(), rate(), contrast_rows(), composition(), lost_tasks(),
           repair_stated(), write_all(), selftest()
Calls: numparse.states, categories.wilson, contamination.newcombe, oracle_audit.corpus_index
Imports: csv, pathlib, typing, categories, config, contamination, numparse, oracle_audit,
         tables_out
"""

import csv
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

import categories as CAT
import config
import adjudication as ADJ
import contamination as C
import numparse
import oracle_audit as OA
import tables_out as T

STATED, NOT_STATED, UNDECIDABLE = "stated", "not-stated", "undecidable"


def bucket(stated: Optional[bool]) -> str:
    """Tri-state, never collapsed to a boolean. An undecidable item is one the instrument cannot
    read, and folding it into `not-stated` would score the instrument's blind spot as a finding
    about the corpus."""
    return UNDECIDABLE if stated is None else (STATED if stated else NOT_STATED)


def _measure(per_cell, models: Sequence[str], leaf: str, idx: int) -> Dict[str, Any]:
    """One item's totals across every configuration that measured it. A cell whose flip flag is
    None was never measurable and contributes to neither denominator. `disp` sums the graded
    dispersion (share of runs disagreeing with the modal answer) over the same measured cells, so
    a severity-sensitive rate can be reported on exactly the population binary wobble is."""
    out: Dict[str, Any] = {"pairs": 0, "flips": 0, "maj_n": 0, "maj_ok": 0, "disp": 0.0}
    for m in models:
        hit = next((i for i in per_cell[m][leaf] if i["item"] == idx), None)
        if hit is None or hit["flipped"] is None:
            continue
        out["pairs"] += 1
        out["flips"] += int(hit["flipped"])
        out["disp"] += hit.get("dispersion") or 0.0
        if hit.get("majority") is not None:
            out["maj_n"] += 1
            out["maj_ok"] += int(hit["majority"])
    return out


def item_rows(leaves: List[Dict[str, Any]], audit_rows: List[Dict[str, Any]], per_cell,
              models: Sequence[str], answer_types: Dict[str, str]) -> List[Dict[str, Any]]:
    """One row per item: what it is, whether the audit flagged it, whether its window states its
    answer, and its measured instability and accuracy. Every later table is a group-by over this,
    so a reader can re-derive any number in the section from one file."""
    index = OA.corpus_index()
    ids = C.oracle_ids(leaves)
    flagged = C.flagged_index(audit_rows)
    # Author-excluded items are out of THIS table too. It is the source every Section 2 rate is a
    # group-by over, and it built its own clean/flagged split rather than going through
    # contamination.keep_sets: for one run it reported 434 clean items beside a bucket table
    # reporting 427, two artifacts describing the same population and disagreeing about its size.
    excluded = ADJ.exclusions()
    by_leaf = {l["leaf"]: l for l in leaves}
    rows = []
    for r in audit_rows:
        leaf, iid = r["leaf"], str(r["item"])
        meta = by_leaf.get(leaf)
        if meta is None or iid not in ids.get(leaf, []):
            continue
        if iid in excluded.get(leaf, set()):
            continue
        window = index["window"].get((leaf, iid), "")
        stated = numparse.states(r.get("answer"), window)
        rows.append({"leaf": leaf, "item": iid, "category": meta.get("family", ""),
                     "answer_type": answer_types.get(leaf, ""),
                     "field_type": meta.get("type", ""),
                     "flagged": int(iid in flagged.get(leaf, set())),
                     "bucket": bucket(stated),
                     "bucket_nowords": bucket(numparse.states(r.get("answer"), window,
                                                              words=False)),
                     **_measure(per_cell, models, leaf, ids[leaf].index(iid))})
    return rows


def rate(rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Wobble and majority accuracy over a set of items, each with its Wilson interval. Both are
    reported because "flagged items are simply harder" is the competing explanation the repair
    null leaves standing, and it is answered by accuracy, not by wobble."""
    pairs = sum(r["pairs"] for r in rows)
    flips = sum(r["flips"] for r in rows)
    maj_n = sum(r["maj_n"] for r in rows)
    maj_ok = sum(r["maj_ok"] for r in rows)
    disp = sum(r.get("disp", 0.0) for r in rows)
    w = CAT.wilson(flips, pairs) if pairs else None
    a = CAT.wilson(maj_ok, maj_n) if maj_n else None
    return {"items": len(rows), "pairs": pairs, "flips": flips,
            "wobble": (flips / pairs) if pairs else None,
            "w_lo": w[0] if w else None, "w_hi": w[1] if w else None,
            "dispersion": (disp / pairs) if pairs else None,
            "acc_n": maj_n, "accuracy": (maj_ok / maj_n) if maj_n else None,
            "a_lo": a[0] if a else None, "a_hi": a[1] if a else None}


def contrast_rows(rows: Sequence[Dict[str, Any]], key: Callable, label: str
                  ) -> List[Dict[str, Any]]:
    """Every value of one grouping, each against the rest of the corpus, on both measures.

    Against the COMPLEMENT rather than against a fixed reference group: a group compared only
    with the clean rate cannot show that it differs from the other groups, which is the whole
    question when two candidate mechanisms are on the table."""
    out = []
    for value in sorted({key(r) for r in rows}):
        inside = [r for r in rows if key(r) == value]
        outside = [r for r in rows if key(r) != value]
        a, b = rate(inside), rate(outside)
        out.append({"grouping": label, "group": value, **a,
                    "wobble_diff": C.newcombe(a["flips"], a["pairs"], b["flips"], b["pairs"]),
                    "acc_diff": C.newcombe(sum(r["maj_ok"] for r in inside), a["acc_n"],
                                           sum(r["maj_ok"] for r in outside), b["acc_n"])})
    return out


def composition(rows: Sequence[Dict[str, Any]], field: str) -> List[Dict[str, Any]]:
    """How the flagged population is composed, beside the corpus base rate for the same slice.
    A share of the flagged set means nothing on its own: a category holding a third of the flags
    and a third of the corpus is not concentrated, it is just large."""
    flagged = [r for r in rows if r["flagged"]]
    out = []
    for value in sorted({r[field] for r in rows}):
        n_all = sum(1 for r in rows if r[field] == value)
        n_flag = sum(1 for r in flagged if r[field] == value)
        out.append({"field": field, "value": value, "items": n_all, "flagged": n_flag,
                    "share_of_flagged": n_flag / len(flagged) if flagged else None,
                    "share_of_corpus": n_all / len(rows) if rows else None,
                    "flag_rate": n_flag / n_all if n_all else None})
    return out


def lost_tasks(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Tasks the exclusion removes entirely, because every one of their items is flagged. These
    are the corpus's own casualties and the brief asks whether they share a structure."""
    out = []
    for leaf in sorted({r["leaf"] for r in rows}):
        sub = [r for r in rows if r["leaf"] == leaf]
        if sub and all(r["flagged"] for r in sub):
            out.append({"leaf": leaf, "category": sub[0]["category"],
                        "answer_type": sub[0]["answer_type"], "items": len(sub),
                        **{k: rate(sub)[k] for k in ("wobble", "accuracy")}})
    return out


def repair_stated(leaves: List[Dict[str, Any]], manifest: Path, windows: Path
                  ) -> List[Dict[str, Any]]:
    """Did the re-windowing actually put the answer in front of the model?

    This is the check that decides how the null can be read. A repair that never achieved its
    mechanical objective would explain the null without saying anything about models; one that
    achieved it on every item it could says the model had the answer in view and still answered
    inconsistently. The question is not rhetorical and is answered per item, not asserted."""
    index = OA.corpus_index()
    by_leaf = {l["leaf"]: l for l in leaves}
    out = []
    for row in csv.DictReader(manifest.open()):
        if row.get("repaired") != "yes":
            continue
        leaf, iid = row["leaf"], row["item"]
        meta = by_leaf[leaf]
        item = next((i for i in OA.leaf_items(meta["rel"]) if str(i.get("id", "")) == iid), None)
        after = windows / leaf / f"{iid}.txt"
        answer = (item or {}).get(meta["field"])
        out.append({"leaf": leaf, "item": iid, "answer": answer,
                    "orig_len": row["orig_len"], "new_len": row["new_len"],
                    "before": numparse.states(answer, index["window"].get((leaf, iid), "")),
                    "after": numparse.states(answer,
                                             after.read_text(errors="ignore")
                                             if after.exists() else "")})
    return out


def _flat(row: Dict[str, Any], keys: Sequence[str]) -> List[Any]:
    """Newcombe returns a dict; a CSV cell holds one value. Flattened here rather than in every
    caller, so the column names in the file and the keys in the code cannot drift apart."""
    out = []
    for k in keys:
        v = row.get(k)
        if isinstance(v, dict):
            out.extend([v.get("d"), v.get("lo"), v.get("hi"), int(bool(v.get("excludes_zero")))])
        else:
            out.append(v)
    return out


RATE_COLS = ("grouping", "group", "items", "pairs", "flips", "wobble", "w_lo", "w_hi",
             "acc_n", "accuracy", "a_lo", "a_hi", "wobble_diff", "acc_diff")
RATE_HEAD = list(RATE_COLS[:-2]) + ["wobble_diff", "wobble_diff_lo", "wobble_diff_hi",
                                    "wobble_diff_excludes_zero", "acc_diff", "acc_diff_lo",
                                    "acc_diff_hi", "acc_diff_excludes_zero"]


def write_all(rows: List[Dict[str, Any]], leaves: List[Dict[str, Any]], tables: Path,
              out_dir: Path) -> Dict[str, Any]:
    """Five files, and the summary the paper's prose is written from."""
    T.write_csv(tables / "flagged_profile.csv", list(rows[0].keys()),
                [[r[k] for k in rows[0]] for r in rows])
    groups = (contrast_rows(rows, lambda r: "flagged" if r["flagged"] else "clean", "audit flag")
              + contrast_rows(rows, lambda r: r["bucket"], "answer stated in window")
              + contrast_rows(rows, lambda r: r["bucket_nowords"],
                              "answer stated in window (no spelled numerals)")
              + contrast_rows(rows, lambda r: f"{r['bucket']} / "
                              f"{'flagged' if r['flagged'] else 'clean'}", "crossed"))
    T.write_csv(tables / "flagged_rates.csv", RATE_HEAD,
                [_flat(g, RATE_COLS) for g in groups])
    comp = composition(rows, "answer_type") + composition(rows, "category")
    T.write_csv(tables / "flagged_composition.csv", list(comp[0].keys()),
                [[r[k] for k in comp[0]] for r in comp])
    lost = lost_tasks(rows)
    T.write_csv(tables / "lost_tasks.csv", list(lost[0].keys()) if lost else ["leaf"],
                [[r[k] for k in lost[0]] for r in lost])
    rep = repair_stated(leaves, tables / "repair_manifest.csv", out_dir / "repair" / "windows")
    T.write_csv(tables / "repair_stated.csv", list(rep[0].keys()) if rep else ["leaf"],
                [[r[k] for k in rep[0]] for r in rep])
    return {"rows": len(rows), "groups": groups, "composition": comp, "lost": lost,
            "repair": rep,
            "repair_before": sum(1 for r in rep if r["before"]),
            "repair_after": sum(1 for r in rep if r["after"]),
            "repair_decidable": sum(1 for r in rep if r["after"] is not None)}


def _fixture() -> List[Dict[str, Any]]:
    def row(leaf, flagged, b, pairs, flips, ok):
        return {"leaf": leaf, "item": f"{leaf}-{flagged}-{flips}", "category": "cat",
                "answer_type": "numeric", "field_type": "number", "flagged": flagged,
                "bucket": b, "bucket_nowords": b, "pairs": pairs, "flips": flips,
                "maj_n": pairs, "maj_ok": ok}
    return [row("a", 1, NOT_STATED, 10, 9, 2), row("a", 1, NOT_STATED, 10, 8, 3),
            row("b", 0, STATED, 10, 1, 9), row("b", 0, STATED, 10, 0, 10)]


def selftest() -> str:
    """Closed-form arithmetic, and the degenerate input that would make a grouping vacuous. A
    group-by whose key takes ONE value compares a set against an EMPTY complement, where every
    difference is undefined rather than zero, and reporting that as a finding scores the
    instrument instead of the data."""
    fx = _fixture()
    r = rate([x for x in fx if x["flagged"]])
    assert r["items"] == 2 and r["pairs"] == 20 and abs(r["wobble"] - 0.85) < 1e-12, r
    assert abs(r["accuracy"] - 0.25) < 1e-12, f"accuracy must be 5/20: {r['accuracy']}"
    con = contrast_rows(fx, lambda x: "flagged" if x["flagged"] else "clean", "flag")
    hit = next(c for c in con if c["group"] == "flagged")
    assert abs(hit["wobble_diff"]["d"] - 0.80) < 1e-12, hit["wobble_diff"]
    assert hit["wobble_diff"]["excludes_zero"], "a 0.85-vs-0.05 split must exclude zero"
    assert hit["acc_diff"]["d"] < 0, "the flagged fixture is LESS accurate; the sign must show it"
    one = contrast_rows(fx, lambda x: "same", "degenerate")
    assert len(one) == 1 and one[0]["wobble_diff"] is None, \
        "a single-valued grouping has an empty complement and must yield no difference, not zero"
    comp = composition(fx, "category")
    assert comp[0]["share_of_flagged"] == 1.0 and comp[0]["flag_rate"] == 0.5, comp
    assert [t["leaf"] for t in lost_tasks(fx)] == ["a"], "only the all-flagged task is lost"
    return ("flagged_profile selftest PASS - wobble and accuracy match closed form, the "
            "flagged-vs-clean contrast reproduces a known difference with the right sign and "
            "excludes zero, a single-valued grouping returns no difference instead of a spurious "
            "zero, composition separates share-of-flagged from base rate, and only a task whose "
            "every item is flagged counts as lost")


if __name__ == "__main__":
    print(selftest())
