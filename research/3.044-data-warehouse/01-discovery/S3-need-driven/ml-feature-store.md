# S3 Scenario 6: ML Feature Store

**Last Updated**: November 6, 2025
**Scenario Type**: Series C AI/ML Company
**Primary Use Case**: Feature engineering and model training data management

---

## 1. Scenario Profile

### Business Context

**Company Stage & Profile**:
VectorAI is a Series C AI/ML company with 150 employees that provides predictive analytics solutions for e-commerce personalization. After raising $40M in Series C funding, the company is scaling its machine learning operations to support 50+ enterprise customers. The data science team develops recommendation engines, demand forecasting models, and customer churn prediction systems that require sophisticated feature engineering pipelines and reproducible model training workflows.

**Industry & Business Model**:
The company operates a B2B SaaS model delivering ML-powered insights through APIs and embedded analytics. Revenue comes from platform fees ($50K-$500K annually per customer) plus usage-based pricing for API calls. The business depends on rapid experimentation cycles—data scientists must iterate on features, train models, and deploy improvements weekly to maintain competitive advantage in recommendation accuracy and prediction performance.

**Key Business Challenges**:
The existing ML infrastructure combines Python notebooks on EC2 instances, S3 data lakes with ad-hoc Parquet files, and custom feature engineering scripts duplicated across projects. This fragmented approach creates critical problems: (1) feature engineering code is duplicated across 12+ ML projects causing inconsistent definitions of metrics like "customer lifetime value" or "7-day engagement score", (2) reproducing training datasets from 3 months ago requires manual reconstruction because feature snapshots aren't versioned, (3) data scientists spend 60% of their time on data preparation instead of model development, (4) training large models on 100TB datasets takes 12+ hours due to inefficient data scanning, and (5) monitoring feature drift in production requires custom tooling that breaks frequently.

**Success Metrics**:
A successful data warehouse implementation would enable: (1) centralized feature store with versioned features reducing engineering duplication by 70%, (2) reproducible training datasets allowing recreation of any historical model's exact training data, (3) Python-native workflows eliminating context switching between notebooks and SQL, (4) training query performance under 2 hours for typical 10TB dataset scans, (5) feature freshness monitoring and drift detection built into platform, and (6) total infrastructure cost under $25,000/month including compute for training and serving.

### Technical Context

**Current State**:
- **Data Lake**: S3 buckets contain 100TB of raw data (customer events, transaction logs, product catalogs) in Parquet format with inconsistent partitioning schemes
- **Feature Engineering**: 50+ Jupyter notebooks scattered across data scientist workstations with custom PySpark and pandas scripts
- **Training**: EMR clusters spun up ad-hoc for model training, leading to inconsistent cluster configurations and unpredictable costs
- **Feature Serving**: Python microservices query S3 directly for real-time predictions, causing 200-500ms latency
- **Monitoring**: Custom CloudWatch metrics and homegrown Python scripts for data quality checks

**Existing Cloud Platform**:
The company runs on AWS with data in S3 (us-west-2), ML training on EMR and SageMaker, and application infrastructure on EKS. The team has deep Python and Spark expertise but limited SQL knowledge. All ML engineers prefer working in notebooks (Jupyter, Databricks) rather than traditional SQL IDEs. AWS expertise is strong, but managing EMR clusters and optimizing Spark jobs consumes significant engineering time.

**Team Composition**:
- **Data Scientists** (15 users): Build ML models, develop features, run experiments, evaluate model performance
- **ML Engineers** (8 users): Productionize models, optimize inference pipelines, manage training infrastructure
- **Data Engineers** (5 users): Maintain data pipelines, ensure data quality, manage ETL from customer systems
- **Analytics Engineers** (4 users): Support business analytics, build dashboards, create customer-facing reports
- **Research Scientists** (3 users): Experiment with novel algorithms, require access to full raw datasets
- **Leadership** (5 users): Monitor platform health metrics, track model performance, review business KPIs

**Technical Constraints**:
- **Python-First Workflow**: Team strongly prefers Python over SQL; solution must support native Python dataframes (Pandas, Polars) and PySpark
- **Reproducibility**: Must version features and training datasets to recreate exact model training conditions from any historical point
- **Performance**: Training queries scanning 10TB should complete in under 2 hours; feature engineering jobs on 1TB datasets should finish in under 30 minutes
- **Integration**: Must integrate with existing SageMaker training jobs, MLflow experiment tracking, and real-time inference services
- **Compliance**: Customer data includes PII requiring encryption at rest, GDPR compliance for EU customers, and audit logs for data access

### Data Characteristics

**Current Data Volume**:
- **Raw Event Data**: 50TB of customer behavioral events (clicks, purchases, browsing sessions) with 50M events/day
- **Feature Tables**: 30TB of computed features (rolling aggregations, embeddings, derived metrics) refreshed daily/hourly
- **Training Datasets**: 15TB of historical training datasets for model versioning and reproducibility
- **Dimensional Data**: 5TB of customer profiles, product catalogs, category hierarchies
- **Growth Rate**: 30% annually as customer base expands and new event types are tracked

**Data Sources**:
1. **Customer Event Streams**: Real-time events via Kafka from 50+ customer deployments (purchases, clicks, sessions)
2. **Transactional Databases**: Nightly dumps from customer PostgreSQL/MySQL databases with orders, products, inventory
3. **Third-Party Enrichment**: Demographic data from Clearbit, geographic data from Census Bureau
4. **Internal Systems**: Model predictions, A/B test results, feature importance scores from MLflow
5. **Web Analytics**: Clickstream data from customer websites via Segment

**Data Types**:
- **Structured**: Relational tables (customers, products, orders) requiring standard SQL operations
- **Semi-Structured**: JSON event payloads with nested attributes and variable schemas
- **Embeddings**: Dense vector arrays (256-1024 dimensions) for product and user embeddings
- **Time-Series**: Temporal features requiring window functions and rolling aggregations (7-day click rate, 30-day purchase frequency)

**Query Patterns**:
- **Feature Engineering**: Complex window functions, rolling aggregations, and joins across billion-row tables
- **Model Training**: Large scans of 1-10TB datasets with filtering by date ranges and customer cohorts
- **Batch Scoring**: Daily batch predictions on entire customer base (10M+ records) requiring sub-2-hour completion
- **Feature Serving**: Low-latency point lookups (1-50ms) for real-time predictions serving user-specific features
- **Experimentation**: Ad-hoc analysis by data scientists exploring feature distributions and correlations across 100+ feature columns

### User Requirements

**Primary Users**:
- **Data Scientists** (15 users): Run 50-100 feature engineering queries daily, train 10-20 models weekly, expect Python notebook integration
- **ML Engineers** (8 users): Deploy 5-10 models monthly, monitor 30+ production models, require programmatic API access
- **Data Engineers** (5 users): Manage 20+ daily ETL jobs, debug data quality issues, optimize pipeline performance
- **Analytics Engineers** (4 users): Build 10-15 customer-facing dashboards, support SQL-based reporting for stakeholders

**Query Patterns by User Type**:
- **Data Scientists**: Complex feature engineering with window functions (target: 5-30 minutes for 1TB scans)
- **ML Engineers**: Batch prediction queries on 10M rows (target: under 1 hour)
- **Data Engineers**: Metadata queries and data quality checks (target: sub-second for monitoring queries)
- **Analytics Engineers**: Standard aggregation queries for dashboards (target: 2-10 seconds)

**Concurrency Requirements**:
Peak concurrency occurs during business hours (9am-6pm PT) when 20-30 users run simultaneous queries. System must support: (1) 10-15 concurrent feature engineering jobs (each scanning 100GB-1TB), (2) 5-10 interactive notebook queries for exploratory analysis, (3) 5 concurrent model training jobs loading training datasets, and (4) continuous real-time feature serving for production inference (1000+ queries/second).

**SLA Expectations**:
- **Feature Engineering**: Queries on 1TB complete in under 30 minutes (p95)
- **Model Training Dataset Creation**: 10TB scans complete in under 2 hours
- **Interactive Exploration**: Ad-hoc queries on 100GB return in under 2 minutes
- **Feature Serving**: Point lookups for real-time inference in under 50ms (p99)
- **Batch Scoring**: Daily batch predictions on 10M records complete in under 90 minutes
- **Uptime**: 99.9% availability with scheduled maintenance windows on weekends

---

## 2. Requirements Matrix

### MoSCoW Prioritization

**Must Have** (Non-negotiable requirements):

1. **Python-Native Interface**: Native support for Pandas/Polars dataframes, PySpark, and Python UDFs—SQL-only solutions are non-starters for this Python-heavy team
2. **Feature Versioning**: Time-travel capabilities to recreate exact training datasets from any historical timestamp for model reproducibility
3. **High-Performance Analytics**: Queries scanning 1TB complete in under 30 minutes; 10TB training dataset queries complete in under 2 hours
4. **ML Framework Integration**: Native integration with SageMaker, MLflow, and Python ML libraries (scikit-learn, TensorFlow, PyTorch)
5. **Budget Constraint**: Total cost under $25,000/month including storage (100TB), compute (training and serving), and platform fees

