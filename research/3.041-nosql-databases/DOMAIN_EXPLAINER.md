# NoSQL Databases: Domain Explainer & Decision Framework

**Category:** 3.041 (Managed Services - Data Persistence - NoSQL Databases)
**Last Updated:** November 16, 2025
**Research Status:** ✅ S1-S4 Complete

---

## What are NoSQL Databases?

**NoSQL** ("Not Only SQL") databases are non-relational databases designed for specific data models and access patterns. Unlike relational databases (SQL), NoSQL databases optimize for schema flexibility, horizontal scaling, and specific workload patterns.

**Four main categories:**
1. **Document databases:** JSON/BSON documents (MongoDB, Firestore)
2. **Key-value stores:** Simple key → value mappings (DynamoDB, Redis)
3. **Wide-column stores:** Column families for time-series (Cassandra, ScyllaDB)
4. **Graph databases:** Nodes and relationships (Neo4j)

---

## When to Use NoSQL vs SQL?

### Use NoSQL when:
- ✅ **Schema flexibility** needed (rapid iteration, varying structures)
- ✅ **Horizontal scaling** required (multi-terabyte data, distributed systems)
- ✅ **Specific data model** fits better (documents, time-series, graphs)
- ✅ **High-throughput writes** (>10K writes/sec, IoT, logging)
- ✅ **Real-time sync** needed (mobile apps, collaborative tools)

### Use SQL (PostgreSQL) when:
- ✅ **Relational data** with many joins
- ✅ **ACID transactions** critical (financial systems, e-commerce)
- ✅ **Complex queries** with aggregations (reporting, analytics)
- ✅ **Data fits in single server** (<1TB, vertical scaling OK)
- ✅ **Standard SQL** important (portability, lowest lock-in)

**Pragmatic rule:** Default to PostgreSQL unless you have a clear NoSQL need

---

## NoSQL Database Categories

### 1. Document Databases

**Data Model:** JSON/BSON documents with nested structures

**Best For:**
- Content management systems
- User profiles and settings
- Product catalogs
- Mobile app backends

**Top Providers:**
- **MongoDB Atlas:** Market leader, rich queries, Atlas Search
- **Firestore:** Google, real-time sync, mobile-first
- **Cosmos DB (SQL API):** Azure, multi-model

**Example data:**
```json
{
  "_id": "user_123",
  "name": "Alice",
  "email": "alice@example.com",
  "settings": {
    "theme": "dark",
    "notifications": ["email", "push"]
  },
  "projects": [
    { "id": "proj_1", "role": "owner" },
    { "id": "proj_2", "role": "member" }
  ]
}
```

---

### 2. Key-Value Stores

**Data Model:** Simple key → value mappings

**Best For:**
- Session storage
- User preferences
- Shopping carts
- Caching (as database, not just cache)
- Real-time leaderboards

**Top Providers:**
- **DynamoDB:** AWS, serverless, single-digit ms latency
- **Redis Enterprise Cloud:** In-memory, sub-ms latency, data structures
- **Upstash:** Serverless Redis, edge-optimized

**Example data:**
```
Key: session:abc123
Value: { userId: "user_456", expiresAt: 1700000000 }

Key: user:user_456:cart
Value: ["item_1", "item_2", "item_3"]
```

---

### 3. Wide-Column Stores

**Data Model:** Tables with flexible column families, optimized for time-series

**Best For:**
- Time-series data (IoT sensors, metrics, logs)
- Event logging
- Write-heavy workloads
- Massive scale (multi-terabyte)

**Top Providers:**
- **Cassandra (DataStax Astra):** Apache Cassandra as-a-service
- **ScyllaDB Cloud:** 10× faster Cassandra (C++ rewrite)
- **Bigtable:** Google, HBase-compatible

**Example data:**
```
device_id | timestamp           | temperature | pressure
----------|---------------------|-------------|----------
device_01 | 2025-11-16 14:00:00 | 22.5        | 1013.2
device_01 | 2025-11-16 14:00:01 | 22.6        | 1013.3
device_01 | 2025-11-16 14:00:02 | 22.5        | 1013.2
```

**Query:** Get all readings for device_01 in last hour (partition by device + time bucket)

---

### 4. Graph Databases

**Data Model:** Nodes and edges (relationships)

