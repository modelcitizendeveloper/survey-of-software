# S2 Comprehensive: Tone Classification Algorithms

## Executive Summary

Tone classification has evolved from traditional statistical methods (HMM, GMM) to modern deep learning approaches (CNN, RNN). For Mandarin Chinese, **CNNs achieve 87-88% accuracy** with end-to-end learning from raw features, while **hybrid CNN-LSTM models with attention mechanisms** represent the current state-of-the-art.

**Key Findings:**
- **Traditional:** HMM/GMM (84-85% accuracy)
- **Deep Learning:** CNN (87-88%), RNN (85-90%), CNN-LSTM (90%+)
- **Feature Engineering:** Critical for traditional methods, less important for deep learning
- **Best Practices:** Speaker normalization, time-normalization, data augmentation

---

## 1. Overview of Approaches

### 1.1 Taxonomy of Methods

```
Tone Classification Methods
├── Traditional Statistical
│   ├── Hidden Markov Models (HMM)
│   ├── Gaussian Mixture Models (GMM)
│   └── Support Vector Machines (SVM)
├── Classical Machine Learning
│   ├── Random Forest
│   ├── Decision Trees
│   └── k-Nearest Neighbors
└── Deep Learning
    ├── Convolutional Neural Networks (CNN)
    ├── Recurrent Neural Networks (RNN/LSTM)
    ├── Hybrid CNN-LSTM
    └── Attention-based Transformers
```

### 1.2 Performance Comparison (Mandarin)

| Method | Accuracy | Year | Notes |
|--------|----------|------|-------|
| **GMM** | 84.55% | 2020 | Requires manual feature extraction |
| **SVM** | 85.50% | 2020 | Good with proper features |
| **BPNN** | 86.28% | 2020 | Back-propagation neural network |
| **CNN** | 87.60% | 2020 | End-to-end from MFCC/spectrogram |
| **RNN** | 88-90% | 2017 | Context modeling with LSTM |
| **CNN-LSTM** | 90%+ | 2021 | State-of-the-art hybrid |
| **MSD-HMM** | 88.80% | 2015 | Multi-space distribution HMM |

**Trend:** Deep learning approaches consistently outperform traditional statistical methods, with hybrid architectures achieving the best results.

---

## 2. Hidden Markov Models (HMM)

### 2.1 Overview

HMMs model tones as sequences of hidden states with observable F0 features. They capture temporal dynamics of tone contours.

**Key Concept:**
- **Hidden states:** Discrete tone categories (T1, T2, T3, T4)
- **Observations:** F0 features (mean, trajectory, derivatives)
- **Transitions:** Probability of tone sandhi or coarticulation

### 2.2 Architecture

```
HMM Tone Model
┌─────────────────────────────────────┐
│  State 1 (T1)  →  State 2 (T2)     │  Hidden Layer
│      ↓               ↓               │
│  F0 Features    F0 Features         │  Observable Layer
│  [f0_1, Δf0]    [f0_2, Δf0]        │
└─────────────────────────────────────┘
```

### 2.3 Feature Extraction for HMM

**LDA-MLLT Method (Linear Discriminant Analysis + Maximum Likelihood Linear Transform):**
> "For GMM-HMM based acoustic model, utilization of spliced features is often achieved using LDA-MLLT method."

**Feature Splicing:**
> "Feature splicing has greatly improved tone classification performance, yielding 5.3% absolute improvement in RNN-based models."

**Common Features:**
- F0 contour (sampled at fixed intervals)
- Δ F0 (first derivative)
- Δ² F0 (second derivative / acceleration)
- F0 from neighboring syllables (context)

### 2.4 Code Example

