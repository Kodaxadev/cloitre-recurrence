#!/usr/bin/env python3
"""Independent bounded checks for Lemmas 63, 65, and Proposition 66.

This script uses raw `(n,q,r)` transitions and imports no project code.
It checks the exact negative suffix, next-ridge remainder, and consecutive
down-epoch defect recurrence. It also checks the explicit diluted family with
arbitrary-precision integers. These finite checks are regressions, not proofs.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    n: int
    q: int
    r: int

    def absorbed(self) -> bool:
        return self.r == self.q


def digit(state: State) -> int:
    delta = 2 * state.r - state.q
    if delta < 0:
        return -1
    if delta >= state.n + 1:
        return 1
    return 0


def step(state: State) -> State:
    change = digit(state)
    modulus = state.n + 1
    delta = 2 * state.r - state.q
    result = State(
        n=modulus,
        q=state.q + change,
        r=delta - change * modulus,
    )
    assert result.q >= 0 and 0 <= result.r < result.n
    return result


def check_segment(parent: State) -> tuple[int, int] | None:
    assert digit(parent) == -1
    start = step(parent)
    start_e = start.r - start.q
    if start_e <= 0:
        return None

    states = [start]
    changes = []
    current = start
    for _ in range(500):
        if current.absorbed():
            return None
        change = digit(current)
        if change == -1:
            break
        changes.append(change)
        current = step(current)
        states.append(current)
    else:
        return None

    up_offsets = [i for i, change in enumerate(changes) if change == 1]
    if not up_offsets:
        return None
    last_up = up_offsets[-1]
    assert all(change == 0 for change in changes[last_up + 1 :])

    before = states[last_up]
    after = states[last_up + 1]
    value = -(after.r - after.q)
    quotient = after.q
    zeros = len(changes) - last_up - 1
    assert 1 <= value <= quotient
    assert current.q == quotient
    assert current.r - current.q == -(1 << zeros) * value
    assert (1 << zeros) * value <= quotient
    assert quotient < (1 << (zeros + 1)) * value

    next_gap = quotient - 2 * current.r
    assert next_gap == (1 << (zeros + 1)) * value - quotient
    assert 1 <= next_gap <= quotient

    parent_gap = parent.q - 2 * parent.r
    parent_budget = parent.q + parent_gap + 2
    next_budget = current.q + next_gap + 2
    distance = current.n - parent.n
    scaled_right = 2 * (current.n + 2) + next_budget
    for offset, change in enumerate(changes):
        if change == 0:
            index = parent.n + offset + 1
            scaled_right += (index + 2) << (distance - offset - 1)
    assert parent_budget << distance == scaled_right
    return len(changes), zeros


def check_diluted_family(max_k: int) -> int:
    checked = 0
    for k in range(1, max_k + 1):
        quotient = 1 << (k * k)
        gap = 3
        start_n = (1 << k) * (quotient + gap + 3) - k - 4
        parent = State(
            n=start_n - 1,
            q=quotient + 1,
            r=(quotient + 1 - gap) // 2,
        )
        assert digit(parent) == -1

        current = step(parent)
        for _ in range(k):
            assert digit(current) == 1
            current = step(current)
        assert current.q == quotient + k
        assert current.r - current.q == -1

        for zero_offset in range(k * k):
            assert digit(current) == 0
            assert current.r - current.q == -(1 << zero_offset)
            current = step(current)
        assert digit(current) == -1
        assert current.r - current.q == -(1 << (k * k))
        checked += 1
    return checked


def check_unit_chain_obstruction(bound: int) -> int:
    checked = 0
    for first_ups in range(1, bound + 1):
        for first_zeros in range(1, bound + 1):
            left_scale = (1 << first_ups) * (
                (1 << (first_zeros + 1)) + 2
            )
            for next_ups in range(1, bound + 1):
                for next_zeros in range(first_zeros, bound + 1):
                    left = left_scale + next_zeros + next_ups + 1
                    right = (1 << next_ups) * (
                        (1 << (next_zeros + 1)) + 2
                    )
                    assert left != right
                    checked += 1
    return checked


def main() -> None:
    checked = 0
    suffix_zeros = 0
    for n in (64, 128, 256, 512):
        for q in range(1, 49):
            for r in range((q + 1) // 2):
                result = check_segment(State(n=n, q=q, r=r))
                if result is None:
                    continue
                checked += 1
                suffix_zeros += result[1]
    diluted_checked = check_diluted_family(12)
    chain_equations_checked = check_unit_chain_obstruction(16)
    assert checked > 1_000
    print(f"terminal ridge segments checked: {checked}")
    print(f"terminal negative zero digits covered: {suffix_zeros}")
    print(f"consecutive down-epoch recurrences checked: {checked}")
    print(f"exact diluted-family parameters checked: {diluted_checked}")
    print(f"unit-chain incompatibilities checked: {chain_equations_checked}")
    print(
        "VERDICT: bounded raw checks agree with Lemmas 63, 65, 68, "
        "and Proposition 66."
    )


if __name__ == "__main__":
    main()
