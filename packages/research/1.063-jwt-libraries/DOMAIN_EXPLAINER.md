# JWT Authentication: Technical Concepts and Domain Knowledge

## Document Purpose

This document provides technical explanations of JSON Web Token (JWT) concepts for business stakeholders, CTOs, product managers, and technical decision-makers. It serves as a glossary and conceptual framework to understand JWT authentication independent of any specific library or implementation.

**This document explains**: What JWT is, how it works, security considerations, and architectural patterns.

**This document does NOT**: Compare specific libraries, provide implementation recommendations, or advocate for particular solutions.

---

## 1. Technical Concept Definitions

### What is JWT?

JSON Web Token (JWT) is an open standard (RFC 7519) for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed.

**JWT Structure**: Three parts separated by dots (.)

```
header.payload.signature
```

**Example**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

**Header**: Contains metadata about the token
- Algorithm used (e.g., HS256, RS256)
- Token type (JWT)

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload**: Contains claims (statements about an entity)
- User identity
- Permissions/roles
- Expiration time
- Custom application data

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622
}
```

**Signature**: Ensures the token hasn't been tampered with
- Created by encoding header + payload + secret key
- Verified using the same secret (HS256) or public key (RS256)

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

### Claims

Claims are statements about an entity (typically the user) and additional metadata. Three types exist:

**Registered Claims**: Standard claims defined by JWT specification
- `iss` (issuer): Who created the token
- `sub` (subject): Who the token is about (usually user ID)
- `aud` (audience): Who the token is intended for
- `exp` (expiration time): When the token expires (Unix timestamp)
- `nbf` (not before): Token is not valid before this time
- `iat` (issued at): When the token was created
- `jti` (JWT ID): Unique identifier for the token

**Public Claims**: Custom claims registered in IANA JWT registry or collision-resistant names
- Example: `https://example.com/claims/roles`

**Private Claims**: Custom claims agreed upon between parties
- Example: `role`, `permissions`, `tenant_id`

### Signature Algorithms

JWT supports multiple cryptographic algorithms for signing tokens.

**HS256 (HMAC with SHA-256)**: Symmetric algorithm
- Same secret key used to sign and verify
- Faster and simpler
- Both issuer and verifier must have the secret
- Cannot delegate verification to third parties securely
- Key size: 256 bits minimum

**RS256 (RSA with SHA-256)**: Asymmetric algorithm
- Private key signs, public key verifies
- Public key can be shared openly
- Enables distributed verification
- Computationally more expensive
- Key size: 2048 bits minimum (recommended)

**ES256 (ECDSA with SHA-256)**: Asymmetric algorithm
- Elliptic curve cryptography
- Smaller keys than RSA with equivalent security
- Faster than RSA
- Public key verification like RS256
- Key size: 256 bits

**PS256 (RSA-PSS with SHA-256)**: Asymmetric algorithm
- Probabilistic signature scheme
- More secure than PKCS#1 v1.5 padding (RS256)
- Requires more recent cryptographic libraries

**Algorithm Selection Criteria**:
- **HS256**: Single server/monolith, simple architecture
- **RS256**: Microservices, third-party verification needed
- **ES256**: Mobile/IoT, performance-critical applications
- **PS256**: High-security requirements, modern infrastructure

### Token Types

**Access Token**: Short-lived token for API access
- Typical lifetime: 15 minutes to 1 hour
- Contains permissions/scopes
- Sent with each API request
- Should be treated as opaque by clients

**Refresh Token**: Long-lived token to obtain new access tokens
- Typical lifetime: Days to months
- Not sent with every request
- Used only at token endpoint
- Can be revoked server-side
- Often stored securely (not in JWT format)

**ID Token**: Contains user identity information (OpenID Connect)
- Used for authentication, not authorization
- Contains user profile claims
- Consumed by the client application
- Should not be sent to APIs

### JWKS (JSON Web Key Set)

A JWKS is a set of public keys used to verify JWT signatures. Enables key rotation and distributed verification.

