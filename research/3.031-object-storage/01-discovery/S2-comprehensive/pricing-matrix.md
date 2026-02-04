# S2: Comprehensive Pricing Matrix

**Date**: 2025-10-16
**Methodology**: S2 - Comprehensive Analysis
**Purpose**: Detailed cost comparison across volume tiers and usage patterns

---

## Storage Pricing Comparison

### Standard / Hot Storage ($/TB/month)

| Provider | Pricing Tier | $/TB/month | Notes |
|----------|-------------|------------|-------|
| **Backblaze B2** | All volumes | $6.00 | Flat rate, 1TB minimum |
| **Cloudflare R2** | All volumes | $15.00 | Flat rate |
| **Wasabi** | All volumes | $6.99 | Flat rate, 1TB minimum, 90-day minimum |
| **AWS S3 Standard** | First 50TB | $23.00 | Decreases with volume |
| **AWS S3 Standard** | 50-500TB | $22.00 | Volume discount |
| **AWS S3 Standard** | >500TB | $21.00 | Further discount |
| **Azure Blob Hot** | First 50TB | $18.00 | Decreases with volume |
| **Azure Blob Hot** | >500TB | $16.60 | Volume discount |
| **Google Cloud Storage** | Standard (multi-region) | $20.00 | Flat rate for multi-region |
| **Google Cloud Storage** | Standard (regional) | $20.00 | Regional pricing |
| **DigitalOcean Spaces** | All volumes | $20.00 | $0.02/GB after 250GB bundle |

**Winner**: Backblaze B2 ($6/TB) - 70% cheaper than next closest

---

### Cool / Infrequent Access Storage ($/TB/month)

| Provider | Storage Class | $/TB/month | Minimum Storage | Retrieval Fee |
|----------|---------------|------------|-----------------|---------------|
| **Cloudflare R2** | Infrequent Access | $10.00 | 30 days | $10.00/TB |
| **AWS S3** | Standard-IA | $12.50 | 30 days | $10.00/TB |
| **Azure Blob** | Cool | $10.00 | 30 days | Free |
| **Google Cloud Storage** | Nearline | $15.00 | 30 days | $10.00/TB |

**Winner**: Azure Blob Cool ($10/TB, free retrieval) or Cloudflare R2 Infrequent ($10/TB)

---

### Cold / Archive Storage ($/TB/month)

| Provider | Storage Class | $/TB/month | Minimum Storage | Retrieval Fee | Retrieval Time |
|----------|---------------|------------|-----------------|---------------|----------------|
| **AWS S3** | Glacier Deep Archive | $0.99 | 180 days | $20.00/TB | 12-48 hours |
| **AWS S3** | Glacier Flexible | $3.60 | 90 days | $20.00-$90/TB | 1-12 hours |
| **Azure Blob** | Archive | $0.99 | 180 days | $20.00/TB | Hours |
| **Azure Blob** | Cold | $3.60 | 90 days | $36.90/TB | — |
| **Google Cloud Storage** | Archive | $1.20 | 365 days | $50.00/TB | — |
| **Google Cloud Storage** | Coldline | $7.00 | 90 days | $20.00/TB | — |
| **DigitalOcean Spaces** | Cold Storage | $7.00 | — | Free (1×/month) | — |

**Winner**: AWS S3 Glacier Deep Archive & Azure Blob Archive (tied at $0.99/TB)

**Note**: Backblaze B2, Cloudflare R2, Wasabi do NOT offer archive tiers

---

## Egress (Data Transfer Out) Pricing

### Egress to Internet ($/GB)

