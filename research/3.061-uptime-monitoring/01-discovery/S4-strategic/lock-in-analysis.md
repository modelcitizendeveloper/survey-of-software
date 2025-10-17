# Lock-In Analysis - Uptime Monitoring Services

## Executive Summary

Lock-in analysis evaluates the difficulty and cost of migrating away from an uptime monitoring provider. Unlike commodity services where switching is trivial, monitoring services create operational dependencies through historical data, alert configurations, integrations, and customer-facing status pages.

**Key Findings:**
- **Lowest Lock-In**: Upptime (1-2 hours), Uptime Kuma (2-4 hours) - open source, config as code
- **Low Lock-In**: UptimeRobot (4-8 hours for 50 monitors) - excellent API, simple config
- **Moderate Lock-In**: Freshping (8-12 hours), StatusCake (10-15 hours) - partial API coverage
- **High Lock-In**: Checkly (15-25 hours) - Monitoring-as-Code, complex migrations
- **Severe Lock-In**: Pingdom (20-40 hours) - poor data export, SolarWinds complexity

## Lock-In Dimensions

### 1. Historical Data Portability

**Critical Questions:**
- Can you export uptime history in machine-readable format (CSV, JSON)?
- How far back does the export go (30 days, 1 year, lifetime)?
- Is historical data accessible via API or manual export only?
- What granularity is preserved (1-minute, 5-minute, hourly aggregates)?

**Business Impact:**
- SLA compliance reporting requires historical uptime percentages
- Trend analysis for capacity planning
- Incident post-mortems reference historical patterns
- Regulatory compliance (SOC 2, HIPAA) may require N years of monitoring data

### 2. Configuration Migration

**Components:**
- Monitor definitions (URLs, check intervals, check types)
- Alert rules (thresholds, notification timing, escalation logic)
- Contact lists (email addresses, phone numbers, Slack webhooks)
- Maintenance windows
- Geographic check locations
- Custom headers, authentication credentials

**Complexity Factors:**
- **Simple**: HTTP/HTTPS GET requests with basic alerts
- **Moderate**: TCP/DNS checks, keyword matching, custom headers
- **Complex**: Multi-step browser checks, API chains, conditional logic

### 3. Integration Recreation

**Common Integrations:**
- PagerDuty, OpsGenie (incident management)
- Slack, Microsoft Teams (real-time notifications)
- Email/SMS gateways
- Webhooks to custom systems
- Status page platforms (Statuspage.io, Atlassian)
- CI/CD pipelines (GitHub Actions, GitLab CI)

**Migration Effort:**
- Each integration = 15-30 minutes to recreate
- Testing notification chains = 30-60 minutes
- On-call rotation mapping = 1-2 hours

### 4. Status Page Migration

**Considerations:**
- **URL changes**: customersite.statuscake.com → customersite.uptimerobot.com
- **DNS CNAME**: status.yourcompany.com (can point anywhere, low lock-in)
- **Historical incidents**: Do they export for continuity?
- **Subscriber lists**: Can you export email subscribers?
- **Custom branding**: How much recreation effort?

**Business Impact:**
- Customer-facing URL change requires communication
- SEO impact of URL changes
- Historical incident records lost if not exportable

### 5. Geographic Distribution

**Lock-In Factor:**
- Provider A has 30 check locations, Provider B has 15
- Specific regions may not overlap (South America, Africa)
- Compliance requirements (data sovereignty, latency requirements)
- Migration may degrade geographic coverage

## Provider-Specific Lock-In Analysis

### 1. UptimeRobot

**Lock-In Score: 2/10 (LOW)**

**Data Portability:**
- **API**: Full REST API with excellent documentation
- **Historical Data**: Accessible via `getMonitors` endpoint with custom time ranges
- **Export Format**: JSON (programmatic), no native CSV export
- **Retention**: Full history available via API

**Configuration Migration:**
- **API Coverage**: 100% - all monitor types creatable via API
- **Bulk Operations**: Supported via API
- **Documentation**: Excellent, community scripts available
- **Monitor Types**: HTTP(S), Keyword, Ping, Port - all standard

