# Use Case 01: Pronunciation Practice Apps

## User Archetype

**Who:** Mandarin/Cantonese language learners (beginner to intermediate)
**Platform:** Mobile app (iOS/Android) or web app
**Context:** Self-directed study, 10-30 minutes per session
**Technical sophistication:** Non-technical end users

## Core Requirements

### Functional
1. **Real-time feedback** - User says syllable, app shows tone accuracy within 200ms
2. **Visual representation** - Display F0 contour overlaid with target tone shape
3. **Progress tracking** - Show improvement over time per tone category
4. **Error diagnosis** - Identify specific mistakes (e.g., "flat instead of rising")
5. **Practice mode** - Focused drills on problem tones (especially Tone 3)

### Non-Functional
- **Latency:** <200ms perception to feedback (feels instant)
- **Accuracy:** 85%+ tone classification (acceptable for learning)
- **Robustness:** Works in normal room noise (not studio quality)
- **Mobile-friendly:** Runs on mid-range smartphones (2-3 year old devices)
- **Battery:** <5% drain per 15-minute session

## Technical Challenges

### Challenge 1: Latency Budget
```
Total budget: 200ms
├─ Audio capture: 50ms (microphone buffering)
├─ Pitch detection: 50ms (must be real-time capable)
├─ Tone classification: 50ms (lightweight model)
├─ UI rendering: 25ms (display update)
└─ Buffer/slack: 25ms
```

**Constraint:** Rules out most deep learning (CNN/LSTM too slow on mobile CPU)

### Challenge 2: Speaker Variation
- Learners have non-native accents
- F0 range varies widely (children, adults, male, female)
- Need speaker normalization WITHOUT enrollment phase

### Challenge 3: Partial Utterances
- Learners often produce incomplete/hesitant syllables
- Need to detect "not a valid tone" vs. "wrong tone"
- Avoid false positives on coughs, laughter, ambient speech

### Challenge 4: Educational Accuracy
- Over-correction discourages learners
- Under-correction reinforces errors
- Need "good enough" threshold (not perfect native-like)

## Recommended Stack: Mobile-Optimized

### Architecture
```
Audio Input (48kHz)
↓
PESTO (pitch detection, <10ms)
↓
Z-score normalization (speaker-adaptive)
↓
Lightweight CNN or Rule-based classifier (<50ms)
↓
Visual feedback (F0 contour + tone label)
```

### Component Choices

**Pitch Detection: PESTO**
- Rationale: <10ms latency, 0.1 MB model, runs on mobile CPU
- Trade-off: Slightly lower accuracy than CREPE (acceptable for learning)
- Alternative: If GPU available on device, use CREPE-Tiny

**Tone Classification: Lightweight CNN or Rule-Based**

*Option A: Rule-Based (Recommended for MVP)*
```python
def classify_tone_simple(f0_contour):
    """
    5-point time-normalized F0 contour
    Z-score normalized per speaker
    """
    if f0_contour is None or len(f0_contour) < 3:
        return None  # Invalid/incomplete

    # Normalize to 5 time points
    f0_norm = interpolate(f0_contour, 5)

    # Calculate slope and shape
    start, mid, end = f0_norm[0], f0_norm[2], f0_norm[4]
    slope_start = mid - start
    slope_end = end - mid

    # Simple decision tree
    if abs(start - end) < 0.5:  # Flat
        if start > 0:
            return "Tone1"  # High level
        else:
            return "Tone3_neutral"  # Low level (could be T3 or neutral)
    elif slope_end > 0.8:
        return "Tone2"  # Rising
    elif slope_end < -0.8:
        return "Tone4"  # Falling
    elif slope_start < 0 and slope_end > 0:
        return "Tone3"  # Dipping
    else:
        return "uncertain"
```

*Option B: TensorFlow Lite CNN*
- Input: Mel-spectrogram (32 bins × 32 time steps)
- Model: 3 conv layers → dense → softmax
- Size: 2-5 MB quantized
- Latency: 30-50ms on mobile CPU

**Recommendation:** Start with rule-based, upgrade to Lite CNN if accuracy insufficient.

**Tone Sandhi: SKIP for MVP**
- Rationale: Pronunciation practice focuses on isolated syllables
- Learners should master individual tones before connected speech
- Add in advanced mode later

### Implementation

**Tech Stack:**
- **iOS:** Swift + AVAudioEngine + CoreML (for CNN if needed)
- **Android:** Kotlin + AudioRecord + TensorFlow Lite
- **Web:** WebAssembly (Parselmouth compiled) + Web Audio API

**Data Requirements:**
- Pre-trained model on THCHS-30 or AISHELL-1
- Fine-tune on learner data (if available)
- Continuous learning: Collect feedback ("Was this correct?")

## MVP Definition

