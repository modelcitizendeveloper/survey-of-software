# LLM Framework Recommendation Guide

## Decision Framework: Which Framework Should You Use?

This guide helps you choose the right LLM orchestration framework based on your specific needs, team, and use case.

## Quick Decision Tree

```
Start Here
│
├─ Do you need RAG/document retrieval as primary feature?
│  └─ YES → Use LlamaIndex (35% better retrieval, specialized tooling)
│
├─ Are you in Microsoft ecosystem (Azure, .NET, M365)?
│  └─ YES → Use Semantic Kernel (best Azure integration, multi-language)
│
├─ Do you need Fortune 500 production deployment?
│  ├─ On-premise/VPC required? → Use Haystack (best performance, enterprise focus)
│  └─ Cloud-native? → Use Haystack or Semantic Kernel
│
├─ Are you rapid prototyping or learning?
│  └─ YES → Use LangChain (3x faster, most examples, largest community)
│
├─ Do you need automated prompt optimization?
│  └─ YES → Use DSPy (research focus, lowest overhead)
│
└─ General-purpose multi-agent system?
   └─ Use LangChain + LangGraph (most mature, largest ecosystem)
```

## Recommendation by Use Case

### 1. Building a Chatbot or Virtual Assistant

**Recommended**: LangChain
- Excellent conversation memory management
- Easy tool integration
- Extensive examples for chatbots
- Streaming support for real-time responses

**Alternative**: Semantic Kernel (if Microsoft ecosystem)

**When to use raw API**: Simple single-turn QA with no memory

---

### 2. Document Search / RAG System

**Recommended**: LlamaIndex
- 35% better retrieval accuracy
- Best-in-class document parsing (LlamaParse)
- Advanced retrieval strategies (hybrid search, reranking)
- Enterprise data source integration

**Alternative**: Haystack (if search quality + production deployment both critical)

**When to use raw API**: Single document, simple QA

---

### 3. Enterprise Production Application

**Recommended**: Haystack
- Best performance (5.9ms overhead, 1.57k tokens)
- Fortune 500 adoption (Airbus, Netflix, Intel)
- On-premise/VPC deployment
- Kubernetes templates
- Haystack Enterprise support

**Alternative**: Semantic Kernel (if Microsoft stack with Azure)

**When to use raw API**: Never for production enterprise apps

---

### 4. Multi-Agent System

**Recommended**: LangChain + LangGraph
- Most mature agent framework
- LinkedIn, Elastic using in production
- 51% of orgs deploy agents in production
- Best orchestration capabilities

**Alternative**: Semantic Kernel (Agent Framework moving to GA, excellent for business processes)

**When to use raw API**: Never for multi-agent systems

---

### 5. Rapid Prototyping / MVP

**Recommended**: LangChain
- 3x faster prototyping than Haystack
- Most examples and tutorials
- Largest community for help
- Quick iteration cycles

**Alternative**: LlamaIndex (if RAG-focused MVP)

**When to use raw API**: Under 50 lines, single LLM call

---

### 6. Research / Academic Project

**Recommended**: DSPy
- Automated prompt optimization
- Lowest overhead (3.53ms)
- Stanford NLP research foundation
- Cutting-edge optimization techniques

**Alternative**: LangChain (if need more examples and ecosystem)

**When to use raw API**: Simple experiments, single LLM calls

---

### 7. Legal / Medical / Regulated Industry

**Recommended**: Semantic Kernel (Microsoft compliance) OR Haystack (on-premise)
- Enterprise security features
- Compliance and governance
- On-premise deployment (Haystack)
- Microsoft SLAs (Semantic Kernel)

**Alternative**: LlamaIndex (for RAG with high accuracy requirements)

**When to use raw API**: Never for regulated industries

---

### 8. Startup / Agency Building for Clients

**Recommended**: LangChain
- Fastest prototyping (3x)
- Most flexible for different client needs
- Largest ecosystem for integrations
- LangSmith for client demos/debugging

**Alternative**: Match to client's specific use case (RAG → LlamaIndex, Microsoft → Semantic Kernel)

**When to use raw API**: Proof-of-concepts, simple demos

---

### 9. Mobile/Frontend Team (TypeScript/JavaScript)

**Recommended**: LangChain
- Full-featured LangChain.js
- JavaScript/TypeScript support
- npm packages available

**Alternative**: LlamaIndex (TypeScript version available)

**Avoid**: Haystack (Python only), Semantic Kernel (no JS/TS)

**When to use raw API**: Simple client-side LLM calls

