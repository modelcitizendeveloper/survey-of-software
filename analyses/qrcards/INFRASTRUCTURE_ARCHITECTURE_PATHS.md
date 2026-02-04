# QRCards Infrastructure Architecture: Two Strategic Paths

**Date**: October 8, 2025
**Context**: Applying service bundling findings (11, 14) from experiments 3.012, 3.020, 3.040
**Current State**: PythonAnywhere + SQLite, monorepo, database-driven routing
**Decision**: Distributed self-managing vs modern backend platform rip-and-replace

---

## Executive Summary

QRCards faces a strategic infrastructure decision with two viable paths:

**Path A: Distributed Self-Managing (Lean Scale)**
- Keep existing Python/SQLite architecture
- Deploy independent instances per trail system (self-hosting)
- No dependency on free tiers or platform bundles
- Target: Single trail system scale (~1K-10K QR scans/month per deployment)
- Economics: DigitalOcean Droplet $12/month per trail vs platform bundles

**Path B: Rip-and-Replace Modern Stack (Hyperscale Platform)**
- Migrate to Supabase/Firebase backend platform OR Neon + best-of-breed
- Centralized multi-tenant database (PostgreSQL or Firestore)
- Leverage platform features (auth, storage, real-time, edge functions)
- Target: Multi-trail aggregation scale (100K+ scans/month centralized)
- Economics: $25-599/month Supabase bundle vs $400+ unbundled

**The Key Question**: Does QRCards architecture match **distributed small-scale** (many independent deployments) or **centralized large-scale** (one platform serving all trails)?

**Current Evidence**:
- Harvard Extension + Melrose Loop = 2 independent trail systems
- Database-driven routing = multi-tenant capable (supports centralization)
- SQLite federated databases = supports distribution
- **Architectural flexibility**: System designed for BOTH paths

**Recommendation**: Start with **Path A (Distributed)** for initial trails, keep **Path B (Platform)** as pivot option when aggregation economics justify platform migration.

---

## 1. Current Architecture Analysis

### 1.1 Existing Infrastructure (PythonAnywhere + SQLite)

**What Works Today**:
- **Hosting**: PythonAnywhere shared hosting
- **Database**: SQLite (admin_prod.db + runtime_prod.db federated)
- **Domain**: qrcard.conventioncityseattle.com (live)
- **Deployment**: Manual git pull + restart
- **Cost**: ~$20/month PythonAnywhere

**Current Capabilities**:
- Database-driven routing (multi-tenant ready)
- Admin/runtime database separation (federated architecture)
- Monorepo with specialized packages (flasklayer, dap-processor, trip-generator)
- Template-based content generation
- QR token resolution (<100ms requirement)

**Current Limitations** (from docs/training/14):
- Manual deployment (no CI/CD)
- SQLite scalability ceiling (~10K concurrent users theoretical, ~1K practical)
- No automated backups (manual tar.gz process)
- Minimal monitoring (manual log review)
- Single-region hosting (PythonAnywhere US)

**From docs/training/02 System Architecture**:
> "Database-driven routing pattern is **framework-agnostic** - could be implemented in Django, FastAPI, Express.js, Rails. Core pattern: `Request → Database Query → Dynamic Response`"

**Portability Assessment**:
- ✅ **High portability**: Database schema is the core asset (SQLite portable, PostgreSQL migration straightforward)
- ✅ **Framework independence**: Routing logic not Flask-specific
- ✅ **Clear separation**: Admin vs runtime databases enable clean migration
- ⚠️ **Jinja2 templates**: Migration requires template re-implementation (React components, etc.)

---

### 1.2 Service Dependencies (Explicit vs Implicit)

**Current Explicit Services** (what QRCards uses today):
- ✅ **Hosting**: PythonAnywhere ($20/month)
- ✅ **Database**: SQLite (bundled, no separate service)
- ✅ **Domain/DNS**: Domain registration (~$15/year)
- ✅ **SSL**: PythonAnywhere includes Let's Encrypt SSL (free)

**Implicit Services** (missing but may be needed):
- ❌ **Auth**: Not currently implemented (no user login, admin access via SSH/files)
- ❌ **Email**: No transactional or notification emails yet
- ❌ **Storage**: File storage via local filesystem (PDFs, QR images in `/qr/` directory)
- ❌ **Real-time**: No WebSocket/real-time updates (static QR resolution)
- ❌ **Analytics**: No visitor tracking (could add PostHog, Plausible)
- ❌ **Monitoring**: Manual health checks (no Sentry, Datadog)

**From SERVICE_SUBTRACTION_STRATEGY.md**:
> "Service subtraction is the inverse of the bundle: identify which services you DON'T need and actively avoid vendor pressure to add them."

**QRCards current service subtraction wins**:
- ✅ **No auth provider**: Content is public QR cards (no login needed) → saves $25-199/month (Clerk, Auth0)
- ✅ **No email service**: Trail content delivered via QR scan (no email notifications) → saves $20-80/month (Resend, SendGrid)
- ✅ **No real-time sync**: Static content delivery (no collaborative editing) → saves $15-99/month (Ably, Pusher)
- ✅ **No CDN**: Single-region traffic acceptable (<100ms QR resolution) → saves $20-100/month (Cloudflare, AWS CloudFront)

**Total service subtraction savings**: $80-378/month avoided by NOT using modern backend platform features

**The strategic question**: Does QRCards NEED these services for hyperscale, or can distributed architecture maintain subtraction advantage?

---

## 2. Path A: Distributed Self-Managing Architecture

### 2.1 The Model: One Deployment Per Trail System

**Core Principle**: Each trail system (Harvard Extension, Melrose Loop, future trails) gets independent deployment.

**Architecture**:
```
Trail 1: DigitalOcean Droplet ($12/month)
├── qrcards/ (full monorepo clone)
├── SQLite databases (admin + runtime)
├── nginx reverse proxy
└── Domain: harvardextension.qrcard.io

Trail 2: DigitalOcean Droplet ($12/month)
├── qrcards/ (full monorepo clone)
├── SQLite databases (admin + runtime)
├── nginx reverse proxy
└── Domain: melroseloop.qrcard.io

Trail N: DigitalOcean Droplet ($12/month)
├── qrcards/ (independent instance)
└── ...
```

