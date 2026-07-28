# Exact constraints on a genuinely aperiodic tail

Theorem 38 rules out every eventually periodic nonzero quotient-change word.
This note begins the remaining aperiodic analysis. It records two exact
reductions and a computational probe; it does not prove stabilization.

Write

```text
a_n = q_(n+1)-q_n in {-1,0,+1},
e_n = r_n-q_n.
```

All statements begin after entry into `q_n<=n`.

## Theorem 39: the future-digit identity

**Statement.** At every index `N`,

```text
e_N = sum_(k=0)^infinity a_(N+k)(N+k+2)/2^(k+1).       (39.1)
```

The series converges absolutely. Thus the entire future digit tail determines
the present integer state exactly.

**Proof.** Unroll the exact doubling law for `L` steps:

```text
e_(N+L)
 = 2^L e_N
   - sum_(k=0)^(L-1) 2^(L-1-k) a_(N+k)(N+k+2).
```

After division by `2^L`,

```text
e_N
 = sum_(k=0)^(L-1) a_(N+k)(N+k+2)/2^(k+1)
   + e_(N+L)/2^L.
```

The state window gives `|e_(N+L)|<=N+L`, so the final term tends to zero.
The same linear-over-exponential bound proves absolute convergence.

**Interpretation.** If

```text
X_N = sum_(k=0)^infinity a_(N+k)/2^(k+1),
Y_N = sum_(k=0)^infinity k a_(N+k)/2^(k+1),
```

then

```text
e_N = (N+2)X_N + Y_N,       |Y_N|<=2.                 (39.2)
```

Hence `e_N/(N+2)` shadows the signed binary value of its future digit word
to error at most `2/(N+2)`. For periodic words this specializes to the affine
phase formula behind Theorem 25; (39.1) remains exact without periodicity.

## Lemma 40: an eventually monotone tail is a hole-avoiding doubling orbit

**Statement.** Suppose an orbit never absorbs and has no down-step from some
index `N` onward. Then for every `n>=N`:

```text
e_n > 0,
a_n in {0,+1},
e_(n+1) = 2e_n mod (n+2),       0 < e_(n+1) < n+2,
```

where the remainder is least nonnegative. Moreover the orbit must avoid

```text
n+1-q_n <= 2e_n <= n+2.                              (40.1)
```

Equivalently, at every tail index it lies in one of the two regions

```text
2e_n < n+1-q_n       or       2e_n > n+2.             (40.2)
```

**Proof.** With no down-step, a negative `e_n` cannot produce an up-step.
Zero-steps would then double that negative integer while `q_n` stayed fixed,
eventually violating the lower state bound `e>=-q`. Thus a down-step would be
forced. Since `e=0` is absorption, every tail value must instead be positive.

The only digits are consequently zero and one. If `a_n=1`, positivity at the
next index requires

```text
e_(n+1)=2e_n-(n+2)>0,
```

so `2e_n>n+2`. Conversely this inequality automatically satisfies the
up-step threshold `q_n+2e_n>=n+1`. All smaller safe values use digit zero and
map to `2e_n`. Therefore the transition is exactly reduction of `2e_n`
modulo `n+2`.

An integer with `n+1-q_n<=2e_n<n+2` already triggers an up-step but produces
a negative next value, contradicting the first paragraph. Equality
`2e_n=n+2` produces absorption. This proves (40.1) and (40.2).

## Computational probe of monotone segments

The exact tool
[`search-framework/src/bin/monotone.rs`](search-framework/src/bin/monotone.rs)
tests every state with `e>0` at a selected index until its first down-step or
absorption. Exhaustive results include:

```text
start index    states checked    longest no-down segment    up / zero
    100             4,950                  75                28 / 47
  1,000           499,500                 223               109 / 114
 10,000        49,995,000                 822               368 / 454
```

At index `100,000`, restricting only the starting quotient to `q<=10`
checks 1,099,934 states; the longest segment is 2,466 steps with 1,178 ups.
No tested state avoids a down-step indefinitely.

