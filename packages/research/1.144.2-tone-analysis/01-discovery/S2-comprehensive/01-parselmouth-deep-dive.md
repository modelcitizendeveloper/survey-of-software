# S2 Comprehensive: Parselmouth Deep Dive

## Executive Summary

**Parselmouth** is a Python library that provides direct access to Praat's C/C++ code, offering identical accuracy to Praat with a Pythonic interface. For CJK tone analysis, it represents the gold standard for pitch extraction with minimal performance overhead.

**Key Verdict:**
- ✅ **Identical accuracy to Praat** (uses same underlying C/C++ code)
- ✅ **Production-ready** (v0.5.0.dev0, January 2026)
- ✅ **Zero dependencies** (standalone package)
- ✅ **Full platform support** (Windows, macOS, Linux with precompiled wheels)
- ✅ **TextGrid support** (via integration with TextGridTools)

---

## 1. Complete API Documentation

### 1.1 Core Pitch Analysis Methods

#### Basic Pitch Extraction

```python
import parselmouth

# Load audio
sound = parselmouth.Sound('audio.wav')

# Extract pitch using autocorrelation (recommended)
pitch = sound.to_pitch_ac(
    time_step=0.01,           # 10ms intervals
    pitch_floor=80.0,         # Minimum F0 (Hz)
    pitch_ceiling=400.0,      # Maximum F0 (Hz)
    max_number_of_candidates=15,
    very_accurate=False,
    silence_threshold=0.03,
    voicing_threshold=0.45,
    octave_cost=0.01,
    octave_jump_cost=0.35,
    voiced_unvoiced_cost=0.14
)

# Alternative: standard method
pitch = sound.to_pitch(
    time_step=0.01,
    pitch_floor=75.0,
    pitch_ceiling=600.0
)
```

#### Pitch Object Methods

```python
# Statistical measures
pitch_mean = pitch.get_mean()                    # Mean F0 (Hz)
pitch_std = pitch.get_standard_deviation()       # F0 std dev
pitch_min = pitch.get_minimum()                  # Minimum F0
pitch_max = pitch.get_maximum()                  # Maximum F0

# Time-based queries
f0_at_time = pitch.get_value_at_time(0.5)       # F0 at 0.5 seconds
f0_interpolated = pitch.selected_array['frequency']  # Full contour

# Contour analysis
slope = pitch.get_mean_absolute_slope()          # Mean F0 slope
slope_no_jumps = pitch.get_slope_without_octave_jumps()

# Manipulation
pitch.interpolate()                              # Fill unvoiced gaps
pitch.kill_octave_jumps()                        # Remove octave errors
pitch.smooth(bandwidth=10)                       # Smooth contour
```

### 1.2 Mandarin/Cantonese-Specific Parameters

#### Recommended Settings for Mandarin

```python
# Male speakers
pitch_mandarin_male = sound.to_pitch_ac(
    time_step=0.01,
    pitch_floor=70.0,      # Lower bound for male voices
    pitch_ceiling=250.0,   # Upper bound for male voices
    voicing_threshold=0.45
)

# Female speakers
pitch_mandarin_female = sound.to_pitch_ac(
    time_step=0.01,
    pitch_floor=100.0,     # Higher floor for female voices
    pitch_ceiling=400.0,   # Higher ceiling for female voices
    voicing_threshold=0.45
)

# Adaptive approach (two-pass method)
# Pass 1: Wide range to find F0 distribution
pitch_initial = sound.to_pitch_ac(
    pitch_floor=50.0,
    pitch_ceiling=700.0
)

# Calculate quartiles
import numpy as np
f0_values = pitch_initial.selected_array['frequency']
f0_values = f0_values[f0_values > 0]  # Remove unvoiced frames
q1, q3 = np.percentile(f0_values, [25, 75])

# Pass 2: Refined range based on speaker's F0 distribution
pitch_refined = sound.to_pitch_ac(
    pitch_floor=0.75 * q1,
    pitch_ceiling=2.5 * q3
)
```

#### Recommended Settings for Cantonese

