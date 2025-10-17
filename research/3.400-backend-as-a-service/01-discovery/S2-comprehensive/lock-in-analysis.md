# BaaS Lock-In Severity Analysis

## Comprehensive Vendor Lock-In Assessment

**Date:** October 10, 2025
**Assessment:** Migration difficulty, time estimates, lock-in scores

---

## Lock-In Severity Rankings (0-100 Scale)

**Scale Definition:**
- **0-30:** Very Low Lock-In (migration 20-40 hours, standard APIs)
- **31-60:** Low Lock-In (migration 40-80 hours, mostly standard tech)
- **61-75:** Moderate Lock-In (migration 80-150 hours, some proprietary APIs)
- **76-85:** High Lock-In (migration 150-300 hours, significant proprietary integration)
- **86-100:** Very High Lock-In (migration 300+ hours, deep proprietary dependencies)

### Rankings

| Provider | Lock-In Score | Migration Time | Difficulty Rating | Primary Lock-In Factor |
|----------|---------------|----------------|-------------------|------------------------|
| **PocketBase** | 50/100 | 60-100 hours | ⚠️ LOW | Standard REST API, SQLite portability |
| **Xata** | 65/100 | 100-180 hours | ⚠️ MODERATE | Proprietary REST API + integrated search |
| **Nhost** | 70/100 | 150-250 hours | ⚠️ MODERATE | Hasura GraphQL APIs, PostgreSQL underneath |
| **Appwrite** | 70/100 | 120-220 hours | ⚠️ MODERATE | Proprietary APIs, NoSQL migration to SQL |
| **Supabase** | 75/100 | 80-120 hours | ⚠️ MODERATE-HIGH | RLS policies, real-time subscriptions |
| **Firebase** | 85/100 | 200-400 hours | 🚨 VERY HIGH | Firestore NoSQL, proprietary SDKs, real-time listeners |

---

## Component-by-Component Lock-In Analysis

### Database Lock-In

| Provider | Database Type | Export Format | Migration Difficulty | Time Estimate |
|----------|---------------|---------------|----------------------|---------------|
| **PocketBase** | SQLite | SQL dump, .db file | ✅ EASY | 8-16 hours |
| **Supabase** | PostgreSQL | pg_dump (standard) | ✅ EASY | 8-16 hours |
| **Xata** | PostgreSQL | pg_dump + wire protocol | ✅ EASY | 8-16 hours |
| **Nhost** | PostgreSQL | pg_dump (standard) | ✅ EASY | 8-16 hours |
| **Appwrite** | MariaDB (NoSQL API) | JSON export | 🚨 HARD | 60-120 hours |
| **Firebase** | Firestore (NoSQL) | JSON export | 🚨 VERY HARD | 80-200 hours |

**Insight:** SQL databases (PostgreSQL, SQLite) have EASY migration (8-16 hours). NoSQL databases (Firestore, Appwrite) have HARD migration (60-200 hours) due to schema restructuring.

**Firestore → PostgreSQL Migration Challenges:**
1. Document collections → SQL tables (schema design)
2. Nested documents → normalized tables (requires joins)
3. Array fields → junction tables (many-to-many relations)
4. Firestore queries → SQL queries (rewrite logic)
5. Denormalized data → normalized schema (data integrity)

**Example:** Firestore `users` collection with nested `posts` array → PostgreSQL `users` and `posts` tables with foreign keys. Requires 80-200 hours to restructure data model and rewrite queries.

---

### API / SDK Lock-In

| Provider | API Type | Portability | Migration Difficulty | Time Estimate |
|----------|----------|-------------|----------------------|---------------|
| **PocketBase** | Standard REST | ✅ HIGH | ✅ EASY | 16-32 hours |
| **Xata** | Proprietary REST + TypeScript SDK | ⚠️ MODERATE | ⚠️ MODERATE | 40-80 hours |
| **Supabase** | PostgREST + Supabase SDK | ⚠️ MODERATE | ⚠️ MODERATE | 32-60 hours |
| **Appwrite** | Proprietary REST + SDKs | ⚠️ MODERATE | ⚠️ MODERATE | 40-80 hours |
| **Nhost** | Hasura GraphQL + Nhost SDK | 🚨 LOW | 🚨 HARD | 80-150 hours |
| **Firebase** | Firebase SDK (proprietary) | 🚨 VERY LOW | 🚨 VERY HARD | 100-200 hours |

