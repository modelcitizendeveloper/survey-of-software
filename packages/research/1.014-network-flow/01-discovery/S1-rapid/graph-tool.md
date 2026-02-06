# graph-tool (Python)

**GitLab:** Not disclosed | **Ecosystem:** Python (C++ core) | **License:** LGPL-3.0

## Positioning

High-performance graph analysis library built on C++ and Boost Graph Library. Designed for researchers needing maximum speed with large-scale networks (millions of nodes). Steepest learning curve, highest performance.

## Key Metrics

- **Performance:** C++ template metaprogramming (fastest Python graph library)
- **Download stats:** Smaller user base (conda-forge primary distribution)
- **Maintenance:** Active development since 2014, 3,730 commits, 150 tags
- **Python versions:** Supports current Python versions
- **Author:** Tiago de Paula Peixoto (network science researcher)

## Algorithms Included

### Maximum Flow
- `edmonds_karp_max_flow()` - O(VE²) or O(VEU) for integer capacities
- `push_relabel_max_flow()` - O(V³) complexity (recommended)
- `boykov_kolmogorov_max_flow()` - specialized variant

All algorithms leverage Boost Graph Library's optimized C++ implementations.

## Community Signals

**Stack Overflow sentiment:**
- "graph-tool when you need absolute maximum performance in Python"
- "Installation can be painful, but worth it for large graphs"
- "Best for academic work with millions of nodes"

**Common use cases:**
- Large-scale network science research (millions of nodes)
- Biological networks (protein interactions, gene regulatory networks)
- Social network analysis at web scale
- Computational neuroscience (brain connectivity graphs)
- Statistical inference on networks (Bayesian models)

## Trade-offs

**Strengths:**
- Fastest graph library for Python (C++ template metaprogramming)
- Scales to millions of nodes/edges
- Comprehensive statistical inference tools (unique among graph libraries)
- LGPL license (more permissive than GPL)
- Advanced algorithms for community detection, graph drawing
- 15+ years of cutting-edge network science development

**Limitations:**
- **Difficult installation** (conda-forge recommended, pip can be problematic)
- Steep learning curve (C++ concepts leak into Python API)
- Smaller community than NetworkX/igraph
- Less documentation and fewer examples
- Requires understanding of Boost Graph Library concepts
- Not suitable for casual graph exploration
- Breaking changes more common than NetworkX

## Decision Context

**Choose graph-tool when:**
- Working with graphs >1M nodes
- Performance is critical (research deadlines, production scale)
- Need statistical inference on network structure (Stochastic Block Models)
- Comfortable with C++ concepts and Boost documentation
- Willing to invest in learning curve for long-term performance

**Skip if:**
- Graph <100K nodes (NetworkX is easier)
- Prototyping or teaching (complexity not justified)
- Installation/deployment simplicity required
- Team lacks C++/Boost background
- Need operations research features (use OR-Tools instead)
