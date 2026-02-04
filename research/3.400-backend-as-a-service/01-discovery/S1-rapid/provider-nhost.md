# Provider Profile: Nhost

**Category:** Backend-as-a-Service (BaaS)
**Website:** https://nhost.io/
**Founded:** 2020
**Headquarters:** Stockholm, Sweden

---

## Overview

Nhost is an open-source Backend-as-a-Service platform built on top of Hasura (GraphQL engine) and PostgreSQL. It provides instant GraphQL APIs, authentication, storage, and serverless functions, targeting developers who prefer GraphQL over REST and want the flexibility of SQL databases.

**Tagline:** "The Open Source Firebase Alternative with GraphQL"

---

## Core Technology Stack

**Database:** PostgreSQL (standard relational database)
**API Layer:** Hasura GraphQL Engine (auto-generated GraphQL from database schema)
**Real-time:** GraphQL subscriptions (Hasura real-time)
**Authentication:** Hasura Auth (JWT-based)
**Storage:** S3-compatible object storage
**Functions:** Node.js serverless functions (JavaScript/TypeScript)
**Deployment:** Docker-based, runs on any server

---

## Pricing (2025)

### Free Tier
- **Cost:** $0/month forever
- **Includes:**
  - 1GB database storage
  - 3GB bandwidth
  - 1GB file storage
  - 10,000 monthly active users (auth)
  - Unlimited GraphQL requests
  - 1 project
- **Limitations:**
  - Project pauses after inactivity (similar to Supabase)
  - No backups or point-in-time recovery
  - Community support only

### Pro Tier
- **Cost:** $25/project/month + usage overages
- **Includes:**
  - 10GB database storage ($0.20/GB additional)
  - 50GB bandwidth
  - 20GB file storage
  - 100,000 monthly active users
  - Daily backups (7-day retention)
  - Email support
- **Point-in-Time Recovery (PITR):** $100/month extra (7-day retention)

### Team Tier
- **Cost:** Custom pricing
- **Adds:** Team collaboration, SSO, priority support

### Enterprise
- **Cost:** Custom pricing
- **Adds:** SLA, dedicated support, multi-region, HIPAA compliance

---

## Key Features

### 1. GraphQL-First API
- Hasura auto-generates GraphQL APIs from PostgreSQL schema
- No backend code needed (queries, mutations, subscriptions)
- Type-safe GraphQL (auto-generated TypeScript types)
- Complex queries supported (joins, aggregations, filters)
- Example: `query { users { posts { comments } } }` (nested query, automatic joins)

### 2. PostgreSQL Database
- Full SQL capabilities (joins, transactions, triggers, views)
- Standard database (can migrate to any PostgreSQL host)
- Extensions support (PostGIS, pg_vector for AI/ML)
- Role-based access control (Hasura permissions)

### 3. Real-Time GraphQL Subscriptions
- Subscribe to database changes via GraphQL subscriptions
- Built on Hasura's real-time engine (WebSocket-based)
- Low latency (sub-100ms)
- Example: `subscription { messages { id, text, user } }` (live chat)

### 4. Authentication
- Email/password, magic links, SMS
- OAuth providers: Google, GitHub, Apple, Facebook, etc. (30+ providers)
- JWT-based, integrates with Hasura permissions
- Multi-factor authentication (MFA)
- Anonymous authentication

### 5. Storage
- S3-compatible file storage
- Image transformations (resize, crop, format conversion)
- Access control via Hasura permissions
- CDN integration

### 6. Serverless Functions
- Node.js functions (JavaScript/TypeScript)
- Triggered by GraphQL mutations, HTTP requests, scheduled (cron), events
- Integrated with Hasura (easy database access via GraphQL)
- Example: Send email after user registration, process payment

---

## Strengths

### 1. GraphQL-First Experience
- Best BaaS for GraphQL (Hasura is industry-standard GraphQL engine)
- Auto-generated GraphQL APIs (no backend code)
- Type-safe queries and mutations (TypeScript code generation)
- Apollo Client, Relay, URQL compatible
- Example: Complex queries with joins in one GraphQL request (vs multiple REST calls)

### 2. PostgreSQL = Standard Database
- Not proprietary NoSQL (unlike Firebase, Appwrite)
- Full SQL flexibility (joins, aggregations, analytics)
- Easy migration to any PostgreSQL host (AWS RDS, DigitalOcean, self-hosted)
- Ecosystem of tools (pgAdmin, Prisma, Hasura compatible)

### 3. Hasura Ecosystem
- Hasura is battle-tested (used by Fortune 500 companies)
- Powerful permissions system (row-level security via GraphQL)
- Event triggers (webhooks on database changes)
- Actions (custom business logic via REST endpoints)
- Remote schemas (federate multiple GraphQL APIs)

