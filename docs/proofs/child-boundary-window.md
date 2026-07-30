# Canonical windows for interior safe-block gates

## Scope

Corollary 102 leaves two possibilities at infinitely many interior
positive-block starts: a nonunique gate or a unique gate in the child
boundary layer. This note combines those alternatives into one exact moving
window. It does not prove that an orbit must eventually miss that window.

Retain the notation of Lemma 92. Thus a positive block starts at
\((n,U,e)\), has length \(k\ge1\), returns at

\[
(m,V,f),\qquad m=n+k+1,
\]

and is followed by \(r\ge0\) zero-only blocks. Put

\[
x=2^{r+2}f-m-r-3,\qquad H=2^{k+r+3}.
\]

At the next positive-block start define

\[
D'=m+r-2V=G+r
\]

and retain its defect

\[
d'=m+r-V-2^{r+1}f.
\]

Let \(\rho=\rho_{k,r}(n)\in\{1,\ldots,H\}\) be the least positive
representative modulo \(H\) of

\[
\boxed{
R_{k,r}(n)
=2^{r+2}(n+k+4)-2^{k+r+2}n-n-k-r-4.
} \tag{103.1}
\]

## Lemma 103 (canonical child-residue decomposition)

There is a unique integer \(j\ge0\) such that

\[
\boxed{x=\rho+jH.} \tag{103.2}
\]

Moreover,

\[
\boxed{D'-3=\rho+jH+2d'.} \tag{103.3}
\]

### Proof

Lemma 83 gives

\[
f=m+3-2^kA,\qquad A=n+4-2e.
\]

Therefore

\[
\begin{aligned}
x
&=2^{r+2}(m+3)-2^{k+r+2}A-m-r-3\\
&=2^{r+2}(n+k+4)-2^{k+r+2}A-n-k-r-4.
\end{aligned}
\]

Since \(A\equiv n\pmod2\), multiplication by \(2^{k+r+2}\) gives

\[
2^{k+r+2}A\equiv2^{k+r+2}n\pmod{2^{k+r+3}}.
\]

Hence \(x\equiv R_{k,r}(n)\equiv\rho\pmod H\). Lemma 92 gives \(x\ge1\).
Because \(1\le\rho\le H\), the congruence has the unique form
\(x=\rho+jH\) with \(j\ge0\), proving (103.2).

