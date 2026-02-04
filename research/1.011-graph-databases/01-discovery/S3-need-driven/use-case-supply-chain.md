# Use Case: Supply Chain

## Domain Description

Supply chain graphs model the network of suppliers, manufacturers, distributors,
and logistics providers that move products from raw materials to end customers.
Graph analysis enables risk assessment, optimization of logistics, supplier
diversification, and end-to-end traceability.

## Requirements Analysis

### Graph Model Requirements

| Aspect | Requirement | Rationale |
|--------|-------------|-----------|
| **Model Type** | Property Graph | Rich attributes on entities; weighted relationships |
| **Multi-graph** | Multiple edge types | Material flow, financial flow, information flow |
| **Temporal** | Time-aware edges | Lead times, seasonal variations, historical performance |

**Key Entity Types:**
- Organizations: Suppliers, manufacturers, distributors, retailers
- Facilities: Factories, warehouses, ports, distribution centers
- Products: SKUs, components, raw materials, finished goods
- Logistics: Routes, carriers, shipments
- Contracts: Agreements, terms, pricing

### Query Pattern Complexity

**Primary Patterns:**
- **Shortest path**: Optimal route from supplier to customer
- **Risk propagation**: "If supplier X fails, what products are affected?"
- **Alternative sourcing**: Finding backup suppliers for a component
- **Bottleneck detection**: Identifying single points of failure
- **Cost optimization**: Weighted path finding for lowest total cost

**Query Characteristics:**
- Depth: 3-10 hops (raw material to finished product)
- Weighted: Edges have cost, time, capacity attributes
- Aggregation: Sum costs, max lead times, min capacities
- Constraints: Capacity limits, geographic restrictions

### Scale Requirements

| Metric | Typical Range | High Scale |
|--------|---------------|------------|
| Entities (nodes) | 10K - 100K | 1M+ |
| Relationships (edges) | 100K - 1M | 10M+ |
| Query frequency | 10 - 100 QPS | 1K QPS |
| Path computations | 100 - 10K/day | 100K/day |

### Processing Mode

- **Real-time**: Disruption impact assessment (< 5s)
- **Batch**: Route optimization, network redesign (hourly/daily)
- **Simulation**: What-if analysis for planning

### Integration Requirements

- ERP systems (SAP, Oracle) for order and inventory data
- TMS (Transportation Management Systems) for logistics
- Supplier portals for performance data
- IoT/tracking systems for shipment visibility
- BI tools for reporting and visualization
- Planning tools for demand forecasting

## Library Evaluation

### neo4j (Official Driver)

**Strengths:**
- Excellent weighted shortest path algorithms
- Cypher handles multi-hop supply chain queries well
- GDS library for network analysis (centrality, community)
- Good visualization for supply chain mapping

**Limitations:**
- Complex optimization needs external solvers
- Limited native geospatial support
- Large-scale simulations may need export to specialized tools

**Fit Score: 8/10**

### python-arango

**Strengths:**
- Multi-model stores complex product/contract documents
- Good geospatial support for logistics
- Scales well for medium-large supply chains
- Cost-effective for exploration

**Limitations:**
- Fewer built-in graph algorithms
- Path optimization less mature than Neo4j
- Smaller supply chain community

**Fit Score: 7/10**

### pyTigerGraph

**Strengths:**
- Excellent for very large global supply chains
- GSQL handles complex path computations
- Built-in graph analytics
- Enterprise supply chain focus

**Limitations:**
- Enterprise licensing costs
- Steeper learning curve
- Overkill for regional supply chains

**Fit Score: 8/10** (global enterprise); **6/10** (smaller chains)

### gremlinpython

**Strengths:**
- Database-agnostic
- Standard traversal patterns
- Works with Neptune for AWS supply chains

**Limitations:**
- Verbose for weighted path queries
- Limited optimization algorithms
- Less intuitive for supply chain queries

**Fit Score: 5/10**

