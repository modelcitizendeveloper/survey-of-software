# Use Case: Agency Managing Client Sites

## Context

PixelCraft Digital is a 12-person web development agency based in Austin, Texas. They build and maintain WordPress sites, custom web applications, and e-commerce stores for 35 active clients ranging from local restaurants to mid-sized B2B companies. Each client pays between $2,000-10,000 for initial development, then $500-3,000/month for ongoing maintenance and hosting.

The agency's business model depends on reliable client sites. Their maintenance contracts include uptime guarantees (99% uptime SLA), and they've lost two clients in the past year due to prolonged downtime they didn't catch quickly enough. In one case, a client's e-commerce site was down for 8 hours overnight, resulting in lost sales and a terminated contract.

Currently, PixelCraft has a hodgepodge of monitoring solutions. Some clients have basic UptimeRobot free monitors, a few premium clients have Pingdom, and several sites have no monitoring at all. This creates several problems: no unified dashboard to see all client statuses, no consistent alerting, and no client-facing status pages that look professional.

The agency's director of operations, Maria, wants to standardize on a single monitoring solution that can:
- Monitor all 35 client sites plus 20-30 critical services (payment processors, APIs, admin panels)
- Provide white-label status pages for each client (branded with client's domain, no mention of PixelCraft or the monitoring vendor)
- Send alerts to the agency's on-call rotation via Slack and SMS
- Allow selective access for clients to view their own status page and uptime reports
- Generate monthly uptime reports to include with client invoices

The challenge is budget. The agency can allocate $50-150/month for monitoring across all clients. They can't charge clients separately for monitoring (it's bundled into maintenance fees), so they need a solution that scales efficiently without breaking the bank.

## Requirements

### Must-Have
- **50-100 monitors** - 35 client main sites, 20-30 critical services, some clients have multiple properties
- **White-label status pages** - Each client gets their own branded status page (e.g., status.clientdomain.com)
- **Multi-user access** - 5 agency team members + selective client access
- **Client-specific notifications** - Route alerts to different Slack channels or people based on client
- **Monthly uptime reports** - Automated reports to prove SLA compliance
- **1-2 minute check intervals** - Balance between fast detection and cost
- **SMS alerts for critical clients** - Phone call or SMS for high-value clients

### Nice-to-Have
- **Multi-location checks** - Verify sites are up globally
- **API for automation** - Integrate with client onboarding workflow
- **Maintenance windows** - Suppress alerts during planned maintenance
- **Response time tracking** - Identify performance degradation
- **SSL certificate monitoring** - Prevent certificate expiry embarrassment
- **Team scheduling** - On-call rotation management
- **Branded email alerts** - Alerts from monitoring@pixelcraftdigital.com, not vendor

### Budget
$50-150/month (prefer lower end, but will pay more for critical features)

## Provider Analysis

### Provider 1: Better Uptime
**Score: 91/100**

**Fit Analysis:**
- 50-100 monitors: ✅ Team plan ($18/month) has 30 monitors; Company plan ($58/month) has 100 monitors
- White-label status pages: ✅ Custom domains supported on Team plan ($18/month)
- Multi-user access: ✅ Unlimited team members on all paid plans
- Client-specific notifications: ✅ Can create separate monitors with different alert policies
- Monthly uptime reports: ✅ Automated reports available
- 1-2 minute check intervals: ✅ 30-second checks on all paid plans (even better)
- SMS alerts: ✅ SMS alerts available on Team plan and up

**Pricing for This Use Case:**
$58/month (Company plan) - 100 monitors, unlimited team members, white-label status pages

Alternative: $18/month (Team plan) if they can stay under 30 monitors initially

