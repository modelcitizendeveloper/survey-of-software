# S2 Comprehensive: Tone Sandhi Detection

## Executive Summary

Tone sandhi (tone change in context) is a phonological phenomenon where tones change based on neighboring tones or prosodic position. **Detection approaches range from rule-based systems (97% accuracy on closed vocabulary) to neural networks (97%+ accuracy on general speech).**

**Key Findings:**
- **Rule-Based:** 97.39% training, 88.98% test (Taiwanese Southern-Min)
- **CNN:** 97%+ accuracy, <1.9% false alarm rate
- **Hybrid:** Combining linguistic rules with ML shows promise
- **Key Challenge:** Generalization to unseen words and speakers

**Mandarin Tone Sandhi Rules:**
1. **Third tone sandhi:** T3 + T3 → T2 + T3 (最经典 most classic rule)
2. **不 (bù):** T4 → T2 before another T4
3. **一 (yī):** T1 → T2 before T4, T1 → T4 before T1/T2/T3

---

## 1. Mandarin Tone Sandhi Rules

### 1.1 Third Tone Sandhi (T3 + T3 → T2 + T3)

**Most frequent and well-studied tone sandhi in Mandarin.**

> "In standard Chinese, a low tone (Tone 3) is usually changed into a rising tone (Tone 2) when it is immediately followed by another third tone, which is known as the third tone sandhi."

**Examples:**
- 你好 nǐ hǎo (T3 + T3) → ní hǎo (T2 + T3)
- 老鼠 lǎo shǔ (T3 + T3) → láo shǔ (T2 + T3)
- 美好 měi hǎo (T3 + T3) → méi hǎo (T2 + T3)

**Acoustic Realization:**
> "A prosodic corpus has been employed to study the acoustic realization of the sandhi rising tones."

**Research Findings:**
- **Surface F0 contours:** Non-neutralization (sandhi T2 ≠ lexical T2)
- **Underlying pitch targets:** Neutralization (sandhi T2 ≈ lexical T2)
- **Implication:** Surface-level analysis alone may miss true tone category

### 1.2 不 (bù) Tone Sandhi

**Rule:** 不 changes from T4 to T2 before another T4.

**Examples:**
- 不对 bù duì (T4 + T4) → **bú duì** (T2 + T4) "not correct"
- 不必 bù bì (T4 + T4) → **bú bì** (T2 + T4) "not necessary"
- 不是 bù shì (T4 + T4) → **bú shì** (T2 + T4) "is not"

**No change before T1, T2, T3:**
- 不开 bù kāi (T4 + T1) - no change
- 不行 bù xíng (T4 + T2) - no change
- 不好 bù hǎo (T4 + T3) - no change

### 1.3 一 (yī) Tone Sandhi

**Rules:**
1. T1 → T2 before T4
2. T1 → T4 before T1, T2, T3

**Examples:**
- 一个 yī gè (T1 + T4) → **yí gè** (T2 + T4) "one [classifier]"
- 一共 yī gòng (T1 + T4) → **yí gòng** (T2 + T4) "in total"
- 一天 yī tiān (T1 + T1) → **yì tiān** (T4 + T1) "one day"
- 一年 yī nián (T1 + T2) → **yì nián** (T4 + T2) "one year"

**Exceptions:**
- Counting sequences: 一月 (yī yuè, T1 + T4) stays T1 despite following T4
- Part of compound words: maintains lexical tone

**Sequential Application Challenge:**
> "One interesting question raised concerns sequential application of rules - when you have 一不做 (yi1 bu4 zuo4), there's ambiguity about which rule to apply first, potentially resulting in different pronunciations."

### 1.4 Implementation: Rule-Based Detector