```python
import numpy as np
from hmmlearn import hmm

class ToneHMM:
    """
    Hidden Markov Model for Mandarin tone classification.
    """

    def __init__(self, n_tones=4, n_components=3):
        """
        Args:
            n_tones: Number of tone categories (4 for Mandarin)
            n_components: Number of hidden states per tone
        """
        self.n_tones = n_tones
        self.n_components = n_components
        self.models = []

        # Create one HMM per tone
        for i in range(n_tones):
            model = hmm.GaussianHMM(
                n_components=n_components,
                covariance_type='diag',
                n_iter=100
            )
            self.models.append(model)

    def extract_features(self, f0_contour):
        """
        Extract features: [f0, Δf0, Δ²f0]
        """
        # Normalize F0
        f0_norm = (f0_contour - np.mean(f0_contour)) / np.std(f0_contour)

        # First derivative
        delta_f0 = np.diff(f0_norm, prepend=f0_norm[0])

        # Second derivative
        delta2_f0 = np.diff(delta_f0, prepend=delta_f0[0])

        # Stack features
        features = np.column_stack([f0_norm, delta_f0, delta2_f0])

        return features

    def train(self, X_train, y_train):
        """
        Train one HMM per tone.

        Args:
            X_train: List of F0 contours
            y_train: Tone labels (0=T1, 1=T2, 2=T3, 3=T4)
        """
        for tone in range(self.n_tones):
            # Get training samples for this tone
            tone_samples = [X_train[i] for i in range(len(X_train)) if y_train[i] == tone]

            # Extract features
            tone_features = [self.extract_features(sample) for sample in tone_samples]

            # Concatenate with lengths
            lengths = [len(f) for f in tone_features]
            X_concat = np.vstack(tone_features)

            # Train HMM
            self.models[tone].fit(X_concat, lengths)

    def predict(self, f0_contour):
        """
        Classify tone using log-likelihood.
        """
        features = self.extract_features(f0_contour)

        # Compute log-likelihood for each tone
        scores = []
        for model in self.models:
            score = model.score(features)
            scores.append(score)

        # Return tone with highest likelihood
        tone = np.argmax(scores)
        return tone, scores

# Usage example
hmm_classifier = ToneHMM(n_tones=4, n_components=3)

# Training data (placeholder)
X_train = [np.random.randn(10) for _ in range(100)]  # F0 contours
y_train = np.random.randint(0, 4, 100)  # Tone labels

hmm_classifier.train(X_train, y_train)

# Predict
f0_test = np.array([0.5, 0.8, 1.2, 1.5, 1.8])  # Rising tone (T2)
tone, scores = hmm_classifier.predict(f0_test)
print(f"Predicted tone: T{tone+1}, Scores: {scores}")
```

### 2.5 Advantages & Limitations

**✅ Advantages:**
- Models temporal dynamics naturally
- Handles variable-length sequences
- Interpretable (state transitions = linguistic rules)

**❌ Limitations:**
- Requires manual feature engineering
- Assumes Markov property (limited context)
- Outperformed by deep learning methods

---

## 3. Gaussian Mixture Models (GMM)

### 3.1 Overview

GMMs model tone F0 distributions as mixtures of Gaussian components. Each tone is represented by a unique probability distribution.

**Key Concept:**
- Each tone = mixture of K Gaussians
- F0 features → probability density
- Classification = maximum likelihood

### 3.2 Architecture

```
GMM Tone Model (Tone 1)
┌────────────────────────────────┐
│  Gaussian 1   Gaussian 2   Gaussian 3  │
│   (μ₁, Σ₁)     (μ₂, Σ₂)     (μ₃, Σ₃)  │
│      π₁           π₂           π₃       │
└────────────────────────────────┘
         ↓
   F0 Features → P(X | Tone 1)
```

### 3.3 Overlapped Ditone Modeling (Cantonese)

> "Overlapped ditone modeling has been used for tone recognition in continuous Cantonese speech, incorporating contextual pitch features for GMM-based tone models."

**Ditone concept:** Model two consecutive tones jointly to capture coarticulation effects.

### 3.4 Code Example

