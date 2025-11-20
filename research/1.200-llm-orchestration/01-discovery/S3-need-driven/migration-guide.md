# Framework Migration Guide

## Overview

This guide covers common migration scenarios between LLM orchestration frameworks, helping you understand when to migrate, how much effort is involved, and how to minimize disruption.

## Migration Decision Framework

### When to Migrate

**Good reasons to migrate**:
1. **Use case mismatch**: Using general framework for specialized need (e.g., LangChain for pure RAG → LlamaIndex)
2. **Production stability**: Breaking changes causing maintenance burden (LangChain → Haystack/Semantic Kernel)
3. **Performance**: High costs or latency becoming problematic (→ Haystack for efficiency)
4. **Ecosystem alignment**: Moving to Microsoft stack (→ Semantic Kernel for Azure)
5. **Team growth**: Need better multi-team coordination (→ enterprise framework)

**Bad reasons to migrate**:
1. **Shiny object syndrome**: New framework hype without clear benefits
2. **Minor performance gains**: Migrating for 5-10% improvement rarely worth it
3. **Feature parity**: Current framework can do it, just differently
4. **Avoiding learning**: Running from complexity instead of understanding it
5. **Premature optimization**: Migrating before validating product-market fit

### Migration Cost Estimation

| Migration Type | Effort | Risk | Business Impact |
|---------------|--------|------|-----------------|
| **Direct API → Framework** | Low (1-2 weeks) | Low | High (enables complexity) |
| **Framework → Direct API** | Low (1-2 weeks) | Moderate | Moderate (simplification) |
| **LangChain → LlamaIndex (RAG)** | Moderate (2-4 weeks) | Low | High (better retrieval) |
| **LangChain → Haystack** | High (4-8 weeks) | Moderate | High (stability + performance) |
| **LangChain → Semantic Kernel** | High (4-8 weeks) | Moderate | High (Azure alignment) |
| **LlamaIndex → LangChain** | Moderate (2-4 weeks) | Low | Moderate (more flexibility) |
| **Any → DSPy** | Moderate (2-4 weeks) | High | Research (not production) |

## Migration Scenario 1: Direct API → LangChain

### When to Migrate

**Complexity threshold reached when you need**:
- Multi-step LLM workflows (chains)
- Conversation memory across turns
- Tool/function calling with multiple tools
- RAG with document retrieval
- Agent-based reasoning

### Migration Example

**Before (Direct API)**:
```python
import openai

def simple_chat(message: str):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

# Problem: No memory, no tools, no chains
response1 = simple_chat("Hi, I'm building an app")
response2 = simple_chat("What should I use?")  # Doesn't remember previous message
```

**After (LangChain)**:
```python
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

llm = ChatOpenAI(model="gpt-4")
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

response1 = conversation.predict(input="Hi, I'm building an app")
response2 = conversation.predict(input="What should I use?")
# Now has memory and context
```

### Migration Effort: 1-2 weeks

**Tasks**:
1. Install LangChain: `uv add langchain langchain-openai`
2. Replace API calls with LangChain chains
3. Add memory if needed
4. Test thoroughly
5. Deploy

**Risks**: Low - additive change, can run both in parallel

## Migration Scenario 2: LangChain → LlamaIndex (RAG Focus)

### When to Migrate

**Migrate to LlamaIndex when**:
- RAG is 80%+ of your use case
- Need better retrieval accuracy (35% improvement)
- Want specialized RAG features (hybrid search, re-ranking)
- Need advanced techniques (CRAG, Self-RAG, HyDE)
- Document parsing quality matters (LlamaParse)

**Don't migrate if**:
- RAG is one feature among many
- LangChain RAG "good enough"
- Heavy agent/tool orchestration needed

### Migration Example

**Before (LangChain RAG)**:
```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Pinecone
from langchain.chains import RetrievalQA

# Load documents
loader = PyPDFLoader("docs.pdf")
documents = loader.load()

# Split
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(documents)

# Embed and store
embeddings = OpenAIEmbeddings()
vectorstore = Pinecone.from_documents(chunks, embeddings, index_name="my-index")

# Create QA chain
llm = ChatOpenAI(model="gpt-4")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Query
result = qa_chain.invoke({"query": "What is X?"})
```

