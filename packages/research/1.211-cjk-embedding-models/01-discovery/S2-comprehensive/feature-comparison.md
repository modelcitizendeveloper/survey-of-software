# Feature Comparison Matrix: CJK Embedding Models

## Executive Summary Comparison

| Model/Library | Best For | Key Strength | Key Weakness | Model Size Range |
|---------------|----------|--------------|--------------|------------------|
| **multilingual-e5** | Multilingual apps, SOTA performance | Best benchmarks, active development | Larger memory, newer (less proven) | 118M-560M |
| **M3E** | Chinese-only apps | Best Chinese performance, fast | Chinese-only, limited multilingual | 24M-340M |
| **LaBSE** | Cross-lingual retrieval | Best translation-pair retrieval | Older (2020), slower inference | ~470M |
| **sentence-transformers** | Flexible, ecosystem integration | 3,000+ models, framework maturity | Framework overhead, not a single model | Varies by model |
| **text2vec-chinese** | Simple Chinese projects | Easy API, Chinese docs | Lower performance, limited models | 102M |

---

## Language Support Matrix

| Model | Chinese (Simp) | Chinese (Trad) | Japanese | Korean | English | Other Languages |
|-------|----------------|----------------|----------|--------|---------|-----------------|
| multilingual-e5 | ★★★★★ | ★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | 100+ languages |
| M3E | ★★★★★ | ★★★ | ★ | ★ | ★★ | Limited |
| LaBSE | ★★★★ | ★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | 109 languages |
| sentence-transformers | Depends on model | Depends on model | Depends on model | Depends on model | Depends on model | Depends on model |
| text2vec-chinese | ★★★★ | ★★ | ✗ | ✗ | ★ | Minimal |

**Legend**: ★★★★★ = Excellent, ★★★★ = Good, ★★★ = Fair, ★★ = Limited, ★ = Poor, ✗ = Not supported

---

## Performance Benchmarks

### Chinese Semantic Similarity (Higher = Better)

| Benchmark | multilingual-e5-base | M3E-base | LaBSE | text2vec-base |
|-----------|---------------------|----------|-------|---------------|
| ATEC | 44.7 | **48.2** | 42.3 | 46.8 |
| BQ | 63.1 | **67.3** | 61.5 | 65.7 |
| LCQMC | 75.8 | **76.4** | 73.2 | 75.1 |
| PAWSX.zh | 58.9 | **61.5** | 56.7 | 59.3 |
| STSB.zh | 82.5 | **83.1** | 79.8 | 81.4 |
| **Average** | **65.0** | **67.3** | 62.7 | 65.7 |

**Winner**: M3E (consistently 2-5 points ahead on Chinese tasks)

### Chinese Retrieval Tasks (Higher = Better)

| Benchmark | multilingual-e5-base | M3E-base | LaBSE | text2vec-base |
|-----------|---------------------|----------|-------|---------------|
| T2Retrieval | **66.8** | 66.1 | 64.2 | 63.2 |
| DuRetrieval | 52.3 | **54.8** | 51.1 | 52.4 |
| MMarcoRetrieval.zh | **38.2** | 37.5 | 35.8 | 36.1 |
| CovidRetrieval | 78.9 | **80.2** | 77.3 | 76.5 |
| **Average** | **59.1** | **59.7** | 57.1 | 57.1 |

**Winner**: Tie between multilingual-e5 and M3E (task-dependent)

### Cross-Lingual Retrieval (Chinese-English)

| Benchmark | multilingual-e5-base | M3E-base | LaBSE | text2vec-base |
|-----------|---------------------|----------|-------|---------------|
| Tatoeba (zh-en) | 89.3 | N/A | **95.2** | N/A |
| BUCC (zh-en) | 96.1 | N/A | **96.5** | N/A |
| XQuAD (zh) | **68.7** | 62.1 | 65.3 | N/A |

**Winner**: LaBSE (purpose-built for cross-lingual retrieval)

---

## Inference Performance Comparison

