# Security Comparison - Python JWT Libraries

## Executive Summary

Security analysis reveals **significant differences** in vulnerability histories across Python JWT libraries. Authlib emerges as the security leader with zero CVEs, while python-jose shows the most concerning security posture with multiple critical vulnerabilities and abandonment issues.

## CVE History Analysis

### PyJWT - 3 CVEs (⚠️ CONCERNING)

**CVE-2025-45768** (CURRENT - v2.10.1)
- **Severity**: Medium
- **Type**: Weak Encryption (CWE-311)
- **Status**: ⚠️ **ACTIVE VULNERABILITY** in latest version
- **Impact**: Affects v2.10.1 cryptographic operations
- **Concern Level**: HIGH - unpatched in current release
- **Published**: Recently (2025)

**CVE-2024-53861** (v2.10.0)
- **Severity**: Medium
- **Type**: Improper Validation of 'iss' Claim
- **Status**: ✓ Patched in v2.10.1
- **Impact**: Unauthorized access via issuer claim bypass
- **Pattern**: Claim validation vulnerability

**CVE-2022-29217** (v1.5.0 - v2.3.0)
- **Severity**: High (Critical for some use cases)
- **Type**: Algorithm Confusion / Key Confusion
- **Status**: ✓ Patched in v2.4.0
- **Impact**: Attackers can manipulate algorithm selection
- **Attack Vector**: Submit JWT and choose signing algorithm
- **GitHub Advisory**: GHSA-ffqj-6fqr-9h24
- **Pattern**: **Classic algorithm confusion vulnerability**
- **Widespread Impact**: Affected Microsoft MSAL and other libraries

**Analysis**: PyJWT has a **concerning pattern** of security vulnerabilities, including the critical algorithm confusion class that has plagued JWT libraries. The current unpatched CVE-2025-45768 is particularly worrying.

### python-jose - 3+ CVEs (⚠️⚠️ HIGH RISK)

**CVE-2025-61152** (Recent)
- **Severity**: High (estimated)
- **Type**: JWT Token Validation Vulnerability
- **Status**: ⚠️ Limited public disclosure
- **Impact**: "Serious risk" to applications using python-jose for validation
- **Concern**: Details limited, suggesting active exploitation potential

**CVE-2024-33663** (v3.0.0 - v3.3.0)
- **Severity**: High
- **Type**: Algorithm Confusion with OpenSSH ECDSA Keys
- **Status**: ✓ Patched in v3.3.1
- **Impact**: Security control bypass, unauthorized actions
- **Pattern**: **Same algorithm confusion class as PyJWT CVE-2022-29217**
- **Attack Vector**: Key format manipulation
- **Widespread Risk**: Algorithm confusion is a fundamental JWT vulnerability

**CVE-2024-33664** (v3.0.0 - v3.3.0)
- **Severity**: High
- **Type**: Denial of Service - JWT Bomb
- **Status**: ✓ Patched in v3.3.1+
- **Impact**: Resource exhaustion via compressed JWE
- **Technical**: High compression ratio decompression bomb
- **Uniqueness**: **Unique to python-jose** - not seen in other analyzed libraries
- **Attack Sophistication**: Crafted JWE tokens with compression

**Analysis**: python-jose shows **the worst security posture**:
1. Multiple vulnerabilities in same version range (3.0.0-3.3.0)
2. Algorithm confusion vulnerability (common pattern)
3. Unique JWT bomb DoS attack
4. Recent CVE with limited disclosure (security through obscurity concern)
5. **4-year maintenance gap (2021-2025)** - vulnerabilities may exist undiscovered

### Authlib - 0 CVEs (✓ EXCELLENT)

**CVE History**: **NONE FOUND**

**Research Coverage**:
- CVE databases searched
- GitHub security advisories checked
- Security blogs reviewed
- Vendor bulletins examined

**Analysis**: Authlib has a **clean security record** with:
- Zero Common Vulnerabilities and Exposures
- No algorithm confusion vulnerabilities
- No DoS vulnerabilities
- No claim validation bypasses
- No security advisories