**After (LlamaIndex)**:
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
import pinecone

# Load documents (simpler)
documents = SimpleDirectoryReader("./docs").load_data()

# Initialize services
llm = OpenAI(model="gpt-4")
embed_model = OpenAIEmbedding()

# Vector store
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index("my-index")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

# Create index
index = VectorStoreIndex.from_documents(
    documents,
    vector_store=vector_store,
    embed_model=embed_model
)

# Query engine with advanced features
query_engine = index.as_query_engine(
    llm=llm,
    similarity_top_k=5,
    node_postprocessors=[
        # Add re-ranking for better results
        # Hybrid search for keyword + semantic
    ]
)

# Query (cleaner)
response = query_engine.query("What is X?")
print(response.response)
print(response.source_nodes)  # Better source attribution
```

### Migration Effort: 2-4 weeks

**Migration Steps**:

1. **Week 1: Parallel Implementation**
   - Set up LlamaIndex alongside existing LangChain
   - Migrate document ingestion pipeline
   - Create new vector index (can reuse Pinecone/Qdrant)
   - Test basic retrieval

2. **Week 2: Feature Parity**
   - Implement all existing RAG features in LlamaIndex
   - Add advanced features (hybrid search, re-ranking)
   - A/B test retrieval quality
   - Measure accuracy improvement

3. **Week 3: Integration**
   - Update API endpoints to use LlamaIndex
   - Migrate user-facing features
   - Run both systems in parallel (shadow mode)
   - Monitor metrics

4. **Week 4: Cutover**
   - Switch traffic to LlamaIndex
   - Monitor for issues
   - Deprecate LangChain RAG code
   - Documentation update

**Code Portability**:
- **Prompts**: 100% portable (just strings)
- **Documents**: 100% portable (standard formats)
- **Vector indices**: 95% portable (may need re-indexing for optimal performance)
- **Evaluation datasets**: 100% portable
- **Monitoring**: Needs new integration (LlamaIndex callbacks vs LangChain)

**Risks**: Low-Moderate
- Can run both in parallel
- Data (documents) is framework-agnostic
- Rollback is straightforward

## Migration Scenario 3: LangChain → Haystack (Production)

### When to Migrate

**Migrate to Haystack when**:
- Frequent LangChain breaking changes causing pain
- Performance optimization critical (5.9ms overhead vs 10ms)
- Token efficiency matters (1.57k vs 2.40k tokens)
- Enterprise production deployment
- Need Fortune 500-level stability

**Don't migrate if**:
- Rapid feature iteration more important than stability
- Heavy agent orchestration (LangGraph advantage)
- Team comfortable with LangChain maintenance

### Migration Challenges

**Key Differences**:
1. **Architecture**: Haystack uses explicit Pipeline vs LangChain's LCEL
2. **Components**: Stricter I/O contracts (more boilerplate but safer)
3. **Abstractions**: Lower-level, more control but more code
4. **Ecosystem**: Smaller (but production-focused)

### Migration Example

**Before (LangChain)**:
```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

# LCEL chain
llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_template("Summarize: {text}")
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"text": long_document})
```

**After (Haystack)**:
```python
from haystack import Pipeline
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder

# Explicit pipeline
pipeline = Pipeline()

# Components
prompt_builder = PromptBuilder(template="Summarize: {{text}}")
generator = OpenAIGenerator(model="gpt-4")

# Add components
pipeline.add_component("prompt_builder", prompt_builder)
pipeline.add_component("generator", generator)

# Connect (explicit I/O)
pipeline.connect("prompt_builder", "generator")

