# QRCards Render Migration Plan v2 (Git Subtree Strategy)

**Strategy:** Git subtree deployment repo + incremental validation
**Timeline:** Nov 15-22, 2025 (Phase 1)
**Vikunja Tasks:** 221016-221020
**Approach:** Deploy from qrcards-deploy repo (subtree of packages/flasklayer)
**Rationale:** See 05_SUBTREE_RECONSIDERED_BARNRAISING.md

---

## Strategic Decision: Git Subtree

### Why Subtree (vs rootDirectory)

**Original plan:** Use Render `rootDirectory: packages/flasklayer` (simple monorepo deploy)

**NEW plan:** Extract `packages/flasklayer/` into separate `qrcards-deploy` repo via git subtree

**Additional effort:** +2 hours upfront setup
**Additional value:**
1. ✅ **Foundation for barnraising** (April 2025 collaboration strategy)
2. ✅ **Enable client content repos** (per-client access control)
3. ✅ **Cleaner deployment artifact** (code only, no content/business docs)
4. ✅ **Security boundaries** (protect business strategy from partners)
5. ✅ **Future white-label licensing** (per-client repo separation)

**Long-term ROI:** 7x year 1, 23x year 2+ (see 05_SUBTREE_RECONSIDERED_BARNRAISING.md)

---

## Repository Architecture

### Current (Monorepo)
```
~/qrcards/                          (1.5GB - everything mixed)
├── content/                        (31MB - multi-client content)
├── docs/                           (163MB - business strategy + tech docs)
├── project/                        (51MB - internal project management)
├── packages/flasklayer/            (685MB - APPLICATION CODE)
└── [other files]
```

### NEW (Multi-Repo with Subtree)
```
PRIMARY REPO (Private - Ivan only):
  ~/qrcards/                        (qrcards-core on GitHub)
  ├── content/                      ← Will extract per-client in Phase 2
  ├── docs/business/                ← PROTECTED (strategy, finance, HR)
  ├── project/                      ← PROTECTED (internal roadmap)
  ├── packages/flasklayer/          ← SOURCE OF TRUTH (syncs to deploy repo)
  └── .github/workflows/            ← Auto-sync to qrcards-deploy

DEPLOYMENT REPO (Semi-private - Dev partners):
  ~/qrcards-deploy/                 (qrcards-deploy on GitHub)
  ├── flasklayer/                   ← EXTRACTED from packages/flasklayer/
  ├── static/
  ├── templates/
  ├── requirements.txt
  ├── Dockerfile                    ← NEW
  ├── render.yaml                   ← NEW
  └── README.md                     ← NEW
```

**Key insight:** Render deploys from `qrcards-deploy`, NOT `qrcards-core`

---

## Migration Plan: Phase-by-Phase

### Phase 1a: Extract Deployment Repo (NEW STEP)

**Goal:** Create qrcards-deploy repo via git subtree
**Time:** 2-3 hours
**When:** Before Render deployment

#### Step 1: Extract Subtree (Local)

```bash
# In ~/qrcards/ (main monorepo)
cd ~/qrcards

# Create branch with ONLY packages/flasklayer/ history
git subtree split --prefix=packages/flasklayer -b deploy-only

# This may take 5-15 minutes depending on Git history size
# Creates new branch with clean history for packages/flasklayer/
```

**What this does:**
- Analyzes all commits touching `packages/flasklayer/`
- Creates new branch with rewritten history
- `packages/flasklayer/` becomes repo root (not nested)

#### Step 2: Create Deployment Repository

```bash
# Create new repo for deployment
mkdir ~/qrcards-deploy
cd ~/qrcards-deploy
git init

# Pull in the extracted subtree
git pull ~/qrcards deploy-only

# Verify structure
ls -la
# Should see: flasklayer/, static/, templates/, requirements.txt, run.py
# (NOT: content/, docs/, project/ - those stay in qrcards-core)
```

