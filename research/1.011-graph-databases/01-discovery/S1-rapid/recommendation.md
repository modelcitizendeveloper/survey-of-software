# Graph Database Python Clients: Recommendations

## Quick Assessment Summary

### Tier Rankings

| Tier | Library | Downloads/Week | Use Case |
|------|---------|---------------|----------|
| 1 | gremlinpython | 5.7M | Multi-DB, Neptune, JanusGraph |
| 1 | rdflib | 1.45M | RDF/Semantic web |
| 1 | neo4j | 520K | Neo4j (official) |
| 1 | python-arango | 350K-1.2M | ArangoDB (official) |
| 2 | neomodel | 25K | Neo4j OGM |
| 3 | pydgraph | 8K | Dgraph |
| 3 | pyTigerGraph | 5.6K | TigerGraph |
| 4 | py2neo | EOL | **Do not use** |
| 4 | pyorient | Stale (2017) | **Avoid** |

## Top Picks by Use Case

### For Neo4j Integration
**Primary: `neo4j`** (official driver)
- Best for: Direct Cypher queries, maximum control, performance
- Install: `pip install neo4j`

**Alternative: `neomodel`** (OGM)
- Best for: Django-style model definitions, rapid development
- Install: `pip install neomodel`

### For Multi-Database Portability
**Primary: `gremlinpython`**
- Best for: Neptune, JanusGraph, CosmosDB, any Gremlin-compatible DB
- Install: `pip install gremlinpython`

### For ArangoDB
**Primary: `python-arango`**
- Best for: Multi-model (document + graph + key-value) applications
- Install: `pip install python-arango`

### For Semantic Web / Knowledge Graphs
**Primary: `rdflib`**
- Best for: RDF processing, SPARQL queries, linked data
- Install: `pip install rdflib`

### For Graph Analytics / ML
**Primary: `pyTigerGraph[gds]`**
- Best for: Large-scale graph analytics, ML on graphs
- Install: `pip install pyTigerGraph[gds]`

## Decision Matrix

| Requirement | Recommended Library |
|-------------|---------------------|
| Need Cypher query language | neo4j, neomodel |
| Need Gremlin query language | gremlinpython |
| Need SPARQL / RDF | rdflib |
| Need vendor portability | gremlinpython |
| Need ORM-style abstraction | neomodel |
| AWS Neptune | gremlinpython + neptune-python-utils |
| Multi-model (doc + graph) | python-arango |
| Graph machine learning | pyTigerGraph[gds] |
| Distributed graph at scale | pydgraph, pyTigerGraph |

## Libraries to Avoid

1. **py2neo** - Officially EOL (April 2025), migrate to neo4j/neomodel
2. **pyorient** - Last release 2017, OrientDB has limited Python support
3. **neo4j-driver** - Deprecated package name, use `neo4j` instead

## Key Insights

1. **gremlinpython dominates downloads** due to AWS Neptune and cloud adoption
2. **Neo4j ecosystem is strongest** with official driver + OGM options
3. **ArangoDB has excellent official support** with zero open issues
4. **RDFLib serves a distinct use case** (semantic web vs property graphs)
5. **TigerGraph and Dgraph are niche** but officially supported

## Next Steps for Deeper Evaluation

1. Test connection setup with actual database instances
2. Benchmark query performance for representative workloads
3. Evaluate async support for concurrent applications
4. Review error handling and retry mechanisms
5. Assess integration with web frameworks (FastAPI, Django)

## Data Sources

- PyPI: Package metadata and downloads
- PyPI Stats: https://pypistats.org/
- GitHub: Repository metrics
- Snyk Advisor: Package health analysis
- Official documentation for each library

*Research conducted: December 2025*
