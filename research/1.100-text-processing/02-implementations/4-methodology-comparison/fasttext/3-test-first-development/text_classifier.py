"""
FastText Text Classification - Method 3: Test-First Development
Implementation driven by comprehensive test suite.
"""

import fasttext
import tempfile
import os
from typing import List, Dict


class FastTextTDDClassifier:
    """TDD-driven FastText classifier implementing exact test interface."""

    def __init__(self):
        self.model = None
        self.temp_dir = tempfile.mkdtemp()
        self._is_trained = False

    def is_trained(self) -> bool:
        """Check if model is trained."""
        return self._is_trained

    def train(self, texts: List[str], labels: List[str]) -> Dict:
        """Train classifier, satisfying all test requirements."""
        # Validate inputs (required by tests)
        if len(texts) != len(labels):
            raise ValueError("Text and label lists must have same length")

        if len(texts) < 3:  # Minimum for meaningful classification
            raise ValueError("Need at least 3 samples for training")

        # Create FastText training file
        train_file = os.path.join(self.temp_dir, 'train.txt')
        with open(train_file, 'w') as f:
            for text, label in zip(texts, labels):
                clean_text = text.replace('\n', ' ').replace('\r', ' ')
                f.write(f'__label__{label} {clean_text}\n')

        # Train model
        self.model = fasttext.train_supervised(
            input=train_file,
            lr=0.1,
            epoch=25,
            wordNgrams=2,
            verbose=0
        )

        self._is_trained = True

        return {
            'training_samples': len(texts),
            'classes': sorted(list(set(labels)))
        }

    def predict(self, text: str) -> Dict:
        """Predict single text, matching test expectations."""
        if not self._is_trained:
            raise ValueError("Model must be trained before prediction")

        clean_text = text.replace('\n', ' ').replace('\r', ' ') if text else ""

        predictions = self.model.predict(clean_text, k=1)
        labels, scores = predictions

        predicted_label = labels[0].replace('__label__', '') if labels else 'unknown'
        confidence = float(scores[0]) if scores else 0.0

        return {
            'text': text,
            'predicted_label': predicted_label,
            'confidence': confidence
        }

    def predict_batch(self, texts: List[str]) -> List[Dict]:
        """Batch prediction matching test interface."""
        return [self.predict(text) for text in texts]

    def save_model(self, filepath: str) -> None:
        """Save model, validating trained state."""
        if not self._is_trained:
            raise ValueError("Cannot save untrained model")

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.model.save_model(filepath)

    def load_model(self, filepath: str) -> None:
        """Load model from file."""
        self.model = fasttext.load_model(filepath)
        self._is_trained = True

    def __del__(self):
        """Cleanup temp files."""
        try:
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                import shutil
                shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass


def create_sample_data():
    """Generate sample data for manual testing."""
    texts = [
        "I love this product! Amazing quality.",
        "Great service, highly recommend!",
        "Excellent experience overall.",
        "Terrible quality, broke immediately.",
        "Poor service, very disappointed.",
        "Awful product, avoid completely.",
        "It's okay, does the job.",
        "Average quality, nothing special.",
        "Decent for the price point."
    ]
    labels = ['positive', 'positive', 'positive',
             'negative', 'negative', 'negative',
             'neutral', 'neutral', 'neutral']
    return texts, labels


if __name__ == "__main__":
    print("FastText TDD Implementation Demo")
    print("=" * 40)

    # Manual testing (tests drive the real validation)
    classifier = FastTextTDDClassifier()
    texts, labels = create_sample_data()

    print(f"Training on {len(texts)} samples...")
    training_info = classifier.train(texts, labels)
    print(f"Training complete: {training_info}")

    # Test predictions
    test_cases = [
        "This is absolutely fantastic!",
        "Really disappointed with this.",
        "It's acceptable for basic use."
    ]

    print("\nTest predictions:")
    for text in test_cases:
        result = classifier.predict(text)
        print(f"'{text}' → {result['predicted_label']} ({result['confidence']:.3f})")

    print("\n✅ TDD Implementation Complete!")
    print("(Run test_text_classifier.py for full validation)")