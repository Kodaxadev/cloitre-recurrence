#!/usr/bin/env python3
"""Bounded raw checks of canonical gates, multiplicity, and residue transfer.

The transition and candidate routines are loaded from the independent raw
gate verifier, not from project dynamics code. The finite census checks the
new identities and iff classification; it is not a termination proof.
"""

from __future__ import annotations

from math import gcd
from pathlib import Path
from runpy import run_path


RAW = run_path(str(Path(__file__).with_name("verify_general_gate_boundaries.py")))
State = RAW["State"]
candidates = RAW["candidates"]
step = RAW["step"]
zero_blocks = RAW["zero_blocks"]


def positive_pairs(blocks: list[object]) -> list[tuple[int, int]]:
    positive = [
        index
        for index, block in enumerate(blocks)
        if block.wraps > 0 and block.next_zero is not None
    ]
    return list(zip(positive, positive[1:]))


def canonical_origin(n: int, k: int, r: int) -> tuple[int, int]:
    spacing = 1 << (k + r + 3)
    expression = (
        (1 << (r + 2)) * (n + k + 4)
        - (1 << (k + r + 2)) * n
        - n
        - k
        - r
        - 4
    )
    residue = expression % spacing
    return residue or spacing, spacing


def unit_conditions(n: int, quotient: int, returned_residue: int) -> bool:
    gap_coordinate = n - 2 * quotient
    return (
        (n + 3 + returned_residue) % 4 == 0
        and returned_residue >= 1
        and returned_residue <= gap_coordinate - 3
        and 4 * returned_residue <= n + gap_coordinate + 2
    )


def check_unit_state(block: object) -> None:
    """Verify Lemma 117 directly on one returning unit block."""
    returned = block.next_zero
    assert block.wraps == 1 and returned is not None
    n = block.start.n
    quotient = block.start.q
    returned_residue = returned.e
    gap_coordinate = n - 2 * quotient
    defect = n - quotient - 2 * block.start.e

    assert unit_conditions(n, quotient, returned_residue)
    assert block.start.e == (n + 3 + returned_residue) // 4
    assert defect == (gap_coordinate - 3 - returned_residue) // 2


def check_unit_reconstruction() -> tuple[int, int]:
    """Exhaust both directions of Lemma 117 on arbitrary bounded states."""
    literal = 0
    reconstructed = 0
    for n in range(2, 121):
        for quotient in range(n):
            for residue in range(1, n - quotient):
                first = step(State(n, quotient, residue))
                if first is None or first[0] != "zero":
                    continue
                second = step(first[1])
                if second is None or second[0] != "wrap":
                    continue
                third = step(second[1])
                if third is None or third[0] != "zero":
                    continue
                returned_residue = second[1].e
                assert unit_conditions(n, quotient, returned_residue)
                assert residue == (n + 3 + returned_residue) // 4
                literal += 1
            for returned_residue in range(1, n + 1):
                if not unit_conditions(n, quotient, returned_residue):
                    continue
                residue = (n + 3 + returned_residue) // 4
                first = step(State(n, quotient, residue))
                assert first is not None and first[0] == "zero"
                second = step(first[1])
                assert second is not None and second[0] == "wrap"
                assert second[1].e == returned_residue
                third = step(second[1])
                assert third is not None and third[0] == "zero"
                reconstructed += 1
    assert literal == reconstructed
    return literal, reconstructed


def check_quotient_erasure() -> int:
    """Compare Lemma 116 with literal safe steps on a bounded corpus."""
    transitions = 0
    for n in range(2, 61):
        for quotient in range(n - 1):
            for residue in range(1, n - quotient):
                original = State(n, quotient, residue)
                lowered = State(n, 0, residue)
                for _ in range(80):
                    original_outcome = step(original)
                    if original_outcome is None:
                        break
                    lowered_outcome = step(lowered)
                    assert lowered_outcome is not None
                    original_digit, original = original_outcome
                    lowered_digit, lowered = lowered_outcome
                    assert lowered_digit == original_digit
                    assert lowered.n == original.n
                    assert lowered.e == original.e
                    assert lowered.q == original.q - quotient
                    transitions += 1
    return transitions


