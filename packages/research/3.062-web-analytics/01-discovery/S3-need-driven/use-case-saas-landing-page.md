# Use Case: SaaS Landing Page

**Traffic:** ~100,000 pageviews/month
**Priority:** Conversion tracking, privacy-focused, professional
**Technical Skill:** Developer-friendly, early-stage startup

## Scenario Description

A bootstrapped SaaS startup with a marketing website and product landing pages. The team needs to track conversions, optimize marketing spend, and demonstrate traction to early customers and potential investors.

**Typical Examples:**
- B2B SaaS landing page
- Freemium product website
- Early-stage startup marketing site
- Developer tool landing page
- Waitlist/beta signup page

## Requirements Analysis

### Must-Have Requirements (4 critical)

1. **Cost: <$30/month**
   - Bootstrapped budget constraints
   - Need room for other tools (email, hosting, etc.)
   - Must prove ROI quickly

2. **Privacy: GDPR/CCPA compliant for global customers**
   - Serving EU customers from day one
   - Avoid cookie banner friction on landing page
   - Build trust with privacy-conscious developers

3. **Real-time: Data visible within 1 minute**
   - Monitor campaign launches
   - Immediate feedback on changes
   - Respond to traffic spikes

4. **Setup: <15 minutes**
   - Small team, limited setup time
   - Single developer implementation
   - Works immediately

### Nice-to-Have Requirements (11 additional)

5. **Custom events** - Track signups, demo requests, feature usage
6. **Simple funnels** - 2-3 step conversion tracking (visit → signup → activation)
7. **API access** - Embed key metrics in internal dashboards
8. **Data retention: 12+ months** - Year-over-year comparison
9. **Script performance: <3KB** - Fast page loads for conversion
10. **Reliability: 99.5%+ uptime** - Always available
11. **Export: CSV for board reports** - Monthly metric exports
12. **Team access: 2-3 users** - Founders and early hires
13. **Support: Email with <48hr response** - When things break
14. **No vendor lock-in** - Ability to migrate data
15. **Professional appearance** - Dashboard for investor demos

## Provider Evaluation

### Option 1: PostHog Free Tier (94% fit) - RECOMMENDED

**Scoring:**
- Cost: Free for 1M events/month ✅ 100%
- Privacy: Cookie-less mode, GDPR-capable ⚠️ 90%
- Real-time: Yes ✅ 100%
- Setup: 5-10 minutes ✅ 90%
- Custom events: Full event-based tracking ✅ 100%
- Simple funnels: Advanced funnels included ✅ 100%
- API access: Comprehensive API ✅ 100%
- Data retention: 7 years on free tier ✅ 100%
- Script performance: ~5 KB (heavier) ⚠️ 70%
- Reliability: 99.9%+ ✅ 100%
- Export: Multiple formats ✅ 100%
- Team access: Unlimited users ✅ 100%
- Support: Community only on free tier ⚠️ 60%
- No lock-in: Self-host option + exports ✅ 100%
- Professional: Modern dashboard ✅ 100%

**Overall: 14.1/15 = 94%**

**Strengths:**
- **Funnels included on free tier** (critical differentiator)
- Event-based tracking superior for SaaS metrics
- 7-year data retention (exceptional)
- Session replay (5K replays free) for debugging UX issues
- Unlimited team members
- Self-host option prevents vendor lock-in
- Purpose-built for product-led growth

**Gaps:**
- Heavier script (5KB vs <2KB ideal) - may impact landing page speed
- Community support only on free tier (no SLA)
- Cookie-less mode requires configuration (not default)

**Why Recommended:**
PostHog is the only free option that includes funnels, which are essential for tracking landing page → signup → activation conversions. For a bootstrapped startup, getting $450/month worth of features (funnels, session replay, unlimited retention) at zero cost is massive. The 1M event limit covers 100K pageviews with generous headroom for custom events.

**Risk Consideration:**
Dependency on free tier stability. Plan migration to paid tier if usage exceeds 1M events or need SLA.

### Option 2: Fathom $14/month (93% fit)