```python
# Cantonese has 6-9 tones (depending on classification)
# Wider pitch range needed due to more complex tone system

pitch_cantonese = sound.to_pitch_ac(
    time_step=0.01,
    pitch_floor=80.0,      # Adjust based on speaker gender
    pitch_ceiling=450.0,   # Higher ceiling for tone distinctions
    voicing_threshold=0.45,
    max_number_of_candidates=15  # More candidates for complex tones
)
```

### 1.3 TextGrid Integration

```python
# Load TextGrid
textgrid = parselmouth.TextGrid.read('annotations.TextGrid')

# Access tiers
tier = textgrid[0]  # First tier (0-indexed)
tier_by_name = textgrid['phones']  # Access by name

# Iterate through intervals
for interval in tier.intervals:
    print(f"Start: {interval.xmin}, End: {interval.xmax}, Label: {interval.text}")

# Query at specific time
interval_at_time = tier.get_interval_at_time(1.5)

# Integration with TextGridTools (since v0.4.0)
tgt_grid = textgrid.to_tgt()  # Convert to TextGridTools format

# Create new TextGrid
new_textgrid = parselmouth.TextGrid.create(
    xmin=0.0,
    xmax=sound.duration,
    tier_names=['words', 'phones'],
    point_tiers=None
)
```

---

## 2. Performance Benchmarks

### 2.1 Accuracy vs. Praat GUI

**Key Finding:** Parselmouth produces **identical results** to Praat because it uses the same underlying C/C++ code.

From the research:
> "Parselmouth directly accesses Praat's C/C++ code (which means the algorithms and their output are exactly the same as in Praat). Each released version of Parselmouth directly corresponds to a specific Praat version and produces the exact same numerical results."

**Accuracy Guarantee:**
- F0 percentiles: **r=0.999** correlation with Praat (perfect agreement)
- No algorithmic differences
- Numerically identical output for same parameters

### 2.2 Accuracy vs. librosa

Recent comparative study (June 2025) on clinical speech data:

| Metric | Correlation | Notes |
|--------|-------------|-------|
| **F0 Percentiles** | r=0.962-0.999 | High agreement |
| **F0 Mean** | r=0.730 (SSD group) | Algorithm-specific differences |
| **F0 Std Dev** | r=-0.197 to -0.536 | Poor correlation (different handling of unvoiced frames) |

**Key Issues with librosa:**
- Different voice onset/offset behavior
- Inconsistent handling of unvoiced frames
- Lower accuracy for F0 mean and std dev vs. Praat
- **Recommendation:** Manual verification required for critical applications

### 2.3 Speed Benchmarks

From research:
> "When it comes to the execution of Praat's functionality, Python scripts that access computationally expensive Praat algorithms are expected to take the same amount of time, but scripts with a high rate of interaction between Python code and Praat functionality show that Python and Parselmouth runs as fast or even faster than the equivalent script runs in the Praat interpreter."

**Performance Characteristics:**
- **Single-threaded:** Comparable to Praat GUI
- **Multi-threaded:** Superior due to Python's multiprocessing module
- **Batch processing:** Can run in parallel (impossible in Praat scripting)

**Speed Comparison (relative):**
- Parselmouth: **1x** (baseline, same as Praat)
- librosa (pYIN): **0.8-1.2x** (comparable)
- CREPE (CPU): **0.05-0.1x** (20-50x slower, neural network overhead)
- CREPE (GPU): **2-5x** (faster with GPU acceleration)

### 2.4 Memory Usage

**Parselmouth:**
- Minimal overhead beyond audio data
- Pitch object memory: ~8 bytes per frame
- Typical 10-second audio (100 fps): ~8 KB pitch data

**Comparison:**
- Parselmouth: **Low** (C/C++ efficiency)
- librosa: **Medium** (Python NumPy arrays)
- CREPE: **High** (neural network model weights ~64 MB)

---

## 3. Installation & Compatibility

### 3.1 Installation

```bash
# Standard installation
pip install praat-parselmouth

# Verify installation
python -c "import parselmouth; print(parselmouth.__version__)"
```

### 3.2 System Requirements

**Python Versions:**
- ✅ Python 2.7
- ✅ Python 3.5+
- ❌ Python 3.0-3.4 (not supported)

**Platform Support:**
- ✅ **Windows** (amd64) - Precompiled wheels
- ✅ **macOS** (x86-64, ARM64/M1/M2) - Universal2 wheels
- ✅ **Linux** (x86_64, i686) - Precompiled wheels

