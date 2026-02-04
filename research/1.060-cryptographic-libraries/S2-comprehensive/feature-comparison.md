# Feature Comparison: Cryptographic Primitives and API Capabilities

## Executive Summary

This document provides a systematic comparison of cryptographic primitives, algorithms, and API capabilities across the four Python cryptographic options. The analysis evaluates each library's breadth of features, algorithm support, and API design philosophy to inform selection decisions based on technical requirements.

## Cryptographic Primitive Coverage Matrix

### Symmetric Encryption

| Algorithm/Mode | cryptography | PyNaCl | pycryptodome | hashlib |
|----------------|-------------|---------|--------------|---------|
| **AES** | ✅ Full | ❌ No | ✅ Full | ❌ No |
| **ChaCha20** | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **XSalsa20** | ❌ No | ✅ Yes (SecretBox) | ✅ Yes | ❌ No |
| **XChaCha20** | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **TripleDES** | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **Camellia** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Blowfish** | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **CAST** | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **ARC4/RC4** | ❌ No | ❌ No | ✅ Yes (legacy) | ❌ No |

**Analysis**:
- **cryptography**: Comprehensive modern cipher support via OpenSSL
- **PyNaCl**: Only XSalsa20 (opinionated, modern choice)
- **pycryptodome**: Widest cipher selection including legacy algorithms
- **hashlib**: Not applicable (hashing only)

### Block Cipher Modes

| Mode | cryptography | PyNaCl | pycryptodome | hashlib |
|------|-------------|---------|--------------|---------|
| **CBC** | ✅ Yes | ❌ No | ✅ Yes | N/A |
| **CTR** | ✅ Yes | ❌ No | ✅ Yes | N/A |
| **CFB** | ✅ Yes | ❌ No | ✅ Yes | N/A |
| **OFB** | ✅ Yes | ❌ No | ✅ Yes | N/A |
| **ECB** | ✅ Yes | ❌ No | ✅ Yes (not recommended) | N/A |
| **XTS** | ✅ Yes | ❌ No | ❌ No | N/A |
| **GCM** (AEAD) | ✅ Yes | ❌ No | ✅ Yes | N/A |
| **CCM** (AEAD) | ✅ Yes | ❌ No | ✅ Yes | N/A |
| **EAX** (AEAD) | ❌ No | ❌ No | ✅ Yes | N/A |
| **SIV** (AEAD) | ❌ No | ❌ No | ✅ Yes | N/A |
| **OCB** (AEAD) | ✅ Yes | ❌ No | ✅ Yes | N/A |

**Analysis**:
- **cryptography**: Standard modes well-covered
- **PyNaCl**: No mode selection (uses XSalsa20-Poly1305 AEAD by default)
- **pycryptodome**: Most comprehensive AEAD mode support (EAX, SIV)
- **hashlib**: Not applicable

**Winner**: pycryptodome (most modes), cryptography (production-standard modes)

### Asymmetric Encryption & Key Exchange

