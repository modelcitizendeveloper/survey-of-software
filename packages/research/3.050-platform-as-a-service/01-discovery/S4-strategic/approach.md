# S4 Strategic Discovery Methodology

**Experiment:** 3.050 Platform-as-a-Service (PaaS)
**Phase:** Strategic Analysis
**Date:** 2025-10-09
**Duration:** 15-18 minutes estimated

## Objective

Analyze long-term viability, acquisition risk, vendor lock-in, and strategic implications of PaaS choices for QRCards. Answer the critical question: **Should QRCards commit to PythonAnywhere long-term or plan migration?**

## Strategic Time Horizon

**5-10 year outlook** - Think beyond immediate deployment needs to business sustainability.

## Analysis Framework

### 1. Vendor Viability Assessment

For each major PaaS provider, assess:

**Funding & Ownership**
- Funding status: Bootstrapped / VC-backed / Public company / PE-owned
- Revenue model: Sustainable pricing or VC-subsidized customer acquisition
- Market position: Growing / stable / declining
- Years in operation / company maturity

**Risk Factors**
- Acquisition risk: Likelihood of being acquired in next 3-5 years (0-100%)
- Pricing stability: Historical price changes, free tier erosion
- Platform continuity: Risk of service discontinuation or radical pivot

**Market Position**
- Market share in target segment (Python web apps, Django specifically)
- Competitive moat: What makes them defensible?
- Innovation rate: New features, platform evolution

### 2. Lock-In Analysis

**Migration Difficulty Assessment**
- Platform-specific APIs and tooling
- Data export capabilities
- Configuration portability (Docker, WSGI, env vars)
- Estimated migration time: hours / days / weeks

**Lock-In Severity Score (0-100%)**
- 0-25%: Easy migration (standardized deployment, minimal vendor-specific code)
- 26-50%: Moderate effort (some reconfiguration, testing required)
- 51-75%: Significant effort (platform-specific features in use)
- 76-100%: Severe lock-in (proprietary APIs, data migration complexity)

### 3. Build vs Buy Economics

**DIY VPS Comparison**
- Setup time: Initial deployment pipeline creation
- Monthly cost: Infrastructure + maintenance time value
- Ongoing maintenance burden
- Break-even analysis: At what scale does DIY make sense?

**PaaS Value Proposition**
- Time saved on DevOps
- Included features (SSL, monitoring, backups, scaling)
- Hidden costs (egress fees, add-ons, scaling costs)

### 4. Acquisition Risk Pattern Analysis

**Historical Context**
- Recent PaaS acquisitions (Heroku → Salesforce, others)
- Post-acquisition outcomes (price increases, feature stagnation, shutdowns)
- VC-backed exit timelines (typical 7-10 year fund cycle)

**Risk Indicators**
- Recent funding rounds (signals 5-7 year exit timeline)
- Company size (small companies more likely acquisition targets)
- Strategic buyers in market (who would acquire?)

## Providers Under Analysis

**Current Provider (Deep Dive)**
1. PythonAnywhere - Need comprehensive viability assessment

**Alternative PaaS**
2. Heroku - Already acquired (Salesforce), baseline for post-acquisition analysis
3. Render - VC-backed, modern competitor
4. Railway - VC-backed, developer-focused
5. Fly.io - VC-backed, edge computing focus
6. Vercel - VC-backed, recent large funding round

**Control Group**
- DIY VPS (DigitalOcean, Linode, Vultr) - Full control, maximum effort

## Research Sources

- Company websites (About, Pricing history, Blog for announcements)
- Crunchbase / PitchBook (funding data)
- HN / Reddit (community sentiment, incident reports)
- Pricing page archives (Wayback Machine for historical pricing)
- Documentation (platform-specific features, migration guides)
- Financial news (acquisition rumors, funding announcements)

## Deliverables

1. **approach.md** (this file) - Methodology documentation
2. **provider-[name]-viability.md** (6-8 files) - Individual provider assessments
3. **acquisition-risk.md** - Cross-provider risk comparison matrix
4. **lock-in-analysis.md** - Migration complexity by provider
5. **build-vs-buy.md** - DIY deployment economics
6. **migration-paths.md** - Specific migration effort estimates from PythonAnywhere
7. **recommendation.md** - Strategic guidance for QRCards

## Key Strategic Questions

1. **PythonAnywhere Sustainability**: Is bootstrapped = stable or stagnant? Are they innovating or coasting?

2. **VC Exit Risk**: Are Render, Railway, Fly.io, Vercel on 5-7 year exit timelines that will trigger price increases?

3. **Simplicity vs Flexibility**: Should QRCards stay simple (PythonAnywhere) or invest in Docker/migration prep?

4. **Exit Cost**: What's the worst-case scenario if PythonAnywhere is acquired, raises prices 10x, or shuts down?

5. **Heroku Case Study**: What happened post-Salesforce acquisition? Pricing? Innovation? Quality?

## Success Criteria

Strategic discovery is complete when:
- Viability score (0-100) assigned to each provider
- Acquisition risk ranking established
- Migration effort quantified (hours/days/weeks)
- Clear recommendation for QRCards' next 5 years
- Contingency plans documented

## Analysis Process

1. Start with PythonAnywhere deep dive (current provider)
2. Research VC-backed alternatives (understand exit pressures)
3. Analyze Heroku as post-acquisition case study
4. Assess DIY VPS economics (control option)
5. Synthesize into risk matrix and recommendations
6. Document migration paths and effort estimates

---

**Note**: This is strategic analysis, not just technical comparison. Focus on business sustainability, not feature lists.
