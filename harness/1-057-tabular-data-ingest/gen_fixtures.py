"""Generate the fixtures for survey 1.057 (Tabular Data Ingest).

Data, not downloaded. The point of generating rather than shipping a file is that every
hazard sits at a KNOWN position, so "did the reader get this right" is checkable instead of
eyeballed. HAZARDS below is the answer key the correctness matrix scores against.

  clean.csv     N rows, well-formed. The baseline nobody argues about.
  hostile.csv   N rows carrying, at recorded positions, the things that break real imports.
  hostile.xlsx  the same content as a workbook, plus the spreadsheet-only hazards.

Usage:  python gen_fixtures.py [--rows 10000] [--out fixtures/]
"""

from __future__ import annotations

import argparse
import csv
import pathlib
import random

# The answer key. Each entry: what the cell literally contains in the file, and what a
# reader that respects an existing string-typed schema must hand back. `note` says which
# real failure this reproduces.
HAZARDS = {
    "zero_padded_id": {
        "raw": "00071",
        "want": "00071",
        "note": "zero-padded identifier; integer inference drops the padding and the value is silently wrong",
    },
    "mixed_numeric": {
        "raw": "n/a",
        "want": "n/a",
        "note": "one non-numeric value in an otherwise numeric column; forces object dtype or coercion to null",
    },
    "empty_cell": {
        "raw": "",
        "want": "",
        "note": "empty cell — 'not supplied'",
    },
    "literal_na": {
        "raw": "NA",
        "want": "NA",
        "note": "the literal string NA — 'recorded as unknown', a different fact from an empty cell",
    },
    "thousands_sep": {
        "raw": "1,234.00",
        "want": "1,234.00",
        "note": "thousands separator inside a quoted field; parses as text unless told otherwise",
    },
    "quoted_delimiter": {
        "raw": 'Smith, John',
        "want": "Smith, John",
        "note": "the delimiter inside a quoted field — the case hand-rolled split(',') gets wrong",
    },
    "embedded_newline": {
        "raw": "line one\nline two",
        "want": "line one\nline two",
        "note": "a newline inside a quoted field; a line-oriented reader loses the row boundary",
    },
    "date_iso": {"raw": "2026-03-04", "want": "2026-03-04", "note": "ISO date"},
    "date_us": {"raw": "03/04/2026", "want": "03/04/2026", "note": "ambiguous US/EU date — 4 March or 3 April"},
    "date_written": {"raw": "4 Mar 2026", "want": "4 Mar 2026", "note": "written date, third format in one file"},
    "leading_plus": {
        "raw": "+44 20 7946 0958",
        "want": "+44 20 7946 0958",
        "note": "phone number with a leading plus; some readers strip it or read it as a formula",
    },
    "excel_formula": {
        "raw": "=1+1",
        "want": "=1+1",
        "note": "a cell that looks like a formula in text; the CSV injection shape",
    },
}

COLUMNS = ["row_id", "zero_padded_id", "name", "amount", "note_text", "when", "contact", "flag"]

# The hazard row: 1-indexed data row (not counting the header) where each hazard is planted.
HAZARD_ROWS = {
    "zero_padded_id": 3,
    "mixed_numeric": 7,
    "empty_cell": 11,
    "literal_na": 12,
    "thousands_sep": 15,
    "quoted_delimiter": 19,
    "embedded_newline": 23,
    "date_iso": 27,
    "date_us": 28,
    "date_written": 29,
    "leading_plus": 33,
    "excel_formula": 37,
}


def _clean_row(i: int) -> dict:
    return {
        "row_id": str(i),
        "zero_padded_id": f"{i:05d}",
        "name": f"Person {i}",
        "amount": f"{(i * 37) % 10000}.{i % 100:02d}",
        "note_text": f"note {i}",
        "when": "2026-01-15",
        "contact": f"+44 20 7946 {i % 10000:04d}",
        "flag": "true" if i % 2 else "false",
    }


def _hostile_row(i: int) -> dict:
    r = _clean_row(i)
    for key, at in HAZARD_ROWS.items():
        if at != i:
            continue
        raw = HAZARDS[key]["raw"]
        if key == "zero_padded_id":
            r["zero_padded_id"] = raw
        elif key == "mixed_numeric":
            r["amount"] = raw
        elif key in ("empty_cell", "literal_na"):
            r["amount"] = raw
        elif key == "thousands_sep":
            r["amount"] = raw
        elif key == "quoted_delimiter":
            r["name"] = raw
        elif key == "embedded_newline":
            r["note_text"] = raw
        elif key in ("date_iso", "date_us", "date_written"):
            r["when"] = raw
        elif key == "leading_plus":
            r["contact"] = raw
        elif key == "excel_formula":
            r["note_text"] = raw
    return r


def write_csv(path: pathlib.Path, rows: int, hostile: bool) -> None:
    make = _hostile_row if hostile else _clean_row
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for i in range(1, rows + 1):
            w.writerow(make(i))
    if hostile:
        # A short final row: too few fields. Appended raw, because a DictWriter cannot
        # produce one — which is itself why this case survives into production files.
        with path.open("a", encoding="utf-8") as fh:
            fh.write("99999,00099,Truncated Row\n")


def write_xlsx(path: pathlib.Path, rows: int) -> None:
    import xlsxwriter

    wb = xlsxwriter.Workbook(str(path), {"constant_memory": False})
    text_fmt = wb.add_format({"num_format": "@"})
    date_fmt = wb.add_format({"num_format": "yyyy-mm-dd"})

    # `notes` is created FIRST, on purpose: it makes sheet index 0 the WRONG sheet, so a
    # reader that takes sheet 0 by index instead of by name gets prose. Created second
    # (as it was until 2026-09-09) the hazard is inert, because index 0 is then the data
    # sheet and taking it by index happens to be correct.
    notes = wb.add_worksheet("notes")
    notes.write_string(0, 0, "This sheet is not the data. A reader that takes sheet 0 by")
    notes.write_string(1, 0, "index rather than by name gets this, not the table.")

    ws = wb.add_worksheet("data")
    # A merged header spanning two columns, above the real header row. Sheets built by
    # people have these, and they shift every subsequent row by one.
    ws.merge_range(0, 0, 0, len(COLUMNS) - 1, "Quarterly export — do not edit")
    for c, name in enumerate(COLUMNS):
        ws.write_string(1, c, name)
    for i in range(1, rows + 1):
        r = _hostile_row(i)
        row = i + 1
        for c, name in enumerate(COLUMNS):
            v = r[name]
            if name == "zero_padded_id":
                # Formatted as text and holding digits: the cell Excel shows as 00071 and
                # a naive reader returns as 71.
                ws.write_string(row, c, v, text_fmt)
            elif name == "when" and v == "2026-01-15":
                ws.write_datetime(row, c, __import__("datetime").datetime(2026, 1, 15), date_fmt)
            else:
                ws.write_string(row, c, v)

    wb.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=10_000)
    ap.add_argument("--out", default="fixtures")
    ap.add_argument("--seed", type=int, default=1057)
    a = ap.parse_args()
    random.seed(a.seed)

    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    write_csv(out / "clean.csv", a.rows, hostile=False)
    write_csv(out / "hostile.csv", a.rows, hostile=True)
    write_xlsx(out / "hostile.xlsx", min(a.rows, 5_000))

    for extra in (100_000, 1_000_000):
        p = out / f"clean_{extra}.csv"
        if not p.exists():
            write_csv(p, extra, hostile=False)

    for p in sorted(out.iterdir()):
        print(f"  {p.name:24} {p.stat().st_size:>12,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
