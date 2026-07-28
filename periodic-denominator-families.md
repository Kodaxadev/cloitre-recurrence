# Periodic slope denominators 5 and 7

This note continues the exact periodic-orbit analysis from
[`periodic-orbit-analysis.md`](periodic-orbit-analysis.md). It excludes two
more infinite families of rational slopes. No bounded-period assumption is
used.

Suppose an eventually periodic quotient-digit word has period `p`. The
notation from Theorem 25 applies:

```text
e_(n+p) - e_n = p A_j
```

at phase `j`, where every `e_n` is an integer. Hence `p A_j` is an integer.
The normalized phase states satisfy

```text
A_(j+1) = 2 A_j - a_j,       -mu <= A_j <= 1-mu,
mu = (1/p) sum_j A_j,
```

with `a_j` an integer digit. Reducing modulo one shows that the fractional
parts of the `A_j` follow the doubling map.

## Theorem 30: denominator 5 is impossible

**Statement.** No eventually periodic admissible integer orbit can have a
phase slope whose reduced denominator is `5`.

**Proof.** The doubling orbit modulo one is

```text
1/5 -> 2/5 -> 4/5 -> 3/5 -> 1/5.
```

The same argument works after rotating the four phases. Since `p A_j` is an
integer, `5 | p`; since the fractional orbit has length four, `4 | p`.
Consequently the four residues occur equally often.

Because `0 <= mu <= 1/2`, the admissible lifts of the four residues are:

```text
residue   positive lift condition   negative lift condition
  1/5          always                    never
  2/5          always                    never
  4/5          mu <= 1/5                 mu >= 1/5
  3/5          mu <= 2/5                 mu >= 2/5
```

At a boundary either lift is permitted. Start with all four positive lifts,
whose mean is `1/2`. Let `E` be the total number of negative lifts in one
period. Replacing a positive lift by its negative representative subtracts
one, so

```text
mu = 1/2 - E/p.
```

Now split at the only two thresholds.

- If `mu < 1/5`, all lifts must be positive, giving `mu=1/2`.
- If `mu = 1/5`, only the `4/5` phases can be negative. The mean requires
  `E=3p/10`, but there are only `p/4` such phases.
- If `1/5 < mu < 2/5`, every `4/5` lift is negative and every `3/5` lift is
  positive. Thus `E=p/4` and necessarily `mu=1/4`.
- If `mu = 2/5`, the mandatory negative `4/5` lifts already give `E=p/4`,
  while the mean would require only `E=p/10`.
- If `mu > 2/5`, both the `4/5` and `3/5` lifts are negative, giving
  `E=p/2` and hence `mu=0`.

Only the middle case survives. Its lifts are uniquely

```text
1/5, 2/5, -1/5, 3/5
```

and therefore its digit word has period four. Returning to the same phase
after four steps would give

```text
e_(n+4) - e_n = 4 A_j.
```

The left side is an integer, but `A_j` has reduced denominator five, so the
right side is not. This contradiction proves the theorem.

## Theorem 31: denominator 7 is impossible

**Statement.** No eventually periodic admissible integer orbit can have a
phase slope whose reduced denominator is `7`.

**Proof.** Doubling modulo one has two nonzero cycles:

```text
O1: 1/7 -> 2/7 -> 4/7 -> 1/7
O2: 3/7 -> 6/7 -> 5/7 -> 3/7.
```

Here `7 | p`, and each fractional cycle has length three, so `p=21h` for
some positive integer `h`.

For `O1`, the `1/7` and `2/7` lifts must be positive. The `4/7` lift can be
negative only when `mu >= 3/7`. But starting from the positive-lift mean
`1/3`, any negative lift only lowers the mean. Thus all lifts are positive,
`mu=1/3`, and the digit word has period three. Then `3 A_j` would have to
be an integer, contrary to the reduced denominator seven.

For `O2`, the `3/7` lift is always positive. The `6/7` lift switches sign
at `mu=1/7`, and the `5/7` lift switches at `mu=2/7`. Starting from the
positive-lift mean `2/3`, again write

```text
mu = 2/3 - E/p,
```

where `E` counts negative lifts.

- Below `1/7`, no lift is negative, contradicting the mean.
- At `1/7`, the required `E=11p/21` exceeds the `p/3` available `6/7`
  phases.
- Strictly between `1/7` and `2/7`, exactly the `p/3` many `6/7` phases
  are negative, forcing `mu=1/3`, outside the interval.
- At `2/7`, all `6/7` phases are negative and exactly `p/21=h` of the
  `5/7` phases must be negative.
- Above `2/7`, both kinds are always negative, forcing `mu=0`.

It remains to eliminate the boundary family at `mu=2/7`. Rotate so each
three-step block starts at `A=3/7`. There are `R=p/3=7h` blocks, of two
types:

```text
P: (3/7, -1/7,  5/7), digits (1,-1, 1), block sum 1
N: (3/7, -1/7, -2/7), digits (1, 0,-1), block sum 0.
```

Exactly `h` blocks are of type `N`. Put

```text
M = 2^p - 1 = 8^R - 1,       G = M/7.
```

For the all-`P` baseline, direct summation of the phase numerator `D` from
Theorem 25 gives

