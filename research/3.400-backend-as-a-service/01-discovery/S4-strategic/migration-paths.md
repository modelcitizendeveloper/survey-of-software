# BaaS Migration Paths

**Experiment:** 2.200 Backend-as-a-Service
**Phase:** S4 Strategic Discovery
**Date:** October 10, 2025
**Topic:** Migration strategies, timelines, costs when exiting BaaS

---

## Executive Summary

All BaaS providers have **moderate-high lock-in** (50-85/100), with migration times ranging from **60-400 hours** ($6K-40K developer time). This guide provides detailed migration paths for moving between BaaS providers or to custom backends (PaaS).

**Key Finding:** SQL-based BaaS (Supabase, Nhost, PocketBase) have easier migration (60-180 hours) than NoSQL BaaS (Firebase, Appwrite) which require 150-400 hours due to data model restructuring.

---

## Migration Time Matrix

| From → To | Time (Hours) | Cost ($100/hr) | Difficulty | Key Challenge |
|-----------|--------------|----------------|------------|---------------|
| **PocketBase → Supabase** | 60-100 | $6K-10K | LOW-MOD | SQLite → PostgreSQL, SDK rewrite |
| **Supabase → Self-Hosted PG** | 80-120 | $8K-12K | MODERATE | RLS → API auth, real-time → Pusher |
| **Appwrite → Supabase** | 120-220 | $12K-22K | MOD-HARD | NoSQL → SQL, SDK rewrite |
| **Firebase → Supabase** | 200-400 | $20K-40K | VERY HARD | Firestore → PostgreSQL, offline sync |
| **Nhost → Supabase** | 150-250 | $15K-25K | MOD-HARD | GraphQL → REST, SDK rewrite |
| **Xata → Supabase** | 100-180 | $10K-18K | MODERATE | PostgreSQL → PostgreSQL, search → Algolia |

---

## Migration Path 1: PocketBase → Supabase

**Time:** 60-100 hours ($6K-10K)
**Difficulty:** LOW-MODERATE
**Reason:** Both SQL databases, SQLite → PostgreSQL migration standard

### Step-by-Step Migration

**Phase 1: Database Migration (20-30 hours)**

1. **Export SQLite data:**
```bash
# Dump SQLite to SQL
sqlite3 pb_data/data.db .dump > backup.sql

# Or export to CSV per table
sqlite3 pb_data/data.db "SELECT * FROM users" > users.csv
```

2. **Convert SQLite → PostgreSQL syntax:**
```bash
# Install converter
npm install -g sqlite-to-pg

# Convert SQL dump
sqlite-to-pg backup.sql > postgres.sql
```

3. **Import to Supabase:**
```bash
# Via Supabase CLI
supabase db push

# Or via psql
psql postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres < postgres.sql
```

4. **Verify data integrity:**
```sql
-- Compare row counts
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM posts;
```

---

**Phase 2: SDK Migration (20-40 hours)**

PocketBase → Supabase SDK rewrite:

**Before (PocketBase):**
```javascript
import PocketBase from 'pocketbase'
const pb = new PocketBase('http://localhost:8090')

// CRUD operations
const posts = await pb.collection('posts').getList(1, 20, {
  filter: 'published = true',
  sort: '-created'
})

const post = await pb.collection('posts').create({
  title: 'Hello',
  content: '...'
})
```

**After (Supabase):**
```javascript
import { createClient } from '@supabase/supabase-js'
const supabase = createClient('https://project.supabase.co', 'anon-key')

// CRUD operations
const { data: posts } = await supabase
  .from('posts')
  .select('*')
  .eq('published', true)
  .order('created', { ascending: false })
  .limit(20)

const { data: post } = await supabase
  .from('posts')
  .insert({ title: 'Hello', content: '...' })
```

**Changes Required:**
- Replace `pb.collection()` with `supabase.from()`
- Update filter syntax (PocketBase `'published = true'` → Supabase `.eq('published', true)`)
- Update authentication calls
- Rewrite real-time subscriptions (SSE → WebSocket)

---

**Phase 3: Real-Time Migration (10-20 hours)**

**Before (PocketBase SSE):**
```javascript
pb.collection('posts').subscribe('*', (e) => {
  console.log(e.action, e.record)
})
```

**After (Supabase WebSocket):**
```javascript
supabase
  .channel('posts')
  .on('postgres_changes', {
    event: 'INSERT',
    schema: 'public',
    table: 'posts'
  }, (payload) => {
    console.log('New post:', payload.new)
  })
  .subscribe()
```

---

