# S1 Synthesis: Graph Database Quick Recommendations

**Research Date:** November 16, 2025
**Providers Analyzed:** 7 (Neo4j, Neptune, Memgraph, JanusGraph, ArangoDB, TigerGraph, Dgraph)
**Primary Use Case:** Knowledge graph for research project (500 nodes, 5K edges)

---

## Executive Summary

**Top Recommendations for Knowledge Graph (Research Project):**

1. **Memgraph Community (self-hosted)** - $25-50/month
   - ✅ Best value: Lowest cost, full MAGE algorithms, 10× faster than Neo4j
   - ✅ Low lock-in: openCypher standard, easy migration to Neo4j
   - ⚠️ Smaller ecosystem than Neo4j

2. **Neo4j Community (self-hosted)** - $50-100/month
   - ✅ Most algorithms: GDS library (60+), best ecosystem
   - ✅ Best documentation and community support
   - ⚠️ Some lock-in (GDS proprietary, APOC)

3. **Dgraph (self-hosted)** - $25-50/month
   - ✅ GraphQL-native (if building API)
   - ✅ Low lock-in (open source, Apache 2.0)
   - ❌ No graph algorithms (must build custom)

**Avoid for Small Knowledge Graph:**
- ❌ Amazon Neptune: $90-350/month, no algorithms, AWS lock-in
- ❌ TigerGraph: $99-499/month, highest lock-in, overkill
- ❌ JanusGraph: $100-150/month, complex ops, no algorithms
- ❌ ArangoDB: Limited algorithms, high lock-in (AQL proprietary)

---

## Comparison Matrix: Quick Reference

| Database | Cost/Month | Algorithms | Lock-In | Query Language | Recommended? |
|----------|------------|------------|---------|----------------|--------------|
| **Memgraph Community** | $25-50 | 30+ (MAGE) | Low | Cypher | ✅ **Yes** |
| **Neo4j Community** | $50-100 | 60+ (GDS) | Medium | Cypher | ✅ **Yes** |
| **Dgraph** | $25-50 | 0 | Low | GraphQL/DQL | ⚠️ Maybe |
| **Neptune Serverless** | $90-350 | 0 | High | Gremlin/openCypher | ❌ No |
| **ArangoDB** | $20-80 | <10 | High | AQL | ⚠️ Maybe |
| **TigerGraph** | $99-499 | 30+ | Highest | GSQL | ❌ No |
| **JanusGraph** | $100-150 | 0 | Low | Gremlin | ❌ No |

---

## Decision Tree

```
Do you need graph algorithms (PageRank, community detection)?
├─ YES → Continue...
│   ├─ Budget <$50/month?
│   │   └─ YES → Memgraph Community ($25-50, 30+ algorithms) ✅
│   ├─ Budget $50-100/month?
│   │   └─ YES → Neo4j Community ($50-100, 60+ algorithms) ✅
│   └─ Budget >$100/month?
│       └─ Consider Neo4j Aura Professional or Memgraph Cloud
│
└─ NO (traversal only) → Continue...
    ├─ Need GraphQL API?
    │   └─ YES → Dgraph ($25-50, GraphQL-native) ⚠️
    ├─ AWS-committed?
    │   └─ YES → Neptune ($90-350, AWS-native) ⚠️
    └─ Multi-model needs (graph + documents)?
        └─ YES → ArangoDB ($20-80, multi-model) ⚠️
```

---

## Detailed Recommendations by Use Case

### Use Case: Knowledge Graph for Research Project

**Requirements:**
- 100-500 nodes (research items, technologies, providers)
- 500-5,000 relationships (complements, upstream_from, references)
- Algorithms: PageRank, Louvain, centrality (identify important research, clusters)
- Budget: <$100/month
- Lock-in: Avoid expensive vendor lock-in

**Recommendation #1: Memgraph Community (self-hosted)**

**Monthly Cost:** $25-50
- Infrastructure: DigitalOcean 4GB Droplet ($24/month)
- License: Free (Community Edition)

**Pros:**
- ✅ Lowest cost ($25-50 vs Neo4j $50-100)
- ✅ Full MAGE algorithms (PageRank, Louvain, centrality, 30+ total)
- ✅ 10× faster queries (in-memory)
- ✅ Low lock-in (openCypher → migrate to Neo4j if needed)
- ✅ Perfect fit for 500 nodes, 5K edges (2-4GB RAM sufficient)

**Cons:**
- ⚠️ Smaller ecosystem (fewer tutorials than Neo4j)
- ⚠️ Less mature (8 years vs Neo4j 17 years)

**Setup:**
```bash
# Docker Compose
docker run -d --name memgraph \
  -p 7687:7687 -p 3000:3000 \
  -v mg_lib:/var/lib/memgraph \
  memgraph/memgraph-platform:latest
```