#### Step 3: Create Deployment Configuration Files

**Create Dockerfile:**
```bash
# ~/qrcards-deploy/Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Gunicorn server (Render provides $PORT)
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 run:app
EOF
```

**Create render.yaml:**
```bash
# ~/qrcards-deploy/render.yaml
cat > render.yaml << 'EOF'
services:
  - type: web
    name: qrcards
    env: python
    region: oregon
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT --workers 2 run:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: DATABASE_PATH
        value: /data/admin_prod.db
    # Optional: Persistent disk for SQLite
    # disk:
    #   name: qrcards-data
    #   mountPath: /data
    #   sizeGB: 1
EOF
```

**Create README:**
```bash
# ~/qrcards-deploy/README.md
cat > README.md << 'EOF'
# QRCards Deployment Repository

This repository contains the deployment-ready QRCards application.

**Source:** Extracted from `qrcards-core/packages/flasklayer/` via git subtree

**Deployment:** Render (auto-deploy from main branch)

**Sync:** Changes in qrcards-core are automatically synced here via GitHub Actions

## Local Development

```bash
pip install -r requirements.txt
gunicorn run:app
```

## Deployment

Push to main branch → Render auto-deploys
EOF
```

#### Step 4: Push to GitHub

```bash
# In ~/qrcards-deploy/
git add .
git commit -m "Initial deployment repo extracted from qrcards-core"

# Create GitHub repo (via CLI or web)
gh repo create qrcards-deploy --private --source=. --remote=origin

# Or manually:
# Create repo on GitHub: https://github.com/new
git remote add origin git@github.com:YOUR-USERNAME/qrcards-deploy.git
git branch -M main
git push -u origin main
```

#### Step 5: Set Up Auto-Sync (GitHub Actions)

**In qrcards-core repo:**
```bash
# ~/qrcards/.github/workflows/sync-deploy-repo.yml
mkdir -p ~/qrcards/.github/workflows
cat > ~/qrcards/.github/workflows/sync-deploy-repo.yml << 'EOF'
name: Sync Deployment Repo

on:
  push:
    branches: [main]
    paths:
      - 'packages/flasklayer/**'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout qrcards-core
        uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Need full history for subtree

      - name: Set up Git
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"

      - name: Add deploy remote
        run: |
          git remote add deploy https://x-access-token:${{ secrets.DEPLOY_REPO_TOKEN }}@github.com/YOUR-USERNAME/qrcards-deploy.git

      - name: Push to deployment repo
        run: |
          git subtree push --prefix=packages/flasklayer deploy main --squash

      - name: Notify on failure
        if: failure()
        run: echo "Deployment repo sync failed!"
EOF
```

**Create GitHub token:**
1. GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. Create token with access to qrcards-deploy repo
3. qrcards-core → Settings → Secrets → Actions → New secret
4. Name: `DEPLOY_REPO_TOKEN`, Value: `[your token]`

#### Step 6: Test Local Deployment

```bash
# In ~/qrcards-deploy/
cd ~/qrcards-deploy

# Test build
docker build -t qrcards-test .

# Test run (if Docker installed)
docker run -p 5000:10000 -e PORT=10000 qrcards-test
# Visit http://localhost:5000

# Or test without Docker:
pip install -r requirements.txt
export PORT=5000
gunicorn --bind 0.0.0.0:$PORT run:app
```

**Success criteria:**
- ✅ Application starts without errors
- ✅ QR resolution endpoint responds
- ✅ Templates render correctly

---

### Phase 1b: Deploy to Render (RISK-PRIORITIZED)

**Goal:** Deploy app.modelcitizendeveloper.com from qrcards-deploy repo (lowest risk active site)
**Time:** 3-4 hours
**Vikunja:** https://app.vikunja.cloud/tasks/221016
**Strategy:** Start with lowest-risk active site to validate Render before migrating revenue-generating sites
**See:** `07_MIGRATION_PRIORITY.md` for full risk assessment

