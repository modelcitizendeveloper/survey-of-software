# S2: Pricing TCO (Total Cost of Ownership)

**Research Date:** November 16, 2025
**Analysis Period:** 3 years (36 months)
**Scenarios:** 6 (hobby, startup, growing, enterprise, knowledge graph, social network)

---

## Scenario 1: Hobby Project / Side Project

**Workload:**
- 1,000 nodes, 10,000 edges
- 10K queries/month, 1K writes/month
- Development/staging only

### Cost Analysis (3-Year TCO)

| Provider | Setup | Tier | Monthly Cost | 3-Year Total |
|----------|-------|------|--------------|--------------|
| **Memgraph Community (self-hosted)** | DigitalOcean 2GB Droplet | Free license | **$12** | **$432** |
| **Dgraph (self-hosted)** | DigitalOcean 2GB Droplet | Open source | **$12** | **$432** |
| **Neo4j Aura Free** | Managed | Free tier | **$0** | **$0** ✅ |
| **Dgraph Cloud Free** | Managed | Free tier | **$0** | **$0** ✅ |
| **ArangoDB Cloud Free** | Managed | Free tier | **$0** | **$0** ✅ |
| **Neo4j Community (self-hosted)** | DigitalOcean 4GB Droplet | Free license | **$24** | **$864** |
| **Neptune Serverless** | AWS managed | Serverless (1 NCU) | **$87** | **$3,132** |
| **TigerGraph Cloud** | Managed | No free tier (trial) | **$99** | **$3,564** |

**Winner:** Neo4j Aura Free or Dgraph Cloud Free ($0/month)

**Key Insight:**
- Free tiers viable for hobby projects (Neo4j Aura, Dgraph, ArangoDB)
- Self-hosted cheapest if free tier insufficient ($12-24/month)
- Neptune/TigerGraph too expensive (7-8× cost) for hobby scale

---

## Scenario 2: Startup MVP / Knowledge Graph (Research Project)

**Workload:**
- 100-500 nodes, 500-5,000 edges
- 100K queries/month, 10K writes/month
- Need graph algorithms (PageRank, community detection)
- Budget-conscious

### Cost Analysis (3-Year TCO)

| Provider | Setup | Tier | Monthly Cost | 3-Year Total |
|----------|-------|------|--------------|--------------|
| **Memgraph Community (self-hosted)** | DigitalOcean 4GB Droplet | Free license + MAGE | **$24** | **$864** ✅ |
| **Dgraph (self-hosted)** | DigitalOcean 4GB Droplet | Open source | **$24** | **$864** ⚠️ |
| **Neo4j Community (self-hosted)** | DigitalOcean 8GB Droplet | Free license + GDS | **$48** | **$1,728** |
| **ArangoDB Community (self-hosted)** | DigitalOcean 4GB Droplet | Free license | **$24** | **$864** ⚠️ |
| **ArangoDB Cloud** | Managed | Developer tier | **$20** | **$720** ⚠️ |
| **Memgraph Cloud** | Managed | Starter tier | **$49** | **$1,764** |
| **Neo4j Aura Professional** | Managed | 4GB RAM | **$65** | **$2,340** |
| **Neptune Serverless** | AWS managed | 1-2 NCUs avg | **$120** | **$4,320** |
| **TigerGraph Cloud** | Managed | Developer tier | **$99** | **$3,564** |

**Winner:** Memgraph Community self-hosted ($24/month, $864 over 3 years)

**Reasoning:**
- Lowest cost + full MAGE algorithms (30+)
- ✅ Dgraph also $24/month, but **no algorithms** (disqualified for this use case)
- ✅ ArangoDB also $24/month, but **<10 basic algorithms** (not enough for research)
- Neo4j Community $48/month (2× cost, but 60+ algorithms if needed)

**Key Insight:**
- 5× cost variance ($24 Memgraph vs $120 Neptune)
- Algorithms are make-or-break (disqualifies Dgraph, ArangoDB, Neptune)
- Managed services 2-5× more expensive than self-hosted

---

## Scenario 3: Growing SaaS Product

**Workload:**
- 100,000 nodes, 1M edges
- 5M queries/month, 500K writes/month
- Need high availability (99.9% uptime)
- Team has ops resources

### Cost Analysis (3-Year TCO)

