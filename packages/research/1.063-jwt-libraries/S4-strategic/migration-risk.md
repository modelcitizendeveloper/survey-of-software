# Migration Risk Analysis

## Overview
Migration risk encompasses both **migrating TO** a library (initial adoption cost) and **migrating FROM** a library (escape cost if it fails). Strategic selection considers both directions.

## Breaking Change Risk Assessment

### API Stability Track Record

#### PyJWT: HIGH BREAKING CHANGE HISTORY

**Major Breaking Changes**:

**v2.0.0 (2020)** - Massive ecosystem disruption
- `algorithms` parameter became REQUIRED in jwt.decode()
  - Previous: Optional parameter, defaulted to allow all algorithms
  - New: Must explicitly specify (security-driven change)
  - Impact: Every decode() call in ecosystem broke
- jwt.encode() return type changed
  - Previous: Returned bytes
  - New: Returns string
  - Impact: Code expecting bytes broke
- `.decode(..., verify=False)` parameter removed
  - Previous: Disable signature verification
  - New: Parameter removed entirely
  - Impact: Test code and development environments broke
- **No backward compatibility** - Hard cutover
- Ecosystem forced migration (Flask-JWT-Extended, etc.)

**v2.2.0 (2021)** - Surprise breaking change
- kwargs removal broke existing code
- Community complaints (Issue #698)
- Some users forced to downgrade to v2.1.0
- **No major version bump** - Unexpected breakage

**API Stability Philosophy**:
- Security > Backward Compatibility (justified but disruptive)
- Limited deprecation warnings
- Breaking changes in minor versions occasionally
- Migration guides available but community-driven

**Future Risk**: MODERATE-HIGH
- Future security issues may require more breaking changes
- Algorithm deprecations likely (HS256 → ES256 trend)
- Maintainer willing to break compatibility for security
- Pattern suggests more disruption ahead

---

#### python-jose: LOW BREAKING CHANGE RISK (Frozen)

**Major Breaking Changes**:

**v4.0.0** - Python version support
- Removed Python 2.7, 3.5 support
- Added Python 3.9 support
- Removed PyCrypto backend
- **Impact**: Moderate - mostly environment changes

**v3.3.0** - Last Python 2.7 release
- Minimal API changes
- Final version for legacy environments

**v3.2.0** - Backend improvements
- Cryptographic backend isolation
- Made pyca/cryptography preferred backend
- Removed `future` dependency
- **Impact**: Low - mostly internal changes

**API Stability Philosophy**:
- Historically stable API
- Most changes were backend/dependency updates
- Minimal user-facing disruption

**Future Risk**: N/A (Library unmaintained)
- No future breaking changes expected
- But also no future fixes or improvements
- **Frozen is not stable** - It's abandoned
- Eventually incompatible with modern Python (breaking by neglect)

---

#### Authlib: MODERATE BREAKING CHANGE RISK

**Major Breaking Changes**:

**v1.0.0 (2021)** - Planned breaking changes with migration guide
- SQLAlchemy integrations removed
  - Previous: Built-in database models
  - New: Users define own database layer
  - Migration: https://git.io/JkY4f
- OAuth 2.0 configuration method changes
  - Previous: OAUTH2_JWT_XXX config variables
  - New: .get_jwt_config() method on extensions
- JSON Web Key model redesign
  - Complete restructuring of JWK handling
- **Migration Guide Provided**: Official documentation for upgrade path

**v1.6.0 (2025)** - Surprise breaking change
- OAuth2Request API change (removed `body` parameter)
- Community reports breakage (Issue #781)
- **No migration warning** in release notes
- Pattern: Occasional minor version breakage

**v0.15 → v1.0** - Pre-1.0 churn
- Multiple refactors of JOSE implementations
- JSON Web Key redesign

**API Stability Philosophy**:
- Semantic versioning mostly followed
- Major versions = breaking changes (expected)
- **Occasional minor version breaks** (unexpected)
- Migration guides for major versions
- OAuth/OIDC standard evolution drives changes

**Future Risk**: MODERATE
- Comprehensive scope = more breaking change surface area
- OAuth 2.1, OIDC updates may require changes
- Business customers provide pressure for stability
- But correctness prioritized over compatibility

---

#### jwcrypto: MODERATE BREAKING CHANGE RISK (Security-Driven)

**Major Breaking Changes**:

**v1.4 (2022)** - Security-driven API break
- Token type auto-detection removed (CVE-2022-3102 fix)
- **Breaking Change**: Applications must explicitly specify token type
- **Impact**: High - Auto-detection was convenient feature
- **Migration Support**:
  - "born-deprecated" module variable for legacy compatibility
  - Heuristics added in later versions for safe auto-detection
  - Clear documentation of security implications
- **Reason**: Critical security vulnerability required API change

**Post-1.4 improvements**:
- Later releases added safer heuristics
- Backward compatibility improved where secure
- Migration path maintained for legacy code

**API Stability Philosophy**:
- **Security always > Backward Compatibility**
- Will break APIs for security without hesitation
- Provides migration paths but strongly discourages unsafe workarounds
- Conservative, deliberate approach otherwise
- Red Hat enterprise focus encourages stability where possible

**RHEL Stability Advantage**:
- RHEL major versions maintain API stability (10-year lifecycle)
- Backports security fixes without breaking changes in RHEL branches
- PyPI versions may break, but RHEL versions stable
- Enterprise customers get long-term API guarantees

**Future Risk**: MODERATE
- Future security issues may require breaking changes
- JOSE/JWT standard evolution (new algorithms, deprecations)
- But Red Hat enterprise focus limits unnecessary breaks
- Security fixes non-negotiable

---

## Migration Cost Analysis

### Migrating TO Each Library (Adoption Cost)

#### Adopting PyJWT (From Scratch)
**Effort**: 1-2 days
- Simple, minimal API
- encode() / decode() core functions
- Good documentation
- Large community (Stack Overflow)
- **Complexity**: LOW

#### Adopting python-jose (From Scratch)
**Effort**: N/A - DO NOT ADOPT
- Unmaintained library
- Should never be selected for new projects
- **Complexity**: IRRELEVANT

#### Adopting Authlib (From Scratch)
**Effort**: 3-5 days
- Comprehensive feature set (learning curve)
- JWT is subset of full OAuth/OIDC library
- Excellent documentation
- Type hints and modern Python
- **Complexity**: MODERATE (comprehensive scope)

#### Adopting jwcrypto (From Scratch)
**Effort**: 3-5 days
- Object-oriented API (more explicit than PyJWT)
- Comprehensive JOSE implementation
- Good documentation (Red Hat quality)
- Less community content (smaller ecosystem)
- **Complexity**: MODERATE (comprehensive JOSE)

---

### Migrating FROM Each Library (Escape Cost)

#### Escaping PyJWT

**To python-jose**: 1-2 days
- 100% API compatible (according to community)
- Import path changes
- Function signatures nearly identical
- **But python-jose is unmaintained - DON'T DO THIS**

**To Authlib**: 3-5 days
```python
# PyJWT
import jwt
token = jwt.encode({"sub": "user123"}, secret, algorithm="HS256")
claims = jwt.decode(token, secret, algorithms=["HS256"])

# Authlib
from authlib.jose import jwt
header = {"alg": "HS256"}
token = jwt.encode(header, {"sub": "user123"}, secret)
claims = jwt.decode(token, secret)
```
- Different import paths
- Similar conceptual model
- Header explicit vs implicit
- **Effort**: 3-5 days for typical application

**To jwcrypto**: 5-10 days
```python
# PyJWT
import jwt
token = jwt.encode({"sub": "user123"}, secret, algorithm="HS256")
claims = jwt.decode(token, secret, algorithms=["HS256"])

# jwcrypto
from jwcrypto import jwt, jwk
key = jwk.JWK(kty="oct", k=base64url_encode(secret))
token = jwt.JWT(header={"alg": "HS256"}, claims={"sub": "user123"})
token.make_signed_token(key)
parsed = jwt.JWT(key=key, jwt=token.serialize())
claims = json.loads(parsed.claims)
```
- Completely different API (OOP vs functional)
- Explicit key objects (JWK)
- More verbose but more control
- **Effort**: 5-10 days for typical application

**Lock-in Level**: LOW
- Simple API makes migration straightforward
- Standard JWT format (tokens portable)
- Multiple alternatives available

---

#### Escaping python-jose

**To PyJWT**: 1-3 days
```python
# python-jose
from jose import jwt
token = jwt.encode({"sub": "user123"}, secret, algorithm="HS256")
claims = jwt.decode(token, secret, algorithms=["HS256"])

# PyJWT (nearly identical)
import jwt
token = jwt.encode({"sub": "user123"}, secret, algorithm="HS256")
claims = jwt.decode(token, secret, algorithms=["HS256"])
```
- Import path change (jose → jwt)
- Function signatures 100% compatible
- Minimal refactoring needed
- **RECOMMENDED MIGRATION PATH**

**To Authlib**: 3-5 days
- Similar effort to PyJWT → Authlib migration
- API patterns similar
- **Effort**: 3-5 days

**To joserfc**: 5-7 days
- Purpose-built python-jose replacement
- Official migration guide: https://jose.authlib.org/en/migrations/python-jose/
- Type hints and modern Python
- More refactoring than PyJWT migration
- **Effort**: 5-7 days

**Lock-in Level**: VERY LOW
- API nearly identical to PyJWT
- Standard JWT format
- Easy migration paths exist
- Community recommends migrating away

---

#### Escaping Authlib

**JWT-Only Usage** (Low Lock-in):

**To PyJWT**: 3-5 days
- Reverse of PyJWT → Authlib migration
- Different API patterns
- **Effort**: 3-5 days

**To jwcrypto**: 5-7 days
- Both comprehensive JOSE implementations
- Different API philosophies
- **Effort**: 5-7 days

**Full OAuth/OIDC Usage** (High Lock-in):

**To Custom OAuth**: 2-4 weeks
- No complete replacement exists in Python ecosystem
- Must implement OAuth 2.0 server/client from scratch
- OIDC provider capabilities rare
- **Effort**: 2-4 weeks (major project)

**To Framework-Specific OAuth**: 1-2 weeks
- Flask-Dance, Django-OAuth-Toolkit, etc.
- Framework-specific replacements
- Limited to specific frameworks
- **Effort**: 1-2 weeks

**Lock-in Level**: MODERATE (JWT-only) to HIGH (Full OAuth)
- JWT-only users: Low lock-in, easy migration
- OAuth users: High lock-in, comprehensive features rare
- Comprehensive scope creates dependency

---

#### Escaping jwcrypto

**To PyJWT**: 5-10 days
- Significant API refactoring (OOP → functional)
- Different key handling (explicit JWK → implicit keys)
- More verbose → simpler (lose explicitness)
- **Effort**: 5-10 days

**To Authlib**: 5-7 days
- Both comprehensive JOSE libraries
- Similar feature parity
- Different API conventions
- **Effort**: 5-7 days

**Lock-in Level**: MODERATE
- API differences create moderate refactoring effort
- Full JOSE implementation (JWK, JWS, JWE) may be utilized
- Standard JWT format (tokens portable)
- Red Hat backing makes migration unlikely to be necessary

---

## Migration Trigger Conditions

### When to Migrate Away (Warning Signs)

#### PyJWT Warning Signs:
- ✗ No releases for 12+ months
- ✗ Critical CVE unpatched for 90+ days
- ✗ Maintainer announces departure without successor
- ✗ Major dependencies deprecated/unmaintained

**Contingency Plan**:
- Prepare PyJWT → Authlib migration plan (3-5 day effort)
- Monitor maintainer activity quarterly
- Have internal fork capability ready

#### python-jose Warning Signs (ALREADY TRIGGERED):
- ✓ No releases for years (TRIGGERED)
- ✓ Critical CVEs unpatched (TRIGGERED)
- ✓ Maintainer non-responsive (TRIGGERED)
- ✓ Major projects migrating away (TRIGGERED)

**Action Required**: Migrate immediately

#### Authlib Warning Signs:
- ✗ Commercial business fails (lepture company closure)
- ✗ No releases for 12+ months
- ✗ Maintainer announces departure without business transfer
- ✗ Enterprise sponsors withdraw

**Contingency Plan**:
- Very low risk due to business model
- 130+ contributors could fork if needed
- Monitor business health annually

#### jwcrypto Warning Signs:
- ✗ Red Hat removes from RHEL (extremely unlikely)
- ✗ All 3 maintainers leave Red Hat
- ✗ Latchset project archived
- ✗ No RHEL releases for 18+ months

**Contingency Plan**:
- Extremely low risk due to RHEL dependency
- 10-year support cycles guarantee maintenance
- Monitor RHEL package status annually

---

## Breaking Change Mitigation Strategies

### Version Pinning Strategy

**Conservative Approach** (Recommended for Production):
```python
# requirements.txt
PyJWT==2.10.1  # Pin exact version
# or
Authlib>=1.6,<2.0  # Major version lock
# or
jwcrypto>=1.5,<2.0  # Major version lock
```

**Benefits**:
- Prevents surprise breaking changes
- Controlled upgrade testing
- Security patches require explicit review

**Risks**:
- May miss security patches
- Manual upgrade burden
- Dependency conflict resolution

### Automated Compatibility Testing

**Pre-Upgrade Testing**:
1. Dedicated test environment
2. Upgrade dependency
3. Run full test suite
4. Test authentication/authorization flows
5. Review changelogs for breaking changes
6. Deploy to staging before production

### Migration Budget Planning

**Budget 5-10 days** for library migration in project planning:
- Allows switching libraries if needed
- Insurance against abandonment
- Reduces migration pressure

---

## Strategic Migration Recommendations

### For New Projects

**Choose Low Migration Risk**:
1. **Authlib** or **jwcrypto** (lowest organizational risk)
   - Migration unlikely to be necessary
   - But if needed, 5-7 days to switch
2. **PyJWT** (higher risk, but simple escape)
   - Higher chance of needing to migrate
   - But only 3-5 days to Authlib

**Avoid High Switching Cost** locked to unmaintained:
- **python-jose** - Already requires migration

### For Existing Projects

**On PyJWT**:
- **Stay** if satisfied with current maintenance
- **Monitor** maintainer activity quarterly
- **Prepare** migration plan to Authlib (3-5 days)
- **Test** migration path in development environment

**On python-jose**:
- **Migrate immediately** to PyJWT (1-3 days) or Authlib (3-5 days)
- **Security risk** remaining on python-jose
- **Plan** 1-2 week migration window

**On Authlib**:
- **Stay** - Best long-term viability
- **Low migration risk** - Unlikely to need
- **Monitor** business health annually

**On jwcrypto**:
- **Stay** - Excellent long-term viability
- **Very low migration risk** - RHEL guarantee
- **Monitor** RHEL package status annually

---

## Migration Risk Summary

| Library     | Breaking Change Risk | Escape Cost (Days) | Lock-in Level | Migration Likelihood |
|-------------|---------------------|-------------------|---------------|---------------------|
| PyJWT       | HIGH                | 3-5 (to Authlib)  | LOW           | MODERATE (single maintainer) |
| python-jose | N/A (Frozen/Dead)   | 1-3 (to PyJWT)    | VERY LOW      | IMMEDIATE (unmaintained) |
| Authlib     | MODERATE            | 3-5 (JWT-only)    | MODERATE      | LOW (commercial backing) |
| jwcrypto    | MODERATE            | 5-10 (to PyJWT)   | MODERATE      | VERY LOW (RHEL guarantee) |

### Strategic Verdict

**Lowest Total Migration Risk**: **Authlib** or **jwcrypto**
- Unlikely to need migration (strong backing)
- Moderate effort if migration needed
- Best long-term risk-adjusted position

**Moderate Migration Risk**: **PyJWT**
- Higher chance of needing migration
- But low effort to escape
- Acceptable risk with monitoring

**Unacceptable Migration Risk**: **python-jose**
- Migration required immediately
- Currently security liability
- Not viable for any timeline
