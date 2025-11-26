# TTS Platform Feature Matrix

**Last Updated**: November 25, 2025
**Platforms**: 7 (Google Cloud TTS, Amazon Polly, Azure TTS, ElevenLabs, Play.ht, Coqui TTS, Piper TTS)
**Features Evaluated**: 60+

---

## Legend

- ✅ = Fully supported
- ⚠️ = Partial support / Limited
- ❌ = Not supported
- 💰 = Paid add-on / Higher tier
- 🔧 = Requires custom implementation

---

## Voice & Language Features

| Feature | Google Cloud | Amazon Polly | Azure | ElevenLabs | Play.ht | Coqui | Piper |
|---------|-------------|--------------|-------|------------|---------|-------|-------|
| **Voice Count** | 380+ | 60+ | 400+ | Library | 800+ | Pre-trained | 200+ |
| **Language Count** | 75+ | 30+ | 140+ | 70+ | Multi | 17 | 50+ |
| **Neural Voices** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Standard Voices** | ✅ | ✅ | ⚠️ | ❌ | ❌ | ❌ | ❌ |
| **Multiple Accents** | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ❌ | ⚠️ |
| **Gender Options** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Child Voices** | ✅ | ⚠️ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ |
| **Voice Variety (per language)** | High | Medium | High | High | Very High | Low | Medium |

**Best language coverage**: Azure (140+)
**Best voice variety**: Play.ht (800+)
**Best accent diversity**: Google/Azure

---

## Voice Customization

| Feature | Google Cloud | Amazon Polly | Azure | ElevenLabs | Play.ht | Coqui | Piper |
|---------|-------------|--------------|-------|------------|---------|-------|-------|
| **Voice Cloning** | 💰 Custom Voice | 💰 Brand Voice | 💰 Custom Neural | ✅ | ✅ | ✅ | ❌ |
| **Clone Sample Length** | 10+ seconds | Training set | Training set | <1 minute | Short | 6 seconds | N/A |
| **Clone Quality** | Good | Good | Good | Excellent | Very Good | Good | N/A |
| **Professional Cloning** | 💰 | 💰 Enterprise | 💰 | 💰 Business | 💰 Enterprise | 🔧 Fine-tune | N/A |
| **Instant Cloning** | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Cross-Language Cloning** | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Voice Blending** | ❌ | ❌ | ❌ | ⚠️ | ❌ | 🔧 | ❌ |
| **Emotion Control** | ⚠️ SSML | ❌ | ⚠️ SSML | ✅ v3 model | ⚠️ | ⚠️ | ❌ |
| **Speaking Style** | ⚠️ | ✅ Newscaster | ⚠️ | ✅ | ⚠️ | ❌ | ❌ |
| **Custom Lexicons** | ✅ | ✅ | ✅ | ⚠️ | ✅ | 🔧 | ❌ |

**Best voice cloning**: ElevenLabs (quality) and Coqui (free, 6-second samples)
**Best emotion control**: ElevenLabs v3 model
**Best professional training**: Azure Custom Neural Voice

---

## Text Processing & Markup

| Feature | Google Cloud | Amazon Polly | Azure | ElevenLabs | Play.ht | Coqui | Piper |
|---------|-------------|--------------|-------|------------|---------|-------|-------|
| **SSML Support** | ✅ Full | ✅ Full | ✅ Full | ⚠️ Limited | ✅ | ⚠️ Basic | ⚠️ Basic |
| **Phoneme Support (IPA)** | ✅ | ✅ | ✅ | ❌ | ✅ | ⚠️ | ❌ |
| **Speed Control** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Pitch Control** | ✅ | ✅ | ✅ | ⚠️ | ✅ | ⚠️ | ⚠️ |
| **Volume Control** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| **Pauses** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Emphasis** | ✅ | ✅ | ✅ | ⚠️ | ✅ | ⚠️ | ❌ |
| **Prosody Tags** | ✅ | ✅ | ✅ | ⚠️ | ✅ | ⚠️ | ❌ |
| **Say-As (date, number)** | ✅ | ✅ | ✅ | ⚠️ | ✅ | ❌ | ❌ |
| **Substitution** | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Math/Formula Rendering** | ⚠️ | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | ❌ |

**Best SSML support**: Google/Amazon/Azure (full W3C compliance)
**Most flexible text control**: Azure (extended SSML tags)

---

## Audio Output

