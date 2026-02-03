# Product Analytics Explainer

**Purpose:** Explain technical concepts and terminology for business audiences evaluating product analytics platforms.

**Not Covered Here:** Provider comparisons (see S1-S4 discovery files), specific recommendations (see DISCOVERY_TOC).

---

## What Is Product Analytics?

**Product analytics** tracks **how users interact with your product** to understand behavior patterns, feature adoption, and user journeys.

### Product Analytics vs Web Analytics (Key Difference)

| Dimension | Web Analytics | Product Analytics |
|-----------|---------------|-------------------|
| **Primary Question** | "How many visitors?" | "What do users do?" |
| **Tracking Unit** | Pageviews, sessions | Events, user actions |
| **Key Metrics** | Traffic, bounce rate, referrers | Feature adoption, retention, funnels |
| **Typical Use Case** | Marketing attribution, SEO | Product-led growth, feature prioritization |
| **Example Tools** | Google Analytics, Plausible | Mixpanel, Amplitude |

**Why This Matters:**
- **Web analytics** answers: "Did our blog post drive traffic?" (marketing question)
- **Product analytics** answers: "Do users who enable feature X have higher retention?" (product question)

**Most companies need both** - they serve different purposes.

---

## When You Need Product Analytics

### Clear Signals You Need It:

1. **Product-Led Growth (PLG) Model**
   - Users can sign up and start using product without talking to sales
   - Need to understand self-serve onboarding funnel
   - **Example:** Notion, Slack, Figma

2. **Feature Prioritization Questions**
   - "Which features drive retention?"
   - "What do power users do differently than churned users?"
   - "Should we build feature X or Y next?"

3. **User Cohort Analysis**
   - Comparing behavior of users who signed up in January vs February
   - Tracking retention over weeks/months
   - Understanding impact of product changes

4. **Funnel Optimization**
   - Multi-step processes: signup → activation → first value → paid conversion
   - Need to identify drop-off points
   - **Example:** SaaS onboarding flows, e-commerce checkout

5. **Retroactive Analysis Needs**
   - "We just launched feature X - can we see how users interacted with it last week?"
   - Requires tracking events you didn't anticipate needing

### Business Model Indicators:

**You NEED product analytics if:**
- Freemium SaaS with self-serve signup
- Mobile app with in-app purchases
- E-commerce optimizing checkout flow
- B2B product with trial-to-paid conversion funnel
- Multi-sided marketplace tracking supply AND demand behavior

**You MIGHT need it if:**
- Enterprise sales with free trial period (lighter usage)
- Content platform tracking engagement metrics
- Internal tools tracking employee adoption

---

## When You DON'T Need Product Analytics

### You Probably Don't Need It If:

1. **Pure Marketing Website**
   - Static content, no user accounts
   - Goal is traffic and lead generation
   - **Use instead:** Web analytics (Plausible, Fathom, Google Analytics)
   - **Cost savings:** $0-$20/month vs $200-$2,000/month for product analytics

2. **Enterprise Sales-Led (No Self-Serve)**
   - All customers go through sales process
   - Low user count (<100 total users)
   - Usage patterns tracked via CRM (Salesforce, HubSpot)
   - **Use instead:** CRM analytics + customer success metrics

3. **Very Early Stage (Pre-Product-Market Fit)**
   - <50 active users
   - Talking to every user directly
   - Qualitative feedback more valuable than quantitative data
   - **Use instead:** User interviews, surveys, basic web analytics
   - **Defer:** Product analytics until 200-500+ users (signals drown out noise)

4. **Internal-Only Tools (Small Team)**
   - <20 internal users
   - Can just ask users directly
   - **Use instead:** User interviews, feedback forms
   - **Exception:** If building platform/API for internal teams (100+ users)

5. **Regulated Industries Where Event Tracking is Prohibited**
   - HIPAA-covered healthcare data (without BAA)
   - Financial data under specific regulations
   - **Use instead:** Aggregated, anonymized metrics + compliance-focused analytics

### The "Excel Spreadsheet Test"

**Question:** Can you track what you need in a simple spreadsheet by asking users or reviewing logs once a week?

- **Yes?** → You don't need product analytics yet (save $2,000-$20,000/year)
- **No?** → You probably need automated product analytics

---

## Core Technical Concepts

### 1. Event-Based Tracking

**What It Is:**
Instead of tracking "pageviews," you track **specific user actions** as discrete events.

