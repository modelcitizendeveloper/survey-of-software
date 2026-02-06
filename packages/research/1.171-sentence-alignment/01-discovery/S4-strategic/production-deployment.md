# Production Deployment: Enterprise Patterns

## Deployment Architecture Patterns

### Pattern 1: Batch Processing Pipeline

**Use Case**: MT training data preparation, periodic TM updates

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   S3/GCS    │────>│  Alignment   │────>│  Filtered   │
│  Raw Data   │     │   Service    │     │   Results   │
└─────────────┘     └──────────────┘     └─────────────┘
                          │
                          ├─> Queue (SQS/Pub/Sub)
                          ├─> Monitoring (Prometheus)
                          └─> Logging (CloudWatch)
```

**Architecture**:
- **Compute**: Kubernetes jobs (auto-scaling)
- **Storage**: Object storage (S3, GCS)
- **Queue**: Message queue for job distribution
- **Monitoring**: Metrics + alerting

**Implementation (Kubernetes)**:
```yaml
# alignment-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: sentence-alignment
spec:
  parallelism: 10  # Number of parallel workers
  completions: 100  # Total chunks to process
  template:
    spec:
      containers:
      - name: aligner
        image: myorg/vecalign:latest
        resources:
          limits:
            nvidia.com/gpu: 1  # Request GPU
            memory: "16Gi"
            cpu: "4"
        command:
        - python3
        - align_chunk.py
        - --input
        - $(CHUNK_FILE)
        - --output
        - $(OUTPUT_FILE)
      restartPolicy: OnFailure
```

**Scaling Strategy**:
- Horizontal: Add more workers
- Vertical: Use larger GPU instances
- Auto-scaling: Based on queue depth

### Pattern 2: Real-Time API Service

**Use Case**: Interactive TM lookups, on-demand alignment

```
┌──────────┐     ┌───────────────┐     ┌──────────────┐
│  Client  │────>│   API Gateway │────>│  Alignment   │
│   App    │<────│   (Rate Limit)│<────│  Service     │
└──────────┘     └───────────────┘     └──────────────┘
                                             │
                                             ├─> Cache (Redis)
                                             ├─> DB (PostgreSQL)
                                             └─> Embeddings (Faiss)
```

**Architecture**:
- **API**: FastAPI or Flask
- **Cache**: Redis for recently aligned pairs
- **Database**: PostgreSQL for TM storage
- **Vector Search**: Faiss for embedding similarity

**Implementation (FastAPI)**:
```python
# alignment_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import vecalign
import redis
import hashlib

app = FastAPI()
cache = redis.Redis(host='localhost', port=6379)

class AlignRequest(BaseModel):
    source: list[str]
    target: list[str]
    source_lang: str
    target_lang: str

class AlignResponse(BaseModel):
    alignments: list[tuple[list[int], list[int]]]
    cached: bool

@app.post("/align", response_model=AlignResponse)
async def align(request: AlignRequest):
    # Generate cache key
    cache_key = hashlib.md5(
        f"{request.source}{request.target}".encode()
    ).hexdigest()

    # Check cache
    cached_result = cache.get(cache_key)
    if cached_result:
        return AlignResponse(
            alignments=eval(cached_result),
            cached=True
        )

    # Perform alignment
    embeddings_src = vecalign.embed(request.source, request.source_lang)
    embeddings_tgt = vecalign.embed(request.target, request.target_lang)

    alignments = vecalign.align(
        embeddings_src,
        embeddings_tgt,
        max_size=4
    )

    # Cache result (TTL: 1 hour)
    cache.setex(cache_key, 3600, str(alignments))

    return AlignResponse(
        alignments=alignments,
        cached=False
    )

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

**Deployment (Docker Compose)**:
```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
      - DB_HOST=postgres
    deploy:
      replicas: 4
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: translation_memory
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api

volumes:
  postgres_data:
```

### Pattern 3: Serverless Event-Driven

