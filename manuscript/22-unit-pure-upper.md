# Unit pure-upper chains

## Lemma 116 (quotient erasure)

If a safe path begins at \((n_0,U_0,e_0)\), then the state
\((n_0,0,e_0)\) generates the same zero/wrap word, with the same indices
and residues and with every wrap count lowered by \(U_0\). Hence every
pure-upper gate word has a quotient-zero realization.

### Proof

A zero digit satisfies \(2e\le n-U\), which remains true after lowering
\(U\). A wrap digit satisfies \(2e>n+2\), independently of \(U\), and its
lowered width is at most \(n\), so it remains a wrap. Induction gives the
claim. Gate defects increase by \(U_0\), so pure-upper headroom is
preserved. \(\square\)

## Lemma 117 (unit-block state test)

Let \(n\ge2\) and \(U\ge0\) be integers, and put \(D=n-2U\). A returning
unit positive block with returned residue \(f\) exists exactly when

\[
n+3+f\equiv0\pmod4,\qquad
f\ge1,\qquad f\le D-3,\qquad4f\le n+D+2.
\tag{22.1}
\]

Its start residue and defect are

\[
e=\frac{n+3+f}{4},\qquad d=\frac{D-3-f}{2}.
\tag{22.2}
\]

### Proof

The first zero is \(2e\le n-U\). The following single wrap returns
\(f=4e-n-3>0\), and the next zero test is \(2f\le n+1-U\).
Rearranging gives (22.1)--(22.2), and each step is reversible. \(\square\)

## Theorem 118 (two-gap critical scale)

On a hypothetical infinite all-unit pure-upper tail,

\[
n_i<2^{r_{i-1}+r_i+6}\qquad(i\ge1).
\tag{22.3}
\]

Moreover,

\[
\frac12\le
\liminf\frac{n_J}{J\log_2J}
\le
\limsup\frac{n_J}{J\log_2J}
\le1,
\tag{22.4}
\]

and

\[
1\le
\liminf\frac{U_J\log_2n_J}{n_J}
\le
\limsup\frac{U_J\log_2n_J}{n_J}
\le2.
\tag{22.5}
\]

### Proof

The preceding pure-upper gate gives
\(f_i\le2^{r_{i-1}+4}\). The unit recurrence gives

\[
n_i=2^{r_i+2}f_i-f_{i+1}-r_i-5<2^{r_i+2}f_i,
\]

proving (22.3).

Let \(S_J=\sum_{i<J}r_i\). Since
\(n_J=n_0+2J+S_J\), summing logarithms of (22.3) gives

\[
2S_J>
\sum_{i=1}^{J-1}\log_2n_i-O(J)
\ge J\log_2J-O(J).
\]

Thus \(n_J\ge\frac12J\log_2J-O(J)\).

Conversely, the pure-upper scale ceiling gives
\(2^{r_i+4}<n_{i+1}\), so
\(S_J\le J\log_2n_J-4J\). Hence

\[
n_J\le J\log_2n_J+O(J)
\le J\log_2J+O(J\log_2\log_2J).
\]

For completeness, writing \(y_J=n_J/J\), the first inequality is
\(y_J\le\log_2J+\log_2y_J+O(1)\). Since
\(\log_2y_J\le y_J/2\) for \(y_J\ge4\), this first gives
\(y_J=O(\log J)\), and substitution gives the displayed second inequality.
This proves (22.4). Since \(U_J/J\to1\) and
\(\log n_J/\log J\to1\), taking reciprocals in (22.4) gives (22.5).
\(\square\)

The theorem forces a critical scale but does not exclude an aperiodic
all-unit pure-upper tail.