| Feature | Google Cloud | Amazon Polly | Azure | ElevenLabs | Play.ht | Coqui | Piper |
|---------|-------------|--------------|-------|------------|---------|-------|-------|
| **MP3 Output** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WAV Output** | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **OGG Output** | ✅ | ✅ Vorbis | ✅ | ❌ | ⚠️ | ✅ | ⚠️ |
| **PCM/RAW Output** | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| **FLAC Output** | ❌ | ❌ | ❌ | ✅ | ⚠️ | ✅ | ❌ |
| **Sample Rate Options** | 8-48 kHz | 8-24 kHz | 8-48 kHz | 24-44.1 kHz | Varies | 16-22 kHz | 16-22 kHz |
| **Bit Depth** | 16-bit | 16-bit | 16-bit | 16-24 bit | 16-bit | 16-bit | 16-bit |
| **Stereo Output** | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| **Background Music** | ❌ | ❌ | ❌ | ❌ | ❌ | 🔧 | ❌ |
| **Audio Effects** | ❌ | ❌ | ✅ | ❌ | ❌ | 🔧 | ❌ |

**Best audio quality**: ElevenLabs (up to 44.1 kHz, 24-bit)
**Most format options**: Google/Azure
**Best for post-processing**: Raw PCM output (Google, Azure, Coqui, Piper)

---

## Performance & Infrastructure

| Feature | Google Cloud | Amazon Polly | Azure | ElevenLabs | Play.ht | Coqui | Piper |
|---------|-------------|--------------|-------|------------|---------|-------|-------|
| **Real-time Synthesis** | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ GPU req | ✅ CPU |
| **Streaming Output** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Batch Processing** | ✅ | ✅ Async | ✅ | ✅ | ✅ | ✅ | ✅ |
| **First-Byte Latency** | <200ms | <200ms | <100ms | ~200ms | ~300ms | Variable | <50ms CPU |
| **Global CDN** | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | N/A | N/A |
| **Multi-Region** | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | 🔧 | 🔧 |
| **Offline Capability** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **GPU Acceleration** | N/A | N/A | N/A | N/A | N/A | ✅ | ⚠️ Optional |
| **CPU Efficiency** | N/A | N/A | N/A | N/A | N/A | ⚠️ Slow | ✅ Fast |
| **Edge Deployment** | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ | ✅ RPi |

**Lowest latency**: Azure (<100ms), Piper (<50ms CPU)
**Best offline**: Piper (Raspberry Pi compatible)
**Best real-time streaming**: Google/Azure

---

## API & Integration

| Feature | Google Cloud | Amazon Polly | Azure | ElevenLabs | Play.ht | Coqui | Piper |
|---------|-------------|--------------|-------|------------|---------|-------|-------|
| **REST API** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ Python | ✅ Python |
| **WebSocket API** | ❌ | ❌ | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| **gRPC API** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Python SDK** | ✅ | ✅ boto3 | ✅ | ✅ | ✅ | ✅ Native | ✅ Native |
| **JavaScript SDK** | ✅ | ✅ AWS SDK | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Java SDK** | ✅ | ✅ AWS SDK | ✅ | ⚠️ | ❌ | ❌ | ❌ |
| **C# SDK** | ✅ | ✅ AWS SDK | ✅ | ⚠️ | ❌ | ❌ | ❌ |
| **Go SDK** | ✅ | ✅ AWS SDK | ✅ | ⚠️ | ❌ | ❌ | ❌ |
| **CLI Tool** | ✅ gcloud | ✅ aws | ✅ az | ⚠️ | ❌ | ✅ | ✅ |
| **Webhooks** | ❌ | ❌ | ❌ | ⚠️ | ⚠️ | ❌ | ❌ |
| **Rate Limiting** | ✅ Quotas | ✅ | ✅ | ✅ | ✅ | N/A | N/A |
| **Concurrent Requests** | High | High | High | Tier-based | Tier-based | Unlimited | Unlimited |

**Best SDK support**: Google/Azure (most languages)
**Best AWS integration**: Amazon Polly (native boto3)
**Most flexible**: Open source (Coqui, Piper) - no rate limits

---

## Metadata & Analysis