**Use Case**: Low-volume, sporadic alignment requests

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   S3 Put    │────>│  Lambda/Cloud│────>│   S3 Output  │
│   Event     │     │   Function   │     │              │
└─────────────┘     └──────────────┘     └──────────────┘
```

**Architecture**:
- **Trigger**: Cloud storage event (S3, GCS)
- **Compute**: Serverless function (Lambda, Cloud Functions)
- **Output**: Write back to storage

**Implementation (AWS Lambda)**:
```python
# lambda_function.py
import boto3
import hunalign

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get input file from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Download input
    s3.download_file(bucket, key, '/tmp/input.txt')

    # Assume parallel structure: src/ and tgt/ folders
    src_file = key.replace('src/', 'tgt/')

    s3.download_file(bucket, src_file, '/tmp/target.txt')

    # Run alignment
    result = hunalign.align(
        '/tmp/input.txt',
        '/tmp/target.txt',
        dict_file='/opt/dict.txt'
    )

    # Upload result
    output_key = key.replace('src/', 'aligned/')
    s3.put_object(
        Bucket=bucket,
        Key=output_key,
        Body=result
    )

    return {
        'statusCode': 200,
        'body': f'Aligned {key}'
    }
```

**When to Use Serverless**:
- ✅ Low volume (<10K pairs/day)
- ✅ Sporadic usage patterns
- ✅ Cost-sensitive (pay per use)
- ❌ Not suitable for: High volume, GPU-heavy (vecalign)

## Monitoring and Observability

### Key Metrics to Track

**Performance Metrics**:
```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Throughput
alignments_total = Counter(
    'alignments_total',
    'Total number of alignments performed',
    ['tool', 'language_pair']
)

# Latency
alignment_duration = Histogram(
    'alignment_duration_seconds',
    'Time to align sentence pair',
    ['tool']
)

# Queue depth (for batch processing)
queue_depth = Gauge(
    'alignment_queue_depth',
    'Number of pending alignment jobs'
)

# Quality metrics
alignment_quality = Histogram(
    'alignment_score',
    'Alignment confidence score',
    ['tool']
)
```

**Dashboard (Grafana Query)**:
```promql
# Throughput (alignments per second)
rate(alignments_total[5m])

# p95 latency
histogram_quantile(0.95, alignment_duration_seconds_bucket)

# Error rate
rate(alignments_failed_total[5m]) / rate(alignments_total[5m])

# Queue backlog
queue_depth > 1000  # Alert if queue too deep
```

### Alerting Rules

```yaml
# prometheus-alerts.yaml
groups:
- name: alignment_alerts
  interval: 30s
  rules:
  - alert: HighErrorRate
    expr: rate(alignments_failed_total[5m]) > 0.05
    for: 5m
    annotations:
      summary: "Alignment error rate above 5%"

  - alert: SlowAlignment
    expr: histogram_quantile(0.95, alignment_duration_seconds_bucket) > 10
    for: 5m
    annotations:
      summary: "p95 alignment latency above 10 seconds"

  - alert: QueueBacklog
    expr: queue_depth > 10000
    for: 15m
    annotations:
      summary: "Alignment queue has large backlog"
```

## Quality Assurance in Production

### Continuous Quality Monitoring

```python
# quality_monitor.py
import random
from typing import Tuple

class QualityMonitor:
    def __init__(self, sample_rate=0.01):
        self.sample_rate = sample_rate
        self.samples = []

    def maybe_sample(self, src: str, tgt: str, alignment: Tuple) -> None:
        """
        Randomly sample alignments for manual review
        """
        if random.random() < self.sample_rate:
            self.samples.append({
                'source': src,
                'target': tgt,
                'alignment': alignment,
                'timestamp': datetime.now()
            })

            # Persist to database for review
            self.save_to_review_queue()

    def compute_metrics(self, validated_samples):
        """
        Compute precision/recall from human-validated samples
        """
        tp = sum(1 for s in validated_samples if s['correct'])
        fp = sum(1 for s in validated_samples if not s['correct'])

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0

        # Emit metric
        alignment_quality.observe(precision)
