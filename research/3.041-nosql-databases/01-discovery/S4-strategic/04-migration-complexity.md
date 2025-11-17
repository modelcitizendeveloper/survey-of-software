# S4: Migration Complexity Matrix

**Research Date:** November 16, 2025
**Focus:** Estimating effort to switch between NoSQL providers
**Complexity Factors:** Data export/import, application code changes, downtime, testing

---

## Migration Complexity Levels

### Low Complexity: 1 Day - 1 Week

**Characteristics:**
- API-compatible databases (same query language)
- Standard export/import tools
- Minimal application code changes
- Low downtime (<1 hour with streaming replication)

---

#### PostgreSQL Migrations (SQL Standard)

**Supabase → AWS RDS PostgreSQL**
- **Method:** `pg_dump` → `pg_restore`
- **Downtime:** <1 hour (with streaming replication: <5 minutes)
- **Application changes:** Connection string only
- **Complexity:** Very low
- **Effort:** 1 day (mostly testing)

**Process:**
```bash
# 1. Dump from Supabase
pg_dump postgres://user:pass@supabase-host/db > dump.sql

# 2. Restore to RDS
psql postgres://user:pass@rds-host/db < dump.sql

# 3. Update application connection string
DATABASE_URL=postgres://rds-host/db

# 4. Test application
# 5. Switch DNS/traffic
```

**Supabase → Self-Hosted PostgreSQL**
- **Method:** Same as above
- **Downtime:** <1 hour
- **Effort:** 1-2 days (including server setup)

---

#### Cassandra Migrations (CQL Standard)

**DataStax Astra → ScyllaDB Cloud**
- **Method:** `sstableloader` or `CQL COPY`
- **Downtime:** <4 hours (with dual-write: near-zero)
- **Application changes:** Connection string + driver config
- **Complexity:** Low-Medium
- **Effort:** 3-5 days (including testing)

**Process:**
```bash
# Method 1: COPY command (slower, simpler)
cqlsh astra-host -e "COPY keyspace.table TO 'export.csv'"
cqlsh scylla-host -e "COPY keyspace.table FROM 'export.csv'"

# Method 2: sstableloader (faster, more complex)
nodetool snapshot keyspace
# Transfer SSTables to ScyllaDB cluster
sstableloader -d scylla-host sstable-directory

# Update application
cassandra:
  hosts: [scylla-host]
  keyspace: keyspace_name
```

**DataStax Astra → Self-Hosted Cassandra**
- **Method:** Same as above
- **Downtime:** <4 hours
- **Effort:** 1 week (including Cassandra cluster setup, tuning)

---

#### Redis Migrations (RESP Protocol)

**Redis Enterprise → Valkey (OSS Fork)**
- **Method:** RDB snapshot → restore
- **Downtime:** <1 hour (with replication: <10 minutes)
- **Application changes:** Connection string only
- **Complexity:** Low
- **Effort:** 1-2 days

**Process:**
```bash
# 1. Create snapshot on Redis Enterprise
redis-cli BGSAVE
redis-cli --rdb /backup/dump.rdb

# 2. Transfer to Valkey server
scp dump.rdb valkey-host:/var/lib/valkey/

# 3. Restart Valkey with snapshot
systemctl restart valkey

# 4. Update application
REDIS_URL=redis://valkey-host:6379
```

**Redis Enterprise → Self-Hosted Redis**
- **Method:** Same as above
- **Effort:** 1-2 days

---

### Medium Complexity: 1-4 Weeks

**Characteristics:**
- Partial API compatibility (80-90% compatible)
- Some features don't transfer
- Moderate application code changes
- Testing required for edge cases

---

#### MongoDB Migrations (Wire Protocol)

**MongoDB Atlas → Self-Hosted MongoDB**
- **Method:** `mongodump` → `mongorestore` or live migration
- **Downtime:** <1 hour (with live migration tool: near-zero)
- **Application changes:** Connection string, possibly auth method
- **Complexity:** Low-Medium
- **Effort:** 1-2 weeks (including testing, monitoring setup)

