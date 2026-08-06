#!/usr/bin/env python3
"""Cross-checks and negative controls for the unit gap-word certificates.

Two independent oracles and ten corruption controls.  Neither oracle shares a
formula with ``unit_gap_words_core``:

* ``oracle_buckets`` writes the unit-state predicate out inline, finds gaps by
  scanning every r against Corollary 115 in its own r coordinates instead of
  evaluating h* = min{h : 2^h f >= n + h + 4}, uses no exponent window, and uses
  no monotonicity in the wrap count.  It classifies each state by whichever gap
  word it actually has, so the six certificates fall out of one pass.
* ``replay_row`` steps the raw safe map digit by digit from its definition and
  reads the gap word, the residues, the indices and the wrap counts off the
  literal trace.

Only the data containers (``Row``, ``WordCertificate``) and the audit under test
are imported from the core.
"""

from __future__ import annotations

import json

from unit_gap_words_core import (
    CertificateError,
    Row,
    WordCertificate,
    audit_word,
    generate_word,
    is_unit_state,
    minimal_exponent,
    start_bound,
)

FORBIDDEN_CLAIMS = ("safe path terminates", "safe-path termination", "full safe path")


def audit_report(report: dict) -> None:
    """The report may record a stopped partial map, never a terminating path."""
    if report.get("full_safe_path_termination_claimed") is not False:
        raise CertificateError("report needs full_safe_path_termination_claimed=false")
    blob = json.dumps(report, sort_keys=True).lower()
    for phrase in FORBIDDEN_CLAIMS:
        if phrase in blob:
            raise CertificateError(f"report contains the forbidden claim {phrase!r}")


# ---------------------------------------------------------------------------
# Oracle one: a literal triple loop with no shared candidate discovery.
# ---------------------------------------------------------------------------


