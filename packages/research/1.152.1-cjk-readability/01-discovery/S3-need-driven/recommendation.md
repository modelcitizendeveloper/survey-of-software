# S3 Need-Driven: Recommendations

## Overview

CJK readability assessment has **no single library solution**. Every use case requires integrating multiple data sources with custom logic. This analysis examined 5 distinct use cases to understand real-world requirements.

## Key Finding: Multi-Library Integration is Universal

**None of the 5 use cases can be solved with a single library.** All require:
1. Word segmentation (jieba, jieba.js)
2. Character/word frequency data (Jun Da, BCC Corpus, SUBTLEX-CH)
3. Proficiency mapping (HSK/TOCFL word lists)
4. Custom business logic (coverage calculation, difficulty scoring, filtering)

## Recommendations by Use Case

### 1. Language Learning Applications
**Who**: Duolingo, HelloChinese, ChinesePod
**Need**: Match content to learner proficiency dynamically

**Recommended Stack**:
- **jieba**: Word segmentation
- **BCC Character Frequency** or **Jun Da**: Character-level difficulty
- **CC-CEDICT + HSK tags**: Word-level proficiency mapping
- **Custom scoring**: Coverage calculation, adaptive recommendations

**Implementation Priority**:
1. HIGH: HSK tagging for vocabulary (curriculum alignment)
2. HIGH: Coverage calculation (90-95% = optimal challenge)
3. MEDIUM: Character frequency indicators (rare character warnings)
4. LOW: Perfect segmentation (learner-facing apps tolerate minor errors)

**Complexity Justified When**:
- Adaptive content selection is core feature
- Target serious learners (not casual tourists)
- Large content library needs automated grading

**Simpler Alternative**:
Manual tiering (easy/medium/hard) for small, curated content libraries

---

### 2. Graded Reader Publishers
**Who**: Mandarin Companion, The Chairman's Bao, Chinese Breeze
**Need**: Categorize books/articles by reading difficulty

**Recommended Stack**:
- **jieba**: Word segmentation
- **CC-CEDICT + HSK**: Vocabulary compliance checking
- **BCC Character Frequency**: Identify rare characters
- **Custom proper name dictionary**: Filter false positives
- **Editorial rules engine**: Validate vocabulary constraints

**Implementation Priority**:
1. HIGH: Vocabulary compliance validation (catch violations before publication)
2. HIGH: Catalog consistency (books at same level should match)
3. MEDIUM: Chapter progression analysis (smooth difficulty curve)
4. MEDIUM: Comparative difficulty ranking (within-level ordering)

**Complexity Justified When**:
- Large catalog (50+ books) requiring consistent leveling
- Series with strict vocabulary control
- Multiple authors need alignment

**Simpler Alternative**:
Editorial judgment for small catalogs (<20 books), literary quality prioritized over strict leveling

---

### 3. Educational Content Creators
**Who**: Textbook authors, educators, course creators
**Need**: Validate material difficulty while writing

**Recommended Stack**:
- **jieba** or **jieba.js**: Real-time segmentation
- **CC-CEDICT + HSK lists**: Vocabulary level lookup
- **Custom synonym engine**: Suggest simpler alternatives
- **Browser extension / Google Docs add-on**: Inline feedback

**Implementation Priority**:
1. HIGH: Real-time violation highlighting (fix while writing)
2. HIGH: Synonym suggestions (pedagogically appropriate replacements)
3. MEDIUM: Batch validation (pre-publication QA)
4. LOW: Grammar complexity (vocabulary harder to assess)

**Complexity Justified When**:
- High-volume production (multiple textbooks/year)
- Strict curriculum alignment (HSK/TOCFL requirements)
- Multi-author coordination needed

**Simpler Alternative**:
Post-writing manual validation with reference materials (Pleco, HSK word lists) for one-off worksheets

---

### 4. Reading Assistant Tools
**Who**: Zhongwen extension, Du Chinese, LingQ, Pleco Reader
**Need**: Real-time difficulty indicators and vocabulary popups

**Recommended Stack**:
- **jieba.js**: Browser-native word segmentation
- **Pruned CC-CEDICT**: Top 10k words only (3 MB vs 30 MB)
- **Jun Da Character Frequency**: Fast character-level difficulty
- **IndexedDB**: Track user's known vocabulary
- **Optional cloud sync**: Cross-device vocabulary tracking

