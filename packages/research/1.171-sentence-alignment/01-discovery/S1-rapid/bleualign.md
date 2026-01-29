# Bleualign

## What It Is
Bleualign is a sentence alignment tool that uses the BLEU metric to align parallel sentences by leveraging machine translation output. Unlike traditional length-based methods, it uses MT quality assessment to find optimal alignments.

**Origin**: Developed by Rico Sennrich, widely used in neural MT research

## Key Characteristics

### Algorithm Foundation
- **BLEU-based alignment**: Uses BLEU score between source and MT output
- **MT-assisted**: Requires a translation system (Moses, neural MT, or third-party API)
- **Dynamic programming**: Finds optimal alignment path maximizing BLEU
- **Semantic awareness**: Captures meaning similarity, not just length correlation

### Alignment Strategy
1. **Translate source to target language** (or vice versa)
2. **Compute BLEU scores** between MT output and reference sentences
3. **Dynamic programming search** for best alignment path
4. **Handle 1-to-many and many-to-1** alignments

## Speed

- **Slower than Hunalign**: Bottlenecked by MT translation step
- **Translation-dependent**: Speed varies by MT system used
- **Typical throughput**: ~1K-10K sentence pairs per minute (with fast MT)
- **GPU acceleration**: Can leverage neural MT on GPUs for faster processing

## Accuracy

### Benchmark Performance
- **F1 scores**: 90-98% on high-quality parallel corpora
- **Superior on divergent translations**: Handles paraphrases and reordering better
- **Robust to length differences**: Not fooled by length mismatches
- **MT quality matters**: Better MT → better alignment

**Tradeoff**: Higher accuracy than length-based methods, but requires MT system

## Ease of Use

### Installation
```bash
pip install bleualign
```

### Basic Usage
```python
from bleualign import align_documents

# Align using external MT
aligned = align_documents(
    source_file='source.txt',
    target_file='target.txt',
    source_to_target_translation='translated.txt'
)
```

### Requirements
- Pre-translated version of source (or target)
- Sentence-segmented text files
- MT system (Moses, Google Translate API, or any MT engine)

## Maintenance

- **Status**: Maintained, stable
- **Community**: Popular in neural MT research
- **Platform support**: Cross-platform (Python package)
- **Python versions**: Python 3.6+

## Best For

- **High-quality alignment** where accuracy is paramount
- **Divergent translations** with reordering or paraphrasing
- **Projects with MT access** (API or local system)
- **Research applications** requiring precise alignments
- **Non-parallel or comparable corpora** (with appropriate MT)

## Limitations

- Requires MT system (adds complexity and cost)
- Slower than pure statistical methods
- MT quality directly impacts alignment quality
- Overkill for simple, well-formed parallel texts

## References

- [GitHub Repository](https://github.com/rsennrich/Bleualign)
- [Original Paper](https://aclanthology.org/E12-1021/)
- [BLEU Metric](https://aclanthology.org/P02-1040/)
