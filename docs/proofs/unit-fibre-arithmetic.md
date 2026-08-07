# Arithmetic of the all-unit C147 fibre

Scope: the **all-unit fibre only**, that is Corollary 147's recursion. Nothing
here applies to the mixed-block branch, and nothing here excludes an infinite
all-unit chain. It constrains only the *exponent data* such a chain could carry.

Throughout, an **admissible chain** is a sequence of unit states obeying

\[
f_{i+1}=2^{h_i}f_i-m_{i+1},\qquad
m_i:=n_i+3,\qquad
m_{i+1}=m_i+h_i,\qquad
G_{i+1}=G_i+h_i-2,
\tag{U.0}
\]

with \(h_i=r_i+2\ge2\) and the admissibility window

\[
1\le f_i\le G_i-3
\tag{U.1}
\]

at every index. This is (147.4) with L143's survival test; on the real fibre
\(h_i\) is the least exponent \(h\ge2\) for which the implied successor
\(f_{i+1}\) is positive.

**Exactly what the proofs use.** L148, L149 and T150 below use only integer
sequences satisfying (U.0), (U.1) and \(h_i\ge2\). They do **not** use the
unit-state congruences of L117, they do **not** use greedy minimality of
\(h_i\), and they do **not** use the additional gate windows of C115 (parent
defect, window \(M\), child headroom \(U\)). Every statement is therefore proved
for that larger class, and holds a fortiori for the real gate, whose extra tests
only shrink it. The transport identities (U.2)–(U.4) immediately below are
recorded for orientation and are *not* inputs to L148–T150.

## The transport identity

Write \(S_i:=n_i+3+f_i=m_i+f_i\). Then (U.0) is exactly

\[
\boxed{S_{i+1}=2^{h_i}f_i,}
\tag{U.2}
\]

because \(S_{i+1}=m_{i+1}+f_{i+1}=m_{i+1}+2^{h_i}f_i-m_{i+1}\). Three immediate
consequences, recorded because they are the natural place to look for a descent:

\[
v_2(S_{i+1})=h_i+v_2(f_i),
\qquad
\operatorname{odd}(S_{i+1})=\operatorname{odd}(f_i),
\qquad
4\mid S_i\ (i\ge1),
\tag{U.3}
\]

the last because \(h_i\ge2\); it is L117's congruence, rederived rather than
assumed. Also, since \(v_2(2^{h_i}f_i)=h_i+v_2(f_i)\),

\[
f_{i+1}\equiv-(n_{i+1}+3)\pmod{2^{\,h_i+v_2(f_i)}}.
\tag{U.4}
\]

These do **not** by themselves give a descent, and the reason is worth stating:
the transport (U.2) is multiplicative into \(S_{i+1}\), but \(f_{i+1}=S_{i+1}-m_{i+1}\)
is additive, so the subtraction of the moving target destroys the odd part at
every step. The results below get their leverage from *integrality* of a forced
solution instead.

## Lemma 148 (one period composes to an affine map, and forces a divisibility)

Let a chain obey (U.0) and (U.1) at every index, and suppose its exponent
sequence is eventually periodic with primitive period \(p\), so that for some
\(i_0\)

\[
h_{i_0+t}=h_t\quad(0\le t<p),
\qquad
h_{i+p}=h_i\quad(i\ge i_0).
\tag{148.0}
\]

**Fix that phase.** Put

\[
P=\sum_{t=0}^{p-1}h_t,\qquad
\sigma_0=0,\quad\sigma_t=\sum_{j=0}^{t-1}h_j,\qquad
W=\sum_{t=1}^{p}2^{\,P-\sigma_t},\qquad
V=\sum_{t=1}^{p}\sigma_t2^{\,P-\sigma_t}.
\]

Then for every \(k\ge0\)

\[
\boxed{
f_{i_0+(k+1)p}=2^{P}f_{i_0+kp}-W\,m_{i_0+kp}-V,
}
\tag{148.1}
\]

and, if the chain is infinite,

\[
\boxed{(2^{P}-1)\mid W\!\cdot\!P.}
\tag{148.2}
\]

