# S4: Lock-In Mitigation Strategies

**Research Date:** November 16, 2025
**Focus:** Reducing vendor lock-in, maintaining exit options
**Risk Levels:** Low (easy migration) to Highest (2-3 months effort)

---

## Lock-In Spectrum (Lowest to Highest)

| Database | Lock-In Level | Query Language | Migration Effort | Portability |
|----------|---------------|----------------|------------------|-------------|
| **JanusGraph** | Lowest | Gremlin (Apache standard) | 1-2 weeks | High (Gremlin standard) |
| **Memgraph** | Low | openCypher (multi-vendor) | 1-2 weeks | High (→ Neo4j, Neptune) |
| **Dgraph** | Low-Medium | GraphQL (standard), DQL (proprietary) | 1-2 months | Medium (GraphQL portable) |
| **Neo4j** | Medium | Cypher (leader, extensions proprietary) | 1-2 months | Medium (GDS proprietary) |
| **ArangoDB** | High | AQL (proprietary) | 2-3 months | Low (AQL unique) |
| **Neptune** | High | Gremlin/openCypher (AWS-only deployment) | 2-3 months | Medium (query portable, infra not) |
| **TigerGraph** | Highest | GSQL (100% proprietary) | 3-6 months | None (GSQL unique) |

---

## Strategy 1: Use Open Standards (Query Language)

**Goal:** Choose query language with multiple implementations

### High Portability Languages

**Gremlin (Apache TinkerPop):**
- **Implementations:** JanusGraph, Neptune, Cosmos DB (Gremlin API)
- **Portability:** High (Apache standard, multiple vendors)
- **Migration:** JanusGraph ↔ Neptune = 1-2 weeks (query compatible)

**Example:**
```gremlin
g.V().has('User', 'id', '12345')
  .out('FRIENDS_WITH')
  .values('name')
```

**openCypher (Multi-Vendor):**
- **Implementations:** Memgraph, Neo4j (with extensions), Neptune (incomplete)
- **Portability:** High (multi-vendor)
- **Migration:** Memgraph ↔ Neo4j = 1-2 weeks (core Cypher compatible)

**Example:**
```cypher
MATCH (u:User {id: '12345'})-[:FRIENDS_WITH]->(friend)
RETURN friend.name
```

---

### Low Portability Languages

**GSQL (TigerGraph):**
- **Implementations:** TigerGraph only
- **Portability:** None
- **Migration:** GSQL → Cypher/Gremlin = 2-3 months (complete rewrite)

**AQL (ArangoDB):**
- **Implementations:** ArangoDB only
- **Portability:** None
- **Migration:** AQL → Cypher/Gremlin = 2-3 months (complete rewrite)

---

**Recommendation:**
- **Low lock-in:** Use Gremlin (JanusGraph, Neptune) or openCypher (Memgraph)
- **Medium lock-in acceptable:** Cypher (Neo4j, worth it for algorithms)
- **Avoid if lock-in critical:** GSQL (TigerGraph), AQL (ArangoDB)

---

## Strategy 2: Avoid Proprietary Features

**Goal:** Use only standard features, avoid vendor-specific extensions

### Neo4j Lock-In Factors

**Low Lock-In (Standard Cypher):**
```cypher
// Standard Cypher (portable to Memgraph, Neptune openCypher)
MATCH (a)-[:RELATIONSHIP]->(b)
RETURN a, b
```

**Medium Lock-In (GDS Algorithms):**
```cypher
// Neo4j GDS (proprietary, not portable)
CALL gds.pageRank.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name, score
```

**High Lock-In (APOC Procedures):**
```cypher
// APOC (Neo4j-specific utilities, not portable)
CALL apoc.periodic.iterate(
  "MATCH (n) RETURN n",
  "SET n.updated = timestamp()",
  {batchSize: 1000}
)
```

---

**Mitigation:**
1. **Use core Cypher only** (avoid APOC, GDS if portability critical)
2. **Abstract algorithms externally** (export graph → NetworkX → run algorithms)
3. **Document proprietary usage** (track APOC, GDS usage for migration planning)

**Trade-Off:**
- Low lock-in (core Cypher only) = less features
- Accept lock-in (GDS, APOC) = more features, faster development
- **Verdict:** Accept GDS lock-in if algorithms critical (worth it)

