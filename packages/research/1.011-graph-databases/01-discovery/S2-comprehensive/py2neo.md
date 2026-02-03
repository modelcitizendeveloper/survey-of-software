# py2neo (End of Life)

## Status: Archived

**IMPORTANT: py2neo is End of Life (EOL) as of 2023. No further updates will be released. Users should migrate to the official Neo4j Python driver.**

The project has been transferred to Neo4j Inc. for archival purposes at `neo4j-contrib/py2neo`.

## Overview

py2neo was a comprehensive Neo4j client library and toolkit providing a high-level API, OGM capabilities, admin tools, and a Cypher lexer for Pygments. It supported both Bolt and HTTP protocols.

## Key Information

| Attribute | Value |
|-----------|-------|
| Package | `py2neo` |
| Final Version | 2021.2 |
| Python Support | 3.x |
| Protocols | Bolt, HTTP |
| License | Apache 2.0 |
| Repository | github.com/neo4j-contrib/py2neo (archived) |

## Historical Features

### Graph Object API

```python
from py2neo import Graph, Node, Relationship

# Connect to database
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# Create nodes and relationships
alice = Node("Person", name="Alice")
bob = Node("Person", name="Bob")
knows = Relationship(alice, "KNOWS", bob)

# Merge to database
graph.merge(alice, "Person", "name")
```

### OGM Capabilities

```python
from py2neo.ogm import GraphObject, Property, RelatedTo

class Person(GraphObject):
    __primarykey__ = "name"

    name = Property()
    born = Property()
    friends = RelatedTo("Person", "KNOWS")

# Usage
person = Person()
person.name = "Alice"
graph.push(person)
```

### Cypher Execution

```python
# Direct Cypher queries
results = graph.run(
    "MATCH (p:Person {name: $name}) RETURN p",
    name="Alice"
)

for record in results:
    print(record["p"])
```

### Batch Operations

```python
from py2neo import Graph

tx = graph.begin()
for i in range(1000):
    tx.create(Node("Item", id=i))
    if i % 100 == 0:
        tx.commit()
        tx = graph.begin()
tx.commit()
```

## Migration Path

### Recommended Migration: neo4j-driver

For low-level access, migrate to the official Neo4j Python driver:

```python
# py2neo (old)
from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
result = graph.run("MATCH (n) RETURN n")

# neo4j-driver (new)
from neo4j import GraphDatabase
driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))
with driver.session() as session:
    result = session.run("MATCH (n) RETURN n")
```

### Recommended Migration: neomodel

For OGM functionality, migrate to neomodel:

```python
# py2neo OGM (old)
from py2neo.ogm import GraphObject, Property

class Person(GraphObject):
    name = Property()

# neomodel (new)
from neomodel import StructuredNode, StringProperty

class Person(StructuredNode):
    name = StringProperty()
```

## Why py2neo Was Deprecated

1. **Maintenance Burden**: Single maintainer model not sustainable
2. **Official Driver Improvements**: Neo4j's official driver matured significantly
3. **Community Fragmentation**: Multiple overlapping libraries caused confusion
4. **Compatibility Challenges**: Keeping up with Neo4j versions became difficult

## Historical Strengths

- Clean, Pythonic API
- Built-in OGM functionality
- Cypher lexer for syntax highlighting
- HTTP fallback when Bolt unavailable
- Comprehensive documentation

## Historical Limitations

- Single maintainer created bus factor risk
- Calendar versioning led to breaking changes
- No async support
- Performance overhead vs. official driver
- Infrequent updates in later years

## Lessons for Library Selection

The py2neo deprecation offers lessons for evaluating graph database libraries:

1. **Prefer Official Drivers**: Better long-term support guarantees
2. **Check Maintainer Count**: Multiple maintainers reduce abandonment risk
3. **Evaluate Release Frequency**: Regular releases indicate active maintenance
4. **Consider Corporate Backing**: Libraries backed by database vendors more stable

## Current Alternatives

| Need | Recommended Library |
|------|---------------------|
| Low-level access | neo4j-driver |
| OGM functionality | neomodel |
| Async support | neo4j-driver (async) |
| Bulk operations | neo4j-driver + UNWIND |

## Resources (Archival)

- [Archived Handbook](https://neo4j-contrib.github.io/py2neo/)
- [GitHub Archive](https://github.com/neo4j-contrib/py2neo)
- [PyPI (frozen)](https://pypi.org/project/py2neo/)
- [Migration Guide](https://neo4j.com/docs/python-manual/current/)
