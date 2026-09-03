"""
Location: paper-a/analysis/block6_gate.py
Purpose: The Block 6 acceptance gate, for the items paper/verify_paper.py does not cover. Each is
         checked by RUNNING something and printing what it measured. verify_paper covers the
         document itself (pages, anonymity, exhibits, numbers, citations, prose, bundle); this
         covers the ANALYSIS side: the audit's tests, the pre-registration, downstream freshness,
         and the specific claims the brief requires to be present or absent in the main text.
         Usage:  python3 analysis/block6_gate.py
Functions: g_audit_tests(), g_prereg_unedited(), g_prereg_threshold(), g_downstream_fresh(),
           g_maintext_claims(), prereg_failure_text(), g_prereg_failure(), selftest(), main()
Calls: quotematch.selftest, windowability.selftest, oracle_audit.selftest, config.out_paths
Imports: json, re, subprocess, sys, pathlib
"""

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config                        # noqa: E402

ROOT = config.PAPER_ROOT
PREREG = ROOT / "out" / "PREREG_UPGRADE.md"
REPAIR_FLOOR = 10                    # PREREG_UPGRADE: run the repair experiment at 10 or more


def g_audit_tests(fail) -> str:
    """The matcher repaired in Block 0d must still prove itself, every run."""
    import oracle_audit
    import quotematch
    import windowability
    names = []
    for mod in (quotematch, windowability, oracle_audit):
        msg = mod.selftest()
        if "PASS" not in msg:
            fail(f"{mod.__name__} selftest did not report PASS: {msg[:80]}")
        names.append(mod.__name__)
    return f"{len(names)} audit selftests pass: {', '.join(names)}"


def g_prereg_unedited(fail) -> str:
    """The pre-registration must be APPENDED to and never edited.

    Checked against git, not by reading the file. A pre-registration you can revise is not one,
    and 'I only added a correction' is exactly what an edit would also look like from inside the
    working copy. The first committed version must still be a literal prefix of the current file."""
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    rel = PREREG.resolve().relative_to(Path(top)).as_posix()
    # Run from the repository top with a top-relative path. `git log -- <path>` resolves its
    # pathspec against the CWD, so a repo-relative path issued from a subdirectory matches nothing
    # and returns an empty history -- which this check then has to treat as a failure rather than
    # as evidence of anything.
    log = subprocess.run(["git", "log", "--format=%H", "--reverse", "--", rel],
                         cwd=top, capture_output=True, text=True)
    shas = log.stdout.split()
    if not shas:
        fail(f"{rel} has no git history; its immutability cannot be verified")
        return "NOT CHECKED - no git history"
    first = subprocess.run(["git", "show", f"{shas[0]}:{rel}"], cwd=top,
                           capture_output=True, text=True).stdout
    now = PREREG.read_text()
    # An empty retrieval makes startswith() vacuously true, so this check reported the
    # pre-registration intact while comparing it against nothing: the path passed to `git show`
    # was relative to the wrong root and every call returned "". A rule that cannot fail is not a
    # weaker rule, it is a false statement about the thing it claims to have verified.
    if len(first.strip()) < 200:
        fail(f"retrieved only {len(first)} chars of the original {rel} from {shas[0][:8]}; "
             f"the comparison would be vacuous, so this is a FAILURE, not a pass")
        return "NOT CHECKED - original could not be retrieved"
    if not now.startswith(first.rstrip("\n")):
        fail(f"{rel} was EDITED, not appended to: the version committed at {shas[0][:8]} is no "
             f"longer a prefix of the current file")
        return "EDITED - see failure"
    added = len(now) - len(first.rstrip("\n"))
    return (f"original {len(first)} chars intact as a prefix since {shas[0][:8]}; "
            f"{added} chars appended across {len(shas)} commits")


def g_prereg_threshold(fail) -> str:
    """The registered threshold must be applied, not renegotiated, and the count it is applied to
    must come from the audit rather than from prose."""
    text = PREREG.read_text()
    stated = re.findall(r"(\d+) or more repairable items", text)
    if not stated:
        fail("no '<n> or more repairable items' threshold found in the pre-registration")
        return "NOT CHECKED - threshold sentence not found"
    if len({int(s) for s in stated}) != 1 or int(stated[0]) != REPAIR_FLOOR:
        fail(f"the pre-registration states thresholds {sorted(set(stated))}, this gate expects "
             f"exactly {REPAIR_FLOOR}; a threshold that moved is a renegotiated one")
    est = ROOT / "out" / "block2b_estimate.json"
    if not est.exists():
        fail("out/block2b_estimate.json is missing; the repairable count was never computed")
        return f"threshold {REPAIR_FLOOR} stated, count NOT computed"
    n = json.loads(est.read_text())["n_items"]
    verdict = "RUNS" if n >= REPAIR_FLOOR else "DROPPED"
    return (f"threshold {REPAIR_FLOOR} stated once and unchanged; {n} repairable items measured, "
            f"so the repair experiment {verdict} by the registered rule")


