# MCP Server Implementation - Domain Explainer

**Audience**: Developers new to MCP who need to build tool servers for LLMs
**Reading Time**: 10 minutes

---

## What is MCP?

**Model Context Protocol (MCP)** is an open standard for connecting LLMs (like Claude) to external tools and data sources. Think of it as "USB-C for AI" - a universal connector that lets AI assistants interact with your systems.

Launched by Anthropic in November 2024, MCP has been adopted by:
- **OpenAI** (ChatGPT, Agents SDK) - March 2025
- **Microsoft** (Windows integration) - May 2025
- **Linux Foundation** (Agentic AI Foundation) - December 2025

---

## Why Does MCP Exist?

Before MCP, every AI integration was custom:
- Each LLM had different tool-calling conventions
- Developers built separate integrations for Claude, GPT, etc.
- No standard way to expose data/functionality to AI

MCP solves this with a single protocol:
- Write one server, connect to any MCP-compatible client
- Standardized tool schemas, resource access, prompt templates
- Protocol-level security and capability negotiation

---

## Core Concepts

### 1. MCP Server
A program that exposes functionality to LLMs. You build this.

### 2. MCP Client
An LLM application that connects to servers. Claude Desktop, Claude.ai, ChatGPT desktop are clients.

### 3. Tools
Functions the LLM can call. Like API endpoints but for AI:

```python
@mcp.tool()
def search_database(query: str) -> list[dict]:
    """Search the database for matching records."""
    return db.search(query)
```

The LLM sees the function name, description, and parameter schema. When it decides to use the tool, MCP handles the invocation.

### 4. Resources
Read-only data the LLM can access. Like GET endpoints:

```python
@mcp.resource("config://{section}")
def get_config(section: str) -> str:
    """Get configuration for a section."""
    return config[section]
```

### 5. Prompts
Reusable message templates:

```python
@mcp.prompt()
def summarize(text: str) -> str:
    """Create a summarization prompt."""
    return f"Please summarize:\n\n{text}"
```

---

## How It Works

```
┌─────────────┐         JSON-RPC 2.0         ┌─────────────┐
│   Claude    │ ◄──────────────────────────► │ Your MCP    │
│   Desktop   │      (stdio or HTTP)         │   Server    │
│  (Client)   │                              │             │
└─────────────┘                              └─────────────┘

1. Client discovers server capabilities
2. Client lists available tools/resources
3. When user asks something requiring a tool:
   - LLM decides which tool to call
   - Client sends tool call to server
   - Server executes and returns result
   - LLM incorporates result into response
```

---

## Transport Options

| Transport | When to Use |
|-----------|-------------|
| **stdio** | Local development, CLI tools. Server runs as subprocess. |
| **Streamable HTTP** | Production, remote servers. Standard HTTP with optional streaming. |
| **SSE** | Legacy. Deprecated since late 2024. |

**Default**: stdio for local, Streamable HTTP for deployed.

---

## Python Library Options

### For Most Projects: FastMCP

```bash
pip install fastmcp
```

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

**Why FastMCP**:
- Minimal boilerplate
- Decorator-based (Pythonic)
- Built-in auth, deployment tools
- 21k+ GitHub stars, actively maintained

### For Protocol Control: MCP SDK

```bash
pip install "mcp[cli]"
```

Use when you need low-level access or are building MCP tooling.

### For Existing FastAPI Apps: FastAPI-MCP

```bash
pip install fastapi-mcp
```

Automatically exposes your REST endpoints as MCP tools.

---

## A Complete Example

```python
from fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("task-server")

# In-memory storage
tasks = {}
next_id = 1

@mcp.tool()
def create_task(title: str, priority: str = "medium") -> dict:
    """Create a new task.

    Args:
        title: The task title
        priority: low, medium, or high
    """
    global next_id
    task = {
        "id": next_id,
        "title": title,
        "priority": priority,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    tasks[next_id] = task
    next_id += 1
    return task

@mcp.tool()
def list_tasks(status: str = "all") -> list[dict]:
    """List all tasks, optionally filtered by status.

    Args:
        status: Filter by 'pending', 'completed', or 'all'
    """
    if status == "all":
        return list(tasks.values())
    return [t for t in tasks.values() if t["status"] == status]

@mcp.tool()
def complete_task(task_id: int) -> dict:
    """Mark a task as completed.

    Args:
        task_id: The ID of the task to complete
    """
    if task_id not in tasks:
        raise ValueError(f"Task {task_id} not found")
    tasks[task_id]["status"] = "completed"
    tasks[task_id]["completed_at"] = datetime.now().isoformat()
    return tasks[task_id]

if __name__ == "__main__":
    mcp.run()
```

---

## Running Your Server

### Local Development (stdio)

```bash
# Run directly
python my_server.py

# Or with fastmcp CLI
fastmcp run my_server.py
```

### Connect to Claude Desktop

Add to Claude Desktop config (`~/.config/claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/my_server.py"]
    }
  }
}
```

Restart Claude Desktop. Your tools appear in the interface.

### Production (HTTP)

```python
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
```

---

## Common Patterns

### Error Handling
Raise exceptions - FastMCP converts them to MCP errors:

```python
@mcp.tool()
def get_user(user_id: int) -> dict:
    if user_id not in users:
        raise ValueError(f"User {user_id} not found")
    return users[user_id]
```

### Type Hints
FastMCP uses type hints for schema generation:

```python
from pydantic import BaseModel

class Task(BaseModel):
    id: int
    title: str
    priority: str

@mcp.tool()
def get_task(task_id: int) -> Task:
    """Get a task by ID."""
    return Task(**tasks[task_id])
```

### Async Support
Both sync and async work:

```python
@mcp.tool()
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

---

## Testing

FastMCP provides in-memory testing:

```python
from fastmcp import Client

async def test_create_task():
    async with Client(mcp) as client:
        result = await client.call_tool("create_task", {
            "title": "Test task",
            "priority": "high"
        })
        assert result["title"] == "Test task"
```

---

## Security Considerations

1. **Input validation**: Validate all tool parameters
2. **Authentication**: Use FastMCP's built-in auth or implement your own
3. **Least privilege**: Only expose what's necessary
4. **Rate limiting**: Protect against abuse

---

## Next Steps

1. **Start simple**: Build a server with 2-3 tools
2. **Test locally**: Connect to Claude Desktop
3. **Add complexity**: Resources, prompts, auth
4. **Deploy**: Streamable HTTP for production

---

## Resources

- [MCP Specification](https://modelcontextprotocol.io)
- [FastMCP Documentation](https://gofastmcp.com)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Anthropic MCP Course](https://anthropic.skilljar.com/introduction-to-model-context-protocol)

---

## Glossary

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - the standard |
| **Tool** | Function an LLM can invoke |
| **Resource** | Read-only data an LLM can access |
| **Prompt** | Reusable message template |
| **Transport** | Communication channel (stdio, HTTP) |
| **FastMCP** | High-level Python framework |
| **JSON-RPC 2.0** | Underlying message protocol |
