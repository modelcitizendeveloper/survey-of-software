# Discovery Table of Contents: Machine Translation APIs for CJK

## Overview

This discovery research evaluates four major machine translation API providers (Google Cloud Translation, Azure Translator, Amazon Translate, DeepL) for Chinese, Japanese, and Korean language pairs.

**Research completed:** 2026-01-29

**Research method:** Four-Pass Strategy (4PS)
- S1-rapid: Quick survey
- S2-comprehensive: Deep feature analysis
- S3-need-driven: Real-world use cases
- S4-strategic: Long-term viability

## S1-Rapid: Quick Survey (30-60 min per service)

**Objective:** Basic capabilities, pricing, CJK support overview

### Documents
- [`S1-rapid/approach.md`](S1-rapid/approach.md) - Methodology
- [`S1-rapid/deepl.md`](S1-rapid/deepl.md) - DeepL overview
- [`S1-rapid/google-translate.md`](S1-rapid/google-translate.md) - Google Cloud Translation overview
- [`S1-rapid/azure-translator.md`](S1-rapid/azure-translator.md) - Azure Translator overview
- [`S1-rapid/amazon-translate.md`](S1-rapid/amazon-translate.md) - Amazon Translate overview
- [`S1-rapid/recommendation.md`](S1-rapid/recommendation.md) - Initial recommendations

### Key Findings
- **Cost range:** $10-25 per million characters
- **Free tiers:** Azure 2M/mo (best), Google/DeepL 500K/mo, Amazon 2M/mo (12 months)
- **CJK support:** All four providers support ZH-CN, ZH-TW, JA, KO
- **Quality leader:** Google (longest track record), DeepL improving (1.7x for JA/ZH-CN)
- **Cost leader:** Azure ($10/M - 50% cheaper than Google)

## S2-Comprehensive: Deep Feature Analysis (2-3 hours per service)

**Objective:** Advanced features, integration complexity, CJK-specific capabilities

### Documents
- [`S2-comprehensive/approach.md`](S2-comprehensive/approach.md) - Methodology
- [`S2-comprehensive/google-translate.md`](S2-comprehensive/google-translate.md) - Google deep-dive
- [`S2-comprehensive/deepl.md`](S2-comprehensive/deepl.md) - DeepL deep-dive
- [`S2-comprehensive/azure-translator.md`](S2-comprehensive/azure-translator.md) - Azure deep-dive
- [`S2-comprehensive/amazon-translate.md`](S2-comprehensive/amazon-translate.md) - Amazon deep-dive
- [`S2-comprehensive/feature-comparison.md`](S2-comprehensive/feature-comparison.md) - Feature matrix
- [`S2-comprehensive/recommendation.md`](S2-comprehensive/recommendation.md) - Decision framework

### Key Findings

#### Formality Control
- ✅ **DeepL**: Japanese formality (keigo), European languages
- ✅ **Amazon**: Japanese formality, multiple languages
- ❌ **Google**: No formality control
- ❌ **Azure**: No formality control

#### Document Translation
- ✅ **DeepL**: DOCX, PDF, PPTX, HTML (best formatting reported)
- ✅ **Google**: DOCX, PDF, PPTX, XLSX, HTML ($0.08/page or text pricing)
- ✅ **Azure**: DOCX, PDF, PPTX, XLSX, HTML
- ❌ **Amazon**: No document translation (text-only)

#### Custom Models
- **Google**: AutoML ($30-80/M, requires training)
- **Azure**: Custom Translator ($10/M + $10/mo hosting)
- **Amazon**: Active Custom Translation (ACT) - unique on-the-fly customization, no training/hosting fees
- **DeepL**: No custom models (glossaries only)

#### Ecosystem Integration
- **Google**: GCP-native (GCS, Cloud Monitoring, IAM)
- **Azure**: Azure-native (Blob Storage, Azure Monitor, AD)
- **Amazon**: AWS-native (S3, Lambda, CloudWatch, IAM)
- **DeepL**: Standalone (no cloud ecosystem coupling)

## S3-Need-Driven: Real-World Use Cases

**Objective:** Validate recommendations through concrete CJK translation scenarios

