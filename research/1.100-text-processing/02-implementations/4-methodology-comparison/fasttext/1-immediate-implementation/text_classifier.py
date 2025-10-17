"""
FastText Text Classification - Method 1: Immediate Implementation
Build quickly, get something working fast.
"""

import fasttext
import tempfile
import os
from typing import List, Dict

class FastTextClassifier:
    def __init__(self):
        self.model = None
        self.temp_dir = tempfile.mkdtemp()
        self.is_trained = False

    def train(self, texts: List[str], labels: List[str]) -> Dict:
        # Create training file in FastText format
        train_file = os.path.join(self.temp_dir, 'train.txt')
        with open(train_file, 'w') as f:
            for text, label in zip(texts, labels):
                # FastText format: __label__LABEL text
                clean_text = text.replace('\n', ' ').replace('\r', ' ')
                f.write(f'__label__{label} {clean_text}\n')

        # Train model
        self.model = fasttext.train_supervised(
            input=train_file,
            lr=0.1,
            epoch=25,
            wordNgrams=2,
            dim=100,
            verbose=0
        )

        self.is_trained = True

        return {
            'training_samples': len(texts),
            'classes': list(set(labels)),
            'model_path': train_file
        }

    def predict(self, text: str) -> Dict:
        if not self.is_trained:
            raise ValueError("Model not trained")

        clean_text = text.replace('\n', ' ').replace('\r', ' ') if text else ""

        predictions = self.model.predict(clean_text, k=3)
        labels, scores = predictions

        # Extract label without __label__ prefix
        predicted_label = labels[0].replace('__label__', '') if labels else 'unknown'
        confidence = float(scores[0]) if scores else 0.0

        # Build probabilities dict
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

    def predict_batch(self, texts: List[str]) -> List[Dict]:
        return [self.predict(text) for text in texts]

    def save_model(self, filepath: str):
        if not self.is_trained:
            raise ValueError("No trained model to save")
        self.model.save_model(filepath)

    def load_model(self, filepath: str):
        self.model = fasttext.load_model(filepath)
        self.is_trained = True

    def __del__(self):
        """Cleanup temp files."""
        try:
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                import shutil
                shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass


def create_sample_data():
    texts = [
        "I love this product! It's amazing.",
        "Great service, highly recommend!",
        "Excellent quality and fast delivery.",
        "Outstanding performance, exceeded expectations.",
        "Wonderful experience, will buy again.",
        "Fantastic product, exactly what I needed!",
        "Amazing quality, perfect fit.",
        "Superb customer service, very helpful.",
        "Brilliant design, love the details.",
        "Perfect solution, works flawlessly.",

        "Terrible quality, broke after one day.",
        "Poor customer service, very disappointed.",
        "Awful product, doesn't work as advertised.",
        "Horrible experience, slow delivery.",
        "Worst purchase ever, requesting refund.",
        "Disappointing quality, not worth the price.",
        "Broken on arrival, terrible packaging.",
        "Useless product, complete failure.",
        "Bad experience, rude staff.",
        "Defective item, doesn't function properly.",

        "It's okay, nothing special but works.",
        "Average product, meets basic requirements.",
        "Standard quality, as expected for price.",
        "Decent enough, works fine for simple tasks.",
        "Fair quality, reasonable value for money.",
        "Acceptable product, gets the job done.",
        "Basic functionality, nothing remarkable.",
        "Standard item, meets expectations.",
        "Ordinary quality, sufficient for use.",
        "Regular product, does what it says."
    ]

    labels = (['positive'] * 10 + ['negative'] * 10 + ['neutral'] * 10)
    return texts, labels


if __name__ == "__main__":
    print("FastText Immediate Implementation Demo")
    print("=" * 50)

    # Create and train
    classifier = FastTextClassifier()
    texts, labels = create_sample_data()

    print(f"Training on {len(texts)} samples...")
    training_info = classifier.train(texts, labels)
    print(f"Training complete: {training_info}")

    # Test predictions
    test_texts = [
        "This is absolutely fantastic!",
        "Really disappointed with this purchase.",
        "It's an acceptable solution for basic needs.",
        ""
    ]

    print("\nTest predictions:")
    for text in test_texts:
        result = classifier.predict(text)
        print(f"'{text}' → {result['predicted_label']} ({result['confidence']:.3f})")

    print("\n✅ FastText Immediate Implementation Complete!")