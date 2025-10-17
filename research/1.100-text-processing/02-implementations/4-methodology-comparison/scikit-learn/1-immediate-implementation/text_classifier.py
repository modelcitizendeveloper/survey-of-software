"""
scikit-learn Text Classification - Method 1: Immediate Implementation
Get something working quickly with minimal planning.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import joblib
from typing import List, Dict


class SklearnQuickClassifier:
    """Quick and dirty sklearn text classifier."""

    def __init__(self):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words='english')),
            ('classifier', LogisticRegression(random_state=42))
        ])
        self.is_trained = False
        self.classes = []

    def train(self, texts: List[str], labels: List[str]) -> Dict:
        """Train the classifier quickly."""
        X = np.array(texts)
        y = np.array(labels)

        # Quick validation split
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train
        self.pipeline.fit(X_train, y_train)
        self.is_trained = True
        self.classes = list(set(labels))

        # Quick validation
        val_pred = self.pipeline.predict(X_val)
        accuracy = accuracy_score(y_val, val_pred)

        return {
            'training_samples': len(X_train),
            'validation_accuracy': accuracy,
            'classes': self.classes
        }

    def predict(self, text: str) -> Dict:
        """Predict single text."""
        if not self.is_trained:
            raise ValueError("Not trained")

        prediction = self.pipeline.predict([text])[0]
        probabilities = self.pipeline.predict_proba([text])[0]
        confidence = float(np.max(probabilities))

        # Get all probabilities
        prob_dict = {}
        for cls, prob in zip(self.pipeline.classes_, probabilities):
            prob_dict[cls] = float(prob)

        return {
            'text': text,
            'predicted_label': prediction,
            'confidence': confidence,
            'probabilities': prob_dict
        }

    def predict_batch(self, texts: List[str]) -> List[Dict]:
        """Batch prediction."""
        return [self.predict(text) for text in texts]

    def save_model(self, filepath: str):
        """Save model."""
        if not self.is_trained:
            raise ValueError("Not trained")
        joblib.dump(self.pipeline, filepath)

    def load_model(self, filepath: str):
        """Load model."""
        self.pipeline = joblib.load(filepath)
        self.is_trained = True
        self.classes = list(self.pipeline.classes_)


def create_sample_data():
    """Quick sample data."""
    texts = [
        "I love this product! Amazing quality.",
        "Great service, highly recommend!",
        "Excellent experience overall.",
        "Outstanding performance, exceeded expectations.",
        "Wonderful experience, will buy again.",
        "Fantastic product, exactly what needed!",
        "Amazing quality, perfect fit.",
        "Superb customer service, very helpful.",
        "Brilliant design, love the details.",
        "Perfect solution, works flawlessly.",

        "Terrible quality, broke immediately.",
        "Poor service, very disappointed.",
        "Awful product, avoid completely.",
        "Horrible experience, slow delivery.",
        "Worst purchase ever, requesting refund.",
        "Disappointing quality, not worth price.",
        "Broken on arrival, terrible packaging.",
        "Useless product, complete failure.",
        "Bad experience, rude staff.",
        "Defective item, doesn't function.",

        "It's okay, does the job.",
        "Average quality, nothing special.",
        "Decent for the price point.",
        "Fair quality, reasonable value.",
        "Acceptable product, gets job done.",
        "Basic functionality, nothing remarkable.",
        "Standard item, meets expectations.",
        "Ordinary quality, sufficient for use.",
        "Regular product, does what it says.",
        "Standard quality, as expected."
    ]

    labels = (['positive'] * 10 + ['negative'] * 10 + ['neutral'] * 10)
    return texts, labels


if __name__ == "__main__":
    print("scikit-learn Immediate Implementation Demo")
    print("=" * 50)

    classifier = SklearnQuickClassifier()
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

    print("\n✅ Immediate Implementation Complete!")