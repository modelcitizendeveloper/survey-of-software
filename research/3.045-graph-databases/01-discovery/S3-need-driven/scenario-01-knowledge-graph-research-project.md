# S3: Knowledge Graph for Research Project

**Use Case:** Representing research project as graph database
**Scale:** 100-500 nodes, 500-5,000 edges (growing ~50 nodes/year)
**Budget:** <$100/month preferred
**Priority:** Graph algorithms (PageRank, community detection, centrality), low lock-in

---

## Business Context

**Problem:**
Research project spans multiple domains (managed services, databases, algorithms, infrastructure). Relationships between research items are complex:
- **Complements:** Research A complements research B (related topics)
- **Upstream dependencies:** Research A must be completed before B
- **References:** Research A references findings from B
- **Integrates with:** Technology A integrates with technology B

**Current State:**
- Research items tracked in markdown files (YAML frontmatter)
- Relationships documented manually in separate files
- No automated dependency analysis
- No visualization of research clusters
- Hard to answer questions like:
  - "What research items complement 3.041 NoSQL?"
  - "What are the dependencies for 3.007 FP&A Platforms?"
  - "Which research areas have the most connections (centrality)?"
  - "Are there natural clusters of related research (community detection)?"

**Desired State:**
- Graph database with research items as nodes
- Relationships as first-class edges
- Query dependencies, complements, references programmatically
- Run graph algorithms (PageRank, Louvain, centrality) to:
  - Identify most important research items
  - Discover clusters of related research
  - Find gaps in coverage
  - Prioritize future research

---

## Data Model

### Nodes

**Research Item:**
```json
{
  "code": "3.041",
  "title": "NoSQL Databases",
  "tier": 3,
  "status": "completed",
  "date_completed": "2025-11-16",
  "deliverables": {
    "files": 21,
    "lines": 5458,
    "providers_analyzed": 8
  }
}
```

**Technology:**
```json
{
  "name": "MongoDB Atlas",
  "category": "NoSQL Database",
  "type": "Document Database"
}
```

**Provider:**
```json
{
  "name": "MongoDB Inc.",
  "type": "Managed Service"
}
```

### Edges

**COMPLEMENTS:**
```cypher
(research_a:Research)-[:COMPLEMENTS]->(research_b:Research)
// 3.041 NoSQL Databases COMPLEMENTS 3.044 Data Warehouses
```

**UPSTREAM_FROM:**
```cypher
(research_a:Research)-[:UPSTREAM_FROM]->(research_b:Research)
// 3.007 FP&A Platforms UPSTREAM_FROM 3.044 Data Warehouses
// (must analyze warehouses before FP&A, since FP&A integrates with warehouses)
```

**REFERENCES:**
```cypher
(research_a:Research)-[:REFERENCES]->(research_b:Research)
// 3.045 Graph Databases REFERENCES 3.041 NoSQL Databases
```

**ANALYZES:**
```cypher
(research:Research)-[:ANALYZES]->(provider:Provider)
// 3.041 NoSQL Databases ANALYZES MongoDB Inc.
```

**INTEGRATES_WITH:**
```cypher
(tech_a:Technology)-[:INTEGRATES_WITH]->(tech_b:Technology)
// MongoDB Atlas INTEGRATES_WITH AWS Lambda
```

---

## Sample Queries

### Query 1: Find All Complements of a Research Item

```cypher
// Find research items that complement 3.041 NoSQL Databases
MATCH (item:Research {code: "3.041"})-[:COMPLEMENTS]-(related:Research)
RETURN related.code, related.title, related.status
ORDER BY related.code
```

**Expected Result:**
- 3.040 Databases (OLTP complements NoSQL)
- 3.044 Data Warehouses (OLAP complements NoSQL)
- 3.064 Metadata Management (catalogs complement NoSQL)

---

### Query 2: Find Dependency Chain (Upstream Path)

```cypher
// Find all upstream dependencies for 3.007 FP&A Platforms
MATCH path = (item:Research {code: "3.007"})-[:UPSTREAM_FROM*1..5]->(dependency:Research)
RETURN dependency.code, dependency.title, length(path) AS depth
ORDER BY depth, dependency.code
```