**Best For:**
- Social networks (friends, followers)
- Recommendation engines
- Fraud detection
- Knowledge graphs
- Network analysis

**Top Providers:**
- **Neo4j Aura:** Market leader, Cypher query language
- **Neptune:** AWS, openCypher + Gremlin
- **ArangoDB:** Multi-model (document + graph)

**Example data:**
```
Nodes:
- (alice:Person {name: "Alice", age: 30})
- (bob:Person {name: "Bob", age: 35})
- (python:Skill {name: "Python"})

Relationships:
- (alice)-[:FRIENDS_WITH {since: 2020}]->(bob)
- (alice)-[:KNOWS]->(python)
- (bob)-[:KNOWS]->(python)

Query: Find friends of Alice who know Python
MATCH (alice:Person {name: "Alice"})-[:FRIENDS_WITH]->(friend)-[:KNOWS]->(python:Skill {name: "Python"})
RETURN friend.name
```

---

## Quick Decision Tree

### Step 1: What's your primary data model?

**Documents (JSON-like nested data):**
→ MongoDB Atlas, Firestore

**Key-value (simple lookups by ID):**
→ DynamoDB, Redis Enterprise

**Time-series (IoT, logs, events):**
→ Cassandra, ScyllaDB, InfluxDB (specialized)

**Graph (relationships, networks):**
→ Neo4j Aura

**Relational (joins, transactions):**
→ PostgreSQL (not NoSQL!)

---

### Step 2: What's your cloud ecosystem?

**AWS:**
- Key-value: DynamoDB (native)
- Document: MongoDB Atlas or DocumentDB
- Wide-column: Cassandra Astra

**GCP:**
- Real-time mobile: Firestore (native)
- Document: MongoDB Atlas
- Wide-column: Bigtable or Cassandra Astra

**Azure:**
- Multi-model: Cosmos DB (native)
- Document: MongoDB Atlas
- Wide-column: Cassandra Astra

**Multi-cloud or cloud-agnostic:**
- MongoDB Atlas (AWS, GCP, Azure)
- Cassandra Astra (AWS, GCP, Azure)
- ScyllaDB Cloud (AWS, GCP, Azure)

---

### Step 3: What's your budget?

**Bootstrap (<$100/month):**
- Free tiers: Cassandra Astra (25GB), DynamoDB (25GB), Firestore (1GB)
- Best value: Supabase (PostgreSQL + real-time, $25/month Pro tier)

**Startup ($100-500/month):**
- Documents: MongoDB Atlas Serverless
- Key-value: DynamoDB
- Time-series: Cassandra Astra Serverless

**Scale-up ($500-5K/month):**
- Documents: MongoDB Atlas (dedicated M20-M40)
- Key-value: DynamoDB (provisioned)
- Time-series: InfluxDB Cloud or Cassandra

**Enterprise (>$5K/month):**
- Consider self-hosting (break-even point)
- Or use managed services with enterprise support

---

### Step 4: What's your lock-in tolerance?

**Low lock-in (prefer open standards):**
- **Cassandra (CQL standard):** Astra ↔ ScyllaDB ↔ self-hosted
- **PostgreSQL (SQL standard):** Supabase ↔ AWS RDS ↔ self-hosted
- **Redis (RESP protocol):** Redis Enterprise ↔ Valkey ↔ self-hosted

**Medium lock-in (self-host option exists):**
- **MongoDB:** Atlas ↔ DocumentDB (80% compatible) ↔ self-hosted Community

**High lock-in (proprietary, but worth it for DX):**
- **Firestore:** Best mobile real-time experience (GCP-only)
- **DynamoDB:** Best AWS serverless integration (AWS-only)
- **Cosmos DB:** Best Azure multi-model (Azure-only)

---

## Cost Comparison (100GB data, 100M reads, 10M writes/month)

| Database | Monthly Cost | Notes |
|----------|--------------|-------|
| **DynamoDB (provisioned)** | $30 | Cheapest, but limited queries |
| **Cassandra Astra** | $38 | Best for time-series |
| **MongoDB Atlas** | $160 | Premium for documents |
| **Firestore** | $96 | Premium for real-time mobile |
| **Redis Enterprise** | $260+ | In-memory, expensive |
| **Neo4j Aura** | $82 | Specialized for graphs |
| **ScyllaDB** | $1,095 | Ultra-low latency (3-node minimum) |

