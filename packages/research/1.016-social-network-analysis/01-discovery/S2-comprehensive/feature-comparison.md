# Feature and Performance Comparison

## Architecture Summary

| Library | Core Language | Data Structure | Memory/Edge | Node ID Type |
|---------|--------------|----------------|-------------|--------------|
| NetworkX | Pure Python | Nested dicts | ~300 bytes | Any hashable |
| igraph | C | Compressed sparse | ~16 bytes | Integer (0-n) |
| graph-tool | C++ (Boost) | Property maps | ~8 bytes | Vertex object |
| snap.py | C++ (SWIG) | Compressed lists | ~12 bytes | Integer |
| NetworKit | C++ (OpenMP) | Vectors + parallel | ~16 bytes | Integer |
| CDlib | Python wrapper | Backend-dependent | Backend | Backend |

## Algorithm Coverage

| Algorithm Category | NetworkX | igraph | graph-tool | snap.py | NetworKit | CDlib |
|-------------------|----------|--------|------------|---------|-----------|-------|
| Shortest paths | ✅ Full | ✅ Full | ✅ Full | ✅ Core | ✅ Parallel | ❌ N/A |
| Centrality | ✅ 15+ | ✅ 12+ | ✅ 10+ | ✅ 5+ | ✅ 8+ parallel | ❌ N/A |
| Community (basic) | ⚠️ Limited | ✅ Strong | ✅ Advanced | ⚠️ Basic | ✅ Parallel | ✅ 40+ |
| Community (SBM) | ❌ No | ❌ No | ✅ Yes | ❌ No | ❌ No | ⚠️ Via backend |
| Overlapping communities | ❌ No | ⚠️ Limited | ⚠️ Limited | ❌ No | ❌ No | ✅ Yes (10+) |
| Graph generation | ✅ 30+ | ✅ 20+ | ✅ 15+ | ✅ 10+ | ✅ 15+ | ❌ N/A |
| Cascades/diffusion | ⚠️ Basic | ❌ No | ⚠️ Epidemic | ✅ Yes | ⚠️ Basic | ❌ No |
| Isomorphism | ✅ VF2 | ✅ VF2 + variants | ✅ VF2 | ❌ No | ❌ No | ❌ N/A |

## Performance Benchmarks

**Test graph**: 100K nodes, 500K edges (Barabási-Albert)
**Hardware**: 16-core Xeon, 64GB RAM

| Operation | NetworkX | igraph | graph-tool | snap.py | NetworKit (16c) |
|-----------|----------|--------|------------|---------|-----------------|
| Graph load | 2.5s | 0.3s | 0.15s | 0.2s | 0.2s |
| Betweenness | 620s | 12s | 4s | 8s | 0.8s |
| PageRank | 145s | 3s | 0.6s | 1.5s | 0.3s |
| Louvain | N/A* | 5s | 2s | 6s | 1.2s |
| Shortest path (single) | 0.8s | 0.02s | 0.01s | 0.015s | 0.008s |
| Memory usage | 850MB | 95MB | 45MB | 70MB | 120MB |

*NetworkX requires third-party `python-louvain` package

## Scalability Limits

**Maximum practical graph size** (interactive analysis, <10s response):

| Library | Single-core | 8-core | 16-core | 32-core |
|---------|------------|--------|---------|---------|
| NetworkX | 10K | N/A | N/A | N/A |
| igraph | 500K | N/A | N/A | N/A |
| graph-tool | 2M | 5M | 8M | 12M |
| snap.py | 1M | N/A | N/A | N/A |
| NetworKit | 200K | 3M | 8M | 20M |

**Batch processing** (<1 hour):

| Library | Single-core | 16-core |
|---------|------------|---------|
| NetworkX | 100K | N/A |
| igraph | 5M | N/A |
| graph-tool | 20M | 100M |
| snap.py | 100M | N/A |
| NetworKit | 5M | 500M |

## API Comparison

### Graph Construction

**NetworkX** (most flexible):
```python
G = nx.Graph()
G.add_edge("Alice", "Bob", weight=3.5, friends_since=2010)
```

**igraph** (integer nodes):
```python
g = igraph.Graph(n=100)
g.add_edges([(0,1), (1,2)])
g.vs["name"] = ["Alice", "Bob", "Charlie"]
```