**Should Have** (Important, strong preference):

1. **Unified Lakehouse Architecture**: Single platform for both data warehousing and data lake capabilities eliminating S3 data movement
2. **Streaming Ingestion**: Real-time or near-real-time feature updates (within 15 minutes) for serving fresh features to production models
3. **GPU Support**: Ability to run GPU-accelerated training and inference workloads for deep learning models
4. **Delta Lake/Iceberg Support**: ACID transactions and schema evolution for reliable feature tables
5. **Auto-Scaling Compute**: Dynamic compute scaling to handle variable workloads without manual cluster management
6. **Collaborative Notebooks**: Built-in notebook environment with version control and collaboration features

**Could Have** (Nice-to-have features):

1. **Feature Store SDK**: Pre-built Python SDK for feature registration, versioning, and serving patterns
2. **AutoML Capabilities**: Automated feature selection and hyperparameter tuning tools
3. **Model Registry**: Built-in model versioning and deployment management
4. **Data Lineage Tracking**: Automated tracking of feature dependencies and data provenance
5. **Embedded BI**: Native visualization tools for feature distribution analysis and model monitoring dashboards

**Won't Have** (Explicitly out of scope):

1. **Graph Analytics**: No graph database requirements (customer relationships are tabular)
2. **Geospatial Analytics**: Limited geographic analysis needs (simple country/region filtering sufficient)
3. **Video/Image Storage**: Media files stored in S3; warehouse only stores metadata and embeddings
4. **Real-Time OLTP**: No transactional update requirements; append-only event streams and batch updates sufficient

### Requirements Scoring Table

| Requirement Category | Weight | Databricks | Snowflake | BigQuery | Redshift | ClickHouse |
|---------------------|--------|-----------|-----------|----------|----------|------------|
| **Must Have** | | | | | | |
| Python-Native Interface | 20% | 10/10 | 7/10 | 8/10 | 4/10 | 5/10 |
| Feature Versioning | 15% | 10/10 | 9/10 | 8/10 | 6/10 | 4/10 |
| Performance (1TB/30min) | 15% | 9/10 | 8/10 | 9/10 | 7/10 | 10/10 |
| ML Integration | 15% | 10/10 | 7/10 | 8/10 | 5/10 | 3/10 |
| Budget ($25K/month) | 10% | 8/10 | 6/10 | 7/10 | 7/10 | 9/10 |
| **Should Have** | | | | | | |
| Lakehouse Architecture | 10% | 10/10 | 8/10 | 7/10 | 4/10 | 3/10 |
| Streaming Ingestion | 5% | 8/10 | 7/10 | 6/10 | 5/10 | 9/10 |
| GPU Support | 5% | 10/10 | 3/10 | 4/10 | 2/10 | 2/10 |
| Auto-Scaling | 5% | 9/10 | 9/10 | 10/10 | 6/10 | 6/10 |
| **Total Score** | 100% | **9.35** | **7.45** | **7.85** | **5.50** | **6.20** |

**Shortlist Finalists**:
1. **Databricks** (9.35/10) - Clear winner for Python-heavy ML workloads
2. **Snowflake** (7.45/10) - Strong alternative if SQL adoption increases
3. **BigQuery** (7.85/10) - Considered but weaker ML integration than Databricks

---

## 3. Provider Shortlist

### Long List Elimination

**Initial Candidates**: Databricks, Snowflake, BigQuery, Redshift, ClickHouse, Azure Synapse, Firebolt, Druid

**Eliminated Providers**:

- **Redshift**: Python support limited (only Python UDFs via Redshift ML, no native PySpark); ML integration weak; lakehouse architecture requires separate Spectrum setup
- **ClickHouse**: Excellent performance but lacks ML framework integration, time-travel capabilities limited, no native Python dataframe support
- **Azure Synapse**: Excluded due to AWS commitment; comparable to Databricks but requires Azure migration
- **Firebolt**: Strong performance but immature ML tooling; limited Python notebook support
- **Druid**: Optimized for real-time analytics, not batch ML workloads; no feature versioning capabilities

**Shortlist**: Databricks, Snowflake, BigQuery

### Shortlist Provider Profiles

#### Option 1: Databricks (Primary Recommendation)

**Why Included**:
- **Python-First Design**: Native PySpark, Pandas-on-Spark, Koalas for seamless Python dataframe workflows; built-in collaborative notebooks
- **Lakehouse Architecture**: Unity Catalog provides unified governance over Delta Lake tables in S3; eliminates data movement between lake and warehouse
- **ML Integration**: Native MLflow integration, Feature Store with versioning, AutoML, deep integration with SageMaker
- **Performance**: Photon engine delivers 1TB scans in 15-25 minutes; optimized for complex window functions and joins common in feature engineering
- **Delta Lake**: Time-travel and ACID transactions enable reproducible training datasets; schema evolution handles changing event schemas
- **GPU Support**: Clusters support GPU instances for deep learning training and inference

**Concerns**:
- **Complexity**: Feature-rich platform has steeper learning curve; cluster configuration tuning required for cost optimization
- **Cost Variability**: DBU consumption can spike with inefficient queries; requires governance and monitoring to stay within budget
- **SQL Users**: Analytics engineers familiar with SQL may find notebook-first workflow less intuitive than Snowflake

**Cost Estimate**:
- **Storage**: 100TB in S3 Delta Lake format = $2,300/month (S3 standard)
- **Compute (Training)**: 500 DBUs/day average for feature engineering and model training at $0.55/DBU = $8,250/month
- **Compute (Interactive)**: 200 DBUs/day for ad-hoc queries and notebooks at $0.55/DBU = $3,300/month
- **Platform Fee**: Databricks platform markup on AWS compute (~40% of compute) = $4,620/month
- **Total**: ~$18,470/month
- **3-Year TCO**: ~$665,000 (assumes 25% annual growth)

**Implementation Complexity**: 6-8 weeks (2 weeks workspace setup and Unity Catalog configuration, 3 weeks migrating feature pipelines from EMR to Databricks notebooks, 2 weeks MLflow integration and SageMaker connectivity, 1 week training and documentation)

#### Option 2: Snowflake (Runner-Up)

**Why Included**:
- **Snowpark Python**: Python dataframe API (Snowpark) enables native Python workflows without leaving Snowflake; UDFs support Python ML libraries
- **Time Travel**: Up to 90 days time-travel for dataset recreation; cloning for reproducible training environments
- **Performance**: Strong performance on large scans; vectorized Python UDFs improve feature engineering query speed
- **Separation of Compute/Storage**: Independent scaling of storage and compute; pause warehouses when not in use
- **SQL Excellence**: If analytics engineers adopt SQL-based feature engineering, Snowflake's SQL engine and dbt integration are best-in-class

**Concerns**:
- **Python Maturity**: Snowpark Python is newer than PySpark; some advanced ML workflows require workarounds
- **ML Tooling**: ML integration less mature than Databricks; no native Feature Store or MLflow alternative
- **Cost at Scale**: Compute costs for large feature engineering jobs can exceed Databricks due to less optimized Spark execution
- **Lakehouse Gaps**: External tables for S3 data lack full optimization; moving 100TB into Snowflake storage increases costs

**Cost Estimate**:
- **Storage**: 100TB in Snowflake = $2,300/month ($23/TB/month)
- **Compute (Training)**: 3X-Large warehouse running 10 hours/day = $9,600/month
- **Compute (Interactive)**: Large warehouse running 12 hours/day = $4,320/month
- **Compute (Serving)**: Small warehouse for feature serving = $1,440/month
- **Total**: ~$17,660/month (slightly cheaper than Databricks but less optimized for ML workloads)
- **3-Year TCO**: ~$635,000

**Implementation Complexity**: 6-8 weeks (similar timeline to Databricks; additional time learning Snowpark vs familiar PySpark)

#### Option 3: BigQuery (Considered)

**Why Included**:
- **Serverless**: No cluster management; queries auto-scale without configuration
- **BigQuery ML**: SQL-based ML model training; supports TensorFlow model imports
- **Performance**: Excellent scan performance; 1TB queries complete in 10-20 minutes
- **Cost Predictability**: Pay-per-query pricing with flat-rate option for predictable budgets

**Concerns**:
- **Python Limitations**: Python support via BigQuery DataFrames is limited; most workflows require pandas with local data movement
- **GCP Migration**: Company committed to AWS; adopting BigQuery requires multi-cloud complexity
- **ML Integration**: No native MLflow, SageMaker integration; requires custom tooling
- **Lakehouse**: BigLake for S3 integration exists but less mature than Databricks Unity Catalog

