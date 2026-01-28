# S3 Need-Driven Recommendations

**Experiment**: 1.033.2 Chinese Word Segmentation Libraries
**Pass**: S3 - Need-Driven Discovery
**Date**: 2026-01-28

## Executive Summary

Use case-driven decision matrix for selecting Chinese word segmentation tools. Focus on WHEN to use each tool rather than technical details.

## Decision Matrix

| Use Case | Primary Tool | Why | Alternative |
|----------|-------------|-----|-------------|
| **E-Commerce Search** | Jieba | Search engine mode, speed, custom dict | PKUSeg (indexing only) |
| **Medical Records** | PKUSeg (medicine) | 95.20% F1, domain model | LTP (multi-task) |
| **Social Media Analytics** | PKUSeg (web) | 94.21% F1 on Weibo | Jieba (real-time) |
| **Legal Documents** | PKUSeg (custom) | Trainable, high accuracy | LTP (parsing) |
| **News Processing** | PKUSeg (news) | 96.88% F1 on MSRA | LTP Small |
| **Traditional Chinese** | CKIP | 97.33% F1, Academia Sinica | LTP |
| **Real-Time Chatbot** | Jieba | <10ms latency | LTP Tiny (GPU) |
| **Academic Research** | LTP Base | 6 tasks, benchmarks | CKIP |
| **High-Throughput Batch** | LTP Legacy | 21,581 sent/s | Jieba |
| **Mobile/Embedded** | Jieba | 55 MB memory | N/A |

## Use Case Categories

### 1. Latency-Critical Applications
**Requirement**: <50ms p95 latency

**Recommended Tools**:
- Jieba: <10ms (CPU)
- LTP Tiny: 10-15ms (GPU)

**Use cases**: Chatbots, real-time translation, live search

### 2. Accuracy-Critical Applications
**Requirement**: >95% F1, patient/legal safety

**Recommended Tools**:
- PKUSeg (domain-specific): 95-97% F1
- CKIP (Traditional): 97.33% F1
- LTP Base (multi-task): 98.7% F1

**Use cases**: Medical records, legal contracts, academic research

### 3. Domain-Specific Applications
**Requirement**: Specialized terminology (medical, legal, finance)

**Recommended Tool**: PKUSeg
- Pre-trained: medicine, web, news, tourism
- Custom training: legal, finance, proprietary domains

**Use cases**: Healthcare, legal tech, social media, news

### 4. Traditional Chinese Applications
**Requirement**: Taiwan/HK text, historical documents

**Recommended Tool**: CKIP
- 97.33% F1 on Traditional Chinese
- Academia Sinica backing (Taiwan)

**Use cases**: Government docs, historical archives, Taiwan market

### 5. Multi-Task NLP Applications
**Requirement**: Segmentation + POS + NER + parsing + SRL

**Recommended Tool**: LTP
- 6 tasks in single pipeline
- Shared representations

**Use cases**: Research pipelines, semantic analysis, entity extraction

## Quick Start Guide

### E-Commerce Product Search

```python
import jieba
jieba.load_userdict("product_brands.txt")

query = "小米手机充电器"
segments = jieba.cut_for_search(query)
# ['小米', '手机', '小米手机', '充电', '充电器', '手机充电器']
```

**Why**: Fine-grained search mode improves recall

### Medical Records Processing

```python
import pkuseg

seg = pkuseg.pkuseg(model_name='medicine')
note = "患者被诊断为2型糖尿病并发肾病"
segments = seg.cut(note)
# ['患者', '被', '诊断', '为', '2型糖尿病', '并发', '肾病']
```

**Why**: Pre-trained medical model handles terminology

### Traditional Chinese Academic Corpus

```python
from ckiptagger import WS

ws = WS("./data", device=0)
text = ["蔡英文是台灣總統。"]
segments = ws(text)
# [['蔡英文', '是', '台灣', '總統', '。']]
```

**Why**: Highest accuracy for Traditional Chinese

### Multi-Task NLP Pipeline

```python
from ltp import LTP

ltp = LTP("LTP/small")
ltp.to("cuda")

output = ltp.pipeline(
    ["他叫汤姆去拿外衣。"],
    tasks=["cws", "pos", "ner", "dep", "srl"]
)
# Words, POS, entities, dependencies, semantic roles
```

**Why**: Complete NLP analysis in single call

## Anti-Patterns

### DO NOT Use Jieba For:
- ❌ Medical terminology (15-20 points lower F1)
- ❌ Legal contracts (accuracy critical)
- ❌ Academic corpus (reproducibility needed)

### DO NOT Use CKIP For:
- ❌ Simplified Chinese primary (use PKUSeg/LTP)
- ❌ Real-time API (too slow on CPU)
- ❌ Commercial proprietary (GPL copyleft)

