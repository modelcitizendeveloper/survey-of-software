# Authentication & Authorization Services: Business-Focused Explainer

**Target Audience**: CTOs, Engineering Directors, Product Managers with MBA/Finance backgrounds, Solo Founders
**Business Impact**: Authentication infrastructure directly affects user activation (40% drop if password reset emails fail), security breach costs ($200K-5M per incident), and engineering velocity (60-120 hours saved vs DIY implementation)

**Purpose**: This EXPLAINER explains the technical complexity of authentication & authorization and why specialized services exist to solve these problems. It does NOT compare specific providers—that analysis is in S1-S4 discovery files.

---

## What Problem Does Authentication Solve?

**Simple Definition**: Authentication verifies "who you are" (login), while authorization determines "what you can access" (permissions). Authentication services handle the entire user identity lifecycle—from signup through login, password recovery, multi-factor authentication, single sign-on, session management, and security monitoring.

**The DIY Challenge**: Building authentication yourself means implementing:
- Password hashing (bcrypt/Argon2) with salt generation and secure storage
- Session management across multiple devices with token rotation
- OAuth 2.0 flows for social login (Google, GitHub, Apple)
- Email verification and password reset workflows
- Multi-factor authentication (SMS, TOTP, WebAuthn/passkeys)
- Brute force protection and rate limiting
- Account recovery flows and suspicious login detection
- Enterprise SSO (SAML 2.0, OIDC) for B2B customers
- RBAC (role-based access control) and organization/team management
- GDPR compliance (consent, data retention, audit logs, breach notification)
- WebAuthn/FIDO2 for passwordless biometric authentication

**Why Services Exist**: Authentication providers employ security specialists, maintain compliance certifications (SOC 2, ISO 27001, HIPAA), handle attack prevention infrastructure (credential stuffing, account takeover, bot detection), and manage relationships with social login providers. They absorb the burden of:
- 24/7 security monitoring and incident response
- Compliance audits (SOC 2 Type II costs $15K-50K annually for audit alone)
- Protocol implementation (OAuth 2.0, OIDC, SAML, WebAuthn standards evolve)
- Multi-region infrastructure (data residency for GDPR, latency optimization)
- Attack surface management (credential stuffing databases, breach detection)

**In Finance Terms**: Like using a payment processor (Stripe) instead of becoming a bank. Technically possible to build your own auth, but the regulatory burden, security expertise, and ongoing operational cost make "buy" the rational choice for most companies.

**Business Priority**: Critical from day one—every user interaction requires authentication. Poor authentication UX directly impacts activation rates (passwordless reduces friction 40-60%), while security breaches erode customer trust and trigger regulatory fines ($50K-500K for GDPR violations, $200K-5M for data breaches).

---

## The Technical Complexity Beneath the Surface

### Infrastructure Requirements

- **Session Management**: Distributed session stores (Redis, DynamoDB), token rotation to prevent replay attacks, multi-device session tracking, session revocation on logout/password change, concurrent session limits for security
- **Token Handling**: JWT generation and validation, refresh token rotation (prevent token theft), secure storage (HttpOnly cookies vs localStorage), token expiration and renewal flows, cryptographic signing (RS256, HS256)
- **Password Security**: Bcrypt/Argon2 hashing with configurable work factors, salt generation and storage, password strength enforcement, breached password detection (Have I Been Pwned integration), password history to prevent reuse
- **Multi-Device Management**: Device fingerprinting, trusted device recognition, cross-device authentication flows (QR code, magic links), device revocation capabilities, "where you're logged in" management UI

### Operational Challenges

