# Backend Analysis: Backblaze B2

**Provider**: Backblaze
**Type**: Managed cloud storage
**S3 API**: Compatible (native API also available)

---

## Overview

Backblaze B2 offers both a native B2 API and S3-compatible API (launched May 2020). Known for **lowest storage costs** among major providers.

**S3 API Compatibility**: ~85% (core features + some limitations)
**Status**: Production since 2015 (S3 API since 2020)

---

## S3 API Compatibility

**Compatibility Score**: ~85% (good core support, some gaps)

**Supported Features**:
- ✅ Core object operations (PUT, GET, DELETE, COPY, HEAD)
- ✅ Bucket operations (CREATE, LIST, DELETE)
- ✅ Multipart uploads
- ✅ Server-side encryption (SSE-B2, SSE-C)
- ✅ Object versioning (versioned by default)
- ✅ Bucket policies (basic)
- ✅ CORS configuration
- ✅ Presigned URLs

**Not Supported / Limited**:
- ❌ SSE-KMS (AWS-specific encryption)
- ❌ IAM roles (use application keys instead)
- ⚠️ Object tagging (Get Object Tagging returns empty for compatibility)
- ❌ Website hosting
- ❌ Lifecycle rules (not in S3 API - use native B2 API)
- ❌ Replication
- ❌ S3 Select
- ⚠️ ACLs (only supports "private" and "public-read", no complex ACLs)

**Authentication**:
- Only supports AWS Signature v4 (v2 not supported)

---

## Performance Characteristics

**Throughput**:
- Download: Up to 1 GB/s per file
- Upload: Scalable with multipart uploads

**Latency**:
- First byte: 150-300ms (depends on region)
- Single region deployment (US West by default)

**Durability**: 99.999999999% (11 nines)
**Availability**: 99.9% target

---

## Pricing (as of 2025)

**Storage**:
- $0.006/GB/month ($6/TB/month) ⭐ Lowest among major providers

**Requests** (via S3 API):
- Class A (PUT, POST): $0.004 per 10,000 requests
- Class B (GET, HEAD): $0.0004 per 10,000 requests
- Class C (LIST): $0.004 per 1,000 requests

**Data Transfer**:
- **Egress**: First 3x your storage is FREE daily, then $0.01/GB
  - Example: 10 TB stored = 30 TB free egress/day
- **Ingress**: FREE

**Free Tier**:
- 10 GB storage
- 1 GB/day egress

**Key Advantage**: Lowest storage cost + generous egress (3x your storage free)

---

## Strengths

1. **Lowest cost**: $6/TB storage (vs AWS $23/TB, R2 $15/TB)
2. **Generous egress**: 3x your storage free daily
3. **S3 API + native B2 API**: Choose which to use
4. **Simplicity**: Straightforward pricing, no hidden fees
5. **Reliability**: 10+ years in production

---

## Weaknesses

1. **Feature gaps**: No lifecycle, tagging, complex ACLs via S3 API
2. **Single region**: US West only (for most users)
3. **Limited ecosystem**: Smaller than AWS/Cloudflare
4. **Performance**: Higher latency than global CDN-backed storage

---

## Migration Experience

**AWS S3 → Backblaze B2**:

**Tools**:
- B2 CLI (official tool)
- rclone (popular third-party)
- s3cmd, s3fs-fuse (S3-compatible tools)

**Code Changes Required**:
```python
# Before (AWS S3)
s3 = boto3.client('s3',
    endpoint_url='https://s3.amazonaws.com',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY)

# After (Backblaze B2) - Change endpoint + credentials
s3 = boto3.client('s3',
    endpoint_url='https://s3.us-west-004.backblazeb2.com',
    aws_access_key_id=B2_KEY_ID,
    aws_secret_access_key=B2_APPLICATION_KEY)
```

**Effort**: 1-2 hours for code changes, data transfer time varies

**Gotcha**: Some advanced S3 features not available - test thoroughly

---

## Compatibility Gotchas

1. **Object Tagging**: API accepts tags but returns empty (doesn't store them)
2. **ACLs**: Only "private" and "public-read" supported (no fine-grained ACLs)
3. **Lifecycle**: Not available via S3 API (use native B2 API or manual management)
4. **Authentication**: Signature v4 only (no v2 support)
5. **Versioning**: All buckets are versioned (can't disable)

---

## Portability Considerations

**Migrating FROM B2**:
- ✅ Easy if using core S3 API
- ⚠️ Moderate if using native B2 API features
- Time: 1-2 hours code changes + data transfer

**Migrating TO B2**:
- ✅ Easy from S3 for basic use cases
- ⚠️ May need to remove unsupported features (tagging, lifecycle, complex ACLs)

**Portability Risk**: Medium (some S3 features not supported, but core API works)

**Recommendation**: Best for cost-conscious users with simple storage needs. Test compatibility if using advanced S3 features. Consider using native B2 API for features not in S3 compatibility layer.
