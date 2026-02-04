# Provider Profile: PocketBase

**Category:** Backend-as-a-Service (BaaS)
**Website:** https://pocketbase.io/
**Founded:** 2022
**Headquarters:** Open-source project (no company)

---

## Overview

PocketBase is an open-source Backend-as-a-Service delivered as a single executable file (written in Go). It includes an embedded SQLite database, real-time subscriptions, authentication, file storage, and an admin dashboard — all in one ~15MB binary. No dependencies, no configuration, no cloud required.

**Tagline:** "Open Source backend in 1 file"

---

## Core Technology Stack

**Database:** SQLite (embedded, file-based SQL database)
**Real-time:** Server-Sent Events (SSE) for real-time subscriptions
**Authentication:** Built-in (JWT-based)
**Storage:** Local filesystem
**API:** Auto-generated REST API from database schema
**Runtime:** Go binary (single executable, no external dependencies)
**Deployment:** Download and run (no Docker, no Node.js, no Python)

---

## Pricing (2025)

### Open Source (Self-Hosted Only)
- **Cost:** $0 (free forever, MIT licensed)
- **Includes:** Everything (unlimited users, storage, requests)
- **Requirements:**
  - Your own server (VPS, Raspberry Pi, NAS, laptop, any computer)
  - Zero dependencies (just download binary and run)
  - Minimal DevOps (no Docker, no complex setup)
- **Infrastructure costs:**
  - $5-12/month VPS (Hetzner, DigitalOcean, Linode)
  - $0 for self-hosting at home (Raspberry Pi, old laptop)

### No Cloud Service
- **PocketBase is self-hosted only** (no managed cloud offering)
- **No company behind it** (maintained by community, primarily Gani Georgiev)
- **No enterprise support** (community-driven, GitHub issues, Discord)

---

## Key Features

### 1. Single Binary Simplicity
- Download one executable file (~15MB)
- No installation, no dependencies, no configuration
- Run `./pocketbase serve` and you have a backend
- Example: `wget pocketbase && chmod +x pocketbase && ./pocketbase serve` (3 commands, 30 seconds)

### 2. SQLite Database
- Embedded SQL database (no separate database server)
- Full SQL support (joins, transactions, triggers, indexes)
- File-based (one `.db` file, easy to backup and migrate)
- Suitable for small-to-medium scale (100-10,000 concurrent users)
- Limited horizontal scaling (SQLite is single-file, not distributed)

### 3. Auto-Generated REST API
- Create database collections via admin UI or API
- PocketBase auto-generates REST endpoints (CRUD operations)
- No backend code needed
- Example: Create "posts" collection → `/api/collections/posts/records` endpoint available

### 4. Real-Time Subscriptions
- Subscribe to database changes via Server-Sent Events (SSE)
- Client SDKs for JavaScript, Dart (Flutter)
- Example: `pb.collection('posts').subscribe('*', callback)` (live updates)

### 5. Authentication
- Email/password, OAuth2 (Google, GitHub, GitLab, Discord, etc.)
- JWT-based authentication
- User and admin roles (built-in)
- Password reset, email verification

### 6. File Storage
- Upload files via API
- Store locally on filesystem
- Access control via collection rules
- Example: Upload profile pictures, documents, images

### 7. Admin Dashboard
- Built-in web UI (accessible at `http://localhost:8090/_/`)
- Manage collections, records, users, settings
- No need for separate database GUI
- Logs and request history viewer

### 8. Extensibility
- PocketBase is a Go library (not just a binary)
- Can embed PocketBase in your own Go app
- Add custom routes, middleware, business logic
- JavaScript hooks (extend via JavaScript VM)

---

## Strengths

### 1. Extreme Simplicity
- Easiest BaaS to deploy (download binary, run one command)
- Zero dependencies (no Node.js, Python, Docker, PostgreSQL)
- No cloud account needed (run anywhere)
- Example: Deploy to Raspberry Pi in 5 minutes

### 2. SQLite = Portable Database
- Single `.db` file (easy to backup, copy, migrate)
- Standard SQL (can export to PostgreSQL, MySQL if needed)
- Fast for small-to-medium workloads (SQLite is lightweight)
- Works offline (perfect for local development)

### 3. Lowest Lock-In of Any BaaS
- Standard REST API (no proprietary SDKs required)
- SQLite database (standard SQL, easy to migrate)
- Open-source (can fork and maintain)
- Migration time: 20-40 hours (easiest BaaS to leave)

### 4. Self-Hosting Made Easy
- No Docker Compose (unlike Supabase, Appwrite, Nhost)
- No Kubernetes (unlike enterprise BaaS)
- Run on any server, even $5/month VPS or Raspberry Pi
- Example: Deploy to Fly.io, Railway, or DigitalOcean in 10 minutes

### 5. Zero Cost
- No cloud vendor (no usage fees, no monthly subscriptions)
- Only pay for hosting (VPS, home server, or free Fly.io tier)
- Perfect for indie hackers, side projects, cost-sensitive apps

