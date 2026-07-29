# Exact compatibility of arbitrary mixed ridges

At a post-down start \(N\), put

\[
Q=q_N,\qquad h=N-Q-e_N,\qquad A=Q+h+3.
\]

Suppose the next down-step is preceded by at least one up-step. Let \(P\)
be the length of the prefix through its last up-step, let
\(\mathcal Z^+\subseteq\{0,\ldots,P-1\}\) contain the zero-digit offsets
in that prefix, and let the last up-step create \(e=-v\). Write \(z\) for
the number of terminal negative zero-digits and \(S\) for the quotient
after the last up-step. Define

\[
W=\sum_{i\in\mathcal Z^+}(N+i+2)2^{P-1-i}. \tag{11.1}
\]

If the prefix is mixed, let \(R\) be the number of final consecutive
up-digits after its last zero; for a pure prefix put \(R=P\).

## Lemma 73 (mixed-ridge defect map)

Every such ridge satisfies

\[
2^PA-W=N+P+3+v,\qquad
z=\left\lfloor\log_2\frac Sv\right\rfloor. \tag{11.2}
\]

At the next post-down start,

\[
N'=N+P+z+1,\quad Q'=S-1,\quad
h'=2^{z+1}v-S,\quad A'=2^{z+1}v+2. \tag{11.3}
\]

If the next ridge has parameters \(P',W',v'\), then

\[
2^PA-W+z+P'+1+v'-v=2^{P'}A'-W'. \tag{11.4}
\]

Also \(2^R\mid W\). If \(\ell\) is the last positive zero offset, then

\[
\frac{W}{2^R}\equiv N+\ell+2\pmod2. \tag{11.5}
\]

For \(A_n=n+3-e_n\), Theorem 6 gives

\[
A_{n+1}=2A_n
\quad(a_n=1),\qquad
A_{n+1}=2A_n-(n+2)
\quad(a_n=0).
\]

Iteration over the positive prefix proves the first identity in (11.2).
The terminal negative defect doubles until it crosses the quotient,
proving the second identity and (11.3). Equating the two formulas for
\(N'\) proves (11.4). In (11.1), the final zero contributes the lowest
power, \(2^R\), and every earlier zero contributes a higher power. This
proves the divisibility and parity statements. \(\square\)

## Corollary 74 (terminal-run congruence)

For adjacent ridges, with \(\rho=\min(R,R')\),

\[
2^\rho\mid z+P'+1+v'-v. \tag{11.6}
\]

If \(z+P'+1+v+v'<2^\rho\), then

\[
v'=v-z-P'-1\le v-2. \tag{11.7}
\]

Indeed, \(R\le P\), \(R'\le P'\), and Lemma 73 makes every other term
in (11.4) divisible by \(2^\rho\). Below the modulus the representative
must vanish. \(\square\)

## Theorem 75 (complexity alternative for arbitrary ridges)

In any infinite ridge chain, put
\(\rho_j=\min(R_j,R_{j+1})\). Infinitely often,

\[
\max\{z_j,P_{j+1}+1,v_j,v_{j+1}\}\ge2^{\rho_j-2}. \tag{11.8}
\]

For

\[
E_j=z_j+P_{j+1}+1+v_{j+1}-v_j,
\]

Corollary 74 gives \(2^{\rho_j}\mid E_j\). The equality \(E_j=0\)
cannot hold eventually, since it would decrease the positive integer
\(v_j\) by at least two at every step. Thus \(E_j\ne0\) infinitely often,
and bounding its absolute value by the sum of the four displayed
nonnegative terms proves (11.8). \(\square\)

The theorem is informative only when the terminal positive up-runs grow.
Theorem 58 forces the initial rebound to grow in a sublinear
counterexample, not the terminal run. Hence the infinitely-many-down-steps
branch remains open.