### DO NOT Use PKUSeg For:
- ❌ Real-time (<100ms latency)
- ❌ Traditional Chinese (use CKIP)
- ❌ General text (Jieba faster, similar accuracy)

### DO NOT Use LTP For:
- ❌ Serverless (5-15s cold start)
- ❌ Single-task WS only (PKUSeg more accurate)
- ❌ Commercial without budget (licensing)

## Performance Guidelines

### Latency Targets

| Use Case | Target | Tool | Achievable |
|----------|--------|------|-----------|
| Search query | <50ms | Jieba | <10ms ✅ |
| Chatbot message | <100ms | Jieba / LTP Tiny | <15ms ✅ |
| Medical record | <1s | PKUSeg | ~500ms ✅ |
| Academic corpus | <5s | CKIP (GPU) | ~1s ✅ |

### Throughput Targets

| Use Case | Target | Tool | Achievable |
|----------|--------|------|-----------|
| Search API | 1K req/s | Jieba | 1K+ req/s ✅ |
| Batch analytics | 50K/hour | PKUSeg | 30K/hour ⚠️ |
| High-throughput | 100K/hour | LTP Legacy | 1M+/hour ✅ |

### Accuracy Targets

| Use Case | Target | Tool | Achievable |
|----------|--------|------|-----------|
| General text | >85% | Jieba | 85-90% ✅ |
| Medical text | >95% | PKUSeg | 95-97% ✅ |
| Traditional Chinese | >97% | CKIP | 97.33% ✅ |
| Multi-task NLP | >98% | LTP Base | 98.7% ✅ |

## Migration Strategies

### From Jieba to Higher Accuracy

**Scenario**: MVP with Jieba, need better accuracy

**Path**:
1. Identify low-accuracy segments (manual review)
2. Add custom dictionary terms (quick win: +5% F1)
3. If still insufficient, migrate to PKUSeg/CKIP
4. A/B test both models (10% → 50% → 100%)

### From PKUSeg to Real-Time

**Scenario**: Batch PKUSeg too slow for real-time

**Path**:
1. Cache frequent results (Redis/Memcached)
2. Pre-segment common phrases (e.g., FAQ)
3. Hybrid: Jieba for real-time, PKUSeg for indexing
4. Consider LTP Tiny on GPU (10x faster)

### Adding Multi-Task Capabilities

**Scenario**: Need entity extraction + dependency parsing

**Path**:
1. Keep existing segmentation tool
2. Add LTP for multi-task analysis
3. Use segmentation output as input to downstream models
4. Optionally migrate to LTP entirely (consolidation)

## Cost-Benefit Analysis

### Infrastructure Costs (Estimated AWS)

| Tool | Instance Type | Monthly Cost | Throughput |
|------|--------------|--------------|------------|
| Jieba (CPU) | t3.medium × 10 | $300 | 10K req/s |
| PKUSeg (CPU) | c5.2xlarge × 5 | $500 | 50 req/s |
| CKIP (GPU) | p3.2xlarge × 3 | $2,700 | 300 req/s |
| LTP (GPU) | p3.2xlarge × 3 | $2,700 | 600 req/s |
| LTP Legacy (CPU) | c5.9xlarge × 2 | $800 | 40K req/s |

**Cost/Performance Leader**: LTP Legacy (batch), Jieba (real-time)

### Development Costs

| Tool | Setup Time | Custom Training | Maintenance |
|------|-----------|----------------|-------------|
| Jieba | 1 day | N/A (dict only) | Low |
| CKIP | 3 days | Complex (source) | Medium |
| PKUSeg | 2 days | Easy (built-in) | Low |
| LTP | 5 days | Medium (fine-tune) | Medium |

**Ease of Use Leader**: Jieba (fastest setup, lowest maintenance)

## Summary

**Rule of Thumb**:
- **Speed > Accuracy**: Jieba
- **Accuracy > Speed**: PKUSeg / CKIP / LTP
- **Domain-Specific**: PKUSeg (6 pre-trained domains)
- **Traditional Chinese**: CKIP (97.33% F1)
- **Multi-Task NLP**: LTP (6 tasks)

**Start with**: Jieba (80% of use cases)
**Upgrade to**: PKUSeg (domain-specific), CKIP (Traditional), LTP (multi-task)

## Cross-References

- **S1 Rapid Discovery**: [recommendation.md](../S1-rapid/recommendation.md)
- **S2 Comprehensive**: [recommendation.md](../S2-comprehensive/recommendation.md)
- **S3 Use Cases**: [use-case-ecommerce.md](use-case-ecommerce.md), [use-case-medical.md](use-case-medical.md), etc.
- **S4 Strategic**: Long-term tool selection (to be created)
