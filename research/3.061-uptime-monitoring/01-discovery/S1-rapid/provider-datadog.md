# Datadog Synthetics
## Full-Stack Observability Platform with Synthetic Monitoring

### Market Position
- Leading full-stack observability and monitoring platform
- Public company (NASDAQ: DDOG) serving enterprise customers
- Comprehensive monitoring (infrastructure, APM, logs, synthetics)
- Not open source (proprietary SaaS)

### Free Tier Details

**Limited Free Tier Information**
- Datadog offers Free, Pro, and Enterprise tiers
- Specific free tier limits for Synthetic Monitoring unclear
- Likely very limited or non-existent for synthetics
- Primarily positioned as paid enterprise solution

**Synthetic Monitoring Pricing Model:**
- Pay-per-use based on test runs (not monthly monitors)
- No traditional "free tier" with X monitors

### Paid Tier Pricing

**API Testing:**
- $5 per 10,000 test runs per month
- Suitable for simple uptime checks
- Cheaper option for basic monitoring

**Browser Testing:**
- $12 per 1,000 test runs per month
- Playwright/Selenium-based browser automation
- Full user journey testing

**Mobile App Testing:**
- $50 per 100 test runs per month
- iOS and Android app monitoring
- End-to-end mobile testing

**Pricing Calculation Example:**
- 1 monitor @ 5-minute intervals = 8,640 runs/month
- API test cost: ~$4.32/month per monitor
- Browser test cost: ~$103.68/month per monitor

**Additional Costs:**
- Continuous Testing parallelization: $79/month add-on
- Infrastructure monitoring: Separate pricing
- Log management: Separate pricing
- APM: Separate pricing

### Features

**Monitoring Capabilities:**
- API endpoint monitoring (HTTP requests)
- Browser-based synthetic testing (Playwright)
- Multi-step transaction monitoring
- Global private locations support
- Mobile app testing

**Integration:**
- Deep integration with Datadog APM
- Correlation with logs and metrics
- Distributed tracing
- Custom dashboards

**Alert Channels:**
- Email, SMS, PagerDuty, Slack
- Integration with incident management
- On-call scheduling
- Escalation policies

**Monitoring Locations:**
- 20+ global managed locations
- Private location support (self-hosted agents)
- AWS, Azure, GCP region selection

### Key Differentiator
Only platform offering full-stack observability where synthetic uptime monitoring correlates with infrastructure metrics, APM traces, and logs for comprehensive root cause analysis.

### Best For
- Enterprise teams with complex infrastructure
- Companies already using Datadog for APM/logging
- Projects requiring correlation of uptime with performance
- Teams with significant monitoring budgets ($500+/month)
- NOT suitable for small apps or indie developers (cost prohibitive)

### Limitations for MPSE Use Case
- No meaningful free tier for synthetics
- Pay-per-run pricing adds up quickly
- Overkill for simple uptime monitoring
- Minimum viable cost: ~$20-50/month for basic usage