```python
from sklearn.mixture import GaussianMixture
import numpy as np

class ToneGMM:
    """
    Gaussian Mixture Model for tone classification.
    """

    def __init__(self, n_tones=4, n_components=3):
        """
        Args:
            n_tones: Number of tone categories
            n_components: Number of Gaussian components per tone
        """
        self.n_tones = n_tones
        self.models = []

        # Create one GMM per tone
        for i in range(n_tones):
            model = GaussianMixture(
                n_components=n_components,
                covariance_type='full',
                max_iter=100,
                random_state=42
            )
            self.models.append(model)

    def extract_features(self, f0_contour):
        """
        Extract statistical features from F0 contour.
        """
        # Time-normalize to 5 points
        from scipy.interpolate import interp1d
        time_orig = np.linspace(0, 1, len(f0_contour))
        time_new = np.linspace(0, 1, 5)
        f = interp1d(time_orig, f0_contour, kind='cubic')
        f0_5points = f(time_new)

        # Z-score normalization
        f0_norm = (f0_5points - np.mean(f0_5points)) / np.std(f0_5points)

        # Features: [f0_1, f0_2, f0_3, f0_4, f0_5, mean, std, range]
        features = np.concatenate([
            f0_norm,
            [np.mean(f0_5points), np.std(f0_5points), np.ptp(f0_5points)]
        ])

        return features

    def train(self, X_train, y_train):
        """
        Train one GMM per tone.
        """
        for tone in range(self.n_tones):
            # Get training samples for this tone
            tone_samples = [X_train[i] for i in range(len(X_train)) if y_train[i] == tone]

            # Extract features
            tone_features = np.array([self.extract_features(sample) for sample in tone_samples])

            # Train GMM
            self.models[tone].fit(tone_features)

    def predict(self, f0_contour):
        """
        Classify tone using log-likelihood.
        """
        features = self.extract_features(f0_contour).reshape(1, -1)

        # Compute log-likelihood for each tone
        scores = []
        for model in self.models:
            score = model.score(features)
            scores.append(score)

        # Return tone with highest likelihood
        tone = np.argmax(scores)
        return tone, scores

# Usage
gmm_classifier = ToneGMM(n_tones=4, n_components=3)

# Train (placeholder data)
X_train = [np.random.randn(10) for _ in range(100)]
y_train = np.random.randint(0, 4, 100)
gmm_classifier.train(X_train, y_train)

# Predict
f0_test = np.array([200, 210, 220, 230, 240])  # Rising tone
tone, scores = gmm_classifier.predict(f0_test)
print(f"Predicted tone: T{tone+1}")
```

### 3.5 Advantages & Limitations

**✅ Advantages:**
- Simple, interpretable
- Fast training and inference
- Works well with limited data

**❌ Limitations:**
- Assumes fixed feature dimensionality
- Doesn't model temporal dynamics well
- Lower accuracy than deep learning

---

## 4. Convolutional Neural Networks (CNN)

### 4.1 Overview

CNNs automatically learn hierarchical features from raw spectrograms or mel-spectrograms, eliminating manual feature engineering.

**Key Innovation:**
> "CNN-based methods fully automate tone classification of syllables in Mandarin Chinese, taking raw tone data as input and achieving substantially higher accuracy compared with previous techniques based on manually edited F0."

### 4.2 ToneNet Architecture

**ToneNet** is a CNN model designed specifically for Mandarin tone classification:

**Input:** Mel-spectrogram (128 mel bins × time frames)
**Architecture:**
1. Conv2D (32 filters, 3×3) + ReLU + MaxPool
2. Conv2D (64 filters, 3×3) + ReLU + MaxPool
3. Conv2D (128 filters, 3×3) + ReLU + MaxPool
4. Flatten + Dense(256) + Dropout(0.5)
5. Dense(4) + Softmax (4 tones)

### 4.3 Code Example

