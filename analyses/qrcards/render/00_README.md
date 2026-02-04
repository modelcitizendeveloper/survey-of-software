# QRCards Render Migration Documentation

**Created:** November 15, 2025
**Status:** Ready for implementation
**Vikunja Project:** https://app.vikunja.cloud/projects/14214/50932

---

## Quick Start

**New to this migration?** Start here:

1. **Read:** `01_MIGRATION_PLAN_V2_SUBTREE.md` (comprehensive migration plan)
2. **Understand:** `05_SUBTREE_RECONSIDERED_BARNRAISING.md` (why git subtree)
3. **Execute:** Follow Phase 1a in migration plan (create qrcards-deploy repo)
4. **Reference:** `06_SUBTREE_QUICK_REFERENCE.md` (daily commands)

---

## Documents Overview

### Core Planning Documents

#### 01_MIGRATION_PLAN_V2_SUBTREE.md ⭐ **START HERE**
- Complete step-by-step migration plan
- Git subtree setup instructions
- Phase-by-phase deployment guide
- Rollback procedures
- **Use:** Primary implementation guide

#### 02_MONOREPO_DEPLOYMENT_STRATEGY.md
- Analysis of monorepo vs split repo approaches
- `rootDirectory` vs git subtree comparison
- File organization best practices
- **Use:** Understanding deployment options

#### 03_INFRASTRUCTURE_INVENTORY.md
- Complete inventory of 20+ deployment scripts
- Analysis of which scripts to keep/eliminate/modify
- ~1,000 lines of bash to delete after migration
- Time savings: 3 hours/month → 30 min/month
- **Use:** Understanding what changes in infrastructure

### Git Subtree Analysis

#### 04_GIT_SUBTREE_DEEP_DIVE.md
- Detailed explanation of git subtree mechanics
- Complexity analysis (setup, operations, maintenance)
- Benefits quantification
- When subtree makes sense
- **Original verdict:** Not worth it (for Render deployment alone)
- **Use:** Technical deep dive on subtree

#### 05_SUBTREE_RECONSIDERED_BARNRAISING.md ⭐ **KEY STRATEGIC DOCUMENT**
- Re-evaluation of subtree for barnraising collaboration
- Multi-domain content separation strategy
- Security & access control architecture
- **NEW verdict:** Strategically essential
- ROI: 7x year 1, 23x year 2+
- **Use:** Understanding WHY we're using git subtree

#### 06_SUBTREE_QUICK_REFERENCE.md ⭐ **DAILY USE**
- Quick command reference
- Daily workflow
- Troubleshooting guide
- Cheat sheet
- **Use:** Day-to-day operations after migration

---

## Decision Timeline

### Original Approach (Nov 15 morning)
- Use Render `rootDirectory: packages/flasklayer`
- Simple monorepo deployment
- 5 hours total effort

### Revised Approach (Nov 15 afternoon)
- Use git subtree to extract qrcards-deploy repo
- Foundation for barnraising collaboration
- 6-8 hours total effort (+2 hours investment)
- Unlocks 250-500 hours/year collaboration value

### Key Turning Point
**Discovery:** Barnraising strategy from April 2025 requires controlled access:
- Clients need content access without seeing business strategy
- Dev partners need code access without seeing client content
- UI designers need template access without seeing application logic
- **Git subtree solves all three problems**

---

## Repository Architecture

### Current DNS/Hosting Architecture
**All sites use split architecture:**
- **Main domain** (e.g., ivantohelpyou.com, modelcitizendeveloper.com) → Canva homepage
- **App subdomain** (e.g., app.ivantohelpyou.com, app.modelcitizendeveloper.com) → QRCards on PythonAnywhere

**Migration scope:** App subdomains only (PythonAnywhere → Render)
**Out of scope:** Main domains (staying on Canva - easy WYSIWYG editor)

---

### Before Migration (Monorepo)
```
~/qrcards/ (1.5GB - everything mixed)
├── content/ (31MB - multi-client content)
├── docs/ (163MB - business strategy + tech docs)
├── project/ (51MB - internal project management)
└── packages/flasklayer/ (685MB - application code)
```

**Problem:** Granting any access = full repo exposure