**Expected Result:**
- Depth 1: 3.044 Data Warehouses (direct dependency)
- Depth 2: 3.031 Object Storage (warehouses depend on object storage)
- Depth 2: 3.040 Databases (warehouses depend on OLTP databases)

---

### Query 3: Most Important Research Items (PageRank)

```cypher
// Run PageRank to find most referenced/connected research items
CALL pagerank.get()
YIELD node, rank
WHERE node:Research
RETURN node.code, node.title, rank
ORDER BY rank DESC
LIMIT 10
```

**Expected Insights:**
- High rank: 3.040 Databases (many items reference/depend on it)
- High rank: 3.031 Object Storage (foundational, many dependencies)
- Low rank: Specialized niche research (1.120 Simulation)

**Business Value:**
- Prioritize high-PageRank items (foundational, high-impact)
- Ensure high-PageRank items are completed first (unblock other research)

---

### Query 4: Identify Research Clusters (Community Detection)

```cypher
// Run Louvain community detection to find research clusters
CALL louvain.get()
YIELD node, community_id
WHERE node:Research
RETURN community_id, collect(node.code) AS research_items, count(*) AS cluster_size
ORDER BY cluster_size DESC
```

**Expected Clusters:**
- Cluster 1: Data persistence (3.040 Databases, 3.041 NoSQL, 3.044 Warehouses)
- Cluster 2: Infrastructure (3.050 PaaS, 3.031 Object Storage)
- Cluster 3: Observability (2.041 Prometheus, 2.050 PostgreSQL logs)

**Business Value:**
- Discover natural groupings of research
- Plan research roadmap by cluster (complete all data persistence research together)
- Identify gaps (clusters with no completed research)

---

### Query 5: Find Missing Links (Should Research A Reference B?)

```cypher
// Find research items in same cluster but not yet connected
MATCH (a:Research)-[:COMPLEMENTS]-(common:Research)-[:COMPLEMENTS]-(b:Research)
WHERE a <> b
  AND NOT (a)-[:COMPLEMENTS]-(b)
  AND NOT (a)-[:REFERENCES]-(b)
RETURN a.code, b.code, count(common) AS common_complements
ORDER BY common_complements DESC
LIMIT 10
```

**Expected Insights:**
- 3.041 NoSQL should reference 3.045 Graph Databases (both NoSQL categories)
- 3.007 FP&A should complement 3.064 Metadata Management (both use metadata)

**Business Value:**
- Discover missing relationships
- Improve research connectivity
- Suggest future research based on gaps

---

## Database Evaluation for This Use Case

### Requirements

**Must-Have:**
- ✅ Graph algorithms (PageRank, Louvain, centrality)
- ✅ Low cost (<$100/month, preferably <$50)
- ✅ Low lock-in (open source or open standards)
- ✅ Self-hosting option (data sovereignty)
- ✅ Cypher or Gremlin (readable query language)

**Nice-to-Have:**
- ⚠️ Managed option (if self-hosting too complex)
- ⚠️ Web UI (query builder, visualization)
- ⚠️ Export formats (JSON, CSV, GraphML)

**Not Needed:**
- ❌ Massive scale (>1M nodes) - only 500 nodes expected
- ❌ High write throughput - mostly read queries after initial load
- ❌ Real-time updates - batch updates daily/weekly acceptable

---

### Option 1: Memgraph Community (Self-Hosted) ✅ RECOMMENDED

**Pricing:**
- DigitalOcean 4GB Droplet: $24/month
- Memgraph Community Edition: Free
- **Total: $24/month ($288/year, $864 over 3 years)**

**Pros:**
- ✅ Lowest cost ($24/month)
- ✅ Full MAGE algorithms (PageRank, Louvain, centrality, 30+ total)
- ✅ 10× faster than Neo4j (in-memory)
- ✅ Low lock-in (openCypher standard, easy migration to Neo4j)
- ✅ Perfect fit for 500 nodes, 5K edges (2-4GB RAM sufficient)
- ✅ Memgraph Lab web UI included (query editor, visualization)
- ✅ Docker setup (10 minutes to deploy)

