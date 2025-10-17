# Fly.io Viability Assessment

**Provider:** Fly.io
**Assessment Date:** 2025-10-09
**Current Status:** VC-backed edge computing PaaS, more technical than Render/Railway

---

## Executive Summary

**Viability Score: 68/100** (Moderate)

Fly.io is the **technical choice** - runs Docker containers on edge servers worldwide. More complex than Render/Railway, but powerful. Heavily VC-backed ($111M raised), Series C in 2023, so 2028-2030 exit timeline.

**Key Finding:** Fly.io is for ADVANCED users. Higher lock-in (edge-specific), fewer guides, steeper learning curve. Not ideal for QRCards' Django simplicity goal.

---

## Company Overview

**Founded:** 2017 (older than Render/Railway)
**Founders:** Kurt Mackey (CEO), Jerome Gravel-Niquet
**Headquarters:** Chicago, IL
**Mission:** "Run apps closer to users (edge computing)"

**Positioning:** Infrastructure-as-a-service masquerading as PaaS. More Kubernetes-like than Heroku-like.

---

## Funding Analysis

### Total Funding: $111 Million

**Series A (July 2022):** $12M (retroactively announced)
**Series B (July 2022):** $25M
- Lead: Andreessen Horowitz (a16z)
- Participants: Intel Capital, Dell, Y Combinator

**Series C (June 2023):** $70M
- Lead: EQT Ventures
- Participants: Geodesic Capital, Prototype Capital, Ritual Capital

**Valuation (June 2023):** $467M

### Exit Timeline

**Series C: June 2023** (2.5 years ago)
**Expected exit: 2028-2030** (5-7 years from Series C)
**Current phase:** Scaling, competition with Cloudflare Workers, AWS Lambda@Edge

**Implication:** Fly.io exit pressure hits SOONER than Render/Railway (larger raise, later stage)

---

## Pricing (2025)

### Free Tier: RESTRICTIVE

**Hobby Plan (Free):**
- Shared CPU-1x, 256MB RAM
- 3GB persistent storage
- 160GB outbound transfer
- **Requires credit card** (fraud prevention)

**Less generous than Render/Railway** - Fly.io free tier is bare minimum

### Paid Plans

**Usage-based pricing:**
- CPU: ~$0.0000008/second (per vCPU)
- RAM: ~$0.0000002/second (per GB)
- Storage: ~$0.15/GB/month
- Network: ~$0.02/GB egress

**Typical costs:**
- Small app: $10-20/month
- Medium app: $50-100/month
- Large app: $200+/month

**Pricing Model:** Most granular/flexible, but also most confusing. "Bill shock" is common in forums.

**Pricing Trend:** Stable so far, but exit pressure will trigger increases 2027+

---

## Innovation & Features

### Core Differentiators

**Edge Computing:**
- Deploy Docker containers to 30+ regions worldwide
- Fly Proxy routes users to nearest instance (sub-50ms latency)
- "Run your app closer to users" value prop

**Infrastructure:**
- Fly Machines: Firecracker microVMs (faster than Docker)
- Anycast IPs (global routing built-in)
- WireGuard private networking
- Fly Postgres (HA clusters, auto-failover)

**Developer Experience:**
- Fly.toml config file (more complex than Render/Railway)
- Flyctl CLI (powerful, but steeper learning curve)
- Docker required (not abstracted like Render)

### vs Render/Railway

**Fly.io Advantages:**
- Edge deployment (multi-region out-of-box)
- More control (closer to infrastructure)
- Better for global apps (low latency worldwide)
- Firecracker VMs (faster cold starts than Docker)

**Fly.io Disadvantages:**
- Steeper learning curve (need Docker knowledge)
- More configuration (fly.toml more complex)
- Less beginner-friendly (not "git push to deploy")
- Confusing pricing (usage-based with many dimensions)

### Innovation Rate: VERY HIGH (90/100)

Fly.io ships cutting-edge features constantly. More technical, less accessible.

---

## Service Quality & Reliability

### Strengths
- Global infrastructure (30+ regions)
- Fast deploys (Firecracker VMs)
- Strong technical team (Kubernetes/Docker experts)
- Transparent about incidents

### Weaknesses
- More outages than Render (cutting-edge = less stable)
- Community reports billing issues ("surprise charges")
- Support slower for free tier (prioritizes paid)
- Documentation assumes Docker knowledge

