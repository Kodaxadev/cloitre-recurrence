#!/usr/bin/env python3
"""Independent bounded checks for Theorems 46/50 and Lemmas 47/49/51.

This verifier uses raw `(n,q,e)` inequalities and imports no project code.
It is a finite regression check, not the proof of either symbolic statement.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    n: int
    q: int
    e: int

    def valid(self) -> bool:
        return self.n >= 2 and self.q >= 0 and 0 < self.e < self.n - self.q


def raw_safe_step(state: State) -> tuple[str, State] | None:
    assert state.valid()
    doubled = 2 * state.e
    modulus = state.n + 2
    if doubled > modulus:
        next_state = State(
            n=state.n + 1,
            q=state.q + 1,
            e=doubled - modulus,
        )
        assert next_state.valid()
        return "wrap", next_state
    if state.q + doubled < state.n + 1:
        next_state = State(
            n=state.n + 1,
            q=state.q,
            e=doubled,
        )
        assert next_state.valid()
        return "zero", next_state
    return None


def check_signed_form(state: State) -> None:
    s = state.n + 2
    x = s + 1 - 2 * state.e
    assert abs(x) < s
    assert (x - s - 1) % 2 == 0
    outcome = raw_safe_step(state)

    if x >= state.q + 3:
        assert outcome is not None and outcome[0] == "zero"
        next_s = outcome[1].n + 2
        next_x = next_s + 1 - 2 * outcome[1].e
        assert next_s == s + 1
        assert next_x == 2 * x - s
        assert outcome[1].q == state.q
    elif x <= 0:
        assert outcome is not None and outcome[0] == "wrap"
        next_s = outcome[1].n + 2
        next_x = next_s + 1 - 2 * outcome[1].e
        assert next_s == s + 1
        assert next_x == 2 * x + s
        assert outcome[1].q == state.q + 1
    else:
        assert 1 <= x <= state.q + 2
        assert outcome is None


def check_local_dominance(state: State) -> None:
    outcome = raw_safe_step(state)
    if outcome is None:
        return
    zero = State(n=state.n, q=0, e=state.e)
    zero_outcome = raw_safe_step(zero)
    assert zero_outcome is not None
    assert zero_outcome[0] == outcome[0]
    assert zero_outcome[1].e == outcome[1].e
    assert outcome[1].q - zero_outcome[1].q == state.q


def check_clearance_prefix(n: int, e: int, shift: int) -> int:
    base = State(n=n, q=0, e=e)
    shifted = State(n=n, q=shift, e=e)
    compared = 0
    for _ in range(500):
        base_outcome = raw_safe_step(base)
        if base_outcome is None:
            return compared

        kind, base_next = base_outcome
        shifted_outcome = raw_safe_step(shifted)
        if kind == "zero":
            slack = base.n - base.q - 2 * base.e
            if slack < shift:
                assert shifted_outcome is None
                return compared

        assert shifted_outcome is not None
        assert shifted_outcome[0] == kind
        assert shifted_outcome[1].e == base_next.e
        assert shifted_outcome[1].q - base_next.q == shift
        base = base_next
        shifted = shifted_outcome[1]
        compared += 1
    return compared


def check_even_checkpoint_predecessors(n: int, e: int) -> bool:
    assert n >= 8 and n % 2 == 0 and e % 2 == 1
    witness = State(n=n, q=0, e=e)
    witness_outcome = raw_safe_step(witness)
    if witness_outcome is None:
        return False

    if witness_outcome[0] == "wrap":
        f = e - (n + 2) // 2
        assert 1 <= f <= n // 2 - 2
        shifted_low = State(n=n, q=1, e=f)
        assert raw_safe_step(shifted_low) == (
            "zero",
            witness_outcome[1],
        )
        if f % 2 == 0:
            predecessor = State(n=n - 1, q=0, e=f // 2)
            assert raw_safe_step(predecessor) == (
                "zero",
                State(n=n, q=0, e=f),
            )
        else:
            predecessor = State(n=n - 1, q=0, e=(f + n + 1) // 2)
            assert raw_safe_step(predecessor) == (
                "wrap",
                shifted_low,
            )
        return True
    else:
        assert 2 * e <= n
        predecessor = State(n=n - 1, q=0, e=(e + n + 1) // 2)
        assert raw_safe_step(predecessor) == (
            "wrap",
            State(n=n, q=1, e=e),
        )
        return True


def check_zero_acceleration(
    state: State,
) -> tuple[int, int, State, tuple[str, State] | None]:
    first = raw_safe_step(state)
    assert first is not None and first[0] == "zero"
    width = state.n - state.q
    slack = width - 2 * state.e
    assert slack >= 0

    current = first[1]
    wraps = 0
    while True:
        outcome = raw_safe_step(current)
        if outcome is None or outcome[0] != "wrap":
            break
        current = outcome[1]
        wraps += 1

    for j in range(wraps):
        assert (1 << (j + 1)) * (state.q + slack + 4) < (
            width + state.q + j + 5
        )
    assert (1 << (wraps + 1)) * (state.q + slack + 4) >= (
        width + state.q + wraps + 5
    )

    candidate = (
        (1 << (wraps + 1)) * (state.q + slack + 4)
        - width
        - 2 * state.q
        - 2 * wraps
        - 7
    )
    assert current.n - current.q == width + 1
    assert current.q == state.q + wraps
    if outcome is None:
        assert candidate < 0
    else:
        assert outcome[0] == "zero"
        assert candidate >= 0
        assert current.n - current.q - 2 * current.e == candidate
    return wraps, candidate, current, outcome


def check_boundary_equalities() -> int:
    checked = 0
    for q in range(51):
        for wraps in range(1, 9):
            e = ((1 << wraps) - 1) * (q + 4) - wraps
            state = State(n=2 * e + q, q=q, e=e)
            actual_wraps, slack, current, outcome = check_zero_acceleration(state)
            assert actual_wraps == wraps
            assert slack == 1
            assert current.e == e
            assert outcome is not None and outcome[0] == "zero"
            checked += 1
    return checked


def check_boundary_growth_example() -> None:
    states = [
        State(n=14, q=0, e=7),
        State(n=15, q=0, e=14),
        State(n=16, q=1, e=11),
        State(n=17, q=2, e=4),
        State(n=18, q=2, e=8),
    ]
    digits = ["zero", "wrap", "wrap", "zero"]
    for before, digit, after in zip(states, digits, states[1:]):
        assert raw_safe_step(before) == (digit, after)
    assert states[0].n - states[0].q - 2 * states[0].e == 0
    assert states[-1].n - states[-1].q - 2 * states[-1].e == 0
    assert states[-1].e > states[0].e


def lifetime(state: State, limit: int) -> int:
    for steps in range(limit):
        outcome = raw_safe_step(state)
        if outcome is None:
            return steps
        state = outcome[1]
    raise AssertionError(f"state did not terminate within {limit}: {state}")


def main() -> None:
    signed_checked = 0
    dominance_checked = 0
    parity_predecessors_checked = 0
    clearance_transitions_checked = 0
    even_predecessors_checked = 0
    zero_epochs_checked = 0
    accelerated_wraps_checked = 0
    for n in range(2, 151):
        for q in range(n):
            for e in range(1, n - q):
                state = State(n=n, q=q, e=e)
                check_signed_form(state)
                signed_checked += 1
                outcome = raw_safe_step(state)
                if outcome is not None:
                    check_local_dominance(state)
                    dominance_checked += 1
                    if n <= 100 and outcome[0] == "zero":
                        wraps, _, _, _ = check_zero_acceleration(state)
                        zero_epochs_checked += 1
                        accelerated_wraps_checked += wraps

        if n >= 3:
            for e in range(2, n, 2):
                predecessor = State(n=n - 1, q=0, e=e // 2)
                outcome = raw_safe_step(predecessor)
                assert outcome == ("zero", State(n=n, q=0, e=e))
                parity_predecessors_checked += 1

        for e in range(1, n):
            for shift in range(1, min(5, n - e)):
                clearance_transitions_checked += check_clearance_prefix(
                    n,
                    e,
                    shift,
                )

        if n >= 8 and n % 2 == 0:
            for e in range(1, n, 2):
                even_predecessors_checked += check_even_checkpoint_predecessors(n, e)

    equality_cases_checked = check_boundary_equalities()
    check_boundary_growth_example()

    for n in (2, 4, 6):
        for e in range(1, n):
            lifetime(State(n=n, q=0, e=e), 100)

    print(f"signed states checked: {signed_checked}")
    print(f"continuing dominance states checked: {dominance_checked}")
    print(f"even-witness predecessors checked: {parity_predecessors_checked}")
    print(f"clearance transitions checked: {clearance_transitions_checked}")
    print(f"even-checkpoint constructions checked: {even_predecessors_checked}")
    print(f"accelerated zero epochs checked: {zero_epochs_checked}")
    print(f"wrap transitions accelerated: {accelerated_wraps_checked}")
    print(f"boundary equality cases checked: {equality_cases_checked}")
    print(
        "VERDICT: bounded raw checks agree with Theorems 46/50, "
        "Lemmas 47/49/51, and Corollaries 48/52."
    )


if __name__ == "__main__":
    main()
