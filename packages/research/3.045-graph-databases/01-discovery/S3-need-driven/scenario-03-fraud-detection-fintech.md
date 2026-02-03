# S3: Fraud Detection for Fintech

**Use Case:** Real-time fraud detection for payment processing platform
**Scale:** 5M users, 50M transactions/month, 20M relationships
**Queries:** Real-time risk scoring (<100ms), pattern detection
**Priority:** Low latency, real-time alerts, pattern analysis

---

## Business Context

**Problem:**
Fintech platform needs to detect fraudulent transactions in real-time:
1. **Ring detection:** Multiple accounts controlled by same fraudster
2. **Money laundering:** Circular money flow patterns (A → B → C → A)
3. **Collusion:** Multiple users coordinating suspicious activity
4. **Velocity checks:** User suddenly sending money to many new recipients
5. **Real-time scoring:** Risk score for every transaction (<100ms)

**Current State:**
- Using rules engine (PostgreSQL) with simple checks
- Cannot detect complex patterns (rings, money laundering circuits)
- High false positive rate (30% of alerts are legitimate transactions)
- Fraudsters adapt quickly (find gaps in simple rules)

**Desired State:**
- Graph-based fraud detection (detect rings, patterns, collusion)
- Real-time risk scoring (<100ms per transaction)
- Low false positive rate (<10% false positives)
- Adaptive patterns (machine learning on graph features)

---

## Data Model

### Nodes

**User:**
```json
{
  "user_id": "user_12345",
  "name": "Alice Smith",
  "email": "alice@example.com",
  "phone": "+1-555-0100",
  "created": "2024-06-15",
  "kyc_status": "verified"
}
```

**BankAccount:**
```json
{
  "account_id": "acct_67890",
  "bank": "Chase",
  "account_number": "****1234",
  "added": "2024-06-16"
}
```

**Device:**
```json
{
  "device_id": "device_abc123",
  "device_type": "iPhone 14",
  "fingerprint": "fp_xyz789",
  "ip_address": "192.168.1.100"
}
```

**Transaction:**
```json
{
  "tx_id": "tx_111222",
  "amount": 500.00,
  "currency": "USD",
  "timestamp": "2025-11-16T10:30:00Z",
  "status": "pending"
}
```

### Edges

**OWNS_ACCOUNT:**
```cypher
(user:User)-[:OWNS_ACCOUNT {verified: true, added: "2024-06-16"}]->(account:BankAccount)
```

**USED_DEVICE:**
```cypher
(user:User)-[:USED_DEVICE {first_seen: "2024-06-15", last_seen: "2025-11-16"}]->(device:Device)
```

**SENT_MONEY:**
```cypher
(sender:User)-[:SENT_MONEY {tx_id: "tx_111222", amount: 500, timestamp: "..."}]->(recipient:User)
```

**SHARES_DEVICE:**
```cypher
(user_a:User)-[:SHARES_DEVICE]->(device:Device)<-[:SHARES_DEVICE]-(user_b:User)
```

**SHARES_PHONE:**
```cypher
(user_a:User)-[:SHARES_PHONE {phone: "+1-555-0100"}]-(user_b:User)
```

---

## Fraud Detection Queries

### Query 1: Ring Detection (Shared Devices/Phones)

```cypher
// Find users sharing devices or phone numbers (fraud ring)
MATCH (user:User)-[:USED_DEVICE]->(device:Device)<-[:USED_DEVICE]-(other:User)
WHERE user <> other
WITH user, other, count(DISTINCT device) AS shared_devices
WHERE shared_devices >= 2
RETURN user.user_id, other.user_id, shared_devices
ORDER BY shared_devices DESC

// Or shared phone numbers
MATCH (user:User)-[:SHARES_PHONE]-(other:User)
RETURN user.user_id, other.user_id
```

**Use Case:** Fraudsters create multiple accounts from same device/phone
**Alert:** High risk (likely fraud ring)

**Performance:** <50ms (real-time transaction scoring)

---

### Query 2: Money Laundering (Circular Flows)

