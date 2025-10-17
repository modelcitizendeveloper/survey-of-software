# PocketBase - Provider Deep Dive

**Category:** Backend-as-a-Service (BaaS)
**Website:** https://pocketbase.io/
**Founded:** 2022
**Positioning:** "Open Source backend in 1 file" - self-hosted, SQLite-based

## Overview & Positioning

PocketBase is an **open-source, self-hosted BaaS** packaged as a single executable (~15 MB), built in Go with an embedded SQLite database. It represents the opposite philosophy from Firebase: simplicity, self-hosting, and zero vendor lock-in.

**Market Position:** Ideal BaaS for indie hackers, MVPs, and cost-conscious developers seeking:
- Zero cloud costs (self-host on $5 VPS)
- Simplest deployment (single binary, zero dependencies)
- Lowest lock-in (50/100, standard REST API + SQLite)
- Rapid prototyping (live admin UI, auto-generated APIs)

**Key Differentiator:** Radical simplicity - download one file, run it, you have a complete backend (database, auth, storage, real-time, admin UI) with zero configuration.

**Project Status:**
- **Maintainer:** Gani Georgiev (solo developer)
- **License:** MIT (open-source)
- **Community:** 40K+ GitHub stars, active Discord
- **Funding:** None (independent project, not VC-backed)
- **Business Model:** Free forever (donations accepted)

---

## 1. Architecture & Technical Stack

### Core Architecture

PocketBase is written in **Go** and compiles to a single statically-linked binary (~15 MB).

**Database Layer:**
- **SQLite** - Embedded SQL database (file-based)
- **No external database server** required (all data in one file: `pb_data/data.db`)
- **Supports:** Full SQL (joins, transactions, indexes, triggers)
- **Limitations:** Single-writer (SQLite constraint), not for >10K concurrent users

**Authentication Layer:**
- **Built-in auth** (JWT-based)
- OAuth2 providers: Google, Facebook, GitHub, GitLab, Discord, etc. (20+ providers)
- Email/password authentication
- User/admin separation (admins manage via web UI)

**Storage Layer:**
- **Local file storage** (stores files in `pb_data/storage/`)
- File upload/download REST API
- Thumbnail generation for images
- S3-compatible storage (optional, via extensions)

**Real-Time Layer:**
- **Server-Sent Events (SSE)** - one-way server-to-client push
- Subscribe to record changes (create, update, delete)
- Not full WebSocket (simpler, but less flexible than Supabase/Firebase)

**Admin UI:**
- **Built-in web dashboard** at `http://localhost:8090/_/` (port 8090 default)
- Manage collections (tables), records (rows), users, settings
- No-code database management (create tables, fields, rules via UI)

**Extensibility:**
- **Go package** - import PocketBase as library, add custom business logic
- **JavaScript hooks** - run custom code on events (beforeCreate, afterUpdate, etc.)
- **Complete control** - build custom backend using PocketBase as foundation

---

### Deployment Models

**Self-Hosted Only** (No Managed Cloud)
- PocketBase is self-hosted by design (no official cloud service)
- Community services exist (PocketHost, etc.) but not official

**Deployment Options:**

**1. Single Binary (Simplest)**
```bash
# Download PocketBase (one file, ~15 MB)
wget https://github.com/pocketbase/pocketbase/releases/download/v0.20.0/pocketbase_0.20.0_linux_amd64.zip
unzip pocketbase_0.20.0_linux_amd64.zip

# Run PocketBase
./pocketbase serve

# Backend running at http://localhost:8090
# Admin UI at http://localhost:8090/_/
```

**2. VPS Deployment (Production)**
```bash
# On $5 Hetzner/DigitalOcean VPS (Ubuntu)
wget <pocketbase-url>
unzip pocketbase.zip
chmod +x pocketbase

# Run as systemd service
sudo nano /etc/systemd/system/pocketbase.service

[Unit]
Description=PocketBase
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/pocketbase
ExecStart=/var/www/pocketbase/pocketbase serve --http=0.0.0.0:8090
Restart=always

[Install]
WantedBy=multi-user.target

sudo systemctl enable pocketbase
sudo systemctl start pocketbase
```

