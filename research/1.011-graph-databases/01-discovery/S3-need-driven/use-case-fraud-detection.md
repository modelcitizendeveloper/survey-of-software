# Use Case: Fraud Detection

## Domain Description

Fraud detection leverages graph analysis to identify suspicious patterns in
transactions, accounts, and entity relationships. Graphs excel at revealing
hidden connections between seemingly unrelated entities, detecting ring
structures, and identifying anomalous behavior patterns that traditional
tabular analysis misses.

## Requirements Analysis

### Graph Model Requirements

| Aspect | Requirement | Rationale |
|--------|-------------|-----------|
| **Model Type** | Property Graph | Need rich properties on both nodes and edges |
| **Schema** | Flexible | Fraud patterns evolve; schema must adapt quickly |
| **Temporality** | Time-aware | Transaction timestamps critical for pattern detection |

**Key Entity Types:**
- Accounts (bank, merchant, user)
- Transactions (payments, transfers, purchases)
- Devices (phones, IP addresses, browsers)
- Identities (SSN, email, phone numbers)
- Locations (addresses, GPS coordinates)

### Query Pattern Complexity

**Primary Patterns:**
- **Ring detection**: Circular money flows (A -> B -> C -> A)
- **Shared identity**: Multiple accounts sharing device/IP/email
- **Velocity analysis**: Transaction frequency and amount patterns
- **Network expansion**: Exploring N-hop neighborhood of suspicious entity
- **Similarity matching**: Finding accounts with similar behavior patterns

**Query Characteristics:**
- Depth: 3-6 hops for pattern detection
- Time windows: Queries scoped to time ranges (last 24h, 7d, 30d)
- Aggregation: Sum, count, standard deviation of transactions
- Pattern matching: Complex subgraph patterns with constraints

### Scale Requirements

| Metric | Typical Range | High Scale |
|--------|---------------|------------|
| Accounts (nodes) | 10M - 100M | 1B+ |
| Transactions (edges) | 100M - 10B | 100B+ |
| Real-time queries | 100 - 1K QPS | 10K+ QPS |
| Pattern scans | 1M - 100M/hour | 1B+/hour |

### Processing Mode

- **Real-time**: Transaction scoring at payment time (< 100ms)
- **Near-real-time**: Alert generation (< 5 min lag)
- **Batch**: Pattern discovery, model training (hourly/daily)

### Integration Requirements

- Transaction streaming (Kafka, Kinesis) for real-time ingestion
- ML pipeline for fraud scoring models
- Case management systems for investigation workflows
- Regulatory reporting and audit trails
- Alert delivery (email, SMS, dashboards)

## Library Evaluation

### neo4j (Official Driver)

**Strengths:**
- Excellent pattern matching with Cypher
- GDS library has community detection, PageRank for risk scoring
- Good transaction support for consistent writes
- Bloom visualization for investigators

**Limitations:**
- Real-time scoring at 10K+ TPS challenging
- Temporal queries require careful indexing
- Graph algorithms not available in Community edition

**Fit Score: 8/10**

### pyTigerGraph

**Strengths:**
- Built for high-throughput transaction processing
- GSQL optimized for deep link analysis
- Native support for temporal patterns
- Designed for financial services scale

**Limitations:**
- Enterprise licensing costs
- Steeper learning curve for GSQL
- Smaller Python community

**Fit Score: 9/10** (high scale); **7/10** (smaller deployments)

### python-arango

**Strengths:**
- Good throughput for transaction ingestion
- Multi-model allows storing raw transaction documents
- Flexible schema for evolving fraud patterns
- Cost-effective scaling

**Limitations:**
- Graph algorithms less mature than Neo4j GDS
- Pattern matching syntax less expressive
- Smaller fraud detection community

**Fit Score: 7/10**

### gremlinpython (with Neptune)

**Strengths:**
- Managed service reduces operational burden
- Good for AWS-native architectures
- Scales horizontally

**Limitations:**
- Query latency can be variable
- Limited graph algorithm support
- Gremlin verbose for complex patterns

**Fit Score: 6/10**

### NetworkX (with external storage)

**Strengths:**
- Rich algorithm library for analysis
- Good for offline pattern discovery
- Easy prototyping of detection logic

**Limitations:**
- In-memory only (not for production scale)
- No persistence or transactions
- Cannot handle real-time requirements

**Fit Score: 4/10** (analysis only)

## Gaps and Workarounds

| Gap | Impact | Workaround |
|-----|--------|------------|
| Real-time graph algorithms | Cannot run PageRank per transaction | Pre-compute risk scores, incremental updates |
| Temporal pattern matching | Limited native time-series support | Time-bucketed subgraphs, temporal indices |
| Streaming ingestion | Not all drivers handle high-volume streams | Kafka Connect, custom streaming layer |
| Explainability | Graph patterns hard to explain to regulators | Path export, visualization, rule extraction |
| Model integration | Limited native ML support | Feature extraction to external ML pipeline |

## Architecture Pattern

```
[Transaction Stream]
        |
        v
[Stream Processor] -- real-time features --> [ML Scoring Service]
        |
        v
[Graph Database] <-- enrichment queries
        |
        v
[Batch Analytics] -- pattern discovery --> [Rule Engine Update]
```

**Hybrid Approach:**
1. Real-time: Feature extraction + ML scoring (sub-100ms)
2. Near-real-time: Graph enrichment queries (100ms-1s)
3. Batch: Deep pattern analysis, model retraining

## Recommendation

**Best Fit: pyTigerGraph** for enterprise fraud detection

At the scale typical for financial fraud detection (billions of transactions),
TigerGraph's distributed architecture and GSQL's pattern matching capabilities
make it the strongest choice. The financial services focus means battle-tested
at relevant scale.

**Alternative: neo4j official driver** for smaller deployments or teams
with existing Cypher expertise. The GDS library provides excellent
algorithm support for pattern discovery.

**Hybrid pattern**: Use Neo4j/TigerGraph for graph storage and queries,
with NetworkX for offline algorithm development and prototyping.
