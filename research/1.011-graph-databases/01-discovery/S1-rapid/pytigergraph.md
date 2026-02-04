# pyTigerGraph - TigerGraph Python Client

## Quick Facts

| Metric | Value |
|--------|-------|
| Package Name | `pyTigerGraph` |
| Latest Version | 1.9.1 (Nov 4, 2025) |
| Python Support | 3.8+ |
| Weekly Downloads | ~5,600 |
| GitHub Stars | 34 |
| Contributors | 22 |
| Open Issues | 7 |
| License | Apache-2.0 |
| Maintainer | TigerGraph (official) |

## Installation

```bash
# Core functionality
pip install pyTigerGraph

# With Graph Data Science / ML capabilities
pip install pyTigerGraph[gds]
```

## First Impression

**Strengths:**
- Official vendor support
- Graph machine learning integration
- Async support (v1.8+)
- DataFrame loading from Pandas
- Good for analytics and ML workloads

**Considerations:**
- Smaller community (niche database)
- Less documentation compared to Neo4j/ArangoDB
- TigerGraph-specific GSQL language

## Quick Example

```python
import pyTigerGraph as tg

conn = tg.TigerGraphConnection(
    host="https://your-instance.i.tgcloud.io",
    graphname="MyGraph",
    username="tigergraph",
    password="password"
)

# Get auth token
conn.getToken(conn.createSecret())

# Run a query
results = conn.runInstalledQuery("find_friends", params={"person": "Alice"})

# Upsert vertices
conn.upsertVertices("Person", [
    {"id": "alice", "name": "Alice"},
    {"id": "bob", "name": "Bob"}
])
```

## Graph Data Science Features

```python
# With pyTigerGraph[gds]
from pyTigerGraph.gds import featurizer

# Create graph features for ML
feat = conn.gds.featurizer()
feat.installAlgorithm("pagerank")
feat.runAlgorithm("pagerank", params={"v_type": "Person"})
```

## Assessment

**Tier: 3 - Emerging/Niche**

pyTigerGraph is the right choice when using TigerGraph, especially for graph
analytics and machine learning use cases. The library has official support but
a smaller community. Best suited for enterprise analytics workloads where
TigerGraph's performance advantages justify the ecosystem trade-offs.

## Links
- PyPI: https://pypi.org/project/pyTigerGraph/
- GitHub: https://github.com/tigergraph/pyTigerGraph
- Docs: https://docs.tigergraph.com/pytigergraph/current/intro/
