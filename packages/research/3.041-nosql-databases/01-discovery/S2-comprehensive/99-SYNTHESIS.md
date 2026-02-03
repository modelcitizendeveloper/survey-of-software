# S2 Synthesis: Comprehensive Analysis Summary

**Research Complete:** November 16, 2025
**Analysis Scope:** 60+ features, 6 cost scenarios, performance benchmarks
**Providers:** 8 major NoSQL platforms

---

## Key Findings

### 1. No Universal Winner

Each database optimizes for specific trade-offs:
- **MongoDB:** Best queries, worst cost at scale
- **DynamoDB:** Best cost-performance, worst query flexibility
- **Firestore:** Best mobile experience, expensive at scale
- **Cosmos DB:** Best multi-model, complex pricing
- **Cassandra:** Best writes, no aggregations
- **Redis:** Fastest, memory-limited
- **Neo4j:** Best graphs, specialized only
- **ScyllaDB:** Fastest wide-column, expensive minimum

---

### 2. Cost Variance is Massive

**100GB data, 100M reads, 10M writes/month:**
- **Cheapest:** DynamoDB provisioned ($30/month)
- **Most Expensive:** ScyllaDB ($1,095/month)
- **Variance:** 36× price difference

**Key insight:** "NoSQL" doesn't mean "cheap" - cost varies wildly by provider and use case

---

### 3. Free Tier Quality Matters

**Best free tiers for getting started:**
1. **Cassandra Astra:** 25GB + 25M operations (most generous)
2. **DynamoDB:** 25GB permanent (AWS lock-in)
3. **Firestore:** 1GB + 50K reads/day (mobile-friendly)
4. **MongoDB Atlas:** 512MB (smallest but works)

**Worst free tiers:**
- Redis Enterprise: 30MB (too small)
- ScyllaDB: None (trial only)
- Neo4j Aura: 200K nodes, pauses after 3 days

---

### 4. Performance Leaders by Category

**Latency (<1ms p99):**
- Redis Enterprise
- ScyllaDB Cloud

**Throughput (500K+ ops/sec/node):**
- ScyllaDB Cloud
- Redis Enterprise

**Write Performance:**
- ScyllaDB: 8,300 writes/sec
- Cassandra: 830 writes/sec (10× slower, Java overhead)

**Query Power:**
- MongoDB: Best aggregation pipeline
- Cosmos DB: Good SQL queries
- Neo4j: Best graph (600× faster than SQL for traversals)

---

### 5. Lock-in Risk Spectrum

**Lowest lock-in (can self-host or migrate):**
- Cassandra/Astra: CQL standard, self-host available
- ScyllaDB: CQL + DynamoDB API, open source
- MongoDB: Wire protocol, Community edition
- Redis: RESP protocol, Valkey fork
- Neo4j: openCypher, Community edition

**Highest lock-in (proprietary APIs):**
- DynamoDB: AWS-only, proprietary API
- Firestore: GCP-only, proprietary real-time
- Cosmos DB: Azure-only, RU system

**Mitigation:** All have export tools, but migration = application rewrite

---

### 6. Feature Trade-offs Matrix

| Need | Best Choice | Trade-off |
|------|-------------|-----------|
| Complex queries | MongoDB | Higher cost |
| Simple key-value | DynamoDB | Limited queries |
| Real-time sync | Firestore | GCP lock-in |
| Massive writes | Cassandra/ScyllaDB | No aggregations |
| Graph relationships | Neo4j | Specialized only |
| Ultra-low latency | Redis/ScyllaDB | Memory cost / minimum spend |
| Multi-model | Cosmos DB | Complexity |

---

### 7. Break-Even Points

**When to self-host vs managed:**
- **<100GB:** Always use managed (free tiers)
- **100GB-1TB:** Managed still cheaper (ops cost > infrastructure)
- **1TB-5TB:** Break-even zone (depends on ops expertise)
- **>5TB:** Consider self-hosting IF you have ops team
- **Specialized requirements:** Self-host (compliance, air-gapped, customization)

**Example:** Self-hosted Cassandra costs $3,800-6,800/month at 1TB (infrastructure + ops) vs Astra $375/month

