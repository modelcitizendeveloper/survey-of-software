# QRCards Infrastructure Inventory: PythonAnywhere → Render Mapping

**Purpose:** Complete inventory of current PythonAnywhere infrastructure and how it maps to Render
**Date:** November 15, 2025
**Status:** Pre-migration analysis

---

## Executive Summary

QRCards has **custom deployment infrastructure** built for PythonAnywhere over ~2 years. This analysis inventories what exists, what's needed, and what Render provides out-of-box.

**Key Finding:** Most custom scripts can be **eliminated** on Render (Git auto-deploy replaces ~1,000 lines of bash).

---

## Part 1: Deployment Scripts Inventory

### Root-Level Deployment Scripts

#### 1. `~/qrcards/launch` ✅ **ELIMINATE on Render**
```bash
Location: ~/qrcards/launch
Lines: ~200
Purpose: "Big Red Button" - Deploy prod_prod database to production
Current workflow:
  1. Copy prod_prod.db → ready_to_launch.db
  2. Call deploy_unified.sh
  3. Archive launched database
```

**Render equivalent:** `git push origin main` (auto-deploys)

---

#### 2. `~/qrcards/copy-db` ⚠️ **KEEP for local dev**
```bash
Location: ~/qrcards/copy-db
Purpose: Copy databases between environments (dev_dev, test_test, prod_prod)
```

**Render equivalent:** N/A (local development tool)
**Action:** Keep for local database management, not needed in Render deployment

---

#### 3. `~/qrcards/backup` ✅ **REPLACE with Render backups**
```bash
Location: ~/qrcards/backup
Purpose: Create timestamped database backups
Creates: ~/qrcards/backups/admin_YYYYMMDD_HHMMSS.db
```

**Render equivalent:**
- Postgres: Automatic daily backups (included)
- SQLite: Manual backup via download from Render dashboard
**Action:** Can eliminate once on Postgres

---

#### 4. `~/qrcards/fetch-production-db` ⚠️ **KEEP but modify**
```bash
Location: ~/qrcards/fetch-production-db
Purpose: Download production database from PythonAnywhere for local testing
```

**Render equivalent:** Download from Render dashboard or use `render psql` CLI
**Action:** Update script for Render API/CLI

---

#### 5. `~/qrcards/compare-databases.sh` ⚠️ **KEEP**
```bash
Location: ~/qrcards/compare-databases.sh
Purpose: Compare two databases to detect drift
```

**Render equivalent:** N/A (local tool)
**Action:** Keep for development

---

### Flasklayer Deployment Scripts

#### 6. `packages/flasklayer/scripts/deploy_unified.sh` ✅ **ELIMINATE**
```bash
Location: ~/qrcards/packages/flasklayer/scripts/deploy_unified.sh
Lines: ~500
Purpose: Unified deployment - Code, DB, Config, Static
Components:
  --code              Deploy Python source
  --deps              Install dependencies
  --templates         Deploy Jinja templates
  --static            Deploy CSS/JS/images
  --database-only     Deploy admin database
  --config            Deploy config files
  --flasklayer        Deploy backend (code + deps)
  --frontend          Deploy UI (templates + static)
```

**Render equivalent:**
- `buildCommand: pip install -r requirements.txt` (replaces --deps)
- `startCommand: gunicorn run:app` (replaces --code)
- Git auto-deploy (replaces --templates, --static)

**Action:** DELETE after migration

---

#### 7. `packages/flasklayer/scripts/deployment_manifest.sh` ✅ **ELIMINATE**
```bash
Location: ~/qrcards/packages/flasklayer/scripts/deployment_manifest.sh
Purpose: Helper functions for deploy_unified.sh
Functions:
  - File filtering
  - Exclusion patterns
  - Deployment logging
```

**Render equivalent:** Not needed (Git handles file selection)
**Action:** DELETE after migration

---

#### 8. `packages/flasklayer/scripts/deploy_wsgi.sh` ✅ **ELIMINATE**
```bash
Location: ~/qrcards/packages/flasklayer/scripts/deploy_wsgi.sh
Purpose: Deploy WSGI configuration to PythonAnywhere
```

**Render equivalent:** Not needed (Render uses gunicorn directly)
**Action:** DELETE after migration

---

#### 9. `packages/flasklayer/scripts/fast_template_deploy.sh` ✅ **ELIMINATE**
```bash
Location: ~/qrcards/packages/flasklayer/scripts/fast_template_deploy.sh
Purpose: Quick single-file template deployment (bypass full deploy)
```

**Render equivalent:** `git push` (deploys changed files only)
**Action:** DELETE after migration

