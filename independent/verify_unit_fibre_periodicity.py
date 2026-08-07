#!/usr/bin/env python3
"""Independent check of L148, L149 and T150 (all-unit C147 fibre).

Reimplements the composed map from the recurrence alone and recovers W and V by
finite differencing, so the closed forms in `unit-fibre-arithmetic.md` are
checked rather than assumed.  Nothing here is part of the proof of T150, which
is unconditional in P; the bounded searches are regression and falsification
data.

Imports only the project's unit-state predicate and gate, to replay the
transport identity on the same transitions K18/K19 were built from.
"""
from __future__ import annotations

import argparse
import itertools
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from unit_gap_words_core import gate, is_unit_state  # noqa: E402


class VerificationError(AssertionError):
    """A checked property of the unit fibre failed."""


def need(cond: bool, what: str) -> None:
    if not cond:
        raise VerificationError(what)


# --------------------------------------------------------------- primitives
def v2(x: int) -> int:
    need(x != 0, "v2(0) is undefined")
    return (x & -x).bit_length() - 1


def odd_part(x: int) -> int:
    return x >> v2(x)


def primitive(word: tuple[int, ...]) -> bool:
    p = len(word)
    return all(p % d or word != word[:d] * (p // d) for d in range(1, p))


def order_mod(q: int) -> int:
    """ord_q(2) for odd q > 1."""
    need(q > 1 and q % 2 == 1, f"order_mod needs odd q>1, got {q}")
    o, x = 1, 2 % q
    while x != 1:
        x = (x * 2) % q
        o += 1
    return o


# ------------------------------------------------------- L148: composition
def step(f: int, m: int, h: int) -> tuple[int, int]:
    """(U.0) once: one gate at exponent h."""
    m = m + h
    return (f << h) - m, m


def compose(word, f0: int, m0: int) -> int:
    f, m = f0, m0
    for h in word:
        f, m = step(f, m, h)
    return f


def closed_form_WV(word) -> tuple[int, int, int]:
    P = sum(word)
    sigma = W = V = 0
    for h in word:
        sigma += h
        W += 1 << (P - sigma)
        V += sigma * (1 << (P - sigma))
    return P, W, V


def check_composition(words) -> int:
    """Recover W, 2^P and V by finite differencing; compare to the closed form."""
    for word in words:
        P, W, V = closed_form_WV(word)
        base = compose(word, 10, 100)
        w_emp = base - compose(word, 10, 101)          # -d/dm0
        pow_emp = compose(word, 11, 100) - base        # d/df0
        v_emp = (1 << P) * 10 - w_emp * 100 - base
        need(pow_emp == 1 << P, f"2^P mismatch for {word}")
        need(w_emp == W, f"W mismatch for {word}: {w_emp} != {W}")
        need(v_emp == V, f"V mismatch for {word}: {v_emp} != {V}")
        need(compose(word, 10, 100) == (1 << P) * 10 - W * 100 - V,
             f"(148.1) mismatch for {word}")
    return len(words)


def check_phase_alignment(word=(4, 2, 5)) -> int:
    """NEGATIVE CONTROL for (148.1).

    (148.1) holds only at the aligned indices i0 + k*p.  Starting one step later
    sees a rotation of the exponent word: P is unchanged but W and V are not.
    This fires if anyone restores the false "for every i" statement.
    """
    p = len(word)
    need(len(set(word)) > 1, "phase control needs a nonconstant word")
    rots = [tuple(word[j:] + word[:j]) for j in range(p)]
    P0, W0, V0 = closed_form_WV(rots[0])

    coeffs = {closed_form_WV(r)[1:] for r in rots}
    need(len(coeffs) == p,
         f"phase control is vacuous: rotations of {word} share (W,V)")

    misfires = 0
    for j, rot in enumerate(rots):
        Pj, Wj, Vj = closed_form_WV(rot)
        need(Pj == P0, "P must be rotation invariant")
        for f0, m0 in ((10, 100), (7, 200), (13, 57)):
            actual = compose(rot, f0, m0)
            need(actual == (1 << Pj) * f0 - Wj * m0 - Vj,
                 f"(148.1) failed in its own phase {j} of {word}")
            wrong = (1 << P0) * f0 - W0 * m0 - V0     # phase-0 coefficients
            if j != 0:
                need(wrong != actual,
                     f"phase-0 (W,V) wrongly predicted phase {j} of {word}: "
                     "the 'for every i' reading would look valid here")
                misfires += 1
    return misfires


# ------------------------------------------- L149: cyclic gaps + orientation
def cyclic_gaps(W: int, P: int) -> tuple[int, ...]:
    S = sorted(i for i in range(P) if (W >> i) & 1)
    need(bool(S), "empty bit set")
    if len(S) == 1:
        return (P,)
    return tuple(
        (S[k + 1] - S[k]) if k < len(S) - 1 else (P - S[-1] + S[0])
        for k in range(len(S))
    )


def rotations(word) -> set[tuple[int, ...]]:
    w = list(word)
    return {tuple(w[i:] + w[:i]) for i in range(len(w))}


def check_orientation(words) -> int:
    """(149.1): gaps are a rotation of the REVERSED word, not of the word."""
    asym = 0
    for word in words:
        P, W, _ = closed_form_WV(word)
        gaps = cyclic_gaps(W, P)
        need(gaps in rotations(tuple(reversed(word))),
             f"orientation: gaps {gaps} not a rotation of reversed {word}")
        if gaps not in rotations(word):
            asym += 1        # word where a rotation-only convention would fail
    need(asym > 0, "orientation test is vacuous: no asymmetric word exercised")
    return asym


def min_binary_period(W: int, P: int) -> int:
    bits = format(W, f"0{P}b")
    for d in range(1, P + 1):
        if P % d == 0 and all(bits[i] == bits[i % d] for i in range(P)):
            return d
    return P


def exponent_words(P: int):
    """Every exponent word with sum P and all letters >= 2, via its bit set."""
    out = []

    def build(acc, W):
        top = acc[0]
        if P - top >= 2:
            out.append((tuple([P - top] + [acc[i] - acc[i + 1]
                                           for i in range(len(acc) - 1)]), W))
        for e in range(top + 2, P - 1):
            build([e] + acc, W + (1 << e))

    build([0], 1)
    return out


def check_bridge(p_max: int) -> tuple[int, int]:
    """(149.2): word primitive  <=>  P-block of W has minimal period P.
    Also checks L149 directly: a proper block period gives a periodic gap word."""
    total = prim = 0
    for P in range(2, p_max + 1):
        for word, W in exponent_words(P):
            total += 1
            is_prim = primitive(word)
            prim += is_prim
            mp = min_binary_period(W, P)
            need(is_prim == (mp == P), f"(149.2) failed for {word}")
            g = cyclic_gaps(W, P)
            if mp < P:                       # L149 forward direction
                need(not primitive(g), f"L149 forward failed for {word}")
            if not primitive(g):             # L149 converse direction
                c = min(d for d in range(1, len(g))
                        if len(g) % d == 0 and g == g[:d] * (len(g) // d))
                dd = sum(g[:c])
                need(P == (len(g) // c) * dd and 0 < dd < P,
                     f"L149 converse: bad d for {word}")
                S = {i for i in range(P) if (W >> i) & 1}
                need({(x + dd) % P for x in S} == S,
                     f"L149 converse: S+d != S for {word}")
    return total, prim


# ------------------------------------------------- T150: divisibility search
def legal_W(W: int, P: int) -> bool:
    """W is an exponent-set sum iff odd (bit 0 set), < 2^(P-1) (h_0>=2),
    and no two adjacent one-bits (all gaps >= 2)."""
    return W % 2 == 1 and W < (1 << (P - 1)) and (W & (W >> 1)) == 0


def word_of(W: int, P: int) -> tuple[int, ...]:
    E = [i for i in range(P) if (W >> i) & 1][::-1]
    return tuple([P - E[0]] + [E[i] - E[i + 1] for i in range(len(E) - 1)])


def check_divisibility_hits(p_max: int) -> tuple[int, int]:
    """Every word satisfying (148.2) up to p_max must be a non-primitive
    repetition, and must satisfy the whole (150.2)/(150.3) chain."""
    hits = primitive_hits = 0
    for P in range(2, p_max + 1):
        d = (1 << P) - 1
        g = math.gcd(d, P)
        if g < 3:            # then W >= d/g > d/3 is impossible
            continue
        Q, j = d // g, 1
        while j * Q <= d // 3:
            W = j * Q
            if legal_W(W, P):
                hits += 1
                word = word_of(W, P)
                need(sum(word) == P and all(h >= 2 for h in word),
                     f"reconstructed word invalid at P={P}")
                need((W * P) % d == 0, f"(148.2) not satisfied at P={P}")
                a = P * W // d
                q1, q2 = P // math.gcd(a, P), d // math.gcd(W, d)
                need(q1 == q2, f"(150.2) mismatch at P={P}")
                need(q1 > 1 and q1 % 2 == 1 and d % q1 == 0 and q1 <= P,
                     f"q properties failed at P={P}")
                d0 = order_mod(q1)
                need(P % d0 == 0 and d0 < P, f"(150.3) failed at P={P}")
                bits = format(W, f"0{P}b")
                need(all(bits[i] == bits[i % d0] for i in range(P)),
                     f"P-block is not the d0-block repeated at P={P}")
                if primitive(word):
                    primitive_hits += 1
            j += 1
    return hits, primitive_hits


# ------------------------------------ transport identity on the real gate map
def check_transport(n_max: int) -> int:
    steps = 0
    for n in range(2, n_max + 1):
        for D in range(n % 2, n + 1, 2):
            u = (n - D) // 2
            top = min(D - 3, (n + D + 2) // 4)
            for f in range(1, top + 1):
                if (n + 3 + f) % 4 or not is_unit_state(n, u, f):
                    continue
                got = gate(n, u, f)
                if got is None:
                    continue
                h, g, n2, _u2 = got
                s_next = n2 + 3 + g
                need(s_next == (f << h), f"(U.2) failed at {(n, u, f)}")
                need(v2(s_next) == h + v2(f), f"(U.3) v2 failed at {(n, u, f)}")
                need(odd_part(s_next) == odd_part(f),
                     f"(U.3) odd part failed at {(n, u, f)}")
                need(s_next % 4 == 0, f"(U.3) mod 4 failed at {(n, u, f)}")
                need((g + n2 + 3) % (1 << (h + v2(f))) == 0,
                     f"(U.4) failed at {(n, u, f)}")
                steps += 1
    return steps


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--p-bridge", type=int, default=22,
                    help="bound for the exhaustive (149.2) bridge check")
    ap.add_argument("--p-hits", type=int, default=400,
                    help="bound for the (148.2) regression search")
    ap.add_argument("--n-max", type=int, default=200,
                    help="bound for replaying (U.2)-(U.4) on the gate map")
    args = ap.parse_args()

    words = [(2,), (5,), (2, 3), (3, 2), (2, 2, 3), (4, 2, 5), (2, 3, 4, 2),
             (7, 3), (2, 5, 3, 2, 4), (3, 3, 2, 2, 4, 2), (9, 2, 2, 3)]

    k = check_composition(words)
    print(f"L148 (148.1): W and V recovered by finite differencing on {k} words")

    mis = check_phase_alignment()
    print(f"L148 phase control: (148.1) holds in each phase of (4,2,5) with that "
          f"phase's own (W,V); the phase-0 coefficients mispredict every one of "
          f"{mis} unaligned cases, as a 'for every i' reading would require")

    asym = check_orientation(words)
    print(f"L149 (149.1): gaps are rotations of the reversed word; "
          f"{asym} of {len(words)} words refute a rotation-only convention")

    total, prim = check_bridge(args.p_bridge)
    print(f"L149 both directions + (149.2): {total} exponent words with "
          f"P<={args.p_bridge} ({prim} primitive), equivalence holds on all")

    hits, prim_hits = check_divisibility_hits(args.p_hits)
    print(f"T150 regression: {hits} words satisfy (148.2) for P<={args.p_hits}; "
          f"primitive among them: {prim_hits}")
    need(prim_hits == 0,
         "a primitive word satisfied (148.2): T150 would be false")

    steps = check_transport(args.n_max)
    print(f"(U.2)-(U.4): {steps} exact gate transitions replayed, n<={args.n_max}")

    print("VERDICT: the composition, orientation, bridge and divisibility "
          "properties behind L148/L149/T150 hold on every case checked. The "
          "bounded searches are regression data; T150 itself is unconditional "
          "in P and does not rest on them.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"VERIFICATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