**Examples:**
- `Button Clicked` (event) with properties: `{button_id: "upgrade_plan", page: "/pricing"}`
- `File Uploaded` with properties: `{file_type: "pdf", file_size_mb: 2.3}`
- `Search Performed` with properties: `{query: "analytics tools", results_count: 47}`

**Why Business People Care:**
- Pageview: "User visited /pricing" (vague)
- Event: "User clicked 'Upgrade to Pro' button on /pricing at 2:47 PM" (actionable)

**Technical Challenge:**
- Must instrument your code: `analytics.track('Button Clicked', {button_id: 'upgrade_plan'})`
- Requires developer time: 2-8 hours for basic setup, 20-40 hours for comprehensive tracking

### 2. User Identity and Session Tracking

**The Problem:**
How do you know that the user who signed up on Monday is the same user who purchased on Friday?

**Solution: User Identification**
```javascript
// Anonymous user (before signup)
analytics.identify('anonymous_id_12345')

// After signup - link anonymous activity to known user
analytics.identify('user_id_67890', {
  email: 'user@example.com',
  signup_date: '2025-10-08'
})
```

**Why This Matters:**
- Without identity tracking: "100 signups and 20 purchases" (can't connect them)
- With identity tracking: "20% of signups purchased within 7 days" (actionable insight)

**Business Implication:**
- Requires handling personally identifiable information (PII)
- Must comply with GDPR, CCPA (see Compliance section below)

### 3. Funnels (Multi-Step Conversion Analysis)

**What It Is:**
Track users through a sequence of steps to identify drop-off points.

**Example: SaaS Signup Funnel**
```
Step 1: Visit landing page (1,000 users)
  ↓ 60% conversion
Step 2: Click "Sign Up" (600 users)
  ↓ 80% conversion
Step 3: Enter email (480 users)
  ↓ 50% conversion (!!! Drop-off here)
Step 4: Verify email (240 users)
  ↓ 90% conversion
Step 5: Complete onboarding (216 users)

Overall conversion: 21.6%
```

**Insight:** Email verification is the problem (50% drop-off). Fix: Switch to passwordless login or defer verification.

**Why Manual Tracking Fails:**
- 5-step funnel × 1,000 users = 5,000 data points to track manually
- Hourly/daily granularity = 120-720 calculations per month
- **DIY spreadsheet:** 20-40 hours/month of manual work
- **Product analytics:** Automated, real-time

### 4. Cohort Analysis

**What It Is:**
Group users by shared characteristic (signup date, acquisition channel, feature usage) and compare behavior.

**Example:**
| Cohort | Week 1 Retention | Week 4 Retention | Week 12 Retention |
|--------|------------------|------------------|-------------------|
| January 2025 signups | 65% | 32% | 18% |
| February 2025 signups | 72% | 41% | 28% |

**Insight:** February cohort has 55% better Week 12 retention. What changed? (New onboarding flow launched Feb 1)

**Technical Challenge:**
- Requires date-based user segmentation
- Needs to recalculate as cohorts age
- Manual spreadsheet: 5-10 hours/month
- Product analytics: Automated

### 5. Retroactive Analysis (Auto-Capture)

**The Problem:**
Traditional analytics: You must decide what to track BEFORE collecting data.

**Example:**
- Developer: "Track button clicks on homepage" ✅
- Two weeks later...
- Product Manager: "Can we see clicks on the sidebar too?"
- Developer: "No, we didn't track that. I can add it now, but we won't have historical data."

**Solution: Auto-Capture (Heap's Innovation)**
- Track **everything** automatically (all clicks, form fills, page views)
- Define events retroactively ("Show me all users who clicked any button with text 'Upgrade'")
- No developer changes required for new queries

**Tradeoff:**
- **Benefit:** Unlimited retroactive analysis
- **Cost:** Higher data volume (2-10x more events tracked)
- **Cost Impact:** Heap is often 3-5x more expensive than Mixpanel/Amplitude for same user base

**When You Need It:**
- Exploratory product with high uncertainty
- Non-technical product managers need self-serve analytics
- Frequent "I wish we had tracked X" conversations

**When You Don't:**
- Mature product with well-defined KPIs
- Technical team can add tracking quickly
- Cost-sensitive (auto-capture costs 3-5x more)

### 6. User Segmentation

**What It Is:**
Filter analytics by user attributes to understand different user groups.

**Examples:**
- "Show me retention for users on Free plan vs Pro plan"
- "Show me feature adoption for users from Google Ads vs organic search"
- "Show me funnel conversion for mobile vs desktop users"

**Technical Requirements:**
- Must send user properties: `{plan: 'pro', acquisition_channel: 'google_ads', device: 'mobile'}`
- Properties can be updated over time (user upgrades from Free to Pro)

**Business Value:**
- Identify high-value user segments
- Target feature development to power users
- Optimize marketing spend by channel

---

## Build vs Buy: Why DIY Product Analytics is Expensive

### Common Misconception:
"Product analytics is just storing events in a database and querying them. We can build this in a weekend."

### Reality: Hidden Complexity

**Core Features (seem simple):**
- Event ingestion API ✅ (weekend project)
- Data storage ✅ (use PostgreSQL/ClickHouse)
- Basic querying ✅ (SQL)

**Actually Complex Features (months of work):**

1. **High-Volume Event Ingestion (Scalability)**
   - 10M events/month = 3,850 events/minute average, 20K+ events/minute peak
   - Must handle spikes (product launch, email blast)
   - Requires: Message queue (Kafka, RabbitMQ), load balancing, auto-scaling
   - **Dev time:** 40-80 hours

2. **Fast Querying on Billions of Events (Performance)**
   - User expects funnel results in <2 seconds
   - Standard PostgreSQL: 30-120 seconds for complex queries on 100M+ events
   - Requires: Columnar database (ClickHouse, BigQuery), pre-aggregation, indexing strategy
   - **Dev time:** 80-160 hours

3. **User Identity Stitching (Accuracy)**
   - Anonymous user → signed up user → same user on mobile app
   - Must deduplicate across devices, merge histories, handle identity conflicts
   - **Dev time:** 60-100 hours

4. **Retroactive Event Definition (Flexibility)**
   - User defines new event from existing data
   - Must re-process historical events (expensive)
   - **Dev time:** 100-200 hours (complex)

5. **Real-Time Dashboard Updates (UX)**
   - Events appear in dashboard within 1-5 minutes
   - Requires: Stream processing (Kafka Streams, Flink), WebSocket updates
   - **Dev time:** 40-60 hours

6. **Data Export and Compliance (Regulatory)**
   - GDPR right to deletion: Remove all events for specific user
   - CCPA data export: Export all user data in portable format
   - Requires: User data deletion pipeline, export API, audit logging
   - **Dev time:** 60-100 hours

**Total DIY Development Time:**
- **Minimum viable product:** 380-700 hours (2-4 months for 1 senior engineer)
- **Production-ready with all features:** 800-1,200 hours (5-7 months)

**Total DIY Cost (Year 1):**
- Development: 400-800 hours × $100-150/hour = $40,000-$120,000
- Infrastructure: ClickHouse/BigQuery, Kafka, monitoring = $6,000-$24,000/year
- Maintenance: 5-10 hours/month × 12 months × $100-150/hour = $6,000-$18,000
- **Total Year 1:** $52,000-$162,000

**Managed Service Cost (Year 1):**
- PostHog: $0-$20,000 (free tier or 10M events/month)
- Mixpanel: $0-$27,000 (free tier or 10M events/month)
- Amplitude: $0-$24,000 (free tier or growth plan)

**Break-Even Analysis:**
- **DIY cheaper:** Only at massive scale (100M+ events/month AND >5 years) OR when you have existing data infrastructure team
- **Managed service cheaper:** 95% of use cases (especially <10M events/month)

**When to Build:**
1. **Extreme scale:** >500M events/month ($180K+/year managed service cost)
2. **Data sovereignty:** Regulated industry requiring on-premise hosting
3. **Existing infrastructure:** Already have data engineering team + ClickHouse/Kafka
4. **Unique requirements:** Need custom features not offered by any vendor

**When to Buy:**
1. **Startup/SMB:** <10M events/month (use free tiers or $0-$20K/year plans)
2. **Time-to-value:** Need analytics today, not in 6 months
3. **No data team:** Engineers focused on core product, not infrastructure
4. **Compliance:** Vendor has certifications (SOC2, GDPR) you'd spend $50K+ achieving

---

## Privacy and Compliance

### Why This Is Complex for Product Analytics:

**Product analytics tracks individual user behavior** → inherently involves PII → must comply with privacy regulations.

### GDPR (EU General Data Protection Regulation)

**Key Requirements:**
1. **Consent:** Must get explicit user consent before tracking (not required for web analytics in many cases)
2. **Right to Access:** Users can request all data you've collected
3. **Right to Deletion:** Users can request full deletion (hard to implement in analytics systems)
4. **Data Minimization:** Only collect data necessary for stated purpose

**Technical Implementation:**
- Cookie consent banner (GDPR-compliant)
- User data export API
- User data deletion pipeline (remove from analytics warehouse)
- **Vendor support:** Most product analytics platforms have GDPR compliance features (PostHog, Mixpanel, Amplitude)

### CCPA (California Consumer Privacy Act)

**Key Requirements:**
1. **Right to Know:** Users can request what data is collected and how it's used
2. **Right to Delete:** Users can request deletion
3. **Do Not Sell:** Users can opt out of data selling (not usually relevant for product analytics)

**Business Implication:**
- Must implement data export and deletion pipelines
- Most vendors offer CCPA compliance features

### Cookie-Less Tracking (Privacy-First Alternative)

**Problem:** GDPR/CCPA make cookie-based tracking complex (consent banners, opt-outs)

**Solution:** Cookie-less tracking using server-side events
- No cookies stored in user browser
- No PII sent to analytics platform (send hashed user IDs)
- **Tradeoff:** Less cross-device tracking, harder to track anonymous users

**Providers Supporting Cookie-Less:**
- PostHog (server-side SDKs)
- Mixpanel (proxy mode)

**When You Need It:**
- European market (GDPR compliance easier)
- Privacy-conscious users
- Want to avoid consent banner friction

---

## Common Misconceptions

### Misconception 1: "We can use Google Analytics for product analytics"

**Why This Fails:**
- Google Analytics 4 (GA4) **can** track custom events
- But: Designed for marketing attribution, not product analytics
- Missing: Funnel analysis, cohort retention, user segmentation with properties
- **Result:** Need to export to BigQuery and write custom SQL (now you're building DIY product analytics)

**When GA4 Is Enough:**
- Content website tracking engagement
- Simple funnel (landing page → signup)
- Marketing-focused questions

### Misconception 2: "Product analytics shows me what to build next"

**Reality:**
- Product analytics shows **what users do**, not **why they do it** or **what they want**
- Example: "50% of users abandon onboarding at step 3" (data)
- Missing: "Why do they abandon?" (requires user interviews, session replays, feedback)

**Best Practice:**
- **Quantitative (product analytics):** What is happening? How many users?
- **Qualitative (user research):** Why is it happening? What do users need?
- **Use both** for product decisions

### Misconception 3: "More events = better insights"

**Reality:**
- Tracking 1,000 event types creates noise
- Hard to find signal in overwhelming data
- Increases cost (usage-based pricing)

**Best Practice:**
- Start with 10-20 core events (signup, key actions, conversion)
- Add events as specific questions arise
- **Quality > Quantity**

### Misconception 4: "Product analytics replaces A/B testing"

**Reality:**
- Product analytics: Observational (track what users naturally do)
- A/B testing: Experimental (test variants, measure causal impact)
- **Complementary, not substitutes**

**Example:**
- Product analytics: "Users who enable dark mode have 2x retention"
- Question: Is dark mode **causing** higher retention, or do power users (who have higher retention) prefer dark mode?
- A/B test: Randomly assign dark mode to 50% of users, measure retention difference
- **Answer:** A/B test proves causality, analytics generates hypothesis

### Misconception 5: "We need real-time analytics"

**Reality:**
- Most product decisions operate on weekly/monthly timelines
- Real-time dashboards are impressive but rarely actionable
- **Exception:** Monitoring for critical issues (payment processing failure)

**Cost Implication:**
- Real-time analytics: 2-5x infrastructure cost (stream processing)
- Batch analytics (1-hour delay): Cheaper, sufficient for 90% of use cases

**When You Need Real-Time:**
- Detecting outages/errors (use APM instead: Sentry, Datadog)
- Live dashboards for exec presentations
- Real-time personalization (recommendation engines)

**When Batch Is Fine:**
- Weekly product reviews
- Monthly cohort analysis
- Feature prioritization decisions

---

## Technical Architecture Patterns

### Pattern 1: Client-Side Tracking (Most Common)

**How It Works:**
```javascript
// JavaScript in user's browser
analytics.track('Button Clicked', {button_id: 'signup'})
// Sends HTTP request to analytics platform
```

**Pros:**
- Easy to implement (drop in SDK)
- Automatic pageview tracking
- Tracks client-side interactions (clicks, scrolls, hovers)

**Cons:**
- Blocked by ad blockers (10-30% of users)
- Can't track server-side events (API calls, background jobs)
- Increases page load time (small impact)

**When to Use:** Standard for web apps, mobile apps

### Pattern 2: Server-Side Tracking (Privacy-First)

**How It Works:**
```python
# Python on your server
analytics.track(user_id='123', event='Purchase Completed', properties={'amount': 49.99})
# Server sends to analytics platform
```

**Pros:**
- Not blocked by ad blockers
- Can track server-side events
- More control over data (filter PII before sending)
- Cookie-less (GDPR-friendly)

**Cons:**
- More complex to implement
- Can't track client-side interactions (clicks, scrolls) unless you send those to your server first

**When to Use:** Privacy-focused, B2B SaaS with backend-heavy workflows

### Pattern 3: Hybrid (Client + Server)

**How It Works:**
- Client-side SDK tracks UI interactions
- Server-side SDK tracks backend events (purchases, API calls)
- Analytics platform merges by user ID

**Pros:**
- Most complete data
- Best of both worlds

**Cons:**
- More complex setup
- Must ensure user IDs match across client/server

**When to Use:** Mature products with dedicated data/analytics team

### Pattern 4: Reverse Proxy (Ad-Blocker Bypass)

**How It Works:**
```javascript
// Instead of sending to mixpanel.com (blocked by ad blockers)
analytics.track('Event') // Sends to yoursite.com/analytics-proxy
// Your server forwards to mixpanel.com
```

**Pros:**
- Bypasses ad blockers (events sent to your domain)
- More complete data (capture all users)

**Cons:**
- Requires server-side proxy setup
- Adds latency (extra hop)
- Ethical concerns (bypassing user's ad blocker choice)

**When to Use:** When ad-blocker impact is >20% and distorts data significantly

---

## Pricing Models Explained

### Model 1: Event-Based Pricing (Most Common)

**How It Works:** Pay per event tracked (e.g., $0.00025 per event)

**Example:**
- 10M events/month × $0.00025 = $2,500/month
- Free tier: 1M events/month (Mixpanel, Amplitude, PostHog)

**Pros:**
- Scales with usage
- Predictable (multiply events × price)

**Cons:**
- Encourages under-tracking (avoid sending events to save money)
- Can explode with auto-capture (10x more events)

**When This Bites You:**
- Mobile app: User opens app 50 times/day = 1,500 events/month/user
- 10,000 active users × 1,500 = 15M events/month = $3,750/month

**Mitigation:** Sample events (track 10% of users), track only critical events

### Model 2: MTU Pricing (Monthly Tracked Users)

**How It Works:** Pay per unique user tracked per month (Amplitude's model)

**Example:**
- 100K MTU × $0.15 = $15,000/month
- Free tier: 10M events OR 10K MTU (whichever comes first)

**Pros:**
- Encourages comprehensive tracking (no penalty for more events per user)
- Better for mobile apps (many events per user)

**Cons:**
- Less predictable (user count fluctuates)
- Can be expensive if many low-engagement users (each counts as 1 MTU even if only 1 event)

**When This Is Better:**
- Mobile app with power users (1,000 events/user/month)
- B2B SaaS with deep usage tracking

### Model 3: Flat-Rate Pricing (Rare)

**How It Works:** Pay fixed price regardless of usage (Heap enterprise plans)

**Example:** $50,000/year for unlimited events

**Pros:**
- Totally predictable
- No optimization needed (track everything)

**Cons:**
- Expensive for startups
- Usually only available at enterprise tier

**When This Makes Sense:**
- Mature product with stable usage
- Enterprise budget ($50K+/year)

### Model 4: Data Storage Pricing (Warehouse-Native)

**How It Works:** Store events in your data warehouse (BigQuery, Snowflake), pay warehouse costs (Kubit's model)

**Example:**
- 10M events/month stored in BigQuery
- Storage: 1GB compressed = $0.02/month
- Queries: $5/TB scanned, ~$50-200/month for typical usage
- **Total:** $50-200/month vs $2,500/month event-based

**Pros:**
- Cheapest at scale (10-50x less than event-based)
- Full control of data (it's in your warehouse)
- No vendor lock-in (data is portable)

**Cons:**
- Requires existing data warehouse
- More technical setup (ETL pipelines)
- Slower query performance (warehouse not optimized for analytics)

**When to Use:**
- Already using data warehouse for other purposes
- >50M events/month (cost savings significant)
- Data engineering team available

---

## Integration Ecosystem

### Why Integrations Matter:

Product analytics is **not used in isolation** - it must integrate with:
1. **Data Sources:** Where events come from (web, mobile, server)
2. **Data Destinations:** Where insights are used (CRM, marketing, BI tools)

### Common Integration Patterns:

**1. Data Sources (Event Collection):**
- **Web SDK:** JavaScript snippet on website
- **Mobile SDK:** iOS (Swift), Android (Kotlin) libraries
- **Server SDK:** Python, Node.js, Ruby, Go libraries
- **Reverse ETL:** Import events from data warehouse (Census, Hightouch)

**2. Data Destinations (Export):**
- **Data Warehouse:** Export to BigQuery, Snowflake, Redshift for custom analysis
- **CRM:** Send high-intent user signals to Salesforce, HubSpot (e.g., "User completed onboarding" → notify sales)
- **Marketing Automation:** Trigger emails in Customer.io, Braze based on product behavior
- **BI Tools:** Connect Looker, Tableau, Metabase for custom dashboards

**3. Identity Resolution:**
- **CDP (Customer Data Platform):** Segment, RudderStack, mParticle
- Collect events once, send to multiple destinations
- Tradeoff: Extra $1K-10K/month for CDP, but simplifies multi-tool setup

**Business Scenario:**
- Without CDP: Instrument events 5 times (product analytics, marketing, support, data warehouse, A/B testing)
- With CDP: Instrument events once, CDP sends to 5 destinations
- **Complexity reduction:** 80% less engineering time

**Cost Implication:**
- CDP: $1,000-$10,000/month
- Break-even: If you use 3+ analytics tools, CDP saves engineering time

---

## Summary: Decision Framework

### Start Here:

**Question 1:** Do you have a product with user accounts and self-serve signup?
- **No** → You probably don't need product analytics (use web analytics)
- **Yes** → Continue

**Question 2:** Do you have >200 active users?
- **No** → Defer product analytics (talk to users directly)
- **Yes** → Continue

**Question 3:** Do you need to answer questions like "Which features drive retention?" or "Where do users drop off in funnels?"
- **No** → You might not need product analytics yet
- **Yes** → You need product analytics

**Question 4:** What's your budget?
- **$0** → PostHog free tier (1M events/month) or Mixpanel/Amplitude free tiers
- **$1K-10K/year** → PostHog Cloud, Mixpanel Growth, Amplitude Plus
- **$20K-50K/year** → Mixpanel Enterprise, Amplitude Scale, Pendo
- **$100K+/year** → Any vendor OR consider PostHog self-hosted / warehouse-native (Kubit)

**Question 5:** Do you have a data engineering team?
- **No** → Use managed SaaS (PostHog, Mixpanel, Amplitude)
- **Yes** → Consider warehouse-native (Kubit) or PostHog self-hosted

---

## Glossary

- **Event:** A discrete user action (e.g., "Button Clicked", "File Uploaded")
- **Property:** Metadata attached to an event (e.g., `{button_id: "signup", page: "/pricing"}`)
- **MTU (Monthly Tracked Users):** Number of unique users who triggered at least one event in a month
- **Funnel:** Multi-step sequence tracking user progression (e.g., signup → activation → conversion)
- **Cohort:** Group of users sharing a characteristic (e.g., "January 2025 signups")
- **Retention:** Percentage of users who return after initial use (e.g., "Day 7 retention: 45%")
- **Auto-Capture:** Automatically track all user interactions without manual instrumentation
- **Retroactive Analysis:** Define events from historical data after it's been collected
- **User Segmentation:** Filter analytics by user attributes (e.g., plan type, acquisition channel)
- **CDP (Customer Data Platform):** Central hub collecting events and routing to multiple tools (Segment, RudderStack)

---

**Last Updated:** 2025-10-08
**Version:** 1.0
**Related Experiments:** 3.062 (Web Analytics), 2.082 (Feature Flags), 2.083 (A/B Testing)
