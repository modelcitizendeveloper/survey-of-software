#!/usr/bin/env python3
"""Format the same pinned corpus with every formatter, and record what it cost.

A `measured-local` rung (docs/map/17-the-evidence-ladder.md). The numbers matter less than
the fact that anyone can reproduce them: pinned tools, a pinned corpus, a stated machine,
and the raw seconds rather than only the ratio.

FOUR METHODOLOGY DECISIONS, each of which changes the answer, so each is stated rather
than buried:

  FRESH CORPUS PER TOOL   formatting rewrites files, so the second tool would otherwise be
                          formatting the first tool's output. Every run gets its own copy.
  CACHES OFF              Ruff, Biome and dprint all cache aggressively. A warm cache is a
                          real number for a developer and the wrong one for a comparison,
                          because it measures the cache rather than the formatter. Cold
                          every time.
  WALL TIME, MEDIAN OF N  not the best run. A formatter people wait on is measured by what
                          it usually does.
  ALREADY-FORMATTED       the corpus is formatted once by each tool before timing, so the
                          timed run is the steady state a developer actually lives in and
                          not a one-off rewrite of the whole tree.
"""
from __future__ import annotations

import io
import json
import os
import platform
import shutil
import statistics
import subprocess
import sys
import tarfile
import time
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = Path("/tmp/bench")
CORPUS = WORK / "corpus"
# Measured 2026-08-27: at 3 reps the ruff-vs-black ratio moved 14.9x -> 18.5x between two
# identical container runs. Three is too few to separate a formatter from its own noise.
REPS = int(os.environ.get("REPS", "9"))

TOOLS = [
    # (name, language, argv builder, version argv)
    ("ruff",     "python", lambda d: ["ruff", "format", "--no-cache", "-q", str(d)],
                           ["ruff", "--version"]),
    ("black",    "python", lambda d: ["black", "-q", "--fast", str(d)],
                           ["black", "--version"]),
    ("autopep8", "python", lambda d: ["autopep8", "--in-place", "--recursive", str(d)],
                           ["autopep8", "--version"]),
    ("yapf",     "python", lambda d: ["yapf", "-i", "-r", str(d)],
                           ["yapf", "--version"]),
    ("prettier", "js",     lambda d: ["prettier", "--write", "--no-cache",
                                      "--log-level", "error", f"{d}/**/*.js"],
                           ["prettier", "--version"]),
    ("biome",    "js",     lambda d: ["biome", "format", "--write", str(d)],
                           ["biome", "--version"]),
    ("dprint",   "js",     lambda d: ["dprint", "fmt", "--config", str(WORK / "dprint.json")],
                           ["dprint", "--version"]),
]


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()


def pypi_source(pkg: str, version: str, into: Path) -> int:
    meta = json.loads(fetch(f"https://pypi.org/pypi/{pkg}/{version}/json").decode())
    files = meta["urls"]
    whl = next((f for f in files if f["filename"].endswith("-py3-none-any.whl")), None)
    src = whl or next(f for f in files if f["packagetype"] == "sdist")
    blob = fetch(src["url"])
    tmp = into / f"_{pkg}"
    tmp.mkdir(parents=True, exist_ok=True)
    if src["filename"].endswith(".whl"):
        zipfile.ZipFile(io.BytesIO(blob)).extractall(tmp)
    else:
        tarfile.open(fileobj=io.BytesIO(blob)).extractall(tmp, filter="data")
    return sum(1 for _ in tmp.rglob("*.py"))


def npm_source(pkg: str, version: str, subdir: str, into: Path) -> int:
    meta = json.loads(fetch(f"https://registry.npmjs.org/{pkg}/{version}").decode())
    blob = fetch(meta["dist"]["tarball"])
    tmp = into / f"_{pkg}"
    tmp.mkdir(parents=True, exist_ok=True)
    tarfile.open(fileobj=io.BytesIO(blob)).extractall(tmp, filter="data")
    keep = tmp / "package" / subdir
    if keep.is_dir():
        for f in keep.rglob("*.js"):
            f.rename(tmp / f.name)
    for junk in (tmp / "package",):
        shutil.rmtree(junk, ignore_errors=True)
    return sum(1 for _ in tmp.rglob("*.js"))