**Migration Time Estimates:**
```
10 monitors (simple HTTP):        2-3 hours
  - API script development:       1 hour
  - Monitor creation:             30 minutes
  - Alert testing:                30 minutes
  - Verification:                 30 minutes

50 monitors (mixed types):        4-6 hours
  - Script enhancement:           1.5 hours
  - Monitor migration:            2 hours
  - Integration setup:            1 hour
  - Testing:                      1 hour

100 monitors (complex):           8-12 hours
  - Custom scripting:             3 hours
  - Monitor creation:             4 hours
  - Integration + status page:    2 hours
  - Full testing:                 2 hours
```

**Integrations:**
- 17 native integrations (Slack, PagerDuty, webhooks, email, SMS)
- Webhook support allows custom integrations
- Migration: 15-30 min per integration

**Status Page:**
- Public status pages included
- Custom domain via CNAME (no lock-in)
- Historical incidents: Not easily exportable
- Subscriber migration: Manual export available

**Mitigating Factors:**
- Community scripts for migration to/from UptimeRobot
- Standard monitor types (no proprietary check logic)
- Simple configuration model
- Excellent API documentation

**Recommendation:** Ideal source or target for migrations. Very low switching cost.

### 2. Pingdom (SolarWinds)

**Lock-In Score: 8/10 (HIGH)**

**Data Portability:**
- **API**: Legacy REST API, mixed quality documentation
- **Historical Data**: Limited API access, export features restricted by plan
- **Export Format**: CSV available for premium plans, limited date ranges
- **Retention**: Data accessible but painful to extract in bulk

**Configuration Migration:**
- **API Coverage**: ~70% - some features require UI
- **Bulk Operations**: Limited support
- **Documentation**: Fragmented between Pingdom and SolarWinds docs
- **Monitor Types**: HTTP, TCP, DNS, SMTP, POP3, IMAP - many proprietary

**Migration Time Estimates:**
```
10 monitors (simple HTTP):        6-8 hours
  - Manual export:                2 hours
  - Data transformation:          2 hours
  - Recreation in new platform:   2 hours
  - Testing:                      1 hour

50 monitors (mixed types):        20-25 hours
  - Export complexity:            6 hours
  - Data cleaning:                5 hours
  - Monitor recreation:           6 hours
  - Integration setup:            3 hours
  - Testing:                      3 hours

100 monitors (complex):           35-45 hours
  - Multi-stage export:           10 hours
  - Transformation scripts:       8 hours
  - Monitor creation:             12 hours
  - Integrations:                 5 hours
  - Validation:                   5 hours
```

**Integrations:**
- Native integrations to SolarWinds ecosystem (deep lock-in)
- Third-party integrations via webhooks
- Migration: Complex due to SolarWinds-specific configurations

**Status Page:**
- Pingdom Public Status Page tied to SolarWinds account
- Custom domain supported but requires DNS changes
- Historical incidents: Limited export capability
- Subscriber migration: Manual process

**Lock-In Factors:**
- **SolarWinds ecosystem**: Deep integration with other SolarWinds products
- **Migration to SolarWinds Observability**: Push to migrate from legacy Pingdom
- **RUM data**: Real User Monitoring data not portable
- **Custom check types**: Some proprietary logic not reproducible elsewhere

**Mitigating Factors:**
- Third-party export tools exist (community-built)
- HTTP monitors are standard and portable
- Webhook integrations reduce integration lock-in

**Recommendation:** High switching cost. Plan 2x time estimates. Avoid new commitments.

### 3. Checkly

**Lock-In Score: 6/10 (MODERATE-HIGH)**

**Data Portability:**
- **API**: Comprehensive REST API and GraphQL API
- **Historical Data**: Full programmatic access via API
- **Export Format**: JSON, Terraform, Pulumi
- **Retention**: Complete history via API

**Configuration Migration:**
- **API Coverage**: 100% - Monitoring-as-Code native
- **Bulk Operations**: Excellent via CLI and Terraform
- **Documentation**: Outstanding (developer-first company)
- **Monitor Types**: Browser (Playwright), API (HTTP), complex multi-step flows

