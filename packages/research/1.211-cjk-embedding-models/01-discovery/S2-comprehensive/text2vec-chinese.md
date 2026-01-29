# text2vec-chinese: Technical Deep Dive

## Library Overview

**text2vec** (shibing624/text2vec) is a practical Chinese text embedding library, not just a single model. It provides:
- Pre-trained Chinese embedding models
- Simple Python API for production use
- Text matching, semantic search, and similarity utilities
- Focus on ease of deployment over cutting-edge performance

**Key Difference from sentence-transformers**: text2vec is Chinese-centric with opinionated defaults, while sentence-transformers is language-agnostic and flexible.

## Architecture & Models

### Available Models (via text2vec)
| Model Name | Parameters | Embedding Dim | Base Architecture |
|------------|-----------|---------------|-------------------|
| text2vec-base-chinese | 102M | 768 | BERT-base |
| text2vec-base-chinese-sentence | 102M | 768 | BERT-base + CoSENT |
| text2vec-base-chinese-paraphrase | 102M | 768 | BERT-base + SimCSE |
| text2vec-base-multilingual | 278M | 768 | XLM-RoBERTa |

### Training Details
- **text2vec-base-chinese**: Fine-tuned on Chinese semantic similarity datasets (ATEC, BQ, LCQMC, PAWSX, STS-B)
- **CoSENT variant**: Uses cosine sentence embedding with negative sampling
- **SimCSE variant**: Contrastive learning with dropout as noise
- **Training Data**: ~10M Chinese sentence pairs from web, social media, Q&A platforms

### Tokenization
```python
Input: "自然语言处理技术应用"
       (Natural language processing technology application)

Tokens: ["自然", "语言", "处理", "技术", "应用"]
# Word-level tokenization via jieba + BERT tokenizer
# Vocabulary: 21,128 tokens (Chinese-optimized)
```

**Tokenization Strategy:**
- Jieba word segmentation + WordPiece
- Handles Chinese-specific features (measure words, particles)
- Better coverage of Chinese idioms and phrases

## Benchmark Performance

### Chinese Semantic Similarity (C-STS)
| Task | text2vec-base | M3E-base | multilingual-e5-base |
|------|---------------|----------|----------------------|
| ATEC | 46.8 | 48.2 | 44.7 |
| BQ | 65.7 | 67.3 | 63.1 |
| LCQMC | 75.1 | 76.4 | 75.8 |
| PAWSX.zh | 59.3 | 61.5 | 58.9 |
| STSB.zh | 81.4 | 83.1 | 82.5 |

**Positioning**: Competitive with M3E, slightly behind on most tasks. Better than general multilingual models.

### Chinese Retrieval (Subset of C-MTEB)
| Task | text2vec-base | M3E-base |
|------|---------------|----------|
| T2Retrieval | 63.2 | 66.1 |
| DuRetrieval | 52.4 | 54.8 |
| MedicalRetrieval | 48.7 | 51.3 |

**Performance Summary**: 2-3 points behind M3E on retrieval tasks. Sufficient for most production use cases.

## Inference Performance

### Latency (sentences/second)
**CPU (Intel i9-12900K, single thread):**
- text2vec-base-chinese: ~220 sent/sec
- text2vec-base-chinese-sentence: ~210 sent/sec

**GPU (NVIDIA V100, batch=1):**
- ~850 sent/sec (FP32)
- ~1,400 sent/sec (FP16)

**GPU (NVIDIA A100, batch=32):**
- ~6,200 sent/sec (FP16)

**Comparison**: Similar to M3E-base and multilingual-e5-base (same model size).

### Memory Footprint
| Model | FP32 | FP16 | INT8 |
|-------|------|------|------|
| text2vec-base-chinese | 408 MB | 204 MB | 102 MB |

**Note**: Slightly smaller than M3E due to vocabulary differences.

## Library API & Usage

