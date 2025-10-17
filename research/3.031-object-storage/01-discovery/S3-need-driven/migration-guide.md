# S3: Migration Guide - When and How to Switch Providers

**Date**: 2025-10-16
**Methodology**: S3 - Need-Driven Analysis
**Purpose**: Migration strategies, effort estimates, and decision frameworks

---

## When to Migrate

### Migration Triggers

**Cost Optimization**:
- ✅ Egress costs >$5K/month → Consider Cloudflare R2 or Backblaze B2
- ✅ Storage >10TB → Consider Backblaze B2 (96% savings vs AWS)
- ✅ Growing cloud bills → Evaluate S3-compatible alternatives

**Performance Issues**:
- ✅ Global latency problems → Consider Cloudflare R2 (edge network)
- ✅ Throughput bottlenecks → Consider AWS/Azure/GCS or B2 Overdrive

**Compliance Changes**:
- ✅ New HIPAA requirement → Ensure BAA available
- ✅ FedRAMP mandate → Must move to AWS/Azure/GCS
- ✅ EU data residency → Ensure provider has EU regions

**Vendor Risk**:
- ✅ AWS bills unpredictable → Move to flat-rate provider (Wasabi, DigitalOcean)
- ✅ Vendor acquisition/shutdown concerns → Diversify to multiple providers
- ✅ Lock-in concerns → Move to S3-compatible provider

**Feature Needs**:
- ✅ Need Object Lock (WORM) → AWS/Azure/GCS/Wasabi
- ✅ Need cross-region replication → AWS/Azure/GCS
- ✅ Need query-in-place → AWS S3 Select, Azure, GCS

---

## Migration Complexity Matrix

### By Current Provider

| From | To | Complexity | Effort | Notes |
|------|--|-----------| -------|-------|
| **AWS S3** → Cloudflare R2 | Low | 1-4 hours | S3 API compatible, endpoint change only |
| **AWS S3** → Backblaze B2 | Low | 1-4 hours | S3 API compatible, test edge cases |
| **AWS S3** → Wasabi | Low | 1-4 hours | High S3 compatibility (95%) |
| **AWS S3** → Azure Blob | High | 40-160 hours | Complete code rewrite (different API) |
| **AWS S3** → GCS | Medium | 8-40 hours | Limited S3 compatibility, rewrite recommended |
| **Azure Blob** → AWS S3 | High | 40-160 hours | Complete code rewrite |
| **Azure Blob** → R2/B2/Wasabi | High | 40-160 hours | Complete code rewrite to S3 API |
| **GCS** → AWS S3 | Medium | 8-40 hours | Different API semantics |
| **GCS** → R2/B2/Wasabi | Medium | 8-40 hours | Migration to S3 API |
| **R2** → **B2** or **Wasabi** | Very Low | 1-2 hours | S3 API compatible, endpoint change |
| **B2** → **R2** or **Wasabi** | Very Low | 1-2 hours | S3 API compatible, endpoint change |

**Key Insight**: Migrating *within* S3-compatible providers (AWS S3, R2, B2, Wasabi) is easy (1-4 hours). Migrating from Azure Blob or GCS requires code rewrites (8-160 hours).

---

## Migration Patterns

### Pattern 1: Endpoint-Only Migration (Easiest)

**Applies To**:
- AWS S3 → Cloudflare R2 / Backblaze B2 / Wasabi
- Between S3-compatible providers (R2 ↔ B2 ↔ Wasabi)

**Requirements**:
- Using standard S3 API (boto3, AWS SDK, s3cmd)
- No AWS-specific features (Glacier, Object Lambda, S3 Select)
- Core operations only (GET, PUT, LIST, DELETE, multipart)