### CPU Latency (sentences/second, i9-12900K, batch=1)

| Model | Small | Base | Large |
|-------|-------|------|-------|
| multilingual-e5 | ~400 | ~180 | ~85 |
| M3E | **~620** | **~240** | ~95 |
| LaBSE | N/A | ~140 | N/A |
| text2vec | N/A | ~220 | N/A |

**Winner**: M3E (smaller vocabulary = faster tokenization)

### GPU Throughput (sentences/second, A100 FP16, batch=32)

| Model | Small | Base | Large |
|-------|-------|------|-------|
| multilingual-e5 | ~2,400 | ~1,200 | ~550 |
| M3E | **~3,800** | **~1,500** | ~650 |
| LaBSE | N/A | ~980 | N/A |
| text2vec | N/A | ~1,400 | N/A |

**Winner**: M3E (consistently 20-30% faster)

### Memory Footprint (FP16)

| Model | Small | Base | Large |
|-------|-------|------|-------|
| multilingual-e5 | 236 MB | 556 MB | 1.1 GB |
| M3E | **48 MB** | **220 MB** | 680 MB |
| LaBSE | N/A | 940 MB | N/A |
| text2vec | N/A | 204 MB | N/A |

**Winner**: M3E (smallest vocabulary, most memory-efficient)

---

## Deployment & Operations

### ONNX Conversion Support

| Model | Support | Performance Gain | Ease of Conversion |
|-------|---------|------------------|-------------------|
| multilingual-e5 | ✓ | 1.3-1.5x | Easy (Optimum) |
| M3E | ✓ | 1.4-1.6x | Easy (Optimum) |
| LaBSE | ✓ | 1.2-1.4x | Moderate |
| text2vec | ✓ | 1.3x | Moderate |
| sentence-transformers | ✓ | Varies | Easy (built-in) |

### Quantization Support

| Model | INT8 Dynamic | INT8 Static | Accuracy Loss | Speedup |
|-------|--------------|-------------|---------------|---------|
| multilingual-e5 | ✓ | ✓ | <1% | 2x |
| M3E | ✓ | ✓ | <0.5% | 2.2x |
| LaBSE | ✓ | ✓ | ~1% | 1.8x |
| text2vec | ✓ | ✓ | ~1% | 2x |

### Vector Database Compatibility

| Model | Pinecone | Weaviate | Milvus | Qdrant | ElasticSearch |
|-------|----------|----------|--------|--------|---------------|
| multilingual-e5 | ✓ | ✓ | ✓ | ✓ | ✓ |
| M3E | ✓ | ✓ | ✓✓ | ✓ | ✓ |
| LaBSE | ✓ | ✓ | ✓ | ✓ | ✓ |
| text2vec | ✓ | ✓ | ✓✓ | ✓ | ✓✓ |
| sentence-transformers | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ |

**Legend**: ✓✓ = Native/official examples, ✓ = Community supported

### LLM/RAG Framework Integration

| Model | LangChain | LlamaIndex | Haystack | Semantic Kernel |
|-------|-----------|------------|----------|-----------------|
| multilingual-e5 | ✓✓ | ✓✓ | ✓ | ✓ |
| M3E | ✓ | ✓ | ✓ | ✓ |
| LaBSE | ✓ | ✓ | ✓ | ✓ |
| text2vec | ✓ | ✓ | Limited | Limited |
| sentence-transformers | ✓✓ | ✓✓ | ✓✓ | ✓✓ |

---

## Fine-Tuning & Customization

### Fine-Tuning Support

| Model | Official Support | Training API | Recommended Data | Compute (100K pairs) |
|-------|------------------|--------------|------------------|----------------------|
| multilingual-e5 | ✓ (via sentence-transformers) | Mature | 100K+ pairs | 1x A100, ~8 hrs |
| M3E | ✓ (via sentence-transformers) | Mature | 50K+ pairs | 1x V100, ~4 hrs |
| LaBSE | Community only | Limited | 50K+ pairs | 1x A100, ~12 hrs |
| text2vec | ✓ (built-in) | Simple | 30K+ pairs | 1x V100, ~3 hrs |
| sentence-transformers | ✓✓ | Comprehensive | Varies | Varies |

