# S2 Synthesis: Key Findings & Trade-Offs

**Research Date:** November 16, 2025
**Analysis:** Feature matrix (50+ features), Pricing TCO (6 scenarios), Performance benchmarks
**Focus:** Comprehensive comparison across all dimensions

---

## Top 10 Key Findings

### 1. Graph Algorithms Are Make-or-Break

**Finding:**
- 3 databases have rich algorithms: Neo4j (60+), Memgraph (30+), TigerGraph (30+)
- 4 databases have NO algorithms: Neptune, JanusGraph, Dgraph, ArangoDB (<10 basic)

**Impact:**
- **For knowledge graph (research project):** Eliminates Neptune, JanusGraph, Dgraph, ArangoDB
- **Winners:** Memgraph (30+ algorithms, $24/mo), Neo4j (60+ algorithms, $48/mo)

**Recommendation:**
- If algorithms critical (PageRank, community detection): Choose Neo4j or Memgraph
- If traversal-only: Dgraph, JanusGraph viable

---

### 2. Cost Variance is Massive (125× Difference!)

**Finding:**
- Hobby project: $0-$3,132/month (infinite variance, free tiers exist)
- Startup/knowledge graph: $24-$120/month (5× variance)
- Enterprise: $800-$2,000+/month (2.5× variance)

**Example (500 nodes, 5K edges):**
- Memgraph Community (self-hosted): $24/month
- Neo4j Community (self-hosted): $48/month (2× Memgraph)
- Neptune Serverless: $120/month (5× Memgraph)
- TigerGraph Cloud: $99/month (4× Memgraph)

**Recommendation:**
- **Small scale (<1M nodes):** Use self-hosted (2-5× cheaper than managed)
- **Enterprise scale:** Managed services competitive (ops cost amortized)

---

### 3. Memgraph is 10× Faster (But RAM-Limited)

**Finding:**
- Memgraph (in-memory): <1ms single-hop, 10-50K qps reads
- Neo4j (disk-based): 1-3ms single-hop, 1-5K qps reads
- **10× performance advantage for Memgraph on reads**

**BUT:**
- Memgraph limited by RAM (1M nodes ≈ 10-20GB RAM)
- At 100M nodes: Memgraph needs 1TB+ RAM ($1,500+/month, expensive)
- Neo4j scales to 100M nodes on cheaper disk storage

**Recommendation:**
- **<10M nodes:** Memgraph best (performance + cost)
- **>10M nodes:** TigerGraph or JanusGraph (distributed, cheaper per node)

---

### 4. Write Throughput Varies 100× (100 wps vs 10,000 wps)

**Finding:**
- **Write-limited:** Neo4j (100-500 wps), Memgraph (100-500 wps), Neptune (100-300 wps)
- **Write-optimized:** JanusGraph (1,000-10,000 wps), TigerGraph (1,000-10,000 wps)
- **100× difference!**

**Impact:**
- **Read-heavy workload:** Any database works
- **Write-heavy (IoT, logging):** Must use JanusGraph or TigerGraph

**Recommendation:**
- **<500 writes/second:** Neo4j or Memgraph OK
- **>1,000 writes/second:** JanusGraph (Cassandra backend) or TigerGraph

---

### 5. Lock-In Spectrum: Low (JanusGraph) to Highest (TigerGraph)

**Finding:**
- **Lowest lock-in:** JanusGraph (Apache open source, Gremlin standard)
- **Low lock-in:** Memgraph (openCypher, Community Edition), Dgraph (Apache, GraphQL)
- **Medium lock-in:** Neo4j (Cypher leader, Community Edition available)
- **High lock-in:** ArangoDB (AQL proprietary), Neptune (AWS-only)
- **Highest lock-in:** TigerGraph (GSQL 100% proprietary, no open source)

**Migration Complexity:**
- **Low (1-2 weeks):** Memgraph ↔ Neo4j (openCypher compatible)
- **Medium (1-2 months):** Neo4j → Gremlin database (Cypher → Gremlin rewrite)
- **High (2-3 months):** TigerGraph → anything (GSQL proprietary)

**Recommendation:**
- **Avoid lock-in:** Use JanusGraph (Gremlin), Memgraph (openCypher), Dgraph (open source)
- **Accept lock-in for features:** Neo4j (60+ algorithms worth it), TigerGraph (performance worth it for enterprise)

---

### 6. Single-Node vs Distributed: Break-Even at 10M Nodes

**Finding:**
- **Single-node (Neo4j, Memgraph):** Great up to 10M nodes, then limited
- **Distributed (JanusGraph, TigerGraph, Dgraph):** Complex ops, but scales to billions

**Cost Break-Even:**
- **<10M nodes:** Single-node cheaper ($84/mo vs $1,500/mo for distributed)
- **>10M nodes:** Distributed cheaper per node (linear scaling vs vertical scaling limits)

