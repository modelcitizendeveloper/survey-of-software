# S2 Comprehensive Recommendations

**Experiment**: 1.033.2 Chinese Word Segmentation Libraries
**Pass**: S2 - Comprehensive Discovery
**Date**: 2026-01-28

## Executive Summary

After deep technical analysis of architecture, performance, deployment, and integration patterns, this document provides architecture-informed recommendations based on technical requirements, infrastructure constraints, and deployment patterns.

## Architecture-Based Decision Framework

### 1. Algorithmic Requirements

#### If You Need Context-Aware Segmentation
**Recommendation**: CKIP or LTP

**Why**:
- CKIP: BiLSTM captures full sentence context bidirectionally
- LTP: BERT transformer with full document context
- Jieba: Limited to local dictionary + HMM (no global context)
- PKUSeg: CRF with ±2 character window (limited context)

**Use case**: Ambiguous segmentation requiring semantic understanding
```
Example: "我/在/北京/天安门/广场/拍照" (context determines boundaries)
```

#### If You Need Feature-Rich Explicit Models
**Recommendation**: PKUSeg

**Why**:
- CRF with hand-crafted features (interpretable)
- Explicit feature weights (debuggable)
- Fast training (hours vs. days)

**Trade-off**: Lower accuracy ceiling than neural models (96% vs. 98%)

#### If You Need End-to-End Neural Architecture
**Recommendation**: LTP or CKIP

**Why**:
- LTP: BERT-based with multi-task knowledge distillation
- CKIP: BiLSTM with attention mechanisms
- Learn representations directly from data
- State-of-the-art accuracy (97-99%)

**Trade-off**: Slower, larger models, GPU recommended

### 2. Performance Requirements

#### High-Throughput CPU-Only Deployment
**Recommendation**: LTP Legacy or Jieba

**Performance comparison**:
```
LTP Legacy: 21,581 sent/s (16 threads) - 500x faster than LTP Small
Jieba: 400 KB/s = ~2,000 sent/s (estimated) - 50x faster than LTP Small
PKUSeg: ~100 char/s (single-thread) - Not suitable
CKIP: ~5 sent/s (CPU) - Not suitable
```

**Use case**: Batch processing millions of documents overnight

**Deployment**:
```bash
# LTP Legacy (highest throughput)
from ltp import LTP
ltp = LTP("LTP/legacy")

# Jieba (balanced throughput + accuracy)
import jieba
jieba.enable_parallel(16)
```

#### Low-Latency Real-Time API
**Recommendation**: Jieba or LTP Tiny

**Latency comparison** (30 char sentence):
```
Jieba: <10ms (warm start)
LTP Tiny: 100-150ms (CPU), 10-15ms (GPU)
PKUSeg: 300-500ms (CPU)
CKIP: 200-300ms (CPU), 20-30ms (GPU)
```

**Use case**: Real-time chatbot, live transcription

**Deployment**:
```python
# Jieba (fastest)
import jieba
jieba.initialize()  # Pre-load dictionary
result = list(jieba.cut(text))  # <10ms

# LTP Tiny (GPU)
from ltp import LTP
ltp = LTP("LTP/tiny")
ltp.to("cuda")
result = ltp.pipeline([text], tasks=["cws"])  # 10-15ms
```

#### GPU-Accelerated Accuracy-Critical
**Recommendation**: LTP Base or CKIP

**GPU throughput comparison**:
```
LTP Base: 100-150 sent/s (98.7% accuracy)
LTP Small: 150-200 sent/s (98.4% accuracy)
CKIP: 50-100 sent/s (97.33% accuracy on Traditional Chinese)
```

**Use case**: Medical records, legal contracts (accuracy paramount)

**Deployment**:
```python
# LTP Base (highest multi-task accuracy)
from ltp import LTP
ltp = LTP("LTP/base")
ltp.to("cuda")
output = ltp.pipeline(sentences, tasks=["cws", "pos", "ner"])

# CKIP (highest Traditional Chinese accuracy)
from ckiptagger import WS, POS, NER
ws = WS("./data", device=0)  # GPU 0
words = ws(sentences)
```

### 3. Memory Constraints

#### Embedded/Mobile Deployment (<100 MB)
**Recommendation**: Jieba

**Memory footprint**:
```
Jieba: 55 MB runtime, 20 MB disk
LTP Tiny: 1 GB runtime, 100 MB disk
PKUSeg: 120 MB runtime, 70 MB disk
CKIP: 4 GB runtime, 2 GB disk
```

**Use case**: Mobile app, edge device, Raspberry Pi

