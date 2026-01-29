# Feature Comparison Matrix: Multilingual & CJK LLMs

## Executive Summary Comparison

| Model | Best For | CJK Strength | Cost (1M req/mo) | Self-Host |
|-------|----------|--------------|------------------|-----------|
| **XLM-R** | Multi-CJK classification | ⭐⭐⭐⭐ Balanced | $500-1,000 | ✅ Yes |
| **ERNIE** | Chinese-dominant apps | ⭐⭐⭐⭐⭐ Chinese-best | $500-1,000 | ✅ Yes |
| **BLOOM** | Multilingual generation | ⭐⭐⭐ Chinese strong | $1,800-6,000 | ✅ Yes |
| **GPT-4** | Quality-critical, low volume | ⭐⭐⭐⭐⭐ All CJK | $15,000-45,000 | ❌ No |
| **mBERT** | Budget learning projects | ⭐⭐ Outdated | $50-80 | ✅ Yes |

---

## Technical Specifications Comparison

### Architecture

| Model | Type | Parameters | Layers | Context Length | Vocabulary |
|-------|------|------------|--------|----------------|------------|
| **XLM-R Base** | Encoder | 270M | 12 | 512 | 250K |
| **XLM-R Large** | Encoder | 550M | 24 | 512 | 250K |
| **ERNIE 3.0 Base** | Encoder | 260M | 12 | 512 | - |
| **ERNIE 3.0 Titan** | Both | 10T | - | - | - |
| **BLOOM-3B** | Decoder | 3B | 30 | 2048 | 250K |
| **BLOOM-7B1** | Decoder | 7.1B | 30 | 2048 | 250K |
| **BLOOM-176B** | Decoder | 176B | 70 | 2048 | 250K |
| **GPT-4** | Decoder | ~1.7T+ | - | 8K-128K | - |
| **mBERT** | Encoder | 110M | 12 | 512 | 119K |

### Training Corpus

| Model | Corpus Size | CJK Data % | Languages | Primary Source |
|-------|-------------|------------|-----------|----------------|
| **XLM-R** | 2.5TB | ~14% | 100 | CommonCrawl |
| **ERNIE** | 4TB | ~50% (Chinese) | Primarily Chinese | Baidu + public |
| **BLOOM** | 1.6TB | ~5% | 46 | ROOTS dataset |
| **GPT-4** | Unknown | Unknown | 50+ | Proprietary |
| **mBERT** | Wikipedia | ~10% | 104 | Wikipedia only |

---

## CJK Performance Comparison

### Benchmark Scores (Higher is Better)

**XNLI (Cross-lingual Natural Language Inference)**

| Model | Chinese | Japanese | Korean | Average |
|-------|---------|----------|--------|---------|
| GPT-4 | ~86 | ~82 | ~80 | 82.7 |
| ERNIE 3.0 | 85 | - | - | 85.0 (CH only) |
| XLM-R Large | 79.3 | 72.6 | 76.5 | 76.1 |
| BLOOM-176B | ~75 | ~68 | ~70 | 71.0 |
| mBERT | 74.2 | 68.5 | 71.8 | 71.5 |

**CLUE (Chinese Language Understanding)**

| Model | Score | Rank |
|-------|-------|------|
| ERNIE 3.0 | 83.5 | 🥇 |
| GPT-4 | ~82 | 🥈 |
| XLM-R Large | 72.8 | 🥉 |
| mBERT | ~68 | - |
| BLOOM | ~70 | - |

### Tokenization Efficiency (Tokens per Character)

Lower is better (fewer tokens = lower cost, faster processing)

| Model | Chinese | Japanese | Korean | vs English Penalty |
|-------|---------|----------|--------|-------------------|
| ERNIE | 1.0-1.2 | - | - | 1.3-1.6x |
| GPT-4 | 1.3-1.6 | 1.8-2.2 | 1.5-1.9 | 1.7-2.9x |
| BLOOM | 1.5-1.8 | 2.3-2.8 | 1.7-2.2 | 2.0-3.7x |
| XLM-R | 1.7 | 2.1 | 1.9 | 2.3-2.8x |
| mBERT | 2.5-3.0 | 3.5-4.5 | 2.8-3.5 | 3.3-6.0x |

**Impact**: mBERT requires 2-4x more tokens than modern models for CJK text

---

## Deployment Comparison

### Hardware Requirements (Minimum for Production)

| Model | GPU Memory | Recommended GPU | CPU Viable? | Multi-GPU? |
|-------|------------|-----------------|-------------|------------|
| **XLM-R Base** | 2-4 GB | T4, V100 | Yes (slow) | No |
| **XLM-R Large** | 4-8 GB | V100, A100 | Marginal | No |
| **ERNIE Base** | 2-4 GB | T4, V100 | Yes (slow) | No |
| **BLOOM-3B** | 6-8 GB | T4, RTX 3090 | No | No |
| **BLOOM-7B1** | 14-16 GB | V100, A100 40GB | No | No |
| **BLOOM-176B** | 352+ GB | 8× A100 80GB | No | Required |
| **GPT-4** | N/A (API) | N/A | N/A | N/A |
| **mBERT** | 1-2 GB | Any GPU | Yes | No |

