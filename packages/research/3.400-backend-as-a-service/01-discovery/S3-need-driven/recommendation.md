# S3 Need-Driven Discovery - Recommendation

**Experiment:** 2.200 Backend-as-a-Service (BaaS)
**Phase:** S3 Need-Driven (Use Case Analysis)
**Date:** October 10, 2025
**Use Cases Analyzed:** 6

---

## Executive Summary

After analyzing 6 providers across 6 real-world use cases, clear patterns emerge showing which BaaS wins for specific scenarios.

### Use Case Winners Summary

| Use Case | Winner | Score | Key Reason |
|----------|--------|-------|------------|
| **1. MVP Speed** | Supabase | 93/100 | PostgreSQL + real-time + 60-min first deploy |
| **2. Mobile-First** | Firebase | 48/50 | Best mobile SDKs + automatic offline sync |
| **3. Real-Time Collaboration** | Supabase | 46/50 | 50-100ms latency + presence channels |
| **4. Self-Hosting** | PocketBase | 46/50 | Single binary + $5/month + MIT license |
| **5. SQL Database** | Supabase | 48/50 | PostgreSQL + joins + easy migration |
| **6. Zero Budget** | PocketBase | 48/50 | $5/month VPS + lowest lock-in (50/100) |

---

## Provider Performance Across Use Cases

### Supabase: 3 Wins (MVP, Real-Time, SQL)

**Dominates:**
- Web apps requiring SQL database
- Real-time collaboration (chat, dashboards)
- Startup MVPs (fast deployment, generous free tier)

**Strengths:**
- PostgreSQL (standard SQL, joins, transactions)
- Real-time subscriptions (50-100ms latency)
- Excellent developer experience
- Moderate lock-in (75/100, easier migration than Firebase)

**When to Choose:** 80% of web/mobile app projects

**Lock-In:** 75/100 (MODERATE)
**Viability:** 85/100 (HIGH - $5B valuation, IPO trajectory)

---

### Firebase: 1 Win (Mobile-First)

**Dominates:**
- Mobile apps (iOS/Android) requiring offline sync
- Real-time mobile apps (chat, collaboration)

**Strengths:**
- Best mobile SDKs (Swift, Kotlin, Flutter)
- Automatic offline persistence (local caching, auto-sync)
- Comprehensive mobile platform (FCM, analytics, crashlytics)
- Google-backed (safest long-term, 90/100 viability)

**When to Choose:** Mobile-first apps ONLY (accept 85/100 lock-in for offline sync)

**Lock-In:** 85/100 (VERY HIGH - highest of all BaaS)
**Viability:** 90/100 (VERY HIGH - Google-backed, profitable)

---

### PocketBase: 2 Wins (Self-Hosting, Zero Budget)

**Dominates:**
- Self-hosting (data sovereignty, GDPR)
- Zero-budget MVPs (indie hackers, side projects)

**Strengths:**
- Simplest deployment (single binary, 2-minute setup)
- Lowest cost ($5/month VPS, MIT license)
- Lowest lock-in (50/100, standard SQL + REST API)
- SQLite (full SQL, easy migration to PostgreSQL)

**When to Choose:** MVPs, self-hosting, cost-conscious indies

**Limitation:** SQLite scaling (not for >10K concurrent users)

**Lock-In:** 50/100 (LOWEST - easiest migration)
**Viability:** 50/100 (MODERATE - single maintainer risk)

---

### Appwrite, Nhost, Xata: 0 Wins

**Appwrite (70/100 lock-in, 65/100 viability):**
- Niche: Multi-language functions (Python, Go, Ruby)
- Best for: Flutter apps requiring Python ML backend
- Why no wins: Complexity (Docker), NoSQL (harder migration), higher cost vs PocketBase

**Nhost (70/100 lock-in, 55/100 viability):**
- Niche: GraphQL-first projects
- Best for: Hasura users, Apollo Client projects
- Why no wins: GraphQL adds complexity, smaller community, not best at any category

**Xata (65/100 lock-in, 60/100 viability):**
- Niche: Database + integrated search
- Best for: E-commerce, content platforms
- Why no wins: No real-time, no auth (must integrate separately), TypeScript-only

---

## Use Case Recommendations

### Use Case 1: Startup MVP (Launch Fast)

**Winner:** Supabase (93/100)

**Why:** PostgreSQL + real-time + generous free tier + 60-minute first deployment

**Alternatives:**
- Firebase (90/100) if mobile-first
- PocketBase (85/100) if zero budget ($5/month)

**Cost:** $0-25/month (free tier → Pro $25/month)

---

### Use Case 2: Mobile App (iOS/Android)

**Winner:** Firebase (48/50)

**Why:** Best mobile SDKs + automatic offline sync + comprehensive mobile platform

**Alternatives:**
- Supabase (36/50) if can implement offline sync manually (20-50 hours)
- Appwrite (33/50) if Flutter + self-hosting

**Cost:** $0-100/month (free tier → Blaze pay-as-you-go)

**WARNING:** Accept 85/100 lock-in (migration 200-400 hours) ONLY if offline sync critical

