# GPT-4 Multilingual Capabilities

## Overview
OpenAI's GPT-4 (2023) represents state-of-the-art commercial multilingual language model. Unlike specialized CJK models, GPT-4 achieves strong multilingual performance through massive scale and diverse training data. Exact architecture undisclosed.

## CJK Language Support
- **Chinese**: Excellent support (Simplified and Traditional)
- **Japanese**: Excellent support
- **Korean**: Excellent support
- Benchmarks show GPT-4 near-native performance in CJK languages

## Architecture
- Transformer-based (details proprietary)
- Estimated 1.7T+ parameters (mixture-of-experts, unconfirmed)
- Multimodal capabilities (vision + language)
- Trained on diverse internet-scale data including CJK sources

## Tokenization Approach
- Enhanced tokenization for CJK efficiency (improvements over GPT-3.5)
- Reduced token-per-character ratio for CJK scripts
- Details proprietary but demonstrably more efficient

## Key Strengths for CJK
- **Best-in-class multilingual reasoning** across benchmarks
- Strong cross-lingual transfer and code-switching handling
- Robust to mixed CJK-English input (common in real-world scenarios)
- Advanced reasoning capabilities in CJK languages
- Regular updates and improvements via API
- Strong instruction-following in CJK languages

## Limitations
- **Closed-source**: No model weights, no self-hosting
- **API-only**: Must use OpenAI API (cost per token)
- **Vendor lock-in**: Dependent on OpenAI service availability
- **Data privacy**: Data sent to OpenAI servers
- **Cost**: Usage-based pricing can be expensive at scale
- **Rate limits**: API throttling for high-volume applications
- **Latency**: Network round-trip for each request

## Use Cases
- High-quality multilingual text generation
- Complex reasoning in CJK languages
- Cross-lingual summarization and translation
- Conversational AI with CJK support
- Rapid prototyping (no infrastructure setup)
- Low-volume applications where accuracy > cost

## Availability
- **License**: Commercial API only (proprietary)
- **Access**: OpenAI API (requires API key and billing)
- **Cost**: ~$0.03/1K tokens (input), ~$0.06/1K tokens (output) for GPT-4
- **Infrastructure**: Cloud-only, managed by OpenAI

## Strategic Considerations
GPT-4 is optimal for applications where:
- Quality and capability justify cost
- Data privacy allows cloud processing
- Self-hosting is not required
- Rapid development is prioritized

For cost-sensitive, high-volume, or data-sensitive CJK applications, open-source alternatives (BLOOM, XLM-R, ERNIE) with self-hosting may be preferable despite capability gaps.
