# Sparse-binary arithmetic and sharp two-renewal families

## Scope

Lemma 123 makes each fixed unit-gap word rigid, but it leaves open how many
different words can connect two occurrences of one fixed renewal pair. This
note rewrites its coefficients as a sparse binary integer and incorporates
the dyadic congruence from Theorem 121.

The resulting arithmetic is exact, but it does not make the return words
finite. Proposition 126 constructs infinitely many literal pure-upper
safe-map segments with two occurrences of the same pair. Thus Theorem 122,
which excludes three strict alternating renewals, is sharp in the number of
renewals.

## Lemma 125 (sparse-binary endpoint equation)

In Lemma 123, put

\[
S=s_p=\sum_{t=0}^{p-1}(r_t+2)
\]

and, for \(0\le j<p\), define the suffix exponents

\[
d_j=S-s_{j+1}.
\]

Set

\[
B=\sum_{j=0}^{p-1}2^{d_j},
\qquad
W=\sum_{j=0}^{p-1}d_j2^{d_j}.
\tag{125.1}
\]

Then

\[
\boxed{
P_p=2^S,\qquad B_p=B,\qquad C_p=(S+3)B-W.
}
\tag{125.2}
\]

Consequently, if \(f_0=f_p=a\), then

\[
\boxed{
B(n_p+3)=(2^S-1)a+W.
}
\tag{125.3}
\]

The exponent set is sparse:

\[
S>d_0>\cdots>d_{p-1}=0,
\qquad
S-d_0=r_0+2\ge2,
\tag{125.4}
\]

and

\[
d_{j-1}-d_j=r_j+2\ge2
\qquad(1\le j<p).
\tag{125.5}
\]

Suppose, in addition, that the endpoints are successive occurrences of a
fixed pair \((R,a)\) of the type isolated in Theorem 121; that is, both
endpoint blocks have
incoming gap \(R\) and returned residue \(a\). Then

\[
\boxed{
S\equiv0\pmod {2^{R+2}}.
}
\tag{125.6}
\]

Moreover \(p\ge2\), the last gap is \(r_{p-1}=R\), and hence

\[
\boxed{d_{p-2}=R+2.}
\tag{125.7}
\]

### Proof

The product recurrence in Lemma 123 gives

\[
P_p=\prod_{t=0}^{p-1}2^{r_t+2}=2^S.
\]

Unrolling the recurrence for \(B_t\) gives one term for each gate:

\[
B_p=\sum_{j=0}^{p-1}
\prod_{t=j+1}^{p-1}2^{r_t+2}
=\sum_{j=0}^{p-1}2^{S-s_{j+1}}=B.
\]

The additive term inserted into \(C_{j+1}\) is

\[
s_j+r_j+5=s_{j+1}+3.
\]

It is multiplied by the same suffix product, so

\[
\begin{aligned}
C_p
&=\sum_{j=0}^{p-1}(s_{j+1}+3)2^{S-s_{j+1}}\\
&=\sum_{j=0}^{p-1}(S+3-d_j)2^{d_j}
=(S+3)B-W.
\end{aligned}
\]

This proves (125.2). Substitute it into Lemma 123:

\[
a=2^Sa-Bn_0-(S+3)B+W.
\]

Since \(n_p=n_0+S\), rearrangement gives (125.3).
Equations (125.4)--(125.5) follow directly from the definitions and
\(r_j\ge0\).

At every occurrence of \((R,a)\), Corollary 114 gives

\[
n+3+a\equiv0\pmod {2^{R+2}}.
\]

Subtracting this congruence at the two endpoints yields (125.6). If \(p=1\),
then \(S=R+2\), but \(0<R+2<2^{R+2}\), contradicting (125.6). Thus \(p\ge2\).
The incoming gap at the final endpoint is the last gap of the word, so
\(r_{p-1}=R\), and (125.5) gives (125.7). \(\square\)

## Proposition 126 (arbitrarily long exact two-renewal segments)

Fix an integer

\[
7\le a\le32,\qquad 3\nmid a.
\tag{126.1}
\]

For every positive integer \(q\) satisfying

\[
\boxed{q\equiv4a\pmod {12},}
\tag{126.2}
\]

put

\[
S=8q,\qquad L=S-5,\qquad T=2^S
\tag{126.3}
\]

and define

\[
\begin{aligned}
n_0&=\frac{a(T-1)+24}{9}-S-3,\\
b&=\frac{n_0+3+a}{8},\\
c&=\frac{a2^{S-3}+a+3}{9}.
\end{aligned}
\tag{126.4}
\]

There is a literal safe-map segment of four consecutive unit positive
blocks with

