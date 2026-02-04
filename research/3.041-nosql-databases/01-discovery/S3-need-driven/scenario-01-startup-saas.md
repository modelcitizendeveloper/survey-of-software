# S3 Scenario 1: Startup SaaS Application

**Use Case:** B2B SaaS product (project management, CRM, analytics tool)
**Scale:** 0 → 10K users in Year 1, 10K → 50K in Year 2
**Budget:** Bootstrap / seed stage ($0-5K/month infrastructure)

---

## Requirements

### Functional
- User profiles and authentication data
- Multi-tenant data isolation (per-workspace/organization)
- Activity logs and audit trails
- Document storage (settings, configurations, templates)
- Search functionality (projects, tasks, users)
- Real-time collaboration features (optional)

### Non-Functional
- **Availability:** 99.9% (some downtime acceptable)
- **Latency:** <100ms p99 (not mission-critical)
- **Scalability:** Must scale from 10 to 50K users without migration
- **Cost:** Free tier for 6 months, <$100/month Year 1, <$500/month Year 2
- **Development Speed:** Solo founder or small team (2-3 devs)

---

## Data Model Analysis

**Primary data types:**
1. **User profiles:** Document structure (name, email, settings, preferences)
2. **Workspaces/Organizations:** Document structure (settings, team members)
3. **Activity data:** Time-series (user actions, audit logs)
4. **Configuration documents:** Nested JSON (templates, workflows)
5. **Relationships:** Moderate (users → workspaces, projects → tasks)

**Access patterns:**
- Get user by ID (frequent)
- Get workspace + all members (frequent)
- Query projects by workspace (frequent)
- Search across entities (occasional)
- Audit log queries (rare)

**Data model fit:**
- ✅ **Document database:** Excellent (nested user/workspace objects)
- ⚠️ **Key-value:** Workable (partition by workspace ID)
- ⚠️ **Wide-column:** Overkill (not time-series heavy)
- ❌ **Graph:** Overkill (relationships not core feature)

---

## Database Recommendation

### Primary Recommendation: **MongoDB Atlas (Serverless)**

**Why MongoDB:**
1. ✅ **Document model fits perfectly** (users, workspaces, settings are JSON)
2. ✅ **Flexible schema** (rapid iteration, add features without migrations)
3. ✅ **Rich queries** (filter by workspace, user, date ranges)
4. ✅ **Free tier** (512MB, enough for first 100-500 users)
5. ✅ **Atlas Search** (full-text search without separate service)
6. ✅ **Serverless option** (pay-as-you-go, perfect for unpredictable growth)
7. ✅ **Ecosystem** (ORMs, tools, documentation for fast development)

**Migration path:**
- Free tier (0-500 users, 6 months)
- Serverless ($5-20/month, 500-5K users, Year 1)
- M10 dedicated ($57/month, 5K-20K users, Year 2)
- M20 ($148/month, 20K-50K users, Year 2)

**3-Year TCO:**
- Year 1: $0-6 months, $5-20/month next 6 months = ~$60
- Year 2: $57-148/month = ~$1,200
- Year 3: $148-480/month = ~$3,000
- **Total: ~$4,260 over 3 years**

---

### Alternative: **DynamoDB (Serverless)**

**Why DynamoDB:**
1. ✅ **Generous free tier** (25GB, permanent)
2. ✅ **True serverless** (zero cost at zero usage)
3. ✅ **AWS integration** (if using Lambda, API Gateway)
4. ✅ **Predictable low cost** ($5-30/month at scale)

**Trade-offs:**
1. ❌ **Limited queries** (must design access patterns upfront)
2. ❌ **Single-table design** (complex data modeling)
3. ❌ **No full-text search** (need separate service)
4. ❌ **AWS lock-in** (hard to migrate)

**When to choose DynamoDB:**
- Already committed to AWS
- Access patterns are simple (get by ID, list by workspace)
- Cost minimization critical
- Don't need complex queries

**3-Year TCO:**
- Year 1: $0 (free tier)
- Year 2: $30/month = $360
- Year 3: $50/month = $600
- **Total: ~$960 over 3 years** (3.4× cheaper than MongoDB)

---

### Alternative: **Supabase (PostgreSQL + Real-Time)**

**Why Supabase:**
1. ✅ **Relational + real-time** (best of both worlds)
2. ✅ **Built-in auth, storage, functions** (complete platform)
3. ✅ **Free tier** (500MB database, 2GB egress)
4. ✅ **Real-time subscriptions** (WebSocket built-in)
5. ✅ **$25/month Pro tier** (8GB database, 50GB storage, very affordable)

