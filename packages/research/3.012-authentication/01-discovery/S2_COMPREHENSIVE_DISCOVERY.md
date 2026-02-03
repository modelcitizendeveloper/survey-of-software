# S2: COMPREHENSIVE DISCOVERY - Authentication & Authorization Services
## Experiment 3.012: Authentication Service Provider Ecosystem Analysis

**Discovery Date**: 2025-10-07
**Scope**: Exhaustive provider analysis across 16 major authentication and authorization platforms
**Focus**: Security features, protocol support, pricing models, compliance certifications, integration complexity, session management, passwordless authentication, enterprise capabilities

---

## 1. PROVIDER OVERVIEW MATRIX

### 1.1 Provider Classification

| Provider | Type | Primary Market | Business Model | Founded |
|----------|------|----------------|----------------|---------|
| **Auth0** | Identity Platform | Enterprise, Developer-First | MAU-based pricing | 2013 (Okta-owned 2021) |
| **Clerk** | Auth-as-a-Service | Modern Developers, SaaS | MAU-based pricing | 2021 |
| **Supabase Auth** | Open-Source Auth | Developers, Full-Stack | MAU-based + self-host | 2020 |
| **Firebase Auth** | BaaS Auth Module | Mobile/Web Apps, Google Ecosystem | MAU-based (generous free tier) | 2011 (Google-owned 2014) |
| **AWS Cognito** | Cloud Identity Service | AWS Ecosystem, Enterprise | MAU-based (ultra-low cost) | 2014 |
| **Ory** | Open-Source Identity | Self-Hosted, Privacy-First | Open-source + managed cloud | 2015 |
| **WorkOS** | Enterprise Auth | B2B SaaS, SSO-First | MAU-based + SSO pricing | 2019 |
| **Stytch** | Passwordless Auth | Modern Apps, Consumer Auth | MAU-based + API calls | 2020 |
| **Magic** | Passwordless Auth | Web3, Consumer Apps | MAU-based pricing | 2018 |
| **Hanko** | Passwordless Auth | Open-Source, Passkey-First | Open-source + cloud | 2022 |
| **Keycloak** | Open-Source IAM | Enterprise, Self-Hosted | Open-source (Red Hat) | 2014 |
| **FusionAuth** | Auth Platform | Developers, Self-Host Option | Freemium + MAU/hosting | 2018 |
| **SuperTokens** | Open-Source Auth | Developers, Self-Host First | Open-source + managed hosting | 2020 |
| **Descope** | No-Code Auth | Developers, Drag-Drop Flows | MAU-based pricing | 2022 |
| **Passage** | Passkey Auth | Developers, Biometric-First | MAU-based pricing | 2022 (1Password-acquired 2023) |
| **Propel Auth** | B2B Auth | SaaS Companies, Org Management | MAU-based pricing | 2022 |

### 1.2 Market Position & Scale

| Provider | Active Customers (Claimed) | MAU Supported | Geographic Reach | Infrastructure |
|----------|---------------------------|---------------|------------------|----------------|
| **Auth0** | 30K+ (pre-Okta) | Billions | Global (Okta Cloud) | Multi-region (US, EU, AU, JP) |
| **Clerk** | 10K+ | Millions | Global | Multi-region (US, EU) |
| **Supabase Auth** | 100K+ projects | Millions | Global | Multi-region (11 regions) |
| **Firebase Auth** | Millions (Google) | Billions (Google scale) | Global | Google Cloud (multi-region) |
| **AWS Cognito** | Unknown (AWS-wide) | Billions (AWS scale) | Global | All AWS regions (33+) |
| **Ory** | 15K+ (OSS) | Self-hosted varies | Global | Cloud: EU, US |
| **WorkOS** | 500+ B2B companies | Millions | Global | US-primary |
| **Stytch** | Growing rapidly | Millions | Global | US, EU |
| **Magic** | Thousands | Millions | Global | Multi-region |
| **Hanko** | Growing (OSS) | Self-hosted | Global | EU-based cloud |
| **Keycloak** | Hundreds of thousands (OSS) | Self-hosted | Global | Self-managed |
| **FusionAuth** | 10K+ | Millions | Global | Self-host or cloud |
| **SuperTokens** | Growing (OSS) | Self-hosted + cloud | Global | Self-host primary |
| **Descope** | Early stage | Growing | Global | Multi-region |
| **Passage** | Growing (1Password) | Millions | Global | 1Password infrastructure |
| **Propel Auth** | Early stage B2B | Growing | Global | US-primary |

---

## 2. FEATURE COMPARISON MATRIX

### 2.1 Core Authentication Methods

| Feature | Auth0 | Clerk | Supabase | Firebase | Cognito | Ory | WorkOS | Stytch | Magic | Hanko | Keycloak | FusionAuth | SuperTokens | Descope | Passage | PropelAuth |
|---------|-------|-------|----------|----------|---------|-----|--------|--------|-------|-------|----------|------------|-------------|---------|---------|------------|
| **Email/Password** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Passwordless (Magic Link)** | Yes | Yes | Yes | Yes | No | Yes | Limited | Yes | Yes | Yes | Limited | Yes | Yes | Yes | No | Yes |
| **Passwordless (OTP/SMS)** | Yes | Yes | Yes | Yes | Yes | Yes | Limited | Yes | Yes | Yes | Yes | Yes | Yes | Yes | No | Yes |
| **WebAuthn/Passkeys** | Yes | Yes | Limited | No (2025) | No | Yes | No | Yes | No | Yes (Core) | Yes | Yes | Limited | Yes | Yes (Core) | Limited |
| **Biometric** | Via WebAuthn | Via WebAuthn | Limited | Yes (mobile) | No | Via WebAuthn | No | Yes | No | Yes | Via WebAuthn | Via WebAuthn | Limited | Yes | Yes | Limited |
| **Social Login (OAuth)** | 30+ providers | 20+ | 10+ | 20+ | 10+ | 5+ | 10+ | 15+ | 5+ | Limited | All major | 20+ | 10+ | 20+ | No | 15+ |
| **Enterprise SSO (SAML)** | Yes | Yes (paid) | No | No | Yes | Yes | Yes (Core) | Yes (paid) | No | No | Yes | Yes | Limited | Yes | No | Yes |
| **Enterprise SSO (OIDC)** | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Limited | Limited | Yes | Yes | Yes | Yes | Limited | Yes |
| **Multi-Factor Auth (MFA)** | Yes (TOTP, SMS, Push) | Yes (TOTP, SMS) | Yes (TOTP) | Yes | Yes (SMS, TOTP) | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Limited | Yes |
| **Adaptive/Risk-Based Auth** | Yes (Enterprise) | Yes | No | Yes (Identity Platform) | Yes (Advanced Security) | Limited | Limited | Yes | No | No | Limited | Limited | No | Yes | No | Limited |
| **Anonymous Users** | Yes | No | Yes | Yes | Yes | No | No | Limited | No | No | Yes | Yes | Yes | Limited | No | No |

### 2.2 Authorization & Access Control

| Feature | Auth0 | Clerk | Supabase | Firebase | Cognito | Ory | WorkOS | Stytch | Magic | Hanko | Keycloak | FusionAuth | SuperTokens | Descope | Passage | PropelAuth |
|---------|-------|-------|----------|----------|---------|-----|--------|--------|-------|-------|----------|------------|-------------|---------|---------|------------|
| **Role-Based Access Control (RBAC)** | Yes | Yes | Via policies | Via custom claims | Via groups | Yes | Yes | Yes | Via metadata | No | Yes | Yes | Yes (Sessions) | Yes | No | Yes (Core) |
| **Attribute-Based Access Control (ABAC)** | Yes (Rules) | Limited | Via RLS | Via custom claims | Limited | Yes (Keto) | Limited | Limited | No | No | Yes | Yes | Limited | Yes | No | Limited |
| **Permission Management** | Yes (Fine-grained) | Yes | Via RLS | Manual | Via policies | Yes (Keto) | Via SAML attrs | Yes | Via metadata | No | Yes | Yes | Via sessions | Yes | No | Yes |
| **Organizations/Tenancy** | Yes | Yes (Core) | Via RLS | Via custom setup | Via groups | Manual | Yes (Core) | Yes | Via metadata | No | Yes (Realms) | Yes (Tenants) | Yes | Yes | No | Yes (Core) |
| **Team Management** | Yes | Yes | Manual | Manual | Via groups | Manual | Yes | Yes | Manual | No | Yes | Yes | Manual | Yes | No | Yes |
| **Scopes/Claims** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Limited | Yes | Yes | Yes | Yes | Limited | Yes |

### 2.3 Session Management

| Feature | Auth0 | Clerk | Supabase | Firebase | Cognito | Ory | WorkOS | Stytch | Magic | Hanko | Keycloak | FusionAuth | SuperTokens | Descope | Passage | PropelAuth |
|---------|-------|-------|----------|----------|---------|-----|--------|--------|-------|-------|----------|------------|-------------|---------|---------|------------|
| **Session Storage** | Cookie or Token | Cookie (HTTP-only) | JWT | Token (ID/Refresh) | JWT | Cookie or Token | Token | Cookie + Token | DID Token | JWT | Cookie or Token | JWT/Refresh | Cookie (HTTP-only) | Cookie/Token | Token | Cookie/Token |
| **Session Lifetime Control** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Refresh Tokens** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes (Rotating) | Yes | Yes | Yes |
| **Token Rotation** | Yes | Yes | Yes | Yes | Yes | Yes | Limited | Yes | Yes | Limited | Yes | Yes | Yes (Auto) | Yes | Limited | Yes |
| **Multi-Device Sessions** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Session Revocation** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Concurrent Session Limits** | Yes (Enterprise) | Yes | Manual | Manual | Manual | Manual | Limited | Yes | No | Limited | Yes | Yes | Manual | Yes | No | Yes |
| **Activity Tracking** | Yes | Yes | Yes | Limited | Yes | Limited | Limited | Yes | Limited | Limited | Yes | Yes | Yes | Yes | Limited | Yes |

### 2.4 User Management

| Feature | Auth0 | Clerk | Supabase | Firebase | Cognito | Ory | WorkOS | Stytch | Magic | Hanko | Keycloak | FusionAuth | SuperTokens | Descope | Passage | PropelAuth |
|---------|-------|-------|----------|----------|---------|-----|--------|--------|-------|-------|----------|------------|-------------|---------|---------|------------|
| **User Database** | Managed | Managed | PostgreSQL | Managed | Managed | PostgreSQL | Managed | Managed | Managed | PostgreSQL | Managed | Managed | Managed/Own DB | Managed | Managed | Managed |
| **Custom User Metadata** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Limited | Yes |
| **User Profile Management** | Yes | Yes (UI) | Yes | Yes | Yes | Limited | Yes | Yes | Limited | Yes | Yes (UI) | Yes (UI) | Yes | Yes (UI) | Limited | Yes (UI) |
| **Email Verification** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | No (passwordless) | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Phone Verification** | Yes | Yes | Limited | Yes | Yes | Limited | Limited | Yes | Yes | Limited | Yes | Yes | Limited | Yes | No | Yes |
| **Account Linking** | Yes | Yes | Yes | Yes | No | Yes | Limited | Yes | No | Limited | Yes | Yes | Yes | Yes | Limited | Yes |
| **User Import/Export** | Yes | Yes | Yes (SQL) | Yes | Yes (CSV) | Yes (SQL) | Yes | Yes | Limited | Yes (SQL) | Yes | Yes | Yes (SQL) | Yes | Limited | Yes |
| **User Deactivation/Deletion** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Bulk Operations** | Yes | Yes | Via SQL | Via Admin SDK | Yes | Via SQL | Limited | Yes | No | Via SQL | Yes | Yes | Via SQL | Yes | No | Yes |

