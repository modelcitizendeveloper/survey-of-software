# S3: Need-Driven Discovery - Authentication & Authorization Services

## Overview

This document analyzes authentication/authorization provider fit for specific business use case patterns. Each section starts with business requirements, evaluates 2-3 best-fit providers, and provides decision criteria for choosing between finalists.

**Discovery Approach**: Use case requirements → provider fit analysis. Start with the need, find the best solution.

---

## Use Case Pattern #1: Simple SaaS App (Email/Password + Social Login)

### Business Requirements

**Core Needs**:
- Email/password authentication with secure password storage
- Social login (Google, GitHub, Microsoft) for low-friction signup
- Email verification and password reset workflows
- Basic user profile management
- Session management with token refresh
- Rate limiting to prevent brute force attacks
- Simple role-based access (user vs. admin)

**Technical Needs**:
- Drop-in authentication UI components (login, signup, password reset)
- JWT or session token management
- OAuth 2.0 / OpenID Connect support for social providers
- API endpoints for user management
- Webhook notifications for auth events
- Mobile SDK support (iOS, Android)
- Easy integration with common frameworks (React, Next.js, Vue)

**Scale Profile**:
- 1,000 - 100,000 users
- Standard security requirements
- Startup or small business budget

### Provider Fit Analysis

#### Clerk - Best for Modern SaaS Developer Experience

**Why It Fits**:
- Beautiful pre-built UI components for React, Next.js, Remix
- Social login providers configured in minutes (Google, GitHub, Microsoft, etc.)
- Email verification and password reset flows built-in
- User management dashboard with search and filtering
- Session management with automatic token refresh
- User impersonation for customer support
- Generous free tier: 10,000 monthly active users

**Best For**:
- Modern JavaScript applications (React, Next.js, Vue)
- Startups wanting to ship fast with minimal auth code
- Teams prioritizing developer experience and design quality
- B2B SaaS needing organization/team features

**Pricing Model**:
- Free: 10,000 MAU (monthly active users)
- Pro: $25/month + $0.02 per MAU over 500
- Enterprise: Custom pricing with SSO, advanced security

**Capabilities Highlight**:
- Organizations and memberships (multi-tenancy built-in)
- Magic link authentication (passwordless option)
- Multi-factor authentication (SMS, TOTP, backup codes)
- User profile enrichment with metadata
- WebAuthn support for passkeys
- Customizable session duration
- Production and development environments

**Limitations**:
- Focused on JavaScript ecosystems (less ideal for backend-heavy apps)
- Newer platform (less enterprise adoption than Auth0)
- Limited control over email templates on lower tiers
- No self-hosted option
- Customization requires learning Clerk APIs
- Higher cost at scale (>10K MAU gets expensive)

#### Supabase Auth - Best for Open Source and Cost

**Why It Fits**:
- Completely free for up to 50,000 MAU
- Open source (can self-host if needed)
- Social login providers easy to configure
- Email/password with email verification built-in
- Row Level Security (RLS) for database-level authorization
- Works seamlessly with Supabase database and storage
- Simple API similar to Firebase but open source

**Best For**:
- Bootstrapped startups optimizing for cost
- Developers comfortable with PostgreSQL and SQL
- Teams wanting open source with option to self-host
- Applications already using or planning to use Supabase
- Projects needing database-level security policies

**Pricing Model**:
- Free: 50,000 MAU, 2GB database
- Pro: $25/month, 100,000 MAU, 8GB database
- Team: $599/month, unlimited MAU, dedicated resources
- Self-hosted: Free (manage your own infrastructure)

**Capabilities Highlight**:
- Row Level Security for fine-grained authorization
- Phone authentication (SMS and WhatsApp)
- Magic link and email OTP
- Social providers: 20+ integrations
- SAML SSO (Enterprise add-on)
- Anonymous sign-ins for guest users
- Server-side auth for better security

**Limitations**:
- No pre-built UI components (you build your own)
- Requires more development work than Clerk
- Best value comes from using full Supabase stack
- Enterprise SSO requires additional add-on
- Less polished documentation than commercial alternatives
- Fewer integrations compared to Auth0/Clerk
- Support quality depends on tier

#### Auth0 - Best for Established Platform with Flexibility

**Why It Fits**:
- Universal Login with customizable hosted pages
- Extensive social provider support (30+ platforms)
- Robust password policy configuration
- Advanced security features (anomaly detection, breached password detection)
- Rules and Actions for custom authentication logic
- Battle-tested at enterprise scale
- Comprehensive documentation and community support

**Best For**:
- Teams needing proven, reliable authentication
- Applications with complex authentication workflows
- Companies requiring extensive customization
- Organizations planning for enterprise customers
- Multi-platform apps (web, mobile, native)

**Pricing Model**:
- Free: 7,500 MAU
- Essentials: $35/month + $0.0175 per MAU (min 500 MAU)
- Professional: $240/month + $0.035 per MAU (min 500 MAU)
- Enterprise: Custom pricing

**Capabilities Highlight**:
- Actions: Custom code in authentication flow
- Organizations (multi-tenancy for B2B)
- Attack protection with adaptive MFA
- Anomaly detection for suspicious logins
- Bot detection and CAPTCHA
- Extensive API and SDKs for all platforms
- Migration tools from other providers

**Limitations**:
- Expensive at scale compared to alternatives
- Free tier limited to 7,500 MAU (less than Clerk)
- UI/UX feels dated compared to Clerk
- Complexity can be overwhelming for simple use cases
- Minimum 500 MAU on paid plans (forces higher cost)
- Owned by Okta (corporate overhead, slower innovation)
- Overkill for simple applications

### Decision Criteria

**Choose Clerk if**:
- You're building with React, Next.js, or modern JavaScript
- You want beautiful pre-built UI components
- Developer experience and speed to market are priorities
- You need organization/team features for B2B SaaS
- Budget allows $25+/month after free tier

**Choose Supabase Auth if**:
- Cost is a primary concern (best free tier at 50K MAU)
- You're using or planning to use Supabase database
- You're comfortable building your own UI components
- Open source and self-hosting options are valuable
- You want database-level security with Row Level Security

**Choose Auth0 if**:
- You need proven enterprise reliability
- You have complex authentication requirements
- You want extensive customization with Actions/Rules
- You're building for multiple platforms (web, mobile, native)
- Enterprise features (SSO, compliance) are needed soon

**Decision Tree**:
```
What's your primary framework?
├─ React/Next.js/Modern JS → Clerk (best DX)
├─ Backend-heavy (Rails, Django, Go) → Auth0 or Supabase
└─ Full-stack with Supabase → Supabase Auth (integrated)

Budget constraints:
├─ <$50/month → Supabase (free up to 50K MAU)
├─ $50-200/month → Clerk (great DX, worth the cost)
└─ >$200/month or enterprise → Auth0 (proven scale)

Complexity:
├─ Simple email + social → Clerk or Supabase
├─ Complex workflows → Auth0 (Actions/Rules)
└─ Custom everything → Auth0 or self-host Supabase
```

**Cost Comparison Example (10K MAU)**:
- Clerk: Free (under 10K MAU limit)
- Supabase: Free (under 50K MAU limit)
- Auth0: Free (under 7,500 MAU) or $35+/month if >7,500

**Real Cost at 20K MAU**:
- Clerk: $25 + (19,500 × $0.02) = $415/month
- Supabase: Free (still under 50K limit)
- Auth0 Essentials: $35 + (19,500 × $0.0175) = $376/month

---

## Use Case Pattern #2: Enterprise B2B with SSO Requirements

### Business Requirements

**Core Needs**:
- SAML 2.0 and OIDC SSO for enterprise customers
- Multi-tenant architecture (one tenant per customer organization)
- Just-in-Time (JIT) provisioning for new enterprise users
- Automated user provisioning and de-provisioning (SCIM)
- Support for major identity providers (Okta, Azure AD, Google Workspace)
- Audit logging for compliance (SOC 2, ISO 27001)
- Custom domain support for white-label login pages
- Role-based access control (RBAC) with granular permissions

**Technical Needs**:
- SSO configuration UI for customer admins
- API for programmatic SSO setup
- SCIM 2.0 support for user lifecycle management
- Webhook events for provisioning/de-provisioning
- Directory sync with enterprise identity providers
- Support for multiple authentication methods per tenant
- Session management with configurable timeouts
- Compliance reporting and audit trails

**Business Context**:
- Selling to enterprises (Fortune 1000, mid-market)
- Security and compliance are deal requirements
- Customers demand SSO as table stakes
- Need to support hundreds of separate enterprise tenants

### Provider Fit Analysis

#### WorkOS - Best for B2B SaaS with Enterprise Features

**Why It Fits**:
- Built specifically for B2B SaaS enterprise features
- SAML and OIDC SSO with minimal code (2-3 API calls)
- Admin Portal: Self-service SSO configuration for customers
- Directory Sync (SCIM) with automatic user provisioning
- Generous free tier: SSO for up to 1M users
- Modern API designed for developers
- Transparent, predictable pricing model
- Excellent documentation with B2B SaaS focus

**Best For**:
- B2B SaaS companies selling to enterprises
- Startups adding enterprise features to close deals
- Teams wanting SSO without building it themselves
- Companies needing Directory Sync for user management

**Pricing Model**:
- SSO: Free up to 1M users (unlimited connections)
- Directory Sync: $125/month per directory connection
- Audit Logs: $50/month flat fee
- User Management: $25/month + usage
- No per-user fees for SSO (huge advantage)