**Recommendation:**
- **<10M nodes:** Use single-node (Neo4j Community or Memgraph Community)
- **>10M nodes:** Use distributed (JanusGraph or TigerGraph)

---

### 7. Managed Services Are 2-5× More Expensive (But Worth It for Small Teams)

**Finding:**
- **Memgraph:** $24/mo self-hosted vs $49-199/mo managed (2-8× premium)
- **Neo4j:** $48/mo self-hosted vs $65-240/mo managed (1.4-5× premium)
- **Neptune:** $120/mo vs no self-host option (N/A)

**Break-Even Analysis:**
- Ops engineer: $2K/month effective cost (20% time on DB ops)
- Managed premium <$1,800/month = worth it for small teams

**Recommendation:**
- **Team <5 people:** Use managed services (Memgraph Cloud $49-199/mo, Neo4j Aura $65-240/mo)
- **Team >5 people with ops:** Self-host (2-5× cheaper)

---

### 8. Free Tiers Viable for Development/Staging

**Finding:**
- **Permanent free tiers:** Neo4j Aura (50K nodes), Dgraph Cloud (1GB), ArangoDB Cloud (4GB)
- **No free tier:** Neptune, TigerGraph (90-day trials only), Memgraph Cloud (14-day trial)

**Recommendation:**
- **Development/staging:** Use free tiers (Neo4j Aura, Dgraph, ArangoDB)
- **Production:** Self-host or paid managed

---

### 9. Neptune Has No Algorithms (Dealbreaker for Many Use Cases)

**Finding:**
- Neptune **does not include graph algorithms** (no PageRank, Louvain, centrality)
- Workarounds: Neptune Analytics ($17K/month!), or export + process externally
- **Impact:** Not suitable for algorithm-heavy workloads (knowledge graphs, social networks, recommendations)

**When Neptune Makes Sense:**
- AWS-committed (existing AWS infrastructure, IAM integration)
- Traversal-only workload (no algorithms needed)
- High availability critical (multi-AZ built-in)
- Budget >$200/month

**Recommendation:**
- **Avoid Neptune for knowledge graphs** (research project needs algorithms)
- **Consider Neptune only if AWS-committed + traversal-only**

---

### 10. Query Language Portability Matters

**Finding:**
- **High portability:** Gremlin (Apache standard), openCypher (multi-vendor)
- **Medium portability:** Cypher (Neo4j dominant, Memgraph compatible)
- **Low portability:** AQL (ArangoDB), GSQL (TigerGraph), DQL (Dgraph advanced queries)

**Migration Effort:**
- **Gremlin → Gremlin:** 1-2 weeks (JanusGraph ↔ Neptune)
- **openCypher → Cypher:** 1-2 weeks (Memgraph ↔ Neo4j)
- **Cypher → Gremlin:** 1-2 months (complete rewrite)
- **GSQL → anything:** 2-3 months (proprietary, no equivalent)

**Recommendation:**
- **Low lock-in:** Use Gremlin (JanusGraph, Neptune) or openCypher (Memgraph)
- **Accept lock-in:** Neo4j (Cypher leader, worth it for algorithms), TigerGraph (GSQL proprietary, worth it for performance)

---

## Decision Matrix: Use Cases → Database

### Use Case: Knowledge Graph (Research Project, 500 nodes, 5K edges)

**Requirements:**
- Graph algorithms (PageRank, community detection, centrality)
- Low cost (<$100/month)
- Low lock-in

**Recommendation:**
1. **Memgraph Community (self-hosted):** $24/mo, 30+ algorithms, low lock-in ✅
2. **Neo4j Community (self-hosted):** $48/mo, 60+ algorithms, medium lock-in ✅

**Avoid:**
- Neptune: $120/mo, no algorithms ❌
- TigerGraph: $99/mo, highest lock-in ❌
- JanusGraph: $100/mo, complex ops, no algorithms ❌
- Dgraph: $24/mo, but no algorithms ❌

---

### Use Case: Social Network (10M nodes, 100M edges, read-heavy)

**Requirements:**
- Massive scale (billions of edges potential)
- Read-heavy (low latency critical)
- Real-time recommendations

**Recommendation:**
1. **TigerGraph Enterprise:** $5,000/mo, distributed MPP, best deep-link analytics ✅
2. **JanusGraph (self-hosted):** $3,000/mo, proven to trillions of edges ✅

**Avoid:**
- Neo4j: Single node limited, max ~50M edges ❌
- Memgraph: In-memory expensive at scale ($1,500+/mo for 128GB RAM) ❌
- Neptune: Slow (200-1000ms deep traversal) ❌

---

### Use Case: IoT / Write-Heavy (5M nodes, 100M writes/month)

