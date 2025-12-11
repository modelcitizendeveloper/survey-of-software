# Git Subtree Quick Reference for QRCards

**Purpose:** Quick commands for daily git subtree operations
**Audience:** Ivan (primary developer)
**Related:** 01_MIGRATION_PLAN_V2_SUBTREE.md

---

## One-Time Setup (Already Done)

```bash
# Extract deployment repo
cd ~/qrcards
git subtree split --prefix=packages/flasklayer -b deploy-only

# Create qrcards-deploy repo
mkdir ~/qrcards-deploy && cd ~/qrcards-deploy
git init
git pull ~/qrcards deploy-only
git remote add origin git@github.com:YOUR-USERNAME/qrcards-deploy.git
git push -u origin main

# Add deploy remote to qrcards-core
cd ~/qrcards
git remote add deploy git@github.com:YOUR-USERNAME/qrcards-deploy.git
```

---

## Daily Workflow

### Scenario: Normal Development (Most Common)

```bash
# Work in qrcards-core as usual
cd ~/qrcards/packages/flasklayer
vim flasklayer/app.py
git add .
git commit -m "Add new feature"
git push origin main

# GitHub Actions automatically:
# 1. Syncs to qrcards-deploy
# 2. Render auto-deploys
# Wait ~1-2 minutes, feature is live
```

**You don't need to do anything manually!** GitHub Actions handles sync.

---

### Scenario: Manual Sync (If GitHub Actions Fails)

```bash
# Push changes to deployment repo manually
cd ~/qrcards
git subtree push --prefix=packages/flasklayer deploy main --squash

# This takes 30-60 seconds
# Render auto-deploys after sync completes
```

---

### Scenario: Pull Changes from Deployment Repo (Rare)

**When:** Someone commits directly to qrcards-deploy (hotfix, dev partner contribution)

```bash
# Pull changes back into qrcards-core
cd ~/qrcards
git subtree pull --prefix=packages/flasklayer deploy main --squash

# Resolve any conflicts in packages/flasklayer/
git push origin main

# Now both repos are in sync again
```

---

## Check Sync Status

### Verify GitHub Actions Ran

```bash
# Visit GitHub Actions page
open https://github.com/YOUR-USERNAME/qrcards-core/actions

# Look for "Sync Deployment Repo" workflow
# Green checkmark = success
# Red X = failed (use manual sync)
```

### Verify qrcards-deploy is Up-to-Date

```bash
# Check latest commit in qrcards-deploy
gh api repos/YOUR-USERNAME/qrcards-deploy/commits/main --jq '.commit.message'

# Should match your latest commit in packages/flasklayer/
cd ~/qrcards/packages/flasklayer
git log -1 --oneline
```

### Verify Render Deployed Latest

```bash
# Check Render dashboard
open https://dashboard.render.com

# Or via CLI
render ps qrcards
# Shows latest deployment time + commit SHA
```

---

## Troubleshooting

### GitHub Actions Sync Failed

**Symptom:** Red X on GitHub Actions

**Fix:**
```bash
# 1. Check error in GitHub Actions logs
# 2. Common issue: Merge conflict

# Manual sync:
cd ~/qrcards
git subtree push --prefix=packages/flasklayer deploy main --squash

# If that fails:
# - Check for uncommitted changes
# - Ensure packages/flasklayer/ has changes to sync
# - Try without --squash: git subtree push --prefix=packages/flasklayer deploy main
```

---

### Render Not Deploying

**Symptom:** Changes in qrcards-deploy but not live

**Fix:**
```bash
# 1. Check Render dashboard
open https://dashboard.render.com

# 2. Manual deploy trigger
render deploy qrcards

# 3. Check Render logs for errors
render logs qrcards --tail
```

---

### Changes Lost Between Repos

**Symptom:** Commit in qrcards-core but not in qrcards-deploy