def scale_corpus(factor: int) -> None:
    """Replicate the corpus N times.

    A ratio measured at ONE size cannot settle a claim that names no size — which is
    exactly the defect the house rule targets. Sweeping the size is what turns "we measured
    19x" into "the ratio is a function of the workload, and the claim does not say which".
    """
    if factor <= 1:
        return
    for lang in ("python", "js"):
        base = CORPUS / lang
        originals = [f for f in base.rglob("*") if f.is_file()]
        for i in range(2, factor + 1):
            dest = base / f"_copy{i}"
            dest.mkdir(exist_ok=True)
            for f in originals:
                shutil.copy2(f, dest / f"{f.parent.name}__{f.name}")


def build_corpus() -> dict:
    spec = json.loads((HERE / "corpus.json").read_text())
    shutil.rmtree(CORPUS, ignore_errors=True)
    (CORPUS / "python").mkdir(parents=True)
    (CORPUS / "js").mkdir(parents=True)
    counts = {"python": 0, "js": 0}
    for e in spec["python"]:
        counts["python"] += pypi_source(e["package"], e["version"], CORPUS / "python")
    for e in spec["javascript"]:
        counts["js"] += npm_source(e["package"], e["version"], e["dir"], CORPUS / "js")
    size = {k: sum(f.stat().st_size for f in (CORPUS / k).rglob("*")
                   if f.is_file()) for k in counts}
    (WORK / "dprint.json").write_text(json.dumps({
        "typescript": {}, "includes": ["**/*.js"],
        "plugins": ["https://plugins.dprint.dev/typescript-0.93.3.wasm"]}))
    return {"files": counts, "bytes": size, "spec": spec}


def version_of(argv: list[str]) -> str:
    try:
        out = subprocess.run(argv, capture_output=True, text=True, timeout=120)
        return (out.stdout or out.stderr).strip().splitlines()[0][:60]
    except Exception as e:
        return f"unavailable ({type(e).__name__})"


def time_tool(name: str, lang: str, argv, reps: int, ok_codes=(0, 1),
              extra_files=(), use_cwd=False) -> dict:
    src = CORPUS / ("python" if lang == "python" else "js")
    times, failures = [], 0
    work = WORK / f"run-{name}"
    for i in range(reps + 1):          # +1: the first pass formats, the rest are steady state
        shutil.rmtree(work, ignore_errors=True)
        shutil.copytree(src, work)
        if lang == "js":
            shutil.copy(WORK / "dprint.json", work / "dprint.json")
        # Config files a LINTER needs beside the source it lints. Empty for the
        # formatters, so their timings are untouched: dropping an extra file into the
        # tree a formatter is about to rewrite would change what it is measuring.
        for extra in extra_files:
            src_cfg = WORK / extra
            if src_cfg.exists():
                shutil.copy(src_cfg, work / extra)
        # ESLint 10 resolves a flat config's `files` patterns relative to the CONFIG's
        # location, so pointing it at a directory from elsewhere matches nothing and it
        # exits 2 with "all of the files ... are ignored". It has to run from inside.
        cwd = work if (use_cwd or name == "dprint") else None
        t0 = time.perf_counter()
        try:
            r = subprocess.run(argv(work), capture_output=True, text=True, cwd=cwd,
                               timeout=1800)
        except FileNotFoundError:
            # A tool that is not installed is a RESULT — "we could not run it here" — not a
            # reason to lose the runs that already succeeded.
            shutil.rmtree(work, ignore_errors=True)
            return {"tool": name, "language": lang, "error": "not installed on this path"}
        dt = time.perf_counter() - t0
        if r.returncode not in ok_codes:   # 1 = "files were changed" for a formatter,
                                           # and "findings exist" for a linter. Pylint
                                           # goes further and returns a BITMASK, so its
                                           # caller widens this rather than the default.
            failures += 1
            if i == 0:
                return {"tool": name, "language": lang, "error":
                        (r.stderr or r.stdout).strip()[:300] or f"exit {r.returncode}"}
        if i:                              # discard the first, unformatted pass
            times.append(dt)
    shutil.rmtree(work, ignore_errors=True)
    return {"tool": name, "language": lang, "reps": len(times),
            "median_s": round(statistics.median(times), 4),
            "min_s": round(min(times), 4), "max_s": round(max(times), 4),
            "failures": failures}


