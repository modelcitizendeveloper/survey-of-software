# CDlib (Community Discovery Library)

## Overview

Python library dedicated exclusively to community detection in complex networks. Provides unified interface to 40+ community detection algorithms. Not a general graph library - focused solely on clustering/partitioning networks.

## Ecosystem Stats

- **GitHub Stars**: ~400
- **PyPI Downloads**: ~30K/month
- **First Release**: 2019
- **Maintenance**: Active (KDDLab, University of Pisa)
- **License**: BSD-2-Clause

## Core Strengths

**Comprehensive community detection**:
- 40+ algorithms in one interface
- Classic: Louvain, label propagation, Girvan-Newman
- Modern: Leiden, SBM-based, overlapping communities
- Comparative evaluation tools built-in
- Consistent API across all algorithms

**Evaluation and comparison**:
- 20+ quality metrics (modularity, NMI, ARI, coverage)
- Built-in benchmarking tools
- Statistical significance testing
- Visualization of communities
- Easy A/B testing of algorithms

**Algorithm diversity**:
- Non-overlapping communities (traditional partitions)
- Overlapping communities (nodes in multiple groups)
- Hierarchical community structure
- Dynamic/temporal community detection
- Attribute-aware community detection (node features + graph structure)

## Performance Characteristics

**Speed**: Depends on backend
- Wraps existing libraries (NetworkX, igraph, graph-tool)
- Performance = underlying library performance
- Overhead minimal (thin wrapper layer)
- Can leverage graph-tool for speed, NetworkX for ease

**Flexibility**: High
- Works with NetworkX, igraph, or graph-tool graphs
- Choose backend based on graph size
- Automatic conversion between graph formats

**Graph size handling**:
- Small graphs (<10K): Any backend works
- Medium (10K-1M): Use igraph backend
- Large (>1M): Use graph-tool backend
- Practical limit: backend library's limit

## Limitations

**Not a general graph library**:
- ONLY community detection (no centrality, shortest paths, etc.)
- Must use with NetworkX/igraph/graph-tool for other operations
- Cannot replace general-purpose libraries

**Dependency complexity**:
- Some algorithms require specific backends
- Not all algorithms available with all backends
- Installation complexity = sum of backend complexities
- graph-tool algorithms require graph-tool installation

**Performance variability**:
- Algorithm speed varies wildly (seconds to hours on same graph)
- No clear "best" algorithm guidance for new users
- Requires domain knowledge to choose appropriate algorithm

**Documentation gaps**:
- Algorithm descriptions brief
- Limited guidance on algorithm selection
- Assumes familiarity with community detection literature

## Best For

- **Community detection focus**: When finding clusters is the primary goal
- **Algorithm comparison**: Testing multiple methods on same data
- **Research**: Systematic evaluation of community structure
- **Overlapping communities**: Nodes belonging to multiple groups
- **Reproducible studies**: Standard benchmark datasets and metrics included

## Avoid For

- **General graph analysis**: Not a replacement for NetworkX/igraph
- **Single algorithm use**: Overkill if you just need Louvain once
- **Beginners**: Requires understanding of community detection methods
- **Real-time detection**: No streaming/incremental algorithms

## Ecosystem Position

**The community detection specialist**:
- Complements general graph libraries
- Use alongside NetworkX/igraph/graph-tool, not instead of
- Unique value: unified interface to diverse algorithms

**Typical workflow**:
```
1. Build graph with NetworkX/igraph
2. Pass to CDlib for community detection
3. Evaluate communities with CDlib metrics
4. Continue analysis with NetworkX/igraph
```

**When to add CDlib**:
- Need to compare multiple community detection algorithms
- Working on overlapping or dynamic communities
- Require systematic evaluation of clustering quality
- Research project focused on community structure

**When to skip CDlib**:
- General graph library (NetworkX/igraph) has the one algorithm you need
- Not doing community detection
- Want minimal dependencies
- Only need basic Louvain or label propagation