**Features that transfer:**
- ✅ Collections, documents, indexes
- ✅ Query language (MQL)
- ✅ Aggregation pipelines
- ✅ Change streams (if MongoDB 4.0+)

**Features that DON'T transfer:**
- ❌ Atlas Search (need to build Elasticsearch separately)
- ❌ Atlas Triggers (need to build with Change Streams + Lambda/Functions)
- ❌ Atlas Charts (need separate BI tool)
- ❌ Atlas Data Lake (need separate data warehouse)

**Process:**
```bash
# Method 1: mongodump (simpler, downtime required)
mongodump --uri="mongodb+srv://atlas-host" --out=/backup
mongorestore --uri="mongodb://self-hosted" /backup

# Method 2: Live migration (complex, zero downtime)
# Use Percona MongoDB Live Migrator or MongoDB Atlas Live Migration API
# Dual-write during transition, cutover when synced
```

**Effort breakdown:**
- Setup self-hosted cluster: 2-3 days
- Data migration: 1 day
- Test applications: 3-5 days
- Monitoring setup (Prometheus, Grafana): 2 days
- **Total: 1-2 weeks**

---

**MongoDB Atlas → AWS DocumentDB**
- **Method:** AWS Database Migration Service (DMS)
- **Downtime:** Near-zero (continuous replication)
- **Application changes:** Some queries may need rewriting
- **Complexity:** Medium
- **Effort:** 2-3 weeks

**DocumentDB compatibility:**
- ✅ CRUD operations (90% compatible)
- ✅ Indexes
- ✅ Aggregation pipeline (most stages)
- ⚠️ Change streams (not supported as of 2025)
- ⚠️ Transactions (limited support)
- ❌ Atlas-specific features (Search, Triggers, etc.)

**Caveat:** Test thoroughly - DocumentDB is ~80% compatible, edge cases exist

---

#### Neo4j Migrations

**Neo4j Aura → Self-Hosted Neo4j Enterprise**
- **Method:** `neo4j-admin dump` → `neo4j-admin load`
- **Downtime:** 2-8 hours (depends on graph size)
- **Application changes:** Connection string
- **Complexity:** Medium
- **Effort:** 1-2 weeks (including cluster setup, testing)

**Process:**
```bash
# 1. Dump from Neo4j Aura
neo4j-admin dump --database=neo4j --to=/backup/graph.dump

# 2. Transfer to self-hosted
scp graph.dump neo4j-host:/backup/

# 3. Load into self-hosted
neo4j-admin load --from=/backup/graph.dump --database=neo4j --force

# 4. Update application
NEO4J_URI=bolt://neo4j-host:7687
```

**Self-hosted setup complexity:**
- Single node: Easy (1 day)
- Cluster (causal clustering): Complex (3-5 days, Enterprise license required)

---

### High Complexity: 1-3 Months (Application Rewrite)

**Characteristics:**
- No API compatibility
- Proprietary features with no equivalent
- Significant application code changes
- Data model transformation required

---

#### Firestore Migrations (Proprietary Real-Time)

**Firestore → Supabase (PostgreSQL + Real-Time)**
- **Method:** Export JSON → transform → load PostgreSQL
- **Downtime:** Cutover period (hours)
- **Application changes:** Complete client SDK rewrite
- **Complexity:** Very High
- **Effort:** 2-3 months

**Why so complex:**
1. **Data model transformation:** NoSQL documents → relational tables
2. **Real-time sync rewrite:** Firestore listeners → Supabase subscriptions
3. **Security rules rewrite:** Firestore rules → PostgreSQL RLS (Row-Level Security)
4. **Client SDK changes:** Firebase SDK → Supabase SDK (iOS, Android, Web all different)
5. **Offline support:** Firestore native → Supabase requires custom implementation

