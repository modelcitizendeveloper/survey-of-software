# QRCards Monorepo Deployment Strategy for Render

**Issue:** QRCards repo is a monorepo containing documentation, project files, and application code. PythonAnywhere deploys a subtree. How should Render handle this?

**Date:** November 15, 2025
**Context:** Task 221016 - Quick Proof deployment planning

---

## Current Repository Structure

```
~/qrcards/                           # Git repository root
├── project/                         # Documentation, planning, reports
├── docs/                            # Project documentation
├── content/                         # Content files
├── data/                            # Data files
├── modernization/                   # Research and exploration
├── scripts/                         # Utility scripts
├── backups/                         # Database backups
├── packages/
│   └── flasklayer/                  # ACTUAL APPLICATION CODE
│       ├── flasklayer/              # Python package
│       │   ├── __init__.py
│       │   ├── app.py
│       │   ├── models/
│       │   ├── routes/
│       │   ├── services/
│       │   └── templates/
│       ├── static/                  # Static assets
│       ├── requirements.txt
│       ├── scripts/deploy_unified.sh
│       └── run.py
├── launch                           # Deployment script (PythonAnywhere)
└── [many other files]
```

**Key insight:** Application code lives in `packages/flasklayer/`, not repo root.

---

## Current PythonAnywhere Deployment

### What Gets Deployed

**PythonAnywhere approach:**
```bash
# From launch script → deploy_unified.sh
# Copies subtree to server:
SOURCE: ~/qrcards/packages/flasklayer/
TARGET: /home/username/qrcards/flasklayer/  (on PythonAnywhere server)

# What gets copied:
- flasklayer/ (Python package)
- static/
- templates/
- requirements.txt
- run.py
- db/ (databases)
```

**What stays local (NOT deployed):**
- project/ (documentation)
- docs/
- content/
- modernization/
- backups/
- Root-level scripts
- Everything except packages/flasklayer/

**Deployment command:**
```bash
./launch  # Runs deploy_unified.sh
# Which does:
# 1. Copy packages/flasklayer/ → server:/home/user/qrcards/flasklayer/
# 2. SSH to server
# 3. cd /home/user/qrcards/flasklayer/
# 4. pip install -r requirements.txt
# 5. Reload WSGI app
```

---

## Render Deployment Options

### Option 1: Deploy Entire Repo (NOT RECOMMENDED)

```yaml
# render.yaml
services:
  - type: web
    name: qrcards
    rootDirectory: /
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
```

**Problems:**
- ❌ Sends 500MB+ repo to Render (project docs, backups, etc.)
- ❌ Longer build times (unnecessary file transfer)
- ❌ requirements.txt not in root (would fail)
- ❌ app.py not in root (would fail)
- ❌ Security risk (exposes project docs, backups)

---

### Option 2: Use Root Directory (RECOMMENDED)

```yaml
# render.yaml (in repo root: ~/qrcards/render.yaml)
services:
  - type: web
    name: qrcards
    rootDirectory: packages/flasklayer  # KEY: Deploy only this subtree
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
```

**What Render does:**
1. Clones entire repo (shallow clone)
2. **Changes working directory to `packages/flasklayer/`**
3. Runs build command from that directory
4. Only deploys files in that directory

**Advantages:**
- ✅ Mimics PythonAnywhere structure (subtree deployment)
- ✅ Only application code deployed
- ✅ Minimal changes to existing structure
- ✅ Keeps monorepo benefits (docs + code in one repo)
- ✅ No gitignore needed for project files

