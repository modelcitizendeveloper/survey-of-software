# S2 Comprehensive: Comparative Analysis & Recommendations

## Executive Summary

This document provides a comprehensive comparison of tone analysis libraries, algorithms, and approaches for CJK (Chinese-Japanese-Korean) tone analysis, with focus on Mandarin and Cantonese.

**Key Recommendations:**
- **Pitch Extraction:** Parselmouth (Praat-level accuracy, Python integration)
- **Tone Classification:** CNN-LSTM hybrid (90%+ accuracy)
- **Tone Sandhi Detection:** Hybrid rule-based + CNN (97%+ accuracy)
- **TextGrid Manipulation:** Parselmouth (integrated with acoustic analysis)

---

## 1. Performance Metrics Comparison

### 1.1 Pitch Detection Accuracy

| Tool | F0 Percentiles | F0 Mean | F0 Std Dev | Overall |
|------|----------------|---------|------------|---------|
| **Parselmouth** | ⭐⭐⭐⭐⭐ (r=0.999) | ⭐⭐⭐⭐⭐ (Praat-identical) | ⭐⭐⭐⭐⭐ (Praat-identical) | **Excellent** |
| **librosa (pYIN)** | ⭐⭐⭐⭐⭐ (r=0.962-0.999) | ⭐⭐⭐ (r=0.730) | ⭐⭐ (r=-0.197 to -0.536) | **Good** |
| **CREPE** | ⭐⭐⭐⭐⭐ (state-of-the-art) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Excellent** |
| **YIN (librosa)** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | **Good** |

**Sources:**
- Parselmouth: Identical to Praat (uses same C/C++ code)
- librosa: Comparative study (June 2025), SSD and HC groups
- CREPE: State-of-the-art neural network (2018)

**Key Insight:**
> "F0 standard deviation exhibits poor correlation between tools, with negative correlations between OpenSMILE and Librosa (r=-0.536 for SSD). This discrepancy likely stems from fundamental differences in the underlying F0 extraction algorithms and how they handle voice onset/offset transitions."

### 1.2 Speed Benchmarks (CPU)

**Single-threaded (1 minute audio @ 22050 Hz):**

| Tool | Processing Time | Real-time Factor | Speed Rating |
|------|-----------------|------------------|--------------|
| **Parselmouth** | ~2-3 seconds | 0.03-0.05x | ⭐⭐⭐⭐ Fast |
| **librosa (pYIN)** | ~2-3 seconds | 0.03-0.05x | ⭐⭐⭐⭐ Fast |
| **librosa (YIN)** | ~1-2 seconds | 0.02-0.03x | ⭐⭐⭐⭐⭐ Very Fast |
| **CREPE (CPU)** | ~40-60 seconds | 0.67-1.0x | ⭐⭐ Slow |
| **CREPE (GPU)** | ~0.4-1 second | 0.007-0.02x | ⭐⭐⭐⭐⭐ Very Fast |
| **PESTO (SSL)** | ~10ms latency | Real-time | ⭐⭐⭐⭐⭐ Very Fast |

**Multi-threaded (100 files, 8 cores):**
- Parselmouth: ~8x speedup with multiprocessing
- librosa: ~8x speedup with multiprocessing
- CREPE: Limited parallelization (GPU batch processing better)

**Key Insight:**
> "Python's built-in multiprocessing module can run analysis in parallel with minimal extra effort, something which is impossible to do in Praat."

### 1.3 Memory Usage

| Tool | Memory per File (1 min) | Model Size | Memory Rating |
|------|-------------------------|------------|---------------|
| **Parselmouth** | ~5 MB | N/A | ⭐⭐⭐⭐⭐ Low |
| **librosa** | ~5 MB | N/A | ⭐⭐⭐⭐⭐ Low |
| **CREPE** | ~10 MB + 64 MB model | 64 MB | ⭐⭐⭐ Medium |
| **PESTO** | ~10 MB + 0.1 MB model | 0.1 MB | ⭐⭐⭐⭐⭐ Low |

**Key Insight:**
> "PESTO has low latency (less than 10 ms) and minimal parameter count, making it particularly suitable for real-time applications."

---

## 2. Feature Comparison Matrix

### 2.1 Pitch Detection Tools

