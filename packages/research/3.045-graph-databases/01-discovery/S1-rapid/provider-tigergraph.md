# TigerGraph (Enterprise Analytics)

**Provider:** TigerGraph Inc.
**Founded:** 2012 (12+ years)
**Query Language:** GSQL (TigerGraph's proprietary language)
**Deployment:** Managed cloud (TigerGraph Cloud), self-hosted (Enterprise license)
**Market Position:** Enterprise graph analytics leader

---

## Overview

TigerGraph is an **enterprise-focused graph analytics platform** with proprietary GSQL query language. Targets large enterprises with massive-scale graph analytics (fraud detection, supply chain, cybersecurity). Known for real-time deep-link analytics (20+ hops) and high-performance parallel processing.

**Strengths:**
- ✅ Massive scale (distributed, proven to 100B+ edges)
- ✅ Real-time deep-link analytics (20+ hops in seconds)
- ✅ Built-in graph algorithms (30+ algorithms)
- ✅ Parallel query execution (MPP architecture)
- ✅ Visual query builder (GraphStudio)

**Weaknesses:**
- ❌ Expensive ($99-2,000+/month, enterprise licensing)
- ❌ Proprietary GSQL (highest lock-in)
- ❌ Enterprise-only (no Community Edition)
- ❌ Complex licensing (node limits, connector costs)
- ❌ Smaller ecosystem (less adoption than Neo4j)

---

## Pricing

### TigerGraph Cloud (Managed)

**Free Tier:**
- 10GB storage, 2 vCPU, 8GB RAM
- 90 days trial (then expires)
- **Cost:** $0 (trial only, not permanent)

**Developer Tier:**
- 50GB storage, 4 vCPU, 16GB RAM
- Suitable for: 100K-500K nodes, 1M-5M edges
- **Cost:** $99/month

**Professional Tier:**
- 200GB storage, 8 vCPU, 32GB RAM
- Suitable for: 1M-5M nodes, 10M-50M edges
- **Cost:** $499/month

**Enterprise Tier:**
- Custom sizing, clustering, multi-region
- **Cost:** $2,000-10,000+/month (contact sales)

### Self-Hosted (Enterprise License Required)

**Enterprise Edition:**
- License: $50K-500K+/year (negotiated, based on cores/nodes)
- Infrastructure: $500-5,000+/month (multi-node cluster)
- **Total:** $5K-50K+/month (all-in cost)

**No Free/Community Edition** (unlike Neo4j, Memgraph, JanusGraph)

---

## Query Language: GSQL

**Syntax Example:**
```gsql
// Find research items that complement 3.041 and their dependencies
CREATE QUERY find_complements_and_deps() {
  Start = {Research.*};
  Item = SELECT t FROM Start:s -(COMPLEMENTS:e)- :t
         WHERE s.code == "3.041";

  Deps = SELECT t FROM Item:s -(UPSTREAM_FROM:e)- :t;

  PRINT Item, Deps;
}
```

**Characteristics:**
- **Syntax:** Procedural, SQL-inspired
- **Readability:** Medium (verbose, imperative)
- **Portability:** ❌ None (TigerGraph-specific)
- **Learning curve:** High (unique paradigm)

**Lock-In:**
- ❌ Highest lock-in (GSQL 100% proprietary)
- ❌ No equivalent in other databases
- ❌ Migration = complete rewrite

---

## Graph Algorithms

**Built-In:** 30+ algorithms (good coverage)

**Algorithm Categories:**
- **Centrality:** PageRank, Betweenness, Closeness, Degree
- **Community:** Louvain, Label Propagation, Connected Components
- **Path:** Shortest Path, All Paths, Cycle Detection
- **Similarity:** Jaccard, Cosine, K-Nearest Neighbors

**Comparison:**
- Neo4j GDS: 60+ algorithms (more comprehensive)
- TigerGraph: 30+ algorithms (good coverage)
- Memgraph MAGE: 30+ algorithms (similar)

**Performance:**
- Parallel execution (distributed across cluster)
- Fast for large graphs (100M+ nodes)

---

## Performance

**Benchmark (TigerGraph claims):**
- 20× faster than Neo4j (on distributed workloads)
- Real-time 20-hop queries (seconds, not minutes)

**Independent Benchmarks:**
- Faster than Neo4j on distributed graphs (>10M nodes)
- Slower than Memgraph on single-node graphs (<1M nodes)

**Latency:**
- Simple read: 1-5ms
- Deep traversal (10+ hops): 500ms-2s (distributed)

**Throughput:**
- Reads: 5,000-20,000 queries/second (cluster)
- Writes: 1,000-10,000 writes/second

---

## Lock-In Assessment

**Lock-In Level:** Highest

- ❌ GSQL 100% proprietary (no standard)
- ❌ No open source option
- ❌ Enterprise licensing (yearly contracts)

**Migration Complexity:**
- **TigerGraph → Any other DB:** Very High (3-6 months)
- Complete GSQL → Cypher/Gremlin rewrite required

---

## Use Case Fit: Knowledge Graph for Research Project

**Recommended:** ❌ No (too expensive, high lock-in)

**Why:**
- ❌ Expensive ($99-499/month minimum, vs $25-100 alternatives)
- ❌ Highest lock-in (GSQL proprietary)
- ❌ Overkill (designed for 100M+ nodes, not 500 nodes)
- ❌ No free tier (90-day trial expires)

**When TigerGraph Makes Sense:**
- ✅ Enterprise budget ($10K+/month OK)
- ✅ Massive scale (100M+ nodes, real-time analytics)
- ✅ Deep-link queries critical (20+ hops)
- ✅ Vendor support required (enterprise SLAs)

---

## Summary

**Best For:**
- Large enterprises with massive graphs (fraud detection, supply chain)
- Real-time deep-link analytics (20+ hop queries)
- Teams with budget ($99-10,000+/month)

**Avoid If:**
- Small/medium graphs (<10M nodes) - overkill and expensive
- Lock-in concern (GSQL proprietary)
- Budget <$100/month

**Recommended For Research Project:**
❌ **No** (too expensive, highest lock-in, overkill)
