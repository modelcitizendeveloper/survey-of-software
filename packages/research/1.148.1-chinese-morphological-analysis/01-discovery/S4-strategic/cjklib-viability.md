# Strategic Viability: cjklib

## Current State

**Library:** cjklib - Han character library for CJKV languages
**Maintainer:** cburgmer (original), free-utils-python (Python 3 fork)
**Status:** Python 2 EOL, Python 3 via fork
**License:** MIT (permissive)

## Maintenance & Longevity Assessment

### Original cjklib (cburgmer/cjklib)
**Risk Level: HIGH**

- ❌ Python 2 only (EOL since 2020)
- ❌ No commits addressing Python 3 in main repo
- ⚠️ Open issue #11 (Python 3 support) since 2017, unresolved
- ⚠️ Unclear maintenance status
- ✅ MIT license allows forking

### cjklib3 Fork (free-utils-python/cjklib3)
**Risk Level: MODERATE-HIGH**

- ✅ Python 3 compatibility via 2to3
- ⚠️ Fork maintenance unclear
- ⚠️ Not on PyPI (manual installation)
- ⚠️ Depends on 2to3 conversion (not native Python 3)
- ⚠️ Small community around fork

### Verdict
**High technical debt, uncertain future**

## Evolution & Adaptation

### Extensibility
- ✅ SQLite backend = easy to extend data
- ✅ Modular architecture
- ❌ Python 2 codebase limits modern Python features
- ⚠️ Would require significant refactoring for modernization

### Migration Paths

**Option A: Continue with fork**
- Keep using cjklib3 as-is
- Accept technical debt
- Risk: Fork abandonment

**Option B: Port to native Python 3**
- Rewrite cjklib in modern Python
- Use same algorithms, fresh codebase
- Effort: ~2-4 weeks
- Benefit: Full control, modern code

**Option C: Extract data, abandon library**
- Parse cjklib's SQLite database
- Build minimal custom API
- Effort: ~1 week
- Benefit: No legacy code

## Ecosystem Integration

### Standards Compliance
- ✅ Unicode IDS standard
- ✅ SQLite (universal format)
- ✅ Standard radical classifications
- ✅ Well-documented file formats

### Integration Points
- ⚠️ Python 2/3 split complicates integration
- ✅ Can extract data for use elsewhere
- ✅ SQL interface standard

## Resource Requirements

### Initial Integration
- **Time:** 1-2 weeks (setup fork, database build)
- **Skills:** Python, SQL, CJK character knowledge
- **Infrastructure:** Minimal (local DB)

### Ongoing Maintenance
- **Monitoring:** Watch for fork updates (low frequency expected)
- **Updates:** Manual process (rebuild from fork)
- **Risk Management:** Plan for fork abandonment

### Exit Costs
- **Low:** Data is accessible via SQLite
- **Migration:** Can extract data, build new tool
- **No vendor lock-in:** Open source, standard formats

## Legal & Compliance

### License: MIT
- ✅ Permissive use
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ No copyleft requirements

### Attribution
- Required: MIT license notice
- Low burden: Include license file

### Data Sources
- ✅ Multiple open character databases
- ✅ Unicode standard (public)
- No licensing concerns for data

## Strategic Risks

### Risk 1: Fork Abandonment
**Probability:** MODERATE-HIGH
**Impact:** MODERATE (data remains accessible)

**Mitigation:**
- Extract SQLite database
- Document data schema
- Prepare migration to custom code

### Risk 2: Python 3 Incompatibility Issues
**Probability:** LOW-MODERATE
**Impact:** LOW-MODERATE (can fix or work around)

**Mitigation:**
- Test thoroughly before production
- Isolate in separate service if needed
- Have extraction plan ready

### Risk 3: Limited Community Support
**Probability:** HIGH
**Impact:** LOW (reduces feature additions, not core functionality)

**Mitigation:**
- Don't depend on new features
- Budget for custom fixes
- Consider eventual migration

## Build vs. Adopt Decision

### Adopt cjklib3 If:
- ✅ Need comprehensive character search immediately
- ✅ Can accept Python 3 fork complexity
- ✅ Short-term solution acceptable (~1-2 years)
- ✅ Plan to migrate eventually

### Build Custom If:
- ✅ Long-term solution needed (5+ years)
- ✅ Have development resources (2-4 weeks)
- ✅ Want full control and modern code
- ✅ Can leverage existing data (CJKVI-IDS, makemeahanzi)

## Recommended Strategy

### Phase 1: Use Data, Not Library (LOW RISK)
1. Extract data from cjklib's sources or use CJKVI-IDS directly
2. Build minimal Python 3 API for your needs
3. Avoid dependency on cjklib code
4. Use cjklib algorithms as reference, but reimplement

### Phase 2: Enhance as Needed
1. Start with basic character decomposition
2. Add search features progressively
3. Optimize based on actual usage
4. No technical debt from legacy code

### Rationale:
- **Same data quality** (using same sources)
- **Modern Python 3** (clean implementation)
- **Full control** (no fork dependency)
- **Lower risk** (no abandonment concerns)
- **Maintainable** (code you understand)

## Timeline & Effort

### Data Extraction: 2-3 days
- Parse CJKVI-IDS or cjklib DB
- Load into modern format (JSON, SQLite, etc.)

### Basic API: 3-5 days
- Character decomposition
- Radical lookup
- IDS parsing

### Advanced Features: 1-2 weeks
- Component search
- Variant mappings
- Optimization

**Total: 2-3 weeks for production-ready solution**

**vs. cjklib3 fork: 1 week setup + ongoing maintenance burden**

## Exit Strategy

If cjklib approach fails:

1. **Data is preserved** - SQLite DB, IDS files remain accessible
2. **Migrate to makemeahanzi** - JSON data, easier integration
3. **Build on CJKVI-IDS** - Authoritative IDS source
4. **No data loss** - All approaches use same underlying data

**Low switching cost** due to standard formats and open data

---

**Strategic Verdict: MODERATE RISK**

cjklib provides excellent functionality but carries significant technical debt. Recommended approach: Extract data and algorithms, rebuild in modern Python for long-term viability. Short-term use acceptable if migration plan exists.

**Timeline:** Can use fork for <1 year, plan migration to custom solution
**Effort:** 2-3 weeks to build modern replacement
**Risk:** Manageable via data extraction and migration plan
