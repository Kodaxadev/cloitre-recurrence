# Exact compatibility of mixed ridges

The pure-ridge law in Lemma 70 omits the main surviving local behavior:
zero-steps may be interspersed throughout the positive part of a segment.
This note encodes every such zero in one exact integer defect. The result
extends the adjacent dyadic congruence to arbitrary ridges, but its modulus
is controlled by the final positive up-run, not by the long rebound at the
start of the ridge.

## Definitions

Consider a post-down start at index \(N\), with

\[
Q=q_N,\qquad h=N-Q-e_N,\qquad A=Q+h+3=N+3-e_N.
\]

Assume that the segment reaches a later down-step and contains an up-step.
Let \(P\) be the length of the digit prefix from index \(N\) through the
last up-step, inclusive. Let

\[
\mathcal Z^+\subseteq\{0,\ldots,P-1\}
\]

be the offsets of the zero-digits in this prefix, and let \(U\) be its
number of up-digits. The last up-step leaves

\[
e_{N+P}=-v,\qquad v\ge1,
\]

and the quotient there is \(S=Q+U\). It is followed by \(z\) zero-digits
and then the terminating down-step.

Define the positive-prefix defect

\[
\boxed{\displaystyle
W=\sum_{i\in\mathcal Z^+}(N+i+2)2^{P-1-i}.} \tag{73.1}
\]

If \(\mathcal Z^+\ne\varnothing\), let
\(\ell=\max\mathcal Z^+\) and put

\[
R=P-1-\ell.
\]

Thus \(R\) is the number of consecutive up-digits after the final positive
zero, including the sign-changing last up. For a pure prefix
\(\mathcal Z^+=\varnothing\), put \(R=P\).

## Lemma 73: mixed-ridge defect map

Every ridge above satisfies

\[
\boxed{\displaystyle
2^PA-W=N+P+3+v,} \tag{73.2}
\]

or equivalently

\[
N=2^PA-W-P-3-v. \tag{73.3}
\]

Moreover,

\[
z=\left\lfloor\log_2\frac Sv\right\rfloor. \tag{73.4}
\]

At the next post-down start,

\[
\begin{aligned}
N'&=N+P+z+1,\\
Q'&=S-1,\\
h'&=2^{z+1}v-S,\\
A'=Q'+h'+3&=2^{z+1}v+2.
\end{aligned} \tag{73.5}
\]

If the next ridge has parameters \(P',W',v'\), then

\[
\boxed{\displaystyle
2^PA-W+z+P'+1+v'-v=2^{P'}A'-W'.} \tag{73.6}
\]

Finally,

\[
2^R\mid W. \tag{73.7}
\]

In the mixed case,

\[
\frac{W}{2^R}\equiv N+\ell+2\pmod2. \tag{73.8}
\]

### Proof

For the auxiliary coordinate \(A_n=n+3-e_n\), Theorem 6 gives, on a
prefix containing only up- and zero-steps,

\[
A_{n+1}=
\begin{cases}
2A_n,&a_n=1,\\
2A_n-(n+2),&a_n=0.
\end{cases}
\]

Iterating across the \(P\)-digit positive prefix gives

\[
A_{N+P}=2^PA-
\sum_{i\in\mathcal Z^+}(N+i+2)2^{P-1-i}.
\]

Since \(e_{N+P}=-v\), the left side is \(N+P+3+v\). This proves
(73.2)--(73.3).

After the last up-step the quotient is \(S\), while the negative defect
successively equals \(-v,-2v,\ldots\). The digit remains zero exactly
while \(2^jv\le S\), and becomes a down-step when \(2^{j+1}v>S\).
This proves (73.4). Direct substitution in the down-step update gives
(73.5).

Combining (73.3) with the first identity in (73.5) gives

\[
N'=2^PA-W+z-2-v.
\]

Equating this with (73.3) for the next ridge proves (73.6).

If the prefix is pure, \(W=0\). Otherwise its final zero occurs at
\(\ell=P-R-1\), so its summand in (73.1) has exact power \(2^R\);
all earlier zero summands have at least one further factor of two.
This proves (73.7) and the parity identity (73.8). \(\square\)

## Corollary 74: terminal-run congruence

For adjacent arbitrary ridges put

\[
\rho=\min(R,R').
\]

Then

\[
\boxed{\displaystyle
2^\rho\mid z+P'+1+v'-v.} \tag{74.1}
\]

If

\[
z+P'+1+v+v'<2^\rho, \tag{74.2}
\]

then

\[
v'=v-z-P'-1\le v-2. \tag{74.3}
\]

### Proof

Because \(R\le P\) and \(R'\le P'\), every power term and both defects
in (73.6) are divisible by \(2^\rho\). This proves (74.1). Under (74.2),
the divisible integer in (74.1) has absolute value below its modulus, so
it vanishes. Since \(P'\ge1\), (74.3) follows. \(\square\)

## Theorem 75: arbitrary-ridge complexity alternative

For any infinite chain of ridges, put

\[
\rho_j=\min(R_j,R_{j+1}).
\]

For infinitely many \(j\),

\[
\boxed{\displaystyle
\max\{z_j,\ P_{j+1}+1,\ v_j,\ v_{j+1}\}
\ge2^{\rho_j-2}.} \tag{75.1}
\]

Consequently, if \(R_j\to\infty\), then infinitely many adjacent pairs
have a parameter exponentially large in the smaller terminal up-run.

### Proof

Let

\[
E_j=z_j+P_{j+1}+1+v_{j+1}-v_j.
\]

Corollary 74 gives \(2^{\rho_j}\mid E_j\). If \(E_j=0\) eventually, then

\[
v_{j+1}=v_j-z_j-P_{j+1}-1\le v_j-2
\]

eventually, impossible for positive integers. Hence \(E_j\ne0\)
infinitely often. At each such index,

\[
2^{\rho_j}\le |E_j|
\le z_j+(P_{j+1}+1)+v_j+v_{j+1}.
\]

One of the four nonnegative summands proves (75.1). \(\square\)

## Exact limitation

Theorem 58 forces the initial rebound after a late down-step to grow in the
sublinear branch. It does not force the *terminal* up-run \(R_j\) to grow.
Bounded raw states already contain valid prefixes of 100 consecutive ridges
with every \(R_j\le2\). Those prefixes are not known to be reachable from
\(b_1=m\), and they do not construct an infinite orbit, but they rule out
deducing terminal-run growth from short-range ridge compatibility alone.

Thus Lemma 73 removes the pure-word assumption exactly; it does not close
the infinitely-many-down-steps branch. The new unresolved question is
whether reachability and sublinear quotient growth constrain the low-order
mixed defects strongly enough to make \(\rho_j\) large, or provide a
different contradiction when it remains bounded.
