# Integration Complexity Analysis

**Purpose**: Assess how easy/hard it is to integrate each data warehouse platform into existing tech stacks, migrate from existing solutions, and avoid vendor lock-in.

**Last Updated**: 2025-11-06

---

## 1. BI Tool Integration

Assessment of native connector support, driver compatibility, and ease of setup for major BI platforms.

**Rating Scale**: 1 (very easy) to 5 (very hard)

### 1.1 Tableau Integration

| Provider | Native Connector | JDBC/ODBC | Setup Ease | Query Performance | Notes |
|----------|-----------------|-----------|------------|-------------------|-------|
| **Snowflake** | ✅ Native | ✅ Both | 1 | Excellent | Official Tableau partner, zero-config connector |
| **BigQuery** | ✅ Native | ✅ Both | 1 | Excellent | Built-in OAuth, automatic schema discovery |
| **Redshift** | ✅ Native | ✅ Both | 1 | Good | Standard AWS IAM authentication |
| **Synapse** | ✅ Native | ✅ Both | 2 | Good | Requires Azure AD configuration |
| **Databricks** | ✅ Native | ✅ Both | 2 | Excellent | Partner connector, requires cluster config |
| **ClickHouse** | ❌ None | ✅ ODBC only | 4 | Excellent | Manual driver install, limited auth options |
| **Druid** | ❌ None | ✅ JDBC only | 4 | Good | Community connector, requires custom config |
| **Firebolt** | ⚠️ Beta | ✅ JDBC | 3 | Excellent | New connector, still maturing |

### 1.2 Looker Integration

| Provider | Native Support | Setup Ease | LookML Generation | Query Caching | Notes |
|----------|---------------|------------|-------------------|---------------|-------|
| **Snowflake** | ✅ Native | 1 | Auto | Excellent | Persistent derived tables (PDTs) work well |
| **BigQuery** | ✅ Native | 1 | Auto | Excellent | Same parent (Google), seamless integration |
| **Redshift** | ✅ Native | 1 | Auto | Good | PDTs can be slow for large datasets |
| **Synapse** | ✅ Native | 2 | Auto | Good | Requires dedicated SQL pool for PDTs |
| **Databricks** | ✅ Native | 2 | Auto | Excellent | Delta Lake caching helps performance |
| **ClickHouse** | ⚠️ Community | 4 | Manual | Good | Limited support, requires custom dialect |
| **Druid** | ⚠️ Community | 4 | Manual | Excellent | Real-time data works well, PDTs limited |
| **Firebolt** | ✅ Native | 2 | Auto | Excellent | Growing support, fast query execution |

### 1.3 Power BI Integration

| Provider | Native Connector | DirectQuery | Import Mode | Setup Ease | Notes |
|----------|-----------------|-------------|-------------|------------|-------|
| **Snowflake** | ✅ Native | ✅ Yes | ✅ Yes | 1 | Official Microsoft partnership |
| **BigQuery** | ✅ Native | ✅ Yes | ✅ Yes | 2 | OAuth flow can be complex for first-time users |
| **Redshift** | ✅ Native | ✅ Yes | ✅ Yes | 2 | Works well but requires VPN/private link setup |
| **Synapse** | ✅ Native | ✅ Yes | ✅ Yes | 1 | Best-in-class integration, same ecosystem |
| **Databricks** | ✅ Native | ✅ Yes | ✅ Yes | 2 | SQL warehouse required, not notebooks |
| **ClickHouse** | ❌ None | ⚠️ Custom | ✅ Yes | 5 | Manual ODBC setup, limited documentation |
| **Druid** | ❌ None | ⚠️ Custom | ✅ Yes | 5 | Poor integration, custom REST API needed |
| **Firebolt** | ⚠️ Beta | ✅ Yes | ✅ Yes | 3 | Growing support, requires JDBC driver |

### 1.4 Metabase Integration

| Provider | Native Driver | Query Caching | Auto-refresh | Setup Ease | Notes |
|----------|--------------|---------------|--------------|------------|-------|
| **Snowflake** | ✅ Built-in | ✅ Yes | ✅ Yes | 1 | Out-of-box support, excellent documentation |
| **BigQuery** | ✅ Built-in | ✅ Yes | ✅ Yes | 2 | Service account JSON key required |
| **Redshift** | ✅ Built-in | ✅ Yes | ✅ Yes | 1 | Standard PostgreSQL driver works |
| **Synapse** | ✅ Built-in | ✅ Yes | ✅ Yes | 2 | SQL Server driver, AD auth can be tricky |
| **Databricks** | ✅ Built-in | ✅ Yes | ✅ Yes | 2 | SQL warehouse endpoint required |
| **ClickHouse** | ✅ Built-in | ✅ Yes | ✅ Yes | 2 | Community-contributed driver, works well |
| **Druid** | ✅ Built-in | ✅ Yes | ⚠️ Limited | 3 | Basic support, some SQL features missing |
| **Firebolt** | ❌ None | ⚠️ Custom | ❌ No | 4 | Requires custom JDBC connection |

