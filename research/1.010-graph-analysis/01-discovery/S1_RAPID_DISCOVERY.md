# S1 Rapid Discovery: Python Graph Analysis Libraries (2025)

## Executive Summary

**TL;DR:** Use **NetworkX** for learning/prototyping, **igraph** for balanced performance/usability, **NetworKit** for large-scale analysis, **graph-tool** for maximum performance, or **rustworkx** for Rust-powered speed.

## Top 5 Graph Analysis Libraries (Ranked by Use Case)

### 1. NetworkX 🏆 **Best for Learning & Prototyping**
- **Performance**: Slowest (40-250x slower than alternatives)
- **Installation**: Pure Python - trivial installation, no compilation
- **Strengths**: Excellent documentation, user-friendly API, massive community
- **Downloads**: 2.3M+ daily downloads (most popular)
- **Use When**: Learning graph algorithms, rapid prototyping, small graphs (<10K nodes)
- **Avoid When**: Performance-critical applications, large datasets

```python
# Easy to get started
import networkx as nx
G = nx.Graph()
# Rich algorithm library with intuitive API
```

### 2. igraph 🚀 **Best Balanced Choice**
- **Performance**: 10-40x faster than NetworkX
- **Installation**: C++ backend with Python bindings
- **Strengths**: Good performance, reasonable learning curve, R/C++ compatibility
- **Use When**: Production applications, medium-large graphs, need cross-language support
- **Key Advantage**: Ideal balance of performance, usability, and features

```python
# Performance with reasonable API
import igraph as ig
g = ig.Graph()
# Fast algorithms with good documentation
```

### 3. NetworKit ⚡ **Best for Large-Scale Analysis**
- **Performance**: Extremely fast on specific algorithms (PageRank: 0.2s vs 1.7s graph-tool)
- **Installation**: C++ with OpenMP support
- **Strengths**: Designed for billion-edge networks, excellent parallel processing
- **Use When**: Massive graphs (millions+ nodes), specific algorithms like PageRank/k-core
- **Limitation**: More specialized, steeper learning curve

```python
# Built for scale
import networkit as nk
# Optimized for billion-edge networks
```

### 4. graph-tool 🔥 **Best Raw Performance**
- **Performance**: Fastest overall (up to 250x faster than NetworkX)
- **Installation**: Complex compilation, high memory requirements
- **Strengths**: Maximum speed, OpenMP parallelization, extensive algorithms
- **Use When**: CPU-intensive analysis, have compilation resources, need maximum speed
- **Trade-off**: Installation complexity vs performance gains

```python
# Maximum performance
from graph_tool.all import *
# Fastest algorithms available
```

### 5. rustworkx 🦀 **Best Rust Alternative**
- **Performance**: High performance via Rust backend
- **Installation**: Pre-compiled binaries available
- **Strengths**: Rust safety/performance, growing ecosystem, Qiskit integration
- **Use When**: Want Rust performance, working with quantum computing, modern toolchain
- **Status**: Actively developed, originally retworkx, now rustworkx

```python
# Rust-powered performance
import rustworkx as rx
# Modern high-performance alternative
```

## Performance Comparison Matrix

| Library | Shortest Path | PageRank | Community Detection | Memory Usage | Installation |
|---------|---------------|----------|-------------------|--------------|--------------|
| NetworkX | ❌ Baseline | ❌ 59.6s | ❌ Slow | ✅ Low | ✅ Trivial |
| igraph | ✅ 10x faster | ⚠️ 59.6s | ✅ Good | ✅ Moderate | ⚠️ Compilation |
| NetworKit | ✅ 10x faster | ✅ 0.2s | ✅ Excellent | ✅ Efficient | ⚠️ C++ deps |
| graph-tool | ✅ 40-250x faster | ✅ 1.7s | ✅ Excellent | ⚠️ High | ❌ Complex |
| rustworkx | ✅ Fast | ✅ Fast | ✅ Good | ✅ Efficient | ✅ Pre-compiled |

## Decision Framework (Choose in 30 seconds)

### 📚 **Learning/Research/Small Graphs** → NetworkX
- Pure Python, extensive docs, huge community
- Accept performance trade-off for ease of use

### ⚖️ **Production Applications** → igraph
- Best balance of performance and usability
- Cross-language support (R, C++)
- Reasonable compilation requirements

### 📊 **Large-Scale Data (>1M nodes)** → NetworKit
- Built for billion-edge networks
- Excellent on specific algorithms (PageRank, k-core)
- Worth the steeper learning curve

### 🏎️ **Maximum Performance** → graph-tool
- Fastest available, 40-250x speedup
- Accept installation complexity
- OpenMP parallelization

### 🔮 **Modern/Future-Proof** → rustworkx
- Rust performance and safety
- Growing ecosystem
- Quantum computing integration

## Algorithm-Specific Recommendations

### Shortest Path Analysis
1. **graph-tool** (fastest)
2. **NetworKit** (10x faster than NetworkX)
3. **igraph** (good performance)

### Centrality Measures
1. **NetworKit** (PageRank: 0.2s)
2. **graph-tool** (1.7s, OpenMP support)
3. **igraph** (reasonable performance)

### Community Detection
1. **graph-tool** (extensive algorithms)
2. **NetworKit** (large-scale optimization)
3. **CDlib** (algorithm comparison library)

## Key Insights for 2025

### Performance Revolution
- **40-250x speed differences** between pure Python (NetworkX) and C++ backends
- **Rust alternatives** (rustworkx) gaining traction
- **Parallel processing** (OpenMP) critical for large datasets

### Ecosystem Maturity
- NetworkX dominates **popularity** (2.3M daily downloads)
- Performance libraries have **mature APIs** and good documentation
- **Installation barriers** decreasing with pre-compiled binaries

### Maintenance Status
- All major libraries **actively maintained** in 2025
- NetworkX supports Python 3.11-3.13
- NetworKit released updates in March 2025

## Installation Quick Reference

```bash
# NetworkX - Pure Python
pip install networkx

# igraph - Requires compilation
pip install igraph  # or conda install igraph

# NetworKit - C++ dependencies
pip install networkit

# graph-tool - Complex (use conda)
conda install -c conda-forge graph-tool

# rustworkx - Pre-compiled available
pip install rustworkx
```

## Bottom Line

**For immediate decisions:**
- **Prototype/Learn**: NetworkX (easiest start)
- **Production**: igraph (best balance)
- **Scale**: NetworKit (billion-edge capable)
- **Speed**: graph-tool (maximum performance)
- **Modern**: rustworkx (Rust-powered future)

**Performance vs Usability Trade-off**: NetworkX remains popular despite being 40-250x slower because it's trivial to install and has excellent documentation. Choose performance libraries when speed matters more than convenience.

---

**Date compiled**: 2025-09-28