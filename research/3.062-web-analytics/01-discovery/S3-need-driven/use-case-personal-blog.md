# Use Case: Personal Blog

**Traffic:** <10,000 pageviews/month
**Priority:** Simple stats, free tier, minimal setup
**Technical Skill:** Non-technical to beginner

## Scenario Description

A personal blog or side project with limited traffic, managed by an individual developer or content creator. The primary goal is to understand basic traffic patterns without complexity or cost.

**Typical Examples:**
- Personal tech blog
- Side project landing page
- Portfolio website
- Small newsletter site
- Indie maker project

## Requirements Analysis

### Must-Have Requirements (4 critical)

1. **Cost: Free or <$10/month**
   - Side projects rarely generate revenue
   - Budget constraint is absolute
   - Must justify any cost with clear value

2. **Setup time: <5 minutes**
   - No complex configuration
   - Single script tag integration
   - Works immediately after setup

3. **Privacy: Cookie-less, no consent banner needed**
   - Avoid friction with cookie banners
   - GDPR-compliant without legal review
   - Simple privacy story

4. **Maintenance: Zero ongoing maintenance**
   - No server management
   - No updates required
   - No monitoring needed

### Nice-to-Have Requirements (9 additional)

5. **Script size: <5KB** - Avoid performance impact on page load
6. **Real-time data** - See traffic as it happens
7. **Basic metrics** - Pageviews, traffic sources, devices
8. **Custom events** - Track button clicks, signups
9. **Reliability: 99%+ uptime** - Always available when checking
10. **Data retention: 90+ days** - Compare month-over-month trends
11. **Export capability** - Download data if needed
12. **Mobile-friendly dashboard** - Check stats on phone
13. **Clear documentation** - Easy to understand setup guides

## Provider Evaluation

### Option 1: GoatCounter (96% fit) - RECOMMENDED

**Scoring:**
- Cost: Free (donation-supported) ✅ 100%
- Setup: 5-10 minutes ✅ 80%
- Privacy: No unique identifiers, GDPR-compliant ✅ 100%
- Maintenance: Zero (fully managed) ✅ 100%
- Script size: 3.5 KB ✅ 100%
- Real-time: Yes ✅ 100%
- Basic metrics: Pageviews, sources, devices ✅ 100%
- Custom events: Available ✅ 100%
- Reliability: 95-98% (solo developer) ⚠️ 70%
- Data retention: 180 days ✅ 100%
- Export: CSV available ✅ 100%
- Mobile-friendly: Yes ✅ 100%
- Documentation: Good ✅ 100%

**Overall: 12.5/13 = 96%**

**Strengths:**
- Completely free (no hidden costs or tier limits)
- Custom events included (rare for free tier)
- Open-source (can self-host if needed)
- Clean, simple interface
- CSV export for data portability
- 180-day retention (better than many paid options)

**Gaps:**
- Solo developer reliability risk (95-98% uptime vs 99.9% enterprise)
- Small team means slower feature development
- Community support only

**Why Recommended:**
GoatCounter is purpose-built for exactly this use case: personal sites that need more than basic stats but can't justify paying $10-20/month. Custom events enable tracking newsletter signups or product launches. The solo developer risk is mitigated by open-source code (community could fork if abandoned).

### Option 2: Cloudflare Web Analytics (87% fit)

**Scoring:**
- Cost: Free forever ✅ 100%
- Setup: 2-5 minutes ✅ 100%
- Privacy: Cookie-less, GDPR-compliant ✅ 100%
- Maintenance: Zero ✅ 100%
- Script size: Minimal ✅ 100%
- Real-time: Yes ✅ 100%
- Basic metrics: Pageviews, sources, devices ✅ 100%
- Custom events: Limited capability ❌ 30%
- Reliability: 99.99%+ (Cloudflare SLA) ✅ 100%
- Data retention: 6+ months ✅ 100%
- Export: No export capability ❌ 0%
- Mobile-friendly: Yes ✅ 100%
- Documentation: Excellent ✅ 100%

