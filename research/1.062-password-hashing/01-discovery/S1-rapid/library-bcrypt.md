# bcrypt

## Overview

Python binding to the bcrypt password hashing algorithm via PyCA (Python Cryptographic Authority).

## Key Metrics

| Metric | Value |
|--------|-------|
| Weekly Downloads | 32,700,000 |
| Monthly Downloads | 138,900,000 |
| GitHub Stars | 1,400 |
| Contributors | 38 |
| Used By | 342,000+ projects |
| Last Release | v5.0.0 (Sep 25, 2025) |
| License | Apache-2.0 |
| Python Support | 3.8+, PyPy 3.11+ |

## Maintainer

**PyCA (Python Cryptographic Authority)** - Trusted organization
- Also maintains `cryptography`, `pyOpenSSL`
- Industry-standard cryptographic libraries
- Strong security practices

## Security Status

- **CVEs**: 0 (current versions)
- **Historical**: CVE-2013-1895 (old py-bcrypt <0.3, fixed)
- **v5.0.0 security improvement**: Now raises ValueError for passwords >72 bytes (was silently truncated)

## Key Features

- Simple 3-function API
- Automatic salt generation
- Adjustable work factor (cost parameter)
- Implemented in Rust (as of recent versions)
- 72-byte password limit (enforced in v5.0.0)

## API Design

```python
import bcrypt

# Hash a password
salt = bcrypt.gensalt(rounds=12)  # Work factor
hashed = bcrypt.hashpw(b"password", salt)

# Verify a password
bcrypt.checkpw(b"password", hashed)  # Returns True/False
```

## Performance

- **Design goal**: Intentionally slow (~103 hashes/sec)
- **Default rounds**: 12 (≈300ms)
- **OWASP guidance**: Tune to 250-500ms on production hardware
- **Comparison**: SHA-256 is ~1,200x faster (that's the point)

## Limitations

1. **72-byte password limit** - Passwords truncated beyond this
2. **No memory-hardness** - Vulnerable to GPU attacks (compared to Argon2)
3. **Legacy status** - OWASP recommends Argon2 for new systems

## OWASP Status

- **Recommendation**: "Only for legacy systems where Argon2 and scrypt are not available"
- **Work factor**: Minimum 10, recommend 12+
- **Still acceptable**: For systems requiring <1 second authentication

## Verdict

**ACCEPTABLE for existing systems, NOT recommended for new projects.** 3x more downloads than argon2-cffi due to legacy adoption, but OWASP explicitly recommends Argon2 over bcrypt for new development.
