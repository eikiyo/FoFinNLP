"""
Location: paper-a/analysis/oracle_flags.py
Purpose: BLOCK 3a. Where EVERY configuration's modal answer agrees with every other and differs
         from the oracle, the oracle is the outlier and the label is a candidate error. The models
         FLAG; they do not decide. Nothing here rewrites a label, and the output is a worklist for
         the author to adjudicate against the source document, which is why it carries the source
         URL and the window rather than only a verdict.
Functions: item_view(), consensus(), flag_rows(), summarise(), selftest()
Calls: none (pure over fold.per_cell + the audit's corpus index)
Imports: typing
"""

from typing import Any, Dict, List, Optional, Sequence

# A flag needs every configuration to agree. Reported alongside is the NEAR-unanimous set, one
# dissenter allowed, because a single outlier configuration is a weak reason to keep a label the
# other eleven reject -- but it is a different, weaker claim and is never merged into the first.
NEAR_MISS_DISSENT = 1
# Agreement between two configurations that each barely preferred their answer is agreement
# between two coin flips. The strict claim additionally requires every configuration to hold its
# modal answer on at least this many of its runs. Carried as a COLUMN rather than as a filter:
# dropping the rows below the floor would hide, from the author reviewing the worklist, exactly
# the items where the models are least entitled to be believed.
RUN_FLOOR = 18


def item_view(models: Sequence[str], name: str, idx: int, per_cell) -> Optional[Dict[str, Any]]:
    """Every configuration's modal answer for one item, or None when any configuration could not
    measure it. An item one configuration never answered cannot support a UNANIMITY claim, and
    scoring it over the eleven that did would let the missing one be counted as agreeing."""
    out = {}
    for m in models:
        hit = next((i for i in per_cell[m][name] if i["item"] == idx), None)
        if hit is None or hit["flipped"] is None or hit.get("modal") is None:
            return None
        out[m] = {"modal": hit["modal"], "modal_n": hit["modal_n"], "n": hit["n"],
                  "majority": hit["majority"], "truth": hit.get("truth")}
    return out


def consensus(view: Dict[str, Any]) -> Dict[str, Any]:
    """How far the configurations agree with each other, and how far they differ from the oracle.

    Both halves are needed and neither implies the other: twelve models can all be wrong in twelve
    different ways (a hard item, not a label error) or all be right while the oracle is wrong (a
    label error). Only the second is a flag."""
    modals = [v["modal"] for v in view.values()]
    truth = next(iter(view.values()))["truth"]
    counts: Dict[Any, int] = {}
    for m in modals:
        counts[m] = counts.get(m, 0) + 1
    winner, n_agree = max(counts.items(), key=lambda kv: kv[1])
    return {"consensus_answer": winner, "n_agree": n_agree, "n_models": len(modals),
            "n_dissent": len(modals) - n_agree, "oracle": truth,
            "differs_from_oracle": winner != truth,
            # Total runs backing the consensus answer, across the configurations that hold it.
            # This is the ranking key: a label rejected by twelve models at 20 runs each is a
            # stronger candidate than one rejected by twelve models that each barely preferred it.
            "runs_backing": sum(v["modal_n"] for v in view.values() if v["modal"] == winner),
            "runs_total": sum(v["n"] for v in view.values()),
            # The WEAKEST configuration's own conviction. A unanimity in which one configuration
            # split 11/20 is a different object from one in which all twelve went 20/20, and the
            # minimum is the only summary that cannot be inflated by the other eleven.
            "min_modal_n": min(v["modal_n"] for v in view.values()),
            "min_runs": min(v["n"] for v in view.values())}


def flag_rows(models: Sequence[str], names: Sequence[str], per_cell, ids: Dict[str, List[str]],
              index) -> List[Dict[str, Any]]:
    """Every item where the configurations agree with each other and differ from the oracle,
    ranked by the runs backing their answer. Near-misses are included and LABELLED, never merged:
    the strict claim and the weaker one must stay separable in the output the author works from."""
    rows = []
    for name in names:
        for idx, iid in enumerate(ids.get(name, [])):
            view = item_view(models, name, idx, per_cell)
            if view is None:
                continue
            c = consensus(view)
            if not c["differs_from_oracle"] or c["n_dissent"] > NEAR_MISS_DISSENT:
                continue
            rows.append({"leaf": name, "item": iid,
                         "unanimous": c["n_dissent"] == 0,
                         "consensus_answer": c["consensus_answer"], "oracle": c["oracle"],
                         "n_agree": c["n_agree"], "n_models": c["n_models"],
                         "runs_backing": c["runs_backing"], "runs_total": c["runs_total"],
                         "support": c["runs_backing"] / c["runs_total"] if c["runs_total"] else 0,
                         "min_modal_n": c["min_modal_n"], "min_runs": c["min_runs"],
                         "meets_run_floor": c["min_modal_n"] >= RUN_FLOOR,
                         "strict": c["n_dissent"] == 0 and c["min_modal_n"] >= RUN_FLOOR,
                         "url": index["url"].get((name, iid), ""),
                         "quote": (index["quote"].get((name, iid), "") or "")[:200]})
    return sorted(rows, key=lambda r: (-int(r["unanimous"]), -r["runs_backing"]))


