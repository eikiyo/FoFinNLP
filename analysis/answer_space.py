"""
Location: paper-a/analysis/answer_space.py
Purpose: Brief 5f -- classify each leaf's answer space as binary | categorical | numeric |
         multi_part, MECHANICALLY from the leaf's own TASK["fields"] where the declared type
         decides it, and by NAMED judgement (with a justification and the real oracle values that
         support it) where it does not.
Functions: task_fields(), classify(), oracle_sample(), write_answer_types()
Calls: reads each leaf's task.py + oracle.jsonl (read-only)
Imports: importlib, json, pathlib, typing, config
"""

import importlib.util
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import config
import tables_out as T

# Leaves whose DECLARED field type (`date`, `string`) does not by itself fix a bucket. Each entry
# is a judgement call, recorded here so it is auditable rather than buried in a branch, and each
# justification cites what the leaf's real oracle values look like.
JUDGEMENT: Dict[str, Tuple[str, str]] = {
    "note_maturity_date": (
        "numeric",
        "declared type `date`; oracle values are single ISO dates (2005-03-31, 2026-12-31) -- one "
        "ordered scalar from an unbounded space, canonicalised by engine/normalize.py, so it "
        "behaves like a numeric extraction rather than a choice among options."),
    "exercise_window": (
        "numeric",
        "declared type `string`; oracle values are a single quantity with one unit "
        "(30/85/90/90/180 days) -- one ordered scalar, not a closed option set."),
    "form_d_fields": (
        "numeric",
        "registry says `string` but the leaf's own TASK field type is `number` and the oracle "
        "values are amounts (2,366,532 / 70,227,931.85); the field type is what the scorer "
        "dispatches on, so the field type wins."),
    "vesting_schedule": (
        "multi_part",
        "declared type `string`; every oracle value carries TWO components that must both be "
        "right (term and cliff: '4yr/1yr-cliff', '1.5yr/no-cliff')."),
    "s1_use_of_proceeds": (
        "multi_part",
        "declared type `string`; the answer is an open-vocabulary multi-word span scored as a "
        "unit ('working capital and general corporate purposes') -- no closed option set and no "
        "scalar, and the known failure mode is returning a longer correct-in-substance span."),
    "s1_risk_factors": (
        "multi_part",
        "declared type `string`; the answer is a sentence-length heading reproduced as a unit."),
}


def task_fields(leaf_rel: str, key: str) -> Dict[str, Any]:
    """The leaf's own declared field schema. Loaded from task.py because that is the object the
    runner and scorer dispatch on -- the registry's `type` column is a summary, not the contract."""
    path = config.probity_root() / leaf_rel / "task.py"
    spec = importlib.util.spec_from_file_location(f"probity_task_{key}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TASK["fields"]


def classify(leaf: Dict[str, Any]) -> Dict[str, Any]:
    """binary | categorical | numeric | multi_part for one leaf, plus how it was decided."""
    name = leaf["leaf"]
    fields = task_fields(leaf["rel"], name)
    if len(fields) > 1:
        return {"leaf": name, "answer_type": "multi_part", "basis": "mechanical",
                "justification": f"TASK declares {len(fields)} answer fields."}
    fname, spec = next(iter(fields.items()))
    ftype, values = spec.get("type"), spec.get("values")
    if ftype == "number":
        return {"leaf": name, "answer_type": "numeric", "basis": "mechanical",
                "justification": "TASK field type is `number`."}
    if ftype == "bool":
        return {"leaf": name, "answer_type": "binary", "basis": "mechanical",
                "justification": "TASK field type is `bool` (two states)."}
    if ftype == "enum" and values is not None:
        kind = "binary" if len(values) == 2 else "categorical"
        return {"leaf": name, "answer_type": kind, "basis": "mechanical",
                "justification": f"TASK field type is `enum` with {len(values)} declared values: "
                                 f"{', '.join(map(str, values))}."}
    if name in JUDGEMENT:
        kind, why = JUDGEMENT[name]
        return {"leaf": name, "answer_type": kind, "basis": "judgement", "justification": why}
    raise SystemExit(f"unclassifiable leaf {name} (field {fname}, type {ftype}) -- refusing to "
                     f"guess a bucket; add an explicit JUDGEMENT entry")


def oracle_sample(leaf: Dict[str, Any], k: int = 3) -> List[str]:
    """A few real oracle values, so a reader can check the label against the data, not the prose."""
    path = config.probity_root() / leaf["rel"] / "oracle.jsonl"
    out: List[str] = []
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        if not line.strip() or len(out) >= k:
            continue
        rec = json.loads(line)
        val = rec.get(leaf["field"], rec.get("truth", rec.get("answer")))
        out.append(str(val)[:70])
    return out


def write_answer_types(leaves: List[Dict[str, Any]], out_dir: Path) -> Tuple[Path, Dict[str, str]]:
    rows = [dict(classify(l), family=l["family"], field=l["field"],
                 sample=" · ".join(oracle_sample(l))) for l in leaves]
    counts: Dict[str, int] = {}
    for r in rows:
        counts[r["answer_type"]] = counts.get(r["answer_type"], 0) + 1
    lines = [
        "# Answer-space classification (brief 5f)",
        "",
        f"Arm: **{config.ARM_HUMAN}**. {len(rows)} leaves. "
        f"{sum(1 for r in rows if r['basis'] == 'mechanical')} classified mechanically from the "
        f"leaf's own `TASK[\"fields\"]`, {sum(1 for r in rows if r['basis'] == 'judgement')} by "
        "judgement (each justified below and re-listed in the report's question 10).",
        "",
        "Counts: " + " · ".join(f"**{k}** {v}" for k, v in sorted(counts.items())),
        "",
        T.md_table(["Leaf", "Family", "Answer type", "Basis", "Justification",
                    "Real oracle values"],
                   [[f"`{r['leaf']}`", r["family"], f"**{r['answer_type']}**", r["basis"],
                     r["justification"], r["sample"]]
                    for r in sorted(rows, key=lambda r: (r["answer_type"], r["leaf"]))]),
    ]
    path = out_dir / "answer_types.md"
    path.write_text("\n".join(lines) + "\n")
    return path, {r["leaf"]: r["answer_type"] for r in rows}