**When to Migrate:**
- If need >30 algorithms (Neo4j GDS has 60+)
- If prefer larger ecosystem (more integrations, tutorials)

---

**Recommendation #2: Neo4j Community (self-hosted)**

**Monthly Cost:** $50-100
- Infrastructure: DigitalOcean 8GB Droplet ($48/month) or AWS r6g.large ($106/month reserved)
- License: Free (Community Edition)

**Pros:**
- ✅ Most graph algorithms (GDS 60+)
- ✅ Best ecosystem (largest community, most integrations, best docs)
- ✅ Most mature (17 years, battle-tested)
- ✅ Cypher query language (most readable)

**Cons:**
- ⚠️ 2× cost vs Memgraph ($50-100 vs $25-50)
- ⚠️ Some lock-in (GDS proprietary, APOC Neo4j-specific)
- ⚠️ Slower than Memgraph (disk-based vs in-memory)

**Setup:**
```bash
# Docker with GDS and APOC
docker run -d --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  -e NEO4J_PLUGINS='["apoc", "graph-data-science"]' \
  neo4j:5.13-community
```

**Choose Neo4j over Memgraph if:**
- Need >30 algorithms (GDS has 60+)
- Prefer mature ecosystem (more resources)
- Team already knows Neo4j/Cypher

---

**Recommendation #3: Dgraph (self-hosted)**

**Monthly Cost:** $25-50
- Infrastructure: DigitalOcean 4GB Droplet ($24/month)
- License: Free (Apache 2.0)

**Pros:**
- ✅ GraphQL-native (if building API for research project)
- ✅ Low lock-in (open source, Apache 2.0)
- ✅ Lowest cost ($25-50)

**Cons:**
- ❌ **No graph algorithms** (must implement PageRank, Louvain manually)
- ⚠️ Smaller ecosystem
- ⚠️ DQL proprietary (for advanced queries)

**Choose Dgraph only if:**
- Building GraphQL API on top of knowledge graph
- Don't need graph algorithms (traversal only)
- Prioritize open source + low lock-in

**Otherwise:** Use Memgraph or Neo4j (both have algorithms)

---

## Why NOT Recommended for Small Knowledge Graph

### Amazon Neptune: ❌ Not Recommended

**Reasons:**
- ❌ Expensive: $90-350/month (vs $25-100 for alternatives)
- ❌ No algorithms: PageRank, Louvain, centrality require expensive Neptune Analytics ($17K/month!) or custom ETL
- ❌ AWS lock-in: Cannot self-host, cannot migrate to other clouds
- ⚠️ Cold start latency: Serverless idles after 15 min (1-3 sec wake-up)

**When Neptune makes sense:**
- ✅ AWS-committed (already on AWS, need IAM integration)
- ✅ Budget >$200/month
- ✅ High availability critical (multi-AZ built-in)
- ✅ Traversal-only workload (no algorithms needed)

---

### TigerGraph: ❌ Not Recommended

**Reasons:**
- ❌ Expensive: $99-499/month (vs $25-100 alternatives)
- ❌ Highest lock-in: GSQL 100% proprietary, no equivalent
- ❌ Overkill: Designed for 100M+ nodes, not 500 nodes
- ❌ No free tier: 90-day trial expires

**When TigerGraph makes sense:**
- ✅ Enterprise budget ($10K+/month OK)
- ✅ Massive scale (100M+ nodes)
- ✅ Real-time deep-link analytics (20+ hop queries)

---

### JanusGraph: ❌ Not Recommended

**Reasons:**
- ❌ Complex ops: Requires Cassandra + Elasticsearch clusters (3 systems)
- ❌ Higher cost: $100-150/month (vs $25-100 simpler alternatives)
- ❌ No algorithms: Must implement PageRank, Louvain manually
- ❌ Overkill: Designed for billions of nodes, not 500

**When JanusGraph makes sense:**
- ✅ Massive scale (>10M nodes, proven to billions)
- ✅ Write-heavy (Cassandra backend optimized)
- ✅ Zero lock-in (Apache open source, Gremlin standard)
- ✅ Strong ops team (can manage multi-cluster)

---

### ArangoDB: ⚠️ Maybe (if multi-model needed)

**Reasons:**
- ⚠️ Limited algorithms (<10 vs 30-60 in Neo4j/Memgraph)
- ⚠️ High lock-in (AQL proprietary, no Cypher/Gremlin)
- ⚠️ Multi-model complexity (if only need graph)

**When ArangoDB makes sense:**
- ✅ Multi-model needs (graph + documents + key-value in one DB)
- ✅ Want to consolidate databases
- ✅ SQL-familiar teams (AQL syntax similar)

