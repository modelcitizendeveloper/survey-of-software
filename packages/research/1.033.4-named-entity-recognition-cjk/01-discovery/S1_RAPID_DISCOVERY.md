# S1 RAPID DISCOVERY: Named Entity Recognition for CJK Languages

**Experiment**: 1.033.4 Named Entity Recognition for CJK Languages (subspecialization of 1.033 NLP Libraries)
**Date**: 2026-01-29
**Duration**: 45 minutes
**Context**: International business intelligence and data processing require extracting entities (persons, organizations, locations) from Chinese, Japanese, and Korean text. CJK languages present unique challenges: no word boundaries (Chinese), multiple writing systems (Traditional/Simplified Chinese; Kanji/Hiragana/Katakana), complex name conventions.

## Executive Summary

Identified 7 production-ready solutions for CJK Named Entity Recognition with varying trade-offs between accuracy, language coverage, and deployment complexity:

1. **HanLP** - Best for Chinese (Traditional & Simplified), state-of-art accuracy
2. **LTP (Language Technology Platform)** - Best for fast Chinese NER with CPU inference
3. **Stanza (Stanford NLP)** - Best for multi-language consistency (Chinese/Japanese/Korean)
4. **spaCy zh_core** - Best for production-ready Chinese pipelines with extensive ecosystem
5. **Google Cloud Natural Language API** - Best for rapid deployment, managed service
6. **Amazon Comprehend** - Best for AWS integration, custom entity training
7. **Azure Text Analytics** - Best for Microsoft ecosystem, enterprise compliance

**Recommendation**: Start with HanLP for Chinese-focused applications (best accuracy), Stanza for multi-language requirements (unified API), or cloud APIs for rapid prototyping before self-hosted commitment.

---

## Quick Comparison Table

| Solution | Languages | Accuracy | Speed (Latency) | Deployment | Model Size | Best For |
|----------|-----------|----------|----------------|------------|------------|----------|
| **HanLP** | Chinese (Simp/Trad), some JP/KR | Excellent (92-95%) | ~100-200ms (GPU) | Self-hosted | ~500MB-1GB | Chinese-focused, best accuracy |
| **LTP** | Chinese (primarily Simp) | Excellent (90-93%) | ~50-100ms (CPU) | Self-hosted | ~200-400MB | Fast Chinese, CPU deployment |
| **Stanza** | Chinese, Japanese, Korean | Excellent (88-92%) | ~150-300ms | Self-hosted | ~300-500MB per lang | Multi-language unified API |
| **spaCy zh_core** | Chinese (Simplified) | Good-Excellent (85-90%) | ~50-150ms | Self-hosted | ~40-500MB | Production pipelines, ecosystem |
| **Google Cloud API** | Chinese (Simp/Trad), JP, KR | Good (85-90%) | ~200-500ms | Managed | N/A (API) | Rapid deployment, managed |
| **Amazon Comprehend** | Chinese (Simp), Japanese | Good (85-90%) | ~300-800ms | Managed | N/A (API) | AWS integration, custom entities |
| **Azure Text Analytics** | Chinese (Simp/Trad), JP, KR | Good (85-90%) | ~200-500ms | Managed | N/A (API) | Microsoft ecosystem, enterprise |

---

## Detailed Findings

### 1. HanLP (Han Language Processing)

**What it is**: Open-source multi-task NLP toolkit from China with state-of-art Chinese NER, developed by HIT (Harbin Institute of Technology) researchers.

**Key Characteristics**:
- Supports both Simplified and Traditional Chinese natively
- BERT-based models achieving 92-95% F1 on standard benchmarks (MSRA, OntoNotes)
- Handles multiple entity types: Person (PER), Organization (ORG), Location (LOC), Time, Money, etc.
- Unified API for word segmentation, POS tagging, NER, dependency parsing
- Pre-trained models available, supports custom training

**Language Support**:
- Primary: Chinese (Simplified & Traditional)
- Secondary: Some Japanese and Korean support (less mature)

**Speed**: ~100-200ms per sentence on GPU, ~500-1000ms on CPU

**Accuracy**:
- MSRA NER Dataset: 95.5% F1
- OntoNotes 4.0: 80.5% F1
- Industry-leading for Chinese entity recognition

