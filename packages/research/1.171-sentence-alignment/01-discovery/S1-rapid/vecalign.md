# vecalign

## What It Is
vecalign is a state-of-the-art multilingual sentence alignment tool from Facebook AI Research that uses dense vector representations (embeddings) to align parallel sentences. It supports 93 languages and achieves high accuracy without requiring language-specific resources.

**Origin**: Facebook AI Research (FAIR), part of the LASER ecosystem

## Key Characteristics

### Algorithm Foundation
- **Multilingual embeddings**: Uses LASER sentence embeddings
- **Cosine similarity**: Measures semantic similarity in embedding space
- **Dynamic programming**: Finds optimal alignment path
- **Language-agnostic**: No dictionaries or language-specific rules needed
- **Handles 1-to-N alignments**: Can align single sentence to multiple sentences

### Key Innovation
- **Deep semantic understanding**: Captures meaning beyond surface form
- **Zero-shot cross-lingual**: Works for language pairs never seen together
- **Length-independent**: Not biased by sentence length differences

## Speed

- **Moderate speed**: Faster than MT-based methods, slower than pure statistical
- **Embedding computation**: Main bottleneck (but can be cached)
- **GPU acceleration**: Significantly faster with GPU for embedding generation
- **Typical throughput**: ~10K-50K sentence pairs per minute (with GPU)

## Accuracy

### Benchmark Performance
- **F1 scores**: 93-99% on WMT test sets
- **State-of-the-art**: Best published results on standard benchmarks
- **Robust across languages**: Consistent performance on high/low-resource pairs
- **Handles noise**: More resilient to OCR errors, informal text

**Advantage**: Combines speed advantage of statistical methods with semantic understanding

## Ease of Use

### Installation
```bash
# Install LASER and vecalign
git clone https://github.com/thompsonb/vecalign
cd vecalign
pip install -r requirements.txt

# Download LASER models
bash download_models.sh
```

### Basic Usage
```bash
# Extract embeddings
python3 embed.py --text source.txt --lang en --output source.emb
python3 embed.py --text target.txt --lang de --output target.emb

# Align
python3 vecalign.py --src source.txt --tgt target.txt \
  --src_embed source.emb --tgt_embed target.emb \
  --alignment_max_size 8 > aligned.txt
```

### Input Requirements
- Sentence-segmented text files
- Language codes for embedding extraction
- LASER model files (downloaded once)

## Maintenance

- **Status**: Actively maintained
- **Community**: Growing adoption in MT and NLP research
- **Platform support**: Linux, macOS (GPU support via CUDA)
- **Python versions**: Python 3.6+
- **Dependencies**: PyTorch, LASER embeddings

## Best For

- **Multilingual projects** with diverse language pairs
- **Low-resource languages** without good dictionaries or MT
- **High-accuracy requirements** for research or quality data
- **Noisy or informal text** (web forums, social media)
- **Projects needing semantic alignment** beyond literal translation
- **Zero-shot alignment** for new language pairs

## Limitations

- Larger dependency footprint (PyTorch, LASER models ~1GB)
- GPU recommended for reasonable performance
- Embedding computation can be memory-intensive
- Overkill for simple European language pairs with good tools

## References

- [GitHub Repository](https://github.com/thompsonb/vecalign)
- [LASER: Language-Agnostic SEntence Representations](https://github.com/facebookresearch/LASER)
- [Original Paper](https://aclanthology.org/D19-1136/)
- [LASER Paper](https://aclanthology.org/P19-1309/)
