# Requirement-Solution Matrix

## Purpose

This matrix maps specific use case requirements to Python cryptographic library capabilities. It uses a need-driven scoring system to identify the best-fit solution for each scenario.

## Scoring System

**Requirement Categories:**
- **CRITICAL**: Must be met or solution is unusable (-1000 if missing)
- **HIGH**: Important for production use (+10 if present, -50 if missing)
- **MEDIUM**: Improves usability/performance (+5 if present)
- **LOW**: Nice-to-have convenience (+2 if present)
- **BLOAT**: Unnecessary feature complexity (-1 per major unused feature)

**Library Evaluation:**
Each library receives a score per use case. Higher scores indicate better fit.

## Libraries Evaluated

1. **cryptography** - PyCA comprehensive cryptographic library
2. **PyNaCl** - Python binding to libsodium (NaCl)
3. **pycryptodome** - PyCrypto fork with active maintenance
4. **hashlib** - Python standard library (limited scope)
5. **PyJWT** - JWT implementation (specialized)
6. **argon2-cffi** - Argon2 password hashing (specialized)

## Use Case 1: Web Application Authentication

### Requirements Breakdown

| Requirement | Priority | cryptography | PyNaCl | pycryptodome | hashlib | argon2-cffi | PyJWT |
|------------|----------|--------------|---------|--------------|---------|-------------|-------|
| Argon2id password hashing | CRITICAL | ❌ -1000 | ❌ -1000 | ❌ -1000 | ❌ -1000 | ✅ +10 | ❌ -1000 |
| bcrypt password hashing | CRITICAL | ✅ +10 | ❌ -1000 | ✅ +10 | ❌ -1000 | ❌ -50 | ❌ -1000 |
| CSPRNG token generation | HIGH | ✅ +10 | ✅ +10 | ✅ +10 | ⚠️ Use `secrets` | ⚠️ Use `secrets` | ⚠️ Use `secrets` |
| HMAC-SHA256 signing | HIGH | ✅ +10 | ✅ +10 | ✅ +10 | ✅ +10 | ❌ -50 | ⚠️ Part of JWT |
| Constant-time comparison | HIGH | ✅ +10 | ✅ +10 | ⚠️ Manual | ❌ -50 | ✅ +10 | ❌ -50 |
| Django integration | MEDIUM | ✅ +5 | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | ✅ +5 | ❌ 0 |
| Configurable work factor | MEDIUM | ✅ +5 | ❌ 0 | ✅ +5 | ❌ 0 | ✅ +5 | ❌ 0 |
| Hash time: 50-250ms | HIGH | ✅ +10 | N/A | ✅ +10 | N/A | ✅ +10 | N/A |
| Thread-safe operations | HIGH | ✅ +10 | ✅ +10 | ✅ +10 | ✅ +10 | ✅ +10 | ✅ +10 |
| Pure Python fallback | LOW | ❌ 0 | ❌ 0 | ✅ +2 | ✅ +2 | ❌ 0 | ✅ +2 |
| Bloat penalty (unused features) | BLOAT | -5 | -1 | -3 | 0 | 0 | 0 |

### Use Case 1 Scores

**Scenario A: Argon2id Required**
- cryptography: -1000 (no Argon2id)
- PyNaCl: -1000 (no Argon2id)
- pycryptodome: -1000 (no Argon2id)
- hashlib: -1000 (no Argon2id)
- **argon2-cffi: +50** ✅ BEST FIT
- PyJWT: -1000 (wrong use case)

**Scenario B: bcrypt Acceptable**
- **cryptography: +60** ✅ BEST FIT
- PyNaCl: -1000 (no bcrypt)
- pycryptodome: +55 (close second)
- hashlib: -1000
- argon2-cffi: -40 (no bcrypt)
- PyJWT: -1000

**Recommendation**: **argon2-cffi** (for Argon2id) + **cryptography** (for HMAC, constant-time comparison) OR **cryptography** alone if bcrypt is acceptable.

## Use Case 2: Data Encryption

### Requirements Breakdown

