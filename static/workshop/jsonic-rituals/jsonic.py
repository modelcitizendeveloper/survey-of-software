# /// script
# requires-python = ">=3.12"
# dependencies = ["marimo", "orjson", "msgspec", "ujson", "simplejson", "pydantic"]
# ///
"""JSONic rituals — a floor model for Survey of Software 1.056 (JSON Libraries).

One marimo notebook that is both the lab (run it: `uvx marimo edit jsonic.py`)
and, exported with `marimo export html-wasm`, the page. Every figure is measured
in the tab while you wait. Where a number came from research instead, it says so.
"""
import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", app_title="JSONic rituals — a floor model for Survey of Software 1.056")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import json, time, random, sys, re
    import orjson, msgspec, msgspec.json, ujson, simplejson
    from typing import Any
    return Any, json, mo, msgspec, orjson, random, re, simplejson, sys, time, ujson


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
<p style="font-size:.78rem;text-transform:uppercase;letter-spacing:.09em;color:#94a3b8;font-weight:600;margin:0 0 12px">
Workshop · floor model for <a href="/survey/1-056/">Survey of Software 1.056</a></p>

# JSONic rituals

**The 6× is a serialising number.** orjson writes JSON five to ten times faster than the
standard library — and reads it back about twice as fast. The fastest *reader* on this
page is the one that also checks the shape of what it read. Paste your own JSON below and
the numbers are about your data.
"""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    register = mo.ui.switch(label="Engineering register — versions, bytes, the measurement behind each claim", value=False)
    register
    return (register,)


@app.cell(hide_code=True)
def _(json, random):
    # ── samples: the same bytes natively and here ──────────────────────────
    def json_logs(target=512 * 1024, seed=7):
        """compresso's generator, unchanged — the 512 KB of API logs from survey 1.050."""
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
        return "".join(out)

    def nested_obj(seed=11, depth=6, fan=4):
        r = random.Random(seed)
        words = ["alpha", "beta", "gamma", "delta", "cache", "ttl", "region", "replicas", "enabled", "endpoint",
                 "timeout", "retries", "backoff", "weight", "tags", "owner", "tier", "mode", "limit", "burst"]
        def node(d):
            if d == 0:
                k = r.random()
                return (r.choice([True, False]) if k < .25 else r.randint(0, 5000) if k < .5
                        else r.choice(words) + "-" + str(r.randint(1, 99)) if k < .8
                        else [r.choice(words) for _ in range(r.randint(1, 4))])
            return {r.choice(words) + str(i): node(d - 1) for i in range(fan)}
        return {"service": "checkout", "version": "2026.08", "env": node(depth)}

    def numbers_obj(n=20000, seed=5):
        r = random.Random(seed); t = 1_723_900_000.0; out = []
        for _ in range(n):
            t += r.random() * 2
            out.append({"t": round(t, 3), "v": round(r.gauss(50, 12), 4), "q": r.randint(0, 3), "ok": r.random() > .02})
        return {"series": "sensor-7", "points": out}

    _logs = [json.loads(l) for l in json_logs().splitlines()]
    SAMPLES = {
        "logs":    ("API logs — 512 KB, the JSON from survey 1.050", _logs),
        "nested":  ("Nested config — 98 KB", nested_obj()),
        "numbers": ("Numeric time series — 976 KB", numbers_obj()),
        "small":   ("One record — 366 B", _logs[0]),
    }
    return (SAMPLES,)


@app.cell(hide_code=True)
def _(SAMPLES, mo):
    sample = mo.ui.radio(options={v[0]: k for k, v in SAMPLES.items()} | {"Your own JSON (below)": "own"},
                         value=list(SAMPLES.values())[0][0], label="What to measure")
    own_text = mo.ui.text_area(placeholder='Paste JSON here — an API response, a config, a log line — then click outside the box. It never leaves this tab.',
                               value="", rows=6, full_width=True, debounce=True)
    own_file = mo.ui.file(kind="button", label="…or choose a .json file (first 1 MB)")
    mo.vstack([sample, own_text, own_file])
    return own_file, own_text, sample


@app.cell(hide_code=True)
def _(SAMPLES, json, mo, own_file, own_text, sample):
    # resolve the selection into (label, object, canonical text bytes)
    _sel = sample.value
    _err = None
    if _sel == "own":
        _raw = None
        if own_file.value:
            _raw = own_file.value[0].contents[: 1024 * 1024].decode("utf-8", "replace")
            _label = own_file.name(0) or "your file"
        elif own_text.value.strip():
            _raw = own_text.value; _label = "your paste"
        if _raw is None:
            obj, label = SAMPLES["logs"][1], SAMPLES["logs"][0]
            _err = "Nothing pasted yet — showing the API logs until you do."
        else:
            try:
                obj = json.loads(_raw); label = _label
            except Exception as e:
                obj, label = SAMPLES["logs"][1], SAMPLES["logs"][0]
                _err = f"That is not JSON this page can read ({str(e)[:80]}) — showing the API logs instead."
    else:
        label, obj = SAMPLES[_sel]
    text = json.dumps(obj, separators=(",", ":"))
    data = text.encode()
    mo.md(f"*{_err}*" if _err else f"Measuring **{label}** — {len(data):,} bytes as compact JSON.")
    return data, label, obj, text


