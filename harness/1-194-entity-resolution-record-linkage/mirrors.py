#!/usr/bin/env python3
"""pypistats /recent counts mirrors. /overall splits them; a package whose
downloads are mostly mirrors is not being installed by people."""
import json, time, urllib.request, urllib.error
from pathlib import Path
PKGS = ["recordlinkage", "splink", "dedupe", "zingg", "pyjedai", "string-grouper",
        "polyfuzz", "nomenklatura", "senzing-core", "csvmatch", "name-matching",
        "datasketch", "rapidfuzz", "dedupe-variable-datetime", "fuzzymatcher",
        "py-entitymatching", "pandas-dedupe", "spark-matcher"]
out = {}
for p in PKGS:
    url = f"https://pypistats.org/api/packages/{p}/overall"
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "survey-of-software/1.194"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode())["data"]
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(20 * (attempt + 1)); continue
            data = [{"_http_error": e.code}]; break
    # last 30 dated points per category
    agg = {}
    for row in data:
        if "category" not in row:
            continue
        agg.setdefault(row["category"], []).append((row["date"], row["downloads"]))
    rec = {}
    dates = set()
    for cat, pts in agg.items():
        pts.sort()
        last30 = pts[-30:]
        rec[cat] = sum(v for _, v in last30)
        dates.update(d for d, _ in last30)
    # window computed PER CATEGORY, not across the pooled list: the endpoint
    # returns one row per (date, category), so pooling halves the window.
    rec["window"] = f"{min(dates)} .. {max(dates)} ({len(dates)} days)" if dates else None
    out[p] = rec
    print(p, rec, flush=True)
    time.sleep(6)
Path("results/mirrors.json").write_text(json.dumps(out, indent=2))
