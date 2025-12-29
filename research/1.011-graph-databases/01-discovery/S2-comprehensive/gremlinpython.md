# gremlinpython - Apache TinkerPop Gremlin Client

## Overview

gremlinpython is the official Python language variant (GLV) for Apache TinkerPop's Gremlin graph traversal language. It provides a consistent API for interacting with any TinkerPop-enabled graph database, offering database portability through a standardized query language.

## Key Information

| Attribute | Value |
|-----------|-------|
| Package | `gremlinpython` |
| Version | 3.7.x |
| Python Support | 3.10+ |
| Protocol | WebSocket (GraphBinary/GraphSON) |
| License | Apache 2.0 |
| Repository | github.com/apache/tinkerpop |

## Supported Databases

gremlinpython works with any TinkerPop-compliant database:
- Amazon Neptune
- Azure Cosmos DB (Gremlin API)
- JanusGraph
- OrientDB
- Neo4j (with TinkerPop plugin)
- TigerGraph (with TinkerPop connector)
- DataStax Graph

## Installation

```bash
pip install gremlinpython
```

## Connection Management

### Basic Connection

```python
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

# Create traversal source
g = traversal().with_remote(
    DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
)

# With authentication
g = traversal().with_remote(
    DriverRemoteConnection(
        'wss://your-endpoint:8182/gremlin',
        'g',
        username='user',
        password='password'
    )
)
```

### Connection Options

```python
from gremlin_python.driver.client import Client

# Lower-level client access
client = Client(
    'ws://localhost:8182/gremlin',
    'g',
    pool_size=8,           # Connection pool size
    max_workers=4,         # Thread pool workers
    message_serializer=None # Custom serializer
)

# Submit raw Gremlin
result = client.submit("g.V().count()")
for r in result:
    print(r)
```

## Traversal Basics

### Creating Vertices

```python
# Add vertex
g.addV('person').property('name', 'Alice').property('age', 30).next()

# Add with ID
g.addV('person').property(T.id, 'alice').property('name', 'Alice').next()
```

### Creating Edges

```python
# Add edge between vertices
g.V().has('person', 'name', 'Alice').as_('a') \
     .V().has('person', 'name', 'Bob').as_('b') \
     .addE('knows').from_('a').to('b').property('since', 2020).next()
```

### Reading Data

```python
# Get all vertices of type
people = g.V().hasLabel('person').toList()

# Get specific vertex
alice = g.V().has('person', 'name', 'Alice').next()

# Get vertex properties
props = g.V().has('person', 'name', 'Alice').valueMap().next()
```

### Updating Data

```python
# Update property
g.V().has('person', 'name', 'Alice') \
     .property('age', 31).next()

# Add multiple properties
g.V().has('person', 'name', 'Alice') \
     .property('email', 'alice@example.com') \
     .property('city', 'NYC').next()
```

### Deleting Data

```python
# Delete vertex (and connected edges)
g.V().has('person', 'name', 'Alice').drop().iterate()

# Delete edge
g.E().hasLabel('knows').drop().iterate()
```

## Traversal Patterns

### Filtering

```python
# Has filters
g.V().has('person', 'age', P.gt(25)).toList()
g.V().has('person', 'name', P.within('Alice', 'Bob')).toList()

# Multiple conditions
g.V().hasLabel('person') \
     .has('age', P.gte(18)) \
     .has('age', P.lt(65)).toList()

# Not filter
g.V().hasLabel('person').not_(__.has('retired', True)).toList()
```

### Traversing Relationships

```python
# Outgoing edges
friends = g.V().has('person', 'name', 'Alice').out('knows').toList()

# Incoming edges
followers = g.V().has('person', 'name', 'Alice').in_('follows').toList()

# Both directions
connections = g.V().has('person', 'name', 'Alice').both('knows').toList()

# Multiple hops
friends_of_friends = g.V().has('person', 'name', 'Alice') \
                          .out('knows').out('knows') \
                          .dedup().toList()
```

### Path Queries

```python
# Get paths
paths = g.V().has('person', 'name', 'Alice') \
             .repeat(__.out('knows')).times(2) \
             .path().by('name').toList()

# Shortest path
path = g.V().has('person', 'name', 'Alice') \
            .repeat(__.out().simplePath()) \
            .until(__.has('person', 'name', 'Charlie')) \
            .path().limit(1).next()
```