| Feature | Parselmouth | librosa | CREPE | PESTO |
|---------|-------------|---------|-------|-------|
| **Accuracy** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Speed (CPU)** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Speed (GPU)** | N/A | N/A | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Memory** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Dependencies** | Zero | NumPy/SciPy | TensorFlow | PyTorch (optional) |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **TextGrid Support** | ✅ Built-in | ❌ No | ❌ No | ❌ No |
| **Real-time Capable** | ✅ Yes | ✅ Yes | ⚠️ GPU only | ✅ Yes |
| **Training Required** | ❌ No | ❌ No | ✅ Pre-trained | ✅ Pre-trained |
| **Best For** | Research, Production | Prototyping | GPU pipelines | Real-time apps |

### 2.2 Tone Classification Algorithms

| Method | Accuracy | Training Time | Inference Speed | Data Requirements | Interpretability |
|--------|----------|---------------|-----------------|-------------------|------------------|
| **GMM** | 84.55% | ⭐⭐⭐⭐⭐ Fast | ⭐⭐⭐⭐⭐ Fast | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐⭐ High |
| **SVM** | 85.50% | ⭐⭐⭐⭐ Fast | ⭐⭐⭐⭐ Fast | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐ Good |
| **HMM** | 88.80% | ⭐⭐⭐⭐ Fast | ⭐⭐⭐⭐ Fast | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐ Good |
| **CNN** | 87.60% | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐ Fast | ⭐⭐ Large | ⭐⭐ Low |
| **RNN/LSTM** | 88-90% | ⭐⭐ Slow | ⭐⭐⭐ Moderate | ⭐⭐ Large | ⭐⭐ Low |
| **CNN-LSTM-Attention** | 90%+ | ⭐ Very Slow | ⭐⭐⭐ Moderate | ⭐ Very Large | ⭐⭐⭐ Fair |

**Key Insight:**
> "Tone classification accuracies of the Gaussian mixture model, BPNN, SVM, and convolutional neural network (CNN) were 84.55%, 86.28%, 85.50%, and 87.60%, respectively."

### 2.3 TextGrid Tools

| Feature | Parselmouth | praatio | TextGridTools |
|---------|-------------|---------|---------------|
| **Read/Write** | ✅ Excellent | ✅ Excellent | ✅ Excellent |
| **File Formats** | 2 (short, long) | 4 (short, long, JSON, TG-JSON) | 2 (short, long) |
| **Manipulation API** | ⭐⭐⭐ Basic | ⭐⭐⭐⭐⭐ Extensive | ⭐⭐⭐⭐⭐ Extensive |
| **Acoustic Analysis** | ✅ Built-in | ⚠️ Via external Praat | ❌ No |
| **Batch Processing** | ⭐⭐⭐ Manual | ⭐⭐⭐⭐ Examples | ⭐⭐⭐ Manual |
| **Interannotator Agreement** | ❌ No | ❌ No | ✅ Yes |
| **Praat Script Integration** | ✅ Excellent | ✅ Good | ❌ No |
| **Dependencies** | Zero | Minimal | Minimal |
| **Maintenance** | ⭐⭐⭐⭐⭐ Active | ⭐⭐ Low | ⭐⭐ Low |

**Verdict:** **Parselmouth wins** for most use cases due to integrated acoustic analysis + TextGrid support.

---

## 3. Use Case Recommendations

### 3.1 Decision Tree

```
┌─────────────────────────────────────────┐
│  What is your primary goal?             │
└─────────────┬───────────────────────────┘
              │
      ┌───────┴────────┐
      │                 │
   PITCH            TONE               TEXTGRID         TONE
   EXTRACTION      CLASSIFICATION      MANIPULATION     SANDHI
      │                 │                 │                │
      ▼                 ▼                 ▼                ▼
  ┌────────┐      ┌──────────┐      ┌──────────┐    ┌──────────┐
  │Research│      │Small Data│      │ + Acoustic│    │Rule-based│
  │Quality?│      │(<1000)?  │      │  Analysis?│    │Sufficient│
  └───┬────┘      └────┬─────┘      └─────┬────┘    └────┬─────┘
      │                 │                  │              │
     YES               YES                YES             NO
      │                 │                  │              │
      ▼                 ▼                  ▼              ▼
 PARSELMOUTH        GMM/SVM          PARSELMOUTH   CNN/RNN-LSTM
      │                 │                  │              │
      NO                NO                 NO            YES
      │                 │                  │              │
      ▼                 ▼                  ▼              ▼
 LIBROSA           CNN-LSTM            PRAATIO        HYBRID
 (Pure Python)    (>10k samples)    (TextGrid only)  (Rule+ML)
```

