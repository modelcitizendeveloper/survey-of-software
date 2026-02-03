# Maintainer Sustainability Analysis

## argon2-cffi

### Maintainer Profile

**Primary**: Hynek Schlawack
- **Type**: Individual (well-known Python community member)
- **Other projects**: attrs, structlog, doc2dash, prometheus-async
- **Track record**: 10+ years maintaining popular Python packages
- **Community standing**: PSF Fellow, conference speaker

### Funding Model

| Source | Status |
|--------|--------|
| Variomedia AG (employer) | ACTIVE |
| Tidelift subscription | ACTIVE |
| GitHub Sponsors | ACTIVE |
| Individual donations | ACTIVE |

### Bus Factor Assessment

| Factor | Score | Notes |
|--------|-------|-------|
| Single maintainer | RISK | One person controls releases |
| Well-documented codebase | MITIGATES | Easy for others to contribute |
| Popular ecosystem | MITIGATES | Community would likely adopt |
| Clear succession | UNKNOWN | No documented succession plan |

**Overall**: MODERATE RISK (well-funded individual with strong track record)

### 5-Year Viability: HIGH (85%)

Rationale:
- Stable funding model
- Strong community reputation
- Simple, focused codebase (easy to maintain)
- Algorithm is standards-track

---

## bcrypt (PyCA)

### Maintainer Profile

**Primary**: Python Cryptographic Authority (PyCA)
- **Type**: Organization
- **Members**: Multiple core maintainers (Alex Gaynor, Paul Kehrer, etc.)
- **Other projects**: cryptography, pyOpenSSL, PyNaCl
- **Track record**: 10+ years, industry standard libraries

### Funding Model

| Source | Status |
|--------|--------|
| Mozilla (via cryptography) | ACTIVE |
| Tidelift | ACTIVE |
| Corporate sponsors | ACTIVE |
| Individual donations | ACTIVE |

### Bus Factor Assessment

| Factor | Score | Notes |
|--------|-------|-------|
| Organization (multiple maintainers) | STRONG | No single point of failure |
| Corporate backing | STRONG | Mozilla, others |
| Industry standard | STRONG | Critical infrastructure |
| Clear governance | STRONG | PyCA has established processes |

**Overall**: LOW RISK (organization with multiple maintainers and funding)

### 5-Year Viability: VERY HIGH (95%)

Rationale:
- Organization structure with multiple maintainers
- Industry-critical infrastructure
- Stable corporate backing
- Proven 10+ year track record

---

## passlib

### Maintainer Profile

**Primary**: Eli Collins
- **Type**: Individual
- **Status**: INACTIVE since October 2020
- **Organization**: Assurance Technologies, LLC (defunct?)

### Funding Model

| Source | Status |
|--------|--------|
| Personal project | INACTIVE |
| No corporate backing | N/A |
| No sponsorship | N/A |

### Bus Factor Assessment

| Factor | Score | Notes |
|--------|-------|-------|
| Single maintainer | CRITICAL | Maintainer abandoned project |
| No succession | CRITICAL | No documented handoff |
| Complex codebase | WORSENS | 30+ algorithms, hard to maintain |
| Active forks | MITIGATES | libpass actively maintained |

**Overall**: CRITICAL RISK (effectively abandoned)

### 5-Year Viability: VERY LOW (10%)

Rationale:
- No releases in 4+ years
- Major frameworks migrating away (FastAPI, Ansible)
- No Python 3.13+ support
- Fork (libpass) is the continuation path

---

## hashlib.scrypt (stdlib)

### Maintainer Profile

**Primary**: Python Core Development Team
- **Type**: Organization (PSF-governed)
- **Size**: Hundreds of contributors
- **Governance**: PEP process, steering council

### Funding Model

| Source | Status |
|--------|--------|
| PSF | ACTIVE |
| Corporate sponsors (Google, Microsoft, etc.) | ACTIVE |
| Grants | ACTIVE |

### Bus Factor Assessment

| Factor | Score | Notes |
|--------|-------|-------|
| Large organization | VERY STRONG | PSF governance |
| Corporate backing | VERY STRONG | Major tech companies |
| Critical infrastructure | VERY STRONG | Python itself |
| Clear succession | VERY STRONG | PSF processes |

**Overall**: VERY LOW RISK (Python Foundation backed)

### 5-Year Viability: VERY HIGH (99%)

Rationale:
- Part of Python stdlib
- PSF governance guarantees maintenance
- Will exist as long as Python exists
- OpenSSL dependency is also well-maintained

---

## Summary: Maintainer Risk Matrix

| Library | Maintainer Type | Funding | Bus Factor | 5-Year Viability |
|---------|-----------------|---------|------------|------------------|
| argon2-cffi | Individual | Good | Moderate | 85% |
| bcrypt | Organization | Strong | Low | 95% |
| passlib | Individual | None | Critical | 10% |
| hashlib.scrypt | Organization (PSF) | Strong | Very Low | 99% |
| libpass | Individual | Unknown | Moderate | 70% |

## Strategic Recommendations

1. **Safest bet**: bcrypt (PyCA) or hashlib.scrypt (stdlib)
2. **Best algorithm + acceptable risk**: argon2-cffi
3. **Avoid**: passlib (use libpass fork if needed)
4. **Hedge**: Abstract password hashing behind interface for easy library swap
