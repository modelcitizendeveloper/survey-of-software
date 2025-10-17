# Section 0: Open Standards Evaluation

**Experiment**: 3.012 Authentication Services
**Tier 2 Standard**: 2.060 OAuth 2.0 / OIDC (Authentication Portability)
**Date**: October 17, 2025

---

## Does a Tier 2 Open Standard Exist?

✅ **YES** - **OAuth 2.0 / OpenID Connect (OIDC)** as authentication portability standards

**Standard Reference**: [2.060-oauth-oidc](../../2.060-oauth-oidc/)

**What they standardize**:
- **OAuth 2.0**: Authorization framework (access delegation)
- **OpenID Connect (OIDC)**: Identity layer on top of OAuth 2.0
- **Token formats**: JWT (JSON Web Tokens) for identity
- **Flows**: Authorization Code, PKCE, Client Credentials, Device Flow

**Governance**:
- OAuth 2.0: IETF RFC 6749 (2012)
- OIDC: OpenID Foundation (2014)
- JWT: IETF RFC 7519 (2015)

---

## Path 2 Viability Assessment

### Portability Level: ✅ **MEDIUM-to-HIGH**

**Standards-compliant providers** (20+ identity providers):
- **Open source**: Keycloak, Ory, Authentik, Authelia, Zitadel
- **Cloud providers**: AWS Cognito, Google Identity Platform, Azure AD B2C
- **Independent platforms**: Auth0, Okta, FusionAuth, SuperTokens
- **Social providers**: Google, GitHub, Facebook, Microsoft (OIDC federation)

### Migration Complexity

**Between OIDC providers** (Keycloak → Auth0):
- **Time**: 8-24 hours (reconfigure provider, test flows, migrate users)
- **Method**: Update OIDC endpoints, export/import users
- **Code changes**: MINIMAL (if using standard OIDC client library)
- **User migration**: 4-12 hours (export users, hash passwords, import)

**Lock-in risk**: **MEDIUM** (OIDC is standard, but user data migration has friction)

**Gotchas**:
- **Password hashing differs**: bcrypt vs Argon2 vs scrypt (need rehashing or password reset)
- **User attributes**: Custom claims, metadata formats vary
- **MFA implementation**: TOTP portable, but vendor-specific MFA (SMS, push) requires changes
- **Social connections**: OAuth app IDs must be reconfigured per provider
- **UI customization**: Login pages, emails need recreation

---

## Path 1 (DIY) vs Path 2 (Standard) vs Path 3 (Managed)

### Path 1: DIY Session-Based Auth

**What it is**: Roll your own authentication (session cookies, password hashing, email verification)

**Pros**:
- ✅ Full control (auth flow, database schema)
- ✅ Lowest cost ($0 for auth logic)
- ✅ No external dependencies

**Cons**:
- ❌ Security risk (easy to get wrong - password hashing, session fixation, CSRF)
- ❌ Missing features (MFA, OAuth social login, password reset flows)
- ❌ Maintenance burden (security patches, compliance - GDPR, SOC2)
- ❌ Time investment (40-120 hours to build securely)

**When to use**:
- Simple apps (username/password only, no social login)
- Learning exercise (understand auth fundamentals)
- Budget = $0 and can't afford managed auth

**Reality**: For production apps, DIY auth is HIGH RISK. Security vulnerabilities = data breaches = lawsuits.

**Recommendation**: If going DIY, use battle-tested libraries (Passport.js, django-allauth, Spring Security), don't write from scratch.

---

### Path 2: Self-Hosted OIDC Provider (Standards)

**What it is**: Run open-source OIDC server (Keycloak, Ory, Authentik)

**Pros**:
- ✅ MEDIUM lock-in (OIDC standard, can migrate to another provider)
- ✅ Full control (self-hosted, custom flows)
- ✅ Cost-effective ($50-200/month server costs)
- ✅ Standards-based (OIDC, OAuth 2.0, JWT)
- ✅ Social login (Google, GitHub, etc. via OIDC federation)
- ✅ MFA built-in (TOTP, WebAuthn)

**Cons**:
- ⚠️ Operational burden (server maintenance, security patches, scaling)
- ⚠️ Expertise required (OIDC configuration, token validation)
- ⚠️ User migration friction (password hashes, custom attributes)