### 2.5 Security Features

| Feature | Auth0 | Clerk | Supabase | Firebase | Cognito | Ory | WorkOS | Stytch | Magic | Hanko | Keycloak | FusionAuth | SuperTokens | Descope | Passage | PropelAuth |
|---------|-------|-------|----------|----------|---------|-----|--------|--------|-------|-------|----------|------------|-------------|---------|---------|------------|
| **Brute Force Protection** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Bot Detection** | Yes (Captcha) | Yes (Captcha) | Manual | Yes (reCAPTCHA) | Yes (WAF) | Manual | Limited | Yes | Limited | Manual | Yes | Yes | Manual | Yes | Limited | Yes |
| **Anomaly Detection** | Yes (Enterprise) | Yes | No | Yes (Identity Platform) | Yes (Advanced Security) | No | Limited | Yes | No | No | Limited | Limited | No | Yes | No | Limited |
| **Breached Password Detection** | Yes | Yes | No | No | No | No | No | Yes | No | No | Limited | No | No | Yes | No | No |
| **IP Allowlist/Blocklist** | Yes | Yes | Manual | Yes | Yes | Manual | Limited | Yes | No | Manual | Yes | Yes | Manual | Yes | No | Yes |
| **Rate Limiting** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Audit Logs** | Yes | Yes | Yes | Yes (Firestore) | Yes (CloudTrail) | Limited | Yes | Yes | Limited | Limited | Yes | Yes | Limited | Yes | Limited | Yes |
| **Encryption at Rest** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Encryption in Transit** | Yes (TLS 1.2+) | Yes (TLS 1.3) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |

---

## 3. PRICING MODELS DEEP-DIVE

### 3.1 Free Tiers (2025)

| Provider | Free MAU Limit | Additional Features | Limitations |
|----------|----------------|---------------------|-------------|
| **Auth0** | 7,500 MAU | Unlimited logins, Social+DB connections, MFA | No enterprise SSO, limited customization |
| **Clerk** | 10,000 MAU | Social login, organizations, webhooks | No enterprise SSO, no custom domains on free |
| **Supabase Auth** | 50,000 MAU | PostgreSQL database, Row-Level Security, social login | Self-service, community support only |
| **Firebase Auth** | Unlimited (with usage limits) | Phone auth: 10K/month, Social providers, Anonymous | Limited to Firebase ecosystem |
| **AWS Cognito** | 50,000 MAU | Full features, advanced security pay-as-go | Requires AWS expertise |
| **Ory** | Unlimited (self-hosted) | Full features, open-source | Self-managed infrastructure |
| **WorkOS** | Free (SSO connections paid) | Basic auth features | SSO requires paid plan ($125/connection) |
| **Stytch** | 5,000 MAU (25 free for testing) | Passwordless, magic links, OTP | Limited social providers on free |
| **Magic** | None (Paid only in 2025) | N/A | Starts at $199/mo |
| **Hanko** | Unlimited (self-hosted) | Passkey-first, open-source | Self-managed |
| **Keycloak** | Unlimited (self-hosted) | Full IAM features | Self-managed, complex setup |
| **FusionAuth** | Unlimited (community) | Full auth features, self-hosted | No hosting, no support |
| **SuperTokens** | Unlimited (self-hosted) | Full features, 5K MAU free on managed | Self-host or small managed |
| **Descope** | 7,500 MAU | Drag-drop flows, social login | Limited customization |
| **Passage** | 1,000 MAU | Passkey authentication | Passkey-only (limited methods) |
| **PropelAuth** | 1,000 MAU | B2B features, organizations | Small free tier |

### 3.2 Standard Pricing Tiers (2025)

#### **Per-MAU Pricing Models**

| MAU Tier | Auth0 | Clerk | Supabase | Firebase | Cognito | Stytch | Descope | PropelAuth |
|----------|-------|-------|----------|----------|---------|--------|---------|------------|
| **Up to 1K MAU** | Free (up to 7.5K) | Free (up to 10K) | Free (up to 50K) | Free | Free (up to 50K) | Free (up to 5K) | Free (up to 7.5K) | $49/mo (up to 1K) |
| **10K MAU** | $228/mo (Essentials) | Free | Free | Free | Free | $249/mo | $99/mo | $249/mo |
| **25K MAU** | $570/mo | $25/mo | Free | Free | Free | $499/mo | $249/mo | $499/mo |
| **50K MAU** | $1,140/mo | $75/mo | Free | ~$50 (Phone auth) | Free | $999/mo | $499/mo | $999/mo |
| **100K MAU** | $2,280/mo | $199/mo | $25/mo (Pro) | ~$100 | $550/mo (0.0055/MAU) | $1,749/mo | $999/mo | Custom |
| **500K MAU** | Custom | $799/mo | $25/mo + scale | ~$500 | $2,750/mo | Custom | Custom | Custom |
| **1M MAU** | Custom | $1,499/mo | ~$100/mo | ~$1,000 | $5,500/mo | Custom | Custom | Custom |

**Notes**:
- **Auth0**: $228/mo Essentials (up to 500 MAU + additional MAU), Custom for enterprise
- **Clerk**: Volume-based with generous free tier, $25/mo starts after 10K MAU
- **Supabase**: Database-focused pricing, auth is included with compute
- **Firebase**: Phone auth charged separately (~$0.01/verification after 10K), otherwise mostly free
- **Cognito**: Most affordable at scale ($0.0055/MAU after 50K free)
- **Stytch**: Premium pricing for passwordless focus
- **Descope**: Competitive mid-market pricing
- **PropelAuth**: B2B-focused with organization features

#### **Flat-Rate & Self-Hosted Options**

| Provider | Hosting Model | Pricing | Support Tier |
|----------|---------------|---------|--------------|
| **Ory** | Open-source (free) + Cloud | Cloud: $29/mo (dev) → Custom (enterprise) | Community (OSS), Paid (Cloud) |
| **Keycloak** | Self-hosted (free) | Free (no official cloud) | Community or Red Hat SSO (enterprise support) |
| **FusionAuth** | Self-host or cloud | Free (community), Cloud starts ~$75/mo, Enterprise custom | Paid support plans available |
| **SuperTokens** | Self-host or managed | Free (self-host), Managed: $49/mo (5K MAU) → Custom | Community + paid support |
| **Hanko** | Self-host or cloud | Free (OSS), Cloud: Custom pricing | Community or enterprise support |

### 3.3 Add-on Costs & Hidden Fees

| Provider | Enterprise SSO | Custom Domains | Advanced Security | Support Upgrades | API Rate Limits |
|----------|----------------|----------------|-------------------|------------------|-----------------|
| **Auth0** | Enterprise plan | Included (paid plans) | Enterprise plan ($$$) | Included in tiers | Based on plan |
| **Clerk** | $99/mo per connection | $20/mo | Included | Email + Slack (all tiers) | Based on plan (generous) |
| **Supabase** | Not available | Included (paid plans) | Manual setup | Email + Discord (community), Priority (Enterprise) | Configurable |
| **Firebase** | Not available | Included | Identity Platform ($$$) | Google Cloud Support ($$$) | Generous (Firebase limits) |
| **Cognito** | Included | Included | $0.05/MAU (Advanced Security) | AWS Support plans ($29-15K+/mo) | AWS account limits |
| **Ory** | Included (OSS) | Self-managed | Included | Community or paid support | Self-managed |
| **WorkOS** | $125/connection/mo | Custom | Included | Email support | Based on plan |
| **Stytch** | $99/connection/mo | Included (Growth+) | Included | Email + Slack | Based on plan |
| **Magic** | Not available | Included | Included | Email support | Based on plan |
| **Hanko** | Not available (OSS) | Self-managed | Included | Community or enterprise | Self-managed |
| **Keycloak** | Included | Self-managed | Included | Community or Red Hat | Self-managed |
| **FusionAuth** | Included | Self-managed | Included | Paid support tiers | Based on hosting |
| **SuperTokens** | Included | Self-managed or included | Included | Community or paid | Based on plan |
| **Descope** | Included (higher tiers) | Included | Included | Email + Slack | Based on plan |
| **Passage** | Not available | Included | Included (passkeys) | 1Password support | Based on plan |
| **PropelAuth** | Included | Included | Included | Email + Slack | Based on plan |

### 3.4 Total Cost of Ownership (TCO) Analysis

**Scenario: 100K Active Users**

| Provider | Base Monthly Cost | SSO (5 connections) | Custom Domain | Support | Total/Month | Total/Year |
|----------|------------------|---------------------|---------------|---------|-------------|------------|
| **AWS Cognito** | $550 | Included | Included | $0 (DIY) | $550 | $6,600 |
| **Supabase** | $25 (Pro) | N/A | Included | Email | $25 | $300 |
| **Clerk** | $199 | $495 ($99 x 5) | $20 | Included | $714 | $8,568 |
| **Auth0** | $2,280 (Essentials) | Enterprise only | Included | Included | $2,280+ | $27,360+ |
| **Stytch** | $1,749 | $495 | Included | Included | $2,244 | $26,928 |
| **FusionAuth** | ~$200 (cloud hosting) | Included | Included | $500/mo (support) | $700 | $8,400 |
| **Keycloak** | $0 (self-host) | Included | Included | DIY or Red Hat | $0-2,000 | $0-24,000 |
| **SuperTokens** | ~$100 (managed) | Included | Included | Community | $100 | $1,200 |
| **Descope** | $999 | Included (higher tier) | Included | Included | $999 | $11,988 |
| **PropelAuth** | Custom (~$1,500) | Included | Included | Included | ~$1,500 | ~$18,000 |

**Key TCO Factors**:
1. **Developer time**: Self-hosted (Keycloak, Ory) = lowest cost, highest setup/maintenance
2. **Scale economics**: AWS Cognito best at massive scale (>500K MAU)
3. **Feature completeness**: Auth0/Clerk/WorkOS offer most out-of-box for B2B
4. **SSO tax**: Enterprise SSO adds $500-1,500/month (Auth0 requires Enterprise tier)
5. **Support quality**: Managed services (Clerk, Stytch, Auth0) provide better developer experience

**Break-Even Analysis**:
- **Under 50K MAU**: Supabase, Firebase, or AWS Cognito (free tiers)
- **50K-200K MAU**: Clerk or AWS Cognito (best price/features)
- **200K-1M MAU**: AWS Cognito or negotiate Auth0/Clerk
- **1M+ MAU**: AWS Cognito or enterprise Auth0/Okta deal
- **Enterprise SSO required**: WorkOS, Clerk, or Auth0 (factor $500-2K/mo SSO tax)

---

## 4. COMPLIANCE & CERTIFICATION MATRIX

### 4.1 Security & Data Protection Standards

