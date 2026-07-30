# Fixed-word rigidity and sparse unit renewals

## Scope

Theorem 121 leaves open infinitely many returns to a fixed pair
\((R,a)\), where \(R\) is a bounded gap and \(a\) is the residue returned
by the next unit block. Theorem 122 excludes only strict alternation.

This note proves a global restriction on arbitrary return spacings. A fixed
gap word and its two endpoint residues determine at most one starting index.
Consequently, successive returns to one fixed pair must use distinct words.
The critical-scale bounds then force those returns to have zero density among
the unit blocks.

The conclusion is still compatible with infinitely many irregular returns.

## Lemma 123 (fixed unit-word endpoint rigidity)

Consider \(p+1\) consecutive unit positive blocks, where \(p\ge1\), with
start indices \(n_0,\ldots,n_p\), returned residues
\(f_0,\ldots,f_p\), and gaps \(r_0,\ldots,r_{p-1}\). Put

\[
s_0=0,\qquad s_{t+1}=s_t+r_t+2. \tag{123.1}
\]

For the fixed gap word, define

\[
\begin{aligned}
P_0&=1,&B_0&=0,&C_0&=0,\\
P_{t+1}&=2^{r_t+2}P_t,&
B_{t+1}&=2^{r_t+2}B_t+1,&
C_{t+1}&=2^{r_t+2}C_t+s_t+r_t+5.
\end{aligned} \tag{123.2}
\]

Then

\[
\boxed{
n_t=n_0+s_t,\qquad
f_t=P_tf_0-B_tn_0-C_t
} \tag{123.3}
\]

for \(0\le t\le p\). In particular, \(B_p>0\), and prescribed endpoint
residues \(f_0=a\), \(f_p=b\) force

\[
\boxed{
n_0=\frac{P_pa-C_p-b}{B_p}.
} \tag{123.4}
\]

Thus a fixed nonempty gap word and two fixed endpoint residues occur from
at most one integer start index.

### Proof

Corollary 114 gives

\[
n_{t+1}=n_t+r_t+2,\qquad
f_{t+1}=2^{r_t+2}f_t-n_t-r_t-5. \tag{123.5}
\]

The first recurrence and (123.1) give \(n_t=n_0+s_t\).
Equation (123.3) holds at \(t=0\). If it holds at \(t\), substitution into
(123.5) gives

\[
\begin{aligned}
f_{t+1}
&=2^{r_t+2}(P_tf_0-B_tn_0-C_t)
  -(n_0+s_t)-r_t-5\\
&=P_{t+1}f_0-B_{t+1}n_0-C_{t+1},
\end{aligned}
\]

which is the induction step. Since \(p\ge1\),
\(B_1=1\), and (123.2) keeps \(B_t\) positive thereafter.
Setting \(t=p\), \(f_0=a\), and \(f_p=b\) proves (123.4) and the
uniqueness claim. \(\square\)

## Corollary 124 (fixed-ladder renewals have zero block density)

Suppose a hypothetical infinite safe tail consists entirely of unit positive
blocks and every gate is pure-upper. Fix integers \(R\ge0\) and \(a\ge1\),
and let

\[
M_{R,a}(J)
=
\#\{\,1\le i\le J:r_{i-1}=R,\ f_i=a\,\}. \tag{124.1}
\]

Then

\[
\boxed{
\limsup_{J\to\infty}
\frac{M_{R,a}(J)\log_2J}
     {J\log_2\log_2J}
\le1.
} \tag{124.2}
\]

In particular,

\[
\boxed{M_{R,a}(J)=o(J).} \tag{124.3}
\]

Hence every fixed pair supplied by Theorem 121 can recur only on a
zero-density set of unit-block indices.

### Proof

List the indices counted by (124.1) as

\[
i_1<i_2<\cdots<i_M
\]

