# 1.253 Code Formatting — measured

A **`measured-local`** rung (see `docs/map/17-the-evidence-ladder.md`). Ruff, Biome and
dprint are compiled binaries, so none of this can run in a reader's browser. What it can do
instead is publish the method completely enough that someone else gets the same numbers.

**Replicate:** `./run.sh` (container) or `./run-host.sh` (same pins, no daemon needed).

**Published at** <https://github.com/modelcitizendeveloper/survey-of-software/tree/main/harness/1-253-code-formatting> — survey 1.253 cites this page 71 times, so it has to be
somewhere a reader can reach. A measurement nobody can get to is not evidence.

## Read this before comparing these numbers to anyone else's

**The first four cells were measured on aarch64, under WSL2, on a laptop.** Running the same
harness on a standard x86 instance did not merely add a column — it showed that the headline
ratio **depends on which architecture you are on**, by roughly a factor of two.

These are Rust binaries measured against CPython, compiled differently for the two targets, so
there was never any reason to expect one number to stand for both. Reporting a single figure
was the error; neither measurement was. See `docs/map/17-the-evidence-ladder.md`.

The x86 cells were produced by `run-droplet.sh` — create, run, collect, destroy — on a
**DigitalOcean `s5-8vcpu-16gb-30gb` in `atl1`, 8 vCPU, AMD EPYC 9555P**. Eight vCPU to match
the 8-core ARM box, so architecture is the only variable that moved. It costs about twenty
cents an hour and the run takes under half of one.

## Six cells, because four would have misled

