# Domain Explainer: Text-to-Speech (TTS) Technical Concepts

**Audience**: Business decision-makers, non-technical founders, product managers
**Purpose**: Explain technical terminology and concepts in text-to-speech technology
**Focus**: "What does this term mean?" NOT "Which platform should I choose?"

**Reading time**: 20-25 minutes

---

## Core Technology Concepts

### What is Text-to-Speech (TTS)?

**Text-to-speech** converts written text into spoken audio. Modern neural TTS systems can generate human-like speech with natural intonation, pauses, and emotional expression.

**How it works** (simplified):
1. **Text preprocessing**: Normalize text (expand abbreviations, numbers → words)
2. **Phoneme conversion**: Text → phonetic units (/həˈloʊ/ for "hello")
3. **Acoustic model**: AI generates audio waveforms from phonemes
4. **Vocoder**: Converts waveforms into final audio (MP3, WAV)

**Example**: Input "The meeting is at 3pm" → AI processes → Outputs audio saying "The meeting is at three P M"

---

## Voice Quality & Naturalness

### Mean Opinion Score (MOS)

**What it means**: Industry-standard metric for voice quality. Human listeners rate audio on 1-5 scale.

**MOS Scale**:
- **4.0-5.0**: Excellent (indistinguishable from human)
- **3.5-3.9**: Very good (clearly synthetic but natural-sounding)
- **3.0-3.4**: Good (acceptable for most applications)
- **2.5-2.9**: Fair (robotic, limited use cases)
- **<2.5**: Poor (unusable for most applications)

**Example scores**:
- **Human speech**: 4.5-4.7 MOS (baseline)
- **Premium neural TTS**: 4.0-4.2 MOS (ElevenLabs, Google WaveNet)
- **Standard neural TTS**: 3.8-3.9 MOS (most cloud providers)
- **Legacy TTS** (pre-2018): 3.0-3.3 MOS (robotic voices)

**Why it matters**: 0.2 MOS difference noticeable to listeners. Premium apps (audiobooks, meditation, language learning) need 4.0+ MOS.

---

### Prosody

**What it means**: Natural rhythm, stress, and intonation patterns of speech.

**Components**:
- **Stress**: Emphasis on syllables ("REcord" noun vs "reCORD" verb)
- **Intonation**: Pitch patterns (rising pitch for questions "Going home?")
- **Rhythm**: Speaking pace, pauses between phrases
- **Tone**: Emotional coloring (excited, sad, formal, casual)

**Good prosody**:
"I didn't say he stole the money" (7 different meanings depending on stress)

**Poor prosody**:
Robotic monotone with incorrect word stress, no pauses, flat pitch.

**Business value**: Natural prosody increases listener engagement by 30-40% (audiobooks, e-learning, voice assistants).

---

### Neural Voices vs Standard Voices

**Standard voices** (pre-2018 technology):
- **Method**: Concatenative synthesis (stitch together recorded speech fragments)
- **Quality**: 3.0-3.3 MOS (robotic, unnatural pauses)
- **Cost**: $4/M characters (cheaper)
- **Use case**: Basic announcements, legacy systems

**Neural voices** (2018+ deep learning):
- **Method**: AI-generated speech from scratch using neural networks
- **Quality**: 3.8-4.2 MOS (human-like)
- **Cost**: $16/M characters (typical cloud pricing)
- **Use case**: Customer-facing applications, premium content

**Technology leap**: Neural TTS (2018 WaveNet) improved MOS from 3.3 → 4.0 (comparable to human speech).

---

## Voice Customization

### Voice Cloning

**What it means**: Create a synthetic voice that sounds like a specific person using audio samples.

**How it works**:
1. **Record voice samples**: 6 seconds to 10 minutes (depending on provider)
2. **AI training**: Extract voice characteristics (pitch, tone, accent, speaking style)
3. **Synthesis**: Generate new speech in cloned voice
4. **Cross-language**: Clone can speak languages original speaker doesn't (some providers)

