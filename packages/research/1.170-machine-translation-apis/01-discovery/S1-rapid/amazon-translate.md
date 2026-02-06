# Amazon Translate API

## Overview
Amazon Translate is AWS's neural machine translation service supporting 75 languages with 5,550 translation combinations. Features Active Custom Translation (ACT) for on-the-fly customization without building custom models.

## CJK Language Support

### Supported Languages
- **Chinese**: Simplified (ZH) and Traditional (ZH-TW)
- **Japanese**: Full support (JA)
- **Korean**: Full support (KO)

### Translation Coverage
- 75 languages total
- 5,550 language pair combinations
- Direct CJK ↔ CJK pairs supported
- Japanese, Russian, Italian, Traditional Chinese added in recent expansion

**Sources:**
- [Amazon Translate supported languages](https://docs.aws.amazon.com/translate/latest/dg/what-is-languages.html)
- [Amazon Translate language expansion](https://aws.amazon.com/blogs/aws/amazon-translate-adds-support-for-new-languages/)
- [Amazon Translate features](https://aws.amazon.com/translate/details/)

## Pricing (2026)

### Free Tier
- 2 million characters/month free for **12 months** (AWS Free Tier)
- After 12 months: no free tier

### Standard Pricing
- **$15 per 1 million characters**
- Pay only for what you use (no base fees)
- Applies to all language pairs (no premium for CJK)

### Custom Terminology
- **No additional cost** (up to 10,000 terms per file)

### Active Custom Translation (ACT)
- Same $15/M rate (no separate charge)
- No model training or hosting fees

**Cost Comparison:**
- Azure: $10/M (cheapest)
- Amazon: **$15/M** (middle)
- Google: $20/M
- DeepL: $25/M (most expensive)

**Sources:**
- [Amazon Translate pricing](https://aws.amazon.com/translate/pricing/)
- [Pricing calculator](https://costgoat.com/pricing/amazon-translate)
- [Amazon Translate FAQ](https://aws.amazon.com/translate/faqs/)

## API Features

### Core Translation
- Real-time translation (synchronous)
- Batch translation (asynchronous)
- Language detection
- Custom terminology (glossaries)
- Formality control (formal/informal)

### Active Custom Translation (ACT)
**Unique approach:** Customizes output on-the-fly without pre-training models
- Provide parallel translation data (source/target pairs)
- ACT selects relevant segments during translation
- Updates translation model dynamically
- Better performance than baseline without model training overhead
- More granular parallel data = better performance

### Integration
- RESTful API
- AWS SDKs (Python, Java, JavaScript, .NET, Go, Ruby, PHP, C++)
- AWS CLI support
- Batch translation via S3
- IAM-based access control
- CloudWatch monitoring

**Sources:**
- [Amazon Translate features](https://aws.amazon.com/translate/details/)
- [Active Custom Translation overview](https://aws.amazon.com/blogs/machine-learning/customizing-your-machine-translation-using-amazon-translate-active-custom-translation/)
- [ACT pipeline](https://aws.amazon.com/blogs/machine-learning/build-a-multilingual-automatic-translation-pipeline-with-amazon-translate-active-custom-translation/)

## CJK-Specific Considerations

### Strengths
- **Strong EN-ZH quality**: Testing shows "higher average BLEU scores" with ACT
- "Particularly strong in certain Asian languages"
- Natural-sounding output: "mostly grammatically correct"
- Context-aware NMT (considers entire source sentence)
- **No extra cost for custom terminology** (unlike competitors)
- **ACT provides customization without training overhead**

### Quality Evidence
- BLEU score improvements for EN↔ZH with ACT
- Qualitative assessments: natural, grammatically correct
- Full-context neural translation (not phrase-based)
- AWS Localization uses Translate internally for scaling

**Sources:**
- [Amazon Science: Auto ML translation](https://www.amazon.science/blog/auto-machine-translation-and-synchronization-for-dive-into-deep-learning)
- [AWS Localization case study](https://aws.amazon.com/blogs/machine-learning/aws-localization-uses-amazon-translate-to-scale-localization/)

### Limitations
- Free tier expires after 12 months (vs permanent for Azure/Google/DeepL)
- Smaller language coverage (75) vs Google (100+) or Azure (130+)
- Less public benchmarking data compared to Google
- ACT requires parallel data preparation

## Active Custom Translation vs Traditional Custom Models

| Approach | Training | Hosting | Flexibility | Cost |
|----------|----------|---------|-------------|------|
| **ACT (Amazon)** | None | None | On-the-fly | $15/M (included) |
| **AutoML (Google)** | Required | N/A | Static model | $30-80/M |
| **Custom (Azure)** | Required | $10/mo/region | Static model | $10/M + hosting |

ACT's advantage: No upfront training time, no hosting fees, dynamic adaptation per request.

## Use Case Fit

**Excellent for:**
- **AWS-native stacks** (S3, Lambda, CloudWatch integration)
- **Dynamic customization needs** (ACT provides flexibility without model training)
- **Cost-conscious projects** (middle pricing, no hosting fees)
- Batch translation workflows (S3 integration)
- Applications needing formality control
- Teams with parallel translation data (ACT leverage)

**Consider alternatives for:**
- Highest-quality CJK translation (Google/DeepL may edge out)
- Long-term projects after 12-month free tier expires (Azure has permanent 2M/mo)
- Teams not on AWS (ecosystem integration less valuable)
- Extremely high volume (Azure $10/M is 33% cheaper)

## Ecosystem Integration
- Native AWS service (IAM, CloudWatch, VPC)
- S3 batch translation (async processing)
- Lambda integration for serverless
- API Gateway for custom REST endpoints
- AWS PrivateLink for VPC-isolated access
- AWS Organizations support
- CloudTrail audit logging
