# S3 Synthesis: Business Scenario Recommendations

**Research Date:** November 16, 2025
**Scenarios Analyzed:** 3 (Knowledge Graph, Social Network, Fraud Detection)
**Focus:** Real-world use case → database selection

---

## Summary Table: Use Case → Recommended Database

| Use Case | Scale | Budget | Winner | 3-Year TCO | Reasoning |
|----------|-------|--------|--------|------------|-----------|
| **Knowledge Graph** | 500 nodes, 5K edges | <$100/mo | Memgraph Community | **$864** | Lowest cost, 30+ algorithms, low lock-in |
| **Social Network** | 10M→100M users, 100M→1B edges | $3K-10K/mo | TigerGraph Enterprise | **$200K** | Only database proven at 100M+ scale, <50ms latency |
| **Fraud Detection** | 5M→30M users, 50M→300M tx/mo | <$1K/mo | Neo4j Aura Professional | **$13K** | Best fraud ecosystem, 60+ algorithms, fast queries |

---

## Key Insights by Use Case

### Insight 1: Knowledge Graph (Research Project)

**Winner: Memgraph Community ($24/month, $864 over 3 years)**

**Why Memgraph Wins:**
- ✅ Lowest cost ($24/month, 3-4× cheaper than alternatives)
- ✅ Full MAGE algorithms (30+: PageRank, Louvain, centrality)
- ✅ Low lock-in (openCypher standard, migrate to Neo4j in 1-2 days)
- ✅ 10× faster than Neo4j (in-memory, <1ms queries)
- ✅ Perfect fit for 500 nodes (2-4GB RAM sufficient)

**Alternatives Considered:**
- Neo4j Community ($48/mo, $1,728): 2× cost, but 60+ algorithms (if need more)
- Dgraph ($24/mo): Same cost, but **no algorithms** (dealbreaker)
- Neptune ($120/mo): 5× cost, **no algorithms** (poor value)
- TigerGraph ($99/mo): 4× cost, overkill for 500 nodes

**Key Trade-Off:**
- Memgraph 30+ algorithms sufficient for knowledge graph
- Neo4j 60+ algorithms if need advanced analytics
- **Verdict:** Memgraph best value (sufficient algorithms, lowest cost)

**Cost Variance:** 5× ($24 Memgraph vs $120 Neptune)

---

### Insight 2: Social Network (10M→100M Users)

**Winner: TigerGraph Enterprise ($3K-10K/month, $200K over 3 years)**

**Why TigerGraph Wins:**
- ✅ Only database proven at 100M+ users with <50ms latency
- ✅ Real-time deep-link analytics (2-3 hop queries in 10-30ms)
- ✅ Distributed MPP (horizontal scaling, linear growth)
- ✅ 30+ graph algorithms (PageRank for influencers, Louvain for communities)
- ✅ High throughput (10K-50K qps reads, 10K wps writes)
- ✅ Cost justified ($10K/month = $0.0001/user at 100M users)

**Alternatives Considered:**
- JanusGraph ($1.5K-5K/mo, $110K): 50% cheaper, but **no algorithms**, complex ops
- Neo4j Enterprise ($12.7K/mo, $460K+): **Cannot scale** to 100M users (single-node limited), 2.3× cost
- Memgraph Enterprise ($800-3K/mo, $100K): **RAM-limited** (1TB RAM = $10K+/month at 100M users)
- Neptune ($2K-6K/mo, $150K): **No algorithms**, slower (50-200ms vs 10-30ms)

**Key Trade-Off:**
- TigerGraph $200K vs JanusGraph $110K (80% more expensive)
- But TigerGraph includes algorithms (worth it for influencer/community detection)
- Simpler ops (managed vs 30-node Cassandra cluster)
- Faster queries (10-30ms vs 50-200ms)
- **Verdict:** TigerGraph worth 80% premium (algorithms + performance + managed)

**Cost Variance:** 4.2× ($110K JanusGraph vs $460K Neo4j)

**Scale Break-Even:**
- <10M users: Single-node (Neo4j, Memgraph) sufficient
- >10M users: Distributed (TigerGraph, JanusGraph) required

---

### Insight 3: Fraud Detection (5M→30M Users)

**Winner: Neo4j Aura Professional ($240-480/month, $13K over 3 years)**

**Why Neo4j Wins:**
- ✅ **Best for fraud detection** (60+ algorithms, pre-built patterns, largest community)
- ✅ Fast real-time queries (<50ms transaction scoring)
- ✅ **Best ecosystem** (fraud detection tutorials, Neo4j Fraud Detection Accelerator)
- ✅ Reasonable cost ($240-480/month = $13K over 3 years)
- ✅ Scale sufficient (30M users target met)
- ✅ Managed service (eliminate ops burden)

