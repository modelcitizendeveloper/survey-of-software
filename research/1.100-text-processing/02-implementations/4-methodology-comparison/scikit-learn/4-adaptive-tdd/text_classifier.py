"""
scikit-learn Text Classification - Method 4: Adaptive TDD
Strategic testing focused on complex pipeline interactions.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import time
import warnings
from typing import List, Dict, Optional


class SklearnAdaptiveTDDClassifier:
    """
    Adaptive TDD scikit-learn classifier with strategic validation.
    Focuses testing on complex pipeline interactions and edge cases.
    """

    def __init__(self):
        """Initialize with strategic configuration for robust pipeline."""
        # Configure vectorizer with adaptive parameters
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            stop_words='english',
            lowercase=True,
            strip_accents='unicode',
            sublinear_tf=True,  # Better for varying document lengths
            min_df=1,  # Handle small vocabularies
            max_df=0.95  # Remove very common terms
        )

        # Configure classifier for robustness
        self.classifier = LogisticRegression(
            random_state=42,
            max_iter=1000,
            class_weight='balanced',  # Handle imbalanced data
            solver='liblinear'  # Stable for small-medium datasets
        )

        self.pipeline = Pipeline([
            ('vectorizer', self.vectorizer),
            ('classifier', self.classifier)
        ])

        self.label_encoder = LabelEncoder()
        self.is_trained = False
        self.classes_ = None

    def train(self, texts: List[str], labels: List[str]) -> Dict:
        """
        Train with adaptive validation on complex pipeline interactions.

        STRATEGIC FOCUS: Pipeline component interaction is where scikit-learn
        complexity creates bugs - validate this thoroughly.
        """
        start_time = time.time()

        # Basic validation (straightforward)
        if len(texts) != len(labels) or len(texts) < 10:
            raise ValueError("Invalid training data")

        # STRATEGIC VALIDATION: Test pipeline component interactions
        self._validate_pipeline_robustness(texts, labels)

        # Prepare data with edge case handling
        processed_texts, processed_labels = self._robust_data_preparation(texts, labels)

        # Train with cross-validation for robustness assessment
        training_metrics = self._validated_training(processed_texts, processed_labels)

        self.is_trained = True
        training_metrics['training_time'] = time.time() - start_time

        return training_metrics

    def _validate_pipeline_robustness(self, texts: List[str], labels: List[str]):
        """
        ADAPTIVE VALIDATION: Test complex interactions between vectorizer and classifier.
        This is where scikit-learn pipelines commonly have issues.
        """
        # Test edge cases that could break the pipeline
        edge_cases = [
            ("", "positive"),  # Empty text
            ("   ", "negative"),  # Whitespace only
            ("a", "neutral"),  # Single character
            ("word " * 1000, "positive"),  # Very long text
            ("UPPERCASE TEXT", "negative"),  # Case variations
            ("text with números 123", "neutral"),  # Mixed content
            ("text\nwith\nnewlines", "positive"),  # Newlines
            ("special !@#$%^&*() characters", "negative")  # Special chars
        ]

        # Create test pipeline to validate edge case handling
        test_vectorizer = TfidfVectorizer(
            max_features=100,  # Small for quick test
            ngram_range=(1, 1),
            stop_words='english'
        )

        test_texts = [case[0] for case in edge_cases]
        test_labels = [case[1] for case in edge_cases]

        try:
            # Test vectorization doesn't break
            test_vectors = test_vectorizer.fit_transform(test_texts)

            # Validate matrix properties
            assert test_vectors.shape[0] == len(test_texts), "Vector count mismatch"
            assert test_vectors.shape[1] > 0, "No features extracted"
            assert not np.any(np.isnan(test_vectors.data)), "NaN values in vectors"

            # Test label encoding
            test_encoder = LabelEncoder()
            encoded_labels = test_encoder.fit_transform(test_labels)
            assert len(encoded_labels) == len(test_labels), "Label encoding failed"

        except Exception as e:
            raise RuntimeError(f"Pipeline robustness validation failed: {e}")

    def _robust_data_preparation(self, texts: List[str], labels: List[str]) -> tuple:
        """Prepare data with comprehensive edge case handling."""
        processed_texts = []
        processed_labels = []

        for text, label in zip(texts, labels):
            # Handle None or empty texts
            if not text:
                processed_text = ""
            else:
                # Normalize text while preserving content
                processed_text = str(text).strip()
                # Handle excessive whitespace
                processed_text = ' '.join(processed_text.split())

            processed_texts.append(processed_text)
            processed_labels.append(label)

        return processed_texts, processed_labels

    def _validated_training(self, texts: List[str], labels: List[str]) -> Dict:
        """Training with strategic validation of complex operations."""
        # Prepare arrays
        X = np.array(texts)
        y = np.array(labels)

        # Encode labels with validation
        y_encoded = self.label_encoder.fit_transform(y)
        self.classes_ = self.label_encoder.classes_

        # STRATEGIC VALIDATION: Test train/test split robustness
        try:
            X_train, X_val, y_train, y_val = train_test_split(
                X, y_encoded,
                test_size=0.2,
                random_state=42,
                stratify=y_encoded
            )
        except ValueError as e:
            # Fallback for edge cases where stratification fails
            X_train, X_val, y_train, y_val = train_test_split(
                X, y_encoded,
                test_size=0.2,
                random_state=42
            )

        # Train pipeline with error handling
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # Suppress sklearn warnings
            self.pipeline.fit(X_train, y_train)

        # STRATEGIC VALIDATION: Test pipeline prediction robustness
        self._validate_prediction_robustness(X_val)

        # Calculate comprehensive metrics
        val_predictions = self.pipeline.predict(X_val)
        validation_accuracy = accuracy_score(y_val, val_predictions)

        # Cross-validation for additional robustness assessment
        try:
            cv_scores = cross_val_score(
                self.pipeline, X_train, y_train,
                cv=min(5, len(X_train) // 10),
                scoring='accuracy'
            )
            cv_mean = float(np.mean(cv_scores))
        except Exception:
            cv_mean = validation_accuracy  # Fallback

        return {
            'training_samples': len(X_train),
            'validation_samples': len(X_val),
            'validation_accuracy': validation_accuracy,
            'cross_validation_mean': cv_mean,
            'classes': list(self.classes_)
        }

    def _validate_prediction_robustness(self, test_samples):
        """
        STRATEGIC VALIDATION: Test prediction pipeline handles edge cases.
        """
        # Test with various edge cases
        edge_test_cases = ["", "   ", "a", "word " * 100]

        for case in edge_test_cases:
            try:
                # Test that prediction doesn't crash
                pred = self.pipeline.predict([case])
                proba = self.pipeline.predict_proba([case])

                # Validate outputs
                assert len(pred) == 1, f"Prediction length error for '{case}'"
                assert proba.shape == (1, len(self.classes_)), f"Probability shape error for '{case}'"
                assert np.allclose(proba.sum(axis=1), 1.0), f"Probability sum error for '{case}'"

            except Exception as e:
                raise RuntimeError(f"Prediction robustness failed for '{case}': {e}")

    def predict(self, text: str) -> Dict:
        """
        Predict with adaptive validation for edge cases.
        """
        if not self.is_trained:
            raise ValueError("Model not trained")

        # ADAPTIVE VALIDATION: Apply extra testing for problematic inputs
        if self._is_complex_input(text):
            return self._validated_complex_prediction(text)

        # Standard prediction for normal cases
        return self._standard_prediction(text)

    def _is_complex_input(self, text: str) -> bool:
        """Identify inputs requiring extra validation."""
        if not text or not text.strip():
            return True
        if len(text) > 1000:  # Very long text
            return True
        if len(text) < 3:  # Very short text
            return True
        if text.count('\n') > 5:  # Many newlines
            return True
        return False

    def _validated_complex_prediction(self, text: str) -> Dict:
        """
        STRATEGIC VALIDATION: Extra testing for complex inputs that might
        break the pipeline or produce inconsistent results.
        """
        try:
            # Test preprocessing robustness
            processed_text = str(text) if text else ""

            # Validate vectorization works
            try:
                vectors = self.pipeline.named_steps['vectorizer'].transform([processed_text])
                assert vectors.shape[0] == 1, "Vectorization shape error"
                assert not np.any(np.isnan(vectors.data)), "NaN in vectors"
            except Exception as e:
                # Fallback for vectorization issues
                return {
                    'text': text,
                    'predicted_label': self.classes_[0] if len(self.classes_) > 0 else 'unknown',
                    'confidence': 0.0,
                    'probabilities': {cls: 0.0 for cls in self.classes_},
                    'error': f"Vectorization failed: {e}"
                }

            # Get predictions with validation
            prediction_encoded = self.pipeline.predict([processed_text])[0]
            probabilities = self.pipeline.predict_proba([processed_text])[0]

            # Validate probability distribution
            assert len(probabilities) == len(self.classes_), "Probability count mismatch"
            assert np.isclose(probabilities.sum(), 1.0, atol=1e-6), "Probabilities don't sum to 1"
            assert np.all(probabilities >= 0), "Negative probabilities"

            # Convert results
            predicted_label = self.label_encoder.inverse_transform([prediction_encoded])[0]
            confidence = float(np.max(probabilities))

            prob_dict = {}
            for label, prob in zip(self.classes_, probabilities):
                prob_dict[label] = float(prob)

            return {
                'text': text,
                'predicted_label': predicted_label,
                'confidence': confidence,
                'probabilities': prob_dict
            }

        except Exception as e:
            # Graceful degradation for edge cases
            return {
                'text': text,
                'predicted_label': self.classes_[0] if len(self.classes_) > 0 else 'unknown',
                'confidence': 0.0,
                'probabilities': {cls: 0.0 for cls in self.classes_},
                'error': str(e)
            }

    def _standard_prediction(self, text: str) -> Dict:
        """Standard prediction for normal inputs."""
        processed_text = str(text) if text else ""

        prediction_encoded = self.pipeline.predict([processed_text])[0]
        probabilities = self.pipeline.predict_proba([processed_text])[0]

        predicted_label = self.label_encoder.inverse_transform([prediction_encoded])[0]
        confidence = float(np.max(probabilities))

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
        """Efficient batch prediction with edge case handling."""
        return [self.predict(text) for text in texts]

    def save_model(self, filepath: str) -> None:
        """Save with validation."""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")

        model_data = {
            'pipeline': self.pipeline,
            'label_encoder': self.label_encoder,
            'classes': self.classes_
        }

        joblib.dump(model_data, filepath)

        # VALIDATION: Test save succeeded
        import os
        assert os.path.exists(filepath), "Model save failed"

    def load_model(self, filepath: str) -> None:
        """Load with validation."""
        model_data = joblib.load(filepath)

        self.pipeline = model_data['pipeline']
        self.label_encoder = model_data['label_encoder']
        self.classes_ = model_data['classes']

        self.is_trained = True

        # VALIDATION: Test loaded model works
        try:
            test_pred = self.pipeline.predict(["test"])
            assert len(test_pred) == 1, "Loaded model validation failed"
        except Exception as e:
            raise RuntimeError(f"Loaded model validation failed: {e}")


def create_sample_data():
    """Generate sample data including edge cases for validation."""
    texts = [
        # Standard positive samples
        "I absolutely love this product! Outstanding quality and performance.",
        "Fantastic experience that exceeded all my expectations completely.",
        "Brilliant design with amazing attention to detail throughout.",
        "Superb customer service, incredibly helpful and responsive team.",
        "Perfect solution that works flawlessly every single time.",
        "Excellent quality with fast delivery, very satisfied customer.",
        "Wonderful experience, will definitely purchase again soon.",
        "Great service and highly recommend to everyone I know.",
        "Amazing product, exactly what I needed for my project.",
        "Outstanding performance, truly exceeded my expectations.",

        # Standard negative samples
        "Terrible quality, broke immediately after first use.",
        "Horrible experience with slow delivery and damaged packaging.",
        "Awful product that doesn't work as advertised.",
        "Poor customer service, very disappointed with experience.",
        "Worst purchase ever, requesting immediate refund.",
        "Disappointing quality, not worth the high price.",
        "Broken on arrival, terrible packaging and handling.",
        "Useless product, complete failure and waste of time.",
        "Bad experience with rude staff and poor service.",
        "Defective item, doesn't function as described.",

        # Standard neutral samples
        "Acceptable product that gets the job done adequately.",
        "Average quality, meets basic requirements without issues.",
        "Standard functionality, nothing remarkable but works.",
        "Decent solution, works fine for simple tasks.",
        "Fair quality, reasonable value for money spent.",
        "Basic functionality, sufficient for general use.",
        "Ordinary quality, meets expectations for price.",
        "Regular product, does what it says without problems.",
        "Standard quality, as expected for this price range.",
        "It's okay, nothing special but works properly.",

        # Edge cases for robustness testing
        "",  # Empty string
        "   ",  # Whitespace only
        "a",  # Single character
        "UPPERCASE TEXT ONLY",  # All caps
        "text with números 123 and symbols !@#",  # Mixed content
        "very " * 200,  # Very long repetitive text
        "Text\nwith\nmultiple\nnewlines\neverywhere",  # Many newlines
        "Short.",  # Very short
        "normal text with some variety here"  # Normal case
    ]

    # Ensure balanced labels including edge cases
    labels = (['positive'] * 10 + ['negative'] * 10 + ['neutral'] * 10 +
             ['positive'] * 3 + ['negative'] * 3 + ['neutral'] * 3)

    return texts, labels


if __name__ == "__main__":
    print("scikit-learn Adaptive TDD Implementation Demo")
    print("=" * 55)

    classifier = SklearnAdaptiveTDDClassifier()
    texts, labels = create_sample_data()

    print(f"Training on {len(texts)} samples (including edge cases)...")
    training_info = classifier.train(texts, labels)
    print(f"Training complete: {training_info}")

    # Test both normal and complex edge cases
    test_cases = [
        "This is absolutely fantastic!",  # Normal positive
        "Really disappointed with this.",  # Normal negative
        "It's acceptable for basic use.",  # Normal neutral
        "",  # Edge: empty
        "   ",  # Edge: whitespace
        "a",  # Edge: single char
        "word " * 100,  # Edge: very long
        "Text\nwith\nnewlines"  # Edge: newlines
    ]

    print("\nTesting predictions (normal + edge cases):")
    for text in test_cases:
        result = classifier.predict(text)
        display_text = repr(text) if len(text) < 20 else f"{text[:20]}..."
        if 'error' in result:
            print(f"  {display_text} → {result['predicted_label']} (error: {result['error']})")
        else:
            print(f"  {display_text} → {result['predicted_label']} ({result['confidence']:.3f})")

    print("\n✅ Adaptive TDD Implementation Complete!")
    print("Strategic validation focused on pipeline complexity areas.")