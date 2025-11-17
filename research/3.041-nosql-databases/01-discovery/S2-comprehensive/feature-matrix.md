# S2: Feature Comparison Matrix

**Research Date:** November 16, 2025
**Providers Analyzed:** 8 major NoSQL platforms
**Features Compared:** 60+

---

## Feature Matrix Legend

- ✅ **Full Support:** Native, production-ready
- ⚠️ **Partial Support:** Limited, requires workarounds
- ❌ **Not Supported:** Not available
- 💰 **Paid Only:** Requires premium tier

---

## Data Model Features

| Feature | MongoDB Atlas | DynamoDB | Firestore | Cosmos DB | Cassandra | Redis Ent | Neo4j | ScyllaDB |
|---------|---------------|----------|-----------|-----------|-----------|-----------|-------|----------|
| **Primary Model** | Document | Key-Value | Document | Multi-Model | Wide-Column | Key-Value | Graph | Wide-Column |
| Document storage | ✅ | ⚠️ (400KB limit) | ✅ | ✅ | ⚠️ (via JSON) | ⚠️ (RedisJSON) | ❌ | ⚠️ (via JSON) |
| Key-value access | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| Graph model | ❌ | ❌ | ❌ | ✅ (Gremlin) | ❌ | ⚠️ (RedisGraph) | ✅ | ❌ |
| Wide-column | ❌ | ⚠️ (sort key) | ❌ | ✅ (Cassandra API) | ✅ | ❌ | ❌ | ✅ |
| Time-series | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ (RedisTimeSeries) | ⚠️ | ✅ |
| Flexible schema | ✅ | ✅ | ✅ | ✅ | ⚠️ (CQL schema) | ✅ | ✅ | ⚠️ (CQL schema) |
| Max document size | 16MB | 400KB | 1MB | 2MB | 2GB (row) | 512MB (value) | N/A | 2GB (row) |

---

## Query Capabilities

| Feature | MongoDB Atlas | DynamoDB | Firestore | Cosmos DB | Cassandra | Redis Ent | Neo4j | ScyllaDB |
|---------|---------------|----------|-----------|-----------|-----------|-----------|-------|----------|
| **Query Language** | MQL | API | SDK | SQL/CQL/Gremlin | CQL | Commands | Cypher | CQL |
| Rich queries | ✅ | ❌ (key only) | ⚠️ (limited) | ✅ | ⚠️ (CQL) | ❌ (key only) | ✅ | ⚠️ (CQL) |
| Secondary indexes | ✅ | ⚠️ (GSI/LSI) | ✅ (composite) | ✅ | ✅ | ⚠️ (RediSearch) | ✅ | ✅ |
| Full-text search | ✅ (Atlas Search) | ❌ | ❌ | ✅ (Azure Search) | ❌ | ✅ (RediSearch) | ✅ (text index) | ❌ |
| Aggregations | ✅ (pipeline) | ❌ | ❌ (client-side) | ✅ (SQL API) | ❌ | ⚠️ (RediSearch) | ✅ (Cypher) | ❌ |
| Joins | ⚠️ ($lookup) | ❌ | ❌ | ⚠️ (SQL API) | ❌ | ❌ | ✅ (graph) | ❌ |
| Graph traversals | ❌ | ❌ | ❌ | ✅ (Gremlin) | ❌ | ❌ | ✅ | ❌ |
| Geospatial queries | ✅ | ❌ | ⚠️ (basic) | ✅ | ❌ | ✅ (Geo commands) | ✅ (spatial) | ❌ |
| Array queries | ✅ | ❌ | ⚠️ (array-contains) | ✅ | ⚠️ (frozen) | ✅ (lists) | ✅ | ⚠️ (frozen) |

---

## Consistency & Transactions

