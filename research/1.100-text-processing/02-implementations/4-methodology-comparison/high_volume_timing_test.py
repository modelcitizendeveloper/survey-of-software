#!/usr/bin/env python3
"""
High Volume Timing Test
Test text classifiers with realistic dataset sizes to get meaningful performance comparisons.
"""

import time
import random
import statistics
from typing import List, Tuple


def generate_large_dataset(size: int = 1000) -> Tuple[List[str], List[str]]:
    """Generate a realistic dataset for timing tests."""

    # Base templates for variety
    positive_templates = [
        "I {adverb} love this {noun}! {positive_adj} quality and {positive_adj} {feature}.",
        "{positive_adj} experience that {positive_phrase}.",
        "{positive_adj} {noun} with {positive_adj} {feature}.",
        "Outstanding {noun}, {positive_phrase}.",
        "Perfect {noun} that {positive_action}.",
        "Brilliant {noun}, {positive_phrase}.",
        "Amazing {positive_adj} {noun} with {positive_feature}.",
        "Superb {noun}, {positive_phrase}.",
        "Excellent {positive_adj} {noun} and {positive_feature}.",
        "Wonderful {positive_phrase} {noun}."
    ]

    negative_templates = [
        "Terrible {negative_adj} {noun}, {negative_phrase}.",
        "Horrible {noun} with {negative_adj} {feature}.",
        "Awful {noun} that {negative_phrase}.",
        "Poor {negative_adj} {noun}, {negative_phrase}.",
        "Worst {noun} {negative_phrase}.",
        "Disappointing {negative_adj} {noun}, {negative_phrase}.",
        "Broken {noun} {negative_phrase}.",
        "Useless {noun}, {negative_phrase}.",
        "Bad {noun} with {negative_adj} {feature}.",
        "Defective {noun} that {negative_phrase}."
    ]

    neutral_templates = [
        "It's {neutral_adj}, {neutral_phrase}.",
        "{neutral_adj} {noun}, {neutral_phrase}.",
        "Standard {noun}, {neutral_phrase}.",
        "Decent {noun}, {neutral_phrase}.",
        "Fair {neutral_adj} {noun}, {neutral_phrase}.",
        "Acceptable {noun}, {neutral_phrase}.",
        "Basic {noun}, {neutral_phrase}.",
        "Regular {noun}, {neutral_phrase}.",
        "Ordinary {noun}, {neutral_phrase}.",
        "{neutral_adj} {noun} that {neutral_phrase}."
    ]

    # Vocabulary for variation
    vocab = {
        'noun': ['product', 'service', 'experience', 'item', 'purchase', 'delivery', 'quality', 'solution', 'design', 'performance'],
        'positive_adj': ['amazing', 'fantastic', 'excellent', 'outstanding', 'perfect', 'brilliant', 'superb', 'wonderful', 'great', 'incredible'],
        'negative_adj': ['terrible', 'awful', 'horrible', 'disappointing', 'poor', 'bad', 'useless', 'broken', 'defective', 'worst'],
        'neutral_adj': ['okay', 'average', 'standard', 'decent', 'fair', 'acceptable', 'basic', 'regular', 'ordinary', 'normal'],
        'adverb': ['absolutely', 'really', 'completely', 'totally', 'definitely', 'certainly', 'truly', 'genuinely', 'honestly', 'simply'],
        'feature': ['performance', 'delivery', 'packaging', 'design', 'functionality', 'interface', 'quality', 'service', 'support', 'value'],
        'positive_phrase': ['exceeded my expectations', 'works perfectly', 'highly recommend', 'very satisfied', 'will buy again', 'amazing quality', 'perfect solution', 'fantastic experience', 'brilliant design', 'outstanding performance'],
        'negative_phrase': ['complete waste of money', 'broke immediately', 'very disappointed', 'requesting refund', 'avoid at all costs', 'doesn\'t work', 'terrible experience', 'complete failure', 'not worth it', 'major problems'],
        'neutral_phrase': ['meets basic requirements', 'does the job', 'nothing special', 'as expected', 'reasonable value', 'gets job done', 'sufficient quality', 'meets expectations', 'works fine', 'decent enough'],
        'positive_action': ['works flawlessly', 'performs excellently', 'exceeds expectations', 'delivers perfectly', 'functions amazingly'],
        'positive_feature': ['incredible attention to detail', 'amazing build quality', 'perfect functionality', 'excellent performance', 'outstanding design']
    }

    def fill_template(template: str) -> str:
        """Fill a template with random vocabulary."""
        result = template
        for key, values in vocab.items():
            if f'{{{key}}}' in result:
                result = result.replace(f'{{{key}}}', random.choice(values))
        return result

    texts = []
    labels = []

    # Generate balanced dataset
    samples_per_class = size // 3

    # Positive samples
    for _ in range(samples_per_class):
        template = random.choice(positive_templates)
        text = fill_template(template)
        texts.append(text)
        labels.append('positive')

    # Negative samples
    for _ in range(samples_per_class):
        template = random.choice(negative_templates)
        text = fill_template(template)
        texts.append(text)
        labels.append('negative')

    # Neutral samples
    for _ in range(samples_per_class):
        template = random.choice(neutral_templates)
        text = fill_template(template)
        texts.append(text)
        labels.append('neutral')

    # Add remaining samples to reach exact size
    remaining = size - len(texts)
    for _ in range(remaining):
        template = random.choice(positive_templates + negative_templates + neutral_templates)
        text = fill_template(template)
        texts.append(text)
        labels.append(random.choice(['positive', 'negative', 'neutral']))

    # Shuffle to mix classes
    combined = list(zip(texts, labels))
    random.shuffle(combined)
    texts, labels = zip(*combined)

    return list(texts), list(labels)


