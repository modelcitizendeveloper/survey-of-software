# PaaS Provider Feature Matrix

**Experiment:** 3.050 Platform-as-a-Service
**Stage:** S2 Comprehensive Discovery
**Date:** 2025-10-09

---

## Feature Comparison Overview

| Feature | PythonAnywhere | Heroku | Render | Railway | Fly.io | DigitalOcean | Vercel | Cloud Run |
|---------|----------------|--------|--------|---------|--------|--------------|--------|-----------|
| **Auto-Scaling** | NO | YES (Perf) | YES (Std+) | NO | NO | YES (Pro+) | AUTO | YES |
| **Custom Domains** | Paid only | YES | YES (all) | YES | YES | YES | YES | YES |
| **Free SSL** | YES | YES | YES | YES | YES | YES | YES | YES |
| **Auto-Deploy (Git)** | NO | YES | YES | YES | CLI | YES | YES | CLI |
| **Docker Support** | NO | YES | YES | YES | REQUIRED | YES | NO | REQUIRED |
| **Database Included** | MySQL | Add-on | Add-on | Built-in | DIY | Add-on | NO | Cloud SQL |
| **Background Workers** | YES | YES | YES | YES | YES | YES | NO | YES |
| **Regions** | 1 (US East) | 5 | 4 | 3 | 30+ | 12 | 20+ | 40+ |
| **Free Tier** | YES* | NO | YES* | Trial | NO | Static | YES* | YES |
| **Monitoring/Logs** | Basic | Good | Good | Excellent | Basic | Good | Basic | Excellent |
| **CI/CD Integration** | NO | Excellent | Good | Good | CLI | Good | Excellent | Good |

*Free tier limitations apply (see pricing matrix)

---

## Detailed Feature Breakdown

### 1. Auto-Scaling

| Provider | Auto-Scaling Support | Details |
|----------|---------------------|---------|
| **PythonAnywhere** | NO | Single worker per app, must manually upgrade tiers |
| **Heroku** | YES (Performance dynos) | Horizontal scaling based on metrics, NOT on Eco/Basic |
| **Render** | YES (Standard+) | Horizontal auto-scaling, configure min/max instances |
| **Railway** | NO | Manual resource allocation, no auto-scale |
| **Fly.io** | Partial | Auto-start/stop machines, but not load-based autoscaling |
| **DigitalOcean** | YES (Professional+) | 1-10 containers, manual config |
| **Vercel** | AUTOMATIC | Serverless - scales automatically |
| **Google Cloud Run** | AUTOMATIC | Best auto-scaling: 0→1000 instances instantly |

**Winners:** Google Cloud Run, Vercel (automatic), Heroku Performance (mature)
**Losers:** PythonAnywhere, Railway (none)

---

### 2. Custom Domains & SSL

| Provider | Custom Domains | Free SSL | Free Tier Domains? |
|----------|----------------|----------|-------------------|
| **PythonAnywhere** | Unlimited (paid) | YES | NO (paid only) |
| **Heroku** | Unlimited | YES | N/A (no free tier) |
| **Render** | Unlimited | YES | YES (even free tier!) |
| **Railway** | Unlimited | YES | YES |
| **Fly.io** | Unlimited | YES | N/A (no free tier) |
| **DigitalOcean** | Unlimited | YES | Static only |
| **Vercel** | Unlimited | YES | YES |
| **Google Cloud Run** | Unlimited | YES | YES |

**Winner:** Render (custom domains + SSL on free tier)
**Loser:** PythonAnywhere (paid plans only for custom domains)

---

### 3. Deployment Methods

| Provider | Git Auto-Deploy | Docker | Buildpacks | CLI | UI Deployment |
|----------|-----------------|--------|------------|-----|---------------|
| **PythonAnywhere** | NO (manual) | NO | NO | NO | YES (web UI) |
| **Heroku** | YES (GitHub) | YES | YES | YES | YES |
| **Render** | YES (GitHub/GitLab) | YES | YES | NO | YES |
| **Railway** | YES (GitHub/GitLab) | YES | Nixpacks/Railpack | YES | YES |
| **Fly.io** | CLI-based | REQUIRED | NO | YES | NO (CLI only) |
| **DigitalOcean** | YES (GitHub/GitLab) | YES | YES | YES | YES |
| **Vercel** | YES (GitHub/GitLab) | NO | NO | YES | YES |
| **Google Cloud Run** | Via Cloud Build | REQUIRED | NO | YES | YES |

**Simplest:** PythonAnywhere (web UI), Render (GitHub auto-deploy)
**Most Flexible:** Heroku, Railway (multiple methods)
**Most Complex:** Fly.io, Cloud Run (Docker required)

---

### 4. Database Support

