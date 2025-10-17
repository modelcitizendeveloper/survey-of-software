"""
Text Classifier Wrapper for scikit-learn

A simple, user-friendly wrapper around sklearn's text classification pipeline.

Example usage:
    >>> from text_classifier import TextClassifier
    >>>
    >>> # Initialize and train
    >>> classifier = TextClassifier()
    >>> texts = ['good product', 'bad service', 'excellent quality']
    >>> labels = ['positive', 'negative', 'positive']
    >>> metrics = classifier.train(texts, labels)
    >>>
    >>> # Predict single text
    >>> result = classifier.predict('great experience')
    >>> print(f"Label: {result['label']}, Confidence: {result['confidence']:.2f}")
    >>>
    >>> # Batch prediction
    >>> results = classifier.predict_batch(['nice', 'terrible', 'ok'])
    >>>
    >>> # Save and load
    >>> classifier.save('model.pkl')
    >>> loaded = TextClassifier.load('model.pkl')
"""

import pickle
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np


class TextClassifier:
    """
    A wrapper around scikit-learn's text classification pipeline.

    Simplifies common text classification tasks with a clean interface
    for training, prediction, and model persistence.

    Attributes:
        pipeline: sklearn Pipeline with CountVectorizer and MultinomialNB
        classes_: Array of class labels after training
    """

    def __init__(self):
        """Initialize the text classifier with a sklearn pipeline."""
        self.pipeline = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('classifier', MultinomialNB())
        ])
        self._is_trained = False
        self.classes_ = None

    def train(
        self,
        texts: List[str],
        labels: List[str],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Train the classifier on provided texts and labels.

        Args:
            texts: List of text documents to train on
            labels: List of corresponding labels
            **kwargs: Additional parameters (reserved for future use)

        Returns:
            Dictionary with training metrics:
                - accuracy: Training accuracy score
                - n_samples: Number of training samples
                - n_classes: Number of unique classes

        Raises:
            ValueError: If texts/labels are empty or mismatched lengths
        """
        # Validation
        if not texts or not labels:
            raise ValueError("texts and labels cannot be empty")

        if len(texts) != len(labels):
            raise ValueError(
                f"texts and labels must have same length: "
                f"got {len(texts)} texts and {len(labels)} labels"
            )

        # Train the pipeline
        self.pipeline.fit(texts, labels)
        self.classes_ = self.pipeline.classes_
        self._is_trained = True

        # Calculate training metrics
        train_predictions = self.pipeline.predict(texts)
        accuracy = (train_predictions == labels).sum() / len(labels)

        return {
            'accuracy': float(accuracy),
            'n_samples': len(texts),
            'n_classes': len(self.classes_)
        }

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predict the label for a single text.

        Args:
            text: Text to classify

        Returns:
            Dictionary with prediction results:
                - label: Predicted class label (str)
                - confidence: Confidence score between 0 and 1 (float)

        Raises:
            ValueError: If model is not trained yet
            ValueError: If text is None or empty
        """
        # Validation
        if not self._is_trained:
            raise ValueError("Model is not trained yet. Call train() first.")

        if text is None or (isinstance(text, str) and not text.strip()):
            raise ValueError("text cannot be None or empty")

        # Wrap single text in list for sklearn (HIGH-RISK AREA)
        text_list = [text]

        # Get prediction and confidence
        label = self.pipeline.predict(text_list)[0]
        probabilities = self.pipeline.predict_proba(text_list)[0]

        # Get confidence for predicted class
        predicted_class_idx = np.where(self.classes_ == label)[0][0]
        confidence = float(probabilities[predicted_class_idx])

        return {
            'label': str(label),
            'confidence': confidence
        }

    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Predict labels for multiple texts efficiently.

        Args:
            texts: List of texts to classify

        Returns:
            List of prediction dictionaries, one per input text

        Raises:
            ValueError: If model is not trained yet
            ValueError: If texts is empty
        """
        # Validation
        if not self._is_trained:
            raise ValueError("Model is not trained yet. Call train() first.")

        if not texts:
            raise ValueError("texts cannot be empty")

        # Batch prediction (EFFICIENT - single sklearn call)
        labels = self.pipeline.predict(texts)
        probabilities = self.pipeline.predict_proba(texts)

        # Build results
        results = []
        for i, (label, probs) in enumerate(zip(labels, probabilities)):
            # Get confidence for predicted class
            predicted_class_idx = np.where(self.classes_ == label)[0][0]
            confidence = float(probs[predicted_class_idx])

            results.append({
                'label': str(label),
                'confidence': confidence
            })

        return results

    def save(self, filepath: str) -> None:
        """
        Save the trained model to disk using pickle.

        Args:
            filepath: Path where to save the model

        Raises:
            ValueError: If model is not trained yet
            IOError: If file cannot be written
        """
        if not self._is_trained:
            raise ValueError("Model is not trained yet. Cannot save untrained model.")

        try:
            with open(filepath, 'wb') as f:
                # Save entire object state
                pickle.dump({
                    'pipeline': self.pipeline,
                    'classes_': self.classes_,
                    '_is_trained': self._is_trained
                }, f)
        except Exception as e:
            raise IOError(f"Failed to save model to {filepath}: {str(e)}")

    @classmethod
    def load(cls, filepath: str) -> 'TextClassifier':
        """
        Load a trained model from disk.

        Args:
            filepath: Path to the saved model file

        Returns:
            TextClassifier instance with loaded model

        Raises:
            IOError: If file cannot be read or is invalid
        """
        try:
            with open(filepath, 'rb') as f:
                state = pickle.load(f)

            # Create new instance and restore state
            instance = cls()
            instance.pipeline = state['pipeline']
            instance.classes_ = state['classes_']
            instance._is_trained = state['_is_trained']

            return instance
        except Exception as e:
            raise IOError(f"Failed to load model from {filepath}: {str(e)}")

    def __repr__(self) -> str:
        """String representation of the classifier."""
        if self._is_trained:
            return (
                f"TextClassifier(trained=True, "
                f"classes={list(self.classes_) if self.classes_ is not None else None})"
            )
        return "TextClassifier(trained=False)"
