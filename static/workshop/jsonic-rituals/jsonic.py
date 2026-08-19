# /// script
# requires-python = ">=3.12"
# dependencies = ["marimo", "orjson", "msgspec", "ujson", "simplejson", "pydantic"]
# ///
"""JSONic rituals — the lab for Survey of Software 1.056 (JSON Libraries).

The measurement lives in core.py (next to this file) and /workshop/_lib/workshop.py; this
notebook imports them, exactly as the floor-model page fetches them. Run it locally
(`uvx marimo edit jsonic.py`, or `uvx marimo edit <url to this file>`) or open it at
marimo.app/?src=<url>. One copy of the code; two front ends.
"""
import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", app_title="JSONic rituals — a floor model for Survey of Software 1.056")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import json, sys, os
    # One copy of the measurement: core.py next to this notebook, workshop.py in ../_lib.
    # Running from the site (marimo.app/?src=) there is no filesystem — fetch both first.
    _here = None
    try:
        _here = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        pass
    if _here and os.path.exists(os.path.join(_here, "core.py")):
        sys.path[:0] = [_here, os.path.join(_here, "..", "_lib")]
    else:
        from pyodide.http import open_url
        _base = "https://research.modelcitizendeveloper.com/workshop/"
        for _name, _url in [("workshop", _base + "_lib/workshop.py"), ("core", _base + "jsonic-rituals/core.py")]:
            open(f"/home/pyodide/{_name}.py", "w").write(open_url(_url).read())
        sys.path.insert(0, "/home/pyodide")
    import core
    return core, json, mo, sys


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
def _(core, mo):
    LABELS = {"logs": "API logs — 512 KB, the JSON from survey 1.050", "nested": "Nested config — 98 KB",
              "numbers": "Numeric time series — 976 KB", "small": "One record — 366 B"}
    SAMPLES = {k: (LABELS[k], core.SAMPLES[k]) for k in LABELS}
    sample = mo.ui.radio(options={v[0]: k for k, v in SAMPLES.items()} | {"Your own JSON (below)": "own"},
                         value=list(SAMPLES.values())[0][0], label="What to measure")
    own_text = mo.ui.text_area(placeholder='Paste JSON here — an API response, a config, a log line — then click outside the box. It never leaves this tab.',
                               value="", rows=6, full_width=True, debounce=True)
    own_file = mo.ui.file(kind="button", label="…or choose a .json file (first 1 MB)")
    mo.vstack([sample, own_text, own_file])
    return SAMPLES, own_file, own_text, sample


@app.cell(hide_code=True)
def _(SAMPLES, core, json, mo, own_file, own_text, sample):
    # resolve the selection into a sample key that core.measure understands
    _sel = sample.value
    _err = None
    key, label = "logs", SAMPLES["logs"][0]
    if _sel == "own":
        _raw = None
        if own_file.value:
            _raw = own_file.value[0].contents[: 1024 * 1024].decode("utf-8", "replace"); _label = own_file.name(0) or "your file"
        elif own_text.value.strip():
            _raw = own_text.value; _label = "your paste"
        if _raw is None:
            _err = "Nothing pasted yet — showing the API logs until you do."
        else:
            _r = json.loads(core.set_own(_raw))
            if _r["ok"]: key, label = "own", _label
            else: _err = f"That is not JSON this page can read ({_r['err'][:80]}) — showing the API logs instead."
    else:
        key, label = _sel, SAMPLES[_sel][0]
    mo.md(f"*{_err}*" if _err else f"Measuring **{label}**.")
    return key, label


@app.cell(hide_code=True)
def _(core, json, key):
    # ── the measurement: core.measure, the same function the page calls ────
    _m = json.loads(core.measure(key, 120))
    rows = _m["rows"]; nbytes = _m["bytes"]
    Schema_src, schema_name, typed_err = _m["schema"], _m["schema_name"], _m["schema_err"]
    typed_ok = Schema_src is not None
    validation = _m["validation"]
    return Schema_src, nbytes, rows, schema_name, typed_err, typed_ok, validation


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
def _(Schema_src, mo, schema_name, typed_err, typed_ok, validation):
    # ── the schema core inferred, and what validation costs ────────────────
    if typed_ok:
        _v = ("" if not validation else
              ("\n\n*Validation, shown:* core changed one number in the JSON to a string and decoded again — "
               + ("it decoded anyway; the first numeric field was inside a list or a string, so the guess did not cover it."
                  if validation == "decoded anyway" else f"msgspec refused: `{validation}`.")))
        body = mo.md(f"""### The schema core.py inferred from your JSON

Typed decoding needs a shape. `core.infer_type` guessed one from the first object — primitives by
type, nested objects as nested Structs, lists by their first element. A starting point, not the
schema you would ship; the point is that even a guessed one is faster than no schema, and it
rejects anything that does not fit.

```python
import msgspec

{Schema_src}

decoder = msgspec.json.Decoder({schema_name})
payload = decoder.decode(raw_bytes)   # validated on the way in
```{_v}
""")
    else:
        body = mo.md(f"*Could not infer a schema for this payload ({typed_err}). Mixed-type lists and top-level scalars need a hand-written Struct — which is the ordinary case for real APIs.*")
    body
    return


@app.cell(hide_code=True)
def _(core, json, mo, register):
    _ver = json.loads(core.versions()); _v = _ver["python"]
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
</div>""" + (f"<p style='font-size:.85rem;opacity:.75;margin-top:10px'>In this tab: Python {_v}, orjson {_ver["orjson"]}, msgspec {_ver["msgspec"]}, ujson {_ver["ujson"]}, simplejson {_ver["simplejson"]}. Throughput here is WebAssembly throughput — roughly half of native, same shape.</p>" if register.value else ""))
    return


@app.cell(hide_code=True)
def _(core, json, label, mo, rows):
    _pyv = json.loads(core.versions())["python"]
    _o = next(r for r in rows if r["lib"] == "orjson"); _t = next((r for r in rows if "typed" in r["lib"]), None)
    brief = f"""I am choosing a JSON library in Python and have just measured the trade-offs myself,
in the browser, on my own data.

My data
  sample   : {label}
  Python   : {_pyv} (Pyodide / WebAssembly — throughput about half of native, same shape)

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
