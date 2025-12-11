# API Design Comparison: Password Hashing Libraries

## Design Philosophy Spectrum

| Library | Philosophy | Target User |
|---------|------------|-------------|
| argon2-cffi | Safe defaults, hard to misuse | Application developers |
| bcrypt | Simple primitives | Developers who understand crypto |
| passlib | Algorithm abstraction | Migration scenarios |
| hashlib.scrypt | Raw primitive | Crypto experts |

## API Comparison

### argon2-cffi

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

# Hash (automatic salt, sensible defaults)
hash = ph.hash("password")

# Verify (constant-time comparison)
try:
    ph.verify(hash, "password")
except VerifyMismatchError:
    # Invalid password
    pass

# Check if rehash needed (parameter updates)
if ph.check_needs_rehash(hash):
    new_hash = ph.hash("password")
```

**Strengths**:
- Sensible defaults (OWASP-compliant out of box)
- Exception-based verification (forces error handling)
- Built-in rehash detection for parameter migration
- Fully typed (IDE support)

**Weaknesses**:
- Exception-based API controversial (some prefer bool)

### bcrypt

```python
import bcrypt

# Hash (must generate salt explicitly)
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(b"password", salt)

# Verify (returns bool)
if bcrypt.checkpw(b"password", hashed):
    # Valid password
    pass
```

**Strengths**:
- Simple 3-function API
- Boolean verification (familiar pattern)
- Explicit salt generation

**Weaknesses**:
- Must remember to generate salt
- Bytes-only API (encoding required)
- No built-in rehash detection
- Silent truncation at 72 bytes (fixed in v5.0.0)

### passlib

```python
from passlib.hash import argon2

# Hash
hash = argon2.hash("password")

# Verify
if argon2.verify("password", hash):
    # Valid
    pass

# CryptContext for migration
from passlib.context import CryptContext
ctx = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

hash = ctx.hash("password")
valid = ctx.verify("password", hash)
needs_update = ctx.needs_update(hash)
```

**Strengths**:
- CryptContext for algorithm migration
- Automatic deprecated hash detection
- Unified API across algorithms

**Weaknesses**:
- Unmaintained (no Python 3.13)
- bcrypt 4.x incompatibility
- Complex configuration

### hashlib.scrypt

```python
import hashlib
import os

# Hash (manual everything)
salt = os.urandom(16)
dk = hashlib.scrypt(
    b"password",
    salt=salt,
    n=2**17,
    r=8,
    p=1,
    maxmem=128*1024*1024,
    dklen=64
)

# Verify (manual comparison)
import hmac
stored_salt = ...  # retrieve from storage
stored_hash = ...  # retrieve from storage
computed = hashlib.scrypt(b"password", salt=stored_salt, n=2**17, r=8, p=1)
if hmac.compare_digest(computed, stored_hash):
    # Valid
    pass
```

**Strengths**:
- No external dependencies
- Full control over parameters

**Weaknesses**:
- No high-level API
- Manual salt management
- Manual constant-time comparison
- Easy to misuse

## Feature Matrix

| Feature | argon2-cffi | bcrypt | passlib | hashlib.scrypt |
|---------|-------------|--------|---------|----------------|
| Auto salt | YES | NO | YES | NO |
| Safe defaults | YES | PARTIAL | YES | NO |
| Rehash detection | YES | NO | YES | NO |
| Type hints | YES | YES | NO | YES |
| Algorithm migration | NO | NO | YES | NO |
| Python 3.13+ | YES | YES | NO | YES |
| Bytes + str | YES | BYTES | YES | BYTES |

## Common Mistakes Prevented

### argon2-cffi

```python
# PREVENTED: Can't forget salt (automatic)
# PREVENTED: Can't use weak parameters (sensible defaults)
# PREVENTED: Can't use timing-vulnerable comparison (built-in)
```

### bcrypt

```python
# POSSIBLE MISTAKE: Forgetting to generate salt
bcrypt.hashpw(b"password", b"$2b$12$...")  # Works but wrong

# POSSIBLE MISTAKE: Using non-constant-time comparison
if stored_hash == bcrypt.hashpw(b"password", stored_hash):  # Timing attack

# FIXED in v5.0.0: Password truncation (now raises ValueError)
```

### hashlib.scrypt

```python
# POSSIBLE MISTAKE: Reusing salt
salt = b"static_salt"  # WRONG - must be unique per password

# POSSIBLE MISTAKE: Weak parameters
hashlib.scrypt(b"password", salt=salt, n=1024, r=1, p=1)  # Too weak

# POSSIBLE MISTAKE: Non-constant-time comparison
if computed_hash == stored_hash:  # Timing attack
```

## API Usability Scoring

| Library | Ease of Use | Misuse Resistance | Migration Support | Score |
|---------|-------------|-------------------|-------------------|-------|
| argon2-cffi | 9/10 | 9/10 | 6/10 | **8.0/10** |
| bcrypt | 7/10 | 6/10 | 4/10 | **5.7/10** |
| passlib | 8/10 | 8/10 | 10/10 | **8.7/10** |
| hashlib.scrypt | 3/10 | 2/10 | 2/10 | **2.3/10** |

## Recommendation

**For new projects**: argon2-cffi (best defaults, hard to misuse)

**For migrations**: libpass (maintained passlib fork) or implement dual-verify pattern:

```python
from argon2 import PasswordHasher
import bcrypt

ph = PasswordHasher()

def verify_and_upgrade(password: str, stored_hash: str) -> tuple[bool, str | None]:
    """Verify password, return new hash if upgrade needed."""

    # Try Argon2 first
    if stored_hash.startswith("$argon2"):
        try:
            ph.verify(stored_hash, password)
            new_hash = ph.hash(password) if ph.check_needs_rehash(stored_hash) else None
            return True, new_hash
        except:
            return False, None

    # Fall back to bcrypt
    if stored_hash.startswith("$2"):
        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            return True, ph.hash(password)  # Upgrade to Argon2
        return False, None

    return False, None
```