**Strengths:**
- Best status page design in the industry (clients will be impressed)
- Unlimited custom domains for status pages (each client gets status.theirdomain.com)
- Incident management features (timeline, post-mortems) make the agency look professional
- Phone call alerts available on Company plan ($58/month)
- Can create separate "teams" for different clients with isolated alerts
- Beautiful, modern interface that won't embarrass them in client demos
- Public API for automating monitor creation during client onboarding
- Slack integration with granular routing
- Mobile apps for on-call team
- Maintenance windows included
- SSL monitoring built-in
- Response time tracking and SLA reporting
- Can add clients as "view-only" users to see their status
- On-call scheduling included
- Webhook support for custom integrations

**Gaps:**
- $58/month for 100 monitors is at the upper end of budget
- No email whitelabeling (emails come from Better Uptime)
- Cannot truly isolate clients from seeing agency name
- Relatively new company (founded 2021)
- No multi-location checks on lower tiers

**Score Breakdown:**
- Requirements coverage: 40/40 (all must-haves met perfectly)
- Pricing fit: 22/25 ($58/month is acceptable but at ceiling)
- Ease of setup: 15/15 (excellent UX, easy client onboarding)
- Feature richness: 10/10 (best-in-class features)
- Support quality: 4/10 (email support on Team/Company plans)

---

### Provider 2: StatusCake
**Score: 87/100**

**Fit Analysis:**
- 50-100 monitors: ✅ Business plan ($74.99/month) has unlimited uptime tests
- White-label status pages: ✅ White-label public reporting on Business plan
- Multi-user access: ✅ Up to 50 users on Business plan
- Client-specific notifications: ✅ Contact groups allow per-client routing
- Monthly uptime reports: ✅ Automated reporting available
- 1-2 minute check intervals: ✅ 1-minute intervals on Business plan
- SMS alerts: ✅ SMS alerts included on Business plan

**Pricing for This Use Case:**
$74.99/month (Business plan) - Unlimited uptime tests, 50 users, white-label status pages

**Strengths:**
- Unlimited uptime tests (no worrying about monitor count)
- True white-label status pages (no vendor branding)
- 50 users included (can give all clients access)
- Contact groups make client-specific alerting easy
- SMS alerts included without extra cost
- Phone call alerts available
- Multi-location checks from 30+ global locations
- Virus scanning (unique feature, good for client security)
- Domain monitoring (WHOIS/DNS expiry alerts)
- Page speed monitoring
- SSL monitoring
- API for automation
- Maintenance windows
- Generous features for the price
- Long-established company (2012)

**Gaps:**
- Interface feels dated and cluttered
- Status pages look basic compared to Better Uptime
- $74.99/month is toward upper budget limit
- No modern incident management features
- Mobile apps exist but aren't great
- Documentation could be better
- No on-call scheduling built-in

**Score Breakdown:**
- Requirements coverage: 40/40 (all must-haves met)
- Pricing fit: 20/25 ($75/month is acceptable but high)
- Ease of setup: 11/15 (confusing UI, but powerful once learned)
- Feature richness: 9/10 (unique features like virus scanning)
- Support quality: 7/10 (email/phone support on Business plan)

---

### Provider 3: UptimeRobot
**Score: 82/100**

**Fit Analysis:**
- 50-100 monitors: ✅ Pro plan ($7/month per 50 monitors) - need $14/month for 100 monitors
- White-label status pages: ⚠️ Custom CNAME on Pro plan, but still shows "Powered by UptimeRobot" unless Business plan ($29/month per 50 monitors)
- Multi-user access: ⚠️ Limited sub-accounts on Pro plan; better on Business plan
- Client-specific notifications: ✅ Alert contacts can be configured per monitor
- Monthly uptime reports: ✅ Can export uptime data
- 1-2 minute check intervals: ✅ 1-minute intervals on Pro plan
- SMS alerts: ❌ SMS alerts require Business plan at $29/month per 50 monitors ($58/month for 100 monitors)

**Pricing for This Use Case:**
$14/month (Pro plan, 100 monitors) - Good but limited white-labeling
OR $58/month (Business plan, 100 monitors) - True white-label and SMS alerts

