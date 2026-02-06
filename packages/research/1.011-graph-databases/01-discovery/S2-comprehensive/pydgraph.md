# pydgraph - Dgraph Python Client

## Overview

pydgraph is the official Python client for Dgraph, a distributed, horizontally scalable graph database. It uses gRPC for high-performance communication and supports Dgraph's GraphQL-like query language (DQL, formerly GraphQL+-).

## Key Information

| Attribute | Value |
|-----------|-------|
| Package | `pydgraph` |
| Version | 24.x / 25.x |
| Python Support | 3.7+ |
| Protocol | gRPC |
| License | Apache 2.0 |
| Repository | github.com/hypermodeinc/pydgraph |

## Version Compatibility

| Dgraph Version | pydgraph Version |
|---------------|------------------|
| 21.03.x | 21.03.x |
| 23.0.x | 23.0.x |
| 24.0.x | 24.0.x |
| 25.0.x | 25.0.x |

## Installation

```bash
pip install pydgraph
```

## Connection Management

### Basic Connection

```python
import pydgraph

# Create client stub
stub = pydgraph.DgraphClientStub('localhost:9080')

# Create client
client = pydgraph.DgraphClient(stub)

# Close when done
stub.close()
```

### Multiple Stubs (Cluster)

```python
# Connect to multiple cluster nodes
stub1 = pydgraph.DgraphClientStub('node1:9080')
stub2 = pydgraph.DgraphClientStub('node2:9080')
stub3 = pydgraph.DgraphClientStub('node3:9080')

client = pydgraph.DgraphClient(stub1, stub2, stub3)
```

### Connection Strings

```python
# Using connection string
client = pydgraph.DgraphClient.from_cloud(
    "dgraph://user:pass@host:9080?tls=true"
)

# Dgraph Cloud
client = pydgraph.DgraphClient.from_cloud(
    "https://your-instance.cloud.dgraph.io/graphql",
    api_key="your-api-key"
)
```

### TLS Configuration

```python
import grpc

# Load credentials
with open('ca.crt', 'rb') as f:
    ca_cert = f.read()

credentials = grpc.ssl_channel_credentials(ca_cert)

stub = pydgraph.DgraphClientStub(
    'localhost:9080',
    credentials=credentials
)
```

## Schema Management

### Alter Schema

```python
schema = """
    name: string @index(exact) .
    age: int @index(int) .
    email: string @index(hash) @upsert .

    type Person {
        name
        age
        email
        friends
    }
"""

client.alter(pydgraph.Operation(schema=schema))
```

### Drop Operations

```python
# Drop all data and schema
client.alter(pydgraph.Operation(drop_all=True))

# Drop specific predicate
client.alter(pydgraph.Operation(drop_attr='name'))

# Drop specific type
client.alter(pydgraph.Operation(drop_op=pydgraph.Operation.TYPE, drop_value='Person'))
```

## Transaction Types

### Read-Write Transaction

```python
txn = client.txn()
try:
    # Mutations and queries
    response = txn.mutate(set_nquads='_:alice <name> "Alice" .')
    txn.commit()
finally:
    txn.discard()
```

### Read-Only Transaction

```python
txn = client.txn(read_only=True)
try:
    response = txn.query(query_string)
finally:
    txn.discard()
```

### Best-Effort Transaction

```python
# For stale reads (better performance)
txn = client.txn(read_only=True, best_effort=True)
```

## Mutations

### JSON Mutations

```python
import json

txn = client.txn()
try:
    data = {
        'uid': '_:alice',
        'dgraph.type': 'Person',
        'name': 'Alice',
        'age': 30,
        'friends': [
            {'uid': '_:bob', 'dgraph.type': 'Person', 'name': 'Bob'}
        ]
    }

    response = txn.mutate(set_obj=data)

    # Get assigned UIDs
    alice_uid = response.uids['alice']
    bob_uid = response.uids['bob']

    txn.commit()
finally:
    txn.discard()
```

### N-Quads Mutations

```python
txn = client.txn()
try:
    nquads = """
        _:alice <dgraph.type> "Person" .
        _:alice <name> "Alice" .
        _:alice <age> "30"^^<xs:int> .
    """
    response = txn.mutate(set_nquads=nquads)
    txn.commit()
finally:
    txn.discard()
```

### Delete Mutations

```python
txn = client.txn()
try:
    # Delete specific predicate
    txn.mutate(del_nquads=f'<{uid}> <name> * .')

    # Delete node completely
    txn.mutate(del_obj={'uid': uid})

    txn.commit()
finally:
    txn.discard()
```