```python
import tensorflow as tf
from tensorflow.keras import layers, models
import librosa
import numpy as np

class ToneCNN:
    """
    Convolutional Neural Network for Mandarin tone classification.
    """

    def __init__(self, input_shape=(128, 44, 1), n_tones=4):
        """
        Args:
            input_shape: (n_mels, time_steps, channels)
            n_tones: Number of tone categories
        """
        self.input_shape = input_shape
        self.n_tones = n_tones
        self.model = self._build_model()

    def _build_model(self):
        """
        Build ToneNet-inspired CNN architecture.
        """
        model = models.Sequential([
            # Block 1
            layers.Conv2D(32, (3, 3), activation='relu', padding='same',
                         input_shape=self.input_shape),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),

            # Block 2
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),

            # Block 3
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),

            # Dense layers
            layers.Flatten(),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),

            # Output
            layers.Dense(self.n_tones, activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        return model

    def extract_mel_spectrogram(self, audio_path, sr=22050, n_mels=128, duration=0.5):
        """
        Extract mel-spectrogram from audio file.
        """
        # Load audio
        y, sr = librosa.load(audio_path, sr=sr, duration=duration)

        # Extract mel-spectrogram
        mel_spec = librosa.feature.melspectrogram(
            y=y,
            sr=sr,
            n_mels=n_mels,
            fmax=8000
        )

        # Convert to dB scale
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

        # Pad or crop to fixed length
        target_length = 44  # ~1 second at hop_length=512
        if mel_spec_db.shape[1] < target_length:
            pad_width = target_length - mel_spec_db.shape[1]
            mel_spec_db = np.pad(mel_spec_db, ((0, 0), (0, pad_width)), mode='constant')
        else:
            mel_spec_db = mel_spec_db[:, :target_length]

        # Add channel dimension
        mel_spec_db = mel_spec_db[..., np.newaxis]

        return mel_spec_db

    def train(self, audio_files, labels, epochs=50, batch_size=32, validation_split=0.2):
        """
        Train CNN on audio files.
        """
        # Extract features
        X = np.array([self.extract_mel_spectrogram(f) for f in audio_files])
        y = np.array(labels)

        # Train
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
                tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5)
            ]
        )

        return history

    def predict(self, audio_path):
        """
        Classify tone from audio file.
        """
        mel_spec = self.extract_mel_spectrogram(audio_path)
        mel_spec = mel_spec[np.newaxis, ...]  # Add batch dimension

        probs = self.model.predict(mel_spec)[0]
        tone = np.argmax(probs)

        return tone, probs

# Usage
cnn_classifier = ToneCNN(input_shape=(128, 44, 1), n_tones=4)

# Train (placeholder)
audio_files = ['tone1_001.wav', 'tone2_001.wav', ...]  # List of audio paths
labels = [0, 1, 2, 3, ...]  # Corresponding tone labels

history = cnn_classifier.train(audio_files, labels, epochs=50)

# Predict
tone, probs = cnn_classifier.predict('test_syllable.wav')
print(f"Predicted tone: T{tone+1}, Probabilities: {probs}")
```

### 4.4 Advantages & Limitations

**✅ Advantages:**
- No manual feature engineering required
- Learns hierarchical features automatically
- State-of-the-art accuracy (87-88%)
- Handles raw spectrograms directly

**❌ Limitations:**
- Requires large training datasets (1000s of samples)
- Black-box model (less interpretable)
- GPU required for fast training

---

## 5. Recurrent Neural Networks (RNN/LSTM)

### 5.1 Overview

RNNs model sequential dependencies in F0 contours using memory cells. LSTMs (Long Short-Term Memory) avoid vanishing gradient problems.

**Key Innovation:**
> "RNN models were trained on large sets of actual utterances and can automatically learn many human-prosody phonologic rules, including the well-known Sandhi Tone 3 F0-change rule."

### 5.2 Encoder-Classifier Framework

**Architecture:**
1. **Encoder (LSTM):** Processes F0 sequence → fixed-dimensional tone embedding
2. **Classifier (Softmax):** Maps embedding → tone probabilities

```
F0 Sequence → [LSTM Encoder] → Tone Embedding → [Dense + Softmax] → Tone Class
  [f0_1, ..., f0_T]     ↓
                    h_1, h_2, ..., h_T
                         ↓
                   Last hidden state (embedding)
```

### 5.3 Code Example