| Provider | Volume Tier | $/GB | Monthly Cap/Limits |
|----------|-------------|------|--------------------|
| **Cloudflare R2** | All volumes | **$0.00** | Unlimited free |
| **Backblaze B2** | Within 3× storage | **$0.00** | 3× average monthly storage |
| **Backblaze B2** | Overage | $0.01 | After 3× limit |
| **Backblaze B2** | Via CDN partners | **$0.00** | Unlimited (Cloudflare, Fastly, etc.) |
| **Wasabi** | Within 1× storage | **$0.00** | Up to 1× monthly storage (fair-use) |
| **Wasabi** | Overage | Suspend | Service may be limited/suspended |
| **DigitalOcean Spaces** | First 1TB | **$0.00** | Included in $5 base |
| **DigitalOcean Spaces** | Overage | $0.01 | After 1TB/month |
| **AWS S3** | First 10TB | $0.09 | Volume discounts apply |
| **AWS S3** | 10-50TB | $0.085 | Decreasing rate |
| **AWS S3** | 50-150TB | $0.07 | Further discount |
| **AWS S3** | >150TB | $0.05 | Best rate |
| **Azure Blob** | First 10TB | $0.087 | Similar to AWS |
| **Azure Blob** | 10-50TB | $0.083 | Volume discounts |
| **Google Cloud Storage** | First 1TB | **$0.00** | Free tier (aggregate across GCP) |
| **Google Cloud Storage** | 1TB+ | $0.085 | Similar to AWS/Azure |

**Winner**: Cloudflare R2 (truly unlimited free) > Backblaze B2 (3× free) > Wasabi (1× free, but risky)

---

## Request Pricing

### Write Operations (PUT/POST/COPY) per Million Requests

| Provider | Cost per Million | Notes |
|----------|------------------|-------|
| **Backblaze B2** | $0.00 | Class A: Free |
| **Wasabi** | $0.00 | Free (fair-use applies) |
| **DigitalOcean Spaces** | Included | No separate charge |
| **Cloudflare R2** | $4.50 | Standard storage |
| **AWS S3** | $5.00 | Standard storage |
| **Azure Blob** | $5.00 | Hot tier |
| **Google Cloud Storage** | $5.00 | Class A operations |

**Winner**: Backblaze B2 & Wasabi (free writes)

---

### Read Operations (GET/LIST) per Million Requests

| Provider | Cost per Million | Notes |
|----------|------------------|-------|
| **Backblaze B2** | $0.40 | After 2,500/day free tier |
| **DigitalOcean Spaces** | Included | No separate charge |
| **Cloudflare R2** | $0.36 | Standard storage |
| **AWS S3** | $0.40 | Standard storage |
| **Azure Blob** | $0.40 | Hot tier |
| **Google Cloud Storage** | $0.40 | Class B operations |
| **Wasabi** | $0.00 | Free (fair-use applies) |

**Winner**: Wasabi (free) > DigitalOcean (included) > Cloudflare R2 ($0.36)

---

## Cost Modeling: 5 Common Scenarios

### Scenario 1: Small Website (10GB storage, 500GB egress/month)

| Provider | Storage | Egress | Requests | Total | Notes |
|----------|---------|--------|----------|-------|-------|
| **DigitalOcean** | — | — | — | **$5.00** | Within $5 bundle |
| **Cloudflare R2** | $0.15 | $0.00 | ~$0.05 | **$0.20** | Or free (10GB tier) |
| **Backblaze B2** | $0.06 | $0.00 | $0.00 | **$0.06** | Or free (10GB tier) |
| **AWS S3** | $0.23 | $45.00 | $0.05 | **$45.28** | Egress dominates |
| **Azure Blob** | $0.18 | $43.50 | $0.05 | **$43.73** | Similar to AWS |

**Winner**: Cloudflare R2 or Backblaze B2 (free tiers), then DigitalOcean ($5 with CDN)

---

### Scenario 2: Backup Storage (100TB storage, 5TB egress/month)

| Provider | Storage | Egress | Total | Notes |
|----------|---------|--------|-------|-------|
| **Backblaze B2** | $600 | $0 | **$600** | 5TB < 300TB free (3× rule) |
| **Wasabi** | $699 | $0 | **$699** | 5TB < 100TB (within 1× limit) |
| **Cloudflare R2** | $1,500 | $0 | **$1,500** | Zero egress |
| **AWS S3 Standard** | $2,300 | $450 | **$2,750** | Egress: 5TB × $0.09 |
| **AWS Glacier Deep** | $99 | $450 | **$549** | But retrieval time 12-48hr |
| **Azure Blob Cool** | $1,000 | $435 | **$1,435** | Cool tier appropriate |