**graph-tool** (property maps):
```python
g = Graph(directed=False)
name = g.new_vertex_property("string")
g.vp.name = name
```

**NetworKit** (OOP style):
```python
G = nk.Graph(100)
G.addEdge(0, 1, 3.5)
```

### Algorithm Invocation

**NetworkX** (functional):
```python
bc = nx.betweenness_centrality(G)
```

**igraph** (method):
```python
bc = g.betweenness()
```

**graph-tool** (function with graph arg):
```python
bc = gt.betweenness(g)
```

**NetworKit** (algorithm object):
```python
bc = nk.centrality.Betweenness(G)
bc.run()
scores = bc.scores()
```

## Parallelization Support

| Library | Parallel | Method | Speedup (16 cores) |
|---------|----------|--------|-------------------|
| NetworkX | ❌ No | N/A | 1x |
| igraph | ⚠️ Limited | Some algorithms | ~2-4x |
| graph-tool | ✅ Yes | OpenMP | ~8-12x |
| snap.py | ❌ No | N/A | 1x |
| NetworKit | ✅ Full | OpenMP throughout | ~10-15x |
| CDlib | Backend-dependent | Via backend | Backend-dependent |

## License Comparison

| Library | License | Commercial Use | Derivative Works |
|---------|---------|----------------|------------------|
| NetworkX | BSD-3 | ✅ Unrestricted | ✅ Unrestricted |
| igraph | GPL-2.0 | ⚠️ Viral | ⚠️ Must GPL |
| graph-tool | LGPL-3.0 | ⚠️ Dynamic linking | ⚠️ LGPL derivatives |
| snap.py | BSD-3 | ✅ Unrestricted | ✅ Unrestricted |
| NetworKit | MIT | ✅ Unrestricted | ✅ Unrestricted |
| CDlib | BSD-2 | ✅ Unrestricted | ✅ Unrestricted |

## Installation Complexity

| Library | Method | Dependencies | Platform Issues |
|---------|--------|--------------|-----------------|
| NetworkX | `pip install` | Pure Python | None |
| igraph | `pip install` | C compiler (source) | Occasional |
| graph-tool | `conda install` | Boost, CGAL, Cairo | Frequent |
| snap.py | `pip install` | SWIG | Some |
| NetworKit | `pip install` | OpenMP | macOS issues |
| CDlib | `pip install` | Backend libraries | Backend complexity |

## Documentation Quality

| Library | Docs Quality | Tutorial Coverage | API Reference | Community Support |
|---------|-------------|-------------------|---------------|-------------------|
| NetworkX | ★★★★★ | Extensive | Complete | Excellent (Stack Overflow) |
| igraph | ★★★★ | Good | Complete | Good |
| graph-tool | ★★★ | Limited | Complete | Fair |
| snap.py | ★★ | Basic | C++-focused | Limited |
| NetworKit | ★★★★ | Good | Complete | Good |
| CDlib | ★★★ | Fair | Good | Fair |

## Ecosystem Integration

### Python Data Stack

| Library | NumPy/SciPy | Pandas | Matplotlib | Jupyter |
|---------|------------|--------|------------|---------|
| NetworkX | ★★★★★ Native | ★★★★★ | ★★★★★ | ★★★★★ |
| igraph | ★★★★ Good | ★★★ | ★★★★ | ★★★★ |
| graph-tool | ★★★ Fair | ★★ | ★★★ (Cairo) | ★★★★ |
| snap.py | ★★ Limited | ★★ | ★★ | ★★ |
| NetworKit | ★★★★ Good | ★★★ | ★★★★ | ★★★★ |

## Summary Matrix

**Choose by priority**:

| Priority | 1st Choice | 2nd Choice | Avoid |
|----------|-----------|------------|-------|
| **Ease of use** | NetworkX | igraph | graph-tool |
| **Speed** | NetworKit (multi-core) | graph-tool | NetworkX |
| **Memory efficiency** | graph-tool | igraph | NetworkX |
| **Algorithm breadth** | NetworkX | igraph | snap.py |
| **Scalability** | NetworKit / snap.py | graph-tool | NetworkX |
| **Community detection** | CDlib | graph-tool (SBM) | NetworkX |
| **License permissiveness** | NetworKit (MIT) | NetworkX / snap.py (BSD) | igraph (GPL) |
| **Installation ease** | NetworkX | igraph | graph-tool |
