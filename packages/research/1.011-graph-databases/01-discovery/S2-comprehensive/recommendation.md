# Graph Database Python Client Recommendations

## Executive Summary

This document provides optimized recommendations for selecting Python client libraries for graph databases based on common use cases and technical requirements.

## Primary Recommendations by Use Case

### 1. General-Purpose Graph Applications

**Recommended: neo4j-driver + neomodel**

| Component | Library | Rationale |
|-----------|---------|-----------|
| Low-level access | neo4j-driver | Best-in-class async, connection pooling, Rust extensions |
| OGM layer | neomodel | Django-style models, validation, hooks |

**Why this combination:**
- Neo4j has the most mature Python ecosystem
- neo4j-driver provides native asyncio for modern applications
- neomodel adds productivity without sacrificing performance
- Excellent documentation and community support

### 2. Multi-Database Portability

**Recommended: gremlinpython (with aiogremlin for async)**

**Compatible databases:** Amazon Neptune, Azure Cosmos DB, JanusGraph, and more

**Why Gremlin:**
- Standardized query language across vendors
- Reduces vendor lock-in risk
- Single codebase for multiple deployment targets

**Caveats:**
- Native gremlinpython is synchronous; use aiogremlin or goblin for async
- Database-specific features may not be accessible
- Connection pooling has known recovery issues

### 3. Multi-Model Requirements (Document + Graph + Key-Value)

**Recommended: python-arango**

**Why ArangoDB:**
- Single database for multiple data models
- AQL is powerful and SQL-like
- Good Python driver quality

**Async strategy:** Use python-arango-async for true asyncio support

### 4. Semantic Web / RDF / Linked Data

**Recommended: rdflib + SPARQLWrapper**

**Why rdflib:**
- De facto standard for Python RDF processing
- Full SPARQL 1.1 support
- Extensive serialization format support

**Limitations:**
- No native async (wrap with thread pools)
- Not suitable for large-scale production graphs (use graph databases with SPARQL endpoints)

### 5. High-Scale Graph Analytics and ML

**Recommended: pyTigerGraph[gds]**

**Why TigerGraph:**
- Built-in graph data science algorithms
- Direct integration with PyTorch Geometric and DGL
- Distributed processing for large graphs

**Caveats:**
- GSQL learning curve
- Performance overhead in Python client
- Smaller community than Neo4j

### 6. Distributed/Horizontally Scalable Graphs

**Recommended: pydgraph**

**Why Dgraph:**
- Native horizontal scaling
- GraphQL-native design
- gRPC for efficient communication

**Caveats:**
- Async uses gRPC futures, not native asyncio
- Smaller ecosystem than alternatives
- DQL query language unique to Dgraph

## Decision Matrix

| Requirement | Best Choice | Runner-up |
|-------------|-------------|-----------|
| Best overall Python experience | neo4j-driver | python-arango |
| OGM/Django-style models | neomodel | Goblin (Gremlin) |
| Native async/FastAPI | neo4j-driver | python-arango-async |
| Database portability | gremlinpython | - |
| Multi-model (doc+graph) | python-arango | - |
| Graph ML/Analytics | pyTigerGraph[gds] | - |
| Semantic web/RDF | rdflib | - |
| Horizontal scaling | pydgraph | TigerGraph |
| Cloud-native (AWS) | gremlinpython (Neptune) | - |
| Cloud-native (Azure) | gremlinpython (Cosmos) | - |

## Libraries to Avoid

### py2neo (Deprecated)

- End of Life - no further updates
- Migrate to neo4j-driver + neomodel

## Framework Integration Recommendations

### FastAPI Applications

```python
# Recommended stack
neo4j-driver (AsyncDriver)
# OR
python-arango-async
```

### Django Applications

```python
# Recommended stack
neomodel with django_neomodel
```

### Data Science / Jupyter

```python
# Recommended stack
pyTigerGraph[gds]  # For graph ML
# OR
rdflib  # For RDF/semantic data
```

## Performance Optimization Tips

### Neo4j Stack

1. Install `neo4j-rust-ext` for 20-40% performance improvement
2. Use `execute_query()` for simple operations (avoids session overhead)
3. Configure connection pool based on concurrency needs
4. Use UNWIND for bulk operations

### ArangoDB Stack

1. Use batch methods (`insert_many`, `update_many`) for bulk operations
2. Consider async driver for I/O-bound workloads
3. Use ArangoSearch for full-text queries instead of AQL filters

### Gremlin Stack

1. Prefer GraphBinary serialization over GraphSON
2. Use prepared traversals for repeated queries
3. Consider Goblin OGM for complex object mapping

## Migration Considerations

### From py2neo to neo4j-driver

- Replace `Graph.run()` with `session.run()` or `driver.execute_query()`
- Update transaction patterns to managed transactions
- Migrate OGM code to neomodel

### From SQL to Graph

- Start with neomodel for familiar ORM patterns
- Use Cypher for complex traversals
- Consider ArangoDB if joining existing document data

## Conclusion

For most Python graph database applications, the **Neo4j ecosystem (neo4j-driver + neomodel)** offers the best balance of:
- API quality and Pythonic design
- Native async support
- Documentation and community
- Performance (with Rust extensions)
- OGM productivity (neomodel)

For specialized requirements (multi-database portability, RDF/semantic web, graph ML, or horizontal scaling), select the specialized library that best matches the use case as outlined above.
