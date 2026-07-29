#!/usr/bin/env python3
"""Independent bounded checks for Lemma 63.

This script uses raw `(n,q,r)` transitions and imports no project code.
It checks the exact negative suffix and next-ridge remainder on arbitrary
post-down segments. These finite checks are regressions, not a proof.
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
    return len(changes), zeros


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
    assert checked > 1_000
    print(f"terminal ridge segments checked: {checked}")
    print(f"terminal negative zero digits covered: {suffix_zeros}")
    print("VERDICT: bounded raw checks agree with Lemma 63.")


if __name__ == "__main__":
    main()
