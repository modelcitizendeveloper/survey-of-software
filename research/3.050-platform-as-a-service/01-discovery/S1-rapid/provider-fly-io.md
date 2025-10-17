# Fly.io

## Overview
Fly.io is a developer-centric cloud platform that enables applications to run globally close to users through its Anycast networking platform. Unlike competitors that run on major cloud providers, Fly.io operates on its own bare-metal servers distributed worldwide, offering significantly better performance through edge computing. It supports containerized applications and allows developers to customize networking behavior. However, Fly.io eliminated its free tier for new users on October 7, 2024, shifting to a pure usage-based model.

## Pricing

### Free Tier (Legacy Only)
- Fly.io honors legacy free allowances for users who signed up before October 7, 2024
- New organizations created after October 7, 2024 have no free tier
- If legacy users switch to Pay As You Go model, old free tier is permanently lost
- **No free tier for new users in 2024-2025**

### Pay As You Go (Current Model)
- Usage-based billing: pay only for resources provisioned
- Virtual machines: billed per second
- Storage: $0.15 per GB per month
- Outbound bandwidth: starting at $0.02 per GB
- No minimum monthly fee, but no free allowance

### Pricing Philosophy
- Simplified: one plan based on consumption
- Pro-rated billing for time resources are provisioned
- No pricing tiers, just usage-based costs

## Key Strengths
- Exceptional performance (34ms response times vs 600ms Heroku, 2.1s Render)
- Global edge computing on bare-metal servers
- Applications run close to users worldwide (reduced latency)
- CLI-first approach for power users
- Full control over container deployment
- Anycast networking platform

## Market Position
**GitHub Stars:** Not applicable (platform, not open-source project)
**Market Share:** Popular among performance-focused developers
**Community:** Strong technical community, less beginner-friendly

## Best For
Performance-critical applications, global user bases needing low latency, teams with technical DevOps expertise, CLI-comfortable developers, applications needing edge computing

## Important Considerations
- No free tier makes it difficult to test before committing
- CLI-first approach has steeper learning curve than git-push platforms
- Best for users who understand container orchestration
- Not ideal for beginners or budget-constrained experimentation
- Removal of free tier in October 2024 limits accessibility
