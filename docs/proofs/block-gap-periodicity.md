# Periodic block-gap data on the full block chain

**Scope.** This note concerns infinite chains of adjacent returning positive
blocks under the exact map \(\Psi\) of Theorem 137. It excludes eventual
periodicity of the joint block-length/gap data \((k_i,r_i)\). It does **not**
prove termination.

The statement covers **arbitrary positive block lengths** \(k_i\ge1\), not only
pure-upper gates and not only the unit fibre \(k_i\equiv1\). Theorem 150 is the
unit-fibre specialization, recovered in the last section; its proof is not
repeated here.

Throughout, an **admissible chain** is a sequence of adjacent returning positive
blocks obeying (137.2),

\[
f_{i+1}=2^{\,k_{i+1}+r_i+1}f_i-\bigl(2^{k_{i+1}}-1\bigr)(n_{i+1}+4)+k_{i+1},
\tag{B.0}
\]

together with the coordinate recurrences and the admissibility window

\[
n_{i+1}=n_i+k_i+1+r_i,
\qquad
U_{i+1}=U_i+k_i,
\qquad
G_i=n_i-2U_i,
\qquad
1\le f_i\le G_i-3,
\tag{B.1}
\]

the last being C144 read at every index. Only (B.0), (B.1), integrality, and —
in one case — T145 are used below.

## Step data

Fix a phase and write, with all indices cyclic modulo \(p\),

\[
x_t:=k_{t+1},
\qquad
z_t:=r_t+1\ \ (\ge1),
\qquad
a_t:=x_t+z_t,
\qquad
A_t:=\sum_{s=0}^{t}a_s,
\qquad
P:=A_{p-1}.
\tag{B.2}
\]

Because the \(k\)'s are summed cyclically, \(\sum_t k_{t+1}=\sum_t k_t\), hence

\[
\boxed{
P=\sum_{t}(k_{t+1}+r_t+1)=\sum_{t}(k_t+r_t+1).
}
\tag{B.3}
\]

So \(P\) is **simultaneously** the total doubling exponent of the composed
residue map (the left sum, from (B.0)) and the total increase of the block-start
index over one period (the right sum, from (B.1)):
\(n_{i_0+(j+1)p}=n_{i_0+jp}+P\). Both readings are used.

## Lemma 151 (aligned period composition, and a divisibility)

Let an admissible chain have eventually periodic joint data: for some \(i_0\) and
primitive period word \((k_0,r_0),\dots,(k_{p-1},r_{p-1})\),

\[
(k_{i_0+t},r_{i_0+t})=(k_t,r_t)\quad(0\le t<p),
\qquad
(k_{i+p},r_{i+p})=(k_i,r_i)\quad(i\ge i_0).
\tag{151.0}
\]

**Fix that phase.** With \(F_j:=f_{i_0+jp}\) and \(N_j:=n_{i_0+jp}+4\), for every
\(j\ge0\)

\[
\boxed{
F_{j+1}=2^{P}F_j-W N_j-V,
}
\qquad
\boxed{
W=\sum_{t=0}^{p-1}\bigl(2^{x_t}-1\bigr)2^{\,P-A_t},
}
\tag{151.1}
\]

\[
\boxed{
V=\sum_{t=0}^{p-1}\Bigl[\bigl(2^{x_t}-1\bigr)B_t-x_t\Bigr]2^{\,P-A_t},
\qquad
B_t:=\sum_{s=0}^{t}(k_s+r_s+1),
}
\tag{151.2}
\]

and if moreover the budget drift

\[
D:=\sum_{t=0}^{p-1}(r_t+1-k_t)
\]

is **positive**, then

\[
\boxed{(2^{P}-1)\mid W\!\cdot\!P.}
\tag{151.3}
\]

> **Two different prefixes occur, and they are not equal.** \(A_t\) is the
> *multiplier* prefix: it collects the exponents \(a_s=k_{s+1}+r_s+1\) that still
> have to be applied after step \(t\). \(B_t\) is the *block-start* prefix: it is
> the amount by which the index has advanced, \(n_{i+t+1}+4=N_j+B_t\), and it
> collects \(k_s+r_s+1\). They differ by \(B_t=A_t+k_0-k_{t+1}\), so they agree
> exactly when the block lengths are constant — which is why the unit fibre does
> not detect a confusion between them. \(W\) uses \(A_t\) only and is unaffected.

