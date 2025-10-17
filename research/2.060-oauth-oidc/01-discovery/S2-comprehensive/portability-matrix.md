# Portability Matrix: OAuth 2.0 / OpenID Connect

## Feature Parity Table

### Core OAuth 2.0 / OIDC Protocol Features

| Feature | Keycloak | Auth0 | Okta | Authentik | Ory Hydra | Azure AD | Google ID | GitHub | Standardized? |
|---------|----------|-------|------|-----------|-----------|----------|-----------|--------|---------------|
| **Authorization Code Flow** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ YES |
| **Authorization Code + PKCE** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ YES |
| **Client Credentials Flow** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ YES |
| **Implicit Flow** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ YES (deprecated) |
| **Hybrid Flow** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (custom) | ✅ | ❌ | ✅ YES |
| **Device Authorization Flow** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ YES (RFC 8628) |
| **Refresh Tokens** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ YES |
| **JWT Access Tokens** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ YES (RFC 7519) |
| **ID Tokens** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ YES (OIDC) |
| **OIDC Discovery** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ YES |
| **JWKS Endpoint** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ YES |
| **UserInfo Endpoint** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ YES |
| **Token Introspection** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ YES (RFC 7662) |
| **Token Revocation** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ YES (RFC 7009) |
| **Standard Scopes** (openid, profile, email) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ YES |
| **OpenID Connect Certified** | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | N/A |

**PORTABILITY VERDICT**: Core OAuth/OIDC protocol features are **FULLY PORTABLE** across all
OIDC-compliant providers (all except GitHub). Migration effort for protocol layer: **2-5 hours**.

**GitHub Exception**: GitHub provides OAuth 2.0 for authorization but NOT OpenID Connect for
authentication. It's not a general-purpose IdP.

---

### User Management APIs

| Feature | Keycloak | Auth0 | Okta | Authentik | Ory Hydra | Azure AD | Google ID | GitHub | Standardized? |
|---------|----------|-------|------|-----------|-----------|----------|-----------|--------|---------------|
| **User CRUD API** | Admin REST | Mgmt API v2 | Users API | REST API | ❌ External | Graph API | Identity API | Users API | ❌ NO |
| **User Search** | ✅ Custom | ✅ Lucene | ✅ Custom | ✅ Custom | ❌ | ✅ Custom | ✅ Custom | ✅ | ❌ NO |
| **User Attributes** | ✅ Custom | ✅ Metadata | ✅ Custom | ✅ Custom | ❌ | ✅ Custom | ✅ Custom | ✅ | ❌ NO |
| **Group Management** | ✅ Custom | ❌ (Roles) | ✅ Custom | ✅ Custom | ❌ | ✅ Groups | ✅ Custom | ✅ Orgs | ❌ NO |
| **SCIM 2.0 Provisioning** | ✅ (plugin) | ✅ Yes | ✅ Yes | ✅ Yes | ❌ | ✅ Yes | ✅ Yes | ❌ | ⚠️ SCIM (limited adoption) |
| **Password Management** | ✅ API | ✅ API | ✅ API | ✅ API | ❌ | ✅ API | ✅ API | ❌ | ❌ NO |
| **Bulk Import/Export** | ✅ Custom | ✅ Custom | ✅ Custom | ✅ Custom | ❌ | ✅ Custom | ✅ Custom | ❌ | ❌ NO |

**PORTABILITY VERDICT**: User management is **NOT PORTABLE**. Each provider has proprietary
APIs with different schemas, query syntaxes, and capabilities.

**SCIM Exception**: SCIM 2.0 provides standardized provisioning (create, update, delete users)
but has LIMITED adoption and does NOT cover all user management scenarios (bulk operations,
advanced search, custom attributes vary).

**Migration Impact**: User management API replacement: **20-60 hours** depending on complexity.

---

### Session Management