# Run
result = pipeline.run({"prompt_builder": {"text": long_document}})
summary = result["generator"]["replies"][0]
```

### Migration Effort: 4-8 weeks

**Migration Steps**:

1. **Week 1-2: Architecture Redesign**
   - Map LangChain chains to Haystack pipelines
   - Identify reusable components
   - Design pipeline architecture
   - Create component inventory

2. **Week 3-4: Core Migration**
   - Implement Haystack pipelines for core features
   - Migrate prompts (portable)
   - Update configuration management
   - Unit testing

3. **Week 5-6: Integration**
   - API endpoint updates
   - Database/vector store integration
   - Observability setup
   - Integration testing

4. **Week 7-8: Validation & Cutover**
   - Load testing
   - Performance benchmarking
   - Gradual rollout (10% → 25% → 50% → 100%)
   - Monitor and optimize

**Code Rewrite Required**: 60-80%
- Pipelines need redesign (not 1:1 mapping)
- Component wrappers for existing logic
- New testing approach

**Common Pitfalls**:
1. **Underestimating complexity**: Haystack is more explicit/verbose
2. **Missing LangChain features**: Some LangChain features don't exist in Haystack
3. **Team learning curve**: Team needs training on Haystack patterns
4. **Observability gap**: LangSmith equivalent needs custom implementation

**Mitigation**:
- Start with pilot feature (not full migration)
- Budget for team training (1-2 weeks)
- Build observability infrastructure early
- Keep LangChain for non-critical features initially

**ROI Analysis**:
```
Migration Cost: 4-8 weeks × team cost
Ongoing Savings:
- Maintenance: 20-30% less (fewer breaking changes)
- Performance: 5-15% cost savings (token efficiency)
- Reliability: Fewer production incidents

Break-even: 6-12 months
```

## Migration Scenario 4: LangChain → Semantic Kernel (Azure)

### When to Migrate

**Migrate to Semantic Kernel when**:
- Moving to Azure cloud (Azure OpenAI, Azure AI)
- .NET or Java primary languages
- Need Microsoft enterprise support and SLAs
- M365 integration required (Teams, SharePoint)
- Compliance/security built-in (Microsoft certifications)

**Don't migrate if**:
- Python-only team
- Multi-cloud strategy (AWS, GCP)
- Not in Microsoft ecosystem

### Migration Example

**Before (LangChain, Python)**:
```python
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

llm = ChatOpenAI(model="gpt-4")
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

response = conversation.predict(input="Hello")
```

**After (Semantic Kernel, C#)**:
```csharp
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;

// Build kernel
var kernel = Kernel.CreateBuilder()
    .AddAzureOpenAIChatCompletion(
        deploymentName: "gpt-4",
        endpoint: azureEndpoint,
        apiKey: azureApiKey
    )
    .Build();

// Chat history (memory)
var chatHistory = new ChatHistory();
chatHistory.AddSystemMessage("You are a helpful assistant");

// Conversation
chatHistory.AddUserMessage("Hello");

var response = await kernel.InvokePromptAsync(
    chatHistory.ToString(),
    new KernelArguments()
);

chatHistory.AddAssistantMessage(response.ToString());
```

### Migration Effort: 4-8 weeks + Language Migration

**Additional Complexity**: If migrating from Python to C#/Java

**Migration Steps**:

1. **Week 1-2: Setup + POC**
   - Set up Azure resources (Azure OpenAI, Key Vault, etc.)
   - C#/.NET environment setup
   - Port single feature to Semantic Kernel
   - Team training on SK concepts

2. **Week 3-4: Core Features**
   - Migrate prompts (portable)
   - Implement memory/state management
   - Tool/function calling
   - Testing infrastructure

3. **Week 5-6: Azure Integration**
   - Managed Identity setup
   - Key Vault integration
   - Application Insights (monitoring)
   - Azure AI services integration

4. **Week 7-8: Deployment**
   - Azure deployment (AKS, App Service)
   - CI/CD pipelines
   - Load testing
   - Gradual rollout

**Code Portability**:
- **Prompts**: 100% portable
- **Logic**: 0% (language change)
- **Architecture**: 30-50% concepts transfer
- **Data**: 100% portable

**Risks**: Moderate-High
- Language change adds complexity
- Team needs .NET training
- Azure-specific knowledge required
- More expensive initially (learning curve)

## Migration Scenario 5: Framework → Direct API (Simplification)

### When to Migrate Back to Direct API

**Migrate away from framework when**:
1. Use case simplified (no longer need framework features)
2. Framework overhead outweighs benefits
3. Performance critical and framework adds latency
4. Team prefers simplicity over abstraction
5. Breaking changes causing too much maintenance

### Migration Example

**Before (LangChain)**:
```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_template("Translate {text} to {language}")
chain = LLMChain(llm=llm, prompt=prompt)

