# Redis Enterprise Cloud

**Category:** Key-Value Database / In-Memory Data Store
**Provider:** Redis Ltd.
**Type:** Level 4 (Managed Database Service)
**Data Model:** Key-Value (with data structures)

---

## Overview

Redis Enterprise Cloud is the fully managed Redis-as-a-Service from Redis Ltd. While Redis is often used as a cache (see 3.042), it can also be used as a primary database with persistence. Supports advanced data structures (strings, hashes, lists, sets, sorted sets, streams, JSON, search).

---

## Pricing

### Free Tier
- **30 MB memory** (very small)
- Single database
- No replication
- Community support
- **Limitations:** Too small for production, useful for testing only

### Fixed Plans
**Essentials (Basic tier):**
- **250 MB:** $7/month
- **500 MB:** $14/month
- **1 GB:** $26/month
- **2.5 GB:** $60/month
- **5 GB:** $120/month

**Essentials (Replication):**
- 2x cost of basic tier (high availability)
- Automatic failover

**Pro (Advanced):**
- **1 GB:** $55/month (with replication)
- **5 GB:** $240/month
- **10 GB:** $440/month
- Active-Active geo-replication available
- Redis modules: Search, JSON, Graph, TimeSeries, Bloom filters

### Flexible (Pay-As-You-Go)
- Custom sizing
- Multi-cloud, multi-region
- Contact sales for pricing

---

## Redis as Database vs Cache

**As Cache (3.042):**
- Temporary data, can be evicted
- No persistence required
- Session storage, API caching

**As Database (3.041):**
- Persistent data (RDB or AOF snapshots)
- Primary data store
- Cannot lose data
- Use cases: Leaderboards, queues, real-time analytics

---

## Key Strengths

1. **Speed:** Sub-millisecond latency (in-memory)
2. **Data Structures:** Not just key-value (lists, sets, sorted sets, streams)
3. **Persistence:** RDB snapshots + AOF (append-only file)
4. **Pub/Sub:** Real-time messaging built-in
5. **Transactions:** MULTI/EXEC for atomic operations
6. **Modules:** Search (full-text), JSON, Graph, TimeSeries, Bloom
7. **Active-Active:** Multi-region, conflict-free replication (CRDT)

---

## Key Weaknesses

1. **Expensive:** Memory is costly ($26/GB vs $0.25/GB for disk)
2. **Memory Limit:** Dataset must fit in RAM
3. **Query Limitations:** Simple key lookups (unless using RedisSearch module)
4. **Backup Complexity:** RDB snapshots can lose data between snapshots
5. **Persistence Overhead:** AOF can impact write performance
6. **Small Free Tier:** 30MB is tiny
7. **Not Ideal for Large Data:** Best for <100GB datasets

---

## Use Cases

**Best For (as Database):**
- Real-time leaderboards (sorted sets)
- Message queues (lists, streams)
- Real-time analytics (counters, HyperLogLog)
- Session storage (with persistence)
- Rate limiting (counters + expiration)
- Geospatial data (geo commands)
- Real-time recommendations (sets, sorted sets)
- Job queues (Sidekiq, BullMQ)

**Not Ideal For:**
- Large datasets (>100GB, too expensive)
- Complex queries (use MongoDB or SQL)
- Document storage (use MongoDB, unless using RedisJSON)
- Batch analytics (use data warehouse)
- Relational data (use PostgreSQL)

---

## Lock-in Assessment

**Protocol:** RESP (Redis Serialization Protocol) - de facto standard
- **Migration Path:** Can export to open source Redis, Valkey, Dragonfly
- **Compatibility:** Standard Redis clients work
- **Migration Cost:** Low to Medium (export/import, API compatible)
- **Egress Costs:** Varies by cloud

**Export Options:**
- RDB snapshot download
- BGSAVE command (background snapshot)
- Redis DUMP/RESTORE commands
- Migrate to Valkey (open source fork)

**Portability:** Good (open source core, standard protocol)

---

## Ecosystem

- **Client Libraries:** Python (redis-py), Node.js (ioredis), Java (Jedis), Go (go-redis)
- **ORMs:** Python (redis-om), Node.js (redis-om-node)
- **Community:** Massive (Redis is extremely popular)
- **Documentation:** Excellent
- **Hosting Options:** Redis Enterprise Cloud, Upstash, AWS ElastiCache, self-hosted

---

## Data Structures

Redis supports rich data types beyond simple key-value:

**Core types:**
- **Strings:** Simple key-value
- **Hashes:** Field-value pairs (like Python dict)
- **Lists:** Ordered collections (queues)
- **Sets:** Unique values
- **Sorted Sets:** Sets with scores (leaderboards)
- **Streams:** Append-only logs (Kafka-like)

**Advanced (modules):**
- **JSON:** RedisJSON (nested documents)
- **Search:** RediSearch (full-text search, secondary indexes)
- **Graph:** RedisGraph (graph database)
- **TimeSeries:** RedisTimeSeries (time-series data)
- **Bloom:** Probabilistic data structures

---

## Persistence Options

**RDB (Redis Database file):**
- Point-in-time snapshots
- Compact, faster startup
- Can lose data between snapshots

**AOF (Append-Only File):**
- Logs every write operation
- More durable (configurable fsync)
- Slower startup, larger files

**Hybrid:** RDB + AOF (recommended for database use case)

---

## Decision Factors

**Choose Redis Enterprise Cloud if:**
- Dataset fits in memory (<100GB)
- Sub-millisecond latency critical
- Using advanced data structures (sorted sets, streams)
- Real-time features needed (pub/sub, leaderboards)
- Redis expertise in team
- Need Redis modules (Search, JSON, Graph)

**Choose alternative if:**
- Large datasets (>100GB, use Cassandra or MongoDB)
- Cost-sensitive (Redis memory expensive)
- Complex queries needed (MongoDB, PostgreSQL)
- Disk-based durability required (PostgreSQL)
- Simple key-value only (DynamoDB cheaper at scale)

---

## Competitive Position

- **vs DynamoDB:** Faster, richer data structures, but expensive and memory-limited
- **vs MongoDB:** Better for real-time/in-memory, worse for large persistent documents
- **vs Cassandra:** Better for reads/real-time, worse for massive writes
- **vs PostgreSQL:** Faster for simple operations, worse for complex queries/relations
- **vs Memcached:** More features, persistence, but similar use case (caching)

---

## Redis Modules (Pro Tier)

**RediSearch:**
- Full-text search
- Secondary indexes
- Aggregations
- Makes Redis queryable like a document database

**RedisJSON:**
- Store JSON documents
- Query/update nested fields
- Alternative to MongoDB for small datasets

**RedisGraph:**
- Graph database (Cypher queries)
- Alternative to Neo4j for small graphs

**RedisTimeSeries:**
- Time-series data
- Downsampling, retention policies
- Alternative to InfluxDB for small datasets

---

## Redis vs Upstash

Comparison with Upstash (serverless Redis):

| Feature | Redis Enterprise | Upstash |
|---------|------------------|---------|
| Pricing | Fixed ($26/GB) | Per-request ($0.20/100K) |
| Free tier | 30MB | 10,000 requests/day |
| Latency | <1ms | <5ms (HTTP) |
| Protocol | RESP | RESP + HTTP |
| Serverless | No | Yes |
| Best for | Dedicated | Edge/serverless |

**See:** 3.042 Redis Hosting for full comparison

---

**Recommendation Category:** Best in-memory data store with persistence (Path 1)
**Open Source Alternative:** Redis (open source), Valkey (Linux Foundation fork) (Path 3)
**Standard-Based Alternative:** RESP protocol is de facto standard