| Provider | SOC 2 Type II | ISO 27001 | GDPR Compliant | HIPAA Compliant | Additional Certifications |
|----------|---------------|-----------|----------------|-----------------|---------------------------|
| **Auth0** | Yes | Yes | Yes | Yes (BAA available, Enterprise) | PCI DSS, Privacy Shield (legacy), CSA STAR |
| **Clerk** | Yes | In progress (2025) | Yes | No | Regular pentests, bug bounty |
| **Supabase** | Yes | No | Yes | No | Regular security audits |
| **Firebase** | Yes (Google) | Yes (Google) | Yes | Yes (Google Cloud BAA) | Full Google Cloud compliance suite |
| **AWS Cognito** | Yes (AWS) | Yes (AWS) | Yes | Yes (AWS BAA) | ISO 9001, ISO 27017, ISO 27018, FedRAMP, PCI DSS Level 1 |
| **Ory** | Yes (Cloud) | No | Yes (EU-first) | No | GDPR-native design, open-source auditable |
| **WorkOS** | Yes | In progress | Yes | No | Regular pentests |
| **Stytch** | Yes | In progress | Yes | No | Regular security audits |
| **Magic** | Yes | No | Yes | No | Security audits |
| **Hanko** | In progress | No | Yes (EU-based) | No | Open-source, auditable |
| **Keycloak** | N/A (OSS) | N/A (self-managed) | Yes (if configured) | Yes (if configured) | Red Hat SSO has certifications |
| **FusionAuth** | Yes (Cloud) | No | Yes | No | Security audits |
| **SuperTokens** | In progress | No | Yes | No | Open-source auditable |
| **Descope** | In progress | In progress | Yes | No | Regular pentests |
| **Passage** | Yes (1Password) | Yes (1Password) | Yes | No | 1Password security heritage |
| **PropelAuth** | In progress | No | Yes | No | Security audits |

### 4.2 Data Residency & Privacy

| Provider | Data Centers | EU Data Residency | Custom Data Residency | Data Retention | Right to Delete |
|----------|--------------|-------------------|----------------------|----------------|-----------------|
| **Auth0** | Global (Okta) | Yes (EU region) | Yes (AU, JP, EU, US) | Configurable | Yes |
| **Clerk** | US, EU | Yes (EU region option) | Planned | 90 days logs (default) | Yes |
| **Supabase** | 11 regions | Yes (EU regions) | Yes (11 regions) | Configurable | Yes |
| **Firebase** | Global (Google) | Yes (EU regions) | Multi-region options | Configurable | Yes |
| **AWS Cognito** | All AWS regions | Yes (6+ EU regions) | Yes (33+ regions) | Configurable | Yes |
| **Ory** | EU, US (Cloud) | Yes (EU primary) | Self-host anywhere | Configurable | Yes |
| **WorkOS** | US-primary | Planned | Limited | 90 days logs | Yes |
| **Stytch** | US, EU | Yes (EU region) | Limited | 90 days logs | Yes |
| **Magic** | Global | Limited info | Limited | Configurable | Yes |
| **Hanko** | EU (Cloud) | Yes (EU-based) | Self-host anywhere | Configurable | Yes |
| **Keycloak** | Self-hosted | Self-managed | Full control | Self-managed | Self-managed |
| **FusionAuth** | Self-hosted or cloud | Cloud: US | Self-host anywhere | Self-managed | Yes |
| **SuperTokens** | Self-hosted primary | Self-managed | Self-host anywhere | Self-managed | Yes |
| **Descope** | Global | Yes | Limited | Configurable | Yes |
| **Passage** | 1Password infra | Yes | Via 1Password | Configurable | Yes |
| **PropelAuth** | US-primary | Planned | Limited | 90 days logs | Yes |

### 4.3 Authentication Protocol Support

| Protocol | Auth0 | Clerk | Supabase | Firebase | Cognito | Ory | WorkOS | Stytch | Magic | Hanko | Keycloak | FusionAuth | SuperTokens | Descope | Passage | PropelAuth |
|----------|-------|-------|----------|----------|---------|-----|--------|--------|-------|-------|----------|------------|-------------|---------|---------|------------|
| **OAuth 2.0** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **OpenID Connect (OIDC)** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Limited | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **SAML 2.0** | Yes | Yes (paid) | No | No | Yes | Yes | Yes | Yes | No | No | Yes | Yes | No | Yes | No | Yes |
| **JWT** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **WebAuthn/FIDO2** | Yes | Yes | Limited | No | No | Yes | No | Yes | No | Yes | Yes | Yes | Limited | Yes | Yes | Limited |
| **LDAP** | Yes (Enterprise) | No | No | No | No | Yes | No | No | No | No | Yes | Yes | No | No | No | No |
| **Kerberos** | Limited | No | No | No | No | No | No | No | No | No | Yes | Limited | No | No | No | No |
| **WS-Federation** | Yes | No | No | No | No | No | No | No | No | No | Yes | Limited | No | No | No | No |

### 4.4 Industry-Specific Compliance

**Best for Healthcare (HIPAA)**:
1. **AWS Cognito**: Full AWS HIPAA compliance, BAA available
2. **Firebase/Google Cloud**: Google Cloud HIPAA compliance, BAA available
3. **Auth0**: Enterprise tier with BAA

**Best for Financial Services (PCI DSS)**:
1. **AWS Cognito**: PCI DSS Level 1 via AWS
2. **Auth0**: PCI DSS certified
3. **Keycloak**: Self-managed compliance possible

**Best for EU/GDPR-First**:
1. **Ory**: EU-based, GDPR-native design
2. **Hanko**: EU-based, open-source
3. **Supabase**: EU region support, transparent data handling
4. **Keycloak**: Self-hosted EU compliance

**Best for Government (FedRAMP)**:
1. **AWS Cognito**: FedRAMP authorized via AWS GovCloud
2. **Auth0**: FedRAMP in progress (via Okta)

---

## 5. INTEGRATION PATTERNS & DEVELOPER EXPERIENCE

### 5.1 SDK & Framework Support

| Framework/Platform | Auth0 | Clerk | Supabase | Firebase | Cognito | Ory | WorkOS | Stytch | Keycloak | FusionAuth | SuperTokens |
|-------------------|-------|-------|----------|----------|---------|-----|--------|--------|----------|------------|-------------|
| **React** | Yes | Yes (hooks) | Yes | Yes | Yes (Amplify) | Yes | Yes | Yes | Manual | Yes | Yes (hooks) |
| **Next.js** | Yes | Yes (App Router) | Yes | Yes | Yes | Yes | Yes | Yes | Manual | Yes | Yes (App Router) |
| **Vue** | Yes | Limited | Yes | Yes | Yes | Limited | Limited | Limited | Manual | Yes | Yes |
| **Angular** | Yes | Limited | Yes | Yes | Yes | Limited | Limited | Limited | Manual | Yes | Limited |
| **Svelte** | Yes | Limited | Yes | Limited | Yes | Limited | Limited | Limited | Manual | Limited | Limited |
| **React Native** | Yes | Yes | Yes | Yes | Yes (Amplify) | Limited | Limited | Yes | Manual | Yes | Limited |
| **iOS (Swift)** | Yes | Yes | Yes | Yes | Yes | Limited | Limited | Yes | Manual | Yes | Limited |
| **Android (Kotlin)** | Yes | Yes | Yes | Yes | Yes | Limited | Limited | Yes | Manual | Yes | Limited |
| **Node.js** | Yes | Yes | Yes | Yes | Yes (SDK) | Yes | Yes | Yes | Yes | Yes | Yes |
| **Python** | Yes | Limited | Yes | Yes | Yes (boto3) | Yes | Yes | Yes | Yes | Yes | Yes |
| **Go** | Yes | Limited | Yes | Yes | Yes (SDK) | Yes | Yes | Yes | Yes | Yes | Yes |
| **Ruby** | Yes | Limited | Yes | Yes | Yes (SDK) | Limited | Limited | Limited | Yes | Yes | Limited |
| **PHP** | Yes | Limited | Yes | Yes | Yes (SDK) | Yes | Limited | Limited | Yes | Yes | Yes |
| **.NET/C#** | Yes | Limited | Yes | Yes | Yes (SDK) | Yes | Yes | Yes | Yes | Yes | Limited |

### 5.2 Pre-Built UI Components

| Provider | Login UI | Signup UI | Profile Management | Customization | Mobile UI |
|----------|----------|-----------|-------------------|---------------|-----------|
| **Auth0** | Universal Login | Yes | Yes | Good (CSS, templates) | Yes |
| **Clerk** | Prebuilt Components | Yes | Yes | Excellent (React components, theming) | Yes |
| **Supabase** | No (bring your own) | No | No | Full control (DIY) | DIY |
| **Firebase** | FirebaseUI | Yes | Limited | Limited (FirebaseUI themes) | Yes (FirebaseUI) |
| **AWS Cognito** | Hosted UI | Yes | Basic | Limited (CSS customization) | Manual |
| **Ory** | Account Experience | Yes | Yes | Good (templates, themes) | Limited |
| **WorkOS** | AuthKit (beta 2025) | Yes | Limited | Limited | Limited |
| **Stytch** | Pre-built UI | Yes | Limited | Good (React components) | Yes |
| **Magic** | Magic SDK UI | Minimal | No | Limited | Yes |
| **Hanko** | Hanko Elements | Yes | Limited | Good (web components) | Limited |
| **Keycloak** | Login themes | Yes | Yes | Good (themes, templates) | Manual |
| **FusionAuth** | Themed pages | Yes | Yes | Good (themes, templates) | Manual |
| **SuperTokens** | Pre-built UI | Yes | Limited | Good (React components) | Limited |
| **Descope** | Flow Builder (no-code) | Yes | Yes | Excellent (visual builder) | Yes |
| **Passage** | Pre-built UI | Yes | Limited | Limited (passkey-focused) | Yes |
| **PropelAuth** | Pre-built UI | Yes | Yes | Good (React components) | Limited |

**Best Pre-Built UI**:
1. **Clerk**: Best-in-class React components, themeable, production-ready
2. **Descope**: Visual flow builder, no-code customization
3. **Auth0**: Universal Login, highly customizable
4. **Keycloak**: Extensive theming system

**Best for Full Control (Headless)**:
1. **Supabase**: Completely headless, bring your own UI
2. **SuperTokens**: Headless option with pre-built fallback
3. **Ory**: Headless-first design

### 5.3 API Design & Documentation Quality