**IMPORTANT ARCHITECTURE NOTE:**
- Main domain (modelcitizendeveloper.com) → Canva homepage (NO CHANGE)
- App subdomain (app.modelcitizendeveloper.com) → QRCards on PythonAnywhere → Migrating to Render
- This pattern applies to ALL sites (ivantohelpyou.com/app.ivantohelpyou.com, etc.)

**Why app.modelcitizendeveloper.com?**
- ✅ Actually running on QRCards (unlike taelyen.com which is just Canva page)
- ✅ Newsletter site with no critical functionality
- ✅ Low traffic, no revenue impact
- ✅ Perfect for proving Render migration works
- ✅ Main domain stays on Canva (easy WYSIWYG editor)

#### Step 1: Connect Render to Deployment Repo

1. **Render Dashboard** → "New Web Service"

2. **Connect Repository:**
   - Connect GitHub account (if not already)
   - **Select:** `qrcards-deploy` (NOT qrcards-core!)
   - Branch: `main`

3. **Render auto-detects render.yaml:**
   - Service name: qrcards
   - Region: Oregon
   - Plan: Starter ($7/month)
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn --bind 0.0.0.0:$PORT --workers 2 run:app`

4. **Environment Variables:**
   - Render pre-fills from render.yaml
   - Add any secrets (API keys, etc.) in dashboard

5. **Create Service** → Render deploys automatically

#### Step 2: Monitor Deployment

Watch Render logs:
```
Build started...
Pulling code from GitHub
Running: pip install -r requirements.txt
Build complete (2-3 minutes)
Starting service...
Service live at: https://qrcards.onrender.com
```

**First deploy:** 2-5 minutes

#### Step 3: Test on Render URL

```bash
# Test QR resolution
curl https://qrcards.onrender.com/qr/test-token

# Test web interface
curl https://qrcards.onrender.com/intelligence
```

**Success criteria:**
- ✅ Service starts without errors
- ✅ QR codes resolve correctly
- ✅ Response time <200ms
- ✅ No errors in Render logs

#### Step 4: Add Custom Domain (app.modelcitizendeveloper.com - Lowest Risk)

**In Render Dashboard:**
1. qrcards service → Settings → Custom Domains
2. Click "Add Custom Domain"
3. Enter: `app.modelcitizendeveloper.com`
4. Render provides DNS instructions

**In DNS Provider:**
```
Type: CNAME
Host: app (subdomain only)
Value: qrcards.onrender.com
TTL: 300 (5 minutes for easy rollback)
```

**IMPORTANT:**
- Main domain (modelcitizendeveloper.com) → NO CHANGE (stays on Canva)
- Only creating CNAME for app subdomain
- Canva homepage remains accessible at modelcitizendeveloper.com

**Wait for SSL certificate:**
- Render auto-provisions Let's Encrypt certificate
- Status shown in dashboard
- Takes 5-15 minutes

#### Step 5: Validate Custom Domain

```bash
# Test app subdomain URL
curl https://app.modelcitizendeveloper.com/

# Test QR resolution
curl https://app.modelcitizendeveloper.com/qr/[test-token]

# Check response time
curl -w "@%{time_total}s\n" -o /dev/null -s https://app.modelcitizendeveloper.com/

# Verify main domain still on Canva (NO CHANGE)
curl -I https://modelcitizendeveloper.com/
# Should still point to Canva
```

**Success criteria:**
- ✅ HTTPS working (valid SSL certificate)
- ✅ All paths responding correctly
- ✅ Response times <100ms
- ✅ No errors in logs

---

### Phase 1c: Test Sync Workflow (NEW)

**Goal:** Verify git subtree auto-sync works
**Time:** 30 minutes

#### Test Workflow

```bash
# 1. Make change in qrcards-core
cd ~/qrcards/packages/flasklayer
echo "# Test change" >> run.py
git add run.py
git commit -m "Test subtree sync"
git push origin main