### 3.2 Scenario-Specific Recommendations

#### Scenario 1: Pronunciation Training App (Production)

**Requirements:**
- Praat-level accuracy for user feedback
- Real-time processing (<100ms)
- TextGrid integration for phoneme alignment
- Cross-platform (Web, iOS, Android)

**Recommended Stack:**
```
Pitch Extraction:  Parselmouth (or PESTO for real-time)
Tone Classification:  Pre-trained CNN (87-88% accuracy)
Tone Sandhi:  Rule-based + CNN verification
TextGrid:  Parselmouth (integrated)
```

**Justification:**
- Parselmouth: Praat accuracy + zero dependencies
- PESTO alternative: <10ms latency for real-time
- CNN: Fast inference, good accuracy
- Rules: High precision for common sandhi patterns

#### Scenario 2: Large-Scale Corpus Analysis (Research)

**Requirements:**
- Process millions of audio files
- Extract statistical features
- Flexible feature engineering
- Publication-quality results

**Recommended Stack:**
```
Pitch Extraction:  Parselmouth (accuracy) or librosa (speed)
Tone Classification:  CNN-LSTM-Attention (90%+ accuracy)
Tone Sandhi:  RNN sequence model (context modeling)
TextGrid:  Parselmouth + SPPAS (auto-annotation)
Batch Processing:  Python multiprocessing (8+ cores)
```

**Justification:**
- Parselmouth: Reviewers expect Praat validation
- CNN-LSTM-Attention: State-of-the-art accuracy
- RNN: Learns implicit sandhi rules
- Multiprocessing: Linear speedup for batch jobs

#### Scenario 3: Real-Time Speech Recognition (Industry)

**Requirements:**
- Low latency (<50ms)
- Streaming audio
- GPU acceleration
- High throughput (100+ streams)

**Recommended Stack:**
```
Pitch Extraction:  PESTO (self-supervised, <10ms)
Tone Classification:  Lightweight CNN (mobile-optimized)
Tone Sandhi:  Cached rule-based (no latency)
Deployment:  TensorFlow Lite / ONNX Runtime
```

**Justification:**
- PESTO: Minimal latency, competitive accuracy
- Lightweight CNN: Fast inference on mobile/edge devices
- Rule-based: Zero latency for common patterns
- TFLite/ONNX: Optimized for production

#### Scenario 4: Prototyping / Experimentation (Academic)

**Requirements:**
- Quick iteration
- No dependencies (Docker-friendly)
- Jupyter notebook workflow
- Cost-effective (no GPU needed)

**Recommended Stack:**
```
Pitch Extraction:  librosa (pure Python)
Tone Classification:  sklearn (GMM, SVM, Random Forest)
Tone Sandhi:  Rule-based (baseline)
Visualization:  matplotlib + librosa.display
```

**Justification:**
- librosa: Pure Python, no system dependencies
- sklearn: Fast training, interpretable
- Rules: Quick baseline for comparison
- Jupyter: Interactive exploration

---

## 4. Accuracy vs. Speed Trade-offs

### 4.1 Pareto Frontier

```
Accuracy (%)
   100 │                    ◆ Parselmouth (Praat)
       │                    ◆ CREPE (GPU)
       │
    95 │         ◆ CNN-LSTM-Attention
       │      ◆ RNN/LSTM
       │   ◆ CNN
    90 │ ◆ HMM
       │◆ librosa (pYIN)
       │
    85 │ GMM ◆
       │
    80 │
       └──────────────────────────────────────> Speed
         Slow           Fast           Very Fast
       (60s+)        (2-5s)           (<1s)
```

**Key Observations:**
1. **Parselmouth + CREPE (GPU):** Best accuracy + fast
2. **librosa (pYIN):** Good accuracy + fast
3. **CNN-LSTM-Attention:** Best ML accuracy but slower training
4. **GMM/HMM:** Fastest training, lower accuracy

