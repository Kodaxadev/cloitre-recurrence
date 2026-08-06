#!/usr/bin/env python3
"""Definitions and exhaustive enumeration for short all-unit pure-upper words.

No project code is imported.  Lemma 117, Corollary 114, Corollary 115 and
Theorem 130 are transcribed here from their statements; everything else is
derived from that transcription.  The cross-checks, negative controls and
report live in ``verify_unit_gap_words.py``, which is the canonical entry
point and the only importer of this module.

Why the enumeration is finite.  For a gap word ``(r0, r1)``:

    Corollary 115 at gate 0 gives      f1 <= 2^(r0+4),
    Corollary 114 at gate 1 gives      f2 = 2^(r1+2) f1 - n1 - r1 - 5,
    Corollary 115 at gate 1 gives      f2 >= 1,
    hence                              n1 <= 2^(r0+r1+6) - r1 - 6,
    and with n1 = n0 + r0 + 2,         n0 <= 2^(r0+r1+6) - r0 - r1 - 8.

That is the sharp form of Theorem 118's two-gap bound (118.1) at a single
adjacent pair, and it is what ``start_bound`` computes.
"""

from __future__ import annotations

from dataclasses import dataclass

# Canonical word order: by gap sum, then lexicographic.  These six are exactly
# the words with r0 + r1 <= 2, i.e. every word whose start bound is <= 246.
REQUIRED_WORDS: tuple[tuple[int, int], ...] = (
    (0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (2, 0),
)


class CertificateError(AssertionError):
    """A certificate disagrees with the definitions or with the contract."""


# ---------------------------------------------------------------------------
# Definitions, transcribed from their statements.
# ---------------------------------------------------------------------------


def is_unit_state(n: int, u: int, f: int) -> bool:
    """Lemma 117 (117.1): (n, U, f) reconstructs a returning unit block.

    All four conditions are required.  ``4f <= n + D + 2`` is the test that the
    block returns to a zero epoch after its single wrap; dropping it changes the
    predicate, which the ``dropped_fourth_clause`` control exhibits.
    """
    d_coord = n - 2 * u
    return (
        n >= 2
        and u >= 0
        and f >= 1
        and (n + 3 + f) % 4 == 0
        and f <= d_coord - 3
        and 4 * f <= n + d_coord + 2
    )


def minimal_exponent(n: int, f: int) -> int:
    """(130.2): the least h >= 2 with 2^h f >= n + h + 4."""
    h = 2
    while (f << h) < n + h + 4:
        h += 1
    return h


def gate(n: int, u: int, f: int) -> tuple[int, int, int, int] | None:
    """The unique pure-upper unit gate out of (n, U, f), or None.

    Returns ``(h, g, n', U')`` with h = r + 2, per Theorem 130 (130.3).  The
    three admissibility tests are Corollary 115 (115.1) rewritten at h: the
    parent defect P, the window M on g, and the child headroom U.

    This does *not* test whether its input is a valid unit state.  Callers must
    apply ``is_unit_state`` first; ``chain`` does.
    """
    d_coord = n - 2 * u
    defect = d_coord - 3 - f
    if defect < 4 or defect % 2 != 0:  # P
        return None
    h = minimal_exponent(n, f)
    g = (f << h) - n - h - 3  # (130.4)
    if g < 1 or g > (1 << (h + 2)):  # L and M
        return None
    if (d_coord + h - 2) - 3 - g < (1 << (h + 2)):  # U
        return None
    return h, g, n + h, u + 1


def start_bound(r0: int, r1: int) -> int:
    """Largest possible start index of a unit state with gap word (r0, r1)."""
    return (1 << (r0 + r1 + 6)) - r0 - r1 - 8


def u_ceiling(n: int, f: int) -> int:
    """Largest U with f <= D - 3, hence the last U that can be a unit state."""
    return (n - f - 3) // 2


# ---------------------------------------------------------------------------
# Certificates.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, order=True)
class Row:
    """One accepted start state and the two states its gap word reaches."""

    n: int
    u: int
    f: int
    n1: int
    u1: int
    f1: int
    n2: int
    u2: int
    f2: int
    continues: bool


@dataclass(frozen=True)
class WordCertificate:
    gaps: tuple[int, int]
    bound: int
    rows: tuple[Row, ...]

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
    def post_pair(self) -> dict[tuple[int, int], tuple[int, int]]:
        """Second successor per seed.  Lemma 131 makes it independent of U."""
        out: dict[tuple[int, int], set[tuple[int, int]]] = {}
        for row in self.rows:
            out.setdefault((row.n, row.f), set()).add((row.n2, row.f2))
        for key, values in out.items():
            if len(values) != 1:
                raise CertificateError(f"seed {key} has {len(values)} post-pair states")
        return {key: values.pop() for key, values in out.items()}

    @property
    def continuing(self) -> int:
        return sum(1 for row in self.rows if row.continues)


# ---------------------------------------------------------------------------
# Phase A: normalized candidate discovery.  Phase B: U-fibre expansion.
# ---------------------------------------------------------------------------


def chain(n, u, f, gaps, *, unit=is_unit_state, transition=gate) -> Row | None:
    """Validate the exact two-gate word from (n, U, f), or return None.

    Every state, including both successors, goes through the complete unit-state
    predicate, and each gate's exponent must equal the requested one.
    """
    h0, h1 = gaps[0] + 2, gaps[1] + 2
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
    return Row(n, u, f, n1, u1, f1, n2, u2, f2, transition(n2, u2, f2) is not None)


def normalized_candidates(
    gaps, *, unit=is_unit_state, exponent=minimal_exponent,
    transition=gate, h0_override: int | None = None,
) -> list[tuple[int, int]]:
    """Every normalized (n, f) at U = 0 carrying the requested word.

    Condition M pins f to at most five consecutive integers once (n, h0) is
    fixed -- this is (132.2) -- so the sweep costs O(bound) rather than
    O(bound^2).  Every candidate in the window is kept: nothing is reduced to a
    least start, and nothing is reduced to one representative per congruence
    class.  There is no U loop here; the wrap count is handled by Phase B.
    """
    h0 = gaps[0] + 2 if h0_override is None else h0_override
    scale = 1 << h0
    out: list[tuple[int, int]] = []
    for n in range(2, start_bound(*gaps) + 1):
        low = -(-(n + h0 + 4) // scale)  # ceil, from L at h0
        high = (n + h0 + 3 + (1 << (h0 + 2))) // scale  # floor, from M at h0
        for f in range(max(1, low), high + 1):
            if not unit(n, 0, f):
                continue
            if exponent(n, f) != h0:
                continue
            if chain(n, 0, f, gaps, unit=unit, transition=transition) is None:
                continue
            out.append((n, f))
    return out


def direct_seeds(gaps, hi: int) -> list[tuple[int, int]]:
    """Window-free normalized scan: every f in [1, n - 3] at U = 0, up to ``hi``.

    This shares no candidate-discovery step with ``normalized_candidates`` -- no
    exponent window, no congruence shortcut, no reliance on h* being the only
    admissible exponent -- so comparing the two tests the window instead of
    assuming it.  It does share ``chain``, hence the transition; the transition is
    what the two oracles in ``unit_gap_words_checks`` cover.
    """
    return [
        (n, f)
        for n in range(2, hi + 1)
        for f in range(1, n - 2)  # f <= D - 3 = n - 3 at U = 0
        if chain(n, 0, f, gaps) is not None
    ]


def expand_fibre(n, f, gaps, *, unit=is_unit_state, transition=gate) -> list[Row]:
    """The complete U-fibre above one normalized candidate.

    By Lemma 131 claim 2 the parent defect P and the child headroom U are
    monotone in the wrap count -- lowering U raises D = n - 2U and can only help
    -- while the congruence, f >= 1 and M do not mention U at all.  The valid
    set is therefore downward closed, so scanning upward and stopping at the
    first failure is complete.  ``audit_word`` re-checks that closure against a
    full scan up to ``u_ceiling`` rather than assuming it.
    """
    rows: list[Row] = []
    for u in range(0, u_ceiling(n, f) + 1):
        row = chain(n, u, f, gaps, unit=unit, transition=transition)
        if row is None:
            break
        rows.append(row)
    return rows


def generate_word(gaps, **kw) -> WordCertificate:
    """Phase A then Phase B, for one gap word."""
    fibre_kw = {k: v for k, v in kw.items() if k in ("unit", "transition")}
    rows: list[Row] = []
    for n, f in normalized_candidates(gaps, **kw):
        rows.extend(expand_fibre(n, f, gaps, **fibre_kw))
    return WordCertificate(gaps, start_bound(*gaps), tuple(sorted(rows)))


# ---------------------------------------------------------------------------
# Audit: re-derive a certificate from the definitions and demand equality.
# ---------------------------------------------------------------------------


def audit_word(cert: WordCertificate) -> None:
    gaps = cert.gaps
    if cert.bound != start_bound(*gaps):
        raise CertificateError(f"{gaps}: bound {cert.bound} is not the derived bound")

    states = cert.states
    if len(states) != len(set(states)):
        raise CertificateError(f"{gaps}: duplicate (n, U, f) in the state list")
    if list(cert.rows) != sorted(cert.rows):
        raise CertificateError(f"{gaps}: rows are not canonically sorted")

    for row in cert.rows:
        if not 2 <= row.n <= cert.bound:
            raise CertificateError(f"{gaps}: start {row.n} outside [2, {cert.bound}]")
        rebuilt = chain(row.n, row.u, row.f, gaps)
        if rebuilt is None:
            raise CertificateError(f"{gaps}: {(row.n, row.u, row.f)} fails the word")
        if rebuilt != row:
            raise CertificateError(
                f"{gaps}: {(row.n, row.u, row.f)} row mismatch, got {rebuilt}"
            )

    # Each U-fibre must be an unbroken prefix 0..k with nothing valid above it.
    # This is what makes the early break in expand_fibre safe, not just plausible.
    for (n, f), wraps in cert.u_ranges.items():
        if wraps != tuple(range(len(wraps))):
            raise CertificateError(f"{gaps}: fibre at {(n, f)} is not a 0.. prefix")
        for u in range(len(wraps), u_ceiling(n, f) + 1):
            if chain(n, u, f, gaps) is not None:
                raise CertificateError(f"{gaps}: fibre at {(n, f)} misses U={u}")

    cert.post_pair  # raises if a seed has two different post-pair states

    # Completeness, and the bound, from the definitions rather than from the
    # window.  Scanning to twice the bound does two jobs: it confirms the seed
    # set is exactly what a window-free sweep finds, and it confirms the derived
    # bound actually binds instead of merely happening to sit above the data.
    margin = direct_seeds(gaps, 2 * cert.bound + 2)
    above = sorted(s for s in margin if s[0] > cert.bound)
    if above:
        raise CertificateError(f"{gaps}: candidates above the bound: {above[:4]}")
    if tuple(sorted(margin)) != cert.seeds:
        raise CertificateError(
            f"{gaps}: window-free scan finds {len(margin)} seeds, certificate "
            f"has {len(cert.seeds)}"
        )

    fresh = generate_word(gaps)
    if fresh.rows != cert.rows:
        raise CertificateError(
            f"{gaps}: regeneration gives {len(fresh.rows)} rows, "
            f"certificate has {len(cert.rows)}"
        )
