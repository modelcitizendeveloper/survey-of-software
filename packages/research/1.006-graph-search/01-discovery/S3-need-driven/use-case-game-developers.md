# Use Case: Game Developers

## Who Needs This

**Primary Persona**: Indie and AAA game developers building real-time strategy, RPG, and simulation games

**Specific Roles**:
- Gameplay programmers (pathfinding for NPCs)
- AI engineers (intelligent agent navigation)
- Technical designers (level design validation)

**Team Context**:
- Solo indie developers (need simple, fast solutions)
- Medium studios (5-50 developers, Unity/Unreal workflows)
- AAA studios (100+ developers, custom engines)

## Why They Need Graph Search

### Primary Problem: Real-Time NPC Pathfinding

**The Challenge**:
- NPCs must navigate complex 3D environments with obstacles
- Pathfinding must run every frame (16ms budget at 60 FPS)
- Paths must look intelligent (not robotic, avoid wall-hugging)
- Dynamic obstacles (other NPCs, player actions, destructible terrain)

**Why A\* Specifically**:
- Guarantees shortest path (unlike greedy algorithms)
- Heuristic enables fast search (unlike Dijkstra)
- Predictable performance (critical for frame budgets)
- Can be tuned for "good enough" paths vs perfect paths

**Real-World Example**:
- RTS game with 100+ units navigating simultaneously
- Each unit needs path recalculation when terrain changes
- Must maintain 60 FPS on mid-range hardware
- Paths must avoid clustering (units blocking each other)

### Secondary Problems

**1. Procedural Map Validation**:
- **What**: Verify generated maps are fully traversable
- **Why**: BFS to check connectivity between spawn points
- **When**: Level generation, quality assurance testing

**2. Strategic AI Planning**:
- **What**: Evaluate multiple route options for tactical decisions
- **Why**: Dijkstra to find safest paths (weighted by danger zones)
- **When**: AI decides how to approach objectives

**3. Dynamic Navigation Mesh Updates**:
- **What**: Recalculate paths when walls destroyed/built
- **Why**: DFS to find newly accessible areas
- **When**: Real-time terrain destruction, building systems

## Specific Requirements

### Performance Constraints

**Frame Budget**: 1-2ms for all pathfinding (out of 16ms total)
- A* must complete in microseconds for typical paths
- Must support async pathfinding for distant goals
- Need path caching and reuse

**Scale Requirements**:
- Small indie game: 10-50 NPCs, 1000-node navigation graphs
- Medium game: 100-500 NPCs, 10K-node graphs
- AAA game: 1000+ NPCs, 100K-node graphs

### Platform Constraints

**Target Platforms**:
- PC (Windows, Linux, macOS)
- Consoles (PlayStation, Xbox, Nintendo Switch)
- Mobile (iOS, Android) for lighter games

**Integration Needs**:
- Must integrate with Unity/Unreal navigation systems
- Or standalone for custom engines
- Ideally C++ (for performance) or Python (for tooling)

## Pain Points with Current Solutions

### Using Built-in Engine Navigation

**Unity NavMesh**:
- ✅ Easy to use, visual tools
- ❌ Limited customization
- ❌ A* implementation hidden, can't optimize

**Unreal Navigation System**:
- ✅ Powerful, production-ready
- ❌ Heavyweight for simple games
- ❌ Overkill for 2D games

### Rolling Custom Solutions

**Common Approach**: Implement A* from scratch
- ✅ Full control, optimized for specific game
- ❌ Time-consuming (weeks to get right)
- ❌ Bug-prone (edge cases, performance issues)
- ❌ Maintenance burden

**What They Want**: Drop-in library that's fast enough, simple enough

## Decision Criteria

### Must-Haves

1. **A* support**: Heuristic-guided pathfinding essential
2. **Performance**: Sub-millisecond paths for typical queries
3. **2D/3D grids**: Grid-based graphs common in games
4. **Diagonal movement**: 8-way or hexagonal grids
5. **Obstacle avoidance**: Handle blocked cells dynamically

### Nice-to-Haves

1. **Multi-threading**: Offload pathfinding to background threads
2. **Path smoothing**: Post-process paths to look natural
3. **Hierarchical pathfinding**: For large open worlds
4. **Influence maps**: Weighted graphs for tactical AI
5. **Flowfields**: For RTS-style group movement

### Deal-Breakers

- ❌ Python-only (too slow for in-game use, OK for tools)
- ❌ No A* support (Dijkstra alone is too slow)
- ❌ Large dependency chains (bloats game builds)
- ❌ GPL/LGPL (many game studios avoid copyleft)

## Success Metrics

**How They Measure Success**:
1. **Frame time**: Pathfinding takes <5% of frame budget
2. **Path quality**: NPCs reach destinations without stuck states
3. **Player experience**: NPC movement feels intelligent, responsive
4. **Development time**: Pathfinding implementation took days, not weeks
5. **Iteration speed**: Can tweak costs/heuristics easily

## Why Python Graph Libraries?

**For Tooling, Not Runtime**:
- Level editor tools (validate map connectivity)
- Offline pathfinding baking (pre-compute paths)
- AI behavior prototyping (test strategies)
- Map generation (procedural level design)

**Runtime Pathfinding**:
- Usually C++ for performance
- But Python tools using NetworkX/rustworkx for prototyping
- Then port performant algorithms to C++

## Market Context

**Demand Indicators**:
- Unity Asset Store: 50+ pathfinding plugins ($10-$100 each)
- Unreal Marketplace: 30+ navigation solutions
- GitHub: 500+ game pathfinding repositories
- Game Dev job postings: "A* pathfinding experience" common requirement

**Alternative Solutions**:
- A\* Pathfinding Project (Unity, $100)
- Recast Navigation (C++, free, open source)
- Custom implementations (very common)

## Representative Use Cases

### Example 1: Tower Defense Game
- **Who**: Solo indie developer
- **Need**: 50 enemies navigate to base simultaneously
- **Solution**: Grid-based A* on 100x100 grid
- **Library fit**: NetworkX for prototyping → C++ for release

### Example 2: Open World RPG
- **Who**: 20-person indie studio
- **Need**: NPCs navigate city streets, follow player
- **Solution**: NavMesh with A* for dynamic obstacles
- **Library fit**: rustworkx for offline pathfinding tools

### Example 3: RTS Game
- **Who**: AA studio (50 developers)
- **Need**: 500 units navigate with formations, avoid collisions
- **Solution**: Hierarchical A* + flowfields
- **Library fit**: Custom C++ (too performance-critical for Python)

## Key Takeaway

**Game developers need A* for NPC pathfinding.** Python libraries (NetworkX, rustworkx) are useful for **tooling and prototyping**, but production games usually port to C++ for performance. The library choice matters most for **level editing tools**, **offline path baking**, and **AI behavior prototyping**.
