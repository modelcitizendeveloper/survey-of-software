# LTP (Language Technology Platform)

## What It Is
LTP is a comprehensive Chinese NLP toolkit developed by Harbin Institute of Technology, providing six fundamental NLP tasks in an integrated platform. Unlike competitors that focus solely on segmentation, LTP offers a complete pipeline from tokenization through semantic analysis.

**Origin**: Social Computing and Information Retrieval Center, HIT (HIT-SCIR)

## Key Characteristics

### Algorithm Foundation
- **Multi-task framework** with shared pre-trained model (captures cross-task knowledge)
- **Knowledge distillation**: Single-task teachers train multi-task student model
- Two architectures available:
  - **Deep Learning** (PyTorch-based, neural models)
  - **Legacy** (Perceptron-based, Rust-implemented for speed)

### Six Fundamental NLP Tasks
1. **Chinese Word Segmentation (CWS)**
2. **Part-of-Speech Tagging (POS)**
3. **Named Entity Recognition (NER)**
4. **Dependency Parsing**
5. **Semantic Dependency Parsing**
6. **Semantic Role Labeling (SRL)**

## Speed

### Deep Learning Models (PyTorch)

| Model | Speed | Model Size |
|-------|-------|-----------|
| **Base** | 39 sent/s | Largest |
| **Small** | 43 sent/s | Medium |
| **Tiny** | 53 sent/s | Smallest |

### Legacy Model (Rust)
- **21,581 sentences/second** (16-threaded)
- **3.55x faster** than previous deep learning version
- **17.17x faster** with full multithreading vs single-thread

**Key advantage**: Users choose speed/accuracy tradeoff by selecting model size

## Accuracy

### Deep Learning Models (Accuracy %)

| Model | Segmentation | POS | NER | SRL | Dependency | Semantic Dep |
|-------|-------------|-----|-----|-----|-----------|-------------|
| **Base** | **98.7** | **98.5** | 95.4 | 80.6 | 89.5 | 75.2 |
| **Small** | **98.4** | **98.2** | 94.3 | 78.4 | 88.3 | 74.7 |
| **Tiny** | 96.8 | 97.1 | 91.6 | 70.9 | 83.8 | 70.1 |

### Comparative Benchmarks (PKU Dataset)
- LTP: 88.7% F1 (segmentation)
- PKUSeg: 95.4% F1
- THULAC: 92.4% F1
- Jieba: 81.2% F1

**Note**: LTP Base model achieves **98.7% accuracy** on its benchmark datasets, but 88.7% on PKU dataset suggests dataset-specific variation.

## Ease of Use

### Installation
```bash
pip install ltp
```

### Basic Usage
```python
from ltp import LTP

# Auto-download from Hugging Face
ltp = LTP("LTP/small")

# Pipeline processing
output = ltp.pipeline(
    ["他叫汤姆去拿外衣。"],
    tasks=["cws", "pos", "ner"]
)
```

### Advanced Features
- **Hugging Face integration**: Models auto-download from Hub
- **Local model loading**: Can specify local paths
- **Multi-task processing**: Run multiple tasks in single pipeline
- **Multiple model sizes**: Base, Base1, Base2, Small, Tiny (choose speed/accuracy)
- **Language bindings**: Rust, C++, Java (beyond Python)

## Maintenance

- **Status**: Actively maintained
- **Latest version**: 4.2.0 (August 2022)
- **Community**: 5.2k GitHub stars, 1.1k forks
- **Adoption**: 1,300+ dependent projects
- **Backing**: Harbin Institute of Technology, partnerships with Baidu, Tencent
- **Proven track record**: Shared by 600+ organizations

## Best For

- **Comprehensive NLP pipelines** requiring multiple tasks (segmentation + POS + parsing + SRL)
- **Research applications** needing semantic analysis beyond tokenization
- **Projects requiring speed flexibility** (can choose Tiny for speed or Base for accuracy)
- **Enterprise deployments** needing institutional backing and proven reliability
- **Applications needing non-Python integration** (Rust, C++, Java bindings)

## Limitations

- **Licensing**: Free for universities/research; **commercial use requires license**
- **Complexity**: More features = steeper learning curve than single-task tools
- **Segmentation accuracy**: Lower than specialized tools (PKUSeg, CKIP) on some benchmarks
- **Model size**: Even "Small" model is larger than lightweight alternatives
- **Overkill for simple segmentation**: If you only need tokenization, simpler tools may suffice

## Key Differentiator

**Complete NLP ecosystem with semantic understanding**, not just segmentation. Only tool offering semantic role labeling and semantic dependency parsing in addition to basic tokenization.

## When to Choose LTP

✅ Choose if:
- Need multiple NLP tasks beyond segmentation (dependency parsing, SRL)
- Building research systems requiring semantic analysis
- Want institutional backing and proven enterprise adoption
- Need flexible speed/accuracy tradeoffs with multiple model sizes
- Require non-Python language bindings

❌ Skip if:
- Only need basic word segmentation (Jieba is faster/simpler)
- Need highest segmentation accuracy (PKUSeg/CKIP are better)
- Commercial use without budget for licensing
- Want lightest-weight dependency

## Architecture Comparison

| Aspect | Deep Learning Models | Legacy Model |
|--------|---------------------|-------------|
| Tasks | All 6 | Only 3 (CWS, POS, NER) |
| Speed | 39-53 sent/s | 21,581 sent/s |
| Accuracy | State-of-the-art | Comparable to LTP v3 |
| Use case | Research, semantic tasks | Production, high-throughput |

## References

- [GitHub Repository](https://github.com/HIT-SCIR/ltp)
- [LTP Cloud Service](https://www.ltp-cloud.com/intro_en)
- [N-LTP Research Paper (EMNLP 2021)](https://aclanthology.org/2021.emnlp-demo.6/)
- [ArXiv Paper](https://arxiv.org/abs/2009.11616)
- [Hugging Face Models](https://huggingface.co/LTP)
