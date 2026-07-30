#!/usr/bin/env python3
"""Bounded raw checks for Lemmas 135/136/140 and Theorems 137/138.

The raw safe map and block decomposition come from
``verify_general_gate_boundaries.py``, which imports no project implementation.
Every check compares a closed form against literal safe-map traces; the sweeps
are finite evidence within their displayed bounds.
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


def forced_length(n: int, overshoot: int) -> int:
    """(135.2): least K >= 1 with 2^(K+1) A >= n + K + 5."""
    k = 1
    while (overshoot << (k + 1)) < n + k + 5:
        k += 1
    return k


def psi(n: int, u: int, k: int, f: int) -> tuple[int, int, int, int]:
    """(137.1): the closed successor of a block description."""
    m = n + k + 1
    r = forced_gap(m, f)
    child_n = m + r
    child_u = u + k
    overshoot = child_n + 4 - (f << (r + 1))
    child_k = forced_length(child_n, overshoot)
    return child_n, child_u, child_k, child_n + child_k + 4 - (overshoot << child_k)


def base_map(n: int, k: int, f: int) -> tuple[int, int, int, int, int]:
    """The base map of Theorem 138: no U argument anywhere.

    Returns ``(n', k', f', r, A')``.
    """
    m = n + k + 1
    r = forced_gap(m, f)
    child_n = m + r
    overshoot = child_n + 4 - (f << (r + 1))
    child_k = forced_length(child_n, overshoot)
    return (
        child_n,
        child_k,
        child_n + child_k + 4 - (overshoot << child_k),
        r,
        overshoot,
    )


def check_skew_product_and_slacks(n_max: int) -> tuple[int, int]:
    """Theorem 138 and Lemma 140 on literal traces."""
    semiconjugacy = 0
    slacks = 0
    for n in range(8, n_max + 1):
        for e in range(1, n):
            chain = descriptions(zero_blocks(State(n, 0, e), limit=200))
            for current, nxt in zip(chain, chain[1:]):
                start_n, start_u, start_k, start_f = current
                child_n, child_k, child_f, gap, overshoot = base_map(
                    start_n, start_k, start_f
                )
                # (138.1): the base map reproduces (n, k, f); U just accumulates.
                assert (child_n, child_k, child_f) == (nxt[0], nxt[2], nxt[3])
                assert nxt[1] == start_u + start_k
                semiconjugacy += 1

                alpha = (start_f << (gap + 2)) - (child_n + 4)
                beta = (overshoot << (child_k + 1)) - (child_n + child_k + 5)
                # (140.2) inversions
                assert 2 * overshoot == child_n + 4 - alpha
                assert 2 * child_f == child_n + child_k + 3 - beta
                # (140.3) first line: beta from alpha
                assert beta == (1 << child_k) * (child_n + 4 - alpha) - (
                    child_n + child_k + 5
                )
                # (140.4) and (140.5)
                assert alpha >= 0 and beta >= 0
                if gap >= 1:
                    assert alpha <= child_n
                if child_k >= 2:
                    assert beta < child_n + child_k + 3
                # (140.6) parities
                assert (alpha - (child_n + 4)) % 2 == 0
                assert (beta - (child_n + child_k + 3)) % 2 == 0
                # (140.7) growing congruences
                assert (alpha + child_n + 4) % (1 << (gap + 2)) == 0
                assert (beta + child_n + child_k + 5) % (1 << (child_k + 1)) == 0
                slacks += 1
    return semiconjugacy, slacks


def check_wrap_prefix(n_max: int) -> tuple[int, int]:
    """Corollary 139: raised wrap counts give a prefix and no more blocks."""
    compared = 0
    strict = 0
    for n in range(8, n_max + 1):
        for e in range(1, n):
            if 2 * e > n:
                continue
            base_word = digit_word(n, 0, e)
            base_blocks = len(descriptions(zero_blocks(State(n, 0, e), limit=400)))
            for u in range(1, n - 2 * e + 1):
                raised_word = digit_word(n, u, e)
                assert raised_word == base_word[: len(raised_word)], (n, u, e)
                raised_blocks = len(
                    descriptions(zero_blocks(State(n, u, e), limit=400))
                )
                assert raised_blocks <= base_blocks, (n, u, e)
                compared += 1
                if raised_blocks < base_blocks:
                    strict += 1
    return compared, strict


def digit_word(n: int, u: int, e: int, cap: int = 1200) -> list[str]:
    word: list[str] = []
    current = State(n, u, e)
    for _ in range(cap):
        outcome = step(current)
        if outcome is None:
            break
        word.append(outcome[0])
        current = outcome[1]
    return word


def descriptions(blocks: list[object]) -> list[tuple[int, int, int, int]]:
    return [
        (block.start.n, block.start.q, block.wraps, block.next_zero.e)
        for block in blocks
        if block.wraps > 0 and block.next_zero is not None
    ]


def check_intermediate_residues(n_max: int) -> int:
    """(135.1): the residue after j wraps of a block."""
    checked = 0
    for n in range(8, n_max + 1):
        for e in range(1, n):
            blocks = zero_blocks(State(n, 0, e), limit=200)
            for block in blocks:
                if block.wraps == 0:
                    continue
                overshoot = block.start.n + 4 - 2 * block.start.e
                # Walk the literal digits of this block.
                outcome = step(block.start)
                if outcome is None or outcome[0] != "zero":
                    continue
                current = outcome[1]
                for wrap_index in range(1, block.wraps + 1):
                    outcome = step(current)
                    assert outcome is not None and outcome[0] == "wrap"
                    current = outcome[1]
                    predicted = (
                        block.start.n + wrap_index + 4 - (overshoot << wrap_index)
                    )
                    assert current.e == predicted, (n, e, wrap_index)
                    assert current.n == block.start.n + 1 + wrap_index
                    checked += 1
    return checked


def check_forced_length(n_max: int) -> tuple[int, int]:
    """(135.2) against the literal wrap count, returning and terminating."""
    returning = 0
    terminating = 0
    for n in range(8, n_max + 1):
        for e in range(1, n):
            for block in zero_blocks(State(n, 0, e), limit=200):
                if block.wraps == 0:
                    continue
                overshoot = block.start.n + 4 - 2 * block.start.e
                assert forced_length(block.start.n, overshoot) == block.wraps, (
                    n,
                    e,
                    block.start,
                )
                if block.next_zero is None:
                    terminating += 1
                else:
                    returning += 1
    return returning, terminating


def check_forced_gap(n_max: int) -> int:
    """(136.1) against the literal gap, at every gate."""
    checked = 0
    for n in range(8, n_max + 1):
        for e in range(1, n):
            blocks = zero_blocks(State(n, 0, e), limit=200)
            spots = [
                index
                for index, block in enumerate(blocks)
                if block.wraps > 0 and block.next_zero is not None
            ]
            for left, right in zip(spots, spots[1:]):
                parent = blocks[left]
                returned = parent.next_zero
                assert forced_gap(returned.n, returned.e) == right - left - 1, (
                    n,
                    e,
                    left,
                )
                checked += 1
    return checked


def check_iterated_map(n_max: int) -> tuple[int, int]:
    """Theorem 137: iterating Psi reproduces every later description."""
    paths = 0
    steps = 0
    for n in range(8, n_max + 1):
        for e in range(1, n):
            chain = descriptions(zero_blocks(State(n, 0, e), limit=200))
            if len(chain) < 2:
                continue
            paths += 1
            state = chain[0]
            for expected in chain[1:]:
                state = psi(*state)
                assert state == expected, (n, e, state, expected)
                steps += 1
    return paths, steps


def check_recurrence(n_max: int) -> int:
    """(137.2): the closed two-step residue recurrence."""
    checked = 0
    for n in range(8, n_max + 1):
        for e in range(1, n):
            blocks = zero_blocks(State(n, 0, e), limit=200)
            spots = [
                index
                for index, block in enumerate(blocks)
                if block.wraps > 0 and block.next_zero is not None
            ]
            for left, right in zip(spots, spots[1:]):
                parent = blocks[left]
                child = blocks[right]
                gap = right - left - 1
                child_k = child.wraps
                predicted = (
                    (parent.next_zero.e << (child_k + gap + 1))
                    - ((1 << child_k) - 1) * (child.start.n + 4)
                    + child_k
                )
                assert predicted == child.next_zero.e, (n, e, left)
                checked += 1
    return checked


def main() -> int:
    bound = int(sys.argv[1]) if len(sys.argv) > 1 else 200

    residues = check_intermediate_residues(min(bound, 120))
    print(f"intermediate residues (135.1) checked: {residues}")

    returning, terminating = check_forced_length(bound)
    print(
        f"forced block length (135.2): {returning} returning, "
        f"{terminating} terminating blocks"
    )

    gaps = check_forced_gap(bound)
    print(f"forced gap (136.1) checked at every gate: {gaps}")

    checked = check_recurrence(bound)
    print(f"closed two-step recurrence (137.2) checked: {checked}")

    paths, steps = check_iterated_map(bound)
    print(f"iterated map (137.1): {paths} paths, {steps} successive descriptions")

    semiconjugacy, slacks = check_skew_product_and_slacks(bound)
    print(
        f"skew product (138.1) checked: {semiconjugacy}; "
        f"slack relations (140.2)-(140.7) checked: {slacks}"
    )

    compared, strict = check_wrap_prefix(min(bound, 110))
    print(
        f"wrap prefix and monotonicity (139.1): {compared} raised states, "
        f"{strict} with strictly fewer blocks"
    )

    print(
        "VERDICT: bounded raw traces agree with Lemmas 135/136/140 and Theorems "
        "137/138; the closed map reproduces every literal block description in "
        "range, the base map needs no wrap count, and every slack relation "
        "holds. Termination of the map is not addressed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