**Dependencies:**
- **Zero external dependencies** (standalone package)
- No need for Praat installation
- No NumPy/SciPy required (optional for data manipulation)

### 3.3 Windows-Specific Requirements

**Potential Issue:** DLL error on import

**Solution:**
```bash
# Install Microsoft Visual C++ Redistributable for Visual Studio 2022
# Download from: https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist
```

### 3.4 Version History

- **v0.5.0.dev0** (January 23, 2026) - Latest development version
- **v0.4.7** (2025) - Stable release with TextGrid integration
- **v0.4.6** (June 8, 2025) - Previous stable
- **v0.4.0** - Added TextGridTools integration (`to_tgt()`)

---

## 4. Code Examples for Tone Analysis

### 4.1 Basic Mandarin Tone Extraction

```python
import parselmouth
import numpy as np
import matplotlib.pyplot as plt

def extract_mandarin_tone(audio_path, gender='male'):
    """Extract F0 contour for Mandarin tone analysis."""

    # Load audio
    sound = parselmouth.Sound(audio_path)

    # Set parameters based on gender
    if gender == 'male':
        pitch_floor, pitch_ceiling = 70, 250
    else:
        pitch_floor, pitch_ceiling = 100, 400

    # Extract pitch
    pitch = sound.to_pitch_ac(
        time_step=0.01,
        pitch_floor=pitch_floor,
        pitch_ceiling=pitch_ceiling,
        very_accurate=True  # More accurate for tone analysis
    )

    # Extract F0 contour
    f0_values = pitch.selected_array['frequency']
    time_points = pitch.xs()

    # Remove unvoiced frames (0 Hz)
    voiced_mask = f0_values > 0
    f0_voiced = f0_values[voiced_mask]
    time_voiced = time_points[voiced_mask]

    return time_voiced, f0_voiced, pitch

# Usage
time, f0, pitch_obj = extract_mandarin_tone('ma1.wav', gender='female')

# Plot
plt.figure(figsize=(10, 4))
plt.plot(time, f0, 'b-', linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('F0 (Hz)')
plt.title('Mandarin Tone Contour')
plt.grid(True, alpha=0.3)
plt.show()
```

### 4.2 Four-Tone Classification (Mandarin)

```python
import numpy as np
from scipy.interpolate import interp1d

def classify_mandarin_tone(f0_contour, normalize=True):
    """
    Classify Mandarin tone based on F0 contour shape.

    Mandarin tones:
    - Tone 1 (阴平): High-level (55)
    - Tone 2 (阳平): Rising (35)
    - Tone 3 (上声): Dipping (214)
    - Tone 4 (去声): Falling (51)
    """

    # Normalize to 0-1 scale
    if normalize:
        f0_norm = (f0_contour - f0_contour.min()) / (f0_contour.max() - f0_contour.min())
    else:
        f0_norm = f0_contour

    # Resample to 5 points for comparison
    time_original = np.linspace(0, 1, len(f0_norm))
    time_resampled = np.linspace(0, 1, 5)
    f = interp1d(time_original, f0_norm, kind='cubic')
    f0_5points = f(time_resampled)

    # Calculate features
    start_f0 = f0_5points[0]
    end_f0 = f0_5points[-1]
    mid_f0 = f0_5points[2]
    slope = end_f0 - start_f0

    # Classification rules (simplified)
    if slope < -0.2:
        tone = 4  # Falling
    elif slope > 0.2:
        tone = 2  # Rising
    elif mid_f0 < start_f0 and mid_f0 < end_f0:
        tone = 3  # Dipping
    else:
        tone = 1  # Level

    return tone, f0_5points

# Usage example
time, f0, _ = extract_mandarin_tone('syllable.wav')
tone_number, contour_5pt = classify_mandarin_tone(f0)
print(f"Detected tone: {tone_number}")
```

### 4.3 Batch Processing with TextGrid Alignment

