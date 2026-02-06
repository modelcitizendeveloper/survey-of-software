# OIDC Provider Quick Reference

**Purpose**: Quick lookup table for OIDC provider characteristics when implementing authentication.

---

## Email Claim Availability

| Provider | Email | Conditions | Fallback Identity |
|----------|-------|------------|-------------------|
| **Google** | ✅ Always | Requires `email` scope | N/A |
| **Microsoft** | ✅ Always | Requires `email` scope | N/A |
| **GitLab** | ✅ Always | Requires `email` scope | N/A |
| **Auth0** | ✅ Always | Configurable | N/A |
| **Keycloak** | ✅ Always | Configurable | N/A |
| **Okta** | ✅ Always | Requires `email` scope | N/A |
| **GitHub** | ⚠️ Conditional | Email public OR `user:email` scope | `preferred_username` |
| **Discord** | ⚠️ Conditional | User privacy settings | `sub` |
| **Apple** | ⚠️ First login | Only on initial authorization | `sub` (store email) |
| **LinkedIn** | ⚠️ Requires permission | Special API access | `sub` |
| **Matrix** | ⚠️ Optional | Homeserver config + user settings | Matrix ID in `sub` |
| **Twitter/X** | ❌ Never | Not provided | `sub` |
| **Reddit** | ❌ Never | Not provided | `preferred_username` |
| **Twitch** | ❌ Never | Not provided | `sub` |

---

## Required Scopes

| Provider | Scopes for Email + Profile |
|----------|----------------------------|
| **Google** | `openid email profile` |
| **Microsoft** | `openid email profile` |
| **GitHub** | `openid email` or `user:email` |
| **GitLab** | `openid email profile` |
| **Discord** | `identify email` |
| **Apple** | `email name` |
| **Matrix** | `openid email profile` (if supported) |

---

## Sub Claim Formats

| Provider | Sub Format | Example | Stable? |
|----------|-----------|---------|---------|
| **Google** | Numeric string | `"108123456789012345678"` | ✅ Yes |
| **Microsoft** | GUID | `"a1b2c3d4-e5f6-..."` | ✅ Yes |
| **GitHub** | Numeric string | `"12345678"` | ✅ Yes |
| **GitLab** | Numeric string | `"987654"` | ✅ Yes |
| **Discord** | Snowflake ID | `"123456789012345678"` | ✅ Yes |
| **Apple** | Opaque string | `"001234.abc123..."` | ✅ Yes |
| **Matrix** | Matrix ID | `"@alice:matrix.org"` | ✅ Yes |
| **Twitter/X** | Numeric string | `"123456789"` | ✅ Yes |

**Note**: All `sub` claims are provider-specific. Use `provider:sub` as composite key for multi-provider support.

---

## Token Endpoints

| Provider | Token Endpoint |
|----------|----------------|
| **Google** | `https://oauth2.googleapis.com/token` |
| **Microsoft** | `https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token` |
| **GitHub** | `https://github.com/login/oauth/access_token` |
| **GitLab** | `https://gitlab.com/oauth/token` |
| **Discord** | `https://discord.com/api/oauth2/token` |
| **Apple** | `https://appleid.apple.com/auth/token` |
| **Matrix** | Varies by homeserver (e.g., `https://matrix.org/.well-known/openid-configuration`) |

---

## JWKS (Public Keys) Endpoints

| Provider | JWKS URI |
|----------|----------|
| **Google** | `https://www.googleapis.com/oauth2/v3/certs` |
| **Microsoft** | `https://login.microsoftonline.com/common/discovery/v2.0/keys` |
| **GitHub** | Not applicable (GitHub uses OAuth 2.0, not full OIDC) |
| **GitLab** | `https://gitlab.com/oauth/discovery/keys` |
| **Discord** | Not documented (verify signature optional) |
| **Apple** | `https://appleid.apple.com/auth/keys` |
| **Matrix** | Check `.well-known/openid-configuration` |

---

## Special Considerations

### Google
- Most reliable email provider
- `email_verified` claim always present
- Supports offline access with refresh tokens

### Microsoft
- Requires tenant ID in endpoints
- Supports both personal and work accounts
- `email` may be missing for guest users

### GitHub
- Not full OIDC (OAuth 2.0 only)
- Requires separate UserInfo API call
- Email only if public or `user:email` scope

### Apple
- **Email only on first login** (critical!)
- Supports relay emails (`@privaterelay.appleid.com`)
- Requires client secret JWT (not static secret)

### Matrix
- Homeserver-specific implementation
- Matrix ID in `sub` is human-readable
- Email availability varies by homeserver config

### Discord
- User can hide email in privacy settings
- `sub` is Discord Snowflake ID
- Supports bot accounts (different flow)

### Twitter/X
- **Never provides email**
- Limited OIDC support
- Consider requiring email collection

---

## Implementation Patterns

### Pattern 1: Email-Only (Simple)

**Use when**: Google/Microsoft only

```python
email = id_token.get("email")
user = get_or_create_user(email)
```

**Pros**: Simple, works for 90% of use cases  
**Cons**: Fails for Matrix, Twitter, Discord

---

### Pattern 2: Email-First with Sub Fallback

**Use when**: Multiple providers including email-less ones

```python
email = id_token.get("email")
if email:
    identity = ("email", email)
else:
    identity = ("sub", f"{provider}:{id_token['sub']}")

user = get_or_create_user_by_identity(*identity)
```

**Pros**: Works for all providers  
**Cons**: More complex database schema

---

### Pattern 3: Multi-Identity Linking

**Use when**: Users need to link multiple provider accounts

```sql
CREATE TABLE user_identities (
    user_id INTEGER,
    provider VARCHAR(50),
    identity_type VARCHAR(20),
    identity_value VARCHAR(255),
    UNIQUE(provider, identity_type, identity_value)
);
```

**Pros**: Full flexibility, cross-provider linking  
**Cons**: Most complex implementation

---

## Testing Checklist

When implementing OIDC authentication:

- [ ] Test with email-based provider (Google)
- [ ] Test with conditional email provider (GitHub with private email)
- [ ] Test with email-less provider (Twitter) if supported
- [ ] Test account linking (same email, different providers)
- [ ] Test first-time login vs returning user
- [ ] Test email verification status
- [ ] Test token expiration and refresh
- [ ] Test revoked access (user revokes in provider settings)
- [ ] Test provider downtime (graceful degradation)
- [ ] Test CSRF protection (state parameter)

---

## Common Pitfalls

1. **Assuming email is always present** → Use fallback to `sub`
2. **Using `sub` alone without provider** → Use `provider:sub` composite key
3. **Not verifying JWT signatures** → Verify in production (optional in dev)
4. **Trusting `email_verified` blindly** → Verify email yourself for critical operations
5. **Storing tokens in localStorage** → Use httpOnly cookies
6. **Not handling token expiration** → Implement refresh token flow
7. **Hardcoding provider endpoints** → Use `.well-known/openid-configuration`
8. **Not validating `state` parameter** → CSRF vulnerability

---

## See Also

- **F001-email-claim-availability.md** - Detailed analysis of email claim availability
- **STANDARD_EXPLAINER.md** - OAuth 2.0 and OIDC fundamentals
- **01-discovery/** - Provider comparisons and recommendations

---

**Last Updated**: 2025-12-30  
**Maintainer**: Research findings from Factumerit OIDC middleware implementation