| Provider | API Type | Documentation Quality | Code Examples | Interactive Playground | OpenAPI/Swagger |
|----------|----------|----------------------|---------------|----------------------|-----------------|
| **Auth0** | REST | Excellent | Extensive (multi-language) | Yes (API Explorer) | Yes |
| **Clerk** | REST | Excellent | Extensive (React-focused) | Yes (docs playground) | Yes |
| **Supabase** | REST + Realtime | Excellent | Extensive (JS-focused) | Yes (SQL editor) | Yes |
| **Firebase** | REST + SDK-first | Good (Google standard) | Good (multi-platform) | Limited | Limited |
| **AWS Cognito** | AWS API | Good (AWS standard) | AWS SDK examples | AWS Console | AWS API docs |
| **Ory** | REST | Very Good | Good (Go, TS focused) | Yes (Ory Console) | Yes |
| **WorkOS** | REST | Very Good | Good (multi-language) | Limited | Yes |
| **Stytch** | REST | Very Good | Good (modern stack) | Limited | Yes |
| **Magic** | SDK-first | Good | Limited (JS-focused) | Limited | Limited |
| **Hanko** | REST + Elements | Good | Good (web components) | Limited | Yes |
| **Keycloak** | REST + Admin API | Fair (improving) | Limited (Java-focused) | No | Yes |
| **FusionAuth** | REST | Good | Good (multi-language) | Limited | Yes |
| **SuperTokens** | REST | Very Good | Excellent (recipe-based) | Limited | Yes |
| **Descope** | REST + SDK | Good | Good (modern) | Yes (Flow Builder) | Yes |
| **Passage** | REST | Good | Good (passkey-focused) | Limited | Yes |
| **PropelAuth** | REST | Good | Good (B2B-focused) | Limited | Yes |

### 5.4 Integration Complexity & Time-to-Production

| Provider | Setup Time (MVP) | Production-Ready | Customization Effort | Maintenance Burden | Migration Complexity |
|----------|------------------|------------------|----------------------|-------------------|---------------------|
| **Auth0** | 2-4 hours | 1-2 days | Medium-High | Low | Medium (vendor lock-in) |
| **Clerk** | 1-2 hours | 4-8 hours | Low-Medium | Very Low | Medium |
| **Supabase** | 2-4 hours | 1-2 days | High (DIY UI) | Low-Medium | Low (PostgreSQL export) |
| **Firebase** | 1-2 hours | 4-8 hours | Medium | Low | High (Firebase ecosystem) |
| **AWS Cognito** | 4-8 hours | 2-5 days | High | Medium | Medium (AWS-specific) |
| **Ory** | 4-8 hours (Cloud) | 2-4 days | High | Medium (self-host) | Low (open standards) |
| **WorkOS** | 2-4 hours | 1 day | Low-Medium | Low | Medium |
| **Stytch** | 1-2 hours | 4-8 hours | Low-Medium | Low | Medium |
| **Magic** | 1 hour | 4 hours | Low | Very Low | Medium |
| **Hanko** | 2-4 hours | 1-2 days | Medium | Medium (self-host) | Low (open-source) |
| **Keycloak** | 8-16 hours | 1-2 weeks | Very High | High (self-managed) | Low (OIDC/SAML standard) |
| **FusionAuth** | 4-8 hours | 2-5 days | High | Medium | Low (standard protocols) |
| **SuperTokens** | 2-4 hours | 1-2 days | Medium | Medium | Medium |
| **Descope** | 1-2 hours | 4-8 hours | Very Low (no-code) | Very Low | Medium |
| **Passage** | 1 hour | 4 hours | Very Low (passkey-only) | Very Low | High (passkey-only) |
| **PropelAuth** | 2-4 hours | 1 day | Low-Medium | Low | Medium |

**Fastest to Production**:
1. **Clerk**: Best DX for React/Next.js, pre-built components
2. **Descope**: Visual flow builder, no-code approach
3. **Magic**: Simplest for passwordless-only
4. **Stytch**: Fast passwordless integration

**Most Customizable**:
1. **Keycloak**: Full control, complex
2. **Ory**: Headless-first, flexible
3. **Supabase**: Headless, PostgreSQL-backed
4. **Auth0**: Extensive customization options

---

## 6. PASSWORDLESS & MODERN AUTHENTICATION

### 6.1 Passwordless Authentication Methods

| Method | Auth0 | Clerk | Supabase | Firebase | Cognito | Ory | Stytch | Magic | Hanko | Passage | Descope |
|--------|-------|-------|----------|----------|---------|-----|--------|-------|-------|---------|---------|
| **Magic Link (Email)** | Yes | Yes | Yes | Yes | No | Yes | Yes (core) | Yes (core) | Yes | No | Yes |
| **OTP (Email)** | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes |
| **SMS OTP** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | No | Yes |
| **WhatsApp OTP** | Limited | Limited | No | No | No | No | Yes | No | No | No | Yes |
| **WebAuthn/Passkeys** | Yes | Yes | Limited | No | No | Yes | Yes | No | Yes (core) | Yes (core) | Yes |
| **FIDO2** | Yes | Yes | Limited | No | No | Yes | Yes | No | Yes | Yes | Yes |
| **Biometric (TouchID/FaceID)** | Via WebAuthn | Via WebAuthn | Limited | Yes (native SDKs) | No | Via WebAuthn | Yes | No | Yes | Yes | Yes |
| **Device Fingerprinting** | Yes (Enterprise) | Yes | No | No | No | No | Yes | No | No | No | Yes |
| **Social Login as Passwordless** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Limited | No | Yes |

### 6.2 Passkey/WebAuthn Implementation Quality

**Passkey Leaders**:
1. **Passage (1Password)**: Best-in-class passkey implementation, 1Password ecosystem
2. **Hanko**: Open-source, passkey-first design, excellent WebAuthn support
3. **Clerk**: Strong passkey support, React-native integration
4. **Stytch**: Production-grade WebAuthn, biometric support
5. **Descope**: Visual passkey flows, no-code setup

**WebAuthn Features**:

| Feature | Passage | Hanko | Clerk | Stytch | Auth0 | Descope | Ory |
|---------|---------|-------|-------|--------|-------|---------|-----|
| **Platform Authenticators** | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Roaming Authenticators** | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Conditional UI (autofill)** | Yes | Yes | Yes | Yes | Limited | Yes | Limited |
| **Passkey Sync** | Yes (1Password) | Yes | Yes | Yes | Limited | Yes | Yes |
| **Cross-device Authentication** | Yes | Yes | Yes | Yes | Limited | Yes | Yes |
| **Backup Credentials** | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Attestation Support** | Yes | Yes | Yes | Yes | Yes | Yes | Yes |

### 6.3 Passwordless User Experience

**Best Passwordless UX**:
1. **Magic**: Simplest email-only passwordless (now paid-only)
2. **Stytch**: Comprehensive passwordless options, smooth flows
3. **Clerk**: Excellent React components for passwordless
4. **Passage**: Best biometric/passkey experience

**Passwordless Trade-offs**:
- **Email Magic Links**: High friction (check email), but universal
- **SMS OTP**: Fast, but carrier costs and availability issues
- **Passkeys**: Best UX, but requires modern devices/browsers
- **Social Login**: Fastest, but third-party dependency

---

## 7. ENTERPRISE & B2B FEATURES

### 7.1 Enterprise SSO (SAML/OIDC)

| Provider | SAML Support | OIDC Support | SSO Pricing | Max Connections | IdP Integrations |
|----------|--------------|--------------|-------------|-----------------|------------------|
| **Auth0** | Yes | Yes | Enterprise tier ($$$$) | Unlimited | Okta, Azure AD, Google Workspace, ADFS, all major |
| **Clerk** | Yes | Yes | $99/connection/mo | Unlimited | Okta, Azure AD, Google Workspace, ADFS |
| **Supabase** | No | Yes | N/A | Manual setup | Manual OIDC |
| **Firebase** | No | No | N/A | N/A | N/A |
| **AWS Cognito** | Yes | Yes | Included | Unlimited | SAML 2.0 generic |
| **Ory** | Yes | Yes | Included (OSS) | Unlimited | Generic SAML/OIDC |
| **WorkOS** | Yes (core) | Yes | $125/connection/mo | Unlimited | 20+ built-in (Okta, Azure, Google, OneLogin, etc.) |
| **Stytch** | Yes | Yes | $99/connection/mo | Unlimited | Okta, Azure AD, Google Workspace |
| **Keycloak** | Yes | Yes | Included (OSS) | Unlimited | All major IdPs |
| **FusionAuth** | Yes | Yes | Included | Unlimited | Generic SAML/OIDC |
| **SuperTokens** | No | Yes | N/A | Manual | Manual OIDC |
| **Descope** | Yes | Yes | Higher tiers | Unlimited | Okta, Azure AD, Google |
| **PropelAuth** | Yes | Yes | Included | Unlimited | Okta, Azure AD, Google |

**SSO Pricing Comparison**:
- **Most Affordable**: AWS Cognito (included), Keycloak (free), FusionAuth (included)
- **Mid-Tier**: Clerk ($99/connection), Stytch ($99/connection), WorkOS ($125/connection)
- **Premium**: Auth0 (Enterprise tier, typically $5K-20K+/month)

**Best SSO Implementation**:
1. **WorkOS**: Purpose-built for B2B SSO, easiest setup, 20+ built-in IdPs
2. **Auth0**: Most comprehensive, enterprise-grade
3. **Keycloak**: Most flexible (open-source), complex setup
4. **PropelAuth**: B2B-focused, included in pricing

### 7.2 Organization & Multi-Tenancy

| Provider | Organizations | Team Management | Invitations | SCIM Provisioning | Directory Sync |
|----------|---------------|-----------------|-------------|-------------------|----------------|
| **Auth0** | Yes | Yes | Yes | Yes (Enterprise) | Yes (Enterprise) |
| **Clerk** | Yes (core feature) | Yes | Yes | Planned | Limited |
| **Supabase** | Via RLS | Manual | Manual | No | No |
| **Firebase** | Manual | Manual | Manual | No | No |
| **AWS Cognito** | Via Groups | Yes | Manual | Limited | No |
| **Ory** | Manual | Manual | Manual | No | No |
| **WorkOS** | Yes (core) | Yes | Yes | Yes | Yes |
| **Stytch** | Yes | Yes | Yes | Planned | Limited |
| **Keycloak** | Yes (Realms) | Yes | Yes | Limited | Manual |
| **FusionAuth** | Yes (Tenants) | Yes | Yes | Limited | Manual |
| **SuperTokens** | Manual | Manual | Manual | No | No |
| **Descope** | Yes | Yes | Yes | Planned | Limited |
| **PropelAuth** | Yes (core) | Yes | Yes | Planned | Limited |

**Best for B2B Multi-Tenancy**:
1. **WorkOS**: Purpose-built for B2B, SCIM, directory sync
2. **Clerk**: Excellent organization management, React-native
3. **PropelAuth**: B2B-focused, organization-first design
4. **Auth0**: Enterprise-grade, comprehensive features
5. **FusionAuth**: Full tenant isolation

### 7.3 Admin & User Management Portals

| Provider | Admin Dashboard | User Management UI | Audit Logs | Impersonation | Bulk Operations |
|----------|----------------|-------------------|------------|---------------|-----------------|
| **Auth0** | Excellent | Yes | Yes | Yes | Yes |
| **Clerk** | Excellent | Yes | Yes | Yes | Yes |
| **Supabase** | Good (Table Editor) | Yes (SQL) | Yes (PostgreSQL logs) | Manual | Via SQL |
| **Firebase** | Good (Firebase Console) | Yes | Yes (Firestore) | Manual | Via Admin SDK |
| **AWS Cognito** | Basic (AWS Console) | Yes | Yes (CloudTrail) | Manual | Via CLI/SDK |
| **Ory** | Ory Console | Yes | Limited | No | Via API |
| **WorkOS** | Good | Yes | Yes | Limited | Limited |
| **Stytch** | Good | Yes | Yes | Yes | Limited |
| **Keycloak** | Excellent | Yes | Yes | Yes | Yes |
| **FusionAuth** | Excellent | Yes | Yes | Yes | Yes |
| **SuperTokens** | Good | Limited | Limited | No | Via API |
| **Descope** | Good | Yes | Yes | Yes | Limited |
| **PropelAuth** | Excellent | Yes | Yes | Yes | Yes |

