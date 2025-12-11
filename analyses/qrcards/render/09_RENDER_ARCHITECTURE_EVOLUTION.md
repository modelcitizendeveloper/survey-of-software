# Render Architecture Evolution for QRCards

**Created:** November 15, 2025
**Status:** Architecture planning
**Context:** Progressive complexity roadmap for Render deployment

---

## Current State: PythonAnywhere

**What you have now:**
- 10 GB storage
- SQLite databases (admin + runtime)
- Flask app serving 4 domains
- Simple file-based persistence

**Migration challenge:** Replicate this on Render with minimal complexity first, then evolve

---

## Evolution Stages

### Stage 0: Minimum Viable Migration (START HERE)

**Goal:** Get QRCards running on Render with absolute minimum components

**Components:**
1. **Web Service** (starter plan, $7/month)
   - Flask app deployment
   - Auto-deploy from qrcards-deploy repo
   - Environment variables (FLASK_ENV, etc.)

2. **Persistent Disk** (1 GB, ~$0.25/month)
   - Mount path: `/opt/render/project/src/data`
   - Stores SQLite databases
   - Preserves QR code data, user data

**Architecture:**
```
┌─────────────────────────────────────┐
│ Web Service (qrcards)               │
│ ├── Flask app                       │
│ ├── SQLite admin.db                 │
│ │   └── Persistent Disk (1 GB)     │
│ ├── SQLite runtime.db               │
│ │   └── Persistent Disk (1 GB)     │
│ └── Serves 4 domains                │
└─────────────────────────────────────┘
```

**Cost:** $9.50/month (Hobby tier - FREE account)
- Web service (Starter): $7/month
- Persistent disk (10 GB): $2.50/month
- Account: FREE (Hobby tier)

**Complexity:** Minimal
**Downtime on deploy:** Yes (disk requires stop/start)
**Data safety:** Good (automatic snapshots)
**Account tier:** Hobby (FREE - individual developer)

**render.yaml:**
```yaml
services:
  - type: web
    name: qrcards
    env: python
    region: oregon
    plan: starter
    disk:
      name: qrcards-data
      mountPath: /opt/render/project/src/data
      sizeGB: 1
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT --workers 2 run:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: DATABASE_PATH
        value: /opt/render/project/src/data
```

**When to use:** Phase 1 migration (prove Render works)

**Limitations:**
- No zero-downtime deploys (disk attached to web service)
- SQLite not ideal for high concurrency
- Single point of failure
- Manual backups needed (snapshots not reliable for databases)
- **Hobby tier limits:** No team collaboration, 100GB bandwidth/month, no autoscaling

**When you'd need Professional tier ($19/user/month):**
- Barnraising collaboration (dev partners need access)
- >100 GB bandwidth/month
- Horizontal autoscaling
- Preview environments
- **Timeline:** Likely Q2 2026 when barnraising kicks off

---

### Stage 1: Separate Database Storage (OPTIONAL - FUTURE)

**Goal:** Decouple database from web service for better architecture

**Components:**
1. **Web Service** (starter plan, $7/month)
   - Flask app only
   - No disk attached
   - Stateless (can scale, zero-downtime deploys)

2. **Private Service** (starter plan, $7/month)
   - SQLite "database server"
   - Persistent disk attached (10 GB, ~$2.50/month)
   - Accessed via Render's private network
   - Simple HTTP/file-based access to SQLite

**Architecture:**
```
┌─────────────────────────────────┐
│ Web Service (qrcards)           │
│ ├── Flask app (stateless)      │
│ └── Connects to private network│
└─────────┬───────────────────────┘
          │ Private Network
          │ (internal only)
          ↓
┌─────────────────────────────────┐
│ Private Service (qrcards-db)    │
│ ├── SQLite databases            │
│ │   └── Persistent Disk (10 GB)│
│ └── Serves DB over private net │
└─────────────────────────────────┘
```

