#!/usr/bin/env python3
"""Cross-checks and negative controls for the three-gap extension tree.

Two cross-check routes and thirteen corruption controls.

``oracle_extensions`` writes the unit-state predicate out inline, finds gaps by
scanning every ``r`` against Corollary 115 in its own ``r`` coordinates instead
of evaluating ``h* = min{h : 2^h f >= n + h + 4}``, uses no exponent window and
no monotonicity in the wrap count, and classifies each state by whichever word
it actually has.  It shares no code with the extension core.  It is an
*independently transcribed* implementation of C114/C115/T130 -- it is not
mathematically independent of them, and it cannot corroborate them.

``replay_ext_row`` steps the raw safe map digit by digit from its definition and
reads the gaps, residues, indices and wrap counts off the literal trace.  What
the digit word does *not* expose is Corollary 115's pure-upper inequalities --
the parent defect P, the window M and the child headroom U.  The raw map keeps
stepping whether or not a gate is pure-upper, so replay can confirm a gate that
the reduced map accepted but can never confirm that a *missing* fourth gate is
really missing.  Fourth-gate absence is decided by C115, not by digits.
"""

from __future__ import annotations

import json

from unit_gap_extensions_audit import layer_verdicts
from unit_gap_extensions_core import (
    NO_GATE,
    PREFIXES,
    ExtCertificate,
    ExtRow,
    word_order,
)
from unit_gap_words_core import CertificateError, generate_word, start_bound

FORBIDDEN_CLAIMS = (
    "safe path terminates",
    "safe-path termination",
    "full safe path",
    "conjecture is resolved",
    "stabilization conjecture is settled",
)

PROVED_MAX_GAP = 3  # see oracle_extensions for the C114/C115 derivation


def audit_report(report: dict) -> None:
    """The report may record a stopped partial map, never a terminating path.

    The scan is total: it covers the scope disclaimers and the negative-control
    records too, with no exempt block.  That is deliberate, and it constrains how
    this report is allowed to phrase things -- a disclaimer has to be worded so
    that it does not contain the formulation it disclaims.  The offending phrase
    is reported by index rather than quoted, so that a rejection message can
    itself be stored in a report without tripping the same scan.
    """
    if report.get("full_safe_path_termination_claimed") is not False:
        raise CertificateError("report needs full_safe_path_termination_claimed=false")
    blob = json.dumps(report, sort_keys=True).lower()
    for index, phrase in enumerate(FORBIDDEN_CLAIMS):
        if phrase in blob:
            raise CertificateError(
                f"report contains forbidden claim #{index} of {len(FORBIDDEN_CLAIMS)}; "
                "see FORBIDDEN_CLAIMS, not quoted here so the scan stays total"
            )


# ---------------------------------------------------------------------------
# Route 2: a literal (n, U, f) triple loop with no shared discovery.
# ---------------------------------------------------------------------------