**Implementation**:
```python
import hanlp

# Load pre-trained NER model
ner = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)

text = "阿里巴巴的马云在杭州创立了这家公司。"
# "Jack Ma founded Alibaba in Hangzhou."

entities = ner(text)
# [('阿里巴巴', 'ORGANIZATION', 0, 4),
#  ('马云', 'PERSON', 5, 7),
#  ('杭州', 'LOCATION', 8, 10)]
```

**Pros**:
- Best-in-class accuracy for Chinese NER
- Native Traditional/Simplified support
- Comprehensive entity type coverage
- Active development and maintenance
- Strong research foundation (academic papers, benchmarks)

**Cons**:
- GPU recommended for reasonable speed
- Larger model sizes (500MB-1GB)
- Documentation primarily in Chinese (English available but less comprehensive)
- Japanese/Korean support less mature than Chinese

**Best for**: Chinese-focused applications where accuracy is critical, especially for business intelligence, compliance, contract analysis.

**Cost Model**: Free open source + GPU infrastructure ($100-500/month depending on throughput)

---

### 2. LTP (Language Technology Platform)

**What it is**: Comprehensive Chinese NLP toolkit from HIT (Harbin Institute of Technology), optimized for production deployment.

**Key Characteristics**:
- Efficient CNN/RNN-based models for fast CPU inference
- Integrated pipeline: word segmentation → POS tagging → NER → semantic role labeling
- Primarily focused on Simplified Chinese
- Strong academic foundation, widely used in Chinese NLP research
- Recent v4.0 adds neural models with improved accuracy

**Language Support**:
- Primary: Chinese (Simplified)
- Traditional Chinese: Requires preprocessing conversion

**Speed**: ~50-100ms per sentence on CPU (optimized for production)

**Accuracy**:
- People's Daily NER: 90-93% F1
- OntoNotes: 78-82% F1
- Fast models trade ~2-5% accuracy for 3-5x speed improvement

**Implementation**:
```python
from ltp import LTP

ltp = LTP()  # Load model
ltp.add_words(["阿里巴巴"])  # Custom dictionary (optional)

text = ["阿里巴巴的马云在杭州创立了这家公司。"]
result = ltp.pipeline(text, tasks=["cws", "pos", "ner"])

# result.ner: [[(0, 4, 'Ni'), (5, 7, 'Nh'), (8, 10, 'Ns')]]
# Ni=Organization, Nh=Person, Ns=Location
```

**Pros**:
- Fast CPU inference (ideal for cost-conscious deployments)
- Integrated pipeline reduces complexity
- Proven academic research foundation
- Good accuracy for most business use cases
- Smaller model sizes (~200-400MB)

**Cons**:
- Primarily Simplified Chinese (Traditional needs conversion)
- Slightly lower accuracy than HanLP on some benchmarks
- Tag schema differs from international standards (uses Ni, Nh, Ns vs PER, ORG, LOC)
- Less active development than HanLP recently

**Best for**: Production Chinese NER with tight latency requirements or CPU-only deployment constraints, integrated Chinese text processing pipelines.

**Cost Model**: Free open source + standard CPU servers ($50-200/month)

---

### 3. Stanza (Stanford NLP)

**What it is**: Stanford NLP Group's neural pipeline for multi-language NLP, including Chinese, Japanese, and Korean.

**Key Characteristics**:
- Unified Python API across 60+ languages including CJK
- Neural models with consistent architecture across languages
- Academic research quality from Stanford NLP Group
- Supports word segmentation, POS tagging, NER, dependency parsing
- Pre-trained models for Chinese (Simplified/Traditional), Japanese, Korean

**Language Support**:
- Chinese: Simplified and Traditional (separate models)
- Japanese: Full support with Kanji/Hiragana/Katakana handling
- Korean: Full support

**Speed**: ~150-300ms per sentence (depends on pipeline components)

**Accuracy**:
- Chinese OntoNotes 4.0: 88-90% F1
- Japanese: ~85-88% F1 (various benchmarks)
- Korean: ~85-87% F1