### 7.4 SLA & Support Tiers

| Provider | Standard SLA | Enterprise SLA | Support Channels | Response Time | Premium Support Cost |
|----------|-------------|----------------|------------------|---------------|---------------------|
| **Auth0** | 99.9% (paid) | 99.99% | Email, chat, phone | 1-24 hours | Included in Enterprise |
| **Clerk** | 99.9% | Custom | Email, Slack, Discord | 1-24 hours | Included in plans |
| **Supabase** | 99.9% (Pro+) | Custom | Email, Discord, GitHub | Community or priority | Enterprise tier |
| **Firebase** | 99.95% (Google) | Custom | Google Cloud Support | Based on plan | $29-15K+/month (GCP) |
| **AWS Cognito** | 99.9% | 99.99% (Enterprise Support) | AWS Support | Based on plan | $29-15K+/month |
| **Ory** | 99.9% (Cloud) | Custom | Email, Slack, GitHub | Community or SLA | Custom enterprise |
| **WorkOS** | 99.9% | Custom | Email, Slack | <24 hours | Included |
| **Stytch** | 99.9% | Custom | Email, Slack | <24 hours | Included |
| **Keycloak** | DIY | Red Hat SSO SLA | Community or Red Hat | N/A or Red Hat SLA | Red Hat subscription |
| **FusionAuth** | 99.9% (Cloud) | Custom | Email, forum | Community or SLA | Paid support tiers |
| **SuperTokens** | 99.9% (managed) | Custom | Email, Discord, GitHub | Community or priority | Enterprise support |
| **Descope** | 99.9% | Custom | Email, Slack | <24 hours | Included |
| **PropelAuth** | 99.9% | Custom | Email, Slack | <24 hours | Included |

---

## 8. LOCK-IN & MIGRATION ANALYSIS

### 8.1 Data Portability

| Provider | User Export | Full Data Export | Export Format | Import Tools | Migration Docs |
|----------|-------------|------------------|---------------|--------------|----------------|
| **Auth0** | Yes (API/bulk) | Yes | JSON, CSV | Import API | Good |
| **Clerk** | Yes (API) | Yes | JSON | Import API | Good |
| **Supabase** | Yes (SQL) | Yes | PostgreSQL dump | Standard SQL | Excellent (open DB) |
| **Firebase** | Yes (Admin SDK) | Yes | JSON | Import via SDK | Good |
| **AWS Cognito** | Yes (API) | Yes | CSV, JSON | Import API | Good |
| **Ory** | Yes (SQL) | Yes | PostgreSQL dump | Standard SQL | Excellent (OSS) |
| **WorkOS** | Yes (API) | Yes | JSON | Import API | Good |
| **Stytch** | Yes (API) | Yes | JSON | Import API | Limited |
| **Keycloak** | Yes (export) | Yes | JSON | Import tool | Excellent (OSS) |
| **FusionAuth** | Yes (API) | Yes | JSON | Import API | Good |
| **SuperTokens** | Yes (DB access) | Yes | PostgreSQL/MySQL | Direct DB | Excellent (OSS) |
| **Descope** | Yes (API) | Yes | JSON | Import API | Limited |
| **PropelAuth** | Yes (API) | Yes | JSON | Import API | Limited |

### 8.2 Lock-In Risk Assessment

| Provider | Lock-in Risk | Proprietary Features | Standard Protocols | Self-Host Option | Migration Complexity |
|----------|--------------|---------------------|-------------------|------------------|---------------------|
| **Auth0** | High | Auth0 Rules, Actions, proprietary APIs | OIDC, SAML, OAuth2 | No | High (custom logic) |
| **Clerk** | Medium-High | Clerk-specific components, orgs | OIDC, SAML, OAuth2 | No | Medium (React deps) |
| **Supabase** | Low | Row-Level Security (PostgreSQL) | Standard PostgreSQL | Yes (OSS) | Low (PostgreSQL export) |
| **Firebase** | Very High | Firebase-specific SDKs, deep integration | Limited standard protocols | No | Very High |
| **AWS Cognito** | Medium | AWS-specific integrations | OIDC, SAML, OAuth2 | No | Medium (AWS-centric) |
| **Ory** | Very Low | Open-source, standard protocols | OIDC, OAuth2 | Yes (OSS) | Very Low |
| **WorkOS** | Medium | WorkOS-specific APIs | OIDC, SAML, OAuth2 | No | Medium |
| **Stytch** | Medium | Stytch-specific SDKs | OIDC, OAuth2 | No | Medium |
| **Keycloak** | Very Low | Open-source, full control | OIDC, SAML, OAuth2, LDAP | Yes (OSS) | Very Low |
| **FusionAuth** | Low | FusionAuth-specific features | OIDC, SAML, OAuth2 | Yes | Low (standard protocols) |
| **SuperTokens** | Low | Open-source | OIDC, OAuth2 | Yes (OSS) | Low |
| **Descope** | Medium-High | Visual flows, proprietary | OIDC, SAML, OAuth2 | No | Medium-High |
| **PropelAuth** | Medium | PropelAuth-specific | OIDC, OAuth2 | No | Medium |

### 8.3 Password Migration Strategies

**Password Hash Support**:

| Provider | Bcrypt | Argon2 | Scrypt | PBKDF2 | Custom Hash | Lazy Migration |
|----------|--------|--------|--------|--------|-------------|----------------|
| **Auth0** | Yes | Yes | Yes | Yes | Yes (Custom DB) | Yes |
| **Clerk** | Yes | Yes | Limited | Yes | Yes (Webhooks) | Yes |
| **Supabase** | Yes (default) | No | No | Yes | Via triggers | Yes |
| **Firebase** | Yes | No | Yes | Yes | No | Limited |
| **AWS Cognito** | No (must reset) | No | No | No | Via Lambda | Yes |
| **Ory** | Yes | Yes | Yes | Yes | Via plugins | Yes |
| **WorkOS** | Yes | Yes | Limited | Yes | Via webhooks | Yes |
| **Stytch** | Yes | Yes | Limited | Yes | Via API | Yes |
| **Keycloak** | Yes | Yes | Yes | Yes | Custom SPI | Yes |
| **FusionAuth** | Yes | Yes | Yes | Yes | Yes | Yes |
| **SuperTokens** | Yes | Yes | Limited | Yes | Via core override | Yes |

**Best for Migration**:
1. **Auth0**: Custom Database Connections for gradual migration
2. **Keycloak**: User Federation for legacy systems
3. **FusionAuth**: Connector support for various hash formats
4. **Ory**: Flexible identity schema

### 8.4 Exit Strategy Complexity

**Easiest Exit** (Low lock-in):
1. **Keycloak**: Standard OIDC/SAML, self-hosted, open-source
2. **Ory**: Open-source, standard protocols, PostgreSQL
3. **Supabase**: PostgreSQL-native, open-source
4. **FusionAuth**: Standard protocols, data export

**Moderate Exit**:
1. **Auth0**: Standard protocols, but custom logic migration complex
2. **AWS Cognito**: Standard protocols, but AWS-centric
3. **Clerk**: Good export, but React component dependencies
4. **Stytch**: API-based export, passwordless-specific

**Difficult Exit** (High lock-in):
1. **Firebase**: Deep ecosystem integration, proprietary SDKs
2. **Descope**: Visual flows don't translate elsewhere
3. **Magic**: Passwordless-only, proprietary

---

## 9. MARKET POSITIONING & USE CASE FIT

### 9.1 Provider Sweet Spots

| Provider | Best For | Not Ideal For |
|----------|----------|---------------|
| **Auth0** | Enterprise B2B, complex auth flows, extensive customization | Startups (price), simple use cases, cost-conscious |
| **Clerk** | Modern SaaS, React/Next.js apps, B2B with orgs | Non-React stacks, budget-conscious at scale, legacy systems |
| **Supabase** | Full-stack apps, PostgreSQL users, open-source preference | Enterprise SSO, compliance-heavy, non-technical teams |
| **Firebase** | Mobile apps, Google ecosystem, prototyping | Enterprise SSO, complex auth, non-Firebase stack |
| **AWS Cognito** | AWS-native apps, high scale (>500K MAU), cost optimization | Non-AWS, quick setup, extensive customization |
| **Ory** | Privacy-first, self-hosted, open-source preference | Quick setup, hosted-only, minimal dev resources |
| **WorkOS** | B2B SaaS with enterprise SSO, directory sync | B2C apps, passwordless-first, budget startups |
| **Stytch** | Passwordless-first, modern consumer apps, fintech | Legacy password systems, enterprise SSO-heavy, self-hosted |
| **Magic** | Web3, simple passwordless, crypto wallets | Traditional auth, password support, complex flows |
| **Hanko** | Passkey-first, open-source, EU compliance | Password-based, quick hosted setup, enterprise SSO |
| **Keycloak** | Enterprise self-hosted, full control, complex IAM | Quick setup, limited dev resources, managed service preference |
| **FusionAuth** | Developers, self-host flexibility, standard protocols | Quick managed setup, passwordless-first, minimal customization |
| **SuperTokens** | Developers, open-source, session security focus | No-code preference, extensive enterprise SSO, minimal setup |
| **Descope** | No-code/low-code, visual flows, fast prototyping | Heavy customization, self-hosted, open-source |
| **Passage** | Passkey-only, 1Password ecosystem, biometric-first | Password support required, legacy systems, complex auth |
| **PropelAuth** | B2B SaaS, organization management, simple pricing | B2C, passwordless-first, enterprise at scale |

### 9.2 Business Size Fit

| MAU Scale | Recommended Providers | Rationale |
|-----------|----------------------|-----------|
| **0-10K MAU** | Firebase (free), Supabase (free), Clerk (free), Cognito (free) | Generous free tiers, easy setup |
| **10K-50K MAU** | Clerk ($25-75/mo), Supabase ($25/mo), Cognito (~$0), Descope ($99-249/mo) | Best price/features, low overhead |
| **50K-100K MAU** | Clerk ($199/mo), Cognito ($550/mo), Supabase ($25/mo), PropelAuth (custom) | Scale efficiently, still affordable |
| **100K-500K MAU** | Cognito ($550-2,750/mo), Clerk ($799/mo), negotiate Auth0 | Cost management critical, volume discounts |
| **500K-1M MAU** | Cognito ($2,750-5,500/mo), Auth0 (custom), enterprise deals | Enterprise features needed, negotiate pricing |
| **1M+ MAU** | Cognito (best economics), Auth0 (enterprise), Keycloak (self-hosted) | Custom deals, dedicated infrastructure |
| **Enterprise SSO Required** | WorkOS ($125/conn), Clerk ($99/conn), PropelAuth (included), Cognito (included) | SSO tax, factor $500-2K/mo for 5-10 connections |

### 9.3 Technology Stack Fit

