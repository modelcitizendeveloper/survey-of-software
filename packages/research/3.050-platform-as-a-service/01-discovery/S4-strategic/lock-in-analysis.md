# PaaS Lock-In Analysis

**Experiment:** 3.050 Platform-as-a-Service
**Analysis Date:** 2025-10-09
**Focus:** Migration complexity and vendor lock-in assessment

---

## Executive Summary

**Key Finding:** Modern PaaS providers (Render, Railway) have LOW lock-in due to Docker-native architectures. Migration between providers is 1-8 hours, not weeks.

**Strategic Advantage:** Low lock-in = freedom to migrate when acquisition/pricing changes occur.

---

## Lock-In Scoring Methodology

**Lock-In Severity Scale (0-100):**
- **0-25:** VERY LOW - Hours to migrate, standard tech stack
- **26-50:** MODERATE - Days to migrate, some reconfiguration
- **51-75:** HIGH - Weeks to migrate, significant vendor-specific features
- **76-100:** VERY HIGH - Months to migrate, deeply embedded APIs

**Factors Assessed:**
1. Configuration portability (Dockerfile, config files)
2. Platform-specific APIs in use
3. Database export/import ease
4. Environment variable standards
5. Multi-region/edge features (harder to replicate)
6. Add-on/marketplace dependencies

---

## Lock-In Comparison Matrix

| Provider | Lock-In Score | Migration Time | Difficulty Level | Primary Lock-In Source |
|----------|---------------|----------------|------------------|------------------------|
| **Render** | 20/100 | 1-8 hours | LOW | render.yaml (easily replaced) |
| **Railway** | 25/100 | 1-8 hours | LOW | Railway.toml (easily replaced) |
| **PythonAnywhere** | 25/100 | 2-8 hours | LOW | WSGI config (standard) |
| **Fly.io** | 40/100 | 4-16 hours | MODERATE | Edge/multi-region setup, fly.toml |
| **Heroku** | 45/100 | 2-12 hours | MODERATE | Procfile, buildpacks, add-ons |
| **Vercel** | N/A | N/A | N/A | Not Django-suitable |

---

## Provider-by-Provider Lock-In Analysis

### 1. Render - Lock-In Score: 20/100 (VERY LOW)

**Configuration:**
- `render.yaml` - Declarative infrastructure config
- Standard Dockerfile (if used) - Completely portable
- Environment variables - Standard
- Build commands - Shell scripts (portable)

**Database:**
- Managed Postgres/Redis
- Standard dumps available (pg_dump, redis-cli)
- No proprietary formats

**Migration Paths:**
- **To Railway:** 1-2 hours (delete render.yaml, create Railway.toml)
- **To Fly.io:** 2-4 hours (create fly.toml, deploy)
- **To Heroku:** 2-4 hours (create Procfile, adjust buildpack)
- **To DIY VPS:** 4-8 hours (Docker Compose setup)

**Lock-In Elements:**
- render.yaml format (unique, but trivial to replace)
- Private networking (if used, need to reconfigure)
- Render-specific env vars (e.g., `RENDER=true`)

**Mitigation:**
- Use Dockerfile (not Render buildpacks)
- Avoid Render-specific features
- Keep render.yaml simple

**Assessment:** Near-zero lock-in. Render's Docker-native approach makes migration trivial.

---

### 2. Railway - Lock-In Score: 25/100 (VERY LOW)

**Configuration:**
- `Railway.toml` or Nixpacks auto-detection
- Dockerfile support (portable)
- Environment variables - Standard
- Templates (if used, need recreation)

**Database:**
- Managed Postgres/MySQL/Redis/MongoDB
- Standard dumps available
- No proprietary formats

**Migration Paths:**
- **To Render:** 1-2 hours (delete Railway.toml, create render.yaml)
- **To Fly.io:** 2-4 hours (create fly.toml)
- **To Heroku:** 2-4 hours (create Procfile)
- **To DIY VPS:** 4-8 hours (Docker Compose)

**Lock-In Elements:**
- Railway.toml format (unique, but simple)
- Usage-based pricing model (need to recalculate costs elsewhere)
- Private networking (if used)

**Mitigation:**
- Use Dockerfile (not Nixpacks auto-detection)
- Avoid Railway-specific features
- Keep Railway.toml simple

**Assessment:** Minimal lock-in. Railway's approach mirrors Render's portability.

---

### 3. PythonAnywhere - Lock-In Score: 25/100 (VERY LOW)

**Configuration:**
- WSGI config file (standard Python web server interface)
- Virtual environment (standard)
- Scheduled tasks (cron-style, easily replicated)
- Static files (standard WSGI_PATH)