def machine() -> dict:
    """ARCHITECTURE IS NOT A FOOTNOTE HERE. These are Rust binaries measured against CPython,
    and both sides of that comparison are compiled differently on aarch64 and x86_64. A ratio
    from one architecture is not directly comparable with a ratio from the other, so the arch
    is recorded explicitly and lands in the results filename rather than being buried in a
    platform string.

    `model name` only exists in /proc/cpuinfo on x86; ARM uses `Processor` or nothing at all,
    which is why the first version recorded an empty CPU on the machine it ran on."""
    cpu = ""
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            for key in ("model name", "Model name", "Processor", "CPU implementer", "Hardware"):
                if line.startswith(key):
                    cpu = cpu or line.split(":", 1)[1].strip()
    except Exception:
        pass
    mem = ""
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal"):
                mem = line.split(":", 1)[1].strip()
                break
    except Exception:
        pass
    return {"arch": platform.machine(),
            "cpu": cpu or platform.processor() or "unreported", "cores": os.cpu_count(),
            "memory": mem, "platform": platform.platform(),
            "python": platform.python_version(),
            "in_container": Path("/.dockerenv").exists()}


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    scale = int(os.environ.get("SCALE", "1"))
    print(f"building the pinned corpus (x{scale})...", file=sys.stderr)
    corpus = build_corpus()
    scale_corpus(scale)
    if scale > 1:
        for k in ("python", "js"):
            d = CORPUS / k
            corpus["files"][k] = sum(1 for f in d.rglob("*") if f.is_file())
            corpus["bytes"][k] = sum(f.stat().st_size for f in d.rglob("*") if f.is_file())
    corpus["scale"] = scale
    print(f"  python: {corpus['files']['python']} files, "
          f"{corpus['bytes']['python']//1024} KB", file=sys.stderr)
    print(f"  js:     {corpus['files']['js']} files, "
          f"{corpus['bytes']['js']//1024} KB", file=sys.stderr)

    versions = {name: version_of(v) for name, _, _, v in TOOLS}
    results = []
    for name, lang, argv, _ in TOOLS:
        print(f"  timing {name}...", file=sys.stderr)
        results.append(time_tool(name, lang, argv, REPS))

    out = {"corpus": corpus, "machine": machine(), "versions": versions,
           "ran_via": os.environ.get("BENCH_ENV", "container"),
           "reps": REPS, "results": results,
           "method": "fresh corpus per tool; caches disabled; first pass discarded so the "
                     "timed runs are steady-state; median of N wall-clock seconds"}
    # Name by environment AND scale. The first version wrote results.json from both paths,
    # so a container run silently overwrote the host numbers it was meant to be compared
    # against.
    via = os.environ.get("BENCH_ENV", "container")
    # Architecture in the filename, so an x86 droplet run and an ARM laptop run can sit
    # side by side instead of overwriting each other.
    dest = (Path(os.environ.get("OUT_DIR", "/out"))
            / f"results-{via}-{platform.machine()}-x{corpus['scale']}.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2))
    print(json.dumps(out["results"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