**Implementation Priority**:
1. HIGH: Fast performance (sub-second page analysis)
2. HIGH: Small bundle size (browser extension limits)
3. MEDIUM: User vocabulary personalization (known word highlighting)
4. LOW: Perfect accuracy (speed > completeness for real-time tools)

**Complexity Justified When**:
- Privacy important (user data stays on device)
- Real-time performance critical
- Offline usage required

**Simpler Alternative**:
Server-side API for complex processing (trade privacy/offline for simplicity), but most users prefer client-side

---

### 5. Curriculum Designers
**Who**: University coordinators, K-12 developers, corporate trainers
**Need**: Design multi-year learning progressions

**Recommended Stack**:
- **jieba**: Batch word segmentation
- **CC-CEDICT + HSK/TOCFL**: Standards alignment validation
- **BCC/SUBTLEX-CH**: Vocabulary frequency reference
- **Custom gap detection**: Find missing difficulty levels
- **Visualization tools**: Progression curves, coverage heatmaps

**Implementation Priority**:
1. HIGH: Standards coverage validation (HSK/TOCFL compliance)
2. HIGH: Gap detection (missing proficiency levels)
3. MEDIUM: Competitive benchmarking (compare to peers)
4. LOW: Cost optimization (budget secondary to quality)

**Complexity Justified When**:
- Large program (>100 students/year)
- Standards-driven (accreditation requirements)
- Textbook adoption decisions (objective comparison)

**Simpler Alternative**:
Faculty judgment for small/specialized programs, experimental curricula, heritage learner programs

---

## Cross-Use-Case Insights

### Universal Requirements
All 5 use cases need:
- ✅ **Word segmentation** (jieba is de facto standard)
- ✅ **HSK/TOCFL mapping** (curriculum alignment universal)
- ✅ **Character frequency data** (difficulty signals)
- ✅ **Custom logic** (no library provides complete solution)

### Use-Case-Specific Requirements

| Feature | Learning Apps | Publishers | Creators | Reading Tools | Curriculum |
|---------|--------------|------------|----------|---------------|------------|
| **Real-time feedback** | Medium | Low | HIGH | HIGH | Low |
| **Batch processing** | Medium | HIGH | Medium | Low | HIGH |
| **User personalization** | HIGH | Low | Low | HIGH | Low |
| **Standards alignment** | HIGH | HIGH | HIGH | Medium | HIGH |
| **Offline capability** | HIGH | Medium | HIGH | HIGH | Medium |

### Common Pain Points
All use cases struggle with:
- ❌ **Proper name handling** (character/place names flagged as rare)
- ❌ **Grammar complexity** (sentence structure difficulty not captured)
- ❌ **Context-aware definitions** (word meaning varies)
- ❌ **Synonym quality** (not all alternatives pedagogically equivalent)
- ❌ **Standards evolution** (HSK 2012 → 2021 migration)

---

## Library Selection Matrix

### Core Components (Choose One from Each)

**Word Segmentation**:
- **jieba** (Python): Server-side, batch processing, highest accuracy
- **jieba.js** (JavaScript): Browser, real-time, lightweight

**Character Frequency**:
- **Jun Da**: Simple, fast, small file (~100 KB)
- **BCC Corpus**: Authoritative, contemporary, large (requires preprocessing)
- **SUBTLEX-CH**: Spoken language focus (conversational content)

**Word-Level Proficiency**:
- **CC-CEDICT + HSK tags**: Comprehensive but incomplete coverage
- **BLCU HSK Lists**: Official standard, requires integration
- **Custom HSK database**: Combine multiple sources for completeness

### Integration Patterns

**Pattern A: Lightweight Client-Side** (Reading Assistants)
```
jieba.js + Jun Da + Pruned CC-CEDICT + IndexedDB
= Fast, offline, privacy-friendly, limited features
```

**Pattern B: Server-Side Comprehensive** (Publishers, Curriculum)
```
jieba + BCC Corpus + Full CC-CEDICT + Custom DB
= Slow, accurate, feature-rich, server required
```

**Pattern C: Hybrid Real-Time** (Learning Apps, Content Creators)
```
jieba.js (client) + HSK API (server) + User vocab cache (IndexedDB)
= Fast feedback, comprehensive data, complex architecture
```

---

## Missing Capabilities (Build Custom)

No existing library provides:

### 1. Proper Name Filtering
**Problem**: Character/place names flagged as rare vocabulary
**Solution**: Custom dictionary of names + NER (Named Entity Recognition)
**Affected Use Cases**: Publishers (50% false positives), Content Creators (40%)

