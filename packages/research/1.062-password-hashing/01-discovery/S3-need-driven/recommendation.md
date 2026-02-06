# S3 Need-Driven Recommendation

## Use Case Summary

| Use Case | Recommended Library | Configuration |
|----------|---------------------|---------------|
| Standard Web App | argon2-cffi | Default (RFC 9106) |
| High-Security | argon2-cffi | 128 MiB, 3 iterations |
| High-Traffic API | bcrypt OR argon2-cffi | cost=10 OR low-memory |
| Legacy Migration | argon2-cffi + bcrypt | Dual verification |
| FIPS Compliance | hashlib | PBKDF2-SHA256, 600K iter |

## Decision Tree

```
Need password hashing?
│
├─ New project?
│  ├─ Yes → argon2-cffi (default config)
│  └─ No → See migration section
│
├─ FIPS-140 required?
│  ├─ Yes → PBKDF2 via hashlib (600K+ iterations)
│  └─ No → argon2-cffi
│
├─ High-security application?
│  ├─ Yes → argon2-cffi (128 MiB, 3 iterations)
│  └─ No → argon2-cffi (default)
│
├─ Memory-constrained?
│  ├─ Yes → bcrypt (cost=12)
│  └─ No → argon2-cffi
│
└─ Migrating from legacy?
   └─ Yes → Dual verification pattern
```

## Configuration Quick Reference

### Standard (Default)
```python
from argon2 import PasswordHasher
ph = PasswordHasher()  # ~200ms, 46 MiB
```

### High Security
```python
ph = PasswordHasher(time_cost=3, memory_cost=128*1024)  # ~500ms, 128 MiB
```

### Memory Constrained
```python
import bcrypt
salt = bcrypt.gensalt(rounds=12)  # ~300ms, 4 KB
```

### FIPS Compliant
```python
import hashlib
dk = hashlib.pbkdf2_hmac('sha256', password, salt, 600000)
```

## Implementation Checklist

### All Projects
- [ ] Use argon2-cffi for new password hashing
- [ ] Implement rate limiting on auth endpoints
- [ ] Log authentication events
- [ ] Use HTTPS for all password transmission
- [ ] Never store plaintext passwords

### High Security
- [ ] Increase memory_cost to 128 MiB+
- [ ] Implement pepper (application secret)
- [ ] Add multi-factor authentication
- [ ] Implement account lockout
- [ ] Security audit logging

### Migration
- [ ] Implement dual verification
- [ ] Track migration progress
- [ ] Plan timeline for legacy deprecation
- [ ] Communicate with users if forced reset needed

## Final Verdict

**argon2-cffi covers 90%+ of use cases** with its default configuration. Only deviate for:
- FIPS compliance → PBKDF2
- Severe memory constraints → bcrypt
- Existing bcrypt codebase → Keep + plan migration
