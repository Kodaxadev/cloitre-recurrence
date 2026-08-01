# Boundary reduction for every periodic rational slope

This note generalizes the lift analysis used for denominators `3`, `5`, and
`7`. It reduces every possible reduced denominator to finitely many exact
boundary families.

## Theorem 32: every nonintegral periodic slope is a boundary slope

**Statement.** Let an admissible integer orbit have an eventually periodic,
nonzero quotient-change word. Suppose one phase slope `A` from Theorem 25 has
reduced denominator `d>1`. Then:

1. `d` is odd.
2. The fractional parts of the phase slopes form one doubling cycle
   `O` modulo `d`, of length `L=ord_d(2)<d`.
3. The quotient slope `mu` equals `(d-y)/d` for some residue `y` in `O`.

In particular, a periodic orbit with a nonintegral phase slope must lie
exactly on an admissibility-window boundary.

**Proof.** Theorem 25 writes every phase slope with denominator dividing
`2^p-1`, so its reduced denominator `d` is odd. If a phase has fractional
part `x/d`, the recurrence

```text
A_(j+1) = 2 A_j - a_j
```

shows that the next fractional numerator is `2x mod d`. Since `x` is a unit
modulo `d`, these numerators form a cycle of length `L=ord_d(2)`. Euler's
theorem gives `L<=phi(d)<d`.

For a residue `x`, the only possible lifts in the window
`[-mu,1-mu]` are

```text
x/d       when mu <= (d-x)/d,
x/d - 1   when mu >= (d-x)/d.
```

Summing `A_(j+1)=2A_j-a_j` over a full period gives
`sum_j A_j=sum_j a_j=p mu`, so the mean of the lifted slopes is exactly
`mu`.

Assume `mu` is unequal to every threshold `(d-x)/d` in the cycle. Then the
lift is uniquely determined by `x`, so the entire lifted slope sequence, and
therefore its digit word, repeats after `L` steps. Applying Theorem 25 to
this shorter digit period says `L A` is an integer. Since `A` has reduced
denominator `d`, this requires `d | L`, contradicting `0<L<d`. Therefore
`mu` must equal one of the thresholds. This proves all three claims.

## Lemma 33: exact boundary multiplicity

**Statement.** Let the doubling cycle be `O`, let `P` be the sum of its `L`
residues, and fix the boundary residue `y`. Let

```text
H = number of x in O with x > y,
N = P - H d - L(d-y).
```

If the period contains `R=p/L` repetitions of the fractional cycle and `K`
of the `R` occurrences of `y` use the negative lift, then necessarily

```text
K/R = N/d,       0 <= N <= d.
```

Conversely, this equation is exactly the mean-consistency condition; phase
integrality remains an additional necessary condition.

**Proof.** Begin with every residue represented by its positive lift. Its
mean is `P/(Ld)`. At `mu=(d-y)/d`, every residue greater than `y` must use
the negative lift, every residue less than `y` must use the positive lift,
and the `y` occurrences may use either. Each negative lift subtracts one.
Across `R` repeats there are `HR+K` negative lifts, hence

```text
(d-y)/d = P/(Ld) - H/L - K/(LR).
```

Solving gives the displayed formula. The bounds follow from `0<=K<=R`.

## Consequences

- For any fixed odd `d`, its unit cycles and all viable boundary residues are
  finite and exactly enumerable.
- If no boundary has `0<=N<=d`, denominator `d` is impossible at every
  period, without a period search.
- When a boundary survives, the choice of `K` positions among `R` repeated
  blocks is the only remaining freedom before applying Theorem 25's phase
  divisibility. The denominator-3 and denominator-7 subset-sum proofs are
  instances of this form.

The exact enumerator is
[`scripts/periodic_boundaries.py`](../../scripts/periodic_boundaries.py). Its output
is a finite classification for the requested denominator range, not a proof
that all denominators are absent.

## Theorem 36: universal block subset equation

**Statement.** Rotate a surviving boundary cycle so its boundary residue is
the last of its `L` slopes. Let `a_0,...,a_(L-1)` be the digit block when
that boundary uses its positive lift, and put

```text
B = 2^L,
C = sum_(j=0)^(L-1) a_j 2^(L-1-j),
E = sum_(j=0)^(L-1) a_j 2^(L-1-j)(j+2).
```

For `R` repeated blocks, let `G=(B^R-1)/d`. Define

```text
alpha = d [E(B-1) + LC] / (B-1)^2.
```

If `T` is the set of blocks using the negative boundary lift, phase
integrality requires, for some integer `J`,

```text
2 sum_(t in T) B^t = (alpha-J)G.                 (36.1)
```

**Proof.** The positive block represents the fixed phase slope
`A_0=C/(B-1)`. In block `l`, its contribution to Theorem 25's phase
numerator is

```text
B^(R-1-l) [E + LC l].
```

Summing the geometric progression and its derivative, then adding the
integer slope numerator `z=pA_0`, cancels every term proportional to `R`.
The all-positive-boundary phase numerator is exactly `alpha G`.

