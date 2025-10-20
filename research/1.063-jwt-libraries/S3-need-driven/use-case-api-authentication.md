# Use Case 1: REST API Token Authentication

## Scenario Description

A Python backend API (Flask/FastAPI/Django) that issues JWT tokens upon login
and validates them on protected endpoints. Tokens contain user identity and
basic claims (user_id, roles, expiration).

## Concrete Requirements (Reality-Based)

### Authentication Flow
1. User submits credentials (username/password)
2. Backend validates credentials against database
3. Backend issues JWT with: user_id, roles, issued_at, expires_at
4. Client stores token (localStorage/sessionStorage)
5. Client includes token in Authorization header for API calls
6. Backend validates token signature and expiration on each request
7. Backend extracts user_id from validated token for authorization

### Must-Have Requirements (Non-Negotiable)

**R1: Token Generation**
- Create JWT with custom claims (user_id: int, roles: list[str])
- Set expiration time (configurable, typically 15-60 minutes)
- Use HS256 algorithm (symmetric key, sufficient for single-service API)
- Encode token as compact string (header.payload.signature)

**R2: Token Validation**
- Verify HMAC signature using shared secret
- Check expiration time (exp claim) against current time
- Raise exception on invalid signature or expired token
- Extract claims from validated token as dictionary

**R3: Security**
- Constant-time signature comparison (timing attack prevention)
- No critical CVEs in last 2 years
- Proper handling of malformed tokens (no crashes)
- RFC 7519 compliant (standard JWT format)

**R4: Performance**
- Validate 1000+ tokens/second on standard hardware
- Minimal CPU overhead per validation (< 1ms)
- No unnecessary cryptographic operations

**R5: Integration**
- Python 3.8+ compatibility
- No heavy dependencies (avoid pulling in entire OAuth frameworks)
- Simple API: encode(payload, secret) and decode(token, secret)
- Type hints for IDE support

### Nice-to-Have Requirements (Desirable)

**R6: Enhanced Validation**
- Audience (aud) claim validation
- Issuer (iss) claim validation
- Not-before (nbf) claim validation
- Custom claim validators

**R7: Developer Experience**
- Clear error messages (distinguish between expired vs invalid signature)
- Good documentation with examples
- Active community (bug fixes, security updates)

**R8: Additional Algorithms**
- RS256 support (for future multi-service scenarios)
- ES256 support (for mobile app integration)

## Validation Tests

### Test 1: Basic Encode/Decode
```python
secret = "my-secret-key"
payload = {"user_id": 123, "roles": ["user", "admin"], "exp": now + 3600}
token = library.encode(payload, secret)
decoded = library.decode(token, secret)
assert decoded["user_id"] == 123
assert decoded["roles"] == ["user", "admin"]
```

### Test 2: Expiration Validation
```python
expired_payload = {"user_id": 123, "exp": now - 3600}  # 1 hour ago
token = library.encode(expired_payload, secret)
with pytest.raises(ExpiredTokenError):
    library.decode(token, secret)
```

### Test 3: Invalid Signature
```python
token = library.encode(payload, "secret1")
with pytest.raises(InvalidSignatureError):
    library.decode(token, "secret2")
```

### Test 4: Malformed Token
```python
with pytest.raises(InvalidTokenError):
    library.decode("not.a.valid.jwt", secret)
with pytest.raises(InvalidTokenError):
    library.decode("only-two-parts.here", secret)
```

### Test 5: Performance
```python
tokens = [library.encode({"user_id": i}, secret) for i in range(1000)]
start = time.time()
for token in tokens:
    library.decode(token, secret)
duration = time.time() - start
assert duration < 1.0  # 1000 validations in < 1 second
```

## Acceptance Criteria

A library is acceptable for this use case if:
1. All 5 must-have requirements (R1-R5) are satisfied
2. At least 2 validation tests pass without modification
3. API requires <= 5 lines of code for encode + decode
4. No dependencies on OAuth/OIDC frameworks (bloat)
5. Actively maintained (commit in last 6 months)

## Edge Cases and Failure Modes

### Edge Case 1: Clock Skew
- Backend clock is 30 seconds ahead of token generation server
- Token appears expired but shouldn't be
- Need configurable leeway (e.g., 30-60 second tolerance)

### Edge Case 2: Long-Running Requests
- Request starts with valid token
- Token expires during processing (long database query)
- Should token be validated at start or throughout?
- Decision: Validate at entry, accept slight expiration overage

### Edge Case 3: Token Revocation
- User logs out but token still valid until expiration
- JWT is stateless - can't revoke without additional infrastructure
- Not a library problem - requires blacklist or short expiration

### Edge Case 4: Key Rotation
- Secret key needs periodic rotation
- Need to support multiple keys (old + new) during transition
- Decode should try multiple keys until one succeeds

## Anti-Requirements (Avoid Over-Engineering)

**AR1: Public Key Infrastructure**
- Don't need RS256/ES256 for single-service API
- Adds complexity of key management, certificate chains
- HS256 with strong secret is sufficient

**AR2: OAuth 2.0 Features**
- Don't need grant types, authorization flows, token introspection
- Just need basic JWT encode/decode
- Avoid libraries that force OAuth patterns

**AR3: JSON Web Encryption (JWE)**
- Don't need encrypted payload
- JWT signature prevents tampering
- Sensitive data shouldn't be in token anyway

**AR4: Advanced Claim Validation**
- Don't need complex claim validation DSL
- Simple checks (expiration, signature) are sufficient
- Custom validation can be in application code

## Implementation Footprint

Ideal library usage for this use case:

```python
import library

SECRET = "strong-random-secret"

def create_token(user_id: int, roles: list[str]) -> str:
    payload = {
        "user_id": user_id,
        "roles": roles,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return library.encode(payload, SECRET, algorithm="HS256")

def validate_token(token: str) -> dict:
    try:
        return library.decode(token, SECRET, algorithms=["HS256"])
    except library.ExpiredSignatureError:
        raise Unauthorized("Token expired")
    except library.InvalidTokenError:
        raise Unauthorized("Invalid token")
```

Total: ~15 lines of code. If a library requires significantly more,
it's either over-engineered or poorly designed for this use case.