**Structure**:
```json
{
  "keys": [
    {
      "kty": "RSA",
      "kid": "key-id-1",
      "use": "sig",
      "n": "modulus-base64url",
      "e": "exponent-base64url"
    }
  ]
}
```

**Key Fields**:
- `kty` (key type): RSA, EC, oct
- `kid` (key ID): Identifier to match with token header
- `use` (public key use): sig (signature) or enc (encryption)
- `n`, `e`: RSA public key parameters

**Usage Pattern**:
1. Identity provider publishes JWKS at `/.well-known/jwks.json`
2. Application fetches JWKS on startup or periodically
3. For each JWT, match `kid` in header to key in JWKS
4. Verify signature using the matched public key

---

## 2. Technology Landscape Overview

### JWT vs Session Cookies

**Session Cookies (Stateful)**:
- Server stores session data in memory/database
- Cookie contains only session ID
- Server lookups required for each request
- Easy to revoke (delete server session)
- Scales vertically (sticky sessions or shared storage)
- Simple to implement

**JWT (Stateless)**:
- All data contained in token
- No server-side storage required
- Self-contained authorization
- Difficult to revoke immediately
- Scales horizontally (no shared state)
- Requires cryptographic operations

**Hybrid Approach**:
- JWT for authentication
- Session storage for revocation list
- Best of both worlds with added complexity

### Stateless Authentication Architecture

JWT enables stateless authentication where each request contains all necessary information.

**Benefits**:
- No session storage required
- Easy horizontal scaling
- Microservices can verify independently
- Reduced database load
- Works across domains (CORS-friendly)

**Challenges**:
- Token size overhead (sent with every request)
- Cannot immediately revoke tokens
- Must wait for expiration
- Requires secure key management
- Clock synchronization for expiration

**Typical Flow**:
1. User logs in with credentials
2. Server validates credentials
3. Server issues JWT with claims
4. Client stores JWT (localStorage, sessionStorage, cookie)
5. Client sends JWT with each API request
6. Server validates signature and claims
7. Server processes request if valid

### OAuth 2.0 / OpenID Connect Integration

**OAuth 2.0**: Authorization framework
- Grants access to resources
- Uses access tokens (often JWT)
- Four grant types: authorization code, implicit, client credentials, password
- Focus: What can you access?

**OpenID Connect**: Authentication layer on top of OAuth 2.0
- Verifies user identity
- Uses ID tokens (always JWT)
- Adds user info endpoint
- Focus: Who are you?

**JWT's Role**:
- Access tokens may be JWT (not required by spec)
- ID tokens must be JWT (required by OIDC spec)
- Enables distributed verification without calling auth server

**Example OIDC Flow**:
1. User authenticates with identity provider (Auth0, Okta, etc.)
2. Provider issues ID token (JWT) and access token
3. Client extracts user info from ID token
4. Client uses access token for API calls
5. APIs verify access token signature and claims

### Microservices Authentication Patterns

**Pattern 1: Shared Secret (HS256)**
- All services share the same symmetric key
- Each service can verify tokens independently
- Risk: Key compromise affects entire system
- Suitable for: Trusted internal services

**Pattern 2: Public Key Infrastructure (RS256/ES256)**
- Auth service holds private key
- All services have public key (via JWKS)
- Services verify without calling auth service
- Key rotation via JWKS updates
- Suitable for: Distributed systems, third-party services

**Pattern 3: API Gateway Verification**
- Gateway verifies JWT at perimeter
- Downstream services trust gateway
- Simplifies service code
- Single point of failure
- Suitable for: Simple microservice architectures

**Pattern 4: Token Exchange**
- Service-to-service calls get new tokens
- Each service validates incoming tokens
- Enables fine-grained authorization
- More complex but more secure
- Suitable for: Zero-trust architectures

### SPA Authentication Flows

**Traditional Flow (OAuth 2.0 Implicit)**:
- Browser-based apps receive tokens directly
- Tokens exposed to JavaScript
- Deprecated due to security concerns

**Current Best Practice (Authorization Code + PKCE)**:
- Browser initiates auth flow
- Auth server issues authorization code
- Exchange code for tokens at backend
- Backend stores refresh token
- Frontend receives access token only
- PKCE prevents authorization code interception

