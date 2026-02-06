# NetworkX

## Overview

Pure Python library for creating, manipulating, and analyzing complex networks. The de facto standard for general-purpose graph analysis in Python, prioritizing ease of use and educational value over raw performance.

## Ecosystem Stats

- **GitHub Stars**: ~15K (as of 2024)
- **PyPI Downloads**: ~15M/month
- **First Release**: 2004
- **Maintenance**: Active (NumFOCUS project)
- **License**: BSD-3-Clause

## Core Strengths

**Educational and prototyping**:
- Readable, Pythonic API
- Excellent documentation with examples
- Low barrier to entry for newcomers
- Reference implementation for many algorithms

**Comprehensive algorithm library**:
- 500+ algorithms across all graph theory domains
- Centrality measures: degree, betweenness, closeness, eigenvector, PageRank
- Community detection: Girvan-Newman, modularity-based, label propagation
- Shortest paths: Dijkstra, A*, Floyd-Warshall, Bellman-Ford
- Graph generation: Erdős-Rényi, Barabási-Albert, Watts-Strogatz, stochastic block models

**Flexibility**:
- Supports directed, undirected, multigraphs, multidigraphs
- Arbitrary node/edge attributes (dictionaries)
- Easy integration with scientific Python stack (NumPy, SciPy, Pandas, Matplotlib)

## Performance Characteristics

**Speed**: Slowest among major libraries
- Pure Python implementation (no C/C++ core)
- ~10-100x slower than igraph/graph-tool for large graphs
- Suitable for graphs up to ~100K nodes (interactive analysis)
- Can handle up to ~1M nodes (batch processing, patience required)

**Memory**: Moderate efficiency
- Graph stored as nested dictionaries
- Higher overhead than C-based libraries
- Practical limit: graphs that fit comfortably in RAM

## Limitations

**Not for production-scale analysis**:
- Poor performance on million-node graphs
- No parallel processing support
- Not designed for billion-node networks

**Community detection gaps**:
- Limited modern community detection algorithms
- Louvain method requires external library (community package)
- No hierarchical community detection built-in

## Best For

- **Learning graph theory**: Clear implementations, educational focus
- **Prototyping**: Rapid experimentation with algorithms
- **Small to medium graphs**: <100K nodes for interactive work
- **Research**: Easy to extend and modify algorithms
- **Integration**: Works seamlessly with Jupyter, Pandas, plotting libraries

## Avoid For

- **Large-scale production**: Use graph-tool or igraph instead
- **Performance-critical paths**: 10-100x slower than alternatives
- **Billion-node graphs**: Use snap.py or specialized systems
- **Real-time analysis**: No streaming support

## Ecosystem Position

**The default choice for**:
- First-time graph analysis users
- Academic teaching and research
- Python-first data science workflows
- Cases where development speed > execution speed

**Graduate to alternatives when**:
- Graph size exceeds ~100K nodes
- Performance becomes a bottleneck
- Production deployment required
