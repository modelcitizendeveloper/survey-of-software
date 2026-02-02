# NetworkX

## Overview
**Pure Python graph library with comprehensive algorithm coverage. The de facto standard for graph analysis in Python.**

## Key Stats (2025)
- **GitHub Stars**: ~15,000
- **PyPI Downloads**: 10M+/month
- **License**: BSD-3-Clause
- **Latest Release**: 3.3 (actively maintained)
- **Python Support**: 3.10+

## Graph Search Algorithms
✅ **A\* (astar_path)**: Full support with custom heuristics
✅ **Dijkstra (dijkstra_path, shortest_path)**: Complete implementation
✅ **BFS (bfs_edges, bfs_tree)**: Multiple BFS variants
✅ **DFS (dfs_edges, dfs_tree)**: Multiple DFS variants
✅ **Bidirectional search**: A* and Dijkstra variants

## Performance Profile
- **Speed**: Moderate (pure Python overhead)
- **Graph Size**: Best for small-to-medium graphs (<100K nodes)
- **Memory**: Higher than C-based libraries
- **Benchmark**: ~1000 Dijkstra ops/sec on 10K node graphs

## Strengths
- **Comprehensive**: 500+ graph algorithms (not just search)
- **Easy to learn**: Pythonic API, excellent documentation
- **Ecosystem**: Integrates with NumPy, pandas, matplotlib
- **Community**: Largest Python graph community
- **Flexibility**: Easy to extend with custom algorithms

## Weaknesses
- **Performance**: 10-100x slower than C/C++ libraries
- **Large graphs**: Struggles with millions of nodes
- **Memory**: Not optimized for memory efficiency

## When to Choose NetworkX
✅ Prototyping and exploration
✅ Educational purposes
✅ Small-to-medium graphs (<100K nodes)
✅ Need many different algorithms (not just search)
✅ Prioritize code readability over performance
✅ Working in scientific Python stack (NumPy/pandas)

❌ Avoid for: Million-node graphs, real-time systems, memory-constrained environments

## Maturity Score: 10/10
- 20+ years of development
- Stable API (v3.0+)
- Comprehensive test coverage
- Active maintenance by core team
