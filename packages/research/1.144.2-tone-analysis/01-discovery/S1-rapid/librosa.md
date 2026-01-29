# librosa: Python Audio Analysis Library

## Overview
Pure Python library for audio and music analysis with pitch detection capabilities suitable for tone analysis.

**Version**: 0.11.0 (current as of 2026)

## Core Pitch Detection Functions

### `librosa.pyin()`
Probabilistic YIN (pYIN) algorithm - recommended for F0 estimation
- Computes F0 candidates with probabilities
- Uses Viterbi decoding for optimal F0 sequence estimation
- Returns: f0, voiced_flag, voiced_probs

### `librosa.yin()`
Standard YIN algorithm for F0 estimation

### `librosa.piptrack()`
STFT-based pitch tracking (note: not a dedicated F0 estimator)

## Basic Usage

```python
import librosa

# Load audio file
y, sr = librosa.load('audio.wav')

# Extract pitch using pYIN
f0, voiced_flag, voiced_probs = librosa.pyin(
    y,
    sr=sr,
    fmin=librosa.note_to_hz('C2'),  # ~65 Hz
    fmax=librosa.note_to_hz('C7')   # ~2093 Hz
)

# Get timestamps
times = librosa.times_like(f0, sr=sr)
```

## Parameters for CJK Tones

**Mandarin (4 tones):**
- Pitch range: 80-400 Hz (male), 120-500 Hz (female)
- Focus on F0 contour direction

**Cantonese (6 tones):**
- Similar pitch range
- Focus on F0 height and contour
- Requires precise height discrimination

**General guidelines:**
- `fmin`: ~65-80 Hz
- `fmax`: ~400-500 Hz (adjust for speaker)
- `frame_length`: 2048 default (~93ms @ 22050 Hz)
- Best practice: At least 2 periods of fmin should fit in frame

## Strengths

1. **Pure Python** - No external dependencies on Praat/other tools
2. **Probabilistic approach** - Uncertainty estimates useful for tone boundaries
3. **Flexible and scriptable** - Easy pipeline integration
4. **Batch processing** - Efficient for large datasets
5. **Well-maintained** - Active development in 2026
6. **Additional features** - Pitch shifting, tuning estimation, spectral analysis

## Weaknesses

1. **Music-optimized** - Designed for music information retrieval, not phonetics
2. **Accuracy concerns** - Research shows variability compared to Praat
   - F0 percentiles: strong correlation (r=0.993-0.999)
   - F0 mean: moderate correlation (r=0.730 or lower)
   - F0 std dev: poor correlation (negative in some cases)
3. **Algorithm differences** - Probabilistic methods vs. Praat's cross-correlation
4. **Voice onset/offset handling** - Different behavior at transitions
5. **No tone sandhi support** - Requires custom implementation

## Use Cases for CJK

✅ **Good for:**
- Batch processing large pronunciation datasets
- Automated pipelines without Praat dependency
- Quick prototyping and experimentation
- Applications where pure Python is required

❌ **Not ideal for:**
- Research requiring Praat-level accuracy
- Clinical/diagnostic applications
- Situations where manual verification is impractical

## Sources
- [librosa.pyin documentation](https://librosa.org/doc/main/generated/librosa.pyin.html)
- [Comparative evaluation of acoustic feature extraction](https://arxiv.org/html/2506.01129v1)
