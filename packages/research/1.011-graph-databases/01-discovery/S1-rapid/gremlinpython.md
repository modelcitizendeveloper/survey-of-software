# gremlinpython - Apache TinkerPop Gremlin for Python

## Quick Facts

| Metric | Value |
|--------|-------|
| Package Name | `gremlinpython` |
| Latest Version | 3.8.0 (Nov 17, 2025) |
| Python Support | 3.10+ |
| Weekly Downloads | ~5.7 million |
| GitHub Stars | 1,900+ (TinkerPop repo) |
| License | Apache-2.0 |
| Maintainer | Apache TinkerPop |

## Installation

```bash
pip install gremlinpython
```

## First Impression

**Strengths:**
- Universal graph query language (Gremlin)
- Works with multiple databases: Neptune, JanusGraph, CosmosDB, etc.
- Most downloaded graph Python library
- Apache Foundation backing
- Stable, mature codebase

**Considerations:**
- Gremlin syntax differs from Cypher
- Generic API may lack database-specific optimizations
- TinkerPop 4.0 brings breaking changes (HTTP replacing WebSockets)

## Compatible Databases

- Amazon Neptune
- JanusGraph
- Azure Cosmos DB (Gremlin API)
- DataStax Enterprise Graph
- IBM Compose for JanusGraph
- OrientDB
- TigerGraph (limited)

## Quick Example

```python
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph

# Connect to Gremlin server
graph = Graph()
conn = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
g = graph.traversal().withRemote(conn)

# Traverse the graph
people = g.V().hasLabel('person').values('name').toList()
print(people)

# Find friends of Alice
friends = g.V().has('person', 'name', 'Alice').out('knows').values('name').toList()
print(friends)

conn.close()
```

## Amazon Neptune Usage

```python
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

# With neptune-python-utils for IAM auth
from neptune_python_utils.gremlin_utils import GremlinUtils

gremlin_utils = GremlinUtils()
conn = gremlin_utils.remote_connection()
g = gremlin_utils.traversal_source(connection=conn)
```

## Assessment

**Tier: 1 - Production Ready**

gremlinpython is the standard for Gremlin-based graph traversal. Its massive
adoption (5.7M downloads/week) reflects use in AWS Neptune and other cloud
graph services. Essential for multi-database portability or when using
Gremlin-compatible databases.

## Links
- PyPI: https://pypi.org/project/gremlinpython/
- GitHub: https://github.com/apache/tinkerpop/tree/master/gremlin-python
- Docs: https://tinkerpop.apache.org/docs/current/reference/#gremlin-python
- Neptune Utils: https://github.com/awslabs/amazon-neptune-tools
