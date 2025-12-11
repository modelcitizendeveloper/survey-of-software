# Multi-Service Architecture Strategy for QRCards

**Date:** November 18, 2025
**Context:** Render pricing update + Flask vs TypeScript strategic analysis
**Question:** Should QRCards use separate services for backend (QR scans), database, and frontend (dashboard)?
**Related:** FLASK_VS_TYPESCRIPT_STRATEGIC_ANALYSIS.md, 2.050_PAAS_STRATEGIC_ASSESSMENT.md

---

## Executive Summary

**RECOMMENDATION: Start monolithic (single Render Flask service), migrate to multi-service architecture at 10+ customers when hiring triggers**

**The Three-Service Pattern:**
```
Service 1: Render Flask ($9/mo) → QR scans, landing pages, API
Service 2: Supabase ($25/mo) → Database, auth, storage (shared)
Service 3: Vercel/Netlify ($0-20/mo) → Customer dashboard (React/TypeScript)

Total: $34-54/month vs $28 monolithic (+$6-26)
```

**Key Insight:** Multi-service architecture is NOT about technology elegance. It's about **team parallelization** and **independent scaling**. The $6-26/month infrastructure premium only makes sense when development velocity gain exceeds cost increase.

**Decision Framework:**

| Stage | Customers | Architecture | Cost/month | Trigger |
|-------|-----------|--------------|------------|---------|
| **Pre-revenue** | 0 | Monolithic Flask + SQLite | $9 | Ship fast, find customers |
| **Early revenue** | 1-10 | Monolithic Flask + Database | $28-34 | First paying customer |
| **Growth** | 10-50 | **Multi-service** (Flask + React + DB) | $34-54 | Hiring frontend dev |
| **Scale** | 50-100+ | Multi-service (optimized) | $50-100+ | Team scaling, optimization |

**When multi-service makes sense:**
1. **Hiring developers** → Frontend/backend specialists work independently
2. **Interactive dashboard primary** → React advantages worth separate service
3. **Different scaling patterns** → QR scans vs dashboard traffic diverge
4. **Technology choice freedom** → Python backend + TypeScript frontend

