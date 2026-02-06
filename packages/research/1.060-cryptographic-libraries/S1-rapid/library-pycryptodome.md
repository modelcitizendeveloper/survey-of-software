# Library Assessment: pycryptodome

## Popularity Metrics (PRIMARY SIGNAL)

**PyPI Downloads**: 8,243,076 weekly downloads (8M+ per week)
**GitHub Stars**: ~3,100 stars
**Rank**: Key ecosystem project (Snyk)
**Classification**: PyCrypto fork/replacement

## Ecosystem Status

- **Maintained by**: Legrandin (single maintainer signal)
- **Origin**: Fork of deprecated PyCrypto
- **Release cadence**: Active maintenance
- **Status**: Drop-in replacement for legacy PyCrypto

## Quick Capability Check

**Core Features** (inferred):
- Full cryptographic suite (PyCrypto compatible)
- Symmetric/asymmetric encryption
- Hash functions
- Digital signatures
- Self-contained (no OpenSSL dependency)

**Use Case**: Projects migrating from PyCrypto or needing pure-Python crypto

**Documentation**: Available (pycryptodome.readthedocs.io likely)

## FIPS Compliance Signal

- **UNCLEAR**: Self-contained implementation (not OpenSSL-based)
- Likely NO FIPS compliance (would be heavily marketed if yes)
- Pure Python/C implementations = hard to certify
- Not mentioned in quick search results

## Community Validation

- 8M weekly downloads = significant usage
- 3.1K GitHub stars = decent community
- PyCrypto migration path = legacy project support
- Less popular than `cryptography` (8M vs 82M downloads)

## Red Flags Check

- Single-maintainer concern (vs PyCA's 330 contributors)
- Legacy compatibility focus (not modern best practices)
- Smaller community than `cryptography`
- No clear FIPS story

## Speed Assessment: 2 minutes

**Verdict**: VIABLE for legacy migration, SECOND-TIER for new projects