---

### QRC Command Wrapper

#### 10. `~/qrcards/qr` Script ⚠️ **KEEP (modify)**
```bash
Location: ~/qrcards/qr
Purpose: Unified CLI for QRCards operations
Commands:
  - deploy          → ./launch (ELIMINATE - use git push)
  - test            → ./test (KEEP - run tests locally)
  - backup/restore  → ./backup, ./restore (REPLACE - use Render backups)
  - health/status   → ./health, ./ignition (KEEP - local diagnostics)
  - local           → ./local (KEEP - local development server)
  - dap/template    → Package CLIs (KEEP - content management)
```

**Render equivalent:** No single wrapper needed (git push replaces deploy)
**Action:** Keep for local development, remove deploy/backup commands

---

## Part 2: Complete Script Inventory

### All Executable Scripts in ~/qrcards/

| Script | Purpose | Keep/Eliminate | Render Equivalent |
|--------|---------|----------------|-------------------|
| `./backup` | Create database backups | ✅ ELIMINATE | Postgres auto-backups |
| `./compare-databases.sh` | Compare DB schemas | ⚠️ KEEP | N/A (local tool) |
| `./copy-db` | Copy DB between envs | ⚠️ KEEP | N/A (local tool) |
| `./db-report` | Database health report | ⚠️ KEEP | N/A (local tool) |
| `./fetch-production-db` | Download prod DB | ⚠️ MODIFY | `render psql` or API |
| `./health` | System health check | ⚠️ KEEP | N/A (local tool) |
| `./ignition` | Quick status check | ⚠️ KEEP | Render dashboard |
| `./launch` | Deploy to prod | ✅ ELIMINATE | `git push origin main` |
| `./launch-content` | Deploy content | ✅ ELIMINATE | `git push origin main` |
| `./launch-db` | Deploy database | ✅ ELIMINATE | `git push origin main` |
| `./local` | Start local server | ⚠️ KEEP | N/A (local dev) |
| `./logs` | View logs | ⚠️ KEEP/MODIFY | Render dashboard logs |
| `./restore` | Restore from backup | ✅ ELIMINATE | Render restore UI |
| `./start` | Start local (alias) | ⚠️ KEEP | N/A (local dev) |
| `./test` | Run test suite | ⚠️ KEEP | GitHub Actions (optional) |
| `./qr` | Unified CLI | ⚠️ MODIFY | Remove deploy commands |

---

## Part 3: Directory Structure Issue

### Current Problem: `flasklayer/flasklayer/` ⚠️ **ANNOYING**

**Current structure:**
```
packages/flasklayer/              # Root
├── flasklayer/                   # Package (same name!)
│   ├── __init__.py
│   ├── app.py
│   ├── models/
│   ├── routes/
│   └── services/
├── static/
├── templates/
├── requirements.txt
└── run.py
```

**Why it's annoying:**
```python
# Import looks weird:
from flasklayer.flasklayer.app import create_app  # NO!

# Actual import (works but confusing):
from flasklayer.app import create_app  # OK but package name = folder name
```

**Standard Python convention:**
```
packages/flasklayer/              # Project root
├── src/                          # Source code directory
│   └── flasklayer/               # Package
│       ├── __init__.py
│       ├── app.py
│       └── ...
├── static/
├── templates/
├── requirements.txt
└── run.py
```

**Better names:**
```
Option A: Rename package
packages/qrcards/                 # Project root
├── qrcards/                      # Package (clear name)
│   ├── __init__.py
│   ├── app.py
│   └── ...

Option B: Add src/ directory
packages/flasklayer/              # Project root
├── src/
│   └── qrcards/                  # Package
│       ├── __init__.py
│       ├── app.py
│       └── ...
```

### Render Impact

**Current (flasklayer/flasklayer/):**
```yaml
# render.yaml
services:
  - type: web
    rootDirectory: packages/flasklayer
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
```

**If renamed to src/qrcards/:**
```yaml
# render.yaml
services:
  - type: web
    rootDirectory: packages/flasklayer
    buildCommand: pip install -e .  # Install package in editable mode
    startCommand: gunicorn run:app
```

**Recommendation:** Fix during migration (rename flasklayer/flasklayer → flasklayer/src/qrcards)

---

## Part 4: Environment Matrix System

### Current PythonAnywhere Setup

**Environment matrix:**
```
{FLASK_ENV}_{DATABASE_ENV}

Combinations:
- prod_prod   → Production Flask + Production DB
- test_test   → Test Flask + Test DB
- dev_dev     → Dev Flask + Dev DB
- dev_prod    → Dev Flask + Production DB (testing)
- prod_test   → Prod Flask + Test DB (validation)
```

