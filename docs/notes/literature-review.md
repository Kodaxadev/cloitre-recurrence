# Literature review

**Bottom line: the conjecture is open.** There is no published paper on it. The
entire recorded history consists of five OEIS entries (2002–2007) and one
MathOverflow thread (2014, with a substantive answer added in 2025). No proof,
no partial proof, and no equivalent formulation under a different name was found.

## Search performed

| Source | Method | Result |
|---|---|---|
| OEIS | sequence search on the $m=1$ orbit `1,1,2,4,4,8,10,13,18,18,26,30,36,46`; full-text search; cross-reference crawl of A073117 | 5 relevant entries, listed below |
| MathOverflow | Stack Exchange API, several phrasings of the recurrence | **1 hit**, question 191518 |
| Math.StackExchange | Stack Exchange API, same phrasings | no relevant hit |
| arXiv | API full-text for `A073117`, `A117846`, `A074482`, "mod sequences", Cloitre + recurrence | **0 hits** |
| Crossref | bibliographic query on the recurrence and on "eventually arithmetic progression" | **0 relevant hits** |
| Web search | recurrence written out in several notations, plus OEIS ids | only the OEIS and MO pages above |
| sci.math (1990s–2000s) | traced via the A066910 citation | original thread link (mathforum epigone) is dead; content survives only as the OEIS comment |

*Not searched:* zbMATH and MathSciNet require subscriptions unavailable here. Given
that arXiv and Crossref are both empty, and that the problem's only public traces
are OEIS comments, the chance of a paywalled paper on it is low but not zero.

## The primary sources

### OEIS A073117 — the base orbit
`a(n+1) = a(n) + a(n) mod n; a(1) = 1.` Reinhard Zumkeller, 19 Aug 2002.
Contains the earliest statement of the conjecture, by **Benoit Cloitre**, 20 Aug 2002:

> *Conjecture (seems provable): More generally let a and b(1) be integers. If
> b(n+1) = b(n) + b(n) (mod(n+a)) there is an integer x(a,b(1)) such that
> b(n+1) = b(n) + x(a,b(1)) for n sufficiently large.*

The parenthetical "seems provable" is 24 years old and no proof has ever been
recorded. The entry notes $a(397)=38606=398\cdot97$, i.e. the orbit is captured at
index 397 with increment 97 — which is exactly the divisibility criterion
(Theorem 2) in the concrete case.

### OEIS A117846 — the conjecture in the form studied here
`b(1)=2n-1, b(k+1)=b(k)+b(k) mod k; a(n) = the eventual common difference, or 0.`
**Alex Abercrombie**, 22 Mar 2007. Two comments matter:

> *Putting b(1)=2n gives essentially the same sequence as putting b(1)=2n-1.*

— this is the **pair-merging theorem** (Theorem 10), which is why the sequence is
indexed by odd starts.

> *It is a plausible conjecture or at least an interesting open problem that a(n)
> is never zero... **Do the values a(n) include all positive numbers?***

The first sentence is the conjecture. **The second question is answered in this
project: no** (Corollary 20; smallest missing values 5 and 7). Only 68 terms are
published; this project computes the equivalent data for all $m\le10^7$.

### OEIS A074482 / A074483 / A074484 — the shifted family
Zumkeller & Cloitre, 23 Aug 2002. `b(1,n)=1, b(k+1,n)=b(k,n)+(b(k,n) mod (k+n))`;
the three sequences give the eventual increment, the stabilization index, and the
value at it. Comment: `b(k,n) = a(n)*(k+n+1) for k > A074483(n)` — again the
$(n{+}1)$-multiple structure. **b-files by David W. Wilson cover $n=0..10000$**,
the largest previously published computation in this family. Note the wild spread:
A074483 contains entries such as 269393 and 292695 for single-digit $n$, the first
public sign of the heavy tail.

### OEIS A066910 — first differences
`a(1)=1; a(n+1) = (sum_{k=1..n} a(k)) mod n.` Leroy Quet, 22 Jan 2002. Apart from
the first term this is the difference sequence of A073117 (Sigrist, 2017). Cites a
sci.math post by **Steven Taschuk and Phil Carmody** observing `a(k)=97 for k>=398`
— apparently the first recorded observation of stabilization anywhere.