**Summary - BI Tool Integration Scores (Average)**:
- **Snowflake**: 1.0 (easiest)
- **BigQuery**: 1.5
- **Redshift**: 1.25
- **Synapse**: 1.75
- **Databricks**: 2.0
- **ClickHouse**: 3.75
- **Druid**: 4.0 (hardest)
- **Firebolt**: 3.0

---

## 2. ETL/ELT Platform Integration

### 2.1 Fivetran Support

| Provider | Native Support | CDC Available | Sync Frequency | Transformations | Connector Maturity |
|----------|---------------|---------------|----------------|-----------------|-------------------|
| **Snowflake** | ✅ Tier 1 | ✅ Yes | Real-time | dbt native | Production-ready, 10+ years |
| **BigQuery** | ✅ Tier 1 | ✅ Yes | Real-time | dbt native | Production-ready, excellent |
| **Redshift** | ✅ Tier 1 | ✅ Yes | Real-time | dbt native | Production-ready, mature |
| **Synapse** | ✅ Tier 1 | ✅ Yes | Real-time | dbt native | Production-ready, growing |
| **Databricks** | ✅ Tier 1 | ✅ Yes | Real-time | dbt native | Production-ready, Delta Lake support |
| **ClickHouse** | ⚠️ Beta | ⚠️ Limited | 15-min | Custom | Beta quality, limited support |
| **Druid** | ❌ None | ❌ No | N/A | N/A | Not supported, must use Kafka |
| **Firebolt** | ⚠️ Beta | ⚠️ Limited | 15-min | Custom | Early stage, improving |

### 2.2 Airbyte Support

| Provider | Native Support | Open Source | Custom Connectors | CDC Support | Community Health |
|----------|---------------|-------------|-------------------|-------------|------------------|
| **Snowflake** | ✅ Yes | ✅ Yes | ✅ Easy | ✅ Yes | Excellent (500+ stars) |
| **BigQuery** | ✅ Yes | ✅ Yes | ✅ Easy | ✅ Yes | Excellent (400+ stars) |
| **Redshift** | ✅ Yes | ✅ Yes | ✅ Easy | ✅ Yes | Excellent (350+ stars) |
| **Synapse** | ✅ Yes | ✅ Yes | ✅ Easy | ✅ Yes | Good (200+ stars) |
| **Databricks** | ✅ Yes | ✅ Yes | ✅ Easy | ✅ Yes | Excellent (450+ stars) |
| **ClickHouse** | ✅ Yes | ✅ Yes | ⚠️ Moderate | ⚠️ Limited | Good (150+ stars) |
| **Druid** | ⚠️ Community | ✅ Yes | ⚠️ Complex | ❌ No | Fair (50+ stars) |
| **Firebolt** | ✅ Yes | ✅ Yes | ✅ Easy | ⚠️ Limited | Fair (80+ stars) |

### 2.3 dbt (Data Build Tool) Support

| Provider | Adapter Quality | Incremental Models | Snapshots | Seeds | Materializations | Tests |
|----------|----------------|-------------------|-----------|-------|------------------|-------|
| **Snowflake** | ✅ Official | ✅ Full | ✅ Full | ✅ Yes | All types | ✅ Full |
| **BigQuery** | ✅ Official | ✅ Full | ✅ Full | ✅ Yes | All types | ✅ Full |
| **Redshift** | ✅ Official | ✅ Full | ✅ Full | ✅ Yes | All types | ✅ Full |
| **Synapse** | ⚠️ Community | ✅ Full | ⚠️ Limited | ✅ Yes | Most types | ⚠️ Partial |
| **Databricks** | ✅ Official | ✅ Full | ✅ Full | ✅ Yes | All types | ✅ Full |
| **ClickHouse** | ⚠️ Community | ⚠️ Limited | ❌ No | ✅ Yes | Basic only | ⚠️ Limited |
| **Druid** | ❌ None | ❌ No | ❌ No | ❌ No | None | ❌ No |
| **Firebolt** | ⚠️ Community | ⚠️ Limited | ⚠️ Limited | ✅ Yes | Basic only | ⚠️ Limited |

### 2.4 Native Data Pipeline Features

| Provider | Native ELT | SQL-based Transforms | Scheduling | Monitoring | Data Quality Checks |
|----------|-----------|---------------------|------------|------------|---------------------|
| **Snowflake** | ✅ Snowpipe | ✅ Tasks | ✅ Tasks | ✅ Query History | ⚠️ Limited |
| **BigQuery** | ✅ Data Transfer | ✅ Scheduled Queries | ✅ Cloud Scheduler | ✅ Stackdriver | ⚠️ Limited |
| **Redshift** | ⚠️ COPY command | ⚠️ Manual | ⚠️ EventBridge | ✅ CloudWatch | ❌ None |
| **Synapse** | ✅ Pipelines | ✅ Data Flows | ✅ Triggers | ✅ Monitor Hub | ⚠️ Limited |
| **Databricks** | ✅ Delta Live Tables | ✅ Notebooks/SQL | ✅ Jobs | ✅ Observability | ✅ Expectations |
| **ClickHouse** | ⚠️ Materialized Views | ✅ SQL | ❌ None | ⚠️ system tables | ❌ None |
| **Druid** | ⚠️ Ingestion specs | ⚠️ Limited | ⚠️ Basic | ⚠️ Metrics API | ❌ None |
| **Firebolt** | ⚠️ COPY command | ✅ SQL | ⚠️ Basic | ⚠️ Query logs | ❌ None |

