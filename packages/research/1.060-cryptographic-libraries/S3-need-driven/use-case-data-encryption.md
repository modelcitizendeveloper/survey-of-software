# Use Case: Data Encryption

## Scenario Description

**Application**: Healthcare patient records management system
**Data Volume**: 2TB patient data, 5M individual records
**Technology Stack**: Python 3.11, PostgreSQL 14, S3-compatible object storage
**Compliance**: HIPAA, GDPR Article 32 (security of processing)

## Concrete Problems to Solve

### 1. Database Field-Level Encryption
- Encrypt sensitive PII fields (SSN, medical record numbers, diagnosis codes)
- 50,000+ patient records created daily
- Search capability on encrypted fields (deterministic encryption)
- Support key rotation without system downtime

**Current Pain Point**: Transparent database encryption (TDE) encrypts entire database, but application needs selective field access for audit logging.

### 2. File Encryption for Medical Documents
- Encrypt PDF/DICOM files stored in object storage
- File sizes: 100KB to 500MB (medical imaging)
- Concurrent upload/download by 500 clinicians
- Preserve metadata for search (filename, patient ID)
- Stream encryption for large files (no full file in memory)

**Current Pain Point**: Need to encrypt files before S3 upload, decrypt on download, without loading entire file in RAM.

### 3. Encryption Key Management
- Master key protection (cannot be stored in database)
- Data encryption key (DEK) wrapping with key encryption key (KEK)
- Key rotation quarterly without re-encrypting all data
- Audit trail: which key encrypted which data
- Support for HSM integration (future requirement)

**Current Pain Point**: No HSM currently, but may need FIPS 140-2 Level 3 compliance later.

### 4. Backup Encryption
- Encrypt PostgreSQL dumps before upload to backup storage
- 500GB daily backup size
- Streaming encryption (cannot load full dump in memory)
- Disaster recovery: key recovery procedures
- 7-year retention requirement

**Current Pain Point**: Backup encryption must not slow down backup window (2-hour maximum).

## Precise Requirements

### Field-Level Encryption Requirements

**MUST HAVE**:
- AES-256 encryption (FIPS 140-2 approved)
- Two modes: deterministic (searchable) and randomized (secure)
- Authenticated encryption (AEAD): detect tampering
- Per-field encryption (granular access control)
- Maximum ciphertext expansion: 50% (database storage)
- Support for NULL values (distinguish from empty string)

**NICE TO HAVE**:
- Format-preserving encryption (encrypted SSN still looks like SSN)
- Prefix-preserving encryption (support LIKE queries)

**PERFORMANCE TARGET**:
- Encrypt single field: <1ms (50-byte plaintext)
- Decrypt single field: <1ms
- Batch encrypt 10K fields: <5 seconds
- Zero performance degradation for non-encrypted columns

**COMPLIANCE**:
- FIPS 140-2 approved algorithm (AES-256-GCM)
- NIST SP 800-38D (GCM mode specification)
- Key management per NIST SP 800-57

### File Encryption Requirements

**MUST HAVE**:
- Streaming encryption/decryption (chunk-based)
- AES-256-GCM or ChaCha20-Poly1305
- Authenticated encryption (detect file tampering)
- Memory usage: <100MB for 500MB file
- Support for random access (decrypt specific chunks)
- File format: standard (not proprietary)

**NICE TO HAVE**:
- Compression before encryption
- Parallel chunk encryption

**PERFORMANCE TARGET**:
- Encryption throughput: 100MB/sec on standard hardware
- Decryption throughput: 100MB/sec
- Seek time (random chunk): <10ms
- 500MB file: encrypt in <5 seconds

**COMPLIANCE**:
- FIPS 140-2 approved algorithm
- GDPR Article 32: state-of-the-art encryption
- HIPAA: encryption of ePHI at rest

### Key Management Requirements

**MUST HAVE**:
- Key derivation function (KDF): PBKDF2/Argon2/HKDF
- Key wrapping: AES-KW (NIST SP 800-38F)
- Support envelope encryption pattern (DEK + KEK)
- Key versioning (track which key version encrypted data)
- Secure key generation (CSPRNG)
- Key serialization (store/load keys securely)

**NICE TO HAVE**:
- PKCS#11 interface for HSM support
- Key rotation utilities
- Automatic re-keying scheduler

**PERFORMANCE TARGET**:
- Key derivation: 50-200ms (slow is okay for security)
- Key unwrapping: <10ms
- DEK generation: <10ms

**COMPLIANCE**:
- NIST SP 800-57: key management lifecycle
- FIPS 140-2 key generation/storage
- Support for HSM (FIPS 140-2 Level 3) in future

### Backup Encryption Requirements

**MUST HAVE**:
- Streaming encryption (pipe PostgreSQL dump → encrypt → upload)
- AES-256-CTR or ChaCha20 (streaming-friendly modes)
- Authentication tag at end (HMAC or GCM)
- Memory usage: <200MB regardless of dump size
- Compatible with standard backup tools (pg_dump)

**NICE TO HAVE**:
- Compression integration
- Split archives (multi-part encryption)

**PERFORMANCE TARGET**:
- Encryption throughput: 200MB/sec minimum
- 500GB backup: encrypt in <45 minutes
- Zero impact on pg_dump performance
- Decrypt throughput: 200MB/sec (disaster recovery)

**COMPLIANCE**:
- HIPAA: encrypted backups of ePHI
- GDPR Article 32: backup encryption
- 7-year retention: ensure key availability

## Integration Constraints

### Database Constraints
- PostgreSQL 14 BYTEA or TEXT column storage
- Maximum column size: 1MB (large fields rare)
- No database extensions required (pure application-layer)
- Support Django ORM field-level encryption

