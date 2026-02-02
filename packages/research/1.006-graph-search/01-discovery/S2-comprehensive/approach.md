# S2 Comprehensive Discovery: Approach

## Research Question
How do these graph search libraries implement A*, Dijkstra, and BFS/DFS? What are the architectural differences, API patterns, and performance characteristics?

## Methodology
1. **Architecture analysis**: Examine implementation strategies (pure Python vs C/Rust bindings)
2. **Algorithm inspection**: Review specific algorithm implementations
3. **API patterns**: Compare API design and usage patterns
4. **Performance deep-dive**: Analyze time/space complexity, benchmark methodologies
5. **Integration patterns**: Examine how libraries integrate with NumPy, pandas, etc.

## Focus Areas
- **Implementation details**: Language choice, data structures, optimization techniques
- **API design**: How search algorithms are exposed and configured
- **Performance trade-offs**: Speed vs memory, flexibility vs optimization
- **Extension points**: How to customize algorithms, add heuristics
- **Real-world usage**: Patterns from production code

## Libraries Deep-Dived
1. NetworkX (pure Python reference implementation)
2. rustworkx (Rust performance leader)
3. graph-tool (C++ academic powerhouse)
4. igraph (C cross-platform library)
5. scipy.csgraph (SciPy sparse matrix approach)

## Technical Questions Answered
- What data structures are used for graph representation?
- How is A* heuristic function customization handled?
- What are the actual Big-O complexities in practice?
- How do priority queues affect performance?
- What memory optimizations are used?
- How do these libraries handle weighted vs unweighted graphs?