| Provider | Setup | Tier | Monthly Cost | 3-Year Total |
|----------|-------|------|--------------|--------------|
| **Memgraph Community (self-hosted)** | DigitalOcean 16GB Droplet | Free license | **$84** | **$3,024** ✅ |
| **Neo4j Community (self-hosted)** | DigitalOcean 16GB Droplet | Free license | **$84** | **$3,024** ✅ |
| **ArangoDB Community (self-hosted)** | 3× 8GB nodes (cluster) | Free license | **$144** | **$5,184** |
| **JanusGraph (self-hosted)** | JG 8GB + Cass 3×8GB | Open source | **$168** | **$6,048** |
| **Dgraph (self-hosted)** | 3× 8GB nodes (cluster) | Open source | **$144** | **$5,184** |
| **Memgraph Cloud** | Professional tier (16GB) | Managed | **$199** | **$7,164** |
| **ArangoDB Cloud** | Professional tier | Managed | **$150** | **$5,400** |
| **Neo4j Aura Professional** | 16GB RAM | Managed | **$240** | **$8,640** |
| **Neptune Provisioned** | db.r6g.xlarge (1yr reserved) | Managed | **$317** | **$11,412** |
| **TigerGraph Cloud** | Professional tier | Managed | **$499** | **$17,964** |

**Winner (Self-Hosted):** Memgraph or Neo4j Community ($84/month, $3,024 over 3 years)

**Winner (Managed):** ArangoDB Cloud ($150/month, $5,400 over 3 years)

**Key Insight:**
- Self-hosted 2-6× cheaper than managed ($84 vs $199-499)
- Neo4j Community viable (no Enterprise needed for single node)
- Memgraph Community limited to single node (no HA without Enterprise)
- Neptune/TigerGraph 4-6× more expensive than self-hosted

**High Availability Consideration:**
- Neo4j Community: ❌ Single node only (no clustering)
- Memgraph Community: ❌ Single node only (no clustering)
- **For HA:** Need Enterprise licenses (+$10K-50K/year) or use managed services

---

## Scenario 4: Enterprise Knowledge Graph

**Workload:**
- 1M nodes, 10M edges
- 50M queries/month, 5M writes/month
- Need high availability, compliance (SOC 2, HIPAA), multi-region
- Enterprise SLAs required

### Cost Analysis (3-Year TCO)

| Provider | Setup | Tier | Monthly Cost | 3-Year Total |
|----------|-------|------|--------------|--------------|
| **Neo4j Community (self-hosted)** | AWS r6g.2xlarge (1yr reserved) | Free license (single node) | **$212** | **$7,632** ⚠️ |
| **JanusGraph (self-hosted)** | 3× JG + 5× Cassandra nodes | Open source | **$840** | **$30,240** |
| **Neo4j Enterprise (self-hosted)** | 3× r6g.2xlarge + license | Enterprise license | **$636 + $12.5K/mo** | **$460K+** |
| **Memgraph Cloud** | Enterprise tier (64GB) | Managed | **$799** | **$28,764** |
| **Neo4j Aura Enterprise** | 32GB RAM + enterprise features | Managed | **$1,000+** | **$36,000+** |
| **ArangoDB Cloud Enterprise** | Custom sizing | Managed | **$800** | **$28,800** |
| **Neptune Provisioned** | db.r6g.4xlarge (1yr reserved) + replicas | Managed | **$1,500** | **$54,000** |
| **TigerGraph Enterprise** | Enterprise tier | Managed | **$2,000+** | **$72,000+** |

**Winner:** Memgraph Cloud Enterprise ($799/month, $28,764 over 3 years)

**Reasoning:**
- Includes HA (clustering), compliance, SLAs
- Neo4j Community insufficient (no clustering, no enterprise features)
- Neo4j Enterprise self-hosted extremely expensive ($150K/year license + infra)
- JanusGraph self-hosted cheaper but complex ops (multi-cluster management)

**Key Insight:**
- Enterprise features expensive ($800-2,000/month typical)
- Self-hosted Enterprise licenses $10K-50K+/year (Neo4j $150K+/year prohibitive)
- Managed enterprise services competitive vs self-hosted + license
- TigerGraph most expensive (2.5× Memgraph)

---

## Scenario 5: Social Network / Recommendation Engine

**Workload:**
- 10M nodes, 100M edges
- 200M queries/month (read-heavy)
- 10M writes/month
- Real-time recommendations (low latency critical)
- Massive scale (growth to 100M+ nodes expected)

### Cost Analysis (3-Year TCO)

