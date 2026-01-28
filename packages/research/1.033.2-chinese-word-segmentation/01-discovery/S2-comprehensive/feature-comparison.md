# S2 Feature Comparison Matrix

**Experiment**: 1.033.2 Chinese Word Segmentation Libraries
**Pass**: S2 - Comprehensive Discovery
**Date**: 2026-01-28

## Executive Summary

Side-by-side comparison of Jieba, CKIP, PKUSeg, and LTP across architecture, performance, deployment, and integration dimensions.

## Algorithm Architecture

| Feature | Jieba | CKIP | PKUSeg | LTP |
|---------|-------|------|--------|-----|
| **Core Algorithm** | HMM + Trie + DAG | BiLSTM + Attention | CRF | BERT + Multi-Task |
| **Segmentation Method** | Dictionary + Statistical | Sequence Labeling (BIO) | Sequence Labeling (BIO) | Sequence Labeling (BIO) |
| **Unknown Word Handling** | HMM (Viterbi) | Character-level BiLSTM | CRF character features | BERT subword tokens |
| **Training Approach** | Pre-built dictionary | Multi-task neural training | CRF feature learning | Knowledge distillation |
| **Model Type** | Hybrid (rule + statistical) | Deep learning | Machine learning | Deep learning |
| **Context Window** | Limited (HMM) | Full sentence (BiLSTM) | ±2 chars (CRF features) | Full document (BERT) |

## Performance Metrics

### Speed Comparison

| Metric | Jieba | CKIP | PKUSeg | LTP (Small) | LTP (Legacy) |
|--------|-------|------|--------|-------------|--------------|
| **CPU Speed** | 400 KB/s | ~5 sent/s | ~100 char/s | ~43 sent/s | 21,581 sent/s |
| **GPU Speed** | N/A | ~50 sent/s | N/A | ~200 sent/s | N/A |
| **Relative Speed** | ★★★★★ (Fastest) | ★★☆☆☆ | ★☆☆☆☆ (Slowest) | ★★★☆☆ | ★★★★★ (Fastest) |
| **Parallel Processing** | ✅ (Linux/Mac) | ✅ (GPU) | ✅ (Multi-thread) | ✅ (GPU) | ✅ (Multi-thread) |

**Notes**:
- Jieba: 2000x faster than PKUSeg on CPU
- LTP Legacy: 500x faster than LTP Small
- CKIP: GPU strongly recommended

### Accuracy Comparison

| Dataset | Jieba | CKIP | PKUSeg | LTP Base |
|---------|-------|------|--------|----------|
| **ASBC (Traditional Chinese)** | 89.80% | **97.33%** | — | — |
| **MSRA (News)** | 88.42% | — | **96.88%** | — |
| **PKU** | 81.2% | — | 95.4% | 88.7% |
| **Internal benchmarks** | — | — | — | **98.7%** |
| **Average F1 (cross-domain)** | 81-89% | ~97% | 91-97% | 97-99% |

**Accuracy Rating**:
- Jieba: ★★★☆☆ (81-89%)
- CKIP: ★★★★★ (97%)
- PKUSeg: ★★★★★ (96-97%)
- LTP: ★★★★★ (97-99%)

**Notes**:
- Different benchmarks = different results
- CKIP best for Traditional Chinese
- PKUSeg best for domain-specific Simplified
- LTP best for multi-task accuracy

### Memory Footprint

| Component | Jieba | CKIP | PKUSeg | LTP Base | LTP Small | LTP Tiny |
|-----------|-------|------|--------|----------|-----------|----------|
| **Model Size** | 20 MB | 2 GB | 70 MB | 500 MB | 250 MB | 100 MB |
| **Runtime Memory (CPU)** | 55 MB | 4-6 GB | 120 MB | 2 GB | 1.5 GB | 1 GB |
| **Runtime Memory (GPU)** | N/A | 2-3 GB | N/A | 2 GB | 1.5 GB | 1 GB |
| **Total Disk Space** | 20 MB | 2.05 GB | 100 MB | 500 MB | 280 MB | 130 MB |

**Memory Rating**:
- Jieba: ★★★★★ (Lightest)
- CKIP: ★☆☆☆☆ (Heaviest)
- PKUSeg: ★★★★☆
- LTP Tiny: ★★★★☆
- LTP Small: ★★★☆☆
- LTP Base: ★★☆☆☆

## Language Support

