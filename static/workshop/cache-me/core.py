"""core.py — the measurement behind the 1.047 Caching Libraries floor model (cache me if you can).

One copy, three readers: the page fetches it into Pyodide, a notebook can import it, the native
bench (01-discovery/bench/) imports it. Timing comes from /workshop/_lib/workshop.py. Every
function the page calls returns JSON.

Three questions, in the order a cache decision is actually made:
  1. what does a hit cost, per tier — a dict, the stdlib's lru_cache, cachetools' policies,
     diskcache's SQLite (the network tier is measured by the bench, not the page);
  2. which eviction policy earns the hit rate, on the access pattern you actually have —
     replayed through cachetools' own cache classes, against the offline optimum;
  3. does it pay — the break-even cost of the function you are wrapping.
"""
import json, random, sys, time, functools, heapq, os, shutil, tempfile
import cachetools
from workshop import best as _best

# ── 1. what a hit costs ──────────────────────────────────────────────────────

def _per_call_us(run, n, budget_s):
    s, _ = _best(run, None, budget_s, min_reps=2)
    return s / n * 1e6

def hit_cost(budget_ms=80):
    """µs per call for a hit on each tier, and µs per store (a miss's extra cost), using the
    cheapest possible wrapped function so the overhead is the whole number."""
    import diskcache
    n = 1000; keys = list(range(n))
    def work(k): return k + 1
    d = {k: work(k) for k in keys}
    f_lru = functools.lru_cache(maxsize=2048)(work)
    f_ct_lru = cachetools.cached(cachetools.LRUCache(2048))(work)
    f_ct_ttl = cachetools.cached(cachetools.TTLCache(2048, ttl=600))(work)
    f_ct_lfu = cachetools.cached(cachetools.LFUCache(2048))(work)
    tmp = tempfile.mkdtemp(prefix="cache-me-"); dc = diskcache.Cache(tmp)
    f_dc = dc.memoize()(work)
    for k in keys: f_lru(k); f_ct_lru(k); f_ct_ttl(k); f_ct_lfu(k); f_dc(k); dc.set(k, k + 1)
    def loop(f, ks=keys):
        def run(_):
            for k in ks: f(k)
        return run
    B = budget_ms / 1000
    hits = {}
    for label, f in [("the function itself (k + 1)", work), ("dict lookup", d.__getitem__),
                     ("functools.lru_cache (stdlib, C)", f_lru), ("cachetools LRUCache", f_ct_lru),
                     ("cachetools TTLCache", f_ct_ttl), ("cachetools LFUCache", f_ct_lfu),
                     ("diskcache.memoize (SQLite)", f_dc), ("diskcache.get", dc.get)]:
        hits[label] = _per_call_us(loop(f), n, B)
    # stores: a run fills a fresh cache with n new keys
    def st_dict(_):
        c = {}
        for k in keys: c[k] = k
    def st_lru(_):
        f = functools.lru_cache(maxsize=2048)(work)
        for k in keys: f(k)
    def st_ct(cls, **kw):
        def run(_):
            c = cls(2048, **kw)
            for k in keys: c[k] = k
        return run
    kd = list(range(200)); i = [0]
    def st_dc(_):
        base = i[0] * 1000 + 100_000; i[0] += 1
        for k in kd: dc.set(base + k, k)
    def st_dc_tx(_):
        base = i[0] * 1000 + 100_000; i[0] += 1
        with dc.transact():
            for k in kd: dc.set(base + k, k)
    stores = {"dict": _per_call_us(st_dict, n, B), "functools.lru_cache": _per_call_us(st_lru, n, B),
              "cachetools LRUCache": _per_call_us(st_ct(cachetools.LRUCache), n, B),
              "cachetools TTLCache": _per_call_us(st_ct(cachetools.TTLCache, ttl=600), n, B),
              "cachetools LFUCache": _per_call_us(st_ct(cachetools.LFUCache), n, B),
              "diskcache.set": _per_call_us(st_dc, len(kd), B),
              "diskcache.set, 200 in one transaction": _per_call_us(st_dc_tx, len(kd), B)}
    dc.close(); shutil.rmtree(tmp, ignore_errors=True)
    return json.dumps({"per_hit_us": hits, "per_store_us": stores})

# ── 2. which policy, on which pattern ────────────────────────────────────────

PATTERNS = {
    "hot":      "a hot set — a few keys get most of the requests (Zipf)",
    "uniform":  "no favourites — every key equally likely",
    "loop":     "a loop — read every key in order, over and over",
    "hot+scan": "a hot set, with a scan through everything mixed in (1 request in 4)",
    "shift":    "a hot set that moves — different favourites every third of the run",
}

