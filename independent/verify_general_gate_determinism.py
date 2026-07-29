#!/usr/bin/env python3
"""Bounded raw checks that Theorem 133 holds for blocks of any length.

The raw safe map is reused from ``verify_general_gate_boundaries.py``, which
imports no project implementation.  Two things are checked on literal traces:
the general-block gate coordinates used by Theorem 133, and the claim that at
most one zero-only gap admits a pure-upper gate out of a given positive block.
The sweeps are finite evidence within their displayed bounds.
"""

from __future__ import annotations

import sys
from pathlib import Path
from runpy import run_path


RAW = run_path(str(Path(__file__).with_name("verify_general_gate_boundaries.py")))
State = RAW["State"]
zero_blocks = RAW["zero_blocks"]


def pure_upper(n: int, u: int, k: int, f: int, r: int) -> tuple[int, int] | None:
    """The two gap-dependent pure-upper conditions of Theorem 133.

    The parent-defect condition ``d >= 2`` is deliberately omitted: it does not
    involve the gap, so it cannot affect uniqueness in the gap. Returns
    ``(child excess, child defect)`` when both gap-dependent conditions hold.
    """
    d_coord = n - 2 * u
    returns_at = n + k + 1
    spacing = 1 << (k + r + 3)
    excess = (f << (r + 2)) - returns_at - r - 3
    if excess < 1 or excess > spacing:
        return None
    child_d = d_coord + r + 1 - k
    twice_child_defect = child_d - 3 - excess
    if twice_child_defect < spacing or twice_child_defect % 2 != 0:
        return None
    return excess, twice_child_defect // 2


def window_form(n: int, u: int, k: int, f: int, r: int) -> tuple[bool, bool]:
    """Theorem 133's two window inequalities, with h = r + 2 and c = 2^(k+1)."""
    d_coord = n - 2 * u
    lower = n + k + (r + 2) + 3 <= (f << (r + 2))
    upper = (f << (r + 2)) * 1 + ((1 << (k + 1)) << (r + 2)) + 2 <= n + d_coord + 2 * (r + 2)
    return lower, upper


def positive_blocks(blocks: list[object]) -> list[int]:
    return [
        index
        for index, block in enumerate(blocks)
        if block.wraps > 0 and block.next_zero is not None
    ]


def check(index_bound: int, residue_bound: int) -> tuple[int, int, int]:
    coordinates = 0
    pure_gates = 0
    parents = 0
    for n in range(8, index_bound + 1):
        for e in range(1, min(n, residue_bound) + 1):
            if 2 * e > n:
                continue
            blocks = zero_blocks(State(n, 0, e), limit=400)
            spots = positive_blocks(blocks)
            for left, right in zip(spots, spots[1:]):
                parent = blocks[left]
                child = blocks[right]
                k = parent.wraps
                r = right - left - 1
                start = parent.start
                returned = parent.next_zero
                assert returned is not None
                # Coordinates used by Theorem 133.
                assert returned.n == start.n + k + 1, (n, e, left)
                assert child.start.q == start.q + k, (n, e, left)
                assert child.start.n == returned.n + r, (n, e, left)
                d_coord = start.n - 2 * start.q
                child_d = child.start.n - 2 * child.start.q
                assert child_d == d_coord + r + 1 - k, (n, e, left)
                excess = (returned.e << (r + 2)) - returned.n - r - 3
                # Lemma 103: D' - 3 = x + 2 d'.
                literal_child_defect = child.start.n - child.start.q - 2 * child.start.e
                assert child_d - 3 == excess + 2 * literal_child_defect, (n, e, left)
                coordinates += 1

                parent_defect = start.n - start.q - 2 * start.e
                found = pure_upper(start.n, start.q, k, returned.e, r)
                if found is not None and parent_defect >= 2:
                    assert found[0] == excess, (n, e, left)
                    assert found[1] == literal_child_defect, (n, e, left)
                    lower, upper = window_form(start.n, start.q, k, returned.e, r)
                    assert lower and upper, (n, e, left, k, r)
                    pure_gates += 1

                # Theorem 133: at most one gap admits a pure-upper gate.
                admissible = [
                    gap
                    for gap in range(0, 60)
                    if pure_upper(start.n, start.q, k, returned.e, gap) is not None
                ]
                assert len(admissible) <= 1, (n, e, left, k, admissible)
                if admissible:
                    lower, upper = window_form(
                        start.n, start.q, k, returned.e, admissible[0]
                    )
                    assert lower and upper, (n, e, left, k, admissible)
                parents += 1
    return coordinates, pure_gates, parents


def main() -> int:
    index_bound = int(sys.argv[1]) if len(sys.argv) > 1 else 220
    residue_bound = int(sys.argv[2]) if len(sys.argv) > 2 else 220

    coordinates, pure_gates, parents = check(index_bound, residue_bound)
    print(f"literal adjacent-block coordinates checked: {coordinates}")
    print(f"literal pure-upper gates matched: {pure_gates}")
    print(f"parent states with a unique admissible gap: {parents}")
    print(
        "VERDICT: bounded raw traces agree with Theorem 133; no positive block "
        "of any length admits two pure-upper gaps in the displayed range."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
