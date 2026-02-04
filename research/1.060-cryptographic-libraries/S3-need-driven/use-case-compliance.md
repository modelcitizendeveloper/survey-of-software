# Use Case: Compliance and Regulatory Requirements

## Scenario Description

**Organization**: Financial services company (FinTech)
**Regulatory Scope**: Multi-jurisdictional (US, EU, UK)
**Compliance Frameworks**: FIPS 140-2, PCI-DSS v4.0, SOC2 Type II, GDPR Article 32
**Audit Frequency**: Annual SOC2, quarterly PCI-DSS scans, GDPR ongoing

## Concrete Problems to Solve

### 1. FIPS 140-2 Compliance for Government Contracts
- Use only FIPS-validated cryptographic modules
- Document validation certificate numbers
- Demonstrate exclusive use of approved algorithms
- Provide audit trail of cryptographic operations
- Support for "FIPS mode" enforcement

**Current Pain Point**: Need to prove cryptographic library has FIPS 140-2 validation certificate (not just "FIPS-approved algorithms").

### 2. PCI-DSS Strong Cryptography Requirements
- Cardholder data encryption at rest (AES-256)
- Transmission security (TLS 1.2+)
- Key management procedures (requirement 3.5-3.7)
- Cryptographic key strength (requirement 3.6.1)
- Documentation for QSA (Qualified Security Assessor)

**Current Pain Point**: QSA requires evidence that keys are generated, stored, and destroyed per PCI requirements. Need documented procedures.

### 3. SOC2 Trust Services Criteria CC6
- Logical access controls (authentication)
- Encryption of sensitive data (CC6.1)
- Key management (CC6.7)
- Annual audit evidence collection
- Control effectiveness demonstration

**Current Pain Point**: Auditors need screenshots, code samples, and test results proving cryptographic controls are effective.

### 4. GDPR Article 32 Technical Safeguards
- Pseudonymization and encryption of personal data
- Confidentiality and integrity guarantees
- State-of-the-art cryptographic techniques
- Data breach notification (72 hours if encryption broken)
- Documentation for DPA (Data Protection Authority)

**Current Pain Point**: Need to justify cryptographic choices as "state-of-the-art" to EU DPA during audits.

## Precise Requirements

### FIPS 140-2 Requirements

**MUST HAVE**:
- Cryptographic module with FIPS 140-2 validation certificate
- Certificate number traceable to NIST CMVP database
- Validation level: Level 1 minimum (Level 2+ if HSM used)
- Approved algorithms only: AES, RSA (2048+), SHA-256+, HMAC
- FIPS mode enforcement (reject non-approved algorithms)
- Validation certificate covers Python bindings (not just C library)

**NICE TO HAVE**:
- FIPS 140-3 validation (newer standard)
- Higher validation levels (2, 3, 4)
- Module version pinning (validation specific to version)

**PERFORMANCE TARGET**:
- No significant performance degradation in FIPS mode
- FIPS mode toggle: <100ms on application startup
- Validation: zero non-approved algorithm usage

**COMPLIANCE**:
- NIST CMVP validation certificate required
- Validation in-process acceptable if recent (not obsolete)
- Must document certificate number in compliance documentation
- Annual re-verification that certificate is still active

### PCI-DSS Requirements

**MUST HAVE** (Requirement 3 - Protect Cardholder Data):
- AES-256 encryption for cardholder data at rest
- Key strength: 256-bit symmetric, 2048-bit RSA minimum
- Key management: generation, distribution, storage, rotation, destruction
- Cryptographic key access controls (least privilege)
- Key split knowledge (multi-party control for key recovery)
- Documentation: key management policy, procedures, audit logs

**MUST HAVE** (Requirement 4 - Encrypt Transmission):
- TLS 1.2 or TLS 1.3 only
- Strong cipher suites (no RC4, no export ciphers)
- Certificate validation (no self-signed in production)
- Certificate expiry monitoring

**NICE TO HAVE**:
- HSM integration for key storage
- Automatic key rotation
- Key usage logging

**PERFORMANCE TARGET**:
- Encryption performance sufficient for transaction volumes (100 TPS)
- TLS handshake: <100ms p95
- No impact on payment processing latency

**COMPLIANCE**:
- QSA audit evidence: code review, penetration test, documentation
- Quarterly vulnerability scans pass
- Annual PCI-DSS Report on Compliance (ROC)

### SOC2 Requirements

**MUST HAVE** (CC6.1 - Logical Access):
- Strong authentication (MFA support)
- Password hashing (Argon2/bcrypt)
- Session management (secure tokens)
- Access control enforcement

