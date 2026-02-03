# S2: Pricing & Total Cost of Ownership Analysis

**Research Date:** November 16, 2025
**Methodology:** 6 realistic scenarios across 8 providers
**Time Horizon:** 3 years projected

---

## TCO Scenarios

We analyze 6 common scenarios to understand true cost:

1. **Hobby Project:** Minimal usage, free tier only
2. **Startup MVP:** 10GB data, 10M reads/month, 1M writes/month
3. **Growing SaaS:** 100GB data, 100M reads/month, 10M writes/month
4. **Enterprise Scale:** 1TB data, 1B reads/month, 100M writes/month
5. **Real-Time Mobile App:** 50GB data, 500M reads/month (real-time sync)
6. **IoT Time-Series:** 500GB data, 50M writes/month (write-heavy)

---

## Scenario 1: Hobby Project (Free Tier Only)

**Requirements:**
- Storage: <1GB
- Reads: <1M/month
- Writes: <100K/month
- Use case: Side project, personal app, learning

### Cost Comparison

| Provider | Free Tier | Limitations | Best For |
|----------|-----------|-------------|----------|
| **Cassandra Astra** | 25GB, 25M ops | Single region | ✅ Most generous |
| **DynamoDB** | 25GB, 25 RCU/WCU | AWS only | ✅ AWS ecosystem |
| **Firestore** | 1GB, 50K reads/day | GCP only | ✅ Mobile apps |
| **MongoDB Atlas** | 512MB | Shared cluster, slow | ⚠️ Limited storage |
| **Neo4j Aura** | 200K nodes | Pauses after 3 days | ⚠️ Very limited |
| **Redis Enterprise** | 30MB | Too small | ❌ Not viable |
| **Cosmos DB** | 25GB, 1K RU/s | 12 months only | ⚠️ Time-limited |
| **ScyllaDB** | $300 credit (14 days) | Trial only | ❌ No free tier |

**Winner:** Cassandra Astra (25GB + 25M operations permanent)
**Runner-up:** DynamoDB (25GB + generous limits, AWS-only)

**Monthly Cost:** $0/month

---

## Scenario 2: Startup MVP

**Requirements:**
- Storage: 10GB
- Reads: 10M/month (~330K/day, ~230/min, ~4/sec)
- Writes: 1M/month (~33K/day, ~23/min, ~0.4/sec)
- Use case: Early SaaS product, 1,000-5,000 users

### Cost Breakdown

**MongoDB Atlas (Serverless):**
- Reads: 10M × $0.10/1M = $1.00
- Writes: 1M × $1.00/1M = $1.00
- Storage: 10GB × $0.25 = $2.50
- **Total: $4.50/month**

**DynamoDB (On-Demand):**
- Reads (eventually consistent): 10M × $0.25/1M = $2.50
- Writes: 1M × $1.25/1M = $1.25
- Storage: 10GB × $0.25 = $2.50
- **Total: $6.25/month**

**Firestore:**
- Reads: 10M × $0.06/100K = $6.00
- Writes: 1M × $0.18/100K = $1.80
- Storage: 10GB × $0.18 = $1.80
- **Total: $9.60/month**

**Cassandra Astra (Serverless):**
- Reads: 10M × $0.10/1M = $1.00
- Writes: 1M × $0.25/1M = $0.25
- Storage: 10GB × $0.25 = $2.50
- **Total: $3.75/month**

**Cosmos DB (Serverless, assumes 10M RUs for reads, 5M for writes):**
- RUs: 15M × $0.25/1M = $3.75
- Storage: 10GB × $0.25 = $2.50
- **Total: $6.25/month**

**Redis Enterprise:**
- 10GB memory: Not viable (too expensive ~$260/month)
- **Total: N/A** (use disk-based DB)

**Neo4j Aura (1GB RAM, 10GB storage):**
- Compute: $18/month
- Storage: 10GB × $0.10 = $1.00
- **Total: $19/month**

**ScyllaDB Cloud:**
- Minimum: 3-node cluster (~$1,095/month)
- **Total: $1,095/month** (not cost-effective for small scale)

### Ranking (Cheapest to Most Expensive)

