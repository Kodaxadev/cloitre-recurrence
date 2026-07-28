#!/usr/bin/env python3
"""Independent finite certificate for the smallest missing increments.

This file deliberately imports no project module. It uses Python's
arbitrary-precision integers and the literal recurrence.
"""

from __future__ import annotations

import argparse
import hashlib


EXPECTED_SHA256 = (
    "66a06cff15735c4a3caf98575f29afbcd"
    "881fbef06334616fbc3bc772b7ab084"
)


def solve_literal(start: int) -> tuple[int, int, int]:
    """Return the first absorbing (index, increment, value)."""
    b = start
    n = 1
    while True:
        if b % (n + 1) == 0:
            c = b // (n + 1)
            if c < n:
                check_b = b
                check_n = n
                for _ in range(64):
                    next_b = check_b + check_b % check_n
                    assert next_b - check_b == c
                    check_b = next_b
                    check_n += 1
                return n, c, b
        b += b % n
        n += 1


def canonical_table() -> tuple[str, list[tuple[int, int, int, int]]]:
    rows = []
    for start in range(1, 260):
        index, increment, value = solve_literal(start)
        rows.append((start, index, increment, value))
    text = "m,t,c,b_t\n" + "".join(
        f"{m},{t},{c},{b_t}\n" for m, t, c, b_t in rows
    )
    return text, rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-table", action="store_true")
    args = parser.parse_args()

    text, rows = canonical_table()
    digest = hashlib.sha256(text.encode("ascii")).hexdigest()
    assert digest == EXPECTED_SHA256

    attained = {row[2] for row in rows}
    missing = [c for c in range(1, 8) if c not in attained]
    assert missing == [5, 7]

    witnesses = {}
    for target in (1, 2, 3, 4, 6):
        witnesses[target] = next(row for row in rows if row[2] == target)

    if args.show_table:
        print(text, end="")
    print(f"starts checked: {len(rows)} (m=1..259)")
    print(f"canonical table sha256: {digest}")
    print(f"missing in 1..7: {missing}")
    for target, row in witnesses.items():
        print(f"witness c={target}: m={row[0]}, t={row[1]}, b_t={row[3]}")
    print("VERDICT: the complete Theorem 18 ranges exclude 5 and 7.")


if __name__ == "__main__":
    main()
