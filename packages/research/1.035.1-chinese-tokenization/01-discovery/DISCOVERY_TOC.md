# Chinese Tokenization: Discovery Documentation

## Overview

Comprehensive research on Chinese tokenization strategies, organized using the 4PS (Four-Pass Survey) methodology. Each pass reveals different aspects of the solution space, from rapid ecosystem scan to long-term strategic viability.

## Four-Pass Structure

### S1: Rapid Discovery (WHAT tools exist?)
**Reading time**: ~10 minutes
**Focus**: Speed-optimized library ecosystem scan

### S2: Comprehensive Discovery (HOW do they work?)
**Reading time**: ~30-45 minutes
**Focus**: Deep technical analysis, algorithms, trade-offs

### S3: Need-Driven Discovery (WHO needs + WHY?)
**Reading time**: ~20 minutes
**Focus**: Use cases, personas, scenario-based matching

### S4: Strategic Discovery (WHICH for long-term?)
**Reading time**: ~25 minutes
**Focus**: Ecosystem trends, maintenance, future-proofing

---

## S1: Rapid Discovery

### [Approach](S1-rapid/approach.md)
S1 methodology: What we scan and why

### Libraries
- [Jieba](S1-rapid/jieba.md) - Most popular Python segmenter (34.7K stars)
- [PKUSEG](S1-rapid/pkuseg.md) - Highest accuracy neural segmenter (F1 ~96%)
- [LAC](S1-rapid/lac.md) - Baidu's production segmenter (800 QPS)
- [SentencePiece](S1-rapid/sentencepiece.md) - Google's subword tokenizer
- [transformers](S1-rapid/transformers.md) - HuggingFace ecosystem (BERT, Qwen)

### [Recommendation](S1-rapid/recommendation.md)
**Quick selection guide**: Jieba for prototyping, LAC for production, SentencePiece for multilingual

**Key takeaway**: Pick based on primary constraint: speed (Jieba), accuracy (PKUSEG), balance (LAC), or multilingual (SentencePiece).

---

## S2: Comprehensive Discovery

### [Approach](S2-comprehensive/approach.md)
S2 methodology: Deep technical analysis

### Technical Deep-Dives
- [Jieba](S2-comprehensive/jieba.md) - Algorithm: Dictionary + HMM, 400 KB/s, O(n²) DAG + O(n) DP
- [PKUSEG](S2-comprehensive/pkuseg.md) - Architecture: BiLSTM-CRF, domain models, neural training

### [Feature Comparison](S2-comprehensive/feature-comparison.md)
**Comprehensive matrix**: Algorithms, performance, features, accuracy by text type

**Key insights**:
- Speed vs accuracy: Jieba (400 KB/s, F1 85%) vs PKUSEG (130 KB/s, F1 96%)
- Context matters: Local (Jieba) vs sentence-level (PKUSEG/LAC) vs full document (transformers)
- OOV handling: Dictionary+HMM (Jieba) < Neural embeddings (PKUSEG/LAC) < Subword (SentencePiece)

### [Recommendation](S2-comprehensive/recommendation.md)
**Algorithm-driven selection**: Match to technical constraints (memory, GPU, training capacity)

**Key takeaway**: No universal winner - each algorithm optimizes for different bottlenecks. Pick based on your limiting constraint.

---

## S3: Need-Driven Discovery

### [Approach](S3-need-driven/approach.md)
S3 methodology: Start with needs, not tools

### Use Cases

#### [E-commerce Product Search](S3-need-driven/use-case-ecommerce-search.md)
**Who**: Backend engineer building product search
**Need**: High recall, fast indexing, custom brands
**Solution**: Jieba (search mode) + custom dictionary
**Why**: Fine-grained segmentation for recall, 1.5 MB/s speed

#### [Academic NLP Research](S3-need-driven/use-case-nlp-research.md)
**Who**: PhD student / NLP researcher
**Need**: Maximum accuracy, reproducibility, citations
**Solution**: PKUSEG (domain model) or bert-base-chinese
**Why**: Highest accuracy (F1 ~96%), academic credibility

#### [Real-Time Chatbot](S3-need-driven/use-case-chatbot-development.md)
**Who**: Developer building customer service bot
**Need**: <50ms latency, handles informal text, robust at scale
**Solution**: LAC (joint seg + NER mode)
**Why**: Fast (800 QPS), extracts entities for intent recognition

