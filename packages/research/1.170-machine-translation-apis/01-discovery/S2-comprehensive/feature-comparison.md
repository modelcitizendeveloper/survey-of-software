# Feature Comparison Matrix: Machine Translation APIs

## Quick Reference

| Feature | Google Cloud | Azure | Amazon | DeepL |
|---------|--------------|-------|--------|-------|
| **Pricing** | $20/M | **$10/M** | $15/M | $25/M + $5.49/mo |
| **Free Tier** | 500K/mo (perm) | **2M/mo (perm)** | 2M/mo (12mo) | 500K/mo (perm) |
| **CJK Languages** | ZH-CN, ZH-TW, JA, KO | ZH-CN, ZH-TW, JA, KO | ZH-CN, ZH-TW, JA, KO | ZH-CN, ZH-TW, JA, KO |
| **Total Languages** | **100+** | **130+** | 75 | 36 |
| **API Versions** | v2, v3 | v3.0 | Single | Single |
| **Auth** | API key, SA | API key, AD | IAM | API key |

## Core Translation Features

| Feature | Google Cloud | Azure | Amazon | DeepL |
|---------|--------------|-------|--------|-------|
| **Real-time translation** | ✅ v2, v3 | ✅ | ✅ | ✅ |
| **Batch translation** | ✅ v3 (GCS) | ✅ (Blob) | ✅ (S3) | ❌ |
| **Document translation** | ✅ v3 | ✅ | ❌ | ✅ |
| **Language detection** | ✅ | ✅ | ✅ | ✅ |
| **Confidence scores** | ✅ | ✅ | Limited | ❌ |
| **Sentence splitting** | ✅ | ✅ | ✅ | ✅ |

## Advanced Features

| Feature | Google Cloud | Azure | Amazon | DeepL |
|---------|--------------|-------|--------|-------|
| **Glossaries** | ✅ v3 (unlimited) | ✅ (custom) | ✅ (10K terms, free) | ✅ (55 pairs, 2026) |
| **Custom models** | ✅ AutoML ($30-80/M) | ✅ ($10/M + $10/mo hosting) | ✅ ACT ($15/M, no hosting) | ❌ |
| **Formality control** | ❌ | ❌ | ✅ (JA, FR, DE, ES...) | ✅ (JA, EU langs) |
| **Transliteration** | ❌ (separate service) | ✅ (built-in) | ❌ | ❌ |
| **Adaptive translation** | ✅ TLLM ($50/M) | ❌ | ✅ ACT ($15/M) | ❌ |
| **Dictionary lookup** | ❌ | ✅ | ❌ | ❌ |

## CJK-Specific Features

| Feature | Google Cloud | Azure | Amazon | DeepL |
|---------|--------------|-------|--------|-------|
| **Direct CJK-CJK pairs** | ✅ | ✅ (explicit) | ✅ | ✅ |
| **ZH-CN ↔ ZH-TW** | ✅ | ✅ | ✅ | ✅ |
| **JA formality (keigo)** | ❌ | ❌ | ✅ | ✅ |
| **ZH formality** | ❌ | ❌ | ❌ | ❌ |
| **KO formality** | ❌ | ❌ | ❌ | ❌ |
| **Next-gen CJK model** | ✅ Translation LLM | ❌ | ❌ | ✅ 1.7x (JA/ZH-CN) |
| **CJK glossaries** | ✅ | ✅ | ✅ | ✅ (ZH added 2026) |
| **Romanization** | ✅ (experimental) | ✅ Transliteration API | ❌ | ❌ |

## Document Translation

| Feature | Google Cloud | Azure | Amazon | DeepL |
|---------|--------------|-------|--------|-------|
| **PDF** | ✅ ($0.08/page) | ✅ ($10/M chars) | ❌ | ✅ |
| **DOCX** | ✅ | ✅ | ❌ | ✅ |
| **PPTX** | ✅ | ✅ | ❌ | ✅ |
| **XLSX** | ✅ | ✅ | ❌ | ❌ |
| **HTML** | ✅ | ✅ | ❌ | ✅ |
| **Images (Beta)** | ❌ | ❌ | ❌ | ✅ JPEG/PNG |
| **Layout preservation** | ✅ | ✅ | N/A | ✅ (reported best) |
| **Batch documents** | ✅ GCS | ✅ Blob Storage | N/A | ✅ API |