**MUST HAVE** (CC6.7 - Encryption):
- Encryption of sensitive data in transit and at rest
- Key management procedures documented
- Regular key rotation (at least annually)
- Encryption failure detection and alerting

**MUST HAVE** (Audit Evidence):
- Code samples demonstrating cryptographic implementation
- Test results showing encryption effectiveness
- Logs of key rotation events
- Incident response procedures for key compromise

**NICE TO HAVE**:
- Automated compliance monitoring
- Real-time encryption status dashboard
- Audit trail export functionality

**PERFORMANCE TARGET**:
- Audit evidence collection: <1 hour per year
- Zero failed controls in SOC2 Type II report
- Response time for auditor questions: <48 hours

**COMPLIANCE**:
- Annual SOC2 Type II audit pass
- Zero exceptions or deficiencies in cryptographic controls
- Management representation letter accuracy

### GDPR Article 32 Requirements

**MUST HAVE**:
- Encryption of personal data (PII) at rest and in transit
- Pseudonymization techniques (reversible de-identification)
- State-of-the-art cryptographic algorithms (current best practices)
- Integrity protection (detect unauthorized modification)
- Resilience of processing systems (key backup and recovery)

**MUST HAVE** (Documentation):
- Technical and organizational measures (TOMs) documentation
- Data breach impact assessment (if encryption broken, severity?)
- DPA reporting: which data encrypted, which algorithms used
- Justification for algorithm choices (why AES-256, not AES-128?)

**NICE TO HAVE**:
- Automated encryption verification
- Breach notification automation
- Privacy-enhancing technologies (PETs)

**PERFORMANCE TARGET**:
- Encryption does not significantly degrade user experience
- Data subject access requests (DSAR): decrypt within 30 days
- Breach assessment: determine encryption status within 24 hours

**COMPLIANCE**:
- GDPR Article 32 compliance documented
- DPA audit pass (if audited)
- Zero data breach notifications due to encryption failure
- DPIA (Data Protection Impact Assessment) approval

## Integration Constraints

### Documentation Requirements
- Compliance documentation directory in repository
- README explaining cryptographic choices
- Mapping: compliance requirement → code implementation
- Evidence collection scripts (for auditors)

### Audit Trail Requirements
- Log all key generation events (with metadata, not key material)
- Log key rotation events (old key version → new key version)
- Log encryption failures (with context, not sensitive data)
- Log access to encrypted data (user ID, timestamp, data type)
- Retain logs for 7 years (compliance requirement)

### Policy Requirements
- Key management policy document
- Cryptographic standard operating procedures (SOPs)
- Incident response plan for key compromise
- Annual cryptographic review process
- Vendor risk assessment for cryptographic library

### Testing Requirements
- Annual penetration test including cryptographic attacks
- Quarterly vulnerability scans of cryptographic implementations
- Automated tests for FIPS mode enforcement
- Regression tests for compliance requirements

## Validation Tests Required

### 1. FIPS Mode Enforcement Test
```python
# Verify only FIPS-approved algorithms work in FIPS mode
import os
os.environ['CRYPTOGRAPHY_FIPS'] = '1'  # Enable FIPS mode

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Approved algorithm should work
try:
    cipher = Cipher(algorithms.AES(b'0' * 32), modes.GCM(b'0' * 16), backend=default_backend())
    encryptor = cipher.encryptor()
    # Success expected
except Exception as e:
    assert False, f"AES-256-GCM should work in FIPS mode: {e}"

# Non-approved algorithm should fail
try:
    cipher = Cipher(algorithms.ChaCha20(b'0' * 32, b'0' * 16), backend=default_backend())
    encryptor = cipher.encryptor()
    assert False, "ChaCha20 should be rejected in FIPS mode"
except Exception:
    pass  # Expected - ChaCha20 not FIPS approved
```

### 2. Key Management Audit Trail Test
```python
# Verify all key operations are logged
import logging
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Setup audit logger
audit_logger = logging.getLogger('cryptographic_audit')
audit_logger.setLevel(logging.INFO)
handler = logging.FileHandler('/var/log/crypto_audit.log')
audit_logger.addHandler(handler)

# Generate key with audit trail
audit_logger.info("Key generation initiated", extra={
    "event": "key_generation",
    "key_type": "RSA",
    "key_size": 2048,
    "purpose": "JWT signing",
    "initiated_by": "admin_user_123"
})

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

audit_logger.info("Key generation completed", extra={
    "event": "key_generation_success",
    "key_fingerprint": "sha256:...",  # Hash of public key
    "timestamp": "2024-01-15T10:30:00Z"
})

# Verify audit log entry exists
with open('/var/log/crypto_audit.log', 'r') as f:
    logs = f.read()
    assert "key_generation" in logs
    assert "admin_user_123" in logs
    assert "RSA" in logs
```

