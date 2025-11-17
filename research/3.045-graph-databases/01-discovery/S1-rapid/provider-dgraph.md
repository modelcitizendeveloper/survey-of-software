# Dgraph (GraphQL-Native)

**Provider:** Dgraph Labs
**Founded:** 2015 (9+ years)
**Query Language:** GraphQL, DQL (Dgraph Query Language)
**Deployment:** Managed cloud (Dgraph Cloud), self-hosted (open source)
**Market Position:** GraphQL-native graph database

---

## Overview

Dgraph is a **GraphQL-native graph database** designed for modern API-first applications. Uses GraphQL as primary query interface (familiar to frontend developers), with proprietary DQL for advanced queries. Written in Go, distributed architecture, horizontally scalable. Open source (Apache 2.0) with managed cloud offering.

**Strengths:**
- ✅ GraphQL-native (best DX for frontend developers)
- ✅ Open source (Apache 2.0, low lock-in)
- ✅ Distributed by design (horizontal scaling)
- ✅ Fast (Go implementation, good performance)
- ✅ Free self-hosting (Docker, Kubernetes)
- ✅ Affordable managed ($0-50/month for small graphs)

**Weaknesses:**
- ❌ No graph algorithms (must build custom)
- ❌ Smaller ecosystem (fewer integrations, tutorials)
- ❌ DQL proprietary (GraphQL is standard, but DQL is not)
- ❌ Less mature (newer than Neo4j, JanusGraph)

---

## Pricing

### Dgraph Cloud (Managed)

**Free Tier (Shared):**
- 1GB storage, shared infrastructure
- Suitable for: Development, prototypes (<10K nodes)
- **Cost:** $0/month (permanent free tier)

**Dedicated Instances:**
- 5GB storage, 1 vCPU, 2GB RAM: $10/month
- 25GB storage, 2 vCPU, 8GB RAM: $50/month
- 100GB storage, 4 vCPU, 16GB RAM: $200/month
- Custom: $500-2,000+/month

### Self-Hosted (Open Source)

**License:** Apache 2.0 (100% free)

**Infrastructure Cost:**

**Small Graph (500 nodes, 5K edges):**
- Single node: 2 vCPU, 4GB RAM = $25/month
- **Total: $25/month**

**Medium Graph (100K nodes, 1M edges):**
- 3 nodes (Alpha, Zero, Ratel): 4 vCPU, 8GB RAM each = $75/month
- **Total: $75-150/month**

**Large Graph (10M+ nodes):**
- 6+ nodes: $300-1,000+/month

---

## Query Language: GraphQL + DQL

### GraphQL (Primary Interface)

**Syntax Example:**
```graphql
query {
  getResearch(code: "3.041") {
    code
    title
    complements {
      code
      title
      upstreamFrom(depth: 3) {
        code
      }
    }
  }
}
```

**Characteristics:**
- **Syntax:** GraphQL standard (widely adopted)
- **Readability:** Excellent (declarative, JSON-like)
- **Portability:** ✅ High (GraphQL is universal)
- **Learning curve:** Low (frontend developers know GraphQL)

**Benefit:**
- No backend code needed (GraphQL schema → automatic CRUD API)
- Frontend-friendly (same language for API and database)

---

### DQL (Dgraph Query Language)

**For Advanced Queries:**
```dql
{
  item(func: eq(code, "3.041")) {
    code
    title
    complements {
      code
      title
      upstreamFrom @recurse(depth: 3) {
        code
      }
    }
  }
}
```

**Characteristics:**
- **Syntax:** JSON-like, Dgraph-specific
- **Portability:** ❌ Low (Dgraph-specific)
- **Use case:** Complex queries beyond GraphQL capabilities

---

## Graph Algorithms

**Built-In:** ❌ None

Dgraph **does not include graph algorithms** (no PageRank, Louvain, centrality).

**Workarounds:**
- Export to Python (NetworkX, igraph)
- Implement custom algorithms in Go
- Use external graph analytics tools

**Impact:**
- ❌ Not suitable for algorithm-heavy workloads
- ✅ Suitable for traversal + CRUD (API-first apps)

---

## Performance

**Latency:**
- Simple read (1 hop): 1-5ms
- Medium traversal (2-3 hops): 10-50ms
- Complex traversal (4-6 hops): 50-200ms

**Throughput:**
- Reads: 2,000-10,000 queries/second (cluster)
- Writes: 1,000-5,000 writes/second

**Scaling:**
- Horizontal scaling (add Alpha nodes)
- Proven to billions of edges

---

## Lock-In Assessment

**Lock-In Level:** Low-Medium

**Low Lock-In Factors:**
- ✅ Open source (Apache 2.0, forkable)
- ✅ GraphQL standard (portable concepts)
- ✅ Self-host option (free forever)

**Medium Lock-In Factors:**
- ⚠️ DQL proprietary (advanced queries)
- ⚠️ Schema design (Dgraph-specific patterns)

**Migration Complexity:**
- **Dgraph → Any graph DB:** Medium-High (1-2 months)
- GraphQL → Cypher/Gremlin translation required
- DQL → complete rewrite

---

## Use Case Fit: Knowledge Graph for Research Project

**Recommended:** ⚠️ Maybe (if GraphQL API desired)

**Pros:**
- ✅ Affordable ($0-50/month managed or $25 self-hosted)
- ✅ Low lock-in (open source, Apache 2.0)
- ✅ GraphQL-native (if building API for research project)

**Cons:**
- ❌ No graph algorithms (PageRank, Louvain, centrality)
- ⚠️ Smaller ecosystem (fewer tutorials, integrations)

**Better if:**
- Building GraphQL API on top of knowledge graph
- Want open source + low lock-in
- Don't need graph algorithms

**Worse than:**
- Neo4j Community: More algorithms, better ecosystem
- Memgraph Community: MAGE algorithms, faster

---

## Vendor Viability

**Financial Stability:**
- Private company, VC-backed
- $11.5M Series A (2019)
- Growing but smaller than Neo4j, Memgraph

**10-Year Outlook:**
- Probability: 75-85%
- Risk: Medium (smaller company, competitive market)
- Acquisition potential: High

**Mitigation:**
- Open source (Apache 2.0, forkable)
- Self-hosting option (no vendor dependency)

---

## Summary

**Best For:**
- GraphQL-first applications (API-driven)
- Frontend developers (GraphQL familiarity)
- Open source preference (Apache 2.0)
- Budget-conscious ($0-50/month)

**Avoid If:**
- Need graph algorithms (PageRank, community detection)
- Prefer mature ecosystem (Neo4j larger)
- Need Cypher/Gremlin (Dgraph uses GraphQL/DQL)

**Recommended For Research Project:**
⚠️ **Maybe** ($0-50/month, low lock-in, but no algorithms)

**Use if:** Building GraphQL API for research project metadata
**Avoid if:** Need graph algorithms (use Neo4j/Memgraph instead)
