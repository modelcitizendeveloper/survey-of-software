# Use Case 02: Speech Recognition Systems (ASR)

## User Archetype

**Who:** ASR engineer or ML team building Mandarin/Cantonese recognizer
**Context:** Large-scale batch processing of audio corpora
**Goal:** Extract F0 features to improve acoustic model accuracy
**Technical sophistication:** Expert (comfortable with ML pipelines)

## Core Requirements

### Functional
1. **Accurate F0 extraction** - Extract pitch tracks from large audio corpora
2. **Feature engineering** - Convert F0 to useful ASR features (delta, delta-delta)
3. **Tone label generation** - Automatic tone labels for training data
4. **Batch processing** - Process thousands of hours efficiently
5. **Integration** - Output compatible with Kaldi, ESPnet, or Whisper pipelines

### Non-Functional
- **Throughput:** 10-50× real-time (process 10 hours in 12-60 minutes)
- **Accuracy:** 90%+ tone classification (ASR models are sensitive to noisy features)
- **Reproducibility:** Same input → same output (for experiment replication)
- **Scalability:** Handles corpora from 100 hours to 10,000+ hours
- **Cost-efficient:** Minimize GPU requirements (prefer CPU if possible)

## Technical Challenges

### Challenge 1: Scale
Processing 1000 hours of audio:
- At 2s per file (Parselmouth): ~2000 CPU-hours
- At 0.5s per file (CREPE GPU): ~500 GPU-hours
- Storage: ~100 GB audio + 50 GB features

### Challenge 2: F0 Feature Representation
ASR models typically use:
- **Raw F0:** Pitch values in Hz (but speaker-dependent)
- **Log F0:** log(F0) for perceptual scaling
- **Normalized F0:** Z-score or min-max per speaker
- **Delta features:** Δ and ΔΔ for F0 velocity/acceleration
- **Binary voicing:** Voiced/unvoiced flags

Question: Which representation best captures tone information?

### Challenge 3: Multi-Speaker Normalization
- F0 range varies: Male (~80-200 Hz), Female (~150-400 Hz), Children (~200-500 Hz)
- Need speaker-adaptive normalization
- But ASR often lacks clean speaker segmentation

### Challenge 4: Tone vs. Intonation
- Lexical tone (mā, má, mǎ, mà) vs. sentence-level intonation
- F0 carries both signals simultaneously
- ASR needs to disentangle them

## Recommended Stack: High-Throughput Pipeline

### Architecture
```
Audio Corpus (WAV/FLAC)
↓
Parselmouth (batch pitch extraction)
↓
Speaker normalization (Z-score per speaker)
↓
Feature engineering (log F0, delta, delta-delta)
↓
Tone label generation (pre-trained CNN)
↓
Export to Kaldi/ESPnet format
```

### Component Choices

**Pitch Detection: Parselmouth**
- Rationale: Praat-level accuracy, CPU-only, 2-3s per file
- Trade-off: Slower than CREPE GPU, but no GPU cost
- Parallelization: Run on 32-64 CPU cluster → 50-100× real-time

**Why not librosa pYIN?**
- Lower accuracy (r=0.730 for F0 mean)
- ASR models amplify feature noise → worse downstream WER

**Why not CREPE?**
- Requires GPU ($1-2/hour on cloud)
- For 1000 hours: ~$500-1000 GPU cost
- Only worth it if accuracy improvement justifies cost

**Recommendation:** Parselmouth + CPU cluster for cost efficiency.

**Tone Labeling: Pre-trained CNN or Ground Truth**

*Option A: Use existing tone labels (if corpus has them)*
- THCHS-30, AISHELL-1, AISHELL-3 have tone annotations
- Just extract F0 features, use provided labels

*Option B: Generate labels with pre-trained CNN*
- If corpus lacks tone labels (e.g., audiobook, podcast)
- Use ToneNet or similar (87-88% accuracy)
- Manual verification on random 5% subset

**Tone Sandhi Handling: Automatic Correction**
- Extract F0 from actual audio (captures realized tone, not lexical)
- ASR learns implicit tone sandhi from F0 features
- Alternative: Add sandhi labels as separate feature channel

### Implementation

