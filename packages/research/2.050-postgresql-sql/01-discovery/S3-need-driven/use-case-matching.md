# S3: Use Case → Provider Matching

**Date**: 2025-10-16
**Methodology**: S3 - Need-Driven Analysis
**Purpose**: Map specific use cases and requirements to optimal PostgreSQL providers

---

## Use Case Taxonomy

### By Application Type
1. **Web Applications** (CRUD, user management)
2. **SaaS Platforms** (multi-tenant, scaling)
3. **Mobile Backends** (API-driven, real-time)
4. **AI/ML Applications** (vector embeddings, RAG)
5. **Analytics/BI** (reporting, aggregations)
6. **IoT/Time-Series** (sensor data, metrics)
7. **Geospatial** (maps, location services)
8. **E-commerce** (transactions, inventory)

### By Scale
9. **Prototype/MVP** (<1GB, low traffic)
10. **Startup/Growth** (1-100GB, moderate traffic)
11. **Production/Scale** (100GB-1TB, high traffic)
12. **Enterprise** (>1TB, mission-critical)

### By Requirements
13. **Cost-Sensitive** (minimize costs)
14. **High Availability** (99.99%+ uptime)
15. **Compliance-Driven** (SOC2, HIPAA, FedRAMP)
16. **Portability-Focused** (vendor independence)

---

## 1. Web Application (Standard CRUD)

### Characteristics
- **Access Pattern**: Balanced reads/writes (user CRUD operations)
- **Scale**: Small to medium (1-100GB)
- **Features**: Standard SQL (tables, indexes, foreign keys)
- **Performance**: Medium latency acceptable (<100ms)

### Database Requirements
- Core SQL support (no extensions needed)
- Backups and point-in-time recovery
- Connection pooling
- Basic monitoring

### Provider Recommendations

**Best for Cost** (small projects <10GB):
1. **Supabase Free/Pro** ($0-25/mo)
   - 500MB free tier, $25/mo Pro (8GB included)
   - Includes Auth, Storage, Realtime (bonus features)
   - Auto-backups, connection pooling
   - **Migration**: Easy (standard PostgreSQL, no lock-in if not using Supabase features)

2. **Neon Free/Launch** ($0-19/mo)
   - 3GB free tier, $19/mo Launch
   - Serverless (scale-to-zero saves costs)
   - Database branching (great for dev/staging)
   - **Migration**: Easy (standard PostgreSQL)

3. **Railway** (~$12-17/mo)
   - $5 base + usage (~$7-12 for small DB)
   - Pay only for what you use
   - **Migration**: Easy (standard PostgreSQL)

**Best for Simplicity** (medium projects 10-100GB):
1. **DigitalOcean Managed PostgreSQL** ($15-60/mo)
   - Simple pricing, predictable costs
   - 1-2 vCPU, 1-4GB RAM options
   - Droplets integration (if using DO)
   - **Migration**: Easy (standard PostgreSQL)

2. **Render** ($52-85/mo)
   - Includes compute + database
   - Auto-sleep on free tier (dev environments)
   - **Migration**: Easy (standard PostgreSQL)

**Avoid**:
- AWS/Azure/GCP (overkill for simple web apps, 3-5× more expensive)
- Timescale (unnecessary for non-time-series)

**Migration Path**: Any → Any (core SQL, 1-4 hours)

---

## 2. SaaS Platform (Multi-Tenant)

### Characteristics
- **Access Pattern**: Read-heavy (10:1 read/write ratio)
- **Scale**: Medium to large (100GB-1TB)
- **Features**: Row-level security, connection pooling, read replicas
- **Performance**: Low latency critical (<50ms)

### Database Requirements
- Row-level security (RLS) for tenant isolation
- Connection pooling (PgBouncer)
- Read replicas (scale reads)
- Advanced monitoring (query performance)

### Provider Recommendations

**Best for Built-in Multi-Tenancy**:
1. **Supabase Pro/Team** ($25-599/mo)
   - Built-in RLS (row-level security)
   - Connection pooling (PgBouncer included)
   - Real-time subscriptions (if needed)
   - **Trade-off**: Supabase features create lock-in (20-40% portability if heavily used)

**Best for Performance**:
1. **AWS RDS PostgreSQL** ($100-600/mo for 100GB-1TB)
   - Read replicas (scale reads horizontally)
   - Performance Insights (query monitoring)
   - Global reach (multi-region)
   - **Trade-off**: More expensive, but proven at scale

