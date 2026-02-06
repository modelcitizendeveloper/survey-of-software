# ArangoDB (Multi-Model)

**Provider:** ArangoDB Inc.
**Founded:** 2011 (13+ years)
**Query Language:** AQL (ArangoDB Query Language)
**Deployment:** Managed cloud (ArangoDB Oasis), self-hosted (Community/Enterprise)
**Market Position:** Multi-model database (graph + document + key-value)

---

## Overview

ArangoDB is a **multi-model database** supporting three data models in one system: graph, document, and key-value. Uses proprietary AQL query language (SQL-like with graph extensions). Unique value proposition: "One database for all workloads" eliminating need for separate graph, document, and key-value databases.

**Strengths:**
- ✅ Multi-model (graph + document + key-value in one DB)
- ✅ Single query language across all models (AQL)
- ✅ Good performance (C++ implementation, fast)
- ✅ Free Community Edition (full features)
- ✅ Reasonable managed pricing ($20-500/month)

**Weaknesses:**
- ❌ Proprietary AQL (high lock-in, not Cypher/Gremlin)
- ❌ Smaller ecosystem (fewer integrations than Neo4j)
- ❌ Limited graph algorithms (basic only)
- ❌ Multi-model complexity (jack-of-all-trades, master of none)

---

## Pricing

### ArangoDB Oasis (Managed Cloud)

**Free Tier:**
- 4GB storage, 1 vCPU, 1GB RAM
- Suitable for: Development, small prototypes
- **Cost:** $0/month

**Developer Tier:**
- 20GB storage, 2 vCPU, 8GB RAM
- Suitable for: 50K-100K nodes, 500K edges
- **Cost:** $20/month

**Professional Tier:**
- 100GB storage, 4 vCPU, 32GB RAM
- Suitable for: 500K-1M nodes, 5M edges
- **Cost:** $80-150/month

**Enterprise Tier:**
- Custom sizing, multi-region
- **Cost:** $500-2,000+/month (contact sales)

### Self-Hosted

**Community Edition:**
- Free (Apache 2.0 license)
- Full features (single node)
- Infrastructure: $25-100/month (4-16GB RAM VPS)

**Enterprise Edition:**
- Clustering, SmartGraphs (sharded graphs), advanced security
- License: $10K-50K+/year

---

## Query Language: AQL

**Syntax Example:**
```aql
// Find research items that complement 3.041 and their dependencies
FOR item IN Research
  FILTER item.code == "3.041"
  FOR related IN 1..1 ANY item COMPLEMENTS
    FOR dependency IN 1..3 OUTBOUND related UPSTREAM_FROM
      RETURN {
        related: related,
        dependencies: dependency
      }
```

**Characteristics:**
- **Syntax:** SQL-like with graph extensions (FOR, FILTER, RETURN)
- **Readability:** Good (familiar to SQL users)
- **Portability:** ❌ Low (ArangoDB-specific, no standard)
- **Learning curve:** Medium (SQL + graph concepts)

**Lock-In:**
- ❌ High (AQL proprietary, no equivalent in other databases)
- ❌ Migration requires complete query rewrite

---

## Graph Algorithms

**Built-In:** Limited (basic traversal only)

ArangoDB includes **basic graph traversal algorithms**:
- ✅ Shortest path (Dijkstra)
- ✅ K-shortest paths
- ✅ All paths (with depth limits)
- ❌ **Missing:** PageRank, Louvain, centrality, community detection

**Community Algorithms:**
- Some algorithms available as community UDFs (User Defined Functions)
- Quality and maintenance variable

**Comparison:**
- Neo4j GDS: 60+ algorithms
- Memgraph MAGE: 30+ algorithms
- ArangoDB: <10 basic algorithms

---

## Performance

**Latency:**
- Simple read (1 hop): 2-10ms
- Medium traversal (2-3 hops): 20-100ms
- Complex traversal (4-6 hops): 100-500ms

**Throughput:**
- Reads: 1,000-5,000 queries/second
- Writes: 500-2,000 writes/second

**Multi-Model Overhead:**
- Slower than specialized graph databases (Neo4j, Memgraph)
- Benefit: One database for multiple workloads

---

## Lock-In Assessment

**Lock-In Level:** High

- ❌ AQL proprietary (no migration path)
- ❌ Multi-model complexity (data modeling differs from pure graph)
- ⚠️ Self-host option (Community Edition mitigates some risk)

**Migration Complexity:**
- **ArangoDB → Neo4j:** High (2-3 months, AQL → Cypher rewrite)
- **ArangoDB → Any other graph DB:** High (complete rewrite)

---

## Use Case Fit: Knowledge Graph for Research Project

**Recommended:** ⚠️ Maybe (if multi-model needs exist)

**Pros:**
- ✅ Multi-model (graph + documents for research metadata)
- ✅ Affordable ($20-80/month managed or $25-50 self-hosted)

**Cons:**
- ❌ Limited algorithms (no PageRank, Louvain, centrality)
- ❌ High lock-in (AQL proprietary)
- ❌ Multi-model complexity (if only need graph)

**Better if:**
- Need graph + document + key-value in one database
- Want to consolidate multiple databases

**Worse than:**
- Neo4j Community: More algorithms, Cypher portability
- Memgraph Community: Faster, MAGE algorithms, lower lock-in

---

## Summary

**Best For:**
- Multi-model workloads (graph + documents in one DB)
- Teams wanting to consolidate databases
- SQL-familiar teams (AQL syntax similar)

**Avoid If:**
- Need rich graph algorithms (PageRank, community detection)
- Lock-in is concern (AQL proprietary)
- Pure graph workload (specialized graph DBs better)

**Recommended For Research Project:**
⚠️ **Maybe** ($20-80/month, but limited algorithms and high lock-in)