The observed maximum is compatible with `O(sqrt(n))`, but that rate is only
computational evidence. Proving any finite upper bound uniform over all
positive states at index `n` would eliminate eventually monotone escape and
force every counterexample to contain infinitely many rebound cascades.

## Lemma 41: quotient-zero dominance

**Statement.** Fix an index `N` and a positive value `e<N`. If the state
`(N,q,e)` has a positive no-down continuation, then the state `(N,0,e)` has
the same digit and `e` continuation for at least as long. In particular, an
infinite no-down tail from any quotient would imply one from quotient zero.

Here `(N,q,e)` abbreviates `r=q+e`; only valid states are considered.

**Proof.** Lemma 40 shows that every positive no-down continuation follows the
pure moving-modulus map. Its positive up-steps are characterized by
`2e>N+2`, independently of `q`. At a zero-step the larger-quotient orbit
satisfies

```text
q + 2e < N+1.
```

Replacing `q` by a smaller quotient preserves that inequality. Induction
therefore gives the same pure digit and `e` sequence, while the quotient
difference stays constant. The quotient-zero state is valid because `e<N`.

## Exact compressed safe sweep

The auxiliary tool
[`search-framework/src/bin/pure.rs`](search-framework/src/bin/pure.rs)
implements two distinct computations:

- `--sweep` advances every pure moving-modulus state, ignoring the danger
  interval.
- `--safe-sweep` starts every `e` with quotient zero, rejects a zero-step as
  soon as `wraps+2e>=n+1`, and merges equal `e` values while retaining only
  the smallest wrap count. Lemma 41 proves that the retained state dominates
  every discarded larger-quotient copy.

The distinction is material. From index one million, one pure state survives
`10^8` steps, so pure capture has no short bound in this range. The safe sweep,
however, starts all 999,999 positive values and becomes empty after 9,019
steps, at index 1,009,019. Thus no positive state at index one million can
begin an infinite no-down tail.

Reproduce the safe certificate with

```text
cd search-framework
cargo run --release --bin pure -- \
  --n 1000000 --max-steps 20000 --safe-sweep
```

The asserted covering identity is

```text
999999 = 2756 danger rejections + 9 captures
       + 997234 dominated merges + 0 live.
```

This is an exact finite certificate at one index, not a uniform theorem in
`N`. A proof still needs a bound valid at arbitrarily large starting indices.

## Lemma 42: the two-counter safe map

**Statement.** Start the dominant path at index `N` with quotient zero. Let
`U` and `Z` count its wrap and zero digits so far, and define

```text
n = N+U+Z,       w = n-U = N+Z.
```

Every positive safe transition is exactly one of

```text
zero:  (e,w,U) -> (2e,             w+1,U)
       when 2e <= w,

wrap:  (e,w,U) -> (2e-w-U-2,       w,U+1)
       when 2e > w+U+2.
```

If neither inequality holds, the positive no-down continuation terminates
through danger or capture.

**Proof.** Along the quotient-zero path, the current quotient is the number
`U` of previous wraps and the current index is `N+U+Z`. A zero is safe
exactly when

```text
U+2e < n+1,
```

which, by integrality, is `2e<=n-U=w`. It doubles `e`, increments `n` and
`Z`, and therefore increments `w`.

A positive wrap is characterized by `2e>n+2=w+U+2`. It replaces `e` by
`2e-(n+2)`, increments both `n` and `U`, and leaves `w=n-U` unchanged. The
remaining strip is precisely Lemma 40's forbidden interval, including the
capture boundary.

**Reduced open problem.** Proving that this integer map always enters its
middle strip, for every `N>=2` and `1<=e<N`, would eliminate eventual
monotone escape. The computation in K13 is an exact finite instance of this
statement at `N=10^6`.

## Lemma 43: binary-Euclidean coordinates

**Statement.** In Lemma 42's dominant safe map, put

```text
h = w-e.
```