**Implementation**:
```python
import stanza

# Download models (one-time setup)
stanza.download('zh')  # Chinese (Simplified)
stanza.download('ja')  # Japanese
stanza.download('ko')  # Korean

# Initialize pipeline
nlp_zh = stanza.Pipeline('zh', processors='tokenize,ner')
nlp_ja = stanza.Pipeline('ja', processors='tokenize,ner')

# Chinese NER
doc_zh = nlp_zh("阿里巴巴的马云在杭州创立了这家公司。")
for ent in doc_zh.entities:
    print(f"{ent.text} - {ent.type}")
# 阿里巴巴 - ORG
# 马云 - PERSON
# 杭州 - GPE (Geo-Political Entity)

# Japanese NER
doc_ja = nlp_ja("東京にあるトヨタ自動車の本社")
for ent in doc_ja.entities:
    print(f"{ent.text} - {ent.type}")
# 東京 - GPE
# トヨタ自動車 - ORG
```

**Pros**:
- Unified API across Chinese, Japanese, Korean
- Consistent quality and architecture
- Strong academic credibility (Stanford)
- Excellent documentation in English
- Active maintenance and updates
- Works on CPU (GPU accelerates but not required)

**Cons**:
- Moderate accuracy (good but not state-of-art for Chinese)
- Slower than specialized libraries (LTP, spaCy)
- Larger model downloads for multi-language support
- Higher memory usage when loading multiple languages

**Best for**: Multi-language applications requiring consistent API across CJK languages, research-grade quality, international business intelligence processing mixed-language content.

**Cost Model**: Free open source + standard infrastructure ($100-300/month for multi-language deployment)

---

### 4. spaCy zh_core Models

**What it is**: spaCy's Chinese language models providing production-ready NER with extensive ecosystem integration.

**Key Characteristics**:
- Multiple model sizes: sm (small), md (medium), lg (large), trf (transformer)
- Industrial-grade engineering and reliability
- Extensive ecosystem: visualization (displaCy), training tools, integration packages
- Efficient CPU inference for smaller models
- Transformer models (zh_core_web_trf) for state-of-art accuracy

**Language Support**:
- Chinese Simplified only
- Traditional Chinese requires separate preprocessing

**Speed**:
- Small/Medium models: ~50-150ms (CPU-friendly)
- Transformer models: ~200-400ms (GPU recommended)

**Accuracy**:
- Small model (zh_core_web_sm): 80-85% F1
- Medium model (zh_core_web_md): 85-88% F1
- Large model (zh_core_web_lg): 88-90% F1
- Transformer (zh_core_web_trf): 90-92% F1

**Implementation**:
```python
import spacy

# Load model (download first: python -m spacy download zh_core_web_md)
nlp = spacy.load("zh_core_web_md")

text = "阿里巴巴的马云在杭州创立了这家公司。"
doc = nlp(text)

for ent in doc.ents:
    print(f"{ent.text} - {ent.label_}")
# 阿里巴巴 - ORG
# 马云 - PERSON
# 杭州 - GPE
```

**Pros**:
- Excellent production engineering (reliable, well-tested)
- Multiple model sizes for speed/accuracy trade-offs
- Extensive ecosystem and tooling
- Excellent English documentation and community
- Easy custom training and entity ruler patterns
- Efficient CPU inference for sm/md models

**Cons**:
- Chinese support less mature than English
- Simplified Chinese only (no native Traditional support)
- Accuracy slightly lower than HanLP for Chinese
- No Japanese or Korean support (separate models)

**Best for**: Production systems with existing spaCy infrastructure, organizations valuing ecosystem maturity and engineering quality, applications requiring rapid CPU inference.

**Cost Model**: Free open source + standard infrastructure ($50-300/month depending on model size)

---

### 5. Google Cloud Natural Language API

**What it is**: Managed NER service from Google Cloud with multi-language support including Chinese, Japanese, Korean.

**Key Characteristics**:
- Fully managed - no infrastructure to maintain
- Supports Simplified Chinese, Traditional Chinese, Japanese, Korean
- RESTful API with client libraries for Python, Java, Node.js, etc.
- Entity types: Person, Organization, Location, Event, Work of Art, Consumer Good, etc.
- Salience scores indicating entity importance in text
- Integrated with Google Cloud ecosystem (AutoML, BigQuery, etc.)

