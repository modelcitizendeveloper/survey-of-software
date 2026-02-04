# Use Case: E-commerce Analytics
## Pattern Analysis for Online Retail & Marketplace Products

**Use Case ID**: UC-2.041-05
**Category**: Product Analytics
**Pattern**: E-commerce / Online Retail
**Last Updated**: 2025-10-08

---

## 1. USE CASE PROFILE

### Business Context
- **Industry**: E-commerce, marketplace, direct-to-consumer (DTC) brands
- **Business Model**: Online retail, subscription commerce, marketplace
- **Customer Segment**: B2C shoppers
- **Team Size**: 5-50 employees (product, marketing, merchandising teams)
- **Stage**: Seed to Series B (established product, scaling revenue)
- **Revenue**: $500K-$50M+ annual GMV/revenue
- **Platform**: Web + mobile apps (omnichannel)

### Example Businesses
- Shopify/WooCommerce stores (DTC brands)
- Marketplaces (Etsy-style platforms)
- Subscription boxes
- Fashion/apparel e-commerce
- Digital product stores

---

## 2. ANALYTICS REQUIREMENTS

### Key Questions to Answer
1. **Conversion Optimization**: Where do users drop in purchase funnel?
2. **Product Discovery**: How do users find products? (search, browse, recommendations)
3. **Cart Abandonment**: Why do users abandon carts? Can we recover them?
4. **Customer Journey**: What's the path from landing → purchase?
5. **Merchandising**: Which products/categories drive revenue?
6. **Personalization**: How to recommend products based on behavior?
7. **Customer Lifetime Value**: What behaviors predict repeat purchases?
8. **Mobile vs Web**: Performance differences across platforms?

### Technical Specifications
- **Event Volume**: 5M-200M+ events/month (high traffic volume)
- **User Base**: 50K-2M monthly visitors (high anonymous traffic)
- **Data Retention**: 12-24 months (seasonal trends, repeat purchase cycles)
- **Segmentation Needs**: User-level + session-level (lots of anonymous traffic)
- **Funnel Complexity**: 5-15 funnels (product view → cart → checkout → purchase)
- **Cohort Analysis**: Monthly cohorts (repeat purchase behavior)
- **Real-time Requirements**: High (monitor campaigns, flash sales)

### Integration Requirements
- **Essential**: E-commerce platform (Shopify, WooCommerce, BigCommerce)
- **Marketing**: Google Ads, Facebook Pixel, email platforms (Klaviyo)
- **Analytics**: Must handle anonymous → identified user transitions
- **Session replay**: Critical for UX friction analysis
- **A/B testing**: Conversion rate optimization experiments
- **Data warehouse**: Nice-to-have for advanced merchandising analytics

---

## 3. PROVIDER FIT ANALYSIS

### Mixpanel - 75% Fit

**Strengths:**
- Strong funnel analysis (purchase funnel optimization)
- Good for behavioral segmentation (shoppers by purchase patterns)
- Clean UI for marketing/merchandising teams
- E-commerce integrations available
- Startup program: $50K credit (if early-stage DTC brand)

**Weaknesses:**
- Event-based pricing expensive for high-traffic e-commerce (millions of events)
- Not specialized for e-commerce (generic product analytics)
- Lacks built-in session replay (need separate tool)
- Missing e-commerce-specific features (cart recovery, product recommendations)

**Cost at Scale:**
- 0-12 months: $0 (if startup program eligible)
- 12-24 months: $8,000-$25,000/year (30-80M events/month)

**Fit Score Breakdown:**
- Feature Fit: 75% (general analytics, not e-commerce specialized)
- Cost Efficiency: 65% (expensive at e-commerce scale)
- Implementation Speed: 85% (straightforward SDK)
- Scalability: 90% (handles traffic volume)
- Team Fit: 90% (marketing-friendly)

---

### FullStory - 88% Fit

**Strengths:**
- **Session replay built-in** (see exact user shopping journey)
- **E-commerce focus**: Rage clicks, error clicks, frustration signals
- Automatic funnel detection (no manual setup)
- Heatmaps and click tracking (UX optimization)
- Strong for conversion rate optimization (CRO)
- Integrates with e-commerce platforms

