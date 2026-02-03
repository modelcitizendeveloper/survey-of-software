# Amazon Polly

**Category**: Cloud TTS API
**Tier**: Enterprise cloud provider
**Status**: Production-ready, widely adopted
**Last Updated**: November 2025

---

## Overview

Amazon Polly is AWS's text-to-speech service, offering 60+ voices across 30+ languages. Built on neural TTS technology, it provides lifelike speech synthesis with features like Newscaster speaking style and custom lexicons.

## Key Features

### Voice Library
- **60+ voices** across **30+ languages**
- Voice types: Standard, Neural, Long-Form, Generative
- Newscaster speaking style for news-reading tone

### Advanced Capabilities
- **Neural voices**: Higher quality than standard voices
- **Brand Voice**: Custom neural voice training (create unique brand voices)
- **Speech marks**: Metadata about speech (phonemes, visemes, word timing)
- **Lexicons**: Custom pronunciation dictionaries

### Technical Features
- Real-time and asynchronous synthesis
- Streaming audio output
- SSML support for fine-grained control
- Multiple audio formats: MP3, OGG (Vorbis), PCM
- Sample rates: 8kHz, 16kHz, 22kHz, 24kHz (neural default: 24kHz)

### AWS Integration
- Native integration with Lambda, S3, Transcribe, Translate
- AWS SDK support (Python boto3, JavaScript, Java, etc.)
- CloudWatch metrics and logging

## Pricing

**Character-based pricing** (billed per million characters):

| Voice Type | Price per 1M chars |
|------------|-------------------|
| Standard voices | $4.00 |
| Neural voices | $16.00 |
| Long-Form voices | $100.00 |
| Generative voices | $30.00 |

**Free tier**:
- **Neural voices**: 1M characters/month for first 12 months
- **Standard voices**: 5M characters/month free forever
- **New AWS customers** (July 2025+): $200 in AWS Free Tier credits

**Example costs**:
- 100 hours of audio (~500K chars): $2-8 (Standard) or $8 (Neural)
- Language learning app (1,000 students × 50 sentences/day): ~$60/month (Neural)

## Language Learning Use Case

### Strengths
- ✅ Generous free tier (1M neural chars/month = ~2 hours/day audio)
- ✅ Excellent AWS integration (Lambda for on-demand synthesis)
- ✅ Speech marks for word-level timing (useful for highlighted text sync)
- ✅ Custom lexicons for pronunciation control
- ✅ Low latency and reliable infrastructure

### Weaknesses
- ❌ Fewer languages than Google (30 vs 75) and Azure (30 vs 140)
- ❌ Fewer voices per language than competitors
- ❌ Voice quality slightly behind Google/Azure neural voices
- ❌ Brand Voice (custom voices) expensive and requires AWS Enterprise Support

### Ideal For
- AWS-native applications (already using Lambda, S3, etc.)
- Apps requiring speech timing metadata (word-level sync)
- High-volume with free tier (1M chars/month free for 12 months)
- Custom pronunciation needs (lexicon support)

## Competitive Position

**vs. Google Cloud TTS**: Same pricing ($16/M neural), but fewer languages (30 vs 75)
**vs. Azure**: Same pricing ($16/M neural), but fewer languages (30 vs 140)
**vs. ElevenLabs**: 4× cheaper ($16 vs $66 effective), but ElevenLabs voice quality much higher
**vs. Open Source**: 4× more expensive, but AWS integration and zero maintenance

## Production Readiness

| Factor | Rating | Notes |
|--------|--------|-------|
| Voice Quality | ⭐⭐⭐⭐ | Good neural voices, not best-in-class |
| Latency | ⭐⭐⭐⭐⭐ | Excellent, especially with AWS regions |
| Language Support | ⭐⭐⭐ | 30+ languages (fewer than competitors) |
| Pricing | ⭐⭐⭐⭐ | Good free tier (1M neural/month × 12 months) |
| Reliability | ⭐⭐⭐⭐⭐ | 99.9% SLA, enterprise-grade |
| AWS Integration | ⭐⭐⭐⭐⭐ | Best AWS integration of any TTS service |

## Notable Features

### Speech Marks
Polly can return metadata about the speech:
- **Phoneme marks**: Phoneme boundaries (useful for lip-sync)
- **Viseme marks**: Visual mouth shapes (animation)
- **Word marks**: Word boundaries with timestamps
- **Sentence marks**: Sentence boundaries

Use case: Highlight text as audio plays (karaoke-style reading)

### Newscaster Style
Neural voices support "Newscaster" speaking style for news-reading tone:
```xml
<amazon:domain name="news">Breaking news: ...</amazon:domain>
```

## References

- [Amazon Polly](https://aws.amazon.com/polly/)
- [Pricing](https://aws.amazon.com/polly/pricing/)
- [Neural voices](https://docs.aws.amazon.com/polly/latest/dg/neural-voices.html)
- [Speech marks](https://docs.aws.amazon.com/polly/latest/dg/speechmarks.html)
