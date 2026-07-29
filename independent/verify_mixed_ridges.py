#!/usr/bin/env python3
"""Independent bounded checks for Lemmas 73 and 76 and Corollary 74.

This script uses raw ``(n,q,r)`` transitions and imports no project code.
The finite grids are regression checks for the exact mixed-ridge formulas,
not proofs of the symbolic statements or of recurrence stabilization.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    n: int
    q: int
    r: int

    def absorbed(self) -> bool:
        return self.r == self.q


@dataclass(frozen=True)
class Ridge:
    start: State
    end: State
    prefix: int
    defect: int
    value: int
    suffix_zeros: int
    terminal_run: int
    width: int
    mixed: bool


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


def ridge(parent: State, limit: int = 2_000) -> Ridge | None:
    assert digit(parent) == -1
    start = step(parent)
    current = start
    states = [start]
    changes: list[int] = []

    for _ in range(limit):
        if current.absorbed() or digit(current) == -1:
            break
        changes.append(digit(current))
        current = step(current)
        states.append(current)
    else:
        return None

    if current.absorbed() or digit(current) != -1 or 1 not in changes:
        return None

    last_up = max(i for i, change in enumerate(changes) if change == 1)
    assert all(change == 0 for change in changes[last_up + 1 :])
    prefix = last_up + 1
    positive_zeros = [
        i for i, change in enumerate(changes[:prefix]) if change == 0
    ]
    defect = sum(
        (start.n + offset + 2) << (prefix - 1 - offset)
        for offset in positive_zeros
    )
    value = states[prefix].q - states[prefix].r
    suffix_zeros = len(changes) - prefix
    width = start.q + start.n - start.r + 3
    if positive_zeros:
        terminal_run = prefix - 1 - positive_zeros[-1]
    else:
        terminal_run = prefix

    assert value >= 1
    assert (1 << prefix) * width - defect == (
        start.n + prefix + 3 + value
    )
    terminal_quotient = states[prefix].q
    assert suffix_zeros == (terminal_quotient // value).bit_length() - 1

    next_start = step(current)
    next_width = next_start.q + next_start.n - next_start.r + 3
    assert next_width == (1 << (suffix_zeros + 1)) * value + 2
    assert defect % (1 << terminal_run) == 0
    if positive_zeros:
        last_zero = positive_zeros[-1]
        last_zero_index = start.n + last_zero
        last_zero_e = states[last_zero].r - states[last_zero].q
        assert (1 << terminal_run) * (
            last_zero_index + 4 - 2 * last_zero_e
        ) == (
            last_zero_index + terminal_run + 4 + value
        )
        for up_offset in range(terminal_run + 1):
            ladder_state = states[last_zero + 1 + up_offset]
            assert (
                ladder_state.n + 3 - (ladder_state.r - ladder_state.q)
                == (1 << up_offset)
                * (last_zero_index + 4 - 2 * last_zero_e)
            )
        assert (defect >> terminal_run) % 2 == (
            start.n + last_zero + 2
        ) % 2

    return Ridge(
        start=start,
        end=current,
        prefix=prefix,
        defect=defect,
        value=value,
        suffix_zeros=suffix_zeros,
        terminal_run=terminal_run,
        width=width,
        mixed=bool(positive_zeros),
    )


def check_grid() -> tuple[int, int, int, Counter[int]]:
    checked = 0
    mixed = 0
    adjacent = 0
    mixed_runs: Counter[int] = Counter()

    for n in (64, 128, 256, 512, 1024):
        for quotient in range(1, min(81, n + 1)):
            for remainder in range((quotient + 1) // 2):
                first = ridge(State(n, quotient, remainder))
                if first is None:
                    continue
                checked += 1
                if first.mixed:
                    mixed += 1
                    mixed_runs[first.terminal_run] += 1

                second = ridge(first.end)
                if second is None:
                    continue
                adjacent += 1
                first_base = (
                    (1 << first.prefix) * first.width - first.defect
                )
                next_start = step(first.end)
                next_width = (
                    next_start.q + next_start.n - next_start.r + 3
                )
                second_base = (
                    (1 << second.prefix) * next_width - second.defect
                )
                assert (
                    first_base
                    + first.suffix_zeros
                    + second.prefix
                    + 1
                    + second.value
                    - first.value
                    == second_base
                )
                representative = (
                    first.suffix_zeros
                    + second.prefix
                    + 1
                    + second.value
                    - first.value
                )
                modulus = 1 << min(
                    first.terminal_run, second.terminal_run
                )
                assert representative % modulus == 0

    return checked, mixed, adjacent, mixed_runs


def check_long_low_terminal_run_prefix() -> None:
    current = State(64, 4, 0)
    for _ in range(100):
        segment = ridge(current)
        assert segment is not None
        assert segment.terminal_run <= 2
        current = segment.end
    assert current == State(878, 215, 55)


def check_small_start_unreachability() -> None:
    target = 256
    for initial in range(1, target + 1):
        value = initial
        for index in range(1, 64):
            value += value % index
        assert value != target


def main() -> None:
    checked, mixed, adjacent, mixed_runs = check_grid()
    check_long_low_terminal_run_prefix()
    check_small_start_unreachability()
    assert checked > 6_000
    assert mixed > 5_000
    assert adjacent > 6_000
    print(f"mixed-ridge finite segments checked: {checked}")
    print(f"segments with positive-prefix zeros: {mixed}")
    print(f"adjacent compatibility equations checked: {adjacent}")
    print(f"mixed terminal-run histogram: {dict(sorted(mixed_runs.items()))}")
    print("literal consecutive ridges with terminal run <= 2 checked: 100")
    print(
        "VERDICT: bounded raw checks agree with Lemmas 73/76, Corollary 74, "
        "and the local limitation used by Theorems 75/77."
    )


if __name__ == "__main__":
    main()
