# Research log: mixed-ridge compatibility

## Exact defect

For a ridge whose positive prefix has length `P`, the positive zeros at
offsets `i` contribute the integer

```text
W = sum (N+i+2) 2^(P-1-i).
```

The coordinate `A_n=n+3-e_n` doubles at an up-step and changes to
`2 A_n-(n+2)` at a zero-step. Consequently,

```text
2^P A-W = N+P+3+v.
```

Combining consecutive ridges gives

```text
2^P A-W+z+P'+1+v'-v = 2^P' A'-W'.
```

This is the exact arbitrary-word extension of Lemma 70.

## Low-bit restriction

Let `R` be the final consecutive up-run of the positive prefix, or `P`
for a pure prefix. Every term of `W` is divisible by `2^R`. Adjacent
ridges therefore obey

```text
2^min(R,R') divides z+P'+1+v'-v.
```

The same positive-integer descent used in Theorem 72 yields Theorem 75
for every infinite arbitrary-ridge chain.

## Adversarial checks and rejected shortcut

A raw-state sweep checked 6,846 finite ridges and 6,486 adjacent pairs;
5,980 adjacent pairs involved at least one mixed prefix. All exact
identities and congruences held.

The sweep also rejected the hoped-for shortcut that the terminal run
should inherit the long initial rebound. Among 5,158 mixed ridges in the
bounded grid, terminal lengths were:

```text
R=1: 3282
R=2: 1330
R=3:  491
R=4:   55
```

The valid local state `(n,q,r)=(64,4,0)` begins at least 100 consecutive
ridges with `R<=2`; after those ridges the state is `(878,215,55)`.
It has no preimage among literal starts `m<=256` at index 64, so this is
local falsification evidence only. It neither gives a reachable
counterexample nor disproves terminal-run growth under the combined
reachability and sublinear hypotheses.

## Remaining target

The mixed-word problem is now isolated in the low-order defect. A useful
next theorem would have to prove one of:

1. reachability plus sublinear quotient forces `R_j` to grow;
2. bounded `R_j` forces a contradiction by a different modulus;
3. the nested low bits of `W_j` cannot satisfy the compatibility equations
   along a reachable infinite chain.

Short-range ridge compatibility alone cannot prove the first statement.