## Model Options

| Model Type | Google Cloud | Azure | Amazon | DeepL |
|------------|--------------|-------|--------|-------|
| **Standard NMT** | ✅ $20/M | ✅ $10/M | ✅ $15/M | ✅ $25/M |
| **Next-gen LLM** | ✅ Translation LLM ($20-50/M) | ❌ | ❌ | ✅ Auto (1.7x JA/ZH-CN) |
| **Custom trained** | ✅ AutoML ($30-80/M) | ✅ Custom ($10/M + hosting) | ❌ | ❌ |
| **Adaptive (no training)** | ✅ TLLM Adaptive ($50/M) | ❌ | ✅ ACT ($15/M) | ❌ |
| **Model selection per request** | ✅ | ✅ | ✅ (terminology/ACT) | ❌ (auto next-gen) |

## Integration & SDKs

| Feature | Google Cloud | Azure | Amazon | DeepL |
|---------|--------------|-------|--------|-------|
| **REST API** | ✅ | ✅ | ✅ | ✅ |
| **gRPC** | ✅ v3 only | ❌ | ❌ | ❌ |
| **Python SDK** | ✅ | ✅ | ✅ (boto3) | ✅ |
| **JavaScript/Node** | ✅ | ✅ | ✅ | ✅ |
| **.NET** | ✅ | ✅ | ✅ | ✅ |
| **Java** | ✅ | ✅ | ✅ | ❌ (community) |
| **Go** | ✅ | ❌ | ✅ | ❌ (community) |
| **Ruby, PHP** | ✅ | Limited | ✅ | ❌ (community) |
| **SDK maturity** | Excellent | Excellent | Excellent | Good |

## Ecosystem Integration

| Feature | Google Cloud | Azure | Amazon | DeepL |
|---------|--------------|-------|--------|-------|
| **Cloud storage** | GCS | Blob Storage | S3 | ❌ |
| **Serverless functions** | Cloud Functions | Azure Functions | Lambda | ❌ |
| **Monitoring** | Cloud Monitoring | Azure Monitor | CloudWatch | ❌ |
| **Logging** | Cloud Logging | Log Analytics | CloudTrail/Logs | ❌ |
| **IAM integration** | ✅ GCP IAM | ✅ Azure AD | ✅ AWS IAM | ❌ |
| **Private endpoints** | ✅ VPC Service Controls | ✅ Private Link | ✅ PrivateLink | ❌ |
| **Cost tracking** | ✅ Labels | ✅ Tags | ✅ Tags | Dashboard only |
| **Compliance certs** | SOC 2, ISO, HIPAA | SOC 2, ISO, HIPAA | SOC 2, ISO, HIPAA, PCI | GDPR |

## Performance & Reliability

| Feature | Google Cloud | Azure | Amazon | DeepL |
|---------|--------------|-------|--------|-------|
| **Typical latency** | ~100ms (NMT) | ~100-200ms | ~100-200ms | ~100-200ms |
| **SLA** | 99.5% | 99.9% | 99.9% | Not published |
| **Regional endpoints** | ✅ Global | ✅ Multi-region | ✅ AWS regions | ❌ Single endpoint |
| **Rate limits** | 600 qps | Varies by tier | 20-100 TPS | Not published |
| **Quotas** | 10M chars/100s | 2M free, unlimited paid | Soft limits | Based on subscription |

## Cost Analysis (1 Billion Characters/Year)

| Provider | Annual Cost | Monthly Avg | Notes |
|----------|-------------|-------------|-------|
| **Azure** | **$10,000** | $833 | After 2M free/mo, cheapest |
| **Amazon** | **$15,000** | $1,250 | After 12-mo free tier |
| **Google** | **$20,000** | $1,667 | After 500K free/mo |
| **DeepL** | **$25,066** | $2,089 | $25K + $66 base fee |

**Savings:**
- Azure saves $10K/year vs Google
- Azure saves $5K/year vs Amazon
- Azure saves $15K/year vs DeepL

## Quality Claims (CJK)