#### Cloud Serverless (<256 MB)
**Recommendation**: Jieba or PKUSeg

**Cold start time**:
```
Jieba: ~200ms (lazy dictionary loading)
PKUSeg: ~500ms (model loading)
LTP Tiny: 5-10s (PyTorch + model)
CKIP: 10-15s (TensorFlow + 2GB model)
```

**Use case**: AWS Lambda, Google Cloud Functions

**Deployment**:
```dockerfile
# Jieba (smallest)
FROM python:3.10-slim
RUN pip install jieba
# Image: ~120 MB

# PKUSeg (medium)
FROM python:3.10-slim
RUN pip install pkuseg
# Image: ~300 MB
```

#### GPU-Enabled Container (<4 GB)
**Recommendation**: LTP Small or LTP Tiny

**Docker image size**:
```
LTP Tiny: ~2.5 GB (CUDA + PyTorch + model)
LTP Small: ~3 GB (CUDA + PyTorch + model)
LTP Base: ~3.5 GB (CUDA + PyTorch + model)
CKIP: ~5 GB (CUDA + TensorFlow + model)
```

**Use case**: Kubernetes GPU pod

### 4. Accuracy Requirements

#### Maximum Accuracy (Traditional Chinese)
**Recommendation**: CKIP

**Benchmark**: 97.33% F1 on ASBC 4.0
- 7.5 points higher than Jieba
- Optimized for Taiwan/HK text

**Use case**: Taiwan government documents, Traditional Chinese academic corpus

#### Maximum Accuracy (Simplified Chinese, Domain-Specific)
**Recommendation**: PKUSeg

**Benchmarks**:
```
MSRA (news): 96.88% F1
Weibo (social): 94.21% F1
Medical: 95.20% F1
```

**Use case**: Medical records, legal contracts, social media analytics

#### Maximum Accuracy (Multi-Task)
**Recommendation**: LTP Base

**Benchmarks**:
```
Word Segmentation: 98.7%
POS Tagging: 98.5%
NER: 95.4%
Dependency Parsing: 89.5%
Semantic Role Labeling: 80.6%
```

**Use case**: Research NLP pipeline, semantic analysis

#### Balanced Accuracy/Speed
**Recommendation**: LTP Small or PKUSeg

**Comparison**:
```
LTP Small: 98.4% accuracy, 43 sent/s (CPU)
PKUSeg: 96.88% accuracy, ~100 char/s (CPU)
Jieba: 81-89% accuracy, 2000 sent/s (estimated)
```

**Use case**: Production system with moderate throughput

## Deployment Pattern Recommendations

### 1. Kubernetes Microservices

#### CPU-Only Pods (Cost-Optimized)
**Recommendation**: Jieba or LTP Legacy

**Deployment YAML**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: segment-service
spec:
  replicas: 10  # Horizontal scaling
  template:
    spec:
      containers:
      - name: jieba
        image: jieba-service:latest
        resources:
          requests:
            cpu: 500m
            memory: 256Mi
          limits:
            cpu: 1000m
            memory: 512Mi
```

**Throughput**: ~500 req/s per pod (Jieba), ~10K req/s cluster-wide (20 pods)

#### GPU Pods (Accuracy-Optimized)
**Recommendation**: LTP Small or CKIP

**Deployment YAML**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ltp-service
spec:
  replicas: 3  # GPU-bound
  template:
    spec:
      containers:
      - name: ltp
        image: ltp-service:latest
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: 4Gi
```

**Throughput**: ~150 req/s per pod, ~450 req/s cluster-wide (3 GPUs)

### 2. Serverless Functions

#### AWS Lambda / Google Cloud Functions
**Recommendation**: Jieba

**Constraints**:
- Memory: 256 MB minimum (Jieba: 55 MB runtime)
- Cold start: <1s (Jieba: ~200ms)
- Package size: <250 MB (Jieba: ~20 MB)

**Configuration**:
```python
# handler.py
import jieba
jieba.initialize()  # Pre-load dictionary

def lambda_handler(event, context):
    text = event['text']
    result = list(jieba.cut(text))
    return {'segments': result}
```

**Alternative**: PKUSeg (500ms cold start, acceptable for non-latency-critical)

### 3. Docker Containers

#### Minimal Image (Alpine Linux)
**Recommendation**: Jieba

**Dockerfile**:
```dockerfile
FROM python:3.10-alpine
RUN pip install jieba
COPY app.py /app/
CMD ["python", "/app/app.py"]
```

**Image size**: ~80 MB (Python Alpine + Jieba)

