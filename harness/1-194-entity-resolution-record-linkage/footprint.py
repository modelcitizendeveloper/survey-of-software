#!/usr/bin/env python3
"""
Install footprint: bytes on disk and number of distributions, per candidate.

Adoption cost is not only whether it installs. A 6 GB virtual environment is a
container image, a CI cache and a cold-start time, and it is invisible on PyPI.
Measured from the venvs the install matrix built, after they settled — a venv
measured mid-install includes build directories and reads high.
"""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
VENVS = HERE / ".venvs"
out = {}
for v in sorted(VENVS.iterdir()):
    if not v.is_dir() or not (v / "bin" / "python").exists():
        continue
    du = subprocess.run(["du", "-sb", str(v)], capture_output=True, text=True)
    size = int(du.stdout.split()[0]) if du.returncode == 0 else None
    n = subprocess.run(
        [str(v / "bin" / "python"), "-c",
         "import importlib.metadata as m;"
         "ds=[d.metadata['Name'] for d in m.distributions()];"
         "import json;print(json.dumps(sorted(x for x in ds if x)))"],
        capture_output=True, text=True)
    dists = json.loads(n.stdout) if n.returncode == 0 else []
    out[v.name] = {"bytes": size, "mib": round(size / 1048576, 1) if size else None,
                   "distributions": len(dists), "names": dists}
    print(f"{v.name:28s} {out[v.name]['mib']:>9} MiB  {len(dists):>4} dists", flush=True)
(HERE / "results" / "footprint.json").write_text(json.dumps(out, indent=2))