Then `e,h` are positive integers and every transition is exactly

```text
zero:  (e,h,U) -> (2e,             h-e+1,U)
       when e<=h,

wrap:  (e,h,U) -> (e-h-U-2,       2h+U+2,U+1)
       when e>h+U+2.
```

The path terminates precisely when

```text
h < e <= h+U+2.                                      (43.1)
```

Equivalently, set `H=h+U+2`. The two safe branches become

```text
zero:  (e,H,U) -> (2e,       H-e+1,U),
wrap:  (e,H,U) -> (e-H,      2H+1,U+1),
```

with conditions `e+U+2<=H` and `e>H`, respectively. At every state,

```text
e+H = n+2,
```

so both branches increase `e+H` by exactly one.

**Proof.** The invariant `0<e<w` gives `h=w-e>0`. Substituting `w=e+h`
into Lemma 42 turns `2e<=w` into `e<=h`, and its zero update gives

```text
h' = w+1-2e = h-e+1.
```

The wrap condition becomes `e>h+U+2`; its update gives

```text
e' = e-h-U-2,       h' = w-e' = 2h+U+2.
```

The gap between those branch conditions is (43.1). Finally
`H=h+U+2=n-e+2`, which gives the displayed equivalent map and
`e+H=n+2`. This is an exact change of coordinates, not an analogy.

## Lemma 44: exact wrap-run doubling

**Statement.** On any positive no-down segment, define

```text
h_n = n-r_n = n-q_n-e_n.
```

If `k` consecutive wrap digits `+1` begin at index `n`, then

```text
h_(n+k)+q_(n+k)+3 = 2^k (h_n+q_n+3),                 (44.1)
```

and consequently

```text
2^k (h_n+q_n+3) < n+k+3.                             (44.2)
```

In particular, every positive wrap run is finite.

**Proof.** At one positive wrap, `q'=q+1`, `e'=2e-(n+2)`, and
`n'=n+1`. Direct substitution gives

```text
h' = n'-q'-e' = 2h+q+2,
h'+q'+3 = 2(h+q+3).
```

Iteration proves (44.1). During the run, `n-q` is constant and positive
`e` gives `h<n-q`. At its end,

```text
h_(n+k)+q_n+k+3 < (n-q_n)+q_n+k+3 = n+k+3,
```

which proves (44.2). Exponential growth cannot satisfy (44.2) for
arbitrarily large `k`.

## Theorem 45: sharper growth on a monotone escape

**Statement.** Suppose a nonabsorbed orbit has no down-step at the digit
indices in `[N,n)`. Put `L=floor(log_2 n)`. Then

```text
q_n-q_N >= (n-N-L)/(L+1).                            (45.1)
```

Therefore, if a counterexample is eventually nondecreasing in quotient,

```text
liminf_(n->infinity) q_n log_2(n)/n >= 1,
liminf_(n->infinity) b_n log_2(n)/n^2 >= 1.          (45.2)
```

For the quotient-zero dominant map, its wrap counter `U` obeys the same
bound. Thus the forbidden strip in Lemma 42 grows at least on the
`n/log n` scale along any infinite safe path.

**Proof.** Let `P=q_n-q_N` be the number of `+1` digits in `[N,n)`, and
let `Z` be the number of zero digits. There are at most `P+1` zero runs.
Lemma 26 bounds every such run by `L`, because all end by index `n`.
Consequently

```text
n-N = P+Z <= P+(P+1)L = P(L+1)+L,
```

which is (45.1). For fixed `N`, multiply the resulting lower bound for
`q_n/n` by `log_2 n` and let `n` tend to infinity. Since
`b_n>=n q_n`, both assertions in (45.2) follow. In the dominant map,
`q_N=0` and each wrap increments `q`, so `q_n=U`.

Theorem 45 improves the leading constant supplied by Theorem 27 by a
factor of three, but only under eventual monotonicity. It does not force
the growing forbidden strip to be hit; that remains the uniform problem.
