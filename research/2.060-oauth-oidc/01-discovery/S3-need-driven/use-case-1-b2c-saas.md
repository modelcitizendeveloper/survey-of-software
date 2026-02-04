# Use Case 1: B2C SaaS Application

## Use Case Profile

**Scenario**: Building a project management SaaS app (like Trello, Asana, Linear) for individual consumers and small teams.

**Requirements:**
- Email/password authentication with email verification
- Social login (Google, GitHub, Microsoft) for low-friction signup
- Password reset flow with email delivery
- User profile management (update email, name, avatar)
- Basic role-based access (admin vs member)
- Session management across web and mobile
- 1K-100K monthly active users (typical growth trajectory)
- Simple, fast time to market (launch in 4-8 weeks)

**Technical Context:**
- React frontend (Next.js or Vite)
- Node.js backend (Express, Fastify, or Next.js API routes)
- PostgreSQL for app data
- Hosted on Vercel, Railway, or AWS

**Business Context:**
- Bootstrapped startup or small team (2-4 engineers)
- Budget-conscious ($0-100/month for auth)
- Need to ship MVP quickly (weeks, not months)
- May grow to enterprise features later (SSO), but not immediate

## OAuth/OIDC Fit Analysis

### What OAuth/OIDC Provides for This Use Case

**Standard OAuth Flows:**
- Authorization code flow for web login (redirect to IdP, redirect back with code)
- PKCE for mobile security (if building mobile app later)
- Refresh token mechanism (long-lived sessions without re-login)
- Social login via OAuth (Google, GitHub, Microsoft use OAuth 2.0)

**Token-Based Authentication:**
- JWT access tokens with standard claims (sub, email, name)
- ID tokens for user information (OpenID Connect layer)
- Refresh tokens for session renewal (standard mechanism)

**Example OAuth/OIDC Login Flow:**

```javascript
// Step 1: Redirect to OAuth provider
app.get('/login', (req, res) => {
  const authUrl = `https://auth-provider.com/authorize?
    response_type=code&
    client_id=${CLIENT_ID}&
    redirect_uri=${REDIRECT_URI}&
    scope=openid profile email&
    state=${CSRF_TOKEN}`;
  res.redirect(authUrl);
});

// Step 2: Handle callback
app.get('/callback', async (req, res) => {
  const { code } = req.query;

  // Exchange code for tokens
  const response = await fetch('https://auth-provider.com/token', {
    method: 'POST',
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: REDIRECT_URI,
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
    }),
  });

  const { access_token, refresh_token, id_token } = await response.json();

  // Store tokens in session
  req.session.tokens = { access_token, refresh_token };
  res.redirect('/dashboard');
});

// Step 3: Refresh tokens when expired
async function refreshAccessToken(refresh_token) {
  const response = await fetch('https://auth-provider.com/token', {
    method: 'POST',
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token,
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
    }),
  });

  return await response.json();
}
```

**What's Standardized:**
- Authorization URL structure (predictable across OAuth providers)
- Token exchange endpoint (same flow for Auth0, Keycloak, Okta)
- Refresh token grant type (standard way to renew tokens)
- JWT token format (can decode and validate consistently)

### What OAuth/OIDC Does NOT Provide

**User Management (100% Proprietary):**
- Creating new users (signup endpoint, validation, email verification)
- Updating user profiles (change email, name, avatar)
- Deleting users (GDPR right to deletion, data cleanup)
- User search and filtering (admin dashboard functionality)

**Password Reset Flow (100% Proprietary):**
- Generating password reset tokens
- Sending reset emails with custom templates
- Validating reset tokens and updating passwords
- Rate limiting password reset attempts

**Multi-Factor Authentication (100% Proprietary):**
- TOTP setup (QR code generation, secret storage)
- SMS delivery (Twilio integration, phone verification)
- WebAuthn/passkeys (credential storage, challenge-response)
- Backup codes (generation, storage, validation)

