"""L5 — error reporting under load, for survey 1.057.

Settles S1's questions 3 and 4:
  * is DuckDB's rejected-row capture usable, or does it only say "something failed"
  * does pandera's lazy validation survive a file that is substantially wrong

Three stacks over the same file at three damage levels (1%, 10%, 50% bad rows). What each
can SAY about a specific bad row is scored on three questions, because "it reported an
error" and "it named the row, the column and the reason" are different products:

    row?     can it identify WHICH input row failed
    column?  can it identify WHICH field was at fault
    why?     is there a reason a person could act on

Cost is wall time and peak RSS in a fresh subprocess per (stack, damage) pair.

Output: results/l5-errors.json
"""

from __future__ import annotations

import csv
import json
import pathlib
import subprocess
import sys

PY = str(pathlib.Path(".venv/bin/python").absolute())
ROWS = 20_000
DAMAGE = (0.01, 0.10, 0.50)


def make_damaged(path: pathlib.Path, rows: int, frac: float) -> list[int]:
    """Every k-th row gets a bad `amount`. Returns the 1-indexed bad row numbers."""
    bad = []
    step = max(1, int(1 / frac))
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["row_id", "name", "amount", "when"])
        for i in range(1, rows + 1):
            if i % step == 0:
                w.writerow([i, f"Person {i}", "NOT_A_NUMBER", "2026-01-15"])
                bad.append(i)
            else:
                w.writerow([i, f"Person {i}", f"{(i*37)%10000}.{i%100:02d}", "2026-01-15"])
    return bad


BODIES = {
    "pandera (lazy)": """
import pandas as pd, pandera.pandas as pa
schema = pa.DataFrameSchema({
    "row_id": pa.Column(int),
    "name":   pa.Column(str),
    "amount": pa.Column(float, coerce=True),
    "when":   pa.Column(str),
})
df = pd.read_csv(PATH, dtype=str, keep_default_na=False, na_filter=False)
df["row_id"] = df["row_id"].astype(int)
try:
    schema.validate(df, lazy=True)
    failures = []
except pa.errors.SchemaErrors as e:
    fc = e.failure_cases
    failures = [{"row": int(r) if r == r else None, "column": str(c), "why": str(ch), "value": str(v)}
                for r, c, ch, v in zip(fc.get("index", []), fc.get("column", []),
                                       fc.get("check", []), fc.get("failure_case", []))]
n_failed = len(failures)
sample = failures[:3]
""",
    "duckdb (store_rejects)": """
import duckdb
con = duckdb.connect()
con.execute("CREATE TABLE t AS SELECT * FROM read_csv('" + PATH + "', "
            "columns={'row_id':'INTEGER','name':'VARCHAR','amount':'DOUBLE','when':'VARCHAR'}, "
            "header=true, store_rejects=true)")
rej = con.execute("SELECT line, column_name, error_type, error_message, csv_line "
                  "FROM reject_errors LIMIT 3").fetchall()
n_failed = con.execute("SELECT count(*) FROM reject_errors").fetchone()[0]
sample = [{"row": r[0], "column": r[1], "why": f"{r[2]}: {r[3]}", "value": (r[4] or "")[:40]}
          for r in rej]
""",
    "stdlib csv + pydantic": """
import csv
from pydantic import BaseModel, ValidationError
class Row(BaseModel):
    row_id: int
    name: str
    amount: float
    when: str
failures = []
with open(PATH, newline='', encoding='utf-8') as fh:
    for lineno, rec in enumerate(csv.DictReader(fh), start=2):
        try:
            Row(**rec)
        except ValidationError as e:
            for err in e.errors():
                failures.append({"row": lineno, "column": ".".join(str(x) for x in err["loc"]),
                                 "why": err["msg"], "value": str(err.get("input"))[:40]})
n_failed = len(failures)
sample = failures[:3]
""",
}

RUNNER = """
import json, resource, time
PATH = {path!r}
_t0 = time.perf_counter()
{body}
dt = time.perf_counter() - _t0
peak_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(json.dumps({{"seconds": round(dt, 4), "n_failed": n_failed, "sample": sample,
                   "peak_rss_mb": round(peak_kb / 1024, 1)}}, default=str))
"""


def run(label: str, path: str) -> dict:
    body = "\n".join(BODIES[label].strip().splitlines())
    out = subprocess.run([PY, "-c", RUNNER.format(path=path, body=body)],
                         capture_output=True, text=True)
    if out.returncode != 0:
        # A child killed by a signal (OOM, returncode -9) writes NOTHING to stderr, and
        # [-1] on an empty list raises IndexError from inside the error handler — losing
        # the whole run instead of recording one failure.
        err = out.stderr.strip().splitlines()
        return {"error": (err[-1][:250] if err else
                          f"no stderr; returncode {out.returncode}")}
    return json.loads(out.stdout.strip())


def main() -> int:
    fx = pathlib.Path("fixtures"); fx.mkdir(exist_ok=True)
    results = {"rows": ROWS, "levels": {}}

    for frac in DAMAGE:
        pct = int(frac * 100)
        path = fx / f"damaged_{pct}.csv"
        bad = make_damaged(path, ROWS, frac)
        print(f"\n=== {pct}% bad ({len(bad):,} of {ROWS:,} rows) ===")
        per = {}
        for label in BODIES:
            r = run(label, str(path))
            per[label] = r
            if "error" in r:
                print(f"  {label:24} ERROR {r['error'][:90]}")
                continue
            s = (r["sample"] or [{}])[0]
            says_row = s.get("row") is not None
            says_col = bool(s.get("column"))
            says_why = bool(s.get("why"))
            r["identifies"] = {"row": says_row, "column": says_col, "why": says_why}
            print(f"  {label:24} {r['seconds']:7.3f} s  peak {r['peak_rss_mb']:7.1f} MB  "
                  f"{r['n_failed']:>6,} reported  row={says_row} col={says_col} why={says_why}")
            if s:
                print(f"      first: row={s.get('row')} col={s.get('column')!r} "
                      f"why={str(s.get('why'))[:72]!r}")
        per["_expected_bad_rows"] = len(bad)
        results["levels"][f"{pct}%"] = per

    out = pathlib.Path("results"); out.mkdir(exist_ok=True)
    (out / "l5-errors.json").write_text(json.dumps(results, indent=2, default=str))
    print("\nwrote results/l5-errors.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
