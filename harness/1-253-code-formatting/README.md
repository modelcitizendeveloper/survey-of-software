# Harness — 1.253 Code Formatting Libraries

Measures the formatter speed claims in survey 1.253 against a pinned corpus, and
publishes the method so the numbers can be checked by someone else.

This is a **`measured-local`** rung on the evidence ladder
(`docs/map/17-the-evidence-ladder.md`). It exists because Ruff, Biome and dprint are
compiled binaries: a floor model cannot run them in a reader's browser, and that makes a
reproducible local benchmark the ceiling rather than a failure.

## Run it

```bash
./run.sh            # container — the published method; needs a Docker daemon
./run-host.sh       # same pins via uv + npm, no daemon required
REPS=5 SCALE=12 ./run.sh    # more repetitions, or a corpus replicated 12x
```

Results land in `out/` and the write-up is `RESULTS.md`.

## Why the size sweep

`SCALE` replicates the corpus. A ratio measured at one size cannot settle a claim that
names no size — and running at 1× and 12× is what separated the survey's three kinds of
error: one ratio stable and overstated, one understated and growing, two
size-dependent with no size stated.

## Files

| | |
|---|---|
| `Dockerfile` | the published recipe — OS, runtimes and every formatter pinned |
| `run.sh` / `run-host.sh` | container path, and the same pins without a daemon |
| `bench.py` | the measurement, with its four methodology decisions stated in the docstring |
| `corpus.json` | the pinned corpus: exact package versions from PyPI and npm |
| `RESULTS.md` | method, machine, versions, and what the numbers say about the claims |
| `out/` | raw JSON, including min/median/max per tool |

## What it does not measure

ESLint. The survey's "Biome 15× faster than ESLint" is a linting claim; this compares
formatters. Anyone extending the harness should add it as a separate comparison rather than
folding a linter into a formatter table.