**Scoring:**
- Cost: $14/month ✅ 100%
- Privacy: Cookie-less, GDPR-compliant, Canada/EU servers ✅ 100%
- Real-time: Yes ✅ 100%
- Setup: 2-5 minutes ✅ 100%
- Custom events: Available ✅ 100%
- Simple funnels: Not available ❌ 0%
- API access: Yes ✅ 100%
- Data retention: Unlimited ✅ 100%
- Script performance: 1.6 KB ✅ 100%
- Reliability: 99.9%+ SLA ✅ 100%
- Export: CSV ✅ 100%
- Team access: Unlimited users ✅ 100%
- Support: Email support included ✅ 100%
- No lock-in: CSV export ✅ 100%
- Professional: Clean dashboard ✅ 100%

**Overall: 14/15 = 93%**

**Strengths:**
- Lowest cost privacy-first paid option
- Unlimited users and retention (best value for teams)
- Uptime monitoring included (bonus feature)
- Very fast script (1.6KB)
- Paid support from day one
- Privacy-first, bootstrapped company (aligned values)

**Gaps:**
- **No funnels** (critical gap for conversion tracking)
- Must manually analyze funnel via custom events + spreadsheets
- Web analytics focus (not product analytics)

**When to Choose:**
Best for teams that prioritize simplicity and privacy over advanced funnel analysis. Can workaround funnel limitation by tracking custom events and building conversion reports manually. The $14/month cost is easily justified with proper attribution data.

### Option 3: Plausible $19/month (93% fit)

**Scoring:**
- Cost: $19/month ✅ 100%
- Privacy: Cookie-less certified, EU hosting (Germany) ✅ 100%
- Real-time: Yes ✅ 100%
- Setup: 2-5 minutes ✅ 100%
- Custom events: Available ✅ 100%
- Simple funnels: Requires Business plan $69/mo ❌ 0%
- API access: Yes ✅ 100%
- Data retention: Unlimited ✅ 100%
- Script performance: <1 KB (best) ✅ 100%
- Reliability: 99.9%+ SLA ✅ 100%
- Export: CSV ✅ 100%
- Team access: Multiple users ✅ 100%
- Support: Email support ✅ 100%
- No lock-in: CSV + open-source self-host ✅ 100%
- Professional: Excellent UI ✅ 100%

**Overall: 14/15 = 93%**

**Strengths:**
- GDPR Article 6(1)(f) certified with legal docs
- <1KB script (fastest in category)
- Most polished UI
- Open-source (can self-host)
- Bootstrapped, privacy-aligned company

**Gaps:**
- **Funnels require $69/mo upgrade** (3.6x cost increase)
- $50/month premium for funnel feature
- Pricing jump is significant for bootstrapped startups

**When to Choose:**
If GDPR certification is critical (EU customers, legal scrutiny) and you can afford $69/month for funnels. The <1KB script is ideal for landing page performance. Otherwise, PostHog free tier offers better value.

### Option 4: Simple Analytics €19/month or €9/month annual (93% fit)

**Scoring:**
- Cost: €19/month = ~$21, or €108/year = $9/mo annual ✅ 100%
- Privacy: Cookie-less, GDPR-first, EU servers (Netherlands) ✅ 100%
- Real-time: Yes ✅ 100%
- Setup: 2-5 minutes ✅ 100%
- Custom events: Available ✅ 100%
- Simple funnels: Not available ❌ 0%
- API access: Yes ✅ 100%
- Data retention: Unlimited ✅ 100%
- Script performance: ~2 KB ✅ 100%
- Reliability: 99%+ ✅ 100%
- Export: CSV + raw data ✅ 100%
- Team access: Multiple users ✅ 100%
- Support: Email support ✅ 100%
- No lock-in: CSV export ✅ 100%
- Professional: Clean dashboard ✅ 100%

**Overall: 14/15 = 93%**

**Strengths:**
- **Best annual pricing** ($9/month = $108/year when paid annually)
- EU-based, GDPR-first design
- Raw data export (more complete than CSV)
- Clean, simple interface

**Gaps:**
- No funnels (same as Fathom)
- Requires annual commitment for best pricing

**When to Choose:**
If you can commit to annual payment and prioritize cost. $108/year ($9/month) is the lowest privacy-focused paid option. Good for budget-conscious startups comfortable with manual funnel analysis.

### Option 5: Umami Self-Hosted (70% fit)

