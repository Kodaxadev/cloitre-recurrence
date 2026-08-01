#!/usr/bin/env python3
"""Search fixed finite block/gap alphabets for a pure-upper gate chain."""

from __future__ import annotations

import argparse

import z3

from synthesize_pure_upper import SymbolicState, block, pure_gate, wrap, zero


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, required=True)
    parser.add_argument("--max-block", type=int, default=8)
    parser.add_argument("--max-gap", type=int, default=8)
    parser.add_argument("--max-n", type=int, default=10**18)
    parser.add_argument("--first-block", type=int)
    parser.add_argument("--node-limit", type=int, default=1_000_000)
    args = parser.parse_args()
    if args.length < 1 or args.max_block < 1 or args.max_gap < 0:
        parser.error("invalid search bounds")

    solver = z3.Solver()
    initial_n, initial_q, initial_e = z3.Ints("initial_n initial_q initial_e")
    solver.add(
        initial_n >= 2,
        initial_n <= args.max_n,
        initial_q >= 0,
        initial_e > 0,
        initial_e < initial_n - initial_q,
    )
    initial = SymbolicState(initial_n, initial_q, initial_e)
    nodes = 0

    def visit(
        state: SymbolicState,
        path: list[tuple[int, int]],
    ) -> tuple[list[tuple[int, int]], z3.ModelRef] | None:
        nonlocal nodes
        if nodes >= args.node_limit:
            return None
        block_lengths = (
            [args.first_block]
            if not path and args.first_block is not None
            else range(1, args.max_block + 1)
        )
        for length in block_lengths:
            if length is None or not 1 <= length <= args.max_block:
                continue
            for gap in range(args.max_gap + 1):
                if nodes >= args.node_limit:
                    return None
                solver.push()
                parent = state
                returned = block(solver, parent, length)
                child = returned
                for _ in range(gap):
                    child = zero(solver, child)
                pure_gate(solver, parent, returned, child, length, gap)
                nodes += 1
                if solver.check() != z3.sat:
                    solver.pop()
                    continue

                next_path = [*path, (length, gap)]
                if len(next_path) == args.length:
                    solver.push()
                    wrap(solver, zero(solver, child))
                    if solver.check() == z3.sat:
                        model = solver.model()
                        solver.pop()
                        solver.pop()
                        return next_path, model
                    solver.pop()
                else:
                    found = visit(child, next_path)
                    if found is not None:
                        solver.pop()
                        return found
                solver.pop()
        return None

    found = visit(initial, [])
    print(f"solver nodes checked         : {nodes}")
    if found is None:
        status = (
            "node limit reached"
            if nodes >= args.node_limit
            else "no bounded-alphabet witness"
        )
        print(f"search result                : {status}")
        return
    path, model = found
    print("search result                : sat")
    print(
        "initial state               : "
        f"n={model.eval(initial_n)}, q={model.eval(initial_q)}, "
        f"e={model.eval(initial_e)}"
    )
    print(f"(block, gap) path           : {path}")


if __name__ == "__main__":
    main()