> **The phase matters.** (148.1) is asserted only at the indices
> \(i=i_0+kp\). Starting one step later sees the *rotated* word
> \((h_1,\dots,h_{p-1},h_0)\); \(P\) is unchanged, but \(W\) and \(V\) generally
> are not. For \((4,2,5)\) the three phases give \(W=161,529,69\) — so the same
> \((W,V)\) at an unaligned index is simply false. No phase-dependent
> \(W_j,V_j\) are needed: T150 uses one phase only. The verifier carries this as
> a negative control.

### Proof

**(148.1).** Fix \(k\) and write \(i=i_0+kp\); by (148.0) the exponents
encountered from \(i\) are \(h_0,\dots,h_{p-1}\) in that order. Induct on
\(t\le p\): unfolding (U.0) introduces the target \(m_{i+t}=m_i+\sigma_t\) at
step \(t\), after which it is multiplied by
\(2^{h_t}2^{h_{t+1}}\cdots2^{h_{p-1}}=2^{\sigma_p-\sigma_t}=2^{P-\sigma_t}\).
Summing the contributions gives
\(f_{i+p}=2^Pf_i-\sum_{t=1}^{p}2^{P-\sigma_t}(m_i+\sigma_t)\), which is (148.1).
The induction uses (148.0) only along the aligned block, so it does not assert
anything at unaligned indices.

**(148.2).** Read the chain stroboscopically in that same phase:
\(F_k:=f_{i_0+kp}\) and \(M_k:=m_{i_0+kp}=M_0+kP\). By (148.1),

\[
F_{k+1}=2^{P}F_k-W(M_0+kP)-V,
\tag{148.3}
\]

a linear recurrence with constant coefficient \(2^P>1\) and inhomogeneity affine
in \(k\). Over \(\mathbb R\) its general solution is \(F_k=C\,2^{Pk}+\lambda k+\mu\)
with

\[
\lambda(2^{P}-1)=WP.
\tag{148.4}
\]

Along the same subsequence \(G\) increases by \(P-2p\ge0\) per period, so
\(G_{i_0+kp}=G_{i_0}+k(P-2p)\) is affine in \(k\); with (U.1) this gives
\(1\le F_k\le G_{i_0}+k(P-2p)-3=O(k)\). If \(C>0\) then \(F_k\) grows
exponentially and breaks the upper bound; if \(C<0\) then \(F_k\to-\infty\) and
breaks \(F_k\ge1\). Hence \(C=0\) and \(F_k=\lambda k+\mu\) for all \(k\). Every
\(F_k\) is an integer, so \(\lambda=F_1-F_0\in\mathbb Z\), and (148.4) is
(148.2). \(\square\)

Only (U.0), (U.1) and integrality are used. In particular the argument never
appeals to \(h_i\) being least, so it does not depend on the greedy rule.

## Lemma 149 (a periodic binary block has a periodic cyclic gap word)

Let \(B\) be a \(P\)-bit binary word, \(P\ge1\), with one-bit set
\(S\subseteq\mathbb Z/P\), \(|S|=p\ge1\), read cyclically. Define its **cyclic
gap word** \((g_0,\dots,g_{p-1})\) by listing \(S\) in cyclic order and taking
successive cyclic differences, so \(\sum g_t=P\).

Then \(B\) has a period \(d_0\mid P\) with \(d_0<P\) **if and only if** the
cyclic gap word is a repetition of a strictly shorter word. Equivalently:

\[
\text{the cyclic gap word is primitive}
\iff
B\text{ has minimal period }P.
\tag{149.0}
\]

### Proof, forward direction

Assume \(B\) has period \(d_0\mid P\), \(d_0<P\).

Periodicity of \(B\) with period \(d_0\) says \(S+d_0=S\) in \(\mathbb Z/P\).
Let \(e=P/d_0>1\). Translation \(\tau:x\mapsto x+d_0\) has order \(e\) in
\(\mathbb Z/P\) and acts freely (for \(0<k<e\), \(kd_0\not\equiv0\)), so it acts
freely on \(S\); hence \(e\mid p\) and \(c:=p/e<p\).