2. **Azure Database for PostgreSQL - Hyperscale** ($120-700/mo)
   - Distributed query engine (Citus extension)
   - Horizontal scaling (sharding)
   - **Trade-off**: Citus creates lock-in (not portable to other providers)

**Best for Cost + Scale**:
1. **Neon Scale** ($69-700/mo)
   - Serverless (autoscaling, scale-to-zero)
   - Database branching (dev/staging environments)
   - Read replicas
   - **Trade-off**: Newer provider, less battle-tested than AWS

**Migration Path**:
- Core SQL only: 4-8 hours (any → any)
- Using RLS: 8-16 hours (Supabase → AWS RDS requires RLS policy migration)
- Using Citus: 40-160 hours (Azure Hyperscale lock-in)

---

## 3. Mobile Backend (Real-Time)

### Characteristics
- **Access Pattern**: Mixed (real-time updates, push notifications)
- **Scale**: Small to medium (1-50GB)
- **Features**: Real-time subscriptions, authentication, file storage
- **Performance**: Low latency (<50ms), real-time updates

### Database Requirements
- Real-time data sync (websockets, subscriptions)
- Built-in authentication (OAuth, JWT)
- File storage integration
- Push notifications

### Provider Recommendations

**Best All-in-One** (BaaS + PostgreSQL):
1. **Supabase** ($25-599/mo)
   - ✅ PostgreSQL + Auth + Storage + Realtime + Edge Functions
   - ✅ Real-time subscriptions (database changes → websockets)
   - ✅ Row-level security (user data isolation)
   - ✅ Client SDKs (JavaScript, Flutter, Swift, Kotlin)
   - **Trade-off**: Heavy Supabase usage creates lock-in (20-40% portability)
   - **Migration to standard PostgreSQL**: 40-80 hours (replace Auth, Realtime, Storage)

**Best for Custom Backend**:
1. **Neon** ($19-700/mo) + separate real-time service (Pusher, Ably)
   - PostgreSQL database (portable)
   - Add real-time service (Pusher: $29-99/mo, Ably: $29-399/mo)
   - Add auth service (Auth0: $240/year, Clerk: $25-599/mo)
   - **Total**: ~$100-1,000/mo
   - **Trade-off**: More complex setup, but fully portable

2. **AWS RDS** ($100-600/mo) + AWS ecosystem (AppSync, Cognito, S3)
   - RDS PostgreSQL (database)
   - AWS AppSync (GraphQL + real-time)
   - AWS Cognito (authentication)
   - AWS S3 (file storage)
   - **Trade-off**: AWS lock-in, but proven at scale

**Decision Framework**:
- **Startup/MVP**: Supabase (fastest time-to-market, all-in-one)
- **Custom backend**: Neon + Pusher/Ably (portability, pay for what you need)
- **AWS-committed**: AWS RDS + AWS ecosystem (scale, enterprise features)

**Migration Path**:
- Supabase → Standard PostgreSQL: 40-80 hours (replace BaaS features)
- Neon → AWS RDS: 4-8 hours (standard PostgreSQL)

---

## 4. AI/ML Application (Vector Embeddings / RAG)

### Characteristics
- **Access Pattern**: Vector similarity search (k-NN, cosine similarity)
- **Scale**: Medium to large (10GB-1TB, millions of vectors)
- **Features**: pgvector extension, HNSW/IVFFlat indexes
- **Performance**: Low latency (<100ms for similarity search)

### Database Requirements
- pgvector extension support
- HNSW or IVFFlat index support
- Sufficient compute for index builds
- Monitoring for vector query performance

### Provider Recommendations

**Best for pgvector Support**:
1. **AWS RDS PostgreSQL** ($100-600/mo)
   - pgvector 0.8.0 (latest version)
   - 90+ extensions supported
   - Performance Insights (monitor vector queries)
   - **Portability**: High (pgvector widely supported)

2. **Supabase** ($25-599/mo)
   - pgvector 0.6+ supported
   - Built-in vector similarity functions
   - Integrated with Auth/Storage (if building AI apps)
   - **Portability**: High (pgvector portable, 85-95%)

3. **Neon** ($19-700/mo)
   - pgvector 0.7 supported
   - Serverless (autoscaling for index builds)
   - **Portability**: High (pgvector portable)

