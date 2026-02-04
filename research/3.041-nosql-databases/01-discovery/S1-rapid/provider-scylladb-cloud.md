# ScyllaDB Cloud

**Category:** Wide-Column Database (Managed)
**Provider:** ScyllaDB Inc.
**Type:** Level 4 (Managed Database Service)
**Data Model:** Wide-Column (Cassandra-compatible)

---

## Overview

ScyllaDB Cloud is the managed service for ScyllaDB, a Cassandra-compatible database rewritten in C++ for 10x performance. Drop-in replacement for Cassandra with the same CQL API, but dramatically faster and more efficient. Designed for ultra-low latency and high throughput.

---

## Pricing

### Free Trial
- **$300 credit** for 14 days
- No permanent free tier
- **Limitation:** Trial only

### Pay-As-You-Go
Pricing varies by cloud provider (AWS, GCP, Azure) and instance type:

**AWS Examples (us-east-1):**
- **i4i.large:** ~$0.50/hour (~$365/month) - 2 vCPUs, 16GB RAM, 468GB NVMe
- **i4i.xlarge:** ~$1.00/hour (~$730/month) - 4 vCPUs, 32GB RAM, 937GB NVMe
- **i4i.2xlarge:** ~$2.00/hour (~$1,460/month) - 8 vCPUs, 64GB RAM, 1,875GB NVMe

**Storage included:** NVMe SSD (local storage)
**Minimum:** 3-node cluster (high availability)

**Typical small cluster:**
- 3x i4i.large = ~$1,095/month (48GB RAM, 1.4TB storage)

---

## Key Strengths

1. **Performance:** 10x faster than Cassandra (C++ vs Java)
2. **Lower Latency:** Sub-millisecond p99 latency
3. **Cassandra Compatible:** Drop-in replacement (CQL, drivers)
4. **Lower Cost:** Fewer nodes needed for same throughput
5. **Efficient:** Better resource utilization (no JVM garbage collection)
6. **DynamoDB Compatible:** Alternator API (DynamoDB wire protocol)
7. **Modern Architecture:** Built from scratch for modern hardware

---

## Key Weaknesses

1. **No Free Tier:** Expensive minimum (3-node cluster)
2. **Smaller Ecosystem:** Newer than Cassandra, smaller community
3. **Same Complexity:** Cassandra data modeling challenges remain
4. **Limited Managed Options:** Only ScyllaDB Cloud (vs many Cassandra providers)
5. **Eventual Consistency:** Same trade-offs as Cassandra
6. **No Joins/Aggregations:** Same limitations as Cassandra

---

## Use Cases

**Same as Cassandra, but when:**
- Ultra-low latency critical (gaming, real-time bidding)
- High throughput required (millions of ops/sec)
- Cost optimization (fewer nodes = lower cost)
- Predictable performance (no JVM GC pauses)

**Best For:**
- Time-series data (IoT, metrics, logs)
- Real-time analytics
- High-frequency trading systems
- Gaming leaderboards
- Ad tech (real-time bidding)
- Messaging backends (Discord migrated from Cassandra to Scylla)

**Not Ideal For:**
- Same as Cassandra: complex queries, small datasets, transactions

---

## Lock-in Assessment

**API Compatibility:** CQL (Cassandra) + Alternator (DynamoDB)
- **Migration Path:** Can migrate to Cassandra or self-hosted Scylla
- **Compatibility:** 100% CQL compatible with Cassandra
- **Migration Cost:** Low (same drivers, same queries)
- **DynamoDB Migration:** Alternator API for DynamoDB workloads

**Export Options:**
- Same as Cassandra (CQL COPY, sstable export)
- Spark connector
- Scylla Migrator tool

**Portability:** Excellent (Cassandra-compatible)

---

## Ecosystem

- **Client Drivers:** Same as Cassandra (Python, Java, Node.js, Go, C++)
- **Tools:** cqlsh, Scylla Monitoring Stack (Grafana + Prometheus)
- **Community:** Growing (Discord, Slack)
- **Documentation:** Good
- **Hosting Options:** ScyllaDB Cloud, self-hosted

---

## ScyllaDB vs Cassandra

| Feature | ScyllaDB | Cassandra |
|---------|----------|-----------|
| Language | C++ | Java |
| Performance | 10x faster | Baseline |
| Latency | Sub-millisecond p99 | Single-digit ms |
| GC pauses | None | Yes (JVM) |
| Resource use | More efficient | Higher overhead |
| API | CQL + DynamoDB | CQL |
| Ecosystem | Smaller | Larger |
| Cost | Lower (fewer nodes) | Higher |

**Verdict:** ScyllaDB is faster, more efficient Cassandra

---

## Alternator API (DynamoDB Compatibility)

ScyllaDB includes DynamoDB-compatible API:
- Use DynamoDB SDKs with ScyllaDB backend
- Escape AWS lock-in (DynamoDB → Scylla migration)
- **Benefit:** Multi-cloud DynamoDB

**Use case:** Start with DynamoDB, migrate to ScyllaDB if needed

---

## Decision Factors

**Choose ScyllaDB Cloud if:**
- Need Cassandra performance but faster
- Ultra-low latency critical (p99 <1ms)
- High throughput (millions of ops/sec)
- Want to reduce infrastructure costs (fewer nodes)
- Migrating from Cassandra (drop-in replacement)
- Want DynamoDB API without AWS lock-in

**Choose Cassandra/Astra if:**
- Need free tier (Astra has 25GB free)
- Prefer larger ecosystem
- More managed options wanted (DataStax, Instaclustr)

**Choose alternative if:**
- Budget-constrained (no free tier)
- Complex queries needed (MongoDB)
- Small dataset (PostgreSQL)

---

## Competitive Position

- **vs Cassandra:** 10x faster, more efficient, smaller ecosystem
- **vs DynamoDB:** Multi-cloud, Cassandra API, but requires cluster management
- **vs MongoDB:** Better for time-series/events, worse for documents
- **vs Bigtable:** ScyllaDB is multi-cloud, Bigtable is GCP-only

---

## Performance Benchmarks

**ScyllaDB published benchmarks:**
- **1M ops/sec** per node (vs 100K for Cassandra)
- **p99 latency:** <1ms (vs 5-10ms for Cassandra)
- **Cost:** 1/10th infrastructure cost for same throughput

**Real-world:**
- Discord migrated from Cassandra to ScyllaDB: 70% cost reduction, 10x performance
- Comcast: 3x throughput with same hardware

---

## Managed Service Features (ScyllaDB Cloud)

- **Auto-scaling:** Vertical and horizontal
- **Multi-cloud:** AWS, GCP, Azure
- **Monitoring:** Built-in Grafana dashboards
- **Backups:** Automated snapshots
- **Security:** VPC, encryption at rest/transit, SSO
- **Support:** 24/7 for production plans

---

**Recommendation Category:** Best performance-optimized wide-column database (Path 1)
**Open Source Alternative:** ScyllaDB Open Source (self-hosted) (Path 3)
**Standard-Based Alternative:** CQL (Cassandra-compatible), Alternator (DynamoDB-compatible)