### Must-Have (Week 1-4)
1. Record single syllable
2. PESTO pitch detection
3. Rule-based tone classification
4. Visual F0 contour display
5. "Correct/Try Again" binary feedback

### Should-Have (Week 5-8)
6. Z-score speaker normalization (adaptive over session)
7. Progress tracking per tone
8. Specific error messages ("Your tone started high but didn't rise")
9. Comparison to native speaker reference

### Nice-to-Have (Week 9-12)
10. Lightweight CNN (if rule-based <85% accuracy)
11. Minimal pairs practice (e.g., mā vs má vs mǎ vs mà)
12. Game-ification (streak tracking, badges)
13. Offline mode (pre-downloaded models)

## Success Metrics

### User-Facing
- **Tone accuracy improvement:** 20% increase after 10 hours of practice
- **User retention:** 40%+ users complete 5+ sessions
- **Subjective quality:** "Helpful" rating from 70%+ users

### Technical
- **Latency:** 95th percentile <200ms end-to-end
- **Classification accuracy:** 85%+ on learner speech (manually verified subset)
- **False positive rate:** <10% (saying "Tone 1" incorrectly marked as correct)

## Cost Estimate

### Development (Months 1-3)
- Mobile app development: $20,000 (iOS + Android)
- PESTO integration: $5,000
- Rule-based classifier: $3,000
- UI/UX design: $8,000
- Testing with learners: $4,000
- **Subtotal:** $40,000

### Training/Data (if using CNN)
- Data acquisition: $5,000 (license THCHS-30)
- Model training: $2,000 (GPU compute)
- Fine-tuning on learners: $3,000
- **Subtotal:** $10,000

### Ongoing (Year 1)
- Cloud infrastructure: $3,000 ($250/month × 12)
- Maintenance: $5,000
- Analytics/monitoring: $2,000
- **Subtotal:** $10,000

**Total Year 1:** $50,000-$60,000 (depending on rule-based vs. CNN)

## Critical Risks

### Risk 1: Latency on Low-End Devices
**Probability:** High
**Impact:** High (unusable app)
**Mitigation:**
- Profile on 3-year-old Android devices early
- Have fallback to cloud processing (adds latency but avoids crashes)
- Progressive enhancement: Advanced features only on high-end devices

### Risk 2: Accuracy on Non-Native Speech
**Probability:** Medium
**Impact:** High (learners lose trust)
**Mitigation:**
- Collect learner data in beta testing
- Fine-tune models on non-native speakers
- Allow "I disagree" feedback to improve models

### Risk 3: Competing with Free Alternatives
**Probability:** High
**Impact:** Medium (market differentiation)
**Mitigation:**
- Better UX (prettier visualizations, clearer feedback)
- Offline mode (use without internet)
- Progress tracking (stickiness)

## Alternatives Considered

### Alternative 1: Server-Side Processing
**Approach:** Record audio → upload → cloud processing → download result

**Pros:**
- Can use heavy models (CREPE, large CNN)
- No mobile optimization needed
- Easy updates (just deploy new model)

**Cons:**
- Latency >500ms (network RTT + processing)
- Requires internet connection
- Costs scale with users ($0.10-$0.50 per 1000 requests)

**Verdict:** Reject due to latency. Consider hybrid (on-device MVP, cloud for advanced).

### Alternative 2: Praat/Parselmouth on Mobile
**Approach:** Compile Parselmouth for iOS/Android

**Pros:**
- High accuracy (Praat-level)
- Mature, well-tested algorithms

**Cons:**
- Latency ~2-3s per file (too slow)
- Large binary size (~50 MB)
- C++ compilation for mobile is complex

**Verdict:** Reject due to latency. Use for teacher/admin dashboard instead.

### Alternative 3: Rule-Based Only (No ML)
**Approach:** Simple F0 contour analysis, thresholds

**Pros:**
- Fastest (10-20ms classification)
- Smallest model size (kilobytes)
- Easiest to debug

**Cons:**
- Lower accuracy (~75-80%)
- Brittle to edge cases
- Requires manual threshold tuning

**Verdict:** Accept for MVP, plan upgrade to Lite CNN in Month 4.

## Next Steps After MVP

1. **Collect usage data** - Which tones are hardest? Where do false positives occur?
2. **Fine-tune models** - Retrain on learner speech (with user consent)
3. **Add connected speech** - Two-syllable practice with tone sandhi
4. **Expand to Cantonese** - 6 tones, different F0 ranges
5. **Teacher dashboard** - Progress reports for classrooms

## References

- [PESTO for real-time pitch](https://github.com/SonyCSLParis/pesto) (2024)
- [TensorFlow Lite for mobile ML](https://www.tensorflow.org/lite)
- [Pronunciation feedback systems (review)](https://doi.org/10.1016/j.specom.2018.04.002)
- THCHS-30 dataset for Mandarin ASR/tone analysis
