# Performance Considerations

## Historical Benchmarks

Comparison of performance across popular open source parsers shows that recent higher-order graph-based techniques can be more accurate, though somewhat slower, than constituent parsers.

For Stanford parsers on English (provides context): Charniak-Johnson reranking parser achieved 89% labeled attachment F1 score for generating Stanford Dependencies.

## Modern Approaches

Character-level parsing models and joint learning frameworks address error propagation challenges. The trend is toward:
- End-to-end neural models
- Pre-trained language model integration
- Joint task learning (segmentation + POS + parsing)

## Sources
- [A Comparison of Chinese Parsers for Stanford Dependencies](https://nlp.stanford.edu/pubs/stanford_dependencies_chinese.pdf)
- [Parsing to Stanford Dependencies: Trade-offs between speed and accuracy](https://nlp.stanford.edu/pubs/lrecstanforddeps_final_final.pdf)
