# Deep Technical Feature Matrix

Comprehensive technical comparison across LangChain, LlamaIndex, Haystack, Semantic Kernel, and DSPy.

## 1. Chain Building Capabilities

### Sequential Chains

| Framework | Implementation | Type Safety | Async Support | Complexity |
|-----------|----------------|-------------|---------------|------------|
| **LangChain** | LCEL (LangChain Expression Language) | Moderate (Pydantic) | Full async | Low |
| **LlamaIndex** | QueryPipeline/Workflow | Good (typed) | Full async | Moderate |
| **Haystack** | Pipeline (directed graph) | Excellent (strict I/O) | Full async | Moderate |
| **Semantic Kernel** | Process Framework | Excellent (.NET typed) | Full async | Low |
| **DSPy** | Module composition | Moderate (signatures) | Limited | Very Low |

**Details**:
- **LangChain**: LCEL uses pipe operator (`|`) for composing chains. Example: `prompt | llm | output_parser`
- **LlamaIndex**: QueryPipeline provides explicit DAG construction with typed inputs/outputs
- **Haystack**: Pipeline enforces explicit component I/O contracts with connection validation
- **Semantic Kernel**: Kernel.InvokeAsync() chains functions through semantic functions
- **DSPy**: Chain of Thought and Predict modules create implicit chains

### Parallel Execution

| Framework | Native Support | Load Balancing | Error Isolation | Performance |
|-----------|---------------|----------------|-----------------|-------------|
| **LangChain** | RunnableParallel | No | Per-branch | Good |
| **LlamaIndex** | Workflow parallel tasks | No | Per-task | Good |
| **Haystack** | Pipeline branches | No | Per-component | Excellent |
| **Semantic Kernel** | Parallel skill invocation | No | Per-skill | Good |
| **DSPy** | Not built-in | N/A | N/A | N/A |

**Details**:
- **LangChain**: RunnableParallel executes multiple chains simultaneously, merges results
- **Haystack**: Pipeline automatically parallelizes independent branches in the graph
- **Semantic Kernel**: Manual parallel invocation using Task.WhenAll or asyncio.gather

### Conditional/Branching Logic

| Framework | If/Else Support | Switch/Router | Dynamic Routing | Agent-based |
|-----------|----------------|---------------|-----------------|-------------|
| **LangChain** | RunnableBranch | RouterChain | LangGraph | Excellent |
| **LlamaIndex** | Workflow conditionals | QueryRouter | RouterQueryEngine | Good |
| **Haystack** | ConditionalRouter | Decision nodes | Pipeline branches | Good |
| **Semantic Kernel** | Step conditionals | Process steps | Agent routing | Excellent |
| **DSPy** | Python conditionals | Limited | Not built-in | Limited |

**Details**:
- **LangChain**: LangGraph provides full state machine capabilities for complex routing
- **LlamaIndex**: RouterQueryEngine routes queries to different indexes/tools based on metadata
- **Haystack**: ConditionalRouter component evaluates Jinja2 expressions for routing
- **Semantic Kernel**: Process Framework supports conditional transitions between steps

## 2. Agent Architectures

### ReAct (Reasoning and Acting)

| Framework | Native Support | Customization | Tool Calling | Performance |
|-----------|---------------|---------------|--------------|-------------|
| **LangChain** | create_react_agent() | Extensive | Excellent | Good (10ms overhead) |
| **LlamaIndex** | ReActAgent | Good | Good | Very Good (6ms overhead) |
| **Haystack** | Agent via Pipeline | Custom implementation | Good | Excellent (5.9ms overhead) |
| **Semantic Kernel** | Agent framework (GA) | Excellent | Native | Good |
| **DSPy** | ReAct module | Limited | Basic | Excellent (3.53ms overhead) |

**Details**:
- **LangChain**: `create_react_agent()` creates zero-shot ReAct agents with thought/action/observation loop
- **LlamaIndex**: ReActAgent queries tools iteratively until task completion
- **Haystack**: Custom ReAct via Agent component with tool nodes in pipeline
- **DSPy**: ReAct module for thought-action-observation patterns with optimization

### Plan-and-Execute

| Framework | Native Support | Planner Type | Executor Type | Replanning |
|-----------|---------------|--------------|---------------|------------|
| **LangChain** | LangGraph (custom) | LLM-based | Tool executor | Yes (LangGraph) |
| **LlamaIndex** | Workflow planning | Query planner | Step executor | Limited |
| **Haystack** | Pipeline orchestration | Component-based | Node execution | Via pipeline |
| **Semantic Kernel** | Process Framework | Stepwise planner | Skill executor | Yes (process) |
| **DSPy** | Not built-in | N/A | N/A | N/A |

