# S2 Comprehensive: librosa Advanced Features

## Executive Summary

**librosa** is a pure Python audio analysis library optimized for music and audio processing. For CJK tone analysis, it offers a lightweight alternative to Praat-based tools with good (but not Praat-level) accuracy.

**Key Verdict:**
- ✅ **Pure Python** (no external dependencies beyond NumPy/SciPy)
- ✅ **Fast** (comparable to Parselmouth for single-threaded work)
- ⚠️ **Lower accuracy** than Praat for F0 mean/std dev (voice onset/offset issues)
- ✅ **Excellent documentation** and active community
- ✅ **Rich ecosystem** (MIR features, spectral analysis, beat tracking)

**Use Case:** Choose librosa when Praat installation is impossible or when integrating with music/audio pipelines. Requires manual verification for critical tone analysis.

---

## 1. Pitch Detection Methods Comparison

### 1.1 Overview of Three Methods

| Method | Algorithm | Speed | Accuracy | Use Case |
|--------|-----------|-------|----------|----------|
| **pYIN** | Probabilistic YIN | Medium | ⭐⭐⭐⭐ | **Recommended for speech** |
| **YIN** | Autocorrelation | Fast | ⭐⭐⭐⭐ | Good for clean recordings |
| **piptrack** | Spectral peaks | Very Fast | ⭐⭐ | Music, not recommended for F0 |

### 1.2 pYIN (Probabilistic YIN) - RECOMMENDED

**What it is:**
- Modification of the YIN algorithm for fundamental frequency (F0) estimation
- Two-step process:
  1. F0 candidates and probabilities computed using YIN
  2. Viterbi decoding estimates most likely F0 sequence and voicing flags

**Advantages over YIN:**
- Outperforms conventional YIN algorithm
- Reduction in pitch errors
- Better handling of uncertainty via probabilistic approach
- Computes multiple pitch candidates with associated probabilities

**Code Example:**

```python
import librosa
import numpy as np

# Load audio
y, sr = librosa.load('mandarin_syllable.wav', sr=22050)

# Extract F0 using pYIN (RECOMMENDED)
f0, voiced_flag, voiced_probs = librosa.pyin(
    y,
    fmin=librosa.note_to_hz('C2'),  # ~65 Hz (male lower bound)
    fmax=librosa.note_to_hz('C7'),  # ~2093 Hz (female upper bound)
    sr=sr,
    frame_length=2048,              # Ideally >=2 periods of fmin
    hop_length=512,                 # Time resolution
    fill_na=None,                   # Best guess for unvoiced frames
    center=True,
    resolution=0.01,                # 0.01 = cents resolution
    max_transition_rate=35.92,      # Octaves per second
    switch_prob=0.01,               # Voiced/unvoiced transition prob
    no_trough_prob=0.01             # Probability of no trough
)

# voiced_flag: Boolean array indicating voiced frames
# voiced_probs: Confidence scores for voicing decisions

# Get time axis
times = librosa.times_like(f0, sr=sr, hop_length=512)

# Plot
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 4))
plt.plot(times, f0, 'b-', linewidth=2, label='F0 (pYIN)')
plt.fill_between(times, 0, 400, where=voiced_flag, alpha=0.2, label='Voiced')
plt.xlabel('Time (s)')
plt.ylabel('F0 (Hz)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 1.3 YIN (Standard Autocorrelation)

**What it is:**
- Autocorrelation-based method for F0 estimation
- Simpler than pYIN (no probabilistic modeling)
- Faster but less robust to noise

**Code Example:**

```python
# Extract F0 using YIN
f0_yin = librosa.yin(
    y,
    fmin=65,
    fmax=2093,
    sr=sr,
    frame_length=2048,
    hop_length=512,
    trough_threshold=0.1,  # YIN threshold (default 0.1)
    center=True
)

# Note: YIN returns raw F0 values (no voicing flags)
```

### 1.4 piptrack (Spectral Peak Tracking) - NOT RECOMMENDED FOR F0

**What it is:**
- Pitch tracking on thresholded parabolically-interpolated STFT
- Performs parabolic interpolation on spectrograms to infer local peaks
- **NOT an F0 estimator** - fundamentally different approach

**Why not recommended:**
> "piptrack is for doing parabolic interpolation on spectrograms to infer local peaks, but it is not an f0 estimator. For f0 estimation, take a look at the yin and pyin functions added in librosa 0.8."

**Code Example (for completeness):**

```python
# piptrack returns multiple pitches per frame (not true F0)
pitches, magnitudes = librosa.piptrack(
    y=y,
    sr=sr,
    threshold=0.1,
    fmin=65,
    fmax=2093
)