1. **Cassandra Astra: $3.75/month** ← Best value
2. **MongoDB Atlas: $4.50/month** ← Good for documents
3. **Cosmos DB: $6.25/month**
4. **DynamoDB: $6.25/month** ← Best for AWS
5. **Firestore: $9.60/month** ← Premium for real-time
6. **Neo4j Aura: $19/month** ← Specialized (graph)
7. **Redis Enterprise: N/A**
8. **ScyllaDB: $1,095/month** ← Massive overkill

**Winner:** Cassandra Astra ($3.75/month)
**Best for Documents:** MongoDB Atlas ($4.50/month)
**Best for AWS:** DynamoDB ($6.25/month)

---

## Scenario 3: Growing SaaS

**Requirements:**
- Storage: 100GB
- Reads: 100M/month (~3.3M/day, ~2.3K/min, ~38/sec)
- Writes: 10M/month (~330K/day, ~230/min, ~4/sec)
- Use case: Growing startup, 10K-50K users, revenue-generating

### Cost Breakdown

**MongoDB Atlas (M20 Dedicated):**
- Instance: M20 (4GB RAM, 20GB storage) = $148/month
- Additional storage: 80GB × $0.08 = $6.40
- Data transfer: ~$5/month
- **Total: ~$160/month**

**DynamoDB (Provisioned):**
- Read capacity: 38 RCU × $0.09 = $3.42/month
- Write capacity: 4 WCU × $0.47 = $1.88/month
- Storage: 100GB × $0.25 = $25
- **Total: ~$30/month** ← Very competitive

**DynamoDB (On-Demand):**
- Reads: 100M × $0.25/1M = $25
- Writes: 10M × $1.25/1M = $12.50
- Storage: 100GB × $0.25 = $25
- **Total: $62.50/month**

**Firestore:**
- Reads: 100M × $0.06/100K = $60
- Writes: 10M × $0.18/100K = $18
- Storage: 100GB × $0.18 = $18
- **Total: $96/month**

**Cassandra Astra (Serverless):**
- Reads: 100M × $0.10/1M = $10
- Writes: 10M × $0.25/1M = $2.50
- Storage: 100GB × $0.25 = $25
- **Total: $37.50/month**

**Cosmos DB (400 RU/s provisioned):**
- 400 RU/s: $23.42/month
- Storage: 100GB × $0.25 = $25
- **Total: $48.42/month** (assumes efficient RU usage)

**Redis Enterprise:**
- 100GB memory: ~$2,600/month
- **Total: N/A** (not cost-effective)

**Neo4j Aura (4GB RAM, 100GB storage):**
- Compute: 4GB × $18 = $72/month
- Storage: 100GB × $0.10 = $10
- **Total: $82/month**

**ScyllaDB Cloud:**
- 3-node cluster: ~$1,095/month
- **Total: $1,095/month** (starting to make sense for write-heavy)

### Ranking

1. **DynamoDB (Provisioned): $30/month** ← Best if access patterns predictable
2. **Cassandra Astra: $37.50/month** ← Best for time-series
3. **Cosmos DB: $48.42/month**
4. **DynamoDB (On-Demand): $62.50/month**
5. **Neo4j Aura: $82/month** ← Specialized
6. **Firestore: $96/month**
7. **MongoDB Atlas: $160/month** ← Premium for documents
8. **ScyllaDB: $1,095/month**

**Winner:** DynamoDB Provisioned ($30/month) - if AWS + predictable load
**Best for Documents:** MongoDB Atlas ($160/month)
**Best for Time-Series:** Cassandra Astra ($37.50/month)

---

## Scenario 4: Enterprise Scale

**Requirements:**
- Storage: 1TB (1,000GB)
- Reads: 1B/month (~33M/day, ~23K/min, ~380/sec)
- Writes: 100M/month (~3.3M/day, ~2.3K/min, ~38/sec)
- Use case: Established company, 100K+ users, mission-critical

### Cost Breakdown

**MongoDB Atlas (M60):**
- Instance: M60 (64GB RAM, 400GB storage) = $1,480/month
- Additional storage: 600GB × $0.08 = $48
- **Total: ~$1,528/month**

