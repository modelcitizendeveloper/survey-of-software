# Checkly

## Overview

Checkly is a modern, developer-centric synthetic monitoring platform founded in 2018, designed for teams practicing Monitoring as Code (MaC) workflows. Unlike traditional monitoring tools built for operations teams using web UIs, Checkly embraces infrastructure-as-code principles, allowing developers to define monitors as JavaScript/TypeScript code, version them in Git, and deploy via CI/CD pipelines. The platform is powered by Playwright, the leading browser automation framework, enabling sophisticated multi-step user journey testing with the same code developers use for end-to-end testing.

Checkly has carved out a niche as the "GitHub for monitoring" by prioritizing developer experience over feature breadth. The company targets DevOps-mature organizations practicing continuous deployment, infrastructure as code, and test-driven development. Checkly's unique positioning appeals to engineering teams frustrated by legacy monitoring tools requiring manual UI configuration and lacking version control, code review, and automated deployment capabilities.

The target audience includes software engineers, SRE teams, and platform engineers at tech-forward startups and scale-ups (10-200 engineers) building modern web applications, APIs, and microservices. Checkly is particularly popular in the Next.js, React, Node.js, and serverless ecosystems. The platform competes with Datadog Synthetics and New Relic Synthetics on technical capabilities while undercutting on price, and differentiates from UptimeRobot/StatusCake through code-first workflows and advanced browser testing.

## Pricing

### Free Tier (Permanent)
- **Uptime monitors:** 10 HTTP/HTTPS checks
- **API checks:** Included in uptime monitors
- **Browser checks:** 150 browser check runs/month (limited)
- **Check interval:** Configurable down to 10 minutes
- **Monitoring locations:** 4 locations (US East, US West, EU West, APAC)
- **Retries:** Configurable retry logic
- **Alerting:** Email, Slack, webhooks
- **API access:** Full API and CLI access
- **Monitoring as Code:** Full support (Terraform, CLI, SDK)
- **Data retention:** 30 days
- **Team members:** 1 user
- **No credit card required**

### Paid Tiers

**Starter Plan - $24/month (billed annually, $29/month monthly)**
- 20 uptime monitors
- 5,000 API check runs/month
- 1,000 browser check runs/month
- Check intervals down to 10 seconds (on request, typically 1-minute)
- 10 monitoring locations (global coverage)
- Advanced Playwright browser checks
- Multi-step API testing
- Unlimited alerting channels
- 3 team members
- Maintenance windows
- 90-day data retention
- Terraform provider
- Monitoring as Code workflows

**Team Plan - $199/month (billed annually, $239/month monthly)**
- 100 uptime monitors
- 50,000 API check runs/month
- 10,000 browser check runs/month
- Check intervals down to 10 seconds
- 22 monitoring locations (comprehensive global coverage)
- Private locations (self-hosted agents)
- Advanced browser checks with traces and screenshots
- Multi-step API workflows with variables
- 10 team members
- SSO/SAML (Enterprise add-on)
- 180-day data retention
- Priority support
- Custom integrations

**Enterprise Plan - Custom pricing (estimated $500-2000+/month)**
- Unlimited monitors (negotiable)
- Custom check run allocations (100K+ API, 20K+ browser)
- Check intervals down to 10 seconds or faster
- Private locations included
- Unlimited team members
- SSO/SAML, audit logs
- 365+ day data retention
- Dedicated support and SLA
- Custom contract terms
- White-glove onboarding

**Usage-Based Overage Pricing:**
- Additional API check runs: $0.80 per 10,000 runs
- Additional browser check runs: $8 per 1,000 runs
- Private locations: $90 per location per month

## Features

### Core Monitoring

**Uptime Monitoring (HTTP/HTTPS)**
- Simple URL availability checks
- Response time measurement
- HTTP status code validation
- Custom headers and authentication
- POST/PUT/DELETE methods
- SSL certificate validation and expiry alerts
- Redirect following or failure
- Timeout configuration

**API Checks**
- Advanced HTTP request testing
- RESTful API endpoint monitoring
- GraphQL API testing
- Multi-step API workflows (chain requests, extract variables)
- JSON/XML response validation (JSONPath, XPath assertions)
- JavaScript-based assertions (full programming power)
- Authentication: OAuth, JWT, API keys, Basic Auth
- Environment variables and secrets management
- Request/response body inspection

**Browser Checks (Playwright-Powered)**
- **Key Differentiator:** Full Playwright framework support
- JavaScript/TypeScript check definitions
- Multi-page user journey testing
- Login flows, checkout sequences, form submissions
- Complex interactions (drag-drop, file uploads, hover states)
- Screenshot capture on failure
- Video recording (Enterprise)
- Network request interception and mocking
- Mobile device emulation (iPhone, Android)
- Performance metrics (page load, resource timing)
- Core Web Vitals (LCP, FID, CLS)

**Heartbeat/Cron Monitoring**
- Passive monitoring expecting regular check-ins
- Ideal for scheduled jobs, backups, webhooks
- Configurable expected intervals
- Grace periods before alerting

### Alerting

**Email Alerts**
- Unlimited email notifications
- Customizable templates
- Incident summaries with check run details
- Digest reports

**Slack Integration**
- Rich message formatting
- Interactive buttons (acknowledge, resolve)
- Channel-based routing
- @mention escalation

