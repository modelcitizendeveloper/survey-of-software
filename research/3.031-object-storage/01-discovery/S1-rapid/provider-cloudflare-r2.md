# Cloudflare R2 (Workers Object Storage)

**Provider Type**: S3-Compatible Alternative (Zero Egress)
**S3 API Compatibility**: ~90% (documented differences)
**Date**: 2025-10-16

---

## Pricing

### Storage
- **Standard**: $0.015/GB/month
- **Infrequent Access**: $0.01/GB/month (30-day minimum storage, $0.01/GB retrieval fee)

### Egress (Data Transfer Out)
- **To Internet**: **$0.00 (FREE)** ← Key differentiator
- **Ingress (upload)**: Free

### Request Pricing
- **Class A (writes)**: $4.50 per million requests (Standard), $9.00/million (Infrequent)
- **Class B (reads)**: $0.36 per million requests (Standard), $0.90/million (Infrequent)

### Free Tier (Monthly, ongoing)
- **Storage**: 10GB
- **Class A operations**: 1 million per month
- **Class B operations**: 10 million per month
- **Egress**: Unlimited free

---

## Key Features

### Strengths ✅
- **Zero egress fees**: Eliminates largest AWS S3 cost component
- **Global network**: Cloudflare's 300+ edge locations
- **R2 + Workers integration**: Serverless compute directly at the edge
- **Predictable pricing**: No surprise egress bills
- **Good free tier**: 10GB storage + operations, suitable for small projects

### Weaknesses ⚠️
- **Newer service**: Launched 2022 (3 years old vs AWS S3's 19 years)
- **S3 API gaps**: ~90% compatible, some features missing (see compatibility notes)
- **Limited storage classes**: Only Standard and Infrequent Access (no archive tiers)
- **No regions selection**: Data stored in Cloudflare's distributed network (less control)

---

## S3 API Compatibility Notes

**Supported** ✅:
- Core CRUD operations (PUT, GET, DELETE, LIST)
- Multipart uploads
- Presigned URLs
- Object metadata
- Lifecycle policies

**Not Supported** ❌:
- Object Lock (WORM)
- Server-side encryption with customer keys (SSE-C)
- S3 Select
- Batch operations
- Some ACL operations

**Documentation**: Cloudflare publishes official compatibility list

---

## Best For

**✅ Ideal Use Cases**:
- High-egress workloads (video streaming, software downloads, public assets)
- Static website hosting
- CDN origin storage
- User-generated content delivery
- Cost-sensitive projects with global audience

**❌ Not Ideal For**:
- Compliance requiring specific geographic data residency
- Apps requiring 100% S3 API compatibility
- Long-term archive storage (no Glacier-equivalent tier)

---

## Differentiators

1. **Zero Egress**: Only major provider with truly free egress (no caps or conditions)
2. **Edge Integration**: Tight integration with Cloudflare Workers (serverless at edge)
3. **Network Effect**: Leverage Cloudflare's global CDN infrastructure
4. **Predictable Costs**: Storage + operations only, no egress surprises

---

## Cost Example (100TB storage + 200TB egress/month)

- Storage (100TB × $0.015): **$1,500**
- Egress (200TB × $0.00): **$0**
- Requests (assume 10M Class B): $3.60

**Monthly Total: ~$1,504**

**Savings vs AWS S3**: $17,150 - $1,504 = **$15,646/month (91% cheaper)**

---

## Quick Assessment

**Market Position**: 🆕 Challenger (launched 2022), backed by Cloudflare
**Cost**: 💰 Very low (especially high-egress scenarios)
**Features**: ⭐⭐⭐ Good core features, missing some advanced AWS features
**Portability**: ✅ High (S3-compatible with documented differences)
**Maturity**: ⚠️ Young (3 years), but Cloudflare-backed

**Bottom Line**: R2 is a game-changer for egress-heavy workloads, offering 90%+ cost savings vs AWS S3 for content delivery scenarios. Trade-off is newer service with some S3 API gaps. If your workload fits within supported features, savings are massive.
