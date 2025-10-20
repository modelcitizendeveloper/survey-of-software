# python-jose - Rapid Assessment

## Popularity Metrics (2025)

**Ecosystem Position: DECLINING**

- **Weekly Downloads**: 2,686,909 (still high!)
- **GitHub Stars**: 1,682 stars
- **Latest Version**: 3.5.0 (May 28, 2025)
- **Community**: Classified as "key ecosystem project"

## Quick Viability Check

### ⚠️ Requirements Coverage
- RFC 7519 compliant
- Supports HS256, RS256, ES256
- Includes JWE (encryption) - more than PyJWT
- Token validation and verification

### ❌ Security Track Record - RED FLAGS
**CVE-2024-33663**: Algorithm confusion vulnerability with OpenSSH ECDSA keys
**CVE-2024-33664**: JWT bomb DoS attack via compressed JWE tokens

**Fixed in**: 3.3.1 and 3.4.0+, but trust is damaged

### ⚠️ Maintenance Concerns
- FastAPI GitHub discussion: "Why is python-jose still recommended when it is nearly abandoned?"
- Community perception: "declining maintenance and community support"
- PyJWT migration guides appearing

## Rapid Decision Factors

**STRENGTHS:**
- Still gets 2.6M weekly downloads (legacy usage)
- More comprehensive than PyJWT (JWE support)
- Based on PyJWT originally (familiar API)

**CRITICAL WEAKNESSES:**
- **ABANDONMENT TRAJECTORY**: Community explicitly discussing it as "nearly abandoned"
- **Recent CVEs**: Two security vulnerabilities in 2024
- **Ecosystem shift**: FastAPI moving away from it
- **Future risk**: New vulnerabilities may not be fixed promptly

## Migration Signals

Multiple sources indicate ecosystem moving away:
- FastAPI discussions about replacing it
- "Why use python-jose over pyjwt?" issues
- Authlib provides migration guides FROM python-jose

## Bottom Line

**Speed Rating: ⚡⚡ (2/5) - DO NOT RECOMMEND**

Despite high download numbers (legacy inertia), this library is on the decline. Recent CVEs + abandonment concerns = red flag. The ecosystem is actively migrating away.

**Ecosystem Wisdom**: When FastAPI (huge user) is moving away, follow the herd.

**Status**: Legacy library with declining trust. Not a good choice for new projects in 2025.
