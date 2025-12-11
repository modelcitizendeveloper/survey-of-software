# argon2-cffi

## Overview

Python binding to the Argon2 password hashing algorithm, winner of the 2015 Password Hashing Competition.

## Key Metrics

| Metric | Value |
|--------|-------|
| Weekly Downloads | 10,578,390 |
| Monthly Downloads | 43,648,848 |
| GitHub Stars | ~500 |
| Contributors | Multiple |
| Last Release | v25.1.0 (June 3, 2025) |
| License | MIT |
| Python Support | 3.8-3.14, PyPy |

## Maintainer

**Hynek Schlawack** (individual developer)
- Well-known Python community member
- Also maintains attrs, structlog
- Supported by Variomedia AG, Tidelift, GitHub Sponsors

## Security Status

- **CVEs**: 0 (none found)
- **Snyk scan**: No vulnerabilities, no malware
- **Security contact**: hs@ox.cx

## Key Features

- High-level `PasswordHasher` API with sensible defaults
- Uses **Argon2id** variant by default (recommended)
- Automatic random salt generation
- RFC 9106 low-memory profile by default
- Fully typed (type hints throughout)
- Can verify any Argon2 variant

## API Design

```python
from argon2 import PasswordHasher

ph = PasswordHasher()
hash = ph.hash("password")
ph.verify(hash, "password")  # Returns True or raises exception
ph.check_needs_rehash(hash)  # Check if parameters need updating
```

## Default Parameters (v25.1.0)

- Memory: 47,104 KiB (46 MiB) - RFC 9106 low-memory profile
- Time cost: 1 iteration
- Parallelism: 1

## OWASP Recommendations

**Argon2id minimum configuration:**
- Memory: 19 MiB (m=19456)
- Iterations: 2 (t=2)
- Parallelism: 1 (p=1)

**Stronger configuration:**
- Memory: 46 MiB (m=47104) ← argon2-cffi default
- Iterations: 1 (t=1)
- Parallelism: 1 (p=1)

## Why Argon2?

1. **PHC Winner** (2015) - Peer-reviewed, competition-hardened
2. **Memory-hard** - Resists GPU/ASIC attacks
3. **Side-channel resistant** (Argon2id variant)
4. **Modern design** - Addresses bcrypt/scrypt limitations
5. **OWASP #1 recommendation** for password storage

## Verdict

**RECOMMENDED for all new projects.** Zero CVEs, OWASP primary recommendation, excellent API design, active maintenance.
