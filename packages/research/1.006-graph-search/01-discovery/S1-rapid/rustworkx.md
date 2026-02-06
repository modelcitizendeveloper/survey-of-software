# rustworkx (formerly retworkx)

## Overview
**Rust-based high-performance graph library for Python, originally developed for quantum computing workflows at IBM.**

## Key Stats (2025)
- **GitHub Stars**: ~1,100
- **PyPI Downloads**: 400K+/month
- **License**: Apache-2.0 (permissive)
- **Latest Release**: 0.15.x (actively developed)
- **Python Support**: 3.8+
- **Backed by**: IBM Quantum, Linux Foundation

## Graph Search Algorithms
✅ **A\* (astar_shortest_path)**: Full implementation with custom heuristics
✅ **Dijkstra (dijkstra_shortest_paths)**: Complete support
✅ **BFS (bfs_search, bfs_successors)**: Multiple variants
✅ **DFS (dfs_search, dfs_edges)**: Multiple variants
✅ **Specialized**: Betweenness, k-shortest paths, isomorphism

## Performance Profile
- **Speed**: Extremely fast (Rust backend, fastest of all Python graph libs)
- **Graph Size**: Designed for large graphs (tested with millions of nodes)
- **Memory**: Rust's memory safety without GC overhead
- **Benchmark**: ~120K Dijkstra ops/sec on 10K node graphs
- **Parallelism**: Some algorithms support parallel execution

## Strengths
- **Performance**: Fastest Python graph library (Rust core)
- **License**: Apache-2.0 (most permissive, commercial-friendly)
- **Installation**: Easy (pip install, pre-built wheels)
- **Modern**: Active development, modern architecture
- **Memory safety**: Rust prevents common C/C++ bugs
- **Quantum computing**: Optimized for quantum circuit graphs
- **Parallel algorithms**: Some operations support multi-threading

## Weaknesses
- **Maturity**: Younger than NetworkX/igraph (less battle-tested)
- **Ecosystem**: Smaller community than established libraries
- **API**: Still evolving (some breaking changes between versions)
- **Documentation**: Good but less comprehensive than NetworkX
- **Algorithm coverage**: Fewer algorithms than NetworkX (but growing)
- **Learning resources**: Fewer tutorials and Stack Overflow answers

## When to Choose rustworkx
✅ Performance critical (need fastest Python option)
✅ Large graphs (100K+ nodes)
✅ Need A* and Dijkstra at maximum speed
✅ Permissive license required (commercial products)
✅ Modern codebase preferred
✅ Quantum computing workflows
✅ Can tolerate API evolution

❌ Avoid for: Maximum algorithm variety, ultra-stable API, extensive learning resources, proven long-term stability

## Maturity Score: 7/10
- 5+ years development (started 2019)
- Active development (IBM backing)
- Growing adoption
- API still maturing
- Strong testing and CI