- **Account Recovery**: Email verification flows (verify on signup or lazy verification), password reset token generation with expiration, account lockout after failed attempts, security questions (deprecated but still used), backup codes for MFA recovery
- **Suspicious Login Detection**: Impossible travel detection (login from US then China 10 minutes later), new device notifications, IP reputation scoring, behavioral biometrics, velocity checks (rate of login attempts)
- **Attack Prevention**: Credential stuffing defense (credential breach databases), brute force protection (exponential backoff, CAPTCHA), bot detection (reCAPTCHA, hCaptcha), account takeover prevention, rate limiting per IP/user/device
- **Email Deliverability**: Transactional email infrastructure for password resets, verification links, suspicious login alerts—email deliverability issues mean users can't log in (40% activation drop)

### Compliance & Standards

- **GDPR (EU Data Protection)**: User consent management, right to deletion (user data export and purge), data retention policies, breach notification within 72 hours, data processing agreements with vendors
- **SOC 2 Type II**: Security, availability, processing integrity, confidentiality, privacy controls—annual audits cost $15K-50K, implementation requires dedicated security personnel
- **HIPAA (Healthcare)**: Business Associate Agreement (BAA) required, encrypted PHI (Protected Health Information) storage, audit logs for all access, secure session handling, breach notification
- **OAuth 2.0 / OIDC**: Standard delegation protocol (login with Google/GitHub), authorization code flow, PKCE (Proof Key for Code Exchange) for mobile, refresh tokens, scope management
- **SAML 2.0**: Enterprise SSO standard (Okta, Azure AD), XML-based assertions, IdP (Identity Provider) and SP (Service Provider) configuration, certificate management, JIT (Just-In-Time) provisioning
- **WebAuthn / FIDO2**: Passwordless standard using biometrics or hardware keys, public key cryptography, phishing-resistant, device attestation, passkey sync across devices

**Why This Matters**: Security breaches cost $200K-5M (incident response, customer notification, regulatory fines, reputation damage). GDPR fines reach 4% of global revenue. Compliance gaps block enterprise sales (no SSO = no deal with Fortune 500).

**In Finance Terms**: Like maintaining banking licenses across 50 jurisdictions vs using a payment processor that handles compliance. The specialized expertise and audit costs make DIY economically irrational below 10M+ users.

---

## Build vs Buy Economics

### What "Building It Yourself" Really Means

**Required Components**:
- Authentication server (Node.js/Go/Python backend with auth endpoints)
- User database (PostgreSQL/MySQL with encrypted password storage)
- Session store (Redis for fast session lookup)
- Email service integration (Sendgrid/Postmark for transactional emails)
- OAuth client implementations (Google/GitHub/Apple social login SDKs)
- MFA infrastructure (TOTP secret generation, SMS gateway, WebAuthn library)
- Admin dashboard (user management, security monitoring)

**Hidden Complexity**:
- Password reset flows take 40-60 hours to implement correctly (token generation, expiration, email templates, security edge cases)
- OAuth 2.0 social login requires 20-40 hours per provider (Google, GitHub, Apple have different implementations)
- Session management across web + mobile + API requires distributed session store and token refresh logic (60-80 hours)
- Account recovery edge cases (email changed, phone number changed, MFA device lost) require careful UX and security design (40-60 hours)
- Security monitoring and attack prevention (rate limiting, suspicious login detection, breach response) is ongoing operational burden (10-20 hours/month)

**Ongoing Operational Burden**:
- Security patches and protocol updates (OAuth, OIDC, SAML standards evolve—20-40 hours/quarter)
- Compliance audits (SOC 2 requires annual audit, GDPR requires ongoing monitoring—$15K-50K/year external audit + 1-2 FTE internal)
- Monitoring and incident response (24/7 on-call for auth outages, breach detection—requires dedicated team at scale)
- Social login provider changes (Google/Apple update APIs, deprecate features—10-20 hours/quarter maintenance)

**Realistic Time Investment**:
- **Initial Setup**: 200-400 hours of engineering time (basic email/password + social login + session management)
- **Production Hardening**: Additional 100-200 hours (security edge cases, compliance, monitoring)
- **Ongoing Maintenance**: 40-80 hours/quarter (security patches, provider changes, compliance updates)
- **Expertise Required**: Security engineer familiar with cryptography, OAuth/OIDC, OWASP Top 10, compliance frameworks

