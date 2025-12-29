# rdflib - RDF Graph Library for Python

## Overview

rdflib is a pure Python library for working with RDF (Resource Description Framework) data. It provides comprehensive support for parsing, serializing, and querying RDF graphs using SPARQL, making it the standard choice for semantic web and linked data applications in Python.

## Key Information

| Attribute | Value |
|-----------|-------|
| Package | `rdflib` |
| Version | 7.2.x |
| Python Support | 3.8+ |
| Query Language | SPARQL 1.1 |
| License | BSD-3-Clause |
| Repository | github.com/RDFLib/rdflib |

## Installation

```bash
pip install rdflib

# With optional dependencies
pip install rdflib[html,lxml]
```

## Core Concepts

### RDF Triples

RDF data consists of triples: (subject, predicate, object)

```python
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, FOAF, XSD

# Create graph
g = Graph()

# Define namespace
EX = Namespace("http://example.org/")

# Add triple
g.add((
    EX.alice,                           # Subject
    FOAF.name,                          # Predicate
    Literal("Alice", datatype=XSD.string)  # Object
))
```

### Node Types

```python
from rdflib import URIRef, Literal, BNode

# URI Reference (resources)
person = URIRef("http://example.org/alice")

# Literal (values)
name = Literal("Alice")
age = Literal(30, datatype=XSD.integer)
name_en = Literal("Alice", lang="en")

# Blank Node (anonymous)
address = BNode()
```

## Graph Operations

### Creating and Populating Graphs

```python
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, FOAF

g = Graph()

# Bind namespace prefix
g.bind("foaf", FOAF)
g.bind("ex", EX)

# Add triples
alice = URIRef("http://example.org/alice")
bob = URIRef("http://example.org/bob")

g.add((alice, RDF.type, FOAF.Person))
g.add((alice, FOAF.name, Literal("Alice")))
g.add((alice, FOAF.knows, bob))

g.add((bob, RDF.type, FOAF.Person))
g.add((bob, FOAF.name, Literal("Bob")))
```

### Querying Triples

```python
# All triples
for s, p, o in g:
    print(s, p, o)

# Specific patterns
for person in g.subjects(RDF.type, FOAF.Person):
    name = g.value(person, FOAF.name)
    print(f"{person}: {name}")

# Check existence
if (alice, FOAF.knows, bob) in g:
    print("Alice knows Bob")
```

### Removing Triples

```python
# Remove specific triple
g.remove((alice, FOAF.knows, bob))

# Remove by pattern (None = wildcard)
g.remove((alice, None, None))  # Remove all triples about Alice
```

## SPARQL Queries

### SELECT Queries

```python
query = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?name ?friend
    WHERE {
        ?person a foaf:Person ;
                foaf:name ?name ;
                foaf:knows ?friendUri .
        ?friendUri foaf:name ?friend .
    }
"""

for row in g.query(query):
    print(f"{row.name} knows {row.friend}")
```

### ASK Queries

```python
query = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    ASK {
        ?person foaf:name "Alice" .
    }
"""

result = g.query(query)
print(bool(result))  # True or False
```

### CONSTRUCT Queries

```python
query = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX ex: <http://example.org/>

    CONSTRUCT {
        ?person ex:displayName ?name .
    }
    WHERE {
        ?person foaf:name ?name .
    }
"""

result_graph = g.query(query).graph
```

### Parameterized Queries

```python
from rdflib.plugins.sparql import prepareQuery

query = prepareQuery("""
    SELECT ?name
    WHERE {
        ?person foaf:name ?name .
    }
""", initNs={"foaf": FOAF})

# With initial bindings
results = g.query(
    query,
    initBindings={'person': alice}
)
```

### SPARQL Update

```python
update = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    INSERT DATA {
        <http://example.org/charlie> a foaf:Person ;
            foaf:name "Charlie" .
    }
"""

g.update(update)
```

## Serialization

### Parsing RDF

```python
# Parse from file
g.parse("data.ttl", format="turtle")

# Parse from URL
g.parse("http://example.org/data.rdf")

# Parse from string
g.parse(data=rdf_string, format="turtle")

# Supported formats
formats = ["xml", "turtle", "n3", "nt", "nquads", "trig", "json-ld"]
```

### Serializing RDF