**Phase 4: Authentication Migration (10-20 hours)**

**PocketBase users → Supabase auth:**
- Export user emails, passwords (hashed)
- Import to Supabase via Admin API
- Update frontend auth calls

---

**Total Time:** 60-100 hours
**Cost:** $6K-10K developer time
**Downtime:** 2-6 hours (database migration + DNS switch)

---

## Migration Path 2: Firebase → Supabase

**Time:** 200-400 hours ($20K-40K)
**Difficulty:** VERY HARD
**Reason:** Firestore NoSQL → PostgreSQL SQL, offline sync rewrite

### Key Challenges

1. **Data Model Restructuring (80-150 hours):**
   - Firestore nested documents → PostgreSQL normalized tables
   - Subcollections → JOIN tables
   - Document references → Foreign keys
   - Denormalized data → Normalized schema

2. **Query Rewrite (50-100 hours):**
   - Firestore queries → SQL queries
   - No joins in Firestore → SQL JOINs
   - Client-side filtering → Server-side WHERE clauses

3. **Offline Sync (40-80 hours):**
   - Firebase offline persistence → Manual local storage + sync
   - Requires implementing conflict resolution, write queues
   - Or use local-first libraries (RxDB, WatermelonDB)

4. **SDK Rewrite (30-70 hours):**
   - Firebase SDK → Supabase SDK throughout app
   - Real-time listeners syntax changes
   - Authentication API changes

---

### Data Model Conversion Example

**Before (Firestore):**
```javascript
// Collection: users
users/user123
  name: "John"
  email: "john@example.com"
  posts: [
    { title: "Post 1", content: "..." },
    { title: "Post 2", content: "..." }
  ]
```

**After (PostgreSQL):**
```sql
-- Table: users
CREATE TABLE users (
  id UUID PRIMARY KEY,
  name TEXT,
  email TEXT UNIQUE
);

-- Table: posts (normalized)
CREATE TABLE posts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  title TEXT,
  content TEXT
);
```

---

**Total Time:** 200-400 hours
**Cost:** $20K-40K developer time
**Downtime:** 8-24 hours (data migration + testing)

**Recommendation:** Avoid Firebase → Supabase migration unless absolutely necessary. Choose SQL upfront if migration likely.

---

## Migration Path 3: Supabase → Self-Hosted PostgreSQL

**Time:** 80-120 hours ($8K-12K)
**Difficulty:** MODERATE
**Reason:** PostgreSQL → PostgreSQL (same database), but APIs must be rewritten

### Step-by-Step Migration

**Phase 1: Database Export (2-4 hours)**

```bash
# Export Supabase database via CLI
supabase db dump -f backup.sql

# Or via pg_dump
pg_dump postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres > backup.sql
```

**Phase 2: Self-Hosted PostgreSQL Setup (8-16 hours)**

```bash
# Install PostgreSQL on VPS (Ubuntu)
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb myapp

# Import data
psql myapp < backup.sql

# Configure pg_bouncer (connection pooling)
sudo apt install pgbouncer
```

**Phase 3: Backend API Rewrite (40-60 hours)**

Replace Supabase SDK with custom API (Express, Flask, FastAPI):

**Before (Supabase SDK):**
```javascript
// Frontend calls Supabase directly
const { data } = await supabase.from('posts').select('*')
```

**After (Custom API):**
```javascript
// Backend API (Express)
app.get('/api/posts', async (req, res) => {
  const posts = await pool.query('SELECT * FROM posts')
  res.json(posts.rows)
})

// Frontend calls custom API
const response = await fetch('/api/posts')
const posts = await response.json()
```

**Changes Required:**
- Build REST API (Express, Flask, FastAPI) for all CRUD operations
- Implement Row-Level Security as API authorization logic
- Replace Supabase SDK calls with fetch/axios

---

**Phase 4: Real-Time Migration (20-40 hours)**

Replace Supabase real-time with Pusher, Ably, or Socket.io:

**Before (Supabase Real-Time):**
```javascript
supabase.channel('posts').on('postgres_changes', ...).subscribe()
```

**After (Pusher):**
```javascript
const pusher = new Pusher('app-key', { cluster: 'us2' })
const channel = pusher.subscribe('posts')
channel.bind('new-post', (data) => {
  console.log('New post:', data)
})
```

Backend triggers Pusher when database changes:
```javascript
app.post('/api/posts', async (req, res) => {
  const post = await pool.query('INSERT INTO posts ... RETURNING *')

  // Trigger Pusher
  pusher.trigger('posts', 'new-post', post.rows[0])

  res.json(post.rows[0])
})
```

