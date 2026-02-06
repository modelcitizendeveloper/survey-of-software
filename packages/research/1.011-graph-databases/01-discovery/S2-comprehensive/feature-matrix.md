# Graph Database Python Client Libraries: Feature Matrix

## Overview

This matrix compares Python client libraries for graph databases across key functional and technical criteria. Libraries are evaluated as of December 2024.

## Quick Reference

| Library | Database | Query Language | Status |
|---------|----------|----------------|--------|
| neo4j-driver | Neo4j | Cypher | Active |
| py2neo | Neo4j | Cypher | EOL |
| neomodel | Neo4j | OGM/Cypher | Active |
| python-arango | ArangoDB | AQL | Active |
| pyTigerGraph | TigerGraph | GSQL | Active |
| gremlinpython | Multi-DB | Gremlin | Active |
| pydgraph | Dgraph | DQL | Active |
| rdflib | RDF stores | SPARQL | Active |

## Async Support

| Library | Native asyncio | Async Variant | Framework Compat |
|---------|----------------|---------------|------------------|
| neo4j-driver | Yes | Built-in | FastAPI, aiohttp |
| py2neo | No | - | - |
| neomodel | Yes | Built-in (v5+) | Django, FastAPI |
| python-arango | No | python-arango-async | FastAPI (separate pkg) |
| pyTigerGraph | Partial | AsyncTigerGraphConnection | Limited |
| gremlinpython | No | aiogremlin, goblin | Via third-party |
| pydgraph | No | gRPC futures only | Limited |
| rdflib | No | Manual wrapping | Via thread pool |

## Connection Management

| Library | Connection Pooling | Pool Size Config | Liveness Check |
|---------|-------------------|------------------|----------------|
| neo4j-driver | Yes | max_connection_pool_size | liveness_check_timeout |
| py2neo | Basic | Limited | No |
| neomodel | Yes (via driver) | Via driver_options | Via driver |
| python-arango | No | - | No |
| pyTigerGraph | No | - | No |
| gremlinpython | Yes | pool_size parameter | Known issues |
| pydgraph | Manual | Multiple stubs | Manual |
| rdflib | N/A | N/A | N/A |

## Transaction Support

| Library | ACID | Managed Txn | Auto-retry | Causal Consistency |
|---------|------|-------------|------------|-------------------|
| neo4j-driver | Yes | execute_read/write | Yes | Bookmarks |
| py2neo | Yes | Context manager | No | No |
| neomodel | Yes | Context manager | No | Via driver |
| python-arango | Yes | Stream/JS txn | No | No |
| pyTigerGraph | Limited | Via REST | No | No |
| gremlinpython | Yes | tx.begin/commit | No | No |
| pydgraph | Yes | txn() context | Manual | No |
| rdflib | No | N/A | N/A | N/A |

## Query Language Features

| Library | Parameterized | Prepared/Cached | Bulk Operations |
|---------|--------------|-----------------|-----------------|
| neo4j-driver | Yes ($params) | No | UNWIND pattern |
| py2neo | Yes | No | Batch methods |
| neomodel | Yes | No | save() loop |
| python-arango | Yes (@params) | No | insert_many() |
| pyTigerGraph | Yes | Installed queries | upsertVertices() |
| gremlinpython | Limited | No | Batch traversals |
| pydgraph | Yes ($params) | No | JSON arrays |
| rdflib | Yes (initBindings) | prepareQuery() | addN() |

## OGM/ORM Capabilities

| Library | OGM Layer | Schema Definition | Hooks | Validation |
|---------|-----------|-------------------|-------|------------|
| neo4j-driver | No | Manual | No | No |
| py2neo | Built-in | GraphObject | Limited | No |
| neomodel | Built-in | StructuredNode | Yes | Property-level |
| python-arango | No | Manual | No | No |
| pyTigerGraph | Schema API | Object-oriented | No | GSQL |
| gremlinpython | Via Goblin | Vertex/Edge classes | Limited | Via Goblin |
| pydgraph | No | DQL schema | No | No |
| rdflib | No | RDF/OWL | No | SHACL (ext) |

## Type System

| Library | Type Hints | MyPy Support | Spatial Types | Temporal Types |
|---------|-----------|--------------|---------------|----------------|
| neo4j-driver | Yes | Good | Point | Date/DateTime/Duration |
| py2neo | Partial | Limited | Via Cypher | Via Cypher |
| neomodel | Yes | Good | PointProperty | DateTime/Date |
| python-arango | Partial | Limited | GeoJSON | ISO strings |
| pyTigerGraph | Limited | Limited | GSQL types | DATETIME |
| gremlinpython | Limited | Limited | Via properties | Via properties |
| pydgraph | Limited | Limited | Geo (geo:) | dateTime |
| rdflib | Partial | Limited | GeoSPARQL | xsd:dateTime |

## Performance Features

