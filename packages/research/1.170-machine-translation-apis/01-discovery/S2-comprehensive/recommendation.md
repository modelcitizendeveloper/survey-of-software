# S2-Comprehensive Recommendation: Machine Translation APIs

## Executive Summary

After deep feature analysis, the choice of machine translation API depends primarily on **ecosystem fit**, **specific feature needs**, and **cost constraints** rather than pure quality differences (all four providers offer competitive CJK translation quality).

## Four-Way Decision Framework

### 1. Ecosystem Lock-In (Primary Decision Factor)

If you're already committed to a cloud provider:
- **GCP → Google Cloud Translation** (no brainer)
- **Azure → Azure Translator** (no brainer)
- **AWS → Amazon Translate** (no brainer)

**Why this matters:**
- Native integration (storage, monitoring, IAM, logging)
- Reduced operational complexity
- No cross-cloud data transfer fees
- Unified billing and cost tracking
- Existing team expertise

**Only break ecosystem choice if:**
- You need Japanese formality control (DeepL or Amazon)
- Cost savings justify complexity (Azure is 50% cheaper than Google)
- Quality gap is proven for your specific use case (test in S3)

### 2. Feature-Based Selection (If No Ecosystem Lock-In)

| Need | Best Choice | Why |
|------|-------------|-----|
| **Japanese formality (keigo)** | DeepL or Amazon | Only providers with JA formality control |
| **Document translation** | DeepL or Google or Azure | DeepL best formatting, Google/Azure good |
| **Lowest cost** | Azure | $10/M (50% cheaper than Google/DeepL) |
| **Custom models (no hosting fees)** | Amazon (ACT) | On-the-fly customization, no $10/mo per model |
| **Highest proven CJK quality** | Google | Longest track record, Translation LLM available |
| **European ↔ CJK bridge** | DeepL | Strongest European languages + improving CJK |
| **Simplest integration** | DeepL | Easiest API, least enterprise complexity |
| **Batch workflows** | Google/Azure/Amazon | All three have cloud storage integration |
| **Direct CJK-CJK pairs** | Azure or Google | Explicit support without English pivot |

### 3. Cost-Based Selection (High Volume)

**At 1 billion characters/year:**

| Provider | Annual Cost | Break-even Threshold |
|----------|-------------|----------------------|
| **Azure** | $10,000 | **Always cheapest** |
| **Amazon** | $15,000 | Better than Google above 100M/year |
| **Google** | $20,000 | Better than DeepL always |
| **DeepL** | $25,066 | Never cost-competitive at high volume |

**Cost Optimization Strategy:**
1. **Under 500K/mo total**: Use free tiers (all providers work)
2. **500K-2M/mo**: Azure free tier covers you (zero cost)
3. **Over 2M/mo**: Azure saves $10K/year per billion chars vs Google

**Hidden Costs to Consider:**
- **Custom models**: Azure $10/mo hosting vs Amazon ACT $0 hosting
- **Document translation**: Google $0.08/page vs text-based pricing
- **Glossary management**: Amazon free (10K terms) vs pay-per-use elsewhere
- **Free tier expiration**: Amazon 12-month vs Azure/Google/DeepL permanent

## Detailed Recommendations by Use Case

### Use Case 1: Japanese Business Communication

**Requirement:** Formal Japanese (keigo) for business correspondence

**Winner:** **DeepL** or **Amazon Translate**
- Both have Japanese formality control
- DeepL: 1.7x quality improvement (verified), best for EN↔JA
- Amazon: AWS integration, formality + ACT customization
- **Choose DeepL** if quality > cost
- **Choose Amazon** if AWS-native or need customization (ACT)

**Avoid:** Google, Azure (no JA formality control)

### Use Case 2: High-Volume Production (Billions of Chars/Year)

**Requirement:** Cost-effective CJK translation at scale

**Winner:** **Azure Translator**
- $10/M (50% cheaper than Google $20/M, 60% cheaper than DeepL $25/M)
- Saves $10K/year per billion chars vs Google
- Competitive quality (modern NMT)
- Enterprise features (monitoring, compliance, SLAs)