# Extract dominant pitch (requires additional logic)
# Not recommended for speech F0 analysis
```

---

## 2. Parameter Tuning for Speech Analysis

### 2.1 Frequency Range Parameters

**fmin (Minimum Frequency):**
- **Default:** `librosa.note_to_hz('C2')` (~65 Hz)
- **Mandarin male:** 70-80 Hz
- **Mandarin female:** 100-120 Hz
- **Cantonese:** 80-100 Hz (wider range for tone distinctions)

**fmax (Maximum Frequency):**
- **Default:** `librosa.note_to_hz('C7')` (~2093 Hz)
- **Mandarin male:** 250-300 Hz
- **Mandarin female:** 400-500 Hz
- **Cantonese:** 400-600 Hz

**Critical Rule:**
> "Ideally, at least two periods of fmin should fit into the frame (sr / fmin < frame_length / 2), otherwise it can cause inaccurate pitch detection."

**Example:**
- fmin = 75 Hz
- period = 1/75 = 0.0133 s
- 2 periods = 0.0267 s
- sr = 22050 Hz
- Required frame_length >= sr * 0.0267 = 588 samples
- **Use frame_length=2048 to be safe**

### 2.2 Time Resolution Parameters

**frame_length:**
- Controls frequency resolution
- Larger = better frequency resolution, worse time resolution
- **Recommended for speech:** 2048 samples @ 22050 Hz = ~93ms

**hop_length:**
- Controls time step between frames
- Smaller = better time resolution, more computation
- **Recommended for speech:** 512 samples @ 22050 Hz = ~23ms (4x oversampling)

**Example calculation:**

```python
sr = 22050
frame_length = 2048
hop_length = 512

time_resolution = hop_length / sr  # 0.023 seconds = 23ms
freq_resolution = sr / frame_length  # 10.77 Hz

print(f"Time resolution: {time_resolution*1000:.1f} ms")
print(f"Frequency resolution: {freq_resolution:.2f} Hz")
```

### 2.3 pYIN-Specific Parameters

**max_transition_rate:**
- Maximum pitch transition rate in octaves per second
- **Default:** 35.92 (allows rapid changes)
- **For slow speech:** 10-20
- **For normal speech:** 20-35
- **For fast speech/singing:** 35-50

**switch_prob:**
- Probability of switching from voiced to unvoiced or vice versa
- **Default:** 0.01 (1% probability)
- **For clean recordings:** 0.01
- **For noisy recordings:** 0.05-0.1

**resolution:**
- Resolution of pitch bins
- **Default:** 0.01 (corresponds to cents)
- Finer resolution = more candidates = slower computation

**fill_na:**
- Default value for unvoiced frames
- **None:** Use best guess (interpolation)
- **np.nan:** Mark as NaN
- **0.0:** Mark as 0 Hz

### 2.4 Complete Parameter Guide

```python
def extract_f0_optimized(
    audio_path,
    gender='male',
    speech_rate='normal',
    recording_quality='clean'
):
    """
    Extract F0 with optimized parameters for Mandarin Chinese.
    """

    # Load audio
    y, sr = librosa.load(audio_path, sr=22050)

    # Gender-specific frequency ranges
    if gender == 'male':
        fmin, fmax = 70, 300
    elif gender == 'female':
        fmin, fmax = 100, 500
    else:
        fmin, fmax = 70, 500  # Wide range

    # Speech rate adjustments
    if speech_rate == 'slow':
        max_transition_rate = 15
    elif speech_rate == 'fast':
        max_transition_rate = 45
    else:
        max_transition_rate = 30

    # Recording quality adjustments
    if recording_quality == 'noisy':
        switch_prob = 0.1
        trough_threshold = 0.15
    else:
        switch_prob = 0.01
        trough_threshold = 0.1

    # Extract F0
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        fmin=fmin,
        fmax=fmax,
        sr=sr,
        frame_length=2048,
        hop_length=512,
        fill_na=None,
        resolution=0.01,
        max_transition_rate=max_transition_rate,
        switch_prob=switch_prob
    )

    return f0, voiced_flag, voiced_probs, sr