### Aggregation

```python
# Count
count = g.V().hasLabel('person').count().next()

# Group by
by_age = g.V().hasLabel('person') \
              .group().by('age').by(__.count()).next()

# Statistics
stats = g.V().hasLabel('person') \
             .values('age').fold() \
             .project('min', 'max', 'avg', 'count') \
             .by(__.min()) \
             .by(__.max()) \
             .by(__.mean()) \
             .by(__.count()).next()
```

## Serialization

### GraphBinary (Recommended)

```python
from gremlin_python.driver.serializer import GraphBinarySerializersV1

g = traversal().with_remote(
    DriverRemoteConnection(
        'ws://localhost:8182/gremlin',
        'g',
        message_serializer=GraphBinarySerializersV1()
    )
)
```

### GraphSON

```python
from gremlin_python.driver.serializer import GraphSONSerializersV3d0

g = traversal().with_remote(
    DriverRemoteConnection(
        'ws://localhost:8182/gremlin',
        'g',
        message_serializer=GraphSONSerializersV3d0()
    )
)
```

## Transaction Support

```python
# Begin transaction
tx = g.tx()

# Get transaction-bound traversal
gtx = tx.begin()

try:
    gtx.addV('person').property('name', 'Alice').next()
    gtx.addV('person').property('name', 'Bob').next()
    tx.commit()
except:
    tx.rollback()
    raise
```

## Async Alternatives

gremlinpython itself is synchronous. For async support, consider:

### aiogremlin

```python
from aiogremlin import Cluster, Graph

cluster = await Cluster.open(hosts=['localhost'])
client = await cluster.connect()
g = Graph().traversal().withRemote(client)

# Async operations
result = await g.V().toList()
```

### Goblin OGM

```python
from goblin import Goblin, Vertex, String

class Person(Vertex):
    name = String()

app = await Goblin.open(hosts=['localhost'])
session = await app.session()

person = Person(name='Alice')
session.add(person)
await session.flush()
```

### gremlinpy (FastAPI compatible)

```python
from gremlinpy import Graph

g = Graph().traversal()
# Compatible with existing event loops
```

## Traversal Strategies

```python
from gremlin_python.process.strategies import *

# Read-only strategy
g = g.withStrategies(ReadOnlyStrategy())

# Subgraph strategy (filter)
g = g.withStrategies(SubgraphStrategy(
    vertices=__.hasLabel('person'),
    edges=__.hasLabel('knows')
))

# Partition strategy
g = g.withStrategies(PartitionStrategy(
    partitionKey='region',
    writePartition='us-west'
))
```

## Error Handling

```python
from gremlin_python.driver.protocol import GremlinServerError

try:
    result = g.V().has('invalid').next()
except GremlinServerError as e:
    print(f"Server error: {e}")
except StopIteration:
    print("No results found")
```

## Connection Pooling Issues

Known limitation (TINKERPOP-3114):
> "Once a connection error occurred, pooled connections are broken and will not be recovered."

Workaround:
```python
# Implement connection health checks
def get_connection():
    try:
        g.V().limit(1).next()
        return g
    except:
        # Reconnect
        return create_new_connection()
```

## Limitations

- No native Python asyncio (use aiogremlin/goblin)
- Connection pool recovery issues
- WebSocket-only protocol
- Remote execution only (no embedded mode)
- Reference-only objects from server (no full properties)
- Significant memory overhead for large result sets

## When to Use

**Choose gremlinpython when:**
- Database portability is important
- Working with TinkerPop-compatible databases
- Standard graph query language preferred
- Amazon Neptune or Azure Cosmos DB target

**Consider alternatives when:**
- Native async required (use aiogremlin/goblin)
- Database-specific features needed
- Maximum performance critical
- OGM patterns preferred (use goblin)

## Resources

- [TinkerPop Documentation](https://tinkerpop.apache.org/docs/current/reference/)
- [Practical Gremlin Book](https://www.kelvinlawrence.net/book/PracticalGremlin.html)
- [PyPI Package](https://pypi.org/project/gremlinpython/)
- [Apache TinkerPop](https://tinkerpop.apache.org/)
- [Goblin OGM](https://goblin.readthedocs.io/)
- [aiogremlin](https://aiogremlin.readthedocs.io/)