### MathOverflow 191518 — "Mod sequences that seem to become constant; and the number 316"
Asked 26 Dec 2014, score 42, 2 answers. Posed in the partial-sum formulation
$a_n=(\sum_{k<n}a_k)\bmod n$; asks (Q1) whether it always becomes constant and
(Q2) what is special about 316.

* **Answer 1** (2014) shows the partial-sum form is equivalent to
  $x(n+1)=x(n)+x(n)\bmod n$ with $x(1)=2s-1$, notes the parity merging, and points
  at A117846 and A074482. No proof.
* **Answer 2** (3 Sep 2025) is the substantive one and overlaps this project's
  starting point. It states, without proof: the exact merge criterion (Theorem 11
  here), the divisibility criterion (Theorem 2 here), the $x_n\approx s+0.25n^2$
  growth law, the $1/n$ capture probability, the heavy tail with infinite expected
  stabilization time, and the claim that the increment should be $\gtrsim\sqrt s$.
  It includes a plot for $s$ up to $100{,}000$ and argues 316 is not special.

## Consequences for attribution

Results **already in the literature**, reproved here for completeness:
Theorem 1 (folklore), **Theorem 2** and **Theorem 11** (MO answer 2, 2025),
Lemma 4, **Theorem 10** (A117846, 2007), and the heuristics H1/H5.

Results that appear to be **new here** (no source found): the doubling coordinate
$e_n$ and Theorem 6, the capture criterion C7, the congruence lemma L8 and parity
corollary C9, the consecutive-step bounds L12, the forced rebound T13, the ratchet
T14, and — the substantive one — **Theorem 18 and its corollaries C19/C20**, which
convert a question that looks infinite into a finite computation and thereby
answer Abercrombie's 2007 question.

The MO answer's $\sqrt s$ remark is the closest anything in the literature comes to
Theorem 18, but it is offered as a heuristic about typical size, not as a bound,
and it points the wrong way (a lower bound on $c$ in terms of $m$, rather than the
upper bound on $m$ in terms of $c$ that makes the spectrum decidable).

## Terminology check

No hidden name for this problem was found. It is not a disguised form of any
studied family: it is not a Collatz-type map (the modulus moves), not a
Recamán-type sequence (no subtraction/injectivity rule), not a Rowland-type
prime-generating recurrence (that uses $\gcd$, cf. A106108), and not a member of
the "mean-median" or max-type difference equation literature that surfaced in the
searches. The closest structural relative is the class of **expanding maps with a
moving modulus**, for which no general capture theory exists.

### Moving-modulus follow-up (28 July 2026)

A fresh formula-level search after Lemma 40 found literature on two nearby but
different systems:

- Allouche, Stipulanti, and Yao study multiplication by two modulo a **fixed**
  odd integer and its cycle structure:
  [arXiv:2504.17564](https://arxiv.org/abs/2504.17564).
- Hare and Sidorov classify periodic doubling-map cycles that avoid a **fixed**
  interval:
  [arXiv:1308.2905](https://arxiv.org/abs/1308.2905).

Neither result covers Lemma 40's simultaneous moving modulus `n+2` and growing
forbidden interval. Searches for the exact recurrences
`x_(n+1)=2x_n mod(n+2)` and `2x_n mod(n+1)` found no applicable capture theorem.
This is a negative search result, not proof that none exists.

The later continuation also appears new: the all-period obstruction
(Theorems 32, 36, and 38), the exact future-digit identity (Theorem 39), and
the moving-modulus danger-interval reduction (Lemma 40).

## Sources

- [OEIS A073117](https://oeis.org/A073117) — base orbit, Cloitre's conjecture
- [OEIS A117846](https://oeis.org/A117846) — the conjecture as studied here; Abercrombie's coverage question
- [OEIS A074482](https://oeis.org/A074482), [A074483](https://oeis.org/A074483), [A074484](https://oeis.org/A074484) — shifted-modulus family, Wilson b-files
- [OEIS A066910](https://oeis.org/A066910) — first differences; sci.math priority note
- [MathOverflow 191518](https://mathoverflow.net/questions/191518/mod-sequences-that-seem-to-become-constant-and-the-number-316) — the only research-level discussion
