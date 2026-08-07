#!/usr/bin/env python3
"""Exhaustive three-gap extension tree above the K18 two-gap certificates.

K18 classified the six all-unit pure-upper words with ``r0 + r1 <= 2`` and found
342 states with a third gate.  This module classifies the *third* gap of every
such state, and reports whether a fourth gate exists.

Why the classification is exhaustive, without any new bound.  A three-gap state
in scope carries, in particular, one of the six K18 two-gap prefixes, so its
start index already obeys the K18 bound

    n0 <= 2^(r0+r1+6) - r0 - r1 - 8      (C114 + C115, proved)

giving 56, 119, 119, 246, 246, 246.  The wrap count is bounded by the unit-state
ceiling ``f <= D - 3``.  The start set is therefore finite and complete before
the third gate is ever considered, and *no bound on r2 is needed*: Theorem 130
makes the gate deterministic, so r2 is read off the forced map rather than
searched for.  The same holds for r3.  No new search ceiling is claimed here.

What this does not establish.  Nothing here says a safe path terminates.  A
missing fourth gate means only that Theorem 130's all-unit pure-upper partial
map is undefined at that state.  Other block lengths, non-pure-upper gates,
reachability from an original start b1 = m, and the Cloitre stabilization
conjecture itself are all untouched.

Only ``unit_gap_words_core`` is imported: the definitions this extension rests
on are the merged K18 ones, not a second transcription.  The independently
transcribed oracle and the raw safe-map replay live in
``unit_gap_extensions_checks``.
"""

from __future__ import annotations

from dataclasses import dataclass

from unit_gap_words_core import (
    REQUIRED_WORDS,
    CertificateError,
    Row,
    gate,
    is_unit_state,
    start_bound,
    u_ceiling,
)

# Provenance only.  Nothing below reads these while generating anything; they
# are recorded in the report so a reader can pin which K18 produced the input.
MERGED_BASE_COMMIT = "791042877602e73b09bb2d1d6bdb9901acc3eb98"
K18_VERIFIER_COMMIT = "283bafd8d8f8e2880c5349af7b878af4380176b8"
K18_REGISTRATION_COMMIT = "be72573c1a7a9b18a2974cdf68567a7436986f83"
K18_REPORT_SHA256 = "6780998c36351d4f0b8a9bbf93639aafa60ec3c64d30602e3452d411444d7cde"

#: The six K18 two-gap prefixes, in K18's canonical order.  This is a scope
#: definition, not a discovered result: the extension tree is by construction
#: the set of three-gap words whose first two gaps are one of these.
PREFIXES: tuple[tuple[int, int], ...] = REQUIRED_WORDS

#: Absent fourth gate.  Kept as a sentinel rather than ``None`` so that rows
#: order and serialize deterministically.
NO_GATE = -1


@dataclass(frozen=True, order=True)
class ExtRow:
    """One start state, the three states its word reaches, and the frontier."""

    n: int
    u: int
    f: int
    n1: int
    u1: int
    f1: int
    n2: int
    u2: int
    f2: int
    n3: int
    u3: int
    f3: int
    r2: int
    continues4: bool
    r3: int
    n4: int
    u4: int
    f4: int

    @property
    def two_gap_row(self) -> Row:
        """The K18 row this extension state sits above.  Always continuing."""
        return Row(
            self.n, self.u, self.f,
            self.n1, self.u1, self.f1,
            self.n2, self.u2, self.f2,
            True,
        )


def three_gap_chain(n, u, f, prefix, *, unit=is_unit_state, transition=gate):
    """Validate three gates from ``(n, U, f)``, pinning only the first two gaps.

    ``r2`` is *read off* the forced map, never requested: Theorem 130 leaves no
    choice at the third gate.  Every one of the four states goes through the
    complete unit-state predicate.
    """
    h0, h1 = prefix[0] + 2, prefix[1] + 2
    if not unit(n, u, f):
        return None
    first = transition(n, u, f)
    if first is None or first[0] != h0:
        return None
    _, f1, n1, u1 = first
    if not unit(n1, u1, f1):
        return None
    second = transition(n1, u1, f1)
    if second is None or second[0] != h1:
        return None
    _, f2, n2, u2 = second
    if not unit(n2, u2, f2):
        return None
    third = transition(n2, u2, f2)
    if third is None:
        return None
    h2, f3, n3, u3 = third
    if not unit(n3, u3, f3):
        return None
    fourth = transition(n3, u3, f3)
    if fourth is None:
        return ExtRow(n, u, f, n1, u1, f1, n2, u2, f2, n3, u3, f3,
                      h2 - 2, False, NO_GATE, NO_GATE, NO_GATE, NO_GATE)
    h3, f4, n4, u4 = fourth
    if not unit(n4, u4, f4):
        raise CertificateError(f"Theorem 130 successor at {(n3, u3, f3)} is not a unit state")
    return ExtRow(n, u, f, n1, u1, f1, n2, u2, f2, n3, u3, f3,
                  h2 - 2, True, h3 - 2, n4, u4, f4)


# ---------------------------------------------------------------------------
# Discovery.  Two paths: an exponent window, and a window-free sweep.
# ---------------------------------------------------------------------------


