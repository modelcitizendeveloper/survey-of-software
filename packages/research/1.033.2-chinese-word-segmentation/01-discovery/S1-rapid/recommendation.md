# S1 RAPID DISCOVERY: Recommendations

**Experiment**: 1.033.2 Chinese Word Segmentation Libraries
**Date**: 2026-01-28
**Duration**: ~30 minutes

## Executive Summary

Identified 4 production-ready Chinese word segmentation libraries with distinct strengths optimized for different use cases:

1. **Jieba** - Best for rapid prototyping and general-purpose applications requiring speed
2. **CKIP** - Best for Traditional Chinese with highest accuracy (97.33% F1)
3. **PKUSeg** - Best for domain-specific applications (medicine, social media, tourism)
4. **LTP** - Best for comprehensive NLP pipelines requiring semantic analysis

**Quick recommendation**: Start with **Jieba** for prototyping, upgrade to **PKUSeg** if accuracy matters, choose **CKIP** for Traditional Chinese, or select **LTP** if you need a complete NLP toolkit.

---

## Quick Comparison Table

| Library | Speed | Accuracy (F1) | Character Type | Domain Support | Best For |
|---------|-------|--------------|---------------|----------------|----------|
| **Jieba** | Fast (400KB/s) | 81-89% | Both | General | Rapid prototyping, real-time |
| **CKIP** | Moderate | **97.33%** | Traditional | General | Taiwan/HK text, research |
| **PKUSeg** | Slow | **96.88%** | Simplified | 6 domains | Medicine, social media, batch |
| **LTP** | Variable (39-21K sent/s) | 88-99% | Both | General | Multi-task NLP pipelines |

---

## Detailed Comparison

### Speed Performance

| Tool | Metric | Notes |
|------|--------|-------|
| **Jieba** | 400 KB/s (default mode) | 3.3x faster with multiprocessing |
| **CKIP** | Moderate (neural overhead) | GPU acceleration available |
| **PKUSeg** | "Much slower than Jieba" | Multi-threaded batch processing |
| **LTP Tiny** | 53 sent/s (neural) | Multiple model sizes available |
| **LTP Legacy** | 21,581 sent/s (16-thread) | Fastest option for production |

### Accuracy Performance

| Dataset | Jieba | CKIP | PKUSeg | LTP |
|---------|-------|------|--------|-----|
| **ASBC (Traditional)** | 89.80% | **97.33%** | — | — |
| **MSRA (News)** | 88.42% | — | **96.88%** | — |
| **PKU** | 81.2% | — | 95.4% | 88.7% |
| **Internal benchmarks** | — | — | — | **98.7%** (Base) |

**Key insight**: No single "best" accuracy - varies by dataset and domain.

---

## Use Case Recommendations

### 1. Real-Time Applications (Web Services, APIs)
**Recommendation**: **Jieba** or **LTP Legacy**

**Why**:
- Jieba: 400KB/s with easy setup, good enough accuracy for most cases
- LTP Legacy: 21,581 sent/s if you need POS tagging alongside segmentation
- Both handle high throughput without GPU requirements

**Trade-off**: Lower accuracy (81-89%) vs specialized tools

---

### 2. Traditional Chinese Text (Taiwan, Hong Kong, Historical)
**Recommendation**: **CKIP**