**Capabilities Highlight**:
- Admin Portal: White-label UI for customer IT admins
- Universal SSO: SAML, OIDC, Google, Microsoft
- Directory Sync: Okta, Azure AD, Google, OneLogin, JumpCloud
- Just-in-Time provisioning with attribute mapping
- Organizations API for multi-tenancy
- Magic Link authentication for non-SSO users
- Domain verification and domain capture
- RBAC with fine-grained permissions

**Limitations**:
- Not a complete authentication solution (add to existing auth)
- No built-in email/password auth (use with Clerk/Auth0/etc.)
- Focused on enterprise features only
- Directory Sync has per-connection costs ($125/month each)
- Smaller ecosystem than Auth0/Okta
- Newer company (less enterprise brand recognition)
- No MFA provider built-in

#### Auth0 (Okta) - Best for Comprehensive Enterprise Platform

**Why It Fits**:
- Full-featured enterprise authentication and SSO
- SAML and OIDC support for all major IdPs
- Organizations feature for multi-tenant B2B
- Extensive customization with Rules, Actions, Hooks
- Enterprise-grade security and compliance (SOC 2, ISO 27001, HIPAA)
- Strong brand recognition (owned by Okta)
- Mature platform with proven scale
- Advanced security: anomaly detection, bot protection, adaptive MFA

**Best For**:
- Established companies with complex auth requirements
- Organizations needing one platform for all auth needs
- Companies where brand recognition matters for sales
- Teams requiring extensive customization and control
- Applications with diverse authentication methods

**Pricing Model**:
- Professional: $240/month + $0.035 per MAU (min 500 MAU)
- Enterprise: Custom pricing (required for SAML SSO)
- Typical enterprise contract: $2,000-$10,000+/month
- Per-MAU pricing can get expensive at scale
- SSO only available on Enterprise tier

**Capabilities Highlight**:
- Organizations: Multi-tenant with member invitations
- SAML and OIDC SSO with major IdPs
- Custom Actions for authentication flow logic
- Attack protection with adaptive authentication
- Extensive API for user management
- Migration capabilities from other platforms
- Advanced MFA options (push, SMS, TOTP, WebAuthn)
- Custom domains and white-label login

**Limitations**:
- Expensive: SSO requires Enterprise tier ($$$)
- Per-MAU pricing becomes costly at scale
- Complexity can be overwhelming
- SCIM/Directory Sync is additional cost
- Setup and configuration time-intensive
- Slower innovation since Okta acquisition
- Overkill if you only need SSO

#### Descope - Best for Modern Drag-and-Drop Auth Flows

**Why It Fits**:
- Visual workflow builder for authentication flows
- SAML and OIDC SSO with no-code configuration
- Multi-tenant support with tenant management UI
- Modern developer experience with SDKs
- Generous free tier with enterprise features
- Passwordless and passkey support built-in
- Faster time to market than Auth0

**Best For**:
- Teams wanting enterprise auth without coding complexity
- Companies needing SSO but wanting modern UX
- Startups balancing ease of use with enterprise features
- Organizations wanting visual configuration over code

**Pricing Model**:
- Free: 7,500 MAU with enterprise features (SSO, MFA included)
- Pro: $0.05 per MAU (volume discounts available)
- Enterprise: Custom pricing with SLA and support
- SSO included in all tiers (unlike Auth0)

**Capabilities Highlight**:
- Flows: Visual drag-and-drop authentication builder
- SAML and OIDC SSO configuration
- Multi-tenancy with tenant isolation
- Passwordless (magic link, OTP, passkeys)
- User management with search and actions
- Audit logs and analytics
- Custom domains and branding
- API and SDKs for all major platforms

**Limitations**:
- Newer platform (less proven at massive scale)
- Smaller ecosystem than Auth0
- Visual flows may be limiting for complex logic
- Less customization than Auth0 Actions/Rules
- No Directory Sync/SCIM yet
- Support quality depends on tier
- Enterprise adoption still growing

### Decision Criteria

**Choose WorkOS if**:
- You need SSO and Directory Sync for B2B SaaS
- You want to add enterprise features to existing auth
- Free SSO for unlimited users is attractive
- You want self-service Admin Portal for customers
- Directory Sync is required ($125/connection is acceptable)

**Choose Auth0 if**:
- You need comprehensive authentication platform
- Enterprise brand recognition matters for sales
- You have complex, custom authentication requirements
- Budget supports $2K-10K+/month for enterprise tier
- You want battle-tested platform at massive scale

**Choose Descope if**:
- You want SSO without enterprise pricing
- Visual flow builder appeals to your team
- Modern UX and DX are important
- You're building new and want faster setup than Auth0
- Free tier with SSO is valuable for getting started

**Decision Tree**:
```
Primary requirement:
├─ Just need SSO (have existing auth) → WorkOS (add-on approach)
├─ Full auth + SSO platform → Auth0 or Descope
└─ SSO + Directory Sync → WorkOS (best value)

Budget consideration:
├─ <$200/month → Descope (SSO on free tier) or WorkOS (free SSO)
├─ $200-1,000/month → Descope (per-MAU pricing)
└─ >$1,000/month + need brand → Auth0 Enterprise

Complexity tolerance:
├─ Want simple/visual → Descope (drag-and-drop flows)
├─ Need customization → Auth0 (Actions/Rules)
└─ Add to existing → WorkOS (minimal integration)

Directory Sync required?
├─ YES, multiple directories → WorkOS ($125/directory)
├─ YES, need full control → Auth0 Enterprise ($$$$)
└─ NO → Descope or WorkOS
```

**Cost Comparison for Enterprise SSO (5 customer SSO connections, 50K users)**:
- WorkOS: Free SSO + (5 × $125 Directory Sync) = $625/month
- Auth0 Enterprise: ~$3,000-5,000/month (typical contract)
- Descope: 50K MAU × $0.05 = $2,500/month (or volume discount)

**Feature Comparison**:

| Feature | WorkOS | Auth0 | Descope |
|---------|--------|-------|---------|
| **SAML SSO** | Yes (free) | Yes (Enterprise) | Yes (all tiers) |
| **OIDC SSO** | Yes (free) | Yes (all tiers) | Yes (all tiers) |
| **Directory Sync** | Yes ($125/conn) | Yes (add-on) | Roadmap |
| **Admin Portal** | Yes (white-label) | Custom build | Built-in |
| **Free Tier** | 1M users SSO | 7,500 MAU | 7,500 MAU + SSO |
| **JIT Provisioning** | Yes | Yes | Yes |
| **Custom Domains** | No | Yes | Yes |
| **Audit Logs** | Yes ($50/month) | Yes (Enterprise) | Yes |
| **MFA Built-in** | No (use with auth) | Yes | Yes |

---

## Use Case Pattern #3: Passwordless & Modern Auth (Passkeys, Magic Links)

### Business Requirements

**Core Needs**:
- Passwordless authentication (no passwords to manage or forget)
- Magic link via email for one-click login
- SMS and WhatsApp OTP for phone-based auth
- Passkeys (WebAuthn) for biometric authentication
- Social login as alternative passwordless option
- Low-friction signup and login experience
- Security without complexity for users
- Mobile-friendly authentication methods

**Technical Needs**:
- WebAuthn/FIDO2 support for passkeys
- Magic link generation and validation
- OTP delivery via SMS, email, WhatsApp
- Biometric authentication on mobile (Touch ID, Face ID)
- Device management and trusted device tracking
- Fallback authentication methods
- Session management with device binding
- Cross-device authentication flows

**Use Case Context**:
- Consumer-facing application prioritizing UX
- Reducing friction in signup/login flows
- Eliminating password-related support tickets
- Modern security without user burden

### Provider Fit Analysis

#### Clerk - Best for Complete Passwordless Platform

**Why It Fits**:
- Comprehensive passwordless options: magic link, OTP, passkeys
- Beautiful pre-built UI for all passwordless flows
- Email magic links with one-click verification
- Phone number authentication with SMS/WhatsApp OTP
- Passkeys (WebAuthn) with biometric support
- Social login alongside passwordless options
- User can choose preferred authentication method
- Device management and trusted devices

**Best For**:
- Modern web apps prioritizing user experience
- Consumer apps wanting frictionless authentication
- Startups wanting passwordless without building it
- React/Next.js applications (best integration)

**Pricing Model**:
- Free: 10,000 MAU with all passwordless features
- Pro: $25/month + $0.02 per MAU over 500
- SMS costs: $0.055 per message (pay as you go)
- Enterprise: Custom pricing

**Passwordless Capabilities**:
- **Magic Links**: Email-based one-click authentication
- **OTP Codes**: SMS and email OTP with customizable templates
- **Passkeys**: WebAuthn/FIDO2 for biometric auth
- **Social Login**: Google, Apple, GitHub, etc. (passwordless alternative)
- **Multi-Method**: Users can authenticate via any enabled method
- **Backup Codes**: For account recovery
- **Device Tracking**: Remember and manage trusted devices

**Implementation Ease**:
```javascript
// Clerk magic link - just enable in dashboard
<SignIn.Root>
  <SignIn.Step name="start">
    <SignIn.Strategy name="email_link">
      <SignIn.Action submit>Send magic link</SignIn.Action>
    </SignIn.Strategy>
  </SignIn.Step>
</SignIn.Root>
```

**Limitations**:
- SMS costs extra ($0.055/message adds up)
- Best for JavaScript ecosystems
- Passkey support relatively new (still maturing)
- Limited control over email/SMS templates on free tier
- Not ideal for backend-heavy applications
- Vendor lock-in (no easy export of users)

#### Magic (now part of Fortmatic) - Best for Web3 and Crypto Apps

