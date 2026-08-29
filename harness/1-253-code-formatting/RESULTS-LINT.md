# 1.250 Linters & Static Analysis — measured

A **`measured-local`** rung (`docs/map/17-the-evidence-ladder.md`), and a partial one. Read
the limits section before quoting any number here.

**Replicate:** `docker build -t sos-lint-bench:1.250 . && docker run --rm -e REPS=9 -e SCALE=12 -v "$PWD/out:/out" --entrypoint python3 sos-lint-bench:1.250 bench_lint.py`

This extends the 1.253 formatter harness rather than replacing it — same container, same
pinned corpus, same fresh-copy-per-tool, caches off, first pass discarded, median of nine.
That is deliberate: it lets the linting ratios be read against 1.253's formatting ratios.

## Read this before comparing these numbers to anyone else's

**Astral benchmarks on the CPython codebase.** Ruff's README captions its chart "Linting
the CPython codebase from scratch" (read 2026-08-29). This harness uses `requests 2.32.5`,
`jinja2 3.1.6` and `click 8.1.8`, pinned. Different corpus, different machine, different
question — **nothing here refutes their chart** and none of it is written as though it does.
What it can say is what the ratio looks like on a mid-sized real dependency tree.

**One architecture only.** Every cell below is aarch64, on a laptop under WSL2, with other
work running on the machine. 1.253's central finding was that the ruff-vs-black ratio is
roughly twice as large on ARM as on x86 — so a single-architecture figure is exactly the
error that survey identified. The x86 cell is outstanding.

## Results — aarch64 container, median of 9

| | 1 MB / 59 py files | 12 MB / 900 py files | spread at x12 |
|---|---|---|---|
| `ruff check` (E,W,F,C90) | 0.0185 s | 0.0864 s | 36% |
| Flake8 (default) | 0.3220 s | 2.6238 s | 14% |
| **Pylint** (timed alone) | **14.46 s** | **349.95 s** | **2.1%** |

Spread is (max−min)/min across the nine repetitions.

### ruff check vs Flake8: 17.4× → 30.4×, and it grows

Matched rule sets — Ruff runs `--select E,W,F,C90`, which is pycodestyle + Pyflakes +
McCabe, exactly Flake8's default. Both tools are doing the same work.

| | 1 MB | 12 MB |
|---|---|---|
| ruff vs flake8 | 17.4× | **30.4×** |

**The ratio survives the noise even though the absolute numbers do not.** Ruff's individual
timings carry 36% spread, but both tools are timed on the same machine in the same run, so a
machine that is briefly slow is slow for both. The test is whether the ratio moves when
computed from the fastest, median and slowest runs:

| ruff vs flake8, 12 MB | min/min | med/med | max/max |
|---|---|---|---|
| aarch64 container | 30.8× | 30.4× | 25.9× |

Consistent. The growth from 17.4× to 30.4× mirrors what 1.253 measured for `ruff format`
against Black on the same architecture (20.5× → 32.3×), which supports that survey's
conclusion that the ratio is a function of the workload rather than a constant.

**Against Astral's `10-100×`:** 17-30× sits inside it, at the bottom. Same finding as 1.253
reached for the formatting half.

### Pylint scales worse than linearly — the clearest result here

**14.46 s → 349.95 s is 24.2× for a 12× corpus.** At 2.1% spread this is the most reliable
measurement in the set: a 350-second run averages out every source of noise that ruins the
fast tools.

This is not a criticism of Pylint and it is not a ratio against anything. Pylint builds an
inference model across the whole program, and that is a graph problem whose cost grows
faster than the file count. It is the measured consequence of the architecture S2
describes, and it is why Ruff reimplemented Pylint's cheap per-file checks and not its
expensive whole-program ones.

The practical reading: **Pylint's cost is superlinear in codebase size**, so a tool that is
tolerable on a small service becomes a CI problem on a monolith. Narrow the path selection
rather than accepting the wall time.

## What is NOT settled, and why

**"Biome is 15× faster than ESLint" — still unsettled.** This survey set out to check it
and cannot yet.

The first attempt was invalid and the failure is worth recording. ESLint exited 2 with
"all of the files matching the glob pattern are ignored" — ESLint 10 resolves a flat
config's `files` patterns relative to the config's location, so pointing it at a directory
from elsewhere matches nothing. Exit 2 had been listed as acceptable, so the harness timed
an *error message* nine times and recorded it as a result. The tell was in the data:
**ESLint appeared to get faster on a 12× larger corpus**, which is not a performance
characteristic.

Corrected, ESLint's x1 time went 0.109 s → 0.354 s. A 3-repetition check of the fixed
invocation suggests **oxlint ≈ 4.0× and Biome ≈ 3.6×** against ESLint at 1 MB — a long way
from 15×, and **not publishable**: 1.253 established that three repetitions cannot separate
a tool from its own noise, which is why this harness defaults to nine.

**The JavaScript cells need a re-run on a quiet machine.** They are not in the table above.

## The measurement floor — a limit 1.253 never hit

Run-to-run spread tracks runtime almost exactly:

| Tool | x12 runtime | spread |
|---|---|---|
| Pylint | 350 s | 2.1% |
| Flake8 | 2.6 s | 14% |
| ESLint | 0.10 s | 27% |
| ruff check | 0.086 s | 36% |
| oxlint | 0.099 s | 77% |

Below roughly 100 ms, wall-clock on a shared machine is measuring the scheduler. 1.253 did
not meet this problem because its slowest tools took seconds; linters are an order of
magnitude faster than formatters, which puts three of these under the floor.

**The consequence for method:** ratios between tools timed in the same run remain usable,
because the noise is common to both. Absolute times below ~100 ms on this hardware are not,
and are reported here with their spread rather than alone. The fix is a dedicated machine —
1.253 measured its x86 droplet cells at 2% spread against this laptop's 62%.

## Outstanding

1. **The x86 cell.** One architecture is not a baseline; 1.253 proved the ratio moves.
2. **The JavaScript trio, re-run at nine repetitions** on a quiet machine, to settle the
   Biome/ESLint claim this survey was written to check.
3. **A clean ARM cell.** What is measured here is *this laptop*, not ARM.

## Method

Inherited from 1.253 in full: pinned immutable corpus, fresh copy per tool, caches off,
first pass discarded, median of nine, one benchmark at a time.

Added for linters:

- **Exit codes per tool.** A linter returns non-zero to mean "I found something". Pylint
  returns a bitmask — fatal 1, error 2, warning 4, refactor 8, convention 16 — so a healthy
  run can exit 20. ESLint's exit 2 is a fatal error and is now rejected.
- **Matched rule sets.** Formatters are comparable by default because they all do the same
  job. Two linters running different rule sets are not, and a ratio between them measures
  the configuration. `ruff check --select E,W,F,C90` matches Flake8's default; Pylint is
  timed alone because nothing else does whole-program inference.

## Versions

```
ruff 0.16.5    flake8 7.3.0 (pyflakes 3.4.0, pycodestyle 2.14.0, mccabe 0.7.0)
pylint 4.0.8   eslint 10.9.1    oxlint 1.80.0    @biomejs/biome 2.5.11
```

## Machine

aarch64, 8 cores, 11.7 GB, `python:3.12.11-slim-bookworm` + Node 22 under Docker 29.0.0,
host Ubuntu 24.04 on WSL2. **Other work was running during these measurements**, which is
what the spread column exists to disclose.