**Trade-offs:**
1. ⚠️ **Relational model** (requires schema design, migrations)
2. ⚠️ **Less flexible** than document DB (schema changes need migrations)
3. ✅ **PostgreSQL portability** (can migrate to any Postgres provider)

**When to choose Supabase:**
- Want relational data model
- Need built-in auth + real-time
- Value open source and portability
- Budget-constrained ($25/month for years)

**3-Year TCO:**
- Year 1: $0 (free tier)
- Year 2-3: $25/month = $600
- **Total: ~$600 over 3 years** (7× cheaper than MongoDB)

---

## Decision Matrix

| Factor | MongoDB Atlas | DynamoDB | Supabase |
|--------|---------------|----------|----------|
| **Free tier** | 512MB | 25GB | 500MB DB |
| **Year 1 cost** | $60 | $0 | $0 |
| **Year 2-3 cost** | $1,200-3,000 | $360-600 | $600 |
| **3-Year TCO** | $4,260 | $960 | $600 |
| **Query flexibility** | ✅ Excellent | ❌ Limited | ✅ SQL |
| **Schema flexibility** | ✅ Schemaless | ✅ Schemaless | ⚠️ Schema required |
| **Full-text search** | ✅ Built-in | ❌ Need external | ⚠️ Need extension |
| **Real-time** | ⚠️ Change streams | ❌ Streams + custom | ✅ Built-in |
| **Developer DX** | ✅ Excellent | ⚠️ Complex | ✅ Excellent |
| **Lock-in risk** | ⚠️ Medium | ❌ High | ✅ Low (Postgres) |
| **Cloud** | Multi-cloud | AWS only | Multi-cloud |

---

## Recommended Architecture

### Option A: MongoDB Atlas (Best DX)

```
┌─────────────┐
│   Next.js   │
│  Frontend   │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Vercel    │
│  API Routes │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  MongoDB    │
│   Atlas     │
│ (Serverless)│
└─────────────┘
```

**Pros:** Fast development, flexible schema, built-in search
**Cons:** More expensive at scale ($148/month at 20K users)

---

### Option B: DynamoDB + AWS Stack (Cheapest)

```
┌─────────────┐
│   React     │
│  (Amplify)  │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ API Gateway │
│  + Lambda   │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  DynamoDB   │
│ (Serverless)│
└─────────────┘
```

**Pros:** Cheapest ($30/month at 20K users), serverless, AWS integration
**Cons:** Complex data modeling, AWS lock-in, limited queries

---

### Option C: Supabase (Best Value)

```
┌─────────────┐
│   Next.js   │
│  Frontend   │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Supabase   │
│  (Postgres  │
│  + Auth +   │
│  Real-time) │
└─────────────┘
```

**Pros:** Best value ($25/month for years), real-time built-in, low lock-in
**Cons:** Relational model requires schema design, PostgreSQL (not NoSQL)

---

## Final Recommendation

### For Solo Founder / Budget-Constrained: **Supabase**
- $25/month for years
- Real-time built-in
- Auth included
- Low lock-in (PostgreSQL standard)
- **3-year TCO: $600**

### For Fast Development / Complex Queries: **MongoDB Atlas**
- Best developer experience
- Flexible schema (rapid iteration)
- Built-in full-text search
- Rich query capabilities
- **3-year TCO: $4,260** (worth it for faster development)

### For AWS Ecosystem / Serverless: **DynamoDB**
- Cheapest at scale ($30/month)
- True serverless
- AWS integration
- **3-year TCO: $960**
- Trade-off: Complex data modeling

---

## Migration Strategy (If Outgrow Choice)

**MongoDB Atlas → Self-Hosted MongoDB:**
- Trigger: >$500/month cost OR >1TB data
- Tool: mongodump → self-hosted
- Time: 1 week
- Cost: $200/month infrastructure vs $480/month Atlas

**DynamoDB → ???:**
- Challenge: No compatible alternative
- Options: Rewrite to Cassandra, MongoDB, or stay on DynamoDB
- Time: 2-3 months (application rewrite)
- Verdict: Avoid DynamoDB if unsure about AWS commitment

**Supabase → Self-Hosted PostgreSQL:**
- Trigger: >$100/month cost OR compliance needs
- Tool: pg_dump → AWS RDS, Render, Railway
- Time: 1 day
- Cost: $7-25/month managed Postgres

**Winner for Portability:** Supabase (PostgreSQL = open standard)

---

**Recommendation:** Start with **Supabase** (best value + low lock-in), switch to **MongoDB Atlas** if complex queries become bottleneck.
