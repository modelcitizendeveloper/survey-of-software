# S3 Need-Driven Discovery: Recommendation

## Executive Summary

Graph search libraries serve **four distinct user communities** with different needs:

1. **Game Developers**: Need A* for NPC pathfinding (Python for tools, C++ for runtime)
2. **Robotics Engineers**: Need A* for robot motion planning (Python for prototyping, C++ for production)
3. **Data Scientists**: Need BFS/Dijkstra for network analysis (Python is production)
4. **Logistics Engineers**: Need Dijkstra/A* for route optimization (Python for mid-scale, C++ for mega-scale)

**Key Insight**: Python graph libraries are PRODUCTION tools for data science, but PROTOTYPING tools for game dev, robotics, and large-scale logistics.

## Who Needs What?

### A* is Critical For:

| User Group | Why A* | Alternative? |
|------------|--------|--------------|
| **Game Developers** | Real-time NPC pathfinding | No (heuristic required for speed) |
| **Robotics Engineers** | Robot navigation planning | No (optimal paths critical) |
| **Logistics (Point-to-Point)** | Single-route optimization | Sometimes (Dijkstra if many destinations) |

**Libraries with A***: NetworkX, rustworkx, graph-tool

**Libraries WITHOUT A***: igraph, scipy.csgraph (deal-breaker for game dev, robotics)

### Dijkstra Sufficient For:

| User Group | Why Dijkstra Enough | Use Case |
|------------|---------------------|----------|
| **Data Scientists** | Exploring network structure (no specific target) | Network analysis, centrality |
| **Logistics (One-to-Many)** | Single depot to all customers | VRP, facility location |

**All libraries support Dijkstra**

## Performance Requirements by User Group

### Millisecond-Critical (Must be VERY fast)

**Game Developers**:
- **Requirement**: <1ms per A* query (100+ NPCs, 60 FPS)
- **Implication**: Python too slow for runtime, OK for tools
- **Library**: Custom C++ or C# (in-engine), NetworkX for tools

**Logistics APIs**:
- **Requirement**: <100ms API response time
- **Implication**: Python viable with rustworkx/graph-tool
- **Library**: rustworkx (production) or custom C++

### Second-Scale Acceptable (Interactive but not real-time)

**Robotics Research**:
- **Requirement**: <1 second initial plan, <100ms re-plan
- **Implication**: Python viable for research robots
- **Library**: NetworkX (prototyping) → C++ (production)

**Data Science**:
- **Requirement**: Minutes to hours for analysis (exploratory)
- **Implication**: NetworkX excellent, igraph when it's too slow
- **Library**: NetworkX (default), igraph (scale up)

## Scale Requirements by User Group

### Small-Medium Graphs (<100K nodes)

**Game Developers**: Typically 1K-10K node navigation meshes
**Robotics**: 10K-100K node occupancy grids
**Data Science (Small)**: Individual project networks

**Library Recommendation**: NetworkX (ease of use dominates)

### Large Graphs (100K-1M nodes)

**Data Science (Medium)**: Company social networks, mid-size biological networks
**Logistics**: Regional road networks

**Library Recommendation**: igraph or rustworkx (performance matters)

### Massive Graphs (>1M nodes)

**Data Science (Large)**: Facebook-scale social networks, entire biological databases
**Logistics**: National road networks, global supply chains

**Library Recommendation**: graph-tool (best performance) or graph database (Neo4j)

## Platform Constraints by User Group

### Must Work on Windows

**Game Developers**: Unity/Unreal development often on Windows
**Data Scientists**: Many use Windows laptops
**Logistics**: Internal tools may be Windows-based

**Libraries with Excellent Windows Support**:
- ✅ NetworkX
- ✅ igraph
- ✅ rustworkx
- ✅ scipy.csgraph
- ⚠️ graph-tool (WSL or Docker required)

### Linux-Focused

**Robotics**: ROS runs on Ubuntu (Linux standard)
**HPC Data Science**: Cluster computing (Linux)
**Production Servers**: Logistics APIs (Linux deployment)

**All libraries work well on Linux**

## Integration Requirements by User Group

### ROS Integration (Robotics)

**Critical**: Must work with ROS ecosystem
**Libraries**: NetworkX (common), custom C++ (performance-critical)
**Note**: Python is first-class in ROS, but C++ preferred for real-time nodes

### pandas/NumPy (Data Science)

**Critical**: Must convert DataFrames to graphs easily
**Libraries**: NetworkX (best), igraph (good), scipy.csgraph (excellent)

### OR Solvers (Logistics)

**Critical**: Must integrate with OR-Tools, Gurobi, CPLEX
**Libraries**: Any (called as subroutine), rustworkx (best performance)

### Game Engines (Game Dev)

**Critical**: Must export paths for Unity/Unreal
**Libraries**: NetworkX (tooling only), custom implementations (runtime)

## License Considerations by User Group

### Commercial Products (Strict Requirement)

**Game Developers**: AAA studios avoid GPL/LGPL
**Logistics Startups**: Need permissive for SaaS products

**Acceptable Licenses**:
- ✅ Apache-2.0 (rustworkx) - Most permissive
- ✅ BSD-3-Clause (NetworkX, scipy.csgraph) - Very permissive
- ⚠️ GPL-2.0 (igraph) - Review with legal team
- ❌ LGPL-3.0 (graph-tool) - Static linking restrictions