**Why It Fits**:
- Passwordless authentication via email magic links
- Web3 wallet integration (crypto-native)
- No passwords, no browser extensions needed
- Simple email-based authentication
- Non-custodial key management
- Focus on blockchain and Web3 applications

**Best For**:
- Web3 and crypto applications
- NFT platforms and DeFi apps
- Applications needing wallet integration
- Teams building blockchain experiences

**Pricing Model**:
- Free: 1,000 MAU
- Growth: $199/month for 10,000 MAU
- Enterprise: Custom pricing
- Higher cost per user than alternatives

**Passwordless Capabilities**:
- Email magic links (primary method)
- SMS authentication available
- Social login (Google, Apple, Discord, Twitter)
- Wallet integration for Web3
- Non-custodial key management
- Cross-device authentication

**Limitations**:
- Focused on Web3/crypto use cases
- Expensive compared to general-purpose solutions
- Limited to email magic links (no passkeys)
- Smaller feature set outside Web3
- Not ideal for traditional web/mobile apps
- Less documentation than mainstream providers
- Uncertain future after acquisition

#### Stytch - Best for Dedicated Passwordless Infrastructure

**Why It Fits**:
- Built specifically for passwordless authentication
- Email magic links with customizable branding
- SMS passcodes with global delivery
- WhatsApp authentication for international users
- Biometric authentication and WebAuthn
- Fraud and risk detection built-in
- Session management with device fingerprinting
- B2B and B2C solutions

**Best For**:
- Companies going all-in on passwordless
- Applications needing fraud detection
- International apps (WhatsApp auth valuable)
- Teams wanting best-in-class passwordless UX

**Pricing Model**:
- Free: 5,000 MAU (B2C) or 1,000 members (B2B)
- Growth: $249/month for 25,000 MAU (B2C)
- B2B: $599/month for organizations features
- Enterprise: Custom pricing
- SMS costs included in pricing (better than pay-per-message)

**Passwordless Capabilities**:
- **Email Magic Links**: Customizable, trackable, secure
- **SMS Passcodes**: Global delivery with fraud detection
- **WhatsApp**: Authentication via WhatsApp OTP
- **Biometrics**: WebAuthn with device attestation
- **OAuth**: Social login as passwordless alternative
- **Crypto Wallets**: Web3 wallet authentication
- **Fraud Detection**: Machine learning-based risk scoring
- **Session Management**: Device fingerprinting and trust

**Implementation Ease**:
```javascript
// Stytch magic link
await stytch.magicLinks.email.send({
  email: user.email,
  login_magic_link_url: 'https://app.com/authenticate',
  signup_magic_link_url: 'https://app.com/authenticate',
});
```

**Limitations**:
- No pre-built UI (you build your own components)
- More expensive than Clerk at same scale
- Focused only on passwordless (no password fallback)
- Requires more development work than Clerk
- B2B features require separate, higher-tier plan
- Less integrated than all-in-one platforms
- Support quality varies by tier

### Decision Criteria

**Choose Clerk if**:
- You want pre-built UI for passwordless flows
- You're building with React/Next.js
- You want users to choose authentication method
- Developer experience and speed are priorities
- You need both passwordless and traditional auth

**Choose Magic if**:
- You're building Web3/crypto application
- Wallet integration is important
- Your users are crypto-native
- Non-custodial key management is valuable
- You're okay with higher cost for Web3 features

**Choose Stytch if**:
- Passwordless is core to your product strategy
- You need advanced fraud detection
- International users benefit from WhatsApp auth
- You're willing to build custom UI
- SMS costs included in pricing is valuable

**Decision Tree**:
```
Application type:
├─ Web3/Crypto → Magic (wallet integration)
├─ Consumer web/mobile → Clerk (best UX) or Stytch (fraud detection)
└─ B2B SaaS → Stytch B2B or Clerk (organizations)

Pre-built UI needed?
├─ YES (want to ship fast) → Clerk (beautiful components)
└─ NO (building custom UI) → Stytch (API-first)

Budget:
├─ <$100/month → Clerk (free up to 10K MAU)
├─ $100-500/month → Clerk or Stytch
└─ >$500/month + need fraud detection → Stytch

SMS volume:
├─ High SMS usage → Stytch (included in pricing)
├─ Moderate SMS → Clerk (pay per message)
└─ Email-only → Clerk or Stytch
```

**Cost Comparison at 10K MAU (50% email, 50% SMS)**:
- Clerk: Free (under 10K limit) + SMS (5K × $0.055) = $275/month
- Stytch Growth: $249/month (includes SMS)
- Magic Growth: $199/month (10K MAU tier)

**Passwordless Method Support**:

| Method | Clerk | Magic | Stytch |
|--------|-------|-------|--------|
| **Email Magic Links** | Yes | Yes | Yes |
| **SMS OTP** | Yes | Yes | Yes |
| **WhatsApp OTP** | Yes | No | Yes |
| **Passkeys (WebAuthn)** | Yes | No | Yes |
| **Social Login** | Yes | Yes | Yes |
| **Crypto Wallets** | No | Yes | Yes |
| **Biometrics** | Yes (via passkeys) | No | Yes |
| **Device Trust** | Yes | Limited | Yes |
| **Fraud Detection** | Basic | No | Advanced |

---

## Use Case Pattern #4: Multi-Tenant B2B (Organization Management)

### Business Requirements

**Core Needs**:
- Organization/workspace/team structure for tenants
- Member invitation and management per organization
- Role-based permissions within organizations
- Team admin dashboard for self-service user management
- Seat-based pricing and subscription enforcement
- SSO per organization (different IdPs per tenant)
- Organization switching for users in multiple teams
- Audit logs per organization for compliance

**Technical Needs**:
- Multi-tenant data isolation
- Organization API for CRUD operations
- Member invitation flow with email verification
- RBAC with custom roles and permissions
- Organization-level settings and configuration
- Billing integration (seats, usage tracking)
- Webhook events for organization lifecycle
- Subdomain or custom domain per organization

**Business Context**:
- B2B SaaS with team/workspace model (Slack, Notion, Linear)
- Seat-based or team-based pricing
- Each customer organization needs isolation
- Users may belong to multiple organizations
- Self-service team management reduces support burden

### Provider Fit Analysis

#### Clerk - Best for Modern Multi-Tenant SaaS

**Why It Fits**:
- Organizations feature built-in and first-class
- Member invitations with customizable emails
- Role-based permissions with flexible RBAC
- Organization switching UI component included
- User profile with organization memberships
- Organization admin dashboard for self-service
- Domain-based organization assignment
- Generous free tier with organizations included

**Best For**:
- Modern B2B SaaS applications
- Team collaboration tools and workspace apps
- React/Next.js applications
- Startups building multi-tenant from day one
- Products with Slack/Notion-like organization model

**Pricing Model**:
- Free: 10,000 MAU with organizations
- Pro: $25/month + $0.02 per MAU
- Enterprise: Custom pricing with advanced features
- Organizations included in all tiers (no extra cost)

**Multi-Tenancy Capabilities**:
- **Organizations**: Isolated workspaces/teams
- **Memberships**: User-organization relationships with roles
- **Invitations**: Send, accept, revoke member invites
- **Roles**: Built-in (admin, member) or custom roles
- **Permissions**: Granular permissions per role
- **Organization Switching**: UI component for users in multiple orgs
- **Domains**: Verified domains for organization membership
- **SSO per Organization**: Each org can have own IdP

**Implementation Example**:
```javascript
// Create organization
const organization = await clerkClient.organizations.createOrganization({
  name: 'Acme Inc',
  createdBy: userId,
});

// Invite member
await organization.inviteMember({
  emailAddress: 'user@example.com',
  role: 'org:member',
});

// Organization switcher component
<OrganizationSwitcher />
```

**Limitations**:
- Best for JavaScript ecosystems
- Custom roles require Pro tier
- SSO per organization requires Enterprise tier
- Limited control over invitation email templates
- No built-in billing/subscription enforcement
- Organization domain verification can be complex
- Vendor-specific approach (not portable)

#### Auth0 Organizations - Best for Enterprise-Grade Multi-Tenancy

**Why It Fits**:
- Organizations feature for B2B multi-tenancy
- Member invitations and lifecycle management
- SSO per organization with different IdPs
- Flexible RBAC with organization context
- Extensive customization via Actions
- Enterprise security and compliance
- Proven at large scale (thousands of organizations)

**Best For**:
- Enterprise B2B applications
- Companies with complex multi-tenant requirements
- Organizations needing extensive customization
- Applications requiring per-tenant SSO
- Established companies with budget for Auth0

**Pricing Model**:
- Professional: $240/month + $0.035 per MAU
- Enterprise: Custom pricing (typically $2K+/month)
- Organizations available on Professional tier
- Per-organization SSO requires Enterprise tier

**Multi-Tenancy Capabilities**:
- **Organizations**: Tenant isolation and management
- **Members**: User-organization relationships
- **Invitations**: Customizable invitation flow
- **Roles**: Organization-scoped RBAC
- **Connections**: Per-organization authentication methods
- **SSO**: Different SAML/OIDC IdP per organization
- **Metadata**: Custom data per organization
- **Actions**: Custom logic for organization events

**Implementation Example**:
```javascript
// Create organization via Management API
await auth0.organizations.create({
  name: 'acme-inc',
  display_name: 'Acme Inc',
});

// Add member to organization
await auth0.organizations.addMembers(
  { id: orgId },
  { members: [userId] }
);
```