**Storage Considerations**:
- **localStorage**: Vulnerable to XSS attacks
- **sessionStorage**: Cleared on tab close, still XSS-vulnerable
- **httpOnly cookies**: Not accessible to JavaScript, CSRF protection needed
- **Memory only**: Most secure, lost on refresh

---

## 3. Build vs Buy Economics Fundamentals

### Why Use JWT Libraries vs Rolling Your Own

**Cryptographic Complexity**:
- Signature algorithms are complex to implement correctly
- Timing attacks can leak keys
- Padding oracle attacks on encryption
- Constant-time comparisons required
- Libraries have been audited and battle-tested

**Standards Compliance**:
- RFC 7519 (JWT)
- RFC 7515 (JWS - JSON Web Signature)
- RFC 7516 (JWE - JSON Web Encryption)
- RFC 7517 (JWK - JSON Web Key)
- RFC 7518 (Algorithms)
- Proper libraries implement all nuances

**Example Complexity**: Base64URL encoding is NOT standard Base64
```
Standard Base64: Uses +, /, =
Base64URL: Uses -, _, no padding
```

Implementing this incorrectly breaks interoperability.

### Security Risks of DIY JWT Implementations

**Common Mistakes**:

1. **Algorithm Confusion**: Accepting `alg: none`
   - Attacker removes signature
   - Changes payload freely
   - Server accepts unsigned token

2. **Key Confusion**: Treating RS256 public key as HS256 secret
   - Attacker signs with public key
   - Server verifies with same public key
   - Completely bypasses security

3. **Improper Validation**: Not checking expiration, audience, issuer
   - Expired tokens accepted
   - Tokens for different apps accepted
   - Replay attacks succeed

4. **Weak Secrets**: Short or predictable HS256 keys
   - Brute force attacks
   - Rainbow table attacks
   - Key must be at least 256 bits random

5. **Insecure Storage**: Embedding secrets in code
   - Source code leaks
   - Version control exposure
   - Difficult to rotate

**Real-World Cost**:
- Auth0 incident (2020): Algorithm confusion in custom parser
- Okta incident (2019): Token validation bypass
- Many organizations with unreported breaches

**Library Benefits**:
- Peer-reviewed code
- Security advisories and patches
- Community testing
- Professional audits
- Standard test vectors

### Standards Compliance (RFCs)

**RFC 7519 (JWT)**: Token format and claims
- Defines structure and semantics
- Registered claim definitions
- Processing rules

**RFC 7515 (JWS)**: Digital signatures
- HMAC, RSA, ECDSA algorithms
- Serialization formats
- Signature generation and validation

**RFC 7516 (JWE)**: Encryption
- Encrypted JWT for confidentiality
- Key management algorithms
- Content encryption algorithms

**RFC 7517 (JWK)**: Key representation
- JSON format for cryptographic keys
- Key sets (JWKS)
- Parameters for different key types

**RFC 7518 (Algorithms)**: Cryptographic algorithms
- Mandatory and optional algorithms
- Algorithm identifiers
- Security considerations

**Why Compliance Matters**:
- Interoperability with identity providers
- Security guarantees from specifications
- Legal and regulatory requirements
- Vendor independence
- Future-proofing

### Integration with Identity Providers

**Common Providers**:
- Auth0
- Okta
- AWS Cognito
- Azure AD
- Google Identity
- Keycloak (self-hosted)

**JWT Integration Points**:

1. **OIDC Discovery**: Provider publishes configuration
   ```
   https://provider.com/.well-known/openid-configuration
   ```

2. **JWKS Endpoint**: Public keys for verification
   ```
   https://provider.com/.well-known/jwks.json
   ```

3. **Token Endpoint**: Exchange code for tokens
   ```
   POST https://provider.com/oauth/token
   ```

4. **Token Introspection**: Validate token status
   ```
   POST https://provider.com/oauth/introspect
   ```

**Library Requirements**:
- JWKS fetching and caching
- Key rotation handling
- Clock skew tolerance
- Issuer and audience validation
- OIDC claims parsing

