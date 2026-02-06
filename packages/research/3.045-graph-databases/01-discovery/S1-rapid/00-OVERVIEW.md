# S1: Graph Databases Overview

**Research Date:** November 16, 2025
**Focus:** Specialized graph database platforms (deeper than 3.041 NoSQL coverage)
**Primary Use Case:** Knowledge graph for research project relationships
**Key Goal:** Avoid Neo4j lock-in while evaluating graph database options

---

## What Makes Graph Databases Different?

Graph databases are optimized for **relationship-heavy data** where traversing connections is the primary operation. Unlike relational databases (joins are expensive) or document databases (relationships are foreign keys), graph databases store relationships as first-class citizens.

**Core Concepts:**
- **Nodes:** Entities (e.g., research items, people, companies)
- **Edges:** Relationships between nodes (e.g., "complements", "upstream_from", "references")
- **Properties:** Attributes on nodes and edges (e.g., date, strength, type)

**Query Pattern:**
```cypher
// Find all research items that complement 3.041 and their dependencies
MATCH (item:Research {code: "3.041"})-[:COMPLEMENTS]-(related)-[:UPSTREAM_FROM*1..3]-(dependency)
RETURN related, dependency
```

This query traverses multiple hops efficiently—something SQL joins struggle with beyond 2-3 levels.

---

## Graph Database Landscape (2025)

### Market Leaders (Established)
1. **Neo4j** - 15+ years, market leader, Cypher query language, $200M+ revenue
2. **Amazon Neptune** - AWS-native, supports Gremlin + openCypher, serverless option

### Growth Category (Emerging)
3. **Memgraph** - In-memory, Cypher-compatible, fast growing
4. **TigerGraph** - Enterprise analytics focus, GSQL query language
5. **ArangoDB** - Multi-model (graph + document + key-value)

### Open Source Options
6. **JanusGraph** - Apache project, Gremlin, highly scalable, self-hosted
7. **Dgraph** - GraphQL-native, open source, distributed

---

## Query Language Landscape

### Cypher (Neo4j Standard)
- **Who uses it:** Neo4j, Memgraph, Amazon Neptune (openCypher)
- **Syntax:** ASCII art style, human-readable
- **Example:**
```cypher
MATCH (a:Person)-[:FRIENDS_WITH]->(b:Person)
WHERE a.name = "Alice"
RETURN b.name
```
- **Portability:** openCypher specification allows some portability (Neo4j → Memgraph → Neptune)

### Gremlin (Apache TinkerPop)
- **Who uses it:** Amazon Neptune, JanusGraph, Azure Cosmos DB (Gremlin API)
- **Syntax:** Functional/traversal style
- **Example:**
```gremlin
g.V().has('Person', 'name', 'Alice').out('FRIENDS_WITH').values('name')
```
- **Portability:** High (industry standard, multiple implementations)

### AQL (ArangoDB Query Language)
- **Who uses it:** ArangoDB only
- **Syntax:** SQL-like with graph extensions
- **Portability:** Low (ArangoDB-specific)

### GSQL (TigerGraph)
- **Who uses it:** TigerGraph only
- **Syntax:** Procedural, SQL-inspired
- **Portability:** None (TigerGraph-specific)

