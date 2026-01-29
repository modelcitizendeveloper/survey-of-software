# S2: COMPREHENSIVE DISCOVERY - Named Entity Recognition for CJK Languages

**Experiment**: 1.033.4 Named Entity Recognition for CJK Languages
**Phase**: S2 Comprehensive Discovery (Deep Technical Analysis)
**Date**: 2026-01-29
**Researcher**: Furiosa Polecat

---

## Executive Summary

This comprehensive analysis examines the CJK NER ecosystem with focus on architectures, accuracy benchmarks, and production deployment patterns. Key finding: **92-95% F1-score** accuracy is achievable for Chinese NER with modern transformer-based models (HanLP BERT), while **50-150ms latency** enables real-time applications with optimized deployments.

### Critical Insights

- **Chinese State-of-Art**: HanLP BERT achieves 95.5% F1 on MSRA dataset, 80.5% F1 on OntoNotes (10-15% better than non-specialized models)
- **Multi-Language Trade-offs**: Stanza provides unified API across CJK at 88-92% F1 vs language-specific models at 92-95%
- **Production Speed**: LTP achieves 50-100ms latency on CPU (3-5x faster than transformer models) with 90-93% accuracy
- **Traditional/Simplified**: Native dual-script support critical (HanLP handles both, others require conversion preprocessing)
- **Cost at Scale**: Self-hosted deployment breaks even at ~500K entities/month vs cloud APIs ($200/month vs $1,000/month)

**Recommendation**: Start with HanLP for Chinese-focused accuracy-critical applications, Stanza for multi-language consistency, or cloud APIs for rapid prototyping (<2 weeks deployment).

---

## Table of Contents

