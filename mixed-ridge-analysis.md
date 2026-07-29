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

## Lemma 76: exact terminal dyadic ladder

In a mixed ridge, let \(L=N+\ell\) be the digit index of the final
positive-prefix zero and put \(x=e_L\). The following \(R\) digits are
up-steps, and the last one creates \(e=-v\). Then

\[
\boxed{\displaystyle
2^R(L+4-2x)=L+R+4+v.} \tag{76.1}
\]

More precisely, for \(0\le j\le R\),

\[
\begin{aligned}
A_{L+1+j}&=2^j(L+4-2x),\\
e_{L+1+j}&=L+j+4-2^j(L+4-2x).
\end{aligned} \tag{76.2}
\]

### Proof

The zero-step at \(L\) gives \(e_{L+1}=2x\), hence

\[
A_{L+1}=L+4-2x.
\]

Every one of the next \(R\) digits is an up-step, so the coordinate \(A\)
doubles at each step. This proves (76.2). At \(j=R\), the state index is
\(L+R+1\) and its defect is \(-v\), so

\[
A_{L+R+1}=L+R+4+v.
\]

Comparing with (76.2) proves (76.1). \(\square\)

## Theorem 77: terminal-run dichotomy in the sublinear branch

Suppose a counterexample has \(q_n=o(n)\) and infinitely many down-steps.
Index its sufficiently late ridges by \(j\), and let \(R_j\) be the
terminal positive up-run from Lemma 73. Exactly one of the following holds.

1. \(R_j\to\infty\). Then
   \(\rho_j=\min(R_j,R_{j+1})\to\infty\), and Theorem 75 forces

   \[
   \max\{z_j,P_{j+1}+1,v_j,v_{j+1}\}
   \ge2^{\rho_j-2}
   \]

   for infinitely many \(j\).

2. There is a fixed \(R\ge1\) and infinitely many mixed ridges with
   \(R_j=R\). If \(L_j\) is the final positive-zero index and
   \(x_j=e_{L_j}\), then

   \[
   \frac{x_j}{L_j}\longrightarrow
   \frac{2^R-1}{2^{R+1}},\qquad
   \frac{v_j}{L_j}\longrightarrow0. \tag{77.1}
   \]

   At every level \(0\le h\le R\) of the following zero/up ladder,

   \[
   \frac{e_{L_j+1+h}}{L_j+1+h}
   \longrightarrow 1-2^{h-R}. \tag{77.2}
   \]

Thus failure of terminal-run growth forces infinitely many visits to one
fixed dyadic boundary ladder, ending at asymptotically zero negative
defect.

### Proof

If \(R_j\) does not tend to infinity, some bounded set contains infinitely
many values; one fixed \(R\) therefore occurs infinitely often.

Theorem 58 makes the initial up-run of every sufficiently late ridge tend
to infinity. A pure ridge has \(R_j=P_j\), at least its initial up-run.
Consequently the fixed-\(R\) subsequence is eventually mixed, so Lemma 76
applies.

Let \(s_j=q_{L_j}\). The quotient after the \(R\) terminal up-steps is
\(s_j+R\), and Lemma 63 gives

\[
1\le v_j\le s_j+R.
\]

Because \(q_n=o(n)\) and \(R\) is fixed, \(v_j/L_j\to0\). Rearranging
(76.1) gives

\[
2^{R+1}x_j
=(2^R-1)L_j+4\cdot2^R-R-4-v_j,
\]

which proves (77.1). Finally substitute (76.1) into (76.2) and divide by
\(L_j+1+h\). The fixed offsets and \(v_j/L_j\) vanish, yielding (77.2).
The first alternative is exactly Theorem 75 with
\(\rho_j\to\infty\). \(\square\)

## Remaining boundary

Theorem 77 is exhaustive but not a termination proof. In its second branch
the orbit may return aperiodically to the same finite dyadic ladder; the
all-period exclusion does not forbid recurrent visits to a boundary
without eventual periodicity. A closing argument must now rule out either
these repeated boundary shadows or the exponential complexity in the first
branch.
