# JanusGraph (Open Source, Gremlin)

**Provider:** Linux Foundation (Apache project)
**Founded:** 2017 (7+ years, forked from TitanDB)
**Query Language:** Gremlin (Apache TinkerPop)
**Deployment:** Self-hosted only (open source)
**Market Position:** Leading open-source graph database

---

## Overview

JanusGraph is an **open-source, distributed graph database** using Gremlin query language (Apache TinkerPop standard). Originally forked from TitanDB (2017), JanusGraph is now a Linux Foundation project with contributions from IBM, Google, and Hortonworks. Designed for massive scale (billions of nodes, trillions of edges) with pluggable storage backends (Cassandra, HBase, Berkeley DB).

**Strengths:**
- ✅ Fully open source (Apache 2.0 license, no vendor lock-in)
- ✅ Gremlin standard (high portability)
- ✅ Massive scalability (billions of nodes proven at scale)
- ✅ Pluggable backends (Cassandra, HBase, Berkeley DB)
- ✅ No licensing costs (100% free forever)
- ✅ Elasticsearch/Solr integration (full-text search, geo queries)

**Weaknesses:**
- ❌ No managed service (self-host only, complex ops)
- ❌ Limited graph algorithms (must build custom)
- ❌ Complex setup (requires Cassandra/HBase + Elasticsearch clusters)
- ❌ Slower development (community-driven, slower releases)
- ❌ Smaller community than Neo4j

---

## Pricing

### Self-Hosted (Only Option)

**License:** Apache 2.0 (100% free, no restrictions)

**Infrastructure Cost:**

**Small Graph (100K nodes, 500K edges):**
- JanusGraph: 1 node (2 vCPU, 8GB RAM) = $50/month
- Cassandra: 1 node (2 vCPU, 8GB RAM) = $50/month
- Elasticsearch (optional): 1 node (2 vCPU, 8GB RAM) = $50/month
- **Total: $100-150/month** (JanusGraph + Cassandra, skip Elasticsearch if no full-text search)

**Medium Graph (1M nodes, 5M edges):**
- JanusGraph: 1-2 nodes (4 vCPU, 16GB RAM each) = $100-200/month
- Cassandra: 3 nodes (4 vCPU, 16GB RAM each) = $300/month (recommended RF=3)
- Elasticsearch (optional): 3 nodes = $300/month
- **Total: $400-800/month**

**Large Graph (100M+ nodes, 1B+ edges):**
- JanusGraph: 5-10 nodes = $500-1,000/month
- Cassandra: 10-20 nodes = $1,000-2,000/month
- Elasticsearch: 5-10 nodes = $500-1,000/month
- **Total: $2,000-4,000/month** (but handles massive scale)

**Key Insight:**
- JanusGraph economical at **large scale** (>10M nodes)
- Expensive for small graphs (<1M nodes) due to multi-cluster complexity
- Break-even vs managed services: >5M nodes

---

## Query Language: Gremlin

**Syntax Example:**
```gremlin
// Find research items that complement 3.041 and their dependencies
g.V().has('Research', 'code', '3.041')
  .both('COMPLEMENTS')
  .as('related')
  .repeat(out('UPSTREAM_FROM')).times(3)
  .as('dependency')
  .select('related', 'dependency')
  .by(valueMap())
```

**Portability:**
- ✅ **High** (Apache TinkerPop standard)
- ✅ Compatible with: Amazon Neptune (Gremlin), Azure Cosmos DB (Gremlin API)
- ✅ Migration path: JanusGraph ↔ Neptune ↔ Cosmos DB (low effort)

**vs Cypher:**
- Gremlin: Functional style, more verbose
- Cypher: ASCII art style, more readable
- **Portability:** Gremlin higher (Apache standard)

---

## Graph Algorithms

**Built-In:** ❌ None

JanusGraph **does not include graph algorithms** (no PageRank, Louvain, centrality, etc.).

**Workarounds:**

**Option 1: Apache TinkerPop GLVs (Graph Language Variants)**
- Write custom algorithms in Python, Java, .NET
- Use TinkerPop traversal API
- **Complexity:** High (implement from scratch)

**Option 2: Export + NetworkX/igraph**
- Export subgraph to Python
- Run algorithms in NetworkX or igraph
- Import results back
- **Cost:** Minimal (compute time)
- **Complexity:** Medium (ETL pipeline)

**Option 3: Gremlin recipes (community patterns)**
- GitHub has community Gremlin recipes for common algorithms
- Copy-paste Gremlin traversals for PageRank, centrality, etc.
- **Quality:** Variable (not production-tested)

**Comparison:**
- Neo4j GDS: 60+ algorithms built-in
- Memgraph MAGE: 30+ algorithms built-in
- JanusGraph: 0 algorithms, DIY required

---

## Performance

**Benchmark Context:**
- 1M nodes, 5M relationships
- Backend: Cassandra 3-node cluster

**Latency:**
- **Simple read (1 hop):** 5-20ms (backend-dependent)
- **Medium traversal (2-3 hops):** 50-200ms
- **Complex traversal (4-6 hops):** 200-1,000ms

**Throughput:**
- **Reads:** 500-2,000 queries/second (cluster-dependent)
- **Writes:** 1,000-10,000 writes/second (Cassandra write-optimized)

**Scaling:**
- **Horizontal:** Add JanusGraph nodes (stateless, easy)
- **Backend scaling:** Add Cassandra/HBase nodes (proven to petabyte scale)

**Performance Characteristics:**
- Write-heavy: Excellent (Cassandra backend optimized for writes)
- Read-heavy: Good (but slower than in-memory like Memgraph)
- Mixed workload: Good

---

## Self-Hosting

**Setup Complexity:** High (multi-cluster deployment)