### Object Storage Constraints
- S3-compatible API (MinIO deployment)
- Client-side encryption before upload (server cannot see plaintext)
- Standard HTTP streaming (no custom protocols)
- Metadata preservation (content-type, custom headers)

### Deployment Constraints
- Python 3.11+ (Ubuntu 22.04 LTS)
- No C compiler on production servers
- Pre-compiled wheels or pure Python acceptable
- No external key management service (initially)

### Key Storage Constraints
- Master key stored in environment variable (initial implementation)
- DEKs stored in database (encrypted by KEK)
- Future: HSM integration via PKCS#11
- Key backup stored in offline secure location

## Validation Tests Required

### 1. Encryption/Decryption Correctness
```python
# Verify round-trip encryption
plaintext = b"Sensitive PII data: SSN 123-45-6789"
key = generate_encryption_key()

ciphertext = encrypt(plaintext, key)
assert ciphertext != plaintext, "Encryption failed"
assert len(ciphertext) <= len(plaintext) * 1.5, "Excessive ciphertext expansion"

decrypted = decrypt(ciphertext, key)
assert decrypted == plaintext, "Decryption failed"
```

### 2. Authentication Tag Validation
```python
# Verify tampering detection
ciphertext = encrypt(b"Original data", key)
tampered = bytearray(ciphertext)
tampered[10] ^= 0xFF  # Flip one bit

try:
    decrypt(bytes(tampered), key)
    assert False, "Tampering not detected"
except AuthenticationError:
    pass  # Expected
```

### 3. Streaming Encryption Test
```python
# Verify memory-efficient streaming
import io
import psutil

process = psutil.Process()
mem_before = process.memory_info().rss

# Encrypt 500MB file
with open("/tmp/large_file.bin", "rb") as infile:
    with open("/tmp/encrypted.bin", "wb") as outfile:
        stream_encrypt(infile, outfile, key, chunk_size=64*1024)

mem_after = process.memory_info().rss
mem_used_mb = (mem_after - mem_before) / 1024 / 1024

assert mem_used_mb < 100, f"Excessive memory usage: {mem_used_mb}MB"
```

### 4. Key Rotation Test
```python
# Verify key rotation without data re-encryption
old_key = generate_key()
new_key = generate_key()

# Encrypt DEK with old KEK
dek = generate_data_encryption_key()
wrapped_dek_v1 = key_wrap(dek, old_key, version=1)

# Re-wrap with new KEK
dek_unwrapped = key_unwrap(wrapped_dek_v1, old_key)
wrapped_dek_v2 = key_wrap(dek_unwrapped, new_key, version=2)

# Data encrypted with DEK remains accessible
ciphertext = encrypt(b"data", dek)
assert decrypt(ciphertext, dek_unwrapped) == b"data"
```

### 5. Performance Benchmark
```python
# Measure field encryption performance
import time

fields = [f"SSN-{i:09d}".encode() for i in range(10000)]
start = time.perf_counter()

for field in fields:
    ciphertext = encrypt_field(field, key)

elapsed = time.perf_counter() - start
per_field_ms = (elapsed / len(fields)) * 1000

assert per_field_ms < 1.0, f"Too slow: {per_field_ms}ms per field"
print(f"Performance: {per_field_ms:.3f}ms per field")
```

### 6. Deterministic Encryption Test
```python
# Verify deterministic mode for searchable encryption
plaintext = b"123-45-6789"

ct1 = encrypt_deterministic(plaintext, key)
ct2 = encrypt_deterministic(plaintext, key)

assert ct1 == ct2, "Deterministic encryption not consistent"

# But different plaintexts produce different ciphertexts
plaintext2 = b"987-65-4321"
ct3 = encrypt_deterministic(plaintext2, key)
assert ct3 != ct1, "Collision in deterministic encryption"
```

## Success Criteria

### Functional Success
- Field-level encryption working in Django ORM
- 500MB file encryption in <5 seconds
- Key rotation procedure tested and documented
- Backup encryption integrated with pg_dump pipeline

### Performance Success
- Field encryption: <1ms measured (not theoretical)
- File throughput: >100MB/sec on production hardware
- Memory usage: <100MB for 500MB file encryption
- Backup window: <2 hours including encryption

### Compliance Success
- FIPS 140-2 approved algorithms used exclusively
- NIST SP 800-57 key management documented
- HIPAA encryption requirements satisfied (audit evidence)
- GDPR Article 32 technical measures documented

### Integration Success
- Django ORM transparent encryption (minimal code changes)
- S3 upload pipeline with client-side encryption
- PostgreSQL backup scripts with streaming encryption
- No changes to application logic required

## Library Evaluation Criteria

### Primary Criteria (Deal-Breakers)
1. Provides AES-256-GCM authenticated encryption
2. Streaming encryption/decryption support
3. Key wrapping/unwrapping functions
4. FIPS 140-2 validated implementation (or mode)
5. Key derivation functions (PBKDF2/HKDF)

### Secondary Criteria (Scoring)
- Support for deterministic encryption: +5 points
- PKCS#11 HSM interface: +5 points
- Format-preserving encryption: +3 points
- Built-in key rotation utilities: +3 points
- Django integration examples: +2 points

### Negative Criteria (Penalties)
- Pure Python implementation (too slow): -10 points
- Proprietary file formats: -5 points
- No streaming support: -10 points (deal-breaker)
- Deprecated algorithms (AES-CBC without auth): -5 points
- No key management support: -5 points

## Expected Library Fit

Based on requirements, ideal library should provide:
- Low-level primitives: AES-GCM, key wrapping, KDF
- High-level recipes: Fernet, envelope encryption patterns
- Streaming support: chunk-based encryption
- FIPS mode: validated cryptographic module

**Hypothesis**: `cryptography` library likely provides all primitives. Need to validate streaming patterns and Django integration.
