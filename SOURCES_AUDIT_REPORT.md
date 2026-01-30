# Sources Audit Report
**Date:** 2026-01-30
**Auditor:** research/polecats/nux
**Scope:** ~/gt/research/crew/ivan/packages/research/

## Executive Summary

**CRITICAL FINDING:** Source tracking is severely inadequate for research replicability.
- Only 5.3% of research documents contain source citations
- 75% of surveys lack sources entirely
- Zero metadata.yaml files include sources field

This represents a **significant risk to research credibility and replicability**.

---

## Audit Findings

### 1. Metadata.yaml Files

**Total metadata.yaml files checked:** 14

**Files with 'source' or 'sources' field:** 0 (0%)

**Assessment:** No research surveys track sources in their metadata.yaml files.

### 2. Markdown Files - Sources Sections

**Total .md files in discovery directories:** 468

**Files with ## Sources sections:** 25 (5.3%)

**Assessment:** Severe under-documentation. 94.7% of research documents lack source citations.

### 3. Survey-Level Source Coverage

**Total surveys:** 24

**Surveys WITH sources (at least 1 file):** 6 (25%)
- 1.035.1-chinese-tokenization/
- 1.144.1-pinyin-zhuyin-conversion/
- 1.144.2-tone-analysis/
- 1.154.1-chinese-text-simplification/
- 1.172-tmx-file-format/
- 1.173-terminology-extraction/

**Surveys MISSING sources entirely:** 18 (75%)
- 1.033.2-chinese-word-segmentation/
- 1.033.3-cjk-tokenizers/
- 1.033.4-named-entity-recognition-cjk/
- 1.075-core-deep-learning-frameworks/
- 1.148.1-chinese-morphological-analysis/
- 1.148.2-classical-chinese-parsing/
- 1.153.1-chinese-dependency-parsing/
- 1.160-character-databases/
- 1.161-radical-component-analysis/
- 1.162-handwriting-recognition-cjk/
- 1.163-character-encoding/
- 1.164-traditional-simplified-conversion/
- 1.165-stroke-order-writing/
- 1.166-ocr-cjk/
- 1.170-machine-translation-apis/
- 1.171-sentence-alignment/
- 1.210-multilingual-cjk-llms/
- 1.211-cjk-embedding-models/

### 4. Format Consistency Assessment

**Sample Analysis:** Examined 5 files with ## Sources sections

**Format:** Markdown bullet lists with links
```markdown
## Sources
- [Descriptive Text](https://url.example.com)
- [Another Source](https://another-url.com)
```

**Consistency:** ✅ **EXCELLENT**
- All sampled files use consistent markdown link format
- Descriptive text clearly identifies source
- URLs are properly formatted
- Mix of official docs, GitHub repos, academic papers, market reports

**Examples:**
```markdown
- [pypinyin PyPI](https://pypi.org/project/pypinyin/)
- [FDA Software as a Medical Device (SaMD)](https://www.fda.gov/medical-devices/software-medical-device-samd)
- [Language Learning App Market Size](https://www.marketgrowthreports.com/market-reports/language-learning-app-market-102085)
```

---

## Analysis

### What's Working
- **Format consistency:** The 5.3% that DO cite sources use a clean, consistent markdown format
- **Quality sources:** Mix of official documentation, GitHub repos, academic/market research
- **Recent surveys better:** 1.144.x series (pinyin/tone) shows good source discipline

### Critical Gaps
1. **No centralized source tracking:** Metadata.yaml files don't aggregate sources
2. **Inconsistent application:** 75% of surveys have zero source citations
3. **Discovery bias:** Sources only in S1/S4 documents, not S2/S3 comparative analyses
4. **No verification mechanism:** No way to validate if research claims are backed by cited sources

### Replicability Risk
**Current state FAILS basic research replicability standards:**
- Reader cannot verify 94.7% of claims
- No audit trail for data sources (GitHub stars, pricing, market share)
- Future researchers cannot reproduce methodology
- Conflicts with MPSE methodology's evidence-based approach

---

## Recommendations

### 1. **REQUIRE sources in metadata.yaml** ✅ **STRONGLY RECOMMEND**

**Rationale:**
- Central tracking enables audit/validation
- Survey-level view of source quality
- Enables automated source link checking
- Aligns with MPSE methodology rigor

**Proposed schema:**
```yaml
sources:
  primary:
    - url: https://github.com/owner/repo
      type: official_repo
      accessed: 2025-12-15
    - url: https://pypi.org/project/name/
      type: package_registry
      accessed: 2025-12-15

  secondary:
    - url: https://blog.example.com/comparison
      type: analysis
      accessed: 2025-12-16

  market_data:
    - url: https://marketreports.com/report
      type: market_research
      accessed: 2025-12-16
```

### 2. **Enforce ## Sources sections in S1-S4 documents**

**Minimum requirement:**
- S1 (Rapid): Sources for library stats, docs, repos
- S2 (Comprehensive): Sources for feature comparisons, benchmarks
- S3 (Need-Driven): Sources for pricing, case studies
- S4 (Strategic): Sources for market data, trend analysis

### 3. **Backfill existing research**

**Priority order:**
1. HIGH: Tier 1 research (foundational libraries)
2. MEDIUM: Tier 2 research (platforms/services)
3. LOW: Tier 3 research (niche/experimental)

**Estimated effort:** 2-4 hours per survey (18 surveys × 3 hours = ~54 hours)

### 4. **Add source validation to CI/CD**

**Automated checks:**
- Metadata.yaml contains sources field
- Each S1-S4 document has ## Sources section
- Links return 200 status (not broken)
- Warning on HTTP (suggest HTTPS)

### 5. **Update MPSE methodology documentation**

Add explicit source citation requirements:
- "All quantitative claims (stars, downloads, pricing) MUST cite source"
- "All qualitative claims (ecosystem maturity, adoption) MUST cite evidence"
- "Sources MUST be aggregated in metadata.yaml"

---

## Implementation Plan

### Phase 1: Standard (Week 1)
- [ ] Update MPSE.md with source requirements
- [ ] Create metadata.yaml source schema template
- [ ] Document ## Sources section format

### Phase 2: Enforcement (Week 2)
- [ ] Add pre-commit hook checking for sources field
- [ ] Create backfill tracking bead (18 surveys)
- [ ] Assign backfill work to research crew

### Phase 3: Validation (Week 3-4)
- [ ] Implement link checker CI job
- [ ] Create source quality rubric
- [ ] Audit backfilled sources for quality

---

## Conclusion

**Current state:** Research source tracking is inadequate for academic/professional rigor.

**Impact:** Credibility risk, replicability failure, methodology inconsistency.

**Action required:** Implement mandatory source tracking in metadata.yaml + enforce ## Sources sections.

**ROI:** High - protects research investment, enables verification, supports MPSE methodology claims.

---

**Audit completed:** 2026-01-30
**Next review:** After backfill completion (estimate 4-6 weeks)
