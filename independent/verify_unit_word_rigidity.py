#!/usr/bin/env python3
"""Independent bounded checks for Lemma 123.

The raw safe-map implementation is reused only to obtain finite unit-block
words.  The coefficient recurrence below is implemented directly.  These
checks support the exact identity, not Corollary 124's asymptotic counting.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
from runpy import run_path


RAW = run_path(str(Path(__file__).with_name("verify_general_gate_boundaries.py")))
State = RAW["State"]
zero_blocks = RAW["zero_blocks"]


def coefficients(gaps: tuple[int, ...]) -> tuple[int, int, int, int]:
    shift = 0
    p_coeff = 1
    b_coeff = 0
    c_coeff = 0
    for gap in gaps:
        scale = 1 << (gap + 2)
        p_coeff *= scale
        b_coeff = scale * b_coeff + 1
        c_coeff = scale * c_coeff + shift + gap + 5
        shift += gap + 2
    return shift, p_coeff, b_coeff, c_coeff


def evolve(start_n: int, start_f: int, gaps: tuple[int, ...]) -> tuple[int, int]:
    index = start_n
    residue = start_f
    for gap in gaps:
        residue = (1 << (gap + 2)) * residue - index - gap - 5
        index += gap + 2
    return index, residue


def check_algebraic_words() -> int:
    checked = 0
    for length in range(1, 6):
        for gaps in product(range(4), repeat=length):
            shift, p_coeff, b_coeff, c_coeff = coefficients(gaps)
            assert b_coeff > 0
            for start_n in range(2, 41):
                for start_f in range(1, 11):
                    end_n, end_f = evolve(start_n, start_f, gaps)
                    assert end_n == start_n + shift
                    assert end_f == (
                        p_coeff * start_f - b_coeff * start_n - c_coeff
                    )
                    numerator = p_coeff * start_f - c_coeff - end_f
                    assert numerator == b_coeff * start_n
                    checked += 1
    return checked


def positive_indices(blocks: list[object]) -> list[int]:
    return [
        index
        for index, block in enumerate(blocks)
        if block.wraps > 0 and block.next_zero is not None
    ]


def check_raw_words() -> tuple[int, int]:
    checked = 0
    endpoint_keys: dict[tuple[int, int, tuple[int, ...]], int] = {}
    for initial_n in range(2, 121):
        for initial_e in range(1, initial_n):
            blocks = zero_blocks(State(initial_n, 0, initial_e))
            positive = positive_indices(blocks)
            for start in range(len(positive)):
                for length in range(1, min(6, len(positive) - start) + 1):
                    window = positive[start : start + length + 1]
                    if len(window) != length + 1:
                        continue
                    parents = [blocks[index] for index in window]
                    if any(block.wraps != 1 for block in parents):
                        continue
                    gaps = tuple(
                        right - left - 1
                        for left, right in zip(window, window[1:])
                    )
                    residues = tuple(
                        block.next_zero.e for block in parents
                    )
                    start_n = parents[0].start.n
                    end_n, end_f = evolve(start_n, residues[0], gaps)
                    assert end_n == parents[-1].start.n
                    assert end_f == residues[-1]

                    _, p_coeff, b_coeff, c_coeff = coefficients(gaps)
                    recovered = (
                        p_coeff * residues[0] - c_coeff - residues[-1]
                    )
                    assert recovered % b_coeff == 0
                    assert recovered // b_coeff == start_n

                    key = (residues[0], residues[-1], gaps)
                    previous = endpoint_keys.setdefault(key, start_n)
                    assert previous == start_n
                    checked += 1
    return checked, len(endpoint_keys)


def main() -> None:
    algebraic = check_algebraic_words()
    raw, keys = check_raw_words()
    assert algebraic == 531_960
    assert raw == 13_214
    assert keys == 907
    print(f"algebraic fixed-word identities checked: {algebraic}")
    print(f"raw unit-block words checked: {raw}")
    print(f"distinct endpoint-word keys checked: {keys}")
    print(
        "VERDICT: bounded independent checks agree with Lemma 123; "
        "Corollary 124 remains a symbolic asymptotic consequence."
    )


if __name__ == "__main__":
    main()