**Insight:** Standard REST APIs (PocketBase) are easiest to migrate (16-32 hours). Proprietary SDKs (Firebase, Supabase) require rewriting API calls throughout codebase (32-200 hours).

**Firebase SDK Lock-In Example:**
```javascript
// Firebase SDK calls throughout codebase
import { getFirestore, collection, query, where, getDocs } from 'firebase/firestore';

const db = getFirestore();
const q = query(collection(db, 'users'), where('age', '>', 18));
const querySnapshot = await getDocs(q);

// Must rewrite to Supabase/PostgreSQL/REST API
// Potentially 100+ files with Firebase SDK calls
// Estimated: 100-200 hours to rewrite all Firebase calls
```

---

### Authentication Lock-In

| Provider | Auth System | User Export | Migration Difficulty | Time Estimate |
|----------|-------------|-------------|----------------------|---------------|
| **PocketBase** | JWT-based | SQLite export | ✅ EASY | 16-24 hours |
| **Supabase** | Supabase Auth (GoTrue) | PostgreSQL export | ⚠️ MODERATE | 24-40 hours |
| **Appwrite** | Appwrite Auth | API export | ⚠️ MODERATE | 24-40 hours |
| **Nhost** | Hasura Auth | PostgreSQL export | ⚠️ MODERATE | 24-40 hours |
| **Firebase** | Firebase Authentication | Firebase Admin SDK export | ⚠️ MODERATE | 24-40 hours |
| **Xata** | N/A (bring-your-own) | N/A (Auth0, Clerk) | ✅ EASY | 4-8 hours |

**Insight:** Auth migration is MODERATE difficulty (24-40 hours) for most BaaS due to password hashing differences and SDK rewrites. Xata has EASY migration (4-8 hours) since auth is external (Auth0, Clerk).

**Password Hashing Migration Challenge:**
- Firebase uses scrypt hashing (Google-specific parameters)
- Supabase uses bcrypt hashing
- Migration requires re-hashing passwords or asking users to reset passwords
- Alternative: Implement custom password verification with Firebase scrypt parameters

---

### Real-Time Lock-In

| Provider | Real-Time Tech | Migration Difficulty | Time Estimate |
|----------|----------------|----------------------|---------------|
| **PocketBase** | Server-Sent Events (SSE) | ⚠️ MODERATE | 16-24 hours |
| **Supabase** | PostgreSQL replication + WebSocket | 🚨 HARD | 40-80 hours |
| **Firebase** | Native Firestore listeners | 🚨 VERY HARD | 40-80 hours |
| **Appwrite** | WebSocket subscriptions | ⚠️ MODERATE | 24-40 hours |
| **Nhost** | Hasura GraphQL subscriptions | 🚨 HARD | 40-80 hours |
| **Xata** | N/A (not available) | N/A | N/A |

**Insight:** Real-time features are the HIGHEST lock-in component (40-80 hours to migrate). Proprietary real-time APIs (Supabase, Firebase, Nhost) require extensive rewrites.

**Supabase Real-Time Migration Example:**
```javascript
// Supabase real-time subscription
const channel = supabase
  .channel('posts')
  .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'posts' }, payload => {
    console.log('New post:', payload.new);
  })
  .subscribe();

// Must rewrite to Pusher, Ably, or custom WebSocket server
// Potentially 50+ real-time subscriptions throughout codebase
// Estimated: 40-80 hours to replace all real-time logic
```

---

### Storage Lock-In