### 3. PCI-DSS Key Strength Validation
```python
# Verify all keys meet PCI-DSS minimum strength requirements
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import algorithms

# Test RSA key strength
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
assert private_key.key_size >= 2048, "RSA key too weak for PCI-DSS"

# Test symmetric key strength
aes_key = os.urandom(32)  # 256 bits
assert len(aes_key) * 8 >= 256, "AES key too weak for PCI-DSS"

# Reject weak keys
weak_rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=1024)
assert weak_rsa_key.key_size < 2048, "Weak key should be rejected"
# In production, validation would raise exception
```

### 4. GDPR State-of-the-Art Verification
```python
# Document that algorithms used are state-of-the-art (2024 standards)
state_of_art_algorithms = {
    "symmetric_encryption": ["AES-256-GCM", "ChaCha20-Poly1305"],
    "asymmetric_encryption": ["RSA-2048", "RSA-4096", "ECDSA-P256"],
    "hashing": ["SHA-256", "SHA-384", "SHA-512", "Argon2id"],
    "key_derivation": ["PBKDF2", "Argon2id", "HKDF"],
    "message_auth": ["HMAC-SHA256", "HMAC-SHA512"]
}

# Verify library supports all state-of-the-art algorithms
from cryptography.hazmat.primitives.ciphers import algorithms
assert hasattr(algorithms, 'AES')
assert hasattr(algorithms, 'ChaCha20')

from cryptography.hazmat.primitives import hashes
assert hasattr(hashes, 'SHA256')
assert hasattr(hashes, 'SHA512')

# Generate compliance report
compliance_report = {
    "assessment_date": "2024-01-15",
    "standard": "GDPR Article 32",
    "algorithms_used": ["AES-256-GCM", "RSA-2048", "SHA-256", "Argon2id"],
    "state_of_art_status": "COMPLIANT",
    "justification": "All algorithms recommended by NIST, ENISA, BSI in 2024"
}
```

### 5. SOC2 Evidence Collection Test
```python
# Automate evidence collection for SOC2 audit
import json
from datetime import datetime, timedelta

def collect_soc2_evidence():
    evidence = {
        "control": "CC6.7 - Encryption of Sensitive Data",
        "collection_date": datetime.utcnow().isoformat(),
        "evidence_items": []
    }

    # Evidence 1: Encryption configuration
    evidence["evidence_items"].append({
        "type": "configuration",
        "description": "Encryption algorithm configuration",
        "data": {
            "algorithm": "AES-256-GCM",
            "key_size": 256,
            "mode": "AEAD (Authenticated Encryption)"
        }
    })

    # Evidence 2: Key rotation log
    key_rotation_log = get_key_rotation_events(days=365)
    evidence["evidence_items"].append({
        "type": "audit_log",
        "description": "Key rotation events (last 12 months)",
        "count": len(key_rotation_log),
        "data": key_rotation_log[:5]  # Sample
    })

    # Evidence 3: Test results
    test_results = run_encryption_tests()
    evidence["evidence_items"].append({
        "type": "test_results",
        "description": "Encryption functionality tests",
        "passed": test_results["passed"],
        "failed": test_results["failed"],
        "date": test_results["date"]
    })

    # Save evidence package
    with open(f'soc2_evidence_{datetime.utcnow().date()}.json', 'w') as f:
        json.dump(evidence, f, indent=2)

    return evidence

# Run evidence collection
evidence = collect_soc2_evidence()
assert len(evidence["evidence_items"]) >= 3, "Insufficient evidence collected"
```