**Example**: Record 1 minute of your CEO speaking English → AI generates product announcements, training videos in CEO's voice.

**Quality tiers**:
- **Instant cloning** (6-60 seconds): 80-90% similarity, slight artifacts
- **Professional cloning** (10+ minutes): 95-98% similarity, indistinguishable for most listeners

**Ethical considerations**: Requires consent from voice owner. Many providers require proof of authorization.

---

### SSML (Speech Synthesis Markup Language)

**What it means**: XML-based markup language to control pronunciation, emphasis, pauses, and pitch.

**Common tags**:
- `<break time="500ms"/>` - Insert 500ms pause
- `<emphasis level="strong">important</emphasis>` - Emphasize word
- `<prosody rate="slow" pitch="+2st">slow speech</prosody>` - Adjust speed and pitch
- `<phoneme ph="həˈloʊ">hello</phoneme>` - Override pronunciation
- `<say-as interpret-as="date">2025-11-25</say-as>` - Format dates, numbers

**Example without SSML**:
Text: "Dr. Smith will see you at 3pm on 11/25/2025"
Audio: "Doctor Smith will see you at three P M on eleven slash twenty-five slash two thousand twenty-five"

**Example with SSML**:
```xml
<speak>
  Doctor <break time="200ms"/> Smith will see you at
  <say-as interpret-as="time">3pm</say-as> on
  <say-as interpret-as="date" format="mdy">11/25/2025</say-as>
</speak>
```
Audio: "Doctor [pause] Smith will see you at three PM on November twenty-fifth, twenty twenty-five"

**Business value**: SSML enables precise pronunciation control for technical terms, product names, brand names.

---

### Phoneme-Level Control

**What phonemes are**: Smallest units of sound in language (e.g., /p/, /b/, /t/, /d/)

**Why it matters**: Some words have non-standard pronunciation:
- "SQL" → some say "sequel", others "S Q L"
- "GIF" → "gif" (hard G) or "jif" (soft G)
- "Data" → "day-tuh" or "dah-tuh"

**IPA (International Phonetic Alphabet)**: Standard notation for phonemes
- "hello" → /həˈloʊ/
- "goodbye" → /ɡʊdˈbaɪ/

**SSML phoneme tag**:
```xml
<phoneme alphabet="ipa" ph="ɛs kjuː ɛl">SQL</phoneme>
```
Forces "S Q L" pronunciation (not "sequel").

**Use cases**:
- Product names: "Nike" → /ˈnaɪki/ (not "nīk")
- Technical jargon: "Kubernetes" → correct pronunciation
- Brand consistency: Ensure standardized pronunciation across all audio

---

## Performance & Technical Metrics

### Real-Time Factor (RTFx)

**What it means**: How fast audio is generated compared to audio duration.

**Formula**: RTFx = (Audio duration) / (Generation time)

**Examples**:
- **10× real-time**: 10 seconds of audio generated in 1 second
- **1× real-time**: 10 seconds of audio generated in 10 seconds (slow)
- **0.5× real-time**: 10 seconds of audio generated in 20 seconds (too slow)

**Typical speeds**:
- **Cloud TTS APIs**: 5-10× real-time (10-second audio in 1-2 seconds)
- **Local CPU TTS**: 2-5× real-time (10-second audio in 2-5 seconds)
- **GPU-accelerated**: 10-50× real-time (10-second audio in 0.2-1 seconds)

**Business value**: Faster RTF enables real-time applications (voice assistants, live dubbing, interactive games).

---

### First-Byte Latency

**What it means**: Time from sending text request to receiving first audio chunk.

**Latency levels**:
- **<100ms**: Excellent (real-time voice assistants, conversational AI)
- **100-300ms**: Very good (interactive applications)
- **300ms-1 second**: Acceptable (button-click scenarios)
- **>1 second**: Poor (users perceive lag)

