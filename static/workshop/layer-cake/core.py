"""core.py — the measurement behind layer cake (floor model for Survey of Software 1.241).

One copy, two readers: the page fetches it into Pyodide, and the survey's native bench
(01-discovery/S2-comprehensive/bench/) measures the same thing the same way. Timing comes
from /workshop/_lib/workshop.py. Every function the page calls returns JSON.

FastAPI is Starlette plus a layer. This measures the layer, and then measures the validation
inside it, which turns out to be a small fraction of the cost.

WHY THERE IS NO EVENT LOOP HERE. Driving an ASGI app normally means loop.run_until_complete,
and a browser tab has no loop you are allowed to run: Pyodide's loop is the page's. But a
handler that returns a dict never suspends on real I/O, so its coroutine runs to completion
on the FIRST send(None) — measured, zero suspensions, for both frameworks. So the request is
stepped by hand and stays synchronous. If a handler ever awaited real I/O this would raise
rather than silently mislead, which is the behavior we want.
"""
import json
from workshop import best as _best

PATH = "/items/42"
BODY = {"id": 42, "name": "item"}


# ── the two applications: same route, same response, same work ────────────────
def build_starlette():
    from starlette.applications import Starlette
    from starlette.routing import Route
    from starlette.responses import JSONResponse

    async def get_item(request):
        return JSONResponse({"id": request.path_params["item_id"], "name": "item"})
    return Starlette(routes=[Route("/items/{item_id:int}", get_item)])


def build_fastapi():
    from fastapi import FastAPI
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    @app.get("/items/{item_id}")
    async def get_item(item_id: int):
        return {"id": item_id, "name": "item"}
    return app


# ── driving one request, without a loop ───────────────────────────────────────
def _scope(path=PATH):
    return {
        "type": "http", "asgi": {"version": "3.0", "spec_version": "2.1"},
        "http_version": "1.1", "method": "GET", "scheme": "http",
        "path": path, "raw_path": path.encode(), "query_string": b"",
        "root_path": "", "headers": [(b"host", b"testserver")],
        "client": ("127.0.0.1", 1), "server": ("testserver", 80),
    }


def one_request(app):
    """Drive one request to completion and return the body bytes. No event loop."""
    chunks, status, sent = [], {}, [False]

    async def receive():
        if not sent[0]:
            sent[0] = True
            return {"type": "http.request", "body": b"", "more_body": False}
        return {"type": "http.disconnect"}

    async def send(m):
        if m["type"] == "http.response.start":
            status["c"] = m["status"]
        elif m["type"] == "http.response.body":
            chunks.append(m.get("body", b""))

    coro = app(_scope(), receive, send)
    steps = 0
    try:
        while True:
            coro.send(None)
            steps += 1
            if steps > 1000:
                raise RuntimeError("handler suspended: this needs a real event loop")
    except StopIteration:
        pass
    return status.get("c"), b"".join(chunks)


# ── panel 1: the race ─────────────────────────────────────────────────────────
_APPS = {}


def _app(name):
    if name not in _APPS:
        _APPS[name] = build_starlette() if name == "starlette" else build_fastapi()
        one_request(_APPS[name])                      # warm: routing tables, imports
    return _APPS[name]


def race():
    """Per-request cost of each framework, on this machine, right now."""
    out = {}
    for name in ("starlette", "fastapi"):
        app = _app(name)
        status, body = one_request(app)
        s, reps = _best(one_request, app)
        out[name] = {"us": s * 1e6, "reps": reps, "status": status,
                     "bytes": len(body), "body": body.decode()}
    st, fa = out["starlette"]["us"], out["fastapi"]["us"]
    out["_summary"] = {"multiple": fa / st if st else None,
                       "layer_us": fa - st}
    return json.dumps(out)


# ── panel 2: what the layer is NOT ────────────────────────────────────────────
_SAMPLE = {"id": 42, "name": "item", "tags": ["a", "b", "c"],
           "price": 9.99, "active": True}


def _pydantic_model():
    import pydantic
    from typing import List

    class Item(pydantic.BaseModel):
        id: int
        name: str
        tags: List[str]
        price: float
        active: bool
    return Item


def validation(payload_json=None):
    """Decode-and-validate against decode-only, on the same bytes.

    Parse-then-check is not the sequence that runs: pydantic v2 parses in compiled code in
    ONE pass and never builds the intermediate dict that the standard library spends its
    time on.
    """
    raw = (payload_json or json.dumps(_SAMPLE)).encode()
    try:
        parsed = json.loads(raw)
    except Exception as e:
        return json.dumps({"error": f"that is not JSON: {e}"})
    if not isinstance(parsed, dict):
        return json.dumps({"error": "give me a JSON object (curly braces at the top)."})

    import pydantic
    from typing import Any, Dict
    fields = {k: (type(v) if not isinstance(v, (list, dict)) else Any, ...)
              for k, v in parsed.items()}
    Model = pydantic.create_model("Pasted", **fields)

    rows = {}
    s, reps = _best(lambda b: Model.model_validate_json(b), raw)
    rows["pydantic (decodes AND validates)"] = {"us": s * 1e6, "reps": reps, "validates": True}
    s, reps = _best(json.loads, raw)
    rows["json.loads (decodes only)"] = {"us": s * 1e6, "reps": reps, "validates": False}

    p = rows["pydantic (decodes AND validates)"]["us"]
    j = rows["json.loads (decodes only)"]["us"]
    return json.dumps({
        "rows": rows, "bytes": len(raw), "fields": len(fields),
        "pydantic_faster": p < j,
        "ratio": j / p if p else None,
    })


def caught(payload_json=None):
    """What validation actually buys: give the model a wrong type and watch it refuse."""
    raw = payload_json or json.dumps(_SAMPLE)
    parsed = json.loads(raw)
    Item = _pydantic_model()
    broken = dict(_SAMPLE, price="not a number", id="forty-two")
    try:
        Item.model_validate(broken)
        return json.dumps({"caught": False})
    except Exception as e:
        errs = getattr(e, "errors", lambda: [])()
        return json.dumps({
            "caught": True, "n": len(errs),
            "detail": [{"field": ".".join(str(x) for x in d.get("loc", ())),
                        "problem": d.get("msg", "")} for d in errs][:4],
            "sent": {"id": "forty-two", "price": "not a number"},
        })


def versions():
    import sys
    import fastapi, starlette, pydantic
    return json.dumps({
        "python": sys.version.split()[0],
        "fastapi": fastapi.__version__,
        "starlette": starlette.__version__,
        "pydantic": pydantic.VERSION,
    })
