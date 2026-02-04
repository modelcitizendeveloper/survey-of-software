# Use Case: E-commerce Site

**Traffic:** 1,000,000 pageviews/month (growth stage)
**Priority:** Funnel analysis, attribution, revenue tracking
**Technical Skill:** E-commerce platform, growth team

## Scenario Description

A growing e-commerce business that needs to optimize conversion funnels, attribute revenue to marketing channels, and understand customer purchase behavior. The business has product-market fit and is scaling marketing spend.

**Typical Examples:**
- Direct-to-consumer (DTC) brand
- Online retail store
- Subscription box service
- Digital product marketplace
- Multi-vendor platform

## Requirements Analysis

### Must-Have Requirements (5 critical)

1. **Advanced funnels: Multi-step conversion analysis**
   - Track: Product page → Add to cart → Checkout → Purchase
   - Identify drop-off points
   - Segment by product category, traffic source
   - Calculate conversion rates at each step

2. **Revenue tracking: Associate analytics with sales**
   - Track purchase value
   - Calculate ROI by channel
   - Measure customer lifetime value (LTV)
   - Monitor average order value (AOV)

3. **Attribution: Understand what drives sales**
   - First-touch attribution (discovery)
   - Last-touch attribution (conversion)
   - Multi-touch attribution (full journey)
   - UTM parameter tracking
   - Campaign performance measurement

4. **Cost efficiency: <$100/month OR self-hosted viable**
   - 1M pageviews = significant cost at tier pricing
   - Need cost-effective solution as traffic grows
   - Consider self-hosted for predictable costs

5. **API access: Integrate with data warehouse, BI tools**
   - Export to BigQuery/Snowflake
   - Connect to Looker/Tableau for reporting
   - Feed data to customer data platform (CDP)

### Nice-to-Have Requirements (10 additional)

6. **Cohort retention** - Track repeat purchase rates by acquisition cohort
7. **Real-time dashboards** - Monitor Black Friday traffic live
8. **Privacy compliance** - GDPR for EU customers, CCPA for California
9. **Custom events** - Track: wishlist_add, coupon_applied, review_submitted
10. **Team collaboration** - 5-10 users (marketing, product, analytics)
11. **Data retention: 24+ months** - Year-over-year holiday comparisons
12. **SLA guarantees: 99.9%+ uptime** - Can't afford downtime during peak sales
13. **Segmentation** - Analyze by: customer type, product category, geographic region
14. **Professional reporting** - Shareable dashboards for executives
15. **No data sampling** - Full accuracy for financial decisions

## Provider Evaluation

### Option 1: PostHog Cloud (95% fit) - RECOMMENDED

**Scoring:**
- Advanced funnels: Best-in-class ✅ 100%
- Revenue tracking: Event properties for purchase value ✅ 100%
- Attribution: Multi-touch attribution capable ✅ 100%
- Cost: ~$450/month for 3M events (1M pageviews) ⚠️ 50% (upper limit)
- API access: Comprehensive, warehouse integrations ✅ 100%
- Cohort retention: Excellent ✅ 100%
- Real-time: Yes ✅ 100%
- Privacy: GDPR-capable, EU hosting option ✅ 100%
- Custom events: Full event tracking ✅ 100%
- Team collaboration: Unlimited users, RBAC ✅ 100%
- Data retention: 7 years ✅ 100%
- SLA: 99.9%+ ✅ 100%
- Segmentation: Advanced segmentation ✅ 100%
- Professional reporting: Excellent dashboards ✅ 100%
- No sampling: Full data ✅ 100%

**Overall: 14.5/15 = 97%**

**Strengths:**
- Purpose-built for product analytics with e-commerce support
- Full funnel analysis from browse to purchase
- Revenue tracking via event properties
- Cohort analysis for repeat purchase tracking
- Session replay (debug checkout friction)
- 7-year data retention (exceptional)
- Warehouse integrations (BigQuery, Snowflake, Redshift)

**Gaps:**
- Cost at upper limit (~$450/month for 3M events)
  - 1M pageviews with e-commerce tracking = ~3M events
  - Add to cart, checkout steps, purchase events add up
- Event-based pricing can escalate quickly

