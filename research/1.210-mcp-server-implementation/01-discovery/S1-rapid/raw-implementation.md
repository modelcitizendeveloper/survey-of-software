# Raw MCP Implementation - Approach Profile

**Package**: None (stdlib only)
**Dependencies**: Python stdlib, optionally `json`, `sys`
**License**: N/A
**Use Case**: Educational, embedded, minimal footprint

---

## Overview

MCP can be implemented without any SDK by directly handling JSON-RPC 2.0 messages over stdio or HTTP. This approach is educational and useful for understanding protocol internals or when external dependencies are unacceptable.

---

## Key Insight

> "At its core, MCP is just JSON-RPC 2.0 over newline-delimited streams. No magic, no hidden complexity—just structured messages over STDIO."

---

## Protocol Basics

### Transport: STDIO

Messages are newline-delimited JSON over stdin/stdout:

```
{"jsonrpc":"2.0","method":"initialize","params":{...},"id":1}\n
{"jsonrpc":"2.0","result":{...},"id":1}\n
```

### Message Types

1. **Request**: Has `method`, `params`, `id`
2. **Response**: Has `result` or `error`, `id`
3. **Notification**: Has `method`, `params`, no `id`

---

## Minimal Implementation

```python
import sys
import json
from datetime import datetime

def send_response(id, result):
    response = {"jsonrpc": "2.0", "result": result, "id": id}
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()

def send_error(id, code, message):
    response = {
        "jsonrpc": "2.0",
        "error": {"code": code, "message": message},
        "id": id
    }
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()

def handle_initialize(id, params):
    send_response(id, {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "serverInfo": {"name": "raw-server", "version": "1.0.0"}
    })

def handle_tools_list(id, params):
    send_response(id, {
        "tools": [{
            "name": "get_time",
            "description": "Get current time",
            "inputSchema": {"type": "object", "properties": {}}
        }]
    })

def handle_tools_call(id, params):
    tool_name = params.get("name")
    if tool_name == "get_time":
        send_response(id, {
            "content": [{"type": "text", "text": datetime.now().isoformat()}]
        })
    else:
        send_error(id, -32601, f"Unknown tool: {tool_name}")

def main():
    for line in sys.stdin:
        try:
            msg = json.loads(line.strip())
            method = msg.get("method")
            id = msg.get("id")
            params = msg.get("params", {})

            if method == "initialize":
                handle_initialize(id, params)
            elif method == "tools/list":
                handle_tools_list(id, params)
            elif method == "tools/call":
                handle_tools_call(id, params)
            elif method == "notifications/initialized":
                pass  # Notification, no response
            else:
                if id:  # Only respond to requests, not notifications
                    send_error(id, -32601, f"Unknown method: {method}")
        except json.JSONDecodeError:
            send_error(None, -32700, "Parse error")

if __name__ == "__main__":
    main()
```

---

## Protocol Lifecycle

1. **Initialize**: Client sends `initialize`, server responds with capabilities
2. **Initialized**: Client sends `notifications/initialized` (no response)
3. **Operation**: Client calls `tools/list`, `tools/call`, etc.
4. **Shutdown**: Client closes connection

---

## Capabilities Declaration

Server declares what it supports:

```json
{
  "capabilities": {
    "tools": {},
    "resources": {},
    "prompts": {},
    "logging": {}
  }
}
```

Only declare capabilities you implement.

---

## Error Codes

| Code | Meaning |
|------|---------|
| -32700 | Parse error |
| -32600 | Invalid request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |

---

## Strengths

1. **Zero dependencies**: Pure Python stdlib
2. **Full understanding**: Learn protocol internals
3. **Minimal footprint**: ~50 lines for basic server
4. **Debuggable**: Easy to log and inspect messages
5. **Portable**: Works anywhere Python runs

---

## Limitations

1. **No schema validation**: Must implement manually
2. **No transport abstraction**: Locked to one transport
3. **No error handling**: Must build robust error handling
4. **No testing utilities**: No mock clients
5. **Maintenance burden**: Must track protocol changes

---

## When to Choose Raw Implementation

- Learning MCP protocol internals
- Extremely resource-constrained environments
- Cannot add external dependencies
- Building custom transports
- Protocol debugging and analysis

---

## When to Avoid

- Production applications (use FastMCP or SDK)
- Time-constrained projects
- Teams unfamiliar with JSON-RPC
- Need resources, prompts, or complex features

---

## Learning Resources

- [Understanding MCP Through Raw STDIO Communication](https://foojay.io/today/understanding-mcp-through-raw-stdio-communication/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/docs/concepts/transports)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)

---

## Advanced: HTTP Transport

For HTTP, implement POST endpoint accepting JSON-RPC:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class MCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        request = json.loads(body)

        # Route to handlers...
        response = handle_request(request)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
```

---

## Recommendation

Use raw implementation only for:
1. Educational purposes
2. Understanding protocol before using SDK
3. Environments where no deps are allowed

For all other cases, use FastMCP (simplest) or MCP SDK (official).