| Feature | MongoDB Atlas | DynamoDB | Firestore | Cosmos DB | Cassandra | Redis Ent | Neo4j | ScyllaDB |
|---------|---------------|----------|-----------|-----------|-----------|-----------|-------|----------|
| **Default Consistency** | Eventual | Eventual | Strong | Session | Eventual | Strong | Strong | Eventual |
| Strong consistency | ✅ | ✅ (opt-in) | ✅ | ✅ (5 levels) | ✅ (QUORUM) | ✅ | ✅ (ACID) | ✅ (QUORUM) |
| Eventual consistency | ✅ | ✅ | ❌ | ✅ | ✅ | N/A | ❌ | ✅ |
| Tunable consistency | ❌ | ⚠️ (read level) | ❌ | ✅ (5 levels) | ✅ (per query) | ❌ | ❌ | ✅ (per query) |
| ACID transactions | ✅ (multi-doc) | ⚠️ (single item) | ⚠️ (500 docs) | ⚠️ (partition) | ⚠️ (partition) | ✅ (MULTI/EXEC) | ✅ (full) | ⚠️ (partition) |
| Distributed transactions | ✅ | ❌ | ⚠️ (batch) | ⚠️ | ❌ | ❌ | ✅ | ❌ |
| Optimistic locking | ✅ | ✅ | ✅ | ✅ | ⚠️ (LWT) | ✅ (WATCH) | ✅ | ⚠️ (LWT) |

---

## Scalability & Performance

| Feature | MongoDB Atlas | DynamoDB | Firestore | Cosmos DB | Cassandra | Redis Ent | Neo4j | ScyllaDB |
|---------|---------------|----------|-----------|-----------|-----------|-----------|-------|----------|
| **Horizontal Scaling** | ✅ (sharding) | ✅ (auto) | ✅ (auto) | ✅ (partitioning) | ✅ (linear) | ⚠️ (cluster) | ⚠️ (limited) | ✅ (linear) |
| Auto-scaling | ✅ | ✅ | ✅ | ✅ | ❌ (manual) | ⚠️ | ⚠️ | ✅ |
| Serverless | ✅ | ✅ | ✅ | ✅ | ✅ (Astra) | ❌ | ⚠️ (auto-pause) | ❌ |
| Read replicas | ✅ | ❌ (GSI) | ✅ (multi-region) | ✅ | ✅ (replication) | ✅ | ✅ | ✅ |
| Write scaling | ✅ (sharding) | ✅ (infinite) | ✅ (auto) | ✅ | ✅ (best) | ⚠️ (primary) | ⚠️ (limited) | ✅ (best) |
| Latency (p99) | 10-50ms | 1-5ms | 10-50ms | 5-20ms | 3-10ms | <1ms | 10-100ms | <1ms |
| Throughput/node | 10K ops/sec | Unlimited | Unlimited | 10K RU/s | 50K ops/sec | 1M ops/sec | Varies | 500K ops/sec |

---

## High Availability & Disaster Recovery

| Feature | MongoDB Atlas | DynamoDB | Firestore | Cosmos DB | Cassandra | Redis Ent | Neo4j | ScyllaDB |
|---------|---------------|----------|-----------|-----------|-----------|-----------|-------|----------|
| **Replication** | ✅ (3+ nodes) | ✅ (3 AZs) | ✅ (multi-region) | ✅ (multi-region) | ✅ (RF=3) | ✅ | ✅ | ✅ (RF=3) |
| Multi-region | ✅ | ✅ (Global Tables) | ✅ | ✅ | ✅ | ⚠️ (Active-Active) | 💰 (Enterprise) | ✅ |
| Active-active | ⚠️ (conflicts) | ✅ | ❌ | ✅ | ✅ | ✅ (CRDT) | ❌ | ✅ |
| Automatic failover | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Backups (automated) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Point-in-time recovery | ✅ | ✅ (PITR) | ❌ | ✅ | ❌ | ⚠️ (AOF) | 💰 | ❌ |
| SLA | 99.995% | 99.99% | 99.95% | 99.999% | 99.99% | 99.99% | 99.95% | 99.99% |

---

## Developer Experience

