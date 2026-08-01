#!/usr/bin/env python3
"""Synthesize an exact safe-map state for a prescribed pure-upper gate chain."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import z3


@dataclass(frozen=True)
class SymbolicState:
    n: z3.ArithRef
    q: z3.ArithRef
    e: z3.ArithRef


def zero(solver: z3.Solver, state: SymbolicState) -> SymbolicState:
    solver.add(2 * state.e <= state.n - state.q)
    return SymbolicState(state.n + 1, state.q, 2 * state.e)


def wrap(solver: z3.Solver, state: SymbolicState) -> SymbolicState:
    solver.add(2 * state.e > state.n + 2)
    return SymbolicState(
        state.n + 1,
        state.q + 1,
        2 * state.e - state.n - 2,
    )


def block(solver: z3.Solver, state: SymbolicState, length: int) -> SymbolicState:
    state = zero(solver, state)
    for _ in range(length):
        state = wrap(solver, state)
    return state


def pure_gate(
    solver: z3.Solver,
    parent: SymbolicState,
    returned: SymbolicState,
    child: SymbolicState,
    length: int,
    gap: int,
) -> z3.ArithRef:
    defect = parent.n - parent.q - 2 * parent.e
    child_defect = child.n - child.q - 2 * child.e
    spacing = 1 << (length + gap + 3)
    excess = (1 << (gap + 2)) * returned.e - returned.n - gap - 3
    solver.add(
        defect >= 2,
        excess >= 1,
        excess <= spacing,
        2 * child_defect >= spacing,
    )
    return excess


def parse_positive_csv(value: str) -> list[int]:
    result = [int(item) for item in value.split(",") if item]
    if not result or any(item < 0 for item in result):
        raise argparse.ArgumentTypeError("expected comma-separated nonnegative integers")
    return result


def concrete(value: z3.ArithRef, model: z3.ModelRef) -> int:
    return model.eval(value, model_completion=True).as_long()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gaps", required=True, type=parse_positive_csv)
    parser.add_argument("--blocks", type=parse_positive_csv)
    parser.add_argument("--max-n", type=int, default=10**15)
    parser.add_argument("--initial-q", type=int)
    args = parser.parse_args()

    gaps = args.gaps
    blocks = args.blocks or [1] * (len(gaps) + 1)
    if (
        len(blocks) != len(gaps) + 1
        or any(length < 1 for length in blocks[:-1])
        or blocks[-1] < 0
    ):
        parser.error(
            "--blocks needs one more entry than --gaps; parent lengths are "
            "positive and a final 0 requests only a positive-block prefix"
        )

    solver = z3.Solver()
    initial_n, initial_q, initial_e = z3.Ints("initial_n initial_q initial_e")
    solver.add(
        initial_n >= 2,
        initial_n <= args.max_n,
        initial_q >= 0,
        initial_e > 0,
        initial_e < initial_n - initial_q,
    )
    if args.initial_q is not None:
        solver.add(initial_q == args.initial_q)
    state = SymbolicState(initial_n, initial_q, initial_e)
    gates: list[tuple[SymbolicState, SymbolicState, int, int, z3.ArithRef]] = []

    for index, gap in enumerate(gaps):
        parent = state
        returned = block(solver, parent, blocks[index])
        state = returned
        for _ in range(gap):
            state = zero(solver, state)
        child = state

        excess = pure_gate(
            solver, parent, returned, child, blocks[index], gap
        )
        gates.append((parent, child, blocks[index], gap, excess))

    if blocks[-1] == 0:
        final_return = wrap(solver, zero(solver, state))
    else:
        final_return = block(solver, state, blocks[-1])
        solver.add(2 * final_return.e <= final_return.n - final_return.q)

    result = solver.check()
    print(f"solver result               : {result}")
    if result != z3.sat:
        return
    model = solver.model()
    print(
        "initial state               : "
        f"n={model[initial_n]}, q={model[initial_q]}, e={model[initial_e]}"
    )
    print(f"block lengths               : {blocks}")
    print(f"zero-only gaps              : {gaps}")
    for index, (parent, child, length, gap, excess) in enumerate(gates, 1):
        parent_n = concrete(parent.n, model)
        parent_q = concrete(parent.q, model)
        parent_e = concrete(parent.e, model)
        parent_d = parent_n - parent_q - 2 * parent_e
        child_n = concrete(child.n, model)
        child_q = concrete(child.q, model)
        child_e = concrete(child.e, model)
        child_d = child_n - child_q - 2 * child_e
        spacing = 1 << (length + gap + 3)
        print(
            f"gate {index:>2}                   : "
            f"(n,q,e,d)=({parent_n},{parent_q},{parent_e},{parent_d}), "
            f"k={length}, r={gap}, x={concrete(excess, model)}, "
            f"H={spacing}, d'={child_d}"
        )


if __name__ == "__main__":
    main()
