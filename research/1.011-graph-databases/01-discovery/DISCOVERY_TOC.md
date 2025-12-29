# 1.011 Graph Database Clients - Discovery Table of Contents

**Research Date**: December 28, 2025
**Methodology**: MPSE v3.0 (Parallel S1-S4 Discovery)
**Scope**: Python client libraries for graph databases (Neo4j, ArangoDB, TigerGraph, Dgraph, etc.)

---

## Quick Reference: Library Tiers

| Tier | Library | Weekly Downloads | Database | Recommendation |
|------|---------|------------------|----------|----------------|
| **1** | gremlinpython | 5.7M | Multi-DB (Neptune, JanusGraph, Cosmos) | Best portability |
| **1** | rdflib | 1.45M | RDF/SPARQL | Semantic web standard |
| **1** | neo4j | 520K | Neo4j | Primary choice for most use cases |
| **1** | python-arango | 350K-1.2M | ArangoDB | Multi-model (graph + document) |
| **2** | neomodel | 25K | Neo4j | OGM when Django-style models needed |
| **3** | pydgraph | 8K | Dgraph | Horizontal scaling focus |
| **3** | pyTigerGraph | 5.6K | TigerGraph | Enterprise graph ML |
| **4** | py2neo | - | Neo4j | **EOL - Do Not Use** |

---

## Convergence Analysis

### Cross-Methodology Agreement

| Aspect | S1 | S2 | S3 | S4 | Consensus |
|--------|----|----|----|----|-----------|
| Primary recommendation | neo4j | neo4j | neo4j | neo4j | **Strong: neo4j driver** |
| Portability choice | gremlinpython | gremlinpython | gremlinpython | gremlinpython | **Strong: TinkerPop** |
| OGM choice | neomodel | neomodel | neomodel | neomodel | **Strong: neomodel** |
| py2neo status | EOL | EOL | - | - | **Unanimous: Avoid** |
| TigerGraph assessment | Niche | Good for ML | Scale-first | Lock-in risk | **Mixed: Use case dependent** |

### Key Convergence Points
1. **neo4j driver** is the clear winner for most new projects
2. **gremlinpython** is the portability hedge when multi-database required
3. **py2neo is dead** - migrate to neo4j + neomodel
4. **Async support** varies significantly - neo4j best, others require separate packages

### Divergence Points
- **TigerGraph**: S2/S3 favorable for enterprise ML, S4 warns of severe lock-in
- **ArangoDB**: Useful multi-model but BSL license change (2024) affects SaaS

---

## Discovery Files Index

### S1: Rapid Discovery
Quick ecosystem assessment with popularity metrics.

| File | Content |
|------|---------|
| [approach.md](S1-rapid/approach.md) | Rapid evaluation methodology |
| [neo4j-driver.md](S1-rapid/neo4j-driver.md) | Official Neo4j driver - Tier 1 |
| [py2neo.md](S1-rapid/py2neo.md) | Deprecated - EOL April 2025 |
| [neomodel.md](S1-rapid/neomodel.md) | Neo4j OGM - Tier 2 |
| [python-arango.md](S1-rapid/python-arango.md) | ArangoDB driver - Tier 1 |
| [pytigergraph.md](S1-rapid/pytigergraph.md) | TigerGraph client - Tier 3 |
| [gremlinpython.md](S1-rapid/gremlinpython.md) | Apache TinkerPop - Tier 1 |
| [pydgraph.md](S1-rapid/pydgraph.md) | Dgraph client - Tier 3 |
| [rdflib.md](S1-rapid/rdflib.md) | RDF/SPARQL - Tier 1 |
| [recommendation.md](S1-rapid/recommendation.md) | Quick picks summary |

### S2: Comprehensive Discovery
Deep technical analysis with feature comparisons.

