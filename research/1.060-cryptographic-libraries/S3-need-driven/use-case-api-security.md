# Use Case: API Security

## Scenario Description

**Application**: Public REST API for financial data aggregation
**Scale**: 10,000 API clients, 1M requests/day
**Technology Stack**: FastAPI, Redis rate limiting, PostgreSQL
**Security Requirements**: PCI-DSS compliance, SOC2 Type II, OAuth 2.0 + JWT

## Concrete Problems to Solve

### 1. JWT Token Generation and Validation
- Issue short-lived access tokens (15 min expiry)
- Refresh tokens with 30-day expiry
- RS256 signing (asymmetric keys for distributed validation)
- Claims: user ID, permissions, token type, issuer
- Prevent token reuse after revocation

**Current Pain Point**: Need to verify tokens in multiple microservices without database lookup on every request.

### 2. API Request Signature Verification
- Clients sign requests with HMAC-SHA256
- Prevent replay attacks (timestamp + nonce)
- Support key rotation (multiple active keys)
- Webhook signature generation (server-to-client callbacks)
- 5000 signature verifications/second during peak

**Current Pain Point**: Custom implementation has timing vulnerabilities allowing signature forgery.

### 3. TLS/HTTPS Certificate Management
- Generate CSR (certificate signing request) for Let's Encrypt
- Validate certificate chains
- Pin critical certificates (prevent MITM)
- Automatic certificate renewal
- Support mutual TLS (client certificates) for sensitive endpoints

**Current Pain Point**: Manual certificate management, need automation.

### 4. OAuth 2.0 PKCE Flow
- Authorization code generation
- Code verifier and challenge (SHA-256)
- State parameter generation (CSRF protection)
- Token exchange validation
- Support for mobile/SPA clients

**Current Pain Point**: Implementing secure PKCE without rolling own crypto.

## Precise Requirements

### JWT Token Requirements

**MUST HAVE**:
- RS256 algorithm (RSA + SHA-256 signature)
- Support HS256 for internal services
- ES256 support (ECDSA, smaller keys) for future
- Key ID (kid) header for key rotation
- Standard claims: iss, sub, aud, exp, iat, jti
- Custom claims: user permissions, tenant ID
- Token validation: signature, expiry, issuer, audience

**NICE TO HAVE**:
- JWE support (encrypted tokens for sensitive data)
- JWK (JSON Web Key) generation/parsing
- Token refresh logic (reissue with extended expiry)

**PERFORMANCE TARGET**:
- Token generation: <10ms (RSA-2048 signing)
- Token validation: <5ms (RSA-2048 verification)
- Throughput: 1000 tokens/sec generation, 5000/sec validation
- Key loading: <50ms on startup

**COMPLIANCE**:
- RFC 7519 (JWT standard)
- RFC 7515 (JWS - JSON Web Signature)
- PCI-DSS: strong cryptography for authentication
- SOC2: secure session management

### API Signature Requirements

**MUST HAVE**:
- HMAC-SHA256 signature generation/verification
- Canonical request format (method + path + body + timestamp)
- Constant-time signature comparison (prevent timing attacks)
- Signature in header: `Authorization: Signature v1, keyId=..., signature=...`
- Timestamp validation (reject requests >5 minutes old)
- Nonce tracking (prevent replay within 5-minute window)

**NICE TO HAVE**:
- Multiple signature algorithms (HMAC-SHA512)
- Webhook signature helpers
- Request signing middleware for client SDK

**PERFORMANCE TARGET**:
- Sign request: <1ms
- Verify signature: <1ms with constant-time comparison
- Throughput: 5000 verifications/sec
- Nonce cache: Redis lookup <2ms

**COMPLIANCE**:
- RFC 6234 (SHA-256/384/512 algorithms)
- PCI-DSS: prevent replay attacks
- Constant-time comparison per OWASP guidelines

### TLS Certificate Requirements

**MUST HAVE**:
- Generate RSA-2048 or ECDSA P-256 private keys
- Create CSR with subject alternative names (SANs)
- Parse X.509 certificates (extract expiry, subject, issuer)
- Verify certificate chains up to trusted root
- Extract public key from certificate
- PEM encoding/decoding

**NICE TO HAVE**:
- OCSP (online certificate status protocol) checking
- Certificate pinning utilities
- Mutual TLS (mTLS) client certificate handling
- Let's Encrypt ACME protocol integration