---

**Phase 5: Authentication Migration (10-20 hours)**

Replace Supabase Auth with Passport.js, Auth0, or custom JWT:

**Before (Supabase Auth):**
```javascript
await supabase.auth.signInWithPassword({ email, password })
```

**After (Passport.js):**
```javascript
app.post('/api/login', passport.authenticate('local'), (req, res) => {
  res.json({ token: generateJWT(req.user) })
})
```

---

**Total Time:** 80-120 hours
**Cost:** $8K-12K developer time
**Downtime:** 2-6 hours (database migration + API cutover)

**Break-Even:** When Supabase costs exceed $500-1K/month, self-hosting becomes cheaper ($100-300/month PaaS + PostgreSQL + S3).

---

## Migration Path 4: Appwrite → Supabase

**Time:** 120-220 hours ($12K-22K)
**Difficulty:** MODERATE-HARD
**Reason:** NoSQL → SQL, multi-language functions → TypeScript only

### Key Challenges

1. **Data Model Restructuring (60-100 hours):**
   - Appwrite collections (NoSQL) → PostgreSQL tables (SQL)
   - Document attributes → Table columns
   - Nested documents → JOIN tables

2. **SDK Rewrite (30-60 hours):**
   - Appwrite SDK → Supabase SDK
   - Document permissions → Row-Level Security

3. **Functions Migration (30-60 hours):**
   - Multi-language functions (Python, Go, Ruby) → TypeScript Edge Functions
   - Or: Use PaaS (Railway, Render) for Python/Go functions

---

**Total Time:** 120-220 hours
**Cost:** $12K-22K developer time

---

## BaaS → PaaS Migration (Custom Backend)

**Time:** 150-300 hours ($15K-30K)
**Difficulty:** HARD
**Reason:** Build custom backend from scratch (Express, Flask, Django, FastAPI)

### When to Migrate to PaaS

1. **BaaS constraints too limiting:** Need custom backend logic (ML, PDF generation, complex workflows)
2. **Costs exceed $500-1K/month:** Self-hosted backend cheaper at scale
3. **Acquisition/repricing:** BaaS acquired, pricing increased 3-5x
4. **Lock-in concerns:** Reduce vendor dependency, full control

### Custom Backend Stack Options

**Option 1: Express (Node.js) + PostgreSQL**
- Time: 150-250 hours
- Cost: $15K-25K
- Deploy to: Railway, Render, Fly.io ($10-50/month)

**Option 2: Flask (Python) + PostgreSQL**
- Time: 150-250 hours
- Cost: $15K-25K
- Deploy to: Railway, Render, Fly.io ($10-50/month)

**Option 3: FastAPI (Python) + PostgreSQL**
- Time: 150-250 hours
- Cost: $15K-25K
- Deploy to: Railway, Render, Fly.io ($10-50/month)

---

## Migration Timeline Planning

### 3-6 Months Before Migration

1. **Audit current BaaS usage:**
   - List all collections/tables, APIs, functions
   - Document data model, relationships
   - Identify BaaS-specific features (real-time, RLS, storage)

2. **Choose target platform:**
   - Another BaaS (Supabase, Firebase, PocketBase)
   - Self-hosted PostgreSQL
   - Custom backend (PaaS + PostgreSQL)

3. **Budget time and cost:**
   - Developer hours (60-400 hours)
   - Cost ($6K-40K at $100/hour)
   - Downtime window (2-24 hours)

---

### 1-3 Months Before Migration

1. **Set up target environment:**
   - Provision database, API server, storage
   - Test data migration script (staging environment)
   - Rewrite critical APIs

2. **Parallel development:**
   - Keep existing BaaS running (production)
   - Build new backend (staging)
   - Test thoroughly (unit tests, integration tests)

---

### 1 Week Before Migration

1. **Final preparation:**
   - Freeze feature development
   - Announce maintenance window to users
   - Backup all data (full export)

2. **Staging cutover:**
   - Run full migration on staging
   - Test all features (CRUD, auth, real-time, storage)
   - Measure performance (latency, throughput)

---

### Migration Day

1. **Maintenance mode:**
   - Enable read-only mode (prevent new writes)
   - Display maintenance banner

2. **Data migration:**
   - Export database (pg_dump, SQLite dump, Firestore export)
   - Import to new database
   - Verify data integrity (row counts, checksums)

3. **API cutover:**
   - Update DNS (point to new API)
   - Deploy new frontend (with new SDK)
   - Monitor errors (Sentry, rollbar)