**Cost Estimate**: ~$14,000/month (competitive but GCP migration risk outweighs cost savings)

**Implementation Complexity**: 10-12 weeks (includes GCP setup, cross-cloud networking, team training on GCP tools)

### Winner Selection

**Primary Recommendation: Databricks**

**Rationale**: Databricks is purpose-built for this exact use case. The combination of native PySpark (familiar to the team from EMR experience), Delta Lake lakehouse architecture (no S3 data movement), built-in Feature Store with versioning (solves reproducibility problem), MLflow integration (existing tool), and GPU support (deep learning models) makes it the clear winner. The platform directly addresses all five critical business challenges: (1) centralized feature definitions, (2) versioned training datasets, (3) Python-native workflows, (4) optimized performance for feature engineering, and (5) production-grade monitoring. Cost is within budget at ~$18,500/month with room for growth.

**Runner-Up: Snowflake**

**Choose Snowflake If**:
- **SQL Adoption Increases**: If analytics engineers become primary feature engineering owners and prefer SQL over Python
- **Simpler Architecture Preferred**: Team prioritizes ease of use over ML-specific features
- **Cost Optimization Priority**: Willing to sacrifice some ML tooling for slightly lower costs and simpler billing
- **Multi-Workload Consolidation**: Need to support both ML feature engineering and traditional BI reporting with single platform optimized for SQL

---

## 4. Architecture Pattern

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                           DATA SOURCES                               │
└─────────────────────────────────────────────────────────────────────┘
         │                    │                  │              │
    Customer Events      Transactional DBs   3rd Party    Internal Systems
    (Kafka Streams)     (Postgres/MySQL)    (Clearbit)    (MLflow/A/B Tests)
         │                    │                  │              │
         ▼                    ▼                  ▼              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        INGESTION LAYER                               │
│  ┌─────────────────┐  ┌────────────────┐  ┌──────────────────────┐ │
│  │ Kafka Connect   │  │ Fivetran       │  │ Databricks Autoloader│ │
│  │ → S3 (Raw)      │  │ → Delta Tables │  │ → Delta Tables       │ │
│  └─────────────────┘  └────────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STORAGE LAYER (Delta Lake on S3)                  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Unity Catalog (Governance & Metadata)                        │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │ Bronze Tables: Raw events, database dumps (50TB)             │  │
│  │ Silver Tables: Cleaned, deduplicated events (30TB)           │  │
│  │ Gold Tables: Feature tables, aggregated metrics (15TB)       │  │
│  │ Training Datasets: Versioned snapshots (15TB)                │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     TRANSFORMATION LAYER                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Databricks Notebooks (Python/PySpark)                        │  │
│  │  - Feature Engineering (window functions, aggregations)      │  │
│  │  - Data Quality Checks (Great Expectations)                  │  │
│  │  - Training Dataset Creation (with versioning)               │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │ Databricks Feature Store                                     │  │
│  │  - Feature Registration & Versioning                         │  │
│  │  - Point-in-Time Correctness                                 │  │
│  │  - Online/Offline Feature Serving                            │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                ▼                               ▼
┌─────────────────────────────┐   ┌───────────────────────────────┐
│    TRAINING & SERVING        │   │    ANALYTICS & BI             │
│                              │   │                               │
│ ┌─────────────────────────┐ │   │ ┌───────────────────────────┐ │
│ │ Model Training          │ │   │ │ Databricks SQL            │ │
│ │ - SageMaker Integration │ │   │ │ - Analytics Queries       │ │
│ │ - Databricks ML Runtime │ │   │ │ - Dashboard Serving       │ │
│ │ - GPU Clusters          │ │   │ └───────────────────────────┘ │
│ └─────────────────────────┘ │   │              │                │
│              │               │   │              ▼                │
│              ▼               │   │ ┌───────────────────────────┐ │
│ ┌─────────────────────────┐ │   │ │ Looker / Tableau          │ │
│ │ MLflow (Tracking)       │ │   │ │ - Business Dashboards     │ │
│ │ - Experiment Logging    │ │   │ │ - Customer Reports        │ │
│ │ - Model Registry        │ │   │ └───────────────────────────┘ │
│ └─────────────────────────┘ │   └───────────────────────────────┘
│              │               │
│              ▼               │
│ ┌─────────────────────────┐ │
│ │ Feature Serving         │ │
│ │ - Real-time Inference   │ │
│ │ - Batch Predictions     │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATION                                 │
│  Databricks Workflows + Airflow (for cross-system orchestration)    │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

**Data Sources**:
1. **Customer Event Streams**: Kafka topics from 50+ customer deployments streaming 50M events/day (purchases, clicks, sessions)
2. **Transactional Databases**: PostgreSQL and MySQL database dumps via Fivetran CDC or nightly batch extracts
3. **Third-Party APIs**: Clearbit demographic enrichment, Census Bureau geographic data via API connectors
4. **Internal Systems**: MLflow experiment tracking, A/B test results, feature importance scores from production models

**Ingestion Layer**:
- **Kafka Connect S3 Sink**: Stream events directly to S3 in JSON/Avro format; Databricks Autoloader incrementally ingests with schema inference
- **Fivetran**: Managed CDC connectors for PostgreSQL/MySQL → Delta Lake tables; handles schema changes automatically
- **Databricks Autoloader**: Cloud-native ingestion for S3 data with automatic schema evolution and exactly-once processing
- **API Connectors**: Python notebooks with scheduled runs to pull third-party data into Delta tables

**Storage Layer (Delta Lake on S3)**:
- **Unity Catalog**: Centralized governance providing fine-grained access control, data lineage, audit logging across all Delta tables
- **Bronze Layer** (50TB): Raw, immutable event data and database snapshots; partitioned by date for efficient time-range queries
- **Silver Layer** (30TB): Cleaned and deduplicated data; standardized schemas; enforced data quality rules
- **Gold Layer** (15TB): Feature tables with computed features (rolling aggregations, embeddings, derived metrics); optimized for model training
- **Training Datasets** (15TB): Versioned snapshots of training data with metadata linking to model versions in MLflow

**Transformation Layer**:
- **Databricks Notebooks**: Python/PySpark notebooks for feature engineering using familiar pandas-like API and distributed Spark for large datasets
- **Feature Engineering Jobs**: Scheduled workflows computing rolling aggregations (7-day click rate), window functions (customer rank by spend), and complex joins (orders + clicks + demographics)
- **Data Quality**: Great Expectations integrated into notebooks to validate feature distributions, check for nulls, detect schema drift
- **Databricks Feature Store**: Central registry for features with versioning, lineage tracking, and point-in-time correctness for training/serving consistency

**Consumption Layer**:
- **Model Training**: SageMaker jobs read training datasets from Delta Lake; Databricks ML Runtime clusters with GPU support for deep learning; Databricks AutoML for rapid prototyping
- **MLflow**: Centralized experiment tracking logging hyperparameters, metrics, and artifacts; model registry for version control and deployment management
- **Feature Serving**: Real-time inference via Databricks Feature Store online store (DynamoDB or RDS); batch predictions via Spark jobs writing to Delta tables
- **Analytics & BI**: Databricks SQL endpoints serve business dashboards in Looker/Tableau; analytics engineers write SQL queries on Gold layer tables

**Orchestration**:
- **Databricks Workflows**: Schedule feature engineering pipelines, model training jobs, and batch scoring workflows with dependency management
- **Airflow** (optional): Cross-system orchestration if workflows span Databricks + SageMaker + external systems; otherwise Databricks Workflows sufficient

### Architecture Decisions

**ELT over ETL**:
- **Decision**: Use ELT pattern with raw data landing in S3 (Bronze), then transformed within Databricks (Silver/Gold)
- **Rationale**: Data scientists need access to raw events for exploratory analysis; Databricks Spark engine is optimized for large-scale transformations; cheaper to store raw data in S3 than pre-filter at ingestion

**Lakehouse over Separate Lake + Warehouse**:
- **Decision**: Delta Lake on S3 as single source of truth; no separate data warehouse
- **Rationale**: Eliminates data duplication and ETL between lake and warehouse; Unity Catalog provides governance over S3 data; reduces costs by avoiding dual storage; enables ML and BI on same datasets

**Feature Store as Central Pattern**:
- **Decision**: Databricks Feature Store as primary interface for feature access (not ad-hoc Delta table queries)
- **Rationale**: Enforces feature reuse across projects; ensures point-in-time correctness preventing data leakage; provides online/offline consistency for training/serving; tracks feature lineage for debugging

**Hybrid Batch + Streaming**:
- **Decision**: Batch feature pipelines (daily/hourly) for most features; streaming for time-sensitive features (recent click count)
- **Rationale**: Most features stable over hours (daily purchase patterns); streaming adds complexity; 15-minute latency acceptable for 90% of use cases; Structured Streaming enables real-time for critical features

### Scalability Considerations

