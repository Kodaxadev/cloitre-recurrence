# Terminal structure of a post-down ridge segment

This note continues Corollary 61 and Lemma 62. It classifies the final
sign change before the next quotient down-step and isolates a second
necessary feature of a sublinear infinite-down counterexample.

## Lemma 63: terminal negative-suffix map

After entry, consider a finite digit interval beginning at a state with
\(e>0\), containing only zero- and up-steps, and ending immediately before
a down-step. Suppose the interval contains at least one up-step. Let \(t\)
be the index of its last up-step and put

\[
Q=q_{t+1},\qquad v=-e_{t+1}.
\]

Then \(v\) is a positive integer with

\[
1\le v\le Q. \tag{63.1}
\]

If \(z\) is the number of zero digits after that up-step and before the
down-step, then

\[
e_{t+1+j}=-2^jv\qquad(0\le j\le z), \tag{63.2}
\]

\[
2^zv\le Q<2^{z+1}v,\qquad
z=\left\lfloor\log_2\frac Qv\right\rfloor. \tag{63.3}
\]

At the terminal pre-down state, if

\[
h_{\mathrm{next}}=q-2r,
\]

then

\[
\boxed{\displaystyle
h_{\mathrm{next}}=2^{z+1}v-Q,\qquad
1\le h_{\mathrm{next}}\le Q.} \tag{63.4}
\]

Thus the last up-step and its negative zero suffix form an exact dyadic
remainder map from \((Q,v)\) to the next post-down ridge parameter.

### Proof

The interval starts with positive \(e\), while a down-step requires

\[
q+2e<0
\]

and hence negative \(e\). A zero-step doubles \(e\) and cannot change its
sign. Therefore at least one up-step changes the sign. Once \(e<0\),
another up-step is impossible because \(q+2e<q\le n<n+1\). Thus the
sign-changing up-step is unique and is the last up-step.

At index \(t\),

\[
e_{t+1}=2e_t-(t+2)=-v.
\]

The up threshold is \(q_t+2e_t\ge t+1\), which becomes
\(v\le q_t+1=Q\); negativity gives \(v\ge1\). Subsequent zero-steps leave
the quotient equal to \(Q\) and double the negative coordinate, proving
(63.2).

At a state with \(e=-2^jv\), the digit is zero exactly while

\[
Q-2^{j+1}v\ge0.
\]

The upper zero threshold is automatic because \(Q\le n\). The digit becomes
a down-step at \(j=z\). The last safe state and the terminal failure
therefore give (63.3). At that terminal pre-down state,

\[
r=Q-2^zv,
\]

so

\[
h_{\mathrm{next}}
=Q-2r=2^{z+1}v-Q.
\]

The two inequalities in (63.3) give the bounds in (63.4). \(\square\)

## Corollary 64: unbounded zero plateaus

In a sublinear counterexample with infinitely many down-steps, use the
subsequence of post-down segments from Corollary 61. Let \(M_j\) be the
longest run of consecutive zero digits in the \(j\)-th segment. Then

\[
M_j\longrightarrow\infty \tag{64.1}
\]

along a further subsequence.

More quantitatively, if the segment has length \(L_j\) and \(U_j\) up-steps,
then

\[
M_j\ge\frac{L_j-U_j}{U_j+1}. \tag{64.2}
\]

At the beginning \(s\) of any such zero run of length \(M\),

\[
2^M|e_s|\le s+M. \tag{64.3}
\]

### Proof

The \(L_j-U_j\) zero digits form at most \(U_j+1\) runs, proving (64.2).
Corollary 61 gives \(U_j/L_j\to0\), while its forced rebound bound gives
\(U_j\to\infty\). Hence the right side of (64.2) tends to infinity.

Along a zero run, \(e_{s+M}=2^Me_s\). The state window after entry gives
\(|e_{s+M}|\le s+M\), proving (64.3). \(\square\)

## Remaining obstruction

Lemma 63 completely determines the negative suffix, but the long zero
plateau supplied by Corollary 64 may occur earlier while \(e>0\). A
contradiction still requires controlling how a small positive integer
created after an up-step can survive long enough to feed the next ridge.

## Lemma 65: nonnegative defect coding at down epochs

At any down-step index \(d\), put

\[
h_d=q_d-2r_d,\qquad B_d=q_d+h_d+2=2-2e_d.
\]

Then the entire future digit tail satisfies

\[
\boxed{\displaystyle
B_d=
\sum_{k=d+1}^{\infty}
\frac{(1-a_k)(k+2)}{2^{k-d}}.} \tag{65.1}
\]

Every summand is nonnegative: an up-step contributes zero, a zero-step
contributes one copy of its weight, and a later down-step contributes two.

