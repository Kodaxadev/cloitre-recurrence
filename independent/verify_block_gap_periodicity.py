#!/usr/bin/env python3
"""Independent check of L151, L152 and T153 (full block chain).

Recovers 2^P, W and V by finite differencing the composed T137 map rather than
trusting the closed forms in `block-gap-periodicity.md`.  Nothing here is part
of the proof of T153, which is unconditional in P; the bounded searches are
regression and falsification data.
"""
from __future__ import annotations

import argparse
import math
import sys


class VerificationError(AssertionError):
    """A checked property of the block chain failed."""


def need(cond: bool, what: str) -> None:
    if not cond:
        raise VerificationError(what)


# ------------------------------------------------------------- the exact map
def step(n: int, k: int, f: int, k_next: int, r: int) -> tuple[int, int, int]:
    """(137.2) once, with the next block length supplied."""
    n2 = n + k + 1 + r
    f2 = (f << (k_next + r + 1)) - ((1 << k_next) - 1) * (n2 + 4) + k_next
    return n2, k_next, f2


def compose(word, n0: int, f0: int) -> tuple[int, int]:
    """One aligned period.  word = [(k_t, r_t)]; the incoming block length is
    k_0, so a consistent periodic tail starts with k = k_0."""
    n, k, f = n0, word[0][0], f0
    for t, (_k, r) in enumerate(word):
        k_next = word[(t + 1) % len(word)][0]
        n, k, f = step(n, k, f, k_next, r)
    return n, f


def closed_forms(word) -> tuple[int, int]:
    """(B.2)/(151.1): P and W."""
    p = len(word)
    x = [word[(t + 1) % p][0] for t in range(p)]      # x_t = k_{t+1}
    z = [word[t][1] + 1 for t in range(p)]            # z_t = r_t + 1
    P = sum(xi + zi for xi, zi in zip(x, z))
    A = W = 0
    for xi, zi in zip(x, z):
        A += xi + zi
        W += ((1 << xi) - 1) << (P - A)
    return P, W


