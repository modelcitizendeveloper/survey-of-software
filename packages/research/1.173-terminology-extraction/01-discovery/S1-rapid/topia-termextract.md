# topia.termextract

## Quick Summary

Lightweight POS-based term extraction library originally from Zope project. Legacy but still functional.

## Installation

```bash
pip install topia.termextract
```

## Key Features

- Simple POS tagging algorithm (focuses on nouns)
- Statistical analysis for term strength
- Returns terms with occurrence count and strength metrics
- Configurable filter component
- Minimum occurrence threshold (default: 3 for single words)

## How It Works

1. Simple POS tagging to identify nouns
2. Statistical analysis of term frequency
3. Filter for minimum occurrence threshold
4. Return ranked terms with strength scores

## Current Status

⚠️ **Last release**: June 30, 2009 (version 1.1.0)
⚠️ **Maintenance**: Discontinued on official PyPI
✓ **Fork available**: turian/topia.termextract on GitHub (updated fork)

## Use Cases

- Lightweight keyword extraction
- Simple terminology extraction for English text
- Projects requiring minimal dependencies

## Resources

- **PyPI**: [topia.termextract](https://pypi.org/project/topia.termextract/)
- **Fork**: [turian/topia.termextract](https://github.com/turian/topia.termextract)
- **Tutorial**: [TextProcessing.org guide](https://textprocessing.org/getting-started-with-topia-termextract)

## Initial Assessment

**Pros**:
- Very lightweight
- Simple API
- Minimal dependencies
- Still works for basic use cases

**Cons**:
- Abandoned (no updates since 2009)
- Limited language support
- Simple POS tagger (less accurate than modern tools)
- No active development

**Recommended for**: Legacy projects, simple keyword extraction where modern dependencies are unwanted. **NOT recommended for new projects** (use pyate or KeyBERT instead).
