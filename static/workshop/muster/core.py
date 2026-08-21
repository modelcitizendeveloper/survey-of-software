"""core.py — the Python half of Muster, the floor model for Survey of Software 1.200.

One copy, three readers: the page fetches it into Pyodide, the marimo notebook imports
it, the native bench imports it. Nothing here is pasted into index.html.

The subject is a photo-ingestion pipeline: read a folder of photos, pull the GPS and the
capture time out of the EXIF, make thumbnails, shrink a copy for a vision model, and get
back a tag and a caption for each one — then plot the lot on a map. Three of its four
three of those run locally and are working code from a real implementation, vendored here
with their docstrings intact, because the point of this page is that the work is real. The
fourth — the vision call itself — is the one that costs money, and it is the only thing
standing in: this file projects its price from published rates and never makes a network
call.

Provenance, all read on 2026-08-21:
  * extract_gps / extract_datetime / encode_for_vision / make_thumbnail
    — the pipeline's own image layer. Adapted only in how bytes arrive (Pyodide has no
      camera roll): the Path argument became bytes. The EXIF walk, the DMS->decimal
      conversion and the 1568 px default are unchanged.
  * count_image_tokens / resized_size
    — Anthropic's own reference implementation, docs.claude.com "Coordinates and
      bounding boxes" -> How Claude resizes and pads images. Copied, not reimplemented:
      the docs warn that scaling to the edge length by hand gets it wrong.
  * PRICING
    — the pipeline's published cost table, and the vendors' own rates.
      Prices move; this file says so wherever it prints one.
"""
from __future__ import annotations

import io
import json
import math
import time

from PIL import Image, ImageOps
from PIL.ExifTags import IFD

__version__ = "2026-08-21"

# HEIC is what a phone actually hands you. The upstream pipeline accepts a .heic
# extension but ships no HEIF plugin, so there an iPhone photo reads as None; Pyodide
# has the wheel, so the page registers it when present and says which happened.
try:
    import pillow_heif

    pillow_heif.register_heif_opener()
    HEIF = True
except Exception:  # pragma: no cover - absent in a plain CPython bench
    HEIF = False


# ── the three local jobs: the pipeline's code, on the reader's own files ────────

def _as_bytes(data):
    """Coerce whatever the caller had into real bytes.

    The one seam where the browser leaks in. Pyodide hands a JS Uint8Array to Python
    as a JsProxy, which supports no buffer protocol, so `io.BytesIO(data)` raises
    `TypeError: a bytes-like object is required`. Converting here rather than on the
    JS side keeps every function below callable unchanged from a native bench.
    """
    if isinstance(data, (bytes, bytearray, memoryview)):
        return bytes(data)
    to_py = getattr(data, "to_py", None)       # pyodide.ffi.JsProxy
    if to_py is not None:
        return bytes(to_py())
    return bytes(data)


def _dms_to_decimal(dms, ref: str) -> float:
    """Convert an EXIF (degrees, minutes, seconds) rational triple to decimal
    degrees, negating for S/W. This is the WGS84 hand-roll the survey describes."""
    degrees, minutes, seconds = (float(v) for v in dms)
    decimal = degrees + minutes / 60.0 + seconds / 3600.0
    if ref and ref.upper() in ("S", "W"):
        decimal = -decimal
    return decimal


def extract_gps(data: bytes):
    """Return (lat, lon) in WGS84 decimal degrees, or None if the photo has no
    usable GPS EXIF."""
    try:
        with Image.open(io.BytesIO(_as_bytes(data))) as img:
            exif = img.getexif()
            gps = exif.get_ifd(IFD.GPSInfo)
    except Exception:
        return None

    if not gps:
        return None

    # GPS IFD tag numbers: 1=LatRef 2=Lat 3=LonRef 4=Lon
    lat_ref, lat = gps.get(1), gps.get(2)
    lon_ref, lon = gps.get(3), gps.get(4)
    if not (lat and lon and lat_ref and lon_ref):
        return None

    try:
        return _dms_to_decimal(lat, lat_ref), _dms_to_decimal(lon, lon_ref)
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def _exif_dt_to_iso(raw):
    """Reshape an EXIF datetime string ('YYYY:MM:DD HH:MM:SS') into ISO-8601.
    EXIF carries no timezone, so neither does the output."""
    if not isinstance(raw, str):
        return None
    try:
        date, clock = raw.strip().split(" ", 1)
        y, mo, d = date.split(":")
    except ValueError:
        return None
    if y in ("", "0000"):  # cameras write '0000:00:00 00:00:00' when unset
        return None
    return f"{y}-{mo}-{d}T{clock}"


