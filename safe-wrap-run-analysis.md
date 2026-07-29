# A log-log ceiling for safe-map wrap blocks

This note combines the accelerated zero-epoch map with the monotone-tail
growth theorem. It bounds every sufficiently late wrap block on a
hypothetical infinite safe path; it does not prove that the path terminates.

## Lemma 80: wrap-block state-window bound

At a zero epoch, retain the coordinates

\[
n=W+U,\qquad A=U+d+4
\]

from Lemma 53. Let \(k\ge1\) be the length of the maximal following wrap
run, whether the first non-wrap state returns to a zero epoch or terminates.
Then

\[
\boxed{2^k(U+4)<n+k+4} \tag{80.1}
\]

and, in particular,

\[
\boxed{2^kU<n.} \tag{80.2}
\]

### Proof

Lemma 53 characterizes \(k\) as the least \(j\ge0\) for which

\[
2^{j+1}A\ge n+j+5.
\]

Because \(k\ge1\), minimality at \(j=k-1\) gives

\[
2^kA<n+k+4.
\]

The zero-epoch bound \(A\ge U+4\) proves (80.1). For every \(k\ge1\),
\(2^{k+2}\ge k+4\). Subtracting \(2^{k+2}\) from (80.1) therefore gives

\[
2^kU<n+k+4-2^{k+2}\le n,
\]

which is (80.2). \(\square\)

## Corollary 81: double-logarithmic wrap ceiling

Suppose a quotient-zero safe path begins at index \(N\) and is infinite.
At a zero epoch of index \(n\), let \(k\ge1\) be the following wrap-run
length and put \(L=\lfloor\log_2n\rfloor\). Whenever \(n>N+L\),

\[
\boxed{
k<
\log_2\!\left(\frac{n(L+1)}{n-N-L}\right).
} \tag{81.1}
\]

In particular, if \(n\ge2(N+L)\), then

\[
k<1+\log_2(L+1), \tag{81.2}
\]

and along the zero epochs of any hypothetical infinite safe path,

\[
\boxed{k\le\log_2\log_2n+o(1).} \tag{81.3}
\]

### Proof

Theorem 45 applied from \(N\) to \(n\) gives

\[
U\ge\frac{n-N-L}{L+1}.
\]

The right side is positive under the stated hypothesis. Combining it with
Lemma 80 yields

\[
2^k<\frac nU
\le\frac{n(L+1)}{n-N-L},
\]

which proves (81.1). If \(n\ge2(N+L)\), the final fraction is at most
\(2(L+1)\), proving (81.2). Finally,

\[
\log_2\!\left(\frac n{n-N-L}\right)=o(1),
\qquad
\log_2(L+1)=\log_2\log_2n+o(1),
\]

which gives (81.3). \(\square\)

## Corollary 82: quantitative positive-block recurrence

On an infinite quotient-zero safe path, let \(B(n)\) be the number of
completed positive wrap blocks before a zero epoch of index \(n\). Then,
along the zero epochs,

\[
\boxed{
\liminf_{n\to\infty}
\frac{B(n)\log_2n\log_2\log_2n}{n}\ge1.
} \tag{82.1}
\]

### Proof

Fix \(\varepsilon>0\). Corollary 81 implies that every sufficiently late
positive block beginning at an index \(t\le n\) has length at most

\[
(1+\varepsilon)\log_2\log_2n.
\]

The finitely many earlier wraps contribute a constant \(C\). Since \(U_n\)
is the total number of wraps before the zero epoch,

\[
U_n\le C+(1+\varepsilon)B(n)\log_2\log_2n. \tag{82.2}
\]

Theorem 45 also gives, for every sufficiently large zero epoch,

\[
U_n\ge(1-\varepsilon)\frac n{\log_2n}. \tag{82.3}
\]

Combine (82.2)--(82.3), pass to the lower limit, and then let
\(\varepsilon\downarrow0\). \(\square\)

## Consequence and limitation

Lemma 44 alone gives only a logarithmic ceiling on a wrap run. Corollary 81
improves this to the double-logarithmic scale by using the quotient already
accumulated along an infinite safe path, and Corollary 82 forces positive
blocks to recur on the \(n/(\log n\log\log n)\) scale. These remain
restrictions, not a contradiction: an aperiodic infinite path with bounded
wrap blocks is not excluded.