\[
\begin{array}{c|cccc}
\text{block}&-1&0&1&2\\ \hline
n&n_0-3&n_0&n_0+S-3&n_0+S\\
U&0&1&2&3\\
\text{returned residue}&b&a&c&a
\end{array}
\tag{126.5}
\]

and intervening gaps

\[
\boxed{(1,L,1).}
\tag{126.6}
\]

Every block satisfies the exact unit-state test in Lemma 117, and every
gate satisfies the pure-upper criterion in Corollary 115. Hence the fixed
pair

\[
(R,a)=(1,a)
\]

occurs at blocks \(0\) and \(2\), with intervening word \((L,1)\).
As \(q\) ranges through (126.2), \(L\) is unbounded.

### Proof

For the word \((L,1)\), the suffix exponents are \(\{3,0\}\), so Lemma 125
has \(B=9\), \(W=24\), and gives exactly the formula for \(n_0\) in
(126.4).

Condition (126.2) implies \(q\equiv a\pmod3\) and \(4\mid q\).
Because \(2^6\equiv1\pmod9\), the two possible nonzero classes give

\[
2^S\equiv
\begin{cases}
4\pmod9,&a\equiv1\pmod3,\\
7\pmod9,&a\equiv2\pmod3.
\end{cases}
\]

Thus \(9\mid a(T-1)+24\), so \(n_0\) is integral. Since \(S\equiv0\pmod8\)
and \(T\equiv0\pmod8\), reduction of (126.4) modulo eight gives

\[
n_0+3+a\equiv0\pmod8,
\]

so \(b\) is integral. The middle recurrence gives the useful equivalent
formula

\[
c=a2^{S-3}-n_0-S,
\tag{126.7}
\]

which proves that \(c\) is integral.

The four unit-state congruences are

\[
\begin{aligned}
(n_0-3)+3+b&=n_0+b,\\
n_0+3+a&=8b,\\
(n_0+S-3)+3+c&=a2^{S-3},\\
(n_0+S)+3+a&=8c.
\end{aligned}
\tag{126.8}
\]

For the first line, multiplying by eight gives

\[
8(n_0+b)=9n_0+a+3=aT-9S.
\]

Here \(32\mid T\) and \(32\mid S\), because \(4\mid q\). Therefore all
four quantities in (126.8) are divisible by four.

The exact returned-residue recurrence across the three gaps follows from

\[
8b-(n_0-3)-6=a,
\]

(126.7), and

\[
8c-(n_0+S-3)-6=a.
\tag{126.9}
\]

It remains to check the inequalities. Condition (126.2) forces
\(S\ge32\). The expression for \(n_0\) is increasing in both \(a\) and
integer \(S\) on this range, so

\[
n_0\ge
\frac{7(2^{32}-1)+24}{9}-35
=3\,340\,530\,086.
\tag{126.10}
\]

The small linear lower bounds in Lemma 117 and Corollary 115 are therefore
immediate. The only scale-sensitive inequalities reduce, after substituting
(126.4), to

\[
\begin{aligned}
2c\le n_0+S-4
&\Longleftarrow a(T/4-1)\ge15,\\
c\le T/2
&\Longleftrightarrow (36-a)T\ge8a+24,\\
n_0+S-10-c\ge T/2
&\Longleftrightarrow (7a-36)T\ge16a+768.
\end{aligned}
\tag{126.11}
\]

They hold for \(7\le a\le32\) and \(T\ge2^{32}\). Also

\[
2b\le n_0-2
\Longleftrightarrow
n_0\ge\frac{a+11}{3},
\]

and \(2a\le n_0\). These inequalities imply all four bounds
\(f\le D-3\) and \(4f\le n+D+2\) in Lemma 117. The first and third gates
have scale \(2^{1+4}=32\); their next residue is \(a\le32\), and (126.10)
supplies their defect and headroom bounds. The middle gate has scale
\(2^{L+4}=T/2\), and its three pure-upper inequalities are precisely the
corresponding large-\(n_0\) bound and the last two lines of (126.11).
Lemma 117 and Corollary 115 now reconstruct the claimed literal segment.
\(\square\)

## Consequence and limitation

The sparse endpoint equation and renewal congruence are necessary arithmetic
conditions, but they do not bound the span of one fixed-ladder return.
Proposition 126 supplies infinitely many exact, locally valid spans with two
renewals. Theorem 122 is therefore sharp: two strict alternating occurrences
exist at unbounded scales, while three consecutive occurrences do not.

These segments are valid states of the reduced safe map. They are not claimed
to be reachable from an original initial value \(b_1=m\). Proposition 129
shows more than the non-concatenation implied by Theorem 122: each segment
has one forced continuation gate and then leaves the pure-upper mechanism.
The remaining fixed-ladder problem is compatibility among other return words
of varying block lengths, not single-word integrality.
