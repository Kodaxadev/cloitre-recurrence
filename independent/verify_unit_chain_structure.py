#!/usr/bin/env python3
"""Bounded raw checks for Lemma 131, Corollary 132 and the P126/P129 family.

The reduced map is reused from ``verify_unit_determinism.py``, which itself
imports no project implementation.  The sweeps are finite evidence within their
displayed bounds; the family check is exact arbitrary-precision arithmetic and
reproduces Propositions 126 and 129 independently of their proofs.
"""

from __future__ import annotations

import sys
from pathlib import Path
from runpy import run_path


CORE = run_path(str(Path(__file__).with_name("verify_unit_determinism.py")))
gate = CORE["gate"]
is_unit_state = CORE["is_unit_state"]
orbit_length = CORE["orbit_length"]


# ---------------------------------------------------------------------------
# Lemma 131: the wrap count is inert.
# ---------------------------------------------------------------------------


def check_wrap_inertness(n_max: int) -> tuple[int, int]:
    """Trajectories in (n, f) ignore U, and chain length decreases in U."""
    compared = 0
    strict = 0
    for n in range(6, n_max + 1):
        for u in range(1, (n - 6) // 2 + 1):
            if n - 2 * u < 8:
                continue
            for f in range(1, n - 2 * u - 2):
                if not is_unit_state(n, u, f):
                    continue
                raised = (n, u, f)
                lowered = (n, 0, f)
                while True:
                    step_raised = gate(*raised)
                    if step_raised is None:
                        break
                    step_lowered = gate(*lowered)
                    assert step_lowered is not None, (n, u, f, raised)
                    # Same exponent, same child residue, same child index.
                    assert step_raised[0] == step_lowered[0], (n, u, f)
                    assert step_raised[1] == step_lowered[1], (n, u, f)
                    assert step_raised[2] == step_lowered[2], (n, u, f)
                    raised = (step_raised[2], step_raised[3], step_raised[1])
                    lowered = (step_lowered[2], step_lowered[3], step_lowered[1])
                high = orbit_length(n, u, f, 4096)
                low = orbit_length(n, 0, f, 4096)
                assert high <= low, (n, u, f, high, low)
                compared += 1
                if high < low:
                    strict += 1
    return compared, strict


# ---------------------------------------------------------------------------
# Theorem 130: successors are unit states; (132.2) confines the residue.
# ---------------------------------------------------------------------------


def check_successor_and_window(n_max: int) -> tuple[int, int]:
    successors = 0
    window_hits = 0
    for n in range(6, n_max + 1):
        for u in range(0, (n - 6) // 2 + 1):
            if n - 2 * u < 8:
                continue
            for f in range(1, n - 2 * u - 2):
                if not is_unit_state(n, u, f):
                    continue
                found = gate(n, u, f)
                if found is None:
                    continue
                h, g, child_n, child_u = found
                assert is_unit_state(child_n, child_u, g), (n, u, f, found)
                assert child_n + 3 + g == (f << h), (n, u, f, found)
                successors += 1
                low = -(-(n + h + 4) // (1 << h))
                high = (n + h + 3) // (1 << h) + 4
                assert low <= f <= high, (n, u, f, h, low, high)
                window_hits += 1
    return successors, window_hits


# ---------------------------------------------------------------------------
# Corollary 132.2: a repeated (f, h) pair forces exact residue descent.
# ---------------------------------------------------------------------------


def check_repetition(n_max: int) -> tuple[int, int]:
    checked = 0
    longest = 0
    for n in range(6, n_max + 1):
        for f in range(1, n - 2):
            if not is_unit_state(n, 0, f):
                continue
            seen: dict[tuple[int, int], tuple[int, int]] = {}
            state = (n, 0, f)
            length = 0
            while True:
                found = gate(*state)
                if found is None:
                    break
                h, g, child_n, child_u = found
                key = (state[2], h)
                if key in seen:
                    prev_n, prev_g = seen[key]
                    assert g == prev_g - (child_n - prev_n), (n, f, key)
                    assert g < prev_g, (n, f, key)
                    checked += 1
                seen[key] = (child_n, g)
                state = (child_n, child_u, g)
                length += 1
            longest = max(longest, length)
    return checked, longest


# ---------------------------------------------------------------------------
# Propositions 126 and 129 through the deterministic map.
# ---------------------------------------------------------------------------


def check_family() -> int:
    cases = 0
    for a in range(7, 33):
        if a % 3 == 0:
            continue
        for q in (4, 16, 28, 40):
            if (q - 4 * a) % 12 != 0:
                continue
            span = 8 * q
            long_gap = span - 5
            power = 1 << span
            assert (a * (power - 1) + 24) % 9 == 0
            n_0 = (a * (power - 1) + 24) // 9 - span - 3
            assert (n_0 + 3 + a) % 8 == 0
            start = (n_0 + 3 + a) // 8
            middle = (a * (1 << (span - 3)) + a + 3) // 9
            # (126.7)
            assert middle == a * (1 << (span - 3)) - n_0 - span

            state = (n_0 - 3, 0, start)
            gaps: list[int] = []
            residues: list[int] = []
            while True:
                found = gate(*state)
                if found is None:
                    break
                h, g, child_n, child_u = found
                gaps.append(h - 2)
                residues.append(g)
                state = (child_n, child_u, g)
                if len(gaps) > 8:
                    break
            # Proposition 126: gaps (1, L, 1) and residues (a, c, a).
            assert gaps[:3] == [1, long_gap, 1], (a, q, gaps[:4])
            assert residues[:3] == [a, middle, a], (a, q)
            # Proposition 129: exactly one more forced gate, then no exit.
            assert len(gaps) == 4, (a, q, gaps)
            assert gaps[3] == long_gap, (a, q, gaps)
            assert residues[3] == middle - span, (a, q)
            cases += 1
    return cases


def main() -> int:
    bound = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    chain_bound = int(sys.argv[2]) if len(sys.argv) > 2 else 2000

    successors, window_hits = check_successor_and_window(bound)
    print(f"successors valid: {successors}; residue windows confirmed: {window_hits}")

    compared, strict = check_wrap_inertness(bound)
    print(f"wrap inertness: {compared} raised states, {strict} strictly shorter")

    checked, longest = check_repetition(chain_bound)
    print(f"repeated (f, h) descents: {checked}; longest chain seen: {longest}")

    cases = check_family()
    print(f"Proposition 126/129 family cases reproduced: {cases}")

    print(
        "VERDICT: bounded independent checks agree with Lemma 131 and "
        "Corollary 132, and the forced map reproduces Propositions 126 and 129 "
        "exactly; the chain ceiling remains computational."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
