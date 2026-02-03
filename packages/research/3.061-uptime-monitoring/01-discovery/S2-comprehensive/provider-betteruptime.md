# Better Uptime (Better Stack)

## Overview

Better Uptime is part of the Better Stack ecosystem, a modern observability platform launched in 2019 that combines uptime monitoring, incident management, on-call scheduling, and status pages into a unified solution. Unlike legacy monitoring tools built for sysadmins, Better Stack is designed for modern DevOps teams who expect seamless integrations, beautiful UX, and developer-friendly workflows.

The platform has rapidly gained traction in the developer community due to its all-in-one approach to incident response. Rather than purchasing separate tools for monitoring (UptimeRobot), on-call (PagerDuty), and status pages (StatusPage.io), teams can consolidate these capabilities under Better Stack's unified pricing model. This bundling strategy appeals to startups and scale-ups seeking to reduce tool sprawl and vendor complexity.

Better Uptime targets modern engineering teams (5-50 developers) who value design, user experience, and efficient incident workflows. The platform is particularly popular among SaaS companies, API-first businesses, and remote-first teams requiring robust on-call rotation and escalation policies. Better Stack competes directly with PagerDuty, Opsgenie, and Incident.io while offering uptime monitoring as a core feature rather than an add-on.

## Pricing

### Free Tier
- **Monitors:** 10 HTTP/HTTPS monitors
- **Check interval:** 3 minutes
- **Alert channels:** Email, webhooks, Slack
- **Status page:** 5 public status pages (generous for free tier)
- **Retention:** Not explicitly stated (assumed 30 days)
- **On-call scheduling:** Not included
- **Incident management:** Basic incident tracking
- **Heartbeat monitors:** 3 heartbeat monitors
- **Phone/SMS alerts:** Not included
- **Team members:** 1 user

### Paid Tiers

**Starter Plan - $29/month per responder (billed annually at $25/month)**
- Includes 1 responder license
- Unlimited phone call and SMS alerts (globally)
- 50 monitors included (add 50 monitors for $21/month)
- 1-minute check intervals
- Unlimited status pages
- Advanced on-call scheduling
- Incident management and timeline
- Escalation policies
- Slack, Teams, email integrations
- 30-day incident retention

**Team Plan - Custom pricing (estimated $100-300/month)**
- Multiple responder licenses ($29/month each)
- Higher monitor limits (negotiate bundles)
- Advanced team features (RBAC, SSO)
- Extended retention (90+ days)
- Priority support
- Custom integrations

**Enterprise Plan - Custom pricing**
- Unlimited responders
- Unlimited monitors
- Custom check intervals (as low as 30 seconds)
- Advanced security (SAML SSO, audit logs)
- 99.9% SLA guarantee
- Dedicated account manager
- Custom contracts and invoicing

**Add-ons:**
- Additional 50 monitors: $21/month
- Additional responder seats: $29/month
- Better Stack Logs (log management): Starting at $25/month
- Better Stack Traces (APM): Custom pricing

## Features

### Core Monitoring

**HTTP/HTTPS Monitoring**
- URL availability checks with custom headers
- TLS/SSL certificate monitoring with expiry alerts
- Keyword validation (check for specific text in responses)
- Response time tracking with P50, P95, P99 percentiles
- Custom timeout settings (1-30 seconds)

**Heartbeat Monitoring**
- Passive cron job and scheduled task monitoring
- Configurable expected intervals (hourly, daily, weekly)
- Grace periods before alerting
- Perfect for backup jobs, ETL pipelines, serverless functions

**API Endpoint Monitoring**
- RESTful API health checks
- JSON response validation
- Custom HTTP methods (GET, POST, PUT, DELETE)
- Authentication support (Bearer tokens, Basic Auth)

**Multi-Step Transaction Checks**
- Browser-based checks (Playwright integration)
- Multi-page user journey monitoring
- Form submission and e-commerce flow validation
- Available on higher-tier plans

**Global Monitoring Locations**
- 20+ monitoring locations worldwide
- US (East, West, Central), EU (London, Frankfurt, Paris), APAC (Singapore, Tokyo, Sydney)
- Configurable location selection per monitor
- Consensus-based alerting (alert only if multiple locations fail)

### Alerting

**Email Alerts**
- Unlimited email notifications
- Rich HTML incident summaries
- Automatic escalation emails
- Digest notifications (daily/weekly uptime summaries)

**SMS and Phone Call Alerts**
- **Unlimited SMS and phone calls included** on Starter plan (major differentiator)
- Global coverage (190+ countries)
- Text-to-speech incident details
- Automatic failover (if SMS fails, try phone call)

**Integration Alerts**
- Slack (rich message formatting with action buttons)
- Microsoft Teams
- Discord webhooks
- Telegram
- Custom webhooks (JSON payloads with full incident context)