**Winner**: Backblaze B2 ($600) - purpose-built for backup

---

### Scenario 3: Video Streaming (100TB storage, 500TB egress/month)

| Provider | Storage | Egress | Total | Notes |
|----------|---------|--------|-------|-------|
| **Cloudflare R2** | $1,500 | $0 | **$1,500** | Zero egress wins |
| **Backblaze B2** | $600 | $2,000 | **$2,600** | Overage: 200TB × $0.01 (500-300) |
| **Backblaze + CDN** | $600 | $0 | **$600** + CDN | Via partner (Cloudflare/Fastly) |
| **Wasabi** | $699 | RISK | **RISK** | 500TB exceeds 1× limit → suspend |
| **AWS S3** | $2,300 | $43,150 | **$45,450** | Egress catastrophic |
| **Azure Blob** | $1,800 | $42,650 | **$44,450** | Similar to AWS |

**Winner**: Backblaze B2 + CDN partner ($600) or Cloudflare R2 ($1,500)

---

### Scenario 4: App User Files (10TB storage, 10TB egress/month)

| Provider | Storage | Egress | Total | Notes |
|----------|---------|--------|-------|-------|
| **Backblaze B2** | $60 | $0 | **$60** | Within 3× limit (30TB free) |
| **Wasabi** | $69.90 | $0 | **$69.90** | Within 1× limit |
| **Cloudflare R2** | $150 | $0 | **$150** | Zero egress |
| **DigitalOcean** | $200 | $90 | **$290** | 10TB storage overage + egress |
| **AWS S3** | $230 | $900 | **$1,130** | Expensive egress |

**Winner**: Backblaze B2 ($60) - best value for balanced workloads

---

### Scenario 5: Data Lake (1PB storage, 10TB egress/month)

| Provider | Storage | Egress | Total | Notes |
|----------|---------|--------|-------|-------|
| **Backblaze B2** | $6,000 | $0 | **$6,000** | Within 3× limit (3PB free) |
| **Wasabi** | $6,990 | $0 | **$6,990** | Within 1× limit |
| **Cloudflare R2** | $15,000 | $0 | **$15,000** | Zero egress |
| **AWS S3 Standard** | $23,000 | $900 | **$23,900** | Volume discount (>500TB) |
| **Azure Blob Hot** | $18,000 | $870 | **$18,870** | Similar to AWS |
| **GCS Standard** | $20,000 | $765 | **$20,765** | Free first 1TB egress |

**Winner**: Backblaze B2 ($6,000) - 4× cheaper than AWS, minimal egress

---

## Key Insights

### Cost Leaders by Category

**Cheapest Storage**: Backblaze B2 ($6/TB) - 70% cheaper than competitors
**Cheapest Egress**: Cloudflare R2 ($0) or Backblaze B2 (3× free) - 100% savings
**Cheapest Archive**: AWS Glacier Deep Archive / Azure Blob Archive ($0.99/TB)
**Best Value Small**: DigitalOcean Spaces ($5 all-in) or Cloudflare R2 (10GB free)
**Best Value Large**: Backblaze B2 (96% cheaper than AWS for most workloads)

### When to Pay More for AWS/Azure/GCS

**Ecosystem Integration**: Lambda/Functions triggers, native analytics (Athena/BigQuery)
**Advanced Features**: Object Lambda, S3 Select, Batch Operations
**Enterprise Compliance**: Extensive certifications, governance tools
**Global Performance**: Lowest latency in all regions

**Cost Premium**: 3-30× more expensive depending on workload

---

## Pricing Trends (2023-2025)

**Increasing**:
- Wasabi: $5.99 → $6.99 (+17% in 2023)
- AWS S3: Gradual increases over time

**Stable**:
- Backblaze B2: $6/TB (unchanged since 2020)
- Azure Blob: Stable pricing
- GCS: Stable pricing

**Decreasing**:
- Cloudflare R2: New entrant, competitive pricing pressure

**Outlook**: Expect continued price competition in S3-compatible alternatives, stability in major cloud providers.
