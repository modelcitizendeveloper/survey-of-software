# pyate (PYthon Automated Term Extraction)

## Quick Summary

Python implementation of multiple term extraction algorithms using spaCy POS tagging. Supports spaCy v3.

## Installation

```bash
pip3 install pyate
```

**Dependencies**: numpy, pandas, spacy, pyahocorasick

## Key Features

- Multiple algorithms: C-Value, Basic, Combo Basic, Weirdness, Term Extractor
- spaCy integration via `add_pipe` method
- Returns "termhood" scores indicating confidence
- Works with spaCy v3 (for v2, use pyate==0.4.3)

## How It Works

1. Uses spaCy POS tagging to identify term candidates
2. Applies statistical algorithms to score candidates
3. Returns ranked list of terms with confidence scores

## Use Cases

- Technical documentation term extraction
- Domain-specific terminology identification
- Translation memory creation
- Glossary generation

## Resources

- **GitHub**: [kevinlu1248/pyate](https://github.com/kevinlu1248/pyate)
- **PyPI**: [pyate](https://pypi.org/project/pyate/)
- **Docs**: https://kevinlu1248.github.io/pyate/
- **Demo**: https://pyate-demo.herokuapp.com/

## Initial Assessment

**Pros**:
- Modern (spaCy v3 support)
- Multiple algorithms in one package
- Active development
- Good documentation

**Cons**:
- Requires spaCy (heavier dependency)
- Limited to languages spaCy supports

**Recommended for**: Technical writing, domain-specific NLP projects requiring modern spaCy integration