| Provider | Evidence | Specific Claims |
|----------|----------|-----------------|
| **Google** | ✅ Longest track record | Translation LLM "significantly higher performance", industry standard |
| **DeepL** | ✅ Verified linguist tests | 1.7x improvement for EN↔JA, EN↔ZH-CN (next-gen LLM) |
| **Amazon** | ✅ BLEU scores | Higher BLEU for EN↔ZH with ACT, "particularly strong in Asian languages" |
| **Azure** | ⚠️ General claims | "Modern NMT major advances", competitive but fewer public benchmarks |

## Decision Matrix

### Choose **Google Cloud Translation** if:
- ✅ CJK quality is absolutely paramount
- ✅ Need multiple model options (NMT, LLM, Custom)
- ✅ Already on GCP ecosystem
- ✅ Complex workflows (batch, document, glossaries)
- ✅ Enterprise features (SLAs, compliance, monitoring)

### Choose **Azure Translator** if:
- ✅ **Cost is primary concern** (50% cheaper than Google)
- ✅ **High-volume translation** (billions of chars/year)
- ✅ Already on Azure ecosystem
- ✅ Need direct CJK-CJK pairs (JA↔KO, JA↔ZH)
- ✅ Largest permanent free tier (2M/mo)

### Choose **Amazon Translate** if:
- ✅ **AWS-native stack** (S3, Lambda, CloudWatch)
- ✅ Need **Active Custom Translation** (no training, no hosting fees)
- ✅ **Japanese formality control** required
- ✅ Strong EN↔ZH quality needed
- ✅ Event-driven workflows (S3 triggers, batch)

### Choose **DeepL** if:
- ✅ **Japanese formality control** (keigo) is critical
- ✅ **Next-gen LLM quality** for EN↔JA/ZH-CN matters
- ✅ **European ↔ CJK bridge** (leveraging DeepL European strength)
- ✅ **Document translation** with best formatting preservation
- ✅ Simplicity over features (easiest API)
- ✅ Quality > cost priorities

## Feature Maturity Summary

| Category | Leader | Runner-up | Notes |
|----------|--------|-----------|-------|
| **CJK Quality** | Google | DeepL (improving) | Google has longest track record |
| **Cost Efficiency** | **Azure** | Amazon | Azure 50% cheaper than Google |
| **Feature Completeness** | **Google** | Azure/Amazon | Most model options, best docs |
| **CJK Formality** | **DeepL/Amazon** | - | Only providers with JA formality |
| **Customization** | **Amazon (ACT)** | Google (AutoML) | ACT unique: no training/hosting fees |
| **Document Translation** | **DeepL** | Google/Azure | DeepL reported best formatting |
| **Ecosystem Integration** | **Google/Azure/Amazon** | - | All three have full cloud native support |
| **Simplicity** | **DeepL** | Amazon | Easiest API, least enterprise complexity |
| **Enterprise Operations** | **Google/Azure/Amazon** | - | Full monitoring, logging, compliance |

## Gaps & Limitations

### Google Cloud
- ❌ No formality control (unlike DeepL, Amazon)
- ❌ Smaller free tier (500K vs Azure 2M)
- ❌ Premium pricing ($20/M)

### Azure
- ❌ No formality control
- ❌ Fewer public quality benchmarks
- ❌ Custom model hosting fees ($10/mo/region)

### Amazon
- ❌ No document translation (text-only)
- ❌ Free tier expires after 12 months
- ❌ 10K glossary term limit
- ❌ More expensive than Azure ($15/M vs $10/M)

### DeepL
- ❌ Most expensive ($25/M + base fee)
- ❌ No batch text processing
- ❌ No custom model training
- ❌ No Chinese/Korean formality
- ❌ No enterprise operations (monitoring, compliance, audit)
- ❌ Smallest language coverage (36 vs 75-130+)

## Summary Recommendations

**Best Overall (CJK Production):** **Google Cloud Translation** - Proven quality, complete features, premium pricing justified

**Best Value (Cost-Sensitive):** **Azure Translator** - Half the cost of Google, competitive quality, enterprise features

**Best for AWS Users:** **Amazon Translate** - Unique ACT customization, native integration, Japanese formality

**Best for Japanese Business:** **DeepL** or **Amazon** - Both have formality control for keigo

**Best for European+CJK:** **DeepL** - Strongest European languages, improving CJK quality (1.7x)

**Best for Simplicity:** **DeepL** - Easiest API, least complexity, good for small teams

**Best for Enterprise:** **Google/Azure/Amazon** - All three have full monitoring, compliance, security
