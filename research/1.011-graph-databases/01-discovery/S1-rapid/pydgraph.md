# pydgraph - Official Dgraph Python Client

## Quick Facts

| Metric | Value |
|--------|-------|
| Package Name | `pydgraph` |
| Latest Version | 24.3.0 (Aug 5, 2025) |
| Python Support | 3.7 - 3.12 |
| Weekly Downloads | ~8,300 |
| GitHub Stars | 288 |
| Forks | 90 |
| Open Issues | 0 |
| License | Apache-2.0 |
| Maintainer | Hypermode Inc. (steward of Dgraph) |

## Installation

```bash
pip install pydgraph
```

## First Impression

**Strengths:**
- Official client with gRPC protocol
- Good Python version support (3.7+)
- Clean, simple API
- Connection string support for clusters
- ACL (Access Control List) authentication

**Considerations:**
- Smaller ecosystem compared to Neo4j
- Dgraph uses GraphQL-like DQL, learning curve
- gRPC dependency can cause build issues on older systems

## Quick Example

```python
import pydgraph

# Create client
client_stub = pydgraph.DgraphClientStub('localhost:9080')
client = pydgraph.DgraphClient(client_stub)

# Set schema
schema = """
name: string @index(exact) .
friends: [uid] .
type Person {
    name
    friends
}
"""
op = pydgraph.Operation(schema=schema)
client.alter(op)

# Create data
txn = client.txn()
try:
    mutation = pydgraph.Mutation(set_nquads='_:alice <name> "Alice" .')
    txn.mutate(mutation)
    txn.commit()
finally:
    txn.discard()

# Query
query = """
{
  people(func: has(name)) {
    name
    friends { name }
  }
}
"""
res = client.txn(read_only=True).query(query)
print(res.json)

client_stub.close()
```

## Connection String Format

```python
# Standard connection
client_stub = pydgraph.DgraphClientStub("localhost:9080")

# With authentication
client_stub = pydgraph.DgraphClientStub("dgraph://username:password@host:9080")
```

## Assessment

**Tier: 3 - Emerging/Niche**

pydgraph is the correct choice for Dgraph integration. While the community is
smaller than Neo4j, the library is well-maintained with zero open issues.
Suitable for applications needing Dgraph's distributed graph capabilities
and native GraphQL-like query language.

## Links
- PyPI: https://pypi.org/project/pydgraph/
- GitHub: https://github.com/dgraph-io/pydgraph
- Dgraph Docs: https://dgraph.io/docs/
