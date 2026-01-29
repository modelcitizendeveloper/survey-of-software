# tiktoken

**Repository:** github.com/openai/tiktoken
**Downloads/Month:** ~10M (PyPI, estimated)
**GitHub Stars:** 12,000+
**Last Updated:** 2025 (Active)

## Quick Assessment
- **Popularity:** Very High - Powers GPT-3.5, GPT-4, GPT-4o
- **Maintenance:** Active - OpenAI maintains
- **Documentation:** Good - Performance-focused

## Pros
- **Extremely fast** - 3-6× faster than other tokenizers
- **Byte-level BPE** - No OOV (out-of-vocabulary) issues
- **Production-tested** - Billions of tokens processed daily
- **Pre-built encodings** - cl100k_base ready to use

## Cons
- **Inefficient for CJK** - 2-3 tokens per character average
- **Not optimized for CJK** - English-centric vocabulary
- **Higher token counts** - 2-8× more tokens than English
- **Cost implications** - Users pay more per CJK character

## Quick Take
Fastest tokenizer available, but CJK is a second-class citizen. Most Chinese characters require 2-3 tokens (89% in GPT-4). Great for English, acceptable for CJK if speed is critical.
