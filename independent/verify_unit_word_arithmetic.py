#!/usr/bin/env python3
"""Independent bounded checks for Lemma 125 and Proposition 126.

The sparse coefficients and raw safe-map steps are implemented directly.
The finite loops are regression checks; the infinite-family claim rests on
the symbolic formulas in the proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class State:
    n: int
    q: int
    e: int


@dataclass(frozen=True)
class Block:
    start: State
    wraps: int
    returned: State | None


def step(state: State) -> tuple[str, State] | None:
    doubled = 2 * state.e
    if doubled > state.n + 2:
        return "wrap", State(
            state.n + 1,
            state.q + 1,
            doubled - state.n - 2,
        )
    if state.q + doubled < state.n + 1:
        return "zero", State(state.n + 1, state.q, doubled)
    return None


def blocks(start: State, limit: int) -> list[Block]:
    current = start
    answer: list[Block] = []
    for _ in range(limit):
        first = step(current)
        if first is None:
            break
        if first[0] != "zero":
            current = first[1]
            continue
        cursor = first[1]
        wraps = 0
        while True:
            outcome = step(cursor)
            if outcome is None:
                answer.append(Block(current, wraps, None))
                return answer
            if outcome[0] == "zero":
                answer.append(Block(current, wraps, cursor))
                current = cursor
                break
            wraps += 1
            cursor = outcome[1]
    return answer


def sparse_coefficients(gaps: tuple[int, ...]) -> tuple[int, int, int]:
    span = sum(gap + 2 for gap in gaps)
    prefix = 0
    exponents = []
    for gap in gaps:
        prefix += gap + 2
        exponents.append(span - prefix)
    binary = sum(1 << exponent for exponent in exponents)
    weighted = sum(exponent << exponent for exponent in exponents)
    return span, binary, weighted


def recurrence_coefficients(
    gaps: tuple[int, ...],
) -> tuple[int, int, int]:
    span = 0
    b_coeff = 0
    c_coeff = 0
    for gap in gaps:
        scale = 1 << (gap + 2)
        b_coeff = scale * b_coeff + 1
        c_coeff = scale * c_coeff + span + gap + 5
        span += gap + 2
    return span, b_coeff, c_coeff


def evolve(
    start_n: int,
    start_f: int,
    gaps: tuple[int, ...],
) -> tuple[int, int]:
    n = start_n
    f = start_f
    for gap in gaps:
        f = (1 << (gap + 2)) * f - n - gap - 5
        n += gap + 2
    return n, f


def unit_state(n: int, quotient: int, returned: int) -> bool:
    d_coord = n - 2 * quotient
    return (
        (n + 3 + returned) % 4 == 0
        and returned >= 1
        and returned <= d_coord - 3
        and 4 * returned <= n + d_coord + 2
    )


def pure_gate(
    n: int,
    quotient: int,
    returned: int,
    gap: int,
    next_returned: int,
) -> bool:
    d_coord = n - 2 * quotient
    defect_numerator = d_coord - 3 - returned
    scale = 1 << (gap + 4)
    return (
        defect_numerator % 2 == 0
        and defect_numerator // 2 >= 2
        and 1 <= next_returned <= scale
        and d_coord + gap - 3 - next_returned >= scale
    )


def check_sparse_words() -> int:
    checked = 0
    for length in range(1, 7):
        for gaps in product(range(4), repeat=length):
            span, binary, weighted = sparse_coefficients(gaps)
            old_span, old_binary, old_constant = recurrence_coefficients(gaps)
            assert span == old_span
            assert binary == old_binary
            assert old_constant == (span + 3) * binary - weighted

            prefix = 0
            exponents = []
            for gap in gaps:
                prefix += gap + 2
                exponents.append(span - prefix)
            assert exponents[-1] == 0
            assert span - exponents[0] == gaps[0] + 2
            assert all(
                left - right == gap + 2
                for left, right, gap in zip(
                    exponents, exponents[1:], gaps[1:]
                )
            )

            for start_n in range(2, 10):
                for start_f in range(1, 6):
                    end_n, end_f = evolve(start_n, start_f, gaps)
                    assert binary * (end_n + 3) == (
                        (1 << span) * start_f + weighted - end_f
                    )
                    checked += 1
    return checked


def family_data(
    a: int,
    q_parameter: int,
) -> tuple[list[int], list[int], list[int], list[int]]:
    span = 8 * q_parameter
    total_power = 1 << span
    numerator = a * (total_power - 1) + 24
    assert numerator % 9 == 0
    n0 = numerator // 9 - span - 3
    assert (n0 + 3 + a) % 8 == 0
    b = (n0 + 3 + a) // 8
    c_numerator = a * (1 << (span - 3)) + a + 3
    assert c_numerator % 9 == 0
    c = c_numerator // 9
    indices = [n0 - 3, n0, n0 + span - 3, n0 + span]
    quotients = [0, 1, 2, 3]
    returned = [b, a, c, a]
    gaps = [1, span - 5, 1]
    return indices, quotients, returned, gaps


def check_family() -> tuple[int, int]:
    algebraic = 0
    raw = 0
    for a in range(7, 33):
        if a % 3 == 0:
            continue
        for q_parameter in range(1, 121):
            if q_parameter % 12 != (4 * a) % 12:
                continue
            indices, quotients, returned, gaps = family_data(a, q_parameter)
            assert all(
                unit_state(n, quotient, residue)
                for n, quotient, residue in zip(
                    indices, quotients, returned
                )
            )
            assert all(
                pure_gate(
                    indices[index],
                    quotients[index],
                    returned[index],
                    gaps[index],
                    returned[index + 1],
                )
                for index in range(3)
            )
            for index, gap in enumerate(gaps):
                end_n, end_f = evolve(
                    indices[index],
                    returned[index],
                    (gap,),
                )
                assert end_n == indices[index + 1]
                assert end_f == returned[index + 1]
            algebraic += 1

            first_e = (indices[0] + 3 + returned[0]) // 4
            raw_blocks = blocks(
                State(indices[0], 0, first_e),
                limit=8 * q_parameter + 8,
            )
            positive = [
                (position, block)
                for position, block in enumerate(raw_blocks)
                if block.wraps > 0 and block.returned is not None
            ]
            assert len(positive) >= 4
            for index in range(4):
                _, block = positive[index]
                assert block.wraps == 1
                assert block.start.n == indices[index]
                assert block.start.q == quotients[index]
                assert block.returned is not None
                assert block.returned.e == returned[index]
            assert [
                positive[index + 1][0] - positive[index][0] - 1
                for index in range(3)
            ] == gaps
            raw += 1
    return algebraic, raw


def main() -> None:
    sparse = check_sparse_words()
    algebraic, raw = check_family()
    assert sparse == 218_400
    assert algebraic == 180
    assert raw == 180
    print(f"sparse-binary endpoint identities checked: {sparse}")
    print(f"algebraic family instances checked: {algebraic}")
    print(f"literal raw safe-map family instances checked: {raw}")
    print(
        "VERDICT: bounded independent checks agree with Lemma 125 and "
        "Proposition 126; infinitude remains a symbolic consequence."
    )


if __name__ == "__main__":
    main()
