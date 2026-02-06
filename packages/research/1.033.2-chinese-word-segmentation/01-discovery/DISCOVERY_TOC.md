# Chinese Word Segmentation: Discovery Phase

**Experiment ID**: 1.033.2
**Topic**: Chinese Word Segmentation Libraries
**Libraries**: Jieba, CKIP, pkuseg, LTP
**Status**: S1 Complete ✅ | S2-S4 Pending

---

## Table of Contents

### S1: Rapid Discovery ✅
**Status**: Complete
**Duration**: ~30 minutes
**Date**: 2026-01-28

- [Approach](./S1-rapid/approach.md) - Research methodology for S1
- [Jieba](./S1-rapid/jieba.md) - Most popular, fastest setup (81-89% F1, 400KB/s)
- [CKIP](./S1-rapid/ckip.md) - Best for Traditional Chinese (97.33% F1)
- [PKUSeg](./S1-rapid/pkuseg.md) - Domain-specific models (96.88% F1 on MSRA)
- [LTP](./S1-rapid/ltp.md) - Comprehensive NLP toolkit (98.7% F1, 6 tasks)
- [Recommendation](./S1-rapid/recommendation.md) - Use case guide and decision tree

**Key Findings**:
- No single "best" tool - depends on use case
- Jieba: Speed champion (400KB/s, easiest setup)
- CKIP: Traditional Chinese specialist (97.33% F1)
- PKUSeg: Domain-specific accuracy leader (medicine, social media)
- LTP: Only tool with semantic understanding (SRL, dependency parsing)

---

### S2: Comprehensive Discovery
**Status**: Not Started
**Planned**: TBD

**Scope**:
- Detailed algorithm analysis (BiLSTM vs CRF vs HMM vs Perceptron)
- Head-to-head benchmarks on same test corpus
- Memory/disk/CPU requirements
- Custom dictionary support comparison
- Mixed English/Chinese handling
- Deployment considerations (Docker, API, model serving)

---

### S3: Need-Driven Discovery
**Status**: Not Started
**Planned**: TBD

**Scope**:
- 3-5 real-world use cases mapped to library recommendations
- E.g., "E-commerce product search", "Medical records", "Social media analytics"
- Accuracy vs speed tradeoffs for each use case
- Cost analysis (infrastructure, licensing)

---

### S4: Strategic Discovery
**Status**: Not Started
**Planned**: TBD

**Scope**:
- Maturity assessment (maintenance, community, institutional backing)
- Long-term viability (development activity, funding)
- Migration paths (if switching tools later)
- Integration with modern ML stacks (Hugging Face, ONNX)
- Ecosystem considerations (documentation, tutorials, support)

---

## Quick Reference

### Speed Ranking
1. **LTP Legacy**: 21,581 sent/s (16-threaded)
2. **Jieba**: 400 KB/s (default mode)
3. **LTP Tiny**: 53 sent/s (neural)
4. **CKIP**: Moderate (GPU-accelerated)
5. **PKUSeg**: Slow (accuracy-focused)

### Accuracy Ranking (Domain-Specific)
1. **LTP Base**: 98.7% (internal benchmarks)
2. **CKIP**: 97.33% F1 (Traditional Chinese, ASBC)
3. **PKUSeg**: 96.88% F1 (Simplified news, MSRA)
4. **Jieba**: 81-89% F1 (general use)

### Ease of Setup
1. **Jieba**: `pip install jieba` (instant)
2. **PKUSeg**: `pip install pkuseg` (auto-downloads model)
3. **LTP**: `pip install ltp` (HuggingFace auto-download)
4. **CKIP**: `pip install ckiptagger` (manual 2GB download)

---

## Document Conventions

Each library document follows this structure:
1. **What It Is**: Overview and origin
2. **Key Characteristics**: Algorithm and features
3. **Speed**: Performance metrics
4. **Accuracy**: Benchmark results
5. **Ease of Use**: Installation and basic usage
6. **Maintenance**: Project status
7. **Best For**: Primary use cases
8. **Limitations**: Known constraints
9. **References**: Sources and links

---

## Related Experiments

- **1.033**: NLP Libraries (parent)
- **1.033.1**: Intent Classification Libraries (sibling)

---

## Next Actions

1. ✅ Complete S1-rapid discovery
2. ⏳ Await direction on S2-S4 execution
3. ⏳ Create DOMAIN_EXPLAINER.md (business-focused, CFO audience)
4. ⏳ Consider hands-on testing (install and benchmark all 4 tools)
