# Backend Analysis: Wasabi

**Provider**: Wasabi Technologies
**Type**: Managed cloud storage
**S3 API**: 100% bit-compatible (claimed)

---

## Overview

Wasabi positions itself as **"100% bit-compatible with Amazon S3"**, focusing on hot storage with predictable pricing. No egress fees, no API fees, but requires 90-day minimum storage retention.

**S3 API Compatibility**: ~85-90% (certified compatible)
**Status**: Production since 2017

---

## S3 API Compatibility

**Compatibility Score**: ~85-90% (certified S3-compatible)

**Supported Features**:
- ✅ Core object operations (PUT, GET, DELETE, COPY, HEAD)
- ✅ Bucket operations (CREATE, LIST, DELETE)
- ✅ Multipart uploads
- ✅ Server-side encryption
- ✅ Object versioning
- ✅ Bucket policies
- ✅ Lifecycle policies (basic)
- ✅ CORS configuration
- ✅ Object locking (immutability)
- ✅ AWS STS (AssumeRole, max 12-hour sessions)
- ✅ Signature v2 and v4 (both headers and query parameters)

**Not Supported**:
- ❌ BitTorrent operations
- ❌ Object tagging (may be added)
- ❌ Multiple storage classes (single hot tier only)
- ❌ POST object RESTORE requests
- ❌ S3 Select
- ❌ S3 Batch Operations
- ❌ Replication (not built-in)

---

## Performance Characteristics

**Throughput**: High (comparable to S3)
**Latency**:
- First byte: 100-200ms (varies by region)
- 6 global storage regions

**Durability**: 99.999999999% (11 nines)
**Availability**: 99.9% guarantee

---

## Pricing (as of 2025)

**Storage**:
- $0.00699/GB/month ($6.99/TB/month) ⭐ Very competitive
- **90-day minimum retention** (deleted early = charged for full 90 days)

**Requests**:
- **FREE** (no per-request charges) ⭐ Unique advantage

**Data Transfer**:
- **Egress**: FREE up to your storage amount (1 TB stored = 1 TB free egress)
  - Example: 10 TB stored = 10 TB free egress per month
- **Ingress**: FREE

**Key Advantages**:
1. No egress fees (up to storage amount)
2. No API request fees
3. Predictable pricing

**Key Constraint**: 90-day minimum retention

---

## Strengths

1. **Predictable pricing**: No per-request or egress fees (within quota)
2. **S3 bit-compatible**: Strong compatibility claims
3. **Hot storage focused**: Optimized for frequently accessed data
4. **Simple pricing model**: Easy to calculate costs
5. **6 global regions**: US, EU, Asia-Pacific options

---

## Weaknesses

1. **90-day minimum retention**: Pay for deleted data until 90 days
2. **Single storage tier**: No cold/archive options
3. **Feature gaps**: No tagging, S3 Select, batch ops
4. **Egress quota**: Free only up to storage amount (10 TB stored = 10 TB free egress)
5. **Smaller ecosystem**: Less tooling than AWS/Cloudflare

---

## Migration Experience

**AWS S3 → Wasabi**:

**Code Changes Required**:
```python
# Before (AWS S3)
s3 = boto3.client('s3',
    region_name='us-east-1')

# After (Wasabi) - Change endpoint + credentials
s3 = boto3.client('s3',
    endpoint_url='https://s3.us-east-1.wasabisys.com',
    aws_access_key_id=WASABI_ACCESS_KEY,
    aws_secret_access_key=WASABI_SECRET_KEY)
```

**Tools**:
- AWS CLI (with endpoint override)
- rclone
- s3cmd
- Any S3-compatible tool

**Effort**: 1-2 hours for code changes + data transfer time

---

## Compatibility Gotchas

1. **90-Day Minimum**: Deleting data before 90 days = still charged
   - Impacts cost for temporary/short-lived data
2. **Egress Quota**: Free egress = your storage amount
   - 10 TB stored, 15 TB egress/month = 5 TB charged
3. **No Storage Classes**: Can't use Glacier, IA, Intelligent-Tiering equivalents
4. **Object Tagging**: Not supported (may impact applications relying on tags)

---

## Use Case Fit

**GOOD For**:
- ✅ Hot storage (frequently accessed data)
- ✅ Long-term storage (>90 days)
- ✅ Predictable access patterns
- ✅ Read-heavy workloads (free egress up to quota)
- ✅ Backup archives (kept long-term)

**NOT GOOD For**:
- ❌ Temporary storage (<90 days)
- ❌ Highly variable data (frequent create/delete)
- ❌ Cold/archive storage needs
- ❌ Applications using S3 tagging heavily

---

## Portability Considerations

**Migrating FROM Wasabi**:
- ✅ Easy to any S3-compatible service
- ⚠️ Watch 90-day minimum (don't delete until retained 90 days)
- Time: 1-2 hours + data transfer

**Migrating TO Wasabi**:
- ✅ Easy from S3/R2/B2
- ⚠️ Test if using object tagging or advanced features
- Time: 1-2 hours + data transfer

**Portability Risk**: Low-Medium (good S3 compatibility, but 90-day retention is business constraint)

**Recommendation**: Great for long-term hot storage with predictable access. Avoid for short-lived or highly dynamic data. Excellent S3 compatibility for core operations.
