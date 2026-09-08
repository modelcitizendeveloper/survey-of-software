# Harness — 1.194 Entity Resolution & Record Linkage

Every measured claim in survey 1.194 comes from here. Scripts print to stdout, raw JSON
is committed, versions are pinned, so a re-run can be diffed against what the survey says.

**Conditions for every number.** aarch64 Linux (WSL2, kernel 6.6.87.2), CPython 3.12.3
and 3.13.15, `uv` 0.12.5, measured 2026-09-07. Architecture matters here: two candidates
publish no aarch64 wheel and compile from source on this machine while installing from a
wheel on x86_64. Where that changes the answer the survey reports the wheel tags for both
rather than generalising from one run.

## Layout

| | |
|---|---|
| `registry.py`, `registry2.py` | L0. PyPI, pypistats and GitHub facts for 66 packages and 48 repositories, each row carrying its source URL |
| `downloads.py` | Backfills install counts the sweep got 429'd on |
| `mirrors.py` | Splits mirror from non-mirror downloads. One headline number needs this to be believable |
| `install_matrix.py` | L1. One clean venv per candidate per interpreter: resolve, build, import, freeze |
| `footprint.py` | Bytes on disk and distribution count per candidate, measured after the venvs settled |
| `export_data.py` | Freezes the FEBRL benchmark to CSV with SHA-256 digests, so no probe depends on a candidate for its data |
| `scoring.py` | The single scorer, imported by every probe. Pure stdlib — it has to load in eleven unrelated environments |
| `probes/probe_*.py` | L2/L3. One per candidate, run by that candidate's own venv |
| `summarize.py` | Builds the comparison tables from the committed JSON. No number is retyped |

## Reproducing

```bash
uv venv --python 3.12 .venvs/recordlinkage-3.12 && \
  uv pip install --python .venvs/recordlinkage-3.12/bin/python recordlinkage==0.16
.venvs/recordlinkage-3.12/bin/python export_data.py      # writes data/, prints digests
python3 install_matrix.py 3.12 3.13                      # ~40 min unattended
for ds in febrl1 febrl3; do for bl in exact prefix; do
  ./.venvs/splink-3.12/bin/python probes/probe_splink.py $ds $bl
done; done
python3 summarize.py
```

`data/*.csv` is gitignored because `export_data.py` regenerates it deterministically;
`data/meta.json` carries the digests to check a regeneration against.

## Three things that bit, recorded so they do not bite the next reader

**dedupe needs `BTrees<6.5`.** BTrees 6.5 (2026-08-20) removed the long-deprecated
`byValue()`; dedupe 3.0.3 calls it in `canopy_index.py:76` and pins only `BTrees>=4.1.4`.
A fresh install therefore installs, imports, and raises `AttributeError` at blocking time.
The venv used for the dedupe probe is `.venvs/dedupe-3.12-btrees64`.

**dedupe needs an address-space cap on this data.** An uncapped run on FEBRL3 reached
7.9 GiB resident and was killed to protect the machine, which also hosts a Dolt server.
The probe now sets `RLIMIT_AS` to 6 GiB, which turns the failure into a reportable
`MemoryError` located at `dedupe/training.py:177`. FEBRL1 completes in 524 MiB.

**Blocking rules decide the comparison, so they are a variable, not a constant.** The
first run gave the libraries whole-field blocking keys and the SQL baseline looser prefix
keys, and the libraries lost recall to the harness rather than to their own design. Both
variants are now run and both are committed (`*_exact.json`, `*_prefix.json`), because
the difference between them turned out to be larger than the difference between the
candidates.

## Reproducibility, measured

The whole harness was re-run on 2026-09-07, hours after the survey was written, and
diffed against the committed `results/summary.txt`.

**Every accuracy figure reproduced identically except one**, and every headline claim
survives unchanged — including the central finding, which came back to three decimal
places:

| exact entity recovery, FEBRL3 | whole-field blocking | prefix blocking |
|---|---|---|
| recordlinkage ECM | 0.894 | 0.970 |
| Splink @0.5 | 0.959 | 0.977 |
| SQL baseline @0.80 | 0.740 | **0.731** — the only candidate made worse |

**The one that moved: Splink on FEBRL3 at threshold 0.99**, recall 0.945 → 0.944 and F1
0.972 → 0.971. Precision, entity count (2,055), exact recovery (0.973) and ARI (0.987)
were unchanged.

**Why, and it is worth knowing before you re-run:** `estimate_u_using_random_sampling`
is stochastic and the probe does not seed it, so the u-probabilities differ slightly
between runs and the model's match probabilities shift in the fourth decimal. At the
tightest threshold that moves one pair across the line. Splink's own advertised property
— that the threshold barely matters between 0.5 and 0.99 — is what keeps this from
mattering anywhere else.

Treat F1 figures in this survey as reproducible to about ±0.001, not to the digit.
Wall-clock timings vary more (±10%) and no claim rests on them.
