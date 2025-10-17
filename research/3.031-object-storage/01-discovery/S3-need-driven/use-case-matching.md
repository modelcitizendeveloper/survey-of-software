# S3: Use Case → Provider Matching

**Date**: 2025-10-16
**Methodology**: S3 - Need-Driven Analysis
**Purpose**: Map specific use cases and requirements to optimal providers

---

## Use Case Taxonomy

### By Access Pattern
1. **High Egress** (downloads >> uploads)
2. **Balanced Access** (reads ≈ writes)
3. **Infrequent Access** (archive, backup)
4. **Write-Heavy** (log aggregation, IoT data)

### By Scale
5. **Small (<1TB)**
6. **Medium (1-100TB)**
7. **Large (100TB-1PB)**
8. **Massive (>1PB)**

### By Requirements
9. **Cost-Sensitive**
10. **Compliance-Driven**
11. **Performance-Critical**
12. **Ecosystem Integration**

---

## 1. Video Streaming / Content Delivery

### Characteristics
- **Access Pattern**: Very high egress (10-100× storage volume)
- **Scale**: Medium to large (10TB-500TB)
- **Performance**: Medium latency acceptable (CDN helps)
- **Compliance**: Minimal

### Cost Analysis (100TB storage, 1PB egress/month)

| Provider | Cost | Calculation |
|----------|------|-------------|
| **Cloudflare R2** | $1,500 | Storage only ($15/TB × 100TB) |
| **Backblaze B2 + CDN** | $600-1,000 | Storage $600 + CDN fees |
| **AWS S3** | $87,300 | $2,300 storage + $85,000 egress |
| **Azure Blob** | $85,800 | Similar to AWS |

**Recommended**:
1. **Cloudflare R2** (best) - $1,500/mo, zero egress
2. **Backblaze B2 + CDN partner** (budget) - $600-1,000/mo, unlimited egress via partner

**Avoid**: AWS S3, Azure Blob, GCS (egress costs $85K+/mo)

**Implementation**:
```
Option 1: Cloudflare R2
- Store videos in R2 buckets
- Serve directly from R2 (edge network)
- Use Cloudflare Workers for authentication/transformation
- Cost: $1,500/mo

Option 2: Backblaze B2 + Cloudflare/Fastly CDN
- Store videos in B2 buckets
- Pull zone via Cloudflare/Fastly (partner = free egress)
- CDN edge caching
- Cost: $600 B2 + CDN fees
```

---

## 2. Backup & Disaster Recovery

### Characteristics
- **Access Pattern**: Infrequent access (restore events rare)
- **Scale**: Large (100TB-10PB typical)
- **Performance**: Restore time flexible (hours acceptable)
- **Compliance**: HIPAA/SOC2 often required

### Cost Analysis (500TB backup, 5TB monthly restore)

| Provider | Cost | Calculation |
|----------|------|-------------|
| **Backblaze B2** | $3,000 | $6/TB × 500TB, 5TB < 1,500TB free egress |
| **Wasabi** | $3,495 | $6.99/TB × 500TB |
| **AWS Glacier Deep** | $495 | $0.99/TB × 500TB (but $100+ retrieval fees) |
| **Cloudflare R2** | $7,500 | $15/TB × 500TB |
| **AWS S3 Standard** | $11,500 | $23/TB × 500TB |

**Recommended**:
1. **Backblaze B2** (best value) - $3,000/mo, fast restore, 3× free egress
2. **Wasabi** (simple pricing) - $3,495/mo, flat rate
3. **AWS Glacier Deep Archive** (ultra-low cost, but slow) - $495/mo + retrieval fees + 12-48hr wait

**Avoid**: AWS S3 Standard (expensive), Cloudflare R2 (more expensive than B2 for cold storage)