| Provider | Setup | Tier | Monthly Cost | 3-Year Total |
|----------|-------|------|--------------|--------------|
| **Memgraph Cloud** | High-memory (128GB+) | Managed | **$1,500+** | **$54,000+** ⚠️ |
| **Neo4j Aura Professional** | 128GB RAM | Managed | **$1,200+** | **$43,200+** |
| **JanusGraph (self-hosted)** | 10× JG + 20× Cassandra | Open source | **$3,000** | **$108,000** ✅ |
| **TigerGraph Enterprise** | Distributed cluster | Managed | **$5,000+** | **$180,000+** |
| **Neptune Provisioned** | 5× db.r6g.8xlarge | Managed | **$4,000+** | **$144,000+** |

**Winner:** JanusGraph self-hosted ($3,000/month, $108,000 over 3 years)

**Reasoning:**
- Proven to trillions of edges (Netflix, Uber scale)
- Cassandra backend optimized for massive scale
- Complex ops acceptable for enterprise scale
- Memgraph limited (in-memory = RAM-constrained, expensive at 100M+ nodes)

**Key Insight:**
- At massive scale (10M+ nodes), distributed architectures win (JanusGraph, TigerGraph)
- In-memory databases (Memgraph) too expensive (RAM = $1,500/month for 128GB)
- Single-node databases (Neo4j, Memgraph) max out at ~100M edges
- TigerGraph best performance but 2× cost of JanusGraph

---

## Scenario 6: IoT / Time-Series Graph

**Workload:**
- 5M nodes (devices, events), 50M edges
- 100M writes/month (write-heavy)
- 10M queries/month
- Time-series queries (latest events, time-range scans)

### Cost Analysis (3-Year TCO)

| Provider | Setup | Tier | Monthly Cost | 3-Year Total |
|----------|-------|------|--------------|--------------|
| **JanusGraph (self-hosted)** | 5× JG + 10× Cassandra | Cassandra backend (write-optimized) | **$1,500** | **$54,000** ✅ |
| **Dgraph (self-hosted)** | 10× nodes (distributed) | Open source | **$840** | **$30,240** ⚠️ |
| **ArangoDB Cloud** | High-memory tier | Managed | **$800** | **$28,800** ⚠️ |
| **TigerGraph Enterprise** | Distributed cluster | Managed | **$3,000+** | **$108,000+** |
| **Neo4j Aura** | 64GB RAM | Managed (write throughput limited) | **$800** | **$28,800** ⚠️ |
| **Neptune Provisioned** | db.r6g.4xlarge | Managed | **$1,500** | **$54,000** |

**Winner:** JanusGraph self-hosted ($1,500/month, $54,000 over 3 years)

**Reasoning:**
- Cassandra backend optimized for high-throughput writes (10K-100K wps)
- Proven at IoT scale (Uber, Netflix historical use cases)
- Dgraph $840/month cheaper, but no graph algorithms (if needed for anomaly detection)
- Neo4j/Memgraph limited write throughput (100-500 wps)

**Key Insight:**
- Write-heavy workloads favor Cassandra-backed graphs (JanusGraph)
- Neo4j/Memgraph limited to 100-500 writes/second (insufficient for high-volume IoT)
- TigerGraph best performance but 2× cost of JanusGraph

---

## TCO Summary Table (3-Year Total Cost)

| Scenario | Scale | Winner | 3-Year TCO | Runners-Up |
|----------|-------|--------|------------|------------|
| **Hobby Project** | 1K nodes | Neo4j Aura Free | **$0** | Dgraph Free ($0), Memgraph self-hosted ($432) |
| **Startup MVP / Knowledge Graph** | 500 nodes | Memgraph Community | **$864** | Neo4j Community ($1,728), Dgraph ($864 but no algorithms) |
| **Growing SaaS** | 100K nodes | Memgraph Community | **$3,024** | Neo4j Community ($3,024), ArangoDB Cloud ($5,400) |
| **Enterprise Knowledge Graph** | 1M nodes | Memgraph Cloud Enterprise | **$28,764** | ArangoDB Cloud ($28,800), Neo4j Aura Enterprise ($36K+) |
| **Social Network / Massive Scale** | 10M+ nodes | JanusGraph | **$108,000** | Neo4j Aura ($43K+ but limited scale), TigerGraph ($180K+) |
| **IoT / Write-Heavy** | 5M nodes | JanusGraph | **$54,000** | Dgraph ($30K but no algorithms), TigerGraph ($108K+) |

---

## Cost Drivers Analysis

### Infrastructure Costs (Self-Hosted)

