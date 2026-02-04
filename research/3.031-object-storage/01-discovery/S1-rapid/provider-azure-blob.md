# Azure Blob Storage

**Provider Type**: Major Cloud Provider (Microsoft Ecosystem)
**S3 API Compatibility**: Not applicable (native Azure Blob API, not S3-compatible)
**Date**: 2025-10-16

---

## Pricing (Pay-as-you-go, US regions)

### Storage Tiers
- **Hot**: $0.018/GB/month (first 50TB)
- **Cool**: $0.010/GB/month (30-day minimum storage)
- **Cold**: $0.0036/GB/month (90-day minimum storage)
- **Archive**: $0.00099/GB/month (180-day minimum storage)

**Note**: Prices decrease with volume (>500TB consumption)

### Data Retrieval Fees
- **Hot/Cool**: Free
- **Cold**: $0.0369/GB
- **Archive**: $0.02/GB (high-priority retrieval)

### Egress (Data Transfer Out)
- **First 100GB/month**: Free
- **Next 10TB/month**: ~$0.087/GB
- **Next 40TB**: ~$0.083/GB
- **Volume discounts**: Continue to decrease

### Operations Pricing
- **Write operations**: $0.05 per 10,000 (Hot), $0.10 per 10,000 (Cool/Cold)
- **Read operations**: $0.004 per 10,000 (Hot), $0.01 per 10,000 (Cool/Cold)

---

## Key Features

### Strengths ✅
- **Microsoft ecosystem**: Native integration with Azure services (VMs, Functions, App Service)
- **Multiple access tiers**: 4 tiers optimize cost vs access patterns
- **Enterprise features**: AD integration, RBAC, encryption, compliance
- **Global presence**: 60+ Azure regions worldwide
- **Reserved capacity**: 1-3 year commitments for 30-50% savings
- **Mature service**: Part of Azure since 2010

### Weaknesses ⚠️
- **NOT S3-compatible**: Requires Azure SDK (no S3 API compatibility)
- **Lock-in**: Migration from Azure Blob requires application code changes
- **Complex pricing**: Multiple tiers, early deletion charges, retrieval fees
- **Egress costs**: Similar to AWS ($0.087/GB), expensive for high-volume downloads

---

## Azure Blob API vs S3 API

**Key Differences**:
- Different SDKs: Azure SDK vs boto3/AWS SDK
- Different terminology: Containers (Azure) vs Buckets (S3)
- Different authentication: Azure AD/SAS tokens vs AWS IAM/signatures
- Different features: Append blobs, page blobs (Azure-specific)

**Portability Impact**: 🔴 **LOW**
Migrating to/from Azure Blob requires code changes (not drop-in S3 replacement)

---

## Best For

**✅ Ideal Use Cases**:
- Azure-native applications (.NET, Azure Functions, VMs)
- Microsoft/Windows environments (AD integration, RBAC)
- Enterprise compliance (Azure compliance certifications)
- Long-term archive (competitive Archive tier pricing)
- Applications already using Azure services

**❌ Not Ideal For**:
- Multi-cloud portability (S3 API required)
- High-egress workloads (expensive like AWS)
- Teams without Azure/Microsoft expertise
- Projects requiring S3 ecosystem tools

---

## Differentiators

1. **Microsoft Ecosystem**: First-class Azure integration (AD, RBAC, Azure services)
2. **Tiering Flexibility**: 4 tiers with auto-tiering policies
3. **Enterprise-Ready**: Strong compliance, governance, hybrid cloud support
4. **Reserved Capacity**: Significant savings (30-50%) with commitments
5. **Append/Page Blobs**: Unique blob types for specific workloads (not in S3)

---

## Cost Example (100TB storage + 200TB egress/month)

**Using Hot Tier**:
- Storage (100TB × $0.018): **$1,800**
- Egress (200TB):
  - First 100GB × $0.00 = $0
  - Next 10TB × $0.087 ≈ $870
  - Next 40TB × $0.083 ≈ $3,320
  - Next 100TB × $0.07 ≈ $7,000
  - Next ~50TB × $0.07 ≈ $3,500
  - **Total egress: ~$14,690**
- Operations: ~$50

**Monthly Total: ~$16,540**

**Comparison to AWS S3**: Similar (~$17,150 for AWS)

---

## Quick Assessment

**Market Position**: 🏆 #2 cloud provider, Microsoft ecosystem leader
**Cost**: 💰💰💰 Expensive (comparable to AWS)
**Features**: ⭐⭐⭐⭐⭐ Comprehensive Azure integration
**Portability**: 🔴 Low (proprietary API, not S3-compatible)
**Maturity**: ✅ 15+ years in production

**Bottom Line**: Azure Blob is the right choice if you're in the Microsoft/Azure ecosystem. Pricing is similar to AWS S3, but lock-in is higher due to non-S3-compatible API. Don't choose Azure Blob for portability—choose it for Azure ecosystem integration and Microsoft enterprise features.