The \(e\) intervals \([kd_0,(k+1)d_0)\), \(k=0,\dots,e-1\), partition
\(\mathbb Z/P\), and \(\tau\) carries each onto the next, so each contains the
same number \(c=p/e\) of elements of \(S\). Since \(\tau\) is a rotation it
preserves the cyclic order of \(S\), and it advances the cyclically sorted list
by exactly \(c\) positions. Writing \(s_{t+c}=s_t+d_0\) (indices mod \(p\),
positions mod \(P\)) gives \(g_{t+c}=g_t\) for every \(t\). So the gap word has
period \(c<p\).

### Proof, converse direction

Assume the cyclic gap word \((g_0,\dots,g_{p-1})\) has a proper period
\(c\mid p\), \(c<p\). Put

\[
d=g_0+g_1+\cdots+g_{c-1}.
\]

Because the same \(c\)-gap block repeats \(p/c\) times and the gaps sum to
\(P\),

\[
P=\frac pc\,d,
\qquad\text{so}\qquad
0<d<P
\]

since \(p/c\ge2\). Listing the one-bits in cyclic order as \(s_0,\dots,s_{p-1}\),
periodicity of the gap word gives
\(s_{t+c}-s_t=g_t+\cdots+g_{t+c-1}=d\) for every \(t\) (the sum telescopes and is
the same \(d\) for each \(t\), again by \(g_{t+c}=g_t\)). Hence translation by
\(d\) carries each one-bit to the one-bit \(c\) positions later in cyclic order,
so

\[
S+d=S \pmod P,
\]

which says exactly that \(B\) has period \(d\), and \(d<P\) is proper.
\(\square\)

Together the two directions give (149.0). Only the forward direction is used by
T150; the converse is recorded because the bridge (149.2) below states an
equivalence and is regression-tested as one.

**Bridge.** For the word of Lemma 148, \(W\) has one-bits exactly at the
positions \(\{P-\sigma_t: 1\le t\le p\}\subseteq[0,P-2]\); bit \(0\) is set
(\(t=p\)) and bit \(P-1\) is not (\(\sigma_1=h_0\ge2\)). Listing them in
increasing order from \(0\) and taking cyclic differences returns

\[
(h_{p-1},h_{p-2},\dots,h_1,h_0),
\tag{149.1}
\]

the **reversal** of the exponent word — not the word itself. The orientation
matters and is easy to get backwards; it is checked mechanically by the
verifier. Since a finite word is primitive if and only if its reversal is
primitive, and if and only if each of its rotations is primitive, (149.1)
identifies "cyclic gap word primitive" with "exponent word primitive". Feeding
that into the equivalence (149.0) gives

\[
(h_0,\dots,h_{p-1})\ \text{primitive}
\iff
\text{the }P\text{-bit block of }W\text{ has minimal period }P.
\tag{149.2}
\]

## Theorem 150 (the exponent sequence cannot be eventually periodic)

No infinite admissible all-unit chain has an eventually periodic exponent
sequence \((h_i)\). Equivalently, the exponent data of any infinite admissible
all-unit chain is genuinely aperiodic.

### Proof

Suppose such a chain exists. Take the **primitive** period word
\((h_0,\dots,h_{p-1})\), \(p\ge1\), and let \(P,W\) be as in Lemma 148. Put
\(d=2^{P}-1\).

Bit \(0\) of \(W\) is set, so \(W\ge1\). The one-bit positions have consecutive
gaps \(\ge2\) and lie in \([0,P-2]\), so
\(W\le\sum_{t\ge1}2^{P-2t}<2^{P}/3\), and as \(W\) is an integer,
\(W\le(2^{P}-1)/3=d/3\). Hence

\[
0<\frac Wd\le\frac13<1 .
\tag{150.1}
\]

By Lemma 148, \(a:=PW/d\in\mathbb Z\), and \(W/d=a/P\). Reduce this rational to
lowest terms, \(W/d=a/P=u/q\) with \(\gcd(u,q)=1\). Reducing the two
representations of the same fraction gives

\[
q=\frac{P}{\gcd(a,P)}=\frac{d}{\gcd(W,d)} .
\tag{150.2}
\]

The first expression gives \(q\le P\); the second gives \(q\mid d=2^P-1\), so
\(q\) is **odd**; and \(q>1\), since \(q=1\) would make \(W/d\) an integer,
contradicting (150.1).