```text
D_P = sum_(t=0)^(R-1) 8^t (9R - 3 - 9t).
```

Since the rotated phase has `A=3/7`, its integer slope numerator is
`z=pA=9h`. Using

```text
sum 8^t = G,
sum t 8^t = [8 + 8^R(7R-8)]/49,
R=7h,
```

one obtains the exact identity

```text
z + D_P = 51G/7.
```

Replacing block `P` by `N` at block position `l` decreases `D` by

```text
2 * 8^(R-1-l).
```

The phase-integrality condition from Theorem 25 is `G | z+D`. Therefore
the `h` replacement positions, written as a set `T`, would have to satisfy

```text
sum_(t in T) 8^t = G/7       or       9G/14.
```

The second value is not an integer because `G` is odd. For the first,

```text
G/7 = (8^(7h)-1)/49
    = 42799 * sum_(j=0)^(h-1) 8^(7j),
42799 = (123457)_8.
```

The displayed base-eight blocks do not overlap. Their digits include
`2,3,4,5,7`, whereas a sum of distinct powers of eight has only digits zero
and one. Thus the first equality is also impossible. This eliminates the
last case and proves the theorem.

## Theorem 34: denominator 9 is impossible

**Statement.** No eventually periodic admissible integer orbit can have a
phase slope whose reduced denominator is `9`.

**Proof.** The only viable boundary family from Theorem 32 and Lemma 33 is

```text
cycle: 1, 2, 4, 8, 7, 5 modulo 9
mu = 2/9
K/R = 2/3.
```

Thus `R=3h`, `p=6R=18h`, and exactly `2h` of the `R` boundary occurrences
use the negative lift. Rotate each six-step block to start at `A=1/9`.
The two block types are

```text
P slopes: (1,2,4,-1, 7,5)/9, digits (0,0,1,-1, 1,1)
N slopes: (1,2,4,-1,-2,5)/9, digits (0,0,1, 0,-1,1).
```

There are `h` blocks of type `P` and `2h` of type `N`. Put

```text
M = 2^p - 1 = 64^R - 1,       G = M/9.
```

For the all-`N` baseline, direct summation in Theorem 25 gives

```text
D_N = sum_(t=0)^(R-1) 64^t (42R - 15 - 42t).
```

The rotated phase has `A=1/9`, so `z=pA=2h`. Using the finite geometric
sum and its derivative gives

```text
z + D_N = 83G/21.
```

Replacing an `N` block at position `l` by a `P` block increases `D` by

```text
4 * 64^(R-1-l).
```

Because the `h` selected powers sum to less than
`1+64+...+64^(R-1)=G/7`, the divisibility condition `G | z+D` has only one
possible multiple. It forces

```text
4 * sum_(t in T) 64^t = G/21,
sum_(t in T) 64^t = G/84.
```

But `G=(64^R-1)/9` is odd, so `G/84` is not an integer. The left side is
an integer, a contradiction.

## Theorem 35: denominator 11 is impossible

**Statement.** No eventually periodic admissible integer orbit can have a
phase slope whose reduced denominator is `11`.

**Proof.** Theorem 32 and Lemma 33 leave one boundary family:

```text
cycle: 1,2,4,8,5,10,9,7,3,6 modulo 11
mu = 3/11,       K/R = 3/11.
```

Thus `R=11h`, `p=10R=110h`, and `3h` boundary lifts are negative. Rotate
each block to start at `A=1/11`. The positive-boundary and
negative-boundary digit blocks are

```text
P: (0,0,0, 1,1,0,-1,1,0,1), block sum 3
N: (0,0,1,-1,1,0,-1,1,0,1), block sum 2.
```

There are `8h` blocks of type `P` and `3h` of type `N`. Put

```text
M = 2^p - 1 = 1024^R - 1,       G = M/11.
```

For the all-`P` baseline, direct summation gives

```text
D_P = sum_(t=0)^(R-1) 1024^t (930R - 435 - 930t).
```

Here `z=p/11=10h`. The geometric-sum identities, with
`1023=11*93`, simplify exactly to

```text
z + D_P = 5455G/1023.
```

Replacing a `P` block by an `N` block decreases `D` by

```text
128 * 1024^(R-1-l).
```

Let `T` contain the `3h` replacement positions. Since

```text
sum_(t in T) 1024^t < (1024^R-1)/1023 = G/93,
```

the value

```text
5455G/1023 - 128 sum_(t in T) 1024^t
```

lies strictly between `3G` and `6G`. The divisibility condition `G|z+D`
therefore permits only `4G` or `5G`. After multiplying by `1023`, these
two cases respectively require

```text
128*1023 sum_(t in T) 1024^t = 1363G,
128*1023 sum_(t in T) 1024^t = 340G.
```

The left side has 2-adic valuation at least seven. Since `G` is odd, the
right sides have valuations zero and two. Both equalities are impossible.

## Consequence and limitation

Theorems 29--31, 34, and 35 exclude every eventually periodic admissible
orbit having a phase slope with reduced denominator `3`, `5`, `7`, `9`, or
`11`, for arbitrary period. This is stronger than the finite period census,
but it is not yet a proof for all rational denominators and does not address
aperiodic escape.
