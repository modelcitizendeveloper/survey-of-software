# S3 Synthesis: Need-Driven Recommendations

**Research Complete:** November 16, 2025
**Scenarios Analyzed:** 3 common use cases
**Approach:** Requirements-first → Database selection

---

## Key Insights from Business Scenarios

### 1. Use Case Determines Database Choice

**There is no "best NoSQL database" - only best for YOUR use case:**

| Use Case | Best Choice | 3-Year TCO | Key Reason |
|----------|-------------|------------|------------|
| **Startup SaaS** | Supabase | $600 | Best value, PostgreSQL portability |
| **Startup SaaS** | MongoDB Atlas | $4,260 | Best DX, flexible schema (worth premium) |
| **Mobile App** | Firestore | $13,500 | Real-time sync built-in, best mobile DX |
| **Mobile App** | AppSync + DynamoDB | $7,700 | 43% cheaper, AWS ecosystem |
| **IoT Time-Series** | InfluxDB Cloud | $25,560 | Purpose-built, 10× compression |
| **IoT Time-Series** | Cassandra Astra | $37,236 | General-purpose, write-optimized |

**Cost variance:** 22× difference ($600 Supabase vs $13,500 Firestore for mobile)

---

### 2. Developer Experience vs Cost Trade-off

**Premium DX databases:**
- **Firestore:** Best for mobile ($13,500 vs $7,700 AWS alternative)
  - Premium: +75% cost
  - Benefit: 50% faster development (real-time built-in)
  - **Verdict:** Worth it for time-to-market

- **MongoDB Atlas:** Best for documents ($4,260 vs $600 Supabase)
  - Premium: +610% cost
  - Benefit: Flexible schema, faster iteration
  - **Verdict:** Worth it if rapid changes expected

**Budget-friendly alternatives:**
- **Supabase:** PostgreSQL + real-time ($600 for SaaS)
- **DynamoDB + AppSync:** AWS serverless ($7,700 for mobile)
- **InfluxDB:** Specialized time-series ($25,560 for IoT)

**Rule of thumb:** Premium DX is worth 2-7× cost if it accelerates development

---

### 3. Free Tier Strategy

**Best free tier for each use case:**

**Startup SaaS:**
- Supabase: 500MB DB (enough for 100-1,000 users)
- MongoDB Atlas: 512MB (enough for 100-500 users)
- DynamoDB: 25GB (enough for 1,000-5,000 users)
- **Strategy:** Start free, pay when revenue-generating

**Mobile App:**
- Firestore: 1GB + 50K reads/day (enough for 500-1,000 users)
- **Strategy:** Stay on free tier for 6-12 months

**IoT:**
- Cassandra Astra: 25GB + 25M operations (enough for 100 devices)
- **Strategy:** Free tier for prototyping only (not production scale)

**Conclusion:** All major providers have viable free tiers for MVP

---

### 4. Cost Optimization Impact

**Batching saves 50-90% on writes:**
- InfluxDB naive: 2.6B writes = $520/month
- InfluxDB batched (100×): 26M writes = $5.20/month
- **Savings: 99%**

**Compression saves 70-90% on storage:**
- Raw Cassandra: 500GB × $0.25 = $125/month
- InfluxDB compressed (10:1): 50GB × $0.25 = $12.50/month
- **Savings: 90%**

**Caching saves 30-50% on reads:**
- Firestore naive: 500M reads = $300/month
- Firestore with client cache: 250M reads = $150/month
- **Savings: 50%**

**Takeaway:** Naive usage = 2-10× higher cost than optimized

---

### 5. Lock-in Risk by Use Case

**Low lock-in choices:**
- **Supabase (PostgreSQL):** Can migrate to any Postgres provider (1 day)
- **Cassandra (CQL):** Can migrate to ScyllaDB or self-hosted (1 week)
- **MongoDB:** Can migrate to self-hosted or DocumentDB (1 week)

**Medium lock-in:**
- **MongoDB Atlas:** Self-host option exists, but features differ
- **Redis:** Valkey fork available (low-risk)
- **Neo4j:** Community edition available (limited features)

**High lock-in:**
- **Firestore:** Real-time sync is proprietary (2-3 months to migrate)
- **DynamoDB:** No compatible alternative (2-3 months rewrite)
- **Cosmos DB:** RU model unique (2-3 months rewrite)

**Mitigation:**
- Use abstraction layer (database access wrapper)
- Regular exports (JSON backups)
- Design for portability (avoid proprietary features)

**Pragmatic view:** Lock-in premium worth it if DX significantly better

---

### 6. Scalability Triggers

**When to upgrade/migrate:**

**Startup SaaS:**
- **0-1K users:** Free tier (Supabase, MongoDB, DynamoDB)
- **1K-10K users:** Paid tier ($5-50/month)
- **10K-50K users:** Dedicated instances ($50-200/month)
- **50K-500K users:** Optimize or self-host (>$500/month)