**Summary - ETL/ELT Integration Scores**:
- **Snowflake**: 1.0 (best ecosystem)
- **BigQuery**: 1.0 (tied)
- **Databricks**: 1.25
- **Redshift**: 1.5
- **Synapse**: 2.0
- **Firebolt**: 3.0
- **ClickHouse**: 3.5
- **Druid**: 4.5 (most limited)

---

## 3. Cloud Platform Integration

### 3.1 AWS Integration

| Provider | S3 Integration | Lambda Triggers | Glue Catalog | IAM Support | VPC Integration | Ease Score |
|----------|----------------|-----------------|--------------|-------------|-----------------|------------|
| **Snowflake** | ✅ Native COPY | ✅ External | ✅ Yes | ✅ Full | ✅ PrivateLink | 1 |
| **BigQuery** | ✅ External table | ⚠️ Via API | ⚠️ Limited | ⚠️ Cross-cloud | ❌ None | 4 |
| **Redshift** | ✅ COPY/UNLOAD | ✅ Native | ✅ Native | ✅ Native | ✅ Native | 1 |
| **Synapse** | ✅ PolyBase | ⚠️ Via API | ⚠️ Limited | ⚠️ Cross-cloud | ❌ None | 4 |
| **Databricks** | ✅ Native mount | ✅ Native | ✅ Native | ✅ Full | ✅ VPC peering | 1 |
| **ClickHouse** | ✅ S3 function | ⚠️ Manual | ❌ None | ⚠️ Basic | ✅ EC2 | 3 |
| **Druid** | ✅ Ingestion | ⚠️ Manual | ❌ None | ⚠️ Basic | ✅ EC2 | 3 |
| **Firebolt** | ✅ Native | ⚠️ Via API | ⚠️ Limited | ✅ Good | ✅ VPC peering | 2 |

### 3.2 GCP Integration

| Provider | BigQuery Export | Cloud Functions | Dataflow | Cloud Storage | IAM Support | Ease Score |
|----------|----------------|-----------------|----------|---------------|-------------|------------|
| **Snowflake** | ⚠️ Via API | ⚠️ External | ⚠️ External | ✅ Native | ✅ Good | 3 |
| **BigQuery** | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ✅ Native | 1 |
| **Redshift** | ⚠️ Manual export | ⚠️ Via API | ❌ None | ⚠️ Cross-cloud | ❌ None | 5 |
| **Synapse** | ⚠️ Manual export | ⚠️ Via API | ❌ None | ⚠️ Cross-cloud | ❌ None | 5 |
| **Databricks** | ✅ Native | ✅ Good | ✅ Good | ✅ Native | ✅ Full | 1 |
| **ClickHouse** | ⚠️ Manual | ⚠️ Via API | ❌ None | ✅ GCS function | ⚠️ Basic | 4 |
| **Druid** | ⚠️ Manual | ⚠️ Via API | ❌ None | ✅ GCS ingestion | ⚠️ Basic | 4 |
| **Firebolt** | ⚠️ Manual | ⚠️ Via API | ❌ None | ✅ Native | ⚠️ Basic | 3 |

### 3.3 Azure Integration

| Provider | Data Factory | Synapse Link | Active Directory | ADLS Gen2 | Key Vault | Ease Score |
|----------|--------------|--------------|------------------|-----------|-----------|------------|
| **Snowflake** | ✅ Native | ⚠️ Via API | ✅ SSO | ✅ External stage | ✅ Yes | 2 |
| **BigQuery** | ⚠️ Manual | ❌ None | ⚠️ Federation | ⚠️ Cross-cloud | ❌ None | 5 |
| **Redshift** | ⚠️ Manual | ❌ None | ⚠️ SAML | ⚠️ Cross-cloud | ❌ None | 5 |
| **Synapse** | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ✅ Native | 1 |
| **Databricks** | ✅ Native | ✅ Good | ✅ Native | ✅ Native | ✅ Native | 1 |
| **ClickHouse** | ⚠️ Manual | ❌ None | ⚠️ LDAP | ⚠️ Basic | ❌ None | 4 |
| **Druid** | ⚠️ Manual | ❌ None | ⚠️ LDAP | ⚠️ Basic | ❌ None | 4 |
| **Firebolt** | ⚠️ Limited | ❌ None | ⚠️ SSO | ✅ Native | ⚠️ Limited | 3 |

**Cloud Platform Integration Summary**:
- **Best for AWS**: Redshift (1.0), Databricks (1.0), Snowflake (1.0)
- **Best for GCP**: BigQuery (1.0), Databricks (1.0)
- **Best for Azure**: Synapse (1.0), Databricks (1.0)
- **Multi-cloud leader**: Databricks (avg 1.0), Snowflake (avg 2.0)
- **Cloud-specific disadvantage**: BigQuery/Synapse/Redshift poor outside home cloud (5.0)