**Data Volume Growth** (30% annually → 130TB in Year 2, 169TB in Year 3):
- **Storage Scaling**: S3 scales infinitely; Delta Lake partitioning by date ensures queries only scan relevant data
- **Compute Scaling**: Databricks auto-scaling clusters grow from 4 to 40 nodes during heavy feature engineering jobs; shrink to zero when idle
- **Cost Management**: Implement table optimization (OPTIMIZE, ZORDER), partition pruning, and caching strategies; monitor DBU consumption with alerts

**User Concurrency** (40 users → 60 users in Year 2):
- **Interactive Queries**: Separate SQL endpoints for analytics engineers (smaller clusters) vs. data scientists (larger clusters for feature engineering)
- **Job Isolation**: Feature engineering jobs run on dedicated job clusters; model training on separate GPU clusters; prevents resource contention
- **Query Optimization**: Databricks Photon engine accelerates SQL queries; result caching reduces redundant scans; query history analysis identifies optimization opportunities

**Performance Maintenance**:
- **Table Maintenance**: Weekly OPTIMIZE and VACUUM operations to compact small files and remove old versions
- **Partition Strategy**: Partition feature tables by date (Year/Month/Day) ensuring most queries scan <10% of data
- **Z-Ordering**: ZORDER by frequently filtered columns (customer_id, event_type) to co-locate related data
- **Caching**: Databricks Delta Cache on SSD-backed instances for frequently accessed feature tables

---

## 5. Implementation Guide

### Phase 1: Foundation (Week 1-2)

**Week 1: Workspace Setup & Data Lake Foundation**

*Day 1-2: AWS Infrastructure*
- Provision S3 bucket for Delta Lake (with versioning enabled, lifecycle policies for cost optimization)
- Configure IAM roles for Databricks-to-S3 access using instance profiles (following least-privilege principle)
- Set up VPC peering between Databricks workspace and existing AWS VPC for secure connectivity
- Enable S3 server-side encryption (SSE-S3) for compliance requirements

*Day 3-4: Databricks Workspace Configuration*
- Create Databricks workspace on AWS (us-west-2 to match existing infrastructure)
- Configure Unity Catalog metastore linked to S3 bucket
- Define catalog structure: `production` (live data), `development` (experimentation), `staging` (validation)
- Set up user groups in Unity Catalog: data_scientists, ml_engineers, data_engineers, analysts
- Configure workspace-level settings: cluster policies (max nodes, instance types), notebook permissions, secret scopes

*Day 5: First Data Pipeline*
- Ingest sample dataset (1 month of customer events from S3) using Databricks Autoloader
- Create Bronze table with raw events; validate record counts match source
- Write simple Silver transformation (deduplicate events, parse JSON, standardize timestamps)
- Run first PySpark query aggregating events by day; verify results in Databricks SQL

**Deliverable**: Working Databricks workspace with Unity Catalog, sample data ingested, and team access configured. First query executed successfully demonstrating end-to-end data flow from S3 → Bronze → Silver → Query.

### Phase 2: Core Implementation (Week 3-6)

**Week 3: Data Ingestion Pipeline**

- Deploy Fivetran connectors for PostgreSQL production database (users, orders, subscriptions)
- Configure Kafka Connect S3 sink for real-time event streams; validate delivery to S3
- Set up Databricks Autoloader notebooks to incrementally process S3 event data into Bronze tables
- Implement data quality checks in Bronze layer: row count validation, schema enforcement, partition existence checks
- Schedule ingestion jobs in Databricks Workflows (Kafka events every 15 minutes, database snapshots nightly)

**Week 4: Feature Engineering Pipeline Migration**

- Identify top 20 features used across ML projects (from existing notebook analysis)
- Translate 5 core feature engineering notebooks from EMR PySpark to Databricks notebooks
  - Example 1: 7-day rolling click rate (window function over events joined with users)
  - Example 2: Customer lifetime value (aggregate orders + subscriptions with Python UDF)
  - Example 3: Product embedding vectors (join catalog with pre-trained embeddings from S3)
  - Example 4: Session engagement score (complex event sequence analysis)
  - Example 5: Churn risk features (time since last purchase, declining engagement trends)
- Register features in Databricks Feature Store with metadata (description, owner, refresh schedule)
- Validate feature values match EMR outputs (compare 1000 sample customer_ids)

**Week 5: Model Training Integration**

- Set up MLflow tracking server (Databricks-managed or self-hosted on EC2)
- Migrate 2 pilot ML models from EMR to Databricks:
  - Model 1: Recommendation engine (load training dataset from Feature Store, train LightGBM model, log to MLflow)
  - Model 2: Churn prediction (create point-in-time training dataset, train scikit-learn model, evaluate on holdout set)
- Configure SageMaker integration for deep learning models requiring GPU training
- Implement training dataset versioning workflow (snapshot feature table with model_version tag in Delta)
- Create Databricks Workflow to orchestrate feature pipeline → training dataset creation → model training

**Week 6: BI and Analytics Setup**

- Deploy Databricks SQL endpoint (size: Medium) for analytics workloads
- Create 5 core dashboards in Databricks SQL:
  - Dashboard 1: Platform Health (data freshness, pipeline success rates, query performance)
  - Dashboard 2: Feature Monitoring (feature distributions, null rates, drift detection)
  - Dashboard 3: Model Performance (prediction volume, accuracy trends, latency metrics)
  - Dashboard 4: Customer Analytics (MAU, engagement scores, churn predictions)
  - Dashboard 5: Business KPIs (revenue, customer growth, feature adoption)
- Connect Looker or Tableau to Databricks SQL endpoint for executive reporting
- Train analytics engineers on SQL query editor and dashboard creation

**Deliverable**: Production-ready feature engineering pipelines running daily, 20+ features registered in Feature Store, 2 ML models successfully trained and logged in MLflow, BI dashboards operational. Data scientists can query features via Feature Store API and Python notebooks.

### Phase 3: Production Rollout (Week 7-10)

**Week 7: Feature Serving and Real-Time Inference**

- Deploy Databricks Feature Store online store (DynamoDB or RDS backend) for low-latency feature serving
- Implement feature publishing workflow: batch job writes features from Delta → online store every hour
- Integrate real-time inference service (Python microservice on EKS) with online feature store
- Performance testing: validate <50ms p99 latency for feature lookups during inference
- Deploy shadow mode: new inference service runs parallel to existing service, compare predictions for consistency

**Week 8: Migration and Validation**

- Migrate remaining 10 feature engineering notebooks from EMR to Databricks
- Run parallel pipelines for 1 week (EMR + Databricks) to validate output consistency
- Reconciliation testing: compare feature values for 10,000 random customers between EMR and Databricks outputs
- Decommission EMR clusters after successful validation (estimated cost savings: $4,000/month)
- Update documentation with Databricks notebook URLs and Feature Store catalog

**Week 9: User Training and Onboarding**

- Conduct 3-day training program for 40 users:
  - Day 1 (Data Scientists): PySpark on Databricks, Feature Store SDK, MLflow integration, notebook collaboration
  - Day 2 (ML Engineers): Databricks Workflows, model deployment patterns, monitoring setup, cost optimization
  - Day 3 (Analytics Engineers): Databricks SQL, dashboard creation, Unity Catalog permissions, query optimization
- Create internal documentation site (Notion or Confluence) with:
  - Feature Store catalog with descriptions and usage examples
  - Best practices for notebook development and cluster configuration
  - Cost optimization guidelines (spot instances, auto-termination, cluster sizing)
  - FAQ and troubleshooting guide
- Establish office hours (2 hours/week) for ongoing support questions

**Week 10: Monitoring, Optimization, and Hardening**

- Implement monitoring stack:
  - Databricks system tables for query performance and cluster utilization analysis
  - CloudWatch alarms for pipeline failures, data freshness delays, and cost spikes
  - Great Expectations data quality suite running nightly on Silver/Gold tables
  - Custom Python dashboard showing DBU consumption trends by team and project
- Performance optimization pass:
  - Analyze slow queries using Databricks query history; apply ZORDER and partition tuning
  - Optimize table file sizes with OPTIMIZE command; schedule weekly maintenance jobs
  - Review cluster configurations; right-size based on actual workload patterns
- Security hardening:
  - Enable audit logging in Unity Catalog to CloudWatch Logs
  - Configure row-level security for sensitive customer data (EU customers require GDPR compliance)
  - Implement secret management using Databricks secrets backed by AWS Secrets Manager
  - Review and lock down IAM policies using least-privilege access

**Deliverable**: Full production system with all feature pipelines migrated, 40 users trained and productive, real-time inference operational, monitoring and alerting in place, EMR decommissioned. System meeting SLA targets: 1TB feature engineering in <30 minutes, <50ms feature serving latency.

### Phase 4: Iteration and Expansion (Ongoing)

**Month 3-6: Advanced Capabilities**