### 6. Fast Development
- Admin dashboard for quick data management
- Auto-generated API endpoints
- Real-time subscriptions included
- Example: Build full-stack app in hours (Vue.js + PocketBase)

---

## Weaknesses

### 1. SQLite Scaling Limits
- Single-file database (no horizontal scaling)
- Suitable for 100-10,000 concurrent users (not millions)
- Write concurrency limited (SQLite locks database during writes)
- Not suitable for high-traffic production apps (use PostgreSQL-based BaaS)

### 2. No Managed Cloud Service
- Must self-host (no Firebase-like managed cloud)
- No automatic backups, monitoring, scaling (DIY)
- No enterprise support or SLA
- Example: Need to set up your own backup scripts, monitoring alerts

### 3. No Multi-Language Functions
- Extensibility requires Go programming (not Python, TypeScript, etc.)
- JavaScript hooks (experimental, limited)
- Not suitable for teams without Go expertise
- Example: Can't easily add Python ML inference endpoint

### 4. Smaller Community
- New project (2022, younger than Firebase, Supabase, Appwrite)
- Fewer tutorials, courses, Stack Overflow answers
- Active GitHub (9,000+ stars), but smaller than competitors
- May encounter bugs or missing features

### 5. Single Maintainer Risk
- Primarily maintained by one developer (Gani Georgiev)
- If maintainer stops, project could stagnate
- Open-source community can fork, but uncertainty remains
- No company backing or commercial support

---

## Ideal Use Cases

### 1. Indie Hackers and Side Projects
- Solo developers building MVPs or side projects
- Zero budget (self-host on Raspberry Pi or free tier VPS)
- Example: Personal blog, habit tracker, note-taking app

### 2. Prototyping and MVPs
- Test product ideas quickly (deploy in minutes)
- No cloud vendor lock-in (easy to migrate later)
- Example: Weekend hackathon project, startup MVP

### 3. Small-Scale Production Apps
- Apps with 100-5,000 users (not millions)
- Predictable, moderate traffic
- Example: Internal company tool, community forum, niche SaaS

### 4. Self-Hosting Enthusiasts
- Developers who prefer self-hosting over cloud
- Run on home server, NAS, Raspberry Pi
- Example: Privacy-focused personal cloud, family app

### 5. Learning and Education
- Students learning backend development
- No cloud account or credit card needed
- Example: University project, coding bootcamp assignment

### 6. Edge Deployment
- Deploy close to users (multiple regional instances)
- SQLite's simplicity makes multi-region deployment easy
- Example: Deploy to Fly.io globally (PocketBase on edge nodes)

---

## NOT Ideal For

### 1. High-Scale Production Apps (>10K Concurrent Users)
- SQLite scaling limits (write concurrency bottleneck)
- Use PostgreSQL-based BaaS (Supabase, Nhost) or Firebase
- Example: Viral social network, global SaaS with 100K+ users

### 2. Enterprise Requirements
- No SLA, no enterprise support, no compliance certifications (SOC 2, HIPAA)
- Use Firebase, Supabase Pro/Enterprise, or AWS
- Example: Healthcare app (HIPAA), financial services (SOC 2)

### 3. Complex Business Logic
- Extensibility requires Go programming (not Python, Node.js, etc.)
- No built-in serverless functions (like Firebase Cloud Functions)
- Use PaaS (Render, Railway) for custom backend
- Example: E-commerce with complex pricing rules, ML inference

### 4. GraphQL Preference
- PocketBase is REST-only (no GraphQL)
- Use Nhost (Hasura GraphQL) or add custom GraphQL layer
- Example: Apollo Client app with complex graph queries

### 5. Managed Cloud with Zero DevOps
- PocketBase requires self-hosting (no managed cloud)
- Use Firebase, Supabase Cloud, or Appwrite Cloud
- Example: Non-technical founder with no DevOps skills

---

## Lock-In Assessment

**Lock-In Severity:** 50/100 (LOW)

### Migration Difficulty

**Database Migration:** EASY (8-16 hours)
- SQLite export to SQL dump
- Import to PostgreSQL, MySQL, or keep SQLite
- Standard SQL (no proprietary extensions)

**API Migration:** EASY (16-32 hours)
- PocketBase uses standard REST API (no proprietary SDK)
- Rewrite API calls to new backend (Supabase, custom API)
- Less lock-in than Firebase, Supabase (which have proprietary SDKs)

**Authentication Migration:** MODERATE (16-24 hours)
- Export user accounts from SQLite database
- Migrate to Auth0, Clerk, Supabase Auth, or custom
- JWT-based (standard, easy to replace)

**Real-Time Migration:** MODERATE (16-24 hours)
- Replace PocketBase SSE subscriptions with Pusher, Ably, Supabase real-time
- Rewrite real-time listeners in codebase

