# Amazon Translate

**Category**: Cloud Translation Service
**Pricing**: $15/M characters (standard), $60/M (custom)
**Free Tier**: 2M characters/month for 12 months
**Languages**: 75 languages, 5,550 language pairs
**Last Updated**: November 26, 2025

---

## Overview

Amazon Translate is AWS's neural machine translation service, offering real-time and batch translation for 75 languages. Tightly integrated with AWS ecosystem (S3, Lambda, Comprehend), with uniform pricing across all AWS regions.

**Best for**: AWS ecosystem users, applications needing 75 languages, custom terminology without extra cost.

---

## Pricing

### Standard Translation
- **$15 per million characters**
- Uniform pricing across all AWS regions
- No separate charge for language detection
- Charged per character submitted (not per successful translation)

### Active Custom Translation (ACT)
- **$60 per million characters** (4× standard pricing)
- Uses parallel data for customization
- No need to build/maintain custom models
- Better quality for specialized domains

### Free Tier
- **2 million characters per month** for 12 months (new AWS accounts)
- **500,000 characters per month** for ACT for first 2 months
- After free tier expires: Pay $15/M standard pricing

### Pricing Examples

| Monthly Volume | Type | Monthly Cost | Cost per Translation (200 chars) |
|----------------|------|--------------|----------------------------------|
| 2M chars | Standard (free tier) | $0 | $0 |
| 5M chars | Standard | $45 | $0.003 |
| 10M chars | Standard | $150 | $0.003 |
| 100M chars | Standard | $1,500 | $0.003 |
| 10M chars | ACT (custom) | $600 | $0.012 |

**Cost comparison**: Amazon Translate ($15/M) matches Google Translate pricing, 40% cheaper than DeepL ($25/M).

---

## Features

### Translation Capabilities
- **Real-time translation**: Text translation via REST API
- **Batch translation**: Asynchronous processing for large volumes (via S3)
- **Document translation**: TXT, HTML, DOCX (preserves formatting for DOCX)
- **Language detection**: Automatic source language detection (no extra cost)
- **Active Custom Translation (ACT)**: Customize output with parallel data
- **Custom Terminology**: Up to 10,000 terms per file (no additional cost)

### Language Support (75 Languages)
**Western European**: English, German, French, Spanish, Italian, Portuguese, Dutch, Swedish, Danish, Finnish, Norwegian, Polish

**Eastern European**: Russian, Czech, Romanian, Bulgarian, Hungarian, Ukrainian

**Asian**: Chinese (Simplified/Traditional), Japanese, Korean, Hindi, Thai, Vietnamese, Indonesian, Malay, Tamil, Telugu, Bengali

**Middle Eastern**: Arabic, Hebrew, Persian, Turkish, Urdu

**Other**: Afrikaans, Albanian, Amharic, Armenian, Azerbaijani, Bosnian, Croatian, Estonian, Georgian, Greek, Gujarati, Hausa, Icelandic, Kannada, Kazakh, Latvian, Lithuanian, Macedonian, Malayalam, Maltese, Mongolian, Nepali, Pashto, Punjabi, Serbian, Sinhala, Slovak, Slovenian, Somali, Swahili, Tagalog, Uzbek

**Coverage**: 75 languages, **5,550 language pair combinations** (75 × 74)

**Notable gaps**: No Latin (Google Translate has Latin)

### Neural Machine Translation (NMT)
- **Deep learning models**: Context-aware translation (entire sentence)
- **Better than statistical/rule-based**: More fluent, natural-sounding output
- **Continuous improvement**: AWS updates models automatically

### AWS Integration
- **S3**: Batch translate documents stored in S3 buckets
- **Lambda**: Trigger translations from serverless functions
- **Comprehend**: Combine with sentiment analysis, entity extraction
- **CloudWatch**: Monitor usage, latency, errors
- **IAM**: Fine-grained access control

---

## Use Cases

### Best Fit
- **AWS ecosystem**: Already using S3, Lambda, EC2, etc.
- **Batch translation**: Large document collections in S3
- **Serverless workflows**: Lambda-triggered translations
- **Custom terminology**: Brand names, technical terms (up to 10K terms free)
- **Asian languages**: Better coverage than DeepL (Hindi, Thai, Vietnamese)