**Requirements:**
- High write throughput (10K+ wps)
- Time-series queries
- Cost-effective at scale

**Recommendation:**
1. **JanusGraph (self-hosted):** $1,500/mo, Cassandra backend (write-optimized) ✅
2. **TigerGraph Enterprise:** $3,000/mo, distributed MPP, balanced reads/writes ✅

**Avoid:**
- Neo4j: Limited writes (100-500 wps) ❌
- Memgraph: Limited writes (100-500 wps) ❌
- Neptune: Limited writes (100-300 wps) ❌

---

### Use Case: Startup SaaS (100K nodes, growing fast)

**Requirements:**
- Flexible schema
- Fast development (ship features quickly)
- Budget <$500/month

**Recommendation:**
1. **Memgraph Cloud:** $49-199/mo, managed, fast, low ops ✅
2. **Neo4j Aura Professional:** $65-240/mo, managed, best ecosystem ✅
3. **ArangoDB Cloud:** $20-150/mo, multi-model, cheapest managed ✅

**Avoid:**
- JanusGraph: Complex ops (not startup-friendly) ❌
- TigerGraph: $499/mo, too expensive ❌

---

### Use Case: Enterprise (1M nodes, compliance, HA required)

**Requirements:**
- High availability (99.9%+ uptime)
- Compliance (SOC 2, HIPAA)
- Enterprise SLAs

**Recommendation:**
1. **Memgraph Cloud Enterprise:** $799/mo, HA, compliance, good value ✅
2. **Neo4j Aura Enterprise:** $1,000+/mo, best ecosystem, proven ✅
3. **TigerGraph Enterprise:** $2,000+/mo, best performance, deep analytics ✅

**Avoid:**
- Self-hosted Community editions: No HA, no compliance ❌
- Dgraph: Limited enterprise features ❌

---

## Trade-Off Summary

| Database | Best Strength | Biggest Weakness | Sweet Spot |
|----------|---------------|------------------|------------|
| **Neo4j** | 60+ algorithms, best ecosystem | Enterprise license expensive ($150K+/yr), single-node limited | <10M nodes, algorithm-heavy, budget <$500/mo |
| **Memgraph** | 10× faster (in-memory), low lock-in | RAM-limited (expensive >10M nodes), smaller ecosystem | <10M nodes, read-heavy, real-time |
| **TigerGraph** | Best at massive scale, deep analytics | Expensive ($99-5,000/mo), highest lock-in (GSQL) | >10M nodes, enterprise budget, real-time analytics |
| **JanusGraph** | Proven to trillions of edges, write-optimized | Complex ops (3 systems), no algorithms, slower latency | >10M nodes, write-heavy, zero lock-in |
| **Neptune** | AWS-native, HA built-in, managed | No algorithms, expensive ($120-1,500/mo), AWS-only | AWS-committed, traversal-only, HA critical |
| **Dgraph** | GraphQL-native, open source, low cost | No algorithms, smaller ecosystem | API-first apps, GraphQL preference, low lock-in |
| **ArangoDB** | Multi-model (graph + doc + KV) | Limited algorithms (<10), high lock-in (AQL) | Multi-model needs, consolidate databases |

---

## Final Recommendations by Scenario

**Budget <$50/month:**
- Free tier: Neo4j Aura Free, Dgraph Cloud Free
- Self-hosted: Memgraph Community ($24/mo) ✅

**Budget $50-500/month:**
- Self-hosted: Neo4j Community ($48-84/mo), Memgraph Community ($24-84/mo)
- Managed: Memgraph Cloud ($49-199/mo), Neo4j Aura ($65-240/mo)

**Budget $500-2,000/month:**
- Managed enterprise: Memgraph Cloud Enterprise ($799/mo), Neo4j Aura Enterprise ($1,000/mo)
- Self-hosted cluster: JanusGraph ($500-1,500/mo)

**Budget >$2,000/month:**
- TigerGraph Enterprise (best performance, deep analytics)
- JanusGraph (largest scale, lowest cost per node)

**Algorithm requirements:**
- Rich algorithms (60+): Neo4j ✅
- Good algorithms (30+): Memgraph, TigerGraph ✅
- No algorithms: Avoid Neptune, JanusGraph, Dgraph, ArangoDB ❌

**Lock-in averse:**
- Lowest: JanusGraph (Gremlin), Memgraph (openCypher), Dgraph (open source) ✅
- Highest: TigerGraph (GSQL), ArangoDB (AQL), Neptune (AWS-only) ❌

**Performance critical:**
- Fastest reads: Memgraph (in-memory, <1ms) ✅
- Fastest writes: JanusGraph (Cassandra, 10K wps), TigerGraph (10K wps) ✅
- Balanced: TigerGraph (high reads + high writes) ✅

---

**Next:** S3 Need-Driven (Business Scenarios)