**When DIY Makes Sense**: Rare cases at 10M+ MAU where provider costs exceed $100K/year AND you have dedicated auth/security team (2-5 FTE). Examples: Fintech companies where auth IS the product (banking, identity verification), scale where provider costs become prohibitive (100M+ MAU), regulatory requirements demanding full control (government, defense).

**When Services Make Sense**: Under 10M MAU, or if auth is NOT your competitive advantage. Focus engineering resources on core product features, not reinventing authentication infrastructure. Provider costs ($6K-60K/year for 1M MAU) are less than 1 FTE ($200K+ fully loaded).

**In Finance Terms**: Like running your own datacenter vs using AWS—possible at massive scale (Netflix runs its own CDN), but economical threshold is extremely high. For authentication, break-even is 10M+ MAU or $100K+/year provider costs.

---

## ROI Impact: Why This Matters for Business

### Operational Efficiency Economics

- **Security Breach Avoidance**: DIY auth has 3-5x higher breach probability (lack of specialized expertise, slower patch response). Average breach cost: $200K-5M (incident response, customer notification, legal fees, regulatory fines, reputation damage). Provider absorbs this risk with dedicated security teams and insurance.
- **Engineering Velocity**: 60-120 hours saved on initial implementation, 40-80 hours/quarter on ongoing maintenance. At $200/hour fully loaded engineer cost, that's $12K-24K initial savings, $32K-64K/year ongoing. Reallocate engineering time to revenue-generating features.
- **Compliance Acceleration**: Providers maintain SOC 2, ISO 27001, HIPAA certifications. DIY requires $15K-50K/year external audit + 0.5-1 FTE internal ($50K-150K/year). Providers amortize audit costs across thousands of customers, making per-customer cost negligible.
- **Scale Economics**: Providers handle 1M MAU for $6K-60K/year. DIY costs: 2-3 FTE engineers ($400K-600K/year) + infrastructure ($10K-50K/year) + compliance ($50K-100K/year) = $460K-750K/year. DIY only makes sense when provider costs exceed this threshold (10M+ MAU at $0.05/MAU = $500K+/year).

### Strategic Value Creation

- **User Activation**: Passwordless authentication (magic links, passkeys) reduces signup friction by 40-60%, directly improving activation rates. Email verification that lands in spam = 40% drop in activation. Providers manage email deliverability and anti-spam infrastructure.
- **Enterprise Sales Enablement**: Enterprise SSO (SAML, OIDC) is table stakes for Fortune 500 sales. DIY SAML implementation takes 60-100 hours. Providers offer pre-built IdP integrations (Okta, Azure AD, Google Workspace) in minutes. SSO capability unlocks $100K+ enterprise deals.
- **Passwordless Evolution**: WebAuthn/passkeys are becoming standard (Apple, Google, Microsoft push). Regulatory mandates emerging (NIST, FIDO Alliance) for phishing-resistant authentication in fintech/healthcare by 2027-2028. Providers invest in passkey infrastructure, saving you 40-80 hours retrofitting.
- **Risk Mitigation**: Account takeover (credential stuffing) costs average $200 per incident (fraud, refunds, customer support). Providers detect and block 99%+ of credential stuffing attempts using breach databases and behavioral analysis. DIY has no access to these databases.

**Bottom Line**: Authentication directly affects three business metrics: (1) Activation rate (passwordless reduces friction 40-60%), (2) Security risk ($200K-5M breach cost), (3) Enterprise sales velocity (SSO unlocks $100K+ deals). Providers deliver ROI through avoided breach costs, engineering time savings, and faster enterprise sales.

**In Finance Terms**: Authentication is infrastructure, not differentiation. Like using AWS instead of building datacenters, or Stripe instead of becoming a payment processor. Outsource commodity infrastructure to specialists, focus limited resources on competitive advantage (your product features).

