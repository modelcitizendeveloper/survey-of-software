# Backend-as-a-Service (BaaS) Discovery - Table of Contents

**Experiment:** 2.200 Backend-as-a-Service (BaaS)
**Date:** October 10, 2025
**Providers Evaluated:** 6 (Supabase, Firebase, PocketBase, Appwrite, Xata, Nhost)

---

## Quick Start

**New to BaaS?** Start here:
1. [BAAS_EXPLAINER.md](#educational-guide) - What is BaaS? When to use it?
2. [DISCOVERY_SYNTHESIS.md](#discovery-synthesis) - Executive summary and top recommendations
3. [S1 Recommendation](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S1-rapid/recommendation.md) - Provider rankings and decision matrix

**Need specific answers?**
- **Which provider should I choose?** → [S1 Recommendation](#s1-rapid-discovery)
- **How much will it cost at scale?** → [S2 Pricing Matrix](#s2-comprehensive-discovery)
- **What's the lock-in severity?** → [S2 Lock-In Analysis](#s2-comprehensive-discovery)
- **Best for my use case?** → [S3 Need-Driven Discovery](#s3-need-driven-discovery)
- **Is this provider safe long-term?** → [S4 Strategic Discovery](#s4-strategic-discovery)

---

## Discovery Structure

### Educational Guide
- [BAAS_EXPLAINER.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/BAAS_EXPLAINER.md) - Comprehensive BaaS educational guide
  - What is BaaS? When to use it?
  - Key concepts (auto-generated APIs, RLS, real-time, edge functions)
  - Provider categories (SQL vs NoSQL, managed vs self-hosted)
  - Cost models and lock-in considerations
  - Decision framework (BaaS vs PaaS)

### Discovery Synthesis
- [DISCOVERY_SYNTHESIS.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/DISCOVERY_SYNTHESIS.md) - High-level findings across all discovery phases
  - Top 3 provider recommendations
  - Critical decision factors (SQL vs NoSQL, lock-in, pricing, features)
  - Use case recommendations
  - BaaS vs PaaS decision criteria
  - Strategic recommendations and migration playbook

---

## S1 Rapid Discovery (Popularity-First)

**Goal:** Identify most popular BaaS providers with rapid market analysis

**Files:**
- [approach.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S1-rapid/approach.md) - Methodology and key findings summary
- [recommendation.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S1-rapid/recommendation.md) - **START HERE** - Provider rankings and decision matrix

**Provider Profiles:**
1. [provider-supabase.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S1-rapid/provider-supabase.md) - PostgreSQL, open-source, $5B valuation (Rank #1)
2. [provider-firebase.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S1-rapid/provider-firebase.md) - Google-backed, Firestore NoSQL, most mature (Rank #2)
3. [provider-pocketbase.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S1-rapid/provider-pocketbase.md) - Single binary, SQLite, self-hosted (Rank #3)
4. [provider-appwrite.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S1-rapid/provider-appwrite.md) - Open-source, multi-language functions, NoSQL (Rank #4)
5. [provider-xata.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S1-rapid/provider-xata.md) - PostgreSQL + Elasticsearch, database branching (Rank #5)
6. [provider-nhost.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S1-rapid/provider-nhost.md) - Hasura GraphQL, PostgreSQL (Rank #6)

**Key Findings:**
- Supabase is best overall (PostgreSQL, open-source, balanced lock-in: 75/100)
- Firebase best for mobile (offline sync, high lock-in: 85/100)
- PocketBase best for MVPs (simplest, lowest lock-in: 50/100)
- Lock-in ranges from 50/100 (PocketBase) to 85/100 (Firebase)

---

## S2 Comprehensive Discovery (Deep Technical Analysis)

**Goal:** Deep-dive pricing, features, and lock-in assessment

**Files:**
- [approach.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S2-comprehensive/approach.md) - Methodology for deep analysis
- [pricing-matrix.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S2-comprehensive/pricing-matrix.md) - **CRITICAL** - Cost at three scales (hobby, growth, production)
- [feature-matrix.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S2-comprehensive/feature-matrix.md) - Database, auth, storage, real-time, functions comparison
- [lock-in-analysis.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S2-comprehensive/lock-in-analysis.md) - **CRITICAL** - Migration time estimates, lock-in severity

**Key Findings:**
- Firebase costs explode at scale ($600/month for 1B reads due to per-read/write pricing)
- Supabase affordable until $200-500/month, then self-hosting cheaper
- PocketBase cheapest ($5-50/month VPS) but hits SQLite scaling limits
- Lock-in: Firebase (85/100, 200-400 hours migration), Supabase (75/100, 80-120 hours), PocketBase (50/100, 60-100 hours)
- SQL databases (PostgreSQL, SQLite) have EASY migration (8-16 hours). NoSQL (Firestore) has VERY HARD migration (80-200 hours)

---

## S3 Need-Driven Discovery (Use Case Scoring)

**Goal:** Score providers across distinct use cases

**Files:**
- [approach.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S3-need-driven/approach.md) - Methodology and scoring system
- [use-case-1-mvp-speed.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S3-need-driven/use-case-1-mvp-speed.md) - Solo founder, launch in 2 weeks (Supabase 93/100)

**Use Cases (7 total):**
1. **MVP Speed** - Supabase (93/100), Firebase (90/100), PocketBase (85/100)
2. **Mobile-First** - Firebase (90/100) for offline sync, Supabase (93/100) for SQL
3. **Real-Time Collaboration** - Supabase (93/100), Firebase (90/100)
4. **Open-Source Self-Host** - PocketBase (85/100) easiest, Appwrite (80/100) more features
5. **PostgreSQL Preference** - Supabase (93/100), Nhost (70/100) for GraphQL
6. **Cost Optimization** - PocketBase (85/100) self-host, Xata (82/100) generous free tier
7. **Enterprise Requirements** - Firebase (90/100) SOC 2/HIPAA, Supabase Enterprise (93/100)

**Key Findings:**
- Supabase wins 5 out of 7 use cases (general-purpose strength)
- Firebase wins mobile-first (offline sync unmatched)
- PocketBase wins cost optimization (self-host, $0-12/month)

---

## S4 Strategic Discovery (Viability and Risk Analysis)

**Goal:** Assess long-term viability, acquisition risk, migration paths

**Files:**
- [approach.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S4-strategic/approach.md) - Methodology for viability assessment

**Provider Viability Assessments:**
1. **provider-supabase-viability.md** - $5B valuation, IPO trajectory, 8-10 years safe
2. **provider-firebase-viability.md** - Google-owned, 10+ years safe, most stable
3. **provider-appwrite-viability.md** - VC-backed $27M, 2026-2029 acquisition window
4. **provider-pocketbase-viability.md** - No company, single maintainer, 3-5 years uncertain

**Cross-Cutting Strategic Analysis:**
1. **acquisition-risk.md** - ALL VC-backed BaaS will be acquired or IPO within 5-10 years
2. **lock-in-severity.md** - High lock-in = forced migration expensive (200-400 hours)
3. **migration-paths.md** - BaaS → PaaS, BaaS → self-hosted, BaaS → different BaaS

**Key Findings:**
- Firebase safest long-term (Google-owned, 10+ years safe)
- Supabase safe 5-10 years ($5B valuation, IPO trajectory)
- VC-backed providers (Appwrite, Xata, Nhost) likely acquired 2026-2029
- PocketBase uncertain (no company, single maintainer, but open-source)
- Recommendation: Choose open-source BaaS (Supabase, PocketBase) for exit strategy

---

## Summary Charts

### Provider Comparison (At a Glance)

| Provider | Rank | Lock-In | Migration Time | Best For | Cost (100K MAU) |
|----------|------|---------|----------------|----------|-----------------|
| **Supabase** | #1 | 75/100 | 80-120 hours | General purpose, web/mobile | $200-400/mo |
| **Firebase** | #2 | 85/100 | 200-400 hours | Mobile apps, offline sync | $600-1,200/mo |
| **PocketBase** | #3 | 50/100 | 60-100 hours | MVPs, self-hosting, low budget | $50-100/mo |
| **Appwrite** | #4 | 70/100 | 120-220 hours | Self-hosting, multi-language | $100-300/mo |
| **Xata** | #5 | 65/100 | 100-180 hours | Database + search, TypeScript | $50-150/mo |
| **Nhost** | #6 | 70/100 | 150-250 hours | GraphQL-first, Hasura | $200-400/mo |

### Decision Flow

```
Do you need mobile offline sync?
├─ YES → Firebase (accept 85/100 lock-in)
└─ NO → Continue...

Do you need SQL or NoSQL?
├─ SQL → Supabase, Nhost, Xata, PocketBase
└─ NoSQL → Firebase, Appwrite

Budget $0-50/month?
├─ YES → PocketBase (self-host $5-12/mo)
└─ NO → Managed cloud (Supabase, Firebase)

Need multi-language functions (Python, Go)?
├─ YES → Appwrite or PaaS (Render, Railway)
└─ NO → Supabase (TypeScript functions)

Need integrated search?
├─ YES → Xata (Elasticsearch built-in)
└─ NO → Supabase + Algolia/Typesense

GraphQL-first?
├─ YES → Nhost (Hasura auto-generated)
└─ NO → Supabase (REST-first)

Default: Supabase (best overall)
```

---

## File Navigation

### By Discovery Phase
- **S1 Rapid Discovery:** 7 files (approach + 6 providers + recommendation)
- **S2 Comprehensive Discovery:** 4 files (approach + pricing + features + lock-in)
- **S3 Need-Driven Discovery:** 2+ files (approach + use cases)
- **S4 Strategic Discovery:** 2+ files (approach + viability assessments)

### By Document Type
- **Approach Files:** Methodology for each discovery phase (S1, S2, S3, S4)
- **Provider Profiles:** Deep-dives on each provider (S1)
- **Comparison Matrices:** Pricing, features, lock-in (S2)
- **Use Case Scoring:** Provider scores per use case (S3)
- **Viability Assessments:** Long-term provider outlook (S4)
- **Educational Guides:** BAAS_EXPLAINER.md
- **Synthesis:** DISCOVERY_SYNTHESIS.md (high-level findings)

### By Research Question
**"Which provider should I choose?"**
→ [S1 recommendation.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S1-rapid/recommendation.md)

**"How much will it cost?"**
→ [S2 pricing-matrix.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S2-comprehensive/pricing-matrix.md)

**"What's the lock-in severity?"**
→ [S2 lock-in-analysis.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S2-comprehensive/lock-in-analysis.md)

**"Best for mobile apps?"**
→ [S3 use-case-2-mobile-first.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S3-need-driven/approach.md)

**"Is this provider safe long-term?"**
→ [S4 provider viability assessments](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/01-discovery/S4-strategic/approach.md)

**"What is BaaS?"**
→ [BAAS_EXPLAINER.md](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/BAAS_EXPLAINER.md)

---

## Research Methodology (MPSE Framework)

This discovery follows the spawn-solutions MPSE framework:

**M** - Multi-Perspective: Evaluated 6 providers from different angles (popularity, features, use cases, strategy)
**P** - Phased: 4 discovery phases (S1 rapid, S2 comprehensive, S3 need-driven, S4 strategic)
**S** - Systematic: Consistent scoring and analysis across all providers
**E** - Explicit: Transparent methodology, scoring criteria, and decision factors

**Discovery Duration:** ~2 hours of research and synthesis
**Output:** 20+ markdown files with comprehensive analysis

---

## Key Takeaways

1. **Supabase is the default choice** for 80% of projects (PostgreSQL, balanced lock-in, excellent DX)
2. **Firebase only for mobile apps** with offline sync requirements (accept high lock-in: 85/100)
3. **PocketBase for MVPs and self-hosting** (simplest, lowest lock-in: 50/100, migrate when scaling)
4. **SQL migration is 10x easier** than NoSQL migration (8-16 hours vs 80-200 hours)
5. **All BaaS have lock-in** (50-85/100), plan for eventual migration when costs >$500/month

---

## Contact and Feedback

This discovery is part of the spawn-solutions research framework (experiment 3.400).

Related experiments:
- [2.050 Platform-as-a-Service (PaaS)](/home/ivanadamin/spawn-solutions/experiments/3.050-platform-as-a-service/) - Comparison with BaaS

**Last Updated:** October 10, 2025
**Maintainer:** spawn-solutions research framework
