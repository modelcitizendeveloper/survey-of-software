# Discovery Table of Contents

## Quick Navigation

- **New to this topic?** Start with [DOMAIN_EXPLAINER.md](DOMAIN_EXPLAINER.md) for accessible overview
- **Want technical details?** Read S1-S4 in order for progressively deeper dives
- **Looking for tools?** Jump to [S3-solutions.md](S3-solutions.md)
- **Making decisions?** Read [S4-synthesis.md](S4-synthesis.md) for strategic recommendations

## Research Files

### [DOMAIN_EXPLAINER.md](DOMAIN_EXPLAINER.md)
**Audience**: Product managers, technical decision makers, non-specialists
**What it covers**: What CJK readability analysis solves, when you need it, trade-offs, costs, implementation reality
**Length**: ~1,800 words
**Key takeaway**: How to decide between simple coverage formulas vs ML approaches, build vs buy, and realistic timeline expectations

### [S1-surface-scan.md](S1-surface-scan.md)
**Phase**: Initial discovery
**What it covers**:
- What CJK readability analysis is (character frequency + proficiency level mapping)
- HSK vs TOCFL standards and their differences
- Existing web tools and libraries (surface level)
- Key insight: Character coverage vs word coverage trade-off

**Key findings**:
- HSK 3.0 (2026): 9 levels, 300-3000+ characters
- TOCFL: 8 levels, word-focused (3,100 chars, 14,425 words)
- 1,000 most common characters = ~90% coverage of everyday text

### [S2-structure.md](S2-structure.md)
**Phase**: Technical deep-dive
**What it covers**:
- Algorithm pipeline: segmentation → frequency analysis → feature extraction → classification
- How Jieba works (DAG + dynamic programming + HMM)
- Linguistic features (82 in CRIE, 196 in CTAP)
- Machine learning approach (SVM) vs simple formulas

**Key findings**:
- Segmentation is the bottleneck and error source
- Simple coverage formula: fast, 80-90% accuracy
- ML approach (CRIE): slower, 95%+ accuracy, diagnostic capabilities
- Performance: Jieba ~200K chars/sec, SVM prediction ~milliseconds

### [S3-solutions.md](S3-solutions.md)
**Phase**: Implementation options survey
**What it covers**:
- Open-source Python libraries (HSK Character Profiler, AlphaReadabilityChinese, CTAP, etc.)
- Commercial APIs (LTP-Cloud, Google Cloud NLP, Tencent)
- Academic tools (CRIE)
- Web-based free tools
- Comparison matrix and decision tree

**Key findings**:
- HSK Character Profiler: Best for quick HSK assessment (OSS, Python)
- CTAP: Most comprehensive (196 features) for research
- Google Cloud NLP: $1/million chars, but no HSK level support built-in
- Break-even: ~5M texts/year for DIY vs commercial API

### [S4-synthesis.md](S4-synthesis.md)
**Phase**: Strategic recommendations
**What it covers**:
- When this technology matters (high vs low-value use cases)
- Architecture decision framework (character vs word, simple vs ML, build vs buy, HSK vs TOCFL)
- Hidden complexity and gotchas (segmentation errors, HSK 3.0 migration, etc.)
- Cost modeling (DIY vs API vs OSS library)
- Implementation roadmap (MVP → production → enhancement → ML)
- Success metrics and market trends

**Key recommendations**:
- **Language learning apps**: Start with HSK Character Profiler (OSS), upgrade to custom Jieba + HSK 3.0 at scale
- **Publishers/educators**: Invest in CRIE-style ML system for fine-grained diagnostics
- **Researchers**: Use CTAP (196 features)
- **Exploring**: Use free web tools (HSK HSK Analyzer)

**ROI sweet spot**: 100K-1M texts/month for OSS libraries; above that, custom build pays off

## Research Timeline

| Phase | Duration | Output |
|-------|----------|--------|
| S1: Surface scan | 1 hour | Understanding of problem space, standards, existing tools |
| S2: Structure | 2 hours | Technical depth on algorithms, pipelines, ML approaches |
| S3: Solutions | 2 hours | Survey of available tools, APIs, libraries |
| S4: Synthesis | 2 hours | Strategic recommendations, decision frameworks |
| DOMAIN_EXPLAINER | 1.5 hours | Accessible overview for non-specialists |
| **Total** | **8.5 hours** | Complete research package |

## Key Decision Points

Based on this research, here are the critical decisions for anyone implementing CJK readability analysis:

1. **Character vs Word-based?**
   - Character for MVP/simple cases
   - Add word-based for HSK 4+ accuracy

2. **Simple vs ML?**
   - Simple coverage formula for B2C learner apps (good enough)
   - ML (CRIE-style) for B2B publishers needing diagnostics

3. **Build vs Buy vs OSS?**
   - OSS library for < 100K texts/month
   - Custom build for 100K-5M texts/month
   - Commercial API only if you need multi-language NLP (not just Chinese readability)

4. **HSK vs TOCFL?**
   - HSK for mainland China market
   - TOCFL for Taiwan/Hong Kong
   - Both if global market with > 20% Traditional Chinese users

## Follow-up Research Opportunities

Topics not covered in this research (potential future beads):

- **1.152.2**: Deep dive into Chinese word segmentation algorithms (Jieba alternatives, BERT-based)
- **1.152.3**: Character frequency datasets comparison (SUBTLEX-CH vs Jun Da vs web-scraped)
- **1.152.4**: HSK 3.0 migration guide (mapping old to new levels, updating applications)
- **1.152.5**: Personalized readability (beyond HSK levels—predicting individual learner difficulty)
- **1.152.6**: Multimodal readability (text + images, children's books, comics)

## External Resources

### Standards & Word Lists
- HSK 3.0 official: https://github.com/krmanik/HSK-3.0
- TOCFL vocabulary: https://github.com/skishore/inkstone/pull/47
- SUBTLEX-CH frequency: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0010729

### Key Papers
- CRIE methodology: https://link.springer.com/article/10.3758/s13428-015-0649-1
- CTAP for Chinese: https://aclanthology.org/2022.lrec-1.592.pdf
- Jieba algorithm: https://medium.com/@ching.achterwinter/chinese-word-segmentation-2e28feee87fe

### Tools to Try
- HSK HSK Analyzer: https://hskhsk.com/analyse
- Chinese Text Analyser: https://www.chinesetextanalyser.com/
- HSK Character Profiler: https://github.com/Ancastal/HSK-Character-Profiler

---

**Research completed**: 2026-01-29
**Researcher**: furiosa (Gas Town polecat)
**Research ID**: 1.152.1-cjk-readability