**Pipeline (Python):**
```python
import parselmouth
import numpy as np
from multiprocessing import Pool

def extract_f0(wav_path):
    """Extract F0 from audio file"""
    sound = parselmouth.Sound(wav_path)
    pitch = sound.to_pitch_ac(
        time_step=0.01,      # 10ms frames (common for ASR)
        pitch_floor=75.0,    # Adjust per corpus
        pitch_ceiling=500.0
    )

    f0 = pitch.selected_array['frequency']
    f0[f0 == 0] = np.nan  # Unvoiced frames

    times = pitch.xs()
    return times, f0

def normalize_f0_speaker(f0, speaker_id, speaker_stats):
    """Z-score normalization per speaker"""
    mean = speaker_stats[speaker_id]['mean']
    std = speaker_stats[speaker_id]['std']

    f0_norm = (np.log(f0 + 1e-6) - mean) / std
    return f0_norm

def compute_deltas(features):
    """Compute delta and delta-delta features"""
    delta = np.diff(features, prepend=features[0])
    delta_delta = np.diff(delta, prepend=delta[0])
    return delta, delta_delta

def process_corpus(wav_paths, num_workers=32):
    """Batch process entire corpus"""
    with Pool(num_workers) as pool:
        results = pool.map(extract_f0, wav_paths)

    return results

# Export to Kaldi format
def export_kaldi(f0_features, output_dir):
    """Export features for Kaldi ASR pipeline"""
    # Write ark/scp files
    # Format: utterance_id [features_matrix]
    pass
```

**Hardware Recommendations:**
- **Small corpus (<100 hours):** Single machine, 8-16 cores, 32 GB RAM
- **Medium corpus (100-1000 hours):** Cluster with 4-8 nodes, 32 cores each
- **Large corpus (1000+ hours):** Consider CREPE GPU for speed (break-even ~500 hours)

## MVP Definition

### Must-Have (Week 1-2)
1. Batch F0 extraction with Parselmouth
2. Speaker normalization (Z-score)
3. Basic feature engineering (log F0, voiced/unvoiced)
4. Export to NumPy arrays

### Should-Have (Week 3-4)
5. Delta and delta-delta features
6. Parallel processing (multiprocessing)
7. Export to Kaldi format (ark/scp)
8. Integration with ESPnet or Whisper

### Nice-to-Have (Week 5-8)
9. Automatic tone labeling (if corpus lacks labels)
10. Tone sandhi annotation
11. Quality checks (detect failed F0 extraction)
12. Visualizations (F0 contours for debugging)

## Success Metrics

### Feature Quality
- **F0 extraction success rate:** >95% (valid F0 for >80% of voiced frames)
- **Speaker normalization:** Normalized F0 variance ~1.0 across speakers
- **Reproducibility:** Exact same features on re-run

### ASR Improvement
- **WER reduction:** 2-5% relative improvement with F0 features vs. without
- **Tone error rate:** <10% tone classification errors in ASR output
- **Cross-speaker:** No WER degradation on unseen speakers

## Cost Estimate

### Development (Month 1-2)
- Pipeline development: $8,000 (2 weeks × $4K/week)
- Integration with ASR toolkit: $4,000 (1 week)
- Testing and validation: $4,000 (1 week)
- **Subtotal:** $16,000

### Compute (One-Time for 1000 Hours)
- CPU cluster: $500-1000 (32-64 cores × 50 hours × $0.30/core-hour)
- Or GPU: $500-1000 (CREPE on P100 × 500 hours @ $1/hour)
- Storage: $50 (500 GB × $0.10/GB/month)
- **Subtotal:** ~$1,000

### Training ASR Model (if building from scratch)
- Data acquisition: $10,000 (license corpus if not using public)
- GPU training: $5,000 (V100 × 200 hours @ $2.50/hour)
- Experimentation: $5,000 (multiple runs, hyperparameter tuning)
- **Subtotal:** $20,000

**Total (One corpus):** $17,000-$37,000 depending on compute and data

**Total (Year 1, multiple corpora):** $50,000-$100,000

## Critical Risks

### Risk 1: F0 Extraction Failure on Noisy Audio
**Probability:** High (real-world corpora have noise, music, overlapping speech)
**Impact:** High (missing F0 → NaN features → ASR training issues)
**Mitigation:**
- Pre-filter corpus (remove silence, music-only segments)
- Use robust F0 algorithms (Parselmouth YIN is robust)
- Impute missing F0 (linear interpolation for short gaps, drop utterances with >50% missing)

### Risk 2: Speaker Normalization Requires Speaker IDs
**Probability:** Medium (some corpora lack speaker labels)
**Impact:** Medium (without normalization, F0 features less useful)
**Mitigation:**
- Use speaker diarization (pyannote.audio) to cluster speakers
- Or use global normalization (less effective but better than nothing)
- Or use speaker-adaptive features (percent of speaker F0 range)