result = chain.invoke({"text": "Hello", "language": "Spanish"})
```

**After (Direct API)**:
```python
import openai

def translate(text: str, language: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Translate {text} to {language}"}
        ]
    )
    return response.choices[0].message.content

result = translate("Hello", "Spanish")
```

### Migration Effort: 1-2 weeks

**Benefits**:
- Simpler code (easier to understand)
- No framework dependencies
- Direct control over API calls
- Faster execution (no framework overhead)

**Losses**:
- No abstraction (harder to swap models)
- Manual error handling
- No built-in observability
- Reinvent wheels (caching, retries, etc.)

**When it makes sense**:
- Simple use cases (single LLM calls)
- Performance critical paths
- Temporary prototypes
- Microservices with single responsibility

## Migration Best Practices

### 1. Run in Parallel (Shadow Mode)

```python
# Run both old and new implementations
# Compare results before cutover

def process_query(query: str):
    # Old implementation (production)
    old_result = langchain_pipeline.run(query)

    # New implementation (shadow)
    try:
        new_result = llamaindex_pipeline.run(query)

        # Compare and log differences
        if old_result != new_result:
            log_difference(query, old_result, new_result)

    except Exception as e:
        # Log errors in new implementation
        log_shadow_error(query, e)

    # Return old result (no user impact)
    return old_result
```

### 2. Feature Flags for Gradual Rollout

```python
import os

MIGRATION_PERCENTAGE = int(os.getenv("MIGRATION_PERCENTAGE", "0"))

def should_use_new_framework(user_id: str) -> bool:
    """Gradually roll out to percentage of users"""
    user_hash = hash(user_id) % 100
    return user_hash < MIGRATION_PERCENTAGE

def process_query(user_id: str, query: str):
    if should_use_new_framework(user_id):
        return new_framework_pipeline.run(query)
    else:
        return old_framework_pipeline.run(query)

# Start with MIGRATION_PERCENTAGE=1 (1% of users)
# Gradually increase: 5% → 10% → 25% → 50% → 100%
```

### 3. Comprehensive Testing

```python
# tests/test_migration.py
import pytest

@pytest.fixture
def test_queries():
    """Representative test queries"""
    return [
        "What is the company policy on X?",
        "How do I file an expense report?",
        # ... 100+ real queries
    ]

def test_parity(test_queries):
    """Ensure new framework matches old results"""
    for query in test_queries:
        old_result = old_framework.run(query)
        new_result = new_framework.run(query)

        # Semantic similarity (not exact match)
        similarity = calculate_similarity(old_result, new_result)
        assert similarity > 0.9, f"Result mismatch for: {query}"

def test_performance(test_queries):
    """Ensure new framework meets performance targets"""
    import time

    for query in test_queries:
        start = time.time()
        new_framework.run(query)
        latency = time.time() - start

        assert latency < 2.0, f"Latency too high: {latency}s"

def test_cost(test_queries):
    """Ensure new framework doesn't increase costs"""
    old_cost = estimate_cost(old_framework, test_queries)
    new_cost = estimate_cost(new_framework, test_queries)

    assert new_cost <= old_cost * 1.1, "Cost increased by >10%"
```

### 4. Rollback Plan

```python
# Always have a rollback plan

def rollback_to_old_framework():
    """Instant rollback if new framework fails"""
    # Set feature flag to 0%
    os.environ["MIGRATION_PERCENTAGE"] = "0"

    # Or use infrastructure rollback
    # kubectl rollout undo deployment/ai-service

    # Alert team
    send_alert("Rolled back to old framework due to errors")