**Cost:** $16.50/month
**Complexity:** Medium
**Downtime on deploy:** Web service = NO, DB service = YES
**Data safety:** Better isolation

**Benefits:**
- ✅ Web service can do zero-downtime deploys
- ✅ Database isolated from app code
- ✅ Can scale web service independently
- ✅ Better separation of concerns

**Challenges:**
- ❌ SQLite not designed for network access
- ❌ Need to build custom DB access layer
- ❌ More complex architecture
- ❌ Higher cost

**When to use:**
- When you need zero-downtime deploys for web service
- When you want to scale web instances
- NOT YET - Stage 0 is simpler and works

---

### Stage 2: Managed PostgreSQL (RECOMMENDED FUTURE)

**Goal:** Replace SQLite with proper client-server database

**Components:**
1. **Web Service** (starter plan, $7/month)
   - Flask app (stateless)
   - Connects to Postgres via connection string
   - Zero-downtime deploys

2. **PostgreSQL** (starter plan, $7/month)
   - Managed database
   - 256 MB RAM, 1 GB disk (expandable)
   - Automatic backups (7-day retention)
   - High availability options available

**Architecture:**
```
┌─────────────────────────────────┐
│ Web Service (qrcards)           │
│ ├── Flask app (stateless)      │
│ └── SQLAlchemy → PostgreSQL    │
└─────────┬───────────────────────┘
          │ Private Network
          │ (encrypted)
          ↓
┌─────────────────────────────────┐
│ PostgreSQL (Managed)            │
│ ├── qrcards_admin database      │
│ ├── qrcards_runtime database    │
│ ├── Automatic backups (7 days) │
│ └── Point-in-time recovery      │
└─────────────────────────────────┘
```

**Cost:** $14/month
**Complexity:** Medium (migration required)
**Downtime on deploy:** NO
**Data safety:** Excellent (managed backups, PITR)

**Benefits:**
- ✅ Zero-downtime deploys
- ✅ Automatic backups (7-day retention)
- ✅ Point-in-time recovery
- ✅ Better concurrency than SQLite
- ✅ Can scale to multiple web instances
- ✅ Industry-standard database
- ✅ No manual backup scripts needed

**Migration path:**
1. Run Stage 0 for 1-2 months
2. Export SQLite data to SQL dumps
3. Create PostgreSQL service on Render
4. Import data to PostgreSQL
5. Update app code to use Postgres (SQLAlchemy already supports)
6. Deploy new version
7. Remove disk from web service

**When to use:**
- After validating Render works (Stage 0)
- When ready for production-grade database
- When zero-downtime deploys become important
- Timeline: Q1 2026 (after FIFA demo proven)

---

### Stage 3: Redis Cache Layer (OPTIMIZATION)

**Goal:** Add caching for frequently accessed data

**Components:**
1. **Web Service** (starter plan, $7/month)
2. **PostgreSQL** (starter plan, $7/month)
3. **Redis** (starter plan, $10/month)
   - Session storage
   - QR code resolution cache
   - Frequently accessed content

**Architecture:**
```
┌─────────────────────────────────┐
│ Web Service (qrcards)           │
│ ├── Flask app                   │
│ ├── → Redis (cache)             │
│ └── → PostgreSQL (persistent)   │
└─────────┬───────┬───────────────┘
          │       │
          ↓       ↓
    ┌─────┴─┐ ┌──┴──────┐
    │ Redis │ │Postgres │
    └───────┘ └─────────┘
```

**Cost:** $24/month
**When to use:** High traffic, performance optimization needed

---

### Stage 4: CDN + Object Storage (SCALE)

**Goal:** Offload static assets and media files

**Components:**
1. **Web Service** (starter plan, $7/month)
2. **PostgreSQL** (starter plan, $7/month)
3. **Redis** (optional, $10/month)
4. **External CDN** (Cloudflare - FREE)
5. **Object Storage** (AWS S3, Backblaze B2, etc.)
   - QR code images
   - User uploads
   - Static assets

