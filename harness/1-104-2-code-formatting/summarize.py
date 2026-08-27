#!/usr/bin/env python3
"""Read every out/results-*.json and print the ratio table.

WHY THIS EXISTS. RESULTS.md's table was hand-transcribed from the raw JSON. That is the same
defect the harness was built to correct, one level up: a number retyped by a human is a number
that can drift from its source silently, and nothing would catch it. The table is now derived.

Usage:  python3 summarize.py            # markdown table for RESULTS.md
        python3 summarize.py --json     # the same ratios as data
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAIRS = [("ruff", "black"), ("ruff", "autopep8"), ("ruff", "yapf"),
         ("biome", "prettier"), ("dprint", "prettier")]


def load() -> list[dict]:
    runs = []
    for p in sorted((HERE / "out").glob("results-*.json")):
        if "firstrun" in p.name:      # a 3-rep pilot, kept for the record, not comparable
            continue
        d = json.loads(p.read_text())
        m, c = d["machine"], d["corpus"]
        d["_label"] = f"{m.get('arch', '?')} {d['ran_via']} x{c.get('scale', 1)}"
        d["_times"] = {r["tool"]: r.get("median_s") for r in d["results"]}
        d["_mb"] = round(sum(c["bytes"].values()) / 1024 / 1024, 1)
        runs.append(d)
    # ARM first, then x86; within each, host then container, then by scale
    return sorted(runs, key=lambda d: (d["machine"].get("arch", ""), d["ran_via"],
                                       d["corpus"].get("scale", 1)))


def ratio(d: dict, fast: str, slow: str) -> float | None:
    a, b = d["_times"].get(fast), d["_times"].get(slow)
    return round(b / a, 1) if a and b else None


def main() -> int:
    runs = load()
    if not runs:
        print("no results in out/", file=sys.stderr)
        return 1
    if "--json" in sys.argv:
        print(json.dumps({"runs": [{"label": d["_label"], "arch": d["machine"].get("arch"),
                                    "via": d["ran_via"], "scale": d["corpus"].get("scale", 1),
                                    "mb": d["_mb"], "cores": d["machine"].get("cores"),
                                    "instance": d["machine"].get("instance"),
                                    "ratios": {f"{f} vs {s}": ratio(d, f, s)
                                               for f, s in PAIRS}} for d in runs]}, indent=2))
        return 0
    head = ["comparison"] + [d["_label"] for d in runs]
    print("| " + " | ".join(head) + " |")
    print("|" + "---|" * len(head))
    for f, s in PAIRS:
        cells = [f"{r}×" if (r := ratio(d, f, s)) else "—" for d in runs]
        print(f"| {f} vs **{s}** | " + " | ".join(cells) + " |")
    print()
    for d in runs:
        inst = d["machine"].get("instance")
        where = f", {inst['provider']} {inst['size']}" if inst else ""
        print(f"  {d['_label']:26} {d['_mb']:>5} MB  {d['machine'].get('cores')} cores"
              f"  {d['machine'].get('cpu', '?')[:38]}{where}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