**On-Call Management**
- PagerDuty-style on-call schedules
- Rotation management (daily, weekly, custom shifts)
- Override shifts (swap on-call person temporarily)
- Escalation policies (primary → secondary → manager after X minutes)
- Calendar integrations (sync on-call schedules to Google Calendar, Outlook)

**Incident Management**
- Automatic incident creation from monitor failures
- Manual incident creation for non-automated issues
- Incident timeline (who was notified, when, response times)
- Incident acknowledgment and resolution tracking
- Postmortem templates
- Slack-based incident commands (/resolve, /acknowledge)

### Status Pages

**Public Status Pages**
- 5 free status pages (best in class for free tier)
- Unlimited status pages on paid plans
- Custom domain support (status.yourcompany.com)
- White-labeled (no Better Stack branding on paid plans)
- Real-time monitor status display
- Historical uptime graphs (30d, 90d)

**Status Page Features**
- Subscriber notifications (email, SMS, RSS)
- Scheduled maintenance announcements
- Incident updates and timeline
- Multi-language support
- Custom CSS styling
- Embed widgets for your main site
- Private status pages (password-protected)

**Incident Communication**
- Create incidents directly from status page
- Real-time updates to subscribers
- Automatic notifications on state changes
- Postmortem publishing

### Advanced Features

**Response Time Analytics**
- P50, P95, P99 response time percentiles
- Historical response time graphs
- Performance degradation alerts (alert if response time > X ms)
- Export data via API

**Uptime SLA Reporting**
- Automatic uptime percentage calculation
- Custom SLA thresholds (99.9%, 99.95%, 99.99%)
- SLA breach notifications
- Historical SLA reports (30d, 90d, 365d)

**API Access**
- Comprehensive REST API
- Create/update/delete monitors
- Manage on-call schedules programmatically
- Retrieve incident history
- Webhook support for real-time events
- Terraform provider (official)

**Maintenance Windows**
- Schedule maintenance periods to suppress alerts
- Recurring maintenance schedules
- Automatic status page updates during maintenance
- Subscriber notifications for planned downtime

**Third-Party Integrations**
- PagerDuty (two-way sync)
- Opsgenie integration
- Jira (create tickets from incidents)
- Datadog (forward metrics)
- GitHub (link incidents to commits)
- Zapier (workflow automation)

**Better Stack Ecosystem**
- Better Stack Logs (centralized log management)
- Better Stack Traces (APM and distributed tracing)
- Unified observability dashboard
- Cross-product correlations (link logs → incidents → traces)

## Strengths

- **Unlimited SMS/phone alerts on paid plans:** Industry-leading value; competitors charge per SMS while Better Stack includes unlimited global alerts, potentially saving $50-200/month for on-call teams
- **Beautiful, modern UX:** Developer-centric interface with intuitive workflows; incident timelines, on-call schedules, and status pages have best-in-class design
- **All-in-one incident response platform:** Combines uptime monitoring, on-call management, incident tracking, and status pages in one tool, reducing vendor fatigue and integration complexity
- **Generous free tier for status pages:** 5 free status pages vs. competitors' 1-2, making it ideal for agencies managing multiple client sites
- **Rapid feature development:** Active product team shipping new features monthly; responsive to community feedback on roadmap priorities

## Weaknesses

- **3-minute intervals on free tier:** Slower than Freshping's 1-minute free checks; free tier insufficient for production SLAs
- **Per-responder pricing can escalate:** $29/month per on-call user adds up quickly for larger teams; a 10-person team costs $290/month before monitor add-ons
- **Limited browser checks on lower tiers:** Advanced multi-step transaction monitoring requires custom enterprise pricing; competitors like Checkly offer Playwright checks at lower price points
- **Shorter data retention:** 30-day default retention vs. UptimeRobot's 12-24 months on paid tiers; long-term SLA analysis requires upgrades or exports
- **Smaller monitoring location network:** 20+ locations vs. Pingdom's 100+ or Site24x7's 130+; may miss regional outages in less-covered geographies

## Best For

Better Uptime is the ideal solution for modern SaaS companies and API-driven businesses with on-call engineering teams (5-20 developers) who need unified incident response capabilities. Teams currently using PagerDuty for on-call plus separate uptime monitoring tools can consolidate to Better Stack and save 30-50% while gaining a superior user experience. The unlimited SMS/phone alert model makes it particularly valuable for high-frequency alerting scenarios. Best suited for companies prioritizing developer experience, incident response speed, and beautiful customer-facing status pages over raw monitoring location count or ultra-long data retention.

---

**Last Updated:** January 2025
**Pricing Source:** betterstack.com/pricing (verified January 2025)