**Cons:**
- ⚠️ Smaller ecosystem than Neo4j (fewer integrations)
- ⚠️ Less mature (8 years vs Neo4j 17 years)
- ⚠️ Single node only (Community Edition, but sufficient for this scale)

**Setup:**
```bash
# Docker Compose
docker run -d --name memgraph \
  -p 7687:7687 -p 3000:3000 \
  -v mg_lib:/var/lib/memgraph \
  memgraph/memgraph-platform:latest

# Access Memgraph Lab: http://localhost:3000
# Run Cypher queries, visualize graph, run MAGE algorithms
```

**Sample Workflow:**
1. Load research items from YAML → Cypher LOAD CSV
2. Create relationships (complements, upstream_from, references)
3. Run PageRank: `CALL pagerank.get()`
4. Run Louvain: `CALL louvain.get()`
5. Export results to JSON for reporting

**Why Recommended:**
- Best value ($24/month with 30+ algorithms)
- Lowest cost among algorithm-rich options
- Low lock-in (migrate to Neo4j if needed in 1-2 days)
- Fast enough for 500 nodes (<1ms queries)
- Self-hosted (data sovereignty, no vendor dependency)

---

### Option 2: Neo4j Community (Self-Hosted) ⚠️ ALTERNATIVE

**Pricing:**
- DigitalOcean 8GB Droplet: $48/month (recommended for GDS)
- Neo4j Community Edition: Free
- **Total: $48/month ($576/year, $1,728 over 3 years)**

**Pros:**
- ✅ Most graph algorithms (GDS 60+, 2× Memgraph)
- ✅ Best ecosystem (largest community, most integrations, best docs)
- ✅ Most mature (17 years, battle-tested)
- ✅ Cypher query language (most readable)
- ✅ Neo4j Browser web UI included (query editor, visualization)

**Cons:**
- ⚠️ 2× cost vs Memgraph ($48 vs $24/month)
- ⚠️ Some lock-in (GDS proprietary, APOC Neo4j-specific)
- ⚠️ Slower than Memgraph (disk-based vs in-memory)
- ⚠️ Single node only (Community Edition, clustering requires Enterprise $150K+/year)

**Why Alternative:**
- 2× cost vs Memgraph for similar value (30 algorithms sufficient for this use case)
- If need >30 algorithms, Neo4j worth it
- If prefer mature ecosystem, Neo4j worth it

---

### Option 3: Dgraph (Self-Hosted) ❌ NOT RECOMMENDED

**Pricing:**
- DigitalOcean 4GB Droplet: $24/month
- Dgraph: Free (Apache 2.0)
- **Total: $24/month**

**Pros:**
- ✅ Low cost ($24/month, same as Memgraph)
- ✅ Low lock-in (Apache 2.0, open source)
- ✅ GraphQL-native (if building API)

**Cons:**
- ❌ **No graph algorithms** (no PageRank, Louvain, centrality)
- ⚠️ Smaller ecosystem than Neo4j/Memgraph
- ⚠️ DQL proprietary (for advanced queries)

**Why NOT Recommended:**
- **Dealbreaker:** No graph algorithms (primary requirement for this use case)
- Would need to export data and run algorithms in NetworkX (complex ETL)
- Memgraph same cost ($24/month) but includes 30+ algorithms

---

### Option 4: Amazon Neptune Serverless ❌ NOT RECOMMENDED

**Pricing:**
- 1 NCU minimum: $87/month baseline
- 500 nodes, 5K edges, 10K queries/month
- **Total: ~$90-120/month**

**Pros:**
- ✅ AWS-native (IAM, VPC, CloudWatch integration)
- ✅ High availability (multi-AZ, automatic failover)
- ✅ Serverless (auto-scaling)

**Cons:**
- ❌ **No graph algorithms** (Neptune Analytics is $17K/month!)
- ❌ Expensive ($90-120/month vs $24 Memgraph)
- ❌ AWS lock-in (cannot self-host, cannot migrate to other clouds)
- ⚠️ Cold start latency (1-3 seconds if idle >15 min)