# Usage
f0, voiced, probs, sr = extract_f0_optimized(
    'mandarin_utterance.wav',
    gender='female',
    speech_rate='normal',
    recording_quality='clean'
)
```

---

## 3. Accuracy Studies & Limitations

### 3.1 Comparative Study (June 2025)

**Study:** "Comparative Evaluation of Acoustic Feature Extraction Tools for Clinical Speech Analysis"

**Compared tools:** OpenSMILE, Praat, librosa on clinical speech data

**Results:**

| Metric | Correlation with Praat | Notes |
|--------|------------------------|-------|
| **F0 Percentiles** | r=0.962-0.999 | ✅ High agreement |
| **F0 Mean** | r=0.730 (SSD), r=0.189 (HC) | ⚠️ Moderate-poor correlation |
| **F0 Std Dev** | r=-0.197 to -0.536 | ❌ Poor correlation (negative!) |

**Key Findings:**

1. **F0 Percentiles:** Strong agreement between all tools
2. **F0 Mean:** Algorithm-specific differences in handling unvoiced frames or edge conditions
3. **F0 Std Dev:** Poor correlation likely stems from fundamental differences in F0 extraction algorithms and how they handle voice onset/offset transitions

### 3.2 Known Limitations

**Voice Onset/Offset Issues:**
- librosa handles transitions differently than Praat
- Can cause significant differences in F0 mean and std dev
- **Impact:** More pronounced for short syllables with rapid voicing changes

**Unvoiced Frame Handling:**
- Different algorithms for filling gaps in F0 contours
- Affects mean and variance calculations
- **Impact:** Tone sandhi detection may be affected

**Octave Errors:**
- Less robust than Praat at avoiding octave jumps
- No built-in `kill_octave_jumps()` function
- **Impact:** Manual post-processing required

**Short Segment Performance:**
- Requires minimum duration based on fmin
- Very short syllables (<100ms) may be unreliable
- **Impact:** Problematic for rapid speech

### 3.3 Comparison with Other Methods

**pYIN vs. YAAPT vs. CREPE (2022 study):**
> "A comparison study from 2022 evaluated pYIN alongside other algorithms (YAAPT and CREPE) for speech analysis, examining voicing decision errors and pitch errors on speech databases."

**Results:**
- pYIN outperforms conventional YIN algorithm
- pYIN competitive with YAAPT for speech
- CREPE remains state-of-the-art for accuracy (but slower)

### 3.4 Recommendations for Critical Applications

**✅ Use librosa if:**
- Pure Python environment required
- Praat installation impossible
- Integration with music/audio pipelines needed
- Batch processing at scale (millions of files)
- Prototyping phase

**⚠️ Manual verification required:**
- Always plot F0 contours for inspection
- Cross-validate with Praat/Parselmouth on sample data
- Use F0 percentiles (more reliable) over mean/std dev
- Implement octave jump detection

**❌ Don't use librosa if:**
- Clinical/research-grade accuracy required
- Pronunciation training (user-facing feedback)
- Subtle tone distinctions critical (e.g., tone sandhi research)
- → Use Parselmouth instead

---

## 4. Integration with Tone Classification

### 4.1 Feature Engineering Pipeline

```python
import librosa
import numpy as np
from scipy.interpolate import interp1d

def extract_tone_features(audio_path, gender='male'):
    """
    Extract features for Mandarin tone classification.
    """

    # Load audio
    y, sr = librosa.load(audio_path, sr=22050)

    # Extract F0
    fmin = 70 if gender == 'male' else 100
    fmax = 300 if gender == 'male' else 500

    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        fmin=fmin,
        fmax=fmax,
        sr=sr,
        frame_length=2048,
        hop_length=512,
        fill_na=None
    )

    # Remove unvoiced frames
    f0_voiced = f0[voiced_flag]

    if len(f0_voiced) < 3:
        return None  # Insufficient voiced frames

    # Time-normalize to 5 points
    time_original = np.linspace(0, 1, len(f0_voiced))
    time_resampled = np.linspace(0, 1, 5)
    f = interp1d(time_original, f0_voiced, kind='cubic')
    f0_5points = f(time_resampled)

    # Extract features
    features = {
        # Statistical features
        'f0_mean': np.mean(f0_voiced),
        'f0_std': np.std(f0_voiced),
        'f0_min': np.min(f0_voiced),
        'f0_max': np.max(f0_voiced),
        'f0_range': np.max(f0_voiced) - np.min(f0_voiced),

        # Contour shape features
        'f0_start': f0_5points[0],
        'f0_mid': f0_5points[2],
        'f0_end': f0_5points[-1],
        'slope': f0_5points[-1] - f0_5points[0],

        # Velocity features
        'f0_velocity': np.diff(f0_5points),

        # Normalized contour
        'f0_5points': f0_5points,

        # Voicing features
        'voicing_ratio': np.sum(voiced_flag) / len(voiced_flag),
        'mean_voiced_prob': np.mean(voiced_probs[voiced_flag])
    }

    return features

