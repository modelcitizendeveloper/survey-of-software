# Algorithm Trajectory Analysis

## Standards Body Adoption

### Argon2

| Body | Status | Document |
|------|--------|----------|
| IETF | RFC 9106 (2021) | Argon2 Memory-Hard Function |
| OWASP | Primary recommendation | Password Storage Cheat Sheet |
| NIST | Under consideration | SP 800-132 revision discussions |
| Password Hashing Competition | Winner (2015) | Official selection |

**Trajectory**: ASCENDING - Becoming the de facto standard

### bcrypt

| Body | Status | Document |
|------|--------|----------|
| OWASP | "Legacy systems only" | Password Storage Cheat Sheet |
| OpenBSD | Original implementation | Default system hash |
| NIST | Not specifically addressed | N/A |

**Trajectory**: STABLE-TO-DECLINING - Acceptable but being superseded

### scrypt

| Body | Status | Document |
|------|--------|----------|
| IETF | RFC 7914 (2016) | The scrypt Password-Based KDF |
| OWASP | Second choice (after Argon2) | Password Storage Cheat Sheet |

**Trajectory**: STABLE - Established but not preferred

### PBKDF2

| Body | Status | Document |
|------|--------|----------|
| NIST | SP 800-132 (2010) | Recommendation for Password-Based KDF |
| FIPS | 140-2/140-3 approved | Only FIPS-compliant option |
| OWASP | "If FIPS required" | Password Storage Cheat Sheet |

**Trajectory**: DECLINING but REQUIRED for FIPS compliance

## Security Research Attention

### Cryptanalysis Activity

| Algorithm | Active Research | Known Weaknesses | Confidence |
|-----------|----------------|------------------|------------|
| Argon2 | High (ongoing) | None significant | Very High |
| bcrypt | Low (mature) | No memory-hardness | High |
| scrypt | Medium | Parameter coupling | High |
| PBKDF2 | Low (mature) | GPU-vulnerable | Medium |

### Recent Publications (2023-2025)

**Argon2**:
- "Evaluating Argon2 Adoption and Effectiveness in Real-World Software" (2024)
- Red Hat Research: Attack cost analysis (2024)
- Multiple parameter tuning studies

**bcrypt**:
- Few new publications (algorithm considered "solved")
- Focus shifting to Argon2 comparison studies

**scrypt**:
- Mostly comparative studies with Argon2
- Parameter optimization research

## OWASP Recommendation Evolution

### Historical Timeline

| Year | Primary Recommendation | Notes |
|------|------------------------|-------|
| 2015 | bcrypt | Pre-Argon2 |
| 2016 | bcrypt, mention scrypt | Argon2 emerging |
| 2018 | bcrypt OR Argon2 | Equal status |
| 2020 | Argon2id preferred | bcrypt acceptable |
| 2023 | Argon2id primary | bcrypt for legacy only |
| 2025 | Argon2id primary | bcrypt explicitly legacy |

### Current OWASP Priority Order (2025)

1. **Argon2id** (primary)
2. **scrypt** (if Argon2 unavailable)
3. **bcrypt** (legacy systems only)
4. **PBKDF2** (FIPS compliance only)

## 5-Year Algorithm Forecast

### Argon2

| Factor | Forecast |
|--------|----------|
| Adoption | Continued growth |
| Standards | NIST adoption likely |
| Security | No concerns |
| Recommendation | PRIMARY for 5+ years |

### bcrypt

| Factor | Forecast |
|--------|----------|
| Adoption | Gradual decline |
| Standards | No new adoption |
| Security | Adequate but not optimal |
| Recommendation | ACCEPTABLE but declining |

### scrypt

| Factor | Forecast |
|--------|----------|
| Adoption | Niche/specialized |
| Standards | Stable |
| Security | Good |
| Recommendation | FALLBACK position |

### PBKDF2

| Factor | Forecast |
|--------|----------|
| Adoption | FIPS-only use |
| Standards | Will remain FIPS-approved |
| Security | Weakest of the options |
| Recommendation | FIPS COMPLIANCE ONLY |

## Post-Quantum Considerations

Password hashing algorithms are NOT directly affected by quantum computing:
- They don't rely on public-key cryptography
- Hash functions remain secure (Grover's algorithm halves effective bits)
- 256-bit outputs provide 128-bit post-quantum security

**Conclusion**: No quantum migration needed for password hashing.

## Strategic Implications

### For New Projects

Choose Argon2 (argon2-cffi):
- Standards trajectory is ascending
- OWASP primary recommendation
- Best security properties
- Will be the standard for foreseeable future

### For Existing bcrypt Projects

No urgent migration needed:
- bcrypt remains acceptable
- Plan gradual migration over 2-5 years
- Implement dual verification for smooth transition

### For FIPS Environments

Stuck with PBKDF2:
- NIST may eventually approve Argon2
- Until then, PBKDF2 with 600K+ iterations
- Consider compensating controls