**Fix:**
```bash
# Force sync (nuclear option)
cd ~/qrcards
git subtree push --prefix=packages/flasklayer deploy main --force

# This overwrites qrcards-deploy with qrcards-core
# Only use if qrcards-core is source of truth
```

---

## Adding More Subtrees (Future)

### Extract Client Content Repo

```bash
# Example: Convention City Seattle content
cd ~/qrcards
git subtree split --prefix=content/convention-city-seattle -b content-ccs

mkdir ~/qrcards-content-conventioncity
cd ~/qrcards-content-conventioncity
git init
git pull ~/qrcards content-ccs
git remote add origin git@github.com:YOUR-USERNAME/qrcards-content-conventioncity.git
git push -u origin main

# Add remote to qrcards-core
cd ~/qrcards
git remote add content-ccs git@github.com:YOUR-USERNAME/qrcards-content-conventioncity.git
```

### Sync Content Repo

```bash
# Push changes to content repo
cd ~/qrcards
git subtree push --prefix=content/convention-city-seattle content-ccs main --squash

# Pull changes from content repo
git subtree pull --prefix=content/convention-city-seattle content-ccs main --squash
```

---

## Emergency: Revert to Monorepo Deployment

**If subtree becomes too complex:**

```bash
# 1. Update Render to deploy from qrcards-core
# In qrcards-core, create render.yaml:
services:
  - type: web
    rootDirectory: packages/flasklayer
    ...

# 2. Update Render service settings
render set-repo qrcards YOUR-USERNAME/qrcards-core

# 3. Disable GitHub Actions sync
# Edit .github/workflows/sync-deploy-repo.yml
# Change: on: push: → on: workflow_dispatch:

# 4. Keep qrcards-deploy for future (don't delete)
```

---

## Useful Commands

### View Subtree History

```bash
# See all commits that touched packages/flasklayer/
cd ~/qrcards
git log --oneline -- packages/flasklayer/
```

### Compare Repos

```bash
# Check if repos are in sync
cd ~/qrcards
git diff deploy/main:flasklayer/app.py packages/flasklayer/flasklayer/app.py

# Or compare entire directory
git diff deploy/main packages/flasklayer/
```

### List All Remotes

```bash
cd ~/qrcards
git remote -v

# Should show:
# origin    (qrcards-core)
# deploy    (qrcards-deploy)
# [future: content-ccs, collab-templates, etc.]
```

---

## Cheat Sheet

| Action | Command |
|--------|---------|
| **Normal dev** | `git push origin main` (GitHub Actions syncs) |
| **Manual sync to deploy** | `git subtree push --prefix=packages/flasklayer deploy main --squash` |
| **Pull from deploy** | `git subtree pull --prefix=packages/flasklayer deploy main --squash` |
| **Check GitHub Actions** | `gh run list --workflow="Sync Deployment Repo"` |
| **Check Render status** | `render ps qrcards` |
| **Force sync** | `git subtree push --prefix=packages/flasklayer deploy main --force` |
| **Add new subtree** | `git subtree split --prefix=PATH -b BRANCH` |

---

## Remember

1. **Source of truth:** qrcards-core (packages/flasklayer/)
2. **Never commit directly to qrcards-deploy** (unless hotfix, then pull back immediately)
3. **GitHub Actions handles sync automatically** (you rarely need manual commands)
4. **Render deploys from qrcards-deploy** (NOT qrcards-core)
5. **Subtree is for deployment + collaboration separation** (barnraising strategy)

---

## Next Steps (Future Subtrees)

**Phase 2 (Jan 2026):** Client content repos
- qrcards-content-conventioncity
- qrcards-content-company
- qrcards-content-personal

**Phase 3 (Mar 2026):** Collaboration repos
- qrcards-collab-templates (UI designers)
- qrcards-collab-analytics (data specialists)

See: 05_SUBTREE_RECONSIDERED_BARNRAISING.md for full roadmap
