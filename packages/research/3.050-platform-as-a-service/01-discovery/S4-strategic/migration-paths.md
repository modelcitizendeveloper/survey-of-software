# PaaS Migration Paths: Effort Estimates

**Experiment:** 3.050 Platform-as-a-Service
**Analysis Date:** 2025-10-09
**Focus:** Specific migration scenarios from PythonAnywhere

---

## Executive Summary

**Key Finding:** PythonAnywhere → modern PaaS (Render/Railway) migration is 4-8 hours. Low lock-in enables painless provider switching when acquisition risk materializes.

**Strategic Implication:** QRCards can start on ANY low lock-in provider (PythonAnywhere, Render, Railway) and migrate easily when circumstances change.

---

## Migration Scenarios

### Scenario 1: PythonAnywhere → Render

**Context:** PythonAnywhere acquired by Anaconda (2022), potential repricing 2029-2032 as Anaconda exits. Migrate to Render proactively.

**Estimated Effort: 4-8 hours**

#### Steps

**1. Prepare Dockerfile (2-3 hours)**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run with Gunicorn
CMD gunicorn qrcards.wsgi:application --bind 0.0.0.0:$PORT
```

**2. Create render.yaml (30 minutes)**
```yaml
services:
  - type: web
    name: qrcards
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput
    startCommand: gunicorn qrcards.wsgi:application
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: qrcards-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DJANGO_SETTINGS_MODULE
        value: qrcards.settings.production

databases:
  - name: qrcards-db
    plan: starter