**Possible Reasons**:
1. **Security-first design**: Explicit validation architecture
2. **Professional maintenance**: Active team catching issues pre-release
3. **Comprehensive testing**: Better security testing practices
4. **Newer codebase**: Less legacy technical debt
5. **Transparent documentation**: Documents limitations honestly

**Verification**: This exceptional record verified across multiple security databases

### jwcrypto - 2-3 CVEs (⚠️ MODERATE)

**CVE-2024-28102** (Recent)
- **Severity**: Medium-High
- **Type**: Denial of Service
- **Status**: ✓ Addressed in recent releases
- **Impact**: Malicious JWE token causes DoS
- **Attack Vector**: Crafted JWE tokens
- **Similar to**: python-jose CVE-2024-33664 (both JWE DoS)

**CVE-2022-3102** (v1.0 - v1.3.1)
- **Severity**: Medium
- **Type**: Token Type Confusion (JWS vs JWE)
- **Status**: ✓ Fixed in v1.4+ with 'expect_type' parameter
- **Impact**: Substitution attack - signed JWS replaced with encrypted JWE
- **Attack Scenario**: JWE encrypted with public key used for signature validation
- **Prerequisite**: Validating app must have access to private key during validation
- **Architectural Fix**: Added explicit type checking

**CVE-2022-39227** (Indirect - python-jwt library)
- **Context**: Affects python-jwt library that depends on jwcrypto
- **Type**: Token forgery with new claims
- **Root Cause**: Parser inconsistency between python-jwt and jwcrypto
- **Note**: Not jwcrypto's fault, but shows integration risks

**Analysis**: jwcrypto has **moderate security concerns**:
1. Recent DoS vulnerability (JWE-specific)
2. Historical type confusion (architecturally fixed)
3. Integration risks with dependent libraries
4. Smaller community = fewer security researchers

## Vulnerability Pattern Analysis

### Algorithm Confusion Vulnerabilities

**Definition**: Attacker manipulates which algorithm is used to verify JWT signatures, potentially allowing:
- Using public key as HMAC secret
- Downgrading from asymmetric to symmetric algorithms
- Bypassing signature verification

**Affected Libraries**:
- ✗ **PyJWT**: CVE-2022-29217 - Direct algorithm confusion
- ✗ **python-jose**: CVE-2024-33663 - Algorithm confusion with ECDSA keys
- ✓ **Authlib**: No algorithm confusion CVEs (explicit algorithm allowlisting)
- ✗ **jwcrypto**: CVE-2022-3102 - Token type confusion (similar pattern)

**Industry Context**: Algorithm confusion is a **well-known JWT vulnerability class** affecting libraries across languages (CVE-2015-9235 in node-jsonwebtoken, etc.)

**Mitigation**:
```python
# ALWAYS specify allowed algorithms explicitly
jwt.decode(token, key, algorithms=["RS256"])  # Good
jwt.decode(token, key)  # BAD - may allow algorithm manipulation
```

### Denial of Service Vulnerabilities

**JWT Bomb Attacks**:
- **python-jose**: CVE-2024-33664 - Compression bomb in JWE
- **jwcrypto**: CVE-2024-28102 - Malicious JWE DoS

**Pattern**: JWE (encrypted tokens) introduce DoS vectors through:
1. Compression bombs (high compression ratio)
2. Resource exhaustion during decryption
3. Complex key agreement operations

**Implication**: Libraries with JWE support have additional attack surface

### Claim Validation Vulnerabilities

**PyJWT CVE-2024-53861**: Improper 'iss' (issuer) claim validation
**Impact**: Bypassing authentication/authorization checks
**Root Cause**: Insufficient validation of registered claims

**Best Practice**: Always validate all security-relevant claims:
```python
# Validate issuer, audience, expiration
claims = jwt.decode(
    token, key, algorithms=["RS256"],
    issuer="trusted-issuer",
    audience="my-app"
)
```

## Security Features Comparison

### Signature Verification