**Strengths:**
- Most affordable at lower tier ($14/month for 100 monitors)
- Extremely reliable service (industry standard since 2010)
- Simple, straightforward interface
- Good API for automation
- Maintenance windows available
- Alert contacts can be configured per monitor (good for client-specific routing)
- SSL monitoring included
- Response time tracking
- Can export data for custom reports
- Very stable service

**Gaps:**
- True white-labeling requires expensive Business plan ($58/month)
- Status pages look dated
- No modern incident management features
- SMS alerts only on Business plan
- Multi-user access limited on Pro plan
- No on-call scheduling
- Single check location unless Business plan
- Interface hasn't evolved much over the years

**Score Breakdown:**
- Requirements coverage: 32/40 (Pro plan misses white-label and SMS; Business plan too expensive for value)
- Pricing fit: 24/25 (Pro plan $14/month is excellent; Business plan $58/month acceptable)
- Ease of setup: 14/15 (very easy)
- Feature richness: 6/10 (solid basics, lacks modern features)
- Support quality: 6/10 (email support on paid plans)

---

### Provider 4: Oh Dear
**Score: 78/100**

**Fit Analysis:**
- 50-100 monitors: ⚠️ Team plan ($79/month) has 30 sites; Business plan ($199/month) has 100 sites
- White-label status pages: ✅ Custom domains for status pages included
- Multi-user access: ✅ Unlimited team members
- Client-specific notifications: ✅ Can configure alerts per site
- Monthly uptime reports: ✅ Excellent reporting features
- 1-2 minute check intervals: ✅ 1-minute intervals included
- SMS alerts: ⚠️ No SMS built-in; uses third-party integrations

**Pricing for This Use Case:**
$79/month (Team plan, 30 sites) - Too few monitors
OR $199/month (Business plan, 100 sites) - Over budget

**Strengths:**
- Beautiful, developer-focused interface
- Broken link checking (great for agency clients)
- Mixed content detection
- Certificate health monitoring
- DNS monitoring
- Cron job monitoring
- Application health checks
- Excellent API and webhook system
- Well-documented
- Created by respected Laravel developers
- Great status pages
- Maintenance windows
- Performance monitoring

**Gaps:**
- Expensive ($79/month for only 30 sites, $199/month for 100 sites)
- $199/month is way over budget
- No built-in SMS alerts
- Smaller company, less proven at scale
- Features like broken link checking not critical for agency use case
- Overkill for simple uptime monitoring

**Score Breakdown:**
- Requirements coverage: 35/40 (meets most, but SMS requires workarounds)
- Pricing fit: 10/25 ($199/month is over budget; $79/month too few monitors)
- Ease of setup: 15/15 (excellent UX)
- Feature richness: 10/10 (comprehensive features)
- Support quality: 8/10 (good email support)

---

### Provider 5: Uptime.com
**Score: 75/100**

**Fit Analysis:**
- 50-100 monitors: ✅ Experience plan ($15/month) has 5 monitors; need custom pricing for 100
- White-label status pages: ✅ Custom domains supported
- Multi-user access: ✅ Multiple users supported
- Client-specific notifications: ✅ Advanced alert rules
- Monthly uptime reports: ✅ Excellent SLA reporting
- 1-2 minute check intervals: ✅ 1-minute intervals available
- SMS alerts: ✅ SMS alerts available

**Pricing for This Use Case:**
~$150-200/month (estimated for 100 monitors based on custom pricing)

**Strengths:**
- Enterprise-grade features
- RUM (Real User Monitoring) included
- API monitoring with complex checks
- Transaction monitoring
- Infrastructure monitoring
- Advanced alerting with escalation policies
- Excellent SLA reporting (perfect for client invoices)
- Multi-location checks from global network
- Status pages with incident management
- Integrations with PagerDuty, Slack, etc.
- Strong support