| Stack | Best Providers | Rationale |
|-------|---------------|-----------|
| **React/Next.js** | Clerk, Supabase, Auth0, Descope | Excellent React integrations, Next.js App Router support |
| **Vue/Nuxt** | Auth0, Supabase, Firebase | Good SDK support, community modules |
| **Svelte/SvelteKit** | Supabase, Auth0, SuperTokens | Headless or flexible SDKs |
| **Mobile (React Native)** | Clerk, Auth0, Firebase, Supabase | Native mobile SDKs, biometric support |
| **iOS/Android Native** | Firebase, Auth0, Stytch, Supabase | Platform-specific SDKs |
| **Node.js Backend** | Supabase, SuperTokens, Auth0, Ory | Excellent Node.js support, session management |
| **Python/Django** | Auth0, Supabase, Keycloak, Ory | Good Python SDK support |
| **Ruby/Rails** | Auth0, Supabase, Keycloak | Standard OIDC/OAuth2 integration |
| **AWS Infrastructure** | Cognito, Auth0, Supabase | AWS-native or multi-cloud |
| **Google Cloud** | Firebase, Auth0, Supabase | GCP-native or multi-cloud |
| **Multi-Cloud/Hybrid** | Auth0, Supabase, Ory, Keycloak | Cloud-agnostic |

### 9.4 Feature Priority Fit

| Priority | Recommended Providers | Why |
|----------|----------------------|-----|
| **Fastest Setup** | Clerk, Descope, Magic, Passage | Pre-built UI, minimal code |
| **Passwordless-First** | Stytch, Magic, Passage, Hanko | Purpose-built for passwordless |
| **Passkey/WebAuthn** | Passage, Hanko, Clerk, Stytch | Best passkey implementation |
| **Enterprise SSO** | WorkOS, Auth0, Keycloak, PropelAuth | Purpose-built or comprehensive |
| **B2B Multi-Tenancy** | Clerk, WorkOS, PropelAuth, Auth0 | Organization management built-in |
| **Open-Source** | Keycloak, Ory, Supabase, SuperTokens, Hanko | Full source access, self-host |
| **Cost Optimization** | Cognito, Supabase, Keycloak (self-host) | Best economics at scale |
| **Privacy/GDPR** | Ory, Hanko, Supabase, Keycloak | EU-based or self-hosted |
| **Developer Experience** | Clerk, Supabase, Auth0, Descope | Best docs, SDKs, community |
| **Compliance (HIPAA)** | Cognito, Firebase (GCP), Auth0 (Enterprise) | BAA available, certified |
| **Full Customization** | Keycloak, Ory, Supabase, Auth0 | Maximum flexibility |
| **No-Code/Low-Code** | Descope, Clerk, Auth0 (Universal Login) | Visual builders, pre-built UI |

---

## 10. KEY DIFFERENTIATORS SUMMARY

### 10.1 Unique Strengths

**Auth0 (Okta)**:
- Most comprehensive enterprise identity platform
- Extensive customization (Rules, Actions, Extensions)
- 30+ social providers, universal login
- Part of Okta ecosystem (enterprise credibility)
- Best for complex, multi-faceted auth requirements

**Clerk**:
- Best-in-class developer experience for React/Next.js
- Beautiful pre-built components, themeable
- Organizations built-in (core feature)
- Excellent pricing for startups (10K free MAU)
- Modern, developer-first approach

**Supabase Auth**:
- Open-source, PostgreSQL-native
- Row-Level Security integration
- Part of full Supabase backend (database, storage, functions)
- 50K free MAU, generous pricing
- Complete data ownership

**Firebase Auth**:
- Unmatched mobile SDK support (iOS, Android, Flutter)
- Deepest Google ecosystem integration
- Anonymous auth, phone auth built-in
- Essentially free for most use cases
- Best for mobile-first applications

**AWS Cognito**:
- Most cost-effective at scale ($0.0055/MAU after 50K)
- Full AWS integration (Lambda triggers, IAM, etc.)
- Advanced security features (risk-based auth, adaptive)
- Best economics for >500K MAU
- Enterprise compliance (FedRAMP, HIPAA)

**Ory**:
- Open-source, GDPR-native design
- Headless-first architecture
- Zero lock-in (self-hosted, open protocols)
- Kratos (auth), Hydra (OAuth2), Keto (permissions)
- Best for privacy-first, self-hosted requirements

**WorkOS**:
- Purpose-built for B2B enterprise SSO
- 20+ built-in IdP integrations
- Directory sync (SCIM) built-in
- Simplest enterprise SSO setup
- Best for B2B SaaS selling to enterprises

**Stytch**:
- Passwordless-first platform
- Comprehensive passwordless options (magic link, OTP, WebAuthn, biometric)
- Fraud prevention built-in
- B2C and B2B modes
- Best for modern passwordless applications

**Magic**:
- Simplest email-based passwordless (historically)
- Web3/crypto wallet integration
- DID (Decentralized Identity) support
- Best for Web3 and crypto applications

**Hanko**:
- Open-source passkey-first platform
- Excellent WebAuthn implementation
- EU-based, GDPR-native
- Web components (framework-agnostic)
- Best for passkey-only, open-source

**Keycloak**:
- Most feature-complete open-source IAM
- Enterprise-grade (Red Hat backing)
- Full LDAP, Kerberos, SAML, OIDC support
- User Federation (integrate legacy systems)
- Best for complex enterprise self-hosted IAM

**FusionAuth**:
- Developer-friendly with self-host flexibility
- Free community edition (full features)
- Tenant isolation built-in
- Flexible deployment (self-host or cloud)
- Best for developers wanting control without Keycloak complexity

**SuperTokens**:
- Open-source with managed hosting option
- Session management focus (secure, anti-CSRF)
- Recipe-based integration (opinionated patterns)
- PostgreSQL or MySQL backend
- Best for session security-conscious developers

**Descope**:
- Visual flow builder (no-code auth flows)
- Drag-drop authentication journeys
- Fast time-to-production
- Modern, user-friendly interface
- Best for no-code/low-code teams

**Passage (1Password)**:
- Best-in-class passkey/biometric authentication
- 1Password ecosystem integration
- Passkey-only focus (no password legacy)
- Acquired by 1Password (security credibility)
- Best for passkey-only modern applications

**PropelAuth**:
- B2B SaaS-focused
- Organization management built-in
- Simple, transparent pricing
- Enterprise SSO included
- Best for B2B SaaS companies

### 10.2 Critical Trade-offs

| Trade-off | Option A | Option B |
|-----------|----------|----------|
| **Cost vs Features** | Cognito (cheap, DIY) | Auth0/Clerk (expensive, full-featured) |
| **Control vs Simplicity** | Keycloak (full control, complex) | Clerk/Descope (simple, less control) |
| **Passwordless vs Traditional** | Stytch/Magic (passwordless-only) | Auth0/Clerk (both options) |
| **Open-Source vs Managed** | Keycloak/Ory (OSS, self-managed) | Auth0/Clerk (managed, vendor lock-in) |
| **Setup Speed vs Customization** | Descope/Clerk (fast, opinionated) | Keycloak/Ory (slow, fully customizable) |
| **B2B vs B2C** | WorkOS/PropelAuth (B2B SSO) | Stytch/Magic (B2C passwordless) |
| **Scale Economics** | Cognito (best >500K MAU) | Clerk (best <200K MAU) |
| **Mobile vs Web** | Firebase (mobile-first) | Clerk (web-first) |
| **Lock-in Risk** | Keycloak/Ory (zero lock-in) | Firebase (high lock-in) |
| **Privacy/GDPR** | Ory/Hanko (EU, self-host) | Firebase/Cognito (US clouds) |

---

## 11. COMPREHENSIVE PROVIDER PROFILES

### 11.1 Auth0 (Okta)

**Type**: Enterprise Identity Platform
**Founded**: 2013 (Acquired by Okta 2021 for $6.5B)
**Headquarters**: Bellevue, WA (part of Okta)

**Core Strengths**:
- Most comprehensive enterprise auth platform
- 30+ social providers, universal login, extensive customization
- Rules engine, Actions (serverless hooks), Extensions marketplace
- Multi-region deployment (US, EU, AU, JP)
- PCI DSS, SOC 2 Type II, ISO 27001, GDPR, HIPAA (Enterprise)

**Pricing**: Free (7,500 MAU) | Essentials $228/mo (500 MAU) | Professional $1,050/mo | Enterprise (custom)

**Best For**: Enterprise B2B, complex auth flows, extensive customization needs, regulatory compliance

**Limitations**: Expensive at scale, complex pricing, Enterprise tier required for SSO/HIPAA, Okta acquisition concerns (consolidation, pricing increases)

---

### 11.2 Clerk

**Type**: Modern Auth-as-a-Service
**Founded**: 2021
**Headquarters**: San Francisco, CA

**Core Strengths**:
- Best-in-class DX for React/Next.js (App Router support)
- Beautiful pre-built components, extensive theming
- Organizations built-in, excellent B2B features
- 10K free MAU, generous pricing ($25/mo after)
- Modern, developer-friendly dashboard

**Pricing**: Free (10K MAU) | Hobby $25/mo | Pro $199/mo (100K MAU) | Enterprise (custom)

**Best For**: Modern SaaS, React/Next.js apps, B2B with organizations, developer-first teams

**Limitations**: React-centric (other frameworks less polished), moderate lock-in (Clerk-specific components), pricing scales quickly beyond 100K MAU

---

### 11.3 Supabase Auth

**Type**: Open-Source Backend-as-a-Service (Auth Module)
**Founded**: 2020
**Headquarters**: Singapore (distributed)

**Core Strengths**:
- Open-source, PostgreSQL-native
- Row-Level Security (RLS) for authorization
- Part of full backend (database, storage, edge functions, realtime)
- 50K free MAU, affordable ($25/mo Pro)
- Complete data ownership, self-hostable

**Pricing**: Free (50K MAU) | Pro $25/mo | Team $599/mo | Enterprise (custom)

**Best For**: Full-stack developers, PostgreSQL users, open-source preference, cost-conscious startups

**Limitations**: No enterprise SSO (SAML), limited compliance certifications, DIY UI (headless), community support (unless enterprise)

---

### 11.4 Firebase Auth

**Type**: Backend-as-a-Service (Google)
**Founded**: 2011 (Acquired by Google 2014)
**Headquarters**: Mountain View, CA (Google)

**Core Strengths**:
- Unmatched mobile SDK support (iOS, Android, Flutter, Unity)
- Deep Google ecosystem integration (GCP, Analytics, Cloud Functions)
- Essentially free (phone auth: 10K/month free, then ~$0.01/verification)
- Anonymous auth, built-in phone verification
- Google Cloud compliance (SOC 2, ISO 27001, HIPAA via BAA)

**Pricing**: Free (unlimited MAU, phone 10K/mo) | Identity Platform (custom, advanced features)

**Best For**: Mobile apps, Google Cloud ecosystem, prototyping, phone authentication

**Limitations**: No enterprise SSO (SAML/OIDC), high lock-in (Firebase ecosystem), limited for B2B use cases, Identity Platform expensive for advanced features

---

### 11.5 AWS Cognito