```python
import tensorflow as tf
from tensorflow.keras import layers, models

class ToneLSTM:
    """
    LSTM-based tone classifier with Encoder-Classifier framework.
    """

    def __init__(self, embedding_dim=64, n_tones=4):
        self.embedding_dim = embedding_dim
        self.n_tones = n_tones
        self.model = self._build_model()

    def _build_model(self):
        """
        Build Encoder-Classifier LSTM model.
        """
        model = models.Sequential([
            # Encoder: LSTM layers
            layers.LSTM(128, return_sequences=True, input_shape=(None, 1)),
            layers.Dropout(0.3),
            layers.LSTM(64, return_sequences=False),  # Last hidden state
            layers.Dropout(0.3),

            # Embedding layer
            layers.Dense(self.embedding_dim, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),

            # Classifier
            layers.Dense(self.n_tones, activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        return model

    def prepare_sequence(self, f0_contour, normalize=True):
        """
        Prepare F0 sequence for LSTM input.
        """
        # Z-score normalization
        if normalize:
            f0_norm = (f0_contour - np.mean(f0_contour)) / (np.std(f0_contour) + 1e-8)
        else:
            f0_norm = f0_contour

        # Reshape to (time_steps, features)
        f0_seq = f0_norm.reshape(-1, 1)

        return f0_seq

    def train(self, X_train, y_train, epochs=50, batch_size=32, validation_split=0.2):
        """
        Train LSTM on F0 sequences.
        """
        # Pad sequences to same length
        from tensorflow.keras.preprocessing.sequence import pad_sequences

        # Prepare sequences
        X_sequences = [self.prepare_sequence(x) for x in X_train]

        # Pad to max length
        max_length = max([len(x) for x in X_sequences])
        X_padded = pad_sequences(X_sequences, maxlen=max_length, dtype='float32', padding='post')

        # Train
        history = self.model.fit(
            X_padded, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
            ]
        )

        return history

    def predict(self, f0_contour):
        """
        Classify tone from F0 contour.
        """
        f0_seq = self.prepare_sequence(f0_contour)
        f0_seq = f0_seq[np.newaxis, ...]  # Add batch dimension

        probs = self.model.predict(f0_seq)[0]
        tone = np.argmax(probs)

        return tone, probs

# Usage
lstm_classifier = ToneLSTM(embedding_dim=64, n_tones=4)

# Train
X_train = [np.random.randn(np.random.randint(10, 30)) for _ in range(100)]
y_train = np.random.randint(0, 4, 100)

history = lstm_classifier.train(X_train, y_train, epochs=30)

# Predict
f0_test = np.array([200, 210, 220, 230, 240, 250])
tone, probs = lstm_classifier.predict(f0_test)
print(f"Predicted tone: T{tone+1}")
```

### 5.4 Feature Splicing for Context

> "Feature splicing has greatly improved tone classification performance, yielding 5.3% absolute improvement in RNN-based models."

**Implementation:**
```python
def extract_spliced_features(f0_sequence, context_window=2):
    """
    Splice F0 features with neighboring frames for context.

    Args:
        f0_sequence: F0 values
        context_window: Number of frames to include on each side

    Returns:
        Spliced features: [f0_t-2, f0_t-1, f0_t, f0_t+1, f0_t+2]
    """
    spliced = []

    for i in range(len(f0_sequence)):
        # Extract context window
        start = max(0, i - context_window)
        end = min(len(f0_sequence), i + context_window + 1)

        context = f0_sequence[start:end]

        # Pad if at boundaries
        if len(context) < (2 * context_window + 1):
            if i < context_window:
                context = np.pad(context, (context_window - i, 0), mode='edge')
            else:
                context = np.pad(context, (0, i - len(f0_sequence) + context_window + 1), mode='edge')

        spliced.append(context)

    return np.array(spliced)
```

### 5.5 Advantages & Limitations

**✅ Advantages:**
- Models temporal dependencies naturally
- Handles variable-length sequences
- Can learn tone sandhi rules implicitly
- Good for continuous speech recognition

**❌ Limitations:**
- Requires more training data than CNNs
- Slower training (sequential processing)
- Vanishing gradient issues (mitigated by LSTM)

---

## 6. Hybrid CNN-LSTM with Attention

### 6.1 Overview

State-of-the-art architecture combining:
- **CNN:** Extracts local spectral features
- **LSTM:** Models temporal dynamics
- **Attention:** Focuses on discriminative time regions

