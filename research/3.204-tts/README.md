# 3.204: Text-to-Speech / Speech Synthesis

**Status**: S1+S2 Complete ✅ (November 25, 2025) | S3+S4 Planned
**Tier**: 3 (Managed Services)
**Category**: Speech & Audio AI
**Estimated Effort**: 8-10 hours (S1-S4), 12-16 hours if all phases
**Actual Effort**: 6 hours (3 hours S1, 3 hours S2)

---

## Overview

Text-to-speech (TTS) platform comparison for language learning applications. Evaluates 7 platforms across cloud enterprise (Google, Amazon, Azure), cloud premium (ElevenLabs, Play.ht), and open-source (Coqui, Piper) categories.

## Research Completed

### S1: Rapid Discovery ✅
**Status**: Complete (November 25, 2025)
**Documents**: 8 files, 1,523 lines, 109 KB

#### Platform Profiles
1. **Google Cloud TTS** - 380+ voices, 75+ languages, $16/M chars
2. **Amazon Polly** - 60+ voices, 30+ languages, $16/M chars, AWS integration
3. **Azure TTS** - 400+ voices, 140+ languages, pronunciation assessment
4. **ElevenLabs** - Best voice quality (4.14 MOS), $20-66/M chars
5. **Play.ht** - 800+ voices, $99/month unlimited plan
6. **Coqui TTS** - Open source, voice cloning (6-second samples), $0/char
7. **Piper TTS** - Open source, Raspberry Pi-compatible, $0/char

#### Key Findings
- **No universal winner**: Choice depends on volume, quality needs, budget
- **Azure unique**: Pronunciation assessment built-in (language learning)
- **Play.ht best value**: High volume >6M chars/month ($99/month flat)
- **ElevenLabs premium**: 4-16× more expensive, best voice quality
- **Open source**: $0/char but infrastructure complexity

### S2: Comprehensive Analysis ✅
**Status**: Complete (November 25, 2025)
**Documents**: 5 files, 2,202 lines, 96 KB

#### Delivered
- **01-feature-matrix.md** (373 lines): 60+ features × 7 platforms
- **02-pricing-tco.md** (451 lines): 6 volume scenarios, break-even analysis
- **03-quality-latency-benchmarks.md** (402 lines): MOS scores, latency measurements
- **04-integration-complexity.md** (677 lines): Time-to-first-audio, code complexity
- **00-README.md** (299 lines): S2 summary and decision frameworks

### S3: Need-Driven Scenarios ⏳
**Status**: Not started
**Planned**:
- Use case #1: Startup language learning app (1K users)
- Use case #2: Enterprise LMS (100K users)
- Use case #3: Voice assistant (real-time, edge)
- Use case #4: Audiobook production (long-form)
- Use case #5: Accessibility (screen readers, WCAG)
- Use case #6: Multi-language content localization

### S4: Strategic Analysis ⏳
**Status**: Not started
**Planned**:
- Vendor viability deep-dive (10-year survival probability)
- Lock-in mitigation strategies
- SSML standardization vs proprietary features
- Voice quality evolution trajectory (2025-2030)
- Pricing trends and market consolidation

---

## Quick Recommendations

### By Use Case

| Use Case | Recommended Platform | Rationale |
|----------|---------------------|-----------|
| **Language learning (basic)** | Google Cloud TTS | 75+ languages, SSML, $16/M, free tier |
| **Language learning (advanced)** | Azure TTS | Pronunciation assessment built-in |
| **Language learning (high volume)** | Play.ht Unlimited | $99/month flat rate (unlimited) |
| **Premium UX** | ElevenLabs | Best voice quality (4.14 MOS) |
| **Voice cloning (paid)** | ElevenLabs | Best quality cloning |
| **Voice cloning (free)** | Coqui TTS | 6-second samples, $0/char |
| **Edge/offline** | Piper TTS | Runs on Raspberry Pi |
| **AWS ecosystem** | Amazon Polly | Native AWS integration |

### By Volume

| Monthly Volume | Recommendation | Monthly Cost |
|----------------|---------------|--------------|
| <1M chars | Amazon Polly | Free (12 months) |
| 1-4M chars | Google Cloud TTS | Free (ongoing) |
| 4-6M chars | Google/Azure/Amazon | $64-96 |
| 6-20M chars | Play.ht Unlimited | $99 (flat rate) |
| 50M+ chars | Coqui or Piper | <$200 (self-host) |

### By Budget

| Budget | Platform | Notes |
|--------|----------|-------|
| **Free** | Google Cloud TTS | 4M chars/month free tier |
| **$0-100/month** | Play.ht Unlimited | $99/month unlimited |
| **$100-500/month** | Google/Azure/Amazon | 6-31M chars ($16/M) |
| **$500+/month** | ElevenLabs or self-host | Premium quality or scale |