| Feature | Jieba | CKIP | PKUSeg | LTP |
|---------|-------|------|--------|-----|
| **Simplified Chinese** | ✅ Excellent | ⚠️ Secondary | ✅ Primary | ✅ Excellent |
| **Traditional Chinese** | ✅ Good | ✅ Primary | ⚠️ Limited | ✅ Good |
| **Mixed (Simp + Trad)** | ✅ Yes | ✅ Yes | ⚠️ Limited | ✅ Yes |
| **Chinese + English** | ✅ Preserves English | ✅ Preserves English | ✅ Preserves English | ✅ Preserves English |
| **Dialect Support** | ❌ No | ❌ No | ❌ No | ❌ No |

**Best for Traditional Chinese**: CKIP (97.33% F1)
**Best for Simplified Chinese**: PKUSeg (96.88% F1 on MSRA)
**Best for Mixed Text**: Jieba or LTP (general-purpose)

## Segmentation Modes

| Mode | Jieba | CKIP | PKUSeg | LTP |
|------|-------|------|--------|-----|
| **Precise Mode** | ✅ Default | ✅ Only mode | ✅ Only mode | ✅ Only mode |
| **Full Mode** | ✅ All possible words | ❌ No | ❌ No | ❌ No |
| **Search Engine Mode** | ✅ Fine-grained | ❌ No | ❌ No | ❌ No |
| **Deep Learning Mode** | ✅ Paddle (optional) | ✅ BiLSTM (default) | ❌ No | ✅ BERT (default) |

**Most Flexible**: Jieba (4 modes)
**Most Specialized**: CKIP, PKUSeg, LTP (single high-accuracy mode)

## Custom Dictionary Support

| Feature | Jieba | CKIP | PKUSeg | LTP |
|---------|-------|------|--------|-----|
| **User Dictionary** | ✅ Excellent | ✅ Weighted lists | ✅ Word lists | ⚠️ Limited (workaround) |
| **Add Word (API)** | ✅ `add_word()` | ✅ `recommend_dictionary` | ✅ `user_dict` | ❌ No direct API |
| **Delete Word (API)** | ✅ `del_word()` | ❌ No | ❌ No | ❌ No |
| **Adjust Frequency** | ✅ `suggest_freq()` | ✅ Weight parameter | ❌ No | ❌ No |
| **Dictionary Format** | `word freq tag` | Python dict | `word\n` | N/A |
| **Loading Method** | File or programmatic | Constructor param | Constructor param | Pre-processing |

**Best Custom Dictionary**: Jieba (most flexible API)
**Second Best**: CKIP (weighted recommendations)
**Limited**: PKUSeg (basic word list)
**Not Supported**: LTP (requires fine-tuning)

## Domain-Specific Models

| Domain | Jieba | CKIP | PKUSeg | LTP |
|--------|-------|------|--------|-----|
| **General** | ✅ Single model | ✅ Single model | ✅ mixed, default_v2 | ✅ Base/Small/Tiny |
| **News** | ⚠️ Via dictionary | ⚠️ Via dictionary | ✅ Pre-trained | ⚠️ Via dictionary |
| **Social Media (Weibo)** | ⚠️ Via dictionary | ⚠️ Via dictionary | ✅ Pre-trained | ⚠️ Via dictionary |
| **Medicine** | ⚠️ Via dictionary | ⚠️ Via dictionary | ✅ Pre-trained | ⚠️ Via fine-tuning |
| **Tourism** | ⚠️ Via dictionary | ⚠️ Via dictionary | ✅ Pre-trained | ⚠️ Via fine-tuning |
| **Legal** | ⚠️ Via dictionary | ⚠️ Via dictionary | ⚠️ Via custom training | ⚠️ Via fine-tuning |
| **Finance** | ⚠️ Via dictionary | ⚠️ Via dictionary | ⚠️ Via custom training | ⚠️ Via fine-tuning |

**Best Domain Support**: PKUSeg (6 pre-trained models)
**Second Best**: LTP (fine-tuning possible but requires expertise)
**Dictionary-Based**: Jieba, CKIP (add domain terms manually)

## Multi-Task Capabilities

