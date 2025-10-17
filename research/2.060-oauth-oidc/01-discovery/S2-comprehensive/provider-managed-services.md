# Provider Analysis: Managed Services (Azure AD, Google Identity, GitHub OAuth)

## Microsoft Azure AD / Entra ID

### Overview
**Type**: Managed service (SaaS), part of Microsoft cloud ecosystem
**Pricing**: Per-user with tiered features (Free, P1, P2)
**Positioning**: Enterprise workforce identity + customer identity (Azure AD B2C)

### OAuth/OIDC Standardization

**What's Standardized**:
- OAuth 2.0 flows (Authorization Code, Client Credentials, Implicit, Device Code)
- OIDC Core 1.0 compliance
- JWT tokens with standard claims
- OIDC Discovery endpoint
- Standard scopes and UserInfo endpoint

**What's Provider-Specific (Non-Portable)**:
- **Hybrid Flow** (mixes OIDC with OAuth code flow, Microsoft-specific)
- **Front Channel Logout** (Microsoft implementation)
- Token version management (v1.0 vs v2.0 tokens, endpoint-specific)
- Multi-tenant authority options (common, organizations, consumers, tenant-specific)
- Custom authentication extensions (external API integration)
- Conditional Access policies (Microsoft-specific security)
- Identity Protection (risk-based authentication)
- App manifest settings (oauth2AllowIdTokenImplicitFlow, etc.)
- Microsoft Graph API (proprietary user management)
- Azure AD B2C policies (custom authentication flows)

### Migration Considerations

**TO Azure AD**:
- User import via Graph API or Azure AD Connect
- Password hash sync (Azure AD Connect) or federated authentication
- Custom claims via optional claims configuration
- Estimated effort: **60-120 hours**

**FROM Azure AD**:
- User export via Graph API
- Conditional Access policies need reimplementation
- Custom authentication extensions lost
- B2C policies require complete rebuild
- Estimated effort: **80-150 hours** (B2C: 150-250 hours)

### Portability Assessment

**Portable**: OAuth/OIDC flows, tokens, discovery ✅
**Non-Portable**:
- Hybrid Flow ❌
- Conditional Access ❌
- Authentication extensions ❌
- B2C policies ❌
- Graph API ❌
- Token version logic ❌

### Lock-In Risk

- **MEDIUM-HIGH**: Conditional Access and custom extensions create significant lock-in
- **HIGH** for B2C: Custom policies are Microsoft-specific XML
- **CRITICAL**: Multi-tenant apps deeply tied to Azure AD authority model

### Unique Characteristics

**Strengths**:
- Deep Microsoft ecosystem integration (Office 365, Azure, Teams)
- Enterprise security features (Conditional Access, Identity Protection)
- B2C for customer identity with custom policies
- Extensive SaaS app integrations

**Weaknesses**:
- Complex pricing (Free vs P1 vs P2 vs B2C)
- B2C custom policies extremely proprietary (XML-based)
- Token version confusion (v1 vs v2)
- Different products (Azure AD vs Azure AD B2C) with different portability

---

## Google Cloud Identity Platform / Google OAuth

### Overview
**Type**: Managed service (SaaS), part of Google Cloud
**Pricing**: Usage-based (MAU for Identity Platform) or free (Google OAuth for social login)
**Positioning**: Consumer identity (Google Sign-In) + enterprise (Cloud Identity Platform)

### OAuth/OIDC Standardization

**What's Standardized**:
- OAuth 2.0 flows (Authorization Code, Client Credentials, Implicit, Device)
- OIDC Core 1.0 compliance
- JWT ID tokens with standard claims
- OIDC Discovery (/.well-known/openid-configuration)
- Standard scopes (openid, profile, email)
- UserInfo endpoint

**What's Provider-Specific (Non-Portable)**:
- Authentication handler endpoint (/__auth/handler, Google-hosted)
- Identity Platform specific configuration (GCP-specific)
- Firebase Authentication (proprietary SDKs and APIs)
- Google-specific flows (One Tap, Google Sign-In button)
- Admin SDK for provider management
- GCP-specific features (Workload Identity Federation)
- Google API scopes (gmail, drive, youtube, etc.)
- Firebase Realtime Database integration

### Migration Considerations

**TO Google Identity**:
- User import via Identity Platform API or Firebase import
- Password hash support (bcrypt, scrypt, HMAC, PBKDF, standard)
- OIDC provider configuration via Admin SDK
- Estimated effort: **40-80 hours**

**FROM Google Identity**:
- User export via Identity Platform API or Firebase export
- Google Sign-In flows need replacement
- Firebase-specific features lost
- Google API access requires reconfiguration
- Estimated effort: **60-100 hours** (Firebase: 80-120 hours)

### Portability Assessment

**Portable**: Standard OAuth/OIDC flows ✅
**Non-Portable**:
- Firebase Authentication SDKs ❌
- Google Sign-In button/One Tap ❌
- Google API scopes ❌
- Firebase integrations ❌
- Identity Platform GCP features ❌