**Implementation:**
```javascript
// Track purchase with revenue
posthog.capture('purchase_completed', {
  revenue: 129.99,
  product_id: 'SKU-12345',
  product_category: 'Electronics',
  coupon_code: 'SAVE20',
  payment_method: 'credit_card'
})

// Build funnel: Product View → Add to Cart → Checkout → Purchase
// Segment by: traffic source, device, customer type
```

**Why Recommended:**
PostHog provides enterprise-grade product analytics at mid-market pricing. For e-commerce, the ability to track revenue, build complex funnels, and analyze cohorts is critical. The $450/month cost is justified if it improves conversion by even 0.5% (1M visits × 2% conversion × 0.5% improvement × $100 AOV = $10,000/month gain).

### Option 2: Matomo Self-Hosted (76% fit)

**Scoring:**
- Advanced funnels: Yes (add-on available) ✅ 100%
- Revenue tracking: E-commerce plugin ✅ 100%
- Attribution: Multi-channel attribution ✅ 100%
- Cost: ~$50-100/month infrastructure ✅ 100%
- API access: Yes ✅ 100%
- Cohort retention: Available but limited ⚠️ 70%
- Real-time: Yes ✅ 100%
- Privacy: Full GDPR compliance (self-hosted) ✅ 100%
- Custom events: Yes ✅ 100%
- Team collaboration: User management ⚠️ 80%
- Data retention: Unlimited (self-controlled) ✅ 100%
- SLA: Self-managed ❌ 0%
- Segmentation: Good ✅ 100%
- Professional reporting: Good ✅ 100%
- No sampling: Full data ✅ 100%

**Overall: 13.5/15 = 90%**

**Strengths:**
- Built-in e-commerce tracking (purpose-built)
- Revenue analytics and goal tracking
- Self-hosted = predictable costs ($50-100/month)
- Full data ownership
- E-commerce plugins available

**Gaps:**
- Self-managed SLA (must maintain yourself)
- Cohort features less advanced than PostHog
- Requires DevOps capacity
- 22.8KB script (slower than competitors)

**Implementation:**
```javascript
// Matomo E-commerce Tracking
_paq.push(['addEcommerceItem',
  'SKU-12345',           // Product SKU
  'Wireless Headphones', // Product name
  'Electronics',         // Category
  129.99,               // Price
  1                     // Quantity
]);

_paq.push(['trackEcommerceOrder',
  'ORDER-7890',  // Order ID
  129.99,        // Grand total
  120.00,        // Subtotal
  5.00,          // Tax
  4.99,          // Shipping
  false          // Discount
]);
```

**When to Choose:**
Best for e-commerce businesses with DevOps capacity that want cost predictability. At 1M pageviews, self-hosting Matomo costs $50-100/month vs $450+ for cloud alternatives. Trade-off is maintenance burden.

### Option 3: Google Analytics 4 (Enhanced E-commerce) (65% fit)

**Scoring:**
- Advanced funnels: Yes (exploration reports) ✅ 100%
- Revenue tracking: Enhanced e-commerce ✅ 100%
- Attribution: Multi-channel funnels ✅ 100%
- Cost: Free ✅ 100%
- API access: BigQuery export (free tier limits) ⚠️ 70%
- Cohort retention: Available ⚠️ 80%
- Real-time: Yes ✅ 100%
- Privacy: GDPR disputed in EU ❌ 0%
- Custom events: Yes ✅ 100%
- Team collaboration: Multiple users ✅ 100%
- Data retention: 14 months default ⚠️ 50%
- SLA: 99.99%+ ✅ 100%
- Segmentation: Advanced ✅ 100%
- Professional reporting: Looker Studio integration ✅ 100%
- No sampling: Sampling on large datasets ❌ 30%

**Overall: 11.3/15 = 75%**

**Strengths:**
- Free (no cost even at high traffic)
- Enhanced e-commerce tracking purpose-built for retail
- BigQuery export for data warehouse
- Google Ads integration
- Familiar to most marketers

**Gaps:**
- **GDPR compliance disputed** (EU court rulings)
- Cookie consent required (conversion friction)
- Data sampling at high traffic volumes
- 45KB script (page load impact)
- Privacy concerns for customers