**Otherwise:** Use Memgraph or Neo4j (specialized graph DBs better)

---

## Cost Comparison (Apples-to-Apples)

**Same workload:** 500 nodes, 5,000 edges, self-hosted

| Database | Infrastructure | License | Total/Month | Algorithms | Lock-In |
|----------|----------------|---------|-------------|------------|---------|
| **Memgraph Community** | $25 (4GB VPS) | $0 | **$25** | 30+ (MAGE) | Low |
| **Dgraph** | $25 (4GB VPS) | $0 | **$25** | 0 | Low |
| **Neo4j Community** | $50 (8GB VPS) | $0 | **$50** | 60+ (GDS) | Medium |
| **ArangoDB Community** | $25 (4GB VPS) | $0 | **$25** | <10 | High |
| **Neptune Serverless** | AWS managed | AWS | **$90-120** | 0 | High |
| **TigerGraph Cloud** | Managed | Included | **$99** | 30+ | Highest |
| **JanusGraph** | $50 (JG) + $50 (Cass) | $0 | **$100** | 0 | Low |

**Key Insight:**
- 4× cost variance ($25 Memgraph vs $99 TigerGraph)
- Cheapest options: Memgraph, Dgraph, ArangoDB ($25/month)
- Best value: Memgraph ($25/month with 30+ algorithms)
- Most expensive: TigerGraph ($99/month minimum)

---

## Lock-In Spectrum (Lowest to Highest)

**Lowest Lock-In:**
1. **JanusGraph** (Apache open source, Gremlin standard)
2. **Memgraph** (openCypher standard, self-host free)
3. **Dgraph** (Apache open source, GraphQL standard)

**Medium Lock-In:**
4. **Neo4j** (Cypher leader, Community Edition available)

**High Lock-In:**
5. **ArangoDB** (AQL proprietary)
6. **Neptune** (AWS-only, no self-host)

**Highest Lock-In:**
7. **TigerGraph** (GSQL 100% proprietary, no open source)

---

## Query Language Portability

**High Portability:**
- **Gremlin** (Apache TinkerPop standard)
  - JanusGraph ↔ Neptune ↔ Cosmos DB (low effort)
- **openCypher** (multi-vendor)
  - Memgraph ↔ Neo4j ↔ Neptune openCypher (low-medium effort)

**Medium Portability:**
- **Cypher** (Neo4j dominant, but Memgraph compatible)
  - Neo4j ↔ Memgraph (low effort, 95%+ compatible)
  - Neo4j ↔ Neptune openCypher (medium effort, 80% compatible)
- **GraphQL** (Dgraph-specific implementation)
  - Dgraph → other DBs (medium-high effort)

**Low Portability (Proprietary):**
- **AQL** (ArangoDB-only)
- **GSQL** (TigerGraph-only)
- **DQL** (Dgraph-only, advanced queries)

---

## Final Recommendation

**For Knowledge Graph (Research Project - 500 nodes, 5K edges):**

### Start with: Memgraph Community ($25-50/month)

**Why:**
- ✅ Lowest cost ($25-50/month)
- ✅ Full MAGE algorithms (PageRank, Louvain, centrality)
- ✅ 10× faster than Neo4j (in-memory)
- ✅ Low lock-in (openCypher → easy migration to Neo4j)
- ✅ Perfect fit for small knowledge graph

**Upgrade to Neo4j Community if:**
- Need >30 algorithms (Neo4j GDS has 60+)
- Prefer larger ecosystem (more tutorials, integrations)
- Budget allows $50-100/month

**Alternative: Dgraph if:**
- Building GraphQL API (frontend-friendly)
- Don't need graph algorithms
- Prioritize open source (Apache 2.0)

---

## Migration Strategy

**Phase 1: Start Small (Year 1)**
- Use Memgraph Community (lowest cost, full features)
- Export data weekly to S3 (backup + migration readiness)
- Track proprietary feature usage (none for core Cypher)

**Phase 2: Evaluate (Year 2)**
- If need more algorithms: Migrate to Neo4j Community (1-2 days effort)
- If outgrow single node: Consider Memgraph Enterprise (clustering) or Neo4j Enterprise
- If budget tight: Stay on Memgraph Community (scales to millions of nodes)

**Phase 3: Scale (Year 3+)**
- If >1M nodes: Consider JanusGraph (distributed, Cassandra backend)
- If AWS-committed: Consider Neptune (managed, eliminate ops)
- If enterprise needs: Neo4j Enterprise or TigerGraph

**Key Principle:**
- Start with lowest lock-in, lowest cost option (Memgraph)
- Migrate only when clear benefit (more algorithms, better scaling, managed service)
- Regular exports ensure migration readiness

---

**Next:** S2 Comprehensive (feature matrix, pricing TCO, performance benchmarks)
