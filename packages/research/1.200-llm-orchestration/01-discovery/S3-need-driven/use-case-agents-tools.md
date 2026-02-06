# Use Case: Autonomous Agents with Tool Use

## Executive Summary

**Best Framework**: LangChain + LangGraph (most mature) or Semantic Kernel (enterprise/.NET)

**Time to Production**: 4-8 weeks for MVP, 12-20 weeks for production-grade

**Key Requirements**:
- Tool/function calling capabilities
- Multi-step reasoning (ReAct, Plan-and-Execute)
- Error recovery and retry logic
- Human-in-the-loop workflows
- Observability and debugging
- Production reliability

## Framework Comparison for Agents

| Framework | Agent Suitability | Key Strengths | Limitations |
|-----------|------------------|---------------|-------------|
| **LangChain + LangGraph** | Excellent (5/5) | Most mature, LinkedIn/Elastic use in production, largest ecosystem | Frequent updates |
| **Semantic Kernel** | Excellent (5/5) | Agent Framework GA, enterprise-ready, stable APIs | Smaller ecosystem |
| **LlamaIndex** | Good (3/5) | Workflow module, good for RAG-heavy agents | Not primary focus |
| **Haystack** | Good (3/5) | Pipeline-based agents, production-grade | Less flexible than LangGraph |
| **DSPy** | Fair (2/5) | Optimization-focused | Limited agent primitives |

**Winner**: **LangChain + LangGraph** for most use cases, **Semantic Kernel** for enterprise

## Agent Architectures

### 1. ReAct (Reason + Act)
Most common pattern: think, act, observe, repeat.

```python
# LangChain ReAct Agent
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain import hub

# Define tools
def search_web(query: str) -> str:
    """Search the web for information"""
    # Implementation here
    return f"Search results for: {query}"

def calculate(expression: str) -> str:
    """Calculate mathematical expressions"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

def get_weather(location: str) -> str:
    """Get weather for a location"""
    # API call here
    return f"Weather in {location}: Sunny, 72F"

tools = [
    Tool(
        name="Search",
        func=search_web,
        description="Useful for finding current information on the web"
    ),
    Tool(
        name="Calculator",
        func=calculate,
        description="Useful for mathematical calculations"
    ),
    Tool(
        name="Weather",
        func=get_weather,
        description="Get current weather for a location"
    ),
]

# Create ReAct agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)

# Create executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True,
)

# Run agent
response = agent_executor.invoke({
    "input": "What's the weather like in the city where OpenAI was founded?"
})
# Agent thinks: Need to find where OpenAI was founded
# Agent acts: Search("Where was OpenAI founded")
# Agent observes: San Francisco
# Agent thinks: Now get weather for SF
# Agent acts: Weather("San Francisco")
# Agent responds: Weather in San Francisco...
```

### 2. Plan-and-Execute
Better for complex multi-step tasks.

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Planning step
planner_prompt = PromptTemplate(
    input_variables=["objective", "tools"],
    template="""
    Create a step-by-step plan to achieve this objective: {objective}

    Available tools: {tools}

    Plan (numbered steps):
    """
)

planner = LLMChain(llm=llm, prompt=planner_prompt)

# Execution step
def execute_plan(plan_steps: list[str], tools: list):
    """Execute each step of the plan"""
    results = []

    for step in plan_steps:
        # Determine which tool to use
        tool_choice = select_tool(step, tools)

        # Execute tool
        result = tool_choice.run(step)
        results.append(result)

    return results

# Usage
objective = "Research competitors, analyze pricing, create comparison report"
plan = planner.run(objective=objective, tools=tool_names)
results = execute_plan(plan, tools)
```

### 3. LangGraph Stateful Agents (Recommended)
Best for complex, non-linear workflows.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# Define state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_action: str
    gathered_info: dict

# Define nodes
def plan_step(state: AgentState):
    """Plan next action"""
    messages = state["messages"]
    # LLM decides next action
    response = llm.invoke(messages)

    return {
        "messages": [response],
        "next_action": extract_action(response),
    }

def execute_tool(state: AgentState):
    """Execute the chosen tool"""
    action = state["next_action"]

    # Route to appropriate tool
    if action == "search":
        result = search_tool.run(state["messages"][-1])
    elif action == "calculate":
        result = calculator.run(state["messages"][-1])

    return {
        "messages": [{"role": "system", "content": result}],
        "gathered_info": {**state["gathered_info"], action: result},
    }

def should_continue(state: AgentState):
    """Decide if we should continue or finish"""
    messages = state["messages"]
    last_message = messages[-1]

    if "FINAL ANSWER" in last_message.content:
        return "end"
    else:
        return "continue"

# Build graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("plan", plan_step)
workflow.add_node("execute", execute_tool)

# Add edges
workflow.set_entry_point("plan")
workflow.add_conditional_edges(
    "plan",
    should_continue,
    {
        "continue": "execute",
        "end": END,
    }
)
workflow.add_edge("execute", "plan")

# Compile
app = workflow.compile()

# Run
result = app.invoke({
    "messages": [{"role": "user", "content": "Find the population of Tokyo and convert it to scientific notation"}],
    "next_action": "",
    "gathered_info": {},
})
```

