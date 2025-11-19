# Render

## Overview
Render is a modern cloud platform that has emerged as the leading Heroku alternative, offering ease-of-use with more advanced features than traditional PaaS. It provides a git-centric, push-and-deploy approach with SSD-based storage, private networking, and support for a wide array of languages and frameworks including Python/Flask. Render stands out for maintaining a generous free tier while competitors have eliminated theirs, and offers granular compute options across the pricing spectrum.

## Pricing

**Account Tiers:**
- **Hobby (Free):** Individual developers, 100 GB bandwidth/month, 500 build minutes/month, up to 1 project, email support
- **Professional:** $19/user/month - 500 GB bandwidth/month, 500 pipeline minutes per user/month, unlimited projects, up to 10 team members, chat support
- **Organization:** $29/user/month - 1 TB bandwidth/month, unlimited team members, SOC 2 Type II & ISO 27001 certified, audit logs
- **Enterprise:** Custom pricing - guaranteed uptime, premium support, dedicated success engineer

**Compute Pricing (Web Services, Private Services, Background Workers):**

| Tier | Price | RAM | CPU |
|------|-------|-----|-----|
| Free | $0/month | 512 MB | 0.1 |
| Starter | $9/month | 512 MB | 0.5 |
| Standard | $25/month | 2 GB | 1 |
| Pro | $85/month | 4 GB | 2 |
| Pro Plus | $175/month | 8 GB | 4 |
| Pro Max | $225/month | 16 GB | 4 |
| Pro Ultra | $450/month | 32 GB | 8 |

**Static Sites:** $0/month - Global CDN with continuous Git deploys and custom domains

**Cron Jobs:** From $1/month - Pricing from $0.00016/minute (Starter) to $0.00405/minute (Pro Plus)

**PostgreSQL Databases:**
- Free tier: $0/month (30-day limit)
- Basic-256mb: $6/month
- Basic-1gb: $19/month
- Basic-4gb: $75/month
- Pro tier: $55-$3,000/month (4GB to 256GB RAM)
- Accelerated tier: $160-$11,000/month

**Redis (Render Key Value):**

| Tier | Price | RAM |
|------|-------|-----|
| Free | $0/month | 25 MB |
| Starter | $10/month | 256 MB |
| Standard | $32/month | 1 GB |
| Pro | $135/month | 5 GB |
| Pro Plus | $250/month | 10 GB |
| Pro Max | $550/month | 20 GB |
| Pro Ultra | $1,100/month | 40 GB |

**Persistent Disks:** $0.25/GB per month

**Free Tier Highlights (Hobby):**
- 0.1 CPU, 512 MB RAM, public-facing servers
- Custom domains and fully-managed TLS certificates
- Pull Request Previews, Log Streams, rollbacks
- Free PostgreSQL database for 30 days (limited resources)
- No credit card required
- **Limitations:** Services spin down after 15 minutes of inactivity, no SMTP email

**Key Features:**
- Compute usage billed and prorated by the second
- If a workspace has no services or activity during a month, per-member fees are waived
- All tiers support persistent disks at $0.25/GB/month

## Key Strengths
- Maintains a free tier when competitors eliminated theirs (major competitive advantage)
- Native Python/Flask support with automatic detection
- Git-based deployment workflow (push to deploy)
- Granular compute options with better mid-range pricing than Heroku
- Managed PostgreSQL, Redis, and other services
- No credit card required to start

## Market Position
**GitHub Stars:** Not applicable (platform, not open-source project)
**Market Share:** Emerging as top Heroku alternative post-2022
**Community:** Strong developer community, particularly among Flask/Django developers

## Best For
Mid-sized web applications, Python/Flask apps, developers migrating from Heroku, projects needing free tier for prototyping, teams wanting git-based deployment without Heroku's cost

## Performance Notes
Benchmarks show slower response times than Fly.io (2.1s vs 34ms for health endpoints) but comparable to Heroku (600ms). Trade-off between ease of use and raw performance.