```

**3. Export Database from PythonAnywhere (30 minutes)**
- SQLite: Download file directly via Files tab
- MySQL: `mysqldump -u username -p database_name > dump.sql`
- Postgres: `pg_dump database_name > dump.sql`

**4. Create Render Account & Deploy (1 hour)**
- Sign up for Render
- Connect GitHub repository
- Deploy application (automatic build)
- Wait for initial deployment (5-10 minutes)

**5. Import Database to Render Postgres (30 minutes)**
- Provision Render Postgres database
- Connect via `psql` or DataGrip
- If SQLite → Postgres: Use Django `dumpdata`/`loaddata` OR manual migration
- If MySQL/Postgres → Postgres: Use `pg_restore` or SQL import

**6. Configure Environment Variables (30 minutes)**
- Copy all env vars from PythonAnywhere
- Set `SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`
- Configure email, storage (S3, etc.) if used

**7. Test & Verify (1-2 hours)**
- Run Django migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Test admin panel
- Test key user flows (QR code generation, etc.)
- Verify static files serving
- Check background tasks (if any)

**8. Update DNS (15 minutes)**
- Point domain from PythonAnywhere to Render
- Wait for DNS propagation (5-60 minutes)
- Test on new domain

**Total Time: 4-8 hours** (depends on database complexity)

#### Gotchas

- **SQLite → Postgres migration:** May need schema adjustments (auto-increment fields, etc.)
- **Static files:** Render serves via WhiteNoise or CDN (different from PythonAnywhere)
- **WSGI path:** PythonAnywhere uses `/var/www/`, Render uses Docker `/app/`
- **Environment variables:** PythonAnywhere uses `.env` file, Render uses dashboard

#### Cost Comparison

**PythonAnywhere (current):**
- Free tier OR $5/month (Hacker plan)

**Render (target):**
- Free tier (with limitations) OR $7/month (Starter) + $7/month (Postgres) = $14/month

**Cost increase:** $0-9/month (negligible)

---

### Scenario 2: PythonAnywhere → Railway

**Context:** Alternative to Render, simpler UX, similar pricing. Virtually identical migration.

**Estimated Effort: 4-8 hours** (same as Render)

#### Steps (Abbreviated)

1. Prepare Dockerfile (2-3 hours) - SAME as Render
2. Create Railway.toml OR use Nixpacks auto-detection (30 minutes)
3. Export Database (30 minutes) - SAME
4. Deploy to Railway (1 hour) - Similar to Render
5. Import Database (30 minutes) - SAME
6. Configure Environment Variables (30 minutes) - SAME
7. Test & Verify (1-2 hours) - SAME
8. Update DNS (15 minutes) - SAME

#### Differences from Render

**Railway Advantages:**
- Simpler UI (some prefer)
- $5/month free credit (vs Render's fixed free tier limits)
- Faster database provisioning (30 seconds)

**Railway Disadvantages:**
- Usage-based pricing (less predictable than Render's fixed tiers)
- Smaller ecosystem (fewer guides)

**Cost:** $10-20/month (similar to Render)

**Verdict:** Render vs Railway is personal preference, migration effort identical.

---

### Scenario 3: PythonAnywhere → Fly.io

**Context:** More complex, edge computing features. NOT recommended for QRCards unless multi-region needed.

**Estimated Effort: 6-12 hours**

#### Additional Complexity

- Fly.toml configuration (more complex than render.yaml)
- Multi-region deployment (optional, but Fly's value prop)
- Fly Postgres HA cluster setup (more involved)
- Firecracker microVMs (new concepts to learn)

#### Steps (Abbreviated)

1. Prepare Dockerfile (2-3 hours) - SAME
2. Create fly.toml (1-2 hours) - MORE COMPLEX
3. Export Database (30 minutes) - SAME
4. Deploy to Fly.io (1-2 hours) - NEW TOOLING (flyctl)
5. Import Database (1 hour) - Fly Postgres more complex
6. Configure Environment Variables (30 minutes) - SAME
7. Test & Verify (1-2 hours) - SAME
8. Update DNS (15 minutes) - SAME

**Total Time: 6-12 hours** (2-4 hours more than Render/Railway)

**Cost:** $15-30/month (similar, but usage-based = unpredictable)

**Verdict:** Fly.io is overkill for QRCards. Use Render/Railway instead.

---

### Scenario 4: PythonAnywhere → Heroku

**Context:** Legacy platform, post-Salesforce acquisition. NOT recommended (higher cost, stagnant platform).

**Estimated Effort: 2-4 hours** (easier than Render, but not worth it)

#### Steps (Abbreviated)

1. Create Procfile (30 minutes) - Simpler than Dockerfile
   ```
   web: gunicorn qrcards.wsgi:application
   ```
2. Export Database (30 minutes) - SAME
3. Deploy to Heroku (30 minutes) - `heroku create && git push heroku main`
4. Import Database (30 minutes) - Heroku Postgres provisioning
5. Configure Environment Variables (30 minutes) - `heroku config:set KEY=value`
6. Test & Verify (1 hour) - SAME
7. Update DNS (15 minutes) - SAME

**Total Time: 2-4 hours** (fastest migration, but worst destination)

**Cost:** $16/month (Eco dyno + mini Postgres) - MORE expensive than Render

**Verdict:** Heroku is EASY to migrate to, but BAD choice strategically (already in decline, expensive).

---

### Scenario 5: PythonAnywhere → DIY VPS (DigitalOcean)

**Context:** Maximum control, lowest cost at scale. Requires DevOps skills.

**Estimated Effort: 8-16 hours** (first time), 4-8 hours (if experienced)

#### Steps

**1. Provision VPS (1 hour)**
- Choose DigitalOcean $12/month droplet (2GB RAM, 2 vCPUs)
- Select Ubuntu 24.04 LTS
- Configure SSH keys
- Set up firewall (UFW)

**2. Install Docker & Docker Compose (1 hour)**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt install docker-compose-plugin
```

**3. Create Docker Compose setup (2-3 hours)**
- Write docker-compose.yml (web + database)
- Create Dockerfile (SAME as Render migration)
- Test locally before deploying

**4. Configure Nginx Reverse Proxy (2-3 hours)**
- Install Nginx
- Write `/etc/nginx/sites-available/qrcards` config
- Enable site, restart Nginx