---

## Generic Use Case Applications

### Use Case Pattern #1: SaaS Application (B2C or B2B)
**Problem**: Need secure user authentication with email/password, social login (Google, GitHub), password reset, and email verification.
**Technical Challenge**: Password reset emails flagged as spam = users can't log in = 40% activation drop. Implementing OAuth correctly for each provider (Google, Apple, GitHub) takes 20-40 hours per provider with different redirect flows and token handling.
**Business Impact**: 1% improvement in email deliverability = 500 fewer support tickets/month for 50K MAU app. Social login reduces signup friction by 40%, improving conversion rates.

**Example Applications**: Project management tools (Linear, Asana), developer tools (Vercel, Railway), productivity apps (Notion, Coda)

### Use Case Pattern #2: Enterprise B2B with SSO Requirements
**Problem**: Enterprise customers (Fortune 500) require SAML or OIDC SSO to integrate with their identity provider (Okta, Azure AD, Google Workspace).
**Technical Challenge**: SAML implementation takes 60-100 hours (XML parsing, certificate management, IdP metadata configuration, JIT provisioning). Each enterprise customer may have different IdP with unique configuration quirks.
**Business Impact**: SSO capability unlocks $100K-1M enterprise deals. Without SSO, unable to sell to 60-70% of Fortune 500 companies (mandatory security requirement). DIY SAML = 60-100 hours per integration, providers offer pre-built IdP connectors in minutes.

**Example Applications**: B2B SaaS selling to enterprises (Slack, Zoom, Salesforce), multi-tenant platforms with organization management

### Use Case Pattern #3: Mobile-First Consumer Applications
**Problem**: Need low-friction signup for consumer mobile apps with social login (Google, Apple) and passwordless options (magic links, biometric).
**Technical Challenge**: Mobile OAuth flows differ from web (custom URL schemes, app-to-app redirects). Biometric authentication (Touch ID, Face ID) requires native SDK integration and secure storage. Password friction causes 40-60% signup abandonment.
**Business Impact**: Passwordless reduces signup friction by 40-60%, directly improving activation. Social login (one-tap Google Sign-In on Android) increases conversion 30-50% vs manual email/password.

**Example Applications**: Gaming apps, social apps, fitness tracking, fintech consumer apps

### Use Case Pattern #4: Compliance-Heavy Industries (Healthcare, Finance)
**Problem**: HIPAA or financial regulations require encrypted PHI storage, audit logs, breach notification, BAA (Business Associate Agreement).
**Technical Challenge**: HIPAA compliance requires encrypted user data, comprehensive audit logs, breach notification procedures, annual security audits. DIY compliance costs $50K-150K/year (external audit + internal FTE). One security gap = $50K-500K regulatory fine.
**Business Impact**: Providers offer HIPAA-compliant infrastructure with BAA, SOC 2 Type II, ISO 27001 certifications. Instant compliance vs 6-12 months DIY implementation + ongoing audit burden.

**Example Applications**: Healthcare platforms, telemedicine, patient portals, fintech, banking applications

**In Finance Terms**: Use cases map to company scale and industry regulation. Consumer apps prioritize low friction (passwordless), B2B SaaS needs enterprise features (SSO, multi-tenancy), regulated industries require compliance (HIPAA, SOC 2). Providers offer vertical-specific solutions, avoiding one-size-fits-all DIY complexity.

---

## When Do You Need This Service?

### Early Stage / MVP
**Trigger**: Day one—every user interaction requires authentication. First transactional email (signup confirmation) sent.
**Technical Reality**: DIY email from application server lands in spam 70% of the time. Users don't receive verification emails = activation failure. OAuth social login takes 20-40 hours per provider to implement correctly.
**Cost of Delay**: Users who don't receive signup email = lost conversions. Security vulnerability in DIY auth = breach risk from day one. Opportunity cost: 100-200 hours building auth vs building product features.

