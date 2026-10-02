"""L3 — read throughput and peak memory for survey 1.057.

Each (reader, size) pair runs in a FRESH subprocess, so peak RSS is that reader's own
high-water mark and not whatever ran before it. Wall time is the minimum of N rounds
inside that process: the floor is the measurement, everything above it is scheduler noise.

THE JOB IS DEFINED AT THE BOUNDARY, not at the API. The readers do not share an output
shape, so each is asked for the same observable thing: every row materialized, and one
column summed as a string length, which forces a reader that would otherwise return a lazy
handle to actually do the work. Without that, a lazy reader reports the cost of building a
plan and looks 100x faster than it is.

Output: results/l3-throughput.json
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

PY = str(pathlib.Path(".venv/bin/python").absolute())
ROUNDS = 5

SIZES = {
    "10k": "fixtures/clean.csv",
    "100k": "fixtures/clean_100000.csv",
    "1M": "fixtures/clean_1000000.csv",
}

# Each body must set `n` (rows seen) and `checksum` (sum of len(name)), so the harness can
# assert every reader did the same work before comparing any timing.
BODIES = {
    "stdlib csv": """
import csv
with open(PATH, newline='', encoding='utf-8') as fh:
    rows = list(csv.DictReader(fh))
n = len(rows); checksum = sum(len(r['name']) for r in rows)
""",
    "pandas (defaults)": """
import pandas as pd
df = pd.read_csv(PATH)
n = len(df); checksum = int(df['name'].str.len().sum())
""",
    "pandas (dtype=str)": """
import pandas as pd
df = pd.read_csv(PATH, dtype=str, keep_default_na=False, na_filter=False)
n = len(df); checksum = int(df['name'].str.len().sum())
""",
    "polars (defaults)": """
import polars as pl
df = pl.read_csv(PATH)
n = df.height; checksum = int(df['name'].str.len_chars().sum())
""",
    "polars (infer_schema=False)": """
import polars as pl
df = pl.read_csv(PATH, infer_schema=False)
n = df.height; checksum = int(df['name'].str.len_chars().sum())
""",
    "polars (scan + collect)": """
import polars as pl
df = pl.scan_csv(PATH).collect()
n = df.height; checksum = int(df['name'].str.len_chars().sum())
""",
    "duckdb": """
import duckdb
con = duckdb.connect()
r = con.execute("SELECT count(*), sum(length(name)) FROM read_csv_auto('" + PATH + "')").fetchone()
n = r[0]; checksum = int(r[1])
""",
    "petl (streaming)": """
import petl
_tbl = petl.fromcsv(PATH)
n = 0; checksum = 0
for r in petl.dicts(_tbl):
    n += 1; checksum += len(r['name'])
""",
    "stdlib csv (streaming)": """
import csv
n = 0; checksum = 0
with open(PATH, newline='', encoding='utf-8') as fh:
    for r in csv.DictReader(fh):
        n += 1; checksum += len(r['name'])
""",
}

RUNNER = """
import json, resource, time, sys
PATH = {path!r}
best = None
for _ in range({rounds}):
    _t0 = time.perf_counter()
{body}
    dt = time.perf_counter() - _t0
    best = dt if best is None else min(best, dt)
peak_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(json.dumps({{"seconds": round(best, 4), "rows": n, "checksum": checksum,
                   "peak_rss_mb": round(peak_kb / 1024, 1)}}))
"""


def run(label: str, path: str, rounds: int) -> dict:
    body = "\n".join("    " + ln for ln in BODIES[label].strip().splitlines())
    code = RUNNER.format(path=path, rounds=rounds, body=body)
    out = subprocess.run([PY, "-c", code], capture_output=True, text=True)
    if out.returncode != 0:
        # A child killed by a signal (OOM, returncode -9) writes NOTHING to stderr, and
        # [-1] on an empty list raises IndexError from inside the error handler — losing
        # the whole run instead of recording one failure. Reachable here: the materialized
        # stdlib arm peaks at 1.4 GB on the 1M fixture.
        err = out.stderr.strip().splitlines()
        return {"error": (err[-1][:200] if err else
                          f"no stderr; returncode {out.returncode}")}
    return json.loads(out.stdout.strip())


def main() -> int:
    # `rounds` is recorded PER SIZE: the 1M sweep drops to 3, and a single
    # top-level 5 would misdescribe it in the machine-readable copy.
    results = {"sizes": {}, "rounds_per_size": {}, "fair": {}}
    for size, path in SIZES.items():
        if not pathlib.Path(path).exists():
            print(f"missing {path}, run gen_fixtures.py", file=sys.stderr)
            return 2
        rounds = ROUNDS if size != "1M" else 3
        print(f"\n=== {size} ({pathlib.Path(path).stat().st_size/1e6:.1f} MB) ===")
        per = {}
        checksums = {}
        for label in BODIES:
            r = run(label, path, rounds)
            per[label] = r
            if "error" in r:
                print(f"  {label:30} ERROR {r['error'][:70]}")
                continue
            checksums[label] = (r["rows"], r["checksum"])
            print(f"  {label:30} {r['seconds']:7.3f} s   peak {r['peak_rss_mb']:7.1f} MB   "
                  f"{r['rows']:,} rows")
        # The leveling assertion: identical work, or the comparison is void. Kept OUTSIDE
        # the per-reader map so a consumer iterating readers does not meet a pseudo-reader
        # with no `seconds`.
        distinct = set(checksums.values())
        results["fair"][size] = {"identical_work": len(distinct) == 1,
                                 "distinct_results": [list(x) for x in distinct]}
        print(f"  -- identical work across readers: {len(distinct) == 1}")
        results["sizes"][size] = per
        results["rounds_per_size"][size] = rounds

    out = pathlib.Path("results"); out.mkdir(exist_ok=True)
    (out / "l3-throughput.json").write_text(json.dumps(results, indent=2))
    print("\nwrote results/l3-throughput.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