> **The phase is load-bearing.** (151.1) is asserted only at the aligned indices
> \(i_0+jp\). A rotated phase has the same \(P\), by (B.3), but generally a
> different \(W\) and \(V\); the verifier carries an asymmetric word as a negative
> control. No phase-dependent \(W_j,V_j\) are needed, because one phase suffices.

### Proof

**(151.1).** Fix \(j\) and write \(i=i_0+jp\); by (151.0) the data met from \(i\)
are \((k_0,r_0),\dots,(k_{p-1},r_{p-1})\) in that order. Unfolding (B.0) once
introduces the term \(-(2^{x_t}-1)(n_{(t+1)}+4)+x_t\) at step \(t\), after which
it is multiplied by \(2^{a_{t+1}}\cdots2^{a_{p-1}}=2^{P-A_t}\). Summing,

\[
F_{j+1}=2^{P}F_j-\sum_{t}\bigl(2^{x_t}-1\bigr)\bigl(n_{(t+1)}+4\bigr)2^{P-A_t}
+\sum_{t}x_t2^{P-A_t}.
\]

By (B.1) the index advances by \(k_s+r_s+1\) at step \(s\), so
\(n_{(t+1)}+4=N_j+B_t\) — an affine function of \(N_j\) with coefficient \(1\).
Collecting the \(N_j\) coefficient gives \(W\) as displayed, which uses the
multiplier prefix \(A_t\) only; the remaining constants give \(V\) as in (151.2),
which uses the block-start prefix \(B_t\). The induction runs only along the
aligned block, so nothing is asserted off-phase.

Note that the \(+k_{i+1}=+x_t\) term of (B.0) is an additive constant: it never
multiplies \(N_j\), so it contributes to \(V\) alone and **does not enter \(W\)**.
The divisibility below is therefore untouched by it.

**(151.3).** Read the chain stroboscopically in the same phase. By (B.3),
\(N_j=N_0+jP\), so (151.1) is

\[
F_{j+1}=2^{P}F_j-W\bigl(N_0+jP\bigr)-V,
\tag{151.4}
\]

a linear recurrence with constant coefficient \(2^{P}>1\) and inhomogeneity
affine in \(j\). Over \(\mathbb R\) its general solution is
\(F_j=C\,2^{Pj}+\lambda j+\mu\) with

\[
\lambda(2^{P}-1)=WP.
\tag{151.5}
\]

By L143, \(G_{i+1}-G_i=r_i+1-k_i\), so along the aligned subsequence
\(G_{i_0+jp}=G_{i_0}+jD\). Since \(D>0\) by hypothesis this is a genuine linear
*upper* window growing with \(j\), and with (B.1),
\(1\le F_j\le G_{i_0}+jD-3=O(j)\). Narrowing (151.3) to \(D>0\) is deliberate:
it is exactly what T153 consumes, and it avoids presenting a decreasing bound as
ordinary asymptotic control in a case that is anyway vacuous. If
\(C>0\) then \(F_j\) grows exponentially and breaks the upper bound; if \(C<0\)
then \(F_j\to-\infty\) and breaks \(F_j\ge1\). Hence \(C=0\), so
\(F_j=\lambda j+\mu\) for all \(j\), and \(\lambda=F_1-F_0\in\mathbb Z\). With
(151.5) this is (151.3). \(\square\)

## Lemma 152 (cyclic run lengths detect a proper binary period)

Let \(B\) be a \(P\)-bit binary word, read cyclically, containing **both** digits.
Its one-bits and zero-bits fall into maximal cyclic runs, alternating; let its
**cyclic run-pair word** be the sequence of pairs (length of a one-run, length of
the zero-run that follows it), read in cyclic order. Then

\[
\boxed{
B\text{ has a period }d_0\mid P,\ d_0<P
\iff
\text{its cyclic run-pair word is nonprimitive.}
}
\tag{152.1}
\]

### Proof

**(\(\Rightarrow\))** Let \(\tau:x\mapsto x+d_0\) on \(\mathbb Z/P\). Since
\(B\) has period \(d_0\), \(\tau\) preserves \(B\), hence preserves the transition
set \(\{i:b_i\ne b_{i+1}\}\); and since it preserves digit values it carries
one-runs to one-runs and zero-runs to zero-runs. So \(\tau\) permutes the set
\(S_1\) of **starts of one-runs**, where \(|S_1|=p\) is the number of run pairs.