**Limitations**:
- Expensive, especially at scale
- Complexity can be overwhelming
- Organizations require Professional tier minimum
- Per-organization SSO only on Enterprise tier
- UI/UX dated compared to Clerk
- Slow innovation cycle
- Overkill for simple multi-tenancy

#### Propel Auth - Best for Developer-Focused B2B Multi-Tenancy

**Why It Fits**:
- Built specifically for B2B SaaS multi-tenancy
- Organizations and RBAC included from day one
- Team member management and invitations
- SSO per organization on all paid tiers
- Modern API similar to Clerk
- More affordable than Auth0 for B2B
- Pre-built UI components and hosted pages

**Best For**:
- B2B SaaS teams wanting Auth0 features at Clerk pricing
- Startups needing SSO without enterprise costs
- Developer teams wanting modern DX
- Companies building multi-tenant B2B products

**Pricing Model**:
- Free: 1,000 MAU (basic features)
- Startup: $150/month for 5,000 MAU (includes SSO)
- Growth: $350/month for 15,000 MAU
- Enterprise: Custom pricing
- SSO included in Startup tier (unlike Auth0)

**Multi-Tenancy Capabilities**:
- **Organizations**: First-class multi-tenant support
- **Members**: Role-based member management
- **Invitations**: Email invites with custom templates
- **RBAC**: Flexible roles and permissions
- **SSO per Org**: SAML and OIDC per organization
- **Domain Verification**: Auto-assign users by domain
- **API Keys**: Organization-scoped API keys
- **Webhooks**: Organization lifecycle events

**Implementation Example**:
```javascript
// Propel Auth SDK
const org = await propelAuth.createOrg({
  name: 'Acme Inc',
});

await org.inviteUser({
  email: 'user@example.com',
  role: 'Member',
});
```

**Limitations**:
- Newer platform (less proven at massive scale)
- Smaller ecosystem than Auth0 or Clerk
- Pre-built UI less polished than Clerk
- Fewer integrations than established platforms
- Documentation still growing
- Support quality varies by tier
- Enterprise adoption still building

### Decision Criteria

**Choose Clerk if**:
- You're building with React/Next.js
- You want beautiful pre-built organization components
- Developer experience is a priority
- You need organization features on free tier
- SSO per organization is not immediate requirement

**Choose Auth0 if**:
- You need proven enterprise-grade multi-tenancy
- Per-organization SSO is critical requirement
- You have budget for Professional/Enterprise tier
- Complex customization with Actions is needed
- Brand recognition matters for enterprise sales

**Choose Propel Auth if**:
- You need B2B multi-tenancy at affordable price
- SSO per organization without enterprise pricing
- You want modern DX similar to Clerk
- You're building B2B SaaS and want purpose-built tool
- Budget is $150-500/month range

**Decision Tree**:
```
Per-organization SSO required?
├─ YES, immediately:
│   ├─ Budget <$500/month → Propel Auth ($150 Startup tier)
│   └─ Budget >$500/month → Auth0 or Propel Auth
├─ YES, eventually → Clerk (migrate to Enterprise) or Propel Auth
└─ NO (shared auth) → Clerk (best overall experience)

Framework:
├─ React/Next.js → Clerk (best integration)
├─ Backend-heavy → Auth0 or Propel Auth
└─ Multi-platform → Auth0 (most SDKs)

Budget:
├─ <$100/month → Clerk Free (10K MAU)
├─ $100-500/month → Propel Auth or Clerk Pro
└─ >$500/month → Auth0 or Propel Auth Enterprise
```

**Cost Comparison (10K MAU, 5 organizations with SSO)**:

| Provider | Monthly Cost | SSO Included? | Notes |
|----------|--------------|---------------|-------|
| **Clerk** | Free (under 10K) | No (Enterprise only) | Best free tier |
| **Propel Auth** | $150 | Yes (5 orgs) | Best value for SSO |
| **Auth0** | $240 + MAU | No (Enterprise only) | Most expensive |

**Feature Comparison**:

| Feature | Clerk | Auth0 | Propel Auth |
|---------|-------|-------|-------------|
| **Organizations** | Yes (all tiers) | Yes (Pro+) | Yes (all tiers) |
| **RBAC** | Yes (Pro for custom) | Yes | Yes |
| **Invitations** | Yes | Yes | Yes |
| **SSO per Org** | Enterprise only | Enterprise only | Startup tier+ |
| **Pre-built UI** | Excellent | Basic | Good |
| **Custom Domains** | Enterprise | Yes | Yes |
| **Audit Logs** | Yes | Yes | Yes |
| **Free Tier MAU** | 10,000 | 7,500 | 1,000 |

---

## Use Case Pattern #5: Compliance-Heavy Industries (HIPAA, SOC 2)

### Business Requirements

**Core Needs**:
- HIPAA compliance for healthcare applications
- SOC 2 Type II certification
- BAA (Business Associate Agreement) availability
- Audit logging for all authentication events
- Data encryption at rest and in transit
- Secure session management with strict timeouts
- MFA enforcement for privileged access
- Access controls and role-based permissions
- Data residency controls (store data in specific regions)

**Technical Needs**:
- Encrypted user data storage
- Audit trail with immutable logs
- Session timeout configuration
- IP allowlisting and geo-blocking
- Advanced MFA options (TOTP, WebAuthn, SMS)
- Webhook events for security monitoring
- SAML/OIDC for SSO with healthcare systems
- Secure password policies (complexity, expiration)

**Regulatory Context**:
- HIPAA (healthcare)
- SOC 2 Type II (SaaS trust)
- GDPR (European data protection)
- ISO 27001 (information security)
- Financial services regulations (FINRA, SOC for Cybersecurity)

### Provider Fit Analysis

#### Auth0 (Okta) - Best for Comprehensive Compliance

**Why It Fits**:
- SOC 2 Type II and ISO 27001 certified
- HIPAA compliance with BAA available
- Extensive audit logging and monitoring
- Advanced security features (anomaly detection, bot protection)
- Enterprise-grade data encryption
- Comprehensive compliance documentation
- Battle-tested at regulated enterprises
- Okta ownership provides enterprise credibility

**Best For**:
- Healthcare companies requiring HIPAA compliance
- Financial services applications
- Enterprise SaaS needing SOC 2
- Regulated industries with strict security requirements
- Organizations where compliance is deal requirement

**Pricing Model**:
- Enterprise tier required for HIPAA/BAA
- Typical contract: $2,000-$10,000+/month
- Includes compliance certifications and support
- BAA available at no additional cost (on Enterprise)
- Audit log retention and compliance reporting included

**Compliance Capabilities**:
- **HIPAA**: BAA available, encrypted PHI storage
- **SOC 2 Type II**: Certified with annual audits
- **ISO 27001**: Information security management
- **GDPR**: Data processing agreements, data residency options
- **Audit Logs**: Comprehensive event logging with retention
- **Encryption**: AES-256 at rest, TLS 1.2+ in transit
- **MFA**: TOTP, SMS, push, WebAuthn, voice
- **Session Security**: Configurable timeouts, device tracking

**Compliance Features**:
- Anomaly detection (unusual login patterns)
- Breached password detection
- Bot detection and CAPTCHA
- Adaptive MFA based on risk
- IP allowlisting and geo-blocking
- Brute force protection
- Secure password policies
- Custom password complexity rules

**Limitations**:
- Expensive (enterprise tier required for compliance)
- Complex setup and configuration
- Compliance features spread across multiple products
- Long sales cycle for enterprise contracts
- Overkill if you don't need full compliance
- Support quality depends on contract tier
- Slower feature development

#### Descope - Best for Affordable Compliance for Startups

**Why It Fits**:
- SOC 2 Type II certified
- Compliance features on all tiers (including free)
- Modern security: passkeys, risk detection
- Audit logs and monitoring included
- Affordable compared to Auth0
- No-code security policies via flows
- Data encryption standard

**Best For**:
- Startups building in regulated industries
- Companies needing SOC 2 without enterprise budget
- Teams wanting compliance without complexity
- Organizations prioritizing modern security methods

**Pricing Model**:
- Free: 7,500 MAU with SOC 2 compliance
- Pro: $0.05 per MAU (volume discounts)
- Enterprise: Custom pricing with enhanced support
- Compliance included in all tiers

**Compliance Capabilities**:
- **SOC 2 Type II**: Certified (available to customers)
- **Audit Logs**: Comprehensive event tracking
- **Encryption**: Industry-standard encryption
- **MFA**: TOTP, SMS, WebAuthn/passkeys
- **Session Management**: Configurable timeouts
- **Risk-Based Auth**: Adaptive authentication
- **GDPR**: Data processing agreement
- **Password Policies**: Customizable rules

**Compliance Features**:
- Visual security policy builder
- Passwordless and passkey support
- Risk-based step-up authentication
- Device fingerprinting
- Rate limiting and bot detection
- IP-based access controls
- Audit trail with search

**Limitations**:
- No HIPAA/BAA (SOC 2 only)
- Newer platform (less enterprise adoption)
- No ISO 27001 certification yet
- Data residency options limited
- Smaller compliance documentation than Auth0
- Enterprise compliance features still maturing
- No dedicated compliance support on lower tiers

#### Stytch - Best for Fraud Prevention in Regulated Industries

**Why It Fits**:
- SOC 2 Type II certified
- Advanced fraud and risk detection
- Device fingerprinting and trust scoring
- HIPAA compliance roadmap (not yet available)
- Session management with device binding
- Passwordless reduces credential theft risk
- Built-in anomaly detection

**Best For**:
- Financial services needing fraud prevention
- Healthcare (non-HIPAA for now)
- Consumer fintech applications
- Applications where fraud is primary concern
- Companies wanting modern security with compliance