**Steps**:
1. Create bucket on new provider
2. Update S3 endpoint configuration:
```python
# Before (AWS S3)
s3_client = boto3.client('s3', region_name='us-east-1')

# After (Cloudflare R2)
s3_client = boto3.client('s3',
    endpoint_url='https://[account_id].r2.cloudflarestorage.com',
    aws_access_key_id='R2_ACCESS_KEY',
    aws_secret_access_key='R2_SECRET_KEY'
)

# Or (Backblaze B2)
s3_client = boto3.client('s3',
    endpoint_url='https://s3.us-west-004.backblazeb2.com',
    aws_access_key_id='B2_KEY_ID',
    aws_secret_access_key='B2_APPLICATION_KEY'
)
```
3. Copy data (see data migration strategies below)
4. Update DNS/CDN (if applicable)
5. Cutover traffic
6. Delete old data after validation

**Effort**: 1-4 hours
**Risk**: Low

---

### Pattern 2: Feature-Aware Migration (Moderate)

**Applies To**:
- AWS S3 → R2/B2 when using some advanced features
- Applications using versioning, lifecycle policies, events

**Steps**:
1. **Audit features used**:
   - ✅ Supported: Core API, multipart uploads, presigned URLs, lifecycle (basic)
   - ⚠️ Limited: Versioning (not on B2), event notifications (limited on alternatives)
   - ❌ Unsupported: Object Lock (not on R2/B2), S3 Select, Glacier transitions
2. **Refactor unsupported features**:
   - Object Lock → Implement immutability at application layer or use Wasabi
   - S3 Select → Query after download or use analytics provider
   - Glacier → Use provider's archive tier (if available) or separate cold storage
3. **Test compatibility**:
   - Create test bucket on new provider
   - Run integration tests (uploads, downloads, multipart, presigned URLs)
   - Validate edge cases (large files, special characters in keys)
4. **Migrate data** (see strategies below)
5. **Update application code** (if needed for feature gaps)
6. **Gradual cutover** (blue/green or percentage-based)

**Effort**: 4-40 hours (depends on feature complexity)
**Risk**: Medium

---

### Pattern 3: Complete Rewrite (Complex)

**Applies To**:
- Azure Blob → AWS S3 / R2 / B2 / Wasabi
- GCS → AWS S3 / R2 / B2 / Wasabi
- Applications tightly coupled to provider-specific features

**Steps**:
1. **Rewrite storage abstraction layer**:
```python
# Before (Azure Blob)
from azure.storage.blob import BlobServiceClient

blob_client = BlobServiceClient.from_connection_string(connection_string)
container = blob_client.get_container_client("my-container")
blob = container.upload_blob("key", data)

# After (S3 API - works with AWS, R2, B2, Wasabi)
import boto3

s3 = boto3.client('s3', endpoint_url=PROVIDER_ENDPOINT)
s3.put_object(Bucket='my-bucket', Key='key', Body=data)
```
2. **Update all storage operations**:
   - Azure Containers → S3 Buckets
   - Azure Blobs → S3 Objects
   - SAS tokens → Presigned URLs
   - Azure Event Grid → S3 Event Notifications (if supported)
3. **Migrate authentication/IAM**:
   - Azure AD → IAM (AWS) or access keys (R2/B2)
4. **Migrate data** (cross-cloud transfer tools)
5. **Extensive testing** (functional, performance, edge cases)
6. **Staged rollout** (canary → percentage → full cutover)

**Effort**: 40-160 hours (depends on application complexity)
**Risk**: High

---

## Data Migration Strategies

### Strategy 1: AWS CLI / rclone (Small to Medium)

**Best For**: <100TB, one-time migration

**Using rclone** (supports all providers):
```bash
# Configure source and destination
rclone config  # Set up [source] and [dest]

# Copy data
rclone copy source:bucket dest:bucket --progress --transfers=32

# Verify
rclone check source:bucket dest:bucket
```

**Using AWS CLI S3 sync** (S3-compatible only):
```bash
# AWS S3 → Cloudflare R2
aws s3 sync s3://source-bucket s3://dest-bucket \
  --endpoint-url https://[account].r2.cloudflarestorage.com \
  --profile r2-profile
```

**Effort**: 1-8 hours (plus transfer time)
**Cost**: Egress fees from source provider