**Social Login UI (100% Proprietary):**
- "Sign in with Google" button styling
- OAuth consent screen branding
- Account linking (merge Google and email accounts)
- Social profile data mapping

**Email Infrastructure (100% Proprietary):**
- Transactional email delivery (SendGrid, Postmark, SES)
- Email template design and customization
- Email deliverability monitoring
- Bounce and complaint handling

**Example: What You Still Build Even with OAuth/OIDC:**

```javascript
// User signup (NOT standardized by OAuth/OIDC)
app.post('/signup', async (req, res) => {
  const { email, password, name } = req.body;

  // Validate email, password strength (proprietary logic)
  // Hash password with bcrypt/Argon2 (provider-specific)
  // Insert into user database (provider-specific schema)
  // Send verification email (provider-specific templates)
  // Generate email verification token (proprietary)

  // OAuth/OIDC doesn't help with any of this
});

// Password reset (NOT standardized by OAuth/OIDC)
app.post('/reset-password', async (req, res) => {
  const { email } = req.body;

  // Generate reset token (proprietary)
  // Send reset email (proprietary templates)
  // Store token with expiration (provider-specific)

  // OAuth/OIDC doesn't help with any of this
});

// Admin API: List users (NOT standardized by OAuth/OIDC)
app.get('/admin/users', async (req, res) => {
  // Query user database (provider-specific API)
  // Filter, sort, paginate (proprietary)
  // Return user data (provider-specific schema)

  // Auth0: auth0.users.getAll()
  // Keycloak: keycloak.users.find()
  // Completely different APIs, must rewrite when switching
});
```

### Provider Recommendations for B2C SaaS

**Option 1: Clerk (Recommended for React/Next.js)**

**Why it fits:**
- Pre-built React components (`<SignIn />`, `<UserButton />`, `<SignUp />`)
- OAuth/OIDC under the hood, but abstracts complexity
- Social login configured in dashboard (Google, GitHub in 5 minutes)
- Free tier: 10,000 MAU (sufficient for MVP and early growth)
- Excellent developer experience (modern API, good docs)

**Setup time:** 2-3 hours
- Install Clerk SDK: 15 minutes
- Configure social providers: 30 minutes
- Add Clerk components to app: 1 hour
- Test signup/login flows: 30 minutes

**Is this OAuth/OIDC?** Yes, Clerk uses OAuth/OIDC flows under the hood, but you don't write OAuth code directly. Clerk abstracts the complexity.

**Migration effort if switching away:** 80-100 hours
- Export users from Clerk: 10-15 hours
- Rebuild signup/login UI: 15-20 hours
- Migrate user data: 20-30 hours
- Rewrite admin API calls: 20-25 hours
- Test migration: 10-15 hours

**Verdict:** OAuth/OIDC provides minimal portability value here. You save maybe 10-15 hours on OAuth flow rewrite, but still 65-85 hours of proprietary migration work.

**Option 2: Firebase Authentication (Non-OAuth/OIDC Alternative)**

**Why it fits:**
- Fastest setup (3-4 hours total)
- Social login with simple SDK (1 line per provider)
- Free unlimited authentication (only pay for phone auth SMS)
- Mobile SDKs excellent (native iOS/Android)
- Integrated with Firebase ecosystem (Firestore, Storage)

**Setup time:** 3-4 hours
- Add Firebase SDK: 30 minutes
- Configure social providers: 1 hour
- Implement signup/login: 1 hour
- Email verification setup: 30 minutes
- Test flows: 30-60 minutes

**Is this OAuth/OIDC?** No. Firebase uses proprietary SDK and proprietary auth tokens. Not OAuth/OIDC compliant.

**Migration effort if switching away:** 100-120 hours
- Export users from Firebase: 15-20 hours (proprietary format)
- Rewrite auth code: 25-35 hours (Firebase SDK → new SDK)
- Migrate password hashes: 20-25 hours (Firebase format incompatible)
- Rebuild admin integration: 20-25 hours
- Test migration: 15-20 hours

