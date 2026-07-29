# Composing fixed-ladder words

## Lemma 127

For a unit-gap word \(w=(r_0,\ldots,r_{p-1})\), let

\[
t_j=\sum_{\ell=0}^{j}(r_\ell+2),\quad S=t_{p-1},
\quad
H_w=\sum_j2^{-t_j},\quad K_w=\sum_jt_j2^{-t_j}.
\]

If both endpoint residues equal \(a\), its forced starting index satisfies

\[
\boxed{
n_{\rm start}+3
=\Phi_a(w)
:=\frac{a(1-2^{-S})-K_w}{H_w}.
}
\tag{26.1}
\]

For a second word \(v\) of span \(T\), consecutive forced indices are
equivalent to

\[
\boxed{\Phi_a(v)=\Phi_a(w)+S.} \tag{26.2}
\]

In the integer notation of Lemma 125, this is

\[
B_w((2^T-1)a+W_v)
=B_v((2^S-1)a+W_w+B_wT). \tag{26.3}
\]

### Proof

The suffix exponents give

\[
B_w=2^SH_w,\qquad W_w=2^S(SH_w-K_w).
\]

Substitute into Lemma 125 and subtract \(S\) from the forced endpoint.
Equation (26.2) says exactly that the next forced start is the preceding
endpoint; clearing denominators gives (26.3). \(\square\)

## Lemma 128

At a pure-upper unit gate whose current returned residue is \(a\), put
\(h=r+2\) and call the next returned residue \(g\). Then

\[
g=a2^h-n-h-3
\]

and

\[
\boxed{
(a+4)2^{h-1}+U-h+1
\le n
\le a2^h-h-4.
}
\tag{26.4}
\]

The windows (26.4) are pairwise disjoint as \(h\) varies. At chronologically
later occurrences of the same \(a\), the outgoing exponents are therefore
nondecreasing. If two are equal, their child residues satisfy

\[
g'=g-(n'-n)<g. \tag{26.5}
\]

For a fixed pair \((R,a)\), this decrease is divisible by \(2^{R+2}\).

### Proof

The unit recurrence gives \(g\). Positivity gives the upper endpoint.
Substitution into Corollary 115's headroom inequality gives the lower one.
The lower endpoint for \(h+1\) exceeds the upper endpoint for \(h\) by
\(4\cdot2^h+U+4\).

Moreover (26.4) implies \(n>a2^{h-1}\). A later occurrence with
\(h'<h\) would have \(n'<a2^{h'}\le a2^{h-1}<n\), impossible.
Equal exponents give (26.5) by subtraction, and Corollary 114 supplies the
fixed-pair divisibility. \(\square\)

## Proposition 129

Every Proposition 126 segment has one further pure-upper gate, uniquely:

\[
(n_0+S,3,a)
\xrightarrow{\,S-5\,}
(n_0+2S-3,4,c-S).
\tag{26.6}
\]

The final block in (26.6) is a valid unit block but has no pure-upper
outgoing gate.

### Proof

The recurrence gives the displayed residue. Proposition 126's inequalities
verify the gate, and Lemma 128 gives uniqueness. Lemma 117 verifies the
child block using \(2(c-S)\le n_0-S-4\).

For a following gap \(r=1\), the returned residue would be \(a-9S<1\);
the \(r=0\) value is smaller. For \(r\ge2\), Corollary 115 would require

\[
2^{r+2}(c-S-4)\le n_0+2S+r+2.
\]

At \(r=2\), left minus right is
\(n_0-16S+2a-62>0\), and the difference increases thereafter.
Thus no following pure-upper gate exists. \(\square\)

This eliminates the infinite local family of Proposition 126 as a possible
pure-upper tail, but it does not exclude other compatible word sequences.
