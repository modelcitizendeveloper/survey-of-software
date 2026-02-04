# QRCards Render Migration: Risk-Prioritized Order

## Site Risk Assessment

**IMPORTANT ARCHITECTURE NOTE:**
All sites run homepages on Canva with QRCards on subdomain:
- Main domain (e.g., `ivantohelpyou.com`) → Canva homepage
- App subdomain (e.g., `app.ivantohelpyou.com`) → QRCards on PythonAnywhere

**Migration target:** App subdomains only (QRCards instances)

---

### NOT A MIGRATION CANDIDATE
**taelyen.com**
- Not currently hosting QRCards app
- Just a Canva home page
- Domain owned but no app subdomain
- **NOT APPLICABLE FOR MIGRATION**

### LOWEST RISK (Start here)
**app.modelcitizendeveloper.com**
- Newsletter site
- No critical functionality yet
- Low traffic
- Currently running on PythonAnywhere
- Main domain (modelcitizendeveloper.com) stays on Canva
- **DEPLOY FIRST**

### MEDIUM RISK
**cfo.inversefractional.com** (note: uses cfo. subdomain, not app.)
- Recent launch (new site)
- Demo/portfolio site
- Limited existing users
- Main domain (inversefractional.com) stays on Canva
- **DEPLOY SECOND**

**qrcard.conventioncityseattle.com**
- Live FIFA demo trails (important for pitch)
- Active content, but recoverable
- **DEPLOY THIRD**

### HIGHEST RISK (Deploy last, after validation)
**app.ivantohelpyou.com**
- Hosts Decision Analysis paid service ($$$)
- Main profile site
- Revenue-generating
- Main domain (ivantohelpyou.com) stays on Canva
- **DEPLOY FOURTH/LAST** (only after all others proven stable)

---

## Revised Migration Sequence

### Phase 1: Proof with Lowest Risk Active Site
**Site:** app.modelcitizendeveloper.com
**Rationale:**
- Lowest risk among sites currently running on QRCards
- Newsletter site with no critical functionality
- Low traffic, zero revenue impact
- Proves Render deployment works
- Validates subtree sync workflow
- Can iterate freely without customer impact

**Note:**
- Main domain (modelcitizendeveloper.com) stays on Canva - NO CHANGE
- Only migrating app subdomain (app.modelcitizendeveloper.com) to Render
- taelyen.com has no QRCards app, so not applicable for migration

**Steps:**
1. Create qrcards-deploy repo (git subtree)
2. Set up GitHub Actions sync
3. Deploy to Render
4. Point app.modelcitizendeveloper.com DNS to Render (CNAME)
5. Test thoroughly for 24-48 hours
6. Main domain (modelcitizendeveloper.com) remains on Canva - UNCHANGED

**Success criteria:**
- Site loads correctly
- QR resolution working (if applicable)
- Response times <100ms
- No errors in logs
- Subtree sync functioning

---

### Phase 2: Expand to Medium Risk Sites
**Order:**
1. cfo.inversefractional.com (medium risk - recent launch, uses cfo. subdomain)
2. qrcard.conventioncityseattle.com (medium-high risk - FIFA trails)

**Rationale:**
- Build confidence with multiple sites (app.modelcitizendeveloper.com already done in Phase 1)
- Validate multi-domain setup
- Test under different traffic patterns
- FIFA trails validated before high-stakes demo

**Note:**
- Main domain (inversefractional.com) stays on Canva - NO CHANGE
- Only migrating QRCards subdomains to Render
- cfo.inversefractional.com uses cfo. subdomain (not app. prefix)

**Time between deployments:** 24-48 hours each

---

### Phase 3: High-Value Site (After Validation)
**Site:** app.ivantohelpyou.com
**Timing:** Only after Phases 1-2 proven stable (1-2 weeks)
**Note:** Main domain (ivantohelpyou.com) stays on Canva - NO CHANGE