# 2. GitHub Actions triggers automatically
# Watch: https://github.com/YOUR-USERNAME/qrcards-core/actions

# 3. Verify sync to qrcards-deploy
# Check: https://github.com/YOUR-USERNAME/qrcards-deploy/commits

# 4. Render auto-deploys from qrcards-deploy
# Watch Render dashboard for new deployment

# 5. Verify change live on app subdomain
curl https://app.modelcitizendeveloper.com/
# Should reflect changes within 1-2 minutes
```

**Full workflow time:** 1-2 minutes (GitHub Actions + Render deploy)

**Success criteria:**
- ✅ GitHub Actions sync completes without errors
- ✅ qrcards-deploy receives changes
- ✅ Render auto-deploys
- ✅ Changes live on production

---

### Phase 2: Full Migration (Task 221018 - Due Nov 22)

**Goal:** Migrate remaining 3 sites (risk-prioritized order)
**Time:** 1-2 hours (UNCHANGED - subtree already set up)
**Vikunja:** https://app.vikunja.cloud/tasks/221018

**Prerequisites:**
- Phase 1 complete (app.modelcitizendeveloper.com working)
- Subtree sync validated

**Migration order (by risk level):**
1. **cfo.inversefractional.com** (medium risk - recent launch, uses cfo. subdomain)
2. **qrcard.conventioncityseattle.com** (medium-high risk - FIFA trails)
3. **app.ivantohelpyou.com** (HIGHEST risk - Decision Analysis paid service)

**IMPORTANT:** Main domains stay on Canva, only migrating QRCards subdomains
- inversefractional.com (Canva) vs cfo.inversefractional.com (QRCards)

**Steps for each site (30 min per site):**

1. **Add Custom Domain in Render**
   - Dashboard → qrcards → Settings → Custom Domains
   - Add subdomain (e.g., `cfo.inversefractional.com` or `app.modelcitizendeveloper.com`)

2. **Update DNS (Subdomain CNAME only)**
   ```
   Type: CNAME
   Host: cfo (for cfo.inversefractional.com) OR app (for app.*.com)
   Value: qrcards.onrender.com
   TTL: 300
   ```
   **IMPORTANT:** Main domain DNS unchanged (stays on Canva)
   - inversefractional.com → Canva (NO CHANGE)
   - cfo.inversefractional.com → Render (MIGRATED)

3. **Wait for SSL** (5-10 minutes)

4. **Test thoroughly**
   - Verify app subdomain working
   - Verify main domain still on Canva
   - Check QR codes
   - Monitor logs for 24-48 hours before next migration

5. **Repeat for next domain** (don't rush - validate stability first)

**Special precautions for app.ivantohelpyou.com:**
- [ ] Deploy during low-traffic hours
- [ ] Keep PythonAnywhere active for 1 week (parallel operation)
- [ ] Test Decision Analysis service thoroughly
- [ ] Monitor payment flows
- [ ] Verify ivantohelpyou.com (main domain) still on Canva
- [ ] Have DNS rollback ready (TTL=300)

---

### Phase 3: FIFA Demo Deployment (Task 221019 - Due Dec 2)

**Goal:** Deploy Mexico fan trail on Render
**Time:** 3-4 hours
**Vikunja:** https://app.vikunja.cloud/tasks/221019

**Optional:** Extract FIFA content into separate repo (test content subtree strategy)

```bash
# In ~/qrcards/
git subtree split --prefix=content/fifa -b content-fifa