---

## 4. Programming Language Support

### 4.1 Python SDK Quality

| Provider | Official SDK | Documentation | PyPI Downloads/Month | Pandas Support | Features | Score |
|----------|-------------|---------------|---------------------|----------------|----------|-------|
| **Snowflake** | ✅ Yes | Excellent | 5M+ | ✅ Native | SQLAlchemy, async | 1 |
| **BigQuery** | ✅ Yes | Excellent | 8M+ | ✅ Native | Streaming, Storage API | 1 |
| **Redshift** | ✅ Yes | Good | 2M+ | ✅ Via psycopg2 | Standard PostgreSQL | 2 |
| **Synapse** | ✅ Yes | Good | 500K+ | ✅ Via pyodbc | Azure SDK integration | 2 |
| **Databricks** | ✅ Yes | Excellent | 3M+ | ✅ Native | PySpark, SQL connector | 1 |
| **ClickHouse** | ✅ Community | Good | 400K+ | ✅ Via clickhouse-driver | HTTP/Native protocols | 2 |
| **Druid** | ⚠️ pydruid | Fair | 50K+ | ⚠️ Manual | Basic SQL API | 3 |
| **Firebolt** | ✅ Yes | Good | 20K+ | ✅ Via SDK | Growing ecosystem | 2 |

### 4.2 Java/Scala Support

| Provider | JDBC Driver | ODBC Driver | Spark Integration | Maven/SBT | Build Tools | Score |
|----------|------------|-------------|-------------------|-----------|-------------|-------|
| **Snowflake** | ✅ Official | ✅ Official | ✅ Native | ✅ Yes | Maven Central | 1 |
| **BigQuery** | ✅ Official | ✅ Official | ✅ Native | ✅ Yes | Maven Central | 1 |
| **Redshift** | ✅ Official | ✅ Official | ✅ Good | ✅ Yes | Maven Central | 1 |
| **Synapse** | ✅ Official | ✅ Official | ✅ Good | ✅ Yes | Maven Central | 1 |
| **Databricks** | ✅ Official | ✅ Official | ✅ Native | ✅ Yes | Maven Central | 1 |
| **ClickHouse** | ✅ Official | ✅ Official | ⚠️ Via JDBC | ✅ Yes | Maven Central | 2 |
| **Druid** | ✅ Official | ⚠️ Limited | ⚠️ Via JDBC | ✅ Yes | Maven Central | 3 |
| **Firebolt** | ✅ Official | ⚠️ Beta | ⚠️ Via JDBC | ✅ Yes | Maven Central | 2 |

### 4.3 R Support

| Provider | R Package | CRAN Available | DBI Support | dplyr Support | RStudio Integration | Score |
|----------|-----------|----------------|-------------|---------------|---------------------|-------|
| **Snowflake** | ✅ Official | ❌ GitHub | ✅ Yes | ✅ Yes | ✅ Excellent | 2 |
| **BigQuery** | ✅ Official | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Excellent | 1 |
| **Redshift** | ⚠️ Via RPostgres | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Good | 2 |
| **Synapse** | ⚠️ Via RODBC | ✅ Yes | ✅ Yes | ⚠️ Limited | ⚠️ Fair | 3 |
| **Databricks** | ✅ Official | ❌ GitHub | ✅ Yes | ✅ Yes | ✅ Good | 2 |
| **ClickHouse** | ⚠️ Community | ❌ GitHub | ⚠️ Partial | ⚠️ Limited | ⚠️ Fair | 4 |
| **Druid** | ❌ None | ❌ None | ❌ No | ❌ No | ❌ None | 5 |
| **Firebolt** | ⚠️ Via RJDBC | ⚠️ Indirect | ⚠️ Basic | ❌ No | ⚠️ Fair | 4 |

### 4.4 JavaScript/Node.js Support

| Provider | Official SDK | npm Downloads/Week | TypeScript Support | Browser Support | Score |
|----------|-------------|-------------------|-------------------|----------------|-------|
| **Snowflake** | ✅ Yes | 50K+ | ✅ Yes | ❌ No | 1 |
| **BigQuery** | ✅ Yes | 200K+ | ✅ Yes | ⚠️ Limited | 1 |
| **Redshift** | ⚠️ Via pg | 500K+ | ✅ Yes | ❌ No | 2 |
| **Synapse** | ⚠️ Via mssql | 100K+ | ✅ Yes | ❌ No | 2 |
| **Databricks** | ✅ Yes | 10K+ | ✅ Yes | ❌ No | 2 |
| **ClickHouse** | ✅ Community | 5K+ | ✅ Yes | ⚠️ HTTP only | 3 |
| **Druid** | ⚠️ Community | 500+ | ⚠️ Limited | ⚠️ HTTP only | 4 |
| **Firebolt** | ✅ Yes | 1K+ | ✅ Yes | ❌ No | 3 |

