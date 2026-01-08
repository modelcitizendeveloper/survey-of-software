# Service Discovery Pattern Catalog

**Experiment**: 2.082 Service Discovery Patterns
**Purpose**: Extract patterns from Consul, etcd, DNS-SD for lightweight MCP registry (Paulina)
**Date**: 2026-01-08

---

## 1. Service Registration Patterns

### 1.1 Push-Based Registration (Self-Registration)

Services announce themselves to a central registry upon startup.

**How it works:**
1. Service starts and gathers its metadata (address, port, capabilities)
2. Service sends registration request to registry
3. Registry stores the service record
4. Service maintains registration through heartbeats/lease renewal

**Implementations:**
- **Consul**: Agent-based registration via config files or HTTP API (`PUT /agent/service/register`)
- **etcd**: Key-value write with lease attachment (`etcdctl put --lease=<id> /services/foo`)
- **DNS-SD**: mDNS multicast announcements (proactive, periodic)

**Consul Example:**
```json
{
  "service": {
    "name": "mcp-server-filesystem",
    "port": 8080,
    "tags": ["mcp", "v1.0"],
    "meta": {
      "protocol": "stdio",
      "tools": "read_file,write_file,list_dir"
    }
  }
}
```

**etcd Example:**
```bash
# Grant lease (TTL=30s)
etcdctl lease grant 30
# Register with lease
etcdctl put --lease=<lease_id> /services/mcp/filesystem '{"addr":"localhost:8080"}'
```

**Pros:**
- Services control their own registration
- Simple mental model - "I exist, let me announce it"
- Natural fit for ephemeral/dynamic services

**Cons:**
- Requires registration logic in every service
- Services must handle registration failures gracefully

---

### 1.2 Pull-Based Registration (Third-Party Registration)

An external registrar monitors services and registers them.

**How it works:**
1. Registrar watches for new service instances (via orchestrator, file system, etc.)
2. Registrar probes service health
3. Registrar adds/removes entries from registry based on discovered state

**Implementations:**
- **Consul ESM**: External Service Monitor for services outside the agent mesh
- **Kubernetes + CoreDNS**: kubelet/controller registers pods, CoreDNS watches API
- **Sidekick Pattern**: External process monitors service and updates registry

**Pros:**
- Services don't need registration logic
- Centralized registration policy
- Works for legacy services that can't self-register

**Cons:**
- Additional infrastructure component
- Polling delay between state change and registration update
- Registrar becomes a dependency

---

### 1.3 Agent-Based Registration (Consul Model)

Local agents run alongside services, handling registration and health checks.

**How it works:**
1. Agent runs on each node
2. Services register with local agent
3. Agent handles health checking and gossip protocol
4. Server nodes aggregate data into service catalog

