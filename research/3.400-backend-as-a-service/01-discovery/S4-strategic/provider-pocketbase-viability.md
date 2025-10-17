# PocketBase Viability Assessment

**Provider:** PocketBase
**Assessment Date:** 2025-10-10
**Current Status:** Single maintainer open-source project

---

## Executive Summary

**Viability Score: 50/100** (MODERATE - Uncertain 5-10 Years)

PocketBase is a **single-maintainer open-source project** (Gani Georgiev) with no company or VC funding. While the **MIT license** ensures the project can continue via community fork, the **single maintainer risk** creates uncertainty beyond 3-5 years.

**Key Finding:** PocketBase is excellent for MVPs and self-hosting (lowest cost, lowest lock-in), but project viability depends on maintainer availability. Community can fork (MIT license), but requires coordination if maintainer stops.

---

## Project Overview

**Founded:** 2022
**Maintainer:** Gani Georgiev (solo developer, based in Bulgaria)
**Funding:** None (independent project, donations accepted)
**License:** MIT (open-source, no commercial restrictions)
**Community:** 40K+ GitHub stars, 7K+ Discord members (active community)
**Business Model:** Free forever (donations via GitHub Sponsors, no paid tiers)

---

## Single Maintainer Risk

**Maintainer:** Gani Georgiev
- Solo developer (no co-founders, no team)
- Full-time on PocketBase (as of 2023)
- Active development (regular releases: v0.20+ in 2025)
- Responsive to community (Discord, GitHub issues)

**Risks:**
1. **Burnout:** Solo development is exhausting (common 3-5 year burnout)
2. **Life changes:** Marriage, family, health issues can slow/stop development
3. **Financial pressure:** Donations may not sustain full-time work long-term
4. **Lack of succession:** No clear plan if maintainer stops

**Mitigation:**
- **MIT License:** Community can fork and maintain if maintainer stops
- **Simple codebase:** Go, SQLite (easier for community to maintain than complex Docker stacks)
- **Active community:** 40K+ stars, 7K+ Discord = potential contributors
- **But:** Coordination required (who leads fork? governance structure?)

---

## Timeline Outlook

**2025-2027:** ACTIVE DEVELOPMENT (High Probability)
- Regular releases (v0.20+, feature additions)
- Active community (40K+ GitHub stars growing)
- Maintainer full-time on PocketBase
- Feature roadmap: Full-text search, multi-tenancy, clustering

**2027-2030:** UNCERTAIN (Moderate Probability)
- Maintainer may slow down (burnout, life changes, financial pressure)
- Community may need to fork (MIT license allows this)
- Potential: Company formed around PocketBase (commercial support, managed cloud)
- Potential: Acquisition by larger project (Supabase, Appwrite could acquire maintainer/project)

**2030+:** COMMUNITY MAINTENANCE (Unknown Probability)
- If maintainer stops, community must coordinate fork
- Precedents: Redis (started solo, now Redis Labs), MongoDB (started solo, now MongoDB Inc.)
- But: Not all projects transition successfully (some die after maintainer leaves)

---

## Risk Assessment

**Acquisition Risk:** NONE (no company to acquire)
**Shutdown Risk:** MODERATE (single maintainer may stop, community must fork)
**Pricing Risk:** NONE (free forever, MIT license)
**Feature Risk:** MODERATE (development pace depends on maintainer)

---

## Viability Score: 50/100

| Factor | Score | Reasoning |
|--------|-------|-----------|
| Financial Stability | 40 | No funding, donations only |
| Maintainer Risk | 40 | Single maintainer, no succession plan |
| Community Strength | 70 | 40K+ stars, active Discord |
| License (MIT) | 90 | Can fork if needed |
| Code Simplicity | 80 | Go + SQLite easier to maintain than Docker stacks |
| Lock-In (Low) | 100 | 50/100 lock-in, easy migration |

**Total: 50/100** (MODERATE - uncertain 5-10 years)

---

## Lock-In Assessment

**Lock-In Score: 50/100** (LOWEST - Easiest Migration)

**Migration Time:** 60-100 hours ($6K-10K developer time)
**Migration Difficulty:** LOW-MODERATE (SQLite → PostgreSQL, REST API → Supabase SDK)

**Why Low Lock-In:**
- Standard SQLite database (easy SQL dump, migrate to PostgreSQL)
- REST API (standard HTTP, not proprietary SDK)
- Simple real-time (SSE, easy to replace with Pusher, Ably)

**Migration Path:** PocketBase → Supabase (60-100 hours, $6K-10K)

---

## Recommendation

**USE POCKETBASE FOR MVPS AND SELF-HOSTING** with understanding of single maintainer risk.

**Why PocketBase is Good Choice:**
1. Lowest cost ($5/month VPS, no BaaS fees)
2. Lowest lock-in (50/100, easiest migration)
3. Simplest deployment (single binary, 2 minutes)
4. MIT license (community can fork if needed)
5. Active community (40K+ stars, likely to continue if maintainer stops)

**Why PocketBase Has Risks:**
1. Single maintainer (may stop development 3-5 years)
2. No company (no commercial support, no managed cloud)
3. SQLite scaling limits (not for >10K concurrent users)
4. Uncertain long-term (community must coordinate if maintainer stops)

**Strategic Approach:**
- **Use PocketBase for MVPs** (2-3 year horizon, validate product)
- **Plan migration** when scaling beyond SQLite limits (>10K concurrent users)
- **Migrate to Supabase** when product proven and scaling (60-100 hours, $6K-10K)
- **Low risk** (50/100 lock-in = easy migration if project stagnates)

**Timeline:**
- **2025-2027:** Use PocketBase (active development, low cost, low lock-in)
- **2027-2030:** Monitor maintainer activity (if slows, plan migration to Supabase)
- **2030+:** Likely community fork or migration needed

**Bottom Line:** PocketBase is **best for MVPs and self-hosting** (lowest cost, lowest lock-in), but **moderate viability** (50/100, single maintainer risk). Use for 2-3 years, migrate to Supabase when scaling or if project stagnates. Low lock-in (50/100) makes this a low-risk choice for MVPs.
