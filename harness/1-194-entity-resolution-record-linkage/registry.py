#!/usr/bin/env python3
"""
L0: registry facts for the entity-resolution / record-linkage candidate set.

Nothing here is a judgment. It is version, release date, license, wheel kind,
download volume, and the four cells of the stall test (open PRs vs merged PRs vs
commits). Every number lands in results/registry.json with the URL it came from.

Run:  uv run --with requests python registry.py
"""
import json, os, sys, time
from datetime import datetime, timezone
from pathlib import Path
import urllib.request, urllib.error

OUT = Path(__file__).parent / "results"
OUT.mkdir(exist_ok=True)
GH_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

# name on PyPI -> GitHub owner/repo (None where there is no package or no repo)
PYPI = [
    "recordlinkage", "dedupe", "splink", "zingg", "pyjedai", "string-grouper",
    "polyfuzz", "fuzzymatcher", "csvmatch", "rltk", "deepmatcher",
    "py-entitymatching", "entity-embed", "datasketch", "pandas-dedupe",
    "csvdedupe", "dedupe-variable-datetime", "febrl", "splink-graph",
    "senzing", "senzing-core", "duckdb", "rapidfuzz", "jellyfish",
    "sparse-dot-topn", "networkx", "scikit-learn", "hierarchical-cluster",
    "recordlinkage-toolkit", "reclin", "anymatch", "ditto-er", "spark-matcher",
    "name-matching", "nomenklatura", "followthemoney", "cleanco", "probablepeople",
    "usaddress", "postal", "pypostal", "dedupe-hcluster", "textdistance",
]

REPOS = [
    ("J535D165", "recordlinkage"),
    ("dedupeio", "dedupe"),
    ("moj-analytical-services", "splink"),
    ("zinggAI", "zingg"),
    ("AI-team-UoA", "pyJedAI"),
    ("scify", "JedAIToolkit"),
    ("Bergvca", "string_grouper"),
    ("MaartenGr", "PolyFuzz"),
    ("RobinL", "fuzzymatcher"),
    ("maxharlow", "csvmatch"),
    ("usc-isi-i2", "rltk"),
    ("anhaidgroup", "deepmatcher"),
    ("anhaidgroup", "py_entitymatching"),
    ("vintasoftware", "entity-embed"),
    ("ekzhu", "datasketch"),
    ("Senzing", "senzing-sdk"),
    ("senzing-garage", "sz-sdk-python"),
    ("OpenRefine", "OpenRefine"),
    ("megagonlabs", "ditto"),
    ("ing-bank", "spark-matcher"),
    ("opensanctions", "nomenklatura"),
    ("dedupeio", "dedupe-examples"),
    ("dedupeio", "csvdedupe"),
    ("Valires", "fastLink"),
    ("djvanderlaan", "reclin2"),
    ("rapidfuzz", "RapidFuzz"),
    ("jamesturk", "jellyfish"),
    ("datamade", "probablepeople"),
    ("datamade", "usaddress"),
    ("openvenues", "libpostal"),
    ("duckdb", "duckdb"),
    ("Tamr", "tamr-client"),
]


