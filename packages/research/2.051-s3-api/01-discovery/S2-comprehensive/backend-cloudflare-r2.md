# Backend Analysis: Cloudflare R2

**Provider**: Cloudflare
**Type**: Managed cloud storage
**S3 API**: Compatible (with modifications)

---

## Overview

Cloudflare R2 is object storage with **zero egress fees**, launched 2022. Primary differentiator vs AWS S3 is cost savings on data transfer.

**S3 API Compatibility**: High (~90% core features)
**Status**: Generally available since May 2022

---

## S3 API Compatibility

**Compatibility Score**: ~90% (core features supported)

**Supported Features**:
- ✅ Core object operations (PUT, GET, DELETE, COPY, HEAD)
- ✅ Bucket operations (CREATE, LIST, DELETE)
- ✅ Multipart uploads (including CRC-64/NVME checksums as of 2025)
- ✅ Server-side encryption (SSE-C as of 2025)
- ✅ Object versioning
- ✅ Object locking (WORM compliance)
- ✅ Lifecycle policies (basic)
- ✅ Access control (bucket policies, presigned URLs)
- ✅ CORS configuration
- ✅ Public buckets (via R2.dev subdomain)

**Not Supported / Limited**:
- ⚠️ Event notifications (limited - no Lambda/Worker triggers yet)
- ❌ S3 Select (SQL queries)
- ❌ S3 Batch operations
- ❌ Replication (not yet available)
- ❌ Website hosting (use Workers instead)
- ⚠️ Storage classes (R2 has single tier, no Glacier/IA)

**R2-Specific Features** (non-portable):
- Cloudflare Workers integration
- R2.dev automatic public URLs
- Integrated CDN capabilities

---

## Performance Characteristics

**Throughput**: High (Cloudflare network scale)
**Latency**:
- First byte: ~100ms globally (varies by location)
- Benefits from Cloudflare's global network

**Durability**: 99.999999999% (11 nines)
**Availability**: 99.9% SLA

---

## Pricing (as of 2025)

**Storage**:
- $0.015/GB/month (all storage)

**Requests**:
- Class A (writes, lists): $4.50 per million requests
- Class B (reads): $0.36 per million requests

**Data Transfer**:
- **Egress**: $0.00 (FREE) ⭐ Key differentiator
- **Ingress**: FREE

**Free Tier**:
- 10 GB storage
- 1 million Class A operations
- 10 million Class B operations

**Key Advantage**: Zero egress fees (vs AWS $0.09/GB)

---

## Strengths

1. **Zero egress fees**: Massive cost savings for read-heavy workloads
2. **S3 API compatible**: Drop-in replacement for most use cases
3. **Cloudflare integration**: Workers, CDN, DDoS protection
4. **Competitive storage pricing**: $0.015/GB (vs AWS $0.023/GB)
5. **Global network**: Cloudflare's extensive edge network

---

## Weaknesses

1. **Feature gaps**: No S3 Select, batch ops, limited events
2. **Single storage tier**: No cold storage options
3. **Newer service**: Less battle-tested than S3 (launched 2022)
4. **Lock-in risk**: Workers integration creates Cloudflare dependency

---

## Migration Experience

**AWS S3 → Cloudflare R2**:

**Tools**:
- Super Slurper (Cloudflare's migration tool) - Generally available
- Sippy (incremental migration) - Zero egress fees during migration
- rclone (third-party tool)

**Reported Migration Times**:
- Small datasets: <30 minutes
- Large datasets (millions of objects): Hours to days depending on volume
- **Example**: PDQ migrated all data in <30 minutes (expected 1 day)

**Code Changes Required**:
```python
# Before (AWS S3)
s3 = boto3.client('s3',
    endpoint_url='https://s3.amazonaws.com',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY)

# After (Cloudflare R2) - ONLY endpoint change
s3 = boto3.client('s3',
    endpoint_url='https://<ACCOUNT_ID>.r2.cloudflarestorage.com',
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY)
```

**Effort**: 1-2 hours for basic setup, hours-days for data migration depending on volume

---

## Compatibility Gotchas

1. **CRC32 Checksums**: Fixed as of Feb 2025, but older SDK versions had issues
2. **Event Notifications**: Limited compared to S3 (can't trigger Workers/Lambda yet)
3. **Storage Classes**: R2 has no Glacier/IA equivalent - single tier only
4. **Website Hosting**: Not supported - use Cloudflare Workers instead

---

## Portability Considerations

**Migrating FROM R2**:
- ✅ Easy if using core S3 API only
- ⚠️ Moderate if using Workers integration
- Time: 1-2 hours code changes + data transfer time

**Migrating TO R2**:
- ✅ Very easy from S3 (Super Slurper handles it)
- ✅ Easy from other S3-compatible providers

**Portability Risk**: Low for core S3 API usage, Medium if using Workers

**Recommendation**: Great S3-compatible alternative for read-heavy workloads (savings on egress). Avoid Workers lock-in for portability.
