# Azure Translator API

## Overview
Azure Translator is Microsoft's cloud translation service with 130+ language support and modern neural machine translation (NMT). Offers the most generous free tier (2M chars/month) and lowest cost per character among major providers.

## CJK Language Support

### Supported Languages
- **Chinese**: Simplified (ZH-CN) and Traditional (ZH-TW)
- **Japanese**: Full support (JA)
- **Korean**: Full support (KO)

### CJK Translation Pairs
- JA ↔ KO (direct translation)
- JA ↔ ZH-CN (direct translation)
- ZH-CN ↔ ZH-TW (direct translation)
- All pairs with English as intermediate language

### Neural Machine Translation
- Modern NMT as default for all supported languages
- "Major advances in translation quality" over previous approaches
- Consistent quality across language pairs

**Sources:**
- [Azure Translator language support](https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support)
- [Azure Translator overview](https://azure.microsoft.com/en-us/products/ai-foundry/tools/translator)
- [Translator API languages](https://learn.microsoft.com/en-us/rest/api/translator/translator/languages)

## Pricing (2026)

### Free Tier (F0)
- **2 million characters/month** free (permanent)
- Includes: standard translation, language detection, bilingual dictionary, transliteration, custom training
- Most generous free tier among major providers

### Pay-as-You-Go (S1)
- **Standard translation**: **$10 per 1 million characters**
- **Document translation**: $10 per 1 million characters (text-based)
- **Image documents**: Price per thousand images (500 chars/image max)
- **Custom translation training**: $10/M source+target chars (capped at $300/training)
- **Custom model hosting**: $10/month per hosted model per region

### Commitment Tiers
- S1 commitment: 250M-4B chars/month (discounts for standard translation)
- C2-C4 tiers: Custom translation volume discounts
- Separate instances needed for mixed standard/custom high-volume use

**Cost Comparison:**
- Azure: **$10/M** (50% cheaper than Google/DeepL)
- Google: $20/M
- DeepL: $25/M

**Sources:**
- [Azure Translator pricing](https://azure.microsoft.com/en-us/pricing/details/translator/)
- [Pricing comparison](https://taia.io/resources/blog/deepl-vs-google-translate-vs-microsoft-translator-2025/)
- [Azure pricing Q&A](https://learn.microsoft.com/en-us/answers/questions/523290/pricing-page-details-of-cognitive-services-(transl)

## API Features

### Core Translation
- Text translation (REST API)
- Language detection
- Transliteration (script conversion)
- Bilingual dictionary lookup
- Sentence length detection

### Document Translation
- Native document format preservation
- Batch document translation
- Text-based documents (PDF, DOCX, etc.)
- Image document OCR + translation

### Custom Translation
- Custom model training with domain-specific data
- Glossary/terminology enforcement
- Model hosting in specific regions
- Training data validation

### Integration
- RESTful API (v3.0)
- Client SDKs for .NET, Python, JavaScript, Java
- Azure AI services integration
- Container deployment support
- Azure portal management

## CJK-Specific Considerations

### Strengths
- **Direct CJK-CJK pairs** (no intermediate English pivot)
- Competitive quality for CJK languages
- **Lowest cost** among major providers ($10/M)
- **Largest free tier** (2M chars vs 500K)
- Custom models for domain-specific CJK translation
- Native Azure ecosystem integration

### Limitations
- Less public quality benchmarking compared to Google/DeepL
- Smaller training dataset than Google (historically)
- Custom model training requires substantial effort
- Hosting fees for custom models add up

## Quality Considerations
- Modern NMT provides "major advances" in quality
- Industry-competitive for CJK pairs
- Custom models can improve domain-specific accuracy
- Less published quality metrics than competitors

## Use Case Fit

**Excellent for:**
- **Cost-sensitive production workloads** (50% cheaper than alternatives)
- **Development and testing** (2M free tier supports substantial prototyping)
- **Azure-native stacks** (ecosystem integration, IAM, monitoring)
- Direct CJK ↔ CJK translation (no English pivot)
- Document translation workflows

**Consider alternatives for:**
- Workflows where quality benchmarks matter more than cost
- Teams preferring Google Cloud ecosystem
- Projects requiring formality control (DeepL strength)
- Scenarios where the 1.5M character free tier difference matters

## Ecosystem Integration
- Native Azure AI service
- Azure Key Vault for secrets management
- Azure Monitor for observability
- Azure Cognitive Services suite member
- Container deployment (Azure Container Instances, Kubernetes)
- Azure Functions integration for serverless