4. **Go live:**
   - Disable maintenance mode
   - Monitor performance (24 hours)
   - Keep old BaaS running 1-2 weeks (rollback option)

---

### 1-2 Weeks After Migration

1. **Monitor closely:**
   - Error rates (Sentry, rollbar)
   - Performance (latency, throughput)
   - User complaints (support tickets)

2. **Rollback plan:**
   - Keep old BaaS accessible (1-2 weeks)
   - If critical issues, rollback to old BaaS
   - Fix issues, retry migration

3. **Decommission old BaaS:**
   - After 1-2 weeks stable, shut down old BaaS
   - Final data export (archive)
   - Cancel subscription

---

## Cost Breakdown

### Developer Time (Largest Cost)

| Migration | Hours | Cost ($100/hr) | Difficulty |
|-----------|-------|----------------|------------|
| PocketBase → Supabase | 60-100 | $6K-10K | LOW-MOD |
| Xata → Supabase | 100-180 | $10K-18K | MODERATE |
| Appwrite → Supabase | 120-220 | $12K-22K | MOD-HARD |
| Nhost → Supabase | 150-250 | $15K-25K | MOD-HARD |
| Firebase → Supabase | 200-400 | $20K-40K | VERY HARD |

### Infrastructure Costs

**Parallel Running (1-4 weeks):**
- Old BaaS: $25-500/month (continue paying during migration)
- New backend: $10-500/month (staging + production)
- **Total:** $35-1000/month for 1-4 weeks

### Downtime Costs

**Maintenance Window:**
- Small app: 2-6 hours (minimal revenue loss)
- Large app: 8-24 hours (negotiate maintenance window, inform users)
- **Revenue loss:** Varies (e-commerce: 8 hours = 1-2 days revenue loss)

---

## Migration Decision Framework

### When to Migrate

**Forced Migration (Act Immediately):**
- BaaS acquired, pricing increased 3-5x
- BaaS shutdown announced (1 year notice typically)
- Major outages (15+ hours downtime, losing customer trust)

**Strategic Migration (Plan 3-6 Months):**
- Costs exceed $500-1K/month (self-hosting cheaper)
- Need features BaaS doesn't offer (custom logic, ML, PDF generation)
- Acquisition announced (prepare for repricing)

**Opportunistic Migration (Optional):**
- Better pricing on new BaaS ($50-200/month savings)
- Learning new technology (Docker, Kubernetes)
- Reducing lock-in (75/100 → 50/100)

---

### Migration ROI Calculation

**Example: Supabase ($500/month) → Self-Hosted PostgreSQL ($150/month)**

**Costs:**
- Migration time: 100 hours × $100/hour = $10,000
- Parallel infrastructure: $650/month × 1 month = $650
- Downtime revenue loss: $2,000 (estimated)
- **Total migration cost:** $12,650

**Savings:**
- Monthly savings: $500 - $150 = $350/month
- Payback period: $12,650 / $350 = **36 months (3 years)**

**ROI Analysis:**
- Year 1: -$12,650 + ($350 × 12) = -$8,450 (loss)
- Year 2: -$8,450 + ($350 × 12) = -$4,250 (loss)
- Year 3: -$4,250 + ($350 × 12) = -$50 (break-even)
- Year 4+: $350/month profit = **$4,200/year savings**

**Verdict:** Migration pays off after 3 years. Only migrate if planning to stay on platform 3+ years.

---

## Bottom Line

**All BaaS have lock-in** (50-85/100). Migration is expensive (60-400 hours, $6K-40K).

**Choose BaaS Based on Lock-In:**
1. **PocketBase** (50/100) - Lowest lock-in, easiest migration (60-100 hours)
2. **Xata** (65/100) - Moderate lock-in (100-180 hours)
3. **Appwrite** (70/100) - Moderate lock-in (120-220 hours)
4. **Supabase** (75/100) - Moderate-high lock-in (80-120 hours to self-hosted)
5. **Firebase** (85/100) - Highest lock-in, avoid unless mobile critical (200-400 hours)

**Plan Migration When:**
- Costs exceed $500-1K/month (self-hosting cheaper)
- BaaS acquired/repriced (forced migration)
- Need custom backend logic (BaaS too limiting)

**Accept Lock-In If:**
- MVP validation (2-3 years, migration risk low)
- Low lock-in provider (PocketBase 50/100, Supabase 75/100)
- Budget for migration ($6K-40K) when scaling

**Choose Firebase ONLY IF:**
- Mobile offline sync is critical (accept 85/100 lock-in for this feature)
- Otherwise, choose Supabase (lower lock-in, SQL, easier migration)