**Runners-up:**
- **Amazon** if AWS-native ($15/M - still cheaper than Google)
- **Google** if quality absolutely paramount (longest CJK track record)

**Avoid:** DeepL (most expensive at scale)

### Use Case 3: Document Translation Workflows

**Requirement:** Translate DOCX, PDF, PPTX preserving formatting

**Winner:** **DeepL**
- Reported best layout preservation
- Supports DOCX, PDF, PPTX, HTML
- Image OCR (Beta for JPEG/PNG)
- Simple API

**Runners-up:**
- **Google** v3 Advanced: PDF, DOCX, PPTX, XLSX, HTML ($0.08/page)
- **Azure**: Full format support, Blob Storage integration

**Avoid:** Amazon (no document translation)

### Use Case 4: Domain-Specific CJK Translation (Legal, Medical, Technical)

**Requirement:** Consistent terminology, domain-specific quality

**Winner:** **Amazon Translate (ACT)**
- Active Custom Translation: no training, no hosting fees
- Proven EN↔ZH quality with ACT
- Dynamic per-request adaptation
- $15/M (no additional costs)

**Runners-up:**
- **Google AutoML**: More powerful but complex ($30-80/M + training time)
- **Azure Custom**: Effective but $10/mo hosting per model per region

**Avoid:** DeepL (no custom model training)

### Use Case 5: European HQ with Asian Operations

**Requirement:** EN/DE/FR ↔ JA/ZH translation, multilingual content

**Winner:** **DeepL**
- Strongest European language quality
- Next-gen LLM for EN↔JA/ZH-CN (1.7x improvement)
- Formality control for JA, DE, FR, ES, IT
- Multilingual glossaries (2026)

**Runner-up:**
- **Google** if volume is high (DeepL most expensive)

**Avoid:** Azure, Amazon if European quality matters

### Use Case 6: Startup/Prototype (Low Volume, Cost-Sensitive)

**Requirement:** Minimal upfront cost, good quality, easy integration

**Winner:** **Azure Translator**
- 2M chars/month free (permanent)
- 4x larger than Google/DeepL (500K/mo)
- Covers prototyping needs for free
- When scaling, still cheapest ($10/M)

**Runner-up:**
- **Google** if CJK quality is absolutely critical
- **DeepL** if simplicity > cost (easiest API)

**Avoid:** Amazon (free tier expires after 12 months)

### Use Case 7: AWS-Native Application

**Requirement:** S3, Lambda, CloudWatch integration, event-driven workflows

**Winner:** **Amazon Translate**
- Native S3 batch translation
- Lambda triggers, SNS notifications
- CloudWatch monitoring, CloudTrail audit
- IAM-based access control
- ACT for customization

**No Alternative:** Ecosystem integration advantage is overwhelming

### Use Case 8: Compliance-Heavy Enterprise (HIPAA, SOC 2)

**Requirement:** Certifications, audit logs, private endpoints

**Winner:** **Google** or **Azure** or **Amazon** (all three excellent)
- All have SOC 2, ISO 27001, HIPAA with BAA
- Full audit logging (Cloud Audit Logs, CloudTrail, Activity Logs)
- Private endpoints (VPC Service Controls, PrivateLink, PrivateLink)
- Customer-managed encryption keys

**Choose based on ecosystem:**
- **Azure** if cost matters (cheapest with full compliance)
- **Google** if CJK quality paramount
- **Amazon** if AWS-native

**Avoid:** DeepL (no enterprise compliance certifications published)

## Feature Priority Decision Tree

```
START: Need Machine Translation API for CJK

1. Already on cloud provider?
   ├─ GCP → Google Cloud Translation
   ├─ Azure → Azure Translator
   ├─ AWS → Amazon Translate
   └─ No → Continue to Q2

2. Need Japanese formality control (keigo)?
   ├─ Yes → DeepL or Amazon Translate
   └─ No → Continue to Q3

3. Need document translation (DOCX/PDF)?
   ├─ Yes → DeepL (best) or Google/Azure
   └─ No → Continue to Q4

4. Volume > 1B chars/year?
   ├─ Yes → Azure (cheapest)
   └─ No → Continue to Q5

5. Need custom domain models?
   ├─ Yes, no hosting fees → Amazon (ACT)
   ├─ Yes, need full training → Google (AutoML)
   └─ No → Continue to Q6

6. European + CJK content?
   ├─ Yes → DeepL (best European quality)
   └─ No → Continue to Q7

7. Startup/prototype budget?
   ├─ Yes → Azure (2M free/mo)
   └─ No → Google (proven CJK quality)
```

