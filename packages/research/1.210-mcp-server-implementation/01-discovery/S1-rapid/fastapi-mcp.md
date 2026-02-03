# FastAPI-MCP - Library Profile

**Package**: `fastapi-mcp`
**Version**: Latest (July 2025)
**License**: MIT
**Maintainer**: Tadata Inc.
**Repository**: https://github.com/tadata-org/fastapi_mcp
**PyPI**: https://pypi.org/project/fastapi-mcp/

---

## Overview

FastAPI-MCP automatically exposes existing FastAPI endpoints as MCP tools with zero configuration. It's designed for brownfield projects where you want to add MCP capability to an existing REST API without rewriting code.

---

## Installation

```bash
pip install fastapi-mcp
# or
uv add fastapi-mcp
```

**Requirements**: Python >= 3.10, FastAPI

---

## Key Features

### Zero Configuration
Automatically introspects FastAPI routes and creates MCP tools:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": "John"}

@app.post("/tasks")
def create_task(title: str, priority: str = "medium"):
    return {"title": title, "priority": priority}

# Add MCP with one line
mcp = FastApiMCP(app)
mcp.mount()  # Available at /mcp
```

### Schema Preservation
- Preserves Pydantic request/response models
- Maintains endpoint documentation
- Swagger-equivalent descriptions in MCP tools

### Authentication Reuse
Uses existing FastAPI `Depends()` for authorization:

```python
from fastapi import Depends, HTTPException

def verify_token(token: str = Header(...)):
    if token != "valid":
        raise HTTPException(401)
    return token

@app.get("/protected")
def protected_endpoint(user=Depends(verify_token)):
    return {"data": "secret"}

# MCP tools inherit the same auth
```

### ASGI Native
Direct ASGI interface - no HTTP hop:
- Efficient communication
- No network overhead for local calls
- Preserves request context

---

## Deployment Options

### Same Application
```python
app = FastAPI()
mcp = FastApiMCP(app)
mcp.mount()  # /mcp endpoint added to app
```

### Separate Application
```python
app = FastAPI()
mcp_app = FastApiMCP(app).create_app()
# Deploy mcp_app separately
```

---

## Comparison to FastMCP

| Aspect | FastAPI-MCP | FastMCP 2.0 |
|--------|-------------|-------------|
| Use Case | Brownfield (existing API) | Greenfield (new project) |
| Configuration | Zero | Minimal |
| Auth | Reuses FastAPI Depends | Built-in OAuth providers |
| Learning Curve | Very low (if you know FastAPI) | Low |
| Features | Endpoint exposure only | Full MCP primitives |

---

## Strengths

1. **Zero configuration**: Automatic endpoint introspection
2. **Preserves existing code**: No rewrite needed
3. **Auth reuse**: Same auth as REST endpoints
4. **ASGI native**: Efficient, no HTTP hop
5. **Dual interface**: Maintain REST + MCP simultaneously

---

## Limitations

1. **FastAPI-only**: Requires FastAPI application
2. **Endpoint-focused**: Doesn't support MCP resources/prompts natively
3. **Brownfield-only**: Not suitable for MCP-first projects
4. **Less control**: Auto-generation may not match desired MCP schema

---

## When to Choose FastAPI-MCP

- Existing FastAPI application
- Want to expose REST endpoints to LLMs
- Need to maintain both REST and MCP interfaces
- Rapid MCP addition without code changes

---

## When to Avoid

- New MCP-first projects (use FastMCP)
- Need full MCP primitives (resources, prompts)
- Non-FastAPI applications
- Want custom tool schemas

---

## Related: FastMCP's FastAPI Integration

FastMCP 2.0 also offers FastAPI integration via `FastMCP.from_fastapi()`:

```python
from fastmcp import FastMCP

mcp = FastMCP.from_fastapi(app)
```

This is similar to FastAPI-MCP but with access to FastMCP's full feature set.

---

## Example: Complete Integration

```python
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel

app = FastAPI(title="Task API")

class Task(BaseModel):
    id: int
    title: str
    priority: str

tasks_db = {}

def api_key_auth(x_api_key: str = Header(...)):
    if x_api_key != "secret":
        raise HTTPException(401, "Invalid API key")
    return x_api_key

@app.get("/tasks", response_model=list[Task])
def list_tasks(auth=Depends(api_key_auth)):
    """List all tasks."""
    return list(tasks_db.values())

@app.post("/tasks", response_model=Task)
def create_task(title: str, priority: str = "medium", auth=Depends(api_key_auth)):
    """Create a new task."""
    task_id = len(tasks_db) + 1
    task = Task(id=task_id, title=title, priority=priority)
    tasks_db[task_id] = task
    return task

# Add MCP - tools automatically created for list_tasks and create_task
# Auth is enforced via the same Depends()
mcp = FastApiMCP(app)
mcp.mount()

# MCP available at: http://localhost:8000/mcp
# REST available at: http://localhost:8000/tasks
```

---

## Sources

- https://github.com/tadata-org/fastapi_mcp
- https://pypi.org/project/fastapi-mcp/
- https://www.infoq.com/news/2025/04/fastapi-mcp/
- https://www.analyticsvidhya.com/blog/2025/05/fastapi-mcp/