**Migration Time Estimates:**
```
10 monitors (API checks):         3-5 hours
  - Export via CLI:               30 minutes
  - Translation to new format:    2 hours
  - Recreation:                   1 hour
  - Testing:                      1 hour

50 monitors (mixed):              15-20 hours
  - Playwright script analysis:   6 hours
  - Conversion to new format:     6 hours
  - Monitor setup:                4 hours
  - Testing:                      3 hours

100 monitors (complex):           30-40 hours
  - Complex Playwright flows:     12 hours
  - Browser check alternatives:   10 hours
  - Monitor creation:             8 hours
  - Integration + testing:        6 hours
```

**Integrations:**
- Slack, PagerDuty, OpsGenie, webhooks
- OTEL (OpenTelemetry) integration
- GitHub/GitLab CI/CD integration
- Migration: Moderate (30-60 min per integration)

**Status Page:**
- Not primary feature (focused on monitoring, not status pages)
- Integrations with third-party status pages
- Low lock-in risk for status page component

**Lock-In Factors:**
- **Playwright-based checks**: Requires translation to other browser automation if migrating
- **Monitoring-as-Code workflow**: Not all providers support this paradigm
- **Multi-step API flows**: Complex chains may be unique to Checkly's model
- **OTEL integration**: Tightly coupled to OTEL ecosystem

**Mitigating Factors:**
- **Excellent API**: Everything is exportable
- **Terraform provider**: Infrastructure-as-Code reduces manual migration
- **Open standards**: Playwright is open source, can run elsewhere
- **CLI tool**: `checkly` CLI makes bulk operations simple

**Recommendation:** Moderate lock-in. Playwright expertise translates elsewhere, but migration requires development time.

### 4. Better Stack

**Lock-In Score: 5/10 (MODERATE)**

**Data Portability:**
- **API**: Modern REST API
- **Historical Data**: Accessible via API
- **Export Format**: JSON
- **Retention**: Full retention with API access

**Configuration Migration:**
- **API Coverage**: ~90% - uptime monitors fully covered
- **Bulk Operations**: Supported via API
- **Documentation**: Good, improving
- **Monitor Types**: HTTP(S), TCP, UDP, Ping, Keyword, SSL - standard types

**Migration Time Estimates:**
```
10 monitors (simple HTTP):        3-4 hours
  - API export:                   30 minutes
  - Data transformation:          1 hour
  - Recreation:                   1 hour
  - Testing:                      1 hour

50 monitors (mixed):              10-15 hours
  - Export + cleaning:            3 hours
  - Monitor recreation:           5 hours
  - Integration setup:            2 hours
  - Testing:                      2 hours

100 monitors (complex):           20-28 hours
  - Bulk export scripting:        4 hours
  - Monitor creation:             10 hours
  - Incident mgmt migration:      4 hours
  - Integrations + testing:       5 hours
```

