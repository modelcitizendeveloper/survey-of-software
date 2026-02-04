# Custom Whisper + Phonetic Analysis (DIY)

**Category**: Open-Source Speech Recognition + Custom Scoring
**Tier**: Self-hosted, requires ML expertise
**Status**: Research/experimental, production requires significant development
**Last Updated**: November 2025

---

## Overview

Custom pronunciation assessment using **OpenAI Whisper** (speech recognition) + **phonetic analysis libraries** (e.g., epitran, panphon, allosaurus). **DIY solution** requiring ML expertise, model fine-tuning, and custom scoring algorithms.

## Key Components

### 1. Whisper (Speech Recognition)
- **Purpose**: Transcribe spoken audio to text
- **Models**: tiny, base, small, medium, large (increasing accuracy)
- **Languages**: 99 languages supported
- **License**: MIT (open source, free)
- **Limitations**: No native phoneme output, no pronunciation scoring

### 2. Phonetic Analysis Libraries

**epitran** (Phonetic transcription):
- Converts text to IPA (International Phonetic Alphabet)
- Supports 100+ languages
- Example: "hello" → /həˈloʊ/

**panphon** (Phonetic features):
- Analyzes phonetic features (voicing, place, manner)
- Useful for comparing phonemes

**allosaurus** (Universal phoneme recognizer):
- Recognizes phonemes directly from audio
- Trained on 200+ languages

### 3. Custom Scoring Algorithms

**Goodness of Pronunciation (GOP)**:
- Measures how well spoken phonemes match reference
- Requires forced alignment (audio ↔ phoneme timing)
- Formula: GOP = log P(phoneme | audio)

**Phoneme Error Rate (PER)**:
- Compares recognized phonemes to reference
- Similar to Word Error Rate (WER) but phoneme-level

**Levenshtein Distance**:
- Edit distance between spoken and reference phonemes
- Counts insertions, deletions, substitutions

## Architecture (DIY Pronunciation Assessment)

```
[Student Audio]
      ↓
[Whisper ASR] → Transcribed text
      ↓
[Reference text comparison] → Word-level accuracy
      ↓
[Phonetic transcription (epitran)] → Reference phonemes
      ↓
[Phoneme recognizer (allosaurus)] → Spoken phonemes
      ↓
[GOP / PER scoring] → Pronunciation score
      ↓
[Custom scoring logic] → Final assessment
```

## Technical Capabilities

### Whisper Models

| Model | Parameters | Speed | Accuracy | Use Case |
|-------|-----------|-------|----------|----------|
| tiny | 39M | Very fast | Good | Real-time applications |
| base | 74M | Fast | Better | Low-latency |
| small | 244M | Moderate | Good | Balanced |
| medium | 769M | Slow | Very good | Quality priority |
| large | 1550M | Very slow | Best | Maximum accuracy |

**Recommendation**: **medium** for pronunciation assessment (balance quality + speed)

### Phoneme Recognition

**allosaurus** (Universal phoneme recognizer):
- **Languages**: 200+ (universal model)
- **Output**: Phoneme sequence with timestamps
- **Accuracy**: Good for cross-language phoneme detection
- **Limitation**: Not as accurate as language-specific models

### GOP (Goodness of Pronunciation) Calculation

**Method**:
1. Forced alignment: Align audio to reference phonemes (timing)
2. Extract acoustic features: MFCCs, spectrograms
3. Calculate log-likelihood: P(phoneme | audio features)
4. Normalize: GOP score 0-100

**Challenges**:
- Requires acoustic model (e.g., Kaldi, Montreal Forced Aligner)
- Complex pipeline (5+ steps)
- No off-the-shelf solution

## Pricing

**$0 for software** (all open-source):
- Whisper: MIT license (free)
- epitran, panphon, allosaurus: Open-source (free)

**Infrastructure costs**:
- **CPU inference** (Whisper medium): $20-50/month (VPS)
- **GPU inference** (Whisper large): $200-500/month (GPU VPS)
- **Self-hosted**: $0 ongoing (own hardware)

**Development costs**:
- **Setup**: 40-80 hours @ $100/hr = $4,000-8,000 (one-time)
- **Fine-tuning**: 20-40 hours @ $100/hr = $2,000-4,000 (per language)
- **Maintenance**: 10-20 hours/month @ $100/hr = $1,000-2,000/month