**Alternatives Considered:**
- Memgraph Cloud ($199-799/mo, $18K): Faster (sub-10ms), but 40% more expensive, smaller fraud ecosystem
- TigerGraph ($2K-3K/mo, $90K): 7× cost, overkill for 30M users (designed for 100M+)
- JanusGraph ($1.5K-3K/mo, $80K): **No algorithms** (dealbreaker), 6× cost
- Neptune ($1.5K-3K/mo, $80K): **No algorithms** (dealbreaker), 6× cost

**Key Trade-Off:**
- Neo4j $13K vs Memgraph $18K (Memgraph 40% more expensive)
- Neo4j best fraud ecosystem (pre-built patterns, tutorials)
- Memgraph faster (sub-10ms vs 10-50ms), but fraud detection acceptable at 50ms
- **Verdict:** Neo4j best value (best fraud ecosystem, cheaper)

**Cost Variance:** 7× ($13K Neo4j vs $90K TigerGraph)

**Algorithm Importance:**
- Fraud detection requires cycle detection (money laundering), community detection (fraud rings)
- Eliminates JanusGraph, Neptune (no algorithms)

---

## Cross-Scenario Patterns

### Pattern 1: Graph Algorithms Are Critical for Most Use Cases

**Finding:**
- Knowledge graph: Needs PageRank, community detection (identify important research, clusters)
- Social network: Needs PageRank, community detection (influencers, interest groups)
- Fraud detection: Needs cycle detection, community detection (money laundering, fraud rings)

**Impact:**
- **Eliminates databases without algorithms:** Neptune, JanusGraph, Dgraph
- **Favors algorithm-rich databases:** Neo4j (60+), Memgraph (30+), TigerGraph (30+)

**Recommendation:**
- If algorithms critical: Choose Neo4j, Memgraph, or TigerGraph
- If traversal-only: Dgraph, JanusGraph viable

---

### Pattern 2: Scale Determines Database Choice

**Finding:**
| Scale | Recommended | Avoid |
|-------|-------------|-------|
| **Small (<1M nodes)** | Memgraph Community, Neo4j Community | TigerGraph (overkill), JanusGraph (complex ops) |
| **Medium (1M-10M nodes)** | Neo4j Aura, Memgraph Cloud | TigerGraph (overkill) |
| **Large (10M-100M nodes)** | TigerGraph Enterprise, JanusGraph | Neo4j (single-node limited), Memgraph (RAM-limited) |
| **Massive (100M+ nodes)** | TigerGraph Enterprise, JanusGraph | Neo4j (cannot scale), Memgraph (too expensive) |

**Break-Even Points:**
- **10M nodes:** Single-node → distributed transition
- **100M nodes:** Neo4j/Memgraph max out, only TigerGraph/JanusGraph viable

---

### Pattern 3: Cost Scales Non-Linearly

**Finding:**
- Small scale (500 nodes): $24-120/month (5× variance)
- Medium scale (1M nodes): $240-3,000/month (12× variance)
- Large scale (10M nodes): $1,500-12,700/month (8× variance)

**Cost per Node:**
- Small scale: $0.05-0.24/node/month
- Medium scale: $0.0002-0.003/node/month
- Large scale: $0.00015-0.0013/node/month

**Insight:** Cost per node decreases as scale increases (economies of scale), but variance remains high (database choice matters).

---

### Pattern 4: Managed Services Premium Varies by Scale

**Finding:**
| Scale | Self-Hosted | Managed | Premium | Worth It? |
|-------|-------------|---------|---------|-----------|
| **Small (500 nodes)** | $24/mo | $49-120/mo | 2-5× | ✅ Yes (ops cost > premium) |
| **Medium (1M nodes)** | $84/mo | $240-800/mo | 3-10× | ⚠️ Maybe (depends on ops team) |
| **Large (10M nodes)** | $1.5K/mo | $3K-10K/mo | 2-7× | ⚠️ Maybe (ops team can manage distributed) |

**Break-Even Analysis:**
- Ops engineer: $2K/month effective cost (20% time on DB ops)
- Managed premium <$1,800/month = worth it

**Recommendation:**
- **Small teams (<5 people):** Use managed services (ops cost > premium)
- **Large teams (>10 people with ops):** Self-host (2-7× cheaper)

---

### Pattern 5: Lock-In Tolerance Varies by Use Case