#### GPU-Accelerated Image (CUDA)
**Recommendation**: LTP or CKIP

**Dockerfile** (LTP):
```dockerfile
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y python3-pip
RUN pip install ltp torch
RUN python3 -c "from ltp import LTP; LTP('LTP/small')"  # Pre-download
COPY app.py /app/
CMD ["python3", "/app/app.py"]
```

**Image size**: ~3 GB (CUDA + PyTorch + LTP Small)

### 4. Batch Processing Pipelines

#### Offline ETL (Airflow, Spark)
**Recommendation**: LTP Legacy or PKUSeg

**Use case**: Nightly processing of archived documents

**Apache Spark example** (LTP Legacy):
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from ltp import LTP

ltp = LTP("LTP/legacy")

@udf
def segment_udf(text):
    output = ltp.pipeline([text], tasks=["cws"])
    return output.cws[0]

df = spark.read.parquet("documents.parquet")
df_segmented = df.withColumn("segments", segment_udf(df.text))
df_segmented.write.parquet("segmented.parquet")
```

**Throughput**: 21,581 sent/s (single worker), 100K+ sent/s (cluster)

#### Real-Time Streaming (Kafka, Flink)
**Recommendation**: Jieba

**Use case**: Real-time social media monitoring

**Flink example**:
```python
from pyflink.datastream import StreamExecutionEnvironment
import jieba

env = StreamExecutionEnvironment.get_execution_environment()

def segment_map(text):
    return list(jieba.cut(text))

stream = env.from_collection(["文本1", "文本2"])
segmented = stream.map(segment_map)
segmented.print()
env.execute()
```

**Latency**: <10ms per message

## Integration Pattern Recommendations

### 1. Multi-Tool Hybrid Approach

#### Fast Pre-Filter + Accurate Refinement
**Recommendation**: Jieba → PKUSeg

**Pattern**:
```python
import jieba
import pkuseg

jieba_seg = jieba.cut
pkuseg_seg = pkuseg.pkuseg(model_name='medicine')

def hybrid_segment(text, threshold=50):
    # Short texts: Use Jieba (fast)
    if len(text) < threshold:
        return list(jieba_seg(text))
    # Long texts: Use PKUSeg (accurate)
    else:
        return pkuseg_seg.cut(text)
```

**Benefit**: 80% of requests (short texts) processed quickly, 20% (long texts) accurately

#### Ensemble Voting
**Recommendation**: PKUSeg + LTP + CKIP

**Pattern**:
```python
from collections import Counter

def ensemble_segment(text, models):
    results = []
    for model in models:
        results.append(tuple(model.segment(text)))

    # Vote: Use most common segmentation
    return Counter(results).most_common(1)[0][0]

# Usage
result = ensemble_segment(text, [pkuseg_model, ltp_model, ckip_model])
```

**Benefit**: 1-2% accuracy improvement (diminishing returns, expensive)

### 2. Dictionary-Augmented Neural Models

#### Custom Dictionary + Neural Segmentation
**Recommendation**: Jieba (dictionary) + LTP (validation)

**Pattern**:
```python
import jieba
from ltp import LTP

# Stage 1: Jieba with custom dictionary
jieba.load_userdict("medical_terms.txt")
jieba_result = list(jieba.cut(text))

# Stage 2: LTP validation (check for errors)
ltp = LTP("LTP/small")
ltp_result = ltp.pipeline([text], tasks=["cws"]).cws[0]

# Stage 3: Merge (prefer LTP for unknowns, Jieba for custom dict)
def merge(jieba_seg, ltp_seg, custom_dict):
    # Custom merging logic
    pass
```

**Use case**: Domain with large custom dictionary + unknown term handling

### 3. Language Detection + Routing

#### Simplified vs. Traditional Chinese
**Recommendation**: Language detection → PKUSeg (Simplified) or CKIP (Traditional)

**Pattern**:
```python
import jieba
from ckiptagger import WS
import pkuseg

def detect_script(text):
    # Heuristic: Check for Traditional-only characters
    traditional_chars = set("繁體字範例")
    return "traditional" if any(c in traditional_chars for c in text) else "simplified"

def segment_by_script(text):
    script = detect_script(text)
    if script == "traditional":
        ws = WS("./data")
        return ws([text])[0]
    else:
        seg = pkuseg.pkuseg()
        return seg.cut(text)
