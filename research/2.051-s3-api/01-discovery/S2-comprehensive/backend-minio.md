# Backend Analysis: MinIO

**Provider**: MinIO (open-source project)
**Type**: Self-hosted object storage
**S3 API**: Highly compatible (~95%)

---

## Overview

MinIO is the **most popular self-hosted S3-compatible object storage**. Open-source (AGPLv3), designed as drop-in S3 replacement for on-premises and multi-cloud deployments.

**S3 API Compatibility**: ~95% (highest among alternatives)
**Deployment**: ~1 million deployments worldwide
**Status**: Production-ready since 2015

---

## S3 API Compatibility

**Compatibility Score**: ~95% (highest S3 compatibility outside AWS)

**Supported Features**:
- ✅ Core object operations (PUT, GET, DELETE, COPY, HEAD)
- ✅ Bucket operations (CREATE, LIST, DELETE, versioning)
- ✅ Multipart uploads
- ✅ Server-side encryption (SSE-S3, SSE-KMS, SSE-C)
- ✅ Object versioning
- ✅ Object locking (WORM compliance)
- ✅ Lifecycle policies (transition, expiration)
- ✅ Event notifications (AMQP, MQTT, NATS, NSQ, Elasticsearch, Kafka, Redis, MySQL, PostgreSQL, webhooks)
- ✅ Bucket policies
- ✅ Bucket notifications
- ✅ CORS configuration
- ✅ Replication (server-side, active-active, multi-site)
- ✅ Object tagging
- ✅ S3 Select (SQL queries on objects)

**Limited/Not Supported**:
- ⚠️ ListMultipartUploads: Requires exact object name as prefix
- ❌ AbortIncompleteMultipartUpload lifecycle action
- ⚠️ Some AWS-specific features (Glacier, Intelligent-Tiering, Object Lambda)

**MinIO-Specific Features** (non-portable):
- MinIO Admin API (cluster management)
- MinIO KMS integration
- Identity and Access Management (IAM/STS)

---

## Performance Characteristics

**Throughput**:
- Read: 325 GB/s (multi-node cluster)
- Write: 165 GB/s (multi-node cluster)
- Single-node: Depends on hardware (typically disk-limited)

**Latency**:
- First byte: <10ms (local network)
- Depends entirely on hardware and network

**Durability**: Configurable (erasure coding, replication)
- Erasure coding: Can survive n/2 disk failures
- Typically configured for 99.999999999% (11 nines) with erasure coding

**Availability**: Depends on deployment (single node vs distributed cluster)

---

## Pricing (Self-Hosted)

**Software**: FREE (open-source AGPLv3)

**Infrastructure Costs** (you provide):
- Servers/VMs: $100-1000+/month depending on scale
- Storage: Disk costs (varies widely)
- Network: LAN/WAN costs
- Personnel: DevOps time for management

**Commercial Support**: Available from MinIO (paid subscriptions)

**Cost Model**:
- **Small scale (<10 TB)**: Usually more expensive than managed services
- **Large scale (>100 TB)**: Can be cheaper than managed services
- **Break-even**: Typically 50-100 TB depending on requirements

---

## Strengths

1. **Highest S3 compatibility**: ~95% feature support
2. **Self-hosted**: Full control, data sovereignty
3. **Open-source**: No vendor lock-in to MinIO itself
4. **Performance**: Extremely fast on proper hardware
5. **Battle-tested**: ~1M deployments, used by major companies
6. **Multi-cloud**: Deploy on AWS, Azure, Google Cloud
7. **Feature-rich**: S3 Select, replication, versioning, encryption

---

## Weaknesses

1. **Operational burden**: You manage infrastructure, updates, backups
2. **Cost at small scale**: Not economical for <10 TB
3. **Expertise required**: Need storage/ops knowledge
4. **Durability responsibility**: You configure erasure coding/replication
5. **No SLA**: Unless you pay for commercial support

---

## Deployment Scenarios

**Single-Server Mode** (development, small deployments):
```bash
docker run -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=admin \
  -e MINIO_ROOT_PASSWORD=password \
  minio/minio server /data --console-address ":9001"
```

**Distributed Mode** (production, high availability):
- Multiple servers (4+) with erasure coding
- Survives disk and node failures
- Horizontal scaling

**Migration to MinIO**:

**AWS S3 → MinIO**:
```python
# Before (AWS S3)
s3 = boto3.client('s3')

# After (MinIO) - Change endpoint only
s3 = boto3.client('s3',
    endpoint_url='http://minio.example.com:9000',
    aws_access_key_id='minio_access_key',
    aws_secret_access_key='minio_secret_key')
```

**Effort**: 1-2 hours code changes + infrastructure setup + data migration

---

## Compatibility Gotchas

1. **ListMultipartUploads**: Requires exact object name prefix (stricter than S3)
2. **Lifecycle Actions**: AbortIncompleteMultipartUpload not supported
3. **Performance**: Heavily hardware-dependent (disk speed, network, CPU)
4. **Erasure coding overhead**: Write performance impact with high parity levels

---

## Portability Considerations

**Migrating FROM MinIO**:
- ✅ Very easy to any S3-compatible service (code unchanged)
- ✅ High S3 API fidelity means low risk
- Time: 1-2 hours + data transfer

**Migrating TO MinIO**:
- ✅ Easy from AWS S3, R2, B2, etc.
- ⚠️ Need infrastructure setup first
- Time: 4-8 hours (setup) + 1-2 hours (code) + data transfer

**Portability Risk**: Very low (highest S3 compatibility)

**Recommendation**: Best self-hosted option for:
- Data sovereignty requirements (healthcare, finance, government)
- Large scale (>50 TB) where cost savings justify ops burden
- Multi-cloud flexibility (deploy anywhere)
- Full control over infrastructure

**Not recommended for**:
- Small scale (<10 TB) - managed services cheaper
- Teams without ops expertise
- When simplicity/speed preferred over control
