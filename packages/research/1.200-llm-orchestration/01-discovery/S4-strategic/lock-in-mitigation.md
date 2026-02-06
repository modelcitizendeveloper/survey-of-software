# Avoiding Framework Lock-In: Mitigation Strategies

## Executive Summary

This document provides comprehensive strategies for avoiding vendor/framework lock-in when using LLM orchestration frameworks (LangChain, LlamaIndex, Haystack, Semantic Kernel, DSPy). It covers lock-in risks, portability strategies, exit strategies, and best practices for maintaining flexibility.

**Key Findings**:
- **Lock-in is relatively low** compared to cloud platforms (AWS, Azure) - prompts and patterns are transferable
- **Medium lock-in risk**: Framework-specific APIs, integrations, observability tooling
- **Mitigation requires upfront work**: Abstraction layers, separate prompts, architecture documentation
- **Migration cost**: 2-4 weeks (50-100 hours) for typical application if properly architected
- **Best practice**: Abstract framework behind interface (adapter pattern), keep prompts separate, test portability

---

## 1. Lock-In Risks Assessment

### Low Lock-In (Fully Portable)

**1. Prompts**:
- **Risk Level**: Very Low (5% lock-in)
- **Portability**: 100% (prompts are text, framework-agnostic)
- **Migration Effort**: 0 hours (copy-paste prompts to new framework)

**Example**:
```python
# Prompt is plain text (works in any framework)
prompt = "You are a helpful assistant. Answer the following question: {question}"

# LangChain
chain = LangChain(prompt=prompt)

# LlamaIndex
index = LlamaIndex(prompt=prompt)

# Haystack
pipeline = Haystack(prompt=prompt)

# Fully portable across frameworks
```

**Best Practice**: Store prompts in separate files (YAML, JSON) independent of framework code.

---

**2. Model Calls (Model-Agnostic)**:
- **Risk Level**: Very Low (5% lock-in)
- **Portability**: 95% (all frameworks support OpenAI, Anthropic, local models)
- **Migration Effort**: 1-2 hours (update model initialization code)

**Example**:
```python
# All frameworks support same models
model = "gpt-4"  # OpenAI
model = "claude-3-opus"  # Anthropic
model = "llama-3-70b"  # Local via Ollama

# LangChain
llm = ChatOpenAI(model="gpt-4")

# LlamaIndex
llm = OpenAI(model="gpt-4")

# Haystack
llm = OpenAIGenerator(model="gpt-4")

# Model choice portable (all frameworks support same providers)
```

**Best Practice**: Use environment variables for model names (easy to switch).

---

**3. Architecture Patterns (Conceptually Transferable)**:
- **Risk Level**: Low (15% lock-in)
- **Portability**: 85% (chains, agents, RAG concepts exist in all frameworks)
- **Migration Effort**: 5-10 hours (reimplement pattern in new framework)

**Example**:
```python
# Pattern: Chains (sequential LLM calls)
# LangChain
chain = LLMChain(prompt1) | LLMChain(prompt2)

# LlamaIndex
pipeline = QueryPipeline([node1, node2])

# Haystack
pipeline = Pipeline([component1, component2])

# Same concept (chains), different API (rewrite required, but concept portable)
```

**Best Practice**: Document architecture patterns in framework-agnostic language ("We use ReAct pattern for agents", not "We use LangGraph").

---

### Medium Lock-In (Effort to Migrate)

**1. Framework-Specific APIs**:
- **Risk Level**: Medium (40% lock-in)
- **Portability**: 60% (requires rewriting code, but concepts transfer)
- **Migration Effort**: 50-100 hours (rewrite chains, agents, RAG in new framework)

**Example**:
```python
# LangChain-specific API (not portable)
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template("Question: {question}")
)
result = chain.run(question="What is AI?")

# To migrate to LlamaIndex, must rewrite:
from llama_index import VectorStoreIndex

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
result = query_engine.query("What is AI?")

# Different API, same result (rewrite required)
```

**Mitigation**: Abstract framework behind interface (see section 2).

---

**2. Integrations (Vector DBs, Tools, APIs)**:
- **Risk Level**: Medium (35% lock-in)
- **Portability**: 65% (most integrations supported by multiple frameworks)
- **Migration Effort**: 10-20 hours (rewrite integration code)

**Example**:
```python
# LangChain integration (framework-specific)
from langchain.vectorstores import Pinecone

vectorstore = Pinecone.from_documents(documents, embeddings)

# LlamaIndex equivalent (different API)
from llama_index.vector_stores import PineconeVectorStore

vector_store = PineconeVectorStore(pinecone_index)

# Same vector DB (Pinecone), different framework API (rewrite required)
```

