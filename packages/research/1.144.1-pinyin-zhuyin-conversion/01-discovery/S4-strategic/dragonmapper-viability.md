# dragonmapper - Strategic Viability Assessment

## Executive Summary
**Risk Level**: MODERATE-HIGH
**Confidence**: MODERATE for 3-5 year horizon
**Recommendation**: Use with caution; have fork/migration plan ready

dragonmapper is a mature but minimally maintained project. While the code is stable and functional, the low activity level raises concerns for long-term sustainability. Suitable for non-critical applications or when combined with contingency planning.

## Maintenance & Activity (2025-2026)

### Recent Releases
- **v0.2.6**: Last stable release (date unclear, likely 2023 or earlier)
- **v0.2**: Major version from 2014-2015 era
- **Cadence**: Minimal (no recent major updates)

### Development Activity
- **2025 Activity**: Classified as "INACTIVE" by Snyk (October 2025)
- **Past month** (as of analysis): No pull request activity
- **Issues**: Multiple open issues from 2020-2025, many unresolved
  - Issue #44: Opened July 27, 2025 (still open)
  - Issue #39: Opened May 24, 2024 (still open)
- **Status**: Minimally maintained or abandoned

### Community Health
- **GitHub Stars**: ~300-400 (modest visibility)
- **Contributors**: Small number (appears to be 1-2 primary)
- **PyPI Downloads**: Minimal compared to pypinyin
- **Package Health**: INACTIVE maintenance status (Snyk)

