# S2 Recommendation: Technical Selection Guide

## Architecture-Driven Decision Framework

S2 revealed that library choice is fundamentally an **architectural trade-off**. No library dominates all dimensions - each optimizes for different constraints.

## The Core Trade-Offs

### 1. Ease vs Performance

**NetworkX** sacrifices speed for:
- Pythonic API (any hashable node type)
- Transparent implementations (readable source)
- Rich ecosystem integration

**Cost**: 10-100x slower, 10-25x more memory

**igraph/graph-tool** sacrifice ease for:
- C/C++ performance
- Memory efficiency
- Scalability

**Cost**: Steeper learning curve, integer-only nodes, installation complexity

### 2. Single-core vs Multi-core

**Most libraries** (NetworkX, igraph, snap.py):
- Optimized for single-core
- No parallelization overhead

**NetworKit/graph-tool**:
- Leverage multi-core hardware
- 5-15x speedup on 16+ cores
- Higher memory usage
- Require OpenMP support

**Decision**: Multi-core only valuable if you have the hardware and graph size justifies it.

### 3. General-purpose vs Specialized

**Comprehensive** (NetworkX, igraph, graph-tool):
- 150-500+ algorithms
- Handle any graph analysis task

**Specialized** (snap.py, NetworKit, CDlib):
- Narrower algorithm selection
- Optimized for specific use cases (scale, parallelism, communities)

**Decision**: Match library strengths to workload requirements.

## When Architecture Differences Matter

### Graph Size Threshold Analysis

**< 10K nodes**:
- All libraries fast enough (<1s for most operations)
- **Choose**: NetworkX (easiest API)
- Performance difference negligible

**10K - 100K nodes**:
- NetworkX becomes slow (>10s for complex operations)
- **Choose**: igraph (balanced speed/ease)
- Or NetworkX if development speed > execution speed

**100K - 10M nodes**:
- NetworkX impractical (minutes to hours)
- **Choose**: igraph (general) or graph-tool (performance-critical)
- NetworKit if 16+ cores available

**10M - 1B nodes**:
- Only graph-tool, NetworKit, snap.py viable
- **Choose**: graph-tool (comprehensive) or NetworKit (multi-core) or snap.py (proven at billion-scale)

**> 1B nodes**:
- **Choose**: snap.py or specialized distributed systems
- General libraries not designed for this scale

### Hardware Sensitivity

**Laptop / workstation (1-8 cores)**:
- Parallel libraries (NetworKit, graph-tool) show limited gains
- **Choose**: NetworkX (small graphs) or igraph (medium graphs)

**Server (16-32 cores)**:
- Parallel libraries shine (5-15x speedup)
- **Choose**: NetworKit (parallelism-first) or graph-tool (comprehensive + parallel)

**HPC cluster (32+ cores)**:
- NetworKit achieves best scaling
- **Choose**: NetworKit (best parallel efficiency)

### Algorithm Requirements

**Need Louvain/Leiden community detection**:
- NetworkX: Requires third-party package
- **Choose**: igraph (built-in) or graph-tool (faster) or CDlib (systematic comparison)

**Need SBM (stochastic block models)**:
- Only available in graph-tool
- **Choose**: graph-tool (no alternatives)

**Need overlapping communities**:
- Most libraries: Non-overlapping only
- **Choose**: CDlib (10+ overlapping algorithms)

**Need cascades/diffusion models**:
- snap.py: Best coverage
- **Choose**: snap.py or implement in general library

## License-Driven Decisions

### Commercial / Proprietary Software

**GPL-compatible**: igraph OK
**GPL-incompatible**: Avoid igraph, use:
- NetworkX (BSD-3)
- snap.py (BSD-3)
- NetworKit (MIT - most permissive)
- graph-tool only with dynamic linking (LGPL)

### Open Source / Academic

All libraries viable - choose on technical merits.

## Migration Complexity

### From NetworkX

**To igraph**: Moderate effort
- Node IDs: Must convert to integers
- API: Method-based vs functional
- Attributes: Different access pattern
- **Benefit**: 10-50x speedup