4. **Timescale** ($110+/mo)
   - pgvector 0.7 supported
   - Time-series + vector embeddings (if combining use cases)
   - **Portability**: High for pgvector (but TimescaleDB creates lock-in if used)

**Avoid**:
- Render, Railway, Heroku (no pgvector support)
- DigitalOcean (basic extensions only, no pgvector by default)

**Migration Path**:
- AWS RDS → Supabase / Neon / Azure / GCP: 4-12 hours (pg_dump + pgvector extension)
- Requires vector index rebuild (HNSW/IVFFlat): 1-4 hours (depending on vector count)

**Cost Optimization**:
- Use Neon for dev/staging (scale-to-zero saves costs)
- Use AWS RDS for production (proven performance)

---

## 5. Analytics / BI (Reporting)

### Characteristics
- **Access Pattern**: Read-heavy (analytical queries, aggregations)
- **Scale**: Large (100GB-10TB)
- **Features**: Complex JOINs, window functions, materialized views
- **Performance**: Query speed critical (seconds for reports)

### Database Requirements
- Optimized for analytical queries (indexes, partitioning)
- Materialized views (pre-computed aggregations)
- Connection pooling (many concurrent report queries)
- Query performance monitoring

### Provider Recommendations

**Best for Analytical Workloads**:
1. **AWS RDS PostgreSQL** ($600-2,000/mo for large datasets)
   - Read replicas (separate analytics from transactional workload)
   - Performance Insights (identify slow queries)
   - Integration with AWS Athena, Redshift (if data warehouse needed)
   - **Alternative**: AWS Aurora PostgreSQL (faster for large datasets, but lock-in)

2. **Azure PostgreSQL - Hyperscale (Citus)** ($700-2,000/mo)
   - Distributed query engine (parallel query execution)
   - Columnar storage (faster aggregations)
   - **Trade-off**: Citus creates lock-in (not portable)

3. **Timescale** ($500-1,500/mo)
   - Continuous aggregates (automatic materialized views)
   - Compression (reduce storage costs for time-series data)
   - **Use if**: Analytics + time-series data combined
   - **Trade-off**: TimescaleDB lock-in (0-20% portable)

**Best for Cost**:
1. **DigitalOcean Managed PostgreSQL** ($480/mo for 8 vCPU, 32GB RAM)
   - Cheapest for large databases
   - Standard PostgreSQL (no vendor-specific features)
   - **Trade-off**: Fewer enterprise features than AWS/Azure

**Migration Path**:
- Standard PostgreSQL: 8-28 hours (pg_dump + test analytical queries)
- Using Citus: 40-160 hours (rewrite for different distributed architecture)
- Using TimescaleDB: 28-96 hours (rewrite continuous aggregates to standard views)

**Alternative**: Consider data warehouse (Redshift, BigQuery, Snowflake) if >1TB and purely analytical

---

## 6. IoT / Time-Series Data

### Characteristics
- **Access Pattern**: High-frequency writes (sensor data, metrics)
- **Scale**: Large (100GB-10TB, millions of rows/day)
- **Features**: Time-series partitioning, compression, retention policies
- **Performance**: Write throughput critical (10K-100K inserts/sec)

### Database Requirements
- Automatic partitioning by time (daily, weekly, monthly)
- Compression (reduce storage costs)
- Data retention policies (auto-delete old data)
- Continuous aggregates (rollups, downsampling)

### Provider Recommendations

**Best for Time-Series**:
1. **Timescale Cloud** ($110-1,500/mo)
   - ✅ TimescaleDB (native time-series extension)
   - ✅ Compression (5-20× storage reduction)
   - ✅ Continuous aggregates (automatic rollups)
   - ✅ Data retention policies
   - **Trade-off**: ⚠️ **Timescale lock-in** (0-20% portability, no alternative PostgreSQL provider supports TimescaleDB)
   - **Migration out**: 28-96 hours (rewrite to standard partitioning + materialized views)

**Alternative (Standard PostgreSQL)**:
1. **AWS RDS PostgreSQL** ($600-2,000/mo) + manual time-series patterns
   - Use pg_partman extension (automatic partitioning)
   - Manual compression (TOAST, or move to S3 for archival)
   - Materialized views (replace continuous aggregates)
   - **Trade-off**: More manual setup, but portable
   - **Portability**: High (standard PostgreSQL, 90-100%)

