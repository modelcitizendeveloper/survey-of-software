# Amazon Neptune (AWS Managed)

**Provider:** Amazon Web Services (AWS)
**Launched:** 2018 (6+ years)
**Query Languages:** Gremlin (Apache TinkerPop), openCypher, SPARQL (RDF)
**Deployment:** Managed cloud only (AWS-native)
**Market Position:** #2 graph database, AWS ecosystem leader

---

## Overview

Amazon Neptune is AWS's **managed graph database service** supporting three query languages: Gremlin (property graph, Apache standard), openCypher (Neo4j-compatible), and SPARQL (RDF/semantic web). Launched in 2018, Neptune is the go-to graph database for AWS-committed organizations.

**Strengths:**
- ✅ AWS-native integration (IAM, VPC, CloudWatch, Lambda)
- ✅ Dual query language support (Gremlin + openCypher)
- ✅ Serverless option (Neptune Serverless, pay-per-request)
- ✅ High availability built-in (6 copies across 3 AZs)
- ✅ Automatic backups, point-in-time recovery
- ✅ Low lock-in for Gremlin (Apache standard, portable)

**Weaknesses:**
- ❌ AWS-only (no self-hosting, no multi-cloud)
- ❌ Limited graph algorithms (no built-in PageRank, Louvain, etc.)
- ❌ Serverless cold start latency (1-3 seconds)
- ❌ Expensive for continuous workloads (serverless pricing model)
- ❌ openCypher support incomplete (missing advanced features)

---

## Pricing

### Neptune Serverless (Pay-Per-Request)

**Pricing Model:**
- **NCUs (Neptune Capacity Units):** 1 NCU = compute + memory for queries
- Minimum: 1 NCU ($0.12/hour = $87/month baseline)
- Auto-scales: 1-128 NCUs based on workload
- Storage: $0.10/GB/month
- I/O: $0.20 per 1M requests

**Example Costs:**

**Small Knowledge Graph (100 nodes, 500 edges):**
- NCU usage: 1-2 NCUs average (idle most of time)
- Storage: 0.1GB = $0.01/month
- I/O: 1M requests/month = $0.20/month
- **Total: ~$90-120/month** (minimum NCU baseline)

**Medium Graph (10K nodes, 50K edges):**
- NCU usage: 2-4 NCUs average
- Storage: 1GB = $0.10/month
- I/O: 10M requests/month = $2/month
- **Total: ~$180-350/month**

**Large Graph (1M nodes, 5M edges):**
- NCU usage: 8-16 NCUs average
- Storage: 100GB = $10/month
- I/O: 100M requests/month = $20/month
- **Total: ~$700-1,400/month**

**Caveat:** Serverless has cold start latency (1-3 seconds) if idle >15 minutes.

---

### Neptune Provisioned (Reserved Instances)

**Instance Types:**

**db.r6g.large (2 vCPU, 16GB RAM):**
- On-demand: $0.348/hour = $252/month
- 1-year reserved: $0.219/hour = $159/month
- 3-year reserved: $0.146/hour = $106/month
- **Suitable for:** 100K nodes, 500K edges

**db.r6g.xlarge (4 vCPU, 32GB RAM):**
- On-demand: $0.696/hour = $504/month
- 1-year reserved: $0.438/hour = $317/month
- 3-year reserved: $0.292/hour = $212/month
- **Suitable for:** 500K nodes, 2.5M edges

**db.r6g.2xlarge (8 vCPU, 64GB RAM):**
- On-demand: $1.392/hour = $1,008/month
- 1-year reserved: $0.876/hour = $635/month
- 3-year reserved: $0.584/hour = $423/month
- **Suitable for:** 2M nodes, 10M edges

**Additional Costs:**
- Storage: $0.10/GB/month (same as serverless)
- I/O: $0.20 per 1M requests
- Backups: $0.021/GB/month (beyond 100% of DB size)
- Data transfer: $0.09/GB out (to internet)

**High Availability:**
- Neptune automatically creates 2 read replicas (6 copies total across 3 AZs)
- Included in instance price (no extra charge for HA)

---

## Query Languages

Neptune supports **three query languages** (choose one based on use case):

### 1. Gremlin (Apache TinkerPop)

**Best For:** Property graph workloads, Apache ecosystem integration

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
- ✅ High (Apache TinkerPop standard)
- ✅ Compatible with: JanusGraph, Azure Cosmos DB (Gremlin API), TinkerGraph
- ✅ Migration path: Neptune → JanusGraph (low effort)

---

