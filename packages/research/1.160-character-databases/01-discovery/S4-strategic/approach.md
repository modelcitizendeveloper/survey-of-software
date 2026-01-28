# S4: Strategic Selection - Approach

## Methodology: Long-Term Viability Assessment

**Time Budget:** 15 minutes
**Philosophy:** "Think long-term and consider broader context"
**Goal:** Assess 5-10 year sustainability, maintenance health, and strategic risk for each database
**Outlook:** 2026-2036 timeframe

## Analysis Dimensions

### 1. Maintenance Health

**Signals to assess:**
- **Activity:** Commit frequency, last update, issue resolution speed
- **Team:** Number of maintainers, bus factor, organizational backing
- **Responsiveness:** Time to address critical bugs, security issues
- **Breaking changes:** Frequency, migration path quality

**Risk levels:**
- **Low:** Active org (Unicode, ISO), 5+ maintainers, biannual updates
- **Medium:** Active project, 2-4 maintainers, irregular updates
- **High:** Single maintainer, 6+ month gaps, declining activity

### 2. Community Trajectory

**Metrics:**
- **Adoption trend:** Growing, stable, or declining usage
- **Ecosystem:** Libraries, tools, integrations built on top
- **Documentation:** Quality improvements, tutorial growth
- **Contributor growth:** New contributors joining

**Indicators:**
- **Growing:** GitHub stars ↑, new libraries, active discussions
- **Stable:** Mature ecosystem, consistent activity, maintained but not expanding
- **Declining:** Issue backlog growing, contributors leaving, forks without merges

### 3. Standards Backing

**Formal standards:**
- **Unicode official:** TR38 (Unihan), TR37 (IDS)
- **ISO standards:** ISO/IEC 10646 IVD (CJKVI)
- **Academic institutions:** CHISE (Kyoto University)

**Value of standards backing:**
- Long-term stability (standards evolve slowly)
- Multi-vendor support (no single-company risk)
- Backward compatibility commitments

**Risk without standards:**
- Project can be abandoned (no formal obligation to maintain)
- Breaking changes (no compatibility guarantees)
- Vendor lock-in (proprietary formats)

### 4. Ecosystem Momentum

**Adoption signals:**
- **Production use:** Fortune 500 companies, government agencies
- **Platform integration:** Built into OSes (Windows, macOS, Linux, Android, iOS)
- **Academic citations:** Research papers, textbooks
- **Training materials:** Tutorials, courses, books

**Momentum types:**
- **Network effect:** More users → more tools → more users (positive feedback)
- **Stagnation:** Mature, no growth, maintained but not expanding
- **Decline:** Users migrating away, alternatives emerging

### 5. Data Longevity

**Stability analysis:**
- **Historical data:** Does old data remain valid?
- **Update frequency:** Too fast (breaking changes) vs too slow (stale data)
- **Format stability:** File formats, schema changes, migration burden

**Best: Additive-only changes**
- Unicode: Codepoints never change (stability policy)
- Unihan: Properties added, rarely removed
- CHISE: Schema evolves, but data preserved

**Worst: Frequent rewrites**
- Breaking schema changes every year
- Migration scripts required
- Backward compatibility not guaranteed

### 6. Funding & Organizational Risk

**Backing types:**
- **Consortium (Low Risk):** Unicode, ISO (membership-funded, multi-organization)
- **Academic (Medium Risk):** University projects (grant-dependent, but long-term)
- **Corporate (Medium Risk):** Company-backed (risk if company exits market)
- **Individual (High Risk):** Single-maintainer OSS (bus factor = 1)

**Sustainability indicators:**
- **Funding model:** Grants, donations, membership fees
- **Succession plan:** Documented maintainer onboarding
- **Institutional memory:** Documentation, decision rationale

## Time Horizons

### 5-Year Outlook (2026-2031)

**Questions:**
- Will this database still be actively maintained?
- Will it support new Unicode versions?
- Will the ecosystem grow or shrink?

**Threshold:** 75% confidence database remains viable

### 10-Year Outlook (2026-2036)

**Questions:**
- Will this database exist in recognizable form?
- Will standards compatibility be maintained?
- Will alternatives replace it?

**Threshold:** 50% confidence (longer horizon = higher uncertainty)

## Risk Assessment Framework

### Low Risk (Score: 8-10/10)

- Standards-backed (Unicode, ISO)
- 5+ active maintainers
- Biannual or more frequent updates
- Production use at scale (billions of users)
- Formal stability policies

### Medium Risk (Score: 5-7/10)

- Academic or community-backed
- 2-4 active maintainers
- Irregular updates (3-12 month gaps)
- Niche production use (thousands-millions of users)
- Informal stability practices

### High Risk (Score: 2-4/10)

- Individual maintainer
- Infrequent updates (12+ month gaps)
- Small user base (hundreds of users)
- No successor plan
- Breaking changes common

## Comparative Analysis

**Relative risk assessment:**
- Which database is most/least risky long-term?
- Which has best/worst funding sustainability?
- Which has strongest/weakest ecosystem?

**Trade-off identification:**
- High-risk but irreplaceable (CHISE for etymology)
- Low-risk but limited features (Unihan)
- Medium-risk with alternatives (IDS can be replaced by CHISE IDS)

## Mitigation Strategies

### For High-Risk Dependencies

**Options:**
1. **Extract subsets:** Pull data into static JSON (insulate from upstream changes)
2. **Fork:** Maintain own version if project abandoned
3. **Contribute:** Join maintainer team, reduce bus factor
4. **Alternatives:** Plan fallback to alternative database
5. **Vendor licensing:** Pay for commercial support (if available)

### For Medium-Risk Dependencies

**Options:**
1. **Monitor health:** Track commits, issues, maintainer activity
2. **Engage community:** Submit PRs, documentation, funding
3. **Contingency plan:** Document migration path to alternatives

### For Low-Risk Dependencies

**Strategy:** Trust but verify
- Use as-is
- Track major version updates
- Plan periodic upgrades (biannual)

## Time Allocation

- **4 min:** Maintenance health assessment (all four databases)
- **3 min:** Community trajectory analysis
- **3 min:** Standards backing validation
- **3 min:** Risk scoring and comparison
- **2 min:** Mitigation recommendations

**Total: 15 minutes**

## Output Structure

### Per Database
1. **Maintenance Health:** Commit activity, maintainer team
2. **Community Trajectory:** Growing/stable/declining
3. **Standards Backing:** Formal standardization status
4. **5-Year Outlook:** Viability prediction + confidence
5. **10-Year Outlook:** Long-term prediction + confidence
6. **Strategic Risk:** Low/medium/high + mitigation

### Final Recommendation
- Rank databases by long-term viability
- Identify safest choices (low-risk baseline)
- Identify risky but valuable (high-risk, high-reward)
- Mitigation strategies for selected stack

---

**S4 Strategic Selection methodology defined.** Proceeding to viability assessments.