def requests(pattern, universe=10_000, n=30_000, seed=7):
    r = random.Random(seed); universe = int(universe); n = int(n)
    if pattern == "uniform":
        return [r.randrange(universe) for _ in range(n)]
    if pattern == "loop":
        return [i % universe for i in range(n)]
    w = [1.0 / (i + 1) for i in range(universe)]            # Zipf, s = 1
    pop = list(range(universe)); r.shuffle(pop)              # hot keys are not the low numbers
    hot = r.choices(pop, weights=w, k=n)
    if pattern == "hot":
        return hot
    if pattern == "hot+scan":
        return [hot[i] if i % 4 else (i // 4) % universe for i in range(n)]
    if pattern == "shift":
        out = []; third = n // 3
        for phase in range(3):
            r.shuffle(pop); out += r.choices(pop, weights=w, k=third)
        return out + hot[len(out):]
    raise ValueError(pattern)

def _replay(c, seq):
    hits = 0; get = c.__getitem__
    for k in seq:
        try:
            get(k); hits += 1
        except KeyError:
            c[k] = 1
    return hits / len(seq)

def _optimal(seq, size):
    """Belady's offline MIN — evict whatever is needed furthest in the future. The ceiling."""
    INF = 1 << 60; nxt = [0] * len(seq); last = {}
    for i in range(len(seq) - 1, -1, -1):
        nxt[i] = last.get(seq[i], INF); last[seq[i]] = i
    cache = {}; heap = []; hits = 0
    for i, k in enumerate(seq):
        if k in cache:
            hits += 1
        elif len(cache) >= size:
            while True:
                nu, ek = heapq.heappop(heap)
                if ek in cache and cache[ek] == -nu:
                    del cache[ek]; break
        cache[k] = nxt[i]; heapq.heappush(heap, (-nxt[i], k))
    return hits / len(seq)

POLICIES = {"LRU": cachetools.LRUCache, "LFU": cachetools.LFUCache,
            "FIFO": cachetools.FIFOCache, "random (RR)": cachetools.RRCache}

def policies(pattern, cache_pct=10, universe=10_000, n=30_000):
    """Hit rate per eviction policy when a cache holding cache_pct % of the keys replays n
    requests of the given pattern — each policy is cachetools' own class, plus the stdlib's
    lru_cache and the offline optimum."""
    universe = int(universe); n = int(n)
    size = max(1, int(universe * float(cache_pct) / 100))
    seq = requests(pattern, universe, n)
    out = {}
    for name, cls in POLICIES.items():
        t0 = time.perf_counter(); h = _replay(cls(size), seq); dt = time.perf_counter() - t0
        out[name] = {"hit_rate": h, "ms": dt * 1000}
    @functools.lru_cache(maxsize=size)
    def f(k): return k
    t0 = time.perf_counter()
    for k in seq: f(k)
    ci = f.cache_info()
    out["functools.lru_cache"] = {"hit_rate": ci.hits / len(seq), "ms": (time.perf_counter() - t0) * 1000}
    out["optimal (offline)"] = {"hit_rate": _optimal(seq, size), "ms": None}
    distinct = len(set(seq))
    return json.dumps({"pattern": pattern, "description": PATTERNS[pattern], "universe": universe,
                       "distinct_requested": distinct, "n": n, "cache_size": size, "cache_pct": float(cache_pct),
                       "results": out})

def belady_anomaly():
    """The textbook sequence on which FIFO misses MORE with a bigger cache — run through
    cachetools' own FIFOCache and LRUCache."""
    seq = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    out = {}
    for name, cls in [("FIFO", cachetools.FIFOCache), ("LRU", cachetools.LRUCache)]:
        out[name] = {str(s): round((1 - _replay(cls(s), seq)) * len(seq)) for s in (3, 4)}
    return json.dumps({"sequence": seq, "misses": out})

# ── 3. does it pay ───────────────────────────────────────────────────────────

def payoff(fn_us, hit_rate, hit_us, store_us):
    """Mean µs per call with the cache against without, and the hit rate at which the cache
    breaks even — the arithmetic the page, the notebook and the survey all use."""
    fn_us = float(fn_us); h = float(hit_rate); hit_us = float(hit_us); store_us = float(store_us)
    with_cache = h * hit_us + (1 - h) * (fn_us + store_us)
    # pays when h*hit + (1-h)*(fn+store) < fn  ⇔  h > store / (fn + store - hit)
    denom = fn_us + store_us - hit_us
    breakeven = store_us / denom if denom > 0 else None
    if breakeven is not None and breakeven > 1: breakeven = None          # never pays
    return json.dumps({"fn_us": fn_us, "hit_rate": h, "without_us": fn_us, "with_us": with_cache,
                       "speedup": fn_us / with_cache if with_cache else None,
                       "breakeven_hit_rate": breakeven})

# ── 4. memory per entry ──────────────────────────────────────────────────────

def memory(n=10_000):
    """Bytes per cached entry, int -> int, measured with tracemalloc on a fresh structure."""
    import tracemalloc
    n = int(n); ks = list(range(n))
    def build_dict(): return {k: k + 1 for k in ks}
    def build(cls, **kw):
        def b():
            c = cls(n + 1, **kw)
            for k in ks: c[k] = k + 1
            return c
        return b
    def build_lru():
        f = functools.lru_cache(maxsize=n + 1)(lambda k: k + 1)
        for k in ks: f(k)
        return f
    out = {}
    for label, b in [("dict", build_dict), ("functools.lru_cache", build_lru),
                     ("cachetools LRUCache", build(cachetools.LRUCache)),
                     ("cachetools TTLCache", build(cachetools.TTLCache, ttl=600)),
                     ("cachetools LFUCache", build(cachetools.LFUCache))]:
        tracemalloc.start(); s0, _ = tracemalloc.get_traced_memory()
        obj = b()
        s1, _ = tracemalloc.get_traced_memory(); tracemalloc.stop()
        out[label] = (s1 - s0) / n
        del obj
    return json.dumps({"n": n, "bytes_per_entry": out})

def versions():
    import diskcache
    return json.dumps({"python": sys.version.split()[0], "cachetools": cachetools.__version__,
                       "diskcache": diskcache.__version__})