**Why NOT Recommended:**
- 4-5× cost vs Memgraph ($90-120 vs $24)
- No algorithms (dealbreaker)
- AWS lock-in not justified for small knowledge graph

---

### Option 5: TigerGraph Cloud ❌ NOT RECOMMENDED

**Pricing:**
- Developer tier: $99/month
- **Total: $99/month**

**Pros:**
- ✅ 30+ graph algorithms (same as Memgraph)
- ✅ Managed service (no ops)

**Cons:**
- ❌ Expensive ($99/month vs $24 Memgraph)
- ❌ Highest lock-in (GSQL 100% proprietary)
- ❌ Overkill (designed for 100M+ nodes, not 500 nodes)

**Why NOT Recommended:**
- 4× cost vs Memgraph ($99 vs $24)
- Highest lock-in (GSQL proprietary, migration = 2-3 months)
- Designed for massive scale (10M+ nodes), not small knowledge graph

---

### Option 6: JanusGraph (Self-Hosted) ❌ NOT RECOMMENDED

**Pricing:**
- JanusGraph: 1 node (8GB) = $50/month
- Cassandra: 1 node (8GB) = $50/month
- **Total: ~$100/month**

**Pros:**
- ✅ Lowest lock-in (Apache open source, Gremlin standard)
- ✅ Proven to trillions of edges (massive scale)

**Cons:**
- ❌ **No graph algorithms** (must build custom)
- ❌ Complex ops (requires Cassandra cluster setup)
- ❌ Overkill (designed for 100M+ nodes, not 500 nodes)
- ❌ 4× cost vs Memgraph ($100 vs $24)

**Why NOT Recommended:**
- No algorithms (dealbreaker)
- Complex ops (3 systems to manage: JanusGraph + Cassandra + Elasticsearch)
- Overkill for small knowledge graph

---

## Final Recommendation

**Winner: Memgraph Community (self-hosted)**

**Reasoning:**
- ✅ Lowest cost ($24/month, $864 over 3 years)
- ✅ Full MAGE algorithms (30+, sufficient for this use case)
- ✅ Low lock-in (openCypher, migrate to Neo4j in 1-2 days if needed)
- ✅ 10× faster than Neo4j (in-memory)
- ✅ Perfect fit for 500 nodes, 5K edges (2-4GB RAM)
- ✅ Memgraph Lab web UI (query editor, visualization)
- ✅ Self-hosted (data sovereignty, no vendor dependency)

**Alternative: Neo4j Community (self-hosted)**
- If need >30 algorithms (Neo4j GDS has 60+)
- If prefer mature ecosystem (more resources, integrations)
- Cost: $48/month (2× Memgraph, but worth it for some use cases)

**3-Year TCO:**
- Memgraph Community: $864
- Neo4j Community: $1,728 (2× Memgraph)
- Neptune Serverless: $4,320 (5× Memgraph)
- TigerGraph Cloud: $3,564 (4× Memgraph)

**Conclusion:** Memgraph Community is the clear winner for this use case (knowledge graph, 500 nodes, <$100/month budget, algorithms critical).

---

## Implementation Plan

**Phase 1: Setup (Week 1)**
1. Deploy Memgraph Community on DigitalOcean 4GB Droplet
2. Load research items from YAML metadata → Cypher LOAD CSV
3. Create relationships (complements, upstream_from, references)
4. Test queries (find complements, dependencies, etc.)

**Phase 2: Algorithms (Week 2)**
1. Run PageRank → Identify most important research items
2. Run Louvain → Discover research clusters
3. Run Betweenness Centrality → Find bridge research items
4. Export results to JSON for reporting

**Phase 3: Automation (Week 3)**
1. Python script to sync YAML metadata → Memgraph
2. Scheduled job (daily/weekly) to update graph
3. Queries for research roadmap planning

**Phase 4: Visualization (Week 4)**
1. Use Memgraph Lab for interactive visualization
2. Export graph to GraphML for external tools (Gephi, Cytoscape)
3. Dashboard for research metrics (completed %, cluster coverage)

**Estimated Effort:** 4 weeks part-time (10-20 hours total)

---

**Next:** Scenario 02 (Social Network Recommendations)
