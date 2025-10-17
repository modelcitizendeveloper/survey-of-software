"""
FastText Text Classification - Method 3: Test-First Development
Tests written first to drive implementation design.
"""

import unittest
import tempfile
import os
from text_classifier import FastTextTDDClassifier


class TestFastTextTDDClassifier(unittest.TestCase):
    """Comprehensive test suite driving TDD implementation."""

    def setUp(self):
        """Set up test fixtures."""
        self.classifier = FastTextTDDClassifier()
        self.sample_texts = [
            "I love this amazing product!",
            "Great service, highly recommend!",
            "Excellent quality and delivery.",
            "Terrible quality, broke immediately.",
            "Poor service, very disappointed.",
            "Awful product, doesn't work.",
            "It's okay, does the job.",
            "Average quality, nothing special.",
            "Decent product for the price."
        ]
        self.sample_labels = ['positive', 'positive', 'positive',
                             'negative', 'negative', 'negative',
                             'neutral', 'neutral', 'neutral']

    def test_initialization(self):
        """Test classifier initializes correctly."""
        self.assertIsNotNone(self.classifier)
        self.assertFalse(self.classifier.is_trained())

    def test_train_with_valid_data(self):
        """Test training with valid dataset."""
        result = self.classifier.train(self.sample_texts, self.sample_labels)

        self.assertTrue(self.classifier.is_trained())
        self.assertIn('training_samples', result)
        self.assertEqual(result['training_samples'], len(self.sample_texts))
        self.assertIn('classes', result)
        self.assertEqual(set(result['classes']), {'positive', 'negative', 'neutral'})

    def test_train_requires_matching_lengths(self):
        """Test training fails with mismatched text/label lengths."""
        with self.assertRaises(ValueError):
            self.classifier.train(self.sample_texts, self.sample_labels[:-1])

    def test_train_requires_minimum_samples(self):
        """Test training fails with insufficient data."""
        with self.assertRaises(ValueError):
            self.classifier.train(["text1"], ["label1"])

    def test_predict_single_text(self):
        """Test single text prediction."""
        self.classifier.train(self.sample_texts, self.sample_labels)

        result = self.classifier.predict("This is fantastic!")

        self.assertIn('text', result)
        self.assertIn('predicted_label', result)
        self.assertIn('confidence', result)
        self.assertEqual(result['text'], "This is fantastic!")
        self.assertIsInstance(result['confidence'], float)
        self.assertIn(result['predicted_label'], ['positive', 'negative', 'neutral'])

    def test_predict_without_training_fails(self):
        """Test prediction fails on untrained model."""
        with self.assertRaises(ValueError):
            self.classifier.predict("test text")

    def test_predict_batch(self):
        """Test batch prediction functionality."""
        self.classifier.train(self.sample_texts, self.sample_labels)

        test_texts = ["Great product!", "Terrible experience!", "It's okay."]
        results = self.classifier.predict_batch(test_texts)

        self.assertEqual(len(results), len(test_texts))
        for result in results:
            self.assertIn('predicted_label', result)
            self.assertIn('confidence', result)

    def test_predict_empty_string(self):
        """Test prediction handles empty strings gracefully."""
        self.classifier.train(self.sample_texts, self.sample_labels)

        result = self.classifier.predict("")

        self.assertIn('predicted_label', result)
        self.assertIsInstance(result['confidence'], float)

    def test_save_and_load_model(self):
        """Test model persistence."""
        self.classifier.train(self.sample_texts, self.sample_labels)

        with tempfile.NamedTemporaryFile(suffix='.bin', delete=False) as f:
            filepath = f.name

        try:
            # Save model
            self.classifier.save_model(filepath)
            self.assertTrue(os.path.exists(filepath))

            # Create new classifier and load
            new_classifier = FastTextTDDClassifier()
            new_classifier.load_model(filepath)

            self.assertTrue(new_classifier.is_trained())

            # Test loaded model works
            result = new_classifier.predict("Great product!")
            self.assertIn('predicted_label', result)

        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_save_untrained_model_fails(self):
        """Test saving untrained model raises error."""
        with self.assertRaises(ValueError):
            self.classifier.save_model("test.bin")

    def test_performance_requirement(self):
        """Test prediction meets <100ms requirement."""
        import time

        self.classifier.train(self.sample_texts, self.sample_labels)

        start_time = time.time()
        self.classifier.predict("Test performance text")
        end_time = time.time()

        prediction_time = (end_time - start_time) * 1000  # Convert to ms
        self.assertLess(prediction_time, 100, f"Prediction took {prediction_time:.2f}ms (requirement: <100ms)")


if __name__ == '__main__':
    unittest.main()