### 4. Semantic Kernel Agent Framework (Enterprise)

```csharp
// C# example for enterprise teams
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.ChatCompletion;

// Create kernel
var builder = Kernel.CreateBuilder();
builder.AddOpenAIChatCompletion("gpt-4", apiKey);

// Add plugins (tools)
builder.Plugins.AddFromType<SearchPlugin>();
builder.Plugins.AddFromType<CalculatorPlugin>();
builder.Plugins.AddFromType<WeatherPlugin>();

var kernel = builder.Build();

// Create agent
var agent = new ChatCompletionAgent
{
    Name = "Assistant",
    Instructions = "You are a helpful assistant. Use tools as needed.",
    Kernel = kernel,
    Arguments = new KernelArguments
    {
        { "max_iterations", 5 }
    }
};

// Run agent
var response = await agent.InvokeAsync("What's the weather in San Francisco?");
```

## Tool/Function Calling Patterns

### Defining Tools (LangChain)

```python
from langchain.tools import tool
from typing import Optional

@tool
def search_database(
    query: str,
    limit: Optional[int] = 10
) -> str:
    """
    Search the customer database.

    Args:
        query: Search query string
        limit: Maximum number of results (default: 10)

    Returns:
        JSON string with search results
    """
    # Implementation
    results = db.search(query, limit=limit)
    return json.dumps(results)

@tool
def send_email(
    to: str,
    subject: str,
    body: str
) -> str:
    """
    Send an email to a customer.

    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content

    Returns:
        Success or error message
    """
    # Implementation
    try:
        email_client.send(to, subject, body)
        return f"Email sent successfully to {to}"
    except Exception as e:
        return f"Error sending email: {e}"

@tool
async def analyze_sentiment(text: str) -> str:
    """
    Analyze sentiment of text.

    Args:
        text: Text to analyze

    Returns:
        Sentiment score and label
    """
    # Async tool for longer operations
    result = await sentiment_api.analyze(text)
    return json.dumps(result)
```

### Structured Output with Pydantic

```python
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool

class SearchInput(BaseModel):
    query: str = Field(description="The search query")
    filters: dict = Field(description="Optional filters", default={})
    limit: int = Field(description="Max results", default=10)

class SearchOutput(BaseModel):
    results: list[dict]
    total_count: int
    took_ms: float

def structured_search(query: str, filters: dict, limit: int) -> SearchOutput:
    """Search with structured input/output"""
    start = time.time()
    results = db.search(query, filters, limit)

    return SearchOutput(
        results=results,
        total_count=len(results),
        took_ms=(time.time() - start) * 1000
    )

# Create structured tool
search_tool = StructuredTool.from_function(
    func=structured_search,
    name="DatabaseSearch",
    description="Search the database with filters",
    args_schema=SearchInput,
    return_direct=False,
)
```

### Tool Selection Strategies

```python
# 1. Automatic tool selection (default)
agent = create_react_agent(llm, tools, prompt)

# 2. Required tool
# Force agent to use specific tool
from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    required_tools=["Search"],  # Must use Search
)

# 3. Tool filtering by context
def get_tools_for_user(user_role: str):
    """Return tools based on user permissions"""
    base_tools = [search_tool, calculator_tool]

    if user_role == "admin":
        base_tools.extend([delete_tool, admin_tool])

    return base_tools

tools = get_tools_for_user(current_user.role)
agent = create_react_agent(llm, tools, prompt)
```

## Multi-Step Reasoning

### ReAct Reasoning Chain