### 4. Open Source with Self-Hosting
- MIT-licensed (Nhost core is open-source)
- Can self-host on your own infrastructure (Docker Compose)
- Hasura itself is open-source (independent of Nhost)
- Community can maintain if Nhost company shuts down

### 5. Developer Experience
- Excellent GraphQL playground (test queries, mutations, subscriptions)
- Auto-generated documentation (GraphQL schema explorer)
- CLI for local development
- Good documentation and tutorials

---

## Weaknesses

### 1. GraphQL Learning Curve
- GraphQL more complex than REST (need to learn query language)
- Hasura permissions system complex (row-level security via GraphQL)
- Not suitable for GraphQL beginners (Supabase's REST API simpler)
- Example: Writing complex Hasura permission rules requires GraphQL expertise

### 2. Smaller Community vs Firebase/Supabase
- Niche BaaS (GraphQL-first limits appeal)
- Fewer tutorials, courses, Stack Overflow content
- Smaller user base (1/10th of Supabase)
- May encounter bugs or missing features

### 3. Functions Limited to Node.js
- No Python, Go, Ruby support (unlike Appwrite)
- TypeScript/JavaScript only (same limitation as Supabase)
- Not suitable for teams with Python/Go expertise
- Example: Can't run ML inference in Python function

### 4. Vendor Lock-In (Despite Open Source)
- Hasura GraphQL APIs are Hasura-specific (not standard REST)
- Migration requires rewriting GraphQL queries to REST or different GraphQL
- Hasura permissions system proprietary (RLS via GraphQL)
- Lock-in: 70/100 (moderate, similar to Supabase)

### 5. Self-Hosting Complexity
- Nhost self-hosting more complex than Appwrite or PocketBase
- Multiple services (Hasura, PostgreSQL, Auth, Storage, Functions)
- Manual upgrades and maintenance
- Managed cloud (Nhost Cloud) better for most users

---

## Ideal Use Cases

### 1. GraphQL-First Projects
- Apps built with Apollo Client, Relay, URQL
- Developers who prefer GraphQL over REST
- Example: React app with complex data fetching (nested queries, fragments)

### 2. Complex Data Relationships
- Apps with many-to-many relations, nested data
- Need joins and aggregations (SQL advantages)
- Example: E-commerce (products, orders, customers, reviews)

### 3. Real-Time Dashboards
- Live data visualizations (charts, graphs)
- GraphQL subscriptions for real-time updates
- Example: Analytics dashboard, stock ticker, IoT monitoring

### 4. Type-Safe Frontend
- TypeScript projects that benefit from auto-generated types
- End-to-end type safety (database → GraphQL → frontend)
- Example: Enterprise SaaS with strict type requirements

### 5. Hasura Experience
- Teams already familiar with Hasura
- Migrating from self-hosted Hasura to managed Nhost
- Example: Startup using Hasura + PostgreSQL, wants managed BaaS

---

## NOT Ideal For

### 1. REST Preference
- If you prefer REST over GraphQL (simpler, more familiar)
- Use Supabase (REST-first) or Appwrite (REST-first)
- Example: Traditional CRUD app with simple API

### 2. GraphQL Beginners
- GraphQL learning curve steep for new developers
- Hasura permissions complex (need GraphQL expertise)
- Use Supabase or Firebase (simpler REST/SDK APIs)

### 3. Multi-Language Functions
- If you need Python, Go, Ruby for serverless functions
- Use Appwrite (multi-language) or PaaS (Render, Railway)
- Example: ML inference (Python), image processing (Go)

### 4. Mobile-First (No GraphQL)
- If building simple mobile app that doesn't use GraphQL
- Firebase or Supabase better (REST APIs, mobile SDKs)
- Example: iOS app with UIKit, native networking (no GraphQL client)

### 5. NoSQL Preference
- If you prefer document databases (MongoDB-style)
- Use Firebase or Appwrite
- Example: Rapidly changing schema, nested documents

---

## Lock-In Assessment

**Lock-In Severity:** 70/100 (Moderate)

### Migration Difficulty

**Database Migration:** EASY (8-16 hours)
- PostgreSQL standard (export dump, import anywhere)
- No proprietary extensions required
- Can migrate to AWS RDS, Supabase, self-hosted PostgreSQL

**API Migration:** HARD (80-150 hours)
- Hasura GraphQL APIs are Hasura-specific
- Rewrite GraphQL queries to REST or different GraphQL server (Apollo Server, Postgraphile)
- Hasura permissions system proprietary (need to rewrite authorization logic)
- Most painful migration component

**Authentication Migration:** MODERATE (24-40 hours)
- Export user accounts via Hasura GraphQL
- Migrate to Auth0, Clerk, Supabase Auth, or custom
- Update auth calls in frontend code

**Storage Migration:** EASY (8-16 hours)
- S3-compatible storage (export to any S3-compatible service)
- Update file URLs in database

**Functions Migration:** MODERATE (16-40 hours)
- Node.js functions (rewrite as PaaS API endpoints or AWS Lambda)
- Hasura event triggers → webhooks or event streams

**Total Migration Time:** 150-250 hours (4-6 weeks for full migration)

### Why Nhost Lock-In is Moderate

1. **Hasura GraphQL APIs:** Proprietary GraphQL (not standard REST)
2. **Hasura Permissions:** RLS via GraphQL (need to rewrite authorization)
3. **GraphQL Subscriptions:** Hasura-specific real-time API
4. **BUT: PostgreSQL Underneath:** Standard database, easy to export
5. **Open Source Hasura:** Can self-host Hasura independently of Nhost

### Mitigation Strategies

1. **Use Hasura Independently**
   - Self-host Hasura + PostgreSQL (not Nhost Cloud)
   - You control Hasura deployment (no Nhost dependency)
   - Reduces lock-in to Hasura (not Nhost)

2. **Abstract Hasura Behind API Layer**
   - Create REST API that calls Hasura GraphQL internally
   - Frontend calls REST API, not Hasura directly
   - Easier to swap out Hasura later (but adds complexity)

3. **Use PostgreSQL Directly**
   - Use Nhost only for database and auth
   - Write custom GraphQL server (Apollo Server, Postgraphile)
   - Avoids Hasura lock-in

---

## Community and Ecosystem

**GitHub:** Nhost has ~8,000 stars (smaller than Supabase, Appwrite)
**Hasura:** 31,000+ stars (Hasura itself has larger community)
**Discord:** 5,000+ members (smaller community)
**Documentation:** Good (GraphQL-focused docs, Hasura guides)
**Tutorials:** Limited (fewer courses vs Firebase/Supabase)
**Integrations:** Hasura ecosystem (event triggers, actions, remote schemas)

---

## Competitive Positioning

### vs Supabase
- **Nhost wins:** GraphQL-first, Hasura ecosystem, better for complex queries
- **Supabase wins:** Larger community, REST-first (simpler), better docs

### vs Firebase
- **Nhost wins:** PostgreSQL (SQL), GraphQL, open-source, lower lock-in
- **Firebase wins:** More mature, larger ecosystem, better mobile SDKs

### vs Appwrite
- **Nhost wins:** PostgreSQL (SQL), GraphQL, Hasura ecosystem
- **Appwrite wins:** Multi-language functions, easier self-hosting, NoSQL for flexible schema

### vs Xata
- **Nhost wins:** Open-source, GraphQL, Hasura ecosystem
- **Xata wins:** Serverless PostgreSQL, built-in search, simpler DX (no GraphQL learning curve)

---

## Funding and Viability

**Total Funding:** Unknown (early-stage, bootstrapped or seed funded)
**Revenue Model:** Nhost Cloud (managed service), enterprise support
**Backed by:** Y Combinator (YC S20)

**Acquisition Risk:** MODERATE
- Small team, early-stage (likely acquisition target)
- Hasura (the underlying tech) is independent (Series C, well-funded)
- Nhost company could be acquired or shut down, but Hasura remains

**Shutdown Risk:** MODERATE
- If Nhost shuts down, can self-host or use Hasura directly
- Hasura Cloud is alternative (official Hasura managed service)
- Open-source nature provides exit path

**Longevity Outlook:** 3-5 years uncertain (small company, early-stage)

---

## Final Verdict

**Recommendation Level:** RECOMMENDED for GraphQL Projects (Niche BaaS)

**Best for:**
- GraphQL-first projects (Apollo Client, Relay, URQL)
- Complex data relationships (SQL joins, aggregations)
- Real-time dashboards and analytics
- Type-safe TypeScript projects (auto-generated types)
- Developers familiar with Hasura

**Avoid if:**
- Prefer REST over GraphQL (use Supabase, Appwrite)
- GraphQL beginners (steep learning curve)
- Need multi-language functions (Python, Go)
- Want larger community and ecosystem (use Supabase, Firebase)

**Bottom line:** Nhost is the best BaaS for GraphQL-first projects, leveraging Hasura's powerful GraphQL engine and PostgreSQL's flexibility. However, the GraphQL learning curve and smaller community limit its appeal to ~10-15% of BaaS use cases. If you're already using GraphQL or need complex data relationships, Nhost is excellent. If you prefer REST or are new to GraphQL, choose Supabase instead.

**2025 Status:** Niche player in BaaS market, growing slowly but steadily. Hasura's maturity and open-source nature provide stability, but Nhost company is early-stage with uncertain long-term viability. Recommended for GraphQL experts, not beginners. Consider using Hasura Cloud directly if Nhost's longevity is a concern.