| Provider | Storage Type | Migration Difficulty | Time Estimate |
|----------|--------------|----------------------|---------------|
| **PocketBase** | Local filesystem | ✅ EASY | 4-8 hours |
| **Supabase** | S3-compatible | ✅ EASY | 8-16 hours |
| **Firebase** | Google Cloud Storage | ⚠️ MODERATE | 8-16 hours |
| **Appwrite** | S3-compatible | ✅ EASY | 8-16 hours |
| **Xata** | File attachments (with records) | ⚠️ MODERATE | 8-16 hours |
| **Nhost** | S3-compatible | ✅ EASY | 8-16 hours |

**Insight:** Storage migration is EASY (8-16 hours) for S3-compatible providers (Supabase, Appwrite, Nhost). Firebase requires export from GCS to S3, still relatively easy.

---

### Serverless Functions Lock-In

| Provider | Function Platform | Migration Difficulty | Time Estimate |
|----------|------------------|----------------------|---------------|
| **Supabase** | Deno Edge Functions | ⚠️ MODERATE | 16-40 hours |
| **Firebase** | Cloud Functions for Firebase | ⚠️ MODERATE | 16-40 hours |
| **PocketBase** | Go extensibility | 🚨 HARD | 40-80 hours |
| **Appwrite** | Appwrite Functions | ⚠️ MODERATE | 16-40 hours |
| **Nhost** | Node.js functions | ⚠️ MODERATE | 16-40 hours |
| **Xata** | N/A (use external) | ✅ EASY | 0 hours |

**Insight:** Function migration is MODERATE difficulty (16-40 hours) for most BaaS. PocketBase is HARD (40-80 hours) because Go extensibility is embedded in app code.

---

## Total Migration Time Estimates

### PocketBase → Alternative BaaS
**Target:** Supabase, Nhost, or self-hosted PostgreSQL

| Component | Time Estimate | Difficulty |
|-----------|---------------|------------|
| Database (SQLite → PostgreSQL) | 8-16 hours | ✅ EASY |
| API calls (REST → Supabase SDK) | 16-32 hours | ⚠️ MODERATE |
| Authentication | 16-24 hours | ⚠️ MODERATE |
| Real-time (SSE → Supabase real-time) | 16-24 hours | ⚠️ MODERATE |
| Storage | 4-8 hours | ✅ EASY |
| **Total** | **60-100 hours** | **⚠️ LOW** |

---

### Supabase → Alternative BaaS
**Target:** Nhost, self-hosted PostgreSQL, or PaaS

| Component | Time Estimate | Difficulty |
|-----------|---------------|------------|
| Database (PostgreSQL → PostgreSQL) | 8-16 hours | ✅ EASY |
| API calls (Supabase SDK → new API) | 32-60 hours | ⚠️ MODERATE |
| Authentication (Supabase Auth → Auth0/Clerk) | 24-40 hours | ⚠️ MODERATE |
| Real-time (Supabase → Pusher/Ably) | 40-80 hours | 🚨 HARD |
| Storage | 8-16 hours | ✅ EASY |
| **Total** | **112-212 hours** (avg **80-120 hours** without real-time) | **⚠️ MODERATE-HIGH** |

**Mitigation:** If you avoid Supabase real-time features, migration reduces to 80-120 hours (MODERATE).

---

### Firebase → Alternative BaaS
**Target:** Supabase, Nhost, or self-hosted PostgreSQL

| Component | Time Estimate | Difficulty |
|-----------|---------------|------------|
| Database (Firestore → PostgreSQL) | 80-200 hours | 🚨 VERY HARD |
| API calls (Firebase SDK → new SDK) | 100-200 hours | 🚨 VERY HARD |
| Authentication (Firebase Auth → Auth0/Clerk) | 24-40 hours | ⚠️ MODERATE |
| Real-time (Firestore listeners → new real-time) | 40-80 hours | 🚨 HARD |
| Storage | 8-16 hours | ✅ EASY |
| Functions (Cloud Functions → PaaS) | 16-40 hours | ⚠️ MODERATE |
| **Total** | **268-576 hours** (avg **200-400 hours**) | **🚨 VERY HIGH** |

