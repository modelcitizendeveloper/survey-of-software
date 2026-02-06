# pyTigerGraph - TigerGraph Python Client

## Overview

pyTigerGraph is the official Python package for interacting with TigerGraph databases. It provides comprehensive access to TigerGraph's graph analytics and machine learning capabilities, with special emphasis on Graph Data Science (GDS) workflows.

## Key Information

| Attribute | Value |
|-----------|-------|
| Package | `pyTigerGraph` |
| Version | 1.6.x |
| Python Support | 3.7+ |
| Protocol | REST API |
| License | Apache 2.0 |
| Repository | github.com/tigergraph/pyTigerGraph |

## Installation

```bash
# Core package
pip install pyTigerGraph

# With Graph Data Science features
pip install 'pyTigerGraph[gds]'
```

## Connection Management

### Basic Connection

```python
import pyTigerGraph as tg

conn = tg.TigerGraphConnection(
    host="https://your-instance.i.tgcloud.io",
    graphname="MyGraph",
    username="tigergraph",
    password="password"
)

# Generate API token
conn.getToken(conn.createSecret())
```

### TigerGraph Cloud

```python
conn = tg.TigerGraphConnection(
    host="https://your-instance.i.tgcloud.io",
    graphname="MyGraph",
    apiToken="your-api-token"
)
```

### Async Connection

```python
from pyTigerGraph import AsyncTigerGraphConnection

async_conn = AsyncTigerGraphConnection(
    host="https://your-instance.i.tgcloud.io",
    graphname="MyGraph",
    username="tigergraph",
    password="password"
)
```

## Schema Management

### Object-Oriented Schema (v1.5+)

```python
# Define vertex types
person = conn.gds.vertexType("Person", [
    ("name", "STRING"),
    ("age", "INT"),
    ("email", "STRING")
])

# Define edge types
knows = conn.gds.edgeType("KNOWS",
    from_vertex="Person",
    to_vertex="Person",
    attributes=[
        ("since", "DATETIME"),
        ("strength", "FLOAT")
    ]
)

# Create graph from schema
conn.gds.createGraph("SocialNetwork", [person], [knows])
```

### GSQL Schema Definition

```python
# Execute GSQL directly
conn.gsql("""
    CREATE VERTEX Person (
        PRIMARY_ID id STRING,
        name STRING,
        age INT
    )

    CREATE DIRECTED EDGE KNOWS (
        FROM Person,
        TO Person,
        since DATETIME
    )
""")
```

## Data Operations

### Vertex Operations

```python
# Upsert vertex (insert or update)
conn.upsertVertex(
    vertexType="Person",
    vertexId="alice",
    attributes={"name": "Alice", "age": 30}
)

# Get vertex
vertex = conn.getVertices(
    vertexType="Person",
    vertexIds=["alice"]
)

# Delete vertex
conn.delVertices(
    vertexType="Person",
    vertexId="alice"
)
```

### Edge Operations

```python
# Upsert edge
conn.upsertEdge(
    sourceVertexType="Person",
    sourceVertexId="alice",
    edgeType="KNOWS",
    targetVertexType="Person",
    targetVertexId="bob",
    attributes={"since": "2020-01-01"}
)

# Get edges
edges = conn.getEdges(
    sourceVertexType="Person",
    sourceVertexId="alice",
    edgeType="KNOWS"
)
```

### Bulk Operations

```python
# Bulk upsert vertices
vertices = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]
conn.upsertVertices("Person", vertices)

# Bulk upsert edges
edges = [
    {
        "from_id": "alice",
        "to_id": "bob",
        "attributes": {"since": "2020-01-01"}
    }
]
conn.upsertEdges("Person", "KNOWS", "Person", edges)
```

## GSQL Queries

### Installed Queries

```python
# Install query
conn.gsql("""
    CREATE QUERY findFriends(VERTEX<Person> p) FOR GRAPH MyGraph {
        Start = {p};
        Friends = SELECT t
                  FROM Start:s -(KNOWS)-> Person:t;
        PRINT Friends;
    }
    INSTALL QUERY findFriends
""")

# Run installed query
result = conn.runInstalledQuery("findFriends", {"p": "alice"})

# Async query execution
job_id = conn.runInstalledQuery("longQuery", params={}, runAsync=True)
status = conn.checkQueryStatus([job_id])
```

