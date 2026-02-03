# Use Case: Network Infrastructure

## Domain Description

Network infrastructure graphs model the topology and dependencies of IT systems,
including physical networks, cloud resources, microservices, and their
interconnections. Use cases include impact analysis, root cause detection,
capacity planning, and configuration management.

## Requirements Analysis

### Graph Model Requirements

| Aspect | Requirement | Rationale |
|--------|-------------|-----------|
| **Model Type** | Property Graph | Rich metadata on nodes (config, status); typed edges |
| **Schema** | Semi-structured | Core types stable; vendor-specific attributes vary |
| **Hierarchy** | Multi-level | Physical -> logical -> application layers |

**Key Entity Types:**
- Physical: Servers, switches, routers, data centers
- Virtual: VMs, containers, Kubernetes pods
- Application: Services, databases, APIs, queues
- Configuration: Ports, IPs, certificates, credentials
- Connections: Network links, API calls, data flows

### Query Pattern Complexity

**Primary Patterns:**
- **Impact analysis**: "What is affected if server X fails?"
- **Root cause**: "What upstream dependencies could cause service Y to fail?"
- **Path analysis**: Network paths between two endpoints
- **Configuration drift**: Finding misconfigurations across related resources
- **Dependency depth**: How deep is the dependency tree for a service?

**Query Characteristics:**
- Depth: Variable (1-hop for direct deps, 5+ for full impact)
- Direction: Both upstream and downstream traversals
- Filtering: By resource type, status, environment
- Aggregation: Counting affected resources, grouping by type

### Scale Requirements

| Metric | Typical Range | High Scale |
|--------|---------------|------------|
| Resources (nodes) | 10K - 100K | 1M+ |
| Dependencies (edges) | 50K - 1M | 10M+ |
| Query frequency | 10 - 100 QPS | 1K+ QPS |
| Update frequency | 100 - 10K/min | 100K/min |

### Processing Mode

- **Real-time**: Incident impact analysis (< 1s)
- **Near-real-time**: Topology updates from discovery (< 1min lag)
- **Batch**: Full topology reconciliation, analytics

### Integration Requirements

- CMDB/asset management systems
- Monitoring tools (Prometheus, Datadog, Nagios)
- Cloud provider APIs (AWS, GCP, Azure)
- Container orchestration (Kubernetes API)
- Incident management (PagerDuty, ServiceNow)
- IaC tools (Terraform, Ansible) for configuration

## Library Evaluation

### neo4j (Official Driver)

**Strengths:**
- Excellent for dependency traversal queries
- Cypher's variable-length paths perfect for impact analysis
- Good visualization integration for operations teams
- APOC procedures for graph algorithms

**Limitations:**
- Schema flexibility can lead to inconsistency
- Need careful index strategy for large topologies
- Single-node architecture limits write scale

**Fit Score: 9/10**

### python-arango

**Strengths:**
- Multi-model stores rich configuration documents
- Good for combining graph with document queries
- Horizontal scaling for large infrastructures
- Cost-effective for moderate scale

**Limitations:**
- AQL traversal syntax less intuitive than Cypher
- Fewer infrastructure-specific examples
- Smaller operations/SRE community

**Fit Score: 7/10**

### pyTigerGraph

**Strengths:**
- Scales well for very large infrastructures
- Good for cross-region federated topologies
- GSQL handles complex impact queries

**Limitations:**
- Overkill for most infrastructure use cases
- Enterprise licensing costs
- Steeper learning curve

**Fit Score: 6/10** (typical); **8/10** (very large scale)

### gremlinpython (with Neptune/JanusGraph)

**Strengths:**
- Cloud-native options integrate with cloud monitoring
- Standard traversal language
- Good for multi-cloud environments

**Limitations:**
- Verbose for operational queries
- Debugging traversals challenging during incidents
- Variable performance

**Fit Score: 6/10**

### NetworkX

**Strengths:**
- Excellent for topology analysis algorithms
- Easy integration with Python operations tools
- Good for offline planning and analysis

**Limitations:**
- In-memory only
- Cannot handle real-time incident queries
- No persistence

**Fit Score: 5/10** (analysis only)

## Gaps and Workarounds

| Gap | Impact | Workaround |
|-----|--------|------------|
| Real-time topology updates | Discovery lag during changes | Event-driven updates, eventual consistency |
| Multi-layer correlation | Physical-logical-app mapping complex | Typed edges, layer property on nodes |
| Historical topology | Need point-in-time topology | Temporal properties, snapshot graphs |
| Dynamic environments | Kubernetes pods ephemeral | Aggregate by service, not pod |
| Cross-system correlation | Multiple source systems | Canonical ID mapping layer |

## Architecture Pattern

```
[Discovery Sources]
   |-- Cloud APIs
   |-- K8s API
   |-- CMDB
   |-- Network monitoring
        |
        v
[Topology Aggregator] -- canonical model --> [Graph Database]
        |                                           |
        v                                           v
[Change Event Stream]                        [Query API]
        |                                           |
        v                                           v
[Alert Enrichment]                           [Dashboard/CLI]
```

**Operational Queries:**

```cypher
// Impact analysis: What services are affected if this server fails?
MATCH (server:Server {id: $serverId})<-[:RUNS_ON*1..3]-(service:Service)
RETURN service.name, service.criticality

// Root cause: What could cause this API to fail?
MATCH path = (api:API {name: $apiName})-[:DEPENDS_ON*1..5]->(dep)
WHERE dep.status = 'unhealthy'
RETURN path

// Dependency depth
MATCH path = (service:Service {name: $svc})-[:DEPENDS_ON*]->(dep)
RETURN max(length(path)) as maxDepth
```

## Operational Considerations

| Consideration | Approach |
|---------------|----------|
| **Incident response** | Pre-computed impact sets for critical services |
| **Discovery frequency** | Balance freshness vs database load |
| **Schema evolution** | Version type hierarchies, migration scripts |
| **Access control** | Environment-based graph partitioning |
| **Audit trail** | Change log for topology modifications |

## Recommendation

**Best Fit: neo4j official driver**

For network infrastructure and dependency mapping, Neo4j's Cypher language
provides the most natural expression of dependency queries. The ability to
write variable-length path queries (`-[:DEPENDS_ON*1..5]->`) makes impact
analysis and root cause queries intuitive.

**Key advantages for operations:**
- Fast time-to-value with intuitive query language
- Bloom visualization for non-technical stakeholders
- Active operations/SRE community with examples

**Alternative: python-arango** when infrastructure includes complex
configuration documents that benefit from document storage alongside
graph relationships.

**Complement with NetworkX** for offline topology analysis, capacity
planning, and what-if simulations that don't need real-time data.