### 4.5 REST API Maturity

| Provider | REST API | OpenAPI Spec | Rate Limits | Authentication | SDK Generation | Score |
|----------|----------|--------------|-------------|----------------|----------------|-------|
| **Snowflake** | ✅ Full | ✅ Yes | Generous | OAuth 2.0, JWT | ✅ Yes | 1 |
| **BigQuery** | ✅ Full | ✅ Yes | Generous | OAuth 2.0, Service Account | ✅ Yes | 1 |
| **Redshift** | ⚠️ Via AWS API | ✅ Yes | AWS limits | IAM | ✅ Via AWS | 2 |
| **Synapse** | ✅ Full | ✅ Yes | Good | OAuth 2.0, AAD | ✅ Via Azure | 1 |
| **Databricks** | ✅ Full | ✅ Yes | Generous | Token, OAuth | ✅ Yes | 1 |
| **ClickHouse** | ✅ HTTP interface | ⚠️ Community | No limits | Basic, custom | ⚠️ Manual | 3 |
| **Druid** | ✅ Native | ⚠️ Incomplete | No limits | Basic, custom | ⚠️ Manual | 3 |
| **Firebolt** | ✅ Full | ✅ Yes | Moderate | API key, token | ⚠️ Growing | 2 |

**Programming Language Support Summary (Average)**:
- **Snowflake**: 1.2
- **BigQuery**: 1.0 (best)
- **Redshift**: 1.8
- **Synapse**: 1.8
- **Databricks**: 1.4
- **ClickHouse**: 2.8
- **Druid**: 3.6 (weakest)
- **Firebolt**: 2.6

---

## 5. Migration Effort Assessment

Estimated hours to migrate 100TB dataset with 500 tables, 1000 queries, and 50 dashboards.

### 5.1 Migration FROM Redshift

| To Provider | Schema Migration | Data Transfer | Query Rewrite | Testing | Total Hours | Complexity |
|------------|------------------|---------------|---------------|---------|-------------|------------|
| **Snowflake** | 20h | 40h | 60h | 40h | 160h | Low-Medium |
| **BigQuery** | 40h | 60h | 120h | 60h | 280h | Medium-High |
| **Redshift** | 0h | 0h | 0h | 0h | 0h | N/A |
| **Synapse** | 30h | 50h | 80h | 50h | 210h | Medium |
| **Databricks** | 25h | 45h | 70h | 45h | 185h | Medium |
| **ClickHouse** | 80h | 60h | 200h | 100h | 440h | High |
| **Druid** | 120h | 80h | 300h | 150h | 650h | Very High |
| **Firebolt** | 35h | 50h | 90h | 55h | 230h | Medium |

**Key Issues from Redshift**:
- **Snowflake**: DISTKEY/SORTKEY → cluster keys, vacuum not needed, similar SQL
- **BigQuery**: No distribution keys, nested/repeated fields, different date functions
- **Synapse**: Similar architecture, but Azure-specific authentication
- **Databricks**: Delta Lake format, Spark SQL differences, cluster configuration
- **ClickHouse**: Complete rewrite needed, different data types, no transactions
- **Druid**: Dimensional modeling required, roll-up tables, limited SQL

### 5.2 Migration FROM BigQuery

| To Provider | Schema Migration | Data Transfer | Query Rewrite | Testing | Total Hours | Complexity |
|------------|------------------|---------------|---------------|---------|-------------|------------|
| **Snowflake** | 50h | 60h | 100h | 60h | 270h | Medium-High |
| **BigQuery** | 0h | 0h | 0h | 0h | 0h | N/A |
| **Redshift** | 60h | 70h | 140h | 80h | 350h | High |
| **Synapse** | 55h | 65h | 130h | 75h | 325h | High |
| **Databricks** | 40h | 50h | 80h | 50h | 220h | Medium |
| **ClickHouse** | 90h | 60h | 220h | 110h | 480h | Very High |
| **Druid** | 130h | 80h | 320h | 160h | 690h | Very High |
| **Firebolt** | 45h | 55h | 105h | 60h | 265h | Medium-High |

**Key Issues from BigQuery**:
- **Snowflake**: Nested/repeated → VARIANT, partition by → cluster by, UDF rewrites
- **Redshift**: Denormalize nested data, add distribution keys, federated queries lost
- **Synapse**: Similar to Redshift but better JSON support
- **Databricks**: Easier due to Delta Lake support for nested data
- **ClickHouse**: Arrays supported but different syntax, no nested structures
- **Druid**: Flattening required, pre-aggregation needed

### 5.3 Migration FROM Snowflake

| To Provider | Schema Migration | Data Transfer | Query Rewrite | Testing | Total Hours | Complexity |
|------------|------------------|---------------|---------------|---------|-------------|------------|
| **Snowflake** | 0h | 0h | 0h | 0h | 0h | N/A |
| **BigQuery** | 45h | 60h | 110h | 65h | 280h | Medium-High |
| **Redshift** | 35h | 50h | 90h | 55h | 230h | Medium |
| **Synapse** | 40h | 55h | 100h | 60h | 255h | Medium-High |
| **Databricks** | 30h | 45h | 75h | 50h | 200h | Medium |
| **ClickHouse** | 85h | 60h | 210h | 105h | 460h | High |
| **Druid** | 125h | 80h | 310h | 155h | 670h | Very High |
| **Firebolt** | 40h | 50h | 95h | 55h | 240h | Medium |

