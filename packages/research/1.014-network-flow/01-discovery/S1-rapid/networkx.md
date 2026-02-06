# NetworkX (Python)

**GitHub:** ~16K stars | **Ecosystem:** Python | **License:** BSD-3-Clause

## Positioning

Pure Python graph library with comprehensive network flow algorithms. De facto standard for graph analysis in Python data science and research workflows.

## Key Metrics

- **Performance:** Pure Python implementation (slower than C++ bindings for large-scale problems)
- **Download stats:** ~15M downloads/week on PyPI (Jan 2026)
- **Maintenance:** Active development since 2002, stable 3.x release line
- **Python versions:** 3.9+ supported (3.6.1 current as of Jan 2026)

## Algorithms Included

### Maximum Flow
- Ford-Fulkerson (via Edmonds-Karp)
- Preflow-push (default, fastest)
- Shortest augmenting path
- Dinitz's algorithm

### Minimum Cost Flow
- `min_cost_flow()` - satisfies all node demands
- `max_flow_min_cost()` - max flow with minimum cost
- `capacity_scaling()` - successive shortest path algorithm

## Community Signals

**Stack Overflow sentiment:**
- "NetworkX is the standard for graph problems in Python - start here unless you need extreme performance"
- "For research and prototyping, NetworkX is unbeatable for API clarity"
- "Production systems with >100K nodes should consider igraph or graph-tool"

**Common use cases:**
- Academic research in network science
- Data science workflows (Jupyter notebooks)
- Supply chain optimization (moderate scale)
- Social network analysis
- Transportation routing (small to medium graphs)

## Trade-offs

**Strengths:**
- Excellent documentation and tutorials
- Clean, Pythonic API - easy to learn
- Rich ecosystem integration (NumPy, SciPy, Pandas)
- Comprehensive algorithm coverage beyond flow (centrality, clustering, etc.)
- Easy visualization with matplotlib integration

**Limitations:**
- Pure Python performance penalty (10-100x slower than C++ implementations)
- Not suitable for graphs with >1M edges in production
- Floating-point weights can cause numerical issues in flow algorithms
- Higher memory overhead compared to C++-backed libraries

## Decision Context

**Choose NetworkX when:**
- Prototyping network algorithms rapidly
- Working in Jupyter/academic environment
- Graph size <100K nodes
- API clarity and documentation matter more than raw speed
- Need broad algorithm coverage beyond just flow

**Skip if:**
- Processing >1M edge graphs regularly
- Flow computations are in critical performance path
- Need sub-second latency for routing queries
- Building production logistics/supply chain systems (use OR-Tools instead)