def get(url, accept=None):
    req = urllib.request.Request(url, headers={"User-Agent": "survey-of-software/1.194"})
    if accept:
        req.add_header("Accept", accept)
    if GH_TOKEN and "api.github.com" in url:
        req.add_header("Authorization", f"Bearer {GH_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"_http_error": e.code, "_url": url}
    except Exception as e:  # noqa: BLE001
        return {"_error": str(e), "_url": url}


def pypi_facts(pkg):
    url = f"https://pypi.org/pypi/{pkg}/json"
    d = get(url)
    if "_http_error" in d or "_error" in d:
        return {"package": pkg, "source_url": url, **d}
    info = d["info"]
    version = info["version"]
    files = d["releases"].get(version, [])
    # Earliest and latest upload across all releases
    uploads = []
    for ver, fl in d["releases"].items():
        for f in fl:
            uploads.append((f["upload_time_iso_8601"], ver))
    uploads.sort()
    wheels = sorted({f["filename"].split("-")[-1].replace(".whl", "")
                     for f in files if f["packagetype"] == "bdist_wheel"})
    return {
        "package": pkg,
        "source_url": url,
        "version": version,
        "license": info.get("license") or (info.get("license_expression") or ""),
        "license_classifiers": [c for c in info.get("classifiers", []) if c.startswith("License")],
        "requires_python": info.get("requires_python"),
        "requires_dist": info.get("requires_dist"),
        "summary": info.get("summary"),
        "home_page": info.get("home_page"),
        "project_urls": info.get("project_urls"),
        "latest_upload": uploads[-1][0] if uploads else None,
        "first_upload": uploads[0][0] if uploads else None,
        "release_count": len(d["releases"]),
        "wheel_tags": wheels,
        "has_sdist_only": bool(files) and not wheels,
        "yanked": all(f.get("yanked") for f in files) if files else None,
    }


def downloads(pkg):
    url = f"https://pypistats.org/api/packages/{pkg}/recent"
    d = get(url)
    return {"package": pkg, "source_url": url, "data": d.get("data", d)}


def gh_facts(owner, repo):
    base = f"https://api.github.com/repos/{owner}/{repo}"
    d = get(base)
    if "_http_error" in d or "_error" in d:
        return {"repo": f"{owner}/{repo}", "source_url": base, **d}
    out = {
        "repo": f"{owner}/{repo}",
        "source_url": base,
        "stars": d.get("stargazers_count"),
        "forks": d.get("forks_count"),
        "open_issues_and_prs": d.get("open_issues_count"),
        "archived": d.get("archived"),
        "disabled": d.get("disabled"),
        "created_at": d.get("created_at"),
        "pushed_at": d.get("pushed_at"),
        "updated_at": d.get("updated_at"),
        "default_branch": d.get("default_branch"),
        "license": (d.get("license") or {}).get("spdx_id"),
        "description": d.get("description"),
        "homepage": d.get("homepage"),
        "full_name": d.get("full_name"),   # reveals a rename/transfer
    }
    # Stall test: four cells
    for label, q in (
        ("open_prs", f"repo:{owner}/{repo}+type:pr+state:open"),
        ("merged_prs_since_2026_03_01", f"repo:{owner}/{repo}+type:pr+is:merged+merged:%3E2026-03-01"),
        ("open_issues_only", f"repo:{owner}/{repo}+type:issue+state:open"),
    ):
        s = get(f"https://api.github.com/search/issues?q={q}&per_page=1")
        out[label] = s.get("total_count", s)
        time.sleep(2.2)  # unauthenticated search is 10/min
    # Commits in the last year (proxy for internal-first workflows)
    c = get(f"{base}/commits?since=2025-09-01T00:00:00Z&per_page=1")
    out["has_commit_since_2025_09"] = bool(c) and isinstance(c, list) and len(c) > 0
    # Latest release
    rel = get(f"{base}/releases/latest")
    out["latest_release"] = {"tag": rel.get("tag_name"), "published_at": rel.get("published_at")} \
        if "tag_name" in rel else None
    return out


def main():
    stamp = datetime.now(timezone.utc).isoformat()
    res = {"fetched_at": stamp, "authenticated_github": bool(GH_TOKEN),
           "pypi": [], "downloads": [], "github": []}
    for p in PYPI:
        res["pypi"].append(pypi_facts(p))
        print(f"pypi {p}", file=sys.stderr)
    for p in PYPI:
        res["downloads"].append(downloads(p))
    for o, r in REPOS:
        res["github"].append(gh_facts(o, r))
        print(f"gh {o}/{r}", file=sys.stderr)
    (OUT / "registry.json").write_text(json.dumps(res, indent=2))
    print(f"wrote {OUT/'registry.json'}")


if __name__ == "__main__":
    main()