**Verdict:** Non-OAuth/OIDC, but faster setup (3-4 hours vs 20-40 hours for OAuth/OIDC). Migration difficulty similar to OAuth providers (100-120 hours vs 80-100 hours).

**Option 3: Supabase Auth (Partial OAuth/OIDC)**

**Why it fits:**
- Generous free tier: 50,000 MAU (best for bootstrapped startups)
- Social login easy to configure (OAuth-based)
- Open source (can self-host if needed)
- Integrated with Supabase database (PostgreSQL with Row Level Security)

**Setup time:** 5-8 hours
- Set up Supabase project: 30 minutes
- Configure social providers: 1-2 hours
- Build custom UI (no pre-built components): 3-4 hours
- Implement auth logic: 1-2 hours
- Test flows: 30-60 minutes

**Is this OAuth/OIDC?** Partially. Supabase uses OAuth/OIDC for social login, and JWT tokens are OAuth-compatible. But user management APIs are proprietary.

**Migration effort if switching away:** 90-110 hours
- Export users: 15-20 hours
- Rebuild UI (Supabase has no components): 20-25 hours
- Migrate user data: 20-25 hours
- Rewrite APIs: 20-25 hours
- Test migration: 10-15 hours

**Verdict:** Best free tier (50K MAU) but requires more setup work (5-8 hours). Migration difficulty similar to other providers despite OAuth/OIDC usage.

**Option 4: Auth0 (Full OAuth/OIDC, Overkill)**

**Why it's NOT ideal:**
- Complex setup (20-40 hours for full OAuth/OIDC implementation)
- Expensive at scale ($240/month Professional tier + $0.035 per MAU)
- Overkill for simple B2C SaaS (enterprise features not needed)
- Steep learning curve (Actions, Rules, extensive API)

**Setup time:** 20-40 hours
- Learn Auth0 concepts: 3-5 hours
- Configure OAuth/OIDC flows: 5-8 hours
- Implement authorization code flow: 5-8 hours
- Add social login: 3-5 hours per provider
- Set up refresh tokens: 3-5 hours
- Build custom UI: 5-10 hours (Auth0 Universal Login limited)
- Test extensively: 5-8 hours

**Is this OAuth/OIDC?** Yes, full OAuth 2.0 / OpenID Connect compliance.

**Migration effort if switching away:** 100-150 hours
- Export users: 15-20 hours
- Rewrite OAuth flows: 15-25 hours (even to another OAuth provider)
- Migrate user data: 25-35 hours
- Rewrite admin APIs: 25-35 hours
- Test migration: 15-20 hours

**Verdict:** OAuth/OIDC compliance doesn't save you on migration (still 100-150 hours). Setup time (20-40 hours) is 5-10× longer than Firebase (3-4 hours).

### OAuth/OIDC Value Proposition for B2C SaaS

**Setup Cost:**
- OAuth/OIDC provider (Auth0, Keycloak): 20-40 hours
- Non-OAuth provider (Firebase, Clerk): 3-8 hours
- **Additional cost of OAuth/OIDC: 15-30 hours**

**Migration Savings:**
- OAuth Provider A → OAuth Provider B: 80-120 hours
- Non-OAuth (Firebase) → Another provider: 100-120 hours
- **OAuth/OIDC saves: 15-30 hours per migration**

**Break-Even Analysis:**

```
Additional setup cost: 20 hours × $200/hour = $4,000
Savings per migration: 20 hours × $200/hour = $4,000

Break-even: Need 1 migration within 3-5 years

Probability of switching:
- Year 1: 5% (just launched, won't switch)
- Year 2: 10% (if Firebase gets expensive)
- Year 3: 15% (if enterprise features needed)

Expected migrations over 5 years: 0.05 + 0.10 + 0.15 + 0.15 + 0.15 = 0.60

Expected value: 0.60 migrations × $4,000 saved = $2,400
Setup cost: $4,000
Net value: -$1,600 (NEGATIVE ROI)
```

