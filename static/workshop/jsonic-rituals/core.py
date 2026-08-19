"""core.py — the measurement behind JSONic rituals (floor model for Survey of Software 1.056).

One copy, three readers: the page fetches it into Pyodide, the marimo notebook (jsonic.py)
imports it, the native bench (01-discovery/bench/) imports it. Timing and the shared API-log
sample come from /workshop/_lib/workshop.py. Every function that the page calls returns JSON.
"""
import json, random, sys, re
from typing import Any
import orjson, msgspec, msgspec.json, ujson, simplejson
from workshop import best as _best, json_logs

def nested_obj(seed=11, depth=6, fan=4):
    r = random.Random(seed)
    words = ["alpha","beta","gamma","delta","cache","ttl","region","replicas","enabled","endpoint","timeout","retries","backoff","weight","tags","owner","tier","mode","limit","burst"]
    def node(d):
        if d == 0:
            k = r.random()
            return (r.choice([True, False]) if k < .25 else r.randint(0, 5000) if k < .5
                    else r.choice(words) + "-" + str(r.randint(1, 99)) if k < .8
                    else [r.choice(words) for _ in range(r.randint(1, 4))])
        return {r.choice(words) + str(i): node(d-1) for i in range(fan)}
    return {"service": "checkout", "version": "2026.08", "env": node(depth)}

def numbers_obj(n=20000, seed=5):
    r = random.Random(seed); t = 1_723_900_000.0; out = []
    for _ in range(n):
        t += r.random() * 2
        out.append({"t": round(t, 3), "v": round(r.gauss(50, 12), 4), "q": r.randint(0, 3), "ok": r.random() > .02})
    return {"series": "sensor-7", "points": out}

_logs = [json.loads(l) for l in json_logs().decode().splitlines()]
SAMPLES = {"logs": _logs, "nested": nested_obj(), "numbers": numbers_obj(), "small": _logs[0]}

def set_own(text):
    try:
        SAMPLES["own"] = json.loads(text[:1024*1024])
        return json.dumps({"ok": True, "bytes": len(json.dumps(SAMPLES["own"], separators=(",", ":")).encode())})
    except Exception as e:
        return json.dumps({"ok": False, "err": str(e)[:120]})

# ── infer a msgspec.Struct from the reader's own JSON ───────────────────
_counter = [0]
def _ident(k):
    s = re.sub(r"\W", "_", k)
    return ("f_" + s) if (not s or s[0].isdigit() or s in {"from","class","import","def","return","None","True","False"}) else s
def infer_type(v, name="Item"):
    if isinstance(v, bool): return bool
    if isinstance(v, int): return int
    if isinstance(v, float): return float
    if isinstance(v, str): return str
    if v is None: return Any
    if isinstance(v, list):
        return list[infer_type(v[0], name + "Item")] if v else list[Any]
    if isinstance(v, dict):
        if not v: return dict[str, Any]
        _counter[0] += 1
        fields, renamed = [], {}
        for k, val in v.items():
            ident = _ident(k)
            if ident != k: renamed[ident] = k
            fields.append((ident, infer_type(val, name + "_" + ident.capitalize())))
        try: return msgspec.defstruct(f"{name}{_counter[0]}", fields, rename=renamed or None)
        except Exception: return dict[str, Any]
    return Any
def struct_source(tp):
    out = []
    def tname(t):
        if isinstance(t, type) and issubclass(t, msgspec.Struct): return t.__name__
        if t is Any: return "Any"
        if hasattr(t, "__origin__"): return f"{t.__origin__.__name__}[{', '.join(tname(a) for a in t.__args__)}]"
        return getattr(t, "__name__", str(t))
    def walk(t):
        if isinstance(t, type) and issubclass(t, msgspec.Struct):
            for f in msgspec.structs.fields(t): walk(f.type)
            src = "\n".join([f"class {t.__name__}(msgspec.Struct):"] + [f"    {f.name}: {tname(f.type)}" for f in msgspec.structs.fields(t)])
            if src not in out: out.append(src)
        elif hasattr(t, "__args__"):
            for a in t.__args__: walk(a)
    walk(tp)
    return "\n\n".join(out)

def measure(sample, budget_ms=120):
    obj = SAMPLES[sample]
    text = json.dumps(obj, separators=(",", ":")); data = text.encode()
    codecs = {
        "json (stdlib)": (json.dumps, json.loads, text, obj),
        "orjson":        (orjson.dumps, orjson.loads, data, obj),
        "msgspec":       (msgspec.json.encode, msgspec.json.decode, data, obj),
        "ujson":         (ujson.dumps, ujson.loads, text, obj),
        "simplejson":    (simplejson.dumps, simplejson.loads, text, obj),
    }
    schema = None; schema_err = None; schema_name = None; bad = None
    try:
        _counter[0] = 0
        Schema = infer_type(obj, "Payload")
        dec = msgspec.json.Decoder(Schema); enc = msgspec.json.Encoder()
        typed = dec.decode(data)
        codecs["msgspec typed (inferred Struct)"] = (enc.encode, dec.decode, data, typed)
        schema = struct_source(Schema); schema_name = getattr(Schema, "__name__", "Payload")
        # show validation: corrupt one leaf and decode again
        try:
            s2 = text
            m = re.search(r'"(\w+)":(\d+)', text)
            if m:
                s2 = text[:m.start(2)] + '"' + m.group(2) + '"' + text[m.end(2):]
                dec.decode(s2.encode()); bad = "decoded anyway"
        except msgspec.ValidationError as e:
            bad = str(e)[:160]
    except Exception as e:
        schema_err = str(e)[:140]
    rows = []
    for lib, (d, l, inp, src) in codecs.items():
        td, _ = _best(d, src, budget_ms/1000); tl, _ = _best(l, inp, budget_ms/1000)
        ok = True
        if "typed" not in lib:
            try: ok = (l(inp) == obj)
            except Exception: ok = False
        rows.append({"lib": lib, "dumps_ms": td*1000, "loads_ms": tl*1000,
                     "dumps_MBs": len(data)/td/1e6, "loads_MBs": len(data)/tl/1e6, "roundtrip": ok})
    base = rows[0]
    for r in rows:
        r["dumps_x"] = base["dumps_ms"]/r["dumps_ms"]; r["loads_x"] = base["loads_ms"]/r["loads_ms"]
    return json.dumps({"bytes": len(data), "rows": rows, "schema": schema, "schema_name": schema_name,
                       "schema_err": schema_err, "validation": bad})

def versions():
    return json.dumps({"python": sys.version.split()[0], "orjson": orjson.__version__, "msgspec": msgspec.__version__,
                       "ujson": ujson.__version__, "simplejson": simplejson.__version__})
