# Use Case 2: OAuth 2.0 / OIDC Token Handling

## Scenario Description

A Python application that integrates with external OAuth 2.0 providers
(Google, GitHub, Auth0, Okta) to authenticate users. The app receives
ID tokens (OIDC) and access tokens (OAuth 2.0) and must validate them
according to OIDC spec before trusting claims.

## Concrete Requirements (Reality-Based)

### Integration Flow
1. User clicks "Login with Google/GitHub"
2. App redirects to provider's authorization endpoint
3. User authenticates and consents
4. Provider redirects back with authorization code
5. App exchanges code for tokens (id_token, access_token, refresh_token)
6. App validates id_token signature using provider's public key (RS256/ES256)
7. App extracts user info from validated id_token (sub, email, name)
8. App creates internal session or issues own JWT

### Must-Have Requirements (Non-Negotiable)

**R1: Public Key Validation (RS256/ES256)**
- Decode tokens signed with RSA (RS256) or ECDSA (ES256)
- Fetch provider's public keys from JWKS endpoint (JSON Web Key Set)
- Verify signature using correct public key (match kid from token header)
- Support key rotation (provider changes keys periodically)

**R2: OIDC Claim Validation**
- Verify issuer (iss) matches expected provider URL
- Verify audience (aud) matches our client_id
- Check expiration (exp) with configurable clock skew
- Validate issued_at (iat) is not in future
- Optionally check nonce (prevent replay attacks)

**R3: JWKS Handling**
- Fetch public keys from provider's .well-known/jwks.json endpoint
- Parse JWKS format (array of JWK objects with kid, kty, use, alg, n, e)
- Select correct key based on kid (key ID) from token header
- Cache keys to avoid fetching on every validation
- Refresh cache when key not found (key rotation scenario)

**R4: Multiple Provider Support**
- Configure different issuers (Google, GitHub, Auth0, custom)
- Each provider has different JWKS URL and client_id
- Handle provider-specific quirks (different claim names)
- Validate tokens from any configured provider

