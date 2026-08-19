"""core.py — the measurement behind compresso (floor model for Survey of Software 1.050).

One copy, two readers: the page fetches it into Pyodide; the native bench imports it.
Timing and the shared samples (API logs, random bytes) come from /workshop/_lib/workshop.py.
Every function the page calls returns JSON.
"""
import json, zlib, gzip, bz2, lzma, hashlib, sys
import zstandard, brotli, lz4.frame
from compression import zstd as stdzstd
from workshop import best as _best, json_logs, random_bytes

SAMPLES = {}
CAP = 1024*1024

def set_sample(name, data):
    b = bytes(data)[:CAP]
    SAMPLES[name] = b
    return json.dumps({"name": name, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()[:16]})

def init_samples():
    SAMPLES["json"] = json_logs()
    SAMPLES["random"] = random_bytes()
    return json.dumps({k: len(v) for k, v in SAMPLES.items()})

_zd = zstandard.ZstdDecompressor()
CODECS = {
    "zstandard":        (lambda d, L: zstandard.ZstdCompressor(level=L).compress(d), _zd.decompress),
    "compression.zstd": (lambda d, L: stdzstd.compress(d, level=L), stdzstd.decompress),
    "brotli":           (lambda d, Q: brotli.compress(d, quality=Q), brotli.decompress),
    "lz4":              (lambda d, L: lz4.frame.compress(d, compression_level=L), lz4.frame.decompress),
    "zlib":             (lambda d, L: zlib.compress(d, L), zlib.decompress),
    "bz2":              (lambda d, L: bz2.compress(d, L), bz2.decompress),
    "lzma":             (lambda d, L: lzma.compress(d, preset=L), lzma.decompress),
}

def measure(codec, level, sample, budget_ms=100):
    data = SAMPLES[sample]; c, d = CODECS[codec]; level = int(level)
    out = c(data, level)
    ok = d(out) == data
    tc, rc = _best(lambda x: c(x, level), data, budget_ms/1000)
    td, rd = _best(d, out, budget_ms/1000)
    n = len(data)
    return json.dumps({"codec": codec, "level": level, "sample": sample, "in": n, "out": len(out),
                       "ratio": round(n/max(1,len(out)), 3), "comp_MBs": round(n/tc/1e6, 1),
                       "decomp_MBs": round(n/td/1e6, 1), "comp_ms": round(tc*1000, 2),
                       "decomp_ms": round(td*1000, 2), "reps": [rc, rd], "roundtrip_ok": bool(ok)})

def stdlib_same(sample, level=3):
    data = SAMPLES[sample]
    a = zstandard.ZstdCompressor(level=level).compress(data); b = stdzstd.compress(data, level=level)
    return json.dumps({"identical": a == b, "bytes": len(a), "lib": ".".join(map(str, zstandard.ZSTD_VERSION)),
                       "stdlib": stdzstd.zstd_version, "python": sys.version.split()[0]})

def tiny(text):
    s = text.encode()
    return json.dumps({"in": len(s),
        "zstandard (level 3)": len(zstandard.ZstdCompressor(level=3).compress(s)),
        "brotli (quality 11)": len(brotli.compress(s)),
        "lz4 (frame)": len(lz4.frame.compress(s)),
        "zlib (level 6)": len(zlib.compress(s)),
        "gzip (level 6)": len(gzip.compress(s)),
        "bz2 (level 9)": len(bz2.compress(s)),
        "lzma (preset 6)": len(lzma.compress(s))})

def versions():
    return json.dumps({"python": sys.version.split()[0], "zstandard": zstandard.__version__,
                       "libzstd": ".".join(map(str, zstandard.ZSTD_VERSION)), "brotli": brotli.__version__,
                       "lz4": lz4.__version__, "zlib": zlib.ZLIB_VERSION, "stdlib_zstd": stdzstd.zstd_version})
