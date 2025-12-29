# Graph Database Python Client Library Viability Assessment

## Executive Summary

This assessment evaluates the long-term viability of Python client libraries for major
graph databases. Libraries are rated on maintenance health, corporate backing, and
sustainability for production use over a 5-year horizon.

---

## Neo4j Python Driver

**Package**: `neo4j` (PyPI)
**Type**: Official vendor driver
**Current Version**: 6.0.3 (November 2025)

### Maintenance Status: EXCELLENT

- **Release Cadence**: Monthly releases since 5.0
- **Recent Activity**: 6.0.x series actively developed with breaking changes for modernization
- **Python Support**: 3.10, 3.11, 3.12, 3.13 (dropped 3.7-3.9 in 6.0)
- **Migration Tools**: Official migration assistant for codebase upgrades

### Corporate Backing: STRONG

- **Vendor**: Neo4j Inc. (founded 2007)
- **Funding**: $581M total raised, $2B valuation
- **Revenue**: $200M+ ARR (2024), 44% market share in graph DBMS
- **Customers**: 75%+ Fortune 100, including BMW, NASA, UBS
- **Business Model**: Open-source core + AuraDB managed service

### Breaking Change History: MODERATE RISK

Recent 5.x to 6.x migration requires attention:
- Error handling redesign (DriverError vs Neo4jError separation)
- Resource management changes (explicit .close() required)
- Package rename from `neo4j-driver` to `neo4j`
- Element IDs changed from integers to strings (5.x)

### Dependency Health: EXCELLENT

- Minimal dependencies, optional Rust extensions for performance
- No security vulnerabilities detected
- Clean dependency tree

### Bus Factor Risk: LOW

- Large engineering team at Neo4j
- Multiple maintainers across driver ecosystem
- Comprehensive documentation and enterprise support

### Viability Score: 9/10

**Recommendation**: Primary choice for Neo4j deployments. Strong long-term investment.

---

## Neomodel (Neo4j OGM)

**Package**: `neomodel` (PyPI)
**Type**: Community OGM under Neo4j Labs
**Current Version**: 6.0.0 (2024)

### Maintenance Status: GOOD (Improved)

- **Release Cadence**: Active development resumed 2023
- **2024 Updates**: Async support, mypy typing (95% coverage), vector index support
- **Python Support**: 3.7+ with Neo4j 5.x and 4.4 LTS

### Corporate Backing: COMMUNITY + LABS

- Moved to Neo4j Labs program (official recognition, community-driven)
- Production use by Novo Nordisk (OpenStudyBuilder)
- No dedicated corporate funding

### Breaking Change History: MODERATE

- Major version bumps may require model adjustments
- Configuration system overhaul in recent versions

### Bus Factor Risk: MEDIUM

- Small maintainer team (Marius Conjeaud primary)
- Active community but concentration of knowledge

### Viability Score: 7/10

**Recommendation**: Suitable for Neo4j projects needing OGM patterns. Monitor maintainer activity.

---

## python-arango (ArangoDB)

**Package**: `python-arango` (PyPI)
**Type**: Official vendor driver
**Current Version**: Latest 2024 release

### Maintenance Status: GOOD

- **Release Cadence**: Healthy release activity
- **Weekly Downloads**: 352,711 (popular package)
- **Python Support**: 3.8+
- **Async Alternative**: `python-arango-async` available

### Corporate Backing: MODERATE (Changed)

- **Vendor**: ArangoDB GmbH (founded 2014)
- **Funding**: $58.6M total raised
- **Licensing Change**: Moved to BSL 1.1 for version 3.12+ (Q1 2024)
  - Still source-available for non-commercial use
  - Cannot be used for competing managed services
  - Community Edition Transition Fund available

### Breaking Change History: LOW

- Stable API evolution
- Good backward compatibility

### Dependency Health: GOOD

- No security vulnerabilities detected
- Reasonable dependency footprint

### Bus Factor Risk: MEDIUM

- Smaller company than Neo4j
- Dual headquarters (San Francisco/Cologne)

### Viability Score: 7/10

**Recommendation**: Viable for multi-model needs. Watch licensing implications for SaaS deployments.

---

## pyTigerGraph

