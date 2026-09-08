#!/usr/bin/env python3
"""Second L0 pass: packages named by the community index that the first sweep missed."""
import json, sys, time, urllib.request, urllib.error
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from registry import pypi_facts, gh_facts, downloads  # noqa: E402

PYPI = ["blockingpy", "py-stringmatching", "er-evaluation", "deezymatch",
        "stringcompare", "nominally", "nameparser", "matchflow", "delex",
        "fingerprints", "rigour", "pyspark", "polars", "recordlinkage-py",
        "splink3", "tilores", "zingg-enterprise", "great-expectations",
        "ftfy", "pyjanitor", "metaphone", "abydos", "pylev", "editdistance"]
REPOS = [("ncn-foreigners", "BlockingPy"), ("anhaidgroup", "py_stringmatching"),
         ("OlivierBinette", "ER-Evaluation"), ("Living-with-machines", "DeezyMatch"),
         ("OlivierBinette", "StringCompare"), ("OlivierBinette", "Awesome-Entity-Resolution"),
         ("vaneseltine", "nominally"), ("derek73", "python-nameparser"),
         ("opensanctions", "rigour"), ("alephdata", "fingerprints"),
         ("chrisjsewell", "matchflow"), ("resolve-io", "delex"),
         ("moj-analytical-services", "splink_demos"),
         ("cleanlab", "cleanlab"), ("Senzing", "senzing"),
         ("senzing-garage", "sz-sdk-python-core")]

res = {"fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "pypi": [], "downloads": [], "github": []}
for p in PYPI:
    res["pypi"].append(pypi_facts(p)); print("pypi", p, file=sys.stderr)
for p in PYPI:
    res["downloads"].append(downloads(p)); time.sleep(5)
for o, r in REPOS:
    res["github"].append(gh_facts(o, r)); print("gh", o, r, file=sys.stderr)
Path("results/registry2.json").write_text(json.dumps(res, indent=2))
print("wrote results/registry2.json")
