# S2 Comprehensive Pass: Tone Analysis Libraries Deep Dive

## Overview

This directory contains comprehensive deep-dive research on tone analysis libraries, algorithms, and approaches for CJK (Chinese-Japanese-Korean) language processing, with primary focus on Mandarin and Cantonese.

**Research Date:** January 29, 2026
**Research Pass:** S2 (Comprehensive)
**Related Passes:** S1 (Rapid) completed, S3 (Need-driven) pending

---

## Document Structure

### 📄 [01-parselmouth-deep-dive.md](./01-parselmouth-deep-dive.md)
**Complete analysis of Parselmouth (Python interface to Praat)**

**Contents:**
- Complete API documentation for pitch analysis
- Performance benchmarks vs. Praat GUI and librosa
- TextGrid integration capabilities
- Mandarin/Cantonese-specific parameter recommendations
- Installation requirements and compatibility (Windows, macOS, Linux)
- Code examples for tone analysis workflows

**Key Findings:**
- ✅ Identical accuracy to Praat (uses same C/C++ code)
- ✅ Zero external dependencies
- ✅ v0.5.0.dev0 released January 2026
- ✅ F0 correlation with Praat: r=0.999 (perfect)

**Verdict:** **Primary recommendation** for CJK tone analysis

---

### 📄 [02-librosa-advanced.md](./02-librosa-advanced.md)
**Detailed comparison of librosa pitch detection methods**

**Contents:**
- pYIN vs. YIN vs. piptrack detailed comparison
- Parameter tuning guides for speech analysis (fmin, fmax, frame_length, hop_length)
- Accuracy studies and research papers (June 2025 comparative study)
- Integration with tone classification algorithms
- Advanced usage patterns (batch processing, real-time streaming)
- Octave jump detection and correction

**Key Findings:**
- ⭐⭐⭐ Good accuracy (F0 percentiles: r=0.962-0.999 with Praat)
- ⚠️ F0 mean/std dev less accurate (r=0.730 mean, r=-0.536 std dev)
- ✅ Pure Python (no system dependencies)
- ⚠️ Voice onset/offset handling differs from Praat

**Verdict:** Use when Praat installation impossible or pure Python required

---

### 📄 [03-praatio-textgrid-manipulation.md](./03-praatio-textgrid-manipulation.md)
**Complete TextGrid manipulation API and batch processing**

**Contents:**
- Complete praatio API documentation
- Four output format comparison (short, long, JSON, TextGrid-JSON)
- Batch processing examples (alignment, extraction, merging)
- Integration with Praat scripts (running Praat from Python)
- Limitations and workarounds (short segments, external Praat dependency)
- Comparison with TextGridTools and Parselmouth

**Key Findings:**
- ✅ Advanced TextGrid manipulation (4 file formats)
- ⚠️ Requires external Praat for acoustic analysis
- ⚠️ Limited maintenance (fewer updates than Parselmouth)
- ⚠️ Short segment issues (<100ms unreliable)

**Verdict:** Use Parselmouth instead for most cases (integrated acoustic analysis)

---

### 📄 [04-tone-classification-algorithms.md](./04-tone-classification-algorithms.md)
**Comprehensive survey of tone classification approaches**

**Contents:**
- HMM, GMM, CNN, RNN, CNN-LSTM-Attention architectures
- Feature engineering best practices (speaker normalization, time normalization)
- Complete code examples for each method
- Accuracy benchmarks (84-90%+ depending on method)
- Benchmark datasets (THCHS-30, AISHELL-1, AISHELL-3)
- Training and deployment recommendations

**Key Findings:**
- **Traditional methods:** GMM (84.55%), SVM (85.50%), HMM (88.80%)
- **Deep learning:** CNN (87.60%), RNN (88-90%), CNN-LSTM-Attention (90%+)
- **Best practices:** Z-score normalization, time-normalization to 5 points
- **Data requirements:** 1000-10000 samples for CNN, 10000+ for LSTM

**Verdict:** CNN for production (87-88%), CNN-LSTM-Attention for research (90%+)

---

### 📄 [05-tone-sandhi-detection.md](./05-tone-sandhi-detection.md)
**Tone sandhi detection: rule-based, ML, and hybrid approaches**