**Package**: `pyTigerGraph` (PyPI)
**Type**: Official vendor SDK
**Current Version**: 1.8.1

### Maintenance Status: ADEQUATE

- **Release Cadence**: Active but less frequent
- **Weekly Downloads**: 5,614 (smaller user base)
- **Recent Features**: Async support (1.8), REST endpoint refactoring (1.7)
- **Contributors**: 30 open-source contributors

### Corporate Backing: STRONG (Enterprise Focus)

- **Vendor**: TigerGraph (founded 2012)
- **Funding**: $172-174M total raised
- **Investors**: Tiger Global, AME Cloud Ventures, Baidu
- **Focus**: Enterprise analytics, fraud detection, supply chain
- **Customers**: Uber, VISA, Alipay, Zillow

### Breaking Change History: LOW-MODERATE

- Version 1.7+ requires TigerGraph DB 4.1+ for new features
- Generally stable API

### Dependency Health: GOOD

- No security vulnerabilities detected

### Bus Factor Risk: MEDIUM

- Enterprise focus may limit open-source investment
- Proprietary GSQL creates ecosystem isolation

### Viability Score: 6/10

**Recommendation**: Best for enterprise-scale graph analytics with existing TigerGraph investment.
Not recommended as a first graph database choice due to GSQL lock-in.

---

## gremlinpython (Apache TinkerPop)

**Package**: `gremlinpython` (PyPI)
**Type**: Apache Foundation project
**Current Version**: 3.8.0 (November 2025)

### Maintenance Status: EXCELLENT

- **Release Cadence**: Regular releases, 4.0 beta in development
- **Governance**: Apache Software Foundation PMC
- **Python Support**: Modern Python versions

### Corporate Backing: FOUNDATION + MULTI-VENDOR

- Apache Software Foundation governance since 2016
- Supported by multiple vendors (AWS, Microsoft, DataStax)
- PMC includes contributors from diverse organizations
- Active community with Discord, Twitch, YouTube presence

### Breaking Change History: MODERATE (4.0 Coming)

TinkerPop 4.0 introduces significant changes:
- Dropping WebSockets for HTTP 1.1
- Removing Bytecode in favor of gremlin-lang scripts
- Simplifying connection options

### Dependency Health: GOOD

- Standard Apache project quality

### Bus Factor Risk: LOW

- Multiple major vendors invested
- PMC governance ensures continuity
- Long-term Apache stewardship

### Viability Score: 8/10

**Recommendation**: Excellent choice for multi-database portability strategy. Works with
JanusGraph, Neptune, Cosmos DB, DataStax. TinkerPop 4.0 migration planning needed.

---

## Cloud Provider SDKs

### AWS Neptune (boto3 + gremlinpython)

- Gremlin and openCypher support
- Strong backing from AWS
- Lock-in to AWS ecosystem
- Viability tied to AWS platform (effectively permanent)

### Azure Cosmos DB (azure-cosmos + gremlinpython)

- Gremlin API among multiple options
- Microsoft backing but graph capabilities seen as stagnant
- Multi-model flexibility
- Viability tied to Azure platform

---

## Summary Viability Matrix

| Library         | Maintenance | Backing | Breaking Risk | Bus Factor | Overall |
|-----------------|-------------|---------|---------------|------------|---------|
| neo4j           | 9           | 9       | 7             | 9          | 9/10    |
| neomodel        | 7           | 6       | 7             | 5          | 7/10    |
| python-arango   | 8           | 6       | 8             | 6          | 7/10    |
| pyTigerGraph    | 6           | 7       | 7             | 6          | 6/10    |
| gremlinpython   | 9           | 8       | 6             | 9          | 8/10    |

---

## Key Findings

### Safest Long-term Bets
1. **neo4j**: Dominant market position, strong funding, active development
2. **gremlinpython**: Apache governance, multi-vendor support, portability value

### Watch List
- **python-arango**: BSL licensing change may affect SaaS use cases
- **pyTigerGraph**: GSQL proprietary language creates lock-in risk

### Emerging Considerations
- All libraries adding async support (critical for modern Python)
- Vector/embedding support becoming table stakes
- GQL standard will reshape query language landscape
