# Architecture Clarifications (Nov 15, 2025)

**Created:** November 15, 2025  
**Status:** Documentation update  
**Context:** Critical architecture details discovered during planning

---

## Key Discovery: Split Domain Architecture

### Current Production Architecture

**ALL sites use split architecture:**
- **Main domain** → Canva homepage (WYSIWYG editor)
- **App subdomain** → QRCards on PythonAnywhere

**Examples:**
```
ivantohelpyou.com              → Canva homepage
app.ivantohelpyou.com          → QRCards (Decision Analysis service)

modelcitizendeveloper.com      → Canva homepage
app.modelcitizendeveloper.com  → QRCards (newsletter)

inversefractional.com          → Canva homepage
cfo.inversefractional.com      → QRCards (CFO demo/portfolio) ← subdomain pattern!

qrcard.conventioncityseattle.com → QRCards (FIFA trails - no Canva)
```

**Note:** inversefractional.com uses subdomain (cfo.) instead of prefix (app.)

---

## Migration Scope

### IN SCOPE (Migrating to Render)
- ✅ app.modelcitizendeveloper.com
- ✅ cfo.inversefractional.com (note: uses cfo. subdomain, not app.)
- ✅ qrcard.conventioncityseattle.com
- ✅ app.ivantohelpyou.com

**Total:** 4 QRCards app instances

### OUT OF SCOPE (Staying on Canva)
- ❌ ivantohelpyou.com (Canva homepage)
- ❌ modelcitizendeveloper.com (Canva homepage)
- ❌ inversefractional.com (Canva homepage - QRCards is on cfo. subdomain)
- ❌ taelyen.com (Canva only - no QRCards app)

**Rationale:** Canva's WYSIWYG editor provides excellent ease-of-use for homepage management

---

## DNS Configuration

### Current (PythonAnywhere)
```
# Main domain
ivantohelpyou.com → CNAME → Canva

# App subdomain
app.ivantohelpyou.com → CNAME → pythonanywhere-username.pythonanywhere.com
```

### After Migration (Render)
```
# Main domain (NO CHANGE)
ivantohelpyou.com → CNAME → Canva

# App subdomain (MIGRATED)
app.ivantohelpyou.com → CNAME → qrcards.onrender.com
```

**Key point:** Only app subdomain DNS changes, main domain unchanged

---

## Migration Risk Assessment (Corrected)

### Phase 1: Lowest Risk
**Site:** app.modelcitizendeveloper.com
- Newsletter site
- No critical functionality
- Low traffic
- Main domain stays on Canva

### Phase 2: Medium Risk
**Sites:**
1. cfo.inversefractional.com (recent launch - uses cfo. subdomain)
2. qrcard.conventioncityseattle.com (FIFA trails)

### Phase 3: Highest Risk
**Site:** app.ivantohelpyou.com
- Decision Analysis paid service ($$$)
- Revenue-generating
- Only after all others proven stable
- Main domain (ivantohelpyou.com) stays on Canva
- inversefractional.com (main domain) stays on Canva

---

## Initial Assumptions (Corrected)

### ❌ INCORRECT Assumption
- taelyen.com is lowest risk for migration

### ✅ CORRECTED Understanding
- taelyen.com has NO QRCards app (just Canva homepage)
- Not applicable for migration
- Can be used to TEST adding new domain to Render later

### ❌ INCORRECT Assumption
- Migrating entire domains (ivantohelpyou.com, modelcitizendeveloper.com, etc.)

### ✅ CORRECTED Understanding
- Only migrating QRCards subdomains
  - app.ivantohelpyou.com (uses app. prefix)
  - app.modelcitizendeveloper.com (uses app. prefix)
  - cfo.inversefractional.com (uses cfo. subdomain - different pattern!)
  - qrcard.conventioncityseattle.com (no Canva homepage)
- Main domains stay on Canva for homepage management
  - ivantohelpyou.com → Canva
  - modelcitizendeveloper.com → Canva
  - inversefractional.com → Canva

---

## Future Considerations

### Homepage Migration (Optional - Future)
Eventually, main domain homepages COULD migrate from Canva to QRCards, but:
- ❌ Not in current scope
- ❌ Not a priority (Canva WYSIWYG works great)
- ✅ Focus on app subdomain migration first
- ✅ Validate Render stability before considering

### New Domain Testing
After migration complete, can test adding taelyen.com to Render to validate:
- Multi-domain configuration
- Setting up NEW domains (not migrating existing)
- Render's domain management capabilities

---

## Documentation Updates Made

### Files Updated (Nov 15, 2025)
1. **00_README.md** - Added split architecture explanation
2. **01_MIGRATION_PLAN_V2_SUBTREE.md** - Updated all domain references to app subdomains
3. **07_MIGRATION_PRIORITY.md** - Corrected risk assessment with subdomain architecture
4. **08_ARCHITECTURE_CLARIFICATIONS.md** - This document (new)

### Key Changes
- ✅ All references changed from `ivantohelpyou.com` to `app.ivantohelpyou.com`
- ✅ All references changed from `modelcitizendeveloper.com` to `app.modelcitizendeveloper.com`
- ✅ Corrected `app.cfo.inversefractional.com` to `cfo.inversefractional.com` (uses cfo. not app.)
- ✅ Added notes: "Main domain stays on Canva - NO CHANGE"
- ✅ Clarified inversefractional.com (Canva) vs cfo.inversefractional.com (QRCards)
- ✅ Updated DNS instructions to only modify subdomain CNAME
- ✅ Clarified taelyen.com is not applicable for migration

---

## Implementation Impact

### No Change to Technical Approach
- ✅ Git subtree strategy: UNCHANGED
- ✅ Render deployment: UNCHANGED
- ✅ GitHub Actions sync: UNCHANGED
- ✅ Subtree ROI analysis: UNCHANGED

### Only Change: Domain Scope
- ✅ Migrating 4 app subdomains (not 5 full domains)
- ✅ DNS changes limited to subdomain CNAMEs
- ✅ Zero impact to Canva homepages
- ✅ Easier rollback (only subdomain DNS)

### Timeline Impact
- ✅ No change to timeline
- ✅ No change to effort estimates
- ✅ Actually SIMPLER (subdomain-only migration)

---

## Vikunja Task Updates

### Task 221016 (Current)
**Title:** Quick Proof: Deploy ivantohelpyou.com to Render

**Should be:** Quick Proof: Deploy app.modelcitizendeveloper.com to Render

**Note:** Task description needs manual update to reflect:
1. Subdomain deployment (app.modelcitizendeveloper.com)
2. Main domain stays on Canva
3. Changed from app.ivantohelpyou.com (too risky) to app.modelcitizendeveloper.com (lowest risk)

---

## Summary

**What we learned:**
1. All sites use main domain (Canva) + app subdomain (QRCards) architecture
2. Only app subdomains need migration to Render
3. taelyen.com has no QRCards app (not applicable for migration)
4. Main domains stay on Canva for easy homepage management
5. Migration is actually SIMPLER than initially planned (subdomain-only)

**Impact:**
- ✅ Documentation updated to reflect subdomain architecture
- ✅ Risk assessment corrected (app.modelcitizendeveloper.com is lowest risk)
- ✅ DNS changes scoped to subdomain CNAMEs only
- ✅ Zero impact to Canva homepages
- ✅ Easier rollback strategy

**Next steps:**
- ⏭️ Proceed with migration as planned
- ⏭️ Start with app.modelcitizendeveloper.com (lowest risk)
- ⏭️ Only modify app subdomain DNS
- ⏭️ Verify main domains stay on Canva after migration