### 6. Compliance Mapping Validation
```python
# Verify traceability: requirement → implementation → test
compliance_mapping = {
    "FIPS_140_2": {
        "requirement": "Use FIPS-validated cryptographic module",
        "implementation": "cryptography library (FIPS mode)",
        "validation_certificate": "Certificate #1234",
        "test": "test_fips_mode_enforcement",
        "status": "COMPLIANT"
    },
    "PCI_DSS_3_5_1": {
        "requirement": "Encrypt cardholder data with AES-256",
        "implementation": "AES-256-GCM via cryptography library",
        "code_location": "/src/encryption/card_data.py:45",
        "test": "test_card_data_encryption",
        "status": "COMPLIANT"
    },
    "SOC2_CC6_7": {
        "requirement": "Encrypt sensitive data at rest",
        "implementation": "Database field-level encryption",
        "code_location": "/src/models/encrypted_fields.py",
        "test": "test_field_level_encryption",
        "status": "COMPLIANT"
    },
    "GDPR_Article_32": {
        "requirement": "State-of-the-art encryption",
        "implementation": "AES-256-GCM, RSA-2048, SHA-256",
        "justification": "NIST/ENISA recommended algorithms (2024)",
        "test": "test_state_of_art_algorithms",
        "status": "COMPLIANT"
    }
}

# Verify all requirements have implementation and tests
for req_id, req_data in compliance_mapping.items():
    assert "implementation" in req_data, f"{req_id}: Missing implementation"
    assert "test" in req_data, f"{req_id}: Missing test"
    assert "status" in req_data, f"{req_id}: Missing status"
    assert req_data["status"] == "COMPLIANT", f"{req_id}: Not compliant"
```

## Success Criteria

### Functional Success
- FIPS mode enforces only approved algorithms (tested)
- All key operations logged with complete audit trail
- PCI-DSS key strength validated programmatically
- GDPR state-of-the-art algorithms documented and justified

### Audit Success
- SOC2 Type II report: zero exceptions in cryptographic controls
- PCI-DSS ROC: compliant rating (no findings)
- GDPR DPA audit: no deficiencies in Article 32 compliance
- Penetration test: no cryptographic vulnerabilities found

### Documentation Success
- Compliance mapping document complete (requirement → code → test)
- FIPS validation certificate documented with active status
- PCI-DSS key management policy approved by QSA
- SOC2 evidence package generated automatically

### Operational Success
- Annual cryptographic review completed in <40 hours
- Audit evidence collection automated (<1 hour manual work)
- Compliance queries answered within 48 hours
- Zero compliance violations or regulatory fines

## Library Evaluation Criteria

### Primary Criteria (Deal-Breakers)
1. FIPS 140-2 validation certificate (NIST CMVP validated)
2. Support for FIPS mode enforcement
3. PCI-DSS approved algorithms (AES-256, RSA-2048+, SHA-256+)
4. Documentation suitable for auditors (detailed, technical)
5. Active maintenance (security updates within 30 days of CVE)

### Secondary Criteria (Scoring)
- FIPS 140-3 validation: +10 points
- Higher FIPS validation level (2, 3): +5 points per level
- Explicit PCI-DSS documentation: +5 points
- SOC2 audit guidance provided: +3 points
- Compliance example code: +3 points

### Negative Criteria (Penalties)
- No FIPS validation: -100 points (deal-breaker for government)
- Deprecated algorithms included: -10 points
- Security advisory response time >30 days: -5 points
- No compliance documentation: -5 points
- Pure Python (unvalidated) implementations: -10 points

## Expected Library Fit

Based on requirements, ideal library must provide:
- FIPS 140-2 validated cryptographic module (OpenSSL FIPS module)
- FIPS mode toggle and enforcement
- Complete documentation of validation certificate
- Audit-friendly documentation and examples
- Active security maintenance and CVE response

**Hypothesis**: `cryptography` library with OpenSSL FIPS module is likely the only option for FIPS 140-2 compliance. Need to verify validation certificate status and FIPS mode functionality.

**Alternative**: If FIPS not required, `pycryptodome` may be sufficient for PCI-DSS/SOC2/GDPR (approved algorithms without formal validation).

## Compliance Risk Assessment

### High Risk (Deal-Breakers)
- Library without FIPS validation used for government contract: **CONTRACT TERMINATION**
- Weak key strength in PCI environment: **PCI-DSS FAILURE, FINES**
- Non-state-of-the-art algorithms in GDPR context: **DPA ENFORCEMENT ACTION**

### Medium Risk (Audit Findings)
- Incomplete audit trails: **SOC2 EXCEPTION**
- Missing documentation: **AUDITOR DELAYS, ADDITIONAL COSTS**
- Deprecated algorithm usage: **REMEDIATION REQUIRED**

### Low Risk (Manageable)
- Performance issues with FIPS mode: **MITIGATABLE WITH HARDWARE**
- Complex audit evidence collection: **AUTOMATE WITH SCRIPTS**
- Library version updates: **STANDARD MAINTENANCE**

**Conclusion**: Compliance requirements are strict and non-negotiable. Library selection must prioritize compliance over convenience, performance, or features.