**Details**:
- **LangChain**: LangGraph enables custom plan-and-execute with explicit planning and execution nodes
- **Semantic Kernel**: Stepwise Planner creates multi-step plans, executes sequentially
- **LlamaIndex**: Query planning for RAG, less general-purpose than LangChain/SK

### Reflexion/Self-Critique

| Framework | Native Support | Feedback Loop | External Tools | Memory Integration |
|-----------|---------------|---------------|----------------|-------------------|
| **LangChain** | LangGraph patterns | Custom loops | Yes | Excellent |
| **LlamaIndex** | RetryQuery modules | Limited | Yes | Good |
| **Haystack** | Custom pipeline | Feedback nodes | Yes | Good |
| **Semantic Kernel** | Agent feedback | Planning loop | Yes | Good |
| **DSPy** | Assertion-driven | Optimization | Limited | Basic |

**Details**:
- **LangChain**: LangGraph supports reflexion via cyclic graphs with human/tool feedback
- **DSPy**: Assertions trigger module re-execution with feedback for optimization
- **Semantic Kernel**: Agent framework supports self-critique through planning iterations

### Multi-Agent Systems

| Framework | Native Support | Agent Communication | Coordination | Maturity |
|-----------|---------------|-------------------|--------------|----------|
| **LangChain** | LangGraph multi-agent | Message passing | Supervisor/hierarchical | Excellent |
| **LlamaIndex** | Multi-agent workflow | Orchestrator-based | Centralized | Good |
| **Haystack** | Pipeline multi-agents | Shared context | Pipeline coordination | Moderate |
| **Semantic Kernel** | Moving to GA | Event-driven | Process-based | Good (improving) |
| **DSPy** | Research-phase | Not built-in | N/A | Limited |

**Details**:
- **LangChain**: LangGraph supports supervisor, hierarchical, and collaborative multi-agent patterns
- **LlamaIndex**: Multi-agent orchestrator coordinates specialist agents for tasks
- **Haystack**: Multiple agent components in pipeline share context via pipeline state

## 3. RAG Components

### Document Loaders

| Framework | Built-in Loaders | File Types | Custom Loaders | Parsing Quality |
|-----------|------------------|------------|----------------|-----------------|
| **LangChain** | 100+ loaders | Extensive | Easy | Good |
| **LlamaIndex** | LlamaHub (600+) | Most comprehensive | Very easy | Excellent (LlamaParse) |
| **Haystack** | 40+ converters | Common formats | Moderate | Good |
| **Semantic Kernel** | Basic | Limited | Moderate | Fair |
| **DSPy** | Not built-in | N/A | Manual | N/A |

**Details**:
- **LlamaIndex**: LlamaParse provides best-in-class PDF/table parsing, premium service
- **LangChain**: Document loaders for Google Drive, Notion, Confluence, 100+ sources
- **Haystack**: FileTypeRouter + specialized converters (PDF, DOCX, HTML)

### Chunking Strategies

| Framework | Recursive Splitting | Semantic Chunking | Custom Splitters | Token-aware |
|-----------|-------------------|------------------|------------------|-------------|
| **LangChain** | RecursiveCharacterTextSplitter | Limited | Easy | Yes |
| **LlamaIndex** | SentenceSplitter, TokenTextSplitter | SemanticSplitter | Very easy | Yes |
| **Haystack** | Document splitters | Sentence-based | Moderate | Yes |
| **Semantic Kernel** | TextChunker | Limited | Moderate | Yes |
| **DSPy** | Not built-in | N/A | Manual | N/A |

**Details**:
- **LlamaIndex**: SemanticSplitter uses embeddings to chunk at semantic boundaries
- **LangChain**: RecursiveCharacterTextSplitter tries hierarchical separators (\n\n, \n, space)
- **Haystack**: DocumentSplitter with respect_sentence_boundary for cleaner chunks

### Retrievers

| Framework | Vector Retrieval | Keyword Search | Hybrid Search | Re-ranking |
|-----------|-----------------|----------------|---------------|------------|
| **LangChain** | VectorStoreRetriever | BM25 (external) | Manual combination | External tools |
| **LlamaIndex** | VectorIndexRetriever | BM25Retriever | Built-in fusion | Built-in re-ranker |
| **Haystack** | EmbeddingRetriever | BM25Retriever | Native hybrid | PromptNode re-ranker |
| **Semantic Kernel** | Memory connectors | Limited | Limited | External |
| **DSPy** | Retrieve module | Custom | Custom | Custom |