| Feature | Google Cloud | Amazon Polly | Azure | ElevenLabs | Play.ht | Coqui | Piper |
|---------|-------------|--------------|-------|------------|---------|-------|-------|
| **Speech Marks** | ❌ | ✅ | ❌ | ❌ | ❌ | 🔧 | ❌ |
| **Word Timestamps** | ❌ | ✅ | ⚠️ Viseme | ❌ | ❌ | 🔧 | ❌ |
| **Phoneme Timestamps** | ❌ | ✅ | ❌ | ❌ | ❌ | 🔧 | ❌ |
| **Viseme Output** | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Sentence Marks** | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Duration Prediction** | ❌ | ❌ | ❌ | ❌ | ⚠️ Preview | 🔧 | 🔧 |
| **Character Count** | ✅ | ✅ | ✅ | ✅ | ✅ | N/A | N/A |

**Best metadata**: Amazon Polly (speech marks unique)
**Best for lip-sync**: Amazon Polly (visemes), Azure (visemes)
**Best for karaoke-style**: Amazon Polly (word timestamps)

---

## Language Learning Specific

| Feature | Google Cloud | Amazon Polly | Azure | ElevenLabs | Play.ht | Coqui | Piper |
|---------|-------------|--------------|-------|------------|---------|-------|-------|
| **Pronunciation Assessment** | ❌ | ❌ | ✅ Built-in | ❌ | ❌ | ❌ | ❌ |
| **IPA Phoneme Support** | ✅ | ✅ | ✅ | ❌ | ✅ | ⚠️ | ❌ |
| **Speed Adjustment** | ✅ 0.25-4x | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Multiple Accents** | ✅ | ⚠️ | ✅ 20+ | ⚠️ | ✅ | ❌ | ⚠️ |
| **Native Speaker Voices** | ✅ | ✅ | ✅ | ✅ | ✅ | 🔧 Clone | 🔧 Train |
| **Dialect Variety** | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ❌ | ⚠️ |
| **Language Mixing** | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ |
| **Sentence Highlighting** | ❌ | ✅ Marks | ⚠️ Viseme | ❌ | ❌ | 🔧 | ❌ |

**Best for language learning**: Azure (pronunciation assessment unique)
**Best accent variety**: Azure (20+ English accents)
**Best for highlighting**: Amazon Polly (word timestamps)

---

## Enterprise & Security

| Feature | Google Cloud | Amazon Polly | Azure | ElevenLabs | Play.ht | Coqui | Piper |
|---------|-------------|--------------|-------|------------|---------|-------|-------|
| **SLA** | ✅ 99.9% | ✅ 99.9% | ✅ 99.9% | ⚠️ | ⚠️ | N/A | N/A |
| **HIPAA BAA** | ✅ | ✅ | ✅ | 💰 Enterprise | 💰 Enterprise | ✅ Self-host | ✅ Self-host |
| **SOC 2** | ✅ | ✅ | ✅ | ✅ | ✅ | N/A | N/A |
| **GDPR Compliance** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Data Residency** | ✅ Regions | ✅ Regions | ✅ Regions | ⚠️ | ⚠️ | ✅ Full | ✅ Full |
| **SSO** | ✅ | ✅ | ✅ | 💰 Enterprise | 💰 Enterprise | N/A | N/A |
| **Audit Logs** | ✅ | ✅ CloudTrail | ✅ | 💰 | 💰 | 🔧 | 🔧 |
| **Encryption at Rest** | ✅ | ✅ | ✅ | ✅ | ✅ | 🔧 | 🔧 |
| **Encryption in Transit** | ✅ TLS | ✅ TLS | ✅ TLS | ✅ TLS | ✅ TLS | 🔧 | 🔧 |
| **Private Endpoints** | ✅ VPC | ✅ VPC | ✅ VNet | ❌ | ❌ | ✅ Self-host | ✅ Self-host |
| **On-Premises** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |

**Best enterprise compliance**: Google/Amazon/Azure (full SOC 2, HIPAA, etc.)
**Best data privacy**: Coqui/Piper (self-hosted, data never leaves premises)
**Best for healthcare**: Azure + self-hosted options

---

## Pricing & Billing

