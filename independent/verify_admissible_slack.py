#!/usr/bin/env python3
"""Bounded raw checks for Lemma 143 through Corollary 147.

Theorem 138 left the wrap count outside the closed map: it accumulates as
``U' = U + k`` and decides only termination, so admissibility sat outside the
slack coordinates of Lemma 140. Lemma 143 puts it inside them. With the budget

    G = n - 2U,

whose recurrence G' = G + r + 1 - k is (133.1), the claim is that the safe path
continues from one positive block to the next exactly when the gap slack fits
that budget, ``alpha <= G' - 4``. Corollary 144 prices the returned residue and
the block length against it, and Theorem 145 turns those into a bound on how
many blocks a chain can hold: N <= 3C - 13, where C is the largest budget the
chain reaches.

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


def check_chain_length(n_max: int) -> tuple[int, int, float]:
    """Theorem 145: a chain of N blocks needs a budget of at least (N+13)/3.

    Returns ``(chains checked, longest chain, tightest N/(3C-13) ratio)``. The
    ratio is reported because the bound is far from sharp in this range and
    saying so is part of stating it honestly.
    """
    chains = longest = 0
    tightest = 0.0
    for n in range(8, n_max + 1):
        for e in range(1, n):
            chain = descriptions(zero_blocks(State(n, 0, e), limit=400))
            if len(chain) < 2:
                continue
            budgets = [bn - 2 * bu for bn, bu, _, _ in chain]
            worst = max(budgets)
            # The proof needs G >= 4 at every block, and needs a chain of two
            # or more to force C >= 5; both are asserted rather than assumed.
            assert min(budgets) >= 4, (n, e, min(budgets))
            assert worst >= 5, (n, e, worst)
            assert len(chain) <= 3 * worst - 13, (n, e, len(chain), worst)
            chains += 1
            longest = max(longest, len(chain))
            tightest = max(tightest, len(chain) / (3 * worst - 13))
    return chains, longest, tightest


def check_unit_fibre(n_max: int) -> tuple[int, int]:
    """Corollary 147, which needs consecutive pairs rather than single blocks.

    Returns ``(single-wrap children, unit parents)``.
    """
    children = parents = 0
    for n in range(8, n_max + 1):
        for e in range(1, n):
            chain = descriptions(zero_blocks(State(n, 0, e), limit=400))
            for (pn, pu, pk, pf), (cn, cu, ck, cf) in zip(chain, chain[1:]):
                r = forced_gap(pn + pk + 1, pf)
                alpha = (pf << (r + 2)) - (cn + 4)
                budget, child_budget = pn - 2 * pu, cn - 2 * cu
                if ck == 1:
                    # (147.1), and with it the collapse of (143.2) into (144.1):
                    # survival at the parent *is* the residue cap at the child.
                    assert cf == alpha + 1, (n, e, pn, cf, alpha)
                    assert (alpha <= child_budget - 4) == (cf <= child_budget - 3)
                    children += 1
                if pk == 1:
                    # (147.3): the window widens relative to the index exactly
                    # when r * U exceeds G. Cross-multiplied to stay exact.
                    assert cn == pn + 2 + r and child_budget == budget + r
                    assert (child_budget * pn > budget * cn) == (r * pu > budget)
                    parents += 1
    return children, parents


def check(n_max: int) -> dict[str, int]:
    tally = {"gates": 0, "continued": 0, "died": 0, "tight": 0, "long_blocks": 0}
    for n in range(8, n_max + 1):
        for e in range(1, n):
            for start_n, start_u, k, f in descriptions(
                zero_blocks(State(n, 0, e), limit=200)
            ):
                assert f >= 1, (n, e, start_n, f)
                m = start_n + k + 1
                r = forced_gap(m, f)
                child_n = m + r
                child_u = start_u + k
                budget = start_n - 2 * start_u
                child_budget = child_n - 2 * child_u
                alpha = (f << (r + 2)) - (child_n + 4)

                # (143.1), which restates (133.1): G is linear in r and k.
                assert child_budget == budget + r + 1 - k, (n, e, start_n)

                # (144.1): the returned residue is bounded by the budget, with
                # no reference to the index. Sharp only when k = 1.
                assert f <= budget - 3, (n, e, start_n, f, budget)
                if f == budget - 3:
                    assert k == 1, (n, e, start_n, k)
                    tally["tight"] += 1

                # (144.2): a block longer than one wrap needs a large budget.
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

                # (144.3): the window the doubled residue has to land in. Stated
                # doubled throughout to keep it in integers.
                doubled = f << (r + 1)
                assert 2 * doubled >= child_n + 4, (n, e, start_n)
                assert doubled <= child_budget + child_u, (n, e, start_n)
    return tally


def main(argv: list[str]) -> int:
    n_max = int(argv[1]) if len(argv) > 1 else 200
    tally = check(n_max)
    chains, longest, tightest = check_chain_length(n_max)
    children, parents = check_unit_fibre(n_max)
    print(f"index bound {n_max}")
    print(f"  gates decided both ways : {tally['gates']}")
    print(f"    path continued        : {tally['continued']}")
    print(f"    path died             : {tally['died']}")
    print(f"  f = G - 3, sharp cases  : {tally['tight']}")
    print(f"  blocks with k >= 2      : {tally['long_blocks']}")
    print(f"  chains of >= 2 blocks   : {chains}")
    print(f"    longest              : {longest}")
    print(f"    tightest N/(3C-13)   : {tightest:.3f}")
    print(f"  single-wrap children    : {children}")
    print(f"  unit parents            : {parents}")
    if tally["died"] == 0 or tally["continued"] == 0:
        print("\nFAIL: one direction of the equivalence was never exercised.")
        return 1
    print("\nLemma 143 through Corollary 147 hold on every case in range.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