**Cost Considerations**:
- Provider pricing (MAUs, features)
- Vendor lock-in risks
- Data residency requirements
- SLA guarantees
- Integration complexity

### When NOT to Use JWT

**Use Session-Based Auth Instead When**:

1. **Immediate Revocation Required**
   - Banking applications
   - Admin dashboards
   - High-security environments
   - User can logout and access is immediately revoked

2. **Token Size is Problematic**
   - Mobile apps with limited bandwidth
   - Embedded devices
   - Hundreds of permissions/claims needed
   - Session ID is much smaller (16-32 bytes)

3. **All Requests to Same Server**
   - Monolithic applications
   - Single backend server
   - No microservices
   - Session storage is simpler

4. **Regulatory Compliance Issues**
   - Audit trails required for every access
   - GDPR right to erasure (hard with JWT)
   - Data minimization requirements
   - Sessions allow centralized control

5. **Team Lacks Cryptographic Expertise**
   - Small teams
   - No security specialists
   - Simple session cookies are safer
   - Fewer ways to misconfigure

**Alternative Technologies**:
- Secure session cookies with CSRF protection
- Server-side sessions with Redis/Memcached
- Database-backed sessions
- Paseto (Platform-Agnostic SEcurity TOkens) - simpler alternative to JWT

**Hybrid Approaches**:
- JWT for authentication, session for authorization
- JWT with revocation list (defeats some stateless benefits)
- Short-lived JWT + long-lived refresh token

---

## 4. Common Misconceptions with Technical Explanations

### "JWT is Encrypted"

**Misconception**: JWT keeps data secret from clients.

**Reality**: Standard JWT is signed, NOT encrypted.
- Base64URL encoding is reversible
- Anyone can decode and read the payload
- Signature only proves authenticity and integrity

**Demonstration**:
```bash
# Anyone can decode this without the secret
echo "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIn0" | base64 -d
# Output: {"sub":"1234567890","name":"John Doe"}
```

**When Encryption is Needed**: Use JWE (JSON Web Encryption)
- Requires additional encryption layer
- More complex to implement
- Performance overhead
- Most use cases don't need it

**Best Practice**: Never put sensitive data (passwords, credit cards, SSNs) in JWT payload.

### "JWT is Secure by Default"

**Misconception**: Using JWT automatically makes authentication secure.

**Reality**: JWT is only secure with proper validation.

**Required Validations**:
1. Signature verification (cryptographic check)
2. Expiration check (`exp` claim)
3. Not-before check (`nbf` claim)
4. Issuer validation (`iss` claim matches expected)
5. Audience validation (`aud` claim matches expected)
6. Algorithm validation (reject unexpected algorithms)

**Example Vulnerability**: Missing audience check
```python
# Insecure: Accepts tokens from any audience
token = jwt.decode(token_string, key, algorithms=['RS256'])

# Secure: Verifies audience
token = jwt.decode(
    token_string,
    key,
    algorithms=['RS256'],
    audience='https://api.myapp.com'
)
```

**Attack Scenario**:
- Attacker gets valid JWT from App A
- Uses same JWT on App B (different audience)
- Without audience check, App B accepts it
- Unauthorized access granted

### "HS256 is Always Sufficient"

**Misconception**: Symmetric signing (HS256) works for all scenarios.

**Reality**: HS256 has significant limitations in distributed systems.

**Limitations**:

1. **Shared Secret Problem**:
   - Every verifier needs the secret
   - Secret can create tokens too
   - No separation of concerns
   - One compromise = full system compromise

2. **Third-Party Verification**:
   - Cannot give secret to untrusted parties
   - Mobile apps can't securely verify
   - Partners can't verify tokens
   - Requires calling auth server

3. **Key Rotation Complexity**:
   - All services must update simultaneously
   - Graceful rotation is difficult
   - Downtime or dual-key period required

**When HS256 is Appropriate**:
- Single application server
- Trusted internal services only
- Simpler key management acceptable
- Performance critical (HS256 is faster)