**Database:**
- SQLite (file-based, easy to copy)
- MySQL (standard dumps)
- Postgres (standard dumps, if using external)

**Migration Paths:**
- **To Render (Docker):** 4-8 hours (create Dockerfile, configure)
- **To Railway (Docker):** 4-8 hours (create Dockerfile, configure)
- **To Heroku:** 2-4 hours (create Procfile, WSGI already set up)
- **To DIY VPS:** 4-8 hours (replicate WSGI config)

**Lock-In Elements:**
- PythonAnywhere-specific WSGI path conventions
- Web app reload mechanism (PA-specific, but trivial)
- Free tier database 90-day limit (if used, need to export)

**Mitigation:**
- Use standard WSGI (Gunicorn, uWSGI)
- Keep SQLite or use external database
- Document deployment steps

**Assessment:** Low lock-in. WSGI is industry standard, easy to replicate elsewhere.

---

### 4. Fly.io - Lock-In Score: 40/100 (MODERATE)

**Configuration:**
- `fly.toml` - Fly-specific format
- Dockerfile (portable)
- Fly Machines API (proprietary, if used)
- Multi-region deployment (complex to replicate)

**Database:**
- Fly Postgres (HA cluster setup Fly-specific)
- Standard Postgres underneath (dumps work)
- Multi-region replication (Fly-specific)

**Migration Paths:**
- **To Render/Railway:** 4-8 hours (simplify to single-region, reconfigure)
- **To Heroku:** 6-10 hours (adapt multi-region logic)
- **To DIY VPS:** 8-16 hours (Docker works, but multi-region is complex)
- **To AWS ECS/Fargate:** 12-20 hours (rebuild edge logic on CloudFront/Lambda@Edge)

**Lock-In Elements:**
- **Multi-region deployment** - Fly's core value prop, hard to replicate
- **Anycast IPs** - Fly-specific, not portable
- **Fly Proxy** - Automatic routing (need to rebuild logic)
- **Fly Postgres HA** - Cluster config is Fly-specific

**Mitigation:**
- Keep Dockerfile standard
- Avoid Fly Machines API (use Docker standard)
- Document multi-region logic (if critical, plan for AWS/GCP alternative)

**Assessment:** Moderate lock-in. Docker is portable, but multi-region setup is Fly-specific and complex to replicate.

---

### 5. Heroku - Lock-In Score: 45/100 (MODERATE)

**Configuration:**
- `Procfile` - Heroku-specific (but simple)
- Buildpacks - Heroku/Cloud Native (semi-portable)
- Config vars - Standard environment variables
- Add-ons - Marketplace dependencies (varies)

**Database:**
- Heroku Postgres (standard Postgres, easy dumps)
- Heroku Redis (standard Redis, easy dumps)
- Add-ons (varies by provider)

**Migration Paths:**
- **To Render/Railway:** 2-4 hours (Procfile → Dockerfile/config)
- **To Fly.io:** 4-6 hours (create Dockerfile, fly.toml)
- **To DIY VPS:** 6-12 hours (rebuild Procfile commands in Docker/systemd)
- **To AWS Elastic Beanstalk:** 4-8 hours (similar Procfile concept)

**Lock-In Elements:**
- **Procfile** - Heroku-specific format (simple to convert)
- **Buildpacks** - Cloud Native buildpacks portable, but Heroku-optimized versions less so
- **Add-ons** - Marketplace dependencies (email, monitoring, etc.) need replacement
- **Heroku Postgres/Redis** - Standard, but HA config is Heroku-specific

**Mitigation:**
- Use standard buildpacks (not Heroku-specific)
- Avoid proprietary add-ons (use external SaaS directly)
- Keep Procfile simple (web, worker, release commands)

**Assessment:** Moderate lock-in. Procfile is easy to convert, but add-ons ecosystem creates dependencies.

---

## Migration Effort Comparison

### Quick Migration Matrix (from QRCards' perspective)

**Scenario: Django app with Postgres database**

| From → To | Time | Complexity | Steps |
|-----------|------|------------|-------|
| **PythonAnywhere → Render** | 4-8h | LOW | 1. Create Dockerfile, 2. render.yaml, 3. Deploy, 4. Migrate DB |
| **PythonAnywhere → Railway** | 4-8h | LOW | 1. Create Dockerfile, 2. Railway.toml, 3. Deploy, 4. Migrate DB |
| **Render → Railway** | 1-2h | VERY LOW | 1. Delete render.yaml, 2. Create Railway.toml, 3. Deploy |
| **Railway → Render** | 1-2h | VERY LOW | 1. Delete Railway.toml, 2. Create render.yaml, 3. Deploy |
| **Render → Fly.io** | 2-4h | LOW | 1. Create fly.toml, 2. Deploy (single-region) |
| **Fly.io → Render** | 4-8h | MODERATE | 1. Simplify multi-region, 2. render.yaml, 3. Deploy |
| **Heroku → Render** | 2-4h | LOW | 1. Procfile → Dockerfile, 2. render.yaml, 3. Deploy |
| **Any PaaS → DIY VPS** | 8-16h | MODERATE | 1. Docker Compose, 2. Nginx config, 3. SSL setup, 4. Deploy automation |