| Library | Verification | Bad Signature Handling |
|---------|--------------|------------------------|
| PyJWT | Automatic | Raises `InvalidSignatureError` |
| python-jose | Automatic | Raises exception |
| Authlib | Automatic | Raises `BadSignatureError` |
| jwcrypto | Automatic | Raises exception |

**All libraries**: ✓ Automatic signature verification

### Algorithm Allowlisting

| Library | Algorithm Control | Default Behavior |
|---------|-------------------|------------------|
| PyJWT | Required in `algorithms=[]` | No default (must specify) |
| python-jose | Supported | Less explicit |
| Authlib | `JsonWebToken(['HS256'])` | Must specify at init |
| jwcrypto | Supported | Less emphasized |

**Best**: Authlib (algorithm restriction at init prevents accidental misconfiguration)
**Good**: PyJWT (requires explicit specification)

### Claim Validation

| Library | Validation Approach | Registered Claims |
|---------|---------------------|-------------------|
| PyJWT | Options in `decode()` | exp, nbf, iat, aud, iss |
| python-jose | Automatic (configurable) | All standard claims |
| Authlib | Explicit `claims.validate()` | All RFC 7519 claims |
| jwcrypto | Manual validation | Standard claims supported |

**Best**: Authlib (explicit validation prevents accidents)
**Risk**: jwcrypto (requires manual validation)

### Expiration Validation

| Library | Expiration Check | Leeway Support |
|---------|------------------|----------------|
| PyJWT | ✓ Automatic (unless disabled) | ✓ Configurable leeway |
| python-jose | ✓ Automatic | ✓ Supported |
| Authlib | ✓ Via `validate()` | ✓ Supported |
| jwcrypto | ✓ Manual | ✓ Supported |

**All libraries**: Support expiration validation with clock skew tolerance

### Audience Validation

| Library | Audience Check | Strict Mode |
|---------|----------------|-------------|
| PyJWT | ✓ `audience=` parameter | ✓ Strict matching |
| python-jose | ✓ Supported | ✓ Supported |
| Authlib | ✓ `validate_aud()` | ✓ **MUST reject if mismatch** (RFC strict) |
| jwcrypto | ✓ Manual | ✓ Configurable |

**Best**: Authlib (RFC 7519 strict compliance - token MUST be rejected)

## Security Best Practices by Library

### PyJWT Security Checklist

```python
# ✓ Always specify algorithms explicitly
jwt.decode(token, key, algorithms=["RS256"])

# ✓ Validate all security claims
jwt.decode(
    token, key,
    algorithms=["RS256"],
    audience="my-app",
    issuer="auth-server",
    options={"verify_exp": True, "verify_aud": True}
)

# ✓ Use latest version (but monitor CVE-2025-45768)
# ✓ Install with crypto extras for RSA/ECDSA
pip install pyjwt[crypto]

# ✗ NEVER allow algorithm="none"
# ✗ NEVER use decode without algorithms parameter
```

### python-jose Security Checklist

```python
# ⚠️ RECOMMENDATION: Migrate to alternative library

# If must use:
# ✓ Upgrade to 3.3.1+ (patches CVE-2024-33663, CVE-2024-33664)
# ✓ Use cryptography backend only
pip install python-jose[cryptography]

# ✓ Remove unused backends in production
# ✓ Plan migration to maintained alternative
```

### Authlib Security Checklist

```python
# ✓ Initialize with explicit algorithms
jwt = JsonWebToken(['RS256'])

# ✓ ALWAYS call validate() after decode
claims = jwt.decode(token, public_key)
claims.validate()  # Critical - do not skip

# ✓ Validate specific claims
claims.validate_iss('expected-issuer')
claims.validate_aud('my-app')
claims.validate_exp()

# ✓ Be aware of algorithm-key type validation limitation
# Ensure keys match algorithm types in application logic
```

### jwcrypto Security Checklist

```python
# ✓ Always specify expected token type
received = jwt.JWT(key=key, jwt=token_string)
received.validate(key, expected_type='JWS')

# ✓ Use latest version (addresses CVE-2024-28102)
# ✓ Validate claims manually
# ✓ Be cautious with JWE (DoS potential)
```