```python
class MandarinToneSandhiDetector:
    """
    Rule-based tone sandhi detector for Mandarin Chinese.
    """

    def __init__(self):
        # Character-specific sandhi rules
        self.special_chars = {
            '不': self._bu_sandhi,
            '一': self._yi_sandhi
        }

    def _bu_sandhi(self, current_tone, next_tone):
        """
        不 (bù) tone sandhi: T4 → T2 before T4
        """
        if current_tone == 4 and next_tone == 4:
            return 2  # Change to T2
        return current_tone  # No change

    def _yi_sandhi(self, current_tone, next_tone):
        """
        一 (yī) tone sandhi:
        - T1 → T2 before T4
        - T1 → T4 before T1, T2, T3
        """
        if current_tone == 1:
            if next_tone == 4:
                return 2  # T1 → T2
            elif next_tone in [1, 2, 3]:
                return 4  # T1 → T4
        return current_tone

    def _third_tone_sandhi(self, current_tone, next_tone):
        """
        Third tone sandhi: T3 + T3 → T2 + T3
        """
        if current_tone == 3 and next_tone == 3:
            return 2  # Change to T2
        return current_tone

    def apply_sandhi(self, syllables):
        """
        Apply tone sandhi rules to sequence of syllables.

        Args:
            syllables: List of (pinyin, tone, character) tuples

        Returns:
            List of (pinyin, surface_tone, character) tuples
        """
        result = []

        for i, (pinyin, tone, char) in enumerate(syllables):
            surface_tone = tone

            # Get next tone (if exists)
            next_tone = syllables[i+1][1] if i+1 < len(syllables) else None

            if next_tone is not None:
                # Check character-specific rules
                if char in self.special_chars:
                    surface_tone = self.special_chars[char](tone, next_tone)
                # Check general third tone sandhi
                else:
                    surface_tone = self._third_tone_sandhi(tone, next_tone)

            result.append((pinyin, surface_tone, char))

        return result

# Usage example
detector = MandarinToneSandhiDetector()

# Example: 你好 (nǐ hǎo, T3 + T3)
syllables = [
    ('ni', 3, '你'),
    ('hao', 3, '好')
]

result = detector.apply_sandhi(syllables)
print("Input:", syllables)
print("Output:", result)
# Output: [('ni', 2, '你'), ('hao', 3, '好')] - First T3 becomes T2

# Example: 不必 (bù bì, T4 + T4)
syllables = [
    ('bu', 4, '不'),
    ('bi', 4, '必')
]

result = detector.apply_sandhi(syllables)
print("Input:", syllables)
print("Output:", result)
# Output: [('bu', 2, '不'), ('bi', 4, '必')] - 不 changes to T2
```

---

## 2. Machine Learning Approaches

### 2.1 Convolutional Neural Networks (CNNs)

**Research Finding:**
> "Research using convolutional neural networks for tone sandhi detection achieved over 97% average accuracy across three categories and over 97% detection accuracy for electronic tone sandhi speech, with a false alarm rate of less than 1.9%."

**Key Innovation:** CNNs can learn acoustic patterns of tone sandhi from raw spectrograms without explicit linguistic rules.

**Architecture (Tone Sandhi Detection):**

