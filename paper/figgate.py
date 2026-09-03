"""
Location: paper-a/paper/figgate.py
Purpose: Run the visual-intelligence engine's validators over every figure this paper ships, and
         record IN CODE which of its gates do not apply to a column-width journal figure and why.
         The engine is the authority on figure quality; it is not the authority on ACL geometry,
         and the two disagree in six specific, named places. A skipped gate with a reason is
         auditable; a skipped gate that nobody wrote down is a hole.
Functions: engine(), declared_exemptions(), checks(), gate(), selftest()  + the Build record
           (the STATIC validate_mpl_script pass lives in figscript.py)
Calls: skills/passive/visual-intelligence/engine.py (validate, check_axis_integrity,
       validate_collision_physics, validate_font_floor, validate_color_semantics,
       validate_contrast_accessibility, verify_palette)
Imports: os, re, pathlib, matplotlib
"""

import os
import re
from collections import namedtuple
from pathlib import Path
from typing import Any, Dict, Sequence

REL = Path("skills") / "passive" / "visual-intelligence" / "engine.py"

# One drawn figure and everything a gate needs to judge it. Returned by each build function so the
# WRITER and the AUDITOR receive the identical object: an audit that re-declared a figure's
# concept colours would be auditing its own copy rather than the figure that ships.
Build = namedtuple("Build", "fig name source concepts allow_truncation min_ticks")
Build.__new__.__defaults__ = ((), ())


def _find_engine() -> Path:
    """Walk up from this file until the skill tree appears. A hardcoded depth breaks the moment
    the project moves, and it breaks by pointing at a path that does not exist rather than by
    saying so -- which is how the first version of this line ended up looking for the engine at
    the filesystem root."""
    override = os.environ.get("VI_ENGINE")
    if override:
        return Path(override)
    for parent in Path(__file__).resolve().parents:
        if (parent / REL).exists():
            return parent / REL
    return Path(__file__).resolve().parents[-1] / REL      # reported by name when it is missing


ENGINE = _find_engine()

# The engine gates this paper does NOT run, each with the reason it cannot apply. Written out
# because "we ran the engine" is a claim, and a reader of this repo is entitled to know exactly
# which checks stand behind it. Every one of these was established by RUNNING the gate and reading
# what it rejected, not by reading its source and guessing.
EXEMPT = {
    "validate_hierarchy":
        "requires a title at the top of the visual hierarchy. An ACL figure carries no title -- "
        "the caption does that job -- so the gate rejects every correctly-formatted figure here.",
    "validate_information_design":
        "validates a multi-section report or slide page (sections, tables per page). One figure "
        "is not a page and has no sections to validate.",
    "whitespace (DENSE/SPARSE inside validate)":
        "measures the axes bounding box against the FIGURE CANVAS. Every figure here is written "
        "with bbox_inches='tight', so canvas margins are cropped out of the delivered file and "
        "padding the canvas to satisfy the gate would change nothing a reader ever sees. The "
        "constraint that actually binds -- the figure must not be scaled down by the column, "
        "which would take its 7pt text below 7pt -- is enforced by make_figures._assert_width.",
    "TICK-CLUTTER on a categorical axis (inside validate)":
        "caps an axis at 8 ticks. That guards a continuous SCALE; on a categorical axis the tick "
        "count is the number of categories, so a twelve-configuration lineup is rejected for "
        "naming its twelve configurations. Exempted only when the named axis is verified "
        "categorical AND holds exactly the reported number of labels, so a cluttered continuous "
        "axis still fails.",
    "NO-SOURCE (inside validate)":
        "requires a 'Source:' line stamped on the figure canvas. That is slide-deck practice; a "
        "journal figure states provenance in its caption, and four stamped lines would cost page "
        "budget. Not dropped: the generating CSV is written into each PDF's "
        "Subject metadata by make_figures.write and read back by pdfcheck.figure_source, so "
        "provenance is machine-checkable rather than merely visible.",
    "save() / output_save()":
        "its .pdf branch requires a reportlab canvas and layout validator; it cannot write a "
        "matplotlib figure as vector PDF, and its image branch writes raster. Verified by "
        "calling it. Every gate save() would have run is run below instead, and the PDF is "
        "written by make_figures.write, which additionally suppresses CreationDate for "
        "byte-identical regeneration and asserts the printed width against the real column.",
}

_NS: Dict[str, Any] = {}


