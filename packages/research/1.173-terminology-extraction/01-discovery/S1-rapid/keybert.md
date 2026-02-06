# KeyBERT

## Quick Summary

Minimal keyword/keyphrase extraction using BERT embeddings. Finds terms most semantically similar to the document.

## Installation

```bash
pip install keybert

# With optional backends:
pip install keybert[flair]  # For Flair embeddings
pip install keybert[spacy]  # For spaCy integration
pip install keybert[gensim] # For Word2Vec/Doc2Vec
pip install keybert[use]    # For Universal Sentence Encoder
```

## Key Features

- **BERT-based**: Uses transformer embeddings (captures meaning, not just counts)
- **Multilingual**: Works with many languages (via multilingual BERT models)
- **Minimal API**: Design goal was "pip install + 3 lines of code"
- **Multiple backends**: Support for sentence-transformers, Flair, spaCy, Gensim
- **Semantic similarity**: Uses cosine similarity to find terms matching document meaning

## How It Works

1. Extract document embedding with BERT
2. Extract word/phrase embeddings for n-grams
3. Calculate cosine similarity between document and candidates
4. Return top-k most similar terms

## Use Cases

- **Semantic keyword extraction**: Beyond simple frequency (meaning-based)
- **Multilingual content**: Works across many languages
- **Modern NLP pipelines**: Integrates with transformer-based workflows
- **Content tagging**: Automatic metadata generation

## Resources

- **GitHub**: [MaartenGr/KeyBERT](https://github.com/MaartenGr/KeyBERT)
- **PyPI**: [keybert](https://pypi.org/project/keybert/)
- **Docs**: [maartengr.github.io/KeyBERT](https://maartengr.github.io/KeyBERT/)

## Initial Assessment

**Pros**:
- Modern (transformer-based)
- Excellent multilingual support
- Simple API (easy to use)
- Semantic understanding (not just statistics)
- Active development (2023+)

**Cons**:
- Requires transformer models (larger memory footprint)
- Slower than statistical methods (BERT inference)
- May extract keywords, not necessarily technical terms (different goals)

**Recommended for**: Projects prioritizing **semantic understanding** over pure statistical term extraction. Best for content with semantic meaning (articles, documents) rather than highly technical terminology.

## Note on Terminology vs Keywords

KeyBERT extracts **keywords** (semantically important words) which overlaps with but differs from **terminology** (domain-specific technical terms). For pure terminology extraction, pyate may be more appropriate. KeyBERT shines when you need meaning-based extraction.
