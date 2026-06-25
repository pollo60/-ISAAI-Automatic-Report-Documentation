#!/usr/bin/env bash
# Build English Project Charter PDF from LaTeX.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TEX="Project-Charter-ISAAI.tex"
if ! command -v latexmk &>/dev/null; then
  echo "latexmk not found. Install MacTeX/TeX Live, or run: pdflatex $TEX"
  if command -v pdflatex &>/dev/null; then
    pdflatex -interaction=nonstopmode "$TEX"
    pdflatex -interaction=nonstopmode "$TEX"
  else
    exit 1
  fi
else
  latexmk -pdf -interaction=nonstopmode "$TEX"
fi

echo "Output: Project-Charter-ISAAI.pdf"