**Architecture:**
```
        ┌──────────┐
        │Cloudflare│ (CDN - FREE)
        │   CDN    │
        └────┬─────┘
             ↓
┌─────────────────────────────────┐
│ Web Service (qrcards)           │
│ ├── Flask app                   │
│ ├── → Redis (cache)             │
│ ├── → PostgreSQL (data)         │
│ └── → S3 (media)                │
└─────────────────────────────────┘
```

**Cost:** $14-24/month + S3 storage (~$0.023/GB/month)
**When to use:** Serving lots of images, user uploads, global traffic

---

### Stage 5: Multi-Region + High Availability (ENTERPRISE)

**Goal:** Geographic distribution, 99.99% uptime

**Components:**
1. **Web Services** (multiple regions, $7/month each)
2. **PostgreSQL HA** (high availability, $95/month+)
3. **Redis HA** (multiple instances)
4. **Load balancer** (built into Render)
5. **Multi-region CDN**

**Cost:** $100+/month
**When to use:** Global scale, enterprise SLA requirements

---

## Recommended Migration Path

### Phase 1: Prove Render Works (Nov 2025)
**Stage 0 - Minimum Viable**
- Web service + persistent disk
- SQLite databases
- 4 domains on single service
- **Cost:** $7.25/month
- **Timeline:** Nov 15-22, 2025

### Phase 2: Validate & Optimize (Dec 2025 - Jan 2026)
**Stay on Stage 0**
- Monitor performance
- Validate stability
- FIFA demo on Stage 0 architecture
- Collect metrics (traffic, response times, disk usage)
- **Cost:** $7.25/month

### Phase 3: Production-Grade Database (Q1 2026)
**Migrate to Stage 2 - PostgreSQL**
- Only IF Stage 0 proves limiting
- Migrate SQLite → PostgreSQL
- Zero-downtime deploys enabled
- Better backup/recovery
- **Cost:** $14/month
- **Trigger:**
  - Decision Analysis service growth
  - Need for zero-downtime deploys
  - SQLite concurrency issues

### Phase 4: Scale as Needed (2026+)
**Add Stage 3/4 components IF needed**
- Redis (high traffic)
- CDN (global users)
- Object storage (lots of media)
- **Cost:** Variable based on growth

---

## Alternative: Private Service for SQLite

**Your question:** "What if I had persistent disk attached as a private network app?"

### Architecture: SQLite as Private Service

```
┌─────────────────────────────────┐
│ Web Service (qrcards)           │  $7/month
│ ├── Flask app (stateless)      │  Zero-downtime ✅
│ └── HTTP client to DB service  │
└─────────┬───────────────────────┘
          │ Private Network
          │ (internal, encrypted)
          ↓
┌─────────────────────────────────┐
│ Private Service (qrcards-db)    │  $7/month
│ ├── SQLite proxy/server         │  Downtime on deploy ❌
│ ├── Simple HTTP API             │
│ │   GET /query                  │
│ │   POST /execute               │
│ └── Persistent Disk (10 GB)     │  $2.50/month
└─────────────────────────────────┘
```

**Cost:** $16.50/month

**Pros:**
- ✅ Web service gets zero-downtime deploys
- ✅ SQLite stays familiar (no migration needed)
- ✅ Database isolated from web code
- ✅ Can scale web instances

**Cons:**
- ❌ SQLite not designed for network access
- ❌ Need to build custom HTTP API for database
- ❌ DB service still has downtime on deploy
- ❌ More complexity than Stage 0
- ❌ More expensive than Stage 0
- ❌ Less reliable than PostgreSQL (Stage 2)

**Verdict:**
- **Don't do this** - worst of both worlds
- If you need separation → go to **Stage 2 (PostgreSQL)** instead
- If you want simplicity → stay on **Stage 0 (web + disk)**

