"""
scikit-learn Text Classification - Method 3: Test-First Development
Comprehensive test suite driving TDD implementation.
"""

import unittest
import tempfile
import os
import numpy as np
from text_classifier import SklearnTDDClassifier


class TestSklearnTDDClassifier(unittest.TestCase):
    """TDD test suite for scikit-learn text classifier."""

    def setUp(self):
        """Set up test fixtures."""
        self.classifier = SklearnTDDClassifier()
        self.sample_texts = [
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
        self.sample_labels = (['positive'] * 10 + ['negative'] * 10 + ['neutral'] * 10)

    def test_initialization(self):
        """Test classifier initializes properly."""
        self.assertIsNotNone(self.classifier)
        self.assertFalse(self.classifier.is_trained())

    def test_train_with_valid_data(self):
        """Test training with valid dataset."""
        result = self.classifier.train(self.sample_texts, self.sample_labels)

        self.assertTrue(self.classifier.is_trained())
        self.assertIn('training_samples', result)
        self.assertIn('validation_accuracy', result)
        self.assertIn('classes', result)
        self.assertEqual(set(result['classes']), {'positive', 'negative', 'neutral'})
        self.assertIsInstance(result['validation_accuracy'], float)
        self.assertGreaterEqual(result['validation_accuracy'], 0.0)
        self.assertLessEqual(result['validation_accuracy'], 1.0)

    def test_train_requires_matching_lengths(self):
        """Test training fails with mismatched lengths."""
        with self.assertRaises(ValueError) as context:
            self.classifier.train(self.sample_texts, self.sample_labels[:-5])
        self.assertIn("length", str(context.exception).lower())

    def test_train_requires_sufficient_data(self):
        """Test training fails with insufficient data."""
        with self.assertRaises(ValueError):
            self.classifier.train(["text1", "text2"], ["label1", "label2"])

    def test_train_requires_multiple_classes(self):
        """Test training fails with single class."""
        texts = ["text1", "text2", "text3", "text4", "text5", "text6"]
        labels = ["same"] * 6
        with self.assertRaises(ValueError):
            self.classifier.train(texts, labels)

    def test_predict_single_text(self):
        """Test single text prediction."""
        self.classifier.train(self.sample_texts, self.sample_labels)

        result = self.classifier.predict("This is absolutely fantastic!")

        self.assertIn('text', result)
        self.assertIn('predicted_label', result)
        self.assertIn('confidence', result)
        self.assertIn('probabilities', result)
        self.assertEqual(result['text'], "This is absolutely fantastic!")
        self.assertIn(result['predicted_label'], ['positive', 'negative', 'neutral'])
        self.assertIsInstance(result['confidence'], float)
        self.assertGreaterEqual(result['confidence'], 0.0)
        self.assertLessEqual(result['confidence'], 1.0)
        self.assertIsInstance(result['probabilities'], dict)
        self.assertEqual(set(result['probabilities'].keys()), {'positive', 'negative', 'neutral'})

    def test_predict_without_training_fails(self):
        """Test prediction fails on untrained model."""
        with self.assertRaises(ValueError) as context:
            self.classifier.predict("test text")
        self.assertIn("trained", str(context.exception).lower())

    def test_predict_batch(self):
        """Test batch prediction functionality."""
        self.classifier.train(self.sample_texts, self.sample_labels)

        test_texts = ["Great product!", "Terrible experience!", "It's okay."]
        results = self.classifier.predict_batch(test_texts)

        self.assertEqual(len(results), len(test_texts))
        for i, result in enumerate(results):
            self.assertEqual(result['text'], test_texts[i])
            self.assertIn('predicted_label', result)
            self.assertIn('confidence', result)
            self.assertIn('probabilities', result)

    def test_predict_empty_string(self):
        """Test prediction handles empty strings."""
        self.classifier.train(self.sample_texts, self.sample_labels)

        result = self.classifier.predict("")

        self.assertEqual(result['text'], "")
        self.assertIn('predicted_label', result)
        self.assertIsInstance(result['confidence'], float)

    def test_predict_whitespace_only(self):
        """Test prediction handles whitespace-only strings."""
        self.classifier.train(self.sample_texts, self.sample_labels)

        result = self.classifier.predict("   \n\t   ")

        self.assertIn('predicted_label', result)
        self.assertIsInstance(result['confidence'], float)

    def test_save_and_load_model(self):
        """Test model persistence."""
        self.classifier.train(self.sample_texts, self.sample_labels)

        with tempfile.NamedTemporaryFile(suffix='.joblib', delete=False) as f:
            filepath = f.name

        try:
            # Save model
            self.classifier.save_model(filepath)
            self.assertTrue(os.path.exists(filepath))

            # Test prediction before loading
            original_prediction = self.classifier.predict("Great product!")

            # Create new classifier and load
            new_classifier = SklearnTDDClassifier()
            self.assertFalse(new_classifier.is_trained())

            new_classifier.load_model(filepath)
            self.assertTrue(new_classifier.is_trained())

            # Test loaded model produces same results
            loaded_prediction = new_classifier.predict("Great product!")
            self.assertEqual(original_prediction['predicted_label'],
                           loaded_prediction['predicted_label'])

        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_save_untrained_model_fails(self):
        """Test saving untrained model raises error."""
        with self.assertRaises(ValueError) as context:
            self.classifier.save_model("test.joblib")
        self.assertIn("trained", str(context.exception).lower())

    def test_load_nonexistent_file_fails(self):
        """Test loading nonexistent file raises error."""
        with self.assertRaises((FileNotFoundError, Exception)):
            self.classifier.load_model("nonexistent_file.joblib")

    def test_performance_requirement(self):
        """Test prediction meets <100ms requirement."""
        import time

        self.classifier.train(self.sample_texts, self.sample_labels)

        # Test single prediction performance
        start_time = time.time()
        self.classifier.predict("Test performance text for timing measurement")
        end_time = time.time()

        prediction_time = (end_time - start_time) * 1000  # Convert to ms
        self.assertLess(prediction_time, 100,
                       f"Single prediction took {prediction_time:.2f}ms (requirement: <100ms)")

    def test_batch_performance_requirement(self):
        """Test batch prediction efficiency."""
        import time

        self.classifier.train(self.sample_texts, self.sample_labels)

        test_texts = ["Test text"] * 100
        start_time = time.time()
        results = self.classifier.predict_batch(test_texts)
        end_time = time.time()

        batch_time = (end_time - start_time) * 1000  # Convert to ms
        self.assertEqual(len(results), 100)
        self.assertLess(batch_time, 500,
                       f"Batch prediction took {batch_time:.2f}ms (requirement: <500ms)")

    def test_probability_distribution_validity(self):
        """Test that probabilities form valid distribution."""
        self.classifier.train(self.sample_texts, self.sample_labels)

        result = self.classifier.predict("Test probability distribution")
        probabilities = result['probabilities']

        # Check all probabilities are non-negative
        for prob in probabilities.values():
            self.assertGreaterEqual(prob, 0.0)

        # Check probabilities sum to approximately 1.0
        total_prob = sum(probabilities.values())
        self.assertAlmostEqual(total_prob, 1.0, places=5)

        # Check confidence matches max probability
        max_prob = max(probabilities.values())
        self.assertAlmostEqual(result['confidence'], max_prob, places=5)

    def test_consistent_predictions(self):
        """Test that same input produces consistent predictions."""
        self.classifier.train(self.sample_texts, self.sample_labels)

        test_text = "Consistent prediction test"

        # Make multiple predictions
        results = [self.classifier.predict(test_text) for _ in range(5)]

        # All predictions should be identical
        first_result = results[0]
        for result in results[1:]:
            self.assertEqual(result['predicted_label'], first_result['predicted_label'])
            self.assertAlmostEqual(result['confidence'], first_result['confidence'], places=5)


if __name__ == '__main__':
    unittest.main()