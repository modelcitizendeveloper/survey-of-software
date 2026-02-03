# Use Case 3: Service-to-Service Authentication

## Scenario Description

A microservices architecture where services need to authenticate requests
from other services. Service A calls Service B's internal API and must
prove its identity. JWTs are used for stateless, cryptographically-verified
service authentication without central auth server on critical path.

## Concrete Requirements (Reality-Based)

### Service Communication Flow
1. Service A needs to call Service B's /internal/process endpoint
2. Service A generates JWT with service identity and short expiration
3. Service A signs JWT with its private key (RS256/ES256)
4. Service A includes JWT in Authorization header
5. Service B validates JWT using Service A's public key
6. Service B extracts service identity and authorizes request
7. Service B processes request and returns response

### Architecture Constraints
- 10-50 services, each service can call 3-10 others
- High throughput: 10,000+ inter-service calls/second
- Low latency: JWT validation must add < 5ms overhead
- Network partitions: Services must work when some services down
- Key rotation: Services rotate keys every 90 days

## Must-Have Requirements (Non-Negotiable)

**R1: Asymmetric Cryptography (RS256 or ES256)**
- Caller signs with private key, receiver validates with public key
- No shared secrets (HS256 won't work - all services would share same key)
- Prefer ES256 (faster, smaller keys) over RS256
- Each service has its own key pair

**R2: Key Distribution**
- Each service publishes its public key at /.well-known/jwks.json
- Services fetch other services' public keys on-demand
- Cache public keys (reduce network calls)
- Refresh on validation failure (handle key rotation)

**R3: Service Identity Claims**
- Service name/ID in "sub" claim (e.g., "user-service")
- Target service in "aud" claim (e.g., "payment-service")
- Short expiration: 60-300 seconds (minimize replay window)
- Request ID in "jti" claim (for debugging/tracing)
- Issued-at timestamp in "iat" claim

**R4: Performance**
- Validate 10,000 tokens/second per service instance
- Signature verification < 5ms (P99 latency)
- Minimal memory overhead (cache public keys, not all tokens)
- No blocking I/O in hot path (async JWKS fetch)

**R5: Fault Tolerance**
- Work with cached keys when JWKS endpoint unreachable
- Graceful degradation (don't cascade failures)
- Circuit breaker for JWKS fetching
- Health check endpoint doesn't require authentication

**R6: Key Rotation**
- Support multiple active keys (old + new during rotation)
- Token specifies kid (key ID) in header
- Validator tries all valid keys from issuer
- Old keys remain valid for grace period (e.g., 24 hours)

### Nice-to-Have Requirements (Desirable)

**R7: Mutual TLS Integration**
- JWT authentication + mTLS transport security
- Verify JWT's "sub" matches TLS client certificate
- Defense in depth

**R8: Request Scopes**
- Token includes scope claim (e.g., "read:users", "write:orders")
- Service validates caller has required scope
- Fine-grained authorization

**R9: Token Chaining**
- Service A calls B, which calls C
- B forwards original caller identity (A) to C
- Audit trail shows complete call chain

## Validation Tests

### Test 1: Generate and Validate with ES256
```python
# Service A generates token
private_key = load_private_key("service-a-private.pem")
payload = {
    "sub": "user-service",
    "aud": "payment-service",
    "exp": now + 300,  # 5 minutes
    "iat": now,
    "jti": generate_request_id()
}
token = library.encode(payload, private_key, algorithm="ES256", kid="key-001")

# Service B validates token
public_key = load_public_key("service-a-public.pem")
decoded = library.decode(
    token,
    public_key,
    algorithms=["ES256"],
    audience="payment-service"
)
assert decoded["sub"] == "user-service"
```

### Test 2: Multiple Keys (Rotation Scenario)
```python
# Service has 2 active keys during rotation
jwks = {
    "keys": [
        {"kid": "key-old", "kty": "EC", ...},  # Still valid for 24h
        {"kid": "key-new", "kty": "EC", ...}   # New key
    ]
}

# Token signed with old key should still validate
old_token = generate_token(kid="key-old")
decoded = library.decode(old_token, jwks=jwks)
assert decoded is not None

# Token signed with new key should validate
new_token = generate_token(kid="key-new")
decoded = library.decode(new_token, jwks=jwks)
assert decoded is not None
```

### Test 3: Performance Under Load
```python
# Pre-generate 10,000 tokens
tokens = [generate_service_token() for _ in range(10000)]
public_key = load_public_key("service-public.pem")

start = time.time()
for token in tokens:
    library.decode(token, public_key, algorithms=["ES256"])
duration = time.time() - start

assert duration < 10.0  # 10,000 validations in < 10s (1000/sec)
avg_latency = duration / 10000 * 1000
assert avg_latency < 5  # < 5ms per validation
```

### Test 4: JWKS Caching and Refresh
```python
# First validation fetches JWKS
token1 = generate_token(kid="key-001")
library.decode(token1, jwks_url="http://service-a/.well-known/jwks.json")

# Second validation uses cache (no network)
token2 = generate_token(kid="key-001")
with no_network_calls():
    library.decode(token2, jwks_url="http://service-a/.well-known/jwks.json")

# Token with unknown kid triggers refresh
token3 = generate_token(kid="key-new")
library.decode(token3, jwks_url="http://service-a/.well-known/jwks.json")
```

### Test 5: Wrong Audience Rejection
```python
# Token for payment-service
token = generate_token(aud="payment-service")

# user-service tries to validate (wrong audience)
with pytest.raises(InvalidAudienceError):
    library.decode(token, public_key, audience="user-service")
```

### Test 6: Expired Short-Lived Token
```python
# Token expired 10 seconds ago (300s TTL, no leeway)
token = generate_token(exp=now - 10)
with pytest.raises(ExpiredTokenError):
    library.decode(token, public_key, leeway=0)
```

## Acceptance Criteria

A library is acceptable for this use case if:
1. All 6 must-have requirements (R1-R6) are satisfied
2. Supports ES256 with EC key pairs (not just RS256)
3. Can validate 1000+ tokens/second per CPU core
4. JWKS fetching and caching work with configurable TTL
5. Supports multiple keys from same issuer (key rotation)
6. No blocking I/O in validation path (async option)

## Edge Cases and Failure Modes

### Edge Case 1: Service Bootstrap
- Service starts up, has no cached public keys
- First request to each downstream service fetches JWKS
- Must handle thundering herd (many services start simultaneously)
- Pre-warm cache on startup? Or lazy load?

### Edge Case 2: Network Partition
- Service A can't reach Service B's JWKS endpoint
- Use cached keys (if available and not expired)
- Fail closed (reject) or fail open (accept)?
- Decision: Fail closed with stale cache allowance (e.g., 1 hour)

### Edge Case 3: Clock Skew Between Services
- Service A's clock is 2 minutes ahead
- Token appears not-yet-valid (iat in future) to Service B
- Need configurable clock skew tolerance (60-120 seconds)

### Edge Case 4: Key Compromise
- Service A's private key is compromised
- Need immediate key rotation (revoke old key)
- Grace period must be short or zero
- May need distributed key revocation list

### Edge Case 5: Circular Dependencies
- Service A calls B, B calls A (rare but possible)
- Each must have the other's public key
- Bootstrap problem: How do they get each other's keys initially?
- Solution: Pre-configure public keys or use service mesh

### Edge Case 6: Token Replay
- Attacker captures valid token, replays it
- Short expiration limits replay window
- JTI claim allows replay detection (requires state)
- Tradeoff: Stateless validation vs replay protection

## Anti-Requirements (Avoid Over-Engineering)

**AR1: Central Authentication Server**
- Don't require online call to auth server per request
- JWT is about distributed authentication
- Avoid designs that defeat stateless validation

**AR2: User Session Management**
- Service tokens are short-lived and request-scoped
- Don't need refresh tokens or session persistence
- Each request generates fresh token

**AR3: Complex Authorization Policies**
- Service-to-service authz is typically simple (identity + audience)
- Don't need role-based access control (RBAC) in JWT
- Application code handles fine-grained authorization

**AR4: Token Revocation Infrastructure**
- Short expiration (5 minutes) makes revocation less critical
- Avoid building distributed revocation list unless required
- Key rotation handles compromised keys

## Implementation Footprint

Ideal library usage for service-to-service authentication:

### Service A (Caller)
```python
import library

PRIVATE_KEY = load_ec_private_key("service-a-private.pem")
SERVICE_NAME = "user-service"
KEY_ID = "key-001"

def create_service_token(target_service: str, request_id: str) -> str:
    payload = {
        "sub": SERVICE_NAME,
        "aud": target_service,
        "exp": datetime.utcnow() + timedelta(seconds=300),
        "iat": datetime.utcnow(),
        "jti": request_id
    }
    return library.encode(payload, PRIVATE_KEY, algorithm="ES256", kid=KEY_ID)

async def call_payment_service(data: dict) -> dict:
    token = create_service_token("payment-service", request_id=generate_id())
    headers = {"Authorization": f"Bearer {token}"}
    response = await http_client.post(
        "http://payment-service/internal/process",
        json=data,
        headers=headers
    )
    return response.json()
```

### Service B (Receiver)
```python
import library
from functools import lru_cache

SERVICE_NAME = "payment-service"
JWKS_CACHE_TTL = 3600  # 1 hour

@lru_cache(maxsize=100)
def get_jwks(service_name: str) -> dict:
    # Cached JWKS fetching with TTL
    url = f"http://{service_name}/.well-known/jwks.json"
    return requests.get(url, timeout=5).json()

def validate_service_token(token: str) -> dict:
    # Extract service name from token (unverified)
    unverified = library.decode_header(token)
    caller_service = unverified.get("iss") or extract_from_token(token)

    # Fetch caller's JWKS
    jwks = get_jwks(caller_service)

    try:
        return library.decode(
            token,
            jwks=jwks,
            algorithms=["ES256"],
            audience=SERVICE_NAME,
            leeway=60  # 60-second clock skew
        )
    except library.ExpiredSignatureError:
        raise Unauthorized("Token expired")
    except library.InvalidAudienceError:
        raise Unauthorized("Invalid audience")
    except library.InvalidTokenError as e:
        raise Unauthorized(f"Invalid token: {e}")

# Middleware
async def authenticate_request(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise Unauthorized("Missing token")

    token = auth_header[7:]  # Remove "Bearer "
    claims = validate_service_token(token)

    # Attach caller identity to request
    request.state.caller_service = claims["sub"]
    request.state.request_id = claims["jti"]
```

Total: ~70 lines of code including caching, error handling, and middleware.
Performance-critical path (validation) is ~15 lines.

## Performance Considerations

ES256 vs RS256 performance:
- ES256 sign: ~0.5ms, verify: ~1ms (with P-256 curve)
- RS256 sign: ~1ms, verify: ~0.1ms (with 2048-bit key)

For service-to-service:
- Caller signs once per request (ES256 0.5ms acceptable)
- Receiver validates once per request (ES256 1ms acceptable)
- Smaller keys (ES256) mean smaller tokens, faster transmission

Conclusion: ES256 is optimal for microservices (balanced performance, smaller tokens).