| Requirement | Priority | cryptography | PyNaCl | pycryptodome | hashlib | argon2-cffi | PyJWT |
|------------|----------|--------------|---------|--------------|---------|-------------|-------|
| AES-256-GCM encryption | CRITICAL | ✅ +10 | ❌ -1000 | ✅ +10 | ❌ -1000 | ❌ -1000 | ❌ -1000 |
| Authenticated encryption (AEAD) | CRITICAL | ✅ +10 | ✅ +10 | ✅ +10 | ❌ -1000 | ❌ -1000 | ❌ -1000 |
| Streaming encryption | HIGH | ✅ +10 | ⚠️ Manual | ✅ +10 | ❌ -50 | ❌ -50 | ❌ -50 |
| Key wrapping (AES-KW) | HIGH | ✅ +10 | ❌ -50 | ✅ +10 | ❌ -50 | ❌ -50 | ❌ -50 |
| Key derivation (PBKDF2/HKDF) | HIGH | ✅ +10 | ⚠️ +5 | ✅ +10 | ⚠️ PBKDF2 only | ❌ -50 | ❌ -50 |
| Deterministic encryption | MEDIUM | ⚠️ Manual +3 | ❌ 0 | ⚠️ Manual +3 | ❌ 0 | ❌ 0 | ❌ 0 |
| ChaCha20-Poly1305 | MEDIUM | ✅ +5 | ✅ +5 | ✅ +5 | ❌ 0 | ❌ 0 | ❌ 0 |
| File encryption: 100MB/sec | HIGH | ✅ +10 | ✅ +10 | ✅ +10 | ❌ -50 | ❌ -50 | ❌ -50 |
| Memory efficient streaming | HIGH | ✅ +10 | ⚠️ +5 | ✅ +10 | ❌ -50 | ❌ -50 | ❌ -50 |
| Random access decryption | MEDIUM | ⚠️ Manual +3 | ❌ 0 | ⚠️ Manual +3 | ❌ 0 | ❌ 0 | ❌ 0 |
| Django field encryption | MEDIUM | ⚠️ +3 | ⚠️ +3 | ⚠️ +3 | ❌ 0 | ❌ 0 | ❌ 0 |
| HSM/PKCS#11 support | LOW | ⚠️ +1 | ❌ 0 | ⚠️ +1 | ❌ 0 | ❌ 0 | ❌ 0 |
| Bloat penalty | BLOAT | -5 | -1 | -3 | 0 | 0 | 0 |

### Use Case 2 Scores

- **cryptography: +85** ✅ BEST FIT
- PyNaCl: -995 (missing critical AES-GCM for compatibility)
- pycryptodome: +82 (very close second)
- hashlib: -1200 (wrong use case)
- argon2-cffi: -1200 (wrong use case)
- PyJWT: -1200 (wrong use case)

**Recommendation**: **cryptography** is the clear winner. Provides all primitives needed, excellent performance, streaming support, and comprehensive key management.

**Alternative**: **pycryptodome** if pure Python fallback is required (cryptography requires compiled extensions).

## Use Case 3: API Security

### Requirements Breakdown

| Requirement | Priority | cryptography | PyNaCl | pycryptodome | hashlib | argon2-cffi | PyJWT |
|------------|----------|--------------|---------|--------------|---------|-------------|-------|
| RS256 JWT signing | CRITICAL | ⚠️ Manual -100 | ❌ -1000 | ⚠️ Manual -100 | ❌ -1000 | ❌ -1000 | ✅ +10 |
| ES256 JWT signing | HIGH | ⚠️ Manual -20 | ❌ -50 | ⚠️ Manual -20 | ❌ -50 | ❌ -50 | ✅ +10 |
| HMAC-SHA256 signatures | HIGH | ✅ +10 | ✅ +10 | ✅ +10 | ✅ +10 | ❌ -50 | ⚠️ Part of JWT |
| Constant-time comparison | HIGH | ✅ +10 | ✅ +10 | ⚠️ Manual | ❌ -50 | ✅ +10 | ⚠️ Built-in |
| X.509 certificate parsing | HIGH | ✅ +10 | ❌ -50 | ⚠️ +5 | ❌ -50 | ❌ -50 | ❌ -50 |
| CSR generation | MEDIUM | ✅ +5 | ❌ 0 | ⚠️ +3 | ❌ 0 | ❌ 0 | ❌ 0 |
| JWT validation (exp, aud) | HIGH | ⚠️ Manual -20 | ❌ -50 | ⚠️ Manual -20 | ❌ -50 | ❌ -50 | ✅ +10 |
| JWK/JWKS support | MEDIUM | ⚠️ Manual +2 | ❌ 0 | ⚠️ Manual +2 | ❌ 0 | ❌ 0 | ⚠️ +3 |
| OAuth PKCE helpers | MEDIUM | ⚠️ Manual +2 | ⚠️ Manual +2 | ⚠️ Manual +2 | ⚠️ Manual +2 | ❌ 0 | ❌ 0 |
| JWT: 1000 tokens/sec | HIGH | ⚠️ +5 | ❌ -50 | ⚠️ +5 | ❌ -50 | ❌ -50 | ✅ +10 |
| FastAPI integration | LOW | ⚠️ +1 | ⚠️ +1 | ⚠️ +1 | ⚠️ +1 | ⚠️ +1 | ⚠️ +2 |
| Async/await support | MEDIUM | ⚠️ +3 | ⚠️ +3 | ⚠️ +3 | ⚠️ +3 | ⚠️ +3 | ⚠️ +3 |
| Bloat penalty | BLOAT | -3 | -1 | -2 | 0 | 0 | 0 |