```

**Benefit**: Use best tool for each script

## Domain-Specific Recommendations

### Medical/Healthcare
**Primary**: PKUSeg (medicine model)
**Secondary**: LTP (fine-tuned on medical corpus)

**Rationale**:
- PKUSeg pre-trained on medical corpus (95.20% F1)
- Handles medical terminology (糖尿病, 高血压, 冠心病)
- MIT license (suitable for commercial health tech)

**Deployment**:
```python
import pkuseg
seg = pkuseg.pkuseg(model_name='medicine')
result = seg.cut('患者被诊断为2型糖尿病并发肾病')
# ['患者', '被', '诊断', '为', '2型糖尿病', '并发', '肾病']
```

### Legal/Contracts
**Primary**: PKUSeg (custom trained)
**Secondary**: LTP Base (dependency parsing for clause analysis)

**Rationale**:
- Legal terminology requires domain adaptation
- PKUSeg supports custom training (legal corpus)
- LTP dependency parsing useful for contract structure analysis

### E-Commerce/Product Search
**Primary**: Jieba (search engine mode)
**Secondary**: PKUSeg (web model)

**Rationale**:
- Jieba search engine mode: Fine-grained segmentation for indexing
- Fast enough for real-time search (400 KB/s)
- Easy custom dictionary (product names, brands)

**Deployment**:
```python
import jieba
result = jieba.cut_for_search('小米手机充电器')
# ['小米', '手机', '小米手机', '充电', '充电器', '手机充电器']
```

### Social Media Analytics (Weibo, WeChat)
**Primary**: PKUSeg (web model)
**Secondary**: Jieba

**Rationale**:
- PKUSeg pre-trained on Weibo (94.21% F1)
- Handles informal text, slang, emoji
- Offline batch processing acceptable for analytics

### News/Media Processing
**Primary**: PKUSeg (news model)
**Secondary**: LTP Small

**Rationale**:
- PKUSeg pre-trained on MSRA news corpus (96.88% F1)
- Highest accuracy for standard written Chinese
- Batch processing typical for news archives

### Traditional Chinese (Taiwan/HK)
**Primary**: CKIP
**Secondary**: LTP

**Rationale**:
- CKIP optimized for Traditional Chinese (97.33% F1)
- Academia Sinica backing (Taiwan institution)
- Multi-task support (WS + POS + NER)

### Research/Academic NLP
**Primary**: LTP Base
**Secondary**: CKIP

**Rationale**:
- LTP: Most comprehensive (6 tasks including SRL, dependency parsing)
- Published benchmarks, reproducible
- Free for academic use

## Anti-Recommendations

### Do NOT Use Jieba If:
- ❌ Accuracy is paramount (medical, legal contracts)
- ❌ Domain-specific terminology critical (use PKUSeg instead)
- ❌ Multi-task NLP pipeline needed (use LTP instead)

**Example failure case**:
```
Text: "患者被诊断为2型糖尿病"
Jieba: ['患者', '被', '诊', '断', '为', '2', '型', '糖', '尿', '病']  # Wrong
PKUSeg: ['患者', '被', '诊断', '为', '2型糖尿病']  # Correct
```

### Do NOT Use CKIP If:
- ❌ Simplified Chinese primary focus (use PKUSeg or LTP)
- ❌ Commercial proprietary software (GPL v3 copyleft)
- ❌ Speed critical, no GPU available (5 sent/s CPU too slow)
- ❌ Serverless deployment (<256 MB memory limit)

### Do NOT Use PKUSeg If:
- ❌ Real-time/low-latency required (<100ms)
- ❌ Traditional Chinese primary focus (use CKIP)
- ❌ No domain match (general-purpose → use Jieba or LTP)

### Do NOT Use LTP If:
- ❌ Single-task segmentation only (PKUSeg more accurate for WS alone)
- ❌ Commercial use without licensing budget (contact HIT)
- ❌ Serverless deployment (5-15s cold start too slow)
- ❌ Extremely memory-constrained (<256 MB)

## Migration Paths

### From Jieba to Higher Accuracy

**Scenario**: MVP used Jieba, now need better accuracy

**Migration path**:
1. **Benchmark current performance**: Measure Jieba F1 on test set
2. **Select replacement**: PKUSeg (domain-specific) or LTP (multi-task)
3. **A/B test**: Run both models in parallel, compare results
4. **Gradual rollout**: Migrate 10% → 50% → 100% of traffic

**Code pattern**:
```python
import jieba
import pkuseg

USE_PKUSEG = os.getenv("USE_PKUSEG_PCT", 0)  # 0-100

def segment(text):
    if random.randint(0, 100) < USE_PKUSEG:
        seg = pkuseg.pkuseg()
        return seg.cut(text)
    else:
        return list(jieba.cut(text))