**Gaps:**
- Expensive (likely $150-200/month for 100 monitors)
- Overkill for WordPress site monitoring
- Complex interface may overwhelm agency team
- Enterprise-focused, not ideal for small agency
- Pricing not transparent (requires sales call)

**Score Breakdown:**
- Requirements coverage: 40/40 (enterprise features meet all requirements)
- Pricing fit: 15/25 (likely at or over budget ceiling)
- Ease of setup: 11/15 (complex, requires learning)
- Feature richness: 10/10 (comprehensive)
- Support quality: 9/10 (excellent support but requires enterprise spend)

---

### Provider 6: Site24x7
**Score: 80/100**

**Fit Analysis:**
- 50-100 monitors: ✅ Starter plan ($9/month per 10 monitors) - $90/month for 100 monitors
- White-label status pages: ⚠️ Public status pages available but limited white-labeling
- Multi-user access: ✅ Multiple users supported
- Client-specific notifications: ✅ User groups and alert profiles
- Monthly uptime reports: ✅ Comprehensive reporting
- 1-2 minute check intervals: ✅ 1-minute intervals included
- SMS alerts: ✅ SMS alerts available

**Pricing for This Use Case:**
$90/month (Starter plan, 100 monitors via 10 monitor packs)

**Strengths:**
- Part of comprehensive monitoring suite (can add server monitoring later)
- $90/month for 100 monitors is mid-range
- SMS alerts included
- Multi-location monitoring
- Performance monitoring
- Transaction monitoring
- API for automation
- Mobile apps
- Good alerting with escalation
- Maintenance windows
- SSL monitoring
- Integration with 100+ third-party tools
- Established company (ManageEngine/Zoho)

**Gaps:**
- Status page white-labeling is limited
- Interface is cluttered (tries to do everything)
- Overkill features for simple uptime monitoring
- Status pages not as polished as Better Uptime
- $90/month is mid-upper budget range

**Score Breakdown:**
- Requirements coverage: 37/40 (white-label status pages limited)
- Pricing fit: 19/25 ($90/month acceptable but not ideal)
- Ease of setup: 10/15 (complex interface)
- Feature richness: 10/10 (comprehensive suite)
- Support quality: 4/10 (email support on Starter plan)

---

### Provider 7: Pingdom
**Score: 70/100**

**Fit Analysis:**
- 50-100 monitors: ⚠️ Advanced plan ($53/month) has 100 checks
- White-label status pages: ⚠️ Custom domains but limited white-labeling
- Multi-user access: ✅ Multiple users supported
- Client-specific notifications: ✅ Alert policies per monitor
- Monthly uptime reports: ✅ Excellent reporting
- 1-2 minute check intervals: ✅ 1-minute intervals
- SMS alerts: ✅ SMS alerts available

**Pricing for This Use Case:**
$53/month (Advanced plan, 100 checks)

**Strengths:**
- Industry leader with excellent reputation
- 100 checks on Advanced plan
- Beautiful, polished interface
- Transaction monitoring
- Root cause analysis
- Real User Monitoring (RUM) available on higher tiers
- Mobile apps
- Multi-location checks
- Good API
- Excellent uptime reports
- Trusted brand name

**Gaps:**
- $53/month for 100 checks is mid-range (Better Uptime is $58 with better features)
- Status page white-labeling limited
- Many advanced features require higher tiers ($115/month+)
- Not optimized for agency multi-tenant use case
- Status pages not as modern as Better Uptime

**Score Breakdown:**
- Requirements coverage: 37/40 (meets most requirements)
- Pricing fit: 21/25 ($53/month acceptable)
- Ease of setup: 14/15 (easy, polished)
- Feature richness: 9/10 (excellent)
- Support quality: 9/10 (good support on paid plans)

## Comparison Matrix

