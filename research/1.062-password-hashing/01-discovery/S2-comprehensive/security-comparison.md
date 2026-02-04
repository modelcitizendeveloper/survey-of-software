# Security Comparison: Password Hashing Libraries

## Algorithm Security Properties

### Memory Hardness

Memory-hard algorithms resist GPU/ASIC attacks by requiring large amounts of memory.

| Algorithm | Memory Hard | GPU Resistant | ASIC Resistant |
|-----------|-------------|---------------|----------------|
| Argon2id | YES | HIGH | HIGH |
| scrypt | YES | MEDIUM | MEDIUM |
| bcrypt | NO | LOW | LOW |
| PBKDF2 | NO | VERY LOW | VERY LOW |

**Why it matters**: GPUs can run thousands of bcrypt/PBKDF2 instances in parallel. Memory-hard algorithms force sequential memory access, limiting parallelism.

### Side-Channel Resistance

| Algorithm | Data-Dependent | Side-Channel Risk |
|-----------|----------------|-------------------|
| Argon2d | YES | HIGH (timing attacks) |
| Argon2i | NO | LOW |
| Argon2id | HYBRID | LOW (first pass data-independent) |
| bcrypt | YES | MEDIUM |
| scrypt | YES | MEDIUM |

**Recommendation**: Argon2id balances GPU resistance (Argon2d) with side-channel resistance (Argon2i).

## CVE History

### argon2-cffi

| CVEs | Critical | High | Medium | Low |
|------|----------|------|--------|-----|
| 0 | 0 | 0 | 0 | 0 |

**Assessment**: Clean security record since 2015.

### bcrypt (pyca/bcrypt)

| CVEs | Critical | High | Medium | Low |
|------|----------|------|--------|-----|
| 1 (historical) | 0 | 0 | 0 | 1 |

- CVE-2013-1895: Affected py-bcrypt <0.3 (fixed)
- v5.0.0: Fixed silent password truncation (security improvement)

**Assessment**: Excellent security record for current versions.

### passlib

| CVEs | Critical | High | Medium | Low |
|------|----------|------|--------|-----|
| 0 (formal) | 0 | 0 | 0 | 0 |

**Known Issues (no CVE assigned):**
- EUVDB #VU28246: bcrypt_sha256 unsalted prehash (medium risk)
- SNYK-PYTHON-PASSLIB-40761: DoS via wildcard passwords
- bcrypt 4.x incompatibility

**Assessment**: No formal CVEs but has unpatched security issues due to abandonment.

### hashlib.scrypt

| CVEs | Critical | High | Medium | Low |
|------|----------|------|--------|-----|
| N/A | N/A | N/A | N/A | N/A |

**Assessment**: Part of Python stdlib, inherits OpenSSL's security posture.

## Attack Resistance Analysis

### Brute Force Cost (2025 estimates)

Based on Red Hat Research analysis for 8-character passwords:

| Configuration | Attack Cost (10 years) |
|---------------|------------------------|
| Argon2 (2048 MiB, 3 iter) | Hundreds of millions USD |
| Argon2 (OWASP 46 MiB) | Millions USD |
| bcrypt (cost=12) | Thousands USD |
| PBKDF2 (600K iter) | Hundreds USD |

**Source**: Red Hat Research, "How expensive is it to crack Argon2?"

### Compromise Rate Reduction

| Configuration | Reduction vs SHA-256 |
|---------------|---------------------|
| Argon2 (2048 MiB) | 46.99% |
| Argon2 (46 MiB OWASP) | 42.5% |
| bcrypt (cost=12) | ~30% |
| PBKDF2 (100K iter) | ~15% |

## Security Scoring

| Library | Algorithm | CVEs | Maintenance | Score |
|---------|-----------|------|-------------|-------|
| argon2-cffi | 10/10 | 10/10 | 9/10 | **9.7/10** |
| bcrypt | 7/10 | 9/10 | 10/10 | **8.7/10** |
| hashlib.scrypt | 8/10 | 10/10 | 10/10 | **9.3/10** |
| passlib | 10/10 | 7/10 | 2/10 | **6.3/10** |

## Recommendations by Security Requirement

| Requirement | Recommended |
|-------------|-------------|
| Maximum security | argon2-cffi (Argon2id, high memory) |
| FIPS-140 compliance | hashlib + PBKDF2-HMAC-SHA256 |
| Side-channel resistance | argon2-cffi (Argon2id) |
| GPU attack resistance | argon2-cffi > scrypt > bcrypt |
| Zero CVE tolerance | argon2-cffi |