### Documents
- [`S3-need-driven/approach.md`](S3-need-driven/approach.md) - Methodology
- [`S3-need-driven/use-case-japanese-business.md`](S3-need-driven/use-case-japanese-business.md) - Japanese business communication (formality-critical)
- [`S3-need-driven/use-case-ecommerce-volume.md`](S3-need-driven/use-case-ecommerce-volume.md) - E-commerce product localization (high-volume, cost-sensitive)
- [`S3-need-driven/use-case-technical-docs.md`](S3-need-driven/use-case-technical-docs.md) - Technical documentation (format preservation, terminology)
- [`S3-need-driven/recommendation.md`](S3-need-driven/recommendation.md) - Context-dependent guidance

### Key Findings

**Use Case 1: Japanese Business Communication**
- **Winner:** DeepL ($5.49/mo) - Only provider with Japanese formality control + proven quality
- **Alternative:** Amazon Translate ($0 year 1) - Japanese formality + ACT customization
- **Avoided:** Google/Azure - No formality control (non-negotiable for business Japanese)

**Use Case 2: E-commerce High Volume (10K products, 4 languages)**
- **Winner:** Azure ($100/year) - 60% cost savings vs Google, quality sufficient
- **Alternative:** Amazon ($150 year 1) - Free first year, but Azure cheaper long-term
- **Avoided:** DeepL ($389/year) - 3.9x more expensive than Azure

**Use Case 3: Technical Documentation (500 pages DOCX)**
- **Winner:** Google ($32/year) - Proven technical quality, DOCX support, unlimited glossary
- **Alternative:** Azure ($0/year) - Free tier covers usage, competitive quality
- **Avoided:** Amazon - No document translation (critical gap)

### Decision Framework Validated

**Three different use cases = three different winners.**
- Formality-critical → DeepL/Amazon (features)
- Cost-sensitive volume → Azure (lowest cost)
- Technical/critical content → Google (proven quality)

**Lesson:** Context matters more than generic rankings.

## S4-Strategic: Long-Term Viability (3-5 years)

**Objective:** Assess sustainability, vendor risk, strategic fit

### Documents
- [`S4-strategic/approach.md`](S4-strategic/approach.md) - Methodology
- [`S4-strategic/recommendation.md`](S4-strategic/recommendation.md) - Long-term strategic guidance

### Key Findings

#### Viability Rankings (3-5 year outlook)
- ⭐⭐⭐⭐⭐ **Google/Azure/Amazon**: Core cloud AI services, stable business models, continuous investment guaranteed
- ⭐⭐⭐⭐ **DeepL**: Independent company, strong quality focus, acquisition risk (could be upside if acquired by cloud giant)

#### Strategic Risks
- **Low Risk:** Google/Azure/Amazon (core services, no shutdown risk)
- **Medium Risk:** DeepL (independent, acquisition possible, premium pricing under pressure)

#### Technology Trends (2026-2027)
1. **LLM integration** - All providers moving to LLM-powered translation (quality convergence)
2. **Formality expansion** - Google/Azure likely to add formality control (competitive pressure)
3. **Document translation** - Amazon likely to add DOCX support (competitive gap)
4. **Custom model democratization** - Amazon ACT approach spreading (lower barriers)

#### Lock-In Assessment
- **Medium-High:** Google/Azure/Amazon (cloud ecosystem coupling)
- **Low-Medium:** DeepL (standalone, easiest to migrate)

**Mitigation:** Abstract translation API behind internal interface (2-4 weeks initial investment)

### Strategic Recommendations

**Safe long-term choices (3-5 years):**
- Google/Azure/Amazon - All three are core cloud services with guaranteed investment

**Conditional choice:**
- DeepL - Quality premium justified for Japanese formality or European+CJK, but monitor acquisition news

**Hedge strategy:**
- Build abstraction layer, primary provider = your cloud platform, backup = DeepL or alternative cloud

## Cross-Cutting Insights