```cypher
// Detect circular money flow (A → B → C → A)
MATCH path = (user:User)-[:SENT_MONEY*2..5]->(user)
WHERE ALL(tx IN relationships(path) WHERE tx.timestamp > datetime() - duration({days: 30}))
WITH user, path,
     reduce(total = 0, tx IN relationships(path) | total + tx.amount) AS total_amount
WHERE total_amount > 1000
RETURN user.user_id, length(path) AS hops, total_amount
ORDER BY total_amount DESC
```

**Use Case:** Money laundering via circular transfers
**Alert:** High risk (investigate circular flows >$1K)

**Performance:** <200ms (batch analysis, not real-time)

---

### Query 3: Velocity Check (Sudden New Recipients)

```cypher
// User suddenly sending money to many new recipients (velocity spike)
MATCH (user:User {user_id: "user_12345"})-[tx:SENT_MONEY]->(recipient:User)
WHERE tx.timestamp > datetime() - duration({hours: 24})
WITH user, count(DISTINCT recipient) AS recipient_count,
     count(tx) AS tx_count,
     sum(tx.amount) AS total_amount
WHERE recipient_count > 5 OR tx_count > 10
RETURN user.user_id, recipient_count, tx_count, total_amount
```

**Use Case:** Compromised account (fraudster sends money to many recipients)
**Alert:** Medium risk (investigate velocity spikes)

**Performance:** <50ms (real-time transaction scoring)

---

### Query 4: First-Degree Connection Risk Score

```cypher
// Calculate risk score based on recipient's connections
MATCH (sender:User {user_id: "user_12345"})-[:SENT_MONEY]->(recipient:User)
OPTIONAL MATCH (recipient)-[:SENT_MONEY|OWNS_ACCOUNT|USED_DEVICE]-(connected)
WITH sender, recipient,
     count(DISTINCT connected) AS connections,
     recipient.kyc_status AS kyc_status
RETURN recipient.user_id,
       CASE
         WHEN kyc_status = 'unverified' THEN 50
         WHEN connections < 3 THEN 30
         ELSE 10
       END AS risk_score
```

**Use Case:** Score recipient based on network connections
**Alert:** High risk if recipient has few connections (new account) or unverified KYC

**Performance:** <50ms (real-time transaction scoring)

---

### Query 5: Community Detection (Fraud Networks)

```cypher
// Detect fraud networks (communities of suspicious users)
CALL louvain.get()
YIELD node, community_id
WHERE node:User
WITH community_id, collect(node.user_id) AS members, count(*) AS size
WHERE size >= 5
MATCH (member:User)-[tx:SENT_MONEY]->(recipient:User)
WHERE member.user_id IN members AND recipient.user_id IN members
WITH community_id, members, count(tx) AS internal_transactions
WHERE internal_transactions > 20
RETURN community_id, members, internal_transactions
ORDER BY internal_transactions DESC
```

**Use Case:** Identify fraud networks (communities with high internal transactions)
**Alert:** Investigate communities with >20 internal transactions

**Performance:** Batch (daily analysis, not real-time)

---

## Scale Projections

| Metric | Current | Year 2 | Year 3 |
|--------|---------|--------|--------|
| **Users** | 5M | 15M | 30M |
| **Transactions/Month** | 50M | 150M | 300M |
| **Avg Transactions/User** | 10/month | 10/month | 10/month |
| **Fraud Rate** | 0.5% | 0.3% (improved) | 0.2% (target) |
| **Real-Time Queries** | 50M/month (100ms) | 150M/month | 300M/month |
| **Batch Analytics** | Daily | Daily | Daily |

---

## Database Evaluation

### Requirements

**Must-Have:**
- ✅ Real-time queries (<100ms for transaction scoring)
- ✅ Pattern detection (rings, circular flows, velocity)
- ✅ Graph algorithms (community detection, PageRank)
- ✅ High read throughput (50M-300M queries/month = 20-120 qps avg, 1K-5K qps peak)
- ✅ Moderate write throughput (50M-300M transactions/month = 20-120 wps avg)

