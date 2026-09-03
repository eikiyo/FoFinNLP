"""
Location: paper-a/analysis/config.py
Purpose: The ONE place Paper A's analysis declares where the frozen data lives, which ARM it may
         read, and every pre-registered constant. Nothing downstream hardcodes a path, a
         temperature, or a threshold.
Functions: probity_root(), out_paths(), aggregate_module(), serving_paths(), assert_arm_clean()
Calls: reads probity/results/aggregate.py + probity/engine/preflight.py -- READ ONLY.
Imports: importlib, os, sys, pathlib, typing
"""

import importlib.util
import os
import sys
from pathlib import Path
from typing import Dict

# --- HARD SCOPE (brief section 2) -------------------------------------------------------------
# The published temperature-0.7 arm is the LEGACY, UNSUFFIXED namespace, represented inside the
# benchmark by the sentinel `None` (engine/coverage.py: artifact_suffix / scored_filename).
# The literal float 0.7 selects `scored_t07.json`, a DIFFERENT 2-model Kaggle control. ARM is the
# only knob and it is deliberately not settable from the command line.
ARM = None
ARM_HUMAN = "legacy (temperature 0.7)"
FORBIDDEN_MARKERS = ("_t01", "scored_t07", "runs_t07", "manifest_t07")

# --- Pre-registered constants (brief 5a, 5e, 4c) ----------------------------------------------
TIE_THRESHOLD = 0.80
N_PERMUTATIONS = 1000
PERM_SEED = 20260728
TOP_K = 10

PAPER_ROOT = Path(__file__).resolve().parent.parent


def probity_root() -> Path:
    """Where the frozen v1.3.1 benchmark lives. Asserted, so a wrong path fails loudly instead of
    producing a confidently empty analysis."""
    root = Path(os.environ.get("PROBITY_ROOT", Path.home() / "probity")).expanduser()
    if not (root / "engine" / "registry.json").exists():
        raise SystemExit(f"PROBITY_ROOT is not the probity repo: {root}")
    return root


def out_paths() -> Dict[str, Path]:
    out = PAPER_ROOT / "out"
    paths = {"out": out, "tables": out / "tables", "figures": out / "figures"}
    for p in paths.values():
        p.mkdir(parents=True, exist_ok=True)
    return paths


def aggregate_module():
    """Import the benchmark's OWN reduction rather than re-deriving leaf paths, field keys and the
    measurability rule by hand -- re-deriving those is a logged failure in this project
    (2026-07-27: a guessed field key gave 0.00%, a doubled path gave ZeroDivisionError)."""
    root = probity_root()
    if str(root / "results") not in sys.path:
        sys.path.insert(0, str(root / "results"))
    spec = importlib.util.spec_from_file_location("probity_aggregate",
                                                  root / "results" / "aggregate.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def assert_arm_clean(paths) -> None:
    """Fail closed if any path this pipeline touched belongs to an excluded arm. A scope rule that
    is only stated in prose is not enforced (guardrail: structure enforces, prose rots)."""
    bad = [str(p) for p in paths if any(m in str(p) for m in FORBIDDEN_MARKERS)]
    if bad:
        raise SystemExit("SCOPE VIOLATION: excluded-arm files opened:\n  " + "\n  ".join(bad))


def _parse_lineup_block(text: str) -> Dict[str, str]:
    bucket = {"ollama": "local", "deepseek": "direct", "anthropic": "direct",
              "gemini": "direct", "openrouter": "routed"}
    block = text.split("LINEUP = [", 1)[1].split("]", 1)[0]
    out: Dict[str, str] = {}
    for line in block.splitlines():
        parts = [p.strip().strip('"') for p in line.strip().rstrip(",").strip("()").split(",")]
        if len(parts) == 3 and parts[0] and parts[1] in bucket:
            out[parts[0]] = bucket[parts[1]]
    return out


def serving_paths() -> Dict[str, str]:
    """
    label -> local | direct | routed, parsed from engine/preflight.py's LINEUP, which the repo
    documents as "the ONE place the label -> (client, model id) mapping is written down".

    NOT inferred from the `-or` filename suffix (a naming convention is not evidence), and NOT read
    from the t01 manifests' recorded `routing` field -- those belong to the excluded arm.
    """
    out = _parse_lineup_block((probity_root() / "engine" / "preflight.py").read_text())
    if not out:
        raise SystemExit("could not parse preflight.LINEUP -- refusing to guess a routing label")
    return out


def model_families() -> Dict[str, str]:
    """label -> model FAMILY, taken from LINEUP's model id rather than from the label.

    The family is the model id's first two hyphen-separated tokens, so `deepseek-v4-flash` and
    `deepseek-v4-pro` share `deepseek-v4`. Needed by the serving-path split: two members of one
    family agreeing is a statement about the family, not about the serving layer, and with only
    three direct-served configurations a single same-family pair would carry that comparison.
    The client field is NOT usable for this -- it is the API a call goes through, so every routed
    model shares the value `openrouter` while being entirely unrelated models."""
    text = (probity_root() / "engine" / "preflight.py").read_text()
    block = text.split("LINEUP = [", 1)[1].split("]", 1)[0]
    out: Dict[str, str] = {}
    for line in block.splitlines():
        parts = [p.strip().strip('"') for p in line.strip().rstrip(",").strip("()").split(",")]
        if len(parts) == 3 and parts[0] and parts[2]:
            # An ollama id names its quantization after a colon (`gemma3:1b`, `gemma3:1b-it`), so
            # the family is everything before it. A hosted id names the variant with hyphens
            # (`deepseek-v4-flash`, `deepseek-v4-pro`), so the family is its first two tokens.
            # One rule for both shapes would call two quantizations of one model two families.
            mid = parts[2]
            out[parts[0]] = (mid.split(":", 1)[0] if ":" in mid
                             else "-".join(mid.split("-")[:2]))
    if not out:
        raise SystemExit("could not parse model ids from preflight.LINEUP -- refusing to guess "
                         "a family from the label, which is a naming convention, not evidence")
    return out