**Type**: AWS Cloud Identity Service
**Founded**: 2014
**Headquarters**: Seattle, WA (AWS)

**Core Strengths**:
- Most cost-effective at scale ($0.0055/MAU after 50K free)
- Full AWS integration (Lambda triggers, IAM, CloudWatch, etc.)
- Advanced security features (risk-based auth, adaptive MFA, Cognito Advanced Security)
- Enterprise compliance (FedRAMP, HIPAA, SOC 2, ISO 27001, PCI DSS Level 1)
- Global scale (all AWS regions)

**Pricing**: Free (50K MAU) | $0.0055/MAU beyond | Advanced Security $0.05/MAU

**Best For**: AWS-native apps, cost optimization at scale (>500K MAU), enterprise compliance, AWS ecosystem users

**Limitations**: AWS expertise required, complex setup, limited customization, basic hosted UI, steeper learning curve

---

### 11.6 Ory

**Type**: Open-Source Identity Infrastructure
**Founded**: 2015
**Headquarters**: Munich, Germany

**Core Strengths**:
- Open-source (Apache 2.0), zero lock-in
- GDPR-native design (EU-based, privacy-first)
- Headless-first architecture (API-driven)
- Modular: Kratos (identity), Hydra (OAuth2/OIDC), Keto (permissions), Oathkeeper (proxy)
- Cloud offering + self-hostable

**Pricing**: Free (self-hosted) | Cloud Developer $29/mo | Cloud Growth custom | Enterprise custom

**Best For**: Privacy-first, self-hosted requirements, zero lock-in, open-source preference, EU/GDPR compliance

**Limitations**: Complex setup (multiple components), limited managed features, smaller community than Keycloak, cloud offering still maturing

---

### 11.7 WorkOS

**Type**: Enterprise Auth for B2B SaaS
**Founded**: 2019
**Headquarters**: San Francisco, CA

**Core Strengths**:
- Purpose-built for B2B enterprise SSO
- 20+ built-in IdP integrations (Okta, Azure AD, Google, OneLogin, JumpCloud, etc.)
- Directory Sync (SCIM) built-in
- Simple pricing ($125/connection/mo)
- Easiest enterprise SSO setup

**Pricing**: Free (basic auth) | SSO $125/connection/mo | Directory Sync $125/connection/mo

**Best For**: B2B SaaS selling to enterprises, SSO requirements, directory sync needs

**Limitations**: B2B-focused only (not ideal for B2C), limited passwordless features, smaller provider (risk), no self-hosting

---

### 11.8 Stytch

**Type**: Passwordless Authentication Platform
**Founded**: 2020
**Headquarters**: San Francisco, CA

**Core Strengths**:
- Passwordless-first platform (magic links, OTP, WebAuthn, biometrics)
- Comprehensive passwordless options
- Fraud prevention built-in (device fingerprinting, bot detection)
- B2C and B2B modes
- SOC 2 Type II, modern infrastructure

**Pricing**: Free (5K MAU, 25 testing) | Growth $249/mo (10K MAU) | $1,749/mo (100K MAU) | Enterprise custom

**Best For**: Modern passwordless apps, fintech, consumer apps, biometric authentication

**Limitations**: Premium pricing, passwordless-focused (password support exists but not core), limited enterprise SSO on lower tiers

---

### 11.9 Magic

**Type**: Passwordless Auth (Web3-focused)
**Founded**: 2018
**Headquarters**: San Francisco, CA

**Core Strengths**:
- Simplest email-based passwordless (historically)
- Web3/crypto wallet integration (core use case)
- DID (Decentralized Identity) support
- SDK-based integration
- SOC 2 Type II

**Pricing**: No free tier (2025) | Starts at $199/mo

**Best For**: Web3 applications, crypto/NFT platforms, simple passwordless

**Limitations**: No free tier (changed in 2025), limited auth methods, smaller provider, high lock-in (Magic-specific SDKs)

---

### 11.10 Hanko

**Type**: Open-Source Passkey Authentication
**Founded**: 2022
**Headquarters**: Berlin, Germany

**Core Strengths**:
- Open-source passkey-first platform
- Excellent WebAuthn/FIDO2 implementation
- EU-based, GDPR-native
- Web components (framework-agnostic)
- Cloud offering + self-hostable

**Pricing**: Free (self-hosted) | Cloud (custom pricing)

**Best For**: Passkey-only authentication, open-source, EU/GDPR compliance, modern biometric auth

**Limitations**: Young project (2022), smaller community, passkey-only (no password fallback), cloud offering nascent

---

### 11.11 Keycloak

**Type**: Open-Source Identity & Access Management
**Founded**: 2014 (Red Hat)
**Headquarters**: Raleigh, NC (Red Hat/IBM)

**Core Strengths**:
- Most feature-complete open-source IAM
- Enterprise-grade (Red Hat backing, Red Hat SSO commercial version)
- Full protocol support (OIDC, SAML, OAuth2, LDAP, Kerberos)
- User Federation (integrate legacy systems)
- Realm-based multi-tenancy, extensive customization

**Pricing**: Free (open-source) | Red Hat SSO (commercial support, custom pricing)

**Best For**: Enterprise self-hosted IAM, complex identity requirements, full control, legacy system integration, zero licensing cost

**Limitations**: Very complex setup, steep learning curve, self-managed infrastructure, no official cloud offering, Java-based (resource-intensive)

---

### 11.12 FusionAuth

**Type**: Auth Platform (Self-Host or Cloud)
**Founded**: 2018
**Headquarters**: Denver, CO

**Core Strengths**:
- Free community edition (full features, unlimited)
- Self-host or managed cloud options
- Tenant isolation built-in
- Standard protocol support (OIDC, SAML, OAuth2)
- Developer-friendly, simpler than Keycloak

**Pricing**: Free (community, self-hosted) | Cloud ~$75/mo (hosting) | Enterprise (custom support)

**Best For**: Developers wanting self-host control, multi-tenant SaaS, no licensing costs, standard protocols

**Limitations**: Self-hosting operational burden, cloud offering less mature than competitors, smaller ecosystem than Keycloak

---

### 11.13 SuperTokens

**Type**: Open-Source Auth (Session-Focused)
**Founded**: 2020
**Headquarters**: Remote-first

**Core Strengths**:
- Open-source, session management focus
- Secure session handling (anti-CSRF, token theft detection)
- Recipe-based integration (opinionated best practices)
- Self-host or managed (5K free MAU on managed)
- PostgreSQL/MySQL backend

**Pricing**: Free (self-hosted) | Managed $49/mo (5K MAU) → Custom

**Best For**: Session security-conscious developers, self-host preference, PostgreSQL/MySQL users, open-source

**Limitations**: Less feature-complete than Keycloak, smaller community, limited enterprise SSO, recipe approach may be limiting for customization

---

### 11.14 Descope

**Type**: No-Code/Low-Code Auth Platform
**Founded**: 2022
**Headquarters**: Los Altos, CA

**Core Strengths**:
- Visual flow builder (drag-drop auth journeys)
- No-code authentication flows
- Pre-built UI components
- Fast time-to-production (minutes to setup)
- Modern interface, developer-friendly

**Pricing**: Free (7,500 MAU) | Essentials $99/mo (10K MAU) | Pro $999/mo (100K MAU) | Enterprise custom

**Best For**: No-code/low-code teams, fast prototyping, visual auth flow design, non-technical stakeholders

**Limitations**: Young company (2022), visual flows don't translate to other platforms (lock-in), limited customization beyond flows, smaller provider risk

---

### 11.15 Passage (1Password)

**Type**: Passkey Authentication
**Founded**: 2022 (Acquired by 1Password 2023)
**Headquarters**: Toronto, Canada (1Password)

**Core Strengths**:
- Best-in-class passkey/biometric authentication
- 1Password ecosystem integration
- Passkey-only focus (modern, no password legacy)
- 1Password security credibility
- Excellent WebAuthn implementation

**Pricing**: Free (1K MAU) | Growth (custom pricing)

**Best For**: Passkey-only modern apps, biometric-first authentication, 1Password ecosystem users

**Limitations**: Passkey-only (no password fallback), small free tier (1K MAU), limited auth methods, 1Password acquisition (integration direction unclear)

---

### 11.16 PropelAuth

**Type**: B2B SaaS Authentication
**Founded**: 2022
**Headquarters**: San Francisco, CA

**Core Strengths**:
- B2B SaaS-focused
- Organization management built-in
- Enterprise SSO included (no per-connection fees)
- Simple, transparent pricing
- Pre-built B2B components (org switcher, team management)

**Pricing**: Free (1K MAU) | Hobby $49/mo | Starter $249/mo (10K MAU) | Growth custom

**Best For**: B2B SaaS companies, organization-based apps, enterprise SSO without extra fees

**Limitations**: Young company (2022), B2B-specific (not ideal for B2C), smaller community, limited track record

---

## 12. SELECTION CRITERIA FRAMEWORK

### 12.1 Decision Tree Factors

**Authentication Model**:
- Password-based → Auth0, Clerk, Supabase, Keycloak, FusionAuth
- Passwordless-first → Stytch, Magic, Hanko, Passage
- Passkey-only → Passage, Hanko
- Hybrid (both) → Clerk, Auth0, Stytch, Descope

**Business Model**:
- B2C consumer apps → Stytch, Clerk, Firebase, Supabase
- B2B SaaS → WorkOS, Clerk, PropelAuth, Auth0
- Enterprise IAM → Auth0, Keycloak, Ory, FusionAuth
- Mobile-first → Firebase, Auth0, Clerk, Stytch

**Scale**:
- 0-50K MAU → Supabase (free), Firebase (free), Clerk (free), Cognito (free)
- 50K-200K MAU → Clerk, Cognito, Supabase, Descope
- 200K-1M MAU → Cognito, Clerk, Auth0 (negotiate)
- 1M+ MAU → Cognito, Auth0 (enterprise), Keycloak (self-host)

**Enterprise Requirements**:
- Enterprise SSO (SAML/OIDC) → WorkOS, Auth0, Clerk, Keycloak, PropelAuth
- SCIM/Directory Sync → WorkOS, Auth0
- Multi-tenancy → Clerk, PropelAuth, Auth0, Keycloak (Realms)
- Compliance (HIPAA) → Cognito, Firebase, Auth0 (Enterprise)

**Technical Preferences**:
- Open-source → Keycloak, Ory, Supabase, SuperTokens, Hanko
- Self-hosted → Keycloak, Ory, FusionAuth, SuperTokens, Supabase
- Managed/SaaS → Clerk, Auth0, Stytch, WorkOS, Descope
- Headless/API-first → Supabase, Ory, SuperTokens

**Development Stack**:
- React/Next.js → Clerk, Supabase, Auth0, Descope
- Mobile (iOS/Android) → Firebase, Auth0, Clerk, Stytch
- AWS ecosystem → Cognito
- Google Cloud → Firebase
- Multi-cloud → Auth0, Clerk, Supabase, Ory

**Geographic/Compliance**:
- EU/GDPR-first → Ory, Hanko, Supabase (EU), Keycloak (self-host)
- US-based → Cognito, Auth0, Clerk, Stytch
- Global multi-region → Auth0, Supabase, Cognito, Firebase

