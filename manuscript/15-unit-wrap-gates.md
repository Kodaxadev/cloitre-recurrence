# 15. Exact coordinates for unit-wrap gates

Assume a safe-map zero epoch \((n,U,e)\) begins a positive block with one
wrap, and let \(r\) zero-only blocks precede the next positive block. Define

\[
D=n-2U,\qquad s=4e-n-3.
\]

### Lemma 85

The block returns to \((n+2,U+1,s)\), and

\[
1\le s\le D-3,\qquad s\equiv1-n\pmod4. \tag{15.1}
\]

The next positive-block start has

\[
n'=n+r+2,\quad U'=U+1,\quad D'=D+r,\quad e'=2^rs,
\]

and its positive excess is

\[
s'=4e'-n'-3=2^{r+2}s-n-r-5,\qquad
1\le s'\le D+r-3. \tag{15.2}
\]

For fixed \(n,D,r\), the exact returned-residue candidates are

\[
\left\{
\begin{array}{ll}
x\in\mathbb Z:\;&x\equiv1-n\pmod4,\quad1\le x\le D-3,\\
&n+r+5<2^{r+2}x\le n+D+2r+2
\end{array}
\right\}. \tag{15.3}
\]

Every candidate reconstructs and realizes the parent and child blocks.

#### Proof

The initial zero doubles \(e\); the following wrap subtracts \(n+3\), giving
the returned residue \(s\). The zero and wrap thresholds give
\(1\le s\le D-3\), and its definition gives the congruence. After \(r\)
zero-only blocks the state is \((n+r+2,U+1,2^rs)\), proving (15.2).
Its zero and following-wrap thresholds are exactly the two strict/non-strict
inequalities in (15.3). Conversely, the congruence reconstructs
\(e=(n+3+x)/4\), while \(U=(n-D)/2\); the four displayed bounds are exactly
the parent and child thresholds.

### Corollary 86

Put \(H=2^{r+4}\). The realized unit-wrap gate is unique if and only if

\[
s'\le H
\quad\text{and}\quad
\bigl(s'+H>D+r-3\ \text{or}\ s>D-7\bigr). \tag{15.4}
\]

If \(s\le D-7\), uniqueness therefore forces

\[
D+r-3<2^{r+5}. \tag{15.5}
\]

#### Proof

The candidates in (15.3) form one class modulo \(4\). The realized \(s\) is
unique exactly when both neighboring class members \(s-4,s+4\) fail.
Under \(x\mapsto2^{r+2}x-n-r-5\), their images differ by \(H\), and the
child interval is \([1,D+r-3]\). The lower neighbor fails exactly when
\(s'\le H\). The upper neighbor fails exactly when it crosses either the
child upper boundary or the parent boundary \(x\le D-3\), which is (15.4).
When the parent boundary is inactive, (15.5) follows.

This is a boundary localization, not a termination theorem. A valid local
path beginning at \((n,U,e)=(36,9,13)\) contains seven consecutive unique
unit-wrap gates.