## Quality vs Cost Trade-off Matrix

| Provider | Quality (CJK) | Cost | Enterprise | Recommendation |
|----------|---------------|------|------------|----------------|
| **Google** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Best if quality > cost |
| **Azure** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Best if cost > marginal quality |
| **Amazon** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Best if AWS-native |
| **DeepL** | ⭐⭐⭐⭐ (⭐ for JA/ZH-CN next-gen) | ⭐⭐ | ⭐⭐ | Best if JA formality or simplicity |

**Quality Assessment Notes:**
- Google: Longest track record, most training data, Translation LLM available
- DeepL: Next-gen LLM 1.7x improvement for JA/ZH-CN (verified), catching up fast
- Azure: Competitive modern NMT, fewer public benchmarks, direct CJK-CJK pairs
- Amazon: Strong EN↔ZH with ACT, "particularly strong in Asian languages"

**All four providers offer production-grade CJK quality.** Quality differences are marginal for most use cases. Test with your actual content in S3 to validate.

## Anti-Recommendations (When NOT to Choose)

### Don't Choose Google if:
- ❌ Cost is primary concern (Azure is 50% cheaper)
- ❌ Need Japanese formality control (DeepL/Amazon have it)
- ❌ Small project under 500K/mo (Azure free tier is 4x larger)

### Don't Choose Azure if:
- ❌ Need Japanese formality control (no support)
- ❌ Japanese quality is absolutely critical (Google/DeepL may edge out)
- ❌ Already on GCP/AWS (ecosystem integration lost)

### Don't Choose Amazon if:
- ❌ Need document translation (no DOCX/PDF support)
- ❌ Cost is primary concern (Azure is 33% cheaper)
- ❌ Long-term project (free tier expires after 12 months)
- ❌ Not on AWS (integration advantage lost)

### Don't Choose DeepL if:
- ❌ High volume (most expensive $25/M vs Azure $10/M)
- ❌ Need enterprise compliance (no SOC 2/HIPAA published)
- ❌ Need batch text processing (no async bulk translation)
- ❌ Need custom models (no training available)
- ❌ Pure CJK↔CJK translation (no unique advantage)

## S2 Final Recommendation

### Tier 1: Default Choices (90% of Use Cases)

1. **Already on cloud provider → Use native service** (Google/Azure/Amazon)
2. **Not on cloud, cost matters → Azure** (cheapest, competitive quality)
3. **Not on cloud, quality paramount → Google** (longest CJK track record)

### Tier 2: Specialized Needs

4. **Japanese formality required → DeepL or Amazon** (only providers)
5. **Document translation → DeepL** (best formatting) or **Google/Azure**
6. **AWS-native → Amazon** (ACT customization unique)
7. **European+CJK → DeepL** (strongest European quality)

### Tier 3: Niche Optimizations

8. **Custom models, no hosting fees → Amazon ACT**
9. **Direct CJK-CJK pairs → Azure** or **Google**
10. **Simplest integration → DeepL** (easiest API)

## Next Steps: S3 Validation

S3 (need-driven) will test these recommendations with real CJK content scenarios:
1. **Business communication** (formal Japanese, Chinese technical docs)
2. **E-commerce** (product descriptions, customer reviews)
3. **Content localization** (blog posts, marketing materials)
4. **Technical documentation** (API docs, user manuals)
5. **Customer support** (informal, conversational tone)

**S3 goals:**
- Validate quality claims with actual CJK text
- Compare formality handling (where available)
- Test glossary effectiveness for CJK terminology
- Assess real-world integration complexity
- Measure latency and error rates

**S2 Conclusion:** All four providers are viable. Choice depends on ecosystem fit, specific features (formality, document translation), and cost constraints more than pure quality differences. Test with your content in S3 to make final decision.