**Performance:** 90%+ accuracy on Mandarin tone classification

### 6.2 Architecture

```
Input (Mel-Spectrogram)
    ↓
[CNN Blocks] → Local feature extraction
    ↓
[LSTM Encoder] → Temporal modeling
    ↓
[Attention Mechanism] → Weighted feature aggregation
    ↓
[Dense Classifier] → Tone prediction
```

### 6.3 Multi-Head Attention

> "Attention mechanisms are key factors in improving model performance, as they adaptively focus on the importance of different features to obtain better speech features at the discourse level."

**Benefits:**
- Focuses on critical time regions (e.g., tone onset)
- Reduces influence of noise/silence
- Improves generalization

### 6.4 Code Example (Simplified)

```python
import tensorflow as tf
from tensorflow.keras import layers, models

class ToneCNNLSTMAttention:
    """
    Hybrid CNN-LSTM with Attention for tone classification.
    """

    def __init__(self, input_shape=(128, 44, 1), n_tones=4):
        self.input_shape = input_shape
        self.n_tones = n_tones
        self.model = self._build_model()

    def _build_model(self):
        """
        Build CNN-LSTM-Attention architecture.
        """
        inputs = layers.Input(shape=self.input_shape)

        # CNN blocks for feature extraction
        x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)

        x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)

        # Reshape for LSTM
        x = layers.Permute((2, 1, 3))(x)  # (time, freq, channels)
        shape = x.shape
        x = layers.Reshape((shape[1], shape[2] * shape[3]))(x)

        # Bidirectional LSTM
        x = layers.Bidirectional(layers.LSTM(128, return_sequences=True))(x)

        # Multi-head attention
        attention_output = layers.MultiHeadAttention(
            num_heads=4,
            key_dim=32
        )(x, x)

        # Global average pooling
        x = layers.GlobalAveragePooling1D()(attention_output)

        # Dense classifier
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.5)(x)
        outputs = layers.Dense(self.n_tones, activation='softmax')(x)

        model = models.Model(inputs=inputs, outputs=outputs)

        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        return model

# Usage
hybrid_classifier = ToneCNNLSTMAttention(input_shape=(128, 44, 1), n_tones=4)
print(hybrid_classifier.model.summary())
```

### 6.5 Advantages

**✅ State-of-the-art performance (90%+ accuracy)**
**✅ Combines local and global feature learning**
**✅ Attention provides interpretability**
**✅ Robust to noise and speaker variation**

---

## 7. Feature Engineering Best Practices

### 7.1 Speaker Normalization Methods

**1. Z-score Normalization**
```python
f0_normalized = (f0 - speaker_mean) / speaker_std
```

**2. Semitone Normalization** (perceptually motivated)
```python
f0_semitones = 12 * np.log2(f0 / reference_f0)
```

**3. Tone 1-Based Normalization**
> "Studies tested normalized F0 data using tone 1-based normalization and first-order derivative from speech tokens from speakers, with the tone 1-based normalization procedure improving neural network performance to human listener-like accuracy."

```python
reference_f0 = np.mean(f0_tone1_samples)  # Speaker's tone 1 mean
f0_normalized = f0 / reference_f0
```

**Research Finding:**
> "Z-score would be hard to compute when processing data from a new speaker, and once an operational model is developed, explicit speaker normalization is not really needed, as the training process is already one of learning to handle variability."

**Recommendation:** Use z-score during training, but design model to handle unseen speakers without normalization at inference time.

### 7.2 Time Normalization

**Fixed-length representation:**
- Resample F0 contour to fixed number of points (typically 5-10)
- Preserves relative shape while normalizing duration

```python
from scipy.interpolate import interp1d

def time_normalize(f0_contour, n_points=5):
    time_orig = np.linspace(0, 1, len(f0_contour))
    time_new = np.linspace(0, 1, n_points)
    f = interp1d(time_orig, f0_contour, kind='cubic')
    return f(time_new)
```

### 7.3 Data Augmentation

