# Vendor Lock-in Analysis: Graph Database Clients

## Query Language Portability Assessment

### Portability Spectrum

```
Most Portable                                    Least Portable
     |                                                  |
  Gremlin -----> Cypher/GQL -----> GSQL -----> Proprietary
```

### Gremlin (Apache TinkerPop)

**Portability Score: 9/10**

- **Supported Databases**: JanusGraph, Neptune, Cosmos DB, DataStax, OrientDB
- **Strengths**: True multi-database abstraction, Apache governance
- **Weaknesses**: Imperative style less intuitive than Cypher
- **Best For**: Projects requiring database portability guarantees

### Cypher / openCypher / GQL

**Portability Score: 7/10 (improving)**

- **Current Support**: Neo4j, Memgraph, AGE (PostgreSQL), RedisGraph (EOL)
- **GQL Future**: Expected broad adoption 2026-2028
- **Strengths**: Declarative, readable, standardizing via ISO GQL
- **Weaknesses**: Neo4j dominance means de facto lock-in
- **Best For**: Projects betting on GQL standardization

### GSQL (TigerGraph)

**Portability Score: 2/10**

- **Single Vendor**: Only TigerGraph
- **Strengths**: Turing-complete, optimized for deep analytics
- **Weaknesses**: Complete vendor lock-in, no migration path
- **Best For**: Enterprise analytics with long-term TigerGraph commitment

## Data Model Portability

### Property Graph Model

All major graph databases (Neo4j, TigerGraph, Neptune, JanusGraph) use property
graphs, providing basic model compatibility:

- **Nodes/Vertices**: Labeled entities with properties
- **Edges/Relationships**: Typed connections with properties
- **Export Formats**: CSV, JSON, GraphML widely supported

### Migration Complexity Matrix

| From          | To Neo4j    | To Neptune  | To TigerGraph | To JanusGraph |
|---------------|-------------|-------------|---------------|---------------|
| Neo4j         | -           | Medium      | High          | Medium        |
| Neptune       | Medium      | -           | High          | Low           |
| TigerGraph    | High        | High        | -             | High          |
| JanusGraph    | Medium      | Low         | High          | -             |

**Key Factors**:
- Query translation (Cypher <-> Gremlin <-> GSQL)
- Schema and constraint differences
- Indexing strategy variations
- Application code rewrite requirements

### Export/Import Tooling

**Available Tools**:
- Neo4j: LOAD CSV, neo4j-admin export, APOC procedures
- Memgraph: Neo4j migration module (direct connection)
- General: GraphML format interchange
- Microsoft: MigrateToGraph (relational to graph)

**Limitations**:
- No universal graph-to-graph migration standard
- Query translation typically manual
- Application logic must be rewritten

## Abstraction Layer Options

### TinkerPop as Universal Layer

**What It Provides**:
- Common Gremlin query language
- Vendor-agnostic driver interfaces
- Standard property graph model

**Databases Supported**:
- JanusGraph (native)
- Amazon Neptune
- Azure Cosmos DB
- DataStax Enterprise
- OrientDB

**Databases NOT Supported**:
- Neo4j (native Cypher only, no TinkerPop)
- TigerGraph (GSQL only)

**When TinkerPop Makes Sense**:
1. Multi-cloud strategy requiring database flexibility
2. Existing investment in Gremlin queries
3. Need to switch between Neptune/Cosmos/JanusGraph
4. Avoiding single-vendor dependency

**When TinkerPop Doesn't Make Sense**:
1. Neo4j-specific features required
2. GSQL analytics capabilities needed
3. Cypher/GQL standardization bet
4. Simple use case not needing portability

### ORM/OGM Abstraction

**Available OGMs**:
- Neomodel: Neo4j only
- Object-Graph Mappers: Database-specific implementations

**Limitation**: No cross-database Python OGM exists. OGMs provide code abstraction
but not database portability.

## Lock-in Risk Mitigation Strategies

### Strategy 1: TinkerPop-First

Choose Gremlin-compatible database; use gremlinpython exclusively.

**Pros**: Maximum portability, multi-vendor competition
**Cons**: Excludes Neo4j, foregoes Cypher benefits
**Risk Level**: Low lock-in, medium feature limitation

### Strategy 2: GQL-Ready Cypher

Choose Neo4j or openCypher database; prepare for GQL migration.

**Pros**: Best tooling (Neo4j), GQL future-proofing
**Cons**: Near-term Cypher lock-in, GQL timeline uncertainty
**Risk Level**: Medium lock-in, low feature limitation

### Strategy 3: Abstraction Layer

Build internal abstraction over database clients.

**Pros**: Control over interfaces, potential future migration
**Cons**: Development overhead, incomplete feature coverage
**Risk Level**: Low lock-in, high development cost

### Strategy 4: Cloud Provider Lock-in Accept

Choose Neptune or Cosmos DB; accept cloud platform dependency.

**Pros**: Managed service benefits, cloud ecosystem integration
**Cons**: Full cloud vendor lock-in
**Risk Level**: High lock-in, low operational burden

## Recommendations by Use Case

### Startup/MVP

- **Choice**: Neo4j + Cypher
- **Rationale**: Best developer experience, largest community, GQL path
- **Lock-in Acceptance**: Medium (acceptable for velocity)

### Enterprise Multi-Database

- **Choice**: TinkerPop/Gremlin
- **Rationale**: Proven portability, vendor-neutral governance
- **Lock-in Acceptance**: Low (portability required)

### Deep Analytics

- **Choice**: TigerGraph + GSQL
- **Rationale**: Best performance for complex algorithms
- **Lock-in Acceptance**: High (feature-driven decision)

### Cloud-Native

- **Choice**: Neptune or Cosmos DB (matching cloud provider)
- **Rationale**: Operational simplicity, ecosystem integration
- **Lock-in Acceptance**: High (cloud strategy dependent)