**Pricing Model**:
- Free: 5,000 MAU with basic features
- Growth: $249/month for 25,000 MAU
- Enterprise: Custom pricing with compliance features
- Fraud detection included in Growth tier

**Compliance Capabilities**:
- **SOC 2 Type II**: Certified
- **Fraud Detection**: ML-based risk scoring
- **Device Intelligence**: Fingerprinting and trust
- **Session Security**: Device binding, timeout controls
- **Audit Logs**: Event tracking and monitoring
- **Encryption**: Data encryption standard
- **GDPR**: Data processing agreement
- **MFA**: TOTP, SMS, WebAuthn

**Fraud & Security Features**:
- Device fingerprinting and velocity checks
- Impossible travel detection
- Known device management
- Email and phone risk scoring
- Bot detection
- Rate limiting per device/IP
- Behavioral biometrics (roadmap)

**Limitations**:
- No HIPAA/BAA yet (on roadmap)
- SOC 2 only (no ISO 27001)
- More expensive than Descope
- Fraud detection requires Growth tier
- Data residency options limited
- Enterprise compliance features in development
- Support quality varies by tier

### Decision Criteria

**Choose Auth0 if**:
- You must have HIPAA compliance with BAA
- You need ISO 27001 certification
- Enterprise brand recognition matters
- Budget supports $2K-10K+/month
- You want comprehensive compliance documentation
- Financial services or healthcare with strict regulations

**Choose Descope if**:
- You need SOC 2 but not HIPAA
- You're a startup with compliance requirements
- Budget is <$500/month
- Modern auth methods (passkeys) are valuable
- You want compliance on free tier
- Visual security policy builder appeals to team

**Choose Stytch if**:
- Fraud prevention is as important as compliance
- You're in financial services (non-banking)
- You need SOC 2 + advanced fraud detection
- Device trust and fingerprinting are critical
- Budget supports $250-1,000/month
- HIPAA not required (or can wait for roadmap)

**Decision Tree**:
```
Regulatory requirement:
├─ HIPAA/BAA required → Auth0 (only option with BAA)
├─ SOC 2 required → All three (choose based on other factors)
└─ ISO 27001 required → Auth0 (only certified option)

Industry:
├─ Healthcare (HIPAA) → Auth0
├─ Financial services → Stytch (fraud) or Auth0 (comprehensive)
├─ B2B SaaS → Descope (affordable SOC 2) or Auth0 (enterprise)
└─ Fintech consumer → Stytch (fraud detection)

Budget:
├─ <$500/month → Descope (free SOC 2)
├─ $500-2,000/month → Stytch or Descope
└─ >$2,000/month → Auth0 Enterprise

Fraud concern:
├─ High (fintech, crypto) → Stytch (fraud detection)
├─ Moderate → Descope (basic protection)
└─ Low (internal tools) → Descope or Auth0
```

**Compliance Certification Matrix**:

| Certification | Auth0 | Descope | Stytch |
|---------------|-------|---------|--------|
| **SOC 2 Type II** | Yes | Yes | Yes |
| **ISO 27001** | Yes | No | No |
| **HIPAA** | Yes (BAA available) | No | Roadmap |
| **GDPR** | Yes | Yes | Yes |
| **PCI DSS** | Yes (Level 1) | No | No |
| **FedRAMP** | No | No | No |

**Cost Comparison (Healthcare, 25K users, HIPAA required)**:
- Auth0 Enterprise: ~$3,000-5,000/month (with BAA)
- Descope: Not applicable (no HIPAA)
- Stytch: Not applicable (no HIPAA yet)

**Cost Comparison (B2B SaaS, 25K MAU, SOC 2 required)**:
- Auth0 Professional: $240 + (24,500 × $0.035) = $1,098/month
- Descope Pro: 25,000 × $0.05 = $1,250/month (or volume discount)
- Stytch Growth: $249/month (includes up to 25K MAU)

**Winner for SOC 2-only requirement**: Stytch (best value) or Descope (modern UX)

---

## Use Case Pattern #6: Consumer Apps (Low Friction, Social-First)

### Business Requirements

**Core Needs**:
- Ultra-low friction signup (one-click social login)
- Social authentication as primary method (Google, Apple, Facebook)
- Mobile-first experience (iOS, Android SDKs)
- Anonymous authentication for guest users
- Progressive authentication (use app before creating account)
- Fast authentication flows (<5 seconds signup to first action)
- Email/password as secondary option
- Account linking (merge social and email accounts)

**Technical Needs**:
- Native mobile SDKs (Swift, Kotlin)
- Social provider integrations (OAuth 2.0, OpenID Connect)
- Anonymous user conversion to authenticated
- Account linking and identity merging
- Minimal required user information
- Deferred profile completion
- Fast session initialization
- Offline authentication support

**Use Case Context**:
- Consumer mobile app (gaming, social, productivity)
- Conversion optimization is critical
- Every friction point loses users
- Social login is expected by users
- Mobile-first or mobile-only application

### Provider Fit Analysis

#### Firebase Authentication - Best for Mobile-First Consumer Apps

**Why It Fits**:
- Native iOS and Android SDKs with excellent DX
- Social login providers pre-integrated and easy to configure
- Anonymous authentication with seamless upgrade
- Google Sign-In optimized (instant on Android)
- Free up to 50K MAU (later tiers also free with Firebase)
- Integrated with Firebase ecosystem (Firestore, Storage, etc.)
- Phone authentication with invisible reCAPTCHA
- Account linking between providers

**Best For**:
- Mobile applications (iOS, Android, Flutter)
- Consumer apps with social login priority
- Startups optimizing for conversion
- Teams already using Firebase/GCP
- Apps needing anonymous authentication
- Gaming and consumer productivity apps

**Pricing Model**:
- Free: Unlimited authentication (part of Spark plan)
- Blaze (pay-as-you-go): Phone auth costs ($0.01-0.06 per verification)
- No per-MAU charges for authentication
- Costs tied to phone auth and SMS only

**Consumer-Focused Capabilities**:
- **Social Providers**: Google, Apple, Facebook, Twitter, GitHub, Microsoft
- **Anonymous Auth**: Start using app without account
- **Anonymous Upgrade**: Convert anonymous user to full account
- **Account Linking**: Merge multiple auth methods to one account
- **Google Sign-In**: One-tap on Android, streamlined on iOS
- **Apple Sign-In**: Required for iOS apps, easy integration
- **Phone Auth**: SMS OTP with automatic code detection
- **Email Link**: Passwordless email authentication

**Mobile Optimization**:
- Native SDKs for iOS (Swift), Android (Kotlin), Flutter
- Automatic SMS code detection on Android
- Apple Sign-In integration with native UI
- Google Sign-In with one-tap on Android
- Offline token persistence
- Background session refresh
- Biometric authentication (via native OS)

**Limitations**:
- Web experience not as polished as mobile
- Limited pre-built UI (you build your own)
- Tied to Firebase/Google ecosystem
- No built-in user management dashboard (basic console only)
- Email templates limited customization
- No advanced RBAC or organizations
- Enterprise features minimal (no SSO, SCIM)

#### Supabase Auth - Best for Open Source Mobile Apps

**Why It Fits**:
- Generous free tier: 50,000 MAU
- Social providers easy to configure
- Anonymous sign-ins for guest users
- Mobile SDKs for iOS, Android, Flutter
- Open source (can self-host)
- Magic link and OTP authentication
- Integrated with Supabase database and storage

**Best For**:
- Bootstrapped consumer apps
- Developers wanting open source
- Flutter applications (excellent SDK)
- Apps needing database + auth integration
- Teams optimizing for cost
- Projects wanting self-hosting option

**Pricing Model**:
- Free: 50,000 MAU (best free tier)
- Pro: $25/month, 100,000 MAU
- Phone auth: Pay per SMS (varies by region)
- Self-hosted: Free (manage infrastructure)

**Consumer-Focused Capabilities**:
- **Social Providers**: 20+ including Google, Apple, Facebook, Discord
- **Anonymous Sign-Ins**: Guest users with optional upgrade
- **Phone Auth**: SMS and WhatsApp OTP
- **Magic Links**: Email-based passwordless
- **Account Linking**: Link multiple providers
- **Mobile SDKs**: Flutter, React Native, Swift, Kotlin
- **Email OTP**: Alternative to magic links

**Mobile Experience**:
- Flutter SDK (official, first-class)
- React Native support
- iOS and Android native SDKs
- Deep linking for magic links
- Offline session management
- Auto-refresh tokens

**Limitations**:
- No pre-built UI components (build your own)
- Social login requires more setup than Firebase
- Documentation less comprehensive than Firebase
- Apple Sign-In requires manual configuration
- Phone auth costs extra (pay per SMS)
- Enterprise features minimal
- Support quality depends on tier

#### Clerk - Best for Web-First Consumer Apps

**Why It Fits**:
- Beautiful pre-built social login UI
- One-click social authentication
- Progressive authentication flows
- Account linking with UI components
- User profile management included
- Mobile SDKs (React Native, Expo)
- Free tier: 10,000 MAU

**Best For**:
- Consumer web applications
- React/Next.js consumer apps
- Apps wanting beautiful auth UI
- Teams prioritizing UX and DX
- Web-first apps with mobile companion

**Pricing Model**:
- Free: 10,000 MAU
- Pro: $25/month + $0.02 per MAU
- SMS: $0.055 per message
- Social auth included in all tiers