**Contents:**
- Mandarin tone sandhi rules (T3+T3, 不, 一)
- CNN-based detection (97%+ accuracy)
- RNN sequence modeling (implicit rule learning)
- Hybrid rule-based + ML approaches
- Specialized tools (SPPAS, ProsodyPro)
- Implementation recommendations and code examples

**Key Findings:**
- **Rule-based:** 97.39% (training), 88.98% (test) - Taiwanese Southern-Min
- **CNN:** 97%+ accuracy, <1.9% false alarm rate - Mandarin
- **RNN:** Can learn Tone 3 sandhi rule implicitly from data
- **Hybrid:** Combining rules + ML shows best precision

**Verdict:** Hybrid rule-based + CNN verification for production

---

### 📄 [06-comparative-analysis.md](./06-comparative-analysis.md)
**Complete comparative analysis and recommendations**

**Contents:**
- Performance metrics comparison (accuracy, speed, memory)
- Feature comparison matrix (all tools and algorithms)
- Use case recommendations (production, research, prototyping, real-time)
- Accuracy vs. speed trade-offs (Pareto frontier analysis)
- Integration recommendations (pipeline architecture)
- Cost-benefit analysis
- Final recommendations by scenario

**Key Findings:**
- **Best overall:** Parselmouth (accuracy) + CNN (classification) + Rule+CNN (sandhi)
- **Best for prototyping:** librosa + GMM/SVM
- **Best for real-time:** PESTO + lightweight CNN
- **Best for research:** Parselmouth + CNN-LSTM-Attention

**Verdict:** See decision tree and scenario-specific recommendations

---

## Quick Start

### For Mandarin Tone Analysis

**1. Pitch Extraction:**
```python
import parselmouth

sound = parselmouth.Sound('audio.wav')
pitch = sound.to_pitch_ac(
    pitch_floor=70,    # Male: 70, Female: 100
    pitch_ceiling=400,  # Male: 300, Female: 500
    very_accurate=True
)

f0_values = pitch.selected_array['frequency']
```

**2. Tone Classification:**
```python
# Use pre-trained CNN model (87-88% accuracy)
# See 04-tone-classification-algorithms.md for full code
from tone_models import ToneCNN

model = ToneCNN(input_shape=(128, 44, 1), n_tones=4)
# model.load_weights('pretrained_mandarin_tones.h5')

tone, probs = model.predict('syllable.wav')
print(f"Predicted tone: T{tone+1}")
```

**3. Tone Sandhi Detection:**
```python
# Rule-based + verification
from sandhi_detector import MandarinToneSandhiDetector

detector = MandarinToneSandhiDetector()

syllables = [
    ('ni', 3, '你'),   # T3
    ('hao', 3, '好')   # T3
]

result = detector.apply_sandhi(syllables)
# Output: [('ni', 2, '你'), ('hao', 3, '好')]
# First T3 changes to T2 (T3+T3 sandhi)
```

---

## Summary Comparison

### Tool Rankings

**Pitch Detection:**
1. 🥇 **Parselmouth** - Praat accuracy, zero dependencies
2. 🥈 **CREPE** - State-of-the-art accuracy (GPU required)
3. 🥉 **librosa (pYIN)** - Good accuracy, pure Python

**Tone Classification:**
1. 🥇 **CNN-LSTM-Attention** - 90%+ accuracy (research)
2. 🥈 **CNN (ToneNet)** - 87-88% accuracy (production)
3. 🥉 **HMM/GMM** - 84-89% accuracy (traditional)

**Tone Sandhi Detection:**
1. 🥇 **Hybrid (Rule + CNN)** - 97%+ accuracy
2. 🥈 **RNN Sequence Model** - 90%+ accuracy, context-aware
3. 🥉 **Rule-based Only** - 88-97% accuracy, interpretable

**TextGrid Manipulation:**
1. 🥇 **Parselmouth** - Integrated acoustic analysis
2. 🥈 **praatio** - Advanced manipulation, 4 file formats
3. 🥉 **TextGridTools** - Interannotator agreement metrics

---

## Performance Benchmarks

### Accuracy (F0 Extraction)

| Tool | F0 Percentiles | F0 Mean | F0 Std Dev |
|------|----------------|---------|------------|
| Parselmouth | r=0.999 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| librosa (pYIN) | r=0.962-0.999 | r=0.730 | r=-0.536 |
| CREPE | State-of-the-art | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### Speed (1 minute audio @ 22050 Hz)