### After Migration (Multi-Repo)
```
qrcards-core (Private - Ivan only)
├── Source of truth for all code
├── Business strategy protected
└── Content managed here

qrcards-deploy (Semi-private - dev partners)
├── Application code only
├── Deployed to Render (serves app.*.com subdomains)
└── Synced from qrcards-core via GitHub Actions

[Future - Phase 2-3]
qrcards-content-[client] (Per-client repos)
qrcards-collab-[space] (Per-collaborator repos)
```

**Solution:** Granular access control via separate repos

---

## Implementation Status

### ✅ Completed
- [x] Infrastructure inventory (20+ scripts analyzed)
- [x] PaaS strategic assessment
- [x] Git subtree deep dive
- [x] Barnraising collaboration analysis
- [x] Multi-repo architecture design
- [x] Migration plan v2 (git subtree)
- [x] Quick reference guide
- [x] Vikunja tasks created (221016-221020)
- [x] Documentation complete

### ⏭️ Next (Task 221016 - Due Nov 20)
- [ ] Create qrcards-deploy repo
- [ ] Set up GitHub Actions sync
- [ ] Deploy to Render
- [ ] Migrate app.modelcitizendeveloper.com (lowest risk - proof of concept)
- [ ] Validate subtree workflow
- **Note:** Main domain (modelcitizendeveloper.com) stays on Canva

### 📅 Future (Phase 2-4)
- [ ] Migrate 3 remaining sites (Nov 22)
- [ ] FIFA demo deployment (Dec 2)
- [ ] Extract client content repos (Jan 2026)
- [ ] Extract collaboration repos (Mar 2026)

---

## Key Metrics

### Infrastructure Simplification
- **Current:** 1,500 lines of custom deployment scripts
- **After:** 700 lines (mostly local dev tools)
- **Reduction:** 53%

### Time Savings
- **Deployment:** 10-15 min → 30 sec (95% faster)
- **Monthly maintenance:** 3.5 hours → 30 min (86% reduction)

### Cost Savings
- **Current:** $19.25/month (PythonAnywhere)
- **After:** $7/month (Render)
- **Savings:** $147/year

### Strategic Value (Git Subtree)
- **Setup cost:** 27 hours (one-time, spread over 6 months)
- **Ongoing cost:** 12 hours/year
- **Value:** 275 hours/year (collaboration + client access)
- **ROI:** 7x year 1, 23x year 2+

---

## Vikunja Tasks

**Project:** FIFA World Cup LOC (14214)
**Section:** Render Experiment (50932)

1. **Task 221016** - Quick Proof: Deploy app.modelcitizendeveloper.com to Render
   - Due: Nov 20, 2025
   - Priority: 5 (DO NOW)
   - Includes: Subtree setup + deployment
   - Time: 6-8 hours
   - **Note:** Changed from app.ivantohelpyou.com (highest risk - paid service) to app.modelcitizendeveloper.com (lowest risk active site - newsletter, no critical functionality)
   - **Architecture:** Main domain (modelcitizendeveloper.com) stays on Canva, only migrating app subdomain

2. **Task 221018** - Migrate Remaining 3 Sites to Render
   - Due: Nov 22, 2025
   - Priority: 4 (Urgent)
   - Time: 1-2 hours

3. **Task 221019** - FIFA: Deploy Mexico Demo Trail on Render
   - Due: Dec 2, 2025
   - Priority: 5 (DO NOW)
   - Time: 3-4 hours

4. **Task 221020** - Document Render Migration Results
   - Due: Dec 5, 2025
   - Priority: 3 (High)
   - Time: 1 hour

---

## Related Documents

### In ~/spawn-solutions/
- `applications/qrcards/2.050_PAAS_STRATEGIC_ASSESSMENT.md` - Original PaaS analysis
- `applications/qrcards/CTO_TECHNICAL_READINESS_ASSESSMENT.md` - CTO assessment

### In ~/qrcards/
- `docs/business/human-resources/collaborative-barn-raising.md` - Barnraising strategy (April 2025)
- `docs/business/human-resources/inner-circle-barn-raising-steps.md` - Implementation steps

### In ~/spawn-analysis/
- `conversations/009-nov-dec-2025-portfolio-strategy/29_WEEK1_FRIDAY_REVIEW_NOV14.md` - FIFA strategy context

---

## FAQ

### Why git subtree instead of rootDirectory?

**Short answer:** Barnraising collaboration strategy requires it.

**Long answer:** See `05_SUBTREE_RECONSIDERED_BARNRAISING.md`

