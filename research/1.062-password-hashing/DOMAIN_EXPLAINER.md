# Password Hashing Domain Explainer

**Purpose**: Technical concepts and terminology glossary for business stakeholders (CTOs, PMs, executives) to understand password hashing in Python applications.

**Target Audience**: Non-cryptography experts who need to make informed decisions about authentication security.

---

## 1. Core Technical Concepts

### 1.1 Password Hashing vs Encryption

**Password hashing** is a one-way transformation that creates a fixed-size "fingerprint" of a password. Unlike encryption, hashing is **intentionally irreversible**.

**Why one-way?**
- If an attacker steals your database, they get hashes, not passwords
- Even system administrators cannot see user passwords
- Users' passwords on other sites remain protected (people reuse passwords)

**Critical distinction**:
- **Encryption**: Reversible with a key (use for data you need to read later)
- **Hashing**: Irreversible (use for passwords)

**Never encrypt passwords.** If someone steals the encryption key, all passwords are exposed instantly. With hashing, attackers must brute-force each password individually.

### 1.2 Why Password Hashing is Intentionally Slow

Regular hash functions (SHA-256, MD5) are designed to be **fast**. Password hashing algorithms are designed to be **slow**.

**The math**:
- SHA-256: ~10,000,000 hashes/second on commodity hardware
- Argon2: ~5 hashes/second (with proper settings)

**Why this matters**:
- If an attacker steals 1 million password hashes...
- With SHA-256: Test all common passwords in seconds
- With Argon2: Testing takes weeks to months

**The goal**: Make brute-force attacks economically infeasible.

### 1.3 Memory-Hard Algorithms

**Memory-hardness** means the algorithm requires large amounts of RAM to compute.

**Why it matters**:
- GPUs can run thousands of simple operations in parallel
- But GPUs have limited memory per core
- Memory-hard algorithms force sequential memory access
- This limits how many passwords can be tested simultaneously

**Memory-hard algorithms**: Argon2, scrypt
**NOT memory-hard**: bcrypt, PBKDF2

**Real-world impact**:
- bcrypt: Attackers can use GPU clusters effectively
- Argon2 (128 MiB): Each GPU core needs 128 MB RAM, severely limiting parallelism

### 1.4 Salting

A **salt** is random data added to each password before hashing.

**Without salt** (DANGEROUS):
```
hash("password123") → "ef92b778..."  # Same for all users
```
If two users have the same password, they have the same hash. Attackers can build "rainbow tables" of pre-computed hashes.

**With salt** (CORRECT):
```
hash("password123" + "randomsalt1") → "a1b2c3d4..."
hash("password123" + "randomsalt2") → "x9y8z7w6..."  # Different!
```
Same password, different hashes. Rainbow tables become useless.

**Best practice**: All modern password hashing libraries generate unique salts automatically.

### 1.5 Work Factor / Cost Parameter

The **work factor** (also called "cost" or "rounds") controls how slow the hashing algorithm runs.

**bcrypt example**:
- cost=10: ~75ms per hash
- cost=12: ~300ms per hash
- cost=14: ~1.2s per hash

**Why adjustable?**
- Hardware gets faster every year
- You want hashing to take 250-500ms
- Increase work factor as CPUs improve

**OWASP recommendation**: Tune to 250-500ms on your production hardware.

### 1.6 Argon2 Variants

Argon2 has three variants designed for different threat models:

| Variant | Design Goal | Best For |
|---------|-------------|----------|
| **Argon2d** | Maximum GPU resistance | Cryptocurrency, server-side |
| **Argon2i** | Side-channel resistance | Cloud/shared environments |
| **Argon2id** | Hybrid (best of both) | Password hashing (recommended) |

**Argon2id** is the recommended variant for password hashing because it provides balanced protection against both GPU attacks (like Argon2d) and timing attacks (like Argon2i).

---

## 2. Security Concepts

### 2.1 Brute Force Attacks

**Brute force**: Trying every possible password until finding a match.

**Attack cost factors**:
- Number of passwords to try
- Time per hash attempt
- Hardware cost (GPUs, ASICs)
- Electricity cost

**Defense**: Make each hash attempt expensive (time + memory).

### 2.2 Dictionary Attacks

**Dictionary attack**: Trying common passwords and variations.

**Facts**:
- "123456" is still the most common password
- Top 1000 passwords cover ~10% of accounts
- Attackers have lists of billions of leaked passwords