| Database | Small (500 nodes) | Medium (100K nodes) | Large (1M+ nodes) | Massive (10M+ nodes) |
|----------|-------------------|---------------------|-------------------|----------------------|
| **Memgraph** | $24/mo (4GB) | $84/mo (16GB) | $336/mo (64GB) | $1,500+/mo (128GB+) ⚠️ RAM-limited |
| **Neo4j** | $48/mo (8GB) | $84/mo (16GB) | $212/mo (32GB) | $424+/mo (64GB+) ⚠️ Single node limited |
| **JanusGraph** | $100/mo (multi-cluster overkill) | $168/mo (3-node Cassandra) | $840/mo (10-node) | $3,000/mo (30-node) ✅ Linear scaling |
| **Dgraph** | $24/mo (4GB) | $144/mo (3×8GB) | $840/mo (10-node) | $3,000+/mo |
| **ArangoDB** | $24/mo (4GB) | $144/mo (3×8GB) | $840/mo (10-node) | $3,000+/mo |

**Key Insight:**
- **Small scale (<1M nodes):** Memgraph/Neo4j/Dgraph cheapest ($24-84/month)
- **Large scale (1M-10M nodes):** Neo4j/Memgraph still viable ($212-424/month)
- **Massive scale (>10M nodes):** JanusGraph/TigerGraph only options (distributed required)
- **In-memory (Memgraph):** RAM-constrained, expensive at large scale

---

### Managed Service Premiums

| Provider | Premium over Self-Hosted | When Worth It |
|----------|-------------------------|---------------|
| **Memgraph Cloud** | 2-3× | HA/clustering needed, ops team <5 people |
| **Neo4j Aura** | 2-4× | Compliance (SOC 2, HIPAA), no ops team |
| **ArangoDB Cloud** | 1.5-2× | Multi-model needs, reasonable premium |
| **Neptune** | 3-5× | AWS-committed, need AWS integrations |
| **TigerGraph Cloud** | 2-3× | Real-time deep analytics, enterprise budget |

**Key Insight:**
- Managed services 2-5× more expensive than self-hosted
- Worth it if: No ops team, compliance required, AWS-committed
- Not worth it if: Budget <$100/month, ops team exists, small scale

---

## Break-Even Analysis: Self-Hosted vs Managed

**Assumptions:**
- Ops engineer: $120K/year salary = $10K/month
- Time spent on DB ops: 20% (monitoring, backups, updates)
- Effective ops cost: $2K/month

**Self-Hosted Costs:**
- Infrastructure: $X/month
- Ops time: $2K/month
- **Total: $X + $2,000**

**Managed Service Costs:**
- Service fee: $Y/month
- Ops time: $200/month (minimal monitoring)
- **Total: $Y + $200**

**Break-Even:**
$X + $2,000 = $Y + $200
$Y = $X + $1,800

**Conclusion:**
- Managed worth it if premium <$1,800/month
- Memgraph Cloud: $199/mo vs $84 self-hosted = $115 premium ✅ Worth it
- Neo4j Aura: $240/mo vs $84 self-hosted = $156 premium ✅ Worth it
- Neptune: $317/mo vs $84 self-hosted = $233 premium ✅ Borderline
- TigerGraph: $499/mo vs $84 self-hosted = $415 premium ⚠️ High but acceptable for enterprise

**Caveat:** Analysis assumes 1 database. For small teams managing 5+ databases, managed services even more attractive (ops cost amortized).

---

## Final Recommendations by Budget

**Budget <$50/month:**
- Use free tiers (Neo4j Aura, Dgraph Cloud, ArangoDB Cloud)
- Or self-host: Memgraph Community ($24/mo), Dgraph ($24/mo)

**Budget $50-100/month:**
- Self-host: Neo4j Community ($48-84/mo), Memgraph Community ($24-84/mo)
- Managed: ArangoDB Cloud ($20-80/mo)

**Budget $100-500/month:**
- Self-host: Neo4j, Memgraph, JanusGraph ($84-336/mo)
- Managed: Memgraph Cloud ($49-199/mo), Neo4j Aura ($65-240/mo)

**Budget $500-2,000/month:**
- Managed: Neo4j Aura Enterprise, Memgraph Cloud Enterprise ($800-1,000/mo)
- Self-host: JanusGraph cluster (if massive scale)

**Budget >$2,000/month:**
- TigerGraph Enterprise (best performance, deep analytics)
- JanusGraph (largest scale, lowest cost per node)
- Neptune (AWS-committed)

---

**Next:** Performance Benchmarks