**Cost variance:** 36× difference (DynamoDB $30 vs ScyllaDB $1,095)

---

## Performance Comparison

### Latency (p99)
1. **Redis Enterprise:** <1ms (in-memory)
2. **ScyllaDB Cloud:** <1ms (C++ efficiency)
3. **DynamoDB:** 1-5ms
4. **Cassandra:** 3-10ms
5. **MongoDB:** 5-20ms
6. **Firestore:** 10-50ms
7. **Neo4j:** 10-100ms (depends on graph traversal)

### Throughput (single node)
1. **Redis:** 1M+ ops/sec
2. **ScyllaDB:** 500K+ ops/sec
3. **Cassandra:** 50K ops/sec
4. **DynamoDB:** Unlimited (serverless auto-scales)
5. **MongoDB:** 10K-50K ops/sec

### Query Power
1. **MongoDB:** Best (aggregation pipeline, full-text search)
2. **Neo4j:** Best for graphs (600× faster than SQL for traversals)
3. **Cosmos DB:** Good (SQL queries, multi-model)
4. **DynamoDB:** Limited (key-only queries)
5. **Cassandra:** Limited (no aggregations, CQL range queries only)

---

## Recommended Providers by Use Case

### Startup SaaS Application
**Primary:** MongoDB Atlas (Serverless)
- Flexible schema (rapid iteration)
- Rich queries (complex filtering)
- Atlas Search (full-text)
- **Cost:** $5-20/month startup, $150-500/month at scale

**Alternative:** Supabase (PostgreSQL + real-time)
- Best value ($25/month Pro tier)
- Low lock-in (SQL standard)
- Real-time built-in
- Trade-off: Relational model (requires schema)

---

### Real-Time Mobile App
**Primary:** Firestore
- Real-time sync built-in
- Offline support (automatic)
- Native mobile SDKs (iOS, Android, Flutter)
- Firebase platform integration
- **Cost:** $100-500/month at scale

**Alternative:** DynamoDB + AppSync
- 43% cheaper
- AWS ecosystem
- GraphQL real-time subscriptions
- Trade-off: More complex setup

---

### IoT Time-Series Data
**Primary:** InfluxDB Cloud
- Purpose-built for time-series
- 10× compression
- Built-in downsampling
- **Cost:** $50-500/month

**Alternative:** Cassandra Astra
- General-purpose (not just time-series)
- Write-optimized (50K+ writes/sec)
- CQL standard (low lock-in)
- **Cost:** $40-400/month

---

### High-Traffic E-Commerce
**Primary:** DynamoDB (AWS)
- Single-digit millisecond latency
- Infinite scale
- Serverless (auto-scales)
- **Cost:** $50-500/month

**Plus:** Redis Enterprise (session storage)
- Sub-millisecond latency
- In-memory data structures
- **Cost:** $50-200/month

---

### Social Network / Recommendations
**Primary:** Neo4j Aura (graph database)
- Native graph storage
- Cypher query language
- Graph algorithms (PageRank, community detection)
- **Cost:** $20-200/month

**For user data:** MongoDB Atlas
- Document model for user profiles
- **Cost:** $50-200/month

**Hybrid:** Neo4j (relationships) + MongoDB (profiles)

---

## Lock-in Mitigation Strategies

### 1. Choose Open Standards (Lowest Lock-in)
- **Cassandra (CQL):** Compatible with ScyllaDB, self-hosted
- **PostgreSQL (SQL):** Universal standard, many providers
- **Redis (RESP):** Compatible with Valkey (open source fork)

### 2. Database Abstraction Layer
```javascript
// Wrap database calls in application layer
const db = require('./database-layer');

// Can swap MongoDB → DynamoDB → PostgreSQL
db.users.findById(userId);
db.users.create(userData);
```

### 3. Regular Exports
- Daily/weekly backups to S3/GCS
- Export formats: JSON, CSV, BSON
- Use for disaster recovery + migration preparation

### 4. Self-Host Option as Insurance
- Cassandra, MongoDB, Redis have viable self-host options
- Test migration path annually
- Break-even: ~$3,000-5,000/month managed spend

### 5. Multi-Cloud Deployment
- Use MongoDB Atlas, Cassandra Astra (all clouds)
- Avoid: DynamoDB (AWS-only), Firestore (GCP-only), Cosmos DB (Azure-only)