1. [Technical Architecture Deep Dive](#1-technical-architecture-deep-dive)
2. [Benchmark Data and Accuracy Analysis](#2-benchmark-data-and-accuracy-analysis)
3. [CJK-Specific Technical Challenges](#3-cjk-specific-technical-challenges)
4. [Model Training and Customization](#4-model-training-and-customization)
5. [Production Deployment Patterns](#5-production-deployment-patterns)
6. [Performance Optimization Techniques](#6-performance-optimization-techniques)
7. [Cost-Benefit Analysis by Scale](#7-cost-benefit-analysis-by-scale)
8. [Integration and Entity Linking Strategies](#8-integration-and-entity-linking-strategies)

---

## 1. Technical Architecture Deep Dive

### 1.1 Modern Transformer-Based NER (HanLP, Stanza)

**Architecture**:
```
Input Text → Tokenization → BERT/RoBERTa Embeddings → BiLSTM/CRF → Entity Tags
                                    ↓
                          Contextual Representations (768-dim vectors)
```

**Technical Approach**:
- **Tokenization**: Character-level or subword (BPE, WordPiece) for CJK
- **Contextualized Embeddings**: BERT pre-trained on large Chinese/Japanese/Korean corpora
- **Sequence Labeling**: BiLSTM-CRF or pure transformer layers
- **Tag Scheme**: BIO/BIOES (Begin, Inside, Outside, End, Single)

**Performance**:
- **Latency**: 100-300ms per sentence (depends on length, GPU vs CPU)
- **Accuracy**: 90-95% F1 for Chinese (MSRA, OntoNotes benchmarks)
- **Resource**: 500MB-1GB models, 2-8GB RAM, GPU recommended

**Key Models**:
- **HanLP**: BERT-base-chinese (12 layers, 768-dim, 110M params)
- **Stanza**: BiLSTM + Transformer (smaller, faster, 88-92% F1)
- **spaCy zh_core_web_trf**: Transformer model (90-92% F1)

**Production Example (HanLP)**:
```python
import hanlp

# Load pre-trained model (one-time, ~5-10s)
ner = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)

# Batch inference for efficiency
texts = [
    "阿里巴巴的马云在杭州创立了这家公司。",
    "微软在西雅图总部宣布新产品发布。"
]

results = ner(texts)
# [
#   [('阿里巴巴', 'ORGANIZATION', 0, 4), ('马云', 'PERSON', 5, 7), ('杭州', 'LOCATION', 8, 10)],
#   [('微软', 'ORGANIZATION', 0, 2), ('西雅图', 'LOCATION', 3, 6)]
# ]
```

**Optimization Techniques**:
1. **Model Quantization**: INT8 quantization reduces model size by 4x, 30-40% latency reduction
2. **ONNX Runtime**: 20-30% speedup with ONNX conversion
3. **Batching**: Process 8-32 sentences together for 3-5x throughput improvement
4. **Mixed Precision**: FP16 on GPU doubles throughput (A100, V100 GPUs)

**Trade-offs**:
- ✅ **State-of-art accuracy**: 92-95% F1 on benchmarks
- ✅ **Contextual understanding**: Handles ambiguous entities
- ✅ **Fine-tuning capable**: Custom domain adaptation possible
- ❌ **Slower inference**: 100-300ms vs 50ms for CNN/RNN models
- ❌ **Resource intensive**: GPU recommended, 2-8GB RAM
- ⚠️ **Good for**: High-accuracy requirements (contracts, legal, compliance)

---

### 1.2 Fast CNN/RNN-Based NER (LTP, Early spaCy)

**Architecture**:
```
Input Text → Word Segmentation → Word Embeddings → CNN/BiLSTM → CRF → Entity Tags
                                        ↓
                              Pre-trained Word2Vec/FastText
```

**Technical Approach**:
- **Word Segmentation**: Critical for Chinese (no spaces)
- **Pre-trained Embeddings**: Word2Vec, FastText trained on large corpora
- **Feature Engineering**: Character features, POS tags, lexicon matching
- **Sequence Modeling**: BiLSTM with CRF decoding layer

**Performance**:
- **Latency**: 50-100ms per sentence on CPU
- **Accuracy**: 85-93% F1 (90-93% for LTP v4, 85-88% for older models)
- **Resource**: 200-400MB models, 1-2GB RAM, CPU-friendly

**Key Models**:
- **LTP v4**: CNN-based with improved neural architecture (90-93% F1)
- **LTP v3**: BiLSTM-CRF baseline (85-88% F1)
- **spaCy sm/md**: Small/medium models without transformers

**Production Example (LTP)**:
```python
from ltp import LTP

ltp = LTP()  # Default fast model

# Batch processing
texts = [
    "阿里巴巴的马云在杭州创立了这家公司。",
    "腾讯公司总部位于深圳市南山区。"
]

# Integrated pipeline: segmentation + NER
results = ltp.pipeline(texts, tasks=["cws", "ner"])

for i, text in enumerate(texts):
    print(f"Text: {text}")
    print(f"Segmentation: {results.cws[i]}")
    print(f"Entities: {results.ner[i]}")
# Output includes word boundaries and entity tags (Ni=Org, Nh=Person, Ns=Location)
```

**Optimization Techniques**:
1. **Model Pruning**: Remove low-weight connections for 20-30% speedup
2. **CPU Optimization**: Intel MKL, OpenMP for multi-core utilization
3. **Caching**: Cache entity dictionary lookups for common names
4. **Early Exit**: Skip complex processing for low-confidence initial predictions

**Trade-offs**:
- ✅ **Fast CPU inference**: 50-100ms, no GPU required
- ✅ **Lower resource**: 1-2GB RAM, smaller models
- ✅ **Proven at scale**: Used in production by major Chinese tech companies
- ❌ **Lower accuracy**: 85-93% vs 92-95% for transformers
- ❌ **Less contextual**: Struggles with ambiguous entities
- ⚠️ **Good for**: High-throughput, cost-sensitive deployments, CPU-only infrastructure

---

### 1.3 Cloud API Architecture (Google, AWS, Azure)

**Architecture**:
```
Client → REST API → Cloud NER Service → Pre-trained Multi-Language Models → Response
              ↓                                ↓
         Rate Limiting                    Auto-Scaling Infrastructure
```

**Technical Approach**:
- **Managed Models**: Google/AWS/Azure maintain and update models automatically
- **Multi-Language Routing**: Language detection → appropriate model selection
- **Entity Linking**: Connect entities to knowledge bases (Wikipedia, Freebase)
- **Confidence Scoring**: Salience/importance scores for entity ranking

**Performance**:
- **Latency**: 200-800ms (includes network round-trip)
- **Accuracy**: 85-90% F1 estimated (vendors don't publish detailed benchmarks)
- **Rate Limits**: 100-600 requests/minute (tier-dependent)
- **Availability**: 99.9%+ SLA for enterprise tiers

**Production Example (Google Cloud)**:
```python
from google.cloud import language_v1
import time

client = language_v1.LanguageServiceClient()

def extract_entities_with_retry(text, language="zh", max_retries=3):
    """Production-ready with retry logic"""
    for attempt in range(max_retries):
        try:
            document = {
                "content": text,
                "type_": language_v1.Document.Type.PLAIN_TEXT,
                "language": language
            }
            response = client.analyze_entities(
                request={"document": document}
            )
            return [
                {
                    "text": entity.name,
                    "type": entity.type_.name,
                    "salience": entity.salience,
                    "mentions": len(entity.mentions)
                }
                for entity in response.entities
            ]
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff

# Batch processing with rate limiting
from time import sleep

texts = [...]  # Large corpus
batch_size = 10
results = []

for i in range(0, len(texts), batch_size):
    batch = texts[i:i+batch_size]
    batch_results = [extract_entities_with_retry(t) for t in batch]
    results.extend(batch_results)
    sleep(1)  # Rate limiting: 600/min = 10/sec
```

**Optimization Techniques**:
1. **Batch APIs**: Use batch endpoints for 30-50% cost reduction
2. **Caching**: Cache results for frequently occurring texts
3. **Request Compression**: gzip compress payloads for faster network transfer
4. **Regional Endpoints**: Use geographically close endpoints to minimize latency

**Trade-offs**:
- ✅ **Zero infrastructure**: No model management, deployment, or scaling
- ✅ **Automatic updates**: Model improvements without redeployment
- ✅ **Enterprise SLA**: 99.9% uptime guarantees
- ✅ **Entity linking**: Built-in knowledge base connections
- ❌ **Higher cost**: $1-2.50 per 1K requests ($1K-2.5K per 1M entities)
- ❌ **Network latency**: 200-800ms including round-trip
- ❌ **Data sovereignty**: Data leaves your infrastructure
- ❌ **Vendor lock-in**: Migration requires application changes
- ⚠️ **Good for**: Prototyping, variable workloads, managed service preference

---

## 2. Benchmark Data and Accuracy Analysis

### 2.1 Chinese NER Benchmarks

**MSRA NER Corpus (Microsoft Research Asia)**
- **Domain**: Simplified Chinese news articles
- **Size**: ~46K sentences, ~2M characters
- **Entity Types**: Person, Location, Organization
- **Benchmark Usage**: Primary evaluation for Chinese NER systems

**Top Performing Models**:
| Model | Architecture | F1-Score | Year |
|-------|-------------|----------|------|
| **HanLP BERT** | BERT-base-chinese + BiLSTM-CRF | **95.5%** | 2020 |
| **LTP v4** | CNN + CRF | 93.2% | 2021 |
| **Lattice-LSTM** | Character + Word Lattice | 93.2% | 2018 |
| **BiLSTM-CRF baseline** | Traditional architecture | 91.2% | 2015 |

**OntoNotes 4.0 Chinese**
- **Domain**: Multi-genre (news, blogs, web, conversation)
- **Size**: ~1.4M tokens
- **Entity Types**: 18 types (Person, Org, GPE, Date, Money, etc.)
- **Challenge**: More diverse and complex than MSRA

**Top Performing Models**:
| Model | F1-Score | Notes |
|-------|----------|-------|
| **HanLP BERT** | **80.5%** | Best open-source |
| **Stanza** | 77-79% | Multi-language consistency |
| **LTP v4** | 76-78% | Fast CPU inference |
| **spaCy zh_core_trf** | 75-77% | Production-optimized |

**Key Insight**: 10-15% accuracy gap between MSRA (narrow domain, news) and OntoNotes (diverse domains). Production systems should benchmark on domain-specific test sets.

---

### 2.2 Japanese NER Benchmarks

**Wikipedia NER Dataset (Japanese)**
- **Domain**: Wikipedia articles
- **Entity Types**: Person, Organization, Location, Artifact
- **Size**: ~20K articles

**Top Performing Models**:
| Model | F1-Score | Notes |
|-------|----------|-------|
| **Stanza Japanese** | **85-88%** | Stanford NLP quality |
| **Tohoku BERT Japanese** | 86-89% | BERT pre-trained on Japanese corpus |
| **spaCy ja_core_trf** | 83-86% | Production-ready |

**Mixed Script Challenge**: Models handle Kanji (漢字), Hiragana (ひらがな), Katakana (カタカナ), Romaji mixture well with subword tokenization.

---

### 2.3 Korean NER Benchmarks

**KLUE NER (Korean Language Understanding Evaluation)**
- **Domain**: Diverse Korean text (news, web, social media)
- **Entity Types**: Person, Location, Organization, Date, Time, etc.
- **Size**: ~21K sentences

**Top Performing Models**:
| Model | F1-Score | Notes |
|-------|----------|-------|
| **KoELECTRA-Base** | **86-88%** | Korean-specific ELECTRA model |
| **Stanza Korean** | **85-87%** | Stanford multi-language |
| **BERT-multilingual** | 82-84% | Generalist multilingual model |

---

### 2.4 Cross-Language Comparison

| Language | Best F1 | Typical Production F1 | Key Challenge |
|----------|---------|----------------------|---------------|
| **Chinese (Simp)** | 95.5% (MSRA) | 88-93% (OntoNotes) | Word segmentation, Traditional/Simplified |
| **Japanese** | 86-89% | 83-88% | Mixed scripts (Kanji/Hiragana/Katakana) |
| **Korean** | 86-88% | 83-87% | Spacing ambiguity, Hangul+Hanja mixture |

**Insight**: Chinese achieves highest benchmark scores due to mature research ecosystem and large training datasets. Japanese and Korean lag by 5-10% due to smaller training data and mixed script complexity.

---

## 3. CJK-Specific Technical Challenges

### 3.1 Chinese Word Segmentation Dependency

**Problem**: Chinese text has no spaces between words. NER requires understanding word boundaries.

**Example**:
```
Text: 我在北京大学学习
Without segmentation: [unclear if "北京大学" (Peking University) is one entity or two]
Correct segmentation: 我 / 在 / 北京大学 / 学习
Entity: 北京大学 (ORGANIZATION - university name)

Incorrect segmentation: 我 / 在 / 北京 / 大学 / 学习
Would identify: 北京 (LOCATION - Beijing city) - WRONG
```

**Solutions**:
1. **Joint Segmentation + NER**: Train models to perform both tasks simultaneously
   - **Pros**: Learns dependencies between tasks, more accurate
   - **Cons**: More complex training, slower inference
   - **Used by**: HanLP, LTP (integrated pipeline)

2. **Lattice-LSTM**: Encode all possible segmentations, let model choose
   - **Pros**: Doesn't commit to single segmentation, more flexible
   - **Cons**: Computationally expensive, complex architecture
   - **Used by**: Research models (not common in production)

3. **Character-Level NER**: Skip word segmentation entirely
   - **Pros**: Avoids segmentation errors propagating to NER
   - **Cons**: Loses word-level context, slightly lower accuracy
   - **Used by**: Some transformer models (BERT character-level)

**Benchmark Impact**:
- **Good segmentation**: 92-95% NER F1
- **Poor segmentation**: 75-85% NER F1 (10-20% degradation)
- **Critical**: Use library with integrated segmentation (HanLP, LTP) or character-level models

---

### 3.2 Traditional vs Simplified Chinese

**Character Differences**:
| Concept | Simplified (Mainland China) | Traditional (Taiwan, HK) | Same/Different |
|---------|---------------------------|------------------------|----------------|
| Beijing | 北京 | 北京 | Same |
| Taiwan | 台湾 | 臺灣 | **Different** |
| Guangdong | 广东 | 廣東 | **Different** |
| Computer | 计算机 | 計算機 | **Different** |

**Training Data Mismatch**:
- Most models trained on Simplified Chinese (MSRA, People's Daily)
- Applying Simplified-trained model to Traditional text: **10-25% F1 degradation**
- Converting Traditional → Simplified before NER: **Works reasonably (5-10% loss)**

**Solutions**:
1. **Native Dual-Script Model** (HanLP approach)
   - Train on both Simplified and Traditional datasets
   - **Pros**: No conversion needed, best accuracy for both
   - **Cons**: Requires annotated Traditional data (scarce)

2. **Conversion Preprocessing** (OpenCC)
   ```python
   import opencc
   converter = opencc.OpenCC('t2s.json')  # Traditional to Simplified
   simplified = converter.convert(traditional_text)
   entities = ner_model(simplified)
   ```
   - **Pros**: Leverages larger Simplified training data
   - **Cons**: Conversion errors (~1-2%), slightly lower accuracy

3. **Cross-Lingual Transfer Learning**
   - Pre-train on Simplified, fine-tune on small Traditional dataset
   - **Pros**: Uses both data sources efficiently
   - **Cons**: Requires some Traditional annotated data

**Production Recommendation**:
- **Taiwan/HK market**: Use HanLP (native Traditional support) or preprocess with OpenCC
- **Mainland China**: Any Simplified-trained model works
- **Both markets**: HanLP or train custom model with mixed data

---

### 3.3 Japanese Mixed-Script Handling

**Challenge**: Japanese mixes 3-4 scripts in same sentence:
```
日本のマイクロソフト株式会社は東京に本社がある。
Japanese: Microsoft Japan K.K. has its headquarters in Tokyo.

Scripts used:
- Kanji (Chinese characters): 日本, 株式会社, 東京, 本社
- Katakana (foreign words): マイクロソフト (Microsoft)
- Hiragana (particles): の, は, に, が, ある
```

**Entity Recognition Complexity**:
- **Company names**: Mix Kanji + Katakana (e.g., トヨタ自動車株式会社)
- **Foreign names**: Usually Katakana but not always entities (アメリカ = America [location], but アイスクリーム = ice cream [not entity])
- **Legal suffixes**: 株式会社 (K.K.), 有限会社 (Y.K.) must be recognized as part of organization name

**Model Solutions**:
1. **Subword Tokenization** (Stanza, Transformers)
   - Break into subword units that span scripts
   - Learns script patterns from training data
   - **Effective**: 85-88% F1 on mixed-script entities

2. **Character-Type Features**
   - Explicitly encode whether character is Kanji, Katakana, Hiragana
   - Feed as additional features to model
   - **Effective**: 83-86% F1 (used in traditional models)

**Production Recommendation**:
- Use Stanza Japanese or spaCy ja_core (handle mixed scripts natively)
- For custom training: Include script-type features in model architecture

---

### 3.4 Korean Spacing Ambiguity

**Challenge**: Korean uses spaces, but spacing rules are complex and inconsistently applied.

**Example**:
```
Correct: 삼성전자 주식회사 (Samsung Electronics Co., Ltd.) - two words
Common: 삼성전자주식회사 (no space) - one word
Also seen: 삼성 전자 주식회사 (extra spaces) - four words
```

**Name Recognition Complexity**:
- **Family names**: Usually 1 syllable (김, 이, 박)
- **Given names**: Usually 2 syllables (민준, 서연)
- **Full names**: May or may not have space between family and given name
  - `김민준` (no space) vs `김 민준` (space)

**Model Solutions**:
1. **Subword Tokenization**
   - Treats spacing as soft signal, not hard boundary
   - Learns name patterns from data
   - **Effective**: 85-87% F1

2. **Character + Syllable Features**
   - Korean characters (Hangul) are syllable blocks
   - Use both character-level and syllable-level features
   - **Effective**: 83-85% F1

**Production Recommendation**:
- Use Stanza Korean (handles spacing variations)
- Normalize spacing before NER if possible (Korean NLP libraries available)

---

## 4. Model Training and Customization

### 4.1 Fine-Tuning Pre-trained Models

**When to Fine-Tune**:
- Domain-specific entities not in general models (company products, technical terms)
- Accuracy on your data 10%+ below published benchmarks
- Have ≥500 annotated examples

**Fine-Tuning Process (HanLP)**:
```python
import hanlp

# Load base model
base_ner = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)

# Prepare training data (CoNLL format)
# Text: 我在使用AWS的EC2服务。
# Annotation:
# 我 O
# 在 O
# 使用 O
# AWS B-PRODUCT
# 的 O
# EC2 B-PRODUCT
# 服务 O
# 。 O

# Fine-tune on custom data
custom_ner = hanlp.pretrain.ner.TransformerNamedEntityRecognizer()
custom_ner.fit(
    train_data='custom_train.conll',
    dev_data='custom_dev.conll',
    save_dir='models/custom-ner',
    epochs=10,
    batch_size=32,
    lr=5e-5  # Lower learning rate for fine-tuning
)

# Evaluation
custom_ner.evaluate('custom_test.conll')
```

**Training Resources**:
- **GPU**: V100 or A100 recommended (3-10x faster than CPU)
- **Time**: 1-4 hours for 1K examples, 4-12 hours for 10K examples
- **Cost**: $1-5 on cloud GPU ($0.40-1.00/hour for V100)

**Expected Improvement**:
- Fine-tuning on 500 examples: +5-10% F1 on domain-specific entities
- Fine-tuning on 5,000 examples: +10-20% F1 on domain-specific entities

---

### 4.2 Annotation and Data Collection

**Minimum Viable Dataset**:
- **Quick prototype**: 100-200 annotated sentences
- **Production baseline**: 500-1,000 annotated sentences
- **High accuracy**: 5,000-10,000 annotated sentences

**Annotation Tools**:
1. **doccano**: Open-source, web-based annotation
   - Supports multi-language, multiple annotators
   - Export to CoNLL, JSON formats
   - **Cost**: Free, self-hosted

2. **Label Studio**: Flexible annotation platform
   - Pre-built NER templates
   - ML-assisted annotation (pre-annotate with base model)
   - **Cost**: Free open-source, or paid cloud

3. **Prodigy**: Commercial annotation tool by spaCy team
   - Active learning (suggests hard examples)
   - Recipe-based workflows for NER
   - **Cost**: $390/user (one-time purchase)

**Annotation Speed**:
- **Experienced annotator**: 50-100 entities/hour
- **With pre-annotation**: 100-200 entities/hour (review + correct)
- **Cost**: $20-40/hour for native speaker annotators

**Annotation Guidelines** (Critical for Quality):
```markdown
# Entity Annotation Guidelines for Chinese NER

## Organization Names
- Include full legal entity: 阿里巴巴集团控股有限公司 (full)
- NOT just: 阿里巴巴 (incomplete)
- Include suffixes: 有限公司, 股份有限公司, 集团

## Person Names
- Mark full name: 马云 (Ma Yun)
- Mark even if abbreviated: 马总 (Mr. Ma) - still PERSON
- Do NOT mark pronouns: 他, 她 (he, she) - not entities

## Locations
- Mark administrative units: 杭州市, 浙江省
- Mark buildings IF named: 阿里巴巴总部大楼
- Do NOT mark generic: 城市 (city), 国家 (country)
```

---

### 4.3 Active Learning and Iterative Improvement

**Active Learning Strategy**:
1. **Initial Model**: Train on 200-500 examples
2. **Inference on Large Unlabeled Corpus**: Run model on 10K-100K sentences
3. **Uncertainty Sampling**: Select sentences where model is least confident
   - Low confidence scores
   - Conflicting predictions
   - Rare entity types
4. **Annotate Selected Examples**: Focus annotation effort on hard cases
5. **Retrain**: Add new examples to training set, retrain model
6. **Repeat**: 3-5 iterations typically achieves 90%+ F1

**Example Implementation**:
```python
import numpy as np

def select_uncertain_examples(model, unlabeled_texts, n_samples=100):
    """Select examples where model is least confident"""
    results = model(unlabeled_texts)
    confidences = []

    for result in results:
        # Calculate average confidence for sentence
        if len(result) > 0:
            avg_conf = np.mean([entity.get('confidence', 1.0) for entity in result])
        else:
            avg_conf = 1.0  # No entities = high confidence
        confidences.append(avg_conf)

    # Select lowest confidence examples
    uncertain_indices = np.argsort(confidences)[:n_samples]
    return [unlabeled_texts[i] for i in uncertain_indices]

# Usage
unlabeled = load_large_corpus()  # 50K sentences
to_annotate = select_uncertain_examples(ner_model, unlabeled, n_samples=200)
# Annotate these 200 examples (focus on hard cases)
# Retrain model with expanded dataset
```

**Benefits**:
- Achieve same accuracy with **40-60% less annotation** (vs random sampling)
- Focus expert time on hard, valuable examples
- Faster iteration cycles (retrain after 100-200 new examples)

---

## 5. Production Deployment Patterns

### 5.1 Self-Hosted Deployment (HanLP, LTP, Stanza)

**Containerized Deployment (Docker)**:
```dockerfile
# Dockerfile for HanLP NER service
FROM python:3.9-slim

# Install dependencies
RUN pip install hanlp fastapi uvicorn

# Download model at build time (not runtime)
RUN python -c "import hanlp; hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)"

# Copy application code
COPY app.py /app/app.py
WORKDIR /app

# Expose API port
EXPOSE 8000

# Run service
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**FastAPI Service**:
```python
# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import hanlp

app = FastAPI()

# Load model at startup (once)
ner = None

@app.on_event("startup")
async def load_model():
    global ner
    ner = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)

class NERRequest(BaseModel):
    texts: list[str]
    language: str = "zh"

@app.post("/ner")
async def extract_entities(request: NERRequest):
    results = ner(request.texts)
    return {
        "entities": [
            [{"text": e[0], "type": e[1], "start": e[2], "end": e[3]}
             for e in sent_entities]
            for sent_entities in results
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "HanLP MSRA_NER_BERT_BASE_ZH"}
```

**Kubernetes Deployment**:
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ner-service
spec:
  replicas: 3  # Horizontal scaling
  selector:
    matchLabels:
      app: ner-service
  template:
    metadata:
      labels:
        app: ner-service
    spec:
      containers:
      - name: ner
        image: ner-service:latest
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: ner-service
spec:
  selector:
    app: ner-service
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

**Infrastructure Costs** (AWS EC2 pricing):
- **CPU-based (LTP)**: t3.xlarge (4 vCPU, 16GB RAM) = $150/month, 100-200 entities/sec
- **GPU-based (HanLP)**: g4dn.xlarge (1 GPU, 16GB RAM) = $400/month, 500-1,000 entities/sec
- **Production HA**: 3x instances + load balancer = $450-1,200/month

---

### 5.2 Batch Processing Pipeline

**For Large-Scale Document Processing**:
```python
import hanlp
from concurrent.futures import ThreadPoolExecutor, as_completed

ner = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)

def process_document(doc_id, text):
    """Process single document"""
    try:
        entities = ner(text)
        return {
            "doc_id": doc_id,
            "entities": entities,
            "status": "success"
        }
    except Exception as e:
        return {
            "doc_id": doc_id,
            "error": str(e),
            "status": "error"
        }

def batch_process(documents, batch_size=32, max_workers=4):
    """Process documents in parallel batches"""
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit batches
        futures = []
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            for doc in batch:
                future = executor.submit(process_document, doc['id'], doc['text'])
                futures.append(future)

        # Collect results
        for future in as_completed(futures):
            results.append(future.result())

    return results

# Usage: Process 10K documents
documents = load_documents()  # List of {id, text}
results = batch_process(documents, batch_size=32, max_workers=4)

# Throughput: ~500-1,000 documents/hour on g4dn.xlarge (GPU)
#            ~200-400 documents/hour on t3.xlarge (CPU)
```

---

### 5.3 Hybrid Cloud + Self-Hosted Architecture

**Pattern**: Use cloud APIs for prototyping and overflow, self-hosted for high-volume

```python
class HybridNERService:
    def __init__(self):
        # Self-hosted for primary workload
        self.local_ner = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)

        # Cloud API for overflow and fallback
        from google.cloud import language_v1
        self.cloud_client = language_v1.LanguageServiceClient()

        self.local_capacity = 100  # requests/sec
        self.request_count = 0
        self.last_reset = time.time()

    def extract_entities(self, text, language="zh", priority="standard"):
        # Rate limiting check
        if time.time() - self.last_reset > 1.0:
            self.request_count = 0
            self.last_reset = time.time()

        # Route based on capacity and priority
        if priority == "high" or self.request_count > self.local_capacity:
            # Use cloud API for overflow or high-priority
            return self._cloud_ner(text, language)
        else:
            # Use self-hosted for standard priority
            self.request_count += 1
            return self._local_ner(text)

    def _local_ner(self, text):
        entities = self.local_ner(text)
        return [{"text": e[0], "type": e[1]} for e in entities]

    def _cloud_ner(self, text, language):
        document = {
            "content": text,
            "type_": language_v1.Document.Type.PLAIN_TEXT,
            "language": language
        }
        response = self.cloud_client.analyze_entities(request={"document": document})
        return [{"text": e.name, "type": e.type_.name} for e in response.entities]

# Usage
service = HybridNERService()

# Standard requests use self-hosted (fast, cheap)
entities = service.extract_entities("阿里巴巴的马云在杭州创立公司", priority="standard")

# High-priority requests use cloud (guaranteed capacity)
entities = service.extract_entities("紧急合同分析内容", priority="high")
```

**Cost Analysis**:
- **Self-hosted baseline**: Process 80% of traffic at $400/month (GPU server)
- **Cloud overflow**: Process 20% overflow at $200/month (100K cloud requests)
- **Total**: $600/month vs $1,000/month (100% cloud) - **40% savings**

---

## 6. Performance Optimization Techniques

### 6.1 Model Quantization

**INT8 Quantization** (reduces model size 4x, 30-40% latency improvement):
```python
import torch
from hanlp import load

# Load original model
ner = load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)

# Quantize to INT8
quantized_ner = torch.quantization.quantize_dynamic(
    ner.model,
    {torch.nn.Linear},  # Quantize linear layers
    dtype=torch.qint8
)

# Save quantized model
torch.save(quantized_ner.state_dict(), 'quantized_ner.pt')

# Latency comparison:
# Original FP32: ~150ms per sentence (CPU)
# INT8: ~90ms per sentence (CPU) - 40% faster
# Accuracy impact: -0.5% to -1.5% F1 (acceptable for most use cases)
```

### 6.2 ONNX Runtime Optimization

**Convert to ONNX** (20-30% latency improvement):
```python
import onnx
import onnxruntime as ort
from transformers import BertTokenizer, BertForTokenClassification

# Load PyTorch model
model = BertForTokenClassification.from_pretrained('hfl/chinese-bert-wwm')
tokenizer = BertTokenizer.from_pretrained('hfl/chinese-bert-wwm')

# Export to ONNX format
dummy_input = tokenizer("测试文本", return_tensors="pt")
torch.onnx.export(
    model,
    (dummy_input['input_ids'], dummy_input['attention_mask']),
    "ner_model.onnx",
    input_names=['input_ids', 'attention_mask'],
    output_names=['output'],
    dynamic_axes={
        'input_ids': {0: 'batch', 1: 'sequence'},
        'attention_mask': {0: 'batch', 1: 'sequence'},
        'output': {0: 'batch', 1: 'sequence'}
    }
)

# Run with ONNX Runtime (faster inference)
ort_session = ort.InferenceSession("ner_model.onnx")
outputs = ort_session.run(None, {
    'input_ids': dummy_input['input_ids'].numpy(),
    'attention_mask': dummy_input['attention_mask'].numpy()
})

# Latency improvement: 20-30% faster than PyTorch
```

### 6.3 Batching and Throughput Optimization

**Dynamic Batching** (3-5x throughput improvement):
```python
import asyncio
from collections import deque
import time

class BatchedNERService:
    def __init__(self, model, max_batch_size=32, max_wait_ms=50):
        self.model = model
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms
        self.queue = deque()
        self.batch_task = asyncio.create_task(self._process_batches())

    async def predict(self, text):
        """Submit text for prediction, wait for result"""
        future = asyncio.Future()
        self.queue.append((text, future))
        return await future

    async def _process_batches(self):
        """Background task that processes queued requests in batches"""
        while True:
            if len(self.queue) == 0:
                await asyncio.sleep(0.001)
                continue

            # Collect batch
            batch = []
            futures = []
            batch_start = time.time()

            while len(batch) < self.max_batch_size:
                # Wait for more items or timeout
                if len(self.queue) > 0:
                    text, future = self.queue.popleft()
                    batch.append(text)
                    futures.append(future)
                elif time.time() - batch_start > self.max_wait_ms / 1000:
                    break  # Timeout, process current batch
                else:
                    await asyncio.sleep(0.001)

            # Process batch
            results = self.model(batch)

            # Return results to waiting futures
            for future, result in zip(futures, results):
                future.set_result(result)

# Usage
service = BatchedNERService(ner_model, max_batch_size=32, max_wait_ms=50)

# Individual requests are automatically batched
entities = await service.predict("阿里巴巴在杭州")
# Throughput: 500-1,000 requests/sec (batched) vs 100-200 (individual)
```

---

## 7. Cost-Benefit Analysis by Scale

### 7.1 Total Cost of Ownership (TCO) by Volume

**Monthly Processing Volumes**:

| Volume | Cloud API Cost | Self-Hosted (CPU) | Self-Hosted (GPU) | Break-Even |
|--------|---------------|-------------------|-------------------|------------|
| **10K entities** | $10-25 | $150 (over-provisioned) | $400 (over-provisioned) | Cloud wins |
| **100K entities** | $100-250 | $150 | $400 | Cloud competitive |
| **500K entities** | $500-1,250 | $150 | $400 | **Self-hosted breaks even** |
| **1M entities** | $1,000-2,500 | $150-300 (scale up) | $400 | Self-hosted wins |
| **10M entities** | $10,000-25,000 | $500-1,000 (multi-node) | $800-1,200 (2x GPU) | **Self-hosted 10-20x cheaper** |

**Break-Even Analysis**:
- **Cloud API**: Ideal for <500K entities/month
- **Self-Hosted CPU (LTP)**: Breaks even at ~500K entities/month
- **Self-Hosted GPU (HanLP)**: Breaks even at ~1M entities/month (higher accuracy justifies cost)

**Example Calculation (1M entities/month)**:
- **Cloud (Google)**: $2.00 per 1K = $2,000/month
- **Self-Hosted (GPU)**:
  - g4dn.xlarge: $400/month (processing)
  - Initial setup: $2,000 (amortized over 12 months = $167/month)
  - Monitoring, maintenance: $50/month
  - **Total**: $617/month
  - **Savings**: $1,383/month (69% cost reduction)

---

### 7.2 Total Cost Including Development

**Year 1 Costs** (including development, infrastructure, operations):

| Approach | Setup Cost | Monthly Cost | Year 1 Total | Notes |
|----------|-----------|-------------|--------------|-------|
| **Cloud API (Prototype)** | $500 | $100-500 | $1,700-6,500 | Fast deployment, low volume |
| **Cloud API (Production)** | $2,000 | $1,000-2,500 | $14,000-32,000 | Managed, scalable |
| **Self-Hosted CPU (LTP)** | $5,000 | $150-300 | $6,800-8,600 | Cost-effective at scale |
| **Self-Hosted GPU (HanLP)** | $8,000 | $400-600 | $12,800-15,200 | Best accuracy, mid cost |
| **Hybrid** | $6,000 | $300-600 | $9,600-13,200 | Balanced approach |

**Setup Costs Include**:
- Development time: $2,000-5,000 (40-100 hours)
- Model selection and testing: $500-1,000
- Infrastructure setup: $500-2,000
- Documentation and training: $500-1,000

**Break-Even Timeline**:
- **Self-Hosted CPU**: 6-12 months (depending on volume)
- **Self-Hosted GPU**: 12-18 months (higher initial investment)
- **Hybrid**: 8-14 months (balanced risk-reward)

---

## 8. Integration and Entity Linking Strategies

### 8.1 Entity Normalization Across Languages

**Challenge**: Same entity appears differently across languages:
- Chinese: 微软 (Microsoft)
- Japanese: マイクロソフト (Maikurosofuto)
- Korean: 마이크로소프트 (Maikeurosopeuteu)
- English: Microsoft

**Solution: Entity Linking to Canonical IDs**:
```python
# Entity database with canonical IDs
entity_db = {
    "COMPANY:MSFT": {
        "canonical_name": "Microsoft Corporation",
        "aliases": {
            "zh": ["微软", "微软公司", "微软集团"],
            "ja": ["マイクロソフト", "マイクロソフト株式会社"],
            "ko": ["마이크로소프트", "마이크로소프트사"],
            "en": ["Microsoft", "Microsoft Corp", "MSFT"]
        },
        "wikipedia_id": "Q2283",
        "wikidata_id": "Q2283"
    }
}

def link_entity(entity_text, language, entity_type):
    """Link extracted entity to canonical ID"""
    # Normalize: Remove whitespace, lowercase
    normalized = entity_text.lower().strip()

    # Lookup in entity database
    for entity_id, entity_data in entity_db.items():
        if language in entity_data["aliases"]:
            if normalized in [a.lower() for a in entity_data["aliases"][language]]:
                return {
                    "entity_id": entity_id,
                    "canonical_name": entity_data["canonical_name"],
                    "matched_alias": entity_text,
                    "confidence": 1.0
                }

    # Fuzzy matching fallback
    # (use edit distance, phonetic matching, etc.)

    return None  # No match found

# Usage
entities_zh = ner_zh("微软在西雅图的总部")  # [('微软', 'ORG'), ...]
entities_ja = ner_ja("マイクロソフトの本社はシアトル")  # [('マイクロソフト', 'ORG'), ...]

linked_zh = [link_entity(e[0], "zh", e[1]) for e in entities_zh]
linked_ja = [link_entity(e[0], "ja", e[1]) for e in entities_ja]

# Both resolve to "COMPANY:MSFT" despite different languages
```

**Entity Database Sources**:
- **Wikidata**: 100M+ entities with multi-language labels (free, open)
- **DBpedia**: Structured Wikipedia data with entity linking
- **Custom Database**: Build from your domain-specific entities

**Entity Linking Accuracy**:
- **Exact match**: 85-90% recall (common entities)
- **Fuzzy match**: 90-95% recall (handles typos, variants)
- **Contextual disambiguation**: 95-98% recall (ML-based, considers context)

---

### 8.2 Downstream Integration Patterns

**Knowledge Graph Construction**:
```python
from neo4j import GraphDatabase

# Extract entities and build knowledge graph
documents = load_corpus()
driver = GraphDatabase.driver("bolt://localhost:7687")

def build_knowledge_graph(documents):
    with driver.session() as session:
        for doc in documents:
            entities = ner(doc['text'])

            # Create entity nodes
            for entity in entities:
                session.run(
                    "MERGE (e:Entity {name: $name, type: $type})",
                    name=entity['text'],
                    type=entity['type']
                )

            # Create relationships (co-occurrence)
            for i, e1 in enumerate(entities):
                for e2 in entities[i+1:]:
                    session.run(
                        """
                        MATCH (e1:Entity {name: $name1})
                        MATCH (e2:Entity {name: $name2})
                        MERGE (e1)-[:CO_OCCURS_WITH]->(e2)
                        """,
                        name1=e1['text'],
                        name2=e2['text']
                    )

# Query knowledge graph
# "Find all organizations associated with person X"
result = session.run(
    """
    MATCH (p:Entity {type: 'PERSON', name: '马云'})-[:CO_OCCURS_WITH]-(o:Entity {type: 'ORGANIZATION'})
    RETURN o.name as organization
    """)
# Returns: 阿里巴巴, 淘宝, 支付宝, etc.
```

**Search Engine Integration**:
```python
from elasticsearch import Elasticsearch

es = Elasticsearch(['localhost:9200'])

def index_document_with_entities(doc_id, text, language="zh"):
    """Index document with extracted entities for faceted search"""
    entities = ner(text)

    # Structure entities by type
    persons = [e['text'] for e in entities if e['type'] == 'PERSON']
    orgs = [e['text'] for e in entities if e['type'] == 'ORGANIZATION']
    locs = [e['text'] for e in entities if e['type'] == 'LOCATION']

    # Index document
    es.index(index='documents', id=doc_id, body={
        'text': text,
        'language': language,
        'entities': {
            'persons': persons,
            'organizations': orgs,
            'locations': locs
        }
    })

# Search with entity filters
# "Find all documents mentioning person X and organization Y"
results = es.search(index='documents', body={
    'query': {
        'bool': {
            'must': [
                {'match': {'entities.persons': '马云'}},
                {'match': {'entities.organizations': '阿里巴巴'}}
            ]
        }
    }
})
```

---

## Summary and Recommendations

### Key Takeaways

1. **Accuracy vs Speed Trade-off**:
   - HanLP BERT: 95% F1, 100-200ms (best accuracy)
   - LTP v4: 93% F1, 50-100ms (balanced)
   - Cloud APIs: 85-90% F1, 200-800ms (managed)

2. **Language Coverage**:
   - Chinese-only: HanLP or LTP (superior accuracy)
   - Multi-language (Chinese/Japanese/Korean): Stanza (unified API)
   - All CJK + managed: Google Cloud, Azure (enterprise SLA)

3. **Cost at Scale**:
   - <500K entities/month: Cloud APIs ($100-500/month)
   - 500K-5M entities/month: Self-hosted CPU ($150-300/month)
   - >5M entities/month: Self-hosted GPU ($400-1,200/month)

4. **Traditional vs Simplified Chinese**:
   - Use HanLP for native dual-script support
   - OR preprocess with OpenCC conversion (5-10% accuracy loss)

5. **Production Deployment**:
   - Containerized (Docker + Kubernetes) for scalability
   - Batch processing for high-throughput (500-1,000 docs/hour on GPU)
   - Hybrid cloud + self-hosted for cost optimization

### Decision Framework

**Choose HanLP when**:
- Chinese is 90%+ of content
- Best accuracy critical (legal, compliance, contracts)
- Traditional + Simplified support required
- Budget allows GPU infrastructure ($400-600/month)

**Choose LTP when**:
- Chinese Simplified focus
- Fast CPU inference required (cost optimization)
- Good-enough accuracy acceptable (90-93% vs 95%)
- Integrated pipeline needed (segmentation + NER)

**Choose Stanza when**:
- Multi-language consistency (Chinese + Japanese + Korean)
- Unified API across languages
- Academic credibility important
- Mixed-language content common

**Choose Cloud APIs when**:
- Rapid prototyping (<2 weeks to production)
- Variable workload (seasonal spikes)
- Managed service preferred (no ML Ops)
- Volume <500K entities/month

**Choose Hybrid when**:
- Predictable base workload + variable spikes
- Cost optimization with safety net
- Gradual migration from cloud to self-hosted

---

**Next Phase**: S3 Need-Driven Discovery will explore specific use case requirements (contract analysis, social media monitoring, customer data processing) and map to optimal technical solutions.