**3. Docker Deployment**
```dockerfile
FROM alpine:latest
WORKDIR /app
COPY pocketbase /app/pocketbase
EXPOSE 8090
CMD ["/app/pocketbase", "serve", "--http=0.0.0.0:8090"]
```

**4. Extend with Go (Custom Business Logic)**
```go
package main

import (
    "log"
    "github.com/pocketbase/pocketbase"
)

func main() {
    app := pocketbase.New()

    // Custom route
    app.OnBeforeServe().Add(func(e *core.ServeEvent) error {
        e.Router.GET("/custom", func(c echo.Context) error {
            return c.String(200, "Custom endpoint")
        })
        return nil
    })

    if err := app.Start(); err != nil {
        log.Fatal(err)
    }
}
```

---

## 2. Database: SQLite

### SQL Database Model

PocketBase uses **SQLite** (embedded SQL database, file-based).

**Advantages:**
- Full SQL support (joins, transactions, subqueries)
- Standard database format (easy to backup, migrate, inspect)
- Zero configuration (no database server to install)
- Fast for reads (up to 100K reads/sec on SSD)

**Limitations:**
- **Single-writer** constraint (only one write at a time)
- Not for high-concurrency writes (>100 writes/sec)
- Not for distributed databases (single-server only)
- Max database size: 281 TB (practically unlimited)

**Scaling Limits:**
- **Concurrent users:** 10K-50K (reads mostly)
- **Concurrent writes:** 100-500/sec (SQLite bottleneck)
- **Database size:** 100 GB+ (practical limit on VPS SSD)

**Migration to PostgreSQL:**
- Easy migration path (SQLite → PostgreSQL via SQL dump)
- Migrate when concurrent writes exceed 100/sec
- Migrate when database size exceeds 50 GB
- Use Supabase, Nhost, or PaaS with PostgreSQL

---

### Collections & Schema

PocketBase uses **collections** (equivalent to SQL tables).

**Admin UI - Create Collection (No Code):**
1. Open http://localhost:8090/_/
2. Click "Create Collection"
3. Add fields (text, number, email, file, relation, etc.)
4. Set validation rules, default values
5. Define API rules (who can create, read, update, delete)

**Example - Users Collection:**
```
Collection: users
Fields:
  - name (text, required)
  - email (email, unique, required)
  - avatar (file, optional)
  - bio (text, optional)
  - created (datetime, auto-set)
  - updated (datetime, auto-set)

API Rules:
  - List: @request.auth.id != ""  // Only authenticated users
  - View: @request.auth.id != ""
  - Create: @request.auth.id != ""
  - Update: @request.auth.id = id  // Only own record
  - Delete: @request.auth.id = id
```

---

### REST API (Auto-Generated)

PocketBase auto-generates REST API from collections.

**Example - CRUD Operations:**
```javascript
// Initialize PocketBase SDK
import PocketBase from 'pocketbase'
const pb = new PocketBase('http://localhost:8090')

// Create record
const record = await pb.collection('posts').create({
  title: 'Hello World',
  content: 'My first post',
  author: 'user123'
})

// List records (with filters)
const posts = await pb.collection('posts').getList(1, 20, {
  filter: 'published = true',
  sort: '-created'
})

// Get single record
const post = await pb.collection('posts').getOne('RECORD_ID')

// Update record
await pb.collection('posts').update('RECORD_ID', {
  title: 'Updated Title'
})

// Delete record
await pb.collection('posts').delete('RECORD_ID')
```

