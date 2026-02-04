# Platform-as-a-Service (PaaS) Explainer

**Purpose:** Educational guide for understanding PaaS, when to use it, and key concepts
**Audience:** Developers evaluating hosting options for web applications
**Date:** October 9, 2025

---

## Table of Contents

1. [What is PaaS?](#what-is-paas)
2. [When Do You Need PaaS?](#when-do-you-need-paas)
3. [Key PaaS Concepts](#key-paas-concepts)
4. [PaaS Provider Categories](#paas-provider-categories)
5. [Cost Models](#cost-models)
6. [Migration Considerations](#migration-considerations)
7. [Decision Framework](#decision-framework)

---

## What is PaaS?

### Definition

**Platform-as-a-Service (PaaS)** is a cloud computing model where you deploy your application code and the provider manages all infrastructure (servers, networking, operating systems, scaling, monitoring).

**You provide:** Application code, database schema, configuration
**Provider manages:** Servers, OS patches, load balancing, SSL certificates, backups, monitoring

### IaaS vs PaaS vs BaaS vs SaaS Comparison

| Level | Examples | You Manage | Provider Manages | Use Case |
|-------|----------|------------|------------------|----------|
| **IaaS** (Infrastructure) | AWS EC2, DigitalOcean Droplets | OS, runtime, app, data | Physical servers, networking, virtualization | Full control, custom infrastructure |
| **PaaS** (Platform) | Heroku, Render, Railway | Application code, data | OS, runtime, scaling, monitoring | Deploy custom backend code |
| **BaaS** (Backend) | Supabase, Firebase, Appwrite | Frontend code, security rules | Backend APIs, database, auth, storage | Skip backend coding entirely |
| **SaaS** (Software) | Salesforce, Gmail, Shopify | Data, configuration | Everything (app + infrastructure) | Use existing software, no coding |

**Key distinction:** PaaS is for deploying your custom backend code (Flask, Django, Express). BaaS provides pre-built backend APIs you call from your frontend. See [experiment 3.400](/home/ivanadamin/spawn-solutions/experiments/2.200-backend-as-a-service/) for BaaS provider comparison.

### Core Value Proposition

**PaaS trades cost for time:**
- You pay MORE per compute unit (vs DIY VPS)
- You save 10-40 hours/month on DevOps tasks
- You deploy in hours instead of days/weeks

**Example:**
- DIY VPS (DigitalOcean): $12/month, 8-16 hours initial setup, 5-10 hours/month maintenance
- PaaS (Render): $7-25/month, 1-4 hours initial setup, 1-2 hours/month maintenance
- **Trade-off:** Pay $7-13/month more, save 4-24 hours/month (worth $600-3,600 at $150/hour)

---

## When Do You Need PaaS?

### PaaS is IDEAL For:

**1. Early-Stage MVPs (Speed Over Cost)**
- Need to deploy in hours, not weeks
- No dedicated DevOps engineer
- Time-to-market is critical
- Example: "Launch beta version next week for customer demo"

**2. Solo Developers (No DevOps Expertise)**
- Building product alone or small team
- Don't want to learn infrastructure management
- Focus on product features, not server administration
- Example: "I know Python/JavaScript, not Docker/Kubernetes"

**3. Startups Pre-Series A (Focus on Product)**
- Burning runway, need to ship features fast
- Can't justify DevOps hire yet ($100K-150K/year)
- Hosting cost $50-500/month acceptable
- Example: "We need 3 engineers building features, not managing servers"

**4. Small-Scale Production Apps (10-10,000 users)**
- Predictable traffic patterns
- Hosting budget $10-500/month
- Don't need custom infrastructure (PaaS features sufficient)
- Example: "SaaS product with 100 paying customers, no special requirements"

### PaaS is NOT IDEAL For:

**1. High-Scale Applications (Hosting >$1,000/month)**
- PaaS pricing scales poorly at high traffic
- DIY infrastructure cheaper at scale
- Break-even point: ~$1,000-2,000/month hosting
- Example: "Our Heroku bill is $5K/month, AWS EC2 would be $1,500"

**2. Custom Infrastructure Needs**
- Need specific OS configurations, kernel modules, custom networking
- PaaS constraints don't fit your architecture
- Example: "We need GPU instances for ML training"

**3. Cost-Sensitive Projects (Every Dollar Matters)**
- Hosting budget <$10/month critical
- Can invest time to save money (setup + maintenance)
- Example: "Personal project, can't justify $20/month, will use $5 VPS"

**4. DevOps Team In-House**
- Already have infrastructure expertise
- Managing 10+ services (PaaS cost compounds)
- Example: "We have 3 DevOps engineers, they manage Kubernetes cluster"

### The Break-Even Analysis

**PaaS makes sense when:**
```
(Time Saved × Hourly Rate) > (PaaS Cost - DIY Cost)

Example:
- PaaS: $25/month, saves 10 hours/month
- DIY: $12/month, requires 10 hours/month
- Break-even: (10 hours × $15/hour) = $150 > ($25 - $12 = $13)
- Verdict: PaaS worth it if you value your time at >$1.30/hour
```

**Rule of thumb:** If your time is worth >$20/hour, PaaS almost always wins until you hit $1,000/month hosting.

---

## Key PaaS Concepts

### 1. Auto-Deployment (Git Push to Production)

**Traditional deployment (DIY VPS):**
```bash
ssh user@server
cd /var/www/app
git pull origin main
pip install -r requirements.txt
sudo systemctl restart app
```
Time: 5-10 minutes per deploy

**PaaS deployment:**
```bash
git push origin main
```
Time: Automatic, 30 seconds (platform builds and deploys)

**How it works:**
1. Developer pushes code to GitHub/GitLab
2. PaaS detects push (webhook)
3. Platform pulls code, builds application (Dockerfile or buildpack)
4. Platform runs tests (if configured)
5. Platform deploys new version (zero-downtime rolling update)
6. Platform notifies developer (success/failure)

**Benefit:** Eliminates manual deployment steps, enables continuous deployment (ship 10x/day vs 1x/week)

---

### 2. Buildpacks (Auto-Detect Language/Framework)

**What are buildpacks?**
Magic that auto-detects your language and framework, installs dependencies, configures runtime.

**Example (Python/Flask app):**
```
PaaS detects:
- requirements.txt → "This is Python"
- Flask in requirements → "This is a Flask web app"
- gunicorn in requirements → "Use gunicorn as WSGI server"

PaaS automatically:
- Installs Python 3.11
- Runs pip install -r requirements.txt
- Configures gunicorn with workers
- Exposes PORT environment variable
- Starts application
```

**Buildpack vs Dockerfile:**
- **Buildpack:** Zero config, auto-detect (Heroku, Render, Railway support)
- **Dockerfile:** Explicit config, full control (Render, Railway, Fly.io support)

**When to use buildpacks:** Simple apps, standard frameworks (Flask, Django, Express, Rails)
**When to use Dockerfile:** Custom setup, multi-service apps, reproducibility

---

### 3. Add-Ons (Databases, Caching, Monitoring)

**What are add-ons?**
One-click services integrated into PaaS platform (databases, Redis, email, monitoring).

**Example (Heroku add-ons):**
```bash
# Add PostgreSQL database
heroku addons:create heroku-postgresql:mini

# PaaS automatically:
# - Provisions database
# - Sets DATABASE_URL environment variable
# - Configures backups
# - Integrates monitoring

# Your app just uses:
import os
DATABASE_URL = os.environ['DATABASE_URL']
```

**Modern PaaS add-on examples:**
- **Databases:** PostgreSQL, MySQL, MongoDB, Redis
- **Email:** SendGrid, Mailgun, Postmark
- **Monitoring:** New Relic, Datadog, Sentry
- **Caching:** Redis, Memcached
- **Storage:** AWS S3, Cloudinary (images)

**Add-on pricing:** Typically separate from compute (database $7-50/month, email $20-80/month)

**Lock-in risk:** High if you use proprietary add-ons (Heroku-specific), low if standard services (generic PostgreSQL)

---

### 4. Environments (Staging vs Production)

**What are environments?**
Separate instances of your application for testing (staging) and live users (production).

**Typical setup:**
```
Production: myapp.com (live users)
Staging: staging.myapp.com (testing before deploy)
Development: localhost:3000 (local development)
```

**PaaS environment features:**
- **Separate databases:** Staging DB ≠ Production DB (safe to test destructive operations)
- **Separate config:** Different API keys, feature flags
- **Preview environments:** Per-branch deploy (test PR before merge)
- **Easy promotion:** Deploy staging → production (one command)

**Example (Render preview environments):**
```yaml
# render.yaml
services:
  - type: web
    name: myapp
    env: production
    branch: main

  - type: web
    name: myapp-staging
    env: staging
    branch: develop

# Every pull request gets own preview:
# PR #123 → myapp-pr-123.onrender.com
```

**Benefit:** Test changes safely before production, catch bugs before users see them

---

### 5. Scaling (Vertical vs Horizontal)

**Vertical Scaling (Bigger Servers):**
```
1 server: 512MB RAM, 1 CPU → $7/month
Upgrade: 1GB RAM, 2 CPU → $14/month
Upgrade: 2GB RAM, 4 CPU → $25/month
```
- Simple (one server)
- Limited (can't scale beyond largest instance)
- Single point of failure

**Horizontal Scaling (More Servers):**
```
1 server: 512MB RAM, 1 CPU → $7/month
Scale: 2 servers (load balanced) → $14/month
Scale: 5 servers (load balanced) → $35/month
```
- Unlimited scale (add more servers)
- High availability (one server fails, others handle traffic)
- More complex (load balancing, session management)

**PaaS auto-scaling:**
```yaml
# Render auto-scaling config
minInstances: 1   # Always 1 server running
maxInstances: 10  # Scale up to 10 if traffic spikes
targetCPU: 70%    # Add server when CPU >70%
```

**Cost:** Auto-scaling can surprise you ($7/month → $70/month during traffic spike)

**Best practice:** Start with vertical scaling (simpler), add horizontal scaling when needed (>10,000 concurrent users)

---

## PaaS Provider Categories

### 1. Python-Native PaaS

**Example:** PythonAnywhere

**Deployment Model:**
- Upload Python files (FTP/Git/web interface)
- Edit WSGI config (Python code)
- Click "Reload" button
- No Docker, no buildpacks, pure Python

**Pros:**
- Zero learning curve for Python developers
- 15-minute first deployment
- No DevOps knowledge required
- Python ecosystem deep integration (virtualenv, pip, popular frameworks)

**Cons:**
- Limited to Python only (can't add Node.js service)
- Can't scale beyond single monolith
- No modern DevOps practices (CI/CD integration weaker)
- Viewed as "educational" not "production"

**Best for:** Python beginners, solo developers, simple Flask/Django apps, 0-50 users

**Lock-in:** Low (standard WSGI, easy to migrate to any WSGI host)

---

### 2. General Buildpack PaaS

**Examples:** Heroku, Render, Railway, DigitalOcean App Platform

**Deployment Model:**
```bash
# Detect language from files:
package.json → Node.js buildpack
requirements.txt → Python buildpack
Gemfile → Ruby buildpack

# Auto-install dependencies
# Auto-configure runtime
# Auto-start application
```

**Pros:**
- Multi-language support (Python, Node, Ruby, Go, Java, PHP)
- Zero config for standard frameworks
- Large ecosystem (Heroku has 200+ add-ons)
- Modern DevOps (CI/CD, preview environments, rollbacks)

**Cons:**
- Less flexible than Docker (constrained by buildpack)
- Learning curve (environment variables, platform-specific config)
- Cost scales poorly at high traffic

**Best for:** Startups, small teams, standard web frameworks, 10-10,000 users

**Lock-in:** Moderate (buildpacks somewhat portable, but platform-specific config)

---

### 3. Docker-Native PaaS

**Examples:** Fly.io, Render, Railway, Google Cloud Run

**Deployment Model:**
```dockerfile
# Dockerfile (you write this)
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app"]
```

**Pros:**
- Full control (define exact runtime, dependencies)
- Dev/prod parity (same Docker image locally and production)
- Language agnostic (run anything that fits in a container)
- Industry standard (transferable to AWS ECS, Kubernetes later)
- Low lock-in (Dockerfile portable to any Docker host)

**Cons:**
- Must learn Docker (3-5 hour learning curve)
- More complex initially (write Dockerfile, understand layers)
- Overkill for simple apps

**Best for:** Teams with Docker experience, multi-service apps, need portability, 100-100,000+ users

**Lock-in:** Very low (Docker is universal, 4-8 hour migration between providers)

---

### 4. Serverless PaaS

**Examples:** Vercel, Cloudflare Workers, AWS Lambda, Netlify Functions

**Deployment Model:**
```javascript
// pages/api/hello.js (Vercel serverless function)
export default function handler(req, res) {
  res.status(200).json({ message: 'Hello World' })
}

// Deployed automatically, scales to zero, pay per request
```

**Pros:**
- Pay-per-request (can be $0/month if no traffic)
- Instant global distribution (edge computing)
- Auto-scaling (0 to millions of requests)
- No server management (truly zero infrastructure)

**Cons:**
- NOT suitable for traditional web frameworks (Flask, Django, Rails)
- Designed for stateless functions (no persistent connections)
- Cold start latency (100-1000ms if function not warm)
- Vendor lock-in (serverless functions platform-specific)

**Best for:** Jamstack sites (static + API functions), microservices, APIs, webhooks

**NOT for:** Flask/Django apps (use Docker PaaS instead)

---

## Cost Models

### 1. Fixed Tiers (Predictable Monthly Cost)

**Example: PythonAnywhere**
```
Beginner: $5/month (1 web app, 1GB storage, 512MB RAM)
Hacker: $12/month (2 web apps, 10GB storage, 1GB RAM)
Web Dev: $25/month (3 web apps, 20GB storage, 3GB RAM)
```

**Pros:**
- Predictable billing (always $5/month, never surprise)
- Simple to budget
- No overage charges

**Cons:**
- Pay for capacity even if unused (low traffic = overpaying)
- Hit ceiling (need next tier, sudden 2-3x cost jump)
- Inflexible (can't fine-tune resources)

**Best for:** Predictable traffic, budget-conscious, small scale

---

### 2. Usage-Based (Pay for What You Use)

**Example: Railway**
```
Included: $5 credit/month (starter plan)
Usage:
- Compute: $0.000463/GB-hour RAM
- Egress: $0.10/GB bandwidth
- Storage: $0.25/GB/month

Example monthly bill:
- 512MB RAM × 720 hours = $0.17
- 10GB bandwidth = $1.00
- 1GB storage = $0.25
Total: $1.42/month (under $5 credit)
```

**Pros:**
- Pay exactly for what you use (low traffic = low cost)
- Flexible (scales with demand)
- No wasted capacity

**Cons:**
- Unpredictable billing (traffic spike = surprise $100 bill)
- Complex to estimate (need to calculate RAM-hours × bandwidth)
- Can forget about low-usage projects (still accrues charges)

**Best for:** Variable traffic, want flexibility, monitoring budget closely

---

### 3. Hybrid (Base Fee + Overages)

**Example: Render**
```
Starter: $7/month base
Includes: 512MB RAM, 0.5 CPU, 100GB bandwidth

Overages:
- Extra RAM: $7/GB/month
- Extra bandwidth: $0.10/GB
- Extra CPU: $7/CPU/month

Example:
- Starter plan: $7/month (under limits)
- Traffic spike (150GB): $7 + (50GB × $0.10) = $12/month
- Need more RAM (1GB): $7 + $7 = $14/month
```

**Pros:**
- Predictable base cost ($7/month minimum)
- Flexible for spikes (don't hit hard limit)
- Clear upgrade path (know cost before exceeding)

**Cons:**
- Can accumulate overages (small charges add up)
- Need to monitor usage (avoid surprise bills)

**Best for:** Growing apps, want safety net, predictable baseline

---

### Cost Comparison Example (Small Flask App)

| Provider | Model | Base Cost | 100GB Traffic | 1GB RAM | Total |
|----------|-------|-----------|---------------|---------|-------|
| **PythonAnywhere** | Fixed | $5/month | Included | 512MB included | **$5/month** |
| **Render** | Hybrid | $7/month | Included | 512MB included | **$7/month** |
| **Railway** | Usage | $5 credit | $10 ($0.10/GB) | $0.17 | **$5/month** (credit covers) |
| **Heroku** | Fixed | $5/dyno + $5/db | Included | 512MB dyno | **$10/month** |
| **Fly.io** | Usage | $0 base | $0 (first 160GB free) | $1.94 (shared CPU) | **$2/month** |

**At 1,000GB traffic (higher scale):**
- PythonAnywhere: $12/month (upgrade tier)
- Render: $7 + $90 overage = $97/month
- Railway: $100/month (bandwidth charges)
- Fly.io: $2 + $84 bandwidth = $86/month

**Insight:** Fixed tiers win at very low scale, usage-based wins at moderate scale, DIY VPS wins at high scale ($1K/month+).

---

## Migration Considerations

### 1. Lock-In Risk (How Hard to Migrate?)

**Lock-In Levels:**

**Very Low (20-25/100): Docker-Native PaaS**
- Render, Railway (Dockerfile portable)
- Migration time: 4-8 hours
- Just deploy Dockerfile to new provider
- Example: Render → Railway migration in one afternoon

**Low (25-40/100): Standard PaaS**
- PythonAnywhere (standard WSGI), DigitalOcean (buildpacks)
- Migration time: 4-12 hours
- Need to adapt to new provider's config format
- Example: PythonAnywhere → Render (write Dockerfile, 8 hours)

**Moderate (40-60/100): Proprietary Features**
- Heroku (buildpacks + add-ons), Fly.io (edge-specific)
- Migration time: 16-40 hours
- Replace add-ons with equivalents, rewrite platform-specific code
- Example: Heroku → Render (remove add-on dependencies, 2-3 days)

**High (60-100/100): Deep Platform Integration**
- Firebase (Firestore), AWS Amplify (vendor SDKs)
- Migration time: 80-300 hours
- Rewrite database layer, replace proprietary APIs
- Example: Firebase → PostgreSQL (complete rewrite, 2-4 weeks)

**Recommendation:** Choose Docker-native PaaS (Render, Railway) for lowest lock-in. Avoid proprietary features (Heroku add-ons, Firebase SDKs) unless absolutely necessary.

---

### 2. Migration Timeline (How Long to Switch?)

**Typical migration scenarios:**

**Docker PaaS → Docker PaaS (Low Lock-In):**
```
1. Create account on new provider (5 minutes)
2. Connect GitHub repo (5 minutes)
3. Deploy Dockerfile (10 minutes build)
4. Migrate database (export/import, 1-2 hours)
5. Update DNS (5 minutes config, 24-48 hours propagation)
6. Test thoroughly (2-4 hours)

Total: 4-8 hours (one afternoon)
```

**Python-Native → Docker PaaS (Learning Curve):**
```
1. Learn Docker basics (3-5 hours tutorials)
2. Write Dockerfile for Flask app (1-2 hours)
3. Test locally with Docker (1 hour)
4. Deploy to new PaaS (4-8 hours, as above)

Total: 8-16 hours (one weekend)
```

**Buildpack PaaS → Different Buildpack (Adaptation):**
```
1. Understand new provider's config (1-2 hours docs)
2. Convert Heroku Procfile → Render render.yaml (1 hour)
3. Replace add-ons (find equivalents, 4-8 hours)
4. Deploy and debug (4-8 hours)

Total: 10-20 hours (1-2 weekends)
```

**Recommendation:** Budget 1-2 weekends for PaaS migration. Low lock-in providers (Docker-native) can migrate in single afternoon.

---

### 3. When to Migrate (Triggers)

**Forced Migration (Act Immediately):**
- Provider acquired, pricing increased 3-5x
- Service shutdown announced (12-24 month timeline)
- Major outages (15+ hours, losing customer trust)
- Free tier eliminated (if you rely on it)

**Strategic Migration (Plan 3-6 Months):**
- Hosting cost >$1,000/month (DIY VPS cheaper)
- Need features current provider doesn't offer (e.g., edge computing)
- Provider innovation frozen 12+ months (maintenance mode)
- Acquisition announced (prepare for future repricing)

**Opportunistic Migration (Optional, Low Priority):**
- Better pricing on new provider ($10-50/month savings)
- Prefer new provider's DX (nicer dashboard, better docs)
- Learning new technology (Docker, Kubernetes)

**Don't Migrate If:**
- Current provider working well (don't fix what isn't broken)
- Migration cost (time) > 1-2 years of savings
- Team comfortable with current setup (familiarity has value)

---

## Decision Framework

### Step 1: Identify Your Constraints

**Budget:**
- <$10/month → Free tier or cheap VPS (DigitalOcean $6)
- $10-100/month → PaaS sweet spot (Render, Railway, PythonAnywhere)
- $100-1,000/month → Premium PaaS or managed services
- >$1,000/month → DIY infrastructure (AWS, Kubernetes)

**Time:**
- Need to deploy this week → PaaS (Render, PythonAnywhere)
- Have 2-4 weeks → DIY VPS acceptable
- Have DevOps team → Build custom infrastructure

**Expertise:**
- Know Python/JavaScript only → PythonAnywhere, Heroku, Render buildpacks
- Know Docker → Render, Railway, Fly.io (Docker-native)
- Know Kubernetes → Self-host or use managed Kubernetes (GKE, EKS)

**Scale:**
- 0-100 users → Any PaaS works
- 100-10,000 users → Mid-tier PaaS (Render, Railway, Fly.io)
- 10,000-100,000 users → High-tier PaaS or DIY
- >100,000 users → Custom infrastructure (PaaS too expensive)

---

### Step 2: Match Provider to Use Case

**Solo Python Developer (Simple Flask/Django App):**
→ **PythonAnywhere** ($5/month) or **Render** ($7/month)
- Why: Lowest learning curve, deploy in hours
- When to migrate: Scaling >50 users, need Docker

**Startup Team (Multi-Service App):**
→ **Railway** ($15-30/month) or **Render** ($20-50/month)
- Why: Modern DX, Docker-native, team-friendly
- When to migrate: Hosting >$500/month (move to AWS)

**High-Performance App (Global Users):**
→ **Fly.io** ($30-100/month)
- Why: Edge computing, 34ms latency, multi-region
- When to migrate: Hosting >$1K/month (DIY with Cloudflare)

**Jamstack Site (Static + API):**
→ **Vercel** ($0-20/month) or **Netlify** ($0-19/month)
- Why: Optimized for static sites, serverless functions, CDN included
- When to migrate: Need traditional backend (not serverless)

**Learning/Portfolio:**
→ **Vercel** free tier or **Render** free tier
- Why: Generous free tier, portfolio-ready URLs
- When to migrate: Going to production (paid tier)

---

### Step 3: Evaluate Lock-In

**Questions to ask:**
1. Does this provider use standard tech? (Docker, PostgreSQL, Redis)
2. Can I migrate in <8 hours? (Render/Railway yes, Firebase no)
3. Am I using proprietary features? (Heroku add-ons, AWS-specific services)
4. Is my Dockerfile portable? (if using Docker)

**Green flags (low lock-in):**
- Docker-native deployment
- Standard PostgreSQL (not proprietary database)
- Environment variables for config (not platform-specific SDK)
- Open source frameworks (Flask, Express, Rails)

**Red flags (high lock-in):**
- Proprietary database (Firestore, DynamoDB without abstraction)
- Platform-specific APIs (Heroku add-ons, AWS SDKs everywhere)
- Vendor SDK deeply integrated (Firebase, Supabase client in every file)
- No Dockerfile (buildpack-only, hard to replicate elsewhere)

---

### Step 4: Plan for Impermanence

**Reality:** No PaaS provider is permanent.
- VC-backed → 5-7 year exit → repricing
- Acquired → 7-15 years → extraction/divestiture
- Market changes → free tiers eliminated, pricing 2-5x

**Strategy:**
1. **Build portably** (use Docker, standard databases, avoid proprietary features)
2. **Monitor quarterly** (watch for funding, pricing changes, acquisition rumors)
3. **Budget for migration** (1-2 weekends every 5-7 years)
4. **Accept reality** (you WILL migrate eventually, make it painless)

**Timeline expectation:**
- 2025-2029: Deploy on Render/Railway (safe window)
- 2029-2032: Likely acquisition/repricing (migration needed)
- 2032-2035: Second provider or DIY (if scaled)

---

## Summary: PaaS Decision Checklist

**Use PaaS if:**
- [ ] Deploying MVP or early-stage product
- [ ] Team <5 people, no dedicated DevOps
- [ ] Hosting budget $10-500/month acceptable
- [ ] Time-to-market critical (ship features > save infrastructure cost)
- [ ] Standard web framework (Flask, Django, Express, Rails)

**Use DIY VPS if:**
- [ ] Hosting cost >$1,000/month (economics favor DIY)
- [ ] Have DevOps expertise in-house
- [ ] Need custom infrastructure (PaaS constraints too limiting)
- [ ] Budget <$10/month critical (personal project, tight margins)

**Provider selection:**
- **Beginner:** PythonAnywhere (Python-only), Vercel (Jamstack)
- **Standard:** Render or Railway (Docker-native, low lock-in)
- **Performance:** Fly.io (edge computing, global)
- **Enterprise:** Heroku (mature ecosystem, expensive)

**Lock-in mitigation:**
- Use Docker (portable between providers)
- Avoid proprietary features (add-ons, vendor SDKs)
- Standard databases (PostgreSQL, Redis, not Firestore)
- Test migration annually (keep migration skills fresh)

**Long-term strategy:**
- Accept impermanence (no "forever" provider)
- Build portably (Docker, standard tech)
- Monitor provider health (funding, pricing, acquisition signals)
- Migrate painlessly (4-8 hours with low lock-in)

---

**Next Steps:**
1. Identify your constraints (budget, time, expertise, scale)
2. Match provider to use case (see Step 2)
3. Evaluate lock-in (see Step 3)
4. Deploy and monitor quarterly (see Step 4)

**Remember:** PaaS is a tool, not a religion. Use it when it makes sense, migrate when it doesn't. The best PaaS is the one that lets you ship features fast while keeping migration painless when circumstances change.
