"""
scikit-learn Text Classification - Method 2: Specification-Driven Implementation
Enterprise-grade implementation following detailed specifications.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
import time
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class TrainingMetrics:
    """Comprehensive training metrics for enterprise monitoring."""
    training_samples: int
    validation_samples: int
    validation_accuracy: float
    cross_validation_mean: float
    feature_count: int
    classes: List[str]
    training_time: float


@dataclass
class ClassificationResult:
    """Complete classification result with metadata."""
    text: str
    predicted_label: str
    confidence: float
    probabilities: Dict[str, float]
    feature_count: int


class SklearnEnterpriseClassifier:
    """
    Enterprise-grade scikit-learn text classifier with comprehensive
    error handling, validation, and monitoring capabilities.
    """

    def __init__(self,
                 max_features: int = 10000,
                 ngram_range: tuple = (1, 2),
                 algorithm: str = 'logistic_regression'):
        """
        Initialize classifier with enterprise configuration.

        Args:
            max_features: Maximum number of TF-IDF features
            ngram_range: N-gram range for feature extraction
            algorithm: Classification algorithm ('logistic_regression', 'svm')
        """
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.algorithm = algorithm

        # Initialize components with enterprise-grade configuration
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            stop_words='english',
            lowercase=True,
            strip_accents='unicode',
            sublinear_tf=True,  # Better for large documents
            min_df=1,  # Handle small datasets
            max_df=0.95  # Remove very common terms
        )

        if algorithm == 'logistic_regression':
            self.classifier = LogisticRegression(
                random_state=42,
                max_iter=1000,
                class_weight='balanced',  # Handle imbalanced data
                solver='liblinear'  # Good for small-medium datasets
            )
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        self.pipeline = Pipeline([
            ('vectorizer', self.vectorizer),
            ('classifier', self.classifier)
        ])

        self.label_encoder = LabelEncoder()
        self.is_trained = False
        self.classes_ = None
        self.feature_count = 0

    def _validate_training_data(self, texts: List[str], labels: List[str]) -> None:
        """Comprehensive enterprise-grade input validation."""
        if not texts or not labels:
            raise ValueError("Training data cannot be empty")

        if len(texts) != len(labels):
            raise ValueError(f"Data length mismatch: {len(texts)} texts vs {len(labels)} labels")

        if len(texts) < 10:
            raise ValueError(f"Insufficient training data: {len(texts)} samples (minimum 10 required)")

        # Validate text content
        empty_texts = sum(1 for text in texts if not text or not text.strip())
        if empty_texts > len(texts) * 0.1:  # Allow up to 10% empty
            raise ValueError(f"Too many empty texts: {empty_texts}/{len(texts)}")

        # Validate class distribution
        unique_labels = set(labels)
        if len(unique_labels) < 2:
            raise ValueError("Need at least 2 classes for classification")

        # Check minimum samples per class for robust validation
        label_counts = pd.Series(labels).value_counts()
        min_samples_per_class = max(3, len(texts) // (len(unique_labels) * 10))
        insufficient_classes = label_counts[label_counts < min_samples_per_class]

        if not insufficient_classes.empty:
            raise ValueError(f"Classes with insufficient samples: {insufficient_classes.to_dict()}")

    def _preprocess_texts(self, texts: List[str]) -> List[str]:
        """Enterprise-grade text preprocessing."""
        processed = []
        for text in texts:
            if not text:
                processed.append("")
                continue

            # Normalize text
            clean_text = str(text).strip()
            # Remove excessive whitespace
            clean_text = ' '.join(clean_text.split())
            processed.append(clean_text)

        return processed

    def train(self, texts: List[str], labels: List[str]) -> TrainingMetrics:
        """
        Train classifier with enterprise-grade validation and monitoring.

        Args:
            texts: Training text samples
            labels: Corresponding class labels

        Returns:
            Comprehensive training metrics

        Raises:
            ValueError: For invalid input data
            RuntimeError: For training failures
        """
        start_time = time.time()

        # Comprehensive validation
        self._validate_training_data(texts, labels)

        # Preprocess data
        processed_texts = self._preprocess_texts(texts)

        try:
            # Prepare data
            X = np.array(processed_texts)
            y = np.array(labels)

            # Encode labels
            y_encoded = self.label_encoder.fit_transform(y)
            self.classes_ = self.label_encoder.classes_

            # Create stratified train/validation split
            X_train, X_val, y_train, y_val = train_test_split(
                X, y_encoded,
                test_size=0.2,
                random_state=42,
                stratify=y_encoded
            )

            # Train pipeline
            self.pipeline.fit(X_train, y_train)

            # Validation metrics
            val_predictions = self.pipeline.predict(X_val)
            validation_accuracy = accuracy_score(y_val, val_predictions)

            # Cross-validation for robust assessment
            cv_scores = cross_val_score(
                self.pipeline, X_train, y_train,
                cv=min(5, len(X_train) // 10),  # Adaptive CV folds
                scoring='accuracy'
            )
            cv_mean = float(np.mean(cv_scores))

            # Feature count
            self.feature_count = len(self.pipeline.named_steps['vectorizer'].get_feature_names_out())

            # Update state
            self.is_trained = True
            training_time = time.time() - start_time

            return TrainingMetrics(
                training_samples=len(X_train),
                validation_samples=len(X_val),
                validation_accuracy=validation_accuracy,
                cross_validation_mean=cv_mean,
                feature_count=self.feature_count,
                classes=list(self.classes_),
                training_time=training_time
            )

        except Exception as e:
            self.is_trained = False
            raise RuntimeError(f"Training failed: {str(e)}")

    def predict(self, text: str) -> ClassificationResult:
        """
        Enterprise-grade single text prediction with comprehensive result.

        Args:
            text: Input text to classify

        Returns:
            Complete classification result with metadata

        Raises:
            ValueError: If model not trained
            RuntimeError: For prediction failures
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        try:
            # Preprocess input
            processed_text = self._preprocess_texts([text])[0]

            # Get prediction and probabilities
            prediction_encoded = self.pipeline.predict([processed_text])[0]
            probabilities = self.pipeline.predict_proba([processed_text])[0]

            # Convert back to original label
            predicted_label = self.label_encoder.inverse_transform([prediction_encoded])[0]
            confidence = float(np.max(probabilities))

            # Build complete probability distribution
            prob_dict = {}
            for label, prob in zip(self.classes_, probabilities):
                prob_dict[label] = float(prob)

            return ClassificationResult(
                text=text,
                predicted_label=predicted_label,
                confidence=confidence,
                probabilities=prob_dict,
                feature_count=self.feature_count
            )

        except Exception as e:
            raise RuntimeError(f"Prediction failed: {str(e)}")

    def predict_batch(self, texts: List[str]) -> List[ClassificationResult]:
        """
        Efficient batch prediction with enterprise error handling.

        Args:
            texts: List of texts to classify

        Returns:
            List of classification results
        """
        if not texts:
            return []

        try:
            # Preprocess all texts
            processed_texts = self._preprocess_texts(texts)

            # Batch prediction for efficiency
            predictions_encoded = self.pipeline.predict(processed_texts)
            probabilities = self.pipeline.predict_proba(processed_texts)

            # Convert predictions back to labels
            predicted_labels = self.label_encoder.inverse_transform(predictions_encoded)

            # Build results
            results = []
            for i, (original_text, predicted_label) in enumerate(zip(texts, predicted_labels)):
                confidence = float(np.max(probabilities[i]))

                prob_dict = {}
                for label, prob in zip(self.classes_, probabilities[i]):
                    prob_dict[label] = float(prob)

                results.append(ClassificationResult(
                    text=original_text,
                    predicted_label=predicted_label,
                    confidence=confidence,
                    probabilities=prob_dict,
                    feature_count=self.feature_count
                ))

            return results

        except Exception as e:
            raise RuntimeError(f"Batch prediction failed: {str(e)}")

    def save_model(self, filepath: str) -> None:
        """Save model with enterprise validation."""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")

        try:
            # Prepare model data
            model_data = {
                'pipeline': self.pipeline,
                'label_encoder': self.label_encoder,
                'classes': self.classes_,
                'feature_count': self.feature_count,
                'config': {
                    'max_features': self.max_features,
                    'ngram_range': self.ngram_range,
                    'algorithm': self.algorithm
                }
            }

            joblib.dump(model_data, filepath)

        except Exception as e:
            raise RuntimeError(f"Failed to save model: {str(e)}")

    def load_model(self, filepath: str) -> None:
        """Load model with enterprise validation."""
        try:
            model_data = joblib.load(filepath)

            # Restore model state
            self.pipeline = model_data['pipeline']
            self.label_encoder = model_data['label_encoder']
            self.classes_ = model_data['classes']
            self.feature_count = model_data['feature_count']

            # Restore configuration
            config = model_data['config']
            self.max_features = config['max_features']
            self.ngram_range = config['ngram_range']
            self.algorithm = config['algorithm']

            self.is_trained = True

        except Exception as e:
            self.is_trained = False
            raise RuntimeError(f"Failed to load model: {str(e)}")

    def get_feature_importance(self, top_n: int = 20) -> Dict[str, List[tuple]]:
        """Get feature importance analysis for model interpretability."""
        if not self.is_trained:
            raise ValueError("Model must be trained to get feature importance")

        try:
            feature_names = self.pipeline.named_steps['vectorizer'].get_feature_names_out()
            coefficients = self.pipeline.named_steps['classifier'].coef_

            importance_dict = {}

            if len(self.classes_) == 2:
                # Binary classification
                coef = coefficients[0]
                top_positive_idx = np.argsort(coef)[-top_n:][::-1]
                top_negative_idx = np.argsort(coef)[:top_n]

                importance_dict[self.classes_[1]] = [
                    (feature_names[idx], float(coef[idx])) for idx in top_positive_idx
                ]
                importance_dict[self.classes_[0]] = [
                    (feature_names[idx], float(coef[idx])) for idx in top_negative_idx
                ]
            else:
                # Multi-class classification
                for i, class_name in enumerate(self.classes_):
                    coef = coefficients[i]
                    top_idx = np.argsort(np.abs(coef))[-top_n:][::-1]
                    importance_dict[class_name] = [
                        (feature_names[idx], float(coef[idx])) for idx in top_idx
                    ]

            return importance_dict

        except Exception as e:
            raise RuntimeError(f"Feature importance analysis failed: {str(e)}")