**Weaknesses:**
- **No public pricing** (reports of $15K-$100K+/year)
- Expensive for small DTC brands
- More UX-focused than product analytics (less cohort/retention depth)
- Session-based pricing can get costly with high traffic

**Cost at Scale:**
- Estimated: $20,000-$75,000/year (based on session volume)

**Fit Score Breakdown:**
- Feature Fit: 90% (e-commerce + UX focus)
- Cost Efficiency: 55% (expensive, no transparency)
- Implementation Speed: 85% (auto-capture)
- Scalability: 85% (enterprise-grade)
- Team Fit: 95% (UX/marketing friendly)

---

### LogRocket - 85% Fit

**Strengths:**
- Session replay + product analytics combined
- **E-commerce optimized**: Cart abandonment tracking, error monitoring
- Rage click detection (frustration signals)
- Performance monitoring (slow checkout = lost sales)
- Pricing more transparent than FullStory
- Good for debugging checkout issues

**Weaknesses:**
- Session-based pricing scales with traffic (can get expensive)
- Less sophisticated behavioral analytics than Mixpanel/Amplitude
- Web-focused (mobile replay newer)

**Cost at Scale:**
- Free tier: 1,000 sessions/month
- Paid: $69/month (Team) → $295/month (Professional) → Enterprise custom
- Estimated at scale: $5,000-$25,000/year

**Fit Score Breakdown:**
- Feature Fit: 85% (session replay + analytics for e-commerce)
- Cost Efficiency: 75% (transparent pricing, moderate cost)
- Implementation Speed: 90% (quick setup)
- Scalability: 80% (handles growth well)
- Team Fit: 90% (accessible to non-technical teams)

---

### PostHog - 82% Fit

**Strengths:**
- All-in-one: Analytics + session replay + feature flags + A/B testing
- Most cost-effective at scale ($0.00045/event)
- Free tier: 1M events + 5K recordings/month
- E-commerce funnel templates available
- Heatmaps and session replay included
- Open-source option

**Weaknesses:**
- Less e-commerce-specialized than FullStory/LogRocket
- Fewer pre-built e-commerce integrations
- UI less polished for non-technical merchandising teams
- E-commerce features newer (still maturing)

**Cost at Scale:**
- 0-12 months: $500-$2,000/year (5-10M events)
- 12-24 months: $5,000-$15,000/year (20-50M events)
- Session replay add-on: Affordable compared to FullStory

**Fit Score Breakdown:**
- Feature Fit: 80% (general-purpose but growing e-commerce features)
- Cost Efficiency: 95% (best TCO)
- Implementation Speed: 85% (fast SDK setup)
- Scalability: 90% (handles high volume)
- Team Fit: 75% (more technical)

---

### Google Analytics 4 + BigQuery - 78% Fit

**Strengths:**
- **Free** (unlimited events)
- E-commerce tracking built-in (purchase events, revenue, product impressions)
- Google Ads integration (attribution)
- Enhanced e-commerce reports
- BigQuery export for advanced analysis
- Familiar to marketing teams

**Weaknesses:**
- **Not true product analytics** (marketing analytics focus)
- Limited behavioral cohorts/retention analysis
- UI not designed for product teams
- Sampling at high volumes (unless BigQuery)
- Session replay not included (need separate tool)

**Cost at Scale:**
- Always free (unless paying for BigQuery storage)

**Fit Score Breakdown:**
- Feature Fit: 70% (e-commerce tracking but limited product insights)
- Cost Efficiency: 100% (free)
- Implementation Speed: 75% (complex e-commerce setup)
- Scalability: 100% (Google scale)
- Team Fit: 80% (marketing-friendly, less so for product teams)

---

### Heap - 70% Fit

**Strengths:**
- Automatic event tracking (captures all clicks/pageviews)
- Retroactive analysis (define funnels after data collected)
- E-commerce integrations available
- Good for teams without analytics engineering

**Weaknesses:**
- Auto-capture creates massive data bloat on e-commerce sites
- No public pricing (expensive - $30K-$85K/year reported)
- Less cost-effective than alternatives
- Lacks session replay (need separate tool)

**Cost at Scale:**
- Estimated: $25,000-$80,000/year

