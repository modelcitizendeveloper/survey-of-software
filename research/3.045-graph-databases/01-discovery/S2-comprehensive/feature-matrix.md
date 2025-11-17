# S2: Feature Matrix - Graph Databases

**Research Date:** November 16, 2025
**Providers:** 7 (Neo4j Aura, Amazon Neptune, Memgraph, JanusGraph, ArangoDB, TigerGraph, Dgraph)
**Features Analyzed:** 50+

---

## Feature Matrix (Core Capabilities)

| Feature | Neo4j Aura | Neptune | Memgraph | JanusGraph | ArangoDB | TigerGraph | Dgraph |
|---------|------------|---------|----------|------------|----------|------------|--------|
| **Query Language** | Cypher | Gremlin, openCypher, SPARQL | Cypher | Gremlin | AQL | GSQL | GraphQL, DQL |
| **Open Source** | ✅ (Community) | ❌ | ✅ (Community) | ✅ | ✅ (Community) | ❌ | ✅ |
| **License** | GPLv3 | Proprietary | BSL | Apache 2.0 | Apache 2.0 | Proprietary | Apache 2.0 |
| **Self-Hosting** | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ (Enterprise) | ✅ |
| **Managed Cloud** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| **Free Tier** | ✅ | ❌ | ❌ (trial) | N/A | ✅ | ❌ (trial) | ✅ |
| **Serverless** | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## Graph Algorithms

| Algorithm Category | Neo4j | Neptune | Memgraph | JanusGraph | ArangoDB | TigerGraph | Dgraph |
|--------------------|-------|---------|----------|------------|----------|------------|--------|
| **Total Algorithms** | 60+ | 0* | 30+ | 0 | <10 | 30+ | 0 |
| **Centrality** | ✅ (8+) | ❌ | ✅ (5+) | ❌ | ⚠️ (2) | ✅ (5+) | ❌ |
| **Community Detection** | ✅ (6+) | ❌ | ✅ (4+) | ❌ | ❌ | ✅ (4+) | ❌ |
| **Path Finding** | ✅ (8+) | ❌ | ✅ (5+) | ❌ | ✅ (3) | ✅ (5+) | ❌ |
| **Similarity** | ✅ (5+) | ❌ | ✅ (4+) | ❌ | ❌ | ✅ (3+) | ❌ |
| **Link Prediction** | ✅ (4+) | ❌ | ✅ (3+) | ❌ | ❌ | ✅ (2+) | ❌ |
| **Graph ML** | ✅ (GNN) | ⚠️ (Neptune ML) | ✅ (Node2Vec) | ❌ | ❌ | ✅ | ❌ |

*Neptune has Neptune Analytics (separate service, $1.50/GB RAM/hour = $17K/month for 16GB)

**Key Insight:**
- **Algorithms Leaders:** Neo4j (60+), Memgraph (30+), TigerGraph (30+)
- **No Algorithms:** Neptune, JanusGraph, Dgraph (must build custom)
- **Limited:** ArangoDB (<10 basic algorithms)

---

## Performance Characteristics

| Metric | Neo4j | Neptune | Memgraph | JanusGraph | ArangoDB | TigerGraph | Dgraph |
|--------|-------|---------|----------|------------|----------|------------|--------|
| **Architecture** | Disk-based | Disk-based | In-memory | Disk-based | Disk-based | Distributed MPP | Distributed |
| **Latency (1-hop)** | 1-5ms | 2-10ms | <1ms | 5-20ms | 2-10ms | 1-5ms | 1-5ms |
| **Latency (3-hop)** | 10-50ms | 20-100ms | 2-10ms | 50-200ms | 20-100ms | 10-50ms | 10-50ms |
| **Latency (10-hop)** | 100-500ms | 200-1000ms | 20-100ms | 500-2000ms | 200-1000ms | 50-200ms | 50-200ms |
| **Throughput (reads)** | 1-5K qps | 0.5-2K qps | 10-50K qps | 0.5-2K qps | 1-5K qps | 5-20K qps | 2-10K qps |
| **Throughput (writes)** | 100-500 wps | 100-300 wps | 100-500 wps | 1-10K wps | 500-2K wps | 1-10K wps | 1-5K wps |
| **Max Single Node** | 768GB RAM | 1024GB RAM | 1TB+ RAM | Backend-limited | 512GB RAM | Distributed | Distributed |

**Key Insight:**
- **Fastest:** Memgraph (in-memory, <1ms queries)
- **Slowest:** JanusGraph (backend latency overhead)
- **Best for deep traversal:** Memgraph, TigerGraph (optimized)
- **Best for writes:** JanusGraph (Cassandra backend), TigerGraph (distributed)

---

## Scalability

