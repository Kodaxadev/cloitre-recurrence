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

## 4. Checkpoint monotonicity and signed distance

The quotient-zero dominance lemma has a second consequence that was not used
in the original safe certificate. If an infinite dominant path exists at
index `N`, take one step and reset the resulting positive state to quotient
zero. Dominance preserves an infinite continuation. Repeating this shows
that failure at `N` forces failure at every later index.

Thus the exact certificate at `N=10^6` covers all starting indices through
one million, not only that single index. A uniform proof need only establish
termination on an unbounded sequence of checkpoints. This is Theorem 46; it
does not turn any finite list of certificates into an infinite proof.

A further coordinate

```text
s = n+2,       x = s+1-2e
```

turns the two safe branches into

```text
x >= U+3 : x' = 2x-s, U' = U,
x <= 0   : x' = 2x+s, U' = U+1,
```

while `1<=x<=U+2` is exactly the terminating strip. This is Lemma 47.
It makes the obstruction especially sharp: an infinite path would be a
centered-doubling orbit that avoids a one-sided hole whose width is its own
negative-visit count. The coordinate is exact, but it does not supply a
pointwise Lyapunov function.

Checkpoint monotonicity also constrains a hypothetical first failure of the
unrestricted safe map. Its witness `e` must be odd, since even `e` has the
exact zero-step predecessor `e/2` at the preceding index. Reachable states
have even `e` at every odd index, so an odd-index first failure would be an
artifact of allowing unreachable initial states. The even-index case is not
resolved by this parity argument.

## 5. Quotient clearance and the even least-failure boundary

For a quotient-zero safe path, a zero step has exact slack

```text
sigma = n-U-2e >= 0.
```

Raising the initial quotient by `Q` preserves precisely those prefixes for
which every zero slack is at least `Q`; wraps do not depend on the quotient.
This quotient-clearance lemma turns the remaining backward argument into an
endpoint question.

At an even least failing checkpoint, an odd witness cannot begin with a
wrap. Its complementary residue below the midpoint either has a zero-step
predecessor or a wrap-step predecessor at the previous checkpoint, and both
merge into the alleged infinite path. If the witness begins with a zero,
the same predecessor construction works with initial quotient one unless
some zero slack is exactly zero.

Therefore an even least failure must start with `2e<=N` and later hit
`n-U-2e=0`. This is Theorem 50. Computation shows that zero-slack events do
occur on finite paths, so the endpoint cannot be dismissed empirically; it
is now the exact obstruction to completing this backward-induction route.

## 6. Accelerating the boundary return

The zero-slack obstruction can be accelerated exactly. At a zero epoch, put

```text
W = n-U,       d = W-2e.
```

After the zero and `k` maximal wraps, the next non-wrap state has candidate
slack

```text
d' = 2^(k+1)(U+d+4) - W - 2U - 2k - 7,
```

where `k` is the first index satisfying the corresponding non-wrap
inequality. Nonnegative `d'` is the next zero epoch; negative `d'` is
termination. This is Lemma 51.

For boundary input `d=0`, a surviving return has positive odd slack and
residue at most the boundary residue. Local equality occurs in the explicit
infinite family

```text
e = (2^k-1)(U+4)-k.
```

A hoped-for global descent is false. The exact path

```text
(14,0,7) --0--> (15,0,14) --1--> (16,1,11)
           --1--> (17,2,4) --0--> (18,2,8)
```

goes from one zero-slack boundary to another while increasing the boundary
residue. Corollary 52 proves that every later boundary residue must increase.
This removes simple boundary monotonicity from the viable proof strategies
and leaves an arithmetic return-map problem.