**Key Challenge:** Firestore NoSQL → PostgreSQL SQL requires complete data model redesign and query rewrites.

---

### Appwrite → Alternative BaaS
**Target:** Supabase, Nhost, or self-hosted PostgreSQL

| Component | Time Estimate | Difficulty |
|-----------|---------------|------------|
| Database (NoSQL → PostgreSQL) | 60-120 hours | 🚨 HARD |
| API calls (Appwrite SDK → new API) | 40-80 hours | ⚠️ MODERATE |
| Authentication | 24-40 hours | ⚠️ MODERATE |
| Real-time | 24-40 hours | ⚠️ MODERATE |
| Storage | 8-16 hours | ✅ EASY |
| Functions | 16-40 hours | ⚠️ MODERATE |
| **Total** | **172-336 hours** (avg **120-220 hours**) | **⚠️ MODERATE** |

---

### Nhost → Alternative BaaS
**Target:** Supabase or self-hosted PostgreSQL

| Component | Time Estimate | Difficulty |
|-----------|---------------|------------|
| Database (PostgreSQL → PostgreSQL) | 8-16 hours | ✅ EASY |
| API calls (Hasura GraphQL → REST/other GraphQL) | 80-150 hours | 🚨 HARD |
| Authentication | 24-40 hours | ⚠️ MODERATE |
| Real-time (GraphQL subscriptions → new real-time) | 40-80 hours | 🚨 HARD |
| Storage | 8-16 hours | ✅ EASY |
| Functions | 16-40 hours | ⚠️ MODERATE |
| **Total** | **176-342 hours** (avg **150-250 hours**) | **🚨 HIGH** |

**Key Challenge:** Hasura GraphQL APIs are Hasura-specific. Rewriting GraphQL queries to REST or different GraphQL server is time-consuming.

---

### Xata → Alternative BaaS
**Target:** Supabase or self-hosted PostgreSQL

| Component | Time Estimate | Difficulty |
|-----------|---------------|------------|
| Database (PostgreSQL → PostgreSQL) | 8-16 hours | ✅ EASY |
| API calls (Xata SDK → new API) | 40-80 hours | ⚠️ MODERATE |
| Search (Elasticsearch → Algolia/Typesense) | 40-80 hours | 🚨 HARD |
| Authentication (already external) | 4-8 hours | ✅ EASY |
| Real-time (not used) | 0 hours | N/A |
| Storage | 8-16 hours | ✅ EASY |
| **Total** | **100-200 hours** (avg **100-180 hours**) | **⚠️ MODERATE** |

**Key Challenge:** Integrated Elasticsearch search requires separate search service (Algolia, Typesense) and query rewrites.

---

## Lock-In Mitigation Strategies

### Strategy 1: Abstract BaaS Behind Your Own API Layer

**Approach:**
1. Create custom API (Express, Flask, FastAPI) that wraps BaaS calls
2. Frontend calls your API, not BaaS directly
3. When migrating, only rewrite API backend (not frontend)

**Example:**
```javascript
// Frontend calls your API (not Firebase directly)
const response = await fetch('/api/users');
const users = await response.json();

// Your API wraps Firebase (easy to swap out)
// server.js (Express API)
app.get('/api/users', async (req, res) => {
  const usersRef = collection(db, 'users');
  const snapshot = await getDocs(usersRef);
  res.json(snapshot.docs.map(doc => doc.data()));
});

// Later: Swap Firebase for Supabase (frontend unchanged)
app.get('/api/users', async (req, res) => {
  const { data } = await supabase.from('users').select('*');
  res.json(data);
});
```

**Trade-offs:**
- ✅ Reduces frontend lock-in (only API backend needs changes)
- ✅ Easier migration (50-60% time reduction)
- ❌ Adds complexity (maintain extra API layer)
- ❌ Slower initial development (build API first)

