#!/usr/bin/env bash
# Assemble the GitHub Pages site into _site/ (or the directory given as $1).
# The PDFs are the committed build outputs, so CI needs no TeX: make -C presentation pdf handout, make derivations.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
out="${1:-$root/_site}"
mkdir -p "$out/pdf" "$out/figures" "$out/data/results"
cp -R "$root/site/." "$out/"
cp "$root/presentation/ch5103-presentation.pdf" "$root/presentation/ch5103-handout.pdf" \
   "$root/derivations/derivations.pdf" "$root/assets/formulae.pdf" "$out/pdf/"
cp "$root"/assets/figures/*.png "$out/figures/"
cp "$root/assets/figures.jsonl" "$root/presentation/data/distonic.csv" "$out/data/"
cp "$root"/verification/results/*.txt "$out/data/results/"
touch "$out/.nojekyll"
echo "site assembled in $out ($(find "$out" -type f | wc -l) files, $(du -sh "$out" | cut -f1))"