| Task | Jieba | CKIP | PKUSeg | LTP |
|------|-------|------|--------|-----|
| **Word Segmentation (CWS)** | ✅ Primary | ✅ Primary | ✅ Primary | ✅ Primary |
| **Part-of-Speech (POS)** | ✅ `jieba.posseg` | ✅ Integrated | ✅ Optional | ✅ Integrated |
| **Named Entity Recognition (NER)** | ⚠️ Via TF-IDF | ✅ Integrated | ❌ No | ✅ Integrated |
| **Dependency Parsing** | ❌ No | ❌ No | ❌ No | ✅ Integrated |
| **Semantic Dependency Parsing** | ❌ No | ❌ No | ❌ No | ✅ Integrated |
| **Semantic Role Labeling (SRL)** | ❌ No | ❌ No | ❌ No | ✅ Integrated |
| **Keyword Extraction** | ✅ TF-IDF, TextRank | ❌ No | ❌ No | ❌ No |

**Most Comprehensive**: LTP (6 tasks)
**Second Best**: CKIP (3 tasks: WS, POS, NER)
**Third**: Jieba (2 tasks: WS, POS + keyword extraction)
**Single-Task**: PKUSeg (WS only, optional POS)

## Deployment Characteristics

### Installation Complexity

| Aspect | Jieba | CKIP | PKUSeg | LTP |
|--------|-------|------|--------|-----|
| **pip install** | ✅ `pip install jieba` | ✅ `pip install ckiptagger` | ✅ `pip install pkuseg` | ✅ `pip install ltp` |
| **Dependencies** | Minimal | TensorFlow/PyTorch | NumPy, Cython | PyTorch, Transformers |
| **Model Download** | ❌ Not required | ✅ 2 GB manual | ✅ Auto (70 MB) | ✅ Auto (100-500 MB) |
| **Cold Start Time** | ~200ms (lazy load) | ~10s (model load) | ~500ms (model load) | ~5-15s (model load) |
| **Complexity Rating** | ★☆☆☆☆ (Easiest) | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ |

**Easiest**: Jieba (instant setup)
**Moderate**: PKUSeg (auto-download, small models)
**Complex**: LTP (large models, deep learning deps)
**Most Complex**: CKIP (manual download, 2 GB models)

### Platform Compatibility

| Platform | Jieba | CKIP | PKUSeg | LTP |
|----------|-------|------|--------|-----|
| **Linux** | ✅ Full | ✅ Full | ✅ Full | ✅ Full |
| **macOS (Intel)** | ✅ Full | ✅ Full | ✅ Full | ✅ Full |
| **macOS (Apple Silicon)** | ✅ Full | ✅ Full (Rosetta) | ✅ Full | ✅ Full (MPS) |
| **Windows** | ⚠️ No parallel | ✅ Full | ✅ Full | ✅ Full |
| **Docker** | ✅ 120 MB image | ✅ 5 GB image (GPU) | ✅ 300 MB image | ✅ 3 GB image (GPU) |
| **ARM/Raspberry Pi** | ✅ Yes | ⚠️ CPU only | ✅ Yes | ⚠️ CPU only |

**Best Compatibility**: Jieba (smallest footprint, broadest support)
**GPU Required**: CKIP, LTP (for production speed)

### Python Version Support

| Version | Jieba | CKIP | PKUSeg | LTP |
|---------|-------|------|--------|-----|
| **Python 2.7** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Python 3.6** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Python 3.7-3.11** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **PyPy** | ✅ 2-3x faster | ❌ No | ⚠️ Limited | ❌ No |

**Best Legacy Support**: Jieba (Python 2.7 compatible)
**Modern Only**: CKIP, PKUSeg, LTP (Python 3.6+)

## Integration Patterns

### API Design

| Aspect | Jieba | CKIP | PKUSeg | LTP |
|--------|-------|------|--------|-----|
| **Initialization** | Lazy (first call) | Explicit (`WS("./data")`) | Explicit (`pkuseg()`) | Explicit (`LTP("model")`) |
| **Return Type** | Generator | List of lists | List | Dataclass (`.cws`, `.pos`, etc.) |
| **Batch Processing** | Manual | Built-in | File-based (`test()`) | Built-in (`pipeline()`) |
| **Streaming** | ✅ Generator-based | ⚠️ Manual batching | ⚠️ Manual batching | ⚠️ Manual batching |
| **Thread Safety** | ✅ Yes | ⚠️ Load model per thread | ⚠️ Load model per thread | ⚠️ Load model per thread |

**Most Pythonic**: Jieba (generator, lazy loading)
**Most Structured**: LTP (dataclass output)
**File-Based**: PKUSeg (optimized for batch files)

### Production Deployment

