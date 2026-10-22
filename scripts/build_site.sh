#!/usr/bin/env bash
# Assemble the GitHub Pages site into _site/ (or the directory given as $1).
# Locally this uses the committed PDFs and test outputs; in CI (.github/workflows/pages.yml) the jobs before
# this one rebuild them from source and drop them in place first.
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
# build stamp, shown in the page footer
sha="${GITHUB_SHA:-$(git -C "$root" rev-parse HEAD 2>/dev/null || echo unknown)}"
run_url=""
[ -n "${GITHUB_RUN_ID:-}" ] && run_url="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"
printf '{"commit": "%s", "built": "%s", "run": "%s"}\n' "$sha" "$(date -u +%Y-%m-%dT%H:%MZ)" "$run_url" > "$out/data/build.json"
echo "site assembled in $out ($(find "$out" -type f | wc -l) files, $(du -sh "$out" | cut -f1))"
