# Feature Comparison - Python JWT Libraries

## Overview

This analysis compares RFC 7519 compliance, algorithm support, validation features, and implementation completeness across four Python JWT libraries.

## RFC 7519 Compliance Matrix

### Registered Claims Support

| Claim | RFC 7519 Description | PyJWT | python-jose | Authlib | jwcrypto |
|-------|---------------------|-------|-------------|---------|----------|
| **iss** | Issuer - identifies who issued JWT | ✓ | ✓ | ✓✓ | ✓ |
| **sub** | Subject - identifies subject | ✓ | ✓ | ✓✓ | ✓ |
| **aud** | Audience - intended recipients | ✓ | ✓ | ✓✓ | ✓ |
| **exp** | Expiration Time | ✓ | ✓ | ✓✓ | ✓ |
| **nbf** | Not Before - not valid before time | ✓ | ✓ | ✓✓ | ✓ |
| **iat** | Issued At - when JWT was issued | ✓ | ✓ | ✓✓ | ✓ |
| **jti** | JWT ID - unique identifier | ✓ | ✓ | ✓✓ | ✓ |

**Legend**:
- ✓✓ = RFC-strict compliance with MUST/SHOULD enforcement
- ✓ = Supported with standard validation

**Analysis**:
- **All libraries** support the seven registered claims defined in RFC 7519
- **Authlib** provides most RFC-strict implementation (explicit MUST reject semantics)
- **PyJWT, python-jose, jwcrypto** provide adequate claim support

### RFC-Specific Documentation

| Library | RFC 7519 Docs | Claims Detail | Validation Semantics |
|---------|---------------|---------------|---------------------|
| PyJWT | ✓ General | Good | Clear |
| python-jose | ✓ Basic | Adequate | Basic |
| **Authlib** | ✓✓ **Dedicated RFC page** | **Excellent** | **RFC MUST/SHOULD** |
| jwcrypto | ✓ Technical | Good | Technical |

**Winner**: **Authlib** - Provides dedicated RFC 7519 documentation page with exact MUST/SHOULD semantics

Example from Authlib docs:
> "Each principal intended to process the JWT MUST identify itself with a value in the audience claim. If the principal processing the claim does not identify itself with a value in the 'aud' claim when this claim is present, then the JWT MUST be rejected."

This level of RFC precision is unique to Authlib's documentation.

## Algorithm Support Comparison

### Symmetric Algorithms (HMAC)

| Algorithm | Description | PyJWT | python-jose | Authlib | jwcrypto |
|-----------|-------------|-------|-------------|---------|----------|
| **HS256** | HMAC SHA-256 (default) | ✓ | ✓ | ✓ | ✓ |
| **HS384** | HMAC SHA-384 | ✓ | ✓ | ✓ | ✓ |
| **HS512** | HMAC SHA-512 | ✓ | ✓ | ✓ | ✓ |

**Universal Support**: All libraries support HMAC algorithms

**Performance**: HMAC algorithms are fastest (~3,000-4,000 ns/op)

### Asymmetric Algorithms (RSA)

| Algorithm | Description | PyJWT | python-jose | Authlib | jwcrypto |
|-----------|-------------|-------|-------------|---------|----------|
| **RS256** | RSA PKCS1 SHA-256 | ✓* | ✓ | ✓ | ✓ |
| **RS384** | RSA PKCS1 SHA-384 | ✓* | ✓ | ✓ | ✓ |
| **RS512** | RSA PKCS1 SHA-512 | ✓* | ✓ | ✓ | ✓ |
| **PS256** | RSA-PSS SHA-256 | ✓* | - | ✓ | ✓ |
| **PS384** | RSA-PSS SHA-384 | ✓* | - | ✓ | ✓ |
| **PS512** | RSA-PSS SHA-512 | ✓* | - | ✓ | ✓ |

**Note**: PyJWT requires `pip install pyjwt[crypto]` for RSA support (marked with *)

**Best Support**: PyJWT, Authlib, jwcrypto (includes PSS variants)

**Performance**: RSA ~2,500,000 ns/op for 2048-bit keys (much slower than HMAC)

### Asymmetric Algorithms (ECDSA)

| Algorithm | Description | PyJWT | python-jose | Authlib | jwcrypto |
|-----------|-------------|-------|-------------|---------|----------|
| **ES256** | ECDSA P-256 SHA-256 | ✓* | ✓ | ✓ | ✓ |
| **ES384** | ECDSA P-384 SHA-384 | ✓* | ✓ | ✓ | ✓ |
| **ES512** | ECDSA P-521 SHA-512 | ✓* | ✓ | ✓ | ✓ |
| **ES256K** | ECDSA secp256k1 SHA-256 | ✓* | - | ✓ | - |

**Best Support**: PyJWT and Authlib (include ES256K for Bitcoin/Ethereum compatibility)