---

## Common Pitfalls

### 1. Choosing NoSQL When SQL Would Work Better
**Mistake:** Using MongoDB for relational e-commerce data (orders, products, inventory)
**Fix:** Use PostgreSQL for relational data, NoSQL for specific needs

### 2. Underestimating Operational Complexity
**Mistake:** Self-hosting Cassandra to save money (without ops expertise)
**Fix:** Use managed services until $5K/month spend, then consider self-hosting

### 3. Ignoring Query Patterns
**Mistake:** Choosing DynamoDB without understanding access patterns (later need complex queries)
**Fix:** Design access patterns upfront, choose database that matches

### 4. Not Optimizing Costs
**Mistake:** Using Firestore naively (no caching, reading entire collections)
**Fix:** Implement caching, batch writes, filtered queries (can save 50-90%)

### 5. Assuming "NoSQL = Scalable"
**Mistake:** Thinking MongoDB will auto-scale without sharding design
**Fix:** Understand scaling model (MongoDB sharding, Cassandra partitioning)

---

## Vendor Viability (5-Year Outlook)

### Extremely Stable (99%+ survival)
- **DynamoDB:** Amazon core service
- **Firestore:** Google core service
- **Cosmos DB:** Microsoft core service
- **MongoDB Atlas:** $1.9B revenue, profitable, public company

### Very Stable (95-99% survival)
- **Redis Enterprise:** $100M+ ARR, critical infrastructure
- **Cassandra (Astra):** Proven at scale (Netflix, Apple, Discord)
- **Neo4j Aura:** Graph database leader, $200M+ ARR

### Stable (90-95% survival)
- **ScyllaDB Cloud:** Growing fast, 10× performance vs Cassandra
- **InfluxDB Cloud:** Time-series leader, niche market

**Acquisition likely:** Redis, Neo4j, DataStax (neutral to positive impact)

---

## Final Recommendations

### For Solo Founder / Budget-Conscious
**Use:** Supabase (PostgreSQL + real-time)
- **Cost:** $25/month (years)
- **Lock-in:** Low (SQL standard)
- **Trade-off:** Relational model (not schemaless)

### For Fast Development / Flexibility
**Use:** MongoDB Atlas (Serverless)
- **Cost:** $5-50/month startup, $150-500/month at scale
- **Lock-in:** Medium (self-host option exists)
- **Benefit:** Fastest iteration, flexible schema

### For Mobile App
**Use:** Firestore
- **Cost:** $100-500/month at scale
- **Lock-in:** High (proprietary real-time)
- **Benefit:** Best mobile developer experience

### For AWS Ecosystem
**Use:** DynamoDB
- **Cost:** $5-50/month startup, $50-300/month at scale
- **Lock-in:** High (AWS-only, proprietary)
- **Benefit:** Cheapest, best AWS integration

### For Time-Series / IoT
**Use:** InfluxDB Cloud or Cassandra Astra
- **Cost:** $50-500/month
- **Lock-in:** Medium-High (InfluxDB), Medium (Cassandra CQL)
- **Benefit:** Purpose-built for time-series

---

## Migration Complexity

**Easy (1 day - 1 week):**
- PostgreSQL providers (Supabase → AWS RDS → self-hosted)
- Cassandra providers (Astra → ScyllaDB → self-hosted)
- Redis (Enterprise → Valkey → self-hosted)

**Medium (1-4 weeks):**
- MongoDB Atlas → self-hosted MongoDB
- MongoDB Atlas → AWS DocumentDB (80% compatible)

**Hard (1-3 months, application rewrite):**
- Firestore → anything (proprietary real-time)
- DynamoDB → anything (proprietary API, no equivalent)
- Cosmos DB → anything (RU model unique)

---

## Research Links

- **S1 Rapid Search:** Provider profiles + synthesis (8 providers)
- **S2 Comprehensive:** Feature matrix (60+ features), pricing TCO (6 scenarios), performance benchmarks
- **S3 Need-Driven:** Business scenarios (startup SaaS, mobile app, IoT)
- **S4 Strategic:** Vendor viability, lock-in mitigation, 5-10 year outlook

**Full Research:** `/research/3.041-nosql-databases/01-discovery/`

---

**Last Updated:** November 16, 2025
**Research Status:** ✅ S1-S4 Complete