| Algorithm | cryptography | PyNaCl | pycryptodome | hashlib |
|-----------|-------------|---------|--------------|---------|
| **RSA** | ✅ Full (OAEP, PKCS#1) | ❌ No | ✅ Full | ❌ No |
| **ECDH** | ✅ Yes (multiple curves) | ✅ X25519 only | ✅ Yes | ❌ No |
| **X25519** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **X448** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **ElGamal** | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **DH (classic)** | ✅ Yes | ❌ No | ❌ No | ❌ No |

**ECC Curves**:
- **cryptography**: secp256r1, secp384r1, secp521r1, secp256k1, BrainpoolP curves, Curve25519, Curve448
- **PyNaCl**: Curve25519 only
- **pycryptodome**: NIST curves, limited selection

**Analysis**:
- **cryptography**: Most comprehensive - RSA + extensive ECC support
- **PyNaCl**: Modern only (X25519), no RSA
- **pycryptodome**: Traditional support (RSA, ElGamal, basic ECC)
- **hashlib**: Not applicable

**Winner**: cryptography (breadth), PyNaCl (modern simplicity)

### Digital Signatures

| Algorithm | cryptography | PyNaCl | pycryptodome | hashlib |
|-----------|-------------|---------|--------------|---------|
| **RSA-PSS** | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **RSA-PKCS#1 v1.5** | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **ECDSA** | ✅ Yes (multiple curves) | ❌ No | ✅ Yes | ❌ No |
| **Ed25519** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Ed448** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **DSA** | ✅ Yes (legacy) | ❌ No | ✅ Yes | ❌ No |

**Analysis**:
- **cryptography**: Complete signature suite (RSA, ECDSA, EdDSA)
- **PyNaCl**: Ed25519 only (modern, recommended)
- **pycryptodome**: Traditional signatures (RSA, DSA, ECDSA), missing EdDSA
- **hashlib**: Not applicable

**Winner**: cryptography (comprehensive), PyNaCl (modern best practice)

### Hashing Algorithms

| Algorithm | cryptography | PyNaCl | pycryptodome | hashlib |
|-----------|-------------|---------|--------------|---------|
| **SHA-256** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **SHA-512** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **SHA-3** | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| **BLAKE2b** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **BLAKE2s** | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| **SHA-1** | ✅ Yes (legacy) | ❌ No | ✅ Yes | ✅ Yes |
| **MD5** | ✅ Yes (legacy) | ❌ No | ✅ Yes | ✅ Yes |
| **SHAKE** | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| **Keccak** | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **RIPEMD-160** | ❌ No | ❌ No | ✅ Yes | ❌ No |

**Analysis**:
- **cryptography**: Modern hashes well-covered
- **PyNaCl**: Limited to BLAKE2b and SHA via stdlib
- **pycryptodome**: Most comprehensive hash collection
- **hashlib**: Excellent coverage of standard algorithms

**Winner**: pycryptodome (breadth), hashlib (stdlib integration)

### Message Authentication Codes (MAC)

| MAC Type | cryptography | PyNaCl | pycryptodome | hashlib |
|----------|-------------|---------|--------------|---------|
| **HMAC** | ✅ Yes | ❌ Stdlib | ✅ Yes | ✅ Yes (hmac module) |
| **CMAC** | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **Poly1305** | ✅ Yes | ✅ Yes (integrated) | ✅ Yes | ❌ No |
| **GMAC** | ✅ Via GCM | ❌ No | ✅ Via GCM | ❌ No |

**Analysis**:
- **cryptography**: Full MAC support
- **PyNaCl**: Poly1305 integrated in SecretBox/Box (automatic)
- **pycryptodome**: Comprehensive MAC support
- **hashlib**: HMAC via separate stdlib module

### Key Derivation Functions (KDF)

| KDF | cryptography | PyNaCl | pycryptodome | hashlib |
|-----|-------------|---------|--------------|---------|
| **PBKDF2** | ✅ Yes | ❌ Stdlib | ✅ Yes | ✅ Yes |
| **HKDF** | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **Scrypt** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Argon2** | ✅ Separate pkg | ✅ Yes | ❌ Separate pkg | ❌ No |
| **bcrypt** | ✅ Separate pkg | ❌ No | ✅ Yes | ❌ No |
| **Concatkdf** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **X963KDF** | ✅ Yes | ❌ No | ❌ No | ❌ No |

**Analysis**:
- **cryptography**: Most comprehensive KDF suite
- **PyNaCl**: Modern password hashing (Argon2, Scrypt)
- **pycryptodome**: Good coverage including bcrypt
- **hashlib**: Basic PBKDF2 only

**Winner**: cryptography (variety), PyNaCl (password hashing quality)

## Feature Coverage Summary

### Algorithm Breadth Score (out of 100)

| Library | Symmetric | Asymmetric | Signatures | Hashing | MAC/KDF | **Total** |
|---------|-----------|------------|------------|---------|---------|-----------|
| **cryptography** | 90 | 95 | 95 | 85 | 90 | **91** |
| **PyNaCl** | 40 | 50 | 50 | 40 | 60 | **48** |
| **pycryptodome** | 95 | 75 | 70 | 95 | 85 | **84** |
| **hashlib** | 0 | 0 | 0 | 90 | 30 | **24*** |

*hashlib score is limited by scope (hashing only)

**Key Insights**:
1. **cryptography**: Most comprehensive (91/100)
2. **pycryptodome**: Wide algorithm selection (84/100)
3. **PyNaCl**: Narrow but modern (48/100) - intentionally limited
4. **hashlib**: Excellent for hashing, incomplete for crypto (24/100)

## API Design Philosophy Comparison

### cryptography

**Design**: Two-layer architecture
- **Layer 1 - Recipes**: High-level, opinionated APIs (Fernet)
- **Layer 2 - Hazmat**: Low-level primitives (maximum flexibility)

**Philosophy**:
- "Make the right thing easy, make the wrong thing hard"
- Provide both convenience and control
- Explicit > implicit for security decisions

**Examples**:
```python
# High-level (Fernet - recommended)
from cryptography.fernet import Fernet
f = Fernet(Fernet.generate_key())
token = f.encrypt(b"secret")

# Low-level (Hazmat - expert use)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
encryptor = cipher.encryptor()
```

**Strengths**:
- ✅ Flexibility for all skill levels
- ✅ Safe defaults available (Fernet)
- ✅ Low-level access when needed

**Weaknesses**:
- ⚠️ Complexity in hazmat layer
- ⚠️ Easy to misuse hazmat APIs

### PyNaCl

**Design**: High-level only
- Single layer of "crypto boxes"
- No low-level primitive access
- Pre-selected algorithm combinations

**Philosophy**:
- "Hard to misuse"
- Secure by default
- Minimal configuration
- Modern algorithms only

**Examples**:
```python
# Secret encryption (only way)
from nacl.secret import SecretBox
box = SecretBox(key)
encrypted = box.encrypt(b"message")  # Automatic nonce, auth

# Public-key encryption (only way)
from nacl.public import PrivateKey, Box
private = PrivateKey.generate()
box = Box(private, their_public_key)
encrypted = box.encrypt(b"message")
```

**Strengths**:
- ✅ Simplest API
- ✅ Very hard to misuse
- ✅ Automatic nonce/IV management
- ✅ Authenticated by default

**Weaknesses**:
- ❌ No low-level access
- ❌ Can't customize algorithm choices
- ❌ Limited to library's opinions

### pycryptodome

**Design**: Low-level only
- Direct primitive access
- Developer controls everything
- No high-level helpers

**Philosophy**:
- Maximum flexibility
- Developer responsibility
- Comprehensive algorithm access

**Examples**:
```python
# AES-GCM (must manage nonce, tag)
from Crypto.Cipher import AES
cipher = AES.new(key, AES.MODE_GCM)
ciphertext, tag = cipher.encrypt_and_digest(plaintext)
# Developer must store: nonce, tag, ciphertext separately

# RSA (must choose padding)
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
key = RSA.generate(2048)
cipher = PKCS1_OAEP.new(key.publickey())
ciphertext = cipher.encrypt(message)
```

**Strengths**:
- ✅ Maximum control
- ✅ Access to all algorithms
- ✅ Explicit configuration

**Weaknesses**:
- ❌ Easy to misuse
- ❌ Requires cryptographic expertise
- ❌ No "safe by default" layer

### hashlib

**Design**: Simple functional API
- Single-purpose: hashing
- Consistent interface across algorithms
- Streaming support

**Philosophy**:
- Simplicity for specific task
- Uniform API design
- Standard library reliability

**Examples**:
```python
# Simple hashing
import hashlib
digest = hashlib.sha256(data).hexdigest()

# Streaming (large files)
h = hashlib.sha256()
h.update(chunk1)
h.update(chunk2)
digest = h.hexdigest()
```

**Strengths**:
- ✅ Very simple
- ✅ Consistent API
- ✅ Hard to misuse (limited scope)

**Weaknesses**:
- ❌ Limited to hashing
- ❌ No encryption capabilities

## API Usability Comparison

| Aspect | cryptography | PyNaCl | pycryptodome | hashlib |
|--------|-------------|---------|--------------|---------|
| **Learning Curve** | Medium | Low | High | Very Low |
| **Ease of Use** | Good (recipes) / Complex (hazmat) | Excellent | Difficult | Excellent |
| **Safe Defaults** | ✅ Fernet | ✅ All APIs | ❌ None | ✅ Yes |
| **Misuse Risk** | Medium (hazmat) | Very Low | High | Very Low |
| **Flexibility** | High | Low | Very High | N/A |
| **Type Hints** | ✅ Excellent | ✅ Good | ⚠️ Partial | ✅ Excellent |
| **Documentation** | Excellent | Good | Good | Excellent |
| **Error Messages** | Good | Good | Technical | Clear |

**Usability Rankings**:
1. **hashlib**: Easiest (but limited scope)
2. **PyNaCl**: Easiest full crypto library
3. **cryptography** (recipes): Easy for common cases
4. **cryptography** (hazmat): Moderate difficulty
5. **pycryptodome**: Requires expertise

## Advanced Features Comparison

| Feature | cryptography | PyNaCl | pycryptodome | hashlib |
|---------|-------------|---------|--------------|---------|
| **X.509 Certificates** | ✅ Full support | ❌ No | ❌ No | ❌ No |
| **CSR Generation** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **PKCS#12** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **PEM/DER Encoding** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **SSH Keys** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **TLS/SSL Support** | ⚠️ Via ssl module | ❌ No | ❌ No | ❌ No |
| **Two-Factor Auth (OTP)** | ✅ Yes (separate) | ❌ No | ❌ No | ❌ No |
| **Constant-time Comparison** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes (secrets) |

**Winner**: cryptography (certificate/PKI support is unique)

## Performance Characteristics

| Operation | cryptography | PyNaCl | pycryptodome | hashlib |
|-----------|-------------|---------|--------------|---------|
| **RSA Encryption** | ⚡⚡⚡ Fast (OpenSSL) | ❌ N/A | 🐌 Slow (Python) | ❌ N/A |
| **AES-GCM** | ⚡⚡⚡ Fast (OpenSSL) | ❌ N/A | ⚡⚡ Good (C ext) | ❌ N/A |
| **ECC Operations** | ⚡⚡⚡ Fast | ⚡⚡⚡ Fast | ⚡⚡ Moderate | ❌ N/A |
| **Hashing (SHA-256)** | ⚡⚡⚡ Fast | ⚡⚡⚡ Fast | ⚡⚡⚡ Fast | ⚡⚡⚡ Fast |
| **Small Data AES** | ⚡⚡ Good | ❌ N/A | ⚡⚡⚡ Excellent | ❌ N/A |
| **Ed25519 Signing** | ⚡⚡⚡ Fast | ⚡⚡⚡ Very Fast | ❌ N/A | ❌ N/A |

**Performance Notes**:
- **cryptography**: Best overall (OpenSSL backend)
- **PyNaCl**: Excellent for supported operations (libsodium)
- **pycryptodome**: Good symmetric, poor RSA
- **hashlib**: Excellent for hashing (OpenSSL backend)

## Use Case Fit Analysis

### Use Case: Web Application (JWT, session encryption)

| Library | Fit Score | Rationale |
|---------|-----------|-----------|
| **cryptography** | 95/100 | Complete feature set, good performance, industry standard |
| **PyNaCl** | 85/100 | Excellent for simple encryption, lacks JWT helpers |
| **pycryptodome** | 70/100 | Sufficient but more complex API |
| **hashlib** | 30/100 | Insufficient (hashing only) |

**Recommendation**: cryptography (comprehensive) or PyNaCl (simplicity)

### Use Case: Government/Enterprise (FIPS required)

| Library | Fit Score | Rationale |
|---------|-----------|-----------|
| **cryptography** | 95/100 | Only option with FIPS path |
| **PyNaCl** | 0/100 | Not FIPS compliant |
| **pycryptodome** | 0/100 | Not FIPS validated |
| **hashlib** | 60/100 | FIPS hashing, but incomplete for crypto |

**Recommendation**: cryptography + hashlib (only viable option)

### Use Case: IoT/Embedded (resource constrained)

| Library | Fit Score | Rationale |
|---------|-----------|-----------|
| **cryptography** | 70/100 | OpenSSL dependency may be large |
| **PyNaCl** | 85/100 | Efficient, modern algorithms |
| **pycryptodome** | 90/100 | Self-contained, pure Python fallback |
| **hashlib** | 75/100 | Lightweight for hashing |

**Recommendation**: pycryptodome (portability) or PyNaCl (efficiency)

### Use Case: API Security (modern protocols)

| Library | Fit Score | Rationale |
|---------|-----------|-----------|
| **cryptography** | 90/100 | Ed25519, X25519, comprehensive |
| **PyNaCl** | 95/100 | Perfect fit - modern, simple |
| **pycryptodome** | 60/100 | Lacks Ed25519 |
| **hashlib** | 40/100 | Insufficient alone |

**Recommendation**: PyNaCl (modern simplicity) or cryptography (flexibility)

### Use Case: Legacy System Integration

| Library | Fit Score | Rationale |
|---------|-----------|-----------|
| **cryptography** | 85/100 | Good legacy algorithm support |
| **PyNaCl** | 30/100 | No legacy algorithms |
| **pycryptodome** | 95/100 | Excellent legacy support (DES, RC4, etc.) |
| **hashlib** | 70/100 | Legacy hash support |

**Recommendation**: pycryptodome (widest legacy coverage)

## Feature Recommendation Matrix

| Requirement | Best Choice | Rationale |
|-------------|-------------|-----------|
| **Broadest algorithm support** | cryptography | 91/100 coverage score |
| **Modern algorithms only** | PyNaCl | Curated modern cryptography |
| **Simplest API** | PyNaCl | Lowest misuse risk |
| **Legacy compatibility** | pycryptodome | Widest algorithm catalog |
| **Certificate handling** | cryptography | Only option with X.509 |
| **Best performance** | cryptography | OpenSSL-backed |
| **Hashing only** | hashlib | Purpose-built, stdlib |
| **Self-contained** | pycryptodome | No external dependencies |
| **FIPS compliance** | cryptography | Only viable path |
| **Password hashing** | PyNaCl (Argon2) | Modern, secure |

## Conclusion

The feature comparison reveals distinct positioning:

1. **cryptography**: Comprehensive feature leader
   - Broadest algorithm support
   - Only option for certificates/PKI
   - Best overall performance
   - FIPS compliance path

2. **PyNaCl**: Curated modern simplicity
   - Narrow but excellent modern algorithm selection
   - Easiest API, hardest to misuse
   - Perfect for modern applications without FIPS

3. **pycryptodome**: Algorithm breadth specialist
   - Widest algorithm catalog (including legacy)
   - Self-contained implementation
   - Best for legacy system integration

4. **hashlib**: Hashing specialist
   - Excellent for its scope
   - Insufficient alone for secure application development
   - Should be paired with comprehensive library

**Recommendation**: Choose based on requirements:
- **General purpose + FIPS**: cryptography
- **Modern + simple**: PyNaCl
- **Legacy + self-contained**: pycryptodome
- **Hashing only**: hashlib (but pair with crypto library for complete solution)