**Defense**: Password hashing makes each guess expensive. Also: enforce password complexity requirements.

### 2.3 Rainbow Tables

**Rainbow table**: Pre-computed database of hash → password mappings.

**Attack**: Look up stolen hash in table, instantly get password.

**Defense**: Salting. Each password has unique salt, so pre-computed tables are useless.

**Note**: All modern password hashing libraries handle salting automatically.

### 2.4 Side-Channel Attacks

**Side-channel**: Extracting information from physical implementation, not the algorithm itself.

**Examples**:
- **Timing attacks**: Measuring how long operations take
- **Power analysis**: Measuring electrical consumption
- **Cache attacks**: Observing memory access patterns

**Relevance**: Mostly affects cloud/shared hosting where attackers can observe your server.

**Defense**: Argon2id (hybrid variant) is designed to resist side-channel attacks.

### 2.5 Credential Stuffing

**Credential stuffing**: Using leaked username/password pairs from one site to attack another.

**Why it works**: 65% of people reuse passwords across sites.

**Why password hashing matters**: Even if your database is breached, properly hashed passwords can't be used to attack other sites.

---

## 3. Algorithm Landscape

### 3.1 OWASP Recommendations (2025)

The Open Web Application Security Project (OWASP) maintains authoritative security guidance.

**Current priority order**:

1. **Argon2id** (PRIMARY) - Memory-hard, PHC winner
2. **scrypt** (SECONDARY) - Memory-hard, if Argon2 unavailable
3. **bcrypt** (LEGACY) - For existing systems only
4. **PBKDF2** (FIPS) - Only if FIPS-140 compliance required

### 3.2 Algorithm Comparison

| Algorithm | Memory-Hard | GPU Resistant | Age | Status |
|-----------|-------------|---------------|-----|--------|
| Argon2id | YES | HIGH | 2015 | RECOMMENDED |
| scrypt | YES | MEDIUM | 2009 | ACCEPTABLE |
| bcrypt | NO | LOW | 1999 | LEGACY |
| PBKDF2 | NO | VERY LOW | 2000 | FIPS ONLY |

### 3.3 Why Argon2 Won

The **Password Hashing Competition** (2013-2015) evaluated algorithms on:
- Security against known attacks
- Memory-hardness
- Resistance to side-channels
- Performance characteristics
- Simplicity and implementability

**Argon2 won** because it provided the best balance across all criteria.

### 3.4 FIPS-140 Compliance

**FIPS-140** is a US government security standard for cryptographic modules.

**Who needs it?**
- US federal agencies
- Federal contractors
- Healthcare (HIPAA) with government data
- Financial services with government work

**The catch**: Only **PBKDF2** is FIPS-approved for password hashing. Argon2 is not (yet).

**If you need FIPS**: Use PBKDF2 with at least 600,000 iterations.

---

## 4. Library Ecosystem

### 4.1 Python Library Landscape

| Library | Algorithm | Status | Recommendation |
|---------|-----------|--------|----------------|
| argon2-cffi | Argon2 | Active | NEW PROJECTS |
| bcrypt (PyCA) | bcrypt | Active | EXISTING SYSTEMS |
| passlib | Multiple | ABANDONED | AVOID |
| hashlib | scrypt, PBKDF2 | Stdlib | FALLBACK/FIPS |

### 4.2 Why passlib Should Be Avoided

passlib was once the standard choice. It's now abandoned:
- Last release: October 2020 (4+ years ago)
- No Python 3.13 support
- Known compatibility issues
- FastAPI and Ansible have migrated away

**If you have passlib**: Migrate to argon2-cffi or libpass (maintained fork).

### 4.3 PyCA (Python Cryptographic Authority)

PyCA is a trusted organization maintaining critical Python security libraries:
- cryptography
- bcrypt
- PyNaCl
- pyOpenSSL

**Why it matters**: Organization-backed libraries have better long-term sustainability than individual-maintained projects.

---

## 5. Business Considerations

### 5.1 Breach Cost Impact

Average data breach cost (2024): **$4.4 million**

**Password hashing impact on breach severity**:
- **Weak/no hashing**: Immediate password exposure
- **Strong hashing**: Attackers get hashes, not passwords
- **Difference**: Weeks to months of protection for users to change passwords

### 5.2 Compliance Requirements