**Mitigation**: Use standard vector DB clients when possible (e.g., Pinecone SDK directly, not framework wrapper).

---

**3. Observability Tools (LangSmith, Langfuse, Phoenix)**:
- **Risk Level**: Medium (30% lock-in)
- **Portability**: 70% (observability concepts transfer, but tooling specific)
- **Migration Effort**: 10-20 hours (setup new observability, migrate dashboards)

**Example**:
```python
# LangSmith (LangChain observability)
from langsmith import Client

client = Client()
# Tracing LangChain chains automatically

# If migrate to LlamaIndex, must use different tool:
# - Langfuse (framework-agnostic)
# - Phoenix (Arize AI)
# - Or build custom logging

# Observability data not portable (historical traces lost)
```

**Mitigation**: Use framework-agnostic observability (Langfuse supports multiple frameworks).

---

### High Lock-In (Difficult to Migrate)

**1. Framework-Specific Features (LangGraph, Query Engines, etc.)**:
- **Risk Level**: High (60% lock-in)
- **Portability**: 40% (requires significant rewrite, some features may not exist in other frameworks)
- **Migration Effort**: 50-100 hours (reimplement complex features)

**Example**:
```python
# LangGraph (LangChain-specific state machines)
from langgraph.graph import StateGraph

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tools_node)
graph.add_edge("agent", "tools")
# Complex state machine logic (100+ lines)

# No direct equivalent in LlamaIndex, Haystack
# Must reimplement from scratch or simplify architecture
```

**Mitigation**: Minimize use of framework-specific advanced features. Use when absolutely necessary, but recognize migration cost.

---

**2. Commercial Tooling (LangSmith Data, LlamaCloud)**:
- **Risk Level**: High (70% lock-in)
- **Portability**: 30% (data not easily exported, tooling proprietary)
- **Migration Effort**: 20-40 hours (export data, rebuild dashboards, lose historical data)

**Example**:
```python
# LangSmith (commercial observability, proprietary data)
# - Traces stored in LangSmith (proprietary format)
# - Dashboards built in LangSmith UI
# - No easy export to Langfuse or Phoenix

# If migrate framework, lose:
# - Historical traces (can export, but format different)
# - Dashboards (must rebuild)
# - Team collaboration features (LangSmith-specific)
```

**Mitigation**: Use open-source observability (Langfuse) or export data regularly (if LangSmith provides export API).

---

