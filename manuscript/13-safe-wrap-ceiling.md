# Safe-map wrap-block ceiling

This section sharpens the local complexity bound in the eventually-no-down
branch. It does not prove termination of the safe map.

## Lemma 80 (wrap-block state window)

At a zero epoch retain \(n=W+U\) and \(A=U+d+4\). If the maximal following
wrap run has length \(k\ge1\), whether it returns or terminates, then

\[
2^k(U+4)<n+k+4,\qquad 2^kU<n. \tag{13.1}
\]

### Proof

Lemma 53 makes \(k\) the least \(j\ge0\) satisfying
\(2^{j+1}A\ge n+j+5\). Minimality at \(j=k-1\) and \(A\ge U+4\) give
the first inequality. Since \(2^{k+2}\ge k+4\) for \(k\ge1\),

\[
2^kU<n+k+4-2^{k+2}\le n.
\]

\(\square\)

## Corollary 81 (double-logarithmic wrap ceiling)

Let an infinite quotient-zero safe path begin at index \(N\). At a zero epoch
of index \(n\), let \(k\ge1\) be the following wrap-run length and put
\(L=\lfloor\log_2n\rfloor\). If \(n>N+L\), then

\[
k<
\log_2\!\left(\frac{n(L+1)}{n-N-L}\right). \tag{13.2}
\]

Consequently

\[
k\le\log_2\log_2n+o(1). \tag{13.3}
\]

### Proof

Theorem 45 gives \(U\ge(n-N-L)/(L+1)\). Combine this with
\(2^kU<n\) from Lemma 80 and take base-two logarithms. Since
\[
\frac n{n-N-L}\longrightarrow1,\qquad
L+1\sim\log_2n,
\]
the asymptotic statement follows. \(\square\)

## Corollary 82 (positive-block recurrence)

Let \(B(n)\) count the completed positive wrap blocks before a zero epoch
of index \(n\) on an infinite quotient-zero safe path. Then

\[
\liminf_{n\to\infty}
\frac{B(n)\log_2n\log_2\log_2n}{n}\ge1. \tag{13.4}
\]

### Proof

For every \(\varepsilon>0\), Corollary 81 bounds every sufficiently late
block ending by \(n\) by \((1+\varepsilon)\log_2\log_2n\). Thus

\[
U_n\le O(1)+(1+\varepsilon)B(n)\log_2\log_2n.
\]

Theorem 45 gives \(U_n\ge(1-\varepsilon)n/\log_2n\) for all sufficiently
large zero epochs. Combine the bounds, pass to the lower limit, and let
\(\varepsilon\downarrow0\). \(\square\)

The results improve the elementary logarithmic wrap-run bound and force
quantitative recurrence of positive blocks, but still allow bounded or
slowly growing aperiodic block sequences.
