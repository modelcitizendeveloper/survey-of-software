# igraph (Python/R/C)

**GitHub:** ~1.4K stars (python-igraph) | **Ecosystem:** Python, R, C | **License:** GPL-2.0

## Positioning

Fast C-based graph library with Python and R bindings. Middle ground between NetworkX's ease of use and graph-tool's extreme performance. Popular in academic network science.

## Key Metrics

- **Performance:** C core with Python bindings (5-20x faster than pure Python)
- **Download stats:** >50M total downloads (50x less than NetworkX as of 2024)
- **Maintenance:** Active development, v1.0.0 released Oct 2025 (C core)
- **Python versions:** 3.9-3.13 supported, PyPy compatible (3x slower than CPython)
- **Contributors:** 72+ contributors, 3,276 commits

## Algorithms Included

### Maximum Flow
- `Graph.maxflow()` - computes max flow with edge capacities
- Returns `Flow` object with:
  - Flow values on each edge
  - Minimal cut information
  - Source/sink partition data

### Implementation
Based on Boost Graph Library algorithms, compiled C code for performance.

## Community Signals

**Stack Overflow sentiment:**
- "igraph when you need C speed but want Python/R convenience"
- "R users: igraph is the go-to for network analysis"
- "More networkx-like API than graph-tool, but faster"

**Common use cases:**
- Social network analysis in R
- Community detection workflows
- Moderate-scale graph analysis (10K-1M nodes)
- Cross-language research (Python prototyping, R visualization)
- Academic publications requiring reproducible results

## Trade-offs

**Strengths:**
- Better performance than NetworkX (C core)
- Mature codebase (15+ years)
- R integration (large user base in statistics)
- Comprehensive graph algorithms beyond flow
- Pre-compiled wheels for easy installation
- Dual Python/R API (learn once, use in both languages)

**Limitations:**
- GPL license (more restrictive than BSD/Apache)
- Smaller Python community than NetworkX
- Documentation less extensive than NetworkX
- Slower than graph-tool for very large graphs
- Limited constraint programming features compared to OR-Tools
- Installation requires C/C++/Fortran compilers for source builds

## Decision Context

**Choose igraph when:**
- Need better performance than NetworkX but simpler than graph-tool
- Working in R ecosystem (statistics, bioinformatics)
- Graph size: 100K-1M nodes
- Want C-level speed without learning graph-tool's complexity
- Need cross-platform reproducibility (Python + R)

**Skip if:**
- Pure Python simplicity preferred (use NetworkX)
- Extreme performance required (use graph-tool or OR-Tools)
- GPL license incompatible with project
- Need operations research features (use OR-Tools)
- Graph <10K nodes (NetworkX is good enough)
