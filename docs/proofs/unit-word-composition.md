# Composing fixed-ladder return words

## Scope

Lemma 125 gives necessary arithmetic for one return word. An infinite
fixed-ladder tail would require infinitely many such words to fit together
at their forced endpoint indices. This note writes that compatibility
exactly and derives a separate local restriction: for a fixed returned
residue, the pure-upper inequalities select at most one outgoing gap.

The explicit two-renewal family in Proposition 126 does not evade the new
restriction. It has one uniquely forced continuation gate, after which the
pure-upper mechanism stops. This does not yet exclude other, longer
compositions.

## Lemma 127 (exact return-word composition)

Let \(w=(r_0,\ldots,r_{p-1})\) be a nonempty unit-gap word with span

\[
S=\sum_{j=0}^{p-1}(r_j+2).
\]

Write its cumulative positions as

\[
t_j=\sum_{\ell=0}^{j}(r_\ell+2)
\qquad(0\le j<p),
\]

so \(t_{p-1}=S\). Define

\[
H_w=\sum_{j=0}^{p-1}2^{-t_j},
\qquad
K_w=\sum_{j=0}^{p-1}t_j2^{-t_j}.
\tag{127.1}
\]

If both endpoint residues equal \(a\), the word's forced starting index is

\[
\boxed{
n_{\mathrm{start}}+3
=
\Phi_a(w)
:=
\frac{a(1-2^{-S})-K_w}{H_w}.
}
\tag{127.2}
\]

Equivalently, using the integer data \(B_w,W_w\) from Lemma 125,

\[
\Phi_a(w)=
\frac{(2^S-1)a+W_w}{B_w}-S.
\tag{127.3}
\]

Now let \(v\) be a second equal-endpoint word of span \(T\), with data
\(B_v,W_v\). Their forced indices compose consecutively exactly when

\[
\boxed{\Phi_a(v)=\Phi_a(w)+S.}
\tag{127.4}
\]

In integer form, this is the cross-word equation

\[
\boxed{
B_w\bigl((2^T-1)a+W_v\bigr)
=
B_v\bigl((2^S-1)a+W_w+B_wT\bigr).
}
\tag{127.5}
\]

### Proof

Lemma 125 uses suffix exponents \(d_j=S-t_j\). Therefore

\[
B_w=2^SH_w
\]

and

\[
\begin{aligned}
W_w
&=\sum_j(S-t_j)2^{S-t_j}\\
&=2^S(SH_w-K_w).
\end{aligned}
\]

Equation (125.3) gives the endpoint index. Subtracting the span \(S\)
from that endpoint and substituting the preceding identities gives
(127.2)--(127.3).

The start of \(v\) must equal the endpoint of \(w\), which is precisely
(127.4). Substitution of (127.3) for both words and clearing
\(B_wB_v\) gives (127.5). \(\square\)

## Lemma 128 (one outgoing dyadic window)

Consider a unit positive block at \((n,U)\) whose returned residue is
\(a\ge1\). Suppose its outgoing gate is pure-upper, put

\[
h=r+2\ge2,
\]

and let \(g\) be the next returned residue. Then

\[
\boxed{
g=a2^h-n-h-3
}
\tag{128.1}
\]

and the start index lies in the exact dyadic window

\[
\boxed{
(a+4)2^{h-1}+U-h+1
\le n
\le a2^h-h-4.
}
\tag{128.2}
\]

For fixed \((n,U,a)\), at most one integer \(h\ge2\) can satisfy this
window.

Suppose two blocks later on the same all-unit pure-upper tail have the same
returned residue \(a\), with data \((n,U,h,g)\) and
\((n',U',h',g')\), where \(n'>n\) and \(U'\ge U\). Then