def create_sample_data():
    """Generate enterprise-grade sample dataset."""
    texts = [
        # Positive sentiment - diverse expressions
        "I absolutely love this product! Outstanding quality and performance throughout.",
        "Fantastic experience that exceeded all my expectations completely and thoroughly.",
        "Brilliant design with amazing attention to detail in every aspect.",
        "Superb customer service with incredibly helpful and responsive team members.",
        "Perfect solution that works flawlessly every single time without issues.",
        "Excellent quality with fast delivery, very satisfied customer experience.",
        "Wonderful experience overall, will definitely purchase again very soon.",
        "Great service and highly recommend to everyone I know personally.",
        "Amazing product quality, exactly what I needed for my specific project.",
        "Outstanding performance that truly exceeded my high expectations significantly.",

        # Negative sentiment - varied expressions
        "Terrible quality that broke immediately after first use. Complete waste of money.",
        "Horrible experience with slow delivery and damaged packaging throughout process.",
        "Awful product that doesn't work as advertised. Avoid at all costs.",
        "Poor customer service, very disappointed with entire experience overall.",
        "Worst purchase decision ever, requesting immediate full refund today.",
        "Disappointing quality, definitely not worth the high price paid.",
        "Broken on arrival due to terrible packaging and careless handling.",
        "Useless product design, complete failure and waste of valuable time.",
        "Bad experience overall with rude staff and poor service quality.",
        "Defective item that doesn't function as described in online documentation.",

        # Neutral sentiment - balanced expressions
        "Acceptable product that gets the basic job done adequately without issues.",
        "Average quality item, meets minimum requirements without exceeding them.",
        "Standard functionality provided, nothing remarkable but works as expected.",
        "Decent enough solution, works fine for simple everyday tasks.",
        "Fair quality construction, reasonable value for the money spent.",
        "Basic product design, sufficient for general use cases.",
        "Ordinary quality level, meets expectations for this specific price point.",
        "Regular item that does what it says without major problems.",
        "Standard quality construction, as expected for this price range.",
        "It's okay overall, nothing special but does work properly."
    ]

    labels = (['positive'] * 10 + ['negative'] * 10 + ['neutral'] * 10)
    return texts, labels


