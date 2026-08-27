# 1.104.2 Code Formatting — measured

A **`measured-local`** rung (see `docs/map/17-the-evidence-ladder.md`). Ruff, Biome and
dprint are compiled binaries, so none of this can run in a reader's browser. What it can do
instead is publish the method completely enough that someone else gets the same numbers.

**Replicate:** `./run.sh` (container) or `./run-host.sh` (same pins, no daemon needed).

## Four cells, because two would have misled

| comparison | host 1× | container 1× | host 12× | container 12× | 1.104.2 says |
|---|---|---|---|---|---|
| ruff vs **black** | 16.5× | 20.5× | 21.0× | **32.3×** | 30-100× / 30× / 100× |
| ruff vs **yapf** | 150.3× | 321.2× | **1171.7×** | 1120.2× | 100× |
| ruff vs autopep8 | 94.7× | 157.6× | 515.0× | 495.2× | — |
| biome vs **prettier** | 14.5× | 11.7× | 27.8× | **31.4×** | 25× |
| dprint vs **prettier** | 7.2× | 6.8× | 11.5× | **14.3×** | 10-35× |

1× is 1 MB / 59 Python files; 12× replicates the same corpus to 12 MB / 900 files.

**The second axis was not planned and it changed the answer.** An earlier version of this
harness ran on the host only, where ruff-vs-black measured 19.4× and 21.0× — apparently
*stable* across a twelvefold size change, and comfortably short of the claimed 30×. That
looked like a clean refutation. Adding the container cells shows the ratio climbing to
32.3×, which reaches the bottom of the survey's stated range.

So the verdict recorded against those claims was **corrected from `wrong` to
`unverifiable`**. The ratio is a function of workload *and* environment, the survey states
neither, and a claim that cannot be pinned down is not a claim that has been disproved.

## What each claim comes to

**`30-100×` and `30×` (ruff vs black) — unverifiable.** Spans 16.5× to 32.3× across the four
cells. Touches the bottom of the range at one corner and nowhere else.

**`100× faster than Black` — wrong.** Outside every cell. The highest measurement anywhere
is 32.3×, and unlike the range claims this one cannot be rescued by a larger workload within
what was tested — it is off by more than threefold at its most favourable point.

**`100×` (ruff vs yapf) — wrong, by understating.** Measured 150.3× to 1171.7×. The claim is
below the minimum in every cell.

**`25×` (biome vs prettier) and `10-35×` (dprint vs prettier) — unverifiable.** Both are
size-dependent: 11.7×→31.4× and 6.8×→14.3×. Each is wrong at 1 MB and roughly right at
12 MB, and neither claim says which.

This is the house rule from `ADDING-RESEARCH.md` earning its keep on its first outing: *a
ratio with no workload is not publishable.* Four of the five comparisons here turn on a
workload the survey never states.

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
| CPU | aarch64, 8 cores |
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
the resolver refuses. 1.104.2 says of it *"Nothing new; move existing users to Ruff with
quote settings."* The dependency pin says the same thing more plainly, and dates it.

## Raw numbers

One file per environment and scale in `out/`, each carrying per-tool min, median and max,
the corpus file counts and byte sizes, the machine, the repetition count, and every version
string as the tool reported it.

`results-container-x1-firstrun.json` is kept deliberately: it is the 5-repetition run whose
disagreement with a later identical run is the evidence for raising the default to 9.
