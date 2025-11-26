# Speechace API

**Category**: Pronunciation Assessment API
**Tier**: Specialized language learning service
**Status**: Production-ready, established provider
**Last Updated**: November 2025

---

## Overview

Speechace is a **dedicated pronunciation assessment API** with patented technology for real-time speech scoring at the syllable and phoneme level. Provides detailed feedback on pronunciation, fluency, grammar, coherence, vocabulary, and relevance.

## Key Features

### Assessment Capabilities
- **Phoneme-level accuracy**: Pinpoint individual syllable and phoneme mistakes
- **Real-time scoring**: Immediate feedback on pronunciation
- **Fluency analysis**: Speech rate, pausing, hesitation, length of run, word correct per minute
- **Comprehensive scoring**: Pronunciation, fluency, grammar, coherence, vocabulary, relevance

### Language Support
- **Primary**: English (full support)
- **Beta**: Spanish (Castilian and Latin American), French
- **Total**: 15+ languages (expanding)

### Assessment Types

**1. Reading Assessment** (scripted):
- Student reads given text
- Scores pronunciation accuracy of each phoneme
- Identifies mispronunciations at syllable level

**2. Spontaneous Speech** (unscripted):
- Free-form speaking on given topics
- Transcription + pronunciation scoring
- Fluency and coherence evaluation

**3. Advanced Scoring**:
- **Describe-Image**: Score image descriptions
- **Retell-Lecture**: Score lecture retelling
- **Answer-Question**: Score question responses
- Content scoring aligned with PTE (Pearson Test of English)

### Scoring Alignment
- **IELTS** scores (International English Language Testing System)
- **PTE** scores (Pearson Test of English)
- **TOEFL** scores (Test of English as a Foreign Language)

Results closely correlated and comparable to official test scores.

## Technical Capabilities

### Audio Processing
- **Max audio length**: 2 minutes+ (long-form analysis)
- **Real-time streaming**: Supported
- **Audio formats**: WAV, MP3, others via API

### Assessment Metrics
- **Pronunciation score**: 0-100 scale
- **Fluency score**: Based on speaking rate, pauses, hesitations
- **Accuracy score**: Phoneme-level correctness
- **Completeness score**: How much of target text was read
- **Syllable stress**: Correct/incorrect stress patterns
- **Word-level scores**: Each word scored individually
- **Phoneme-level scores**: Each phoneme scored (most granular)

### API Integration
- **RESTful API**: HTTP POST requests
- **Response format**: JSON with detailed scores
- **SDKs**: None (use HTTP clients)
- **Authentication**: API key

## Pricing

**Model**: Contact for custom pricing (not publicly listed)

**Indicative pricing** (from industry sources):
- **$0.01-0.03 per assessment** (typical range)
- **Volume discounts**: Available for high usage
- **Free trial**: Available on all plans
- **Annual plans**: Discounted pricing available

**Example costs**:
- 1,000 assessments/month: ~$10-30/month
- 10,000 assessments/month: ~$100-300/month
- 100,000 assessments/month: Volume discount (contact sales)

**Note**: Pricing varies based on:
- Assessment type (reading vs spontaneous)
- Languages supported
- Volume commitments
- Contract terms

## Language Learning Use Case

### Strengths
- ✅ **Phoneme-level feedback**: Most granular assessment available
- ✅ **15+ languages**: Multi-language support (expanding)
- ✅ **Test alignment**: IELTS/PTE/TOEFL score correlation
- ✅ **Spontaneous speech**: Assess unscripted speaking
- ✅ **Real-time scoring**: Immediate feedback for students

### Weaknesses
- ❌ **Pricing opacity**: No public pricing (requires sales contact)
- ❌ **English-focused**: Spanish/French still in beta
- ❌ **No SDK**: Must use raw HTTP API
- ❌ **Limited languages**: 15+ vs Azure 32+

### Ideal For
- **Language learning apps**: Pronunciation drills with detailed feedback
- **Test prep platforms**: IELTS/PTE/TOEFL practice
- **Corporate training**: Business English pronunciation coaching
- **Education**: K-12 and higher ed language courses

### Not Ideal For
- **Rare languages**: Limited to 15+ languages
- **DIY projects**: Pricing requires sales contact
- **Low volume**: Minimum pricing may be high

## Competitive Position

