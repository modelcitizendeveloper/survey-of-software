# Use Case: High-Security Application

## Scenario

Applications with elevated security requirements:
- Financial services, healthcare, government
- Sensitive personal data
- Compliance requirements (SOC2, HIPAA, etc.)
- Sophisticated threat model

## Requirements

| Requirement | Priority | Notes |
|-------------|----------|-------|
| Maximum attack resistance | CRITICAL | Resist nation-state attackers |
| Side-channel resistance | HIGH | Timing attack protection |
| Audit trail | HIGH | Security logging |
| Compliance | HIGH | Meet regulatory standards |
| Login latency | MEDIUM | Can accept 500ms+ |

## Library Fitness

| Library | Fit Score | Reasoning |
|---------|-----------|-----------|
| argon2-cffi | **98%** | Best algorithm, tunable security |
| bcrypt | 65% | Lacks memory-hardness |
| hashlib.scrypt | 75% | Good security but poor API |
| passlib | 20% | Unmaintained = security risk |

## Recommendation: argon2-cffi (High Memory Configuration)

### Configuration

```python
from argon2 import PasswordHasher, Type

# High-security configuration
# - Memory: 128 MiB (2.8x default)
# - Time cost: 3 (3x default)
# - Parallelism: 1
# - Latency: ~400-500ms
ph = PasswordHasher(
    time_cost=3,
    memory_cost=128 * 1024,  # 128 MiB in KiB
    parallelism=1,
    hash_len=32,
    salt_len=16,
    type=Type.ID  # Argon2id (default, explicit for clarity)
)
```

### Implementation Pattern

```python
import logging
from datetime import datetime
from argon2 import PasswordHasher, Type
from argon2.exceptions import VerifyMismatchError

logger = logging.getLogger("security")

class SecureAuthService:
    def __init__(self):
        self.ph = PasswordHasher(
            time_cost=3,
            memory_cost=128 * 1024,
            parallelism=1,
            type=Type.ID
        )

    def hash_password(self, password: str, user_id: str) -> str:
        """Hash password with audit logging."""
        hash = self.ph.hash(password)
        logger.info(f"Password hashed for user {user_id}", extra={
            "event": "password_hash",
            "user_id": user_id,
            "algorithm": "argon2id",
            "timestamp": datetime.utcnow().isoformat()
        })
        return hash

    def verify_password(
        self,
        password: str,
        hash: str,
        user_id: str,
        ip_address: str
    ) -> bool:
        """Verify password with security logging."""
        try:
            self.ph.verify(hash, password)
            logger.info(f"Successful authentication for {user_id}", extra={
                "event": "auth_success",
                "user_id": user_id,
                "ip_address": ip_address,
                "timestamp": datetime.utcnow().isoformat()
            })
            return True
        except VerifyMismatchError:
            logger.warning(f"Failed authentication for {user_id}", extra={
                "event": "auth_failure",
                "user_id": user_id,
                "ip_address": ip_address,
                "timestamp": datetime.utcnow().isoformat()
            })
            return False

    def enforce_password_policy(self, password: str) -> list[str]:
        """Validate password against security policy."""
        errors = []
        if len(password) < 12:
            errors.append("Password must be at least 12 characters")
        if not any(c.isupper() for c in password):
            errors.append("Password must contain uppercase letter")
        if not any(c.islower() for c in password):
            errors.append("Password must contain lowercase letter")
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            errors.append("Password must contain special character")
        return errors
```

### Attack Cost Analysis

With 128 MiB memory, 3 iterations:

| Attacker Resource | Time to Crack 8-char | Cost |
|-------------------|---------------------|------|
| Single GPU | Years | N/A |
| GPU cluster (100) | Months | $100K+ |
| Nation-state | Weeks | Millions |

**Source**: Red Hat Research Argon2 analysis

### Additional Security Measures

1. **Hardware Security Module (HSM)** for key storage
2. **Pepper** (application-level secret added to passwords)
3. **Rate limiting** with exponential backoff
4. **Account lockout** after failed attempts
5. **Multi-factor authentication** as additional layer

### Pepper Implementation

```python
import hmac
import hashlib
import os

class PepperedAuthService(SecureAuthService):
    def __init__(self, pepper: bytes):
        super().__init__()
        # Pepper should be stored securely (HSM, env var, secrets manager)
        self.pepper = pepper

    def _apply_pepper(self, password: str) -> str:
        """Apply pepper to password before hashing."""
        return hmac.new(
            self.pepper,
            password.encode(),
            hashlib.sha256
        ).hexdigest()

    def hash_password(self, password: str, user_id: str) -> str:
        peppered = self._apply_pepper(password)
        return super().hash_password(peppered, user_id)

    def verify_password(self, password: str, hash: str, user_id: str, ip: str) -> bool:
        peppered = self._apply_pepper(password)
        return super().verify_password(peppered, hash, user_id, ip)
```

## Compliance Considerations

| Standard | Password Hashing Requirement | argon2-cffi Status |
|----------|------------------------------|-------------------|
| SOC2 | Strong hashing | COMPLIANT |
| HIPAA | Encryption of PHI | COMPLIANT |
| PCI-DSS | Strong cryptography | COMPLIANT |
| FIPS 140-2 | FIPS-approved algorithms | NOT COMPLIANT* |

*For FIPS compliance, use PBKDF2-HMAC-SHA256 with 600,000+ iterations.
