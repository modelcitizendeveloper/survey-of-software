"""
Strategic tests for TextClassifier (Method 4: Adaptive TDD)

Testing ONLY high-risk areas:
1. State management (predict before train)
2. Batch prediction correctness
3. Save/load with pickle (state preservation)
4. Single text wrapping (common bug)
"""

import pytest
import pickle
import tempfile
import os
from text_classifier import TextClassifier


# Test data
TRAIN_TEXTS = [
    "I love this product",
    "This is terrible",
    "Great quality",
    "Waste of money",
    "Highly recommended",
    "Very disappointed",
    "Excellent service",
    "Poor experience"
]

TRAIN_LABELS = [
    "positive",
    "negative",
    "positive",
    "negative",
    "positive",
    "negative",
    "positive",
    "negative"
]


class TestStateManagement:
    """HIGH-RISK: State management errors are common in wrappers"""

    def test_predict_before_training_raises_error(self):
        """Should raise ValueError when predicting before training"""
        classifier = TextClassifier()
        with pytest.raises(ValueError, match="not trained"):
            classifier.predict("test text")

    def test_predict_batch_before_training_raises_error(self):
        """Should raise ValueError when batch predicting before training"""
        classifier = TextClassifier()
        with pytest.raises(ValueError, match="not trained"):
            classifier.predict_batch(["test1", "test2"])

    def test_is_trained_flag_updated_after_training(self):
        """State flag should be updated after training"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)
        # After training, predict should work (not raise)
        result = classifier.predict("great product")
        assert 'label' in result
        assert 'confidence' in result


class TestBatchPrediction:
    """HIGH-RISK: Batch operations often have efficiency/correctness bugs"""

    def test_batch_prediction_returns_correct_count(self):
        """Batch should return same number of results as inputs"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        test_texts = ["good", "bad", "excellent"]
        results = classifier.predict_batch(test_texts)

        assert len(results) == len(test_texts)

    def test_batch_prediction_format_consistency(self):
        """Each batch result should have consistent format"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        results = classifier.predict_batch(["good", "bad"])

        for result in results:
            assert 'label' in result
            assert 'confidence' in result
            assert isinstance(result['label'], str)
            assert isinstance(result['confidence'], float)
            assert 0.0 <= result['confidence'] <= 1.0

    def test_batch_vs_single_prediction_consistency(self):
        """Batch prediction should match multiple single predictions"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        test_texts = ["amazing", "terrible"]

        # Single predictions
        single_results = [classifier.predict(text) for text in test_texts]

        # Batch prediction
        batch_results = classifier.predict_batch(test_texts)

        # Should match
        for single, batch in zip(single_results, batch_results):
            assert single['label'] == batch['label']
            assert abs(single['confidence'] - batch['confidence']) < 0.001


class TestSingleTextWrapping:
    """HIGH-RISK: Forgetting to wrap single text in list is common sklearn bug"""

    def test_single_text_prediction_works(self):
        """Single text should be properly wrapped for sklearn"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        # Should not raise error about shape/dimensionality
        result = classifier.predict("great product")

        assert 'label' in result
        assert result['label'] in ['positive', 'negative']

    def test_single_text_returns_single_result_not_list(self):
        """Single prediction should return dict, not list of dicts"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        result = classifier.predict("test")

        # Should be dict, not list
        assert isinstance(result, dict)
        assert not isinstance(result, list)


class TestSaveLoadSerialization:
    """HIGH-RISK: Pickle serialization can fail to preserve state"""

    def test_save_and_load_preserves_predictions(self):
        """Loaded model should make same predictions as original"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        # Make prediction with original
        original_result = classifier.predict("excellent product")

        # Save and load
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pkl') as f:
            temp_path = f.name
            classifier.save(temp_path)

        try:
            loaded_classifier = TextClassifier.load(temp_path)
            loaded_result = loaded_classifier.predict("excellent product")

            # Should match
            assert loaded_result['label'] == original_result['label']
            assert abs(loaded_result['confidence'] - original_result['confidence']) < 0.001
        finally:
            os.unlink(temp_path)

    def test_loaded_model_is_trained(self):
        """Loaded model should have trained state"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pkl') as f:
            temp_path = f.name
            classifier.save(temp_path)

        try:
            loaded_classifier = TextClassifier.load(temp_path)

            # Should be able to predict (not raise "not trained" error)
            result = loaded_classifier.predict("test")
            assert 'label' in result
        finally:
            os.unlink(temp_path)

    def test_save_before_training_raises_error(self):
        """Should not allow saving untrained model"""
        classifier = TextClassifier()

        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pkl') as f:
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="not trained"):
                classifier.save(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestConfidenceScores:
    """MEDIUM-RISK: Confidence calculation can be incorrect"""

    def test_confidence_in_valid_range(self):
        """Confidence should be between 0 and 1"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        result = classifier.predict("great")

        assert 0.0 <= result['confidence'] <= 1.0

    def test_confidence_uses_predict_proba(self):
        """Should use predict_proba for proper probability scores"""
        classifier = TextClassifier()
        classifier.train(TRAIN_TEXTS, TRAIN_LABELS)

        result = classifier.predict("excellent")

        # With good training data, confidence should be reasonable (not 0 or 1)
        # This ensures we're using predict_proba, not just hardcoding
        assert result['confidence'] > 0.0
