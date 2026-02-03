# Data Warehouse & Analytics Databases: Business Explainer

**Audience**: CFOs, CTOs, product managers, data team leaders
**Reading time**: 10 minutes
**Purpose**: Understand what data warehouses are, when you need one, and how to choose

---

## What is a Data Warehouse?

A **data warehouse** is a specialized database optimized for **analytical queries** rather than transactional operations. Think of it as the difference between:

- **Regular database (OLTP)**: Handles your application's transactions (user signup, purchase order, inventory update) - optimized for writing and reading individual records quickly
- **Data warehouse (OLAP)**: Handles your analytics queries (monthly revenue by region, customer cohort analysis, 5-year sales trends) - optimized for reading and aggregating millions of records

### Real-World Analogy

**Regular database** = Bank teller
- Fast at processing individual transactions (deposit check, withdraw $50)
- Not efficient at answering "show me all transactions over $1,000 in the past 5 years across all branches"

**Data warehouse** = Research department
- Slow at individual transactions (not designed for this)
- Excellent at answering complex analytical questions across massive datasets

---

## When Do You Need a Data Warehouse?

### You DON'T need a data warehouse if:
- ✅ Your analytics queries run fast enough on your production database (<5 seconds)
- ✅ You have <100GB of data
- ✅ Your reporting needs are simple (dashboard with 5-10 metrics)
- ✅ You're okay with impacting production database performance during heavy reporting

### You DO need a data warehouse when:
- ❌ Analytics queries slow down your production database (affecting customer experience)
- ❌ You have 100GB-10TB+ of data across multiple sources
- ❌ You need to join data from multiple systems (Stripe + Salesforce + Google Analytics)
- ❌ Business users want self-service analytics (BI tools like Tableau, Looker, Power BI)
- ❌ You're running daily/hourly batch jobs to aggregate data
- ❌ Compliance requires historical data retention (7+ years)

### Common Trigger: The "BI Tool Crashing Production" Incident

**Scenario**: Marketing director runs a complex Tableau query ("show me customer lifetime value by acquisition channel for the past 3 years"). Query takes 15 minutes and locks up production database tables. Customer checkout page times out. Engineering gets paged.

**Solution**: Move analytics workload to data warehouse. Production database handles transactions. Data warehouse handles analytics. Problem solved.

---

## OLTP vs OLAP: What's the Difference?

| Dimension | OLTP (Production Database) | OLAP (Data Warehouse) |
|-----------|---------------------------|----------------------|
| **Purpose** | Transactional operations | Analytical queries |
| **Query pattern** | Read/write individual records | Read millions of records |
| **Storage format** | Row-based (fast for individual records) | Column-based (fast for aggregations) |
| **Example query** | `SELECT * FROM orders WHERE id = 12345` | `SELECT SUM(revenue) FROM orders WHERE year = 2024 GROUP BY month, region` |
| **Performance** | Milliseconds per query | Seconds to minutes per query |
| **Data volume** | Gigabytes to low terabytes | Terabytes to petabytes |
| **Schema** | Normalized (avoid duplication) | Denormalized (optimize for reads) |
| **Users** | Application code | Business analysts, BI tools |

---

## Key Concepts

### 1. Columnar Storage

Traditional databases store data **row-by-row** (good for reading entire records):
```
Row 1: [customer_id=123, name="Alice", revenue=5000, signup_date="2024-01-15"]
Row 2: [customer_id=456, name="Bob", revenue=3000, signup_date="2024-02-20"]
```

Data warehouses store data **column-by-column** (good for aggregations):
```
customer_id: [123, 456, ...]
name: ["Alice", "Bob", ...]
revenue: [5000, 3000, ...]  ← Can read ONLY this column for SUM(revenue)
signup_date: ["2024-01-15", "2024-02-20", ...]
```

**Why columnar is faster for analytics**: If you're calculating `SUM(revenue)`, you only read the revenue column, not all 4 columns. 4× less data to scan = 4× faster query.

### 2. Separation of Storage and Compute

Modern data warehouses (Snowflake, BigQuery) separate:
- **Storage**: Where your data lives (cheap, ~$23/TB/month)
- **Compute**: Processing power to run queries (expensive, ~$2-4/hour per cluster)

**Old model (pre-2015)**: Pay for fixed cluster (8 servers running 24/7 = $50K/month)
**New model (2015+)**: Pay only when running queries (8 hours of queries = $32/month)

**Cost optimization**: Pause compute when not querying. Storage stays active (data never goes away).

### 3. ETL vs ELT

**ETL (Extract, Transform, Load)** - Old way:
1. Extract data from source systems
2. Transform data on ETL server (clean, aggregate, join)
3. Load into data warehouse

**ELT (Extract, Load, Transform)** - Modern way:
1. Extract raw data from source systems
2. Load raw data into data warehouse immediately
3. Transform inside the data warehouse using SQL

**Why ELT won**: Data warehouses are now powerful enough to handle transformations. Faster time-to-insight (load raw data first, transform later).