**Key Insight (Consul's Push Model):**
> "Consul uses a push-based model where agents send events only upon status changes.
> As such, even large clusters will have very few requests."

**Pros:**
- Distributes health check load
- Local agent provides caching and resilience
- No central bottleneck for health checks

**Cons:**
- Agent per node = operational overhead
- Overkill for single-node deployments

---

## 2. Health Check Patterns

### 2.1 TTL (Time-to-Live) Checks

Services must actively "heartbeat" to maintain registration.

**How it works:**
1. Service registers with TTL (e.g., 30 seconds)
2. Service periodically calls health endpoint before TTL expires
3. If TTL expires without update, service marked unhealthy/removed

**Implementations:**
- **Consul TTL**: `PUT /agent/check/pass/:check_id` before timeout
- **etcd Lease**: `LeaseKeepAlive` RPC stream, keys deleted on lease expiry

**etcd Lease Pattern:**
```python
# Python example with etcd3
lease = client.lease(ttl=30)
client.put('/services/mcp/foo', 'data', lease=lease)
# Must call lease.refresh() periodically
```

**Pros:**
- Simple to implement
- Service controls its own liveness signal
- Works across network boundaries (no inbound connections needed)

**Cons:**
- Silent failures possible (service dead but TTL not expired)
- Chatty - constant heartbeat traffic
- TTL tuning is tricky (too short = false positives, too long = stale data)

**Best For:** Services behind firewalls, services that can't accept incoming health probes

---

### 2.2 Active Health Probes (HTTP/TCP/Script)

Registry or agent actively checks service health.

**Types:**
| Type | How It Works | Example |
|------|--------------|---------|
| **HTTP** | GET request, expect 2xx response | `http://localhost:8080/health` |
| **TCP** | Establish TCP connection | Connect to port 8080 |
| **Script** | Run command, check exit code | `/scripts/check-mcp.sh` |
| **gRPC** | gRPC health check protocol | `grpc.health.v1.Health/Check` |

**Consul HTTP Check:**
```json
{
  "check": {
    "http": "http://localhost:8080/health",
    "interval": "10s",
    "timeout": "1s"
  }
}
```

**Pros:**
- Verifies actual service health, not just liveness
- Can check deep health (database connections, dependencies)
- Immediate detection of failures

**Cons:**
- Requires services to expose health endpoint
- Inbound network access needed
- Scaling concern: N services × M checks = N×M requests

**Best For:** Services that can expose health endpoints, trusted networks

---

### 2.3 Gossip-Based Health (Consul SWIM)

Nodes participate in peer-to-peer gossip to detect failures.

**How it works:**
1. Each node periodically probes random other nodes
2. Failed probes trigger indirect probes through other nodes
3. Consistent failure detection leads to node being marked down
4. Load is O(1) per node regardless of cluster size

**Key Insight:**
> "The problem with edge triggered monitoring is that there are no liveness heartbeats.
> Consul gets around this by using a gossip-based failure detector."

**Pros:**
- Scales to thousands of nodes
- No central bottleneck
- Resistant to network partitions

**Cons:**
- Complexity
- Not applicable to single-node setups
- Eventual consistency (detection delay)

**Best For:** Large distributed clusters

---

## 3. Service Discovery Patterns

### 3.1 DNS-Based Discovery

Services discovered via DNS queries.

**Implementations:**
- **DNS-SD (RFC 6763)**: `_service._tcp.local` PTR records
- **Consul DNS**: `service.consul` domain queries
- **CoreDNS + Kubernetes**: `service.namespace.svc.cluster.local`

**DNS-SD Query Flow:**
```
1. Query: _mcp-server._tcp.local PTR ?
2. Response: filesystem._mcp-server._tcp.local
3. Query: filesystem._mcp-server._tcp.local SRV ?
4. Response: 0 0 8080 host.local
5. Query: filesystem._mcp-server._tcp.local TXT ?
6. Response: "protocol=stdio" "tools=read_file,write_file"
```

**Pros:**
- Universal - every language/platform has DNS client
- Caching built into DNS
- Works with existing infrastructure

**Cons:**
- Limited metadata in TXT records
- Caching can cause stale data
- No built-in health integration

**Best For:** Broad compatibility, existing DNS infrastructure

---

### 3.2 API-Based Discovery

Direct registry queries via HTTP/gRPC.

**Implementations:**
- **Consul HTTP API**: `GET /v1/catalog/service/:service`
- **etcd API**: `GET /v3/kv/range` with prefix
- **Kubernetes API**: Watch endpoints

**Consul Catalog Query:**
```bash
curl http://localhost:8500/v1/catalog/service/mcp-server
# Returns: [{ServiceID, ServiceName, ServiceAddress, ServicePort, ServiceMeta, ...}]
```

**Pros:**
- Rich metadata support
- Real-time watches/subscriptions
- Fine-grained filtering (tags, metadata)

**Cons:**
- Registry becomes critical path
- Client library needed
- More complex than DNS

**Best For:** Rich service metadata, real-time updates, complex queries

---

### 3.3 Client-Side Discovery

Clients query registry and choose target instance.

**Flow:**
1. Client queries registry for service endpoints
2. Client receives list of healthy instances
3. Client applies load balancing logic (round-robin, weighted, etc.)
4. Client connects directly to chosen instance

**Examples:** Netflix Ribbon, gRPC name resolution, Go resolver

**Pros:**
- No intermediate proxy
- Client can make smart routing decisions
- Lower latency (direct connection)

**Cons:**
- Discovery logic duplicated in every client
- Client complexity increases
- Language/framework coupling

---

### 3.4 Server-Side Discovery

Load balancer/proxy handles discovery.

**Flow:**
1. Client sends request to well-known proxy address
2. Proxy queries registry
3. Proxy routes request to healthy instance
4. Client unaware of actual service locations

**Examples:** AWS ELB, NGINX, Envoy, Kubernetes kube-proxy

**Pros:**
- Simple clients
- Centralized routing policy
- Works with any client language

**Cons:**
- Additional network hop
- Proxy becomes potential bottleneck/SPOF
- More infrastructure to manage

---

## 4. Metadata and Tagging Patterns

### 4.1 Flat Tags (Consul Style)

Simple string array attached to services.

```json
{
  "tags": ["mcp", "v1.0", "stdio", "production"]
}
```

**Filtering:** Single tag match via DNS or API
```
# DNS: tag.service.consul
mcp.mcp-server.service.consul

# API: ?tag=mcp
/v1/catalog/service/mcp-server?tag=mcp
```

**Pros:** Simple, fast filtering
**Cons:** No structure, limited expressiveness

---

### 4.2 Key-Value Metadata (Consul Meta)

Structured metadata as key-value pairs.

```json
{
  "meta": {
    "version": "1.0.0",
    "protocol": "stdio",
    "tools": "read_file,write_file,list_dir",
    "resources": "file://*",
    "capabilities": "sampling,logging"
  }
}
```

**Filtering:** Expression-based filtering via API
```
/v1/catalog/service/mcp-server?filter=ServiceMeta.protocol=="stdio"
```

**Pros:** Structured, queryable, extensible
**Cons:** More complex queries, potential for inconsistent schemas

---

### 4.3 JSON Payload (etcd Style)

Full JSON document as value.

```bash
etcdctl put /services/mcp/filesystem '{
  "name": "filesystem",
  "version": "1.0.0",
  "endpoint": "stdio:///usr/local/bin/mcp-filesystem",
  "capabilities": {
    "tools": ["read_file", "write_file", "list_dir"],
    "resources": ["file://*"],
    "sampling": true
  }
}'
```

**Pros:** Maximum flexibility, complex nested structures
**Cons:** No built-in querying (client must parse), schema enforcement needed

---

## 5. Consensus and Consistency Patterns

### 5.1 Raft Consensus

Leader-based consensus for strong consistency.

**Used by:** etcd, Consul

**Key Properties:**
- Single leader handles all writes
- Followers replicate log entries
- Majority quorum required for commits
- Leader election on failure

**Trade-offs:**
- Strong consistency (linearizable reads available)
- Write throughput limited by leader
- Cluster size typically 3, 5, or 7 nodes

---

### 5.2 Gossip Protocol (Consul SWIM)

Peer-to-peer protocol for membership and failure detection.

**Key Properties:**
- O(1) message complexity per node
- Eventually consistent membership
- Handles network partitions gracefully

**Trade-offs:**
- Fast membership updates
- Eventual consistency (seconds of delay)
- Complements but doesn't replace strong consistency for data

---

### 5.3 Single-Node Mode

No consensus needed - direct in-memory or file storage.

**When Applicable:**
- Development/testing
- Single-node deployments
- Non-critical services

**Trade-offs:**
- Simplest implementation
- No fault tolerance
- Sufficient for many use cases

---

## 6. Summary: Pattern Selection Matrix

| Pattern | Complexity | Scale | Consistency | Best For |
|---------|------------|-------|-------------|----------|
| Self-Registration + TTL | Low | Small-Medium | Eventual | MCP servers (self-contained) |
| Agent-Based | High | Large | Strong | Enterprise service mesh |
| DNS-SD | Low | Small | Eventual | Local network, zero-config |
| API Discovery | Medium | Any | Configurable | Rich metadata, filtering |
| Client-Side Discovery | Medium | Medium-Large | N/A | Direct connections |
| Server-Side Discovery | Medium | Any | N/A | Simple clients, proxy infra |
| Raft Consensus | High | 3-7 nodes | Strong | Distributed clusters |
| Single-Node | Lowest | 1 node | N/A | Development, simple deploys |

---

## Sources

- [Consul Service Registration](https://developer.hashicorp.com/consul/docs/register/service/vm)
- [Consul Health Checks](https://developer.hashicorp.com/consul/docs/register/health-check/vm)
- [Consul Service Discovery](https://developer.hashicorp.com/consul/docs/use-case/service-discovery)
- [etcd Leases Tutorial](https://etcd.io/docs/v3.5/tutorials/how-to-create-lease/)
- [etcd Service Discovery](https://www.pixelstech.net/article/1615108646-Service-discovery-with-etcd)
- [DNS-SD RFC 6763](https://datatracker.ietf.org/doc/html/rfc6763)
- [mDNS and DNS-SD](https://dn.org/mdns-and-dns-sd-service-discovery-in-local-networks/)
- [CoreDNS Kubernetes](https://kubernetes.io/docs/tasks/administer-cluster/coredns/)
- [Client vs Server-Side Discovery](https://microservices.io/patterns/client-side-discovery.html)
- [Consul vs etcd vs Zookeeper](https://ahmettsoner.medium.com/advanced-service-discovery-in-microservices-consul-etcd-and-zookeeper-b8860dce8363)
