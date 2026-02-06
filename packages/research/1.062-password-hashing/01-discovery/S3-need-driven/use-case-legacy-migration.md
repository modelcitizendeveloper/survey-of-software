# Use Case: Legacy Migration

## Scenario

Upgrading from older password hashing schemes:
- MD5, SHA1, SHA256 (unsalted or weakly salted)
- Old bcrypt with low cost factor
- passlib-based systems
- Custom/proprietary schemes

## Requirements

| Requirement | Priority | Notes |
|-------------|----------|-------|
| Zero-downtime migration | CRITICAL | No forced password resets |
| Backward compatibility | CRITICAL | Verify old hashes |
| Gradual upgrade | HIGH | Upgrade on login |
| Security improvement | HIGH | Move to Argon2 |
| Audit trail | MEDIUM | Track migration progress |

## Migration Strategies

### Strategy 1: Dual Verification (Recommended)

Verify old hash formats, upgrade on successful login.

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import bcrypt
import hashlib

class MigrationAuthService:
    def __init__(self):
        self.ph = PasswordHasher()

    def verify_and_upgrade(
        self,
        password: str,
        stored_hash: str
    ) -> tuple[bool, str | None]:
        """
        Verify password against any supported hash format.
        Returns (is_valid, new_hash_if_upgrade_needed).
        """

        # Try Argon2 first (target format)
        if stored_hash.startswith("$argon2"):
            try:
                self.ph.verify(stored_hash, password)
                # Check if parameters need updating
                if self.ph.check_needs_rehash(stored_hash):
                    return True, self.ph.hash(password)
                return True, None
            except VerifyMismatchError:
                return False, None

        # bcrypt (legacy)
        if stored_hash.startswith("$2"):
            try:
                if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                    return True, self.ph.hash(password)
            except:
                pass
            return False, None

        # SHA256 (very old, insecure)
        if len(stored_hash) == 64 and stored_hash.isalnum():
            # Assuming format: sha256(password)
            computed = hashlib.sha256(password.encode()).hexdigest()
            if computed == stored_hash:
                return True, self.ph.hash(password)
            return False, None

        # MD5 (ancient, very insecure)
        if len(stored_hash) == 32 and stored_hash.isalnum():
            computed = hashlib.md5(password.encode()).hexdigest()
            if computed == stored_hash:
                return True, self.ph.hash(password)
            return False, None

        # Unknown format
        return False, None
```

### Strategy 2: Wrap-and-Replace

Wrap old hash with new algorithm (no password required).

```python
def wrap_legacy_hash(old_hash: str) -> str:
    """
    Wrap legacy hash with Argon2 for immediate security upgrade.
    User can still login with original password.

    stored = argon2(old_hash)
    verify: argon2_verify(stored, legacy_hash(password))
    """
    ph = PasswordHasher()
    return ph.hash(old_hash)

def verify_wrapped(password: str, wrapped_hash: str, legacy_func) -> bool:
    """Verify against wrapped legacy hash."""
    ph = PasswordHasher()
    legacy_hash = legacy_func(password)
    try:
        ph.verify(wrapped_hash, legacy_hash)
        return True
    except:
        return False
```

### Strategy 3: Force Reset (Last Resort)

For severely compromised schemes or compliance requirements.

```python
from datetime import datetime, timedelta

def identify_users_needing_reset(db) -> list:
    """Find users with legacy hashes requiring forced reset."""
    users = db.query(User).filter(
        ~User.password_hash.like("$argon2%")
    ).all()
    return users

def initiate_forced_reset(user, db):
    """Force password reset for user with legacy hash."""
    user.password_reset_required = True
    user.password_reset_deadline = datetime.utcnow() + timedelta(days=30)
    user.password_hash = None  # Invalidate old hash
    db.commit()
    send_password_reset_email(user)
```

## Migration from passlib

passlib is unmaintained. Migrate to direct library usage or libpass.

### Option A: Direct Libraries (Recommended)

```python
# Before (passlib)
from passlib.context import CryptContext
ctx = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

# After (direct)
from argon2 import PasswordHasher
import bcrypt

ph = PasswordHasher()

def verify_and_upgrade(password: str, hash: str) -> tuple[bool, str | None]:
    if hash.startswith("$argon2"):
        try:
            ph.verify(hash, password)
            return True, None
        except:
            return False, None

    if hash.startswith("$2"):
        if bcrypt.checkpw(password.encode(), hash.encode()):
            return True, ph.hash(password)
        return False, None

    return False, None
```

### Option B: libpass (passlib Fork)

```python
# pip install libpass

from libpass.context import CryptContext

# Same API as passlib, but maintained
ctx = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
```

## Database Migration Tracking

```sql
-- Add migration tracking columns
ALTER TABLE users ADD COLUMN password_algorithm VARCHAR(20);
ALTER TABLE users ADD COLUMN password_migrated_at TIMESTAMP;

-- Update on migration
UPDATE users
SET password_hash = :new_hash,
    password_algorithm = 'argon2id',
    password_migrated_at = NOW()
WHERE id = :user_id;
```

## Migration Progress Monitoring

```python
def migration_stats(db) -> dict:
    """Get password migration statistics."""
    total = db.query(User).count()
    argon2 = db.query(User).filter(User.password_hash.like("$argon2%")).count()
    bcrypt = db.query(User).filter(User.password_hash.like("$2%")).count()
    legacy = total - argon2 - bcrypt

    return {
        "total_users": total,
        "argon2": argon2,
        "argon2_pct": round(argon2 / total * 100, 1),
        "bcrypt": bcrypt,
        "bcrypt_pct": round(bcrypt / total * 100, 1),
        "legacy": legacy,
        "legacy_pct": round(legacy / total * 100, 1),
        "migration_complete": legacy == 0 and bcrypt == 0
    }
```

## Timeline Recommendation

| Phase | Action | Duration |
|-------|--------|----------|
| 1 | Deploy dual verification | Week 1 |
| 2 | Monitor migration progress | Weeks 2-12 |
| 3 | Email inactive users | Week 8 |
| 4 | Force reset remaining legacy | Week 12+ |
| 5 | Remove legacy verification code | Week 16+ |
