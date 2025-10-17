"""
FastText Text Classification Wrapper

A clean, user-friendly wrapper around FastText for text classification.
Handles file preparation, temp cleanup, and provides a consistent API.

Example usage:
    classifier = TextClassifier()

    # Train
    texts = ['good product', 'bad service', 'excellent quality']
    labels = ['positive', 'negative', 'positive']
    classifier.train(texts, labels)

    # Predict
    result = classifier.predict('great experience')
    print(f"{result['label']}: {result['confidence']:.2f}")

    # Save/Load
    classifier.save('model.bin')
    loaded = TextClassifier.load('model.bin')
"""

import os
import tempfile
from typing import List, Dict, Any, Optional
import fasttext


class TextClassifier:
    """FastText text classification wrapper with clean API"""

    def __init__(self):
        """Initialize empty classifier"""
        self.model: Optional[fasttext.FastText._FastText] = None
        self._is_trained = False

    def train(
        self,
        texts: List[str],
        labels: List[str],
        lr: float = 0.5,
        epoch: int = 25,
        wordNgrams: int = 2,
        dim: int = 100
    ) -> Dict[str, Any]:
        """
        Train the classifier on provided texts and labels.

        Args:
            texts: List of text strings to train on
            labels: List of corresponding labels
            lr: Learning rate (default: 0.5)
            epoch: Number of training epochs (default: 25)
            wordNgrams: Word n-gram size (default: 2)
            dim: Dimension of word vectors (default: 100)

        Returns:
            Dict with training metrics (accuracy, etc.)

        Raises:
            ValueError: If inputs are empty or mismatched lengths
        """
        # Validate inputs
        if not texts or not labels:
            raise ValueError("Training data cannot be empty")

        if len(texts) != len(labels):
            raise ValueError("Texts and labels must have the same length")

        # Prepare training data in FastText format
        temp_file = None
        try:
            # Create temp file for training data
            fd, temp_file = tempfile.mkstemp(suffix='.txt', text=True)

            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                for text, label in zip(texts, labels):
                    # FastText format: __label__<label> <text>
                    # Clean text to avoid line breaks
                    clean_text = text.replace('\n', ' ').replace('\r', ' ')
                    f.write(f"__label__{label} {clean_text}\n")

            # Train model (suppress FastText output)
            self.model = fasttext.train_supervised(
                temp_file,
                lr=lr,
                epoch=epoch,
                wordNgrams=wordNgrams,
                dim=dim,
                verbose=0
            )

            self._is_trained = True

            # Get training metrics
            samples, precision, recall = self.model.test(temp_file)
            accuracy = precision  # For single-label classification

            return {
                'accuracy': accuracy,
                'samples': samples,
                'precision': precision,
                'recall': recall
            }

        finally:
            # Clean up temp file
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predict the label for a single text.

        Args:
            text: Text string to classify

        Returns:
            Dict with 'label' and 'confidence' keys

        Raises:
            RuntimeError: If model is not trained yet
            ValueError: If text is empty
        """
        if not self._is_trained or self.model is None:
            raise RuntimeError("Model is not trained. Call train() first.")

        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Get prediction
        labels, confidences = self.model.predict(text, k=1)

        # Clean up __label__ prefix
        label = labels[0].replace('__label__', '')
        confidence = float(confidences[0])

        return {
            'label': label,
            'confidence': confidence
        }

    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Predict labels for multiple texts efficiently.

        Args:
            texts: List of text strings to classify

        Returns:
            List of dicts, each with 'label' and 'confidence' keys

        Raises:
            RuntimeError: If model is not trained yet
        """
        if not self._is_trained or self.model is None:
            raise RuntimeError("Model is not trained. Call train() first.")

        if not texts:
            return []

        results = []
        for text in texts:
            # Skip empty texts in batch
            if not text or not text.strip():
                results.append({'label': 'unknown', 'confidence': 0.0})
                continue

            labels, confidences = self.model.predict(text, k=1)
            label = labels[0].replace('__label__', '')
            confidence = float(confidences[0])

            results.append({
                'label': label,
                'confidence': confidence
            })

        return results

    def save(self, path: str) -> None:
        """
        Save the trained model to disk.

        Args:
            path: File path to save the model

        Raises:
            RuntimeError: If model is not trained yet
        """
        if not self._is_trained or self.model is None:
            raise RuntimeError("Model is not trained. Cannot save.")

        self.model.save_model(path)

    @classmethod
    def load(cls, path: str) -> 'TextClassifier':
        """
        Load a trained model from disk.

        Args:
            path: File path to load the model from

        Returns:
            TextClassifier instance with loaded model

        Raises:
            FileNotFoundError: If model file doesn't exist
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found: {path}")

        classifier = cls()
        classifier.model = fasttext.load_model(path)
        classifier._is_trained = True

        return classifier
