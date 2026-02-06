# Use Case: NLP Pipeline & Text Processing

## Goal

Process Chinese text for downstream NLP tasks: sentiment analysis, machine translation, information extraction, question answering, etc.

## User Stories

1. **Machine translation preprocessing:**
   - Input: Raw Chinese text (no spaces)
   - System: Segment into words, tag POS
   - Output: Structured tokens for MT system

2. **Sentiment analysis:**
   - Input: Product reviews in Chinese
   - System: Tokenize, identify entities, extract features
   - Output: Sentiment scores per aspect

3. **Named entity recognition:**
   - Input: News articles
   - System: Segment text, identify person/org/location names
   - Output: Annotated entities

4. **Chatbot processing:**
   - Input: User query in Chinese
   - System: Parse intent, extract entities
   - Output: Structured query for dialog system

## Required Capabilities

### Word-Level (Primary)
- ✅ Word segmentation (critical for Chinese)
- ✅ POS tagging (grammatical analysis)
- ✅ NER (entity extraction)
- ✅ Dependency parsing (sentence structure)
- Optional: Semantic role labeling

### Character-Level (Secondary)
- Optional: Character decomposition for OOV handling
- Optional: Radical features for ML models

## Library Fit Analysis

### HanLP
**Excellent fit (9/10):**
- ✅ Complete NLP pipeline
- ✅ Python 3 support
- ✅ pip installable
- ✅ RESTful API option
- ✅ Multilingual (130 languages)
- ✅ Joint task training
- ✅ Production-ready

**Pipeline:**
```python
import hanlp

HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)

result = HanLP("我爱学习汉字")
# {
#   'tok': ['我', '爱', '学习', '汉字'],
#   'pos': ['PN', 'VV', 'VV', 'NN'],
#   'ner': [],
#   'dep': [...],
#   ...
# }
```

### Stanza
**Excellent fit (9/10):**
- ✅ Complete pipeline
- ✅ UD framework (cross-lingual consistency)
- ✅ Python 3, pip installable
- ✅ Stanford backing
- ✅ 80 languages
- ✅ Proven performance

**Pipeline:**
```python
import stanza

nlp = stanza.Pipeline('zh')
doc = nlp("我爱学习汉字")

for sentence in doc.sentences:
    for word in sentence.words:
        print(word.text, word.pos, word.deprel)
```

### LTP
**Excellent fit (9/10):**
- ✅ Chinese-specific optimization
- ✅ Complete NLP pipeline
- ✅ Python 3 (N-LTP)
- ✅ Cloud service available
- ✅ Academic backing (HIT)

**Use case:** Chinese-only applications benefit from Chinese-specific training

### Comparison

| Feature | HanLP | Stanza | LTP |
|---------|-------|--------|-----|
| **Segmentation** | ✅ | ✅ | ✅ |
| **POS Tagging** | ✅ | ✅ UD | ✅ |
| **NER** | ✅ | ✅ | ✅ |
| **Dependency** | ✅ | ✅ UD | ✅ |
| **Semantic Role** | ✅ | ⚠️ | ✅ |
| **Languages** | 130 | 80 | Chinese |
| **Framework** | MTL | UD | Multi-task |
| **Deployment** | Lib + API | Lib | Lib + Cloud |

### Character Analysis Libraries
**Poor fit (1/10):**
- cjklib, makemeahanzi: Not designed for NLP pipelines
- Use case: Supplementary features, not primary processing

## Recommended Solutions

### For General NLP: HanLP
**Rationale:**
- Broadest language support (future-proof)
- RESTful API option (microservices)
- Active development
- Comprehensive task coverage

**Architecture:**
```
Raw Text → HanLP Pipeline → Structured Data → Downstream Tasks
                                              ↓
                                         ML Models
                                         Rule Systems
                                         Search Engines
```

### For UD-Compliant Projects: Stanza
**Rationale:**
- Cross-lingual research
- UD framework consistency
- Integration with UD tools
- Academic reproducibility

### For Chinese-Only, High-Performance: LTP
**Rationale:**
- Optimized for Chinese
- Chinese-specific models
- Lower latency
- Cloud service option (scalability)

## Character Decomposition Integration

### Use Case: OOV Handling

**Problem:** Unknown words break segmentation

**Solution:** Use character features

```python
# Segment with HanLP
tokens = hanlp_segment(text)

# For OOV tokens, analyze character structure
for token in tokens:
    if is_oov(token):
        # Get character components
        components = decompose_chars(token)
        # Use components as features for classification
        features = extract_features(components)
```

**Benefit:** Character decomposition provides fallback features for ML models when encountering unknown words.

### Implementation

1. Primary: HanLP for word segmentation
2. Secondary: makemeahanzi/CJKVI-IDS for character features
3. Use character features in ML pipeline:
   - Word embeddings + character embeddings
   - Radical embeddings
   - Structural features from IDS

## Production Pipeline Example

```python
import hanlp
from character_analyzer import decompose  # Custom

# Initialize
nlp = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)

def process_document(text):
    # NLP pipeline
    result = nlp(text)

    # Enhance with character features
    for token in result['tok']:
        if is_rare(token):
            # Decompose characters in token
            char_features = [decompose(c) for c in token]
            result['char_features'] = char_features

    return result
```

## Performance Considerations

### Throughput
- HanLP: ~100-1000 chars/sec (depends on model)
- Stanza: Similar performance
- LTP: Optimized for speed in Chinese

### Optimization
- Batch processing (process multiple docs together)
- Model selection (smaller models for speed vs. accuracy)
- Caching (segment common phrases once)
- GPU acceleration (for large-scale processing)

## Deployment Options

### Option A: Local Library
```bash
pip install hanlp
```
Pro: No network, full control
Con: Model size (~GB), memory usage

### Option B: RESTful API (HanLP)
```bash
# HanLP provides hosted API
curl -X POST https://hanlp.hankcs.com/api/...
```
Pro: No local setup, scalability
Con: Network dependency, cost

### Option C: Self-Hosted Service
```python
# FastAPI + HanLP
from fastapi import FastAPI
app = FastAPI()

@app.post("/segment")
def segment(text: str):
    return nlp(text)
```
Pro: Control + scalability
Con: Infrastructure management

---

**Verdict:** HanLP, Stanza, or LTP are all excellent for NLP pipelines. Choose based on: multilingual needs (HanLP), UD framework (Stanza), or Chinese-only optimization (LTP). Character decomposition is supplementary, not primary.