**Budget**:
- Free/minimal → Supabase, Firebase, Keycloak, Ory (self-host)
- Budget-conscious → Clerk, Cognito, Supabase, Descope
- Mid-market → Auth0, Stytch, WorkOS, PropelAuth
- Enterprise (custom) → Auth0, Cognito (scale), Keycloak

### 12.2 Cost Analysis Templates

**Scenario 1: Early-Stage Startup (10K MAU, B2C)**

| Provider | Monthly Cost | Setup Time | Maintenance | Features | Recommendation |
|----------|--------------|------------|-------------|----------|----------------|
| Firebase | $0 | 2 hours | Low | Mobile-focused, limited enterprise | Best for mobile MVP |
| Supabase | $0 | 3 hours | Low | Full-stack, PostgreSQL | Best for full-stack apps |
| Clerk | $0 (free tier) | 1 hour | Very Low | Modern UI, orgs | Best for React SaaS |
| Cognito | $0 | 6 hours | Medium | AWS integration | Best if on AWS |

**Scenario 2: Growing SaaS (100K MAU, B2B with SSO)**

| Provider | Monthly Cost | SSO (5 connections) | Total | Features | Recommendation |
|----------|--------------|---------------------|-------|----------|----------------|
| Clerk | $199 | $495 ($99 x 5) | $694 | Orgs, modern DX | Best DX, React-focused |
| WorkOS | $0 (auth free) | $625 ($125 x 5) | $625 | Purpose-built SSO | Best for SSO-primary |
| PropelAuth | ~$1,500 (custom) | Included | ~$1,500 | B2B features | Best all-in pricing |
| Auth0 | $2,280+ (Essentials) | Enterprise only | $2,280+ | Most comprehensive | Most expensive, overkill |
| Cognito | $550 | Included | $550 | AWS integration | Cheapest, DIY setup |

**Scenario 3: Enterprise Scale (1M MAU, Compliance)**

| Provider | Monthly Cost | Compliance | Support | Total/Year | Recommendation |
|----------|--------------|------------|---------|------------|----------------|
| Cognito | $5,500 | HIPAA, FedRAMP | AWS Support ($100-1K/mo) | $66K-78K | Most cost-effective |
| Auth0 | Custom (~$10-20K/mo) | All certs, BAA | Included (Enterprise) | $120-240K | Most comprehensive |
| Keycloak | $0 (self-host) + infra | Self-managed | Red Hat SSO (custom) | $24-60K | Most control, complex |

### 12.3 Feature Priority Matrix

**Must-Have Features**:
- [ ] Email/Password authentication
- [ ] Social login (Google, GitHub, etc.)
- [ ] Email verification
- [ ] Password reset
- [ ] MFA/2FA support
- [ ] Session management
- [ ] User profile management

**Nice-to-Have Features**:
- [ ] Passwordless (magic link, OTP)
- [ ] WebAuthn/Passkeys
- [ ] Organizations/multi-tenancy
- [ ] Enterprise SSO (SAML/OIDC)
- [ ] Pre-built UI components
- [ ] Mobile SDKs
- [ ] Audit logs

**Enterprise Features**:
- [ ] SCIM/Directory sync
- [ ] Advanced MFA (hardware tokens, biometric)
- [ ] Risk-based authentication
- [ ] Custom domains
- [ ] SLA guarantees
- [ ] Dedicated support
- [ ] HIPAA/SOC 2/ISO 27001

**Map providers to your priorities**:
- High DX + React → **Clerk**
- Passwordless-first → **Stytch, Hanko**
- Enterprise SSO → **WorkOS, Auth0**
- Cost-optimized → **Cognito, Supabase**
- Open-source → **Keycloak, Ory**

---

## 13. SYNTHESIS PREPARATION NOTES

### 13.1 Data Quality Assessment

**Highly Reliable Data**:
- Auth0, Clerk, Supabase, Firebase, Cognito (official docs, public pricing)
- Compliance certifications (public audit reports)
- Protocol support (documented standards)
- SDK availability (GitHub repositories)

**Partially Reliable Data**:
- User-reported experiences (Reddit, HackerNews, reviews)
- Pricing at scale (custom deals, not public)
- Enterprise features (gated behind sales)
- Actual setup time (varies by use case)

**Gaps Requiring Further Investigation**:
- Real-world SSO integration complexity beyond docs
- Actual support quality (response times, resolution rates)
- Migration difficulty (provider-to-provider)
- Hidden costs (overages, add-ons, support)
- Long-term viability (Passage/1Password, Descope, PropelAuth)

### 13.2 Market Trends Observed

1. **Passwordless Growth**: Shift toward passwordless (Stytch, Magic, Hanko, Passage) - 2020-2025 wave
2. **Passkey Adoption**: WebAuthn/FIDO2 becoming standard (Apple, Google, Microsoft push)
3. **Consolidation**: Okta acquired Auth0 ($6.5B, 2021), 1Password acquired Passage (2023)
4. **B2B SaaS Focus**: Purpose-built B2B auth (WorkOS, PropelAuth, Clerk orgs)
5. **Open-Source Renaissance**: Supabase, Ory, Hanko, SuperTokens - developer preference for OSS
6. **Developer Experience**: Clerk setting new bar for DX (pre-built components, docs, React-first)
7. **Cost Optimization**: Cognito dominance at scale, free tiers expanding (Clerk 10K, Supabase 50K)
8. **Compliance Commoditization**: SOC 2/ISO 27001 becoming table stakes
9. **Multi-Cloud**: Moving away from cloud-specific (Firebase/AWS) to multi-cloud (Clerk, Auth0, Supabase)
10. **Visual/No-Code**: Descope-style flow builders gaining traction

### 13.3 Provider Viability Assessment

**Established (Low Risk)**:
- Auth0 (Okta), Firebase (Google), Cognito (AWS), Keycloak (Red Hat/IBM)
- Track record: 10+ years, large customer bases, corporate backing

**Growth Stage (Medium Risk)**:
- Clerk, Supabase, Ory, WorkOS, Stytch
- VC-backed, growing rapidly, 3-5 years old, strong market traction

**Early Stage (Higher Risk)**:
- Descope, PropelAuth, Hanko (all 2022-founded)
- Limited track record, smaller teams, early customers

**Acquired/Integration Risk**:
- Passage (1Password, 2023) - integration path unclear
- Magic - smaller player, Web3 focus (niche)

**Open-Source (Sustainability Risk)**:
- SuperTokens, Hanko - smaller communities, monetization unclear
- Ory - strong funding, clearer monetization (managed cloud)
- Keycloak - Red Hat backing (sustainable)

### 13.4 Recommended Deep-Dive Areas for S3 (Need-Driven Discovery)

Potential S3 scenarios:
1. Early-stage SaaS (React/Next.js, 0-50K MAU, B2C)
2. B2B SaaS selling to enterprises (SSO required, 50-200K MAU)
3. Mobile-first consumer app (iOS/Android, social login, 100K+ MAU)
4. Fintech/healthcare (compliance-critical, HIPAA, passwordless)
5. Enterprise replacing legacy IAM (Keycloak/Ory vs Auth0/Okta)
6. Open-source platform (self-hosted, zero lock-in requirement)

---

## CONCLUSION

This comprehensive discovery analyzed **16 major authentication and authorization providers** across:
- Feature comparison matrices (auth methods, authorization, session management, user management, security)
- Pricing models (MAU-based, self-hosted, add-ons, TCO analysis)
- Compliance certifications (SOC 2, ISO 27001, GDPR, HIPAA, FedRAMP)
- Integration patterns (SDKs, frameworks, pre-built UI, API design, documentation)
- Passwordless authentication (magic links, OTP, WebAuthn, passkeys, biometrics)
- Enterprise features (SSO, SCIM, organizations, multi-tenancy, audit logs)
- Lock-in assessment (data portability, migration complexity, protocol standards)
- Developer experience (setup time, customization, maintenance, support)

**Key Findings**:

**By Use Case**:
- **Modern SaaS (React/Next.js)**: Clerk (best DX, components) | Supabase (open-source, cost-effective)
- **B2B Enterprise SSO**: WorkOS (purpose-built) | Auth0 (comprehensive) | PropelAuth (all-in pricing)
- **Mobile-First**: Firebase (best mobile SDKs) | Auth0 (multi-platform) | Clerk (React Native)
- **Passwordless**: Stytch (comprehensive) | Hanko (passkey-first, OSS) | Passage (biometric)
- **Cost Optimization**: Cognito ($0.0055/MAU at scale) | Supabase (50K free) | Keycloak (free OSS)
- **Open-Source**: Keycloak (most features) | Ory (modern, headless) | Supabase (PostgreSQL-native)
- **Enterprise Self-Hosted**: Keycloak (most complete) | FusionAuth (simpler) | Ory (GDPR-native)

**By Scale**:
- **0-50K MAU**: Supabase, Firebase, Clerk (generous free tiers)
- **50K-200K MAU**: Clerk, Cognito, Descope (best price/features)
- **200K-1M MAU**: Cognito, Clerk, Auth0 (negotiate)
- **1M+ MAU**: Cognito (best economics), Auth0 (enterprise), Keycloak (self-hosted)

**Critical Trade-offs**:
- **Managed Simplicity** (Clerk, Descope, Stytch) vs **Self-Hosted Control** (Keycloak, Ory, Supabase)
- **Fast Setup** (Clerk, Descope, Magic) vs **Full Customization** (Keycloak, Ory, Auth0)
- **Cost** (Cognito $0.0055/MAU, Supabase free 50K) vs **Features** (Auth0 $2,280/mo for 100K)
- **Passwordless Modern** (Stytch, Hanko, Passage) vs **Traditional Flexibility** (Auth0, Clerk, Keycloak)
- **B2B SSO Focus** (WorkOS, PropelAuth) vs **B2C Consumer** (Stytch, Firebase, Magic)
- **Zero Lock-in** (Keycloak, Ory, open standards) vs **Vendor Integration** (Firebase, Clerk, Auth0)

**Emerging Trends**:
- Passkeys/WebAuthn becoming mainstream (Passage, Hanko, Clerk, Stytch)
- Developer experience as key differentiator (Clerk setting new standard)
- Open-source gaining traction (Supabase, Ory, Hanko, SuperTokens)
- B2B SaaS-specific auth (WorkOS, PropelAuth, Clerk organizations)
- Visual/no-code auth flows (Descope)
- Cost optimization driving Cognito adoption at scale

The authentication landscape offers solutions for every scale, budget, and technical requirement. Selection depends heavily on:
1. **Use case** (B2C vs B2B, mobile vs web)
2. **Scale** (MAU tier, growth trajectory)
3. **Technical preferences** (managed vs self-hosted, React vs framework-agnostic)
4. **Enterprise needs** (SSO, compliance, support SLAs)
5. **Budget** (free tiers vs scale economics vs enterprise deals)
6. **Lock-in tolerance** (open-source portability vs managed convenience)

**Recommendation**: Start with generous free tiers (Supabase 50K, Clerk 10K, Firebase unlimited) for MVP. Evaluate based on your stack (Clerk for React, Firebase for mobile, Cognito for AWS). Plan migration to cost-optimized solutions (Cognito, Keycloak) or enterprise platforms (Auth0, WorkOS) as you scale and requirements evolve.
