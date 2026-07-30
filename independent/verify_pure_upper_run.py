#!/usr/bin/env python3
"""Bounded raw check of the pure-upper run ceiling (K17).

The raw safe map and block decomposition come from
``verify_general_gate_boundaries.py``, which imports no project implementation.
The sweep is finite evidence within its displayed bound; it is not a theorem
that pure-upper runs are bounded.
"""

from __future__ import annotations

import sys
from pathlib import Path
from runpy import run_path


RAW = run_path(str(Path(__file__).with_name("verify_general_gate_boundaries.py")))
State = RAW["State"]
zero_blocks = RAW["zero_blocks"]


def defect(state: object) -> int:
    return state.n - state.q - 2 * state.e


def pure_upper(blocks: list[object], left: int, right: int) -> bool:
    """The pure-upper test: d >= 2, 1 <= x <= H, and 2 d' >= H."""
    parent = blocks[left]
    child = blocks[right]
    if parent.wraps == 0 or child.wraps == 0 or parent.next_zero is None:
        return False
    gap = right - left - 1
    spacing = 1 << (parent.wraps + gap + 3)
    if defect(parent.start) < 2:
        return False
    returned = parent.next_zero
    excess = (returned.e << (gap + 2)) - returned.n - gap - 3
    if excess < 1 or excess > spacing:
        return False
    return 2 * defect(child.start) >= spacing


def residue_window(parent: object, gap: int) -> tuple[float, float]:
    """Corollary 134: the admissible band for the parent's returned residue."""
    returned = parent.next_zero
    low = (returned.n + gap + 3) / (1 << (gap + 2))
    return low, (1 << (parent.wraps + 1)) + low


def check_windows(n_max: int) -> int:
    """Every literal pure-upper gate must satisfy (134.1) and (134.2)."""
    checked = 0
    for n in range(8, n_max + 1):
        for e in range(1, n):
            blocks = zero_blocks(State(n, 0, e), limit=400)
            spots = [
                index
                for index, block in enumerate(blocks)
                if block.wraps > 0 and block.next_zero is not None
            ]
            for left, right in zip(spots, spots[1:]):
                if not pure_upper(blocks, left, right):
                    continue
                gap = right - left - 1
                low, high = residue_window(blocks[left], gap)
                residue = blocks[left].next_zero.e
                assert low < residue <= high, (n, e, left, residue, low, high)
                # (134.2): the two-block ceiling, from d' >= 2^(k+r+2) and
                # Lemma 83 applied to the child block.
                child = blocks[right]
                exponent = blocks[left].wraps + gap + child.wraps + 2
                assert (1 << exponent) <= child.start.n + child.wraps + 3, (
                    n,
                    e,
                    left,
                    exponent,
                )
                checked += 1
    return checked


def longest_run(n: int, u: int, e: int) -> int:
    blocks = zero_blocks(State(n, u, e), limit=3000)
    spots = [
        index
        for index, block in enumerate(blocks)
        if block.wraps > 0 and block.next_zero is not None
    ]
    best = 0
    run = 0
    for left, right in zip(spots, spots[1:]):
        if pure_upper(blocks, left, right):
            run += 1
            best = max(best, run)
        else:
            run = 0
    return best


def sweep(n_max: int) -> tuple[int, tuple[int, int], int]:
    best = 0
    argbest = (0, 0)
    states = 0
    for n in range(6, n_max + 1):
        for e in range(1, n):
            states += 1
            run = longest_run(n, 0, e)
            if run > best:
                best = run
                argbest = (n, e)
    return best, argbest, states


def main() -> int:
    bound = int(sys.argv[1]) if len(sys.argv) > 1 else 500

    # R8: the K14 witness really has six consecutive pure-upper gates, and
    # Lemma 116's normalization preserves the run.
    literal = longest_run(971, 5, 482)
    normalized = longest_run(971, 0, 482)
    print(f"K14 state (971,5,482): {literal} gates; normalized: {normalized}")
    assert literal == 6 and normalized == 6, (literal, normalized)

    windows = check_windows(min(bound, 260))
    print(f"pure-upper gates inside the Corollary 134 window: {windows}")

    best, argbest, states = sweep(bound)
    print(f"sweep n<={bound}: {states} normalized states, longest run {best} at {argbest}")
    assert best <= 6, (best, argbest)

    print(
        "VERDICT: bounded raw traces confirm the six-gate K14 run and find no "
        "longer pure-upper run in the displayed range; boundedness is not proved."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
