# Finding 001: Email Claim Availability Across OIDC Providers

**Date**: 2025-12-30  
**Category**: Identity Claims  
**Impact**: Critical for identity-based access control systems  
**Status**: Validated

---

## Summary

**Not all OIDC providers share email addresses.** While the `sub` (subject) claim is mandatory per OIDC spec, the `email` claim is optional and varies by provider. Applications relying on email as the primary user identifier must implement fallback strategies.

---

## The OIDC Specification

### Mandatory Claims (Always Present)

Per [OpenID Connect Core 1.0 specification](https://openid.net/specs/openid-connect-core-1_0.html):

```json
{
  "sub": "248289761001",  // ✅ REQUIRED - Subject identifier (unique user ID)
  "iss": "https://accounts.google.com",  // ✅ REQUIRED - Issuer
  "aud": "client_id_here",  // ✅ REQUIRED - Audience
  "exp": 1735689600,  // ✅ REQUIRED - Expiration time
  "iat": 1735686000   // ✅ REQUIRED - Issued at time
}
```

### Optional Claims (May Be Absent)

```json
{
  "email": "user@example.com",  // ⚠️ OPTIONAL
  "email_verified": true,  // ⚠️ OPTIONAL
  "name": "John Doe",  // ⚠️ OPTIONAL
  "preferred_username": "johndoe",  // ⚠️ OPTIONAL
  "picture": "https://...",  // ⚠️ OPTIONAL
  "locale": "en-US"  // ⚠️ OPTIONAL
}
```

**Key insight**: Only `sub`, `iss`, `aud`, `exp`, and `iat` are guaranteed. Everything else is optional.

---

## Provider-by-Provider Analysis

### ✅ Providers That Reliably Share Email

| Provider | Email Availability | Requirements | Notes |
|----------|-------------------|--------------|-------|
| **Google** | ✅ Always | `email` scope | Most reliable |
| **Microsoft** | ✅ Always | `email` scope | Azure AD, Microsoft accounts |
| **GitLab** | ✅ Always | `email` scope | Self-hosted and SaaS |
| **Auth0** | ✅ Always | Configurable | Enterprise identity platform |
| **Keycloak** | ✅ Always | Configurable | Self-hosted identity server |
| **Okta** | ✅ Always | `email` scope | Enterprise SSO |

### ⚠️ Providers With Conditional Email

| Provider | Email Availability | Conditions | Workaround |
|----------|-------------------|------------|------------|
| **GitHub** | ⚠️ Conditional | Email must be public OR `user:email` scope granted | User can hide email |
| **Discord** | ⚠️ Conditional | User privacy settings | User can opt out |
| **Apple** | ⚠️ First login only | Only provided on initial authorization | Can use relay email |
| **LinkedIn** | ⚠️ Requires permission | Special API access needed | Not available to all apps |
| **Matrix** | ⚠️ Optional | Depends on homeserver config and user settings | Use Matrix ID instead |

### ❌ Providers That Never Share Email

| Provider | Email Availability | Alternative Identifier |
|----------|-------------------|------------------------|
| **Twitter/X** | ❌ Never | `sub` claim only |
| **Reddit** | ❌ Never | Username in `preferred_username` |
| **Twitch** | ❌ Never | `sub` claim only |

---

## Real-World Implications

### Use Case 1: Email as Primary Identifier

**Scenario**: Application uses email to identify users across sessions and devices.

**Problem**: 
```python
# This fails for Twitter, Matrix (sometimes), Discord (sometimes)
email = id_token.get("email")
user = database.get_user_by_email(email)  # ❌ email may be None
```

**Solution**: Implement fallback to provider-scoped `sub` claim.

### Use Case 2: Cross-Provider Account Linking

**Scenario**: User logs in with Google (has email), then logs in with Matrix (no email).

**Problem**: Can't automatically link accounts without email.

**Solution**: 
- Use email when available (enables automatic linking)
- Use `provider:sub` when email unavailable (separate account)
- Provide manual account linking UI

### Use Case 3: Invite-Only Registration

**Scenario**: Application checks if user's email exists in allowlist before allowing registration.

**Problem**: Can't check email if provider doesn't share it.

**Solution**:
- For email-based providers: Check email against allowlist
- For non-email providers: Check `provider:sub` against allowlist OR require email collection during registration

---

## Technical Patterns

### Pattern 1: Email-First with Sub Fallback

```python
def extract_identity(id_token: dict, provider: str) -> tuple[str, str]:
    """
    Extract user identity from ID token.
    
    Returns:
        (identity_type, identity_value)
    """
    # Prefer email (enables cross-provider linking)
    email = id_token.get("email")
    if email:
        return ("email", email)
    
    # Fallback to provider-scoped sub
    sub = id_token.get("sub")
    if sub:
        return ("sub", f"{provider}:{sub}")
    
    raise ValueError("No usable identity claim")
```

**Pros**: 
- Works with all providers
- Enables cross-provider linking when email available
- Graceful degradation

**Cons**: 
- More complex database schema
- Users without email can't link accounts

### Pattern 2: Require Email Collection

```python
def handle_oidc_callback(id_token: dict):
    email = id_token.get("email")
    
    if not email:
        # Redirect to email collection form
        return redirect("/complete-profile?sub={sub}&provider={provider}")
    
    # Proceed with email-based flow
    user = get_or_create_user(email)
```

**Pros**: 
- Consistent user experience
- Email always available for communication
- Simpler database schema

**Cons**: 
- Extra friction for users
- May violate user privacy expectations
- Requires email verification

### Pattern 3: Multi-Identity Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),  -- Optional
    display_name VARCHAR(255),
    created_at TIMESTAMP
);