**Why PostgreSQL is better than "SQLite as service":**
- PostgreSQL designed for client-server
- Managed backups (7-day retention)
- Point-in-time recovery
- Better concurrency
- Same cost ($14 vs $16.50)
- Less complexity (no custom DB API needed)

---

## Decision Matrix

| Need | Stage 0 | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|------|---------|---------|---------|---------|---------|
| **Minimum viable** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Low cost** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Simple setup** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Zero-downtime deploys** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Reliable backups** | ⚠️ | ⚠️ | ✅ | ✅ | ✅ |
| **High concurrency** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Horizontal scaling** | ❌ | ⚠️ | ✅ | ✅ | ✅ |
| **Global performance** | ❌ | ❌ | ❌ | ⚠️ | ✅ |

---

## Immediate Recommendation

### Start with Stage 0 (Minimum Viable)

**Why:**
1. ✅ Simplest migration path
2. ✅ Lowest cost ($7.25/month vs $19.25 PythonAnywhere)
3. ✅ Matches current SQLite architecture
4. ✅ No code changes needed
5. ✅ Proves Render works before adding complexity

**What to monitor:**
- Disk usage (start with 1 GB, expand to 10 GB if needed)
- Deploy downtime (how long does stop/start take?)
- Database performance (any concurrency issues?)
- Backup reliability (test snapshot restoration)

**When to evolve to Stage 2:**
- After 1-2 months on Render
- After FIFA demo proven (Dec 2025)
- When zero-downtime deploys become important
- When Decision Analysis service grows

**Timeline:**
- **Now - Dec 2025:** Stage 0 (web + disk + SQLite)
- **Jan - Mar 2026:** Evaluate need for Stage 2 (PostgreSQL)
- **Q2 2026+:** Add Stage 3/4 components if needed

---

## render.yaml for Stage 0 (Recommended Start)

```yaml
services:
  - type: web
    name: qrcards
    env: python
    region: oregon
    plan: starter

    # Persistent disk for SQLite databases
    disk:
      name: qrcards-data
      mountPath: /opt/render/project/src/data
      sizeGB: 10  # Match PythonAnywhere 10 GB

    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT --workers 2 run:app

    envVars:
      - key: FLASK_ENV
        value: production
      - key: DATABASE_PATH
        value: /opt/render/project/src/data
      - key: SQLITE_ADMIN_DB
        value: /opt/render/project/src/data/flasklayer_admin.sqlite
      - key: SQLITE_RUNTIME_DB
        value: /opt/render/project/src/data/flasklayer_runtime.sqlite
```

**Cost breakdown:**
- Web service (starter): $7/month
- Persistent disk (10 GB): $2.50/month
- **Total:** $9.50/month (vs $19.25 PythonAnywhere)
- **Savings:** $117/year

---

## Summary

**Start simple, evolve as needed:**

1. **Stage 0** (NOW): Web + disk + SQLite → Prove Render works
2. **Stage 2** (Q1 2026): PostgreSQL → Production-grade database
3. **Stage 3+** (Future): Redis, CDN, etc. → Scale as needed

**Don't do:**
- ❌ Stage 1 (SQLite as private service) - complexity without benefits
- ❌ Over-engineer upfront - start minimal

**Key insight:**
Your current 10 GB on PythonAnywhere maps perfectly to **Stage 0: Web + 10 GB disk**. Start there, validate, then evolve to PostgreSQL when you're ready for zero-downtime deploys and better backups.

---

## Hobby vs Professional Tier (Account-Level Decision)

### What the PaaS Research Missed

**Original 3.050 research (October 2025):**
- ❌ Didn't distinguish account tiers from compute tiers
- ❌ Implied persistent disks only on "Production Tier" ($25/month)
- ❌ Didn't mention $19/month Professional tier

**Corrected understanding (November 2025):**
- ✅ **Hobby tier:** FREE account (individual developer)
- ✅ **Persistent disks:** Available on ALL tiers including Hobby ($0.25/GB)
- ✅ **Professional tier:** $19/user/month (team features, not compute)

