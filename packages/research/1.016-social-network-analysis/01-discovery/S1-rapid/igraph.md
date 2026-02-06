# igraph

## Overview

High-performance graph library with C core and bindings for Python, R, and Mathematica. Balances speed, ease of use, and comprehensive algorithm coverage - the "production-ready NetworkX."

## Ecosystem Stats

- **GitHub Stars**: ~4K (Python bindings)
- **PyPI Downloads**: ~1M/month
- **First Release**: 2005 (Python bindings)
- **Maintenance**: Active
- **License**: GPL-2.0

## Core Strengths

**Performance**:
- C library core with Python bindings
- ~10-50x faster than NetworkX for most operations
- Efficient memory layout (compressed sparse representation)
- Handles graphs with millions of nodes comfortably

**Comprehensive algorithms**:
- 200+ graph algorithms
- Strong community detection: Louvain, Infomap, label propagation, multilevel
- Centrality: all standard measures plus Katz, subgraph centrality
- Clustering coefficients, motif finding, isomorphism testing
- Advanced: VF2 graph isomorphism, hierarchical clustering

**Production-ready**:
- Stable API, well-maintained
- Cross-platform (Windows, macOS, Linux)
- Available in multiple languages (Python, R, Mathematica)

## Performance Characteristics

**Speed**: Fast
- C core provides significant speedup over pure Python
- Betweenness centrality: ~50x faster than NetworkX on 100K node graph
- Community detection (Louvain): ~20x faster than NetworkX alternatives
- Practical for graphs up to ~10M nodes

**Memory**: Efficient
- Compressed sparse graph representation
- Lower memory footprint than NetworkX
- Can handle larger graphs in same RAM

**Scalability**:
- Interactive analysis: up to ~1M nodes
- Batch processing: up to ~10M nodes
- Beyond that: consider graph-tool or specialized systems

## Limitations

**GPL license**:
- Viral GPL-2.0 (not LGPL)
- May conflict with proprietary/commercial projects
- Requires legal review for commercial use

**Python API ergonomics**:
- Less Pythonic than NetworkX
- Steeper learning curve
- Documentation not as beginner-friendly
- Index-based node references (integers) vs NetworkX's flexible node IDs

**Installation complexity**:
- Requires C compiler for source builds
- Binary wheels available but can have platform issues
- Slightly more friction than pure Python packages

## Best For

- **Production graph analysis**: Reliable, fast, maintained
- **Medium to large graphs**: 100K-10M nodes
- **Community detection**: Excellent algorithm selection
- **Cross-language workflows**: Use same library in Python and R
- **Performance-sensitive research**: Faster iteration on large graphs

## Avoid For

- **Proprietary software**: GPL license issues
- **Beginner projects**: NetworkX is easier to learn
- **Billion-node graphs**: Use graph-tool or snap.py
- **Quick prototyping**: NetworkX has cleaner API for exploration

## Ecosystem Position

**Sweet spot**:
- Projects that outgrew NetworkX performance
- Need production reliability without extreme scale requirements
- Want comprehensive algorithms without implementation complexity
- Can accept GPL license

**The bridge between**:
- NetworkX (ease of use) and graph-tool (extreme performance)
- Academic prototyping and production deployment
