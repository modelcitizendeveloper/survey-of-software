# PKUSeg (Peking University Segmenter)

## What It Is
PKUSeg is a multi-domain Chinese word segmentation toolkit developed by Peking University, specializing in domain-specific segmentation. Unlike single-model toolkits, it provides separate pre-trained models optimized for different domains (news, web, medicine, tourism).

**Origin**: Language Computing Lab, Peking University (lancopku)

## Key Characteristics

### Algorithm Foundation
- **Conditional Random Field (CRF)**: Fast and high-precision model
- **Domain adaptation**: Separate models trained on domain-specific corpora
- **Research published**: Luo et al. (2019), "PKUSEG: A Toolkit for Multi-Domain Chinese Word Segmentation"

### Domain-Specific Models
1. **news**: MSRA news corpus (default)
2. **web**: Weibo social media text
3. **medicine**: Medical domain terminology
4. **tourism**: Travel and hospitality domain
5. **mixed**: General-purpose cross-domain
6. **default_v2**: Enhanced via domain adaptation techniques

## Speed

**Performance tradeoff**: Higher accuracy comes at cost of speed
- **Comparison**: "Much slower than Jieba" per multiple benchmarks
- **Batch processing**: Supports multi-threaded processing (`nthread` parameter)
- **Architecture**: Written in Python (66.6%) and Cython (33.4%) for optimization

**Typical use case**: Offline processing where accuracy > speed

## Accuracy

### Benchmark Performance

**MSRA Dataset (News Domain)**
- PKUSeg: **96.88%** F1
- THULAC: 95.71% F1
- Jieba: 88.42% F1

**Weibo Dataset (Social Media)**
- PKUSeg: **94.21%** F1
- Competitors: Lower scores

**Cross-Domain Average**
- PKUSeg default: **91.29%** F1
- THULAC: 88.08% F1
- Jieba: 81.61% F1

**Error reduction**: 79.33% on MSRA, 63.67% on CTB8 versus previous toolkits

## Ease of Use

### Installation
```bash
pip3 install pkuseg
```

### Basic Usage
```python
import pkuseg

# Default model (news domain)
seg = pkuseg.pkuseg()
text = seg.cut('我爱北京天安门')

# Domain-specific (auto-downloads model)
seg_med = pkuseg.pkuseg(model_name='medicine')

# With POS tagging
seg_pos = pkuseg.pkuseg(postag=True)

# Batch processing
pkuseg.test('input.txt', 'output.txt', nthread=20)
```

### Advanced Features
- **Automatic model download**: Fetches domain models on first use
- **User dictionaries**: Custom lexicons for domain terminology
- **POS tagging**: Simultaneous segmentation and annotation
- **Custom training**: Train models on your own annotated data
- **Mirror sources**: Tsinghua University mirror for faster downloads (China)

## Maintenance

- **Status**: Actively maintained
- **Community**: 6.7k GitHub stars, 985 forks
- **Activity**: 200+ commits with recent updates
- **Platform support**: Windows, Linux, macOS
- **Python version**: Python 3

## Best For

- **Domain-specific applications** where terminology matters (medical, legal, e-commerce)
- **High-accuracy requirements** where precision is critical
- **Social media text** (Weibo, informal Chinese)
- **Offline batch processing** where speed is not primary concern
- **Projects needing custom models** trained on proprietary data

## Limitations

- **Significantly slower than Jieba** (speed vs. accuracy tradeoff)
- **Model selection required**: Must know your domain in advance
- **Larger memory footprint**: Each domain model adds overhead
- **Python 3 only** (no Python 2 support)
- **Cold start**: First run downloads large model files

## Key Differentiator

**Highest accuracy for domain-specific Simplified Chinese text** with pre-trained models for major verticals (medicine, tourism, social media).

## When to Choose PKUSeg

✅ Choose if:
- Accuracy is paramount (medical, legal, financial applications)
- Working within a specific domain with available pre-trained model
- Processing offline/batch with no real-time constraints

❌ Skip if:
- Need real-time/low-latency segmentation
- Working with Traditional Chinese (CKIP is better)
- General-purpose text with no specific domain

## References

- [GitHub Repository](https://github.com/lancopku/pkuseg-python)
- [PyPI Package](https://pypi.org/project/pkuseg/)
- [English Documentation](https://github.com/lancopku/pkuseg-python/blob/master/readme/readme_english.md)
- [Research Paper (arXiv)](https://arxiv.org/abs/1906.11455)
- [Performance Comparison](https://github.com/EOA-AILab/Seg_Pos)
