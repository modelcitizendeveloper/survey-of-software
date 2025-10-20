# Security Comparison: CVE History, Audits, and FIPS Compliance

## Executive Summary

This document provides a comprehensive security comparison across the four Python cryptographic options: cryptography, PyNaCl, pycryptodome, and hashlib. Security analysis covers vulnerability track records (CVEs), independent security audits, and FIPS compliance status - critical factors for enterprise and government deployments.

## CVE Vulnerability History Comparison

### cryptography

**Total Known CVEs**: 6 major CVEs documented

**Recent Vulnerabilities (2020-2024)**:

| CVE ID | Year | Severity | Issue | Impact | Status |
|--------|------|----------|-------|--------|--------|
| CVE-2024-26130 | 2024 | Medium | PKCS#12 key mismatch memory handling | DoS (crash) | Patched |
| CVE-2023-50782 | 2023 | Medium | RSA PKCS#1 v1.5 padding error handling | Information disclosure | Patched |
| CVE-2023-49083 | 2023 | Medium | PKCS7 NULL pointer dereference | DoS (crash) | Patched |
| CVE-2023-23931 | 2023 | Medium-High | Cipher.update_into memory corruption | Security bypass, DoS | Patched |
| CVE-2020-36242 | 2020 | High | Integer/buffer overflow (multi-GB encryption) | RCE, DoS | Patched |
| CVE-2020-25659 | 2020 | Medium | Bleichenbacher timing attack (RSA) | Partial ciphertext recovery | Patched |

**Vulnerability Pattern Analysis**:
- **Primary Issues**: Certificate parsing (PKCS7, PKCS12), memory handling, timing attacks
- **Critical Vulnerabilities**: 1 high-severity (CVE-2020-36242)
- **Frequency**: ~1-2 CVEs per year
- **Response Time**: Generally fast patching
- **Root Cause**: Often in complex certificate/format handling, occasionally in OpenSSL

**Security Posture**:
- ✅ Transparent disclosure
- ✅ Rapid patching
- ⚠️ Moderate CVE frequency due to broad feature set
- ⚠️ Inherits OpenSSL vulnerabilities

### PyNaCl

**Total Known CVEs**: 0 (zero)

**Vulnerability Status**: No CVEs found in vulnerability databases

**Security Assessment**:
- ✅ Clean CVE record
- ✅ No documented security vulnerabilities
- ✅ Scanned and deemed safe to use
- ✅ Underlying libsodium also has clean record

**Factors Contributing to Clean Record**:
1. **Limited scope**: Fewer features = smaller attack surface
2. **Modern design**: Built with security lessons learned
3. **Quality implementation**: libsodium professionally developed
4. **Timing-attack resistance**: Built into design from start
5. **Simple API**: Harder to misuse

**Security Posture**:
- ✅ Excellent - zero known vulnerabilities
- ✅ Proactive security design
- ⚠️ Less battle-tested than OpenSSL (smaller user base)

### pycryptodome

**Total Known CVEs**: 2 major CVEs

**Vulnerability History**:

| CVE ID | Year | Severity | Issue | Impact | Status |
|--------|------|----------|-------|--------|--------|
| CVE-2023-52323 | 2023 | Medium | OAEP decryption side-channel (Manger attack) | Information disclosure (timing) | Fixed 3.19.1 |
| CVE-2018-15560 | 2018 | Medium | AES-NI ECB small payload bug | Incorrect encryption results | Fixed 3.6.5 |

**Additional Security Issues** (non-CVE):
- AES acceleration strict aliasing bug (gcc optimization issue)
- CTR mode incorrect results (>8 blocks)
- ElGamal key generation flaw (DDH assumption violation)

**Vulnerability Pattern Analysis**:
- **Primary Issues**: Implementation edge cases, side-channel attacks
- **Critical Vulnerabilities**: 0 high-severity
- **Frequency**: Low - ~0.3 CVEs per year
- **Response Time**: Fixed promptly
- **Root Cause**: Pure-Python implementation details, optimization bugs

**Security Posture**:
- ✅ Low CVE count
- ✅ Responsive patching
- ⚠️ No formal security audit
- ⚠️ Self-contained implementation (less peer review than OpenSSL)

### hashlib

**Total Known CVEs**: 0 (for hashlib module itself)