**Query Filters (SQL-like):**
```javascript
// Filter by field
filter: 'status = "active"'

// Multiple conditions
filter: 'status = "active" && published = true'

// Comparison operators
filter: 'price > 100 && price <= 500'

// Text search
filter: 'title ~ "hello"'  // Contains "hello"

// Relations
filter: 'author.name = "John"'  // Join with author collection
```

---

## 3. Authentication

PocketBase provides built-in authentication with JWT tokens.

**Email/Password Authentication:**
```javascript
// Sign up
const user = await pb.collection('users').create({
  email: 'john@example.com',
  password: 'password123',
  passwordConfirm: 'password123',
  name: 'John Doe'
})

// Login
const authData = await pb.collection('users').authWithPassword(
  'john@example.com',
  'password123'
)

console.log('Token:', authData.token)
console.log('User:', authData.record)

// Auto-refresh token (PocketBase SDK handles this)
pb.authStore.isValid // true if authenticated

// Logout
pb.authStore.clear()
```

**OAuth2 Providers (Google, GitHub, etc.):**
```javascript
// List available OAuth2 providers
const providers = await pb.collection('users').listAuthMethods()

// Initiate OAuth2 flow
const authData = await pb.collection('users').authWithOAuth2({
  provider: 'google'
})
```

**API Rules (Authorization):**
```
// Only authenticated users can create posts
@request.auth.id != ""

// Users can only update their own posts
@request.auth.id = author.id

// Public read, authenticated write
List: true
Create: @request.auth.id != ""
```

---

## 4. Real-Time Capabilities

PocketBase uses **Server-Sent Events (SSE)** for real-time subscriptions.

**Subscribe to Record Changes:**
```javascript
// Subscribe to 'posts' collection
pb.collection('posts').subscribe('*', (e) => {
  console.log('Action:', e.action) // create, update, delete
  console.log('Record:', e.record)
})

// Subscribe to specific record
pb.collection('posts').subscribe('RECORD_ID', (e) => {
  console.log('Record updated:', e.record)
})

// Unsubscribe
pb.collection('posts').unsubscribe()
```