def extract_datetime(data: bytes):
    """Return the capture timestamp as an ISO-8601 string, or None if absent."""
    try:
        with Image.open(io.BytesIO(_as_bytes(data))) as img:
            exif = img.getexif()
            raw = exif.get_ifd(IFD.Exif).get(0x9003) or exif.get(0x0132)
    except Exception:
        return None
    return _exif_dt_to_iso(raw)


def encode_for_vision(data: bytes, *, max_edge: int = 1568):
    """Return JPEG bytes (+ size) downscaled so the long edge is <= max_edge.

    The original docstring: "Claude downsizes large images server-side anyway; doing it
    here keeps token cost predictable and normalizes orientation/format." Panel 1
    measures whether that is true, and on which models.
    """
    with Image.open(io.BytesIO(_as_bytes(data))) as im:
        im = ImageOps.exif_transpose(im)  # honor camera orientation
        im = im.convert("RGB")
        if max(im.size) > max_edge:
            im.thumbnail((max_edge, max_edge))
        size = im.size
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=85)
    return buf.getvalue(), size


def make_thumbnail(data: bytes, *, size=(400, 400)):
    """Return JPEG thumbnail bytes. Upstream these go to disk; the page shows them."""
    with Image.open(io.BytesIO(_as_bytes(data))) as im:
        im = ImageOps.exif_transpose(im)
        im = im.convert("RGB")
        im.thumbnail(size)
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=85)
    return buf.getvalue()


# ── the vision call: what it would cost. No network, ever. ─────────────────────

def count_image_tokens(width: int, height: int) -> int:
    """Visual tokens consumed by an image: one token per 28x28 pixel patch."""
    return math.ceil(width / 28) * math.ceil(height / 28)


def resized_size(width: int, height: int, max_edge: int = 1568, max_tokens: int = 1568):
    """The size Claude resizes an image to before padding.

    Defaults are for the standard resolution tier. For high-resolution-tier models,
    use max_edge=2576 and max_tokens=4784. Returns (width, height).
    """

    def fits(w: int, h: int) -> bool:
        return (
            math.ceil(w / 28) * 28 <= max_edge
            and math.ceil(h / 28) * 28 <= max_edge
            and count_image_tokens(w, h) <= max_tokens
        )

    if fits(width, height):
        return (width, height)
    if height > width:
        resized_h, resized_w = resized_size(height, width, max_edge, max_tokens)
        return (resized_w, resized_h)

    aspect_ratio = width / height
    lo, hi = 1, width  # lo always fits; hi never fits
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if fits(mid, max(round(mid / aspect_ratio), 1)):
            lo = mid
        else:
            hi = mid
    return (lo, max(round(lo / aspect_ratio), 1))


# Resolution tiers, docs.claude.com "Resolution and token cost", read 2026-08-21.
TIERS = {
    "high": {"max_edge": 2576, "max_tokens": 4784, "label": "high-resolution (Claude 4.7 and later)"},
    "standard": {"max_edge": 1568, "max_tokens": 1568, "label": "standard (every other model)"},
}

# The pipeline's own cost table. (input $/Mtok, output $/Mtok, tier).
# The Gemini rates are Google's and are carried across unverified here; the Anthropic
# rows were re-checked against the published price list on 2026-08-21.
PRICING = {
    "claude-opus-4-8":   (5.00, 25.00, "high"),
    "claude-sonnet-4-6": (3.00, 15.00, "standard"),
    "claude-haiku-4-5":  (1.00, 5.00, "standard"),
    "gemini-3-flash":      (0.50, 3.00, "standard"),
    "gemini-3.1-flash-lite": (0.25, 1.50, "standard"),
}
PRICE_NOTE = ("estimate at published rates (Anthropic rows re-checked 2026-08-21); "
              "verify before invoicing.")
OUTPUT_TOKENS = 120   # the pipeline's own per-photo assumption for one analysis object
PROMPT_TOKENS = 210   # the classification rubric this page builds, counted as text


def vision_cost(width: int, height: int, model: str):
    """What the vision call costs for a photo of these dimensions — projected, never made.

    Returns the tier's resize, the visual-token count, and the dollar figure. The
    dimensions are measured from the reader's file; everything else is published.
    """
    in_rate, out_rate, tier = PRICING[model]
    t = TIERS[tier]
    rw, rh = resized_size(width, height, t["max_edge"], t["max_tokens"])
    visual = count_image_tokens(rw, rh)
    inp = visual + PROMPT_TOKENS
    return {
        "model": model, "tier": tier, "resized": [rw, rh], "visual_tokens": visual,
        "input_tokens": inp, "output_tokens": OUTPUT_TOKENS,
        "usd": inp / 1e6 * in_rate + OUTPUT_TOKENS / 1e6 * out_rate,
    }


