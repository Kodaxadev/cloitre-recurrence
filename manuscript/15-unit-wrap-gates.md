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

### Lemma 87

Suppose three consecutive unit-wrap positive-block starts
\((n_i,D_i,s_i)\), \(0\le i\le2\), all satisfy \(s_i>D_i-7\). Then

\[
\begin{array}{c|ccc}
i&n_i&D_i&s_i\\ \hline
0&12&8&5\\
1&14&8&3\\
2&17&9&4
\end{array},
\qquad (r_0,r_1)=(0,1). \tag{15.6}
\]

The third start is \((n,U,e)=(17,4,6)\), and its safe path enters the
terminating middle strip before another positive block.

#### Proof

Set \(\delta_i=D_i-s_i\). Equations (15.1) and \(n_i\equiv D_i\pmod2\)
give \(\delta_i\in\{3,5\}\). For a transition with gap \(r_i\), (15.2)
gives

\[
n_i=(2^{r_i+2}-1)D_i-2^{r_i+2}\delta_i-2r_i-5
    +\delta_{i+1}, \tag{15.7}
\]

and reduction modulo \(4\) gives

\[
\delta_{i+1}=\delta_i\ (r_i\text{ odd}),\qquad
\delta_{i+1}=8-\delta_i\ (r_i\text{ even}). \tag{15.8}
\]

Write \(r=r_0\), \(r'=r_1\), \(a=2^{r+2}\), and \(a'=2^{r'+2}\).
Eliminating the intermediate state yields

\[
(a-a')D_0
=a'r+a\delta_0-(a'+1)\delta_1-2r'-2+\delta_2. \tag{15.9}
\]

If \(r=r'\), (15.8) makes the right side nonzero. If \(r>r'\), reduction
modulo \(a'\) forces \(r'=0\); the four cases from (15.8) reduce to

\[
\frac r{2^r-1},\quad\frac{r-1}{2^r-1},\quad
\frac{r-3}{2^r-1},\quad\frac{r+2}{2^r-1},
\]

and their only positive integral case gives the invalid index \(n_0=0\).
If \(r<r'\), put \(d=r'-r\), \(M=2^d-1\), and

\[
t=\frac{\delta_1+2r'+2-\delta_2}{2^{r+2}}.
\]

Then

\[
D_0=\delta_1-r+
\frac{t-(r+\delta_0-\delta_1)}M. \tag{15.10}
\]

For \(r\ge2\), validity forces \(t\ge M\), contradicting
\(t\le(r+d+2)/2^{r+1}<M\). The case \(r=1\) similarly requires
\(t\ge2M+1>(r'+2)/4\). For \(r=0\), divisibility in (15.10) leaves only
\((\delta_0,\delta_1,r')=(3,5,1)\), which gives (15.6).

The resulting raw path ends

\[
(17,4,6)\to(18,4,12)\to(19,5,4)\to(20,5,8),
\]

where \(15<16\le22\), the terminating strip.

### Corollary 88

Among any \(L\) consecutive unique unit-wrap gates, at least
\(\lfloor L/2\rfloor\) satisfy

\[
D+r-3<2^{r+5},
\qquad
r>\log_2(D+r-3)-5. \tag{15.11}
\]

#### Proof

Put \(H=2^{r+4}\). Every unique gate has \(s'\le H\). If
\(s\le D-7\), Corollary 86 also gives \(s'+H>D+r-3\), proving
(15.11). If a unique gate fails (15.11), then

\[
D'=D+r\ge2H+3,\qquad D'-s'\ge H+3>7.
\]

The successor parent boundary is therefore inactive, so its next unique
gate must satisfy (15.11). Failures cannot be consecutive, proving the
pair count.

This remains compatible with \(n/\log n\)-scale quotient growth and is not a
termination theorem.

### Corollary 89

Suppose an infinite safe path consists entirely of unit-wrap positive blocks
and every gate is unique. At its \(j\)-th positive-block start,

\[
\liminf_{j\to\infty}\frac{D_j}{j\log_2j}\ge\frac12, \tag{15.12}
\]

and

\[
1\le\liminf_{j\to\infty}\frac{U_j\log_2n_j}{n_j}
\le\limsup_{j\to\infty}\frac{U_j\log_2n_j}{n_j}\le2. \tag{15.13}
\]

#### Proof

The transition gives \(U_j=U_0+j\), \(D_{j+1}=D_j+r_j\), and
\(n_j=D_j+2U_j\). The sequence \(D_j\) must diverge: otherwise eventually
\(r_j=0\), while bounded \(s_j\le D_j-3\) cannot satisfy
\(4s_j>n_j+5\) as \(n_j\to\infty\).

By Corollary 88, one gate in each pair beginning at \(2t\) satisfies

\[
D_{2t+2}-D_{2t}>\log_2(D_{2t}-3)-5. \tag{15.14}
\]

For any \(\varepsilon>0\), this is eventually at least
\((1-\varepsilon)\log_2D_{3t}\). Summing and using
\(\sum_{u\le t}\log_2u=t\log_2t-O(t)\) proves (15.12). Theorem 45 gives
the lower bound in (15.13); (15.12), \(U_j=U_0+j\), and
\(n_j=D_j+2U_j\) give the upper bound.

This confines the subcase to a critical quotient scale but does not exclude
it.

### Theorem 90

Under the hypotheses of Corollary 89, every sufficiently late gate satisfies

\[
D_j+r_j-3<2^{r_j+5}, \tag{15.15}
\]

and

\[
\frac{D_j}{j\log_2j}\longrightarrow1,\qquad
\frac{U_j\log_2n_j}{n_j}\longrightarrow1. \tag{15.16}
\]

#### Proof

Put \(a=2^{r+2}\) and \(\delta=D-s\). The transition gives

\[
\delta'=2U-(a-2)D+a\delta+2r+5. \tag{15.17}
\]

If a unique gate fails (15.15), Corollary 86 forces
\(\delta\in\{3,5\}\), while failure gives \(D\ge8a-r+3\). Since
\(\delta'\ge3\),

\[
2U\ge(a-2)D-5a-2r-2.
\]

The bound \(D\ge8a-r+3\) implies
\((a-3)D\ge5a+2r+2\): check \(r=0\) directly, while for \(r\ge1\),
\(r\le a/4\), \(D>7a\), and \(a-3\ge5\). Hence every failing gate has
\(U\ge D/2\).

Corollary 89 and \(U_j=U_0+j\) give \(U_j/D_j\to0\), so only finitely many
gates fail (15.15). Therefore

\[
D_{j+1}-D_j>\log_2(D_j-3)-5
\]

at every sufficiently late gate. Summation gives
\(\liminf D_j/(j\log_2j)\ge1\), hence
\(\limsup U_j\log_2n_j/n_j\le1\). Theorem 45 supplies the reverse lower
limit. Since \(n_j/D_j\to1\), this yields
\(j\log_2D_j/D_j\to1\), then \(\log D_j/\log j\to1\), and finally both
limits in (15.16).

The exact critical scale is still compatible with an aperiodic integer
trajectory.