**Performance**: ECDSA moderate (faster than RSA, slower than HMAC)

### Modern Algorithms (EdDSA)

| Algorithm | Description | PyJWT | python-jose | Authlib | jwcrypto |
|-----------|-------------|-------|-------------|---------|----------|
| **EdDSA** | Ed25519/Ed448 | ✓* | - | ✓ | ✓ |

**Support**: PyJWT, Authlib, jwcrypto

**Note**: python-jose lacks EdDSA support (older codebase)

**Advantage**: EdDSA provides excellent performance and security

## JWE (Encryption) Support

### Key Management Algorithms

| Algorithm | PyJWT | python-jose | Authlib | jwcrypto |
|-----------|-------|-------------|---------|----------|
| RSA1_5 | - | ✓ | ✓ | ✓ |
| RSA-OAEP | - | ✓ | ✓ | ✓ |
| RSA-OAEP-256 | - | ✓ | ✓ | ✓ |
| A128KW | - | ✓ | ✓ | ✓ |
| A192KW | - | ✓ | ✓ | ✓ |
| A256KW | - | ✓ | ✓ | ✓ |
| dir | - | ✓ | ✓ | ✓ |
| ECDH-ES | - | - | ✓ | ✓ |
| ECDH-ES+A128KW | - | - | ✓ | ✓ |
| ECDH-ES+A192KW | - | - | ✓ | ✓ |
| ECDH-ES+A256KW | - | - | ✓ | ✓ |
| A128GCMKW | - | - | ✓ | ✓ |
| A192GCMKW | - | - | ✓ | ✓ |
| A256GCMKW | - | - | ✓ | ✓ |
| PBES2-HS256+A128KW | - | - | ✓ | ✓ |
| PBES2-HS384+A192KW | - | - | ✓ | ✓ |
| PBES2-HS512+A256KW | - | - | ✓ | ✓ |

### Content Encryption Algorithms

| Algorithm | PyJWT | python-jose | Authlib | jwcrypto |
|-----------|-------|-------------|---------|----------|
| A128CBC-HS256 | - | ✓ | ✓ | ✓ |
| A192CBC-HS384 | - | ✓ | ✓ | ✓ |
| A256CBC-HS512 | - | ✓ | ✓ | ✓ |
| A128GCM | - | ✓ | ✓ | ✓ |
| A192GCM | - | ✓ | ✓ | ✓ |
| A256GCM | - | ✓ | ✓ | ✓ |

**JWE Support Summary**:
- **PyJWT**: ✗ Limited/No JWE support (JWS-focused)
- **python-jose**: ✓ Basic JWE support
- **Authlib**: ✓✓ Comprehensive JWE support
- **jwcrypto**: ✓✓ Comprehensive JWE support (specialized)

**Winner for JWE**: **Authlib** and **jwcrypto** (both comprehensive)

**Security Note**: JWE introduces additional attack surface (see CVE-2024-33664 python-jose, CVE-2024-28102 jwcrypto)

## Token Validation Features

### Signature Verification

| Library | Automatic Verification | Error Handling | Custom Validation |
|---------|------------------------|----------------|-------------------|
| PyJWT | ✓ Auto | `InvalidSignatureError` | ✓ Supported |
| python-jose | ✓ Auto | Exception | ✓ Supported |
| Authlib | ✓ Auto | `BadSignatureError` | ✓ Extensive |
| jwcrypto | ✓ Auto | Exception | ✓ Supported |

**All libraries**: Automatic signature verification with clear error handling

### Expiration Validation (exp)

| Library | Default Behavior | Leeway Support | Disable Option |
|---------|------------------|----------------|----------------|
| PyJWT | ✓ On by default | ✓ Configurable | ✓ `verify_exp=False` |
| python-jose | ✓ Automatic | ✓ Supported | ✓ Options |
| Authlib | ✓ Via `validate()` | ✓ Configurable | ✓ Skip validate |
| jwcrypto | Manual | ✓ Supported | N/A (manual) |

**Best Practice**: All libraries support clock skew tolerance (leeway)

**Unique**: Authlib requires explicit `claims.validate()` call (prevents accidental acceptance)

### Audience Validation (aud)

| Library | Validation Method | Strict Matching | Multiple Audiences |
|---------|-------------------|-----------------|-------------------|
| PyJWT | `audience=` parameter | ✓ | ✓ List support |
| python-jose | Built-in | ✓ | ✓ Supported |
| Authlib | `validate_aud()` | ✓✓ **MUST reject** | ✓ RFC-compliant |
| jwcrypto | Manual | ✓ | ✓ Supported |

**Best**: **Authlib** - Implements RFC 7519 MUST reject semantics

### Issuer Validation (iss)