**When to use**:
- Want portability (avoid vendor lock-in)
- Have technical team (can manage OIDC server)
- Medium-to-long-term project
- Budget-conscious ($50-200/month vs $1,000-10,000/month)

**Provider options**:

**Keycloak** (Red Hat, open source):
- **Cost**: $50-200/month (self-hosted server)
- **Pros**: Mature (15+ years), full OIDC/SAML, admin UI
- **Cons**: Heavy (Java, high memory), complex configuration

**Ory** (open source):
- **Cost**: $50-100/month (self-hosted, lightweight)
- **Pros**: Cloud-native (Go, K8s-ready), modern
- **Cons**: Steeper learning curve, less documentation

**Authentik** (open source):
- **Cost**: $50-100/month (self-hosted)
- **Pros**: User-friendly UI, modern, good docs
- **Cons**: Younger project (less mature than Keycloak)

---

### Path 3: Managed Auth Platforms (Proprietary + Managed)

**What it is**: Auth0, Okta, AWS Cognito - managed auth services

**Pros**:
- ✅ Managed convenience (zero ops burden)
- ✅ Turnkey features (MFA, social login, passwordless, bot detection)
- ✅ Compliance (SOC2, HIPAA, GDPR tools)
- ✅ Fast setup (30 minutes to production)
- ✅ Enterprise features (SSO, SAML, AD integration)

**Cons**:
- ⚠️ MEDIUM lock-in (OIDC portable, but user migration has friction)
- ⚠️ Expensive ($500-10,000+/month at scale)
- ⚠️ MAU-based pricing (unpredictable costs as users grow)
- ⚠️ Vendor-specific features (Actions, Hooks, Rules create soft lock-in)

**When to use**:
- Need managed convenience (no ops team)
- Want enterprise features (SSO, SAML, AD)
- Budget available ($500-10,000/month)
- Short-to-medium term project (portability less critical)

**Provider comparison**:

**Auth0** (Okta-owned):
- **Cost**: $240-1,400/month (1K-10K MAU), $0.05/MAU beyond
- **Pros**: Best developer experience, extensive docs, rules/hooks
- **Cons**: Expensive at scale, Okta acquisition creates uncertainty
- **Lock-in**: MEDIUM (OIDC standard, but Auth0 Actions proprietary)

**Okta**:
- **Cost**: $1,500-5,000/month (enterprise-focused)
- **Pros**: Enterprise-grade, SSO, SAML, AD integration
- **Cons**: Very expensive, overkill for small/mid-size
- **Lock-in**: MEDIUM (OIDC, but Okta Workflows proprietary)

**AWS Cognito**:
- **Cost**: $0.0055/MAU (first 50K free), $275/month for 50K MAU
- **Pros**: Cheap, integrates with AWS ecosystem
- **Cons**: Poor developer experience, limited customization, AWS lock-in
- **Lock-in**: MEDIUM-to-HIGH (OIDC standard, but AWS-specific integrations)

**Supabase Auth**:
- **Cost**: $25/month (unlimited MAU)
- **Pros**: Cheapest managed option, good DX, integrates with Supabase ecosystem
- **Cons**: Supabase-specific features (RLS integration) create soft lock-in
- **Lock-in**: MEDIUM (OIDC-based, but Supabase ecosystem lock-in)

---

## Decision Framework

### Choose Self-Hosted OIDC Provider (Path 2) if:

✅ **Portability is priority** (want to switch providers)
✅ **Technical team available** (can manage OIDC server)
✅ **Budget-conscious** ($50-200/month vs $500-10,000/month)
✅ **Medium-to-long-term project** (portability investment pays off)
✅ **Want control** (custom auth flows, branding)

**Recommended stack**:
- **Start simple**: Keycloak (mature, battle-tested)
- **Cloud-native**: Ory (Go, K8s-ready)
- **User-friendly**: Authentik (modern UI)

---

### Choose Managed Auth Platform (Path 3) if:

⚠️ **No ops team** (can't manage OIDC server)
⚠️ **Need enterprise features** (SSO, SAML, AD integration)
⚠️ **Fast time-to-market** (30 minutes vs 8-20 hours)
⚠️ **Budget available** ($500+/month)
⚠️ **Accept lock-in** (convenience > portability)

**Provider recommendation by use case**:

**Startup/SMB** (<10K users):
- **Choice**: Supabase Auth ($25/month unlimited MAU) or AWS Cognito ($0-275/month)
- **Why**: Cheapest managed options
- **Warning**: Supabase creates ecosystem lock-in, Cognito has poor DX

**Developer-focused** (10K-100K users):
- **Choice**: Auth0 ($240-1,400/month)
- **Why**: Best developer experience, extensive docs
- **Warning**: Expensive at scale ($0.05/MAU)

**Enterprise** (100K+ users, need SSO/SAML):
- **Choice**: Okta ($1,500-5,000/month)
- **Why**: Enterprise-grade features, compliance
- **Warning**: Very expensive

---

### DIY Session-Based Auth (Path 1) - NOT RECOMMENDED

❌ **Security risk**: Easy to get wrong (password hashing, session fixation, CSRF)
❌ **Missing features**: No MFA, social login, password reset out of the box
❌ **Maintenance burden**: Security patches, compliance

**Only use if**:
- Simple username/password auth (no social login, no MFA)
- Learning exercise
- Budget = $0 AND understand security risks

**If going DIY**: Use battle-tested libraries (Passport.js, django-allauth), NOT from scratch

---

## Migration Paths

### Scenario 1: Keycloak → Auth0 (Self-hosted → Managed)

**Motivation**: Reduce operational burden, get managed features

**Migration effort**: **12-24 hours**

**Steps**:
1. Create Auth0 tenant (1 hour)
2. Export users from Keycloak (2-4 hours)
   - Export user data (email, attributes)
   - Password hashes (bcrypt) - Auth0 supports import
3. Import users to Auth0 (4-8 hours)
   - Bulk import via Management API
   - Test password login
4. Update application OIDC config (2-4 hours)
   - Change issuer URL, client ID, client secret
   - Test login flows (authorization code, PKCE)
5. Reconfigure social connections (2-4 hours)
   - Google, GitHub OAuth apps (update redirect URIs)
6. Test MFA, password reset flows (1-2 hours)
7. Decommission Keycloak (1 hour)

**Code changes**: MINIMAL (if using standard OIDC client library)
**User impact**: Password reset required if password hashing differs

**Cost change**: $50-200/month → $240-1,400/month (5-7x increase for zero ops)

**When worth it**: Team spending >20 hours/month managing Keycloak

---

### Scenario 2: Auth0 → Keycloak (Managed → Self-hosted)

**Motivation**: Reduce costs (Auth0 $1,400/month → Keycloak $200/month)

**Migration effort**: **20-40 hours**

**Steps**:
1. Deploy Keycloak (2-4 hours)
2. Export users from Auth0 (4-8 hours)
   - Use Auth0 Management API to export users
   - Export password hashes (Auth0 supports bcrypt export)
3. Import users to Keycloak (8-16 hours)
   - Bulk import via Keycloak Admin API
   - Map Auth0 user attributes to Keycloak
4. Update application OIDC config (2-4 hours)
5. Reconfigure social connections (2-4 hours)
6. Recreate Auth0 Rules/Actions in Keycloak (4-8 hours)
   - Auth0 Rules → Keycloak Event Listeners/SPIs
7. Test thoroughly (4-8 hours)
8. Cancel Auth0 subscription

**Challenges**:
- Auth0 Actions/Rules proprietary (need recreation in Keycloak)
- Auth0 UI customization (need recreation in Keycloak themes)

**Cost savings**: $1,200/month ($14,400/year)
**ROI**: Migration pays for itself in 2 months

**When worth it**: Auth0 costs >$500/month, long-term project, have technical team

---

### Scenario 3: DIY Session Auth → Keycloak (DIY → Standards)

**Motivation**: Add MFA, social login, improve security

**Migration effort**: **40-80 hours**

**Steps**:
1. Deploy Keycloak (2-4 hours)
2. Migrate users (8-20 hours)
   - Export user data from your database
   - Hash format: bcrypt → Keycloak import (supported)
   - If different hash (e.g., MD5), force password reset
3. Rewrite auth logic (20-40 hours)
   - Remove DIY session management
   - Add OIDC client library (Passport.js, Spring Security)
   - Implement authorization code flow
4. Update frontend (8-16 hours)
   - Remove login forms
   - Add "Login with Keycloak" redirect
5. Test all auth flows (4-8 hours)
6. Remove DIY auth code (2-4 hours)

**Code changes**: EXTENSIVE (replace auth logic with OIDC)

**Benefit**: Gain MFA, social login, standards-based auth

---

### Scenario 4: AWS Cognito → Supabase Auth (Cloud → Independent)

**Motivation**: Better developer experience, reduce AWS lock-in

**Migration effort**: **12-24 hours**

**Steps**:
1. Create Supabase project (1 hour)
2. Export users from Cognito (2-4 hours)
3. Import users to Supabase (4-8 hours)
4. Update OIDC config (2-4 hours)
5. Reconfigure social connections (2-4 hours)
6. Test (2-4 hours)
7. Decommission Cognito (1 hour)

**Cost change**: $275/month (Cognito, 50K MAU) → $25/month (Supabase unlimited)
**Savings**: $250/month ($3,000/year)

**Trade-off**: Supabase ecosystem lock-in (RLS, Realtime, Storage)

---

## Provider-Specific Lock-in Risks

### Keycloak (Self-Hosted OIDC)

**Standard features** (portable):
- OAuth 2.0, OIDC (100% compliant)
- JWT tokens
- Social login (OIDC federation)

**Proprietary features** (lock-in):
- Keycloak themes (UI customization)
- Keycloak Event Listeners (custom logic)
- Keycloak SPIs (Service Provider Interfaces)

**Migration away**: 12-24 hours (reconfigure OIDC, export users)
**Lock-in level**: **LOW** (mostly standard OIDC)

---

### Auth0 (Managed Platform)

**Standard features** (portable):
- OAuth 2.0, OIDC (100% compliant)
- JWT tokens
- Social login

**Proprietary features** (lock-in):
- Auth0 Actions (custom logic on auth events)
- Auth0 Rules (deprecated, but still used)
- Auth0 Hooks (custom endpoints)
- Auth0 Universal Login (customizable login page)

**Migration away**: 20-40 hours (recreate Actions/Rules, export users)
**Lock-in level**: **MEDIUM** (OIDC standard, but Actions proprietary)

---

### AWS Cognito

**Standard features** (portable):
- OAuth 2.0, OIDC (compliant)
- JWT tokens

**Proprietary features** (lock-in):
- Cognito User Pools (AWS-specific API)
- Cognito Identity Pools (federated identities, AWS-specific)
- AWS IAM integration
- Lambda triggers (AWS-specific)

**Migration away**: 12-24 hours (OIDC portable, but Lambda triggers need recreation)
**Lock-in level**: **MEDIUM-to-HIGH** (AWS ecosystem integration)

---

### Supabase Auth

**Standard features** (portable):
- OAuth 2.0, OIDC-based
- JWT tokens

**Proprietary features** (lock-in):
- Supabase Row-Level Security (RLS) integration
- Supabase Realtime (auth-aware subscriptions)
- Supabase Storage (auth-aware access control)

**Migration away**: 12-24 hours (OIDC portable, but RLS/Realtime requires redesign)
**Lock-in level**: **MEDIUM** (Supabase ecosystem lock-in)

---

## Cost Comparison (10K MAU, 3 Years)

### Path 2: Keycloak (Self-Hosted)

**Monthly cost**: $200/month (server + maintenance)
**Year 1**: $200 × 12 = $2,400
**Year 2**: $200 × 12 = $2,400
**Year 3**: $200 × 12 = $2,400
**Total**: **$7,200** (3 years)

**Operational cost**: ~10 hours/month maintenance = $3,000/month (if valued at $300/hour)
**True TCO**: $7,200 + $108,000 = **$115,200** (3 years)

---

### Path 3: Auth0 (Managed)

**Monthly cost**: $1,400/month (10K MAU)
**Year 1**: $1,400 × 12 = $16,800
**Year 2**: $1,400 × 12 = $16,800
**Year 3**: $1,400 × 12 = $16,800
**Total**: **$50,400** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$50,400** (3 years)

---

### Path 3: AWS Cognito (Managed)

**Monthly cost**: $275/month (50K MAU), $55/month (10K MAU)
**Year 1**: $55 × 12 = $660
**Year 2**: $55 × 12 = $660
**Year 3**: $55 × 12 = $660
**Total**: **$1,980** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$1,980** (3 years)

---

### Path 3: Supabase Auth (Managed)

**Monthly cost**: $25/month (unlimited MAU)
**Year 1**: $25 × 12 = $300
**Year 2**: $25 × 12 = $300
**Year 3**: $25 × 12 = $300
**Total**: **$900** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$900** (3 years)

---

### Savings Analysis

**Supabase vs Auth0**: $49,500 saved (98% reduction)
**AWS Cognito vs Auth0**: $48,420 saved (96% reduction)

**Even accounting for operational burden** (Keycloak + $108K ops cost):
- Keycloak total: $115,200
- Auth0 total: $50,400
- **Auth0 is cheaper** when accounting for ops (managed platforms win for small teams)

**Key insight**: For small teams, managed platforms (Supabase, Cognito, Auth0) are cost-effective when factoring in operational burden.

---

## Recommendation

**Default choice**: **Depends on team size and budget**

### Startup (<10K MAU):
- **Choice**: Supabase Auth ($25/month unlimited) or AWS Cognito ($0-55/month)
- **Why**: Cheapest options, managed
- **Warning**: Supabase ecosystem lock-in, Cognito poor DX

### Small Business (10K-50K MAU, technical team):
- **Choice**: Keycloak (self-hosted, $200/month) if have ops team
- **Choice**: Auth0 ($240-1,400/month) if prefer managed
- **Why**: Keycloak for cost+control, Auth0 for convenience

### Mid-Size (50K-100K MAU):
- **Choice**: Auth0 ($1,400-2,800/month)
- **Why**: Developer experience, enterprise features

### Enterprise (100K+ MAU, need SSO/SAML):
- **Choice**: Okta ($1,500-5,000/month)
- **Why**: Enterprise-grade, compliance, SSO/SAML

---

## When to Avoid OIDC Standards

❌ **Very simple app** (username/password only, <100 users)
- DIY session auth may suffice
- OIDC may be overkill

❌ **No technical expertise** AND budget = $0
- Managed platform (Supabase, Cognito) better than insecure DIY

❌ **Need proprietary features** (Auth0 Actions, AWS IAM)
- Accept lock-in for those features
- Mitigation: Use standard OIDC for 90% of auth, vendor features for 10%

---

## Integration with Other Standards

**Related Tier 2 standards**:
- **2.050 PostgreSQL**: Store user profiles, session data
- **2.040 OpenTelemetry**: Instrument auth flows (login success/failure metrics)

**Related Tier 1 libraries**:
- **1.036 JWT Libraries**: PyJWT, python-jose (validate JWT tokens)
- **1.XXX OIDC Client Libraries**: Passport.js, Spring Security OAuth

**Related Tier 3 services**:
- This experiment (3.012) - Choose auth provider
- **3.010 WAF/Security**: Protect auth endpoints from brute force

---

## Key Takeaways

1. ✅ **OAuth 2.0 / OIDC ARE the portability standards** for authentication
2. ✅ **20+ compatible providers** - true portability (12-24 hour migrations)
3. ⚠️ **User migration has friction** - password hashes, custom attributes (MEDIUM lock-in)
4. ⚠️ **Vendor-specific features** (Auth0 Actions, AWS Lambda triggers) create soft lock-in
5. ✅ **Managed platforms can be cheaper** than self-hosted (when accounting for ops burden)
6. ✅ **Supabase cheapest** ($25/month unlimited MAU), **Auth0 best DX** ($240-1,400/month)
7. ❌ **DIY session auth is HIGH RISK** (security vulnerabilities, missing features)

**Decision**: For startups, use managed OIDC platform (Supabase, Cognito, Auth0). For enterprises with ops team, self-hosted Keycloak offers portability + control.

**Specific choice**: Supabase Auth (budget-conscious) or Auth0 (best developer experience).