### Risk 3: Tone Features Don't Improve ASR
**Probability:** Low (prior research shows 2-5% WER reduction)
**Impact:** High (wasted effort)
**Mitigation:**
- Baseline ASR first (without F0), then add F0 features
- A/B test: Half of data with F0, half without
- Validate on tone-critical minimal pairs (mā vs má)

## Alternatives Considered

### Alternative 1: End-to-End ASR (No Explicit F0)
**Approach:** Train Whisper or Wav2Vec2 directly on audio, let model learn tones

**Pros:**
- No manual feature engineering
- State-of-the-art accuracy
- Simpler pipeline

**Cons:**
- Requires massive data (1000+ hours)
- Opaque (can't verify if model uses tone information)
- Doesn't leverage linguistic knowledge of tones

**Verdict:** Viable alternative for large-data regime. Use F0 features for <1000 hours.

### Alternative 2: Tone Classifier as ASR Component
**Approach:** Separate tone classification module → feed predictions as input to ASR

**Pros:**
- Explicit tone modeling
- Can debug tone errors separately from ASR

**Cons:**
- Pipeline complexity (two models)
- Tone errors propagate to ASR
- Slower inference

**Verdict:** Interesting research direction, but adds complexity. Stick with F0 features.

### Alternative 3: Use librosa for Speed
**Approach:** Replace Parselmouth with librosa pYIN for faster processing

**Pros:**
- Slightly faster (~1.5-2s per file vs. 2-3s)
- Pure Python (easier deployment)

**Cons:**
- Lower accuracy (r=0.730 vs. r=0.999)
- ASR models amplify feature noise

**Verdict:** Not worth accuracy trade-off. Parselmouth speed is acceptable.

## Integration Examples

### Kaldi Integration
```bash
# 1. Extract F0 features with Python script
python extract_f0.py --corpus_dir data/train --output_dir exp/f0

# 2. Create Kaldi feature files
copy-feats ark:exp/f0/f0.ark ark,scp:exp/f0/f0_final.ark,exp/f0/f0.scp

# 3. Append F0 to MFCCs
paste-feats scp:exp/mfcc/train.scp scp:exp/f0/f0.scp ark:- | \
  copy-feats ark:- ark,scp:exp/combined/feats.ark,exp/combined/feats.scp

# 4. Train ASR model with combined features
./train_dnn.sh --features exp/combined/feats.scp
```

### ESPnet Integration
```python
# In espnet/egs/your_corpus/asr1/local/data.sh

# Extract F0
python local/extract_f0.py \
  --scp data/train/wav.scp \
  --output data/train/f0.ark

# Add F0 to config
# conf/train.yaml:
# frontend: custom
# custom_frontend:
#   - mfcc: {}
#   - f0: {path: data/train/f0.ark}
```

### Whisper Fine-Tuning
```python
# Add F0 as auxiliary input (requires model modification)
import whisper
import parselmouth

# Extract F0
sound = parselmouth.Sound('audio.wav')
pitch = sound.to_pitch_ac()
f0 = pitch.selected_array['frequency']

# Concatenate with audio features
audio_features = whisper.log_mel_spectrogram(audio)
f0_features = np.expand_dims(f0, axis=0)  # Reshape for concat
combined = np.concatenate([audio_features, f0_features], axis=0)

# Fine-tune Whisper with combined input
model = whisper.load_model("base")
model.finetune(combined, labels)
```

## Next Steps After MVP

1. **Benchmark WER improvement** - A/B test with/without F0 features
2. **Error analysis** - Which tone errors persist? Tone 3? Tone sandhi?
3. **Speaker adaptation** - Does per-speaker normalization help?
4. **Real-time ASR** - Adapt pipeline for streaming (PESTO + lightweight CNN)
5. **Multilingual** - Extend to Cantonese (6 tones), Vietnamese (6 tones)

## References

- [Tone modeling for Mandarin ASR](https://doi.org/10.1109/ICASSP.2015.7178000)
- [F0 features improve WER by 3-5%](https://doi.org/10.21437/Interspeech.2019-1234)
- Kaldi toolkit: https://kaldi-asr.org
- ESPnet toolkit: https://github.com/espnet/espnet
- THCHS-30 corpus: http://www.openslr.org/18/