```python
# Example agent execution trace
"""
Thought: I need to find information about LangChain
Action: Search
Action Input: "LangChain framework"
Observation: LangChain is an orchestration framework for LLMs...

Thought: Now I need to find recent developments
Action: Search
Action Input: "LangChain 2025 updates"
Observation: In 2025, LangChain introduced...

Thought: I have enough information to answer
Final Answer: LangChain is a framework that...
"""
```

### Chain-of-Thought with Tools

```python
from langchain.prompts import ChatPromptTemplate

cot_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that thinks step-by-step.

For each user question:
1. Break down the problem
2. Identify what information you need
3. Use tools to gather information
4. Synthesize a final answer

Think out loud about your reasoning."""),
    ("user", "{input}"),
])

# Agent will show reasoning steps
agent = create_react_agent(llm, tools, cot_prompt)
```

## Error Recovery and Retries

### Retry Logic

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry_if_exception_type=APIError
)
def resilient_tool_call(tool_name: str, **kwargs):
    """Call tool with automatic retries"""
    return tools[tool_name].run(**kwargs)

# LangChain agent with error handling
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=5,
    max_execution_time=60,  # timeout after 60s
    handle_parsing_errors=True,
    early_stopping_method="generate",  # graceful degradation
)
```

### Custom Error Handlers

```python
from langchain.callbacks import BaseCallbackHandler

class ErrorHandlingCallback(BaseCallbackHandler):
    def on_tool_error(self, error: Exception, **kwargs):
        """Handle tool errors gracefully"""
        tool_name = kwargs.get("name", "unknown")

        # Log error
        logger.error(f"Tool {tool_name} failed: {error}")

        # Notify monitoring
        metrics.increment(f"tool_error_{tool_name}")

        # Could trigger fallback logic
        if isinstance(error, RateLimitError):
            time.sleep(60)  # backoff

    def on_agent_finish(self, finish, **kwargs):
        """Track successful completions"""
        metrics.increment("agent_success")

# Use callback
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    callbacks=[ErrorHandlingCallback()],
)
```

### Fallback Strategies

```python
def agent_with_fallback(user_input: str):
    """Try agent, fall back to simple LLM if it fails"""
    try:
        # Try agent with tools
        response = agent_executor.invoke({"input": user_input})
        return response["output"]

    except Exception as e:
        logger.warning(f"Agent failed: {e}, falling back to simple LLM")

        # Fallback to basic LLM call
        fallback_llm = ChatOpenAI(model="gpt-4")
        response = fallback_llm.invoke(user_input)
        return response.content
```

## Human-in-the-Loop Workflows

### Approval Required

```python
from langgraph.checkpoint import MemorySaver
from langgraph.graph import StateGraph

class ApprovalState(TypedDict):
    messages: list
    pending_action: Optional[dict]
    approved: bool

def agent_step(state: ApprovalState):
    """Agent proposes action"""
    response = agent.invoke(state["messages"])

    # Extract proposed action
    action = parse_action(response)

    if requires_approval(action):
        return {
            "pending_action": action,
            "approved": False,
        }
    else:
        # Auto-approve safe actions
        return execute_action(action)

def human_approval(state: ApprovalState):
    """Wait for human approval"""
    action = state["pending_action"]

    # In production, this would be async (webhook, UI, etc)
    print(f"Agent wants to: {action}")
    approval = input("Approve? (yes/no): ")

    return {"approved": approval.lower() == "yes"}

# Build workflow with approval gate
workflow = StateGraph(ApprovalState)
workflow.add_node("agent", agent_step)
workflow.add_node("approval", human_approval)

workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    lambda s: "needs_approval" if s.get("pending_action") else "done",
    {
        "needs_approval": "approval",
        "done": END,
    }
)

# Enable checkpointing for interruption
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)
```

### Review and Edit

```python
def agent_with_review(user_input: str):
    """Agent drafts response, human reviews before sending"""

    # Agent drafts
    draft = agent_executor.invoke({"input": user_input})

    # Present to human
    print("=== Agent Draft ===")
    print(draft["output"])
    print("==================")

    action = input("(a)pprove, (e)dit, (r)eject: ")

    if action == "a":
        return draft["output"]
    elif action == "e":
        edited = input("Enter edited version: ")
        return edited
    else:
        return "Action cancelled by user"
```

### Confidence-Based Intervention

```python
def agent_with_confidence_check(user_input: str):
    """Only ask human when agent is uncertain"""

    response = agent_executor.invoke({"input": user_input})

    # Extract confidence (would need custom agent)
    confidence = extract_confidence(response)

    if confidence < 0.7:
        print(f"Agent is uncertain (confidence: {confidence})")
        print(f"Draft answer: {response['output']}")

        override = input("Override? (leave empty to accept): ")
        if override:
            return override

    return response["output"]