| Feature | Keycloak | Auth0 | Okta | Authentik | Ory Hydra | Azure AD | Google ID | GitHub | Standardized? |
|---------|----------|-------|------|-----------|-----------|----------|-----------|----------|---------------|
| **Session Creation** | ✅ Custom | ✅ Custom | ✅ Custom | ✅ Custom | ❌ External | ✅ Custom | ✅ Custom | ✅ Custom | ❌ NO |
| **Session Duration** | ✅ Config | ✅ Config | ✅ Config | ✅ Config | ❌ | ✅ Config | ✅ Config | ✅ | ❌ NO |
| **Session Revocation** | ✅ API | ✅ API | ✅ API | ✅ API | ❌ | ✅ API | ✅ API | ✅ | ❌ NO |
| **Active Sessions List** | ✅ Admin | ✅ Mgmt API | ✅ API | ✅ API | ❌ | ✅ Graph | ✅ API | ✅ | ❌ NO |
| **Single Logout** | ✅ Custom | ✅ Custom | ✅ Custom | ✅ Custom | ✅ Custom | ✅ Custom | ✅ Custom | ✅ | ⚠️ OIDC spec exists |
| **Session Monitoring** | ✅ Console | ✅ Dashboard | ✅ Console | ✅ UI | ❌ | ✅ Portal | ✅ Console | ✅ | ❌ NO |
| **Keep Me Signed In** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ NO |
| **IP Binding** | ⚠️ Custom | ❌ | ✅ (IE) | ⚠️ | ❌ | ⚠️ | ❌ | ❌ | ❌ NO |

**PORTABILITY VERDICT**: Session management is **PROVIDER-SPECIFIC**. While OpenID Connect
defines session management specifications (Front-Channel Logout, Back-Channel Logout), implementation
details, APIs, and capabilities vary significantly.

**Migration Impact**: Session management logic replacement: **10-30 hours**.

**Note**: OIDC Session Management 1.0 spec exists but is NOT universally implemented consistently.

---

### Multi-Factor Authentication (MFA)

| Feature | Keycloak | Auth0 | Okta | Authentik | Ory Hydra | Azure AD | Google ID | GitHub | Standardized? |
|---------|----------|-------|------|-----------|-----------|----------|-----------|--------|---------------|
| **TOTP (Authenticator Apps)** | ✅ | ✅ | ✅ | ✅ | ❌ (Kratos) | ✅ | ✅ | ✅ | ❌ NO (impl varies) |
| **SMS MFA** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ NO |
| **Email MFA** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ NO |
| **WebAuthn / FIDO2** | ✅ | ✅ | ✅ | ✅ | ❌ (Kratos) | ✅ | ✅ | ⚠️ | ⚠️ W3C standard |
| **Push Notifications** | ❌ | ✅ Guardian | ✅ Verify | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ NO |
| **Recovery Codes** | ✅ | ✅ | ✅ | ✅ | ❌ (Kratos) | ✅ | ✅ | ✅ | ❌ NO |
| **MFA Enrollment API** | ✅ Custom | ✅ Custom | ✅ Custom | ✅ Custom | ❌ | ✅ Custom | ✅ Custom | ✅ | ❌ NO |
| **MFA Policy Engine** | ✅ Flows | ✅ Rules/Actions | ✅ Policies | ✅ Flows | ❌ | ✅ Conditional | ✅ Custom | ❌ | ❌ NO |
| **Adaptive MFA** | ⚠️ Custom | ✅ Anomaly | ✅ Risk-based | ⚠️ Policies | ❌ | ✅ Identity Prot | ⚠️ | ❌ | ❌ NO |

**PORTABILITY VERDICT**: MFA is **NOT STANDARDIZED** by OAuth/OIDC. Each provider has
different enrollment flows, configuration APIs, and policy engines.

**WebAuthn Exception**: WebAuthn (FIDO2) has W3C standard, but enrollment and management
APIs are provider-specific.

**Migration Impact**: MFA reconfiguration and enrollment: **20-40 hours**.

---

### Social Login / Identity Federation

| Feature | Keycloak | Auth0 | Okta | Authentik | Ory Hydra | Azure AD | Google ID | GitHub | Standardized? |
|---------|----------|-------|------|-----------|-----------|----------|-----------|--------|---------------|
| **Google OAuth** | ✅ Config | ✅ Config | ✅ Config | ✅ Source | ❌ External | ✅ Config | N/A | ✅ | ⚠️ OAuth standard |
| **Facebook OAuth** | ✅ Config | ✅ Config | ✅ Config | ✅ Source | ❌ | ✅ Config | ✅ Config | ❌ | ⚠️ OAuth standard |
| **GitHub OAuth** | ✅ Config | ✅ Config | ✅ Config | ✅ Source | ❌ | ✅ Config | ✅ Config | N/A | ⚠️ OAuth standard |
| **SAML Federation** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ⚠️ SAML standard |
| **OIDC Federation** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ (EMU) | ✅ YES |
| **Attribute Mapping** | ✅ Custom | ✅ Custom | ✅ Custom | ✅ Custom | ❌ | ✅ Custom | ✅ Custom | ❌ | ❌ NO |
| **Account Linking** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ NO |