```

### A/B Testing Framework

```python
# ab_test.py
class AlignmentABTest:
    def __init__(self, variant_a, variant_b, traffic_split=0.5):
        self.variant_a = variant_a  # e.g., hunalign
        self.variant_b = variant_b  # e.g., vecalign
        self.traffic_split = traffic_split

    def align(self, src, tgt):
        # Route traffic
        if random.random() < self.traffic_split:
            variant = 'A'
            result = self.variant_a.align(src, tgt)
        else:
            variant = 'B'
            result = self.variant_b.align(src, tgt)

        # Log for analysis
        self.log_result(variant, result)

        return result

    def analyze_results(self):
        """
        Compare quality and latency between variants
        """
        # Query logs and compute metrics
        a_quality = self.get_quality('A')
        b_quality = self.get_quality('B')

        a_latency = self.get_latency('A')
        b_latency = self.get_latency('B')

        print(f"Variant A: Quality={a_quality}, Latency={a_latency}")
        print(f"Variant B: Quality={b_quality}, Latency={b_latency}")
```

## Cost Optimization Strategies

### Strategy 1: Tiered Processing

```python
# tiered_alignment.py
def align_with_tiers(src, tgt):
    """
    Use cheap tool first, escalate to expensive for hard cases
    """
    # Tier 1: Fast and cheap (hunalign)
    result_fast = hunalign.align(src, tgt)

    # Check confidence
    if result_fast.confidence > 0.7:
        return result_fast  # Good enough

    # Tier 2: Slower but accurate (vecalign)
    result_accurate = vecalign.align(src, tgt)

    return result_accurate
```

**Cost Savings**: 70-80% of pairs use cheap tool, 20-30% use expensive

### Strategy 2: Caching and Deduplication

```python
# caching.py
import hashlib
from functools import lru_cache

class AlignmentCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    def align_with_cache(self, src, tgt):
        # Generate cache key (hash of source + target)
        cache_key = hashlib.sha256(
            f"{src}|{tgt}".encode()
        ).hexdigest()

        # Check cache
        cached = self.redis.get(cache_key)
        if cached:
            return pickle.loads(cached)

        # Compute alignment
        result = vecalign.align(src, tgt)

        # Cache for future (TTL: 30 days)
        self.redis.setex(
            cache_key,
            30 * 24 * 3600,
            pickle.dumps(result)
        )

        return result
```

**Cost Savings**: 40-60% cache hit rate in production

### Strategy 3: Spot Instances for Batch Jobs

```yaml
# k8s-spot-instances.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: alignment-batch
spec:
  template:
    spec:
      nodeSelector:
        workload-type: spot  # Use spot/preemptible instances
      tolerations:
      - key: "spot"
        operator: "Equal"
        value: "true"
        effect: "NoSchedule"
      containers:
      - name: aligner
        image: myorg/vecalign:latest
```

**Cost Savings**: 60-90% vs on-demand instances (for batch workloads)

## Disaster Recovery and Business Continuity

### Backup Strategy

```bash
#!/bin/bash
# backup_tm.sh

# Daily backup of translation memory database
pg_dump translation_memory | gzip > tm_backup_$(date +%Y%m%d).sql.gz

# Upload to S3 (versioned bucket)
aws s3 cp tm_backup_$(date +%Y%m%d).sql.gz s3://backups/tm/

# Retain 30 days of backups
find . -name "tm_backup_*.sql.gz" -mtime +30 -delete
```

### Failover Pattern

```python
# failover.py
class AlignmentServiceWithFailover:
    def __init__(self, primary, secondary):
        self.primary = primary  # e.g., self-hosted vecalign
        self.secondary = secondary  # e.g., SaaS API

    def align(self, src, tgt):
        try:
            return self.primary.align(src, tgt)
        except Exception as e:
            logger.warning(f"Primary failed: {e}, using failover")
            return self.secondary.align(src, tgt)
```

## References

- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Prometheus Monitoring](https://prometheus.io/docs/introduction/overview/)
- [AWS Lambda](https://docs.aws.amazon.com/lambda/)
