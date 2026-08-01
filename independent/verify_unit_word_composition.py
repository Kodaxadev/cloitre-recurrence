#!/usr/bin/env python3
"""Independent checks for Lemmas 127/128 and Proposition 129."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import product


def integer_word_data(
    gaps: tuple[int, ...],
    a: int,
) -> tuple[int, int, int, int]:
    span = sum(gap + 2 for gap in gaps)
    prefix = 0
    binary = 0
    weighted = 0
    for gap in gaps:
        prefix += gap + 2
        exponent = span - prefix
        binary += 1 << exponent
        weighted += exponent << exponent
    x_value = ((1 << span) - 1) * a + weighted
    return span, binary, weighted, x_value


def word_data(
    gaps: tuple[int, ...],
    a: int,
) -> tuple[int, int, int, int, Fraction]:
    span, binary, weighted, x_value = integer_word_data(gaps, a)
    prefix = 0
    h_sum = Fraction()
    k_sum = Fraction()
    for gap in gaps:
        prefix += gap + 2
        h_sum += Fraction(1, 1 << prefix)
        k_sum += Fraction(prefix, 1 << prefix)
    phi = (a * (1 - Fraction(1, 1 << span)) - k_sum) / h_sum
    assert phi == Fraction(x_value, binary) - span
    return span, binary, weighted, x_value, phi


def evolve(
    start_n: int,
    start_f: int,
    gaps: tuple[int, ...],
) -> tuple[int, tuple[int, ...]]:
    n = start_n
    f = start_f
    residues = [f]
    for gap in gaps:
        f = (1 << (gap + 2)) * f - n - gap - 5
        n += gap + 2
        residues.append(f)
    return n, tuple(residues)


def check_normalized_words() -> int:
    checked = 0
    for length in range(1, 7):
        for gaps in product(range(4), repeat=length):
            for a in range(5, 13):
                span, binary, weighted, x_value, phi = word_data(gaps, a)
                assert binary * (phi + span) == x_value
                assert weighted < span * binary
                checked += 1
    return checked


def candidate_word(
    gaps: tuple[int, ...],
    a: int,
    renewal_gap: int,
) -> tuple[int, int] | None:
    span, binary, _, x_value = integer_word_data(gaps, a)
    modulus = 1 << (renewal_gap + 2)
    if gaps[-1] != renewal_gap or span % modulus:
        return None
    if x_value % binary:
        return None
    start = x_value // binary - span - 3
    if start < 2:
        return None
    end, residues = evolve(start, a, gaps)
    if end != start + span or residues[-1] != a:
        return None
    if min(residues) < 1:
        return None
    assert binary * (end + 3) == x_value
    return start, end


def check_bounded_compositions() -> tuple[int, int]:
    candidates = 0
    compatible = 0
    for renewal_gap in range(3):
        maximum_a = min(32, 1 << (renewal_gap + 4))
        for a in range(5, maximum_a + 1):
            starts: dict[int, list[tuple[int, ...]]] = defaultdict(list)
            records = []
            for length in range(2, 6):
                for prefix in product(range(13), repeat=length - 1):
                    gaps = prefix + (renewal_gap,)
                    indices = candidate_word(gaps, a, renewal_gap)
                    if indices is None:
                        continue
                    start, end = indices
                    starts[start].append(gaps)
                    records.append((gaps, start, end))
                    candidates += 1
            for _gaps, _start, end in records:
                compatible += len(starts.get(end, []))
    return candidates, compatible


def unit_state(n: int, quotient: int, returned: int) -> bool:
    d_coord = n - 2 * quotient
    return (
        (n + 3 + returned) % 4 == 0
        and returned >= 1
        and returned <= d_coord - 3
        and 4 * returned <= n + d_coord + 2
    )


def pure_gaps(
    n: int,
    quotient: int,
    returned: int,
) -> list[tuple[int, int]]:
    d_coord = n - 2 * quotient
    answer = []
    for gap in range(n.bit_length() + 3):
        next_returned = (
            (1 << (gap + 2)) * returned - n - gap - 5
        )
        scale = 1 << (gap + 4)
        if (
            (d_coord - 3 - returned) % 2 == 0
            and (d_coord - 3 - returned) // 2 >= 2
            and 1 <= next_returned <= scale
            and d_coord + gap - 3 - next_returned >= scale
        ):
            exponent = gap + 2
            assert (
                (returned + 4) * (1 << (exponent - 1))
                + quotient
                - exponent
                + 1
                <= n
                <= returned * (1 << exponent) - exponent - 4
            )
            answer.append((gap, next_returned))
    return answer


def check_dyadic_windows() -> tuple[int, int, int]:
    states = 0
    gates = 0
    ordered = 0
    for returned in range(5, 65):
        for quotient in range(16):
            for exponent in range(2, 13):
                lower = (
                    (returned + 4) * (1 << (exponent - 1))
                    + quotient
                    - exponent
                    + 1
                )
                upper = returned * (1 << exponent) - exponent - 4
                next_lower = (
                    (returned + 4) * (1 << exponent)
                    + quotient
                    - exponent
                )
                assert lower > returned * (1 << (exponent - 1))
                assert next_lower > upper
                ordered += 1
    for n in range(2, 501):
        for quotient in range(min(16, n)):
            for returned in range(5, min(65, n) + 1):
                if not unit_state(n, quotient, returned):
                    continue
                options = pure_gaps(n, quotient, returned)
                assert len(options) <= 1
                states += 1
                if options:
                    gates += 1
    return states, gates, ordered


def family_data(a: int, q_parameter: int) -> tuple[int, int, int, int]:
    span = 8 * q_parameter
    total_power = 1 << span
    numerator = a * (total_power - 1) + 24
    assert numerator % 9 == 0
    n0 = numerator // 9 - span - 3
    c = (a * (1 << (span - 3)) + a + 3) // 9
    return span, n0, c, span - 5


def check_family_termination() -> int:
    checked = 0
    for a in range(7, 33):
        if a % 3 == 0:
            continue
        for q_parameter in range(1, 121):
            if q_parameter % 12 != (4 * a) % 12:
                continue
            span, n0, c, large_gap = family_data(a, q_parameter)
            endpoint_n = n0 + span
            endpoint_options = pure_gaps(endpoint_n, 3, a)
            assert endpoint_options == [(large_gap, c - span)]

            child_n = n0 + 2 * span - 3
            child_f = c - span
            assert unit_state(child_n, 4, child_f)
            assert pure_gaps(child_n, 4, child_f) == []
            assert 8 * child_f - child_n - 6 == a - 9 * span
            assert n0 - 16 * span + 2 * a - 62 > 0
            checked += 1
    return checked


def main() -> None:
    normalized = check_normalized_words()
    candidates, compatible = check_bounded_compositions()
    states, gates, ordered = check_dyadic_windows()
    family = check_family_termination()
    assert normalized == 43_680
    assert candidates == 35
    assert compatible == 0
    assert family == 180
    print(f"normalized word identities checked: {normalized}")
    print(
        "bounded positive equal-endpoint words / compatible pairs: "
        f"{candidates} / {compatible}"
    )
    print(f"bounded unit states / pure dyadic windows: {states} / {gates}")
    print(f"ordered adjacent dyadic windows checked: {ordered}")
    print(f"maximal family continuations checked: {family}")
    print(
        "VERDICT: bounded independent checks agree with Lemmas 127/128 "
        "and Proposition 129; the empty composition search is not a proof."
    )


if __name__ == "__main__":
    main()