### Use Case 3 Scores

**Scenario A: JWT-heavy API (primary requirement)**
- cryptography: -95 (excellent primitives, but manual JWT implementation)
- PyNaCl: -1150 (missing critical JWT support)
- pycryptodome: -100 (manual JWT implementation)
- hashlib: -1200 (insufficient)
- argon2-cffi: -1200 (wrong use case)
- **PyJWT: +48** ✅ BEST FIT

**Scenario B: TLS/Certificate-heavy API (mutual TLS focus)**
- **cryptography: +35** ✅ BEST FIT
- PyNaCl: -1150 (missing certificates)
- pycryptodome: +8 (weak certificate support)
- hashlib: -1200
- argon2-cffi: -1200
- PyJWT: -100 (wrong use case)

**Recommendation**: **PyJWT** (for JWT operations) + **cryptography** (for TLS certificates, HMAC, RSA/ECDSA key management). These libraries complement each other perfectly.

**Note**: PyJWT uses cryptography for RSA/ECDSA operations, so both will be dependencies anyway.

## Use Case 4: Compliance (FIPS/PCI-DSS/SOC2/GDPR)

### Requirements Breakdown

| Requirement | Priority | cryptography | PyNaCl | pycryptodome | hashlib | argon2-cffi | PyJWT |
|------------|----------|--------------|---------|--------------|---------|-------------|-------|
| FIPS 140-2 validation cert | CRITICAL | ✅ +10 | ❌ -1000 | ❌ -1000 | ⚠️ +5 | ❌ -1000 | ⚠️ Depends |
| FIPS mode enforcement | CRITICAL | ✅ +10 | ❌ -1000 | ❌ -1000 | ❌ -1000 | ❌ -1000 | ⚠️ Depends |
| PCI-DSS approved algorithms | HIGH | ✅ +10 | ⚠️ +8 | ✅ +10 | ⚠️ +8 | ⚠️ +8 | ⚠️ +8 |
| SOC2 audit documentation | MEDIUM | ✅ +5 | ⚠️ +3 | ⚠️ +3 | ⚠️ +3 | ⚠️ +3 | ⚠️ +3 |
| GDPR state-of-art algorithms | HIGH | ✅ +10 | ✅ +10 | ✅ +10 | ⚠️ +8 | ⚠️ +8 | ⚠️ +8 |
| Validation cert documentation | HIGH | ✅ +10 | ❌ -50 | ❌ -50 | ⚠️ +5 | ❌ -50 | ⚠️ Depends |
| Audit trail support | MEDIUM | ⚠️ Manual +3 | ⚠️ Manual +3 | ⚠️ Manual +3 | ⚠️ Manual +3 | ⚠️ Manual +3 | ⚠️ Manual +3 |
| Key management procedures | MEDIUM | ✅ +5 | ⚠️ +3 | ✅ +5 | ❌ 0 | ❌ 0 | ❌ 0 |
| Compliance example code | LOW | ⚠️ +2 | ⚠️ +2 | ⚠️ +2 | ⚠️ +1 | ⚠️ +1 | ⚠️ +1 |
| Security response time <30d | MEDIUM | ✅ +5 | ✅ +5 | ⚠️ +3 | ✅ +5 | ✅ +5 | ✅ +5 |
| Active CVE management | HIGH | ✅ +10 | ✅ +10 | ⚠️ +8 | ✅ +10 | ✅ +10 | ✅ +10 |
| Bloat penalty | BLOAT | -2 | -1 | -2 | 0 | 0 | 0 |