**Implementation**:
```
Backblaze B2 Backup Architecture:
1. Use backup tool integration (Veeam, MSP360, Duplicity)
2. Encrypt before upload (client-side encryption)
3. Lifecycle policy: Keep daily (30 days), weekly (12 weeks), monthly (12 months)
4. Test restores quarterly (within 3× egress allowance)
5. Cost: $3,000/mo for 500TB
```

---

## 3. Static Website / App Assets

### Characteristics
- **Access Pattern**: High read (serving JS, CSS, images)
- **Scale**: Small to medium (100GB-10TB)
- **Performance**: Low latency critical
- **Compliance**: Minimal

### Cost Analysis (1TB storage, 10TB egress/month)

| Provider | Cost | Calculation |
|----------|------|-------------|
| **Cloudflare R2** | $15 | $15/TB × 1TB storage, $0 egress |
| **DigitalOcean Spaces** | $5-105 | $5 base + overage (if >1TB egress) |
| **Backblaze B2** | $6 | $6/TB × 1TB, 10TB < 3TB free → $70 overage |
| **AWS S3 + CloudFront** | $23 + CDN | S3 $23 + CloudFront fees |

**Recommended**:
1. **Cloudflare R2** (best) - $15/mo, edge delivery, zero egress
2. **DigitalOcean Spaces** (small sites) - $5/mo if <1TB egress, includes CDN

**Implementation**:
```
Cloudflare R2 Static Site:
1. Upload assets to R2 bucket
2. Configure custom domain
3. Use Cloudflare Workers for SSR/auth (optional)
4. Automatic edge caching (300+ locations)
5. Cost: $15/mo for 1TB + unlimited egress
```

---

## 4. User-Generated Content (Photos, Documents)

### Characteristics
- **Access Pattern**: Balanced (users upload and download)
- **Scale**: Medium (1-100TB)
- **Performance**: Medium latency acceptable
- **Compliance**: GDPR/HIPAA if personal data

### Cost Analysis (10TB storage, 10TB egress/month)

| Provider | Cost | Calculation |
|----------|------|-------------|
| **Backblaze B2** | $60 | $6/TB × 10TB, 10TB < 30TB free egress |
| **Wasabi** | $70 | $7/TB × 10TB (rounded to 10TB minimum) |
| **Cloudflare R2** | $150 | $15/TB × 10TB |
| **AWS S3** | $230 + $900 = $1,130 | Storage + egress |

**Recommended**:
1. **Backblaze B2** (best value) - $60/mo, S3-compatible
2. **Cloudflare R2** (if edge performance needed) - $150/mo
3. **AWS S3** (if using Lambda triggers/AWS ecosystem) - $1,130/mo

**Implementation**:
```
Backblaze B2 UGC Storage:
1. Generate presigned upload URLs (S3 API)
2. Users upload directly to B2 (client → B2)
3. Store metadata in database (app → database)
4. Serve via CDN or presigned download URLs
5. Optional: Partner CDN for unlimited free egress
6. Cost: $60/mo for 10TB
```

---

## 5. Data Lake / Analytics

### Characteristics
- **Access Pattern**: Large writes, query-in-place
- **Scale**: Large to massive (100TB-10PB)
- **Performance**: Query performance critical
- **Compliance**: Varies (healthcare, financial, etc.)

### Provider Selection by Analytics Tool

| Analytics Tool | Best Provider | Reason |
|----------------|---------------|--------|
| **AWS Athena** | AWS S3 | Native integration, no data movement |
| **AWS EMR/Glue** | AWS S3 | Optimized for S3 |
| **Azure Synapse** | Azure Blob | Native integration |
| **Google BigQuery** | Google Cloud Storage | Best performance |
| **Databricks** | AWS S3 or Azure Blob | Cloud-specific deployment |
| **Apache Spark (self-hosted)** | Any S3-compatible (R2, B2, Wasabi) | s3a:// connector |
| **Presto/Trino** | Any S3-compatible | S3 connector |
| **Snowflake** | Any (external tables) | Multi-cloud support |

**Cost Analysis (1PB storage, 10TB egress/month)** for self-hosted Spark:

| Provider | Cost | Calculation |
|----------|------|-------------|
| **Backblaze B2** | $6,000 | $6/TB × 1,000TB, egress free (< 3PB) |
| **Wasabi** | $6,990 | $6.99/TB × 1,000TB |
| **Cloudflare R2** | $15,000 | $15/TB × 1,000TB |
| **AWS S3** | $21,000 + $900 = $21,900 | Volume discount + egress |

**Recommended**:
1. **Match your analytics platform** (Athena→S3, BigQuery→GCS)
2. **Self-hosted analytics**: Backblaze B2 ($6,000/mo for 1PB)
3. **Multi-cloud analytics**: Any S3-compatible (portability)

**Implementation**:
```
Self-Hosted Spark + Backblaze B2:
1. Configure Spark s3a connector with B2 S3-compatible endpoint
2. Partition data by date/region (s3://bucket/year=2025/month=10/day=16/)
3. Use Parquet/ORC for columnar storage (10× compression)
4. Query in place (Spark DataFrame API)
5. Cost: $6,000/mo for 1PB (4× cheaper than AWS S3)
```

---

## 6. Application Database Backups

### Characteristics
- **Access Pattern**: Infrequent (disaster recovery)
- **Scale**: Small to medium (100GB-10TB)
- **Performance**: Restore time critical (hours not acceptable)
- **Compliance**: HIPAA/SOC2 often required

### Cost Analysis (5TB backups, 500GB monthly restore)

| Provider | Cost | Calculation |
|----------|------|-------------|
| **Backblaze B2** | $30 | $6/TB × 5TB, 500GB < 15TB free egress |
| **Wasabi** | $35 | $6.99/TB × 5TB |
| **Cloudflare R2** | $75 | $15/TB × 5TB |
| **AWS S3 Standard-IA** | $62.50 + $5 = $67.50 | Storage + retrieval |
| **AWS Glacier Flexible** | $18 + $10-45 = $28-63 | Storage + retrieval ($0.02-$0.09/GB) |

**Recommended**:
1. **Backblaze B2** (best balance) - $30/mo, fast restore, HIPAA compliant
2. **Wasabi** (simple) - $35/mo, immediate access
3. **AWS Glacier Flexible** (if restore time flexible) - $28-63/mo, 1-12hr retrieval

**Avoid**: Glacier Deep Archive (12-48hr restore time), Cloudflare R2 (overkill for backups)

**Implementation**:
```
PostgreSQL/MySQL Backup to Backblaze B2:
1. Daily pg_dump/mysqldump (compressed)
2. Upload to B2 via S3 API (boto3 or aws-cli)
3. Retention: Daily (7 days), Weekly (4 weeks), Monthly (12 months)
4. Encrypt dumps before upload (GPG or pg_dump --password)
5. Test restores monthly
6. Cost: $30/mo for 5TB
```

---

## 7. Machine Learning Model Storage

### Characteristics
- **Access Pattern**: Write models, read for inference
- **Scale**: Medium (1-100TB)
- **Performance**: Fast read access for model loading
- **Compliance**: Varies

### Provider Selection by ML Platform

| ML Platform | Best Provider | Cost (10TB) |
|-------------|---------------|-------------|
| **AWS SageMaker** | AWS S3 | $230/mo (+ egress for training) |
| **Azure ML** | Azure Blob | $180/mo |
| **Google Vertex AI** | GCS | $200/mo |
| **Self-hosted (Kubernetes)** | Backblaze B2 | $60/mo |
| **Hugging Face / Cloud-agnostic** | Cloudflare R2 | $150/mo |

**Recommended**:
1. **Match your ML platform** (SageMaker→S3, Vertex AI→GCS)
2. **Self-hosted inference**: Cloudflare R2 ($150, edge inference)
3. **Cost-optimized**: Backblaze B2 ($60, S3-compatible)

