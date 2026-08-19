"""workshop.py — the Python half of the Survey of Software workshop runtime.

One copy, three readers: floor-model pages fetch it into Pyodide alongside their core.py,
the marimo notebooks import it, the native benches import it. Anything measured on more
than one page lives here so the number means the same thing everywhere.
"""
import json, random, time

__version__ = "2026-08-19"


def best(fn, arg, budget_s=0.12, min_reps=3):
    """Best-of timing under a wall-clock budget.

    Browser clocks clamp (100 µs in Chromium without cross-origin isolation), so calls are
    timed in batches calibrated to take at least 5 ms — fifty clamp ticks — before a reading
    is trusted. Slow calls get one measured rep. Returns (seconds_per_call, reps).
    """
    t0 = time.perf_counter(); fn(arg); first = time.perf_counter() - t0
    if first > budget_s:
        return first, 1
    k = 1
    while True:                       # calibrate the batch, not the call
        t0 = time.perf_counter()
        for _ in range(k): fn(arg)
        dt = time.perf_counter() - t0
        if dt >= 0.005 or k >= 200_000: break
        k *= 4
    b = dt / k; reps = 1; total = dt
    while reps < min_reps or total < budget_s:
        t0 = time.perf_counter()
        for _ in range(k): fn(arg)
        dt = time.perf_counter() - t0
        if dt > 0: b = min(b, dt / k)
        reps += 1; total += dt
        if reps >= 40: break
    return max(b, 1e-9), reps


def json_logs(target=512 * 1024, seed=7):
    """512 KB of API access logs, one JSON object per line — deterministic, so the same bytes
    are measured natively, in every page that uses them (1.050 compresso, 1.056 jsonic-rituals)
    and on the machine the survey figures came from."""
    r = random.Random(seed)
    routes = ["/api/v1/users", "/api/v1/orders", "/api/v1/orders/{id}", "/api/v1/cart",
              "/api/v1/products", "/api/v1/products/{id}/reviews", "/health", "/api/v1/auth/token"]
    methods = ["GET"] * 6 + ["POST"] * 2 + ["PUT", "DELETE"]
    agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
              "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
              "python-requests/2.32.3", "curl/8.5.0", "okhttp/4.12.0"]
    out = []; size = 0; t = 1_723_900_000
    while size < target:
        t += r.randint(0, 3)
        rec = {"ts": t, "level": r.choice(["INFO"] * 8 + ["WARN", "ERROR"]),
               "req_id": "%032x" % r.getrandbits(128),
               "user": {"id": r.randint(1000, 99999), "plan": r.choice(["free", "free", "pro", "team"])},
               "http": {"method": r.choice(methods), "path": r.choice(routes).replace("{id}", str(r.randint(1, 50000))),
                        "status": r.choice([200] * 7 + [201, 304, 404, 500]), "bytes": r.randint(120, 48000),
                        "latency_ms": round(r.lognormvariate(3.2, 0.7), 1)},
               "ua": r.choice(agents), "region": r.choice(["us-west-2", "us-east-1", "eu-central-1"]),
               "tags": r.sample(["cache-hit", "cache-miss", "retry", "slow", "auth", "cdn"], r.randint(0, 3))}
        line = json.dumps(rec, separators=(",", ":")) + "\n"
        out.append(line); size += len(line)
    return "".join(out).encode()


def random_bytes(n=256 * 1024, seed=7):
    """Incompressible: what any already-compressed file looks like to a codec."""
    return random.Random(seed).randbytes(n)