| Aspect | Jieba | CKIP | PKUSeg | LTP |
|--------|-------|------|--------|-----|
| **Docker Image Size** | 120 MB | 5 GB (GPU) | 300 MB | 3 GB (GPU) |
| **Cold Start (Serverless)** | ~200ms | 10-15s | ~500ms | 5-15s |
| **Throughput (CPU)** | 500-1000 req/s | 5-10 req/s | 10-20 req/s | 10-20 req/s |
| **Throughput (GPU)** | N/A | 50-100 req/s | N/A | 100-200 req/s |
| **Horizontal Scaling** | ✅ Excellent | ⚠️ GPU-bound | ✅ Good | ⚠️ GPU-bound |
| **Serverless Fit** | ★★★★★ | ★★☆☆☆ | ★★★★☆ | ★★★☆☆ |

**Best for Serverless**: Jieba (small, fast cold start)
**Best for GPU**: LTP (highest throughput)
**Best for CPU Scaling**: Jieba (horizontal scaling)

## Output Formats

| Format | Jieba | CKIP | PKUSeg | LTP |
|--------|-------|------|--------|-----|
| **List of Words** | ✅ `list()` or generator | ✅ List of lists | ✅ List | ✅ `.cws` attribute |
| **String (Joined)** | ✅ `" ".join()` | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual |
| **POS Tagged** | ✅ `[(word, pos)]` | ✅ List of POS lists | ✅ `[(word, pos)]` | ✅ `.pos` attribute |
| **NER Annotated** | ⚠️ Via TF-IDF | ✅ `(start, end, type, text)` | ❌ No | ✅ `(start, end, type, text)` |
| **Dependency Tree** | ❌ No | ❌ No | ❌ No | ✅ `(head, index, relation)` |

**Most Flexible**: Jieba (generator or list)
**Most Structured**: LTP (dataclass with attributes)
**Most Complete**: LTP (all NLP outputs)

## Custom Training Support

| Aspect | Jieba | CKIP | PKUSeg | LTP |
|--------|-------|------|--------|-----|
| **Custom Model Training** | ⚠️ Dictionary only | ⚠️ Requires source code | ✅ Built-in (`train()`) | ⚠️ Fine-tuning (advanced) |
| **Training Data Format** | N/A | BIO tags | BIO tags | BIO tags |
| **Training Time** | N/A | Days (GPU) | Hours (CPU) | Days (GPU) |
| **Ease of Training** | N/A | ★☆☆☆☆ | ★★★★☆ | ★★☆☆☆ |

**Best Trainability**: PKUSeg (built-in training API)
**Second Best**: LTP (fine-tuning possible)
**Not Supported**: Jieba (dictionary-based), CKIP (requires source modification)

## Licensing

| Aspect | Jieba | CKIP | PKUSeg | LTP |
|--------|-------|------|--------|-----|
| **License** | MIT | GNU GPL v3.0 | MIT | Apache 2.0 |
| **Commercial Use** | ✅ Free | ⚠️ Copyleft | ✅ Free | ⚠️ License required |
| **Derivative Works** | ✅ Permissive | ⚠️ Must be GPL | ✅ Permissive | ⚠️ Must contact HIT |
| **Attribution** | ❌ Not required | ⚠️ Required | ❌ Not required | ✅ Required |
| **SaaS Use** | ✅ Free | ⚠️ GPL applies | ✅ Free | ⚠️ License required |

**Best for Commercial**: Jieba, PKUSeg (MIT - fully permissive)
**Restrictive**: CKIP (GNU GPL v3.0 copyleft)
**Commercial License**: LTP (requires agreement with HIT)

## Maintenance & Community

| Aspect | Jieba | CKIP | PKUSeg | LTP |
|--------|-------|------|--------|-----|
| **GitHub Stars** | 34.7k | 1.7k | 6.7k | 5.2k |
| **Last Updated** | Active | 2025-07 | Active | 2022-08 |
| **Institutional Backing** | Community | Academia Sinica | Peking University | Harbin Institute of Technology |
| **Commercial Backing** | ❌ No | ❌ No | ❌ No | ✅ Baidu, Tencent |
| **Documentation Quality** | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★☆ |
| **Community Size** | ★★★★★ (Largest) | ★★☆☆☆ | ★★★☆☆ | ★★★☆☆ |

**Most Popular**: Jieba (34.7k stars)
**Best Institutional Backing**: LTP (HIT + industry partners)
**Best Academic Backing**: CKIP (Academia Sinica), PKUSeg (Peking University)

## Use Case Fit Matrix

