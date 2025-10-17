# AWS S3 (Amazon Simple Storage Service)

**Provider Type**: Major Cloud Provider (Market Leader)
**S3 API Compatibility**: 100% (reference implementation)
**Date**: 2025-10-16

---

## Pricing (US East - N. Virginia)

### Storage
- **S3 Standard**: $0.023/GB/month
- **S3 Intelligent-Tiering**: $0.023/GB/month (frequent access)
- **S3 Standard-IA** (Infrequent Access): $0.0125/GB/month
- **S3 Glacier Instant Retrieval**: $0.004/GB/month
- **S3 Glacier Flexible Retrieval**: $0.0036/GB/month
- **S3 Glacier Deep Archive**: $0.00099/GB/month

### Egress (Data Transfer Out)
- **To Internet**: $0.09/GB (first 10TB/month)
- **Volume discounts**: Decreases to $0.085/GB (next 40TB), $0.07/GB (next 100TB), $0.05/GB (>150TB)
- **Ingress (upload)**: Free

### Request Pricing
- **PUT/COPY/POST/LIST**: $0.005 per 1,000 requests
- **GET/SELECT**: $0.0004 per 1,000 requests

### Free Tier (First 12 months for new customers)
- 5GB S3 Standard storage
- 20,000 GET requests
- 2,000 PUT requests
- 100GB egress to internet

---

## Key Features

### Strengths ✅
- **Most mature**: 19 years in production (launched 2006)
- **Feature-rich**: 300+ features (versioning, replication, lifecycle, object lock, etc.)
- **Global reach**: 33+ regions, 100+ availability zones
- **Ecosystem integration**: Native integration with entire AWS ecosystem
- **Durability**: 99.999999999% (11 nines) durability
- **Availability**: 99.99% SLA for Standard class

### Weaknesses ⚠️
- **Highest egress costs**: $0.09/GB makes large downloads expensive
- **Complex pricing**: Multiple storage classes, features have separate charges
- **Lock-in risk**: AWS-specific features (Glacier, Object Lambda, S3 Select) aren't portable

---

## Best For

**✅ Ideal Use Cases**:
- AWS-native applications (Lambda, EC2, ECS workloads)
- Enterprises requiring advanced features (compliance, governance, analytics)
- Applications needing AWS ecosystem integrations (Athena, Glue, SageMaker)
- Multi-region replication with AWS services

**❌ Not Ideal For**:
- High-egress workloads (video streaming, large file downloads)
- Cost-sensitive small projects
- Multi-cloud portability requirements

---

## Differentiators

1. **Market Leader**: De-facto standard, most documentation and tooling
2. **Feature Breadth**: Unmatched feature set (Object Lambda, S3 Select, Batch Operations)
3. **AWS Ecosystem**: Seamless integration with 200+ AWS services
4. **Enterprise Features**: Advanced compliance (HIPAA, PCI-DSS, SOC2), governance tools

---

## Cost Example (100TB storage + 200TB egress/month)

- Storage (100TB × $0.023): **$2,300**
- Egress (200TB):
  - First 10TB × $0.09 = $900
  - Next 40TB × $0.085 = $3,400
  - Next 100TB × $0.07 = $7,000
  - Next 50TB × $0.07 = $3,500
  - **Total egress: $14,800**
- Requests (negligible): ~$50

**Monthly Total: ~$17,150**

---

## Quick Assessment

**Market Position**: 🏆 Market leader, reference implementation
**Cost**: 💰💰💰 Expensive (especially egress)
**Features**: ⭐⭐⭐⭐⭐ Most comprehensive
**Portability**: ⚠️ Medium (if using AWS-specific features)
**Maturity**: ✅ 19 years, battle-tested

**Bottom Line**: AWS S3 is the gold standard with the most features, but you pay a premium—especially for egress. Best for AWS-native workloads where ecosystem integration outweighs cost.