**Process:**
```bash
# 1. Export Firestore data
gcloud firestore export gs://bucket/firestore-export

# 2. Transform JSON → SQL
# Custom script to convert documents to tables
python firestore_to_postgres.py

# 3. Load into Supabase
psql -f transformed.sql

# 4. Rewrite application (largest effort)
# - Replace Firestore SDK with Supabase SDK
# - Rewrite real-time listeners
# - Rewrite security rules
# - Test offline scenarios
```

**Effort breakdown:**
- Data export + transform: 1 week
- Client SDK rewrite (iOS): 3-4 weeks
- Client SDK rewrite (Android): 3-4 weeks
- Client SDK rewrite (Web): 2-3 weeks
- Server-side logic rewrite: 2 weeks
- Testing: 2-3 weeks
- **Total: 2-3 months** (can parallelize iOS/Android/Web)

---

**Firestore → MongoDB Atlas**
- **Method:** Export JSON → import MongoDB
- **Downtime:** Cutover period
- **Application changes:** Client SDK rewrite, lose real-time sync
- **Complexity:** High
- **Effort:** 1-2 months

**Easier than Firestore → Supabase because:**
- Document model stays same (NoSQL → NoSQL)
- But: Lose real-time sync (must build custom with Change Streams)

---

#### DynamoDB Migrations (Proprietary API)

**DynamoDB → Cassandra**
- **Method:** Export JSON → transform → load Cassandra
- **Downtime:** Cutover period
- **Application changes:** Complete application rewrite
- **Complexity:** Very High
- **Effort:** 2-3 months

**Why so complex:**
1. **API completely different:** DynamoDB API → CQL
2. **Data modeling different:** Single-table design → multi-table
3. **Access patterns change:** Partition key + sort key → CQL WHERE clauses
4. **No equivalent:** DynamoDB Streams → Cassandra CDC (different)

**Process:**
```bash
# 1. Export DynamoDB
aws dynamodb create-backup --table-name table
aws dynamodb export-table-to-point-in-time --table-arn arn --s3-bucket bucket

# 2. Transform data model
# Single DynamoDB table → Multiple Cassandra tables
# Overloaded keys → Proper columns
python dynamodb_to_cassandra.py

# 3. Load into Cassandra
cqlsh -f transformed.cql

# 4. Rewrite application (largest effort)
# - Replace AWS SDK with Cassandra driver
# - Redesign data model
# - Rewrite all queries
# - Test extensively
```

**Effort breakdown:**
- Data model redesign: 1-2 weeks
- Data export + transform: 1 week
- Application rewrite: 6-8 weeks
- Testing: 2-3 weeks
- **Total: 2-3 months**

---

**DynamoDB → MongoDB**
- **Method:** Export JSON → import MongoDB
- **Complexity:** High
- **Effort:** 2-3 months

**Similar complexity to DynamoDB → Cassandra:**
- Still requires API rewrite (DynamoDB → MongoDB)
- Data model still changes (key-value → document)

---

#### Cosmos DB Migrations (Proprietary Multi-Model)

**Cosmos DB → MongoDB Atlas**
- **Method:** Export via MongoDB API → import Atlas
- **Downtime:** Cutover period
- **Application changes:** Remove RU-specific code, some API differences
- **Complexity:** Medium-High
- **Effort:** 1-2 months

**If using Cosmos DB SQL API:**
- Higher complexity (SQL API → MongoDB)
- 2-3 months effort

**If using Cosmos DB Cassandra API:**
- Lower complexity (Cassandra API → real Cassandra)
- 1 month effort

**If using Cosmos DB Gremlin API (graph):**
- Migrate to Neo4j: 2-3 months (Gremlin → Cypher translation)

---

## Migration Complexity Summary Table

