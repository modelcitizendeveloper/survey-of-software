# Amundsen

**Category**: Open-Source Metadata Discovery Platform
**Website**: https://www.amundsen.io
**GitHub**: https://github.com/amundsen-io/amundsen (~4k stars)
**Managed Service**: Limited commercial options

## Overview

Amundsen is an open-source data discovery tool developed by Lyft and open-sourced in 2019. It focuses on enhancing productivity through efficient metadata ingestion and providing a user-friendly interface for searching and discovering data assets. Amundsen emphasizes simplicity and backend flexibility, making it an excellent choice for teams prioritizing ease of use over comprehensive feature sets.

## Key Features

### Data Discovery
- Simple, intuitive search interface
- Browse by table, dashboard, user
- Popular tables and frequently used assets
- Rich descriptions and documentation
- User and team information

### Data Preview
- Unique capability: Connect catalog with live databases
- Preview table data directly in the UI
- Query statistics and usage patterns
- Column-level metadata

### Metadata Ingestion
- ETL-focused approach (extract, transform, load metadata)
- Databuilder framework for custom extractors
- Scheduled ingestion jobs
- Support for various data sources

### Backend Flexibility
- **Neo4j**: Default graph database backend
- **AWS Neptune**: Managed graph database option
- **Apache Atlas**: Hadoop ecosystem integration
- **Extensible**: Custom backend implementations possible

### Basic Governance
- Ownership tracking
- Tag-based organization
- Basic classification
- Description management

## Integration Ecosystem

### Connectors
- **Data Warehouses**: Snowflake, BigQuery, Redshift, Hive, Presto
- **Databases**: PostgreSQL, MySQL, Druid
- **BI Tools**: Tableau, Mode, Redash
- **Pipeline Tools**: Airflow

### Backend Options
- Neo4j (community default)
- AWS Neptune (managed option)
- Apache Atlas (enterprise option)

## Deployment Options

### Self-Hosted
- **Docker Compose**: Quick-start for local development
- **Kubernetes**: Production deployment
- **Requirements**: Python, Neo4j/Neptune/Atlas, Elasticsearch

### Managed Service
- **Limited Options**: No official managed service from Lyft
- **Community Solutions**: Some third-party deployment options
- **DIY Cloud**: Deploy to AWS/GCP/Azure manually

## Technical Architecture

### Tech Stack
- **Frontend**: React (TypeScript)
- **Backend**: Python (Flask)
- **Search**: Elasticsearch
- **Graph Database**: Neo4j / Neptune / Atlas
- **Ingestion**: Python (Databuilder)

### Components
- **Frontend Service**: React UI
- **Metadata Service**: Flask API
- **Search Service**: Elasticsearch wrapper
- **Databuilder**: ETL framework for metadata ingestion

## Pricing

### Open-Source (Self-Hosted Only)
- **License**: Apache 2.0
- **Cost**: Free (infrastructure costs only)
- **Support**: Community Slack, GitHub issues
- **Managed Option**: Not officially available

## Setup Complexity

### Self-Hosted Installation
- **Time Estimate**: 1-3 hours (Docker Compose), 4-6 hours (Kubernetes)
- **Complexity**: Low to medium (simpler than DataHub/OpenMetadata)
- **Prerequisites**: Docker, Neo4j, Elasticsearch

### Connector Configuration
- **Time per Connector**: 20-60 minutes
- **Complexity**: Medium (requires writing/configuring Databuilder scripts)
- **Documentation**: Good but less comprehensive than DataHub

## Strengths

1. **Simplicity**: Easiest to set up among major open-source platforms
2. **User Experience**: Clean, intuitive UI focused on discovery
3. **Backend Flexibility**: Choice of Neo4j, Neptune, or Atlas
4. **Data Preview**: Unique feature to preview live data from catalog
5. **Lyft-Backed**: Proven in production at Lyft
6. **Lightweight**: Fewer components than DataHub or OpenMetadata
7. **Fast Setup**: Can be running in 1-3 hours

## Weaknesses

1. **Limited Features**: Focuses on discovery, lacks comprehensive governance/observability
2. **No Official Managed Service**: Must self-host (no Lyft-backed SaaS)
3. **Smaller Community**: Less active than DataHub (4k vs 15k stars)
4. **No Column-Level Lineage**: Basic lineage only
5. **Limited Data Quality**: No built-in profiling or testing
6. **ETL-Based Ingestion**: Batch-oriented, not real-time
7. **Fewer Connectors**: Smaller ecosystem than DataHub/OpenMetadata

## Use Cases

### Ideal For
- Small to medium teams (5-50 people) prioritizing simplicity
- Organizations wanting fastest time-to-value for discovery
- Teams comfortable with ETL-based metadata ingestion
- Companies needing backend flexibility (Neo4j vs Neptune vs Atlas)
- Projects where data preview is critical feature

### Not Ideal For
- Teams requiring comprehensive governance features
- Organizations needing column-level lineage
- Companies wanting unified observability + governance
- Teams requiring managed service option
- Projects needing extensive data quality features

## Competitive Positioning

### vs DataHub
- **Amundsen**: Simpler, faster setup, better UX for discovery
- **DataHub**: More comprehensive, better governance, larger community
- **Winner**: Amundsen for simplicity, DataHub for production scale

### vs OpenMetadata
- **Amundsen**: Simpler, focused on discovery only
- **OpenMetadata**: Unified platform (discovery + observability + governance)
- **Winner**: Amundsen for quick wins, OpenMetadata for comprehensive solution

### vs Commercial (Atlan, Alation)
- **Amundsen**: Open-source, self-hosted, free (no managed option)
- **Commercial**: Managed service, enterprise support, more features
- **Winner**: Amundsen for budget-conscious teams, commercial for ease of use

## Community and Governance

- **License**: Apache 2.0
- **Contributors**: ~100+ (less active than DataHub)
- **Releases**: Less frequent (mature, stable project)
- **Community**: Slack workspace (smaller than DataHub)
- **Maintainer**: Lyft (original), community-driven now
- **Roadmap**: Community-driven, less structured than DataHub

## Migration Considerations

### Inbound Migration
- **From Custom Solutions**: Databuilder ETL scripts for import
- **From DataHub**: Manual migration (no automated tool)
- **Connector-Based**: Re-ingest from data sources

### Outbound Migration
- **API Export**: REST APIs for metadata extraction
- **Neo4j Dump**: Graph database can be exported
- **Vendor Lock-In Risk**: Low (open-source, simple architecture)

## Recent Updates (2025)

- **Stable Releases**: Fewer updates (mature project)
- **Community Maintenance**: Community-driven development
- **Backend Support**: Continued support for Neo4j, Neptune, Atlas

## Recommendation

**Overall Score**: ⭐⭐⭐⭐ (4/5)

**Best For**: Small to medium teams wanting the simplest possible open-source data discovery solution with a focus on user experience over feature breadth. Ideal for organizations prioritizing fast time-to-value and willing to trade advanced governance/observability features for ease of setup.

**Consider Alternatives If**:
- You need comprehensive governance features (DataHub)
- You want unified observability + governance (OpenMetadata)
- You require managed service option (Collate, Acryl Data, Atlan)
- You need column-level lineage or data quality features
- Your team is large (50+ people) with complex requirements

## Quick Start Resources

- **Documentation**: https://www.amundsen.io/amundsen/
- **GitHub**: https://github.com/amundsen-io/amundsen
- **Slack Community**: https://amundsen-io.slack.com
- **Blog**: https://eng.lyft.com/amundsen (Lyft Engineering)
