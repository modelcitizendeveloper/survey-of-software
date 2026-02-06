# S4: Migration Complexity Matrix

**Research Date:** November 16, 2025
**Focus:** Effort to switch between graph database providers
**Factors:** Data export/import, query rewrite, downtime, testing

---

## Migration Complexity Levels

| Complexity | Timeframe | Characteristics | Example |
|------------|-----------|-----------------|---------|
| **Low** | 1-2 weeks | Same query language, API-compatible | Memgraph → Neo4j (openCypher) |
| **Medium** | 1-2 months | Partial query rewrite, some features lost | Neo4j → Neptune (Cypher → openCypher) |
| **High** | 2-3 months | Complete query rewrite, data model changes | Neo4j → JanusGraph (Cypher → Gremlin) |
| **Very High** | 3-6 months | Proprietary language, architecture changes | TigerGraph → Any (GSQL proprietary) |

---

## Low Complexity Migrations (1-2 Weeks)

### Memgraph ↔ Neo4j (openCypher Compatible)

**Compatibility:** 95%+ (core Cypher portable)

**Process:**
```bash
# 1. Export from Memgraph
EXPORT DATABASE TO '/backup/graph.csv'

# 2. Import to Neo4j
neo4j-admin import \
  --nodes=/backup/nodes.csv \
  --relationships=/backup/relationships.csv

# 3. Update application (connection string only)
# Old: bolt://memgraph-host:7687
# New: bolt://neo4j-host:7687

# 4. Test queries (most work unchanged)
```

**Downtime:** <4 hours (data transfer + testing)

**Application Changes:**
- Connection string update
- Remove Memgraph-specific features (MAGE → Neo4j GDS translation)

**Effort:** 1-2 weeks (mostly testing edge cases)

---

### JanusGraph ↔ Neptune (Gremlin Standard)

**Compatibility:** 90%+ (Apache TinkerPop standard)

**Process:**
```bash
# 1. Export from JanusGraph (Gremlin scripts)
g.V().toList()  // Export to JSON
g.E().toList()  // Export edges

# 2. Import to Neptune (bulk loader)
aws neptune-loader load \
  --source s3://bucket/graph-export.json \
  --format opencypher

# 3. Update application (endpoint only)
# Old: janusgraph-host:8182
# New: neptune-endpoint:8182
```

**Downtime:** 2-8 hours (depending on data size)

**Effort:** 1-2 weeks

---

## Medium Complexity Migrations (1-2 Months)

### Neo4j → Neptune (Cypher → openCypher)

**Compatibility:** 80% (Neptune openCypher incomplete)

**Missing Features in Neptune openCypher:**
- ❌ APOC procedures (Neo4j-specific)
- ❌ GDS algorithms (Neo4j proprietary)
- ⚠️ Advanced Cypher (FOREACH, some MERGE edge cases)

**Process:**
```bash
# 1. Export from Neo4j
CALL apoc.export.csv.all("graph-export.csv", {})

# 2. Transform queries (Cypher → Neptune-compatible openCypher)
# Manual rewrite of APOC, GDS usage
# Test each query for Neptune compatibility

# 3. Import to Neptune
aws neptune-loader load \
  --source s3://bucket/graph-export.csv \
  --format csv

# 4. Reimplement algorithms (GDS → Neptune ML or external)
# Export → Python NetworkX → Neptune
```

**Downtime:** 4-12 hours (cutover period)

**Effort:** 1-2 months (query rewrite + algorithm reimplementation)

**Cost:** 40-80 hours engineering time = $20K-40K

---

### Memgraph → DGraph (Cypher → GraphQL/DQL)

**Compatibility:** Low (different paradigms)

**Process:**
```bash
# 1. Export from Memgraph
EXPORT DATABASE TO '/backup/graph.json'

# 2. Transform data model (property graph → GraphQL schema)
# Define GraphQL types, relationships

# 3. Import to Dgraph (bulk load)
dgraph live -f /backup/graph.json

# 4. Rewrite queries (Cypher → GraphQL)
# MATCH (u:User)-[:FRIENDS_WITH]->(f)
# → GraphQL: { getUser(id: "...") { friends { id name } } }
```

**Effort:** 1-2 months (data model + query rewrite)

---