**PERFORMANCE TARGET**:
- Key generation: <500ms (acceptable for infrequent operation)
- CSR generation: <100ms
- Certificate parsing: <10ms
- Chain verification: <50ms

**COMPLIANCE**:
- RFC 5280 (X.509 certificate standard)
- TLS 1.2 minimum (TLS 1.3 preferred)
- PCI-DSS: strong cryptography for transmission

### OAuth PKCE Requirements

**MUST HAVE**:
- Code verifier generation (43-128 characters, URL-safe)
- Code challenge generation (SHA-256 hash of verifier)
- Challenge method: S256 (plain method not acceptable)
- State parameter generation (CSRF protection)
- Authorization code generation (single-use)
- Constant-time code comparison

**NICE TO HAVE**:
- Complete OAuth 2.0 flow helpers
- Token refresh utilities
- Scope validation

**PERFORMANCE TARGET**:
- Code verifier generation: <10ms
- Code challenge calculation: <5ms
- Authorization code validation: <10ms
- Throughput: 100 OAuth flows/sec

**COMPLIANCE**:
- RFC 7636 (PKCE specification)
- RFC 6749 (OAuth 2.0 framework)
- OWASP OAuth security best practices

## Integration Constraints

### FastAPI Integration
- Dependency injection for JWT validation
- Middleware for request signature verification
- Exception handlers for auth failures (401, 403)
- OpenAPI schema security definitions
- Support for async request handlers

### Redis Integration
- Nonce storage for replay prevention (5-minute TTL)
- Revoked token list (until expiry)
- Rate limiting by client ID (sliding window)
- Session storage for OAuth flows

### Key Storage Constraints
- Private keys stored in environment variables (initial)
- Public keys served via JWKS endpoint (/.well-known/jwks.json)
- Key rotation: generate new key, publish both, retire old after 24h
- Future: HSM or KMS integration

### Client SDK Constraints
- Python client library for API signature generation
- JavaScript SDK for browser-based OAuth PKCE
- Example code for curl/Postman users
- Clear error messages for signature failures

## Validation Tests Required

### 1. JWT Generation and Validation
```python
# Test complete JWT lifecycle
from datetime import datetime, timedelta
import jwt

private_key = load_rsa_private_key()
public_key = load_rsa_public_key()

# Generate token
payload = {
    "sub": "user_12345",
    "iss": "https://api.example.com",
    "aud": "api_clients",
    "exp": datetime.utcnow() + timedelta(minutes=15),
    "iat": datetime.utcnow(),
    "permissions": ["read:data", "write:data"]
}

token = jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": "key_v1"})

# Validate token
decoded = jwt.decode(token, public_key, algorithms=["RS256"], audience="api_clients")
assert decoded["sub"] == "user_12345"
assert decoded["permissions"] == ["read:data", "write:data"]

# Test expiry
expired_token = jwt.encode(
    {**payload, "exp": datetime.utcnow() - timedelta(minutes=1)},
    private_key,
    algorithm="RS256"
)
try:
    jwt.decode(expired_token, public_key, algorithms=["RS256"])
    assert False, "Expired token accepted"
except jwt.ExpiredSignatureError:
    pass  # Expected
```

### 2. Request Signature Verification
```python
# Test HMAC signature with timing attack resistance
import hmac
import hashlib
import time

def sign_request(method, path, body, timestamp, secret):
    message = f"{method}\n{path}\n{body}\n{timestamp}"
    signature = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature

def verify_signature_constant_time(expected, actual):
    # Must use constant-time comparison
    return hmac.compare_digest(expected, actual)

secret = "api_secret_key_12345"
signature = sign_request("POST", "/api/v1/transaction", '{"amount":100}', "1640000000", secret)

# Verify timing is constant
timings_valid = []
timings_invalid = []

for _ in range(10000):
    start = time.perf_counter()
    result = verify_signature_constant_time(signature, signature)
    timings_valid.append(time.perf_counter() - start)
    assert result

for _ in range(10000):
    start = time.perf_counter()
    result = verify_signature_constant_time(signature, "wrong_signature_xyz")
    timings_invalid.append(time.perf_counter() - start)
    assert not result

# Statistical test
import statistics
assert abs(statistics.mean(timings_valid) - statistics.mean(timings_invalid)) < 1e-7
```