| Library | Validation Method | CVE History | Strictness |
|---------|-------------------|-------------|------------|
| PyJWT | `issuer=` parameter | ⚠️ CVE-2024-53861 | Fixed |
| python-jose | Built-in | - | Standard |
| Authlib | `validate_iss()` | ✓ No CVEs | Strict |
| jwcrypto | Manual | - | Manual |

**Note**: PyJWT had issuer validation bypass (CVE-2024-53861) - now fixed

### Not Before Validation (nbf)

| Library | Support | Leeway | Default Behavior |
|---------|---------|--------|------------------|
| PyJWT | ✓ | ✓ | Auto if present |
| python-jose | ✓ | ✓ | Auto if present |
| Authlib | ✓ | ✓ | Via `validate()` |
| jwcrypto | ✓ | ✓ | Manual |

**All libraries**: Support not-before validation with clock skew

### JWT ID Validation (jti)

| Library | Support | Replay Protection | Database Integration |
|---------|---------|-------------------|---------------------|
| PyJWT | ✓ Present | Manual | App responsibility |
| python-jose | ✓ Present | Manual | App responsibility |
| Authlib | ✓ Present | Manual | App responsibility |
| jwcrypto | ✓ Present | Manual | App responsibility |

**Note**: No library provides built-in replay protection - application must track JTI

## Standards Compliance

### JOSE Specifications

| Standard | Description | PyJWT | python-jose | Authlib | jwcrypto |
|----------|-------------|-------|-------------|---------|----------|
| **RFC 7519** | JWT | ✓ | ✓ | ✓✓ | ✓ |
| **RFC 7515** | JWS (Signatures) | ✓ | ✓ | ✓✓ | ✓ |
| **RFC 7516** | JWE (Encryption) | - | ✓ | ✓✓ | ✓ |
| **RFC 7517** | JWK (Keys) | Partial | ✓ | ✓✓ | ✓ |
| **RFC 7518** | JWA (Algorithms) | ✓ | ✓ | ✓✓ | ✓ |
| **RFC 7523** | JWT for OAuth 2.0 | - | - | ✓✓ | - |
| **RFC 9068** | JWT for OAuth 2.0 Access Tokens | - | - | ✓✓ | - |

**Most Comprehensive**: **Authlib** (includes OAuth-specific JWT RFCs)

**Basic JWT**: PyJWT (focused on core JWT functionality)

### Additional Standards (Authlib Only)

| Standard | Description |
|----------|-------------|
| OAuth 1.0 | Legacy OAuth |
| OAuth 2.0 | Current OAuth standard |
| OAuth 2.1 | Latest OAuth specification |
| OpenID Connect | Identity layer on OAuth 2.0 |

**Advantage**: Authlib provides complete authentication/authorization stack

## API Design and Usability

### Basic Encoding

**PyJWT** (Simplest):
```python
import jwt
token = jwt.encode({"data": "value"}, "secret", algorithm="HS256")
```

**python-jose**:
```python
from jose import jwt
token = jwt.encode({'data': 'value'}, 'secret', algorithm='HS256')
```

**Authlib** (Explicit):
```python
from authlib.jose import jwt
header = {'alg': 'HS256'}
payload = {'data': 'value'}
token = jwt.encode(header, payload, 'secret')
```

**jwcrypto** (Low-level):
```python
from jwcrypto import jwt, jwk
key = jwk.JWK(kty='oct', k='secret')
token = jwt.JWT(header={"alg": "HS256"}, claims={"data": "value"})
token.make_signed_token(key)
```

**Ease of Use**: PyJWT = python-jose > Authlib > jwcrypto

### Basic Decoding

**PyJWT**:
```python
decoded = jwt.decode(token, "secret", algorithms=["HS256"])
```

**python-jose**:
```python
decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
```

**Authlib** (Two-step):
```python
claims = jwt.decode(token, 'secret')
claims.validate()  # MUST call explicitly
```

**jwcrypto**:
```python
received = jwt.JWT(key=key, jwt=token)
claims = received.claims
```

**Ease of Use**: PyJWT = python-jose > Authlib ≈ jwcrypto

### Advanced Validation

**PyJWT**:
```python
decoded = jwt.decode(
    token, key, algorithms=["RS256"],
    audience="app", issuer="auth", options={"verify_exp": True}
)
```

**Authlib** (Most Explicit):
```python
claims = jwt.decode(token, key)
claims_options = {
    'iss': {'essential': True, 'value': 'auth'},
    'aud': {'essential': True, 'value': 'app'},
    'exp': {'essential': True, 'validate': jwt.verify_exp}
}
claims.validate(claims_options)
```

**Power**: Authlib > PyJWT > python-jose > jwcrypto

## Key Management

### Key Format Support

