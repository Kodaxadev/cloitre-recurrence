#!/usr/bin/env python3
"""Independent finite certificates for the short all-unit pure-upper gap words.

Canonical use:

    python independent/verify_unit_gap_words.py
    python independent/verify_unit_gap_words.py --report artifacts/unit-gap-words.json

The default run does the whole job: all six gap words with r0 + r1 <= 2, the 00
specification cross-check, a brute-force oracle over the entire range, a literal
safe-map replay of every accepted state, and ten negative controls.  No flag
weakens any of that.

The definitions and the exhaustive enumeration are in ``unit_gap_words_core``;
the two independent oracles and the controls are in ``unit_gap_words_checks``.
No project code outside those two modules is imported.

What the result is.  Each word's certificate is a bounded exhaustive
computation: within the displayed start bound these are all the unit states
carrying that word.  Where the third gate is absent the *partial map* of Theorem
130 is undefined, so the all-unit pure-upper mechanism has no continuation
there.  That is not termination of the safe trajectory -- other block lengths
and non-pure-upper gates are never examined -- and no such claim is made.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

# The two siblings below hold the definitions and the cross-checks. Put this
# file's own directory on the path explicitly: the implicit script-directory
# entry is suppressed by `python -P` and by PYTHONSAFEPATH, and every other
# verifier in this directory is a single self-contained file that does not care.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from unit_gap_words_checks import (
    audit_report,
    cross_check_oracle,
    cross_check_raw,
    negative_controls,
)
from unit_gap_words_core import (
    REQUIRED_WORDS,
    CertificateError,
    WordCertificate,
    audit_word,
    generate_word,
    start_bound,
)

# Specification expectations for the 00 word, quoted from the verifier contract.
# Nothing consults them while generating; they are compared afterwards.
EXPECTED_SEEDS = ((36, 13), (39, 14), (42, 15), (45, 16), (48, 17), (51, 18))
EXPECTED_U_RANGES = {
    (36, 13): range(0, 4),
    (39, 14): range(0, 5),
    (42, 15): range(0, 6),
    (45, 16): range(0, 7),
    (48, 17): range(0, 8),
    (51, 18): range(0, 9),
}
EXPECTED_POST_PAIR = {
    (36, 13): (40, 1),
    (39, 14): (43, 2),
    (42, 15): (46, 3),
    (45, 16): (49, 4),
    (48, 17): (52, 5),
    (51, 18): (55, 6),
}
EXPECTED_STATE_COUNT = 39


def audit_zero_zero(cert: WordCertificate) -> dict[str, object]:
    """Compare the generated 00 certificate with the contract's expectations."""
    if cert.gaps != (0, 0):
        raise CertificateError("audit_zero_zero applied to the wrong word")
    bad: list[str] = []
    if cert.seeds != EXPECTED_SEEDS:
        bad.append(f"seeds {cert.seeds} != {EXPECTED_SEEDS}")
    if cert.u_ranges != {k: tuple(v) for k, v in EXPECTED_U_RANGES.items()}:
        bad.append(f"u fibres {sorted(cert.u_ranges.items())}")
    if cert.post_pair != EXPECTED_POST_PAIR:
        bad.append(f"post-pair {sorted(cert.post_pair.items())}")
    if len(cert.rows) != EXPECTED_STATE_COUNT:
        bad.append(f"state count {len(cert.rows)} != {EXPECTED_STATE_COUNT}")
    if len(set(cert.states)) != EXPECTED_STATE_COUNT:
        bad.append(f"unique state count {len(set(cert.states))}")
    if cert.continuing:
        bad.append(f"{cert.continuing} states have a third all-unit gate")
    if bad:
        raise CertificateError("00 specification mismatch: " + "; ".join(bad))
    return {
        "seeds_match": True,
        "u_ranges_match": True,
        "post_pair_match": True,
        "state_count": EXPECTED_STATE_COUNT,
        "unique_state_count": EXPECTED_STATE_COUNT,
        "third_all_unit_gate_undefined_for_every_state": True,
    }


# ---------------------------------------------------------------------------
# Deterministic report.
# ---------------------------------------------------------------------------


