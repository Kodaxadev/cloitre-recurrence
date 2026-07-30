#!/usr/bin/env bash
# Run the same checks as .github/workflows/ci.yml, in the same order.
#
# Intended for the pinned Docker image (see Dockerfile), but works on any host
# with the right toolchains on PATH. Every step is fast; the heavy computations
# that back K1-K8 and the N=10^6 certificate are NOT run here, because they take
# hours. Those are listed at the end with their commands.

set -euo pipefail

say() { printf '\n=== %s ===\n' "$1"; }

say "toolchain versions"
rustc --version
cargo --version
python --version
lean --version || true

say "Rust: primary search framework"
cargo test --release --manifest-path search-framework/Cargo.toml

say "Rust: independent verifier"
cargo test --release --manifest-path verification-framework/Cargo.toml
cargo run --release --manifest-path verification-framework/Cargo.toml -- --selftest

say "Python: published OEIS terms"
python verification-framework/verify.py --oeis

say "Python: certificates and bounded checks"
python independent/verify_small_spectrum.py
python independent/verify_safe_certificate.py --n 10000 --max-steps 20000
python independent/verify_safe_checkpoint.py
python independent/verify_safe_block_gates.py
python independent/verify_general_gate_boundaries.py
python independent/verify_parent_gap_dynamics.py
python independent/verify_child_boundary_window.py
python independent/verify_unit_pure_upper.py
python independent/verify_unit_word_rigidity.py
python independent/verify_unit_word_arithmetic.py
python independent/verify_unit_word_composition.py
python independent/verify_unit_determinism.py 200 400 30000
python independent/verify_unit_chain_structure.py 300 1200
python independent/verify_general_gate_determinism.py 220 220
python independent/verify_pure_upper_run.py 500
python independent/verify_block_chain_map.py 200
python independent/verify_admissible_slack.py 200
python independent/verify_sharp_growth.py
python independent/verify_ridge_segments.py
python independent/verify_mixed_ridges.py
python scripts/periodic_phase_blocks.py --max-denominator 501

say "committed artifact hashes"
sha256sum --check <<'HASHES'
7f854fbe4d4978a253d5f9ce43f59d2ae62e3301cc0e946af61b74b18baa08ed  certificates/safe_n1000000.txt
66a06cff15735c4a3caf98575f29afbcd881fbef06334616fbc3bc772b7ab084  certificates/spectrum_m259.csv
41216cd3830cb97fd809b6aa9f78ee8a3e77ce7f13c7a5244d65ebc7c96beeef  independent/verify_safe_certificate.py
a0b60e6d229e56adbba04808130218a807817d5471edfc2f659c253b47370e4b  independent/verify_small_spectrum.py
HASHES

say "Lean: compile and audit axioms"
lake env lean lean/Conjecture.lean
lake env leanchecker Conjecture
bash scripts/check_lean_nanoda.sh

say "Paper: compile the arXiv draft"
if command -v pdflatex >/dev/null 2>&1; then
  bash scripts/build_paper.sh build-a
  bash scripts/build_paper.sh build-b
  python scripts/check_pdf_reproducible.py \
    manuscript/arxiv/build-a/main.pdf manuscript/arxiv/build-b/main.pdf --require
else
  echo "pdflatex not on PATH; skipping."
  echo "The image built with --build-arg WITH_TEX=0 has no LaTeX."
fi

cat <<'NOTE'

=== all fast checks passed ===

NOT run here, because each takes hours. Reproduce individually:

  # K1/K2/K7/K8: the 10^7 census and record sweep
  cargo run --release --manifest-path search-framework/Cargo.toml --bin sweep -- \
      --lo 1 --hi 10000000 --max-n 400000000 --out data/sweep_10M.csv

  # K13: regenerate the N=10^6 safe-map certificate
  cargo run --release --manifest-path search-framework/Cargo.toml --bin pure -- \
      --safe-sweep --n 1000000

  # K15: the deep all-unit pure-upper chain sweep (about an hour at 5e9)
  cargo run --release --manifest-path search-framework/Cargo.toml --bin unit_chain -- \
      5000000000 8

  # K17: the pure-upper run ceiling sweep
  cargo run --release --manifest-path search-framework/Cargo.toml --bin pure_upper_run -- \
      60000 8
NOTE