| Tool | Processing Time | Real-time Factor |
|------|-----------------|------------------|
| Parselmouth | ~2-3 seconds | 0.03-0.05x |
| librosa (pYIN) | ~2-3 seconds | 0.03-0.05x |
| CREPE (CPU) | ~40-60 seconds | 0.67-1.0x |
| CREPE (GPU) | ~0.4-1 second | 0.007-0.02x |

### Accuracy (Tone Classification)

| Method | Mandarin Accuracy |
|--------|-------------------|
| CNN-LSTM-Attention | 90%+ |
| RNN/LSTM | 88-90% |
| CNN | 87.60% |
| HMM | 88.80% |
| SVM | 85.50% |
| GMM | 84.55% |

---

## Recommended Stacks

### Production System (Mandarin Tone Analysis)
```
Pitch:  Parselmouth (Praat accuracy)
Tones:  Pre-trained CNN (87-88%)
Sandhi: Rule-based + CNN verification (97%+)
Grid:   Parselmouth (integrated)
Deploy: Docker + REST API
Cost:   ~$12,000 (Year 1)
```

### Research System (State-of-the-Art)
```
Pitch:  Parselmouth + CREPE validation
Tones:  CNN-LSTM-Attention (90%+)
Sandhi: RNN Sequence Model
Grid:   Parselmouth + SPPAS
Deploy: GPU cluster
Cost:   ~$22,000 (Year 1)
```

### Prototyping System (Fast Iteration)
```
Pitch:  librosa (pure Python)
Tones:  GMM/SVM (sklearn)
Sandhi: Rule-based baseline
Grid:   Manual (CSV)
Deploy: Jupyter notebook
Cost:   ~$2,000 (Year 1)
```

### Real-Time System (Low Latency)
```
Pitch:  PESTO (<10ms latency)
Tones:  Lightweight CNN (mobile-optimized)
Sandhi: Cached rules (zero latency)
Deploy: TensorFlow Lite / ONNX
Cost:   ~$15,000 (Year 1)
```

---

## Key Research Papers

### Parselmouth
- **Introducing Parselmouth: A Python interface to Praat** (2018)
  Journal of Phonetics, DOI: 10.1016/j.wocn.2017.12.001

### Comparative Studies
- **Comparative Evaluation of Acoustic Feature Extraction Tools for Clinical Speech Analysis** (June 2025)
  arXiv:2506.01129

### Pitch Detection
- **CREPE: A Convolutional Representation for Pitch Estimation** (2018)
  ICASSP 2018

- **PESTO: Pitch Estimation with Self-Supervised Training** (2024)
  ISMIR 2024

### Tone Classification
- **ToneNet: A CNN Model of Tone Classification of Mandarin Chinese** (2019)
  ResearchGate

- **Machine Learning for Mandarin Tone Recognition** (2024-2025)
  Preprints.org

### Tone Sandhi
- **Generation of Voice Signal Tone Sandhi and Melody Based on CNN** (2022)
  ACM Transactions on Asian and Low-Resource Language Information Processing

---

## Related Resources

### Benchmark Datasets
- **AISHELL-1:** 170+ hours, 400 speakers (Mandarin ASR)
- **THCHS-30:** 30 hours, 50 speakers (free Chinese corpus)
- **AISHELL-3:** >98% tone transcription accuracy (TTS corpus)

### Tools & Libraries
- **Parselmouth:** [GitHub](https://github.com/YannickJadoul/Parselmouth)
- **librosa:** [Documentation](https://librosa.org/)
- **praatio:** [GitHub](https://github.com/timmahrt/praatIO)
- **SPPAS:** Multi-lingual automatic annotation
- **ProsodyPro:** Large-scale prosody analysis

---

## Next Steps

After completing S2 comprehensive pass:

1. **S3 (Need-driven):** Focus on specific use case requirements
2. **S4 (Strategic):** Long-term technology roadmap and ecosystem analysis
3. **Implementation:** Build proof-of-concept based on recommendations
4. **Evaluation:** Benchmark on AISHELL-1/THCHS-30 datasets

---

## Contact & Contributions

For questions, corrections, or contributions to this research:
- Check existing issues in the research repository
- Submit pull requests with additional findings
- Cite papers following APA format

**Last Updated:** January 29, 2026
**Version:** 1.0.0
**Status:** Complete