### Domain Adaptation Results (Average Improvement)

| Model | Legal | Medical | E-commerce | Finance |
|-------|-------|---------|------------|---------|
| multilingual-e5 | +6.7 pts | +8.3 pts | +11.2 pts | +9.1 pts |
| M3E | +12.7 pts | +9.3 pts | +14.1 pts | +10.8 pts |
| LaBSE | +5.2 pts | +6.8 pts | +8.9 pts | +7.3 pts |
| text2vec | +11.7 pts | +11.6 pts | +13.4 pts | +10.2 pts |

**Winner**: M3E and text2vec (Chinese-focused baselines + fine-tuning amplifies performance)

---

## Documentation & Support

### Documentation Quality

| Model | English | Chinese | API Docs | Tutorials | Examples |
|-------|---------|---------|----------|-----------|----------|
| multilingual-e5 | ★★★★ | ★★★ | ★★★★ | ★★★ | ★★★★ |
| M3E | ★★★ | ★★★★★ | ★★★ | ★★★★ | ★★★★ |
| LaBSE | ★★ | ★★ | ★★ | ★ | ★★ |
| text2vec | ★ | ★★★★★ | ★★★★ | ★★★★★ | ★★★★ |
| sentence-transformers | ★★★★★ | ★★★ | ★★★★★ | ★★★★★ | ★★★★★ |

### Community Support

| Model | GitHub Stars | Monthly Downloads | Stack Overflow | Active Maintenance |
|-------|--------------|-------------------|----------------|-------------------|
| multilingual-e5 | 1.8K (flagembedding) | 2.5M (HF) | Moderate | ✓✓ |
| M3E | 2.3K | 800K (HF) | Chinese forums | ✓✓ |
| LaBSE | Part of SBERT (19K) | 350K (HF) | Low | ✗ (2020 model) |
| text2vec | 5.2K | 50K/month (PyPI) | Chinese forums | ✓ |
| sentence-transformers | 19K | 10M+ | High | ✓✓ |

---

## Cost Analysis (1M Embeddings/Month)

### Self-Hosted (AWS t3.large, 8GB RAM, INT8 models)

| Model | Can Fit in 8GB? | Estimated Cost | Requests/Hour |
|-------|-----------------|----------------|---------------|
| multilingual-e5-small | ✓ | $60/month | 3K |
| multilingual-e5-base | ✓ | $60/month | 2K |
| M3E-base | ✓ | $60/month | 2.5K |
| LaBSE | ✓ | $60/month | 1.5K |
| text2vec-base | ✓ | $60/month | 2.2K |

**All models**: ~$60/month for self-hosting (no API fees, unlimited embeddings after compute cost)

### Serverless (AWS Lambda, 1GB memory)

| Model | Cold Start | Warm Latency | Cost per 1M Invocations |
|-------|------------|--------------|-------------------------|
| multilingual-e5-small | 1.0s | 45ms | $0.15 |
| M3E-small | 0.8s | 35ms | $0.12 |
| M3E-base | 2.8s | 120ms | $0.25 |

**Winner**: M3E-small (fastest cold start, lowest cost)

### Commercial API Comparison (for context)

- **OpenAI text-embedding-ada-002**: $0.10 per 1M tokens (~$0.13 per 1M sentences)
- **Cohere embed-multilingual-v3.0**: $0.10 per 1M tokens
- **Self-hosted CJK models**: $0.00 per sentence (after fixed compute cost)

**Cost Advantage**: Self-hosting for CJK is dramatically cheaper for high-volume use cases.

---

## Decision Matrix

### Use Case → Model Mapping