### Basic Usage
```python
from text2vec import SentenceModel

# Load pre-trained model
model = SentenceModel('shibing624/text2vec-base-chinese')

# Encode Chinese sentences
sentences = ['如何更换花呗绑定银行卡', '花呗更改绑定银行卡']
embeddings = model.encode(sentences)

# Compute similarity
similarity = model.similarity(sentences[0], sentences[1])
# Returns: 0.89 (cosine similarity)
```

### Semantic Search
```python
from text2vec import SentenceModel, cos_sim
import numpy as np

model = SentenceModel('shibing624/text2vec-base-chinese')

# Corpus
corpus = [
    '如何更换花呗绑定银行卡',
    '花呗如何还款',
    '支付宝怎么转账'
]
corpus_embeddings = model.encode(corpus)

# Query
query = '怎么修改花呗绑定的银行卡'
query_embedding = model.encode(query)

# Find most similar
scores = cos_sim(query_embedding, corpus_embeddings)[0]
top_idx = np.argmax(scores)
print(f"Most similar: {corpus[top_idx]} (score: {scores[top_idx]:.2f})")
# Output: "如何更换花呗绑定银行卡" (score: 0.87)
```

### Text Matching (Pairwise)
```python
from text2vec import Similarity

# Higher-level API for text matching
sim = Similarity('shibing624/text2vec-base-chinese')

# Pairwise similarity
pairs = [
    ('用户登录失败', '无法登录账户'),
    ('用户登录失败', '天气预报查询')
]

scores = sim.get_scores(pairs)
# Returns: [0.82, 0.15]
```

### Custom Corpus Search
```python
from text2vec import Similarity

# Initialize with corpus
sim = Similarity(
    model_name='shibing624/text2vec-base-chinese',
    corpus=['文档1', '文档2', '文档3', ...]  # Can be millions of docs
)

# Search
results = sim.most_similar(queries=['用户查询'], topn=5)
# Returns: [(doc_id, score), ...]
```

## Fine-Tuning Capabilities

### Training API
```python
from text2vec import SentenceModel
from datasets import load_dataset

# Load base model
model = SentenceModel('shibing624/text2vec-base-chinese')

# Prepare training data (Chinese sentence pairs)
train_data = load_dataset('shibing624/nli-zh', 'STS-B')

# Fine-tune with CoSENT loss
model.train(
    train_file='chinese_pairs.txt',  # Format: sent1\tsent2\tscore
    output_dir='./finetuned-model',
    num_epochs=3,
    batch_size=32,
    max_seq_length=128
)
```

### Domain Adaptation Results
| Domain | Base Model | After Fine-Tuning (50K pairs) |
|--------|------------|-------------------------------|
| E-commerce (product search) | 68.3 | 81.7 (+13.4) |
| Financial services (Q&A) | 71.2 | 82.9 (+11.7) |
| Healthcare (symptom matching) | 65.8 | 77.4 (+11.6) |

**Key Strength**: Simple training API makes domain adaptation accessible.

### Fine-Tuning Requirements
- **Minimum Data**: 5K Chinese sentence pairs
- **Recommended Data**: 30K+ pairs for production quality
- **Compute**: 1x V100, ~3 hours for 30K pairs
- **Expertise**: Low (well-documented in Chinese)

## Production Deployment

### Installation
```bash
pip install text2vec
# Includes model download, jieba, torch dependencies
```

**Package Size**: ~800 MB (includes PyTorch and pre-trained models)

### ONNX Conversion
```python
from text2vec import SentenceModel
import torch.onnx

model = SentenceModel('shibing624/text2vec-base-chinese')

# Export to ONNX
dummy_input = torch.randint(0, 21128, (1, 128))  # vocab_size, max_seq_len
torch.onnx.export(
    model.model,
    dummy_input,
    'text2vec-chinese.onnx',
    opset_version=12
)
```

**ONNX Performance**: 1.3x speedup on CPU inference.

