# Neo4j Python Driver (neo4j)

## Overview

The official Neo4j Python driver provides low-level, high-performance access to Neo4j databases using the Bolt protocol. Maintained by Neo4j Inc., it serves as the foundation for higher-level libraries like neomodel.

## Key Information

| Attribute | Value |
|-----------|-------|
| Package | `neo4j` (formerly `neo4j-driver`) |
| Version | 6.0.x |
| Python Support | 3.10, 3.11, 3.12, 3.13, 3.14 |
| Protocol | Bolt 4.4, 5.0-5.8, 6.0 |
| License | Apache 2.0 |
| Repository | github.com/neo4j/neo4j-python-driver |

## Installation

```bash
pip install neo4j

# With optional Rust extensions for performance
pip install neo4j-rust-ext
```

## Core Features

### Connection Management

```python
from neo4j import GraphDatabase

# Basic connection
driver = GraphDatabase.driver(
    "neo4j://localhost:7687",
    auth=("neo4j", "password")
)

# With context manager (recommended)
with GraphDatabase.driver(uri, auth=auth) as driver:
    driver.verify_connectivity()
    # Use driver...
```

### Query Execution

```python
# Simple query execution (v5.0+)
records, summary, keys = driver.execute_query(
    "MATCH (p:Person {name: $name}) RETURN p",
    name="Alice",
    database_="neo4j"
)

# With routing control
from neo4j import RoutingControl

records, summary, keys = driver.execute_query(
    "MATCH (p:Person) RETURN p",
    routing_=RoutingControl.READ
)
```

### Session-Based Transactions

```python
with driver.session(database="neo4j") as session:
    # Managed transaction (recommended - auto-retry)
    result = session.execute_read(
        lambda tx: tx.run("MATCH (p:Person) RETURN p").data()
    )

    # Write transaction
    session.execute_write(
        lambda tx: tx.run(
            "CREATE (p:Person {name: $name})",
            name="Bob"
        )
    )
```

## Async Support

Full async/await support mirrors the synchronous API:

```python
from neo4j import AsyncGraphDatabase

async def main():
    async with AsyncGraphDatabase.driver(uri, auth=auth) as driver:
        async with driver.session() as session:
            result = await session.execute_read(
                lambda tx: tx.run("MATCH (n) RETURN n").data()
            )
```

### Async Features

- `AsyncDriver`, `AsyncSession`, `AsyncTransaction`
- `AsyncResult` with async iteration
- Compatible with asyncio, FastAPI, aiohttp
- Shares non-I/O components with sync implementation

## Connection Pooling

### Configuration Options

```python
driver = GraphDatabase.driver(
    uri, auth=auth,
    max_connection_pool_size=100,        # Max connections per host
    connection_acquisition_timeout=60,    # Seconds to wait for connection
    connection_timeout=30,                # TCP connection timeout
    max_connection_lifetime=3600,         # Max age of pooled connection
    liveness_check_timeout=60             # Idle check threshold
)
```

### Best Practices

- Create one driver instance per application
- Driver objects are expensive to create (connection pool setup)
- Sessions are lightweight - create/close as needed
- Use context managers for automatic resource cleanup

## Transaction Support

### Transaction Types

1. **Auto-commit**: Single statement, no retry
   ```python
   session.run("CREATE (n:Node)")
   ```

2. **Managed Transactions**: Recommended - includes retry logic
   ```python
   session.execute_read(work_function)
   session.execute_write(work_function)
   ```

3. **Explicit Transactions**: Manual control
   ```python
   tx = session.begin_transaction()
   try:
       tx.run(query)
       tx.commit()
   except:
       tx.rollback()
   ```

### Causal Consistency

```python
# Bookmark management for causal chains
with driver.session(bookmarks=[bookmark]) as session:
    session.execute_write(work)
    new_bookmark = session.last_bookmark()
```

## Error Handling

```python
from neo4j.exceptions import (
    ServiceUnavailable,
    TransientError,
    ClientError,
    DatabaseError
)

try:
    driver.execute_query(query)
except ServiceUnavailable:
    # Connection/cluster issues
except TransientError:
    # Retryable errors (deadlock, etc.)
except ClientError:
    # Query syntax, constraint violations
```

## Type System

### Neo4j to Python Type Mapping

| Neo4j Type | Python Type |
|------------|-------------|
| Integer | int |
| Float | float |
| String | str |
| Boolean | bool |
| List | list |
| Map | dict |
| Node | neo4j.graph.Node |
| Relationship | neo4j.graph.Relationship |
| Path | neo4j.graph.Path |
| Date | datetime.date |
| DateTime | datetime.datetime |
| Duration | neo4j.time.Duration |
| Point | neo4j.spatial.Point |

## Performance Optimization

### Rust Extensions

```bash
pip install neo4j-rust-ext
```

- Drop-in replacement for default transport
- Significant performance improvement for I/O-heavy workloads
- No code changes required

### Bulk Operations

```python
# Batch create with UNWIND
session.execute_write(lambda tx: tx.run(
    "UNWIND $batch AS row CREATE (n:Node {id: row.id, name: row.name})",
    batch=[{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
))
```

## Testing

```python
# Use testcontainers for integration tests
from testcontainers.neo4j import Neo4jContainer

with Neo4jContainer() as neo4j:
    driver = GraphDatabase.driver(
        neo4j.get_connection_url(),
        auth=("neo4j", neo4j.NEO4J_ADMIN_PASSWORD)
    )
```

## Limitations

- No built-in ORM/OGM (use neomodel for that)
- Cypher-only (no Gremlin support)
- Manual schema management required
- No migration tooling included

## When to Use

**Choose neo4j-driver when:**
- Direct control over queries and transactions is needed
- Performance is critical (with Rust extensions)
- Building custom abstractions on top
- Async support is required

**Consider alternatives when:**
- OGM patterns would simplify development (use neomodel)
- Multi-database portability is needed (use gremlinpython)

## Resources

- [Python Driver Manual](https://neo4j.com/docs/python-manual/current/)
- [API Documentation](https://neo4j.com/docs/api/python-driver/current/)
- [GitHub Repository](https://github.com/neo4j/neo4j-python-driver)