**Scoring:**
- Cost: ~$10-15/month infrastructure ✅ 100%
- Privacy: Full data sovereignty ✅ 100%
- Real-time: Yes (self-managed) ⚠️ 90%
- Setup: 15-30 minutes + maintenance ❌ 30%
- Custom events: Available ✅ 100%
- Simple funnels: Not available ❌ 0%
- API access: Yes ✅ 100%
- Data retention: Unlimited (self-controlled) ✅ 100%
- Script performance: <2 KB ✅ 100%
- Reliability: Self-managed ⚠️ 70%
- Export: CSV ✅ 100%
- Team access: Self-managed users ⚠️ 80%
- Support: Community only ❌ 0%
- No lock-in: Direct database access ✅ 100%
- Professional: Good but self-hosted stigma ⚠️ 80%

**Overall: 10.5/15 = 70%**

**Strengths:**
- Very low cost ($10-15/month)
- Full data ownership
- Open-source
- Customizable

**Gaps:**
- Setup complexity (Docker, database, deployment)
- No funnels (critical for SaaS)
- No support (community only)
- Self-managed reliability
- Maintenance burden for small team

**When to Choose:**
Only if team has DevOps capacity and strong preference for self-hosting. The maintenance burden (updates, monitoring, backups) typically isn't worth the $5-10/month savings for early-stage startups. Focus on product, not infrastructure.

## Implementation Guide

### Recommended: PostHog Free Tier Setup

**Step 1: Create Account (3 minutes)**
1. Go to posthog.com
2. Sign up for free cloud account
3. Create new project
4. Get JavaScript snippet

**Step 2: Add Tracking Code (5 minutes)**

**Basic Pageview Tracking:**
```html
<script>
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
  posthog.init('YOUR_API_KEY',{api_host:'https://app.posthog.com'})
</script>
```

**Step 3: Configure Cookie-less Mode (2 minutes)**
```javascript
posthog.init('YOUR_API_KEY', {
  api_host: 'https://app.posthog.com',
  persistence: 'memory', // Cookie-less mode
  disable_session_recording: false, // Enable 5K free replays
  autocapture: false // Disable to control events
})
```

**Step 4: Track Custom Events (3 minutes)**

**Signup Button Click:**
```javascript
document.getElementById('signup-btn').addEventListener('click', function() {
  posthog.capture('signup_clicked', {
    button_location: 'hero_section',
    plan_type: 'free'
  })
})
```

**Form Submission:**
```javascript
posthog.capture('signup_completed', {
  email_domain: email.split('@')[1],
  referral_source: utmSource
})
```

**Step 5: Create Funnel (5 minutes)**
1. Go to PostHog dashboard → Insights → Funnels
2. Add steps:
   - Step 1: Pageview `/pricing`
   - Step 2: Event `signup_clicked`
   - Step 3: Event `signup_completed`
3. Save funnel
4. Monitor conversion rates

**Total Setup Time: 15-20 minutes**

### Alternative: Fathom Setup (No Funnels)

**Step 1: Create Account (2 minutes)**
1. Go to usefathom.com
2. Start 7-day free trial
3. Add your site

**Step 2: Add Tracking Code (2 minutes)**
```html
<!-- Fathom Analytics -->
<script src="https://cdn.usefathom.com/script.js"
        data-site="YOUR_SITE_ID"
        defer></script>
```

**Step 3: Track Custom Events (3 minutes)**
```javascript
// Signup clicked
fathom.trackGoal('SIGNUP_GOAL_ID', 0);

// Demo requested (with value)
fathom.trackGoal('DEMO_GOAL_ID', 500); // $500 potential value
```

**Step 4: Manual Funnel Analysis (Ongoing)**
- Export custom event data to CSV
- Build conversion funnel in Google Sheets
- Calculate: Visits → Signups → Activations

**Total Setup Time: 10 minutes (+ manual funnel work)**

## Cost Analysis

### 1-Year Total Cost of Ownership

**PostHog Free Tier**
- Subscription: $0
- Infrastructure: $0
- Setup time: 20 min × $100/hr = $33
- Maintenance: 0 hrs/month × $0 = $0
- **Total Year 1: $33 (setup only)**

**Fathom $14/month**
- Subscription: $14/month × 12 = $168
- Infrastructure: $0
- Setup time: 10 min × $100/hr = $17
- Maintenance: 0 hrs/month × $0 = $0
- Manual funnel analysis: 2 hrs/month × 12 × $100 = $2,400
- **Total Year 1: $2,585** (with time cost)
- **Total Year 1: $185** (cash only)