**Webhook Alerts**
- Custom JSON/XML payloads
- Full check run context
- Retry logic and failure handling
- Perfect for custom integrations

**Third-Party Integrations**
- PagerDuty (bi-directional sync)
- Opsgenie
- Discord, Microsoft Teams
- Telegram
- SMS via Twilio (custom webhook)
- Email-to-SMS gateways

**Alert Configuration**
- Configurable failure thresholds (alert after N failures)
- Multi-location consensus (alert if X of Y locations fail)
- Escalation delays (wait 5 min, then escalate)
- Maintenance windows (suppress alerts during deployments)
- Alert rate limiting
- Custom alert grouping

### Status Pages

**No native status page functionality.** Checkly focuses on monitoring and alerting; customers use third-party status page providers (Better Uptime, StatusPage.io) or build custom pages using Checkly's API.

**Workarounds:**
- Embed Checkly badges on custom status pages
- Use Checkly API to power status pages
- Integrate with Better Uptime for status page + Checkly monitoring

### Advanced Features

**Monitoring as Code (MaC) - Core Differentiator**
- Define monitors in JavaScript/TypeScript
- Version control checks in Git
- Code review via pull requests
- Automated deployment via CI/CD
- Checkly CLI for local testing and deployment
- Terraform provider (official, comprehensive)
- SDK for programmatic monitor management

**Global Monitoring Locations**
- Free: 4 locations (US East, US West, EU West, APAC)
- Starter: 10 locations
- Team: 22 locations (US, EU, APAC, South America)
- Enterprise: Custom locations
- Private locations (self-hosted agents for internal monitoring)
- Configurable location selection per check
- Consensus alerting

**CI/CD Integration**
- Run checks in GitHub Actions, GitLab CI, CircleCI
- Pre-deployment smoke tests
- Post-deployment verification
- Block deployments on check failures
- Checkly CLI for pipeline integration

**Performance Monitoring**
- Response time tracking (DNS, TCP, SSL, TTFB, total)
- Browser performance metrics (Lighthouse-based)
- Resource timing (JavaScript, CSS, images)
- Core Web Vitals
- Historical performance trends
- P50, P95, P99 percentiles

**API Access**
- Comprehensive REST API
- Create, update, delete checks programmatically
- Retrieve check run results and metrics
- Manage alert channels and integrations
- Webhook support for real-time events
- Rate limits based on plan tier

**Private Locations**
- Deploy Checkly agents in your infrastructure
- Monitor internal services, staging environments
- Docker container or Kubernetes deployment
- Available on Team and Enterprise plans
- Pricing: $90 per private location per month

**Maintenance Windows**
- Schedule maintenance periods via API/UI
- Suppress alerts during deployments
- Recurring maintenance schedules
- Integration with deployment pipelines

**Environment Management**
- Separate environments (dev, staging, production)
- Environment-specific variables and secrets
- Promote checks across environments
- Perfect for testing before production deployment

**Advanced Reporting**
- Custom dashboards
- SLA reporting (uptime percentage over time)
- Export data (CSV, JSON via API)
- Embed check results in external dashboards

## Strengths

- **Best-in-class Monitoring as Code:** Checkly is the only uptime tool built natively for infrastructure-as-code workflows; Git-based versioning, code review, and CI/CD deployment are first-class features
- **Full Playwright framework support:** Browser checks use real Playwright code, enabling sophisticated testing scenarios impossible in UI-driven tools; developers reuse existing E2E test skills
- **Developer-centric UX:** Clean, modern interface designed for engineers; minimal learning curve for developers familiar with JavaScript, Git, and CI/CD
- **Competitive pricing for API/browser checks:** 5-10x cheaper than Datadog Synthetics for equivalent check volumes; $24/month Starter plan excellent value for small teams
- **Active community and rapid feature development:** Responsive product team, strong documentation, and growing ecosystem of integrations and examples

## Weaknesses

- **No native status pages:** Unlike Better Uptime and UptimeRobot, Checkly doesn't include public status page functionality; requires third-party integration or custom development
- **Steeper learning curve for non-developers:** Monitoring as Code workflows assume JavaScript/Git proficiency; operations teams preferring UI-driven configuration may struggle
- **Limited free tier check runs:** 150 browser check runs/month depletes quickly with frequent testing; free tier best for evaluation, not production use
- **Smaller location network than enterprise tools:** 22 locations on Team plan vs. Pingdom's 100+; adequate for most use cases but less geographic coverage than enterprise alternatives
- **Usage-based pricing can surprise:** API/browser check run quotas require monitoring usage; overages at $0.80-8 per additional runs can add unexpected costs during high-frequency testing periods

## Best For

Checkly excels as the monitoring solution for engineering teams (5-50 developers) practicing DevOps, infrastructure as code, and continuous deployment. Perfect for organizations building modern web applications with React, Next.js, Vue, or Angular requiring sophisticated browser testing beyond simple uptime checks. Teams frustrated by legacy monitoring tools lacking version control, code review, and automated deployment will find Checkly transformative. Particularly valuable for API-driven businesses and microservices architectures needing multi-step API testing with variable extraction. Best suited for tech-forward startups and scale-ups prioritizing developer experience; less ideal for non-technical teams or organizations requiring native status page capabilities.

---

**Last Updated:** January 2025
**Pricing Source:** checklyhq.com/pricing (verified January 2025)