**Components Required:**
1. **JanusGraph server(s):** Query processing
2. **Storage backend:** Cassandra, HBase, or Berkeley DB
3. **Index backend (optional):** Elasticsearch or Solr

**Docker Compose Example:**
```yaml
version: '3'
services:
  janusgraph:
    image: janusgraph/janusgraph:latest
    ports:
      - "8182:8182"  # Gremlin Server
    environment:
      JANUS_PROPS_TEMPLATE: cassandra-es
      janusgraph.storage.backend: cql
      janusgraph.storage.hostname: cassandra
      janusgraph.index.search.backend: elasticsearch
      janusgraph.index.search.hostname: elasticsearch

  cassandra:
    image: cassandra:4.0
    ports:
      - "9042:9042"
    volumes:
      - ./cassandra-data:/var/lib/cassandra

  elasticsearch:
    image: elasticsearch:7.17.0
    ports:
      - "9200:9200"
    environment:
      discovery.type: single-node
```

**Operations:**
- **Backups:** Cassandra snapshots + JanusGraph schema export
- **Monitoring:** JMX metrics, Prometheus exporters
- **Updates:** Coordinated updates (JanusGraph → Cassandra → Elasticsearch)
- **Complexity:** High (3 systems to manage)

**When JanusGraph Makes Sense:**
- ✅ Massive scale (>10M nodes, >100M edges)
- ✅ Write-heavy workloads (Cassandra backend)
- ✅ Full-text search critical (Elasticsearch integration)
- ✅ Zero vendor lock-in required (Apache license)
- ❌ Small scale (<1M nodes): Too complex, use Neo4j/Memgraph instead

---

## Lock-In Assessment

**Lock-In Level:** Lowest

**Low Lock-In Factors:**
- ✅ Open source (Apache 2.0, forkable)
- ✅ Gremlin standard (portable to Neptune, Cosmos DB)
- ✅ No vendor (community-driven)
- ✅ Pluggable backends (switch Cassandra → HBase → Berkeley DB)

**Migration Complexity:**

**JanusGraph → Amazon Neptune (Gremlin):**
- **Effort:** Low (1-2 weeks)
- **Data export:** Gremlin scripts or bulk export
- **Query compatibility:** High (both use Apache TinkerPop)
- **Benefit:** Eliminate ops burden (managed service)

**JanusGraph → Neo4j:**
- **Effort:** High (2-3 months)
- **Data export:** CSV export → Neo4j import
- **Query rewrite:** Gremlin → Cypher (complete rewrite)

**Mitigation:**
- Already lowest lock-in (open source, Apache standard)

---

## Use Case Fit: Knowledge Graph for Research Project

**Scenario:**
- 100-500 nodes (research items, technologies, providers)
- 500-5,000 relationships (complements, upstream_from, references)
- Queries: Dependency traversal, community detection, centrality

**Recommended:** ❌ Not recommended (overkill)

**Why:**
- ❌ **Too complex for small scale:** Requires Cassandra + Elasticsearch clusters
  - Operational overhead: 3 systems to manage (JanusGraph + Cassandra + Elasticsearch)
  - Setup time: 1-2 days (vs 10 minutes for Neo4j/Memgraph)
- ❌ **No graph algorithms:** Must implement PageRank, Louvain, centrality manually
- ❌ **Higher cost:** $100-150/month (vs $25-100 for Neo4j/Memgraph)
- ❌ **Slower for small graphs:** 5-20ms latency (vs <1ms for Memgraph)

**When JanusGraph Makes Sense:**
- ✅ Massive scale (>10M nodes, proven to billions)
- ✅ Write-heavy (Cassandra optimized for high-throughput writes)
- ✅ Full-text search critical (Elasticsearch integration)
- ✅ Zero lock-in required (Apache open source)

**Better Alternatives for Research Project:**
1. **Memgraph Community:** $25-50/month, MAGE algorithms, 10× faster
2. **Neo4j Community:** $50-100/month, GDS algorithms, best ecosystem
3. **Dgraph:** $50-100/month, GraphQL-native, simpler than JanusGraph

---

## Vendor Viability

**Financial Stability:**
- Linux Foundation project (no vendor risk)
- Contributions from IBM, Google, Hortonworks, Expero
- Community-driven (no single vendor dependency)

**Market Position:**
- Leading open-source graph database
- Used by: IBM, Uber, Netflix (historically), FTC

**10-Year Outlook:**
- **Probability of existence:** 90%+
- **Risk:** Low (open source, community-driven)
- **Acquisition potential:** N/A (not a company)

**Maintenance Risk:**
- Medium (slower development, community-driven)
- Releases: 1-2 per year (vs quarterly for Neo4j, Memgraph)
- Active contributors: 50-100 (smaller than Neo4j)

---

## Summary

**Best For:**
- Massive-scale graphs (billions of nodes, trillions of edges)
- Write-heavy workloads (Cassandra backend optimized)
- Zero vendor lock-in (Apache open source)
- Organizations with strong ops teams (can manage multi-cluster)

**Avoid If:**
- Small/medium graphs (<10M nodes) - too complex
- Need graph algorithms (must build custom)
- Limited ops resources (3 systems to manage)
- Prefer managed services (no JanusGraph managed option)

**Recommended For Research Project Use Case:**
❌ **No** (overkill, no algorithms, complex ops)

**Reasoning:**
- 500 nodes too small for JanusGraph (designed for millions/billions)
- Requires Cassandra + Elasticsearch setup (operational complexity)
- No built-in algorithms (PageRank, Louvain, centrality must be DIY)
- Higher cost ($100-150/month) than simpler alternatives ($25-100)
- Memgraph or Neo4j Community better fit (simpler, cheaper, algorithms included)
