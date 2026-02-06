# DataHub

**Category**: Open-Source Metadata Platform (with managed service option)
**Website**: https://datahubproject.io
**GitHub**: https://github.com/datahub-project/datahub (~15k stars estimated, 300+ contributors)
**Managed Service**: Acryl Data (https://www.acryldata.io)

## Overview

DataHub is an extensible metadata platform created by LinkedIn and open-sourced in 2020. It emphasizes data governance and collaboration across teams through a plugin-based architecture and fine-grained access controls. DataHub is LinkedIn's second attempt at solving cataloging and data discovery problems, built on lessons learned from their first iteration.

## Key Features

### Data Discovery
- Search across all data assets (datasets, dashboards, pipelines, ML models)
- Rich metadata context (ownership, tags, glossary terms)
- Browse by domain, platform, or entity type
- Automated metadata ingestion

### Data Lineage
- Table and column-level lineage tracking
- Cross-platform lineage (data warehouse → BI tool → dashboard)
- Impact analysis (what breaks if I change this?)
- Visual lineage graphs

### Data Governance
- Fine-grained access controls (dataset, column, tag-level)
- PII tagging and automatic data deletion (GDPR compliance)
- Column-level classification
- Domain-based organization
- Policy enforcement

### Data Quality
- Data assertions and checks
- Freshness monitoring
- Validation rules
- Integration with Great Expectations

### Collaboration
- Discussions and announcements
- Ownership assignment
- Team mentions and notifications
- Activity feeds

## Integration Ecosystem

### Connectors (50+)
- **Data Warehouses**: Snowflake, BigQuery, Redshift, Databricks, Hive
- **Databases**: PostgreSQL, MySQL, Oracle, MongoDB, Cassandra
- **BI Tools**: Tableau, Looker, PowerBI, Superset, Mode
- **Pipeline Tools**: Airflow, dbt, Spark, Kafka, Flink
- **Cloud Platforms**: AWS Glue, Azure Data Factory, GCP Dataflow

### Plugin Architecture
- Extensible via custom plugins
- Source plugins for metadata ingestion
- Sink plugins for downstream systems
- Transformer plugins for metadata enrichment

## Deployment Options

### Self-Hosted
- **Docker Compose**: Quick-start for development (single command)
- **Kubernetes**: Production deployment with Helm charts
- **Cloud VMs**: Manual installation on any cloud provider
- **Requirements**: Java, Python, MySQL/PostgreSQL, Elasticsearch/OpenSearch

### Managed Service (Acryl Data)
- **SaaS**: Fully managed cloud deployment
- **Pricing**: Contact for quote (usage-based)
- **Support**: Enterprise SLA, dedicated customer success
- **Features**: Additional governance and observability features

## Technical Architecture

### Tech Stack
- **Backend**: Java (GraphQL API, GMS - General Metadata Service)
- **Frontend**: React (TypeScript)
- **Ingestion**: Python
- **Storage**: MySQL/PostgreSQL + Elasticsearch/OpenSearch
- **Schema**: Pegasus (LinkedIn's data schema language)

### Components
- **Metadata Service (GMS)**: Central API layer
- **Frontend (DataHub UI)**: Web interface
- **Metadata Ingestion**: Python-based ingestion framework
- **MCE/MAE**: Metadata Change Events/Audit Events (event-driven)

## Pricing

### Open-Source (Self-Hosted)
- **License**: Apache 2.0
- **Cost**: Free (infrastructure costs only)
- **Support**: Community Slack (5000+ members), GitHub issues

### Acryl Data (Managed)
- **Pricing**: Contact sales (usage-based)
- **Free Tier**: None (enterprise-focused)
- **Support**: Dedicated support, CSM, training
- **Additional Features**: Enhanced governance, observability, security

## Setup Complexity

### Self-Hosted Installation
- **Time Estimate**: 1-2 hours (Docker Compose), 4-8 hours (Kubernetes)
- **Complexity**: Medium (simpler than OpenMetadata due to mature docs)
- **Prerequisites**: Docker/K8s, database, search engine

### Managed Service (Acryl Data)
- **Time Estimate**: 1-2 hours (onboarding + connector setup)
- **Complexity**: Low (SaaS)
- **Prerequisites**: Connector credentials

### Connector Configuration
- **Time per Connector**: 15-45 minutes
- **Complexity**: Low to medium
- **Documentation**: Extensive per-connector guides

## Strengths

1. **Mature Ecosystem**: 300+ contributors, established community, proven at LinkedIn scale
2. **Strong Governance**: Fine-grained access controls, PII tagging, GDPR compliance
3. **Plugin Architecture**: Extensible and customizable for unique needs
4. **Event-Driven**: MCE/MAE system enables real-time metadata updates
5. **Production-Ready**: Battle-tested at LinkedIn and 100+ companies
6. **Active Community**: 5000+ Slack members, frequent releases
7. **Comprehensive Documentation**: Extensive guides, tutorials, API docs

## Weaknesses

1. **Setup Complexity**: Multiple components (GMS, frontend, Elasticsearch, etc.)
2. **Resource Requirements**: Can be resource-intensive at scale
3. **Learning Curve**: Plugin architecture and Pegasus schema have learning curve
4. **UI Complexity**: Feature-rich but can feel overwhelming for simple use cases
5. **Managed Service Cost**: Acryl Data pricing can be high for smaller teams

## Use Cases

### Ideal For
- Enterprises with complex data governance requirements
- Organizations needing fine-grained access control
- Teams requiring GDPR/compliance features (PII tagging, deletion)
- Companies with unique metadata needs (custom plugins)
- Data teams at scale (proven at LinkedIn scale)

### Not Ideal For
- Very small teams (< 10 people) with simple data stack
- Teams wanting simplest possible setup (Amundsen better)
- Organizations without Kubernetes/infrastructure expertise (unless using Acryl)
- Projects needing unified observability (OpenMetadata more integrated)

## Competitive Positioning

### vs OpenMetadata
- **DataHub**: Larger community, more mature, better governance
- **OpenMetadata**: Unified observability/governance, faster UI, simpler architecture
- **Winner**: DataHub for governance/maturity, OpenMetadata for feature integration

### vs Amundsen
- **DataHub**: More comprehensive, better governance, active development
- **Amundsen**: Simpler, faster setup, Lyft-backed
- **Winner**: DataHub for production use, Amundsen for quick wins

### vs Atlan (Commercial)
- **DataHub**: Open-source, self-hosted option, larger community
- **Atlan**: Active metadata, packaged deployment, modern UI
- **Winner**: DataHub for flexibility, Atlan for ease of use

## Community and Governance

- **License**: Apache 2.0
- **Contributors**: 300+ (as of Oct 2025)
- **Releases**: Frequent (monthly releases)
- **Community**: 5000+ Slack members, active GitHub discussions
- **Maintainer**: Linux Foundation (DataHub Project)
- **Backing**: LinkedIn (original), Acryl Data (commercial support)
- **Roadmap**: Public roadmap with community input

## Migration Considerations

### Inbound Migration
- **From Custom Solutions**: REST/GraphQL API for metadata import
- **From Amundsen**: Some community tools available
- **Connector-Based**: Re-ingest from data sources directly

### Outbound Migration
- **API Export**: GraphQL API for metadata extraction
- **Database Backup**: Metadata can be exported from storage
- **Vendor Lock-In Risk**: Low (open-source, Apache 2.0)

## Recent Updates (2025)

- **Monthly Releases**: Regular feature updates and bug fixes
- **Governance Enhancements**: Expanded access control policies
- **Connector Growth**: New connectors added regularly
- **Performance Improvements**: UI and backend optimizations

## Recommendation

**Overall Score**: ⭐⭐⭐⭐⭐ (5/5)

**Best For**: Enterprises and large data teams requiring mature, battle-tested metadata platform with strong governance features and extensibility. Ideal for organizations with complex compliance requirements (GDPR, PII management) and the resources to manage self-hosted infrastructure or budget for Acryl Data managed service.

**Consider Alternatives If**:
- You want simpler setup and unified observability (OpenMetadata)
- You need the simplest possible solution (Amundsen)
- You prefer commercial-first with packaged deployment (Atlan)
- Your team is very small (< 10 people) and budget-constrained

## Quick Start Resources

- **Documentation**: https://datahubproject.io/docs
- **Demo**: https://demo.datahubproject.io
- **GitHub**: https://github.com/datahub-project/datahub
- **Slack Community**: https://datahubspace.slack.com
- **Acryl Data (Managed)**: https://www.acryldata.io
