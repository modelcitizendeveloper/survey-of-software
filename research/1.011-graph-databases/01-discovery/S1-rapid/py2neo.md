# py2neo - End of Life (EOL)

## Quick Facts

| Metric | Value |
|--------|-------|
| Package Name | `py2neo` |
| Latest Version | 2021.2.4 |
| Status | **END OF LIFE** |
| Last Meaningful Release | 2021 |
| GitHub Stars | ~1,200 (archived) |
| License | Apache-2.0 |

## Status Warning

**py2neo has been officially declared End of Life as of April 2025.**

The project is no longer maintained and will receive no further updates. The GitHub
repository has moved to neo4j-contrib/py2neo but is effectively archived.

## Migration Path

Neo4j recommends migrating to:

1. **neo4j** - Official Python driver for direct Cypher queries
2. **neomodel** - For ORM-style object-graph mapping

## Why py2neo Was Popular

Historically, py2neo offered:
- Higher-level API than the raw driver
- Built-in OGM (Object-Graph Mapper)
- HTTP and Bolt protocol support
- Cypher lexer for Pygments
- Command-line tools

## Migration Example

**Old (py2neo):**
```python
from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
graph.run("MATCH (n) RETURN n LIMIT 10")
```

**New (neo4j driver):**
```python
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
with driver.session() as session:
    session.run("MATCH (n) RETURN n LIMIT 10")
```

## Assessment

**Tier: 4 - Do Not Use**

Do not start new projects with py2neo. For existing codebases, plan migration to
the official neo4j driver or neomodel. Historical releases remain available on
PyPI for legacy compatibility.

## Links
- PyPI (historical): https://pypi.org/project/py2neo/
- GitHub (archived): https://github.com/neo4j-contrib/py2neo
- Migration Guide: https://neo4j.com/blog/developer/py2neo-end-migration-guide/