**5. Set Up SSL (Let's Encrypt) (1-2 hours)**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d qrcards.example.com
```

**6. Export & Import Database (1 hour)**
- Export from PythonAnywhere (SAME as above)
- Import to VPS Postgres container
- Run migrations

**7. Deployment Automation (2-4 hours)**
- Write GitHub Actions workflow (SSH deploy)
- Test deployment pipeline
- Document process

**8. Monitoring & Backups (2-3 hours)**
- Set up Uptime Robot (free tier)
- Configure daily database backups to S3/Backblaze
- Set up log rotation

**9. Test & Verify (1-2 hours)**
- SAME as Render migration

**Total Time: 8-16 hours** (significant investment)

#### Ongoing Maintenance

- OS security updates: 1-2 hours/month
- SSL renewal: Automated (check quarterly)
- Database maintenance: 1 hour/month
- Monitoring/alerting: 1-2 hours/month
- **Total: 5-10 hours/month**

#### Cost

- VPS: $12-18/month
- Managed Database (optional): $15-25/month OR DIY for $0
- Backups (S3): $2-5/month
- **Total: $14-48/month**

**Savings vs PaaS:** $5-15/month (not worth it unless >$150/month hosting OR forced by PaaS repricing)

**Verdict:** DIY VPS makes sense ONLY if:
1. Hosting costs >$150/month (break-even)
2. PaaS provider repriced significantly (forced migration)
3. DevOps skills in-house (maintenance manageable)

---

## Migration Effort Summary Table

| From → To | Time | Complexity | Cost (monthly) | Recommended? |
|-----------|------|------------|----------------|--------------|
| **PythonAnywhere → Render** | 4-8h | LOW | $0-14/mo | YES (best choice) |
| **PythonAnywhere → Railway** | 4-8h | LOW | $10-20/mo | YES (equally good) |
| **PythonAnywhere → Fly.io** | 6-12h | MODERATE | $15-30/mo | NO (overkill) |
| **PythonAnywhere → Heroku** | 2-4h | LOW | $16+/mo | NO (bad value) |
| **PythonAnywhere → DIY VPS** | 8-16h | MODERATE-HIGH | $14-48/mo | LATER (when scaled or forced) |
| **Render → Railway** | 1-2h | VERY LOW | ~same | YES (trivial) |
| **Railway → Render** | 1-2h | VERY LOW | ~same | YES (trivial) |
| **Render → DIY VPS** | 6-12h | MODERATE | -$10 to -50/mo | WHEN >$150/mo hosting |

---

## When to Migrate: Decision Framework

### Proactive Migration (Before Forced)

**Trigger 1: Hosting costs exceed $150/month**
- **Action:** Evaluate DIY VPS migration
- **Timeline:** 2-4 weeks (plan, test, execute)
- **Effort:** 8-16 hours
- **Savings:** $50-150/month

**Trigger 2: PaaS provider announces acquisition**
- **Action:** Prepare migration to alternative PaaS (Render ↔ Railway)
- **Timeline:** 1-2 weeks (can execute quickly if needed)
- **Effort:** 4-8 hours
- **Savings:** Avoid future repricing

**Trigger 3: Pricing changes announced (2-3x increase)**
- **Action:** Migrate to alternative PaaS OR DIY VPS
- **Timeline:** 2-4 weeks (depends on repricing deadline)
- **Effort:** 4-16 hours
- **Savings:** 50-70% hosting costs

### Reactive Migration (Forced)

**Trigger 4: PaaS provider shuts down (12-24 month notice)**
- **Action:** Migrate to alternative PaaS (easiest) OR DIY VPS
- **Timeline:** Within deprecation window
- **Effort:** 4-16 hours
- **Impact:** Business continuity

**Trigger 5: Service quality degrades (outages, slow support)**
- **Action:** Migrate to more reliable provider
- **Timeline:** 1-3 months (not urgent, but proactive)
- **Effort:** 4-8 hours
- **Benefit:** Better uptime

---

## Migration Best Practices

### 1. Run Parallel for 1-2 Weeks

**Why:** Allows rollback if issues arise
**How:**
- Deploy to new provider (new domain or subdomain)
- Test thoroughly on new platform
- Keep old provider running
- DNS cutover AFTER validation
- Monitor for 1-2 weeks
- Decommission old provider AFTER stable

**Cost:** Extra hosting for 1 month (~$15-50)
**Benefit:** Zero-risk migration

### 2. Export Database BEFORE Starting

**Why:** Ensures you have backup if migration fails
**How:**
- Full database dump (pg_dump, mysqldump, SQLite copy)
- Store in S3 or local backup
- Verify dump integrity (restore to local test DB)

**Time:** 30 minutes
**Benefit:** Data safety

### 3. Document Current Configuration

**Why:** Ensures nothing is forgotten
**Checklist:**
- All environment variables (SECRET_KEY, DATABASE_URL, etc.)
- External services (email, storage, APIs)
- Background tasks (cron jobs, workers)
- Static files configuration
- Custom domains, SSL certs
- User accounts (admin, etc.)

**Time:** 1 hour
**Benefit:** Complete migration

### 4. Test Thoroughly Before DNS Cutover

**Why:** Avoid downtime
**Testing:**
- User registration/login
- QR code generation (core feature)
- Admin panel access
- Email sending (if used)
- Static files loading
- Database queries
- Background tasks (if any)

**Time:** 1-2 hours
**Benefit:** Confidence in new platform

### 5. Plan DNS Cutover During Low Traffic

**Why:** Minimize user impact if issues arise
**Best Time:**
- Weekend or late night (user time zone)
- Announce maintenance window (if needed)

**TTL Adjustment:**
- Lower DNS TTL to 300 seconds (5 minutes) 24 hours before cutover
- Allows fast rollback if needed

**Time:** 15 minutes cutover, 5-60 minutes propagation

---

## Emergency Migration Scenario

**Context:** PaaS provider announces shutdown in 60 days OR reprices 10x immediately

**Timeline: Compressed to 1-2 weeks**

### Week 1: Preparation (8-12 hours)

**Day 1-2:** Choose destination (Render or Railway)
**Day 3-4:** Create Dockerfile, test locally
**Day 5-6:** Export database, document configuration
**Day 7:** Deploy to new provider (staging/test)

### Week 2: Execution (4-6 hours)

**Day 8-10:** Test thoroughly on new platform
**Day 11-12:** DNS cutover, monitor
**Day 13-14:** Decommission old provider (after stable)

**Total Effort:** 12-18 hours compressed into 2 weeks

**Outcome:** Business continuity maintained, minimal downtime

---

## Conclusion

### Strategic Takeaways

**1. Migration is EASY from low lock-in providers:**
- PythonAnywhere, Render, Railway: 4-8 hour migrations
- Modern Docker-native PaaS: 1-2 hour migrations between each other

**2. DIY VPS is VIABLE but requires 8-16 hours + ongoing maintenance:**
- Makes sense at scale (>$150/month) OR forced by repricing
- Not worth it for early-stage projects

**3. Plan migrations BEFORE forced:**
- Monitor quarterly for acquisition signals
- Have backup provider documented
- Test migration annually (2-4 hours exercise)

**4. Low lock-in = strategic freedom:**
- Can migrate when circumstances change (acquisition, repricing, scale)
- 4-8 hours is acceptable migration cost every 5-7 years
- Avoid high lock-in providers (Heroku add-ons, Fly.io edge features)

### For QRCards

**Start:** PythonAnywhere or Render (4-8 hour migration between them if needed)
**Monitor:** Quarterly check on provider status (acquisition rumors, pricing changes)
**Migrate:** When forced (acquisition/repricing) OR when scaled (>$150/month)
**Destination:** Render/Railway (if timing) OR DIY VPS (if scaled)

**Bottom Line:** Migration is NOT scary. Low lock-in architecture makes it a weekend project, not a multi-month nightmare.