def build_report(certs, zero_zero, oracle, raw, controls) -> dict:
    words: dict[str, object] = {}
    for gaps, cert in sorted(certs.items()):
        words[f"{gaps[0]}{gaps[1]}"] = {
            "gaps": list(gaps),
            "start_bound": cert.bound,
            "normalized_seeds": [list(s) for s in cert.seeds],
            "normalized_seed_count": len(cert.seeds),
            "u_fibres": {
                f"{n},{f}": [min(w), max(w)]
                for (n, f), w in sorted(cert.u_ranges.items())
            },
            "post_pair": {
                f"{n},{f}": list(v) for (n, f), v in sorted(cert.post_pair.items())
            },
            "state_count": len(cert.rows),
            "unique_state_count": len(set(cert.states)),
            "continuing_state_count": cert.continuing,
            "all_unit_map_undefined_for_every_state": cert.continuing == 0,
            "states": [
                [r.n, r.u, r.f, r.n1, r.u1, r.f1, r.n2, r.u2, r.f2, r.continues]
                for r in cert.rows
            ],
        }
    return {
        "schema": "unit-gap-words/1",
        "word_order": [f"{a}{b}" for a, b in REQUIRED_WORDS],
        "state_row_fields": [
            "n", "U", "f", "n1", "U1", "f1", "n2", "U2", "f2", "third_gate_exists",
        ],
        "bound_formula": "n0 <= 2^(r0+r1+6) - r0 - r1 - 8",
        "words": words,
        "zero_zero_specification": zero_zero,
        "oracle_cross_check": oracle,
        "raw_safe_map_replay": raw,
        "negative_controls": controls,
        "full_safe_path_termination_claimed": False,
        "evidence_class": "bounded exhaustive computation",
        "reading": (
            "Within each displayed start bound these are all the unit states "
            "carrying the word. Where no third gate exists the partial map of "
            "Theorem 130 is undefined, so the all-unit pure-upper mechanism has "
            "no continuation there. Other block lengths and non-pure-upper gates "
            "are not examined, so nothing here decides a trajectory."
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


# ---------------------------------------------------------------------------
# Entry point.
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Enumerate every unit state carrying a short pure-upper gap word."
    )
    parser.add_argument("--report", type=Path, help="write the deterministic JSON here")
    parser.add_argument(
        "--oracle-bound",
        type=int,
        default=max(start_bound(*w) for w in REQUIRED_WORDS),
        help="brute-force cross-check bound; must cover every required word",
    )
    args = parser.parse_args(argv)

    certs: dict[tuple[int, int], WordCertificate] = {}
    for gaps in REQUIRED_WORDS:
        clock = time.perf_counter()
        cert = generate_word(gaps)
        audit_word(cert)
        certs[gaps] = cert
        print(
            f"word {gaps[0]}{gaps[1]}: n0<={cert.bound}, {len(cert.seeds)} normalized "
            f"seeds, {len(cert.rows)} states, {cert.continuing} with a third gate "
            f"[{time.perf_counter() - clock:.2f}s]"
        )

    zero_zero = audit_zero_zero(certs[(0, 0)])
    print(
        f"00 specification: {len(EXPECTED_SEEDS)} seeds, {EXPECTED_STATE_COUNT} "
        "distinct states, two zero gaps, no third all-unit gate"
    )

    clock = time.perf_counter()
    oracle = cross_check_oracle(certs, args.oracle_bound)
    print(
        f"oracle n<={args.oracle_bound}: exact agreement on "
        f"{len(oracle['words_compared'])} words [{time.perf_counter() - clock:.2f}s]"
    )

    clock = time.perf_counter()
    raw = cross_check_raw(certs)
    print(
        f"literal safe-map replay: {raw['states_checked']} states agree "
        f"[{time.perf_counter() - clock:.2f}s]"
    )

    clock = time.perf_counter()
    controls = negative_controls(certs[(0, 0)])
    unrejected = [c["name"] for c in controls if not c["rejected"]]
    if unrejected:
        raise CertificateError(f"negative controls did not reject: {unrejected}")
    print(
        f"negative controls: {len(controls)} corruptions all rejected "
        f"[{time.perf_counter() - clock:.2f}s]"
    )

    report = build_report(certs, zero_zero, oracle, raw, controls)
    audit_report(report)
    if args.report:
        size, digest = write_report(report, args.report)
        print(f"report: {args.report} ({size} bytes, sha256 {digest})")

    print(
        "VERDICT: within the displayed bounds these are every unit state carrying "
        "each of the six gap words. Where the third gate is missing the all-unit "
        "pure-upper partial map is undefined; that is not termination of the safe "
        "trajectory, and none is claimed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