@app.cell(hide_code=True)
def _(time):
    def best(fn, arg, budget_s=0.12, min_reps=3):
        """Best-of timing under a wall-clock budget. Browser clocks clamp (100 µs in Chromium
        without isolation), so calls are timed in batches calibrated to take at least 5 ms —
        fifty clamp ticks — before a single reading is trusted."""
        t0 = time.perf_counter(); fn(arg); first = time.perf_counter() - t0
        if first > budget_s: return first, 1
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
    return (best,)


@app.cell(hide_code=True)
def _(Any, msgspec, re):
    # ── infer a msgspec.Struct from the reader's own JSON ──────────────────
    # "Why parse into dicts at all" only lands if it works on THEIR payload. A
    # schema is inferred from the first object: primitives by type, nested dicts
    # become nested Structs, lists take the type of their first element. Anything
    # irregular falls back to Any. Good enough to measure; the reader writes the real one.
    _counter = [0]
    def _ident(k):
        s = re.sub(r"\W", "_", k)
        return ("f_" + s) if (not s or s[0].isdigit() or s in {"from", "class", "import", "def", "return", "None", "True", "False"}) else s
    def infer_type(v, name="Item"):
        if name == "Payload": _counter[0] = 0
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
            fields = []
            renamed = {}
            for k, val in v.items():
                ident = _ident(k)
                if ident != k: renamed[ident] = k
                fields.append((ident, infer_type(val, name + "_" + ident.capitalize()), msgspec.UNSET if False else msgspec.NODEFAULT))
            try:
                return msgspec.defstruct(f"{name}{_counter[0]}", [(f, t) for f, t, _ in fields], rename=renamed or None)
            except Exception:
                return dict[str, Any]
        return Any
    def struct_source(tp, depth=0):
        """Render the inferred Struct as code the reader can take away."""
        out = []
        def walk(t):
            if isinstance(t, type) and issubclass(t, msgspec.Struct):
                for f in msgspec.structs.fields(t):
                    walk(f.type)
                lines = [f"class {t.__name__}(msgspec.Struct):"]
                for f in msgspec.structs.fields(t):
                    lines.append(f"    {f.encode_name if f.encode_name == f.name else f.name}: {tname(f.type)}")
                src = "\n".join(lines)
                if src not in out: out.append(src)
            elif hasattr(t, "__args__"):
                for a in t.__args__: walk(a)
        def tname(t):
            if isinstance(t, type) and issubclass(t, msgspec.Struct): return t.__name__
            if t is Any: return "Any"
            if hasattr(t, "__origin__"): return f"{t.__origin__.__name__}[{', '.join(tname(a) for a in t.__args__)}]"
            return getattr(t, "__name__", str(t))
        walk(tp)
        return "\n\n".join(out)
    return infer_type, struct_source


@app.cell(hide_code=True)
def _(best, data, infer_type, json, msgspec, obj, orjson, simplejson, text, ujson):
    # ── the measurement ────────────────────────────────────────────────────
    CODECS = {
        "json (stdlib)": (json.dumps, json.loads, text),
        "orjson":        (orjson.dumps, orjson.loads, data),
        "msgspec":       (msgspec.json.encode, msgspec.json.decode, data),
        "ujson":         (ujson.dumps, ujson.loads, text),
        "simplejson":    (simplejson.dumps, simplejson.loads, text),
    }
    typed_ok, typed_err, Schema = True, None, None
    try:
        Schema = infer_type(obj, "Payload")
        _dec = msgspec.json.Decoder(Schema); _enc = msgspec.json.Encoder()
        _typed_obj = _dec.decode(data)
        CODECS["msgspec typed (inferred Struct)"] = (_enc.encode, _dec.decode, data)
        _typed_src = _typed_obj
    except Exception as e:
        typed_ok, typed_err = False, str(e)[:140]
    rows = []
    for _lib, (_d, _l, _inp) in CODECS.items():
        _src = _typed_src if "typed" in _lib else obj
        _td, _ = best(_d, _src); _tl, _ = best(_l, _inp)
        rows.append({"lib": _lib, "dumps_ms": _td * 1000, "loads_ms": _tl * 1000,
                     "dumps_MBs": len(data) / _td / 1e6, "loads_MBs": len(data) / _tl / 1e6})
    _base = rows[0]
    for _r in rows:
        _r["dumps_x"] = _base["dumps_ms"] / _r["dumps_ms"]; _r["loads_x"] = _base["loads_ms"] / _r["loads_ms"]
    return Schema, rows, typed_err, typed_ok