# Usage
features = extract_tone_features('ma1.wav', gender='female')
print(f"F0 mean: {features['f0_mean']:.1f} Hz")
print(f"Slope: {features['slope']:.1f} Hz")
print(f"5-point contour: {features['f0_5points']}")
```

### 4.2 Speaker Normalization

```python
def normalize_f0_semitone(f0_contour, reference_f0=None):
    """
    Convert F0 to semitone scale relative to reference.

    Semitone normalization is more perceptually relevant than z-score.
    """

    if reference_f0 is None:
        reference_f0 = np.median(f0_contour)

    # Convert to semitones: 12 * log2(f0 / reference)
    semitones = 12 * np.log2(f0_contour / reference_f0)

    return semitones

def normalize_f0_zscore(f0_contour, speaker_mean=None, speaker_std=None):
    """
    Z-score normalization for speaker independence.
    """

    if speaker_mean is None:
        speaker_mean = np.mean(f0_contour)
    if speaker_std is None:
        speaker_std = np.std(f0_contour)

    f0_normalized = (f0_contour - speaker_mean) / speaker_std

    return f0_normalized

# Usage
y, sr = librosa.load('mandarin_syllable.wav')
f0, voiced, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr)
f0_voiced = f0[voiced]

# Semitone normalization (recommended for perception)
f0_semitones = normalize_f0_semitone(f0_voiced, reference_f0=np.median(f0_voiced))

# Z-score normalization (recommended for ML)
f0_zscore = normalize_f0_zscore(f0_voiced)
```

### 4.3 Tone Classification with librosa Features

```python
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def classify_tone_ml(features, model=None):
    """
    Classify Mandarin tone using machine learning.

    Features should include:
    - f0_mean, f0_std, f0_range
    - f0_start, f0_mid, f0_end, slope
    - f0_5points (normalized)
    """

    if model is None:
        # Load pre-trained model (placeholder)
        model = RandomForestClassifier()

    # Feature vector
    X = np.array([
        features['f0_mean'],
        features['f0_std'],
        features['f0_range'],
        features['slope'],
        features['f0_start'],
        features['f0_mid'],
        features['f0_end']
    ]).reshape(1, -1)

    # Predict
    tone = model.predict(X)[0]
    proba = model.predict_proba(X)[0]

    return tone, proba

# Example training workflow
def train_tone_classifier(audio_files, labels):
    """
    Train tone classifier on labeled data.
    """

    # Extract features for all files
    feature_list = []
    for audio_path in audio_files:
        features = extract_tone_features(audio_path)
        if features is not None:
            feature_list.append(features)

    # Convert to DataFrame
    df = pd.DataFrame(feature_list)

    # Feature matrix
    X = df[['f0_mean', 'f0_std', 'f0_range', 'slope',
            'f0_start', 'f0_mid', 'f0_end']].values

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, labels)

    return model
```

---

## 5. Advanced Usage Patterns

### 5.1 Batch Processing Pipeline

```python
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import pandas as pd

def process_single_file(audio_path):
    """Process single audio file."""
    try:
        features = extract_tone_features(audio_path)
        return {'file': audio_path.name, **features}
    except Exception as e:
        print(f"Error processing {audio_path}: {e}")
        return None

def batch_process_tones(audio_dir, output_csv, n_workers=4):
    """
    Batch process audio files in parallel.
    """

    audio_files = list(Path(audio_dir).glob('*.wav'))

    # Parallel processing
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        results = list(executor.map(process_single_file, audio_files))

    # Filter out failed files
    results = [r for r in results if r is not None]

    # Save to CSV
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)

    print(f"Processed {len(results)} files -> {output_csv}")