**Why**:
- Highest accuracy for Traditional Chinese (97.33% F1)
- Institutional backing from Academia Sinica (Taiwan's premier research institution)
- Multi-task support (segmentation + POS + NER)

**Trade-off**: 2GB model download, GPU recommended, GNU GPL v3 license

---

### 3. Domain-Specific Applications
**Recommendation**: **PKUSeg**

**Why**:
- Pre-trained models for medicine (96.88% F1), social media (94.21% F1), tourism
- Highest accuracy on domain-specific corpora
- Custom training support for proprietary domains

**Trade-off**: Significantly slower than Jieba, requires knowing your domain

**Domains available**: news, web, medicine, tourism, mixed, default_v2

---

### 4. Comprehensive NLP Pipelines
**Recommendation**: **LTP**

**Why**:
- Only tool offering semantic role labeling and dependency parsing
- 6 fundamental NLP tasks in single framework (CWS, POS, NER, DP, SDP, SRL)
- Flexible speed/accuracy with multiple model sizes (Tiny → Base)
- Enterprise backing (HIT, Baidu, Tencent)

**Trade-off**: Commercial licensing required, overkill if you only need segmentation

**Model options**: Tiny (53 sent/s, 96.8%), Small (43 sent/s, 98.4%), Base (39 sent/s, 98.7%)

---

### 5. Rapid Prototyping / Getting Started
**Recommendation**: **Jieba**

**Why**:
- Simplest installation: `pip install jieba`
- No model downloads required
- Works out of the box with no configuration
- Extensive documentation and community support (34.7k stars)

**When to graduate**: Switch to PKUSeg when accuracy becomes critical, or CKIP for Traditional Chinese

---

### 6. Research / Academic Applications
**Recommendation**: **CKIP** or **LTP**

**Why**:
- Both have published benchmarks and academic papers
- CKIP: Best for word segmentation research (AAAI 2020 paper)
- LTP: Best for multi-task research (EMNLP 2021 paper, semantic understanding)
- Free for university/research use

---

### 7. Batch Processing (Offline, Large Corpora)
**Recommendation**: **PKUSeg** or **LTP Legacy**

**Why**:
- PKUSeg: Highest accuracy for offline processing with multi-threading
- LTP Legacy: Extreme speed (21,581 sent/s) if accuracy is sufficient

**Trade-off**: PKUSeg slower but more accurate, LTP Legacy faster but lower accuracy

---

## Decision Tree

```
START
  │
  ├─ Need Traditional Chinese? ───[YES]──> CKIP (97.33% F1, Academia Sinica)
  │
  ├─ Need semantic analysis? ─────[YES]──> LTP (SRL, dependency parsing)
  │
  ├─ Have specific domain? ───────[YES]──> PKUSeg (medicine, social, tourism)
  │
  ├─ Need maximum speed? ─────────[YES]──> Jieba (400KB/s) or LTP Legacy (21K sent/s)
  │
  ├─ Just getting started? ───────[YES]──> Jieba (simplest setup)
  │
  └─ Default choice ──────────────────────> Jieba → upgrade to PKUSeg if accuracy matters
```

---

## Key Differentiators

| Library | Primary Strength |
|---------|-----------------|
| **Jieba** | Easiest to use, fastest to deploy, community favorite |
| **CKIP** | Highest accuracy for Traditional Chinese (Taiwan/HK) |
| **PKUSeg** | Domain-specific models for specialized accuracy |
| **LTP** | Complete NLP ecosystem with semantic understanding |

---

## Installation Comparison

| Library | Installation | First Run | Complexity |
|---------|-------------|-----------|------------|
| **Jieba** | `pip install jieba` | Instant (lazy loading) | ★☆☆☆☆ |
| **CKIP** | `pip install ckiptagger` + 2GB download | Slow (model load) | ★★★☆☆ |
| **PKUSeg** | `pip install pkuseg` | Model auto-downloads | ★★☆☆☆ |
| **LTP** | `pip install ltp` | Model auto-downloads from HF | ★★★☆☆ |

---

## Licensing Considerations

| Library | License | Commercial Use |
|---------|---------|---------------|
| **Jieba** | MIT | ✅ Free |
| **CKIP** | GNU GPL v3.0 | ⚠️  Copyleft (derivatives must be GPL) |
| **PKUSeg** | MIT | ✅ Free |
| **LTP** | Apache 2.0 | ⚠️  Requires licensing for commercial use |

**Important**: LTP is free for universities/research but requires commercial licensing from HIT.

---

## Common Use Case Matrix

| Use Case | Best Choice | Alternative |
|----------|------------|-------------|
| E-commerce product search | Jieba | PKUSeg (web domain) |
| Medical records processing | PKUSeg (medicine) | LTP (if need NER) |
| Social media analytics (Weibo) | PKUSeg (web) | Jieba (if speed critical) |
| Taiwan government documents | CKIP | — |
| News aggregation | PKUSeg (news) | Jieba |
| Research NLP pipelines | LTP | CKIP |
| Real-time chatbots | Jieba | LTP Legacy |
| Academic corpus analysis | CKIP | LTP |

---

## Recommendations by Team Size / Resources

### Solo Developer / Startup
**Recommendation**: **Jieba** → **PKUSeg** (when accuracy needed)
- Start with Jieba for MVP (fastest time-to-market)
- Upgrade to PKUSeg when users complain about segmentation quality
- Avoid LTP commercial licensing complexity initially

### Research Lab / University
**Recommendation**: **CKIP** or **LTP**
- Both free for academic use
- Choose CKIP for Traditional Chinese focus
- Choose LTP for comprehensive multi-task research

### Enterprise with ML Team
**Recommendation**: **PKUSeg** with custom training or **LTP** with commercial license
- PKUSeg: Train custom models on proprietary domain data
- LTP: Get enterprise support and comprehensive NLP pipeline
- Budget for LTP commercial licensing from HIT

---

## Next Steps for S2 (Comprehensive Discovery)

1. **Benchmark all 4 tools** on same test corpus for direct comparison
2. **Deep dive into algorithms**: How do BiLSTM (CKIP) vs CRF (PKUSeg) vs HMM (Jieba) differ?
3. **Deployment considerations**: Docker, API wrapping, model serving
4. **Memory and disk requirements**: Exact footprint for each tool
5. **Custom dictionary evaluation**: Which tool has best support for domain terms?
6. **Multi-language support**: Do any handle English/Chinese mixed text well?

---

## References

- [Jieba GitHub](https://github.com/fxsjy/jieba) | [Performance Comparison](https://zhuanlan.zhihu.com/p/64409753)
- [CKIP GitHub](https://github.com/ckiplab/ckiptagger) | [AAAI 2020 Paper](https://ojs.aaai.org/index.php/AAAI/article/view/6338)
- [PKUSeg GitHub](https://github.com/lancopku/pkuseg-python) | [ArXiv Paper](https://arxiv.org/abs/1906.11455)
- [LTP GitHub](https://github.com/HIT-SCIR/ltp) | [EMNLP 2021 Paper](https://aclanthology.org/2021.emnlp-demo.6/)