### Inference Latency (Single Request)

| Model | GPU Latency | CPU Latency | Batch Throughput |
|-------|-------------|-------------|------------------|
| mBERT | 10-30ms | 100-300ms | 80-150/sec |
| XLM-R Base | 20-50ms | 200-500ms | 50-100/sec |
| XLM-R Large | 30-80ms | 500-1500ms | 30-60/sec |
| ERNIE Base | 15-40ms | 200-500ms | 60-120/sec |
| BLOOM-3B | 50-150ms | N/A | 20-40/sec |
| BLOOM-7B1 | 200-500ms | N/A | 10-20/sec |
| BLOOM-176B | 1-3 sec | N/A | 5-10/sec |
| GPT-4 | 1-5 sec | N/A | - |

---

## Cost Analysis Comparison

### Self-Hosted Infrastructure Costs (1M requests/month)

| Model | AWS Instance | $/hour | Monthly Cost | Break-even vs GPT-4 |
|-------|--------------|--------|--------------|---------------------|
| **mBERT** | g4dn.xlarge | $0.53 | $50-80 | Always cheaper |
| **XLM-R Base** | p3.2xlarge | $3.06 | $500-1,000 | 30K requests |
| **XLM-R Large** | p3.2xlarge | $3.06 | $750-1,500 | 50K requests |
| **ERNIE Base** | p3.2xlarge | $3.06 | $500-1,000 | 30K requests |
| **BLOOM-3B** | g5.2xlarge | $1.21 | $1,800 | 120K requests |
| **BLOOM-7B1** | p4d.2xlarge | $4.10 | $6,000 | 400K requests |
| **BLOOM-176B** | p4d.24xlarge | $32.77 | $545,000 | Never |

### API Costs (Commercial Models)

| Service | Input Cost/1K tokens | Output Cost/1K tokens | CJK Penalty |
|---------|----------------------|-----------------------|-------------|
| **GPT-4** | $0.03 | $0.06 | 1.3-2.2x tokens |
| **GPT-4-Turbo** | $0.01 | $0.03 | 1.3-2.2x tokens |
| **ERNIE API** | ~$0.008 | ~$0.008 | 1.0-1.2x tokens |

**Example: 1M requests, 200 tokens in, 150 tokens out**
- GPT-4: $15,000/month (factoring CJK penalty)
- GPT-4-Turbo: $5,000/month
- ERNIE API: $1,200/month (Chinese only)

### Total Cost of Ownership (TCO) Considerations

| Factor | Self-Hosted | API (GPT-4) | API (ERNIE) |
|--------|-------------|-------------|-------------|
| **Infrastructure** | $500-6,000/mo | $0 | $0 |
| **Engineering** | 2-4 weeks setup | Hours | Hours |
| **Maintenance** | Ongoing | None | None |
| **Scaling** | Manual | Auto | Auto |
| **Monitoring** | DIY | Minimal | Minimal |
| **Break-even** | >30K-500K req/mo | <30K req/mo | <100K req/mo |

---

## Capabilities Matrix

### Task Suitability

| Task | XLM-R | ERNIE | BLOOM | GPT-4 | mBERT |
|------|-------|-------|-------|-------|-------|
| **Text Classification** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Named Entity Recognition** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Semantic Search** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Text Generation** | ❌ | ❌ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ |
| **Translation** | ⭐⭐⭐ | ⭐⭐⭐⭐ (CH) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Question Answering** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (CH) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Chatbots** | ❌ | ❌ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ |
| **Summarization** | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| **Code-switching** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |

### Language Coverage

| Language | XLM-R | ERNIE | BLOOM | GPT-4 | mBERT |
|----------|-------|-------|-------|-------|-------|
| **Chinese** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Japanese** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Korean** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **English** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Other Languages** | ⭐⭐⭐⭐ (100) | ⭐⭐ | ⭐⭐⭐⭐ (46) | ⭐⭐⭐⭐⭐ (50+) | ⭐⭐⭐ (104) |

---

## Strategic Factors Comparison

### Licensing and Openness

| Model | License | Model Weights | Training Code | Commercial Use |
|-------|---------|---------------|---------------|----------------|
| XLM-R | MIT | ✅ Open | ✅ Open | ✅ Unrestricted |
| ERNIE | Apache 2.0 | ✅ Open (most) | ✅ Open | ✅ Allowed |
| BLOOM | RAIL | ✅ Open | ✅ Open | ⚠️ Restricted |
| GPT-4 | Proprietary | ❌ Closed | ❌ Closed | ✅ API only |
| mBERT | Apache 2.0 | ✅ Open | ✅ Open | ✅ Unrestricted |

### Ecosystem and Support

