#!/usr/bin/env python3
"""Bounded raw checks for the three-start Lemma 100 and formal exceptions.

The raw safe-map implementation is loaded from the independent gate verifier,
not from project code. Finite checks support but do not prove Theorem 101.
"""

from __future__ import annotations

from runpy import run_path


RAW = run_path("independent/verify_general_gate_boundaries.py")
State = RAW["State"]
zero_blocks = RAW["zero_blocks"]


def defect(state: object) -> int:
    return state.n - state.q - 2 * state.e


def check_raw_increases() -> list[tuple[int, ...]]:
    witnesses = []
    for n in range(2, 701):
        for quotient in range(n):
            width = n - quotient
            for initial_defect in range(2):
                if (width - initial_defect) % 2:
                    continue
                e = (width - initial_defect) // 2
                if not 0 < e < width:
                    continue
                blocks = zero_blocks(State(n, quotient, e))
                positive = [
                    index
                    for index, block in enumerate(blocks)
                    if block.wraps > 0 and block.next_zero is not None
                ]
                for first, second, third in zip(
                    positive,
                    positive[1:],
                    positive[2:],
                ):
                    starts = (
                        blocks[first].start,
                        blocks[second].start,
                        blocks[third].start,
                    )
                    if any(defect(start) > 1 for start in starts):
                        continue
                    if blocks[first].wraps != blocks[second].wraps:
                        continue
                    gap = second - first - 1
                    next_gap = third - second - 1
                    assert next_gap > gap
                    witnesses.append(
                        (
                            n,
                            quotient,
                            e,
                            blocks[first].wraps,
                            blocks[third].wraps,
                            gap,
                            next_gap,
                        )
                    )
    return witnesses


def check_formal_exceptions() -> None:
    # The d=0 formal case forces A=2, below the state bound A>=4.
    k, gap, returned, d, next_d = 1, 1, 1, 0, 0
    scale = 1 << (gap + 1)
    a_value = (
        (scale - 1) * returned
        - gap
        + k
        - d
        - 1
        + next_d
    ) // ((1 << k) - 1)
    assert a_value == 2

    # The d=1 formal case gives (n,U,d)=(12,2,1), so e=9/2.
    returned, d = 3, 1
    a_value = 7
    quotient = a_value - d - 4
    index = (1 << k) * a_value - k - 4 + returned
    assert (index, quotient, d) == (12, 2, 1)
    assert (index - quotient - d) % 2 == 1


def main() -> None:
    witnesses = check_raw_increases()
    check_formal_exceptions()
    assert witnesses == [
        (12, 2, 5, 1, 1, 0, 1),
        (39, 4, 17, 2, 2, 1, 2),
        (41, 3, 19, 2, 2, 0, 1),
        (174, 2, 86, 4, 3, 0, 3),
        (492, 3, 244, 5, 4, 0, 1),
    ]
    print(f"three-start parent gap increases checked: {len(witnesses)}")
    print("two formal decreasing-gap exceptions rejected exactly")
    print("VERDICT: bounded raw states agree with Lemma 100.")


if __name__ == "__main__":
    main()