## Queries (DQL)

### Basic Query

```python
query = """
    {
        people(func: type(Person)) {
            uid
            name
            age
            friends {
                name
            }
        }
    }
"""

response = client.txn(read_only=True).query(query)
result = json.loads(response.json)
people = result['people']
```

### Parameterized Query

```python
query = """
    query findPerson($name: string) {
        person(func: eq(name, $name)) {
            uid
            name
            age
        }
    }
"""

variables = {'$name': 'Alice'}
response = client.txn(read_only=True).query(query, variables=variables)
```

### Aggregation Queries

```python
query = """
    {
        stats(func: type(Person)) {
            count: count(uid)
            avgAge: avg(age)
            minAge: min(age)
            maxAge: max(age)
        }
    }
"""
```

## Upsert Operations

### Basic Upsert

```python
query = """
    query {
        user as var(func: eq(email, "alice@example.com"))
    }
"""

mutation = """
    uid(user) <name> "Alice" .
    uid(user) <email> "alice@example.com" .
"""

txn = client.txn()
try:
    request = txn.create_request(
        query=query,
        mutations=[pydgraph.Mutation(set_nquads=mutation)]
    )
    response = txn.do_request(request)
    txn.commit()
finally:
    txn.discard()
```

### Conditional Upsert

```python
query = """
    query {
        user as var(func: eq(email, "alice@example.com"))
    }
"""

# Only mutate if user doesn't exist
mutation = pydgraph.Mutation(
    set_nquads='uid(user) <name> "Alice" .',
    cond='@if(eq(len(user), 0))'
)
```

## Async Operations

pydgraph provides async variants using gRPC futures:

### async_alter

```python
future = client.async_alter(pydgraph.Operation(schema=schema))

# Handle result
try:
    result = pydgraph.DgraphClient.handle_alter_future(future)
except Exception as e:
    if pydgraph.util.is_jwt_expired(e):
        # Refresh token and retry
        pass
```

### async_query and async_mutation

```python
txn = client.txn()

# Async query
query_future = txn.async_query(query_string)
result = pydgraph.Txn.handle_query_future(query_future)

# Async mutation
mutation_future = txn.async_mutation(set_obj=data)
result = pydgraph.Txn.handle_mutate_future(mutation_future)
```

**Note**: Async methods use gRPC futures, not native Python asyncio. They cannot retry on JWT expiration.

## ACL and Authentication

### Login

```python
# Login with credentials
client.login("groot", "password")

# Login with namespace (multi-tenancy)
client.login_into_namespace("user", "password", namespace=1)
```

### Refresh Token

```python
# Tokens expire - refresh periodically
client.retry_login()
```

## Error Handling

```python
import grpc

try:
    response = txn.mutate(set_obj=data)
    txn.commit()
except grpc.RpcError as e:
    if e.code() == grpc.StatusCode.ABORTED:
        # Transaction conflict - retry
        pass
    elif e.code() == grpc.StatusCode.UNAUTHENTICATED:
        # JWT expired
        client.retry_login()
except pydgraph.errors.TransactionError as e:
    # Transaction-specific error
    pass
finally:
    txn.discard()
```

## Performance Considerations

### Batch Mutations

```python
# Accumulate mutations, commit in batches
txn = client.txn()
batch = []

for item in large_dataset:
    batch.append(item)
    if len(batch) >= 1000:
        txn.mutate(set_obj=batch)
        batch = []

if batch:
    txn.mutate(set_obj=batch)

txn.commit()
```

### Connection Reuse

```python
# Reuse client and stubs across requests
# Create once at application startup
```

## Limitations

- gRPC futures not native asyncio
- No connection pooling (manage stubs manually)
- No OGM layer included
- DQL learning curve (different from Cypher/Gremlin)
- Limited IDE support for DQL
- No built-in migration tooling

## When to Use

**Choose pydgraph when:**
- Distributed, horizontally scalable graph needed
- GraphQL-native development preferred
- Multi-tenancy (namespaces) required
- Integration with Dgraph Cloud
- High-write throughput scenarios

**Consider alternatives when:**
- Native asyncio critical
- OGM patterns preferred
- Cypher or Gremlin expertise exists
- Smaller scale deployments

## Resources

- [Dgraph Documentation](https://docs.hypermode.com/dgraph/)
- [GitHub Repository](https://github.com/hypermodeinc/pydgraph)
- [DQL Query Language](https://docs.hypermode.com/dgraph/dql/)
- [PyPI Package](https://pypi.org/project/pydgraph/)
- [Dgraph Cloud](https://cloud.dgraph.io/)
