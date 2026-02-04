# Performance Comparison: Python DES Libraries

## Critical Research Finding

**NO comprehensive performance benchmarks exist** comparing SimPy, salabim, Ciw, Mesa, and desmod across standardized workloads (as of October 2025).

## Research Evidence

### What Was Found:
- SimPy documented as "fast" (anecdotal, no numbers)
- salabim uses greenlet coroutines (claimed performance benefit)
- Mesa-frames developed (2024) specifically to address Mesa performance limits
- Python DES ~2.2x slower than R-simmer (only cross-language comparison found)

### What Was NOT Found:
- Event throughput comparisons (events/second)
- Memory usage comparisons
- Scaling benchmarks (performance vs model size)
- Standardized test suite results

## Performance Claims (Unverified)

| Library | Claim | Source |
|---------|-------|--------|
| SimPy | "Efficient process-based implementation" | Official docs |
| salabim | "Minimal overhead when animation disabled" | Documentation |
| Mesa | "Mesa-frames addresses performance limits" | GSoC 2024 project |
| Ciw | No specific claims | — |
| desmod | No specific claims | — |

## Indirect Performance Indicators

### SimPy
- **20+ years of optimization**: Mature codebase suggests performance refinement
- **Minimal dependencies**: Lower overhead than feature-rich alternatives
- **Generator-based**: Python generators are efficient for coroutine-style code

### salabim
- **Greenlet coroutines**: Potentially faster context switching than generators
- **Lightweight option**: Can disable animation to reduce overhead

### Mesa
- **Mesa-frames (2024)**: Indicates vanilla Mesa struggles with large agent counts
- **Agent overhead**: Each agent is an object with state (higher memory than passive entities)

### Ciw
- **Focused scope**: Queueing-specific code may be more optimized than general libraries
- **No animation**: Lower overhead than salabim/Mesa

### desmod
- **Built on SimPy**: Inherits SimPy's performance baseline
- **Component overhead**: Additional abstraction layer may add slight overhead

## Cross-Language Comparison (Limited Evidence)

**Python DES vs R-simmer**: One study found Python SimPy ~2.2x slower than R-simmer (C++-backed DES).

**Implication**: Python DES is adequate for business modeling but not for extreme performance needs (>10M events/second, real-time embedded systems).

## Practical Performance Guidelines

### When Python DES is Sufficient:
- Business process modeling (<1M events)
- Capacity planning simulations
- Educational/research models
- Prototyping and analysis

### When to Consider Compiled Tools:
- Real-time control systems
- Extreme-scale simulations (>10M events)
- Performance-critical applications (trading systems, embedded control)

### Mitigation Strategies:
1. **Profile first**: Identify actual bottlenecks before optimizing
2. **Vectorize data collection**: Use pandas DataFrame operations, not row-by-row
3. **Minimize logging**: Print statements are expensive at scale
4. **Use PyPy**: Alternative Python interpreter, can speed up pure Python code
5. **Cython/Numba**: Compile hot paths for critical code

## Research Gap: Need for Standardized Benchmark

**Proposal**: Community-driven benchmark suite testing:
- M/M/1 queue (10k, 100k, 1M events)
- M/M/c queue with varying c (1, 5, 10 servers)
- Multi-stage network (3 nodes, 5 nodes, 10 nodes)
- Memory footprint (entities in system)
- Event scheduling overhead (empty processes)

**Benefit**: Evidence-based library selection for performance-critical projects.

## Pragmatic Recommendation

**Default assumption**: All five libraries are "fast enough" for typical business simulations (<100k entities, <1M events).

**Choose based on features, not speed**:
- Usability (yieldless API, built-in stats)
- Documentation quality
- Community support
- Integration ecosystem

**Only benchmark if**:
- Your simulation will exceed 1M events
- Performance is a known constraint
- You've exhausted algorithmic optimizations

## Summary

Performance comparison is **limited by lack of data**. All Python DES libraries are adequate for business use cases. Choose based on features, community, and usability—not unverified speed claims.

**Research need**: Community-developed benchmark suite for evidence-based performance comparison.