**Consumer-Focused Capabilities**:
- **Social Providers**: 15+ with easy config
- **Pre-built UI**: Beautiful social login buttons
- **Account Linking**: Automatic account merging
- **Progressive Auth**: Use app, sign up later
- **User Profiles**: Built-in profile management
- **Organization Support**: For team-based consumer apps
- **Session Management**: Automatic token refresh

**Mobile Experience**:
- React Native SDK
- Expo integration
- Deep linking support
- Native iOS and Android (beta)
- Web-optimized (best experience)

**Limitations**:
- More expensive than Firebase/Supabase at scale
- Mobile SDKs less mature than Firebase
- Best for web, mobile is secondary
- No anonymous authentication (yet)
- SMS costs add up for phone auth
- Focused on JavaScript ecosystem
- Not ideal for native mobile apps

### Decision Criteria

**Choose Firebase Authentication if**:
- You're building native mobile app (iOS, Android)
- You need anonymous authentication
- Google Sign-In is important (Android optimization)
- You're using Firebase for other services
- Free tier and low cost matter
- Consumer mobile is primary platform

**Choose Supabase Auth if**:
- You're building with Flutter
- Cost is primary concern (best free tier at 50K MAU)
- You want open source option
- You're using or plan to use Supabase database
- You're comfortable building custom UI
- Self-hosting is valuable long-term

**Choose Clerk if**:
- You're building consumer web app
- Beautiful pre-built UI is important
- You're using React/Next.js
- User profile management is needed
- Developer experience matters most
- Budget allows $25+/month after free tier

**Decision Tree**:
```
Platform priority:
├─ Native mobile (iOS/Android) → Firebase (best mobile SDKs)
├─ Flutter → Supabase (excellent Flutter SDK)
├─ React Native → Clerk or Firebase
└─ Web-first → Clerk (best web UX)

Budget:
├─ Free forever → Firebase (unlimited) or Supabase (50K MAU)
├─ <$100/month → Supabase or Firebase
└─ >$100/month willing → Clerk (best UX)

Anonymous auth needed?
├─ YES (critical) → Firebase or Supabase
└─ NO → Any option

Ecosystem preference:
├─ Google/Firebase → Firebase Auth
├─ Open source → Supabase
└─ Modern JS → Clerk
```

**Cost Comparison (Consumer App, 25K MAU, 50% social, 50% phone)**:
- Firebase: Free (auth) + phone SMS (~$125-750/month depending on region)
- Supabase: Free (under 50K MAU) + phone SMS (~$125-750/month)
- Clerk: Free (under 10K) or $25 + (15K × $0.02) + phone SMS = $325 + SMS

**Social Provider Support**:

| Provider | Firebase | Supabase | Clerk |
|----------|----------|----------|-------|
| **Google** | Yes (optimized) | Yes | Yes |
| **Apple** | Yes | Yes | Yes |
| **Facebook** | Yes | Yes | Yes |
| **Twitter/X** | Yes | Yes | Yes |
| **GitHub** | Yes | Yes | Yes |
| **Discord** | No | Yes | Yes |
| **TikTok** | No | Yes | No |
| **LinkedIn** | No | Yes | Yes |
| **Easy Setup** | Excellent | Good | Excellent |

**Mobile SDK Quality**:
- Firebase: Excellent (native iOS/Android)
- Supabase: Excellent (Flutter), Good (iOS/Android)
- Clerk: Good (React Native), Beta (native)

---

## Use Case Pattern #7: Developer Tools (GitHub-Only, Simple)

### Business Requirements

**Core Needs**:
- GitHub authentication only (developer audience)
- Minimal signup friction for developers
- Access to GitHub user data (repos, orgs, email)
- GitHub OAuth scopes for repository access
- Simple session management
- API key generation for CLI tools
- Team authentication via GitHub organizations
- Open source friendly pricing

**Technical Needs**:
- GitHub OAuth 2.0 integration
- Access to GitHub API on behalf of users
- Webhook for GitHub organization membership changes
- API tokens for programmatic access
- Simple user profile (GitHub username, avatar, email)
- GitHub App integration for repository access
- CLI authentication flow (device code flow)

**Use Case Context**:
- Developer tools (CI/CD, deployment, monitoring)
- Infrastructure and DevOps platforms
- Code analysis and security tools
- GitHub-native applications
- Developer-only audience (no consumer users)

### Provider Fit Analysis

#### Auth0 - Best for GitHub + Extensibility

**Why It Fits**:
- GitHub social connection built-in
- GitHub Enterprise support
- Custom scopes configuration
- Rules/Actions for GitHub API calls
- Extensible for future auth methods
- Management API for automation
- Organizations for team management

**Best For**:
- Developer tools needing flexibility
- Platforms that might add auth methods later
- Teams wanting enterprise GitHub support
- Applications needing custom auth logic
- Companies planning for enterprise sales

**Pricing Model**:
- Free: 7,500 MAU
- Essentials: $35/month + $0.0175 per MAU
- Professional: $240/month + $0.035 per MAU
- GitHub auth included in all tiers

**Developer-Focused Capabilities**:
- **GitHub Connection**: OAuth 2.0 with custom scopes
- **GitHub Enterprise**: Support for GHE servers
- **Actions**: Call GitHub API in auth flow
- **Organizations**: Map to GitHub organizations
- **API Keys**: Management API for automation
- **Machine-to-Machine**: For CLI and automation
- **Custom Domains**: For branded auth experience

**Implementation**:
```javascript
// Auth0 GitHub connection
await auth0.authenticate({
  connection: 'github',
  scope: 'read:user repo read:org',
});

// Access GitHub API with user token
const githubToken = user.identities[0].access_token;
```

**Limitations**:
- Overkill if you only need GitHub auth
- Expensive for simple use case
- Complex setup for basic needs
- Free tier limited (7,500 MAU)
- Dashboard complexity for simple workflow
- Slower than purpose-built GitHub auth

#### Supabase Auth - Best for Cost-Effective GitHub Auth

**Why It Fits**:
- GitHub provider easy to configure
- Free tier: 50,000 MAU (generous)
- Access to GitHub user data
- Simple API for authentication
- Open source (can self-host)
- Integrated with Supabase database
- Custom scopes configuration

**Best For**:
- Bootstrapped developer tools
- Open source projects
- Teams optimizing for cost
- Applications using Supabase database
- Simple GitHub-only authentication
- Developers comfortable with SQL

**Pricing Model**:
- Free: 50,000 MAU (best free tier)
- Pro: $25/month for 100,000 MAU
- GitHub auth included (no additional cost)
- Self-hosted: Free

**Developer-Focused Capabilities**:
- **GitHub Provider**: OAuth with scope config
- **Access Tokens**: Retrieve GitHub access token
- **User Metadata**: GitHub username, email, avatar
- **Database Integration**: Store GitHub data in PostgreSQL
- **Row Level Security**: Database-level authorization
- **API**: Simple auth API
- **Self-Hosted**: Deploy on your infrastructure

**Implementation**:
```javascript
// Supabase GitHub auth
const { user, session } = await supabase.auth.signInWithOAuth({
  provider: 'github',
  options: {
    scopes: 'read:user repo',
  },
});

// Access GitHub token
const githubToken = session.provider_token;
```

**Limitations**:
- No pre-built UI (build your own)
- GitHub Enterprise not officially supported
- Limited team/organization features
- No custom auth logic (no Rules/Actions equivalent)
- Best value requires using Supabase stack
- Documentation less comprehensive for edge cases

#### Clerk - Best for GitHub + Beautiful UI

**Why It Fits**:
- GitHub provider with one-click config
- Beautiful pre-built GitHub sign-in UI
- Organization sync with GitHub orgs
- User management dashboard
- Free tier: 10,000 MAU
- Modern developer experience
- Webhooks for GitHub events

**Best For**:
- Developer tools wanting polished UI
- React/Next.js developer applications
- Teams prioritizing UX for developers
- Applications needing organization management
- Developer tools with web dashboard

**Pricing Model**:
- Free: 10,000 MAU
- Pro: $25/month + $0.02 per MAU
- GitHub auth included
- Organization features included

**Developer-Focused Capabilities**:
- **GitHub Sign-In**: Pre-built UI component
- **GitHub Data**: Access to username, email, avatar
- **Organizations**: Map to GitHub organizations
- **User Profiles**: Built-in profile management
- **Webhooks**: Events for user lifecycle
- **Dashboard**: User management UI
- **Dev/Prod Environments**: Separate instances

**Implementation**:
```jsx
// Clerk GitHub auth
<SignIn.Root>
  <SignIn.Strategy name="oauth_github">
    <SignIn.Action submit>Continue with GitHub</SignIn.Action>
  </SignIn.Strategy>
</SignIn.Root>
```

**Limitations**:
- Best for JavaScript ecosystem
- More expensive than Supabase at scale
- No GitHub Enterprise support
- Limited access to GitHub access token
- Organization sync limited
- Not ideal for CLI-first tools
- Vendor-specific UI components

### Decision Criteria

**Choose Auth0 if**:
- You need GitHub Enterprise support
- You want flexibility to add auth methods later
- Custom auth logic (Actions) is valuable
- You're building for enterprise developers
- Budget supports $35+/month

**Choose Supabase Auth if**:
- Cost is primary concern (best free tier)
- You only need GitHub authentication
- You're using or plan to use Supabase database
- You're comfortable building custom UI
- Open source and self-hosting are valuable
- Simple authentication is sufficient

**Choose Clerk if**:
- You want beautiful pre-built GitHub UI
- You're building with React/Next.js
- User management dashboard is valuable
- Developer experience is priority
- Budget allows $25+/month after 10K MAU

