#!/usr/bin/env python3
"""Generate static/workshop/index.json from the cards in static/workshop/index.html.

The homepage stays the single hand-written source; this derives the machine-readable
manifest other sites consume (workshop.modelcitizendeveloper.com renders its SoS section
from it, so adding a floor model here shows up there with no second edit).

Run after editing the homepage:  python3 scripts/workshop_manifest.py
"""
import json, re, html, pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent / "static" / "workshop"
src = (root / "index.html").read_text(encoding="utf-8")

cards = []
for m in re.finditer(r'<a class="card" href="(?P<href>[^"]+)">\s*<h2>(?P<title>.*?)</h2>\s*'
                     r'<p class="finding">(?P<finding>.*?)</p>\s*<p class="meta">(?P<meta>.*?)</p>', src, re.S):
    strip = lambda t: html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t))).strip()
    meta = strip(m["meta"])
    survey, _, libraries = meta.partition("·")
    sm = re.search(r"Survey ([\d.]+) — (.+)", survey.strip())
    cards.append({
        "name": strip(m["title"]),
        "url": "https://research.modelcitizendeveloper.com" + m["href"],
        "finding": strip(m["finding"]),
        "survey_code": sm.group(1) if sm else None,
        "survey_title": sm.group(2).strip() if sm else survey.strip(),
        "survey_url": f"https://research.modelcitizendeveloper.com/survey/{sm.group(1).replace('.', '-')}/" if sm else None,
        "libraries": libraries.strip(),
    })

if not cards:
    sys.exit("no cards parsed — did the homepage markup change?")
out = {
    "title": "The Workshop — Survey of Software floor models",
    "url": "https://research.modelcitizendeveloper.com/workshop/",
    "description": ("Free working pages that measure a Survey of Software finding on your own data, "
                    "in your own browser. The real Python libraries run in the tab; nothing is uploaded."),
    "models": cards,
}
(root / "index.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {len(cards)} models to static/workshop/index.json")