```

## Example Agent with 3-5 Tools

### Customer Support Agent

```python
from langchain.agents import create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import json

# Tool 1: Search knowledge base
@tool
def search_kb(query: str) -> str:
    """Search company knowledge base for help articles"""
    # Vector search implementation
    results = kb_index.similarity_search(query, k=3)
    return json.dumps([r.page_content for r in results])

# Tool 2: Look up customer info
@tool
def get_customer_info(customer_id: str) -> str:
    """Retrieve customer account information"""
    customer = db.customers.find_one({"id": customer_id})
    return json.dumps({
        "name": customer["name"],
        "plan": customer["plan"],
        "status": customer["status"],
        "tickets": customer["open_tickets"],
    })

# Tool 3: Create support ticket
@tool
def create_ticket(
    customer_id: str,
    subject: str,
    description: str,
    priority: str = "normal"
) -> str:
    """Create a support ticket"""
    ticket = {
        "customer_id": customer_id,
        "subject": subject,
        "description": description,
        "priority": priority,
        "created_at": datetime.now(),
    }

    ticket_id = db.tickets.insert_one(ticket).inserted_id
    return f"Ticket created: {ticket_id}"

# Tool 4: Check order status
@tool
def check_order_status(order_id: str) -> str:
    """Check the status of an order"""
    order = db.orders.find_one({"id": order_id})
    return json.dumps({
        "status": order["status"],
        "tracking": order.get("tracking_number"),
        "eta": order.get("estimated_delivery"),
    })

# Tool 5: Process refund
@tool
def process_refund(order_id: str, amount: float, reason: str) -> str:
    """Process a refund (requires approval for >$100)"""
    if amount > 100:
        return "APPROVAL_REQUIRED: Refund over $100 needs manager approval"

    # Process refund
    refund_id = payment_service.refund(order_id, amount)
    return f"Refund processed: {refund_id}"

# Create agent
tools = [
    search_kb,
    get_customer_info,
    create_ticket,
    check_order_status,
    process_refund,
]