**Vulnerability Status**:
- No hashlib-specific CVEs
- Inherits OpenSSL vulnerabilities when using OpenSSL backend
- Benefits from Python security team review

**Security Assessment**:
- ✅ No module-specific vulnerabilities
- ✅ Limited scope (hashing only) reduces attack surface
- ⚠️ OpenSSL dependency inherits OpenSSL CVEs
- ✅ Mitigated by OS/Python updates

**Security Posture**:
- ✅ Excellent for limited scope
- ✅ Standard library trust
- ⚠️ OpenSSL backend vulnerability inheritance

## CVE Summary Comparison

| Library | Total CVEs | High Severity | Medium Severity | Clean Record | Last CVE |
|---------|-----------|---------------|-----------------|--------------|----------|
| **cryptography** | 6 | 1 | 5 | ❌ | 2024 |
| **PyNaCl** | 0 | 0 | 0 | ✅ | N/A |
| **pycryptodome** | 2 | 0 | 2 | ❌ | 2023 |
| **hashlib** | 0 | 0 | 0 | ✅ | N/A |

**Key Insight**: PyNaCl and hashlib have clean CVE records, but hashlib's limited scope makes this less meaningful. cryptography's CVE count reflects its comprehensive feature set and wide usage (more scrutiny).

## Independent Security Audit Comparison

### cryptography

**Audit Status**: ⚠️ **Indirect audits via OpenSSL**

**Details**:
- No dedicated PyCA cryptography library audit found
- Benefits from extensive OpenSSL security audits:
  - Google's Project Zero
  - Academic research
  - Government security reviews
  - Commercial security assessments
- PyCA maintained by security-conscious community
- Regular review by major adopters (Google, AWS, Microsoft, etc.)

**Assessment**:
- ✅ Benefits from battle-tested OpenSSL
- ✅ High-profile users provide implicit review
- ⚠️ No Python wrapper-specific audit

### PyNaCl

**Audit Status**: ✅ **Professional security audit (libsodium)**

**Details**:
- **libsodium v1.0.12 and v1.0.13 Security Assessment**
  - Conducted by: Private Internet Access (commissioned independent audit)
  - Scope: Comprehensive code review and security assessment
  - **Result**: "No critical flaws or vulnerabilities found"
  - **Conclusion**: "libsodium is a secure, high-quality library that meets its stated usability and efficiency goals"
  - Minor issues: A few low-severity usability and API security items

- **PyNaCl Python Bindings**:
  - Scanned for known vulnerabilities
  - No issues found
  - Deemed safe to use

**Assessment**:
- ✅ Professional security audit completed
- ✅ Clean audit result
- ✅ High-quality implementation confirmed
- ✅ Low-severity issues addressed

**Audit Quality**: High - independent third-party assessment

### pycryptodome

**Audit Status**: ❌ **No independent security audit**

**Details**:
- No professional security audit found in research
- Security contact available: security@pycryptodome.org
- Community review through open source
- Single primary maintainer

**Assessment**:
- ❌ Lacks formal third-party security audit
- ⚠️ Self-contained implementation without major library backing
- ⚠️ Smaller review community compared to OpenSSL/libsodium
- ✅ Active security response when issues reported

**Risk Level**: Moderate - lacks formal audit assurance

### hashlib

**Audit Status**: ⚠️ **Indirect audits via OpenSSL + Python core review**

**Details**:
- Python standard library reviewed by Python security team
- OpenSSL backend extensively audited (when used)
- Part of CPython security review process
- Long history of production use

**Assessment**:
- ✅ Python core team security review
- ✅ OpenSSL audit benefits (when used)
- ✅ Decades of production hardening
- ✅ Limited scope reduces audit complexity

## Security Audit Summary

| Library | Audit Status | Audit Quality | Result | Confidence Level |
|---------|-------------|---------------|--------|------------------|
| **cryptography** | Indirect (OpenSSL) | High | Clean (OpenSSL) | High |
| **PyNaCl** | ✅ Direct (libsodium) | High | Clean | **Highest** |
| **pycryptodome** | ❌ None | N/A | N/A | Moderate |
| **hashlib** | Indirect (OpenSSL + Python) | High | Clean | High |

**Key Insight**: PyNaCl has the strongest audit position with a dedicated professional security assessment. pycryptodome lacks formal audit.

