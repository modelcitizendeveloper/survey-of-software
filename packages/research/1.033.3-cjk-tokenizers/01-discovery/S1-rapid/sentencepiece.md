# SentencePiece

**Repository:** github.com/google/sentencepiece
**Downloads/Month:** ~2.5M (PyPI, estimated)
**GitHub Stars:** 10,000+
**Last Updated:** 2025 (Active)

## Quick Assessment
- **Popularity:** High - Used by T5, ALBERT, XLNet
- **Maintenance:** Active - Google maintains
- **Documentation:** Excellent - Explicit CJK guidance

## Pros
- **Language-independent design** - No pre-tokenization required
- **Explicit CJK support** - `character_coverage=0.9995` parameter
- **Handles no-space languages** - Designed for Japanese/Chinese
- **Multiple algorithms** - BPE, unigram, char, word
- **End-to-end training** - Direct from raw text

## Cons
- Slower than tiktoken for inference
- Requires training a model (not pre-built)
- More configuration choices to understand

## Quick Take
Industry standard for CJK tokenization. Explicitly designed to handle languages without word boundaries. Gold standard for training custom tokenizers on CJK text.