@app.cell(hide_code=True)
def _(mo, register, rows):
    # ── bars ───────────────────────────────────────────────────────────────
    def _fmt_ms(ms): return f"{ms*1000:.0f} µs" if ms < 1 else f"{ms:.2f} ms" if ms < 10 else f"{ms:.0f} ms"
    def _bar(label, val, mx, display, color):
        w = max(1, min(70, val / mx * 70))
        return (f'<div style="display:flex;align-items:center;gap:10px;margin:5px 0;font-size:.86rem">'
                f'<span style="width:210px;flex:none;opacity:.75">{label}</span>'
                f'<span style="height:20px;width:{w:.1f}%;background:{color};border-radius:3px;min-width:2px"></span>'
                f'<span style="font-variant-numeric:tabular-nums;white-space:nowrap">{display}</span></div>')
    _mx = max(max(r["dumps_x"], r["loads_x"]) for r in rows)
    html = '<h3 style="margin:14px 0 4px">dumps — object → JSON</h3>'
    for _r in rows:
        html += _bar(_r["lib"], _r["dumps_x"], _mx, f'{_r["dumps_x"]:.1f}× stdlib · {_fmt_ms(_r["dumps_ms"])}' + (f' · {_r["dumps_MBs"]:.0f} MB/s' if register.value else ""), "#5eead4")
    html += '<h3 style="margin:18px 0 4px">loads — JSON → object</h3>'
    for _r in rows:
        html += _bar(_r["lib"], _r["loads_x"], _mx, f'{_r["loads_x"]:.1f}× stdlib · {_fmt_ms(_r["loads_ms"])}' + (f' · {_r["loads_MBs"]:.0f} MB/s' if register.value else ""), "#4ade80")
    _o = next(r for r in rows if r["lib"] == "orjson")
    _t = next((r for r in rows if "typed" in r["lib"]), None)
    note = (f"**On this payload orjson writes {_o['dumps_x']:.1f}× faster than the standard library and reads {_o['loads_x']:.1f}× faster.** "
            "The famous multiple is the first number; most people quote it for the second."
            + (f" The fastest reader here is msgspec with an inferred schema — {_t['loads_x']:.1f}× stdlib, {_t['loads_x']/_o['loads_x']:.2f}× orjson — and it validated the shape on the way in." if _t else ""))
    mo.vstack([mo.Html(html), mo.md(note)])
    return


@app.cell(hide_code=True)
def _(Schema, mo, msgspec, register, struct_source, typed_err, typed_ok):
    # ── the schema it inferred, and what validation costs ──────────────────
    if typed_ok and Schema is not None:
        _src = struct_source(Schema)
        body = mo.md(f"""### The schema this page inferred from your JSON

Typed decoding needs a shape. This page guessed one from the first object — primitives by
type, nested objects as nested Structs, lists by their first element. It is a starting
point, not the schema you would ship; the point is that even a guessed one is faster than
no schema, and it rejects anything that does not fit.

```python
import msgspec

{_src}

decoder = msgspec.json.Decoder({Schema.__name__ if hasattr(Schema, "__name__") else "Payload"})
payload = decoder.decode(raw_bytes)   # validated on the way in
```
""")
    else:
        body = mo.md(f"*Could not infer a schema for this payload ({typed_err}). Mixed-type lists and top-level scalars need a hand-written Struct — which is the ordinary case for real APIs.*")
    body
    return