def check_raw_gates(
) -> tuple[int, int, int, int, int, int, int, int, int, dict[int, int]]:
    checked = 0
    band_checked = 0
    interior = 0
    interior_unique = 0
    interior_nonunique = 0
    multiplicities: dict[int, int] = {}
    upper_nonunique = 0
    unit_transfers = 0
    unit_states = 0
    critical_pairs = 0
    for initial_n in range(2, 121):
        for initial_e in range(1, initial_n):
            blocks = zero_blocks(State(initial_n, 0, initial_e))
            for block in blocks:
                if block.wraps == 1 and block.next_zero is not None:
                    check_unit_state(block)
                    unit_states += 1
            previous_pure_unit_gap: int | None = None
            for left, right in positive_pairs(blocks):
                block = blocks[left]
                returned = block.next_zero
                assert returned is not None
                k = block.wraps
                r = right - left - 1
                parent_a = block.start.n + 4 - 2 * block.start.e
                parent_d = parent_a - block.start.q - 4

                rho, spacing = canonical_origin(block.start.n, k, r)
                excess = (
                    (1 << (r + 2)) * returned.e
                    - returned.n
                    - r
                    - 3
                )
                assert excess >= rho
                assert (excess - rho) % spacing == 0
                translate = (excess - rho) // spacing

                child = blocks[right].start
                child_gap = child.n - 2 * child.q
                child_d = child.n - child.q - 2 * child.e
                child_block = blocks[right]
                child_k = child_block.wraps
                child_returned = child_block.next_zero
                assert child_returned is not None
                child_a = child.n + 4 - 2 * child.e
                assert 2 * child_a == child.n + 5 - excess
                expected_returned = (
                    child.n
                    + child_k
                    + 4
                    - (1 << (child_k - 1)) * (child.n + 5 - excess)
                )
                assert child_returned.e == expected_returned
                if child_k == 1:
                    assert child_returned.e == excess
                    unit_transfers += 1
                assert child_gap - 3 == (
                    rho + translate * spacing + 2 * child_d
                )

                gate = candidates(returned.n, returned.q, k, r)
                assert translate <= block.start.e - 1
                lower_depth = translate
                upper_depth = min(parent_d // 2, (2 * child_d) // spacing)
                assert len(gate) == 1 + lower_depth + upper_depth
                assert (len(gate) - 1) * spacing <= child_gap - 3 - rho
                multiplicities[len(gate)] = multiplicities.get(len(gate), 0) + 1
                if parent_d >= 2 and 2 * child_d >= spacing:
                    assert (
                        1 << (k + r + child_k + 2)
                    ) < child.n + child_k + 4
                    upper_nonunique += 1
                pure_unit = (
                    k == 1
                    and child_k == 1
                    and translate == 0
                    and parent_d >= 2
                    and 2 * child_d >= spacing
                )
                if pure_unit:
                    if previous_pure_unit_gap is not None:
                        assert block.start.n < (
                            1 << (previous_pure_unit_gap + r + 6)
                        )
                        critical_pairs += 1
                    previous_pure_unit_gap = r
                else:
                    previous_pure_unit_gap = None
                if len(gate) == 1:
                    assert 2 * child_a == child.n + 5 - rho
                    assert (
                        (1 << (child_k - 1)) * (child.n + 5 - rho)
                        < child.n + child_k + 4
                    )
                    assert (
                        (1 << child_k) * (child.n + 5 - rho)
                        >= child.n + child_k + 5
                    )
                    assert (child_k == 1) == (2 * rho <= child.n + 4)
                    if child_k >= 2:
                        assert 2 * rho > child.n + 4
                        assert 2 * spacing > child.n + 4
                    band_checked += 1
                if parent_d < 2:
                    checked += 1
                    continue
                predicted_unique = (
                    rho <= child_gap - 3 < rho + spacing
                )
                assert predicted_unique == (len(gate) == 1)
                assert (child_gap - 3 >= rho + spacing) == (len(gate) >= 2)
                checked += 1
                interior += 1
                interior_unique += len(gate) == 1
                interior_nonunique += len(gate) >= 2
    return (
        checked,
        band_checked,
        interior,
        interior_unique,
        interior_nonunique,
        upper_nonunique,
        unit_transfers,
        unit_states,
        critical_pairs,
        multiplicities,
    )


def check_pure_upper_witness() -> int:
    blocks = zero_blocks(State(971, 5, 482))
    pairs = positive_pairs(blocks)
    expected = [
        (971, 5, 482, 6, 0, 2, 413),
        (978, 11, 277, 1, 1, 413, 461),
        (981, 12, 254, 1, 3, 461, 461),
        (986, 13, 256, 1, 3, 461, 417),
        (991, 14, 280, 1, 1, 417, 475),
        (994, 15, 252, 1, 5, 475, 281),
    ]
    for (left, right), wanted in zip(pairs[:6], expected, strict=True):
        parent = blocks[left]
        returned = parent.next_zero
        assert returned is not None
        child = blocks[right].start
        k = parent.wraps
        r = right - left - 1
        spacing = 1 << (k + r + 3)
        excess = (1 << (r + 2)) * returned.e - returned.n - r - 3
        parent_d = parent.start.n - parent.start.q - 2 * parent.start.e
        child_d = child.n - child.q - 2 * child.e
        assert (
            parent.start.n,
            parent.start.q,
            parent.start.e,
            k,
            r,
            parent_d,
            child_d,
        ) == wanted
        assert 1 <= excess <= spacing
        assert parent_d >= 2
        assert 2 * child_d >= spacing
    return len(expected)


def check_residue_permutations() -> int:
    checked = 0
    for k in range(1, 6):
        for r in range(6):
            spacing = 1 << (k + r + 3)
            coefficient = -(((1 << k) - 1) * (1 << (r + 2)) + 1)
            assert gcd(coefficient, spacing) == 1
            residues = {
                canonical_origin(n, k, r)[0]
                for n in range(spacing)
            }
            assert len(residues) == spacing
            checked += 1
    return checked


def main() -> None:
    (
        checked,
        band_checked,
        interior,
        unique,
        nonunique,
        upper_nonunique,
        unit_transfers,
        unit_states,
        critical_pairs,
        multiplicities,
    ) = check_raw_gates()
    quotient_erasure_steps = check_quotient_erasure()
    literal_units, reconstructed_units = check_unit_reconstruction()
    permutations = check_residue_permutations()
    pure_upper_run = check_pure_upper_witness()
    assert (checked, band_checked) == (27_030, 8_411)
    assert (interior, unique, nonunique) == (25_646, 7_380, 18_266)
    assert permutations == 30
    assert upper_nonunique == 12_021
    assert unit_transfers > 10_000
    assert unit_states == 18_852
    assert critical_pairs == 580
    assert quotient_erasure_steps == 166_156
    assert (literal_units, reconstructed_units) == (24_140, 24_140)
    assert pure_upper_run == 6
    assert multiplicities == {
        1: 8_411,
        2: 5_776,
        3: 4_578,
        4: 3_021,
        5: 1_127,
        6: 1_370,
        7: 2_204,
        8: 543,
    }
    print(f"raw gates canonically decomposed: {checked}")
    print(f"unique next-block bands checked: {band_checked}")
    print(f"interior raw gates classified: {interior}")
    print(f"unique first-window hits: {unique}")
    print(f"nonunique later-window hits: {nonunique}")
    print(f"complete bounded residue permutations checked: {permutations}")
    print(f"exact gate multiplicity histogram: {multiplicities}")
    print(f"upper-nonunique two-block ceilings checked: {upper_nonunique}")
    print(f"unit-child residue transfers checked: {unit_transfers}")
    print(f"returning unit states checked: {unit_states}")
    print(f"consecutive pure-unit critical pairs checked: {critical_pairs}")
    print(f"quotient-erasure safe steps checked: {quotient_erasure_steps}")
    print(
        "arbitrary-state unit iff checks: "
        f"{literal_units} literal / {reconstructed_units} reconstructed"
    )
    print(f"consecutive pure-upper witness length: {pure_upper_run}")
    print(
        "VERDICT: bounded raw gates agree with Lemma 103 and "
        "Corollaries 104--105, Lemmas 106/110/113, and "
        "Corollaries 107/111--112/114--115, Lemmas 116--117, and "
        "the local inequality in Theorem 118."
    )


if __name__ == "__main__":
    main()
