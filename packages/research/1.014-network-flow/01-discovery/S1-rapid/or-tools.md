# OR-Tools (Multi-language)

**GitHub:** ~13K stars | **Ecosystem:** C++, Python, Java, C# | **License:** Apache 2.0

## Positioning

Google's production-grade combinatorial optimization suite with specialized, highly optimized network flow solvers. Industry standard for logistics, supply chain, and operations research.

## Key Metrics

- **Performance:** C++ core with optimized algorithms (10-100x faster than pure Python)
- **Download stats:** Enterprise usage (exact PyPI stats not public)
- **Maintenance:** Active Google development, v9.15 released Jan 2026
- **Language support:** First-class APIs for C++, Python, Java, C#
- **Contributors:** 151 people, 15,808 commits

## Algorithms Included

### Maximum Flow
- `SimpleMaxFlow` solver - optimized for basic max flow problems

### Minimum Cost Flow
- `SimpleMinCostFlow` solver - standard min cost flow
- `SolveMaxFlowWithMinCost()` - max flow with min cost variant
- Methods: `AddArcWithCapacityAndUnitCost`, `SetNodeSupply`

## Community Signals

**Stack Overflow sentiment:**
- "OR-Tools for production logistics - battle-tested at Google scale"
- "If you're building a real supply chain system, skip everything else and use OR-Tools"
- "Steeper learning curve than NetworkX, but worth it for performance"

**Common use cases:**
- Supply chain optimization (flow of goods through warehouses)
- Transportation routing with capacity constraints
- Task assignment with resource limits
- Network capacity planning
- Production systems requiring sub-second latency

## Trade-offs

**Strengths:**
- Production-grade performance and reliability (Google's internal tooling)
- Comprehensive documentation with multi-language examples
- Constraint programming (CP-SAT) integration for complex problems
- Specialized solvers tuned for specific problem types
- Cross-platform wheels (Python installation via pip)
- Winning gold medals in MiniZinc Challenge (solver competitions)

**Limitations:**
- Heavier dependency (larger binary size due to C++ core)
- Steeper learning curve than pure Python libraries
- API verbosity compared to NetworkX
- Requires understanding of operations research concepts
- Less suitable for ad-hoc graph exploration

## Decision Context

**Choose OR-Tools when:**
- Building production systems with hard performance requirements
- Graphs have >100K nodes or time-critical routing
- Need constraint programming beyond basic flow
- Working on logistics, supply chain, or scheduling problems
- Require multi-language deployment (Python backend, Java frontend)

**Skip if:**
- Prototyping or research (NetworkX is easier)
- Graph algorithms beyond optimization (centrality, clustering)
- Team lacks OR/optimization background
- Simple problems solvable in <1 second with pure Python