# ── all three local jobs for one photo, measured ────────────────────────────────

def process_photo(name: str, data: bytes) -> str:
    """Run the three local jobs on one photo and price the vision call both ways.

    Every field here except the prices is measured from the bytes handed in.
    """
    data = _as_bytes(data)
    t0 = time.perf_counter()
    try:
        with Image.open(io.BytesIO(data)) as probe:
            probe = ImageOps.exif_transpose(probe)
            w, h = probe.size
            fmt = probe.format or "?"
    except Exception as exc:
        return json.dumps({"name": name, "ok": False, "error": f"{type(exc).__name__}: {exc}"})

    gps = extract_gps(data)
    t1 = time.perf_counter()
    thumb = make_thumbnail(data)
    t2 = time.perf_counter()
    enc, enc_size = encode_for_vision(data)
    t3 = time.perf_counter()

    return json.dumps({
        "name": name, "ok": True, "format": fmt,
        "orig": [w, h], "orig_bytes": len(data),
        "encoded": list(enc_size), "encoded_bytes": len(enc),
        "thumb_bytes": len(thumb),
        "gps": list(gps) if gps else None,
        "taken": extract_datetime(data),
        "ms": {"gps": (t1 - t0) * 1e3, "thumb": (t2 - t1) * 1e3, "encode": (t3 - t2) * 1e3},
        # the vision call, priced both ways: as shot, and after encoding did its job
        "cost": {
            m: {"raw": vision_cost(w, h, m), "encoded": vision_cost(*enc_size, m)}
            for m in PRICING
        },
    })


def build_feature_collection(records) -> str:
    """The pipeline's final step: GeoJSON, WGS84 by RFC 7946, no reprojection anywhere.

    `records` is a list of dicts carrying at least name/gps, plus whatever the vision
    call returned for that photo (absent until the reader brings an analysis back).
    """
    feats = []
    for r in records:
        gps = r.get("gps")
        if not gps:
            continue
        props = {"photo": r.get("name"), "taken": r.get("taken")}
        for k in ("kind", "category", "severity", "summary", "area_type", "disposition"):
            if r.get(k) is not None:
                props[k] = r[k]
        feats.append({"type": "Feature",
                      "geometry": {"type": "Point", "coordinates": [gps[1], gps[0]]},
                      "properties": props})
    return json.dumps({"type": "FeatureCollection", "features": feats}, indent=2)


# ── the return leg: one envelope, one parser, no model call ─────────────────────
# speakeasy/web/capture_lane.py's convention, named for this payload. A mismatch
# says so in words rather than raising. Tolerant at exactly one seam: if this ever
# starts drowning in malformed pastes, swap this function and nothing else changes.

ENVELOPE_KEY = "photo_analysis"
ENVELOPE_VERSION = 1

# PhotoAnalysis — the enums the paste is checked against, from the pipeline's contract.
KINDS = ["concern", "asset"]
SEVERITIES = ["low", "medium", "high", "unknown"]
DISPOSITIONS = ["map", "review", "decline"]
IDENTIFIABILITY = ["none", "incidental", "identifiable_subject"]
REQUIRED = ["photo", "kind", "category", "severity", "summary", "area_type",
            "identifiability", "vulnerable", "disposition"]


def _loads(text: str):
    for candidate in _candidates(text):
        try:
            return json.loads(candidate)
        except Exception:
            try:  # one repair: a trailing comma before a closer
                import re
                return json.loads(re.sub(r",(\s*[}\]])", r"\1", candidate))
            except Exception:
                continue
    return None


def _candidates(text: str):
    t = text.strip()
    if "```" in t:                                   # a fenced block, first
        parts = t.split("```")
        for p in parts[1:]:
            body = p.split("\n", 1)[-1] if p[:20].strip().lower() in ("json", "") else p
            yield body.rsplit("```", 1)[0]
    yield t                                          # then the raw text
    i, j = t.find("{"), t.rfind("}")                 # then the outermost object
    if i != -1 and j > i:
        yield t[i:j + 1]


