# textacy

## Quick Summary

Higher-level NLP library built on spaCy, providing tools for tasks like keyphrase extraction, readability analysis, and more.

## Installation

```bash
pip install textacy
```

**Dependencies**: spaCy (and language models)

## Key Features

- **Built on spaCy**: Extends spaCy with higher-level tasks
- **Keyphrase extraction**: Via textacy.extract using TextRank algorithm
- **Preprocessing tools**: Text normalization, cleaning
- **Multiple extraction methods**: Named entities, n-grams, terms, etc.
- **Corpus management**: Tools for working with document collections

## How It Works (for term extraction)

Uses `textacy.extract` module:
- TextRank algorithm for keyphrase ranking
- Various extraction methods (n-grams, entities, terms)
- Statistical ranking of extracted phrases

## Use Cases

- Projects already using spaCy that need higher-level features
- Keyphrase extraction with TextRank
- Text preprocessing pipeline
- Corpus-level analysis

## Resources

- **GitHub**: [chartbeat-labs/textacy](https://github.com/chartbeat-labs/textacy)
- **Docs**: [textacy.readthedocs.io](https://textacy.readthedocs.io/)
- **PyPI**: `pip install textacy`

## Initial Assessment

**Pros**:
- Convenient if already using spaCy
- Multiple extraction methods in one library
- Good documentation
- TextRank implementation

**Cons**:
- Requires spaCy (heavier dependency)
- Less focused than specialized tools (pyate, KeyBERT)
- May be overkill if you only need term extraction

**Recommended for**: Projects **already using spaCy** that want additional NLP features including term extraction. If starting fresh, consider pyate (also spaCy-based but focused on term extraction) or KeyBERT (semantic approach).

## Comparison to pyate

Both build on spaCy, but:
- **textacy**: General-purpose NLP toolkit with term extraction as one feature
- **pyate**: Focused specifically on terminology extraction with multiple algorithms

For **pure terminology extraction**, pyate is more specialized. For **broader NLP tasks** including term extraction, textacy provides more features.