**When to Avoid:**
E-commerce sites serving EU customers should avoid GA4 due to GDPR legal risk. The Austrian, French, and Italian DPAs have ruled against GA4. Even if "technically compliant," customer trust erosion isn't worth free analytics.

### Option 4: Plausible Business $69/month (85% fit)

**Scoring:**
- Advanced funnels: Yes (Business plan) ✅ 100%
- Revenue tracking: Custom events with properties ⚠️ 80%
- Attribution: UTM tracking, sources ⚠️ 70%
- Cost: $69/month (1M pageviews tier) ✅ 100%
- API access: Yes ✅ 100%
- Cohort retention: Not available ❌ 0%
- Real-time: Yes ✅ 100%
- Privacy: Cookie-less certified, EU hosting ✅ 100%
- Custom events: Yes with properties ✅ 100%
- Team collaboration: Multiple users ✅ 100%
- Data retention: Unlimited ✅ 100%
- SLA: 99.9%+ ✅ 100%
- Segmentation: Limited ⚠️ 60%
- Professional reporting: Excellent UI ✅ 100%
- No sampling: Full data ✅ 100%

**Overall: 12.1/15 = 81%**

**Strengths:**
- Privacy-first (cookie-less, GDPR certified)
- <1KB script (fastest page loads)
- $69/month for 1M pageviews (cost-effective)
- Beautiful dashboards
- Funnels on Business plan

**Gaps:**
- **No cohort retention** (critical for e-commerce)
- Revenue tracking via custom events (not native)
- Attribution less sophisticated than GA4/PostHog
- Web analytics, not purpose-built for e-commerce

**When to Choose:**
Good for privacy-conscious e-commerce brands where GDPR compliance is critical and cohort analysis can be done externally. The <1KB script improves page load (faster checkout = higher conversion).

### Option 5: Mixpanel (Free tier 20M events) (85% fit)

**Scoring:**
- Advanced funnels: Excellent ✅ 100%
- Revenue tracking: Revenue analytics built-in ✅ 100%
- Attribution: Multi-touch attribution ✅ 100%
- Cost: Free for <20M events (1M pageviews ~3-5M events) ✅ 100%
- API access: Comprehensive ✅ 100%
- Cohort retention: Best-in-class ✅ 100%
- Real-time: Yes ✅ 100%
- Privacy: GDPR-capable (requires config) ⚠️ 80%
- Custom events: Full event-based ✅ 100%
- Team collaboration: 5 users on free tier ⚠️ 80%
- Data retention: 90 days on free tier ❌ 30%
- SLA: No SLA on free tier ❌ 40%
- Segmentation: Advanced ✅ 100%
- Professional reporting: Excellent ✅ 100%
- No sampling: Full data ✅ 100%

**Overall: 13.3/15 = 89%**

**Strengths:**
- Purpose-built product analytics with e-commerce focus
- 20M event free tier (generous headroom)
- Best-in-class cohort and retention analysis
- Revenue tracking native

**Gaps:**
- **90-day retention on free tier** (critical gap for YoY comparisons)
- No SLA on free tier
- 5-user limit
- Free tier dependency risk

**When to Choose:**
Good for e-commerce startups that can work within 90-day retention limit. The 20M event tier provides significant buffer. Upgrade to paid when need historical data or SLA.

## Implementation Guide

### Recommended: PostHog Setup for E-commerce

**Step 1: Initialize PostHog (5 minutes)**
```html
<script>
  !function(t,e){/* PostHog snippet */}(document,window.posthog||[]);
  posthog.init('YOUR_API_KEY', {
    api_host: 'https://app.posthog.com',
    persistence: 'cookie', // Need persistence for attribution
    capture_pageview: true,
    autocapture: false // Manual event tracking for accuracy
  })
</script>
```

**Step 2: Track E-commerce Events (15 minutes)**

**Product Viewed:**
```javascript
posthog.capture('product_viewed', {
  product_id: 'SKU-12345',
  product_name: 'Wireless Headphones',
  product_category: 'Electronics',
  price: 129.99,
  currency: 'USD',
  traffic_source: utmSource,
  device_type: isMobile ? 'mobile' : 'desktop'
})
```

**Add to Cart:**
```javascript
posthog.capture('add_to_cart', {
  product_id: 'SKU-12345',
  quantity: 1,
  price: 129.99,
  cart_value: currentCartTotal
})
```

