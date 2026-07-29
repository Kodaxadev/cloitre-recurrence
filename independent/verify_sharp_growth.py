#!/usr/bin/env python3
"""Independent bounded checks for Theorems 56 and 58.

This script uses raw `(n,q,r)` transitions and imports no project code.
It checks the parameterized rebound implication on arbitrary admissible
states, the finite sharp-growth inequality on literal starting orbits, and
the finite low-window count used for sparse down-steps. These checks are
regressions, not proofs of the asymptotic theorems.
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


def check_explicit_rate() -> int:
    checked = 0
    for start in (31_873, 1_320_111):
        state = enter(start)
        entry_n = state.n
        for _ in range(100_000):
            if state.r == state.q:
                break
            scale = state.n.bit_length()
            log_scale = scale.bit_length() - 1
            if log_scale >= 4:
                assert (
                    (log_scale - 1)
                    * scale
                    * (state.q + entry_n + 5)
                    >= (log_scale - 3) * state.n
                )
                checked += 1
            state = step(state)
    return checked


def check_floor_endpoints() -> int:
    checked = 0
    for scale in range(16, 1_000_001):
        log_scale = scale.bit_length() - 1
        rebound_len = log_scale - 2
        numerator = rebound_len - 1
        denominator = rebound_len + 1
        cascade_scale = 1 << (rebound_len + 2)
        assert rebound_len >= 2
        assert cascade_scale <= scale
        assert denominator * scale >= numerator * cascade_scale
        assert numerator == log_scale - 3
        assert denominator == log_scale - 1
        checked += 1
    return checked


def check_low_window_counts() -> int:
    checked = 0
    for initial_n in (128, 256, 512):
        stride = initial_n // 32
        for initial_q in range(1, 9):
            for initial_r in range(0, initial_n, stride):
                state = State(initial_n, initial_q, initial_r)
                counts = {length: [0, 0] for length in range(2, 8)}
                for _ in range(500):
                    change = digit(state)
                    for length, (changes, downs) in counts.items():
                        if state.n < (1 << (length + 2)) * state.q:
                            counts[length] = [0, 0]
                            continue
                        changes += change != 0
                        downs += change == -1
                        assert (length + 1) * downs <= changes + length
                        counts[length] = [changes, downs]
                        checked += 1
                    state = step(state)
    return checked


def main() -> None:
    cascades = check_parameterized_cascades()
    growth = check_finite_growth()
    explicit = check_explicit_rate()
    endpoints = check_floor_endpoints()
    windows = check_low_window_counts()
    assert cascades > 1_000
    assert growth > 100_000
    assert explicit > 100_000
    assert endpoints > 900_000
    assert windows > 100_000
    print(f"parameterized rebound cascades checked: {cascades}")
    print(f"finite sharp-growth inequalities checked: {growth}")
    print(f"explicit unit-leading rate checks: {explicit}")
    print(f"floor-threshold endpoints checked: {endpoints}")
    print(f"low-window counting prefixes checked: {windows}")
    print(
        "VERDICT: bounded raw checks agree with Theorems 56/58 "
        "and Corollaries 57/59."
    )


if __name__ == "__main__":
    main()