| Format | PyJWT | python-jose | Authlib | jwcrypto |
|--------|-------|-------------|---------|----------|
| PEM | ✓ | ✓ | ✓ | ✓ |
| JWK | Partial | ✓ | ✓✓ | ✓✓ |
| SSH | - | ✓ (CVE!) | - | - |
| Raw bytes | ✓ | ✓ | ✓ | ✓ |

**Note**: python-jose SSH key support led to CVE-2024-33663 (algorithm confusion)

**Best JWK Support**: Authlib and jwcrypto (automatic JWK handling)

### Key Type Classes

**Authlib** (Structured):
- `OctKey` - Symmetric keys
- `RSAKey` - RSA keys
- `ECKey` - Elliptic Curve keys
- `OKPKey` - Octet Key Pair (EdDSA)

**jwcrypto** (Explicit):
- `JWK` - JSON Web Key class
- Key generation support
- Key set management

**PyJWT**: Basic key loading (less structured)

## Integration Features

### Framework Support

| Framework | PyJWT | python-jose | Authlib | jwcrypto |
|-----------|-------|-------------|---------|----------|
| Flask | Via extensions | Via extensions | ✓✓ **Official** | Manual |
| Django | Via packages | Via packages | ✓✓ **Official** | Manual |
| FastAPI | ✓ Recommended | ⚠️ Deprecated | ✓ Supported | Manual |
| Starlette | Via FastAPI | Via packages | ✓✓ **Official** | Manual |

**Winner**: **Authlib** - Official framework integrations

### OAuth 2.0 Integration

| Feature | PyJWT | python-jose | Authlib | jwcrypto |
|---------|-------|-------------|---------|----------|
| OAuth 2.0 Client | - | - | ✓✓ | - |
| OAuth 2.0 Server | - | - | ✓✓ | - |
| OpenID Connect | - | - | ✓✓ | - |
| Service Accounts | - | - | ✓✓ | - |

**Unique**: **Authlib** - Only library with complete OAuth ecosystem

### Migration Support

| Library | Migration Guides | From Libraries |
|---------|------------------|----------------|
| Authlib | ✓✓ Official | PyJWT, python-jose |
| Others | - | Community guides |

**Advantage**: Authlib provides official migration documentation

## Performance Characteristics

### Algorithm Performance (General)

| Algorithm Type | Speed Rating | Use Case |
|----------------|--------------|----------|
| HMAC (HS256/384/512) | ⚡⚡⚡ Very Fast | Internal services, APIs |
| ECDSA (ES256/384/512) | ⚡⚡ Moderate | Modern applications |
| RSA (RS256/384/512) | ⚡ Slower | Legacy compatibility |
| EdDSA | ⚡⚡⚡ Very Fast | Modern, high-performance |

**Note**: Performance primarily determined by algorithm choice, not library

### Library-Specific Performance

**All libraries use python-cryptography backend** → Similar performance

**Optimization Features**:
- PyJWT: Key reuse optimization, optional verification disabling
- Authlib: Efficient key handling
- jwcrypto: Proper cryptography usage
- python-jose: Multiple backends (cryptography fastest)

**Expected Performance**: Authlib ≈ PyJWT ≈ jwcrypto > python-jose (native backend)

## Feature Summary Matrix

### Overall Capability Scores

| Feature Category | PyJWT | python-jose | Authlib | jwcrypto |
|------------------|-------|-------------|---------|----------|
| **RFC 7519 Compliance** | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★★☆ |
| **Algorithm Support** | ★★★★★ | ★★★☆☆ | ★★★★★ | ★★★★★ |
| **JWE (Encryption)** | ★☆☆☆☆ | ★★★☆☆ | ★★★★★ | ★★★★★ |
| **Validation Features** | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★☆☆ |
| **API Simplicity** | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★☆☆ |
| **Documentation** | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★☆☆ |
| **OAuth Integration** | ★☆☆☆☆ | ★☆☆☆☆ | ★★★★★ | ★☆☆☆☆ |
| **Framework Support** | ★★★☆☆ | ★★☆☆☆ | ★★★★★ | ★★☆☆☆ |

### Recommended By Feature Need

**Simple JWT Signing/Verification**: PyJWT
**Comprehensive JOSE**: Authlib or jwcrypto
**JWE Encryption**: Authlib or jwcrypto
**OAuth 2.0 Integration**: Authlib (only option)
**RFC Strict Compliance**: Authlib
**EdDSA Algorithm**: PyJWT, Authlib, or jwcrypto
**Framework Integration**: Authlib

## Conclusion

**Most Feature-Complete**: **Authlib** - Comprehensive JWT, JWE, OAuth, OIDC, framework integrations

**Simplest for Basic JWT**: **PyJWT** - Easy API for signing/verification only

**Best for JWE Focus**: **jwcrypto** or **Authlib** - Both comprehensive encryption support

**Avoid**: **python-jose** - Lacking modern features (EdDSA), abandoned maintenance
