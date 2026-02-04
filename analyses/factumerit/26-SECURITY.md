# 26: Security Considerations

**Date**: 2025-12-22
**Status**: Design

---

## Threat Model

| Asset | Threat | Impact | Mitigation |
|-------|--------|--------|------------|
| Vikunja API tokens | Leak/theft | Full access to user's tasks | Encrypt at rest, never log |
| LLM API keys | Leak/theft | Financial (API charges) | Encrypt at rest, never log |
| User messages | Eavesdropping | Privacy breach | E2EE (Matrix), TLS |
| Bot credentials | Compromise | Impersonation | Rotate, secure storage |
| Provisioning nonces | Replay attack | Unauthorized accounts | One-time, short expiry |

---

## Token Storage

### Encryption at Rest

```python
from cryptography.fernet import Fernet

# Key from environment variable (not in code/DB)
ENCRYPTION_KEY = os.environ["FACTUMERIT_ENCRYPTION_KEY"]
fernet = Fernet(ENCRYPTION_KEY)

def encrypt_token(token: str) -> str:
    return fernet.encrypt(token.encode()).decode()

def decrypt_token(encrypted: str) -> str:
    return fernet.decrypt(encrypted.encode()).decode()
```

### Database Schema

```sql
-- Tokens stored encrypted, never plaintext
CREATE TABLE vikunjae (
    ...
    token TEXT NOT NULL,  -- fernet-encrypted
    ...
);

-- Encryption key NEVER in database
-- Stored in Render environment variables
```

### Logging Policy

```python
# NEVER log tokens or keys
logger.info(f"Connected to {url}")  # OK
logger.info(f"Token: {token}")       # NEVER

# Mask in error messages
except Exception as e:
    logger.error(f"Vikunja error for {matrix_id}: {type(e).__name__}")
    # NOT: logger.error(f"Failed with token {token}: {e}")
```

---

## Matrix E2EE

### Device Verification

Matrix E2EE requires device verification. For a bot:

**Option 1: Unverified (simpler, less secure)**
- Bot responds to unverified messages
- Users see "not verified" warning
- OK for non-sensitive task data

**Option 2: Verified (complex, more secure)**
- Bot stores device keys persistently
- Users must verify bot device once
- Required for sensitive environments

**Recommendation**: Start with Option 1, add verification later if users request.

### E2EE Implementation

```python
from nio import AsyncClient, RoomMessageText
from nio.store import SqliteStore

# Persistent crypto store for E2EE
store = SqliteStore(
    user_id="@bot:matrix.factumerit.app",
    device_id="FACTUMERIT01",
    store_path="/data/crypto_store"
)

client = AsyncClient(
    homeserver="https://matrix.factumerit.app",
    user="@bot:matrix.factumerit.app",
    store_path="/data/crypto_store"
)

# Keys persist across restarts
await client.keys_upload()
```

---

## Provisioning Security

### One-Time Nonces

```python
import secrets
from datetime import datetime, timedelta

async def create_provisioning_link(matrix_id: str) -> str:
    # Cryptographically secure random nonce
    nonce = secrets.token_urlsafe(32)

    # Short expiry (1 hour)
    expires = datetime.utcnow() + timedelta(hours=1)

    await db.execute(
        "INSERT INTO nonces (matrix_id, nonce, expires_at) VALUES ($1, $2, $3)",
        matrix_id, nonce, expires
    )

    return f"https://factumerit.app/setup?mid={quote(matrix_id)}&nonce={nonce}"

async def verify_nonce(matrix_id: str, nonce: str) -> bool:
    row = await db.fetchone(
        "DELETE FROM nonces WHERE matrix_id=$1 AND nonce=$2 AND expires_at > NOW() RETURNING 1",
        matrix_id, nonce
    )
    return row is not None  # One-time use, deleted immediately
```

### Rate Limiting

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.get("/setup")
@limiter.limit("5/minute")  # Prevent brute force
async def setup(mid: str, nonce: str):
    ...
```

---

## API Communication

### TLS Everywhere

```
Bot ──TLS──▶ Dendrite
Bot ──TLS──▶ PostgreSQL
Bot ──TLS──▶ User's Vikunja
Bot ──TLS──▶ Ollama (if remote)
Bot ──TLS──▶ Claude/OpenAI API
```

### Vikunja API Validation

```python
async def validate_vikunja_connection(url: str, token: str) -> bool:
    """Verify token works before storing"""
    try:
        # Timeout to prevent hanging
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{url}/api/v1/user",
                headers={"Authorization": f"Bearer {token}"}
            )
            return resp.status_code == 200
    except Exception:
        return False
```

---

## Data Residency

| Data | Location | User Control |
|------|----------|--------------|
| Matrix messages | Dendrite (our server) | Standard Matrix retention |
| User config | PostgreSQL (Render) | `config clear` deletes all |
| Vikunja data | User's vikunja (their choice) | Full control |
| LLM context | Transient (not stored) | Ephemeral per request |

### Right to Deletion

```
User: config clear

Bot: This will delete:
     • All your vikunjae connections
     • Your LLM API keys
     • Your preferences

     Type "config clear confirm" to proceed.

User: config clear confirm

Bot: ✓ All your data has been deleted.
     DM me again anytime to start fresh.
```

---

## Secrets Management

### Render Environment Variables

```
FACTUMERIT_ENCRYPTION_KEY=...   # Token encryption
MATRIX_BOT_PASSWORD=...          # Bot login
DATABASE_URL=...                 # PostgreSQL (auto by Render)
VIKUNJA_ADMIN_TOKEN=...          # For provisioning (Phase 2)
```

### .env Template (for local dev)

```bash
# .env.example (commit this)
export FACTUMERIT_ENCRYPTION_KEY=generate-with-fernet
export MATRIX_BOT_PASSWORD=your-bot-password
export DATABASE_URL=postgresql://localhost/factumerit
export VIKUNJA_ADMIN_TOKEN=admin-token-for-provisioning

# .env (DO NOT COMMIT - in .gitignore)
export FACTUMERIT_ENCRYPTION_KEY=actual-secret-key
...
```

---

## Incident Response

### Token Compromise

If a user's Vikunja token is compromised:
1. User revokes token in their Vikunja settings
2. User runs `config remove [name]` in bot
3. User creates new token, runs `config add`

### Bot Compromise

If bot credentials are compromised:
1. Rotate Matrix bot password immediately
2. Rotate FACTUMERIT_ENCRYPTION_KEY
3. All stored tokens become unreadable (users must re-add)
4. Notify affected users via Matrix

---

## Audit Logging

```python
# Log security-relevant events (no secrets)
audit_logger.info({
    "event": "vikunja_added",
    "matrix_id": matrix_id,
    "vikunja_url": url,  # URL is OK
    "timestamp": datetime.utcnow().isoformat()
})

audit_logger.info({
    "event": "config_cleared",
    "matrix_id": matrix_id,
    "timestamp": datetime.utcnow().isoformat()
})
```

---

## Related

- [25-ARCHITECTURE.md](25-ARCHITECTURE.md)
- [24-USER_EXPERIENCE_FLOW.md](24-USER_EXPERIENCE_FLOW.md)
