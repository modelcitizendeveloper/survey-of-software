"""
scikit-learn Text Classification - Method 3: Test-First Development
Implementation driven by comprehensive test requirements.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from typing import List, Dict


class SklearnTDDClassifier:
    """TDD-driven scikit-learn classifier implementing exact test interface."""

    def __init__(self):
        """Initialize classifier to satisfy test requirements."""
        # Configure pipeline to handle test requirements
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english',
            lowercase=True,
            strip_accents='unicode'
        )

        self.classifier = LogisticRegression(
            random_state=42,
            max_iter=1000,
            class_weight='balanced'  # Handle potential class imbalance
        )

        self.pipeline = Pipeline([
            ('vectorizer', self.vectorizer),
            ('classifier', self.classifier)
        ])

        self.label_encoder = LabelEncoder()
        self._is_trained = False
        self.classes_ = None

    def is_trained(self) -> bool:
        """Check training status as required by tests."""
        return self._is_trained

    def train(self, texts: List[str], labels: List[str]) -> Dict:
        """Train classifier meeting all test validation requirements."""
        # Validate inputs as required by tests
        if len(texts) != len(labels):
            raise ValueError("Text and label lists must have same length")

        if len(texts) < 6:  # Need minimum for train/val split
            raise ValueError("Need at least 6 samples for training")

        # Check for multiple classes as required by tests
        unique_labels = set(labels)
        if len(unique_labels) < 2:
            raise ValueError("Need at least 2 different classes")

        # Prepare data
        X = np.array(texts)
        y = np.array(labels)

        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        self.classes_ = self.label_encoder.classes_

        # Create train/validation split for test requirements
        X_train, X_val, y_train, y_val = train_test_split(
            X, y_encoded,
            test_size=0.2,
            random_state=42,
            stratify=y_encoded
        )

        # Train pipeline
        self.pipeline.fit(X_train, y_train)

        # Calculate validation accuracy as required by tests
        val_predictions = self.pipeline.predict(X_val)
        validation_accuracy = accuracy_score(y_val, val_predictions)

        self._is_trained = True

        return {
            'training_samples': len(X_train),
            'validation_accuracy': validation_accuracy,
            'classes': list(self.classes_)
        }

    def predict(self, text: str) -> Dict:
        """Predict single text meeting test interface exactly."""
        if not self._is_trained:
            raise ValueError("Model must be trained before prediction")

        # Handle edge cases as required by tests
        processed_text = text if text else ""

        # Get prediction and probabilities
        prediction_encoded = self.pipeline.predict([processed_text])[0]
        probabilities = self.pipeline.predict_proba([processed_text])[0]

        # Convert back to original label
        predicted_label = self.label_encoder.inverse_transform([prediction_encoded])[0]
        confidence = float(np.max(probabilities))

        # Create probability dictionary as required by tests
        prob_dict = {}
        for label, prob in zip(self.classes_, probabilities):
            prob_dict[label] = float(prob)

        return {
            'text': text,
            'predicted_label': predicted_label,
            'confidence': confidence,
            'probabilities': prob_dict
        }

    def predict_batch(self, texts: List[str]) -> List[Dict]:
        """Batch prediction meeting test requirements."""
        return [self.predict(text) for text in texts]

    def save_model(self, filepath: str) -> None:
        """Save model with test validation requirements."""
        if not self._is_trained:
            raise ValueError("Cannot save untrained model")

        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Save model data
        model_data = {
            'pipeline': self.pipeline,
            'label_encoder': self.label_encoder,
            'classes': self.classes_
        }
        joblib.dump(model_data, filepath)

    def load_model(self, filepath: str) -> None:
        """Load model meeting test requirements."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")

        # Load model data
        model_data = joblib.load(filepath)
        self.pipeline = model_data['pipeline']
        self.label_encoder = model_data['label_encoder']
        self.classes_ = model_data['classes']

        self._is_trained = True


def create_sample_data():
    """Generate sample data for manual testing."""
    texts = [
        "I love this amazing product! Outstanding quality.",
        "Great service, highly recommend to everyone!",
        "Excellent quality and fast delivery experience.",
        "Fantastic product, exactly what I needed!",
        "Amazing quality, perfect fit and finish.",
        "Superb customer service, very helpful staff.",
        "Brilliant design, love attention to detail.",
        "Perfect solution, works flawlessly every time.",
        "Wonderful experience, will buy again soon.",
        "Outstanding performance, exceeded expectations.",

        "Terrible quality, broke after one day usage.",
        "Poor customer service, very disappointed overall.",
        "Awful product, doesn't work as advertised.",
        "Horrible experience, slow delivery and damage.",
        "Worst purchase ever, requesting immediate refund.",
        "Disappointing quality, not worth the price.",
        "Broken on arrival, terrible packaging job.",
        "Useless product, complete failure and waste.",
        "Bad experience, rude staff and poor service.",
        "Defective item, doesn't function as described.",

        "It's okay, nothing special but does job.",
        "Average product, meets basic requirements only.",
        "Standard quality, as expected for price.",
        "Decent enough, works fine for simple tasks.",
        "Fair quality, reasonable value for money.",
        "Acceptable product, gets the job done.",
        "Basic functionality, nothing remarkable here.",
        "Standard item, meets expectations for price.",
        "Ordinary quality, sufficient for general use.",
        "Regular product, does what it says."
    ]

    labels = (['positive'] * 10 + ['negative'] * 10 + ['neutral'] * 10)
    return texts, labels


if __name__ == "__main__":
    print("scikit-learn TDD Implementation Demo")
    print("=" * 45)

    # Manual demo (tests provide the real validation)
    classifier = SklearnTDDClassifier()
    texts, labels = create_sample_data()

    print(f"Training on {len(texts)} samples...")
    training_info = classifier.train(texts, labels)
    print(f"Training complete: {training_info}")

    # Test predictions
    test_cases = [
        "This is absolutely fantastic!",
        "Really disappointed with this.",
        "It's acceptable for basic use.",
        ""  # Edge case: empty string
    ]

    print("\nTest predictions:")
    for text in test_cases:
        result = classifier.predict(text)
        display_text = text if text else "(empty)"
        print(f"'{display_text}' → {result['predicted_label']} ({result['confidence']:.3f})")

    print("\n✅ TDD Implementation Complete!")
    print("(Run test_text_classifier.py for comprehensive validation)")