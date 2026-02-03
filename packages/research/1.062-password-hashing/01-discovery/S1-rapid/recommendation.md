# S1 Recommendation: argon2-cffi

## Decision (Made in 15 minutes)

**WINNER**: `argon2-cffi` library

**Installation**: `pip install argon2-cffi`

## Rationale: OWASP + Zero CVEs + Modern Design

### Security Authority Alignment

- **OWASP 2025**: Argon2id is #1 recommendation for password storage
- **PHC 2015**: Argon2 won the Password Hashing Competition
- **CVE History**: Zero vulnerabilities in argon2-cffi

### Download Trends Tell the Story

| Library | Weekly Downloads | Trajectory |
|---------|-----------------|------------|
| bcrypt | 32.7M | Legacy adoption, steady |
| argon2-cffi | 10.6M | Growing, new projects |
| passlib | 4.9M | Declining, unmaintained |
| scrypt | 38K | Niche |

bcrypt's higher downloads reflect legacy adoption, not current best practice.

### Requirements Alignment

| Requirement | argon2-cffi |
|------------|-------------|
| OWASP recommended | YES (#1) |
| Zero CVEs | YES |
| Active maintenance | YES (Jun 2025) |
| Python 3.13+ support | YES |
| Memory-hard (GPU resistant) | YES |
| Good API design | YES |
| Sensible defaults | YES |

## Decision Matrix

| Scenario | Recommendation |
|----------|----------------|
| New project | argon2-cffi |
| Existing bcrypt system | Keep bcrypt, plan migration |
| FIPS-140 required | PBKDF2 via hashlib |
| Need algorithm abstraction | libpass (passlib fork) |
| Legacy Python 2 | bcrypt |

## Why Not the Alternatives?

**bcrypt**:
- OWASP: "Only for legacy systems"
- Not memory-hard (GPU vulnerable)
- 72-byte password limit
- Still acceptable, just not preferred

**passlib**:
- UNMAINTAINED since October 2020
- No Python 3.13 support
- FastAPI/Ansible migrating away
- Use libpass fork if needed

**hashlib.scrypt**:
- OWASP #2 (fallback position)
- Parameter coupling problem
- No high-level API
- Acceptable when Argon2 unavailable

## Quick Start

```python
from argon2 import PasswordHasher

ph = PasswordHasher()

# Hash password
hash = ph.hash("user_password")

# Verify password
try:
    ph.verify(hash, "user_password")
    # Check if rehash needed (parameter updates)
    if ph.check_needs_rehash(hash):
        new_hash = ph.hash("user_password")
except argon2.exceptions.VerifyMismatchError:
    # Invalid password
    pass
```

## Decision Confidence: VERY HIGH

When OWASP explicitly ranks Argon2id as #1 and the library has:
- Zero CVEs
- Active maintenance
- Excellent API
- Sensible defaults

The choice is clear. Use argon2-cffi for all new password hashing.

## Migration Note

For existing bcrypt deployments:
1. Add argon2-cffi alongside bcrypt
2. Hash new passwords with Argon2
3. Verify old passwords with bcrypt
4. Re-hash to Argon2 on successful login
5. Eventually deprecate bcrypt verification