**Storage Migration:** EASY (4-8 hours)
- Copy files from local filesystem to S3, Cloudflare R2, etc.
- Update file URLs in database

**Total Migration Time:** 60-100 hours (1.5-2.5 weeks for full migration)

### Why PocketBase Lock-In is LOW

1. **Standard REST API:** No proprietary SDK (unlike Firebase, Supabase)
2. **SQLite Standard:** Easy to export and migrate to any database
3. **Open Source:** Can fork and maintain if project stagnates
4. **No Cloud Dependency:** Self-hosted, no vendor control
5. **Simple Architecture:** Single binary, easy to understand and replace

### Mitigation Strategies

1. **Use PocketBase for MVP, Migrate Later**
   - Launch quickly with PocketBase (zero cost, fast setup)
   - Migrate to Supabase or custom backend when scaling
   - Migration easier than Firebase → PostgreSQL (50/100 lock-in vs 85/100)

2. **Abstract PocketBase Behind API Layer**
   - Create your own API that calls PocketBase
   - Frontend calls your API, not PocketBase directly
   - Easiest to swap out later (reduces lock-in to 30/100)

3. **Use Standard SQL**
   - Avoid PocketBase-specific features (use plain SQL)
   - Makes migration even easier (no PocketBase API rewrites)

---

## Community and Ecosystem

**GitHub:** 45,000+ stars (strong community, very rapid growth)
**Discord:** 5,000+ members (active support)
**Documentation:** Good (improving, clear examples)
**Tutorials:** Growing (YouTube, blog posts, courses)
**Integrations:** Limited (no Firebase Extensions equivalent, but standard REST means easy integration)
**Client SDKs:** JavaScript, Dart (Flutter), community-maintained for other languages

---

## Competitive Positioning

### vs Firebase
- **PocketBase wins:** Open-source, self-hosting, zero lock-in, zero cost
- **Firebase wins:** Managed cloud, mobile SDKs, larger ecosystem, scales to millions

### vs Supabase
- **PocketBase wins:** Simpler (single binary), lower lock-in, zero cost, easier self-hosting
- **Supabase wins:** PostgreSQL (better scaling), managed cloud, larger community

### vs Appwrite
- **PocketBase wins:** Simpler (single binary vs Docker Compose), SQLite portability
- **Appwrite wins:** Multi-language functions, more features, managed cloud option

### vs Nhost
- **PocketBase wins:** Simpler (no GraphQL learning curve), lower lock-in, easier self-hosting
- **Nhost wins:** PostgreSQL + GraphQL, better for complex queries

---

## Funding and Viability

**Funding:** $0 (no company, no investors)
**Maintainer:** Gani Georgiev (primary developer)
**Revenue Model:** None (donations, personal project)
**Business Model:** No business (open-source passion project)

**Acquisition Risk:** N/A (no company to acquire)
**Shutdown Risk:** MODERATE
- Single maintainer (if Gani stops, project could stagnate)
- BUT: Open-source (community can fork and maintain)
- MIT license (anyone can continue development)

**Longevity Outlook:** 3-5 years safe (active development), 5-10 years uncertain (depends on community)

---

## Final Verdict

**Recommendation Level:** HIGHLY RECOMMENDED for MVPs and Self-Hosting (Niche BaaS)

**Best for:**
- Indie hackers and solo developers (zero budget)
- Rapid prototyping and MVPs (launch in hours)
- Small-scale production apps (100-5,000 users)
- Self-hosting enthusiasts (run on Raspberry Pi, home server)
- Learning and education (no cloud account needed)
- Lowest lock-in requirement (easy to migrate later)

**Avoid if:**
- High-scale production apps (>10K concurrent users)
- Enterprise requirements (SLA, support, compliance)
- Need managed cloud (zero DevOps)
- Complex backend logic (multi-language functions)
- GraphQL preference

**Bottom line:** PocketBase is the simplest and most portable BaaS, perfect for MVPs, indie projects, and cost-conscious developers. The single binary simplicity and SQLite portability make it the easiest BaaS to deploy and migrate away from. However, SQLite scaling limits and lack of managed cloud restrict it to small-to-medium scale apps. Recommended for 20-30% of BaaS use cases where simplicity, cost, and low lock-in are top priorities.

**2025 Status:** Rapidly growing community (45K+ GitHub stars in 3 years), actively maintained, gaining popularity among indie hackers and developers seeking simple self-hosted backends. No company backing creates uncertainty, but open-source nature ensures community can continue development. Best used for early-stage projects with plan to migrate to PostgreSQL-based BaaS (Supabase) when scaling.

**Unique positioning:** PocketBase is the only "true self-hosted" BaaS that's genuinely simple (single binary vs Docker Compose). It fills a niche between DIY backend (too complex) and managed BaaS (too expensive, too much lock-in). Ideal for developers who want "Firebase simplicity without Firebase lock-in."