**DynamoDB (Provisioned):**
- Read capacity: 380 RCU × $0.09 = $34.20/month
- Write capacity: 38 WCU × $0.47 = $17.86/month
- Storage: 1TB × $0.25 = $250
- **Total: ~$302/month** ← Extremely competitive

**Firestore:**
- Reads: 1B × $0.06/100K = $600
- Writes: 100M × $0.18/100K = $180
- Storage: 1TB × $0.18 = $180
- **Total: $960/month**

**Cassandra Astra (Serverless):**
- Reads: 1B × $0.10/1M = $100
- Writes: 100M × $0.25/1M = $25
- Storage: 1TB × $0.25 = $250
- **Total: $375/month** ← Very competitive

**Cosmos DB (10,000 RU/s provisioned):**
- 10,000 RU/s: $584/month
- Storage: 1TB × $0.25 = $250
- **Total: $834/month**

**ScyllaDB Cloud (6-node cluster for redundancy + performance):**
- 6× i4i.large: ~$2,190/month
- **Total: $2,190/month** (makes sense for ultra-low latency)

**Self-Hosted Cassandra (for comparison):**
- 6× c5.2xlarge (8 vCPU, 16GB RAM): ~$1,200/month
- Storage (6TB EBS): ~$600/month
- **Infrastructure: $1,800/month**
- **Operations (estimate): $2,000-5,000/month** (engineer time)
- **Total: $3,800-6,800/month** (higher ops cost)

### Ranking

1. **DynamoDB (Provisioned): $302/month** ← Best price/performance
2. **Cassandra Astra: $375/month** ← Best for time-series
3. **Cosmos DB: $834/month**
4. **Firestore: $960/month**
5. **MongoDB Atlas: $1,528/month**
6. **ScyllaDB: $2,190/month** ← Worth it for ultra-low latency
7. **Self-Hosted Cassandra: $3,800-6,800/month** ← Only if specialized needs

**Winner:** DynamoDB Provisioned ($302/month) - AWS + key-value
**Best for Documents:** MongoDB Atlas ($1,528/month) still reasonable
**Best for Time-Series:** Cassandra Astra ($375/month)
**Best for Ultra-Low Latency:** ScyllaDB ($2,190/month)

**Break-even for self-hosting:** ~5TB+ or specialized requirements (compliance, air-gapped)

---

## Scenario 5: Real-Time Mobile App

**Requirements:**
- Storage: 50GB
- Reads: 500M/month (real-time sync, many clients)
- Writes: 20M/month
- Real-time sync, offline support critical
- Use case: Social app, chat, collaborative tool

### Cost Breakdown

**Firestore (Native Mode):**
- Reads: 500M × $0.06/100K = $300
- Writes: 20M × $0.18/100K = $36
- Storage: 50GB × $0.18 = $9
- **Total: $345/month** ← Best for this use case

**MongoDB Atlas + Realm Sync:**
- Instance: M30 (8GB RAM) = $480/month
- Realm Sync: ~$100/month (estimate)
- **Total: ~$580/month**

**DynamoDB + AppSync (real-time):**
- DynamoDB reads: 500M × $0.25/1M = $125
- DynamoDB writes: 20M × $1.25/1M = $25
- Storage: 50GB × $0.25 = $12.50
- AppSync (GraphQL API): ~$100/month
- **Total: ~$262.50/month**

**Supabase (PostgreSQL + real-time):**
- Pro plan: $25/month (8GB DB, 50GB storage)
- Additional bandwidth: ~$50/month
- **Total: ~$75/month** ← Cheapest but different model (relational)

### Ranking (for NoSQL real-time)

1. **DynamoDB + AppSync: $262.50/month** ← AWS ecosystem
2. **Firestore: $345/month** ← Best DX, native real-time
3. **MongoDB + Realm: $580/month** ← Enterprise features

**Winner (NoSQL):** Firestore ($345/month) - easiest real-time implementation
**Winner (SQL alternative):** Supabase ($75/month) - if relational model works

---

## Scenario 6: IoT Time-Series (Write-Heavy)

**Requirements:**
- Storage: 500GB
- Reads: 10M/month (write-heavy, rare reads)
- Writes: 50M/month (continuous sensor data)
- Use case: IoT sensors, logs, metrics, events

