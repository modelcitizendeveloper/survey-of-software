# Backblaze B2 Cloud Storage

**Provider Type**: S3-Compatible Alternative (Low Cost)
**S3 API Compatibility**: ~90% (native B2 API + S3-compatible API)
**Date**: 2025-10-16

---

## Pricing

### Storage
- **Standard (Pay-as-you-go)**: $6.00/TB/month ($0.006/GB/month)
- **B2 Overdrive (High Performance)**: $15.00/TB/month (1 Tbps sustained throughput)

### Egress (Data Transfer Out)
- **Free egress**: Up to 3× average monthly storage
  - Example: 100TB storage → 300TB/month free egress
- **Overage**: $0.01/GB (for egress beyond 3× storage)
- **Partner egress**: Unlimited free egress through CDN partners (Cloudflare, Fastly, bunny.net, etc.)
- **B2 Overdrive**: Unlimited free egress to any destination

### Request Pricing
- **Class A (writes)**: Free
- **Class B (reads)**: Free (first 2,500/day), then $0.0004 per 1,000 calls
- **Class C (deletes/lists)**: Free (first 2,500/day), then $0.004 per 1,000 calls

### Free Tier (Ongoing)
- **Storage**: 10GB
- **Class A/B/C operations**: 2,500/day each (before charges apply)
- **Egress**: 1GB/day (or 3× storage rule)

---

## Key Features

### Strengths ✅
- **Lowest storage cost**: $6/TB/month (4× cheaper than AWS S3 Standard)
- **Generous egress**: 3× storage free, then only $0.01/GB
- **Partner CDN integrations**: Free unlimited egress through partners
- **Simple pricing**: No hidden fees, easy cost estimation
- **Dual API**: Native B2 API + S3-compatible API
- **Transparent**: Founder publicly shares pricing/cost rationale

### Weaknesses ⚠️
- **S3 API gaps**: ~90% compatible, some operations missing
- **Performance**: Standard tier slower than AWS S3 (Overdrive available for $15/TB)
- **Geographic coverage**: Fewer regions (US West, US East, EU Central)
- **Smaller company**: Risk compared to AWS/Azure/GCP/Cloudflare
- **90-day minimum storage**: Early deletion charges

---

## S3 API Compatibility Notes

**Supported** ✅:
- Core CRUD operations
- Multipart uploads
- Presigned URLs
- Bucket lifecycle rules
- Object metadata

**Not Supported** ❌:
- Object versioning (coming soon, per roadmap)
- Object Lock
- Some ACL operations
- S3 Select
- Event notifications (limited)

**Recommendation**: Use native B2 API for full features, S3 API for portability

---

## Best For

**✅ Ideal Use Cases**:
- Backup and archive (lowest cost storage)
- Media storage with CDN delivery (partner integrations)
- Cost-sensitive large-volume storage
- Application file storage (if S3 compatibility suffices)
- Disaster recovery storage

**❌ Not Ideal For**:
- Ultra-low latency requirements (unless using Overdrive)
- Apps requiring 100% S3 API compatibility
- Enterprise compliance (smaller vendor, fewer certifications)

---

## Differentiators

1. **Cheapest Storage**: $6/TB is industry-leading for standard storage
2. **3× Egress Rule**: Store 100TB, download 300TB/month free
3. **CDN Partner Network**: Free unlimited egress through 10+ CDN partners
4. **Transparency**: Public pricing philosophy, no hidden fees
5. **Backup-focused**: Tight integration with backup tools (Veeam, MSP360, etc.)

---

## Cost Example (100TB storage + 200TB egress/month)

**Scenario 1: Direct egress (without CDN partner)**
- Storage (100TB × $6): **$600**
- Egress:
  - First 300TB (3× 100TB): **$0**
  - Overage: 0TB (200TB < 300TB free)
- Requests: ~$0 (generous free tier)

**Monthly Total: $600**

**Scenario 2: Using CDN partner (Cloudflare/Fastly)**
- Storage: **$600**
- Egress (via partner): **$0**
- CDN fees: Varies by partner

**Monthly Total: $600 + CDN fees**

**Savings vs AWS S3**: $17,150 - $600 = **$16,550/month (96% cheaper)**

---

## Quick Assessment

**Market Position**: 🥇 Cost leader for storage
**Cost**: 💰 Lowest (especially with 3× egress rule)
**Features**: ⭐⭐⭐ Solid core features, some gaps vs AWS
**Portability**: ✅ High (dual API: native B2 + S3-compatible)
**Maturity**: ✅ 10+ years in business (launched 2015)

**Bottom Line**: Backblaze B2 offers the best price-to-performance for backup, archive, and large-volume storage. If you can work within S3 API limitations or use native B2 API, savings are extreme (96% vs AWS for many workloads). Perfect for cost-conscious teams willing to trade some features for massive savings.