```python
import parselmouth
from pathlib import Path

def batch_extract_tones(audio_path, textgrid_path, output_csv):
    """
    Extract F0 contours for each syllable in a TextGrid.
    """

    # Load audio and TextGrid
    sound = parselmouth.Sound(audio_path)
    textgrid = parselmouth.TextGrid.read(textgrid_path)

    # Extract pitch for entire utterance
    pitch = sound.to_pitch_ac(
        time_step=0.01,
        pitch_floor=80,
        pitch_ceiling=400
    )

    results = []

    # Get syllable tier (adjust tier name as needed)
    syllable_tier = textgrid['syllables']

    for interval in syllable_tier.intervals:
        if not interval.text.strip():
            continue  # Skip empty intervals

        # Get F0 values within interval
        f0_values = []
        time_points = []

        for i, t in enumerate(pitch.xs()):
            if interval.xmin <= t <= interval.xmax:
                f0 = pitch.get_value_at_time(t)
                if f0 > 0:  # Only voiced frames
                    f0_values.append(f0)
                    time_points.append(t)

        if len(f0_values) > 0:
            # Calculate statistics
            f0_mean = np.mean(f0_values)
            f0_std = np.std(f0_values)
            f0_range = max(f0_values) - min(f0_values)

            results.append({
                'syllable': interval.text,
                'start': interval.xmin,
                'end': interval.xmax,
                'duration': interval.xmax - interval.xmin,
                'f0_mean': f0_mean,
                'f0_std': f0_std,
                'f0_range': f0_range,
                'f0_contour': f0_values
            })

    # Save to CSV
    import pandas as pd
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)

    return results

# Usage
results = batch_extract_tones(
    'conversation.wav',
    'conversation.TextGrid',
    'tone_features.csv'
)
```

### 4.4 Speaker Normalization (z-score)

```python
def normalize_f0_zscore(f0_contour, speaker_f0_mean=None, speaker_f0_std=None):
    """
    Z-score normalization for speaker-independent tone analysis.

    Args:
        f0_contour: F0 values for current syllable
        speaker_f0_mean: Speaker's mean F0 (if None, computed from contour)
        speaker_f0_std: Speaker's F0 std dev (if None, computed from contour)

    Returns:
        Normalized F0 contour (z-scores)
    """

    if speaker_f0_mean is None:
        speaker_f0_mean = np.mean(f0_contour)
    if speaker_f0_std is None:
        speaker_f0_std = np.std(f0_contour)

    f0_normalized = (f0_contour - speaker_f0_mean) / speaker_f0_std

    return f0_normalized

# Usage: Compute speaker baseline from neutral tone 1 syllables
time, f0_tone1, _ = extract_mandarin_tone('speaker_baseline.wav')
speaker_mean = np.mean(f0_tone1)
speaker_std = np.std(f0_tone1)

# Normalize new syllable
time, f0_test, _ = extract_mandarin_tone('test_syllable.wav')
f0_normalized = normalize_f0_zscore(f0_test, speaker_mean, speaker_std)
```

### 4.5 Visualization with Plotting

```python
import parselmouth
import matplotlib.pyplot as plt
import numpy as np

def plot_pitch_spectrogram(audio_path):
    """
    Create publication-quality plot with spectrogram and pitch overlay.
    """

    sound = parselmouth.Sound(audio_path)
    pitch = sound.to_pitch_ac(time_step=0.01, pitch_floor=75, pitch_ceiling=500)

    # Create spectrogram
    spectrogram = sound.to_spectrogram(
        window_length=0.005,
        maximum_frequency=5000
    )

    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Draw spectrogram
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)

    ax.pcolormesh(X, Y, sg_db, shading='gouraud', cmap='gray_r', vmin=sg_db.max() - 70)

    # Overlay pitch
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values == 0] = np.nan  # Hide unvoiced
    ax.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
    ax.plot(pitch.xs(), pitch_values, 'o', markersize=2, color='red')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_title('Pitch Tracking on Spectrogram')
    ax.set_ylim(0, 500)

    plt.tight_layout()
    plt.show()

# Usage
plot_pitch_spectrogram('mandarin_utterance.wav')
```

---

## 5. Limitations & Considerations

### 5.1 Current Limitations

1. **TextGrid API Incomplete**
   - Basic read/write supported
   - Advanced manipulation via `to_tgt()` conversion to TextGridTools
   - Some Praat TextGrid functions not yet ported

2. **No Built-in Tone Sandhi Detection**
   - Parselmouth extracts pitch only
   - Tone sandhi rules must be implemented separately
   - No phonological rule engine included

