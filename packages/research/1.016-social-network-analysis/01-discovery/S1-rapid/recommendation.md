# S1 Synthesis: Social Network Analysis Libraries

## Executive Summary

Python offers six major libraries for social network analysis, each optimized for different trade-offs between ease of use, performance, and scale. The best choice depends on three critical factors:

1. **Graph size**: Thousands, millions, or billions of nodes
2. **Hardware**: Laptop vs multi-core server
3. **Priority**: Learning/prototyping vs production performance

**Key finding**: There's no single "best" library - each dominates a different niche. NetworkX for learning, igraph for production, graph-tool for massive graphs, NetworKit for parallel processing, SNAP for billion-node networks, and CDlib for community detection research.

## Library Landscape Overview

### General-Purpose Libraries

**NetworkX** (Pure Python):
- **Speed**: Slowest (~10-100x slower than competitors)
- **Scale**: Up to ~100K nodes (interactive), ~1M nodes (batch)
- **Strength**: Ease of use, 500+ algorithms, excellent documentation
- **Weakness**: Performance on large graphs
- **Best for**: Learning, prototyping, small graphs

**igraph** (C core):
- **Speed**: Fast (~10-50x faster than NetworkX)
- **Scale**: Up to ~10M nodes
- **Strength**: Balance of speed and ease, comprehensive algorithms
- **Weakness**: GPL license, less Pythonic API
- **Best for**: Production analysis, medium to large graphs

**graph-tool** (C++ core):
- **Speed**: Fastest single-threaded (~100-1000x faster than NetworkX)
- **Scale**: Up to ~100M+ nodes
- **Strength**: Extreme performance, advanced community detection (SBM)
- **Weakness**: Installation complexity, steep learning curve, LGPL license
- **Best for**: Large-scale scientific research, performance-critical work

**snap.py** (C++ core):
- **Speed**: Very fast for core operations
- **Scale**: Billion-node graphs
- **Strength**: Extreme scalability, research provenance (Stanford)
- **Weakness**: Limited algorithms, awkward API, slower development
- **Best for**: Billion-node graphs, web-scale networks

**NetworKit** (C++ core, OpenMP):
- **Speed**: Fastest with multi-core hardware (~2-10x faster than graph-tool on 16+ cores)
- **Scale**: Up to ~1B edges (with sufficient cores/RAM)
- **Strength**: Parallel processing, algorithmic engineering
- **Weakness**: Requires multi-core hardware for benefits, narrower algorithm selection
- **Best for**: Multi-core servers, large-scale batch analysis

### Specialized Library

**CDlib**:
- **Type**: Community detection specialist (not general-purpose)
- **Strength**: 40+ algorithms, unified interface, evaluation tools
- **Weakness**: Requires general library (NetworkX/igraph/graph-tool) as backend
- **Best for**: Community detection research, algorithm comparison

## Quick Decision Matrix

### By Graph Size

| Nodes | Recommended | Alternative | Avoid |
|-------|------------|-------------|-------|
| <10K | NetworkX | igraph | graph-tool (overkill) |
| 10K-100K | NetworkX or igraph | graph-tool | SNAP (overkill) |
| 100K-1M | igraph | graph-tool | NetworkX (too slow) |
| 1M-10M | igraph or graph-tool | NetworKit (if 16+ cores) | NetworkX |
| 10M-100M | graph-tool | NetworKit (if 16+ cores) | NetworkX, igraph |
| 100M-1B | graph-tool or SNAP | NetworKit (32+ cores) | NetworkX, igraph |
| >1B | SNAP | Specialized systems | General libraries |

### By Priority

| Priority | Recommended | Why |
|----------|------------|-----|
| **Learning graph theory** | NetworkX | Clear implementations, excellent docs, educational focus |
| **Rapid prototyping** | NetworkX | Fast to write code, Pythonic, Jupyter-friendly |
| **Production reliability** | igraph | Maintained, fast, comprehensive, stable API |
| **Maximum performance** | graph-tool | Fastest single-threaded, advanced algorithms |
| **Parallel processing** | NetworKit | Multi-core optimization, 5-25x speedup with cores |
| **Billion-node graphs** | SNAP | Proven at web scale, efficient memory layout |
| **Community detection** | CDlib + igraph/graph-tool | 40+ algorithms, systematic evaluation |

### By Hardware

| Hardware | Recommended | Why |
|----------|------------|-----|
| **Laptop (4-8 cores)** | NetworkX or igraph | Ease > speed, limited parallel benefits |
| **Workstation (8-16 cores)** | igraph or graph-tool | Balance of ease and performance |
| **Server (16-32 cores)** | graph-tool or NetworKit | Leverage parallelism for speed |
| **HPC cluster (32+ cores)** | NetworKit | Maximum parallel efficiency |

## Performance Comparison

### Speed Relative to NetworkX (Approximate)

| Operation | NetworkX | igraph | graph-tool | NetworKit (16 cores) | SNAP |
|-----------|----------|--------|------------|---------------------|------|
| **Betweenness centrality** (1M nodes) | 1x (baseline) | 50x | 100x | 500x | 80x |
| **PageRank** (1M nodes) | 1x | 20x | 200x | 1000x | 150x |
| **Community detection** (1M nodes) | 1x | 20x | 50-500x* | 100x | 15x |
| **Shortest paths** (1M nodes) | 1x | 30x | 80x | 200x | 60x |

*graph-tool's SBM-based methods are extremely fast; simpler algorithms comparable to others

### Memory Efficiency (Relative)

| Library | Memory Overhead | Notes |
|---------|----------------|-------|
| graph-tool | Lowest (1x) | Compact Boost property maps |
| igraph | Low (1.2x) | Compressed sparse representation |
| SNAP | Low (1.3x) | Optimized for sparse graphs |
| NetworKit | Medium (1.5-2x) | Parallel data structures |
| NetworkX | High (2-3x) | Nested Python dictionaries |

