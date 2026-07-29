#!/usr/bin/env python3
"""Independent checks that the all-unit pure-upper subsystem is deterministic.

No project code is imported.  The raw safe map is reimplemented here from the
definition, and the reduced map on ``(n, U, f)`` is checked against literal
safe-map traces.  The exhaustive orbit sweep is finite evidence within its
displayed bounds, not a proof.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Raw safe map, reimplemented from the definition.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class State:
    n: int
    q: int
    e: int


def raw_step(state: State) -> tuple[str, State] | None:
    doubled = 2 * state.e
    if doubled > state.n + 2:
        return "wrap", State(state.n + 1, state.q + 1, doubled - state.n - 2)
    if state.q + doubled < state.n + 1:
        return "zero", State(state.n + 1, state.q, doubled)
    return None


def raw_digits(state: State, budget: int) -> tuple[list[str], list[State]]:
    """Return the safe digit word and visited states, up to ``budget`` steps."""
    word: list[str] = []
    seen = [state]
    current = state
    for _ in range(budget):
        outcome = raw_step(current)
        if outcome is None:
            break
        word.append(outcome[0])
        current = outcome[1]
        seen.append(current)
    return word, seen


# ---------------------------------------------------------------------------
# Reduced unit-block coordinates.
# ---------------------------------------------------------------------------


def is_unit_state(n: int, u: int, f: int) -> bool:
    """Lemma 117: (n, U, f) reconstructs a returning unit positive block."""
    d_coord = n - 2 * u
    return (
        n >= 2
        and u >= 0
        and f >= 1
        and (n + 3 + f) % 4 == 0
        and f <= d_coord - 3
        and 4 * f <= n + d_coord + 2
    )


def minimal_exponent(n: int, f: int) -> int:
    """Least h >= 2 with 2^h f >= n + h + 4 (monotone in h)."""
    h = 2
    while (f << h) < n + h + 4:
        h += 1
    return h


def gate(n: int, u: int, f: int) -> tuple[int, int, int, int] | None:
    """The unique pure-upper unit gate out of (n, U, f), if any.

    Returns ``(h, g, n', U')`` where h = r + 2.
    """
    d_coord = n - 2 * u
    defect = d_coord - 3 - f
    if defect < 4 or defect % 2 != 0:
        return None
    h = minimal_exponent(n, f)
    g = (f << h) - n - h - 3
    if g < 1 or g > (1 << (h + 2)):
        return None
    child_d = d_coord + h - 2
    if child_d - 3 - g < (1 << (h + 2)):
        return None
    return h, g, n + h, u + 1


def all_gates(n: int, u: int, f: int, h_max: int) -> list[int]:
    """Every h in [2, h_max] passing the full pure-upper test."""
    d_coord = n - 2 * u
    defect = d_coord - 3 - f
    if defect < 4 or defect % 2 != 0:
        return []
    found = []
    for h in range(2, h_max + 1):
        g = (f << h) - n - h - 3
        if g < 1 or g > (1 << (h + 2)):
            continue
        if (d_coord + h - 2) - 3 - g < (1 << (h + 2)):
            continue
        found.append(h)
    return found


# ---------------------------------------------------------------------------
# Check 1: the reduced gate agrees with literal safe-map traces.
# ---------------------------------------------------------------------------


def literal_unit_gate(n: int, u: int, f: int) -> tuple[int, int] | None:
    """Read (h, g) off a raw safe-map trace, or None if the shape fails."""
    e = (n + 3 + f) // 4
    word, seen = raw_digits(State(n, u, e), 4096)
    # Expected shape: zero, wrap, then r zeros, then wrap, then a zero.
    if len(word) < 3 or word[0] != "zero" or word[1] != "wrap":
        return None
    if seen[2].e != f:
        return None
    index = 2
    zeros = 0
    while index < len(word) and word[index] == "zero":
        zeros += 1
        index += 1
    if index >= len(word) or word[index] != "wrap":
        return None
    if index + 1 >= len(word) or word[index + 1] != "zero":
        return None
    child_start = seen[2 + zeros - 1] if zeros >= 1 else None
    if child_start is None:
        return None
    returned = seen[index + 1].e
    return zeros + 1, returned


def check_literal_agreement(n_max: int) -> tuple[int, int]:
    matched = 0
    states = 0
    for n in range(6, n_max + 1):
        for u in range(0, (n - 6) // 2 + 1):
            d_coord = n - 2 * u
            if d_coord < 8:
                continue
            for f in range(1, d_coord - 2):
                if not is_unit_state(n, u, f):
                    continue
                states += 1
                reduced = gate(n, u, f)
                literal = literal_unit_gate(n, u, f)
                if reduced is None:
                    continue
                h, g, _, _ = reduced
                assert literal is not None, (n, u, f, h, g)
                assert literal == (h, g), (n, u, f, reduced, literal)
                matched += 1
    return states, matched


# ---------------------------------------------------------------------------
# Check 2: determinism -- at most one admissible exponent.
# ---------------------------------------------------------------------------


def check_determinism(n_max: int, h_max: int) -> tuple[int, int]:
    states = 0
    live = 0
    for n in range(6, n_max + 1):
        for u in range(0, (n - 6) // 2 + 1):
            d_coord = n - 2 * u
            if d_coord < 8:
                continue
            for f in range(1, d_coord - 2):
                if not is_unit_state(n, u, f):
                    continue
                states += 1
                found = all_gates(n, u, f, h_max)
                assert len(found) <= 1, (n, u, f, found)
                if found:
                    live += 1
                    reduced = gate(n, u, f)
                    assert reduced is not None, (n, u, f, found)
                    assert reduced[0] == found[0], (n, u, f, reduced, found)
                else:
                    assert gate(n, u, f) is None, (n, u, f)
    return states, live


# ---------------------------------------------------------------------------
# Check 3: exhaustive forward orbits of the deterministic map.
# ---------------------------------------------------------------------------


def orbit_length(n: int, u: int, f: int, cap: int) -> int:
    """Number of successive pure-upper unit gates taken from (n, U, f)."""
    length = 0
    while length < cap:
        nxt = gate(n, u, f)
        if nxt is None:
            return length
        _, g, n, u = nxt
        f = g
        length += 1
    return cap


def least_starts(n_max: int) -> dict[int, tuple[int, int]]:
    """Least (start index, residue) per chain length, via (132.2).

    Condition M pins f to about four consecutive integers once (n, h) is fixed,
    so this enumerates every state with an outgoing gate in O(N log N).
    """
    table: dict[int, tuple[int, int]] = {}
    for n in range(6, n_max + 1):
        h = 2
        while (1 << (h + 2)) <= n + h:
            power = 1 << h
            low = -(-(n + h + 4) // power)
            high = (n + h + 3 + (1 << (h + 2))) // power
            for f in range(max(1, low), high + 1):
                if (n + 3 + f) % 4 != 0:
                    continue
                if gate(n, 0, f) is None:
                    continue
                length = orbit_length(n, 0, f, 4096)
                if length not in table or table[length][0] > n:
                    table[length] = (n, f)
            h += 1
    return table


def sweep(n_max: int, cap: int) -> tuple[int, tuple[int, int, int], int]:
    """Brute-force scan over every residue, as a cross-check on least_starts."""
    best = 0
    argbest = (0, 0, 0)
    total = 0
    for n in range(6, n_max + 1):
        for u in range(0, (n - 6) // 2 + 1):
            d_coord = n - 2 * u
            if d_coord < 8:
                continue
            for f in range(1, d_coord - 2):
                if not is_unit_state(n, u, f):
                    continue
                total += 1
                length = orbit_length(n, u, f, cap)
                if length > best:
                    best = length
                    argbest = (n, u, f)
    return best, argbest, total


def main() -> int:
    literal_bound = int(sys.argv[1]) if len(sys.argv) > 1 else 240
    determinism_bound = int(sys.argv[2]) if len(sys.argv) > 2 else 700
    sweep_bound = int(sys.argv[3]) if len(sys.argv) > 3 else 2000

    states, matched = check_literal_agreement(literal_bound)
    print(f"literal agreement: {states} unit states, {matched} live gates")

    states, live = check_determinism(determinism_bound, 40)
    print(f"determinism: {states} unit states, {live} with a unique exponent")

    best, argbest, total = sweep(determinism_bound, 4096)
    print(
        f"brute-force sweep n<={determinism_bound}: {total} states, "
        f"longest chain {best} at {argbest}"
    )

    # The two enumerations must agree wherever both are complete.
    coarse = least_starts(determinism_bound)
    assert coarse.get(best, (None, None))[0] == argbest[0], (coarse, argbest)
    table = least_starts(sweep_bound)
    for length in sorted(table):
        start, residue = table[length]
        if length in coarse:
            assert coarse[length] == (start, residue), (length, coarse[length])
        print(f"  chain length {length}: least start n={start}, f={residue}")
    print(f"exponent-indexed sweep n<={sweep_bound}: longest chain {max(table)}")

    print(
        "VERDICT: bounded raw states agree with Theorem 130; the forced gate "
        "matches literal safe-map traces and no state has two admissible "
        "exponents. The chain ceiling is computational, not a theorem."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
