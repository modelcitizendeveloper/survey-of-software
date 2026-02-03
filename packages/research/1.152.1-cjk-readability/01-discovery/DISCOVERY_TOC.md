# Discovery Table of Contents

## Quick Navigation

- **New to this topic?** Start with [DOMAIN_EXPLAINER.md](../DOMAIN_EXPLAINER.md) for accessible overview
- **Want rapid insights?** Read [S1-rapid/recommendation.md](S1-rapid/recommendation.md)
- **Need technical depth?** Explore S2-comprehensive/
- **Looking for tools?** Jump to S3-need-driven/
- **Making decisions?** Read S4-strategic/

## 4PS Discovery Structure

### S1: Rapid (Surface Scan)
Quick overview of CJK readability, standards, and existing tools.

- [approach.md](S1-rapid/approach.md) - Research methodology
- [hsk-standards.md](S1-rapid/hsk-standards.md) - HSK proficiency levels (2026 update)
- [tocfl-standards.md](S1-rapid/tocfl-standards.md) - Taiwan TOCFL standards
- [web-tools.md](S1-rapid/web-tools.md) - Free web-based analysis tools
- [recommendation.md](S1-rapid/recommendation.md) - **START HERE** for quick insights

**Key finding**: 1,000 characters = 90% coverage; Character vs word analysis is key choice

### S2: Comprehensive (Technical Structure)
How readability analysis works - algorithms, features, ML approaches.

- [approach.md](S2-comprehensive/approach.md) - Research methodology
- [jieba-segmentation.md](S2-comprehensive/jieba-segmentation.md) - How Jieba segments Chinese text
- [frequency-analysis.md](S2-comprehensive/frequency-analysis.md) - Character frequency datasets & methods
- [crie-methodology.md](S2-comprehensive/crie-methodology.md) - CRIE's 82 features + SVM approach
- [ctap-features.md](S2-comprehensive/ctap-features.md) - CTAP's 196 linguistic features
- [feature-comparison.md](S2-comprehensive/feature-comparison.md) - Simple vs ML approaches compared
- [recommendation.md](S2-comprehensive/recommendation.md) - Technical insights summary

**Key finding**: 80% accuracy (simple) vs 90% accuracy (ML) costs 50-100x more complexity

### S3: Need-Driven (Solutions by Use Case)
Mapping tools to real-world applications with cost models.

- [approach.md](S3-need-driven/approach.md) - Research methodology
- [use-case-language-learning-apps.md](S3-need-driven/use-case-language-learning-apps.md) - B2C learner apps
- [use-case-publishers-educators.md](S3-need-driven/use-case-publishers-educators.md) - High-stakes publishing
- [use-case-researchers.md](S3-need-driven/use-case-researchers.md) - Academic research
- [recommendation.md](S3-need-driven/recommendation.md) - Decision tree by use case

**Key finding**: 80% of apps should use HSK Character Profiler (OSS, free, 1-2 days)

### S4: Strategic (Viability & ROI Analysis)
Long-term strategic decisions with financial models and risk assessment.

- [approach.md](S4-strategic/approach.md) - Research methodology
- [build-vs-buy-viability.md](S4-strategic/build-vs-buy-viability.md) - 3-year TCO analysis
- [simple-vs-ml-viability.md](S4-strategic/simple-vs-ml-viability.md) - When complexity pays off
- [recommendation.md](S4-strategic/recommendation.md) - **FINAL RECOMMENDATIONS**

**Key finding**: Start simple (OSS), upgrade only when hitting scale/accuracy walls

## Research Timeline

| Phase | Duration | Output |
|-------|----------|--------|
| S1: Rapid | 1-2 hours | Understanding of standards, tools |
| S2: Comprehensive | 2-3 hours | Technical depth on algorithms |
| S3: Need-driven | 2-3 hours | Solutions mapped to use cases |
| S4: Strategic | 2-3 hours | Strategic recommendations, ROI |
| **Total** | **8-11 hours** | Complete research package |

## Critical Decision Points

### 1. Character vs Word-Based?
- **Character**: Simpler, aligns with HSK, no segmentation needed
- **Word**: More accurate for comprehension, requires Jieba
- **Recommendation**: Start character-based, add word-based for HSK 4+

### 2. Simple vs ML?
- **Simple (80%)**: Coverage formula, < 1ms, days to build
- **ML (90%)**: CRIE-style, 1-5s, months to build
- **Break-even**: High-stakes publishing OR volume > 1M texts/month

### 3. Build vs Buy?
- **OSS**: < 500K texts/month
- **Custom**: > 1M texts/month (cost savings)
- **Commercial API**: Only if need multi-language NLP (not just readability)

### 4. HSK vs TOCFL?
- **HSK**: Mainland China, larger ecosystem, character-focused
- **TOCFL**: Taiwan/HK, word-focused, Traditional Chinese
- **Both**: If > 20% Traditional Chinese users

## Quick Start Guide

### For Language Learning Apps
1. Integrate [HSK Character Profiler](https://github.com/Ancastal/HSK-Character-Profiler)
2. Deploy simple API
3. Collect feedback
4. Upgrade only if complaints > 20%

### For Publishers
1. Test CRIE (if accessible)
2. Compare vs expert grading
3. Build custom ML if volume > 500 texts/year
4. Use hybrid (OSS + manual) if smaller

### For Researchers
1. Install CTAP
2. Extract 196 features
3. Select relevant features for research question
4. Publish findings

## External Resources

### Standards & Data
- HSK 3.0 Lists: https://github.com/krmanik/HSK-3.0
- TOCFL Vocabulary: https://github.com/skishore/inkstone/pull/47
- SUBTLEX-CH Frequency: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0010729

### Key Papers
- CRIE Methodology: https://link.springer.com/article/10.3758/s13428-015-0649-1
- CTAP for Chinese: https://aclanthology.org/2022.lrec-1.592.pdf
- Jieba Segmentation: https://medium.com/@ching.achterwinter/chinese-word-segmentation-2e28feee87fe

### Tools to Try
- HSK HSK Analyzer (web): https://hskhsk.com/analyse
- Chinese Text Analyser (web): https://www.chinesetextanalyser.com/
- HSK Character Profiler (Python): https://github.com/Ancastal/HSK-Character-Profiler

## Follow-Up Research Opportunities

Topics not covered (potential future beads):

- **Deep dive into Jieba alternatives** (BERT-based segmentation)
- **Character frequency dataset comparison** (SUBTLEX vs Jun Da vs modern web)
- **HSK 3.0 migration guide** (2026 implementation)
- **Personalized readability** (individual learner models beyond HSK)
- **Multimodal readability** (text + images, audio transcripts)

---

**Research completed**: 2026-01-29
**Researcher**: furiosa (Gas Town polecat)
**Research ID**: 1.152.1-cjk-readability
**Protocol**: 4PS (Four-Pass Search)
