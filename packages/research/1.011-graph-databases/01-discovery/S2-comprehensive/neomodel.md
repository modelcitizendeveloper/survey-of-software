# neomodel - Neo4j Object Graph Mapper

## Overview

neomodel is a Python Object Graph Mapper (OGM) for Neo4j that provides Django-style model definitions for graph data. It allows developers to work with graph data using Pythonic patterns without writing raw Cypher queries.

## Key Information

| Attribute | Value |
|-----------|-------|
| Package | `neomodel` |
| Version | 6.0.x |
| Python Support | 3.8+ |
| Protocol | Bolt (via neo4j-driver) |
| License | MIT |
| Repository | github.com/neo4j-contrib/neomodel |
| Status | Neo4j Labs (actively maintained) |

## Installation

```bash
pip install neomodel

# With extras (includes Shapely for spatial data)
pip install neomodel[extras]

# With Rust driver extensions for performance
pip install neomodel[rust-driver-ext]
```

## Configuration

```python
from neomodel import config

# Connection string
config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'

# Or using dataclass configuration (v6.0+)
from neomodel import NeomodelConfig

config = NeomodelConfig(
    driver_options={"max_connection_pool_size": 50},
    database="neo4j",
    auto_install_labels=True
)
```

### Environment Variables

```bash
NEO4J_BOLT_URL=bolt://neo4j:password@localhost:7687
NEO4J_DATABASE=neo4j
```

## Model Definition

### Basic Node Definition

```python
from neomodel import (
    StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, RelationshipFrom
)

class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    age = IntegerProperty(index=True)

    # Relationships
    friends = RelationshipTo('Person', 'FRIENDS_WITH')
    employer = RelationshipTo('Company', 'WORKS_AT')
```

### Property Types

```python
from neomodel import (
    StringProperty,      # String values
    IntegerProperty,     # Integer values
    FloatProperty,       # Floating point
    BooleanProperty,     # Boolean
    DateProperty,        # datetime.date
    DateTimeProperty,    # datetime.datetime
    UniqueIdProperty,    # Auto-generated UUID
    ArrayProperty,       # Lists
    JSONProperty,        # JSON-serializable dicts
    PointProperty,       # Spatial data
)
```

### Relationship Properties

```python
from neomodel import StructuredRel, DateTimeProperty

class WorkedAt(StructuredRel):
    start_date = DateTimeProperty()
    end_date = DateTimeProperty()
    role = StringProperty()

class Person(StructuredNode):
    name = StringProperty()
    employers = RelationshipTo('Company', 'WORKED_AT', model=WorkedAt)
```

## CRUD Operations

### Create

```python
# Create single node
person = Person(name="Alice", age=30).save()

# Create with relationships
company = Company(name="Acme").save()
person.employer.connect(company)
```

### Read

```python
# Get by property
alice = Person.nodes.get(name="Alice")

# Filter nodes
adults = Person.nodes.filter(age__gte=18)

# All nodes
all_people = Person.nodes.all()

# First match
first_person = Person.nodes.first()
```

### Update

```python
person = Person.nodes.get(name="Alice")
person.age = 31
person.save()
```

### Delete

```python
person = Person.nodes.get(name="Alice")
person.delete()
```

## Query API

### Filtering

```python
# Comparison operators
Person.nodes.filter(age__gt=25)      # Greater than
Person.nodes.filter(age__gte=25)     # Greater or equal
Person.nodes.filter(age__lt=25)      # Less than
Person.nodes.filter(age__lte=25)     # Less or equal
Person.nodes.filter(name__ne="Bob")  # Not equal

# String operators
Person.nodes.filter(name__contains="ali")
Person.nodes.filter(name__startswith="A")
Person.nodes.filter(name__endswith="ce")
Person.nodes.filter(name__icontains="ALI")  # Case insensitive

# List operations
Person.nodes.filter(name__in=["Alice", "Bob"])
```

### Traversal (v6.0+)

