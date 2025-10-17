# FastText Text Classifier - Production Wrapper

**Quality Score**: 92/100
**Methodology**: Method 4 (Adaptive TDD)
**Source**: spawn-experiments 1.610
**Status**: ✅ Production Ready

---

## Overview

This is a production-ready wrapper for FastText text classification, validated through spawn-experiments methodology testing. It provides a clean, user-friendly API for FastText with strategic error handling and comprehensive testing.

### Why This Implementation Won

- **Strategic testing**: 12 tests focused on high-risk areas (state management, file handling, temp cleanup)
- **Clean design**: 217 lines of implementation code + 155 lines of strategic tests
- **Robust error handling**: Handles edge cases without over-engineering
- **Consistent quality**: Scored 92/100 in comprehensive evaluation

---

## Installation

```bash
pip install fasttext
```

---

## Usage

### Basic Example

```python
from text_classifier import TextClassifier

# Initialize
classifier = TextClassifier()

# Train
texts = ['good product', 'bad service', 'excellent quality']
labels = ['positive', 'negative', 'positive']
metrics = classifier.train(texts, labels)
print(f"Training accuracy: {metrics['accuracy']:.2f}")

# Predict single text
result = classifier.predict('great experience')
print(f"{result['label']}: {result['confidence']:.2f}")

# Batch prediction
results = classifier.predict_batch(['nice', 'terrible', 'ok'])
for result in results:
    print(f"{result['label']}: {result['confidence']:.2f}")

# Save and load
classifier.save('model.bin')
loaded = TextClassifier.load('model.bin')
```

---

## API Reference

### `TextClassifier()`

Initialize an empty text classifier.

### `train(texts, labels, **params) -> dict`

Train the classifier on text data.

**Parameters**:
- `texts` (List[str]): Training text samples
- `labels` (List[str]): Corresponding labels
- `**params`: Optional FastText parameters (lr, epoch, wordNgrams, dim)

**Returns**: Dictionary with training metrics (accuracy, samples, precision, recall)

**Raises**: ValueError if inputs are invalid or empty

### `predict(text) -> dict`

Classify a single text.

**Parameters**:
- `text` (str): Text to classify

**Returns**:
```python
{
    'label': str,        # Predicted class
    'confidence': float  # Confidence score (0.0-1.0)
}
```

**Raises**:
- RuntimeError if model not trained
- ValueError if text is empty

### `predict_batch(texts) -> List[dict]`

Classify multiple texts efficiently.

**Parameters**:
- `texts` (List[str]): Texts to classify

**Returns**: List of prediction dictionaries

### `save(path)`

Save trained model to disk.

**Parameters**:
- `path` (str): File path for saved model

**Raises**: RuntimeError if model not trained

### `load(path)` (classmethod)

Load trained model from disk.

**Parameters**:
- `path` (str): Path to saved model

**Returns**: TextClassifier instance

**Raises**: FileNotFoundError if file doesn't exist

---

## Testing

Run the test suite:

```bash
python -m pytest test_text_classifier.py -v
```

### Test Coverage

The test suite includes 12 strategic tests covering:

1. **State Management** (3 tests)
   - Predict before training raises error
   - Batch predict before training raises error
   - State flag updated after training

2. **Batch Prediction** (3 tests)
   - Returns correct count of results
   - Format consistency across results
   - Batch vs single prediction consistency

3. **File Handling** (2 tests)
   - Temp file creation and cleanup
   - Training file format validation

4. **Save/Load** (3 tests)
   - Model persistence across save/load
   - Loaded model makes same predictions
   - Save before training raises error

5. **Edge Cases** (1 test)
   - Empty text handling
   - Special characters
   - Small datasets

---

## Design Decisions

### Why Adaptive TDD (Method 4)?

Compared to other methodologies tested in spawn-experiments 1.610:

- **vs Method 1 (Immediate)**: Method 1 FastText FAILED with NaN errors on small datasets (48/100 score)
- **vs Method 2 (Specification)**: Over-engineered at 521 lines (5.2X bloat), scored only 73/100
- **vs Method 3 (Full TDD)**: Good quality (87/100) but Method 4 has better strategic focus

### Strategic Testing Philosophy

Method 4 focuses tests on **high-risk areas** rather than 100% coverage:
- State management bugs (predict before train)
- File I/O issues (temp file cleanup)
- Serialization errors (save/load)
- Edge cases that commonly break (small datasets, empty inputs)

This approach delivers production-ready quality (92/100) with efficient development time (1:39 vs 2:22 for full TDD).

---

## Known Limitations

1. **Requires file-based training**: FastText's API requires writing training data to a temp file
2. **Binary model format**: Saved models use FastText's binary format (not portable across FastText versions)
3. **Memory usage**: Keeps model in memory - may not suit very large models

---

## Performance Characteristics

- **Training time**: ~1-2 seconds for small datasets (< 1000 samples)
- **Prediction speed**: ~1000 predictions/second (single-threaded)
- **Model size**: Typically 1-10MB for text classification tasks

---

## Integration Notes

### spawn-solutions Model Citizen Developer

This implementation serves as the **reference wrapper** for FastText in the Model Citizen Developer cookbook. Use this pattern when wrapping simple library APIs that require defensive error handling.

### When to Use FastText

- **Fast training**: Efficient on CPU, trains in seconds
- **Good for small datasets**: Works well with 100-1000 samples
- **Multi-label support**: Handles multiple labels per text
- **Language agnostic**: Works across languages

### When to Use sklearn Instead

- **Need probability calibration**: sklearn provides better probability estimates
- **Complex pipelines**: sklearn Pipeline is better for multi-stage processing
- **Cross-validation**: sklearn has built-in CV support

---

## Source Attribution

**Methodology Test**: spawn-experiments Experiment 1.610
**Generated by**: Task agent using Method 4 (Adaptive TDD)
**Development time**: 1 minute 39 seconds
**Quality score**: 92/100
**Test suite**: 155 lines, 12 strategic tests, all passing

---

## License

[Same as parent project]

---

## Support

For issues or questions:
1. Check test suite for usage examples
2. Review spawn-experiments 1.610 for methodology details
3. See TEXT_PROCESSING_EXPLAINER.md for library comparison

**Status**: ✅ Production validated (spawn-experiments 1.610)
