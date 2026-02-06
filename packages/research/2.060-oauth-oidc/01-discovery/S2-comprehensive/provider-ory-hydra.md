# Provider Analysis: Ory Hydra

## Overview

**Type**: Self-hosted, open-source OAuth 2.0 and OIDC Server
**Maintainer**: Ory (also offers Ory Network - managed service)
**License**: Apache 2.0
**Positioning**: Cloud-native, minimal, OAuth 2.0/OIDC-focused authorization server (headless)

## OAuth/OIDC Standardization

### What's Standardized (Portable)

**Authentication Flows**:
- Authorization Code Flow (fully compliant)
- Implicit Flow (fully compliant)
- Hybrid Flow (fully compliant)
- Client Credentials Flow (fully compliant)
- Device Authorization Flow (RFC 8628)
- Resource Owner Password Credentials Flow
- JWT Bearer Grant (RFC 7523)

**Token Support**:
- JWT access tokens (configurable signing algorithms)
- Opaque access tokens (with introspection)
- ID tokens with standard OIDC claims
- Refresh tokens with rotation support
- Token introspection (RFC 7662)
- Token revocation (RFC 7009)

**Discovery & Standards**:
- OIDC Discovery (/.well-known/openid-configuration)
- JWKS endpoint for public key distribution
- Standard scopes: openid, profile, email, address, phone, offline_access
- UserInfo endpoint (/userinfo)
- **OpenID Connect Certified** provider

**Protocol Compliance**:
- OAuth 2.0 (RFC 6749, 6750)
- OpenID Connect Core 1.0 (certified)
- OpenID Connect Discovery 1.0
- PKCE (RFC 7636)
- JWT (RFC 7519)
- OAuth 2.0 Token Introspection (RFC 7662)
- OAuth 2.0 Token Revocation (RFC 7009)
- OAuth 2.0 Mutual-TLS (RFC 8705)

### What's Provider-Specific (Non-Portable)

**Architecture Model**:
- **Headless design** (NO built-in UI for login, consent, etc.)
- Requires external identity provider integration (Ory Kratos, custom, etc.)
- Separation of concerns: Hydra = OAuth/OIDC, Kratos = user management
- Microservices architecture (not monolithic like Keycloak)

**User Management**:
- **NO built-in user management** (by design)
- Must integrate with external user system (Ory Kratos or custom)
- User attributes managed outside Hydra
- Ory Kratos API (if using Kratos) is proprietary

**Authentication Features**:
- Login flow delegation (external login UI required)
- Consent flow delegation (external consent UI required)
- Logout flow delegation
- Session management (if using Kratos)
- **Hydra only validates OAuth flows, doesn't authenticate users**

**Session Management**:
- Session handled by external identity provider (Kratos or custom)
- Hydra manages OAuth sessions (consent, grants)
- Logout flows customizable via external endpoints

**MFA/Security**:
- **NO built-in MFA** (handled by external IdP)
- If using Ory Kratos: TOTP, WebAuthn, recovery codes
- MFA logic external to Hydra

**Advanced Features**:
- Client management API (Ory-specific)
- Dynamic client registration (standard, but with Ory extensions)
- Policy engine for consent validation
- OAuth 2.0 introspection for policy decisions
- Ory Keto integration (permissions/authorization)
- Ory Oathkeeper integration (zero-trust proxy)

**Extensibility Model**:
- **Webhook-based extensibility** (login/consent/logout flows)
- Hydra delegates to external URLs for UI/UX
- Custom login provider implementation required
- Custom consent provider implementation required
- Integration via REST APIs (language-agnostic)

## Configuration Approach

**Standard Configuration**:
- OAuth 2.0 client registration (standard properties)
- Grant types and response types
- Redirect URIs and scopes
- Token lifetimes and signing algorithms
- OIDC Discovery endpoint configuration

**Ory-Specific Configuration**:
- Login provider URL (external endpoint)
- Consent provider URL (external endpoint)
- Logout redirect URLs
- Hydra + Kratos integration (if using Ory stack)
- Subject identifier algorithms
- Database backend (PostgreSQL, MySQL, CockroachDB)

## Migration Evidence

### Migrations TO Ory Hydra

**Other Providers → Ory Hydra**:
- Requires building login/consent UI (significant effort)
- User management needs external system (Kratos or custom)
- OAuth flows straightforward, user layer complex
- Estimated effort: **60-120 hours** (mostly building external components)

**Keycloak → Ory Hydra**:
- Move from monolithic to microservices architecture
- User data migration to Kratos or custom system
- Rebuild authentication UI
- Rebuild admin workflows
- Estimated effort: **100-150 hours**

### Migrations FROM Ory Hydra

**Ory Hydra → Keycloak/Authentik**:
- User data in Kratos or custom system (not in Hydra)
- OAuth client configuration portable
- Lose microservices architecture (may be benefit or drawback)
- Estimated effort: **40-80 hours**

**Ory Hydra → Managed Services** (Auth0, Okta):
- User data migration from Kratos or custom system
- OAuth flows portable (standard OIDC)
- Custom login/consent UIs discarded (use provider UIs)
- Estimated effort: **40-80 hours** (easier than other directions)

**Ory Hydra → Other OIDC**:
- Most portable provider due to minimal features
- OAuth/OIDC configuration directly portable
- User management handled externally anyway
- Estimated effort: **5-20 hours** (if user system stays separate)

## Known Migration Paths

### Ory Documentation

**Migration Support**:
- Ory provides migration guides between Hydra versions
- No specific guides for migrations to/from other providers
- Community documentation for Keycloak → Ory migrations
- Emphasis on standards compliance for portability

**Architecture Considerations**:
- Hydra's headless design makes it more portable (fewer opinions)
- But also requires more external integration work
- Trade-off: Less lock-in but more initial implementation effort

