#!/usr/bin/env bash
# The host path: identical tool versions to the Dockerfile, resolved by uv and npm.
# Keep the pins here and in the Dockerfile in step — they are the same measurement.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out node_tools

# blue is omitted on purpose: it pins black==22.1.0 and cannot coexist with a
# current Black. See the Dockerfile.
PY_PINS="ruff==0.16.5 black==26.5.1 autopep8==2.3.2 yapf==0.43.0"
JS_PINS="prettier@3.4.2 @biomejs/biome@1.9.4 dprint@0.47.6"

# Check for an actual binary, not just the directory: a half-finished npm install
# leaves node_modules behind and the old guard then skipped the retry.
[ -x node_tools/node_modules/.bin/prettier ] || \
  (cd node_tools && npm install --silent --no-fund --no-audit $JS_PINS)
export PATH="$PWD/node_tools/node_modules/.bin:$PATH"
export OUT_DIR="$PWD/out"
export BENCH_ENV="host"

exec /home/ivanadamin/.local/bin/uv run --quiet \
    $(for p in $PY_PINS; do printf -- "--with %s " "$p"; done) \
    python bench.py "$@"
