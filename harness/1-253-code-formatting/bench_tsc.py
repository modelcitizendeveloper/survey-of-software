#!/usr/bin/env python3
"""TypeScript 6 against TypeScript 7 — the same source, two implementations.

WHY THIS IS THE CLEANEST EXPERIMENT IN THE RANGE. Every other comparison here has a
confound: different tools implement different rule sets and answer subtly different
questions, which is why 1.250 had to construct matched rule sets before any ratio meant
anything. Here there is none. TypeScript 6.0.3 is the last TypeScript-in-TypeScript
release; 7.0.2 is the Go rewrite. Same language specification, same source, same config.
Only the implementation differs.

AND THE CLOCK IS THE LESSER HALF. A rewrite promising "the same code typechecks the same
way" makes a claim about a very large surface, and it is checkable for free once both are
installed: run both, capture the diagnostics, diff them. A speed number that came with
different errors would not be a speed number at all.

Inherits the harness's method: pinned immutable corpus, fresh copy per run, first pass
discarded, median of nine, caches off (tsc is given no --incremental and no tsbuildinfo
survives between runs, so every timed run is cold).
"""
from __future__ import annotations
import json, os, platform, statistics, subprocess, shutil, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bench                                    # noqa: E402

WORK = bench.WORK
TSC = {"6": "/opt/ts6/bin/tsc", "7": "/opt/ts7/bin/tsc"}

TSCONFIG = {
    "compilerOptions": {
        # node16, NOT "node". "node" resolves to node10, which TypeScript 6 deprecates
        # and TypeScript 7 has REMOVED — so both runs failed on the config instead of
        # checking the corpus, and the timings were the cost of printing an error. The
        # diagnostic diff caught it on the first run, which is the argument for capturing
        # diagnostics rather than only the clock.
        "target": "ES2022", "module": "node16", "moduleResolution": "node16",
        "allowJs": True, "checkJs": True, "noEmit": True,
        # skipLibCheck is what nearly every real project sets, and leaving it off would
        # make this a measurement of node_modules' own declaration files instead.
        "skipLibCheck": True,
        "strict": False,          # the corpus is untyped JS; strict would drown both runs
        "incremental": False,     # every timed run is cold, by construction
    },
    # SCOPED TO express, and this is a real constraint rather than a convenience.
    #
    # axios ships lib/axios.js and lib/core/Axios.js, which differ only in casing. tsc
    # raises TS1149 on that and REFUSES TO BUILD THE PROGRAM, so a run including axios
    # times a failure rather than a check — the first version of this benchmark did
    # exactly that and reported 4.9x. forceConsistentCasingInFileNames: false does not
    # suppress it; the check is unconditional in modern TypeScript.
    #
    # So the tsc cell uses the express half of the shared corpus. That is a smaller
    # workload than the lint and format cells use, and any number from it says so.
    "include": ["_express/**/*.js"],
}


def run_once(binary: str, work: Path) -> tuple[float, str, int]:
    t0 = time.perf_counter()
    r = subprocess.run([binary, "-p", str(work)], capture_output=True, text=True,
                       timeout=3600)
    return time.perf_counter() - t0, (r.stdout or "") + (r.stderr or ""), r.returncode


def normalise(out: str, work: Path) -> list[str]:
    """Diagnostics, comparable between runs: absolute paths and ordering removed."""
    lines = []
    for line in out.splitlines():
        line = line.replace(str(work) + "/", "").replace(str(work), "").strip()
        if line and not line.startswith("Found ") and "error" in line.lower():
            lines.append(line)
    return sorted(lines)


def time_tsc(ver: str, reps: int) -> dict:
    binary = TSC[ver]
    src = bench.CORPUS / "js"
    work = WORK / f"tsc{ver}"
    times, diags, rc = [], None, None
    for i in range(reps + 1):                   # +1: first pass discarded
        shutil.rmtree(work, ignore_errors=True)
        shutil.copytree(src, work)
        (work / "tsconfig.json").write_text(json.dumps(TSCONFIG), encoding="utf-8")
        try:
            dt, out, rc = run_once(binary, work)
        except FileNotFoundError:
            shutil.rmtree(work, ignore_errors=True)
            return {"version": ver, "error": f"{binary} not installed"}
        if i == 0:
            diags = normalise(out, work)        # capture from the discarded pass
        else:
            times.append(dt)
    shutil.rmtree(work, ignore_errors=True)
    v = subprocess.run([binary, "--version"], capture_output=True, text=True).stdout.strip()
    return {"version": ver, "reported": v, "reps": len(times),
            "median_s": round(statistics.median(times), 4),
            "min_s": round(min(times), 4), "max_s": round(max(times), 4),
            "exit_code": rc, "diagnostic_count": len(diags), "diagnostics": diags}


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    scale = int(os.environ.get("SCALE", "1"))
    reps = bench.REPS
    corpus = bench.build_corpus()
    bench.scale_corpus(scale)
    if scale > 1:
        for k in ("python", "js"):
            d = bench.CORPUS / k
            corpus["files"][k] = sum(1 for f in d.rglob("*") if f.is_file())
            corpus["bytes"][k] = sum(f.stat().st_size for f in d.rglob("*") if f.is_file())
    corpus["scale"] = scale
    print(f"js corpus: {corpus['files']['js']} files, {corpus['bytes']['js']//1024} KB",
          flush=True)

    results = {}
    for ver in ("6", "7"):
        print(f"  timing tsc {ver} ...", flush=True)
        results[ver] = time_tsc(ver, reps)
        r = results[ver]
        print(f"    {r.get('reported','?')}  median {r.get('median_s','-')}s  "
              f"{r.get('diagnostic_count','-')} diagnostics", flush=True)

    # THE COMPARISON THAT MATTERS MORE THAN THE CLOCK
    agree = None
    if "diagnostics" in results["6"] and "diagnostics" in results["7"]:
        a, b = set(results["6"]["diagnostics"]), set(results["7"]["diagnostics"])
        agree = {"identical": a == b,
                 "only_in_6": sorted(a - b)[:400], "only_in_7": sorted(b - a)[:400],
                 "count_6": len(a), "count_7": len(b)}
        print(f"\n  diagnostics identical: {agree['identical']}  "
              f"({len(a)} vs {len(b)}; {len(a-b)} only in 6, {len(b-a)} only in 7)")

    ratio = None
    if all("median_s" in results[v] for v in ("6", "7")) and results["7"]["median_s"]:
        ratio = round(results["6"]["median_s"] / results["7"]["median_s"], 2)
        print(f"  tsc6 / tsc7 = {ratio}x")

    out = {"kind": "tsc", "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
           "scale": scale, "reps": reps, "machine": bench.machine(), "corpus": corpus,
           "tsconfig": TSCONFIG, "results": results,
           "speed_ratio_6_over_7": ratio, "diagnostic_agreement": agree,
           "caveat": ("The corpus is JavaScript checked with --checkJs, not a densely "
                      "annotated TypeScript project. Both implementations do identical "
                      "work on identical input, so the 6-vs-7 ratio is valid; it is NOT "
                      "'how fast tsc is on a TypeScript codebase'.")}
    via = os.environ.get("BENCH_ENV", "container")
    f = (Path(os.environ.get("OUT_DIR", "/out"))
         / f"tsc-{via}-{platform.machine()}-x{scale}.json")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