### Growth Stage
**Trigger**: Sending 1K+ auth emails/day (password resets, verification). Enterprise sales prospects require SSO. User complaints about security (compromised passwords, account takeovers).
**Technical Complexity**: Managing email deliverability across providers, implementing SAML for enterprise SSO (60-100 hours per integration), adding MFA (40-60 hours), passwordless options (40-80 hours), compliance requirements (SOC 2 audit for enterprise sales).
**Cost of DIY**: 15-20 hours/week managing auth issues vs building features. Security incidents increase (credential stuffing, account takeover). Enterprise sales blocked without SSO capability.

### Enterprise Scale
**Trigger**: Multi-region compliance (GDPR data residency), dedicated IP pools for email, advanced segmentation, 100K+ MAU scale, enterprise customers demanding SAML, SCIM directory sync.
**Technical Requirements**: HIPAA-compliant infrastructure with BAA, multi-region deployment (EU data residency), audit logs for compliance, guaranteed SLAs (99.9%+ uptime), dedicated support for enterprise customers.
**Strategic Considerations**: At 10M+ MAU, provider costs reach $60K-600K/year (depending on provider). Evaluate DIY if auth team exists (2-5 FTE) and provider costs exceed DIY total cost ($460K-750K/year). Otherwise, negotiate enterprise contracts (30-50% discounts at scale).

---

## Key Decision Factors (See S1-S4 for Provider Analysis)

**What to Evaluate When Choosing a Service**:
1. **Pricing model transparency**: Avoid opaque pricing that increases at scale (growth penalty). Prefer per-MAU pricing with published rates vs "contact sales" (price negotiation overhead).
2. **Lock-in risk and data portability**: Can you export users with password hashes? Does provider use standard protocols (OIDC, SAML) or proprietary APIs? Migration complexity: 60-200 hours depending on vendor.
3. **Compliance certifications**: SOC 2 Type II (table stakes for B2B SaaS), ISO 27001, HIPAA/BAA (healthcare), GDPR compliance (EU data residency options). Verify audit reports, not just self-attestation.
4. **Enterprise features roadmap**: SSO (SAML, OIDC), SCIM directory sync, multi-tenancy/organizations, advanced security (adaptive MFA, risk-based auth), audit logs. Evaluate current capabilities AND roadmap (passwordless, passkeys coming 2025-2028).

**Note**: Detailed provider comparisons, pricing analysis, and recommendations are in S1_RAPID_DISCOVERY.md, S2_COMPREHENSIVE_DISCOVERY.md, S3_NEED_DRIVEN_DISCOVERY.md, S4_STRATEGIC_DISCOVERY.md, and DISCOVERY_SYNTHESIS.md.

---

## Technical Deep Dive: What Makes Authentication Hard?

### Session Management Complexity
**The Challenge**: Distributed systems require coordinated session state. User logs in on web, session must work on mobile app. User logs out on one device, session must invalidate on all devices instantly. Token theft (XSS, MITM) requires token rotation to limit exposure window.

**DIY Requirements**:
- Distributed session store (Redis cluster for fast lookup across servers)
- Token rotation on every request or time-based (prevent replay attacks)
- Multi-device tracking (user can see "where you're logged in" and revoke devices)
- Session revocation on password change or logout (invalidate all sessions)
- Refresh token mechanism (short-lived access tokens + long-lived refresh tokens)

**Service Provider Value**: Providers manage distributed session infrastructure, automatic token rotation, multi-device session tracking UI, instant session revocation across all servers globally. You call a logout API, provider handles distributed invalidation.

### OAuth & Social Login Implementation
**The Challenge**: Each provider (Google, Apple, GitHub, Microsoft) has different OAuth flows, redirect URLs, token formats, and API changes. Google deprecated Google+ Sign-In in 2019, requiring migration to new Google Sign-In. Apple requires Sign In with Apple for iOS apps using social login.