**Details**:
- **LlamaIndex**: Best hybrid search with QueryFusionRetriever combining vector + BM25
- **Haystack**: Native hybrid retrieval with Document Store supporting both methods
- **LangChain**: Requires manual orchestration of vector + keyword retrievers

### Advanced RAG Techniques

| Framework | CRAG | Self-RAG | HyDE | RAPTOR | Agentic RAG |
|-----------|------|----------|------|--------|-------------|
| **LangChain** | Custom (LangGraph) | Custom | Custom | External | LangGraph agents |
| **LlamaIndex** | Built-in modules | Built-in | Built-in | Built-in | Native agents |
| **Haystack** | Custom pipeline | Custom | Custom | External | Agent pipeline |
| **Semantic Kernel** | Custom | Custom | Limited | External | Agent framework |
| **DSPy** | Research modules | Research | Research | Research | Limited |

**Details**:
- **LlamaIndex**: Leading in advanced RAG with pre-built modules for CRAG, Self-RAG, HyDE, RAPTOR
- **CRAG** (Corrective RAG): Evaluates retrieved docs, refines search if needed
- **Self-RAG**: LLM decides when to retrieve, what to retrieve
- **HyDE**: Hypothetical Document Embeddings for better retrieval
- **RAPTOR**: Recursive summarization tree for hierarchical retrieval

## 4. Memory Systems

### Short-term Memory

| Framework | Conversation Buffer | Message Window | Token Limiting | Summarization |
|-----------|-------------------|----------------|----------------|---------------|
| **LangChain** | ConversationBufferMemory | Sliding window | Token-aware | ConversationSummaryMemory |
| **LlamaIndex** | ChatMemoryBuffer | Message history | Built-in | Not built-in |
| **Haystack** | ConversationMemory | Pipeline state | Manual | Pipeline-based |
| **Semantic Kernel** | ChatHistory | Message window | Token-aware | Not built-in |
| **DSPy** | Basic context | Manual | Manual | Not built-in |

**Details**:
- **LangChain**: ConversationTokenBufferMemory maintains sliding window by token count
- **Semantic Kernel**: ChatHistory with SystemMessages, UserMessages, AssistantMessages
- **LlamaIndex**: ChatMemoryBuffer with configurable token_limit

### Long-term Memory

| Framework | Vector Store Memory | Persistent Storage | Memory Retrieval | Entity Memory |
|-----------|-------------------|------------------|------------------|---------------|
| **LangChain** | VectorStoreMemory | Yes (40% adoption) | Semantic search | ConversationEntityMemory |
| **LlamaIndex** | Vector index native | Yes (core feature) | Built-in retrieval | Not built-in |
| **Haystack** | DocumentStore-based | Yes | Retrieval pipeline | Custom |
| **Semantic Kernel** | Memory connectors (GA) | Azure Cosmos DB | Plugin-based | Not built-in |
| **DSPy** | Not built-in | Manual | Manual | Not built-in |

**Details**:
- **LangChain**: VectorStoreBackedMemory retrieves relevant past conversations semantically
- **LlamaIndex**: VectorStoreIndex naturally serves as long-term memory
- **Semantic Kernel**: Memory packages (GA Nov 2024) with vector store plugins

### Semantic Memory

| Framework | Auto-embedding | Fact Extraction | Memory Consolidation | Memory Search |
|-----------|---------------|----------------|---------------------|---------------|
| **LangChain** | Manual setup | Custom chains | Not built-in | Vector search |
| **LlamaIndex** | Automatic | KnowledgeGraphIndex | Not built-in | Semantic retrieval |
| **Haystack** | Pipeline-based | NER components | Not built-in | Embedding search |
| **Semantic Kernel** | Memory plugin | Custom | Not built-in | Vector similarity |
| **DSPy** | Custom | Custom | Not built-in | Custom |

**Details**:
- **LlamaIndex**: KnowledgeGraphIndex extracts entities/relationships for structured memory
- **LangChain**: ConversationKGMemory builds knowledge graph from conversations
- **Semantic Kernel**: Semantic memory stores facts with embeddings for retrieval

## 5. Tool/Function Calling

### Function Schema Definition

