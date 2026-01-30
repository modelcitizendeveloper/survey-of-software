# S4: Ecosystem and Commercial Options - Chinese Dependency Parsing

## Commercial Cloud APIs

### Google Cloud Natural Language API

Supports Chinese (Simplified and Traditional) among 11 languages. Provides:
- Syntax analysis with token and sentence extraction
- Parts of speech (PoS) identification
- Dependency parse trees for each sentence

**Pricing**: Free tier available, then pay-per-request after threshold.

Sources:
- [NLP With Google Cloud Natural Language API](https://www.toptal.com/machine-learning/google-nlp-tutorial)
- [How to use NLP in GCP](https://medium.com/codex/how-to-use-nlp-in-gcp-ad6c0a0c4b2a)

### NLP Cloud

Part-of-speech tagging and dependency parsing API based on spaCy and GiNZA. Supports 15 different languages including Chinese.

**Pricing**: Free testing available, then usage-based pricing.

Source:
- [Part-Of-Speech (POS) Tagging and Dependency Parsing API](https://nlpcloud.com/nlp-part-of-speech-pos-tagging-api.html)

### LTP-Cloud

Developed by Research Center for Social Computing and Information Retrieval at Harbin Institute of Technology. Cloud-based analysis infrastructure providing:
- Chinese word segmentation
- POS tagging
- Dependency parsing
- Named entity recognition
- Semantic role labeling

Specifically designed for Chinese with rich, scalable, and accurate NLP services.

Sources:
- [LTP-Cloud](https://www.ltp-cloud.com/intro_en)

## Open-Source Self-Hosted Options

### HanLP (Recommended for Chinese)

**Pros:**
- Apache 2.0 license (free commercial use)
- Specialized for Chinese (including Ancient Chinese)
- Active development
- Python and Java APIs
- Pre-trained models available
- 10 joint tasks including dependency parsing

**Cons:**
- Requires local infrastructure
- GPU recommended for large-scale use
- Must manage model updates

**Cost Structure:**
- Software: Free (Apache 2.0)
- Infrastructure: Depends on volume (CPU/GPU compute)
- Maintenance: Developer time for updates

Source:
- [HanLP GitHub](https://github.com/hankcs/HanLP/tree/master)

### Stanford CoreNLP

**Pros:**
- Well-documented
- Strong research foundation
- Chinese Treebank-based parser included
- Java ecosystem integration

**Cons:**
- Primarily Java (less Python-friendly)
- Slower than modern neural approaches
- More complex setup

**Cost Structure:**
- Software: Free (GPL)
- Infrastructure: CPU-based, moderate requirements
- GPL licensing may require legal review for commercial use

Source:
- [CoreNLP GitHub](https://github.com/stanfordnlp/CoreNLP)

### spaCy with Chinese Models

**Pros:**
- Fast and accurate
- Python-native
- Industrial-strength
- Good documentation

**Cons:**
- Chinese models less mature than English
- May need custom training for domain-specific use

**Cost Structure:**
- Software: Free (MIT license)
- Infrastructure: CPU/GPU depending on model
- Training custom models: Data annotation cost

Sources:
- [Chinese spaCy Models](https://spacy.io/models/zh)
- [Chinese NLP with spaCy](https://alvinntnu.github.io/python-notes/nlp/nlp-spacy-zh.html)

## Decision Framework

### Choose Cloud API When:
- Processing volume is unpredictable
- No ML/NLP expertise in-house
- Need instant scaling
- Want to avoid infrastructure management
- Prototyping or low-volume use

### Choose Self-Hosted When:
- High processing volume (cloud costs exceed self-hosting)
- Data privacy/sovereignty requirements
- Need customization or fine-tuning
- Have ML/NLP team capacity
- Long-term production use at scale

## Cost Comparison Example

**Scenario**: Processing 1 million Chinese sentences/month

**Cloud (Google NLP API):**
- ~$1-2 per 1000 syntax requests
- Monthly cost: $1,000-2,000
- Zero infrastructure cost
- No maintenance burden

**Self-Hosted (HanLP on cloud VM):**
- VM with GPU: ~$300-500/month
- Developer time: ~8-16 hours/month setup/maintenance
- Cost per sentence: negligible after setup
- Monthly cost: $300-500 + developer time

**Break-even**: Around 500K-1M sentences/month, self-hosted becomes cheaper.

## Integration Patterns

### Microservice Architecture
- Deploy parser as REST API service
- Use containers (Docker) for deployment
- Scale horizontally for load balancing
- Cache common parses

### Batch Processing
- Queue-based processing for non-real-time needs
- Process overnight or during low-traffic periods
- Store results in database for retrieval
- Use distributed processing (Spark, etc.) for very large scale

### Hybrid Approach
- Cloud API for prototyping and bursts
- Self-hosted for baseline traffic
- Failover between them
- Cost optimization through intelligent routing

## Ecosystem Tools

### Visualization
- displaCy (spaCy): Interactive dependency visualizations
- Stanford Parser tools: Tree visualization
- HanLP web demos: Online testing and visualization

### Model Training
- Universal Dependencies treebanks: Training data
- DoccanoL Annotation tool for custom treebanks
- Prodigy: Commercial annotation tool with active learning

### Quality Assurance
- CoNLL evaluation scripts: Standard metrics (UAS, LAS)
- Cross-validation frameworks
- A/B testing infrastructure for parser comparison