### Quantization
```python
import torch

model = SentenceModel('shibing624/text2vec-base-chinese')

# Dynamic INT8 quantization
quantized_model = torch.quantization.quantize_dynamic(
    model.model,
    {torch.nn.Linear},
    dtype=torch.qint8
)

# 2x speedup, ~1% accuracy drop
```

### Serving with FastAPI
```python
from fastapi import FastAPI
from text2vec import SentenceModel
from pydantic import BaseModel

app = FastAPI()
model = SentenceModel('shibing624/text2vec-base-chinese')

class EmbedRequest(BaseModel):
    texts: list[str]

@app.post("/embed")
def embed(request: EmbedRequest):
    embeddings = model.encode(request.texts)
    return {"embeddings": embeddings.tolist()}

class SimilarityRequest(BaseModel):
    text1: str
    text2: str

@app.post("/similarity")
def similarity(request: SimilarityRequest):
    score = model.similarity(request.text1, request.text2)
    return {"similarity": float(score)}

# Run: uvicorn app:app --host 0.0.0.0 --port 8000
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

# Install dependencies
RUN pip install text2vec fastapi uvicorn

# Copy application
COPY app.py /app/app.py
WORKDIR /app

# Pre-download model (cached in image)
RUN python -c "from text2vec import SentenceModel; SentenceModel('shibing624/text2vec-base-chinese')"

# Serve
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Vector Database Integration

### Milvus (Popular in China)
```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
from text2vec import SentenceModel

# Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# Create collection
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768)
]
schema = CollectionSchema(fields)
collection = Collection("chinese_docs", schema)

# Insert embeddings
model = SentenceModel('shibing624/text2vec-base-chinese')
texts = ["文档1", "文档2", "文档3"]
embeddings = model.encode(texts)
collection.insert([list(range(len(texts))), embeddings.tolist()])

# Search
query_embedding = model.encode(["查询"])
results = collection.search(query_embedding, "embedding", limit=5)
```

### ElasticSearch (Chinese E-commerce Common)
```python
from elasticsearch import Elasticsearch
from text2vec import SentenceModel

es = Elasticsearch(['localhost:9200'])
model = SentenceModel('shibing624/text2vec-base-chinese')

# Index documents with embeddings
doc = {
    'text': '苹果手机最新款',
    'embedding': model.encode('苹果手机最新款').tolist()
}
es.index(index='products', body=doc)