**Break-even analysis** (vs Azure $1/hour):
- **Azure cost**: 1,000 hours/month × $1 = $1,000/month
- **DIY cost**: $500 infrastructure + $1,500 maintenance = $2,000/month
- **Break-even**: Need >2,000 hours/month (33,000 1-minute assessments)

**Conclusion**: DIY only cost-effective at **>30,000 assessments/month**

## Language Learning Use Case

### Strengths
- ✅ **$0 per-assessment cost**: No usage fees (infrastructure only)
- ✅ **99 languages**: Whisper supports 99 languages
- ✅ **Full control**: Customize scoring algorithms, thresholds
- ✅ **Privacy**: Data never leaves your infrastructure
- ✅ **No vendor lock-in**: Open-source, portable

### Weaknesses
- ❌ **High development cost**: $4K-8K setup + $1K-2K/month maintenance
- ❌ **ML expertise required**: Need ML engineers, not just developers
- ❌ **No pronunciation focus**: Whisper designed for transcription, not pronunciation
- ❌ **Complex pipeline**: 5+ components (ASR, phoneme recognizer, forced aligner, GOP calculator)
- ❌ **Lower accuracy**: DIY GOP scoring less accurate than commercial (Speechace, Azure, ELSA)
- ❌ **No phoneme output**: Whisper doesn't output phonemes natively

### Ideal For
- **Massive scale**: >50,000 assessments/month (cost advantage)
- **Privacy-critical**: Healthcare, government (data sovereignty)
- **Research projects**: Academic research, algorithm development
- **ML teams**: Already have ML engineers on staff
- **Custom requirements**: Need highly specific scoring algorithms

### Not Ideal For
- **Small-medium apps**: <10,000 assessments/month (commercial APIs cheaper)
- **No ML expertise**: Requires ML engineers (not just developers)
- **Fast time-to-market**: 3-6 months vs 1-2 weeks (commercial APIs)
- **English-only**: ELSA better for English depth
- **Multi-language**: Azure better for 32+ languages out-of-box

## Competitive Position

**vs. Speechace**:
- Whisper: $0/assessment (after development), 99 languages, requires ML team
- Speechace: $0.01-0.03/assessment, 15+ languages, no ML required
- **Winner**: Speechace for <30K assessments/month, Whisper for massive scale

**vs. Azure**:
- Whisper: $0/assessment (after development), DIY maintenance, lower accuracy
- Azure: $1/hour ($0.017/min), 32+ languages, enterprise support
- **Winner**: Azure for <2,000 hours/month, Whisper for massive scale + privacy

**vs. ELSA**:
- Whisper: $0/assessment, English + 98 languages, requires development
- ELSA: $0.02-0.05/assessment, English-only, L1-specific feedback
- **Winner**: ELSA for English accuracy, Whisper for multi-language at scale

## Production Readiness

| Factor | Rating | Notes |
|--------|--------|-------|
| Assessment Quality | ⭐⭐⭐ | Lower accuracy than commercial (no native pronunciation focus) |
| Language Support | ⭐⭐⭐⭐⭐ | 99 languages (Whisper) |
| Cost (at scale) | ⭐⭐⭐⭐⭐ | $0/assessment (infrastructure only) |
| Development Complexity | ⭐ | Very high (40-80 hours setup) |
| ML Expertise Required | ⭐ | Requires ML engineers |
| Time-to-Market | ⭐⭐ | 3-6 months vs 1-2 weeks (APIs) |
| Maintenance | ⭐⭐ | Ongoing ML engineering required |

## Implementation Steps

### Phase 1: Basic Setup (2-4 weeks)
1. **Install Whisper**: `pip install openai-whisper`
2. **Transcribe audio**: Whisper ASR → text
3. **Compare transcription**: Levenshtein distance vs reference
4. **Word-level accuracy**: % words correct

**Output**: Basic transcription accuracy (not pronunciation-specific)

### Phase 2: Phoneme Recognition (4-8 weeks)
1. **Install allosaurus**: Phoneme recognizer
2. **Extract phonemes**: Audio → phoneme sequence
3. **Reference phonemes**: epitran (text → IPA)
4. **Phoneme alignment**: Align spoken vs reference phonemes
5. **Phoneme Error Rate (PER)**: % phonemes correct

**Output**: Phoneme-level accuracy (better than word-level)

### Phase 3: GOP Scoring (8-12 weeks)
1. **Forced alignment**: Montreal Forced Aligner or Kaldi
2. **Acoustic features**: Extract MFCCs, spectrograms
3. **GOP calculation**: log P(phoneme | audio)
4. **Normalize scores**: 0-100 scale
5. **Tuning**: Calibrate thresholds

