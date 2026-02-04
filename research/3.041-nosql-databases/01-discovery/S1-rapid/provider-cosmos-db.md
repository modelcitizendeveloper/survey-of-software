# Azure Cosmos DB

**Category:** Multi-Model Database (Managed)
**Provider:** Microsoft Azure
**Type:** Level 3 (Cloud Provider Managed)
**Data Model:** Document, Key-Value, Graph, Column-Family (all supported)

---

## Overview

Azure Cosmos DB is Microsoft's globally distributed, multi-model database service. Unique in supporting multiple NoSQL data models (document, key-value, graph, column-family) through different APIs, all backed by the same underlying storage engine.

---

## Pricing

### Free Tier
- **25 GB storage**
- **1,000 RU/s throughput** (Request Units per second)
- Available for 12 months OR lifetime free tier (one per subscription)
- **Limitation:** One free tier account per Azure subscription

### Serverless
- **Pay-per-operation:** No provisioned capacity
- **RU consumption:** $0.25 per million RUs
- **Storage:** $0.25/GB/month
- **Best for:** Unpredictable workloads, development
- **Limitation:** 5,000 RU/s max, 50GB max per container

### Provisioned Throughput
**Manual provisioning:**
- **100 RU/s minimum:** ~$5.76/month
- **Price per 100 RU/s:** $0.008/hour (~$5.76/month)
- **1,000 RU/s:** ~$57.60/month
- **Storage:** $0.25/GB/month

**Autoscale:**
- **400 RU/s minimum**
- Scales automatically between min and max
- ~1.5x cost of manual provisioning

### Global Distribution
- **Multi-region writes:** Extra RU/s cost per region
- **Example:** 2 regions = 2x RU/s cost

### Additional Costs
- **Backups:** Continuous (free), periodic backups beyond retention ($0.10-0.15/GB)
- **Analytical storage:** $0.02-0.03/GB/month (for Synapse Link)

---

## Request Units (RU) System

Cosmos DB uses Request Units (RU) to abstract CPU, memory, IOPS:
- **1 RU = 1KB document read** (point read)
- **5 RU = 1KB document write**
- **Query complexity affects RU consumption**

**Example:**
- 1M reads of 1KB documents = 1M RUs = $0.25
- 100K writes of 1KB documents = 500K RUs = $0.125

---

## Key Strengths

1. **Multi-Model:** Document (MongoDB API), Key-Value (Table API), Graph (Gremlin), Column (Cassandra API)
2. **Global Distribution:** Multi-region active-active with automatic failover
3. **Five Consistency Levels:** Strong, bounded staleness, session, consistent prefix, eventual
4. **SLA Guarantees:** 99.999% availability, <10ms latency (p99)
5. **API Compatibility:** MongoDB wire protocol, Cassandra CQL, Gremlin graph queries
6. **Azure Integration:** Native integration with Azure Functions, Logic Apps, Synapse
7. **Change Feed:** Real-time change data capture

---

## Key Weaknesses

1. **Complex Pricing:** RU model is hard to predict and optimize
2. **Expensive at Scale:** Can be 3-10x more expensive than alternatives
3. **Azure Lock-in:** Proprietary RU system, hard to migrate
4. **API Compatibility Gaps:** MongoDB/Cassandra APIs not 100% compatible
5. **Learning Curve:** Partition key design critical for performance
6. **Serverless Limits:** 5,000 RU/s max, 50GB max (too small for many apps)
7. **Minimum Costs:** Manual provisioning requires minimum spend

---

## Multi-Model APIs

Cosmos DB supports multiple APIs for the same data:

1. **SQL API (Core API):** Native JSON document API
2. **MongoDB API:** MongoDB wire protocol (version 3.6, 4.0, 4.2, 5.0)
3. **Cassandra API:** CQL queries (Cassandra-compatible)
4. **Gremlin API:** Graph traversals (Apache TinkerPop)
5. **Table API:** Azure Table Storage compatible (key-value)

