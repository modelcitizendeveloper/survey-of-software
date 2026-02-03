# 1.200: LLM Orchestration Frameworks

## Overview

**Category**: 1.200-209 AI & LLM Application Frameworks (Tier 1 - you run the code)
**Research Question**: Which LLM orchestration framework should developers use for building AI applications? What are the trade-offs between frameworks?
**Status**: S1 Rapid Discovery completed
**Generic Use Cases**: Developers building chatbots, teams building RAG systems, agencies building AI products

## What This Research Covers

This research explores frameworks for building LLM applications (chains, agents, RAG systems) using libraries you import and control. These frameworks help developers build production-grade AI applications without writing everything from scratch.

**In Scope**:
- General-purpose frameworks (LangChain, Semantic Kernel)
- Specialized RAG frameworks (LlamaIndex)
- Production-focused frameworks (Haystack)
- Research/optimization frameworks (DSPy)
- Framework comparison and selection guidance

**Out of Scope**:
- Hosted LLM APIs (3.200 - different tier)
- No-code AI platforms (Tier 3)
- Model training frameworks (different category)
- Specific client implementations (generic research only)

## Quick Start: Which Framework Should I Use?

**For most developers starting out**: LangChain (most examples, largest community, fastest prototyping)
**For RAG/document search**: LlamaIndex (35% better retrieval accuracy, specialized tooling)
**For enterprise production**: Haystack (Fortune 500 adoption, best performance)
**For Microsoft ecosystem**: Semantic Kernel (C#/Python/Java, Azure integration)
**For research/optimization**: DSPy (automated prompt optimization, lowest overhead)

See `/01-discovery/S1-rapid/recommendation.md` for detailed decision framework.

## Key Findings (S1 Rapid Discovery)

### Framework Landscape
Five major frameworks dominate the LLM orchestration space:

1. **LangChain** (~111k GitHub stars)
   - Most popular, general-purpose
   - Best for prototyping (3x faster than alternatives)
   - Largest ecosystem and community
   - Breaking changes every 2-3 months

2. **LlamaIndex** (significant community)
   - RAG specialist, 35% better retrieval accuracy
   - Best-in-class document parsing (LlamaParse)
   - Enterprise data integration (SharePoint, Google Drive)

3. **Haystack** (deepset AI, since 2019)
   - Production-first, Fortune 500 adoption (Airbus, Netflix, Intel)
   - Best performance: 5.9ms overhead, 1.57k tokens
   - Haystack Enterprise launched August 2025

4. **Semantic Kernel** (Microsoft)
   - Multi-language: C#, Python, Java (unique)
   - Stable v1.0+ APIs (non-breaking changes)
   - Azure ecosystem integration

5. **DSPy** (Stanford NLP, ~16k stars)
   - Automated prompt optimization
   - Lowest overhead: 3.53ms
   - Research focus, steeper learning curve

### Performance Comparison
| Framework | Overhead | Token Usage | Best For |
|-----------|----------|-------------|----------|
| DSPy | 3.53ms | 2.03k | Performance |
| Haystack | 5.9ms | 1.57k | Production |
| LlamaIndex | 6ms | 1.60k | RAG |
| LangChain | 10ms | 2.40k | Prototyping |

### Production Adoption
- **51% of organizations** deploy agents in production (LangChain report)
- **Fortune 500 companies** using Haystack: Airbus, Intel, Netflix, Apple, NVIDIA, Comcast
- **Notable deployments**: LinkedIn SQL Bot (LangChain), Elastic AI assistant (LangGraph)

### Key Trade-offs

**LangChain**: Fastest prototyping but frequent breaking changes
**LlamaIndex**: Best RAG but less suited for non-retrieval use cases
**Haystack**: Best production/performance but slower prototyping
**Semantic Kernel**: Best stability but Microsoft-centric ecosystem
**DSPy**: Best optimization but steepest learning curve, smallest community

## When to Use Raw API vs Framework

### Use Raw API When:
- Single LLM call, no chaining
- Under 50 lines of code
- No memory or state management
- Simple use cases (translation, sentiment analysis)

### Use Framework When:
- Multi-step workflows (chains)
- Agent systems with tool calling
- RAG systems with retrieval
- Production deployment
- Over 100 lines of LLM code

## Research Deliverables

### S1 Rapid Discovery (Completed)

**Framework Profiles**:
- `/01-discovery/S1-rapid/framework-langchain.md` - General-purpose leader
- `/01-discovery/S1-rapid/framework-llamaindex.md` - RAG specialist
- `/01-discovery/S1-rapid/framework-haystack.md` - Production champion
- `/01-discovery/S1-rapid/framework-semantic-kernel.md` - Microsoft enterprise
- `/01-discovery/S1-rapid/framework-dspy.md` - Research optimizer

**Comparison & Recommendations**:
- `/01-discovery/S1-rapid/comparison-matrix.md` - Detailed comparison across 15+ dimensions
- `/01-discovery/S1-rapid/recommendation.md` - Decision framework for choosing the right tool

**Domain Understanding**:
- `DOMAIN_EXPLAINER.md` - What are LLM frameworks and why they exist

## Key Questions Answered

1. **Learning curve**: LangChain easiest for beginners (linear workflows), DSPy steepest (research concepts)
2. **RAG specialization**: LlamaIndex wins (35% better accuracy, specialized tooling)
3. **Production readiness**: Haystack (Fortune 500) and Semantic Kernel (Microsoft SLAs) lead
4. **Vendor lock-in**: All frameworks are model-agnostic (OpenAI, Anthropic, local models)
5. **Observability**: LangChain (LangSmith) has best debugging/tracing
6. **Agent capabilities**: LangChain + LangGraph most mature (LinkedIn, Elastic in production)
7. **Complexity threshold**: Use framework when 100+ lines of LLM code, multi-step workflows, or production deployment

## Cross-References

- **3.200** (LLM APIs): These frameworks CALL those APIs (OpenAI, Anthropic, etc.)
- **3.134** (AI Content Generation): S4 build-vs-buy mentions LangChain - this is the deep dive
- **1.203** (Vector Databases): RAG workflows need vector DBs (Pinecone, Chroma, etc.)
- **Related frameworks**: LangGraph (agents), AutoGen (Microsoft multi-agent)

## Market Trends (2025)

1. **Agent Frameworks Maturing**: LangGraph, Semantic Kernel Agent Framework moving to GA
2. **RAG Evolution**: From naive chunk retrieval to agentic retrieval (sophisticated multi-step)
3. **Observability Critical**: LangSmith, Langfuse, Phoenix now table stakes for production
4. **Enterprise Adoption**: 51% of orgs deploying agents, 78% planning implementations
5. **Framework Consolidation**: LangChain, LlamaIndex, Haystack as dominant players
6. **Microsoft Push**: Semantic Kernel + AutoGen unification for enterprise
7. **Performance Focus**: Framework overhead matters (3.53ms - 10ms range)

## Repository Structure

```
1.200-llm-orchestration/
├── README.md (this file)
├── DOMAIN_EXPLAINER.md (what are LLM frameworks, why they exist)
├── metadata.yaml (experiment tracking)
└── 01-discovery/
    └── S1-rapid/
        ├── framework-langchain.md (LangChain profile)
        ├── framework-llamaindex.md (LlamaIndex profile)
        ├── framework-haystack.md (Haystack profile)
        ├── framework-semantic-kernel.md (Semantic Kernel profile)
        ├── framework-dspy.md (DSPy profile)
        ├── comparison-matrix.md (15+ dimension comparison)
        └── recommendation.md (decision framework)
```

## Next Steps (Potential S2-S4)

### S2 Comprehensive (If Needed)
- Hands-on testing with sample RAG application
- Performance benchmarking on consistent workload
- Cost analysis (token usage, infrastructure)
- Migration path documentation

### S3 Need-Driven (If Specific Client Need)
- Deep dive into specific framework for client use case
- Production deployment architecture
- Observability setup (LangSmith, Langfuse, Phoenix)
- Evaluation framework implementation

### S4 Strategic (If Build Decision)
- Implement reference architecture for chosen framework
- Create reusable templates for common patterns
- Production deployment guide
- Team training materials

## Recommendations Summary

### By Use Case:
- **Chatbot/Virtual Assistant**: LangChain
- **Document Search/RAG**: LlamaIndex
- **Enterprise Production**: Haystack or Semantic Kernel
- **Multi-Agent System**: LangChain + LangGraph
- **Rapid MVP**: LangChain
- **Research Project**: DSPy
- **Regulated Industry**: Semantic Kernel or Haystack (on-premise)

### By Team:
- **Solo/Small (1-3)**: LangChain (most tutorials)
- **Mid-Size (4-10)**: Match to use case
- **Enterprise (10+)**: Haystack or Semantic Kernel (stable APIs)

### By Expertise:
- **Beginner**: LangChain (easiest learning curve)
- **Intermediate**: Match to use case
- **Advanced**: Choose best tool for job

### By Requirements:
- **High Stability**: Semantic Kernel (v1.0+) or Haystack
- **Performance Critical**: DSPy (3.53ms) or Haystack (1.57k tokens)
- **Largest Ecosystem**: LangChain (111k stars)
- **Best RAG**: LlamaIndex (35% accuracy boost)

## Resources

### Official Websites:
- LangChain: https://www.langchain.com/
- LlamaIndex: https://www.llamaindex.ai/
- Haystack: https://haystack.deepset.ai/
- Semantic Kernel: https://learn.microsoft.com/en-us/semantic-kernel/
- DSPy: https://dspy.ai/

### Observability Tools:
- LangSmith: https://www.langchain.com/langsmith (commercial)
- Langfuse: https://langfuse.com/ (open-source)
- Phoenix: https://phoenix.arize.com/ (Arize AI)

### Community:
- LangChain Discord (largest)
- GitHub discussions for each framework
- StackOverflow tags

## Research Methodology

**S1 Rapid Discovery** conducted via:
- Web search for current state (2024-2025)
- GitHub stars and activity analysis
- Production use case research
- Documentation quality review
- Performance metric comparison
- Enterprise adoption verification

**Time Investment**: ~90 minutes (within S1 60-90 minute target)
**Sources**: Official documentation, tech blogs, case studies, GitHub repositories
**Currency**: All data from 2024-2025 unless noted

## Conclusion

The LLM orchestration framework landscape has matured significantly in 2025, with clear leaders emerging for different use cases:

- **LangChain** dominates general-purpose orchestration and prototyping
- **LlamaIndex** owns the RAG specialization with 35% better retrieval
- **Haystack** leads in production enterprise deployments
- **Semantic Kernel** is Microsoft's enterprise play with unique multi-language support
- **DSPy** represents cutting-edge research in automated optimization

There is no single "best" framework - the right choice depends on your use case, team, and requirements. Use the decision framework in `recommendation.md` to make an informed choice.

For most developers new to LLM applications, start with LangChain to learn the concepts, then specialize based on your specific needs (RAG → LlamaIndex, Production → Haystack, Microsoft → Semantic Kernel).

The complexity threshold for adopting a framework is around 100 lines of LLM code, multi-step workflows, or production deployment. Below that, consider using raw LLM APIs directly.

---

**Last Updated**: 2025-11-19 (S1 Rapid Discovery)
**Maintained By**: spawn-solutions research team
**MPSE Version**: v3.0