| Source → Destination | Complexity | Downtime | Application Changes | Effort | Risk |
|---------------------|------------|----------|-------------------|--------|------|
| **Supabase → RDS Postgres** | Very Low | <1 hr | Connection string | 1 day | Low |
| **Astra → ScyllaDB** | Low | <4 hrs | Connection string | 3-5 days | Low |
| **Redis Ent → Valkey** | Low | <1 hr | Connection string | 1-2 days | Low |
| **Atlas → Self-Hosted Mongo** | Medium | <1 hr | Minor (auth, monitoring) | 1-2 weeks | Low-Med |
| **Atlas → DocumentDB** | Medium | Near-zero | Some queries | 2-3 weeks | Medium |
| **Neo4j Aura → Self-Hosted** | Medium | 2-8 hrs | Connection string | 1-2 weeks | Medium |
| **Firestore → Supabase** | Very High | Hours | Complete rewrite | 2-3 months | High |
| **Firestore → MongoDB** | High | Hours | Major rewrite | 1-2 months | High |
| **DynamoDB → Cassandra** | Very High | Hours | Complete rewrite | 2-3 months | Very High |
| **DynamoDB → MongoDB** | Very High | Hours | Complete rewrite | 2-3 months | Very High |
| **Cosmos DB → MongoDB** | Medium-High | Hours | Moderate rewrite | 1-2 months | Medium-High |

---

## Migration Decision Framework

### Is Migration Worth It?

**Calculate migration ROI:**

**Migration cost:**
- Engineer time: [weeks] × $10,000/week = $X
- Downtime cost: [hours] × $Y/hour revenue = $Y
- Risk cost (bugs, data loss): $Z estimate
- **Total cost: $X + $Y + $Z**

**Ongoing savings:**
- Old database: $A/month
- New database: $B/month
- **Savings: ($A - $B) × 12 months = $S/year**

**Break-even:** Total cost ÷ Annual savings = [years]

**Example:**
- Migration cost: 6 weeks × $10K = $60,000
- Old database (Firestore): $500/month = $6,000/year
- New database (Supabase): $100/month = $1,200/year
- Annual savings: $4,800/year
- **Break-even: $60,000 ÷ $4,800 = 12.5 years** ❌ Not worth it

**When migration makes sense:**
- Break-even <2 years ✅
- Compliance requires it (no choice) ✅
- Current database hitting limits (technical reasons) ✅
- Vendor viability concerns (risk mitigation) ✅

**When to stay:**
- Break-even >3 years ❌
- High migration complexity (Firestore, DynamoDB) ❌
- Small team (can't afford 2-3 months) ❌
- Current database working fine ❌

---

## Migration Best Practices

### 1. Test Migration First

**Steps:**
1. Export production data to staging database (new provider)
2. Run application against staging for 1-2 weeks
3. Identify issues before production cutover
4. Fix bugs, optimize queries

**Time investment:** 20% of total migration effort
**Risk reduction:** 80% of bugs caught in testing

---

### 2. Dual-Write Strategy

For low-downtime migrations:

**Process:**
1. Setup new database alongside old
2. Application writes to BOTH databases
3. Read from old database (source of truth)
4. Monitor sync lag
5. When new database synced, switch reads to new
6. Run dual-write for 1 week (safety)
7. Decommission old database

**Downtime:** <5 minutes (DNS/config switch)
**Complexity:** Higher (dual-write code)
**Worth it for:** Mission-critical systems

---

### 3. Feature Flag Migration

Gradual rollout:

**Process:**
1. Implement feature flag (use LaunchDarkly, Split, or custom)
2. Route 1% traffic to new database
3. Monitor errors, performance
4. Increase to 10%, 25%, 50%, 100%
5. Rollback instantly if issues

**Risk reduction:** Can catch issues at low traffic volume
**Time:** Slower overall migration (weeks vs days)

---

### 4. Backup Everything

Before migration:

- ✅ Export old database (multiple formats)
- ✅ Store backups in S3/GCS (redundant storage)
- ✅ Test restore process (ensure backups are valid)
- ✅ Keep old database running for 30 days (rollback option)

**Don't:**
- ❌ Delete old database immediately
- ❌ Assume backups work without testing
- ❌ Skip redundant backups (one backup to S3 + one to GCS)

---

**Next:** Strategic Recommendations Synthesis
