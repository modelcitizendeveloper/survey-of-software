# Heroku

## Overview
Heroku is the original and most established Platform-as-a-Service, abstracting away infrastructure complexities to let developers focus on application code. It pioneered the PaaS model with container-based deployment (dynos) and robust add-on marketplace. Heroku is owned by Salesforce and remains a market leader, though it has faced criticism for high costs and recent reliability issues. The platform eliminated its free tier on November 28, 2022, citing fraud and abuse, making it the most expensive option among PaaS providers.

## Pricing

### Free Tier
- Eliminated November 28, 2022
- No free option available
- **Requires payment from day one**

### Eco Plan (Lowest Tier)
- $5 per dyno per month (minimum)
- Basic web dynos for low-traffic apps
- Shared compute resources
- Apps sleep after 30 minutes of inactivity

### Professional Tier
- Starting at $25-50/month per dyno
- Heroku Dynos: $7+/month
- Heroku Postgres: $9+/month
- Heroku Data for Redis: $15+/month
- No sleep, dedicated resources

### Enterprise
- Custom pricing
- Enhanced security, compliance, support
- Typically hundreds to thousands per month

## Key Strengths
- Most mature PaaS with 15+ years of development
- Extensive add-on marketplace (200+ services)
- Strong Python/Flask support and documentation
- Simple git-based deployment (git push heroku main)
- Excellent for quick prototyping (despite cost)
- Built-in CI/CD, review apps, pipelines

## Market Position
**GitHub Stars:** Not applicable (platform, not open-source project)
**Market Share:** Dominant in PaaS space, but losing ground to alternatives
**Community:** Massive developer community and ecosystem

## Reliability Concerns
- 15-hour, 45-minute outage on June 10, 2025
- 8-hour, 30-minute outage on June 18, 2025
- Frequent and significant outages have damaged reputation
- Users increasingly concerned about reliability

## Best For
Enterprise applications with budget, teams familiar with Heroku, projects requiring extensive add-ons, organizations valuing maturity over cost, rapid MVPs with funding

## Cost Comparison
- Basic app with dyno + Postgres + Redis: ~$49/month (doubled from pre-free-tier-elimination)
- Significantly more expensive than Render, Railway, or Fly.io for equivalent workloads
- Premium justified by add-on ecosystem and enterprise features