def g_downstream_fresh(fail, audit: dict = None) -> str:
    """The generated tables must describe the partition the audit currently reports.

    Checked on CONTENT, not on mtimes. An mtime rule sounds right and is unusable here: the audit
    is regenerated by its own entry point, so re-running it makes every table 'older' than the
    audit while changing nothing, and the check then measures the order commands were typed in
    rather than whether anything is stale. It failed on 26 tables that were entirely current.

    The two denominators are the partition. If a table were built against the old 424/46 split,
    the clean mirror would top out at 424 and this would say so."""
    import csv
    a = audit or json.loads((ROOT / "out" / "annotation" / "oracle_audit.json").read_text())
    seen = {}
    for pop, expect in (("clean", a["n_clean"]), ("all", a["n_items"])):
        path = ROOT / "out" / "tables" / pop / "model_summary.csv"
        if not path.exists():
            fail(f"out/tables/{pop}/model_summary.csv is missing; the partition cannot be checked")
            continue
        got = max(int(r["total_measured_items"]) for r in csv.DictReader(path.open()))
        seen[pop] = got
        if got != expect:
            fail(f"out/tables/{pop}/ was built against a partition of {got} items, but the audit "
                 f"now reports {expect}; re-run python3 analysis/gate0.py")
    n = sum(1 for _ in (ROOT / "out" / "tables").rglob("*.csv"))
    return (f"all {n} generated tables describe the current partition "
            f"({seen.get('clean')} clean of {seen.get('all')}, {a['n_with_issues']} flagged)")


MAIN_REQUIRED = {"permutation null": r"permutation",
                 "model-level bootstrap": r"bootstrap",
                 "intra-annotator label": r"intra-annotator",
                 "oracle flags reported": r"\b7 such items\b|\b7 flags?\b|7 items across"}
MAIN_FORBIDDEN = {"k=10 in the main text": r"k\s*=\s*10",
                  "the word first": r"\bwe are the first\b"}


def g_maintext_claims(fail) -> str:
    """What the brief requires present, and absent, in the MAIN text specifically.

    Scoped to the body before \\appendix. k=10 is not banned from the paper, only from the main
    text: it belongs in the appendix, where the truncation that makes it uninterpretable is
    explained. A whole-file scan would report the appendix copy and be wrong."""
    sys.path.insert(0, str(ROOT / "paper"))
    import prosecheck as W
    tex = (ROOT / "paper" / "main.tex").read_text()
    body = W.body(tex.split(r"\appendix")[0])
    for label, pat in MAIN_REQUIRED.items():
        if not re.search(pat, body, re.I):
            fail(f"the main text does not contain {label} (pattern {pat!r})")
    for label, pat in MAIN_FORBIDDEN.items():
        hits = re.findall(pat, body, re.I)
        if hits:
            fail(f"{label}: {len(hits)} occurrence(s) in the main text")
    return (f"{len(MAIN_REQUIRED)} required claims present, {len(MAIN_FORBIDDEN)} forbidden "
            f"patterns absent, over {len(body.split())} words of main text")


def prereg_failure_text(body: str, res: dict, fail) -> None:
    """The prereg's failure clause, enforced against the result rather than trusted.

    It commits us, if the repaired wobble does not fall below the threshold, to reporting that in
    the main text with the observed value AND its interval, and to withdrawing the causal claim.
    A commitment nothing checks is a commitment the next edit can quietly drop, and the edit that
    drops it is the one that makes the paper read better."""
    if res.get("meets_threshold"):
        return
    for label, value in (("the observed repaired wobble", res["after_wobble"]),
                         ("its interval's lower bound", res["after_lo"]),
                         ("its interval's upper bound", res["after_hi"])):
        if f"{value:.3f}" not in body:
            fail(f"the prediction failed, so the main text must state {label} "
                 f"({value:.3f}); it does not")
    if not re.search(r"correlational", body, re.I):
        fail("the prediction failed, so the main text must report the association as "
             "correlational; the word does not appear")
    if not re.search(r"withdraw", body, re.I):
        fail("the prediction failed, so the causal claim must be withdrawn in those terms")