| Standard | Password Hashing Requirement |
|----------|------------------------------|
| SOC2 | Strong cryptographic hashing |
| HIPAA | Encryption/hashing of credentials |
| PCI-DSS | Strong one-way hash functions |
| GDPR | Appropriate technical measures |
| FIPS-140 | FIPS-approved algorithms (PBKDF2) |

### 5.3 Performance vs Security Trade-off

**The tension**:
- Slower hashing = better security
- Slower hashing = worse user experience
- Slower hashing = higher server load

**Sweet spot**: 250-500ms per hash
- Secure enough for most applications
- Fast enough for good user experience
- Manageable server load

**High-security applications**: Accept 500ms+ latency.

### 5.4 DoS Risk

Password hashing is CPU/memory intensive. Attackers can abuse this.

**Attack**: Send many login requests to exhaust server resources.

**Defense**:
- Rate limiting on authentication endpoints
- CAPTCHA after failed attempts
- Account lockout policies
- Queue-based authentication processing

---

## 6. Common Misconceptions

### 6.1 "More downloads = better"

bcrypt has 3x more PyPI downloads than argon2-cffi.

**Reality**: This reflects legacy adoption, not current best practice. OWASP explicitly recommends Argon2 over bcrypt for new projects.

### 6.2 "bcrypt is insecure"

**Reality**: bcrypt is still secure and acceptable. It's just not optimal:
- Not memory-hard (GPU-vulnerable)
- 72-byte password limit
- Newer algorithms are better

**Recommendation**: No urgent need to migrate existing bcrypt systems, but use Argon2 for new projects.

### 6.3 "Password hashing is encryption"

**Reality**: They're fundamentally different:
- Encryption is reversible (with key)
- Hashing is one-way (irreversible)

Never encrypt passwords. Always hash them.

### 6.4 "SHA-256 is secure for passwords"

**Reality**: SHA-256 is a secure hash function, but it's too fast for password hashing. Attackers can try billions of passwords per second.

Password hashing algorithms (Argon2, bcrypt) are intentionally slow to resist brute-force attacks.

### 6.5 "Longer passwords don't matter with hashing"

**Reality**: Longer passwords dramatically increase brute-force time:
- 8-character: Hours to days
- 12-character: Months to years
- 16-character: Effectively impossible

Encourage users to use longer passwords/passphrases.

---

## 7. Key Takeaways

### For Engineering Decisions

1. **New projects**: Use argon2-cffi with default settings
2. **Existing bcrypt**: Keep it, no urgent migration needed
3. **FIPS required**: Use PBKDF2 with 600,000+ iterations
4. **Using passlib**: Migrate to argon2-cffi or libpass

### For Security Policy

1. **Algorithm**: Argon2id (or bcrypt for legacy)
2. **Target latency**: 250-500ms per hash
3. **Password requirements**: 12+ characters minimum
4. **Rate limiting**: Required on all auth endpoints
5. **Monitoring**: Log and alert on authentication failures

### For Compliance

1. **SOC2/HIPAA/PCI-DSS**: Argon2 or bcrypt acceptable
2. **FIPS-140**: PBKDF2 only (for now)
3. **Document choices**: Maintain security decision records

---

## Glossary

**ASIC**: Application-Specific Integrated Circuit - Custom hardware for specific computations (like password cracking)

**Brute force**: Systematically trying all possible passwords

**Cost parameter**: Setting that controls how slow password hashing runs

**GPU**: Graphics Processing Unit - Can run many password hash attempts in parallel

**Hash**: Fixed-size output from a hash function, regardless of input size

**Memory-hard**: Algorithm requiring large amounts of RAM, limiting parallel attacks

**OWASP**: Open Web Application Security Project - Security standards organization

**Password Hashing Competition (PHC)**: 2013-2015 competition that selected Argon2

**PBKDF2**: Password-Based Key Derivation Function 2 - Older, FIPS-approved algorithm

**PyCA**: Python Cryptographic Authority - Organization maintaining Python crypto libraries

**Rainbow table**: Pre-computed database of hash-to-password mappings

**Salt**: Random data added to password before hashing to ensure unique outputs

**Side-channel attack**: Extracting secrets from physical implementation (timing, power, etc.)

**Work factor**: Same as cost parameter - controls hash computation time

---

**Document Version**: 1.0
**Last Updated**: 2025-12-11
**Target Audience**: CTOs, Product Managers, Security Officers
**Prerequisites**: None (designed for non-cryptography experts)
