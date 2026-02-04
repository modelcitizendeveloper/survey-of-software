# 04: Security Model

**Date**: 2025-12-23
**Status**: Draft
**Context**: Security architecture for multi-bot Matrix platform

---

## Overview

Security model for `matrix.factumerit.app` supporting multiple bot services with varying access levels.

---

## Authentication Layers

### Layer 1: Matrix Identity (MAS)

**Primary authentication**: Matrix user account via MAS

```
User → MAS → Synapse
     ↓
  Matrix ID: @username:factumerit.app
```

**Features**:
- Password-based login (bcrypt)
- Email verification required
- Session management (JWT tokens)
- Password reset via email

**Configuration**:
- `password_registration_enabled: true` (invite-only in future?)
- `email_change_allowed: true`
- `password_change_allowed: true`

---

### Layer 2: Bot Authorization

**Question**: How do bots verify user identity and permissions?

#### Option A: Trust Matrix Identity (Current)

Bot receives Matrix user ID from Synapse, trusts it implicitly.

```python
# Bot receives event
user_id = event.sender  # @alice:factumerit.app
# Assume authenticated, no further checks
```

**Pros**: Simple, no additional auth needed
**Cons**: All Matrix users can use all bots

#### Option B: Per-Bot Access Control Lists

Bots maintain allowlists of authorized users.

```yaml
# vikunja-bot config
authorized_users:
  - @alice:factumerit.app
  - @bob:factumerit.app
```

**Pros**: Fine-grained control
**Cons**: Manual management, doesn't scale

#### Option C: Role-Based Access (Future)

Use Matrix room membership or custom roles.

```
#admins:factumerit.app → Can use @analysis: bot
#users:factumerit.app  → Can use @tasks: bot
#public:factumerit.app → Can use @assistant: bot
```

**Pros**: Scalable, self-service via room invites
**Cons**: Requires room management, more complex

**Current decision**: Start with Option A (trust Matrix identity), add ACLs per-bot as needed.

---

## Authorization Patterns

### Public Bots (Anyone Can DM)

- `@assistant:factumerit.app` - General LLM assistant
- `@qrcards:factumerit.app` - QR code generation

**Security**: Rate limiting only

### Private Bots (Authorized Users Only)

- `@tasks:factumerit.app` - Vikunja access (personal data)
- `@research:factumerit.app` - Internal research library
- `@analysis:factumerit.app` - Business intelligence

**Security**: ACL + rate limiting

### Admin-Only Bots (Future)

- `@admin:factumerit.app` - Server management
- `@monitor:factumerit.app` - System metrics

**Security**: Hardcoded admin list

---

## Rate Limiting

### Per-User Limits

| Bot Type | Requests/Minute | Requests/Hour | Requests/Day |
|----------|-----------------|---------------|--------------|
| Public | 10 | 100 | 1000 |
| Private | 30 | 500 | 5000 |
| Admin | Unlimited | Unlimited | Unlimited |

### Implementation

```python
# Redis-based rate limiter
from redis import Redis
import time

def check_rate_limit(user_id: str, limit: int, window: int) -> bool:
    key = f"ratelimit:{user_id}:{window}"
    current = redis.incr(key)
    if current == 1:
        redis.expire(key, window)
    return current <= limit
```

### Abuse Prevention

- **Exponential backoff**: Increase delay after repeated violations
- **Temporary bans**: 1 hour ban after 3 violations
- **Permanent bans**: Manual review for persistent abuse

---

## Data Access Control

### Vikunja Bot (@tasks:)

**Problem**: User A shouldn't see User B's tasks

**Solution**: Vikunja API token per Matrix user

```python
# Store mapping in PostgreSQL
vikunja_tokens = {
    "@alice:factumerit.app": "vikunja_token_alice",
    "@bob:factumerit.app": "vikunja_token_bob"
}

# Bot uses user's token for API calls
def get_tasks(matrix_user_id: str):
    token = get_vikunja_token(matrix_user_id)
    return vikunja_api.get_tasks(token)
```

**Encryption**: Tokens encrypted at rest with Fernet (see analyses/factumerit/26-SECURITY.md)

---

### Research Bot (@research:)

**Problem**: Some research may be confidential

**Options**:
1. **All public** - Any authorized user can query any research
2. **Project-based** - Tag research with projects, filter by user's projects
3. **Sensitivity levels** - Public, Internal, Confidential

**Current decision**: Start with "all public" (research is internal anyway), add filtering later if needed.

---

## Network Security

### TLS Everywhere

- ✅ Render terminates TLS at edge (automatic HTTPS)
- ✅ Internal services use HTTP (within Render private network)
- ✅ External API calls use HTTPS (Vikunja, LLM providers)

### Secrets Management

| Secret | Storage | Access |
|--------|---------|--------|
| MAS client secrets | Render env vars | MAS only |
| Vikunja API tokens | PostgreSQL (encrypted) | Bot service only |
| LLM API keys | PostgreSQL (encrypted) | Bot service only |
| Database passwords | Render env vars | Services only |

**Never**:
- ❌ Commit secrets to git
- ❌ Log secrets (even in debug mode)
- ❌ Return secrets in API responses

---

## Federation Security

### Server ACLs (Future)

Control which Matrix servers can federate with yours.

```yaml
# homeserver.yaml
federation:
  ip_range_blacklist:
    - '127.0.0.0/8'
    - '10.0.0.0/8'
  
  # Allow only trusted servers (optional)
  allowed_servers:
    - matrix.org
    - element.io
```

**Current decision**: Open federation (default), add ACLs if abuse occurs.

### Room Encryption

- **DMs with bots**: Unencrypted (bots need to read messages)
- **User-to-user DMs**: E2EE available (Synapse supports it)
- **Bot-created rooms**: Unencrypted by default

**Note**: E2EE prevents server-side moderation and logging.

---

## Audit Logging

### What to Log

| Event | Log Level | Retention |
|-------|-----------|-----------|
| User registration | INFO | 1 year |
| Login attempts | INFO | 90 days |
| Failed logins | WARNING | 1 year |
| Bot commands | INFO | 30 days |
| Rate limit violations | WARNING | 90 days |
| Admin actions | WARNING | 1 year |
| Errors | ERROR | 1 year |

### Log Storage

- **Render logs**: 7 days (free tier)
- **External logging** (future): Ship to S3 or log aggregator

---

## Incident Response

### Security Incident Levels

| Level | Description | Response Time | Actions |
|-------|-------------|---------------|---------|
| P0 | Data breach, unauthorized access | Immediate | Disable service, investigate, notify users |
| P1 | Abuse, spam, DoS | 1 hour | Rate limit, ban user, investigate |
| P2 | Suspicious activity | 24 hours | Monitor, investigate |
| P3 | Policy violation | 1 week | Warning, educate user |

### Runbook (Future)

- [ ] Create incident response playbook
- [ ] Define escalation path
- [ ] Set up alerting (Render metrics, custom monitors)

---

## Related

- [26-SECURITY.md](../factumerit/26-SECURITY.md) - Vikunja-specific security
- [03-DEPLOYMENT_LESSONS.md](./03-DEPLOYMENT_LESSONS.md) - TLS, secrets config
- [05-MONITORING_RUNBOOK.md](./05-MONITORING_RUNBOOK.md) - Health checks, alerts (TODO)