CREATE TABLE user_identities (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    provider VARCHAR(50) NOT NULL,
    identity_type VARCHAR(20) NOT NULL,  -- "email", "sub", "matrix_id"
    identity_value VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    UNIQUE(provider, identity_type, identity_value)
);
```

**Pros**: 
- Supports all providers
- Enables multi-provider linking
- Future-proof

**Cons**: 
- More complex queries
- Requires migration from email-only schema

---

## Provider-Specific Considerations

### Matrix Homeservers

**What Matrix provides**:
```json
{
  "sub": "@alice:matrix.example.org",  // Matrix ID (always present)
  "email": "alice@example.com",  // Optional (user setting)
  "preferred_username": "alice"  // Localpart (usually present)
}
```

**Recommendation**: 
- Prefer email if available (cross-provider linking)
- Use Matrix ID (`sub`) as fallback (stable, human-readable)
- Don't use `preferred_username` alone (not globally unique)

### Apple Sign In

**Unique behavior**: Email only provided on first authorization.

**What Apple provides**:
```json
// First login
{
  "sub": "001234.abc123...",
  "email": "user@privaterelay.appleid.com",  // ✅ Present
  "email_verified": true
}

// Subsequent logins
{
  "sub": "001234.abc123...",
  // ❌ No email claim
}
```

**Recommendation**: 
- Store email on first login
- Use `sub` for subsequent authentications
- Handle relay emails (`@privaterelay.appleid.com`)

### GitHub

**Conditional email**: Only if public or `user:email` scope granted.

**What GitHub provides**:
```json
// If email is public or scope granted
{
  "sub": "12345678",
  "email": "user@example.com",  // ✅ Present
  "preferred_username": "octocat"
}

// If email is private and no scope
{
  "sub": "12345678",
  "preferred_username": "octocat"
  // ❌ No email claim
}
```

**Recommendation**: 
- Request `user:email` scope explicitly
- Provide fallback to username-based identity
- Consider requiring email verification

---

## Decision Framework

### When to Use Email-Only

**Use email as primary identifier when**:
- ✅ You control which providers are enabled (Google, Microsoft only)
- ✅ Email is required for your business logic (notifications, billing)
- ✅ You're building an MVP and can add complexity later

**Example**: Internal enterprise app with Google Workspace SSO only.

### When to Use Multi-Identity

**Use multi-identity approach when**:
- ✅ Supporting multiple OIDC providers (including Matrix, Twitter, Discord)
- ✅ Users need to link multiple provider accounts
- ✅ Building a platform with diverse user base

**Example**: Open-source community platform supporting GitHub, GitLab, Matrix.

### When to Require Email Collection

**Require email collection when**:
- ✅ Email is essential for business operations
- ✅ You need verified contact information
- ✅ Willing to add registration friction

**Example**: SaaS product requiring billing contact.

---

## Recommendations

### For New Applications

1. **Start simple**: Email-only if using Google/Microsoft
2. **Document limitation**: "Currently supports Google and Microsoft. Other providers coming soon."
3. **Plan migration**: Design database to support multi-identity later

### For Existing Applications

1. **Assess provider mix**: Which providers do you need to support?
2. **Evaluate impact**: How many users would be affected by email-less providers?
3. **Migrate incrementally**: Add `user_identities` table, migrate existing users, enable new providers

### For Enterprise Applications

1. **Standardize on email providers**: Require Google Workspace, Microsoft 365, or Okta
2. **Enforce email verification**: Don't trust `email_verified` claim alone
3. **Implement account linking**: Let users connect multiple work identities

---

## Related Findings

- **F002**: `sub` claim uniqueness and stability across providers (TODO)
- **F003**: Email verification and trust levels (TODO)
- **F004**: Privacy implications of email-based identity (TODO)

---

## References

- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html) - Section 5.1 (Standard Claims)
- [RFC 6749: OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc6749)
- [Google Identity Platform: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
- [Matrix Authentication Service](https://github.com/matrix-org/matrix-authentication-service)

---

## Changelog

- **2025-12-30**: Initial finding based on Factumerit OIDC middleware implementation

