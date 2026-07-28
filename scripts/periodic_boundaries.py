#!/usr/bin/env python3
"""Enumerate Theorem 32 boundary families using exact integer arithmetic."""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Boundary:
    denominator: int
    cycle: tuple[int, ...]
    residue: int
    numerator: int
    min_repeats: int

    @property
    def length(self) -> int:
        return len(self.cycle)

    @property
    def min_period(self) -> int:
        return self.length * self.min_repeats

    @property
    def negative_choices(self) -> int:
        return self.numerator * self.min_repeats // self.denominator


def unit_cycles(denominator: int) -> list[tuple[int, ...]]:
    unseen = {
        value
        for value in range(1, denominator)
        if math.gcd(value, denominator) == 1
    }
    cycles: list[tuple[int, ...]] = []
    while unseen:
        start = min(unseen)
        cycle: list[int] = []
        value = start
        while value not in cycle:
            cycle.append(value)
            unseen.remove(value)
            value = (2 * value) % denominator
        cycles.append(tuple(cycle))
    return cycles


def lcm(left: int, right: int) -> int:
    return left // math.gcd(left, right) * right


def boundaries(denominator: int) -> list[Boundary]:
    found: list[Boundary] = []
    for cycle in unit_cycles(denominator):
        length = len(cycle)
        residue_sum = sum(cycle)
        for residue in cycle:
            greater = sum(value > residue for value in cycle)
            numerator = (
                residue_sum
                - greater * denominator
                - length * (denominator - residue)
            )
            if not 0 <= numerator <= denominator:
                continue
            period_factor = denominator // math.gcd(denominator, length)
            choice_factor = denominator // math.gcd(denominator, numerator)
            repeats = lcm(period_factor, choice_factor)
            found.append(
                Boundary(
                    denominator,
                    cycle,
                    residue,
                    numerator,
                    repeats,
                )
            )
    return found


def self_test() -> None:
    d3 = boundaries(3)
    assert [(item.residue, item.numerator) for item in d3] == [(2, 1)]
    assert boundaries(5) == []
    d7 = boundaries(7)
    assert [(item.cycle, item.residue, item.numerator) for item in d7] == [
        ((3, 6, 5), 5, 1)
    ]
    for h in range(1, 4):
        repeats = 11 * h
        power = 1024**repeats
        g = (power - 1) // 11
        z = 10 * h
        baseline = sum(
            1024**t * (930 * repeats - 435 - 930 * t)
            for t in range(repeats)
        )
        assert z + baseline == 5455 * g // 1023


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-denominator", type=int, default=101)
    parser.add_argument("--show-excluded", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.max_denominator < 3:
        raise SystemExit("--max-denominator must be at least 3")
    self_test()
    excluded: list[int] = []
    total = 0
    for denominator in range(3, args.max_denominator + 1, 2):
        items = boundaries(denominator)
        if not items:
            excluded.append(denominator)
            continue
        total += len(items)
        for item in items:
            fraction = f"{item.numerator}/{item.denominator}"
            print(
                f"d={item.denominator:3} L={item.length:3} "
                f"y={item.residue:3} K/R={fraction:>7} "
                f"minR={item.min_repeats:4} "
                f"minP={item.min_period:5} K={item.negative_choices:3} "
                f"cycle={item.cycle}"
            )
    print(f"boundary families: {total}")
    print(f"denominators with no boundary family: {len(excluded)}")
    if args.show_excluded:
        print("excluded:", " ".join(map(str, excluded)))


if __name__ == "__main__":
    main()