| Framework | Schema Format | Auto-generation | Type Validation | JSON Schema Support |
|-----------|---------------|----------------|----------------|-------------------|
| **LangChain** | Pydantic models | @tool decorator | Runtime (Pydantic) | Yes |
| **LlamaIndex** | Pydantic FunctionTool | From function signature | Runtime | Yes |
| **Haystack** | Component I/O | Component signature | Strict (enforced) | Yes |
| **Semantic Kernel** | SKFunction | Attributes/decorators | Strong (.NET) / Runtime (Python) | Yes |
| **DSPy** | Signature definition | From signature | Basic | Limited |

**Details**:
- **LangChain**: `@tool` decorator converts functions to tools with auto JSON schema
- **Semantic Kernel**: `[SKFunction]` attribute (C#) or decorators (Python) define functions
- **Haystack**: Component `@component` decorator enforces input/output types

### Tool Execution

| Framework | Sync Execution | Async Execution | Error Handling | Timeout Support |
|-----------|---------------|----------------|----------------|----------------|
| **LangChain** | Yes | Yes | Try/catch + retries | Via custom wrapper |
| **LlamaIndex** | Yes | Yes | Exception handling | Via wrapper |
| **Haystack** | Yes | Yes | Component-level | Pipeline timeout |
| **Semantic Kernel** | Yes | Yes | Exception handling | Configurable |
| **DSPy** | Yes | Limited | Basic | Not built-in |

**Details**:
- **LangChain**: Tools can be sync or async, framework handles both transparently
- **Semantic Kernel**: Native async/await support across all languages
- **Haystack**: Component execution handles errors with graceful degradation

### Built-in Tool Ecosystem

| Framework | Web Search | API Calling | Database | File System | Math/Code |
|-----------|-----------|-------------|----------|-------------|-----------|
| **LangChain** | Tavily, SerpAPI | OpenAPI | SQL toolkit | Document loaders | Python REPL, Calculator |
| **LlamaIndex** | Built-in search | OpenAPI | SQL tools | LlamaHub loaders | Code interpreter |
| **Haystack** | WebSearch | Custom | DocumentStores | File converters | Not built-in |
| **Semantic Kernel** | Bing Search | HTTP plugin | SQL connector | File I/O plugin | Not built-in |
| **DSPy** | Research tools | Custom | Custom | Custom | Custom |

**Details**:
- **LangChain**: Largest ecosystem with 100+ pre-built tools
- **LlamaIndex**: LlamaHub provides 600+ data connectors/tools
- **Haystack**: Production-focused tools with strong data integration

## 6. Observability

### Tracing

| Framework | Built-in Tracing | Trace Visualization | Distributed Tracing | Performance Impact |
|-----------|-----------------|-------------------|-------------------|-------------------|
| **LangChain** | LangSmith (commercial) | Excellent UI | Yes | Low (~1-2%) |
| **LlamaIndex** | Callback system | Basic | Via OpenTelemetry | Low |
| **Haystack** | Pipeline serialization | Pipeline graphs | Via integrations | Minimal |
| **Semantic Kernel** | Telemetry hooks | Azure Monitor | OpenTelemetry | Low |
| **DSPy** | Basic logging | Not built-in | Not built-in | Minimal |

**Details**:
- **LangChain**: LangSmith provides industry-leading tracing with token counts, latency, costs
- **LlamaIndex**: Integrates with Phoenix, Arize for observability
- **Haystack**: Langfuse integration announced May 2024 for enhanced tracing

### Logging

| Framework | Structured Logging | Log Levels | Custom Loggers | Integration |
|-----------|-------------------|-----------|----------------|------------|
| **LangChain** | Yes | Standard levels | Callback handlers | LangSmith |
| **LlamaIndex** | Yes | Standard levels | Callback handlers | LlamaCloud |
| **Haystack** | Yes | Standard levels | Component logging | Standard tools |
| **Semantic Kernel** | Yes | Standard levels | Logger injection | Azure Monitor |
| **DSPy** | Basic | Limited | Not built-in | Not built-in |

**Details**:
- **LangChain**: Callback system enables custom logging at each step
- **Haystack**: Component-level logging with clear pipeline execution logs
- **Semantic Kernel**: ILogger injection for enterprise-grade logging

### Debugging Tools

| Framework | Breakpoints | Step Debugging | Replay | Test Mode |
|-----------|------------|---------------|--------|-----------|
| **LangChain** | LangSmith playground | Interactive | LangSmith replay | Mock LLMs |
| **LlamaIndex** | Callback inspection | Manual | Not built-in | Mock mode |
| **Haystack** | Pipeline inspection | Step-through | Pipeline export/import | Mock components |
| **Semantic Kernel** | Standard debuggers | Native (.NET/IDE) | Not built-in | Mock skills |
| **DSPy** | Assertions | Python debugger | Not built-in | Not built-in |

**Details**:
- **LangChain**: LangSmith playground allows re-running chains with different inputs
- **Haystack**: Pipeline.draw() visualizes execution flow for debugging
- **Semantic Kernel**: Standard IDE debugging works naturally (breakpoints, watches)

## 7. Prompt Management

### Template Systems

| Framework | Template Format | Variables | Logic/Conditionals | Reusability |
|-----------|----------------|-----------|-------------------|------------|
| **LangChain** | Jinja2, f-strings | Yes | Jinja2 logic | Template hub |
| **LlamaIndex** | Jinja2, f-strings | Yes | Jinja2 logic | Prompt templates |
| **Haystack** | Jinja2 | Yes | Full Jinja2 | PromptNode templates |
| **Semantic Kernel** | Handlebars, text | Yes | Limited | Function templates |
| **DSPy** | Signature-based | Signature fields | Python logic | Module-based |

**Details**:
- **LangChain**: ChatPromptTemplate with message roles, extensive LangChain Hub
- **LlamaIndex**: RichPromptTemplate with Jinja2 for complex logic
- **Haystack**: PromptTemplate with Jinja2 expressions for dynamic prompts
- **DSPy**: Signature defines prompt structure, compiler optimizes automatically

### Versioning

| Framework | Version Control | Prompt Registry | A/B Testing | Rollback |
|-----------|----------------|----------------|------------|----------|
| **LangChain** | LangSmith versioning | LangChain Hub | LangSmith experiments | Yes |
| **LlamaIndex** | Manual (code) | Not built-in | Not built-in | Manual |
| **Haystack** | Manual (code) | Pipeline templates | Not built-in | Pipeline versions |
| **Semantic Kernel** | Code-based | Not built-in | Not built-in | Git-based |
| **DSPy** | Compiled programs | Not built-in | Optimizer experiments | Manual |

**Details**:
- **LangChain**: LangSmith tracks prompt versions, compares performance across versions
- **MLflow**: Third-party prompt registry works with all frameworks
- **DSPy**: Compiled programs are versioned artifacts with optimizer configs

### Optimization

| Framework | Automated Optimization | Few-shot Learning | Prompt Engineering | Human Feedback |
|-----------|----------------------|------------------|-------------------|----------------|
| **LangChain** | LangSmith (manual) | Manual examples | LangSmith insights | LangSmith feedback |
| **LlamaIndex** | Some automation | Example selectors | Manual | Not built-in |
| **Haystack** | Manual | Example components | Manual | Not built-in |
| **Semantic Kernel** | Planner optimization | Not built-in | Manual | Not built-in |
| **DSPy** | **Automatic (core feature)** | **Auto few-shot** | **Compiled optimization** | Assertion-driven |

**Details**:
- **DSPy**: MIPROv2 optimizer automatically generates instructions and few-shot examples
- **LangChain**: LangSmith provides insights but optimization is manual
- **DSPy**: Treats prompts as learnable parameters, optimizes via Bayesian methods

## 8. Model Support

### LLM Provider Coverage

| Framework | OpenAI | Anthropic | Cohere | Local (Ollama) | HuggingFace |
|-----------|--------|-----------|--------|----------------|-------------|
| **LangChain** | Full | Full | Full | Yes | Yes |
| **LlamaIndex** | Full | Full | Full | Yes | Yes |
| **Haystack** | Full | Full | Full | Yes | Yes |
| **Semantic Kernel** | Full | Full | Full | Yes | Yes |
| **DSPy** | Full | Full | Full | Yes | Yes |

**Winner**: All frameworks are model-agnostic with excellent provider support

### Azure Integration

| Framework | Azure OpenAI | Azure AI Studio | Managed Identity | Key Vault | Rating |
|-----------|-------------|----------------|------------------|-----------|---------|
| **LangChain** | Yes | Limited | Manual | Manual | Good |
| **LlamaIndex** | Yes | Limited | Manual | Manual | Good |
| **Haystack** | Yes | Limited | Manual | Manual | Good |
| **Semantic Kernel** | **Excellent** | **Native** | **Built-in** | **Native** | **Excellent** |
| **DSPy** | Yes | No | Manual | Manual | Fair |

**Details**:
- **Semantic Kernel**: Purpose-built for Azure with first-class support
- **LangChain/LlamaIndex**: AzureChatOpenAI connectors, manual identity setup
- **Semantic Kernel**: Azure AI Foundry integration for model catalog

### Fine-tuned Models

| Framework | Custom Endpoints | Fine-tune Support | Model Switching | Adapter Support |
|-----------|-----------------|------------------|----------------|-----------------|
| **LangChain** | Yes (custom LLM class) | Via providers | Easy (LCEL) | Via providers |
| **LlamaIndex** | Yes (custom LLM) | Via providers | Easy | Via providers |
| **Haystack** | Yes (custom component) | Via providers | Component swap | Via providers |
| **Semantic Kernel** | Yes (custom connector) | Via Azure | Easy | Via providers |
| **DSPy** | Yes (custom LM) | **BetterTogether optimizer** | Easy | Research-phase |

**Details**:
- **DSPy**: BetterTogether (2024) fine-tunes LM weights within DSPy programs
- All frameworks support custom model endpoints for fine-tuned models
- Model switching is easy across all frameworks (abstraction layer)

## 9. Streaming Support

### Token Streaming

| Framework | Streaming API | Async Streaming | Partial Output | Server-Sent Events |
|-----------|---------------|----------------|----------------|-------------------|
| **LangChain** | stream() method | astream() | Per-token callbacks | LangServe support |
| **LlamaIndex** | stream_chat() | astream_chat() | StreamingResponse | Built-in |
| **Haystack** | Not primary focus | Limited | Component-based | Manual |
| **Semantic Kernel** | StreamAsync() | Native async | Per-token events | Via ASP.NET |
| **DSPy** | Limited | Limited | Not built-in | Not built-in |

**Details**:
- **LangChain**: Full streaming with `astream()` and `astream_events()` for fine-grained control
- **LlamaIndex**: StreamingResponse for chat and query engines
- **Semantic Kernel**: IAsyncEnumerable<StreamingTextContent> for token streaming
- **Haystack**: Streaming not a primary feature, focused on batch processing

### Response Streaming

| Framework | Chunk Size Control | Backpressure | Error Mid-stream | Resume Support |
|-----------|-------------------|--------------|------------------|----------------|
| **LangChain** | Per-token | Built-in (async) | Error callbacks | Not built-in |
| **LlamaIndex** | Configurable | Built-in (async) | Exception handling | Not built-in |
| **Haystack** | Limited | Limited | Component errors | Not built-in |
| **Semantic Kernel** | Per-token | Built-in (async) | Exception handling | Not built-in |
| **DSPy** | Not built-in | N/A | N/A | N/A |

**Details**:
- **LangChain**: `astream_events()` provides granular control over streaming chunks
- **Semantic Kernel**: IAsyncEnumerable handles backpressure naturally
- All streaming frameworks handle mid-stream errors via exception propagation

## 10. Error Handling & Retries

### Retry Strategies

| Framework | Exponential Backoff | Max Retries | Retry Conditions | Jitter Support |
|-----------|-------------------|-------------|------------------|----------------|
| **LangChain** | Yes (configurable) | max_retries param | Exception types | Yes |
| **LlamaIndex** | Yes | Retry decorators | Exception types | Limited |
| **Haystack** | Component-level | Pipeline config | Component errors | Limited |
| **Semantic Kernel** | Configurable | Retry policy | Exception types | Yes |
| **DSPy** | Basic | Manual | Manual | Not built-in |

**Details**:
- **LangChain**: ChatOpenAI(max_retries=3) with exponential backoff
- **LangChain**: RunnableRetry for custom retry logic with specific exceptions
- **Semantic Kernel**: HttpRetryPolicy with configurable backoff and jitter

### Fallback Mechanisms

| Framework | Model Fallback | Chain Fallback | Timeout Handling | Graceful Degradation |
|-----------|---------------|----------------|------------------|---------------------|
| **LangChain** | RunnableWithFallbacks | Multi-level | Via async timeout | Excellent |
| **LlamaIndex** | Custom wrapper | Limited | Via async timeout | Good |
| **Haystack** | Pipeline branches | Component fallback | Pipeline timeout | Good |
| **Semantic Kernel** | Custom error handling | Process fallback | Cancellation tokens | Good |
| **DSPy** | Manual | Manual | Manual | Limited |

**Details**:
- **LangChain**: `primary.with_fallbacks([backup1, backup2])` for cascading fallbacks
- **LangChain**: Model fallback (GPT-4 → GPT-3.5) and chain fallback (RAG → summarization)
- **Haystack**: Pipeline branches can route to fallback components on error

### Error Context

| Framework | Error Messages | Stack Traces | Debug Info | Root Cause Analysis |
|-----------|---------------|--------------|------------|-------------------|
| **LangChain** | Descriptive | Full | LangSmith context | LangSmith traces |
| **LlamaIndex** | Good | Full | Callback data | Manual |
| **Haystack** | Clear | Full | Pipeline state | Pipeline logs |
| **Semantic Kernel** | Descriptive | Full (.NET) | Telemetry | Azure Monitor |
| **DSPy** | Basic | Python traceback | Limited | Manual |

**Details**:
- **LangChain**: LangSmith captures full error context with input/output at each step
- **Haystack**: Clear component-level errors with explicit I/O mismatches
- **Semantic Kernel**: Enterprise-grade error handling with detailed telemetry

## 11. Testing & Evaluation

### Unit Testing

| Framework | Mock LLMs | Test Utilities | Assertion Helpers | Coverage Tools |
|-----------|-----------|---------------|------------------|----------------|
| **LangChain** | FakeLLM, FakeListLLM | pytest fixtures | Custom | Standard Python |
| **LlamaIndex** | MockLLM | Test utilities | Custom | Standard Python |
| **Haystack** | Mock components | Component testing | Custom | Standard Python |
| **Semantic Kernel** | Mock skills | xUnit/pytest | Standard | .NET/Python tools |
| **DSPy** | Mock LM | Assertions | **Built-in assertions** | Standard Python |

**Details**:
- **LangChain**: FakeListLLM returns predefined responses for deterministic testing
- **Haystack**: Component.run() testable with mock inputs/outputs
- **DSPy**: `dspy.Assert()` and `dspy.Suggest()` for runtime validation

### Integration Testing

| Framework | End-to-end Testing | Dataset Support | Evaluation Metrics | Benchmarking |
|-----------|-------------------|----------------|-------------------|--------------|
| **LangChain** | LangSmith datasets | Built-in datasets | LangSmith evaluators | LangSmith experiments |
| **LlamaIndex** | Evaluation module | Custom datasets | RAGAS integration | Manual benchmarks |
| **Haystack** | Pipeline testing | Custom datasets | Custom evaluators | Manual benchmarks |
| **Semantic Kernel** | Standard testing | Manual datasets | Custom metrics | Manual benchmarks |
| **DSPy** | Metric optimization | Training/dev sets | **Auto-optimization** | Research benchmarks |

**Details**:
- **LangChain**: LangSmith experiments run chains across datasets, compute metrics
- **LlamaIndex**: Evaluation modules for RAG (faithfulness, relevancy)
- **DSPy**: Optimizers require metric function, automatically maximize it

### Evaluation Frameworks

| Framework | Human Evaluation | Auto-evaluation | Custom Metrics | A/B Testing |
|-----------|-----------------|----------------|---------------|------------|
| **LangChain** | LangSmith UI | LangSmith evaluators | Python functions | LangSmith compare |
| **LlamaIndex** | Manual | RAGAS, custom | Python functions | Manual |
| **Haystack** | Manual | Custom evaluators | Python functions | Manual |
| **Semantic Kernel** | Manual | Custom | Custom | Manual |
| **DSPy** | Manual | Metric functions | Python functions | Optimizer runs |

**Details**:
- **LangChain**: LangSmith supports human annotation and auto-evals (PII detection, correctness)
- **LlamaIndex**: RAGAS integration for RAG-specific metrics (context precision, recall)
- **DSPy**: Metric function drives optimization (accuracy, F1, custom objectives)

## 12. Production Features

### Caching

| Framework | Semantic Caching | Response Caching | Embedding Caching | Cache Invalidation |
|-----------|-----------------|------------------|-------------------|-------------------|
| **LangChain** | Via LangSmith | InMemoryCache | Manual | TTL-based |
| **LlamaIndex** | Built-in cache | Query cache | Index cache | Manual/TTL |
| **Haystack** | Document cache | Not primary | DocumentStore cache | Manual |
| **Semantic Kernel** | Not built-in | Manual | Manual | Manual |
| **DSPy** | Not built-in | Manual | Manual | Manual |

**Details**:
- **LangChain**: InMemoryCache and RedisCache for LLM response caching
- **LlamaIndex**: Persistent caching of index and query results
- **Production**: GPTCache and Helicone provide semantic caching across frameworks

### Rate Limiting

| Framework | Built-in Limiting | Token Budgets | Concurrent Requests | Backpressure |
|-----------|------------------|---------------|-------------------|--------------|
| **LangChain** | Via callbacks | Token counting | Manual throttling | Async queues |
| **LlamaIndex** | Not built-in | Token counting | Manual | Async queues |
| **Haystack** | Not built-in | Component limits | Pipeline parallelism | Limited |
| **Semantic Kernel** | Not built-in | Token tracking | Async semaphore | Manual |
| **DSPy** | Not built-in | Not built-in | Manual | Manual |

**Details**:
- All frameworks rely on LLM provider rate limits
- **Production**: Helicone, LiteLLM provide rate limiting as middleware
- **LangChain**: Token counting callbacks can enforce budgets

### Cost Optimization

| Framework | Token Counting | Cost Tracking | Budget Alerts | Model Routing |
|-----------|---------------|--------------|--------------|---------------|
| **LangChain** | Built-in (callbacks) | LangSmith | LangSmith alerts | Manual |
| **LlamaIndex** | Built-in | LlamaCloud | Not built-in | Router modules |
| **Haystack** | Component-level | Manual | Not built-in | Pipeline routing |
| **Semantic Kernel** | Token usage tracking | Azure Monitor | Azure alerts | Manual |
| **DSPy** | Built-in | Manual | Not built-in | Manual |

**Details**:
- **LangChain**: get_openai_callback() tracks tokens and costs during execution
- **LangSmith**: Automatic cost tracking across all traced runs
- **LlamaIndex**: Token counting built into LLM abstraction
- **Production**: Smaller models for simple tasks, larger for complex (routing)

## Performance Summary

### Framework Overhead (Orchestration Latency)

1. **DSPy**: 3.53ms (best)
2. **Haystack**: 5.9ms
3. **LlamaIndex**: 6ms
4. **LangChain**: 10ms
5. **Semantic Kernel**: Not measured

### Token Efficiency (API Cost)

1. **Haystack**: 1.57k tokens (best)
2. **LlamaIndex**: 1.60k tokens
3. **DSPy**: 2.03k tokens
4. **LangChain**: 2.40k tokens (highest)
5. **Semantic Kernel**: Not measured

### Production Readiness Score

1. **Haystack**: 9/10 (Fortune 500, stability, performance)
2. **Semantic Kernel**: 9/10 (Microsoft enterprise, stable APIs)
3. **LangChain**: 7/10 (large ecosystem, frequent changes)
4. **LlamaIndex**: 7/10 (RAG excellence, growing production use)
5. **DSPy**: 5/10 (research-phase, limited production)

## Key Insights

### Strengths by Framework

**LangChain**:
- Largest ecosystem (100+ tools, integrations)
- Best agent support (LangGraph)
- Industry-leading observability (LangSmith)
- Fastest prototyping (3x faster than Haystack)

**LlamaIndex**:
- Best-in-class RAG (35% accuracy boost)
- Advanced retrieval techniques (CRAG, Self-RAG, HyDE, RAPTOR)
- Excellent document parsing (LlamaParse)
- Comprehensive data connectors (LlamaHub 600+)

**Haystack**:
- Best performance (5.9ms overhead, 1.57k tokens)
- Production-grade stability
- Fortune 500 enterprise adoption
- Typed components with strict I/O contracts

**Semantic Kernel**:
- Best Azure integration
- Multi-language support (C#, Python, Java)
- Enterprise security/compliance
- Stable APIs (v1.0+ non-breaking)

**DSPy**:
- Lowest overhead (3.53ms)
- Automated prompt optimization
- Research innovation leader
- Minimal boilerplate code

### Trade-offs

**Flexibility vs Stability**:
- LangChain/LlamaIndex: More features, faster iteration, breaking changes
- Haystack/Semantic Kernel: Stable APIs, slower feature additions, production-first

**Ease of Use vs Performance**:
- LangChain: Easiest to start, highest overhead
- DSPy/Haystack: Steeper learning curve, best performance

**General-Purpose vs Specialized**:
- LangChain/Semantic Kernel: General-purpose, wide use cases
- LlamaIndex: RAG specialist, deep expertise in retrieval
- DSPy: Optimization specialist, research applications

**Open-Source vs Commercial**:
- All frameworks: Open-source core (MIT/Apache 2.0)
- Optional paid services: LangSmith, LlamaCloud, Haystack Enterprise
- Semantic Kernel: Free with Azure paid services