## Security Ratings

### Overall Security Posture

**Authlib**: ★★★★★ (5/5)
- Zero CVE history
- Comprehensive security features
- Explicit validation architecture
- Transparent documentation of limitations
- **Recommendation**: Highest security confidence

**jwcrypto**: ★★★☆☆ (3/5)
- Moderate CVE history (2-3 CVEs)
- Fixed type confusion vulnerability
- Recent DoS vulnerability
- Security-focused design
- **Recommendation**: Acceptable with caution

**PyJWT**: ★★☆☆☆ (2/5)
- Multiple CVEs including algorithm confusion
- Current unpatched CVE-2025-45768
- History of security issues
- Requires careful configuration
- **Recommendation**: Use with strong security practices, monitor closely

**python-jose**: ★☆☆☆☆ (1/5)
- Multiple critical CVEs
- Algorithm confusion vulnerability
- Unique JWT bomb attack
- 4-year abandonment period
- Recent CVE with limited disclosure
- **Recommendation**: AVOID for new projects, migrate existing

## Time-to-Patch Analysis

### CVE Response Speed

**PyJWT**:
- CVE-2022-29217: Patched in v2.4.0 (reasonable timeline)
- CVE-2024-53861: Patched in v2.10.1 (quick response)
- CVE-2025-45768: ⚠️ Currently unpatched (concerning)

**python-jose**:
- Long abandonment meant delayed responses
- CVE-2024-33663 & CVE-2024-33664: Patched together in v3.3.1
- CVE-2025-61152: Status unclear

**Authlib**:
- N/A (no CVEs)
- Proactive security practices appear effective

**jwcrypto**:
- CVE-2022-3102: Fixed with architectural change (v1.4+)
- CVE-2024-28102: Addressed in recent releases
- Responsive to security issues

**Best Response**: Authlib (proactive prevention) and jwcrypto (responsive patching)
**Concerning**: PyJWT (current unpatched CVE), python-jose (abandonment delays)

## Cryptographic Backend Security

### python-cryptography Quality

**All libraries use python-cryptography** (pyca/cryptography):
- ✓ Well-maintained, industry-standard
- ✓ Memory-safe (Rust/C implementation)
- ✓ NIST-certified algorithms
- ✓ Regular security audits
- ✓ Used by major projects (Requests, Paramiko, etc.)

**Backend Comparison**:
- **PyJWT**: python-cryptography only ✓
- **python-jose**: Multiple backends (complexity risk) ✗
- **Authlib**: python-cryptography only ✓
- **jwcrypto**: python-cryptography only ✓

**Security Implication**: python-jose's multiple backends increase attack surface

## Security Recommendations

### Critical Applications (Banking, Healthcare, Government)
1. **Authlib** - Zero CVE history, professional maintenance
2. jwcrypto - If JWE required, with careful monitoring
3. PyJWT - Only with strong security review and monitoring
4. python-jose - ⚠️ NOT RECOMMENDED

### Standard Applications (SaaS, E-commerce)
1. **Authlib** - Best overall security posture
2. PyJWT - With explicit algorithm allowlisting and regular updates
3. jwcrypto - For JWE requirements
4. python-jose - ⚠️ Migrate away

### Internal Tools (Low Security Requirements)
1. Authlib - Still recommended
2. PyJWT - Acceptable with proper configuration
3. jwcrypto - Acceptable
4. python-jose - Plan migration timeline

### JWE (Encryption) Requirements
1. **Authlib** - Comprehensive JWE support, zero CVEs
2. jwcrypto - Specialized JWE focus (monitor CVE-2024-28102)
3. python-jose - ⚠️ Has JWE but security concerns

## Conclusion

**Security analysis clearly favors Authlib** with its exceptional zero-CVE track record and comprehensive security features. python-jose presents the highest risk with multiple critical vulnerabilities and abandonment concerns. PyJWT's current unpatched CVE-2025-45768 is concerning despite wide adoption. jwcrypto offers moderate security with JWE specialization.

**For production applications requiring strong security guarantees, Authlib is the clear choice.**