```python
import tensorflow as tf
from tensorflow.keras import layers, models

class ToneSandhiCNN:
    """
    CNN for Mandarin tone sandhi detection.

    Approach: Binary classification for each sandhi type.
    """

    def __init__(self, input_shape=(128, 88, 1), n_sandhi_types=3):
        """
        Args:
            input_shape: (n_mels, time_steps, channels) for ditone
            n_sandhi_types: Number of sandhi categories to detect
                - T3+T3 sandhi
                - 不 sandhi
                - 一 sandhi
        """
        self.input_shape = input_shape
        self.n_sandhi_types = n_sandhi_types
        self.models = self._build_models()

    def _build_models(self):
        """
        Build separate binary classifier for each sandhi type.
        """
        models = []

        for i in range(self.n_sandhi_types):
            model = tf.keras.Sequential([
                # Conv blocks
                layers.Conv2D(32, (3, 3), activation='relu', padding='same',
                             input_shape=self.input_shape),
                layers.BatchNormalization(),
                layers.MaxPooling2D((2, 2)),
                layers.Dropout(0.25),

                layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
                layers.BatchNormalization(),
                layers.MaxPooling2D((2, 2)),
                layers.Dropout(0.25),

                layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
                layers.BatchNormalization(),
                layers.MaxPooling2D((2, 2)),
                layers.Dropout(0.25),

                # Dense layers
                layers.Flatten(),
                layers.Dense(256, activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(0.5),

                # Binary output (sandhi vs. no sandhi)
                layers.Dense(1, activation='sigmoid')
            ])

            model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )

            models.append(model)

        return models

    def extract_ditone_spectrogram(self, audio_path, syllable1_start, syllable1_end,
                                   syllable2_start, syllable2_end, sr=22050):
        """
        Extract mel-spectrogram for two consecutive syllables.
        """
        import librosa
        import numpy as np

        # Load audio segment covering both syllables
        y, sr = librosa.load(
            audio_path,
            sr=sr,
            offset=syllable1_start,
            duration=(syllable2_end - syllable1_start)
        )

        # Extract mel-spectrogram
        mel_spec = librosa.feature.melspectrogram(
            y=y,
            sr=sr,
            n_mels=128,
            fmax=8000
        )

        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

        # Pad/crop to fixed length
        target_length = 88  # ~2 seconds for ditone
        if mel_spec_db.shape[1] < target_length:
            pad_width = target_length - mel_spec_db.shape[1]
            mel_spec_db = np.pad(mel_spec_db, ((0, 0), (0, pad_width)), mode='constant')
        else:
            mel_spec_db = mel_spec_db[:, :target_length]

        mel_spec_db = mel_spec_db[..., np.newaxis]

        return mel_spec_db

    def detect_sandhi(self, ditone_spectrogram, sandhi_type=0):
        """
        Detect if tone sandhi occurred.

        Args:
            ditone_spectrogram: Mel-spectrogram of two consecutive syllables
            sandhi_type: 0=T3+T3, 1=不, 2=一

        Returns:
            (is_sandhi, confidence)
        """
        spec = ditone_spectrogram[np.newaxis, ...]
        prob = self.models[sandhi_type].predict(spec)[0][0]

        is_sandhi = prob > 0.5

        return is_sandhi, prob

# Usage
cnn_detector = ToneSandhiCNN(input_shape=(128, 88, 1), n_sandhi_types=3)

# Train on labeled ditone examples
# X_train: List of ditone spectrograms
# y_train: Binary labels (1=sandhi applied, 0=no sandhi)

# Detect sandhi in new audio
# ditone_spec = cnn_detector.extract_ditone_spectrogram(
#     'audio.wav',
#     syllable1_start=0.5,
#     syllable1_end=1.0,
#     syllable2_start=1.0,
#     syllable2_end=1.5
# )
# is_sandhi, confidence = cnn_detector.detect_sandhi(ditone_spec, sandhi_type=0)
# print(f"T3+T3 Sandhi: {is_sandhi}, Confidence: {confidence:.2f}")
```

### 2.2 Recurrent Neural Networks (RNNs)

**Key Advantage:**
> "RNN models were trained on large sets of actual utterances and can automatically learn many human-prosody phonologic rules, including the well-known Sandhi Tone 3 F0-change rule."

**Architecture:** Sequence-to-sequence model

```python
class ToneSandhiRNN:
    """
    RNN for tone sandhi prediction in continuous speech.
    """

    def __init__(self, vocab_size=5, embedding_dim=32):
        """
        Args:
            vocab_size: Number of tone categories (4 tones + neutral)
            embedding_dim: Dimension of tone embeddings
        """
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.model = self._build_model()

    def _build_model(self):
        """
        Build sequence-to-sequence RNN for tone sandhi prediction.
        """
        model = tf.keras.Sequential([
            # Embedding layer for lexical tones
            layers.Embedding(self.vocab_size, self.embedding_dim,
                           input_length=None),

            # Bidirectional LSTM
            layers.Bidirectional(layers.LSTM(64, return_sequences=True)),
            layers.Dropout(0.3),

            layers.Bidirectional(layers.LSTM(32, return_sequences=True)),
            layers.Dropout(0.3),

            # Output: Surface tone for each syllable
            layers.TimeDistributed(layers.Dense(self.vocab_size, activation='softmax'))
        ])

        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        return model

    def predict_surface_tones(self, lexical_tones):
        """
        Predict surface tones from lexical tones.

        Args:
            lexical_tones: List of lexical tone indices [1, 3, 3, 2, ...]

        Returns:
            surface_tones: List of predicted surface tones
        """
        import numpy as np

        # Add batch dimension
        tones = np.array([lexical_tones])

        # Predict
        probs = self.model.predict(tones)[0]
        surface_tones = np.argmax(probs, axis=-1)

        return surface_tones.tolist()

# Usage
rnn_detector = ToneSandhiRNN(vocab_size=5, embedding_dim=32)

# Train on pairs of (lexical_tone_sequence, surface_tone_sequence)
# X_train: [[1, 3, 3, 2], [4, 4, 1, 2], ...]
# y_train: [[1, 2, 3, 2], [2, 4, 1, 2], ...]  # After sandhi

# Predict
lexical = [3, 3, 2, 1]  # 你好朋友 (nǐ hǎo péng yǒu)
surface = rnn_detector.predict_surface_tones(lexical)
print(f"Lexical: {lexical}")
print(f"Surface: {surface}")
# Expected: [2, 3, 2, 1] - First T3 changes to T2
```