**PORTABILITY VERDICT**: While OAuth/OIDC protocols for federation are standard,
**CONFIGURATION is provider-specific**. Each provider has different:
- Connection setup UI/API
- Attribute mapping syntax
- Account linking logic
- Social provider buttons/UI

**Migration Impact**: Social login reconfiguration: **10-20 hours** (mostly manual config).

---

### Advanced Authentication Features

| Feature | Keycloak | Auth0 | Okta | Authentik | Ory Hydra | Azure AD | Google ID | GitHub | Standardized? |
|---------|----------|-------|------|-----------|-----------|----------|-----------|--------|---------------|
| **Custom Auth Flows** | ✅ Executions | ✅ Actions | ✅ Hooks | ✅ Flows/Stages | ❌ Webhooks | ✅ Extensions | ⚠️ | ❌ | ❌ NO |
| **Passwordless** | ✅ | ✅ | ✅ FastPass | ✅ | ❌ (Kratos) | ✅ | ✅ | ❌ | ❌ NO |
| **Risk-Based Auth** | ⚠️ Custom | ✅ Anomaly | ✅ Threat | ⚠️ Reputation | ❌ | ✅ Identity Prot | ⚠️ | ❌ | ❌ NO |
| **Attack Protection** | ⚠️ Custom | ✅ Built-in | ✅ ThreatInsight | ⚠️ Policies | ❌ | ✅ Built-in | ⚠️ | ⚠️ | ❌ NO |
| **Breached Pwd Check** | ❌ | ✅ HaveIBeenPwned | ⚠️ | ❌ | ❌ | ✅ | ❌ | ⚠️ | ❌ NO |
| **Bot Detection** | ❌ | ✅ | ⚠️ | ❌ | ❌ | ⚠️ | ✅ reCAPTCHA | ❌ | ❌ NO |

**PORTABILITY VERDICT**: Advanced authentication features are **HIGHLY PROPRIETARY**.
These represent major differentiators between providers and create SIGNIFICANT lock-in.

**Migration Impact**: Reimplementing advanced auth features: **40-100+ hours**.

---

## Vendor-Specific Extensions Summary

### Keycloak
- **Proprietary**: User Federation, Authorization Services (UMA 2.0), Authentication SPIs, Event Listeners
- **Lock-in Risk**: MEDIUM (high feature count, but open source aids migration)

### Auth0
- **Proprietary**: Rules (deprecated), Actions, Organizations, Universal Login customization, Anomaly Detection
- **Lock-in Risk**: HIGH (Actions have no standard equivalent)

### Okta
- **Proprietary**: Interaction Code Flow, Inline Hooks, Event Hooks, Okta Workflows, ThreatInsight, Identity Threat Protection
- **Lock-in Risk**: HIGH (Hooks/Workflows proprietary, AI features unique)

### Authentik
- **Proprietary**: Flows/Stages, Policy Engine (Python expressions), Property Mappings, Blueprints, Outposts
- **Lock-in Risk**: MEDIUM (simpler than Auth0/Okta, but flows are core concept)

### Ory Hydra
- **Proprietary**: Headless architecture (login/consent delegation), Kratos integration, Keto integration, Oathkeeper integration
- **Lock-in Risk**: LOW for Hydra alone, MEDIUM for Ory stack

### Azure AD
- **Proprietary**: Conditional Access, Custom Authentication Extensions, B2C Policies, Graph API, Hybrid Flow
- **Lock-in Risk**: HIGH (especially for B2C with XML policies)

### Google Identity Platform
- **Proprietary**: Firebase Authentication SDKs, Identity Platform Admin SDK, GCP integrations
- **Lock-in Risk**: MEDIUM (Firebase SDKs proprietary)