### 2. openCypher (Neo4j-Compatible)

**Best For:** Teams familiar with Neo4j, Cypher syntax preference

**Syntax Example:**
```cypher
// Same query in openCypher
MATCH (item:Research {code: "3.041"})-[:COMPLEMENTS]-(related)
MATCH (related)-[:UPSTREAM_FROM*1..3]-(dependency)
RETURN related.code, related.title, collect(dependency.code) AS dependencies
```

**Portability:**
- ⚠️ Medium (openCypher spec, but Neptune support incomplete)
- ⚠️ Compatible with: Neo4j, Memgraph (core Cypher only)
- ❌ Missing features: APOC, advanced Cypher (FOREACH, MERGE edge cases)

**Caveat:** Neptune's openCypher is ~80% compatible with Neo4j Cypher. Test thoroughly before migrating.

---

### 3. SPARQL (RDF/Semantic Web)

**Best For:** Semantic web, ontologies, knowledge graphs (W3C standards)

**Not relevant for property graph use cases** (research project relationships).

---

## Graph Algorithms

**Built-In Algorithms:** ❌ None

Neptune **does not provide built-in graph algorithms** (no PageRank, Louvain, centrality, etc.).

**Workarounds:**

**Option 1: Neptune ML (Machine Learning)**
- Export graph to S3 → SageMaker → Train embeddings → Import predictions
- **Use case:** Node classification, link prediction (ML-based)
- **Cost:** SageMaker charges ($0.50-5/hour)
- **Complexity:** High (multi-step pipeline)

**Option 2: Neptune Analytics (NEW in 2024)**
- Separate service for graph analytics (in-memory, algorithm-focused)
- Supports: PageRank, centrality, community detection, shortest path
- **Pricing:** $1.50/GB RAM/hour (expensive for continuous use)
- **Example:** 16GB RAM = $24/hour = $17,280/month (!)
- **Use case:** Periodic batch analytics (not real-time queries)

**Option 3: Export + Process Externally**
- Export graph to S3 (JSON/CSV)
- Run algorithms in Python (NetworkX, igraph)
- Import results back to Neptune
- **Cost:** Minimal (compute time only)
- **Complexity:** High (custom ETL pipeline)

**Option 4: AWS Lambda + NetworkX**
- Lambda function triggered on query
- Load subgraph, run algorithm (PageRank, Louvain)
- Cache results
- **Cost:** $0.20 per 1M requests
- **Complexity:** Medium

**Comparison to Neo4j:**
- Neo4j GDS: 60+ algorithms built-in, fast
- Neptune: Zero built-in algorithms, workarounds required

**Impact:**
- ❌ Neptune not suitable for algorithm-heavy workloads (research project use case)
- ✅ Neptune suitable for traversal-only workloads (social graph, recommendation)

---

## Performance

**Benchmark Context:**
- 1M nodes, 5M relationships
- Instance: db.r6g.large (2 vCPU, 16GB RAM)

**Latency (Provisioned Instances):**
- **Simple read (1 hop):** 2-10ms
- **Medium traversal (2-3 hops):** 20-100ms
- **Complex traversal (4-6 hops):** 100-500ms

**Latency (Serverless):**
- **Warm:** Same as provisioned
- **Cold start:** 1-3 seconds (if idle >15 minutes)

**Throughput:**
- **Reads:** 500-2,000 queries/second (single instance)
- **Writes:** 100-300 writes/second (ACID transactions)

**Comparison:**
- Slower than Neo4j (optimized indexes)
- Slower than Memgraph (in-memory)
- Similar to JanusGraph (backend-dependent)

**Scaling:**
- **Vertical:** Up to 128 vCPU, 1024GB RAM (db.r6g.32xlarge)
- **Horizontal:** Read replicas (up to 15 replicas)

---

## Self-Hosting

**Self-Hosting:** ❌ Not available

Neptune is **managed-only** (AWS-proprietary, no download/install option).

**Implications:**
- Cannot self-host (no cost optimization via DIY)
- Cannot deploy on-premises (air-gapped environments)
- Must stay on AWS (no multi-cloud)

**Migration Path:**
- If need self-hosting: Migrate to JanusGraph (Gremlin-compatible) or Neo4j (openCypher)

---

## Lock-In Assessment

**Lock-In Level:** Medium-High

**Low Lock-In Factors:**
- ✅ Gremlin queries portable (Apache standard → JanusGraph, Cosmos DB)
- ✅ openCypher queries partially portable (→ Neo4j, Memgraph with rewrite)
- ✅ Export formats (JSON, CSV, GraphML)

