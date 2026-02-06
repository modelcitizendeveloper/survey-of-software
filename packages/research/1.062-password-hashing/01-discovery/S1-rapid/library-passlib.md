# passlib

## Overview

Comprehensive password hashing framework supporting 30+ algorithms. **UNMAINTAINED since October 2020.**

## Key Metrics

| Metric | Value |
|--------|-------|
| Weekly Downloads | 4,925,500 |
| Monthly Downloads | 17,887,685 |
| Dependent Packages | 615 |
| Last Release | v1.7.4 (Oct 8, 2020) |
| License | BSD |
| Python Support | 2.6+, 3.3+ (no 3.13 support) |

## Maintainer

**Eli Collins** (individual developer)
- Organization: Assurance Technologies, LLC
- **Status**: No activity since 2020

## Security Status

- **Formal CVEs**: 0 assigned
- **Known issues**:
  - bcrypt_sha256 unsalted prehash vulnerability (EUVDB #VU28246)
  - DoS via wildcard passwords (SNYK-PYTHON-PASSLIB-40761)
- **Compatibility**: Incompatible with bcrypt 4.x (must pin <=4.0.0)

## Supported Algorithms

**Modern (recommended):**
- Argon2 (argon2id)
- BCrypt, BCrypt+SHA256
- SCrypt
- PBKDF2 (multiple variants)

**Legacy (compatibility only):**
- Unix crypt variants (DES, MD5, SHA256, SHA512)
- Windows NTLM, LanMan
- Oracle, MySQL, PostgreSQL hashes
- LDAP schemes
- Many others

## API Design

```python
from passlib.hash import argon2

# Hash
hash = argon2.hash("password")

# Verify
argon2.verify("password", hash)

# CryptContext for migration
from passlib.context import CryptContext
ctx = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
```

## Why Projects Used Passlib

1. **Algorithm abstraction** - Easy migration between algorithms
2. **CryptContext** - Automatic hash upgrades on login
3. **Legacy support** - Verify old hashes during migration
4. **Comprehensive** - One library for all algorithms

## Critical Problems (2025)

1. **Unmaintained 4+ years** - No releases since October 2020
2. **No Python 3.13 support** - crypt module removed in 3.13
3. **bcrypt 4.x incompatible** - Must pin old versions
4. **Community exodus** - FastAPI, Ansible migrating away
5. **Security debt** - No patches for reported issues

## Active Alternatives

| Library | Description | Status |
|---------|-------------|--------|
| **libpass** | Passlib fork by maintainer "Doctor" | v1.9.3 (Oct 2025), Python 3.9-3.13 |
| **pwdlib** | Modern, Argon2-focused | Actively maintained |
| Direct libs | argon2-cffi, bcrypt | Recommended |

## Verdict

**DO NOT USE for new projects.** Unmaintained for 4+ years with known compatibility issues. For existing passlib deployments, plan migration to libpass (fork) or direct argon2-cffi/bcrypt usage.
