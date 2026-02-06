# S4 Strategic Selection - Recommendation

## Risk Ranking (5-10 Year Viability)

| Rank | Database | Risk Score | 5-Year Confidence | 10-Year Confidence | Strategic Assessment |
|------|----------|-----------|------------------|-------------------|---------------------|
| **1** | Unihan | 9.75/10 (LOW) | 95% | 75% | ✅ Safest choice, mandatory foundation |
| **2** | IDS | 9.9/10 (LOW) | 95% | 80% | ✅ Equally safe, part of Unicode |
| **3** | CJKVI | 9.4/10 (LOW) | 90% | 70% | ✅ Safe, multi-vendor backed |
| **4** | CHISE | 5.25/10 (MED) | 65% | 45% | ⚠️ Risky but mitigatable |

## Strategic Analysis

### Tier 1: Infrastructure-Safe (Unihan, IDS, CJKVI)

**Common characteristics:**
- Standards-backed (Unicode/ISO official)
- Multi-organization maintenance
- 10-20 year track records
- Biannual to quarterly updates
- Production use at billions-of-users scale
- Strong backward compatibility

**Strategic verdict:** ✅ **Use without hesitation**
- Plan: Integrate and rely on for 5-10 year horizon
- Maintenance: Biannual/quarterly upgrades (low-effort)
- Risk mitigation: None required (risk <5%)

**Confidence:** 90%+ (5-year), 70-80% (10-year)

### Tier 2: Valuable but Risky (CHISE)

**Characteristics:**
- Academic backing (not standards body)
- Small team (2-3 maintainers)
- Irregular updates (3-6 month gaps)
- Niche production use
- Irreplaceable for specific domain (etymology/ontology)

**Strategic verdict:** ⚠️ **Use with active mitigation**
- Plan: Extract subsets, don't depend on runtime RDF queries
- Maintenance: Monitor project health, have contingency
- Risk mitigation: **Required** (extraction, fork plan, alternatives)

**Confidence:** 65% (5-year), 45% (10-year)

## Long-Term Selection Strategy

### Decision Rule 1: Always include Tier 1 databases for their domains

**Unihan:** Always (mandatory foundation)
**IDS:** If structural decomposition needed (IME, learning, handwriting)
**CJKVI:** If multi-locale (PRC/TW/HK/JP)

**Rationale:** Risk is negligible (<5%), all are safe long-term bets

### Decision Rule 2: Include CHISE only with mitigation

**IF you need etymology/semantics:**
1. ✅ Evaluate alternative: Manual curation, licensed content (Pleco)
2. ✅ If CHISE is optimal: Extract subsets to JSON
3. ✅ Avoid runtime RDF dependency
4. ✅ Plan contingency (fork, community maintenance)

**Don't use CHISE if:**
- MVP/prototype (defer to v2)
- Critical infrastructure (too much risk)
- No etymology/semantics need (unnecessary complexity)

### Decision Rule 3: Prefer standards over research projects

**When choosing between:**
- IDS (Unicode TR37) vs CHISE IDS (richer but non-standard)
  → **Choose IDS** (standard, safer)
- Unihan variants vs CHISE variants
  → **Choose Unihan** (standard, safer)
- CJKVI IVD vs CHISE glyphs
  → **Choose CJKVI** (ISO standard, safer)

**Only use CHISE when:** No standard alternative exists (etymology, semantic ontology)

## Risk Mitigation Hierarchy

### Low-Risk Databases (Unihan, IDS, CJKVI)

**Mitigation: Trust but verify**
- Monitor: Subscribe to Unicode/IVD release announcements
- Upgrade: Plan biannual (Unihan/IDS) or quarterly (CJKVI) updates
- Test: Regression tests for data schema changes
- Contingency: None needed (risk <5%, but keep backups)

**Effort:** 1 hour/quarter

### Medium-Risk Databases (CHISE)

**Mitigation: Active insulation**

**Tier 1 (Required):**
1. **Extract subsets:** Export etymology + semantic links → JSON
   - One-time: 1 day setup
   - Maintenance: 1 hour/quarter (re-export if CHISE updates)
   - Benefit: Decouples from CHISE runtime risk

2. **Monitor project health:**
   - Track: git.chise.org commits, mailing list activity
   - Frequency: Monthly check
   - Trigger: If 6+ months no commits → activate contingency

**Tier 2 (Recommended):**
3. **Fork repository:** Preserve data in case of abandonment
   - Effort: 10 minutes (fork on GitHub)
   - Benefit: Community can continue if maintainers leave

4. **Document schema:** Enable future community maintenance
   - Effort: 4 hours (write schema guide)
   - Benefit: Lowers barrier for new maintainers

**Tier 3 (Optional):**
5. **Contribute:** Join maintainer team, reduce bus factor
   - Effort: 4-8 hours/month
   - Benefit: Strengthens project, improves your control

**Effort:** 1 day (Tier 1) + 4 hours (Tier 2) = 1.5 days one-time, 1 hour/quarter ongoing

## Funding & Organizational Sustainability

### Highly Sustainable (Unihan, IDS, CJKVI)