| comparison | aarch64 container x1 | aarch64 container x12 | aarch64 host x1 | aarch64 host x12 | x86_64 container x1 | x86_64 container x12 |
|---|---|---|---|---|---|---|
| ruff vs **black** | 20.5× | 32.3× | 16.5× | 21.0× | 20.0× | 16.1× |
| ruff vs **autopep8** | 157.6× | 495.2× | 94.7× | 515.0× | 219.5× | 616.6× |
| ruff vs **yapf** | 321.2× | 1120.2× | 150.3× | 1171.7× | 352.1× | 1052.7× |
| biome vs **prettier** | 11.7× | 31.4× | 14.5× | 27.8× | 9.8× | 21.9× |
| dprint vs **prettier** | 6.8× | 14.3× | 7.2× | 11.5× | 5.1× | 10.1× |

  aarch64 container x1         1.2 MB  8 cores  unreported (ARM /proc/cpuinfo has no `
  aarch64 container x12       14.4 MB  8 cores  unreported (ARM /proc/cpuinfo has no `
  aarch64 host x1              1.2 MB  8 cores  aarch64
  aarch64 host x12            14.4 MB  8 cores  aarch64
  x86_64 container x1          1.2 MB  8 cores  AMD EPYC 9555P 64-Core Processor, digitalocean s5-8vcpu-16gb-30gb
  x86_64 container x12        14.4 MB  8 cores  AMD EPYC 9555P 64-Core Processor, digitalocean s5-8vcpu-16gb-30gb

1× is 1 MB / 59 Python files; 12× replicates the same corpus to 12 MB / 900 files.

### What the x86 run changed — and what the 2026-08-29 correction took back

**This section's original claim was that Ruff's lead over Black is roughly twice as large on
ARM as on x86. That is now withdrawn as a finding**, though not shown to be false. The ARM
cells were measured on a laptop doing other work, and this harness times each tool in its own
window, so a machine that got busier between two tools' windows biases the ratio between
them. The x86 cells are the reference — re-run two days later on a fresh machine they
reproduced within 2.7%. **A clean ARM run is the outstanding work**, and until it exists the
architecture question is open rather than answered.

The original argument, kept so the correction has something to correct: Ruff's lead over
Black is roughly twice as large on ARM as on x86, once the corpus is big
enough to show it. Same container, same pinned tools, same corpus, eight cores on both:

| ruff vs black, container | 1 MB | 12 MB | direction |
|---|---|---|---|
| aarch64 | 20.5× | **32.3×** | grows |
| x86_64 | 20.0× | **16.1×** | shrinks |

They start in the same place and go opposite ways.

#### This is not the laptop being noisy

It is the obvious objection, and the ARM box invites it — it is a WSL2 laptop and its Black
runs at 12 MB spanned 2.223 s to 3.599 s, a 62% spread across nine repetitions of identical
work. The x86 droplet's spanned 2%.

> **CORRECTION, 2026-08-29.** The paragraph that stood here claimed the noise cancels
> "because both tools are timed on the same machine in the same run", and offered the
> min/med/max table below as proof. **That defense was too strong, and the test cannot see
> the failure it was offered against.**
>
> The harness times tools SEQUENTIALLY — all nine Ruff passes, then all nine Black passes.
> Same machine and same run, but **not the same time window.** If the machine got busier
> between one tool's window and the next, the ratio absorbs that difference directly. The
> cancellation argument holds only if contention is stationary across the whole run, which
> on a laptop somebody is using is exactly what it is not.
>
> And the min/med/max check measures variance WITHIN a window. If the machine was uniformly
> busier during Black's nine passes, all three of Black's estimators shift together, the
> ratio shifts with them, and the table below reports reassuring agreement. It is blind to
> between-window drift.
>
> **The test that does work: a ratio is only as good as the spread on BOTH sides of it.**
> Low spread on both ends means both windows were quiet, which is what licenses comparing
> them. That rule is applied throughout `RESULTS-LINT.md`, and the fix — interleaving the
> tools so they share time windows — is described there.
>
> The x86 droplet cells are unaffected: measured at 1-5% spread on a machine whose load
> average sat at exactly 1.00 for the whole run. **Treat the ARM laptop cells as
> provisional and the droplet as the reference.**

The original argument, kept so the correction has something to correct: both tools are timed
on the same machine in the same run, so a machine that is 20% slow is 20% slow for Ruff and
for Black alike. The test offered was whether the ratio moves when computed from the fastest
runs, the median runs, or the slowest runs:

| ruff vs black, 12 MB | min/min | med/med | max/max |
|---|---|---|---|
| aarch64 container | 29.3× | 32.3× | 25.6× |
| x86_64 container | 16.6× | 16.1× | 15.6× |

**The two ranges do not overlap on any estimator.** 25.6-32.3× against 15.6-16.6×. The gap
is a property of the platform, not of the machine's mood.

At 1 MB the two architectures are indistinguishable (aarch64 17.1-26.1×, x86_64 18.7-21.4×,
overlapping). The divergence needs a corpus large enough for it to show.

#### What is still open

Our ARM cells come from a laptop under WSL2, so what is measured is *this ARM machine*, not
ARM in general — the ratio is sound but a clean ARM server would pin it down. DigitalOcean
offers no ARM instances at all, so that cell could not be filled here. **A Graviton or Ampere
run is the outstanding work**, and until it exists the phrasing is "on the ARM machine we
tested", not "on ARM".

Two other findings hold on both architectures: ruff-vs-yapf climbs with corpus size
(150-1172× on aarch64, 352-1053× on x86_64) and biome-vs-prettier roughly doubles
(11.7-31.4× and 9.8-21.9×).

## What each claim comes to

**`30-100×` and `30×` (ruff vs black) — unverifiable, and now for a stated reason.** The
measured range is 16.1× to 32.3×, and *which end you get depends on your architecture*. On
the ARM machine at 12 MB it reaches 32.3×, clearing the claimed 30×. On x86 it never exceeds
20.0×. A claim that names neither a workload nor a platform cannot be settled by a
measurement that fixes both.

**`100× faster than Black` — wrong.** Outside every cell on both architectures. The highest
measurement anywhere is 32.3×.

**`100×` (ruff vs yapf) — wrong, by understating.** 150× to 1172× on aarch64 and 352× to
1053× on x86_64. The claim is below the minimum in every cell on both architectures.

**`15×` (biome vs ESLint) — not ours to settle, and now settled elsewhere as UNSETTLED.**
This is a linting claim and this harness compares formatters, so it was parked rather than
tested. **1.250 took it up** and could not settle it either: its first measurement was
invalid — ESLint exited with a fatal error and never linted anything — and the corrected
run fell below that harness's nine-repetition threshold. The claim is unsupported by
anything measured in either survey and is not shown to be false. See
1.250's `performance-benchmarks.md`.

**`25×` (biome vs prettier) and `10-35×` (dprint vs prettier) — unverifiable.** Size-dependent
on both architectures: biome 11.7×→31.4× on aarch64 and 9.8×→21.9× on x86_64. Each is wrong
on a small codebase and roughly right on a large one, and neither claim says which. This is
the defect the house rule targets — *a ratio with no workload is not publishable*.

**Astral's own `10-100×`** (vendor: astral-sh/ruff README) covers linters and formatters
together. For formatting against Black, the measured 16-32× sits inside that range at the
bottom on both architectures. The linter half is untested here.

### The general lesson

A benchmark that runs on one architecture does not know it is measuring one architecture. This
one reported a ratio *growing* with codebase size for three days, and the growth was real on
the machine that produced it and absent on the machine most readers have. Neither number was
wrong. The single-platform *summary* was.

## Method

Everything below changes the answer, so all of it is stated rather than assumed.

- **Corpus**: pinned, public, immutable — `requests 2.32.5`, `jinja2 3.1.6`, `click 8.1.8`
  for Python; `express 4.21.2` and `axios 1.7.9` (`lib/` only) for JavaScript. PyPI and npm
  never republish a version under the same name, so it is fetchable again exactly.
- **Fresh corpus per tool.** Formatting rewrites files; without this the second tool would
  be formatting the first tool's output.
- **Caches off.** Ruff, Biome and dprint all cache aggressively. A warm cache is a real
  number for a developer and the wrong one for a comparison, because it measures the cache.
- **First pass discarded.** Each tool formats the tree once before timing, so the timed runs
  are the steady state a developer lives in rather than a one-off rewrite.
- **Median of 9.** An earlier run used 3, and two identical container runs disagreed by 20%
  (14.9× against 18.5× for ruff-vs-black). Three repetitions cannot separate a formatter
  from its own noise.
- **One benchmark at a time.** Running the host and container cases concurrently would have
  had them contend for the same 8 cores; that attempt was aborted rather than reported.
- **Not measured**: ESLint. The survey's "Biome 15× faster than ESLint" is a *linting*
  claim, and this harness compares formatters only.

## Machine

| | |
|---|---|
| Architecture | **aarch64** for cells 1-4, **x86_64** for cells 5-6 — see above |
| CPU | 8 cores |
| Memory | 11.7 GB |
| Container | `python:3.12.11-slim-bookworm`, Node 22, Docker 29.0.0 |
| Host | Ubuntu 24.04 under WSL2, Python 3.12.3 |

Both paths pin the same tool versions. The container additionally pins the OS and both
runtimes, and is the form to replicate from.

## Versions

```
ruff 0.16.5      black 26.5.1      autopep8 2.3.2      yapf 0.43.0
prettier 3.4.2   @biomejs/biome 1.9.4                  dprint 0.47.6
```

## Blue is absent, and that is a finding

`blue 0.9.1` pins `black==22.1.0` and cannot be installed beside a current Black at all —
the resolver refuses. 1.253 says of it *"Nothing new; move existing users to Ruff with
quote settings."* The dependency pin says the same thing more plainly, and dates it.

## Raw numbers

One file per environment and scale in `out/`, each carrying per-tool min, median and max,
the corpus file counts and byte sizes, the machine, the repetition count, and every version
string as the tool reported it.

`results-container-x1-firstrun.json` is kept deliberately: it is the 5-repetition run whose
disagreement with a later identical run is the evidence for raising the default to 9.