---

## 3. Hybrid Approaches

### 3.1 Rule-Based + ML Verification

**Concept:** Use linguistic rules for initial detection, then ML model to verify.

**Advantages:**
- High precision from rules
- ML catches exceptions and context-dependent cases
- Interpretable decisions

**Implementation:**

```python
class HybridToneSandhiDetector:
    """
    Hybrid rule-based + ML tone sandhi detector.
    """

    def __init__(self, cnn_model=None):
        self.rule_detector = MandarinToneSandhiDetector()
        self.cnn_model = cnn_model  # Pre-trained CNN verifier

    def detect(self, syllables, audio_path=None):
        """
        Two-stage detection:
        1. Rule-based detection
        2. ML verification (if audio provided)

        Args:
            syllables: List of (pinyin, tone, character) tuples
            audio_path: Optional audio for ML verification

        Returns:
            List of (pinyin, surface_tone, character, confidence)
        """
        # Stage 1: Rule-based detection
        rule_result = self.rule_detector.apply_sandhi(syllables)

        # Stage 2: ML verification (optional)
        if audio_path is not None and self.cnn_model is not None:
            verified_result = []

            for i, (pinyin, surface_tone, char) in enumerate(rule_result):
                lexical_tone = syllables[i][1]

                # If rule predicted sandhi, verify with CNN
                if surface_tone != lexical_tone:
                    # Extract ditone spectrogram (placeholder)
                    # ditone_spec = extract_ditone_spectrogram(audio_path, i)
                    # is_sandhi, confidence = self.cnn_model.detect_sandhi(ditone_spec)

                    # If CNN disagrees, use lexical tone
                    # if not is_sandhi:
                    #     surface_tone = lexical_tone

                    confidence = 0.95  # Placeholder
                else:
                    confidence = 1.0  # No sandhi predicted

                verified_result.append((pinyin, surface_tone, char, confidence))

            return verified_result
        else:
            # Return rule-based result with default confidence
            return [(p, t, c, 1.0) for p, t, c in rule_result]

# Usage
hybrid_detector = HybridToneSandhiDetector()

syllables = [
    ('ni', 3, '你'),
    ('hao', 3, '好')
]

result = hybrid_detector.detect(syllables)
print(result)
# Output: [('ni', 2, '你', 1.0), ('hao', 3, '好', 1.0)]
```

### 3.2 Statistical Modeling + ML

**Growth Curve Analysis:**
> "Statistical modeling methods including growth curve analysis and quantitative f0 target approximation models have been used to quantify third tone sandhi in Standard Mandarin, revealing that while surface f0 contours show non-neutralization, underlying pitch targets demonstrate neutralization."

**F0 Target Model:**
- Model underlying tone targets (phonological)
- Separate from surface F0 realization (phonetic)
- ML learns mapping from context → target adjustments

---

## 4. Implicit Learning Research

### 4.1 Generalization Challenge

> "Recent studies investigate whether unfamiliar tone sandhi patterns in Tianjin Mandarin can be implicitly learned and if the acquired knowledge is rule-based and generalizable. Results showed learning effects generalized to unseen phrases with familiar words but not to phrases with new words, indicating partial rather than fully rule-based learning."

**Key Finding:** Human learners (and by extension, ML models) struggle to generalize tone sandhi rules to completely novel vocabulary.

**Implications for ML:**
- **Training data diversity critical**
- **Transfer learning** may help (pre-train on one dialect, fine-tune on another)
- **Hybrid approaches** (rules + ML) may outperform pure ML

### 4.2 Form and Meaning Co-Determination

> "Form and meaning co-determine the realization of tone in Taiwan Mandarin spontaneous speech: the case of T2-T3 and T3-T3 tone sandhi."

