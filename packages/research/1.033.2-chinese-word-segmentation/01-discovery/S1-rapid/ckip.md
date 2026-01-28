# CKIP (Chinese Knowledge and Information Processing)

## What It Is
CKIP is a neural Chinese NLP toolkit developed by Academia Sinica (Taiwan), specializing in Traditional Chinese text processing. Open-sourced in 2019 after years as a closed academic tool, it represents modernized versions of classical CKIP tools using deep learning approaches.

**Origin**: CKIP Lab, Academia Sinica (Institute of Information Science)

## Key Characteristics

### Algorithm Foundation
- **BiLSTM with attention mechanisms** for sequence labeling
- Research published in AAAI 2020: "Why Attention? Analyze BiLSTM Deficiency and Its Remedies in the Case of NER"
- Character preservation: does not auto-delete, modify, or insert characters
- Supports indefinite sentence lengths

### Three Core Tasks
1. **Word Segmentation (WS)**: Chinese text tokenization
2. **Part-of-Speech Tagging (POS)**: Grammatical annotation
3. **Named Entity Recognition (NER)**: Entity extraction

## Speed

**Processing speed**: Not extensively benchmarked in public documentation
- GPU acceleration available via CUDA configuration
- Models are 2GB total size (includes all three tasks)
- **Typical inference**: Moderate speed (neural model overhead)

## Accuracy

### Benchmark Performance (ASBC 4.0 test split, 50,000 sentences)

| Metric | CkipTagger | CKIPWS (classic) | Jieba-zh_TW |
|--------|-----------|-----------------|-----------|
| **Word segmentation F1** | **97.33%** | 95.91% | 89.80% |
| **POS accuracy** | **94.59%** | 90.62% | — |

**Key insight**: 7.5 percentage point improvement over Jieba for Traditional Chinese

## Ease of Use

### Installation
```bash
python -m pip install -U pip
python -m pip install ckiptagger
```

### Model Download (2GB, one-time)
```python
# Multiple mirrors available
wget http://ckip.iis.sinica.edu.tw/data/ckiptagger/data.zip
```

### Basic Usage
```python
from ckiptagger import WS, POS, NER

ws = WS("./data")
pos = POS("./data")

words = ws(["他叫汤姆去拿外衣。"])
pos_tags = pos(words)
```

### Advanced Features
- **Custom dictionaries**: User-defined recommended and mandatory word lists with weights
- **Multi-task architecture**: Shared representations across WS, POS, NER
- **Flexible processing**: Can use tasks independently or together

## Maintenance

- **Status**: Actively maintained
- **Latest release**: v0.3.0 (July 2025)
- **Community**: 1,674 GitHub stars, 936 weekly downloads on PyPI
- **Development**: Maintained by Peng-Hsuan Li and Wei-Yun Ma at CKIP Lab

## Best For

- **Traditional Chinese text** (Taiwan, Hong Kong, historical texts)
- **High-accuracy requirements** where precision matters most
- **Academic and research applications** with established benchmarks
- **Multi-task pipelines** requiring WS + POS + NER together
- **Government and institutional applications** in Taiwan

## Limitations

- Primarily optimized for **Traditional Chinese** (less emphasis on Simplified)
- **Large model size** (2GB download required)
- **GPU recommended** for reasonable performance on large corpora
- **Slower than Jieba** due to neural architecture overhead
- **Licensing**: GNU GPL v3.0 (copyleft - derivative works must use same license)

## Key Differentiator

**Highest accuracy for Traditional Chinese** among widely available open-source tools, with strong institutional backing from Taiwan's premier research institution.

## References

- [GitHub Repository](https://github.com/ckiplab/ckiptagger)
- [PyPI Package](https://pypi.org/project/ckiptagger/)
- [CKIP Lab Demo](https://ckip.iis.sinica.edu.tw/demo/)
- [Technical Paper (AAAI 2020)](https://ojs.aaai.org/index.php/AAAI/article/view/6338)
- [Python Implementation Guide](https://alvinntnu.github.io/python-notes/corpus/ckiptagger.html)