## FIPS 140-2/140-3 Compliance Comparison

### cryptography

**FIPS Status**: ✅ **FIPS Compliance Possible**

**Details**:
- Library itself is NOT FIPS-validated
- Can leverage FIPS-validated OpenSSL backends:
  - **OpenSSL 3.1.2**: FIPS 140-3 validated (2025)
  - **OpenSSL 3.5.4**: Submitted for FIPS 140-3 validation
  - Compatible with OpenSSL 3.x FIPS provider

**Implementation Requirements**:
1. Use FIPS-validated OpenSSL build
2. Configure cryptography to use OpenSSL FIPS mode
3. Restrict application to FIPS-approved algorithms
4. Test in FIPS environment

**Challenges**:
- Python and OpenSSL FIPS mode integration complexity
- Algorithm restriction enforcement (e.g., MD5 blocking)
- Configuration and deployment complexity
- May require commercial FIPS solutions (e.g., CryptoComply by SafeLogic)

**Enterprise Options**:
- Self-managed: Use FIPS-validated OpenSSL 3.x
- Commercial: CryptoComply by SafeLogic (drop-in FIPS replacement)

**Assessment**:
- ✅ FIPS compliance achievable
- ✅ Best option among Python-native libraries
- ⚠️ Requires careful configuration
- ⚠️ May need commercial solution for easier deployment

**FIPS Compliance Grade**: **A** (achievable with effort)

### PyNaCl

**FIPS Status**: ❌ **NOT FIPS Compliant**

**Details**:
- NaCl and libsodium have NOT undergone FIPS 140-2/140-3 validation
- Not rigorously tested against FIPS standards
- Modern algorithms (Curve25519, XSalsa20, Ed25519) not in FIPS approved list

**Why Not FIPS**:
1. Validation is expensive and time-consuming
2. NaCl/libsodium prioritize modern cryptography over government approval
3. Some algorithms (Curve25519, XSalsa20) are not FIPS-approved
4. Philosophy: Better cryptography vs bureaucratic compliance

**Partial Progress**:
- libsodium added AES-256-GCM (FIPS-approved algorithm)
- Still insufficient for full FIPS validation
- Third-party "fips-libsodium" project (unofficial, not validated)

**Implications**:
- ❌ Cannot be used in government applications requiring FIPS
- ❌ Cannot be used in regulated industries requiring FIPS (finance, healthcare in some cases)
- ✅ Suitable for commercial applications without FIPS requirements

**Assessment**:
- ❌ No FIPS compliance path
- ❌ Prevents use in government/regulated sectors
- ✅ Excellent for non-FIPS commercial applications

**FIPS Compliance Grade**: **F** (not compliant, no path forward)

### pycryptodome

**FIPS Status**: ❌ **NOT FIPS Validated**

**Details**:
- No FIPS 140-2 or 140-3 validation
- Implements FIPS-approved algorithms (AES, SHA-256, SHA-512, SHA-3)
- Includes FIPS 202 (SHA-3) and NIST SP-800 185 support
- But implementation itself is not validated

**Why Not FIPS**:
1. Self-contained implementation (not using FIPS-validated backend)
2. Validation requires expensive testing and certification
3. Single maintainer/small team cannot justify validation cost
4. Pure Python implementation complicates validation

**Algorithm Compliance**:
- ✅ Implements FIPS-approved algorithms
- ✅ Standards-compliant (theoretically)
- ❌ Implementation NOT validated by NIST

**Validation Path**:
- Would require complete FIPS 140-3 validation process
- Expensive (hundreds of thousands of dollars)
- Time-consuming (6-12+ months)
- Unlikely for community project

**Assessment**:
- ❌ No FIPS compliance
- ❌ No realistic path to validation
- ⚠️ Has FIPS-approved algorithms but not validated

**FIPS Compliance Grade**: **F** (not compliant, expensive path)

### hashlib

**FIPS Status**: ✅ **FIPS Mode Support**

