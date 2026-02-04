# OAuth 2.0 & OpenID Connect - Standard Overview

## Governance Bodies

### OAuth 2.0
- **Governance**: Internet Engineering Task Force (IETF)
- **Primary Specification**: RFC 6749 - The OAuth 2.0 Authorization Framework
- **Status**: Internet Standards Track (highest IETF maturity level)
- **Publication Date**: October 2012
- **Current Evolution**: OAuth 2.1 (draft consolidation), RFC 9700 (security best practices, 2024)

### OpenID Connect (OIDC)
- **Governance**: OpenID Foundation
- **Primary Specification**: OpenID Connect Core 1.0 (Final)
- **Status**: Final specification, also published as ISO/IEC Publicly Available Specification (PAS)
- **Publication Date**: February 2014
- **ISO/IEC Status**: 9 OIDC specifications published as ISO/IEC standards (2024)

## Maturity Assessment

### OAuth 2.0
- **Age**: 13 years (RFC 6749 from 2012)
- **Version Status**: Stable, with numerous extension RFCs (PKCE RFC 7636, Native Apps RFC 8252, etc.)
- **Maintenance**: Active IETF OAuth Working Group
- **Security**: Ongoing updates (RFC 9700 in 2024, OAuth 2.1 draft incorporating best practices)

### OpenID Connect
- **Age**: 11 years (Final spec from 2014)
- **Version Status**: Core 1.0 Final (incorporating errata set 2)
- **Maintenance**: Active OpenID Foundation working groups
- **Certification**: OpenID Certification program for conformance testing

## Backend Count Analysis

### Certified OpenID Connect Implementations
**Total Certified: 64 unique implementations**

### Self-Hosted Open Source Options (12+)
1. **Keycloak** (Red Hat) - Full IAM solution
2. **Ory Hydra** - OpenID Certified, lightweight OAuth2 server
3. **Authentik** - Modern Python-based IdP
4. **IdentityServer** (.NET) - OpenID Certified
5. **Gluu Server** - Enterprise open source
6. **WSO2 Identity Server** - Enterprise IAM
7. **Gravitee.io Access Management**
8. **Authelia** - Authentication/authorization server
9. **Open Liberty** (IBM open source)
10. **node-oidc-provider** (Node.js) - OpenID Certified
11. **Dex** - Kubernetes-focused OIDC provider
12. **FusionAuth** - Developer-focused auth platform

### Managed Commercial Services (20+)
1. **Auth0** (Okta) - OpenID Certified
2. **Okta** - OpenID Certified
3. **Microsoft Entra ID** (Azure AD) - OpenID Certified
4. **Google Identity Platform** - OpenID Certified
5. **AWS Cognito**
6. **Ping Identity (PingFederate)** - OpenID Certified
7. **ForgeRock** - OpenID Certified
8. **IBM Security Verify** - OpenID Certified
9. **Cloudentity** - OpenID Certified with FAPI support
10. **Curity Identity Server**
11. **OneLogin**
12. **SAP Customer Identity**
13. **Descope**
14. **Akamai Identity Cloud**
15. **Connect2id** - Certified enterprise OIDC/OAuth server
16. **MonoCloud**
17. **PlusAuth**
18. **LoginRadius**
19. **Stytch**
20. **Clerk**

### Cloud Provider Native Support
- **Google** (Google Sign-In, Workspace)
- **GitHub** (OAuth Apps, GitHub Apps)
- **Microsoft** (Azure AD, Microsoft Account)
- **Apple** (Sign in with Apple)
- **Facebook/Meta** (Facebook Login)
- **Amazon** (Login with Amazon, Cognito)

### Backend Count Verdict
**PASS: 64+ certified implementations, 30+ major providers**
- Self-hosted options: 12+ viable open source solutions
- Managed services: 20+ commercial providers
- Cloud providers: All major platforms support OAuth/OIDC
- **Threshold exceeded**: 5+ required, 64+ certified implementations found

## Adoption Indicators

### Enterprise Ubiquity
- Used by millions of developers worldwide (OpenID Foundation claim)
- Deployed in billions of applications globally
- Standard authentication for major platforms: Google, Microsoft, Apple, GitHub, Facebook

### Developer Ecosystem
- Every major programming language has certified client libraries
- Default auth method for modern API security
- Native support in frameworks: Spring Security, ASP.NET Core, Django, Rails, Next.js

### Industry Recognition
- ISO/IEC standardization (rare for web protocols)
- NIST Digital Identity Guidelines reference OIDC
- Financial-grade API (FAPI) profiles for banking/finance
- Government adoption (gov.uk, US federal agencies)

## Timeline Summary

- **2012**: OAuth 2.0 RFC 6749 published (IETF)
- **2014**: OpenID Connect Core 1.0 Final published
- **2015-2020**: Massive enterprise adoption, extension RFCs
- **2024**: OIDC published as ISO/IEC standard, RFC 9700 security updates
- **2025**: OAuth 2.1 draft consolidation (ongoing), 64+ certified implementations
