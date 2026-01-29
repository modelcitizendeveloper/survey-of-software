# Discovery Table of Contents: Sentence Alignment

## Overview

This research explores sentence alignment tools for matching parallel sentences in bilingual corpora, essential for machine translation training and translation memory systems.

**Primary Tools Evaluated**:
- **Hunalign**: Fast dictionary-based alignment (Gale-Church algorithm)
- **Bleualign**: BLEU-based alignment using MT output
- **vecalign**: Multilingual embedding-based alignment (LASER)

## Pass Structure

### S1: Rapid Discovery (20-30 minutes)
Quick assessment of each tool's core strengths and use cases.

**Files**:
- [`approach.md`](S1-rapid/approach.md) - Research methodology
- [`hunalign.md`](S1-rapid/hunalign.md) - Fast statistical alignment
- [`bleualign.md`](S1-rapid/bleualign.md) - BLEU-based alignment
- [`vecalign.md`](S1-rapid/vecalign.md) - Embedding-based alignment
- [`recommendation.md`](S1-rapid/recommendation.md) - Quick decision guide

**Key Takeaway**: Hunalign for speed, vecalign for accuracy, bleualign for divergent texts.

### S2: Comprehensive Discovery (2-3 hours)
Deep technical analysis of algorithms, parameters, and performance characteristics.

**Files**:
- [`approach.md`](S2-comprehensive/approach.md) - Research methodology
- [`hunalign.md`](S2-comprehensive/hunalign.md) - Algorithmic deep dive, parameter tuning
- [`bleualign.md`](S2-comprehensive/bleualign.md) - BLEU scoring, MT system impact
- [`vecalign.md`](S2-comprehensive/vecalign.md) - Embedding architecture, scaling
- [`recommendation.md`](S2-comprehensive/recommendation.md) - Technical decision guide

**Key Takeaway**: Hunalign scales linearly with O(n) complexity, vecalign achieves 93-99% F1 but requires GPU, bleualign depends on MT quality.

### S3: Need-Driven Discovery (1-2 hours)
Practical implementation workflows for common scenarios.

**Files**:
- [`approach.md`](S3-need-driven/approach.md) - Research methodology
- [`mt-training-data.md`](S3-need-driven/mt-training-data.md) - Large-scale MT corpus creation
- [`multilingual-cms.md`](S3-need-driven/multilingual-cms.md) - Translation memory for CMS
- [`recommendation.md`](S3-need-driven/recommendation.md) - Scenario selection guide

**Key Takeaway**: Most workflows follow: extract → align → filter → validate. Tool choice depends on volume and quality requirements.

### S4: Strategic Discovery (1-2 hours)
Long-term organizational decisions, production deployment, and cost analysis.

**Files**:
- [`approach.md`](S4-strategic/approach.md) - Research methodology
- [`build-vs-buy.md`](S4-strategic/build-vs-buy.md) - SaaS vs open source vs custom
- [`production-deployment.md`](S4-strategic/production-deployment.md) - Kubernetes, monitoring, scaling
- [`recommendation.md`](S4-strategic/recommendation.md) - Long-term decision framework

**Key Takeaway**: For most orgs, start with SaaS (validate), migrate to open source (scale). Only build custom if alignment is core business.

## Reading Paths

### Path 1: "I need a quick answer" (15 minutes)
1. [S1 Recommendation](S1-rapid/recommendation.md)
2. Pick your tool based on speed vs accuracy tradeoff
3. Done

### Path 2: "I'm implementing this" (1-2 hours)
1. [S1 Recommendation](S1-rapid/recommendation.md) - Choose tool
2. [S3 Scenario Guide](S3-need-driven/recommendation.md) - Pick your workflow
3. [S3 Workflow](S3-need-driven/) - Follow step-by-step guide
4. Done

### Path 3: "I'm making a strategic decision" (3-4 hours)
1. [S1 Recommendation](S1-rapid/recommendation.md) - Understand options
2. [S2 Recommendation](S2-comprehensive/recommendation.md) - Technical tradeoffs
3. [S4 Build vs Buy](S4-strategic/build-vs-buy.md) - Strategic analysis
4. [S4 Recommendation](S4-strategic/recommendation.md) - Long-term framework
5. Present to stakeholders

### Path 4: "I'm a researcher" (Full read, 6-8 hours)
1. Read all S1 files (tools overview)
2. Read all S2 files (algorithms and benchmarks)
3. Read S3 workflows for implementation details
4. Read S4 for production considerations
5. Synthesize for your specific research needs

## Key Findings Summary

### Performance Comparison
| Tool | Speed | Accuracy | Complexity | Best For |
|------|-------|----------|------------|----------|
| Hunalign | ⚡⚡⚡ Very Fast | 85-95% | Low | Large-scale MT pipelines |
| Bleualign | ⚡ Slow | 90-98% | Medium | Divergent translations |
| vecalign | ⚡⚡ Moderate | 93-99% | High | Multilingual, low-resource |

### Cost Comparison (10M pairs/year)
| Approach | Year 1 | Year 2 | Year 3 | 3-Year Total |
|----------|--------|--------|--------|--------------|
| SaaS | $30K | $20K | $20K | $70K |
| Open Source | $90K | $50K | $50K | $190K |
| Custom Build | $350K | $190K | $190K | $730K |

### Decision Framework
```
Volume < 1M pairs/year → SaaS
Volume 1M-10M pairs/year → Open Source (hunalign)
Volume > 10M pairs/year → Open Source (vecalign or hunalign)
Quality critical + low volume → vecalign or bleualign
Speed critical + high volume → hunalign
```

## Cross-References

### Related Research
- **1.033.2 Chinese Word Segmentation**: Pre-processing for Chinese alignment
- **1.033.3 CJK Tokenizers**: Tokenization before alignment
- **1.210 Machine Translation Libraries**: Downstream use of aligned corpora

### External Resources
- [Hunalign GitHub](https://github.com/danielvarga/hunalign)
- [vecalign GitHub](https://github.com/thompsonb/vecalign)
- [Bleualign GitHub](https://github.com/rsennrich/Bleualign)
- [LASER Embeddings](https://github.com/facebookresearch/LASER)

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-29 | 1.0 | Initial research - all 4 passes completed |
