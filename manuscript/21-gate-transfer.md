# Residue transfer through a gate

Retain the notation of the preceding section. A parent gate reaches a
child positive-block start \((n',U',e')\), whose block has length
\(\ell\), overshoot \(A'=n'+4-2e'\), and returned residue \(g\).

## Lemma 113 (child-residue transfer)

Every gate satisfies

\[
2A'=n'+5-x
\]

and

\[
g=n'+\ell+4-2^{\ell-1}(n'+5-x).
\tag{21.1}
\]

Hence \(g=x\) whenever \(\ell=1\).

### Proof

Put \(D'=n'-2U'\). From \(D'-3=x+2d'\) and
\(A'=U'+d'+4\),

\[
2A'=n'-D'+2d'+8=n'+5-x.
\]

The returned-residue identity
\(g=n'+\ell+4-2^\ell A'\) now gives (21.1). \(\square\)

## Corollary 114 (unit-block recurrence)

For consecutive unit positive blocks, let \((n_i,U_i)\) be the starts,
\(D_i=n_i-2U_i\), \(f_i\) the returned residues, and \(r_i\) the
intervening zero-only gaps. Then

\[
\begin{aligned}
n_{i+1}&=n_i+r_i+2,&
U_{i+1}&=U_i+1,\\
D_{i+1}&=D_i+r_i,&
f_{i+1}&=2^{r_i+2}f_i-n_i-r_i-5.
\end{aligned}
\tag{21.2}
\]

### Proof

The first three formulas are the elementary index and wrap updates.
For a unit parent, \(m=n_i+2\), so its child excess is the last
expression in (21.2). Lemma 113 identifies that excess with the next
unit block's returned residue. \(\square\)

## Corollary 115 (pure-upper unit criterion)

The pure upper mechanism is active at the \(i\)-th gate exactly when

\[
d_i\ge2,\qquad
1\le f_{i+1}\le2^{r_i+4},\qquad
D_i+r_i-3-f_{i+1}\ge2^{r_i+4}.
\tag{21.3}
\]

In particular,

\[
2^{r_i+4}\le D_{i+1}-4.
\tag{21.4}
\]

### Proof

For \(k=1\), the canonical spacing is \(H_i=2^{r_i+4}\), and Lemma
113 gives \(x_i=f_{i+1}\). Thus the first canonical window is the
middle inequality in (21.3). Also

\[
2d_{i+1}=D_{i+1}-3-x_i
=D_i+r_i-3-f_{i+1}.
\]

The exact upper-candidate test proves (21.3); (21.4) follows from
\(f_{i+1}\ge1\). \(\square\)

The recurrence is exact but not terminating by inspection. A verified
safe path contains six consecutive pure-upper gates, five of whose parent
blocks are unit blocks. Thus no shorter uniform-transience claim is
available.