**Decision Framework**:
- **If time-series is core use case**: Timescale (accept lock-in for superior features)
- **If portability critical**: AWS RDS + pg_partman (more work, but portable)
- **Alternative**: Consider purpose-built time-series DB (InfluxDB, TimescaleDB, QuestDB) if PostgreSQL not required

**Migration Path**:
- Timescale → Standard PostgreSQL: 28-96 hours (rewrite continuous aggregates, compression, retention)
- Standard PostgreSQL → Timescale: 8-16 hours (add TimescaleDB, migrate to hypertables)

---

## 7. Geospatial Application (Maps, Location)

### Characteristics
- **Access Pattern**: Spatial queries (geofencing, proximity search, route planning)
- **Scale**: Medium to large (10GB-1TB)
- **Features**: PostGIS extension, spatial indexes (GiST, BRIN)
- **Performance**: Spatial query speed critical (<100ms)

### Database Requirements
- PostGIS extension (geospatial data types, functions)
- Spatial indexes (GiST index for geometry columns)
- Sufficient compute for spatial query processing
- Monitoring for spatial query performance

### Provider Recommendations

**Best for PostGIS Support**:
1. **AWS RDS PostgreSQL** ($100-600/mo)
   - PostGIS 3.4.2 (latest version)
   - 90+ extensions supported
   - Performance Insights (monitor spatial queries)
   - **Portability**: High (PostGIS widely supported, 90-100%)

2. **Supabase** ($25-599/mo)
   - PostGIS 3.3+ supported
   - Geospatial functions available
   - **Portability**: High (PostGIS portable, 90-100%)

3. **Azure / GCP / Timescale** ($120-600/mo)
   - PostGIS 3.3-3.4 supported
   - All major providers support PostGIS
   - **Portability**: High (90-100%)

**Avoid**:
- Render, Railway, Heroku (no or limited PostGIS support)
- DigitalOcean (basic extensions, PostGIS manual setup)
- Neon (PostGIS support limited/experimental)

**Migration Path**:
- AWS RDS → Supabase / Azure / GCP / Timescale: 4-12 hours
  - pg_dump with PostGIS data
  - Enable PostGIS on target: `CREATE EXTENSION postgis;`
  - Restore, rebuild spatial indexes (GiST)
  - Test spatial queries (proximity, geofencing)

**Portability**: ✅ **High (90-100%)** - PostGIS is widely supported, migration is straightforward

---

## 8. E-Commerce Platform

### Characteristics
- **Access Pattern**: Transactional (ACID compliance critical)
- **Scale**: Medium to large (10GB-1TB)
- **Features**: Transactions, foreign keys, constraints, inventory management
- **Performance**: Low latency (<50ms), high concurrency

### Database Requirements
- ACID compliance (transactions, rollback, isolation)
- Foreign keys, constraints (data integrity)
- Connection pooling (handle traffic spikes)
- Backups (point-in-time recovery for data loss)
- High availability (99.99%+ uptime)

### Provider Recommendations

**Best for Reliability**:
1. **AWS RDS PostgreSQL** ($100-600/mo)
   - Multi-AZ (99.99% availability)
   - Automated backups (35 days retention)
   - Read replicas (scale reads for product catalog)
   - **Portability**: High (standard PostgreSQL, 95-100%)

2. **Azure Database for PostgreSQL - Flexible Server** ($120-700/mo)
   - Zone-redundant HA (99.99% availability)
   - Automated backups (35 days retention)
   - **Portability**: High (standard PostgreSQL, 95-100%)

3. **Google Cloud SQL for PostgreSQL** ($110-650/mo)
   - Regional HA (99.99% availability)
   - Automated backups, point-in-time recovery
   - **Portability**: High (standard PostgreSQL, 95-100%)

**Best for Cost + Reliability**:
1. **Supabase Pro/Team** ($25-599/mo)
   - Daily backups (Pro: 7 days, Team: 14 days)
   - Connection pooling (PgBouncer)
   - Real-time inventory updates (if needed)
   - **Trade-off**: Less proven at enterprise scale than AWS/Azure/GCP

**Avoid**:
- Free tiers (paused after inactivity, deleted after 90 days)
- Render free (not suitable for production e-commerce)
- Railway (usage-based pricing can spike during traffic surges)

**Migration Path**:
- Standard PostgreSQL: 8-16 hours (pg_dump + extensive transaction testing)
- Critical: Test transaction isolation, foreign key constraints, concurrent updates