### Not Ideal For
- **Premium quality**: DeepL or LLM-based better for European languages
- **Latin or rare languages**: Not supported (use Google's 100+ languages)
- **Non-AWS users**: No advantage over Google Translate if not using AWS

---

## Strengths

1. **AWS integration**: Seamless with S3, Lambda, Comprehend, CloudWatch
2. **Competitive pricing**: $15/M matches Google, 40% cheaper than DeepL
3. **Large free tier**: 2M chars/month for 12 months (4× Google's 500K ongoing)
4. **Uniform pricing**: Same $15/M across all AWS regions (no regional variance)
5. **Custom terminology**: 10,000 terms per file at no extra cost
6. **Batch translation**: Asynchronous S3-to-S3 translation for large volumes
7. **Language coverage**: 75 languages (more than DeepL's 30, less than Google's 100+)
8. **Asian languages**: Better coverage than DeepL (Hindi, Thai, Vietnamese)

---

## Weaknesses

1. **Quality**: Moderate translation quality (behind DeepL for European languages)
2. **AWS-centric**: Best value only if already using AWS ecosystem
3. **No formality control**: Unlike DeepL's formal/informal tone
4. **Limited document formats**: Only TXT, HTML, DOCX (vs Google's PDF, PPTX, XLSX)
5. **Free tier limited**: 12 months only (vs Google's 500K/month permanent)
6. **No streaming**: Batch-only for document translation
7. **Smaller language coverage**: 75 languages (vs Google's 100+)

---

## Integration Complexity

### Time to First Translation
- **10-15 minutes**: Create AWS account, configure IAM, install boto3, send first request

### Sample Code (Python - boto3)
```python
import boto3

# Initialize client
translate = boto3.client('translate', region_name='us-east-1')

# Translate text
response = translate.translate_text(
    Text='Hello, world!',
    SourceLanguageCode='en',
    TargetLanguageCode='es'
)

print(response['TranslatedText'])  # "Hola, mundo!"
print(response['SourceLanguageCode'])  # Auto-detected if not specified
```

### Batch Translation (S3)
```python
# Start batch translation job
response = translate.start_text_translation_job(
    JobName='my-translation-job',
    InputDataConfig={
        'S3Uri': 's3://my-bucket/input/',
        'ContentType': 'text/plain'
    },
    OutputDataConfig={
        'S3Uri': 's3://my-bucket/output/'
    },
    DataAccessRoleArn='arn:aws:iam::123456789012:role/TranslateRole',
    SourceLanguageCode='en',
    TargetLanguageCodes=['es', 'fr', 'de']
)

job_id = response['JobId']

# Check job status
status = translate.describe_text_translation_job(JobId=job_id)
print(status['TextTranslationJobProperties']['JobStatus'])
```

### Custom Terminology
```python
# Create custom terminology
import csv

# Create CSV file
terminology_data = [
    ['en', 'es'],
    ['AWS', 'AWS'],  # Don't translate acronym
    ['Amazon Translate', 'Amazon Translate'],  # Keep brand name
]

with open('terminology.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(terminology_data)

# Upload to AWS
with open('terminology.csv', 'rb') as f:
    translate.import_terminology(
        Name='MyTerminology',
        MergeStrategy='OVERWRITE',
        TerminologyData={
            'File': f.read(),
            'Format': 'CSV'
        }
    )

# Use terminology in translation
response = translate.translate_text(
    Text='AWS powers Amazon Translate',
    SourceLanguageCode='en',
    TargetLanguageCode='es',
    TerminologyNames=['MyTerminology']
)
print(response['TranslatedText'])  # "AWS impulsa Amazon Translate"
```

**Complexity**: Medium (requires AWS account setup, IAM roles, boto3)

---

## Quality Benchmarks

### Translation Quality (Informal Assessment, 2025)
- **WMT competitions**: Typically ranks 3rd-4th (behind DeepL, Claude, GPT-4)
- **BLEU scores**: ~35-45 for European languages (similar to Google Translate)
- **Human evaluation**: "Good" ratings 60-70% (similar to Google, behind DeepL 75-80%)

### Language-Specific Performance

| Language Pair | Amazon Quality | Google Quality | DeepL Quality | Notes |
|---------------|----------------|----------------|---------------|-------|
| **English ↔ Spanish** | Good | Good | Excellent | - |
| **English ↔ French** | Good | Good | Excellent | DeepL stronger |
| **English ↔ German** | Good | Good | Excellent | DeepL stronger |
| **English ↔ Japanese** | Good | Good | Good | GPT-4/Claude stronger |
| **English ↔ Chinese** | Good | Good | Good | GPT-4/Claude stronger |
| **English ↔ Hindi** | Good | Good | N/A | Amazon supports, DeepL doesn't |

**Verdict**: Amazon Translate quality is **on par with Google Translate**, but **behind DeepL** for European languages and **behind GPT-4/Claude** for Asian languages.

---

## Language Learning Use Case

### Suitability for Language-Learning Apps

**Strengths**:
- **Asian language coverage**: Hindi, Thai, Vietnamese (DeepL doesn't support)
- **Large free tier**: 2M chars/month for 12 months = 200K-400K flashcard translations
- **AWS ecosystem**: If using AWS for hosting, storage, etc.
- **Custom terminology**: Language-specific vocabulary (e.g., Latin declensions)

**Weaknesses**:
- **No Latin**: Not supported (Google Translate has Latin)
- **Quality**: Moderate quality vs DeepL/LLMs
- **No formality**: Can't teach formal vs informal register
- **AWS overhead**: Requires AWS account, IAM setup (friction for small projects)

### Recommended For
- **AWS-hosted apps**: If already using AWS infrastructure
- **Asian language learning**: Hindi, Thai, Vietnamese (not supported by DeepL)
- **High-volume free tier**: 2M chars/month for 12 months

### Not Recommended For
- **Latin learning**: Not supported (use Google Translate)
- **European language quality**: DeepL better for German, French, Spanish
- **Non-AWS projects**: No advantage over Google Translate
- **Formality teaching**: Can't distinguish formal vs informal tone

---

## Key Decisions

### Amazon Translate vs Competitors

| Decision Factor | Amazon Translate | Google Translate | DeepL | GPT-4/Claude |
|-----------------|------------------|------------------|-------|--------------|
| **Price** | $15/M | $15/M | $25/M | $3-30/M tokens |
| **Free tier** | 2M/month 12mo | 500K/month ongoing | 500K/month | $5-10 credits |
| **Language coverage** | 75 | 100+ | 30+ | 100+ |
| **Quality** | Good | Good | Excellent | Excellent |
| **AWS integration** | Excellent | None | None | None |
| **Formality control** | No | No | Yes | Yes (prompts) |

**Choose Amazon Translate if**:
- Already using AWS ecosystem (S3, Lambda, EC2)
- Need batch translation from S3 buckets
- Need Asian languages not supported by DeepL (Hindi, Thai, Vietnamese)
- Want large free tier (2M/month for 12 months)
- Custom terminology critical (10K terms free)

**Choose Google Translate if**:
- Need 100+ language coverage (rare languages, Latin)
- Want permanent free tier (500K/month ongoing vs Amazon's 12 months)
- Not using AWS ecosystem (simpler API, no IAM setup)

**Choose DeepL if**:
- European language quality critical (German, French, Spanish)
- Translating business documents, formal content
- Budget allows $25/M premium
- Language coverage limited to 30+ is acceptable

**Choose GPT-4/Claude if**:
- Need context-aware, pedagogical translations
- Want translation explanations, cultural context
- Asian languages critical (better than Amazon/Google)
- Willing to build custom prompts

---

## References & Sources

- [Amazon Translate Pricing - AWS](https://aws.amazon.com/translate/pricing/)
- [Amazon Translate Features - AWS](https://aws.amazon.com/translate/details/)
- [AWS Amazon Translate Pricing Calculator](https://costgoat.com/pricing/amazon-translate)
- [Amazon Translate FAQs - AWS](https://aws.amazon.com/translate/faqs/)

---

## Bottom Line

**Amazon Translate** is the best choice **if you're already using AWS**. It offers the same pricing as Google Translate ($15/M), better free tier (2M/month for 12 months), and seamless integration with S3, Lambda, and other AWS services. Quality is moderate (on par with Google, behind DeepL), but the AWS integration premium makes it a no-brainer for AWS users.

**For language-learning apps**: Use Amazon Translate if **already hosting on AWS** and need **Asian languages** (Hindi, Thai, Vietnamese). Otherwise, use **Google Translate for broader coverage** (100+ languages, Latin) or **DeepL for European quality**.