### 4.2 Resource Requirements

**Development Time:**
- **Rule-based:** 1-2 days (implement linguistic rules)
- **Traditional ML (GMM/SVM):** 3-5 days (feature engineering + training)
- **CNN:** 1-2 weeks (architecture design + training)
- **CNN-LSTM-Attention:** 2-4 weeks (complex architecture + tuning)

**Training Data Requirements:**
- **Rule-based:** 0 samples (hand-coded rules)
- **GMM/HMM:** 100-1000 samples
- **CNN:** 1000-10000 samples
- **CNN-LSTM-Attention:** 10000+ samples

**Computational Resources:**
- **Parselmouth/librosa:** CPU sufficient
- **CNN training:** GPU recommended (10-100x speedup)
- **CNN inference:** CPU acceptable for single-threaded
- **Large-scale batch:** Multi-core CPU or GPU cluster

---

## 5. Integration Recommendations

### 5.1 Recommended Pipeline Architecture

**Complete Tone Analysis System:**

```python
class ToneAnalysisPipeline:
    """
    Production-ready tone analysis pipeline combining best tools.
    """

    def __init__(self):
        # Pitch extraction (Parselmouth for accuracy)
        self.pitch_extractor = parselmouth

        # Tone classification (pre-trained CNN)
        self.tone_classifier = load_pretrained_cnn()

        # Tone sandhi detection (hybrid)
        self.sandhi_detector = HybridSandhiDetector()

        # TextGrid manipulation (Parselmouth)
        self.textgrid_handler = parselmouth.TextGrid

    def analyze(self, audio_path, transcript=None):
        """
        Full analysis pipeline.

        Returns:
            {
                'f0_contour': [...],
                'syllable_tones': [...],
                'surface_tones': [...],  # After sandhi
                'textgrid': TextGrid object
            }
        """
        # Step 1: Load audio
        sound = parselmouth.Sound(audio_path)

        # Step 2: Extract pitch
        pitch = sound.to_pitch_ac(
            pitch_floor=70,
            pitch_ceiling=400,
            very_accurate=True
        )

        f0_contour = pitch.selected_array['frequency']

        # Step 3: Segment syllables (forced alignment if transcript provided)
        if transcript:
            syllables = self.forced_alignment(audio_path, transcript)
        else:
            syllables = self.auto_segment(sound, pitch)

        # Step 4: Classify tones
        syllable_tones = []
        for syllable in syllables:
            f0_segment = self.extract_f0_segment(pitch, syllable['start'], syllable['end'])
            tone, prob = self.tone_classifier.predict(f0_segment)
            syllable_tones.append(tone)

        # Step 5: Detect tone sandhi
        surface_tones = self.sandhi_detector.apply_sandhi(syllables, syllable_tones)

        # Step 6: Create TextGrid
        textgrid = self.create_textgrid(sound.duration, syllables, surface_tones)

        return {
            'f0_contour': f0_contour,
            'syllable_tones': syllable_tones,
            'surface_tones': surface_tones,
            'textgrid': textgrid
        }
```

### 5.2 Deployment Considerations

**Cloud Deployment (AWS/GCP/Azure):**
```python
# Docker container with dependencies
FROM python:3.9-slim

# Install system dependencies (for Parselmouth)
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install praat-parselmouth==0.5.0 \
                librosa==0.11.0 \
                tensorflow==2.15.0 \
                flask==3.0.0

# Copy application code
COPY . /app
WORKDIR /app

# Run API server
CMD ["python", "api.py"]
```

**Edge Deployment (Mobile/Embedded):**
```python
# Use ONNX Runtime for optimized inference
import onnxruntime as ort

# Convert TensorFlow model to ONNX
# tf2onnx.convert.from_keras(model, output_path='model.onnx')

# Load for inference
session = ort.InferenceSession('model.onnx')

def predict_tone_edge(audio_features):
    """Optimized inference for edge devices."""
    input_name = session.get_inputs()[0].name
    result = session.run(None, {input_name: audio_features})
    return result[0]
```

---

## 6. Future-Proofing Recommendations

### 6.1 Technology Trends (2024-2026)

