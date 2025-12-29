# rdflib - Python Library for RDF

## Quick Facts

| Metric | Value |
|--------|-------|
| Package Name | `rdflib` |
| Latest Version | 7.5.0 (Nov 28, 2025) |
| Python Support | 3.8.1+ |
| Weekly Downloads | ~1.45 million |
| GitHub Stars | 2,400 |
| Contributors | 189 |
| Open Issues | 291 |
| License | BSD-3-Clause |
| Maintainer | RDFLib community |

## Installation

```bash
pip install rdflib
```

## First Impression

**Strengths:**
- Dominant library for RDF/semantic web in Python
- Comprehensive format support (RDF/XML, Turtle, JSON-LD, N-Quads, etc.)
- Full SPARQL 1.1 implementation
- Mature, well-documented
- Large ecosystem of extensions

**Considerations:**
- Focus on RDF graphs (different paradigm from property graphs)
- Not designed for high-performance graph traversal
- Steeper learning curve for developers new to semantic web

## Quick Example

```python
from rdflib import Graph, Literal, RDF, URIRef, Namespace

# Create a graph
g = Graph()

# Define namespace
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
g.bind("foaf", FOAF)

# Add triples
alice = URIRef("http://example.org/alice")
g.add((alice, RDF.type, FOAF.Person))
g.add((alice, FOAF.name, Literal("Alice")))
g.add((alice, FOAF.knows, URIRef("http://example.org/bob")))

# SPARQL query
results = g.query("""
    SELECT ?name WHERE {
        ?person foaf:name ?name .
    }
""")
for row in results:
    print(row.name)

# Serialize
print(g.serialize(format="turtle"))
```

## RDF vs Property Graphs

| RDF (rdflib) | Property Graphs (Neo4j, etc.) |
|--------------|-------------------------------|
| Triple-based (subject-predicate-object) | Nodes and relationships with properties |
| URIs for identifiers | Internal IDs |
| SPARQL query language | Cypher, Gremlin, etc. |
| Semantic web / linked data focus | Application data modeling |
| Standards-based (W3C) | Vendor-specific |

## Assessment

**Tier: 1 - Production Ready**

rdflib is the standard for RDF processing in Python. Essential for semantic web
applications, knowledge graphs with linked data, and SPARQL-based querying.
Different use case than property graph databases but equally mature.

## Links
- PyPI: https://pypi.org/project/rdflib/
- GitHub: https://github.com/RDFLib/rdflib
- Docs: https://rdflib.readthedocs.io/
- Website: https://rdflib.dev/
