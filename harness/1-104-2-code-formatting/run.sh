#!/usr/bin/env bash
# Build and run the harness. Two paths, same pins.
#
#   container  the published method — everything pinned including the OS and the runtimes.
#              This is what someone else should run to replicate.
#   host       the same tool versions resolved by uv and npx, run directly. Produces the
#              same measurement on a machine where the Docker daemon is not available;
#              results.json records which path produced the numbers, because "in a
#              container" and "on this laptop" are different claims about a measurement.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out

if docker info >/dev/null 2>&1; then
    echo "→ container path"
    docker build -q -t sos-fmt-bench:1.104.2 . >/dev/null
    # `docker run` does NOT inherit the host environment. Without these, REPS and SCALE
    # were silently ignored and every container run used the defaults — a "12x" run that
    # was actually 1x, which would then have been compared against a real 12x host run.
    docker run --rm -e REPS -e SCALE -v "$PWD/out:/out" sos-fmt-bench:1.104.2 "$@"
else
    echo "→ host path (docker daemon unavailable); same pins, uv + npx" >&2
    ./run-host.sh "$@"
fi
echo
echo "raw numbers: $(pwd)/out/  (one file per environment and scale)"
