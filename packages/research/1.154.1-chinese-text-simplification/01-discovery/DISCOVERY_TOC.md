# Discovery Table of Contents

## Quick Navigation

- **New to this topic?** Start with [DOMAIN_EXPLAINER.md](../DOMAIN_EXPLAINER.md)
- **Want rapid insights?** Read [S1-rapid/recommendation.md](S1-rapid/recommendation.md)
- **Need technical depth?** Read [S2-comprehensive/recommendation.md](S2-comprehensive/recommendation.md)
- **Looking for use case guidance?** Read [S3-need-driven/recommendation.md](S3-need-driven/recommendation.md)
- **Making strategic decisions?** Read [S4-strategic/recommendation.md](S4-strategic/recommendation.md)

## 4PS Discovery Structure

### S1: Rapid (Surface Scan) ✅ COMPLETE

Library landscape and MVP recommendations.

- [README.md](S1-rapid/README.md) - Library inventory
- [mcts-dataset.md](S1-rapid/mcts-dataset.md) - MCTS dataset deep dive
- [foundational-libraries.md](S1-rapid/foundational-libraries.md) - jieba, OpenCC, HanLP
- [recommendation.md](S1-rapid/recommendation.md) - MVP recommendations

**Key finding**: No pip-installable libraries exist; build using jieba + OpenCC + custom rules

---

### S2: Comprehensive (Technical Structure) ✅ COMPLETE

Neural approaches, training, and evaluation.

- [README.md](S2-comprehensive/README.md) - Overview
- [neural-architectures.md](S2-comprehensive/neural-architectures.md) - mT5, mBART, training
- [evaluation-metrics.md](S2-comprehensive/evaluation-metrics.md) - BLEU, SARI, HSK metrics
- [recommendation.md](S2-comprehensive/recommendation.md) - Technical recommendations

**Key finding**: mT5-base + LoRA on MCTS = best balance (1 week, $500, 85-90% accuracy)

---

### S3: Need-Driven (Solutions by Use Case) ✅ COMPLETE

Implementation strategies mapped to use cases with TCO models.

- [README.md](S3-need-driven/README.md) - Overview
- [use-cases.md](S3-need-driven/use-cases.md) - 4 major use cases with TCO
- [recommendation.md](S3-need-driven/recommendation.md) - Decision tree

**Key finding**: Break-even at 500 texts/month; rule-based → hybrid path for most teams

---

### S4: Strategic (Viability & ROI Analysis) ✅ COMPLETE

Strategic go/no-go decision framework with ROI models.

- [README.md](S4-strategic/README.md) - Overview
- [roi-analysis.md](S4-strategic/roi-analysis.md) - 3-year TCO, break-even analysis
- [recommendation.md](S4-strategic/recommendation.md) - **FINAL RECOMMENDATIONS**

**Key finding**: BUILD if volume > 500/month; 60-80% cost savings vs manual over 3 years

---

## Research Timeline

| Phase | Status | Duration | Output |
|-------|--------|----------|--------|
| S1: Rapid | ✅ Complete | 2-3 hours | Library landscape, MVP recommendations |
| S2: Comprehensive | ✅ Complete | 2-3 hours | Technical depth on neural approaches |
| S3: Need-driven | ✅ Complete | 1-2 hours | Use case TCO models |
| S4: Strategic | ✅ Complete | 1-2 hours | Strategic ROI analysis |
| **Total** | **✅ 100%** | **6-10 hours** | Complete research package |

---

## Executive Summary

### The Question
"What Python libraries exist for Chinese text simplification, and should I build one?"

### The Answer
**No turnkey libraries exist.** You must build using:
- jieba (segmentation)
- OpenCC (conversion)
- Custom simplification logic (rules or neural)

### The Recommendation
**BUILD** if:
- Volume > 500 texts/month
- Budget > $15K Year 1
- Have mid-level dev + Chinese speaker

**Start with**: Rule-based MVP (2-4 weeks, $15K, 70-80% accuracy)
**Upgrade to**: Hybrid when volume > 5K/month (add neural for complex cases)

### The ROI
- **Rule-based**: $25K over 3 years vs $108K manual (77% savings)
- **Hybrid**: $46K over 3 years vs $108K manual (57% savings)
- **Break-even**: 6-9 months at 1K texts/month

### The Risk
- Technology immature (no turnkey solutions)
- Must build custom (15-20% Year 1 cost ongoing)
- Quality ceiling: 85-90% with hybrid (not 100%)

**Mitigation**: Start small (rule-based MVP), iterate (hybrid), validate early (100 test texts)

---

## Critical Decision Points

### 1. Build vs Wait?
- **Build now** (2026-2027): Early mover advantage, data moat
- **Wait 2-3 years** (2028-2029): Mature libraries may emerge, lower risk

**Recommendation**: Build if volume > 500/month (ROI positive even if libraries emerge later)

### 2. Rule-Based vs Neural?
- **Rule-based**: Fast (2-4 weeks), cheap ($15K), 70-80% accuracy
- **Neural**: Slow (2-4 months), expensive ($60K), 85-90% accuracy

**Recommendation**: Rule-based → hybrid path (add neural only when needed)

### 3. Which Neural Model?
- **mT5-small**: Fast, good for < 10K/day
- **mT5-base**: Best balance (recommended)
- **mBART**: Highest quality, slowest

**Recommendation**: mT5-base + LoRA (1 week training, $500, production-ready)

### 4. How to Evaluate?
- **MVP**: HSK coverage (95%+) + spot checks (20 samples)
- **Production**: SARI (40+) + semantic similarity (0.75+) + human eval (200 samples quarterly)

---

## Implementation Path

**Week 1-4**: Rule-based MVP
- jieba + OpenCC + synonym dictionary
- 70-80% success rate
- $10K-15K

**Month 2-3**: Production hardening
- Monitoring, caching, error handling
- 1K texts/month capacity
- $5K-10K

**Month 4-6**: Hybrid (if needed)
- Add neural for complex cases
- 85-90% success rate
- $15K-25K

**Month 7-12**: Optimization
- Fine-tune on domain data
- < 500ms latency
- $5K-10K

**Year 2-3**: Maintenance
- Ongoing curation
- $5K-10K/year

---

## Key Resources

### Datasets
- [MCTS](https://github.com/blcuicall/mcts) - 691K training pairs
- [HSK 3.0 Lists](https://github.com/krmanik/HSK-3.0) - Vocabulary

### Libraries
- [jieba](https://github.com/fxsjy/jieba) - Segmentation
- [OpenCC](https://github.com/BYVoid/OpenCC) - Conversion
- [HanLP](https://hanlp.hankcs.com/) - NLP platform
- [mT5](https://huggingface.co/google/mt5-base) - Neural model

### Papers
- [MCTS Paper](https://arxiv.org/abs/2306.02796)
- [SARI Metric](https://aclanthology.org/Q16-1029/)

---

**Research completed**: 2026-01-29
**Researcher**: furiosa (Gas Town polecat)
**Research ID**: 1.154.1-chinese-text-simplification
**Protocol**: 4PS (Four-Pass Search)
**Status**: ✅ COMPLETE (S1-S4 all phases)
