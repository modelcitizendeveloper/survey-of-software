# S1 Rapid Discovery: Graph Database Python Clients

## Research Methodology

### Scope Definition
This discovery focuses on **client libraries** for interacting with graph databases from Python,
NOT the graph databases themselves. The goal is to evaluate developer experience, community
health, and production readiness of each library.

### Discovery Process

1. **Initial Library Identification**
   - Categorize by database: Neo4j, ArangoDB, TigerGraph, Amazon Neptune, Dgraph
   - Identify multi-database solutions: Apache TinkerPop (Gremlin), RDFLib
   - Note official vs community-maintained libraries

2. **Metrics Collection**
   For each library, we gather:
   - **GitHub metrics**: stars, forks, contributors, open issues, last commit date
   - **PyPI metrics**: weekly downloads, latest version, Python version support
   - **Maintenance signals**: release frequency, issue response time
   - **Documentation quality**: quick scan of docs completeness

3. **First Impression Evaluation**
   - Installation simplicity: `pip install <package>` should work cleanly
   - Quickstart availability: can a developer be productive in 10 minutes?
   - API design: does it feel Pythonic?

### Libraries Evaluated

| Database | Official Client | Alternative/OGM |
|----------|-----------------|-----------------|
| Neo4j | neo4j (driver) | neomodel (OGM), py2neo (EOL) |
| ArangoDB | python-arango | python-arango-async |
| TigerGraph | pyTigerGraph | - |
| Amazon Neptune | gremlinpython + neptune-python-utils | - |
| Dgraph | pydgraph | - |
| Multi-DB (Gremlin) | gremlinpython | - |
| RDF Graphs | rdflib | - |
| OrientDB | pyorient | - (stale) |

### Evaluation Criteria

**Tier 1 - Production Ready**
- 500k+ weekly downloads
- Active maintenance (commits within 30 days)
- Official/vendor support
- Comprehensive documentation

**Tier 2 - Mature Community**
- 50k-500k weekly downloads
- Regular releases (quarterly or better)
- Good documentation
- Active issue resolution

**Tier 3 - Emerging/Niche**
- <50k weekly downloads
- May have gaps in documentation
- Smaller community
- Specialized use cases

**Tier 4 - Caution Advised**
- Stale/EOL projects
- No recent releases
- Deprecated in favor of alternatives

### Data Sources
- PyPI: https://pypi.org/ (version, dependencies, downloads)
- PyPI Stats: https://pypistats.org/ (download statistics)
- GitHub: Repository metrics and activity
- Snyk Advisor: Package health analysis
- Official documentation sites

### Key Findings Summary
See individual library files and `recommendation.md` for detailed analysis.
The most widely adopted libraries are gremlinpython (5.7M weekly downloads),
rdflib (1.4M), neo4j driver (520K), and python-arango (350K-1.2M).