---

## Strategy 3: Regular Exports (Data Portability)

**Goal:** Maintain ability to migrate by exporting data regularly

### Export Formats

**CSV (Universal):**
```bash
# Neo4j: Export nodes + edges to CSV
CALL apoc.export.csv.all("graph-export.csv", {})

# Memgraph: Export to CSV
EXPORT DATABASE TO '/backup/graph.csv'
```

**JSON (Flexible):**
```bash
# Export to JSON
CALL apoc.export.json.all("graph-export.json", {})
```

**GraphML (Graph Standard):**
```bash
# Export to GraphML (standard format)
CALL apoc.export.graphml.all("graph-export.graphml", {})
```

---

**Best Practice:**
- **Daily exports:** CSV/JSON to S3/GCS (backup + migration readiness)
- **Weekly exports:** GraphML (standard format for migration)
- **Test restore:** Quarterly (ensure exports valid)

**Storage Cost:**
- 1M nodes, 5M edges ≈ 1GB export
- S3 cost: $0.023/GB/month = $0.02/month
- **Negligible cost, high migration insurance**

---

## Strategy 4: Abstraction Layer (Application Code)

**Goal:** Isolate database-specific code, easier to swap databases

### Repository Pattern (Code Abstraction)

**Bad (Database-Specific):**
```python
# Direct Neo4j driver usage (high lock-in)
from neo4j import GraphDatabase

def get_friends(user_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User {id: $id})-[:FRIENDS_WITH]->(f) RETURN f",
            id=user_id
        )
        return [record["f"] for record in result]
```

**Good (Abstraction Layer):**
```python
# Abstract repository interface
class GraphRepository:
    def get_friends(self, user_id): pass

class Neo4jRepository(GraphRepository):
    def get_friends(self, user_id):
        # Neo4j-specific implementation
        ...

class MemgraphRepository(GraphRepository):
    def get_friends(self, user_id):
        # Memgraph-specific implementation (same as Neo4j, openCypher)
        ...

# Application uses interface, not specific DB
repo = get_repository()  # Factory returns Neo4j or Memgraph
friends = repo.get_friends(user_id)
```

---

**Trade-Off:**
- **Abstraction layer:** 20-30% slower development (extra layer)
- **Direct driver:** 20-30% faster development, but high lock-in
- **Recommendation:** Use abstraction layer if lock-in critical, direct driver if speed matters more

---

## Strategy 5: Self-Hosting Option

**Goal:** Maintain ability to self-host, avoid managed-only lock-in

### Self-Hosting Availability

| Database | Self-Hosting | License | Exit Path |
|----------|--------------|---------|-----------|
| **Neo4j** | ✅ Community Edition | GPLv3 (free) | Easy (Docker, 1-2 days setup) |
| **Memgraph** | ✅ Community Edition | BSL (free) | Easy (Docker, 1-2 days setup) |
| **JanusGraph** | ✅ Open Source | Apache 2.0 | Medium (multi-cluster, 1-2 weeks) |
| **Dgraph** | ✅ Open Source | Apache 2.0 | Easy (Docker, 1-2 days setup) |
| **ArangoDB** | ✅ Community Edition | Apache 2.0 | Easy (Docker, 1-2 days setup) |
| **TigerGraph** | ⚠️ Enterprise Only | Proprietary (license) | Hard (license required, $50K+/year) |
| **Neptune** | ❌ Managed Only | AWS proprietary | None (AWS-only) |

---

**Mitigation:**
- **Prefer databases with self-hosting** (Neo4j, Memgraph, JanusGraph, Dgraph, ArangoDB)
- **Avoid managed-only** (Neptune) if lock-in critical
- **Test self-hosting annually** (fire drill, ensure exit path viable)

**Cost Comparison (1M nodes):**
- **Managed:** $240-800/month (Neo4j Aura, Memgraph Cloud)
- **Self-hosted:** $84-212/month (infrastructure only)
- **Savings:** 60-75% (managed premium = 2-5×)

**When Self-Hosting Worth It:**
- Budget >$500/month (savings justify ops cost)
- Strong ops team (can manage infrastructure)
- Compliance (data sovereignty, air-gapped)