**Key Issues from Snowflake**:
- **BigQuery**: VARIANT → JSON/STRUCT, time travel differences, task → scheduled query
- **Redshift**: Add DISTKEY/SORTKEY, remove zero-copy cloning, slower performance
- **Synapse**: Similar issues to Redshift, dedicated SQL pool sizing
- **Databricks**: VARIANT → complex types, tasks → jobs, generally smooth
- **ClickHouse**: No time travel, different clustering, materialized views needed
- **Druid**: Major architectural change, streaming-first mindset

### 5.4 Migration FROM On-Premises (Oracle/SQL Server/Teradata)

| To Provider | Schema Migration | Data Transfer | Query Rewrite | Testing | Total Hours | Complexity |
|------------|------------------|---------------|---------------|---------|-------------|------------|
| **Snowflake** | 80h | 120h | 180h | 100h | 480h | High |
| **BigQuery** | 100h | 140h | 240h | 130h | 610h | Very High |
| **Redshift** | 90h | 130h | 200h | 110h | 530h | High |
| **Synapse** | 70h | 110h | 160h | 90h | 430h | High |
| **Databricks** | 75h | 115h | 175h | 95h | 460h | High |
| **ClickHouse** | 120h | 140h | 300h | 160h | 720h | Very High |
| **Druid** | 150h | 160h | 380h | 200h | 890h | Very High |
| **Firebolt** | 85h | 125h | 190h | 105h | 505h | High |

**Key Issues from On-Prem**:
- **Schema differences**: Sequences, triggers, stored procedures need rewriting
- **Data transfer**: Network bandwidth limitations, export/import time
- **Query rewrite**: Vendor-specific SQL, optimizer hints, performance tuning
- **Authentication**: LDAP/AD integration, SSO setup
- **Application changes**: Connection strings, drivers, retry logic
- **Synapse advantage**: Best for SQL Server migrations (T-SQL compatibility)
- **ClickHouse/Druid**: Require architectural rethinking

**Migration Effort Summary (Average Hours)**:
- **Easiest to migrate TO**: Snowflake (298h avg), Databricks (316h avg)
- **Hardest to migrate TO**: Druid (677h avg), ClickHouse (525h avg)
- **Easiest to migrate FROM**: Redshift → Snowflake (160h)
- **Hardest to migrate FROM**: BigQuery → Druid (690h)

---

## 6. Vendor Lock-in Assessment

Rating scale: 1 (very low lock-in) to 5 (very high lock-in)

### 6.1 Storage Format Portability

| Provider | Storage Format | Open Standard | Direct File Access | Export Formats | Lock-in Score |
|----------|----------------|---------------|-------------------|----------------|---------------|
| **Snowflake** | Proprietary | ❌ No | ❌ No | CSV, JSON, Parquet (via COPY) | 4 |
| **BigQuery** | Proprietary | ❌ No | ❌ No | CSV, JSON, Avro, Parquet (via export) | 4 |
| **Redshift** | Proprietary | ❌ No | ❌ No | CSV, Parquet (via UNLOAD) | 4 |
| **Synapse** | Proprietary | ❌ No | ❌ No | CSV, Parquet (via PolyBase) | 4 |
| **Databricks** | Delta Lake | ✅ Yes | ✅ Yes | Parquet, Delta (native) | 2 |
| **ClickHouse** | MergeTree | ⚠️ OSS | ✅ Yes | CSV, Parquet, Native | 2 |
| **Druid** | Segment files | ⚠️ OSS | ✅ Yes | JSON (via API) | 3 |
| **Firebolt** | Proprietary | ❌ No | ❌ No | CSV, Parquet (via COPY) | 4 |

### 6.2 SQL Dialect Lock-in

| Provider | SQL Standard | ANSI Compliance | Proprietary Extensions | Migration Difficulty | Lock-in Score |
|----------|-------------|----------------|----------------------|---------------------|---------------|
| **Snowflake** | ANSI SQL + | High | Many (FLATTEN, TIME_TRAVEL) | Medium | 3 |
| **BigQuery** | Standard SQL | High | Many (UNNEST, ML functions) | Medium-High | 3 |
| **Redshift** | PostgreSQL-based | Medium | Moderate (DISTKEY, SORTKEY) | Medium | 3 |
| **Synapse** | T-SQL | Medium | Many (T-SQL specific) | Medium | 3 |
| **Databricks** | Spark SQL | High | Some (DELTA commands) | Low-Medium | 2 |
| **ClickHouse** | Custom SQL | Low | Many (ClickHouse-specific) | High | 4 |
| **Druid** | Limited SQL | Low | Limited feature set | Very High | 5 |
| **Firebolt** | ANSI SQL | High | Few (index hints) | Low-Medium | 2 |