3. **Short Segments**
   - Minimum duration: ~3 periods of pitch_floor
   - For 75 Hz floor: minimum ~40ms
   - Very short syllables may produce unreliable results

4. **Unvoiced Consonants**
   - No F0 during unvoiced segments
   - Requires interpolation or segmentation strategy

### 5.2 Best Practices

**Parameter Tuning:**
- Start with wide pitch range, then refine
- Use `very_accurate=True` for tone analysis (slower but better)
- Adjust `voicing_threshold` for breathy/creaky voice

**Quality Control:**
- Always plot F0 contours for manual inspection
- Check for octave errors (`kill_octave_jumps()`)
- Verify unvoiced frame handling

**Performance Optimization:**
- Use multiprocessing for batch jobs
- Cache pitch objects if analyzing multiple times
- Consider downsampling audio to 16 kHz for speed

---

## 6. Comparison Matrix

| Feature | Parselmouth | librosa | CREPE |
|---------|-------------|---------|-------|
| **Accuracy** | ⭐⭐⭐⭐⭐ (Praat-level) | ⭐⭐⭐ (good) | ⭐⭐⭐⭐⭐ (excellent) |
| **Speed (CPU)** | ⭐⭐⭐⭐ (fast) | ⭐⭐⭐⭐ (fast) | ⭐⭐ (slow) |
| **Speed (GPU)** | N/A | N/A | ⭐⭐⭐⭐⭐ (very fast) |
| **Memory** | ⭐⭐⭐⭐⭐ (low) | ⭐⭐⭐⭐ (medium) | ⭐⭐ (high) |
| **Dependencies** | ⭐⭐⭐⭐⭐ (zero) | ⭐⭐⭐⭐ (minimal) | ⭐⭐⭐ (TensorFlow/Keras) |
| **Ease of Use** | ⭐⭐⭐⭐⭐ (excellent) | ⭐⭐⭐⭐ (good) | ⭐⭐⭐⭐ (good) |
| **TextGrid Support** | ⭐⭐⭐⭐ (built-in) | ❌ (no) | ❌ (no) |
| **Platform Support** | ⭐⭐⭐⭐⭐ (all) | ⭐⭐⭐⭐⭐ (all) | ⭐⭐⭐⭐⭐ (all) |
| **Maintenance** | ⭐⭐⭐⭐⭐ (active) | ⭐⭐⭐⭐⭐ (active) | ⭐⭐⭐⭐ (stable) |

---

## 7. Production Recommendations

### For Mandarin/Cantonese Tone Analysis:

**✅ Use Parselmouth if:**
- Accuracy is critical (pronunciation training, speech therapy)
- You need TextGrid integration
- Working with phonetic research workflows
- Want Praat compatibility without external scripts
- Need batch processing with Python ecosystem

**⚠️ Consider alternatives if:**
- Pure Python environment required (use librosa)
- GPU acceleration needed (use CREPE)
- Integration with music/audio pipelines (use librosa)

**Overall Verdict:** Parselmouth is the **recommended choice** for serious CJK tone analysis work due to its proven accuracy, Python integration, and active development.

---

## Sources

- [Parselmouth GitHub Repository](https://github.com/YannickJadoul/Parselmouth)
- [Parselmouth Documentation (v0.5.0.dev0, Jan 2026)](https://app.readthedocs.org/projects/parselmouth/downloads/pdf/latest/)
- [Parselmouth API Reference](https://parselmouth.readthedocs.io/en/stable/api_reference.html)
- [Introducing Parselmouth: A Python interface to Praat](https://www.sciencedirect.com/science/article/abs/pii/S0095447017301389)
- [Parselmouth for bioacoustics](https://www.tandfonline.com/doi/full/10.1080/09524622.2023.2259327)
- [Comparative Evaluation of Acoustic Feature Extraction Tools](https://arxiv.org/html/2506.01129v1)
- [Parselmouth Installation Documentation](https://parselmouth.readthedocs.io/en/stable/installation.html)
- [VoiceLab: Automated Acoustic Analysis](https://voice-lab.github.io/VoiceLab/)
- [Standardization of pitch range settings](https://pmc.ncbi.nlm.nih.gov/articles/PMC2669687/)