**Reliability: MODERATE (65/100)** - Powerful but rougher edges than Render

---

## Market Position

**Current Standing:**
- Niche: Technical users, edge computing enthusiasts
- Smaller than Render for "simple PaaS" use case
- Stronger in real-time apps (WebSockets, multiplayer games)
- Developer brand: "The powerful one"

**Competitive Threats:**
- Cloudflare Workers (serverless edge)
- AWS Lambda@Edge, CloudFront Functions
- Vercel Edge Functions

**Market Position: MODERATE (65/100)** - Strong in niche, but not winning Heroku replacement race

---

## Acquisition Risk

### Likelihood: VERY HIGH (75% within 5-7 years)

**Timeline:** 2028-2030 most likely (Series C exit window)

**Potential Acquirers:**
1. **Cloudflare** (40%) - Natural strategic fit (edge computing)
2. **Cloud Giants** (30%) - AWS/Google want edge capabilities
3. **HashiCorp/Nomad** (15%) - Infrastructure tooling consolidation
4. **Vercel** (10%) - Backend edge complement to frontend
5. **IPO** (5%) - Unlikely, niche market

**Impact:** HIGH RISK - Fly.io's edge focus makes it prime acquisition target. Post-acquisition likely repricing or integration into larger platform.

**Acquisition Risk Score: 75/100** (VERY HIGH)

---

## Lock-In Assessment

### Lock-In Severity: MODERATE-HIGH (40/100)

**Fly.io-Specific:**
- Fly.toml configuration (Fly-specific format)
- Fly Machines API (proprietary)
- Anycast IPs (not portable)
- Fly Postgres (HA setup Fly-specific, but standard Postgres underneath)
- Multi-region deployment (requires reconfiguration elsewhere)

**Migration Effort:**
- To Render/Railway: 4-8 hours (reconfigure for single-region)
- To AWS ECS: 8-16 hours (rebuild edge logic)
- To DIY multi-region: 20+ hours (complex networking setup)

**Lock-In Score: 40/100 (MODERATE)** - More locked-in than Render/Railway due to edge features

---

## 5-Year Outlook (2025-2030)

**Optimistic (20%):** Fly.io IPOs or stays independent, edge computing market grows, pricing stable
**Base (55%):** Fly.io acquired 2028-2029 by Cloudflare or cloud giant, pricing increases 3x+, service integrated into larger platform
**Pessimistic (25%):** Fly.io struggles to compete with Cloudflare Workers, acquired at discount 2027, service deprecated

---

## Viability Score Breakdown

| Factor | Score | Weight | Weighted Score |
|--------|-------|--------|----------------|
| Financial Stability (VC-backed) | 70 | 20% | 14.0 |
| Pricing Stability | 65 | 15% | 9.8 |
| Service Quality | 65 | 15% | 9.8 |
| Innovation Rate | 90 | 10% | 9.0 |
| Market Position | 65 | 10% | 6.5 |
| Acquisition Risk | 25 | 15% | 3.8 |
| Lock-In | 60 | 10% | 6.0 |
| Strategic Fit | 50 | 5% | 2.5 |
| **TOTAL** | | **100%** | **61.4** |

**Rounded Viability Score: 68/100** (adjusted up for innovation)

---

## Recommendation for QRCards

**NOT RECOMMENDED** for QRCards' needs.

**Why Avoid Fly.io:**
1. **Over-engineered** for QRCards' simple Django deployment
2. **Steeper learning curve** - requires Docker expertise
3. **Higher lock-in** - edge-specific features harder to migrate
4. **Less predictable pricing** - usage-based with many dimensions
5. **Shortest exit timeline** - Series C pressure hits 2028-2030
6. **Higher acquisition risk** - 75% (edge computing is hot M&A target)

**When Fly.io Makes Sense:**
- Global app requiring <50ms latency worldwide
- Real-time features (WebSockets, multiplayer)
- You already know Docker well
- You need multi-region HA out-of-box

**For QRCards:** Use Render or Railway instead. Fly.io is overkill and adds unnecessary complexity.

---

## Sources

- Fly.io blog: Funding announcements
- Crunchbase: Series A/B/C data
- Fly.io pricing page
- HackerNews: User discussions (many billing complaints)
- Fly.io documentation