**Verdict for B2C SaaS:** OAuth/OIDC has NEGATIVE ROI. The 20-40 hour setup cost outweighs the 15-30 hour migration savings unless you're extremely likely to switch providers (>60% probability in 5 years).

## Recommended Approach for B2C SaaS

### Tier 1: Start with Fastest Solution (Not OAuth/OIDC)

**Recommendation:** Use Clerk or Firebase, NOT raw OAuth/OIDC

**Clerk for web-first (React/Next.js):**
- Setup: 2-3 hours
- Free: 10,000 MAU
- Pro: $25/month + $0.02/MAU
- Uses OAuth/OIDC under hood, but abstracts complexity
- Pre-built UI components

**Firebase for mobile-first:**
- Setup: 3-4 hours
- Free: Unlimited auth
- No OAuth/OIDC, but fastest to market
- Excellent mobile SDKs

**Supabase for cost-conscious:**
- Setup: 5-8 hours
- Free: 50,000 MAU (best free tier)
- Partial OAuth/OIDC
- Requires building custom UI

### Tier 2: Consider Raw OAuth/OIDC Only If...

**Scenario A: You're Building Multi-App Ecosystem**
- Have 3+ separate apps needing unified SSO
- OAuth/OIDC enables single sign-on across apps
- Worth 20-40 hour setup to centralize auth
- Use: Keycloak (self-hosted) or Auth0 (managed)

**Scenario B: You Have OAuth/OIDC Expertise In-House**
- Team already knows OAuth flows deeply
- Can implement in 10-15 hours instead of 20-40 hours
- Comfort with OAuth complexity
- Use: Auth0 or Keycloak

**Scenario C: Enterprise Features on Roadmap**
- Planning B2B pivot with customer SSO in 6-12 months
- OAuth/OIDC providers (Auth0) better handle enterprise SSO
- Early investment in OAuth foundation
- Use: Auth0 Professional tier

### Tier 3: Avoid Raw OAuth/OIDC If...

**Scenario A: Need to Ship MVP in 2-4 Weeks**
- 20-40 hour OAuth setup eats 50%+ of timeline
- Firebase 3-4 hours leaves more time for product features
- Can always migrate later if needed

**Scenario B: Budget <$100/Month**
- Auth0 Professional ($240/month) too expensive
- Firebase (free) or Supabase (free to 50K MAU) better
- Clerk free tier (10K MAU) good balance

**Scenario C: Simple Email/Password Only**
- No social login, no multi-app SSO
- Session cookies simpler than OAuth redirects
- OAuth/OIDC complexity not justified

## Trade-Offs Summary

### What You Gain with OAuth/OIDC

**Technical:**
- Standard authorization code flow (portable across providers)
- Standard token formats (JWT access tokens, ID tokens)
- Standard refresh mechanism (consistent token renewal)

**Portability:**
- OAuth flow code somewhat portable (~15-30 hours saved in migration)
- Can switch between Auth0, Keycloak, Okta with less rewrite
- Token validation logic portable

**Flexibility:**
- Easier to add second app with SSO later
- Mobile app can use same OAuth provider (PKCE flow)
- Third-party OAuth integrations simpler

### What You Lose with OAuth/OIDC

**Time to Market:**
- 20-40 hour setup vs 3-8 hours for Firebase/Clerk
- 2-3 weeks extra engineering time
- Delayed product feature development

**Simplicity:**
- OAuth redirect flows more complex than session cookies
- Token refresh logic added complexity
- Debugging OAuth flows harder (state parameters, PKCE)

**Cost:**
- Auth0 Professional: $240/month + $0.035/MAU
- Firebase: Free auth
- Supabase: Free to 50K MAU
- Clerk: Free to 10K MAU, then $25/month