### NetworkX

**Strengths:**
- Rich library for network optimization
- Excellent for simulations and what-if analysis
- Easy integration with optimization libraries (PuLP, OR-Tools)
- Good for research and prototyping

**Limitations:**
- In-memory only
- Cannot serve production queries
- Export/import overhead for real data

**Fit Score: 6/10** (analysis); **2/10** (production)

## Gaps and Workarounds

| Gap | Impact | Workaround |
|-----|--------|------------|
| Constrained optimization | Cannot express capacity constraints in query | Export to optimization solver |
| Multi-objective paths | Trade-off cost vs time vs risk complex | Pareto frontier computation offline |
| Temporal edges | Lead times vary by season/volume | Time-parameterized edge properties |
| Geospatial routing | Distance calculations limited | Integrate with mapping APIs |
| Simulation | What-if at scale challenging | Clone subgraphs, sandbox environments |
| Data freshness | Supply chain data from many sources | ETL pipeline, change data capture |

## Architecture Pattern

```
[Source Systems]
   |-- ERP
   |-- TMS
   |-- Supplier portals
   |-- IoT/Tracking
        |
        v
[ETL Pipeline] -- transformation --> [Graph Database]
        |                                    |
        v                                    v
[Master Data Management]              [Query API]
                                            |
                                            v
                            [Planning/Visualization Tools]
```

**Query Examples:**

```cypher
// Shortest path by lead time
MATCH path = shortestPath(
  (supplier:Supplier {id: $supplierId})-[:SHIPS_TO*]-(dc:DistributionCenter {id: $dcId})
)
RETURN path, reduce(time=0, r in relationships(path) | time + r.leadTimeDays) as totalLeadTime

// Risk propagation: What's affected if this supplier fails?
MATCH (supplier:Supplier {id: $supplierId})<-[:SOURCED_FROM*1..5]-(product:Product)
RETURN product.sku, product.name, product.criticality

// Alternative suppliers
MATCH (product:Product {sku: $sku})-[:SOURCED_FROM]->(current:Supplier)
MATCH (component)<-[:CONTAINS]-(product)
MATCH (alt:Supplier)-[:PROVIDES]->(component)
WHERE alt <> current
RETURN alt.name, count(component) as componentsAvailable
```

## Optimization Patterns

For complex supply chain optimization, combine graph database with optimization:

1. **Graph database**: Topology storage, constraint queries
2. **Export to pandas/NumPy**: Data preparation
3. **Optimization solver** (OR-Tools, Gurobi): Route optimization
4. **Write back to graph**: Optimal routes as relationships

```python
# Example hybrid pattern
from neo4j import GraphDatabase
from ortools.constraint_solver import routing_enums_pb2, pywrapcp

# 1. Extract network from graph
with driver.session() as session:
    network = session.run("MATCH (a)-[r:ROUTE]->(b) RETURN ...").data()

# 2. Build optimization model
manager = pywrapcp.RoutingIndexManager(...)
routing = pywrapcp.RoutingModel(manager)

# 3. Solve
solution = routing.SolveWithParameters(search_params)

# 4. Write optimal routes back to graph
with driver.session() as session:
    session.run("CREATE (r:OptimalRoute {...})", optimal_route)
```

## Recommendation

**Best Fit: neo4j official driver**

For supply chain applications, Neo4j provides the best balance of query
expressiveness, graph algorithms, and ecosystem maturity. The combination of
Cypher for querying and GDS for analytics covers most supply chain needs.

**Key advantages for supply chain:**
- Weighted shortest path for logistics optimization
- Centrality algorithms for identifying critical nodes
- Community detection for supplier clustering
- Good visualization for supply chain mapping

**Alternative: pyTigerGraph** for global enterprises with very large,
distributed supply chains requiring massive scale.

**Complement with NetworkX/OR-Tools** for complex constrained optimization
that goes beyond graph traversal (e.g., vehicle routing, facility location).