**Funding model:**
- Unicode Consortium: Membership-funded (Apple, Google, Microsoft, Adobe, IBM, Oracle, etc.)
- Diversified revenue: 100+ member companies
- 40-year track record (Unicode founded 1987)

**Risk assessment:** Consortium dissolution probability <1% (too embedded in digital infrastructure)

**IVD (CJKVI):**
- Vendor-supported: Adobe, Google, Apple, Microsoft fund font development
- Commercial incentive: Professional publishing market (billions in revenue)
- Self-sustaining: Vendors need IVD for product differentiation

**Risk assessment:** Vendor exit probability 2% per vendor, but 4+ major vendors = <0.5% all-exit risk

### Moderately Sustainable (CHISE)

**Funding model:**
- Academic grants: Japanese govt, research foundations
- Grant-dependent: Funding cycles 3-5 years, renewal uncertain

**Risk assessment:**
- Grant renewal probability: 70-80% (project has 20-year track record)
- Succession risk: 20-30% (small team, aging maintainers)
- Mitigation: Community fork possible (open source, GPL)

**Contingency:** If funding ends, data remains valid (characters don't change). Community can maintain read-only archive.

## 10-Year Scenarios

### Scenario A: Stable Evolution (70% probability)

**Prediction:**
- Unihan, IDS, CJKVI continue biannual/quarterly updates
- CHISE continues with irregular updates (3-6 month gaps)
- No major disruptions, incremental improvements

**Action:** Maintain current strategy, plan periodic upgrades

### Scenario B: CHISE Stagnation (20% probability)

**Prediction:**
- CHISE updates stop (maintainers retire, funding ends)
- Data remains valid but unmaintained
- Community fork emerges (or doesn't)

**Action:**
- Extraction strategy succeeds (data already in JSON, no impact)
- Community fork if needed (contribute to successor project)
- Worst case: Use last CHISE version (etymology doesn't change)

### Scenario C: Unicode Disruption (5% probability)

**Prediction:**
- New encoding standard emerges (extremely unlikely, but 10-year horizon)
- Unicode remains but evolves significantly
- Requires migration effort

**Action:**
- Monitor standards bodies (W3C, Unicode)
- Plan migration if needed (10-year warning typical)
- Unlikely to affect applications (backward compatibility strong)

### Scenario D: AI Transformation (5% probability)

**Prediction:**
- AI-generated character data (embeddings, semantic models)
- Traditional databases complemented by learned models
- CHISE becomes less critical (AI learns etymology from corpus)

**Action:**
- Hybrid approach: Traditional databases + AI models
- CHISE remains useful for explicit knowledge (not learned)
- No disruption, just expansion of available tools

## Final Strategic Recommendation

### Core Stack (95% of Applications)

**Databases:** Unihan + IDS (if structural) + CJKVI (if multi-locale)

**Rationale:**
- All three: Low risk (9-10/10), safe 5-10 year bets
- Standards-backed, multi-vendor/organization
- Proven at billions-of-users scale
- Minimal maintenance burden

**Confidence:** 90%+ (5-year), 75%+ (10-year)

### Extended Stack (5% of Applications)

**Databases:** Core + CHISE (with extraction)

**Rationale:**
- CHISE: Risky (6/10) but irreplaceable for etymology
- Mitigation required: Extract to JSON, monitor health
- Acceptable for learning/research (high value despite risk)

**Confidence:** 65% (5-year), 45% (10-year)
**Mitigation cost:** 1.5 days setup, 1 hour/quarter maintenance

## Monitoring Strategy

### Quarterly Health Check (30 minutes)

**Unihan/IDS:**
- Check: unicode.org/Public/ for new releases
- Action: Plan upgrade if new version (biannual)
- Alert: If release missed (never happened)

**CJKVI (IVD):**
- Check: unicode.org/ivd/ for updates
- Action: Plan upgrade if new sequences (quarterly)
- Alert: If 6+ months no update (unusual)

**CHISE:**
- Check: git.chise.org commits, mailing list
- Action: Re-export if schema changes (rare)
- Alert: If 6+ months no commits → activate contingency

### Annual Strategy Review (2 hours)

**Assess:**
- Are databases still maintained?
- Has project health changed (better/worse)?
- New alternatives emerged?
- Should mitigation strategy change?

**Decision:** Continue, escalate contingency, or migrate to alternative

## Conclusion

**Strategic verdict:** Unihan/IDS/CJKVI are safe long-term dependencies. CHISE is valuable but risky—use with extraction mitigation.

**Risk-adjusted recommendation:**
1. **Always use:** Unihan (mandatory)
2. **Use if needed:** IDS (structure), CJKVI (multi-locale) - both safe
3. **Use cautiously:** CHISE (etymology) - extract subsets, monitor health

**Confidence:** High for Tier 1 (90%+ 5-year), Medium for CHISE (65% 5-year)

**Maintenance burden:** Minimal (1 hour/quarter for all four databases with extraction)

**Strategic risk:** Low (Tier 1 safe, CHISE risk mitigated via extraction)

**Verdict:** The four-database stack is strategically sound for 5-10 year horizon with appropriate risk management.