# Usage
batch_process_tones(
    audio_dir='mandarin_corpus/',
    output_csv='tone_features.csv',
    n_workers=8
)
```

### 5.2 Real-Time F0 Tracking (Streaming)

```python
import librosa
import numpy as np

class RealtimeF0Tracker:
    """
    Real-time F0 tracking with overlap-add buffering.
    """

    def __init__(self, sr=22050, frame_length=2048, hop_length=512):
        self.sr = sr
        self.frame_length = frame_length
        self.hop_length = hop_length
        self.buffer = np.array([])

    def process_chunk(self, audio_chunk):
        """
        Process incoming audio chunk.

        Args:
            audio_chunk: 1D numpy array of audio samples

        Returns:
            f0: Estimated F0 for this chunk (or None if insufficient data)
        """

        # Append to buffer
        self.buffer = np.concatenate([self.buffer, audio_chunk])

        # Check if we have enough samples
        if len(self.buffer) < self.frame_length:
            return None

        # Extract F0 for current frame
        frame = self.buffer[:self.frame_length]

        try:
            f0, _, _ = librosa.pyin(
                frame,
                fmin=70,
                fmax=400,
                sr=self.sr,
                frame_length=self.frame_length,
                hop_length=self.hop_length
            )

            # Advance buffer
            self.buffer = self.buffer[self.hop_length:]

            return f0[0] if len(f0) > 0 else None

        except Exception as e:
            print(f"Error in F0 extraction: {e}")
            return None

# Usage
tracker = RealtimeF0Tracker(sr=22050)

# Simulate real-time chunks (512 samples = ~23ms @ 22050 Hz)
y, sr = librosa.load('test.wav', sr=22050)

for i in range(0, len(y), 512):
    chunk = y[i:i+512]
    f0 = tracker.process_chunk(chunk)
    if f0 is not None:
        print(f"Time: {i/sr:.3f}s, F0: {f0:.1f} Hz")
```

### 5.3 Octave Jump Detection & Correction

```python
def detect_octave_jumps(f0_contour, threshold=0.7):
    """
    Detect and correct octave jumps in F0 contour.

    Args:
        f0_contour: F0 values (Hz)
        threshold: Ratio threshold for octave jump (default 0.7 = 70%)

    Returns:
        Corrected F0 contour
    """

    f0_corrected = f0_contour.copy()

    for i in range(1, len(f0_corrected)):
        if f0_corrected[i] == 0:
            continue  # Skip unvoiced frames

        ratio = f0_corrected[i] / f0_corrected[i-1]

        # Check for octave jump up (ratio ~2.0)
        if 1.7 < ratio < 2.3:
            f0_corrected[i] /= 2.0

        # Check for octave jump down (ratio ~0.5)
        elif 0.43 < ratio < 0.59:
            f0_corrected[i] *= 2.0

    return f0_corrected

# Usage
y, sr = librosa.load('audio.wav')
f0, voiced, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr)

# Correct octave jumps
f0_corrected = detect_octave_jumps(f0)