| Library | Native Extensions | Binary Protocol | Compression |
|---------|-------------------|-----------------|-------------|
| neo4j-driver | Rust (optional) | Bolt | No |
| py2neo | No | Bolt/HTTP | No |
| neomodel | Via driver | Bolt | No |
| python-arango | No | HTTP/REST | Optional |
| pyTigerGraph | No | HTTP/REST | No |
| gremlinpython | No | WebSocket | GraphBinary |
| pydgraph | No | gRPC | Protocol Buffers |
| rdflib | No | N/A | N/A |

## Error Handling

| Library | Typed Exceptions | Retry Categories | Error Codes |
|---------|------------------|------------------|-------------|
| neo4j-driver | Yes | Transient/Client/DB | Yes |
| py2neo | Partial | No | Limited |
| neomodel | Via driver | Via driver | Via driver |
| python-arango | Yes | No | ArangoDB codes |
| pyTigerGraph | Basic | No | REST status |
| gremlinpython | GremlinServerError | No | Server codes |
| pydgraph | gRPC errors | Manual | gRPC codes |
| rdflib | Standard Python | No | No |

## Testing Support

| Library | Mocking | Embedded Mode | Testcontainers |
|---------|---------|---------------|----------------|
| neo4j-driver | Manual | No | Yes |
| py2neo | No | No | Possible |
| neomodel | Manual | No | Yes |
| python-arango | No | No | Yes |
| pyTigerGraph | No | No | Limited |
| gremlinpython | No | JVM only | Yes (Gremlin Server) |
| pydgraph | No | No | Yes |
| rdflib | In-memory graph | Yes | N/A |

## Documentation and Community

| Library | Official Docs | API Reference | Examples | Community |
|---------|---------------|---------------|----------|-----------|
| neo4j-driver | Excellent | Complete | Extensive | Large |
| py2neo | Archived | Archived | Limited | Inactive |
| neomodel | Good | Complete | Moderate | Active |
| python-arango | Good | Complete | Good | Moderate |
| pyTigerGraph | Good | Complete | Good | Moderate |
| gremlinpython | Good | Reference | Book available | Large |
| pydgraph | Moderate | README | Basic | Small |
| rdflib | Excellent | Complete | Extensive | Large |

## Python Version Support

| Library | Min Version | Max Version | Notes |
|---------|-------------|-------------|-------|
| neo4j-driver | 3.10 | 3.14 | Drops 3.9 in v6 |
| py2neo | 3.x | - | EOL |
| neomodel | 3.8 | 3.12+ | |
| python-arango | 3.9 | Latest | |
| pyTigerGraph | 3.7 | Latest | |
| gremlinpython | 3.10 | Latest | |
| pydgraph | 3.7 | Latest | |
| rdflib | 3.8 | Latest | |

## Database Version Support

| Library | Supported Versions | LTS Support |
|---------|-------------------|-------------|
| neo4j-driver | 4.4+, 5.x | 4.4 LTS, 5.26 LTS |
| py2neo | 4.x (frozen) | - |
| neomodel | 4.4+, 5.x | Via driver |
| python-arango | 3.11+ | Via ArangoDB |
| pyTigerGraph | 3.x+ | Via TigerGraph |
| gremlinpython | TinkerPop 3.x | Via database |
| pydgraph | Version-matched | Via Dgraph |
| rdflib | N/A | N/A |

## Installation Size

| Library | Core Size | Dependencies | Optional Extras |
|---------|-----------|--------------|-----------------|
| neo4j-driver | ~500KB | pytz | rust-ext (~2MB) |
| py2neo | ~1MB | Several | pygments |
| neomodel | ~200KB | neo4j-driver | shapely, extras |
| python-arango | ~300KB | requests | - |
| pyTigerGraph | ~500KB | requests | torch (GDS) |
| gremlinpython | ~200KB | aiohttp, nest-asyncio | - |
| pydgraph | ~100KB | grpcio, protobuf | - |
| rdflib | ~2MB | pyparsing, isodate | lxml, html5lib |

## Summary Scores (1-5)

| Library | API Design | Performance | Async | Ecosystem | Overall |
|---------|-----------|-------------|-------|-----------|---------|
| neo4j-driver | 5 | 5 | 5 | 5 | 5.0 |
| py2neo | 4 | 3 | 1 | 1 | 2.3 |
| neomodel | 5 | 4 | 4 | 4 | 4.3 |
| python-arango | 4 | 4 | 3 | 4 | 3.8 |
| pyTigerGraph | 3 | 3 | 2 | 3 | 2.8 |
| gremlinpython | 3 | 3 | 2 | 4 | 3.0 |
| pydgraph | 3 | 4 | 2 | 2 | 2.8 |
| rdflib | 4 | 3 | 1 | 4 | 3.0 |

---

*Scores based on: API ergonomics, Python idiom adherence, documentation quality, maintenance activity, and production readiness.*