### GitHub OAuth
- **Proprietary**: Entire implementation (not OIDC)
- **Lock-in Risk**: LOW (because it's not a full IdP, limited use case)

---

## Lock-In Boundaries: Where Portability Breaks

### PORTABLE (Config-Only, <5 hours)
1. ✅ OAuth 2.0 / OIDC protocol flows
2. ✅ Token formats (JWT)
3. ✅ Discovery endpoints
4. ✅ Client credentials and redirect URIs
5. ✅ Standard scopes and claims

### BOUNDED PORTABILITY (Reconfiguration, 5-30 hours)
1. ⚠️ Social login providers (reconfigure each)
2. ⚠️ Basic MFA (TOTP, SMS) - reconfigure enrollment
3. ⚠️ Session timeouts (different APIs, similar concepts)
4. ⚠️ User data export/import (SCIM helps, but incomplete)
5. ⚠️ Password hashes (compatibility varies)

### NON-PORTABLE (Reimplementation, 30-100+ hours)
1. ❌ User management APIs (completely different)
2. ❌ Custom authentication flows/logic (Actions, Rules, Hooks, Flows, Executions)
3. ❌ Advanced security features (anomaly detection, threat protection, risk-based auth)
4. ❌ Authorization policies (fine-grained permissions)
5. ❌ Custom UI/UX (login pages, consent screens, enrollment)
6. ❌ Admin workflows and automation
7. ❌ Audit/event systems (different formats, APIs)
8. ❌ Multi-tenancy features (Organizations, B2C tenants)

---

## Migration Complexity Scoring

| Provider Switch | Standard OIDC Only | With User Mgmt | With MFA | Full Features | Portability Tier |
|-----------------|-------------------|----------------|----------|---------------|------------------|
| **Keycloak → Auth0** | 2-5 hrs | 30-50 hrs | 50-80 hrs | 80-150 hrs | PARTIAL |
| **Auth0 → Keycloak** | 2-5 hrs | 30-50 hrs | 50-80 hrs | 80-150 hrs | PARTIAL |
| **Okta → Keycloak** | 2-5 hrs | 30-50 hrs | 50-80 hrs | 100-150 hrs | PARTIAL |
| **Auth0 → Okta** | 2-5 hrs | 30-50 hrs | 50-80 hrs | 80-120 hrs | PARTIAL |
| **Authentik → Keycloak** | 2-5 hrs | 20-40 hrs | 40-60 hrs | 60-100 hrs | PARTIAL |
| **Ory Hydra → Any** | 2-5 hrs | 5-15 hrs | 20-40 hrs | 60-100 hrs | **TRUE** (Hydra alone) |
| **Azure AD → Auth0** | 2-5 hrs | 30-50 hrs | 50-80 hrs | 80-150 hrs | PARTIAL |
| **Google → Auth0** | 2-5 hrs | 30-50 hrs | 50-80 hrs | 80-120 hrs | PARTIAL |
| **GitHub → OIDC** | 10-20 hrs | 10-20 hrs | 20-30 hrs | 20-30 hrs | WEAK (not OIDC) |

**Key Insight**: Migration effort splits into TWO categories:
1. **Protocol layer** (OAuth/OIDC): 2-5 hours (TRUE PORTABILITY)
2. **Platform layer** (user mgmt, MFA, custom logic): 40-150 hours (LOCK-IN)

---

## Feature Parity Conclusion

**What's Truly Portable**:
- OAuth 2.0 authorization flows ✅
- OpenID Connect authentication flows ✅
- JWT token formats ✅
- Standard claims and scopes ✅
- Discovery endpoints ✅

**What's NOT Portable**:
- User management (CRUD, search, attributes) ❌
- Session management (APIs, monitoring) ❌
- MFA configuration and enrollment ❌
- Custom authentication logic ❌
- Advanced security features ❌
- Social login configuration ❌
- Admin and management APIs ❌

**VERDICT**: OAuth/OIDC provides **PARTIAL PORTABILITY**.

The standard covers **authentication protocol** (portable in 2-5 hours), but NOT
**identity management platform** (requires 40-150 hours to migrate).

True migration cost depends on how deeply you integrate with provider-specific features.
Minimal integration = TRUE portability. Deep integration = WEAK portability.
