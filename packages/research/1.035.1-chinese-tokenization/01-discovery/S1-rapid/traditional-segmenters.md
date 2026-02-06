# Traditional Word Segmenters

Dictionary-based and neural segmenters that output word-level tokens.

## Jieba (结巴中文分词)

- **Maturity**: 34.7K GitHub stars, most popular Python tool, 10+ years active
- **Speed**: 400 KB/s (precise mode), 1.5 MB/s (full mode) - fastest in category
- **Accuracy**: F1 ~85% (SIGHAN 2005 benchmark) - lower than academic tools
- **Approach**: Dictionary + HMM for unknown words
- **Ease**: Minimal setup, works out-of-box, easy custom dictionaries
- **Maintenance**: Single maintainer (fxsjy), maintenance mode since 2020
- **Best for**: Prototyping, web scraping, keyword extraction, high-throughput batch processing

**Trade-off**: Speed and simplicity at cost of accuracy.

---

## PKUSEG (北大分词)

- **Maturity**: 6.3K GitHub stars, academic tool from Peking University
- **Speed**: ~130 KB/s (3x slower than Jieba)
- **Accuracy**: F1 ~96% (PKU corpus) - highest among traditional tools
- **Approach**: BiLSTM-CRF neural model
- **Ease**: Domain model selection required (news, web, medicine, tourism, mixed)
- **Maintenance**: Active academic project, last update 2023
- **Best for**: Domain-specific accuracy (medical, legal, news), research benchmarks

**Trade-off**: Best accuracy but slower, requires domain model choice.

---

## LAC (Baidu Lexical Analysis)

- **Maturity**: 2.8K stars, production tool from Baidu
- **Speed**: 800 QPS (queries per second) - optimized for production
- **Accuracy**: F1 ~91% (segmentation), ~94% (POS tagging)
- **Approach**: BiGRU-CRF, joint seg+POS+NER model
- **Ease**: Moderate, mode selection (seg-only vs full pipeline)
- **Maintenance**: Actively maintained by Baidu, 2024 updates
- **Best for**: Production Chinese-only systems, when you need seg+POS+NER together

**Trade-off**: Balanced speed + accuracy, but Chinese-only focus.

---

## LTP (Language Technology Platform)

- **Maturity**: 4.4K stars, academic/research tool
- **Speed**: ~100 KB/s (similar to PKUSEG)
- **Accuracy**: F1 ~94% (mixed domains)
- **Approach**: Neural pipeline (seg → POS → parsing → NER)
- **Ease**: Complex, full NLP pipeline
- **Maintenance**: Harbin Institute of Technology, periodic updates
- **Best for**: Research requiring full Chinese NLP pipeline

**Trade-off**: Comprehensive but heavyweight, slower than alternatives.

---

## Quick Comparison

| Library | Speed | Accuracy | Complexity | Maintenance |
|---------|-------|----------|------------|-------------|
| **Jieba** | ⭐⭐⭐⭐⭐ (400 KB/s) | ⭐⭐⭐ (F1 ~85%) | ⭐⭐⭐⭐⭐ Simple | ⚠️ Single maintainer |
| **PKUSEG** | ⭐⭐⭐ (130 KB/s) | ⭐⭐⭐⭐⭐ (F1 ~96%) | ⭐⭐⭐⭐ Medium | ✅ Academic active |
| **LAC** | ⭐⭐⭐⭐⭐ (800 QPS) | ⭐⭐⭐⭐ (F1 ~91%) | ⭐⭐⭐⭐ Medium | ✅ Corporate (Baidu) |
| **LTP** | ⭐⭐⭐ (100 KB/s) | ⭐⭐⭐⭐ (F1 ~94%) | ⭐⭐⭐ Complex | ✅ Academic active |

## Selection Heuristics

**Need speed?** → Jieba (400 KB/s) or LAC (800 QPS)

**Need accuracy?** → PKUSEG (F1 ~96%)

**Need production stability?** → LAC (Baidu-backed)

**Need full NLP pipeline?** → LTP (seg+POS+parsing+NER)

**Prototyping?** → Jieba (fastest to start)
