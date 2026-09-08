#!/usr/bin/env python3
"""
L1: can you actually install it?

One clean venv per candidate per interpreter, cold uv cache disabled only for
timing honesty (we keep the cache ON — a cold-cache number measures the network,
not the package). What this records is: does resolution succeed, does the build
succeed, does `import` succeed, how long, and whether a C toolchain was needed
(inferred from uv's own "Building" lines).

Failure is the result, not an error. Every outcome lands in results/install.json.
"""
import json, os, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
VENVS = HERE / ".venvs"

# candidate -> (pip requirement, import name to smoke-test)
CANDIDATES = {
    "splink":            ("splink", "splink"),
    "dedupe":            ("dedupe", "dedupe"),
    "recordlinkage":     ("recordlinkage", "recordlinkage"),
    "pyjedai":           ("pyjedai", "pyjedai"),
    "string_grouper":    ("string-grouper", "string_grouper"),
    "polyfuzz":          ("polyfuzz", "polyfuzz"),
    "csvmatch":          ("csvmatch", "csvmatch"),
    "zingg":             ("zingg", "zingg"),
    "nomenklatura":      ("nomenklatura", "nomenklatura"),
    "senzing":           ("senzing-core", "senzing_core"),
    "datasketch":        ("datasketch", "datasketch"),
    "name_matching":     ("name-matching", "name_matching"),
    "spark_matcher":     ("spark-matcher", "spark_matcher"),
    "py_entitymatching": ("py-entitymatching", "py_entitymatching"),
    "rltk":              ("rltk", "rltk"),
    "deepmatcher":       ("deepmatcher", "deepmatcher"),
    "entity_embed":      ("entity-embed", "entity_embed"),
    "fuzzymatcher":      ("fuzzymatcher", "fuzzymatcher"),
    "pandas_dedupe":     ("pandas-dedupe", "pandas_dedupe"),
    "duckdb":            ("duckdb", "duckdb"),
}

PYTHONS = sys.argv[1:] or ["3.12", "3.13"]
TIMEOUT = 900


def run(cmd, **kw):
    t0 = time.monotonic()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, **kw)
    return p, time.monotonic() - t0


def one(name, req, mod, py):
    venv = VENVS / f"{name}-{py}"
    if venv.exists():
        shutil.rmtree(venv)
    venv.parent.mkdir(parents=True, exist_ok=True)
    rec = {"candidate": name, "requirement": req, "python": py}
    try:
        p, _ = run(["uv", "venv", "--python", py, str(venv)])
        if p.returncode != 0:
            return {**rec, "outcome": "venv-failed", "stderr": p.stderr[-800:]}
        env = {**os.environ, "VIRTUAL_ENV": str(venv)}
        p, secs = run(["uv", "pip", "install", "--python", str(venv / "bin" / "python"), req], env=env)
        rec["install_seconds"] = round(secs, 1)
        err = p.stderr
        # uv prints "Building x==1.2" for anything with no usable wheel
        rec["source_builds"] = sorted({
            ln.split("Building", 1)[1].strip().split(" ")[0]
            for ln in err.splitlines() if "Building " in ln
        })
        if p.returncode != 0:
            return {**rec, "outcome": "install-failed",
                    "stderr_tail": err.strip().splitlines()[-14:]}
        p2, _ = run([str(venv / "bin" / "python"), "-c",
                     f"import {mod}, sys; "
                     f"print(getattr({mod}, '__version__', 'n/a'))"])
        if p2.returncode != 0:
            return {**rec, "outcome": "import-failed",
                    "stderr_tail": p2.stderr.strip().splitlines()[-10:]}
        rec["imported_version"] = p2.stdout.strip()
        # what actually landed, so a claim can be tied to exact versions
        p3, _ = run(["uv", "pip", "freeze", "--python", str(venv / "bin" / "python")], env=env)
        rec["freeze"] = p3.stdout.strip().splitlines()
        return {**rec, "outcome": "ok"}
    except subprocess.TimeoutExpired:
        return {**rec, "outcome": f"timeout-{TIMEOUT}s"}
    finally:
        pass


def main():
    uname = subprocess.run(["uname", "-srm"], capture_output=True, text=True).stdout.strip()
    res = {"measured_at": datetime.now(timezone.utc).isoformat(), "uname": uname,
           "uv": subprocess.run(["uv", "--version"], capture_output=True, text=True).stdout.strip(),
           "runs": []}
    for py in PYTHONS:
        for name, (req, mod) in CANDIDATES.items():
            r = one(name, req, mod, py)
            res["runs"].append(r)
            print(f"{py}  {name:20s} {r['outcome']:16s} "
                  f"{r.get('install_seconds','')}s builds={r.get('source_builds')}", flush=True)
            (OUT / "install.json").write_text(json.dumps(res, indent=2))
    print("done")


if __name__ == "__main__":
    main()