| Provider | Score | Monthly Cost | Monitors | White-Label | SMS Alerts | Status Page Quality | Best For |
|----------|-------|--------------|----------|-------------|------------|---------------------|----------|
| Better Uptime | 91/100 | $58 | 100 | ✅ Full | ✅ Yes | ⭐⭐⭐⭐⭐ | Agencies wanting best client UX |
| StatusCake | 87/100 | $75 | Unlimited | ✅ Full | ✅ Yes | ⭐⭐⭐ | Agencies needing unlimited monitors |
| UptimeRobot | 82/100 | $14 (limited) or $58 (full) | 100 | ⚠️ Limited / ✅ Full | ❌ / ✅ | ⭐⭐⭐ | Budget-conscious agencies |
| Site24x7 | 80/100 | $90 | 100 | ⚠️ Limited | ✅ Yes | ⭐⭐⭐ | Agencies needing server monitoring too |
| Oh Dear | 78/100 | $199 | 100 | ✅ Full | ⚠️ Via integration | ⭐⭐⭐⭐ | Developer-focused agencies |
| Uptime.com | 75/100 | ~$150-200 | 100 | ✅ Full | ✅ Yes | ⭐⭐⭐⭐ | Enterprise agencies |
| Pingdom | 70/100 | $53 | 100 | ⚠️ Limited | ✅ Yes | ⭐⭐⭐⭐ | Agencies wanting brand name |

## Recommendation

**Winner: Better Uptime at $58/month (91/100)**

**Why:**

Better Uptime is the perfect fit for PixelCraft Digital's agency model for three critical reasons. First, the status pages are so beautifully designed that they actually enhance client perception. When a client sees their status page at status.clientdomain.com, they're impressed by the modern, professional interface - many assume the agency built it custom. This perceived quality justifies the agency's premium maintenance fees and positions PixelCraft as a sophisticated technical partner.

Second, the incident management features make the agency look exceptionally professional during outages. When a client site goes down, PixelCraft can post incident updates with timestamps, tag the issue as "Investigating," "Identified," "Monitoring," and "Resolved," and automatically generate a post-mortem. This level of transparency and communication is what clients expect from a $2,000/month maintenance contract. Better Uptime makes this workflow effortless.

Third, the pricing structure scales perfectly with the agency's growth. At $58/month for 100 monitors, PixelCraft pays $0.58 per monitor. They can include this cost in their standard maintenance fees ($500-3,000/month per client), making the monitoring effectively free from a margin perspective. If they grow beyond 100 monitors, they can negotiate custom pricing or carefully manage which endpoints truly need monitoring.

The 30-second check intervals mean the on-call engineer gets alerted within 30-60 seconds of downtime, not 5-10 minutes. For a client's e-commerce site processing transactions, this faster detection could prevent thousands in lost revenue and save the client relationship. The $58/month investment pays for itself if it prevents even one client churn ($500-3,000/month MRR loss).

The unlimited team members feature is crucial for an agency. PixelCraft can add all 5 operations staff, plus grant view-only access to clients who want to see their own uptime metrics. This transparency builds trust and reduces "is my site down?" support tickets.

**Alternative:**

**StatusCake at $74.99/month** (87/100) is a strong alternative if unlimited monitors is more important than beautiful status pages. At $75/month, PixelCraft gets unlimited uptime tests, which means they never have to worry about hitting monitor limits as they onboard new clients or add more services.

Choose StatusCake if:
- You expect to grow beyond 100 monitors quickly (each new client adds 2-3 monitors on average)
- You prioritize full white-labeling (StatusCake's white-label is more complete)
- You want the virus scanning feature for client security reports
- You prefer phone support (StatusCake includes this on Business plan)
- You don't care as much about status page aesthetics

However, the $17/month extra cost ($75 vs $58) is significant over a year ($204/year), and the status page quality difference is substantial. Better Uptime's status pages look modern and professional, while StatusCake's look functional but dated. Since clients will see these status pages, the visual quality matters for agency brand perception.

**Budget Consideration:**

If $58/month is still too high, consider starting with **UptimeRobot Pro at $14/month** for 100 monitors. This gets basic monitoring in place for all clients at a very low cost. The status pages won't be fully white-labeled (they'll show "Powered by UptimeRobot"), and there's no SMS alerts, but it's functional monitoring that covers the core need.

