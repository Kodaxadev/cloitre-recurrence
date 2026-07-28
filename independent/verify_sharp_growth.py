#!/usr/bin/env python3
"""Independent bounded checks for Theorem 56.

This script uses raw `(n,q,r)` transitions and imports no project code.
It checks the parameterized rebound implication on arbitrary admissible
states and the finite sharp-growth inequality on literal starting orbits.
These checks are regressions, not a proof of the asymptotic theorem.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    n: int
    q: int
    r: int

    def valid(self) -> bool:
        return self.n >= 2 and self.q >= 0 and 0 <= self.r < self.n


def digit(state: State) -> int:
    delta = 2 * state.r - state.q
    modulus = state.n + 1
    if delta < 0:
        return -1
    if delta >= modulus:
        return 1
    return 0


def step(state: State) -> State:
    assert state.valid()
    change = digit(state)
    delta = 2 * state.r - state.q
    modulus = state.n + 1
    next_state = State(
        n=modulus,
        q=state.q + change,
        r=delta - change * modulus,
    )
    assert next_state.valid()
    return next_state


def enter(start: int) -> State:
    n = 2
    value = start
    while value >= n * n:
        value += value % n
        n += 1
    return State(n=n, q=value // n, r=value % n)


def check_parameterized_cascades() -> int:
    checked = 0
    for n in range(2, 161):
        for q in range(n + 1):
            for r in range(n):
                state = State(n=n, q=q, r=r)
                if digit(state) != -1:
                    continue
                for length in range(2, 8):
                    if n < (1 << (length + 2)) * q:
                        continue
                    current = step(state)
                    for _ in range(length):
                        assert digit(current) == 1
                        current = step(current)
                    checked += 1
    return checked


def check_finite_growth() -> int:
    checked = 0
    for start in range(1, 1001):
        state = enter(start)
        entry_n = state.n
        for _ in range(5_000):
            if state.r == state.q:
                break
            if state.n >= 4:
                scale = state.n.bit_length()
                for length in range(2, 8):
                    numerator = length - 1
                    denominator = length + 1
                    cascade_scale = 1 << (length + 2)
                    if denominator * scale < numerator * cascade_scale:
                        continue
                    assert (
                        denominator
                        * scale
                        * (state.q + entry_n + 5)
                        >= numerator * state.n
                    )
                    checked += 1
            state = step(state)
    return checked


def main() -> None:
    cascades = check_parameterized_cascades()
    growth = check_finite_growth()
    assert cascades > 1_000
    assert growth > 100_000
    print(f"parameterized rebound cascades checked: {cascades}")
    print(f"finite sharp-growth inequalities checked: {growth}")
    print("VERDICT: bounded raw checks agree with Theorem 56.")


if __name__ == "__main__":
    main()
