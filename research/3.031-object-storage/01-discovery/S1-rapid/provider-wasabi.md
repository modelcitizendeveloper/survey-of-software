# Wasabi Hot Cloud Storage

**Provider Type**: S3-Compatible Alternative (Flat Pricing)
**S3 API Compatibility**: ~95% (high compatibility)
**Date**: 2025-10-16

---

## Pricing

### Storage
- **Hot Cloud Storage**: $6.99/TB/month (increased from $5.99 in June 2023)
- **Minimum charge**: 1TB (even if storing less)
- **Minimum storage duration**: 90 days (early deletion charged for remaining days)

### Egress (Data Transfer Out)
- **"Free egress"*** with conditions:
  - Free if monthly egress ≤ monthly active storage
  - Example: 100TB storage → 100TB/month free egress
  - If egress > storage, Wasabi reserves right to limit/suspend service
- **Overage**: No per-GB charge, but service may be limited/suspended

**⚠️ Important**: This is a **fair-use policy**, not unlimited free egress

### Request Pricing
- **All API requests**: Free (with "reasonable" usage)
- **Unreasonable loads**: Wasabi reserves right to limit/suspend service

### Free Tier
- ❌ **No free tier** (1TB minimum charge applies)

---

## Key Features

### Strengths ✅
- **Simple pricing**: One flat rate ($6.99/TB), no complex tiers
- **High S3 compatibility**: ~95% compatible (better than many alternatives)
- **Fast performance**: Advertised as faster than AWS S3
- **No retrieval fees**: Unlike archive tiers, all data is "hot" (immediately accessible)
- **Immutability features**: Object lock, versioning for compliance

### Weaknesses ⚠️
- **1TB minimum**: Small projects pay for 1TB even if storing 10GB
- **90-day minimum storage**: Early deletion penalties
- **Egress restrictions**: "Free" egress is conditional (must be ≤ storage volume)
- **Service suspension risk**: Exceeding fair-use limits may suspend account
- **Single storage class**: No archive tier for cost optimization
- **Recent price increase**: 17% increase in 2023 ($5.99 → $6.99)

---

## S3 API Compatibility Notes

**Supported** ✅:
- Core CRUD operations
- Multipart uploads
- Presigned URLs
- Bucket policies
- Object versioning
- Object Lock (WORM)
- Lifecycle policies

**Not Supported** ❌:
- S3 Select
- Some advanced ACL operations
- Glacier/Archive tiers (Wasabi is hot storage only)

**Compatibility Level**: ~95% (among highest for S3 alternatives)

---

## Best For

**✅ Ideal Use Cases**:
- Active data storage (not archive)
- Balanced read/write workloads (egress ≈ storage volume)
- Compliance requiring immutability (Object Lock support)
- Teams wanting simple, predictable pricing
- Minimum 1TB storage needs

**❌ Not Ideal For**:
- Small projects (<1TB due to minimum)
- High-egress workloads (>1× storage/month risks suspension)
- Archive/infrequent access (no cold tiers)
- Cost-sensitive projects (B2 is cheaper at $6/TB vs $6.99/TB)

---

## Differentiators

1. **Flat Pricing**: One simple rate, no tiers or complex calculations
2. **High S3 Compatibility**: 95% compatible (better than R2, B2)
3. **Performance**: Advertises faster speeds than AWS S3
4. **Immutability Features**: Strong compliance features (Object Lock)
5. **Simplicity**: Easy to predict costs (if within fair-use limits)

---

## Pricing Reality Check ⚠️

**Advertised**: "Free egress"
**Reality**: Free if egress ≤ storage volume, service may be suspended otherwise

**Comparison**:
- **Backblaze B2**: 3× storage free egress (100TB storage → 300TB egress)
- **Wasabi**: 1× storage free egress (100TB storage → 100TB egress, then risk suspension)
- **Cloudflare R2**: Truly unlimited free egress

**Verdict**: Wasabi's "free egress" is more restrictive than B2 or R2

---

## Cost Example (100TB storage + 200TB egress/month)

**Scenario 1: Within egress limits (100TB egress)**
- Storage (100TB × $6.99): **$699**
- Egress (100TB, within 1× limit): **$0**
- Requests: **$0**

**Monthly Total: $699**

**Scenario 2: Exceeds egress limits (200TB egress)**
- Storage: **$699**
- Egress: **$0** (but account at risk of suspension due to 2× storage ratio)

**⚠️ Risk**: 200TB egress on 100TB storage violates fair-use policy

**Alternative**: Use Backblaze B2 (allows 3× = 300TB free egress)

---

## Quick Assessment

**Market Position**: 🥈 S3 alternative, flat pricing niche
**Cost**: 💰 Low for balanced workloads, risky for high-egress
**Features**: ⭐⭐⭐⭐ High S3 compatibility, good compliance features
**Portability**: ✅ High (95% S3-compatible)
**Maturity**: ✅ 8 years in business (launched 2017)

**Bottom Line**: Wasabi offers simple flat pricing and high S3 compatibility, but "free egress" comes with significant restrictions. If your egress ≤ storage volume, it's competitive. For high-egress workloads, Backblaze B2 (3× rule) or Cloudflare R2 (unlimited) are better choices. The 1TB minimum makes it unsuitable for small projects.