Changing the last slope in a block from `y/d` to `y/d-1` increases the
preceding digit by one and decreases the last digit by two. In the weighted
phase numerator the terms containing the absolute index cancel, leaving

```text
-2 B^(R-1-l).
```

Reindexing the selected block positions gives phase numerator
`alpha G-2 sum_(t in T)B^t`. Theorem 25 requires this to be divisible by
`G`, which is exactly (36.1).

**Use.** A subset of powers of `B` has a base-`B` expansion containing only
zeros and ones. Equation (36.1) therefore converts every surviving boundary
family into a digit certificate. The script
[`scripts/periodic_phase_blocks.py`](../../scripts/periodic_phase_blocks.py)
computes these exact certificates at the minimal repeat count; the next
corollary explains why that certifies every repeat count.

## Corollary 37: all periods excluded through denominator 501

**Statement.** No nonzero eventually periodic admissible orbit has a phase
slope with reduced denominator `d<=501`.

This is a finite, computer-assisted corollary of Theorems 32 and 36. It is
not an assertion about denominators above 501.

The omitted integral case cannot produce a nonzero word: the state window and
`0<=mu<=1/2` leave only integer slope zero, and the identity
`mean(A_j)=mu` then forces `mu=0` and every digit to be zero.

**Why one scale proves all scales.** For a boundary family, Lemma 33 requires

```text
d | LR,       d | NR.
```

The enumerator chooses their least common solution `R_0`; every possible
repeat count is `R=hR_0`. Put

```text
Q_h = 1 + B^R_0 + ... + B^((h-1)R_0).
```

Then `G_h=G_1 Q_h`, and `Q_h` is odd. The loose subset bound

```text
0 <= sum_(t in T) B^t <= (B^R-1)/(B-1)
```

shows that every possible integer `J` in (36.1) belongs to the same finite
interval, independent of `h`.

For each such `J`, if `(alpha-J)G_1` is odd, it stays odd after multiplication
by `Q_h` and cannot equal twice an integer. If it is even, the target at
scale `h` is the scale-one target multiplied by `Q_h`. In base `B`, this
concatenates `h` copies of the scale-one digit block without carries. A bad
digit remains bad; if all digits are zero or one, their count and the
required count `K=hK_0` both scale by `h`. Therefore the minimal scale is
an exact certificate for every scale.

**Finite certificate.** Running

```text
python scripts/periodic_phase_blocks.py --max-denominator 501
```

enumerates all 250 odd denominators from 3 through 501. Eighty-one have no
boundary family. The remaining denominators produce 463 boundary families.
For each family, the script enumerates every possible `J`, checks parity,
and checks the exact base-`B` digits and required number of selected blocks.
Zero phase-integral subset patterns survive. The deterministic certificate
digest is
`1508d04cc91c8a007d17028efb24fe726785f4f210272721d8fc7f6149d4bb06`;
the script asserts it when run through denominator 501.

## Theorem 38: no nonzero eventually periodic digit orbit

**Statement.** An admissible integer orbit cannot have an eventually
periodic, nonzero quotient-change word.

**Proof.** An integral phase slope cannot support a nonzero word, as noted
above. Otherwise Theorem 32 supplies an odd reduced denominator `d>1` and a
boundary family. If every boundary lift has the same sign (`K=0` or `K=R`),
the lifted slopes repeat after `L<d` steps; Theorem 25 would require `d|L`,
a contradiction. Hence `0<K<R`.

Use Theorem 36's rotation and put

```text
H = B-1,       S_R = 1+B+...+B^(R-1).
```

Because `L=ord_d(2)`, we have `d|H`. If the first signed slope is `s/d`,
then

```text
C/H = s/d,       C = sH/d.
```

Consequently Theorem 36's baseline ratio simplifies from

```text
alpha = d[E H + LC]/H^2
```

to

```text
alpha = (dE+Ls)/H.
```

Equation (36.1), multiplied by `d`, is therefore

```text
2d sum_(t in T) B^t = F S_R,                    (38.1)
F = dE+Ls-JH.
```

The selected set is nonempty and proper, so comparison with `S_R` gives

```text
0 < F < 2d.
```

Also `R>=2`: phase integrality gives `d|p=LR`, while `0<L<d`.

Write the first two base-`B` subset digits as
`epsilon_0,epsilon_1 in {0,1}`. Reducing (38.1) modulo `B` gives

```text
2d epsilon_0 = F  (mod B).
```

Here `d<B`, `B` is even, and `0<F<2d<2B`. There are only two cases.

- If `epsilon_0=0`, then `F=B`. Subtract the constant digit from (38.1)
  and divide by `B`. Reduction modulo `B` now requires
  `2d epsilon_1 = 1 (mod B)`, impossible because the left side and `B`
  are even.
- If `epsilon_0=1`, then `F=2d-B`. At the next digit, divisibility by
  `B` requires either `B-2d+1` (when `epsilon_1=0`) or `B+1` (when
  `epsilon_1=1`) to be divisible by `B`. Both are odd, while `B` is even.

Both possibilities fail. Thus the exact phase-integrality condition cannot
hold for any boundary family, at any denominator or repeat count.