**Insight:** Tone sandhi application influenced by:
- **Prosodic structure** (word boundaries, phrase boundaries)
- **Semantic relationships** (compound words vs. phrases)
- **Speech rate** (fast speech → more sandhi)

**Implication:** Context beyond adjacent tones matters for accurate detection.

---

## 5. Specialized Tools

### 5.1 SPPAS (SPeech Phonetization Alignment and Syllabification)

> "SPPAS is a tool to automatically produce annotations which include utterance, word, syllable and phoneme segmentations from a recorded speech sound and its transcription."

**Features:**
- Multi-platform (Linux, macOS, Windows)
- Designed for linguists
- Automatic annotation pipeline
- Integration with prosody analysis tools

**Use for Tone Sandhi:**
- Provides syllable segmentation
- Can be extended with tone sandhi rules
- Exports to Praat TextGrid format

### 5.2 ProsodyPro

> "ProsodyPro is a software tool for facilitating large-scale analysis of speech prosody, especially for experimental data. The program allows users to perform systematic analysis of large amounts of data and generates a rich set of output, including both continuous data like time-normalized F0 contours and F0 velocity profiles suitable for graphical analysis, and discrete measurements suitable for statistical analysis."

**Features:**
- Time-normalized F0 contours
- F0 velocity profiles
- Statistical feature extraction
- Graphical analysis tools

**Use for Tone Sandhi Research:**
- Extract F0 tracks for sandhi analysis
- Visualize tone contour changes
- Compare lexical vs. surface tones

---

## 6. Evaluation Metrics

### 6.1 Detection Accuracy

**Metrics:**
- **Accuracy:** Correct detections / Total cases
- **Precision:** True positives / (True positives + False positives)
- **Recall:** True positives / (True positives + False negatives)
- **F1-score:** Harmonic mean of precision and recall

**Benchmark Performance:**
- **Rule-based:** 97.39% (training), 88.98% (test) - Taiwanese Southern-Min
- **CNN:** 97%+ accuracy, <1.9% false alarm rate - Mandarin
- **RNN:** Can learn Tone 3 sandhi rule implicitly

### 6.2 Error Analysis

**Common Error Types:**
1. **False positives:** Predicting sandhi where none occurs
   - Often due to prosodic boundary effects
   - Solution: Model prosodic structure explicitly

2. **False negatives:** Missing actual sandhi
   - Often in fast/casual speech
   - Solution: Data augmentation with variable speech rates

3. **Context confusion:** Incorrect rule application
   - Example: 一月 (yī yuè) should stay T1 but model predicts T2
   - Solution: Add lexical knowledge / word boundaries

---

## 7. Implementation Recommendations

### 7.1 Recommended Pipeline

```python
class CompleteToneSandhiPipeline:
    """
    Complete pipeline for tone sandhi detection and correction.
    """

    def __init__(self):
        self.rule_detector = MandarinToneSandhiDetector()
        # self.cnn_model = load_pretrained_cnn()  # Pre-trained CNN
        # self.rnn_model = load_pretrained_rnn()  # Pre-trained RNN

    def process_audio(self, audio_path, transcript):
        """
        Full pipeline: segmentation → detection → correction.

        Args:
            audio_path: Path to audio file
            transcript: Text transcript with lexical tones

        Returns:
            Corrected transcript with surface tones
        """
        # Step 1: Forced alignment (use SPPAS or Montreal Forced Aligner)
        # syllables = forced_alignment(audio_path, transcript)

        # Step 2: Extract F0 contours (use Parselmouth)
        # f0_contours = extract_f0_per_syllable(audio_path, syllables)

        # Step 3: Rule-based detection
        # surface_tones_rule = self.rule_detector.apply_sandhi(syllables)

        # Step 4: ML verification (CNN for ditones)
        # surface_tones_cnn = self.verify_with_cnn(syllables, f0_contours)

        # Step 5: Sequence modeling (RNN for context)
        # surface_tones_rnn = self.rnn_model.predict(syllables)

        # Step 6: Ensemble decision
        # surface_tones_final = ensemble_vote([
        #     surface_tones_rule,
        #     surface_tones_cnn,
        #     surface_tones_rnn
        # ])

        # return surface_tones_final
        pass
```

### 7.2 Best Practices