| Feature | Google Cloud | Amazon Polly | Azure | ElevenLabs | Play.ht | Coqui | Piper |
|---------|-------------|--------------|-------|------------|---------|-------|-------|
| **Free Tier** | ✅ 4M/mo | ✅ 1M/mo 12mo | ⚠️ F0 | ✅ 10K/mo | ✅ 12.5K/mo | ✅ Unlimited | ✅ Unlimited |
| **Pay-as-you-go** | ✅ | ✅ | ✅ | ❌ | ❌ | N/A | N/A |
| **Subscription** | ❌ | ❌ | ❌ | ✅ | ✅ | N/A | N/A |
| **Flat-rate Option** | ❌ | ❌ | ❌ | ❌ | ✅ $99/mo | N/A | N/A |
| **Volume Discounts** | ⚠️ Contact | ⚠️ Contact | ⚠️ Contact | ✅ Tiers | ✅ Annual | N/A | N/A |
| **Predictable Costs** | ⚠️ | ⚠️ | ⚠️ | ⚠️ Tiers | ✅ Unlimited | ✅ Fixed | ✅ Fixed |
| **Overage Charges** | ✅ | ✅ | ✅ | ✅ | ⚠️ Unlimited | ❌ | ❌ |
| **Invoice Billing** | ✅ | ✅ | ✅ | 💰 Enterprise | 💰 Enterprise | N/A | N/A |
| **Cost Tracking** | ✅ GCP | ✅ AWS | ✅ Azure | ⚠️ Dashboard | ⚠️ Dashboard | 🔧 | 🔧 |

**Most generous free tier**: Google (4M chars/month ongoing)
**Most predictable**: Play.ht Unlimited ($99/month flat)
**Best for startups**: Free tiers (Google, Amazon first year)

---

## Developer Experience

| Feature | Google Cloud | Amazon Polly | Azure | ElevenLabs | Play.ht | Coqui | Piper |
|---------|-------------|--------------|-------|------------|---------|-------|-------|
| **Documentation Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Code Examples** | ✅ Many | ✅ Many | ✅ Many | ✅ Good | ⚠️ Some | ⚠️ Some | ✅ Good |
| **Interactive Playground** | ✅ | ⚠️ Console | ✅ Studio | ✅ | ✅ | ❌ | ❌ |
| **Voice Preview** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ Samples |
| **Quickstart Time** | 5-10 min | 5-10 min | 10-15 min | 5 min | 5 min | 30-60 min | 15-30 min |
| **Learning Curve** | Low | Low | Medium | Low | Low | High | Medium |
| **Community Support** | ✅ Active | ✅ Active | ✅ Active | ✅ Growing | ⚠️ Small | ⚠️ Small | ⚠️ Small |
| **Official Support** | ✅ Paid | ✅ Paid | ✅ Paid | ✅ Paid | ✅ Paid | ❌ | ❌ |
| **Status Page** | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | N/A | N/A |

**Best docs**: Google/Amazon/Azure (enterprise-grade)
**Fastest start**: ElevenLabs/Play.ht (5 minutes to first audio)
**Steepest learning curve**: Coqui (requires ML/DevOps knowledge)

---

## Summary Score Cards

### Google Cloud TTS
**Strengths**: Language coverage (75+), free tier (4M/mo), SSML, documentation
**Weaknesses**: No voice cloning (unless paid Custom Voice), no speech marks
**Best for**: Multi-language apps, GCP ecosystem, free tier users
**Overall**: ⭐⭐⭐⭐ (4/5)

### Amazon Polly
**Strengths**: Speech marks (unique), AWS integration, free tier (1M/mo × 12mo)
**Weaknesses**: Fewer languages (30), no pronunciation assessment
**Best for**: AWS apps, karaoke-style highlighting, word timing
**Overall**: ⭐⭐⭐⭐ (4/5)

### Azure TTS
**Strengths**: Most languages (140+), pronunciation assessment (unique), visemes
**Weaknesses**: Higher learning curve, F0 free tier limited
**Best for**: Language learning, rare languages, Azure ecosystem
**Overall**: ⭐⭐⭐⭐⭐ (5/5) for language learning

### ElevenLabs
**Strengths**: Best voice quality (4.14 MOS), voice cloning, emotional expression
**Weaknesses**: 4-16× more expensive, limited SSML, startup risk
**Best for**: Premium apps, voice cloning, emotional content
**Overall**: ⭐⭐⭐⭐⭐ (5/5) for quality, ⭐⭐ (2/5) for cost

### Play.ht
**Strengths**: Huge voice library (800+), unlimited plan ($99/mo), voice cloning
**Weaknesses**: Smaller company risk, documentation gaps
**Best for**: High-volume apps (>6M chars/mo), voice variety
**Overall**: ⭐⭐⭐⭐ (4/5)