**Implementation**:
```
Self-Hosted ML Model Storage (Cloudflare R2):
1. Upload trained models to R2 (versioned buckets)
2. Inference service loads models from R2 (presigned URLs)
3. Use Cloudflare Workers for edge inference (ultra-low latency)
4. Automatic global distribution (300+ edge locations)
5. Cost: $150/mo for 10TB + unlimited model downloads
```

---

## 8. Compliance-Driven (Healthcare, Finance)

### Characteristics
- **Access Pattern**: Varies
- **Scale**: Varies
- **Performance**: Varies
- **Compliance**: **CRITICAL** (HIPAA, PCI-DSS, FedRAMP)

### Provider Selection by Compliance Requirement

| Requirement | Providers | Rationale |
|-------------|-----------|-----------|
| **HIPAA only** | Cloudflare R2, Wasabi, Backblaze B2, AWS, Azure, GCS | BAA available, cost varies |
| **HIPAA + PCI-DSS** | AWS S3, Azure Blob, GCS, Cloudflare R2 | PCI-DSS Level 1 certified |
| **HIPAA + ISO 27001** | AWS, Azure, GCS, Wasabi | ISO 27001 certified |
| **FedRAMP** | AWS S3, Azure Blob, GCS | Only FedRAMP-authorized providers |
| **GDPR + EU residency** | All (choose EU region) | Ensure provider has EU regions |
| **SEC 17a-4 (WORM)** | AWS, Azure, GCS, Wasabi | Object Lock (WORM) support |

**Cost-Optimized Compliance** (HIPAA, 10TB):

| Provider | Cost | Compliance |
|----------|------|------------|
| **Backblaze B2** | $60 | HIPAA (BAA), SOC2, GDPR |
| **Wasabi** | $70 | HIPAA, SOC2, ISO 27001, GDPR |
| **Cloudflare R2** | $150 | HIPAA (BAA, Enterprise), SOC2, PCI-DSS, GDPR |
| **AWS S3** | $230 | HIPAA, PCI-DSS, ISO 27001, FedRAMP, SOC2, GDPR, 90+ more |

**Recommended**:
1. **FedRAMP required**: AWS S3, Azure Blob, or GCS (no alternatives)
2. **PCI-DSS required**: AWS, Azure, GCS, or Cloudflare R2
3. **HIPAA only**: Backblaze B2 (cheapest, $60 vs $230 AWS)
4. **WORM compliance**: AWS, Azure, GCS, or Wasabi (Object Lock)

---

## 9. Multi-Cloud / Vendor Independence

### Characteristics
- **Access Pattern**: Varies
- **Scale**: Varies
- **Performance**: Varies
- **Compliance**: Portability > specific certifications

### Portability Ranking

| Portability Priority | Providers | S3 API Compatibility |
|---------------------|-----------|---------------------|
| **Highest** | Wasabi, Cloudflare R2, Backblaze B2, DigitalOcean | 90-95% S3 compatible |
| **Medium** | Google Cloud Storage | 70-80% (interoperability layer) |
| **Low** | Azure Blob Storage | 0% (proprietary API) |
| **Lock-in Risk** | AWS S3 (if using AWS-specific features) | 100% S3, but extensions lock you in |

**Recommended**:
1. **Wasabi** (95% S3 compatible, highest portability)
2. **Cloudflare R2** (90% S3 compatible, zero egress for migrations)
3. **Backblaze B2** (90% S3 compatible, dual API)

**Avoid**: Azure Blob (proprietary API), GCS (limited S3 compatibility), AWS S3-specific features (Glacier, Object Lambda)

**Implementation**:
```
Multi-Cloud Strategy:
1. Use S3 API exclusively (avoid provider-specific features)
2. Abstract storage layer (interface/adapter pattern)
3. Test migrations annually (validate portability)
4. Use Terraform/IaC for infrastructure (portable)
5. Monitor for S3 API compatibility (95%+ required)
```

---

## 10. Cost-Sensitive Startups