If \(M_{R,a}(J)\) remains bounded, both conclusions are immediate.
Otherwise consider sufficiently large \(J\) for which \(M\ge2\), and put
\(K=M-1\). The \(h\)-th interval has length
\(p_h=i_{h+1}-i_h\) and gap word

\[
w_h=(r_{i_h},\ldots,r_{i_{h+1}-1}).
\]

Both endpoint residues of every \(w_h\) equal \(a\). If two interval words
were equal, Lemma 123 would force their start indices \(n_{i_h}\) to be
equal. But \(n_i\) is strictly increasing. Therefore

\[
\boxed{w_1,\ldots,w_K\text{ are pairwise distinct}.} \tag{124.4}
\]

Let

\[
A_J=1+\max_{0\le i<J}r_i.
\]

Corollary 115 and monotonicity of the start indices give

\[
2^{r_i+4}<n_{i+1}\le n_J.
\]

Theorem 118 gives \(n_J\le(1+o(1))J\log_2J\). Consequently

\[
A_J=O(\log J),\qquad
\log_2A_J\le(1+o(1))\log_2\log_2J. \tag{124.5}
\]

The same theorem forces the prefix maximum of the gaps to diverge, so
\(A_J\ge2\) for all sufficiently large \(J\).

The interval lengths satisfy \(\sum_{h=1}^Kp_h\le J\). Fix
\(\lambda>1\). Fewer than \(K/\lambda\) intervals can have length larger
than

\[
P_{\lambda,J}:=\left\lceil\frac{\lambda J}{K}\right\rceil, \tag{124.6}
\]

because their lengths would otherwise sum to more than \(J\). There are
fewer than \(A_J^{P_{\lambda,J}+1}\) nonempty words of length at most
\(P_{\lambda,J}\) over an alphabet of size \(A_J\). Pairwise distinctness
therefore gives

\[
\left(1-\frac1\lambda\right)K
\le A_J^{P_{\lambda,J}+1}. \tag{124.7}
\]

First take \(\lambda=2\). Equation (124.7) forces \(K/J\to0\).
Otherwise \(K\ge\varepsilon J\) on a subsequence,
\(P_{2,J}\) would be bounded there, and the right side would be a fixed
power of \(O(\log J)\), contradicting \(K/2\ge\varepsilon J/2\).

Return to an arbitrary fixed \(\lambda>1\). Taking base-two logarithms in
(124.7), using \(P_{\lambda,J}\le\lambda J/K+1\), and then (124.5), gives

\[
\frac KJ
\left(
\log_2K+\log_2\left(1-\frac1\lambda\right)
\right)
\le
\left(\lambda+\frac{2K}{J}\right)\log_2A_J
\le(\lambda+o(1))\log_2\log_2J. \tag{124.8}
\]

On any subsequence where the left side of (124.2) has a positive lower
bound,

\[
K\gg\frac{J\log\log J}{\log J},
\]

so the logarithmic factor on the left of (124.8), divided by
\(\log_2J\), tends to one. Thus the limsup for \(K\) is at most
\(\lambda\). Since every fixed \(\lambda>1\) is allowed, it is at most
one. Replacing \(K=M-1\) by \(M\) changes the normalized quantity by
\(o(1)\), proving (124.2). Equation (124.3) follows either from (124.2)
or directly from the first consequence of (124.7). \(\square\)

## Consequence and limitation

The fixed-ladder branch of Theorem 121 is no longer an unrestricted
infinite recurrence. Each return must carry a new gap word, and any fixed
ladder pair appears at most

\[
(1+o(1))\frac{J\log_2\log_2J}{\log_2J}
\]

times among the first \(J\) gates.

This does not exclude a sparse aperiodic renewal sequence, and it does not
touch the growing-modulus branch. Lemma 125 carries out the next arithmetic
step by combining endpoint rigidity with the dyadic renewal congruence.
Proposition 126 then shows why this alone cannot close the branch:
arbitrarily long literal two-renewal segments survive. The remaining target
is compatibility between successive distinct return words.