**When RS256 is Required**:
- Microservices architecture
- Third-party API consumers
- Mobile/SPA applications verify tokens
- Multiple applications share auth
- Key rotation without coordination

### "Tokens Can't be Revoked"

**Misconception**: Once issued, JWT remains valid until expiration.

**Reality**: Multiple revocation strategies exist, each with tradeoffs.

**Strategy 1: Short Expiration + Refresh Tokens**
- Access token: 15-30 minutes
- Refresh token: Stored server-side, can be revoked
- On logout: Revoke refresh token
- Access token expires quickly anyway
- Tradeoff: More frequent token refreshes

**Strategy 2: Token Blacklist**
- Maintain list of revoked token IDs (`jti` claim)
- Check blacklist on each request
- Tradeoff: Requires storage lookup (not fully stateless)

**Strategy 3: Token Versioning**
- Add version claim to token
- User has current version in database
- Increment version on logout/password change
- Token with old version rejected
- Tradeoff: Database lookup per request

**Strategy 4: Short-Lived Tokens + Introspection**
- Very short tokens (5 minutes)
- Check token status with auth server periodically
- Tradeoff: Network calls to auth server

**Strategy 5: Event-Driven Revocation**
- Publish revocation events to message bus
- Services maintain in-memory revocation cache
- Eventual consistency (small time window)
- Tradeoff: Complex infrastructure

**Best Practice**: Combine short expiration + refresh tokens for most use cases.

### "JWT Prevents CSRF"

**Misconception**: Using JWT means CSRF protection is unnecessary.

**Reality**: Storage method determines CSRF risk.

**If Stored in httpOnly Cookie**:
- Browser sends automatically
- CSRF attacks possible
- CSRF protection required (tokens, SameSite, etc.)
- Same risk as session cookies

**If Stored in localStorage/sessionStorage**:
- Must send manually via JavaScript
- Not sent automatically by browser
- CSRF not possible via browser auto-send
- BUT: Vulnerable to XSS attacks

**Security Matrix**:

| Storage          | XSS Risk | CSRF Risk | Best For              |
|------------------|----------|-----------|------------------------|
| httpOnly Cookie  | Low      | High*     | Traditional web apps   |
| localStorage     | High     | Low       | SPAs with strong CSP   |
| sessionStorage   | High     | Low       | SPAs, cleared on close |
| Memory Only      | Medium   | Low       | SPAs, lost on refresh  |

*Mitigated with SameSite=Strict and CSRF tokens

**Best Practice**:
- Use httpOnly cookies + SameSite=Strict + CSRF tokens
- OR: localStorage + strong Content Security Policy
- Never: Plain cookies accessible to JavaScript

### "Storing Secrets in JWT is Safe"

**Misconception**: JWT payload is protected from viewing.

**Reality**: JWT payload is base64-encoded, not encrypted.

**Vulnerable Example**:
```json
{
  "sub": "user123",
  "api_key": "sk_live_12345abcdef",
  "database_password": "supersecret",
  "ssn": "123-45-6789"
}
```

Anyone with the JWT can decode and read this data.

**What to Store in JWT**:
- User ID (public identifier)
- Username/email
- Roles/permissions
- Non-sensitive metadata
- Session identifiers

**What NOT to Store**:
- Passwords
- API keys
- Credit card numbers
- Social security numbers
- Private encryption keys
- PII unless encrypted separately

**If Encryption is Required**: Use JWE
```
# JWE structure
header.encrypted_key.iv.ciphertext.authentication_tag
```

Much more complex than standard JWT. Most applications don't need this.

**Best Practice**: Treat JWT as public information. Only include data you'd be comfortable with users seeing.

---

## 5. Security and Best Practices Context

### Algorithm Confusion Attacks

**Attack Type**: Exploiting improper algorithm validation.

**CVE-2015-9235 (auth0/node-jsonwebtoken)**:
- Library accepted `alg: none` when algorithm not specified
- Attacker could create unsigned tokens
- Server accepted them as valid

**Attack Vector**:
```json
// Attacker creates token with no signature
{
  "alg": "none",
  "typ": "JWT"
}
{
  "sub": "admin",
  "role": "administrator"
}
// No signature part, or empty signature
```

