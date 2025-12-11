# S2 Comprehensive Recommendation

## Overall Scoring

| Library | Security | Performance | API | Maintenance | Overall |
|---------|----------|-------------|-----|-------------|---------|
| argon2-cffi | 9.7 | 8.0 | 8.0 | 9.0 | **8.7/10** |
| bcrypt | 8.7 | 7.7 | 5.7 | 10.0 | **8.0/10** |
| hashlib.scrypt | 9.3 | 6.0 | 2.3 | 10.0 | **6.9/10** |
| passlib | 6.3 | 8.0 | 8.7 | 2.0 | **6.3/10** |

## Primary Recommendation: argon2-cffi

**Winner**: `argon2-cffi`

### Why argon2-cffi Wins

1. **Best algorithm**: Argon2id is OWASP #1 recommendation
2. **Zero CVEs**: Clean security record
3. **Modern design**: Memory-hard, side-channel resistant
4. **Excellent API**: Safe defaults, hard to misuse
5. **Active maintenance**: Python 3.13+ support, recent releases

### When bcrypt is Acceptable

- Existing bcrypt codebase (don't rewrite just for this)
- Memory-constrained environments
- Need maximum throughput (cost=10)
- Legacy Python 2 support required

### When to Avoid

| Library | Avoid When |
|---------|------------|
| passlib | Always (unmaintained, use libpass instead) |
| hashlib.scrypt | Building application code (use argon2-cffi) |
| bcrypt | New projects (use argon2-cffi) |

## Recommended Configurations

### argon2-cffi (New Projects)

```python
from argon2 import PasswordHasher, Type

# Standard web application
ph = PasswordHasher()  # Uses RFC 9106 low-memory defaults

# High-security application
ph_secure = PasswordHasher(
    time_cost=3,
    memory_cost=128 * 1024,  # 128 MiB
    parallelism=1,
    type=Type.ID
)
```

### bcrypt (Existing Systems)

```python
import bcrypt

# Minimum acceptable
BCRYPT_ROUNDS = 12  # ~300ms

# Tune based on your hardware
# Target: 250-500ms per hash
```

## Migration Path

### Phase 1: Add argon2-cffi

```python
# requirements.txt
argon2-cffi>=25.1.0
bcrypt>=5.0.0  # Keep for verification
```

### Phase 2: Dual Verification

```python
def verify_password(password: str, stored_hash: str) -> tuple[bool, str | None]:
    """Verify password, upgrade hash if needed."""

    if stored_hash.startswith("$argon2"):
        # Already Argon2
        try:
            ph.verify(stored_hash, password)
            return True, None
        except:
            return False, None

    if stored_hash.startswith("$2"):
        # Legacy bcrypt - verify and upgrade
        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            return True, ph.hash(password)
        return False, None

    return False, None
```

### Phase 3: Deprecate bcrypt

After sufficient time (6-12 months), consider:
1. Force password reset for remaining bcrypt users
2. Remove bcrypt verification code
3. Simplify to Argon2-only

## Final Verdict

| Scenario | Recommendation | Confidence |
|----------|----------------|------------|
| New project | argon2-cffi | VERY HIGH |
| Existing bcrypt | Keep + plan migration | HIGH |
| FIPS required | PBKDF2 | HIGH |
| Algorithm abstraction | libpass (passlib fork) | MEDIUM |
| Raw performance | bcrypt (cost=10) | MEDIUM |

**Default choice**: `pip install argon2-cffi`
