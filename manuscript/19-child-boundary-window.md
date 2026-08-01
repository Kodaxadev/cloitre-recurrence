# Canonical child-boundary windows

Retain Lemma 92's gate notation. A positive block starts at \((n,U,e)\),
has length \(k\ge1\), returns at \((m,V,f)\), and is followed by \(r\ge0\)
zero-only blocks. Put

\[
x=2^{r+2}f-m-r-3,\qquad H=2^{k+r+3},
\]

and at the next positive-block start put

\[
D'=m+r-2V,\qquad d'=m+r-V-2^{r+1}f.
\]

Let \(\rho\in\{1,\ldots,H\}\) be the least positive representative of

\[
R_{k,r}(n)
=2^{r+2}(n+k+4)-2^{k+r+2}n-n-k-r-4
\pmod H. \tag{19.1}
\]

## Lemma 103 (canonical child-residue decomposition)

There is a unique \(j\ge0\) such that

\[
x=\rho+jH,\qquad D'-3=\rho+jH+2d'. \tag{19.2}
\]

### Proof

Lemma 83 gives \(f=m+3-2^kA\), where \(A=n+4-2e\). Substitution gives

\[
x=2^{r+2}(n+k+4)-2^{k+r+2}A-n-k-r-4.
\]

Since \(A\equiv n\pmod2\), this is congruent to \(R_{k,r}(n)\) modulo
\(H\). Lemma 92 gives \(x\ge1\), so the least-positive convention gives
the unique decomposition \(x=\rho+jH\) with \(j\ge0\). Finally, (92.2)
is \(D'-3=x+2d'\). \(\square\)

## Corollary 104 (exact interior child window)

If the parent defect satisfies \(d\ge2\), then

\[
\boxed{\text{unique}\iff \rho\le D'-3<\rho+H,} \tag{19.3}
\]

and

\[
\boxed{\text{nonunique}\iff D'-3\ge\rho+H.} \tag{19.4}
\]

### Proof

For \(d\ge2\), Lemma 92 gives uniqueness exactly when \(x\le H\) and
\(2d'<H\). By (19.2), these conditions are respectively \(j=0\) and
\(D'-3<\rho+H\). The lower endpoint follows from \(d'\ge0\), and (19.4)
is the exact complement. \(\square\)

## Corollary 105 (dyadic residue permutation)

For fixed \(k,r\), the map \(n\bmod H\mapsto\rho_{k,r}(n)\) permutes all
positive residue representatives modulo \(H\).

### Proof

The coefficient of \(n\) in (19.1) is

\[
-\bigl((2^k-1)2^{r+2}+1\bigr),
\]

which is odd and hence invertible modulo the power of two \(H\). \(\square\)

## Lemma 106 (unique-gate next-block band)

Suppose the gate is unique. Let \(n'=m+r\), and let the
positive block at that child start have length \(\ell\ge1\). Then

\[
\boxed{
n'+5-\frac{n'+\ell+4}{2^{\ell-1}}
<\rho
\le n'+5-\frac{n'+\ell+5}{2^\ell}.
} \tag{19.5}
\]

### Proof

Lemma 92 and (19.2) give \(j=0\). At the child start,
\(D'=n'-2U'\), so

\[
2A'=2U'+2d'+8=n'+5-\rho. \tag{19.6}
\]

Lemma 53 makes \(\ell\) the least \(j\) satisfying
\(2^{j+1}A'\ge n'+j+5\). Failure at \(j=\ell-1\), success at
\(j=\ell\), and (19.6) give (19.5). \(\square\)

## Corollary 107 (long-child gap scale)

Under Lemma 106's hypotheses,

\[
\ell=1\iff2\rho\le n'+4,\qquad
\ell\ge2\iff2\rho>n'+4. \tag{19.7}
\]

In the second case,

\[
r>\log_2(n'+4)-k-4. \tag{19.8}
\]

Every gate satisfies

\[
2^{r+1}\le n',\qquad r\le\log_2n'-1. \tag{19.9}
\]

Along a hypothetical infinite safe path, every sufficiently late such gate
satisfies

\[
r\ge\log_2n'-\log_2\log_2n'-O(1), \tag{19.10}
\]

so along any infinite sequence of them,
\[
r/\log_2n'\to1. \tag{19.11}
\]

### Proof

For \(\ell=1\), (19.5) is
\(0<\rho\le(n'+4)/2\). If \(\ell\ge2\), failure of the stopping test at
\(j=1\), together with (19.6), gives \(2\rho>n'+4\).
Since \(\rho\le H=2^{k+r+3}\), this proves (19.8).
Corollary 81 gives \(k\le\log_2\log_2n'+o(1)\), which yields (19.10).
\(2^{r+1}f\le m-V+r\le n'\) and \(f\ge1\) give the upper bound.
The ratio limit follows.
\(\square\)

## Corollary 108 (scaled safe-gate alternative)

Every hypothetical infinite safe path has either infinitely many nonunique
gates, or infinitely many unique gates leading to longer child blocks whose
zero-only gaps satisfy

\[
r\ge\log_2n'-\log_2\log_2n'-O(1). \tag{19.12}
\]

### Proof

If nonunique gates are finite, all late gates are unique. Theorem 91 then
forces infinitely many nonunit child blocks, and Corollary 107 applies to
their preceding gates. \(\square\)

## Corollary 109 (reset sparsity in time)

Let \(R(N)\) count unique gates whose child blocks have length at least two
and whose child-start indices are at most \(N\). Along a hypothetical
infinite safe path,

\[
R(N)=O(N/\log N),\qquad R(N)/N\to0. \tag{19.13}
\]

### Proof

For all sufficiently late counted gates, Corollary 107 gives
\(r\ge\frac12\log_2n'\). Those with \(n'<\sqrt N\) number at most
\(\sqrt N\). Every other counted gate has
\(r\ge\frac14\log_2N\). Their zero-only gaps are disjoint and have total
length at most \(N\), so they number at most \(4N/\log_2N\). \(\square\)

Thus every interior gate is classified by one explicit moving window. This
is an exact coordinate reduction. Longer-block returns require nearly
logarithmic zero-only gaps, but neither repeated unit returns nor sparse
longer-block resets are excluded, and neither alternative in Corollary 108
is yet contradictory.
