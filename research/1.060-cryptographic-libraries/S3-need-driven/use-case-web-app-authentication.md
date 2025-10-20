# Use Case: Web Application Authentication

## Scenario Description

**Application**: SaaS platform with 50,000 active users
**Technology Stack**: Django 4.2, PostgreSQL 14, Redis cache
**Security Requirements**: SOC2 Type II compliance, password breach notification laws

## Concrete Problems to Solve

### 1. Password Storage
- Store user passwords securely in PostgreSQL
- Prevent rainbow table attacks
- Resist brute-force attacks if database compromised
- Support password strength validation

**Current Pain Point**: Django default PBKDF2 may not be sufficient for SOC2 audit requirements.

### 2. Session Token Generation
- Generate cryptographically secure session tokens
- 128-bit entropy minimum
- Prevent session prediction attacks
- Support 100K concurrent sessions

**Current Pain Point**: Need tokens for both cookies and API authentication.

### 3. Password Reset Tokens
- Time-limited password reset links
- Single-use tokens
- Prevent timing attacks during validation
- Email-safe encoding

**Current Pain Point**: Custom implementation has timing vulnerabilities.

### 4. Secure Cookie Signing
- Sign session cookies to prevent tampering
- Support key rotation without mass logout
- Integrate with Django's cookie framework
- HMAC-based integrity

**Current Pain Point**: Need seamless integration with existing Django middleware.

## Precise Requirements

### Password Hashing Requirements

**MUST HAVE**:
- Argon2id or bcrypt algorithm support
- Configurable work factor (adjust difficulty over time)
- Automatic salt generation and storage
- Hash output compatible with Django auth system
- Time cost: 50-250ms per hash on standard hardware
- Memory hard function (resistant to ASIC attacks)

**NICE TO HAVE**:
- Multiple algorithm support for migration
- Parallel hashing for batch operations

**PERFORMANCE TARGET**:
- Hash generation: 100-200ms (login throttling acceptable)
- Hash verification: 100-200ms per attempt
- Throughput: 10 concurrent hashes during peak traffic

**COMPLIANCE**:
- NIST 800-63B compliant password storage
- SOC2 evidence: documented algorithm + parameters

### Session Token Requirements

**MUST HAVE**:
- CSPRNG (cryptographically secure pseudo-random)
- 128+ bit entropy
- URL-safe encoding (Base64 or hex)
- Thread-safe generation
- No external dependencies (network, filesystem)

**PERFORMANCE TARGET**:
- Generate 1000 tokens/second
- Zero collisions in 1B token generation
- <1ms per token

**COMPLIANCE**:
- RFC 4086 compliant randomness
- Predictability: pass NIST SP 800-22 statistical tests

### Password Reset Token Requirements

**MUST HAVE**:
- Time-based expiration (encode timestamp)
- Single-use enforcement (requires state storage)
- Constant-time comparison to prevent timing attacks
- 256-bit entropy minimum
- Include user identifier (encrypted or HMAC)

**NICE TO HAVE**:
- Automatic cleanup of expired tokens
- Rate limiting integration

**PERFORMANCE TARGET**:
- Generate token: <10ms
- Validate token: <10ms
- Support 1000 concurrent resets

### Cookie Signing Requirements

**MUST HAVE**:
- HMAC-SHA256 or better
- Key rotation without invalidating all sessions
- Integration with Django's signing framework
- Maximum message size: 4KB (cookie limit)
- Timestamp inclusion for expiration

**NICE TO HAVE**:
- Compression for large payloads
- Multiple key versioning

**PERFORMANCE TARGET**:
- Sign: <1ms per cookie
- Verify: <1ms per cookie
- 10K operations/second

## Integration Constraints

### Django Integration
- Must work with Django 4.2+ authentication system
- Compatible with `django.contrib.auth.hashers`
- No modification to User model required
- Support Django's `make_password()` and `check_password()`

### Database Constraints
- PostgreSQL `VARCHAR` storage for hashes
- Maximum hash length: 255 characters
- No custom column types required

### Deployment Constraints
- Pure Python or pre-compiled wheels (no C compiler on prod)
- Python 3.11+
- Linux (Ubuntu 22.04 LTS)
- No external dependencies (HSM, key servers)

## Validation Tests Required

### 1. Password Hash Strength Test
```python
# Verify resistance to brute force
import time
hasher = get_password_hasher()
start = time.perf_counter()
hash_result = hasher.hash("test_password")
elapsed = time.perf_counter() - start
assert 0.05 <= elapsed <= 0.3, f"Hash time {elapsed}s outside acceptable range"
assert len(hash_result) <= 255, "Hash too long for database"
```

### 2. Token Uniqueness Test
```python
# Generate 1M tokens, verify no collisions
tokens = set()
for _ in range(1_000_000):
    token = generate_session_token()
    assert token not in tokens, "Token collision detected"
    tokens.add(token)
```

### 3. Timing Attack Resistance Test
```python
# Verify constant-time comparison
import time
valid_token = "abc123"
timings_valid = []
timings_invalid = []

for _ in range(10000):
    start = time.perf_counter()
    compare_constant_time(valid_token, valid_token)
    timings_valid.append(time.perf_counter() - start)

    start = time.perf_counter()
    compare_constant_time(valid_token, "xyz789")
    timings_invalid.append(time.perf_counter() - start)

# Statistical test: means should be similar
import statistics
mean_valid = statistics.mean(timings_valid)
mean_invalid = statistics.mean(timings_invalid)
assert abs(mean_valid - mean_invalid) / mean_valid < 0.1, "Timing leak detected"
```

### 4. Django Integration Test
```python
# Verify seamless Django integration
from django.contrib.auth.hashers import make_password, check_password

hashed = make_password("secure_password")
assert check_password("secure_password", hashed)
assert not check_password("wrong_password", hashed)
assert hashed.startswith("argon2$"), "Wrong hasher selected"
```

## Success Criteria

### Functional Success
- All 4 authentication scenarios working in Django
- Zero timing vulnerabilities in token validation
- Password hashes survive SOC2 audit review
- Session tokens pass NIST randomness tests

### Performance Success
- Password hashing: 50-250ms (measured, not assumed)
- Token generation: >1000/sec sustained
- Cookie signing: <1ms per operation
- No performance degradation under load (tested with locust)

### Integration Success
- Zero Django code changes required
- Drop-in replacement for existing hashers
- Compatible with Django admin, REST framework
- Existing user passwords continue to work

## Library Evaluation Criteria

### Primary Criteria (Deal-Breakers)
1. Provides Argon2id or bcrypt with configurable parameters
2. CSPRNG accessible via simple API
3. Constant-time comparison function available
4. HMAC-SHA256 implementation
5. Django integration support or compatibility

### Secondary Criteria (Scoring)
- Official Django documentation mentions it: +5 points
- Used by other major Django projects: +3 points
- Includes Django-specific helpers: +5 points
- Pure Python fallback available: +2 points
- Last update within 6 months: +3 points

### Negative Criteria (Penalties)
- Requires C compiler for installation: -5 points
- Cryptographic implementation in pure Python (slow): -3 points
- No CSPRNG (must use `secrets` module): -2 points
- Deprecated algorithms (MD5, SHA1 for passwords): -10 points
- CVE in last 2 years: -5 points per CVE

## Expected Library Fit

Based on requirements, ideal library should provide:
- Password hashing: Argon2id/bcrypt with Django integration
- Randomness: CSPRNG or documentation to use `secrets` module
- Comparison: Constant-time functions
- HMAC: Standard implementation

**Hypothesis**: Django's built-in + `argon2-cffi` may be sufficient. Need to validate.