**Checkout Started:**
```javascript
posthog.capture('checkout_started', {
  cart_value: 129.99,
  item_count: 2,
  coupon_applied: 'SAVE20'
})
```

**Purchase Completed:**
```javascript
posthog.capture('purchase_completed', {
  order_id: 'ORDER-7890',
  revenue: 129.99,
  tax: 5.00,
  shipping: 4.99,
  coupon_code: 'SAVE20',
  payment_method: 'credit_card',
  products: [
    {id: 'SKU-12345', name: 'Headphones', price: 129.99, quantity: 1}
  ]
})
```

**Step 3: Create E-commerce Funnel (10 minutes)**
1. Go to PostHog → Insights → Funnels
2. Add funnel steps:
   - Step 1: `product_viewed`
   - Step 2: `add_to_cart`
   - Step 3: `checkout_started`
   - Step 4: `purchase_completed`
3. Add breakdowns: `traffic_source`, `device_type`, `product_category`
4. Set date range: Last 30 days
5. Save funnel

**Step 4: Set Up Retention Cohorts (10 minutes)**
1. Go to PostHog → Insights → Retention
2. Define cohort: Users who triggered `purchase_completed`
3. Return condition: `purchase_completed` again (repeat purchase)
4. Time interval: Weekly
5. Analyze: What % of customers return to purchase?

**Step 5: Revenue Dashboard (15 minutes)**
1. Create dashboard: "E-commerce Metrics"
2. Add insights:
   - Total revenue (sum of `revenue` property)
   - Average order value (AVG `revenue`)
   - Conversion rate (funnel %)
   - Revenue by traffic source
   - Revenue by product category
3. Share with team

**Total Setup Time: 1 hour**

## Cost Analysis

### 1-Year Total Cost of Ownership

**PostHog Cloud (~3M events for 1M pageviews)**
- Subscription: ~$450/month × 12 = $5,400
- Infrastructure: $0
- Setup: 1 hour × $100/hr = $100
- Maintenance: Minimal (cloud) = $0
- **Total Year 1: $5,500**

**Matomo Self-Hosted**
- Subscription: $0
- Infrastructure: $75/month × 12 = $900
- E-commerce plugin: $199/year = $199
- Setup: 4 hours × $100/hr = $400
- Maintenance: 5 hours/month × 12 × $100/hr = $6,000
- **Total Year 1: $7,499** (with time cost)
- **Total Year 1: $1,099** (cash only)

**Google Analytics 4**
- Subscription: $0
- Infrastructure: $0
- Setup: 2 hours × $100/hr = $200
- Maintenance: $0
- Legal risk: Potential fines, customer trust loss (unquantified)
- **Total Year 1: $200** (excluding legal/trust risk)

**Plausible Business**
- Subscription: $69/month × 12 = $828
- Infrastructure: $0
- Setup: 30 min × $100/hr = $50
- External cohort analysis: 3 hours/month × 12 × $100/hr = $3,600
- **Total Year 1: $4,478** (with time cost)
- **Total Year 1: $878** (cash only)

**Mixpanel Free Tier**
- Subscription: $0
- Infrastructure: $0
- Setup: 1 hour × $100/hr = $100
- 90-day limit workaround: Manual historical data export/storage
- **Total Year 1: $100** (assumes staying under 20M events)

### 3-Year Total Cost of Ownership

| Provider | Year 1 | Year 2 | Year 3 | 3-Year Total | Notes |
|----------|--------|--------|--------|--------------|-------|
| PostHog | $5,400 | $5,400 | $5,400 | **$16,200** | Assumes stable 3M events |
| Matomo (cash) | $1,099 | $1,099 | $1,099 | **$3,297** | Infrastructure + plugins |
| Matomo (loaded) | $7,499 | $6,000 | $6,000 | **$19,499** | Including DevOps time |
| GA4 | $0 | $0 | $0 | **$0** | Excluding GDPR risk |
| Plausible | $828 | $828 | $828 | **$2,484** | No cohorts |
| Mixpanel Free | $0 | $0 | $0 | **$0** | If under 20M events |

### ROI Calculation