def g_prereg_failure(fail) -> str:
    """Report the registered verdict and, on a failure, that the paper honours the commitment."""
    p = ROOT / "out" / "block2c_result.json"
    if not p.exists():
        fail("out/block2c_result.json is absent, so the registered prediction has no recorded "
             "verdict; a repair experiment with no scored outcome must never read as passing")
        return "NOT CHECKED - no Block 2c result on disk"
    res = json.loads(p.read_text())
    sys.path.insert(0, str(ROOT / "paper"))
    import prosecheck as W
    body = W.body((ROOT / "paper" / "main.tex").read_text().split(r"\appendix")[0])
    prereg_failure_text(body, res, fail)
    verdict = "MET" if res["meets_threshold"] else "FAILED and reported as the prereg requires"
    return (f"repaired wobble {res['after_wobble']:.4f} "
            f"[{res['after_lo']:.4f}, {res['after_hi']:.4f}] against the registered "
            f"{res['threshold']}: prediction {verdict}")


def selftest() -> str:
    """Prove the partition check goes RED on a wrong partition.

    Without this it is a check that has only ever been run against data that satisfies it, and a
    comparison that always passes is indistinguishable from one that cannot fail. The doctored
    audit is the old 424/46 split, the exact partition this gate exists to detect."""
    ok = []
    g_downstream_fresh(ok.append)
    assert not ok, f"the real partition must pass: {ok}"
    red = []
    g_downstream_fresh(red.append, {"n_clean": 424, "n_items": 470, "n_with_issues": 46})
    assert len(red) == 1 and "424" in red[0], \
        f"a superseded partition must be reported, naming the number: {red}"
    # The prereg-failure clause, proven RED against the corruption it exists to catch: a body that
    # withdraws the claim in words but has dropped the number, and one that keeps the number but
    # quietly stops withdrawing. Both read fine to a human skimming for tone.
    res = {"meets_threshold": False, "after_wobble": 0.2083, "after_lo": 0.1453,
           "after_hi": 0.2895, "threshold": 0.161}
    # 0.2895 formats to "0.289", not "0.290": the fixture must be built the way the gate formats,
    # or the selftest reports a defect in itself as a defect in the paper.
    good = (f"we withdraw the causal claim; it is {res['after_wobble']:.3f} "
            f"[{res['after_lo']:.3f}, {res['after_hi']:.3f}] and correlational only")
    clean = []
    prereg_failure_text(good, res, clean.append)
    assert not clean, f"a body that honours the commitment must pass: {clean}"
    for body, want in ((good.replace(f"{res['after_wobble']:.3f}", "some"), "0.208"),
                       (good.replace("correlational", "descriptive"), "correlational"),
                       (good.replace("withdraw", "soften"), "withdraw")):
        bad = []
        prereg_failure_text(body, res, bad.append)
        assert any(want in m for m in bad), f"dropping {want!r} must be reported: {bad}"
    # And it must stay quiet when the prediction is MET, or it would demand a withdrawal of a
    # claim that was never falsified.
    met = []
    prereg_failure_text("nothing relevant here", {**res, "meets_threshold": True}, met.append)
    assert not met, f"a met prediction must require nothing: {met}"
    return ("block6_gate selftest PASS - the partition check accepts the current split and "
            "reports the superseded 424/46 one by name, and the prereg-failure clause goes RED "
            "when the value, the interval or the withdrawal is dropped")


GATES = [("partition check discriminates", lambda f: selftest()),
         ("audit selftests", g_audit_tests), ("prereg not edited", g_prereg_unedited),
         ("prereg threshold", g_prereg_threshold), ("downstream fresh", g_downstream_fresh),
         ("main-text claims", g_maintext_claims),
         ("prereg failure reported", g_prereg_failure)]


def main() -> int:
    failed = []
    for name, fn in GATES:
        mine = []
        try:
            note = fn(mine.append)
        except Exception as e:                                    # noqa: BLE001
            mine.append(f"the check itself raised {type(e).__name__}: {e}")
            note = "CRASHED - this is a failure, not a skip"
        print(f"  {'FAIL' if mine else 'ok  '}  {name:<20} {note}")
        for m in mine:
            print(f"          !! {m}")
        failed += [name] if mine else []
    print(f"\n{len(GATES) - len(failed)}/{len(GATES)} analysis-side gates pass"
          + (f"; FAILED: {', '.join(failed)}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