---

### 10. .NET / C# / Java Enterprise

**Recommended**: Semantic Kernel
- Only framework with C#, Python, AND Java support
- v1.0+ stable APIs (non-breaking changes)
- Microsoft backing and support
- Azure integration

**Alternative**: LangChain (Python) if not in Microsoft ecosystem

**When to use raw API**: Simple .NET apps with single LLM calls

---

## Recommendation by Team Size

### Solo Developer / Small Team (1-3 people)
**Recommended**: LangChain
- Most tutorials and examples
- Largest community for help
- Fastest prototyping
- Good enough for most use cases

### Mid-Size Team (4-10 people)
**Recommended**: Depends on use case
- RAG focus → LlamaIndex
- Production deployment → Haystack
- Microsoft stack → Semantic Kernel
- General purpose → LangChain

### Enterprise Team (10+ people)
**Recommended**: Haystack or Semantic Kernel
- Stable APIs important for large teams
- Production-grade deployment
- Enterprise support available
- Clear separation of concerns

---

## Recommendation by Technical Expertise

### Beginner (New to LLMs)
**Recommended**: LangChain
- Easiest learning curve for linear flows
- Most examples and tutorials
- Largest community for questions
- Gentle introduction to concepts

**Avoid**: DSPy (too steep), Haystack (too structured)

### Intermediate (Some LLM experience)
**Recommended**: Match to use case
- Explore specialized frameworks (LlamaIndex for RAG)
- Consider production needs (Haystack)
- Experiment with optimization (DSPy)

### Advanced (LLM expert)
**Recommended**: Choose best tool for job
- DSPy for optimization research
- Haystack for production excellence
- LlamaIndex for RAG excellence
- Semantic Kernel for enterprise .NET

---

## Recommendation by Stability Requirements

### High Stability (Enterprise, Production)
**Recommended**: Semantic Kernel or Haystack
- Semantic Kernel: v1.0+ stable APIs, non-breaking changes
- Haystack: Mature (2019), production-focused
- Both have enterprise support options

**Avoid**: LangChain (breaking changes every 2-3 months)

### Moderate Stability (Can handle updates)
**Recommended**: LangChain or LlamaIndex
- Accept frequent updates for latest features
- Active development is a plus
- Budget for maintenance

### Experimental (Cutting-edge OK)
**Recommended**: DSPy or latest LangChain features
- Willing to work with evolving APIs
- Want newest techniques
- Can tolerate breaking changes

---

## Recommendation by Performance Requirements

### Performance Critical (Low Latency)
**Recommended**: DSPy or Haystack
- DSPy: 3.53ms overhead (lowest)
- Haystack: 5.9ms overhead, 1.57k tokens (best token efficiency)

**Avoid**: LangChain (10ms overhead, 2.40k tokens)

### Moderate Performance
**Recommended**: LlamaIndex
- 6ms overhead, 1.60k tokens
- Good balance of features and performance

### Performance Not Critical
**Recommended**: Any framework
- Choose based on other factors (features, community, etc.)

---

## When to Use Raw API (No Framework)

Use direct API calls (OpenAI, Anthropic, etc.) when:

1. **Single LLM call**: No chaining or multi-step workflows
2. **No tool calling**: Simple prompts, no external tool integration
3. **No memory**: Stateless interactions
4. **Under 50 lines**: Simple scripts or proofs-of-concept
5. **Learning**: Understanding LLM basics before using frameworks
6. **Performance critical**: Every millisecond matters, minimal overhead needed
7. **Simple use case**: "Translate this text", "Summarize this article"

**Example scenarios**:
- Email subject line generator
- Simple sentiment analysis
- One-off text transformations
- Embedding generation
- Basic completion tasks

---

## When Framework Complexity is Warranted

Use a framework when:

1. **Multi-step workflows**: Chains of LLM calls
2. **Agent systems**: Tool calling, planning, execution loops
3. **RAG systems**: Retrieval, embedding, vector search
4. **Memory management**: Conversation history, long-term memory
5. **Production deployment**: Monitoring, observability, error handling
6. **Team collaboration**: Shared patterns, reusable components
7. **Over 100 lines**: Complex LLM logic that benefits from structure

---

## Hybrid Approaches

### LangChain + LlamaIndex
- Use LangChain for general orchestration and agents
- Use LlamaIndex for RAG components
- Both integrate well together

### Framework + Raw API
- Use framework for 80% (chains, agents, RAG)
- Use raw API for 20% (performance-critical paths, simple calls)