| File | Content |
|------|---------|
| [approach.md](S2-comprehensive/approach.md) | Comprehensive methodology |
| [neo4j-driver.md](S2-comprehensive/neo4j-driver.md) | Async, Bolt 6.0, Rust extensions |
| [py2neo.md](S2-comprehensive/py2neo.md) | Migration guidance |
| [neomodel.md](S2-comprehensive/neomodel.md) | Django-style OGM, async v5+ |
| [python-arango.md](S2-comprehensive/python-arango.md) | Multi-model, AQL queries |
| [pytigergraph.md](S2-comprehensive/pytigergraph.md) | Graph ML, PyTorch Geometric |
| [gremlinpython.md](S2-comprehensive/gremlinpython.md) | Multi-DB, WebSocket protocol |
| [pydgraph.md](S2-comprehensive/pydgraph.md) | gRPC-based, DQL |
| [rdflib.md](S2-comprehensive/rdflib.md) | SPARQL 1.1, serialization |
| [feature-matrix.md](S2-comprehensive/feature-matrix.md) | Full comparison table |
| [recommendation.md](S2-comprehensive/recommendation.md) | Use-case guidance |

### S3: Need-Driven Discovery
Use case validation and requirements matching.

| File | Content |
|------|---------|
| [approach.md](S3-need-driven/approach.md) | Need-driven methodology |
| [use-case-social-network.md](S3-need-driven/use-case-social-network.md) | Users, follows, influence |
| [use-case-knowledge-graph.md](S3-need-driven/use-case-knowledge-graph.md) | Entities, semantic queries |
| [use-case-fraud-detection.md](S3-need-driven/use-case-fraud-detection.md) | Transaction patterns, rings |
| [use-case-recommendation-engine.md](S3-need-driven/use-case-recommendation-engine.md) | Collaborative filtering |
| [use-case-network-infrastructure.md](S3-need-driven/use-case-network-infrastructure.md) | Dependency mapping |
| [use-case-supply-chain.md](S3-need-driven/use-case-supply-chain.md) | Logistics, risk |
| [recommendation.md](S3-need-driven/recommendation.md) | Best-fit by use case |

### S4: Strategic Discovery
Long-term viability and ecosystem evolution.

| File | Content |
|------|---------|
| [approach.md](S4-strategic/approach.md) | Strategic methodology |
| [library-viability.md](S4-strategic/library-viability.md) | Maintenance, backing, bus factor |
| [ecosystem-evolution.md](S4-strategic/ecosystem-evolution.md) | 2025-2030 trends, GQL, GraphRAG |
| [lock-in-analysis.md](S4-strategic/lock-in-analysis.md) | Query language portability |
| [recommendation.md](S4-strategic/recommendation.md) | 5-year strategic choices |

---

## Executive Summary

### Primary Recommendation: `neo4j` (Official Driver)

**Why**: Dominant market position ($2B valuation), best Python support, native asyncio, GQL convergence path, GraphRAG leadership. Use with `neomodel` OGM for Django-style models.

```bash
uv add neo4j neomodel
```

### Portability Recommendation: `gremlinpython`

**Why**: Apache governance, works with Neptune/Cosmos/JanusGraph. Accept some ergonomic trade-offs for multi-database portability.

```bash
uv add gremlinpython
```

### Decision Framework

```
Start here:
├── Need multi-database portability? → gremlinpython
├── Need semantic web / RDF? → rdflib
├── Need multi-model (graph + documents)? → python-arango (check BSL license)
├── Need graph ML at massive scale? → pyTigerGraph (accept lock-in)
└── General purpose graph database? → neo4j + neomodel
```

### Critical Warnings

1. **py2neo is EOL** - Migrate immediately to neo4j + neomodel
2. **ArangoDB BSL license** (2024) - Review if building SaaS
3. **TigerGraph GSQL** - Severe vendor lock-in (2/10 portability)
4. **Async support** - Only neo4j has native asyncio; others need separate packages

---

**Research Disclaimer:**
This research is provided for informational purposes only. Performance claims and vendor capabilities should be independently verified. Vendor pricing, features, and policies change frequently.

**Date compiled**: December 28, 2025