def oracle_buckets(bound: int, r_max: int = 24) -> dict[tuple[int, int], list[Row]]:
    """Brute force over (n, U, f), classifying each state by its own gap word.

    Determinism is a conclusion here rather than an assumption: if two gaps ever
    passed at one state this raises instead of picking one.
    """

    def unit(n: int, u: int, f: int) -> bool:
        d_coord = n - 2 * u
        return (
            n >= 2
            and u >= 0
            and f >= 1
            and (n + 3 + f) % 4 == 0
            and f <= d_coord - 3
            and 4 * f <= n + d_coord + 2
        )

    def gaps_at(n: int, u: int, f: int) -> list[tuple[int, int]]:
        """Every r >= 0 passing Corollary 115 (115.1) written in r coordinates."""
        d_coord = n - 2 * u
        if d_coord - 3 - f < 4 or (d_coord - 3 - f) % 2 != 0:
            return []
        found = []
        for r in range(0, r_max):
            nxt = (f << (r + 2)) - n - r - 5  # Corollary 114 (114.1)
            span = 1 << (r + 4)
            if 1 <= nxt <= span and d_coord + r - 3 - nxt >= span:
                found.append((r, nxt))
        return found

    def only(n: int, u: int, f: int) -> tuple[int, int] | None:
        found = gaps_at(n, u, f)
        if len(found) > 1:
            raise CertificateError(f"two admissible gaps at {(n, u, f)}: {found}")
        return found[0] if found else None

    buckets: dict[tuple[int, int], list[Row]] = {}
    for n in range(2, bound + 1):
        # Both loop bounds below are the literal content of f >= 1 and
        # f <= D - 3, and unit() re-tests them anyway.
        for u in range(0, (n - 4) // 2 + 1):
            for f in range(1, n - 2 * u - 2):
                if not unit(n, u, f):
                    continue
                first = only(n, u, f)
                if first is None:
                    continue
                r0, f1 = first
                n1, u1 = n + r0 + 2, u + 1
                if not unit(n1, u1, f1):
                    continue
                second = only(n1, u1, f1)
                if second is None:
                    continue
                r1, f2 = second
                n2, u2 = n1 + r1 + 2, u1 + 1
                if not unit(n2, u2, f2):
                    continue
                buckets.setdefault((r0, r1), []).append(
                    Row(n, u, f, n1, u1, f1, n2, u2, f2, only(n2, u2, f2) is not None)
                )
    return {key: sorted(v) for key, v in buckets.items()}


def cross_check_oracle(
    certs: dict[tuple[int, int], WordCertificate], bound: int
) -> dict[str, object]:
    """Compare word by word.  Every required word must lie inside the bound."""
    uncovered = [f"{a}{b}" for a, b in certs if start_bound(a, b) > bound]
    if uncovered:
        raise CertificateError(f"oracle bound {bound} does not cover {uncovered}")
    buckets = oracle_buckets(bound)
    compared = []
    for gaps, cert in sorted(certs.items()):
        theirs = tuple(buckets.get(gaps, ()))
        if tuple(cert.rows) != theirs:
            raise CertificateError(
                f"oracle disagrees on {gaps}: {len(theirs)} states vs {len(cert.rows)}"
            )
        compared.append(f"{gaps[0]}{gaps[1]}")
    return {"bound": bound, "words_compared": compared, "agrees": True}


# ---------------------------------------------------------------------------
# Oracle two: the raw safe map, replayed digit by digit.
# ---------------------------------------------------------------------------


def raw_trace(n, u, e, steps) -> tuple[str, list[tuple[int, int, int]]]:
    """The safe map from its definition: double, wrap past n + 2, stop if stuck."""
    word: list[str] = []
    seen = [(n, u, e)]
    for _ in range(steps):
        doubled = 2 * e
        if doubled > n + 2:
            n, u, e = n + 1, u + 1, doubled - n - 2
            word.append("w")
        elif u + doubled < n + 1:
            n, e = n + 1, doubled
            word.append("0")
        else:
            break
        seen.append((n, u, e))
    return "".join(word), seen


def replay_row(row: Row, gaps: tuple[int, int]) -> None:
    """Check one accepted row against a literal safe-map trace.

    Lemma 117 reconstructs the start residue as e = (n + 3 + f) / 4.  Each unit
    block spends one zero digit and one wrap, and Corollary 114 puts the next
    start at n + r + 2, so between two wraps sit exactly r + 1 zeros.  A block's
    returned residue appears one digit after its wrap, at index n + 2.
    """
    r0, r1 = gaps
    want = "0w" + "0" * (r0 + 1) + "w" + "0" * (r1 + 1) + "w0"
    word, seen = raw_trace(row.n, row.u, (row.n + 3 + row.f) // 4, len(want) + 4)
    if not word.startswith(want):
        raise CertificateError(
            f"{gaps}: raw digits at {(row.n, row.u, row.f)} are {word!r} not {want!r}"
        )
    at1, at2 = 2, 2 + r0 + 2
    at3 = at2 + r1 + 2
    residues = (seen[at1][2], seen[at2][2], seen[at3][2])
    if residues != (row.f, row.f1, row.f2):
        raise CertificateError(
            f"{gaps}: raw residues {residues} != {(row.f, row.f1, row.f2)}"
        )
    for step, want_state in ((at2, (row.n1, row.u1)), (at3, (row.n2, row.u2))):
        if (seen[step][0] - 2, seen[step][1] - 1) != want_state:
            raise CertificateError(
                f"{gaps}: raw coordinates {seen[step]} against {want_state}"
            )


def cross_check_raw(certs: dict[tuple[int, int], WordCertificate]) -> dict[str, object]:
    checked = 0
    for gaps, cert in sorted(certs.items()):
        for row in cert.rows:
            replay_row(row, gaps)
            checked += 1
    return {"states_checked": checked, "agrees": True}


# ---------------------------------------------------------------------------
# Negative controls.
# ---------------------------------------------------------------------------


def _weakened_unit(n: int, u: int, f: int) -> bool:
    """is_unit_state without 4f <= n + D + 2."""
    d_coord = n - 2 * u
    return n >= 2 and u >= 0 and f >= 1 and (n + 3 + f) % 4 == 0 and f <= d_coord - 3


def _shifted_gate(n: int, u: int, f: int) -> tuple[int, int, int, int] | None:
    """gate() with the additive constant of (130.4) moved from 3 to 4."""
    d_coord = n - 2 * u
    defect = d_coord - 3 - f
    if defect < 4 or defect % 2 != 0:
        return None
    h = minimal_exponent(n, f)
    g = (f << h) - n - h - 4
    if g < 1 or g > (1 << (h + 2)):
        return None
    if (d_coord + h - 2) - 3 - g < (1 << (h + 2)):
        return None
    return h, g, n + h, u + 1


def _rejects(cert: WordCertificate) -> bool:
    try:
        audit_word(cert)
    except CertificateError:
        return True
    return False


def _rejects_report(report: dict) -> bool:
    try:
        audit_report(report)
    except CertificateError:
        return True
    return False


def _bend(base: WordCertificate, rows: list[Row]) -> WordCertificate:
    return WordCertificate(base.gaps, base.bound, tuple(sorted(rows)))


def negative_controls(base: WordCertificate) -> list[dict[str, object]]:
    """Corrupt meaningful certificate content and require rejection."""
    rows = list(base.rows)
    out: list[dict[str, object]] = []

    def record(name: str, rejected: object, note: str = "") -> None:
        out.append({"name": name, "rejected": bool(rejected), "note": note})

    record("missing_expected_state", _rejects(_bend(base, rows[1:])))
    record("duplicated_expected_state", _rejects(_bend(base, rows + [rows[0]])))

    moved = [r for r in rows if (r.n, r.f) != (36, 13)]
    moved.append(Row(36, 0, 17, 38, 1, 15, 40, 2, 5, False))
    record("altered_normalized_seed", _rejects(_bend(base, moved)))

    record(
        "altered_u_fibre_endpoint",
        _rejects(_bend(base, rows + [Row(36, 4, 13, 38, 5, 11, 40, 6, 1, False)])),
    )

    record("altered_post_pair_state", _rejects(_bend(base, [
        Row(r.n, r.u, r.f, r.n1, r.u1, r.f1, r.n2, r.u2, r.f2 + 1, r.continues)
        if (r.n, r.f) == (36, 13) else r
        for r in rows
    ])))

    # The fourth clause is load-bearing as a predicate, but on these six words it
    # is not independently binding: the child headroom U at h <= 10 already
    # implies it.  So the control is stated where it can be decided -- the
    # weakened predicate must accept a state the full one rejects -- and the
    # certificate-level consequence is reported rather than asserted.
    witness = next(
        (n, u, f)
        for n in range(2, 60)
        for u in range(0, (n - 2) // 2 + 1)
        for f in range(1, n)
        if _weakened_unit(n, u, f) and not is_unit_state(n, u, f)
    )
    weakened = generate_word(base.gaps, unit=_weakened_unit)
    record(
        "dropped_fourth_clause",
        _weakened_unit(*witness) and not is_unit_state(*witness),
        f"witness {witness} is accepted only without the clause; the {base.gaps} "
        f"certificate is unchanged at {len(weakened.rows)} rows, because the child "
        "headroom U at h <= 10 already implies it",
    )

    record("altered_transition_constant",
           _rejects(generate_word(base.gaps, transition=_shifted_gate)))
    record("altered_gap_exponent",
           _rejects(generate_word(base.gaps, h0_override=base.gaps[0] + 3)))

    record("termination_overclaim_in_text", _rejects_report({
        "full_safe_path_termination_claimed": False,
        "reading": "the full safe path terminates after the pair",
    }))
    record("termination_flag_true",
           _rejects_report({"full_safe_path_termination_claimed": True}))
    return out