# Monitor error rates
if error_rate > threshold:
    rollback_to_old_framework()
```

### 5. Document Everything

```markdown
# Migration Runbook

## Pre-Migration Checklist
- [ ] Parallel implementation tested
- [ ] Performance benchmarks meet targets
- [ ] Cost analysis completed
- [ ] Team trained on new framework
- [ ] Rollback plan documented
- [ ] Monitoring dashboards updated

## Migration Steps
1. Enable shadow mode (0% user traffic)
2. Monitor for 1 week
3. Gradual rollout: 1% → 5% → 10% → 25% → 50%
4. Each step: monitor for 24-48 hours
5. If error rate <0.1%, proceed to next step
6. If error rate >0.1%, rollback and investigate

## Success Metrics
- Latency p95 < 2s
- Error rate < 0.1%
- Cost increase < 10%
- User satisfaction maintained

## Rollback Triggers
- Error rate > 0.5%
- Latency p95 > 5s
- User complaints > baseline
- Production incident
```

## Common Migration Pitfalls

### Pitfall 1: Big Bang Migration

**Problem**: Migrating everything at once

**Solution**: Incremental migration
- Start with single feature
- Prove value before scaling
- Learn from early mistakes

### Pitfall 2: Underestimating Effort

**Problem**: "Should take 1 week" → takes 2 months

**Solution**: Conservative estimates
- Add 50-100% buffer to estimates
- Account for unknowns
- Include testing and validation time

### Pitfall 3: Ignoring Team Training

**Problem**: Team struggles with new framework

**Solution**: Invest in training
- 1-2 weeks dedicated training time
- Hands-on workshops
- Documentation and examples
- Pair programming during migration

### Pitfall 4: No Rollback Plan

**Problem**: Migration fails, can't roll back

**Solution**: Always have rollback ready
- Keep old code running
- Feature flags for instant rollback
- Test rollback procedure

### Pitfall 5: Optimizing Too Early

**Problem**: Migrating for minor performance gains

**Solution**: Validate need first
- Profile current system
- Quantify actual benefit
- Consider opportunity cost

## Migration Decision Matrix

| Current | Target | Effort | Risk | ROI | Recommendation |
|---------|--------|--------|------|-----|----------------|
| Direct API | LangChain | Low | Low | High | **Do it** if need chains/memory |
| LangChain | LlamaIndex (RAG) | Moderate | Low | High | **Do it** if RAG-focused |
| LangChain | Haystack | High | Moderate | Moderate | **Consider** if stability critical |
| LangChain | Semantic Kernel | High | Moderate | High | **Do it** if Azure/Microsoft stack |
| LangChain | DSPy | Moderate | High | Low | **Avoid** (research-phase) |
| Any | Direct API | Low | Low | Moderate | **Consider** for simplification |

## Summary

**Key Takeaways**:

1. **Migrate for right reasons**: Use case fit, stability, performance - not hype
2. **Estimate conservatively**: 2-8 weeks typical, add 50-100% buffer
3. **Run in parallel**: Shadow mode before cutover
4. **Gradual rollout**: 1% → 5% → 10% → 25% → 50% → 100%
5. **Always have rollback**: Test rollback before migration
6. **Invest in testing**: Comprehensive test suite essential
7. **Train team**: Budget 1-2 weeks for team training
8. **Monitor closely**: Watch metrics during and after migration
9. **Document thoroughly**: Migration runbook, architecture docs
10. **Learn from others**: Read migration case studies, ask community

**Most Common Migrations**:
1. Direct API → LangChain (complexity threshold)
2. LangChain → LlamaIndex (RAG specialization)
3. LangChain → Haystack (production stability)
4. Framework → Direct API (simplification)

**Avoid These Migrations**:
1. Between frameworks without clear benefit
2. Before validating product-market fit
3. During critical business periods
4. Without team buy-in

**Migration is a means, not an end. Only migrate when the benefit clearly outweighs the cost.**