def windowed_seeds(prefix, *, unit=is_unit_state, transition=gate) -> list[tuple[int, int, int]]:
    """Optimized normalized discovery: condition M pins f given ``(n, h0)``.

    Returns ``(n, f, r2)`` triples at ``U = 0`` within the inherited bound.  The
    exponent is always the one the prefix asks for; there is no override, so this
    phase cannot be pointed at an h0 that ``expand_fibre`` would not agree with.
    """
    h0 = prefix[0] + 2
    scale = 1 << h0
    out: list[tuple[int, int, int]] = []
    for n in range(2, start_bound(*prefix) + 1):
        low = -(-(n + h0 + 4) // scale)  # ceil, from L at h0
        high = (n + h0 + 3 + (1 << (h0 + 2))) // scale  # floor, from M at h0
        for f in range(max(1, low), high + 1):
            row = three_gap_chain(n, 0, f, prefix, unit=unit, transition=transition)
            if row is not None:
                out.append((n, f, row.r2))
    return out


def direct_seeds(prefix, hi: int) -> list[tuple[int, int, int]]:
    """Window-free normalized sweep: every f in [1, n - 3] at U = 0, up to ``hi``.

    No exponent window, no congruence shortcut, no reliance on h* being the only
    admissible exponent.  It does share ``three_gap_chain``, hence the
    transition; the transition is what the oracle in
    ``unit_gap_extensions_checks`` covers.
    """
    out: list[tuple[int, int, int]] = []
    for n in range(2, hi + 1):
        for f in range(1, n - 2):  # f <= D - 3 = n - 3 at U = 0
            row = three_gap_chain(n, 0, f, prefix)
            if row is not None:
                out.append((n, f, row.r2))
    return out


def expand_fibre(n, f, prefix, *, unit=is_unit_state, transition=gate) -> list[ExtRow]:
    """The complete U-fibre above one normalized seed.

    Downward closure in U, for three gates.  Write the k-th state's coordinates
    as ``(n_k, U0 + k, f_k)``; by Lemma 131 claim 1 the ``(n_k, f_k)`` are free of
    U, so ``D_k = (n_k - 2k) - 2*U0`` is a U-free constant minus ``2*U0``.  Every
    U-dependent condition across states 0..3 and gates 0..2 -- ``f_k <= D_k - 3``,
    ``4 f_k <= n_k + D_k + 2``, P and the child headroom U_h -- is of the form
    ``D_k >= (U-free quantity)``, and the parity of ``D_k - 3 - f_k`` does not
    move with U0 at all.  Lowering U0 raises every D_k, so validity is downward
    closed and scanning upward to the first failure is complete.
    ``audit_certificates`` re-checks that against a full scan to ``u_ceiling``
    instead of assuming it.
    """
    rows: list[ExtRow] = []
    for u in range(0, u_ceiling(n, f) + 1):
        row = three_gap_chain(n, u, f, prefix, unit=unit, transition=transition)
        if row is None:
            break
        rows.append(row)
    return rows


@dataclass(frozen=True)
class ExtCertificate:
    """Every state carrying one realized three-gap word."""

    word: tuple[int, int, int]
    inherited_bound: int
    rows: tuple[ExtRow, ...]

    @property
    def prefix(self) -> tuple[int, int]:
        return self.word[0], self.word[1]

    @property
    def seeds(self) -> tuple[tuple[int, int], ...]:
        return tuple(sorted({(r.n, r.f) for r in self.rows}))

    @property
    def states(self) -> tuple[tuple[int, int, int], ...]:
        return tuple(sorted((r.n, r.u, r.f) for r in self.rows))

    @property
    def u_ranges(self) -> dict[tuple[int, int], tuple[int, ...]]:
        out: dict[tuple[int, int], list[int]] = {}
        for row in self.rows:
            out.setdefault((row.n, row.f), []).append(row.u)
        return {key: tuple(sorted(v)) for key, v in out.items()}

    @property
    def fourth_continuing(self) -> int:
        return sum(1 for r in self.rows if r.continues4)

    @property
    def r3_values(self) -> tuple[int, ...]:
        return tuple(sorted({r.r3 for r in self.rows if r.continues4}))


def word_order(words) -> list[tuple[int, int, int]]:
    """Canonical order: by gap sum, then lexicographic.  Stable and total."""
    return sorted(words, key=lambda w: (sum(w), w))


def build_certificates(**kw) -> dict[tuple[int, int, int], ExtCertificate]:
    """Discover every realized three-gap word above the six K18 prefixes.

    Both phases now take exactly ``unit`` and ``transition``, so ``**kw`` reaches
    them unfiltered and the two cannot be given different definitions.
    """
    buckets: dict[tuple[int, int, int], list[ExtRow]] = {}
    for prefix in PREFIXES:
        for n, f, _ in windowed_seeds(prefix, **kw):
            for row in expand_fibre(n, f, prefix, **kw):
                buckets.setdefault(prefix + (row.r2,), []).append(row)
    return {
        word: ExtCertificate(word, start_bound(*word[:2]), tuple(sorted(buckets[word])))
        for word in word_order(buckets)
    }


#: Per-prefix inherited start bounds, computed from C114/C115 rather than typed.
INHERITED_BOUNDS: dict[tuple[int, int], int] = {p: start_bound(*p) for p in PREFIXES}