| Feature | Neo4j | Neptune | Memgraph | JanusGraph | ArangoDB | TigerGraph | Dgraph |
|---------|-------|---------|----------|------------|----------|------------|--------|
| **Horizontal Scaling** | ⚠️ (Enterprise) | ✅ (replicas) | ⚠️ (Enterprise) | ✅ | ✅ | ✅ | ✅ |
| **Clustering** | ⚠️ (Enterprise) | ✅ (built-in) | ⚠️ (Enterprise) | ✅ | ✅ | ✅ | ✅ |
| **Read Replicas** | ✅ | ✅ (15 max) | ⚠️ (Enterprise) | ✅ | ✅ | ✅ | ✅ |
| **Multi-Region** | ⚠️ (Enterprise) | ✅ | ⚠️ (Enterprise) | ✅ (via backend) | ✅ | ✅ | ✅ |
| **Proven Scale** | 100B edges | 100B edges | 10B edges | 1T+ edges | 100B edges | 100B+ edges | 100B edges |

**Key Insight:**
- **Best for massive scale:** JanusGraph (trillions of edges proven), TigerGraph (100B+)
- **Community limitations:** Neo4j, Memgraph (single node only, clustering requires Enterprise)
- **Cloud-native scaling:** Neptune (AWS-managed), TigerGraph (distributed MPP)

---

## Query Language Features

| Feature | Neo4j (Cypher) | Neptune (Gremlin/openCypher) | Memgraph (Cypher) | JanusGraph (Gremlin) | ArangoDB (AQL) | TigerGraph (GSQL) | Dgraph (GraphQL/DQL) |
|---------|----------------|------------------------------|-------------------|----------------------|----------------|-------------------|----------------------|
| **Standard** | openCypher | Apache TinkerPop / openCypher | openCypher | Apache TinkerPop | Proprietary | Proprietary | GraphQL / Proprietary |
| **Readability** | Excellent | Medium / Good | Excellent | Medium | Good | Medium | Excellent |
| **Portability** | Medium | High / Medium | High | High | Low | None | Medium |
| **Pattern Matching** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Variable-Length Paths** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Aggregations** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Subqueries** | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ⚠️ |
| **Procedures/UDFs** | ✅ (APOC) | ❌ | ✅ (custom) | ❌ | ✅ (Foxx) | ✅ | ❌ |

**Key Insight:**
- **Most portable:** Gremlin (Apache standard), openCypher (multi-vendor)
- **Most readable:** Cypher (Neo4j, Memgraph), GraphQL (Dgraph)
- **Least portable:** AQL (ArangoDB), GSQL (TigerGraph)

---

## Developer Experience

| Feature | Neo4j | Neptune | Memgraph | JanusGraph | ArangoDB | TigerGraph | Dgraph |
|---------|-------|---------|----------|------------|----------|------------|--------|
| **Web UI** | ✅ (Browser) | ⚠️ (Workbench) | ✅ (Lab) | ❌ | ✅ (Web UI) | ✅ (GraphStudio) | ✅ (Ratel) |
| **Visual Query Builder** | ⚠️ (Bloom, paid) | ❌ | ❌ | ❌ | ⚠️ (basic) | ✅ (GraphStudio) | ❌ |
| **Docker Image** | ✅ | N/A | ✅ | ✅ | ✅ | N/A | ✅ |
| **Client Libraries** | 10+ languages | 10+ languages | 8+ languages | 5+ languages | 10+ languages | 8+ languages | 10+ languages |
| **Documentation Quality** | Excellent | Good | Good | Fair | Good | Good | Good |
| **Community Size** | Large (1M+) | Medium | Growing (50K+) | Small (10K+) | Medium (100K+) | Small (10K+) | Medium (50K+) |
| **StackOverflow Questions** | 15K+ | 2K+ | 500+ | 1K+ | 3K+ | 200+ | 800+ |

**Key Insight:**
- **Best DX:** Neo4j (best docs, largest community, most integrations)
- **Best for beginners:** Dgraph (GraphQL-native, frontend-friendly), Neo4j (Cypher readability)
- **Weakest DX:** JanusGraph (complex setup, smaller community)

---

## Integrations

| Integration | Neo4j | Neptune | Memgraph | JanusGraph | ArangoDB | TigerGraph | Dgraph |
|-------------|-------|---------|----------|------------|----------|------------|--------|
| **Apache Spark** | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ❌ |
| **Kafka/Streaming** | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ⚠️ |
| **Elasticsearch** | ⚠️ (manual) | ⚠️ (manual) | ⚠️ (manual) | ✅ (native) | ⚠️ (manual) | ⚠️ (manual) | ⚠️ (manual) |
| **PostgreSQL** | ⚠️ (ETL) | ⚠️ (ETL) | ⚠️ (ETL) | ⚠️ (ETL) | ⚠️ (ETL) | ⚠️ (ETL) | ⚠️ (ETL) |
| **Python Libraries** | ✅ (neo4j, py2neo) | ✅ (gremlinpython) | ✅ (pymgclient) | ✅ (gremlinpython) | ✅ (pyArango) | ✅ (pyTigerGraph) | ✅ (pydgraph) |
| **GraphQL** | ⚠️ (plugin) | ❌ | ⚠️ (custom) | ❌ | ⚠️ (custom) | ❌ | ✅ (native) |
| **Prometheus** | ✅ | ✅ (CloudWatch) | ✅ | ✅ | ✅ | ✅ | ✅ |