---

### Use Case 3: Real-Time Collaboration

**Winner:** Supabase (46/50)

**Why:** 50-100ms latency + presence channels + broadcast + database subscriptions

**Alternatives:**
- Firebase (40/50) if mobile real-time
- Nhost (38/50) if GraphQL subscriptions

**Cost:** $25/month (Pro tier for 500 concurrent connections)

---

### Use Case 4: Self-Hosting Requirement

**Winner:** PocketBase (46/50)

**Why:** Single binary + $5/month VPS + MIT license + 2-minute setup

**Alternatives:**
- Appwrite (37/50) if need enterprise features (teams, multi-language functions)
- Supabase (32/50) if need PostgreSQL at scale (10+ Docker containers)

**Cost:** $5-12/month (VPS only)

---

### Use Case 5: SQL Database Required

**Winner:** Supabase (48/50)

**Why:** PostgreSQL + joins + transactions + easy migration to self-hosted PostgreSQL

**Alternatives:**
- Nhost (44/50) if GraphQL-first
- Xata (43/50) if need integrated search

**Cost:** $0-25/month (free tier → Pro $25/month)

**AVOID:** Firebase (5/50), Appwrite (5/50) - NoSQL only, no joins

---

### Use Case 6: Zero-Budget MVP

**Winner:** PocketBase (48/50)

**Why:** $5/month VPS + unlimited users/storage + lowest lock-in (50/100)

**Alternatives:**
- Supabase (43/50) if prefer managed cloud (no DevOps)
- Firebase (36/50) if mobile offline sync (accept 85/100 lock-in)

**Cost:** $5/month (PocketBase self-hosted) or $0/month (Supabase free tier)

---

## Decision Framework

### Step 1: Identify Your Primary Need

```
┌─────────────────────────────────────────────────────┐
│ What is your PRIMARY requirement?                  │
└────────────┬────────────────────────────────────────┘
             │
             ├─ Mobile app (iOS/Android) with offline sync
             │  → Firebase (48/50)
             │
             ├─ SQL database (joins, complex queries)
             │  → Supabase (48/50)
             │
             ├─ Real-time collaboration (chat, live editing)
             │  → Supabase (46/50)
             │
             ├─ Self-hosting (data sovereignty, GDPR)
             │  → PocketBase (46/50)
             │
             ├─ Zero budget ($0-12/month)
             │  → PocketBase (48/50)
             │
             └─ General purpose (web/mobile app, fast MVP)
                → Supabase (93/100)
```

---

### Step 2: Assess Lock-In Tolerance

```
┌─────────────────────────────────────────────────────┐
│ How important is low lock-in?                      │
└────────────┬────────────────────────────────────────┘
             │
             ├─ CRITICAL (must migrate easily)
             │  → PocketBase (50/100 lock-in)
             │  → Supabase (75/100 lock-in)
             │  → AVOID Firebase (85/100 lock-in)
             │
             ├─ MODERATE (accept lock-in for features)
             │  → Supabase (75/100 lock-in)
             │  → Appwrite (70/100 lock-in)
             │  → Nhost (70/100 lock-in)
             │
             └─ LOW (willing to accept high lock-in)
                → Firebase (85/100 lock-in)
                → ONLY if mobile offline sync critical
```

---

### Step 3: Consider Cost at Scale

```
┌─────────────────────────────────────────────────────┐
│ What is your expected scale?                       │
└────────────┬────────────────────────────────────────┘
             │
             ├─ 1K-5K users (MVP, prototype)
             │  → PocketBase ($5/month)
             │  → Supabase ($0 free tier)
             │  → Firebase ($0 free tier)
             │
             ├─ 10K-50K users (growing startup)
             │  → Supabase ($25/month Pro)
             │  → PocketBase ($12/month VPS)
             │  → Firebase ($50-100/month)
             │
             ├─ 100K-500K users (scaling product)
             │  → Supabase ($100-400/month)
             │  → Self-hosted PostgreSQL ($50-200/month)
             │  → Firebase ($200-600/month)
             │
             └─ >500K users (high scale)
                → Self-hosted PostgreSQL ($200-500/month)
                → Supabase Enterprise (custom pricing)
                → AVOID Firebase (costs explode)
```

---

## Red Flags: Avoid These Combinations

1. **Firebase for SQL-heavy app** → Choose Supabase (PostgreSQL, joins)
2. **PocketBase for >10K concurrent users** → Choose Supabase (PostgreSQL scales better)
3. **Firebase if lock-in is concern** → Choose Supabase (75/100 vs 85/100)
4. **Supabase for multi-language functions** → Choose Appwrite (Python, Go, Ruby)
5. **Xata for real-time apps** → Choose Supabase (Xata has no real-time)
6. **Firebase for cost-sensitive** → Choose Supabase (costs explode at scale)

---

## Lock-In Comparison

