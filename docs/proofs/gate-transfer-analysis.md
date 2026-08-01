# Exact residue transfer across adjacent safe-block gates

## Scope

Lemma 103 decomposes the child excess \(x\), and Lemma 110 counts every
locally valid parent. The next positive block turns the same \(x\) into its
returned residue by an exact affine formula. This removes the defects and
the quotient from one inter-gate transition.

Retain the notation of Lemmas 83 and 103. A parent positive block of length
\(k\), followed by \(r\) zero-only blocks, reaches a child positive-block
start \((n',U',e')\). Put

\[
x=2^{r+2}f-m-r-3,
\]

where \(f\) is the parent's returned residue. Let the child block have
length \(\ell\ge1\), overshoot

\[
A'=n'+4-2e'=U'+d'+4,
\]

and returned residue \(g\).

## Lemma 113 (exact child-residue transfer)

Every adjacent-block gate satisfies

\[
\boxed{2A'=n'+5-x} \tag{113.1}
\]

and

\[
\boxed{
g=n'+\ell+4-2^{\ell-1}(n'+5-x).
} \tag{113.2}
\]

In particular, when the child block is a unit block,

\[
\boxed{g=x.} \tag{113.3}
\]

### Proof

Write \(D'=n'-2U'\). Lemma 103 gives

\[
D'-3=x+2d'.
\]

Therefore

\[
\begin{aligned}
2A'
&=2U'+2d'+8\\
&=n'-D'+2d'+8\\
&=n'-(x+2d'+3)+2d'+8\\
&=n'+5-x,
\end{aligned}
\]

which proves (113.1). Lemma 83 applied to the child block gives

\[
g=n'+\ell+4-2^\ell A'.
\]

Substitution of (113.1) proves (113.2). Setting \(\ell=1\) gives
(113.3). \(\square\)

## Corollary 114 (exact unit-block gate recurrence)

Consider consecutive unit positive blocks. At the \(i\)-th start write
\((n_i,U_i)\), put \(D_i=n_i-2U_i\), let \(f_i\) be its returned residue,
and let \(r_i\) be the zero-only gap before the next positive block. Then

\[
\boxed{
\begin{aligned}
n_{i+1}&=n_i+r_i+2,\\
U_{i+1}&=U_i+1,\\
D_{i+1}&=D_i+r_i,\\
f_{i+1}&=2^{r_i+2}f_i-n_i-r_i-5.
\end{aligned}
} \tag{114.1}
\]

### Proof

The first three identities are the index, wrap-count, and \(D=n-2U\)
updates for \(k=1\). In that case the parent returns at \(m=n_i+2\), so

\[
x_i=2^{r_i+2}f_i-n_i-r_i-5.
\]

The next block is a unit block. Lemma 113 gives \(f_{i+1}=x_i\).
\(\square\)

## Corollary 115 (exact pure-upper criterion for unit gates)

For a gate in Corollary 114, the pure upper mechanism is active exactly
when

\[
\boxed{
d_i\ge2,\qquad
1\le f_{i+1}\le2^{r_i+4},\qquad
D_i+r_i-3-f_{i+1}\ge2^{r_i+4}.
} \tag{115.1}
\]

Consequently every such gate satisfies

\[
\boxed{2^{r_i+4}\le D_{i+1}-4.} \tag{115.2}
\]

### Proof

For \(k=1\), the canonical spacing is \(H_i=2^{r_i+4}\).
Lemma 113 gives \(x_i=f_{i+1}\). Thus \(j_i=0\) is exactly
\(1\le f_{i+1}\le H_i\).

Lemma 103 and \(D_{i+1}=D_i+r_i\) give

\[
2d_{i+1}
=D_{i+1}-3-x_i
=D_i+r_i-3-f_{i+1}.
\]

The upper mechanism is active exactly when \(d_i\ge2\) and
\(2d_{i+1}\ge H_i\), proving (115.1). Since \(f_{i+1}\ge1\), the last
inequality gives \(H_i\le D_{i+1}-4\), proving (115.2). \(\square\)

## Adversarial computational finding

A fixed short-transience claim for the pure upper mechanism is false.
Exact safe-map searches found a run of six consecutive pure-upper gates:

\[
\begin{array}{c|c|c|c|c|c}
n&U&e&k&r&(d,d')\\ \hline
971&5&482&6&0&(2,413)\\
978&11&277&1&1&(413,461)\\
981&12&254&1&3&(461,461)\\
986&13&256&1&3&(461,417)\\
991&14&280&1&1&(417,475)\\
994&15&252&1&5&(475,281)
\end{array}
\]

Every row has canonical translate \(j=0\) and satisfies
\(2d'\ge2^{k+r+3}\). The witness is checked directly by the Rust search
tool and by the symbolic finite-word generator. It refutes bounds below
six; it does not prove that pure-upper runs are unbounded or bounded by
six. This is a valid safe-map state, not a claim of reachability from an
original start \(b_1=m\).

## Consequence and limitation

The child excess is not merely a boundary coordinate: for a unit child it
is exactly the next returned residue. Thus a unit-block ambiguity chain is
the explicit affine recurrence (114.1), with pure-upper membership given
by the three inequalities (115.1).

This is a smaller exact subsystem for the unresolved nonunique branch.
It still permits long finite chains, and no uniform termination argument
for it is known.
