#!/usr/bin/env python3
"""Bounded raw checks of Lemmas 92/94 and Corollaries 93/95.

This verifier imports no project implementation. It compares the exact
boundary test with literal gate enumeration and performs a bounded parameter
search for consecutive unique parent-boundary starts. The search is evidence,
not a proof outside its displayed bounds.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    n: int
    q: int
    e: int


@dataclass(frozen=True)
class Block:
    start: State
    wraps: int
    next_zero: State | None


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


def accelerate_zero(state: State) -> tuple[int, State | None] | None:
    outcome = step(state)
    if outcome is None or outcome[0] != "zero":
        return None
    current = outcome[1]
    wraps = 0
    while True:
        outcome = step(current)
        if outcome is None:
            return wraps, None
        if outcome[0] == "zero":
            return wraps, current
        wraps += 1
        current = outcome[1]


def zero_blocks(start: State, limit: int = 2_000) -> list[Block]:
    current = start
    blocks = []
    for _ in range(limit):
        accelerated = accelerate_zero(current)
        if accelerated is None:
            outcome = step(current)
            if outcome is None:
                break
            current = outcome[1]
            continue
        wraps, next_zero = accelerated
        blocks.append(Block(current, wraps, next_zero))
        if next_zero is None:
            break
        current = next_zero
    return blocks


def candidates(m: int, q: int, k: int, r: int) -> list[int]:
    width = m - q
    parent_n = m - k - 1
    parent_q = q - k
    modulus = 1 << (k + 1)
    target = (m + 3 - (1 << k) * parent_n) % modulus
    return [
        value
        for value in range(1, width)
        if value % modulus == target
        and (1 << (r + 2)) * value > m + r + 3
        and (1 << (r + 1)) * value <= width + r
        and parent_q + 4
        <= (m + 3 - value) // (1 << k)
        <= parent_n + 2
    ]


def check_raw_gates() -> tuple[int, int]:
    checked = 0
    nonunique = 0
    for n in range(2, 121):
        for e in range(1, n):
            blocks = zero_blocks(State(n, 0, e))
            positive = [
                index
                for index, block in enumerate(blocks)
                if block.wraps > 0 and block.next_zero is not None
            ]
            for left, right in zip(positive, positive[1:]):
                block = blocks[left]
                returned = block.next_zero
                assert returned is not None
                r = right - left - 1
                k = block.wraps
                gate = candidates(returned.n, returned.q, k, r)

                parent_a = block.start.n + 4 - 2 * block.start.e
                parent_d = parent_a - block.start.q - 4
                gap = returned.n - 2 * returned.q
                excess = (
                    (1 << (r + 2)) * returned.e
                    - returned.n
                    - r
                    - 3
                )
                spacing = 1 << (k + r + 3)
                next_start = blocks[right].start
                child_d = (
                    next_start.n
                    - next_start.q
                    - 2 * next_start.e
                )

                assert 1 <= excess <= gap + r - 3
                assert gap + r - 3 - excess == 2 * child_d
                predicted_unique = excess <= spacing and (
                    parent_d <= 1 or 2 * child_d < spacing
                )
                assert predicted_unique == (len(gate) == 1)
                predicted_multiple = excess > spacing or (
                    parent_d >= 2 and 2 * child_d >= spacing
                )
                assert predicted_multiple == (len(gate) >= 2)
                checked += 1
                nonunique += len(gate) >= 2
    return checked, nonunique


def solve_boundary_pair(
    k: int,
    r: int,
    next_k: int,
    next_r: int,
    d: int,
    next_d: int,
    final_d: int,
) -> tuple[int, int] | None:
    a = 1 << (r + 1)
    b = a << k
    c = a * (k + 4) - b * (d + 4) - r - 1 + next_d
    aa = 1 << (next_r + 1)
    bb = aa << next_k
    cc = (
        (aa - 1) * (k + r + 1)
        + aa * (next_k + 4)
        - bb * (next_d + 4)
        - next_r
        - 1
        + final_d
        - (bb - 1) * k
    )
    determinant = (bb - 1) * (a - 1) - (b - 1) * (aa - 1)
    if determinant == 0:
        return None
    q_numerator = cc * (a - 1) - c * (aa - 1)
    n_numerator = (b - 1) * cc - (bb - 1) * c
    if q_numerator % determinant or n_numerator % determinant:
        return None
    return n_numerator // determinant, q_numerator // determinant


def singular_boundary_system(
    k: int,
    r: int,
    next_k: int,
    next_r: int,
    d: int,
    next_d: int,
    final_d: int,
) -> bool:
    a = 1 << (r + 1)
    b = a << k
    c = a * (k + 4) - b * (d + 4) - r - 1 + next_d
    aa = 1 << (next_r + 1)
    bb = aa << next_k
    cc = (
        (aa - 1) * (k + r + 1)
        + aa * (next_k + 4)
        - bb * (next_d + 4)
        - next_r
        - 1
        + final_d
        - (bb - 1) * k
    )
    determinant = (bb - 1) * (a - 1) - (b - 1) * (aa - 1)
    return determinant == 0 and c == cc


def local_unique_transition(
    n: int,
    q: int,
    k: int,
    r: int,
    defect: int,
) -> tuple[int, int, int] | None:
    if n < 2 or not 0 <= q < n or (n - q - defect) % 2:
        return None
    e = (n - q - defect) // 2
    if not 0 < e < n - q:
        return None
    overshoot = q + defect + 4
    if not (
        (1 << k) * overshoot < n + k + 4
        and (1 << (k + 1)) * overshoot >= n + k + 5
    ):
        return None
    m = n + k + 1
    next_q = q + k
    residue = m + 3 - (1 << k) * overshoot
    returned_a = (1 << (k + 1)) * overshoot - (m + 2)
    if residue <= 0 or returned_a < next_q + 4:
        return None
    excess = (1 << (r + 2)) * residue - m - r - 3
    gap = m - 2 * next_q
    upper = gap + r - 3
    if not 1 <= excess <= upper:
        return None
    spacing = 1 << (k + r + 3)
    if not (
        excess <= spacing
        and (defect <= 1 or excess + spacing > upper)
    ):
        return None
    next_n = m + r
    child_defect = upper - excess
    assert child_defect % 2 == 0
    return next_n, next_q, child_defect // 2


def check_boundary_triples(bound: int = 16) -> list[tuple[int, ...]]:
    hits = []
    singular = []
    for k in range(1, bound + 1):
        for r in range(bound + 1):
            for next_k in range(1, bound + 1):
                for next_r in range(bound + 1):
                    for defect in range(2):
                        for next_defect in range(2):
                            for final_defect in range(2):
                                parameters = (
                                    k,
                                    r,
                                    next_k,
                                    next_r,
                                    defect,
                                    next_defect,
                                    final_defect,
                                )
                                if singular_boundary_system(*parameters):
                                    singular.append(parameters)
                                    continue
                                solved = solve_boundary_pair(*parameters)
                                if solved is None:
                                    continue
                                first = local_unique_transition(
                                    *solved,
                                    k,
                                    r,
                                    defect,
                                )
                                if first is None or first[2] != next_defect:
                                    continue
                                second = local_unique_transition(
                                    first[0],
                                    first[1],
                                    next_k,
                                    next_r,
                                    next_defect,
                                )
                                if second is None or second[2] != final_defect:
                                    continue
                                final_n, final_q, _ = second
                                if (
                                    2 * (final_q + final_defect + 4)
                                    >= final_n + 5
                                ):
                                    continue
                                hits.append((*solved, *parameters))
    assert singular == [(1, 0, 1, 0, 0, 0, 1)]
    # Its dependent equation is 3q-n=-7. With d=0 this gives
    # n-q-d=2q+7, so no integral starting residue exists.
    return hits


def main() -> None:
    checked, nonunique = check_raw_gates()
    triples = check_boundary_triples()
    assert triples == [
        (12, 2, 1, 0, 1, 1, 0, 1, 1),
        (41, 3, 2, 0, 2, 1, 0, 1, 1),
        (39, 4, 2, 1, 2, 2, 1, 1, 0),
    ]
    print(f"raw arbitrary-block gates checked: {checked}")
    print(f"nonunique gates classified exactly: {nonunique}")
    print("unique parent-boundary triples checked for parameters <=16")
    print(f"bounded triple patterns: {len(triples)}")
    print(
        "VERDICT: bounded raw gates agree with Lemmas 92/94 "
        "and Corollaries 93/95."
    )


if __name__ == "__main__":
    main()