| Provider | Lock-In Score | Migration Time | Migration Cost |
|----------|---------------|----------------|----------------|
| PocketBase | 50/100 | 60-100 hours | $6K-10K |
| Xata | 65/100 | 100-180 hours | $10K-18K |
| Appwrite | 70/100 | 120-220 hours | $12K-22K |
| Nhost | 70/100 | 150-250 hours | $15K-25K |
| Supabase | 75/100 | 80-120 hours | $8K-12K |
| Firebase | 85/100 | 200-400 hours | $20K-40K |

**Key Insight:** PocketBase has lowest lock-in (50/100), Firebase has highest (85/100). All BaaS have moderate-high lock-in; plan for migration when scaling or if acquired.

---

## Cost Comparison (50K Users)

| Provider | Monthly Cost | Breakdown |
|----------|--------------|-----------|
| **PocketBase** | $12 | Hetzner CX21 VPS (2 CPU, 4 GB RAM) |
| **Supabase** | $25-50 | Pro $25 + small overages |
| **Xata** | $30-50 | Usage-based, no per-request charges |
| **Nhost** | $25-50 | Similar to Supabase |
| **Appwrite** | $15-30 | Appwrite Cloud Pro $15 + overages |
| **Firebase** | $100-200 | Per-read/write charges explode |

**Key Insight:** PocketBase cheapest ($12/month self-hosted), Firebase most expensive ($100-200/month per-read pricing).

---

## Viability Comparison (5-10 Year Outlook)

| Provider | Viability | Acquisition Risk | Safe Until |
|----------|-----------|------------------|------------|
| **Firebase** | 90/100 | None (Google-owned) | 2035+ (10+ years safe) |
| **Supabase** | 85/100 | Low (IPO trajectory) | 2030-2035 (8-10 years safe) |
| **Appwrite** | 65/100 | Moderate (VC-backed) | 2027-2029 (3-5 years uncertain) |
| **Xata** | 60/100 | Moderate (early-stage) | 2027-2029 (3-5 years uncertain) |
| **Nhost** | 55/100 | Moderate (small team) | 2027-2029 (3-5 years uncertain) |
| **PocketBase** | 50/100 | None (single maintainer) | 2027-2029 (3-5 years uncertain) |

**Key Insight:** Firebase safest long-term (Google-backed), Supabase safe 5-10 years (IPO trajectory), others uncertain 3-5 years (VC exit window or single maintainer risk).

---

## Final Recommendations

### For 80% of Projects: Supabase

**Use Supabase as default choice** for web/mobile apps needing SQL database, real-time features, and fast MVP deployment.

**Why:** Best balance of speed, flexibility, lock-in (75/100), and viability (85/100, $5B valuation).

---

### For Mobile Apps: Firebase

**Use Firebase ONLY for mobile apps** (iOS/Android) requiring automatic offline sync.

**Why:** Best mobile SDKs, offline persistence built-in, comprehensive mobile platform.

**Accept:** 85/100 lock-in (highest) in exchange for mobile advantages.

---

### For MVPs and Self-Hosting: PocketBase

**Use PocketBase for zero-budget MVPs** and self-hosting requirements.

**Why:** Lowest cost ($5/month), lowest lock-in (50/100), simplest deployment (2 minutes).

**Limitation:** SQLite scaling (migrate to Supabase when >10K concurrent users).

---

### For Niche Requirements

**Choose Appwrite if:**
- Need multi-language functions (Python, Go, Ruby)
- Flutter app + self-hosting

**Choose Nhost if:**
- GraphQL-first project (Apollo Client, Relay)
- Already using Hasura

**Choose Xata if:**
- Need database + integrated search (e-commerce, content)
- TypeScript/Next.js project

---

## Summary Table

| Provider | Best For | Lock-In | Viability | Cost (50K users) | Recommendation |
|----------|----------|---------|-----------|------------------|----------------|
| **Supabase** | General purpose, SQL, real-time | 75/100 | 85/100 | $25-50/mo | **Highly Recommended** |
| **Firebase** | Mobile apps, offline sync | 85/100 | 90/100 | $100-200/mo | Recommended (mobile only) |
| **PocketBase** | MVPs, self-hosting, zero budget | 50/100 | 50/100 | $12/mo | **Highly Recommended** (MVPs) |
| **Appwrite** | Multi-language, self-hosting | 70/100 | 65/100 | $15-30/mo | Recommended (niche) |
| **Xata** | Database + search, TypeScript | 65/100 | 60/100 | $30-50/mo | Recommended (search-heavy) |
| **Nhost** | GraphQL-first, Hasura | 70/100 | 55/100 | $25-50/mo | Recommended (GraphQL only) |

---

## Bottom Line

1. **Default choice:** Supabase (80% of projects)
2. **Mobile apps:** Firebase (accept 85/100 lock-in for offline sync)
3. **MVPs/self-hosting:** PocketBase (lowest cost, lowest lock-in)
4. **Niche requirements:** Appwrite (multi-language), Nhost (GraphQL), Xata (search)

**All BaaS have lock-in** (50-85/100). Accept moderate lock-in (75/100) in exchange for 10x faster development than custom backend. Plan migration when costs exceed $500-1K/month or need custom backend logic.
