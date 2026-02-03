# 3.050 Platform-as-a-Service (PaaS) - Discovery Table of Contents

**Experiment Date:** October 9, 2025
**Status:** Discovery Complete (10 providers analyzed)
**Recommendation:** Render (primary) or PythonAnywhere (alternative) for QRCards

---

## Quick Navigation

- [S1 Rapid Discovery](#s1-rapid-discovery) - Popularity-based provider discovery
- [S2 Comprehensive Discovery](#s2-comprehensive-discovery) - Deep dive technical analysis
- [S3 Need-Driven Discovery](#s3-need-driven-discovery) - Use case scoring (7 scenarios)
- [S4 Strategic Discovery](#s4-strategic-discovery) - Long-term viability and exit risk
- [QRCards Assessment](#qrcards-strategic-assessment) - Business-specific recommendation

---

## Discovery Methodologies

### S1 Rapid Discovery

**Approach:** Popularity-first discovery for Python/Flask hosting
**File:** [01-discovery/S1-rapid/approach.md](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S1-rapid/approach.md)

**Provider Analysis:**
- [Render](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S1-rapid/provider-render.md) - Most popular Heroku alternative, free tier hero
- [Railway](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S1-rapid/provider-railway.md) - Modern DX, beautiful UI, usage-based pricing
- [Fly.io](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S1-rapid/provider-fly-io.md) - Best performance (34ms), edge computing focus
- [Heroku](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S1-rapid/provider-heroku.md) - Market leader (established), premium pricing
- [PythonAnywhere](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S1-rapid/provider-pythonanywhere.md) - Python-native niche player
- [Vercel](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S1-rapid/provider-vercel.md) - Serverless/Jamstack specialist (not traditional PaaS)
- [DigitalOcean App Platform](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S1-rapid/provider-digitalocean-app-platform.md) - VPS brand expanding to PaaS
- [AWS Elastic Beanstalk](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S1-rapid/provider-aws-elastic-beanstalk.md) - AWS ecosystem (enterprise only)
- [Google App Engine](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S1-rapid/provider-google-app-engine.md) - Enterprise serverless leader (86% market share)
- [Azure App Service](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S1-rapid/provider-azure-app-service.md) - Microsoft ecosystem (enterprise only)

**Recommendation:** [01-discovery/S1-rapid/recommendation.md](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S1-rapid/recommendation.md)

**Key Finding:** Top 3 by popularity: Render (free tier champion), Heroku (expensive leader), Google App Engine (enterprise serverless). PythonAnywhere ranks #7-8 overall, #1-2 for Python beginners.

---

### S2 Comprehensive Discovery

**Approach:** Deep dive technical analysis of top providers
**File:** [01-discovery/S2-comprehensive/approach.md](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S2-comprehensive/approach.md)

**Technical Deep Dives:**
- [Render](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S2-comprehensive/provider-render.md) - Git-native, Docker support, best documentation
- [Railway](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S2-comprehensive/provider-railway.md) - Modern DX, nixpacks buildpack innovation
- [Fly.io](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S2-comprehensive/provider-flyio.md) - Edge computing, Firecracker VMs, multi-region
- [Heroku](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S2-comprehensive/provider-heroku.md) - Mature ecosystem, 200+ add-ons, declining innovation
- [PythonAnywhere](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S2-comprehensive/provider-pythonanywhere.md) - Python-specific, beginner-friendly, educational focus
- [DigitalOcean App Platform](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S2-comprehensive/provider-digitalocean.md) - Predictable pricing, VPS integration
- [Vercel](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S2-comprehensive/provider-vercel.md) - Next.js-optimized, serverless functions
- [Google Cloud Run](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S2-comprehensive/provider-google-cloud-run.md) - Container-native serverless, pay-per-request

**Cross-Provider Analysis:**
- [Pricing Matrix](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S2-comprehensive/pricing-matrix.md) - Cost comparison across providers and tiers
- [Feature Matrix](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S2-comprehensive/feature-matrix.md) - Technical capabilities side-by-side
- [Python/Flask Support](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S2-comprehensive/python-flask-support.md) - Framework-specific deployment quality
- [Deployment Methods](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S2-comprehensive/deployment-methods.md) - Git, Docker, CLI comparison

**Key Finding:** Modern Docker-native PaaS (Render, Railway, Fly.io) winning over language-specific platforms. Python-native deployment (PythonAnywhere) remains competitive for solo developers without Docker expertise.

---

### S3 Need-Driven Discovery

**Approach:** Score 7 providers across 7 distinct use cases
**File:** [01-discovery/S3-need-driven/approach.md](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S3-need-driven/approach.md)

**Use Case Scoring:**
- [Use Case 1: Solo Python/Flask Developer](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S3-need-driven/use-case-1-solo-python-flask.md) - PythonAnywhere wins (46/50)
- [Use Case 2: Docker-Experienced Startup](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S3-need-driven/use-case-2-docker-multi-language.md) - Railway wins (45/50)
- [Use Case 3: Serverless Functions](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S3-need-driven/use-case-3-serverless-functions.md) - Vercel/Cloudflare win (46/50)
- [Use Case 4: Static + Backend API](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S3-need-driven/use-case-4-static-backend-api.md) - Vercel wins (47/50)
- [Use Case 5: Global Edge Deployment](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S3-need-driven/use-case-5-global-edge-deployment.md) - Cloudflare Workers wins (48/50)
- [Use Case 6: Hobbyist Free Tier](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S3-need-driven/use-case-6-hobbyist-free-tier.md) - Vercel wins (46/50)
- [Use Case 7: Production SaaS (10-50 customers)](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S3-need-driven/use-case-7-production-saas.md) - Fly.io wins (42/50), PythonAnywhere competitive (38/50)

**Recommendation:** [01-discovery/S3-need-driven/recommendation.md](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S3-need-driven/recommendation.md)

**Key Finding:** No single "best" provider. PythonAnywhere dominates one niche (solo Python developers), loses dramatically in all other use cases. Docker-native PaaS (Railway, Render, Fly.io) wins most scenarios.

---

### S4 Strategic Discovery

**Approach:** 5-10 year viability analysis, acquisition risk, exit timelines
**File:** [01-discovery/S4-strategic/approach.md](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S4-strategic/approach.md)

**Provider Viability Analysis:**
- [Render Viability](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S4-strategic/provider-render-viability.md) - 72/100 score, 4-7 year safe window, 70% acquisition risk by 2029-2032
- [Railway Viability](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S4-strategic/provider-railway-viability.md) - 70/100 score, Series A exit 2029-2031, 65% acquisition risk
- [Fly.io Viability](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S4-strategic/provider-flyio-viability.md) - 68/100 score, HIGHEST acquisition risk (75%), edge computing hot M&A sector
- [Heroku Viability](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S4-strategic/provider-heroku-viability.md) - 55/100 score, already in decline phase, 50% divestiture risk 2027-2030
- [PythonAnywhere Viability](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S4-strategic/provider-pythonanywhere-viability.md) - 68/100 score, tied to Anaconda exit 2029-2032, 60% repricing/shutdown risk
- [Vercel Viability](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S4-strategic/provider-vercel-viability.md) - 58/100 score (wrong tech stack for QRCards), IPO track 2026-2028

**Strategic Analysis:**
- [Acquisition Risk](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S4-strategic/acquisition-risk.md) - ALL PaaS providers face exit events within 5-10 years, no "forever" choice
- [Lock-In Analysis](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S4-strategic/lock-in-analysis.md) - Render/Railway 20-25/100 (low), Fly.io 40/100 (moderate), Heroku 45/100 (high)
- [Build vs Buy](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S4-strategic/build-vs-buy.md) - PaaS vs DIY VPS break-even at $150-200/month hosting
- [Migration Paths](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S4-strategic/migration-paths.md) - Docker-native: 4-8 hour migration, Python-native: similar portability

**Recommendation:** [01-discovery/S4-strategic/recommendation.md](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/01-discovery/S4-strategic/recommendation.md)

**Key Finding:** Accept impermanence. No PaaS provider is permanent (VC exit cycles, acquisitions). Choose based on low lock-in + current fit, NOT false promises of stability. Render/PythonAnywhere: 4-7 year safe window, easy migration when needed.

---

## Key Findings Summary

### Top 3 Providers (General Purpose)

**1. Render** - Modern PaaS Champion
- Popularity: #1 Heroku alternative post-2022
- Free tier: 750 hours/month, best in market
- Pricing: $7-25/month starter/production
- Lock-in: 20/100 (LOW) - Docker-native
- Exit timeline: 2029-2032 (4-7 year safe window)
- Best for: Mid-sized Flask apps, Heroku migrations, modern workflows

**2. Railway** - Developer Experience Leader
- Popularity: #4 overall, strong community
- Pricing: $5-20/month usage-based
- Lock-in: 25/100 (LOW) - Docker-native
- Exit timeline: 2029-2031
- Best for: Startups, teams, rapid iteration

**3. Fly.io** - Performance Champion
- Popularity: #5 overall, performance-focused
- Performance: 34ms (vs 600ms Heroku)
- Pricing: $10-30/month
- Lock-in: 40/100 (MODERATE) - edge-specific features
- Exit timeline: 2028-2030 (HIGHEST acquisition risk)
- Best for: Global distribution, high performance, multi-region

### PythonAnywhere Position

**Market Ranking:** #7-8 overall, #1-2 for Python beginners specifically

**Strengths:**
- Python-specialized (no Docker needed)
- Excellent beginner experience (15-minute deploy)
- Maintains free tier (competitive advantage 2024-2025)
- Low-friction entry for Python learners
- Lowest cost: $5/month production

**Weaknesses:**
- Not competing in mainstream PaaS market
- Viewed as "educational" rather than "production-ready"
- Limited modern deployment practices (no git-push auto-deploy, weak CI/CD)
- Outbound Internet restrictions on free/lower tiers
- Not suitable for scaling or microservices

**Acquisition Status:** Acquired by Anaconda (June 2022)
- Safe window: 2025-2029 (Anaconda growth phase)
- Risk window: 2029-2032 (tied to Anaconda exit)
- Acquisition risk: 60% (repricing or shutdown when Anaconda exits)

**Best Fit Use Case:** Solo Python developer, 0-50 customers, simple monolithic app, no Docker expertise

---

## QRCards Strategic Assessment

**Location:** [/home/ivanadamin/spawn-solutions/applications/qrcards/2.050_PAAS_STRATEGIC_ASSESSMENT.md](/home/ivanadamin/spawn-solutions/applications/qrcards/2.050_PAAS_STRATEGIC_ASSESSMENT.md)

**Current State:**
- Platform: PythonAnywhere ($19.25/month for 4 web apps)
- Deployment: MANUAL (git pull + reload, no auto-deploy)
- Staging: NONE (test in production)
- Database: SQLite (PostgreSQL migration planned 6-12 months)
- CI/CD: NONE (planned GitHub Actions)
- Customers: 7 paying customers

**Recommendation:** Migrate to Render within 30 days

**Rationale:**
- Docker experience already exists (not constrained by PythonAnywhere's simplicity advantage)
- Manual deployment blocking planned improvements (CI/CD, staging)
- PostgreSQL migration planned (Render includes free Postgres, PythonAnywhere charges $7/month extra)
- 7 paying customers justify $14/month vs $5/month investment
- Migration effort: 8-16 hours (one weekend)
- Net cost: $2/month more for dramatically better developer experience

**Migration Timeline:**
- Week 1: Dockerfile + Render staging (2-4 hours)
- Week 2: Deploy staging + database migration (4-8 hours)
- Week 3: Production cutover (2-4 hours)
- Total: 8-16 hours

**Alternative Considered:** Railway (equally good, similar pricing)

**NOT Recommended:** Stay on PythonAnywhere (blocks CI/CD, PostgreSQL, staging environments)

---

## Cross-Reference Resources

### Related Experiments
- [2.030 Database Services](/home/ivanadamin/spawn-solutions/experiments/2.030-database-services/) - PostgreSQL provider analysis
- [2.040 Analytics](/home/ivanadamin/spawn-solutions/applications/qrcards/2.040+2.041_ANALYTICS_STRATEGIC_ASSESSMENT.md) - Application analytics for PaaS-hosted apps
- [2.042 Application Monitoring](/home/ivanadamin/spawn-solutions/applications/qrcards/2.042_APPLICATION_MONITORING_STRATEGIC_ASSESSMENT.md) - Error tracking, performance monitoring
- [2.045 Uptime Monitoring](/home/ivanadamin/spawn-solutions/applications/qrcards/2.045_UPTIME_MONITORING_STRATEGIC_ASSESSMENT.md) - Health checks, availability tracking

### QRCards Infrastructure
- [Infrastructure Architecture Paths](/home/ivanadamin/spawn-solutions/applications/qrcards/INFRASTRUCTURE_ARCHITECTURE_PATHS.md) - Distributed vs centralized deployment analysis
- [Service Subtraction Strategy](/home/ivanadamin/spawn-solutions/applications/qrcards/2.001+2.020_SERVICE_SUBTRACTION_STRATEGY.md) - Avoiding unnecessary PaaS bundle features

---

## Discovery Methodology Summary

**S1 Rapid:** Popularity-first (HN, Reddit, developer surveys) → Top 3 identified
**S2 Comprehensive:** Technical deep dive → Documentation, deployment quality, pricing models
**S3 Need-Driven:** Use case scoring (7 scenarios × 7 providers = 49 evaluations) → Best fit per scenario
**S4 Strategic:** 5-10 year viability, acquisition risk, exit timelines → Accept impermanence strategy

**Total Analysis:** 10 providers, 4 methodologies, 50+ documents, 100+ hours research

**Outcome:** Render (primary) or PythonAnywhere (alternative) for QRCards. Both have 4-7 year safe window, low lock-in (20-25/100), easy migration when circumstances change.

---

**Discovery Status:** COMPLETE
**Next Action:** QRCards migration to Render (8-16 hours) OR stay on PythonAnywhere with awareness of 2029-2032 exit risk
**Strategic Principle:** Accept impermanence, build portably, migrate painlessly when needed
