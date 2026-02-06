# S1-Rapid Recommendation: Machine Translation APIs

## Summary Matrix

| Provider | Free Tier | Cost/M Chars | CJK Quality | Key Strength |
|----------|-----------|--------------|-------------|--------------|
| **Azure Translator** | 2M/mo (perm) | **$10** | Competitive | **Lowest cost** |
| **Amazon Translate** | 2M/mo (12mo) | $15 | Strong EN-ZH | **ACT customization** |
| **Google Cloud** | 500K/mo (perm) | $20 | **Industry-leading** | **Best CJK track record** |
| **DeepL** | 500K/mo (perm) | $25 + $5.49/mo | Improving (1.7x) | **European language quality** |

## Quick Decision Tree

### For Production CJK Translation
→ **Google Cloud Translation** (Advanced/LLM)
- Longest track record for CJK
- Most extensive training data
- Multiple model options (NMT, LLM, custom)
- Industry-standard baseline

### For Cost-Sensitive Projects
→ **Azure Translator**
- 50% cheaper than Google ($10/M vs $20/M)
- Largest permanent free tier (2M vs 500K)
- Direct CJK-CJK pairs
- Competitive quality

### For AWS-Native Stacks
→ **Amazon Translate**
- Native AWS integration (S3, Lambda, IAM)
- Active Custom Translation (no training overhead)
- Strong EN-ZH performance
- Middle-ground pricing ($15/M)

### For European ↔ CJK Translation
→ **DeepL**
- 1.7x improvement for EN-JA, EN-ZH (2025)
- Strongest European language quality
- Good for multilingual content (European + CJK)
- Most expensive option

## CJK Quality Ranking (Estimated)

Based on documented features and claims:

1. **Google Cloud Translation** - Most extensive CJK training data, multiple models, longest track record
2. **DeepL** (with next-gen LLM) - Recent 1.7x improvement, linguist-verified gains for JA/ZH-CN
3. **Amazon Translate** - Strong EN-ZH results, "particularly strong" in Asian languages
4. **Azure Translator** - Competitive but fewer published benchmarks

*Note: S2/S3 will involve actual testing to validate these rankings*

## Cost Analysis (1B characters/year)

| Provider | Annual Cost | Monthly Average | Notes |
|----------|-------------|-----------------|-------|
| Azure | $10,000 | $833 | After 2M free/mo |
| Amazon | $15,000 | $1,250 | After 12-month free tier |
| Google | $20,000 | $1,667 | After 500K free/mo |
| DeepL | $25,000 + $66 | $2,089 | Base fee adds up at scale |

**Savings:** Azure saves $10K/year vs Google at 1B chars/year

## Key Differentiators

### Google: Most Complete Platform
- Multiple models (NMT, LLM, Custom)
- AutoML for custom training
- Glossary support
- Document + batch translation
- Vertex AI integration

### Azure: Best Value
- Lowest per-character cost
- Largest free tier
- Direct CJK-CJK pairs
- Custom models available
- Native Azure ecosystem

### Amazon: Unique ACT Approach
- On-the-fly customization (no pre-training)
- No hosting fees for customization
- Formality control
- S3 batch workflows
- AWS ecosystem native

### DeepL: Quality Leader (European)
- Next-gen LLM for JA/ZH-CN
- 1.7x quality improvement (verified)
- Formality control
- Document translation
- Voice translation

## Ecosystem Considerations

### Choose Google if:
- Already on Google Cloud
- Need Vertex AI integration
- Want most model flexibility
- CJK quality is paramount

### Choose Azure if:
- Cost is primary concern
- Already on Azure
- Need direct CJK-CJK pairs
- Want largest free tier

### Choose Amazon if:
- AWS-native stack
- Need dynamic customization (ACT)
- S3/Lambda integration matters
- Formality control required

### Choose DeepL if:
- European ↔ CJK translation
- Quality > cost for EN-JA/EN-ZH
- Document workflows
- Need voice translation

## Next Steps for S2-Comprehensive

1. **Quality testing** across all four APIs for same CJK text samples
2. **Feature deep-dive**: Glossaries, formality, batch processing
3. **Integration complexity**: SDK quality, documentation, developer experience
4. **Latency benchmarking**: Response times for typical requests
5. **Error handling**: Failure modes, rate limits, retry strategies
6. **Document translation**: Format preservation testing
7. **Custom model/terminology**: Setup complexity and quality gains

## Initial Recommendation (Pending S2/S3 validation)

**General-purpose CJK translation:** Google Cloud Translation Advanced
- Proven track record
- Best CJK language pair quality
- Most flexibility

**Cost-optimized production:** Azure Translator
- Half the cost of Google
- Competitive quality
- Generous free tier

**AWS users:** Amazon Translate
- Native ecosystem fit
- Unique ACT customization
- Good EN-ZH quality

**European-CJK bridge:** DeepL
- Strongest European languages
- Improving CJK quality (1.7x gain)
- Premium pricing justified for specific use cases