**Techniques:**
1. **Pitch shifting** (±1 semitone)
2. **Time stretching** (0.9-1.1x speed)
3. **Adding noise** (SNR 20-30 dB)
4. **Vocal tract length perturbation** (VTLP)

```python
import librosa

def augment_audio(y, sr):
    # Pitch shift
    y_pitch = librosa.effects.pitch_shift(y, sr=sr, n_steps=np.random.uniform(-1, 1))

    # Time stretch
    rate = np.random.uniform(0.9, 1.1)
    y_stretch = librosa.effects.time_stretch(y, rate=rate)

    # Add noise
    noise = np.random.normal(0, 0.005, len(y))
    y_noise = y + noise

    return y_pitch, y_stretch, y_noise
```

---

## 8. Benchmark Datasets

### 8.1 THCHS-30

**Details:**
- **Size:** 30 hours, 50 speakers
- **Language:** Mandarin Chinese
- **License:** Open-source
- **Use:** ASR training and evaluation

**Citation:** THCHS-30: A Free Chinese Speech Corpus (2015)

### 8.2 AISHELL-1

**Details:**
- **Size:** 170+ hours, 400 speakers
- **Language:** Mandarin Chinese
- **License:** Apache 2.0
- **Use:** Largest open-source Mandarin ASR corpus

**Features:**
- High-quality recordings
- Diverse speakers (gender, age, dialect)
- Suitable for tone classification research

### 8.3 AISHELL-3

**Details:**
- **Tone transcription accuracy:** >98%
- **Use:** Multi-speaker TTS and tone analysis

---

## 9. Summary & Recommendations

### 9.1 Method Selection Guide

| Use Case | Recommended Method | Rationale |
|----------|-------------------|-----------|
| **Limited data** (<1000 samples) | GMM or SVM | Works well with small datasets |
| **Moderate data** (1000-10000) | CNN (ToneNet) | End-to-end learning, good accuracy |
| **Large data** (>10000) | CNN-LSTM-Attention | State-of-the-art performance |
| **Continuous speech** | RNN/LSTM | Models context and tone sandhi |
| **Real-time applications** | CNN | Fast inference |
| **Research/interpretability** | HMM or Attention | Explainable models |

### 9.2 Implementation Roadmap

**Phase 1: Baseline** (Week 1-2)
- Implement CNN classifier (ToneNet architecture)
- Train on AISHELL-1 or THCHS-30
- Target: 85-87% accuracy

**Phase 2: Optimization** (Week 3-4)
- Add data augmentation
- Tune hyperparameters
- Implement speaker normalization
- Target: 88-90% accuracy

**Phase 3: Advanced** (Week 5-6)
- Implement CNN-LSTM-Attention hybrid
- Multi-task learning (tone + tone sandhi)
- Target: 90%+ accuracy

---

## Sources

- [End-to-End Mandarin Tone Classification (2021)](https://arxiv.org/pdf/2104.05657)
- [ToneNet: CNN Model of Tone Classification](https://www.researchgate.net/publication/335829403_ToneNet_A_CNN_Model_of_Tone_Classification_of_Mandarin_Chinese)
- [Mandarin Tone Recognition Algorithm Based on Random Forest](https://www.mdpi.com/2227-7390/11/8/1879)
- [Machine Learning for Mandarin Tone Recognition (2024-2025)](https://www.preprints.org/manuscript/202510.2478/v1/download)
- [Mandarin Tone Modeling Using RNNs (2017)](https://arxiv.org/pdf/1711.01946)
- [Deep Neural Networks for Mandarin Tone Recognition](https://www.researchgate.net/publication/286240764_Deep_neural_networks_for_Mandarin_tone_recognition)
- [A Comparison of Tone Normalization Methods](https://aclanthology.org/Y18-1095.pdf)
- [Hybrid LSTM-Attention and CNN Model for Speech Recognition](https://www.mdpi.com/2076-3417/14/23/11342)
- [AISHELL-1: Open-Source Mandarin Speech Corpus](https://arxiv.org/pdf/1709.05522)
- [THCHS-30: A Free Chinese Speech Corpus](https://www.openslr.org/18/)