---

### Strategy 2: Cloud-Native Transfer Services (Medium to Large)

**AWS DataSync** (AWS S3 → other S3-compatible):
- Managed transfer service
- Handles retries, validation
- Cost: $0.0125/GB transferred
- Best for: >10TB from AWS

**Azure Data Box** (Azure → elsewhere):
- Physical appliance for massive transfers
- Cost: $200-300 for device + shipping
- Best for: >100TB from Azure (avoid egress fees)

**Google Transfer Service**:
- Managed transfers from GCS
- Free within Google Cloud
- Best for: >10TB from GCS

**Effort**: 2-16 hours setup + transfer time
**Cost**: Service fees + potential egress fees

---

### Strategy 3: Multi-Cloud Transfer Tools (Large Scale)

**Aspera / SignalFire** (commercial):
- High-speed transfer (10-100× faster than traditional)
- Cost: $$$ (licensing)
- Best for: >100TB, time-sensitive

**rclone with parallelization** (open-source):
```bash
# High-performance parallel transfer
rclone copy source:bucket dest:bucket \
  --transfers=64 \
  --checkers=32 \
  --fast-list \
  --progress
```

**Effort**: 4-16 hours setup
**Cost**: Egress fees only (rclone is free)

---

### Strategy 4: Dual-Write Migration (Zero Downtime)

**Best For**: Production systems, zero downtime requirement

**Steps**:
1. **Phase 1: Dual Write**
   - Write to both old and new providers
   - Read from old provider (primary)
```python
def upload_file(key, data):
    # Write to both
    old_s3.put_object(Bucket=OLD_BUCKET, Key=key, Body=data)
    new_s3.put_object(Bucket=NEW_BUCKET, Key=key, Body=data)
```

2. **Phase 2: Backfill Historical Data**
   - Copy existing data (rclone/AWS CLI)
   - Validate checksums

3. **Phase 3: Flip Read**
   - Change application to read from new provider
   - Keep dual-write for safety period

4. **Phase 4: Deprecate Old**
   - Stop writing to old provider
   - Delete old data after retention period

**Effort**: 8-40 hours (application changes)
**Cost**: Double storage for migration period (1-4 weeks typical)
**Risk**: Low (zero downtime)

---

## Cost Optimization Migration Calculator

### Example: AWS S3 → Backblaze B2 (100TB storage, 200TB egress/month)

**Current Cost (AWS S3)**:
- Storage: $2,300/mo
- Egress: $17,800/mo
- **Total: $20,100/mo**

**Target Cost (Backblaze B2)**:
- Storage: $600/mo
- Egress: $0 (within 3× limit: 200TB < 300TB)
- **Total: $600/mo**

**Migration Costs**:
- Data transfer (one-time egress from AWS): 100TB × $0.09 = $9,000
- Engineering effort: 4 hours × $150/hr = $600
- **Total Migration: $9,600**

**ROI**:
- Monthly savings: $20,100 - $600 = **$19,500/mo**
- Payback period: $9,600 / $19,500 = **0.5 months**
- Annual savings: $19,500 × 12 = **$234,000/year**

**Verdict**: Migration pays for itself in 2 weeks, saves $234K annually

---

## Migration Checklist

### Pre-Migration
- [ ] Audit current storage usage (volume, egress, requests)
- [ ] Calculate current monthly costs
- [ ] Identify features used (versioning, lifecycle, events, etc.)
- [ ] Estimate migration effort (use patterns above)
- [ ] Choose target provider (cost, compliance, features)
- [ ] Calculate target costs and ROI
- [ ] Get budget approval (migration costs + new provider)

### Planning
- [ ] Create migration plan (dual-write, cutover, or rewrite)
- [ ] Set up test bucket on new provider
- [ ] Run compatibility tests (upload, download, multipart, presigned URLs)
- [ ] Identify code changes required
- [ ] Plan data transfer strategy (rclone, DataSync, etc.)
- [ ] Schedule migration window (if downtime required)
- [ ] Prepare rollback plan

