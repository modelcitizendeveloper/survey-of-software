# S3 Scenario 3: E-commerce Reporting

**Business Profile**: Mid-market online retailer with $50M annual revenue, 200 employees, serving both B2C and B2B customers across North America.

**Data Warehouse Need**: Operational reporting platform for daily business operations, inventory forecasting, marketing attribution, and executive dashboards.

**Decision Context**: Heavy AWS investment (EC2, RDS, S3, Lambda) with existing data engineering team comfortable with SQL and Postgres. Need to consolidate reporting from 15+ disparate systems into unified analytics platform.

---

## 1. Scenario Profile

### Business Context

**Company Stage**: Series B-funded, mid-market e-commerce retailer in high-growth phase (40% YoY revenue growth). The company operates a direct-to-consumer website, B2B wholesale portal, and marketplace presence (Amazon, Walmart). Primary product categories include home goods and consumer electronics with average order value of $85 (B2C) and $1,200 (B2B).

**Key Business Challenges**:
- **Inventory optimization**: $8M in inventory with 180-day turn rate—need better forecasting to reduce stockouts (currently 12% of SKUs) and overstock (22% of inventory aging beyond 90 days)
- **Marketing attribution**: $400K/month ad spend across 8 channels with unclear ROI—CMO needs to understand which channels drive profitable customers
- **Operational efficiency**: Operations team manually exports data from 6 systems daily to create Excel-based reports, consuming 15 hours/week of analyst time
- **Executive visibility**: CEO and board lack real-time visibility into key metrics—currently rely on weekly email reports with 5-day data lag

**Success Metrics**:
- Reduce manual reporting time from 15 hours/week to <2 hours/week (87% reduction)
- Enable daily inventory reports by 8 AM for operations team (currently weekly, 5-day lag)
- Provide marketing attribution dashboard with 24-hour data freshness (currently manual monthly analysis)
- Support 100 concurrent users during business hours without performance degradation
- Achieve sub-5 second query times for operational dashboards
- Stay within $15,000/month total cost budget (warehouse + ETL + BI tools)

### Technical Context

**Current State**: Fragmented data landscape across multiple systems:
- **Transactional database**: PostgreSQL 14 RDS instance (500GB) storing orders, customers, products, inventory
- **Web analytics**: Google Analytics 4 + custom event tracking (500K events/day)
- **Marketing platforms**: Facebook Ads, Google Ads, Amazon Advertising (API data)
- **ERP system**: NetSuite for financials, purchasing, inventory management
- **Warehouse management**: ShipStation for logistics, shipping, fulfillment
- **Customer support**: Zendesk with 2,000 tickets/month
- **Payment processing**: Stripe for payment transactions, refunds, disputes
- **Spreadsheets**: 20+ Excel/Google Sheets files for manual calculations, forecasts, reports

**Existing Cloud Platform**: Deeply committed to AWS ecosystem:
- **Compute**: 15 EC2 instances (web servers, API servers, workers)
- **Database**: RDS PostgreSQL (primary transactional DB), RDS MySQL (legacy B2B portal)
- **Storage**: 50TB in S3 (product images, logs, backups, exports)
- **Streaming**: Kinesis Data Streams for real-time event ingestion (web clickstream)
- **ETL**: AWS Glue for basic data lake ETL jobs (CSV exports to S3)
- **Identity**: IAM-based access control across all services
- **Monitoring**: CloudWatch for logging, alerting, dashboards

**Team Composition**:
- **Data engineer** (1 FTE): Senior engineer with 5 years Postgres/SQL experience, 2 years AWS experience
- **BI analyst** (2 FTE): Mid-level analysts skilled in SQL, Excel, Tableau; limited Python experience
- **Analytics engineer** (0.5 FTE): Part-time contractor with dbt experience, Python proficiency
- **Stakeholder users** (100): Operations (25), marketing (15), supply chain (20), sales (30), executives (10)

**Technical Constraints**:
- **AWS preference**: Strong preference for AWS-native solutions to leverage existing IAM, VPC, and operational expertise
- **Postgres familiarity**: Team comfortable with Postgres SQL dialect; desire minimal reskilling
- **Data freshness**: Daily batch loads sufficient for most use cases (no real-time requirement except web clickstream)
- **Business hours queries**: 95% of queries occur 8 AM - 8 PM EST (12-hour window)
- **Compliance**: PCI DSS compliance required for payment card data (tokenized in Stripe, limited exposure)
- **Budget constraint**: $15,000/month total budget ceiling (board-approved)

### Data Characteristics

**Current Data Volume**: 50TB total across all systems
- **Transactional data**: 500GB (orders, line items, customers, products, inventory snapshots)
  - 5M orders (3 years history)
  - 18M order line items
  - 800K customers
  - 12,000 SKUs
  - Daily inventory snapshots (365 days × 12K SKUs)
- **Web analytics**: 20TB (clickstream events, sessions, pageviews—3 years history)
- **Marketing data**: 50GB (campaign data, ad performance, attribution—2 years history)
- **Logistics data**: 100GB (shipments, tracking, delivery times, returns—2 years history)
- **Customer support**: 25GB (tickets, conversations, satisfaction scores—3 years history)
- **Financial data**: 150GB (invoices, payments, refunds, commissions—5 years history)
- **Data lake exports**: 30TB (CSV/JSON exports, logs, raw files in S3)

**Growth Rate**: 25% annual data volume growth
- Revenue growing 40% YoY but data volume growing faster due to increased event tracking
- Adding 150K new customers annually
- Expanding product catalog by 20% annually (2,400 new SKUs/year)
- Web traffic growing 35% YoY as marketing scales

**Number of Data Sources**: 15 distinct systems
- **Core transactional**: PostgreSQL RDS (orders, customers, inventory)
- **Legacy systems**: MySQL RDS (B2B portal—legacy, migrating off)
- **SaaS platforms**: NetSuite (ERP), Stripe (payments), Zendesk (support)
- **Marketing**: Google Analytics 4, Facebook Ads API, Google Ads API, Amazon Advertising API
- **Logistics**: ShipStation API, freight carrier APIs (UPS, FedEx, USPS)
- **Data lake**: S3 buckets with CSV/JSON exports from various systems
- **Spreadsheets**: Google Sheets (manual forecasts, planning data)

**Data Types**: Primarily structured with some semi-structured
- **Structured (85%)**: Relational tables from Postgres, MySQL, NetSuite—well-defined schemas
- **Semi-structured (15%)**: JSON event payloads from Google Analytics, API responses, webhooks
- **Unstructured (<1%)**: Customer support text (future NLP analysis potential)

### User Requirements

**Primary Users**:
- **Operations team (25 users)**: Need daily inventory reports, order fulfillment dashboards, warehouse performance metrics—access 8-11 AM daily
- **Marketing team (15 users)**: Need campaign performance dashboards, customer acquisition cost analysis, channel attribution—access throughout day
- **Supply chain team (20 users)**: Need inventory forecasting models, supplier performance reports, stockout alerts—access weekly + ad-hoc
- **Sales team (30 users)**: Need B2B customer dashboards, sales pipeline reports, account health scores—access throughout day
- **Executives (10 users)**: Need KPI dashboards, board reports, trend analysis—access weekly + monthly board meetings

**Query Patterns**:
- **Daily operational reports (70% of queries)**: Pre-built dashboards refreshed nightly via batch ETL
  - Inventory status by warehouse, SKU velocity, reorder recommendations
  - Order fulfillment rates, shipping times, delivery exceptions
  - Customer acquisition costs by channel, ROAS (return on ad spend) dashboards
  - Revenue dashboards: daily sales, YoY growth, category performance
- **Ad-hoc analysis (25% of queries)**: Analysts exploring data, answering business questions
  - "Which products have highest return rates by category?"
  - "What's the lifetime value of customers acquired from Facebook vs Google?"
  - "Which zip codes have slowest delivery times?"
- **Executive reporting (5% of queries)**: Monthly/quarterly aggregations for board reports
  - Three-year revenue trends, cohort analysis, strategic planning metrics

**Concurrency**: 100 total users, but queries concentrated during business hours
- **Peak hours (9-11 AM EST)**: 50 concurrent users (operations + marketing morning reviews)
- **Business hours (8 AM - 8 PM EST)**: Average 30 concurrent users
- **Off-hours (8 PM - 8 AM EST)**: 1-5 concurrent users (mostly automated batch jobs)
- **Batch ETL window**: Midnight - 6 AM EST (6-hour window for daily loads)

**SLA Expectations**:
- **Dashboard queries**: Sub-5 second response time for operational dashboards (P95 latency)
- **Ad-hoc queries**: Sub-30 second response time for moderate complexity queries (aggregations across millions of rows)
- **Batch ETL**: Complete daily loads within 6-hour overnight window (midnight - 6 AM)
- **Data freshness**: Daily updates sufficient; no real-time requirement (24-hour max staleness acceptable)
- **Uptime**: 99.5% availability during business hours (8 AM - 8 PM EST, Monday-Friday)

---

## 2. Requirements Matrix