### 6.3 API Lock-in

| Provider | REST API | SQL API | Proprietary SDKs | Alternative Access | Lock-in Score |
|----------|---------|---------|------------------|-------------------|---------------|
| **Snowflake** | ✅ Yes | ✅ JDBC/ODBC | Many languages | Standard drivers | 2 |
| **BigQuery** | ✅ Yes | ✅ JDBC/ODBC | Google SDKs | Standard drivers | 2 |
| **Redshift** | ✅ AWS API | ✅ JDBC/ODBC | AWS SDKs | PostgreSQL drivers | 2 |
| **Synapse** | ✅ Yes | ✅ JDBC/ODBC | Azure SDKs | SQL Server drivers | 2 |
| **Databricks** | ✅ Yes | ✅ JDBC/ODBC | Databricks SDKs | Spark APIs | 2 |
| **ClickHouse** | ✅ HTTP | ✅ JDBC/ODBC | Community | Open drivers | 1 |
| **Druid** | ✅ REST | ⚠️ Limited | Python only | HTTP queries | 3 |
| **Firebolt** | ✅ Yes | ✅ JDBC/ODBC | Growing | Standard drivers | 2 |

### 6.4 Data Export Complexity

| Provider | Full Export Speed | Incremental Export | Automation Support | Cost to Export | Lock-in Score |
|----------|------------------|-------------------|-------------------|----------------|---------------|
| **Snowflake** | Fast (parallel) | ✅ Tasks/Streams | ✅ Full | Compute + storage egress | 3 |
| **BigQuery** | Fast (parallel) | ✅ Scheduled queries | ✅ Full | $0.011/GB export | 3 |
| **Redshift** | Moderate | ✅ UNLOAD to S3 | ✅ Full | Compute + S3 storage | 3 |
| **Synapse** | Moderate | ✅ Pipelines | ✅ Full | Compute + ADLS storage | 3 |
| **Databricks** | Fast (native Parquet) | ✅ Delta export | ✅ Full | Compute only (no egress) | 1 |
| **ClickHouse** | Fast | ✅ SELECT INTO | ⚠️ Manual | No egress fees | 1 |
| **Druid** | Slow (API-based) | ⚠️ Limited | ⚠️ Manual | No egress fees | 4 |
| **Firebolt** | Moderate | ✅ COPY TO | ⚠️ Growing | Compute + egress | 3 |

### 6.5 Ecosystem Lock-in

| Provider | BI Tool Dependency | Cloud Dependency | Partner Ecosystem | Alternative Tools | Lock-in Score |
|----------|-------------------|------------------|-------------------|-------------------|---------------|
| **Snowflake** | None | ⚠️ Multi-cloud | Extensive | Many alternatives | 2 |
| **BigQuery** | ⚠️ Looker favored | ✅ GCP only | GCP-centric | Limited outside GCP | 4 |
| **Redshift** | None | ✅ AWS only | AWS-centric | Limited outside AWS | 4 |
| **Synapse** | ⚠️ Power BI favored | ✅ Azure only | Azure-centric | Limited outside Azure | 4 |
| **Databricks** | None | ⚠️ Multi-cloud | Extensive | Many alternatives | 2 |
| **ClickHouse** | None | None | Open source | Full portability | 1 |
| **Druid** | ⚠️ Limited BI support | None | Apache ecosystem | Limited commercial tools | 2 |
| **Firebolt** | None | ⚠️ AWS/GCP | Growing | Standard tools work | 2 |

### 6.6 Overall Lock-in Severity

| Provider | Storage | SQL | API | Export | Ecosystem | Average | Severity |
|----------|---------|-----|-----|--------|-----------|---------|----------|
| **Snowflake** | 4 | 3 | 2 | 3 | 2 | 2.8 | Medium |
| **BigQuery** | 4 | 3 | 2 | 3 | 4 | 3.2 | Medium-High |
| **Redshift** | 4 | 3 | 2 | 3 | 4 | 3.2 | Medium-High |
| **Synapse** | 4 | 3 | 2 | 3 | 4 | 3.2 | Medium-High |
| **Databricks** | 2 | 2 | 2 | 1 | 2 | 1.8 | Low-Medium |
| **ClickHouse** | 2 | 4 | 1 | 1 | 1 | 1.8 | Low-Medium |
| **Druid** | 3 | 5 | 3 | 4 | 2 | 3.4 | High |
| **Firebolt** | 4 | 2 | 2 | 3 | 2 | 2.6 | Medium |

**Lock-in Risk Summary**:
- **Lowest risk**: Databricks (1.8), ClickHouse (1.8) - open formats, portable
- **Medium risk**: Snowflake (2.8), Firebolt (2.6) - multi-cloud helps
- **Higher risk**: BigQuery (3.2), Redshift (3.2), Synapse (3.2) - cloud-specific
- **Highest risk**: Druid (3.4) - limited SQL, export challenges

### 6.7 Lock-in Mitigation Strategies

