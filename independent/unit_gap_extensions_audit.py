#!/usr/bin/env python3
"""Layered audit of the three-gap extension certificates.

Each check is a separate named layer rather than one long function, so that a
negative control can report *which* layer actually caught it and which other
layers would also have caught it.  A control that merely produces a nonzero exit
is not evidence that the layer it targets works.

Import direction is one-way: ``verify_unit_gap_extensions`` ->
``unit_gap_extensions_checks`` -> this module -> ``unit_gap_extensions_core`` ->
``unit_gap_words_core``.
"""

from __future__ import annotations

from unit_gap_extensions_core import (
    PREFIXES,
    build_certificates,
    direct_seeds,
    three_gap_chain,
)
from unit_gap_words_core import (
    CertificateError,
    Row,
    audit_word,
    generate_word,
    start_bound,
    u_ceiling,
)


def k18_source() -> tuple[dict[tuple[int, int], tuple[Row, ...]], dict[str, dict]]:
    """Regenerate and re-audit K18, returning its continuing rows and its counts.

    The merged two-gap verifier is re-run here rather than trusted.  Its commit
    SHAs and report hash are carried in the report as provenance only; nothing
    reads them back to decide anything.
    """
    continuing: dict[tuple[int, int], tuple[Row, ...]] = {}
    counts: dict[str, dict] = {}
    for prefix in PREFIXES:
        cert = generate_word(prefix)
        audit_word(cert)
        continuing[prefix] = tuple(r for r in cert.rows if r.continues)
        counts[f"{prefix[0]}{prefix[1]}"] = {
            "start_bound": cert.bound,
            "normalized_seeds": len(cert.seeds),
            "states": len(cert.rows),
            "continuing": cert.continuing,
        }
    return continuing, counts


def _layer_bound(certs, source, stats) -> None:
    for word, cert in certs.items():
        if cert.inherited_bound != start_bound(*cert.prefix):
            raise CertificateError(
                f"{word}: bound {cert.inherited_bound} is not the inherited K18 bound"
            )


def _layer_sorted(certs, source, stats) -> None:
    for word, cert in certs.items():
        if list(cert.rows) != sorted(cert.rows):
            raise CertificateError(f"{word}: rows are not canonically sorted")


def _layer_duplicate(certs, source, stats) -> None:
    for word, cert in certs.items():
        states = cert.states
        if len(states) != len(set(states)):
            raise CertificateError(f"{word}: duplicate (n, U, f) in the state list")


def _layer_row(certs, source, stats) -> None:
    """Rebuild every row from the definitions and demand exact equality."""
    for word, cert in certs.items():
        for row in cert.rows:
            if not 2 <= row.n <= cert.inherited_bound:
                raise CertificateError(
                    f"{word}: start {row.n} outside [2, {cert.inherited_bound}]"
                )
            rebuilt = three_gap_chain(row.n, row.u, row.f, cert.prefix)
            if rebuilt is None:
                raise CertificateError(
                    f"{word}: {(row.n, row.u, row.f)} fails the three-gap word"
                )
            if rebuilt.r2 != word[2]:
                raise CertificateError(
                    f"{word}: {(row.n, row.u, row.f)} realizes r2={rebuilt.r2}, not {word[2]}"
                )
            if rebuilt != row:
                raise CertificateError(
                    f"{word}: {(row.n, row.u, row.f)} row mismatch, got {rebuilt}"
                )


def _layer_fibre(certs, source, stats) -> None:
    """Every fibre is an unbroken 0.. prefix with nothing valid above it.

    The rescan runs to the unit-state ceiling, above which ``f <= D - 3`` fails
    unconditionally, so it is exhaustive rather than a sample.  This is what
    makes ``expand_fibre``'s early break safe rather than merely plausible.
    """
    stats["fibres"] = 0
    stats["max_u"] = 0
    stats["u_values_rescanned"] = 0
    for word, cert in certs.items():
        for (n, f), wraps in cert.u_ranges.items():
            stats["fibres"] += 1
            stats["max_u"] = max(stats["max_u"], max(wraps))
            if wraps != tuple(range(len(wraps))):
                raise CertificateError(f"{word}: fibre at {(n, f)} is not a 0.. prefix")
            for u in range(len(wraps), u_ceiling(n, f) + 1):
                stats["u_values_rescanned"] += 1
                if three_gap_chain(n, u, f, cert.prefix) is not None:
                    raise CertificateError(f"{word}: fibre at {(n, f)} misses U={u}")