If \(d<d'\) are consecutive down-step indices and

\[
\mathcal Z(d,d')=\{k:d<k<d',\ a_k=0\},
\]

then

\[
B_d=
\sum_{k\in\mathcal Z(d,d')}
\frac{k+2}{2^{k-d}}
+\frac{2(d'+2)+B_{d'}}{2^{d'-d}}. \tag{65.2}
\]

For an infinite sequence \(d_1<d_2<\cdots\) of down-steps, iteration gives

\[
\frac{B_{d_j}}{2^{d_j}}
=
\sum_{\substack{k>d_j\\a_k=0}}\frac{k+2}{2^k}
+2\sum_{\ell>j}\frac{d_\ell+2}{2^{d_\ell}}. \tag{65.3}
\]

Thus the post-down zero budgets and terminal remainder maps are consecutive
pieces of one globally nonnegative dyadic expansion.

### Proof

The future-digit identity at a down-step, where \(a_d=-1\), gives

\[
2e_d=-(d+2)+
\sum_{k=d+1}^{\infty}\frac{a_k(k+2)}{2^{k-d}}.
\]

The all-up tail has the closed form

\[
\sum_{k=d+1}^{\infty}\frac{k+2}{2^{k-d}}=d+4.
\]

Subtracting the actual tail from the all-up tail yields

\[
\sum_{k=d+1}^{\infty}
\frac{(1-a_k)(k+2)}{2^{k-d}}
=2-2e_d.
\]

Since \(h_d=q_d-2r_d\) and \(e_d=r_d-q_d\), the right side is
\(q_d+h_d+2=B_d\), proving (65.1).

Split (65.1) at the next down-step. Between \(d\) and \(d'\), only zero
digits contribute. The digit at \(d'\) contributes twice, and the remaining
tail is \(2^{-(d'-d)}B_{d'}\), proving (65.2). Iteration and positivity
allow passage to the limit; \(B_{d_\ell}=O(d_\ell)\) makes the terminal
remainder vanish. Dividing by \(2^{d_j}\) gives (65.3). \(\square\)

## Proposition 66: exact arbitrarily diluted ridge segments

The local positive-density route suggested after Corollary 61 is false for
valid states. More precisely, let \(K\ge1\), let \(Q\ge2\), and choose an
integer \(h\) such that

\[
1\le h\le Q+1,\qquad h\equiv Q+1\pmod2.
\]

Put

\[
A=Q+h+3,\qquad N=2^KA-K-4,
\]

and consider the state at index \(N-1\)

\[
\left(q_{N-1},r_{N-1}\right)
=\left(Q+1,\frac{Q+1-h}{2}\right). \tag{66.1}
\]

This is a valid down-step. If

\[
z=\left\lfloor\log_2(Q+K)\right\rfloor,
\]

then the complete digit word from this down-step through the next one is

\[
\boxed{\displaystyle -1,\;1^K,\;0^z,\;-1.} \tag{66.2}
\]

Thus the \(L=K+z\) intervening digits have exactly \(U=K\) up-steps.
In particular, take

\[
Q_K=2^{K^2},\qquad h=3.
\]

Then \(z=K^2\), so

\[
L_K=K+K^2,\qquad
\frac{U_K}{L_K}=\frac1{K+1}\longrightarrow0. \tag{66.3}
\]

Moreover \(Q_K/N_K\sim2^{-K}\to0\), while the initial up-run length
\(K\to\infty\). Hence all three local features demanded by Corollary 61
-- a sublinear quotient ratio, a diverging rebound, and a vanishing up-step
fraction -- are simultaneously compatible with exact finite dynamics.

### Proof

At (66.1),

\[
2r_{N-1}-q_{N-1}=-h,
\]

and \(0<h<N\), so the digit is \(-1\). Its image at index \(N\) has

\[
q_N=Q,\qquad r_N=N-h,\qquad e_N=N-Q-h=N+3-A.
\]

The parity assumption makes \(r_{N-1}\) integral, while
\(1\le h\le Q+1\) gives \(r_{N-1}\ge0\). Also
\(Q+1\le N-1\), so both the parent and its image lie in the valid
post-entry state window.

If the following digits are up-steps, induction in the exact doubling
coordinate gives, for \(0\le j\le K\),

\[
e_{N+j}=N+j+3-2^jA
       =(2^K-2^j)A+j-K-1. \tag{66.4}
\]

For \(j<K\), the candidate coordinate after the next up-step is

\[
\widetilde e_{N+j+1}
=(2^K-2^{j+1})A+j-K.
\]

It is positive when \(j<K-1\), and it equals \(-1\) when \(j=K-1\).
In either case it is at least \(-q_{N+j+1}\), which is exactly the lower
threshold for an up-step. Therefore all \(K\) up-steps occur, and

\[
q_{N+K}=Q+K,\qquad e_{N+K}=-1. \tag{66.5}
\]

From (66.5), a zero-step doubles the negative coordinate while leaving the
quotient fixed. At the state with \(e=-2^\ell\), the lower zero threshold
is

\[
Q+K-2^{\ell+1}\ge0.
\]

It holds for \(0\le\ell<z\) and fails at \(\ell=z\). This proves (66.2).

For \(Q_K=2^{K^2}\), one has
\(Q_K\le Q_K+K<2Q_K\), hence \(z=K^2\). Formula (66.3) follows, and

\[
N_K=2^K(Q_K+6)-K-4\sim2^KQ_K
\]

gives both \(Q_K/N_K\to0\) and
\((Q_K+1)/(N_K-1)\to0\). The logarithmic forced-rebound lower bound at
the parent is asymptotic to \(K\). \(\square\)

## Consequence and limitation

Proposition 66 rules out any proof of the sublinear infinite-down branch
based only on a uniform positive lower bound for the up-step density of
all valid post-down segments. It does **not** construct a nonstabilizing
orbit: the parent states (66.1) are valid local states, but no claim is made
that one original start reaches infinitely many of them. Theorem 69 proves
that this exact unit-terminal mechanism cannot occur on three consecutive
ridge segments; more general concatenations remain open.
