#!/usr/bin/env python3
"""Bounded raw checks for Lemma 119 and the local ladder identity.

The raw transition implementation is reused, but no project dynamics code is
imported.  These finite checks support the identities, not Theorem 121's
infinite-subsequence dichotomy.
"""

from __future__ import annotations

from pathlib import Path
from runpy import run_path


RAW = run_path(str(Path(__file__).with_name("verify_general_gate_boundaries.py")))
State = RAW["State"]
zero_blocks = RAW["zero_blocks"]


def valuation_two(value: int) -> int:
    assert value > 0
    return (value & -value).bit_length() - 1


def positive_indices(blocks: list[object]) -> list[int]:
    return [
        index
        for index, block in enumerate(blocks)
        if block.wraps > 0 and block.next_zero is not None
    ]


def is_pure_unit(
    blocks: list[object],
    left: int,
    right: int,
) -> bool:
    parent = blocks[left]
    child = blocks[right]
    if parent.wraps != 1 or child.wraps != 1:
        return False
    returned = parent.next_zero
    assert returned is not None
    gap = right - left - 1
    spacing = 1 << (gap + 4)
    next_returned = child.next_zero
    assert next_returned is not None
    parent_defect = (
        parent.start.n - parent.start.q - 2 * parent.start.e
    )
    child_defect = child.start.n - child.start.q - 2 * child.start.e
    return (
        parent_defect >= 2
        and 1 <= next_returned.e <= spacing
        and 2 * child_defect >= spacing
    )


def check() -> tuple[int, int, int]:
    unit_triples = 0
    pure_triples = 0
    six_unit_windows = 0
    for initial_n in range(2, 121):
        for initial_e in range(1, initial_n):
            blocks = zero_blocks(State(initial_n, 0, initial_e))
            positive = positive_indices(blocks)
            for first, second, third in zip(
                positive, positive[1:], positive[2:]
            ):
                parents = (blocks[first], blocks[second], blocks[third])
                if any(block.wraps != 1 for block in parents):
                    continue
                if any(block.next_zero is None for block in parents):
                    continue
                gap = second - first - 1
                next_gap = third - second - 1
                f0, f1, f2 = (
                    block.next_zero.e for block in parents
                )
                n1 = blocks[second].start.n

                assert (
                    (1 << (gap + 2)) * f0
                    + f2
                    + next_gap
                    + 2
                    == ((1 << (next_gap + 2)) + 1) * f1
                )
                modulus = 1 << (min(gap, next_gap) + 2)
                assert (f2 - f1 + next_gap + 2) % modulus == 0
                assert gap + 2 == (
                    valuation_two(n1 + 3 + f1) - valuation_two(f0)
                )
                assert n1 + 3 + f1 == (1 << (gap + 2)) * f0
                unit_triples += 1

                if is_pure_unit(blocks, first, second) and is_pure_unit(
                    blocks, second, third
                ):
                    n2 = blocks[third].start.n
                    quotient2 = blocks[third].start.q
                    assert f1 <= 1 << (gap + 4)
                    assert f1 >= 5
                    assert (f1 - 4) * n2 >= (
                        2 * f1 * quotient2 + 4 * f1 + 12 + 4 * f2
                    )
                    assert (
                        n2 + 3 + f2
                        == (1 << (next_gap + 2)) * f1
                    )
                    pure_triples += 1

            for window in zip(
                positive,
                positive[1:],
                positive[2:],
                positive[3:],
                positive[4:],
                positive[5:],
            ):
                parents = [blocks[index] for index in window]
                if any(block.wraps != 1 for block in parents):
                    continue
                gaps = [
                    window[index + 1] - window[index] - 1
                    for index in range(5)
                ]
                residues = [
                    block.next_zero.e for block in parents
                ]
                assert not (
                    gaps[0] == gaps[2] == gaps[4]
                    and residues[1] == residues[3] == residues[5]
                )
                six_unit_windows += 1
    return unit_triples, pure_triples, six_unit_windows


def check_alternating_growth() -> int:
    checked = 0
    for renewal_gap in range(5):
        scale = 1 << (renewal_gap + 2)
        assert scale >= renewal_gap + 4
        for residue in range(1, 33):
            for quotient in range(1, 9):
                large_gap = scale * quotient - renewal_gap - 4
                numerator = (
                    residue
                    * (1 << (large_gap + 2))
                    * ((1 << scale) - 1)
                )
                assert numerator > (quotient + 1) * (scale + 1)
                checked += 1
    return checked


def main() -> None:
    unit_triples, pure_triples, six_unit_windows = check()
    alternating_growth = check_alternating_growth()
    assert (unit_triples, pure_triples, six_unit_windows) == (
        3_250,
        580,
        167,
    )
    assert alternating_growth == 1_280
    print(f"three-unit compatibility checks: {unit_triples}")
    print(f"pure-unit local ladder checks: {pure_triples}")
    print(f"six-unit alternating-renewal exclusions: {six_unit_windows}")
    print(f"alternating-growth inequalities checked: {alternating_growth}")
    print(
        "VERDICT: bounded raw states agree with Lemma 119, Corollary "
        "120, Theorem 121's local identity, and Theorem 122."
    )


if __name__ == "__main__":
    main()
