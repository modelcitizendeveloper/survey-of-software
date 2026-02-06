# DeepL API

## Overview
DeepL is a German-based neural machine translation service known for high-quality translations, particularly for European languages. Recently expanded CJK support with next-generation LLM models.

## CJK Language Support

### Supported Languages
- **Chinese**: Simplified (ZH-HANS) and Traditional (ZH-HANT)
- **Japanese**: Full support (JA)
- **Korean**: Full support (KO)

### Recent Improvements
- Next-gen LLM model available for Japanese and Simplified Chinese (2025)
- Blind tests show **1.7x improvement** over DeepL's previous model for EN↔JA and EN↔ZH-HANS pairs
- Voice translation support added for Mandarin, Japanese, and Korean
- Document translation enhanced for Traditional Chinese

**Sources:**
- [DeepL Translator languages](https://support.deepl.com/hc/en-us/articles/360019925219-DeepL-Translator-languages)
- [DeepL API supported languages](https://developers.deepl.com/docs/getting-started/supported-languages)
- [DeepL next-gen LLM announcement](https://www.prnewswire.com/news-releases/deepl-bolsters-api-with-next-gen-llm-model-and-write-functionality-302360279.html)

## Pricing (2026)

### DeepL API Free
- **500,000 characters/month** free

### DeepL API Pro
- **Base**: $5.49/month
- **Usage**: $25.00 per 1 million characters
- **Effective cost**: $0.000025 per character (2.5¢ per 1,000 chars)

### Comparison
- ~25% more expensive than Google Translate ($20/million)
- Base fee becomes negligible at scale
- Free tier is generous for low-volume use

**Sources:**
- [DeepL pricing guide 2025](https://www.eesel.ai/blog/deepl-pricing)
- [DeepL API plans](https://support.deepl.com/hc/en-us/articles/360021200939-DeepL-API-plans)
- [Character billing details](https://support.deepl.com/hc/en-us/articles/360020685720-Character-count-and-billing-in-DeepL-API)

## API Features

### Core Capabilities
- Text translation
- Document translation (.docx, .pptx, .pdf, .html, .txt)
- Glossary support for consistent terminology
- Formality control (formal/informal)
- Tag handling (preserve XML/HTML tags)

### Integration
- RESTful API
- Authentication via API key
- SDKs available for multiple languages
- Simple HTTP POST requests

## CJK-Specific Considerations

### Strengths
- Next-gen LLM specifically optimized for JA/ZH-CN
- Measurable quality improvements for CJK pairs
- Traditional Chinese document support
- Voice translation for all CJK languages

### Limitations
- Newer to CJK market compared to Google/Microsoft
- Less extensive training data for CJK compared to European languages
- Custom model training not available (glossaries only)

## Quality Claims
- 1.7x improvement over previous model for EN-JA, EN-ZH
- Linguist-verified blind tests
- Generally rated highest quality for European languages
- CJK quality improving but historically behind Google for Asian languages

## Use Case Fit
**Good for:**
- European ↔ CJK translations where DeepL's European language strength matters
- Applications needing formality control
- Document translation workflows
- Low to medium volume (generous free tier)

**Consider alternatives for:**
- Pure CJK ↔ CJK translation
- Very high volume (cost adds up)
- Custom model training requirements
- Localization workflows needing extensive language variants