| Feature | MongoDB Atlas | DynamoDB | Firestore | Cosmos DB | Cassandra | Redis Ent | Neo4j | ScyllaDB |
|---------|---------------|----------|-----------|-----------|-----------|-----------|-------|----------|
| **Client Drivers** | 15+ languages | 10+ (AWS SDKs) | 8+ | 10+ | 10+ | 15+ | 10+ | 10+ (Cassandra) |
| ORMs/Abstractions | ✅ (many) | ⚠️ (few) | ✅ (Firebase SDKs) | ⚠️ (few) | ⚠️ (few) | ✅ (many) | ✅ (Spring Data) | ⚠️ (Cassandra ORMs) |
| Local development | ✅ (Community) | ✅ (Local) | ✅ (Emulator) | ✅ (Emulator) | ✅ (Docker) | ✅ (Docker) | ✅ (Desktop) | ✅ (Docker) |
| GUI tools | ✅ (Compass) | ⚠️ (AWS Console) | ✅ (Console) | ✅ (Data Explorer) | ⚠️ (cqlsh) | ✅ (RedisInsight) | ✅ (Browser/Bloom) | ⚠️ (cqlsh) |
| Query builder | ✅ | ❌ | ✅ | ⚠️ | ❌ | ❌ | ✅ | ❌ |
| Schema validation | ✅ | ❌ | ✅ (rules) | ✅ | ⚠️ (CQL DDL) | ❌ | ✅ (constraints) | ⚠️ (CQL DDL) |
| Migrations tools | ✅ | ⚠️ (custom) | ⚠️ (Firebase CLI) | ⚠️ | ⚠️ (custom) | ⚠️ | ⚠️ | ⚠️ (custom) |

---

## Real-Time & Streaming

| Feature | MongoDB Atlas | DynamoDB | Firestore | Cosmos DB | Cassandra | Redis Ent | Neo4j | ScyllaDB |
|---------|---------------|----------|-----------|-----------|-----------|-----------|-------|----------|
| **Change streams** | ✅ | ✅ (Streams) | ✅ (listeners) | ✅ (Change Feed) | ❌ | ✅ (Pub/Sub) | ❌ | ⚠️ (CDC) |
| Real-time sync | ⚠️ (Realm Sync) | ❌ | ✅ (native) | ⚠️ | ❌ | ✅ (Pub/Sub) | ❌ | ❌ |
| Offline support | ⚠️ (Realm) | ❌ | ✅ (native) | ❌ | ❌ | ❌ | ❌ | ❌ |
| Webhooks | ⚠️ (Triggers) | ❌ (use Streams) | ❌ (use Functions) | ❌ | ❌ | ❌ | ❌ | ❌ |
| Event-driven | ✅ (Atlas Triggers) | ✅ (EventBridge) | ✅ (Cloud Functions) | ✅ (Functions) | ⚠️ (external) | ✅ (Streams) | ❌ | ⚠️ (CDC) |

---

## Security & Compliance

| Feature | MongoDB Atlas | DynamoDB | Firestore | Cosmos DB | Cassandra | Redis Ent | Neo4j | ScyllaDB |
|---------|---------------|----------|-----------|-----------|-----------|-----------|-------|----------|
| **Encryption at rest** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Encryption in transit | ✅ (TLS) | ✅ (TLS) | ✅ (TLS) | ✅ (TLS) | ✅ (TLS) | ✅ (TLS) | ✅ (TLS) | ✅ (TLS) |
| VPC/Private Link | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 💰 | ✅ |
| IAM integration | ⚠️ (AWS IAM) | ✅ (AWS IAM) | ✅ (GCP IAM) | ✅ (Azure AD) | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| RBAC | ✅ | ✅ (IAM policies) | ✅ (Security Rules) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Audit logging | ✅ | ✅ (CloudTrail) | ✅ (Cloud Logging) | ✅ | ⚠️ | ⚠️ | 💰 | ⚠️ |
| Compliance | SOC 2, HIPAA, PCI | All AWS certs | All GCP certs | All Azure certs | Varies | Varies | SOC 2 | SOC 2 |

---

## Advanced Features

