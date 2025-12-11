# QRCards Render Migration Plan

**Strategy:** Incremental validation - prove with one site, migrate rest if successful
**Timeline:** Nov 15-22, 2025
**Vikunja Tasks:** 221016-221020
**Total Effort:** 6-8 hours (vs 16h original estimate)

---

## Service Selection Decision

### What You Need

**Current QRCards Architecture:**
- Flask web application (Python 3.11)
- 4 customer domains (ivantohelpyou.com, conventioncityseattle.com, etc.)
- SQLite databases (admin_prod.db, runtime_prod.db)
- Single codebase, router handles all domains
- ~100 QR scans/month (demo traffic)

### Render Service Types Available

#### ✅ **Web Service** (RECOMMENDED)
**Use this for QRCards**

**What it is:**
- Dynamic web application
- Supports Flask, Django, Node.js, Ruby, etc.
- HTTP/HTTPS traffic
- Can handle multiple custom domains
- Auto-deploy from Git

**Why it fits:**
- ✅ Flask application = perfect match
- ✅ Handles unlimited custom domains (no extra charge vs PythonAnywhere's $3/domain)
- ✅ Git auto-deploy (eliminates custom scripts)
- ✅ Built-in SSL certificates
- ✅ Starter plan: $7/month (vs $19.25 PythonAnywhere)

**Configuration:**
```yaml
services:
  - type: web
    name: qrcards
    plan: starter  # $7/month
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT app:app
```

---

#### ❌ Static Site
**NOT for QRCards**

**What it is:** HTML/CSS/JS files served from CDN (no server-side code)
**Why not:** QRCards is dynamic (Flask backend, database queries, QR resolution logic)

---

#### ❌ Private Service
**NOT for QRCards**

**What it is:** Web app only accessible from other Render services
**Why not:** QRCards needs public internet access (customer QR scans)

---

#### ❌ Background Worker
**NOT needed (yet)**

**What it is:** Long-running async tasks (job queue processing)
**Why not:** QRCards handles all requests synchronously (QR resolution <100ms)
**Future use:** If you add batch content generation or analytics processing

---

#### ❌ Cron Job
**NOT needed (yet)**

**What it is:** Scheduled tasks (hourly/daily scripts)
**Why not:** No current scheduled tasks in QRCards
**Future use:** Database backups, analytics aggregation, cleanup jobs

---

#### 🤔 **Postgres** (OPTIONAL - Phase 2)
**Consider for post-migration**

**What it is:** Managed PostgreSQL database
**Current:** Using SQLite (adequate for demo traffic)
**Cost:** $7/month (Starter plan)
**When to add:**
- After successful Render migration (separate decision)
- When traffic grows beyond SQLite capacity
- If you need multi-user write concurrency

**Decision:** **START WITHOUT POSTGRES**
- Prove Render with SQLite first (cheaper, simpler)
- Add Postgres later if needed (separate $7/month)
- Initial cost: $7/month (web only) vs $14/month (web + db)

---

#### ❌ Key Value (Redis)
**NOT needed**

**What it is:** Redis-compatible cache/message broker
**Why not:** No caching or job queue in current architecture
**Future use:** Session management, cache layer for high traffic

---

## Migration Plan: Phase-by-Phase

### Phase 1: Quick Proof (Task 221016 - Due Nov 20)
**Goal:** Deploy ivantohelpyou.com to Render, validate functionality
**Time:** 4-6 hours
**Vikunja:** https://app.vikunja.cloud/tasks/221016

**What to create in Render Dashboard:**

1. **Click "New Web Service"**

2. **Connect Repository:**
   - Connect GitHub account
   - Select repository: `[your-qrcards-repo]`
   - Branch: `main` (or create `render-test` branch)

3. **Configure Service:**
   ```
   Name: qrcards
   Region: Oregon (closest to Seattle)
   Branch: main
   Root Directory: [leave blank if app is in repo root]

   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --bind 0.0.0.0:$PORT app:app

   Plan: Starter ($7/month)
   ```

4. **Environment Variables:**
   ```
   FLASK_ENV=production
   PORT=[auto-provided by Render]
   ```

5. **DO NOT add Postgres yet** - Using SQLite for initial proof

**Steps:**

1. **Create Dockerfile** (~/qrcards/Dockerfile)
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD gunicorn --bind 0.0.0.0:$PORT app:app
   ```

2. **Create render.yaml** (~/qrcards/render.yaml)
   ```yaml
   services:
     - type: web
       name: qrcards
       env: python
       region: oregon
       plan: starter
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app
       envVars:
         - key: FLASK_ENV
           value: production
   ```

3. **Test Locally with Docker**
   ```bash
   cd ~/qrcards
   docker build -t qrcards .
   docker run -p 5000:10000 -e PORT=10000 qrcards
   curl http://localhost:5000/qr/test-token
   ```

4. **Push to GitHub**
   ```bash
   git add Dockerfile render.yaml
   git commit -m "Add Render deployment config"
   git push origin main
   ```

5. **Create Web Service in Render**
   - Dashboard → "New Web Service"
   - Connect GitHub repo
   - Follow config above
   - Click "Create Web Service"
   - Wait for deployment (~3-5 minutes)

6. **Test on Render URL**
   - Render provides URL: `qrcards.onrender.com`
   - Test: `https://qrcards.onrender.com/qr/test-token`
   - Verify QR resolution works
   - Check logs in Render dashboard

7. **Point DNS for ivantohelpyou.com**
   ```
   DNS Provider: [your DNS provider]
   Record Type: CNAME
   Host: app.ivantohelpyou.com
   Value: qrcards.onrender.com
   TTL: 300 (5 minutes for easy rollback)
   ```

8. **Add Custom Domain in Render**
   - Render dashboard → qrcards service → Settings → Custom Domains
   - Add: `app.ivantohelpyou.com`
   - Render auto-provisions SSL certificate (~5-10 minutes)

9. **Validate**
   - Test: `https://app.ivantohelpyou.com/intelligence`
   - Test dev path: `https://app.ivantohelpyou.com/dev/intelligence`
   - Test test path: `https://app.ivantohelpyou.com/test/intelligence`
   - Verify response times <100ms
   - Check Render logs for errors

**Success Criteria:**
- ✅ ivantohelpyou.com working on Render
- ✅ Dev/test/prod paths all functional
- ✅ Response times <100ms
- ✅ Git push triggers auto-deploy
- ✅ No errors in logs

**Decision Point:**
- **If successful:** Proceed to Phase 2 (migrate remaining sites)
- **If issues:** Document problems, stay on PythonAnywhere, update Vikunja Task 221020

---

### Phase 2: Full Migration (Task 221018 - Due Nov 22)
**Goal:** Migrate remaining 3 sites
**Time:** 1-2 hours
**Vikunja:** https://app.vikunja.cloud/tasks/221018

**Prerequisites:**
- Phase 1 complete (ivantohelpyou.com working)
- No major issues discovered

**Steps (30 min per site):**

For each remaining domain:
1. **Add Custom Domain in Render**
   - Render dashboard → qrcards service → Settings → Custom Domains
   - Click "Add Custom Domain"
   - Enter: `qrcard.conventioncityseattle.com`

2. **Update DNS**
   ```
   Record Type: CNAME
   Host: qrcard.conventioncityseattle.com
   Value: qrcards.onrender.com
   TTL: 300 (5 minutes)
   ```

3. **Wait for SSL** (~5-10 minutes)
   - Render auto-provisions Let's Encrypt certificate
   - Status shown in dashboard

4. **Test**
   - Verify QR codes work
   - Check response times
   - Review logs

**Sites to Migrate:**
- [ ] qrcard.conventioncityseattle.com
- [ ] [Site 3]
- [ ] [Site 4]

**Parallel Operation:**
- Keep PythonAnywhere active for 48 hours (safety net)
- Monitor both platforms
- If issues, revert DNS to PythonAnywhere

**Success Criteria:**
- ✅ All 4 sites working on Render
- ✅ All QR codes resolving correctly
- ✅ No customer complaints
- ✅ Response times consistent

---

### Phase 3: FIFA Demo Deployment (Task 221019 - Due Dec 2)
**Goal:** Deploy Mexico fan trail on Render
**Time:** 3-4 hours
**Vikunja:** https://app.vikunja.cloud/tasks/221019

**Prerequisites:**
- Render migration complete
- YAML→DAP pipeline productized

**Steps:**
1. Generate Mexico fan trail using pipeline
2. Deploy to same Render service (new path/domain)
3. Test on mobile
4. Create demo tent cards

**Demo URL Options:**
- `fifa.conventioncityseattle.com/mexico-fans`
- `app.ivantohelpyou.com/fifa/mexico-demo`

---

### Phase 4: Decommission PythonAnywhere
**Goal:** Cancel PythonAnywhere subscription
**Time:** 30 minutes
**When:** After 1 week stable on Render

**Steps:**

1. **Verify Stability** (1 week monitoring)
   - [ ] No errors in Render logs
   - [ ] Response times <100ms
   - [ ] No customer complaints
   - [ ] All QR codes working

2. **Final Backup from PythonAnywhere**
   ```bash
   ssh pythonanywhere
   cd ~/qrcards
   tar -czf qrcards-backup-final-$(date +%Y%m%d).tar.gz admin_prod.db runtime_prod.db
   # Download to local machine
   ```

3. **Cancel PythonAnywhere**
   - PythonAnywhere dashboard → Account → Cancel subscription
   - Keep account active for 1 month (free tier) as emergency fallback

4. **Update Documentation**
   - Mark PythonAnywhere decommissioned
   - Update deployment docs to reference Render only

---

## Cost Comparison

### Before (PythonAnywhere)
```
Base plan: $12/month
Extra web apps: 2 × $3 = $6/month
Disk space: $1.25/month
Total: $19.25/month
```

### After (Render - Phase 1)
```
Web Service (Starter): $7/month
Postgres: $0 (using SQLite)
Total: $7/month
Savings: $12.25/month ($147/year)
```

### Future (If Adding Postgres)
```
Web Service: $7/month
Postgres: $7/month
Total: $14/month
Savings: $5.25/month ($63/year)
Still cheaper + better DevOps
```

---

## Rollback Plan

**If Render has issues:**

1. **DNS Rollback** (5-15 minutes)
   ```
   Revert CNAME: app.ivantohelpyou.com → PythonAnywhere IP
   Wait for DNS propagation (5-15 min with TTL=300)
   ```

2. **PythonAnywhere Still Active**
   - Database untouched
   - Custom scripts still work
   - Zero data loss

**Rollback Triggers:**
- QR resolution error rate >10%
- Response times >500ms
- Database corruption
- Customer complaints

---

## Success Metrics

### Technical
- ✅ All domains responding <100ms
- ✅ Zero errors in Render logs (24h monitoring)
- ✅ Git push auto-deploys working
- ✅ SSL certificates valid on all domains

### Business
- ✅ No customer complaints
- ✅ All QR codes working
- ✅ Saving $12.25/month confirmed
- ✅ FIFA demo deployed successfully

### Operational
- ✅ Custom deployment scripts deleted
- ✅ Deployment time: <5 minutes (vs 10-15 min manual)
- ✅ Logs accessible in dashboard (no SSH needed)

---

## Next Steps

1. **Immediate** (Today, Nov 15)
   - [ ] Review this plan
   - [ ] Confirm Render account created
   - [ ] Identify QRCards GitHub repository

2. **Nov 18-20** (Task 221016)
   - [ ] Create Dockerfile
   - [ ] Create render.yaml
   - [ ] Deploy Phase 1 (ivantohelpyou.com)

3. **Nov 22** (Task 221018)
   - [ ] Migrate remaining 3 sites (if Phase 1 successful)

4. **Dec 2** (Task 221019)
   - [ ] Deploy FIFA Mexico demo trail

---

## References

- **Vikunja Project:** https://app.vikunja.cloud/projects/14214
- **PaaS Assessment:** ~/spawn-solutions/applications/qrcards/2.050_PAAS_STRATEGIC_ASSESSMENT.md
- **Render Docs:** https://render.com/docs
- **Experiment Log:** ~/spawn-solutions/applications/qrcards/render/EXPERIMENT_LOG.md (create as you work)