**Implementation:**
- Separate database files: db/admin/prod_prod.db, db/admin/test_test.db, etc.
- Environment detection via custom script
- Manual environment selection in deploy scripts

### Render Equivalent

**Render approach:**
```
Separate services per environment:

Production:
  - Branch: main
  - Service: qrcards-production
  - Database: qrcards-prod

Staging:
  - Branch: staging
  - Service: qrcards-staging
  - Database: qrcards-staging

Development:
  - Local only (not deployed)
```

**Simplification:** No matrix - standard dev/staging/prod pipeline

---

## Part 5: What Gets Eliminated

### Scripts to DELETE After Migration ✅

1. `./launch` (200 lines)
2. `./launch-content`
3. `./launch-db`
4. `./backup` (replaced by Postgres backups)
5. `./restore` (replaced by Render UI)
6. `packages/flasklayer/scripts/deploy_unified.sh` (500 lines)
7. `packages/flasklayer/scripts/deployment_manifest.sh`
8. `packages/flasklayer/scripts/deploy_wsgi.sh`
9. `packages/flasklayer/scripts/fast_template_deploy.sh`

**Total lines eliminated:** ~1,000+ lines of bash

### Scripts to KEEP ⚠️

**Local development:**
- `./local` - Start local Flask server
- `./test` - Run test suite
- `./copy-db` - Database management (local)
- `./compare-databases.sh` - Schema comparison
- `./db-report` - Database diagnostics
- `./health` / `./ignition` - System checks

**Update for Render:**
- `./fetch-production-db` - Download from Render instead of PythonAnywhere
- `./logs` - Add Render log viewing
- `./qr` - Remove deploy/backup commands

### Scripts to CREATE 📝

**New Render-specific scripts:**
```bash
# ~/qrcards/scripts/render/
├── deploy-staging.sh       # Deploy to Render staging (git push staging)
├── deploy-production.sh    # Deploy to Render prod (git push main)
├── download-db.sh          # Download database from Render
├── logs.sh                 # Tail Render logs (render logs command)
└── rollback.sh             # Rollback to previous deployment
```

**Estimated:** 200 lines total (vs 1,000+ eliminated)

---

## Part 6: Database Strategy

### Current: SQLite Files

```
packages/flasklayer/db/admin/
├── prod_prod.db           # Production admin database
├── test_test.db           # Test admin database
├── dev_dev.db             # Development admin database
└── ready_to_launch.db     # Staging area for deployments

packages/flasklayer/db/runtime/
└── [similar structure]
```

**Size:** ~50MB combined
**Deployment:** Copied to PythonAnywhere via SCP

### Render Options

**Option A: Keep SQLite (Phase 1 - Quick Proof)**
```yaml
services:
  - type: web
    disk:
      name: qrcards-data
      mountPath: /data
      sizeGB: 1
```

**Pros:**
- ✅ No migration needed
- ✅ Identical to current setup
- ✅ Faster initial deployment

**Cons:**
- ❌ Manual backups required
- ❌ Persistent disk = extra $1-2/month
- ❌ Not taking advantage of Render Postgres

**Option B: Migrate to Postgres (Phase 2 - Post-Proof)**
```yaml
services:
  - type: web
databases:
  - name: qrcards-db
    plan: starter  # $7/month, includes backups
```

**Pros:**
- ✅ Automatic backups
- ✅ Better scalability
- ✅ Point-in-time recovery
- ✅ Read replicas available

**Cons:**
- ⚠️ Migration effort (4-8 hours)
- ⚠️ $7/month cost

**Recommendation:**
1. **Phase 1:** Use SQLite with persistent disk (prove Render works)
2. **Phase 2:** Migrate to Postgres (after FIFA demo, before production scale)

---

## Part 7: Static Assets & Templates

### Current Structure

```
packages/flasklayer/
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── [domain-specific assets]
├── templates/  (symlink to flasklayer/templates/)
└── flasklayer/
    └── templates/
        ├── base.html
        ├── intelligence.html
        └── [domain-specific templates]
```

**Deployment:** Copied via deploy_unified.sh --frontend

### Render Handling

**Auto-deployed with code:**
```
Git push → Render clones repo → static/ and templates/ included automatically
```

**No special handling needed** - Git tracks everything

**CDN (future optimization):**
- Move static assets to Cloudflare/Fastly
- Serve from CDN instead of app server
- Update template references

---

## Part 8: Secrets Management

### Current: PythonAnywhere