### Quality vs Cost Trade-off
| Provider | Quality (CJK) | Cost/M | Best For |
|----------|---------------|--------|----------|
| **Google** | ⭐⭐⭐⭐⭐ | $20 | Critical content, proven track record |
| **DeepL** | ⭐⭐⭐⭐⭐ (JA/ZH-CN) | $25 | Japanese formality, European+CJK |
| **Azure** | ⭐⭐⭐⭐ | **$10** | Cost-sensitive, high volume |
| **Amazon** | ⭐⭐⭐⭐ | $15 | AWS-native, ACT customization |

**All providers offer production-grade CJK quality.** Quality differences are marginal for most use cases.

### Feature Gaps that Disqualify
- **Japanese formality needed** → Google/Azure eliminated
- **Document translation needed** → Amazon eliminated
- **AWS-native integration** → Google/Azure/DeepL lose ecosystem advantage

### Free Tier Economics
- **Azure 2M/mo (permanent):** Covers most low/medium-volume use cases **forever**
- **Google 500K/mo (permanent):** Covers low-volume use cases
- **Amazon 2M/mo (12 months):** Good year 1, plan transition after
- **DeepL 500K/mo (permanent):** Covers low-volume use cases

**At low volumes (<2M/month), all providers are effectively free - choose on features/quality.**

### Cost Savings at Scale (1B chars/year)
- Azure: $10,000
- Amazon: $15,000 (50% more than Azure)
- Google: $20,000 (100% more than Azure)
- DeepL: $25,000 (150% more than Azure)

**Azure saves $10K-15K/year vs competitors at high volume.**

## Decision Matrix (Summary)

### Choose **Google Cloud Translation** if:
- Quality and track record are paramount
- Already on GCP (ecosystem fit)
- Need Translation LLM or AutoML
- Enterprise compliance required

### Choose **Azure Translator** if:
- Cost optimization is priority (50% savings)
- Already on Azure (ecosystem fit)
- High volume expected (billions of chars/year)
- Good enough quality acceptable

### Choose **Amazon Translate** if:
- AWS-native stack (S3, Lambda integration)
- Need Active Custom Translation (unique)
- Japanese formality required
- Domain-specific adaptation needed

### Choose **DeepL** if:
- Japanese formality is critical (keigo)
- European + CJK content (DeepL European strength)
- Quality > cost priorities
- Independence from cloud providers valued

## Implementation Guidance

### Timeline
- **POC**: 1-3 days
- **Integration**: 1-2 weeks
- **Quality validation**: 2-4 weeks
- **Production rollout**: 1-2 weeks
- **Total MVP**: 6-10 weeks

### Team Requirements
- Backend engineer (API integration)
- Native speaker per target language (quality validation)
- Product manager (requirements, quality bar)
- DevOps engineer (monitoring, cost tracking)

### Common Pitfalls
1. Shipping without native speaker validation
2. Translating sentence-by-sentence (lose context)
3. Ignoring free tier limits (surprise bills)
4. Assuming all APIs have same quality
5. Missing formality control (Japanese business)

### Success Criteria (90 days)
- ✅ Translations live in production
- ✅ <5% user complaints about quality
- ✅ Cost within budget (±20%)
- ✅ Glossary covers 80%+ domain terms
- ✅ Native speakers rate quality 7+/10

## Additional Resources

### Root Level
- [`../DOMAIN_EXPLAINER.md`](../DOMAIN_EXPLAINER.md) - Universal analogies, decision criteria, implementation reality

### Discovery Outputs
- **S1-rapid**: Provider overviews, initial cost/quality comparison
- **S2-comprehensive**: Feature matrices, integration deep-dives
- **S3-need-driven**: Real-world use case validation
- **S4-strategic**: Long-term viability assessment

## Research Conclusion

**No universally "best" provider exists.** The right choice depends on:
1. **Specific features** (formality, document translation, customization)
2. **Volume and cost** (free tier vs high-volume pricing)
3. **Quality bar** (critical vs good enough)
4. **Ecosystem fit** (GCP/Azure/AWS-native)

**All four providers are viable for production CJK translation.** Choose based on your specific context (S3 use cases) and long-term strategy (S4 viability).

**Safe default:** Your cloud platform's native service (Google if GCP, Azure if Azure, Amazon if AWS). Lock-in is a feature (continuous investment), not a bug.
