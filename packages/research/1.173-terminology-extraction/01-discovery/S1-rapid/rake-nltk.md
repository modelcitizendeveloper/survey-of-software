# RAKE-NLTK (Rapid Automatic Keyword Extraction)

## Quick Summary

Domain-independent keyword extraction using word co-occurrence and frequency analysis. NLTK-based Python implementation.

## Installation

```bash
pip install rake-nltk
```

**Dependencies**: NLTK

## Key Features

- **Domain-independent**: Works without domain-specific training
- **Co-occurrence analysis**: Identifies key phrases by analyzing word co-occurrences
- **Stopword filtering**: Uses stopwords as phrase delimiters
- **Frequency-based**: Combines word frequency and co-occurrence scores

## How It Works

1. Use stopwords to split text into candidate phrases
2. Calculate word scores based on frequency and co-occurrence
3. Compute phrase scores (sum of word scores)
4. Rank phrases by score
5. Return top-k key phrases

## Use Cases

- General-purpose keyword extraction
- Document summarization
- Content tagging
- Search engine optimization (SEO)

## Resources

- **PyPI**: [rake-nltk](https://pypi.org/project/rake-nltk/)
- **GitHub**: Multiple implementations available

## Initial Assessment

**Pros**:
- Simple, well-understood algorithm
- Fast (no ML inference)
- Domain-independent
- Works on single documents (no corpus needed)

**Cons**:
- Statistical only (no semantic understanding)
- Quality depends on stopword list
- May extract common phrases, not technical terms
- Less sophisticated than modern methods

**Recommended for**: Quick keyword extraction when you need **speed over precision**. For technical terminology extraction, pyate or KeyBERT are likely better choices.

## Note: Keyword vs Terminology Extraction

RAKE extracts **keywords/key phrases** based on statistical prominence. This differs from **terminology extraction** which targets domain-specific technical terms. RAKE may miss low-frequency but important technical terms.