**Portability**: ✅ **High (95-100%)** - Core SQL, standard transactions, portable across all providers

---

## 9. Prototype / MVP (<1GB)

### Characteristics
- **Access Pattern**: Low traffic (10-100 requests/hour)
- **Scale**: Very small (<1GB)
- **Features**: Basic CRUD, no advanced features
- **Performance**: Medium latency acceptable (100-500ms)

### Provider Recommendations

**Best Free Tier**:
1. **Neon Free** ($0/mo)
   - ✅ 3GB storage (largest free tier)
   - ✅ Scale-to-zero (no charges when inactive)
   - ✅ 5 compute branches (dev/staging/prod)
   - **Limitation**: 191.9 CU-hours/month compute limit
   - **Portability**: High (standard PostgreSQL)

2. **Supabase Free** ($0/mo)
   - ✅ 500MB storage
   - ✅ Includes Auth, Storage, Realtime (bonus features for prototypes)
   - **Limitation**: Paused after 7 days inactivity (need to unpause)
   - **Portability**: High (if not using Supabase features)

3. **Railway Trial** ($5 one-time credit)
   - ✅ No time limit (credit expires in 30 days, but flexible usage)
   - **Portability**: High (standard PostgreSQL)

**Best Paid (if need always-on)**:
1. **DigitalOcean Managed PostgreSQL** ($15/mo)
   - Cheapest always-on option
   - 1 vCPU, 1GB RAM, 10GB storage
   - **Portability**: High (standard PostgreSQL)

**Migration Path**: Easy (core SQL, 1-2 hours to export/import)

---

## 10. Enterprise (Mission-Critical)

### Characteristics
- **Access Pattern**: High concurrency (1K-10K queries/sec)
- **Scale**: Large to massive (1TB-100TB)
- **Features**: High availability, encryption, compliance, audit logs
- **Performance**: Ultra-low latency (<10ms), 99.99%+ uptime

### Database Requirements
- Multi-region high availability (failover <30 seconds)
- Encryption at rest and in transit
- Compliance certifications (SOC2, HIPAA, FedRAMP)
- Advanced monitoring (query performance, slow queries, deadlocks)
- Dedicated support (24/7, SLA-backed)

### Provider Recommendations

**Best for Enterprise**:
1. **AWS RDS PostgreSQL** ($2,000-10,000+/mo)
   - Multi-AZ HA (99.99% SLA)
   - Global databases (multi-region replication)
   - Encryption (KMS, at-rest and in-transit)
   - Compliance: SOC2, HIPAA, FedRAMP High
   - AWS Support (Enterprise: $15K+/mo)
   - **Alternative**: AWS Aurora PostgreSQL (faster, but lock-in)

2. **Azure Database for PostgreSQL - Hyperscale** ($2,000-15,000+/mo)
   - Zone-redundant HA (99.99% SLA)
   - Distributed architecture (Citus)
   - Encryption (Azure Key Vault)
   - Compliance: SOC2, HIPAA, FedRAMP High
   - **Trade-off**: Citus creates lock-in

3. **Google Cloud SQL for PostgreSQL** ($2,000-12,000+/mo)
   - Regional HA (99.99% SLA)
   - Encryption (Cloud KMS)
   - Compliance: SOC2, HIPAA, FedRAMP High

4. **Crunchy Data** ($800-5,000+/mo)
   - Enterprise PostgreSQL specialist
   - Kubernetes-based (multi-cloud deployment)
   - Compliance: SOC2, HIPAA, FedRAMP Ready
   - **Portability**: High (standard PostgreSQL + extensions)

**Avoid**:
- Supabase, Neon (newer providers, less proven at enterprise scale)
- Render, Railway (not enterprise-grade)
- DigitalOcean (basic features, limited compliance)

**Migration Path**:
- Enterprise migrations: 40-160 hours (extensive testing, cutover planning, compliance validation)
- Requires staging environment, load testing, performance validation

**Portability**: Medium to High (depends on features used)
- Core PostgreSQL: High (95-100%)
- Cloud-specific features (Aurora, Citus): Low (0-40%)

---

## Decision Matrix