### Cost Breakdown

**Cassandra Astra (Serverless):**
- Reads: 10M × $0.10/1M = $1.00
- Writes: 50M × $0.25/1M = $12.50
- Storage: 500GB × $0.25 = $125
- **Total: $138.50/month** ← Optimized for writes

**ScyllaDB Cloud (3-node):**
- 3× i4i.large: $1,095/month
- **Total: $1,095/month** (overkill for this scale)

**DynamoDB (Provisioned):**
- Read capacity: 4 RCU × $0.09 = $0.36/month
- Write capacity: 20 WCU × $0.47 = $9.40/month
- Storage: 500GB × $0.25 = $125
- **Total: $134.76/month** ← Very competitive

**MongoDB Atlas (M30):**
- Instance: M30 (8GB RAM) = $480/month
- Additional storage: 460GB × $0.08 = $36.80
- **Total: ~$517/month** (not optimized for time-series)

**InfluxDB Cloud (specialized time-series, for comparison):**
- Writes: 50M × $0.20/1M = $10
- Storage (compressed): 50GB × $0.25 = $12.50
- **Total: ~$22.50/month** ← Best for pure time-series

### Ranking

1. **InfluxDB Cloud: $22.50/month** ← Specialized time-series DB (not NoSQL general)
2. **DynamoDB: $134.76/month** ← AWS, key-value
3. **Cassandra Astra: $138.50/month** ← Best general NoSQL for time-series
4. **MongoDB Atlas: $517/month**
5. **ScyllaDB: $1,095/month**

**Winner (NoSQL):** Cassandra Astra ($138.50/month) or DynamoDB ($134.76/month)
**Winner (Specialized):** InfluxDB ($22.50/month) - if pure time-series

---

## 3-Year TCO Summary

Projected costs over 3 years (36 months) for Scenario 3 (Growing SaaS):

| Provider | Monthly | 3-Year Total | Notes |
|----------|---------|--------------|-------|
| DynamoDB (Prov) | $30 | $1,080 | Best value for AWS key-value |
| Cassandra Astra | $37.50 | $1,350 | Best for time-series |
| Cosmos DB | $48 | $1,728 | Azure multi-model |
| DynamoDB (On-Demand) | $62.50 | $2,250 | Unpredictable load |
| Neo4j Aura | $82 | $2,952 | Specialized graph |
| Firestore | $96 | $3,456 | Real-time mobile |
| MongoDB Atlas | $160 | $5,760 | Documents |
| ScyllaDB | $1,095 | $39,420 | Ultra-low latency |

**Cost Variance:** 36× difference (DynamoDB vs ScyllaDB)

---

## Key Insights

### 1. Free Tier Value
- **Cassandra Astra:** Most generous (25GB + 25M ops)
- **DynamoDB:** Best for AWS (25GB permanent)
- **Firestore:** Best for mobile (1GB + 50K reads/day)

### 2. Small Scale (<100GB)
- **DynamoDB serverless:** Best for key-value ($6-30/month)
- **MongoDB serverless:** Best for documents ($5-50/month)
- **Cassandra serverless:** Best for time-series ($4-38/month)

### 3. Medium Scale (100GB-1TB)
- **DynamoDB provisioned:** Unbeatable for predictable load ($30-300/month)
- **Cassandra Astra:** Best for write-heavy ($38-375/month)
- **MongoDB Atlas:** Premium but worth it for documents ($160-1,500/month)

### 4. Enterprise Scale (1TB+)
- **DynamoDB:** Still cheapest ($300+/month)
- **Cassandra Astra:** Competitive for time-series ($375+/month)
- **Self-hosted:** Only makes sense at 5TB+ or special requirements

### 5. Real-Time Mobile
- **Firestore:** Best DX for real-time ($100-500/month)
- **DynamoDB + AppSync:** Cheaper if AWS ($50-300/month)

### 6. Price/Performance Champions
- **Value:** DynamoDB (key-value), Cassandra Astra (time-series)
- **Premium:** MongoDB Atlas (documents), Firestore (mobile real-time)
- **Specialized:** Neo4j (graph), ScyllaDB (ultra-low latency)

---

**Next:** Performance benchmarks