```python
# Advanced traversal with filtering and ordering
results = Person.nodes.filter(name="Alice").traverse(
    relation_type="FRIENDS_WITH",
    filter_expr={"age__gte": 18},
    order_by="age"
)
```

### Raw Cypher

```python
from neomodel import db

results, meta = db.cypher_query(
    "MATCH (p:Person) WHERE p.age > $age RETURN p",
    {"age": 25}
)
```

## Async Support

```python
from neomodel import adb, AsyncStructuredNode

class Person(AsyncStructuredNode):
    name = StringProperty()

async def main():
    # Async operations
    person = await Person(name="Alice").save()
    alice = await Person.nodes.get(name="Alice")
    await person.delete()

    # Async traversal
    friends = await alice.friends.all()
```

### Async Configuration

```python
from neomodel import adb

await adb.set_connection("bolt://localhost:7687")
```

## Schema Management

### Constraints and Indexes

```python
from neomodel import install_all_labels, install_labels

# Install all constraints and indexes
install_all_labels()

# Install for specific models
install_labels(Person)
```

### Schema Definition

```python
class Person(StructuredNode):
    # Unique constraint
    email = StringProperty(unique_index=True)

    # Index only
    name = StringProperty(index=True)

    # Required (not null)
    created = DateTimeProperty(required=True)
```

## Hooks

```python
class Person(StructuredNode):
    name = StringProperty()

    def pre_save(self):
        # Called before saving
        self.name = self.name.strip()

    def post_save(self):
        # Called after saving
        log.info(f"Saved {self.name}")

    def pre_delete(self):
        # Called before deletion
        pass

    def post_delete(self):
        # Called after deletion
        pass
```

## Transaction Support

```python
from neomodel import db

# Context manager
with db.transaction:
    person = Person(name="Alice").save()
    company = Company(name="Acme").save()
    person.employer.connect(company)

# Explicit control
db.begin()
try:
    person = Person(name="Alice").save()
    db.commit()
except:
    db.rollback()
    raise
```

## Django Integration

```python
# settings.py
NEOMODEL_NEO4J_BOLT_URL = 'bolt://neo4j:password@localhost:7687'

# models.py
from django_neomodel import DjangoNode
from neomodel import StringProperty

class Person(DjangoNode):
    name = StringProperty()

    class Meta:
        app_label = 'myapp'
```

## Vector and Full-Text Search (v6.0+)

```python
from neomodel import VectorIndex, FullTextIndex

class Document(StructuredNode):
    content = StringProperty()
    embedding = ArrayProperty()

    # Vector index for semantic search
    __vector_index__ = VectorIndex(
        property_name='embedding',
        dimensions=384
    )

    # Full-text index
    __fulltext_index__ = FullTextIndex(
        property_names=['content']
    )
```

## Performance Considerations

### Batch Operations

```python
# Use batch_save for bulk inserts
from neomodel import db

with db.transaction:
    for data in large_dataset:
        Person(name=data['name']).save()
```

### Connection Pooling

Inherited from neo4j-driver configuration - set via `driver_options` in config.

## Limitations

- Neo4j-specific (no multi-database portability)
- No automatic migration tooling (schema drift possible)
- OGM overhead vs. raw Cypher
- Complex traversals may require raw Cypher

## When to Use

**Choose neomodel when:**
- Django-like model patterns preferred
- Type safety and validation important
- Schema enforcement needed
- Working primarily with Neo4j

**Consider alternatives when:**
- Maximum performance required (use neo4j-driver)
- Multi-database support needed (use gremlinpython)
- Complex graph algorithms (use raw Cypher)

## Resources

- [Documentation](https://neomodel.readthedocs.io/)
- [Neo4j Labs Page](https://neo4j.com/labs/neomodel/)
- [GitHub Repository](https://github.com/neo4j-contrib/neomodel)
- [Django Integration](https://github.com/neo4j-contrib/django-neomodel)