**CVE-2016-10555 (PyJWT)**:
- RS256 public key could be used as HS256 secret
- Attacker signs with public key (known to everyone)
- Server verifies with same public key
- Completely bypasses security

**Mitigation**:
```python
# Insecure: Accepts any algorithm
jwt.decode(token, key)

# Secure: Explicitly specify allowed algorithms
jwt.decode(token, key, algorithms=['RS256'])
```

**Best Practices**:
- Always specify allowed algorithms explicitly
- Reject `alg: none` unless specifically needed
- Validate algorithm before decoding
- Use different keys for different algorithms
- Update libraries regularly

### Token Theft and Mitigation

**Threat Vectors**:

1. **XSS (Cross-Site Scripting)**
   - Attacker injects JavaScript
   - Steals token from localStorage/sessionStorage
   - Sends to attacker's server

2. **Man-in-the-Middle**
   - Intercepts HTTP requests
   - Captures token in transit
   - Requires HTTPS

3. **Browser Extensions**
   - Malicious extensions read localStorage
   - User installs unknowingly

4. **Physical Access**
   - Attacker uses unlocked computer
   - Extracts token from browser storage

**Mitigation Strategies**:

**Short Expiration Times**:
```json
{
  "exp": 1516242622,  // 15-30 minutes from issue
  "iat": 1516241622
}
```
Limits damage window if stolen.

**httpOnly Cookies**:
```
Set-Cookie: token=<jwt>; HttpOnly; Secure; SameSite=Strict
```
- Not accessible to JavaScript
- Prevents XSS theft
- Still needs CSRF protection

**Token Binding**:
- Bind token to specific device/browser
- Include fingerprint in claims
- Verify fingerprint on each request
- Limits token portability

**Refresh Token Rotation**:
- Issue new refresh token each use
- Invalidate old refresh token
- Detect token reuse (possible theft)

**IP Address Validation**:
```json
{
  "ip": "192.168.1.100"
}
```
- Validate IP hasn't changed
- Tradeoff: Breaks for mobile users, VPNs

### Signature Verification Importance

**What Signature Provides**:
1. **Authenticity**: Proves who created the token
2. **Integrity**: Detects any modifications
3. **Non-repudiation**: Creator can't deny creating it (with asymmetric keys)

**What Signature Does NOT Provide**:
1. **Confidentiality**: Payload is still readable
2. **Freshness**: Old tokens are still valid if not expired
3. **Authorization**: Server must still check permissions

**Verification Process**:

For HS256 (symmetric):
```
1. Decode header and payload
2. Recreate signature: HMAC-SHA256(header.payload, secret)
3. Compare with token's signature (constant-time comparison)
4. If match, token is valid
```

For RS256 (asymmetric):
```
1. Decode header and payload
2. Get public key (from JWKS or local storage)
3. Verify signature using RSA public key verification
4. If valid, token was signed by private key holder
```

**Critical**: Always verify before trusting claims.

**Anti-Pattern**:
```python
# NEVER DO THIS
payload = base64_decode(token.split('.')[1])
user_id = payload['sub']
# Attacker can modify payload freely
```

**Correct Pattern**:
```python
# Always verify first
payload = jwt.decode(token, key, algorithms=['RS256'])
user_id = payload['sub']
# Cryptographically guaranteed to be authentic
```

### Audience and Issuer Validation

**Issuer (`iss`) Validation**: Who created the token?

**Purpose**: Prevent tokens from one auth server being used with another.

**Example**:
```json
{
  "iss": "https://auth.company.com",
  "sub": "user123"
}
```

**Validation**:
```python
jwt.decode(
    token,
    key,
    algorithms=['RS256'],
    issuer='https://auth.company.com'
)
```

**Attack Prevented**: Attacker uses token from compromised external service.

**Audience (`aud`) Validation**: Who is this token for?

**Purpose**: Prevent token reuse across different applications.

**Example**:
```json
{
  "aud": ["https://api.company.com", "https://admin.company.com"],
  "sub": "user123"
}
```