**Key Insight:**
- **Best integrations:** Neo4j (largest ecosystem), JanusGraph (Elasticsearch native)
- **Best for streaming:** Memgraph (Kafka native), TigerGraph (real-time)
- **Best for API-first:** Dgraph (GraphQL native)

---

## Security & Compliance

| Feature | Neo4j | Neptune | Memgraph | JanusGraph | ArangoDB | TigerGraph | Dgraph |
|---------|-------|---------|----------|------------|----------|------------|--------|
| **Authentication** | ✅ | ✅ (IAM) | ⚠️ (Enterprise) | ⚠️ (plugin) | ✅ | ✅ | ✅ |
| **RBAC** | ✅ | ✅ (IAM) | ⚠️ (Enterprise) | ❌ | ✅ | ✅ | ⚠️ (ACL) |
| **Encryption at Rest** | ✅ | ✅ | ⚠️ (Enterprise) | ⚠️ (backend) | ✅ | ✅ | ✅ |
| **Encryption in Transit** | ✅ (TLS) | ✅ (TLS) | ✅ (TLS) | ✅ (TLS) | ✅ (TLS) | ✅ (TLS) | ✅ (TLS) |
| **Audit Logs** | ⚠️ (Enterprise) | ✅ (CloudTrail) | ⚠️ (Enterprise) | ❌ | ✅ | ✅ | ⚠️ |
| **SOC 2** | ✅ (Aura) | ✅ | ⚠️ (Cloud) | N/A | ✅ (Cloud) | ✅ | ⚠️ (Cloud) |
| **HIPAA** | ✅ (Aura) | ✅ | ⚠️ | N/A | ⚠️ | ⚠️ | ❌ |
| **GDPR** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Key Insight:**
- **Best for compliance:** Neo4j Aura (SOC 2, HIPAA), Neptune (AWS compliance)
- **Enterprise features locked:** Neo4j, Memgraph (RBAC, audit logs require Enterprise)
- **Open source security:** JanusGraph limited (must build custom)

---

## Backup & Recovery

| Feature | Neo4j | Neptune | Memgraph | JanusGraph | ArangoDB | TigerGraph | Dgraph |
|---------|-------|---------|----------|------------|----------|------------|--------|
| **Automated Backups** | ✅ (Aura) | ✅ | ✅ (Cloud) | ❌ (DIY) | ✅ (Cloud) | ✅ | ✅ (Cloud) |
| **Point-in-Time Recovery** | ✅ (Aura) | ✅ (5 min) | ⚠️ (Enterprise) | ❌ | ✅ | ✅ | ⚠️ |
| **Hot Backups** | ⚠️ (Enterprise) | ✅ | ⚠️ (Enterprise) | ⚠️ (backend) | ✅ | ✅ | ✅ |
| **Export Formats** | CSV, JSON, Cypher | CSV, JSON, Gremlin | CSV, JSON, Cypher | GraphML, JSON | JSON, JSONL | CSV, JSON | RDF, JSON |
| **Backup to S3** | ✅ | ✅ (automatic) | ⚠️ (manual) | ⚠️ (manual) | ✅ | ✅ | ⚠️ (manual) |

**Key Insight:**
- **Best backups:** Neptune (AWS-managed, PITR), Neo4j Aura (automatic)
- **DIY backups:** JanusGraph (backend snapshots), Memgraph Community (manual)
- **Hotbackups locked:** Neo4j, Memgraph (require Enterprise for zero-downtime)

---

## Summary: Feature Coverage

**Algorithm-Rich:** Neo4j (60+), Memgraph (30+), TigerGraph (30+)
**Fastest:** Memgraph (in-memory, <1ms latency)
**Most Portable:** JanusGraph (Gremlin), Memgraph (openCypher)
**Best DX:** Neo4j (largest ecosystem), Dgraph (GraphQL-native)
**Cloud-Native:** Neptune (AWS), TigerGraph (distributed MPP)
**Best for Small Scale:** Memgraph Community, Neo4j Community, Dgraph
**Best for Massive Scale:** JanusGraph (trillions of edges), TigerGraph (100B+)

---

**Next:** Pricing TCO (Total Cost of Ownership analysis)