def parse_envelope(text: str) -> str:
    """Validate a pasted analysis against the pipeline's PhotoAnalysis contract.

    Returns {ok, rows, errors}. No LLM call happens here, which is the property
    that makes the paste-back lane cheap enough to be the default.
    """
    obj = _loads(text or "")
    if obj is None:
        return json.dumps({"ok": False, "errors": ["Could not find JSON in that paste."], "rows": []})
    if not isinstance(obj, dict):
        return json.dumps({"ok": False, "errors": ["Expected an object at the top level."], "rows": []})

    if ENVELOPE_KEY not in obj:
        return json.dumps({"ok": False, "rows": [], "errors": [
            f'No "{ENVELOPE_KEY}" key. The prompt asks for an envelope shaped '
            f'{{"{ENVELOPE_KEY}": {{"version": {ENVELOPE_VERSION}, "photos": [...]}}}}.']})
    env = obj[ENVELOPE_KEY]
    ver = env.get("version") if isinstance(env, dict) else None
    if ver != ENVELOPE_VERSION:
        return json.dumps({"ok": False, "rows": [], "errors": [
            f"envelope version {ver!r}, this page speaks {ENVELOPE_VERSION}"]})

    rows, errors = [], []
    for i, row in enumerate(env.get("photos") or []):
        where = f"photos[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{where}: not an object"); continue
        missing = [k for k in REQUIRED if k not in row]
        if missing:
            errors.append(f"{where}: missing {', '.join(missing)}"); continue
        for field, allowed in (("kind", KINDS), ("severity", SEVERITIES),
                               ("disposition", DISPOSITIONS),
                               ("identifiability", IDENTIFIABILITY)):
            if row[field] not in allowed:
                errors.append(f"{where}: {field}={row[field]!r} is not one of {allowed}")
        if not isinstance(row.get("vulnerable"), bool):
            errors.append(f"{where}: vulnerable must be true or false")
        rows.append(row)
    return json.dumps({"ok": not errors, "rows": rows, "errors": errors})


def versions() -> str:
    import sys
    import PIL
    return json.dumps({"python": sys.version.split()[0], "pillow": PIL.__version__,
                       "pillow_heif": HEIF, "core": __version__})


# ── samples, so the page works before the reader finds a folder ─────────────────

def sample_photos(n: int = 12, seed: int = 7):
    """Generate n JPEGs carrying real EXIF — GPS IFD and a capture time.

    Not photographs of anything: colored noise at phone-camera dimensions. They
    exist so the pipeline has genuine bytes and a genuine EXIF walk to do when the
    reader has not dropped a folder in. Everything measured from them is measured;
    it is only the subject matter that is synthetic, and the page says so.
    """
    import random
    from PIL import Image
    from PIL.TiffImagePlugin import IFDRational as R

    rnd = random.Random(seed)
    out = []
    # a few blocks of one street grid, so the GeoJSON plots as a walk
    lat0, lon0 = 45.5202, -122.6742
    for i in range(n):
        w, h = (4032, 3024) if i % 3 else (3024, 4032)   # some portrait, as a phone does
        # A per-pixel Python loop costs seconds per photo under WebAssembly. Build a
        # small noise field in one call and scale it up: same JPEG work, no Python loop.
        seed_im = Image.frombytes("RGB", (64, 48), rnd.randbytes(64 * 48 * 3))
        im = seed_im.resize((w, h), Image.BILINEAR)
        lat = lat0 + (i % 4) * 0.0012 + rnd.uniform(-2e-4, 2e-4)
        lon = lon0 + (i // 4) * 0.0016 + rnd.uniform(-2e-4, 2e-4)

        def dms(v):
            v = abs(v)
            d = int(v); m = int((v - d) * 60); s = round((v - d - m / 60) * 3600, 2)
            return (R(d), R(m), R(int(s * 100), 100))

        exif = Image.Exif()
        exif[0x8825] = {1: "N" if lat >= 0 else "S", 2: dms(lat),
                        3: "E" if lon >= 0 else "W", 4: dms(lon)}
        exif[0x0132] = f"2026:08:{14 + i // 6:02d} {9 + i % 6:02d}:{(i * 7) % 60:02d}:00"
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=88, exif=exif)
        out.append((f"SAMPLE_{i + 1:04d}.jpg", buf.getvalue()))
    return out


def sample_photo_bytes(n: int = 12, seed: int = 7) -> str:
    """The samples as a JSON manifest of name + latin-1 payload, for the page."""
    return json.dumps([{"name": nm, "n": len(b)} for nm, b in sample_photos(n, seed)])
