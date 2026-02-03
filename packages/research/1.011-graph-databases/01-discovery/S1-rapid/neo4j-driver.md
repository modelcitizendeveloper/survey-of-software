# neo4j - Official Neo4j Python Driver

## Quick Facts

| Metric | Value |
|--------|-------|
| Package Name | `neo4j` |
| Latest Version | 6.0.3 (Nov 6, 2025) |
| Python Support | 3.10, 3.11, 3.12, 3.13 |
| Weekly Downloads | ~520,000 |
| GitHub Stars | 1,000 |
| Contributors | 58 |
| License | Apache-2.0 |
| Maintainer | Neo4j, Inc. (official) |

## Installation

```bash
pip install neo4j

# With optional Rust extension for 10x performance
pip install neo4j-rust-ext

# With pandas/numpy integration
pip install neo4j[numpy,pandas,pyarrow]
```

## First Impression

**Strengths:**
- Official vendor support with dedicated team
- Production-stable with semantic versioning
- Async support built-in
- Rust extensions available for performance-critical workloads
- Excellent documentation and examples
- Type hints throughout

**Considerations:**
- Python 3.10+ required (no legacy support)
- Deprecated `neo4j-driver` package still in PyPI (causes confusion)

## Quick Example

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

with driver.session() as session:
    result = session.run("MATCH (n:Person) RETURN n.name LIMIT 10")
    for record in result:
        print(record["n.name"])

driver.close()
```

## Assessment

**Tier: 1 - Production Ready**

The official Neo4j driver is the clear choice for Neo4j integration. It has strong
community adoption, official support, excellent documentation, and modern Python
features. The Rust extension option makes it suitable for high-throughput workloads.

## Links
- PyPI: https://pypi.org/project/neo4j/
- GitHub: https://github.com/neo4j/neo4j-python-driver
- Docs: https://neo4j.com/docs/python-manual/current/