#### [Multilingual SaaS Product](S3-need-driven/use-case-multilingual-product.md)
**Who**: Product engineer at SaaS expanding to China
**Need**: Unified tokenizer, no language detection, token efficiency
**Solution**: SentencePiece or Qwen/mT5 tokenizer
**Why**: Language-agnostic, efficient for CJK, single codebase

### [Recommendation](S3-need-driven/recommendation.md)
**Scenario-based lookup table**: Map your use case to recommended library

**Key takeaway**: Match library to YOUR constraints, not theoretical "best". Context matters more than benchmarks.

---

## S4: Strategic Discovery

### [Approach](S4-strategic/approach.md)
S4 methodology: Beyond technical specs to long-term viability

### Strategic Analysis

#### [Jieba Viability](S4-strategic/jieba-viability.md)
**Status**: ⚠️ Maintenance mode, single maintainer
**Trajectory**: DECLINING (rule-based losing to neural)
**Horizon**: Safe 2-3 years, risky 5+ years
**Use if**: Traditional NLP, stable product, cost-sensitive
**Avoid if**: Building transformers, research, long-term ML investment

#### [SentencePiece Viability](S4-strategic/sentencepiece-viability.md)
**Status**: ✅ Active, Google-backed
**Trajectory**: RISING (standard for multilingual LLMs)
**Horizon**: Safe 5+ years
**Use if**: Building transformers, multilingual, ML-first team
**Avoid if**: Simple NLP, small team, no ML expertise

### [Recommendation](S4-strategic/recommendation.md)
**Strategic paths**: Transformer-native, pragmatic hybrid, or simple & stable

**Key insights**:
- **Industry trajectory**: Character-level winning (Chinese-only), subword standard (multilingual)
- **Hidden costs**: Migration debt, team expertise mismatch, vendor lock-in
- **Organizational fit** > technical superiority

**Bottom line**: Choose based on your organization's trajectory and team capabilities, not today's benchmark results.

---

## Key Findings Summary

### Core Problem
Chinese lacks spaces between words → Tokenization is necessary but inherently ambiguous → Affects all downstream NLP tasks (7-8 BLEU points in MT, 10-15% in NER accuracy).

### Three Viable Approaches (2025)
1. **Traditional segmenters** (Jieba, PKUSEG, LAC) - Word-level, dictionary/neural
2. **Subword tokenization** (SentencePiece) - Data-driven boundaries, multilingual
3. **Character-level** (BERT) - Transformers learn composition from data

### Library Landscape

| Library | Best For | Speed | Accuracy | Viability |
|---------|----------|-------|----------|-----------|
| Jieba | Prototyping, search | 400 KB/s | F1 ~85% | 2-3 years |
| PKUSEG | Domain accuracy | 130 KB/s | F1 ~96% | 3-5 years |
| LAC | Production balance | 800 QPS | F1 ~91% | 3-5 years |
| SentencePiece | Multilingual, LLMs | Very fast | Task-dep | 5+ years ✅ |
| transformers | State-of-art | Slow | F1 ~97% | 5+ years ✅ |

### Critical Technical Decisions
- **character_coverage**: Must be 0.9995 for SentencePiece on Chinese
- **Byte-level BPE**: Avoid for Chinese-heavy (2-3x token inflation)
- **Domain models**: PKUSEG offers news/web/medicine/tourism pre-trained
- **GPU**: Required for BERT, optional (6x faster) for PKUSEG

### Strategic Recommendations

**Default (2025)**:
- **Transformer teams**: bert-base-chinese (Chinese-only) or SentencePiece (multilingual)
- **Production teams**: LAC (balanced) or Jieba (pragmatic)
- **Small teams**: Jieba (simple)
- **Research teams**: PKUSEG or BERT (reproducible)

**Future-proof bet**: SentencePiece for ML-driven orgs, character-level BERT for Chinese-only transformers.

---

## Related Research

- **1.033.2 - Chinese Word Segmentation**: Traditional segmentation approaches
- **1.033.3 - CJK Tokenizers**: Cross-language considerations (Chinese, Japanese, Korean)
- **1.153.1 - Chinese Dependency Parsing**: Downstream impact of tokenization choices

---

## Document Status

- ✅ S1 Rapid Discovery: Complete
- ✅ S2 Comprehensive Discovery: Complete
- ✅ S3 Need-Driven Discovery: Complete
- ✅ S4 Strategic Discovery: Complete

**Last Updated**: January 2025
**Coverage**: Libraries, algorithms, use cases, strategic viability
**Audience**: NLP engineers, data scientists, product managers, researchers