| Provider | Database Options | Managed? | Included in Base Price? |
|----------|------------------|----------|------------------------|
| **PythonAnywhere** | MySQL (Postgres +$7) | YES | MySQL YES (in quota) |
| **Heroku** | Postgres, Redis (add-ons) | YES | NO (from $5/month) |
| **Render** | Postgres, Redis | YES | NO (from $7/month) |
| **Railway** | Postgres, MySQL, Redis, MongoDB | YES | NO (usage-based) |
| **Fly.io** | Run-it-yourself Postgres | SEMI | NO (DIY setup) |
| **DigitalOcean** | Postgres, MySQL, Redis, MongoDB | YES | NO (from $7/month) |
| **Vercel** | NO (external only) | N/A | N/A |
| **Google Cloud Run** | Cloud SQL (Postgres/MySQL) | YES | NO (from $7/month) |

**Best Database Experience:** Railway (one-click), Heroku (mature add-ons)
**Simplest for Small Apps:** PythonAnywhere (MySQL included)
**DIY:** Fly.io (run Postgres as app)
**No Database:** Vercel (must use external service)

---

### 5. Environment Management

| Provider | Staging/Production | Preview Environments | Secrets Management |
|----------|-------------------|---------------------|-------------------|
| **PythonAnywhere** | Manual (separate apps) | NO | Web UI env vars |
| **Heroku** | Pipelines (excellent) | Review Apps | Config Vars |
| **Render** | Manual | PR Previews | Environment Vars |
| **Railway** | Manual (separate projects) | NO | Environment Vars |
| **Fly.io** | Manual | NO | Secrets CLI |
| **DigitalOcean** | Manual | NO | Environment Vars |
| **Vercel** | Built-in | PR Previews | Environment Vars |
| **Google Cloud Run** | Revisions (excellent) | Manual | Secret Manager |

**Best:** Heroku (Pipelines + Review Apps), Google Cloud Run (revisions)
**Good:** Render (PR previews), Vercel (PR previews)
**Basic:** PythonAnywhere, Railway, Fly.io

---

### 6. Monitoring & Logs

| Provider | Log Access | Metrics/Monitoring | Alerting | Log Retention |
|----------|------------|-------------------|----------|---------------|
| **PythonAnywhere** | Web UI | NO metrics | NO | Limited |
| **Heroku** | CLI streaming | Heroku Metrics | Via add-ons | 1,500 lines |
| **Render** | Web UI/CLI | Basic metrics | Email | Varies by plan |
| **Railway** | Web UI (beautiful) | Excellent dashboard | NO | Good |
| **Fly.io** | CLI | Basic | NO | Limited |
| **DigitalOcean** | Web UI | Basic metrics | Email | Good |
| **Vercel** | Web UI | Analytics (paid) | Email | Good |
| **Google Cloud Run** | Cloud Logging | Cloud Monitoring | Cloud Alerting | Excellent |

**Best:** Google Cloud Run (enterprise-grade), Railway (beautiful UI)
**Good:** Heroku (mature), Render, DigitalOcean
**Basic:** PythonAnywhere, Fly.io

---

### 7. CI/CD Integration

| Provider | GitHub Actions | GitLab CI | Built-In Pipeline | Automated Tests |
|----------|----------------|-----------|-------------------|----------------|
| **PythonAnywhere** | NO | NO | NO | NO |
| **Heroku** | YES (native) | YES | Heroku CI | YES |
| **Render** | YES | YES | Auto-deploy | Via external |
| **Railway** | YES (CLI) | YES (CLI) | Auto-deploy | Via external |
| **Fly.io** | YES (action) | YES | NO | Via external |
| **DigitalOcean** | YES | YES | Auto-deploy | Via external |
| **Vercel** | YES (native) | YES | Built-in | YES |
| **Google Cloud Run** | YES (action) | YES | Cloud Build | YES |

**Best:** Heroku (Heroku CI), Vercel (built-in), Cloud Run (Cloud Build)
**Good:** Render, Railway, DigitalOcean (auto-deploy)
**None:** PythonAnywhere (manual deployment only)

---

### 8. Regions & Global Deployment

| Provider | Number of Regions | Edge/Global? | Multi-Region Support |
|----------|------------------|--------------|---------------------|
| **PythonAnywhere** | 1 (US East) | NO | NO |
| **Heroku** | 5 (US, EU, Asia) | NO | Choose one |
| **Render** | 4 (US, EU, Singapore) | NO | Choose one |
| **Railway** | 3 (US West, US East, EU) | NO | Choose one |
| **Fly.io** | 30+ (worldwide) | YES (Anycast) | YES (multi-region apps) |
| **DigitalOcean** | 12 (global) | NO | Choose one |
| **Vercel** | 20+ (Edge Network) | YES | Automatic global |
| **Google Cloud Run** | 40+ (GCP regions) | NO | Choose one |

**Best Global:** Fly.io (30+ regions, Anycast), Vercel (Edge)
**Good Coverage:** Cloud Run (40+ regions), DigitalOcean (12)
**Limited:** PythonAnywhere (1), Railway (3), Render (4)

---

### 9. Background Workers & Cron Jobs