## High Complexity Migrations (2-3 Months)

### Neo4j → JanusGraph (Cypher → Gremlin)

**Compatibility:** None (different query languages)

**Process:**
```bash
# 1. Export from Neo4j (CSV)
CALL apoc.export.csv.all("graph-export.csv", {})

# 2. Setup JanusGraph cluster (complex)
# Deploy JanusGraph + Cassandra + Elasticsearch (3 systems)

# 3. Import data
# Use Gremlin scripts or bulk loader

# 4. Rewrite ALL queries (Cypher → Gremlin)
# MATCH (a)-[:REL]->(b) RETURN a, b
# → g.V().outE('REL').inV().path()

# 5. Reimplement algorithms (Neo4j GDS → custom or NetworkX)
```

**Downtime:** 8-24 hours (cutover + validation)

**Effort:** 2-3 months (query rewrite + cluster setup + testing)

**Cost:** 160-240 hours engineering = $80K-120K

---

### Neo4j/Memgraph → ArangoDB (Cypher → AQL)

**Compatibility:** None (AQL proprietary)

**Process:**
- Export from Neo4j/Memgraph (CSV/JSON)
- Transform data model (property graph → ArangoDB collections)
- Rewrite ALL queries (Cypher → AQL)
- Test extensively (AQL syntax completely different)

**Effort:** 2-3 months

---

## Very High Complexity Migrations (3-6 Months)

### TigerGraph → Any Database (GSQL Proprietary)

**Compatibility:** None (GSQL 100% proprietary)

**Process:**
```bash
# 1. Export from TigerGraph (CSV)
# Custom export scripts (GSQL)

# 2. Redesign data model
# TigerGraph schema → target database schema

# 3. Rewrite ALL queries (GSQL → Cypher/Gremlin)
# Complex procedural GSQL → declarative Cypher
# 100% rewrite required

# 4. Reimplement ALL algorithms
# TigerGraph built-in → Neo4j GDS or custom

# 5. Extensive testing (6-8 weeks)
```

**Downtime:** 12-48 hours (complex cutover)

**Effort:** 3-6 months (complete rewrite)

**Cost:** 240-480 hours engineering = $120K-240K

**Why So Complex:**
- GSQL completely different paradigm (procedural vs declarative)
- No equivalent in other databases
- TigerGraph schema design differs significantly
- Distributed architecture (multi-node cutover complex)

---

## Migration Complexity Matrix

| Source → Destination | Query Rewrite | Data Transform | Effort | Cost | Risk |
|---------------------|---------------|----------------|--------|------|------|
| **Memgraph → Neo4j** | Minimal (5%) | None | 1-2 weeks | $5K-10K | Low |
| **Neo4j → Memgraph** | Minimal (5%) | None | 1-2 weeks | $5K-10K | Low |
| **JanusGraph → Neptune** | Minimal (10%) | None | 1-2 weeks | $5K-10K | Low |
| **Neptune → JanusGraph** | Minimal (10%) | Setup cluster | 2-4 weeks | $10K-20K | Medium |
| **Neo4j → Neptune** | Medium (20%) | None | 1-2 months | $20K-40K | Medium |
| **Neo4j → JanusGraph** | High (100%) | Setup cluster | 2-3 months | $80K-120K | High |
| **Neo4j → ArangoDB** | High (100%) | Data model | 2-3 months | $80K-120K | High |
| **TigerGraph → Any** | Very High (100%) | Complete redesign | 3-6 months | $120K-240K | Very High |
| **ArangoDB → Any** | Very High (100%) | Complete redesign | 3-6 months | $120K-240K | Very High |

---

## Should You Migrate? (ROI Calculation)

### Migration Cost

**Engineering Time:**
- Low complexity: 40-80 hours × $50/hr = $2K-4K
- Medium complexity: 160-320 hours × $50/hr = $8K-16K
- High complexity: 320-480 hours × $50/hr = $16K-24K
- Very high: 480-960 hours × $50/hr = $24K-48K

**Downtime Cost:**
- E-commerce: $10K-100K/hour (revenue loss)
- B2B SaaS: $1K-10K/hour (customer impact)
- Internal tools: $100-1K/hour (productivity loss)