- Expand Feature Store to 50+ registered features covering new ML use cases
- Implement automated feature backfilling for newly added features (historical data population)
- Deploy Databricks AutoML for rapid prototyping by data scientists (citizen data scientists can train baseline models)
- Integrate Unity Catalog data lineage with external documentation (auto-generate feature dependency graphs)
- Build custom Python SDK wrapping Feature Store for company-specific patterns (internal library for onboarding)

**Month 6-12: Scale and Optimization**

- Optimize costs as data grows to 130TB: implement Parquet compression tuning, archive old Bronze data to S3 Glacier
- Deploy streaming feature pipelines using Structured Streaming for time-sensitive use cases (real-time fraud detection)
- Implement A/B testing framework integrated with Feature Store (feature flags for controlled rollout)
- Build model monitoring dashboard tracking prediction drift, feature importance changes, and model performance degradation
- Establish Feature Store governance: feature review board, deprecation policy, naming conventions

### Team Requirements

**Roles and Time Commitment**:

- **Data Engineer** (1 FTE for first 3 months, then 0.5 FTE): Infrastructure setup, pipeline migration, monitoring implementation
- **ML Engineer** (0.5 FTE): SageMaker integration, model deployment patterns, feature serving architecture
- **Data Scientist Lead** (0.25 FTE): Feature Store design, training dataset patterns, pilot model migration
- **Analytics Engineer** (0.25 FTE): BI setup, dashboard creation, SQL training for business users

**Skill Requirements**:
- PySpark proficiency (existing EMR experience transfers directly)
- Python for notebooks and Feature Store SDK
- Delta Lake and Unity Catalog concepts (1-week learning curve)
- Databricks-specific features (Workflows, MLflow integration) learned during implementation

### Tools and Costs

**Monthly Cost Breakdown**:

| Component | Cost | Notes |
|-----------|------|-------|
| **Databricks** | | |
| - Storage (S3) | $2,300 | 100TB Delta Lake |
| - Training Compute | $8,250 | 500 DBU/day @ $0.55 |
| - Interactive Compute | $3,300 | 200 DBU/day @ $0.55 |
| - Platform Fee | $4,620 | ~40% of compute |
| **Data Ingestion** | | |
| - Fivetran | $1,500 | 3 connectors (Postgres, Stripe, Salesforce) |
| - Kafka (existing) | $0 | Already provisioned |
| **BI Tools** | | |
| - Looker | $2,000 | 20 users @ $100/user |
| **Orchestration** | | |
| - Airflow (optional) | $0 | Use Databricks Workflows |
| **Monitoring** | | |
| - CloudWatch | $200 | Logs and alarms |
| - Great Expectations | $0 | Open source |
| **Total** | **$22,170/month** | Within $25K budget |

**3-Year Cost Projection**:
- **Year 1**: $266,000 (includes setup costs)
- **Year 2**: $320,000 (25% data growth → 125TB)
- **Year 3**: $384,000 (25% data growth → 156TB)
- **Total 3-Year TCO**: $970,000

---

## 6. Cost Breakdown

### Year 1 Costs

**Setup Costs (One-Time)**:
- Databricks workspace setup and configuration: $0 (no setup fee)
- Data migration engineering time: $15,000 (1.5 engineer-months @ $10K/month contractor rate)
- Training and documentation: $5,000 (trainer fees, documentation tools)
- **Total One-Time**: $20,000

**Monthly Recurring Costs** (Average):

*Databricks Platform*:
- **Storage**: 100TB in S3 Delta Lake at $23/TB = $2,300/month
  - Breakdown: 50TB Bronze (raw events), 30TB Silver (cleaned), 15TB Gold (features), 5TB training datasets
  - S3 lifecycle policies move Bronze data >1 year to Glacier (saves ~$800/month after Year 1)
- **Training Compute**: 500 DBUs/day average
  - Feature engineering: 300 DBUs/day (6 hours on 10-node cluster with i3.xlarge instances)
  - Model training: 150 DBUs/day (3 hours on GPU cluster for deep learning)
  - Batch scoring: 50 DBUs/day (1 hour on 8-node cluster)
  - Cost: 500 DBU/day × 30 days × $0.55/DBU = $8,250/month
- **Interactive Compute**: 200 DBUs/day average
  - Ad-hoc queries by data scientists: 120 DBUs/day
  - Notebook development: 50 DBUs/day
  - Dashboard serving: 30 DBUs/day
  - Cost: 200 DBU/day × 30 days × $0.55/DBU = $3,300/month
- **Platform Fee**: ~40% markup on AWS compute = (8,250 + 3,300) × 0.4 = $4,620/month
- **Subtotal Databricks**: $18,470/month

*Data Ingestion Tools*:
- **Fivetran**: $1,500/month for 3 connectors (PostgreSQL, Stripe, Salesforce) with 5TB/month data movement
- **Kafka**: $0 (existing infrastructure, already provisioned)
- **Subtotal Ingestion**: $1,500/month

*BI and Analytics*:
- **Looker**: $2,000/month (20 users at $100/user/month)
- **Databricks SQL**: Included in Databricks platform cost
- **Subtotal BI**: $2,000/month

*Monitoring and Observability*:
- **CloudWatch**: $200/month (logs storage, custom metrics, alarms)
- **Great Expectations**: $0 (open source)
- **Subtotal Monitoring**: $200/month

**Total Monthly Recurring**: $22,170/month

**Year 1 Total**: $20,000 (setup) + $22,170/month × 12 = **$286,040**

### 3-Year TCO Projection

**Growth Assumptions**:
- Data volume: +25% annually (100TB → 125TB → 156TB)
- Users: +20% annually (40 → 48 → 58 users)
- Query volume: +30% annually as adoption increases

**Year 2 Costs**:
- Storage: 125TB × $23 = $2,875/month (+25%)
- Training Compute: 600 DBU/day × 30 × $0.55 = $9,900/month (+20% due to more models)
- Interactive Compute: 250 DBU/day × 30 × $0.55 = $4,125/month (+25% due to user growth)
- Platform Fee: (9,900 + 4,125) × 0.4 = $5,610/month
- Ingestion: $1,800/month (new data sources added)
- BI: $2,400/month (24 Looker users)
- Monitoring: $250/month
- **Year 2 Monthly**: $26,960/month
- **Year 2 Total**: $323,520

**Year 3 Costs**:
- Storage: 156TB × $23 = $3,588/month (+25%)
- Training Compute: 720 DBU/day × 30 × $0.55 = $11,880/month (+20%)
- Interactive Compute: 300 DBU/day × 30 × $0.55 = $4,950/month (+20%)
- Platform Fee: (11,880 + 4,950) × 0.4 = $6,732/month
- Ingestion: $2,200/month (additional connectors)
- BI: $2,900/month (29 Looker users)
- Monitoring: $300/month
- **Year 3 Monthly**: $32,550/month
- **Year 3 Total**: $390,600

**3-Year TCO**: $286,040 + $323,520 + $390,600 = **$1,000,160**

### Cost Optimization Strategies

**Quick Wins** (Immediate, 10-15% savings):

1. **Spot Instances for Training**: Use EC2 spot instances for job clusters (non-interactive workloads)
   - Savings: 50-70% on training compute = $4,125/month → saves ~$2,000/month
2. **Auto-Termination Policies**: Enforce 30-minute idle timeout for interactive clusters
   - Savings: Reduce interactive compute waste by 20% = saves ~$660/month
3. **Table Caching**: Enable Delta Cache on frequently queried feature tables
   - Benefit: 30% faster queries, reduced redundant scans = saves ~$500/month in compute
4. **Query Result Caching**: Enable result caching for dashboards queried hourly
   - Savings: Eliminate 80% of duplicate dashboard queries = saves ~$300/month
5. **S3 Lifecycle Policies**: Move Bronze data >12 months to S3 Glacier
   - Savings: $23/TB → $4/TB for 30TB historical data = saves ~$570/month after Year 1

**Total Quick Wins**: ~$4,030/month (18% reduction)

**Medium-Term Optimizations** (3-6 months, additional 10-15% savings):

1. **Reserved Capacity**: Purchase 1-year Databricks commit for 30% discount on predictable baseline workloads
   - Savings: 30% off 200 DBU/day baseline = saves ~$990/month
2. **Photon Acceleration**: Enable Photon engine for SQL queries (2-3x faster, uses fewer DBUs)
   - Savings: Reduce interactive query DBUs by 30% = saves ~$990/month
3. **Table Optimization**: Implement OPTIMIZE and ZORDER on all feature tables weekly
   - Benefit: 40% faster queries on feature tables = reduces compute by 20% = saves ~$1,000/month
4. **Partition Pruning**: Redesign partitioning strategy (date-based) to minimize data scanned
   - Savings: Reduce full table scans by 60% = saves ~$800/month
5. **Materialized Views**: Pre-aggregate frequently queried metrics into materialized Gold tables
   - Savings: Eliminate 50% of heavy aggregation queries = saves ~$600/month