Let \(d_0=\operatorname{ord}_q(2)\), which exists because \(q\) is odd. From
\(q\mid2^{P}-1\) we get \(2^{P}\equiv1\pmod q\), hence \(d_0\mid P\). Suppose
\(d_0=P\). Then \(P=\operatorname{ord}_q(2)\) divides \(\varphi(q)\), so
\(P\le\varphi(q)\le q-1\), that is \(q\ge P+1\), contradicting \(q\le P\).
Therefore

\[
d_0\mid P,\qquad d_0<P .
\tag{150.3}
\]

Because \(q\) is odd, the **real** binary expansion of \(u/q\in(0,1)\) is purely
periodic with minimal period exactly \(d_0\). (No 2-adic expansion is used
anywhere; the series below converges in \(\mathbb R\).) On the other hand
\(0<W<2^{P}\) gives

\[
\frac Wd=\frac{W}{2^{P}-1}=\sum_{k\ge1}W2^{-kP},
\]

whose binary expansion is purely periodic with repetend the \(P\)-bit block of
\(W\). A purely periodic sequence with minimal period \(d_0\) admits a period
\(P\) only if \(d_0\mid P\), and then its \(P\)-block is the \(d_0\)-block
repeated \(P/d_0\) times. By (150.3) that repetition is proper, so the \(P\)-bit
block of \(W\) has minimal period at most \(d_0<P\).

By Lemma 149 the cyclic gap word of that block is a repetition of a shorter
word, and by (149.1)–(149.2) so is the exponent word \((h_0,\dots,h_{p-1})\).
That contradicts primitivity of the period. \(\square\)

### What this subsumes, and what it does not

It **subsumes** three weaker statements that were proved first and are now
special cases:

* *eventually constant exponent* — the case \(p=1\), where \(W=1\) and (148.2)
  reads \((2^{h}-1)\mid h\), impossible for \(h\ge2\) since \(0<h/(2^h-1)<1\);
* *prime \(P\)* — then \(\gcd(2^P-1,P)=1\) by Fermat, and (150.2) would force
  \(q=d>P\);
* the exhaustive machine search over \(P\le400\), which is now a regression
  check rather than evidence.

It does **not** prove any of the following, and none should be read into it:

* that an infinite admissible all-unit chain does not exist — the theorem
  constrains only what its exponent data could look like;
* anything about **bounded aperiodic** or **unbounded aperiodic** exponent
  sequences, which remain entirely open and are the actual C147 obstruction;
* anything about the mixed-block branch, where \(k_i\ge2\) occurs;
* any bound on \(C=\max_i(n_i-2U_i)\), so T145 is not upgraded.

The C147 obstruction — a one-dimensional expanding recursion aimed at a moving
admissible window — is narrowed, not resolved.

## Verification

`independent/verify_unit_fibre_periodicity.py` is an **independent arithmetic
verifier plus a replay against the existing exact gate implementation**. The
arithmetic — composition, \(W\) and \(V\), orientation, binary periods,
divisibility — is rederived from the recurrence alone; only the final transport
replay imports `gate` and `is_unit_state` from `unit_gap_words_core`, so that
part is a cross-check against the existing implementation rather than an
independent one. Specifically it:

* it recomputes \(W\) and \(V\) by finite differencing the composed map, rather
  than trusting the closed form, and compares against (148.1);
* it checks the orientation (149.1) explicitly, including the reversal, on words
  chosen so that a rotation-only convention would fail;
* it checks (150.2), \(d_0\mid P\), \(d_0<P\), and that the \(P\)-block of \(W\)
  really is the \(d_0\)-block repeated;
* it checks Lemma 149 and the equivalence (149.2) by brute force over every
  admissible exponent word up to a bound;
* it confirms every word satisfying (148.2) up to a bound is a non-primitive
  repetition, which is the regression form of the old search;
* it replays (U.2)–(U.4) against the project's own gate map, so the transport
  identity is checked on the same transitions K18 and K19 were built from.

The bounded searches are **regression and falsification data**. They are not
part of the proof of Theorem 150, which is unconditional in \(P\).
