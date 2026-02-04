# neomodel - Python OGM for Neo4j

## Quick Facts

| Metric | Value |
|--------|-------|
| Package Name | `neomodel` |
| Latest Version | 6.0.0 (Nov 26, 2025) |
| Python Support | 3.10+ |
| Weekly Downloads | ~25,000 |
| GitHub Stars | 1,100 |
| Contributors | 97 |
| Open Issues | 49 |
| License | MIT |
| Maintainer | Neo4j Labs (community) |

## Installation

```bash
pip install neomodel

# With Rust driver extension for performance
pip install neomodel[rust-driver-ext]

# With optional dependencies (Shapely, pandas, numpy)
pip install neomodel[extras,rust-driver-ext]
```

## First Impression

**Strengths:**
- Django-style model definitions (familiar pattern)
- Schema enforcement with cardinality restrictions
- Full transaction and async support
- Neo4j Labs project (good maintenance quality)
- Django integration via django-neomodel plugin
- Vector and full-text search support (v6.0+)

**Considerations:**
- Abstracts away Cypher (less control for complex queries)
- Learning curve for graph-specific concepts
- Performance overhead vs raw driver

## Quick Example

```python
from neomodel import StructuredNode, StringProperty, RelationshipTo

class Person(StructuredNode):
    name = StringProperty(required=True)
    friends = RelationshipTo('Person', 'FRIEND')

# Create and relate nodes
alice = Person(name="Alice").save()
bob = Person(name="Bob").save()
alice.friends.connect(bob)

# Query
for friend in alice.friends.all():
    print(friend.name)
```

## Assessment

**Tier: 2 - Mature Community**

neomodel is the recommended OGM for Neo4j, especially for developers coming from
Django/SQLAlchemy backgrounds. It provides a Pythonic abstraction over the graph
while still allowing raw Cypher when needed. Good choice for rapid development.

## Links
- PyPI: https://pypi.org/project/neomodel/
- GitHub: https://github.com/neo4j-contrib/neomodel
- Docs: https://neomodel.readthedocs.io/
- Neo4j Labs: https://neo4j.com/labs/neomodel/