def summarise(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Counts the author's review is measured against. `upheld` and `rejected` stay absent until a
    human fills them: a flag is a question, and reporting a raised flag as a found error would be
    exactly the substitution of a model for an annotator that section 2 argues against."""
    return {"flags_raised": len(rows),
            "unanimous": sum(1 for r in rows if r["unanimous"]),
            "near_miss": sum(1 for r in rows if not r["unanimous"]),
            "strict": sum(1 for r in rows if r["strict"]),
            "run_floor": RUN_FLOOR,
            # Why the strict count came out as it did, in the rows' own numbers. A criterion that
            # admits nothing is a result, and reporting it as a bare zero invites the reader to
            # assume a bug; the range of weakest-configuration support says what actually
            # happened, and it is read off the rows rather than described from memory.
            "weakest_support": min((r["min_modal_n"] for r in rows), default=None),
            "weakest_support_max": max((r["min_modal_n"] for r in rows), default=None),
            "leaves_touched": len({r["leaf"] for r in rows})}


def _view(*specs):
    """Build a per_cell fixture from (modal, modal_n, truth) triples, one per configuration."""
    per_cell, models = {}, []
    for i, (modal, modal_n, truth) in enumerate(specs):
        m = f"m{i}"
        models.append(m)
        per_cell[m] = {"L": [{"item": 0, "flipped": modal_n < 20, "modal": modal,
                              "modal_n": modal_n, "n": 20, "truth": truth,
                              "majority": modal == truth}]}
    return models, per_cell


def selftest() -> str:
    """Prove the flag fires ONLY on the case it claims, and stays silent on the two that resemble
    it. A reviewer's first question is whether this is just 'items the models get wrong'."""
    models, pc = _view(("B", 20, "A"), ("B", 19, "A"), ("B", 18, "A"))
    c = consensus(item_view(models, "L", 0, pc))
    assert c["differs_from_oracle"] and c["n_dissent"] == 0 and c["runs_backing"] == 57, c
    idx0 = {"url": {}, "quote": {}}
    at_floor = flag_rows(models, ["L"], pc, {"L": ["i0"]}, idx0)[0]
    assert at_floor["min_modal_n"] == RUN_FLOOR and at_floor["strict"], \
        f"a unanimity whose weakest configuration sits exactly at the floor is strict: {at_floor}"

    # One configuration BELOW the run floor. Still unanimous, no longer strict, and still
    # REPORTED -- the floor is a column the author reads, never a silent filter.
    models, pc = _view(("B", 20, "A"), ("B", 19, "A"), ("B", 17, "A"))
    weak = flag_rows(models, ["L"], pc, {"L": ["i0"]}, idx0)
    assert len(weak) == 1 and weak[0]["unanimous"] and not weak[0]["strict"], \
        f"a sub-floor unanimity must be reported and marked not-strict: {weak}"
    assert summarise(weak)["strict"] == 0 and summarise(weak)["unanimous"] == 1, \
        "the strict count and the unanimous count must be able to disagree, or the floor is inert"

    # All three wrong but in DIFFERENT directions: a hard item, NOT a label error. Must not flag.
    models, pc = _view(("B", 20, "A"), ("C", 19, "A"), ("D", 18, "A"))
    c2 = consensus(item_view(models, "L", 0, pc))
    assert c2["n_dissent"] == 2, \
        f"three different wrong answers must show dissent, not unanimity: {c2}"
    idx = {"url": {}, "quote": {}}
    assert flag_rows(models, ["L"], pc, {"L": ["i0"]}, idx) == [], \
        "models disagreeing with each other must NOT be reported as an oracle error"

    # All three AGREE WITH the oracle: nothing to flag.
    models, pc = _view(("A", 20, "A"), ("A", 19, "A"), ("A", 18, "A"))
    assert flag_rows(models, ["L"], pc, {"L": ["i0"]}, idx) == [], \
        "agreement WITH the oracle is not a flag"

    # One configuration could not measure the item: unanimity is unclaimable, so no row.
    models, pc = _view(("B", 20, "A"), ("B", 19, "A"), ("B", 18, "A"))
    pc["m2"]["L"][0]["flipped"] = None
    assert item_view(models, "L", 0, pc) is None, \
        "an unmeasured configuration must void the item, never be counted as agreeing"
    assert flag_rows(models, ["L"], pc, {"L": ["i0"]}, idx) == [], "and it must produce no row"

    # A near miss is reported but LABELLED, and sorts below a unanimous flag.
    models, pc = _view(("B", 20, "A"), ("B", 20, "A"), ("C", 20, "A"))
    near = flag_rows(models, ["L"], pc, {"L": ["i0"]}, idx)
    assert len(near) == 1 and near[0]["unanimous"] is False and near[0]["n_agree"] == 2, near
    s = summarise(near)
    assert s["near_miss"] == 1 and s["unanimous"] == 0 and "upheld" not in s, \
        f"a raised flag must never be counted as a confirmed error: {s}"
    return ("oracle_flags selftest PASS - a unanimous disagreement with the oracle flags with its "
            "backing run count, three DIFFERENT wrong answers do not, agreement with the oracle "
            "does not, an unmeasured configuration voids the item rather than counting as assent, "
            f"a unanimity whose weakest configuration falls below {RUN_FLOOR}/20 is reported but "
            "not counted as strict, and a near miss is reported separately and never as a "
            "confirmed error")
