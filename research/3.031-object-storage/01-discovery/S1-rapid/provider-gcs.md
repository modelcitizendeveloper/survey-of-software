# Google Cloud Storage (GCS)

**Provider Type**: Major Cloud Provider (Google Ecosystem)
**S3 API Compatibility**: Partial (interoperability API available, but not primary)
**Date**: 2025-10-16

---

## Pricing (US Multi-Region)

### Storage Classes
- **Standard**: $0.020/GB/month
- **Nearline**: $0.015/GB/month (30-day minimum, $0.01/GB retrieval)
- **Coldline**: $0.007/GB/month (90-day minimum, $0.02/GB retrieval)
- **Archive**: $0.0012/GB/month (365-day minimum, $0.05/GB retrieval)

**Note**: Regional storage is cheaper (Standard: $0.020 → region-specific pricing)

### Egress (Data Transfer Out)
- **First 1TB/month (aggregate across all GCP services)**: Free
- **To Internet**: Tiered pricing, varies by destination
  - North America/Europe: ~$0.085/GB (similar to AWS)
  - Volume discounts available

### Operations Pricing
- **Class A (writes)**: $0.05 per 10,000 operations
- **Class B (reads)**: $0.004 per 10,000 operations

---

## Key Features

### Strengths ✅
- **Google ecosystem**: Native integration with BigQuery, AI/ML services, GKE
- **Analytics integration**: Best-in-class data lake/analytics capabilities
- **Multiple storage classes**: 4 classes for cost optimization
- **Global network**: Google's private fiber network (low latency)
- **Object lifecycle management**: Automatic tiering based on access patterns
- **Strong consistency**: All operations (unlike eventual consistency in some providers)

### Weaknesses ⚠️
- **Limited S3 compatibility**: Interoperability API exists but not 100% compatible
- **Lock-in**: Migration requires code changes (GCS API != S3 API)
- **Egress costs**: Comparable to AWS/Azure (~$0.085/GB)
- **Complex pricing**: Multiple dimensions (storage class, location type, operations)

---

## S3 API Compatibility Notes

**GCS offers "S3 Interoperability"**:
- Allows S3 tools (boto3, s3cmd) to work with GCS via compatibility layer
- **Compatibility level**: ~70-80% (basic operations work, advanced features don't)
- **Not recommended**: Google recommends native GCS API for production use
- **Better approach**: Use Google Cloud Storage client libraries

**Portability Impact**: ⚠️ **MEDIUM**
Partial S3 compatibility means some tools work, but full migration requires code changes

---

## Best For

**✅ Ideal Use Cases**:
- Google Cloud-native applications (GKE, Cloud Run, Cloud Functions)
- Data analytics workloads (BigQuery integration)
- AI/ML pipelines (Vertex AI, TensorFlow integration)
- Multi-region applications (strong global network)
- Organizations using Google Workspace (unified ecosystem)

**❌ Not Ideal For**:
- S3 API portability requirements (use true S3-compatible providers)
- High-egress workloads (expensive like AWS)
- Small teams without GCP expertise
- Cost-sensitive projects (similar pricing to AWS/Azure)

---

## Differentiators

1. **Analytics Leader**: Best integration with data analytics (BigQuery, Dataflow, Dataproc)
2. **AI/ML Integration**: First-class ML pipeline support (Vertex AI, AutoML)
3. **Global Network**: Google's private fiber for low-latency access
4. **Strong Consistency**: All operations strongly consistent (not eventual)
5. **Object Versioning**: Built-in versioning with lifecycle policies

---

## Cost Example (100TB storage + 200TB egress/month)

**Using Standard Storage**:
- Storage (100TB × $0.020): **$2,000**
- Egress (200TB):
  - First 1TB × $0.00 = $0
  - Remaining 199TB × ~$0.085 ≈ $16,915
  - **Total egress: ~$16,915**
- Operations: ~$50

**Monthly Total: ~$18,965**

**Comparison**:
- AWS S3: ~$17,150
- Azure Blob: ~$16,540
- GCS: ~$18,965

**Note**: GCS is slightly more expensive than AWS/Azure for this workload

---

## Quick Assessment

**Market Position**: 🏆 #3 cloud provider, analytics/ML leader
**Cost**: 💰💰💰 Expensive (comparable to AWS/Azure)
**Features**: ⭐⭐⭐⭐⭐ Excellent analytics/ML integration
**Portability**: ⚠️ Medium (limited S3 compatibility)
**Maturity**: ✅ 10+ years in production

**Bottom Line**: Google Cloud Storage is the best choice for data analytics and AI/ML workloads in the Google ecosystem. Pricing is similar to AWS/Azure, and lock-in is moderate due to limited S3 compatibility. Choose GCS for BigQuery integration, AI/ML pipelines, or if you're already invested in Google Cloud—not for portability or cost savings.