### Interpreted Queries

```python
# Run query without installing
result = conn.gsql("""
    INTERPRET QUERY () FOR GRAPH MyGraph {
        Persons = SELECT p FROM Person:p;
        PRINT Persons;
    }
""")
```

### Query Metadata

```python
# Get query information
metadata = conn.getQueryMetadata("findFriends")

# List running queries
running = conn.getRunningQueries()

# Abort query
conn.abortQuery(["query_id_1", "query_id_2"])
```

## Graph Data Science

### Feature Engineering (with GDS package)

```python
# Install GDS algorithms
conn.gds.featurizer.installAlgorithm("pagerank")

# Run PageRank
result = conn.gds.featurizer.runAlgorithm(
    "pagerank",
    params={"v_type": "Person", "e_type": "KNOWS"}
)

# Community detection
result = conn.gds.featurizer.runAlgorithm(
    "louvain",
    params={"v_type": "Person", "e_type": "KNOWS"}
)
```

### Graph Neural Networks

```python
# PyTorch Geometric data loader
from torch_geometric.loader import NeighborLoader

# Create graph data
data = conn.gds.getVertexDataFrame("Person")

# Vertex feature extraction
features = conn.gds.featurizer.extractVertexFeatures(
    v_type="Person",
    attributes=["age", "degree"]
)

# Edge feature extraction
edge_features = conn.gds.featurizer.extractEdgeFeatures(
    e_type="KNOWS",
    attributes=["strength"]
)
```

### Train/Test Split

```python
# Split vertices for ML
conn.gds.vertexSplitter(
    v_types=["Person"],
    train_fraction=0.8,
    validate_fraction=0.1,
    test_fraction=0.1
)
```

## Error Handling

```python
from pyTigerGraph.pyTigerGraphException import TigerGraphException

try:
    result = conn.runInstalledQuery("nonexistent")
except TigerGraphException as e:
    print(f"Error: {e}")
```

## Authentication

### Token Management

```python
# Create secret
secret = conn.createSecret()

# Get token with lifetime
token = conn.getToken(secret, lifetime=86400)  # 24 hours

# Refresh token
new_token = conn.refreshToken(secret)
```

### Role-Based Access

```python
# With RBAC
conn = tg.TigerGraphConnection(
    host="https://your-instance.i.tgcloud.io",
    graphname="MyGraph",
    username="analyst",
    password="password"
)
```

## Performance Considerations

### Caveats

From official documentation:
> "pyTigerGraph may perform slower than direct HTTP requests to the TigerGraph REST API due to its feature-rich abstraction layer adding URL setup, logging, authentication, and validation."

### Optimization Tips

```python
# Use bulk operations for large datasets
conn.upsertVertices("Person", large_list, atomic=False)

# Disable unnecessary logging
import logging
logging.getLogger("pyTigerGraph").setLevel(logging.WARNING)

# Use async for long-running queries
job_id = conn.runInstalledQuery("heavyQuery", runAsync=True)
```

## Limitations

- REST-only protocol (higher latency than binary protocols)
- Performance overhead from abstraction layer
- GSQL learning curve for complex queries
- Less mature ecosystem than Neo4j/ArangoDB
- GDS features require additional package

## When to Use

**Choose pyTigerGraph when:**
- Graph analytics and ML are primary use cases
- Large-scale graph processing needed
- GSQL expertise available
- TigerGraph Cloud deployment
- Integration with PyTorch Geometric or DGL needed

**Consider alternatives when:**
- Simple CRUD operations primary use case
- Low latency critical (consider direct REST)
- Multi-database portability needed
- Smaller graphs with simpler requirements

## Resources

- [Documentation](https://docs.tigergraph.com/pytigergraph/current/intro/)
- [GitHub Repository](https://github.com/tigergraph/pyTigerGraph)
- [GSQL Documentation](https://docs.tigergraph.com/gsql-ref/current/)
- [Graph Data Science](https://docs.tigergraph.com/pytigergraph/current/gds/)
- [TigerGraph Cloud](https://tgcloud.io/)
