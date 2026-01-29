# S2 Comprehensive Pass: Recommendation

## Executive Summary

After deep-dive analysis, the **recommended production stack** for CJK tone analysis is:

```
Pitch Detection:  Parselmouth (Praat-identical accuracy, zero dependencies)
Tone Classification: Pre-trained CNN (87-88% accuracy, ToneNet architecture)
Tone Sandhi:      Hybrid (Rule-based + CNN verification, 97%+ accuracy)
Annotation:       Parselmouth (integrated TextGrid support)
```

**Expected Performance:**
- Tone accuracy: 87-88%
- Sandhi accuracy: 97%+
- Processing: 2-3s per audio file
- Year 1 cost: ~$12,000 (dev + compute)

---

## Detailed Recommendations by Component

### 1. Pitch Detection: Parselmouth ⭐⭐⭐⭐⭐

**Winner: Parselmouth** for all production use cases.

**Evidence:**
- Identical to Praat: r=0.999 correlation with gold standard
- Zero dependencies: Precompiled wheels, no external Praat needed
- Complete API: Pitch, intensity, formants, spectrograms, TextGrids
- Fast: 2-3s per file (equivalent to librosa)
- Python 3.6-3.12 support

**Code Example:**
```python
import parselmouth

sound = parselmouth.Sound('audio.wav')
pitch = sound.to_pitch_ac(
    time_step=0.01,
    pitch_floor=75.0,    # Mandarin: 70-100 Hz
    pitch_ceiling=400.0  # Mandarin: 300-500 Hz
)

pitch_values = pitch.selected_array['frequency']
times = pitch.xs()
```

**When to use librosa instead:**
- ONLY if you need pYIN probabilistic approach for uncertainty quantification
- Be aware: Lower accuracy (r=0.730 for F0 mean)

**When to use CREPE instead:**
- Real-time requirements (<10ms latency) → Use PESTO variant
- GPU available and need absolute highest accuracy

---

### 2. Tone Classification: CNN (ToneNet) ⭐⭐⭐⭐

**Winner: CNN with ToneNet architecture** for production.

**Evidence:**
- 87-88% accuracy on Mandarin tones
- End-to-end learning from spectrograms (no manual feature engineering)
- Robust to speaker variation
- Moderate training cost (~$10K Year 1)

**Architecture:**
```
Input: Mel-spectrogram (128 bins × time)
Conv layers: 32→64→128 filters
Pooling: Max pooling 2×2
Dense: 128 units + Dropout(0.5)
Output: Softmax(5) [4 tones + neutral]
```

**When to use alternatives:**

**HMM/GMM (84-89% accuracy):**
- Quick prototype with limited data
- Interpretable statistical model needed
- Lower cost (~$1,000 Year 1)

**RNN/LSTM (88-90% accuracy):**
- Need implicit tone sandhi learning
- Sequential context important
- Higher training cost (~$15K Year 1)

**CNN-LSTM-Attention (90%+ accuracy):**
- State-of-the-art accuracy required
- Budget allows ($22K Year 1)
- Complex sandhi patterns

---

### 3. Tone Sandhi: Hybrid (Rules + CNN) ⭐⭐⭐⭐⭐

**Winner: Hybrid approach** - Rule-based detection + CNN verification.

**Evidence:**
- Rule-based alone: 88-97% accuracy, fast, low cost
- CNN alone: 97%+ accuracy, <1.9% false alarm, but expensive
- Hybrid: 97%+ accuracy + low false alarms + interpretable

**Implementation:**
```python
# Step 1: Rule-based detection
def detect_tone3_sandhi(syllables):
    """T3 + T3 → T2 + T3"""
    if syllables[i].tone == 3 and syllables[i+1].tone == 3:
        return True, "T3+T3"
    return False, None

# Step 2: CNN verification
if rule_triggered:
    f0_contour = extract_pitch(syllables[i:i+2])
    prediction = cnn_model.predict(f0_contour)
    if prediction > 0.9:  # High confidence
        apply_sandhi()
```

**Key Mandarin Rules:**
1. **不 (bù) tone change:** T4 → T2 before another T4
2. **一 (yī) tone change:** T1 → T2 before T4, T1 → T4 before T1/T2/T3
3. **Tone 3 sandhi:** T3 + T3 → T2 + T3

**When to use alternatives:**

**Rule-based only:**
- Prototype phase
- Budget constrained
- Rules well-documented

**CNN only:**
- Need to discover new patterns
- Training data abundant
- Budget allows

---

### 4. Annotation: Parselmouth TextGrids ⭐⭐⭐⭐⭐

**Winner: Parselmouth** for integrated pitch + annotation workflow.

