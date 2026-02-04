# S3 Scenario 3: IoT Time-Series Analytics

**Use Case:** IoT sensor network (smart building, fleet tracking, industrial monitoring)
**Scale:** 1,000 devices → 10,000 devices in Year 1, 1 reading/sec/device
**Data Volume:** 2.6 billion data points/month (10K devices × 1/sec × 60 × 60 × 24 × 30)

---

## Requirements

### Functional
- Ingest sensor readings (temperature, pressure, location, status)
- Time-range queries (last hour, last day, last month)
- Aggregations (min, max, avg, percentiles)
- Device metadata storage (device ID, location, config)
- Alert rules (threshold exceeded)
- Data retention (raw data: 30 days, aggregated: 1 year)

### Non-Functional
- **Write throughput:** 10,000 writes/sec sustained (peak: 50,000 writes/sec)
- **Read latency:** <100ms for recent data
- **Scalability:** Linear scale (10K → 100K devices without rewrite)
- **Availability:** 99.9% (some downtime acceptable for analytics)
- **Cost:** <$500/month Year 1, optimize for write cost
- **Data retention:** Automatic downsampling/archival

---

## Data Model Analysis

**Primary data types:**
1. **Sensor readings:** Time-series (device_id, timestamp, metrics)
2. **Device metadata:** Document (device_id, location, config, last_seen)
3. **Aggregations:** Pre-computed rollups (hourly, daily averages)

**Access patterns:**
- **Write-heavy:** 10K writes/sec (86 million writes/day, 2.6B/month)
- **Read-light:** Occasional queries (dashboards, alerts)
- Query by device_id + time range
- Aggregations over time windows
- Recent data most frequently accessed

**Data model fit:**
- ✅ **Wide-column (time-series optimized):** Perfect (Cassandra, ScyllaDB)
- ✅ **Specialized time-series DB:** Excellent (InfluxDB, TimescaleDB)
- ⚠️ **Key-value:** Workable but expensive (DynamoDB)
- ❌ **Document database:** Expensive for high-volume writes (MongoDB)

---

## Database Recommendation

### Primary Recommendation: **Cassandra (DataStax Astra DB) Serverless**

**Why Cassandra:**
1. ✅ **Write-optimized** (LSM tree architecture, 50K+ writes/sec)
2. ✅ **Time-series partitioning** (partition by device + time bucket)
3. ✅ **Linear scalability** (add nodes = proportional throughput)
4. ✅ **Cost-effective** ($0.25/1M writes, cheapest for write-heavy)
5. ✅ **Serverless option** (Astra DB, no cluster management)
6. ✅ **Free tier** (25GB + 25M operations, good for testing)
7. ✅ **TTL support** (automatic data expiration)

**Architecture:**
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Device    │     │   Device    │ ... │   Device    │
│   Sensor    │     │   Sensor    │     │   Sensor    │
│ (10K total) │     │   (MQTT)    │     │    (HTTP)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                    │
       └───────────────────┼────────────────────┘
                           ↓
                  ┌────────────────┐
                  │  MQTT Broker   │
                  │  (AWS IoT Core)│
                  └────────┬───────┘
                           │
                           ↓
                  ┌────────────────┐
                  │     Lambda     │
                  │ (batch writer) │
                  └────────┬───────┘
                           │
                           ↓
                  ┌────────────────┐
                  │   Cassandra    │
                  │  Astra DB      │
                  │  (Serverless)  │
                  └────────────────┘