### MoSCoW Prioritization

#### Must Have (Deal-Breakers)

| Requirement | Rationale | Scoring Weight |
|-------------|-----------|----------------|
| **AWS-native integration** | Existing AWS infrastructure (IAM, VPC, S3, RDS) must integrate seamlessly | 20 points |
| **Postgres SQL compatibility** | Team expertise in Postgres; minimize reskilling and query rewrites | 15 points |
| **50TB storage capacity** | Current data volume with 25% annual growth headroom | 15 points |
| **100+ concurrent users** | Support operations, marketing, sales, supply chain teams simultaneously | 10 points |
| **Sub-5 second dashboard queries** | Operational dashboards must load quickly during peak morning hours | 10 points |
| **<$15,000/month total cost** | Board-approved budget ceiling (warehouse + ETL + BI tools) | 15 points |
| **Daily batch ETL support** | Nightly data loads from 15+ sources within 6-hour window | 10 points |
| **SOC 2 / PCI DSS compliance** | Payment card data handling requires compliance certification | 5 points |

**Total Must-Have Points**: 100 points

#### Should Have (Important but Flexible)

| Requirement | Rationale | Scoring Weight |
|-------------|-----------|----------------|
| **Semi-structured data support** | JSON event payloads from Google Analytics, API webhooks | 10 points |
| **Materialized views** | Pre-aggregate expensive queries for dashboard performance | 8 points |
| **Auto-suspend/resume** | Reduce costs during off-hours when query load is minimal | 8 points |
| **S3 integration (external tables)** | Query data lake exports in S3 without full ETL ingestion | 8 points |
| **BI tool connectors** | Native Tableau, Looker, Metabase connectors for seamless integration | 7 points |
| **dbt compatibility** | Enable modern analytics engineering workflows with dbt transformations | 7 points |
| **Query result caching** | Eliminate redundant compute costs for repeated dashboard queries | 6 points |
| **Workload isolation** | Separate ETL batch jobs from interactive user queries (resource isolation) | 6 points |

**Total Should-Have Points**: 60 points

#### Could Have (Nice-to-Have)

| Requirement | Rationale | Benefit |
|-------------|-----------|---------|
| **Machine learning integration** | Future: demand forecasting, churn prediction, dynamic pricing models | Future innovation |
| **Real-time streaming ingestion** | Future: real-time inventory updates, live web analytics dashboards | Competitive edge |
| **Cross-region replication** | Future: expand to EU market, require EU data residency compliance | Geographic expansion |
| **Data sharing capabilities** | Future: share sales data with B2B partners, vendors via secure shares | Partner ecosystem |
| **Python/Pandas integration** | Future: enable data scientists to run Python notebooks on warehouse data | Advanced analytics |

#### Won't Have (Out of Scope)

| Feature | Reason |
|---------|--------|
| **Multi-cloud portability** | Committed to AWS ecosystem; no GCP or Azure requirement |
| **Sub-second query latency** | Daily operational reports don't require real-time/sub-second performance |
| **Graph analytics** | No graph-based use cases (supply chain network analysis deferred to future) |
| **Video/image analytics** | Product images stored in S3; no warehouse-based image processing needed |
| **Transactional OLTP** | Postgres RDS handles transactional workloads; warehouse is analytics-only |

---

## 3. Provider Shortlist

### Long List Elimination (8 → 3 Finalists)

**Eliminated Immediately**:

1. **Azure Synapse Analytics**: Azure-only, not AWS-native (fails Must-Have: AWS integration) ❌
2. **Apache Druid**: Real-time focus with sub-second latency not required; adds operational complexity ❌
3. **Firebolt**: Requires $24K-40K annual platform fee, exceeds budget for 50TB scale ❌

**Eliminated After Analysis**:

4. **Google BigQuery**: Not AWS-native, requires GCP account; team prefers AWS ecosystem (weak AWS integration) ❌
5. **Databricks Lakehouse**: Optimized for ML/AI workloads which aren't immediate priority; higher learning curve than traditional SQL warehouses ❌

**Finalists (3 platforms)**:

1. **Amazon Redshift** (Primary Recommendation)
2. **Snowflake** (Runner-Up)
3. **ClickHouse Cloud** (Budget Alternative)

---

### Shortlist Profiles

#### 1. Amazon Redshift (Primary Winner)

**Why Included**: Perfect fit for AWS-native e-commerce scenario
- **AWS ecosystem integration**: Seamless integration with existing RDS, S3, Glue, Kinesis, IAM, CloudWatch infrastructure
- **Postgres compatibility**: Postgres 11 SQL dialect matches team expertise (minimal reskilling)
- **Mature ecosystem**: 13+ years production deployments, extensive community resources, proven at e-commerce scale
- **Redshift Serverless**: Auto-scaling, pay-per-second billing aligns with 12-hour business day usage pattern
- **Cost-effective**: ~$5,000-8,000/month for 50TB with moderate query load (well within $15K budget)

**Concerns**:
- **Query performance**: Slower than ClickHouse for sub-second queries (typically 2-10s for complex aggregations)
- **Semi-structured data**: Limited JSON support compared to Snowflake (SUPER data type improving but less elegant)
- **Learning curve**: Requires understanding of distribution keys, sort keys, workload management for optimal performance

**Cost Estimate**:
- **Monthly**: $7,500 (32 RPUs Serverless, 50% utilization + managed storage)
- **3-Year TCO**: $270,000 (includes 20% annual data growth, reserved capacity discounts)

**Implementation Complexity**: Medium (4-6 weeks)
- Week 1-2: Provision Redshift Serverless, connect RDS sources, first queries
- Week 3-4: ETL pipelines via Glue/Fivetran, dbt transformations
- Week 5-6: Tableau dashboards, user training, production rollout

**Scoring**: 95/100 Must-Have + 52/60 Should-Have = **147/160 Total**

---

#### 2. Snowflake (Runner-Up)

**Why Included**: Best-in-class data warehouse features
- **Zero-maintenance**: Fully managed with no cluster tuning, automatic query optimization
- **Multi-cloud optionality**: Future-proofs against potential cloud strategy changes
- **Superior semi-structured data**: VARIANT data type handles JSON/nested data elegantly
- **Data sharing**: Future B2B partner data sharing via secure shares (not immediate need but valuable)
- **Ecosystem strength**: Strongest BI tool integrations, dbt support, extensive community

**Concerns**:
- **Cost premium**: ~$12,000/month for equivalent workload (60% higher than Redshift)
- **AWS integration**: Requires AWS PrivateLink setup; not as seamless as Redshift's native AWS integration
- **Overkill for use case**: Many advanced features (data sharing, multi-cloud, ML) not needed for daily operational reporting

**Cost Estimate**:
- **Monthly**: $12,100 (Medium warehouse 12hr/day + 50TB storage)
- **3-Year TCO**: $437,400 (includes auto-scaling, result caching optimization)

**Implementation Complexity**: Low (3-4 weeks)
- Week 1: Provision Snowflake account, configure AWS PrivateLink, connect sources
- Week 2-3: ELT pipelines, dbt transformations, data modeling
- Week 4: Dashboard development, training, production cutover

**Scoring**: 85/100 Must-Have (loses points on AWS integration, cost) + 58/60 Should-Have = **143/160 Total**

---

#### 3. ClickHouse Cloud (Budget Alternative)

**Why Included**: Best price-performance ratio
- **Cost leader**: ~$3,265/month for 50TB workload (56% lower than Redshift)
- **Fast queries**: Sub-second query latency for operational dashboards (10x faster than Redshift)
- **Excellent compression**: 10-40x compression ratios reduce storage costs dramatically
- **AWS deployment**: Available on AWS (us-east-1, us-west-2) with VPC peering
- **Open-source flexibility**: No vendor lock-in; can self-host if Cloud becomes expensive

**Concerns**:
- **Operational complexity**: Requires deeper technical expertise than managed Redshift/Snowflake
- **Limited ecosystem**: Fewer pre-built connectors; requires more custom ETL development
- **BI tool integration**: Tableau/Looker connectors exist but less mature than Redshift/Snowflake
- **Team learning curve**: Team has no ClickHouse experience; SQL dialect differences require training
- **Compliance**: SOC 2 certified but PCI DSS compliance requires self-assessment (less turnkey)

**Cost Estimate**:
- **Monthly**: $3,265 (10 compute units, 16hr/day + 50TB compressed storage)
- **3-Year TCO**: $149,374 (includes production tier, aggressive compression)

**Implementation Complexity**: High (8-10 weeks)
- Week 1-2: ClickHouse Cloud setup, VPC peering, team training
- Week 3-5: Custom ETL development (ClickPipes, Airbyte, Python scripts)
- Week 6-7: Data modeling (ReplacingMergeTree, aggregating tables), query optimization
- Week 8-10: Tableau integration, user training, production rollout

**Scoring**: 75/100 Must-Have (loses points on Postgres compatibility, ecosystem maturity) + 45/60 Should-Have = **120/160 Total**

---

### Winner Selection

**Primary Recommendation: Amazon Redshift** (Score: 147/160)

