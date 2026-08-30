#!/usr/bin/env python3
"""Lint half of the 1.253/1.250 harness — the FORMATTER harness, extended, not replaced.

Everything that makes a number trustworthy is inherited from bench.py: the pinned
immutable corpus, a fresh copy per tool, caches off, the first pass discarded, and the
median of nine. Rebuilding any of that would make 1.250's linting ratios incomparable
with 1.253's formatting ratios, and that comparison is one of the results.

WHAT IS DIFFERENT ABOUT TIMING LINTERS

  Exit codes. A formatter returns 0, or 1 for "files changed". A linter returns non-zero
  to mean "I found something", which is the normal case on real code. Pylint goes further
  and returns a BITMASK (1 fatal, 2 error, 4 warning, 8 refactor, 16 convention), so a
  clean-ish run can exit 20 and be perfectly healthy. Each tool declares what it may return.

  Rule sets. This is the hard part, and formatters do not have it. Formatters are
  comparable by default because they all do the same job. Ruff running four rules and
  Flake8 running three hundred are NOT doing comparable work, and a ratio between them
  measures the configuration. So:

    ruff check --select E,W,F,C90   matches Flake8's default (pycodestyle E/W + pyflakes F
                                    + mccabe C90). Both then run the same checks.
    pylint                          has no match. Nothing else does whole-program
                                    inference, so there is no honest ratio — it is timed
                                    alone and reported as a fact about Pylint.
    eslint/oxlint/biome lint        share eslint.config.mjs's intersection set where the
                                    tool can read it; the caveat for each is in RESULTS.

  Caches. Ruff, Biome and oxlint all cache aggressively. A warm cache is a real number for
  a developer and the wrong one for a comparison, because it measures the cache.
"""
from __future__ import annotations
import json, os, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bench                                    # noqa: E402  — the harness proper

WORK = bench.WORK
BIOME2 = "/opt/biome2/bin/biome"                # Biome 2.5.11, kept off 1.253's 1.9.4 path

LINT_TOOLS = [
    # (name, language, argv builder, version argv, acceptable exit codes)
    ("ruff-check", "python",
     lambda d: ["ruff", "check", "--no-cache", "--quiet", "--exit-zero",
                "--select", "E,W,F,C90", str(d)],
     ["ruff", "--version"], (0,)),

    ("flake8", "python",
     lambda d: ["flake8", str(d)],
     ["flake8", "--version"], (0, 1)),

    # Timed alone, not raced. --disable=all + a named enable would defeat the point:
    # what costs time in Pylint is the inference it does before any check runs.
    ("pylint", "python",
     lambda d: ["pylint", "--recursive=y", "--score=n", "--persistent=n",
                "--output-format=text", str(d)],
     ["pylint", "--version"], tuple(range(0, 64))),

    # Runs from inside the copied corpus with the config beside it; see bench.time_tool.
    # Exit 2 is NOT accepted: for ESLint that is a fatal error, and accepting it is how
    # the first version of this benchmark timed an error message nine times and reported
    # it as a result.
    ("eslint", "js",
     lambda d: ["eslint", "."],
     ["eslint", "--version"], (0, 1)),

    ("oxlint", "js",
     lambda d: ["oxlint", "--silent", "."],
     ["oxlint", "--version"], (0, 1)),

    ("biome-lint", "js",
     lambda d: [BIOME2, "lint", "--config-path=.", "."],
     [BIOME2, "--version"], (0, 1)),
]


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    scale = int(os.environ.get("SCALE", "1"))
    reps = bench.REPS
    print(f"building the pinned corpus (x{scale})...", flush=True)
    corpus = bench.build_corpus()
    bench.scale_corpus(scale)
    if scale > 1:                       # recount after replication, as bench.main does
        for k in ("python", "js"):
            d = bench.CORPUS / k
            corpus["files"][k] = sum(1 for f in d.rglob("*") if f.is_file())
            corpus["bytes"][k] = sum(f.stat().st_size for f in d.rglob("*") if f.is_file())
    corpus["scale"] = scale
    print(f"  python: {corpus['files']['python']} files, {corpus['bytes']['python']//1024} KB")
    print(f"  js:     {corpus['files']['js']} files, {corpus['bytes']['js']//1024} KB", flush=True)

    # configs the JS linters need to see
    here = Path(__file__).resolve().parent
    for name in ("eslint.config.mjs",):
        src = here / name
        if src.exists():
            (WORK / name).write_bytes(src.read_bytes())
    # Biome needs a config object even to lint with defaults
    (WORK / "biome.json").write_text(json.dumps({
        "$schema": "https://biomejs.dev/schemas/2.5.11/schema.json",
        "linter": {"enabled": True, "rules": {"recommended": True}},
        "formatter": {"enabled": False},
    }), encoding="utf-8")

    only = {x for x in os.environ.get("ONLY", "").split(",") if x}
    # INTERLEAVED. Every tool takes one pass, then every tool takes another, rather than
    # all nine passes of one tool before the next begins. Sequential timing gave each tool
    # its own time window, so a machine that got busier between windows biased the ratio —
    # and the min/med/max estimator check could not detect it, because that only measures
    # variance INSIDE a window. See the correction at the top of RESULTS.md.
    specs = [{"name": n, "lang": l, "argv": a, "ok_codes": ok,
              "extra_files": ("eslint.config.mjs", "biome.json"), "use_cwd": (l == "js")}
             for n, l, a, _v, ok in LINT_TOOLS if not (only and n not in only)]
    versions = {n: v for n, _l, _a, v, _ok in LINT_TOOLS}
    print(f"  interleaving {len(specs)} tools x {reps} reps ...", flush=True)
    results = []
    for row in bench.interleave(specs, reps):
        name = row["tool"]
        row["version"] = bench.version_of(versions[name])
        row["rule_set"] = {
            "ruff-check": "E,W,F,C90 — matched to Flake8's default",
            "flake8": "default (pycodestyle E/W + pyflakes F + mccabe C90)",
            "pylint": "default; NOT matched to anything — timed alone, no ratio",
            "eslint": "eslint.config.mjs intersection set",
            "oxlint": "default correctness rules",
            "biome-lint": "recommended",
        }[name]
        results.append(row)
        print(f"    {json.dumps(row)}", flush=True)

    out = {
        "kind": "lint",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "scale": scale,
        "reps": reps,
        "machine": bench.machine(),
        "corpus": corpus,
        "results": results,
        "caveat": ("Ratios are only meaningful between tools running a MATCHED rule set. "
                   "ruff-check vs flake8 is matched. pylint is timed alone. The JS trio "
                   "share an intersection config where each tool can read one; see "
                   "rule_set on each row."),
    }
    # Same naming convention as the formatter half: environment AND architecture AND scale,
    # so an ARM laptop run and an x86 droplet run sit side by side instead of overwriting.
    via = os.environ.get("BENCH_ENV", "container")
    import platform
    # A PARTIAL run must not claim the canonical filename. bench.py carries a comment
    # about this exact failure — an earlier version wrote one results.json from both the
    # host and container paths, so one silently overwrote the numbers it was meant to be
    # compared against. A filtered run reproduced it here: ONLY=eslint,oxlint,biome-lint
    # destroyed the ruff, flake8 and pylint cells in the file it landed on.
    suffix = "-partial" if only else ""
    f = (Path(os.environ.get("OUT_DIR", "/out"))
         / f"lint-{via}-{platform.machine()}-x{scale}{suffix}.json")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