### Academia & Research (Permissive)

**Data Scientists (Academic)**: License less critical
**Robotics Research**: Usually open-source projects

**Any license acceptable** (including LGPL)

## Learning Curve by User Group

### Prioritize Ease of Use

**Data Scientists**: Jupyter notebooks, rapid iteration
**Game Developers (Tools)**: Quick prototyping, level design
**Robotics (Research)**: Algorithm experimentation

**Library**: NetworkX (easiest, most Pythonic)

### Willing to Invest in Learning

**Logistics (Production)**: Long-term system, justify learning time
**Robotics (Production)**: Safety-critical, worth deep understanding
**Data Science (Scale)**: Hit performance wall, must upgrade

**Libraries**: igraph (moderate curve), graph-tool (steep curve)

## Decision Matrix: Who Should Use What?

| User Group | Primary Use | 1st Choice | 2nd Choice | Avoid |
|------------|-------------|------------|------------|-------|
| **Game Dev (Tools)** | Level editing, prototyping | NetworkX | rustworkx | graph-tool |
| **Game Dev (Runtime)** | In-game pathfinding | Custom C++ | Unity/Unreal NavMesh | Python |
| **Robotics (Research)** | Algorithm development | NetworkX | rustworkx | scipy.csgraph |
| **Robotics (Production)** | Real robot navigation | C++ (OMPL) | rustworkx | NetworkX |
| **Data Science (Small)** | Network analysis | NetworkX | igraph | scipy.csgraph |
| **Data Science (Large)** | Big network analysis | igraph | graph-tool | NetworkX |
| **Logistics (Prototype)** | Algorithm testing | NetworkX | igraph | scipy.csgraph |
| **Logistics (Production)** | Route optimization API | rustworkx | Custom C++ | NetworkX |

## Key Findings by User Group

### Game Developers

**Need**: A*, real-time performance
**Reality**: Python for tooling only, not runtime
**Library**: NetworkX (prototyping), then port to C++/C#

### Robotics Engineers

**Need**: A*, safety-critical correctness
**Reality**: Python for research, C++ for production
**Library**: NetworkX (research), OMPL/custom (production)

### Data Scientists

**Need**: BFS, Dijkstra, all-pairs, ease of use
**Reality**: Python IS the production environment
**Library**: NetworkX (default), igraph (scale up)

### Logistics Engineers

**Need**: Dijkstra/A*, fast, integrate with OR solvers
**Reality**: Mixed (Python for mid-scale, C++ for mega-scale)
**Library**: rustworkx (good middle ground)

## Why Python Libraries Matter

### Prototyping and Research (Universal)

**All user groups**:
- Rapid algorithm development
- Validate correctness on small examples
- Benchmark different approaches
- Then port to production language if needed

### Production Use (Varies by Group)

**Data Science**: Python IS production ✅
**Logistics (Mid-Scale)**: Python production viable ✅
**Robotics**: Rarely (only simple robots) ⚠️
**Game Dev**: Never (too slow) ❌

## Common Misconceptions

### Misconception: "Python is always too slow for graph algorithms"

**Reality**: Depends on scale and latency requirements
- **Data Science**: NetworkX handles 100K node graphs fine (analysis not real-time)
- **Logistics**: rustworkx fast enough for APIs (<100ms queries)
- **Game Dev/Robotics**: TRUE for real-time use, but fine for tooling

### Misconception: "A* is always needed for shortest paths"

**Reality**: Depends on whether you have a heuristic
- **Game Dev/Robotics**: Coordinates available (Euclidean heuristic) → A* wins
- **Data Science**: Abstract networks (no coordinates) → Dijkstra sufficient
- **Logistics**: Roads have coordinates → A* when point-to-point

### Misconception: "graph-tool is always fastest"

**Reality**: Marginal over rustworkx, installation overhead not worth it unless:
- Massive graphs (>1M nodes)
- Linux-only environment
- Need advanced algorithms (community detection, inference)

## Final Recommendations by User Group

### Game Developers
**Use NetworkX for**: Map editor tools, pathfinding prototypes, level validation
**Don't use Python for**: In-game runtime pathfinding (too slow)

### Robotics Engineers
**Use NetworkX for**: Algorithm research, ROS integration scripts, offline planning
**Don't use Python for**: Safety-critical real-time planning (use C++/OMPL)

### Data Scientists
**Use NetworkX for**: Everything (default choice)
**Upgrade to igraph when**: NetworkX too slow (>100K nodes)
**Upgrade to graph-tool when**: igraph still too slow (rare)

### Logistics Engineers
**Use NetworkX for**: Prototyping VRP algorithms, consulting projects
**Use rustworkx for**: Production routing APIs, mid-scale optimization
**Use Custom C++ for**: Mega-scale (Uber, Amazon) or extreme latency requirements

## Conclusion

**Graph search libraries serve different roles for different users**:
- Game Dev: Tooling and prototyping (not production runtime)
- Robotics: Research and ROS glue code (not safety-critical control)
- Data Science: PRIMARY TOOL (Python is production)
- Logistics: Mid-scale production + prototyping (mega-scale needs C++)

**NetworkX is the universal starting point**, valued for ease of use across all groups. Performance libraries (rustworkx, igraph, graph-tool) become necessary when scale or latency demands it.
