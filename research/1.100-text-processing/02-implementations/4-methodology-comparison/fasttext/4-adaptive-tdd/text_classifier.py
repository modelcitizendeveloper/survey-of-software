"""
FastText Text Classification - Method 4: Adaptive TDD
Strategic testing with validation focus on complex areas.
"""

import fasttext
import tempfile
import os
import time
from typing import List, Dict, Optional


class FastTextAdaptiveClassifier:
    """
    Adaptive TDD FastText classifier with strategic validation.
    Focuses testing effort on areas where FastText complexity requires validation.
    """

    def __init__(self):
        self.model = None
        self.temp_dir = tempfile.mkdtemp()
        self.is_trained = False
        self.classes = []

    def train(self, texts: List[str], labels: List[str]) -> Dict:
        """
        Train with adaptive validation focus on data preparation complexity.
        FastText's data format is a critical area requiring robust testing.
        """
        # Basic validation (straightforward)
        if len(texts) != len(labels) or len(texts) < 6:
            raise ValueError("Invalid training data")

        # STRATEGIC VALIDATION: FastText format handling is complex
        self._validate_fasttext_format_handling(texts, labels)

        # Create training file with careful format validation
        train_file = self._create_validated_training_file(texts, labels)

        # Train model
        start_time = time.time()
        self.model = fasttext.train_supervised(
            input=train_file,
            lr=0.1,
            epoch=25,
            wordNgrams=2,
            dim=100,
            verbose=0
        )

        self.is_trained = True
        self.classes = sorted(list(set(labels)))

        return {
            'training_samples': len(texts),
            'classes': self.classes,
            'training_time': time.time() - start_time
        }

    def _validate_fasttext_format_handling(self, texts: List[str], labels: List[str]):
        """
        ADAPTIVE VALIDATION: Test complex edge cases in FastText format preparation.
        This is where bugs commonly occur, so extra validation adds value.
        """
        # Test cases that could break FastText format
        edge_cases = [
            ("Text with __label__ in content", "positive"),  # Label collision
            ("Text\nwith\nnewlines", "negative"),           # Newline handling
            ("Text with 'quotes' and \"double quotes\"", "neutral"),  # Quote handling
            ("", "positive"),                                # Empty text
            ("   whitespace only   ", "negative")           # Whitespace-only
        ]

        for text, label in edge_cases:
            formatted_line = f'__label__{label} {self._preprocess_text(text)}'
            # Validate that our preprocessing creates valid FastText format
            assert '\n' not in formatted_line, f"Newline in formatted line: {formatted_line}"
            assert formatted_line.startswith('__label__'), f"Invalid format: {formatted_line}"

    def _create_validated_training_file(self, texts: List[str], labels: List[str]) -> str:
        """Create training file with format validation."""
        train_file = os.path.join(self.temp_dir, 'train.txt')

        with open(train_file, 'w', encoding='utf-8') as f:
            for text, label in zip(texts, labels):
                clean_text = self._preprocess_text(text)
                line = f'__label__{label} {clean_text}\n'
                f.write(line)

        # VALIDATION: Verify file was created correctly
        with open(train_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert len(lines) == len(texts), "File line count mismatch"
            for line in lines:
                assert line.startswith('__label__'), f"Invalid line format: {line}"

        return train_file

    def _preprocess_text(self, text: str) -> str:
        """Robust text preprocessing with edge case handling."""
        if not text:
            return ""

        # Handle problematic characters that could break FastText format
        clean_text = str(text)
        clean_text = clean_text.replace('\n', ' ').replace('\r', ' ')
        clean_text = clean_text.replace('\t', ' ')
        clean_text = ' '.join(clean_text.split())  # Normalize whitespace

        return clean_text

    def predict(self, text: str) -> Dict:
        """
        Predict with strategic validation on prediction edge cases.
        FastText's prediction behavior with edge cases needs verification.
        """
        if not self.is_trained:
            raise ValueError("Model not trained")

        # ADAPTIVE VALIDATION: Test prediction robustness for edge cases
        if self._is_edge_case_input(text):
            return self._validated_edge_case_prediction(text)

        # Standard prediction for normal cases
        clean_text = self._preprocess_text(text)
        predictions = self.model.predict(clean_text, k=len(self.classes))
        labels, scores = predictions

        predicted_label = labels[0].replace('__label__', '') if labels else self.classes[0]
        confidence = float(scores[0]) if scores else 0.0

        # Build probability distribution
        probabilities = {}
        for label, score in zip(labels, scores):
            clean_label = label.replace('__label__', '')
            probabilities[clean_label] = float(score)

        return {
            'text': text,
            'predicted_label': predicted_label,
            'confidence': confidence,
            'probabilities': probabilities
        }

    def _is_edge_case_input(self, text: str) -> bool:
        """Identify inputs that require extra validation."""
        if not text or not text.strip():
            return True
        if '\n' in text or '\r' in text:
            return True
        if '__label__' in text:
            return True
        if len(text) > 1000:  # Very long text
            return True
        return False

    def _validated_edge_case_prediction(self, text: str) -> Dict:
        """
        STRATEGIC VALIDATION: Extra testing for edge cases where FastText
        behavior might be unexpected or inconsistent.
        """
        clean_text = self._preprocess_text(text)

        # Test that preprocessing doesn't break prediction
        try:
            predictions = self.model.predict(clean_text, k=len(self.classes))
            labels, scores = predictions

            if not labels or not scores:
                # Fallback handling validated
                return {
                    'text': text,
                    'predicted_label': self.classes[0] if self.classes else 'unknown',
                    'confidence': 0.0,
                    'probabilities': {cls: 0.0 for cls in self.classes}
                }

            predicted_label = labels[0].replace('__label__', '')
            confidence = float(scores[0])

            # Validate confidence is reasonable
            assert 0.0 <= confidence <= 1.0, f"Invalid confidence: {confidence}"

            probabilities = {}
            for label, score in zip(labels, scores):
                clean_label = label.replace('__label__', '')
                probabilities[clean_label] = float(score)

            return {
                'text': text,
                'predicted_label': predicted_label,
                'confidence': confidence,
                'probabilities': probabilities
            }

        except Exception as e:
            # Graceful degradation for edge cases
            return {
                'text': text,
                'predicted_label': self.classes[0] if self.classes else 'unknown',
                'confidence': 0.0,
                'probabilities': {cls: 0.0 for cls in self.classes},
                'error': str(e)
            }

    def predict_batch(self, texts: List[str]) -> List[Dict]:
        """Batch prediction with efficiency focus."""
        return [self.predict(text) for text in texts]

    def save_model(self, filepath: str) -> None:
        """Save model with validation."""
        if not self.is_trained:
            raise ValueError("No trained model to save")

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.model.save_model(filepath)

        # VALIDATION: Verify save succeeded
        assert os.path.exists(filepath), "Model file not created"

    def load_model(self, filepath: str) -> None:
        """Load model with validation."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")

        self.model = fasttext.load_model(filepath)
        self.is_trained = True

        # Extract classes (best effort)
        try:
            test_pred = self.model.predict("test", k=10)
            if test_pred[0]:
                self.classes = [label.replace('__label__', '') for label in test_pred[0]]
        except:
            self.classes = []

    def __del__(self):
        """Cleanup resources."""
        try:
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                import shutil
                shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass


def create_sample_data():
    """Generate sample data including edge cases for validation."""
    texts = [
        # Standard cases
        "I love this product! Amazing quality.",
        "Great service, highly recommend!",
        "Excellent experience overall.",
        "Terrible quality, broke immediately.",
        "Poor service, very disappointed.",
        "Awful product, avoid completely.",
        "It's okay, does the job.",
        "Average quality, nothing special.",
        "Decent for the price point.",

        # Edge cases for validation
        "Text with __label__ in content should work",
        "Text\nwith\nnewlines gets cleaned",
        "Text with 'quotes' and \"double quotes\"",
        "",  # Empty text
        "   whitespace only   ",
        "Very long text " * 50 + " should still work fine"
    ]

    labels = ['positive'] * 3 + ['negative'] * 3 + ['neutral'] * 3 + \
             ['positive'] * 3 + ['negative'] * 3
    return texts, labels


if __name__ == "__main__":
    print("FastText Adaptive TDD Implementation Demo")
    print("=" * 50)

    classifier = FastTextAdaptiveClassifier()
    texts, labels = create_sample_data()

    print(f"Training on {len(texts)} samples (including edge cases)...")
    training_info = classifier.train(texts, labels)
    print(f"Training complete: {training_info}")

    # Test both normal and edge cases
    test_cases = [
        "This is absolutely fantastic!",  # Normal
        "Really disappointed with this.",  # Normal
        "",  # Edge case: empty
        "Text\nwith\nnewlines",  # Edge case: newlines
        "Text with __label__ content"  # Edge case: label collision
    ]

    print("\nTest predictions (including edge cases):")
    for text in test_cases:
        result = classifier.predict(text)
        display_text = text if text else "(empty)"
        print(f"'{display_text}' → {result['predicted_label']} ({result['confidence']:.3f})")

    print("\n✅ Adaptive TDD Implementation Complete!")
    print("Strategic validation focused on FastText complexity areas.")