# S1 Rapid Discovery: Password Hashing Libraries

## Approach

**Time budget**: 30 minutes
**Goal**: Identify the de facto standard Python password hashing library based on popularity metrics, security track record, and OWASP recommendations.

## Selection Criteria

1. **PyPI download volume** - ecosystem adoption signal
2. **Security track record** - CVE history, vulnerability disclosures
3. **OWASP recommendation status** - official security guidance
4. **Maintenance status** - active development, recent releases
5. **Organization backing** - individual vs organization maintainer

## Libraries Evaluated

| Library | Weekly Downloads | Maintainer | Last Release | CVEs |
|---------|-----------------|------------|--------------|------|
| argon2-cffi | 10.6M | Hynek Schlawack | Jun 2025 | 0 |
| bcrypt | 32.7M | PyCA | Sep 2025 | 0 (current) |
| passlib | 4.9M | Eli Collins | Oct 2020 | 0 (CVE), issues exist |
| hashlib.scrypt | stdlib | Python core | N/A | N/A |

## OWASP 2025 Priority Order

1. **Argon2id** - Primary recommendation (PHC winner)
2. **scrypt** - Fallback when Argon2 unavailable
3. **bcrypt** - Legacy systems only
4. **PBKDF2** - FIPS-140 compliance only

## Quick Decision Framework

- **New project?** → argon2-cffi (OWASP #1)
- **Existing bcrypt codebase?** → Keep bcrypt, plan migration
- **FIPS compliance required?** → PBKDF2 via hashlib
- **Need algorithm abstraction?** → Consider pwdlib (modern) or libpass (passlib fork)