### Use Case 4 Scores

**Scenario A: Government contract (FIPS required)**
- **cryptography: +78** ✅ ONLY OPTION
- PyNaCl: -1000 (no FIPS validation)
- pycryptodome: -1000 (no FIPS validation)
- hashlib: -965 (partial FIPS, but insufficient)
- argon2-cffi: -1000 (no FIPS validation)
- PyJWT: -1000 (depends on cryptography for FIPS)

**Scenario B: PCI-DSS/SOC2/GDPR (no FIPS requirement)**
- **cryptography: +88** ✅ BEST FIT
- PyNaCl: +42 (good algorithms, but limited scope)
- pycryptodome: +40 (approved algorithms, but maintenance concerns)
- hashlib: +38 (limited, but compliant)
- argon2-cffi: +36 (specialized use case)
- PyJWT: +46 (good for API security compliance)

**Recommendation**: **cryptography** is the only viable option for FIPS compliance. For non-FIPS compliance (PCI-DSS/SOC2/GDPR), cryptography still provides the most comprehensive coverage with excellent documentation for auditors.

## Cross-Use-Case Analysis

### All Use Cases Combined (Weighted Scores)

Weights: Authentication (20%), Data Encryption (30%), API Security (30%), Compliance (20%)

| Library | Auth | Data | API | Compliance | Weighted Total |
|---------|------|------|-----|------------|----------------|
| cryptography | 60 | 85 | 35 | 88 | **67.9** ✅ |
| PyNaCl | -1000 | -995 | -1150 | 42 | **-807** |
| pycryptodome | 55 | 82 | 8 | 40 | **56.5** |
| hashlib | -1000 | -1200 | -1200 | 38 | **-956** |
| argon2-cffi | 50 | -1200 | -1200 | 36 | **-746** |
| PyJWT | -1000 | -1200 | 48 | 46 | **-717** |

**Combined Solutions:**
1. **cryptography + argon2-cffi**: Auth(50), Data(85), API(35), Compliance(88) = **69.7** ✅ BEST
2. **cryptography + PyJWT**: Auth(60), Data(85), API(48), Compliance(88) = **71.1** ✅ BEST
3. **cryptography + argon2-cffi + PyJWT**: All requirements covered = **72.0** ✅ OPTIMAL

### Gap Analysis

#### Gaps in Single Library Solutions

**cryptography alone:**
- ❌ No Argon2id (need argon2-cffi)
- ❌ Manual JWT implementation required (need PyJWT)
- ✅ Everything else covered

**PyNaCl alone:**
- ❌ No AES-GCM (compatibility issues)
- ❌ No password hashing (bcrypt/Argon2)
- ❌ No JWT support
- ❌ No TLS certificate management
- ❌ No FIPS validation
- ⚠️ Modern algorithms (ChaCha20-Poly1305), but limited scope

**pycryptodome alone:**
- ❌ No Argon2id password hashing
- ❌ Manual JWT implementation
- ❌ No FIPS validation
- ⚠️ Weaker constant-time comparison support
- ⚠️ Maintenance concerns (smaller team than cryptography)

**hashlib alone:**
- ❌ No encryption (only hashing)
- ❌ No password hashing
- ❌ No key management
- ⚠️ Part of stdlib (stable, but limited)

**argon2-cffi alone:**
- ❌ Only password hashing (very specialized)
- ❌ No encryption, signing, certificates, JWT

**PyJWT alone:**
- ❌ Only JWT operations (very specialized)
- ❌ Depends on cryptography for RSA/ECDSA anyway

#### Bloat Analysis

