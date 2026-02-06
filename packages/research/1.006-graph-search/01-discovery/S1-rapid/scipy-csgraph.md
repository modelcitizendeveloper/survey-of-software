# scipy.sparse.csgraph

## Overview
**SciPy's sparse graph algorithms module. Lightweight, fast, focused on essential graph operations with NumPy integration.**

## Key Stats (2025)
- **Part of**: SciPy (50M+ downloads/month)
- **License**: BSD-3-Clause (permissive)
- **Python Support**: 3.9+ (follows SciPy)
- **Installation**: `pip install scipy` (no extra dependencies)

## Graph Search Algorithms
❌ **A\***: Not available
✅ **Dijkstra (dijkstra, shortest_path)**: Full implementation
✅ **BFS (breadth_first_order, breadth_first_tree)**: Available
✅ **DFS (depth_first_order, depth_first_tree)**: Available
✅ **Specialized**: Floyd-Warshall, Bellman-Ford, minimum spanning trees

## Performance Profile
- **Speed**: Very fast (C/Cython backend, comparable to igraph)
- **Graph Size**: Efficient for sparse graphs (millions of edges)
- **Memory**: Excellent (uses sparse matrices)
- **Benchmark**: ~70K shortest path ops/sec on sparse 10K node graphs

## Strengths
- **No extra dependency**: Already installed if using NumPy/SciPy stack
- **Performance**: Fast C/Cython implementation
- **Sparse matrices**: Optimized for sparse graphs (adjacency matrices)
- **NumPy integration**: Seamless with scientific Python
- **Lightweight**: Minimal API surface, focused tools
- **Memory**: Excellent for sparse graphs

## Weaknesses
- **No A\***: Critical limitation for pathfinding applications
- **Limited API**: Fewer algorithms than dedicated graph libraries
- **Graph representation**: Must use sparse matrices (less intuitive)
- **No graph objects**: Raw matrix operations only
- **Visualization**: No built-in graph drawing
- **Community**: Smaller graph-specific community

## When to Choose scipy.csgraph
✅ Already using NumPy/SciPy stack
✅ Sparse graphs (few edges relative to nodes)
✅ Simple shortest path needs (Dijkstra sufficient)
✅ Minimize dependencies
✅ Scientific computing context
✅ Memory efficiency critical

❌ Avoid for: A* pathfinding, rich graph APIs, visualization, complex graph operations, need for graph objects

## Maturity Score: 10/10
- Part of SciPy (20+ years, battle-tested)
- Extremely stable API
- Professional maintenance
- Comprehensive testing
