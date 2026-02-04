# Provider Analysis: Authentik

## Overview

**Type**: Self-hosted, open-source
**Maintainer**: Authentik Security Inc.
**License**: Open source (permissive license)
**Positioning**: Modern, flexible Identity Provider focused on versatility and user experience

## OAuth/OIDC Standardization

### What's Standardized (Portable)

**Authentication Flows**:
- Authorization Code Flow (fully compliant)
- Implicit Flow (fully compliant)
- Hybrid Flow (fully compliant)
- Client Credentials Flow (fully compliant)
- Device Authorization Flow (RFC 8628)
- Resource Owner Password Credentials

**Token Support**:
- JWT access tokens with configurable signing
- ID tokens with standard OIDC claims
- Refresh tokens with configurable rotation
- Token introspection support
- Token revocation support

**Discovery & Standards**:
- OIDC Discovery (/.well-known/openid-configuration)
- JWKS endpoint for public key distribution
- Standard scopes: openid, profile, email, etc.
- UserInfo endpoint with standard claims
- OAuth 2.0 and OIDC protocol compliance

**Protocol Compliance**:
- OAuth 2.0 (RFC 6749, 6750)
- OpenID Connect Core 1.0
- OpenID Connect Discovery 1.0
- PKCE support (RFC 7636)
- JWT standards (RFC 7519)

### What's Provider-Specific (Non-Portable)

**User Management**:
- Authentik REST API (proprietary endpoints)
- User attributes and custom fields
- Group membership management
- User enrollment flows (Authentik-specific)
- User profile customization