**Disadvantages:**
- ⚠️ Still clones full repo (but doesn't deploy it)
- ⚠️ Build cache includes full repo (slightly larger disk usage)

---

### Option 3: Split Repo (NOT RECOMMENDED for now)

**Create separate repos:**
```
~/qrcards-app/           # Application code only (NEW repo)
├── flasklayer/
├── static/
├── templates/
├── requirements.txt
├── Dockerfile
└── render.yaml

~/qrcards-docs/          # Documentation (existing repo)
├── project/
├── docs/
└── modernization/
```

**Advantages:**
- ✅ Clean separation
- ✅ Faster clones
- ✅ Smaller deployments

**Disadvantages:**
- ❌ Breaks existing workflow
- ❌ Two repos to manage
- ❌ Cross-references between docs and code harder
- ❌ Migration effort required
- ❌ Loses monorepo benefits

**Verdict:** Not worth it for current scale.

---

### Option 4: Git Subtree (ADVANCED - Future consideration)

Use `git subtree` to split packages/flasklayer/ into separate repo, keep synced with main repo.

**Complexity:** High
**Benefit:** Marginal
**Verdict:** Overkill for current needs

---

## Recommended Approach: Option 2 (Root Directory)

### Implementation

**1. Create render.yaml in repo root** (`~/qrcards/render.yaml`)

```yaml
services:
  - type: web
    name: qrcards
    env: python
    region: oregon
    plan: starter
    rootDirectory: packages/flasklayer  # Deploy only this subtree
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT run:app
    envVars:
      - key: FLASK_ENV
        value: production
```

**2. Verify application entry point**

Check `packages/flasklayer/run.py`:
```python
from flasklayer.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
```

**3. Ensure requirements.txt exists**

```bash
ls -la ~/qrcards/packages/flasklayer/requirements.txt
# Should exist (it does based on earlier inspection)
```

**4. Optional: Create Dockerfile** (in `packages/flasklayer/Dockerfile`)

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Copy application files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Gunicorn server
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 run:app
```

---

## Directory Structure Mapping

### PythonAnywhere (Current)
```
LOCAL:  ~/qrcards/packages/flasklayer/
SERVER: /home/user/qrcards/flasklayer/
```

### Render (Proposed)
```
GIT REPO:     ~/qrcards/                     # Full monorepo
CLONE:        /opt/render/project/src/       # Render clones here
WORKING DIR:  /opt/render/project/src/packages/flasklayer/  # rootDirectory applied
BUILD:        pip install in working dir
RUN:          gunicorn from working dir
```

**Key point:** Render's `rootDirectory` acts like `cd packages/flasklayer` before running commands.

---

## File Organization Best Practices

### What stays in monorepo root
```
~/qrcards/
├── project/              # Keep - project management
├── docs/                 # Keep - documentation
├── modernization/        # Keep - research
├── content/              # Keep - content files
├── data/                 # Keep - data files
├── render.yaml           # NEW - Render config (points to packages/flasklayer)
├── README.md             # Keep - repo overview
└── .gitignore            # Update - exclude sensitive files
```

### What goes in application directory
```
~/qrcards/packages/flasklayer/
├── flasklayer/           # Application code
├── static/               # Static assets
├── templates/            # Jinja templates (symlinked)
├── requirements.txt      # Python dependencies
├── Dockerfile            # NEW - Docker config (optional)
├── run.py                # Application entry point
├── db/                   # Databases (local dev only)
└── scripts/              # Deployment scripts (PythonAnywhere only)
```

### .gitignore additions
```
# Add to ~/qrcards/.gitignore
packages/flasklayer/db/*.db         # Don't commit databases
packages/flasklayer/db/admin/*.db
backups/*.tar.gz                    # Don't commit backups
private_config/                      # Don't commit secrets
*.log                                # Don't commit logs
```

---

## Migration Steps

### Phase 1: Preparation
1. ✅ Confirm `packages/flasklayer/` contains all application code
2. ✅ Verify `requirements.txt` is up to date
3. ✅ Check `run.py` is the entry point
4. ✅ Create `render.yaml` in repo root with `rootDirectory: packages/flasklayer`

### Phase 2: Testing
1. Clone repo fresh (simulate Render)
   ```bash
   cd /tmp
   git clone ~/qrcards test-deploy
   cd test-deploy/packages/flasklayer
   pip install -r requirements.txt
   gunicorn run:app  # Should work
   ```

2. Verify paths resolve correctly
   ```bash
   # From packages/flasklayer/
   python -c "from flasklayer.app import create_app; app = create_app(); print(app)"
   ```

### Phase 3: Deployment
1. Push `render.yaml` to GitHub
2. Connect Render to repo
3. Render auto-detects `render.yaml`
4. Deploy using `rootDirectory: packages/flasklayer`

---

## Comparison: Monorepo vs Split Repo

| Aspect | Monorepo (Current) | Split Repo |
|--------|-------------------|------------|
| **Code location** | packages/flasklayer/ | qrcards-app/ (new repo) |
| **Docs location** | project/, docs/ | qrcards-docs/ (separate repo) |
| **Deployment** | rootDirectory points to subtree | Full repo deployed |
| **Git history** | Unified (code + docs) | Separate histories |
| **Cross-references** | Easy (same repo) | Harder (cross-repo links) |
| **Clone size** | ~500MB (includes docs) | ~50MB (app only) |
| **Build time** | +30 seconds (full clone) | Faster (smaller clone) |
| **Maintenance** | Single repo | Two repos to sync |
| **Migration effort** | None (rootDirectory) | High (repo split) |

**Verdict:** Keep monorepo, use `rootDirectory`.

---

## Alternative: Sparse Checkout (Advanced)

If Render supported sparse checkout, you could clone only `packages/flasklayer/`. But Render doesn't expose this, so `rootDirectory` is the practical solution.

---

## FAQ

### Q: Will Render clone my 500MB repo every deploy?
**A:** Yes, but only once per build. Render caches the repo between builds. Incremental deploys only fetch new commits (fast).

### Q: Are my project docs exposed in the deployment?
**A:** No. `rootDirectory: packages/flasklayer` means only that directory is deployed. Docs stay in the clone but aren't served.

### Q: Can I keep using the monorepo structure?
**A:** Yes! `rootDirectory` is designed exactly for this use case.

### Q: What if I want to deploy from a different branch?
**A:** Change branch in Render dashboard. `rootDirectory` still applies.

### Q: Should I add a .dockerignore?
**A:** If using Dockerfile, yes:
```
# packages/flasklayer/.dockerignore
db/*.db
logs/
__pycache__/
*.pyc
.pytest_cache/
```

---

## Recommended File Locations

### Place in repo root (~/qrcards/)
- `render.yaml` - Points to packages/flasklayer
- `.gitignore` - Excludes databases, logs, backups
- `README.md` - Project overview

### Place in application dir (~/qrcards/packages/flasklayer/)
- `Dockerfile` (optional) - Docker build config
- `.dockerignore` (optional) - Exclude from Docker build
- `requirements.txt` - Python dependencies
- `run.py` - Application entry point

---

## Decision: Use rootDirectory

**Final recommendation:**
- ✅ Keep monorepo structure (~/qrcards/)
- ✅ Use `rootDirectory: packages/flasklayer` in render.yaml
- ✅ Place render.yaml in repo root
- ✅ No repo split needed
- ✅ Minimal changes to existing workflow

**Next step:** Create render.yaml and test local deployment from packages/flasklayer/ directory.

---

## References

- **Render docs:** https://render.com/docs/yaml-spec#root-directory
- **Current deployment:** ~/qrcards/packages/flasklayer/scripts/deploy_unified.sh
- **Application code:** ~/qrcards/packages/flasklayer/flasklayer/
- **Migration plan:** 01_MIGRATION_PLAN.md