**Example**: User says "What's the weather?" → Voice assistant responds:
- **Low latency** (<200ms): Feels instant, natural conversation
- **High latency** (>1s): Noticeable pause, feels broken

**Why it varies**: Cloud APIs have network round-trip time, local inference has no network delay.

---

### Streaming vs Batch Synthesis

**Streaming TTS**:
- Audio chunks sent as generated (incremental playback)
- **Latency**: Low (first chunk arrives in <300ms)
- **Use case**: Real-time voice assistants, live narration
- **User experience**: Audio starts playing immediately, rest streams in

**Batch TTS**:
- Entire audio file generated, then sent
- **Latency**: Higher (wait for full synthesis)
- **Use case**: Audiobook generation, pre-recorded content
- **User experience**: Wait 5-30 seconds, then play complete audio

**Example**:
- Audiobook (10,000 words): Batch synthesis (5-minute wait, then play)
- Voice assistant response (20 words): Streaming (audio starts in <300ms)

---

## Audio Format & Quality

### Sample Rate

**What it means**: Audio samples per second (Hz). Higher sample rate = higher quality, larger files.

**Common rates**:
- **8 kHz**: Phone quality (low, telephony)
- **16 kHz**: Voice quality (acceptable for speech)
- **22.05 kHz**: Good quality (podcasts, voice apps)
- **24 kHz**: High quality (neural TTS default)
- **44.1 kHz**: CD quality (music, premium audio)
- **48 kHz**: Professional audio (video production)

**File size impact**:
- 1 hour of audio at 16 kHz = ~15 MB (MP3, 64 kbps)
- 1 hour of audio at 24 kHz = ~22 MB (MP3, 96 kbps)
- 1 hour of audio at 48 kHz = ~43 MB (MP3, 192 kbps)

**Recommendation**: 24 kHz for voice apps (best balance of quality + file size).

---

### Audio Formats

**MP3**:
- **Compression**: Lossy (smaller files, slight quality loss)
- **File size**: 1 MB per minute (typical)
- **Use case**: Web apps, mobile apps (widely supported)

**WAV**:
- **Compression**: Uncompressed (large files, perfect quality)
- **File size**: 10 MB per minute (10× larger than MP3)
- **Use case**: Audio editing, professional production

**OGG (Vorbis)**:
- **Compression**: Lossy (similar to MP3)
- **File size**: 0.8 MB per minute (slightly smaller than MP3)
- **Use case**: Open-source preference, web apps

**FLAC**:
- **Compression**: Lossless (smaller than WAV, perfect quality)
- **File size**: 5 MB per minute (50% smaller than WAV)
- **Use case**: Archival, high-quality audio storage

**Business decision**: MP3 for 99% of applications (best compatibility + file size).

---

## Language & Accent Support

### Language vs Locale

**Language**: Broad category (English, Spanish, French)

**Locale**: Region-specific variant (en-US, en-GB, en-AU)

**Why locales matter**:
- **en-US** (American): "color", "aluminum", rhotic "r"
- **en-GB** (British): "colour", "aluminium", non-rhotic "r"
- **en-AU** (Australian): Rising intonation, unique vowel sounds

**Example**: "Tuesday at 3pm"
- **en-US**: "TUESday" (stress first syllable)
- **en-GB**: "tuesDAY" (stress second syllable, subtle)

**Business value**: Match voice locale to target audience (en-GB voice for UK customers, not en-US).

---

### Multilingual vs Language-Specific Models

**Language-specific models**:
- Trained on single language (English-only, Spanish-only)
- **Quality**: Higher accuracy, better pronunciation
- **Limitation**: Can't handle code-switching (mixing languages)

**Multilingual models**:
- Trained on 50-100 languages simultaneously
- **Quality**: Slightly lower per-language accuracy
- **Advantage**: Handle code-switching ("Let's meet at Café de Paris")

**Example**:
- **Multilingual**: "The restaurant is called El Churrasco" (English + Spanish word, natural pronunciation)
- **English-only**: "The restaurant is called El Churrasco" (butchered Spanish pronunciation)