```

**Data model:**
```cql
CREATE TABLE sensor_readings (
  device_id text,
  bucket text,          -- e.g., "2025-11-16-14" (hourly buckets)
  timestamp timestamp,
  temperature float,
  pressure float,
  location text,
  PRIMARY KEY ((device_id, bucket), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
  AND default_time_to_live = 2592000;  -- 30 days TTL
```

**Queries:**
```cql
-- Get last hour of data for device
SELECT * FROM sensor_readings
WHERE device_id = 'device_001'
  AND bucket = '2025-11-16-14'
  AND timestamp > '2025-11-16 14:00:00'
ORDER BY timestamp DESC;

-- Efficient: Queries single partition (fast)
```

**3-Year TCO:**
- **Year 1:** (10K devices, 2.6B writes/month, 10M reads/month, 500GB storage)
  - Writes: 2,600M × $0.25/1M = $650/month
  - Reads: 10M × $0.10/1M = $1/month
  - Storage: 500GB × $0.25 = $125/month
  - **Total: $776/month** = $9,312/year
- **Year 2:** (same load)
  - $9,312
- **Year 3:** (scale to 20K devices, 5.2B writes/month, 1TB storage)
  - Writes: $1,300/month
  - Reads: $1/month
  - Storage: $250/month
  - **Total: $1,551/month** = $18,612/year
- **3-Year TCO: ~$37,236**

---

### Alternative: **InfluxDB Cloud (Specialized Time-Series)**

**Why InfluxDB:**
1. ✅ **Purpose-built for time-series** (best data model)
2. ✅ **Better compression** (10× better than Cassandra)
3. ✅ **Built-in downsampling** (automatic rollups)
4. ✅ **Flux query language** (powerful time-series queries)
5. ✅ **Cheaper storage** ($0.25/GB compressed vs $0.25/GB raw in Cassandra)

**Trade-offs:**
1. ⚠️ **Specialized** (not general-purpose NoSQL)
2. ⚠️ **Smaller ecosystem** vs Cassandra
3. ⚠️ **Lock-in** (InfluxDB-specific queries)

**3-Year TCO:**
- **Year 1:** (2.6B writes, 50GB compressed storage)
  - Writes: 2,600M × $0.20/1M = $520/month
  - Storage (compressed 10:1): 50GB × $0.25 = $12.50/month
  - **Total: $532.50/month** = $6,390/year (31% cheaper than Cassandra)
- **Year 2:** $6,390
- **Year 3:** (5.2B writes, 100GB compressed)
  - Writes: $1,040/month
  - Storage: $25/month
  - **Total: $1,065/month** = $12,780/year
- **3-Year TCO: ~$25,560** (31% cheaper than Cassandra)

**Verdict:** InfluxDB is 31% cheaper and better for pure time-series

---

### Alternative: **DynamoDB**

**Why DynamoDB:**
1. ✅ **Serverless** (true pay-as-you-go)
2. ✅ **AWS integration** (IoT Core → DynamoDB direct)
3. ✅ **Simple setup** (no cluster management)

**Trade-offs:**
1. ❌ **Expensive for high writes** ($1.25/1M writes vs $0.20-0.25)
2. ⚠️ **No time-series optimizations** (no automatic TTL on free tier)
3. ⚠️ **No aggregations** (need Athena or Timestream)

**3-Year TCO:**
- **Year 1:** (2.6B writes/month, 10M reads, 500GB)
  - Writes: 2,600M × $1.25/1M = $3,250/month
  - Reads: 10M × $0.25/1M = $2.50/month
  - Storage: 500GB × $0.25 = $125/month
  - **Total: $3,377.50/month** = $40,530/year (4.3× more expensive)
- **3-Year TCO: ~$80,000+**

**Verdict:** DynamoDB is 4× more expensive than Cassandra for write-heavy IoT

---

### Alternative: **TimescaleDB (PostgreSQL Extension)**

**Why TimescaleDB:**
1. ✅ **PostgreSQL-based** (SQL queries, standard tools)
2. ✅ **Time-series optimizations** (hypertables, compression)
3. ✅ **Open source** (can self-host)
4. ✅ **Low lock-in** (PostgreSQL portability)

**Managed options:**
- Timescale Cloud
- Self-hosted on AWS/GCP
- Supabase (doesn't include TimescaleDB)

**3-Year TCO (Timescale Cloud):**
- **Year 1:** ~$500-800/month = $7,200/year
- **Year 3:** ~$1,500/month = $18,000/year
- **3-Year TCO: ~$30,000**

**Verdict:** Competitive with InfluxDB, best if SQL queries preferred

---

## Decision Matrix

| Factor | Cassandra Astra | InfluxDB Cloud | DynamoDB | TimescaleDB |
|--------|-----------------|----------------|----------|-------------|
| **Year 1 cost** | $9,312 | $6,390 | $40,530 | $7,200 |
| **3-Year TCO** | $37,236 | $25,560 | $80,000+ | $30,000 |
| **Write performance** | 50K+/sec | 100K/sec | Unlimited | 10K/sec |
| **Compression** | 1:1 | 10:1 ✅ | 1:1 | 5:1 |
| **Query language** | CQL | Flux | API | SQL |
| **Downsampling** | Manual | ✅ Built-in | Manual | ✅ Built-in |
| **Lock-in** | Medium (CQL) | High (Flux) | High (AWS) | Low (SQL) |
| **Ecosystem** | Large | Small | Large | Large |
| **General-purpose** | ✅ Yes | ❌ Time-series only | ✅ Yes | ✅ Yes |

---

## Recommended Architecture

### Winner: **InfluxDB Cloud** (Best for Pure Time-Series)

**Full stack:**
```
Devices (MQTT) → AWS IoT Core → Lambda → InfluxDB Cloud
                                              ↓
                                        Grafana Dashboards
                                        Alert Rules
```

**Reasons:**
1. ✅ **31% cheaper** than Cassandra ($25,560 vs $37,236)
2. ✅ **10× better compression** (500GB → 50GB)
3. ✅ **Built-in downsampling** (automatic rollups)
4. ✅ **Purpose-built for time-series**
5. ⚠️ **Lock-in** (InfluxDB-specific, but worth it for IoT)

**When to choose Cassandra instead:**
- Need general-purpose NoSQL (not just time-series)
- Want CQL portability (can migrate to ScyllaDB)
- Plan to self-host eventually (Cassandra open source)
- Need ultra-high write throughput (>100K writes/sec)

**When to choose TimescaleDB instead:**
- Prefer SQL queries
- Want PostgreSQL portability (lowest lock-in)
- Need relational features (JOINs with device metadata)

**When to avoid DynamoDB:**
- Write-heavy workloads (4× more expensive)

---

## Cost Optimization Strategies

### 1. Batch Writes
- Batch 100 readings before write
- Reduce write operations by 50-90%
- InfluxDB: 2.6B → 260M writes = $52/month (90% savings)

### 2. Data Downsampling
- Raw data: 30 days (high resolution)
- Hourly aggregates: 1 year
- Daily aggregates: Forever
- **Storage savings: 70-90%**

### 3. Compression
- Use InfluxDB or TimescaleDB (10× compression)
- 500GB → 50GB = $125/month → $12.50/month

### 4. Cold Storage Archival
- Move old data to S3 ($0.023/GB vs $0.25/GB)
- 90% cost savings for historical data

**Example optimization:**
- Naive Cassandra: $776/month
- Batched writes (100×): $78/month
- InfluxDB compressed: $532/month → $53/month (batched)
- **Total savings: $723/month (93%)**

---

## Scalability Path

### Start: InfluxDB Cloud (1K-10K devices)
- **Cost:** $50-532/month
- **Effort:** Low (managed service)

### Grow: InfluxDB Cloud (10K-100K devices)
- **Cost:** $500-5,000/month
- **Effort:** Low (auto-scales)

### Massive Scale: Self-Hosted Cassandra (100K+ devices)
- **Cost:** $2,000/month infrastructure + $3,000/month ops
- **Break-even:** ~$5,000/month InfluxDB spend
- **Benefit:** More control, custom optimizations

---

## Final Recommendation

**For IoT Time-Series: InfluxDB Cloud**
- 31% cheaper than Cassandra
- 10× compression
- Built-in downsampling
- Purpose-built for time-series
- **3-Year TCO: $25,560** (optimized: ~$10,000 with batching)

**For General-Purpose + Time-Series: Cassandra Astra**
- Not just time-series (multi-use database)
- CQL portability
- Self-host option
- **3-Year TCO: $37,236**

**For SQL + Time-Series: TimescaleDB**
- PostgreSQL portability (lowest lock-in)
- SQL queries
- **3-Year TCO: $30,000**

**Avoid: DynamoDB**
- 4× more expensive for write-heavy IoT
- **3-Year TCO: $80,000+**

---

**Verdict:** InfluxDB Cloud wins for IoT - purpose-built for time-series, best compression, automatic downsampling make it the most cost-effective choice.