**Authentication Features**:
- **Flows and Stages** (Authentik's core concept, proprietary)
- Stage bindings and execution order
- Policy engine (Authentik-specific)
- Expression policies (Python expressions)
- Reputation policies (failed login tracking)
- Consent management (Authentik-specific UI)
- Provider mappings (claim/attribute transformation)

**Session Management**:
- Authentik session handling
- Session timeouts and policies
- Active session management
- Device tracking and session revocation

**MFA/Security**:
- Authenticator configuration (TOTP, WebAuthn, Duo, etc.)
- MFA enrollment policies
- Device management and trust
- Recovery codes and backup methods
- Authenticator validation stages

**Advanced Features**:
- Source federation (delegate to other IdPs)
- Property mappings (transform user attributes)
- Blueprints (declarative configuration, Authentik-specific)
- Custom providers (SAML, LDAP, SCIM, Proxy, RAC)
- Outpost architecture (remote authentication)
- Event logging and webhooks
- Brand customization per-tenant
- User self-service portal

**Extensibility Model**:
- Python expressions in policies
- Custom stages (Python-based)
- Property mappings (transform claims)
- Event handlers and webhooks
- Blueprint system (YAML configuration)

## Configuration Approach

**Standard Configuration**:
- OAuth/OIDC providers with standard settings
- Redirect URIs and client credentials
- Scope and claim configuration
- OIDC Discovery for client auto-configuration

**Authentik-Specific Configuration**:
- Flow configuration (enrollment, authentication, recovery, consent)
- Stage configuration and bindings
- Policy attachments (when/how to execute)
- Property mappings for claim transformation
- Source configuration (external IdPs)
- Outpost configuration (remote deployment)
- Tenant branding and customization

## Migration Evidence

### Migrations TO Authentik

**Other IdPs → Authentik**:
- User import via API or database migration
- Password hash compatibility varies (bcrypt, pbkdf2, etc.)
- Flow recreation required (no standard migration)
- Estimated effort: **40-80 hours**

**Auth0/Okta → Authentik**:
- User export from managed service
- Actions/Rules → Authentik flows and policies (manual rebuild)
- Social connections reconfiguration
- Estimated effort: **60-100 hours**

### Migrations FROM Authentik

**Authentik → Keycloak**:
- User export via API
- Flow logic needs translation to Keycloak authentication flows
- Similar architecture helps, but config rebuild required
- Estimated effort: **40-80 hours**

**Authentik → Managed Services** (Auth0, Okta):
- User data export
- Flow and policy logic → provider-specific features
- Property mappings → provider claim configuration
- Estimated effort: **60-100 hours**

**Authentik → Other Self-Hosted**:
- Similar effort to Keycloak migration
- Standard OAuth/OIDC parts portable (2-5 hours)
- Custom flows and policies require rebuild (40-80 hours)
- Estimated effort: **40-80 hours**

## Known Migration Paths

### Authentik Documentation

**Migration Resources**:
- Blog post: "How to break up with your IdP: migrating to a new identity provider"
- API documentation for user export/import
- Blueprint system for configuration management
- Community migration guides

**Migration Approach**:
- Authentik positions itself as migration-friendly
- Emphasizes reducing IdP lock-in
- Supports multiple protocols (OIDC, SAML, LDAP, SCIM)
- Flow-based approach designed for flexibility

### Migration Complexity Factors

**Simple Migration** (standard OAuth/OIDC only):
- Update OIDC discovery URL
- Update client credentials
- Configure redirect URIs
- **Time: 2-5 hours**

**Complex Migration** (using Authentik-specific features):
- User data migration (API-based export/import)
- Flow recreation (enrollment, authentication, recovery)
- Policy configuration (reputation, expression policies)
- Stage configuration (MFA, consent, user verification)
- Property mapping setup (claim transformation)
- Provider mapping configuration
- Source configuration (external IdP federation)
- Outpost deployment (if used)
- Brand and theme customization
- **Time: 40-80 hours** (lower than Auth0/Okta due to simpler model)

## Portability Assessment

### Portable Features (Config-Only Migration)
- OAuth 2.0 / OIDC flows: ✅ Fully portable
- Token formats: ✅ Standard JWT
- Discovery endpoint: ✅ Standard OIDC Discovery
- Core authentication: ✅ Works with standard clients
- Password hashes: ✅ Common formats supported

### Non-Portable Features (Require Reimplementation)
- User management API: ❌ Authentik-specific
- Flows and stages: ❌ **CORE CONCEPT** - proprietary
- Policy engine: ❌ Authentik-specific (Python expressions)
- Session management: ❌ Provider-specific
- Property mappings: ❌ Authentik-specific transformation
- Provider mappings: ❌ Non-standard
- Blueprints: ❌ Authentik YAML format
- Outposts: ❌ Authentik architecture concept
- User enrollment flows: ❌ Proprietary UI/UX
- Consent management: ❌ Authentik-specific
- Source federation: ❌ Configuration non-portable

## Lock-In Risk Analysis

**LOW LOCK-IN** (if using):
- Standard OAuth/OIDC flows only
- Minimal flow customization
- No complex policies
- External user management

**MEDIUM LOCK-IN** (if using):
- Authentik user database
- Standard flows with minor customization
- Basic property mappings
- Simple policies (password strength, etc.)

**HIGH LOCK-IN** (if using):
- Complex custom flows (multi-stage enrollment, recovery)
- Expression policies (Python-based business logic)
- Extensive property mappings
- Outpost architecture
- Source federation with complex mappings
- Custom stages or policies
- Blueprints for infrastructure-as-code

## Feature Comparison Context

**Authentik's Strengths**:
- Modern, intuitive UI/UX
- Flow-based architecture (flexible)
- Open source with active development
- Multi-protocol support (OIDC, SAML, LDAP, SCIM, Proxy, RAC)
- Blueprint system (infrastructure-as-code)
- Outpost architecture (deployment flexibility)
- Lower resource footprint than Keycloak

**Authentik's Weaknesses**:
- Smaller community than Keycloak
- Less mature (newer project)
- Flow/stage model creates learning curve
- No official managed service
- Expression policies require Python knowledge

## Recommendations

**Choose Authentik if**:
- Want modern, user-friendly self-hosted IAM
- Need flexible flow-based authentication
- Require multi-protocol support (OIDC, SAML, LDAP, etc.)
- Value infrastructure-as-code (Blueprints)
- Want lighter-weight alternative to Keycloak
- Prefer Python-based extensibility

**Avoid Authentik if**:
- Need maximum portability (flows are non-standard)
- Require large community/ecosystem
- Want managed service option
- Need proven enterprise adoption
- Prefer minimal configuration complexity

**Portability Strategy**:
- Keep flows simple and close to standard authentication patterns
- Minimize expression policies (each one increases lock-in)
- Use standard property mappings where possible
- Document flow logic for migration planning
- Use SCIM for user provisioning where possible
- Avoid deep integration with Authentik-specific features
- Leverage Blueprints for configuration portability (within Authentik)

## Unique Characteristics

**Flow-Based Philosophy**:
- Authentik's core differentiator is flows and stages
- More flexible than traditional authentication flows
- Allows sophisticated authentication workflows
- **BUT**: This flexibility comes at portability cost
- No standard equivalent in other providers

**Infrastructure-as-Code**:
- Blueprint system allows configuration as YAML
- Portable within Authentik ecosystem
- Enables version control and repeatability
- Does NOT enable portability to other providers

**Multi-Protocol Versatility**:
- Single IdP can serve OIDC, SAML, LDAP, SCIM, Proxy, RAC
- Reduces need for multiple identity systems
- Each protocol has provider-specific configuration
- Portability is protocol-specific (OIDC parts portable, flows are not)

## Migration Time Estimates

Based on feature usage:

- **Minimal Authentik features**: 5-10 hours (mostly config + user data)
- **Standard flows + basic policies**: 30-50 hours
- **Complex flows + expression policies**: 60-80 hours
- **Extensive customization + outposts**: 80-120 hours

Lower than Auth0/Okta due to:
- Simpler extensibility model (no complex Actions/Hooks)
- Open source (can inspect internals)
- Clear flow/stage structure (easier to understand and recreate)
- Active community with migration focus

## Portability Verdict

Authentik sits between Keycloak and Auth0/Okta for portability:
- **Better than Auth0/Okta**: Simpler model, fewer proprietary extensions
- **Worse than minimal OIDC**: Flows and policies are non-standard
- **Similar to Keycloak**: Custom authentication logic creates lock-in

Use Authentik when flexibility and UX matter more than portability.
Use minimal OIDC provider when portability is top priority.