**Total Medium-Term**: ~$4,380/month (additional 17% reduction)

**Long-Term Optimizations** (6-12 months, additional 5-10% savings):

1. **Databricks SQL Serverless**: Migrate BI queries to SQL Serverless (pay-per-query, no cluster management)
   - Savings: Eliminate idle time on SQL endpoint = saves ~$400/month
2. **Feature Store Serving Optimization**: Batch feature serving jobs during off-peak hours with larger, more efficient clusters
   - Savings: 20% reduction in serving costs = saves ~$200/month
3. **Cluster Right-Sizing**: Continuous monitoring and adjustment of cluster sizes based on workload profiling
   - Savings: Ongoing 5-10% efficiency gains = saves ~$1,100/month
4. **Compression Tuning**: Experiment with Zstandard compression for Delta tables (better than Snappy default)
   - Savings: 20% storage reduction = saves ~$460/month
5. **Databricks Pools**: Use instance pools to reduce cluster start time and reuse instances
   - Benefit: Faster job completion = 10% compute reduction = saves ~$1,150/month

**Total Long-Term**: ~$3,310/month (additional 13% reduction)

**Cumulative Savings Potential**: $4,030 + $4,380 + $3,310 = **$11,720/month (52% reduction)**
**Optimized Monthly Cost**: $22,170 - $11,720 = **$10,450/month**

### Cost Comparison: Databricks vs Snowflake

**Databricks** (as calculated above):
- Year 1: $22,170/month average ($266,040 annual)
- Optimized: $10,450/month with aggressive cost management

**Snowflake** (for same workload):
- Storage: 100TB × $23/TB = $2,300/month
- Training Compute: 3X-Large warehouse (128 credits/hour) × 10 hours/day × $3/credit × 30 days = $11,520/month
- Interactive Compute: Large warehouse (32 credits/hour) × 12 hours/day × $3/credit × 30 days = $3,456/month
- Serving Compute: Small warehouse (1 credit/hour) × 24 hours/day × $3/credit × 30 days = $2,160/month
- Ingestion: $1,500/month (Fivetran)
- BI: $2,000/month (Looker)
- Monitoring: $200/month
- **Total Snowflake**: $23,136/month (slightly higher than Databricks)

**Break-Even Analysis**:
- Databricks is cheaper at current scale ($22,170 vs $23,136)
- Snowflake becomes more competitive at lower usage (can pause warehouses; Databricks has platform fee overhead)
- Databricks scales better for ML workloads (Photon, GPU support, Feature Store reduce costs at scale)
- **Verdict**: Databricks offers better TCO for this Python-heavy, ML-centric use case

---

## 7. Migration & Onboarding

### Current State Assessment

**Existing Architecture**:
- **Data Storage**: 100TB in S3 Parquet files (inconsistent partitioning, no ACID guarantees)
- **Feature Engineering**: 50+ Jupyter notebooks on data scientist laptops and shared EC2 instances
- **Compute**: EMR clusters (10-node cluster, i3.xlarge instances) running PySpark jobs
- **Cost**: ~$6,000/month for EMR, ~$2,300/month for S3, ~$500/month for EC2 notebook servers
- **Pain Points**: No feature versioning, duplicate feature logic, slow iteration cycles, high EMR management overhead

**Migration Scope**:
- 50+ feature engineering notebooks (Python/PySpark)
- 15 ML model training pipelines
- 100TB historical data (2 years of events)
- 40 users (data scientists, ML engineers, analysts)
- 5 data ingestion pipelines (Kafka, Fivetran, custom scripts)

### Migration Complexity Assessment

**Complexity: Medium**

**Factors Increasing Complexity**:
- 50+ notebooks require code migration (EMR PySpark → Databricks PySpark)
- Feature definitions scattered across projects (no central registry)
- Inconsistent S3 Parquet schemas requiring data cleanup
- Training data recreation requires backfilling historical features

**Factors Reducing Complexity**:
- Team already proficient in PySpark (minimal retraining needed)
- Data already in S3 (no cloud migration, can read existing Parquet in-place)
- Databricks PySpark API nearly identical to EMR (90% code compatibility)
- No production SLA during migration (can run parallel systems)

### Migration Timeline and Steps

**Pre-Migration (Week 0): Planning and Preparation**

*Assessment*:
- Inventory all 50+ feature engineering notebooks; categorize by priority (critical, important, low-priority)
- Analyze EMR job logs to understand compute requirements (cluster size, runtime, frequency)
- Identify feature dependencies (which features depend on other features?)
- Document current data quality issues and schema inconsistencies

*Planning*:
- Create migration project plan with milestones and success criteria
- Define rollback plan if critical issues discovered during migration
- Set up communication plan (weekly updates to stakeholders, daily standups for migration team)
- Allocate resources: 1 data engineer (full-time), 2 data scientists (50% time), 1 ML engineer (25% time)

**Phase 1 (Week 1-2): Parallel Environment Setup**

*Databricks Workspace*:
- Create production workspace and Unity Catalog (following Phase 1 implementation guide)
- Configure cluster policies mirroring current EMR cluster sizes (baseline: 10 nodes, i3.xlarge)
- Import sample notebooks from Git repositories into Databricks workspace
- Set up user access for 5 pilot users (early adopters from each team)

*Data Access*:
- Configure Databricks to read existing S3 Parquet data (Bronze layer points to current S3 paths)
- Validate data readability: query 1 month of events, compare row counts with EMR
- Create Delta Lake Silver tables for critical datasets (users, orders, events)
- Run one-time CONVERT TO DELTA on existing Parquet tables for ACID guarantees

**Phase 2 (Week 3-6): Pilot Migration**

*Feature Pipeline Migration*:
- Migrate 10 critical feature engineering notebooks (highest business value, daily usage)
- Code changes required:
  - Update Spark session initialization (EMR uses custom config, Databricks auto-configured)
  - Replace `s3a://` paths with Delta table references
  - Add Feature Store registration calls for computed features
  - Update Airflow DAGs to trigger Databricks jobs instead of EMR steps
- Run parallel pipelines: EMR version + Databricks version for 2 weeks

*Validation*:
- Compare feature outputs between EMR and Databricks for 1000 random customers
- Acceptable variance: <0.1% difference (floating-point precision acceptable)
- Track performance: Databricks should match or exceed EMR runtimes
- User acceptance testing: 5 pilot users run daily workflows on Databricks

*Issues and Resolutions* (observed in typical migrations):
- Issue: Custom Python UDFs with native dependencies fail on Databricks
  - Resolution: Install dependencies via cluster init scripts or use Databricks ML Runtime with pre-installed packages
- Issue: Different Spark version causes behavior changes (EMR Spark 3.2 vs Databricks Runtime 11.x)
  - Resolution: Pin Databricks Runtime version matching EMR Spark version for consistency
- Issue: S3 read performance slower than EMR (different IAM role configuration)
  - Resolution: Configure Databricks instance profiles with S3 read optimization settings

**Phase 3 (Week 7-8): Full Migration**

*Remaining Pipelines*:
- Migrate remaining 40 notebooks in batches of 10/week
- Prioritize by usage frequency: high-traffic features first, experimental notebooks last
- Update documentation with Databricks notebook URLs and Feature Store catalog
- Archive old EMR notebooks in Git with "DEPRECATED" tags

*Training Dataset Recreation*:
- Backfill feature tables for 2 years of history (required for model reproducibility)
- Use Databricks batch jobs to compute historical features from Bronze event data
- Register backfilled features in Feature Store with historical timestamps
- Validate: recreate 3 production models using new training datasets, compare metrics

**Phase 4 (Week 9-10): Cutover and Decommissioning**

*Go-Live*:
- Redirect all Airflow DAGs to Databricks jobs (disable EMR step triggers)
- Monitor closely for 1 week: check job success rates, query performance, user feedback
- Establish on-call rotation for migration support (respond to issues within 2 hours)

*EMR Decommission*:
- Terminate EMR clusters after 1 week of stable Databricks operation
- Archive EMR logs and cluster configurations to S3 for historical reference
- Update infrastructure-as-code (Terraform) to remove EMR resources
- **Cost Savings**: Eliminate $6,000/month EMR costs (offset by $18,470 Databricks, net increase $12,470 but with significantly better capabilities)

*Knowledge Transfer*:
- Conduct post-migration retrospective (what went well, what to improve)
- Document lessons learned for future migrations (common pitfalls, workarounds)
- Celebrate success with team (migration complete, faster iteration cycles enabled)

### Onboarding Plan

**Week 1: Foundation Training**

*Data Scientists (15 users)*:
- 4-hour hands-on workshop: Databricks notebooks, Feature Store SDK, PySpark API differences
- Exercise 1: Convert existing notebook from EMR to Databricks
- Exercise 2: Register feature in Feature Store and use in training pipeline
- Exercise 3: Query Feature Store programmatically for model training