| Use Case | Best Choice | Second Best | Third |
|----------|------------|-------------|-------|
| **Real-time Web API** | Jieba | LTP Tiny | PKUSeg |
| **Traditional Chinese** | CKIP | LTP | Jieba |
| **Medical Domain** | PKUSeg | LTP (fine-tuned) | Jieba + dict |
| **Social Media (Weibo)** | PKUSeg | Jieba | LTP |
| **News Articles** | PKUSeg | LTP | Jieba |
| **Offline Batch** | LTP Legacy | PKUSeg | Jieba |
| **Research/Academic** | CKIP | LTP | PKUSeg |
| **Multi-Task NLP** | LTP | CKIP | Jieba |
| **Rapid Prototyping** | Jieba | PKUSeg | LTP Tiny |
| **High-Throughput** | LTP Legacy | Jieba | PKUSeg |
| **Low-Resource (Mobile)** | Jieba | PKUSeg | LTP Tiny |
| **GPU-Accelerated** | LTP | CKIP | N/A |
| **Commercial Product** | Jieba/PKUSeg | LTP (licensed) | CKIP (GPL) |

## Decision Matrix

### Choose Jieba If:
- ✅ Speed is critical (real-time, high-throughput)
- ✅ Minimal setup required (rapid prototyping)
- ✅ Custom dictionaries needed (extensive API)
- ✅ Low-resource environment (mobile, edge)
- ✅ Commercial product (MIT license)
- ❌ Accuracy is paramount

### Choose CKIP If:
- ✅ Traditional Chinese text (Taiwan, Hong Kong)
- ✅ Highest accuracy required
- ✅ Multi-task pipeline (WS + POS + NER)
- ✅ Academic/research application
- ✅ GPU available
- ❌ Commercial proprietary software (GPL restriction)
- ❌ Speed critical on CPU

### Choose PKUSeg If:
- ✅ Domain-specific application (medical, social, tourism)
- ✅ Highest accuracy for Simplified Chinese
- ✅ Custom model training needed
- ✅ Offline batch processing
- ✅ Commercial product (MIT license)
- ❌ Real-time/low-latency required
- ❌ Traditional Chinese focus

### Choose LTP If:
- ✅ Comprehensive NLP pipeline needed (6 tasks)
- ✅ Semantic analysis required (SRL, dependency parsing)
- ✅ Flexible speed/accuracy tradeoff (multiple model sizes)
- ✅ Enterprise support needed (institutional backing)
- ✅ GPU available
- ❌ Budget for commercial licensing
- ❌ Single-task segmentation only

## Summary Scorecard

| Criterion | Jieba | CKIP | PKUSeg | LTP |
|-----------|-------|------|--------|-----|
| **Speed** | ★★★★★ | ★★☆☆☆ | ★☆☆☆☆ | ★★★☆☆ / ★★★★★ (Legacy) |
| **Accuracy** | ★★★☆☆ | ★★★★★ | ★★★★★ | ★★★★★ |
| **Memory Efficiency** | ★★★★★ | ★☆☆☆☆ | ★★★★☆ | ★★★☆☆ |
| **Ease of Use** | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ |
| **Custom Dictionary** | ★★★★★ | ★★★★☆ | ★★★☆☆ | ★☆☆☆☆ |
| **Domain Support** | ★★☆☆☆ | ★★☆☆☆ | ★★★★★ | ★★★☆☆ |
| **Multi-Task** | ★★☆☆☆ | ★★★★☆ | ★☆☆☆☆ | ★★★★★ |
| **Deployment** | ★★★★★ | ★★☆☆☆ | ★★★★☆ | ★★★☆☆ |
| **Commercial License** | ★★★★★ | ★★☆☆☆ | ★★★★★ | ★★☆☆☆ |
| **Community** | ★★★★★ | ★★☆☆☆ | ★★★☆☆ | ★★★☆☆ |
| **Overall** | **4.0/5** | **3.0/5** | **3.7/5** | **3.6/5** |

**Note**: Overall scores reflect general-purpose use. Domain-specific use cases shift rankings.

## Cross-References

- **S1 Rapid Discovery**: [recommendation.md](../S1-rapid/recommendation.md) - Quick comparison
- **S2 Individual Deep Dives**: [jieba.md](jieba.md), [ckip.md](ckip.md), [pkuseg.md](pkuseg.md), [ltp.md](ltp.md)
- **S3 Need-Driven**: Use case recommendations (to be created)
- **S4 Strategic**: Long-term viability analysis (to be created)
