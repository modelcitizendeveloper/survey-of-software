# Migration Testing: S3-Compatible Provider Switching

**Purpose**: Document actual migration steps and time estimates between S3-compatible providers

---

## Migration Scenario 1: AWS S3 → Cloudflare R2

**Use Case**: Reduce egress costs (AWS $0.09/GB → R2 $0.00/GB)

**Migration Steps**:

1. **Create R2 Bucket** (5 minutes)
   - Sign up for Cloudflare account
   - Create R2 bucket with same name
   - Generate R2 API credentials

2. **Update Application Code** (10-30 minutes)
   ```python
   # Before
   s3_client = boto3.client('s3')

   # After - Change endpoint + credentials
   s3_client = boto3.client('s3',
       endpoint_url='https://<account_id>.r2.cloudflarestorage.com',
       aws_access_key_id=R2_ACCESS_KEY,
       aws_secret_access_key=R2_SECRET_KEY,
       region_name='auto')
   ```

3. **Migrate Data** (variable time)
   - **Tool**: Cloudflare Super Slurper or rclone
   - **Time**: Minutes to days depending on volume
   - **Example**: <30 min for small datasets, hours for large

4. **Update DNS/CDN** (15-30 minutes)
   - Update CloudFront/CDN to point to R2
   - Test public URL access

5. **Verify & Cutover** (30-60 minutes)
   - Test uploads/downloads
   - Verify application functionality
   - Switch production traffic

**Total Time**: 1-2 hours (code/config) + data transfer time
**Difficulty**: Low
**Code Changes**: Minimal (endpoint + credentials only)

---

## Migration Scenario 2: AWS S3 → Backblaze B2

**Use Case**: Reduce storage costs (AWS $23/TB → B2 $6/TB)

**Migration Steps**:

1. **Create B2 Bucket** (5 minutes)
2. **Update Code** (10-30 minutes)
   ```python
   s3_client = boto3.client('s3',
       endpoint_url='https://s3.us-west-004.backblazeb2.com',
       aws_access_key_id=B2_KEY_ID,
       aws_secret_access_key=B2_APP_KEY)
   ```

3. **Migrate Data** (variable)
   - **Tool**: rclone, B2 CLI
   - **Time**: Depends on volume

4. **Feature Compatibility Check** (30-60 minutes)
   - Test lifecycle policies (not supported via S3 API)
   - Verify tagging behavior (returns empty)
   - Check ACLs (only private/public-read)

5. **Verify & Cutover** (30-60 minutes)

**Total Time**: 2-4 hours (code/testing) + data transfer
**Difficulty**: Medium (feature gaps require testing)
**Code Changes**: Minimal (endpoint) + potential feature workarounds

---

## Migration Scenario 3: AWS S3 → MinIO (Self-Hosted)

**Use Case**: Data sovereignty, cost savings at large scale

**Migration Steps**:

1. **Deploy MinIO** (2-8 hours)
   - Provision servers/VMs
   - Install MinIO (Docker or binary)
   - Configure erasure coding/replication
   - Set up load balancer (if distributed)

2. **Update Code** (10-30 minutes)
   ```python
   s3_client = boto3.client('s3',
       endpoint_url='http://minio.internal.example.com:9000',
       aws_access_key_id=MINIO_ACCESS_KEY,
       aws_secret_access_key=MINIO_SECRET_KEY)
   ```

3. **Migrate Data** (variable)
   - **Tool**: `mc` (MinIO Client), rclone, or s3cmd
   - **Time**: Network and volume dependent

4. **Configure Replication/Backup** (1-2 hours)
   - Set up erasure coding (if not done in setup)
   - Configure backups
   - Implement monitoring

5. **Verify & Cutover** (1-2 hours)

**Total Time**: 4-12 hours (infrastructure + code) + data transfer
**Difficulty**: High (infrastructure management required)
**Code Changes**: Minimal (endpoint only)

---

## Migration Time Estimates

| From → To | Setup | Code | Data | Total (Excluding Data) |
|-----------|-------|------|------|------------------------|
| **S3 → R2** | 5 min | 15 min | Variable | 1-2 hours |
| **S3 → B2** | 5 min | 30 min | Variable | 2-4 hours |
| **S3 → MinIO** | 2-8 hrs | 30 min | Variable | 4-12 hours |
| **S3 → Wasabi** | 5 min | 15 min | Variable | 1-2 hours |
| **R2 → B2** | 5 min | 15 min | Variable | 1-2 hours |
| **B2 → MinIO** | 2-8 hrs | 15 min | Variable | 3-10 hours |

**Data Transfer Time** (separate from above):
- 100 GB: 5-30 minutes (depending on bandwidth)
- 1 TB: 1-4 hours
- 10 TB: 10-40 hours
- 100 TB: Days to weeks

---

## Key Findings

1. **Endpoint-only migrations** (S3 ↔ managed providers): 1-4 hours
2. **Self-hosted setup** (MinIO, Ceph): Add 4-12 hours infrastructure time
3. **Data transfer**: Usually longer than code changes
4. **Feature testing**: Required for B2, Wasabi (2-4 hours)

**S3 API delivers on portability promise**: Code changes are minimal, setup time is predictable.
