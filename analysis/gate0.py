"""
Location: paper-a/analysis/gate0.py
Purpose: Entry point for the §0 provenance-contamination gate. Runs the whole thing end to end and
         writes out/AUDIT_CONTAMINATION.md plus every CSV the paper's exhibits read, in both
         readings (out/tables/all/ and out/tables/clean/). Deterministic: no arguments, no state.
         Usage:  python3 analysis/gate0.py
Functions: main()
Calls: matrix, analyses, contamination, contam_recompute, contam_tables, contam_report
Imports: sys, pathlib
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analyses as an              # noqa: E402
import config                      # noqa: E402
import contam_recompute as CR      # noqa: E402
import contam_report               # noqa: E402
import contam_tables as CT         # noqa: E402
import contamination               # noqa: E402
import folddiag                    # noqa: E402
import fulltext                    # noqa: E402
import matrix                      # noqa: E402
import quotematch                  # noqa: E402


def main() -> dict:
    print(folddiag.band_selftest())
    print(quotematch.selftest())
    print(fulltext.selftest(config.probity_root()))
    print(contamination.selftest())
    print(CR.selftest())
    out = config.out_paths()
    t = out["tables"]
    models, leaves, cells = matrix.load_cells()
    names = [l["leaf"] for l in leaves]
    accuracy = matrix.load_accuracy(models, leaves)
    frontier = an.capability_split(an.aggregate_wobble(models, names, cells))["frontier"]
    gate = contamination.run(models, leaves, cells, frontier, accuracy)
    rb = CR.rebuild(models, leaves, gate, cells, gate["all_items"]["active"],
                    gate["clean_only"]["active"], frontier)
    for line in gate["checks"] + [rb["rel_control"]]:
        print(" ", line)
    tasks = CT.task_rows(leaves, gate)
    CT.write_contamination(gate["rows"], t)
    CT.write_tasks(tasks, t)
    CT.write_categories(tasks, t)
    CT.write_delta(CT.headline_deltas(gate, rb, models, tasks), t)
    CT.write_mirror(models, leaves, gate["cells_all"], gate["all_items"], rb["all"], t, "all")
    CT.write_mirror(models, leaves, gate["cells_clean"], gate["clean_only"], rb["clean"], t,
                    "clean")
    res = contam_report.write(gate, rb, models, tasks, out["out"])
    print(f"\nMATERIAL DIFFERENCE: {res['material']}")
    print(f"written: {res['path']}")
    return res


if __name__ == "__main__":
    main()
