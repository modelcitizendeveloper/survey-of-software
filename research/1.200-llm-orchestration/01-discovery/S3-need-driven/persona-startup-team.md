# Persona: Startup Team (2-10 People)

## Profile

**Who**: Early-stage startup with small engineering team building AI product

**Characteristics**:
- 2-5 engineers (1-2 focused on AI/LLM features)
- Product manager or founder-led product
- Seed funding ($500K-$3M) or revenue-generating
- Growing user base (100-10,000 users)
- 3-12 month runway
- Need to iterate quickly while building for scale

**Constraints**:
- Limited engineering resources (can't rebuild everything)
- Cost-conscious but willing to invest in right tools
- Must balance speed with maintainability
- Can't afford major rewrites every quarter
- Need observability and debugging tools

**Goals**:
- Ship features weekly/bi-weekly
- Scale to 10K-100K users
- Maintain <$5K/month LLM costs initially
- Build technical foundation for Series A
- Enable team collaboration and code review

## Recommended Framework Strategy

### Primary Recommendation: Match to Use Case

Unlike indie developers (who should default to LangChain), startups should **choose framework based on primary use case**:

| Primary Use Case | Framework | Why |
|-----------------|-----------|-----|
| **RAG / Document Search** | LlamaIndex | 35% better retrieval, specialized tooling |
| **Conversational AI / Agents** | LangChain + LangGraph | Most mature agents, production-proven |
| **Azure / .NET Stack** | Semantic Kernel | Best Azure integration, stable APIs |
| **High-Volume Processing** | Haystack | Best performance, token efficiency |
| **Multi-use (unclear focus)** | LangChain | Most flexible, largest ecosystem |

### Secondary Tools

Regardless of primary framework, invest in:
1. **Observability**: LangSmith ($39-99/month) - essential for debugging
2. **Vector Database**: Pinecone ($70/month) or Qdrant Cloud ($25-50/month)
3. **Analytics**: PostHog (free tier) or Mixpanel
4. **Error Tracking**: Sentry (free tier)

## Architecture Patterns

### Pattern 1: RAG-First Product (Use LlamaIndex)

**Example**: Internal knowledge base, customer support with docs, research assistant

```python
# startup_rag/app.py
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext
import pinecone

# Configuration management
class Config:
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    INDEX_NAME = "prod-knowledge-base"
    ENVIRONMENT = os.getenv("ENV", "development")

# Initialize services
def get_vector_store():
    """Reusable vector store initialization"""
    pc = pinecone.Pinecone(api_key=Config.PINECONE_API_KEY)
    pinecone_index = pc.Index(Config.INDEX_NAME)
    return PineconeVectorStore(pinecone_index=pinecone_index)

def build_rag_engine():
    """Production RAG engine with monitoring"""
    # Use production-grade components
    llm = OpenAI(
        model="gpt-4o-mini",  # Balanced cost/quality
        temperature=0.1,      # Low for accuracy
        max_tokens=500
    )

    embed_model = OpenAIEmbedding(model="text-embedding-3-small")

    # Vector store
    vector_store = get_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create index
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        storage_context=storage_context,
        embed_model=embed_model
    )

    # Query engine with reranking
    query_engine = index.as_query_engine(
        llm=llm,
        similarity_top_k=5,
        response_mode="compact",
        node_postprocessors=[
            # Add reranking for better results
            # SimilarityPostprocessor(similarity_cutoff=0.7)
        ]
    )

    return query_engine

# FastAPI for production API
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Global engine (initialized once)
query_engine = None

@app.on_event("startup")
async def startup_event():
    global query_engine
    query_engine = build_rag_engine()

class QueryRequest(BaseModel):
    query: str
    user_id: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

@app.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    try:
        # Track user for analytics
        analytics.track(request.user_id, "query_submitted")

        # Query with timeout
        response = await asyncio.wait_for(
            query_engine.aquery(request.query),
            timeout=30.0
        )

        # Extract sources
        sources = [node.node.metadata.get("source", "unknown")
                   for node in response.source_nodes]

        return QueryResponse(
            answer=str(response),
            sources=list(set(sources))
        )

    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Query timeout")
    except Exception as e:
        # Log to Sentry
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Internal error")
```

**Deployment**: Cloud Run / Fly.io / Railway

**Cost**: $200-500/month (100-1000 daily users)

### Pattern 2: Agent-First Product (Use LangChain + LangGraph)

**Example**: AI assistant with tools, workflow automation, complex multi-step tasks

```python
# startup_agent/agent.py
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator

# Define tools
def search_database(query: str) -> str:
    """Search internal database"""
    # Implementation
    return f"Database results for: {query}"

def call_api(endpoint: str, data: dict) -> str:
    """Call external API"""
    # Implementation
    return f"API response from {endpoint}"

def send_email(to: str, subject: str, body: str) -> str:
    """Send email via SendGrid"""
    # Implementation
    return f"Email sent to {to}"

tools = [
    Tool(
        name="database_search",
        func=search_database,
        description="Search the internal database for customer information"
    ),
    Tool(
        name="api_call",
        func=call_api,
        description="Call external APIs for data"
    ),
    Tool(
        name="send_email",
        func=send_email,
        description="Send emails to customers"
    )
]

# Agent with LangGraph for complex workflows
class AgentState(TypedDict):
    messages: Annotated[Sequence[str], operator.add]
    next_step: str

def create_agent_workflow():
    """Production agent with state management"""

    llm = ChatOpenAI(model="gpt-4", temperature=0)

    # Create agent
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use tools to help users."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True
    )

    return agent_executor

# FastAPI endpoint
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()

class AgentRequest(BaseModel):
    task: str
    user_id: str

@app.post("/agent/execute")
async def execute_agent_task(request: AgentRequest, background_tasks: BackgroundTasks):
    """Execute agent task asynchronously"""

    agent = create_agent_workflow()

    # Run in background for long tasks
    def run_agent():
        try:
            result = agent.invoke({"input": request.task})

            # Save result to database
            save_agent_result(request.user_id, result)

            # Notify user
            send_notification(request.user_id, "Task completed")

        except Exception as e:
            sentry_sdk.capture_exception(e)
            send_notification(request.user_id, "Task failed")

    background_tasks.add_task(run_agent)

    return {"status": "processing", "message": "Task started"}
```

**Deployment**: Kubernetes (GKE/EKS) or Railway

**Cost**: $500-1500/month (with agent execution costs)

### Pattern 3: Hybrid Approach (LangChain + LlamaIndex)

Many startups use **both** frameworks for different features:

```python
# Use LlamaIndex for RAG
from llama_index.core import VectorStoreIndex

rag_engine = VectorStoreIndex.from_documents(documents)

# Use LangChain for orchestration and agents
from langchain.agents import Tool
from langchain_openai import ChatOpenAI

def rag_tool(query: str) -> str:
    """Tool that uses LlamaIndex RAG"""
    response = rag_engine.query(query)
    return str(response)

langchain_tools = [
    Tool(name="knowledge_base", func=rag_tool, description="Search company knowledge"),
    # ... other tools
]

agent = create_agent(tools=langchain_tools)
```

**When to use hybrid**:
- RAG is one feature among many
- Need best-of-breed for each use case
- Team can handle multiple frameworks

## Team Collaboration

### Code Organization

```
my-ai-startup/
├── src/
│   ├── agents/          # Agent definitions
│   ├── chains/          # Reusable chains
│   ├── prompts/         # Prompt templates
│   ├── tools/           # Custom tools
│   ├── config/          # Configuration
│   └── utils/           # Helpers
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/
│   ├── index_documents.py
│   └── evaluate_performance.py
├── .env.example
├── pyproject.toml       # uv/poetry dependencies
├── docker-compose.yml
└── README.md
```

### Configuration Management

```python
# src/config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM
    openai_api_key: str
    anthropic_api_key: str
    default_model: str = "gpt-4o-mini"
    temperature: float = 0.7

    # Vector DB
    pinecone_api_key: str
    pinecone_environment: str
    pinecone_index: str

    # Observability
    langsmith_api_key: str
    langsmith_project: str

    # Environment
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
```

### Testing Strategy

```python
# tests/unit/test_chains.py
import pytest
from langchain.llms.fake import FakeListLLM
from src.chains.summarization import create_summary_chain

def test_summary_chain():
    """Test summary chain with mock LLM"""
    # Use fake LLM for deterministic testing
    fake_llm = FakeListLLM(responses=["This is a summary."])

    chain = create_summary_chain(llm=fake_llm)
    result = chain.invoke({"text": "Long document text..."})

    assert result == "This is a summary."
    assert len(result) < 100

# tests/integration/test_rag.py
@pytest.mark.integration
def test_rag_retrieval():
    """Test RAG with real embeddings but test documents"""
    from src.rag.engine import build_test_rag_engine

    engine = build_test_rag_engine()  # Uses test data
    response = engine.query("What is the company policy?")

    assert response is not None
    assert len(response.source_nodes) > 0
```

### Code Review Checklist

```markdown
## LLM Feature PR Checklist

- [ ] Prompt templates are version controlled
- [ ] Token usage is logged/monitored
- [ ] Error handling for API failures
- [ ] Timeout protection (max 30s for user-facing)
- [ ] Cost estimation added to PR description
- [ ] Unit tests with mock LLMs
- [ ] Integration tests pass
- [ ] LangSmith tracing enabled
- [ ] No API keys in code (use .env)
- [ ] Documentation updated
```

## Observability & Monitoring

### LangSmith Setup (Essential)

```python
# src/utils/tracing.py
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
os.environ["LANGCHAIN_PROJECT"] = f"{settings.environment}-project"

# Now all chains/agents automatically traced
```

**LangSmith Pricing**:
- Developer: $39/month (1 user)
- Team: $99/month (5 users)
- Enterprise: Custom

**ROI**: Pays for itself in 1 hour of debugging time saved

### Custom Metrics

```python
# src/utils/metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
llm_requests = Counter(
    'llm_requests_total',
    'Total LLM API requests',
    ['model', 'endpoint', 'status']
)

llm_latency = Histogram(
    'llm_latency_seconds',
    'LLM request latency',
    ['model']
)

llm_tokens = Counter(
    'llm_tokens_total',
    'Total tokens used',
    ['model', 'type']  # type: input/output
)

llm_cost = Counter(
    'llm_cost_usd',
    'Estimated LLM cost in USD',
    ['model']
)

active_chains = Gauge(
    'active_chains',
    'Number of active chain executions'
)

def track_llm_call(model: str):
    """Decorator to track LLM calls"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            active_chains.inc()
            start_time = time.time()

            try:
                result = await func(*args, **kwargs)

                # Track success
                llm_requests.labels(
                    model=model,
                    endpoint=func.__name__,
                    status='success'
                ).inc()

                # Track latency
                latency = time.time() - start_time
                llm_latency.labels(model=model).observe(latency)

                return result

            except Exception as e:
                llm_requests.labels(
                    model=model,
                    endpoint=func.__name__,
                    status='error'
                ).inc()
                raise

            finally:
                active_chains.dec()

        return wrapper
    return decorator

# Usage
@track_llm_call(model="gpt-4o-mini")
async def query_rag(query: str):
    return await rag_engine.aquery(query)
```

### Alerting

```python
# src/utils/alerts.py
import os
from slack_sdk import WebClient

slack_client = WebClient(token=os.getenv("SLACK_TOKEN"))

def alert_high_cost(amount: float, threshold: float = 10.0):
    """Alert team if single request costs too much"""
    if amount > threshold:
        slack_client.chat_postMessage(
            channel="#ai-alerts",
            text=f"🚨 High cost LLM request: ${amount:.2f}"
        )

def alert_high_latency(latency: float, threshold: float = 10.0):
    """Alert if request takes too long"""
    if latency > threshold:
        slack_client.chat_postMessage(
            channel="#ai-alerts",
            text=f"⚠️  Slow LLM request: {latency:.1f}s"
        )
```

## Scaling Considerations

### Traffic Levels

| Users | Requests/Day | LLM Cost/Month | Infrastructure | Strategy |
|-------|-------------|----------------|----------------|----------|
| 100-1K | 1K-10K | $100-500 | Serverless (Cloud Run) | Single region, basic caching |
| 1K-10K | 10K-100K | $500-2K | Container (Railway/Render) | Redis cache, rate limiting |
| 10K-50K | 100K-500K | $2K-10K | Kubernetes (GKE/EKS) | Multi-region, aggressive caching |
| 50K+ | 500K+ | $10K+ | K8s + autoscaling | CDN, edge caching, optimize everything |

### Caching Strategy

```python
# src/utils/cache.py
from functools import lru_cache
import hashlib
import redis
import pickle

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=False  # Store binary for pickle
)

def cache_llm_response(ttl: int = 3600):
    """Cache LLM responses in Redis"""
    def decorator(func):
        async def wrapper(query: str, *args, **kwargs):
            # Create cache key
            cache_key = f"llm:{hashlib.md5(query.encode()).hexdigest()}"

            # Check cache
            cached = redis_client.get(cache_key)
            if cached:
                print(f"Cache hit: {cache_key}")
                return pickle.loads(cached)

            # Call LLM
            result = await func(query, *args, **kwargs)

            # Store in cache
            redis_client.setex(
                cache_key,
                ttl,
                pickle.dumps(result)
            )

            return result

        return wrapper
    return decorator

# Usage
@cache_llm_response(ttl=1800)  # 30 min cache
async def generate_summary(text: str):
    return await summary_chain.ainvoke({"text": text})
```

### Rate Limiting

```python
# src/utils/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)

@app.post("/query")
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def query_endpoint(request: Request, query: QueryRequest):
    # Your endpoint logic
    pass

# Per-user rate limiting
from redis import Redis
from datetime import datetime, timedelta

class UserRateLimiter:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def is_allowed(self, user_id: str, limit: int = 100, window: int = 3600):
        """Check if user is within rate limit"""
        key = f"rate_limit:{user_id}"

        # Increment counter
        current = self.redis.incr(key)

        # Set expiry on first request
        if current == 1:
            self.redis.expire(key, window)

        return current <= limit

limiter = UserRateLimiter(redis_client)

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    if not limiter.is_allowed(request.user_id, limit=100):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Process request
```

## Cost Management

### Monthly Budget Planning

```python
# scripts/estimate_costs.py
"""Estimate monthly LLM costs based on usage projections"""

# Assumptions
DAILY_ACTIVE_USERS = 1000
QUERIES_PER_USER_PER_DAY = 5
AVG_INPUT_TOKENS = 500
AVG_OUTPUT_TOKENS = 300

# Model pricing (per 1K tokens)
PRICING = {
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-4": {"input": 0.03, "output": 0.06},
    "text-embedding-3-small": {"input": 0.00002, "output": 0},
}

def estimate_monthly_cost(model: str):
    """Estimate monthly cost for given model"""
    pricing = PRICING[model]

    # Daily queries
    daily_queries = DAILY_ACTIVE_USERS * QUERIES_PER_USER_PER_DAY

    # Token usage
    daily_input_tokens = daily_queries * AVG_INPUT_TOKENS
    daily_output_tokens = daily_queries * AVG_OUTPUT_TOKENS

    # Daily cost
    daily_cost = (
        (daily_input_tokens / 1000) * pricing["input"] +
        (daily_output_tokens / 1000) * pricing["output"]
    )

    # Monthly cost (30 days)
    monthly_cost = daily_cost * 30

    return {
        "model": model,
        "daily_queries": daily_queries,
        "daily_cost": daily_cost,
        "monthly_cost": monthly_cost
    }

# Compare models
for model in ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4"]:
    result = estimate_monthly_cost(model)
    print(f"{model}: ${result['monthly_cost']:.2f}/month")

# Output:
# gpt-3.5-turbo: $562.50/month
# gpt-4o-mini: $112.50/month
# gpt-4: $13,500/month
```

### Cost Optimization Strategies

1. **Route by Complexity**
   - Simple queries → GPT-3.5-turbo
   - Moderate → GPT-4o-mini
   - Complex → GPT-4

2. **Aggressive Caching**
   - Cache identical queries
   - Semantic caching for similar queries
   - 30-50% cost reduction typical

3. **Prompt Optimization**
   - Shorter prompts save tokens
   - Remove unnecessary examples
   - Use system message efficiently

4. **Batch Processing**
   - Batch non-urgent requests
   - Process during off-peak hours
   - Lower priority for background jobs

5. **User Tiers**
   - Free tier: GPT-3.5-turbo, limited queries
   - Pro tier: GPT-4o-mini, more queries
   - Enterprise: GPT-4, unlimited

## Migration Path as Team Grows

### Startup (2-5 people) → Scale-up (10-20 people)

**Trigger**: Series A funding, growing to 10+ engineers

**Changes needed**:
1. **Framework**: Consider migrating to Haystack if stability becomes critical
2. **Architecture**: Microservices for different AI features
3. **Observability**: Upgrade to LangSmith Team/Enterprise
4. **Testing**: Implement comprehensive E2E test suite
5. **Infra**: Kubernetes for orchestration
6. **Team**: Hire dedicated AI/ML engineer

**Timeline**: 3-6 months for gradual migration

## Common Mistakes

1. **Over-optimizing too early**: Don't optimize for 1M users when you have 100
2. **Ignoring observability**: LangSmith saves 10x its cost in debugging time
3. **No cost monitoring**: Surprise $5K bill at end of month
4. **Poor error handling**: Users see raw API errors
5. **No rate limiting**: One user can drain your budget
6. **Monolith**: Hard to scale different AI features independently
7. **No testing**: Breaking changes in production

## Best Practices

1. **Invest in LangSmith from day 1** ($39-99/month is worth it)
2. **Set up cost alerts** (Slack notification at $X/day)
3. **Implement caching aggressively** (30-50% cost savings)
4. **Rate limit per user** (prevent abuse)
5. **Version prompts** (track changes, enable rollback)
6. **Monitor latency** (p50, p95, p99)
7. **Test with mocks** (faster CI, cheaper)
8. **Document architecture** (enable team collaboration)
9. **Use feature flags** (gradual rollouts)
10. **Plan for scale** (but don't over-engineer)

## Summary

**Framework Choice**:
- **RAG-focused**: LlamaIndex
- **Agent/conversation**: LangChain + LangGraph
- **Azure/.NET**: Semantic Kernel
- **High-volume**: Haystack
- **Unclear**: LangChain (most flexible)

**Essential Tools**:
- LangSmith: $39-99/month (debugging, observability)
- Vector DB: Pinecone $70/month or Qdrant $25-50/month
- Caching: Redis (Railway/Upstash)
- Error Tracking: Sentry (free tier)

**Budget** (1K users):
- LLM API: $500-2K/month
- Infrastructure: $100-500/month
- Tools/SaaS: $150-300/month
- **Total**: $750-2,800/month

**Timeline**:
- Week 1-2: Architecture + setup
- Week 3-6: Core features
- Week 7-8: Testing + observability
- Week 9-12: Polish + deploy to production

**Key Success Factors**:
1. Choose right framework for use case
2. Invest in observability (LangSmith)
3. Monitor costs from day 1
4. Enable team collaboration (testing, docs, code review)
5. Plan for 10x scale but don't over-engineer