### Lock-In Risk

- **LOW** for standard Google OAuth (social login only)
- **MEDIUM** for Identity Platform (GCP integration)
- **HIGH** for Firebase Authentication (proprietary SDKs and Realtime Database)

### Unique Characteristics

**Strengths**:
- Massive user base (Google accounts)
- Firebase ecosystem (mobile-first development)
- Good password hash compatibility
- Generous free tier for Google OAuth

**Weaknesses**:
- Identity Platform pricing can escalate
- Firebase SDKs are proprietary
- Google API scopes only work with Google (obvious but limiting)
- Strict OAuth policy compliance required

---

## GitHub OAuth

### Overview
**Type**: Managed service (SaaS), social login provider
**Pricing**: Free for public apps
**Positioning**: Developer authentication (not general-purpose IdP)

### OAuth/OIDC Standardization

**What's Standardized**:
- OAuth 2.0 Authorization Code Flow
- Access tokens for GitHub API access
- Standard OAuth endpoints (authorize, access_token)

**What's NOT Standardized (CRITICAL)**:
- **NO OpenID Connect support** (no ID tokens) ❌
- **NO UserInfo endpoint** (use GitHub API /user instead)
- **NO OIDC Discovery** ❌
- Only OAuth 2.0, NOT OIDC (authorization only, not authentication)

**GitHub-Specific Features**:
- GitHub App OAuth (different from OAuth Apps)
- GitHub API access (repos, issues, pull requests, etc.)
- Organization and team-based authorization
- OIDC for GitHub Actions (limited use case, not general IdP)
- Enterprise Managed Users (OIDC support, but only with Azure AD)

### Migration Considerations

**TO GitHub OAuth**:
- Limited use case (developer tools, GitHub-related apps)
- No user database (uses GitHub accounts)
- GitHub API scopes required
- Estimated effort: **10-20 hours** (simple integration)

**FROM GitHub OAuth**:
- Easy (not a full IdP, so limited dependencies)
- Replace with OIDC provider
- Update authorization flow (OAuth → OIDC)
- Estimated effort: **10-20 hours**

### Portability Assessment

**Portable**: OAuth 2.0 flows (limited) ⚠️
**Non-Portable**:
- NO OIDC support ❌ **CRITICAL**
- NO ID tokens ❌
- GitHub API dependencies ❌
- GitHub-specific scopes ❌

### Lock-In Risk

- **LOW** (because it's NOT a full IdP, just OAuth for GitHub API)
- **If used as authentication**: MEDIUM-HIGH (not standards-based)
- GitHub OIDC (Actions): HIGH (GitHub-specific, not general-purpose)

### Unique Characteristics

**Strengths**:
- Free for open-source and public apps
- Large developer user base
- Simple integration for developer tools

**Weaknesses**:
- **NOT an OIDC provider** (OAuth 2.0 only) ❌
- Limited to developer use cases
- No user profile customization
- OIDC support only for specific use cases (Actions, EMU)

**CRITICAL NOTE**: GitHub OAuth is NOT suitable for general authentication because
it lacks OpenID Connect (no ID tokens, no authentication layer). It's OAuth 2.0
for AUTHORIZATION only. Using it for authentication violates OAuth 2.0 principles
(OAuth is for delegation, OIDC is for authentication).

---

## Comparison Matrix: Managed Services

| Feature | Azure AD | Google Identity | GitHub OAuth |
|---------|----------|-----------------|--------------|
| **OIDC Compliant** | ✅ Yes | ✅ Yes | ❌ NO (OAuth only) |
| **Standard Flows** | ✅ Yes + Hybrid | ✅ Yes | ⚠️ OAuth only |
| **User Management API** | Graph API (MS) | Identity Platform (GCP) | GitHub API |
| **Session Management** | MS-specific | Google-specific | GitHub-specific |
| **MFA** | Conditional Access | Firebase/GCP | GitHub 2FA (not IdP) |
| **Migration FROM Effort** | 80-150 hrs | 60-100 hrs | 10-20 hrs |
| **Lock-In Risk** | Medium-High | Medium | Low (but limited) |
| **Portability** | Partial | Partial | Low (not OIDC) |

## Key Insights

1. **Azure AD**: Enterprise-focused, deep Microsoft integration, B2C has severe lock-in
2. **Google Identity**: Consumer-focused, Firebase creates SDK lock-in, Identity Platform more portable
3. **GitHub OAuth**: NOT an OIDC provider, developer-focused, limited use case

All three have proprietary features beyond OAuth/OIDC core, resulting in **PARTIAL PORTABILITY**.

Migration efforts range from 60-150 hours for full feature migrations, but **2-5 hours for
standard OAuth/OIDC flows only**.

The portability boundary is consistent: **Protocol is portable, platform features are not**.
