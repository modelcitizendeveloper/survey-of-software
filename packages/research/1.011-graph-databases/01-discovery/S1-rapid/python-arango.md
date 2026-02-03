# python-arango - Official ArangoDB Python Driver

## Quick Facts

| Metric | Value |
|--------|-------|
| Package Name | `python-arango` |
| Latest Version | 8.2.5 (Dec 22, 2025) |
| Python Support | 3.9, 3.10, 3.11, 3.12 |
| Weekly Downloads | ~350,000 - 1.2M |
| GitHub Stars | 466 |
| Contributors | 32+ |
| Open Issues | 0 |
| License | MIT |
| Maintainer | ArangoDB (official) |

## Installation

```bash
pip install python-arango

# For async support
pip install python-arango-async
```

## First Impression

**Strengths:**
- Official vendor support
- Excellent maintenance (zero open issues)
- Clean, Pythonic API
- Comprehensive AQL query support
- Graph traversal, document, and key-value operations
- Async alternative available

**Considerations:**
- ArangoDB-specific (multi-model but single vendor)
- Smaller community than Neo4j ecosystem

## Quick Example

```python
from arango import ArangoClient

client = ArangoClient(hosts="http://localhost:8529")
db = client.db("mydb", username="root", password="password")

# Create a graph
graph = db.create_graph("social")
people = graph.create_vertex_collection("people")
friends = graph.create_edge_definition(
    edge_collection="friends",
    from_vertex_collections=["people"],
    to_vertex_collections=["people"]
)

# Insert vertices and edges
alice = people.insert({"_key": "alice", "name": "Alice"})
bob = people.insert({"_key": "bob", "name": "Bob"})
friends.insert({"_from": "people/alice", "_to": "people/bob"})

# AQL query
cursor = db.aql.execute("FOR p IN people RETURN p.name")
print([doc for doc in cursor])
```

## Assessment

**Tier: 1 - Production Ready**

python-arango is an excellent choice for ArangoDB integration. The library is
well-maintained with official support, zero open issues, and comprehensive
coverage of ArangoDB features. Particularly strong for applications needing
multi-model (document + graph + key-value) capabilities.

## Links
- PyPI: https://pypi.org/project/python-arango/
- GitHub: https://github.com/arangodb/python-arango
- Docs: https://docs.python-arango.com/
- Async: https://github.com/arangodb/python-arango-async
