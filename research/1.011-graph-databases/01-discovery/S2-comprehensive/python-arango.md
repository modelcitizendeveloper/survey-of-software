# python-arango - ArangoDB Python Driver

## Overview

python-arango is the official Python driver for ArangoDB, providing comprehensive access to ArangoDB's multi-model capabilities including document, graph, and key-value operations. It offers a Pythonic interface to ArangoDB's REST API.

## Key Information

| Attribute | Value |
|-----------|-------|
| Package | `python-arango` |
| Version | 8.2.x |
| Python Support | 3.9+ |
| ArangoDB Support | 3.11+ |
| Protocol | HTTP REST |
| License | MIT |
| Repository | github.com/arangodb/python-arango |

## Installation

```bash
pip install python-arango

# For async support (separate package)
pip install python-arango-async
```

## Connection Management

### Basic Connection

```python
from arango import ArangoClient

# Initialize client
client = ArangoClient(hosts="http://localhost:8529")

# Connect to database
db = client.db("mydb", username="root", password="password")

# System database for admin operations
sys_db = client.db("_system", username="root", password="password")
```

### Connection Options

```python
client = ArangoClient(
    hosts="http://localhost:8529",
    http_client=None,          # Custom HTTP client
    serializer=None,           # Custom JSON serializer
    deserializer=None          # Custom JSON deserializer
)
```

## Document Operations

### Basic CRUD

```python
# Get collection
collection = db.collection("users")

# Insert
metadata = collection.insert({"name": "Alice", "age": 30})
# Returns: {'_id': 'users/12345', '_key': '12345', '_rev': '_abc123'}

# Get by key
doc = collection.get("12345")

# Update
collection.update({"_key": "12345", "age": 31})

# Replace
collection.replace({"_key": "12345", "name": "Alice", "age": 31})

# Delete
collection.delete("12345")
```

### Batch Operations

```python
# Batch insert
docs = [{"name": f"User{i}"} for i in range(1000)]
results = collection.insert_many(docs)

# Batch update
updates = [{"_key": key, "status": "active"} for key in keys]
collection.update_many(updates)

# Batch delete
collection.delete_many([{"_key": k} for k in keys])
```

## AQL Queries

### Query Execution

```python
# Simple query
cursor = db.aql.execute(
    "FOR doc IN users FILTER doc.age > @min_age RETURN doc",
    bind_vars={"min_age": 25}
)

# Iterate results
for doc in cursor:
    print(doc)

# Get all results as list
results = cursor.batch()
```

### Query Options

```python
cursor = db.aql.execute(
    query,
    bind_vars={"param": value},
    count=True,           # Include count
    batch_size=100,       # Results per batch
    ttl=3600,             # Cursor TTL in seconds
    max_runtime=30.0,     # Max execution time
    profile=True          # Include query profile
)

# Access statistics
print(cursor.statistics())
print(cursor.profile())
```

## Graph Operations

### Graph Management

```python
# Create graph
graph = db.create_graph(
    "social",
    edge_definitions=[{
        "edge_collection": "knows",
        "from_vertex_collections": ["users"],
        "to_vertex_collections": ["users"]
    }]
)

# Get existing graph
graph = db.graph("social")
```

### Vertex Operations

```python
# Get vertex collection
users = graph.vertex_collection("users")

# Insert vertex
users.insert({"_key": "alice", "name": "Alice"})

# Get vertex
alice = users.get("alice")

# Update vertex
users.update({"_key": "alice", "age": 30})
```

### Edge Operations

```python
# Get edge collection
knows = graph.edge_collection("knows")

# Insert edge
knows.insert({
    "_from": "users/alice",
    "_to": "users/bob",
    "since": 2020
})

# Traverse graph
result = graph.traverse(
    start_vertex="users/alice",
    direction="outbound",
    max_depth=2
)
```

## Async Support

### python-arango-async (Separate Package)