| Feature | MongoDB Atlas | DynamoDB | Firestore | Cosmos DB | Cassandra | Redis Ent | Neo4j | ScyllaDB |
|---------|---------------|----------|-----------|-----------|-----------|-----------|-------|----------|
| **Full-text search** | ✅ (Atlas Search) | ❌ | ❌ | ✅ (Azure Search) | ❌ | ✅ (RediSearch) | ✅ | ❌ |
| Vector search | ✅ (Atlas Vector) | ❌ | ⚠️ (extensions) | ✅ | ✅ (Astra) | ✅ (RediSearch) | ❌ | ❌ |
| Graph algorithms | ❌ | ❌ | ❌ | ⚠️ (Gremlin) | ❌ | ❌ | ✅ (GDS) | ❌ |
| Time-series optimization | ⚠️ | ⚠️ | ❌ | ⚠️ | ✅ | ✅ (RedisTimeSeries) | ❌ | ✅ |
| Analytics integration | ✅ (Atlas Data Lake) | ✅ (Athena, Redshift) | ✅ (BigQuery) | ✅ (Synapse Link) | ✅ (Spark) | ⚠️ | ⚠️ | ✅ (Spark) |
| Serverless functions | ✅ (Atlas Functions) | ✅ (Lambda) | ✅ (Cloud Functions) | ✅ (Azure Functions) | ❌ | ❌ | ❌ | ❌ |
| GraphQL API | ⚠️ (Atlas GraphQL) | ⚠️ (AppSync) | ❌ | ❌ | ✅ (Astra) | ❌ | ❌ | ❌ |

---

## Cloud & Multi-Cloud Support

| Feature | MongoDB Atlas | DynamoDB | Firestore | Cosmos DB | Cassandra | Redis Ent | Neo4j | ScyllaDB |
|---------|---------------|----------|-----------|-----------|-----------|-----------|-------|----------|
| **AWS** | ✅ | ✅ (native) | ❌ | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| **GCP** | ✅ | ❌ | ✅ (native) | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| **Azure** | ✅ | ❌ | ❌ | ✅ (native) | ✅ | ✅ | ✅ | ✅ |
| Multi-cloud | ✅ | ❌ (AWS only) | ❌ (GCP only) | ❌ (Azure only) | ✅ | ✅ | ✅ | ✅ |
| Hybrid cloud | ⚠️ | ❌ | ❌ | ⚠️ (Arc) | ✅ | ✅ | ✅ | ✅ |

---

## Summary Scores (Out of 10)

| Category | MongoDB | DynamoDB | Firestore | Cosmos DB | Cassandra | Redis | Neo4j | ScyllaDB |
|----------|---------|----------|-----------|-----------|-----------|-------|-------|----------|
| **Ease of Use** | 8 | 6 | 9 | 5 | 4 | 7 | 7 | 4 |
| **Query Power** | 9 | 3 | 5 | 8 | 5 | 3 | 10 | 5 |
| **Performance** | 7 | 9 | 7 | 8 | 8 | 10 | 6 | 10 |
| **Scalability** | 8 | 10 | 9 | 9 | 10 | 6 | 5 | 10 |
| **Flexibility** | 9 | 6 | 7 | 10 | 7 | 8 | 6 | 7 |
| **Free Tier** | 6 | 8 | 7 | 7 | 9 | 3 | 5 | 2 |
| **Portability** | 7 | 2 | 2 | 3 | 9 | 8 | 6 | 9 |
| **Ecosystem** | 9 | 8 | 8 | 7 | 7 | 9 | 7 | 6 |
| **Total** | 63/80 | 52/80 | 54/80 | 57/80 | 59/80 | 54/80 | 52/80 | 53/80 |

---

**Key Takeaways:**

1. **MongoDB Atlas:** Best all-around document database (ease + query power + ecosystem)
2. **DynamoDB:** Best performance + scalability for key-value (AWS lock-in trade-off)
3. **Firestore:** Best for mobile (real-time + offline)
4. **Cosmos DB:** Best multi-model flexibility (complexity + cost trade-off)
5. **Cassandra/Astra:** Best for massive scale time-series (free tier champion)
6. **Redis Enterprise:** Best performance but memory-limited and expensive
7. **Neo4j Aura:** Best for graphs (specialized use case)
8. **ScyllaDB Cloud:** Best performance for wide-column (no free tier)

---

**Next:** Pricing TCO analysis