---

### 8. Cost Optimization Strategies

**Small scale (<100GB):**
- Use free tiers
- DynamoDB serverless for unpredictable load
- MongoDB serverless for documents
- Cassandra serverless for time-series

**Medium scale (100GB-1TB):**
- DynamoDB provisioned (massive savings vs on-demand)
- Cassandra serverless (best for writes)
- MongoDB dedicated instances (M20-M40)

**Large scale (>1TB):**
- DynamoDB provisioned with reserved capacity
- Self-hosted Cassandra (if ops team exists)
- MongoDB dedicated with multi-year commit

---

### 9. Real-World Performance Insights

**Discord:** Cassandra → ScyllaDB migration
- 70% cost reduction
- 10× performance improvement
- Same API (CQL compatible)

**Expedia:** DynamoDB at scale
- 200K requests/sec peak
- 100TB data
- $10K/month (predictable cost)

**eBay:** PostgreSQL → Neo4j for recommendations
- 50ms graph queries (vs 30 sec in SQL)
- 600× performance improvement

**Conclusion:** Picking the right database = 10-100× performance difference

---

### 10. Hidden Costs

**Beyond sticker price, consider:**
1. **Data transfer (egress):** Can double cloud costs
2. **Backups:** PITR adds 50-100% storage cost
3. **Multi-region:** 2-3× compute/storage cost
4. **Support:** Enterprise support = +20-30%
5. **Operations:** Self-hosted = $2-5K/month engineer time

**Example:** $100/month database → $250/month true TCO (backups, egress, support)

---

## Decision Framework

### Use MongoDB Atlas if:
- ✅ Document model fits data (nested JSON)
- ✅ Complex queries needed (aggregations, joins)
- ✅ Schema flexibility critical
- ✅ Budget allows ($50-1,500/month)
- ❌ NOT for: simple key-value, time-series at scale

### Use DynamoDB if:
- ✅ AWS ecosystem
- ✅ Key-value access patterns
- ✅ Serverless architecture
- ✅ Infinite scale needed
- ❌ NOT for: complex queries, multi-cloud

### Use Firestore if:
- ✅ Mobile app (iOS/Android/Flutter)
- ✅ Real-time sync required
- ✅ Offline support needed
- ✅ Firebase platform (auth, hosting, functions)
- ❌ NOT for: complex server-side queries, high read volume

### Use Cassandra/Astra if:
- ✅ Time-series data (IoT, logs, metrics)
- ✅ Write-heavy workload
- ✅ Massive scale (multi-TB)
- ✅ Budget-conscious ($4-375/month serverless)
- ❌ NOT for: complex queries, transactions, aggregations

### Use Redis Enterprise if:
- ✅ Dataset fits in memory (<100GB)
- ✅ Sub-millisecond latency critical
- ✅ Advanced data structures needed
- ✅ Real-time use cases
- ❌ NOT for: large persistent data, cost-sensitive

### Use Neo4j Aura if:
- ✅ Highly connected data (social networks)
- ✅ Graph traversals core feature
- ✅ Relationship-centric queries
- ✅ Graph algorithms needed
- ❌ NOT for: document storage, simple lookups

### Use Cosmos DB if:
- ✅ Azure ecosystem
- ✅ Multi-model flexibility needed
- ✅ Global distribution critical
- ✅ 99.999% SLA required
- ❌ NOT for: cost-sensitive, simple use cases

### Use ScyllaDB Cloud if:
- ✅ Ultra-low latency critical (<1ms p99)
- ✅ Millions of operations/sec needed
- ✅ Budget allows ($1,095+/month)
- ✅ Cassandra migration (CQL compatible)
- ❌ NOT for: small scale, budget-constrained

---

## Next Steps: S3 Need-Driven Scenarios

S3 will create business-driven decision trees:
1. Startup SaaS application
2. E-commerce platform
3. Social media / chat app
4. IoT / time-series analytics
5. Content management system
6. Gaming leaderboards

Each scenario will map requirements → database choice with TCO and migration paths.

---

**S2 Complete:** Feature matrix, pricing, performance benchmarks, synthesis
**Ready for:** S3 Need-Driven Scenarios