**User Experience:**
- OAuth redirects feel slower than direct login
- Users confused by redirect to auth provider
- Social login requires same redirect flow

### Honest Portability Assessment

**If you use Firebase (non-OAuth/OIDC):**
- Migration to Auth0: 100-120 hours
- Locked into Firebase until you invest those 100 hours

**If you use Auth0 (OAuth/OIDC):**
- Migration to Keycloak: 80-100 hours (saved 15-30 hours)
- Still locked into Auth0, just slightly less

**Verdict:** OAuth/OIDC reduces lock-in from 100-120 hours to 80-100 hours. Still significant lock-in (30% portable, 70% proprietary).

Compare to OpenTelemetry:
- Backend switch: 1-4 hours (95% portable)
- Minimal lock-in

## ROI Calculation for B2C SaaS

**Scenario: Bootstrapped SaaS, 5K MAU, React frontend**

**Option A: Firebase (Non-OAuth/OIDC)**
- Setup: 3 hours × $200/hour = $600
- Monthly cost: $0 (free auth)
- Year 1 total: $600

**Option B: Clerk (OAuth/OIDC under hood)**
- Setup: 2 hours × $200/hour = $400
- Monthly cost: $0 (under 10K MAU free tier)
- Year 1 total: $400

**Option C: Auth0 (Raw OAuth/OIDC)**
- Setup: 30 hours × $200/hour = $6,000
- Monthly cost: $35 + (4,500 × $0.0175) = $114/month
- Year 1 total: $6,000 + $1,368 = $7,368

**Winner:** Clerk ($400) or Firebase ($600)

**Auth0 costs 15-18× more in Year 1.** You'd need to migrate providers 15-18 times to justify OAuth/OIDC investment. Unrealistic.

## Decision Matrix

```
Choose Firebase if:
├─ Native mobile app (iOS/Android) → Firebase mobile SDKs best
├─ Need to ship in 1-2 weeks → Fastest setup (3-4 hours)
├─ Budget $0 → Free unlimited auth
└─ Want to avoid vendor → Can self-host Firebase alternatives

Choose Clerk if:
├─ React/Next.js app → Best React integration
├─ Want pre-built UI → Beautiful components included
├─ Budget $0-100/month → Free to 10K MAU, then $25/month
└─ Developer experience priority → Modern API, great docs

Choose Supabase if:
├─ Budget $0 and >10K MAU → Free to 50K MAU
├─ Want open source → Can self-host
├─ Using Supabase database → Integrated auth
└─ Comfortable building custom UI → No pre-built components

Choose Auth0 (OAuth/OIDC) if:
├─ Multi-app ecosystem → Need unified SSO
├─ Enterprise roadmap → B2B SSO in 6-12 months
├─ OAuth expertise → Team knows OAuth deeply
└─ Budget >$200/month → Can afford Professional tier
```

## Conclusion for B2C SaaS Use Case

**OAuth/OIDC Recommendation: Skip for MVP, Reconsider at Scale**

**Use Firebase, Clerk, or Supabase for B2C SaaS:**
1. Faster setup (3-8 hours vs 20-40 hours)
2. Lower cost (free tiers vs $240/month)
3. Simpler implementation (abstracts OAuth complexity)
4. Migration difficulty similar (80-120 hours either way)

**Reconsider OAuth/OIDC when:**
- Growing to 100K+ MAU (provider costs hit $500+/month)
- Adding second app needing SSO (multi-app use case emerges)
- Pivoting to B2B with enterprise SSO (customer requirements change)
- Current provider becomes expensive (migration justified)

**The honest verdict:** For B2C SaaS MVP, OAuth/OIDC adoption is a premature optimization. The 20-40 hour setup cost and $240/month+ pricing don't justify the 15-30 hour migration savings. Start with Firebase/Clerk/Supabase, migrate to OAuth/OIDC later if needed.

**ROI: Negative** (-$1,600 over 5 years) unless enterprise pivot or multi-app ecosystem emerges.