**Note:** API choice is per-account (cannot mix APIs in same account)

---

## Use Cases

**Best For:**
- Global applications (multi-region active-active)
- Mission-critical apps (99.999% SLA)
- Azure-native applications (tight integration)
- Multi-model needs (document + graph in one platform)
- Migrating from MongoDB/Cassandra to Azure (API compatibility)
- Low-latency requirements (<10ms p99)

**Not Ideal For:**
- Cost-sensitive applications (expensive)
- Predictable workloads on other clouds (use DynamoDB on AWS)
- Simple use cases (overkill, use simpler database)
- Open source preference (vendor lock-in)

---

## Lock-in Assessment

**Underlying System:** Proprietary (Request Units, partitioning)
- **Migration Path:** Difficult despite API compatibility
- **API Compatibility:** MongoDB/Cassandra APIs help, but not 100%
- **Migration Cost:** High (RU optimization, partition key redesign)
- **Egress Costs:** Azure data transfer charges

**Mitigation:**
- Use MongoDB API for some portability (can export to Atlas)
- Use Cassandra API for some portability
- Regular backups to Azure Storage
- Abstract database layer in application code

**Export Options:**
- Azure Data Factory
- Change feed → Event Hubs → export
- Point-in-time restore to new account

---

## Ecosystem

- **Client SDKs:** .NET, Java, Python, Node.js, Go
- **API-Specific Drivers:** MongoDB drivers, Cassandra drivers, Gremlin drivers
- **Azure Integration:** Functions, Logic Apps, App Service, Synapse Analytics
- **Community:** Azure-focused
- **Documentation:** Excellent (Microsoft docs)

---

## Consistency Levels

Unique feature: Five tunable consistency levels

1. **Strong:** Linearizability (slowest, highest consistency)
2. **Bounded Staleness:** Reads lag by K versions or T time
3. **Session:** Read your writes (default, most popular)
4. **Consistent Prefix:** Never see out-of-order writes
5. **Eventual:** Fastest, lowest consistency

**Trade-off:** Consistency ↔ Latency ↔ Throughput

---

## Decision Factors

**Choose Cosmos DB if:**
- Global distribution is critical (multi-region active-active)
- You're on Azure (native integration)
- 99.999% SLA required
- Multi-model flexibility needed
- Migrating from MongoDB/Cassandra to Azure
- Strong consistency with low latency needed

**Choose alternative if:**
- Cost is primary concern (MongoDB Atlas, DynamoDB cheaper)
- AWS/GCP is your cloud (use DynamoDB/Firestore)
- Simple use case (PostgreSQL, MongoDB simpler)
- Open source required (self-hosted Cassandra/MongoDB)
- Predictable pricing needed (RU model complex)

---

## Competitive Position

- **vs DynamoDB:** More flexible (multi-model), better global distribution, but more expensive
- **vs MongoDB Atlas:** Native Azure, multi-model, but MongoDB has better query language
- **vs Cassandra:** Managed Cassandra API, but expensive vs self-hosted
- **vs Neptune:** Cosmos supports graph + document, Neptune is graph-only
- **vs Firestore:** Enterprise-focused vs developer-focused

---

## Partition Key Design

Critical for performance (similar to DynamoDB):

**Good partition key:**
- High cardinality (many unique values)
- Even distribution of requests
- Queries include partition key

**Bad partition key:**
- Low cardinality (few unique values)
- Hot partitions (one key gets all traffic)
- Cross-partition queries required

**Example:**
- Good: `userId` (unique per user)
- Bad: `country` (hot partitions for popular countries)

---

**Recommendation Category:** Best multi-model globally distributed database (Path 1)
**Open Source Alternative:** Cassandra (column), MongoDB (document), Neo4j (graph) separately (Path 3)
**Standard-Based Alternative:** Cassandra API (CQL standard-ish), MongoDB API (wire protocol)