**3. Team Knowledge and Training**:
- **Risk Level**: High (50% lock-in)
- **Portability**: 50% (team must learn new framework, concepts transfer but APIs don't)
- **Migration Effort**: 20-40 hours per team member (learning new framework)

**Example**:
- Team trained on LangChain (40 hours training investment)
- If migrate to LlamaIndex, must retrain (20-30 hours per developer)
- Loss: Expertise in LangChain-specific patterns (LangGraph, LCEL)
- Gain: Expertise in LlamaIndex patterns (query engines, RAG specialization)

**Mitigation**: Focus training on transferable patterns (chains, agents, RAG) rather than framework-specific APIs.

---

### Overall Lock-In Assessment

**Compared to Cloud Platforms**:
- **LLM Frameworks**: Low-Medium lock-in (60-70% portable)
- **Cloud Platforms (AWS, Azure)**: High lock-in (30-40% portable)

**Migration Feasibility**:
- **LLM Framework Migration**: 2-4 weeks (50-100 hours) for typical application
- **Cloud Migration (AWS → Azure)**: 6-12 months (1000+ hours) for typical application

**Conclusion**: LLM framework lock-in is **relatively low** compared to cloud platforms. Most teams can migrate frameworks in 2-4 weeks if needed.

---

## 2. Portability Strategies

### Strategy 1: Abstract Framework Behind Interface (Adapter Pattern)

**Concept**: Wrap framework in abstraction layer (interface) so swapping frameworks only requires changing adapter.

**Implementation**:

```python
# Step 1: Define framework-agnostic interface
from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMOrchestrator(ABC):
    """Framework-agnostic interface for LLM orchestration"""

    @abstractmethod
    def run_chain(self, input: str, **kwargs) -> str:
        """Run LLM chain and return result"""
        pass

    @abstractmethod
    def run_rag_query(self, query: str, **kwargs) -> str:
        """Run RAG query and return result"""
        pass

    @abstractmethod
    def run_agent(self, task: str, tools: list, **kwargs) -> str:
        """Run agent with tools and return result"""
        pass


# Step 2: Implement adapter for LangChain
from langchain.chains import LLMChain
from langchain.agents import AgentExecutor

class LangChainOrchestrator(LLMOrchestrator):
    """LangChain-specific implementation"""

    def __init__(self, llm, prompts):
        self.llm = llm
        self.prompts = prompts
        # Initialize LangChain components
        self.chain = LLMChain(llm=self.llm, prompt=self.prompts['chain'])

    def run_chain(self, input: str, **kwargs) -> str:
        return self.chain.run(input=input)

    def run_rag_query(self, query: str, **kwargs) -> str:
        # LangChain RAG implementation
        pass

    def run_agent(self, task: str, tools: list, **kwargs) -> str:
        # LangChain agent implementation
        pass


# Step 3: Implement adapter for LlamaIndex
from llama_index import VectorStoreIndex

class LlamaIndexOrchestrator(LLMOrchestrator):
    """LlamaIndex-specific implementation"""

    def __init__(self, llm, prompts):
        self.llm = llm
        self.prompts = prompts
        # Initialize LlamaIndex components

    def run_chain(self, input: str, **kwargs) -> str:
        # LlamaIndex chain implementation (different API, same interface)
        pass

    def run_rag_query(self, query: str, **kwargs) -> str:
        # LlamaIndex RAG implementation
        pass

    def run_agent(self, task: str, tools: list, **kwargs) -> str:
        # LlamaIndex agent implementation
        pass


# Step 4: Factory pattern to switch frameworks easily
def get_orchestrator(framework: str = "langchain") -> LLMOrchestrator:
    """Factory to create orchestrator (framework-agnostic)"""

    prompts = load_prompts()  # Load from YAML (framework-agnostic)
    llm = get_llm()  # Model initialization (framework-agnostic)

    if framework == "langchain":
        return LangChainOrchestrator(llm, prompts)
    elif framework == "llamaindex":
        return LlamaIndexOrchestrator(llm, prompts)
    elif framework == "haystack":
        return HaystackOrchestrator(llm, prompts)
    else:
        raise ValueError(f"Unknown framework: {framework}")


# Step 5: Use framework-agnostic interface in application code
# Application code (framework-agnostic)
orchestrator = get_orchestrator(framework="langchain")  # or "llamaindex"
result = orchestrator.run_chain(input="What is AI?")
print(result)

# To switch frameworks, change only get_orchestrator() parameter
# No changes to application code required
```

**Benefits**:
- **Low migration cost**: Change only adapter (10-20 hours), not application code (0 hours)
- **Test portability**: Can run tests against multiple adapters (ensure portability)
- **Future-proof**: Easy to add new framework adapters (Haystack, Semantic Kernel)

**Drawbacks**:
- **Upfront cost**: 20-40 hours to build abstraction layer
- **Least common denominator**: Interface limited to features supported by all frameworks
- **Performance**: Abstraction layer adds minimal overhead (~1-2ms)

**When to Use**:
- Production applications (long-lived, worth investment)
- Teams of 4+ developers (shared interface improves consistency)
- High framework migration risk (40%+ probability of switching)

**When NOT to Use**:
- Prototypes or MVPs (abstraction overkill)
- Solo developer (simpler to rewrite than abstract)
- Low migration risk (95%+ staying with current framework)

---

### Strategy 2: Keep Prompts Separate from Framework Code

**Concept**: Store prompts in separate files (YAML, JSON) independent of framework code.

**Implementation**:

```yaml
# prompts.yaml (framework-agnostic)
prompts:
  question_answering:
    system: "You are a helpful assistant."
    user: "Question: {question}\n\nAnswer:"

  summarization:
    system: "You are a summarization expert."
    user: "Summarize the following text:\n\n{text}"

  rag_query:
    system: "Answer based on the provided context."
    user: |
      Context: {context}

      Question: {question}

      Answer:
```

```python
# Load prompts (framework-agnostic)
import yaml

def load_prompts():
    with open("prompts.yaml", "r") as f:
        return yaml.safe_load(f)

prompts = load_prompts()

# Use in LangChain
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", prompts['prompts']['question_answering']['system']),
    ("user", prompts['prompts']['question_answering']['user'])
])

# Use in LlamaIndex (same prompts, different framework)
from llama_index.prompts import PromptTemplate

prompt = PromptTemplate(
    prompts['prompts']['question_answering']['system'] +
    prompts['prompts']['question_answering']['user']
)

# Prompts portable (just load from YAML in new framework)
```

**Benefits**:
- **Zero migration cost for prompts**: Copy prompts.yaml to new framework project (0 hours)
- **Version control**: Git tracks prompt changes (independent of code)
- **A/B testing**: Easy to test multiple prompt versions (switch YAML file)
- **Non-technical editing**: Product managers can edit prompts (no code changes)

**Drawbacks**:
- **Two files to manage**: prompts.yaml + code (minor complexity)
- **Less IDE support**: No autocomplete for prompts in YAML (vs inline)

**When to Use**:
- All production applications (always separate prompts, best practice)
- Multiple prompt versions (A/B testing, experimentation)
- Non-technical team members edit prompts (product, design)

**When NOT to Use**:
- Quick prototypes (inline prompts faster for iteration)
- Single-use scripts (overkill for one-off tasks)

---

### Strategy 3: Document Architecture Patterns (Framework-Agnostic)

**Concept**: Document system architecture using framework-agnostic language (patterns, not framework APIs).

**Implementation**:

```markdown
# System Architecture (Framework-Agnostic)

## Overview
Our LLM application uses a RAG (Retrieval-Augmented Generation) architecture with agentic capabilities.

## Core Patterns

### 1. RAG Pattern
- **Embedding**: Documents embedded using OpenAI text-embedding-ada-002
- **Storage**: Vectors stored in Pinecone (1536 dimensions)
- **Retrieval**: Top-5 semantic search with cosine similarity
- **Reranking**: Cohere reranker (top-3 from top-5)
- **Generation**: GPT-4 with context injection (max 3k context tokens)

**Current Implementation**: LangChain (but pattern portable to LlamaIndex, Haystack)

### 2. Agent Pattern
- **Type**: ReAct (Reasoning + Acting)
- **Tools**: Database query, API call, web search
- **Planning**: LLM generates plan → executes → validates → repeats
- **Termination**: Max 5 iterations or task complete

**Current Implementation**: LangGraph (but ReAct pattern portable to other frameworks)

### 3. Memory Pattern
- **Short-term**: Last 10 messages in conversation buffer
- **Long-term**: Conversation summaries stored in vector DB
- **Retrieval**: Semantic search over past conversations (top-3)

**Current Implementation**: LangChain ConversationBufferMemory (but pattern portable)

## Migration Path
To migrate to different framework:
1. Reimplement RAG pattern (50-100 lines)
2. Reimplement ReAct agent (100-150 lines)
3. Reimplement memory (30-50 lines)
**Estimated migration effort**: 2-3 weeks

## Dependencies (Framework-Specific)
- LangChain==0.1.9
- LangGraph==0.0.20
- Pinecone SDK==2.0.0 (framework-agnostic, portable)
- OpenAI SDK==1.12.0 (framework-agnostic, portable)
```

**Benefits**:
- **Transfer knowledge**: New team members understand architecture (not just code)
- **Migration planning**: Document estimates migration effort upfront (2-3 weeks)
- **Framework-agnostic**: Architecture persists even if framework changes

**Drawbacks**:
- **Maintenance**: Must update docs when architecture changes (can drift from code)

**When to Use**:
- All production applications (documentation is best practice)
- Teams of 4+ developers (shared understanding critical)
- Complex architectures (RAG + agents + memory)

**When NOT to Use**:
- Simple prototypes (overkill for 50-line scripts)
- Solo developer (you already know the architecture)

---

### Strategy 4: Use Standard Data Formats (JSON, Pydantic)

**Concept**: Use standard data formats (JSON, Pydantic models) for data interchange, not framework-specific formats.

**Implementation**:

```python
# Framework-agnostic data model (Pydantic)
from pydantic import BaseModel
from typing import List

class Document(BaseModel):
    """Framework-agnostic document model"""
    text: str
    metadata: dict
    embedding: List[float] = None

class QueryResult(BaseModel):
    """Framework-agnostic query result"""
    answer: str
    sources: List[Document]
    confidence: float


# Use in LangChain
from langchain.schema import Document as LangChainDoc

def to_langchain_doc(doc: Document) -> LangChainDoc:
    return LangChainDoc(page_content=doc.text, metadata=doc.metadata)

# Use in LlamaIndex
from llama_index.schema import Document as LlamaIndexDoc

def to_llamaindex_doc(doc: Document) -> LlamaIndexDoc:
    return LlamaIndexDoc(text=doc.text, metadata=doc.metadata)

# Data model portable (just convert to framework-specific format)
```

**Benefits**:
- **Data portability**: Standard formats (JSON, Pydantic) work across frameworks
- **Testing**: Easy to test with known data (JSON fixtures)
- **API boundaries**: If multiple services, JSON API is framework-agnostic

**Drawbacks**:
- **Conversion overhead**: Must convert between standard and framework-specific formats (minor)

**When to Use**:
- Multi-service architectures (API boundaries)
- Testing (fixtures in JSON)
- Data persistence (store in standard format, not framework-specific)

**When NOT to Use**:
- Monolithic applications (conversion overhead not worth it)

---

### Strategy 5: Test with Multiple Frameworks (Proof of Portability)

**Concept**: Maintain implementations in 2+ frameworks to prove portability.

**Implementation**:

```python
# Test portability by implementing in multiple frameworks

# 1. Implement in LangChain (primary)
from langchain.chains import LLMChain

langchain_result = LLMChain(llm=llm, prompt=prompt).run(input="Test")

# 2. Implement same logic in LlamaIndex (secondary, for testing)
from llama_index import VectorStoreIndex

llamaindex_result = VectorStoreIndex.from_documents(docs).query("Test")

# 3. Assert outputs match (prove portability)
assert langchain_result == llamaindex_result  # Or similar (minor differences OK)

# If outputs match, portability proven (migration feasible)
```

**Benefits**:
- **Proof of portability**: If 2+ implementations exist, migration is low-risk
- **Catch lock-in early**: If can't implement in second framework, identify lock-in
- **Fallback option**: If primary framework fails, secondary works (redundancy)

**Drawbacks**:
- **Double maintenance**: Maintain 2+ implementations (2x effort)
- **Only for critical paths**: Too expensive to do for entire application

**When to Use**:
- Critical business logic (worth redundancy)
- High migration risk (40%+ probability of switching frameworks)
- Evaluating frameworks (prototype in 2+, choose best)

**When NOT to Use**:
- Low migration risk (95%+ staying with current framework)
- Non-critical code (not worth double maintenance)
- Resource-constrained teams (1-2 developers, no capacity for redundancy)

---

## 3. Exit Strategies

### Strategy 1: Framework → Direct API Migration

**Scenario**: Migrating from framework (LangChain) to direct API calls (OpenAI SDK).

**When to Do It**:
- Performance critical (framework overhead 3-10ms unacceptable)
- Simplification (project actually needs only 1-2 LLM calls, framework overkill)
- Security/compliance (too many framework dependencies)
- Cost optimization (framework token overhead +1.5k-2.4k tokens too expensive)

**Migration Path**:

```
Week 1: Identify core prompts and LLM calls
- Audit all LLM calls (what prompts, what models, what parameters)
- Extract prompts to separate files (YAML)
- Document current behavior (outputs, edge cases)

Week 2: Rewrite main flow with direct API
- Rewrite chains as sequential API calls
- Rewrite RAG as manual retrieval + API call
- Rewrite agents as loop (plan → execute → validate)

Week 3: Implement custom error handling and retries
- Add retry logic (exponential backoff)
- Add timeout handling
- Add error classification (rate limit vs API error)

Week 4: Build lightweight observability (logging)
- Add logging for all LLM calls (input, output, latency, cost)
- Build simple dashboard (log aggregation)
- Monitor in production (ensure behavior matches old framework)

Week 5: Test and deploy, remove framework dependency
- Parallel run (old framework + new direct API)
- Compare outputs (should match)
- Cut over to direct API
- Remove framework dependency (uninstall package)
```

**Effort**: 3-6 weeks (120-240 hours) for typical migration

**Example**:

```python
# Before: LangChain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template("Question: {question}")
)
result = chain.run(question="What is AI?")

# After: Direct API
import openai
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def call_llm(prompt: str, model: str = "gpt-4") -> str:
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        timeout=30
    )
    return response.choices[0].message.content

# Use
question = "What is AI?"
prompt = f"Question: {question}"
result = call_llm(prompt)

# Same result, but 80+ lines to reimplement error handling, retries, logging
```

**Warning**: Most teams regret this migration (framework → direct API is more work than expected). Only do if absolutely necessary.

---

### Strategy 2: Framework A → Framework B Migration

**Scenario**: Migrating from one framework to another (e.g., LangChain → LlamaIndex).

**When to Do It**:
- Better framework for use case (RAG use case → LlamaIndex 35% better)
- Performance requirements (need Haystack 5.9ms overhead vs LangChain 10ms)
- Stability issues (LangChain breaking changes too frequent → Semantic Kernel stable)
- Acquisition/abandonment (framework shut down, must migrate)

**Migration Path**:

```
Week 1: Choose new framework and learn basics
- Evaluate alternatives (LlamaIndex, Haystack, Semantic Kernel)
- Learn new framework (tutorials, documentation)
- Prototype simple chain in new framework (proof of concept)

Week 2: Rewrite main flow in new framework
- Rewrite chains (sequential LLM calls)
- Rewrite RAG (retrieval + generation)
- Rewrite agents (tool calling, planning)

Week 3: Migrate integrations (vector DBs, tools)
- Rewrite Pinecone integration in new framework
- Rewrite API tool integrations
- Test integrations (ensure same behavior)

Week 4: Setup observability in new framework
- Setup Langfuse (framework-agnostic) or new framework's observability
- Migrate dashboards (rebuild in new tool)
- Historical data (export from old tool if possible)

Week 5: Test and deploy
- Parallel run (old framework + new framework)
- Compare outputs (should match)
- Cut over to new framework
- Remove old framework dependency

Week 6: Clean up and optimize
- Remove old framework code
- Optimize new framework (performance tuning)
- Document new architecture
```

**Effort**: 2-4 weeks (50-100 hours) for typical migration

**Example**:

```python
# Before: LangChain
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone

vectorstore = Pinecone.from_documents(documents, embeddings)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
result = qa_chain.run("What is AI?")

# After: LlamaIndex
from llama_index import VectorStoreIndex
from llama_index.vector_stores import PineconeVectorStore

vector_store = PineconeVectorStore(pinecone_index)
index = VectorStoreIndex.from_vector_store(vector_store)
query_engine = index.as_query_engine()
result = query_engine.query("What is AI?")

# Same result, different API (rewrite required, but concepts transfer)
```

**Effort Estimate by Application Size**:
- Small (< 500 lines): 1 week (40 hours)
- Medium (500-2000 lines): 2-3 weeks (80-120 hours)
- Large (2000+ lines): 4-6 weeks (160-240 hours)

---

### Strategy 3: Gradual Migration (Brownfield Approach)

**Scenario**: Migrate framework gradually (not all at once).

**When to Do It**:
- Large application (2000+ lines, too risky for big-bang migration)
- Production system (can't afford downtime)
- Team capacity limited (can't dedicate 4+ weeks to migration)

**Migration Path**:

```
Phase 1 (Week 1-2): Setup new framework alongside old
- Install new framework (LlamaIndex) alongside old (LangChain)
- Create abstraction layer (adapter pattern from section 2)
- Route 10% of traffic to new framework (canary deployment)

Phase 2 (Week 3-4): Migrate one component at a time
- Migrate RAG component to new framework (test, deploy)
- Keep chains in old framework (gradual migration)
- Monitor: Compare outputs (old vs new framework)

Phase 3 (Week 5-6): Migrate second component
- Migrate agent component to new framework
- Keep memory in old framework (if needed)

Phase 4 (Week 7-8): Complete migration
- Migrate remaining components (memory, etc.)
- Remove old framework dependency
- Clean up abstraction layer (if no longer needed)
```

**Benefits**:
- **Lower risk**: Migrate one component at a time (catch issues early)
- **No downtime**: Old framework still running (gradual cutover)
- **Reversible**: If new framework has issues, roll back to old

**Drawbacks**:
- **Longer timeline**: 2x-3x longer than big-bang migration (6-8 weeks vs 2-4 weeks)
- **Complexity**: Running 2 frameworks simultaneously (more dependencies)
- **Testing overhead**: Must test both old and new framework

**When to Use**:
- Large production applications (2000+ lines)
- Risk-averse teams (can't afford big-bang failures)
- Limited capacity (1-2 developers, can't dedicate full time)

**When NOT to Use**:
- Small applications (< 500 lines, big-bang faster)
- Greenfield projects (no legacy code, start fresh)

---

## 4. Best Practices for Lock-In Mitigation

### Practice 1: Don't Over-Invest in Framework-Specific Features

**Guideline**: Use framework-specific features only when absolutely necessary (recognize migration cost).

**Examples**:

**Good** (Use Framework-Specific if High Value):
- LangGraph state machines (complex agent workflows, worth investment)
- LlamaIndex advanced retrievers (35% RAG accuracy boost, worth investment)
- Haystack custom components (production performance, worth investment)

**Bad** (Avoid Framework-Specific if Low Value):
- LangChain LCEL (Expression Language) for simple chains (overkill, use basic chains)
- LlamaIndex query engines for non-RAG (use simple chains instead)
- Framework-specific utilities (e.g., LangChain text splitters → use tiktoken directly)

**Decision Framework**:
```
If framework-specific feature provides:
- High value (20%+ improvement in key metric) → Use it (worth lock-in risk)
- Medium value (5-20% improvement) → Consider alternatives (weigh value vs lock-in)
- Low value (< 5% improvement) → Avoid (not worth lock-in risk)
```

---

### Practice 2: Maintain Framework-Agnostic Core Logic

**Guideline**: Keep business logic separate from framework code (framework is infrastructure, not business logic).

**Architecture**:

```
Application Architecture (Layers)

┌─────────────────────────────────────┐
│   Business Logic (Framework-Agnostic)   │  ← Core domain logic (prompts, rules)
├─────────────────────────────────────┤
│   Orchestration Interface (Adapter)     │  ← Abstraction layer (adapter pattern)
├─────────────────────────────────────┤
│   Framework Layer (LangChain, etc.)      │  ← Framework-specific code (can swap)
└─────────────────────────────────────┘
```

**Example**:

```python
# Business logic (framework-agnostic)
class BusinessRules:
    def classify_customer(self, customer_data: dict) -> str:
        """Business rule: Classify customer (VIP, Standard, etc.)"""
        # Pure business logic (no framework code)
        if customer_data['revenue'] > 100000:
            return "VIP"
        else:
            return "Standard"

    def get_prompt(self, customer_type: str) -> str:
        """Business logic: Get prompt based on customer type"""
        prompts = {
            "VIP": "You are assisting a VIP customer. Be extra helpful.",
            "Standard": "You are assisting a standard customer."
        }
        return prompts[customer_type]


# Orchestration (uses framework, but business logic separate)
class CustomerServiceOrchestrator:
    def __init__(self, framework_adapter, business_rules):
        self.framework = framework_adapter  # Adapter (can swap)
        self.rules = business_rules  # Business logic (portable)

    def handle_customer_query(self, customer_data: dict, query: str) -> str:
        # Step 1: Business logic (framework-agnostic)
        customer_type = self.rules.classify_customer(customer_data)
        prompt = self.rules.get_prompt(customer_type)

        # Step 2: Framework-specific (but abstracted via adapter)
        result = self.framework.run_chain(f"{prompt}\n\nQuery: {query}")

        return result

# Business logic portable (no framework code)
# Framework adapter swappable (LangChain → LlamaIndex)
```

---

### Practice 3: Regular Framework Evaluation (Quarterly or Biannually)

**Guideline**: Evaluate frameworks every 3-6 months (market evolves rapidly, better options may emerge).

**Evaluation Checklist**:

```markdown
## Quarterly Framework Evaluation (Q1 2026)

### Current Framework: LangChain

### Evaluation Criteria:
1. **Performance**:
   - Current: 10ms overhead, 2.40k tokens
   - Requirement: < 15ms overhead (OK), < 3k tokens (OK)
   - Status: ✅ Meets requirements

2. **Stability**:
   - Current: Breaking changes every 2-3 months
   - Requirement: < 1 breaking change per quarter
   - Status: ❌ Fails requirement (too many breaking changes)

3. **Community**:
   - Current: 111k stars, 50k Discord members
   - Requirement: Active community (10k+ stars)
   - Status: ✅ Exceeds requirements

4. **Cost**:
   - Current: $0 (open-source) + LangSmith $999/mo
   - Requirement: < $2k/mo
   - Status: ✅ Meets requirements

5. **Features**:
   - Current: Chains, agents (LangGraph), RAG, 100+ integrations
   - Requirement: Agents + RAG (critical features)
   - Status: ✅ Meets requirements

### Alternative Frameworks:

**LlamaIndex**:
- Pros: Better RAG (35% accuracy), more stable APIs
- Cons: Smaller ecosystem, less mature agents
- Decision: Consider for RAG-heavy use cases

**Haystack**:
- Pros: Best performance (5.9ms), most stable
- Cons: Slower prototyping, Python-only
- Decision: Consider for production deployments

**Semantic Kernel**:
- Pros: Most stable (v1.0+ APIs), multi-language
- Cons: Microsoft-centric, smaller community
- Decision: Consider if migrating to Azure

### Decision:
- **Stay with LangChain** (Q1 2026)
- **Re-evaluate in Q3 2026** (if breaking changes continue, migrate to Haystack or Semantic Kernel)
- **Monitor**: LlamaIndex for RAG improvements, Haystack for stability
```

**Frequency**:
- **Quarterly** (every 3 months): Quick evaluation (1-2 hours)
- **Biannually** (every 6 months): Deep evaluation (8-16 hours, prototype alternatives)

---

### Practice 4: Keep Migration Cost Low (Architecture Decisions)

**Guideline**: Make architectural decisions that minimize migration cost (even if slight performance trade-off).

**Examples**:

**Good** (Low Migration Cost):
- Use adapter pattern (abstraction layer) → Migration cost: 10-20 hours
- Keep prompts in YAML → Migration cost: 0 hours
- Use standard data formats (JSON, Pydantic) → Migration cost: 5-10 hours
- Document architecture (framework-agnostic) → Migration cost: 0 hours (knowledge transfer)

**Bad** (High Migration Cost):
- Tightly couple to framework (no abstraction) → Migration cost: 100+ hours
- Embed prompts in code → Migration cost: 20+ hours (extract + test)
- Use framework-specific data formats → Migration cost: 20+ hours (convert)
- No documentation → Migration cost: 40+ hours (reverse-engineer architecture)

**Decision Framework**:
```
When making architecture decision:
- Option A: Low migration cost (abstraction, standard formats)
- Option B: High migration cost (tight coupling, framework-specific)

If performance difference < 10% → Choose Option A (low migration cost)
If performance difference > 20% → Consider Option B (worth lock-in risk)
If performance difference 10-20% → Case-by-case (weigh value vs lock-in)
```

---

## 5. Lock-In Mitigation Checklist

### For New Projects (Starting Fresh)

- [ ] **Choose framework carefully** (match to use case, stability requirements)
- [ ] **Setup abstraction layer** (adapter pattern from day one)
- [ ] **Store prompts separately** (YAML/JSON, not embedded in code)
- [ ] **Document architecture** (framework-agnostic patterns, not APIs)
- [ ] **Use standard data formats** (JSON, Pydantic, not framework-specific)
- [ ] **Choose framework-agnostic observability** (Langfuse, not LangSmith if lock-in concern)
- [ ] **Minimize framework-specific features** (use only if high value)
- [ ] **Budget for migration** (assume 2-4 weeks migration possible, architecture for it)

### For Existing Projects (Reducing Lock-In)

- [ ] **Audit framework-specific code** (identify tight coupling)
- [ ] **Extract prompts to YAML** (separate from code)
- [ ] **Add abstraction layer** (wrap framework in adapter pattern)
- [ ] **Document architecture** (patterns, not framework APIs)
- [ ] **Test migration feasibility** (prototype in alternative framework, 1-2 days)
- [ ] **Evaluate quarterly** (check if better framework available)
- [ ] **Plan migration budget** (estimate 2-4 weeks, get management approval upfront)

### For Production Systems (Ongoing Monitoring)

- [ ] **Monitor framework health** (community activity, breaking changes, funding)
- [ ] **Quarterly evaluation** (compare alternatives, check if migration needed)
- [ ] **Export observability data** (if using LangSmith, export regularly)
- [ ] **Maintain documentation** (keep architecture docs up-to-date)
- [ ] **Test portability** (annual test: can we migrate in 2-4 weeks?)

---

## Conclusion

### Key Takeaways

1. **Lock-in is relatively low**: LLM framework lock-in is 60-70% portable (vs 30-40% for cloud platforms)

2. **Migration feasible**: 2-4 weeks (50-100 hours) for typical application if properly architected

3. **Upfront work reduces lock-in**: Abstraction layer (20-40 hours) saves 100+ hours in migration

4. **Prompts are fully portable**: Store in YAML/JSON (0 hours migration cost)

5. **Framework-specific features = lock-in**: Use only when high value (20%+ improvement)

6. **Regular evaluation critical**: Quarterly checks (1-2 hours) catch when better framework emerges

7. **Architecture matters**: Framework-agnostic core logic + adapter pattern = low migration cost

### Strategic Recommendations

**For Startups/MVPs**:
- **Low lock-in concern**: Focus on shipping fast (use LangChain, optimize later)
- **Minimal abstraction**: Don't over-engineer (adapter pattern overkill for MVP)
- **Separate prompts**: Easy win (0 migration cost, always do this)

**For Enterprises**:
- **High lock-in concern**: Abstract framework (adapter pattern worth investment)
- **Framework-agnostic observability**: Use Langfuse (not LangSmith if lock-in risk)
- **Quarterly evaluation**: Enterprise can afford 1-2 hours quarterly (catch migrations early)

**For Production Systems**:
- **Assume migration**: Budget 2-4 weeks migration (30-40% will switch by 2030)
- **Architecture for portability**: Adapter pattern, separate prompts, standard formats
- **Test portability**: Annual test (prototype in alternative framework, 1-2 days)

**Final Advice**: LLM framework lock-in is low compared to cloud platforms. With proper architecture (abstraction layer, separate prompts, standard data formats), migration is 2-4 weeks. Don't over-optimize for lock-in (premature abstraction is costly), but do the easy things (separate prompts, document architecture) that reduce migration cost to near-zero.

---

**Last Updated**: 2025-11-19 (S4 Strategic Discovery)
**Maintained By**: spawn-solutions research team
**MPSE Version**: v3.0
