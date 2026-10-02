"""L1 — what each option costs before it reads a byte.

THE NUMBER THAT MATTERS is the install closure: what `uv pip install X` actually puts on
disk, dependencies included. Two cheaper measurements were tried first and both lie:

  * walking the import-name directory  — misses siblings. duckdb's 54 MB engine ships as
    `_duckdb...so` NEXT TO the `duckdb/` package, so the directory reads 0.5 MB.
  * the distribution's own RECORD      — misses separate distributions. polars 1.44.2
    installs its Rust engine as `polars-runtime-32`, a DIFFERENT distribution carrying a
    171.8 MB `.so`, so polars' own RECORD reads 4.3 MB for a library that costs ~176 MB.

So each library gets its own venv and the whole site-packages tree is weighed. Import cost
is the minimum of seven cold subprocess imports in that same venv.

Output: results/l1-install.json
"""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

PINS = {
    "pandas": "pandas==3.0.5",
    "polars": "polars==1.44.2",
    "duckdb": "duckdb==1.5.5",
    "openpyxl": "openpyxl==3.1.5",
    "python-calamine": "python-calamine==0.8.2",
    "pandera": "pandera==0.33.1",
    "pydantic": "pydantic==2.13.5",
    "petl": "petl==1.7.25",
    "pyarrow": "pyarrow==25.0.1",
    "xlsxwriter": "XlsxWriter==3.2.9",
}
IMPORT_NAME = {"python-calamine": "python_calamine", "xlsxwriter": "xlsxwriter"}
ROUNDS = 7


def _ms(v) -> str:
    """import_ms returns None when the import failed, and a None through `:7.2f` raises
    TypeError from inside the reporting line."""
    return "  failed" if v is None else f"{v:7.2f}"


def tree_bytes(root: pathlib.Path) -> int:
    return sum(f.stat().st_size for f in root.rglob("*") if f.is_file() and not f.is_symlink())


def import_ms(py: str, module: str) -> float | None:
    code = (
        "import time,importlib\n"
        f"t=time.perf_counter(); importlib.import_module({module!r}); "
        "print((time.perf_counter()-t)*1000)\n"
    )
    best = None
    for _ in range(ROUNDS):
        out = subprocess.run([py, "-c", code], capture_output=True, text=True)
        if out.returncode != 0:
            # None, not float("nan"): json.dumps emits a bare NaN literal, which jq,
            # JSON.parse and every strict parser reject. A wheel that installs but fails
            # to import would make the whole results file unreadable outside Python.
            return None
        v = float(out.stdout.strip())
        best = v if best is None else min(best, v)
    return round(best, 2)


def measure(label: str, spec: str) -> dict:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="l1-"))
    try:
        venv = tmp / "v"
        subprocess.run(["uv", "venv", "--python", "3.12", str(venv)],
                       capture_output=True, check=True)
        sp = venv / "lib" / "python3.12" / "site-packages"
        empty = tree_bytes(sp)
        r = subprocess.run(["uv", "pip", "install", "--quiet", spec],
                           capture_output=True, text=True,
                           env={"VIRTUAL_ENV": str(venv), "PATH": "/usr/bin:/bin:" +
                                str(pathlib.Path.home() / ".local/bin")})
        if r.returncode != 0:
            return {"error": r.stderr[-400:]}
        full = tree_bytes(sp)
        dists = sorted(p.name.rsplit("-", 2)[0] for p in sp.glob("*.dist-info"))
        py = str((venv / "bin" / "python").absolute())
        ms = import_ms(py, IMPORT_NAME.get(label, label))
        return {
            "spec": spec,
            "install_bytes": full - empty,
            "site_packages_bytes": full,
            "distributions": dists,
            "dependency_count": max(0, len(dists) - 1),
            "import_ms_min_of_7": ms,
        }
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    rows = {}
    # The stdlib baseline: no install, and the import cost of a module already present.
    base_py = str(pathlib.Path(".venv/bin/python").absolute())
    rows["stdlib csv"] = {
        "spec": "ships with CPython",
        "install_bytes": 0,
        "distributions": [],
        "dependency_count": 0,
        "import_ms_min_of_7": import_ms(base_py, "csv"),
    }
    print(f"{'stdlib csv':18} {0:>9.1f} MB   0 deps   import "
          f"{_ms(rows['stdlib csv']['import_ms_min_of_7'])} ms")

    for label, spec in PINS.items():
        r = measure(label, spec)
        rows[label] = r
        if "error" in r:
            print(f"{label:18} INSTALL FAILED: {r['error'][:80]}")
            continue
        print(f"{label:18} {r['install_bytes']/1e6:>9.1f} MB   {r['dependency_count']:>2} deps   "
              f"import {_ms(r['import_ms_min_of_7'])} ms")

    meta = subprocess.run([base_py, "-VV"], capture_output=True, text=True).stdout.strip()
    out = pathlib.Path("results")
    out.mkdir(exist_ok=True)
    (out / "l1-install.json").write_text(json.dumps(
        {"python": meta, "rounds": ROUNDS,
         "method": "one isolated uv venv per library; whole site-packages tree weighed",
         "libraries": rows}, indent=2))
    print("\nwrote results/l1-install.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