*ML Engineers (8 users)*:
- 3-hour workshop: Databricks Workflows, cluster configuration, cost optimization
- Exercise 1: Create Databricks job from notebook with schedule and dependencies
- Exercise 2: Configure job cluster with GPU support for model training
- Exercise 3: Monitor job runs and debug failures using job logs

*Analytics Engineers (4 users)*:
- 2-hour workshop: Databricks SQL, Unity Catalog permissions, dashboard creation
- Exercise 1: Write SQL query on Delta tables and create visualization
- Exercise 2: Build dashboard using Databricks SQL editor
- Exercise 3: Grant table access to team members using Unity Catalog

**Week 2-4: Hands-On Support**

- **Office Hours**: 2 hours/day for first 2 weeks (drop-in support for migration questions)
- **Pair Programming**: Senior data engineer pairs with each team member to migrate first notebook
- **Slack Channel**: #databricks-migration for asynchronous questions and knowledge sharing
- **Documentation**: Create internal wiki with FAQs, best practices, and troubleshooting guide

**Month 2-3: Advanced Topics**

- **Advanced Feature Engineering**: Window functions, streaming features, complex joins
- **Cost Optimization**: Cluster sizing, spot instances, auto-termination policies
- **MLOps Patterns**: Model deployment, monitoring, A/B testing with Feature Store

### Change Management

**Stakeholder Communication**:
- **Executives**: Monthly updates on migration progress, cost impact, business benefits
- **Data Science Team**: Weekly demos of new capabilities (Feature Store, faster queries, collaboration features)
- **IT/Security**: Unity Catalog governance, audit logging, compliance validation

**Adoption Incentives**:
- **Quick Wins**: Showcase successful pilot migrations with 2x faster query performance
- **Ease of Use**: Emphasize Python-native workflow (no context switching to SQL)
- **Collaboration**: Highlight notebook sharing and version control features

**Resistance Mitigation**:
- Common concern: "EMR works fine, why change?"
  - Response: Demonstrate feature versioning solving reproducibility pain, 60% reduction in data prep time
- Common concern: "Will my code break?"
  - Response: Provide migration guide showing 90% code compatibility, offer pair programming support

### Common Pitfalls and Mitigation

**Pitfall 1: Underestimating Backfill Time**
- **Risk**: Backfilling 2 years of features on 100TB data takes weeks, delays migration
- **Mitigation**: Start backfill early in Phase 2; run incrementally (1 month at a time); prioritize critical features

**Pitfall 2: Cost Overruns During Migration**
- **Risk**: Running parallel EMR + Databricks doubles compute costs temporarily
- **Mitigation**: Shut down non-critical EMR jobs during migration; use spot instances for Databricks backfill jobs; set DBU budget alerts

**Pitfall 3: User Resistance to New Tooling**
- **Risk**: Data scientists prefer familiar EMR environment, slow Databricks adoption
- **Mitigation**: Identify 5 early adopter champions; showcase productivity gains in team meetings; provide generous support during transition

**Pitfall 4: Schema Inconsistencies in Historical Data**
- **Risk**: S3 Parquet files have schema evolution issues breaking backfill jobs
- **Mitigation**: Use Databricks Autoloader schema inference and evolution; implement schema enforcement in Silver layer; clean up Bronze data before Delta conversion

**Pitfall 5: Performance Regressions**
- **Risk**: Databricks queries slower than EMR for certain workloads
- **Mitigation**: Enable Photon engine; optimize table partitioning and Z-ordering; right-size clusters based on workload profiling; cache frequently accessed tables

---

## 8. Risks & Mitigations

### Technical Risks

**Risk 1: Performance Degradation on Large Queries**
- **Description**: Feature engineering queries on 10TB datasets exceed 2-hour SLA target
- **Likelihood**: Medium (30%)
- **Impact**: High (blocks model training, delays experiments)
- **Mitigation**:
  - Pre-optimization: Run performance benchmarks on sample datasets before migration
  - Design: Implement proper partitioning (by date) and Z-ordering (by frequently filtered columns)
  - Monitoring: Set up query performance monitoring with alerts for slow queries (>2 hours)
  - Response: Databricks support engagement for query optimization assistance (included in platform)
  - Fallback: Increase cluster size for critical jobs (cost vs. performance tradeoff)

**Risk 2: DBU Cost Overruns**
- **Description**: Actual DBU consumption exceeds $25K/month budget due to inefficient queries or unexpected usage
- **Likelihood**: Medium-High (40%)
- **Impact**: High (budget overruns require stakeholder escalation)
- **Mitigation**:
  - Prevention: Implement cluster policies limiting max cluster size, enforcing auto-termination
  - Monitoring: Daily DBU consumption dashboards by team and project; budget alerts at 80% threshold
  - Governance: Monthly cost review meetings identifying top DBU consumers; optimization action items
  - Controls: Require manager approval for XL+ clusters; peer review for long-running jobs
  - Education: Cost optimization training for all users (spot instances, query optimization techniques)

**Risk 3: Feature Store Adoption Resistance**
- **Description**: Data scientists continue creating ad-hoc feature code instead of using centralized Feature Store
- **Likelihood**: Medium (35%)
- **Impact**: Medium (undermines reproducibility and reuse goals)
- **Mitigation**:
  - Incentives: Make Feature Store registration mandatory for production models (enforced in code review)
  - Ease of Use: Provide Python SDK templates and cookbooks for common feature patterns
  - Champions: Identify early adopters who demonstrate Feature Store benefits in team demos
  - Process: Update ML project checklist to include feature registration as required step
  - Tracking: Monitor Feature Store usage metrics; celebrate teams with highest reuse rates

**Risk 4: Data Quality Issues in Migration**
- **Description**: Bugs in migrated feature code produce incorrect feature values, causing model performance degradation
- **Likelihood**: Medium (30%)
- **Impact**: Critical (bad predictions impact customer-facing products)
- **Mitigation**:
  - Validation: Run parallel EMR + Databricks pipelines for 2 weeks comparing outputs
  - Testing: Implement Great Expectations data quality tests on all feature tables
  - Reconciliation: Automated nightly jobs compare Databricks vs EMR outputs; alert on >0.1% variance
  - Rollback: Maintain EMR environment for 1 month post-migration as fallback
  - Monitoring: Track model performance metrics post-migration; investigate any degradation immediately

### Business Risks