**vs. Azure Pronunciation Assessment**:
- Speechace: 15+ languages, specialized provider, patented tech
- Azure: 32+ languages, Microsoft ecosystem, $1/hour transcription
- **Winner**: Speechace for English depth, Azure for language breadth

**vs. ELSA Speak**:
- Speechace: Multi-language (15+), API for integration
- ELSA: English-only, largest non-native audio dataset
- **Winner**: Speechace for multi-language, ELSA for English accuracy

**vs. Custom Whisper**:
- Speechace: Out-of-box phoneme scoring, no ML expertise required
- Whisper: DIY solution, requires fine-tuning and ML expertise
- **Winner**: Speechace for time-to-market, Whisper for cost at scale

## Production Readiness

| Factor | Rating | Notes |
|--------|--------|-------|
| Assessment Quality | ⭐⭐⭐⭐⭐ | Patented phoneme-level scoring |
| Language Support | ⭐⭐⭐⭐ | 15+ languages, English best |
| Pricing Transparency | ⭐⭐ | No public pricing, contact sales |
| Integration Complexity | ⭐⭐⭐⭐ | RESTful API, straightforward |
| Documentation | ⭐⭐⭐⭐ | Good API docs, examples |
| Reliability | ⭐⭐⭐⭐ | Production-ready, established |

## API Example

```python
import requests
import json

url = "https://api.speechace.com/api/scoring/text/v9/json"
headers = {"Content-Type": "application/json"}

payload = {
    "key": "YOUR_API_KEY",
    "dialect": "en-us",
    "text": "The quick brown fox jumps over the lazy dog",
    "audio_base64": "BASE64_ENCODED_AUDIO",
    "user_id": "student123"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
result = response.json()

# Extract scores
pronunciation_score = result['pronunciation_score']
fluency_score = result['fluency_score']
word_scores = result['word_score_list']  # Word-level scores
phoneme_scores = result['phoneme_score_list']  # Phoneme-level scores

print(f"Pronunciation: {pronunciation_score}/100")
print(f"Fluency: {fluency_score}/100")
```

## Assessment Response Example

```json
{
  "status": "success",
  "pronunciation_score": 85,
  "fluency_score": 78,
  "accuracy_score": 88,
  "completeness_score": 95,
  "word_score_list": [
    {
      "word": "quick",
      "pronunciation_score": 90,
      "syllable_score_list": [
        {"syllable": "quick", "phoneme_score_list": [
          {"phoneme": "k", "score": 95},
          {"phoneme": "w", "score": 85},
          {"phoneme": "ɪ", "score": 92},
          {"phoneme": "k", "score": 88}
        ]}
      ]
    }
  ]
}
```

## Use Cases

### 1. Pronunciation Drills
**Scenario**: Student practices 50 vocabulary words daily
- **Cost**: 50 assessments/day × $0.02 = **$1/day** = $30/month/student
- **Value**: Phoneme-level feedback identifies specific pronunciation errors
- **ROI**: Replaces human tutor ($30-50/hour) with automated scoring

### 2. Speaking Test Prep
**Scenario**: IELTS speaking practice (100 practice tests/month)
- **Cost**: 100 assessments × $0.02 = **$2/month/student**
- **Value**: IELTS-aligned scoring provides test score estimates
- **ROI**: IELTS test costs $250, practice helps improve score 1-2 bands

### 3. Corporate Training
**Scenario**: 100 employees practicing business English (10 assessments/month each)
- **Cost**: 1,000 assessments × $0.02 = **$20/month** for entire company
- **Value**: Pronunciation improvement for client-facing roles
- **ROI**: Better communication with international clients

## When to Choose Speechace

Choose Speechace when:
1. **English-focused** language learning (best support)
2. **Phoneme-level feedback** critical (most granular)
3. **Test prep** (IELTS/PTE/TOEFL alignment)
4. **Medium-high volume** (1,000+ assessments/month)
5. **Willing to contact sales** for pricing

Don't choose Speechace when:
1. **Rare languages** needed (limited to 15+)
2. **DIY/experimental** projects (pricing requires commitment)
3. **Low volume** (<100 assessments/month)
4. **Azure ecosystem** (already using Azure, pronunciation assessment built-in)

## References

- [Speechace API](https://www.speechace.com/api-plans/)
- [API Documentation](https://api-docs.speechace.com/)
- [Postman Collection](https://www.postman.com/speechace/speechace-s-public-workspace/collection/fwsskik/speechace-api)