# Create qrcards-content-fifa repo
mkdir ~/qrcards-content-fifa
cd ~/qrcards-content-fifa
git init
git pull ~/qrcards content-fifa
# Push to GitHub
```

**Benefits:**
- ✅ Test content subtree workflow
- ✅ Can share with Sheela/April without business exposure
- ✅ Clean FIFA demo without other client content

---

### Phase 4: Documentation (Task 221020 - Due Dec 5)

**Goal:** Document migration + subtree workflow
**Time:** 1-2 hours
**Vikunja:** https://app.vikunja.cloud/tasks/221020

**Documents to create:**
1. `DEPLOYMENT.md` - How to deploy (for future reference)
2. `SUBTREE_WORKFLOW.md` - How subtree sync works
3. `RENDER_MIGRATION_RESULTS.md` - Actual vs estimated effort

**Update:**
1. `2.050_PAAS_STRATEGIC_ASSESSMENT.md` - Mark Render complete
2. `03_INFRASTRUCTURE_INVENTORY.md` - List scripts deleted

---

## Effort Summary

### Original Plan (rootDirectory only)
- **Setup:** 5 minutes (Render config)
- **Deployment:** 4-5 hours
- **Total:** ~5 hours

### NEW Plan (git subtree)
- **Subtree setup:** 2-3 hours (one-time)
- **Deployment:** 3-4 hours (same as before)
- **Total:** 6-8 hours

**Additional investment:** 2-3 hours upfront

**Return:**
- Foundation for barnraising (250-500 hours/year collaboration value)
- Foundation for per-client content repos (25 hours/year saved)
- Foundation for white-label licensing (future revenue)
- **ROI: 7x year 1, 23x year 2+**

---

## Rollback Plan

**If subtree sync fails:**
```bash
# Emergency: Deploy directly from qrcards-core
# 1. Create render.yaml in qrcards-core/
services:
  - type: web
    rootDirectory: packages/flasklayer  # Fallback to original plan
    ...

# 2. Update Render to deploy from qrcards-core
# 3. Disable GitHub Actions sync
```

**If Render deployment fails:**
```bash
# Revert DNS to PythonAnywhere
# Keep qrcards-deploy repo for future retry
```

**Data safety:**
- PythonAnywhere stays active during migration
- Databases unchanged
- Can revert DNS within 5 minutes (TTL=300)

---

## Success Metrics

### Technical
- ✅ All domains responding <100ms
- ✅ Subtree sync working (1-2 min end-to-end)
- ✅ Git auto-deploy functioning
- ✅ SSL certificates valid

### Business
- ✅ Saving $12.25/month ($147/year)
- ✅ Deployment time: 10-15 min → 30 sec (git push)
- ✅ Foundation for barnraising established
- ✅ Can extract client content repos (Phase 2)

### Strategic
- ✅ Subtree workflow validated
- ✅ Ready to onboard collaborators (April 2026)
- ✅ Content separation architecture proven
- ✅ White-label licensing path established

---

## Next Actions

### Immediate (Today - Nov 15)
1. ✅ Read this plan
2. ✅ Review subtree rationale (05_SUBTREE_RECONSIDERED_BARNRAISING.md)
3. ⏭️ Create qrcards-deploy repo (Phase 1a)
4. ⏭️ Test local deployment

### This Week (Nov 18-20)
1. ⏭️ Set up GitHub Actions sync
2. ⏭️ Connect Render to qrcards-deploy
3. ⏭️ Deploy ivantohelpyou.com
4. ⏭️ Validate subtree sync workflow

### Next Week (Nov 22)
1. ⏭️ Migrate remaining 3 sites
2. ⏭️ Monitor for 48 hours
3. ⏭️ Deactivate PythonAnywhere (or keep as backup)

---

## References

- **Subtree rationale:** 05_SUBTREE_RECONSIDERED_BARNRAISING.md
- **Subtree deep dive:** 04_GIT_SUBTREE_DEEP_DIVE.md
- **Infrastructure inventory:** 03_INFRASTRUCTURE_INVENTORY.md
- **Monorepo strategy:** 02_MONOREPO_DEPLOYMENT_STRATEGY.md
- **Barnraising plan:** ~/qrcards/docs/business/human-resources/collaborative-barn-raising.md
- **Vikunja tasks:** https://app.vikunja.cloud/projects/14214/50932
