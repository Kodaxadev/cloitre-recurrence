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
\mu=\min\left\{\left\lfloor\frac d2\right\rfloor,
\left\lfloor\frac{2d'}H\right\rfloor\right\}.
\]

Then

\[
\boxed{
\mathcal F=
\{f+t2^{k+1}:-j\le t\le\mu\},
\qquad
|\mathcal F|=1+j+\mu.
} \tag{110.1}
\]

Thus every missed canonical window contributes one lower candidate. Only
the upper-candidate depth is truncated: independently by the parent defect
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
\max\{1-e,-j\}\le t\le
\min\left\{\left\lfloor\frac d2\right\rfloor,
\left\lfloor\frac{2d'}H\right\rfloor\right\},
\]

It remains to compare the two lower endpoints. Substituting
\(A=n+4-2e\), \(m=n+k+1\), and
\(f=m+3-2^kA\) into \(x\) gives

\[
eH-x=
2^{r+2}\bigl((2^k-1)n+2^{k+2}-k-4\bigr)
+n+k+r+4>0. \tag{110.3}
\]

Therefore \(x\le eH\). Since \(x=\rho+jH\) with \(\rho\ge1\), this forces
\(j\le e-1\), so \(\max\{1-e,-j\}=-j\). This proves (110.1). \(\square\)

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
\bigl(|\mathcal F|-1\bigr)H=(j+\mu)H.
\]

Here \(\mu H\le2d'\). Lemma 103 gives

\[
D'-3-\rho=jH+2d',
\]

so (111.1) follows. \(\square\)

## Consequence and limitation

Every later-window miss contributes exactly one lower alternative. Thus
unbounded canonical translate \(j\) forces unbounded gate multiplicity.
A large child defect, however, creates upper alternatives only while the
parent defect remains available.

The unresolved escape is consequently narrower: displacement stored in
\(2d'\), rather than in \(jH\), can still be truncated by the parent defect
headroom. A closing argument needs an inter-gate budget showing that this
defect storage cannot be continually replenished.

## Corollary 112 (upper nonuniqueness forces a two-block ceiling)

Suppose the upper-candidate mechanism is active:

\[
d\ge2,\qquad 2d'\ge H.
\]

If the child positive block has length \(\ell\ge1\) and starts at index
\(n'\), then

\[
\boxed{
2^{k+r+\ell+2}<n'+\ell+4.
} \tag{112.1}
\]

### Proof

At the child start put \(A'=U'+d'+4\). Lemma 53's failed stopping test
immediately before its length-\(\ell\) block gives

\[
2^\ell A'<n'+\ell+4.
\]

The upper-candidate hypothesis gives \(d'\ge H/2\), so

\[
2^{\ell-1}H\le2^\ell d'<2^\ell A'<n'+\ell+4.
\]

Since \(H=2^{k+r+3}\), this is (112.1). \(\square\)

This ceiling couples two consecutive positive blocks, but remains
compatible with logarithmic total block/gap complexity.