| Provider | Background Workers | Cron/Scheduled Tasks | Long-Running Processes |
|----------|-------------------|---------------------|----------------------|
| **PythonAnywhere** | Always-on tasks (paid) | Scheduled tasks (1/day free) | YES (with CPU limits) |
| **Heroku** | Worker dynos (paid) | Scheduler add-on | YES |
| **Render** | Background workers | Cron jobs | YES |
| **Railway** | Via Procfile | Cron service | YES |
| **Fly.io** | Full VMs (any process) | Via external | YES |
| **DigitalOcean** | Workers | Via external | YES |
| **Vercel** | NO (serverless only) | Via external | NO (10-sec limit) |
| **Google Cloud Run** | Cloud Run Jobs | Cloud Scheduler | YES (up to 60 min) |

**Best:** Fly.io (full VM control), Cloud Run (Cloud Run Jobs)
**Good:** Heroku, Render, Railway (native support)
**Limited:** Vercel (serverless constraints), PythonAnywhere (CPU limits)

---

### 10. Python/Flask Compatibility

| Provider | Flask Support | Buildpack/Auto-Detect | WSGI Server | Complexity |
|----------|---------------|----------------------|-------------|------------|
| **PythonAnywhere** | EXCELLENT (native) | Web UI config | Built-in | SIMPLE |
| **Heroku** | EXCELLENT | YES (buildpack) | Gunicorn | MEDIUM |
| **Render** | EXCELLENT | YES (buildpack) | Gunicorn | MEDIUM |
| **Railway** | EXCELLENT | YES (Railpack) | Gunicorn | MEDIUM |
| **Fly.io** | GOOD | NO (Docker) | Gunicorn | COMPLEX |
| **DigitalOcean** | GOOD | YES (buildpack) | Gunicorn | MEDIUM |
| **Vercel** | LIMITED (functions only) | NO | N/A | N/A |
| **Google Cloud Run** | GOOD | NO (Docker) | Gunicorn | COMPLEX |

**Best for Flask:** PythonAnywhere (simplest), Heroku (mature), Render (modern)
**Not for Flask:** Vercel (serverless functions only)
**Requires Docker:** Fly.io, Cloud Run

---

## Feature Score Summary (1-5 scale)

| Provider | Ease of Use | Flask Support | Auto-Scaling | Global Reach | DevOps Features | Total |
|----------|-------------|---------------|--------------|--------------|----------------|-------|
| **PythonAnywhere** | 5 | 5 | 1 | 1 | 1 | 13 |
| **Heroku** | 4 | 5 | 4 | 3 | 5 | 21 |
| **Render** | 4 | 5 | 3 | 2 | 4 | 18 |
| **Railway** | 5 | 5 | 1 | 2 | 3 | 16 |
| **Fly.io** | 2 | 3 | 2 | 5 | 3 | 15 |
| **DigitalOcean** | 4 | 4 | 3 | 3 | 3 | 17 |
| **Vercel** | 5 | 1 | 5 | 5 | 4 | 20 |
| **Google Cloud Run** | 2 | 3 | 5 | 4 | 5 | 19 |

**Notes:**
- Vercel scores high but is NOT for Flask (deducted in Flask Support)
- PythonAnywhere: Simple but limited features
- Heroku: Best overall feature set (but expensive)
- Railway: Great DX but missing auto-scaling
- Fly.io: Global but complex

---

## Feature Recommendations by Use Case

### For Flask Apps (Traditional Web Apps)
**Best Features:** Heroku, Render, Railway
**Avoid:** Vercel (incompatible), Fly.io/Cloud Run (Docker complexity)

### For Global Applications
**Best Features:** Fly.io (30+ regions), Vercel (Edge)
**Avoid:** PythonAnywhere (1 region)

### For Beginners
**Best Features:** PythonAnywhere (simplest), Railway (beautiful UI)
**Avoid:** Fly.io, Cloud Run (steep learning curve)

### For Production/Enterprise
**Best Features:** Heroku (mature), Cloud Run (enterprise), Render (modern)
**Avoid:** PythonAnywhere (limited scaling), Railway (no auto-scale)

### For Cost Optimization
**Best Features:** Cloud Run (pay-per-request), PythonAnywhere (cheapest fixed)
**Avoid:** Heroku (expensive), Vercel (high overages)

---

## Missing Features Comparison

| Feature | Providers WITHOUT |
|---------|------------------|
| **Auto-Scaling** | PythonAnywhere, Railway, Fly.io |
| **Git Auto-Deploy** | PythonAnywhere |
| **Docker Support** | PythonAnywhere, Vercel |
| **Free Tier** | Heroku, Fly.io (new users) |
| **Multi-Region** | PythonAnywhere (only 1 region) |
| **Built-in Database** | Vercel |
| **Traditional Flask Apps** | Vercel (serverless only) |

---

## Conclusion

**Feature-Rich Leaders:** Heroku, Cloud Run (enterprise features)
**Modern Sweet Spot:** Render, Railway (good features, modern DX)
**Simplicity Winner:** PythonAnywhere (but feature-limited)
**Global Specialist:** Fly.io (30+ regions)
**Wrong Tool:** Vercel (not for Flask)

**For QRCards:**
- **Current needs:** Simple deployment, low cost → PythonAnywhere good fit
- **Growth needs:** Auto-deploy, scaling → Render/Railway better
- **Global expansion:** Fly.io (but complex)