**Use case**: Language learning apps benefit from multilingual models (mix English explanations with target language words).

---

## Cost Models & Pricing

### Character-Based Pricing

**What it means**: Pay per character sent to TTS API (including spaces, punctuation).

**Example**:
- Text: "Hello, world!" (13 characters)
- Price: 13 × ($16 / 1,000,000) = $0.000208 (less than 1 cent)

**Cost per audio minute** (assuming 1,000 characters = 2 minutes of audio):
- $16/M characters = $8/hour of audio

**Typical pricing tiers**:
- **Standard voices**: $4/M characters ($2/hour of audio)
- **Neural voices**: $16/M characters ($8/hour of audio)
- **Premium voices** (voice cloning): $24-100/M characters ($12-50/hour)

**Estimation formula**: 100 words ≈ 500 characters ≈ 1 minute of audio

---

### Flat-Rate vs Usage-Based

**Usage-based (pay-per-character)**:
- **Cost**: $0.003-$0.016/minute of audio ($0.18-$1/hour)
- **Advantage**: Only pay for what you use
- **Disadvantage**: Unpredictable costs if volume spikes
- **Best for**: Variable usage (100 hours one month, 10 hours next month)

**Flat-rate (unlimited subscription)**:
- **Cost**: $99/month (example: Play.ht Unlimited)
- **Advantage**: Predictable budgeting, no overage surprises
- **Disadvantage**: Overpaying if low usage (<6M characters/month)
- **Best for**: High-volume, predictable workloads (>10 hours/day)

**Break-even example**:
- Flat rate: $99/month
- Usage-based: $16/M characters
- Break-even: $99 / $16 × 1M = 6.2M characters/month
- **If <6.2M chars/month**: Usage-based cheaper
- **If >6.2M chars/month**: Flat-rate cheaper

---

## Infrastructure & Deployment

### Cloud API vs Self-Hosted

**Cloud API** (e.g., Google Cloud TTS, Amazon Polly):
- **Setup**: Minutes (API key, start sending requests)
- **Cost**: $4-16/M characters
- **Advantages**: Zero infrastructure, auto-scaling, enterprise features
- **Disadvantages**: Per-character costs, audio leaves your servers (privacy)

**Self-hosted** (e.g., Coqui TTS, Piper TTS on your servers):
- **Setup**: Days to weeks (install dependencies, configure servers, test)
- **Cost**: $0/character (infrastructure only: $10-1,500/month)
- **Advantages**: Privacy (data never leaves premises), unlimited usage
- **Disadvantages**: DevOps complexity, maintenance burden

**Break-even analysis**:
- Cloud API: 10M characters/month × $16/M = $160/month
- Self-hosted: $200/month infrastructure + $0 variable costs
- **Break-even**: ~12M characters/month

**When self-hosted makes sense**:
- Privacy-critical (healthcare, finance, government)
- High volume (>20M characters/month, cost savings)
- Offline requirements (no internet connectivity)

**Misconception**: "Self-hosted is always cheaper" - FALSE for low volume (<5M chars/month). Cloud APIs avoid upfront setup cost.

---

### GPU vs CPU Inference

**GPU inference** (Graphics Processing Unit):
- **Speed**: 10-50× faster than CPU
- **Cost**: $200-1,500/month (GPU server rental)
- **Use case**: Real-time applications, high-volume batch processing

**CPU inference**:
- **Speed**: 2-5× real-time (acceptable for batch processing)
- **Cost**: $10-100/month (CPU server)
- **Use case**: Low-latency-tolerant applications, cost-sensitive

**Example (10 seconds of audio)**:
- **GPU**: 0.2-1 second generation time (very fast)
- **CPU**: 2-5 seconds generation time (acceptable for batch)

**Business decision**: CPU sufficient for 90% of applications (batch audiobook generation, offline use). GPU needed for real-time voice assistants (<300ms latency requirement).