Equation (92.2), together with \(D'=G+r\), gives

\[
D'-3=x+2d'.
\]

Substitute (103.2) to obtain (103.3). \(\square\)

## Corollary 104 (exact interior child window)

Suppose the parent start is interior, so \(d\ge2\). Then the gate is unique
if and only if

\[
\boxed{\rho\le D'-3<\rho+H.} \tag{104.1}
\]

It is nonunique if and only if

\[
\boxed{D'-3\ge\rho+H.} \tag{104.2}
\]

### Proof

For \(d\ge2\), Lemma 92 says that the gate is unique exactly when

\[
x\le H,\qquad 2d'<H.
\]

By (103.2), the first inequality is equivalent to \(j=0\). Under \(j=0\),
equation (103.3) makes the second inequality equivalent to
\(D'-3<\rho+H\); its lower endpoint holds because \(d'\ge0\).
This proves (104.1). Equation (103.3) always gives \(D'-3\ge\rho\), so
(104.2) is the exact complement. \(\square\)

## Corollary 105 (the window origin permutes dyadic residues)

For fixed \(k\ge1\) and \(r\ge0\), the map

\[
n\bmod H\longmapsto\rho_{k,r}(n)
\]

permutes the \(H\) positive residue representatives.

### Proof

The coefficient of \(n\) in (103.1) is

\[
2^{r+2}-2^{k+r+2}-1
=-\bigl((2^k-1)2^{r+2}+1\bigr),
\]

which is odd. It is therefore invertible modulo the power of two \(H\).
Adding the constant term preserves bijectivity. \(\square\)

## Lemma 106 (every unique gate fixes the next-block band)

Suppose the gate is unique, and let

\[
n'=m+r
\]

be the next positive-block start. If its positive block has length
\(\ell\ge1\), then

\[
\boxed{
n'+5-\frac{n'+\ell+4}{2^{\ell-1}}
<\rho
\le
n'+5-\frac{n'+\ell+5}{2^\ell}.
} \tag{106.1}
\]

### Proof

Every unique gate has \(x\le H\) by Lemma 92, so Lemma 103 gives \(j=0\).
At the child start, write \(A'=U'+d'+4\), where
\(U'=V\). Since \(D'=n'-2U'\), equation (103.3) gives

\[
\begin{aligned}
2A'
&=2U'+2d'+8\\
&=n'-D'+(D'-3-\rho)+8\\
&=n'+5-\rho. \tag{106.2}
\end{aligned}
\]

Lemma 53 makes \(\ell\) the least \(j\ge0\) satisfying

\[
2^{j+1}A'\ge n'+j+5.
\]

Because \(\ell\ge1\), failure at \(j=\ell-1\) and success at \(j=\ell\)
give

\[
2^\ell A'<n'+\ell+4,\qquad
2^{\ell+1}A'\ge n'+\ell+5.
\]

Substitute (106.2) and solve both inequalities for \(\rho\). \(\square\)

## Corollary 107 (long child blocks require an almost-logarithmic gap)

Under Lemma 106's hypotheses,

\[
\boxed{\ell=1\iff 2\rho\le n'+4,} \tag{107.1}
\]

and

\[
\boxed{\ell\ge2\iff 2\rho>n'+4.} \tag{107.2}
\]

In the latter case,

\[
\boxed{
r>\log_2(n'+4)-k-4.
} \tag{107.3}
\]

Every adjacent-block gate also satisfies

\[
\boxed{2^{r+1}\le n',\qquad r\le\log_2n'-1.} \tag{107.4}
\]

Consequently, along a hypothetical infinite safe path, every sufficiently
late unique gate whose child block has length at least two satisfies

\[
\boxed{
r\ge
\log_2 n'-\log_2\log_2 n'-O(1).
} \tag{107.5}
\]

Along any infinite sequence of such gates,

\[
\boxed{\frac{r}{\log_2n'}\longrightarrow1.} \tag{107.6}
\]

### Proof

For \(\ell=1\), (106.1) reduces to

\[
0<\rho\le\frac{n'+4}{2}.
\]

If \(\ell\ge2\), the stopping test has not succeeded at \(j=1\), so

\[
4A'<n'+6.
\]

Using (106.2), this is \(2\rho>n'+4\). These alternatives are exhaustive,
proving (107.1)--(107.2).

Since \(\rho\le H=2^{k+r+3}\), (107.2) gives

\[
2^{k+r+4}>n'+4,
\]

which is (107.3). Corollary 81 gives

\[
k\le\log_2\log_2 n'+o(1)
\]

along an infinite safe path; replacing the parent index by the larger
child index only weakens that bound. Substitution into (107.3) proves
(107.5).

The upper gate endpoint in Lemma 83 gives

\[
2^{r+1}f\le m-V+r\le m+r=n'.
\]

Since \(f\ge1\), this proves (107.4). Divide (107.4)--(107.5) by
\(\log_2n'\) to obtain (107.6). \(\square\)

## Corollary 108 (exhaustive scaled safe-gate alternative)

Every hypothetical infinite safe path satisfies at least one of:

1. infinitely many adjacent positive-block gates are nonunique;
2. infinitely many unique gates lead to child blocks of length at least two,
   and their zero-only gaps satisfy
   \[
   r\ge\log_2n'-\log_2\log_2n'-O(1).
   \tag{108.1}
   \]

In the second alternative, \(r/\log_2n'\to1\) along those gates.

### Proof

If only finitely many gates are nonunique, every sufficiently late gate is
unique. Theorem 91 then implies that the positive blocks cannot be eventually
unit, so infinitely many child blocks have length at least two. Apply
Corollary 107 to their preceding gates. \(\square\)

## Corollary 109 (longer-child resets have zero time density)

Along a hypothetical infinite safe path, let \(R(N)\) count the unique gates
whose child block has length at least two and whose child start satisfies
\(n'\le N\). Then

\[
\boxed{R(N)=O\!\left(\frac{N}{\log N}\right),} \tag{109.1}
\]

so \(R(N)/N\to0\).

### Proof

Corollary 107 implies that, for every sufficiently large such gate,

\[
r\ge\frac12\log_2n'.
\]

Fix large \(N\). Gates with \(n'<\sqrt N\) contribute at most \(\sqrt N\),
because child-start indices are distinct. Every remaining counted gate has

\[
r\ge\frac14\log_2N.
\]

The zero-only gaps belonging to distinct adjacent-block gates are disjoint,
and every counted gap ends by index \(N\). Their total length is therefore
at most \(N\). Hence the remaining gates number at most
\(4N/\log_2N\), proving (109.1). \(\square\)

## Consequence and limitation

At every interior start, the two nonuniqueness mechanisms in Corollary 93
are now one event: the successor gap lies at or above the next translate of
an explicit canonical window. A unique child-boundary gate is exactly a hit
in the first window.

The origin \(\rho\) depends only on \(n,k,r\), not on the other state
coordinates, and it sweeps every residue for fixed \(k,r\). This removes any
fixed congruence-class obstruction. What remains is dynamical: exclude an
infinite orbit whose changing successor gaps repeatedly stay inside these
moving windows, or show that misses accumulate strongly enough to force
termination. Lemma 106 adds that every first-window hit leading to a longer
child block consumes an almost-logarithmic zero-only gap. Such sparse resets
remain compatible with Corollary 82's lower bound on positive-block
frequency. Corollary 109 makes the longer-block resets sparse in absolute
time, but does not make them finite. Corollary 108 is exhaustive, and
neither of its alternatives is yet a contradiction.