**To graph-tool**: High effort
- Property maps: Conceptually different
- API: Boost-style complexity
- **Benefit**: 100-1000x speedup

**To NetworKit**: Moderate effort
- OOP algorithm objects
- Integer node IDs
- **Benefit**: 10-100x speedup (with cores)

### Minimizing Migration Pain

**Best practice**:
1. Abstract graph operations behind interface
2. Keep NetworkX API for prototyping
3. Swap backend when deploying
4. Use CDlib pattern (backend-agnostic wrapper)

## Production Deployment Considerations

### Maintenance & Stability

**Most stable**: NetworkX (20+ years, NumFOCUS)
**Production-ready**: igraph, graph-tool (active development, stable APIs)
**Slower updates**: snap.py (academic project pace)

### Team Expertise

**Python-first teams**: NetworkX or igraph
**HPC/systems teams**: graph-tool or NetworKit
**Research teams**: graph-tool (cutting-edge algorithms)

### SLA Requirements

**Sub-second response** (web API):
- Graph size must be small, or
- Use igraph/graph-tool with precomputation

**Batch processing** (overnight jobs):
- Can use slower libraries (NetworkX) for small graphs
- Must use fast libraries (graph-tool, NetworKit) for large

## Recommended Combinations

### The Standard Stack

**Development**: NetworkX
- Prototype quickly
- Explore algorithms
- Integrate with Jupyter/Pandas

**Production**: igraph
- Migrate when hitting performance limits
- Balanced speed/ease
- Maintained and stable

**Large-scale**: graph-tool
- When igraph too slow
- Performance-critical workloads

### The Specialist Stack

**Community detection focus**:
- Base: igraph or graph-tool
- Add: CDlib for algorithm comparison
- Advanced: graph-tool for SBM

**Billion-node graphs**:
- Primary: snap.py (proven at scale)
- Alternative: NetworKit (if 32+ cores)
- Fallback: Distributed systems (GraphX, Giraph)

### The HPC Stack

**Multi-core server**:
- Primary: NetworKit (best parallel scaling)
- Secondary: graph-tool (comprehensive + parallel)
- Avoid: Single-threaded libraries

## Anti-Patterns

### Don't Do This

❌ Use NetworkX for production >100K nodes
- Too slow, will hit scaling wall
- Migrate to igraph instead

❌ Use graph-tool for small graphs (<10K)
- Installation friction not worth performance gain
- NetworkX easier, fast enough

❌ Use NetworKit on single-core laptop
- No performance benefit over igraph
- Extra complexity for no gain

❌ Implement community detection from scratch
- Use CDlib or library built-ins
- Avoid reinventing complex algorithms

❌ Mix licenses carelessly
- GPL (igraph) in proprietary software = legal issues
- Check license compatibility early

## Decision Algorithm

```
1. What's your graph size?
   < 10K → NetworkX
   10K-100K → NetworkX or igraph
   100K-10M → igraph or graph-tool
   10M-1B → graph-tool, NetworKit, or snap.py
   > 1B → snap.py or distributed

2. Do you have multi-core server (16+)?
   YES + graph >10M → NetworKit
   NO → graph-tool or igraph

3. Need specific algorithm?
   SBM → graph-tool (only option)
   Overlapping communities → CDlib
   Cascades → snap.py
   General → NetworkX or igraph

4. License constraints?
   Proprietary → Avoid igraph (GPL)
   Prefer: NetworKit (MIT) > NetworkX/snap.py (BSD)

5. Team expertise?
   Python-first → NetworkX or igraph
   HPC/systems → graph-tool or NetworKit
```

## Final Recommendation

**Default path** (covers 80% of use cases):
1. Start: **NetworkX** (prototype, explore)
2. Scale: **igraph** (production, maintained)
3. Optimize: **graph-tool** (performance-critical)

**Specialist paths**:
- Multi-core servers → **NetworKit**
- Billion-node graphs → **snap.py**
- Community detection research → **CDlib** + backend
- Cutting-edge algorithms → **graph-tool**

**The pragmatic choice**: **igraph** balances all concerns well enough for most production use cases.