def primitive(word) -> bool:
    p = len(word)
    return all(p % d or tuple(word) != tuple(word[:d]) * (p // d)
               for d in range(1, p))


def order_mod(q: int) -> int:
    need(q > 1 and q % 2 == 1, f"order_mod needs odd q>1, got {q}")
    o, v = 1, 2 % q
    while v != 1:
        v = (v * 2) % q
        o += 1
    return o


# ------------------------------------------------------- L151: composition
def check_composition(words) -> int:
    for word in words:
        P, W = closed_forms(word)
        # (B.3): P is also the total index increase over one period
        n1, _ = compose(word, 100, 10)
        need(n1 - 100 == P, f"(B.3) failed for {word}: {n1-100} != {P}")
        base = compose(word, 100, 10)[1]
        w_emp = base - compose(word, 101, 10)[1]      # -d/dN
        pow_emp = compose(word, 100, 11)[1] - base    # d/df
        need(pow_emp == 1 << P, f"2^P mismatch for {word}")
        need(w_emp == W, f"W mismatch for {word}: {w_emp} != {W}")
        v_emp = (1 << P) * 10 - w_emp * (100 + 4) - base
        need(base == (1 << P) * 10 - W * 104 - v_emp,
             f"(151.1) inconsistent for {word}")
    return len(words)


def check_phase_control(word=((2, 0), (1, 2), (4, 1))) -> int:
    """NEGATIVE CONTROL 1 for (151.1): fixed (W,V) hold only on one phase."""
    p = len(word)
    rots = [tuple(word[j:] + word[:j]) for j in range(p)]
    coeffs = {closed_forms(r) for r in rots}
    need(len(coeffs) == p,
         f"phase control is vacuous: rotations of {word} share (P,W)")
    P0, W0 = closed_forms(rots[0])
    V0 = (1 << P0) * 10 - W0 * 104 - compose(rots[0], 100, 10)[1]
    misfires = 0
    for j, rot in enumerate(rots):
        Pj, Wj = closed_forms(rot)
        need(Pj == P0, "P must be rotation invariant by (B.3)")
        for n0, f0 in ((100, 10), (200, 7), (57, 13)):
            actual = compose(rot, n0, f0)[1]
            Vj = (1 << Pj) * 10 - Wj * 104 - compose(rot, 100, 10)[1]
            need(actual == (1 << Pj) * f0 - Wj * (n0 + 4) - Vj,
                 f"(151.1) failed in its own phase {j} of {word}")
            if j != 0:
                wrong = (1 << P0) * f0 - W0 * (n0 + 4) - V0
                need(wrong != actual,
                     f"phase-0 (W,V) predicted phase {j}: the 'every i' "
                     "reading would look valid here")
                misfires += 1
    return misfires


# --------------------------------------------------- L152: runs and periods
def run_pairs(W: int, P: int) -> tuple[tuple[int, int], ...]:
    """Cyclic alternating (one-run, following zero-run) pairs, high to low."""
    seq = [(W >> i) & 1 for i in range(P - 1, -1, -1)]     # index 0 = MSB
    need(any(seq) and not all(seq), "word must contain both digits")
    start = next(i for i in range(P) if seq[i] == 1 and seq[(i - 1) % P] == 0)
    lens, i = [], 0
    while i < P:
        v, L = seq[(start + i) % P], 0
        while L < P and seq[(start + i + L) % P] == v:
            L += 1
        lens.append(L)
        i += L
    need(len(lens) % 2 == 0, "alternating run list must have even length")
    return tuple((lens[j], lens[j + 1]) for j in range(0, len(lens), 2))


def rotations(word) -> set:
    w = list(word)
    return {tuple(w[i:] + w[:i]) for i in range(len(w))}


def run_pairs_preceding(W: int, P: int) -> tuple[tuple[int, int], ...]:
    """MUTATION: pair each one-run with the zero-run BEFORE it."""
    pairs = run_pairs(W, P)
    p = len(pairs)
    return tuple((pairs[t][0], pairs[(t - 1) % p][1]) for t in range(p))


def check_orientation(words) -> tuple[int, int, int]:
    """(152.2), plus NEGATIVE CONTROL 2 in two independent directions.

    The index shift is *not* a hazard: (k_(t+1), r_(t+1)+1) is the left rotation
    of (k_t, r_t+1), and (152.3) compares only up to rotation.  What is a hazard
    is pairing a one-run with the preceding rather than the following zero-run,
    and reading the cyclic run list in the wrong direction.  Both mutations must
    be rejected by some asymmetric witness.
    """
    shift_free = prec_rejected = rev_rejected = 0
    for word in words:
        P, W = closed_forms(word)
        got = run_pairs(W, P)
        p = len(word)
        fwd = tuple((word[t][0], word[t][1] + 1) for t in range(p))
        shifted = tuple((word[(t + 1) % p][0], word[(t + 1) % p][1] + 1)
                        for t in range(p))
        # (152.2): a rotation of the forward word, equivalently of the shift
        need(got in rotations(fwd),
             f"(152.2) failed for {word}: {got} not a rotation of {fwd}")
        need(rotations(fwd) == rotations(shifted),
             f"shift is not a rotation for {word}")
        shift_free += 1
        if run_pairs_preceding(W, P) not in rotations(fwd):
            prec_rejected += 1
        if tuple(reversed(fwd)) not in rotations(fwd):
            rev_rejected += 1
    need(prec_rejected > 0,
         "orientation control vacuous: no word rejects the preceding-zero pairing")
    need(rev_rejected > 0,
         "orientation control vacuous: no word rejects the reversed reading")
    return shift_free, prec_rejected, rev_rejected


def min_bin_period(W: int, P: int) -> int:
    b = format(W, f"0{P}b")
    for d in range(1, P + 1):
        if P % d == 0 and all(b[i] == b[i % d] for i in range(P)):
            return d
    return P


def all_words(P: int, max_letter: int):
    """Every joint word (k_t, r_t), k>=1, r>=0, with total exponent P."""
    out = []

    def rec(acc, tot):
        if tot == P:
            if acc:
                out.append(tuple(acc))
            return
        for k in range(1, min(max_letter, P - tot) + 1):
            for r in range(0, min(max_letter, P - tot - k - 1) + 1):
                rec(acc + [(k, r)], tot + k + r + 1)

    rec([], 0)
    return out


def check_lemma152_and_bridge(p_max: int, max_letter: int) -> tuple[int, int]:
    total = prim = 0
    for P in range(2, p_max + 1):
        for word in all_words(P, max_letter):
            Pw, W = closed_forms(word)
            if Pw != P:
                continue
            total += 1
            is_prim = primitive(word)
            prim += is_prim
            mp = min_bin_period(W, P)
            need(is_prim == (mp == P), f"(152.3) failed for {word}")
            pairs = run_pairs(W, P)
            if mp < P:                                   # L152 forward
                need(not primitive(pairs), f"L152 forward failed for {word}")
            if not primitive(pairs):                     # L152 converse
                c = min(d for d in range(1, len(pairs))
                        if len(pairs) % d == 0
                        and pairs == pairs[:d] * (len(pairs) // d))
                d_bits = sum(a + b for a, b in pairs[:c])
                need(P == (len(pairs) // c) * d_bits and 0 < d_bits < P,
                     f"L152 converse: bad d for {word}")
                bits = format(W, f"0{P}b")
                need(all(bits[i] == bits[(i + d_bits) % P] for i in range(P)),
                     f"L152 converse: translation by d fails for {word}")
    return total, prim


# --------------------------------------------------- T153 regression search
def check_divisibility(p_max: int, max_letter: int) -> tuple[int, int]:
    hits = prim_hits = 0
    for P in range(2, p_max + 1):
        d = (1 << P) - 1
        for word in all_words(P, max_letter):
            Pw, W = closed_forms(word)
            if Pw != P or (W * P) % d:
                continue
            hits += 1
            a = P * W // d
            q1, q2 = P // math.gcd(a, P), d // math.gcd(W, d)
            need(q1 == q2, f"(153.1) mismatch at {word}")
            need(1 < q1 <= P and q1 % 2 == 1 and d % q1 == 0,
                 f"q properties failed at {word}")
            d0 = order_mod(q1)
            need(P % d0 == 0 and d0 < P, f"(153.2) failed at {word}")
            if primitive(word):
                prim_hits += 1
    return hits, prim_hits


def check_t150_specialization() -> int:
    """All k=1 must reproduce T150's coefficient exactly, not merely agree."""
    def w_t150(hs):
        P, s, W = sum(hs), 0, 0
        for h in hs:
            s += h
            W += 1 << (P - s)
        return P, W

    cases = [(2, 3), (3, 2), (2, 2, 3), (4, 2, 5), (2, 3, 4, 2), (7, 3), (5,)]
    for hs in cases:
        word = tuple((1, h - 2) for h in hs)             # k=1, r = h-2
        P1, W1 = closed_forms(word)
        P2, W2 = w_t150(hs)
        need(P1 == P2 and W1 == W2,
             f"T150 specialization failed at h={hs}: ({P1},{W1}) != ({P2},{W2})")
    return len(cases)


def check_degenerate() -> int:
    """p=1, all k=1, all r=0, and each sign of the budget drift D."""
    seen = set()
    for word in [((1, 0),), ((3, 2),), ((1, 1), (1, 2)), ((2, 0), (3, 0)),
                 ((1, 5), (4, 0)), ((2, 0), (1, 2), (4, 1)), ((1, 0), (2, 2))]:
        P, W = closed_forms(word)
        need(W % 2 == 1 and W < (1 << (P - 1)), f"W shape wrong for {word}")
        run_pairs(W, P)                                   # must not raise
        D = sum(r + 1 - k for k, r in word)
        seen.add(0 if D == 0 else (1 if D > 0 else -1))
    need(seen == {-1, 0, 1}, f"budget trichotomy not exercised: {seen}")
    return len(seen)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--p-max", type=int, default=18)
    ap.add_argument("--max-letter", type=int, default=5)
    args = ap.parse_args()

    words = [((2, 0), (1, 2), (4, 1)), ((3, 1), (1, 0), (2, 3), (1, 1)),
             ((1, 2), (1, 1)), ((1, 0),), ((2, 1),), ((1, 3), (3, 0), (2, 1)),
             ((4, 0), (1, 1), (1, 4))]

    k = check_composition(words)
    print(f"L151 (B.3)/(151.1): P and W recovered by finite differencing "
          f"on {k} mixed-block words")

    mis = check_phase_control()
    print(f"L151 phase control: each rotation composes with its own (W,V); "
          f"phase-0 coefficients mispredict all {mis} unaligned cases")

    sf, pr, rv = check_orientation(words)
    print(f"L152 (152.2): run pairs are a rotation of (k_t, r_t+1) on all {sf} "
          f"words (the index shift is itself a rotation); {pr} reject the "
          f"preceding-zero pairing and {rv} reject the reversed reading")

    tot, prim = check_lemma152_and_bridge(args.p_max, args.max_letter)
    print(f"L152 both directions + (152.3): {tot} joint words with "
          f"P<={args.p_max} ({prim} primitive), equivalence holds on all")

    hits, prim_hits = check_divisibility(args.p_max, args.max_letter)
    print(f"T153 regression: {hits} words satisfy (151.3) for "
          f"P<={args.p_max}; primitive among them: {prim_hits}")
    need(prim_hits == 0,
         "a primitive word satisfied (151.3): T153 would be false")

    c = check_t150_specialization()
    print(f"T150 specialization: W identity holds on {c} all-unit words")

    d = check_degenerate()
    print(f"degenerate cases: p=1, all k=1, all r=0 and all {d} signs of D")

    print("VERDICT: composition, phase alignment, run orientation, the cyclic "
          "run lemma and the divisibility all hold on every case checked. The "
          "bounded searches are regression data; T153 is unconditional in P "
          "and does not rest on them.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"VERIFICATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
