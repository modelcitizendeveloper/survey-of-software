# S4 Strategic Recommendation

## Overall Strategic Assessment

| Library | Algorithm Trajectory | Maintainer Risk | 5-Year Viability | Strategic Score |
|---------|---------------------|-----------------|------------------|-----------------|
| argon2-cffi | ASCENDING | MODERATE | 85% | **A** |
| bcrypt | DECLINING | LOW | 95% | **B+** |
| hashlib.scrypt | STABLE | VERY LOW | 99% | **B** |
| passlib | N/A | CRITICAL | 10% | **F** |

## Primary Recommendation: argon2-cffi

### Strategic Rationale

1. **Algorithm is winning**: OWASP #1, RFC 9106, PHC winner
2. **Maintainer acceptable**: Well-funded individual with track record
3. **Migration risk low**: Algorithm will be standard for 10+ years
4. **No quantum concerns**: Hash functions unaffected

### Risk Mitigation

```python
# Abstract for future flexibility
from abc import ABC, abstractmethod

class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str: ...

    @abstractmethod
    def verify(self, password: str, hash: str) -> bool: ...

class Argon2Hasher(PasswordHasher):
    def __init__(self):
        from argon2 import PasswordHasher as ArgonPH
        self._ph = ArgonPH()

    def hash(self, password: str) -> str:
        return self._ph.hash(password)

    def verify(self, password: str, hash: str) -> bool:
        try:
            self._ph.verify(hash, password)
            return True
        except:
            return False

# Future-proof: can swap implementation without changing interface
hasher: PasswordHasher = Argon2Hasher()
```

## Secondary Recommendation: bcrypt (PyCA)

### When to Choose

- Maintainer stability is paramount
- Memory constraints exist
- Existing bcrypt codebase
- Need proven 10+ year track record

### Strategic Rationale

- **PyCA backing**: Organization with proven sustainability
- **Industry standard**: Critical infrastructure status
- **Algorithm acceptable**: Not optimal but still secure
- **Migration cost**: Low if already using bcrypt

## What to Avoid

### passlib

**Status**: Effectively dead
- Unmaintained since October 2020
- Major frameworks migrating away
- Use libpass fork if passlib API needed

### hashlib.scrypt (as primary)

**Not recommended as primary** despite high viability:
- Poor API for application code
- Parameter coupling makes tuning difficult
- Argon2 is superior algorithm

**Acceptable as**: Fallback or stdlib-only requirement

## Long-Term Strategy

### Phase 1: Current (2025)

| New Projects | Existing Projects |
|--------------|-------------------|
| argon2-cffi | Keep current algorithm |
| Default config | Plan migration roadmap |

### Phase 2: Migration (2025-2027)

| Action | Timeline |
|--------|----------|
| Deploy dual verification | Q1 2025 |
| Monitor upgrade rates | Ongoing |
| Force-reset legacy hashes | Q4 2026 |

### Phase 3: Consolidation (2027+)

| Action | Timeline |
|--------|----------|
| Remove legacy verification | 2027 |
| Argon2-only codebase | 2027+ |
| Monitor NIST developments | Ongoing |

## Decision Framework

```
Choosing password hashing library (strategic view):

1. Is FIPS-140 compliance required?
   YES → PBKDF2 (hashlib.pbkdf2_hmac)
   NO → Continue

2. Is this a new project?
   YES → argon2-cffi
   NO → Continue

3. Are you currently using bcrypt?
   YES → Keep bcrypt, plan 2-year migration to Argon2
   NO → Continue

4. Are you using passlib?
   YES → Migrate to libpass OR direct argon2-cffi/bcrypt
   NO → Continue

5. Default → argon2-cffi
```

## Final Verdict

| Scenario | Library | Confidence |
|----------|---------|------------|
| New project (default) | argon2-cffi | VERY HIGH |
| Risk-averse organization | bcrypt (PyCA) | HIGH |
| FIPS compliance | PBKDF2 | HIGH |
| Migrating from passlib | libpass or argon2-cffi | HIGH |
| Stdlib-only requirement | hashlib.scrypt | MEDIUM |

**Strategic winner**: argon2-cffi

The algorithm trajectory strongly favors Argon2, and the moderate maintainer risk is acceptable given the algorithm's standards-track status. If argon2-cffi were to become unmaintained, another library would quickly fill the gap due to Argon2's importance.