**Current State:**
1. **Self-supervised learning** (PESTO) reducing need for labeled data
2. **Transformer architectures** replacing RNNs for sequence modeling
3. **Multi-modal learning** (audio + text) improving accuracy
4. **On-device inference** (TFLite, ONNX) enabling mobile apps

**Recommendations:**
- **Invest in:** Self-supervised pre-training (PESTO, Wav2Vec2)
- **Monitor:** Transformer-based tone models (attention mechanisms)
- **Prepare for:** Multi-modal architectures (joint audio-text)
- **Optimize for:** Mobile/edge deployment (quantization, pruning)

### 6.2 Benchmark Datasets

**Recommended Datasets for Training:**

1. **AISHELL-1** (Mandarin)
   - 170+ hours, 400 speakers
   - Open-source, Apache 2.0
   - Best for general Mandarin ASR + tone analysis

2. **THCHS-30** (Mandarin)
   - 30 hours, 50 speakers
   - Free, open-source
   - Good for smaller-scale experiments

3. **AISHELL-3** (Mandarin)
   - >98% tone transcription accuracy
   - Multi-speaker TTS corpus
   - Best for tone-specific research

**Evaluation Protocol:**
```python
# Standard train/dev/test split
# - Train: 80% (stratified by speaker + tone)
# - Dev: 10% (hyperparameter tuning)
# - Test: 10% (final evaluation, held-out speakers)

from sklearn.model_selection import train_test_split

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

X_dev, X_test, y_dev, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.5,
    stratify=y_temp,
    random_state=42
)
```

---

## 7. Cost-Benefit Analysis

### 7.1 Development Costs (USD, Estimated)

| Approach | Development Time | Compute Cost | Maintenance | Total (Year 1) |
|----------|------------------|--------------|-------------|----------------|
| **Rule-based** | 2 days | $0 | Low | $1,000 |
| **GMM/HMM** | 1 week | $50 | Low | $5,000 |
| **CNN** | 2 weeks | $500 (GPU) | Medium | $10,000 |
| **CNN-LSTM-Attention** | 1 month | $2,000 (GPU) | High | $20,000 |
| **Parselmouth Only** | 3 days | $0 | Very Low | $2,000 |

**Notes:**
- Assumes developer salary $100/hour
- GPU costs assume AWS p3.2xlarge ($3/hour)
- Maintenance includes monitoring, retraining, bug fixes

### 7.2 Performance vs. Cost

**Best ROI Options:**

1. **Prototyping:** librosa + GMM ($2,000, 85% accuracy)
2. **Production (accuracy critical):** Parselmouth + CNN ($12,000, 88% accuracy)
3. **Production (speed critical):** PESTO + lightweight CNN ($15,000, 87% accuracy)
4. **Research (state-of-the-art):** Parselmouth + CNN-LSTM ($22,000, 90%+ accuracy)

---

## 8. Final Recommendations

### 8.1 For CJK Tone Analysis Projects

**Tier 1: Core Tools (Must-Have)**
- ✅ **Parselmouth** - Pitch extraction + TextGrid (zero dependencies, Praat accuracy)
- ✅ **librosa** - Backup for pure Python environments
- ✅ **Rule-based sandhi** - 88%+ accuracy baseline, no training needed

**Tier 2: Enhanced Accuracy (Recommended)**
- ✅ **Pre-trained CNN** - 87-88% tone classification
- ✅ **CNN sandhi verification** - 97%+ accuracy with rules
- ✅ **SPPAS / Montreal Forced Aligner** - Auto-segmentation

**Tier 3: State-of-the-Art (Research)**
- ⭐ **CNN-LSTM-Attention** - 90%+ accuracy
- ⭐ **CREPE** - Highest pitch accuracy (if GPU available)
- ⭐ **RNN sequence models** - Context-aware tone sandhi

### 8.2 Implementation Roadmap

**Week 1-2: Foundation**
- Set up Parselmouth for pitch extraction
- Implement rule-based tone sandhi detector
- Create baseline evaluation (accuracy metrics)

**Week 3-4: Enhancement**
- Train CNN tone classifier on AISHELL-1
- Add data augmentation pipeline
- Implement speaker normalization

**Week 5-6: Optimization**
- Add CNN verification for sandhi detection
- Tune hyperparameters on dev set
- Deploy batch processing pipeline