# Search by vector
query_embedding = model.encode('买手机')
response = es.search(
    index='products',
    body={
        'query': {
            'script_score': {
                'query': {'match_all': {}},
                'script': {
                    'source': 'cosineSimilarity(params.query_vector, "embedding") + 1.0',
                    'params': {'query_vector': query_embedding.tolist()}
                }
            }
        }
    }
)
```

## Chinese NLP Ecosystem Position

### Community Adoption
- **GitHub Stars**: 5.2K (shibing624/text2vec)
- **Pypi Downloads**: 50K+/month
- **Primary Users**: Chinese companies, Chinese NLP researchers
- **Documentation**: Primarily in Chinese (limited English docs)

### Integration with Chinese Tools
- **Jieba**: Native integration for word segmentation
- **PaddleNLP**: Compatible via model hub
- **THULAC**: Alternative segmenter support
- **HanLP**: Can use text2vec embeddings

### Comparison to Chinese Alternatives
| Library | Focus | Strength | text2vec Position |
|---------|-------|----------|-------------------|
| M3E | Chinese embeddings | SOTA performance | text2vec: easier API, slightly lower perf |
| sentence-transformers | Multilingual | Ecosystem, flexibility | text2vec: Chinese-focused simplicity |
| text2vec | Chinese, ease of use | Simplicity, Chinese docs | **This library** |

## Limitations

### Known Issues
1. **Language Coverage**: Chinese only (no Japanese, Korean, or multilingual support)
2. **Performance**: 2-3 points behind M3E on benchmarks
3. **Model Selection**: Limited to a few pre-trained models (vs 3,000+ in sentence-transformers)
4. **International Support**: Documentation primarily in Chinese
5. **Innovation Pace**: Slower updates compared to sentence-transformers or M3E
6. **Traditional Chinese**: Suboptimal (trained on Simplified Chinese)

### When NOT to Use text2vec
- Need for multilingual support (use sentence-transformers + multilingual models)
- Cutting-edge performance required (use M3E or multilingual-e5)
- Team primarily English-speaking (documentation barrier)
- Japanese/Korean support needed (no support)
- Need for latest models (text2vec lags behind Hugging Face releases)

### When text2vec IS Best Choice
- Chinese-only application with simplicity as priority
- Team comfortable with Chinese documentation
- Need for turnkey solution (minimal configuration)
- Integration with Chinese NLP tools (Jieba, PaddleNLP)
- Internal deployment without external dependencies on model hubs

## Ecosystem & Support

### Documentation
- **Chinese**: Comprehensive (README, tutorials, examples)
- **English**: Basic (README only)
- **Tutorials**: Primarily on Chinese platforms (Zhihu, Bilibili, CSDN)

### Community Support
- **GitHub Issues**: Active (author responds within days)
- **Chinese Forums**: Strong presence on Zhihu, CSDN
- **WeChat Groups**: Developer community available
- **Stack Overflow**: Limited (primarily Chinese Stack Overflow clone)

### Maintenance
- **Update Frequency**: Monthly bug fixes, quarterly new features
- **Latest Release**: Jan 2024 (v1.2.0)
- **Stability**: Mature library (4+ years development)

## Comparison: text2vec vs Alternatives

### vs M3E
| Aspect | text2vec | M3E |
|--------|----------|-----|
| Performance | 63.2 (T2Retrieval) | 66.1 |
| API Simplicity | Very simple (opinionated) | Requires sentence-transformers |
| Documentation | Chinese-focused | Chinese + English |
| Fine-tuning | Built-in API | Via sentence-transformers |
| Model Selection | Limited (4-5 models) | Multiple variants |

**Verdict**: M3E for performance, text2vec for simplicity.

### vs sentence-transformers (with Chinese models)
| Aspect | text2vec | sentence-transformers |
|--------|----------|----------------------|
| API Learning Curve | Low (Chinese-focused) | Medium (general-purpose) |
| Model Selection | 4-5 Chinese models | 3,000+ (including Chinese) |
| Ecosystem | Chinese NLP tools | Global ML ecosystem |
| Flexibility | Limited (opinionated) | Very high |
| Documentation | Chinese | English |

**Verdict**: sentence-transformers for flexibility, text2vec for Chinese-specific simplicity.

## Recommendation

**Best For:**
- Chinese-only applications where simplicity matters more than cutting-edge performance
- Teams with Chinese-speaking developers
- Quick prototyping of Chinese semantic search
- Integration with existing Chinese NLP pipelines (Jieba, etc.)
- Internal deployments without dependency on external model hubs

**Not Ideal For:**
- Multilingual applications (no support for J/K or other languages)
- Teams requiring English documentation
- Projects needing SOTA performance (M3E is better)
- Applications with uncertain language requirements (sentence-transformers more flexible)

**Strategic Fit:**
text2vec occupies a niche: Chinese-only applications where ease of use trumps maximum performance. It's the "batteries-included" option for Chinese NLP. However, for most new projects, **sentence-transformers + M3E or multilingual-e5** offers better future-proofing (easy to switch models, multilingual option, broader ecosystem). Choose text2vec if your team strongly values Chinese documentation and simplicity over flexibility and cutting-edge performance.

**Upgrade Path:**
text2vec models are available on Hugging Face and can be used via sentence-transformers. If you start with text2vec and later need more flexibility, you can migrate to sentence-transformers while keeping the same underlying model.