**Language Support**:
- Chinese: Simplified and Traditional
- Japanese: Full support
- Korean: Full support

**Speed**: ~200-500ms per request (network + processing)

**Accuracy**: 85-90% F1 on diverse content (Google doesn't publish detailed benchmarks)

**Implementation**:
```python
from google.cloud import language_v1

client = language_v1.LanguageServiceClient()

text = "阿里巴巴的马云在杭州创立了这家公司。"
document = {
    "content": text,
    "type_": language_v1.Document.Type.PLAIN_TEXT,
    "language": "zh"  # or "zh-Hant" for Traditional, "ja", "ko"
}

response = client.analyze_entities(request={"document": document})

for entity in response.entities:
    print(f"{entity.name} - {entity.type_} (salience: {entity.salience:.2f})")
# 阿里巴巴 - ORGANIZATION (salience: 0.45)
# 马云 - PERSON (salience: 0.38)
# 杭州 - LOCATION (salience: 0.17)
```

**Pros**:
- Zero infrastructure management
- Unified API across all CJK languages
- Automatic model updates and improvements
- Enterprise SLA and support
- Handles Traditional/Simplified Chinese seamlessly
- Salience scores for entity importance

**Cons**:
- Per-request pricing can be expensive at scale
- Network latency adds to processing time
- No custom entity type training (standard types only)
- Data leaves your infrastructure (compliance consideration)
- Vendor lock-in risk

**Best for**: Rapid prototyping, variable workloads, organizations with existing Google Cloud infrastructure, applications where managed service justifies cost.

**Cost Model**: $1.00-2.50 per 1,000 requests (volume discounts available)

---

### 6. Amazon Comprehend

**What it is**: AWS managed NLP service with entity recognition for Chinese and Japanese.

**Key Characteristics**:
- Fully managed AWS service
- Supports Simplified Chinese and Japanese (Korean planned)
- Custom entity recognition training available
- Batch and real-time processing modes
- Integrated with AWS ecosystem (S3, Lambda, SageMaker)
- Entity types: Person, Organization, Location, Date, Quantity, Title, Event, etc.

**Language Support**:
- Chinese: Simplified (Traditional not officially supported but may work)
- Japanese: Full support
- Korean: Limited/experimental

**Speed**: ~300-800ms per document (API processing), batch mode more efficient

**Accuracy**: 85-90% F1 on standard entities (AWS doesn't publish detailed benchmarks)

**Implementation**:
```python
import boto3

comprehend = boto3.client('comprehend', region_name='us-east-1')

text = "阿里巴巴的马云在杭州创立了这家公司。"
response = comprehend.detect_entities(
    Text=text,
    LanguageCode='zh'  # or 'ja' for Japanese
)

for entity in response['Entities']:
    print(f"{entity['Text']} - {entity['Type']} (confidence: {entity['Score']:.2f})")
# 阿里巴巴 - ORGANIZATION (confidence: 0.98)
# 马云 - PERSON (confidence: 0.95)
# 杭州 - LOCATION (confidence: 0.92)
```

**Custom Entity Training**:
```python
# Train custom entity recognizer for domain-specific entities
response = comprehend.create_entity_recognizer(
    RecognizerName='custom-chinese-entities',
    LanguageCode='zh',
    InputDataConfig={
        'EntityTypes': [{'Type': 'PRODUCT'}, {'Type': 'COMPETITOR'}],
        'Documents': {'S3Uri': 's3://bucket/training-docs/'},
        'Annotations': {'S3Uri': 's3://bucket/annotations/'}
    },
    DataAccessRoleArn='arn:aws:iam::...'
)
```

**Pros**:
- Seamless AWS integration (S3, Lambda, CloudWatch)
- Custom entity recognition training
- Batch processing for cost efficiency
- Enterprise SLA and support
- Pay-per-use pricing model
- No infrastructure management

**Cons**:
- Limited language support (no Korean, Traditional Chinese uncertain)
- Higher latency than self-hosted
- Custom training requires annotation effort
- Vendor lock-in to AWS ecosystem
- More expensive than open-source at scale

**Best for**: AWS-native applications, organizations with AWS infrastructure, custom entity types requiring domain-specific training, batch processing workloads.

**Cost Model**: $0.0001 per unit (100 characters), custom entities $3.00 per hour training + $0.50/month storage + inference costs

---

### 7. Azure Text Analytics (Language Service)

**What it is**: Microsoft Azure cognitive service providing NER for multiple languages including Chinese, Japanese, Korean.

**Key Characteristics**:
- Part of Azure Cognitive Services / Language Service
- Supports Simplified Chinese, Traditional Chinese, Japanese, Korean
- Entity types: Person, Organization, Location, DateTime, Quantity, Skill, etc.
- Entity linking to Wikipedia/knowledge bases
- Integrated with Microsoft ecosystem (Power BI, Office, SharePoint)
- Custom NER available through Language Studio

**Language Support**:
- Chinese: Simplified and Traditional
- Japanese: Full support
- Korean: Full support

**Speed**: ~200-500ms per request

**Accuracy**: 85-90% F1 (Microsoft doesn't publish detailed benchmarks)

**Implementation**:
```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

client = TextAnalyticsClient(
    endpoint="https://<your-resource>.cognitiveservices.azure.com/",
    credential=AzureKeyCredential("<your-key>")
)

text = "阿里巴巴的马云在杭州创立了这家公司。"
documents = [text]
result = client.recognize_entities(documents, language="zh-Hans")
# language options: "zh-Hans" (Simplified), "zh-Hant" (Traditional), "ja", "ko"

for entity in result[0].entities:
    print(f"{entity.text} - {entity.category} (confidence: {entity.confidence_score:.2f})")
# 阿里巴巴 - Organization (confidence: 0.95)
# 马云 - Person (confidence: 0.98)
# 杭州 - Location (confidence: 0.93)
```

**Pros**:
- Native Traditional/Simplified Chinese support
- Full CJK language coverage
- Entity linking to knowledge bases
- Microsoft ecosystem integration
- Custom NER training via Language Studio
- Enterprise compliance and certifications
- Free tier (5,000 requests/month)

**Cons**:
- Vendor lock-in to Azure
- Network latency overhead
- Cost at scale vs self-hosted
- Standard entity types (custom requires training)
- API limits and throttling

**Best for**: Microsoft-centric organizations, enterprise applications requiring compliance certifications, applications leveraging Office/Power BI integration, balanced CJK language support.

**Cost Model**: Free tier 5,000 text records/month, then $1-4 per 1,000 text records depending on features (custom NER higher pricing)

---

## Key Findings Summary

### Accuracy Hierarchy (Chinese NER)
1. **HanLP**: 92-95% F1 (best-in-class)
2. **LTP**: 90-93% F1 (fast, CPU-friendly)
3. **Stanza**: 88-90% F1 (multi-language consistency)
4. **spaCy**: 88-92% F1 (trf model, 80-85% for sm/md)
5. **Cloud APIs**: 85-90% F1 (estimated, managed)

### Speed Hierarchy (Lower is Better)
1. **LTP (CPU)**: 50-100ms
2. **spaCy sm/md (CPU)**: 50-150ms
3. **HanLP (GPU)**: 100-200ms
4. **Stanza**: 150-300ms
5. **Cloud APIs**: 200-800ms (includes network)

### Language Coverage
- **Chinese Only**: LTP, spaCy (Simplified focus)
- **Chinese Best**: HanLP (Traditional + Simplified)
- **Multi-CJK**: Stanza, Google Cloud, Azure (all three languages)
- **Chinese + Japanese**: Amazon Comprehend

### Deployment Complexity
- **Easiest**: Cloud APIs (zero infrastructure)
- **Moderate**: spaCy, LTP (standard Python deployment)
- **Advanced**: HanLP, Stanza (GPU recommended, larger models)

### Cost at Scale (1M entities/month)
- **Lowest**: Self-hosted LTP/spaCy ($50-200/month infrastructure)
- **Low-Medium**: HanLP GPU ($200-500/month)
- **High**: Cloud APIs ($1,000-2,500/month)

---

## Decision Framework

### Choose HanLP When:
- Chinese is primary focus (90%+ of content)
- Best accuracy is critical (compliance, contracts, legal)
- Traditional and Simplified support both required
- Willing to invest in GPU infrastructure
- Self-hosted preferred (data sovereignty, China regulations)

### Choose LTP When:
- Chinese Simplified is primary language
- Fast CPU inference required (cost optimization)
- Integrated Chinese pipeline needed (segmentation + POS + NER)
- Academic research foundation valued
- Budget constraints favor CPU-only deployment

### Choose Stanza When:
- Multi-language consistency across Chinese, Japanese, Korean
- Unified API across CJK languages is priority
- Stanford academic credibility important
- Mixed-language content processing
- Research or analysis requiring cross-language entity linking

### Choose spaCy zh_core When:
- Existing spaCy infrastructure in production
- Extensive ecosystem tooling needed (visualization, training)
- Multiple model size options for speed/accuracy trade-offs
- Industrial-grade engineering and reliability priority
- Simplified Chinese sufficient for use case

### Choose Cloud APIs (Google/AWS/Azure) When:
- Rapid deployment more important than long-term cost
- Variable workload not justifying dedicated infrastructure
- Managed service preferred (no ML ops capability)
- Standard entity types sufficient (no custom training needed)
- Enterprise SLA and support required

---

## Implementation Recommendations

### Rapid Prototyping (Week 1-2)
**Start with**: Google Cloud Natural Language API or Azure Text Analytics
- Zero infrastructure setup
- Validate business value quickly
- Test accuracy on your specific content
- Cost: ~$100-500 for prototype phase

### Production MVP (Month 1-2)
**Migrate to**: HanLP (Chinese focus) or Stanza (multi-language)
- Deploy self-hosted models
- 70-90% cost reduction vs cloud APIs
- Full control over data and processing
- Cost: $200-500/month infrastructure + initial setup

### Scale Optimization (Month 3+)
**Optimize**: Hybrid architecture
- Fast path: LTP or spaCy for high-volume standard entities
- Accurate path: HanLP for high-value or complex entities
- Fallback: Cloud API for edge cases or new languages
- Cost: Optimized for throughput and accuracy balance

---

## Technical Considerations

### Chinese-Specific Challenges

**Word Segmentation Dependency**:
- Chinese has no spaces between words
- NER accuracy depends on segmentation quality
- HanLP, LTP include optimized segmenters
- Stanza, spaCy handle segmentation internally

**Traditional vs Simplified**:
- Mainland China: Simplified (简体)
- Taiwan, Hong Kong: Traditional (繁體)
- Some entities identical: 北京 (Beijing)
- Others differ: 台湾/臺灣 (Taiwan), 广东/廣東 (Guangdong)
- **Solution**: Use HanLP (native support) or preprocess with OpenCC converter

**Name Disambiguation**:
- Chinese names are short: 李明, 王伟 (2-3 characters)
- Same name, different people: 李伟 could be thousands of individuals
- Context critical for accurate entity resolution
- **Solution**: Entity linking to databases, confidence thresholds

### Japanese-Specific Challenges

**Mixed Scripts**:
- Kanji (漢字): 東京, 日本 - entity candidates
- Hiragana (ひらがな): Typically particles, not entities
- Katakana (カタカナ): Foreign names/companies (マイクロソフト = Microsoft)
- Romaji: Latin alphabet mixed in

**Corporate Naming**:
- Legal suffixes: 株式会社 (K.K.), 有限会社 (Y.K.), 合同会社 (G.K.)
- Position matters: トヨタ自動車株式会社 vs 株式会社トヨタ自動車

**Best Tool**: Stanza Japanese models handle mixed scripts well

### Korean-Specific Challenges

**Spacing Rules**:
- Korean uses spaces (unlike Chinese) but rules are complex
- Proper nouns may or may not be spaced consistently
- Historical texts use Chinese characters (Hanja) occasionally

**Name Conventions**:
- Family name (1 syllable) + Given name (2 syllables): 김민준 (Kim Min-jun)
- Corporate names: Mix Hangul and English (삼성전자 Samsung Electronics)

**Best Tool**: Stanza Korean models or Azure/Google APIs

---

## Performance Benchmarks (Approximate)

### Throughput Comparison (entities per second)

**CPU-based (8-core server)**:
- LTP: 200-500 entities/second
- spaCy sm/md: 150-400 entities/second
- Stanza: 50-150 entities/second
- HanLP CPU: 20-80 entities/second

**GPU-based (single V100)**:
- HanLP: 500-1,000 entities/second
- Stanza: 300-600 entities/second
- spaCy trf: 400-800 entities/second

**Cloud APIs (rate limits)**:
- Google Cloud: 600 requests/minute (free tier), higher with quota increase
- AWS Comprehend: 100 units/second (unit = 100 chars), burst up to 500
- Azure: 300 requests/minute (S tier)

### Cost per Million Entities

**Self-Hosted**:
- LTP (CPU): ~$50-100 (infrastructure amortized)
- spaCy (CPU): ~$50-100
- HanLP (GPU): ~$200-300
- Stanza (GPU): ~$200-300

**Cloud APIs**:
- Google Cloud: ~$1,000-2,500 (volume discounts)
- AWS Comprehend: ~$800-2,000 (depends on text size)
- Azure: ~$1,000-4,000 (depends on tier and features)

---

## Integration Patterns

### Batch Processing Pipeline
```python
# Efficient batch processing with HanLP
import hanlp
ner = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)

documents = [...]  # Large corpus
batch_size = 32

for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    results = ner(batch)  # Process batch together
    # Store results...
```

### Real-Time API Service
```python
from fastapi import FastAPI
import stanza

app = FastAPI()
nlp_zh = stanza.Pipeline('zh', processors='tokenize,ner')

@app.post("/ner")
async def extract_entities(text: str, language: str = "zh"):
    nlp = nlp_zh if language == "zh" else nlp_ja
    doc = nlp(text)
    entities = [{"text": ent.text, "type": ent.type} for ent in doc.entities]
    return {"entities": entities}
```

### Hybrid Cloud + Self-Hosted
```python
def extract_entities(text, language, priority="standard"):
    """Route based on priority and language"""
    if priority == "high" or language not in ["zh", "ja", "ko"]:
        # Use cloud API for high-priority or unsupported languages
        return google_cloud_ner(text, language)
    else:
        # Use self-hosted for standard priority supported languages
        if language == "zh":
            return hanlp_ner(text)
        elif language == "ja":
            return stanza_ner(text, "ja")
        else:
            return stanza_ner(text, "ko")
```

---

## Next Steps for S2 Comprehensive Discovery

1. **Benchmark accuracy** on domain-specific test sets (contracts, news, social media)
2. **Performance profiling** with realistic workloads and document sizes
3. **Custom entity training** evaluation (effort vs accuracy improvement)
4. **Entity linking** strategies for cross-language normalization
5. **Error analysis** on common failure modes (rare names, abbreviations, ambiguous entities)
6. **Production deployment** patterns (containerization, scaling, monitoring)
7. **Cost modeling** for various volume scenarios (1K, 100K, 1M, 10M entities/month)
8. **Integration testing** with downstream systems (databases, analytics, visualization)

---

## References and Resources

### Open-Source Libraries
- **HanLP**: https://github.com/hankcs/HanLP
- **LTP**: https://github.com/HIT-SCIR/ltp
- **Stanza**: https://stanfordnlp.github.io/stanza/
- **spaCy**: https://spacy.io/models/zh

### Cloud APIs
- **Google Cloud**: https://cloud.google.com/natural-language
- **AWS Comprehend**: https://aws.amazon.com/comprehend/
- **Azure Text Analytics**: https://azure.microsoft.com/en-us/services/cognitive-services/text-analytics/

### Benchmarks and Papers
- **MSRA NER Dataset**: Chinese NER benchmark (Simplified Chinese news)
- **OntoNotes 4.0**: Multi-language NER benchmark including Chinese
- **People's Daily Corpus**: Chinese NER training data

### Conversion Tools
- **OpenCC**: Traditional/Simplified Chinese conversion (https://github.com/BYVoid/OpenCC)
