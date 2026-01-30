# Implementation Patterns

## For Chinese Specifically

Chinese implementation must handle:

1. **Word Segmentation First**: Either pipeline (segment → parse) or joint (simultaneous)
2. **Encoding Choice**: Simplified vs Traditional Chinese models
3. **Domain Adaptation**: Different models for modern vs classical Chinese

## Joint vs Pipeline Approach

### Pipeline Approach
- Segment text → POS tag → Dependency parse
- Simpler but error propagation issue
- Each stage compounds errors

### Joint Approach
- All tasks learned together
- Reduces error propagation
- More complex to implement
- Better overall accuracy

**Modern best practice**: Use joint models or character-level parsing to avoid segmentation bottleneck.