**Environment variables:**
```
Set via PythonAnywhere dashboard → Web → Environment Variables
- DATABASE_URL (local file path)
- FLASK_ENV (prod/test/dev)
- SECRET_KEY
- API_KEYS
```

### Render Equivalent

**Environment variables:**
```yaml
# render.yaml
services:
  - type: web
    envVars:
      - key: FLASK_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: qrcards-db
          property: connectionString
      - key: SECRET_KEY
        sync: false  # Set in dashboard (not in YAML)
```

**Secret management:**
- Sensitive values: Set in Render dashboard (not committed to Git)
- Non-sensitive: Can include in render.yaml
- Database URL: Auto-configured by Render

---

## Part 9: Migration Effort Summary

### Scripts Analysis

| Category | Current (PythonAnywhere) | After (Render) | Reduction |
|----------|--------------------------|----------------|-----------|
| **Deployment scripts** | 1,000+ lines | 0 lines | -100% |
| **Local dev scripts** | 500 lines | 500 lines | 0% |
| **Render-specific** | 0 lines | 200 lines | +200 lines |
| **Net change** | 1,500 lines | 700 lines | **-53%** |

### Time Savings

| Activity | PythonAnywhere | Render | Savings |
|----------|----------------|--------|---------|
| **Deployment** | 10-15 min (manual) | 30 sec (git push) | -95% |
| **Script maintenance** | 2 hours/month | 0 hours/month | -100% |
| **Debugging deploy** | 1 hour/month | 0 hours/month | -100% |
| **Total per month** | ~3.5 hours | ~30 min | **-86%** |

---

## Part 10: Decision Matrix

### What to Do With Each Component

| Component | Action | Timing | Effort |
|-----------|--------|--------|--------|
| `launch`, `deploy_unified.sh` | ✅ DELETE | After migration | 0 hours |
| `backup`, `restore` | ✅ DELETE | After Postgres | 0 hours |
| `local`, `test`, `health` | ⚠️ KEEP | N/A | 0 hours |
| `qr` command | ⚠️ MODIFY | After migration | 1 hour |
| `fetch-production-db` | ⚠️ UPDATE | After migration | 2 hours |
| `flasklayer/flasklayer/` | ⚠️ RENAME | During migration | 4 hours |
| SQLite → Postgres | 📝 MIGRATE | Phase 2 (optional) | 8 hours |
| Environment matrix | 🔄 SIMPLIFY | During migration | 2 hours |

**Total migration effort (infrastructure):** 15-17 hours (spread across migration phases)

---

## Part 11: Recommendations

### Immediate (Task 221016 - Quick Proof)

1. ✅ **Keep SQLite** - Don't migrate database yet
2. ✅ **Keep flasklayer/flasklayer/ structure** - Don't rename yet (reduces risk)
3. ✅ **Deploy with rootDirectory** - Monorepo works as-is
4. ✅ **Test git push workflow** - Prove auto-deploy works
5. ⚠️ **Keep PythonAnywhere active** - Parallel operation for 48 hours

### Short-term (Post-Quick Proof)

1. 📝 **Delete deployment scripts** - Remove launch, deploy_unified.sh, etc.
2. 📝 **Update qr command** - Remove deploy/backup, keep dev tools
3. 📝 **Create Render helpers** - Simple scripts for logs, rollback

### Long-term (Post-FIFA)

1. 🔄 **Migrate to Postgres** - Better backups, scalability
2. 🔄 **Rename flasklayer/flasklayer/** - Fix annoying structure
3. 🔄 **Add CI/CD** - GitHub Actions for tests before deploy
4. 🔄 **CDN for static assets** - Offload to Cloudflare

---

## Part 12: Next Steps

### For Task 221016 (Quick Proof)

1. **Create render.yaml** in ~/qrcards/:
   ```yaml
   services:
     - type: web
       rootDirectory: packages/flasklayer
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn run:app
   ```

2. **Test local build:**
   ```bash
   cd ~/qrcards/packages/flasklayer
   pip install -r requirements.txt
   gunicorn run:app
   ```

3. **Push to GitHub** and connect Render

4. **Deploy ivantohelpyou.com** (single site proof)

5. **If successful:** Plan script cleanup (use this inventory)

---

## Summary

**Current state:** ~1,500 lines of custom deployment infrastructure
**Render state:** ~700 lines (mostly local dev tools)
**Effort to migrate:** 15-17 hours (infrastructure only)
**Ongoing savings:** 3 hours/month → 30 min/month

**Bottom line:** Most custom scripts become obsolete with Git auto-deploy. Keep local dev tools, delete deployment scripts, create minimal Render helpers.
