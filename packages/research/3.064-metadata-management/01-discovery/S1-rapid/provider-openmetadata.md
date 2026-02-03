# OpenMetadata

**Category**: Open-Source Metadata Platform (with managed service option)
**Website**: https://open-metadata.org
**GitHub**: https://github.com/open-metadata/OpenMetadata (7.7k stars, 373 contributors)
**Managed Service**: Collate (https://www.getcollate.io)

## Overview

OpenMetadata is a unified metadata platform for data discovery, data observability, and data governance powered by a central metadata repository, in-depth column-level lineage, and seamless team collaboration. Born from the team behind Databook at Uber, it provides a comprehensive solution for managing metadata across the entire data stack.

## Key Features

### Data Discovery
- Unified metadata graph centralizing all metadata for all data assets
- AI-powered search and discovery
- Rich data context (descriptions, tags, ownership, lineage)
- 84+ turnkey connectors for data sources

### Data Lineage
- End-to-end lineage tracking across data pipelines
- Column-level lineage with filter queries
- Manual lineage editing via no-code editor
- Visual lineage graphs showing transformations

### Data Quality
- Data profiling (statistics, distributions, nulls)
- Column-level test definitions
- Freshness metrics and monitoring
- Integration with Great Expectations
- Test suite ownership and observability alerts

### Data Governance
- Domain and ownership assignment
- PII tagging and classification
- Policy management
- Glossary and taxonomy management
- Integration with quality and observability

### Collaboration
- Team discussions on data assets
- Slack, Microsoft Teams, Google Chat webhooks
- Announcement feeds
- Activity tracking

## Integration Ecosystem

### Connectors (84+)
- **Data Warehouses**: Snowflake, BigQuery, Redshift, Databricks, Synapse
- **Databases**: PostgreSQL, MySQL, Oracle, MongoDB, DynamoDB
- **BI Tools**: Tableau, Looker, PowerBI, Superset, Metabase
- **Pipeline Tools**: Airflow, dbt, Dagster, Prefect, Fivetran
- **Messaging**: Kafka, Redpanda, Pulsar
- **ML Platforms**: MLflow, SageMaker

## Deployment Options

### Self-Hosted
- **Local Docker**: Quick-start for development/testing
- **Kubernetes**: Production deployment with Helm charts
- **Cloud VMs**: Manual installation on AWS/GCP/Azure
- **Requirements**: Java, Python, TypeScript runtime

### Managed Service (Collate)
- **Free Tier**: Available (waitlist signup)
- **Paid Plans**: Usage-based pricing (users + data assets)
- **Bring Your Own Cloud**: AWS, GCP, Azure with VPN
- **Deployment Models**: Single-tenant SaaS, hybrid, private cloud

## Technical Architecture

### Tech Stack
- **Backend**: Java (31.9%)
- **Frontend**: TypeScript (45.4%)
- **Ingestion**: Python (20.5%)
- **Database**: MySQL/PostgreSQL (metadata store)
- **Search**: Elasticsearch

### Components
- **Metadata Schemas**: Core definitions and vocabulary
- **Metadata Store**: Central repository connecting data assets
- **Metadata APIs**: REST APIs for producing/consuming metadata
- **Ingestion Framework**: Pluggable connector system

## Pricing

### Open-Source (Self-Hosted)
- **License**: Apache 2.0
- **Cost**: Free (infrastructure costs only)
- **Support**: Community Slack, GitHub issues

### Collate (Managed)
- **Free Tier**: Limited users and data assets
- **Growth/Enterprise**: Usage-based (contact for pricing)
- **Additional Costs**: Extra users, data assets, BYOC deployment
- **Support**: SLA-backed support for paid plans

## Setup Complexity

### Self-Hosted Installation
- **Time Estimate**: 2-4 hours (Docker), 6-12 hours (Kubernetes)
- **Complexity**: Medium (requires infrastructure knowledge)
- **Prerequisites**: Docker/K8s, database, domain setup

### Managed Service (Collate)
- **Time Estimate**: 30 minutes to 2 hours
- **Complexity**: Low (SaaS onboarding)
- **Prerequisites**: Connector credentials

### Connector Configuration
- **Time per Connector**: 15-60 minutes
- **Complexity**: Low to medium (depends on data source)
- **Documentation**: Comprehensive per-connector guides

## Strengths

1. **Comprehensive Feature Set**: Discovery + observability + governance in one platform
2. **Connector Breadth**: 84+ connectors covering most data tools
3. **Column-Level Lineage**: Deep lineage tracking across transformations
4. **Active Development**: 164 releases, 373 contributors, regular updates
5. **Open-Source**: Apache 2.0 license with no vendor lock-in
6. **Managed Option**: Collate provides enterprise support without self-hosting burden
7. **Data Quality Integration**: Built-in profiling, testing, and monitoring

## Weaknesses

1. **Setup Complexity**: Self-hosted deployment requires infrastructure expertise
2. **Resource Requirements**: Java + TypeScript + Python stack can be resource-intensive
3. **Learning Curve**: Comprehensive feature set requires time to master
4. **Enterprise Features**: Some advanced features only in Collate managed service
5. **Smaller Community**: Smaller than DataHub (7.7k vs ~15k GitHub stars)

## Use Cases

### Ideal For
- Organizations wanting unified discovery + observability + governance
- Teams with 84+ connector ecosystem (modern data stack)
- Companies prioritizing column-level lineage
- Data teams needing self-hosted option with escape hatch
- Enterprises requiring open-source foundation with managed option

### Not Ideal For
- Very small teams (< 5 people) with simple data stack
- Organizations with legacy systems not in connector list
- Teams without infrastructure expertise (unless using Collate)
- Projects requiring custom metadata models not supported by schemas

## Competitive Positioning

### vs DataHub
- **OpenMetadata**: Unified discovery/observability/governance, newer, faster UI
- **DataHub**: Larger community, more mature, plugin architecture
- **Winner**: OpenMetadata for feature breadth, DataHub for ecosystem

### vs Amundsen
- **OpenMetadata**: More comprehensive (lineage, quality, governance)
- **Amundsen**: Simpler, focused on discovery, flexible backend
- **Winner**: OpenMetadata for full-featured platform, Amundsen for simplicity

### vs Atlan (Commercial)
- **OpenMetadata**: Open-source, self-hosted option, lower cost
- **Atlan**: Active metadata (real-time), packaged deployment, enterprise support
- **Winner**: OpenMetadata for cost/flexibility, Atlan for enterprise features

## Community and Governance

- **License**: Apache 2.0
- **Contributors**: 373 (as of Oct 2025)
- **Releases**: 164 total, latest 1.10.1 (Oct 9, 2025)
- **Community**: Public Slack workspace, GitHub discussions
- **Maintainer**: Collate (company behind OpenMetadata)
- **Roadmap**: Public roadmap with community input

## Migration Considerations

### Inbound Migration
- **From Custom Solutions**: API-based ingestion for metadata import
- **From Amundsen/DataHub**: Manual migration (no automated tool)
- **Connector-Based**: Many sources can be re-ingested directly

### Outbound Migration
- **API Export**: REST APIs for metadata extraction
- **Database Backup**: Metadata store can be exported
- **Vendor Lock-In Risk**: Low (open-source, standard APIs)

## Recent Updates (2025)

- **Release 1.10.x**: Redshift/DynamoDB connector improvements, UI performance
- **Release 1.8.x**: Enterprise-grade data context for AI agents
- **Release 1.5.x**: Data quality enhancements, new connectors
- **Collate Integration**: AI agents for data work automation

## Recommendation

**Overall Score**: ⭐⭐⭐⭐½ (4.5/5)

**Best For**: Teams wanting a comprehensive open-source metadata platform with unified discovery, observability, and governance features, and the option to use managed service (Collate) for enterprise support.

**Consider Alternatives If**:
- You need the largest ecosystem and community (DataHub)
- You want simplicity over feature breadth (Amundsen)
- You require enterprise support without self-hosting (Atlan, Alation)
- Your data stack uses tools outside the 84+ connector list

## Quick Start Resources

- **Documentation**: https://docs.open-metadata.org
- **Sandbox**: https://sandbox.open-metadata.org
- **GitHub**: https://github.com/open-metadata/OpenMetadata
- **Slack Community**: https://slack.open-metadata.org
- **Collate (Managed)**: https://www.getcollate.io
