# Jiayan (嘉言)

## Overview

Jiayan is a Python library specifically designed for processing Classical Chinese (文言文) texts. Unlike general-purpose Chinese NLP tools, Jiayan focuses on pre-modern Chinese language processing.

## Architecture

**Type**: Specialized Classical Chinese processor
**Language**: Python 3
**Focus**: Segmentation and basic analysis of Classical Chinese
**Training Data**: Classical Chinese corpus (specific sources not fully documented)

## Core Capabilities

### Word Segmentation
- **Classical Chinese optimized**: Trained on pre-modern texts
- **Character handling**: Properly handles classical compounds
- **Function words**: Recognizes classical particles (也、矣、乎、焉、哉)
- **Quality**: Better than modern Chinese segmenters for 文言文

### Text Processing
- **Sentence splitting**: Handles classical punctuation patterns
- **Character variants**: Normalizes variant forms
- **Traditional/Simplified**: Handles both character sets
- **Idiom detection**: Recognizes classical set phrases

### Basic Analysis
- Limited POS tagging (experimental)
- Character frequency analysis
- Named entity hints (not full NER)

## Installation

```bash
pip install jiayan
```

## Usage Example

```python
import jiayan

# Initialize segmenter
segmenter = jiayan.load()

# Segment Classical Chinese text
text = "學而時習之不亦說乎"
words = segmenter.cut(text)
print(list(words))
# Output: ['學', '而', '時', '習', '之', '不', '亦', '說', '乎']

# With delimiter
result = segmenter.lcut(text)
print(' '.join(result))
# Output: "學 而 時 習 之 不 亦 說 乎"
```

## Strengths

1. **Classical Chinese focus**: Designed specifically for 文言文
2. **Easy installation**: Available via pip
3. **Lightweight**: Minimal dependencies
4. **Python-native**: Easy integration with Python workflows
5. **Better than general tools**: Outperforms modern Chinese segmenters on classical texts

## Limitations

1. **Limited functionality**: Primarily segmentation, not full parsing
2. **No dependency parsing**: Does not provide syntactic trees
3. **Minimal POS tagging**: Part-of-speech support is experimental
4. **Documentation**: Limited English documentation
5. **Maintenance**: Less active than major NLP projects
6. **No NER**: Named entity recognition not available
7. **Performance data**: Limited published benchmarks

## Comparison with Alternatives

| Feature | Jiayan | Stanford CoreNLP | ctext.org |
|---------|--------|------------------|-----------|
| Classical Chinese segmentation | ✓✓✓ Good | ✗ Poor | ✓ Basic |
| POS tagging | ✓ Limited | ✗ Inaccurate | ✗ None |
| Dependency parsing | ✗ None | ✗ Inaccurate | ✗ None |
| Ease of use (Python) | ✓✓✓ Easy | ✓ Moderate | ✓✓✓ Easy |
| Documentation | ✓ Limited | ✓✓✓ Excellent | ✓✓ Good |

## Current Status

- **Repository**: GitHub (search: jiayan python classical chinese)
- **PyPI**: Available
- **Last Update**: Check PyPI for current status
- **License**: Likely open source (verify on repository)
- **Community**: Small but specialized user base

## Use Cases

### Suitable For
- Classical Chinese text segmentation
- Preprocessing for further analysis
- Educational applications
- Research projects focused on 文言文

### Not Suitable For
- Full syntactic parsing
- Modern Chinese texts
- Named entity extraction
- Production systems requiring comprehensive NLP

## Integration Strategy

```python
# Combined pipeline: Jiayan + custom analysis
import jiayan

def analyze_classical_text(text):
    # Step 1: Segment with Jiayan
    segmenter = jiayan.load()
    words = list(segmenter.cut(text))

    # Step 2: Custom POS tagging (implement separately)
    pos_tags = custom_pos_tagger(words)

    # Step 3: Custom parsing (implement separately)
    parse_tree = custom_parser(words, pos_tags)

    return parse_tree
```

## Verdict

**Best specialized tool for Classical Chinese segmentation**, but limited to that task. Would be a valuable component in a larger Classical Chinese parsing system, but cannot handle full parsing alone. Recommended as the segmentation layer if building a custom solution.