**Plausible $19/month (or $69/month with funnels)**
- Subscription (Growth): $19/month × 12 = $228
- Subscription (Business): $69/month × 12 = $828
- Infrastructure: $0
- Setup time: 10 min × $100/hr = $17
- Maintenance: 0 hrs/month × $0 = $0
- **Total Year 1: $245 (Growth)** or **$845 (Business with funnels)**

**Simple Analytics €108/year annual**
- Subscription: €108/year = $117/year
- Infrastructure: $0
- Setup time: 10 min × $100/hr = $17
- Manual funnel work: 2 hrs/month × 12 × $100 = $2,400
- **Total Year 1: $2,534** (with time cost)
- **Total Year 1: $134** (cash only, best annual pricing)

### 3-Year Total Cost of Ownership

| Provider | Year 1 | Year 2 | Year 3 | 3-Year Total |
|----------|--------|--------|--------|--------------|
| PostHog Free | $0 | $0 | $0 | **$0** |
| Fathom | $168 | $168 | $168 | **$504** |
| Plausible Growth | $228 | $228 | $228 | **$684** |
| Plausible Business | $828 | $828 | $828 | **$2,484** |
| Simple Analytics | $117 | $117 | $117 | **$351** |

### ROI Calculation

**Scenario:** 100K monthly pageviews, 2% signup conversion

Without analytics:
- Blind marketing spend optimization
- No conversion tracking
- Guessing at what works

With analytics ($0-828/year):
- A/B test landing page variations
- Identify best traffic sources
- Optimize conversion funnel
- Track campaign ROI

**Example ROI:**
- Current: 100K visits × 2% = 2,000 signups/month
- Optimize funnel: 2% → 2.5% = +500 signups/month
- Customer LTV: $50/customer
- Value gain: 500 × $50 = $25,000/month

**Conclusion:** Even $828/year (Plausible Business) pays for itself if it improves conversion by 0.01%.

## Decision Framework

### Choose PostHog Free Tier if:
- ✅ Budget is absolutely <$30/month
- ✅ Need funnel analysis (critical)
- ✅ Comfortable with event-based tracking
- ✅ Can configure cookie-less mode
- ✅ Technical team (developers)
- ✅ Don't need paid support yet
- ✅ 1M events covers usage (100K pageviews + moderate events)

**Best for:** Technical founders, developer tools, early-stage SaaS with developer users

### Choose Fathom if:
- ✅ Prioritize simplicity over features
- ✅ Want paid support from day one
- ✅ Privacy is critical (cookie-less default)
- ✅ Can do manual funnel analysis
- ✅ Budget allows $14/month
- ✅ Value unlimited retention + unlimited users
- ✅ Fast script (<2KB) is important

**Best for:** Non-technical founders, privacy-first SaaS, teams wanting simplicity

### Choose Plausible if:
- ✅ Need GDPR legal certification
- ✅ EU customers with legal scrutiny
- ✅ Can afford $19/month (Growth) or $69/month (Business)
- ✅ Want fastest script (<1KB)
- ✅ Value open-source option
- ✅ Appreciate polished UI
- ✅ Support privacy-focused businesses

**Best for:** EU-focused SaaS, privacy-conscious market, investor demo requirements

### Choose Simple Analytics if:
- ✅ Can commit to annual payment
- ✅ Want lowest cost privacy option ($108/year)
- ✅ EU hosting required
- ✅ Manual funnel analysis acceptable
- ✅ Budget is tight but privacy matters

**Best for:** Budget-conscious EU startups, annual planning cycle

## Migration Path

### Month 0-6: Validation Phase
**Use:** PostHog Free Tier
- Zero cost during validation
- Full funnel analysis
- Prove product-market fit
- **Trigger to upgrade:** Hit 1M events/month OR need SLA

### Month 6-12: Growth Phase
**Consider:** PostHog Paid OR Fathom/Plausible
- PostHog Paid: If need advanced features (session replay, experimentation)
- Fathom/Plausible: If want simplicity + privacy certification

**Decision factors:**
- Events >1M/month → PostHog paid (~$450/month for 3M events) OR self-host
- Events <1M/month but need SLA → Fathom $14-54/month
- GDPR certification required → Plausible $19-69/month