### 3. Certificate Chain Validation
```python
# Test X.509 certificate parsing and validation
from cryptography import x509
from cryptography.hazmat.backends import default_backend

# Load certificate chain
cert_pem = open("/path/to/cert.pem", "rb").read()
cert = x509.load_pem_x509_certificate(cert_pem, default_backend())

# Verify not expired
from datetime import datetime
now = datetime.utcnow()
assert cert.not_valid_before <= now <= cert.not_valid_after, "Certificate expired"

# Extract subject
subject = cert.subject
common_name = subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
assert common_name == "api.example.com"

# Verify signature with issuer public key
issuer_cert = load_issuer_certificate()
issuer_public_key = issuer_cert.public_key()
issuer_public_key.verify(
    cert.signature,
    cert.tbs_certificate_bytes,
    # Signature algorithm parameters
)
```

### 4. OAuth PKCE Flow
```python
# Test PKCE code verifier and challenge
import secrets
import hashlib
import base64

# Generate code verifier (client)
code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
assert 43 <= len(code_verifier) <= 128

# Generate code challenge (client sends to server)
challenge_bytes = hashlib.sha256(code_verifier.encode()).digest()
code_challenge = base64.urlsafe_b64encode(challenge_bytes).decode('utf-8').rstrip('=')

# Server stores code_challenge
# Later, client sends code_verifier with authorization code

# Verify (server)
received_verifier = code_verifier
computed_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(received_verifier.encode()).digest()
).decode('utf-8').rstrip('=')

assert computed_challenge == code_challenge, "PKCE verification failed"
```

### 5. Performance Benchmark
```python
# Measure JWT validation throughput
import time

tokens = [generate_test_token() for _ in range(5000)]

start = time.perf_counter()
for token in tokens:
    jwt.decode(token, public_key, algorithms=["RS256"])
elapsed = time.perf_counter() - start

throughput = len(tokens) / elapsed
assert throughput >= 1000, f"JWT validation too slow: {throughput:.0f} tokens/sec"
print(f"JWT validation: {throughput:.0f} tokens/sec")
```

## Success Criteria

### Functional Success
- JWT tokens work across 3 microservices without shared database
- API signature verification prevents all replay attacks (tested)
- Certificate renewal automated with zero downtime
- OAuth PKCE flow tested with mobile app and SPA

### Performance Success
- JWT validation: 1000+ tokens/sec measured on production hardware
- Signature verification: 5000+ ops/sec sustained load
- Token generation: <10ms p99 latency
- No performance degradation under DDoS simulation

### Security Success
- Zero timing vulnerabilities in signature comparison (statistically verified)
- Expired tokens rejected 100% of time (fuzz tested)
- Replay attacks prevented (tested with replayed requests)
- Key rotation completes without invalidating valid tokens

### Compliance Success
- PCI-DSS requirement 4 satisfied (strong cryptography documented)
- SOC2 CC6.1 evidence (logical access controls via JWT)
- OAuth 2.0 RFC compliance verified with test suite
- Penetration test report: no cryptographic vulnerabilities

## Library Evaluation Criteria

### Primary Criteria (Deal-Breakers)
1. RS256/ES256 JWT support with standard claims
2. HMAC-SHA256 with constant-time comparison
3. X.509 certificate parsing and chain validation
4. CSR generation for TLS certificates
5. OAuth PKCE helper functions or examples

### Secondary Criteria (Scoring)
- FastAPI integration examples: +5 points
- Built-in key rotation support: +5 points
- JWK/JWKS generation: +3 points
- Async/await support: +3 points
- ACME protocol support: +2 points

### Negative Criteria (Penalties)
- Only supports HS256 (symmetric JWT): -5 points
- No constant-time comparison: -10 points (critical)
- Custom JWT format (non-standard): -10 points
- No certificate validation: -5 points
- Synchronous-only API: -3 points

## Expected Library Fit

Based on requirements, ideal library should provide:
- JWT: Complete RS256/ES256 implementation with validation
- HMAC: Constant-time comparison built-in
- TLS: CSR generation, certificate parsing, chain verification
- OAuth: At minimum, PKCE helper functions

**Hypothesis**: `cryptography` library for low-level primitives + `PyJWT` for JWT implementation. Need to validate integration and performance.