**Decision Tree**:
```
GitHub Enterprise needed?
├─ YES → Auth0 (only option with GHE support)
└─ NO → Based on other factors

Budget:
├─ <$50/month → Supabase (free up to 50K MAU)
├─ $50-200/month → Clerk or Supabase
└─ >$200/month → Auth0 or Clerk

Framework:
├─ React/Next.js → Clerk (best integration)
├─ Backend-heavy → Auth0 or Supabase
└─ CLI tool → Auth0 (device code flow) or Supabase

Need custom UI?
├─ YES (branded) → Build on Supabase or Auth0
└─ NO (pre-built) → Clerk
```

**Cost Comparison (Developer Tool, 5K MAU, GitHub-only)**:
- Auth0: Free (under 7,500 MAU limit)
- Supabase: Free (under 50,000 MAU limit)
- Clerk: Free (under 10,000 MAU limit)

**Cost Comparison (10K MAU)**:
- Auth0: $35 + (2,500 × $0.0175) = $79/month
- Supabase: Free (still under 50K limit)
- Clerk: Free (at 10K MAU limit) or $25 if over

**Winner for GitHub-only, cost-sensitive**: Supabase (free up to 50K MAU)
**Winner for GitHub-only, best DX**: Clerk (beautiful UI, modern API)
**Winner for GitHub Enterprise**: Auth0 (only option)

**Feature Matrix**:

| Feature | Auth0 | Supabase | Clerk |
|---------|-------|----------|-------|
| **GitHub OAuth** | Yes | Yes | Yes |
| **GitHub Enterprise** | Yes | No | No |
| **Custom Scopes** | Yes | Yes | Limited |
| **Access Token Access** | Yes | Yes | Limited |
| **Pre-built UI** | Basic | No | Excellent |
| **Free Tier MAU** | 7,500 | 50,000 | 10,000 |
| **Org Mapping** | Yes | No | Yes |
| **Device Code Flow** | Yes | Limited | No |

---

## Summary Decision Matrix

### Quick Reference: Use Case to Provider Mapping

| Use Case | Primary Need | Best Fit | Alternative | Budget Option |
|----------|--------------|----------|-------------|---------------|
| **Simple SaaS App** | Fast setup + social | Clerk | Auth0, Supabase | Supabase |
| **Enterprise B2B SSO** | SAML/OIDC SSO | WorkOS | Auth0, Descope | Descope |
| **Passwordless/Modern** | Magic links, passkeys | Clerk | Stytch, Descope | Clerk |
| **Multi-Tenant B2B** | Organizations, RBAC | Clerk | Auth0, Propel Auth | Propel Auth |
| **Compliance-Heavy** | HIPAA, SOC 2 | Auth0 | Stytch, Descope | Descope |
| **Consumer Apps** | Social-first mobile | Firebase | Supabase, Clerk | Firebase/Supabase |
| **Developer Tools** | GitHub auth only | Supabase | Clerk, Auth0 | Supabase |

### Key Decision Factors Across Use Cases

**Technical Resources**:
- High technical capacity → Supabase, Auth0, Firebase
- Moderate technical capacity → Clerk, Stytch, Descope
- Low technical capacity → Clerk, Firebase (pre-built UI)

**Budget Constraints**:
- <$50/month → Supabase (50K MAU free), Firebase (free auth)
- $50-200/month → Clerk, Descope, Propel Auth
- $200-1,000/month → Auth0, Stytch, WorkOS
- >$1,000/month → Auth0 Enterprise, WorkOS (Directory Sync)

**Platform Focus**:
- Native mobile (iOS/Android) → Firebase (best mobile SDKs)
- Flutter → Supabase (excellent Flutter SDK)
- React/Next.js → Clerk (best integration)
- Backend-heavy → Auth0, Supabase
- Multi-platform → Auth0, Firebase

**Primary Use Case**:
- Simple auth → Clerk, Supabase, Firebase
- Enterprise SSO → WorkOS, Auth0, Descope
- Passwordless → Clerk, Stytch, Descope
- Multi-tenant B2B → Clerk, Auth0, Propel Auth
- Compliance → Auth0, Descope, Stytch
- Consumer mobile → Firebase, Supabase
- Developer tools → Supabase, Clerk, Auth0

**Scale and Volume**:
- <10K MAU → Free tiers (Clerk, Supabase, Firebase)
- 10K-100K MAU → Clerk, Supabase, Descope
- 100K-1M MAU → Auth0, Clerk, Firebase
- >1M MAU → Auth0 Enterprise, Firebase

**Compliance Needs**:
- HIPAA/BAA → Auth0 (only option)
- SOC 2 → Auth0, Descope, Stytch
- ISO 27001 → Auth0
- Basic compliance → All providers

---

## Hybrid/Multi-Provider Strategies

### When One Provider Isn't Enough

**Strategy #1: Core Auth + Enterprise Add-On**

**Problem**: Need simple auth for most users but enterprise SSO for big customers.

**Solution**: Use Clerk/Supabase for core auth + WorkOS for enterprise SSO.

**Recommended Combination**:
- **Clerk (core auth) + WorkOS (enterprise SSO)**
  - Clerk handles email/password, social login for majority of users
  - WorkOS provides SAML/OIDC SSO for enterprise customers
  - WorkOS Admin Portal for customer self-service SSO setup
  - Total cost: $25 (Clerk) + $0 (WorkOS SSO free) + $125/directory (if Directory Sync)

**Benefits**:
- Best of both: modern auth + enterprise features
- Cost-effective (pay for enterprise only when needed)
- WorkOS SSO is free for unlimited users
- Self-service SSO reduces support burden
- Can sell enterprise features without rebuilding auth

**Drawbacks**:
- Two providers to integrate and manage
- User management split across platforms
- More complex user flow logic
- Testing complexity increases
- Monitoring two systems

**Implementation**:
```javascript
// Route based on domain or organization
if (user.organization.hasSSO) {
  // Route to WorkOS SSO
  await workos.sso.getAuthorizationURL({
    organization: user.organizationId,
    redirectURI: 'https://app.com/callback',
  });
} else {
  // Route to Clerk standard auth
  await clerk.signIn.create({ ... });
}
```

---

**Strategy #2: Regional Compliance Split**

**Problem**: Need HIPAA in US but prefer cost-effective auth for international users.

**Solution**: Use Auth0 (US, HIPAA) + Supabase (International, cost-effective).

**Recommended Combination**:
- **Auth0 Enterprise (US healthcare) + Supabase (international)**
  - Auth0 with BAA for US healthcare users
  - Supabase for international users (cheaper, sufficient compliance)
  - Route based on user location or market

**Benefits**:
- Compliance where needed (HIPAA for US healthcare)
- Cost savings (Supabase free tier for international)
- Optimized for each market's requirements
- Regulatory arbitrage

**Drawbacks**:
- Complex routing logic by geography
- Two user databases to manage
- Different UX across regions
- Migration complexity if users move
- Support complexity

---

**Strategy #3: Consumer + Developer Split**

**Problem**: Need social login for consumers but GitHub-only for developers.

**Solution**: Use Firebase (consumer mobile) + Supabase (developer web).

**Recommended Combination**:
- **Firebase (consumer mobile app) + Supabase (developer dashboard)**
  - Firebase for mobile app with social login
  - Supabase for web developer dashboard with GitHub auth
  - Separate user bases, optimized for each audience

**Benefits**:
- Right tool for each audience
- Firebase excels at mobile consumer
- Supabase cost-effective for developer tools
- Independent scaling and optimization

**Drawbacks**:
- Completely separate user management
- No unified admin dashboard
- Cross-platform users problematic
- Two integrations to maintain

---

### Gap Analysis: What No Single Provider Does Well

**Gap #1: Affordable Enterprise SSO for Startups**
- **Problem**: Auth0 Enterprise ($2K+/month) too expensive; Clerk Enterprise pricing unclear
- **Solutions**:
  - Use Descope (SSO on free tier, limited scale)
  - Use Propel Auth ($150/month with SSO)
  - Hybrid: Clerk + WorkOS (free SSO, pay for Directory Sync if needed)

**Gap #2: Native Mobile UX + Backend Flexibility**
- **Problem**: Firebase great for mobile but locked to Google; Clerk great for web but mobile secondary
- **Solutions**:
  - Use Firebase for mobile, separate backend auth (JWT validation)
  - Use Supabase (good Flutter, backend flexibility)
  - Accept trade-off: Firebase mobile focus or Clerk web focus

**Gap #3: Open Source + Enterprise Features**
- **Problem**: Supabase open source but lacks enterprise SSO; Auth0 has enterprise but proprietary
- **Solutions**:
  - Use Supabase + build custom SSO (high effort)
  - Wait for Supabase enterprise features (roadmap)
  - Accept trade-off: open source or enterprise features

**Gap #4: HIPAA Compliance at Startup Prices**
- **Problem**: Only Auth0 has BAA, requires Enterprise tier ($2K+/month)
- **Solutions**:
  - Delay HIPAA compliance until revenue justifies cost
  - Use Auth0 Professional ($240) with careful PHI handling (not ideal)
  - Self-host open source with custom HIPAA setup (high complexity)

**Gap #5: Consumer Mobile + Multi-Tenant B2B**
- **Problem**: Firebase great for consumer mobile but no B2B organizations; Clerk has organizations but web-first
- **Solutions**:
  - Use Firebase + build custom organization layer
  - Use Clerk + accept less optimal mobile experience
  - Use Supabase + build both UI and organizations (most work)