The shift count is then obtained by counting, not by freeness. The \(e=P/d_0\)
half-open intervals \([jd_0,(j+1)d_0)\), \(0\le j<e\), partition \(\mathbb Z/P\),
and \(\tau\) carries each onto the next. Hence every interval contains the same
number of elements of \(S_1\), namely

\[
c:=\frac pe,
\]

so in particular \(e\mid p\), and \(c<p\) because \(e>1\). Since \(\tau\) is a
rotation it preserves the cyclic order of \(S_1\), so it advances the cyclically
ordered list of one-run starts by exactly \(c\) positions — equivalently, it
advances the run-pair word by exactly \(c\) pairs. As \(\tau\) fixes the word,
the run-pair word has period \(c<p\).

**(\(\Leftarrow\))** Suppose the run-pair word has a proper period \(c\mid p\),
\(c<p\). Let \(d\) be the total bit length of the first \(c\) pairs. Since the
\(c\)-pair block repeats \(p/c\ge2\) times and the pairs exhaust the \(P\) bits,
\(P=(p/c)d\), so \(0<d<P\). Translation by \(d\) carries each run onto the run
\(c\) pairs later, which has the same length and the same digit; since the runs
partition \(\mathbb Z/P\), that translation preserves \(B\). So \(B\) has the
proper period \(d\). \(\square\)

Runs split across the visible \(P\)-bit boundary need no special case: the whole
statement is cyclic, and the boundary is not part of the data.

## The run structure of \(W\)

Each summand \((2^{x_t}-1)2^{P-A_t}\) of (151.1) is a block of exactly \(x_t\)
consecutive one-bits occupying positions \([P-A_t,\;P-A_t+x_t-1]\). Consecutive
blocks are separated, because the gap between block \(t\) and block \(t+1\) is
\(z_{t+1}\ge1\) zero-bits; the top block leaves \(z_0\ge1\) zeros above it, and
bit \(0\) is set by the last block. Hence \(W\) is odd, \(W<2^{P-1}\), and
reading the \(P\)-bit word cyclically from high to low starting at a one-run, the
alternating run pairs are exactly

\[
\boxed{
(k_1,r_1+1),\ (k_2,r_2+1),\ \dots,\ (k_{p-1},r_{p-1}+1),\ (k_0,r_0+1),
}
\tag{152.2}
\]

a cyclic rotation of \((k_0,r_0+1),\dots,(k_{p-1},r_{p-1}+1)\). Since
\(r\mapsto r+1\) is a bijection applied coordinatewise, and primitivity of a
finite word is invariant under rotation, we get

\[
(k_t,r_t)_{t}\ \text{primitive}
\iff
\text{the }P\text{-bit block of }W\text{ has minimal period }P.
\tag{152.3}
\]

Two orientation choices here are *not* free, and the verifier carries asymmetric
witnesses that reject both mutations. First, a one-run must be paired with the
zero-run that **follows** it; pairing it with the preceding zero-run gives a
different cyclic word. Second, the run list must be read in one fixed cyclic
**direction**; reading it the other way returns the reversal, which is generally
not a rotation of the forward word.

What is *not* a hazard is the index shift: \((k_{t+1},r_{t+1}+1)_t\) is the
left rotation by one of \((k_t,r_t+1)_t\), and since (152.3) compares words only
up to rotation, the two readings are interchangeable. The shift visible in
(152.2) is therefore cosmetic, and (152.3) may be applied to either.

## Theorem 153 (no eventually periodic block-gap data)

No infinite admissible chain of adjacent returning positive blocks has eventually
periodic joint data \((k_i,r_i)\).

### Proof

Suppose one does. Take the primitive period word, \(p\ge1\), and let
\(P,W,D\) be as above. Three cases.

**\(D<0\).** By L143, \(G_{i_0+jp}=G_{i_0}+jD\to-\infty\). But (B.1) gives
\(f\ge1\) and \(f\le G-3\), so \(G_i\ge4\) at every index. Contradiction.

**\(D=0\).** Then \(G_{i_0+jp}=G_{i_0}\) for all \(j\), and within a period the
increments \(r_t+1-k_t\) repeat, so for \(0\le t<p\) the value
\(G_{i_0+jp+t}=G_{i_0}+\sum_{s<t}(r_s+1-k_s)\) is independent of \(j\). Hence
\(\sup_iG_i=\max_{t<p}G_{i_0+t}<\infty\) over the whole tail, and taking the
maximum with the finite prefix, \(C:=\sup_iG_i<\infty\). T145 then bounds every
chain of \(N\ge2\) consecutive positive blocks by \(N\le3C-13\), a finite number,
contradicting an infinite chain.

