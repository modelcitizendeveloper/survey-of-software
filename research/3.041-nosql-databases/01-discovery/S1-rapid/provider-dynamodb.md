# AWS DynamoDB

**Category:** Key-Value / Wide-Column Database (Managed)
**Provider:** Amazon Web Services
**Type:** Level 3 (Cloud Provider Managed)
**Data Model:** Key-Value with optional secondary indexes

---

## Overview

DynamoDB is AWS's fully managed, serverless NoSQL database offering single-digit millisecond performance at any scale. Designed for high-throughput, low-latency applications with predictable performance.

---

## Pricing

### Free Tier (Permanent)
- **25 GB storage** (permanent free tier)
- **25 WCU + 25 RCU** provisioned capacity
- 2.5 million stream read requests/month
- 1GB data transfer out
- **Enough for:** Small apps, development, testing

### On-Demand Mode
- **Pay-per-request:** No capacity planning
- **Write:** $1.25 per million write requests
- **Read:** $0.25 per million read requests (eventually consistent), $0.50 (strongly consistent)
- **Storage:** $0.25/GB/month
- **Best for:** Unpredictable traffic, new apps, spiky workloads
- **Cost example:** 1M reads + 100K writes = $0.25 + $0.125 = $0.375

### Provisioned Mode
- **Write Capacity Unit (WCU):** $0.00065/hour (~$0.47/month per WCU)
- **Read Capacity Unit (RCU):** $0.00013/hour (~$0.09/month per RCU)
- Auto-scaling available
- **Best for:** Predictable traffic, cost optimization
- **Cost example:** 10 WCU + 10 RCU = $4.70 + $0.90 = $5.60/month + storage

### Additional Costs
- **Storage:** $0.25/GB/month
- **Backups:** On-demand ($0.10/GB), continuous (PITR) ($0.20/GB/month)
- **Global Tables:** Replicated write units (~2x write cost)
- **Data Transfer:** Standard AWS egress rates

---

## Key Strengths

1. **Serverless:** No servers to manage, auto-scaling
2. **Performance:** Single-digit millisecond latency (p99)
3. **Infinite Scale:** Handles 10+ trillion requests/day
4. **AWS Integration:** Native integration with Lambda, API Gateway, S3, Streams
5. **Global Tables:** Multi-region, active-active replication
6. **Cost at Small Scale:** Free tier + on-demand very cheap for low traffic
7. **DynamoDB Streams:** Change data capture for real-time processing

---

## Key Weaknesses

1. **Query Limitations:** Only query by partition key + sort key (no arbitrary queries)
2. **Learning Curve:** Single-table design patterns are complex
3. **AWS Lock-in:** Proprietary API, no standard, hard to migrate away
4. **Cost at High Scale:** Can become expensive with many indexes
5. **Item Size Limit:** 400KB per item (documents must be small)
6. **No Aggregations:** Must use DynamoDB Streams + Lambda for analytics
7. **Secondary Index Costs:** GSI/LSI increase storage and RCU/WCU costs

---

## Use Cases

**Best For:**
- Session storage (fast key-value lookups)
- User profiles (single-item access patterns)
- Shopping carts (low latency, high availability)
- Real-time leaderboards (sort by score)
- IoT device data (write-heavy, partition by device ID)
- Serverless applications (Lambda + API Gateway)
- Mobile backends (AWS Amplify integration)

**Not Ideal For:**
- Complex queries (use MongoDB or PostgreSQL)
- Analytics (use data warehouse)
- Relational data with joins (use PostgreSQL)
- Document storage with flexible schemas (use MongoDB)
- Full-text search (use Elasticsearch/Algolia)

---

## Lock-in Assessment

**API:** Proprietary AWS API
- **Migration Path:** Very difficult (no compatible alternatives)
- **Compatibility:** None (DynamoDB-only)
- **Migration Cost:** High (application rewrite required)
- **Egress Costs:** AWS data transfer charges apply

**Mitigation:**
- Use DynamoDB abstraction layer (e.g., OneTable, Dynamoose)
- Export to S3, transform, import to alternative
- Use DynamoDB Local for development (reduces vendor testing lock-in)

**Export Options:**
- On-demand backup to S3 (JSON or DynamoDB JSON format)
- DynamoDB Streams → Kinesis → S3
- AWS Data Pipeline

---

## Ecosystem

- **Client SDKs:** AWS SDK for 10+ languages (Python: boto3)
- **ORMs/Abstractions:** PynamoDB, OneTable, Dynamoose (Node.js)
- **Local Development:** DynamoDB Local (Docker)
- **Community:** Large (AWS-focused)
- **Documentation:** Excellent (AWS docs)

---

## Decision Factors

**Choose DynamoDB if:**
- You're already on AWS (tight integration)
- Single-digit millisecond latency is critical
- Access patterns are key-based (get/put by ID)
- Serverless architecture (Lambda)
- Infinite scalability needed
- Low traffic (free tier is generous)

**Choose alternative if:**
- Multi-cloud portability required (MongoDB Atlas)
- Complex queries needed (MongoDB, PostgreSQL)
- Vendor lock-in is unacceptable (self-hosted Cassandra)
- Full-text search required (MongoDB Atlas Search)
- You need SQL (PostgreSQL, MySQL)

---

## Competitive Position

- **vs MongoDB:** Simpler data model, faster for key lookups, but very limited queries
- **vs Cassandra:** Fully managed, easier, but AWS-only and proprietary
- **vs Redis:** Persistent, scalable, but slower than Redis for cache use cases
- **vs PostgreSQL:** Better for simple key-value at scale, worse for relational data
- **vs Firestore:** Similar serverless model, but AWS vs GCP ecosystem

---

## Access Patterns

DynamoDB requires careful access pattern design:

**Supported:**
- Get item by partition key: `GetItem(PK)`
- Query items by partition key + range: `Query(PK, SK begins_with "...")`
- Scan entire table (expensive, avoid)

**Not Supported:**
- Query by non-key attribute (must create GSI)
- Joins (denormalize or use multiple queries)
- Full-text search (need external index)
- Aggregations (use Streams + Lambda)

**Single-Table Design:** Best practice is one table with overloaded keys and GSIs

---

**Recommendation Category:** Best serverless key-value database for AWS (Path 1)
**Open Source Alternative:** Cassandra, ScyllaDB (different API though) (Path 3)
**Standard-Based Alternative:** None (proprietary AWS service)