**When to stay monolithic:**
- Solo founder (you're coding everything)
- Pre-revenue or early revenue (0-10 customers)
- Simple UI (server-rendered templates sufficient)
- Optimize for speed, not architecture elegance

**Migration trigger:** Hire first frontend developer OR customer dashboard becomes primary product (not simple QR scans).

---

## The Multi-Service Architecture Pattern

### Architecture Overview

```
                        ┌─────────────────────────┐
                        │    END USERS            │
                        │  (scan QR codes)        │
                        └────────────┬────────────┘
                                     │
                                     ▼
                   ┌─────────────────────────────────┐
                   │   SERVICE 1: QR Backend         │
                   │   Render Flask ($9/mo)          │
                   │                                 │
                   │   - QR code resolution          │
                   │   - Serve HTML landing pages    │
                   │   - API endpoints (RESTful)     │
                   │   - DAP Processor (content gen) │
                   └─────────────┬───────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
         ┌──────────────────────┐  ┌──────────────────────────┐
         │  SERVICE 2: Database │  │  SERVICE 3: Dashboard UI │
         │  Supabase ($25/mo)   │◄─┤  Vercel ($0-20/mo)       │
         │                      │  │                          │
         │  - PostgreSQL        │  │  - React/TypeScript      │
         │  - Auth (Supabase)   │  │  - Customer dashboard    │
         │  - Storage (files)   │  │  - Analytics charts      │
         │  - Row-level security│  │  - Trail management UI   │
         └──────────────────────┘  └──────────────────────────┘
                    ▲                         │
                    └─────────────────────────┘
                   Direct connection (no Flask middleman)
```

### Service Responsibilities

#### Service 1: Backend (Render Flask) - The Content Engine

**Purpose:** Handle QR scans, serve landing pages, process content

**Technology:** Python/Flask (optimized for content processing)

**Responsibilities:**
- QR code token resolution (lookup in database)
- Serve HTML landing pages (Jinja2 templates)
- Scan logging (record to database)
- RESTful API endpoints (for dashboard consumption)
- DAP Processor (content generation pipeline - Python strength)
- Admin tools (internal use)

**Why Flask/Python:**
- Excellent for content processing (Markdown, templating, text manipulation)
- Mature libraries (Python-Markdown, Jinja2, GPT SDK)
- Lightweight (512MB RAM sufficient for QR resolution)
- Fast for server-side rendering (QR → HTML in <100ms)

**Deployment:**
- Platform: Render
- Cost: $9/month (Starter tier)
- Region: Single (US West or closest to users)
- Auto-scaling: Not needed (fixed $9/mo resources)

**Example code:**
```python
# app.py (Render Flask)
from flask import Flask, render_template, request, jsonify
from supabase import create_client

app = Flask(__name__)
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# QR resolution endpoint (end users)
@app.route('/qr/<token>')
def resolve_qr(token):
    # Look up token in Supabase
    trail = supabase.table('trails').select('*').eq('token', token).single().execute()

    # Log scan
    supabase.table('scans').insert({
        'token': token,
        'timestamp': datetime.now().isoformat(),
        'user_agent': request.headers.get('User-Agent'),
        'ip_address': request.remote_addr
    }).execute()

    # Serve HTML landing page
    return render_template('trail.html', trail=trail.data)

# API endpoint (dashboard consumption)
@app.route('/api/customers/<customer_id>/trails')
def get_customer_trails(customer_id):
    # Verify API key (service-to-service auth)
    if request.headers.get('X-API-Key') != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401

    trails = supabase.table('trails').select('*').eq('customer_id', customer_id).execute()
    return jsonify(trails.data)

# DAP Processor endpoint (content generation)
@app.route('/api/generate-trail', methods=['POST'])
def generate_trail():
    # Python strength: content processing pipeline
    content = request.json['markdown_content']

    # Process with DAP (Document Assembly Pipeline)
    processed = dap_processor.process(content)

    # Store in Supabase
    trail = supabase.table('trails').insert(processed).execute()

    return jsonify(trail.data)
```

**When to scale:**
- Traffic: >10,000 QR scans/month → Upgrade to Standard tier ($25/mo, 1 vCPU)
- Processing: Heavy DAP processing → Add background workers (Render workers)

---

#### Service 2: Database (Supabase) - The Shared Truth

**Purpose:** Centralized data store, authentication, file storage

**Technology:** PostgreSQL + Supabase platform (RLS, Auth, Storage)

**Responsibilities:**
- PostgreSQL database (trails, scans, customers, users)
- Authentication (Supabase Auth - email, OAuth, magic links)
- File storage (trail images, PDFs, user uploads)
- Row-level security (RLS - multi-tenant data isolation)
- Real-time subscriptions (optional - dashboard live updates)

**Why Supabase:**
- PostgreSQL (industry standard, portable)
- Built-in auth (saves $25/month Clerk or Firebase integration)
- Row-level security (multi-tenant isolation, security by default)
- Real-time subscriptions (WebSocket updates, no custom infrastructure)
- Open source (MIT license, self-hosting option if acquired)

**Deployment:**
- Platform: Supabase Cloud
- Cost: $25/month (Pro tier - 8GB database, 100K MAU auth, 100GB storage)
- Region: Auto-selected (Supabase chooses optimal AWS region)
- Backups: Automatic daily (7-day point-in-time recovery)

**Database schema:**
```sql
-- Customers (QRCards clients)
CREATE TABLE customers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  subdomain TEXT UNIQUE,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Users (customer employees who log into dashboard)
CREATE TABLE users (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  customer_id UUID REFERENCES customers(id),
  email TEXT NOT NULL,
  role TEXT DEFAULT 'viewer',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Trails (QR code trails)
CREATE TABLE trails (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID REFERENCES customers(id),
  token TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  content JSONB,
  template TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Scans (QR scan logs)
CREATE TABLE scans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  token TEXT REFERENCES trails(token),
  timestamp TIMESTAMPTZ DEFAULT now(),
  user_agent TEXT,
  ip_address INET,
  referer TEXT
);

-- Row-level security (RLS)
ALTER TABLE trails ENABLE ROW LEVEL SECURITY;
ALTER TABLE scans ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their customer's trails
CREATE POLICY customer_trails ON trails
  FOR SELECT
  USING (
    customer_id IN (
      SELECT customer_id FROM users WHERE id = auth.uid()
    )
  );

-- Policy: Users can only see their customer's scans
CREATE POLICY customer_scans ON scans
  FOR SELECT
  USING (
    token IN (
      SELECT token FROM trails WHERE customer_id IN (
        SELECT customer_id FROM users WHERE id = auth.uid()
      )
    )
  );
```

**Access patterns:**

| Service | Connection | Auth Method | Access Level |
|---------|------------|-------------|--------------|
| **Flask backend** | Supabase client | Service key | Full access (bypass RLS) |
| **React dashboard** | Supabase client | User JWT | RLS-filtered (customer data only) |
| **Direct SQL** | psql connection | Database password | Full access (admin only) |

**When to scale:**
- Storage: >8GB database → Upgrade to higher tier ($55+/mo)
- Users: >100K MAU → Pay overage fees ($0.00325 per MAU)
- Features: Need database branching → Consider Neon migration

---

#### Service 3: Frontend (Vercel/Netlify) - The Customer Experience

**Purpose:** Interactive customer dashboard, self-service portal

**Technology:** React + TypeScript + Next.js (modern web stack)

**Responsibilities:**
- Customer authentication UI (login, signup, password reset)
- Dashboard home (overview, recent scans, analytics)
- Trail management (create, edit, delete trails)
- Analytics charts (scan trends, geographic distribution)
- Settings (user profile, billing, team management)

**Why React/TypeScript:**
- Best-in-class UI libraries (Shadcn/UI, Radix, Recharts)
- Type safety (end-to-end types from database to UI)
- Rich interactivity (no page refreshes, smooth UX)
- Developer experience (hot reload, component libraries)
- Ecosystem maturity (massive npm ecosystem)

**Why separate from Flask:**
- **Independent deployment:** Update dashboard without backend restart
- **Technology choice:** TypeScript for UI, Python for content processing
- **Team parallelization:** Frontend dev works independently from backend dev
- **Scaling independence:** Dashboard traffic != QR scan traffic

**Deployment:**
- Platform: Vercel (Next.js optimized) or Netlify
- Cost: $0/month (Hobby tier, <100GB bandwidth) or $20/month (Pro)
- Region: Global CDN (edge deployment, <100ms worldwide)
- Auto-scaling: Automatic (serverless, infinite scale)

**Example code:**
```typescript
// app/dashboard/page.tsx (Next.js + TypeScript)
'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@supabase/supabase-js'
import { BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
)

interface Trail {
  id: string
  name: string
  token: string
  created_at: string
}

interface Scan {
  timestamp: string
  token: string
}

export default function Dashboard() {
  const [trails, setTrails] = useState<Trail[]>([])
  const [scans, setScans] = useState<Scan[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  async function fetchDashboardData() {
    // Connect directly to Supabase (no Flask middleman)
    // RLS automatically filters by logged-in user's customer_id

    const { data: trailsData } = await supabase
      .from('trails')
      .select('*')
      .order('created_at', { ascending: false })

    const { data: scansData } = await supabase
      .from('scans')
      .select('*')
      .gte('timestamp', new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString())

    setTrails(trailsData || [])
    setScans(scansData || [])
    setLoading(false)
  }

  if (loading) return <div>Loading...</div>

  return (
    <div className="dashboard">
      <h1>Your QR Code Trails</h1>

      {/* Trail list */}
      <div className="trails-grid">
        {trails.map(trail => (
          <TrailCard key={trail.id} trail={trail} />
        ))}
      </div>

      {/* Analytics chart */}
      <div className="analytics">
        <h2>Scans (Last 30 Days)</h2>
        <BarChart width={600} height={300} data={scansByDay(scans)}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#8884d8" />
        </BarChart>
      </div>
    </div>
  )
}

// Helper: Group scans by day
function scansByDay(scans: Scan[]) {
  const grouped: Record<string, number> = {}
  scans.forEach(scan => {
    const date = scan.timestamp.split('T')[0]
    grouped[date] = (grouped[date] || 0) + 1
  })
  return Object.entries(grouped).map(([date, count]) => ({ date, count }))
}
```

**When to scale:**
- Traffic: >100GB bandwidth/month → Upgrade to Pro ($20/mo)
- Features: Need ISR, middleware → Already included (Next.js)
- Team: Multiple frontend devs → Vercel Teams ($20/seat/month)

---

## Communication Patterns

### Pattern 1: QR Scan Flow (End User → Flask → Database)

**Scenario:** Someone scans a QR code, lands on trail page

```
┌─────────┐
│  User   │ Scans QR code: qrcard.app/qr/abc123
└────┬────┘
     │
     ▼
┌─────────────────┐
│  Render Flask   │ 1. Receive request (GET /qr/abc123)
│                 │ 2. Query Supabase: SELECT * FROM trails WHERE token='abc123'
│                 │ 3. Log scan: INSERT INTO scans (token, timestamp, user_agent)
│                 │ 4. Render template: Jinja2 → HTML
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│  Supabase DB    │ Returns trail data + records scan
└─────────────────┘
     │
     ▼
┌─────────┐
│  User   │ Receives HTML page (trail landing page)
└─────────┘
```

**Key points:**
- Flask handles everything (query, log, render)
- User never interacts with database directly
- Fast: <100ms (database lookup + template render)

**Flask advantage:** Server-side rendering (SSR) is ideal for QR landing pages
- SEO-friendly (search engines see HTML)
- Fast load (no JavaScript bundle, just HTML+CSS)
- Works without JavaScript (accessibility)

---

### Pattern 2: Dashboard View (Direct Supabase Connection)

**Scenario:** Customer logs into dashboard, views their trails

```
┌──────────────┐
│  Customer    │ Opens dashboard: dashboard.qrcards.com
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  Vercel (Next.js)│ 1. Load React app (static bundle)
│                  │ 2. User login (Supabase Auth)
│                  │ 3. Fetch data: supabase.from('trails').select('*')
└──────┬───────────┘
       │
       │ Direct connection (bypass Flask)
       ▼
┌──────────────────┐
│  Supabase DB     │ 4. Authenticate user (JWT token)
│  + RLS           │ 5. Filter by customer_id (RLS policy)
│                  │ 6. Return trails (only customer's data)
└──────┬───────────┘
       │
       ▼
┌──────────────┐
│  Customer    │ Sees interactive dashboard (real-time updates possible)
└──────────────┘
```

**Key points:**
- React connects **directly** to Supabase (no Flask middleman)
- Row-level security (RLS) filters data automatically
- Real-time: Supabase can push updates via WebSocket (optional)

**React advantage:** No Flask API needed for simple CRUD operations
- Faster (direct database connection, no API latency)
- Type-safe (TypeScript types generated from database schema)
- Real-time (Supabase subscriptions, live updates)

---

### Pattern 3: Complex Operations (React → Flask → Database)

**Scenario:** Customer creates new trail using DAP Processor (content generation)

```
┌──────────────┐
│  Customer    │ Clicks "Create Trail" → fills form with Markdown content
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  Vercel (Next.js)│ 1. User submits form (POST /api/generate-trail)
│                  │ 2. Call Flask API: fetch('render.app/api/generate-trail')
└──────┬───────────┘
       │
       ▼
┌─────────────────┐
│  Render Flask   │ 3. Receive Markdown content
│  DAP Processor  │ 4. Process with DAP (Python pipeline)
│                 │    - Parse Markdown
│                 │    - Generate HTML
│                 │    - Create QR token
│                 │    - Transform content
└──────┬──────────┘
       │
       ▼
┌──────────────────┐
│  Supabase DB     │ 5. Insert new trail (processed content)
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Vercel (Next.js)│ 6. Receive confirmation (trail created)
│                  │ 7. Refresh trail list (fetch from Supabase directly)
└──────┬───────────┘
       │
       ▼
┌──────────────┐
│  Customer    │ Sees new trail in dashboard
└──────────────┘
```

**Key points:**
- Complex operations (DAP processing) still go through Flask
- Python is better for content processing than TypeScript
- React calls Flask API, Flask writes to Supabase
- After processing, React can fetch directly from Supabase (skip Flask)

**Hybrid approach advantage:** Use each language for its strength
- Python (Flask): Content processing, text manipulation, AI prompts
- TypeScript (React): Interactive UI, real-time updates, rich forms

---

### Pattern 4: Real-Time Updates (Supabase Subscriptions)

**Scenario:** Dashboard shows live scan count as QR codes are scanned

```
┌──────────────┐                        ┌─────────┐
│  Customer    │                        │  User   │ Scans QR code
│  (dashboard) │                        └────┬────┘
└──────┬───────┘                             │
       │                                     ▼
       │ Subscribe to scans table     ┌─────────────────┐
       │ (WebSocket connection)       │  Render Flask   │ Insert scan record
       │                              └────┬────────────┘
       ▼                                   │
┌──────────────────┐                       ▼
│  Supabase        │◄──────────────────────┤
│  Real-time       │ New scan inserted     │
│  (WebSocket)     │                       │
└──────┬───────────┘                       │
       │                                   │
       │ Push update to subscribers        │
       ▼                                   ▼
┌──────────────┐                    ┌─────────────────┐
│  Customer    │                    │  Supabase DB    │
│  (dashboard) │                    │  scans table    │
│              │                    └─────────────────┘
│ Chart updates│
│ automatically│
└──────────────┘
```

**Key points:**
- React subscribes to Supabase real-time (WebSocket)
- Flask inserts scan → Supabase broadcasts → React updates UI
- No polling (efficient, instant updates)

**Example code:**
```typescript
// Real-time subscription (React)
useEffect(() => {
  const subscription = supabase
    .channel('scans')
    .on('postgres_changes', {
      event: 'INSERT',
      schema: 'public',
      table: 'scans'
    }, (payload) => {
      // New scan detected, update chart
      setScans(prev => [...prev, payload.new])
    })
    .subscribe()

  return () => subscription.unsubscribe()
}, [])
```

**Real-time advantage:** Dashboard feels alive, no manual refresh needed

---

## Cost Comparison: Monolithic vs Multi-Service

### Scenario A: Monolithic Flask (Single Service)

**Architecture:**
```
Render Flask (all-in-one):
├─ QR resolution
├─ Dashboard (server-rendered Jinja2 templates)
├─ API endpoints
├─ DAP Processor
└─ PostgreSQL database (Render managed)
```

**Cost breakdown:**
```
Render web service: $9/month (Starter - 512MB RAM, 0.5 CPU)
Render PostgreSQL:  $19/month (Basic-1gb - 1GB storage)
Total: $28/month
```

**Pros:**
- **Simplest deployment** (single service, one codebase)
- **Lowest cost** ($28/month total)
- **Fewest moving parts** (easier to debug)
- **Solo-friendly** (one developer can manage everything)

**Cons:**
- **Technology lock-in** (dashboard stuck with Flask/Jinja2 templates)
- **Coupled deployment** (dashboard update requires backend restart)
- **Limited scalability** (QR + dashboard scale together, wasteful)
- **Hiring constraint** (need full-stack Flask developer, niche skill)

**When to choose:**
- Pre-revenue or early revenue (0-10 customers)
- Solo founder (you're coding everything)
- Simple dashboard (server-rendered templates acceptable)
- Optimize for speed and simplicity

---

### Scenario B: Multi-Service (Flask + Supabase + React)

**Architecture:**
```
Service 1: Render Flask
├─ QR resolution
├─ API endpoints
└─ DAP Processor

Service 2: Supabase
├─ PostgreSQL database
├─ Auth (Supabase)
└─ Storage (files)

Service 3: Vercel (React)
├─ Customer dashboard
├─ Analytics UI
└─ Trail management
```

**Cost breakdown:**
```
Render Flask:     $9/month (QR backend, API)
Supabase Pro:    $25/month (database + auth + storage)
Vercel Hobby:     $0/month (free tier, <100GB bandwidth)
Total: $34/month (+$6 vs monolithic)
```

**OR with Vercel Pro:**
```
Render Flask:     $9/month
Supabase Pro:    $25/month
Vercel Pro:      $20/month (>100GB bandwidth, team features)
Total: $54/month (+$26 vs monolithic)
```

**Pros:**
- **Technology freedom** (Python for content, TypeScript for UI)
- **Independent deployment** (update dashboard without backend restart)
- **Team parallelization** (frontend + backend devs work independently)
- **Independent scaling** (scale QR backend separately from dashboard)
- **Better UX** (React dashboard > Flask templates for interactive UI)
- **Hiring flexibility** (hire frontend specialists, backend specialists separately)

**Cons:**
- **Higher cost** (+$6-26/month infrastructure)
- **More complexity** (three services to manage)
- **Coordination overhead** (API contracts, schema changes)
- **Learning curve** (TypeScript + React for dashboard)

**When to choose:**
- Growth stage (10-50 customers)
- Hiring developers (frontend + backend specialists)
- Interactive dashboard critical (React advantages significant)
- Different scaling needs (QR scans != dashboard traffic)

---

### Break-Even Analysis: When Does Multi-Service Pay Off?

**Cost differential:** $6-26/month ($72-312/year)

**Break-even scenarios:**

#### Scenario 1: Hiring Frontend Developer

**Monolithic Flask:**
- Need full-stack Flask developer (rare, expensive)
- Hiring time: 2-3 months (niche skill)
- Hourly rate: $120-180/hour (specialized)

**Multi-service:**
- Hire frontend specialist (React/TypeScript - common skill)
- Hiring time: 2-4 weeks (large talent pool)
- Hourly rate: $80-120/hour (commodity skill)

**Savings:**
- Faster hiring: 1.5-2.5 months saved = $20K-40K opportunity cost
- Lower rate: $40-60/hour difference = $6,400-9,600/year (full-time)

**Break-even:** First month of hiring (faster + cheaper developers > $6-26/mo infrastructure)

---

#### Scenario 2: Development Velocity

**Monolithic Flask (single developer):**
- Update dashboard → Deploy entire app → Restart backend
- Risk: Backend deployment can break QR resolution
- Deployment frequency: Conservative (weekly, avoid customer disruption)

**Multi-service (separate deployments):**
- Update dashboard → Deploy React only → No backend impact
- Risk: Zero (dashboard independent from QR backend)
- Deployment frequency: Aggressive (daily, safe iterations)

**Productivity gain:**
- 4x more dashboard deployments (daily vs weekly)
- Faster feature iteration = more customer feedback
- Reduced deployment risk = less debugging time

**Value of velocity:**
- 1 extra feature/week × 4 weeks = 4 features/month
- Customer retention impact: 5-10% (better UX from rapid iteration)
- On $10K MRR: $500-1,000/month retention value

**Break-even:** First month (velocity gain > $6-26/mo infrastructure cost)

---

#### Scenario 3: Scaling Independence

**Example traffic pattern:**
```
QR scans:      10,000/month (steady, predictable)
Dashboard:     50 users × 100 page views = 5,000 views/month

Monolithic: Scale to $25 Render tier (both QR + dashboard)
Multi-service: Keep QR at $9, dashboard free (Vercel Hobby)

Savings: $16/month ($25 - $9)
```

**Break-even:** When QR and dashboard have different scaling needs (common at 50+ customers)

---

### Decision Matrix: Monolithic vs Multi-Service

| Factor | Monolithic Flask | Multi-Service | Winner |
|--------|-----------------|---------------|--------|
| **Cost** | $28/mo | $34-54/mo | Monolithic (-$6-26) |
| **Complexity** | LOW (1 service) | MEDIUM (3 services) | Monolithic |
| **Solo velocity** | HIGH (familiar stack) | MEDIUM (learning curve) | Monolithic |
| **Team velocity** | LOW (coordination overhead) | HIGH (independent work) | Multi-service |
| **Hiring** | HARD (niche Flask skill) | EASY (common React skill) | Multi-service |
| **Dashboard UX** | BASIC (Jinja2 templates) | EXCELLENT (React) | Multi-service |
| **Technology choice** | LIMITED (Flask only) | FLEXIBLE (Python + TypeScript) | Multi-service |
| **Scaling** | COUPLED (QR + dashboard together) | INDEPENDENT (optimize each) | Multi-service |
| **Deployment risk** | MEDIUM (full app restart) | LOW (dashboard independent) | Multi-service |

**Recommendation:**
- **0-10 customers:** Monolithic Flask (simplicity wins)
- **10-50 customers:** Multi-service (team velocity wins)
- **50+ customers:** Multi-service (scaling independence wins)

---

## Migration Path: Monolithic → Multi-Service

### Phase 1: Monolithic Flask + SQLite (Today)

**Goal:** Ship fast, find customers

**Architecture:**
```
Render Flask ($9/mo):
├─ QR resolution
├─ Simple dashboard (Jinja2 templates)
├─ SQLite databases (admin_prod.db, runtime_prod.db)
└─ DAP Processor
```

**Why:**
- Fastest path to production (working Flask code)
- Lowest cost ($9/mo, no database service)
- SQLite adequate for demo traffic (0 customers)

**Timeline:** Now (already planned in 2.050 PaaS assessment)

**Deliverable:** QRCards on Render, PythonAnywhere decommissioned

---

### Phase 2: Add Managed Database (First Customer)

**Goal:** Multi-tenant data isolation

**Architecture:**
```
Render Flask ($9/mo):
├─ QR resolution
├─ Dashboard (still Jinja2)
├─ API endpoints
└─ DAP Processor

Supabase ($25/mo):
├─ PostgreSQL (migrate from SQLite)
├─ Auth (basic setup, not used yet)
└─ Storage (future)
```

**Changes:**
- Migrate SQLite → PostgreSQL (4-8 hours)
- Configure DATABASE_URL (Supabase connection)
- No code changes (same SQL queries, different connection string)

**Why:**
- First customer needs data isolation (RLS)
- Automatic backups (Supabase daily backups)
- Professional infrastructure (vs SQLite files)

**Timeline:** When first customer pays (trigger: $500+ MRR or 1,000 scans/month)

**Deliverable:** PostgreSQL backend, RLS configured, customer data isolated

---

### Phase 3: Split Frontend (Hire Frontend Developer)

**Goal:** Team parallelization, modern dashboard UX

**Architecture:**
```
Render Flask ($9/mo):
├─ QR resolution (unchanged)
├─ API endpoints (new: RESTful JSON)
└─ DAP Processor (unchanged)

Supabase ($25/mo):
├─ PostgreSQL (unchanged)
├─ Auth (now used: customer login)
└─ Storage (now used: file uploads)

Vercel ($0/mo):
├─ React dashboard (NEW)
├─ TypeScript (NEW)
└─ Next.js (NEW)
```

**Changes from Phase 2:**

**Backend (Flask):**
```python
# Old: Render Jinja2 dashboard
@app.route('/dashboard')
def dashboard():
    trails = get_trails(customer_id)
    return render_template('dashboard.html', trails=trails)

# New: API endpoint (JSON)
@app.route('/api/customers/<customer_id>/trails')
def get_customer_trails(customer_id):
    trails = supabase.table('trails').select('*').eq('customer_id', customer_id).execute()
    return jsonify(trails.data)
```

**Frontend (React - NEW):**
```typescript
// app/dashboard/page.tsx
export default function Dashboard() {
  const [trails, setTrails] = useState([])

  useEffect(() => {
    // Connect directly to Supabase (bypass Flask)
    async function fetchTrails() {
      const { data } = await supabase.from('trails').select('*')
      setTrails(data)
    }
    fetchTrails()
  }, [])

  return <TrailList trails={trails} />
}
```

**Migration steps:**
1. Create Vercel account, connect GitHub
2. Build React dashboard (60-120 hours initial build)
3. Configure Supabase Auth (customer login)
4. Migrate customers from Flask dashboard → React dashboard
5. Deprecate Flask dashboard routes (keep API endpoints)

**Why:**
- Hiring frontend developer (React specialist, cheaper + faster to find)
- Modern dashboard UX (interactive, real-time, no page refreshes)
- Independent deployment (dashboard updates don't touch backend)

**Timeline:** When hiring first developer OR customer dashboard becomes critical (10-50 customers)

**Deliverable:** React dashboard live, Flask dashboard deprecated, team parallelization enabled

---

### Phase 4: Optimize Backend (Optional)

**Goal:** Reduce costs or improve performance

**Option A: Keep Flask for Everything (Recommended)**
```
Render Flask ($9/mo) - Keep as-is
Supabase ($25/mo) - Keep as-is
Vercel ($0-20/mo) - Keep as-is
Total: $34-54/mo
```

**Rationale:**
- Flask excellent for content processing (DAP Processor - Python strength)
- No need to rewrite backend (working, tested, stable)
- $9/mo Flask is cheap (not worth rewriting to save $0)

---

**Option B: Migrate Simple APIs to Next.js (Reduce Services)**
```
Next.js API Routes ($0-20/mo Vercel):
├─ Simple CRUD (GET trails, POST scans)
├─ Dashboard API (analytics, user management)
└─ TypeScript (unified frontend + backend)

Render Flask ($9/mo):
├─ DAP Processor (keep Python - its strength)
└─ Complex content processing

Supabase ($25/mo):
├─ PostgreSQL (unchanged)
└─ Auth (unchanged)

Total: $34-54/mo (same cost, one fewer service)
```

**Rationale:**
- Reduce from 3 services to 2.5 (Next.js handles most APIs)
- Keep Python for DAP Processor only (microservice)
- TypeScript end-to-end (frontend + backend, except content processing)

**Migration effort:** 20-40 hours (rewrite simple Flask APIs in TypeScript)

---

**Option C: Full TypeScript (Maximum Unified)**
```
Next.js (Vercel $0-20/mo):
├─ Frontend (React)
├─ Backend API (Next.js API routes)
└─ Content processing (port DAP Processor to TypeScript - 40-80 hours)

Supabase ($25/mo):
├─ PostgreSQL
└─ Auth

Total: $25-45/mo (-$9 Render Flask eliminated)
```

**Rationale:**
- Unified TypeScript codebase (single language, end-to-end types)
- One fewer service ($9/mo savings)
- Simpler deployment (one frontend/backend service instead of two)

**Drawbacks:**
- Rewrite DAP Processor in TypeScript (40-80 hours, loses Python text processing advantages)
- Lose Python ecosystem (weaker text libraries in Node.js)

**When to consider:** 50-100+ customers, team entirely TypeScript-focused, Python ecosystem not needed

---

### Recommended Migration Timeline

| Phase | Trigger | Timeline | Effort | Deliverable |
|-------|---------|----------|--------|-------------|
| **Phase 1** | Now | Week 1-3 | 8-16h | Render Flask + SQLite |
| **Phase 2** | First customer | Week 4 | 4-8h | Add Supabase PostgreSQL |
| **Phase 3** | Hire frontend dev | Month 3-6 | 60-120h | React dashboard |
| **Phase 4** | 50-100 customers | Month 12+ | 20-80h | Optimize (optional) |

**Current recommendation:** Execute Phase 1 now (Render Flask + SQLite migration already planned in 2.050 PaaS assessment).

---

## Service Communication Best Practices

### 1. API Design: RESTful JSON Endpoints

**Flask backend should expose RESTful API:**

```python
# Good: RESTful API (JSON responses)
@app.route('/api/customers/<customer_id>/trails', methods=['GET'])
def get_trails(customer_id):
    trails = supabase.table('trails').select('*').eq('customer_id', customer_id).execute()
    return jsonify({
        'data': trails.data,
        'count': len(trails.data)
    })

@app.route('/api/trails/<trail_id>', methods=['GET'])
def get_trail(trail_id):
    trail = supabase.table('trails').select('*').eq('id', trail_id).single().execute()
    return jsonify(trail.data)

@app.route('/api/trails', methods=['POST'])
def create_trail():
    data = request.json
    trail = supabase.table('trails').insert(data).execute()
    return jsonify(trail.data), 201
```

**React consumes API:**
```typescript
// React: Fetch from Flask API when needed
const createTrail = async (trailData) => {
  const response = await fetch('https://api.qrcards.app/api/trails', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(trailData)
  })
  return response.json()
}
```

---

### 2. Authentication: Service Keys vs User Tokens

**Flask backend (service key - full access):**
```python
# Bypass RLS with service key (admin access)
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY  # Full database access, bypasses RLS
)
```

**React frontend (user JWT - RLS filtered):**
```typescript
// User token respects RLS (customer data only)
const supabase = createClient(
    SUPABASE_URL,
    SUPABASE_ANON_KEY  // Public key, RLS enforced
)

// User logs in
await supabase.auth.signInWithPassword({ email, password })
// All queries now filtered by user's customer_id (RLS)
```

**API key for service-to-service:**
```python
# Flask requires API key for dashboard calls
@app.route('/api/customers/<customer_id>/trails')
def get_trails(customer_id):
    if request.headers.get('X-API-Key') != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    # ...
```

---

### 3. Schema Sharing: TypeScript Types from Database

**Generate TypeScript types from Supabase schema:**

```bash
# Run once: Generate types
npx supabase gen types typescript --project-id <project-id> > types/database.ts
```

**Use types in React:**
```typescript
// types/database.ts (auto-generated)
export interface Trail {
  id: string
  customer_id: string
  token: string
  name: string
  content: Json
  created_at: string
}

// React component (type-safe)
const [trails, setTrails] = useState<Trail[]>([])

const fetchTrails = async () => {
  const { data } = await supabase
    .from('trails')
    .select('*')

  setTrails(data as Trail[])  // Type-safe
}
```

**Benefit:** Change database schema → Regenerate types → TypeScript catches errors at compile time

---

### 4. Direct Database Access: When to Bypass Flask

**Use React → Supabase directly for:**
- Simple CRUD (read trails, create scan)
- Dashboard queries (analytics, charts)
- Real-time subscriptions (live scan count)

**Use React → Flask → Supabase for:**
- Complex operations (DAP Processor, content generation)
- Python-specific logic (text processing, AI prompts)
- Operations requiring server-side secrets (API keys, service keys)

**Example decision tree:**
```
IF operation is simple CRUD:
  → React → Supabase directly (faster, type-safe)

IF operation requires Python processing:
  → React → Flask API → Supabase (leverage Python ecosystem)

IF operation requires sensitive data:
  → React → Flask API → Supabase (keep secrets server-side)
```

---

## Cost Optimization Strategies

### Strategy 1: Start Small, Scale Incrementally

**Month 1-3 (Pre-revenue):**
```
Render Flask + SQLite: $9/mo
→ Eliminate PythonAnywhere ($19.25), save $10.25/mo
```

**Month 4-6 (First customer):**
```
Render Flask + Supabase: $34/mo (+$25)
→ Add database, auth, storage (all-in-one)
```

**Month 7-12 (10+ customers):**
```
Render Flask + Supabase + Vercel: $34/mo (free tier)
→ Add React dashboard (Vercel free tier sufficient)
```

**Month 13+ (50+ customers):**
```
Render Flask + Supabase + Vercel Pro: $54/mo (+$20)
→ Upgrade Vercel for higher bandwidth, team features
```

**Cumulative cost:**
- Year 1: $9×3 + $34×9 = $333
- Year 2: $54×12 = $648

**vs Monolithic:**
- Year 1: $9×3 + $28×9 = $279 (Multi-service +$54 more)
- Year 2: $28×12 = $336 (Multi-service +$312 more)

**Break-even:** When team velocity gain or hiring savings exceed $54-312/year (typically month 7-12 when hiring frontend dev)

---

### Strategy 2: Use Free Tiers Aggressively

**Free tier maximums:**

| Service | Free Tier Limit | Typical Usage (50 customers) | Cost |
|---------|----------------|------------------------------|------|
| **Vercel** | 100 GB bandwidth/mo | 20 GB/mo (dashboard) | $0 |
| **Supabase** | 500 MB DB, 2 GB bandwidth | Use Pro ($25, outgrow free fast) | $25 |
| **Render** | None (used to have free tier) | N/A | $9 |

**Strategy:**
- Keep Vercel on free tier as long as possible (<100 GB bandwidth)
- Upgrade Supabase early (free tier too small for production)
- Render has no free tier (pay $9 minimum)

---

### Strategy 3: Eliminate Services When Not Needed

**Example: Skip React dashboard for first 5 customers**

```
Months 1-6 (0-5 customers):
Render Flask + Supabase: $34/mo
Dashboard: Flask Jinja2 templates (adequate for 5 customers)

Months 7+ (5+ customers):
Render Flask + Supabase + Vercel: $34/mo
Dashboard: React (migrate when customer demand justifies)
```

**Savings:** $0 (Vercel free), but delay React dashboard build effort (60-120 hours) until needed

---

## QRCards-Specific Recommendations

### Current State (November 2025)

**Customers:** 0 paying customers
**Traffic:** <100 QR scans/month (demos)
**Team:** Solo founder (Ivan)
**Dashboard needs:** Minimal (no customer self-service yet)

**Recommendation: Monolithic Flask + SQLite**

**Architecture:**
```
Render Flask ($9/mo):
├─ QR resolution
├─ Simple admin dashboard (Jinja2)
├─ SQLite databases (files)
└─ DAP Processor
```

**Rationale:**
- Fastest migration (already planned in 2.050 PaaS assessment)
- Lowest cost ($9/mo, no database service)
- SQLite adequate for demo traffic
- Focus on customer acquisition, not architecture

**Timeline:** Execute now (Weeks 1-3, 8-16 hours)

---

### First Customer Milestone (Projected: Q1 2026)

**Trigger:** First paying customer OR 1,000 scans/month

**Recommendation: Add Supabase Database**

**Architecture:**
```
Render Flask ($9/mo):
├─ QR resolution
├─ Admin dashboard (still Jinja2)
├─ API endpoints (prepare for future React dashboard)
└─ DAP Processor

Supabase ($25/mo):
├─ PostgreSQL (migrate from SQLite)
├─ Auth (set up, not used yet)
└─ Storage (set up, not used yet)

Total: $34/mo (+$25)
```

**Changes:**
- Migrate SQLite → PostgreSQL (4-8 hours)
- Configure RLS policies (multi-tenant data isolation)
- Keep Flask dashboard (defer React migration)

**Timeline:** Week after first customer pays (4-8 hours migration)

---

### Hiring Frontend Developer Milestone (Projected: Q3 2026)

**Trigger:** 10-20 customers, need customer self-service dashboard

**Recommendation: Split Frontend (React Dashboard)**

**Architecture:**
```
Render Flask ($9/mo):
├─ QR resolution
├─ API endpoints (RESTful JSON)
└─ DAP Processor

Supabase ($25/mo):
├─ PostgreSQL
├─ Auth (NOW used: customer login)
└─ Storage (NOW used: file uploads)

Vercel ($0/mo, free tier):
├─ React dashboard (NEW)
├─ TypeScript (NEW)
└─ Next.js (NEW)

Total: $34/mo (same as Phase 2, but with React dashboard)
```

**Changes:**
- Hire frontend developer (React/TypeScript specialist)
- Build React dashboard (60-120 hours initial build)
- Migrate customers from Flask admin → React self-service
- Deprecate Flask dashboard (keep API only)

**Benefits:**
- Frontend dev works independently (team parallelization)
- Modern dashboard UX (customers can self-serve)
- Independent deployment (dashboard updates don't touch backend)

**Timeline:** When hiring frontend dev (60-120 hours React dashboard build)

---

### Scale Milestone (Projected: 2027+)

**Trigger:** 50-100+ customers, team of 2-5 developers

**Recommendation: Evaluate TypeScript Backend (Optional)**

**Option A: Keep Flask Backend (Recommended)**
```
Render Flask: $9-25/mo (scale as needed)
Supabase: $25-55/mo (scale database)
Vercel: $0-20/mo (scale frontend)
Total: $34-100/mo
```

**Option B: Migrate to Full TypeScript (Evaluate)**
```
Vercel (Next.js): $20-40/mo (frontend + backend)
Supabase: $25-55/mo (database)
Total: $45-95/mo (-$9 Render eliminated)
```

**Decision criteria:**
- If Python ecosystem still needed (DAP Processor): Keep Flask (Option A)
- If team entirely TypeScript: Consider full TypeScript (Option B)
- If costs matter: Option B saves $9/mo (marginal at this revenue scale)

**Timeline:** Year 2+ (reassess when team scaling or costs become significant)

---

## Conclusion

**Multi-service architecture (Flask + Supabase + React) is NOT about technology elegance or saving $3/month on infrastructure.**

**It's about:**
1. **Team parallelization** → Frontend/backend devs work independently
2. **Technology choice freedom** → Python for content, TypeScript for UI
3. **Independent scaling** → Optimize each service separately
4. **Deployment independence** → Update dashboard without backend restart

**For QRCards:**

**Now (0 customers):**
- ✅ Monolithic Flask + SQLite ($9/mo)
- Focus: Customer acquisition, not architecture

**First customer (Q1 2026):**
- ✅ Add Supabase database ($34/mo total)
- Focus: Multi-tenant data isolation, professional infrastructure

**Hiring trigger (Q3 2026, 10-20 customers):**
- ✅ Split frontend (React dashboard, $34/mo total, Vercel free tier)
- Focus: Team parallelization, modern dashboard UX

**Scale (2027+, 50-100+ customers):**
- ⚠️ Evaluate TypeScript backend (optional, marginal savings)
- Focus: Team efficiency, optimize costs at scale

**Cost differential:** Multi-service is +$6-26/month vs monolithic, but pays for itself via:
- Faster hiring (React developers 10x more common than Flask specialists)
- Team velocity (independent deployments, parallel work)
- Better UX (React dashboard > Flask templates)

**Migration trigger:** Hire first frontend developer OR customer dashboard becomes critical (typically 10-50 customers).

**Recommendation confidence:** HIGH (clear economic justification when hiring or dashboard becomes primary product)

---

**Next action:** Execute Phase 1 (Render Flask + SQLite migration, already planned in 2.050 PaaS assessment). Defer multi-service architecture until hiring or dashboard trigger (6-12 months).