### Multiple Frameworks
- Different services can use different frameworks
- Match framework to service requirements
- API boundaries between services

---

## Migration Paths

### Starting with Raw API → Moving to Framework
1. Start with raw API to learn LLM basics
2. Hit complexity threshold (chains, agents, RAG)
3. Migrate to LangChain (easiest) or specialized framework
4. Refactor gradually, one component at a time

### LangChain → LlamaIndex (for RAG)
- If RAG becomes primary focus
- Want better retrieval accuracy (35% boost)
- Need specialized RAG tooling
- Can coexist (use both in same project)

### Any Framework → Haystack (for Production)
- When prototyping phase ends
- Production deployment becomes priority
- Need enterprise features
- Rewrite recommended (different architecture)

### LangChain → LangGraph (for Agents)
- LangChain docs recommend LangGraph for agents
- When agent complexity grows
- Need stateful, event-based workflows
- Smooth migration path (same ecosystem)

---

## Budget Considerations

### Free / Open Source Only
All frameworks are open-source (MIT or Apache 2.0):
- DSPy: Completely free, no commercial offering
- LangChain: Free core, optional LangSmith ($)
- LlamaIndex: Free core, optional LlamaCloud ($)
- Haystack: Free core, optional Haystack Enterprise ($)
- Semantic Kernel: Free core, Azure costs ($)

### Budget for Commercial Support
If you need enterprise support:
- **Haystack Enterprise** (Aug 2025): Private support, templates, Kubernetes guides
- **LangSmith**: Observability, debugging, team collaboration
- **LlamaCloud**: Managed RAG infrastructure
- **Microsoft Azure**: Semantic Kernel with Azure SLAs

### Cost of DIY vs Framework
- Framework saves 6-12 months of development time
- Building observability alone takes 6-12 months
- Community support reduces debugging time
- Commercial offerings reduce operational burden

---

## Common Mistakes to Avoid

1. **Using Framework for Simple Tasks**: Don't use LangChain for single LLM calls
2. **Wrong Framework for Use Case**: Don't use LangChain for RAG when LlamaIndex excels
3. **Ignoring Breaking Changes**: LangChain updates frequently, monitor deprecation list
4. **Over-Engineering**: Start simple, add complexity as needed
5. **Ignoring Performance**: If latency matters, measure framework overhead
6. **No Observability**: Use LangSmith, Langfuse, or Phoenix for production
7. **Vendor Lock-in**: All frameworks are model-agnostic, use that flexibility

---

## Summary Recommendations

### Best for Beginners
**LangChain** - Most examples, largest community, easiest for linear workflows

### Best for RAG
**LlamaIndex** - 35% better retrieval, specialized tooling, best document parsing

### Best for Enterprise
**Haystack** - Fortune 500 adoption, best performance, production-focused

### Best for Microsoft Ecosystem
**Semantic Kernel** - Multi-language (C#, Python, Java), Azure integration, stable APIs

### Best for Production
**Haystack** or **Semantic Kernel** - Both excellent, choose based on ecosystem

### Best for Prototyping
**LangChain** - 3x faster than alternatives, most flexible

### Best for Performance
**DSPy** - Lowest overhead (3.53ms), automated optimization

### Best for Agents
**LangChain + LangGraph** - Most mature, production-proven (LinkedIn, Elastic)

### Best for Stability
**Semantic Kernel** - v1.0+ stable APIs, non-breaking change commitment

### Best Overall
**Depends on your use case** - There is no one-size-fits-all answer

---

## Final Advice

1. **Start Simple**: Use raw API to learn, graduate to frameworks when needed
2. **Match to Use Case**: RAG → LlamaIndex, Enterprise → Haystack, General → LangChain
3. **Consider Long-Term**: Stability and maintenance matter for production
4. **Experiment**: Try multiple frameworks in prototyping phase
5. **Monitor Performance**: Measure overhead and token usage for your use case
6. **Join Communities**: Discord, GitHub discussions, StackOverflow
7. **Budget for Updates**: LangChain requires ongoing maintenance
8. **Use Observability**: LangSmith, Langfuse, or Phoenix for production
9. **Read the Docs**: All frameworks have improved documentation in 2025
10. **Ask for Help**: Large communities mean faster answers to problems

The LLM framework landscape is maturing rapidly. Choose the tool that best fits your team's skills, use case requirements, and long-term maintenance capacity. When in doubt, start with LangChain for general-purpose work or LlamaIndex for RAG, then optimize later.
