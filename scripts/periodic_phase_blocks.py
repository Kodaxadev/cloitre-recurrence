#!/usr/bin/env python3
"""Check exact phase divisibility for Theorem 32 boundary block families."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256

from periodic_boundaries import Boundary, boundaries


@dataclass(frozen=True)
class Check:
    boundary: Boundary
    scale: int
    baseline_ratio: Fraction
    candidate_multiples: int
    passing_subsets: int


def ceil_div(numerator: int, denominator: int) -> int:
    return -((-numerator) // denominator)


def digits_for(states: list[int], denominator: int) -> list[int]:
    digits: list[int] = []
    for index, state in enumerate(states):
        following = states[(index + 1) % len(states)]
        numerator = 2 * state - following
        assert numerator % denominator == 0
        digits.append(numerator // denominator)
    return digits


def geometric_sum(base: int, count: int) -> int:
    return (base**count - 1) // (base - 1)


def is_subset_sum(value: int, base: int, length: int, count: int) -> bool:
    used = 0
    for _ in range(length):
        value, digit = divmod(value, base)
        if digit not in (0, 1):
            return False
        used += digit
    return value == 0 and used == count


def check_family(boundary: Boundary, scale: int) -> Check:
    d = boundary.denominator
    cycle = list(boundary.cycle)
    split = cycle.index(boundary.residue)
    cycle = cycle[split + 1 :] + cycle[: split + 1]
    length = len(cycle)
    repeats = boundary.min_repeats * scale
    choices = boundary.numerator * repeats // d
    period = length * repeats
    base = 1 << length

    positive_states = [value - d if value > boundary.residue else value for value in cycle]
    negative_states = positive_states.copy()
    assert positive_states[-1] == boundary.residue
    negative_states[-1] -= d
    positive_digits = digits_for(positive_states, d)
    negative_digits = digits_for(negative_states, d)
    assert sum(
        left - right for left, right in zip(negative_digits, positive_digits)
    ) == -1

    target_sum = period * (d - boundary.residue) // d
    observed_sum = (
        (repeats - choices) * sum(positive_digits)
        + choices * sum(negative_digits)
    )
    assert observed_sum == target_sum

    slope_numerator = positive_states[0]
    assert (period * slope_numerator) % d == 0
    z = period * slope_numerator // d
    phase_numerator = z
    for block in range(repeats):
        for offset, digit in enumerate(positive_digits):
            position = block * length + offset
            phase_numerator += (
                digit * (position + 2) * (1 << (period - 1 - position))
            )

    modulus = (1 << period) - 1
    assert modulus % d == 0
    obstruction = modulus // d
    binary_value = sum(
        digit * (1 << (length - 1 - offset))
        for offset, digit in enumerate(positive_digits)
    )
    weighted_value = sum(
        digit * (1 << (length - 1 - offset)) * (offset + 2)
        for offset, digit in enumerate(positive_digits)
    )
    closed_ratio = Fraction(
        d * (weighted_value * (base - 1) + length * binary_value),
        (base - 1) ** 2,
    )
    assert Fraction(phase_numerator, obstruction) == closed_ratio

    for block in range(repeats):
        before = phase_numerator
        delta = 0
        for offset, (negative, positive) in enumerate(
            zip(negative_digits, positive_digits)
        ):
            position = block * length + offset
            delta += (
                (negative - positive)
                * (position + 2)
                * (1 << (period - 1 - position))
            )
        expected = -2 * base ** (repeats - 1 - block)
        assert delta == expected
        assert before + delta == phase_numerator + expected

    # Use the looser range of every possible subset, not merely subsets with
    # the required size. This makes the candidate-multiple list independent
    # of scale and licenses the all-scale repetition certificate.
    minimum = 0
    maximum = geometric_sum(base, repeats)
    low_multiple = ceil_div(phase_numerator - 2 * maximum, obstruction)
    high_multiple = (phase_numerator - 2 * minimum) // obstruction
    candidates = 0
    passes = 0
    for multiple in range(low_multiple, high_multiple + 1):
        difference = phase_numerator - multiple * obstruction
        if difference < 0 or difference % 2:
            continue
        candidates += 1
        subset = difference // 2
        if is_subset_sum(subset, base, repeats, choices):
            passes += 1
    return Check(
        boundary,
        scale,
        closed_ratio,
        candidates,
        passes,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-denominator", type=int, default=101)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    checked = 0
    passes = 0
    no_boundary = 0
    digest = sha256()
    for denominator in range(3, args.max_denominator + 1, 2):
        items = boundaries(denominator)
        no_boundary += not items
        digest.update(repr(("denominator", denominator, len(items))).encode())
        for boundary in items:
            result = check_family(boundary, 1)
            checked += 1
            passes += result.passing_subsets
            digest.update(
                repr(
                    (
                        boundary,
                        result.baseline_ratio,
                        result.candidate_multiples,
                        result.passing_subsets,
                    )
                ).encode()
            )
            print(
                f"d={denominator:3} y={boundary.residue:3} "
                f"candidates={result.candidate_multiples:2} "
                f"passes={result.passing_subsets} "
                f"baseline={result.baseline_ratio}"
            )
    certificate = digest.hexdigest()
    if args.max_denominator == 501:
        assert certificate == (
            "1508d04cc91c8a007d17028efb24fe72"
            "6785f4f210272721d8fc7f6149d4bb06"
        )
    print(f"families checked: {checked}")
    print(f"denominators with no boundary family: {no_boundary}")
    print(f"phase-integral subset patterns: {passes}")
    print(f"certificate sha256: {certificate}")
    if passes:
        raise SystemExit("a phase-integral boundary pattern survived")


if __name__ == "__main__":
    main()