def oracle_extensions(bound: int, r_max: int = 24) -> dict[tuple[int, int, int], list[ExtRow]]:
    """Brute force over every (n, U, f), classifying each state by its own word.

    Determinism is a conclusion here, not an assumption: if two gaps ever passed
    at one state this raises instead of picking one.

    ``r_max`` is a scan limit, not a mathematical bound, and the tree it happens
    to find is not the argument for it.  C114 gives ``D_{i+1} = D_i + r_i``; C115
    with ``f_{i+1} >= 1`` gives ``2^(r_i+4) <= D_{i+1} - 4 = D_i + r_i - 4``.  In
    scope ``r0 + r1 <= 2`` and ``D0 = n0 - 2 U0 <= n0 <= 246``, so
    ``D2 = D0 + r0 + r1 <= 248`` and ``r2 = 4`` would need ``256 <= 248``, false:
    hence ``r2 <= 3``.  Then ``D3 = D2 + r2 <= 251`` and ``r3 = 4`` would need
    ``256 <= 251``, false: hence ``r3 <= 3``.  Both are sharp -- ``203`` realizes
    ``r2 = 3``, ``0213`` realizes ``r3 = 3`` -- so no slack is claimed.  Finally
    ``range(r_max)`` scans ``r = 0 .. r_max - 1``, so the default 24 covers
    ``0 .. 23``, strictly containing ``0 .. PROVED_MAX_GAP``; the guard below
    keeps that true if the ceiling is ever lowered.
    """
    if r_max <= PROVED_MAX_GAP:
        raise CertificateError(f"oracle gap ceiling {r_max} scans r <= {r_max - 1}, "
                               f"below the proved domain 0..{PROVED_MAX_GAP}")

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

    def step(n, u, f):
        got = only(n, u, f)
        if got is None:
            return None
        r, nxt = got
        succ = (n + r + 2, u + 1, nxt)
        return (r, succ) if unit(*succ) else None

    buckets: dict[tuple[int, int, int], list[ExtRow]] = {}
    for n in range(2, bound + 1):
        for u in range(0, (n - 4) // 2 + 1):
            for f in range(1, n - 2 * u - 2):
                if not unit(n, u, f):
                    continue
                path, gaps = [(n, u, f)], []
                for _ in range(3):
                    got = step(*path[-1])
                    if got is None:
                        break
                    gaps.append(got[0])
                    path.append(got[1])
                if len(gaps) != 3:
                    continue
                word = (gaps[0], gaps[1], gaps[2])
                if word[:2] not in PREFIXES:
                    continue
                if n > start_bound(*word[:2]):
                    raise CertificateError(
                        f"{word}: start {n} exceeds the proved inherited bound "
                        f"{start_bound(*word[:2])}"
                    )
                nxt4 = step(*path[-1])
                tail = ((False, NO_GATE, NO_GATE, NO_GATE, NO_GATE) if nxt4 is None
                        else (True, nxt4[0]) + nxt4[1])
                buckets.setdefault(word, []).append(
                    ExtRow(*path[0], *path[1], *path[2], *path[3], gaps[2], *tail)
                )
    return {word: sorted(rows) for word, rows in buckets.items()}


def _row_diff(word, mine, theirs) -> str:
    """Row-level, not count-level; both sides are sorted, so the report is stable."""
    missing = sorted(set(theirs) - set(mine))  # oracle has it, certificate does not
    extra = sorted(set(mine) - set(theirs))    # certificate has it, oracle does not
    parts = [f"oracle disagrees on {word}: {len(mine)} certificate rows, "
             f"{len(theirs)} oracle rows, {len(missing)} missing, {len(extra)} extra"]
    parts += [f"first missing from certificate: {missing[0]}"] if missing else []
    parts += [f"first extra in certificate: {extra[0]}"] if extra else []
    return "; ".join(parts)


def cross_check_oracle(certs, bound: int) -> dict[str, object]:
    """Compare word by word.  Every word must lie inside its inherited bound."""
    uncovered = [f"{a}{b}" for a, b in PREFIXES if start_bound(a, b) > bound]
    if uncovered:
        raise CertificateError(f"oracle bound {bound} does not cover {uncovered}")
    buckets = oracle_extensions(bound)
    theirs = {w: tuple(rows) for w, rows in buckets.items()}
    mine = {w: c.rows for w, c in certs.items()}
    if set(theirs) != set(mine):
        raise CertificateError(
            f"oracle words {sorted(set(theirs) - set(mine))} / {sorted(set(mine) - set(theirs))}"
        )
    for word in word_order(mine):
        if mine[word] != theirs[word]:
            raise CertificateError(_row_diff(word, mine[word], theirs[word]))
    return {
        "bound": bound,
        "words_compared": ["".join(map(str, w)) for w in word_order(mine)],
        "states_compared": sum(len(v) for v in mine.values()),
        "agrees": True,
        "independence": "independently transcribed C114/C115/T130, not mathematically independent of them",
    }


# ---------------------------------------------------------------------------
# Route 3: the raw safe map, replayed digit by digit.
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


def _digits(gaps) -> tuple[str, list[int]]:
    """Expected digit word and the index of each wrap, from Corollary 114."""
    word, at, cursor = "0w", [2], 2
    for r in gaps:
        word += "0" * (r + 1) + "w"
        cursor += r + 2
        at.append(cursor)
    return word + "0", at


def replay_ext_row(row: ExtRow, gaps: tuple[int, ...]) -> None:
    """Check one accepted row against a literal safe-map trace.

    Lemma 117 reconstructs the start residue as ``e = (n + 3 + f) / 4``.  Each
    unit block spends one zero digit and one wrap, and Corollary 114 puts the
    next start at ``n + r + 2``, so between two wraps sit exactly ``r + 1``
    zeros, and a block's returned residue appears one digit after its wrap.
    """
    want, at = _digits(gaps)
    states = [(row.n, row.u, row.f), (row.n1, row.u1, row.f1),
              (row.n2, row.u2, row.f2), (row.n3, row.u3, row.f3)]
    if len(gaps) == 4:
        states.append((row.n4, row.u4, row.f4))
    word, seen = raw_trace(row.n, row.u, (row.n + 3 + row.f) // 4, len(want) + 4)
    if not word.startswith(want):
        raise CertificateError(
            f"{gaps}: raw digits at {(row.n, row.u, row.f)} are {word!r} not {want!r}"
        )
    for step, (want_n, want_u, want_f) in zip(at, states):
        got_n, got_u, got_f = seen[step]
        if (got_n - 2, got_u - 1, got_f) != (want_n, want_u, want_f):
            raise CertificateError(
                f"{gaps}: raw state at digit {step} is {(got_n - 2, got_u - 1, got_f)}, "
                f"not {(want_n, want_u, want_f)}"
            )


def cross_check_raw(certs) -> dict[str, object]:
    checked = fourth = 0
    for word in word_order(certs):
        for row in certs[word].rows:
            replay_ext_row(row, word)
            checked += 1
            if row.continues4:
                replay_ext_row(row, word + (row.r3,))
                fourth += 1
    return {
        "states_replayed": checked,
        "fourth_gates_replayed": fourth,
        "agrees": True,
        "not_established_by_replay": (
            "Corollary 115's pure-upper inequalities P, M and U are invisible in "
            "the digit word, so replay cannot confirm that a missing fourth gate "
            "is really missing; that is decided by C115."
        ),
    }


# ---------------------------------------------------------------------------
# Negative controls.
# ---------------------------------------------------------------------------


def _swap(certs, word, rows) -> dict:
    out = dict(certs)
    out[word] = ExtCertificate(word, certs[word].inherited_bound, tuple(sorted(rows)))
    return out


def _rebound(certs, word, bound) -> dict:
    out = dict(certs)
    out[word] = ExtCertificate(word, bound, certs[word].rows)
    return out


def _edit(row: ExtRow, **kw) -> ExtRow:
    fields = {f: getattr(row, f) for f in ExtRow.__dataclass_fields__}
    fields.update(kw)
    return ExtRow(**fields)


def _record(name, mutation, intended, certs, source) -> dict[str, object]:
    verdicts = layer_verdicts(certs, source)
    hits = [n for n, rejected, _ in verdicts if rejected]
    message = next((m for _, rejected, m in verdicts if rejected), "")
    return {
        "name": name,
        "mutation": mutation,
        "intended_layer": intended,
        "first_rejecting_layer": hits[0] if hits else "",
        "also_rejected_by": hits[1:],
        "rejected": bool(hits),
        "error": message[:160],
    }


def _record_report(name, mutation, intended, report) -> dict[str, object]:
    try:
        audit_report(report)
        return {"name": name, "mutation": mutation, "intended_layer": intended,
                "first_rejecting_layer": "", "also_rejected_by": [],
                "rejected": False, "error": ""}
    except CertificateError as exc:
        return {"name": name, "mutation": mutation, "intended_layer": intended,
                "first_rejecting_layer": "report-audit", "also_rejected_by": [],
                "rejected": True, "error": str(exc)[:160]}


def negative_controls(certs, source) -> list[dict[str, object]]:
    """Corrupt meaningful content and require rejection by an identified layer.

    ``intended`` is the layer expected to reject *first* under the implemented
    AUDIT_LAYERS order, not necessarily the layer the mutation aims at.
    """
    word = (1, 0, 1)          # 21 states, 2 seeds, 16 with a fourth gate
    rows = list(certs[word].rows)
    tall = max(certs[word].u_ranges.items(), key=lambda kv: len(kv[1]))[0]
    top = max(r for r in rows if (r.n, r.f) == tall)
    fourth = next(r for r in rows if r.continues4)
    out = []

    out.append(_record("removed_state", "drop the U=0 row of the first seed",
                       "u-fibre", _swap(certs, word, rows[1:]), source))
    out.append(_record("duplicated_state", "append an existing row a second time",
                       "duplicate", _swap(certs, word, rows + [rows[0]]), source))
    out.append(_record("altered_r2", "set r2 := r2 + 1 on one row", "row-rebuild",
                       _swap(certs, word, [_edit(r, r2=r.r2 + 1) if r is rows[0] else r
                                           for r in rows]), source))
    out.append(_record("altered_third_residue", "set f3 := f3 + 4 on one row",
                       "row-rebuild",
                       _swap(certs, word, [_edit(r, f3=r.f3 + 4) if r is rows[0] else r
                                           for r in rows]), source))
    out.append(_record("altered_third_index", "set n3 := n3 + 2 on one row",
                       "row-rebuild",
                       _swap(certs, word, [_edit(r, n3=r.n3 + 2) if r is rows[0] else r
                                           for r in rows]), source))
    out.append(_record("truncated_u_fibre", f"drop the top U of the fibre at {tall}",
                       "u-fibre", _swap(certs, word, [r for r in rows if r is not top]),
                       source))
    out.append(_record("extended_u_fibre", f"append an invalid U above the fibre at {tall}",
                       "row-rebuild",  # 0..k+1 still reads as a 0.. prefix: u-fibre never fires
                       _swap(certs, word, rows + [_edit(top, u=top.u + 1)]), source))
    out.append(_record("flipped_fourth_flag", "negate continues4 on one row",
                       "row-rebuild",
                       _swap(certs, word, [_edit(r, continues4=not r.continues4)
                                           if r is fourth else r for r in rows]), source))
    out.append(_record("altered_r3", "set r3 := r3 + 1 on a fourth-continuing row",
                       "row-rebuild",
                       _swap(certs, word, [_edit(r, r3=r.r3 + 1) if r is fourth else r
                                           for r in rows]), source))

    stray = next(r for r in generate_word((0, 0)).rows if not r.continues)
    imported = ExtRow(stray.n, stray.u, stray.f, stray.n1, stray.u1, stray.f1,
                      stray.n2, stray.u2, stray.f2, stray.n2 + 2, stray.u2 + 1, 1,
                      0, False, NO_GATE, NO_GATE, NO_GATE, NO_GATE)
    injected = dict(certs)
    injected[(0, 0, 0)] = ExtCertificate((0, 0, 0), start_bound(0, 0), (imported,))
    out.append(_record("imported_noncontinuing_k18_state",
                       f"inject the noncontinuing 00 state {(stray.n, stray.u, stray.f)}",
                       "row-rebuild",  # fails the row rebuild before k18-source runs
                       injected, source))

    out.append(_record("weakened_inherited_bound", "raise the inherited bound by 64",
                       "bound", _rebound(certs, word, certs[word].inherited_bound + 64),
                       source))

    out.append(_record_report("termination_overclaim_in_text",
                              "prose asserting the whole trajectory halts after the third gate",
                              "report-audit",
                              {"full_safe_path_termination_claimed": False,
                               "reading": "the full safe path terminates after the third gate"}))
    out.append(_record_report("termination_flag_true",
                              "set full_safe_path_termination_claimed = true",
                              "report-audit",
                              {"full_safe_path_termination_claimed": True}))
    return out
