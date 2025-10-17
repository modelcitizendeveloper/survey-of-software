"""
Strategic tests for FastText wrapper - Method 4 (Adaptive TDD)

Tests focus on HIGH-RISK areas only:
1. Temp file cleanup (resource leaks)
2. Error handling (predict before train, empty input)
3. Save/load (serialization integrity)

Straightforward parts (basic predict, simple getters) are NOT tested.
"""

import os
import tempfile
import pytest
from text_classifier import TextClassifier


# Test data
TRAIN_TEXTS = [
    "I love this product",
    "This is terrible",
    "Great quality",
    "Waste of money",
    "Highly recommended",
    "Very disappointed"
]

TRAIN_LABELS = ["positive", "negative", "positive", "negative", "positive", "negative"]


class TestHighRiskAreas:
    """Strategic tests for high-risk functionality"""

    def test_predict_before_train_raises_error(self):
        """HIGH-RISK: Predict before training should fail gracefully"""
        classifier = TextClassifier()
        with pytest.raises(RuntimeError, match="not trained"):
            classifier.predict("test text")

    def test_train_with_empty_data_raises_error(self):
        """HIGH-RISK: Empty training data should be rejected"""
        classifier = TextClassifier()
        with pytest.raises(ValueError, match="empty"):
            classifier.train([], [])

    def test_train_with_mismatched_lengths_raises_error(self):
        """HIGH-RISK: Mismatched texts/labels should be rejected"""
        classifier = TextClassifier()
        with pytest.raises(ValueError, match="same length"):
            classifier.train(["text1", "text2"], ["label1"])

    def test_temp_file_cleanup_after_training(self):
        """HIGH-RISK: Temp files must be cleaned up to avoid resource leaks"""
        temp_dir = tempfile.gettempdir()
        before_files = set(os.listdir(temp_dir))

        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        after_files = set(os.listdir(temp_dir))
        new_files = after_files - before_files

        # Filter for likely training files
        training_files = [f for f in new_files if 'train' in f.lower() or 'fasttext' in f.lower()]
        assert len(training_files) == 0, f"Temp files not cleaned up: {training_files}"

    def test_save_and_load_preserves_predictions(self):
        """HIGH-RISK: Save/load must preserve model integrity"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        test_text = "excellent product"
        original_result = classifier.predict(test_text)

        # Save and load
        with tempfile.NamedTemporaryFile(suffix='.bin', delete=False) as f:
            model_path = f.name

        try:
            classifier.save(model_path)
            loaded_classifier = TextClassifier.load(model_path)

            loaded_result = loaded_classifier.predict(test_text)

            assert loaded_result['label'] == original_result['label']
            assert abs(loaded_result['confidence'] - original_result['confidence']) < 0.01
        finally:
            if os.path.exists(model_path):
                os.remove(model_path)

    def test_save_before_train_raises_error(self):
        """HIGH-RISK: Cannot save untrained model"""
        classifier = TextClassifier()
        with pytest.raises(RuntimeError, match="not trained"):
            classifier.save("model.bin")

    def test_load_nonexistent_file_raises_error(self):
        """HIGH-RISK: Loading missing file should fail gracefully"""
        with pytest.raises(FileNotFoundError):
            TextClassifier.load("nonexistent_model.bin")

    def test_predict_empty_text_raises_error(self):
        """HIGH-RISK: Empty text input should be rejected"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        with pytest.raises(ValueError, match="empty"):
            classifier.predict("")

    def test_predict_batch_with_empty_list(self):
        """HIGH-RISK: Empty batch should return empty list, not crash"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        results = classifier.predict_batch([])
        assert results == []

    def test_prediction_format_consistency(self):
        """HIGH-RISK: Output format must be consistent (dict with label and confidence)"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        result = classifier.predict("great product")

        assert isinstance(result, dict)
        assert 'label' in result
        assert 'confidence' in result
        assert isinstance(result['label'], str)
        assert isinstance(result['confidence'], float)
        assert 0.0 <= result['confidence'] <= 1.0

    def test_label_prefix_cleanup(self):
        """HIGH-RISK: FastText's __label__ prefix must be removed from predictions"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        result = classifier.predict("amazing")

        # Label should NOT contain __label__ prefix
        assert not result['label'].startswith('__label__')
        assert result['label'] in ['positive', 'negative']

    def test_batch_prediction_returns_list_of_dicts(self):
        """HIGH-RISK: Batch predictions must return consistent format"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        results = classifier.predict_batch(["great", "terrible"])

        assert isinstance(results, list)
        assert len(results) == 2
        for result in results:
            assert isinstance(result, dict)
            assert 'label' in result
            assert 'confidence' in result
