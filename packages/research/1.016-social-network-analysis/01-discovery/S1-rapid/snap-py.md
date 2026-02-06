# snap.py (Stanford Network Analysis Platform)

## Overview

Python interface to SNAP, Stanford's C++ library for massive network analysis. Designed for billion-node graphs and large-scale research. Focused on scalability over algorithm breadth.

## Ecosystem Stats

- **GitHub Stars**: ~2K (SNAP repository)
- **PyPI Downloads**: ~50K/month
- **First Release**: 2009
- **Maintenance**: Stable (Stanford InfoLab)
- **License**: BSD-3-Clause

## Core Strengths

**Extreme scalability**:
- Designed for billion-node, billion-edge graphs
- Stanford's research on web-scale networks (Google, Facebook collaborations)
- Efficient in-memory representations
- Optimized for scale over ease of use

**Fast core operations**:
- C++ core with SWIG-generated Python bindings
- Graph traversal, connected components: optimized for huge graphs
- PageRank, centrality measures: handle web-scale networks
- Cascade and diffusion models at scale

**Research provenance**:
- Developed by Stanford Network Analysis Project
- Used in published research on billion-node networks
- Dataset library included (SNAP datasets)
- Academic credibility for large-scale studies

## Performance Characteristics

**Speed**: Very fast for supported operations
- Optimized for graphs with 10M-1B+ nodes
- Comparable to graph-tool for core algorithms
- Faster than igraph for very large graphs
- Not as fast as graph-tool for general algorithms

**Memory**: Efficient for massive graphs
- Compact representations for sparse graphs
- Handles billions of edges in RAM
- Designed for web/social network sparsity patterns

**Scalability ceiling**:
- Interactive: 1M-10M nodes
- Batch: 100M-1B nodes
- Practical limit: available RAM (sparse graphs)

## Limitations

**Limited algorithm coverage**:
- Narrower than NetworkX, igraph, graph-tool
- Focused on core operations (centrality, connectivity, cascades)
- Community detection: basic algorithms only (no SBM, Infomap)
- Missing many specialized algorithms

**API and documentation**:
- Less Pythonic (auto-generated SWIG bindings)
- Documentation more C++-focused
- Fewer examples than NetworkX/igraph
- Steeper learning curve than alternatives

**Maintenance concerns**:
- Slower development pace than igraph/graph-tool
- Fewer updates in recent years
- Smaller active community
- Some platform-specific installation issues

**Python integration**:
- SWIG bindings feel foreign to Python developers
- Less idiomatic than hand-written Python APIs
- Harder to debug and extend

## Best For

- **Billion-node graphs**: Web crawls, social networks at scale
- **Research replication**: Papers using SNAP datasets/methodology
- **Scalability-first projects**: Size is the primary constraint
- **Core graph operations**: PageRank, centrality, cascades at massive scale
- **Exploratory analysis of huge graphs**: Quick stats on billion-edge networks

## Avoid For

- **Comprehensive analysis**: Limited algorithm library
- **Modern community detection**: Use igraph or graph-tool
- **Pythonic workflows**: Awkward API integration
- **Small to medium graphs (<1M nodes)**: Overkill, use NetworkX or igraph
- **Active development needs**: Slower update cycle

## Ecosystem Position

**The billion-node specialist**:
- Unique niche: graphs too large for igraph, but need Python
- Research-proven at extreme scale
- Trade-off: scale vs algorithm breadth

**Competitive position**:
- **vs NetworkX**: 1000x faster, but 1/10th the algorithms
- **vs igraph**: Better for >10M nodes, worse for general use
- **vs graph-tool**: Similar speed, but narrower scope and weaker API

**When to choose SNAP**:
- Graph size exceeds igraph/graph-tool comfort zone (>10M nodes)
- Need Python interface (not C++)
- Core operations sufficient (don't need exotic algorithms)
- Stanford research ecosystem familiarity

**When to skip SNAP**:
- Graph fits comfortably in igraph/graph-tool (<10M nodes)
- Need comprehensive algorithm library
- Want modern Python API ergonomics
- Require active community support