**\(D>0\).** This is the case L151 was built for. By (151.3),
\(a:=PW/d\in\mathbb Z\) where \(d=2^{P}-1\), and \(W/d=a/P\).

Every \(k_i\ge1\) gives \(W\) at least one one-bit, and every \(r_i+1\ge1\) gives
at least one zero-bit; with \(W<2^{P-1}\) this yields \(0<W<d\). Reduce
\(W/d=a/P=u/q\) to lowest terms; reducing the two representations of one
fraction,

\[
q=\frac{P}{\gcd(a,P)}=\frac{d}{\gcd(W,d)}.
\tag{153.1}
\]

The first gives \(q\le P\); the second gives \(q\mid2^{P}-1\), so \(q\) is odd;
and \(q>1\), since \(q=1\) would make \(W/d\) an integer, impossible as
\(0<W<d\).

Let \(d_0=\operatorname{ord}_q(2)\), which exists because \(q\) is odd. From
\(q\mid2^{P}-1\) we get \(d_0\mid P\). If \(d_0=P\) then \(P\mid\varphi(q)\), so
\(P\le\varphi(q)\le q-1\), i.e. \(q\ge P+1\), contradicting \(q\le P\). Hence

\[
d_0\mid P,\qquad d_0<P.
\tag{153.2}
\]

Because \(q\) is odd, the **real** binary expansion of \(u/q\in(0,1)\) is purely
periodic with minimal period exactly \(d_0\). (Nothing here is 2-adic; the series
converges in \(\mathbb R\).) On the other hand \(0<W<2^{P}\) gives
\(W/d=\sum_{m\ge1}W2^{-mP}\), whose expansion is purely periodic with repetend
the \(P\)-bit block of \(W\). A purely periodic sequence of minimal period
\(d_0\) admits the period \(P\) only if \(d_0\mid P\), and then its \(P\)-block is
the \(d_0\)-block repeated \(P/d_0\) times; by (153.2) that repetition is proper.

So the \(P\)-bit block of \(W\) has a proper period. It contains both digits, so
L152 makes its cyclic run-pair word nonprimitive, and by (152.2)–(152.3) the
joint period word \((k_t,r_t)\) is nonprimitive. That contradicts primitivity of
the period. \(\square\)

### What is left open

Theorem 153 constrains the *shape* of the data an infinite chain could carry. It
does not prove termination, and none of the following is excluded:

* infinite chains with **bounded but aperiodic** joint data;
* infinite chains with **unbounded aperiodic** joint data;
* general nonperiodic budget excursions — no bound on \(C=\sup_i G_i\) follows,
  so T145 is not upgraded;
* the stabilization conjecture itself.

## Theorem 150 as the unit-fibre specialization

Put \(k_i\equiv1\). Then \(x_t\equiv1\), each one-run of \(W\) has length one, and
(152.2) reads \((1,r_1+1),\dots,(1,r_0+1)\): the binary word is a single one
followed by \(r_i+1\) zeros, repeated. The cyclic distance between successive
one-bits is therefore

\[
1+(r_i+1)=r_i+2=h_i,
\]

which is exactly the gap word of T150, and \(W\) collapses to T150's coefficient
under \(h_i=r_i+2\). L152 specializes to L149, and Theorem 153 specializes to
Theorem 150. The verifier checks this as a numerical identity on \(W\), not
merely as agreement of verdicts. T150's proof is not repeated.

## Verification

`independent/verify_block_gap_periodicity.py` is an independent arithmetic
verifier. It recovers \(2^{P}\), \(W\) and \(V\) by finite differencing the
composed map and compares **all three** against the closed forms above, so
(151.2) is genuinely checked rather than merely fitted. It carries the asymmetric
witness \((k,r)=\bigl((2,0),(1,2),(4,1)\bigr)\), where \(V=5749\) while the
\(A_t\)-for-\(B_t\) confusion would give \(5515\). It checks the phase control on
an asymmetric mixed word; reconstructs the cyclic run-pair word and requires the
rotation (152.2), with two independent mutations that must fail — pairing a
one-run with the **preceding** zero-run, and a literal **reverse-direction** run
parser; brute-forces both directions of L152; confirms the T150 coefficient
identity; and searches primitive period words for (151.3).

That last search is **regression only**. Theorem 153 is unconditional in \(P\)
and does not rest on it.