@app.cell(hide_code=True)
def _(mo, register, rows, sys):
    import orjson as _o, msgspec as _m, ujson as _u, simplejson as _s
    _v = sys.version.split()[0]
    mo.Html(f"""<div style="border-left:3px solid #f59e42;padding-left:14px;line-height:1.6">
<p style="font-size:.78rem;text-transform:uppercase;letter-spacing:.09em;color:#f59e42;font-weight:600;margin:0 0 8px">From research, not measured in this tab</p>
<p style="margin:0 0 10px"><strong>python-rapidjson</strong> is not in Pyodide. Native, one machine (CPython 3.14.7, aarch64): slower than the
standard library on every sample — loads at 0.8× stdlib on the logs, 0.83× on the nested config, 0.83× on the numbers — confirming the
survey's caution and sharpening it from "sometimes" to "every time measured". 4.7M downloads a month.</p>
<p style="margin:0 0 10px"><strong>Memory.</strong> Resident memory after <code>loads</code> of a 19 MB numeric document: stdlib 106 MB, orjson 104 MB,
msgspec 100 MB — the dicts are the dicts, whichever library built them. msgspec <strong>Structs</strong>: 47 MB (2.2× less), 40 MB with
<code>gc=False</code>. pydantic models: 436 MB. orjson adds a transient ~75 MB peak while parsing. The survey's "6–9× less memory" is
2.2–2.6× resident, typed against untyped.</p>
<p style="margin:0"><strong>Across interpreters</strong> (3.11, 3.12, 3.14, same machine): orjson reads 1.6–2.1× stdlib and writes 5–13×; ujson
1.1–1.7× reading, 1.2–2.7× writing. None of it is a Python-3.14 effect.</p>
</div>""" + (f"<p style='font-size:.85rem;opacity:.75;margin-top:10px'>In this tab: Python {_v}, orjson {_o.__version__}, msgspec {_m.__version__}, ujson {_u.__version__}, simplejson {_s.__version__}. Throughput here is WebAssembly throughput — roughly half of native, same shape.</p>" if register.value else ""))
    return


@app.cell(hide_code=True)
def _(label, mo, rows, sys):
    _o = next(r for r in rows if r["lib"] == "orjson"); _t = next((r for r in rows if "typed" in r["lib"]), None)
    brief = f"""I am choosing a JSON library in Python and have just measured the trade-offs myself,
in the browser, on my own data.

My data
  sample   : {label}
  Python   : {sys.version.split()[0]} (Pyodide / WebAssembly — throughput about half of native, same shape)

What I measured on it (real libraries, in-tab, multiples of the standard library)
""" + "\n".join(f"  {r['lib']:32}: dumps {r['dumps_x']:.1f}x, loads {r['loads_x']:.1f}x" for r in rows) + f"""

What the survey established
  The widely quoted "orjson is 6x faster" is a serialising (dumps) number; parsing is ~2x.
  msgspec with a schema is the fastest parser and validates on the way in; Structs hold
  ~2.2x less memory than dicts. pydantic models are slower than the stdlib and hold 4x more.
  ujson is 1.1-1.7x the stdlib today. python-rapidjson is slower than the stdlib.

Help me build this
  Recommend a library for my workload and write the encode/decode code. If my data has a
  stable shape, write the msgspec Struct for it (the page inferred a rough one). Tell me
  whether serialising or parsing dominates my case — the answer depends on it.

Reference: https://research.modelcitizendeveloper.com/survey/1-056/"""
    import html as _html
    # marimo strips inline handlers and <script> from mo.Html; a sandboxed iframe runs them
    # and the clipboard write works from inside it (probed 2026-08-19). So the envelope lives here.
    copy_btn = mo.iframe(f'''<!doctype html><html><head><meta charset="utf-8"><style>
      body{{margin:0;background:#0b1220;color:#cbd5e1;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}}
      button{{font:inherit;cursor:pointer;background:#5eead4;color:#042f2e;border:1px solid #5eead4;border-radius:6px;padding:8px 16px;font-weight:700}}
      pre{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.82rem;white-space:pre-wrap;background:#0f1a2e;border:1px solid #1e293b;border-radius:6px;padding:12px;margin-top:12px;max-height:300px;overflow:auto}}
      .note{{font-size:.9rem;color:#94a3b8;margin-left:10px}}</style></head><body>
      <button id="c" onclick="navigator.clipboard.writeText(document.getElementById('b').textContent).then(()=>{{document.getElementById('s').textContent='Copied — paste it into any AI.'}}).catch(()=>{{document.getElementById('s').textContent='Select the text below and copy it.'}})">Copy the brief</button><span id="s" class="note"></span>
      <pre id="b">{_html.escape(brief).replace(chr(10), "<br>")}</pre></body></html>''', height="420px")
    mo.vstack([mo.md("## Start your build\nTake what you just measured and hand it to whichever AI you use — your sample, your numbers, a brief for what to do next. No vendor link, no API key."), copy_btn])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
<div style="margin-top:40px;padding-top:16px;border-top:1px solid #64748b55;font-size:.88rem;opacity:.8">
<strong>JSONic rituals</strong> is a floor model for <a href="/survey/1-056/">Survey of Software 1.056 — JSON Libraries</a>.
Libraries run under Pyodide (CPython compiled to WebAssembly) in this tab; nothing is sent anywhere. Measurements are from
your machine except where marked orange. This page is a marimo notebook — the code is the method, and it is one click away.<br>
Made by Ivan Schneider · <a href="https://modelcitizendeveloper.com/">Model Citizen Developer</a>
</div>""")
    return


if __name__ == "__main__":
    app.run()