---

## Critical Insights

### 1. Pricing Spread: $0 to $66/M Characters
- **Open source**: $0/char (+ infrastructure)
- **Cloud enterprise**: $16/M (Google, Amazon, Azure)
- **Cloud premium**: $20-66/M (ElevenLabs)
- **Break-even**: Self-host at >10M chars/month

### 2. Quality Gap: ElevenLabs vs Others
- **ElevenLabs**: 4.14 MOS (Mean Opinion Score)
- **Cloud providers**: ~3.8-4.0 MOS (clustered together)
- **Open source**: ~3.5-3.7 MOS (good but not premium)

### 3. Language Coverage: 17 to 140+ Languages
- **Azure**: 140+ languages (best-in-class)
- **Google**: 75+ languages
- **Piper**: 50+ languages
- **Amazon**: 30+ languages
- **Coqui**: 17 languages

### 4. Unique Features
- **Azure**: Only provider with pronunciation assessment
- **ElevenLabs/Play.ht/Coqui**: Voice cloning capabilities
- **Piper**: Only open-source running on Raspberry Pi
- **Amazon Polly**: Speech marks (word-level timing)

### 5. Break-Even Analysis
- **Play.ht Unlimited** cheaper than cloud at >6M chars/month
- **Self-hosted** cheaper than cloud at >10M chars/month
- **Cloud free tiers** best for <4M chars/month

---

## Integration Relationships

### Upstream (Inputs)
- **3.202 Speech-to-Text**: Transcription → TTS (voice assistants)
- **3.203 Translation**: Translation → TTS (multilingual audio)

### Downstream (Outputs)
- **3.205 Pronunciation Assessment**: TTS model audio → student speaks → scoring
- **Language-learning app**: Listening comprehension drills
- **Audiobook production**: Long-form content narration

### Adjacent (Related)
- **1.106.2 TTS Libraries** (Tier 1): Self-hosted alternatives
- **3.202 Speech & Audio AI**: Broader speech/audio ecosystem

---

## Trigger & Context

**Trigger**: Language-learning app integration (November 24, 2025)

**Business Need**:
- Generate native pronunciation audio for vocabulary practice
- Listening comprehension drills (80% of language apps use TTS)
- Cost-effective at scale ($4 for 100 hours of student practice)

**Research Question**:
Which TTS platform balances quality, cost, language coverage, and features for language learning apps?

**Answer**:
- **MVP/Basic**: Google Cloud TTS (free tier 4M chars/month, 75+ languages)
- **Advanced features**: Azure TTS (pronunciation assessment)
- **High volume**: Play.ht Unlimited ($99/month flat rate)
- **Premium**: ElevenLabs (best quality, 4× more expensive)

---

## File Structure

```
3.204-tts/
├── README.md (this file)
├── metadata.yaml
├── S1-rapid/
│   ├── 00-SYNTHESIS.md (comprehensive comparison)
│   ├── 01-google-cloud-tts.md
│   ├── 02-amazon-polly.md
│   ├── 03-azure-tts.md
│   ├── 04-elevenlabs.md
│   ├── 05-playht.md
│   ├── 06-coqui-tts.md
│   └── 07-piper-tts.md
├── S2-comprehensive/ (not started)
├── S3-need-driven/ (not started)
└── S4-strategic/ (not started)
```

---

## Next Actions

### Immediate (S1 Complete)
✅ Platform landscape documented
✅ Pricing comparison complete
✅ Quick recommendations ready
✅ Language learning specific guidance

### Short-Term (S2 Start)
- [ ] Build feature matrix (50+ features)
- [ ] Calculate TCO for 6 volume scenarios
- [ ] Conduct voice quality benchmarks
- [ ] Measure latency performance
- [ ] Document integration complexity

### Medium-Term (S3)
- [ ] Write 6 detailed use case scenarios
- [ ] Create architecture patterns
- [ ] Develop implementation guides

### Long-Term (S4)
- [ ] Analyze vendor viability
- [ ] Document lock-in mitigation
- [ ] Project voice quality evolution

---

## Related Research

- **3.202 Speech & Audio AI** ✅ (Completed Nov 24, 2025)
- **3.205 Pronunciation Assessment** ⏳ (Next in queue)
- **3.203 Translation & Localization** ⏳ (Planned)
- **1.106.2 TTS Libraries** ⏳ (Tier 1 self-hosted)

---

## Research Metadata

- **Code**: 3.204
- **Started**: November 25, 2025
- **S1 Completed**: November 25, 2025
- **S1 Documents**: 8 files, 1,523 lines, 109 KB
- **Platforms Evaluated**: 7 (3 cloud enterprise, 2 cloud premium, 2 open source)
- **S1 Effort**: 3 hours
- **Estimated Total**: 8-10 hours (S1-S4)