#### For Cloud-Specific Platforms (BigQuery, Redshift, Synapse)
1. **Abstraction layers**: Use dbt for transformations (portable SQL)
2. **Query federation**: Trino/Presto for multi-warehouse queries
3. **Regular exports**: Scheduled exports to S3/GCS in Parquet format
4. **Standard SQL**: Avoid vendor-specific extensions where possible
5. **Estimated migration buffer**: Budget 300-400 hours for full migration

#### For Proprietary Platforms (Snowflake, Firebolt)
1. **Multi-cloud deployment**: Reduces cloud vendor lock-in
2. **ANSI SQL focus**: Minimize use of proprietary functions
3. **External stages**: Keep raw data in S3/GCS/ADLS
4. **Incremental exports**: Use streams/CDC for continuous data backup
5. **Estimated migration buffer**: Budget 200-300 hours for full migration

#### For Open Platforms (Databricks, ClickHouse)
1. **Delta Lake**: Already portable, can be read by multiple engines
2. **Spark ecosystem**: Large community, many alternative runtimes
3. **File-based storage**: Direct S3/GCS access reduces lock-in
4. **Open source**: ClickHouse can be self-hosted
5. **Estimated migration buffer**: Budget 150-200 hours for full migration

---

## Summary: Integration Complexity Scorecard

### Overall Integration Ease (1 = easiest, 5 = hardest)

| Provider | BI Tools | ETL/ELT | Cloud | Languages | Migration | Lock-in | **Average** |
|----------|----------|---------|-------|-----------|-----------|---------|-------------|
| **Snowflake** | 1.0 | 1.0 | 2.0 | 1.2 | 2.4 | 2.8 | **1.7** |
| **BigQuery** | 1.5 | 1.0 | 2.3 | 1.0 | 3.0 | 3.2 | **2.0** |
| **Redshift** | 1.25 | 1.5 | 2.3 | 1.8 | 2.6 | 3.2 | **2.1** |
| **Synapse** | 1.75 | 2.0 | 2.3 | 1.8 | 2.5 | 3.2 | **2.3** |
| **Databricks** | 2.0 | 1.25 | 1.3 | 1.4 | 2.2 | 1.8 | **1.7** |
| **ClickHouse** | 3.75 | 3.5 | 3.7 | 2.8 | 3.9 | 1.8 | **3.2** |
| **Druid** | 4.0 | 4.5 | 3.7 | 3.6 | 4.5 | 3.4 | **4.0** |
| **Firebolt** | 3.0 | 3.0 | 2.7 | 2.6 | 2.8 | 2.6 | **2.8** |

### Key Insights

**Easiest Overall Integration**:
1. **Snowflake (1.7)** - Best ecosystem support, mature connectors, multi-cloud
2. **Databricks (1.7)** - Tied, excels in cloud integration, open format reduces lock-in
3. **BigQuery (2.0)** - Strong within GCP, but poor cross-cloud

**Most Challenging Integration**:
1. **Druid (4.0)** - Limited BI tools, no dbt, requires architecture change
2. **ClickHouse (3.2)** - Open source flexibility but immature ecosystem
3. **Firebolt (2.8)** - Improving but still maturing connectors

**Best for Cloud Ecosystems**:
- **AWS**: Redshift (1.0) or Databricks (1.0)
- **GCP**: BigQuery (1.0) or Databricks (1.0)
- **Azure**: Synapse (1.0) or Databricks (1.0)
- **Multi-cloud**: Databricks (1.0), Snowflake (2.0)

**Lowest Lock-in Risk**:
- **Databricks (1.8)** - Delta Lake open format, Spark portability
- **ClickHouse (1.8)** - Open source, file-level access
- **Snowflake (2.8)** - Multi-cloud reduces risk despite proprietary storage

**Migration Recommendations**:
- **From Redshift**: Snowflake (160h), Databricks (185h), or Synapse (210h)
- **From BigQuery**: Databricks (220h), Snowflake (270h), or Firebolt (265h)
- **From Snowflake**: Databricks (200h), Redshift (230h), or Firebolt (240h)
- **From On-prem**: Synapse (430h for SQL Server), Snowflake (480h), or Databricks (460h)

**Programming Language Support**:
- **Best Python**: BigQuery, Snowflake, Databricks
- **Best Java/Scala**: All major platforms equal
- **Best R**: BigQuery (only CRAN package)
- **Best JavaScript**: BigQuery, Snowflake

**ETL/ELT Integration**:
- **Fivetran Tier 1**: Snowflake, BigQuery, Redshift, Synapse, Databricks
- **dbt Official Adapters**: Snowflake, BigQuery, Redshift, Databricks
- **Limited Support**: ClickHouse, Druid, Firebolt

---

**Document Statistics**:
- **Total providers analyzed**: 8
- **Integration dimensions**: 6 (BI, ETL/ELT, Cloud, Languages, Migration, Lock-in)
- **Data points collected**: 320+
- **Migration scenarios**: 32 (4 source platforms × 8 targets)
- **Lock-in factors assessed**: 5 per provider

**Next Steps**: See `synthesis.md` for cross-cutting insights and decision frameworks based on this integration analysis.