**Week 7-8: Production**
- Optimize for inference speed
- Add API endpoints (REST/gRPC)
- Deploy to cloud (Docker container)

**Week 9+: Iteration**
- Monitor production accuracy
- Collect edge cases for retraining
- Explore state-of-the-art methods (CNN-LSTM-Attention)

---

## 9. Summary Decision Matrix

### 9.1 Quick Reference Guide

**Choose Parselmouth if:**
- ✅ Research-grade accuracy required
- ✅ TextGrid integration needed
- ✅ Publishing in phonetics journals
- ✅ Praat compatibility important

**Choose librosa if:**
- ✅ Pure Python environment required
- ✅ Docker containers without system dependencies
- ✅ Prototyping / experimentation phase
- ✅ Integration with music/audio pipelines

**Choose CREPE if:**
- ✅ GPU available
- ✅ Highest pitch accuracy needed
- ✅ Real-time processing with GPU
- ✅ Large-scale batch processing

**Choose PESTO if:**
- ✅ Real-time applications (<10ms latency)
- ✅ Mobile/edge deployment
- ✅ Self-supervised learning preferred
- ✅ Minimal model size (<1 MB)

### 9.2 Algorithm Selection

**Choose CNN if:**
- ✅ 1000-10000 training samples available
- ✅ End-to-end learning preferred
- ✅ Fast inference required
- ✅ 87-88% accuracy sufficient

**Choose CNN-LSTM-Attention if:**
- ✅ 10000+ training samples available
- ✅ State-of-the-art accuracy needed (90%+)
- ✅ GPU for training available
- ✅ Research publication target

**Choose Rule-based + CNN if:**
- ✅ Tone sandhi detection
- ✅ High precision required (97%+)
- ✅ Interpretability important
- ✅ Domain knowledge available

---

## 10. Conclusion

**Recommended Default Stack for Mandarin Tone Analysis:**

```
┌─────────────────────────────────────────┐
│  COMPLETE TONE ANALYSIS SYSTEM          │
├─────────────────────────────────────────┤
│  Pitch Extraction:  Parselmouth         │  ⭐⭐⭐⭐⭐
│  Tone Classification:  CNN (pre-trained)│  ⭐⭐⭐⭐
│  Tone Sandhi:  Rule-based + CNN         │  ⭐⭐⭐⭐⭐
│  TextGrid:  Parselmouth                 │  ⭐⭐⭐⭐⭐
│  Batch Processing:  Multiprocessing     │  ⭐⭐⭐⭐
└─────────────────────────────────────────┘

Overall: ⭐⭐⭐⭐⭐ Excellent
Cost: $12,000 (Year 1)
Accuracy: 87-88% (tone), 97%+ (sandhi)
Speed: Fast (2-3s per file)
Maintenance: Low
```

**This stack provides:**
- ✅ Production-ready accuracy
- ✅ Reasonable development cost
- ✅ Low maintenance burden
- ✅ Scalable to millions of files
- ✅ Cross-platform compatibility

**Start here, then optimize based on your specific requirements.**

---

## Sources

All sources cited in individual deep-dive documents (01-05) apply to this comparative analysis. Key papers include:

- [Comparative Evaluation of Acoustic Feature Extraction Tools (2025)](https://arxiv.org/html/2506.01129v1)
- [Parselmouth: A Python interface to Praat](https://www.sciencedirect.com/science/article/abs/pii/S0095447017301389)
- [CREPE: A Convolutional Representation for Pitch Estimation](https://arxiv.org/abs/1802.06182)
- [PESTO: Pitch Estimation with Self-Supervised Training](https://transactions.ismir.net/articles/251/)
- [Machine Learning for Mandarin Tone Recognition (2024-2025)](https://www.preprints.org/manuscript/202510.2478/v1)
- [ToneNet: CNN Model of Tone Classification](https://www.researchgate.net/publication/335829403_ToneNet_A_CNN_Model_of_Tone_Classification_of_Mandarin_Chinese)
- [Generation of Voice Signal Tone Sandhi Based on CNN](https://dl.acm.org/doi/10.1145/3545569)
- [AISHELL-1: Open-Source Mandarin Speech Corpus](https://arxiv.org/pdf/1709.05522)