**Risk 5: Vendor Lock-In to Databricks**
- **Description**: Heavy investment in Databricks-specific features (Feature Store, Unity Catalog) makes switching costly
- **Likelihood**: High (60% - intentional choice for productivity gains)
- **Impact**: Medium (limits future flexibility, exposes to pricing changes)
- **Mitigation**:
  - Abstraction: Use open formats (Delta Lake = open source, Parquet underneath)
  - Portability: Store raw data in S3 (not Databricks-managed storage); can be read by other tools
  - Alternatives: Maintain awareness of alternatives (Snowflake, BigQuery) for leverage in pricing negotiations
  - Contracts: Negotiate multi-year pricing agreements with annual price caps
  - Hybrid: Keep critical workloads portable (e.g., inference doesn't depend on Databricks runtime)

**Risk 6: Team Capacity Constraints**
- **Description**: Migration competes with product roadmap work; insufficient engineering time to complete in 10 weeks
- **Likelihood**: Medium (35%)
- **Impact**: Medium (delays migration, extends dual-cost period)
- **Mitigation**:
  - Planning: Obtain executive buy-in for resource allocation (1 FTE data engineer dedicated to migration)
  - Contractors: Budget for 1-2 contract data engineers if internal capacity insufficient
  - Prioritization: Defer non-critical feature development during migration (focus on P0 pipelines only)
  - Pilot: Start with 10 critical notebooks; defer long-tail notebooks to Phase 4 (post-migration iteration)
  - Tooling: Invest in automation (notebook conversion scripts, automated testing) to reduce manual effort

**Risk 7: Integration Failures with Existing Systems**
- **Description**: Databricks integration with SageMaker, MLflow, or real-time inference services fails or has unacceptable latency
- **Likelihood**: Low (15%)
- **Impact**: High (blocks production model deployment)
- **Mitigation**:
  - Proof of Concept: Test critical integrations (SageMaker, MLflow) in pilot phase before full migration
  - Architecture Review: Databricks Solutions Architect reviews integration design pre-migration
  - Testing: End-to-end integration tests for model training → deployment → inference workflows
  - Fallback: Maintain ability to train models on EMR if Databricks integration doesn't meet requirements
  - Vendor Support: Escalation path to Databricks technical account manager for integration issues

**Risk 8: Security and Compliance Gaps**
- **Description**: Databricks configuration doesn't meet SOC 2, GDPR, or PII protection requirements
- **Likelihood**: Low (20%)
- **Impact**: Critical (blocks production use, compliance violations)
- **Mitigation**:
  - Pre-Assessment: Security team reviews Databricks architecture before migration kickoff
  - Configuration: Enable all security features (encryption at rest/in transit, audit logging, IP whitelisting)
  - Compliance: Leverage Databricks SOC 2 Type II certification; review Unity Catalog for GDPR compliance
  - Testing: Penetration testing and compliance audit post-migration before production cutover
  - Documentation: Maintain compliance documentation for auditors (access controls, data lineage, audit logs)

### Mitigation Matrix

| Risk | Likelihood | Impact | Priority | Mitigation Strategy | Owner | Status |
|------|------------|--------|----------|---------------------|-------|--------|
| Performance Degradation | Medium | High | P1 | Benchmarking, partitioning, monitoring | Data Engineer | Pre-migration |
| DBU Cost Overruns | Medium-High | High | P1 | Policies, dashboards, governance | Finance + Engineering | Ongoing |
| Feature Store Adoption | Medium | Medium | P2 | Champions, templates, process | ML Platform Lead | Post-migration |
| Data Quality Issues | Medium | Critical | P0 | Parallel runs, validation, testing | Data Engineer | During migration |
| Vendor Lock-In | High | Medium | P2 | Open formats, S3 storage, contracts | Engineering Director | Strategic |
| Team Capacity | Medium | Medium | P2 | Resource allocation, contractors | Engineering Manager | Pre-migration |
| Integration Failures | Low | High | P1 | PoC testing, vendor support | ML Engineer | Pilot phase |
| Compliance Gaps | Low | Critical | P0 | Security review, audit logging | Security Team | Pre-migration |

**Priority Legend**:
- **P0**: Showstopper, blocks migration
- **P1**: Critical, high attention required
- **P2**: Important, monitor and manage

---

## 9. Success Metrics

### 30-Day Success Metrics (Post-Migration)

**Technical Metrics**:
- ✅ **Data Pipeline Health**: 95%+ success rate for all feature engineering jobs (measured via Databricks job monitoring)
- ✅ **Query Performance**: p95 query latency for 1TB scans <30 minutes (10TB scans <2 hours)
- ✅ **Data Freshness**: Event data available in Delta Lake within 15 minutes of ingestion (p95)
- ✅ **System Uptime**: 99.5%+ availability during business hours (9am-6pm PT, Mon-Fri)

**Adoption Metrics**:
- ✅ **User Onboarding**: 40/40 users (100%) successfully logged into Databricks and run at least one query
- ✅ **Feature Store**: 20+ features registered in Feature Store with metadata (description, owner, refresh schedule)
- ✅ **Notebook Migration**: 10 critical feature engineering notebooks migrated and running in production
- ✅ **Model Training**: 2 ML models successfully trained using Databricks + Feature Store + MLflow integration

**Cost Metrics**:
- ✅ **Budget Compliance**: Monthly DBU consumption <$12,000/month (within $25K total budget)
- ✅ **Cost Per Query**: Baseline established for average cost per feature engineering query (DBUs consumed)
- ✅ **EMR Decommission**: EMR clusters terminated, saving $6,000/month

**Business Impact**:
- ✅ **Engineering Time Savings**: Data engineers report 50% reduction in time spent on "can you pull this data?" requests
- ✅ **Iteration Speed**: Data scientists report 30% faster feature experimentation cycle (idea → code → results)

### 90-Day Success Metrics

**Technical Excellence**:
- ✅ **Full Migration Complete**: 50/50 feature engineering notebooks migrated from EMR to Databricks
- ✅ **Feature Coverage**: 50+ features registered in Feature Store covering all active ML projects
- ✅ **Performance Optimized**: 80% of queries complete within SLA targets (1TB/30min, 10TB/2hr)
- ✅ **Data Quality**: Zero data quality incidents (measured by Great Expectations test failures impacting production models)
- ✅ **Reproducibility**: 100% of new production models have versioned training datasets in Feature Store

**Operational Maturity**:
- ✅ **Monitoring Coverage**: Dashboards tracking pipeline health, query performance, DBU consumption, feature drift
- ✅ **Incident Response**: Mean time to resolution (MTTR) for data pipeline failures <2 hours
- ✅ **Cost Optimization**: Implemented 3+ quick-win optimizations (spot instances, auto-termination, caching) reducing costs by 10-15%
- ✅ **Documentation**: Internal wiki with 20+ pages covering common tasks, troubleshooting, best practices

**User Adoption**:
- ✅ **Daily Active Users**: 30+ users querying Databricks daily (75% of total user base)
- ✅ **Self-Service Analytics**: 80% reduction in ad-hoc data requests to data engineering team
- ✅ **Collaboration**: 10+ notebooks shared across teams (evidence of cross-team feature reuse)
- ✅ **Advanced Features**: 5+ users actively using Delta Lake time-travel for debugging or dataset recreation

**Business Outcomes**:
- ✅ **Model Velocity**: 20% increase in number of models deployed to production (faster iteration)
- ✅ **Feature Reuse**: 30% of new models use existing features from Feature Store (reduced duplication)
- ✅ **Data Scientist Productivity**: Data scientists spend 40% of time on modeling (up from 25%) and 60% on data prep (down from 75%)

### 12-Month Success Metrics

**Strategic Goals**:
- ✅ **Feature Store as Standard**: 100% of new production models use Feature Store for feature management
- ✅ **Platform Adoption**: Databricks is primary analytics platform for all data science and ML engineering work
- ✅ **Cost Predictability**: Monthly DBU costs within 10% variance month-over-month (seasonal patterns understood and managed)
- ✅ **Performance at Scale**: Query performance maintained as data grows to 130TB (25% growth from 100TB baseline)

**Organizational Impact**:
- ✅ **Team Growth**: Onboarded 10+ new data scientists/ML engineers to Databricks with <2 week ramp-up time
- ✅ **Knowledge Base**: 50+ internal documentation articles, 20+ reusable notebook templates
- ✅ **Training Program**: Formalized onboarding curriculum for new hires (1-week Databricks bootcamp)
- ✅ **Community of Practice**: Monthly Databricks office hours with 60%+ attendance, active Slack channel

**Advanced Capabilities**:
- ✅ **Streaming Features**: 5+ real-time features deployed using Structured Streaming (sub-15-minute freshness)
- ✅ **AutoML Adoption**: 10+ experiments run using Databricks AutoML for rapid prototyping
- ✅ **A/B Testing Integration**: Feature flags integrated with Feature Store for controlled rollouts
- ✅ **Model Monitoring**: Automated drift detection and alerting for 30+ production models

**Business Value**:
- ✅ **ROI Demonstration**: Documented 3x ROI based on:
  - Engineering time savings: $200K/year (reduced manual data wrangling)
  - Model velocity improvement: 20% more models deployed → estimated $500K revenue impact
  - Infrastructure cost reduction: EMR decommission + optimization = $50K/year savings
  - Total benefits: $750K vs. $320K platform cost = 2.3x ROI
- ✅ **Customer Impact**: Improved model performance (measured by prediction accuracy, latency) drives 10% increase in customer satisfaction scores
- ✅ **Competitive Advantage**: Faster experimentation cycles enable launch of 3 new ML-powered product features ahead of competitors

**Risk Reduction**:
- ✅ **Reproducibility**: Zero incidents of "can't recreate training dataset" issues (historical problem eliminated)
- ✅ **Compliance**: Successful SOC 2 Type II audit with Databricks platform, no findings related to data infrastructure
- ✅ **Business Continuity**: Disaster recovery tested (restore from S3 backups to new Databricks workspace in <4 hours)

---

## Summary

This S3 scenario demonstrates that **Databricks is the optimal data warehouse choice for VectorAI's ML feature store use case**, delivering Python-native workflows, lakehouse architecture, and ML-first capabilities that directly address the company's critical challenges around feature engineering, reproducibility, and model training performance.

**Key Decision Factors**:
1. **Python-First**: Native PySpark and Feature Store SDK eliminate context switching for Python-heavy data science team
2. **Lakehouse Architecture**: Delta Lake on S3 provides unified platform for ML and analytics, eliminating data movement
3. **ML Integration**: Built-in Feature Store, MLflow, and GPU support accelerate model development lifecycle
4. **Performance**: Photon engine and optimized Spark execution deliver 1TB scans in <30 minutes, 10TB in <2 hours
5. **Cost**: $22,170/month within budget, with clear path to $10,450/month through optimization strategies

**Implementation Path**: 10-week migration from EMR to Databricks with medium complexity, delivering immediate productivity gains (60% reduction in data prep time) and long-term strategic benefits (centralized feature store, reproducible training datasets, faster experimentation cycles).

**Expected ROI**: 2.3x return on investment through engineering time savings ($200K/year), model velocity improvements ($500K revenue impact), and infrastructure cost reduction ($50K/year), while eliminating critical reproducibility and feature duplication pain points.