\[
\boxed{h'\ge h.}
\tag{128.3}
\]

If \(h'=h\), then

\[
\boxed{g'=g-(n'-n)<g.}
\tag{128.4}
\]

For two occurrences of a fixed pair \((R,a)\), the decrease in (128.4) is
a positive multiple of \(2^{R+2}\).

### Proof

Corollary 114 gives (128.1). Positivity \(g\ge1\) gives the upper endpoint
in (128.2). The pure-upper headroom inequality in Corollary 115 is

\[
D+r-3-g\ge2^{r+4},
\qquad D=n-2U.
\]

Substitute \(r=h-2\) and (128.1):

\[
(a+4)2^h\le2n-2U+2h-2,
\]

which is the lower endpoint in (128.2).

The upper endpoint for exponent \(h\) is strictly below the lower endpoint
for \(h+1\), because their difference is

\[
\bigl((a+4)2^h+U-h\bigr)
-\bigl(a2^h-h-4\bigr)
=4\cdot2^h+U+4>0.
\]

Thus the windows are disjoint and ordered, proving uniqueness.

The lower endpoint at the first occurrence also gives

\[
n-a2^{h-1}
\ge4\cdot2^{h-1}+U-h+1>0.
\tag{128.5}
\]

If \(h'<h\), the upper endpoint at the later occurrence would give

\[
n'<a2^{h'}\le a2^{h-1}<n,
\]

a contradiction. This proves (128.3). When \(h'=h\), subtract (128.1)
at the two starts to get (128.4). Corollary 114 places both occurrences in
the same residue class modulo \(2^{R+2}\), so
\(2^{R+2}\mid n'-n\). \(\square\)

## Proposition 129 (the two-renewal family cannot persist)

Use the notation of Proposition 126. The endpoint block \(2\), with state

\[
(n,U,f)=(n_0+S,3,a),
\]

has exactly one pure-upper unit successor. Its gap and returned residue are

\[
\boxed{r=L=S-5,\qquad d=c-S.}
\tag{129.1}
\]

The successor block is

\[
\boxed{(n,U,f)=(n_0+2S-3,4,d).}
\tag{129.2}
\]

It is a valid unit positive block, but no pure-upper gate can leave it.
Thus every segment in Proposition 126 extends by exactly one pure-upper
gate and then exits the all-unit pure-upper mechanism.

### Proof

At block \(2\), choosing \(r=L\) gives

\[
d=a2^{S-3}-(n_0+S)-S=c-S.
\]

The lower bound (126.10) makes the endpoint parent defect at least two.
Monotonicity of \(c-S\) for \(a\ge7,S\ge32\) also gives

\[
d=c-S\ge\frac{7\cdot2^{29}}9-32>1,
\]

while \(d<c\le2^{S-1}\). Its headroom exceeds the already verified
middle-gate headroom by \(2S-4\). Hence the gate is pure-upper.
Lemma 128 makes this outgoing gap unique.

The next start has the coordinates in (129.2), and

\[
(n_0+2S-3)+3+d=a2^{S-3},
\]

so its unit congruence holds. Also

\[
2d=2c-2S\le n_0-S-4<n_0+2S-6,
\]

using (126.11). Together with the lower bound (126.10), these inequalities
imply both remaining conditions in Lemma 117, so the block is valid.

It remains to exclude its outgoing gaps. For \(r=1\), the next returned
residue would be

\[
8d-(n_0+2S-3)-6=a-9S<1.
\tag{129.3}
\]

The value for \(r=0\) is smaller. For \(r\ge2\), the upper-residue
condition in Corollary 115 would require

\[
2^{r+2}(d-4)\le n_0+2S-3+r+5.
\tag{129.4}
\]

At \(r=2\), left minus right equals

\[
n_0-16S+2a-62>0,
\tag{129.5}
\]

where the last inequality follows from (126.10), \(S\ge32\), and the
monotonic exponential growth of \(n_0-16S\). The difference between the
two sides of (129.4) strictly increases with \(r\), since \(d\ge5\).
Thus (129.4) fails for every \(r\ge2\), completing the proof. \(\square\)

## Consequence and limitation

The fixed-ladder branch is now an exact word-composition problem, not a
collection of independent divisibility tests. Outgoing exponents at repeated
ladder coefficients are nondecreasing, and equal exponents force an
arithmetic descent of the child residue.

Proposition 129 disposes of the infinite local family from Proposition 126:
none of those segments can seed an infinite pure-upper tail. It does not
exclude other return words or prove that equation (127.5) has no infinite
valid chain.

**Superseded framing.** Theorem 130 in
[`unit-chain-determinism.md`](unit-chain-determinism.md) shows that the
disjointness argument used for (128.2) needs neither a fixed returned residue
nor a return word: it applies at every block. The outgoing exponent is
therefore forced everywhere, the mechanism is a deterministic map, and the
cross-word equation (127.5) is satisfied automatically along any orbit rather
than being a constraint to solve. The composition identities above remain
correct and are still the right description of an individual return word; they
are no longer the frontier.