**High Lock-In Factors:**
- ❌ AWS-only (no self-hosting, no multi-cloud)
- ❌ IAM integration (migrate away = rewrite auth)
- ❌ CloudWatch, VPC, Lambda integrations (tight AWS coupling)
- ❌ Neptune ML, Analytics (proprietary services)
- ❌ Serverless pricing model unique (hard to replicate elsewhere)

**Migration Complexity:**

**Neptune (Gremlin) → JanusGraph (Gremlin):**
- **Effort:** Low-Medium (1-2 weeks)
- **Data export:** Gremlin scripts or bulk export
- **Query compatibility:** High (both use Apache TinkerPop)
- **Infrastructure:** Setup JanusGraph cluster (Cassandra + Elasticsearch backends)

**Neptune (openCypher) → Neo4j:**
- **Effort:** Medium (2-4 weeks)
- **Data export:** CSV export → Neo4j import
- **Query compatibility:** Medium (80% compatible, test edge cases)
- **Cost:** Neo4j Aura $65-240/month or Community self-hosted $50-100/month

**Mitigation Strategies:**
1. Use Gremlin (more portable than openCypher on Neptune)
2. Avoid Neptune ML, Analytics (proprietary services)
3. Minimize IAM/AWS-specific integrations
4. Regular exports to S3 (backup + migration readiness)

---

## Use Case Fit: Knowledge Graph for Research Project

**Scenario:**
- 100-500 nodes (research items, technologies, providers)
- 500-5,000 relationships (complements, upstream_from, references)
- Queries: Dependency traversal, **community detection, centrality**

**Recommended:** ❌ Not recommended

**Why:**
- ❌ **No built-in graph algorithms** (PageRank, Louvain, centrality)
  - Must use Neptune Analytics ($17K/month for 16GB RAM!) or export + process externally
  - Research project requires algorithm-heavy analysis (community detection, centrality)
- ❌ **Expensive for small scale:** Serverless minimum ~$90/month (1 NCU baseline)
  - Neo4j Community self-hosted: $50-100/month (full algorithms)
  - Memgraph Community self-hosted: $50-100/month (full algorithms)
- ❌ **AWS lock-in:** Cannot self-host, cannot migrate to other clouds easily
- ⚠️ **Cold start latency:** Serverless idles after 15 minutes (1-3 second wake-up)

**When Neptune Makes Sense:**
- ✅ AWS-committed organization (already on AWS, IAM integration required)
- ✅ Traversal-only workloads (no algorithms needed)
- ✅ High availability critical (built-in multi-AZ replication)
- ✅ Budget >$200/month (provisioned instance worth it)

**Better Alternatives for Research Project:**
1. **Neo4j Community (self-hosted):** $50-100/month, full GDS algorithms
2. **Memgraph Community (self-hosted):** $50-100/month, MAGE algorithms, faster
3. **JanusGraph (self-hosted):** $100-200/month, Gremlin, scalable

---

## Vendor Viability

**Financial Stability:**
- Backed by Amazon (trillion-dollar company)
- Part of AWS core services (not at risk of shutdown)

**Market Position:**
- #2 graph database (after Neo4j)
- Default choice for AWS-committed organizations

**10-Year Outlook:**
- **Probability of existence:** 99%+
- **Risk:** Extremely low (AWS core service)
- **Acquisition potential:** N/A (AWS product)

**Price Change Risk:**
- Medium (AWS has history of gradual price increases)
- Mitigation: 3-year reserved instances (lock pricing)

---

## Summary

**Best For:**
- AWS-committed organizations (existing AWS infrastructure)
- Traversal-heavy workloads (social graphs, recommendation engines)
- High availability requirements (multi-AZ, automatic failover)
- Teams needing Gremlin + openCypher flexibility

**Avoid If:**
- Graph algorithms critical (PageRank, community detection, centrality)
- Budget <$200/month (too expensive for small scale)
- Self-hosting needed (air-gapped, on-premises, multi-cloud)
- Sub-millisecond latency required (cold start on serverless)

**Recommended For Research Project Use Case:**
❌ **No** (no built-in algorithms, expensive, AWS lock-in)

**Reasoning:**
- Research project requires graph algorithms (PageRank, Louvain, centrality)
- Neptune requires expensive workarounds (Neptune Analytics $17K/month or custom ETL)
- Neo4j Community or Memgraph Community cheaper ($50-100/month) with full algorithms
- AWS lock-in not justified for small-scale knowledge graph