### Month 12+: Scale Phase
**Evaluate:**
- Self-hosted PostHog: If events >5M/month (cost efficiency)
- Enterprise analytics: If need SSO, RBAC, compliance docs
- Product analytics upgrade: If need advanced cohorts, retention

**Migration triggers:**
- Revenue >$50K/month → Justify enterprise analytics
- Team >10 people → Need collaboration features
- EU enterprise customers → Need Piwik PRO compliance certification

## Common Pitfalls to Avoid

### Pitfall 1: Choosing GA4 Because It's Free
**Problem:** 45KB script, cookie consent required, GDPR issues
**Impact:** Slower landing page, lower conversion, legal risk
**Solution:** Use PostHog free tier (same cost, better fit)

### Pitfall 2: Paying for Analytics Before Validating Product
**Problem:** $69/month Plausible Business when 0 customers
**Impact:** Wasted money during validation
**Solution:** Start with PostHog/GoatCounter free, upgrade when justified

### Pitfall 3: Skipping Funnel Analysis
**Problem:** Using Fathom/Cloudflare without funnels
**Impact:** Can't optimize conversion, miss revenue opportunities
**Solution:** Either use PostHog (free funnels) or build manual funnel analysis

### Pitfall 4: Ignoring Page Load Impact
**Problem:** Heavy analytics script slows landing page
**Impact:** 1-second delay = 7% conversion drop
**Solution:** Prioritize lightweight scripts (<3KB): Plausible, Fathom, Umami

### Pitfall 5: No Event Tracking from Day 1
**Problem:** Only tracking pageviews, missing conversions
**Impact:** Can't attribute signups to campaigns
**Solution:** Implement custom events for: signup_clicked, demo_requested, trial_started

## Real-World Examples

### Example 1: Developer Tool Startup
- **Product:** API monitoring tool
- **Traffic:** 80K pageviews/month
- **Solution:** PostHog Free Tier
- **Events tracked:**
  - signup_started
  - email_verified
  - api_key_created (activation)
  - first_alert_received
- **Funnel:** Landing → Signup → API Key → First Alert (24% conversion)
- **Cost:** $0/month
- **Result:** Identified 50% drop-off at email verification, implemented social auth, +30% conversion

### Example 2: B2B SaaS Landing Page
- **Product:** Team collaboration tool
- **Traffic:** 120K pageviews/month
- **Solution:** Fathom $14/month
- **Why:** CEO wants privacy-first, doesn't trust free tiers
- **Events tracked:** demo_requested, pricing_viewed, signup_completed
- **Funnel:** Manual (CSV export + Google Sheets)
- **Cost:** $14/month
- **Result:** Clean dashboards for board meetings, privacy story for EU customers

### Example 3: Waitlist Landing Page
- **Product:** AI writing assistant (pre-launch)
- **Traffic:** 50K pageviews/month
- **Solution:** Plausible $9/month (10K tier)
- **Why:** Investor asked for "professional analytics" in deck
- **Events tracked:** waitlist_signup, share_clicked
- **Cost:** $9/month
- **Result:** Beautiful dashboards in investor presentations, validated demand (5K waitlist)

## Next Steps

1. **Assess your situation:**
   - What's your monthly budget? (<$30/month)
   - Need funnels? (Yes for conversion optimization)
   - Technical team? (Can configure PostHog)
   - EU customers? (GDPR compliance matters)

2. **Start with PostHog Free Tier if:**
   - Budget is $0-10/month
   - Need funnel analysis
   - Have developer who can set up

3. **Or start with Fathom $14/month if:**
   - Can afford $14/month
   - Want simplicity + paid support
   - Manual funnel analysis is okay

4. **Implement in this order:**
   - Day 1: Basic pageview tracking (5 min)
   - Day 2: Custom event tracking (30 min)
   - Week 1: Funnel analysis setup (1 hr)
   - Week 2: Optimize based on data

5. **Monitor and iterate:**
   - Track conversion funnel weekly
   - A/B test landing page variations
   - Attribute signups to campaigns
   - Calculate ROI monthly

## Related Use Cases

- **Personal Blog**: If you're pre-revenue or side project
- **E-commerce Site**: If you're selling products (need revenue tracking)
- **Product-Led Growth SaaS**: If you're tracking in-app product usage
- **Enterprise Marketing**: If you need compliance certifications