**Validation**:
```python
jwt.decode(
    token,
    key,
    algorithms=['RS256'],
    audience='https://api.company.com'
)
```

**Attack Prevented**: Using API token on admin interface with higher privileges.

**Real-World Scenario**:
- Company has public API and internal admin API
- Both use same auth server
- Without audience check, public API token works on admin API
- Privilege escalation possible

### Key Rotation Strategies

**Why Rotate Keys**:
1. Limit damage from key compromise
2. Comply with security policies (e.g., every 90 days)
3. Employee departures
4. Suspected breach

**Strategy 1: Overlapping Keys** (Recommended)

1. Generate new key (`key2`)
2. Publish both keys in JWKS
   ```json
   {
     "keys": [
       {"kid": "key1", ...},
       {"kid": "key2", ...}
     ]
   }
   ```
3. Start signing with `key2`, keep verifying `key1`
4. Wait for all `key1` tokens to expire
5. Remove `key1` from JWKS

**Timeline**:
```
Day 0: Add key2 to JWKS
Day 0: Start signing with key2
Day 0-30: Both keys valid (grace period = max token lifetime)
Day 30: Remove key1 from JWKS
```

**Strategy 2: Immediate Rotation** (Disruptive)

1. Generate new key
2. Replace old key in JWKS
3. All existing tokens invalid immediately
4. All users must re-authenticate

Only use for security incidents.

**Strategy 3: Version-Based Rotation**

1. Add version to token claims
   ```json
   {"key_version": "v2"}
   ```
2. Rotate keys, increment version
3. Reject tokens with old version
4. More complex but fine-grained control

**Best Practices**:
- Automate rotation process
- Test rotation in staging first
- Monitor error rates during rotation
- Have rollback plan
- Document rotation procedures

### Common CVEs in JWT Libraries

**CVE-2015-9235** (node-jsonwebtoken)
- Severity: Critical
- Issue: Accepted `alg: none`
- Impact: Complete authentication bypass
- Fix: Specify algorithms explicitly

**CVE-2016-10555** (PyJWT)
- Severity: High
- Issue: Algorithm confusion (RS256 public key as HS256 secret)
- Impact: Authentication bypass
- Fix: Updated to version 1.5.0+

**CVE-2018-0114** (Multiple libraries)
- Severity: Medium
- Issue: JWT signature stripping
- Impact: Authentication bypass
- Fix: Proper signature validation

**CVE-2019-20933** (ruby-jwt)
- Severity: High
- Issue: Improper algorithm verification
- Impact: Signature bypass
- Fix: Update to 2.2.2+

**CVE-2020-28042** (python-jose)
- Severity: Critical
- Issue: Algorithm confusion attack
- Impact: Remote code execution possible
- Fix: Update to 3.2.0+

**Lessons Learned**:
1. Keep libraries updated
2. Subscribe to security advisories
3. Use automated dependency scanning
4. Prefer well-maintained libraries
5. Implement defense in depth

**Monitoring for CVEs**:
- GitHub Security Advisories
- Snyk vulnerability database
- NIST National Vulnerability Database
- Library-specific security pages
- Dependabot / Renovate Bot

---

## Conclusion

JWT is a powerful tool for stateless authentication in modern distributed systems. Understanding its technical foundations, security implications, and proper usage patterns is essential for making informed decisions about authentication architecture.

**Key Takeaways**:
1. JWT is signed, not encrypted - never store secrets in payload
2. Proper validation is critical - signature, expiration, audience, issuer
3. Choose algorithms based on architecture - HS256 vs RS256 vs ES256
4. Revocation is possible but requires additional infrastructure
5. Use established libraries - don't implement cryptography yourself
6. Security is a process - rotate keys, update libraries, monitor for CVEs

This document provides the conceptual foundation. Implementation-specific recommendations and library comparisons are covered in separate research documentation (S1-S4 discovery phases and synthesis).

---

**Document Version**: 1.0
**Last Updated**: 2025-10-20
**Scope**: JWT technical concepts and domain knowledge for business stakeholders
