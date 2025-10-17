# Render

## Overview
Render is a modern cloud platform that has emerged as the leading Heroku alternative, offering ease-of-use with more advanced features than traditional PaaS. It provides a git-centric, push-and-deploy approach with SSD-based storage, private networking, and support for a wide array of languages and frameworks including Python/Flask. Render stands out for maintaining a generous free tier while competitors have eliminated theirs, and offers granular compute options across the pricing spectrum.

## Pricing

### Free Tier
- 750 hours per month of free instance credit (enough for one instance running 24/7)
- 0.1 CPU, public-facing servers
- Custom domains and fully-managed TLS certificates
- Pull Request Previews, Log Streams, rollbacks
- Free PostgreSQL database for 90 days (1GB disk, 256MB RAM, 0.1 CPU)
- No credit card required
- **Limitations:** Services spin down after 15 minutes of inactivity, no persistent disk, no SMTP email

### Starter Tier
- Pay-as-you-go starting at $7/month for basic web service
- Shared CPU instances with guaranteed resources
- Multiple container sizes available

### Production Tier
- Dedicated instances starting at $25/month
- Full CPU cores, more RAM options
- Persistent disks available
- Production PostgreSQL from $7/month

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