### 2. Grammar Complexity Metrics
**Problem**: Sentence structure difficulty not captured (only vocabulary)
**Solution**: Dependency parsing + sentence length + clause complexity
**Affected Use Cases**: All (but especially Curriculum Designers)

### 3. Pedagogical Synonym Ranking
**Problem**: Not all synonyms equally teachable
**Solution**: ML model trained on textbook corpora + teacher feedback
**Affected Use Cases**: Content Creators (critical), Learning Apps (important)

### 4. Context-Aware Proficiency
**Problem**: Word difficulty varies by context (多 harder in 多少 vs 很多)
**Solution**: Phrase-level HSK tagging + context windows
**Affected Use Cases**: Learning Apps (important), Reading Assistants (nice-to-have)

### 5. Standards Migration Tools
**Problem**: HSK 2012 → HSK 2021 vocabulary changes
**Solution**: Mapping tables + automated curriculum updates
**Affected Use Cases**: Publishers (critical), Curriculum Designers (critical)

---

## Decision Framework

### When to Build Custom Solution

Build custom readability tools when:
- **Volume justifies cost**: 100+ books, 1000+ lessons, or 10k+ users
- **Competitive advantage**: Readability assessment is core differentiation
- **Domain-specific needs**: Business Chinese, medical Chinese, classical Chinese
- **Standards compliance critical**: Accreditation, certification, testing

### When to Use Manual Methods

Rely on human judgment when:
- **Small scale**: <20 books, <100 lessons, boutique programs
- **Experimental**: Pioneering new approaches, no benchmarks
- **Quality > consistency**: Literary content, cultural nuance
- **Budget constraints**: Custom tooling expensive, ROI unclear

### When to License Third-Party

Consider SaaS tools when:
- **Exists**: (Currently no comprehensive SaaS for CJK readability)
- **Cost-effective**: Subscription < custom development
- **Good enough**: 80% solution acceptable, not 100% perfection

**Reality check**: As of 2025, no off-the-shelf SaaS provides comprehensive CJK readability assessment. All serious use cases require custom integration.

---

## Implementation Roadmap (Generic)

### Phase 1: Proof of Concept (1-2 months)
1. Choose core libraries (jieba + frequency data + HSK lists)
2. Build basic difficulty estimator
3. Validate on sample content (10-20 texts)
4. Measure accuracy vs manual classification

### Phase 2: MVP (3-6 months)
1. Integrate libraries into workflow (API, UI, or batch tool)
2. Add custom logic (coverage, scoring, filtering)
3. Pilot with small user group (5-10 people)
4. Iterate based on feedback

### Phase 3: Production (6-12 months)
1. Optimize performance (caching, parallel processing)
2. Build proper name dictionary (reduce false positives)
3. Add synonym suggestions (for content creators)
4. Implement user vocabulary tracking (for learners)

### Phase 4: Advanced Features (12+ months)
1. Grammar complexity metrics
2. Context-aware proficiency
3. ML-based improvements
4. Cross-device sync, collaboration features

---

## Cost-Benefit Analysis

### Automation Benefits (Quantified)
- **Textbook publisher**: Save 20-40 hours/book in manual leveling
- **Learning app**: 2x content library size (more materials graded)
- **Curriculum designer**: 80% reduction in textbook evaluation time
- **Content creator**: 50% faster writing (real-time feedback)

### Automation Costs (Estimated)
- **Development**: $50k-$200k (depending on features)
- **Maintenance**: $10k-$30k/year (data updates, bug fixes)
- **Accuracy trade-offs**: 10-20% false positive rate on proper names

### ROI Thresholds
- **High-volume publishers**: ROI positive at 10+ books/year
- **Large learning apps**: ROI positive at 1000+ active users
- **Universities**: ROI positive at 100+ students/year
- **Individual creators**: ROI negative (manual methods better)

---

## Final Recommendation

**For most use cases, build custom integration of:**
1. **jieba** (segmentation)
2. **Jun Da or BCC** (character frequency)
3. **CC-CEDICT + HSK** (word proficiency)
4. **Custom logic** (business-specific rules)

**Start simple** (manual validation) and **add automation incrementally** as volume grows. Perfect accuracy is unattainable - optimize for "good enough" given use case constraints.

**No silver bullet exists.** CJK readability assessment requires domain expertise + software engineering + continuous iteration. Tools enable but don't replace human judgment.