| Use Case | Best Provider | Runner-Up | Avoid | Migration Effort |
|----------|---------------|-----------|-------|------------------|
| **Web App (CRUD)** | Supabase, Neon | Railway, DigitalOcean | AWS/Azure (overkill) | 1-4 hours |
| **SaaS (Multi-Tenant)** | AWS RDS, Neon | Supabase | Railway, Render | 4-16 hours |
| **Mobile Backend** | Supabase | Neon + Pusher | AWS (complex) | 4-80 hours |
| **AI/ML (pgvector)** | AWS RDS, Supabase | Neon, Timescale | Render, Railway | 4-12 hours |
| **Analytics/BI** | AWS RDS, Timescale | DigitalOcean | Neon (small compute) | 8-96 hours |
| **IoT/Time-Series** | Timescale | AWS RDS + pg_partman | Supabase, Neon | 8-96 hours |
| **Geospatial** | AWS RDS, Supabase | Azure, GCP, Timescale | Render, Railway, Neon | 4-12 hours |
| **E-Commerce** | AWS RDS, Azure | GCP, Supabase | Free tiers | 8-16 hours |
| **Prototype/MVP** | Neon Free, Supabase Free | Railway Trial | Heroku (no free tier) | 1-2 hours |
| **Enterprise** | AWS RDS, Crunchy Data | Azure, GCP | Supabase, Neon | 40-160 hours |

---

## Portability vs Features Trade-Off

### High Portability (Core SQL Only)

**Strategy**: Use only standard PostgreSQL features
**Providers**: Any PostgreSQL provider
**Migration**: 1-8 hours (pg_dump/restore)
**Cost**: Variable ($0-2,000/mo depending on scale)

**When to Choose**:
- ✅ Vendor independence critical
- ✅ Multi-cloud strategy
- ✅ Future provider flexibility desired

**Trade-offs**:
- ❌ Miss out on provider-specific features (Supabase Auth, Neon branching, Timescale compression)
- ❌ More manual work (build features yourself)

---

### Medium Portability (PostgreSQL Extensions)

**Strategy**: Use widely-supported extensions (PostGIS, pgvector)
**Providers**: AWS RDS, Azure, GCP, Supabase, Timescale
**Migration**: 4-16 hours (pg_dump + extension verification)
**Cost**: $25-2,000/mo

**When to Choose**:
- ✅ Need extensions (geospatial, vector search)
- ✅ Portability still important (can switch among major providers)
- ✅ Extension widely supported (PostGIS, pgvector)

**Trade-offs**:
- ⚠️ Some providers don't support all extensions (Render, Railway)
- ⚠️ Extension versions may differ slightly

---

### Low Portability (Cloud-Specific Features)

**Strategy**: Use provider-specific features (Supabase Auth, Neon branching, Timescale compression, Aurora)
**Providers**: Specific to feature
**Migration**: 40-160 hours (rewrite features)
**Cost**: $25-15,000/mo

**When to Choose**:
- ✅ Features provide significant value (faster development, better performance)
- ✅ Committed to provider long-term
- ✅ Migration cost acceptable if needed

**Trade-offs**:
- 🔴 Vendor lock-in (20-40% portability for Supabase BaaS, 0-20% for Timescale)
- 🔴 Migration requires application changes

---

## Key Takeaways

1. **Core SQL = maximum portability** (99-100%, 1-4 hour migrations)
2. **PostGIS & pgvector widely supported** (90-100%, 4-12 hour migrations)
3. **TimescaleDB creates extreme lock-in** (0-20%, 28-96 hour migrations)
4. **Supabase BaaS features create lock-in** (20-40%, 40-80 hour migrations if heavily used)
5. **Cost leaders**: Neon/Supabase free tiers (prototypes), DigitalOcean ($15-480/mo, production)
6. **Enterprise leaders**: AWS RDS, Azure, GCP, Crunchy Data (proven, compliant, expensive)
7. **AI/ML**: Requires pgvector (AWS RDS, Supabase, Neon, Timescale)
8. **Time-series**: Timescale is best (but lock-in), AWS RDS + pg_partman is portable alternative
9. **Mobile/Real-time**: Supabase wins (all-in-one BaaS), but creates lock-in if heavily used
10. **Web apps**: Supabase, Neon, Railway offer best value for small-medium scale

**Most Common Recommendation**:
- **Prototypes**: Neon Free or Supabase Free
- **Startups**: Supabase Pro ($25) or Neon Launch ($19)
- **Production**: DigitalOcean ($15-480) for cost, AWS RDS ($100-2,000) for scale/reliability
- **Enterprise**: AWS RDS or Crunchy Data (compliance, support, global HA)