---

## Specialized Features

### Voice Cloning Sample Length

**Why sample length matters**: Longer samples = better voice clone accuracy.

**Sample length tiers**:
- **6-10 seconds**: 70-80% similarity (acceptable for basic cloning)
- **30-60 seconds**: 85-90% similarity (good quality)
- **5-10 minutes**: 95-98% similarity (professional quality)

**Trade-offs**:
- **Short samples** (6 seconds): Quick setup, lower accuracy, artifacts
- **Long samples** (10 minutes): Time-consuming recording, high accuracy, indistinguishable

**Example**: Clone CEO voice for company announcements
- **6 seconds**: Sounds like CEO but listeners notice "something off"
- **10 minutes**: Indistinguishable from real CEO (unless listeners know voice intimately)

---

### Cross-Language Voice Cloning

**What it means**: Clone voice in Language A, use to generate speech in Language B.

**Example**:
- Record English speaker for 1 minute
- Clone voice
- Generate Spanish speech in cloned English speaker's voice
- **Result**: Spanish words spoken with English speaker's pitch, tone, accent characteristics

**Limitation**: AI can't perfectly preserve voice across languages (phonetic differences). Spanish "r" sounds different than English "r" - cloned voice approximates but isn't perfect.

**Use case**: Multilingual e-learning (same instructor voice across all language courses), international brand consistency.

---

## Privacy & Compliance

### Data Retention Policies

**What it means**: How long TTS provider stores your text input and generated audio.

**Retention models**:
- **Zero retention**: Text deleted immediately after synthesis (best privacy)
- **30-day retention**: Stored for debugging, deleted after 30 days (typical)
- **Indefinite retention**: Stored permanently for model improvement (privacy risk)

**Privacy implications**:
- Text input may contain PII (Personally Identifiable Information)
- Audio output may contain confidential information
- GDPR/CCPA require data deletion on request

**Business decision**: Choose zero-retention or 30-day providers for sensitive applications (medical, legal, financial).

---

### HIPAA Compliance

**What it means**: U.S. healthcare privacy law requiring Business Associate Agreement (BAA) for handling Protected Health Information (PHI).

**PHI in TTS context**:
- Patient names in text ("John Smith's prescription is ready")
- Medical terms ("Diagnosis: diabetes")
- Appointment details ("Your appointment is Tuesday at 3pm")

**HIPAA requirements for TTS**:
1. **BAA signed**: Legal contract with provider
2. **Encryption**: Data encrypted in transit (HTTPS) and at rest
3. **Access controls**: Only authorized users can access audio
4. **Audit logs**: Track who accessed what data when
5. **Data deletion**: Delete PHI on request

**Providers offering HIPAA BAA**: Some (typically enterprise tier, not free tier)

**Misconception**: "HIPAA-compliant" doesn't mean secure - means contractual obligations exist. Still need to verify actual security practices.

---

## Common Misconceptions

### "All TTS sounds robotic now"
**Reality**: 2018+ neural TTS (4.0 MOS) sounds human-like. Legacy pre-2018 TTS (3.3 MOS) sounds robotic. 90% of modern cloud TTS uses neural voices.

### "Voice cloning requires hours of audio"
**Reality**: Modern AI can clone voices with 6-60 seconds of audio (80-90% similarity). Professional cloning (95-98% similarity) needs 5-10 minutes.

### "Self-hosted TTS is always cheaper"
**Reality**: Break-even at ~10M characters/month ($160 cloud vs $200 self-hosted). Below that, cloud APIs cheaper (avoid setup costs, maintenance).

### "Higher sample rate always better"
**Reality**: Diminishing returns above 24 kHz for speech. 24 kHz (neural TTS default) sufficient for 99% of applications. 48 kHz overkill (2× file size, no perceptible quality improvement for voice).

### "TTS can speak any language"
**Reality**: Model must be trained on language. 70-140 languages supported (depending on provider), not all 7,000+ world languages. Rare languages not supported.

