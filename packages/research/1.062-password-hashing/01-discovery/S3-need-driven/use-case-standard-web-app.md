# Use Case: Standard Web Application

## Scenario

A typical SaaS or web application with user authentication:
- 1,000 - 100,000 users
- 10-100 logins per minute peak
- Standard security requirements
- Modern Python stack (3.10+)

## Requirements

| Requirement | Priority | Notes |
|-------------|----------|-------|
| Secure password storage | CRITICAL | Resist offline attacks |
| Acceptable login latency | HIGH | <500ms |
| Easy implementation | HIGH | Developer-friendly API |
| Future-proof | MEDIUM | Algorithm migration path |
| Memory efficiency | LOW | Standard server resources |

## Library Fitness

| Library | Fit Score | Reasoning |
|---------|-----------|-----------|
| argon2-cffi | **95%** | OWASP #1, excellent API, sensible defaults |
| bcrypt | 80% | Acceptable but not preferred for new projects |
| passlib | 30% | Unmaintained, avoid |
| hashlib.scrypt | 50% | Too low-level for application code |

## Recommendation: argon2-cffi

### Configuration

```python
from argon2 import PasswordHasher

# Default configuration (RFC 9106 low-memory)
# - Memory: 46 MiB
# - Time cost: 1
# - Parallelism: 1
# - Latency: ~200ms
ph = PasswordHasher()
```

### Implementation Pattern

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

class AuthService:
    def __init__(self):
        self.ph = PasswordHasher()

    def hash_password(self, password: str) -> str:
        """Hash password for storage."""
        return self.ph.hash(password)

    def verify_password(self, password: str, hash: str) -> bool:
        """Verify password against stored hash."""
        try:
            self.ph.verify(hash, password)
            return True
        except (VerifyMismatchError, VerificationError):
            return False

    def needs_rehash(self, hash: str) -> bool:
        """Check if hash needs updating (parameter changes)."""
        return self.ph.check_needs_rehash(hash)
```

### Database Schema

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,  -- Argon2 hashes are ~100 chars
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Framework Integration

**FastAPI:**
```python
from fastapi import Depends, HTTPException
from argon2 import PasswordHasher

ph = PasswordHasher()

async def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(401, "Invalid credentials")

    try:
        ph.verify(user.password_hash, password)
    except:
        raise HTTPException(401, "Invalid credentials")

    # Upgrade hash if needed
    if ph.check_needs_rehash(user.password_hash):
        user.password_hash = ph.hash(password)
        db.commit()

    return user
```

**Django:**
```python
# settings.py
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',  # fallback
]

# pip install django[argon2]
```

## Security Checklist

- [ ] Use argon2-cffi default configuration
- [ ] Store only hashed passwords (never plaintext)
- [ ] Use HTTPS for password transmission
- [ ] Implement rate limiting on login endpoint
- [ ] Log failed authentication attempts
- [ ] Consider account lockout after N failures