Then, upgrade to Better Uptime when:
- The agency lands a major client who demands professional status pages
- They lose a client due to monitoring gaps and realize the cost of Better Uptime is less than one lost client
- They raise prices and can absorb the $58/month cost
- They reach $200K+ annual revenue and $58/month becomes negligible

**Implementation Notes:**

1. **Monitor Organization Strategy:**
   - Create one monitor per client's main site (35 monitors)
   - Add monitors for critical client services: payment processors, booking systems, APIs (20-30 monitors)
   - Add monitors for agency infrastructure: main website, client portal, project management tool (5 monitors)
   - Total: 60-70 monitors (comfortably under 100 limit)

2. **Status Page Setup Per Client:**
   - During client onboarding, create a status page: status.clientdomain.com
   - Add CNAME DNS record: status.clientdomain.com → statuspage.betteruptime.com
   - Customize status page with client's logo and brand colors
   - Include only client-relevant monitors (don't show other clients)
   - Enable subscriber notifications so client stakeholders can get alerts

3. **Alert Routing Strategy:**
   - Create Slack channel #client-alerts-critical for high-value clients
   - Create Slack channel #client-alerts-standard for regular clients
   - Configure phone call alerts for top 5 clients (e-commerce, high revenue)
   - Set up escalation: Slack alert → wait 5 min → SMS to on-call → wait 10 min → phone call
   - Use Better Uptime's on-call scheduling to rotate who gets alerted

4. **Client Access Management:**
   - Add clients as "Stakeholder" role (view-only access to their monitors)
   - Don't give clients edit access to monitors
   - Clients can view uptime reports and incident history
   - This transparency reduces "is my site down?" support tickets

5. **Monthly Reporting Workflow:**
   - Use Better Uptime's API to pull monthly uptime data for each client
   - Create automated report template: "Client XYZ - 99.94% uptime in September"
   - Include this in monthly invoice: "Uptime SLA: 99.0% guaranteed / 99.94% achieved"
   - Proves value of maintenance contract

6. **Client Onboarding Automation:**
   - Use Better Uptime's API to automate monitor creation
   - When new client signs contract, script creates:
     - Monitor for client's main site
     - Status page at status.clientdomain.com
     - Alert policy routing to appropriate Slack channel
   - Reduces manual setup from 30 minutes to 5 minutes per client

7. **Maintenance Windows:**
   - Before deploying client site updates, enable maintenance window in Better Uptime
   - Suppresses alerts during planned downtime
   - Status page shows "Under Maintenance" instead of "Down"
   - Clients see professional maintenance communication

8. **Team Training:**
   - Train all 5 operations staff on Better Uptime interface
   - Document standard operating procedures:
     - How to acknowledge an incident
     - How to post status page updates
     - How to generate uptime reports
     - Who is on-call this week
   - Create runbook for common incidents (WordPress down, SSL expired, DNS issues)

9. **Cost Recovery:**
   - Calculate: $58/month ÷ 35 clients = $1.66 per client per month
   - Include monitoring cost in maintenance fees (clients never see this line item)
   - Position as "24/7 uptime monitoring with status page" in sales materials
   - Use it as differentiator against competitors who don't offer monitoring

10. **Future Scaling:**
    - If you grow beyond 100 monitors, consider:
      - Consolidating monitors (do you really need to monitor /admin separate from main site?)
      - Removing monitors for low-value clients (controversial but pragmatic)
      - Negotiating custom pricing with Better Uptime for agencies
      - Raising maintenance fees to cover higher monitoring costs
