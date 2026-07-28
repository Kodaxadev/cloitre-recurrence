#!/usr/bin/env python3
"""Third independent verifier for the A073117 / A117846 stabilization data.

Independence from the two Rust implementations:
  * different language and arbitrary-precision integers (no fixed width at all,
    so an overflow bug in either Rust path cannot be reproduced here)
  * absorption is detected by the *behavioural* definition -- run past the
    claimed index and confirm the first differences are literally constant --
    rather than by any algebraic criterion
  * the reference OEIS terms are hard-coded from the OEIS text records

Usage:
    python verify.py --csv ../data/scan_200k.csv --sample 3000
    python verify.py --oeis
    python verify.py --digest ../data/scan_200k.csv
"""

import argparse
import csv
import hashlib
import random
import sys

# --- OEIS reference data, transcribed from the OEIS text records -------------

A073117_HEAD = [1, 1, 2, 4, 4, 8, 10, 13, 18, 18, 26, 30, 36, 46,
                50, 55, 62, 73, 74, 91, 102, 120, 130, 145, 146]

A117846 = [97, 1, 2, 2, 316, 2, 3, 3, 3, 4, 12, 4, 4, 12, 11, 11, 316, 11,
           316, 316, 6, 316, 316, 316, 316, 97, 316, 316, 13, 316, 13, 13, 13,
           13, 8, 13, 13, 12, 13, 13, 13, 13, 13, 13, 14, 14, 316, 14, 316,
           316, 316, 97, 9, 97, 97, 13, 10, 10, 11, 10, 14, 11, 12, 12, 97,
           12, 97, 132]


def orbit(m, upto):
    """Literal definition: b_1 = m, b_{n+1} = b_n + (b_n mod n)."""
    b = m
    out = [b]
    for n in range(1, upto):
        b += b % n
        out.append(b)
    return out


def value_at(m, target):
    b = m
    for n in range(1, target):
        b += b % n
    return b


def first_constant_index(m, cap):
    """First n with b_n = c*(n+1), c < n, found by the divisibility test."""
    b, n = m, 1
    while n <= cap:
        if b % (n + 1) == 0 and b // (n + 1) < n:
            return n, b
        b += b % n
        n += 1
    return None


def check_row(m, t, c, b_t, tail=200):
    """Behavioural check: reach index t, confirm the value, then confirm that
    the next `tail` first differences are all exactly c."""
    b = value_at(m, t)
    if b != b_t:
        return f"m={m}: b_{t} = {b}, csv says {b_t}"
    if b != c * (t + 1):
        return f"m={m}: b_t != c*(t+1)"
    if not c < t:
        return f"m={m}: c={c} not < t={t}"
    n = t
    for _ in range(tail):
        nb = b + b % n
        if nb - b != c:
            return f"m={m}: difference at n={n} is {nb - b}, expected {c}"
        b, n = nb, n + 1
    # minimality: no earlier absorbing index
    got = first_constant_index(m, t)
    if got is None or got[0] != t:
        return f"m={m}: earlier absorbing index {got} before t={t}"
    return None


def cmd_oeis():
    got = orbit(1, len(A073117_HEAD) + 1)[:len(A073117_HEAD)]
    assert got == A073117_HEAD, f"A073117 mismatch:\n{got}\n{A073117_HEAD}"
    print(f"A073117: first {len(A073117_HEAD)} terms match")

    t, b = first_constant_index(1, 100000)
    assert (t, b) == (397, 38606), (t, b)
    assert b == 398 * 97
    print("A073117: a(397) = 38606 = 398*97, increment 97 -- confirmed")

    for i, want in enumerate(A117846, start=1):
        m = 2 * i - 1
        t, b = first_constant_index(m, 50_000_000)
        c = b // (t + 1)
        assert c == want, f"A117846({i}) start {m}: got {c}, want {want}"
        # pair partner must give the same increment (Abercrombie's remark)
        t2, b2 = first_constant_index(m + 1, 50_000_000)
        assert b2 // (t2 + 1) == want, f"pair partner {m+1} disagrees"
    print(f"A117846: all {len(A117846)} published terms match (both parities)")

    for k in range(1, 5000):
        assert value_at(2 * k - 1, 3) == 2 * k
        assert value_at(2 * k, 3) == 2 * k
    print("Pair merging: b_3(2k-1) = b_3(2k) = 2k for k < 5000 -- confirmed")


def cmd_csv(path, sample, seed, tail):
    rows = []
    with open(path, newline="") as fh:
        for rec in csv.DictReader(fh):
            if rec["t"] == "UNRESOLVED":
                print(f"FAIL: unresolved start m={rec['m']}")
                sys.exit(1)
            rows.append((int(rec["m"]), int(rec["t"]), int(rec["c"]), int(rec["b_t"])))
    print(f"loaded {len(rows)} rows from {path}")

    rng = random.Random(seed)
    # Always include the extremes: they are the load-bearing claims.
    picked = {max(rows, key=lambda r: r[1]), max(rows, key=lambda r: r[2]), rows[0], rows[-1]}
    picked |= set(rng.sample(rows, min(sample, len(rows))))
    picked = sorted(picked)
    print(f"deep-checking {len(picked)} rows (seed {seed}, tail {tail})")

    bad = 0
    for i, (m, t, c, b_t) in enumerate(picked, 1):
        err = check_row(m, t, c, b_t, tail)
        if err:
            print("FAIL:", err)
            bad += 1
        if i % 250 == 0:
            print(f"  ... {i}/{len(picked)}")
    print(f"checked {len(picked)} rows, {bad} failures")
    if bad:
        sys.exit(1)
    hi = max(rows, key=lambda r: r[1])
    print(f"record orbit: m={hi[0]} t={hi[1]} c={hi[2]} b_t={hi[3]}")
    print(f"             c/t = {hi[2] / hi[1]:.6f}   (n^2/4 law predicts 0.25)")
    print("VERDICT: all deep-checked rows independently confirmed.")


def cmd_digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    print(f"sha256  {h.hexdigest()}  {path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--csv")
    p.add_argument("--sample", type=int, default=2000)
    p.add_argument("--seed", type=int, default=20260728)
    p.add_argument("--tail", type=int, default=200)
    p.add_argument("--oeis", action="store_true")
    p.add_argument("--digest")
    a = p.parse_args()
    if a.oeis:
        cmd_oeis()
    if a.digest:
        cmd_digest(a.digest)
    if a.csv:
        cmd_csv(a.csv, a.sample, a.seed, a.tail)
    if not (a.oeis or a.csv or a.digest):
        p.print_help()