def _layer_seed_r2(certs, source, stats) -> None:
    """r2 depends only on (n, f): Lemma 131 claim 1 keeps U out of the orbit."""
    by_seed: dict[tuple[tuple[int, int], int, int], set[int]] = {}
    for word, cert in certs.items():
        for (n, f) in cert.seeds:
            by_seed.setdefault((cert.prefix, n, f), set()).add(word[2])
    split = {k: sorted(v) for k, v in by_seed.items() if len(v) > 1}
    if split:
        raise CertificateError(f"r2 varies inside a seed: {sorted(split.items())[:2]}")


def _layer_k18_source(certs, source, stats) -> None:
    """The extension start set must be exactly K18's continuing set.

    Catches a missing continuing state, an extra state, a changed successor, a
    flipped continuation flag, a duplicate, and a state sourced from a K18 word
    that has no third gate at all.
    """
    seen: dict[tuple[int, int], list[Row]] = {p: [] for p in PREFIXES}
    for cert in certs.values():
        if cert.prefix not in seen:
            raise CertificateError(f"{cert.word}: prefix is not one of the six K18 words")
        for row in cert.rows:
            seen[cert.prefix].append(row.two_gap_row)
    total = 0
    for prefix in PREFIXES:
        mine, theirs = seen[prefix], source[prefix]
        if len(mine) != len(set(mine)):
            raise CertificateError(f"{prefix}: duplicate K18 source row in the extension set")
        missing = sorted(set(theirs) - set(mine))
        extra = sorted(set(mine) - set(theirs))
        if missing:
            raise CertificateError(
                f"{prefix}: {len(missing)} K18 continuing rows missing, e.g. {missing[0]}"
            )
        if extra:
            raise CertificateError(
                f"{prefix}: {len(extra)} rows outside the K18 continuing set, e.g. {extra[0]}"
            )
        total += len(theirs)
    stats["third_gate_inputs"] = total


def _layer_completeness(certs, source, stats) -> None:
    """Completeness from the definitions rather than from the exponent window.

    Sweeping to twice the inherited bound does two jobs: it confirms the seed set
    is exactly what a window-free sweep finds, and it confirms the inherited
    bound actually binds instead of merely sitting above the data.
    """
    for prefix in PREFIXES:
        mine = tuple(sorted(
            (n, f, w[2])
            for w, c in certs.items() if c.prefix == prefix
            for (n, f) in c.seeds
        ))
        bound = start_bound(*prefix)
        margin = direct_seeds(prefix, 2 * bound + 2)
        above = sorted(s for s in margin if s[0] > bound)
        if above:
            raise CertificateError(f"{prefix}: seeds above the inherited bound: {above[:4]}")
        if tuple(sorted(margin)) != mine:
            missing = sorted(set(margin) - set(mine))
            extra = sorted(set(mine) - set(margin))
            raise CertificateError(
                f"{prefix}: window-free sweep disagrees; missing {missing[:3]}, extra {extra[:3]}"
            )


def _layer_regeneration(certs, source, stats) -> None:
    fresh = build_certificates()
    if {w: c.rows for w, c in fresh.items()} != {w: c.rows for w, c in certs.items()}:
        raise CertificateError("regeneration does not reproduce the certificates")


#: Ordered audit layers.
AUDIT_LAYERS: tuple[tuple[str, object], ...] = (
    ("bound", _layer_bound),
    ("sorted", _layer_sorted),
    ("duplicate", _layer_duplicate),
    ("row-rebuild", _layer_row),
    ("u-fibre", _layer_fibre),
    ("seed-r2", _layer_seed_r2),
    ("k18-source", _layer_k18_source),
    ("completeness", _layer_completeness),
    ("regeneration", _layer_regeneration),
)


def audit_certificates(certs, source) -> dict[str, object]:
    """Run every layer in order.  Raises on the first disagreement."""
    stats: dict[str, object] = {}
    for _, layer in AUDIT_LAYERS:
        layer(certs, source, stats)
    stats["layers"] = [name for name, _ in AUDIT_LAYERS]
    stats["all_layers_pass"] = True
    return stats


def layer_verdicts(certs, source) -> list[tuple[str, bool, str]]:
    """Run every layer independently.  Used only by the negative controls.

    Returns ``(layer, rejected, message)`` for each layer, so a control can name
    the first layer that catches it and every other layer that also would.
    """
    out: list[tuple[str, bool, str]] = []
    for name, layer in AUDIT_LAYERS:
        try:
            layer(certs, source, {})
            out.append((name, False, ""))
        except CertificateError as exc:
            out.append((name, True, str(exc)))
        except (IndexError, KeyError, ValueError, TypeError) as exc:
            out.append((name, True, f"{type(exc).__name__}: {exc}"))
    return out