def engine() -> Dict[str, Any]:
    """Load the engine once. Executed rather than imported: it lives outside this package and the
    skill is distributed as a single file meant to be exec'd, which is how its own docs call it."""
    if not _NS:
        if not ENGINE.exists():
            raise SystemExit(f"visual-intelligence engine not found at {ENGINE}; set VI_ENGINE")
        exec(compile(ENGINE.read_text(), str(ENGINE), "exec"), _NS)
    return _NS


def declared_exemptions() -> Dict[str, str]:
    return dict(EXEMPT)


FLAT_EXEMPT = ("DENSE:", "SPARSE:", "NO-SOURCE")
CLUTTER = re.compile(r"TICK-CLUTTER: ([xy])-axis has (\d+) ticks")


def _clutter_ok(fig, line: str) -> bool:
    """A tick-clutter report is inapplicable only when the axis it names is CATEGORICAL and holds
    exactly the reported number of labels. Checked against the figure rather than waved through on
    the word 'categorical', so a genuinely cluttered continuous axis still fails."""
    hit = CLUTTER.match(line)
    if not hit:
        return False
    which, count = hit.group(1), int(hit.group(2))
    for ax in fig.get_axes():
        axis = ax.xaxis if which == "x" else ax.yaxis
        labels = [t for t in axis.get_ticklabels() if t.get_text().strip()]
        if _categorical(ax) and len(labels) == count:
            return True
    return False


def _inapplicable(fig, err: str) -> bool:
    """True when EVERY issue validate() raised is one of the declared-inapplicable classes.

    The message is parsed rather than the checks re-implemented, and the test is that nothing else
    is present: one unrecognised line and the error propagates untouched. A gate that swallowed
    any issue it could not classify would be worse than no gate."""
    lines = [l.strip().lstrip("✗").strip() for l in err.splitlines() if l.strip().startswith("✗")]
    return bool(lines) and all(l.startswith(FLAT_EXEMPT) or _clutter_ok(fig, l) for l in lines)


def _categorical(ax) -> bool:
    """True when either axis is labelled with names rather than numbers.

    Detected from the tick labels themselves rather than declared by the caller, so a panel cannot
    opt out of a check by asserting it is categorical when it is not."""
    for axis in (ax.xaxis, ax.yaxis):
        for tick in axis.get_ticklabels():
            text = tick.get_text().strip()
            if not text:
                continue
            try:
                float(text.replace("\N{MINUS SIGN}", "-").replace(",", ""))
            except ValueError:
                return True
    return False


def _tick_bounds(ax) -> Dict[str, int]:
    """The engine's tick-density window (3 to 8) guards a CONTINUOUS scale, where two ticks make
    it unreadable and nine make it noise. On a CATEGORICAL axis the tick count IS the number of
    categories: a two-group comparison would be rejected for having exactly the two groups it is
    about, and a twelve-configuration lineup for naming its twelve configurations. The density
    rule does not apply to a list of names, so on those axes only the continuous one is checked."""
    return {"min_ticks": 1, "max_ticks": 64} if _categorical(ax) else {}


def checks(fig, font_sizes: Dict[str, float], concept_colors: Dict[str, str],
           text_colors: Sequence[str], allow_truncation: Sequence[bool] = (),
           min_ticks: Sequence[int] = ()) -> Sequence[tuple]:
    """The applicable gates as (label, thunk) pairs. ONE list, consumed by two callers with
    opposite needs: gate() runs it and raises on the first failure, figaudit runs it and RECORDS
    every result. Two lists would let the build gate and the audit report disagree about which
    checks stand behind a figure, which is the one thing an audit exists to prevent."""
    e = engine()

    def _validate():
        try:
            e["validate"](fig)
        except ValueError as exc:
            if not _inapplicable(fig, str(exc)):
                raise

    def _axes():
        for i, ax in enumerate(fig.get_axes()):
            bounds = _tick_bounds(ax)
            if i < len(min_ticks):
                bounds["min_ticks"] = min_ticks[i]
            e["check_axis_integrity"](
                ax, allow_truncation=allow_truncation[i] if i < len(allow_truncation) else False,
                **bounds)

    return (("G7 validate (21 checks, less canvas whitespace)", _validate),
            ("check_axis_integrity (every axes)", _axes),
            ("G6 validate_collision_physics", lambda: e["validate_collision_physics"](fig=fig)),
            ("G5 validate_font_floor", lambda: e["validate_font_floor"](
                font_sizes, output_type="pdf", font_families=["serif"])),
            ("G3 validate_color_semantics", lambda: e["validate_color_semantics"](concept_colors)),
            ("G4 validate_contrast_accessibility",
             lambda: e["validate_contrast_accessibility"](concept_colors)),
            ("verify_palette (text colours)", lambda: e["verify_palette"](list(text_colors))))