**Gap #6: Passwordless + Full Feature Set**
- **Problem**: Stytch passwordless-only; Clerk has passwordless but includes passwords too
- **Solutions**:
  - Use Stytch and enforce passwordless-only in product
  - Use Clerk and disable password auth (keep passwordless only)
  - Accept that passwordless providers are focused/limited

---

## Migration Considerations

### When to Switch Providers

**Scenario #1: Outgrowing Free Tier**
- **Trigger**: Approaching 10K MAU (Clerk) or 50K MAU (Supabase)
- **Consideration**: Evaluate paid tier cost vs. switching to another free tier
- **Action**: If Clerk $25+/month too expensive, consider Supabase (free to 50K)
- **Migration Complexity**: Medium (export users, re-integrate, test)

**Scenario #2: Enterprise Customer Demands SSO**
- **Trigger**: Enterprise prospect requires SAML SSO as deal requirement
- **Consideration**: Does current provider support SSO? At what cost?
- **Action**: Add WorkOS for SSO or upgrade to Auth0/Descope Enterprise
- **Migration Complexity**: Low (add-on approach) to High (full migration)

**Scenario #3: Compliance Requirement Emerges**
- **Trigger**: Customer or regulation requires HIPAA/SOC 2
- **Consideration**: Does current provider have certification? BAA available?
- **Action**: If HIPAA needed, migrate to Auth0 (only option with BAA)
- **Migration Complexity**: High (compliance testing required)

**Scenario #4: Cost Optimization at Scale**
- **Trigger**: Auth costs >$500/month and growing
- **Consideration**: Can you reduce costs with different provider or self-hosting?
- **Action**: Evaluate Firebase (free auth) or Supabase (cheaper) or self-host
- **Migration Complexity**: High (large user base to migrate)

### Migration Checklist

**Phase 1: Planning (Week 1-2)**
- [ ] Audit current auth usage (MAU, features used, integrations)
- [ ] Export user database (emails, metadata, auth methods)
- [ ] Test new provider with small subset (100-1K users)
- [ ] Plan password migration (hashed passwords, re-auth, or force reset)
- [ ] Map features (ensure new provider supports all current features)
- [ ] Notify users of upcoming changes (if visible)

**Phase 2: Parallel Setup (Week 3-4)**
- [ ] Set up new provider account
- [ ] Configure authentication methods (social, email, SSO)
- [ ] Build or configure UI components
- [ ] Update application code to support both providers
- [ ] Set up webhook handling for new provider
- [ ] Test authentication flows end-to-end

**Phase 3: Gradual Migration (Week 5-6)**
- [ ] Start with internal team users
- [ ] Migrate non-critical user segments
- [ ] Monitor error rates and support tickets
- [ ] Gradually increase percentage to new provider
- [ ] Keep old provider active for rollback
- [ ] Test edge cases (password reset, account linking, etc.)

**Phase 4: Complete Cutover (Week 7-8)**
- [ ] Migrate remaining users
- [ ] Update all client applications (web, mobile)
- [ ] Remove old provider code (keep for emergency rollback)
- [ ] Cancel or downgrade old provider account
- [ ] Document new authentication flows
- [ ] Update security and compliance documentation

**Migration Risks to Manage**:
- User lockout (can't login after migration)
- Lost user metadata or profile data
- Broken integrations (webhooks, API calls)
- Social login connection issues (re-authorization)
- Session invalidation (force re-login)
- Password hash incompatibility (force password reset)
- Analytics and audit log history lost

---

## Next Steps After Choosing a Provider

### Implementation Checklist

1. **Account Setup and Configuration**:
   - Create provider account and verify email
   - Set up development and production environments
   - Configure authentication methods (social, email, SSO)
   - Set up DNS records if custom domain required
   - Enable two-factor authentication for admin account

2. **Integration Development**:
   - Install SDKs or libraries for your framework
   - Implement signup and login flows
   - Build or configure UI components
   - Add password reset and email verification
   - Implement session management and token refresh
   - Add logout and account deletion flows

3. **Security Configuration**:
   - Configure password policies (length, complexity)
   - Enable MFA options for users
   - Set up rate limiting and brute force protection
   - Configure session timeout and idle timeout
   - Add CORS and allowed origins
   - Set up webhook signature verification

4. **User Management**:
   - Build admin dashboard or use provider's UI
   - Implement user search and filtering
   - Add user blocking/suspension capabilities
   - Configure user metadata and profile fields
   - Set up user export for backups
   - Plan for GDPR data deletion requests

5. **Monitoring and Logging**:
   - Set up authentication event logging
   - Configure alerts for suspicious activity
   - Monitor signup and login conversion rates
   - Track authentication errors and failures
   - Set up uptime monitoring for auth endpoints
   - Plan for audit log retention

6. **Testing**:
   - Test all authentication flows (signup, login, reset)
   - Test social login for each provider
   - Test MFA flows (SMS, TOTP, WebAuthn)
   - Test session management (refresh, expiration)
   - Load test for expected user volume
   - Security test (penetration testing, vulnerability scan)

7. **Documentation and Training**:
   - Document authentication flows for team
   - Create runbooks for common issues
   - Train support team on auth troubleshooting
   - Document security policies and compliance
   - Create user-facing documentation (how to login, reset password)

---

## Appendix: Provider Comparison Tables

### Pricing Comparison (10K MAU)

| Provider | Monthly Cost | Free Tier | Notes |
|----------|--------------|-----------|-------|
| **Clerk** | Free | 10K MAU | Best free tier for features |
| **Supabase** | Free | 50K MAU | Best free tier for volume |
| **Firebase** | Free | Unlimited auth | Only pay for phone auth SMS |
| **Auth0** | $35+ | 7.5K MAU | Minimum 500 MAU on paid |
| **Descope** | Free | 7.5K MAU | SSO included on free tier |
| **Stytch** | Free | 5K MAU | Lower free tier |
| **WorkOS** | Free | 1M users (SSO) | SSO free, Directory Sync $125/conn |
| **Propel Auth** | $150 | 1K MAU | Includes SSO |

### Pricing Comparison (50K MAU)

| Provider | Monthly Cost | Per-User Cost | Notes |
|----------|--------------|---------------|-------|
| **Supabase** | Free | $0 | Still under free tier |
| **Firebase** | Free | $0 | Auth always free |
| **Clerk** | $825 | $0.02 | $25 + (40K × $0.02) |
| **Descope** | $2,500 | $0.05 | 50K × $0.05 |
| **Auth0** | $1,933 | $0.035 | $240 + (49.5K × $0.035) |
| **Stytch** | $249-499 | Tiered | Growth tier 25K-50K range |

### Feature Comparison Matrix

| Feature | Clerk | Auth0 | Supabase | Firebase | WorkOS | Descope | Stytch | Propel Auth |
|---------|-------|-------|----------|----------|--------|---------|--------|-------------|
| **Email/Password** | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes |
| **Social Login** | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes |
| **Magic Links** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Passkeys/WebAuthn** | Yes | Yes | Yes | No | No | Yes | Yes | Yes |
| **Phone Auth (SMS)** | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes |
| **SAML SSO** | Enterprise | Enterprise | Enterprise | No | Yes (free) | All tiers | No | Startup+ |
| **OIDC SSO** | Enterprise | All tiers | All tiers | No | Yes (free) | All tiers | No | Startup+ |
| **Directory Sync (SCIM)** | No | Add-on | No | No | Yes ($125/conn) | Roadmap | No | No |
| **Organizations/Multi-tenant** | Yes | Yes | No | No | Yes | Yes | Limited | Yes |
| **RBAC** | Yes | Yes | Limited | Limited | Yes | Yes | No | Yes |
| **MFA (TOTP)** | Yes | Yes | Yes | No | No | Yes | Yes | Yes |
| **Pre-built UI** | Excellent | Basic | No | Limited | No | Good | No | Good |
| **Mobile SDKs** | RN, Expo | Native | Native, Flutter | Native (iOS/Android) | Limited | Native | Limited | Limited |
| **Anonymous Auth** | No | No | Yes | Yes | No | No | No | No |
| **SOC 2 Type II** | Yes | Yes | No | Yes (Google) | Yes | Yes | Yes | No |
| **HIPAA/BAA** | No | Yes | No | Yes (GCP) | No | No | Roadmap | No |
| **Self-Hosted** | No | No | Yes | No | No | No | No | No |
| **Open Source** | No | No | Yes | No | No | No | No | No |

### Best-in-Class by Category

**Best Free Tier (Volume)**: Supabase (50K MAU) or Firebase (unlimited auth)
**Best Free Tier (Features)**: Clerk (10K MAU with full features)
**Best Pre-Built UI**: Clerk (beautiful React components)
**Best Mobile SDKs**: Firebase (native iOS/Android, Flutter)
**Best for Enterprise SSO**: WorkOS (free SSO, self-service Admin Portal)
**Best for Compliance (HIPAA)**: Auth0 (only provider with BAA)
**Best for Compliance (SOC 2, affordable)**: Descope (included on free tier)
**Best for Passwordless**: Clerk or Stytch (purpose-built)
**Best for Multi-Tenant B2B**: Clerk (organizations built-in)
**Best for Developer Tools**: Supabase (open source, generous free tier)
**Best for Consumer Mobile**: Firebase (optimized for mobile)
**Best for Cost at Scale**: Supabase or Firebase (free/cheap)
**Best Developer Experience**: Clerk (modern, well-documented)
**Best for Customization**: Auth0 (Actions/Rules, extensive APIs)
**Best Open Source**: Supabase (can self-host)

---

*This analysis is part of the MPSE (Multi-Phase Systematic Evaluation) discovery methodology for experiment 3.012: Authentication & Authorization Services.*
