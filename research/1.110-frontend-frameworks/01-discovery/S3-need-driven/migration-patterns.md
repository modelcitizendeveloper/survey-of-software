# S3 Need-Driven: Migration Patterns

**Methodology**: Cost and risk assessment for framework migration scenarios

**Date**: October 17, 2025

---

## Migration Scenarios

### Angular → React

**Typical scenario**: Modernizing legacy enterprise app

**Effort estimate** (50-component app):
- **Time**: 800-1,200 hours
- **Cost**: $100K-$150K (at $125/hr)
- **Risk**: High (rewrite business logic, re-test everything)
- **Timeline**: 4-6 months with 2 developers

**Migration approach**:
1. **Incremental** (recommended): Microfrontends, run Angular + React side-by-side
2. **Big bang**: Rewrite entire app (high risk)

**Recommendation**: Only migrate if Angular maintenance costs exceed migration investment ($150K)

---

### React → Svelte

**Typical scenario**: Performance optimization for consumer app

**Effort estimate** (50-component app):
- **Time**: 400-800 hours
- **Cost**: $50K-$100K
- **Risk**: Moderate (similar concepts, but ecosystem gaps)
- **Timeline**: 2-4 months with 2 developers

**ROI analysis**:
- **Performance gain**: 2.7x smaller bundles, 7% conversion increase
- **Break-even**: Need $71K+ monthly revenue to justify

**Recommendation**: Only migrate for high-traffic apps (>1M monthly users)

---

### Create React App → Next.js

**Typical scenario**: Adding SEO to existing React app

**Effort estimate** (50-component app):
- **Time**: 100-200 hours
- **Cost**: $12K-$25K
- **Risk**: Low (same framework, additive changes)
- **Timeline**: 2-4 weeks with 1 developer

**Migration steps**:
1. Install Next.js
2. Move components to `app/` directory
3. Add server-side data fetching
4. Test SSR/SSG behavior

**Recommendation**: Low-risk migration, high SEO value

---

## Key Findings

**Highest risk**: Angular → React (800-1,200 hours)
**Lowest risk**: CRA → Next.js (100-200 hours)
**Best ROI**: CRA → Next.js (low cost, high SEO value)

**Date compiled**: October 17, 2025
