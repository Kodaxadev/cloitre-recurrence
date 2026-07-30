#!/usr/bin/env python3
"""Bounded raw checks for Lemma 143 and Corollary 144.

Theorem 138 left the wrap count outside the closed map: it accumulates as
``U' = U + k`` and decides only termination, so admissibility sat outside the
slack coordinates of Lemma 140. Lemma 143 puts it inside them. With

    G = n - 2U,

the claim is that the safe path continues from one positive block to the next
exactly when the gap slack fits the budget, ``alpha <= G' - 4``, and that G
itself follows a linear recurrence driven only by the gap and the block length.

The point of checking it here is the *equivalence*. A one-directional check
would be satisfied by any sufficient condition; what needs confirming is that
the inequality also fails at every gate where the literal path dies. So each
gate is decided twice: once by the formula, once by stepping the raw safe map
forward from the return state until it wraps or terminates.

The raw safe map comes from ``verify_general_gate_boundaries.py``, which imports
no project implementation. The sweeps are finite evidence within their bounds.

    independent/verify_admissible_slack.py [n_max]
"""

from __future__ import annotations

import sys
from pathlib import Path
from runpy import run_path


RAW = run_path(str(Path(__file__).with_name("verify_general_gate_boundaries.py")))
State = RAW["State"]
step = RAW["step"]
zero_blocks = RAW["zero_blocks"]


def forced_gap(m: int, f: int) -> int:
    """(136.1): least r >= 0 with 2^(r+2) f >= m + r + 4."""
    r = 0
    while (f << (r + 2)) < m + r + 4:
        r += 1
    return r


def walk_gap(return_state: object) -> tuple[bool, int]:
    """Step the raw map from a return state until it wraps or dies.

    Returns ``(reached_a_wrap, index_of_the_last_zero_taken)``. The second value
    is the index the leading zero of the next positive block was taken at, which
    is what (136.2) predicts as ``n'``; it is meaningless when the first value
    is False.
    """
    current = return_state
    last_zero_index = current.n
    while True:
        outcome = step(current)
        if outcome is None:
            return False, last_zero_index
        if outcome[0] == "wrap":
            return True, last_zero_index
        last_zero_index = current.n
        current = outcome[1]


def descriptions(blocks: list[object]) -> list[tuple[int, int, int, int]]:
    """(n, U, k, f) for each positive block that returns to a zero epoch."""
    return [
        (block.start.n, block.start.q, block.wraps, block.next_zero.e)
        for block in blocks
        if block.wraps > 0 and block.next_zero is not None
    ]


def check(n_max: int) -> dict[str, int]:
    tally = {"gates": 0, "continued": 0, "died": 0, "tight": 0, "long_blocks": 0}
    for n in range(8, n_max + 1):
        for e in range(1, n):
            for start_n, start_u, k, f in descriptions(
                zero_blocks(State(n, 0, e), limit=200)
            ):
                m = start_n + k + 1
                r = forced_gap(m, f)
                child_n = m + r
                child_u = start_u + k
                budget = start_n - 2 * start_u
                child_budget = child_n - 2 * child_u
                alpha = (f << (r + 2)) - (child_n + 4)

                # (143.1): G is linear in the gap and the block length.
                assert child_budget == budget + r + 1 - k, (n, e, start_n)

                # (143.3): the returned residue is bounded by the budget, with
                # no reference to the index. Sharp only when k = 1.
                assert f <= budget - 3, (n, e, start_n, f, budget)
                if f == budget - 3:
                    assert k == 1, (n, e, start_n, k)
                    tally["tight"] += 1

                # (143.4): a block longer than one wrap needs a large budget.
                if k >= 2:
                    assert budget >= 2 * start_u + 11, (n, e, start_n, budget)
                    tally["long_blocks"] += 1

                # (143.2), both directions, against the literal safe map.
                predicted = alpha <= child_budget - 4
                reached, index = walk_gap(State(m, child_u, f))
                assert reached == predicted, (n, e, start_n, alpha, child_budget)
                tally["gates"] += 1

                if not reached:
                    tally["died"] += 1
                    continue
                tally["continued"] += 1

                # The gap the path actually took is the one (136.1) predicts,
                # so the alpha tested above is the child's, not a fiction.
                assert index == child_n, (n, e, start_n, index, child_n)

                # (144.1): the window the doubled residue has to land in. Stated
                # with 2P to keep it in integers.
                doubled = f << (r + 1)
                assert 2 * doubled >= child_n + 4, (n, e, start_n)
                assert doubled <= child_budget + child_u, (n, e, start_n)
    return tally


def main(argv: list[str]) -> int:
    n_max = int(argv[1]) if len(argv) > 1 else 200
    tally = check(n_max)
    print(f"index bound {n_max}")
    print(f"  gates decided both ways : {tally['gates']}")
    print(f"    path continued        : {tally['continued']}")
    print(f"    path died             : {tally['died']}")
    print(f"  f = G - 3, sharp cases  : {tally['tight']}")
    print(f"  blocks with k >= 2      : {tally['long_blocks']}")
    if tally["died"] == 0 or tally["continued"] == 0:
        print("\nFAIL: one direction of the equivalence was never exercised.")
        return 1
    print("\nLemma 143 and Corollary 144 hold on every gate in range.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
