"""Search eventually periodic quotient-change patterns.

For a period-p digit word a_j in {-1,0,1}, the exact law

    e_{n+1} = 2 e_n - a_n (n+2)

has a unique O(n) solution on each phase. This script checks:

1. nonnegative quotient slope mu = sum(a)/p in [0,1];
2. the asymptotic state and digit inequalities on every phase;
3. the necessary integrality condition p*A in Z for the phase-0 e-slope.

Passing a finite-period search is only computational evidence. Failure of every
word up to a bound is not a proof that all eventual periods are impossible.
"""

from __future__ import annotations

import argparse
import itertools
import math
from fractions import Fraction


def phase_solution(
    word: tuple[int, ...],
) -> tuple[list[Fraction], list[Fraction]]:
    """Return e_j = slopes[j] * n + intercepts[j] for base phase index n."""
    p = len(word)
    powers = [1 << (p - 1 - j) for j in range(p)]
    weighted = sum(a * power for a, power in zip(word, powers))
    weighted_offset = sum(
        a * power * (j + 2) for j, (a, power) in enumerate(zip(word, powers))
    )
    slope = Fraction(weighted, (1 << p) - 1)
    intercept = Fraction(p * slope + weighted_offset, (1 << p) - 1)

    slopes: list[Fraction] = []
    intercepts: list[Fraction] = []
    current_slope = slope
    current_intercept = intercept
    for j, digit in enumerate(word):
        slopes.append(current_slope)
        intercepts.append(current_intercept)
        current_slope = 2 * current_slope - digit
        current_intercept = 2 * current_intercept - digit * (j + 2)

    if current_slope != slope or current_intercept != intercept + p * slope:
        raise AssertionError("periodic affine solution failed to close")
    return slopes, intercepts


def classify(word: tuple[int, ...]) -> tuple[bool, str, list[Fraction]]:
    p = len(word)
    total = sum(word)
    if not 0 <= total <= p:
        return False, "quotient slope", []

    mu = Fraction(total, p)
    powers = [1 << (p - 1 - j) for j in range(p)]
    weighted = sum(a * power for a, power in zip(word, powers))
    weighted_offset = sum(
        a * power * (j + 2) for j, (a, power) in enumerate(zip(word, powers))
    )
    modulus = (1 << p) - 1
    slopes, _ = phase_solution(word)
    slope = slopes[0]

    if (p * weighted) % modulus != 0:
        return False, "integrality", []
    cycle_delta = p * weighted // modulus
    if (cycle_delta + weighted_offset) % math.gcd(weighted, modulus) != 0:
        return False, "phase integrality", []

    for digit, current in zip(word, slopes):
        remainder_slope = mu + current
        if not 0 <= remainder_slope <= 1:
            return False, "state window", slopes

        decision_slope = mu + 2 * current
        if digit == -1 and not decision_slope <= 0:
            return False, "digit -1", slopes
        if digit == 0 and not 0 <= decision_slope <= 1:
            return False, "digit 0", slopes
        if digit == 1 and not 1 <= decision_slope <= 2:
            return False, "digit +1", slopes

    return True, "candidate", slopes


def passes_phase_integrality(word: tuple[int, ...]) -> bool:
    """Fast Theorem 25 check for a word already produced by the focused generator."""
    p = len(word)
    powers = [1 << (p - 1 - j) for j in range(p)]
    weighted = sum(a * power for a, power in zip(word, powers))
    weighted_offset = sum(
        a * power * (j + 2) for j, (a, power) in enumerate(zip(word, powers))
    )
    modulus = (1 << p) - 1
    if (p * weighted) % modulus != 0:
        return False
    cycle_delta = p * weighted // modulus
    return (cycle_delta + weighted_offset) % math.gcd(weighted, modulus) == 0


def step_state(n: int, q: int, r: int) -> tuple[int, int, int, int]:
    d = 2 * r - q
    if d < 0:
        digit = -1
        return n + 1, q - 1, d + n + 1, digit
    if d >= n + 1:
        digit = 1
        return n + 1, q + 1, d - n - 1, digit
    return n + 1, q, d, 0


def exact_examples(
    word: tuple[int, ...], max_n: int = 500
) -> list[tuple[int, int, int]]:
    """Find exact states that follow the word for 100 periods."""
    slopes, intercepts = phase_solution(word)
    mu = Fraction(sum(word), len(word))
    examples: list[tuple[int, int, int]] = []

    for n in range(2, max_n + 1):
        e_value = slopes[0] * n + intercepts[0]
        if e_value.denominator != 1:
            continue
        e = int(e_value)
        center = mu * n
        if center.denominator != 1:
            q_candidates = range(max(0, int(center) - 20), min(n, int(center) + 20) + 1)
        else:
            q_candidates = range(max(0, int(center) - 20), min(n, int(center) + 20) + 1)
        for q in q_candidates:
            r = q + e
            if not 0 <= r < n or q == r:
                continue
            state = (n, q, r)
            digits: list[int] = []
            valid = True
            for j in range(100 * len(word)):
                if state[1] == state[2]:
                    valid = False
                    break
                state = step_state(*state)
                digits.append(state[3])
                state = state[:3]
                if digits[-1] != word[j % len(word)]:
                    valid = False
                    break
            if valid:
                examples.append((n, q, r))
                return examples
    return examples


