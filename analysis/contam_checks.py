"""
Location: paper-a/analysis/contam_checks.py
Purpose: The two controls that must pass BEFORE any contamination number is read: re-counting every
         item reproduces the published cells, and the partitions add back to them. Split out of
         contamination.py when the author-exclusion arm took that file past its 300-line budget.
         They are the file's fail-closed gate, so they live together and nothing else lives here.
Functions: identity_check(), sum_check(), selftest()
Calls: nothing; both take already-computed cell dicts
Imports: typing
"""

from typing import Sequence

def identity_check(models: Sequence[str], names: Sequence[str], whole, published,
                   accuracy=None) -> str:
    """POSITIVE CONTROL. Re-counting over ALL items must reproduce every published cell exactly --
    wobble AND, when the published accuracy matrix is supplied, majority accuracy too. A partition
    that loses or duplicates an item would otherwise look exactly like a finding, and a `majority`
    flag that means something slightly different from the benchmark's would silently rewrite
    Figure 1(b)'s x-axis."""
    bad = []
    for m in models:
        for n in names:
            a, b = whole[m][n], published[m][n]
            if a["n_items"] != b["n_items"] or a["flipped"] != b["flipped"]:
                bad.append(f"{m}/{n}: recounted {a['flipped']}/{a['n_items']} vs published "
                           f"{b['flipped']}/{b['n_items']}")
            pub_acc = (accuracy or {}).get(m, {}).get(n)
            if pub_acc is not None and abs((a["accuracy"] or 0.0) - pub_acc) > 1e-12:
                bad.append(f"{m}/{n}: recounted accuracy {a['accuracy']} vs published {pub_acc}")
    if bad:
        raise SystemExit("CONTAMINATION IDENTITY CHECK FAILED:\n  " + "\n  ".join(bad[:10]))
    return (f"identity PASS - re-counting all items through the partition code reproduces all "
            f"{len(models) * len(names)} published cells exactly (wobble"
            f"{' and majority accuracy' if accuracy else ''})")


def sum_check(models: Sequence[str], names: Sequence[str], clean, flag, published,
              excluded=None) -> str:
    """The other half of the control: the partitions must PARTITION. Every item lands in exactly
    one of clean, flagged or author-excluded, so the three add back to the published counts.

    The excluded arm is part of the sum rather than subtracted from the total on the left: that
    way an exclusion that silently failed to apply shows up here as a mismatch instead of as a
    smaller corpus nobody questioned."""
    def tot(cell, m, n, key):
        return cell[m][n][key] if cell else 0
    bad = [f"{m}/{n}" for m in models for n in names
           if clean[m][n]["n_items"] + flag[m][n]["n_items"] + tot(excluded, m, n, "n_items")
           != published[m][n]["n_items"]
           or clean[m][n]["flipped"] + flag[m][n]["flipped"] + tot(excluded, m, n, "flipped")
           != published[m][n]["flipped"]]
    if bad:
        raise SystemExit("PARTITION DOES NOT SUM TO THE PUBLISHED COUNTS: " + ", ".join(bad[:10]))
    n_ex = sum(tot(excluded, m, n, "n_items") for m in models for n in names)
    return (f"partition PASS - clean + flagged + {n_ex} author-excluded = published counts in all "
            f"{len(models) * len(names)} cells")


def _cell(n, flipped, acc=None):
    return {"n_items": n, "flipped": flipped, "accuracy": acc}


def _raises(fn) -> bool:
    """True when fn() fails closed. The exception is recorded and returned, never swallowed."""
    caught = False
    try:
        fn()
    except SystemExit:
        caught = True
    return caught


def selftest() -> str:
    """A truth table, not one good case. Both of these gates decide whether any contamination
    number in the paper may be read, and a gate never shown to go RED on known-bad input is the
    exact defect the rest of this paper is about: each arm below must PASS on correct input and
    FAIL on a specific corruption, so a green here means the check discriminates rather than
    merely runs."""
    M, N = ["m1"], ["t1"]
    whole = {"m1": {"t1": _cell(10, 3, 0.9)}}
    pub = {"m1": {"t1": _cell(10, 3)}}
    acc = {"m1": {"t1": 0.9}}
    assert "identity PASS" in identity_check(M, N, whole, pub, acc), "correct input must pass"
    # NEGATIVE CONTROLS, one per way a partition can lie.
    assert _raises(lambda: identity_check(M, N, {"m1": {"t1": _cell(9, 3, 0.9)}}, pub)), \
        "a lost item must be caught"
    assert _raises(lambda: identity_check(M, N, {"m1": {"t1": _cell(10, 4, 0.9)}}, pub)), \
        "a miscounted flip must be caught"
    assert _raises(lambda: identity_check(M, N, whole, pub, {"m1": {"t1": 0.8}})), \
        "an accuracy that disagrees with the published matrix must be caught"

    clean = {"m1": {"t1": _cell(6, 1)}}
    flag = {"m1": {"t1": _cell(3, 1)}}
    excl = {"m1": {"t1": _cell(1, 1)}}
    assert "partition PASS" in sum_check(M, N, clean, flag, pub, excl), "6+3+1 = 10 must pass"
    assert _raises(lambda: sum_check(M, N, clean, flag, pub)), \
        "dropping the excluded arm must break the sum, not silently shrink the corpus"
    assert _raises(lambda: sum_check(M, N, clean, flag, pub, {"m1": {"t1": _cell(2, 1)}})), \
        "an over-counted exclusion must be caught"
    assert _raises(lambda: sum_check(M, N, clean, {"m1": {"t1": _cell(3, 2)}}, pub, excl)), \
        "flips that do not add back must be caught even when the item counts do"
    return ("contam_checks selftest PASS - identity and partition each accept correct cells and "
            "go RED on a lost item, a miscounted flip, a disagreeing accuracy, a dropped "
            "exclusion arm, an over-counted exclusion, and flips that do not add back")


if __name__ == "__main__":
    print(selftest())