**Overall: 11.3/13 = 87%**

**Strengths:**
- Cloudflare reliability and infrastructure
- Absolutely free with no limits
- Best-in-class uptime
- Zero setup if already using Cloudflare
- No vendor risk (Cloudflare isn't going anywhere)

**Gaps:**
- Limited custom events capability
- No data export (vendor lock-in)
- Basic features only

**When to Choose:**
Best for absolute simplicity where custom event tracking isn't needed. If your blog is already using Cloudflare CDN, this is a one-click addition. Maximum reliability with zero vendor risk.

### Option 3: Plausible $9/month (99% fit)

**Scoring:**
- Cost: $9/month ⚠️ 90% (slightly over free target)
- Setup: 2-5 minutes ✅ 100%
- Privacy: Cookie-less certified ✅ 100%
- Maintenance: Zero ✅ 100%
- Script size: <1 KB ✅ 100%
- Real-time: Yes ✅ 100%
- Basic metrics: Comprehensive ✅ 100%
- Custom events: Available ✅ 100%
- Reliability: 99.9%+ SLA ✅ 100%
- Data retention: Unlimited ✅ 100%
- Export: CSV ✅ 100%
- Mobile-friendly: Excellent ✅ 100%
- Documentation: Best-in-class ✅ 100%

**Overall: 12.9/13 = 99%**

**Strengths:**
- Most polished UI in the category
- GDPR Article 6(1)(f) certified with legal docs
- <1KB script (fastest loading)
- Unlimited data retention
- Open-source (can self-host)
- Bootstrapped company (sustainable business model)

**Gaps:**
- $9/month = $108/year (not free)
- May be overkill for side projects

**When to Choose:**
If you can justify $9/month, this is the best overall solution. Perfect for professional bloggers, monetized side projects, or anyone who values polish and wants to support privacy-first businesses.

### Option 4: Umami Self-Hosted (79% fit)

**Scoring:**
- Cost: Free + ~$5/month infrastructure ✅ 95%
- Setup: 15-30 minutes Docker ⚠️ 50%
- Privacy: Cookie-less, full data control ✅ 100%
- Maintenance: Requires updates, monitoring ❌ 40%
- Script size: <2 KB ✅ 100%
- Real-time: Yes ✅ 100%
- Basic metrics: Comprehensive ✅ 100%
- Custom events: Available ✅ 100%
- Reliability: Self-managed (DIY) ⚠️ 60%
- Data retention: Unlimited ✅ 100%
- Export: CSV ✅ 100%
- Mobile-friendly: Yes ✅ 100%
- Documentation: Good but technical ⚠️ 80%

**Overall: 10.25/13 = 79%**

**Strengths:**
- Very low cost ($5-10/month infrastructure)
- Full data ownership
- Open-source and auditable
- Can customize as needed

**Gaps:**
- Setup complexity (Docker, database, deployment)
- Ongoing maintenance burden
- Self-managed reliability
- Requires technical skills

**When to Choose:**
Only if you're comfortable with Docker and want the learning experience. The maintenance burden (updates, monitoring, backups) isn't worth the $5-10/month savings for most side projects. Better for technical bloggers who enjoy infrastructure.

### Option 5: Counter.dev (72% fit)

**Scoring:**
- Cost: Free (pay-what-you-want) ✅ 100%
- Setup: 2-5 minutes ✅ 100%
- Privacy: Aggregated data only ✅ 100%
- Maintenance: Zero ✅ 100%
- Script size: Minimal ✅ 100%
- Real-time: Yes ✅ 100%
- Basic metrics: Core analytics ✅ 100%
- Custom events: Not available ❌ 0%
- Reliability: Small team risk ⚠️ 70%
- Data retention: Available ✅ 100%
- Export: Not available ❌ 0%
- Mobile-friendly: Yes ✅ 100%
- Documentation: Minimal ⚠️ 70%

**Overall: 9.4/13 = 72%**

**Strengths:**
- Free with no limitations
- Aggregated data approach (privacy-first)
- Very simple setup
- Germany-based

**Gaps:**
- No custom events (critical for tracking conversions)
- No data export
- Minimal documentation
- Small team reliability risk

**When to Choose:**
Only for the absolute simplest use cases where you just need pageview counts. The lack of custom events is a dealbreaker for most projects.

## Implementation Guide

### Recommended: GoatCounter Setup

**Step 1: Create Account (2 minutes)**
1. Go to goatcounter.com
2. Sign up for free hosted account
3. Choose subdomain: `yoursite.goatcounter.com`

**Step 2: Add Tracking Code (2 minutes)**
```html
<script data-goatcounter="https://yoursite.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
```

Add before closing `</body>` tag on all pages.

**Step 3: Verify Installation (1 minute)**
1. Visit your website
2. Check GoatCounter dashboard
3. You should see the pageview immediately

**Step 4: Configure Custom Events (Optional)**
Track newsletter signups:
```html
<button onclick="goatcounter.count({
  path: 'signup-clicked',
  title: 'Newsletter Signup',
  event: true
})">Subscribe</button>
```

**Total Setup Time: 5-10 minutes**

### Alternative: Cloudflare Setup

**Step 1: Enable in Cloudflare Dashboard (1 minute)**
1. Log into Cloudflare
2. Select your site
3. Go to Analytics > Web Analytics
4. Click "Enable"

**Step 2: Add Tracking Code (1 minute)**
```html
<!-- Cloudflare Web Analytics -->
<script defer src='https://static.cloudflareinsights.com/beacon.min.js'
        data-cf-beacon='{"token": "YOUR_TOKEN"}'></script>
```

**Step 3: Verify (1 minute)**
Check Cloudflare dashboard for incoming data.

**Total Setup Time: 3-5 minutes**

## Cost Analysis

### 1-Year Total Cost of Ownership

**GoatCounter (Free)**
- Subscription: $0
- Infrastructure: $0
- Setup time: 10 min × $0 (side project) = $0
- Maintenance: 0 hrs/month × $0 = $0
- **Total: $0/year**

**Cloudflare (Free)**
- Subscription: $0
- Infrastructure: $0
- Setup time: 5 min × $0 = $0
- Maintenance: 0 hrs/month × $0 = $0
- **Total: $0/year**

**Plausible ($9/month)**
- Subscription: $9/month × 12 = $108
- Infrastructure: $0
- Setup time: 5 min × $0 = $0
- Maintenance: 0 hrs/month × $0 = $0
- **Total: $108/year**

**Umami Self-Hosted**
- Subscription: $0
- Infrastructure: $5/month × 12 = $60
- Setup time: 30 min × $100/hr (if valued) = $50
- Maintenance: 2 hrs/month × 12 × $100/hr = $2,400
- **Total: $60-2,510/year** (depending on time value)

### 3-Year Total Cost of Ownership

| Provider | Year 1 | Year 2 | Year 3 | Total |
|----------|--------|--------|--------|-------|
| GoatCounter | $0 | $0 | $0 | **$0** |
| Cloudflare | $0 | $0 | $0 | **$0** |
| Plausible | $108 | $108 | $108 | **$324** |
| Umami | $60 | $60 | $60 | **$180** (infra only) |

### Cost Justification

**When Free Is Right:**
For side projects not generating revenue, paying $108/year for analytics is hard to justify. GoatCounter provides everything needed at zero cost.

**When Paid Makes Sense:**
- Professional blog with affiliate income ($500+/month)
- Sponsored content requiring traffic proof
- Portfolio site for job hunting (polish matters)
- Learning platform with paid courses

At $500/month revenue, $9/month (1.8% of revenue) is easily justified for professional analytics.

## Decision Framework

### Choose GoatCounter if:
- ✅ Budget is absolutely $0
- ✅ Need custom event tracking
- ✅ Want data export capability
- ✅ Comfortable with 95-98% reliability
- ✅ Support open-source projects

### Choose Cloudflare if:
- ✅ Already using Cloudflare
- ✅ Don't need custom events
- ✅ Want maximum reliability (99.99%+)
- ✅ Prefer corporate-backed solution
- ✅ Basic stats sufficient

### Choose Plausible if:
- ✅ Can afford $9/month
- ✅ Want most polished experience
- ✅ Need GDPR legal documentation
- ✅ Value open-source + paid support
- ✅ Plan to grow (unlimited retention)

### Choose Umami if:
- ✅ Comfortable with Docker
- ✅ Want learning experience
- ✅ Need data sovereignty
- ✅ Have time for maintenance
- ✅ Technical background

## Migration Path

### Starting Out (Month 1-6)
**Use:** GoatCounter or Cloudflare (free)
**Why:** Validate project traction before paying
**Monitor:** Pageviews, traffic sources

### Growing (Month 6-12)
**Switch to:** Plausible $9/month
**When:** Hitting 5K+ pageviews/month, monetization starting
**Trigger:** First $100/month revenue, or need for polish

### Scaling (Month 12+)
**Evaluate:** Umami self-hosted or Plausible upgrade
**When:** 50K+ pageviews/month, multiple projects
**Trigger:** Cost efficiency becomes important ($9/month × 3 sites = $27/month vs $20/month self-hosted for all)

## Common Questions

### Q: Do I need analytics at all for a side project?

**A:** Only if you want to:
- Validate that people are actually visiting
- Understand which content resonates
- Track conversion goals (signups, purchases)
- Prove traction to investors/employers

If it's truly just for you, you might not need analytics.

### Q: GoatCounter vs Cloudflare - which is really better?

**A:**
- **GoatCounter**: Better if you need custom events, data export, or open-source
- **Cloudflare**: Better if you prioritize reliability, simplicity, or already use Cloudflare

Both are excellent free options. Try both and see which dashboard you prefer.

### Q: Should I just use Google Analytics since it's free?

**A:** No for several reasons:
1. **Script size**: 45KB vs <5KB (hurts page load, SEO)
2. **Privacy**: Requires cookie consent banner in EU
3. **Complexity**: Overkill for personal projects
4. **GDPR**: Court rulings against GA in EU countries

GoatCounter or Cloudflare are better free alternatives.

### Q: When is paying $9/month for Plausible worth it?

**A:**
- Professional blog with income ($100+/month)
- Portfolio site for job hunting (polish matters)
- Client work requiring legal compliance docs
- You value supporting privacy-focused businesses

### Q: Can I start free and upgrade later?

**A:** Yes, all recommended providers:
- **GoatCounter → Plausible**: Export CSV, manual migration
- **Cloudflare → Plausible**: No export, fresh start (not a problem for small sites)
- **Free tier → Paid tier**: Usually seamless upgrade

Start free, upgrade when justified.

## Related Use Cases

- **SaaS Landing Page**: If you're tracking conversions and growth metrics
- **Developer Documentation**: If you're documenting open-source projects
- **Bootstrapped Startup**: If your side project becomes a real business

## Real-World Examples

**Personal Tech Blog**
- Using: GoatCounter
- Traffic: 3,000 pageviews/month
- Events tracked: Newsletter signups, external link clicks
- Cost: $0/month
- Decision: Custom events essential, budget is zero

**Indie Hacker Portfolio**
- Using: Cloudflare
- Traffic: 500 pageviews/month
- Events tracked: None needed
- Cost: $0/month (already using Cloudflare CDN)
- Decision: Simplicity + reliability, basic stats sufficient

**Professional Developer Blog**
- Using: Plausible
- Traffic: 15,000 pageviews/month
- Events tracked: Newsletter signups, course purchases
- Cost: $9/month
- Revenue: $800/month (courses)
- Decision: Professional appearance, GDPR docs for EU readers, cost is 1% of revenue
