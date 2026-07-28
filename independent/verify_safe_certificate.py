#!/usr/bin/env python3
"""Independent generator for the finite two-counter safe certificate.

Independence from the Rust generator:
  * Python arbitrary-precision transition arithmetic;
  * raw `(n, q, e)` threshold tests rather than the SafeState helper;
  * two monotone image lists merged linearly, rather than a BTreeMap;
  * an independently implemented covering identity and trajectory digest.
"""

from __future__ import annotations

import argparse


MASK = (1 << 64) - 1
FNV_OFFSET = 0xCBF29CE484222325
FNV_PRIME = 0x00000100000001B3


def fnv_u64(digest: int, value: int) -> int:
    for byte in (value & MASK).to_bytes(8, "little"):
        digest ^= byte
        digest = (digest * FNV_PRIME) & MASK
    return digest


def rotate_left(value: int, shift: int) -> int:
    return ((value << shift) | (value >> (64 - shift))) & MASK


def mix_state(e: int, wraps: int, witness: int) -> int:
    value = e ^ rotate_left(wraps, 21) ^ rotate_left(witness, 42)
    value = (value + 0x9E3779B97F4A7C15) & MASK
    value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & MASK
    value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & MASK
    return value ^ (value >> 31)


def merge_images(
    low: list[tuple[int, int, int]],
    high: list[tuple[int, int, int]],
) -> tuple[list[tuple[int, int, int]], int]:
    """Merge sorted `(e,wraps,witness)` images and retain the dominant copy."""
    merged = []
    duplicates = 0
    i = 0
    j = 0
    while i < len(low) or j < len(high):
        if j == len(high) or (i < len(low) and low[i][0] < high[j][0]):
            merged.append(low[i])
            i += 1
        elif i == len(low) or high[j][0] < low[i][0]:
            merged.append(high[j])
            j += 1
        else:
            left = low[i]
            right = high[j]
            assert left[0] == right[0]
            merged.append(left if left[1:] <= right[1:] else right)
            duplicates += 1
            i += 1
            j += 1
    assert all(merged[k - 1][0] < merged[k][0] for k in range(1, len(merged)))
    return merged, duplicates


def certificate(start_n: int, max_steps: int) -> dict[str, int]:
    live = [(e, 0, e) for e in range(1, start_n)]
    starts = start_n - 1
    n = start_n
    rejected = 0
    captured = 0
    merges = 0
    steps = 0
    trajectory = FNV_OFFSET
    trajectory = fnv_u64(trajectory, start_n)
    trajectory = fnv_u64(trajectory, starts)

    while live and steps < max_steps:
        low = []
        high = []
        modulus = n + 2
        for e, wraps, witness in live:
            doubled = 2 * e
            if doubled == modulus:
                captured += 1
            elif doubled > modulus:
                high.append((doubled - modulus, wraps + 1, witness))
            elif wraps + doubled < n + 1:
                low.append((doubled, wraps, witness))
            else:
                rejected += 1

        live, duplicates = merge_images(low, high)
        merges += duplicates
        assert starts == rejected + captured + merges + len(live)

        state_sum = 0
        state_xor = 0
        e_sum = 0
        wrap_sum = 0
        for e, wraps, witness in live:
            fingerprint = mix_state(e, wraps, witness)
            state_sum = (state_sum + fingerprint) & MASK
            state_xor ^= fingerprint
            e_sum = (e_sum + e) & MASK
            wrap_sum = (wrap_sum + wraps) & MASK
        for value in (
            n,
            rejected,
            captured,
            merges,
            len(live),
            state_sum,
            state_xor,
            e_sum,
            wrap_sum,
        ):
            trajectory = fnv_u64(trajectory, value)
        n += 1
        steps += 1

    return {
        "ending_index": n,
        "steps": steps,
        "live": len(live),
        "rejected": rejected,
        "captured": captured,
        "merges": merges,
        "trajectory": trajectory,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10_000)
    parser.add_argument("--max-steps", type=int, default=20_000)
    args = parser.parse_args()
    result = certificate(args.n, args.max_steps)
    for key, value in result.items():
        if key == "trajectory":
            print(f"{key}: 0x{value:016x}")
        else:
            print(f"{key}: {value}")
    if result["live"]:
        raise SystemExit("certificate did not empty within the step limit")


if __name__ == "__main__":
    main()