```python
# Serialize to string
turtle = g.serialize(format="turtle")
jsonld = g.serialize(format="json-ld")

# Serialize to file
g.serialize("output.ttl", format="turtle")

# Available formats
# RDF/XML, N3, NTriples, N-Quads, Turtle, TriG, TriX, JSON-LD, HexTuples
```

## Persistence

### In-Memory (Default)

```python
g = Graph()  # Default in-memory store
```

### Berkeley DB

```python
from rdflib import Graph
from rdflib.plugins.stores import BerkeleyDB

store = BerkeleyDB()
g = Graph(store, identifier="mygraph")
g.open("/path/to/store", create=True)

# Use graph...

g.close()
```

### SQLite (via rdflib-sqlalchemy)

```python
# pip install rdflib-sqlalchemy
from rdflib import Graph, ConjunctiveGraph
from rdflib_sqlalchemy import registerplugins

registerplugins()

g = Graph(store="SQLAlchemy", identifier="mygraph")
g.open("sqlite:///graph.db", create=True)
```

## Remote SPARQL Endpoints

### SPARQLWrapper

```python
# pip install sparqlwrapper
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    SELECT ?label
    WHERE {
        <http://dbpedia.org/resource/Python_(programming_language)>
            rdfs:label ?label .
        FILTER (lang(?label) = 'en')
    }
""")
sparql.setReturnFormat(JSON)

results = sparql.query().convert()
```

### Federated Queries

```python
query = """
    SELECT ?name ?abstract
    WHERE {
        ?person foaf:name ?name .
        SERVICE <http://dbpedia.org/sparql> {
            ?dbperson rdfs:label ?name ;
                      dbo:abstract ?abstract .
            FILTER (lang(?abstract) = 'en')
        }
    }
"""
```

## Named Graphs and Datasets

### Conjunctive Graph

```python
from rdflib import ConjunctiveGraph, URIRef

# Dataset with multiple named graphs
ds = ConjunctiveGraph()

# Add to specific graph
graph1 = URIRef("http://example.org/graph1")
ds.add((alice, FOAF.name, Literal("Alice"), graph1))

# Query across graphs
for ctx in ds.contexts():
    print(f"Graph: {ctx.identifier}")
```

### Dataset

```python
from rdflib import Dataset

ds = Dataset()
g1 = ds.graph(URIRef("http://example.org/graph1"))
g1.add((alice, FOAF.name, Literal("Alice")))
```

## Custom SPARQL Functions

```python
from rdflib.plugins.sparql.operators import register_custom_function
from rdflib import Literal, URIRef

def custom_uppercase(value):
    return Literal(str(value).upper())

# Register function
register_custom_function(
    URIRef("http://example.org/uppercase"),
    custom_uppercase
)

# Use in query
query = """
    SELECT (ex:uppercase(?name) AS ?upper)
    WHERE { ?person foaf:name ?name }
"""
```

## Async Support

rdflib is synchronous. For async operations:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

async def async_query(graph, query):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor,
        lambda: list(graph.query(query))
    )
```

## Inference and Reasoning

### RDFS Inference

```python
from rdflib import Graph
from rdflib.plugins.stores.memory import IOMemory

# Enable RDFS reasoning
from rdflib import RDF, RDFS

g = Graph()
g.parse("ontology.ttl")

# Manual inference example
for s, _, o in g.triples((None, RDFS.subClassOf, None)):
    # Infer types based on subclass
    pass
```

### OWL-RL (via owlrl)

```python
# pip install owlrl
import owlrl

g = Graph()
g.parse("data.ttl")

# Apply OWL-RL reasoning
owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
```

## Limitations

- No native async/await support
- Memory-intensive for large graphs
- SPARQL performance varies by store
- Limited OWL reasoning (requires extensions)
- Not a graph database (in-memory or file-based)

## When to Use

**Choose rdflib when:**
- Working with RDF/semantic web data
- SPARQL queries required
- Linked data integration needed
- Ontology processing
- Standards compliance important (W3C RDF)

**Consider alternatives when:**
- Property graph model preferred (use Neo4j)
- High-performance database needed
- Native async required
- Large-scale graph analytics

## Resources

- [Documentation](https://rdflib.readthedocs.io/)
- [GitHub Repository](https://github.com/RDFLib/rdflib)
- [SPARQL Reference](https://rdflib.readthedocs.io/en/stable/intro_to_sparql.html)
- [SPARQLWrapper](https://rdflib.dev/sparqlwrapper/)
- [W3C RDF Primer](https://www.w3.org/TR/rdf-primer/)
