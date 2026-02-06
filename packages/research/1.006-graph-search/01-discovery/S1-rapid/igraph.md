# igraph

## Overview
**Fast C library for network analysis with Python, R, and Mathematica interfaces. Balance between performance and ease of use.**

## Key Stats (2025)
- **GitHub Stars**: ~4,500 (C core + Python wrapper)
- **PyPI Downloads**: 500K+/month
- **License**: GPL-2.0 (⚠️ copyleft, but can be used in proprietary apps)
- **Latest Release**: 0.11.x (actively maintained)
- **Python Support**: 3.8+

## Graph Search Algorithms
✅ **A\***: Not directly available (use shortest_paths with weights)
⚠️ **Dijkstra (shortest_paths)**: Available via generic shortest_path
✅ **BFS (bfs)**: Full implementation with callbacks
✅ **DFS (dfs)**: Full implementation with callbacks
✅ **Specialized**: Betweenness, closeness, diameter algorithms

## Performance Profile
- **Speed**: Fast (C backend, 50-80x faster than NetworkX)
- **Graph Size**: Handles large graphs well (up to millions of nodes)
- **Memory**: Efficient memory usage
- **Benchmark**: ~80K shortest path ops/sec on 10K node graphs

## Strengths
- **Performance**: Near graph-tool speeds, easier installation
- **Installation**: Simpler than graph-tool (pip install works)
- **Cross-platform**: Good Windows support
- **API**: More intuitive than graph-tool
- **R integration**: Use same library across Python/R projects
- **Community**: Strong community, used in academia

## Weaknesses
- **A\* support**: No dedicated A* implementation (workaround possible)
- **License**: GPL (though less restrictive than LGPL in practice)
- **Documentation**: Good but less comprehensive than NetworkX
- **Algorithm coverage**: Fewer algorithms than NetworkX
- **API differences**: Different paradigm from NetworkX (less Pythonic)

## When to Choose igraph
✅ Medium-to-large graphs (10K-1M nodes)
✅ Need good performance without installation complexity
✅ Cross-platform deployment (including Windows)
✅ Working with R as well as Python
✅ GPL license acceptable
✅ Don't need A* specifically

❌ Avoid for: A* pathfinding requirements, NetworkX API compatibility, maximum algorithm variety

## Maturity Score: 9/10
- 20+ years of development
- Stable API
- Active maintainer (Gábor Csárdi, Tamás Nepusz)
- Used widely in academic research
