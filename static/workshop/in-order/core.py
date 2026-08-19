"""core.py — the measurement behind the 1.040 Collections floor model (working name: in order).

One copy, three readers: the page fetches it into Pyodide, a notebook can import it, the native
bench (01-discovery/bench/) imports it. Timing comes from /workshop/_lib/workshop.py. Every
function the page calls returns JSON.

The race: keep N random keys in sorted order, inserting one at a time. Pure-Python
sortedcontainers against the standard library's C (bisect.insort on a list), against "just
sort at the end", against a heap, against a dict that gives up on order. Then the operations
that decide whether you needed it sorted at all.
"""
import json, random, bisect, heapq, sys, time
from sortedcontainers import SortedList
from workshop import best as _best

def keys_for(n, seed=7):
    r = random.Random(seed)
    return [r.randrange(0, 1 << 40) for _ in range(n)]

def _once(fn):
    t0 = time.perf_counter(); fn(); return time.perf_counter() - t0

def _timed(fn, budget_s):
    """ms for one run: best-of under a budget for fast cases, a single run for slow ones."""
    s, _ = _best(lambda _: fn(), None, budget_s, min_reps=2)
    return s * 1000

STRUCTURES = {
    "SortedList (sortedcontainers, pure Python)": "sortedlist",
    "list + bisect.insort (stdlib, C)":           "insort",
    "list.append, then .sort() once":             "appendsort",
    "heapq (stdlib, C) — min only":               "heapq",
    "dict — no order at all":                      "dict",
}

def _racers(keys):
    def sortedlist():
        s = SortedList()
        for k in keys: s.add(k)
        return s
    def insort():
        l = []
        for k in keys: bisect.insort(l, k)
        return l
    def appendsort():
        l = []
        for k in keys: l.append(k)
        l.sort(); return l
    def hp():
        h = []
        for k in keys: heapq.heappush(h, k)
        return h
    def dct():
        d = {}
        for k in keys: d[k] = None
        return d
    return {"sortedlist": sortedlist, "insort": insort, "appendsort": appendsort, "heapq": hp, "dict": dct}

def race_one(n, key, budget_ms=150):
    """One structure, so a page can show the finishing order live. Same keys as race()."""
    fn = _racers(keys_for(int(n)))[key]
    return json.dumps({"n": int(n), "key": key, "ms": round(_timed(fn, budget_ms / 1000), 3)})

def race(n, budget_ms=150):
    """Insert n random keys one at a time into each structure. Returns ms per structure."""
    keys = keys_for(int(n))
    fns = _racers(keys)
    out = {}
    for label, key in STRUCTURES.items():
        out[key] = {"label": label, "ms": round(_timed(fns[key], budget_ms / 1000), 3)}
    base = out["insort"]["ms"]
    for v in out.values():
        v["x_vs_insort"] = round(base / v["ms"], 2) if v["ms"] else None
    return json.dumps({"n": int(n), "results": out})

def ops(n, probes=10_000, budget_ms=120):
    """At size n: membership, a range query, and pop-the-minimum — the operations that decide
    whether 'sorted' was the requirement or just 'fast'."""
    n = int(n); keys = keys_for(n); q = random.Random(9); pr = [q.randrange(0, 1 << 40) for _ in range(probes)]
    s = SortedList(keys); l = sorted(keys); st = set(keys)
    lo = keys[0]; hi = lo + (1 << 30)
    def sl_in():
        for p in pr: p in s
    def l_in():
        for p in pr:
            i = bisect.bisect_left(l, p); (i < len(l) and l[i] == p)
    def set_in():
        for p in pr: p in st
    def sl_range():
        return sum(1 for _ in s.irange(lo, hi))
    def l_range():
        a = bisect.bisect_left(l, lo); b = bisect.bisect_right(l, hi); return len(l[a:b])
    k = min(probes, n)
    def sl_pop():
        s2 = SortedList(keys)
        for _ in range(k): s2.pop(0)
    def l_pop():
        l2 = sorted(keys)
        for _ in range(k): l2.pop(0)
    def hp_pop():
        h = list(keys); heapq.heapify(h)
        for _ in range(k): heapq.heappop(h)
    B = budget_ms / 1000
    return json.dumps({"n": n, "probes": probes, "k": k,
        "membership": {"SortedList": _timed(sl_in, B), "bisect on list": _timed(l_in, B), "set": _timed(set_in, B)},
        "range":      {"SortedList.irange": _timed(sl_range, B), "bisect + slice": _timed(l_range, B)},
        "popmin":     {"SortedList.pop(0)": _timed(sl_pop, B), "list.pop(0)": _timed(l_pop, B), "heapq.heappop": _timed(hp_pop, B)}})

def functional(n_rows=100_000, budget_ms=150):
    """toolz vs cytoolz vs the standard library, on one pipeline over n_rows records."""
    import toolz, cytoolz
    from collections import defaultdict, Counter
    r = random.Random(7)
    rows = [{"user": r.randint(1, 500), "region": r.choice(["us", "eu", "ap"]), "bytes": r.randint(100, 50000)} for _ in range(int(n_rows))]
    def mk(tz):
        def pipe():
            g = tz.groupby("region", rows); f = tz.frequencies(tz.pluck("user", rows))
            s = tz.reduceby("user", lambda acc, x: acc + x["bytes"], rows, 0); return len(g), len(f), len(s)
        return pipe
    def hand():
        g = defaultdict(list)
        for x in rows: g[x["region"]].append(x)
        f = Counter(x["user"] for x in rows)
        s = defaultdict(int)
        for x in rows: s[x["user"]] += x["bytes"]
        return len(g), len(f), len(s)
    B = budget_ms / 1000
    return json.dumps({"n_rows": int(n_rows), "toolz": _timed(mk(toolz), B), "cytoolz": _timed(mk(cytoolz), B), "stdlib by hand": _timed(hand, B),
                       "toolz_version": toolz.__version__, "cytoolz_version": cytoolz.__version__})

def persistent(n=100_000, k=1000, budget_ms=150):
    """pyrsistent's point: k updates of an n-element vector, each producing a new value, against
    copying the whole thing each time — and the cost it pays on plain appends."""
    import pyrsistent
    from pyrsistent import pvector
    n = int(n); k = int(k)
    def pv_set():
        v = pvector(range(n))
        for i in range(k): v = v.set(i, -1)
    def tuple_copy():
        tp = tuple(range(n))
        for i in range(k): tp = tp[:i] + (-1,) + tp[i+1:]
    def pv_append():
        v = pvector()
        for i in range(n): v = v.append(i)
    def list_append():
        l = []
        for i in range(n): l.append(i)
    B = budget_ms / 1000
    impl = pyrsistent.pvector().__class__.__module__
    return json.dumps({"n": n, "k": k, "pvector.set x k": _timed(pv_set, B), "copy a tuple x k": _timed(tuple_copy, B),
                       "pvector.append x n": _timed(pv_append, B), "list.append x n": _timed(list_append, B),
                       "impl": "C extension (pvectorc)" if "pvectorc" in impl else "pure Python (pyrsistent._pvector)"})

def versions():
    import sortedcontainers, toolz, cytoolz, pyrsistent
    try:
        import importlib.metadata as md; pv = md.version("pyrsistent")
    except Exception: pv = "?"
    return json.dumps({"python": sys.version.split()[0], "sortedcontainers": sortedcontainers.__version__,
                       "toolz": toolz.__version__, "cytoolz": cytoolz.__version__, "pyrsistent": pv})