def is_primitive(word: tuple[int, ...]) -> bool:
    p = len(word)
    for d in range(1, p):
        if p % d == 0 and word == word[:d] * (p // d):
            return False
    return True


def signed_binary_words(target: int, length: int):
    """Yield all {-1,0,1} words with the requested weighted binary value."""

    def visit(position: int, residual: int, prefix: list[int]):
        if position == length:
            if residual == 0:
                yield tuple(prefix)
            return
        weight = 1 << (length - 1 - position)
        remaining = weight - 1
        for digit in (-1, 0, 1):
            next_residual = residual - digit * weight
            if abs(next_residual) <= remaining:
                prefix.append(digit)
                yield from visit(position + 1, next_residual, prefix)
                prefix.pop()

    yield from visit(0, target, [])


def integrality_first_words(period: int):
    """Generate every self-consistent asymptotic slope cycle.

    Fix S=sum(a_j), so mu=S/p. Cycle integrality writes A_j=v_j/p with
    integer v_j. The state window is -S <= v_j <= p-S, and the leading digit
    decision depends only on S+2*v_j. Except at 0 and p it is deterministic.
    """

    def visit(
        digit_sum: int,
        start: int,
        position: int,
        current: int,
        running_sum: int,
        prefix: list[int],
    ):
        if not -digit_sum <= current <= period - digit_sum:
            return
        if position == period:
            if current == start and running_sum == digit_sum:
                yield tuple(prefix)
            return

        decision = digit_sum + 2 * current
        if decision < 0:
            digits = (-1,)
        elif decision == 0:
            digits = (-1, 0)
        elif decision < period:
            digits = (0,)
        elif decision == period:
            digits = (0, 1)
        else:
            digits = (1,)

        remaining = period - position - 1
        for digit in digits:
            next_sum = running_sum + digit
            if not next_sum - remaining <= digit_sum <= next_sum + remaining:
                continue
            prefix.append(digit)
            yield from visit(
                digit_sum,
                start,
                position + 1,
                2 * current - digit * period,
                next_sum,
                prefix,
            )
            prefix.pop()

    # The state-window average gives 0 <= mu <= 1/2.
    for digit_sum in range(0, period // 2 + 1):
        for start in range(-digit_sum, period - digit_sum + 1):
            yield from visit(digit_sum, start, 0, start, 0, [])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-period", type=int, default=1)
    parser.add_argument("--max-period", type=int, default=12)
    parser.add_argument("--show", type=int, default=20)
    parser.add_argument(
        "--focused",
        action="store_true",
        help="enumerate only words satisfying the necessary cycle integrality condition",
    )
    parser.add_argument(
        "--primitive-only",
        action="store_true",
        help="discard words that repeat a shorter digit period",
    )
    args = parser.parse_args()

    totals: dict[str, int] = {}
    rejected_examples: dict[str, list[tuple[int, ...]]] = {}
    candidates: list[tuple[tuple[int, ...], list[Fraction]]] = []

    for p in range(args.min_period, args.max_period + 1):
        period_candidates = 0
        period_rejected: list[tuple[tuple[int, ...], str]] = []
        words = integrality_first_words(p) if args.focused else itertools.product((-1, 0, 1), repeat=p)
        checked = 0
        for word in words:
            if all(a == 0 for a in word):
                continue
            if args.primitive_only and not is_primitive(word):
                continue
            checked += 1
            if args.focused and not passes_phase_integrality(word):
                ok, reason, slopes = False, "phase integrality", []
            else:
                ok, reason, slopes = classify(word)
            totals[reason] = totals.get(reason, 0) + 1
            if not ok and len(rejected_examples.setdefault(reason, [])) < 3:
                rejected_examples[reason].append(word)
            if not ok and len(period_rejected) < args.show:
                period_rejected.append((word, reason))
            if ok:
                candidates.append((word, slopes))
                period_candidates += 1
        print(f"period={p:2d} checked={checked:8d} candidates={period_candidates}")
        if args.focused:
            for word, reason in period_rejected:
                powers = [1 << (p - 1 - j) for j in range(p)]
                c_value = sum(a * power for a, power in zip(word, powers))
                d_value = sum(
                    a * power * (j + 2)
                    for j, (a, power) in enumerate(zip(word, powers))
                )
                modulus = (1 << p) - 1
                z_value = p * c_value // modulus
                divisor = math.gcd(c_value, modulus)
                print(
                    f"  {reason}: word={word} z={z_value}"
                    f" D={d_value} gcd={divisor}"
                    f" residue={(z_value + d_value) % divisor}"
                )

    print("rejection counts:")
    for reason, count in sorted(totals.items()):
        print(f"  {reason:16s} {count}")
        if args.focused:
            for word in rejected_examples.get(reason, []):
                print(f"    example {word}")
    print(f"nonzero candidates: {len(candidates)}")
    for word, slopes in candidates[: args.show]:
        examples = exact_examples(word)
        _, intercepts = phase_solution(word)
        print(
            f"  {word} slopes={slopes} intercepts={intercepts}"
            f" exact_example={examples[:1]}"
        )


if __name__ == "__main__":
    main()