**Additional precautions:**
- Deploy during low-traffic hours
- Keep PythonAnywhere active for 1 week (parallel)
- Easy DNS rollback prepared (TTL=300)
- Monitor Decision Analysis service closely
- Test payment flows thoroughly

**Rollback triggers:**
- Any error in Decision Analysis service
- Response time degradation >20%
- Any customer complaints
- Database issues

---

## Updated Vikunja Task 221016

**OLD:** Deploy ivantohelpyou.com to Render
**NEW:** Deploy app.modelcitizendeveloper.com to Render (Quick Proof)

**Changes:**
- Lowest risk active site for initial validation
- app.ivantohelpyou.com deferred to Phase 3
- Same technical approach (subtree, Render)
- De-risks the entire migration

**Important Architecture Notes:**
- Main domains (*.com) stay on Canva - NO CHANGES
- Only migrating app subdomains (app.*.com) to Render
- taelyen.com has no QRCards app subdomain (just Canva homepage)

---

## Rollback Safety Net

**For each site:**
1. DNS TTL = 300 seconds (5 min rollback)
2. PythonAnywhere stays active during migration
3. Database backups before DNS change
4. Revert procedure documented and tested

**For ivantohelpyou.com specifically:**
- Parallel operation for 1 week minimum
- Monitor Decision Analysis usage daily
- Customer notification prepared (if needed)
- Financial reconciliation process ready

---

## Timeline (Revised)

**Week 1 (Nov 18-22):**
- Nov 18: Create qrcards-deploy repo
- Nov 19: Deploy modelcitizendeveloper.com to Render (Task 221016)
- Nov 20: Monitor modelcitizendeveloper.com (24h)
- Nov 21: Deploy cfo.inversefractional.com
- Nov 22: Monitor cfo.inversefractional.com (24h)

**Week 2 (Nov 25-29):**
- Nov 25: Deploy qrcard.conventioncityseattle.com
- Nov 27: Validate FIFA trails working
- Nov 29: Optional - Test adding taelyen.com (new domain setup)

**Week 3+ (Dec 2-9):**
- Dec 2: FIFA demo with trails on Render ✅
- Dec 5: Decision point - proceed with ivantohelpyou.com?
- Dec 9: Deploy ivantohelpyou.com (if all prior sites stable)
- Dec 16: Monitor ivantohelpyou.com for 1 week

**Final cutover:** Mid-December (after holiday risk period)

---

## Decision Analysis Service Protection

**Critical functionality on ivantohelpyou.com:**
- Decision matrix generation
- Payment processing
- User authentication
- Saved decision data

**Testing checklist before migration:**
- [ ] Create test decision matrix
- [ ] Test payment flow (test mode)
- [ ] Verify user login works
- [ ] Check decision data retrieval
- [ ] Test all saved decision features
- [ ] Validate email notifications
- [ ] Check analytics tracking

**Migration day checklist:**
- [ ] Backup all databases
- [ ] Notify paying customers (optional)
- [ ] Deploy during low-traffic window
- [ ] Test Decision Analysis immediately after DNS change
- [ ] Monitor error logs for 4 hours continuously
- [ ] Check payment processor for any issues

---

## Recommendation

Update Task 221016 from:
> "Quick Proof: Deploy **ivantohelpyou.com** to Render"

To:
> "Quick Proof: Deploy **modelcitizendeveloper.com** to Render"

**Rationale:**
- De-risk migration with lowest-risk active site
- Same technical validation (migrating live QRCards site)
- Allows confident iteration
- Protects paid Decision Analysis service
- ivantohelpyou.com deploys only after 3 other sites proven stable

**Testing New Domains:**
After app.modelcitizendeveloper.com is stable, can test adding additional domains (taelyen.com or others) to validate Render's multi-domain configuration, even if they're not migrating from PythonAnywhere.

**Future Homepage Migration:**
Eventually, main domain homepages could migrate from Canva to QRCards, but Canva's WYSIWYG editor provides excellent ease-of-use for now. This migration focuses on app subdomains only.

