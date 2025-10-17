# Provider Analysis: Keycloak

## Overview

**Type**: Self-hosted, open-source
**Maintainer**: Red Hat (CNCF)
**License**: Apache 2.0
**Positioning**: Comprehensive identity and access management (IAM) solution

## OAuth/OIDC Standardization

### What's Standardized (Portable)

**Authentication Flows**:
- Authorization Code Flow (fully compliant)
- Implicit Flow (fully compliant)
- Hybrid Flow (fully compliant)
- Client Credentials Flow (fully compliant)
- Device Authorization Flow (RFC 8628)
- Resource Owner Password Credentials (discouraged but supported)

**Token Support**:
- JWT access tokens (RFC 7519)
- ID tokens with standard claims (OIDC Core 1.0)
- Refresh tokens with configurable rotation
- Token introspection (RFC 7662)
- Token revocation (RFC 7009)

**Discovery & Standards**:
- OIDC Discovery (/.well-known/openid-configuration)
- JWKS endpoint for public key verification
- Standard scopes: openid, profile, email, address, phone
- Standard claims fully supported
- UserInfo endpoint (OIDC Core 1.0)

**Protocol Compliance**:
- OAuth 2.0 (RFC 6749, 6750)
- OpenID Connect Core 1.0
- OpenID Connect Discovery 1.0
- OpenID Connect Session Management
- OpenID Connect Front-Channel Logout
- OpenID Connect Back-Channel Logout

### What's Provider-Specific (Non-Portable)

**User Management**:
- Admin REST API (proprietary endpoints)
- User federation (LDAP/Kerberos integration)
- User storage SPI (custom user providers)
- Attribute mappers (Keycloak-specific configuration)
- Group/role management API (non-standard)

**Authentication Features**:
- Required actions (password reset, OTP setup, verify email)
- Authentication flows (custom flow configuration)
- Execution chains (conditional authentication)
- Authenticator SPIs (extensibility framework)

**Session Management**:
- Session monitoring via Admin Console
- Active session management API
- Session limits and timeouts (admin configuration)
- Offline token management

**MFA/Security**:
- OTP configuration (TOTP/HOTP)
- WebAuthn support (FIDO2)
- X.509 client certificate authentication
- Kerberos/SPNEGO integration
- Custom authenticator implementations

**Advanced Features**:
- Identity brokering (delegate to external IdPs)
- Social login providers (pre-configured integrations)
- Client policies and profiles
- Authorization services (UMA 2.0, fine-grained permissions)
- Custom themes and UI extensions
- Event listeners and webhooks
- Realm-specific configuration

**Extensibility Model**:
- Service Provider Interfaces (SPIs)
- Custom providers (Java implementation required)
- Event listener SPI
- Protocol mapper SPI
- Authentication SPI

## Configuration Approach

**Standard Configuration**:
- OIDC discovery enables automatic client configuration
- Standard OAuth/OIDC client libraries work without modifications
- Redirect URIs and client credentials are portable concepts

**Keycloak-Specific Configuration**:
- Realm concept (multi-tenancy within single instance)
- Client scopes and protocol mappers
- Composite roles and role mappings
- Authentication flow bindings
- Required actions configuration
- Identity provider mappers

## Migration Evidence

### Migrations TO Keycloak

**Auth0 → Keycloak**:
- User migration: Export users from Auth0, import to Keycloak (custom tooling required)
- Password hash compatibility: Auth0's bcrypt vs. Keycloak's pbkdf2-sha256 (27,500 iterations)
- Migration complexity: Significant effort due to proprietary features
- Estimated effort: **80-120 hours** (per community reports)
- Pain points: Custom Auth0 rules/actions have no direct equivalent

**Okta → Keycloak**:
- Similar challenges to Auth0 migration
- SCIM provisioning needs replacement with Keycloak's user federation
- Social login re-configuration required
- Estimated effort: **60-100 hours**

### Migrations FROM Keycloak

**Keycloak → Auth0**:
- User export: Keycloak REST API or database export
- Password migration: Custom hash algorithm configuration in Auth0
- Configuration rebuild: Clients, roles, scopes need manual recreation
- Loss of features: Authorization services, user federation
- Estimated effort: **80-150 hours**

**Keycloak → Other Self-Hosted**:
- To Authentik/Ory: **40-80 hours** (similar architecture, but config rebuild)
- Standard OAuth/OIDC clients: **2-5 hours** (just endpoint changes)

## Known Migration Paths

### Community Documentation

**Migration Guides Available**:
- Keycloak provides export/import functionality for realm configurations
- User database export via Admin REST API
- Social provider re-configuration documented
- Identity broker migration requires manual setup

**Third-Party Tools**:
- Keycloak user migration scripts (community-developed)
- Terraform providers for infrastructure-as-code migrations
- Migration consulting services from Red Hat

### Migration Complexity Factors

**Simple Migration** (application uses ONLY standard OAuth/OIDC):
- Update OIDC discovery URL
- Update client ID/secret
- Verify redirect URIs
- **Time: 2-5 hours**

**Complex Migration** (application uses Keycloak-specific features):
- User data migration with password hash conversion
- Rebuild authentication flows
- Reconfigure MFA methods
- Re-implement custom extensions/SPIs
- Social login provider reconfiguration
- Authorization policies reimplementation
- **Time: 80-150 hours**

## Portability Assessment

### Portable Features (Config-Only Migration)
- OAuth 2.0 / OIDC flows: ✅ Fully portable
- Token formats: ✅ Standard JWT
- Discovery endpoint: ✅ Standard OIDC Discovery
- Core authentication: ✅ Works with any standard client

### Non-Portable Features (Require Reimplementation)
- User management API: ❌ Proprietary REST API
- Session management: ❌ Keycloak-specific
- MFA configuration: ❌ Provider-specific
- Custom authentication flows: ❌ Keycloak execution chains
- Authorization services: ❌ UMA 2.0 implementation proprietary
- User federation: ❌ LDAP/Kerberos integration proprietary
- Identity brokering: ❌ Configuration non-portable

## Lock-In Risk Analysis

**LOW LOCK-IN** (if using):
- Standard OAuth/OIDC flows only
- External user management system
- Minimal custom configuration

**MEDIUM LOCK-IN** (if using):
- Keycloak user database
- Social login integrations
- Basic MFA
- Standard role-based access control

**HIGH LOCK-IN** (if using):
- Custom authentication flows
- Authorization services (fine-grained permissions)
- User federation with LDAP/Kerberos
- Custom SPIs or extensions
- Identity brokering with complex mappings
- Event listeners and custom actions

## Feature Comparison Context

**Keycloak's Strengths**:
- Most comprehensive feature set among open-source options
- Enterprise-grade scalability and clustering
- Strong community and Red Hat support
- Extensive protocol support (SAML, LDAP, Kerberos)

**Keycloak's Weaknesses**:
- Heavy memory footprint (JVM-based)
- Steeper learning curve
- Customization requires Java development
- No official managed service

## Recommendations

**Choose Keycloak if**:
- Need comprehensive self-hosted IAM solution
- Require enterprise features (SAML, LDAP federation, SSO)
- Want strong community and commercial support
- Have infrastructure to run Java applications

**Avoid Keycloak if**:
- Need lightweight solution
- Want managed service (no self-hosting)
- Require frequent custom code changes
- Prioritize portability above features

**Portability Strategy**:
- Keep authentication logic in applications minimal
- Use standard OAuth/OIDC flows exclusively
- Avoid deep integration with Keycloak-specific features
- Use SCIM for user provisioning where possible
- Document all custom configurations for migration planning
