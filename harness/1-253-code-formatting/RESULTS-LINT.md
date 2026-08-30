# 1.250 Linters & Static Analysis — measured

A **`measured-local`** rung (`docs/map/17-the-evidence-ladder.md`).

**Replicate:** `./run-droplet.sh` (x86, clean) or `docker run --rm -e REPS=9 -e SCALE=12 -v "$PWD/out:/out" --entrypoint python3 sos-lint-bench:1.250 bench_lint.py`

Extends the 1.253 formatter harness rather than replacing it — same container, same pinned
corpus, caches off, first pass discarded, median of nine. That is deliberate: it lets the
linting ratios be read against 1.253's formatting ratios.

## The reference is the droplet, not the laptop

**Every number below is from a DigitalOcean `s5-8vcpu-16gb-30gb` in `atl1`, 8 vCPU AMD EPYC
9555P, whose load average sat at exactly 1.00 for the entire run.** The ARM laptop cells are
published beside them as a comparison and should not be quoted alone.

That is a change of position, and the reason is in `RESULTS.md`'s correction: this harness
times tools **sequentially**, so two tools occupy different time windows and a machine that
gets busier between them biases the ratio. The min/med/max estimator check cannot detect
that — it measures variance *inside* a window. The rule that does work:

> **A ratio is only as good as the spread on both sides of it.**

The difference is not subtle. Same benchmark, same corpus, same pinned tools:

| | x86 droplet | ARM laptop |
|---|---|---|
| ruff check | **4%** | 36% |
| flake8 | **2%** | 14% |
| ESLint | **4%** | 26% |
| Biome lint | **3%** | 17% |
| Pylint | 1% | 2% |
| oxlint | 26% | 77% |

**The harness has since been changed to interleave** — every tool takes one pass, then every
tool takes another — so tools share time windows and the cancellation argument is true rather
than approximately true. The cells below predate that change and are labeled sequential.

## Results — x86 droplet, container, median of 9

| | 1 MB / 59 py files | 12 MB / 900 py files | 12× costs | spread @ x12 |
|---|---|---|---|---|
| `ruff check` (E,W,F,C90) | 0.0143 s | 0.0673 s | 4.7× | 4% |
| Flake8 (default) | 0.4009 s | 2.5499 s | 6.4× | 2% |
| **Pylint** (timed alone) | 14.81 s | **348.38 s** | **23.5×** | **1%** |
| ESLint (intersection set) | 0.2637 s | 0.8749 s | 3.3× | 4% |
| Biome lint | 0.0663 s | 0.2534 s | 3.8× | 3% |
| oxlint | 0.0457 s | 0.0552 s | *1.2×* | *26%* |

### ruff check vs Flake8 — 28.0× → 37.9×

Matched rule sets: Ruff runs `--select E,W,F,C90`, which is pycodestyle + Pyflakes + McCabe,
exactly Flake8's default. Spreads of 4% and 2% on the two sides, so the ratio is licensed.

The ARM laptop measured 17.4× and 30.4× for the same comparison — **lower at both sizes**,
and its ruff cell carried 36% spread. The two are not directly comparable and the ARM pair
should not be read as an architecture finding until a clean ARM cell exists.

### Pylint is superlinear, and it is not the machine

**23.5× on x86 for a 12× corpus, against 24.2× on ARM.** Two architectures, two machines,
one shape — and both at 1-2% spread, which is what licenses comparing them.

That agreement is the point. A curve that reproduces across architectures is a property of
**whole-program inference**, not of anyone's laptop. It is the measured form of the
architectural claim in S2: settling one inferred type forces re-checking everything
downstream, and that cost grows faster than the file count.

The practical reading: **Pylint's cost grows faster than your codebase does.** A tool that is
fine on a service becomes a CI problem you grow into. Narrow the path selection rather than
absorbing the wall time.

For contrast, `ruff check` measured **4.7× on both machines** — identical. Sublinear, because
fixed startup amortises and per-file work parallelises.

## "Biome is 15× faster than ESLint" — settled, and it is not supported

1.253 carried this claim and could not test it: its harness compares formatters and this is
a linting claim. This survey took it up.

**Measured: 4.0× at 1 MB and 3.5× at 12 MB**, matched rule sets, spreads of 3% and 4%.
Not 15×.

Two honest qualifications:

**oxlint gets close to 15×, and Biome is the tool the claim names.** oxlint measured 5.8× at
1 MB and 15.8× at 12 MB. If a real measurement lies behind the circulating figure, it may
belong to a different tool — but oxlint's own cell carries 26% spread even on a quiet
machine, because at 55 ms it is under the floor described below. Suggestive; not evidence.

**Our rule set is not theirs.** The comparison here is an intersection config all three tools
implement, with no type-aware rules. A benchmark running ESLint with `typescript-eslint`
against Biome without it would produce a much larger number and would not be measuring the
same job.

## The measurement floor

Run-to-run spread tracks runtime, and it does so **even on a quiet machine**:

| | runtime @ x12 | spread, quiet x86 |
|---|---|---|
| Pylint | 348 s | 1% |
| Flake8 | 2.5 s | 2% |
| ESLint | 0.87 s | 4% |
| Biome | 0.25 s | 3% |
| ruff check | 0.067 s | 4% |
| **oxlint** | **0.055 s** | **26%** |

A dedicated box lowers the floor by roughly an order of magnitude — ruff went from 36% to 4%
— but it does not remove it. **oxlint at 55 ms is still unmeasurable here**, and its 1.2×
"curve" is noise rather than a finding.

1.253 never met this because its slowest tools took seconds. Linters are an order of
magnitude faster, which puts the fastest of them under the floor on any machine.

## Outstanding

1. **A clean ARM cell.** The laptop numbers are provisional; whether the linting ratio is
   architecture-dependent the way 1.253's formatting ratio was cannot be answered from a
   contended machine.
2. **A re-run under interleaved timing**, to check whether the sequential cells shifted.
3. **oxlint needs a larger corpus** to rise above the floor at all.

## Method

Pinned immutable corpus (`requests 2.32.5`, `jinja2 3.1.6`, `click 8.1.8`; `express 4.21.2`,
`axios 1.7.9`), fresh copy per tool, caches off, first pass discarded, median of nine, one
benchmark at a time.

Linter-specific:

- **Exit codes per tool.** A linter returns non-zero to mean "I found something". Pylint
  returns a bitmask, so a healthy run can exit 20. ESLint's exit 2 is fatal and is rejected —
  accepting it is how an earlier version of this harness timed an error message nine times.
- **Matched rule sets, or no ratio.** Two linters running different rules are not doing
  comparable work. Pylint is timed alone because nothing else does whole-program inference.

## Versions

```
ruff 0.16.5    flake8 7.3.0 (pyflakes 3.4.0, pycodestyle 2.14.0, mccabe 0.7.0)
pylint 4.0.8   eslint 10.9.1    oxlint 1.80.0    @biomejs/biome 2.5.11
```

## Machines

| | |
|---|---|
| **Reference** | DigitalOcean `s5-8vcpu-16gb-30gb`, `atl1`, 8 vCPU AMD EPYC 9555P, load 1.00 throughout |
| Comparison | aarch64, 8 cores, WSL2 on Ubuntu 24.04, **other work running** |

Both ran `python:3.12.11-slim-bookworm` + Node 22 under Docker.