**DIY Requirements**:
- OAuth 2.0 client implementation for each provider (authorization code flow, state parameter for CSRF protection)
- Provider-specific SDKs (Google Sign-In SDK, Apple Sign-In, GitHub OAuth app)
- Redirect URL configuration and callback handling (web vs mobile deep links)
- Token exchange and user info retrieval (different endpoints per provider)
- Account linking (user signs in with Google, later with email—link accounts)
- Migration when providers deprecate APIs (Google+ Sign-In, Facebook API changes)

**Service Provider Value**: Pre-built integrations for 20-30 social providers, automatic API version updates, account linking UI, migration support when providers change. Provider absorbs the burden of maintaining OAuth clients for every social login service.

### Passwordless & Passkey Infrastructure
**The Challenge**: WebAuthn/FIDO2 standard is complex—public key cryptography, device attestation, challenge-response flows, credential storage, backup credentials, cross-device authentication (QR codes for passkey sync).

**DIY Requirements**:
- WebAuthn server library (challenge generation, attestation verification, credential storage)
- Client-side JavaScript (navigator.credentials.create, navigator.credentials.get)
- Secure credential storage (public keys in database, private keys in device secure enclave)
- Backup authentication methods (user loses passkey device, needs recovery flow)
- Cross-device authentication (register passkey on phone, use on desktop)
- Conditional UI (autofill passkeys in login form)

**Service Provider Value**: Pre-built passkey registration and authentication flows, secure credential storage, backup recovery mechanisms, cross-device passkey sync, conditional UI support, device attestation verification. Providers invest in passkey UX research, saving you months of trial-and-error.

**In Finance Terms**: Like payment processing—technically possible to integrate with Visa/Mastercard directly, but specialized providers (Stripe) handle protocol complexity, compliance, and provider relationships. Authentication providers do the same for OAuth, SAML, WebAuthn standards.

---

## Common Misconceptions About Authentication

**Misconception #1**: "Authentication is simple—just hash passwords and store in database"
- **Reality**: Password hashing is 5% of authentication. Session management, password reset flows, OAuth social login, MFA, account recovery, security monitoring, compliance are 95% of complexity. DIY auth takes 200-400 hours initial + 40-80 hours/quarter maintenance.
- **Business Impact**: Security breach from DIY auth mistakes costs $200K-5M (incident response, customer notification, regulatory fines, reputation damage). Providers employ security specialists, undergo annual audits, maintain breach insurance.

**Misconception #2**: "DIY authentication saves money vs paying $0.02-0.05 per user"
- **Reality**: Provider costs at 1M MAU: $6K-60K/year (depending on provider). DIY costs: 2-3 FTE engineers ($400K-600K/year) + infrastructure ($10K-50K/year) + compliance audits ($50K-100K/year) = $460K-750K/year total. DIY only cheaper after 10M+ MAU.
- **Business Impact**: Opportunity cost of 200-400 hours initial + 40-80 hours/quarter = 360-720 hours/year not building product features. At $200/hour, that's $72K-144K/year engineering time reallocated from revenue-generating work.

**Misconception #3**: "Vendor lock-in doesn't matter—we'll migrate if needed"
- **Reality**: Authentication migration takes 60-200 hours depending on vendor lock-in (proprietary APIs, password hash export restrictions, custom logic migration). High-risk operation—users can't log in during migration = business-critical outage.
- **Business Impact**: Migration during growth phase (when costs spike) is worst-case timing—high user volume + high business risk. Choosing low-lock-in provider (standard protocols, data export) reduces future migration cost from 200 hours → 60-80 hours (50-60% reduction).