**Integrations:**
- Slack, MS Teams, PagerDuty, email, SMS, webhooks
- Incident management integration (Better Stack's platform)
- Log management (Logtail) integration
- Migration: Moderate (full platform migration more complex)

**Status Page:**
- Public status pages with custom domains
- Incident management integrated
- Subscriber lists exportable
- Historical incidents: API accessible

**Lock-In Factors:**
- **Platform approach**: Logs + Uptime + Incidents creates cross-product dependencies
- **Incident management**: Workflow tied to Better Stack's incident response
- **On-call scheduling**: Integrated but proprietary

**Mitigating Factors:**
- **Standard monitor types**: HTTP/TCP/Ping are portable
- **Good API**: Programmatic access to all data
- **Export capabilities**: Can extract configurations
- **No proprietary check logic**: Standard monitoring constructs

**Recommendation:** Moderate lock-in if using full platform (logs + uptime + incidents). Low if only using uptime monitoring.

### 5. StatusCake

**Lock-In Score: 5/10 (MODERATE)**

**Data Portability:**
- **API**: REST API available
- **Historical Data**: API access, limited free plan
- **Export Format**: JSON via API, no native CSV
- **Retention**: Depends on plan tier

**Configuration Migration:**
- **API Coverage**: ~80% - most features accessible
- **Bulk Operations**: Possible via API
- **Documentation**: Adequate, some gaps
- **Monitor Types**: Uptime, Page Speed, Domain, SSL, Virus - mixed portability

**Migration Time Estimates:**
```
10 monitors (simple HTTP):        4-5 hours
  - API export:                   1 hour
  - Data mapping:                 1.5 hours
  - Recreation:                   1.5 hours
  - Testing:                      1 hour

50 monitors (mixed):              12-16 hours
  - Export scripting:             3 hours
  - Monitor migration:            6 hours
  - Integration setup:            3 hours
  - Testing:                      2 hours

100 monitors (complex):           25-32 hours
  - Bulk export:                  5 hours
  - PageSpeed migration:          6 hours
  - Monitor creation:             10 hours
  - Integrations:                 4 hours
  - Validation:                   4 hours
```

**Integrations:**
- Email, SMS, Slack, webhooks, PagerDuty
- Contact groups (reusable notification lists)
- Migration: 20-30 min per integration

**Status Page:**
- Public status pages (custom domains supported)
- Historical uptime display
- Subscriber management
- Export: Limited API support

**Lock-In Factors:**
- **Page Speed monitoring**: Proprietary metrics, hard to replicate
- **Virus scanning**: Unique feature, no direct equivalent elsewhere
- **Contact groups**: Nested notification logic requires recreation
- **Free plan limits**: API access restricted on free tier

**Mitigating Factors:**
- **Standard uptime checks**: HTTP/TCP/DNS are portable
- **API availability**: Paid plans have full API access
- **Community**: Users have shared migration scripts

**Recommendation:** Moderate lock-in. Budget extra time for proprietary features (PageSpeed, Virus scan).

### 6. Freshping (Freshworks)

**Lock-In Score: 4/10 (LOW-MODERATE)**

**Data Portability:**
- **API**: REST API available
- **Historical Data**: Accessible via API
- **Export Format**: JSON
- **Retention**: 90 days on free tier, longer on paid

**Configuration Migration:**
- **API Coverage**: ~85% - uptime monitoring fully covered
- **Bulk Operations**: Supported
- **Documentation**: Good (Freshworks standard)
- **Monitor Types**: HTTP(S), Ping, TCP, DNS - all standard

**Migration Time Estimates:**
```
10 monitors (simple HTTP):        3-4 hours
  - API export:                   45 minutes
  - Data transformation:          1 hour
  - Recreation:                   1 hour
  - Testing:                      45 minutes

50 monitors (mixed):              8-12 hours
  - Export scripting:             2 hours
  - Monitor migration:            4 hours
  - Integration setup:            2 hours
  - Testing:                      2 hours

100 monitors (complex):           16-22 hours
  - Bulk operations:              3 hours
  - Monitor creation:             8 hours
  - Integrations:                 3 hours
  - Freshdesk integration alt:    2 hours
  - Validation:                   2 hours
```

**Integrations:**
- Freshdesk, Freshservice (Freshworks ecosystem)
- Slack, email, webhooks, PagerDuty
- Migration: Easy for standard integrations, complex for Freshworks-specific

**Status Page:**
- Public status pages with custom domains
- Historical uptime display
- Subscriber management via API
- Export: Supported

**Lock-In Factors:**
- **Freshworks ecosystem**: Deep integration with Freshdesk/Freshservice
- **Automatic ticketing**: Freshdesk integration creates operational dependency
- **Free tier**: 90-day data retention vs. lifetime on paid plans

**Mitigating Factors:**
- **Standard monitors**: All check types are industry-standard
- **Good API**: Freshworks has consistent API quality across products
- **Free tier**: No cost to maintain parallel monitoring during migration

**Recommendation:** Low lock-in for standalone use. Moderate if integrated with Freshdesk/Freshservice.

### 7. Uptime.com

**Lock-In Score: 6/10 (MODERATE-HIGH)**

**Data Portability:**
- **API**: REST API available (enterprise features)
- **Historical Data**: API access, plan-dependent
- **Export Format**: JSON, CSV (premium)
- **Retention**: Varies by plan tier

**Configuration Migration:**
- **API Coverage**: ~75% - some enterprise features UI-only
- **Bulk Operations**: Limited
- **Documentation**: Adequate for common operations
- **Monitor Types**: HTTP(S), TCP, ICMP, DNS, Transaction - mixed complexity

**Migration Time Estimates:**
```
10 monitors (simple HTTP):        5-7 hours
  - Manual export (if no API):    2 hours
  - Data preparation:             2 hours
  - Recreation:                   2 hours
  - Testing:                      1 hour

50 monitors (mixed):              18-24 hours
  - Export complexity:            5 hours
  - Monitor migration:            8 hours
  - Integration recreation:       4 hours
  - Testing:                      3 hours

100 monitors (complex):           35-45 hours
  - Enterprise feature export:    8 hours
  - Transaction monitoring:       10 hours
  - Monitor creation:             12 hours
  - Integrations:                 5 hours
  - Validation:                   5 hours
```

**Integrations:**
- PagerDuty, Slack, email, SMS, webhooks
- Enterprise integrations (ServiceNow, Jira)
- Migration: Complex for enterprise integrations

**Status Page:**
- Advanced status page features
- Custom domains supported
- Historical incidents
- Export: Limited

**Lock-In Factors:**
- **Transaction monitoring**: Multi-step web transactions proprietary
- **Enterprise features**: Advanced alerting logic hard to replicate
- **RUM integration**: Real User Monitoring not portable
- **Tiered access**: API features limited by plan tier

**Mitigating Factors:**
- **Standard checks**: HTTP/TCP/DNS are portable
- **API availability**: Exists, though not always comprehensive
- **Industry standard**: Uses common monitoring paradigms

**Recommendation:** Moderate-high lock-in for enterprise features. Budget 2x estimates.

### 8. Hyperping

**Lock-In Score: 3/10 (LOW)**

**Data Portability:**
- **API**: REST API available
- **Historical Data**: Accessible via API
- **Export Format**: JSON
- **Retention**: Full history

**Configuration Migration:**
- **API Coverage**: ~90% - simple product, good coverage
- **Bulk Operations**: Supported
- **Documentation**: Good for core features
- **Monitor Types**: HTTP(S), TCP, Ping - all standard

**Migration Time Estimates:**
```
10 monitors (simple HTTP):        2-3 hours
  - API export:                   30 minutes
  - Recreation:                   1 hour
  - Testing:                      1 hour

50 monitors (mixed):              6-8 hours
  - Export + scripting:           2 hours
  - Monitor migration:            3 hours
  - Integration setup:            1.5 hours
  - Testing:                      1.5 hours

100 monitors (complex):           12-16 hours
  - Bulk operations:              3 hours
  - Monitor creation:             6 hours
  - Integrations:                 3 hours
  - Validation:                   2 hours
```

**Integrations:**
- Email, Slack, webhooks, Discord, Telegram
- Simple notification model
- Migration: Easy (15-20 min per integration)

**Status Page:**
- Public status pages included
- Custom domains supported
- Subscriber management
- Export: Available via API

**Lock-In Factors:**
- Minimal - very standard feature set

**Mitigating Factors:**
- **Simple product**: Easy to understand and replicate
- **Standard monitors**: All types are portable
- **Good API**: Clean, well-documented
- **No proprietary features**: Everything has equivalents

**Recommendation:** Very low lock-in. Easy migration source or target.

### 9. Upptime (Open Source)

**Lock-In Score: 1/10 (MINIMAL)**

**Data Portability:**
- **Config**: YAML file in GitHub repository
- **Historical Data**: GitHub Issues contain incident history
- **Export Format**: Structured YAML, easily parseable
- **Retention**: Unlimited (GitHub-hosted)

**Configuration Migration:**
- **API Coverage**: N/A - it's a config file
- **Bulk Operations**: Edit YAML, commit, done
- **Documentation**: GitHub README
- **Monitor Types**: HTTP(S) endpoints only

**Migration Time Estimates:**
```
10 monitors (HTTP):               1-2 hours
  - YAML export:                  15 minutes
  - Script to convert:            45 minutes
  - Verification:                 30 minutes

50 monitors (HTTP):               2-3 hours
  - Scripted migration:           1 hour
  - Testing:                      1 hour

100 monitors (HTTP):              3-4 hours
  - Automated conversion:         1.5 hours
  - Validation:                   1.5 hours
```

**Integrations:**
- GitHub Actions (notifications)
- Webhook support for Slack, Discord, etc.
- Migration: Recreate notification actions (30-60 min)

**Status Page:**
- GitHub Pages static site
- Custom domain via CNAME (no lock-in)
- Historical incidents in GitHub Issues
- Export: Everything is already in Git

**Lock-In Factors:**
- **None**: Everything is open, portable, version-controlled

**Mitigating Factors:**
- **Git-based**: All config in repository
- **YAML**: Human-readable, machine-parseable
- **Static output**: Status page is HTML/CSS/JS
- **GitHub Actions**: Can run anywhere with slight modifications

**Recommendation:** Zero lock-in. Perfect for avoiding vendor dependency.

### 10. Uptime Kuma (Open Source)

**Lock-In Score: 1/10 (MINIMAL)**

**Data Portability:**
- **Config**: SQLite database or JSON export
- **Historical Data**: Full database access
- **Export Format**: JSON, database file
- **Retention**: Unlimited (self-hosted)

**Configuration Migration:**
- **API Coverage**: 100% (REST API)
- **Bulk Operations**: Database direct access or API
- **Documentation**: GitHub wiki
- **Monitor Types**: HTTP(S), TCP, DNS, Ping, Docker, Keyword - comprehensive

**Migration Time Estimates:**
```
10 monitors (simple HTTP):        2-3 hours
  - JSON export:                  15 minutes
  - Script to convert:            1 hour
  - Recreation:                   1 hour

50 monitors (mixed):              4-6 hours
  - Database export:              1 hour
  - Transformation script:        2 hours
  - Migration + testing:          2 hours

100 monitors (complex):           8-10 hours
  - Bulk export scripting:        2 hours
  - Data transformation:          3 hours
  - Monitor creation:             3 hours
  - Validation:                   2 hours
```

**Integrations:**
- 70+ notification services (Slack, Discord, Telegram, email, SMS, etc.)
- Webhook support
- Migration: Recreate notification configs (varies)

**Status Page:**
- Built-in status pages
- Custom domain via reverse proxy
- Historical uptime displayed
- Export: Full database access

**Lock-In Factors:**
- **Minimal**: Self-hosted, you control the data
- **Docker-based**: Portable across infrastructure

**Mitigating Factors:**
- **SQLite database**: Can query directly
- **JSON export**: Built-in export functionality
- **REST API**: Programmatic access to all features
- **Open source**: Can fork and modify

**Recommendation:** Minimal lock-in. Technical migration required but all data accessible.

## Migration Complexity Matrix

| Provider       | Lock-In Score | 10 Monitors | 50 Monitors | 100 Monitors | Key Challenge                    |
|----------------|---------------|-------------|-------------|--------------|----------------------------------|
| Upptime        | 1/10          | 1-2 hrs     | 2-3 hrs     | 3-4 hrs      | HTTP-only (simplicity)           |
| Uptime Kuma    | 1/10          | 2-3 hrs     | 4-6 hrs     | 8-10 hrs     | Self-hosting setup               |
| UptimeRobot    | 2/10          | 2-3 hrs     | 4-6 hrs     | 8-12 hrs     | Status page subscribers          |
| Hyperping      | 3/10          | 2-3 hrs     | 6-8 hrs     | 12-16 hrs    | Limited features (simple)        |
| Freshping      | 4/10          | 3-4 hrs     | 8-12 hrs    | 16-22 hrs    | Freshworks ecosystem             |
| StatusCake     | 5/10          | 4-5 hrs     | 12-16 hrs   | 25-32 hrs    | PageSpeed/Virus proprietary      |
| Better Stack   | 5/10          | 3-4 hrs     | 10-15 hrs   | 20-28 hrs    | Platform integration             |
| Checkly        | 6/10          | 3-5 hrs     | 15-20 hrs   | 30-40 hrs    | Playwright script conversion     |
| Uptime.com     | 6/10          | 5-7 hrs     | 18-24 hrs   | 35-45 hrs    | Transaction monitoring           |
| Pingdom        | 8/10          | 6-8 hrs     | 20-25 hrs   | 35-45 hrs    | SolarWinds integration           |

## Strategic Recommendations

### Minimizing Lock-In Risk

**When Selecting a Provider:**

1. **Prioritize API Quality**
   - Full REST API covering all features
   - Comprehensive documentation
   - Bulk operation support
   - Historical data access

2. **Favor Open Standards**
   - Standard HTTP/TCP/DNS checks over proprietary logic
   - OpenTelemetry compatibility
   - Terraform providers (Infrastructure-as-Code)
   - Webhook integrations (avoid platform-specific)

3. **Test Export Early**
   - During trial period, export sample data
   - Verify API functionality
   - Confirm historical data accessibility
   - Check configuration export formats

4. **Use Custom Domains**
   - CNAME for status pages (status.yourcompany.com)
   - Avoid provider-specific URLs in customer communications
   - Reduces switching friction

### Migration Planning

**Pre-Migration Checklist:**
- [ ] Export all monitor configurations via API
- [ ] Download historical uptime data (CSV/JSON)
- [ ] Document integration mappings (Slack channels, PagerDuty services)
- [ ] Screenshot complex alert logic
- [ ] Export status page subscribers
- [ ] List all custom headers, authentication credentials
- [ ] Map geographic check locations

**Parallel Operation Strategy:**
- Run new provider in parallel for 2-4 weeks
- Compare alert firing (should be identical)
- Gradual cutover: non-critical → critical monitors
- Maintain old provider for 1 month post-migration (validate)

### Tool-Assisted Migration

**Migration Scripts:**
Many providers have community-contributed migration tools:
- UptimeRobot ↔ Uptime Kuma: Active GitHub repos
- Pingdom → UptimeRobot: Partial support
- Generic HTTP monitors: Easy to script (curl + jq)

**Terraform Approach:**
```hcl
# Define monitors as code
resource "uptimerobot_monitor" "example" {
  count          = length(var.monitors)
  friendly_name  = var.monitors[count.index].name
  url            = var.monitors[count.index].url
  type           = "http"
}
```

Allows provider-agnostic definition, change backend to migrate.

## Conclusion

**Lowest Lock-In (Recommended for Risk-Averse):**
1. **Upptime** (1/10): YAML config, GitHub-based, zero proprietary features
2. **Uptime Kuma** (1/10): Self-hosted, full data access, REST API
3. **UptimeRobot** (2/10): Excellent API, standard features, easy migration

**Moderate Lock-In (Acceptable with Monitoring):**
4. **Hyperping** (3/10): Simple, standard features
5. **Freshping** (4/10): Good API, Freshworks ecosystem adds complexity
6. **StatusCake** (5/10): PageSpeed adds lock-in
7. **Better Stack** (5/10): Platform play increases dependencies

**High Lock-In (Avoid or Plan Exit):**
8. **Checkly** (6/10): Playwright conversion requires dev time
9. **Uptime.com** (6/10): Enterprise features proprietary
10. **Pingdom** (8/10): SolarWinds ecosystem, poor export

For MPSE V2 framework, lock-in risk should weight 15-25% of service selection scoring, with higher weighting for organizations with limited engineering resources or frequent provider reassessment cycles.

**Migration Budget Rule of Thumb:**
```
Simple migration (API + standard checks): $500-2,000
Moderate migration (mixed features):      $2,000-5,000
Complex migration (proprietary features): $5,000-15,000

(Based on $150/hour engineering time)
```

Plan migration windows during low-traffic periods and maintain dual monitoring for 2-4 weeks to ensure reliability parity.