```

### From CPU to GPU Deployment

**Scenario**: Current CPU deployment too slow, adding GPU

**Migration path**:
1. **Benchmark current throughput**: Measure req/s on CPU
2. **Deploy GPU pod**: LTP or CKIP on GPU
3. **Load balancer routing**: CPU for <10 char texts, GPU for >10 char
4. **Monitor GPU utilization**: Scale GPU pods based on load

**Kubernetes setup**:
```yaml
# CPU service (existing)
apiVersion: v1
kind: Service
metadata:
  name: segment-cpu
spec:
  selector:
    app: jieba

# GPU service (new)
apiVersion: v1
kind: Service
metadata:
  name: segment-gpu
spec:
  selector:
    app: ltp-gpu

# Ingress routing (by text length)
# Use external logic or service mesh
```

## Future-Proofing

### Preparing for Model Evolution

**Recommendation**: Abstract segmentation behind interface

**Pattern**:
```python
from abc import ABC, abstractmethod

class Segmenter(ABC):
    @abstractmethod
    def segment(self, text: str) -> list[str]:
        pass

class JiebaSegmenter(Segmenter):
    def __init__(self):
        import jieba
        self.jieba = jieba

    def segment(self, text):
        return list(self.jieba.cut(text))

class PKUSEGSegmenter(Segmenter):
    def __init__(self, model='news'):
        import pkuseg
        self.seg = pkuseg.pkuseg(model_name=model)

    def segment(self, text):
        return self.seg.cut(text)

# Application code
segmenter = PKUSEGSegmenter()  # Easy to swap
result = segmenter.segment(text)
```

**Benefit**: Swap implementations without changing application code

### Monitoring and Metrics

**Key metrics to track**:
```python
import time
from prometheus_client import Counter, Histogram

seg_requests = Counter('segmentation_requests_total', 'Total segmentation requests')
seg_latency = Histogram('segmentation_latency_seconds', 'Segmentation latency')
seg_chars = Histogram('segmentation_chars', 'Text length in characters')

def segment_with_metrics(text, segmenter):
    seg_requests.inc()
    seg_chars.observe(len(text))

    start = time.time()
    result = segmenter.segment(text)
    latency = time.time() - start

    seg_latency.observe(latency)
    return result
```

**Dashboard**:
- P50, P95, P99 latency
- Requests per second
- Text length distribution
- Error rate

## Summary Decision Table

| Requirement | Tool | Rationale |
|-------------|------|-----------|
| **Speed > Accuracy** | Jieba | 2000 sent/s, good enough accuracy |
| **Accuracy > Speed** | PKUSeg / CKIP / LTP | 96-99% F1, GPU recommended |
| **Traditional Chinese** | CKIP | 97.33% F1, Academia Sinica |
| **Simplified Chinese** | PKUSeg | 96.88% F1, domain models |
| **Medical/Legal** | PKUSeg | Pre-trained domain models |
| **Social Media** | PKUSeg (web) | 94.21% F1 on Weibo |
| **Multi-Task NLP** | LTP | 6 tasks (WS, POS, NER, DP, SDP, SRL) |
| **Embedded/Mobile** | Jieba | 55 MB runtime |
| **Serverless** | Jieba | 200ms cold start |
| **GPU Deployment** | LTP / CKIP | 10-20x speedup |
| **High Throughput Batch** | LTP Legacy | 21,581 sent/s |
| **Commercial Product** | Jieba / PKUSeg | MIT license |
| **Research/Academic** | LTP / CKIP | Published benchmarks |

## Next Steps

After selecting a tool based on this analysis:

1. **Benchmark**: Test on your specific corpus
2. **Prototype**: Implement POC with selected tool
3. **Load test**: Verify throughput meets requirements
4. **A/B test**: Compare accuracy with ground truth
5. **Deploy**: Roll out gradually with monitoring
6. **Iterate**: Fine-tune (custom dictionaries, model training)

## Cross-References

- **S1 Rapid Discovery**: [recommendation.md](../S1-rapid/recommendation.md) - Quick overview
- **S2 Deep Dives**: [jieba.md](jieba.md), [ckip.md](ckip.md), [pkuseg.md](pkuseg.md), [ltp.md](ltp.md)
- **S2 Feature Comparison**: [feature-comparison.md](feature-comparison.md) - Side-by-side matrix
- **S3 Need-Driven**: Use case recommendations (to be created)
- **S4 Strategic**: Long-term viability and maintenance (to be created)
