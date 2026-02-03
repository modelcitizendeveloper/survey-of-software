# Use Case: Developer Documentation

**Traffic:** Variable (100K-5M pageviews/month)
**Priority:** Technical audience, minimal overhead, privacy
**Technical Skill:** Developer-focused, open-source friendly

## Scenario Description

Documentation sites for developer tools, open-source projects, APIs, and technical products. The audience is privacy-conscious developers who appreciate minimal tracking and fast page loads.

**Typical Examples:**
- Open-source project documentation
- API reference documentation
- Developer tool documentation (CLI, SDK, framework)
- Technical blog / engineering blog
- Internal developer portal

## Requirements Analysis

### Must-Have Requirements (5 critical)

1. **Minimal overhead: <2KB script, fast page load**
   - Developers inspect Network tab
   - Heavy analytics = bad impression
   - Documentation speed is critical (SEO, UX)

2. **Privacy-first: No cookies, no tracking without consent**
   - Developer audience is privacy-conscious
   - Avoid creepy tracking
   - Respect Do Not Track

3. **Technical transparency: Open-source preferred**
   - Developers want to inspect code
   - Trust through transparency
   - Ability to self-host if needed

4. **Search analytics: What docs are people looking for?**
   - Track search queries (what's missing)
   - Most visited pages
   - User journeys through docs

5. **Cost-effective: Free or <$20/month for OSS projects**
   - Open-source projects have no budget
   - Justify cost to maintainers
   - Community-supported solutions preferred

### Nice-to-Have Requirements (8 additional)

6. **Real-time traffic** - See when docs go viral (Hacker News, Reddit)
7. **Version tracking** - Separate v1, v2, v3 docs traffic
8. **Referral sources** - Understand how people find docs
9. **Exit pages** - Where do people give up (documentation gaps)
10. **Custom events** - Track: copy_code_snippet, expand_example, switch_language
11. **API access** - Embed metrics in OSS project dashboards
12. **Zero maintenance** - No server management for maintainers
13. **Community-friendly** - Support OSS projects (free tier, discounts)

## Provider Evaluation

### Option 1: GoatCounter (96% fit) - RECOMMENDED FOR OSS

**Scoring:**
- Minimal overhead: 3.5 KB ✅ 95%
- Privacy-first: No unique identifiers, GDPR-compliant ✅ 100%
- Open-source: Fully auditable ✅ 100%
- Search analytics: Track searches as events ✅ 100%
- Cost: Free (donation-supported) ✅ 100%
- Real-time: Yes ✅ 100%
- Version tracking: Path-based filtering ✅ 100%
- Referral sources: Yes ✅ 100%
- Exit pages: Not built-in ⚠️ 60%
- Custom events: Available ✅ 100%
- API access: Yes ✅ 100%
- Zero maintenance: Hosted (zero) ✅ 100%
- Community-friendly: Free for OSS ✅ 100%

**Overall: 12.55/13 = 97%**

**Strengths:**
- Purpose-built for sites like documentation
- Solo developer project (Martin Tournoij) - understands OSS
- 3.5KB script (minimal impact)
- Completely free (donation-supported)
- Open-source (can self-host)
- No tracking, no cookies, no fingerprinting
- Developer-friendly API

**Gaps:**
- Exit page analytics not built-in (can track via custom events)
- Solo developer = less feature velocity
- 95-98% uptime (vs 99.9% enterprise)

**Implementation:**
```html
<!-- Simple integration -->
<script data-goatcounter="https://yourproject.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>

<!-- Track search queries -->
<script>
  document.querySelector('#search').addEventListener('input', function(e) {
    if (e.target.value.length > 3) {
      window.goatcounter.count({
        path: 'search-' + e.target.value,
        title: 'Search: ' + e.target.value,
        event: true
      })
    }
  })
</script>

<!-- Track code snippet copies -->
<script>
  document.querySelectorAll('.copy-button').forEach(btn => {
    btn.addEventListener('click', function() {
      window.goatcounter.count({
        path: 'code-copied',
        title: 'Code Snippet Copied',
        event: true
      })
    })
  })
</script>
```

**Why Recommended:**
Perfect fit for open-source documentation. The developer audience will appreciate the transparency (open-source), privacy (no tracking), and minimal footprint (3.5KB). Free tier eliminates budget concerns for OSS maintainers.

### Option 2: Plausible (100% fit) - RECOMMENDED FOR COMMERCIAL

**Scoring:**
- Minimal overhead: <1 KB (best) ✅ 100%
- Privacy-first: Cookie-less certified ✅ 100%
- Open-source: Fully auditable ✅ 100%
- Search analytics: Custom events ✅ 100%
- Cost: $9/month (10K tier) OR self-hosted ✅ 100%
- Real-time: Yes ✅ 100%
- Version tracking: Custom properties ✅ 100%
- Referral sources: Yes ✅ 100%
- Exit pages: Not built-in ⚠️ 70%
- Custom events: Available with properties ✅ 100%
- API access: Yes ✅ 100%
- Zero maintenance: Hosted (zero) ✅ 100%
- Community-friendly: OSS discount available ✅ 100%

**Overall: 12.7/13 = 98%**

**Strengths:**
- <1KB script (fastest possible)
- GDPR Article 6(1)(f) certified (legal documentation)
- Beautiful, simple dashboard
- Open-source (AGPLv3)
- Can self-host (same as hosted features)
- Bootstrapped company (privacy-aligned)
- 33% discount for OSS projects

**Gaps:**
- $9/month may be hard for unfunded OSS (but can self-host for free)

**Implementation:**
```html
<!-- Plausible script -->
<script defer data-domain="docs.yourproject.com"
        src="https://plausible.io/js/script.js"></script>

<!-- Track version views -->
<script>
  plausible('pageview', {
    props: {
      version: 'v2.0',
      language: 'javascript'
    }
  })
</script>

<!-- Track search -->
<script>
  function trackSearch(query) {
    plausible('Search', {
      props: {
        query: query,
        results: resultsCount
      }
    })
  }
</script>
```

**When to Choose:**
Best for commercial developer tools or well-funded OSS projects. The $9/month (or $6/month with OSS discount) is easily justified for professional documentation. The <1KB script is the fastest option.

### Option 3: Umami Self-Hosted (93% fit)

**Scoring:**
- Minimal overhead: <2 KB ✅ 100%
- Privacy-first: Cookie-less, no tracking ✅ 100%
- Open-source: MIT license ✅ 100%
- Search analytics: Custom events ✅ 100%
- Cost: Free + $5/month infrastructure ✅ 95%
- Real-time: Yes ✅ 100%
- Version tracking: Custom properties ✅ 100%
- Referral sources: Yes ✅ 100%
- Exit pages: Bounce rate tracking ⚠️ 70%
- Custom events: Available ✅ 100%
- API access: Yes ✅ 100%
- Zero maintenance: Requires Docker management ❌ 50%
- Community-friendly: Free OSS ✅ 100%

**Overall: 12.15/13 = 93%**

**Strengths:**
- Truly self-hosted (full control)
- <2KB script
- MIT license (most permissive)
- Very active development
- Modern React UI
- Simple Docker deployment

**Gaps:**
- Maintenance required (updates, backups)
- Not zero maintenance (disqualifying for some OSS maintainers)
- 15-30 minute setup

**Implementation:**
```bash
# Deploy with Docker Compose
git clone https://github.com/umami-software/umami.git
cd umami
docker-compose up -d

# Access at http://localhost:3000
# Add tracking script to docs
```

```html
<script async defer
        data-website-id="YOUR_WEBSITE_ID"
        src="https://analytics.yourproject.com/umami.js"></script>
```

**When to Choose:**
Best for OSS projects with technical maintainers who want full control and don't mind maintenance. The $5/month infrastructure cost is minimal, and self-hosting avoids any vendor dependency.

### Option 4: Cloudflare Web Analytics (85% fit)

**Scoring:**
- Minimal overhead: Minimal script ✅ 100%
- Privacy-first: Cookie-less, privacy-preserving ✅ 100%
- Open-source: Proprietary ❌ 0%
- Search analytics: Not available ❌ 30%
- Cost: Free ✅ 100%
- Real-time: Yes ✅ 100%
- Version tracking: Path-based ⚠️ 70%
- Referral sources: Yes ✅ 100%
- Exit pages: Bounce rate ⚠️ 60%
- Custom events: Not available ❌ 0%
- API access: Limited ⚠️ 50%
- Zero maintenance: Yes ✅ 100%
- Community-friendly: Free for all ✅ 100%

**Overall: 8.1/13 = 62%**

**Strengths:**
- Completely free
- Cloudflare reliability (99.99%+)
- Zero setup if using Cloudflare
- Privacy-preserving by design

**Gaps:**
- **Proprietary** (developers can't inspect code)
- **No custom events** (can't track searches, code copies)
- Limited API access
- Not purpose-built for developer docs

**When to Choose:**
Only for the simplest documentation sites where basic pageview stats are sufficient and the site already uses Cloudflare. The lack of custom events is a dealbreaker for most technical documentation.

### Option 5: Simple Analytics (90% fit)

**Scoring:**
- Minimal overhead: ~2 KB ✅ 100%
- Privacy-first: Cookie-less, GDPR-first ✅ 100%
- Open-source: Proprietary ❌ 0%
- Search analytics: Custom events ✅ 100%
- Cost: €19/month OR €9/month annual ⚠️ 80%
- Real-time: Yes ✅ 100%
- Version tracking: Custom events ✅ 100%
- Referral sources: Yes ✅ 100%
- Exit pages: Not built-in ⚠️ 60%
- Custom events: Available ✅ 100%
- API access: Yes ✅ 100%
- Zero maintenance: Hosted ✅ 100%
- Community-friendly: No specific OSS program ⚠️ 60%

**Overall: 11.0/13 = 85%**

**Strengths:**
- Privacy-first, EU-based
- Clean, simple interface
- Custom events available
- Good API

**Gaps:**
- Proprietary (not open-source)
- Higher cost for OSS projects (no discount)
- Less community-aligned than GoatCounter/Plausible

**When to Choose:**
Good alternative to Plausible for commercial docs if annual pricing is attractive ($9/month = $108/year). Not ideal for OSS due to lack of open-source code and OSS discount.

### Option 6: PostHog Free Tier (70% fit)

**Scoring:**
- Minimal overhead: ~5 KB (heavy) ❌ 40%
- Privacy-first: Cookie-less mode available ⚠️ 90%
- Open-source: Yes (MIT) ✅ 100%
- Search analytics: Full event tracking ✅ 100%
- Cost: Free (1M events) ✅ 100%
- Real-time: Yes ✅ 100%
- Version tracking: Custom properties ✅ 100%
- Referral sources: Yes ✅ 100%
- Exit pages: Exit analysis ✅ 100%
- Custom events: Full event tracking ✅ 100%
- API access: Comprehensive ✅ 100%
- Zero maintenance: Hosted ✅ 100%
- Community-friendly: 1M free events ✅ 100%

**Overall: 12.3/13 = 95%**

**But:**
- Script size (5KB) is disqualifying for docs
- Overkill for simple documentation analytics
- Better suited for product analytics, not content

**When to Choose:**
Only if you're already using PostHog for product analytics and want to reuse the same infrastructure. The 5KB script is too heavy for documentation where <2KB is expected.

## Implementation Guide

### Recommended: GoatCounter for OSS Projects

**Step 1: Create Account (2 minutes)**
1. Go to goatcounter.com
2. Sign up for free account
3. Choose subdomain: `yourproject.goatcounter.com`

**Step 2: Add Tracking Code (1 minute)**
```html
<!-- Add before </body> in your docs template -->
<script data-goatcounter="https://yourproject.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
```

**Step 3: Track Documentation-Specific Events (10 minutes)**

**Search Queries:**
```javascript
// Track what users search for (identify missing docs)
document.querySelector('#docsearch').addEventListener('submit', function(e) {
  const query = e.target.querySelector('input').value
  window.goatcounter.count({
    path: 'search',
    title: 'Search: ' + query,
    event: true
  })
})
```

**Code Snippet Copies:**
```javascript
// Track which code examples are most useful
document.querySelectorAll('.copy-code-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    const language = this.dataset.language
    const page = window.location.pathname
    window.goatcounter.count({
      path: 'code-copied',
      title: 'Code copied: ' + language + ' on ' + page,
      event: true
    })
  })
})
```

**Version Selection:**
```javascript
// Track which documentation versions are used
document.querySelector('#version-selector').addEventListener('change', function(e) {
  window.goatcounter.count({
    path: 'version-switch',
    title: 'Switched to: ' + e.target.value,
    event: true
  })
})
```

**Language/Framework Toggle:**
```javascript
// Track language preference (Python, JavaScript, Go, etc.)
document.querySelectorAll('.language-tab').forEach(function(tab) {
  tab.addEventListener('click', function() {
    const language = this.dataset.lang
    window.goatcounter.count({
      path: 'language-selected',
      title: 'Language: ' + language,
      event: true
    })
  })
})
```

**External Link Clicks:**
```javascript
// Track when users leave docs (to GitHub, Stack Overflow, etc.)
document.querySelectorAll('a[href^="http"]').forEach(function(link) {
  link.addEventListener('click', function() {
    if (!this.href.includes(window.location.hostname)) {
      window.goatcounter.count({
        path: 'external-link',
        title: 'External: ' + this.href,
        event: true
      })
    }
  })
})
```

**Total Setup Time: 15 minutes**

### Alternative: Plausible for Commercial Docs

**Step 1: Sign Up (2 minutes)**
1. Go to plausible.io
2. Start free trial
3. Add domain: `docs.yourproduct.com`

**Step 2: Add Script (1 minute)**
```html
<script defer data-domain="docs.yourproduct.com"
        src="https://plausible.io/js/script.js"></script>
```

**Step 3: Track Custom Events (10 minutes)**

**Search Tracking:**
```javascript
// Track searches
function trackSearch(query, resultCount) {
  plausible('Search', {
    props: {
      query: query,
      results: resultCount
    }
  })
}
```

**Version Tracking:**
```javascript
// Track version views
plausible('pageview', {
  props: {
    version: 'v2.1',
    docSection: 'api-reference'
  }
})
```

**Code Copies:**
```javascript
// Track code snippet engagement
document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.onclick = () => {
    plausible('Code Copied', {
      props: {
        language: btn.dataset.language,
        page: window.location.pathname
      }
    })
  }
})
```

## Cost Analysis

### 1-Year Total Cost of Ownership

**GoatCounter (Free)**
- Subscription: $0
- Infrastructure: $0
- Setup time: 15 min × $0 (OSS volunteer time) = $0
- Maintenance: 0 hrs/month × $0 = $0
- **Total: $0/year**

**Plausible (Hosted)**
- Subscription: $9/month × 12 = $108/year (10K tier)
- OSS discount (33%): $6/month × 12 = $72/year
- Setup time: 15 min × $0 = $0
- Maintenance: 0 hrs/month × $0 = $0
- **Total: $72-108/year**

**Plausible (Self-Hosted)**
- Subscription: $0
- Infrastructure: $10/month × 12 = $120/year
- Setup time: 2 hours × $100/hr = $200
- Maintenance: 1 hr/month × 12 × $100/hr = $1,200
- **Total: $1,520/year** (with time cost)
- **Total: $120/year** (cash only)

**Umami (Self-Hosted)**
- Subscription: $0
- Infrastructure: $5/month × 12 = $60/year
- Setup time: 1 hour × $100/hr = $100
- Maintenance: 1 hr/month × 12 × $100/hr = $1,200
- **Total: $1,360/year** (with time cost)
- **Total: $60/year** (cash only)

**Cloudflare**
- Subscription: $0
- Infrastructure: $0
- Setup time: 5 min × $0 = $0
- Maintenance: 0 hrs/month × $0 = $0
- **Total: $0/year**
- **Trade-off:** No custom events, proprietary

### 3-Year Total Cost of Ownership

| Provider | Year 1 | Year 2 | Year 3 | 3-Year Total | Notes |
|----------|--------|--------|--------|--------------|-------|
| GoatCounter | $0 | $0 | $0 | **$0** | Free forever |
| Plausible Hosted | $72 | $72 | $72 | **$216** | With OSS discount |
| Plausible Self-Hosted (cash) | $120 | $120 | $120 | **$360** | Infrastructure only |
| Umami Self-Hosted (cash) | $60 | $60 | $60 | **$180** | Cheapest self-hosted |
| Cloudflare | $0 | $0 | $0 | **$0** | Limited features |

### ROI for Documentation Analytics

**Scenario:** Developer tool with 500K monthly doc visitors

**Without analytics:**
- Don't know what docs are missing (search queries unknown)
- Don't know where users get stuck (no exit page tracking)
- Can't prioritize doc improvements (no data)

**With analytics ($0-216 over 3 years):**
- Track top 100 search queries → Write missing docs
- Identify high bounce pages → Improve clarity
- See which code examples are copied → Expand popular examples
- Understand version adoption → Focus on latest version docs

**Value:**
- Better documentation → Faster onboarding
- Faster onboarding → Higher adoption
- Higher adoption → More users/customers
- Improved docs = 10% faster onboarding = 10% more successful users

**Conclusion:** Even $216/year (Plausible) pays for itself if better docs improve user success by any measurable amount.

## Decision Framework

### Choose GoatCounter if:
- ✅ Open-source project (no budget)
- ✅ Privacy-conscious audience
- ✅ Want open-source analytics
- ✅ Need custom event tracking
- ✅ Accept 95-98% uptime
- ✅ Appreciate community-supported projects

**Best for:** OSS documentation, community projects, technical blogs

### Choose Plausible if:
- ✅ Commercial developer tool
- ✅ Can afford $6-9/month (or self-host)
- ✅ Want <1KB script (fastest)
- ✅ Need GDPR legal documentation
- ✅ Appreciate polished UI
- ✅ Value privacy + open-source

**Best for:** Commercial API docs, SaaS developer portals, funded OSS

### Choose Umami if:
- ✅ Want full control (self-hosted)
- ✅ Technical team (comfortable with Docker)
- ✅ Budget is minimal ($5/month infra)
- ✅ MIT license preferred
- ✅ Modern UI important

**Best for:** Self-hosted OSS projects, internal developer portals

### Choose Cloudflare if:
- ✅ Already using Cloudflare
- ✅ Need basic stats only
- ✅ Don't need custom events
- ✅ Want maximum reliability
- ✅ Zero budget, zero maintenance

**Best for:** Simple docs sites, static documentation, basic tracking

### Avoid PostHog for Docs:
- ❌ 5KB script too heavy
- ❌ Overkill for content analytics
- ❌ Better suited for product analytics

## Real-World Examples

### Example 1: Next.js Documentation

**Solution:** Custom analytics (privacy-first)
- Tracks: Page views, search queries, navigation patterns
- Privacy: No cookies, aggregated data only
- Cost: Custom built (OSS project)
- Learning: Even major frameworks avoid heavy analytics

### Example 2: FastAPI Documentation

**Solution:** Google Analytics (surprisingly)
- Why: Creator wanted familiarity, broad adoption
- Trade-off: Privacy concerns, 45KB script
- Community feedback: Some users block GA
- Learning: GA for docs is controversial in dev community

### Example 3: Supabase Documentation

**Solution:** PostHog
- Why: Already using for product analytics
- Custom events: Track which code examples are copied
- Trade-off: Heavier script, but acceptable for product company
- Learning: If already using tool for product, extend to docs

### Example 4: Docusaurus (Open-Source)

**Default:** Allows any analytics
**Common choices:**
- GoatCounter (OSS projects)
- Plausible (commercial projects)
- Google Analytics (controversial)

### Example 5: Stripe API Documentation

**Solution:** Custom internal analytics
- Privacy: Logged-in users only (can attribute to account)
- Events: Which API endpoints docs are viewed
- Use case: Correlate doc usage with API adoption
- Learning: Product docs can be more sophisticated than pure OSS docs

## Documentation-Specific Insights

### What to Track

**1. Content Gaps (via search)**
```javascript
// Most searched terms = missing documentation
// Example findings:
// - "rate limits" (500 searches) → Write rate limit docs
// - "authentication" (300 searches) → Improve auth guide
// - "error codes" (200 searches) → Add error reference
```

**2. User Journeys**
```
Common paths:
1. Getting Started → Installation → First API Call (good flow)
2. Getting Started → Authentication → Back to Search (stuck on auth)
3. API Reference → Pricing → Signup (ready to buy)
```

**3. Version Adoption**
```
- v3.0 docs: 60% of traffic (latest)
- v2.5 docs: 35% of traffic (still popular)
- v1.x docs: 5% of traffic (legacy)
→ Decision: Maintain v2.5 docs, archive v1.x
```

**4. Code Example Engagement**
```javascript
// Which languages are most popular?
- JavaScript examples: 1,000 copies/month
- Python examples: 800 copies/month
- Go examples: 200 copies/month
→ Decision: Expand JavaScript and Python examples
```

**5. External Link Exits**
```
Top exits:
1. GitHub Issues (users need help) → Improve troubleshooting
2. Stack Overflow (searching for answers) → FAQ needed
3. Competitors (comparing features) → Comparison page needed
```

### Metrics That Matter for Docs

**Engagement Metrics:**
- Time on page (longer = more thorough reading or confusion?)
- Scroll depth (did they read the whole page?)
- Code snippet copies (which examples are useful?)
- Search queries (what's missing?)

**Success Metrics:**
- Getting Started → First API Call (onboarding success)
- Docs → Signup (conversion attribution)
- Search → Found page (search effectiveness)
- Low bounce rate on key pages (content quality)

**Health Metrics:**
- 404 errors (broken links to fix)
- High exit pages (content gaps)
- Version adoption (migration progress)
- Mobile vs desktop (mobile docs experience)

## Common Mistakes

### Mistake 1: Using Heavy Analytics (GA, PostHog)
**Problem:** 45KB or 5KB script on documentation site
**Impact:** Slow page loads, developers notice and complain
**Solution:** Use <2KB option (GoatCounter, Plausible, Umami)

### Mistake 2: Not Tracking Search
**Problem:** Missing the #1 signal of content gaps
**Impact:** Don't know what docs to write next
**Solution:** Track all search queries as custom events

### Mistake 3: Ignoring Privacy
**Problem:** Cookie consent banners on developer docs
**Impact:** Developers disable analytics, use ad blockers
**Solution:** Cookie-less analytics (no consent needed)

### Mistake 4: Not Tracking Code Copies
**Problem:** Don't know which examples are useful
**Impact:** Waste time on examples nobody uses
**Solution:** Track copy-to-clipboard events

### Mistake 5: Over-Analyzing
**Problem:** Spending hours in analytics instead of writing docs
**Impact:** Analysis paralysis, no documentation improvements
**Solution:** Weekly review (30 minutes), focus on top 3 insights

## Next Steps

1. **Choose based on project type:**
   - Open-source → GoatCounter (free, open-source)
   - Commercial → Plausible (polished, $6-9/month)
   - Self-hosted preference → Umami ($5/month infra)
   - Basic needs → Cloudflare (free, simple)

2. **Implement tracking:**
   - Day 1: Basic pageview tracking (5 min)
   - Day 2: Search query tracking (10 min)
   - Week 1: Code copy tracking (10 min)
   - Week 2: Version/language tracking (15 min)

3. **Weekly review (30 minutes):**
   - Top 10 visited pages (validate priority)
   - Top 10 search queries (find content gaps)
   - Top exit pages (find friction points)
   - Code copy patterns (popular examples)

4. **Monthly actions:**
   - Write docs for top 3 searched topics
   - Improve top 3 high-bounce pages
   - Expand top 3 most-copied code examples

5. **Quarterly planning:**
   - Review version adoption (plan deprecations)
   - Analyze user journeys (optimize flows)
   - Assess mobile experience (mobile traffic %)

## Related Use Cases

- **Personal Blog**: If you're writing technical content
- **SaaS Landing Page**: If you need conversion tracking
- **Open-Source Project**: If you're tracking project website (not docs)

## Further Reading

- GoatCounter documentation: https://www.goatcounter.com/help
- Plausible documentation: https://plausible.io/docs
- Umami documentation: https://umami.is/docs
- "Why I Don't Use Google Analytics" (developer blog posts)
- "Documentation Metrics That Matter" (Write the Docs)
