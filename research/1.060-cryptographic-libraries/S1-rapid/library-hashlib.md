# Library Assessment: hashlib (stdlib)

## Popularity Metrics (PRIMARY SIGNAL)

**PyPI Downloads**: N/A (standard library - bundled with Python)
**GitHub Stars**: N/A (part of CPython)
**Rank**: Universal (every Python installation)
**Classification**: Python standard library module

## Ecosystem Status

- **Maintained by**: Python core developers
- **Release cadence**: Python release schedule
- **Backend**: OpenSSL (typically)
- **Status**: Built-in, always available

## Quick Capability Check

**Core Features** (limited scope):
- Hash functions ONLY (MD5, SHA-1, SHA-2, SHA-3, BLAKE2)
- Key derivation (PBKDF2)
- No encryption (symmetric or asymmetric)
- No digital signatures
- No certificate handling

**SCOPE LIMITATION**: Hashing only, not a full crypto library

**Documentation**: Python standard library docs (excellent)

## FIPS Compliance Signal

- Supports FIPS mode when Python built with FIPS OpenSSL
- Blocks non-FIPS algorithms (MD5, SHA-1) in FIPS mode
- LIMITED SCOPE: Only covers hashing, not full FIPS suite

## Community Validation

- Universal adoption (it's built-in!)
- Extensively documented
- Well-understood by all Python developers
- Zero installation friction

## Red Flags Check

- **MAJOR LIMITATION**: Hashing only - not a complete crypto solution
- Cannot handle encryption/decryption
- Cannot handle digital signatures
- Cannot handle key exchange

## Speed Assessment: 1 minute

**Verdict**: INSUFFICIENT for full crypto needs (hashing only)
