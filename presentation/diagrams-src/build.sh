#!/usr/bin/env bash
# Build the JS/SVG diagrams: node generators -> SVG -> PDF (vector) for \includegraphics.
set -euo pipefail
cd "$(dirname "$0")"
export FONTCONFIG_FILE="$PWD/fonts.conf"
for gen in *.mjs; do node "$gen"; done
mkdir -p ../figures/diagrams
for svg in ../figures/diagrams-svg/*.svg; do
  rsvg-convert -f pdf -o "../figures/diagrams/$(basename "${svg%.svg}").pdf" "$svg"
done
echo "built: $(ls ../figures/diagrams | tr '\n' ' ')"
