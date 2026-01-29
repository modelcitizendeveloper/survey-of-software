# Google Cloud Translation API

## Overview
Google Cloud Translation is the longest-established cloud translation service with extensive language support (100+ languages) and deep CJK expertise. Offers multiple translation engines including NMT, custom models, and LLM-based translation.

## CJK Language Support

### Supported Languages
- **Chinese**: Simplified (ZH-CN, ZH) and Traditional (ZH-TW)
- **Japanese**: Full support (JA), including romanized Japanese
- **Korean**: Full support (KO)

### Language Coverage
- 100+ languages total
- Strong historical focus on CJK pairs
- Romanized Japanese → English/Spanish/Chinese support
- All variants supported in v2 (Basic) and v3 (Advanced)

**Sources:**
- [Google Cloud Translation language support](https://docs.cloud.google.com/translate/docs/languages)
- [Cloud Translation overview](https://cloud.google.com/translate)

## Pricing (2026)

### Free Tier
- **500,000 characters/month** free (permanent, no expiration)

### Standard Translation
- **v2 Basic NMT**: $20 per 1 million characters
- **v3 Advanced NMT**: $20 per 1 million characters (same price, better features)

### LLM-based Translation (v3)
- **Standard LLM**: $10/M input + $10/M output = **$20/M effective**
- **Adaptive LLM**: $25/M input + $25/M output = **$50/M effective**

### Custom Models
- Tiered pricing: $80/M (0-250M), $60/M (250M-2.5B), $40/M (2.5B-4B), $30/M (4B+)

### Document Translation
- **Standard**: $0.08/page
- **Custom models**: $0.25/page

**Sources:**
- [Google Cloud Translation pricing](https://cloud.google.com/translate/pricing)
- [Pricing calculator](https://costgoat.com/pricing/google-translate)
- [G2 pricing overview](https://www.g2.com/products/google-cloud-translation-api/pricing)

## API Features

### v2 (Basic)
- Simple text translation
- Language detection
- RESTful API
- Fast (~100ms latency)

### v3 (Advanced)
- All v2 features plus:
- Glossary support (terminology consistency)
- Batch translation
- Document translation
- Custom model training (AutoML)
- Translation LLM access
- Model selection per request
- Transliteration

### Integration
- RESTful API (v2 and v3)
- gRPC API (v3 only)
- Client libraries for 10+ languages
- Google Cloud Console integration
- Authentication via service accounts/API keys

## CJK-Specific Considerations

### Strengths
- **Longest track record** for CJK translation
- Extensive CJK training data from Google's services
- Multiple model options (NMT, LLM, custom)
- Romanized Japanese support
- AutoML for domain-specific customization
- Document translation with formatting preservation

### Quality
- NMT model: ~100ms latency, highest quality at that latency
- Translation LLM: "significantly higher performance" than NMT
- Recent MQM error reduction across bidirectional translations
- Industry-standard baseline for CJK pairs

**Sources:**
- [Translation v3 advanced features](https://cloud.google.com/translate/docs/advanced/translating-text-v3)
- [Translation LLM announcement](https://cloud.google.com/blog/products/ai-machine-learning/google-cloud-translation-ai)
- [NMT quality overview](https://cloud.google.com/blog/products/gcp/cloud-translation-api-adds-more-languages-and-neural-machine-translation-enters-ga)

## Model Selection Strategy

| Model | Best For | Cost | Latency |
|-------|----------|------|---------|
| v2 Basic NMT | Simple, fast translation | $20/M | ~100ms |
| v3 Advanced NMT | Glossaries, batch jobs | $20/M | ~100ms |
| Translation LLM | Highest quality, context-aware | $20-50/M | Higher |
| Custom (AutoML) | Domain-specific terminology | $30-80/M | Similar |

## Use Case Fit

**Excellent for:**
- Production CJK translation at scale
- Applications needing custom terminology (glossaries)
- Document translation workflows
- Mixed CJK ↔ European language projects
- Teams already on Google Cloud

**Consider alternatives for:**
- Tiny projects under 500K chars/month (all providers have free tiers)
- Workflows requiring formality control (DeepL stronger here)
- Azure-native stacks (ecosystem integration)

## Ecosystem Integration
- Native Google Cloud service
- Integrates with Cloud Storage, Pub/Sub, BigQuery
- IAM-based access control
- Cloud Console monitoring
- Vertex AI integration for LLM workflows
