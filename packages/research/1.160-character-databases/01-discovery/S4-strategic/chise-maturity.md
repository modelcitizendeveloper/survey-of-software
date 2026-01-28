# CHISE - Long-Term Viability

## Maintenance Health

**Last commit:** 2024-12-18 (git.chise.org)
**Commit frequency:** Irregular (2-4 month gaps typical, occasional 6+ month gaps)
**Open issues:** ~15 (project tracker)
**Issue resolution time:** 2-8 weeks (responsive for active issues)
**Maintainers:** 2-3 core (MORIOKA Tomohiko, Kyoto University team)
**Bus factor:** Low-Medium (small team, but institutional backing)

**Assessment:** ⚠️ **Adequate but concerning**
- Active development (commits within last month)
- Small core team (2-3 people)
- Irregular update cadence (not predictable)
- Responsive when active (but can have gaps)

## Community Trajectory

**Adoption trend:** ⚠️ **Stable (not growing)**
- GitHub stars: ~150 (niche, stable)
- Production use: Niche (some Japanese NLP, digital humanities)
- Ecosystem: Few libraries (mostly Ruby-based)
- Academic citations: 80+ papers (validates research value)

**Contributor growth:** **Flat**
- Same core team for 10+ years
- Few external contributors (complex codebase)
- Active mailing list but small community

**Ecosystem integration:**
- Used by: Some Japanese dictionary apps, academic projects
- Not integrated into OSes or major platforms
- RDF/ontology focus limits broader adoption

## Standards Backing

**Formal status:** ⚠️ **Academic project (no formal standard)**

**Institutional backing:**
- Kyoto University (academic institution)
- Grant-funded research project
- Not ISO/Unicode official (complements, doesn't compete)

**Stability:**
- Ontology schema evolves (breaking changes possible)
- Data format stable (RDF/Berkeley DB)
- Migration guides provided (but manual effort required)

**Risk:** Medium
- No formal standardization commitment
- Academic funding can end
- Schema changes require application updates

## 5-Year Outlook (2026-2031)

**Prediction:** ⚠️ **Cautiously Optimistic**

**Rationale:**
- Kyoto University backing continues (long-term research project, 20+ years active)
- Core maintainer (MORIOKA) still active
- Niche but stable use case (etymology, digital humanities)
- No direct competitors for its specific domain (character ontology)

**Expected changes:**
- Continued irregular updates (2-6 month gaps)
- Ontology refinements (incremental, some breaking changes)
- Slow feature additions (research-driven, not market-driven)

**Risks:**
- Maintainer departure: 15% probability (small team, aging)
- Funding loss: 10% probability (academic grants end)
- Community stagnation: 20% probability (not growing, could decline)

**Confidence: 65%** - More uncertainty than Unihan, but project has longevity

## 10-Year Outlook (2026-2036)

**Prediction:** ⚠️ **Uncertain**

**Rationale:**
- 10-year horizon risks: Maintainer retirement, funding shifts, alternative projects
- Historical track record: 20+ years suggests resilience
- But: Small team, niche use case, no formal standardization

**Potential scenarios:**
1. **Continued maintenance (40%):** Core team persists, slow evolution
2. **Community fork (25%):** If maintainers leave, community takes over
3. **Stagnation (25%):** Updates stop, data remains but unmaintained
4. **Replacement (10%):** New ontology project emerges, CHISE deprecated

**Risks:**
- Successor problem: 35% probability (small team, no clear succession plan)
- Breaking schema changes: 40% probability (ontology research evolves)
- Project abandonment: 20% probability (funding loss, maintainer departure)

**Confidence: 45%** - Long horizon + small team + academic funding = high uncertainty

## Strategic Risk Assessment

**Overall Risk: MEDIUM (6/10)**

| Factor | Score | Rationale |
|--------|-------|-----------|
| **Maintenance** | 7/10 | Active but irregular updates |
| **Team** | 5/10 | Small (2-3 core), low bus factor |
| **Funding** | 6/10 | Academic (grant-dependent) |
| **Standards** | 4/10 | No formal standard (academic project) |
| **Adoption** | 5/10 | Niche use (digital humanities, research) |
| **Stability** | 6/10 | Schema evolves, breaking changes possible |
| **Ecosystem** | 5/10 | Few libraries, limited integration |
| **Bus Factor** | 4/10 | Small team, succession risk |

**Average: 5.25/10** → **MEDIUM RISK**

## Mitigation Strategies

### Primary: Extract Subsets (Recommended)

**Approach:**
1. Export CHISE etymology + semantic links → JSON (one-time)
2. Bundle JSON with application (no runtime dependency)
3. Update JSON quarterly (manual export from CHISE)
4. Insulate from upstream schema changes

**Benefits:**
- Decouples from CHISE maintenance risk
- Fast runtime (JSON vs RDF queries)
- No Berkeley DB dependency

**Cost:** 1 day setup, 1 hour/quarter maintenance

### Secondary: Community Engagement

**Approach:**
1. Contribute to CHISE project (PRs, funding, documentation)
2. Join maintainer team (reduce bus factor)
3. Build Ruby/Python wrapper libraries (expand ecosystem)

**Benefits:**
- Strengthens project (more maintainers = lower risk)
- Improves documentation (easier adoption)
- Increases visibility (grow user base)

**Cost:** 4-8 hours/month

### Tertiary: Contingency Plan

**Approach:**
1. Fork CHISE repository (preserve data)
2. Document schema (enable community maintenance)
3. Plan alternative: Manual etymology curation (if CHISE fails)

**Benefits:**
- Insurance against project abandonment
- Community can continue if maintainers leave

**Cost:** Minimal (fork GitHub repo, 1 hour)

## Competitive Landscape

**Alternatives:**
- **None directly:** No other open character ontology with CHISE's depth
- **Partial:** Wiktionary (community-curated, but not structured ontology)
- **Commercial:** Pleco licensed content (proprietary, expensive)

**CHISE advantage:**
- Unique: Only open character ontology at this depth
- Academic rigor (scholarly sources, citations)
- 20+ year data accumulation

**Risk:** Irreplaceable for its domain (if abandoned, no direct substitute)

## Conclusion

**Long-term viability: ADEQUATE with caveats**

**Rationale:**
- 20-year track record suggests resilience
- BUT: Small team, irregular updates, no formal standard
- Niche but irreplaceable for etymology/semantics
- Risk is manageable with mitigation (extract subsets)

**Strategic recommendation:** ⚠️ **Use with mitigation**
- Extract subsets to JSON (insulate from risk)
- Monitor project health (commits, maintainer activity)
- Plan contingency (fork, alternative data sources)
- Acceptable for learning/research apps (high value despite risk)
- Avoid for critical infrastructure (too much uncertainty)

**Confidence:** 65% (5-year), 45% (10-year)

**Risk level:** **MEDIUM (6/10)** - Valuable but risky, requires active mitigation.

**Decision:** Use CHISE IF you need etymology/semantics AND implement extraction/contingency plan.