# Compare
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(f0, 'b-', label='Original')
plt.title('Original F0')
plt.ylabel('Hz')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(f0_corrected, 'r-', label='Corrected')
plt.title('Corrected F0 (Octave Jumps Removed)')
plt.ylabel('Hz')
plt.xlabel('Frame')
plt.legend()
plt.tight_layout()
plt.show()
```

---

## 6. Benchmarks & Performance

### 6.1 Speed Comparison

**Single-threaded (1 minute of audio @ 22050 Hz):**
- pYIN: ~2-3 seconds (0.03-0.05x real-time)
- YIN: ~1-2 seconds (0.02-0.03x real-time)
- piptrack: ~0.5-1 second (0.01-0.02x real-time)

**Multi-threaded (100 files, 8 cores):**
- Linear speedup with ProcessPoolExecutor
- ~8x faster than single-threaded

**Comparison to alternatives:**
- librosa pYIN: **1x** (baseline)
- Parselmouth: **~1x** (comparable)
- CREPE (CPU): **~0.05x** (20x slower)
- CREPE (GPU): **~5x** (5x faster with GPU)

### 6.2 Memory Usage

**Per audio file (1 minute @ 22050 Hz):**
- Raw audio: ~5 MB (float32)
- F0 contour: ~4 KB (512 samples)
- Total: **~5 MB per file**

**Batch processing (1000 files):**
- With multiprocessing: **~40-80 MB** (8 workers × 5 MB)
- Sequential: **~5 MB** (constant memory)

### 6.3 Accuracy Metrics

**From 2022 benchmark study:**
- pYIN error rate: **~3x lower** than conventional methods
- CREPE error rate: **~5x lower** than pYIN (state-of-the-art)

**Practical accuracy for Mandarin tones:**
- Tone 1 (level): ✅ Excellent
- Tone 2 (rising): ✅ Good
- Tone 3 (dipping): ⚠️ Fair (onset/offset issues)
- Tone 4 (falling): ✅ Good

---

## 7. Use Case Recommendations

### ✅ Use librosa for:

1. **Prototyping & Experimentation**
   - Quick iteration on tone analysis algorithms
   - Testing different parameter configurations
   - Research without production requirements

2. **Pure Python Environments**
   - Docker containers without system dependencies
   - Cloud functions (AWS Lambda, Google Cloud Functions)
   - Jupyter notebooks for teaching

3. **Music/Audio Pipeline Integration**
   - Applications using librosa for other features (MFCCs, spectrograms)
   - Beat tracking + tone analysis hybrid systems
   - Audio augmentation pipelines

4. **Large-Scale Batch Processing**
   - Millions of files where manual verification impractical
   - F0 percentiles sufficient (more reliable than mean/std)
   - Non-critical applications (e.g., data exploration)

### ⚠️ Use with caution for:

1. **Tone Sandhi Research**
   - Voice onset/offset issues may affect sandhi detection
   - Recommend Parselmouth for subtle distinctions

2. **Clinical Applications**
   - Speech therapy feedback
   - Pronunciation training (user-facing)
   - Medical diagnostics

3. **Short Syllables**
   - <100ms duration may produce unreliable results
   - Cross-validate with Praat/Parselmouth

### ❌ Don't use librosa for:

1. **Production Pronunciation Training**
   - Use Parselmouth for Praat-level accuracy

2. **Research-Grade Publications**
   - Reviewers expect Praat/Parselmouth validation
   - F0 mean/std differences may affect conclusions

3. **Real-Time Critical Systems**
   - Consider CREPE with GPU for better accuracy
   - Or Parselmouth for lower latency

---

## 8. Summary Comparison

| Feature | librosa | Parselmouth | CREPE |
|---------|---------|-------------|-------|
| **Accuracy** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐⭐ Excellent |
| **Speed** | ⭐⭐⭐⭐ Fast | ⭐⭐⭐⭐ Fast | ⭐⭐ Slow (CPU) |
| **Dependencies** | NumPy/SciPy | Zero | TensorFlow/Keras |
| **Ease of Use** | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Good |
| **F0 Mean Accuracy** | ⚠️ Moderate | ✅ Excellent | ✅ Excellent |
| **F0 Std Accuracy** | ❌ Poor | ✅ Excellent | ✅ Excellent |
| **Tone Analysis** | ⚠️ Fair | ✅ Excellent | ✅ Excellent |
| **Best For** | Prototyping, Pure Python | Production, Research | GPU-accelerated pipelines |

---

## Sources

- [librosa Documentation (v0.11.0)](https://librosa.org/doc/main/)
- [librosa.pyin Documentation](https://librosa.org/doc/main/generated/librosa.pyin.html)
- [librosa.yin Documentation](https://librosa.org/doc/main/generated/librosa.yin.html)
- [librosa.piptrack Documentation](https://librosa.org/doc/main/generated/librosa.piptrack.html)
- [Comparing Conventional Pitch Detection (2022)](https://arxiv.org/pdf/2206.14357)
- [Comparative Evaluation of Acoustic Feature Extraction Tools (June 2025)](https://arxiv.org/html/2506.01129v1)
- [librosa: Audio and Music Signal Analysis in Python](https://www.researchgate.net/publication/328777063_librosa_Audio_and_Music_Signal_Analysis_in_Python)
- [librosa GitHub - Pitch Detection Discussion](https://github.com/librosa/librosa/issues/1102)
- [Open-source packages for using speech data in ML](https://drivendata.co/blog/speech-for-ml)
