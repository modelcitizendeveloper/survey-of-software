# Jieba (结巴中文分词)

## What It Is
Jieba is the most popular Python library for Chinese word segmentation, with 34.7k GitHub stars. Described by its creators as aiming to be "the best Python Chinese word segmentation module," it's widely adopted for its ease of use and versatility.

**Origin**: Community-developed open-source project (fxsjy/jieba)

## Key Characteristics

### Algorithm Foundation
- **Prefix dictionary** for directed acyclic graph (DAG) construction
- **Dynamic programming** for optimal path selection
- **Hidden Markov Model (HMM)** with Viterbi algorithm for unknown word discovery
- Trie tree structure for efficient word graph scanning

### Four Segmentation Modes
1. **Precise mode**: Default mode for text analysis (most accurate)
2. **Full mode**: Scans all possible words (faster but less precise)
3. **Search engine mode**: Fine-grained segmentation optimized for indexing
4. **Paddle mode**: Deep learning-based (requires paddlepaddle-tiny)

## Speed

Test hardware: Intel Core i7-2600 CPU @ 3.4GHz
- **Full mode**: 1.5 MB/second
- **Default mode**: 400 KB/second
- **Parallel processing**: 3.3x speedup on 4-core Linux (multiprocessing module)

## Accuracy

### Comparative Benchmarks
From research studies comparing major toolkits:
- **F-measure ranking**: LTP > ICTCLAS > THULAC > Jieba
- **Typical scores**: 81-89% F1 on standard datasets (MSRA, CTB, PKU)
- **Notable**: Largest accuracy gap compared to specialized academic tools

**Tradeoff**: Jieba prioritizes speed and ease of use over maximum accuracy

## Ease of Use

### Installation
```bash
pip install jieba
```

### Basic Usage
```python
import jieba
seg_list = jieba.cut("我爱北京天安门")
print(" ".join(seg_list))
```

### Advanced Features
- **Lazy loading**: Dictionaries load on first use (reduces startup time)
- **Custom dictionaries**: Easy to add domain-specific terms
- **TF-IDF and TextRank**: Built-in keyword extraction
- **POS tagging**: Part-of-speech annotation available
- **Traditional Chinese support**: Works with Traditional characters

## Maintenance

- **Status**: Actively maintained
- **Community**: 34.7k stars, 6.7k forks on GitHub
- **Platform support**: Windows, Linux, macOS
- **Python versions**: Python 2.x and 3.x

## Best For

- **General-purpose Chinese segmentation** where speed matters
- **Rapid prototyping** and getting started quickly
- **Applications with mixed Simplified/Traditional Chinese**
- **Keyword extraction** and text analysis pipelines
- **Projects requiring custom dictionaries**

## Limitations

- Lower accuracy than specialized academic tools (LTP, CKIP, PKUSEG)
- No domain-specific models (uses single general-purpose approach)
- Parallel processing not available on Windows

## References

- [GitHub Repository](https://github.com/fxsjy/jieba)
- [PyPI Package](https://pypi.org/project/jieba/)
- [Performance Comparison Study](https://zhuanlan.zhihu.com/p/64409753)
- [Jieba Technical Analysis](https://www.oreateai.com/blog/principles-of-chinese-word-segmentation-and-indepth-analysis-of-jieba-segmentation-technology/9ccbdeec1568de03098ec714f4be5270)
