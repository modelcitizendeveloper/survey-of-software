# S2 Comprehensive Research: Approach

## Goal

Deep technical analysis of pyate and KeyBERT to understand:
1. Algorithm implementation details
2. Performance characteristics and benchmarks
3. Multilingual support (especially CJK - per research label)
4. Integration patterns and dependencies
5. Use case fit (terminology vs keyword extraction)

## Research Method

1. **Algorithm Analysis**: Study implementations of C-Value, Combo Basic (pyate) vs BERT embeddings + cosine similarity (KeyBERT)
2. **Benchmark Review**: Find published comparisons and performance data
3. **CJK Support**: Evaluate Chinese, Japanese, Korean language capabilities
4. **Integration Patterns**: Understand how each integrates with NLP pipelines (spaCy, sentence-transformers)
5. **Use Case Mapping**: Clarify when to use terminology extraction vs keyword extraction

## Key Questions to Answer

### For pyate:
- How do C-Value, Combo Basic, and Weirdness algorithms compare?
- What are spaCy model dependencies for CJK languages?
- Does it have general domain corpora for Chinese, Japanese, Korean?
- What is the precision of different algorithms per Astrakhantsev 2016?

### For KeyBERT:
- Which sentence-transformers models support CJK best?
- How does BERT handle CJK tokenization (character-based vs word-based)?
- What is the trade-off between multilingual-BERT and language-specific models?
- Is there semantic understanding of technical terminology or just keywords?

### For Both:
- What is the fundamental difference between terminology and keyword extraction?
- Which is better for translation workflows?
- Which is better for technical writing glossary generation?
- What are the memory/compute requirements?

## Sources

- PyATE GitHub and documentation
- KeyBERT GitHub and documentation
- Astrakhantsev 2016 (ATR4S toolkit benchmark)
- Sentence-transformers model documentation
- spaCy language model documentation
- Research papers on terminology vs keyword extraction

## Expected Outcome

Clear technical comparison with recommendations for:
1. **Pure terminology extraction** (technical terms, domain-specific concepts)
2. **Semantic keyword extraction** (meaning-based content tagging)
3. **CJK language support** (Chinese, Japanese, Korean capabilities)
4. **Integration patterns** (when to use with spaCy, sentence-transformers)