**Nice-to-Have:**
- ⚠️ Machine learning integration (graph features → ML models)
- ⚠️ Real-time alerting (webhooks, notifications)

---

## Option 1: Neo4j Aura Professional ✅ RECOMMENDED

**Pricing:**
- Year 1 (5M users, 50M tx/month): $240/month (16GB RAM)
- Year 3 (30M users, 300M tx/month): $480/month (32GB RAM)
- **3-Year TCO: ~$13,000**

**Pros:**
- ✅ **Best graph algorithms** (60+: PageRank, Louvain, cycle detection)
- ✅ **Fast queries** (<50ms for 2-3 hop traversals)
- ✅ **Managed service** (eliminate ops)
- ✅ **Best ecosystem** (fraud detection examples, tutorials, integrations)
- ✅ **Cypher** (most readable for pattern detection)
- ✅ **Neo4j Fraud Detection Accelerator** (pre-built fraud queries)

**Cons:**
- ⚠️ Single-node limited (scales to ~30M users, sufficient for this use case)
- ⚠️ Some lock-in (GDS proprietary)
- ⚠️ Write throughput limited (100-500 wps, sufficient for 20-120 wps avg)

**Why Recommended:**
- Best for fraud detection (pre-built patterns, largest community)
- 60+ algorithms (cycle detection for money laundering, community detection for rings)
- Fast real-time queries (<50ms transaction scoring)
- Reasonable cost ($240-480/month = $13K over 3 years)
- Scale sufficient for 30M users (target met)

---

## Option 2: TigerGraph Enterprise ⚠️ IF NEED MASSIVE SCALE

**Pricing:**
- Year 1: $2,000/month
- Year 3: $3,000/month
- **3-Year TCO: ~$90,000**

**Pros:**
- ✅ Massive scale (100M+ users)
- ✅ Real-time deep-link analytics (20+ hop queries in seconds)
- ✅ 30+ graph algorithms
- ✅ High throughput (10K-50K qps)

**Cons:**
- ❌ Expensive ($90K vs Neo4j $13K, 7× cost)
- ❌ Overkill (designed for 100M+ users, this use case only 30M)
- ❌ Highest lock-in (GSQL proprietary)

**Choose TigerGraph if:**
- Need to scale beyond 30M users (100M+ users)
- Budget >$2K/month
- Deep-link analytics critical (20+ hop queries)

**Otherwise:** Neo4j better value (sufficient scale, 7× cheaper)

---

## Option 3: Memgraph Cloud ⚠️ IF NEED SUB-10MS LATENCY

**Pricing:**
- Year 1: $199/month (16GB RAM)
- Year 3: $799/month (64GB RAM)
- **3-Year TCO: ~$18,000**

**Pros:**
- ✅ **Fastest queries** (<1ms single-hop, 2-10ms 2-3 hop)
- ✅ 30+ graph algorithms (MAGE)
- ✅ Low lock-in (openCypher)
- ✅ Real-time streaming (Kafka integration)

**Cons:**
- ⚠️ In-memory = RAM-limited (30M users = 128GB+ RAM = $799/month)
- ⚠️ Smaller ecosystem (fewer fraud detection examples than Neo4j)
- ⚠️ 40% more expensive than Neo4j ($18K vs $13K)

**Choose Memgraph if:**
- Need sub-10ms queries (real-time = critical)
- Real-time streaming (Kafka ingestion of transactions)
- Low lock-in (openCypher portability)

**Otherwise:** Neo4j better (best fraud ecosystem, cheaper)

---

## Option 4: JanusGraph ❌ NOT RECOMMENDED

**Pricing:**
- Year 1: $1,500/month (distributed cluster)
- Year 3: $3,000/month
- **3-Year TCO: ~$80,000**

**Pros:**
- ✅ Lowest lock-in (Gremlin standard)
- ✅ Proven at scale (trillions of edges)

**Cons:**
- ❌ **No graph algorithms** (must build cycle detection, community detection custom)
- ❌ Slower queries (50-200ms vs Neo4j 10-50ms)
- ❌ Complex ops (JanusGraph + Cassandra + Elasticsearch)
- ❌ 6× cost of Neo4j ($80K vs $13K)

