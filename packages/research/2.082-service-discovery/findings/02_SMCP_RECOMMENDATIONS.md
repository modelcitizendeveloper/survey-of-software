# SMCP Service Discovery Recommendations

**Experiment**: 2.082 Service Discovery Patterns
**Component**: Paulina (MCP Server Registry)
**Target Scale**: Single node to small cluster (1-5 nodes)
**Date**: 2026-01-08

---

## Executive Summary

For SMCP's Paulina registry component, we recommend a **lightweight, single-node-first design** that adopts proven patterns from Consul and etcd while explicitly skipping enterprise complexity. The core insight: MCP servers are typically long-running local processes, not ephemeral cloud instances - this fundamentally changes which patterns make sense.

---

## ADOPT: Patterns Worth Implementing

### A1. Self-Registration via API

**Pattern:** Push-based self-registration where MCP servers announce themselves

**Why Adopt:**
- MCP servers already have a startup phase - natural place for registration
- Aligns with MCP protocol's `initialize` handshake
- No external registrar infrastructure needed
- Each server controls its own metadata

**Paulina Implementation:**
```python
# MCP server registers itself at startup
paulina.register(
    name="filesystem-server",
    transport="stdio",
    command=["/usr/local/bin/mcp-filesystem"],
    capabilities={
        "tools": ["read_file", "write_file", "list_dir"],
        "resources": ["file://*"],
    }
)
```

**Complexity:** Low
**Value:** High - foundational pattern

---

### A2. TTL-Based Health with Lease Refresh

**Pattern:** Services maintain registration via periodic heartbeats, auto-removed on expiry

**Why Adopt:**
- Works for any transport (stdio, HTTP, SSE) - no inbound probes needed
- etcd's lease model is elegant and proven
- Natural fit: if MCP server stops heartbeating, it's dead
- Handles crash scenarios automatically

**Paulina Implementation:**
```python
# Server-side: heartbeat loop
async def heartbeat_loop(paulina, server_id, ttl=30):
    while running:
        await paulina.refresh(server_id)
        await asyncio.sleep(ttl // 2)

# Registry-side: prune expired entries
async def prune_expired():
    now = time.time()
    for server in registry.values():
        if now > server.expires_at:
            registry.remove(server.id)
```

**Recommended TTL:** 30 seconds (with 15s refresh interval)

**Complexity:** Low
**Value:** High - essential for dynamic environments

---

### A3. Key-Value Metadata for Capabilities