**R5: Security**
- RFC 7519 (JWT) and RFC 7517 (JWK) compliance
- No critical CVEs related to signature validation
- Proper error handling (don't leak key material in errors)
- Timing-attack resistant comparisons

### Nice-to-Have Requirements (Desirable)

**R6: Token Introspection**
- Call provider's introspection endpoint to check token status
- Handle revoked tokens (user logged out from provider)
- Optional fallback if signature validation fails

**R7: Automatic JWKS Discovery**
- Given issuer URL, auto-discover JWKS endpoint
- Fetch from .well-known/openid-configuration
- Reduces manual configuration

**R8: Advanced Algorithms**
- PS256/PS384/PS512 (RSA-PSS) support
- ES384/ES512 (different ECDSA curves)
- EdDSA support (modern providers)

**R9: Caching Strategy**
- Configurable JWKS cache TTL
- Background refresh of keys
- Fallback to cached keys if JWKS endpoint down

## Validation Tests

### Test 1: RS256 Token Validation (Real Provider)
```python
# Real Google ID token (structure)
token = "eyJhbGc...valid.google.id_token"
jwks_url = "https://www.googleapis.com/oauth2/v3/certs"

decoded = library.decode(
    token,
    jwks_url=jwks_url,
    audience="my-client-id.apps.googleusercontent.com",
    issuer="https://accounts.google.com",
    algorithms=["RS256"]
)
assert decoded["iss"] == "https://accounts.google.com"
assert decoded["aud"] == "my-client-id.apps.googleusercontent.com"
assert "sub" in decoded  # User ID
assert "email" in decoded
```

### Test 2: JWKS Key Selection
```python
# Token with kid="key-123" in header
# JWKS has multiple keys, must select correct one
token_with_kid = generate_test_token(kid="key-123")
jwks = {
    "keys": [
        {"kid": "key-456", "kty": "RSA", ...},
        {"kid": "key-123", "kty": "RSA", ...},  # Correct key
    ]
}
# Library must use key-123, not key-456
decoded = library.decode(token_with_kid, jwks=jwks)
assert decoded is not None
```

### Test 3: Expiration with Clock Skew
```python
# Token expired 30 seconds ago
# Should accept with 60-second leeway
expired_token = generate_token(exp=now - 30)
decoded = library.decode(expired_token, leeway=60)
assert decoded is not None

# Should reject with 20-second leeway
with pytest.raises(ExpiredTokenError):
    library.decode(expired_token, leeway=20)
```

### Test 4: Invalid Issuer
```python
token = generate_token(iss="https://evil.com")
with pytest.raises(InvalidIssuerError):
    library.decode(
        token,
        expected_issuer="https://accounts.google.com"
    )
```

### Test 5: Missing Required Claims
```python
# OIDC requires sub claim
token_without_sub = generate_token(claims={"email": "user@example.com"})
with pytest.raises(MissingClaimError):
    library.decode(token_without_sub, require_claims=["sub"])
```

### Test 6: JWKS Caching
```python
# First call fetches JWKS from network
start = time.time()
library.decode(token, jwks_url=url)
first_duration = time.time() - start

# Second call uses cache (much faster)
start = time.time()
library.decode(token, jwks_url=url)
cached_duration = time.time() - start

assert cached_duration < first_duration * 0.1  # 10x faster
```

## Acceptance Criteria

A library is acceptable for this use case if:
1. All 5 must-have requirements (R1-R5) are satisfied
2. Can validate real Google/GitHub ID tokens out-of-box
3. JWKS fetching and caching work automatically
4. Supports at least RS256 and ES256 algorithms
5. Provides clear configuration for issuer/audience validation

## Edge Cases and Failure Modes

### Edge Case 1: JWKS Endpoint Unavailable
- Provider's JWKS endpoint returns 500 or times out
- Should use cached keys if available
- Should fail gracefully with clear error if no cache
- Configurable retry strategy

### Edge Case 2: Key Rotation During Validation
- Token signed with key-old (kid="old")
- App cached JWKS has key-old
- Provider rotates keys, removes key-old
- Next token has kid="new"
- Library must detect missing key and refresh JWKS

### Edge Case 3: Multiple Audiences
- Token has aud=["client-1", "client-2"] (array)
- Our client_id is "client-1"
- Library must accept token (one of audiences matches)

### Edge Case 4: Nonce Validation
- OIDC requires nonce to prevent replay attacks
- App generates random nonce, stores in session
- Token must have matching nonce claim
- Library should support nonce validation or allow custom validators

### Edge Case 5: Provider-Specific Claims
- Google uses "email_verified" (boolean)
- GitHub uses "login" instead of "preferred_username"
- Auth0 has custom namespaced claims
- Library shouldn't enforce rigid claim schema

## Anti-Requirements (Avoid Over-Engineering)

**AR1: Full OAuth 2.0 Server**
- Don't need to implement authorization server
- Just need to validate tokens from existing providers
- Avoid libraries that force server-side OAuth flow

**AR2: Token Generation with Public Keys**
- As a client, we don't generate RS256/ES256 tokens
- We only validate them
- Don't need private key management features

**AR3: Every Algorithm Under the Sun**
- RS256 and ES256 cover 95% of providers
- Don't need exotic algorithms (HS512, PS512, EdDSA)
- Can add later if specific provider requires

**AR4: Complex Claim Validation DSL**
- Simple issuer/audience checks are sufficient
- Custom validation can be in application code
- Don't need JSON Schema validation of claims

## Implementation Footprint

Ideal library usage for this use case:

```python
import library

# Configuration for multiple providers
PROVIDERS = {
    "google": {
        "jwks_url": "https://www.googleapis.com/oauth2/v3/certs",
        "issuer": "https://accounts.google.com",
        "client_id": "my-app.apps.googleusercontent.com"
    },
    "github": {
        "jwks_url": "https://token.actions.githubusercontent.com/.well-known/jwks",
        "issuer": "https://token.actions.githubusercontent.com",
        "client_id": "my-github-client-id"
    }
}

def validate_id_token(token: str, provider: str) -> dict:
    config = PROVIDERS[provider]

    try:
        return library.decode(
            token,
            jwks_url=config["jwks_url"],
            audience=config["client_id"],
            issuer=config["issuer"],
            algorithms=["RS256", "ES256"],
            leeway=60  # 60-second clock skew tolerance
        )
    except library.ExpiredSignatureError:
        raise Unauthorized("Token expired")
    except library.InvalidAudienceError:
        raise Unauthorized("Invalid audience")
    except library.InvalidIssuerError:
        raise Unauthorized("Invalid issuer")
    except library.InvalidTokenError as e:
        raise Unauthorized(f"Invalid token: {e}")

def extract_user_info(decoded: dict) -> dict:
    return {
        "user_id": decoded["sub"],
        "email": decoded.get("email"),
        "name": decoded.get("name"),
        "picture": decoded.get("picture")
    }
```

Total: ~40 lines of code including configuration and error handling.
If a library requires significantly more, it's not designed for this use case.

## Integration with Use Case 1

After validating external provider's token, we may issue our own internal JWT:

```python
# Validate provider token
provider_claims = validate_id_token(id_token, "google")

# Issue internal token with our secret (HS256)
internal_token = create_internal_token(
    user_id=provider_claims["sub"],
    email=provider_claims["email"]
)
```

This allows using HS256 for internal API (fast, simple) and RS256/ES256
for external provider validation (required by OIDC).