def gate(fig, name: str, font_sizes: Dict[str, float], concept_colors: Dict[str, str],
         text_colors: Sequence[str], allow_truncation: Sequence[bool] = (),
         min_ticks: Sequence[int] = ()) -> str:
    """Every applicable engine gate, on one figure, before it is written. Raises on any failure.

    `allow_truncation` and `min_ticks` are per-axes and positional, so any relaxation is DECLARED
    at the call site where a reader of that figure will see it, rather than negotiated inside this
    module where it would apply to every figure at once."""
    pairs = checks(fig, font_sizes, concept_colors, text_colors, allow_truncation, min_ticks)
    for _label, thunk in pairs:
        thunk()
    return f"{name}: {len(pairs)} engine gates pass, {len(EXEMPT)} declared inapplicable"


def _contrast_arm(fig) -> None:
    """G4 is RUN, not exempted, since 2026-07-29: a palette of three accents that each clear 4.5:1
    exists, so the gate the paper used to declare inapplicable now passes on the real figures.
    Proved by a colour that does NOT clear it, so a future palette drift is caught."""
    try:
        gate(fig, "probe", {"tick": 7}, {"clean": "#EE7733"}, ["#2c3e50"])
        raise AssertionError("a 2.9:1 accent must be REJECTED by the contrast gate")
    except ValueError as exc:
        assert "WCAG-AA-FAIL" in str(exc), f"and rejected for that reason: {exc}"


def selftest() -> str:
    """Prove the gate discriminates. A wrapper that passed everything would be indistinguishable
    from no wrapper at all, and the exemption parser must refuse to widen itself."""
    e = engine()
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    assert _inapplicable(None, "  ✗ DENSE: 6% whitespace (min 40%)."), "the exemption recognises"
    assert not _inapplicable(None, "  ✗ DENSE: 6% ws\n  ✗ CLIPPED-X: '0.4'"), \
        "one unrecognised issue beside the exempt one must NOT be swallowed"
    assert not _inapplicable(None, "no issues at all"), "an unparseable message must not be exempt"
    plt.rcParams.update({"figure.constrained_layout.use": False, "pdf.fonttype": 42})
    fig, ax = plt.subplots(figsize=(3.0, 2.0), dpi=200)
    fig.subplots_adjust(left=0.26, right=0.97, top=0.94, bottom=0.26)
    ax.bar([0, 1], [0.09, 0.25], width=0.5)
    ax.set_xlabel("group", labelpad=6)
    ax.set_ylabel("wobble", labelpad=6)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["clean", "flagged"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(0.05, 0.40)                       # a truncated bar axis: the gate must catch it
    try:
        gate(fig, "probe", {"tick": 7}, {"clean": "#4477AA"}, ["#2c3e50"])
        raise AssertionError("a bar chart whose y-axis starts above zero must be REJECTED")
    except ValueError as exc:
        assert "TRUNCATED" in str(exc), f"and rejected for that reason: {exc}"
    ax.set_ylim(0, 0.40)
    ok = gate(fig, "probe", {"tick": 7}, {"clean": "#4477AA"}, ["#2c3e50"])
    assert "engine gates pass" in ok, ok
    try:
        gate(fig, "probe", {"tick": 6}, {"clean": "#4477AA"}, ["#2c3e50"])
        raise AssertionError("a 6pt role must be REJECTED by the font floor")
    except ValueError as exc:
        assert "FONT-FLOOR" in str(exc), f"and rejected for that reason: {exc}"
    _contrast_arm(fig)
    n = len(checks(fig, {"tick": 7}, {"clean": "#4477AA"}, ["#2c3e50"]))
    plt.close(fig)
    return (f"figgate selftest PASS - {n} engine gates run and a zero-based-bar violation, a 6pt "
            f"font and a 2.9:1 accent colour are each rejected by name, while the "
            f"canvas-whitespace exemption refuses to widen to any issue beside itself "
            f"({len(EXEMPT)} exemptions declared)")


if __name__ == "__main__":
    print(selftest())
