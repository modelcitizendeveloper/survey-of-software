# hashlib.scrypt (Python stdlib)

## Overview

Built-in scrypt implementation in Python's hashlib module, available since Python 3.6.

## Key Metrics

| Metric | Value |
|--------|-------|
| Availability | Python 3.6+ |
| Requirement | OpenSSL 1.1+ |
| RFC | RFC 7914 |
| Added | September 2016 (Christian Heimes) |
| Pure Python | Removed in Python 3.12 |

## API Design

```python
import hashlib
import os

# Generate hash
salt = os.urandom(16)
dk = hashlib.scrypt(
    b"password",
    salt=salt,
    n=2**14,      # CPU/memory cost (power of 2)
    r=8,          # Block size
    p=1,          # Parallelization
    maxmem=64*1024*1024,  # Max memory (64 MiB)
    dklen=64      # Output length
)
```

## Parameters

| Parameter | Description | OWASP Minimum |
|-----------|-------------|---------------|
| n | CPU/memory cost (power of 2) | 2^17 (131072) |
| r | Block size | 8 |
| p | Parallelization factor | 1 |
| maxmem | Memory limit in bytes | Default 32 MiB |

**Memory calculation**: 128 × n × r × p bytes

## Security Considerations

**Strengths:**
- Memory-hard (resists GPU/ASIC attacks)
- Part of Python stdlib (no external dependencies)
- Designed by Colin Percival (2009)

**Limitations:**
1. **Parameter coupling** - n controls BOTH time AND memory (cannot tune independently)
2. **Salt management** - Must generate unique salts manually
3. **No high-level API** - Raw primitive, easy to misuse
4. **Requires OpenSSL 1.1+** - Not available on older systems

## OWASP Status

- **Priority**: #2 (after Argon2id)
- **Recommendation**: "Use when Argon2id unavailable"
- **Configuration**: n=2^17, r=8, p=1 minimum

## Standalone scrypt Libraries

| Library | Weekly Downloads | Status |
|---------|-----------------|--------|
| scrypt (py-scrypt) | 38,903 | v0.9.4, Python 2/3/PyPy |
| pyscrypt | 46,665 | Pure Python (slow) |
| pylibscrypt | 1,373 | v2.0.0 (Feb 2021) |

**Recommendation**: Use `hashlib.scrypt` on Python 3.6+. Use `scrypt` package for older Python.

## Why Argon2 Over scrypt?

1. **Independent parameters** - Argon2 separates time and memory costs
2. **PHC winner** - More recent, competition-hardened design
3. **Side-channel resistance** - Argon2id variant addresses this
4. **Better defaults** - argon2-cffi provides safe defaults

## Verdict

**ACCEPTABLE as Argon2 fallback.** Stdlib availability is convenient, but parameter coupling makes tuning difficult. Prefer argon2-cffi for new projects per OWASP guidance.