**Pattern:** Structured metadata (like Consul's ServiceMeta) for storing MCP capabilities

**Why Adopt:**
- MCP servers have rich metadata: tools, resources, prompts, sampling support
- Clients need to query "which servers have tool X?"
- Consul's key-value approach is flexible without being complex

**Paulina Schema:**
```yaml
server:
  id: "filesystem-abc123"
  name: "filesystem"
  version: "1.0.0"
  transport: "stdio"
  command: ["/usr/local/bin/mcp-filesystem"]
  capabilities:
    tools:
      - name: "read_file"
        description: "Read contents of a file"
      - name: "write_file"
        description: "Write contents to a file"
    resources:
      - uri_template: "file:///{path}"
        name: "File"
    sampling: true
    logging: true
  tags: ["filesystem", "local", "production"]
  registered_at: "2026-01-08T10:00:00Z"
  expires_at: "2026-01-08T10:00:30Z"
```

**Query Support:**
```python
# Find servers with specific tool
servers = paulina.find(tool="read_file")

# Find servers supporting sampling
servers = paulina.find(capability="sampling")

# Tag-based filtering
servers = paulina.find(tags=["production"])
```

**Complexity:** Medium
**Value:** High - enables smart client routing

---

### A4. API-Based Discovery (Not DNS)

**Pattern:** HTTP/gRPC API for service queries (like Consul's catalog API)

**Why Adopt:**
- Rich query capabilities (filter by tool, capability, version)
- Real-time - no DNS caching issues
- Easy to add subscriptions/watches later
- MCP clients are programmable - they can use an API

**Paulina API:**
```
GET /v1/servers                    # List all registered servers
GET /v1/servers?tool=read_file     # Filter by tool
GET /v1/servers/{id}               # Get specific server
POST /v1/servers                   # Register server
PUT /v1/servers/{id}/refresh       # Heartbeat
DELETE /v1/servers/{id}            # Deregister
GET /v1/servers/{id}/health        # Health status
```

**Why Not DNS:**
- DNS-SD lacks rich metadata support
- DNS caching defeats health check purpose
- Added complexity for marginal benefit in single-node case

**Complexity:** Medium
**Value:** High - primary client interface

---

### A5. In-Process Registry for Single Node

**Pattern:** Registry runs embedded in the MCP orchestrator process

**Why Adopt:**
- No separate infrastructure to deploy
- Microsecond latency for local queries
- Simple startup: orchestrator starts, registry is available
- Can always extract to separate process later

**Implementation:**
```python
class SMCPOrchestrator:
    def __init__(self):
        self.registry = PaulinaRegistry()  # In-process
        self.router = MCPRouter(self.registry)

    async def start(self):
        await self.registry.start()  # Starts pruning task
        await self.router.start()    # HTTP API for clients
```

**Complexity:** Low
**Value:** High - simplicity for common case

---

## SKIP: Patterns to Avoid

### S1. Raft/Paxos Consensus

**Pattern:** Distributed consensus for strong consistency across nodes

**Why Skip:**
- Requires 3+ nodes for meaningful fault tolerance
- Adds significant operational complexity
- Single-node SMCP doesn't need consensus
- Even small clusters (2-3 nodes) can use simpler approaches

**Alternative for Small Clusters:**
- Primary/backup with leader election (simpler than Raft)
- SQLite with Litestream for replication
- Just re-register on restart (registrations are cheap)

**Complexity Saved:** Very High

---

### S2. Agent-Per-Node Architecture

**Pattern:** Consul-style agents on every node participating in gossip

**Why Skip:**
- Massive operational overhead for single-node
- Gossip protocol complexity not justified
- No benefit until 10+ nodes

**Alternative:**
- Direct API calls to central registry
- If multi-node needed later, add load balancer in front

**Complexity Saved:** High

---

### S3. Multi-Datacenter Replication

**Pattern:** WAN gossip and cross-datacenter service federation

**Why Skip:**
- SMCP target is local/single-cluster
- Adds network complexity, latency, consistency challenges
- Completely unnecessary for MCP server registry

**Complexity Saved:** Very High

---

### S4. Service Mesh / Sidecar Proxies

**Pattern:** Envoy/Consul Connect style proxies for mTLS, traffic shaping

**Why Skip:**
- MCP servers typically communicate via stdio or local HTTP
- mTLS between local processes is overkill
- Traffic shaping unnecessary for request/response MCP protocol

**Complexity Saved:** Very High

---

### S5. DNS-SD/mDNS for Discovery

**Pattern:** Zero-config discovery via multicast DNS

**Why Skip:**
- Limited to single subnet (no cross-network)
- Poor metadata support (TXT records are clunky)
- No built-in health checking integration
- Security concerns (no authentication)

**Exception:** Could be useful for "discover local MCP servers" scenario, but API-based discovery is simpler to implement correctly.

**Complexity Saved:** Medium

---

### S6. Active HTTP/TCP Health Probes

**Pattern:** Registry actively probes service health endpoints

**Why Skip:**
- MCP servers may not have HTTP endpoints (stdio transport)
- Requires opening ports, firewall considerations
- TTL heartbeats achieve same goal more simply

**Exception:** For HTTP/SSE transport MCP servers, optional health endpoint probe could supplement TTL.

**Complexity Saved:** Medium

---

## SIMPLIFY: Patterns to Implement in Reduced Form

### P1. Health Checking → Single-Level TTL

**Full Pattern:** Multiple check types (HTTP, TCP, Script, TTL) with configurable intervals

**Simplified For SMCP:**
- TTL-only with single refresh endpoint
- Binary health state: `healthy` (recent heartbeat) or `unhealthy` (TTL expired)
- No partial health, no degraded states

```python
class ServerHealth:
    HEALTHY = "healthy"      # TTL not expired
    UNHEALTHY = "unhealthy"  # TTL expired (or never registered)
```

**Complexity Reduction:** High - one health model instead of five

---

### P2. Tags → Simple String Array

**Full Pattern:** Consul's tags with DNS filtering, anti-entropy, tag override

**Simplified For SMCP:**
- Simple string array, no special behavior
- Exact match filtering only
- No DNS integration

```python
# Registration
paulina.register(..., tags=["filesystem", "local", "v1"])

# Query
servers = paulina.find(tags=["filesystem"])  # Exact match
```

**Complexity Reduction:** Medium - no tag synchronization logic

---

### P3. Service Catalog → In-Memory Dict + Optional Persistence

**Full Pattern:** Consul's distributed catalog with anti-entropy, blocking queries

**Simplified For SMCP:**
```python
class PaulinaRegistry:
    def __init__(self, persist_path: Optional[Path] = None):
        self.servers: Dict[str, ServerRecord] = {}
        self.persist_path = persist_path

    async def register(self, server: ServerRecord):
        self.servers[server.id] = server
        if self.persist_path:
            await self._persist()

    async def _persist(self):
        # Simple JSON file, reloaded on restart
        async with aiofiles.open(self.persist_path, 'w') as f:
            await f.write(json.dumps([s.dict() for s in self.servers.values()]))
```

**Optional persistence:** Nice for surviving orchestrator restarts, but servers re-register anyway.

**Complexity Reduction:** High - no distributed state management

---

### P4. Client Discovery → Direct API Calls

**Full Pattern:** Client-side discovery with caching, load balancing, circuit breaking

**Simplified For SMCP:**
- Clients call registry API directly
- No client-side caching (registry is local, fast)
- Simple round-robin if multiple instances

```python
class MCPClient:
    async def get_server(self, name: str) -> ServerRecord:
        servers = await self.paulina.find(name=name, healthy=True)
        if not servers:
            raise NoHealthyServersError(name)
        return random.choice(servers)  # Simple load balancing
```

**Complexity Reduction:** Medium - no sophisticated client library

---

## Implementation Roadmap

### Phase 1: Minimal Viable Registry (Week 1)

1. In-memory registry with Dict storage
2. Register/Deregister/List API endpoints
3. TTL-based health with background pruner
4. Capability metadata storage

**Deliverable:** Working registry for single-node SMCP

### Phase 2: Query and Filtering (Week 2)

1. Filter by name, tags, capabilities
2. Tool-based lookup ("which server has read_file?")
3. Health-aware queries (exclude expired registrations)

**Deliverable:** Smart routing based on capabilities

### Phase 3: Persistence and Reliability (Week 3)

1. Optional JSON file persistence
2. Graceful degradation on registry restart
3. Server re-registration on reconnect

**Deliverable:** Production-ready for single-node

### Phase 4: Multi-Node Support (Future)

Only if needed:
1. Simple primary/backup with health checks
2. Load balancer in front of registry replicas
3. Consider SQLite + Litestream for simple replication

**Trigger:** When users request multi-node deployments

---

## Decision Summary

| Pattern | Decision | Rationale |
|---------|----------|-----------|
| Self-Registration | **ADOPT** | Natural fit for MCP servers |
| TTL Health | **ADOPT** | Works for all transports |
| K/V Metadata | **ADOPT** | Rich capability queries |
| API Discovery | **ADOPT** | Better than DNS for MCP |
| In-Process Registry | **ADOPT** | Simplicity for single-node |
| Raft Consensus | **SKIP** | Overkill for target scale |
| Agent Architecture | **SKIP** | Operational overhead |
| Multi-DC | **SKIP** | Not in scope |
| Service Mesh | **SKIP** | Wrong abstraction level |
| DNS-SD | **SKIP** | Poor metadata, complexity |
| Active Probes | **SKIP** | TTL sufficient |
| Complex Health | **SIMPLIFY** | Binary TTL-based |
| Tag System | **SIMPLIFY** | Simple string array |
| Catalog | **SIMPLIFY** | In-memory + optional persist |
| Client Discovery | **SIMPLIFY** | Direct API, no caching |

---

## Key Insight

The enterprise service discovery tools (Consul, etcd, Zookeeper) solve hard distributed systems problems that don't exist in SMCP's target environment:

- **They solve:** Thousands of services across datacenters with complex networking
- **SMCP has:** Tens of MCP servers on a single machine or small cluster

By explicitly choosing NOT to solve the distributed case, Paulina can be **100x simpler** while still providing the core value: "What MCP servers are available, what can they do, and are they healthy?"

---

## Sources

- [Consul Service Discovery](https://developer.hashicorp.com/consul/docs/use-case/service-discovery)
- [etcd Lease Tutorial](https://etcd.io/docs/v3.5/tutorials/how-to-create-lease/)
- [Service Discovery in Microservices](https://www.baeldung.com/cs/service-discovery-microservices)
- [Client-Side vs Server-Side Discovery](https://microservices.io/patterns/client-side-discovery.html)
- [Consul vs etcd vs Zookeeper](https://stackshare.io/stackups/consul-vs-etcd-vs-zookeeper)
- [Raft Consensus Algorithm](https://raft.github.io/)