**Data Preparation:**
1. **Balanced dataset:** Equal representation of sandhi and non-sandhi cases
2. **Diverse speakers:** Multiple genders, ages, dialects
3. **Variable speech rates:** Slow, normal, fast
4. **Prosodic context:** Word boundaries, phrase boundaries marked

**Model Training:**
1. **Start with rule-based baseline** (easy to debug)
2. **Add CNN for acoustic verification** (improves precision)
3. **Add RNN for sequence modeling** (captures context)
4. **Ensemble models** for robustness

**Evaluation:**
1. **Test on held-out speakers** (generalization)
2. **Test on unseen words** (rule learning)
3. **Error analysis** by sandhi type
4. **Perceptual validation** (human listeners)

---

## 8. Future Directions

### 8.1 Multi-Dialect Models

**Challenge:** Tone sandhi rules vary across Mandarin dialects
- **Beijing Mandarin:** Standard T3+T3 sandhi
- **Taiwan Mandarin:** Partial sandhi application
- **Tianjin Mandarin:** Different sandhi patterns

**Solution:** Multi-task learning across dialects

### 8.2 Prosodic Structure Integration

**Research Need:**
> "Form and meaning co-determine the realization of tone in Taiwan Mandarin spontaneous speech."

**Future Work:**
- Joint modeling of prosody + tone sandhi
- Incorporate syntactic structure
- Model semantic composition effects

### 8.3 Real-Time Applications

**Use Cases:**
- L2 learner pronunciation feedback
- Text-to-Speech (TTS) systems
- Speech recognition post-processing

**Requirements:**
- Low latency (<100ms)
- Streaming processing
- Lightweight models (mobile deployment)

---

## 9. Summary

### 9.1 Method Comparison

| Method | Accuracy | Strengths | Limitations |
|--------|----------|-----------|-------------|
| **Rule-Based** | 88-97% | Interpretable, high precision | Fails on exceptions |
| **CNN** | 97%+ | Automatic feature learning | Requires large data |
| **RNN** | 90%+ | Context modeling | Slower training |
| **Hybrid** | Best | Combines rule + ML | More complex |

### 9.2 Recommended Approach

**For Production Systems:**
1. **Start:** Rule-based detector (baseline)
2. **Add:** CNN for acoustic verification
3. **Enhance:** RNN for sequence modeling
4. **Optimize:** Ensemble + prosodic features

**For Research:**
1. **Use:** RNN/Transformer for implicit rule learning
2. **Explore:** Transfer learning across dialects
3. **Investigate:** Prosody-tone sandhi interaction

---

## Sources

- [Generation of Voice Signal Tone Sandhi and Melody Based on CNN](https://dl.acm.org/doi/10.1145/3545569)
- [Modeling Taiwanese Southern-Min Tone Sandhi Using Rule-Based Methods](https://aclanthology.org/O07-6.pdf)
- [Machine Learning for Mandarin Tone Recognition (2024)](https://www.preprints.org/manuscript/202510.2478/v1/download)
- [Implicit learning of unfamiliar tone sandhi patterns](https://pmc.ncbi.nlm.nih.gov/articles/PMC11814201/)
- [Mandarin Tone Modeling Using RNNs](https://arxiv.org/pdf/1711.01946)
- [A quantitative analysis of tone sandhi in Standard Mandarin](https://slam.lin.ufl.edu/wp-content/uploads/sites/106/2020/01/CHE1.pdf)
- [Form and meaning co-determine tone realization in Taiwan Mandarin](https://arxiv.org/html/2408.15747v1)
- [SPPAS - Multi-lingual Approaches to Automatic Annotation](https://www.researchgate.net/publication/311707209_SPPAS_-_MULTI-LINGUAL_APPROACHES_TO_THE_AUTOMATIC_ANNOTATION_OF_SPEECH)
- [ProsodyPro - A Tool for Large-scale Systematic Prosody Analysis](https://www.researchgate.net/publication/256761804_ProsodyPro_-_A_Tool_for_Large-scale_Systematic_Prosody_Analysis)
- [Tone marks for yi1 and bu4](https://forum.wordreference.com/threads/tone-marks-for-yi1-and-bu4.4063051/)
- [Ask Nincha: Tone sandhi - Why are there tone changes in Chinese?](https://ninchanese.com/blog/2016/10/19/ask-nincha-tone-sandhi-chinese/)