**Sources**:
- [GitHub Repository](https://github.com/tsroten/dragonmapper)
- [Snyk Package Analysis](https://snyk.io/advisor/python/dragonmapper)
- [PyPI Package](https://pypi.org/project/dragonmapper/)

## Maintainer Analysis

### Primary Maintainer
- **Name**: Thomas Roten (tsroten)
- **GitHub**: https://github.com/tsroten
- **Recent activity**: Minimal (no visible 2025 commits)
- **Other projects**: Multiple Python projects, unclear activity levels

### Bus Factor Assessment
- **Current bus factor**: 1 (single maintainer)
- **Risk**: HIGH
- **Mitigation**: Few to none

**Critical Concern**: Project appears to be effectively unmaintained. Primary maintainer has not been responsive to recent issues.

## Data Dependencies

### Data Sources
1. **CC-CEDICT**: Chinese-English dictionary
   - Third-party, community-maintained
   - Loaded into memory by dragonmapper
   - Risk: LOW (CC-CEDICT is well-maintained independently)

2. **Unihan Database**: Unicode Han character database
   - Maintained by Unicode Consortium
   - Stable, authoritative source
   - Risk: LOW (official Unicode data)

### Data Sustainability
- ✅ Data sources are external and well-maintained
- ✅ CC-CEDICT and Unihan are stable, long-term projects
- ⚠️ dragonmapper's bundled data may become outdated
- ❌ No mechanism for automatic data updates

**Verdict**: Data sources are sustainable, but dragonmapper won't benefit from data updates without releases.

## Ecosystem Position

### Dependent Projects
- Limited visibility into dependent projects
- Likely used in specialized applications (linguistics, research)
- Not widely adopted as infrastructure

### Alternatives
Based on research, alternatives include:
- **python-pinyin-jyutping-sentence**: Different scope (includes Jyutping)
- **g2pC**: Context-aware grapheme-to-phoneme for Chinese
- **pypinyin**: Overlaps in Pinyin/Zhuyin but different direction

**Key Point**: dragonmapper's unique value is Pinyin ↔ Zhuyin conversion. Few direct competitors for this specific feature.

### Industry Adoption
- Appears to be niche adoption
- Used in academic/research contexts
- Lower commercial adoption than pypinyin

**Verdict**: dragonmapper is useful but not critical infrastructure. Its disappearance would be noticed but not catastrophic.

## Risk Assessment

### Existential Risks
1. **Maintainer abandonment**: HIGH
   - Already appears abandoned based on activity
   - No evidence of maintenance transfer
   - Mitigation: Fork immediately if using in production

2. **Data source decay**: MODERATE
   - CC-CEDICT continues independently (good)
   - dragonmapper won't pull updates (bad)
   - Unicode updates may break compatibility (possible)

3. **Python ecosystem changes**: MODERATE-HIGH
   - Compatible with older Python versions
   - May break with Python 3.13+ changes (no maintainer to fix)
   - Dependencies may become incompatible

4. **Licensing changes**: LOW
   - MIT license (stable, permissive)
   - Unlikely to change

5. **Competition**: MODERATE
   - pypinyin could add direct Pinyin ↔ Zhuyin conversion
   - New libraries could emerge
   - But conversion logic is simple (forkable)

### Technical Debt Indicators
- ⚠️ **CI/CD**: Unknown status
- ⚠️ **Test coverage**: Exists but not actively maintained
- ✅ **Documentation**: Good (readthedocs) but static
- ✅ **Code quality**: Clean, readable
- ✅ **Dependencies**: Minimal (good for forking)

**Verdict**: Low technical debt in code itself, but lack of maintenance creates growing debt vs Python ecosystem.

## Sustainability Score

| Factor | Score (1-5) | Weight | Weighted Score |
|--------|-------------|--------|----------------|
| **Maintenance activity** | 1 | 20% | 0.2 |
| **Community size** | 2 | 15% | 0.3 |
| **Bus factor** | 1 | 15% | 0.15 |
| **Financial sustainability** | 1 | 10% | 0.1 |
| **Data source stability** | 4 | 10% | 0.4 |
| **Ecosystem position** | 2 | 15% | 0.3 |
| **Technical debt** | 3 | 10% | 0.3 |
| **License stability** | 5 | 5% | 0.25 |
| **TOTAL** | | **100%** | **2.0 / 5.0** |

**Overall Rating**: **Moderate/Poor** (2.0/5.0)

## Long-Term Scenarios

### Best Case (30% probability)
- Maintainer returns or hands off to new maintainer
- Project revived with updates
- Continues for 3-5 years

**Action**: Monitor for signs of revival, use if revived

### Base Case (50% probability)
- Project remains in maintenance mode (works but no updates)
- Compatible with Python 3.x through ~3.11
- Breaks on Python 3.14+ or dependency updates
- Community fork may emerge

**Action**: Use with caution, have fork plan ready, abstract behind internal API

### Worst Case (20% probability)
- No revival, no community fork
- Becomes incompatible with modern Python (3.13+)
- Must fork internally or migrate away

**Action**: Fork preemptively if critical, or plan migration to alternatives

## Strategic Recommendations

### For Different Risk Tolerances

**Conservative Organizations** (low risk tolerance):
- ⚠️ **AVOID** for new projects
- **If already using**: Plan migration or fork
- **Mitigation**: Maintain internal fork immediately
- **Timeline**: Migrate within 1-2 years

**Moderate Risk Tolerance**:
- ⚠️ **Use with caution**
- Abstract behind internal API (easy migration)
- Have fork strategy ready
- Monitor for Python compatibility issues
- Budget for migration in 2-3 years

**High Risk Tolerance** (startups, experiments):
- ✅ **OK for non-critical use**
- Transcription conversion logic is simple
- Easy to fork or reimplement if needed
- Not worth worrying about

### Fork Strategy (RECOMMENDED)

**If dragonmapper is critical to your project:**

**Phase 1 - Immediate** (Month 0):
1. Fork to internal repository
2. Set up CI/CD for your fork
3. Document customizations
4. Test with current Python versions

**Phase 2 - Ongoing** (Quarterly):
1. Monitor upstream for unlikely revival
2. Test fork against new Python versions
3. Update dependencies as needed
4. Cherry-pick any upstream fixes (if any)

**Phase 3 - Long-term** (Year 2+):
1. Decide: maintain fork or migrate
2. If migrating: evaluate alternatives (pypinyin + custom, new libs)
3. If maintaining: ensure team bandwidth

### Alternative: Migrate Away

**Option 1**: pypinyin + Custom Logic
- Use pypinyin for character conversion
- Write custom Pinyin ↔ Zhuyin conversion (not complex)
- Pros: More active project, reduces dependencies
- Cons: Need to implement transcription conversion yourself

**Option 2**: Vendor dragonmapper
- Copy dragonmapper source into your project
- Maintain as internal module
- Pros: Full control, no dependency
- Cons: More code to maintain

**Option 3**: Wait for Alternatives
- Monitor for new libraries
- May emerge as dragonmapper decays
- Pros: Better long-term solution
- Cons: May not happen, creates limbo

## 3-5 Year Outlook

### 2026-2028 Prediction
- **Maintenance**: Unlikely to resume (already inactive)
- **Python versions**: May break on Python 3.13+ (no one to fix)
- **Community fork**: Possible but uncertain (depends on adoption level)
- **Position**: Niche, possibly obsolete

**Confidence**: MODERATE (60%)

### When dragonmapper Breaks

**Most likely breaking changes:**
1. Python 3.13+ changes to core libraries
2. Dependency updates (pip, setuptools)
3. Unicode database format changes
4. Changes to CC-CEDICT structure

**Your responsibility** if using:
- Monitor Python release notes
- Test with new Python versions early
- Have migration/fork plan ready

## Practical Fork Guide

### If You Must Fork dragonmapper

**When to fork:**
- If it's critical to your application
- If migration is too costly
- If you have Python expertise in-house

**How to fork:**
```bash
# 1. Fork on GitHub
git clone https://github.com/YOUR-ORG/dragonmapper
cd dragonmapper

# 2. Set up development environment
python -m venv venv
source venv/bin/activate
pip install -e .[dev]

# 3. Run tests
pytest

# 4. Update dependencies
pip-compile requirements.in

# 5. Test with target Python version
tox -e py313

# 6. Publish to internal PyPI or vendor directly
```

**Maintenance burden**: LOW (simple codebase, minimal dependencies)

**Ongoing effort**: ~4-8 hours per year (test new Python versions, update deps)

## Comparison to pypinyin Viability

| Factor | pypinyin | dragonmapper |
|--------|----------|--------------|
| **Maintenance** | Active | Inactive |
| **Community** | Large | Small |
| **Bus factor** | 2-3 | 1 |
| **Risk level** | LOW | MODERATE-HIGH |
| **3-5 year confidence** | HIGH | MODERATE |
| **Recommendation** | Use freely | Use with caution |

## Conclusion

**dragonmapper is a MODERATE-HIGH RISK choice for long-term projects.**

**Strengths:**
- ✅ Stable, working code
- ✅ Clean architecture
- ✅ Unique features (Pinyin ↔ Zhuyin)
- ✅ Easy to fork if needed

**Weaknesses:**
- ❌ Inactive maintenance
- ❌ Single maintainer (bus factor = 1)
- ❌ May break on future Python versions
- ❌ Small community (unlikely revival)

**Recommended for**:
- Non-critical applications
- Short-term projects (< 2 years)
- When combined with fork plan
- When transcription conversion is must-have

**NOT recommended for**:
- Mission-critical applications (without fork)
- Conservative organizations
- Long-term projects (> 5 years) without mitigation

**Next actions if using**:
1. ✅ Abstract behind internal API (easy migration)
2. ✅ Test with Python 3.13+ (verify compatibility)
3. ✅ Have fork strategy documented
4. ✅ Budget for migration or fork maintenance
5. ⚠️ Consider migrating to pypinyin + custom logic
6. ⚠️ Or fork immediately if critical to operations

**Verdict**: Use dragonmapper if its unique features justify the risk, but have an exit plan ready. For most projects, pypinyin (even without direct Pinyin ↔ Zhuyin) is the safer long-term choice.