**Key Insight:** Modern Docker-native PaaS (Render, Railway) are nearly interchangeable (1-2 hour migration).

---

## Lock-In Mitigation Best Practices

### 1. Use Standard Technologies

**Prefer:**
- Dockerfile over platform-specific buildpacks
- Standard WSGI (Gunicorn) over platform-specific app servers
- Environment variables over platform-specific config
- Standard database dumps over proprietary export formats

**Avoid:**
- Platform-specific APIs (Fly Machines, Render cron syntax)
- Proprietary add-ons (use external SaaS with API keys)
- Custom deployment scripts (keep simple, shell-based)

### 2. Document Deployment Process

**Create migration checklist:**
1. Application dependencies (requirements.txt, Dockerfile)
2. Environment variables (list all, with descriptions)
3. Database schema (migrations, sample data)
4. Static files configuration
5. Background tasks/cron jobs
6. External services (APIs, storage, email)

**Keep updated:** Review quarterly, test annually

### 3. Test Alternative Deployments

**Annual exercise:**
- Deploy to backup provider (Railway if on Render, vice versa)
- Verify everything works
- Document differences/gotchas
- Keep backup config files in repo

**Cost:** 2-4 hours/year
**Benefit:** Ready to migrate immediately if needed

### 4. Avoid Platform-Specific Features

**High Lock-In Features to Avoid:**
- Render Cron (use external cron service or standard Kubernetes cron)
- Fly.io multi-region (start single-region, add later if critical)
- Heroku add-ons (use external SaaS directly)
- Platform-specific databases (prefer managed DB elsewhere)

**Low Lock-In Features Safe to Use:**
- Environment variables
- Standard Dockerfile
- Database dumps
- SSL certificates (all providers offer)

---

## Strategic Recommendations

### For QRCards (Experiment 3.050)

**1. Choose Low Lock-In Provider:**
- Render (20/100) or Railway (25/100) or PythonAnywhere (25/100)
- All have 1-8 hour migration times
- Avoid Fly.io (40/100, edge-specific) unless multi-region needed
- Avoid Heroku (45/100, add-on dependencies)

**2. Build Portably:**
- Use Dockerfile (Render/Railway) or standard WSGI (PythonAnywhere)
- Keep configuration simple (single file, declarative)
- Document all environment variables
- Avoid platform-specific APIs

**3. Maintain Migration Readiness:**
- Keep deployment docs updated
- Test on alternative provider annually
- Budget 4-8 hours for future migration
- Monitor provider for acquisition signals

**4. Plan for Migration by 2030:**
- All VC-backed PaaS will face exit events 2028-2032
- Low lock-in = painless migration
- Next platform: DIY VPS (if scaled) or new VC-backed PaaS

---

## Lock-In vs Features Trade-Off

### The Dilemma

**Lower Lock-In = Less Platform Value**
- Render/Railway: Generic Docker hosting (low lock-in, but minimal differentiation)
- Fly.io: Edge computing magic (higher lock-in, but unique capabilities)

**For QRCards:**
- Simple Django app doesn't need edge computing
- Prefer low lock-in (Render/Railway) over advanced features (Fly.io)
- If QRCards scales globally, THEN consider Fly.io or DIY multi-region

---

## Conclusion

**Modern PaaS has LOW lock-in** compared to historical platforms:
- Render: 20/100 (1-8 hour migration)
- Railway: 25/100 (1-8 hour migration)
- PythonAnywhere: 25/100 (2-8 hour migration)

**Strategic Advantage:**
- Low lock-in = freedom to migrate when providers change
- All providers will change (acquisition, repricing) by 2030
- Migration-ready architecture is ESSENTIAL

**QRCards Strategy:**
- Deploy to Render or PythonAnywhere (lowest lock-in)
- Build with standard Docker or WSGI (no vendor-specific features)
- Plan for 4-8 hour migration when needed (2029-2030)
- Low lock-in turns acquisition risk into minor inconvenience

**Bottom Line:** Lock-in is NOT a dealbreaker. All top choices (Render, Railway, PythonAnywhere) have low lock-in and are easily portable.