**Why this works for QRCards**:
- **Database-driven routing** already multi-tenant (each droplet serves one trail = simple)
- **SQLite sufficient** for single trail scale (1K-10K scans/month, <100 concurrent users)
- **No shared infrastructure** = no coordination overhead, no central point of failure
- **Independent scaling** = each trail scales independently (or doesn't, if low traffic)

**From docs/training/02**:
> "QR Cards uses federated database approach with clear separation - Admin database (configuration, content) + Runtime database (scan logs, analytics)."

**Federated architecture advantage**: Each droplet has complete database independence → no cross-trail dependencies → perfect for distribution.

---

### 2.2 Economics: Distributed vs Platform Bundle

**Path A: Distributed Self-Managing**

**Per-trail cost** (DigitalOcean Droplet):
```
Basic Droplet (1 GB RAM, 1 vCPU): $12/month
- CPU: 1 vCPU (sufficient for 1K-10K QR scans/month)
- RAM: 1 GB (SQLite + Flask fits comfortably)
- Storage: 25 GB SSD (plenty for SQLite databases + QR assets)
- Bandwidth: 1 TB (more than enough for QR resolution)

Additional costs:
- Domain: $15/year (~$1.25/month per trail)
- SSL: Free (Let's Encrypt via certbot)
- Backups: DigitalOcean Snapshots $1/month (optional)

Total per trail: $13.25/month ($159/year per trail system)
```

**3 trails deployed**: 3 × $12 = $36/month ($432/year)

**10 trails deployed**: 10 × $12 = $120/month ($1,440/year)

**Path B: Supabase Backend Platform (Multi-Tenant)**

**Centralized multi-trail platform** (all trails in one Supabase instance):
```
Supabase Pro: $25/month
- PostgreSQL: 8 GB database (stores all trails)
- Auth: 100K MAU (not used, but included)
- Storage: 100GB (all QR images, PDFs)
- Real-time: 500 connections (not used)
- Edge Functions: 2M invocations (maybe QR resolution)

Problem: QRCards doesn't need Auth, Storage API, Real-time, Edge Functions
- Paying for bundled services: ~$60/month value (from finding 14)
- Actually using: ~$20/month database equivalent (Neon comparison)
- **Waste**: $5/month (auth, real-time, edge functions unused)
```

**3 trails**: Supabase $25/month vs Distributed 3 × $12 = $36/month
- **Supabase wins** by $11/month ($132/year)

**10 trails**: Supabase $25/month vs Distributed 10 × $12 = $120/month
- **Distributed wins** by $95/month ($1,140/year)

**Break-even point**: 2 trails

**Critical insight**: Distributed becomes dramatically cheaper as trail count increases, because platform bundle doesn't scale linearly with trail count.

---

### 2.3 Distributed Architecture Benefits

**Independence Advantages**:
1. **No single point of failure**: One trail down ≠ all trails down
2. **Independent updates**: Update Harvard Extension without touching Melrose Loop
3. **Trail-specific customization**: Each trail can run different QRCards versions if needed
4. **Billing isolation**: Client pays for their own droplet (clean cost attribution)

**Operational Advantages**:
5. **Simple monitoring**: One trail = one droplet = one monitoring dashboard
6. **Backup simplicity**: SQLite file backup (tar.gz) per trail, no multi-tenant restore complexity
7. **Migration ease**: Moving trail to new droplet = copy SQLite files + restart
8. **Testing safety**: Test new features on one trail without risking others

**From Service Subtraction Strategy**:
> "Distributed architecture enables service subtraction: each deployment can omit unnecessary services. Centralized platform forces bundle consumption."

**QRCards specific advantages**:
- **Public content**: No auth needed per trail → no Clerk/Auth0 integration complexity
- **Static QR resolution**: No real-time sync → no Ably/Pusher integration
- **Filesystem storage**: QR images in `/qr/` directory → no S3/Supabase Storage integration
- **No email**: Trail content delivery via QR scan → no Resend/SendGrid integration

**Total avoided integration time** (from finding 14):
- Auth integration: 15-25 hours saved per trail
- Storage integration: 15-25 hours saved per trail
- Real-time integration: 20-40 hours saved per trail
- **Total**: 50-90 hours saved ($7,500-13,500 at $150/hour) by staying distributed with service subtraction

---

### 2.4 Distributed Architecture Limitations

**Challenges**:
1. **No centralized analytics**: Each trail's scan data in separate SQLite → aggregating requires manual export
2. **Update coordination**: Deploying QRCards core update to 10 trails = 10 deployments (can script, but operational overhead)
3. **Shared asset management**: QR template updates → must deploy to all trails (no centralized asset server)
4. **No cross-trail features**: User scans Harvard Extension + Melrose Loop → separate databases, no unified profile

**When distributed breaks down**:
- **Cross-trail analytics**: Client wants "total scans across all our trails" → need central aggregation
- **Unified user profiles**: "Show me all trails a user visited" → need centralized user database
- **Real-time leaderboards**: "Which trail has most scans today?" → need live aggregation
- **Shared content library**: "Reuse activities across trails" → need centralized content management

**Scalability ceiling**:
- **Per-trail**: SQLite handles ~1K-10K scans/month comfortably (based on <100ms QR resolution requirement)
- **Aggregated**: 100 trails × 10K scans = 1M scans/month → distributed works fine (no cross-trail queries)
- **Centralized query**: "Top 10 activities across all trails" → requires central database → distributed architecture can't answer efficiently

**From docs/training/14**:
> "SQLite-based architecture: Theoretical limit ~10K concurrent users, practical limit ~1K concurrent users for QR resolution <100ms requirement."

**Distributed suitability**: If each trail stays <1K concurrent users (10K scans/month = ~333 scans/day = ~14 concurrent users peak), distributed SQLite architecture is sufficient.

---

### 2.5 Distributed Deployment Automation

**Current pain point** (from docs/training/14):
> "Manual deployment workflow: git pull → restart web app → manual verification"

**Distributed deployment solution**: Ansible playbook for multi-droplet orchestration

```yaml
# ansible/deploy_qrcards.yml
---
- name: Deploy QRCards to distributed trail instances
  hosts: qrcards_trails
  become: yes

  tasks:
    - name: Pull latest QRCards code
      git:
        repo: 'https://github.com/yourorg/qrcards.git'
        dest: /var/www/qrcards
        version: main
        force: yes

    - name: Install/update dependencies
      pip:
        requirements: /var/www/qrcards/requirements.txt
        virtualenv: /var/www/qrcards/venv

    - name: Run database migrations (admin)
      command: alembic -c alembic_admin.ini upgrade head
      args:
        chdir: /var/www/qrcards

    - name: Run database migrations (runtime)
      command: alembic -c alembic_runtime.ini upgrade head
      args:
        chdir: /var/www/qrcards

    - name: Restart Flask application
      systemd:
        name: qrcards
        state: restarted

    - name: Wait for health check
      uri:
        url: "https://{{ inventory_hostname }}/health"
        status_code: 200
      retries: 5
      delay: 10
```

**Inventory file** (ansible/inventory.ini):
```ini
[qrcards_trails]
harvardextension.qrcard.io ansible_user=admin
melroseloop.qrcard.io ansible_user=admin
trail3.qrcard.io ansible_user=admin
# ... add trails as needed
```

**Deploy all trails with one command**:
```bash
ansible-playbook -i ansible/inventory.ini ansible/deploy_qrcards.yml
```

**Selective deployment**:
```bash
# Deploy only to Harvard Extension
ansible-playbook -i ansible/inventory.ini ansible/deploy_qrcards.yml --limit harvardextension.qrcard.io

# Deploy to subset of trails
ansible-playbook -i ansible/inventory.ini ansible/deploy_qrcards.yml --limit "trail3.qrcard.io,trail4.qrcard.io"
```

**Implementation time**: 10-15 hours to build Ansible playbook + test

**Ongoing benefit**: Deploy to N trails in ~5 minutes vs N × 10 minutes manual (saves hours as trail count grows)

---

## 3. Path B: Rip-and-Replace Modern Backend Platform

### 3.1 The Model: Centralized Multi-Tenant Platform

**Core Principle**: Migrate from distributed SQLite to centralized PostgreSQL/Firestore, consolidate all trails in one platform instance.

**Architecture**:
```
Supabase (or Firebase) - Centralized Multi-Tenant
├── PostgreSQL Database (all trails)
│   ├── trails table (trail_id, name, config)
│   ├── paths table (trail_id FK, path_id, url_path)
│   ├── activities table (trail_id FK, activity_id, content)
│   └── scans table (trail_id FK, scan_id, timestamp, token)
├── Supabase Auth (if needed for admin access)
├── Supabase Storage (QR images, PDFs)
├── Supabase Real-time (optional live analytics)
└── Edge Functions (QR resolution at edge)

Frontend: Next.js/React (replaces Jinja2 templates)
Domain: api.qrcard.io (centralized API)
Trail Domains: harvardextension.qrcard.io → routes to api.qrcard.io/trail/harvard
```

**Why centralized**:
- **Cross-trail analytics**: Aggregated scans, top activities, trail comparisons
- **Unified admin**: Manage all trails from one dashboard (Supabase Studio)
- **Shared content**: Reuse activities, templates, QR designs across trails
- **Real-time features**: Live scan counts, leaderboards, notifications

**Migration complexity** (from SQLite → PostgreSQL):
- Database schema migration: 30-50 hours (Alembic migrations → PostgreSQL schema)
- Template migration: 60-100 hours (Jinja2 → React components)
- QR resolution logic: 20-40 hours (Flask routes → Next.js API routes or Supabase Edge Functions)
- Testing + deployment: 40-60 hours
- **Total**: 150-250 hours ($22,500-37,500 at $150/hour)

---

### 3.2 Platform Options: Supabase vs Firebase vs Unbundled

**Option B1: Supabase Backend Platform ($25/month)**

**What you get**:
- PostgreSQL 8GB (multi-tenant trails database)
- Auth 100K MAU (admin access, optional trail visitor auth)
- Storage 100GB (QR images, PDFs centralized)
- Real-time 500 connections (live scan analytics)
- Edge Functions 2M invocations (QR resolution at edge)

**What you use** (QRCards needs):
- ✅ **PostgreSQL**: Core database (trail content, scan logs)
- ⚠️ **Auth**: Maybe for admin dashboard (not public QR content)
- ⚠️ **Storage**: Maybe for centralized QR assets (currently filesystem)
- ❌ **Real-time**: Nice-to-have (live analytics), not core requirement
- ⚠️ **Edge Functions**: Maybe for QR resolution (currently Flask routes)

**Bundle fit assessment** (from finding 14):
- Database: 100% utilization (PostgreSQL needed)
- Auth: 10% utilization (admin only, not public QR scanning)
- Storage: 30% utilization (could use, but filesystem works)
- Real-time: 0% utilization (static content delivery)
- Edge Functions: 40% utilization (QR resolution could use, but Flask routes work)

**Bundle waste**: Paying for $60 value (from finding 14 bundle breakdown), using ~$20 equivalent (database + partial storage)

**Cost**: $25/month ($300/year) for all trails centralized

**Break-even vs distributed**:
- 2 trails: Supabase $25 < Distributed $24 ✅ (Supabase wins by $1/month)
- 3 trails: Supabase $25 < Distributed $36 ✅ (Supabase wins by $11/month)
- 10 trails: Supabase $25 < Distributed $120 ✅ (Supabase wins by $95/month)

**But**: Migration cost $22,500-37,500 + ongoing bundle waste ($5-10/month unused services) vs distributed savings

**First year total cost**:
- Supabase: $300 subscription + $22,500-37,500 migration = $22,800-37,800
- Distributed (10 trails): $1,440 subscription + $2,250 Ansible automation = $3,690
- **Distributed saves $19,110-34,110 first year**

**Break-even**: Year 6-30 (assuming $95/month ongoing savings from Supabase bundle)

---

**Option B2: Firebase Backend Platform ($50-100/month)**

**What you get**:
- Firestore (NoSQL database, real-time, offline-first)
- Firebase Auth (email, social, phone, anonymous)
- Firebase Storage (file hosting, CDN)
- Cloud Functions (serverless backend)
- Firebase Hosting (static site hosting)
- Analytics, Messaging, Remote Config (included)

**What you use** (QRCards needs):
- ✅ **Firestore**: Multi-tenant trails database (NoSQL doc model)
- ⚠️ **Auth**: Admin access (not public)
- ⚠️ **Storage**: Centralized QR assets
- ❌ **Cloud Functions**: QR resolution (could use)
- ❌ **Hosting**: Static hosting (Next.js could use)
- ❌ **Analytics/Messaging**: Nice-to-have features

**Bundle fit**: Similar to Supabase (database primary use, other services partial/unused)

**Cost**: $50-100/month (Firestore reads/writes metered, higher than Supabase fixed)

**Firebase-specific advantages**:
- Mobile SDKs (if QRCards adds iOS/Android apps)
- Offline-first (Firestore offline persistence)
- Analytics bundled (Firebase Analytics better than adding PostHog separately)

**Firebase-specific disadvantages** (from finding 14):
- Maximum lock-in (Firestore → SQL migration 200-300 hours)
- NoSQL vs SQL (QRCards schema is relational, Firestore doc model awkward)
- Higher cost than Supabase ($50-100 vs $25)

**Verdict**: Firebase not ideal for QRCards (relational schema, no mobile app, lock-in concerns)

---

**Option B3: Unbundled Best-of-Breed ($69-120/month)**

**Specialist stack**:
```
Neon PostgreSQL: $19-69/month (database only, serverless, branching)
+ Clerk Auth: $0-25/month (admin dashboard access, SSO optional)
+ AWS S3 + CloudFront: $10-25/month (centralized QR assets + CDN)
+ Vercel/Netlify: $0-20/month (Next.js frontend hosting)
────────────────
Total: $29-139/month (depends on usage)
```

**Why unbundled** (from finding 14):
- Neon branching: Preview database per Git branch (test trail updates safely)
- Specialist pricing: PostgreSQL-only cheaper than Supabase bundle if you don't use auth/storage/real-time
- Portability: Standard Postgres (migrate to RDS, DO Managed DB, self-hosted later)

**Cost comparison** (10 trails centralized):
- Supabase: $25/month (bundle)
- Unbundled (Neon + Vercel): $39/month (database + hosting, no auth/storage)
- Distributed: $120/month (10 droplets)

**Unbundled fits if**:
- Need Neon-specific features (database branching for preview environments)
- Want portability (avoid Supabase platform lock-in 60% acquisition risk by 2027-2028)
- Growth path to enterprise (negotiate Neon/AWS pricing independently)

**Unbundled doesn't fit if**:
- Service subtraction wins (QRCards doesn't need auth/storage → why pay for Neon + separate services?)
- Distributed already cheaper ($120 vs $39 = distributed loses, but distributed gives independence)

**Verdict**: Unbundled makes sense for growth stage (>$500/month spend), not early trails

---

### 3.3 Platform Migration Path (Supabase Example)

**Migration steps** (SQLite → PostgreSQL):

**Phase 1: Database Schema Migration** (30-50 hours)
```sql
-- Convert SQLite admin.db schema to PostgreSQL

-- Trails table (new for multi-tenancy)
CREATE TABLE trails (
  trail_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  domain TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Paths table (add trail_id FK for multi-tenancy)
CREATE TABLE paths (
  path_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  trail_id UUID REFERENCES trails(trail_id) ON DELETE CASCADE,
  url_path TEXT NOT NULL,
  template_name TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(trail_id, url_path)  -- Path unique per trail
);

-- Activities table (add trail_id FK)
CREATE TABLE activities (
  activity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  trail_id UUID REFERENCES trails(trail_id) ON DELETE CASCADE,
  activity_name TEXT NOT NULL,
  content JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Scans table (runtime database migration)
CREATE TABLE scans (
  scan_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  trail_id UUID REFERENCES trails(trail_id),
  qr_token TEXT NOT NULL,
  scanned_at TIMESTAMPTZ DEFAULT NOW(),
  user_agent TEXT,
  ip_address INET
);

-- Row-Level Security for multi-tenancy
ALTER TABLE paths ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Paths scoped to trail" ON paths
  FOR ALL USING (trail_id = current_setting('app.current_trail_id')::UUID);
```

**Data migration** (existing SQLite → PostgreSQL):
```python
# scripts/migrate_sqlite_to_postgres.py
import sqlite3
import psycopg2
from uuid import uuid4

def migrate_trail(sqlite_db_path, postgres_conn, trail_name, trail_domain):
    """Migrate one SQLite trail database to PostgreSQL multi-tenant"""

    # Create trail record
    trail_id = str(uuid4())
    postgres_cur = postgres_conn.cursor()
    postgres_cur.execute(
        "INSERT INTO trails (trail_id, name, domain) VALUES (%s, %s, %s)",
        (trail_id, trail_name, trail_domain)
    )

    # Migrate paths
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_cur = sqlite_conn.cursor()

    for row in sqlite_cur.execute("SELECT url_path, template_name FROM paths"):
        url_path, template_name = row
        postgres_cur.execute(
            "INSERT INTO paths (trail_id, url_path, template_name) VALUES (%s, %s, %s)",
            (trail_id, url_path, template_name)
        )

    # Migrate activities, scans, etc.
    # ...

    postgres_conn.commit()
    postgres_conn.close()
    sqlite_conn.close()

# Run migration for each trail
migrate_trail("databases/admin_prod_harvard.db", postgres_conn, "Harvard Extension", "harvardextension.qrcard.io")
migrate_trail("databases/admin_prod_melrose.db", postgres_conn, "Melrose Loop", "melroseloop.qrcard.io")
```

**Migration time**: 30-50 hours (schema design + data migration + testing)

---

**Phase 2: Application Code Migration** (60-100 hours)

**Flask → Next.js API Routes** (QR resolution logic):

```typescript
// pages/api/qr/[token].ts (Next.js API route)
import { createClient } from '@supabase/supabase-js'

export default async function handler(req, res) {
  const { token } = req.query
  const host = req.headers.host

  const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY)

  // Get trail by domain
  const { data: trail } = await supabase
    .from('trails')
    .select('trail_id')
    .eq('domain', host)
    .single()

  if (!trail) {
    return res.status(404).json({ error: 'Trail not found' })
  }

  // Resolve QR token to path (multi-tenant query)
  const { data: path } = await supabase
    .from('paths')
    .select('url_path, template_name')
    .eq('trail_id', trail.trail_id)
    .eq('qr_token', token)
    .single()

  if (!path) {
    return res.status(404).json({ error: 'QR token not found' })
  }

  // Log scan
  await supabase.from('scans').insert({
    trail_id: trail.trail_id,
    qr_token: token,
    user_agent: req.headers['user-agent'],
    ip_address: req.headers['x-forwarded-for'] || req.connection.remoteAddress
  })

  // Return activity content or redirect
  res.redirect(path.url_path)
}
```

**Jinja2 Templates → React Components**:

```tsx
// components/ActivityCard.tsx (React component replaces Jinja2 template)
interface Activity {
  activity_name: string
  content: {
    description: string
    image_url: string
    duration_minutes: number
  }
}

export function ActivityCard({ activity }: { activity: Activity }) {
  return (
    <div className="activity-card">
      <img src={activity.content.image_url} alt={activity.activity_name} />
      <h2>{activity.activity_name}</h2>
      <p>{activity.content.description}</p>
      <span>{activity.content.duration_minutes} minutes</span>
    </div>
  )
}
```

**Migration complexity**:
- Template migration: 60-100 hours (Jinja2 → React components, styling, responsive design)
- API routes: 20-40 hours (Flask routes → Next.js API, Supabase queries)
- Testing: 40-60 hours (QR resolution, multi-tenancy, performance)

**Total migration**: 150-250 hours ($22,500-37,500 engineering)

---

**Phase 3: Deployment** (20-40 hours)

**Vercel deployment** (Next.js frontend + API):
```bash
# vercel.json
{
  "env": {
    "SUPABASE_URL": "@supabase-url",
    "SUPABASE_KEY": "@supabase-key"
  },
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/qr/(.*)",
      "dest": "/api/qr/$1"
    }
  ]
}
```

**Deployment time**: 20-40 hours (Vercel config, domain setup, DNS migration, testing)

---

**Total Migration Investment**:
- Phase 1 (Database): 30-50 hours
- Phase 2 (Application): 120-200 hours
- Phase 3 (Deployment): 20-40 hours
- **Total**: 170-290 hours ($25,500-43,500 at $150/hour)

**Ongoing cost**:
- Supabase: $25/month ($300/year)
- Vercel: $0-20/month (hobby free, Pro $20 if needed)
- **Total**: $300-540/year

**vs Distributed** (10 trails):
- Droplets: $1,440/year
- Ansible automation: $2,250 one-time
- **Total Year 1**: $3,690

**Platform migration break-even**:
- Year 1: Platform $25,800-44,040 vs Distributed $3,690 → **Distributed $22,110-40,350 cheaper**
- Year 2+: Platform $300-540 vs Distributed $1,440 → **Platform $900-1,140 cheaper**
- **Break-even**: Year 25-45 (platform migration never pays off unless trail count stays <2)

**When platform migration makes sense**:
- Need cross-trail analytics (centralized database required)
- Plan >100 trails (distributed ops overhead > platform cost)
- Want modern stack (React vs Jinja2, PostgreSQL vs SQLite)
- Building SaaS product (multi-tenant database, admin dashboard, billing)

**When distributed wins**:
- <10 trails (platform migration cost never recoups)
- Independence valued (each trail separate client, isolated billing/updates)
- Service subtraction advantage (no auth/email/real-time/storage needs)
- Existing architecture works (SQLite sufficient, Flask mature)

---

## 4. Decision Framework: Which Path for QRCards?

### 4.1 Trail Count Projection

**Current**: 2 trails (Harvard Extension, Melrose Loop)

**Growth scenarios**:

**Scenario A: Boutique Trail Provider** (2-5 trails/year growth)
- Year 1: 2 trails
- Year 2: 4 trails
- Year 3: 7 trails
- Year 5: 13 trails
- **Model**: Custom trail experiences for high-end clients ($5K-15K per trail setup)

**Distributed economics** (Year 5, 13 trails):
- Cost: 13 × $12 = $156/month ($1,872/year)
- Ansible already built (one-time $2,250 Year 1)
- **Total**: $1,872/year ongoing

**Platform economics** (Year 5, 13 trails centralized):
- Cost: Supabase $25/month ($300/year)
- Migration: $25,500-43,500 (Year 1 only)
- **Total Year 1**: $25,800-43,800, **Year 2+**: $300/year

**Break-even**: Platform cheaper Year 2+ ($300 vs $1,872 = $1,572/year savings)

**But**: Platform migration ($25,500-43,500) ÷ annual savings ($1,572) = **16-28 years to break even**

**Verdict**: Distributed wins for boutique model (migration cost too high relative to savings)

---

**Scenario B: Trail SaaS Platform** (10-50 trails/year aggressive growth)
- Year 1: 10 trails (land initial clients)
- Year 2: 30 trails (referral growth)
- Year 3: 80 trails (market expansion)
- Year 5: 200+ trails
- **Model**: Self-service trail creation platform, $500-2K/year per trail

**Distributed economics** (Year 3, 80 trails):
- Cost: 80 × $12 = $960/month ($11,520/year)
- Ansible deployment at scale (10-50 trails = manageable, 80+ trails = operational burden)
- **Problem**: 80 independent deployments, 80 health checks, 80 backup processes

**Platform economics** (Year 3, 80 trails centralized):
- Cost: Supabase Team $599/month ($7,188/year) or negotiate custom
- Migration: $25,500-43,500 (Year 1 sunk cost)
- **Total Year 1**: $32,688-50,688, **Year 2**: $7,188, **Year 3**: $7,188

**Platform ROI**:
- Year 3 savings: $11,520 (distributed) - $7,188 (platform) = $4,332/year
- Migration cost recovery: $25,500-43,500 ÷ $4,332 = 6-10 years
- **Break-even**: Year 7-11

**Centralized features enable SaaS**:
- **Unified admin dashboard**: Manage 80 trails from Supabase Studio (vs SSH into 80 droplets)
- **Cross-trail analytics**: "Show me top 10 activities across all trails" (distributed can't answer)
- **Shared content library**: Reuse QR templates, activities across trails (distributed requires manual sync)
- **Real-time leaderboards**: "Which trails have most scans today?" (platform enables, distributed doesn't)

**Verdict**: Platform wins for SaaS model (centralization required for product features, break-even Year 7-11 acceptable for aggressive growth)

---

### 4.2 Feature Requirements

**Current QRCards features** (working today):
- ✅ QR token resolution (<100ms)
- ✅ Database-driven routing (dynamic paths)
- ✅ Multi-tenant (multiple trails via separate deployments)
- ✅ Template-based content (Jinja2 templates)
- ✅ Admin tools (CLI for trail setup, DAP processor for content generation)

**Features NOT currently needed** (but platform enables):
- ❌ User authentication (public QR content, no login)
- ❌ Real-time analytics (static scan logs, no live dashboards)
- ❌ Cross-trail queries ("top activities across all trails")
- ❌ Shared content library (each trail independent content)
- ❌ Email notifications (no transactional emails)
- ❌ Collaborative editing (single admin per trail)

**Platform bundle waste** (from finding 14):
- Supabase Auth: $25/month value (QRCards uses $0 - no auth)
- Supabase Real-time: $15/month value (QRCards uses $0 - no live sync)
- Supabase Storage: $15/month value (QRCards uses ~$5 - filesystem works)
- **Total waste**: $55/month bundle value, QRCards uses $20 equivalent (database only)

**Service subtraction strategy** (from SERVICE_SUBTRACTION_STRATEGY.md):
> "Platform bundles pressure you to use bundled services. Distributed architecture lets you maintain service subtraction: only pay for what you need."

**QRCards distributed advantage**: Avoids $55/month bundle waste by not migrating to platform

---

### 4.3 Operational Complexity

**Distributed operational tasks** (per trail):
- Deployment: Ansible playbook (5 minutes for all trails)
- Monitoring: DigitalOcean dashboard per droplet + UptimeRobot ping checks
- Backups: Cron job SQLite tar.gz (automated, $1/month snapshots)
- Updates: Ansible deploys QRCards update to all trails (10 minutes)
- Debugging: SSH into specific trail droplet, check logs

**Platform operational tasks** (all trails):
- Deployment: Vercel git push (auto-deploy to all trails)
- Monitoring: Supabase Studio dashboard (all trails in one view)
- Backups: Supabase automated (point-in-time recovery included)
- Updates: Push to main branch (all trails update instantly)
- Debugging: Supabase logs, query recent scans across all trails

**Operational complexity comparison** (10 trails):

| Task | Distributed (10 droplets) | Platform (Supabase) |
|------|---------------------------|---------------------|
| **Deploy update** | 10 minutes (Ansible all) | 2 minutes (git push) |
| **Check health** | 10 dashboards (DO + UptimeRobot) | 1 dashboard (Supabase Studio) |
| **Backup** | 10 cron jobs, 10 snapshot configs | Automatic (included) |
| **Debug QR issue** | SSH into trail droplet, grep logs | Query Supabase logs (all trails) |
| **Analytics query** | Export 10 SQLite DBs, aggregate manually | Single PostgreSQL query |

**Platform wins on ops simplicity**: One dashboard, one deployment, one backup system

**Distributed wins on independence**: One trail down ≠ all trails down, update one trail without touching others

**Trade-off**: Platform reduces ops overhead, distributed reduces blast radius

**When ops complexity matters**:
- <5 trails: Distributed overhead minimal (Ansible makes it easy)
- 5-20 trails: Distributed ops manageable (scripts automate most tasks)
- >20 trails: Platform wins (centralized dashboard scales, distributed doesn't)

---

### 4.4 Decision Matrix

```
                  Trail Growth Projection
               Boutique          SaaS
              (2-20 trails)   (50-200+ trails)
           ┌──────────────┬──────────────┐
           │              │              │
Feature    │  DISTRIBUTED │   PLATFORM   │
Needs      │   (Ansible   │  (Supabase   │
 Simple    │   multi-     │   multi-     │
(no cross- │   deploy)    │   tenant)    │
trail)     │              │              │
           ├──────────────┼──────────────┤
           │              │              │
 Complex   │  DISTRIBUTED │   PLATFORM   │
(cross-    │  + MANUAL    │  (Supabase   │
trail      │  AGGREGATION │   unified)   │
analytics) │              │              │
           └──────────────┴──────────────┘
```

**Quadrant 1: Boutique + Simple Features → Distributed (Recommended)**
- Use case: 2-20 independent trail clients, public QR content, no cross-trail features
- Why: Service subtraction wins ($55/month bundle waste avoided), independence valued, distributed economics favor low trail count
- **QRCards current fit**: Harvard Extension + Melrose Loop = 2 trails, no auth/email/real-time needed

**Quadrant 2: SaaS + Simple Features → Platform (if >20 trails)**
- Use case: 50+ trails, still no cross-trail features, but operational simplicity needed
- Why: Distributed ops overhead (50 droplets, 50 backups, 50 health checks) > platform simplicity

**Quadrant 3: Boutique + Complex Features → Distributed + Manual Aggregation**
- Use case: 5-15 trails, clients want cross-trail analytics ("top activities across our 3 trails")
- Why: Don't migrate entire stack to platform for occasional aggregation query, export SQLite → aggregate manually

**Quadrant 4: SaaS + Complex Features → Platform (Required)**
- Use case: Self-service trail creation platform, real-time leaderboards, shared content library, cross-trail profiles
- Why: Centralized database required for product features, platform migration justified by SaaS economics

---

## 5. Recommended Strategy: Hybrid Approach

### 5.1 Phase 1: Distributed Start (Months 1-12)

**Current state**: 2 trails (Harvard Extension, Melrose Loop) on PythonAnywhere

**Immediate action** (next 30-60 days):
1. **Migrate to DigitalOcean droplets** (distributed architecture)
   - Create 2 droplets ($12/month each = $24/month, saves $0 vs PythonAnywhere $20 but gains control)
   - Deploy QRCards to each droplet (nginx + gunicorn + SQLite)
   - Migrate databases (copy SQLite files)
   - Update DNS (harvardextension.qrcard.io, melroseloop.qrcard.io)
   - Time: 15-25 hours ($2,250-3,750)

2. **Build Ansible automation** (one-time investment)
   - Playbook for multi-droplet deployment
   - Inventory management (add trails easily)
   - Automated health checks
   - Backup automation (cron + DO snapshots)
   - Time: 10-15 hours ($1,500-2,250)

3. **Service subtraction audit**
   - Verify no auth needed (public QR content confirmed)
   - Verify no email needed (no transactional notifications)
   - Verify no real-time needed (static scan logs)
   - **Result**: Confirm $55/month bundle waste avoided vs Supabase

**First year economics** (2 trails):
- Distributed: $24/month × 12 = $288 + $3,750-6,000 setup = $4,038-6,288
- Supabase: $25/month × 12 = $300 + $25,500-43,500 migration = $25,800-43,800
- **Distributed saves $21,762-37,512 Year 1**

**Trail 3-10 growth** (Months 6-12):
- Add droplet per trail: $12/month × 8 new = $96/month additional
- Ansible deploys new trails: 2 hours setup per trail
- Year 1 total (10 trails by month 12): $120/month = $1,440/year
- **Still cheaper than Supabase migration** ($1,440 < $25,800-43,800)

---

### 5.2 Phase 2: Evaluate Platform Migration Trigger (Month 12-24)

**Decision point triggers** (when to consider platform migration):

**Trigger 1: Trail count >20** (operational complexity threshold)
- Distributed ops: 20 droplets, 20 health checks, 20 backup configs → getting unwieldy
- Platform ops: 1 Supabase dashboard, 1 deployment, automatic backups → scales better
- **Action**: If >20 trails, calculate platform migration ROI

**Trigger 2: Cross-trail features requested** (clients want analytics)
- Client asks: "Show me top 10 activities across all my trails"
- Distributed can't answer efficiently (requires manual SQLite export + aggregation)
- Platform answers with single PostgreSQL query
- **Action**: If cross-trail features become product differentiator, migrate to platform

**Trigger 3: SaaS pivot** (self-service trail creation)
- Business model shifts from boutique ($5K-15K custom trails) to SaaS ($500-2K self-service)
- SaaS requires: unified admin dashboard, shared content library, real-time leaderboards
- Distributed architecture can't support SaaS features
- **Action**: Platform migration required for SaaS product

**Trigger 4: Acquisition or enterprise client** (compliance requirements)
- Enterprise client requires SOC 2, HIPAA, PCI DSS compliance
- Distributed droplets: Self-managed compliance (expensive, complex)
- Platform (Supabase/AWS RDS): Compliance certifications included
- **Action**: Migrate to platform or managed database with compliance certs

**Decision criteria** (Month 12-24):
```python
def should_migrate_to_platform(trail_count, cross_trail_features, saas_pivot, compliance_required):
    # Trigger 1: Trail count
    if trail_count > 20:
        score = 2  # Strong signal
    elif trail_count > 10:
        score = 1  # Moderate signal
    else:
        score = 0

    # Trigger 2: Cross-trail features
    if cross_trail_features == "required":
        score += 3  # Very strong signal
    elif cross_trail_features == "requested":
        score += 1

    # Trigger 3: SaaS pivot
    if saas_pivot:
        score += 4  # Critical signal (can't do SaaS with distributed)

    # Trigger 4: Compliance
    if compliance_required:
        score += 2

    # Decision threshold
    if score >= 5:
        return "MIGRATE NOW"
    elif score >= 3:
        return "PLAN MIGRATION (6-12 months)"
    else:
        return "STAY DISTRIBUTED"
```

**Year 2 status check** (Month 24):
- Trail count: 15 trails (boutique model, score=1)
- Cross-trail features: Not requested (score=0)
- SaaS pivot: No (score=0)
- Compliance: Not required (score=0)
- **Total score**: 1 → **STAY DISTRIBUTED**

---

### 5.3 Phase 3: Incremental Platform Adoption (If Triggered)

**If platform migration triggered** (Month 24-36), use **incremental migration** not rip-and-replace:

**Step 1: Hybrid Architecture** (database platform + distributed apps)
```
Neon PostgreSQL (centralized database)
├── Multi-tenant trails table (all trails)
└── Centralized analytics queries

Trail 1-20: DigitalOcean Droplets (distributed apps)
├── Flask apps query Neon PostgreSQL (no local SQLite)
├── Independent deployments (Ansible)
└── Shared database, distributed compute
```

**Why hybrid first**:
- Keep distributed deployment independence (Ansible, per-trail updates)
- Gain centralized database (cross-trail analytics, shared content)
- Avoid full Next.js rewrite (Flask apps stay, just swap SQLite → Neon)
- Lower migration cost: $10,000-15,000 (database only) vs $25,000-43,500 (full stack)

**Migration steps**:
1. **Deploy Neon PostgreSQL**: $19-69/month (Launch/Scale tier)
2. **Migrate schema**: SQLite → PostgreSQL (30-50 hours)
3. **Update Flask apps**: Replace SQLAlchemy SQLite connection → Neon connection (10-20 hours)
4. **Test multi-tenancy**: Verify trail isolation (RLS policies)
5. **Migrate trails incrementally**: Trail 1 → Neon (test), Trail 2-20 follow
6. **Keep Ansible**: Deploy Flask apps to droplets (still distributed compute)

**Cost**:
- Neon: $19-69/month (database only)
- Droplets: 20 × $12 = $240/month (apps still distributed)
- **Total**: $259-309/month ($3,108-3,708/year)

**vs Full Platform** (Supabase + Vercel):
- Supabase: $25/month (database + unused auth/storage/real-time)
- Vercel: $0-20/month (Next.js hosting)
- **Total**: $25-45/month ($300-540/year)

**Hybrid more expensive** ($3,108 vs $300), but:
- ✅ Keep distributed deployment independence
- ✅ Avoid Next.js rewrite (Flask apps work)
- ✅ Incremental migration (lower risk)
- ✅ Escape hatch (can go back to SQLite if Neon doesn't work)

**When to move from hybrid to full platform** (Neon + distributed → Supabase + Vercel):
- Trail count >50 (distributed app ops overhead > platform centralization)
- SaaS pivot (need unified frontend, admin dashboard, billing)
- Neon cost >$300/month (Supabase bundle becomes cheaper)

---

## 6. Final Recommendation

### 6.1 Path A: Distributed (Start Here)

**For QRCards current state** (2 trails, boutique model, simple features):

**Immediate actions** (next 60 days):
1. ✅ **Migrate PythonAnywhere → DigitalOcean droplets** (distributed architecture foundation)
   - 2 droplets × $12 = $24/month
   - Setup time: 15-25 hours
   - Benefit: Full control, preparation for multi-trail scaling

2. ✅ **Build Ansible automation** (multi-droplet deployment)
   - Playbook + inventory management
   - Setup time: 10-15 hours
   - Benefit: Deploy to N trails in 5 minutes (scales to 100+ trails)

3. ✅ **Service subtraction audit** (confirm no auth/email/real-time needed)
   - Verify public QR content (no auth)
   - Verify no transactional emails (no SendGrid/Resend)
   - Verify no real-time features (no Ably/Pusher)
   - Benefit: Avoid $55/month platform bundle waste

**Year 1 investment**:
- Setup: $3,750-6,000 (migration + Ansible)
- Ongoing: $288-1,440 (2-10 trails)
- **Total**: $4,038-7,440

**Year 2+ ongoing**:
- $1,440/year (10 trails assumed)
- Add $144/year per trail ($12/month)

**When to pivot** (evaluate quarterly):
- Trail count >20: Consider platform for ops simplicity
- Cross-trail features requested: Hybrid architecture (Neon + distributed apps)
- SaaS pivot: Full platform migration (Supabase + Vercel)

---

### 6.2 Path B: Platform (Defer Until Triggered)

**Don't migrate to platform until**:
- Trail count >20 (operational complexity threshold)
- OR cross-trail features required (analytics, shared content)
- OR SaaS business model (self-service trail creation)
- OR compliance requirements (SOC 2, HIPAA for enterprise clients)

**If/when triggered, use incremental migration**:
1. **Hybrid first**: Neon PostgreSQL + distributed Flask apps (avoid full rewrite)
2. **Test centralization**: Cross-trail analytics, shared content library
3. **Evaluate full platform**: If hybrid cost >$300/month, consider Supabase bundle

**Migration budget** (when triggered):
- Hybrid (Neon + distributed): $10,000-15,000 migration
- Full platform (Supabase + Vercel): $25,000-43,500 migration

**Don't migrate for**:
- Trail count <10 (distributed economics win)
- Service subtraction advantage (no auth/email/real-time needs)
- Client independence valued (separate deployments, billing, updates)

---

### 6.3 Next Steps (60-Day Action Plan)

**Week 1-2: Distributed Architecture Setup**
- [ ] Create DigitalOcean account, provision 2 droplets
- [ ] Deploy QRCards to droplets (nginx + gunicorn + SQLite)
- [ ] Migrate Harvard Extension database (test QR resolution)
- [ ] Update DNS (harvardextension.qrcard.io → new droplet)

**Week 3-4: Ansible Automation**
- [ ] Build Ansible playbook (deploy, health check, backup)
- [ ] Test multi-droplet deployment (2 trails)
- [ ] Document runbook (adding new trails, debugging)

**Week 5-6: Melrose Loop Migration**
- [ ] Deploy Melrose Loop to second droplet
- [ ] Verify independence (update Harvard without touching Melrose)
- [ ] Test disaster recovery (restore from backup)

**Week 7-8: Service Subtraction Validation**
- [ ] Confirm no auth provider needed (public QR content)
- [ ] Confirm no email service needed (no transactional emails)
- [ ] Confirm no real-time needed (static scan logs)
- [ ] Document savings: $55/month bundle waste avoided

**Month 3+: Trail 3-10 Growth**
- [ ] Add trail → spin up droplet → Ansible deploy (2 hours per trail)
- [ ] Monitor costs: $12/month per trail vs $25 Supabase for all
- [ ] Evaluate quarterly: Should we migrate to platform? (see trigger criteria)

---

### 6.4 Decision Criteria Summary

**Stay Distributed if**:
- ✅ Trail count <20
- ✅ No cross-trail features needed
- ✅ Service subtraction advantage (no auth/email/real-time)
- ✅ Client independence valued
- ✅ Existing architecture works (SQLite sufficient, Flask mature)

**Migrate to Platform if**:
- ⚠️ Trail count >20 (ops complexity threshold)
- ⚠️ Cross-trail analytics required (can't do with distributed)
- ⚠️ SaaS pivot (self-service trail creation platform)
- ⚠️ Compliance requirements (SOC 2, HIPAA for enterprise)
- ⚠️ Modern stack desired (React vs Jinja2, PostgreSQL vs SQLite)

**Current verdict** (2 trails, boutique model, simple features):
→ **START DISTRIBUTED, PIVOT IF TRIGGERED**

---

**Status**: Analysis complete. Ready for 60-day distributed architecture implementation or platform migration planning if triggers met.

**Cross-references**:
- Finding 11: SERVICE_BUNDLING_AUTH_EMAIL_DEPENDENCIES.md
- Finding 14: SERVICE_BUNDLING_DATABASE_BACKEND_PLATFORMS.md
- Experiments: 3.012-authentication, 3.020-email-communication, 3.040-database-services
- QRCards: docs/training/02-system-architecture-overview.md, docs/training/14-deployment-production-operations.md
