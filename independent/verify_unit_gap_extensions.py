#!/usr/bin/env python3
"""The three-gap extension tree above the K18 two-gap certificates.

Canonical use:

    python independent/verify_unit_gap_extensions.py
    python independent/verify_unit_gap_extensions.py --report artifacts/unit-gap-extensions.json

The default run does the whole job: it regenerates and re-audits K18, reproduces
its 342 third-gate inputs by exact row identity, discovers every realized
three-gap word, expands every U-fibre, cross-checks against a full literal
(n, U, f) oracle and against a raw safe-map replay, classifies the fourth-gate
frontier, and runs thirteen negative controls.  No flag weakens any of that.

What the result is.  A bounded exhaustive computation, exhaustive because the
first two gaps already pin the start index to K18's proved bound
``n0 <= 2^(r0+r1+6) - r0 - r1 - 8`` and the wrap count to the unit-state
ceiling.  No new search ceiling is introduced: Theorem 130 forces the third and
fourth gaps, so r2 and r3 are read off rather than searched for.

What the result is not.  Where a fourth gate is absent, Theorem 130's all-unit
pure-upper *partial map* is undefined at that state.  That is not termination of
the safe trajectory.  Other block lengths and non-pure-upper gates are never
examined, reachability from an original start b1 = m is not addressed, and the
Cloitre stabilization conjecture is untouched.  None of those is claimed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

# The sibling modules below hold the definitions, the audit and the cross-checks.
# Put this file's own directory on the path explicitly: the implicit
# script-directory entry is suppressed by `python -P` and by PYTHONSAFEPATH.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from unit_gap_extensions_audit import audit_certificates, k18_source
from unit_gap_extensions_checks import (
    audit_report,
    cross_check_oracle,
    cross_check_raw,
    negative_controls,
)
from unit_gap_extensions_core import (
    INHERITED_BOUNDS,
    K18_REGISTRATION_COMMIT,
    K18_REPORT_SHA256,
    K18_VERIFIER_COMMIT,
    MERGED_BASE_COMMIT,
    PREFIXES,
    CertificateError,
    build_certificates,
    word_order,
)

#: What the certificate may not be read as establishing.  Worded to avoid the
#: exact formulations in FORBIDDEN_CLAIMS, because ``audit_report`` scans the
#: whole report including these lines and cannot tell a disclaimer from a claim.
SCOPE_LIMITS = (
    "does not establish that the safe trajectory halts",
    "does not establish universal termination of all-unit pure-upper chains",
    "does not establish reachability from an original recurrence start b1 = m",
    "does not exclude longer-block or non-pure-upper continuation",
    "does not resolve the Cloitre stabilization conjecture",
)


def _key(word) -> str:
    return "".join(str(g) for g in word)


def four_gap_frontier(certs) -> dict[str, object]:
    """Group the fourth-continuing states by realized four-gap prefix.

    A frontier report, not a four-gap certificate: nothing here recurses to a
    fifth gate, and a missing fourth gate is not termination of anything.
    """
    groups: dict[tuple[int, ...], list] = {}
    for word in word_order(certs):
        for row in certs[word].rows:
            if row.continues4:
                groups.setdefault(word + (row.r3,), []).append(row)
    return {
        _key(w): {
            "gaps": list(w),
            "states": len(groups[w]),
            "normalized_seeds": sorted({(r.n, r.f) for r in groups[w]}),
            "fourth_successors": sorted({(r.n4, r.u4, r.f4) for r in groups[w]}),
        }
        for w in word_order(groups)
    }


def build_report(certs, source_counts, k18_audit, oracle, raw, controls) -> dict:
    words: dict[str, object] = {}
    for word in word_order(certs):
        cert = certs[word]
        words[_key(word)] = {
            "gaps": list(word),
            "k18_prefix": _key(cert.prefix),
            "inherited_start_bound": cert.inherited_bound,
            "normalized_seeds": [list(s) for s in cert.seeds],
            "normalized_seed_count": len(cert.seeds),
            "u_fibres": {
                f"{n},{f}": [min(w), max(w)] for (n, f), w in sorted(cert.u_ranges.items())
            },
            "state_count": len(cert.rows),
            "unique_state_count": len(set(cert.states)),
            "fourth_continuing_count": cert.fourth_continuing,
            "realized_r3": list(cert.r3_values),
            "fourth_gate_undefined_for_every_state": cert.fourth_continuing == 0,
            "states": [
                [r.n, r.u, r.f, r.n1, r.u1, r.f1, r.n2, r.u2, r.f2,
                 r.n3, r.u3, r.f3, r.continues4, r.r3, r.n4, r.u4, r.f4]
                for r in cert.rows
            ],
        }
    return {
        "schema": "unit-gap-extensions/1",
        "source": {
            "merged_base_commit": MERGED_BASE_COMMIT,
            "k18_verifier_commit": K18_VERIFIER_COMMIT,
            "k18_registration_commit": K18_REGISTRATION_COMMIT,
            "k18_report_sha256": K18_REPORT_SHA256,
            "provenance_only": "regenerated and re-audited here; never read back to decide anything",
        },
        "inherited_bounds": {f"{a}{b}": INHERITED_BOUNDS[(a, b)] for a, b in PREFIXES},
        "bound_formula": "n0 <= 2^(r0+r1+6) - r0 - r1 - 8, inherited from the two-gap prefix",
        "source_two_gap_counts": source_counts,
        "source_continuing_count": k18_audit["third_gate_inputs"],
        "k18_source_reproduction": k18_audit,
        "word_order": [_key(w) for w in word_order(certs)],
        "state_row_fields": [
            "n", "U", "f", "n1", "U1", "f1", "n2", "U2", "f2", "n3", "U3", "f3",
            "fourth_gate_exists", "r3", "n4", "U4", "f4",
        ],
        "absent_value": -1,
        "three_gap_words": words,
        "three_gap_word_count": len(certs),
        "three_gap_seed_total": sum(len(c.seeds) for c in certs.values()),
        "three_gap_state_total": sum(len(c.rows) for c in certs.values()),
        "fourth_continuing_total": sum(c.fourth_continuing for c in certs.values()),
        "four_gap_frontier": four_gap_frontier(certs),
        "oracle": oracle,
        "raw_replay": raw,
        "negative_controls": controls,
        "full_safe_path_termination_claimed": False,
        "evidence_class": "bounded exhaustive computation inside a proved inherited bound",
        "scope_limits": list(SCOPE_LIMITS),
        "reading": (
            "Within the inherited K18 start bounds these are all the unit states "
            "carrying each realized three-gap word, together with every wrap "
            "count. Where no fourth gate exists the partial map of Theorem 130 is "
            "undefined, so the all-unit pure-upper mechanism has no continuation "
            "there. Other block lengths and non-pure-upper gates are not examined, "
            "so nothing here decides a trajectory."
        ),
    }


def write_report(report: dict, path: Path) -> tuple[int, str]:
    """Serialize deterministically: sorted keys, ASCII, LF, one trailing newline."""
    blob = (
        json.dumps(
            report, sort_keys=True, indent=2, separators=(",", ": "), ensure_ascii=True
        )
        + "\n"
    ).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as handle:  # binary, so no platform newline rewriting
        handle.write(blob)
    return len(blob), hashlib.sha256(blob).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Classify the third gap of every K18 state that has one."
    )
    parser.add_argument("--report", type=Path, help="write the deterministic JSON here")
    parser.add_argument(
        "--oracle-bound",
        type=int,
        default=max(INHERITED_BOUNDS.values()),
        help="brute-force cross-check bound; must cover every inherited bound",
    )
    args = parser.parse_args(argv)

    clock = time.perf_counter()
    source, source_counts = k18_source()
    print(
        f"K18 source: {sum(len(v) for v in source.values())} third-gate inputs from "
        f"{sum(c['states'] for c in source_counts.values())} two-gap states "
        f"[{time.perf_counter() - clock:.2f}s]"
    )

    clock = time.perf_counter()
    certs = build_certificates()
    k18_audit = audit_certificates(certs, source)
    print(
        f"extension tree: {len(certs)} realized three-gap words, "
        f"{sum(len(c.seeds) for c in certs.values())} normalized seeds, "
        f"{sum(len(c.rows) for c in certs.values())} states "
        f"[{time.perf_counter() - clock:.2f}s]"
    )
    for word in word_order(certs):
        cert = certs[word]
        print(
            f"  word {_key(word)}: n0<={cert.inherited_bound}, {len(cert.seeds)} seeds, "
            f"{len(cert.rows)} states, {cert.fourth_continuing} with a fourth gate"
            + (f", r3 in {list(cert.r3_values)}" if cert.r3_values else "")
        )
    print(
        f"U-fibres: {k18_audit['fibres']} fibres, max U {k18_audit['max_u']}, "
        f"{k18_audit['u_values_rescanned']} wrap counts rescanned above the prefixes"
    )

    clock = time.perf_counter()
    oracle = cross_check_oracle(certs, args.oracle_bound)
    print(
        f"oracle n<={args.oracle_bound}: exact agreement on "
        f"{len(oracle['words_compared'])} words, {oracle['states_compared']} states "
        f"[{time.perf_counter() - clock:.2f}s]"
    )

    clock = time.perf_counter()
    raw = cross_check_raw(certs)
    print(
        f"literal safe-map replay: {raw['states_replayed']} states and "
        f"{raw['fourth_gates_replayed']} fourth gates agree "
        f"[{time.perf_counter() - clock:.2f}s]"
    )

    clock = time.perf_counter()
    controls = negative_controls(certs, source)
    unrejected = [c["name"] for c in controls if not c["rejected"]]
    if unrejected:
        raise CertificateError(f"negative controls did not reject: {unrejected}")
    print(
        f"negative controls: {len(controls)} corruptions all rejected "
        f"[{time.perf_counter() - clock:.2f}s]"
    )

    report = build_report(certs, source_counts, k18_audit, oracle, raw, controls)
    audit_report(report)
    if args.report:
        size, digest = write_report(report, args.report)
        print(f"report: {args.report} ({size} bytes, sha256 {digest})")

    frontier = report["four_gap_frontier"]
    print(
        "fourth-gate frontier: "
        + ", ".join(f"{k}={v['states']}" for k, v in frontier.items())
        + f" ({report['fourth_continuing_total']} states total)"
    )
    print(
        "VERDICT: within the inherited K18 bounds these are every unit state "
        "carrying each realized three-gap word. Where the fourth gate is missing "
        "the all-unit pure-upper partial map is undefined; that is not "
        "termination of the safe trajectory, and none is claimed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