```python
from arangoasync import ArangoClient
from arangoasync.auth import Auth

async with ArangoClient(hosts="http://localhost:8529") as client:
    auth = Auth(username="root", password="password")
    db = await client.db("mydb", auth=auth)

    # Async operations
    collection = db.collection("users")
    await collection.insert({"name": "Alice"})

    cursor = await db.aql.execute("FOR doc IN users RETURN doc")
    async for doc in cursor:
        print(doc)
```

### Fire-and-Forget Async (python-arango)

```python
# Create async execution context
async_db = db.begin_async_execution(return_result=True)

# Queue operations
job1 = async_db.collection("users").insert({"name": "Alice"})
job2 = async_db.collection("users").insert({"name": "Bob"})

# Check job status
print(job1.status())  # 'pending', 'done', or 'error'

# Get results when ready
result1 = job1.result()
```

## Transaction Support

### Single Request Transactions

```python
# Stream transaction
txn = db.begin_transaction(
    read=["users"],
    write=["orders"]
)

try:
    txn.collection("users").insert({"name": "Alice"})
    txn.collection("orders").insert({"item": "Book"})
    txn.commit()
except:
    txn.abort()
    raise
```

### JavaScript Transactions

```python
# Server-side transaction with JavaScript
result = db.transaction(
    read=["users"],
    write=["orders"],
    action="""
        function(params) {
            const db = require('@arangodb').db;
            const user = db.users.insert({name: params.name});
            return user;
        }
    """,
    params={"name": "Alice"}
)
```

## Index Management

```python
# Create persistent index
collection.add_persistent_index(
    fields=["name", "email"],
    unique=True,
    sparse=False
)

# Create geo index
collection.add_geo_index(
    fields=["location"],
    geo_json=True
)

# Create fulltext index (deprecated, use ArangoSearch)
collection.add_fulltext_index(
    fields=["description"],
    min_length=3
)

# List indexes
for index in collection.indexes():
    print(index)
```

## ArangoSearch Views

```python
# Create search view
db.create_arangosearch_view(
    name="users_view",
    properties={
        "links": {
            "users": {
                "analyzers": ["text_en"],
                "fields": {
                    "name": {},
                    "bio": {"analyzers": ["text_en"]}
                }
            }
        }
    }
)

# Search query
cursor = db.aql.execute("""
    FOR doc IN users_view
    SEARCH ANALYZER(doc.bio == "developer", "text_en")
    RETURN doc
""")
```

## Error Handling

```python
from arango.exceptions import (
    ArangoError,
    DocumentInsertError,
    DocumentGetError,
    AQLQueryExecuteError,
    TransactionAbortError
)

try:
    collection.insert({"_key": "duplicate"})
except DocumentInsertError as e:
    print(f"Error code: {e.error_code}")
    print(f"HTTP status: {e.http_code}")
    print(f"Message: {e.error_message}")
except ArangoError as e:
    # Generic error handling
    pass
```

## Foxx Microservices

```python
# Install Foxx service
db.foxx.install(
    mount="/myapp",
    source="https://github.com/user/foxx-service/archive/main.zip"
)

# Call Foxx endpoint
response = db.foxx.request(
    method="POST",
    mount="/myapp",
    path="/api/endpoint",
    data={"param": "value"}
)
```

## Cluster Support

```python
# Cluster health
health = sys_db.cluster.server_health()

# Cluster statistics
stats = sys_db.cluster.statistics()

# Rebalance shards
sys_db.cluster.rebalance_shards()
```

## Limitations

- No native Python asyncio in main package (use python-arango-async)
- No OGM layer (document-centric design)
- HTTP protocol only (no binary protocol)
- Fire-and-forget async differs from true async

## When to Use

**Choose python-arango when:**
- Multi-model database needed (document + graph + key-value)
- AQL query language preferred
- Microservice architecture (Foxx)
- Horizontal scaling required

**Consider alternatives when:**
- Pure graph database needed (use Neo4j)
- Native asyncio critical (use python-arango-async)
- Gremlin compatibility needed (use gremlinpython)

## Resources

- [Documentation](https://docs.python-arango.com/)
- [GitHub Repository](https://github.com/arangodb/python-arango)
- [Async Driver](https://github.com/arangodb/python-arango-async)
- [ArangoDB Documentation](https://docs.arangodb.com/)