| Use Case | Best Choice | Alternative | Why |
|----------|-------------|-------------|-----|
| Chinese-only semantic search | M3E-base | text2vec-base | Best Chinese performance, fastest |
| Multilingual search (CJK + English) | multilingual-e5-base | sentence-transformers | SOTA, active development |
| Cross-lingual retrieval (zh↔en) | LaBSE | multilingual-e5-large | Purpose-built for translation |
| Japanese/Korean applications | multilingual-e5-base | LaBSE | No Chinese-specific models exist |
| Resource-constrained (edge/mobile) | M3E-small | multilingual-e5-small | Smallest memory, fastest |
| Maximum quality (no constraints) | multilingual-e5-large | M3E-large | Best benchmarks |
| Rapid prototyping (Chinese) | text2vec-base | M3E-base | Simplest API, turnkey |
| Uncertain language requirements | sentence-transformers + e5 | Start multilingual | Easy to switch models later |
| Domain-specific (need fine-tuning) | M3E-base | multilingual-e5-base | Strong baseline + fine-tuning |
| RAG pipeline (LangChain/LlamaIndex) | sentence-transformers + e5 | Any via sentence-transformers | Best ecosystem integration |

### Team Skill Profile → Model Mapping

| Team Profile | Recommended Approach |
|-------------|---------------------|
| Chinese-speaking, Chinese-only app | text2vec or M3E directly |
| English-speaking, multilingual app | sentence-transformers + multilingual-e5 |
| ML engineers, need customization | sentence-transformers + fine-tune any model |
| App developers, need simplicity | text2vec (Chinese) or sentence-transformers (multilingual) |
| Startup, uncertain requirements | sentence-transformers + multilingual-e5 (flexibility) |
| Enterprise, proven stability | LaBSE (mature) or sentence-transformers (ecosystem) |

---

## Key Takeaways

### Performance
1. **M3E wins Chinese-only benchmarks** by 2-5 points
2. **multilingual-e5 is SOTA for multilingual** tasks
3. **LaBSE best for cross-lingual** retrieval (translation-focused)
4. **text2vec competitive** but slightly behind M3E

### Speed
1. **M3E is fastest** (20-30% faster than multilingual models)
2. All models support ONNX + quantization (2x speedup)
3. GPU inference essential for high-volume (>1K req/sec)

### Flexibility
1. **sentence-transformers is the ecosystem** (3,000+ models, framework maturity)
2. Easy to switch models within sentence-transformers
3. M3E, multilingual-e5, LaBSE all usable via sentence-transformers

### Chinese-Specific
1. **M3E is the best Chinese-only model** (performance + speed)
2. **text2vec easiest for Chinese teams** (simple API, Chinese docs)
3. Multilingual models lag by 2-5 pts on Chinese tasks

### Future-Proofing
1. **sentence-transformers + multilingual-e5**: Most future-proof (ecosystem, flexibility, active development)
2. **M3E**: Future-proof for Chinese-only (active development, growing adoption)
3. **LaBSE**: Mature but aging (2020 release, no updates)
4. **text2vec**: Stable but slower innovation pace

### Cost
1. Self-hosting is dramatically cheaper than commercial APIs
2. All models run on modest hardware (8GB RAM sufficient for base models)
3. M3E is most memory-efficient (smallest vocabulary)

---

## Recommendation Framework

**Step 1: Language Requirements**
- Chinese only → M3E or text2vec
- Multilingual → multilingual-e5 or LaBSE
- Japanese/Korean → multilingual-e5 (no CJK-specific alternatives)

**Step 2: Performance vs. Simplicity**
- Need SOTA performance → M3E (Chinese) or multilingual-e5 (multilingual)
- Need simplicity → text2vec (Chinese) or sentence-transformers (multilingual)

**Step 3: Team Preferences**
- Chinese-speaking team, Chinese app → text2vec
- English-speaking team or mixed languages → sentence-transformers + model of choice

**Step 4: Future Requirements**
- Certain about language scope → Use specialized model
- Uncertain or expect to expand → Start with sentence-transformers + multilingual-e5

**Default Recommendation**: **sentence-transformers + multilingual-e5-base** (or M3E-base for Chinese-only) balances performance, flexibility, and future-proofing for most teams.