**Scenario:** 1M monthly pageviews, 2% conversion rate, $100 AOV

**Current state (no analytics):**
- Monthly orders: 1M × 2% = 20,000 orders
- Monthly revenue: 20,000 × $100 = $2,000,000
- Annual revenue: $24,000,000

**With advanced analytics ($828-5,400/year):**

**Optimization 1: Reduce cart abandonment**
- Current cart abandonment: 70%
- Optimized (identify friction points): 65%
- Impact: +5% checkout conversion = +1,000 orders/month
- Value: 1,000 × $100 = $100,000/month = $1,200,000/year

**Optimization 2: Improve product page conversion**
- Current product → cart: 10%
- Optimized (better CTAs, images): 11%
- Impact: +1% conversion = +10,000 add-to-carts/month
- Value: 10,000 × 30% checkout rate × $100 = $300,000/year

**Optimization 3: Better attribution**
- Current: Blind spend across channels
- Optimized: Shift budget to high-ROI channels
- Impact: 10% improvement in marketing efficiency
- Marketing spend: $2M/year × 10% = $200,000/year savings

**Total Annual Value: $1,700,000**

**Conclusion:** Even $5,400/year (PostHog) delivers 315x ROI if it enables just 1% revenue improvement.

## Decision Framework

### Choose PostHog if:
- ✅ Need best-in-class funnels and cohorts
- ✅ Budget allows ~$450/month ($5,400/year)
- ✅ Want session replay to debug checkout UX
- ✅ Technical team comfortable with event tracking
- ✅ Need warehouse integrations (BigQuery, Snowflake)
- ✅ Value open-source + cloud hybrid option

**Best for:** Growth-stage DTC brands, technical teams, data-driven optimization

### Choose Matomo Self-Hosted if:
- ✅ Have DevOps capacity (or budget for it)
- ✅ Want cost predictability ($50-100/month)
- ✅ Need full data ownership
- ✅ E-commerce plugins meet your needs
- ✅ Can manage maintenance burden
- ✅ EU data residency required

**Best for:** Larger e-commerce (5M+ pageviews), teams with infrastructure expertise

### Choose Plausible if:
- ✅ Privacy is top priority (GDPR certified)
- ✅ <1KB script essential (conversion optimization)
- ✅ Can do cohort analysis externally
- ✅ EU customers, privacy-conscious market
- ✅ Budget is $69/month
- ✅ Value simplicity + privacy

**Best for:** Privacy-conscious DTC brands, EU markets, smaller catalogs

### Choose Mixpanel Free Tier if:
- ✅ Under 20M events/month
- ✅ Can work within 90-day retention
- ✅ Need excellent cohort analysis now
- ✅ Budget is tight ($0)
- ✅ Plan to upgrade when revenue grows

**Best for:** E-commerce startups, pre-revenue, validating business model

### Avoid Google Analytics 4 if:
- ❌ Serving EU customers (GDPR risk)
- ❌ Privacy-conscious customer base
- ❌ Brand reputation matters
- ❌ Want lightweight script

## Migration Path

### Month 0-6: Launch Phase
**Use:** PostHog Free Tier or Mixpanel Free Tier
- Validate product-market fit
- Track basic e-commerce funnel
- Zero cost during validation
- **Trigger:** Hit event limits or need historical data

### Month 6-12: Growth Phase (1M pageviews)
**Upgrade to:** PostHog Paid (~$450/month) OR Matomo Self-Hosted (~$100/month)
- **PostHog**: If budget allows, want session replay, advanced features
- **Matomo**: If cost-sensitive, have DevOps capacity
- **Trigger:** Revenue >$50K/month justifies analytics investment

### Month 12-24: Scale Phase (5M pageviews)
**Evaluate:** Self-hosted PostHog OR Matomo Enterprise
- PostHog Cloud at 5M pageviews × 3 events = 15M events = ~$2,250/month
- PostHog Self-Hosted: ~$200-300/month infrastructure
- Matomo Self-Hosted: ~$200-300/month infrastructure
- **Trigger:** Cloud costs >$1,000/month → self-host saves 60-80%

