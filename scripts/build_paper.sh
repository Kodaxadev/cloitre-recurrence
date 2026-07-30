#!/usr/bin/env bash
# Compile the arXiv draft and fail on anything a referee would notice.
#
#   scripts/build_paper.sh [output-directory]
#
# Two pdflatex passes, so cross-references resolve. The build is run with a
# fixed SOURCE_DATE_EPOCH: pdfTeX has honoured that for /CreationDate and
# /ModDate since TeX Live 2016, which is a prerequisite for a byte-reproducible
# PDF. Whether it is sufficient is measured separately by
# scripts/check_pdf_reproducible.py rather than assumed here.

set -euo pipefail

outdir="${1:-build}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
paper="$here/manuscript/arxiv"

# 2026-01-01T00:00:00Z. Any fixed value works; it only has to be stable.
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1767225600}"
export FORCE_SOURCE_DATE=1

cd "$paper"
mkdir -p "$outdir"

for pass in 1 2; do
  echo "=== pdflatex pass $pass ==="
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory "$outdir" main.tex \
    > "$outdir/pass$pass.out" || {
      echo "pdflatex failed on pass $pass; last 40 lines:"
      tail -40 "$outdir/pass$pass.out"
      exit 1
    }
done

log="$outdir/main.log"

fail=0
if grep -q "LaTeX Warning: There were undefined references" "$log"; then
  echo "FAIL: undefined references"
  grep -n "LaTeX Warning: Reference" "$log" | head -20
  fail=1
fi
if grep -q "LaTeX Warning: Citation" "$log"; then
  echo "FAIL: undefined citations"
  grep -n "LaTeX Warning: Citation" "$log" | head -20
  fail=1
fi

boxes=$(grep -cE "^(Overfull|Underfull)" "$log" || true)
if [ "$boxes" -ne 0 ]; then
  echo "FAIL: $boxes over/underfull boxes"
  grep -nE "^(Overfull|Underfull)" "$log" | head -20
  fail=1
fi

pages=$(grep -oE "Output written on [^(]*\(([0-9]+) page" "$log" | grep -oE "[0-9]+ page" | grep -oE "[0-9]+" | head -1 || true)
echo "pages: ${pages:-unknown}"
echo "over/underfull boxes: $boxes"
echo "output: $paper/$outdir/main.pdf"

exit "$fail"