**Limitations vs. WebSocket (Supabase/Firebase):**
- **SSE is one-way** (server → client only, not bidirectional)
- No presence channels (can't track online users like Supabase)
- No broadcast channels (can't send ephemeral messages)
- Simpler protocol (lower latency, easier to implement)

**Performance:**
- Latency: 50-200ms (depends on server load)
- Max concurrent connections: 10K-50K (SSE is lightweight)
- Auto-reconnect (SDK handles disconnections)

---

## 5. Developer Experience

### Setup & First Deployment

**Time to First API:** 2-5 minutes (fastest of all BaaS)

**Steps:**
1. Download PocketBase binary (one file, ~15 MB)
2. Run `./pocketbase serve`
3. Open http://localhost:8090/_/
4. Create admin account
5. Create collection (e.g., "posts")
6. Add fields (title, content, author)
7. REST API live at http://localhost:8090/api/collections/posts/records

**No Code Required:** Entire backend setup via web UI (no SQL, no YAML, no Docker).

---

### SDKs & Client Libraries

**Official SDKs:**
- **JavaScript/TypeScript** - pocketbase-js (browser, Node.js)
- **Dart/Flutter** - pocketbase-dart

**Community SDKs:**
- **Python** - pocketbase-python (unofficial)
- **Go** - PocketBase is written in Go (import as library)
- **Rust, C#, PHP, Ruby** - various community SDKs

**SDK Maturity:**
- **Excellent:** JavaScript/TypeScript (official, well-maintained)
- **Good:** Dart/Flutter (official)
- **Limited:** Python, other languages (community-maintained, less stable)

---

### Documentation Quality

**Good** (7/10)

**Strengths:**
- Clear getting-started guide
- API documentation (REST endpoints, SDK methods)
- Active Discord community (7K+ members)
- Example projects (to-do app, blog, chat)

**Weaknesses:**
- Limited advanced use cases (scaling, clustering not officially supported)
- Self-hosting production setup underdocumented (systemd, backups, monitoring)
- Extending with Go requires familiarity with Go ecosystem

---

## 6. Performance Benchmarks

### SQLite Performance

**Read Performance:**
- Simple SELECT (indexed): 1-5ms (extremely fast)
- Complex JOIN (3 tables): 10-30ms
- Full-text search: 20-100ms

**Write Performance:**
- Single INSERT: 10-50ms
- Bulk INSERT (1000 rows): 100-500ms
- UPDATE/DELETE: 10-50ms

**Concurrent Performance:**
- Max concurrent reads: 100K reads/sec (SSD)
- Max concurrent writes: 100-500 writes/sec (single-writer bottleneck)

**Scaling Limits:**
- Database size: 100 GB+ practical limit (VPS SSD)
- Concurrent users: 10K-50K (reads mostly, <100 writes/sec)
- When to migrate: >100 writes/sec → migrate to PostgreSQL (Supabase, PaaS)

---

## 7. Lock-In Assessment: 50/100 (LOWEST)

### Lock-In Factors

**1. Standard REST API (Low Lock-In: 10 points)**
- PocketBase auto-generates REST API (standard HTTP)
- Easy to replace with custom backend (Express, Flask, FastAPI)
- SDK abstraction layer minimal (just HTTP requests)

**2. SQLite Database (Low Lock-In: 5 points)**
- SQLite is standard format (migrate to PostgreSQL, MySQL in 4-8 hours)
- SQL dump: `sqlite3 pb_data/data.db .dump > backup.sql`
- Import to PostgreSQL: `psql mydb < backup.sql`

**3. Authentication (Low Lock-In: 10 points)**
- JWT tokens (standard, easy to verify in custom backend)
- OAuth2 providers (standard protocol, easy to replicate)

**4. Real-Time (SSE) (Low Lock-In: 15 points)**
- Server-Sent Events (standard web protocol)
- Easy to replace with WebSocket, Pusher, Ably

**5. File Storage (Low Lock-In: 5 points)**
- Local file storage (copy files to S3, Cloudflare R2)
- Standard file paths (no proprietary storage API)

**6. Admin UI Dependency (Moderate Lock-In: 5 points)**
- Admin UI is PocketBase-specific (must build replacement if migrating)
- Not critical (admin UI not part of production app)

---

### Migration Paths

**PocketBase → Supabase:**
- Time: 60-100 hours (SQLite → PostgreSQL, REST API similar, rewrite real-time)
- Difficulty: LOW-MODERATE (SQL migration easy, SDK replacement moderate)
- Cost: $6K-10K developer time (at $100/hour)

**PocketBase → Custom Backend (Express + PostgreSQL):**
- Time: 80-120 hours (build REST API, migrate SQLite → PostgreSQL)
- Difficulty: MODERATE (must write backend code from scratch)
- Cost: $8K-12K developer time

**PocketBase → Firebase:**
- Time: 150-250 hours (SQLite → Firestore NoSQL, data model restructuring)
- Difficulty: HARD (SQL → NoSQL migration, SDK replacement)
- Cost: $15K-25K developer time
- Not recommended (choose SQL or NoSQL upfront)

---

### Mitigation Strategies

**Already Low Lock-In** (50/100 is lowest among BaaS)

**Best Practices:**
1. **Use PocketBase SDK minimally** (abstract behind your own API if concerned)
2. **Standard SQL only** (avoid PocketBase-specific features)
3. **Regular SQLite backups** (easy to migrate to PostgreSQL anytime)
4. **Avoid complex real-time** (easy to replace with Pusher, Ably if needed)

**Recommended Approach:** PocketBase is **low-risk** for lock-in. Use it for MVPs, self-host on $5 VPS, migrate to Supabase/PostgreSQL when scaling demands it.

---

## 8. Pricing Structure

### Free Forever (Self-Hosted)

**Monthly Cost:** $0 (no licensing fees, MIT open-source)

**Infrastructure Costs:**
- **VPS:** $5-50/month (Hetzner, DigitalOcean, Linode)
  - $5/month: 1 vCPU, 1 GB RAM, 25 GB SSD (sufficient for 1K-5K users)
  - $12/month: 2 vCPU, 2 GB RAM, 50 GB SSD (sufficient for 5K-20K users)
  - $24/month: 2 vCPU, 4 GB RAM, 80 GB SSD (sufficient for 20K-100K users)
- **Backups:** $2-5/month (automated backups via VPS provider)
- **Monitoring:** $0-10/month (Uptime Robot free, Betterstack $10/month)

**Total Cost Examples:**

**Hobby Project (1K users, 5 GB database):**
- Hetzner CX11 VPS: $5/month
- **Total:** $5/month

**Side Project (5K users, 20 GB database):**
- Hetzner CX21 VPS: $12/month
- **Total:** $12/month

**Small Business (20K users, 50 GB database):**
- Hetzner CX31 VPS: $24/month
- Backups: $5/month
- **Total:** $29/month

**Scaling SaaS (100K users, 100 GB database):**
- Hetzner CX41 VPS: $48/month
- Backups: $10/month
- Monitoring: $10/month
- **Total:** $68/month

**Break-Even Point:** PocketBase is **always cheaper** than managed BaaS (Supabase $25+/month, Firebase $50-500/month) if you handle DevOps.

---

### Community Cloud Hosting (Unofficial)

**PocketHost (pockethost.io):**
- Free tier: 1 project, 100 MB storage, 1 GB bandwidth
- Pro tier: $10/month per project, 10 GB storage, 100 GB bandwidth
- Not official PocketBase (community service, use at own risk)

---

## 9. Competitive Advantages

### vs. Supabase

**PocketBase Wins:**
- Zero cost ($5 VPS vs $25/month Supabase Pro)
- Simplest deployment (single binary vs 10+ Docker containers)
- Lowest lock-in (50/100 vs 75/100)
- No vendor dependency (self-hosted, MIT open-source)

**Supabase Wins:**
- Managed cloud (no DevOps required)
- PostgreSQL (scales better than SQLite)
- Real-time subscriptions (WebSocket vs SSE)
- Edge Functions (global CDN, sub-50ms latency)

---

### vs. Firebase

**PocketBase Wins:**
- Zero cost ($5 VPS vs $50-500/month Firebase)
- SQL database (joins, easier migration)
- Lowest lock-in (50/100 vs 85/100)
- Self-hosted (no vendor lock-in)

**Firebase Wins:**
- Better mobile SDKs (offline sync, push notifications)
- Managed cloud (no server management)
- Comprehensive platform (analytics, crashlytics, hosting)
- Google-backed (safest long-term)

---

### vs. Appwrite

**PocketBase Wins:**
- Simpler deployment (1 binary vs 10+ Docker containers)
- Lower resource usage (15 MB vs 2 GB RAM for Appwrite)
- Faster setup (2 minutes vs 15 minutes)

**Appwrite Wins:**
- Multi-language functions (Python, Go, Ruby vs Go only)
- NoSQL option (if NoSQL preferred)
- Managed cloud option (Appwrite Cloud)

---

## 10. Strategic Viability: 50/100 (UNCERTAIN)

### Project Status

**Maintainer:** Gani Georgiev (solo developer)
**Funding:** None (independent project, not VC-backed)
**Business Model:** Free forever (donations accepted)
**License:** MIT (open-source, no commercial restrictions)

**Risk Assessment:**
- **Acquisition Risk:** NONE (no company to acquire)
- **Shutdown Risk:** MODERATE (single maintainer, if stops, community must fork)
- **Pricing Risk:** NONE (free forever, MIT license)
- **Feature Risk:** MODERATE (development pace depends on maintainer availability)

---

### Timeline Outlook

**2025-2027:** ACTIVE DEVELOPMENT
- Regular releases (v0.20+ in 2025)
- Active community (40K+ GitHub stars, 7K+ Discord members)
- Feature additions (full-text search, multi-tenancy, clustering planned)

**2027-2030:** UNCERTAIN
- Maintainer may slow down (burnout, life changes)
- Community may fork (MIT license allows this)
- Potential: Company formed around PocketBase (commercial support, managed cloud)

**Mitigation:**
- **MIT License:** Community can maintain if maintainer stops
- **Simple codebase:** Easy for community to fork and continue
- **Low lock-in:** Easy to migrate to Supabase/PostgreSQL if project stagnates

**Verdict:** PocketBase is **low-risk for short-term** (2-3 years), **moderate-risk for long-term** (5-10 years). Use for MVPs, plan migration to Supabase when scaling or if project stagnates.

---

## 11. Use Case Fit

### Ideal For:

- **MVPs and prototypes** - Fastest deployment, zero cost
- **Indie hackers and side projects** - $5-12/month total cost
- **Self-hosting advocates** - Full control, no vendor lock-in
- **Cost-conscious startups** - Zero BaaS cost, only VPS cost
- **Small-scale apps** - 1K-50K users (SQLite scaling limits)
- **Learning and education** - Simple architecture, easy to understand

### NOT Ideal For:

- **High-concurrency writes** - SQLite bottleneck (>100 writes/sec)
- **Large databases** - SQLite practical limit ~100 GB
- **Distributed systems** - No clustering, single-server only
- **Enterprise compliance** - No SOC 2, HIPAA (self-hosted means you're responsible)
- **Teams without DevOps** - Self-hosting requires server management skills

---

## 12. Summary Verdict

**PocketBase is the best BaaS for MVPs, indie hackers, and cost-conscious developers** who can self-host and accept SQLite scaling limits.

**Strengths:**
- Simplest deployment (single binary, 2-minute setup)
- Zero cost ($5-12/month VPS only)
- Lowest lock-in (50/100, standard SQL + REST API)
- Full SQL support (joins, transactions, standard SQLite)
- Admin UI (no-code database management)
- MIT open-source (no vendor lock-in, community can fork)

**Weaknesses:**
- Self-hosted only (requires DevOps skills)
- SQLite scaling limits (>100 writes/sec → migrate to PostgreSQL)
- Single maintainer risk (project may stagnate if maintainer stops)
- Limited real-time (SSE only, not full WebSocket)
- No managed cloud (must handle server, backups, monitoring)

**Recommendation:**
- **Use PocketBase** for MVPs, side projects, learning (fastest + cheapest)
- **Accept 50/100 lock-in** (lowest among BaaS, easy migration path)
- **Plan migration** when concurrent writes exceed 100/sec or database exceeds 50 GB
- **Migrate to Supabase** when scaling demands PostgreSQL (60-100 hours, $6K-10K cost)
- **Moderate viability** (50/100, single maintainer risk, but MIT license allows community fork)

**When to Choose PocketBase:**
1. Building MVP or prototype (validate idea fast)
2. Budget constraint ($0-12/month hosting)
3. Self-hosting preference (full control, data sovereignty)
4. Small-scale app (1K-50K users, <100 writes/sec)
5. Learning backend development (simple architecture)

**When to Avoid PocketBase:**
1. High-concurrency writes (>100 writes/sec → use Supabase)
2. Large database (>100 GB → use PostgreSQL)
3. No DevOps skills (use managed BaaS like Supabase, Firebase)
4. Enterprise compliance required (SOC 2, HIPAA → use Firebase, Supabase Enterprise)
5. Need managed cloud (use Supabase, Firebase)

**Lock-In Score:** 50/100 (LOWEST - easiest migration)
**Viability Score:** 50/100 (MODERATE - single maintainer risk)
**Overall Recommendation:** HIGHLY RECOMMENDED for MVPs and indie hackers, MIGRATE to Supabase when scaling
