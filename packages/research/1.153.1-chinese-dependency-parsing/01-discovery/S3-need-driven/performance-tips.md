# Performance Tips

1. **Choose the right model size**: Larger models = better accuracy but slower

2. **Batch processing**: Process multiple sentences together for efficiency

3. **Cache results**: Dependency parsing is deterministic, cache common phrases

4. **Pre-filter**: For large datasets, pre-filter irrelevant text before parsing

5. **GPU acceleration**: Use GPU-enabled models for large-scale processing
