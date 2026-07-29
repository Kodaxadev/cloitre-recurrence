# Unit-wrap gate coordinates

## Scope

This note sharpens the exact adjacent-block gate when the first positive
safe-map block has one wrap. It gives an induced three-coordinate map and an
if-and-only-if uniqueness test. It does not bound the length of a chain of
unique gates and does not prove termination.

Use the safe state \((n,U,e)\), where \(U\) is the accumulated wrap counter
and \(0<e<n-U\). Assume it is a zero epoch whose following wrap block has
length one. Put

\[
D=n-2U,\qquad s=4e-n-3.
\]

Let \(r\ge0\) be the number of zero-only blocks before the next positive
block.

## Lemma 85 (unit-wrap induced gate)

The unit-wrap block returns to

\[
(n+2,U+1,s).
\]

Moreover,

\[
1\le s\le D-3,\qquad s\equiv1-n\pmod4. \tag{85.1}
\]

The next positive-block start has coordinates

\[
\begin{aligned}
n'&=n+r+2,\\
U'&=U+1,\\
D'&=D+r,\\
e'&=2^rs,\\
s'&=4e'-n'-3
   =2^{r+2}s-n-r-5.
\end{aligned} \tag{85.2}
\]

In particular,

\[
1\le s'\le D+r-3. \tag{85.3}
\]

For fixed \(n,D,r\), the exact gate candidates are

\[
\mathcal S(n,D,r)=
\left\{
\begin{array}{ll}
x\in\mathbb Z:\;&x\equiv1-n\pmod4,\\
&1\le x\le D-3,\\
&2^{r+2}x>n+r+5,\\
&2^{r+2}x\le n+D+2r+2
\end{array}
\right\}. \tag{85.4}
\]

Every \(x\in\mathcal S(n,D,r)\) reconstructs the preceding start by

\[
U=(n-D)/2,\qquad e=(n+3+x)/4,
\]

and realizes exactly one wrap, \(r\) zero-only blocks, and then a positive
block. Thus the set is sufficient as well as necessary.

### Proof

The first zero sends \(e\) to \(2e\). The single following wrap subtracts
the modulus \(n+3\), so the returned residue is
\(4e-(n+3)=s\), at index \(n+2\) and counter \(U+1\).

The first step is zero, so \(2e\le n-U\). The following step is a wrap, so
\(4e>n+3\). Hence

\[
1\le s=4e-n-3
\le2(n-U)-n-3=D-3.
\]

The congruence in (85.1) follows directly from \(s=4e-n-3\).

Each zero-only block doubles the residue and advances the index once without
changing \(U\). This gives the first four relations in (85.2), and the
definition of \(s'\) gives the last. The next block is positive exactly when

\[
2^{r+2}s>n+r+5.
\]

The zero step at its start is valid exactly when

\[
2^{r+1}s\le n-U+r+1,
\]

which, using \(2U=n-D\), is the final inequality in (85.4). These two
conditions also give (85.3). Conversely, (85.1) makes \(U,e\) integral, and
the four inequalities in (85.4) are precisely the parent zero/wrap and child
zero/wrap thresholds. This proves exact reconstruction.

## Corollary 86 (exact unit-wrap uniqueness boundary)

Let

\[
H=2^{r+4}.
\]

The realized gate in Lemma 85 is unique if and only if

\[
\boxed{
s'\le H
\quad\text{and}\quad
\bigl(s'+H>D+r-3\ \text{or}\ s>D-7\bigr).
} \tag{86.1}
\]

Consequently, if \(s\le D-7\), uniqueness forces

\[
D+r-3<2^{r+5}. \tag{86.2}
\]

### Proof

The candidates in (85.4) occupy one residue class modulo \(4\). Since \(s\)
is a candidate, it is unique exactly when neither \(s-4\) nor \(s+4\) is
admissible.

Under the affine change

\[
x\longmapsto 2^{r+2}x-n-r-5,
\]

adjacent lattice values differ by \(H\), and the child interval becomes
\([1,D+r-3]\). Thus \(s-4\) is absent exactly when \(s'\le H\).
The value \(s+4\) is absent exactly when it exceeds either the child upper
boundary, giving \(s'+H>D+r-3\), or the parent upper boundary \(D-3\),
giving \(s>D-7\). This proves (86.1). If the parent boundary is inactive,
the two remaining strict inequalities give (86.2).

## Initial consequence

The unit-wrap gate is now a deterministic affine map on \((n,D,s)\), with
uniqueness localized to explicit lower and upper boundary layers. This
replaces a qualitative “narrow lattice interval” description by an exact
test. It still permits chains: the valid state \((n,U,e)=(36,9,13)\) has
seven consecutive unique unit-wrap gates.