**Risk Cost:**
- Data loss risk: $50K-500K (insurance)
- Bug risk: 10-20% time padding

**Total Migration Cost:** Engineering + Downtime + Risk

---

### Annual Savings

**Current database:** $A/month × 12 = $Current/year
**New database:** $B/month × 12 = $New/year
**Savings:** $Current - $New = $S/year

---

### Break-Even Analysis

**Break-Even:** Total Migration Cost ÷ Annual Savings = X years

**Decision:**
- Break-even <18 months: ✅ Migrate
- Break-even 18-36 months: ⚠️ Consider (depends on other factors)
- Break-even >36 months: ❌ Stay

---

### Example: Neo4j Aura → Memgraph Cloud

**Current:** Neo4j Aura $480/month = $5,760/year
**New:** Memgraph Cloud $199/month = $2,388/year
**Savings:** $5,760 - $2,388 = $3,372/year

**Migration Cost:**
- Engineering: 40-80 hours × $50 = $2K-4K
- Downtime: 4 hours × $100 = $400
- **Total: $2,400-4,400**

**Break-Even:** $3,400 ÷ $3,372/year = 1.0 years ✅

**Decision:** Worth it (break-even <18 months)

---

### Example: Neo4j Aura → TigerGraph Enterprise

**Current:** Neo4j Aura $240/month = $2,880/year
**New:** TigerGraph Enterprise $3,000/month = $36,000/year
**Change:** -$33,120/year (MORE expensive!)

**Decision:** ❌ Not a cost migration (only migrate for technical reasons: scale, performance)

---

## Migration Best Practices

### 1. Test Migration First (Staging)

**Process:**
1. Export production data → staging database (new provider)
2. Run application against staging for 2-4 weeks
3. Identify issues before production cutover
4. Fix bugs, optimize queries

**Time Investment:** 20% of total migration effort
**Risk Reduction:** 80% of bugs caught in staging

---

### 2. Dual-Write Strategy (Zero Downtime)

**Process:**
1. Setup new database alongside old
2. Application writes to BOTH databases
3. Read from old database (source of truth)
4. Monitor sync lag
5. When new database synced, switch reads to new
6. Run dual-write for 1-2 weeks (safety)
7. Decommission old database

**Downtime:** <5 minutes (DNS/config switch)
**Complexity:** Higher (dual-write code)
**Worth it for:** Mission-critical systems (e-commerce, fintech)

---

### 3. Feature Flag Migration (Gradual Rollout)

**Process:**
1. Implement feature flag (LaunchDarkly, Split, or custom)
2. Route 1% traffic to new database
3. Monitor errors, performance
4. Increase to 10%, 25%, 50%, 100%
5. Rollback instantly if issues

**Risk Reduction:** Catch issues at low traffic volume
**Time:** Slower overall (weeks vs days)
**Worth it for:** User-facing systems

---

### 4. Backup Everything

**Before migration:**
- ✅ Export old database (multiple formats: CSV, JSON, GraphML)
- ✅ Store backups in S3/GCS (redundant storage)
- ✅ Test restore process (ensure backups valid)
- ✅ Keep old database running for 30-90 days (rollback option)

**Don't:**
- ❌ Delete old database immediately
- ❌ Assume backups work without testing
- ❌ Skip redundant backups (S3 + GCS)

---

## Migration Complexity Recommendations

**Easiest Migrations (1-2 weeks):**
- Memgraph ↔ Neo4j (openCypher compatible)
- JanusGraph ↔ Neptune (Gremlin standard)

**Medium Migrations (1-2 months):**
- Neo4j → Neptune (Cypher → openCypher, 80% compatible)
- Any → Self-hosted (same database, managed → self-hosted)

**Avoid If Possible (2-3 months):**
- Neo4j → JanusGraph (Cypher → Gremlin, complete rewrite)
- Neo4j/Memgraph → ArangoDB (Cypher → AQL, proprietary)

**Extremely Complex (3-6 months):**
- TigerGraph → Any (GSQL 100% proprietary)
- ArangoDB → Any (AQL proprietary)

**Key Principle:** Choose database with low migration complexity today (openCypher, Gremlin). Avoid proprietary languages (GSQL, AQL) if lock-in critical.

---

**Next:** S4 Synthesis (Strategic Recommendations)
