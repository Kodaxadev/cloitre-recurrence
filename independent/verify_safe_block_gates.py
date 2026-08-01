#!/usr/bin/env python3
"""Independent bounded checks of Lemma 83 and Corollary 84.

The verifier uses raw `(n,q,e)` thresholds and imports no project code.
It is a finite regression check, not the symbolic proof.
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
        return (
            "wrap",
            State(state.n + 1, state.q + 1, doubled - state.n - 2),
        )
    if state.q + doubled < state.n + 1:
        return ("zero", State(state.n + 1, state.q, doubled))
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


def check_candidate_realizes(
    m: int,
    q: int,
    k: int,
    r: int,
    residue: int,
) -> None:
    parent_n = m - k - 1
    parent_q = q - k
    parent_a = (m + 3 - residue) // (1 << k)
    parent_e = (parent_n + 4 - parent_a) // 2
    accelerated = accelerate_zero(State(parent_n, parent_q, parent_e))
    assert accelerated == (k, State(m, q, residue))

    current = State(m, q, residue)
    for _ in range(r):
        accelerated = accelerate_zero(current)
        assert accelerated is not None
        assert accelerated[0] == 0
        assert accelerated[1] is not None
        current = accelerated[1]
    accelerated = accelerate_zero(current)
    assert accelerated is not None and accelerated[0] > 0


def check_gate(blocks: list[Block], index: int) -> tuple[bool, int]:
    block = blocks[index]
    if block.wraps == 0 or block.next_zero is None:
        return False, 0

    next_positive = index + 1
    while (
        next_positive < len(blocks)
        and blocks[next_positive].wraps == 0
        and blocks[next_positive].next_zero is not None
    ):
        next_positive += 1
    if (
        next_positive == len(blocks)
        or blocks[next_positive].wraps == 0
    ):
        return False, 0

    r = next_positive - index - 1
    m, q, residue = (
        block.next_zero.n,
        block.next_zero.q,
        block.next_zero.e,
    )
    old_overshoot = block.start.n + 4 - 2 * block.start.e
    assert m + 3 - residue == (1 << block.wraps) * old_overshoot

    gate = candidates(m, q, block.wraps, r)
    assert residue in gate
    for candidate in gate:
        check_candidate_realizes(m, q, block.wraps, r, candidate)
    gap = m - 2 * q
    numerator = gap + r - 3
    denominator = 1 << (block.wraps + r + 3)
    bound = (numerator + denominator - 1) // denominator
    assert len(gate) <= bound
    if len(gate) >= 2:
        assert denominator < numerator
    if block.wraps == 1:
        start = block.start
        gap = start.n - 2 * start.q
        excess = 4 * start.e - start.n - 3
        next_excess = (
            (1 << (r + 2)) * excess - start.n - r - 5
        )
        spacing = 1 << (r + 4)
        reduced = [
            value
            for value in range(1, gap - 2)
            if value % 4 == (1 - start.n) % 4
            and (1 << (r + 2)) * value > start.n + r + 5
            and (1 << (r + 2)) * value
            <= start.n + gap + 2 * r + 2
        ]
        assert reduced == gate
        boundary_unique = next_excess <= spacing and (
            next_excess + spacing > gap + r - 3
            or excess > gap - 7
        )
        assert boundary_unique == (len(gate) == 1)
    return True, len(gate)


def unique_chain(start: State) -> list[tuple[int, int, int]]:
    blocks = zero_blocks(start)
    positive = [
        index
        for index, block in enumerate(blocks)
        if block.wraps > 0 and block.next_zero is not None
    ]
    observed = []
    for left, right in zip(positive, positive[1:]):
        block = blocks[left]
        assert block.next_zero is not None
        r = right - left - 1
        gate = candidates(
            block.next_zero.n,
            block.next_zero.q,
            block.wraps,
            r,
        )
        observed.append((block.wraps, r, len(gate)))
    return observed


def check_unique_chains() -> None:
    observed = unique_chain(State(61, 0, 49))
    target = [
        (2, 1, 1),
        (1, 2, 1),
        (2, 3, 1),
        (1, 2, 1),
        (1, 4, 1),
    ]
    assert any(
        observed[index : index + len(target)] == target
        for index in range(len(observed) - len(target) + 1)
    )

    observed = unique_chain(State(36, 9, 13))
    assert observed == [
        (1, 0, 1),
        (1, 0, 1),
        (1, 4, 1),
        (1, 0, 1),
        (1, 1, 1),
        (1, 0, 1),
        (1, 0, 1),
    ]


def check_arbitrary_unit_gates() -> int:
    checked = 0
    for n in range(6, 101):
        for q in range(n - 1):
            width = n - q
            for e in range(1, width):
                if 2 * e > width or 4 * e <= n + 3:
                    continue
                blocks = zero_blocks(State(n, q, e), limit=500)
                if not blocks or blocks[0].wraps != 1:
                    continue
                realized, _ = check_gate(blocks, 0)
                if realized:
                    checked += 1
    return checked


def check_parent_boundary_compatibility() -> None:
    solutions = []
    for r in range(65):
        scale = 1 << (r + 2)
        for next_r in range(65):
            next_scale = 1 << (next_r + 2)
            for delta in (3, 5):
                next_delta = delta if r % 2 else 8 - delta
                final_delta = (
                    next_delta if next_r % 2 else 8 - next_delta
                )
                numerator = (
                    next_scale * r
                    + scale * delta
                    - (next_scale + 1) * next_delta
                    - 2 * next_r
                    - 2
                    + final_delta
                )
                denominator = scale - next_scale
                if denominator == 0 or numerator % denominator:
                    continue
                gap = numerator // denominator
                n = (
                    (scale - 1) * gap
                    - scale * delta
                    - 2 * r
                    - 5
                    + next_delta
                )
                if gap < delta + 1 or n < gap or (n - gap) % 2:
                    continue
                solutions.append(
                    (
                        r,
                        next_r,
                        delta,
                        next_delta,
                        final_delta,
                        gap,
                        n,
                    )
                )

    assert solutions == [(0, 1, 3, 5, 5, 8, 12)]
    assert accelerate_zero(State(12, 2, 5)) == (
        1,
        State(14, 3, 5),
    )
    assert accelerate_zero(State(14, 3, 5)) == (
        1,
        State(16, 4, 3),
    )
    assert accelerate_zero(State(16, 4, 3)) == (
        0,
        State(17, 4, 6),
    )
    assert accelerate_zero(State(17, 4, 6)) == (
        1,
        State(19, 5, 4),
    )
    assert accelerate_zero(State(19, 5, 4)) == (0, None)


def check_same_epoch_exclusion() -> None:
    for exponent in range(50, 65):
        for offset in range(6):
            for next_offset in range(6):
                for excess in range(1, 48):
                    for next_excess in range(1, 48):
                        coefficient = (
                            (1 << (5 - offset)) * excess
                            - (1 << (5 - next_offset)) * next_excess
                        )
                        final_excess = (
                            -exponent
                            + next_offset
                            + next_excess
                            - 2
                            - (1 << (exponent - 3)) * coefficient
                        )
                        assert not 1 <= final_excess < 48

    for exponent in range(50, 1_000):
        assert (
            (1 << (exponent + 1)) + 2 * exponent + 5
            < 1 << (exponent + 2)
        )


def main() -> None:
    gates = 0
    unique = 0
    multiple = 0
    for n in range(2, 121):
        for e in range(1, n):
            blocks = zero_blocks(State(n, 0, e))
            for index in range(len(blocks)):
                checked, count = check_gate(blocks, index)
                if not checked:
                    continue
                gates += 1
                if count == 1:
                    unique += 1
                else:
                    multiple += 1

    assert gates == 29_630
    assert unique == 9_718
    assert multiple == 19_912
    arbitrary_unit = check_arbitrary_unit_gates()
    assert arbitrary_unit == 9_682
    check_parent_boundary_compatibility()
    check_same_epoch_exclusion()
    check_unique_chains()
    print(f"adjacent positive-block gates checked: {gates}")
    print(f"unique gates: {unique}")
    print(f"multiple-candidate gates: {multiple}")
    print(f"arbitrary unit-wrap gates checked: {arbitrary_unit}")
    print("parent-boundary compatibility checked through r,r'<=64")
    print("same-epoch obstruction checked for 50<=L<65")
    print("consecutive unique-gate chain reproduced: 7")
    print(
        "VERDICT: bounded raw checks agree with Lemmas 83/85/87 "
        "and Corollaries 84/86/88."
    )


if __name__ == "__main__":
    main()