### GraphQL (Dgraph)
- **Who uses it:** Dgraph, general API layer
- **Syntax:** GraphQL standard
- **Portability:** Medium (GraphQL is universal, but Dgraph's implementation is specific)

---

## Lock-In Spectrum (Lowest to Highest)

**Lowest Lock-In:**
1. **JanusGraph** (open source, Gremlin standard, self-hosted)
2. **Memgraph** (openCypher, self-hosted option, Cypher-compatible)
3. **Amazon Neptune** (openCypher + Gremlin, but AWS-specific)

**Medium Lock-In:**
4. **Neo4j Aura** (Cypher leader, but Community Edition self-host option exists)
5. **Dgraph** (open source, but GraphQL implementation is specific)

**Higher Lock-In:**
6. **ArangoDB** (AQL proprietary, multi-model complexity)
7. **TigerGraph** (GSQL proprietary, enterprise licensing)

---

## Pricing Tiers (Managed Services)

**Free Tier Available:**
- Neo4j Aura: Free tier (50k nodes, 175k relationships)
- Memgraph Cloud: Free trial (14 days)
- Dgraph Cloud: Free tier (1GB)

**Serverless Pricing:**
- Amazon Neptune Serverless: Pay-per-request (NCUs)
- Neo4j Aura: Pay-per-hour (capacity units)

**Provisioned Pricing:**
- Neo4j Aura Professional: $65-500+/month
- Memgraph Cloud: $49-1,000+/month
- TigerGraph Cloud: $99-2,000+/month
- ArangoDB Cloud: $20-500+/month

**Self-Hosted:**
- Neo4j Community Edition: Free (single node, limited features)
- Neo4j Enterprise: $150K+/year (clustering, advanced features)
- JanusGraph: Free (open source, but infra costs $100-1,000+/month)
- Memgraph: Free (Community Edition)
- Dgraph: Free (open source)

---

## Use Case: Knowledge Graph for Research Project

**Scenario:**
Represent research project as graph database to explore relationships and dependencies.

**Data Model:**
```
Nodes:
- Research item (code, title, tier, status)
- Technology (name, category)
- Provider (name, type)

Edges:
- COMPLEMENTS (research A complements research B)
- UPSTREAM_FROM (research A is upstream from B - must do A before B)
- REFERENCES (research A references research B)
- INTEGRATES_WITH (technology A integrates with technology B)
- ANALYZES (research analyzes provider/technology)
```

**Sample Queries:**
1. "Find all research items that complement 3.041 NoSQL Databases"
2. "What research items must be completed before 3.007 FP&A Platforms?"
3. "Identify clusters of related research (community detection)"
4. "Find the most referenced research items (PageRank/centrality)"
5. "Discover gaps: which technologies have no research coverage?"

**Scale:**
- Nodes: 100-500 (research items, technologies, providers)
- Edges: 500-5,000 (relationships)
- Growth: +50 nodes/year, +200 edges/year

**Requirements:**
- Low lock-in (avoid Neo4j Premium pricing)
- Self-hosting option preferred (data sovereignty)
- Graph algorithms (PageRank, centrality, community detection)
- Reasonable cost (<$50/month managed or <$100/month self-hosted)

---

## Key Evaluation Criteria

### 1. Query Language Portability
- **High:** Gremlin (Apache standard), openCypher (multi-vendor)
- **Medium:** Cypher (Neo4j dominant, but Memgraph compatible)
- **Low:** AQL, GSQL, proprietary extensions

### 2. Self-Hosting Viability
- **Easy:** Neo4j Community, Memgraph, JanusGraph, Dgraph (Docker images, docs)
- **Medium:** Neo4j Enterprise (licensing complexity)
- **Hard:** Managed-only services (Neptune, TigerGraph Cloud)

### 3. Graph Algorithms
- **Rich:** Neo4j GDS (60+ algorithms), TigerGraph (built-in analytics)
- **Good:** Memgraph MAGE (algorithms library), JanusGraph (via plugins)
- **Basic:** Neptune (limited built-in), ArangoDB (community algorithms)
- **None:** Dgraph (must implement custom)

### 4. Cost at Scale (100-500 nodes, 500-5K edges)
- **Cheapest:** Self-hosted JanusGraph, Memgraph, Dgraph ($0-100/month infra)
- **Low:** Neo4j Community self-hosted ($50-100/month infra)
- **Medium:** ArangoDB Cloud ($20-80/month), Memgraph Cloud ($49-99/month)
- **High:** Neo4j Aura Professional ($65-200/month), Neptune ($100-300/month)
- **Highest:** TigerGraph Cloud ($99-500/month)

### 5. Performance (Traversal Speed)
- **Fastest:** Memgraph (in-memory, <1ms queries), Neo4j (optimized index)
- **Fast:** TigerGraph (distributed), Dgraph (distributed)
- **Medium:** JanusGraph (depends on backend), ArangoDB (multi-model overhead)
- **Slower:** Neptune (serverless cold start latency)

---

## Recommendations by Use Case

### Knowledge Graph (Research Project)
**Recommended:** Memgraph Community (self-hosted) or Neo4j Community (self-hosted)
- **Reason:** Low lock-in, Cypher compatibility, self-hosted cost ~$50/month, rich algorithms
- **Avoid:** Neo4j Aura (expensive at scale), TigerGraph (proprietary GSQL)

### Social Network (Millions of Users)
**Recommended:** Neo4j Enterprise or TigerGraph
- **Reason:** Proven at scale (LinkedIn uses Neo4j, large enterprises use TigerGraph)

### AWS Ecosystem
**Recommended:** Amazon Neptune
- **Reason:** Best AWS integration, serverless option, IAM integration

### Real-Time Analytics
**Recommended:** Memgraph
- **Reason:** In-memory, <1ms query latency, streaming data integration

### Multi-Model Needs (Graph + Documents)
**Recommended:** ArangoDB
- **Reason:** One database for graph, document, and key-value workloads

---

## Next Steps: S1 Provider Profiles

Detailed analysis of 7 graph database platforms:
1. Neo4j Aura (market leader, baseline)
2. Amazon Neptune (AWS managed)
3. ArangoDB (multi-model)
4. TigerGraph (enterprise analytics)
5. Memgraph (in-memory, Cypher-compatible)
6. JanusGraph (open source, Gremlin)
7. Dgraph (GraphQL-native)

Each profile includes: pricing, query language, algorithms, self-hosting, lock-in assessment.
