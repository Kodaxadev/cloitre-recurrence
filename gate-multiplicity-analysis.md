# Exact multiplicity of arbitrary safe-block gates

## Scope

Lemma 92 classifies when an adjacent-block gate is unique. The same lattice
coordinates determine the exact number of locally valid parent states.
This quantifies nonuniqueness but does not exclude it along an infinite
path.

Retain the notation of Lemmas 92 and 103. Thus \(f\) is the realized
returned residue, \(e\) is the parent residue, \(d,d'\) are the parent and
child defects,

\[
x=\rho+jH,\qquad H=2^{k+r+3},
\]

with \(1\le\rho\le H\) and \(j\ge0\). Let \(\mathcal F\) be the exact gate
candidate set from Corollary 84.

## Lemma 110 (exact gate multiplicity)

Put

\[
\lambda=\min\{e-1,j\},\qquad
\mu=\min\left\{\left\lfloor\frac d2\right\rfloor,
\left\lfloor\frac{2d'}H\right\rfloor\right\}.
\]

Then

\[
\boxed{
\mathcal F=
\{f+t2^{k+1}:-\lambda\le t\le\mu\},
\qquad
|\mathcal F|=1+\lambda+\mu.
} \tag{110.1}
\]

Thus the lower-candidate depth is limited independently by the canonical
window translate \(j\) and the parent residue headroom \(e-1\). The
upper-candidate depth is limited independently by the parent defect
headroom \(d/2\) and child defect headroom \(2d'/H\).

### Proof

Every candidate has the form

\[
f_t=f+t2^{k+1},\qquad t\in\mathbb Z.
\]

The corresponding parent overshoot, parent defect, and child excess are

\[
A_t=A-2t,\qquad d_t=d-2t,\qquad x_t=x+tH. \tag{110.2}
\]

Corollary 84's exact reconstruction says that \(f_t\) is admissible exactly
when the parent and child interval bounds hold. The parent bounds

\[
U+4\le A_t\le n+2
\]

are equivalent to

\[
t\le\left\lfloor\frac d2\right\rfloor,
\qquad
t\ge1-e,
\]

because \(A=n+4-2e\). The child bounds are

\[
1\le x_t\le G+r-3.
\]

Since \(x=\rho+jH\), the lower bound is exactly \(t\ge-j\). By (92.2),
the upper bound is exactly

\[
t\le\left\lfloor\frac{G+r-3-x}{H}\right\rfloor
=\left\lfloor\frac{2d'}H\right\rfloor.
\]

Intersecting the two integer intervals gives

\[
-\min\{e-1,j\}\le t\le
\min\left\{\left\lfloor\frac d2\right\rfloor,
\left\lfloor\frac{2d'}H\right\rfloor\right\},
\]

which proves (110.1). \(\square\)

## Corollary 111 (multiplicity consumes window displacement)

Every gate satisfies

\[
\boxed{
\bigl(|\mathcal F|-1\bigr)H
\le D'-3-\rho.
} \tag{111.1}
\]

### Proof

Lemma 110 gives

\[
\bigl(|\mathcal F|-1\bigr)H=(\lambda+\mu)H.
\]

Here \(\lambda\le j\) and \(\mu H\le2d'\). Lemma 103 gives

\[
D'-3-\rho=jH+2d',
\]

so (111.1) follows. \(\square\)

## Consequence and limitation

The first later-window miss contributes one lower alternative unless the
parent residue has no headroom; positive blocks in fact have \(e\ge2\).
Additional missed windows need not create additional candidates because
the parent state window can truncate them. Likewise a large child defect
creates upper alternatives only while the parent defect remains available.

This exact truncation explains why canonical-window displacement alone
cannot force arbitrarily large gate multiplicity. A closing argument still
needs an inter-gate budget showing that repeated displacement cannot be
continually absorbed by the two parent headrooms.
