# S1 Synthesis: LLM Evaluation & Testing Frameworks

## Executive Summary

The LLM evaluation landscape has matured significantly, with clear tool differentiation by use case. **DeepEval** emerges as the most comprehensive open-source option, while **Ragas** leads for RAG-specific evaluation. **PromptFoo** excels at quick iterations and security testing, **LangSmith** dominates observability, and **TruLens** offers OpenTelemetry-native tracing.

## Comparison Matrix

| Tool | Focus | Metrics | Pricing | Best For |
|------|-------|---------|---------|----------|
| **DeepEval** | Comprehensive | 60+ | Free + Enterprise | CI/CD, full coverage |
| **PromptFoo** | Prompt testing | Basic | Free | Quick iterations, red team |
| **LangSmith** | Observability | Custom | $39/seat+ | LangChain users, tracing |
| **Ragas** | RAG-specific | 5 core | Free | RAG pipelines |
| **TruLens** | Feedback functions | Extensible | Free | OTel users, custom evals |

## Decision Framework

### Choose DeepEval when:
- Need comprehensive metric coverage (RAG, agents, safety, multimodal)
- Want CI/CD integration with pytest-style tests
- Require self-explaining metrics for debugging
- Building production systems with regression detection

### Choose PromptFoo when:
- Doing rapid prompt engineering iterations
- Need security/red team testing
- Prefer YAML config over code
- Want lightweight CLI tool without SDK

### Choose LangSmith when:
- Using LangChain/LangGraph
- Need production observability + evaluation
- Want unified tracing and testing platform
- Have budget for commercial tooling

### Choose Ragas when:
- Evaluating RAG systems specifically
- Want lower-cost RAG metrics (vs LLM-as-judge)
- Need quick integration, pandas-like workflow
- Don't need general LLM evaluation

### Choose TruLens when:
- Already using OpenTelemetry
- In Snowflake ecosystem
- Need custom feedback functions
- Want extensible evaluation framework

## Recommended Stack

### For QRCards / spawn-solutions:

**Primary: DeepEval**
- Comprehensive coverage for diverse LLM patterns
- CI/CD ready for automated testing
- Self-explaining metrics aid debugging

**Secondary: Ragas**
- Supplement for RAG-specific depth
- RAG Triad metrics for retrieval quality
- Lower cost for high-volume RAG testing

**Optional: PromptFoo**
- Red teaming for security validation
- Quick prompt A/B testing during development

## Key Insights

1. **No single tool covers everything** - Most teams combine 2-3 tools
2. **DeepEval has widest metric coverage** (60+) with self-explanation
3. **Ragas pioneered RAG Triad** - still best for retrieval-focused eval
4. **PromptFoo leads red teaming** - best for security testing
5. **LangSmith = observability-first** - evaluation is secondary
6. **TruLens differentiator** - OpenTelemetry native, extensible

## Cost Considerations

| Tool | Free Tier | Paid Trigger |
|------|-----------|--------------|
| DeepEval | Full OSS | Enterprise features |
| PromptFoo | Full OSS | Hosted dashboard |
| LangSmith | Limited | Team collaboration |
| Ragas | Full OSS | N/A |
| TruLens | Full OSS | N/A |

## Sources

- [DeepEval Alternatives Compared](https://deepeval.com/blog/deepeval-alternatives-compared)
- [LLM Evaluation Frameworks Comparison](https://www.comet.com/site/blog/llm-evaluation-frameworks/)
- [Top LLM Evaluation Tools 2025](https://www.confident-ai.com/blog/greatest-llm-evaluation-tools-in-2025)
- [TruLens Documentation](https://www.trulens.org/)
- [PromptFoo Docs](https://www.promptfoo.dev/docs/intro/)
- [LangSmith Docs](https://docs.langchain.com/langsmith)