if __name__ == "__main__":
    print("scikit-learn Specification-Driven Implementation Demo")
    print("=" * 60)

    try:
        # Initialize enterprise classifier
        classifier = SklearnEnterpriseClassifier()

        # Generate sample data
        texts, labels = create_sample_data()
        print(f"Created enterprise dataset: {len(texts)} samples")

        # Train with comprehensive metrics
        print("\nTraining enterprise model...")
        metrics = classifier.train(texts, labels)

        print(f"Training completed successfully:")
        print(f"  - Training samples: {metrics.training_samples}")
        print(f"  - Validation samples: {metrics.validation_samples}")
        print(f"  - Validation accuracy: {metrics.validation_accuracy:.3f}")
        print(f"  - Cross-validation mean: {metrics.cross_validation_mean:.3f}")
        print(f"  - Feature count: {metrics.feature_count:,}")
        print(f"  - Classes: {metrics.classes}")
        print(f"  - Training time: {metrics.training_time:.2f}s")

        # Test enterprise predictions
        test_cases = [
            "This is absolutely fantastic and amazing!",
            "Really disappointed with this terrible purchase.",
            "It's an acceptable solution for basic needs.",
            ""  # Edge case: empty string
        ]

        print("\nEnterprise prediction testing:")
        for text in test_cases:
            try:
                result = classifier.predict(text)
                display_text = text if text else "(empty string)"
                print(f"  '{display_text}' → {result.predicted_label} (confidence: {result.confidence:.3f})")
            except Exception as e:
                print(f"  Error predicting '{text}': {e}")

        # Feature importance analysis
        print("\nFeature importance analysis:")
        try:
            importance = classifier.get_feature_importance(top_n=5)
            for class_name, features in importance.items():
                top_features = [f[0] for f in features[:3]]
                print(f"  {class_name}: {top_features}")
        except Exception as e:
            print(f"  Feature importance error: {e}")

        print("\n✅ Specification-Driven Implementation Complete!")
        print("Enterprise-grade validation and monitoring successful.")

    except Exception as e:
        print(f"\n❌ Enterprise implementation failed: {e}")
        raise