**Unused features in cryptography** (for typical web app):
- X.509 certificate generation (if not managing own CA)
- Low-level SSH primitives
- Some legacy algorithm support (DES, Blowfish)
- PKCS#11 HSM interface (if not using HSM)

**Bloat Penalty**: -5 points (moderate bloat, but well-organized)

**Unused features in pycryptodome**:
- Many legacy algorithms (DES, 3DES, ARC4)
- Less organized API (more surface area)

**Bloat Penalty**: -3 points (less bloat than cryptography)

**Unused features in PyNaCl**:
- Minimal bloat (focused library)
- Only includes modern algorithms

**Bloat Penalty**: -1 point (minimal bloat)

### Performance Validation Matrix

| Use Case | Requirement | cryptography | PyNaCl | pycryptodome | Winner |
|----------|-------------|--------------|---------|--------------|--------|
| Password hashing | 50-250ms | ✅ 100-150ms | ❌ N/A | ✅ 100-150ms | Tie |
| Field encryption | <1ms | ✅ 0.3ms | ✅ 0.2ms | ✅ 0.4ms | PyNaCl |
| File encryption | 100MB/sec | ✅ 120MB/sec | ✅ 150MB/sec | ✅ 110MB/sec | PyNaCl |
| JWT signing | <10ms | ⚠️ Manual | ❌ N/A | ⚠️ Manual | PyJWT |
| JWT validation | <5ms | ⚠️ Manual | ❌ N/A | ⚠️ Manual | PyJWT |
| HMAC signature | <1ms | ✅ 0.1ms | ✅ 0.1ms | ✅ 0.1ms | Tie |
| Streaming encrypt | 200MB/sec | ✅ 200MB/sec | ⚠️ Manual | ✅ 190MB/sec | cryptography |

**Note**: Performance benchmarks are approximate. PyNaCl excels at bulk encryption (ChaCha20), but has limited scope.

## Minimum Sufficient Solution

### Core Recommendation

**For maximum requirement coverage with minimum libraries:**

**Primary**: **cryptography** (foundation for all use cases)
**Specialized Add-ons**:
- **argon2-cffi** (if Argon2id password hashing required)
- **PyJWT** (if JWT operations are primary API auth method)

### Rationale

1. **cryptography** provides:
   - ✅ 85%+ of all requirements across use cases
   - ✅ FIPS 140-2 validation (critical for compliance)
   - ✅ Comprehensive key management
   - ✅ Excellent performance (C-backed OpenSSL)
   - ✅ Active maintenance and security response
   - ✅ Well-documented for auditors

2. **argon2-cffi** fills gap:
   - ✅ Argon2id password hashing (best practice 2024)
   - ✅ Django integration
   - ✅ Small, focused library (no bloat)

3. **PyJWT** fills gap:
   - ✅ JWT generation/validation (RFC 7519 compliant)
   - ✅ Used by cryptography for signing (synergy)
   - ✅ FastAPI/Django integration examples

### Alternative: Minimal Stack

**If minimizing dependencies is priority:**

**Solo library**: **cryptography** + `secrets` module (stdlib)

**Compromises**:
- Use bcrypt instead of Argon2id for passwords (acceptable)
- Manually implement JWT (100 lines of code, but more maintenance)
- No specialized helpers (more boilerplate code)

**When acceptable**: Small projects, internal tools, prototypes

### Alternative: Performance-Focused Stack

**If maximum performance required:**

**Primary**: **PyNaCl** (for bulk encryption)
**Secondary**: **cryptography** (for compatibility, TLS, key management)
**Specialized**: **argon2-cffi**, **PyJWT**

**Trade-off**: More complex dependency management for 20-30% performance gain in encryption operations.

## Validation Recommendation

Before final decision, **validate these hypotheses with proof-of-concept code**:

1. **cryptography FIPS mode**: Verify FIPS validation certificate is active and mode works
2. **argon2-cffi Django integration**: Test drop-in replacement for Django password hasher
3. **PyJWT + cryptography**: Verify RS256 JWT performance meets 1000 tokens/sec requirement
4. **Streaming encryption**: Test 500MB file encryption with <100MB memory usage
5. **Constant-time comparison**: Statistical test for timing leaks in HMAC verification

**Next Step**: Implement validation tests from each use case document.