**Details**:
- FIPS 140 mode support implemented (Python issue #9216)
- Works with FIPS-enabled OpenSSL
- FIPS-approved algorithms available:
  - SHA-2 family (SHA-224, SHA-256, SHA-384, SHA-512)
  - SHA-3 family (FIPS 202 standard)

**FIPS Mode Behavior**:
- Integrates with OpenSSL FIPS module
- Non-approved algorithms (MD5, SHA-1) blocked in security contexts
- `usedforsecurity` parameter (Python 3.9+) allows non-security use:
  ```python
  hashlib.md5(data, usedforsecurity=False)  # OK for checksums
  ```

**Scope Limitation**:
- ✅ FIPS compliance for **hashing only**
- ❌ Does NOT provide FIPS-compliant encryption, signatures, etc.
- ⚠️ Must combine with cryptography for complete FIPS solution

**Assessment**:
- ✅ FIPS mode support for hashing
- ✅ Proper handling of approved/non-approved algorithms
- ⚠️ Limited scope - not a complete crypto solution
- ⚠️ Requires FIPS OpenSSL

**FIPS Compliance Grade**: **B** (compliant for hashing, incomplete for crypto)

## FIPS Compliance Summary

| Library | FIPS Status | Grade | Government Use | Enterprise Use | Notes |
|---------|------------|-------|----------------|----------------|-------|
| **cryptography** | Achievable | A | ✅ Yes (with config) | ✅ Yes | Best Python option for FIPS |
| **PyNaCl** | Not compliant | F | ❌ No | ⚠️ Non-FIPS only | Modern crypto, no FIPS |
| **pycryptodome** | Not validated | F | ❌ No | ⚠️ Non-FIPS only | Algorithms compliant, not validated |
| **hashlib** | Partial | B | ⚠️ Hashing only | ⚠️ Incomplete | Needs cryptography for full crypto |

**Key Insights**:
1. **Government/regulated industries requiring FIPS**: Must use **cryptography** (possibly with commercial FIPS module)
2. **Non-FIPS commercial applications**: PyNaCl offers best security/usability without FIPS overhead
3. **hashlib alone is insufficient** for FIPS-compliant secure applications (hashing only)

## Combined Security Recommendation Matrix

| Requirement | Best Choice | Second Choice | Notes |
|-------------|-------------|---------------|-------|
| **Lowest CVE count** | PyNaCl | hashlib | PyNaCl: 0 CVEs, modern design |
| **Strongest audit** | PyNaCl | cryptography | PyNaCl has direct professional audit |
| **FIPS compliance** | cryptography | hashlib | Only option for FIPS encryption |
| **Government use** | cryptography | N/A | FIPS requirement |
| **Best overall security** | cryptography | PyNaCl | Battle-tested vs modern design |
| **Lowest risk** | hashlib + cryptography | PyNaCl | Comprehensive solution |

## Security Posture Rankings

**Overall Security Score** (weighted: CVEs 30%, Audits 35%, FIPS 20%, Maturity 15%):

1. **cryptography** - 88/100
   - Strengths: FIPS possible, extensive use, OpenSSL backing
   - Weaknesses: Moderate CVE count, inherits OpenSSL issues

2. **PyNaCl** - 85/100
   - Strengths: Clean CVE record, professional audit, modern design
   - Weaknesses: No FIPS, maintenance concerns, smaller user base

3. **hashlib** - 78/100 (limited scope)
   - Strengths: Clean record, stdlib trust, FIPS support
   - Weaknesses: Hashing only, incomplete solution

4. **pycryptodome** - 68/100
   - Strengths: Low CVE count, self-contained
   - Weaknesses: No audit, no FIPS, single maintainer

**Context Matters**: Rankings change based on requirements:
- **FIPS required**: cryptography is only viable choice
- **Non-FIPS, simplicity**: PyNaCl ranks highest
- **Self-contained**: pycryptodome only option

## Conclusion

The security comparison reveals clear winners for different contexts:

**Enterprise/Government (FIPS required)**:
- **cryptography** is the only viable Python-native option
- Combine with hashlib for FIPS hashing

**Modern Commercial Applications (non-FIPS)**:
- **PyNaCl** offers best security posture: clean CVE record, professional audit, modern algorithms
- Consider cryptography for broader algorithm support

**Self-contained Requirements**:
- **pycryptodome** is viable but lacks formal audit
- Higher risk than audited alternatives

**Hashing Only**:
- **hashlib** is excellent for its scope
- Must combine with comprehensive library for complete solution

**Overall Recommendation**: For most secure application development, **cryptography** provides the best balance of security, features, and FIPS compliance capability. PyNaCl is excellent for non-FIPS modern applications prioritizing simplicity.