### "Free tier TTS is low quality"
**Reality**: Free tiers often use same AI models as paid tiers (neural voices). Limitation is quota (characters/month), not quality.

### "Voice cloning requires consent"
**Reality**: Legally yes (most jurisdictions), technically no (AI can clone any voice from audio sample). Ethical providers require proof of authorization.

### "SSML works everywhere"
**Reality**: Cloud providers support SSML (Google, Amazon, Azure). Some premium providers (ElevenLabs) have limited SSML support. Open-source varies.

---

## Strategic Concepts

### Commoditization of TTS

**What it means**: TTS accuracy plateaus at "good enough" (4.0 MOS), making basic TTS a commodity.

**Trend** (2018-2025):
- **2018**: WaveNet launches (4.0 MOS, revolutionary)
- **2020**: Neural TTS standard across providers (3.8-4.0 MOS)
- **2025**: Marginal improvements (4.0-4.2 MOS, most users can't tell difference)

**Implication**: Platforms compete on price, features, ecosystem integration (not raw voice quality, which is "good enough").

**Example**: 2018 → TTS cost $20/hour. 2025 → TTS cost $4-8/hour (60-75% price drop as commodity).

---

### Lock-In Risk

**What it means**: Difficulty switching TTS providers once integrated.

**Lock-in factors**:
1. **API-specific code**: Platform-specific API requires code rewrite
2. **Voice consistency**: Brand uses specific voice, hard to match elsewhere
3. **Custom voice cloning**: Investment in professional voice clone (95% similarity) lost if switching
4. **SSML lock-in**: Platform-specific SSML tags don't work elsewhere

**Mitigation strategies**:
- **Abstraction layer**: Wrapper API isolates platform-specific code (reduces rewrite cost 80%)
- **SSML standardization**: Use only W3C-standard SSML tags (portable across providers)
- **Voice portability**: Clone voices with multiple providers (avoid single-provider dependency)

**Low lock-in**: Cloud APIs with standard SSML (Google, Amazon, Azure)
**High lock-in**: Custom voice training, proprietary features (professional cloning, platform-specific voices)

---

## Future Trajectory (2025-2030)

### Voice Quality Plateau

**Current state** (2025): 4.0-4.2 MOS (near-human quality)

**Future expectation** (2030): 4.3-4.5 MOS (marginal improvements)

**Implication**: Quality differentiation shrinks. Platforms compete on:
- **Cost**: Price drops 30-50% (commoditization)
- **Features**: Voice cloning, emotional expression, multimodal
- **Latency**: <100ms real-time streaming
- **Ecosystem**: Integration with other AI services

---

### Emotional Expression

**Current state** (2025): Some providers offer emotional models (happy, sad, angry, neutral)

**Future expectation** (2030): Fine-grained emotional control
- **Granular emotions**: Excited, sarcastic, empathetic, frustrated (16+ emotions)
- **Dynamic emotions**: Emotion changes mid-sentence ("I was happy, but now I'm sad")
- **Context-aware**: AI infers emotion from text ("That's great!" → excited tone)

**Use case**: Audiobooks with emotional narration, voice assistants with empathy, interactive storytelling.

---

### Multimodal Integration

**Current state** (2025): TTS operates independently (text → audio)

**Future expectation** (2030): TTS integrated with vision, video, lip-sync
- **Avatar integration**: TTS generates audio + facial animations (lip-sync, expressions)
- **Video dubbing**: TTS replaces audio track + lip movements match new speech
- **AR/VR**: 3D avatars speak with TTS voices, synchronized with virtual environment

**Example**: Video game character speaks player-generated dialogue (text input → TTS audio + lip-sync animation).

---

**Document status**: Generic research (no platform recommendations)
**For platform comparisons**: See S1 provider profiles, S2 comprehensive analysis
**Last updated**: November 25, 2025
**Version**: 1.0