**Finding:**
- **Knowledge graph (research project):** Low lock-in preferred (Memgraph openCypher, migrate to Neo4j easily)
- **Social network (10M+ users):** Lock-in acceptable if performance justifies (TigerGraph GSQL proprietary, but 10-30ms queries worth it)
- **Fraud detection (5M-30M users):** Medium lock-in acceptable (Neo4j GDS proprietary, but best fraud ecosystem worth it)

**Trade-Off:**
- Low lock-in (Gremlin, openCypher) → Easier migration (1-2 weeks)
- High lock-in (GSQL, Neo4j GDS) → Better features/performance, but migration 2-3 months

**Recommendation:**
- **Startups (0-3 years):** Accept lock-in for speed (Neo4j Aura, TigerGraph Cloud)
- **Enterprises (5-10 years):** Choose low lock-in (JanusGraph Gremlin, Memgraph openCypher)

---

## Decision Framework: Use Case → Database

### Step 1: What's Your Scale?

**<1M nodes:**
- Budget <$100/mo: Memgraph Community ($24/mo) or Neo4j Community ($48/mo)
- Budget >$100/mo: Neo4j Aura ($65-240/mo) or Memgraph Cloud ($49-199/mo)

**1M-10M nodes:**
- Budget <$1K/mo: Neo4j Aura ($240-800/mo), Memgraph Cloud ($199-799/mo)
- Budget >$1K/mo: Self-hosted Neo4j or Memgraph

**10M-100M nodes:**
- Budget >$3K/mo: TigerGraph Enterprise ($3K-10K/mo)
- Budget-conscious: JanusGraph self-hosted ($1.5K-5K/mo, but no algorithms)

**>100M nodes:**
- Only options: TigerGraph Enterprise, JanusGraph

---

### Step 2: Do You Need Graph Algorithms?

**Yes (PageRank, community detection, centrality):**
- Neo4j (60+ algorithms), Memgraph (30+), TigerGraph (30+)
- **Avoid:** Neptune, JanusGraph, Dgraph (no algorithms)

**No (traversal-only):**
- Dgraph (GraphQL-native), JanusGraph (Gremlin standard), Neptune (if AWS-committed)

---

### Step 3: What's Your Latency Requirement?

**<10ms (real-time critical):**
- Memgraph (in-memory, <1ms queries)

**<50ms (user-facing):**
- Neo4j (10-50ms), TigerGraph (10-30ms), Memgraph (2-10ms)

**<200ms (acceptable for most use cases):**
- All databases acceptable

**>200ms (batch analytics):**
- Any database works

---

### Step 4: What's Your Budget?

**<$100/month:**
- Free tiers (Neo4j Aura Free, Dgraph Cloud Free)
- Self-hosted: Memgraph Community ($24/mo), Dgraph ($24/mo)

**$100-1,000/month:**
- Managed: Neo4j Aura ($65-800/mo), Memgraph Cloud ($49-799/mo)
- Self-hosted: Neo4j, Memgraph

**>$1,000/month:**
- TigerGraph Enterprise (massive scale)
- JanusGraph (distributed self-hosted)
- Neo4j Aura Enterprise

---

### Step 5: Lock-In Tolerance?

**Low lock-in (easy migration):**
- JanusGraph (Gremlin standard), Memgraph (openCypher), Dgraph (open source)

**Medium lock-in (acceptable if features justify):**
- Neo4j (Cypher leader, GDS proprietary)

**High lock-in (performance justifies):**
- TigerGraph (GSQL proprietary, but best performance)

---

## Final Recommendations by Scenario

**Knowledge Graph (500 nodes, <$100/mo):**
1. **Memgraph Community** ($24/mo) ✅
2. Neo4j Community ($48/mo) ⚠️ (if need >30 algorithms)

**Social Network (10M-100M users, $3K-10K/mo):**
1. **TigerGraph Enterprise** ($3K-10K/mo) ✅
2. JanusGraph ($1.5K-5K/mo) ⚠️ (if no algorithms needed, budget-conscious)

**Fraud Detection (5M-30M users, <$1K/mo):**
1. **Neo4j Aura Professional** ($240-480/mo) ✅
2. Memgraph Cloud ($199-799/mo) ⚠️ (if need sub-10ms latency)

**General Purpose (unknown scale):**
- Start with Neo4j Aura Free (free tier)
- Upgrade to Neo4j Aura Professional or Memgraph Cloud as scale grows
- Migrate to TigerGraph or JanusGraph if exceed 10M nodes

---

**Next:** S4 Strategic Analysis (Vendor viability, lock-in mitigation, migration complexity)