**Misconception #4**: "We can start with DIY and migrate to provider later"
- **Reality**: Migration from DIY to provider is HARDER than provider-to-provider migration. Password hash format differences (DIY uses Argon2, provider expects bcrypt), session token incompatibility, OAuth client re-registration, user communication ("verify your email again"). Takes 100-200 hours.
- **Business Impact**: Starting with provider saves 200-400 hours initial implementation + avoids 100-200 hour migration later. Total savings: 300-600 hours ($60K-120K at $200/hour). Use provider from day one unless auth IS your competitive advantage.

---

## Next Steps

1. **Read this EXPLAINER** to understand the technical complexity and business value of authentication services (you're here)
2. **Review S1_RAPID_DISCOVERY.md** for provider comparison and quick start recommendations (15-30 minutes)
3. **Consult S3_NEED_DRIVEN_DISCOVERY.md** for your specific use case fit analysis (15-20 minutes)
4. **Read DISCOVERY_SYNTHESIS.md** for decision framework and executive recommendations (15 minutes)
5. **Deep-dive S2 & S4** if needed for comprehensive pricing/feature analysis or strategic vendor assessment

**Total Time Investment**: 1-2 hours for informed decision

**Outcome**: Clear understanding of:
- Why authentication services exist (technical complexity: session management, OAuth, compliance, security monitoring)
- When DIY vs service makes sense (DIY only viable at 10M+ MAU OR $100K+/year provider costs)
- Which provider characteristics matter for your use case (pricing transparency, lock-in risk, compliance certifications, enterprise features)
- How to evaluate and select the right solution (avoid growth penalty pricing, minimize lock-in, verify compliance)

---

## Related Resources

**Provider Discovery & Selection** (experiments/3.012-authentication/01-discovery/):
- **S1_RAPID_DISCOVERY.md**: Top 8 providers, quick comparison, "get started this weekend" recommendation
- **S2_COMPREHENSIVE_DISCOVERY.md**: Complete provider matrix (16 providers), pricing models, feature comparison, compliance certifications
- **S3_NEED_DRIVEN_DISCOVERY.md**: 7 use case patterns (SaaS, B2B SSO, mobile, passwordless, compliance, consumer, dev tools) with provider fit analysis
- **S4_STRATEGIC_DISCOVERY.md**: Vendor viability, acquisition risk, market trends (passwordless timeline), long-term positioning, build vs buy inflection analysis
- **DISCOVERY_SYNTHESIS.md**: Decision frameworks, convergence analysis (all 4 methodologies agree on Clerk, Cognito, Auth0, Supabase), executive recommendations by stage

**Build vs Buy Decision** (covered in S4_STRATEGIC_DISCOVERY.md):
- Detailed TCO analysis: DIY costs $460K-750K/year vs provider $6K-60K/year for 1M MAU
- Break-even calculations: 10M+ MAU OR $100K+/year provider costs makes DIY viable
- Migration paths: Provider-to-provider (60-200 hours) vs DIY-to-provider (100-200 hours)

**DIY Implementation** (not recommended unless 10M+ MAU):
- If building custom: Open-source options (Keycloak, Ory, Supabase self-hosted) in experiments/3.012-authentication/01-discovery/S2_COMPREHENSIVE_DISCOVERY.md
- Self-hosted vs managed trade-offs: Full control vs operational burden (20-40 hours/quarter maintenance)

---

**Bottom Line**: Authentication is deceptively complex—session management across distributed systems, OAuth provider integrations, passwordless/passkey infrastructure, compliance requirements (GDPR, SOC 2, HIPAA), and security monitoring require specialized expertise that rarely justifies building in-house until you're processing 10M+ MAU or provider costs exceed $100K/year. Services exist because managing distributed sessions, social login provider relationships, compliance audits, and attack prevention infrastructure (credential stuffing databases, behavioral analysis) requires dedicated security teams that only make economic sense at massive scale. For most companies, $6K-60K/year provider cost is less than 1 FTE ($200K+ fully loaded), making "buy" the rational choice to focus engineering on competitive advantage (product features) rather than commodity infrastructure (authentication).
