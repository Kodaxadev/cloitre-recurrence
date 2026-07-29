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
    return True, len(gate)


def check_unique_chain() -> None:
    blocks = zero_blocks(State(61, 0, 49))
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

    target = [(2, 1, 1), (1, 2, 1), (2, 3, 1), (1, 2, 1), (1, 4, 1)]
    assert any(
        observed[index : index + len(target)] == target
        for index in range(len(observed) - len(target) + 1)
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
    check_unique_chain()
    print(f"adjacent positive-block gates checked: {gates}")
    print(f"unique gates: {unique}")
    print(f"multiple-candidate gates: {multiple}")
    print("consecutive unique-gate chain reproduced: 5")
    print("VERDICT: bounded raw checks agree with Lemma 83 and Corollary 84.")


if __name__ == "__main__":
    main()