**Fit Score Breakdown:**
- Feature Fit: 75% (captures everything but overwhelming)
- Cost Efficiency: 40% (expensive for e-commerce scale)
- Implementation Speed: 90% (no event planning needed)
- Scalability: 80% (handles volume but costly)
- Team Fit: 80% (non-technical friendly)

---

## 4. E-COMMERCE-SPECIFIC PROVIDER COMPARISON

### Session Replay Priority (High for E-commerce)

| Provider   | Session Replay | Cost          | E-commerce Features           |
|------------|----------------|---------------|-------------------------------|
| FullStory  | ✓ (Best)       | $$$$ (High)   | Rage clicks, auto-funnels     |
| LogRocket  | ✓ (Great)      | $$$ (Moderate)| Cart abandonment, errors      |
| PostHog    | ✓ (Good)       | $ (Low)       | Growing e-commerce features   |
| Mixpanel   | ✗ (Need add-on)| $$$ (High)    | General product analytics     |
| GA4        | ✗ (Need tool)  | Free          | E-commerce reports only       |
| Heap       | ✗ (Need add-on)| $$$$ (High)   | Auto-capture everything       |

**Best for Session Replay**: LogRocket (balance of features + transparent pricing)

---

## 5. COST ANALYSIS (24-MONTH TCO)

### Scenario: DTC E-commerce Brand Growing from $500K → $5M GMV

**Assumptions:**
- Event volume: 10M → 80M events/month (product views, carts, purchases)
- Traffic: 100K → 500K monthly visitors
- Conversion rate: 2-3%
- Team: Marketing, product, merchandising (5-10 people using analytics)

**Provider TCO Comparison:**

| Provider    | Months 0-12 | Months 13-24 | 24-Month Total | Notes                                |
|-------------|-------------|--------------|----------------|--------------------------------------|
| PostHog     | $3,000      | $18,000      | $21,000        | Analytics + session replay all-in-one|
| LogRocket   | $8,000      | $20,000      | $28,000        | Session replay focus                 |
| Mixpanel    | $0 (credits)| $20,000      | $20,000        | If startup program, else $15K year 1 |
| FullStory   | $35,000     | $55,000      | $90,000        | Premium pricing, no transparency     |
| GA4         | $0          | $0           | $0             | Free but limited, need replay tool   |
| Heap        | $40,000     | $60,000      | $100,000       | Expensive auto-capture               |

**Winner: PostHog (cost) or LogRocket (e-commerce specialization)**

---

## 6. DECISION FRAMEWORK

### Choose LogRocket If:
- Session replay is top priority (see exact user struggles)
- Cart abandonment and checkout optimization critical
- Budget allows $500-$2K/month
- Marketing/UX teams need accessible tool
- Want transparent pricing (no sales calls)

### Choose PostHog If:
- Cost efficiency critical (high traffic = high costs elsewhere)
- Want all-in-one (analytics + replay + A/B testing)
- Technical team can handle setup
- Need to run experiments on site (feature flags + A/B tests)
- Long-term TCO optimization

### Choose FullStory If:
- Enterprise budget ($50K+/year)
- Need absolute best session replay + analytics
- UX optimization is core competency
- Team is non-technical (need easiest tool)
- Willing to pay premium for quality

### Choose Mixpanel + Separate Replay Tool If:
- Qualify for startup program ($50K credit)
- Need robust product analytics beyond e-commerce
- Can budget for session replay separately (Hotjar, Clarity)
- Cross-functional team (product + marketing)

### Choose GA4 (Temporary) If:
- Pre-revenue or very early stage
- Need basic e-commerce tracking only
- Zero budget for analytics
- Plan to upgrade once profitable
- Combine with free session replay (Microsoft Clarity)

---

## 7. E-COMMERCE IMPLEMENTATION CHECKLIST

### Phase 1: Purchase Funnel Tracking (Week 1-2)
- [ ] Track e-commerce events:
  - Product viewed (product ID, category, price)
  - Added to cart
  - Checkout initiated
  - Payment info entered
  - Purchase completed (revenue, order ID, products)
- [ ] Set up purchase funnel visualization
- [ ] Configure revenue tracking