### Characteristics
- **Access Pattern**: Variable (evolving product)
- **Scale**: Small to medium (<10TB)
- **Performance**: Medium acceptable
- **Compliance**: Minimal initially

### Provider Selection by Budget

**Free Tier** (0-10GB):
1. **Cloudflare R2** (10GB storage + unlimited egress, free forever)
2. **Backblaze B2** (10GB storage + 1GB/day egress, free forever)

**Budget Tier** ($5-50/month, 100GB-1TB):
1. **DigitalOcean Spaces** ($5 for 250GB + 1TB egress + CDN)
2. **Cloudflare R2** ($1.50-15 for 100GB-1TB + unlimited egress)
3. **Backblaze B2** ($0.60-6 for 100GB-1TB)

**Growth Tier** ($50-500/month, 1-10TB):
1. **Backblaze B2** ($6-60 for 1-10TB)
2. **Cloudflare R2** ($15-150 for 1-10TB, if high egress)
3. **Wasabi** ($70-699 for 10TB minimum, 1TB charged anyway)

**Recommended**:
1. **Start**: Cloudflare R2 free tier (10GB)
2. **Scale to 1TB**: DigitalOcean Spaces ($5) or Cloudflare R2 ($15)
3. **Scale beyond 1TB**: Backblaze B2 (cheapest per TB)

**Avoid**: AWS/Azure/GCS (expensive, complex billing), Wasabi (1TB minimum)

---

## Use Case Decision Matrix

| Use Case | Best Provider | Runner-Up | Avoid |
|----------|---------------|-----------|-------|
| **Video Streaming** | Cloudflare R2 | Backblaze B2 + CDN | AWS, Azure, GCS |
| **Backup / DR** | Backblaze B2 | Wasabi | AWS S3 Standard, R2 |
| **Static Website** | Cloudflare R2 | DigitalOcean Spaces | AWS S3 (expensive egress) |
| **User Content** | Backblaze B2 | Cloudflare R2 | AWS S3 (expensive) |
| **AWS Analytics** | AWS S3 | N/A | Alternatives (poor integration) |
| **Azure Analytics** | Azure Blob | N/A | Alternatives (poor integration) |
| **GCP Analytics** | GCS | N/A | Alternatives (poor integration) |
| **Self-Hosted Analytics** | Backblaze B2 | Wasabi | AWS S3 (expensive) |
| **Database Backups** | Backblaze B2 | Wasabi | Glacier Deep (slow restore) |
| **ML Models** | Match platform | Cloudflare R2 (self-hosted) | — |
| **HIPAA only** | Backblaze B2 | Wasabi, R2 | DigitalOcean (no HIPAA) |
| **FedRAMP** | AWS/Azure/GCS | N/A | All alternatives |
| **Multi-Cloud** | Wasabi | Cloudflare R2, B2 | Azure Blob (no S3 API) |
| **Startup (<1TB)** | Cloudflare R2 | DigitalOcean Spaces | AWS, Wasabi (expensive/minimum) |

---

## Key Takeaways

1. **High Egress**: Always choose Cloudflare R2 (zero egress) or Backblaze B2 (3× free)
2. **Cold Storage**: Backblaze B2 beats all others (96% cheaper than AWS S3)
3. **Analytics**: Match your analytics platform (Athena→S3, BigQuery→GCS)
4. **Compliance**: HIPAA alone doesn't require AWS/Azure (save 70-96% with B2/Wasabi/R2)
5. **Startups**: Start with Cloudflare R2 free tier, scale to B2 for storage or R2 for egress
6. **Ecosystem Lock-in**: If on AWS/Azure/GCP, native storage often makes sense
7. **Portability**: Use Wasabi/R2/B2 + stick to core S3 API for vendor independence

**Most Common Mistake**: Choosing AWS S3 by default without evaluating alternatives. For 80% of use cases, S3-compatible alternatives save 70-96% while meeting requirements.
