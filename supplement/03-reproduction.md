# Reproduction commands

Commands assume PowerShell, Rust 1.94.0, Python 3, and Lean 4.32.1.

## Source identity

```powershell
git rev-parse HEAD
git show --stat --oneline f19ffcd75d04a05529878ce0226088f2f3221c0b
```

The frozen research snapshot is the named commit. Audit documents may appear
in later commits.

## Test suites

```powershell
Set-Location search-framework
cargo test --release

Set-Location ..\verification-framework
cargo test --release
cargo run --release -- --selftest
python verify.py --oeis

Set-Location ..
lean lean\Conjecture.lean
```

Expected at the freeze: all Rust tests pass, OEIS checks pass, and Lean exits
zero without `sorryAx`.

## Complete \(10^7\) census

```powershell
Set-Location search-framework
cargo run --release --bin sweep -- `
  --lo 1 --hi 10000000 --max-n 2000000000

cargo run --release --bin record -- `
  --lo 1 --hi 10000000 --out ..\data\census_10M.regenerated.csv
```

Compare the regenerated file with the manifest-bound census by SHA-256 and
numeric content. Do not overwrite the frozen artifact.

## Minimal nonsurjectivity certificate

```powershell
python independent\verify_small_spectrum.py
Get-FileHash -Algorithm SHA256 certificates\spectrum_m259.csv
```

Expected SHA-256:

```text
66a06cff15735c4a3caf98575f29afbcd881fbef06334616fbc3bc772b7ab084
```

This 259-row check, together with Theorem 18, is sufficient for the claim that
5 and 7 are the smallest missing increments.

## Independent row verification

```powershell
Set-Location verification-framework
cargo run --release -- `
  --csv ..\data\scan_200k.csv --stride 1 --threads 16 --tail 64

python verify.py --csv ..\data\scan_200k.csv `
  --sample 4000 --seed 20260728 --tail 200
```

The two large `scan_*.csv` files are intentionally ignored by Git but are bound
by hashes in the evidence manifest.

## Periodic-family certificate

```powershell
python scripts\periodic_phase_blocks.py --max-denominator 501
```

Expected terminal values:

```text
families checked: 463
denominators with no boundary family: 81
phase-integral subset patterns: 0
certificate sha256:
1508d04cc91c8a007d17028efb24fe726785f4f210272721d8fc7f6149d4bb06
```

## Safe-map certificate

```powershell
Set-Location search-framework
cargo run --release --bin pure -- `
  --n 1000000 --max-steps 20000 --safe-sweep
```

Expected terminal values are listed in `02-certificates.md`. The audit requires
agreement with the independent generator:

```powershell
Set-Location ..
python independent\verify_safe_certificate.py `
  --n 1000000 --max-steps 20000
```

Both outputs must report trajectory digest `0xffe3df00b02fcb2d`.

## Post-down ridge probe

To exhaust every down-step state with \(q\le752\) at index \(10^4\), then
measure the positive no-down segment beginning immediately afterward:

```powershell
cargo run --release --manifest-path search-framework\Cargo.toml `
  --bin ridge -- --n 10000 --max-q 752 `
  --min-steps 50 --max-steps 20000
```

Use `--max-r 0` for a deliberately restricted boundary-residue probe. Output
from this command is exploratory and is not a certificate or theorem.

## Mixed-ridge identities

Run the arbitrary-precision raw-state checker:

```powershell
python independent\verify_mixed_ridges.py
```

Expected principal counts:

```text
mixed-ridge finite segments checked: 6846
segments with positive-prefix zeros: 5158
adjacent compatibility equations checked: 6486
literal consecutive ridges with terminal run <= 2 checked: 100
```

The independent native test is included in the ordinary Rust suite, or can
be run alone:

```powershell
cargo test --release --manifest-path search-framework\Cargo.toml `
  --test mixed_ridges
```

These are bounded algebra regressions, not a proof that a reachable infinite
ridge chain exists or terminates.

To measure the terminal-run geometry of one literal orbit:

```powershell
cargo run --release --manifest-path search-framework\Cargo.toml `
  --bin ridge_trace -- --m 1320111 --terminal-bound 2
```

The published record orbit reports 40,963,537 completed ridges and maximum
initial, internal, and terminal consecutive up-run lengths all equal to two.
This finite stabilizing orbit does not model the sublinear counterexample
branch, where Theorem 58 forces initial runs to grow.

## Artifact hashing

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath <artifact>
```

Compare lowercase hexadecimal output with
`../audit/evidence-manifest.md`.
