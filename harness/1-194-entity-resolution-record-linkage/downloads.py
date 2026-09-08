#!/usr/bin/env python3
"""Backfill pypistats download counts; the sweep's inline pass gets 429'd."""
import json, time, urllib.request, urllib.error
from pathlib import Path
R = Path(__file__).parent / "results" / "registry.json"
d = json.loads(R.read_text())
by = {x["package"]: x for x in d["downloads"]}
for pkg, rec in by.items():
    data = rec.get("data") or {}
    if isinstance(data, dict) and "last_month" in data:
        continue
    for attempt in range(6):
        url = f"https://pypistats.org/api/packages/{pkg}/recent"
        req = urllib.request.Request(url, headers={"User-Agent": "survey-of-software/1.194"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                rec["data"] = json.loads(r.read().decode()).get("data", {})
            print(pkg, rec["data"])
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(20 * (attempt + 1)); continue
            rec["data"] = {"_http_error": e.code}; print(pkg, e.code); break
        except Exception as e:  # noqa: BLE001
            rec["data"] = {"_error": str(e)}; print(pkg, e); break
    time.sleep(6)
R.write_text(json.dumps(d, indent=2))
print("updated")