**Evidence:**
- Unified API: Acoustic analysis + TextGrid manipulation
- No external process overhead (vs. praatio)
- Compatible with Praat ecosystem
- Active development (Jan 2026 release)

**Example:**
```python
# Extract pitch
pitch = sound.to_pitch_ac()

# Create TextGrid
tg = parselmouth.praat.call(sound, "To TextGrid", "syllables tones")

# Add annotations
tg.insert_point(1, 0.5, "T1")  # Tier 1, time 0.5s, label "T1"
```

**When to use praatio instead:**
- ONLY if you don't need acoustic analysis
- Already have external Praat workflow

---

## Production Deployment Stack

### Recommended: Standard Accuracy (87-88%)

```yaml
Components:
  - Pitch: Parselmouth
  - Tones: CNN (ToneNet)
  - Sandhi: Hybrid (Rules + CNN)

Infrastructure:
  - CPU: 4-8 cores
  - RAM: 16 GB
  - Storage: 100 GB (model + data)

Performance:
  - Tone accuracy: 87-88%
  - Sandhi accuracy: 97%+
  - Throughput: 1200-1800 files/hour
  - Latency: 2-3s per file

Cost (Year 1):
  - Development: $8,000 (4 weeks × $2K/week)
  - Training: $2,000 (GPU compute)
  - Infrastructure: $1,200 ($100/month × 12)
  - Maintenance: $1,000
  - Total: ~$12,000
```

### Alternative: High Accuracy (90%+)

Use CNN-LSTM-Attention for tones (increases cost to ~$22K Year 1).

### Alternative: Budget Constrained (<$5K)

Use Rule-based sandhi only, skip CNN verification (reduces accuracy to 88-97%).

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- Install Parselmouth: `pip install praat-parselmouth`
- Implement pitch extraction pipeline
- Test on sample Mandarin audio
- Parameter tuning for speaker demographics

### Phase 2: Tone Classification (Weeks 3-4)
- Collect/acquire training data (THCHS-30, AISHELL-1)
- Implement CNN architecture (ToneNet)
- Train model (or use pre-trained if available)
- Evaluate on test set (target: 85%+ accuracy)

### Phase 3: Tone Sandhi (Weeks 5-6)
- Implement rule-based detector (不, 一, T3+T3)
- Train CNN verifier on sandhi examples
- Integrate hybrid pipeline
- Test precision/recall (target: 95%+ precision)

### Phase 4: Production (Weeks 7-8)
- Optimize for throughput (batch processing)
- Add error handling and logging
- Deploy to production environment
- Monitor accuracy on live data

---

## Trade-offs Matrix

| Factor | Parselmouth | librosa | CREPE | PESTO |
|--------|-------------|---------|-------|-------|
| Accuracy | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Speed | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Dependencies | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Cost | Free | Free | Free | Free |
| GPU Required | No | No | Yes | Optional |

| Factor | HMM/GMM | CNN | RNN/LSTM | CNN-LSTM-Attn |
|--------|---------|-----|----------|---------------|
| Accuracy | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Training Cost | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Interpretability | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ |
| Sandhi Aware | ⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## Decision Tree

```
START: What's your primary goal?
│
├─ Pronunciation practice app
│  └─ Need real-time feedback?
│     ├─ YES → Parselmouth + PESTO + Rules
│     └─ NO  → Parselmouth + CNN + Hybrid [RECOMMENDED]
│
├─ Speech recognition tuning
│  └─ Have GPU available?
│     ├─ YES → CREPE + CNN-LSTM-Attn
│     └─ NO  → Parselmouth + CNN [RECOMMENDED]
│
├─ Linguistic research
│  └─ Need Praat compatibility?
│     ├─ YES → Parselmouth (100% compatible)
│     └─ NO  → Parselmouth [STILL RECOMMENDED]
│
└─ Batch processing large corpus
   └─ Budget constraints?
      ├─ YES → Parselmouth + HMM + Rules
      └─ NO  → Parselmouth + CNN + Hybrid [RECOMMENDED]
```

---

## Next Steps for S3

Investigate specific use cases:
1. **Pronunciation practice**: Real-time feedback, learner errors, progress tracking
2. **Speech recognition**: ASR F0 features, multi-speaker adaptation
3. **Linguistic research**: Corpus annotation, tone variation studies
4. **Language learning apps**: Gamification, UX considerations
5. **Clinical applications**: Tone perception deficits, rehabilitation

Each use case will inform different trade-offs in the deployment stack.

---

## References

See individual S2 documents for full citation lists:
- 01-parselmouth-deep-dive.md
- 02-librosa-advanced.md
- 04-tone-classification-algorithms.md
- 05-tone-sandhi-detection.md
- 06-comparative-analysis.md