### Phase 2: Session Replay + UX Analysis (Week 3)
- [ ] Enable session replay (LogRocket/PostHog/FullStory)
- [ ] Filter sessions: Cart abandonment, error encounters
- [ ] Identify friction points (rage clicks, dead clicks)
- [ ] Watch checkout failure sessions

### Phase 3: Advanced Analytics (Week 4+)
- [ ] Customer cohort analysis (first purchase → repeat purchase)
- [ ] Product recommendation logic (collaborative filtering via events)
- [ ] Cart abandonment email triggers (integrate with Klaviyo)
- [ ] A/B test checkout flow variations
- [ ] Attribution: Which channels drive highest LTV customers?

---

## 8. CRITICAL E-COMMERCE METRICS

**Conversion Funnel:**
- Product page view → Add to cart: X%
- Add to cart → Checkout initiated: Y%
- Checkout initiated → Purchase: Z%
- Overall conversion rate: X × Y × Z

**Cart Abandonment:**
- Cart abandonment rate: (Carts - Purchases) / Carts
- Recovery rate: Abandoned cart emails → purchases

**Customer Value:**
- Average order value (AOV)
- Customer lifetime value (LTV)
- Repeat purchase rate
- Time between purchases

**UX Metrics (Session Replay):**
- Checkout completion time
- Error rate in checkout
- Rage clicks on checkout page
- Mobile vs desktop conversion gap

---

## 9. COMMON E-COMMERCE PITFALLS

1. **Tracking only purchases**: Miss critical drop-off points (cart, checkout).
2. **Ignoring mobile**: 60-70% of traffic is mobile but desktop converts better - track separately.
3. **No session replay**: Can't diagnose WHY users abandon without seeing their journey.
4. **Over-relying on GA4**: Not designed for product-level insights (use for marketing attribution only).
5. **Event bloat**: Every product impression tracked = millions of events = high costs.

---

## 10. SESSION REPLAY: CRITICAL FOR E-COMMERCE

**Why Session Replay Matters:**
- **See** exactly where users struggle (broken UI, confusing flow)
- **Diagnose** checkout errors that analytics alone can't explain
- **Prioritize** fixes based on actual user pain (not guesses)

**Use Cases:**
- User rage-clicks "Checkout" button (not working) → Fix immediately
- Mobile users can't enter credit card (keyboard issues) → Fix UX
- Users confused by shipping options → Simplify UI

**Recommendation**: Don't run e-commerce without session replay. It's not optional.

---

## 11. RECOMMENDED CHOICE

**PRIMARY**: LogRocket (if budget allows $500-$2K/month)

**Rationale:**
- Best balance of session replay + analytics for e-commerce
- Purpose-built for e-commerce/conversion optimization
- Transparent pricing (no sales runaround)
- Accessible to marketing/UX teams (not just product/eng)
- Cart abandonment and error tracking built-in

**SECONDARY**: PostHog (if cost-conscious)

**Rationale:**
- All-in-one platform (analytics + replay + A/B testing)
- 30-50% cheaper than LogRocket at scale
- Growing e-commerce feature set
- Best long-term TCO for high-traffic sites

**ENTERPRISE**: FullStory (if budget >$50K/year and UX is core)

**Rationale:**
- Absolute best session replay and UX analytics
- Auto-funnel detection (less manual work)
- Premium support and features
- Worth the cost if UX optimization is strategic advantage

**BUDGET/TEMPORARY**: GA4 + Microsoft Clarity (free session replay)

**Rationale:**
- $0 cost while validating product
- Migrate to LogRocket/PostHog once profitable
- Clarity provides basic session replay for free

---

## 12. HYBRID APPROACH (COST OPTIMIZATION)

**Best-of-Breed Stack:**
- **GA4** (free): Marketing attribution, traffic sources
- **PostHog** ($200-$1K/month): Product analytics, A/B testing
- **Microsoft Clarity** (free): Basic session replay
- **Total Cost**: $200-$1K/month

**All-in-One Stack:**
- **LogRocket** ($500-$2K/month): Analytics + session replay
- **Total Cost**: $500-$2K/month

**Premium Stack:**
- **FullStory** ($3K-$8K/month): Premium analytics + session replay
- **Amplitude** (if needed): Deep behavioral analytics
- **Total Cost**: $3K-$12K/month

---

END OF USE CASE ANALYSIS
