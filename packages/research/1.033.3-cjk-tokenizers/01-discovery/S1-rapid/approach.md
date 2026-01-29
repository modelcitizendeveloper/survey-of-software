# S1: Rapid Discovery Approach

## Methodology
Speed-focused ecosystem scan to identify popular CJK tokenization solutions through:
- GitHub repository activity and stars
- LLM ecosystem adoption (GPT, Llama, Qwen)
- Package download metrics
- Community discussions and documentation quality

## Time Budget
10 minutes

## Discovery Tools Used
- GitHub trending and stars
- Package registries (PyPI download counts)
- LLM model documentation (official tokenizer choices)
- Technical blog posts and community resources

## Selection Criteria
- **Popularity**: Adoption by major LLM projects
- **Recent activity**: Active development and maintenance
- **Documentation**: Clear CJK-specific guidance
- **Ecosystem integration**: Used by production systems

## Findings Summary
Three dominant approaches emerged:
1. **SentencePiece** - Language-independent, explicitly designed for CJK
2. **tiktoken** - OpenAI's fast BPE, byte-level approach
3. **HuggingFace Tokenizers** - Fast Rust implementation with CJK support

Character vs byte-level is a **strategy choice**, not a library choice - most modern tokenizers support both.