## Algorithm Coverage Comparison

| Library | Total Algorithms | Centrality | Community Detection | Specialized |
|---------|-----------------|------------|---------------------|-------------|
| NetworkX | 500+ | Comprehensive | Basic | Extensive |
| igraph | 200+ | Comprehensive | Strong (Louvain, Infomap) | Good |
| graph-tool | 150+ | Comprehensive | Advanced (SBM, hierarchical) | Research-focused |
| SNAP | 50+ | Core measures | Basic | Cascades, diffusion |
| NetworKit | 80+ | Parallel versions | Good (parallel Louvain) | Sampling |
| CDlib | 40+ community only | N/A | Comprehensive (40+ methods) | Overlapping, temporal |

## Decision Tree

```
START: Need to analyze a network graph

├─ Graph size < 100K nodes?
│  ├─ YES: Learning/prototyping?
│  │  ├─ YES → NetworkX (easiest, great docs)
│  │  └─ NO → igraph (fast enough, production-ready)
│  └─ NO: Continue...
│
├─ Graph size 100K - 10M nodes?
│  ├─ Need ease of use → igraph
│  ├─ Need max performance → graph-tool
│  └─ Have 16+ cores → NetworKit
│
├─ Graph size 10M - 1B nodes?
│  ├─ Have 32+ cores → NetworKit
│  ├─ Single/few cores → graph-tool
│  └─ Need proven billion-node scale → SNAP
│
├─ Graph size > 1B nodes?
│  └─ → SNAP (or specialized distributed systems)
│
└─ Community detection focus?
   └─ → CDlib + (igraph or graph-tool backend)
```

## License Considerations

| Library | License | Commercial Use | Notes |
|---------|---------|----------------|-------|
| NetworkX | BSD-3 | ✅ Unrestricted | Most permissive |
| igraph | GPL-2.0 | ⚠️ Viral | Requires legal review for proprietary software |
| graph-tool | LGPL-3.0 | ⚠️ Dynamic linking OK | Less restrictive than GPL, but still copyleft |
| SNAP | BSD-3 | ✅ Unrestricted | Permissive |
| NetworKit | MIT | ✅ Unrestricted | Most permissive |
| CDlib | BSD-2 | ✅ Unrestricted | Permissive |

**For proprietary/commercial software**: Prefer NetworkX, SNAP, NetworKit, or CDlib. Consult legal team for igraph (GPL) or graph-tool (LGPL).

## Ecosystem Integration

### Python Stack Compatibility

| Library | NumPy/SciPy | Pandas | Matplotlib | Jupyter |
|---------|------------|--------|------------|---------|
| NetworkX | Excellent | Excellent | Native | Excellent |
| igraph | Good | Good | Good | Good |
| graph-tool | Good | Fair | Native (Cairo) | Good |
| SNAP | Fair | Fair | Manual | Fair |
| NetworKit | Good | Good | Good | Good |
| CDlib | Excellent (via backend) | Good | Native | Excellent |

### Installation Difficulty

| Library | Difficulty | Notes |
|---------|-----------|-------|
| NetworkX | Easy | Pure Python, pip install works everywhere |
| igraph | Medium | Binary wheels available, occasional platform issues |
| graph-tool | Hard | Conda only, complex dependencies (Boost, CGAL) |
| SNAP | Medium | Prebuilt wheels, some platform issues |
| NetworKit | Medium | OpenMP dependency, macOS can be tricky |
| CDlib | Easy | Pure Python wrapper, but backend dependency complexity |

## Common Use Cases: Best Library

| Use Case | Best Choice | Alternative |
|----------|------------|-------------|
| **Teaching graph theory** | NetworkX | - |
| **Interactive data exploration** | NetworkX + Jupyter | igraph |
| **Production web analytics** | igraph | graph-tool (if team can handle complexity) |
| **Large-scale scientific research** | graph-tool | NetworKit (if cluster available) |
| **Billion-user social network** | SNAP | Distributed systems (Giraph, GraphX) |
| **HPC batch analysis** | NetworKit | graph-tool |
| **Community detection comparison** | CDlib + graph-tool | CDlib + igraph |
| **Real-time recommendations** | Pre-computed with igraph/graph-tool | Specialized systems |

## Migration Paths

**Common progression**:
1. Start with **NetworkX** (learning, prototyping)
2. Hit performance wall at ~100K nodes
3. Move to **igraph** (production, maintained, good docs)
4. If still too slow or graph >10M nodes:
   - Multi-core server? → **NetworKit**
   - Single/few cores? → **graph-tool**
   - Billion nodes? → **SNAP**

**Minimize rewrites**:
- Keep business logic separate from graph library calls
- Use NetworkX-like APIs where possible (igraph has some compatibility)
- Test at scale early to avoid late migrations

## Final Recommendations

### For most users
**Start with NetworkX**, migrate to **igraph** when needed. This path minimizes friction while providing clear upgrade path.

### For production systems
**igraph** unless graph size or performance demands graph-tool/NetworKit. Balance of speed, reliability, and maintainability.

### For research
**graph-tool** if comfortable with installation/learning curve, or **igraph** for easier setup. Add **CDlib** if community detection is focus.

### For extreme scale
**NetworKit** (with 16+ cores) or **SNAP** (billion+ nodes). Specialized use cases only.

### For community detection
**CDlib** (with igraph or graph-tool backend) for comprehensive algorithm comparison, or library's built-in methods for single algorithm.

---

**The one-line summary**: NetworkX to learn, igraph for production, graph-tool for scale, NetworKit for parallelism, SNAP for billions, CDlib for communities.