### Hobby Tier (FREE) - Use This Now

**What you get:**
- ✅ All compute tiers (Free, Starter $7, Production $25+)
- ✅ Persistent disks ($0.25/GB/month)
- ✅ Custom domains
- ✅ Automatic SSL certificates
- ✅ Git-based deployment
- ✅ Managed databases (PostgreSQL, Redis)
- ✅ 100 GB bandwidth/month

**Limitations:**
- ❌ No team collaboration (solo developer only)
- ❌ No horizontal autoscaling
- ❌ No preview environments
- ❌ Community support only (no chat)
- ❌ Limited to 100 GB bandwidth/month (vs 500 GB Professional)

**Perfect for QRCards now because:**
- Solo developer (Ivan only)
- Pre-revenue (<100 scans/month → minimal bandwidth)
- No team collaboration needed yet
- No autoscaling needed (demos)

### Professional Tier ($19/user/month) - Future

**When you'd need it:**

1. **Barnraising Collaboration (Q2 2026)**
   - Dev partners need repo access
   - UI designers need template access
   - Professional enables team members (up to 10)
   - **Cost:** $19/month (first user) + $19/month per additional user

2. **High Traffic (Future)**
   - >100 GB bandwidth/month
   - Horizontal autoscaling needed
   - Variable traffic patterns

3. **Preview Environments (Nice-to-have)**
   - Per-PR test deployments
   - Client demo environments
   - Professional feature

**Cost comparison with barnraising:**

**Option 1: Hobby tier + controlled repo access**
- Hobby tier: FREE
- Use git subtree for controlled access (already planned)
- Dev partners have read-only or limited access
- **Cost:** $0/month additional
- **Limitation:** No shared Render dashboard access

**Option 2: Professional tier with team**
- Professional: $19/month (first user)
- Add 2-3 dev partners: $38-57/month
- Full Render dashboard access for team
- Autoscaling, preview environments
- **Cost:** $19-76/month additional

**Recommendation:**
- **Now - Q1 2026:** Hobby tier (FREE)
- **Q2 2026:** Evaluate if barnraising needs Professional tier
- **Decision driver:** Whether dev partners need Render dashboard access vs just git repo access

### Cost Evolution Timeline

**Phase 1 (Nov 2025 - Q1 2026): Hobby Tier**
- Web service (Starter): $7/month
- Persistent disk (10 GB): $2.50/month
- Account: FREE
- **Total:** $9.50/month

**Phase 2 (Q1 2026): PostgreSQL Migration (Still Hobby)**
- Web service (Starter): $7/month
- PostgreSQL (Starter): $7/month
- Account: FREE
- **Total:** $14/month

**Phase 3 (Q2 2026): Professional Tier IF Needed**
- Web service (Starter): $7/month
- PostgreSQL (Starter): $7/month
- Professional account: $19/user/month
- **Total:** $33/month (1 user) or $52+/month (2-3 users)

**Decision point Q2 2026:**
- If barnraising only needs git subtree access → Stay on Hobby ($14/month)
- If team needs Render dashboard access → Upgrade to Professional ($33+/month)

### Summary: PaaS Research Gap Closed

**What we learned:**
1. ✅ Hobby tier is FREE (account-level)
2. ✅ Persistent disks work on Hobby tier
3. ✅ Professional tier ($19/month) is for teams, not compute
4. ✅ Stage 0 architecture works perfectly on Hobby tier
5. ✅ Can defer Professional decision until barnraising (Q2 2026)

**Updated cost calculation:**
- **Stage 0 (Hobby):** $9.50/month ✅
- **Stage 2 (Hobby + PostgreSQL):** $14/month ✅
- **Stage 2 (Professional + PostgreSQL):** $33/month (if team needed)

**PaaS research correction made:** Updated 3.050 research to clarify Hobby vs Professional distinction and persistent disk availability.