Key points:
- Need to grant clients content access without exposing business strategy
- Need to grant dev partners code access without exposing client content
- Need to grant UI designers template access without exposing application logic
- Git subtree creates separate repos with controlled access
- Enables 250-500 hours/year of collaboration value

### Is this over-engineering?

**For Render deployment alone:** Yes (ROI negative)

**For barnraising + multi-domain + security:** No (ROI 7x-23x)

The 2-hour additional investment NOW:
- Proves subtree workflow
- Creates foundation for 4-6 future repos
- Unlocks collaboration strategy from April 2025

### Can I still use rootDirectory if I want?

**Yes!** Rollback plan is documented in migration plan.

If subtree becomes too complex:
1. Update Render to deploy from qrcards-core
2. Use `rootDirectory: packages/flasklayer`
3. Disable GitHub Actions sync
4. Keep qrcards-deploy for potential future use

### What if I just want to deploy to Render quickly?

**Fast path (5 hours):**
1. Skip all subtree docs
2. Follow original plan: Use `rootDirectory`
3. Deploy from qrcards monorepo
4. Done

**Recommended path (6-8 hours):**
1. Read `01_MIGRATION_PLAN_V2_SUBTREE.md`
2. Extract qrcards-deploy repo (+2 hours)
3. Deploy from qrcards-deploy
4. Gain foundation for future collaboration

The 2-hour investment enables barnraising in 2026.

---

## Next Steps

### Today (Nov 15)
1. ✅ Read this README
2. ✅ Review `01_MIGRATION_PLAN_V2_SUBTREE.md`
3. ✅ Understand `05_SUBTREE_RECONSIDERED_BARNRAISING.md`
4. ⏭️ Decide: Proceed with subtree approach?

### This Weekend (Nov 16-17)
1. ⏭️ Create Render account (if not done)
2. ⏭️ Create qrcards-deploy repo (Phase 1a)
3. ⏭️ Test local deployment
4. ⏭️ Set up GitHub Actions sync

### Next Week (Nov 18-20)
1. ⏭️ Connect Render to qrcards-deploy
2. ⏭️ Deploy app.modelcitizendeveloper.com (lowest risk active site)
3. ⏭️ Validate subtree sync workflow
4. ⏭️ Complete Task 221016
**Note:** Main domains stay on Canva, only migrating app subdomains

### Following Weeks (Nov 22 - Dec 16)
1. ⏭️ Migrate cfo.inversefractional.com (medium risk - recent launch)
2. ⏭️ Migrate qrcard.conventioncityseattle.com (medium-high risk - FIFA trails)
3. ⏭️ Optional: Test taelyen.com (new domain setup - no existing QRCards app)
4. ⏭️ Deploy app.ivantohelpyou.com LAST (highest risk - paid Decision Analysis service)
5. ⏭️ Complete Task 221018
**See:** `07_MIGRATION_PRIORITY.md` for detailed risk-prioritized sequence
**Architecture:** Main domains stay on Canva, QRCards subdomains migrate to Render
- inversefractional.com (Canva) / cfo.inversefractional.com (QRCards)
- modelcitizendeveloper.com (Canva) / app.modelcitizendeveloper.com (QRCards)
- ivantohelpyou.com (Canva) / app.ivantohelpyou.com (QRCards)

---

## Questions or Issues?

**Unclear documentation?**
- All questions anticipated in FAQ sections of each doc
- Check `06_SUBTREE_QUICK_REFERENCE.md` for commands

**Subtree seems too complex?**
- Rollback plan documented in `01_MIGRATION_PLAN_V2_SUBTREE.md`
- Can always fall back to `rootDirectory` approach

**Need to understand the "why"?**
- Read `05_SUBTREE_RECONSIDERED_BARNRAISING.md`
- Reviews barnraising collaboration strategy
- Explains multi-domain content separation
- Quantifies ROI (7x-23x)

---

## Summary

**What:** Migrate QRCards from PythonAnywhere to Render

**How:** Git subtree deployment repo + incremental site migration

**Why subtree:** Enable barnraising collaboration + multi-domain content separation

**When:** Nov 15-22, 2025 (Phase 1), then incremental (Phase 2-4)

**Effort:** 6-8 hours Phase 1 (+2 hours vs simple approach)

**Value:** $147/year cost savings + 275 hours/year collaboration value

**ROI:** 7x year 1, 23x year 2+

---

**Ready to start? → Read `01_MIGRATION_PLAN_V2_SUBTREE.md`**