**Why NOT Recommended:**
- No algorithms = dealbreaker (fraud detection requires cycle detection, community detection)
- 6× cost of Neo4j without algorithms = poor value
- Complex ops not justified for this scale

---

## Option 5: Neptune ❌ NOT RECOMMENDED

**Pricing:**
- Year 1: $1,500/month (db.r6g.xlarge + replicas)
- Year 3: $3,000/month (db.r6g.2xlarge + replicas)
- **3-Year TCO: ~$80,000**

**Pros:**
- ✅ AWS-native (if already on AWS)
- ✅ Managed service
- ✅ HA built-in

**Cons:**
- ❌ **No graph algorithms** (Neptune Analytics $17K/month extra!)
- ❌ 6× cost of Neo4j ($80K vs $13K)
- ❌ Slower queries (50-200ms vs Neo4j 10-50ms)

**Why NOT Recommended:**
- No algorithms = dealbreaker for fraud detection
- 6× cost of Neo4j without better value
- Only choose if AWS-committed AND don't need algorithms

---

## Final Recommendation

### Winner: Neo4j Aura Professional

**Reasoning:**
- ✅ **Best for fraud detection** (60+ algorithms, pre-built patterns, largest community)
- ✅ **Fast real-time queries** (<50ms transaction scoring, <100ms pattern detection)
- ✅ **Reasonable cost** ($240-480/month = $13K over 3 years)
- ✅ **Scale sufficient** (30M users target met)
- ✅ **Managed service** (eliminate ops burden)
- ✅ **Best ecosystem** (fraud detection examples, tutorials, Neo4j Fraud Detection Accelerator)

**Cost Comparison (3-Year TCO):**
1. Neo4j Aura: $13K ✅ (best value, best algorithms)
2. Memgraph Cloud: $18K (faster, but 40% more expensive)
3. TigerGraph: $90K (7× cost, overkill for 30M users)
4. JanusGraph: $80K (6× cost, no algorithms)
5. Neptune: $80K (6× cost, no algorithms)

**Alternative: Memgraph Cloud if:**
- Need sub-10ms queries (real-time critical)
- Real-time streaming (Kafka ingestion)
- Budget allows $18K (vs Neo4j $13K)

---

## Implementation Plan

**Phase 1: Setup (Month 1)**
1. Deploy Neo4j Aura Professional (16GB RAM)
2. Load user data, bank accounts, devices, transactions
3. Create relationships (OWNS_ACCOUNT, USED_DEVICE, SENT_MONEY, SHARES_DEVICE, SHARES_PHONE)
4. Test queries (ring detection, circular flows, velocity)

**Phase 2: Fraud Rules Migration (Month 2)**
1. Migrate existing fraud rules to Cypher queries
2. Implement ring detection (shared devices/phones)
3. Implement circular flow detection (money laundering)
4. Implement velocity checks (sudden new recipients)
5. Test false positive rate (<10% target)

**Phase 3: Real-Time Integration (Month 3)**
1. Integrate Neo4j with transaction processing (real-time scoring)
2. Webhook alerts (high-risk transactions → investigation queue)
3. A/B test (Neo4j graph scoring vs old rules engine)
4. Measure fraud detection rate (target: 0.3% fraud rate)

**Phase 4: Machine Learning (Month 4-5)**
1. Extract graph features (degree, betweenness, PageRank, community)
2. Train ML model on graph features (XGBoost, LightGBM)
3. Deploy ML-enhanced fraud scoring
4. Target: 0.2% fraud rate (40% improvement from 0.3%)

**Phase 5: Optimization (Month 6+)**
1. Tune query performance (indexes, caching)
2. Monitor scale (increase RAM as users grow)
3. Weekly fraud network analysis (Louvain community detection)
4. Monthly model retraining (adapt to new fraud patterns)

**Estimated Effort:** 6 months with 2-3 engineers

---

**Next:** S3 Synthesis
