# Continuation audit: Theorem 58 and Lemma 63

## Scope and evidence boundary

This is the requested continuation of
[`opus-pr2-audit.md`](opus-pr2-audit.md). That audit rederived the
post-freeze ridge cut through Theorem 77 but left its imported Theorem 58
and Lemma 63 unchecked. This pass audits those two imports against:

- [`sparse-downstep-analysis.md`](../sparse-downstep-analysis.md);
- [`ridge-segment-analysis.md`](../ridge-segment-analysis.md);
- the compact proofs in
  [`manuscript/08-sparse-downsteps.md`](../manuscript/08-sparse-downsteps.md)
  and
  [`manuscript/09-ridge-segments.md`](../manuscript/09-ridge-segments.md);
- the raw-transition verifiers
  [`verify_sharp_growth.py`](../independent/verify_sharp_growth.py) and
  [`verify_ridge_segments.py`](../independent/verify_ridge_segments.py).

This is an internal AI proof audit, not human peer review. The finite checks
are regression evidence and do not replace the symbolic arguments.

## Theorem 58

### Rebound implication

Fix \(s\ge2\). At a down-step \(k\), the tail condition

\[
2^{s+2}q_k\le k
\]

implies Theorem 22's sufficient cascade inequality. Indeed \(q_k\ge1\), so

\[
(2^{s+1}-1)q_k+2^{s+1}-2s-2
\le (2^{s+2}-1)q_k-2s-2
< k+1.
\]

Thus the next \(s\) digits are up-steps.

### Counting and endpoint loss

The forced blocks following distinct down-steps are disjoint: a second
down-step cannot lie inside a block consisting entirely of forced
up-steps. On a finite interval, only the last such block can cross the
right endpoint, losing at most \(s\) charged up-steps. Hence

\[
P_s\ge sD_s-s,\qquad
D_s\le\frac{C_s+s}{s+1}.
\]

Theorem 24 gives \(q_n\to\infty\), while
\(\lvert q_n-q_{N_s}\rvert\le C_s(n)\), so \(C_s(n)\to\infty\). For each
fixed \(s\),

\[
\limsup\frac{D(n)}{C(n)}\le\frac1{s+1}.
\]

The initial-prefix correction is fixed and disappears because
\(C_s(n)\to\infty\). Only after taking this tail limit is \(s\) allowed to
grow. This proves \(D/C\to0\) with the quantifiers in the required order.

### Remaining limits and explicit spacing

The exact identity

\[
q_n-q_{n_0}=P(n)-D(n)=C(n)-2D(n)
\]

then gives \(q_n/C(n)\to1\). Combining this with \(q_n=o(n)\) proves
\(C(n)/n\to0\), and the other density statements follow directly.
Theorem 56's lower limit transfers through the factors
\(C/q_n\to1\) and \(P/C\to1\).

At a late down-step, taking

\[
s=\left\lfloor\log_2(k/q_k)\right\rfloor-2
\]

is valid once \(k\ge16q_k\), and gives the stated next-down spacing
\(s+1=\lfloor\log_2(k/q_k)\rfloor-1\). Since \(q_k/k\to0\), these
individual spacings diverge.

**Finding:** no defect found in Theorem 58. Its fixed-\(s\) tail argument,
prefix removal, endpoint loss, count-ratio conversion, and explicit spacing
bound are valid.

## Lemma 63

The segment begins with \(e>0\), ends at a down-step with \(e<0\), and
contains no earlier down-step. Zero digits only double \(e\), so at least
one up-step changes its sign. After \(e<0\), another up-step is impossible
because \(q+2e<q\le n<n+1\). The unique sign-changing up-step is therefore
the last up-step.

Writing \(Q=q_{t+1}\) and \(e_{t+1}=-v\), the up threshold gives
\(1\le v\le Q\). Each following zero digit keeps the quotient \(Q\) and
doubles the negative coordinate. With \(z\) such zeros, the last zero and
first down thresholds are exactly

\[
2^zv\le Q<2^{z+1}v.
\]

At the terminal pre-down state,

\[
r=Q-2^zv,\qquad
q-2r=2^{z+1}v-Q\in[1,Q].
\]

The research and compact proofs now say explicitly that this ridge
parameter is evaluated at the terminal pre-down state.

**Finding:** no mathematical defect found in Lemma 63. One sentence was
clarified to distinguish the unique sign-changing up-step from possible
earlier up-steps that remain in the positive half-window.

## Independent bounded checks

Fresh local runs produced:

- 2,138 parameterized rebound cascades;
- 185,232 explicit rebound-length states;
- 112,033 low-window counting prefixes;
- 2,210 terminal ridge segments;
- 1,899 terminal negative zero digits.

Both raw-transition verifiers passed. They import no project dynamics code.

## Effect on Theorem 77

The Opus cut audit had already checked Theorem 77's dichotomy and limiting
algebra, conditional only on Theorem 58 and Lemma 63. This continuation
closes that stated dependency gap. Theorem 77 remains an exhaustive
restriction, not a termination theorem, and all three results still await
external mathematical review.

The next unresolved audit target from the Opus report is the fully
quantified asymptotic chain Corollary 89--Theorem 90.