**Rationale**:
1. **Perfect AWS fit**: Native integration with existing RDS, S3, Glue, IAM eliminates integration friction
2. **Team expertise**: Postgres SQL compatibility leverages existing team skills (zero reskilling required)
3. **Proven at scale**: 13+ years of production e-commerce deployments; mature, battle-tested platform
4. **Cost-effective**: $7,500/month leaves $7,500/month budget headroom for ETL tools (Fivetran $3K), BI tools (Tableau $2K), infrastructure ($1.5K)
5. **Low risk**: Redshift Serverless auto-scaling handles business hours concurrency without capacity planning

**Runner-Up: Snowflake** (Score: 143/160)

**Choose Snowflake if**:
- Budget increases to $20K/month (Snowflake's premium features justify 60% higher cost)
- Multi-cloud strategy emerges (CEO considering GCP/Azure for geographic expansion)
- Advanced data sharing needed (B2B partners, vendor collaboration becomes strategic priority)
- Team lacks AWS expertise and wants zero-maintenance operation

**Budget Alternative: ClickHouse Cloud** (Score: 120/160)

**Choose ClickHouse if**:
- Budget drops below $10K/month (ClickHouse saves $4K/month vs Redshift)
- Sub-second query performance becomes critical (real-time dashboards, customer-facing analytics)
- Data engineering team has bandwidth for custom integration development
- Company values open-source flexibility and wants to avoid cloud vendor lock-in

---

## 4. Architecture Pattern

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          DATA SOURCES (15)                          │
├─────────────────────────────────────────────────────────────────────┤
│  [PostgreSQL RDS]  [NetSuite]  [Stripe]  [Google Analytics 4]      │
│  [ShipStation]  [Zendesk]  [Facebook Ads]  [Google Ads]  [S3 CSVs] │
└────────────┬────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       INGESTION LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│  Fivetran (SaaS connectors): NetSuite, Stripe, Zendesk, Ads APIs   │
│  AWS DMS (Database CDC): PostgreSQL RDS → S3 (staged)               │
│  AWS Glue (S3 ETL): CSV/JSON exports → Parquet transformation       │
│  Airbyte (Open-source): ShipStation, custom APIs → S3               │
└────────────┬────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     STAGING LAYER (S3)                               │
├─────────────────────────────────────────────────────────────────────┤
│  s3://company-data-lake/raw/orders/YYYY-MM-DD/*.parquet             │
│  s3://company-data-lake/raw/analytics/YYYY-MM-DD/*.json             │
│  s3://company-data-lake/raw/marketing/YYYY-MM-DD/*.csv              │
│  (100TB raw data, 90-day retention, compressed Parquet/JSON)        │
└────────────┬────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STORAGE + PROCESSING                              │
│                   Amazon Redshift Serverless                         │
├─────────────────────────────────────────────────────────────────────┤
│  Base Capacity: 32 RPUs (auto-scales 32-128 RPUs during peak)       │
│  Managed Storage: 50TB → 5-8TB compressed (10:1 compression)        │
│                                                                       │
│  Schema Design:                                                      │
│    • raw schema: Staged data from S3 (COPY command)                 │
│    • staging schema: dbt incremental models, data quality tests     │
│    • mart schema: Business-ready fact/dimension tables              │
│    • metrics schema: Pre-aggregated metrics, materialized views     │
│                                                                       │
│  Workload Management:                                                │
│    • ETL queue: Batch jobs (midnight-6AM), priority 3               │
│    • Dashboard queue: Operational dashboards, priority 1            │
│    • Ad-hoc queue: Analyst queries, priority 2                      │
└────────────┬────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    TRANSFORMATION LAYER                              │
├─────────────────────────────────────────────────────────────────────┤
│  dbt Core (orchestrated via Airflow):                                │
│    • 50+ dbt models: staging → intermediate → mart                  │
│    • Incremental models for large tables (orders, events)           │
│    • Data quality tests (not_null, unique, accepted_values)         │
│    • Documentation (model descriptions, column definitions)          │
│                                                                       │
│  Example dbt models:                                                 │
│    • stg_orders: Clean, deduplicated orders from raw.orders         │
│    • int_customer_orders: Join orders + customers + line_items      │
│    • fct_orders: Final fact table with business logic               │
│    • dim_products: Product dimension with SKU attributes            │
│    • mrt_inventory_daily: Daily inventory snapshots by warehouse    │
│    • mrt_marketing_attribution: Multi-touch attribution logic       │
└────────────┬────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    CONSUMPTION LAYER                                 │
├─────────────────────────────────────────────────────────────────────┤
│  [Tableau Cloud]: Operations dashboards, executive KPIs (100 users) │
│  [Metabase]: Ad-hoc SQL editor for analysts (15 power users)        │
│  [AWS QuickSight]: Embedded customer-facing analytics (future)      │
│  [Reverse ETL - Census]: Sync Redshift → Salesforce, HubSpot       │
│  [Jupyter Notebooks]: Data science experimentation (Python/pandas)  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION                                     │
├─────────────────────────────────────────────────────────────────────┤
│  Amazon MWAA (Managed Airflow): Schedule dbt runs, monitor pipelines│
│    • DAG: nightly_etl (midnight-6AM): Fivetran sync → dbt run       │
│    • DAG: hourly_refresh: Refresh materialized views (dashboards)   │
│    • DAG: weekly_reports: Generate executive summary emails         │
│    • Slack alerts: Pipeline failures, data quality test failures    │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### Data Sources (15 systems)

**Core transactional**:
- PostgreSQL RDS (500GB): Orders, customers, products, inventory—ingested via AWS DMS CDC
- MySQL RDS (100GB): Legacy B2B portal—batch COPY nightly (deprecated, migrating to Postgres)

**SaaS platforms** (Fivetran connectors):
- NetSuite ERP: Financials, purchasing, supplier data—synced every 6 hours
- Stripe: Payments, refunds, disputes, subscriptions—synced every 1 hour
- Zendesk: Support tickets, conversations, CSAT scores—synced daily
- ShipStation: Shipments, tracking, carrier performance—synced every 6 hours

**Marketing APIs** (Fivetran/custom):
- Google Analytics 4: Web events, sessions, conversions—batch export daily
- Facebook Ads API: Campaign performance, ad spend, impressions—synced hourly
- Google Ads API: Search/display campaigns, keywords, conversions—synced hourly
- Amazon Advertising: Sponsored products, brand campaigns—synced daily

**Data lake exports**:
- S3 buckets: CSV/JSON exports from legacy systems, manual uploads, archived data

#### Ingestion Layer

**Fivetran** ($3,000/month, 500M rows/month):
- Pre-built connectors for NetSuite, Stripe, Zendesk, Facebook Ads, Google Ads
- Automatic schema drift detection, data type management
- Incremental sync strategies (timestamp, cursor, log-based)
- Native Redshift destination with automatic table creation

**AWS Database Migration Service (DMS)** (included in AWS costs):
- Real-time CDC from PostgreSQL RDS → S3 staging (Parquet format)
- Tracks transaction logs (WAL) for insert/update/delete changes
- Minimal impact on source database performance

**AWS Glue** ($500/month for 100 DPU-hours):
- Transform S3 CSV/JSON exports → Parquet (10x compression, faster queries)
- Glue Catalog: Central metadata registry for S3 data lake tables
- Scheduled jobs: Nightly transformations, data validation, deduplication

**Airbyte Open-Source** (self-hosted on EC2 t3.large, $100/month):
- Custom connectors for ShipStation, niche APIs without Fivetran support
- Python-based custom source connectors for internal APIs
- Destination: S3 (staged) → Redshift COPY

#### Storage Layer: Amazon Redshift Serverless

**Configuration**:
- **Base capacity**: 32 RPUs (Redshift Processing Units)
- **Auto-scaling**: Scales to 128 RPUs during peak hours (9-11 AM EST)
- **Managed storage**: S3-backed storage, scales automatically with data growth
- **Compression**: ENCODE AUTO applies optimal compression (10:1 typical for e-commerce data)

**Schema Design** (4-schema structure):

**1. raw schema** (staging from S3):
```sql
raw.orders_staged          -- Daily COPY from S3 DMS exports
raw.customers_staged       -- Full snapshot nightly
raw.ga4_events_staged      -- Daily event exports (partitioned by date)
raw.stripe_charges_staged  -- Incremental sync via Fivetran
```

**2. staging schema** (dbt staging models):
```sql
staging.stg_orders         -- Cleaned, typed, deduplicated orders
staging.stg_customers      -- Customer dimension with SCD Type 2
staging.stg_products       -- Product dimension with attributes
staging.stg_inventory      -- Daily inventory snapshots
```

**3. mart schema** (business-ready models):
```sql
mart.fct_orders            -- Order fact table (20M rows)
mart.fct_order_lines       -- Order line item fact (60M rows)
mart.dim_customers         -- Customer dimension (800K rows)
mart.dim_products          -- Product dimension (12K rows)
mart.dim_date              -- Date dimension (3 years = 1,095 rows)
mart.fct_inventory_daily   -- Daily inventory fact (4M rows)
mart.fct_web_sessions      -- Web analytics session fact (50M rows)
```

**4. metrics schema** (pre-aggregated for dashboards):
```sql
metrics.daily_revenue           -- Materialized view: daily revenue by channel
metrics.inventory_velocity      -- SKU velocity (90-day rolling average)
metrics.marketing_attribution   -- Multi-touch attribution (weekly refresh)
metrics.customer_ltv            -- Customer lifetime value by cohort
```

**Distribution and Sort Keys** (performance optimization):
```sql
-- fct_orders: Distribute by customer_id (frequent joins), sort by order_date
CREATE TABLE mart.fct_orders (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT DISTKEY,
    order_date DATE SORTKEY,
    ...
) DISTSTYLE KEY;

-- fct_order_lines: Distribute by order_id (co-locate with fct_orders)
CREATE TABLE mart.fct_order_lines (
    line_item_id BIGINT PRIMARY KEY,
    order_id BIGINT DISTKEY,
    sku VARCHAR(50),
    ...
) DISTSTYLE KEY;
```

#### Transformation Layer: dbt Core

**dbt Project Structure**:
```
dbt_project/
├── models/
│   ├── staging/           # 1:1 with source tables, light transformations
│   │   ├── stg_orders.sql
│   │   ├── stg_customers.sql
│   │   └── stg_products.sql
│   ├── intermediate/      # Business logic, joins, calculations
│   │   ├── int_customer_orders.sql
│   │   └── int_product_returns.sql
│   └── marts/            # Final fact/dimension tables
│       ├── fct_orders.sql
│       ├── dim_customers.sql
│       └── mrt_inventory_daily.sql
├── tests/                # Data quality tests
│   └── assert_revenue_positive.sql
├── macros/               # Reusable SQL macros
│   └── generate_date_spine.sql
└── dbt_project.yml       # Config: materializations, vars
```

**Incremental Models** (large tables):
```sql
-- models/marts/fct_orders.sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    sort='order_date',
    dist='customer_id'
) }}

SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    ...
FROM {{ ref('stg_orders') }}
{% if is_incremental() %}
WHERE order_date > (SELECT MAX(order_date) FROM {{ this }})
{% endif %}
```

#### Consumption Layer

**Tableau Cloud** ($70/user/month × 100 users = $7,000/month, negotiated to $2,000/month for Creator licenses):
- 20 operational dashboards: inventory, orders, marketing, sales
- Live Redshift connection (not extract): Always fresh data
- Row-level security: Filter data by user role (operations see only their warehouse)
- Mobile app: Executives access KPI dashboards on iPad

**Metabase Open-Source** (self-hosted on EC2 t3.medium, $50/month):
- Ad-hoc SQL editor for 15 power users (analysts, data engineers)
- Simple dashboards for non-critical use cases
- Lower cost alternative to additional Tableau Creator licenses

**AWS QuickSight** (deferred to Phase 2):
- Future: Embedded analytics for B2B customers (show order history, account analytics)
- Pay-per-session pricing attractive for external users

#### Orchestration: Amazon MWAA (Managed Airflow)

**Cost**: $500/month (mw1.small environment)

**DAGs** (Directed Acyclic Graphs):

**1. nightly_etl** (runs 12:00 AM EST):
```python
nightly_etl = DAG(
    dag_id='nightly_etl',
    schedule_interval='0 0 * * *',  # Midnight daily
    catchup=False
)

# Step 1: Wait for Fivetran syncs to complete
wait_fivetran = FivetranOperator(...)

# Step 2: Run dbt models (staging → marts)
dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='dbt run --models +marts'
)

# Step 3: Run dbt tests (data quality)
dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command='dbt test'
)

# Step 4: Refresh materialized views
refresh_metrics = PostgresOperator(
    task_id='refresh_metrics',
    sql='REFRESH MATERIALIZED VIEW metrics.daily_revenue'
)

wait_fivetran >> dbt_run >> dbt_test >> refresh_metrics
```

**2. hourly_dashboard_refresh** (runs 6 AM - 8 PM, hourly):
- Refresh materialized views for real-time dashboards
- Faster than full dbt run (5 minutes vs 2 hours)

### Architecture Decisions

#### ELT vs ETL

**Decision**: ELT (Extract-Load-Transform) approach

**Rationale**:
- **Redshift compute power**: Transform in-warehouse using SQL/dbt leverages Redshift's MPP architecture
- **Team expertise**: Data analysts proficient in SQL can own transformations (no Python/Spark required)
- **Flexibility**: Raw data available in Redshift for ad-hoc analysis, reprocessing
- **Modern stack**: dbt is industry standard for SQL-based transformations

**Trade-off**: Slightly higher Redshift compute costs vs. pre-transforming in Glue (but lower overall complexity)

#### Single Warehouse vs Lakehouse

**Decision**: Single Redshift warehouse (not lakehouse)

**Rationale**:
- **Use case simplicity**: Operational reporting doesn't require ML/AI workloads (Databricks lakehouse overkill)
- **Team skills**: SQL-first team; Spark/Python not required
- **Cost-effectiveness**: Redshift Serverless cheaper than Databricks SQL + storage for this workload
- **Query performance**: Columnar Redshift storage optimized for aggregations

**Trade-off**: Less flexible for future ML/Python use cases (but can add Databricks later if needed)

#### Centralized vs Federated

**Decision**: Centralized warehouse

**Rationale**:
- **Single source of truth**: Consolidate 15 disparate systems into one analytics platform
- **Simplified governance**: Central access control, audit logging, cost management
- **Team size**: Single data engineer can manage one platform (federated requires coordination)

**Trade-off**: Data duplication (RDS + Redshift), but storage costs low ($23/TB)

#### Real-Time vs Batch

**Decision**: Batch-first (daily loads), with opt-in hourly refresh for critical dashboards

**Rationale**:
- **Business requirements**: 24-hour data freshness acceptable for 95% of use cases
- **Cost optimization**: Batch loads cheaper than continuous streaming (no Kinesis streaming costs)
- **Simplicity**: Daily ETL windows easier to monitor, debug, replay than real-time streams

**Future**: Add real-time for web analytics if sub-minute freshness becomes requirement

### Scalability Considerations

**Data Volume Growth** (25% annually):
- **Year 1**: 50TB → Redshift handles easily with 32 RPUs base
- **Year 3**: 97TB → Scale to 64 RPUs base, still well within Redshift Serverless limits
- **Year 5**: 152TB → Consider RA3 clusters with managed storage (2.56PB max capacity)

**Concurrency Growth**:
- **Current**: 100 users → Workload management queues handle easily
- **Future (300 users)**: Enable multi-cluster warehouses or migrate to larger RPU base (64-128 RPUs)

**Query Performance Optimization**:
- **Phase 1** (Months 1-3): Basic distribution/sort keys, ANALYZE statistics
- **Phase 2** (Months 4-6): Materialized views for slow dashboards, result caching
- **Phase 3** (Months 7-12): Advanced tuning (DISTKEY optimization, VACUUM schedules, concolic join optimization)

**Cost Optimization Strategies**:
- **Auto-suspend**: Redshift Serverless auto-pauses during off-hours (8 PM - 8 AM = 12 hours saved daily)
- **Query result caching**: Eliminate redundant queries (dashboards auto-refresh every 15 minutes)
- **Redshift Spectrum**: Move cold data (>2 years old) to S3, query via Spectrum (save on managed storage)
- **Reserved capacity**: After 6 months production, commit to 1-year reserved RPUs (20% discount)

---

## 5. Implementation Guide

### Phase 1: Foundation (Weeks 1-2)

**Goal**: Working proof-of-concept with first data source and query

**Week 1: Infrastructure Setup**
- **Day 1-2**: Provision Redshift Serverless
  ```bash
  aws redshift-serverless create-namespace \
      --namespace-name ecommerce-analytics \
      --admin-username admin \
      --admin-user-password <secure-password>

  aws redshift-serverless create-workgroup \
      --workgroup-name production \
      --namespace-name ecommerce-analytics \
      --base-capacity 32 \
      --publicly-accessible false \
      --subnet-ids subnet-abc123 subnet-def456
  ```
- **Day 3**: Configure VPC security groups (allow traffic from BI tools, Airflow, analysts' IPs)
- **Day 4**: Set up IAM roles for Redshift → S3 access (read S3 data, write query results)
- **Day 5**: Install Redshift Query Editor v2, run first query (`SELECT 1;`)

**Week 2: First Data Source**
- **Day 6-7**: Set up AWS DMS task for PostgreSQL RDS → S3 (full load + CDC)
- **Day 8**: Create `raw.orders_staged` table in Redshift, run first COPY command
  ```sql
  COPY raw.orders_staged
  FROM 's3://company-data-lake/dms/orders/'
  IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftS3Access'
  FORMAT AS PARQUET;
  ```
- **Day 9**: Write first dbt staging model (`stg_orders.sql`), run `dbt run`
- **Day 10**: Connect Tableau to Redshift, build simple dashboard (daily order counts)

**Deliverable**: Working proof-of-concept (Postgres → Redshift → Tableau dashboard)

---

### Phase 2: Core Implementation (Weeks 3-6)

**Goal**: MVP analytics platform with critical dashboards

**Week 3: ETL Pipeline Expansion**
- Set up Fivetran account, connect NetSuite, Stripe, Zendesk (3 sources)
- Configure Fivetran destination: Redshift Serverless
- Run initial sync (historical backfill), validate data quality
- Set up Airbyte for ShipStation API (custom connector)

**Week 4: Data Modeling**
- Expand dbt project: 15 staging models (one per source table)
- Build intermediate models: `int_customer_orders`, `int_product_inventory`
- Create mart models: `fct_orders`, `fct_order_lines`, `dim_customers`, `dim_products`
- Implement distribution/sort keys for performance
- Run full dbt pipeline: `dbt run --full-refresh`

**Week 5: Orchestration + Automation**
- Set up Amazon MWAA (Managed Airflow), install Airflow DAGs
- Create `nightly_etl` DAG: Fivetran sync → dbt run → tests
- Schedule DAG: Midnight EST, Slack alerts on failure
- Test end-to-end: Trigger manual DAG run, validate data freshness

**Week 6: Dashboard Development**
- Build 5 core operational dashboards in Tableau:
  1. **Daily Operations Dashboard**: Orders by hour, fulfillment rates, shipping exceptions
  2. **Inventory Dashboard**: Stock levels by warehouse, reorder alerts, SKU velocity
  3. **Marketing Dashboard**: Campaign performance, CAC by channel, ROAS
  4. **Executive KPIs**: Revenue, YoY growth, top products, customer cohorts
  5. **Supply Chain Dashboard**: Delivery times by carrier, return rates, supplier performance
- Configure row-level security (operations see only their warehouse data)
- User acceptance testing with 10 pilot users (operations, marketing)

**Deliverable**: MVP analytics platform with 5 dashboards, 100 users onboarded

---

### Phase 3: Production Rollout (Weeks 7-10)

**Goal**: Production-ready system with monitoring, documentation, training

**Week 7: Remaining Data Sources**
- Connect remaining 7 sources: Google Analytics 4, Facebook Ads, Google Ads, Amazon Ads, legacy MySQL
- Expand dbt models to cover all 15 sources
- Build remaining dashboards (10 additional dashboards for sales, finance teams)

**Week 8: Performance Optimization**
- Analyze slow queries via Redshift Query History (`STL_QUERY`, `SVL_QUERY_SUMMARY`)
- Create materialized views for expensive aggregations:
  ```sql
  CREATE MATERIALIZED VIEW metrics.daily_revenue AS
  SELECT
      order_date,
      SUM(total_amount) AS revenue
  FROM mart.fct_orders
  GROUP BY order_date;
  ```
- Tune distribution keys (use `EXPLAIN` to identify data shuffle)
- Set up query result caching (enable in workgroup settings)

**Week 9: Monitoring + Alerting**
- Configure CloudWatch dashboards: RPU utilization, query latency P95, storage growth
- Set up CloudWatch alarms: RPU utilization >80% (alert to scale up), ETL failures
- Implement dbt data quality tests: Not-null constraints, uniqueness, referential integrity
- Set up Slack integration: Pipeline failures, test failures, query timeouts

**Week 10: Training + Documentation**
- **User training** (2 sessions):
  - Session 1: Operations/marketing teams (dashboard usage, filters, drill-downs)
  - Session 2: Analysts (SQL editor, ad-hoc queries, Redshift Query Editor v2)
- **Documentation**:
  - Data dictionary: Table definitions, column descriptions, business logic
  - dbt docs: Generate with `dbt docs generate`, host on S3 static site
  - Runbooks: ETL troubleshooting, query optimization guide, incident response
- **Handoff**: Transition from contractor to internal data engineer

**Deliverable**: Production-ready system with 20 dashboards, 100 trained users, full documentation

---

### Phase 4: Iteration (Ongoing)

**Months 4-6**:
- Add new data sources as business expands (new ad platforms, international payment processors)
- Build advanced analytics: Cohort analysis, customer segmentation, demand forecasting
- Optimize costs: Reserved capacity commitments (1-year, 20% discount)
- Implement row-level security for sensitive data (PII masking for non-privileged users)

**Months 7-12**:
- Implement Redshift Spectrum: Move 3+ year old data to S3, query without loading
- Add reverse ETL: Sync Redshift → Salesforce (customer LTV scores), HubSpot (marketing segments)
- Explore ML: Redshift ML for demand forecasting, churn prediction (integrate with SageMaker)
- Governance: Implement data catalog (AWS Glue Catalog), lineage tracking (third-party tool)

### Team Requirements

**Data Engineer (1 FTE)**:
- **Responsibilities**: ETL pipeline maintenance, Redshift optimization, dbt model development
- **Time commitment**: Full-time (40 hours/week)
- **Skills required**: SQL (expert), Postgres (proficient), AWS (intermediate), dbt (intermediate), Python (basic for Airflow/scripting)

**BI Analyst (2 FTE)**:
- **Responsibilities**: Dashboard development, user training, ad-hoc analysis, stakeholder support
- **Time commitment**: Full-time (80 hours/week combined)
- **Skills required**: SQL (proficient), Tableau (expert), business domain knowledge (e-commerce, operations, marketing)

**Analytics Engineer (0.5 FTE, contract)**:
- **Responsibilities**: dbt architecture, data modeling best practices, code reviews, training
- **Time commitment**: Part-time (20 hours/week, Months 1-3; 5 hours/week ongoing)
- **Skills required**: dbt (expert), SQL (expert), data modeling (expert), Python (proficient)

### Tools & Costs

**Monthly Cost Breakdown**:

| Category | Tool | Cost | Notes |
|----------|------|------|-------|
| **Warehouse** | Redshift Serverless | $7,500 | 32 RPUs base, 50% avg utilization |
| **ETL** | Fivetran | $3,000 | 500M rows/month, 10 SaaS connectors |
| **ETL** | AWS DMS | $150 | t3.large replication instance |
| **ETL** | AWS Glue | $500 | 100 DPU-hours/month |
| **ETL** | Airbyte (self-hosted) | $100 | EC2 t3.large |
| **BI Tool** | Tableau Cloud | $2,000 | 100 users (negotiated rate) |
| **BI Tool** | Metabase (self-hosted) | $50 | EC2 t3.medium |
| **Orchestration** | Amazon MWAA | $500 | mw1.small environment |
| **dbt** | dbt Core (open-source) | $0 | Self-hosted via Airflow |
| **Infrastructure** | EC2, S3, CloudWatch | $800 | Misc infrastructure costs |
| **Support** | AWS Business Support | $400 | 7% of AWS usage, ~$5,700/month |
| **Total** | | **$15,000** | Within budget ceiling |

**3-Year TCO**: $540,000 total ($15K/month × 36 months)

**Cost Breakdown**:
- Warehouse: 50% ($270K)
- ETL tools: 30% ($162K)
- BI tools: 10% ($54K)
- Infrastructure: 10% ($54K)

---

## 6. Cost Breakdown

### Year 1 Costs

**Setup Costs (One-Time)**:

| Item | Cost | Notes |
|------|------|-------|
| Redshift Serverless provisioning | $0 | No upfront costs |
| Fivetran onboarding + setup | $1,000 | Professional services (optional) |
| Tableau deployment | $500 | Initial configuration, training |
| Contractor (Analytics Engineer) | $15,000 | 3 months @ $5K/month, dbt setup |
| **Total Setup** | **$16,500** | One-time, Month 1 |

**Monthly Recurring Costs (Months 1-12)**:

| Category | Item | Monthly Cost | Annual Cost |
|----------|------|--------------|-------------|
| **Warehouse** | Redshift Serverless (32 RPUs, 50% util) | $7,500 | $90,000 |
| **ETL** | Fivetran (500M rows, 10 sources) | $3,000 | $36,000 |
| **ETL** | AWS DMS (t3.large replication) | $150 | $1,800 |
| **ETL** | AWS Glue (100 DPU-hours) | $500 | $6,000 |
| **ETL** | Airbyte (self-hosted EC2) | $100 | $1,200 |
| **BI** | Tableau Cloud (100 users) | $2,000 | $24,000 |
| **BI** | Metabase (self-hosted EC2) | $50 | $600 |
| **Orchestration** | Amazon MWAA (mw1.small) | $500 | $6,000 |
| **dbt** | dbt Core (open-source) | $0 | $0 |
| **Infrastructure** | S3, EC2, CloudWatch, VPC | $800 | $9,600 |
| **Support** | AWS Business Support (7%) | $400 | $4,800 |
| **Total Recurring** | | **$15,000** | **$180,000** |

**Year 1 Total**: $16,500 (setup) + $180,000 (recurring) = **$196,500**

---

### 3-Year TCO Projection

**Assumptions**:
- **Data growth**: 25% annually (50TB → 62.5TB → 78TB)
- **Query volume growth**: 20% annually (follows user growth)
- **Tool costs**: 5% annual inflation (Fivetran, Tableau pricing increases)
- **Reserved capacity**: Year 2 commit to 1-year Redshift reserved (20% discount)

| Year | Warehouse | ETL Tools | BI Tools | Infrastructure | Support | **Annual Total** |
|------|-----------|-----------|----------|----------------|---------|------------------|
| **Year 1** | $90,000 | $45,000 | $24,600 | $9,600 | $4,800 | **$180,000** |
| **Year 2** | $86,400 (reserved) | $51,300 (+14% growth) | $25,800 | $10,800 | $5,200 | **$186,500** |
| **Year 3** | $103,680 (28% growth) | $58,500 | $27,100 | $12,200 | $6,020 | **$214,500** |
| **Total 3-Year** | $280,080 | $154,800 | $77,500 | $32,600 | $16,020 | **$581,000** |

**3-Year TCO**: $581,000 ($16,166/month average)

**Note**: Includes $16.5K Year 1 setup costs in total. Monthly average exceeds $15K budget by ~$1,166/month (8% overage) due to data growth in Year 3. Acceptable given 25% data growth and reserved capacity discounts.

---

### Cost Optimization Strategies

**Quick Wins (Months 1-3)**:

1. **Redshift auto-suspend** (save $3,600/month):
   - Auto-pause Serverless during off-hours (8 PM - 8 AM = 12 hours/day)
   - Expected savings: 50% of idle hours = 12 hours × 32 RPUs × $3/hour = $1,152/day → $3,600/month saved

2. **Query result caching** (save $800/month):
   - Enable result cache (24-hour retention) for dashboard queries
   - Estimated 20% of queries are duplicates (auto-refresh dashboards)
   - Savings: 20% of compute costs = $1,500 × 0.2 = $300/month
   - Materialized views: Pre-aggregate dashboard metrics (save $500/month on repeated aggregations)

3. **Partition pruning** (save $400/month):
   - Partition large tables by date (fct_orders, fct_web_sessions)
   - Reduce scanned data by 60% for date-filtered queries
   - Savings: $7,500 × 0.05 (5% compute reduction) = $375/month

**Total Quick Wins**: $4,800/month savings → Effective cost $10,200/month (32% under budget)

---

**Medium-Term Optimizations (Months 4-12)**:

1. **Reserved capacity** (save $1,350/month):
   - Commit to 1-year Redshift Serverless reserved capacity (20% discount)
   - Baseline usage: 32 RPUs × 730 hours × $3/hour = $70,080/month
   - Reserved pricing: $70,080 × 0.8 = $56,064/month
   - Savings: $14,016/year = $1,168/month

2. **Redshift Spectrum for cold data** (save $600/month):
   - Move 3+ year old data (20% of 50TB = 10TB) to S3 ($23/TB = $230/month)
   - Query via Spectrum (pay-per-query: $5/TB scanned, minimal usage)
   - Savings: Redshift managed storage ($600/month) - S3 ($230/month) = $370/month net savings

3. **VACUUM and ANALYZE optimization** (save $300/month):
   - Schedule weekly VACUUM FULL (reclaim space, improve compression)
   - Daily ANALYZE (update statistics, improve query plans)
   - Savings: 5% query performance improvement = $7,500 × 0.05 = $375/month

**Total Medium-Term**: $2,268/month additional savings

---

**Long-Term Optimizations (Year 2-3)**:

1. **Fivetran optimization** (save $1,000/month):
   - Audit connectors: Reduce sync frequency for low-priority sources (daily → weekly)
   - Schema exclusions: Exclude unused tables (reduce rows synced by 30%)
   - Savings: $3,000 × 0.33 = $1,000/month

2. **Self-hosted dbt Cloud alternative** (save $0, already using open-source):
   - Already using dbt Core (free) via Airflow
   - If considering dbt Cloud ($100/seat × 5 seats = $500/month), stick with open-source

3. **BI tool consolidation** (save $500/month):
   - Consolidate Tableau + Metabase → Single tool if usage overlaps
   - Alternatively: Replace Tableau with open-source alternatives (Apache Superset) for non-critical dashboards

**Total Long-Term**: $1,500/month additional savings

---

### Cost Comparison: Winner vs Runner-Up

**Redshift vs Snowflake (Apples-to-Apples)**:

| Cost Category | Redshift | Snowflake | Difference |
|---------------|----------|-----------|------------|
| **Warehouse (Year 1)** | $90,000 | $145,200 | +$55,200 (61% more) |
| **ETL Tools** | $45,000 | $45,000 | Same |
| **BI Tools** | $24,600 | $24,600 | Same |
| **Infrastructure** | $9,600 | $12,000 | +$2,400 (VPC PrivateLink) |
| **Support** | $4,800 | $7,200 | +$2,400 (higher base) |
| **Year 1 Total** | $180,000 | $241,000 | **+$61,000 (34% more)** |
| **3-Year Total** | $581,000 | $824,000 | **+$243,000 (42% more)** |

**Break-Even Analysis**:
- Snowflake becomes cost-competitive if:
  - Budget increases to $20K/month (premium features justify cost)
  - Multi-cloud strategy requires GCP/Azure (Redshift AWS-only)
  - Data sharing becomes strategic (Snowflake zero-copy sharing superior)

**Winner: Redshift saves $243,000 over 3 years (42% lower TCO)**

---

## 7. Migration & Onboarding

### Current State Assessment

**Existing Reporting Landscape**:
- **Excel-based reports**: 20+ spreadsheets maintained manually by analysts
  - Daily operations report: 15 hours/week to compile (export from 6 systems → pivot tables → email)
  - Weekly executive dashboard: 8 hours to prepare (manual SQL queries → Excel charts → PowerPoint)
  - Monthly marketing attribution: 20 hours (export ad platform CSVs → manual joins → attribution model in Excel)
- **Ad-hoc SQL queries**: Analysts run queries directly on production PostgreSQL RDS (performance impact on transactional workload)
- **No single source of truth**: Finance uses NetSuite data, Operations uses ShipStation, Marketing uses Google Analytics—numbers don't reconcile

**Pain Points**:
- **Data staleness**: Most reports use 5-day old data (manual exports run weekly)
- **Manual errors**: Copy-paste errors in Excel lead to incorrect metrics (happened 3 times in Q4)
- **Performance impact**: Heavy analytical queries slow down production database (customer-facing impact)
- **Lack of self-service**: Analysts wait 2-3 days for data engineer to export data

### Migration Complexity: Medium (Net-New Implementation)

**Migration Type**: Net-new implementation (not replacing existing warehouse)
- **No legacy warehouse**: No data migration required (building first analytics platform)
- **Lift-and-shift**: Extract data from operational systems → Load into Redshift (one-time backfill)
- **Parallel run**: Run Excel reports + Redshift dashboards in parallel for 4 weeks (validate data accuracy)

**Complexity Drivers**:
- **Data source diversity**: 15 distinct systems (each requires custom connector/ETL logic)
- **Data quality issues**: Discovered during POC—NetSuite has duplicate records, Stripe timestamps in UTC vs EST
- **Business logic reconstruction**: Excel formulas contain undocumented business logic (must reverse-engineer)

### Migration Steps

**Phase 1: Discovery + Planning (Week 1-2)**:
- Audit existing reports: Document all Excel reports, SQL queries, business logic
- Interview stakeholders: Understand requirements, priorities, pain points
- Data profiling: Analyze source systems for data quality issues (nulls, duplicates, outliers)
- Define success criteria: Which reports must match Excel exactly? Which can be redefined?

**Phase 2: POC (Week 3-4)**:
- Build POC: Connect Postgres RDS → Redshift, recreate 1 critical report (daily inventory)
- Validate data accuracy: Compare Redshift query results vs Excel report (row-by-row)
- Identify gaps: Document discrepancies, resolve business logic misunderstandings
- Stakeholder demo: Show POC dashboard to operations team, gather feedback

**Phase 3: Parallel Run (Week 5-8)**:
- Build 5 core dashboards in Redshift (operations, marketing, executive KPIs)
- Run in parallel with Excel reports: Analysts maintain both systems for 4 weeks
- Data validation: Compare Redshift vs Excel daily—investigate any discrepancies >1%
- Iterative refinement: Fix bugs, adjust business logic, optimize query performance

**Phase 4: Cutover (Week 9)**:
- **Go/No-Go decision**: Review data accuracy, performance, user feedback
- **Cutover**: Deprecate Excel reports, Redshift becomes single source of truth
- **Monitoring**: Closely monitor first week—address any issues immediately
- **Celebrate**: Announce success to company, highlight time savings (15 hours/week → 2 hours/week)

**Phase 5: Deprecation (Week 10-12)**:
- Archive Excel reports: Move to shared drive (read-only for audit trail)
- Update documentation: Redirect all wiki links to Redshift dashboards
- Decommission ad-hoc access: Revoke analyst access to production Postgres (force migration to Redshift)

### Estimated Timeline: 10 Weeks (POC → Production)

**Timeline Breakdown**:
- Weeks 1-2: Discovery + planning
- Weeks 3-4: POC development
- Weeks 5-8: Parallel run + validation
- Weeks 9-10: Cutover + stabilization

**Critical Path**:
- Data quality issues (discovered in Week 3) add 1-2 weeks to timeline
- Stakeholder alignment (CFO insists on exact Excel match) requires additional validation

### Onboarding Plan

**User Segmentation**:

**1. Power Users (5 users: Data engineer, 2 BI analysts, 2 senior analysts)**:
- **Training**: 4-hour workshop on Redshift SQL, query optimization, Tableau development
- **Access**: Full read access to all schemas, write access to sandbox schema
- **Support**: 1:1 onboarding sessions, Slack channel for questions

**2. Dashboard Users (80 users: Operations, marketing, sales, supply chain)**:
- **Training**: 1-hour webinar on dashboard usage (filters, drill-downs, exporting)
- **Access**: View-only access to dashboards (row-level security applied)
- **Support**: Email support, recorded training videos

**3. Executives (10 users: CEO, CFO, VPs)**:
- **Training**: 30-minute 1:1 walkthrough of executive KPI dashboard
- **Access**: View-only access to executive dashboards, mobile app setup
- **Support**: Dedicated BI analyst for ad-hoc requests

**4. Analysts (5 users: Marketing analysts, operations analysts)**:
- **Training**: 2-hour workshop on Redshift Query Editor v2, writing SQL, ad-hoc analysis
- **Access**: Read access to marts schema, Metabase SQL editor
- **Support**: Office hours (Tuesdays 2-3 PM) for SQL help

### Change Management Approach

**Communication Strategy**:
- **Week 1**: Announce project kickoff—CEO email highlighting benefits (faster insights, time savings)
- **Week 4**: POC demo video—show operations dashboard, invite feedback
- **Week 8**: Pre-launch announcement—training schedule, cutover date, support resources
- **Week 9**: Go-live announcement—celebrate launch, highlight success metrics
- **Week 12**: Retrospective—share lessons learned, acknowledge contributors

**Incentives**:
- **Gamification**: Award "Data Champion" badges to early adopters who complete training
- **Time savings**: Highlight analyst time saved (15 hours/week = 60 hours/month = $3,000 cost savings)
- **Executive sponsorship**: CFO champions project, attends training sessions, uses dashboards in board meetings

### Training Program

**Training Materials**:
- **Video tutorials** (10 videos, 5-10 minutes each):
  - Dashboard navigation basics
  - Applying filters and drill-downs
  - Exporting data to Excel
  - Writing SQL queries in Redshift
  - Understanding data freshness (last updated timestamp)
- **Documentation**:
  - Data dictionary (table definitions, column descriptions)
  - FAQ (common questions, troubleshooting)
  - Quick reference guide (PDF cheat sheet)
- **Office hours**: Weekly 1-hour sessions (Tuesdays 2-3 PM) for live Q&A

**Training Schedule**:
- Week 6: Power user training (4 hours, in-person)
- Week 7: Dashboard user webinar (1 hour, virtual, 2 sessions to accommodate timezones)
- Week 8: Executive 1:1s (30 minutes each, in-person)
- Week 9: Analyst workshop (2 hours, in-person)

### Success Metrics

**30-Day Metrics** (Post-Launch):
- ✅ 80% of users complete training (target: 80/100 users)
- ✅ 5 core dashboards live and used daily (operations, marketing, executive KPIs)
- ✅ Average query response time <5 seconds (P95 latency)
- ✅ Zero critical bugs (dashboard data incorrect)

**90-Day Metrics**:
- ✅ 100% of Excel reports deprecated (all reporting moved to Redshift)
- ✅ Analyst time saved: 15 hours/week → 2 hours/week (87% reduction)
- ✅ Data freshness: 5-day lag → 24-hour lag (80% improvement)
- ✅ User satisfaction: 4.2/5 average rating (user survey)

**12-Month Metrics**:
- ✅ 20 dashboards live (5 initial + 15 new use cases)
- ✅ 100 active users (95% adoption rate)
- ✅ Self-service analytics: 60% of queries run by analysts (no data engineer involvement)
- ✅ ROI demonstration: $200K cost savings (analyst time + faster decision-making) vs $196K investment

### Common Pitfalls

**Pitfall 1: Data Quality Issues Discovered Late**:
- **Scenario**: Week 6 parallel run reveals 15% revenue discrepancy between Excel and Redshift
- **Root cause**: Excel report applies manual adjustments (refunds deducted) not documented anywhere
- **Prevention**: Week 1 discovery phase—document all business logic, compare sample calculations
- **Mitigation**: Add dbt tests for data quality (revenue matches expected range), manual validation process

**Pitfall 2: Performance Issues During Peak Hours**:
- **Scenario**: Week 9 go-live—dashboards time out during peak hours (50 concurrent users)
- **Root cause**: Underestimated concurrency, 32 RPUs insufficient for 50 users
- **Prevention**: Load testing in Week 7 (simulate 50 concurrent dashboard refreshes)
- **Mitigation**: Auto-scale to 64 RPUs during peak hours (9-11 AM), materialized views for slow dashboards

**Pitfall 3: Stakeholder Resistance to Change**:
- **Scenario**: Operations manager refuses to adopt Redshift—insists Excel reports more accurate
- **Root cause**: Fear of change, lack of trust in new system
- **Prevention**: Involve stakeholders in POC (Week 3-4), show side-by-side comparison
- **Mitigation**: 4-week parallel run builds trust, CFO executive sponsorship mandates adoption

---

## 8. Risks & Mitigations

### Technical Risks

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **Query performance degradation** (dashboards >5s) | Medium | High | - Materialized views for slow aggregations<br>- Distribution/sort key optimization<br>- Auto-scale RPUs during peak hours<br>- Query result caching (24-hour retention) |
| **Cost overruns** (exceed $15K/month budget) | Medium | High | - Reserved capacity commitment (20% discount)<br>- Auto-suspend during off-hours (save $3.6K/month)<br>- Query monitoring (kill expensive queries)<br>- Monthly cost reviews, CloudWatch budget alarms |
| **ETL pipeline failures** (missing daily data loads) | Low | High | - Redundant pipelines (Fivetran + Airbyte backups)<br>- Airflow retry logic (3 retries with exponential backoff)<br>- Slack alerts on failure (page on-call engineer)<br>- Runbook for common failures (Fivetran sync stuck) |
| **Data quality issues** (incorrect dashboard metrics) | Medium | Critical | - dbt data quality tests (not_null, unique, relationships)<br>- Automated anomaly detection (revenue >50% change alerts)<br>- Parallel run validation (4 weeks Excel vs Redshift)<br>- Manual spot checks (CFO reviews daily revenue) |
| **Postgres RDS performance impact** (CDC load) | Low | Medium | - AWS DMS uses WAL (minimal CPU impact <5%)<br>- Schedule heavy exports during off-hours (2-6 AM)<br>- Monitor RDS CloudWatch (CPU, IOPS, connections) |
| **Redshift Serverless capacity limits** (RPU exhaustion) | Low | Medium | - Auto-scale to 128 RPUs (4x base capacity)<br>- Workload management (prioritize dashboards over batch)<br>- Query timeout limits (kill runaway queries after 30 min) |

### Business Risks

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **Vendor lock-in** (Redshift AWS-only) | High | Medium | - Use dbt for transformations (portable SQL)<br>- Store raw data in S3 (can migrate to other warehouses)<br>- Document business logic (enable future migration)<br>- Accept risk: AWS commitment already made (EC2, RDS, S3) |
| **Team capacity** (1 data engineer insufficient) | Medium | High | - Hire second data engineer by Month 6<br>- Engage analytics engineer contractor (dbt expertise)<br>- Self-service BI (reduce ad-hoc data requests)<br>- Prioritize ruthlessly (focus on top 5 dashboards) |
| **Scope creep** (150 dashboard requests) | High | Medium | - Phased approach (5 dashboards → 20 → 50 over 12 months)<br>- Product management mindset (prioritize by ROI)<br>- User training (enable self-service, reduce requests)<br>- Quarterly roadmap planning (stakeholder alignment) |
| **Stakeholder misalignment** (CFO vs CMO priorities) | Medium | Medium | - Executive steering committee (monthly meetings)<br>- Clear success metrics (align on KPIs upfront)<br>- Transparent roadmap (publish dashboard backlog)<br>- Quick wins (deliver operations dashboard in Week 6) |
| **Regulatory compliance failure** (PCI DSS audit) | Low | Critical | - Tokenize payment card data (Stripe handles PCI)<br>- Redshift encryption at rest/transit (AES-256, TLS 1.2)<br>- IAM-based access control (least privilege principle)<br>- Audit logging (CloudWatch Logs, 90-day retention) |
| **Budget cuts** (economic downturn, $15K → $10K) | Low | High | - ClickHouse Cloud alternative ($3.3K/month warehouse)<br>- Open-source BI tools (Metabase, Apache Superset)<br>- Reduce Fivetran sources (8 → 5 critical sources)<br>- Scale down Redshift (32 RPUs → 16 RPUs) |

### Mitigation Matrix (Prioritized)

**High Likelihood + High Impact** (Top Priority):

1. **Scope creep** + **Team capacity**:
   - **Mitigation**: Hire second data engineer by Month 6 ($120K salary), set clear quarterly roadmap with 5 dashboard limit per quarter
   - **Owner**: VP Engineering (hiring), Director of Analytics (roadmap prioritization)
   - **Timeline**: Month 6 hire, ongoing quarterly planning

**Medium Likelihood + High Impact**:

2. **Cost overruns**:
   - **Mitigation**: Reserved capacity commitment (Month 6), auto-suspend overnight, monthly cost reviews
   - **Owner**: Data engineer (monitoring), CFO (budget oversight)
   - **Timeline**: Immediate (auto-suspend), Month 6 (reserved capacity)

3. **Query performance degradation**:
   - **Mitigation**: Materialized views (Month 3), distribution key tuning (Month 4), auto-scaling (immediate)
   - **Owner**: Data engineer (optimization), BI analysts (identify slow dashboards)
   - **Timeline**: Ongoing optimization, immediate auto-scaling

4. **Data quality issues**:
   - **Mitigation**: dbt tests (Month 2), parallel run validation (Month 5-8), automated anomaly detection (Month 9)
   - **Owner**: Analytics engineer (dbt tests), CFO (manual spot checks)
   - **Timeline**: Month 2 (tests), Month 5-8 (validation)

**Medium/Low Likelihood + Critical Impact**:

5. **Regulatory compliance failure**:
   - **Mitigation**: PCI DSS self-assessment (Month 3), encryption audit (Month 6), annual penetration testing
   - **Owner**: Security team (assessment), data engineer (implementation)
   - **Timeline**: Month 3 (assessment), Month 6 (audit), annual testing

---

## 9. Success Metrics

### 30-Day Metrics (End of Month 1)

**Technical Metrics**:
- ✅ **First dashboard live**: Operations inventory dashboard deployed, used by 25 operations team members
- ✅ **10 queries running daily**: Automated dashboard refreshes + analyst ad-hoc queries
- ✅ **10 users onboarded**: Power users (data engineer, 2 BI analysts) + 7 pilot users (operations managers)
- ✅ **Sub-5 second dashboard load time**: P95 latency for operations dashboard <5 seconds
- ✅ **Zero critical bugs**: No data accuracy issues, no system downtime during business hours

**Business Metrics**:
- ✅ **5 hours/week time saved**: Operations team no longer manually exports inventory data (pilot only)
- ✅ **24-hour data freshness**: Inventory dashboard shows yesterday's data (down from 5-day lag)
- ✅ **1 data source connected**: PostgreSQL RDS → Redshift (first ETL pipeline live)

**Success Criteria**: All metrics green → Proceed to Phase 2 (expand to 15 data sources)

---

### 90-Day Metrics (End of Month 3)

**Technical Metrics**:
- ✅ **5 core dashboards live**: Operations, marketing, executive KPIs, supply chain, sales dashboards
- ✅ **15 data sources connected**: All 15 systems integrated (Postgres, NetSuite, Stripe, Ads APIs, etc.)
- ✅ **500 queries/day**: Dashboard refreshes (300) + analyst ad-hoc queries (200)
- ✅ **80 users onboarded**: Operations (25), marketing (15), sales (30), executives (10)
- ✅ **P95 query latency <5 seconds**: 95% of dashboard queries return within 5 seconds
- ✅ **99.5% uptime**: No unplanned downtime during business hours (8 AM - 8 PM EST)

**Business Metrics**:
- ✅ **All Excel reports migrated**: 20+ Excel reports deprecated, Redshift is single source of truth
- ✅ **15 hours/week → 2 hours/week**: 87% reduction in manual reporting time (analyst time saved)
- ✅ **Marketing attribution dashboard**: CMO can see ROI by channel with 24-hour freshness (previously monthly)
- ✅ **Cost within budget**: $13,500/month actual spend (10% under $15K budget, after auto-suspend optimization)

**ROI Calculation** (90 Days):
- **Cost**: $16,500 (setup) + $40,500 (3 months × $13.5K) = $57,000 total investment
- **Savings**: 13 hours/week × $75/hour × 13 weeks = $12,675 (analyst time saved)
- **Intangible**: Faster decision-making (CEO catches inventory stockout 3 days earlier, saves $50K lost sales)
- **Net**: ($57,000) + $12,675 + $50,000 = $5,675 positive ROI (break-even achieved)

**Success Criteria**: All metrics green → Proceed to Phase 4 (advanced analytics, ML)

---

### 12-Month Metrics (End of Year 1)

**Technical Metrics**:
- ✅ **20 dashboards live**: 5 core + 15 new dashboards (finance, HR, customer success, product analytics)
- ✅ **2,000 queries/day**: Dashboard refreshes (1,000) + analyst ad-hoc queries (1,000)
- ✅ **100 active users**: 95% adoption rate (100 of 105 total company employees use Redshift weekly)
- ✅ **Self-service analytics**: 60% of queries run by analysts (no data engineer involvement)
- ✅ **Advanced features enabled**: Redshift ML (demand forecasting), Spectrum (3-year old data in S3)

**Business Metrics**:
- ✅ **Data-driven decisions increase**: 80% of weekly executive meetings reference Redshift dashboards (up from 20% Excel reports)
- ✅ **Inventory optimization**: Stockouts reduced from 12% to 7% (demand forecasting model), overstock reduced from 22% to 15%
- ✅ **Marketing ROI clarity**: CMO reallocates $50K/month from low-ROI channels (Facebook) to high-ROI (Google Search), increasing ROAS from 3.2x to 4.1x
- ✅ **Operational efficiency**: Order fulfillment dashboard reduces fulfillment time from 36 hours to 24 hours (operations team catches bottlenecks faster)

**ROI Demonstration** (12 Months):
- **Cost**: $196,500 total investment (Year 1 setup + recurring)
- **Direct savings**:
  - Analyst time saved: 15 hours/week × 52 weeks × $75/hour = $58,500
  - Inventory optimization: $50K (reduced overstock carrying costs)
- **Revenue impact**:
  - Marketing reallocation: $50K/month × 12 months = $600K additional revenue
  - Faster fulfillment: 10% improvement in customer satisfaction → 5% reduction in churn → $120K revenue retention
- **Total benefit**: $58,500 + $50,000 + $600,000 + $120,000 = $828,500
- **Net ROI**: ($196,500 cost) + $828,500 benefit = **$632,000 net positive ROI** (4.2x return)

**Long-Term Vision** (Year 2-3):
- Expand to international markets (EU, APAC): Add region-specific dashboards, multi-currency support
- Real-time analytics: Integrate Kinesis → Redshift streaming for live web dashboards
- Customer-facing analytics: Embed QuickSight dashboards in B2B portal (show account health, order history)
- Advanced ML: Churn prediction, dynamic pricing, customer segmentation models

**Success Criteria**: ROI >3x → Board approves Year 2 budget expansion to $20K/month for advanced features

---

## Summary

Amazon Redshift emerges as the clear winner for this mid-market e-commerce scenario, scoring 147/160 on requirements fit. The platform's native AWS integration, Postgres SQL compatibility, and mature ecosystem align perfectly with the company's existing infrastructure and team expertise.

**Key Decision Factors**:
1. **AWS-native fit**: Seamless integration with RDS, S3, Glue, IAM eliminates 80% of integration complexity
2. **Cost-effectiveness**: $7,500/month warehouse cost leaves 50% budget headroom for ETL/BI tools
3. **Team expertise**: Postgres compatibility enables immediate productivity (zero reskilling required)
4. **Proven reliability**: 13+ years of e-commerce production deployments reduce implementation risk

**Alternative Considerations**:
- **Snowflake** becomes compelling if budget increases to $20K/month or multi-cloud strategy emerges
- **ClickHouse Cloud** offers 56% cost savings if budget drops below $10K/month and team has bandwidth for custom integration work

**Expected Outcomes**:
- 87% reduction in manual reporting time (15 hours → 2 hours weekly)
- 24-hour data freshness (down from 5-day lag)
- 4.2x ROI in Year 1 ($632K net benefit on $196K investment)
- Foundation for future innovation (real-time analytics, ML/AI, customer-facing dashboards)

This implementation delivers on the core business need—operational reporting at scale—while future-proofing for growth (25% annual data increase, 100+ concurrent users). The phased approach (POC → MVP → Production → Innovation) mitigates risk while demonstrating value early (Month 3 break-even).

---

**Document Status**: Complete
**Word Count**: 14,847 words
**Last Updated**: 2025-11-06
**Scenario**: E-commerce Reporting (Mid-Market, 50TB, $15K/month budget)
**Recommendation**: Amazon Redshift Serverless (Primary), Snowflake (Runner-Up), ClickHouse Cloud (Budget Alternative)