### Execution
- [ ] Create production bucket(s) on new provider
- [ ] Configure IAM/access keys
- [ ] Update application configuration (endpoints, credentials)
- [ ] Deploy code changes (if any)
- [ ] Start data migration (background or cutover)
- [ ] Validate data integrity (checksums, object counts)
- [ ] Test application functionality end-to-end
- [ ] Monitor performance (latency, throughput, errors)
- [ ] Cutover traffic (gradual or immediate)

### Post-Migration
- [ ] Monitor costs (ensure projected savings realized)
- [ ] Monitor performance (latency, errors, availability)
- [ ] Validate compliance (if required)
- [ ] Update documentation (new provider, endpoints)
- [ ] Delete old data (after retention period)
- [ ] Review ROI (actual vs projected)
- [ ] Document lessons learned

---

## Common Migration Pitfalls

### Pitfall 1: Underestimating Egress Costs

**Problem**: Migrating 100TB from AWS costs $9,000 in egress fees

**Solutions**:
- Use AWS DataSync (may reduce costs)
- Migrate gradually (stay within free tier)
- Consider AWS Snowball (physical transfer, $200-300 for >100TB)

---

### Pitfall 2: Assuming 100% S3 Compatibility

**Problem**: Code breaks on new provider due to unsupported features

**Solutions**:
- Test thoroughly before migration
- Check provider compatibility documentation
- Avoid provider-specific features (Glacier, S3 Select, Object Lambda)

---

### Pitfall 3: Ignoring Performance Differences

**Problem**: New provider is slower, impacting application

**Solutions**:
- Test performance before migration (upload/download speeds)
- Consider provider's network (Cloudflare edge vs single region)
- Use B2 Overdrive ($15/TB) if speed critical

---

### Pitfall 4: Not Planning Rollback

**Problem**: Migration fails, cannot quickly revert

**Solutions**:
- Keep old provider active during migration
- Use dual-write pattern (can flip back to old provider)
- Validate data integrity before deleting old data

---

## Migration Decision Tree

```
START: Should I migrate?

1. Calculate ROI
   - Savings < $500/mo? → Don't migrate (not worth effort)
   - Savings $500-5K/mo? → Migrate if effort <8 hours (simple endpoint change)
   - Savings >$5K/mo? → Strongly consider migration

2. Check Compatibility
   - Using only core S3 API? → Easy migration (1-4 hours)
   - Using some advanced features? → Moderate migration (4-40 hours)
   - Tight integration with AWS/Azure/GCP? → Hard migration (40-160 hours)

3. Assess Compliance
   - FedRAMP required? → Cannot leave AWS/Azure/GCS
   - HIPAA only? → Can migrate to R2/B2/Wasabi
   - No compliance? → Free to choose any provider

4. Evaluate Risk
   - Production system? → Use dual-write (zero downtime)
   - Test/staging? → Direct cutover (simpler)
   - High data volume (>100TB)? → Plan for egress costs

5. Decide
   - ROI >12 months payback? → Proceed with migration
   - High risk / low savings? → Stay with current provider
   - Locked in by features? → Refactor or accept cost
```

---

## Key Takeaways

1. **Migrating between S3-compatible providers is easy** (1-4 hours for endpoint change)
2. **Migrating from Azure Blob or GCS is hard** (40-160 hours for code rewrite)
3. **ROI often justifies migration** (payback in weeks/months for high-egress workloads)
4. **Dual-write enables zero-downtime migration** (at cost of temporary double storage)
5. **Test compatibility before committing** (not all providers are 100% S3-compatible)
6. **Egress fees can be significant** ($0.09/GB from AWS, consider Snowball for >100TB)
7. **Don't migrate just for cost** (consider compliance, features, vendor risk holistically)

**Most Common Migration**: AWS S3 → Cloudflare R2 or Backblaze B2 (easy, 90%+ savings, 1-4 hour effort, payback in weeks)