### 4. Data Lake vs Data Warehouse vs Data Lakehouse

**Data Lake** (S3, Azure Blob Storage):
- Raw, unstructured data storage
- Cheap ($20/TB/month)
- Files (CSV, JSON, Parquet, video, images)
- No query engine built-in

**Data Warehouse** (Snowflake, BigQuery):
- Structured, queryable data
- Expensive ($50-200/TB/month including compute)
- Optimized for SQL queries
- Query engine included

**Data Lakehouse** (Databricks):
- Combines both approaches
- Raw data in object storage (cheap)
- Query engine on top (SQL + Python + Spark)
- Open formats (Iceberg, Delta Lake) reduce lock-in

---

## Pricing Models

### Consumption-Based (Snowflake, BigQuery)

Pay for:
1. **Storage**: $23-40/TB/month (how much data you store)
2. **Compute**: $2-4/hour per cluster (how many queries you run)

**Example cost**:
- 10TB data stored = $300/month
- 40 hours queries/month = $120/month
- **Total**: $420/month

**Pro**: Only pay for what you use
**Con**: Unpredictable costs (runaway query can cost $500)

### Reserved Capacity (Redshift, Synapse)

Pay for:
1. **Fixed cluster**: $1,000-10,000/month (always running)

**Example cost**:
- 4-node cluster = $5,000/month (regardless of usage)

**Pro**: Predictable costs
**Con**: Paying for idle capacity (cluster running 24/7 even if only used 2 hours/day)

---

## Platform Overview

### Snowflake
- **Best for**: General-purpose data warehousing, multi-cloud
- **Strengths**: Easiest to use, zero-maintenance, excellent concurrency
- **Pricing**: Consumption-based, ~$2/hour compute + $40/TB storage
- **Lock-in risk**: Medium (proprietary format, but Iceberg support coming)

### Google BigQuery
- **Best for**: Cost-conscious teams, Google Cloud ecosystem
- **Strengths**: Cheapest at scale, serverless, excellent for event data
- **Pricing**: Consumption-based, $6.25/TB scanned + $20/TB storage
- **Lock-in risk**: Medium (proprietary format, but easy to export)

### Amazon Redshift
- **Best for**: AWS-heavy companies, reserved capacity workloads
- **Strengths**: Deep AWS integration, mature ecosystem
- **Pricing**: Reserved capacity or serverless, ~$1,000+/month
- **Lock-in risk**: Low (standard Postgres wire protocol)

### Azure Synapse Analytics
- **Best for**: Microsoft ecosystem, Power BI integration
- **Strengths**: Integrated with Azure services, hybrid analytics
- **Pricing**: Consumption or reserved, similar to Redshift
- **Lock-in risk**: Medium

### Databricks Lakehouse
- **Best for**: ML/AI workloads, data science teams, unifying lake + warehouse
- **Strengths**: Python + SQL, Delta Lake (open format), great for ML feature stores
- **Pricing**: Consumption-based, ~$0.22-0.55/DBU (Databricks Unit)
- **Lock-in risk**: Low (open Delta Lake format)

### ClickHouse (Open Source + Cloud)
- **Best for**: Real-time analytics, high-performance use cases
- **Strengths**: Fastest queries, open source, low cost
- **Pricing**: Self-hosted free, cloud ~$0.30/hour + storage
- **Lock-in risk**: Very low (open source)

### Apache Druid
- **Best for**: Real-time dashboards, time-series data, high-concurrency
- **Strengths**: Sub-second query latency, excellent for user-facing analytics
- **Pricing**: Self-hosted free, managed offerings available
- **Lock-in risk**: Very low (open source)

---

## Decision Framework

### Question 1: How much data do you have?

- **<100GB**: Stay on production database (add read replica for analytics)
- **100GB-1TB**: Start exploring data warehouse (BigQuery or ClickHouse for cost)
- **1TB-10TB**: Definitely need data warehouse (Snowflake or BigQuery)
- **10TB+**: Enterprise data warehouse (Snowflake, BigQuery, or Redshift)

### Question 2: What's your query pattern?

- **Daily batch reports**: Redshift reserved capacity (cheaper for predictable workloads)
- **Ad-hoc analytics**: Snowflake or BigQuery (pay only when querying)
- **Real-time dashboards**: ClickHouse or Druid (sub-second latency)
- **ML feature store**: Databricks (Python + SQL integration)

### Question 3: What's your cloud provider?

- **AWS**: Redshift (deep integration) or Snowflake (if multi-cloud)
- **Google Cloud**: BigQuery (no-brainer, best economics)
- **Azure**: Synapse (Power BI integration) or Snowflake
- **Multi-cloud**: Snowflake (works everywhere)
- **No preference**: BigQuery (cheapest) or Snowflake (easiest)

### Question 4: What's your budget?

