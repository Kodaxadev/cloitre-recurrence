# 1. Foundations and the attainable-increment spectrum

Write

\[
b_n=q_n n+r_n,\qquad 0\le r_n<n,
\]

and define \(e_n=r_n-q_n\) and \(a_n=q_{n+1}-q_n\). Since \(b_2=m\),
index \(2\) is the natural initial index. Direct substitution gives

\[
q_{n+1}=q_n+\left\lfloor\frac{2r_n-q_n}{n+1}\right\rfloor,\qquad
r_{n+1}=(2r_n-q_n)\bmod(n+1). \tag{1.1}
\]

## Theorem 1 (absorption)

For a fixed index \(t\), the following are equivalent:

1. \(b_{n+1}-b_n=c\) for every \(n\ge t\);
2. \(b_t=c(t+1)\) with \(0\le c<t\);
3. \(q_t=r_t=c\).

### Proof

If \(q_t=r_t=c\), then \(b_t=ct+c=c(t+1)\). If
\(b_n=c(n+1)\) with \(c<n\), then \(b_n\bmod n=c\), so
\(b_{n+1}=c(n+2)\); induction proves constant increment \(c\).

Conversely, constant increment gives \(r_n=c\) and
\(b_n=b_t+c(n-t)\). Thus

\[
q_n=c+\frac{b_t-ct-c}{n}.
\]

The left side is integral for every sufficiently large \(n\), while the
fraction tends to zero. Its numerator must vanish, so
\(b_t=c(t+1)\), and \(c=r_t<t\). \(\square\)

## Lemma 3 (entry)

Every orbit reaches an index \(n_0\le\lceil\sqrt{2m}\rceil+2\) such that
\(b_{n_0}<n_0^2\). Once this inequality holds it continues to hold.

### Proof

Let \(f(n)=b_n-n^2\). Since \(r_n\le n-1\),

\[
f(n+1)-f(n)=r_n-(2n+1)\le-(n+2)<0.
\]

Starting at \(f(2)=m-4\), summing this decrease proves entry by the stated
bound. Strict decrease proves forward invariance. An absorbing state cannot
be skipped, because \(b_n=c(n+1)\), \(c<n\), implies \(b_n<n^2\).
\(\square\)

## Lemma 4 (bounded quotient)

After entry, \(a_n\in\{-1,0,1\}\), and \(q_n\le n\) is forward invariant.

### Proof

Put \(d=2r_n-q_n\). If \(q_n\le n\), then

\[
-(n+1)<d<2(n+1).
\]

Equation (1.1) therefore makes its quotient correction one of
\(-1,0,1\), and \(q_{n+1}\le q_n+1\le n+1\). \(\square\)

## Theorem 5 (growth ceiling)

Every orbit satisfies

\[
\limsup_{n\to\infty}\frac{q_n}{n}\le\frac12.
\]

### Proof

Since \(b_{n+1}-b_n=r_n\le n-1\),

\[
b_n\le m+\sum_{k=2}^{n-1}(k-1)
   =m+\frac{(n-2)(n-1)}2.
\]

Also \(q_n=\lfloor b_n/n\rfloor\le b_n/n\). Divide the displayed bound
by \(n^2\) and take the upper limit. \(\square\)

## Theorem 6 (exact doubling coordinate)

After entry,

\[
e_{n+1}=2e_n-a_n(n+2),\qquad e_{n+1}\equiv2e_n\pmod{n+2}. \tag{1.2}
\]

Moreover, stabilization is exactly the event \(e_n=0\).

### Proof

Since \(2r_n-q_n=q_n+2e_n\), equation (1.1) gives

\[
r_{n+1}=q_n+2e_n-a_n(n+1),\qquad q_{n+1}=q_n+a_n.
\]

Subtracting proves (1.2). The equality \(e_n=0\) is \(r_n=q_n\), so the
last assertion follows from Theorem 1. \(\square\)

## Theorem 13 (forced rebound)

If \(a_n=-1\) and \(3q_n\le n+1\), then \(a_{n+1}=1\).

### Proof

A down-step gives

\[
q_{n+1}=q_n-1,\qquad r_{n+1}=2r_n-q_n+n+1.
\]

The next transition numerator is

\[
2r_{n+1}-q_{n+1}=4r_n-3q_n+2n+3.
\]

It is at least \(n+2\) whenever \(4r_n\ge3q_n-n-1\), which follows from
\(r_n\ge0\) and the hypothesis. \(\square\)

## Theorem 14 (ratchet)

Suppose \(3q_k\le k+1\) throughout an interval \([u,v]\). Then
\(q_k\ge q_u-1\) for \(u\le k\le v+1\), and every decrease is undone by
the next step.

### Proof

Induct on \(k\). From a value at least \(q_u\), one down-step reaches at
least \(q_u-1\), and Theorem 13 forces the next step upward. Whenever
\(q_k=q_u-1\), that value arose from the preceding down-step, so the same
theorem forces \(q_{k+1}=q_u\). Thus the lower level cannot be crossed.
\(\square\)

## Theorem 18 (the increment bounds the start)

If the orbit from \(m\ge1\) stabilizes with eventual increment \(c\), then

\[
\boxed{m<(c+3)(3c+5)}. \tag{1.3}
\]

### Proof

Let \(n_0\) be the first entry index and \(t\) the stabilization index, so
\(q_t=r_t=c\). Define

\[
S=\{n\in[n_0,t]:3q_n>n+1\}.
\]

The sequence \(b_n\) is nondecreasing, hence \(m=b_2\le b_n\).

First suppose \(S\) is empty. Theorem 14 gives
\(c=q_t\ge q_{n_0}-1\), hence

\[
b_{n_0}< (c+2)n_0.
\]

If \(n_0=2\), this is already stronger than (1.3). If \(n_0\ge3\),
minimality of \(n_0\) and monotonicity give

\[
(n_0-1)^2\le b_{n_0}<(c+2)n_0.
\]

This forces \(n_0\le c+4\), and therefore

\[
m\le b_{n_0}<(c+2)(c+4)<(c+3)(3c+5).
\]

Now suppose \(S\ne\varnothing\), and let \(n^*=\max S\). If \(n^*<t\),
Theorem 14 on \([n^*+1,t]\), together with
\(q_{n^*+1}\ge q_{n^*}-1\), gives \(q_{n^*}\le c+2\).
The same bound is immediate if \(n^*=t\). Since \(n^*\in S\),

\[
n^*<3c+5.
\]

Consequently

\[
m\le b_{n^*}< (q_{n^*}+1)n^*
 \le(c+3)n^*<(c+3)(3c+5).
\]

This proves (1.3). \(\square\)

## Corollary 19 (finite candidate set)

For every \(c\ge1\), every start whose eventual increment is \(c\) lies in

\[
1\le m<(c+3)(3c+5).
\]

This corollary is unconditional but does not assert that every candidate
stabilizes.

## Corollary 20 (computer-assisted nonsurjectivity)

The eventual-increment map is not surjective onto the positive integers.
Its smallest omitted values are \(5\) and \(7\).

### Proof

Corollary 19 confines every possible witness for increment \(c\) to a
finite interval. The certified enumeration described in the computational
supplement resolves every start \(m\le10^7\), hence every increment
\(c\le1823\). No candidate in the complete ranges

\[
m<160\quad(c=5),\qquad m<260\quad(c=7)
\]

has the corresponding eventual increment, while increments \(1,2,3,4,6\)
do occur. \(\square\)

Corollary 20 depends on both Theorem 18 and the finite certificate. It does
not depend on the unresolved universal stabilization conjecture.