### Month 24+: Enterprise Phase (10M+ pageviews)
**Consider:** Enterprise analytics, advanced attribution
- PostHog Enterprise: SSO, RBAC, SLA
- Piwik PRO: Compliance certifications
- Custom data warehouse + BI tooling
- **Trigger:** Need compliance docs, multi-team collaboration, advanced features

## Common Pitfalls

### Pitfall 1: Not Tracking Revenue from Day 1
**Problem:** Only tracking pageviews, not purchase events
**Impact:** Can't calculate ROI, attribute revenue to channels
**Solution:** Implement `purchase_completed` event with `revenue` property immediately

### Pitfall 2: Overlooking Page Load Impact
**Problem:** Heavy analytics script slows checkout page
**Impact:** 1-second delay = 7% conversion drop = $140K/year loss (at $2M/year revenue)
**Solution:** Use lightweight script (<3KB): Plausible, Fathom, or async loading

### Pitfall 3: Ignoring GDPR Compliance
**Problem:** Using GA4 for EU customers without proper consent
**Impact:** Legal fines, DPA rulings, customer trust erosion
**Solution:** Use privacy-first analytics (Plausible, PostHog cookie-less, Matomo self-hosted)

### Pitfall 4: No Cohort Analysis
**Problem:** Don't track repeat purchase rates
**Impact:** Miss LTV optimization, retention issues
**Solution:** Use PostHog or Mixpanel for cohort retention analysis

### Pitfall 5: Relying Only on Last-Click Attribution
**Problem:** Only crediting the last touchpoint before purchase
**Impact:** Under-value awareness channels (social, content)
**Solution:** Implement multi-touch attribution (PostHog, GA4, or external tool)

## Real-World Example

### Case Study: DTC Electronics Brand

**Situation:**
- Product: Premium wireless headphones
- Traffic: 800K pageviews/month
- Revenue: $1.5M/month
- Team: 3 marketers, 2 developers
- Markets: US (70%), EU (30%)

**Solution:** PostHog Cloud + Plausible

**Why dual analytics?**
- PostHog: Product analytics, funnels, session replay (US traffic)
- Plausible: Privacy-certified for EU compliance (EU traffic)
- Cost: PostHog $350/month + Plausible $49/month = $399/month

**Implementation:**
```javascript
// Route by geography
if (userInEU) {
  // Plausible for EU (GDPR certified)
  plausible('pageview')
} else {
  // PostHog for US (full features)
  posthog.capture('$pageview')
}

// Critical purchases tracked in both
posthog.capture('purchase', {revenue: 199.99})
plausible('purchase', {props: {revenue: 199.99}})
```

**Results:**
- Identified 65% mobile cart abandonment (session replay showed checkout UX issue)
- Fixed mobile checkout flow → +8% mobile conversion
- Impact: 400K mobile visits/month × 8% lift × 2% base conversion × $150 AOV = $96,000/month
- ROI: $96K monthly gain / $399 monthly cost = 240x ROI

**Key Learning:** Don't be dogmatic about "one analytics tool." Use the right tool for each use case (privacy for EU, advanced for US).

## Next Steps

1. **Assess current situation:**
   - Monthly pageviews: ___
   - Current conversion rate: ___%
   - Monthly revenue: $___
   - EU customer %: ___%
   - DevOps capacity: Yes/No

2. **Calculate analytics budget:**
   - 1% of revenue is reasonable
   - Example: $100K/month revenue → $1,000/month analytics budget

3. **Choose provider:**
   - <$100/month budget + need funnels → PostHog
   - <$100/month budget + have DevOps → Matomo self-hosted
   - Privacy priority → Plausible
   - Maximum features at $0 → Mixpanel free tier (with limitations)

4. **Implement tracking:**
   - Week 1: Basic pageview tracking
   - Week 2: E-commerce events (view, cart, checkout, purchase)
   - Week 3: Funnels and dashboards
   - Week 4: Attribution and cohort analysis

5. **Optimize and iterate:**
   - Monitor funnel drop-offs weekly
   - A/B test checkout improvements
   - Shift budget to high-ROI channels
   - Track repeat purchase cohorts monthly

## Related Use Cases

- **SaaS Landing Page**: If you're tracking SaaS conversions instead of purchases
- **Enterprise Marketing**: If you need compliance certifications
- **Product-Led Growth**: If your product has in-app analytics needs
