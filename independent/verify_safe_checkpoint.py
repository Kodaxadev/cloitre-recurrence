#!/usr/bin/env python3
"""Independent bounded checks for Theorem 46, Lemma 47, and Corollary 48.

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


def main() -> None:
    signed_checked = 0
    dominance_checked = 0
    parity_predecessors_checked = 0
    for n in range(2, 151):
        for q in range(n):
            for e in range(1, n - q):
                state = State(n=n, q=q, e=e)
                check_signed_form(state)
                signed_checked += 1
                if raw_safe_step(state) is not None:
                    check_local_dominance(state)
                    dominance_checked += 1

        if n >= 3:
            for e in range(2, n, 2):
                predecessor = State(n=n - 1, q=0, e=e // 2)
                outcome = raw_safe_step(predecessor)
                assert outcome == ("zero", State(n=n, q=0, e=e))
                parity_predecessors_checked += 1

    print(f"signed states checked: {signed_checked}")
    print(f"continuing dominance states checked: {dominance_checked}")
    print(f"even-witness predecessors checked: {parity_predecessors_checked}")
    print(
        "VERDICT: bounded raw checks agree with Theorem 46, "
        "Lemma 47, and Corollary 48."
    )


if __name__ == "__main__":
    main()