| Model | Framework | Community Size | Documentation | Production Tools |
|-------|-----------|----------------|---------------|------------------|
| XLM-R | PyTorch/HF | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| ERNIE | PaddlePaddle | ⭐⭐⭐ (China) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| BLOOM | PyTorch/HF | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| GPT-4 | API | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| mBERT | PyTorch/HF/TF | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

### Data Privacy and Compliance

| Model | Self-Hostable | Data Leaves Premises | GDPR Compliant | China Deployment |
|-------|---------------|----------------------|----------------|------------------|
| XLM-R | ✅ Yes | ❌ No (if self-hosted) | ✅ Yes | ✅ Yes |
| ERNIE | ✅ Yes | ⚠️ If using Baidu API | ⚠️ China-based | ⭐ Ideal |
| BLOOM | ✅ Yes | ❌ No (if self-hosted) | ✅ Yes | ✅ Yes |
| GPT-4 | ❌ No | ✅ Yes (US servers) | ⚠️ Concerns | ❌ Blocked |
| mBERT | ✅ Yes | ❌ No (if self-hosted) | ✅ Yes | ✅ Yes |

---

## Decision Matrix by Use Case

### Use Case: Chinese-Only Application

| Criterion | ERNIE | XLM-R | GPT-4 | Winner |
|-----------|-------|-------|-------|--------|
| Performance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ERNIE/GPT-4 |
| Cost | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ERNIE |
| Tokenization | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ERNIE |
| Ease of Use | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | XLM-R/GPT-4 |
| **Recommendation** | 🥇 ERNIE | - | - | - |

### Use Case: Multi-CJK (Chinese + Japanese + Korean)

| Criterion | XLM-R | BLOOM | GPT-4 | Winner |
|-----------|-------|-------|-------|--------|
| Performance | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | GPT-4 |
| Cost | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | XLM-R |
| Balance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | XLM-R/GPT-4 |
| Self-Host | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ❌ | XLM-R |
| **Recommendation** | 🥇 XLM-R | - | - | (Self-host) |
| **Recommendation** | - | - | 🥇 GPT-4 | (API/Quality) |

### Use Case: Text Generation (Chatbot, Summarization)

| Criterion | BLOOM | GPT-4 | Winner |
|-----------|-------|-------|--------|
| Quality | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | GPT-4 |
| Cost | ⭐⭐⭐ | ⭐⭐ | BLOOM |
| Open-source | ⭐⭐⭐⭐⭐ | ❌ | BLOOM |
| Ease of Use | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | GPT-4 |
| **Recommendation** | 🥇 BLOOM | - | (Open/Cost) |
| **Recommendation** | - | 🥇 GPT-4 | (Quality) |

### Use Case: Classification/NER (Understanding Tasks)

| Criterion | XLM-R | ERNIE (CH) | Winner |
|-----------|-------|------------|--------|
| Performance | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ERNIE (CH only) |
| Multi-CJK | ⭐⭐⭐⭐⭐ | ⭐⭐ | XLM-R |
| Cost | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ERNIE |
| Ecosystem | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | XLM-R |
| **Recommendation** | 🥇 XLM-R | - | (Multi-CJK) |

---

## Summary Recommendations by Scenario

| Scenario | 1st Choice | 2nd Choice | Avoid |
|----------|------------|------------|-------|
| **Chinese-only, budget** | ERNIE | XLM-R | GPT-4 |
| **Chinese-only, quality** | GPT-4 | ERNIE | mBERT |
| **Multi-CJK, self-host** | XLM-R | BLOOM-3B | mBERT |
| **Multi-CJK, API** | GPT-4-Turbo | - | ERNIE |
| **Generation, open-source** | BLOOM-7B | BLOOM-3B | XLM-R |
| **Generation, quality** | GPT-4 | GPT-4-Turbo | BLOOM |
| **Classification/NER** | XLM-R | ERNIE (CH) | mBERT |
| **Prototype/MVP** | GPT-4 | XLM-R | BLOOM-176B |
| **High-volume (>1M/mo)** | XLM-R | ERNIE | GPT-4 |
| **Low-volume (<100K/mo)** | GPT-4 | XLM-R | Self-host |
| **Learning/Research** | XLM-R | mBERT | GPT-4 |
| **China deployment** | ERNIE | XLM-R | GPT-4 |

---

## Key Takeaways

1. **No universal winner**: Choice depends on language mix, task type, volume, and budget
2. **XLM-R is the safe default** for multi-CJK understanding tasks with self-hosting
3. **ERNIE dominates Chinese-only** applications (performance + tokenization efficiency)
4. **GPT-4 wins on quality** but at significant cost (especially for high volume)
5. **BLOOM fills the open-source generation gap** but requires careful size selection
6. **mBERT is obsolete** for production (use only for learning or extreme budget constraints)
7. **Tokenization efficiency matters** - can change TCO by 2-3x for CJK applications
8. **Break-even analysis critical** - self-hosting vs API depends heavily on volume