- **<$500/month**: ClickHouse Cloud or BigQuery (most cost-effective)
- **$500-5K/month**: Snowflake or BigQuery (standard choice)
- **$5K-50K/month**: Any platform (enterprise tier)
- **$50K+/month**: Negotiate custom pricing with Snowflake/Databricks/etc.

### Question 5: Do you care about vendor lock-in?

- **Don't care**: Snowflake or BigQuery (best features, proprietary formats)
- **Moderate concern**: Databricks (Delta Lake is open format)
- **High concern**: ClickHouse or Druid (fully open source)

---

## Common Misconceptions

### "We need a data lake before a data warehouse"

**Reality**: Most companies should start with a data warehouse, not a data lake. Data lakes are useful for unstructured data (images, videos, logs), but 90% of analytics needs are structured data (sales, customers, revenue) which belong in a data warehouse.

**When you need a lake**: Machine learning on raw logs, archiving historical data for compliance, storing unstructured data (images/video).

### "Data warehouses are only for enterprises"

**Reality**: Modern data warehouses (BigQuery, ClickHouse Cloud) start at $50-200/month. Perfectly viable for startups with 500GB-1TB of data.

### "Snowflake is always expensive"

**Reality**: Snowflake can be expensive if misconfigured (auto-scaling clusters, inefficient queries). But for many workloads, it's cost-competitive with BigQuery and Redshift when optimized properly.

### "We can build our own data warehouse"

**Reality**: Possible (Postgres with columnar extension, ClickHouse self-hosted), but only worth it if:
- You have dedicated data engineering team
- Your needs are very specific (custom aggregations)
- You're at massive scale (1PB+) where cloud costs are prohibitive

For most companies: Use managed service. Focus engineering time on business logic, not infrastructure.

---

## Integration with Other Systems

### Upstream: Where Data Comes From

Data warehouses pull data from:
- **Production databases** (3.040): Postgres, MySQL (via ETL/ELT)
- **SaaS applications**: Salesforce, Stripe, HubSpot (via Fivetran, Airbyte)
- **Event tracking**: Segment, Rudderstack (real-time event streams)
- **Object storage** (3.031): S3, Azure Blob (data lake raw files)

### Downstream: What Uses Data Warehouse

- **BI tools**: Tableau, Looker, Power BI, Metabase (dashboards & reports)
- **FP&A platforms** (3.007): Causal, Runway (financial planning)
- **Reverse ETL**: Census, Hightouch (warehouse → operational systems)
- **Data catalogs** (3.064): OpenMetadata, Atlan (metadata layer on top)

---

## Cost Examples

### Scenario 1: Startup Analytics (1TB data, 10 queries/day)
- **BigQuery**: $20/month storage + $30/month queries = **$50/month**
- **Snowflake**: $40/month storage + $60/month compute = **$100/month**
- **ClickHouse Cloud**: $15/month storage + $40/month compute = **$55/month**

### Scenario 2: Mid-Market Company (10TB data, 100 queries/day)
- **BigQuery**: $200/month storage + $600/month queries = **$800/month**
- **Snowflake**: $400/month storage + $800/month compute = **$1,200/month**
- **Redshift**: $5,000/month reserved cluster = **$5,000/month**

### Scenario 3: Enterprise (100TB data, 24/7 concurrent queries)
- **BigQuery**: $2,000/month storage + $8,000/month queries = **$10,000/month**
- **Snowflake**: $4,000/month storage + $15,000/month compute = **$19,000/month**
- **Redshift**: $25,000/month reserved cluster = **$25,000/month**

**Key insight**: Consumption pricing (BigQuery, Snowflake) scales better for variable workloads. Reserved pricing (Redshift) better for consistent 24/7 usage.

---

## Summary: 30-Second Decision Tree

```
Do you have >100GB of data across multiple sources?
├─ NO → Stay on production database (add read replica)
└─ YES → Need data warehouse
    │
    ├─ Budget <$500/month?
    │  └─ YES → BigQuery or ClickHouse Cloud
    │
    ├─ Google Cloud ecosystem?
    │  └─ YES → BigQuery
    │
    ├─ Need real-time (<1 second queries)?
    │  └─ YES → ClickHouse or Druid
    │
    ├─ Heavy ML/Python workloads?
    │  └─ YES → Databricks Lakehouse
    │
    ├─ AWS-heavy, predictable workload?
    │  └─ YES → Redshift
    │
    └─ General purpose, multi-cloud?
       └─ YES → Snowflake
```

---

## Next Steps

1. **Audit current state**: How much data? How many analytics queries? Current database struggling?
2. **Estimate costs**: Use vendor calculators (Snowflake, BigQuery, Redshift)
3. **Run POC**: Load sample data (1-10% of total) and test queries on 2-3 platforms
4. **Start small**: Begin with 1-2 data sources, expand over time
5. **Monitor costs**: Set budget alerts (especially on consumption-based platforms)

**Further reading**: See S1-S4 discovery documents for detailed platform comparisons, TCO models, and use case recommendations.