### Migration Complexity Factors

**Simple Migration** (OAuth/OIDC flows only):
- Hydra is MOST portable for standard OAuth flows
- Update OIDC discovery URL
- Update client credentials
- No user management tied to Hydra
- **Time: 2-5 hours**

**Complex Migration** (full Ory stack):
- User data migration from/to Kratos
- Rebuild login/consent UIs (if moving TO Hydra)
- Kratos configuration and schemas (Ory-specific)
- Ory Keto permissions (if used)
- Ory Oathkeeper policies (if used)
- Custom webhook integrations
- **Time: 60-120 hours** (mostly non-Hydra components)

## Portability Assessment

### Portable Features (Config-Only Migration)
- OAuth 2.0 / OIDC flows: ✅ **MOST PORTABLE** (certified, minimal)
- Token formats: ✅ Standard JWT or opaque
- Discovery endpoint: ✅ Standard OIDC Discovery
- Core authentication: ✅ Pure OAuth/OIDC, no proprietary extensions
- Client configuration: ✅ Standard OAuth client properties

### Non-Portable Features (Require Reimplementation)
- User management: ✅ **EXTERNAL** (actually aids portability)
- Login UI: ❌ Custom implementation required
- Consent UI: ❌ Custom implementation required
- Session management: ❌ External system (Kratos or custom)
- MFA configuration: ❌ External system
- Ory Kratos integration: ❌ Ory-specific (if used)
- Ory Keto integration: ❌ Ory-specific (if used)
- Ory Oathkeeper integration: ❌ Ory-specific (if used)

## Lock-In Risk Analysis

**LOW LOCK-IN** (Hydra alone):
- Pure OAuth 2.0 / OIDC server
- No proprietary protocol extensions
- Headless design = no UI lock-in
- User management external = no user data lock-in
- **Hydra itself has LOWEST lock-in of any provider**

**MEDIUM LOCK-IN** (Ory stack):
- Ory Kratos for user management (proprietary API)
- Custom login/consent UIs (effort to rebuild)
- Kratos identity schemas (Ory-specific)

**HIGH LOCK-IN** (full Ory ecosystem):
- Ory Keto for permissions (proprietary permission system)
- Ory Oathkeeper for zero-trust proxy (Ory-specific)
- Deep integration across Ory stack
- Webhook-based customizations throughout

## Feature Comparison Context

**Ory Hydra's Strengths**:
- **Maximum OAuth/OIDC portability** (certified, minimal, no proprietary extensions)
- Cloud-native, microservices architecture
- Language-agnostic (REST APIs, no SDK lock-in)
- Headless design (bring your own UI)
- Lightweight and performant
- OpenID Connect certified
- Strong security focus

**Ory Hydra's Weaknesses**:
- Requires external user management (more implementation work)
- Must build login/consent UIs (not turnkey)
- Microservices complexity (multiple components)
- Smaller community than Keycloak
- Requires more upfront development effort

## Recommendations

**Choose Ory Hydra if**:
- **Portability is TOP priority** (least lock-in of any provider)
- Want microservices architecture
- Have development resources for custom UIs
- Need cloud-native, containerized solution
- Prefer minimal, focused tools (Unix philosophy)
- Want language-agnostic integration

**Avoid Ory Hydra if**:
- Need turnkey solution (prefer Keycloak/Auth0)
- Want built-in user management
- Lack resources to build login/consent UIs
- Prefer monolithic architecture
- Need quick time-to-market

**Portability Strategy**:
- Hydra itself is HIGHLY portable (pure OAuth/OIDC)
- Keep user management in separate system (aids portability)
- Use standard OAuth/OIDC clients (not Ory-specific SDKs)
- Minimize integration with other Ory products (Keto, Oathkeeper)
- Document webhook integrations for migration planning

## Unique Characteristics

**Headless Philosophy**:
- Hydra provides OAuth/OIDC protocol, NOT user experience
- Requires external login provider (UI + authentication logic)
- This separation INCREASES portability (fewer opinions, less lock-in)

**Microservices Architecture**:
- Ory Hydra: OAuth 2.0 and OpenID Connect server
- Ory Kratos: User management and authentication
- Ory Keto: Permissions and authorization (Zanzibar-inspired)
- Ory Oathkeeper: Identity and access proxy
- Each component replaceable independently

**OAuth/OIDC Purity**:
- Hydra is ONLY an OAuth/OIDC server (not IAM platform)
- No user management, no MFA, no admin console
- This minimalism = maximum standards compliance = best portability

## Migration Time Estimates

Based on usage pattern:

- **Hydra alone** (with external user system): 5-15 hours to migrate
- **Hydra + custom UIs**: 20-40 hours (reuse UIs, update endpoints)
- **Ory stack** (Hydra + Kratos): 50-80 hours (Kratos migration)
- **Full Ory ecosystem** (Hydra + Kratos + Keto + Oathkeeper): 100-150 hours

**Paradox**: Hydra has LOWEST lock-in but HIGHEST initial implementation effort.
Other providers have MORE lock-in but LOWER initial implementation effort.

## Portability Verdict

**Ory Hydra: HIGHEST OAuth/OIDC portability** among all providers analyzed.

Why:
- OpenID Connect certified (pure standards compliance)
- No proprietary protocol extensions
- Headless design (no UI lock-in)
- External user management (no user data lock-in)
- Microservices architecture (components replaceable)
- Language-agnostic (REST APIs, no SDK lock-in)

But:
- Requires more initial development (not turnkey)
- Ory ecosystem (Kratos, Keto, Oathkeeper) CAN create lock-in if deeply integrated
- Portability benefit only realized if keeping concerns separated

**Use Hydra when**: Portability and standards compliance are more important than
time-to-market and built-in features.
