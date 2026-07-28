# Aperiodic research log

This continues [`research-log.md`](research-log.md) after that file reached the
project's authored-file size limit.

## 1. Pure moving-modulus map versus the danger interval

Lemma 40 separates a hypothetical no-down tail into two components:

```text
pure dynamics: e_(n+1) = 2e_n mod(n+2),
admissibility: zero digits require q_n+2e_n < n+1.
```

The pure dynamics alone can be extremely long. A compressed image sweep from
index `10^6` starts all `999,999` nonzero residues. After `10^8` steps, one
state remains, with `e=49,383,743`; its witness is the starting value `e=2`.
This disproves the working assumption that pure capture should have a short
uniform bound. It does not establish an infinite pure orbit.

For a pure path begun with quotient zero, let `U_n` count wrap digits. A zero
is safe exactly when

```text
n - 2e_n - U_n >= 0.
```

For fixed `e`, a smaller starting quotient can only make this inequality
easier and never changes a positive wrap. Lemma 41 formalizes the resulting
quotient-zero dominance.

This enables a compressed safe sweep keyed only by `e`. When paths merge, the
copy with the smallest wrap count dominates every other copy. Exact results:

```text
start index       positive starts       last safe index       duration
        100                    99                   173             73
      1,000                   999                 1,222            222
     10,000                 9,999                10,819            819
  1,000,000               999,999             1,009,019          9,019
```

The square-root scale remains striking but unproved. The compression turns
the monotone-tail question into a one-dimensional exact survivor problem;
the missing step is a bound uniform in the starting index.

## 2. Two-counter form

Writing `w=n-U=N+Z` makes the safe rule independent of the full historical
state:

```text
2e <= w       : zero, increment w;
2e > w+U+2    : wrap, increment U;
otherwise     : terminate.
```

The corresponding `e` updates are `2e` and `2e-w-U-2`. Lemma 42 proves this
reduction. It is now the smallest exact formulation of the eventual-monotone
subproblem; no empirical distribution assumption remains in its statement.

## 3. Binary-Euclidean form and run growth

Writing `h=w-e` turns the safe map into a gap version of a binary Euclidean
algorithm. A zero doubles `e` and subtracts it from `h` (with the exact
index correction `+1`); a wrap doubles the complementary side and subtracts
it from `e`. The forbidden region is simply

```text
h < e <= h+U+2.
```

This is Lemma 43. It exposes a second exact doubling law: during consecutive
wraps, `h+q+3` doubles at every step (Lemma 44). Thus neither zero runs nor
wrap runs can be infinite.

Counting the zero runs gives a quantitative consequence. On a no-down segment
ending at `n`, if `L=floor(log_2 n)`, then

```text
q_n-q_N >= (n-N-L)/(L+1).
```

Hence an eventually monotone counterexample would satisfy
`liminf q_n log_2(n)/n >= 1` (Theorem 45), sharpening the general
counterexample bound by a factor of three in its leading constant. The
forbidden strip must therefore grow on the `n/log n` scale. The unresolved
step is still deterministic capture: a growing hole need not be hit merely
because its measure grows.
