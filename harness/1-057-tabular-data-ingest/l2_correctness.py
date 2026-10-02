"""L2 — the correctness matrix for survey 1.057.

Every reader over hostile.csv, twice: once with DEFAULTS, once CONFIGURED to treat every
column as text. What each produced at each known hazard position is scored against
gen_fixtures.HAZARDS, which is the answer key.

Both arms run on purpose. The difference between them IS the finding — measuring only the
configured arm would delete it.

Rows are located by their `row_id` value rather than by position, so a reader that loses a
row boundary (the embedded-newline hazard) is scored as wrong about that row rather than
silently shifting every later answer.

Output: results/l2-correctness.json
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen_fixtures import HAZARDS, HAZARD_ROWS  # noqa: E402

FIXTURE = pathlib.Path("fixtures/hostile.csv")

# hazard -> which column carries it
COLUMN_OF = {
    "zero_padded_id": "zero_padded_id",
    "mixed_numeric": "amount",
    "empty_cell": "amount",
    "literal_na": "amount",
    "thousands_sep": "amount",
    "quoted_delimiter": "name",
    "embedded_newline": "note_text",
    "excel_formula": "note_text",
    "date_iso": "when",
    "date_us": "when",
    "date_written": "when",
    "leading_plus": "contact",
}

MISSING = "<row not found>"


def _render(v) -> str:
    """One rendering rule for every reader, so the comparison is of values and not of repr
    conventions. A null of any flavor renders as the empty string, which is the charitable
    reading: it is what a reader that conflated empty with missing would have to claim."""
    if v is None:
        return ""
    try:
        import math

        if isinstance(v, float) and math.isnan(v):
            return ""
    except Exception:
        pass
    if isinstance(v, str):
        return v
    return str(v)


# --- readers: each returns {row_id: {column: rendered value}} -----------------


def read_stdlib_csv():
    import csv as _csv

    with FIXTURE.open(newline="", encoding="utf-8") as fh:
        return _from_records(_csv.DictReader(fh))


def _from_records(records):
    """Returns (by_row_id, record_count).

    The mapping is keyed by `row_id` so a hazard can be located without depending on
    position. That COLLAPSES duplicates, so len(mapping) cannot detect a reader that split
    one row into two fragments sharing a row_id, or emitted one twice — which is exactly
    the failure the embedded-newline hazard probes for. The raw record count is returned
    alongside it, and both are published."""
    recs = list(records)
    return ({_render(r.get("row_id")): {k: _render(v) for k, v in r.items()} for r in recs},
            len(recs))


def read_pandas_default():
    import pandas as pd

    df = pd.read_csv(FIXTURE)
    return _from_records(df.to_dict("records"))


def read_pandas_str():
    import pandas as pd

    df = pd.read_csv(FIXTURE, dtype=str, keep_default_na=False, na_filter=False)
    return _from_records(df.to_dict("records"))


def read_polars_default():
    import polars as pl

    df = pl.read_csv(FIXTURE)
    return _from_records(df.to_dicts())


def read_polars_str():
    import polars as pl

    df = pl.read_csv(FIXTURE, infer_schema=False)  # every column Utf8
    return _from_records(df.to_dicts())


def read_duckdb_default():
    import duckdb

    con = duckdb.connect()
    rel = con.execute(f"SELECT * FROM read_csv_auto('{FIXTURE}')")
    cols = [d[0] for d in rel.description]
    return _from_records([dict(zip(cols, row)) for row in rel.fetchall()])


def read_duckdb_varchar():
    import duckdb

    con = duckdb.connect()
    rel = con.execute(
        f"SELECT * FROM read_csv('{FIXTURE}', all_varchar=true, header=true, ignore_errors=true)"
    )
    cols = [d[0] for d in rel.description]
    return _from_records([dict(zip(cols, row)) for row in rel.fetchall()])


def read_duckdb_lenient():
    """The third arm DuckDB needs and the others do not. Its own error message names these
    flags, so this is the reader taking its own advice rather than the harness inventing a
    configuration for it."""
    import duckdb

    con = duckdb.connect()
    rel = con.execute(
        f"SELECT * FROM read_csv('{FIXTURE}', all_varchar=true, header=true, "
        "null_padding=true, ignore_errors=true, strict_mode=false)"
    )
    cols = [d[0] for d in rel.description]
    return _from_records([dict(zip(cols, row)) for row in rel.fetchall()])


def read_petl():
    import petl

    t = petl.fromcsv(str(FIXTURE))
    return _from_records(petl.dicts(t))


READERS = {
    "stdlib csv": read_stdlib_csv,
    "pandas (defaults)": read_pandas_default,
    "pandas (dtype=str)": read_pandas_str,
    "polars (defaults)": read_polars_default,
    "polars (infer_schema=False)": read_polars_str,
    "duckdb (read_csv_auto)": read_duckdb_default,
    "duckdb (all_varchar)": read_duckdb_varchar,
    "duckdb (lenient)": read_duckdb_lenient,
    "petl": read_petl,
}


def main() -> int:
    if not FIXTURE.exists():
        print("run gen_fixtures.py first", file=sys.stderr)
        return 2

    results = {"fixture": str(FIXTURE), "hazards": {}, "readers": {}, "errors": {}}
    for key, spec in HAZARDS.items():
        results["hazards"][key] = {
            "row_id": str(HAZARD_ROWS[key]),
            "column": COLUMN_OF[key],
            "in_file": spec["raw"],
            "want": spec["want"],
            "note": spec["note"],
        }

    for name, fn in READERS.items():
        try:
            data, n_records = fn()
        except Exception as e:  # a reader that cannot open the file is a result
            results["errors"][name] = f"{type(e).__name__}: {e}"
            print(f"{name:32} FAILED TO READ: {type(e).__name__}: {e}")
            continue

        per = {}
        for key in HAZARDS:
            rid = str(HAZARD_ROWS[key])
            col = COLUMN_OF[key]
            row = data.get(rid)
            got = MISSING if row is None else row.get(col, "<column missing>")
            per[key] = {"got": got, "correct": got == HAZARDS[key]["want"]}
        score = sum(1 for v in per.values() if v["correct"])
        results["readers"][name] = {"records_returned": n_records,
                                    "distinct_row_ids": len(data),
                                    "score": score, "of": len(HAZARDS), "cells": per}
        dup = "" if n_records == len(data) else f"  ** {n_records - len(data)} duplicate row_id(s)"
        print(f"{name:32} {score:2}/{len(HAZARDS)} hazards correct, "
              f"{n_records:,} records / {len(data):,} distinct row_ids{dup}")

    out = pathlib.Path("results"); out.mkdir(exist_ok=True)
    (out / "l2-correctness.json").write_text(json.dumps(results, indent=2))
    print("\nwrote results/l2-correctness.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
