#!/usr/bin/env bash
set -euo pipefail

# Independently check the compiled Conjecture environment with nanoda.
# Revisions are pinned because this repository is an auditable research artifact.
# lean4export: https://github.com/leanprover/lean4export
# nanoda:     https://github.com/ammkrn/nanoda_lib

readonly LEAN4EXPORT_REV="af5aa64bb914c3c2c781f378088dbd38acf4f804"
readonly NANODA_REV="ddfac2bf5a7b56cb46e141494427ff3dd55963c7"
readonly MODULE_NAME="Conjecture"
readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly TEMP_BASE="${TMPDIR:-/tmp}"
WORK_DIR="$(mktemp -d "${TEMP_BASE%/}/cloitre-lean-check.XXXXXX")"
readonly WORK_DIR

for required_tool in git lake cargo; do
  if ! command -v "${required_tool}" >/dev/null 2>&1; then
    echo "required tool not found on PATH: ${required_tool}" >&2
    exit 127
  fi
done

cleanup() {
  if [[ -n "${WORK_DIR}" && -d "${WORK_DIR}" &&
        "${WORK_DIR}" == "${TEMP_BASE%/}"/cloitre-lean-check.* ]]; then
    rm -rf -- "${WORK_DIR}"
  fi
}
trap cleanup EXIT

clone_at_revision() {
  local repository="$1"
  local revision="$2"
  local destination="$3"
  git clone --quiet --filter=blob:none --no-checkout "${repository}" "${destination}"
  git -C "${destination}" checkout --quiet --detach "${revision}"
}

readonly EXPORTER_DIR="${WORK_DIR}/lean4export"
readonly NANODA_DIR="${WORK_DIR}/nanoda_lib"
readonly EXPORT_FILE="${WORK_DIR}/environment.txt"
readonly CONFIG_FILE="${WORK_DIR}/nanoda.json"
NANODA_EXPORT_FILE="${EXPORT_FILE}"
if command -v cygpath >/dev/null 2>&1; then
  NANODA_EXPORT_FILE="$(cygpath -m "${EXPORT_FILE}")"
fi
readonly NANODA_EXPORT_FILE

clone_at_revision \
  "https://github.com/leanprover/lean4export.git" \
  "${LEAN4EXPORT_REV}" \
  "${EXPORTER_DIR}"
cp "${PROJECT_ROOT}/lean-toolchain" "${EXPORTER_DIR}/lean-toolchain"
(
  cd "${EXPORTER_DIR}"
  lake build
)

clone_at_revision \
  "https://github.com/ammkrn/nanoda_lib.git" \
  "${NANODA_REV}" \
  "${NANODA_DIR}"
(
  cd "${NANODA_DIR}"
  case "$(uname -s)" in
    MINGW*|MSYS*)
      RUSTFLAGS="-C link-arg=/STACK:67108864" cargo build --release --locked
      ;;
    *)
      cargo build --release --locked
      ;;
  esac
)

cd "${PROJECT_ROOT}"
lake env "${EXPORTER_DIR}/.lake/build/bin/lean4export" \
  "${MODULE_NAME}" > "${EXPORT_FILE}"

cat > "${CONFIG_FILE}" <<EOF
{
  "export_file_path": "${NANODA_EXPORT_FILE}",
  "use_stdin": false,
  "permitted_axioms": [
    "propext",
    "Classical.choice",
    "Quot.sound",
    "Lean.trustCompiler"
  ],
  "unpermitted_axiom_hard_error": false,
  "nat_extension": true,
  "string_extension": true,
  "print_axioms": false,
  "print_success_message": true
}
EOF

"${NANODA_DIR}/target/release/nanoda_bin" "${CONFIG_FILE}"