### Coqui TTS
**Strengths**: Free voice cloning (6-sec samples), $0/char, privacy (self-hosted)
**Weaknesses**: GPU required, company defunct, DevOps complexity
**Best for**: High volume (>10M/mo), privacy-critical, voice cloning
**Overall**: ⭐⭐⭐⭐ (4/5) for cost, ⭐⭐ (2/5) for ease-of-use

### Piper TTS
**Strengths**: Fastest CPU inference, Raspberry Pi compatible, offline, $0/char
**Weaknesses**: No voice cloning, basic features, lower quality
**Best for**: Edge devices, offline, real-time CPU synthesis
**Overall**: ⭐⭐⭐⭐ (4/5) for edge, ⭐⭐⭐ (3/5) for quality

---

## Feature Coverage by Category

| Category | Google | Amazon | Azure | ElevenLabs | Play.ht | Coqui | Piper |
|----------|--------|--------|-------|------------|---------|-------|-------|
| **Voice & Language** | 90% | 75% | 95% | 85% | 90% | 60% | 70% |
| **Customization** | 70% | 60% | 75% | 95% | 85% | 90% | 30% |
| **Text Processing** | 95% | 95% | 100% | 60% | 85% | 50% | 40% |
| **Audio Quality** | 85% | 75% | 90% | 100% | 80% | 80% | 70% |
| **Performance** | 90% | 90% | 95% | 85% | 80% | 70% | 95% |
| **API/Integration** | 95% | 95% | 95% | 80% | 75% | 60% | 60% |
| **Metadata** | 40% | 100% | 60% | 20% | 30% | 40% | 20% |
| **Enterprise** | 95% | 95% | 95% | 70% | 70% | 100% | 100% |
| **Developer UX** | 95% | 95% | 90% | 85% | 80% | 50% | 70% |

**Overall coverage**: Azure (88%) > Google (84%) > Amazon (82%) > ElevenLabs (76%) > Play.ht (74%) > Coqui (67%) > Piper (62%)

---

## Unique Features by Platform

**Google Cloud TTS**:
- AudioML conversational voices (disfluencies, emotional range)
- Natural-language prompts for voice styling

**Amazon Polly**:
- Speech marks (word/phoneme/viseme timestamps) — **UNIQUE**
- Newscaster speaking style

**Azure TTS**:
- Pronunciation assessment (phoneme-level feedback) — **UNIQUE**
- 140+ languages (most coverage) — **UNIQUE**
- Audio effects (reverb, EQ)

**ElevenLabs**:
- 4.14 MOS voice quality (best-in-class) — **UNIQUE**
- v3 emotional model (emotionally rich speech)
- Professional voice cloning quality

**Play.ht**:
- 800+ voice library (largest) — **UNIQUE**
- Unlimited plan ($99/month flat rate) — **UNIQUE**
- White-labeled audio players

**Coqui TTS**:
- Voice cloning with 6-second samples — **BEST FREE**
- Cross-language voice transfer (open source)
- Full self-hosted privacy

**Piper TTS**:
- Raspberry Pi 4 compatible — **UNIQUE**
- Fastest CPU inference (real-time on weak hardware) — **UNIQUE**
- <50ms latency on CPU

---

## Decision Matrix

Use this matrix to quickly identify which features matter for your use case:

### If you need...

**Pronunciation assessment** → Azure (only option)
**Speech marks/timestamps** → Amazon Polly (only full implementation)
**140+ languages** → Azure (most coverage)
**800+ voices** → Play.ht (most variety)
**Best voice quality** → ElevenLabs (4.14 MOS)
**Free voice cloning** → Coqui (6-second samples)
**Raspberry Pi** → Piper (only option)
**Unlimited flat rate** → Play.ht ($99/month)
**Best free tier** → Google (4M/month ongoing)
**AWS integration** → Amazon Polly (native)
**Privacy/HIPAA** → Coqui or Piper (self-hosted)
**Emotional expression** → ElevenLabs v3
**IPA phonemes** → Google/Amazon/Azure
**Fastest latency** → Azure (<100ms) or Piper (<50ms CPU)

---

## Next Steps

See companion documents:
- **02-pricing-tco.md**: Total cost of ownership for 6 volume scenarios
- **03-quality-latency-benchmarks.md**: Voice quality MOS scores and latency measurements
- **04-integration-complexity.md**: Time-to-first-audio comparison