**Output**: Pronunciation scores comparable to commercial APIs

### Phase 4: Fine-Tuning (ongoing)
1. **Collect labeled data**: 1,000+ pronunciation samples
2. **Fine-tune Whisper**: Improve ASR accuracy for L2 speakers
3. **Fine-tune allosaurus**: Language-specific phoneme models
4. **Optimize GOP**: Adjust scoring algorithms

**Output**: Improved accuracy (closer to commercial quality)

## Academic Research (2025)

**Recent findings**:
- **Smaller Whisper models better for L2 pronunciation** (2023 study)
  - tiny/base/small models pinpoint L2 mispronunciations better than large
  - Large model "over-corrects" non-native speech
- **Whisper + GOP scores effective** (2025 study)
  - Medium Whisper + GOP scoring competitive with commercial tools
  - Requires forced alignment (Montreal Forced Aligner)
- **Fine-tuning on L2 speech improves accuracy** (2023 research)
  - Fine-tuned Whisper on non-native speech → 15% accuracy improvement
  - Requires 10-20 hours of labeled L2 audio per language

## Cost Comparison (30K Assessments/Month)

| Solution | Monthly Cost | Notes |
|----------|-------------|-------|
| **Custom Whisper** | $500 (infra) + $1,500 (maint) = **$2,000** | Break-even at 30K assessments |
| **Speechace** | 30K × $0.02 = **$600** | Per-assessment pricing |
| **Azure** | 500 hours × $1 = **$500** | Hourly pricing (1 min/assessment) |
| **ELSA** | 30K × $0.03 = **$900** | English-only |

**Conclusion at 30K/month**:
1. **Azure cheapest**: $500/month (if short assessments)
2. **Speechace**: $600/month (good balance)
3. **ELSA**: $900/month (premium English)
4. **Custom Whisper**: $2,000/month (most expensive at this scale)

**Break-even**: Custom Whisper becomes cheaper at **>50K-100K assessments/month**

## When to Choose Custom Whisper

Choose Custom Whisper when:
1. **Massive scale**: >100,000 assessments/month (cost advantage)
2. **Privacy-critical**: Healthcare, government (data sovereignty requirements)
3. **ML team available**: Have ML engineers on staff
4. **Custom algorithms**: Need highly specific scoring logic
5. **Research project**: Academic research, algorithm development
6. **Long-term investment**: Willing to invest 6-12 months upfront

Don't choose Custom Whisper when:
1. **<30K assessments/month**: Commercial APIs cheaper
2. **No ML expertise**: Requires ML engineers (not just developers)
3. **Fast time-to-market**: Need production in <3 months
4. **Best accuracy**: ELSA/Speechace more accurate for English
5. **No DevOps capacity**: Self-hosting requires infrastructure management

## Technical Stack Example

```python
# 1. Whisper ASR
import whisper
model = whisper.load_model("medium")
result = model.transcribe("student_audio.wav")
transcription = result['text']

# 2. Phoneme reference (epitran)
import epitran
epi = epitran.Epitran('eng-Latn')
reference_phonemes = epi.transliterate("hello")  # → /həˈloʊ/

# 3. Phoneme recognition (allosaurus)
from allosaurus.app import read_recognizer
recognizer = read_recognizer()
spoken_phonemes = recognizer.recognize("student_audio.wav")

# 4. Phoneme alignment + GOP scoring
from montreal_forced_aligner import align
alignment = align(audio="student_audio.wav", text=transcription)
gop_scores = calculate_gop(alignment, spoken_phonemes, reference_phonemes)

# 5. Final scoring
pronunciation_score = normalize_gop_scores(gop_scores)  # 0-100
print(f"Pronunciation Score: {pronunciation_score}")
```

**Total complexity**: 5 libraries + custom GOP calculation + fine-tuning

## References

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Whisper Pronunciation Discussion](https://github.com/openai/whisper/discussions/1861)
- [Allosaurus (Universal Phoneme Recognizer)](https://github.com/xinjli/allosaurus)
- [epitran (Phonetic Transcription)](https://github.com/dmort27/epitran)
- [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- [L2 Speech Analysis Paper (2023)](https://aclanthology.org/2023.icnlsp-1.30.pdf)
- [Pronunciation Scorer Paper (2025)](https://onlinelibrary.wiley.com/doi/full/10.1111/lang.70000)