---

## Strategy 6: Multi-Cloud Strategy

**Goal:** Deploy on multiple clouds, avoid cloud lock-in

**Multi-Cloud Providers:**
- **Neo4j Aura:** AWS, GCP, Azure ✅
- **Memgraph Cloud:** AWS, GCP, Azure ✅
- **TigerGraph Cloud:** AWS, GCP, Azure ✅
- **ArangoDB Cloud:** AWS, GCP, Azure ✅
- **Neptune:** AWS only ❌
- **Cosmos DB:** Azure only ❌

---

**Mitigation:**
- **Choose multi-cloud vendors** (Neo4j, Memgraph, TigerGraph, ArangoDB)
- **Avoid cloud-specific** (Neptune AWS-only, Cosmos DB Azure-only)
- **Test cross-cloud migration** (AWS → GCP) annually

**Trade-Off:**
- **Multi-cloud:** Avoid lock-in, but higher complexity
- **Cloud-specific:** Better integration (IAM, VPC), but lock-in

**Recommendation:**
- **Startups (0-3 years):** Accept cloud lock-in (speed > portability)
- **Scale-ups (3-5 years):** Multi-cloud preferred
- **Enterprises (5-10 years):** Multi-cloud required (leverage in negotiations)

---

## Lock-In Mitigation Summary

| Strategy | Effort | Impact | Recommended For |
|----------|--------|--------|-----------------|
| **Use open standards (Gremlin, openCypher)** | Low | High | All projects |
| **Avoid proprietary features** | Medium | Medium | Lock-in critical projects |
| **Regular exports (CSV, GraphML)** | Low | High | All projects (always do this) |
| **Abstraction layer** | High | Medium | Large projects (>1 year) |
| **Self-hosting option** | Medium | High | Enterprises, compliance |
| **Multi-cloud strategy** | Medium | Medium | Scale-ups, enterprises |

---

## Recommended Approach by Company Stage

### Startups (0-3 Years)

**Accept Lock-In for Speed:**
- Use managed services (Neo4j Aura, Memgraph Cloud, TigerGraph Cloud)
- Accept proprietary features (Neo4j GDS, TigerGraph GSQL if needed)
- Focus on shipping features, not portability

**Minimal Mitigation:**
- ✅ Regular exports (CSV to S3) - always do this
- ⚠️ Self-hosting fire drill (annually) - optional
- ❌ Abstraction layer - skip (slows development)

**Migration Trigger:**
- Monthly cost >$3,000 (re-evaluate self-hosting)
- Vendor viability concerns (acquisition, price increases)

---

### Scale-Ups (3-5 Years)

**Monitor Lock-In, Prepare Exit:**
- Use managed services (faster shipping) but test self-hosting annually
- Abstraction layer for core queries (isolate vendor-specific code)
- Regular exports (daily CSV + weekly GraphML)

**Moderate Mitigation:**
- ✅ Regular exports (daily)
- ✅ Abstraction layer (for core CRUD)
- ✅ Test self-hosting annually (fire drill)
- ⚠️ Multi-cloud - only if corporate mandate

**Migration Triggers:**
- Monthly cost >$5,000 (evaluate self-hosting)
- Vendor acquisition (price increase risk)
- Compliance requirements (data sovereignty)

---

### Enterprises (5-10 Years)

**Maintain Exit Options:**
- Self-host or multi-cloud managed (avoid single cloud lock-in)
- Open standards only (Gremlin, openCypher)
- Abstraction layer (all database access)
- Regular exports + restore testing (quarterly)

**Maximum Mitigation:**
- ✅ Open standards (Gremlin, openCypher)
- ✅ Regular exports (daily + weekly + monthly to multiple clouds)
- ✅ Abstraction layer (all database code)
- ✅ Self-host fire drills (quarterly)
- ✅ Multi-cloud deployment
- ✅ Contractual guarantees (data export, pricing caps)

**Migration Approach:**
- Plan migration every 3-5 years (technology refresh cycle)
- Budget for migration (6-12 months effort)
- Use migrations as leverage (renegotiate with vendor)

---

**Next:** Migration Complexity Matrix