def time_multiple_runs(func, *args, runs: int = 5):
    """Time a function over multiple runs and return statistics."""
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        result = func(*args)
        times.append(time.perf_counter() - start)

    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'min': min(times),
        'max': max(times),
        'std': statistics.stdev(times) if len(times) > 1 else 0,
        'times': times,
        'result': result  # Return last result for validation
    }


def test_classifier_performance(classifier_class, classifier_name: str, dataset_sizes: List[int]):
    """Test classifier performance across different dataset sizes."""
    print(f"\n{'='*60}")
    print(f"TESTING {classifier_name.upper()}")
    print(f"{'='*60}")

    for size in dataset_sizes:
        print(f"\nDataset Size: {size:,} samples")
        print("-" * 40)

        # Generate data
        print("Generating dataset...")
        texts, labels = generate_large_dataset(size)
        print(f"Generated {len(texts)} texts, {len(set(labels))} classes")

        # Initialize classifier
        classifier = classifier_class()

        # Time training
        print("Testing training performance...")
        train_stats = time_multiple_runs(classifier.train, texts, labels, runs=3)

        print(f"Training Times:")
        print(f"  Mean: {train_stats['mean']*1000:.1f}ms")
        print(f"  Range: {train_stats['min']*1000:.1f}ms - {train_stats['max']*1000:.1f}ms")
        print(f"  Std Dev: {train_stats['std']*1000:.1f}ms")

        # Time predictions
        test_texts = [
            "This is absolutely fantastic and amazing!",
            "Really disappointed with this terrible purchase.",
            "It's an acceptable solution for basic needs.",
            "Outstanding quality and performance throughout.",
            "Horrible experience, complete waste of money."
        ]

        print("Testing prediction performance...")

        # Single predictions
        single_times = []
        for test_text in test_texts:
            pred_stats = time_multiple_runs(classifier.predict, test_text, runs=10)
            single_times.extend(pred_stats['times'])

        print(f"Single Prediction Times (over {len(single_times)} predictions):")
        print(f"  Mean: {statistics.mean(single_times)*1000:.3f}ms")
        print(f"  Median: {statistics.median(single_times)*1000:.3f}ms")
        print(f"  Range: {min(single_times)*1000:.3f}ms - {max(single_times)*1000:.3f}ms")

        # Batch predictions
        batch_stats = time_multiple_runs(classifier.predict_batch, test_texts, runs=5)

        print(f"Batch Prediction Times ({len(test_texts)} texts):")
        print(f"  Mean: {batch_stats['mean']*1000:.1f}ms")
        print(f"  Per item: {batch_stats['mean']*1000/len(test_texts):.3f}ms")
        print(f"  Range: {batch_stats['min']*1000:.1f}ms - {batch_stats['max']*1000:.1f}ms")

        # Test a few predictions for sanity check
        print(f"\nSample Predictions:")
        for i, test_text in enumerate(test_texts[:3]):
            result = classifier.predict(test_text)
            label = result.get('predicted_label', 'unknown')
            confidence = result.get('confidence', 0.0)
            print(f"  '{test_text[:30]}...' → {label} ({confidence:.3f})")


def main():
    """Run comprehensive high-volume timing tests."""
    print("🚀 HIGH VOLUME TIMING ANALYSIS")
    print("Testing text classifiers with realistic dataset sizes")
    print("This will take several minutes to complete...")

    # Test with progressively larger datasets
    dataset_sizes = [100, 500, 1000, 2000]

    # Import and test implementations
    import sys
    import os

    # Add paths for imports
    fasttext_path = os.path.join(os.path.dirname(__file__), 'fasttext', '3-test-first-development')
    sklearn_path = os.path.join(os.path.dirname(__file__), 'scikit-learn', '3-test-first-development')

    try:
        # Test FastText TDD implementation (most reliable)
        sys.path.insert(0, fasttext_path)
        from text_classifier import FastTextTDDClassifier
        test_classifier_performance(FastTextTDDClassifier, "FastText (TDD Implementation)", dataset_sizes)
        sys.path.remove(fasttext_path)

    except Exception as e:
        print(f"❌ FastText testing failed: {e}")

    try:
        # Test scikit-learn TDD implementation (most reliable)
        sys.path.insert(0, sklearn_path)
        from text_classifier import SklearnTDDClassifier
        test_classifier_performance(SklearnTDDClassifier, "scikit-learn (TDD Implementation)", dataset_sizes[:2])  # Test smaller sizes due to numpy issues
        sys.path.remove(sklearn_path)

    except Exception as e:
        print(f"❌ scikit-learn testing failed: {e}")

    print(f"\n{'='*60}")
    print("🎯 HIGH VOLUME TIMING ANALYSIS COMPLETE")
    print("="*60)
    print("Key insights:")
    print("- Training time scales with dataset size")
    print("- Prediction time should remain constant")
    print("- Batch predictions are more efficient than individual calls")
    print("- Real-world performance includes data loading, preprocessing overhead")


if __name__ == "__main__":
    # Set random seed for reproducible results
    random.seed(42)
    main()