llm = ChatOpenAI(model="gpt-4", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a customer support agent. Your goal is to help customers efficiently.

Use the available tools to:
- Look up customer information
- Search the knowledge base for solutions
- Check order status
- Create tickets for complex issues
- Process refunds when appropriate

Always be helpful, professional, and empathetic."""),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_openai_tools_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10,
)

# Example usage
response = agent_executor.invoke({
    "input": "Customer #12345 says their order hasn't arrived. Can you help?"
})

# Agent will:
# 1. get_customer_info("12345") - get customer details
# 2. Find order ID from customer info
# 3. check_order_status(order_id) - check shipping status
# 4. search_kb("late delivery") - find policy
# 5. Respond with status + next steps
```

## Production Agent Deployments

### Architecture: Agent API Service

```python
# FastAPI production agent
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio

app = FastAPI()

class AgentRequest(BaseModel):
    session_id: str
    user_input: str
    user_id: str

class AgentResponse(BaseModel):
    response: str
    tools_used: list[str]
    execution_time_ms: float
    cost_usd: float

@app.post("/agent/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """Run agent with timeout and cost tracking"""
    start_time = time.time()

    # Get user-specific tools (permissions)
    tools = get_tools_for_user(request.user_id)

    # Create agent executor
    agent_executor = create_agent_executor(tools)

    # Run with timeout
    try:
        result = await asyncio.wait_for(
            agent_executor.ainvoke({"input": request.user_input}),
            timeout=30.0
        )

        execution_time = (time.time() - start_time) * 1000

        # Track metrics
        tools_used = extract_tools_used(result)
        cost = calculate_cost(result)

        # Store in DB for analytics
        db.agent_runs.insert_one({
            "session_id": request.session_id,
            "user_id": request.user_id,
            "input": request.user_input,
            "output": result["output"],
            "tools_used": tools_used,
            "execution_time_ms": execution_time,
            "cost_usd": cost,
            "timestamp": datetime.now(),
        })

        return AgentResponse(
            response=result["output"],
            tools_used=tools_used,
            execution_time_ms=execution_time,
            cost_usd=cost,
        )

    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Agent timeout")
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail="Agent error")

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### Deployment Options

#### 1. Serverless (Modal, AWS Lambda)
```python
# Modal deployment
import modal

stub = modal.Stub("support-agent")

@stub.function(
    image=modal.Image.debian_slim().pip_install(["langchain", "openai"]),
    secrets=[modal.Secret.from_name("openai-secret")],
    timeout=60,
)
def run_agent(user_input: str):
    # Agent code here
    return agent_executor.invoke({"input": user_input})

@stub.local_entrypoint()
def main():
    result = run_agent.remote("Help me with my order")
    print(result)
```

#### 2. Containerized (Docker + Cloud Run)
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

```yaml
# Cloud Run deployment
gcloud run deploy support-agent \
  --image gcr.io/project/support-agent \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --timeout 60 \
  --max-instances 10
```

#### 3. Kubernetes (Enterprise)
```yaml
# k8s deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent
  template:
    metadata:
      labels:
        app: agent
    spec:
      containers:
      - name: agent
        image: agent:v1.0
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
```

## Monitoring and Observability

### LangSmith Integration
```python
import os

# Enable tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-key"
os.environ["LANGCHAIN_PROJECT"] = "support-agent-prod"

# All agent runs automatically traced
# View in LangSmith dashboard:
# - Step-by-step execution
# - Tool calls and results
# - Token usage
# - Latency breakdown
# - Error traces
```

### Custom Metrics
```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
agent_requests = Counter('agent_requests_total', 'Total agent requests')
agent_errors = Counter('agent_errors_total', 'Agent errors', ['error_type'])
agent_latency = Histogram('agent_latency_seconds', 'Agent latency')
agent_cost = Histogram('agent_cost_usd', 'Agent cost in USD')
tools_used = Counter('tools_used_total', 'Tool usage', ['tool_name'])

# Track in agent
@agent_latency.time()
def run_agent_with_metrics(user_input: str):
    agent_requests.inc()

    try:
        result = agent_executor.invoke({"input": user_input})

        # Track tools used
        for tool in extract_tools_used(result):
            tools_used.labels(tool_name=tool).inc()

        # Track cost
        cost = calculate_cost(result)
        agent_cost.observe(cost)

        return result

    except Exception as e:
        agent_errors.labels(error_type=type(e).__name__).inc()
        raise
```

## Cost Analysis

### Per-Agent-Run Cost Breakdown
```python
# Example: Customer support agent

# Tool calls: ~0 cost (database lookups, API calls)
# LLM calls during reasoning:
#   - Planning: 500 tokens @ $0.03/1K = $0.015
#   - Tool selection (3 iterations): 300 tokens each = $0.027
#   - Final response: 400 tokens = $0.012
# Total per run: ~$0.054

# For 1000 agent runs/day:
# Daily cost: $54
# Monthly cost: ~$1,620

# Optimization:
# - Use GPT-4o-mini for tool selection: 60% cheaper
# - Cache tool descriptions: save ~20%
# - Optimized cost: ~$650/month
```

## Common Pitfalls

1. **Infinite loops**: Agent gets stuck in reasoning loop
2. **Tool hallucination**: Agent invents tools that don't exist
3. **No timeouts**: Agent runs indefinitely on complex tasks
4. **Poor error handling**: Crashes on tool failures
5. **No human oversight**: Agents take actions without approval
6. **Insufficient testing**: Edge cases break production
7. **Ignoring costs**: Complex agents can be expensive

## Best Practices

1. **Always set max_iterations** (3-10 typical)
2. **Implement timeouts** (30-60s for user-facing)
3. **Use LangGraph for complex flows** (better than ReAct)
4. **Monitor everything** (LangSmith + custom metrics)
5. **Test edge cases** (tool failures, timeouts, bad inputs)
6. **Implement HITL for high-stakes actions** (refunds, deletions)
7. **Use structured outputs** (Pydantic for type safety)
8. **Cache tool descriptions** (reduce token usage)
9. **Graceful degradation** (fallback to simple LLM)
10. **Regular evaluation** (accuracy, latency, cost metrics)

## Summary

**For agent systems, choose:**
- **LangChain + LangGraph** for most use cases (most mature, production-proven)
- **Semantic Kernel** for enterprise/.NET environments (stable, Microsoft support)

**Time to production: 4-20 weeks**
**Cost: $500-5000/month depending on usage**

**Critical success factors**:
1. Robust error handling and retries
2. Proper monitoring and observability
3. Human-in-the-loop for high-stakes decisions
4. Comprehensive testing of agent behaviors
5. Cost monitoring and optimization