**Verdict:** Worth it if long-term migration is likely (>50% chance of switching BaaS).

---

### Strategy 2: Use BaaS Only for Core Features (Database, Auth)

**Approach:**
1. Use BaaS for database and auth only (standard features)
2. Avoid BaaS-specific features (real-time, functions, storage)
3. Use separate services (Pusher for real-time, Vercel for functions, S3 for storage)

**Trade-offs:**
- ✅ Lower lock-in (40-60% reduction)
- ✅ Easier migration (avoid real-time/functions lock-in)
- ❌ More services to manage (Pusher, S3, Vercel)
- ❌ Higher cost (pay for separate services)

**Verdict:** Good for projects with high migration risk or lock-in concerns.

---

### Strategy 3: Choose Low Lock-In BaaS from Day One

**Approach:**
1. Choose PocketBase (50/100 lock-in) or Supabase (75/100 lock-in)
2. Avoid Firebase (85/100 lock-in) and Nhost (70/100 lock-in for GraphQL)
3. Accept moderate lock-in for faster development

**Trade-offs:**
- ✅ Faster development (no abstraction layer)
- ✅ Lower migration cost (60-120 hours vs 200-400 hours)
- ❌ Still locked in (60-120 hours to migrate)

**Verdict:** Best for most projects. Balance speed and lock-in.

---

### Strategy 4: Self-Host from Day One

**Approach:**
1. Self-host PocketBase, Appwrite, or Supabase
2. You control deployment (no vendor cloud dependency)
3. Can maintain indefinitely (no forced migration)

**Trade-offs:**
- ✅ No vendor lock-in (self-hosted = full control)
- ✅ Can maintain forever (even if company shuts down)
- ❌ Requires DevOps expertise (Docker, backups, scaling)
- ❌ Slower initial setup (10-20 hours vs 1-2 hours managed cloud)

**Verdict:** Worth it if data sovereignty is critical (EU GDPR, healthcare HIPAA) or budget is tight.

---

## Lock-In Risk by Use Case

### Startup MVP (Likely to Scale, Migrate Later)
**Recommended:** PocketBase (50/100) → Migrate to Supabase when scaling
**Why:** Lowest lock-in allows easy migration when venture-funded

### Production SaaS (Long-Term Commitment)
**Recommended:** Supabase (75/100) with abstraction layer
**Why:** Balance of speed and reasonable lock-in, open-source exit strategy

### Mobile App (Offline Sync Required)
**Recommended:** Firebase (85/100) → Accept lock-in for offline sync features
**Why:** No alternative matches Firebase offline sync, lock-in justified

### Enterprise App (Data Sovereignty)
**Recommended:** Self-hosted PocketBase or Appwrite
**Why:** No cloud vendor lock-in, full control

### Side Project (Zero Budget)
**Recommended:** PocketBase (50/100) self-hosted
**Why:** Lowest lock-in + zero cost

---

## Summary: Lock-In Rankings

| Provider | Lock-In Score | Best Mitigation | Worst Lock-In Component | Migration Time |
|----------|---------------|-----------------|-------------------------|----------------|
| **PocketBase** | 50/100 | Use standard REST API | Go extensibility | 60-100 hours |
| **Xata** | 65/100 | Use Postgres wire protocol, separate search | Integrated Elasticsearch | 100-180 hours |
| **Appwrite** | 70/100 | Self-host, abstract API | NoSQL → SQL migration | 120-220 hours |
| **Nhost** | 70/100 | Self-host Hasura | Hasura GraphQL APIs | 150-250 hours |
| **Supabase** | 75/100 | Avoid real-time, abstract API | Real-time subscriptions | 80-120 hours |
| **Firebase** | 85/100 | Use sparingly (auth + simple DB only) | Firestore NoSQL migration | 200-400 hours |

**Bottom Line:** Choose PocketBase or Supabase for lowest practical lock-in. Avoid Firebase unless mobile offline sync is absolutely critical. All BaaS have 50-85/100 lock-in; plan for eventual migration.