**Mobile App:**
- **0-1K users:** Free tier (Firestore)
- **1K-10K users:** Paid tier ($50-200/month)
- **10K-100K users:** Optimize pricing ($200-500/month)
- **100K-1M users:** Consider alternatives ($500-2,000/month)

**IoT:**
- **<1K devices:** Free tier (Cassandra Astra)
- **1K-10K devices:** Serverless ($100-500/month)
- **10K-100K devices:** Provisioned or self-hosted ($500-5,000/month)
- **>100K devices:** Self-hosted Cassandra (>$5,000/month)

**Break-even for self-hosting:** Usually $3,000-5,000/month managed spend

---

### 7. Architecture Patterns by Use Case

**Startup SaaS (Document Model):**
```
Frontend → API → MongoDB/Supabase → Backup to S3
                    ↓
              Search Index (optional)
```

**Mobile App (Real-Time Sync):**
```
Mobile App → Firestore/AppSync → Cloud Functions → External Services
    ↓              ↓
  Offline      Real-time Sync
  Cache        (WebSocket)
```

**IoT Time-Series (Write-Heavy):**
```
Devices → MQTT Broker → Batch Writer → InfluxDB/Cassandra
                                             ↓
                                        Dashboards
                                        (Grafana)
```

**Common pattern:** Separate hot data (NoSQL) from cold data (S3/data warehouse)

---

### 8. When to Use SQL Instead of NoSQL

**Use PostgreSQL (not NoSQL) if:**
- ✅ Relational data with many joins
- ✅ ACID transactions critical (financial systems)
- ✅ Complex queries with aggregations (reporting)
- ✅ Data fits in single server (<1TB, vertical scaling OK)
- ✅ Team knows SQL well (no learning curve)

**Use NoSQL if:**
- ✅ Schema flexibility needed (rapid iteration)
- ✅ Horizontal scaling required (multi-TB data)
- ✅ Specific data model (documents, time-series, graph)
- ✅ High-throughput writes (>10K writes/sec)
- ✅ Real-time sync needed (mobile apps)

**Hybrid approach:**
- Use PostgreSQL for transactional data (orders, users)
- Use NoSQL for analytics data (events, logs)
- Use both (e.g., Postgres for profiles + Firestore for chat)

**Pragmatic:** Start with PostgreSQL unless clear NoSQL need

---

### 9. Total Cost of Ownership Beyond Database

**Hidden costs:**
1. **Data transfer (egress):** 10-30% of database cost
2. **Backups:** 20-50% of storage cost
3. **Multi-region:** 2-3× database cost
4. **Support:** 20-30% upcharge for enterprise
5. **Migration cost:** $10K-50K engineer time if switch

**Example (Firestore):**
- Database: $400/month
- Egress (10GB/month): $50/month
- Backups: $20/month
- Functions: $30/month
- **True TCO: $500/month** (25% higher than database alone)

**Budget rule:** Database cost × 1.25-1.5 = true TCO

---

### 10. Recommended Decision Process

**Step 1: Identify primary use case**
- Documents (content, settings) → MongoDB, Firestore
- Key-value (sessions, carts) → DynamoDB, Redis
- Time-series (IoT, logs) → InfluxDB, Cassandra
- Real-time sync (mobile, chat) → Firestore, AppSync
- Graph (social, recommendations) → Neo4j

**Step 2: Determine budget constraint**
- Bootstrap (<$100/month) → Free tiers, Supabase
- Seed ($100-500/month) → Serverless options
- Series A ($500-5K/month) → Managed services
- Series B+ (>$5K/month) → Self-hosted option

**Step 3: Assess lock-in tolerance**
- Low tolerance → PostgreSQL (Supabase), Cassandra (CQL)
- Medium tolerance → MongoDB, Redis
- High tolerance → Firestore, DynamoDB (worth it for DX)

**Step 4: Calculate 3-year TCO**
- Use pricing calculator
- Include: database + storage + egress + backups
- Multiply by 1.25-1.5× for true cost

**Step 5: Prototype on free tier**
- Test developer experience
- Validate performance
- Measure actual costs (reads/writes/storage)

**Step 6: Re-evaluate at scale**
- <$3K/month → Stay on managed
- $3K-5K/month → Optimize pricing
- >$5K/month → Consider self-hosting

---

## Scenario Summary Table

| Scenario | Best DB | Why | 3-Yr TCO | Lock-in | Alternative |
|----------|---------|-----|----------|---------|-------------|
| **Startup SaaS** | Supabase | Best value + portability | $600 | Low (Postgres) | MongoDB ($4,260) |
| **Mobile App** | Firestore | Real-time sync DX | $13,500 | High | AppSync ($7,700) |
| **IoT Time-Series** | InfluxDB | Purpose-built, compression | $25,560 | High | Cassandra ($37,236) |

---

**Next:** S4 Strategic Selection (vendor viability, 5-year outlook, lock-in mitigation)
