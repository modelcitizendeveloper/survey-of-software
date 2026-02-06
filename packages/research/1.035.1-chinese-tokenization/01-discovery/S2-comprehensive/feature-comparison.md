# Feature Comparison Matrix

## Algorithmic Approaches

| Library | Algorithm | Training | Context Window |
|---------|-----------|----------|----------------|
| Jieba | Dict + HMM | Pre-trained HMM | Local (bigrams) |
| PKUSEG | BiLSTM-CRF | Neural on corpus | Sentence-level |
| LAC | BiGRU-CRF | Neural on corpus | Sentence-level |
| SentencePiece | Unigram LM | Train on corpus | Subword-level |
| transformers | Model-dependent | Pre-trained LLMs | Full context |

## Performance Metrics

| Library | Speed | Accuracy | Memory | GPU Support |
|---------|-------|----------|--------|-------------|
| Jieba | 400 KB/s | F1 ~85% | 100 MB | ❌ |
| PKUSEG (CPU) | 130 KB/s | F1 ~96% | 300 MB | ✅ (6x faster) |
| LAC | 800 QPS | F1 ~91% | 250 MB | ✅ |
| SentencePiece | Very fast | Task-dependent | 50 MB | ❌ |
| transformers (BERT) | ~20 KB/s | F1 ~97% | 1-2 GB | ✅ (required) |

## Feature Support Matrix

| Feature | Jieba | PKUSEG | LAC | SentencePiece | transformers |
|---------|-------|--------|-----|---------------|--------------|
| **Core Segmentation** |
| Character-level | ❌ | ❌ | ❌ | ✅ | ✅ |
| Word-level | ✅ | ✅ | ✅ | ❌ | ❌ |
| Subword | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Advanced Features** |
| Custom dictionary | ✅ | ✅ | ❌ | N/A | N/A |
| POS tagging | ✅ | ✅ (optional) | ✅ | ❌ | ✅ (via model) |
| NER | ❌ | ❌ | ✅ | ❌ | ✅ (via model) |
| Keyword extraction | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Modes** |
| Precise mode | ✅ | ✅ | ✅ | N/A | N/A |
| Full mode | ✅ | ❌ | ❌ | N/A | N/A |
| Search mode | ✅ | ❌ | ❌ | N/A | N/A |
| **Domain Adaptation** |
| Pre-trained domains | 1 (general) | 5 (news, web, etc.) | 1 (general) | Custom training | Many models |
| Custom training | ❌ | ✅ | ❌ | ✅ | ✅ |
| Fine-tuning | ❌ | ✅ | ❌ | ✅ | ✅ |
| **Integration** |
| Python API | ✅ | ✅ | ✅ | ✅ | ✅ |
| C++ API | ❌ | ❌ | ❌ | ✅ | ❌ |
| REST API | ❌ | ❌ | ❌ | ❌ | ✅ (via inference) |
| **Multilingual** |
| Chinese only | ✅ | ✅ | ✅ | ❌ | ❌ |
| CJK support | ✅ | ✅ | ❌ | ✅ | ✅ |
| Multilingual | ❌ | ❌ | ❌ | ✅ | ✅ |

## Accuracy by Text Type

| Text Type | Jieba | PKUSEG | LAC | Note |
|-----------|-------|--------|-----|------|
| News | ~89% | ~96% | ~95% | Formal writing |
| Social media | ~85% | ~93% | ~94% | Informal, slang |
| Medical | ~81% | ~96% | ~93% | PKUSEG has domain model |
| Legal | ~83% | ~94% | ~92% | Technical terms |
| Chat/IM | ~80% | ~90% | ~91% | Very informal |

## Technical Constraints

| Constraint | Jieba | PKUSEG | LAC | SentencePiece | transformers |
|------------|-------|--------|-----|---------------|--------------|
| **Minimum corpus size** | N/A | 10M chars | N/A | 1M sentences | 100M tokens |
| **Max sequence length** | Unlimited | ~500 chars | ~512 chars | Unlimited | 512-4096 tokens |
| **Batch processing** | Linux only | ✅ | ✅ | ✅ | ✅ |
| **Streaming** | ✅ | ❌ | ❌ | ✅ | ❌ |

## Ecosystem Maturity

| Aspect | Jieba | PKUSEG | LAC | SentencePiece | transformers |
|--------|-------|--------|-----|---------------|--------------|
| GitHub stars | 34.7K | 6.3K | 2.8K | 10.4K | 135K |
| Last update | 2024 | 2023 | 2024 | 2025 | 2025 |
| Documentation | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Community | Very active | Moderate | Small | Active | Very active |

## OOV Handling

| Library | Mechanism | Effectiveness |
|---------|-----------|---------------|
| Jieba | HMM (BMES tags) | Moderate (struggles with compounds) |
| PKUSEG | Neural embeddings | Good (learns from context) |
| LAC | Neural embeddings | Good (learns from context) |
| SentencePiece | Subword fallback | Excellent (always decomposes) |
| transformers | Subword/character | Excellent (no true OOV) |

## Configuration Complexity

| Library | Setup Time | Configuration Options | Learning Curve |
|---------|------------|---------------------|----------------|
| Jieba | 2 minutes | Low (mostly defaults) | Easy |
| PKUSEG | 5 minutes | Medium (model selection) | Medium |
| LAC | 5 minutes | Low (mode selection) | Easy |
| SentencePiece | 30 minutes | High (many parameters) | Hard |
| transformers | 10 minutes | High (model selection) | Hard |

## Decision Matrix

### Choose Jieba if:
- ✅ Prototyping / exploratory analysis
- ✅ High-volume processing (speed matters)
- ✅ Easy custom dictionary
- ❌ NOT if accuracy is critical

### Choose PKUSEG if:
- ✅ Domain-specific accuracy needed
- ✅ Have GPU for faster inference
- ✅ Can select appropriate domain model
- ❌ NOT for real-time applications

### Choose LAC if:
- ✅ Production speed + accuracy balance
- ✅ Need seg + POS + NER together
- ✅ Chinese-only application
- ❌ NOT for multilingual projects

### Choose SentencePiece if:
- ✅ Multilingual tokenization
- ✅ Building transformers from scratch
- ✅ Have corpus to train on
- ❌ NOT for quick prototyping

### Choose transformers if:
- ✅ Using pre-trained LLMs
- ✅ Maximum accuracy required
- ✅ Have GPU resources
- ❌ NOT for real-time or large-scale batch
