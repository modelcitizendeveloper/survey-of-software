# Use Case: Robotics Engineers

## Who Needs This

**Primary Persona**: Robotics engineers building autonomous navigation systems

**Specific Roles**:
- Motion planning engineers (path planning algorithms)
- Perception engineers (obstacle avoidance integration)
- Systems engineers (robot fleet coordination)

**Team Context**:
- Research labs (university, corporate R&D)
- Startups (autonomous delivery, warehouse robotics)
- Established companies (manufacturing, logistics automation)

**Common Frameworks**: ROS (Robot Operating System), ROS 2, custom C++/Python stacks

## Why They Need Graph Search

### Primary Problem: Safe, Efficient Robot Navigation

**The Challenge**:
- Robot must navigate from A to B in physical 3D space
- Avoid static obstacles (walls, furniture, machinery)
- Avoid dynamic obstacles (people, other robots, moving objects)
- Minimize energy consumption (battery life critical)
- Meet real-time constraints (can't stop to think for minutes)

**Why A\* Specifically**:
- Guarantees optimal paths (critical for battery efficiency)
- Heuristic speeds up search (real-time requirement)
- Can incorporate cost functions (safety margins, terrain difficulty)
- Proven in robotics (decades of research, well-understood)

**Real-World Examples**:
- Warehouse robot navigating between storage shelves
- Delivery robot on sidewalks with pedestrians
- Manufacturing robot moving parts between stations
- Autonomous vacuum cleaner covering entire floor plan

### Motion Planning Stack

**Configuration Space Planning**:
- **What**: Plan robot arm movements through valid joint configurations
- **Why**: A* to find collision-free paths in high-dimensional space
- **Complexity**: 6-DOF robot arm = 6D graph search

**Global Path Planning**:
- **What**: High-level path from start to goal on map
- **Why**: A* on occupancy grid or roadmap graph
- **Typical**: 2D grid (ground robots) or 3D voxel grid (drones)

**Local Path Planning**:
- **What**: Real-time obstacle avoidance while following global path
- **Why**: DFS/BFS to explore local escape options
- **Timing**: 10-50Hz update rate

## Specific Requirements

### Performance Constraints

**Real-Time Planning**:
- Initial path: <1 second (acceptable for robot to "think")
- Re-planning (obstacle detected): <100ms (react quickly)
- Continuous re-planning: 10-50Hz (dynamic environments)

**Scale Requirements**:
- **Small robots** (vacuums, toys): 100x100 grid, simple heuristics
- **Warehouse robots**: 1000x1000 grid, complex cost functions
- **Outdoor robots**: Multi-layered maps, elevation, terrain types

### Platform Constraints

**Hardware**:
- Onboard computers (limited CPU, e.g., NVIDIA Jetson)
- Must run alongside perception, control loops
- Battery-powered (computational efficiency matters)

**Software**:
- ROS integration essential (most robots use ROS)
- Often Python for prototyping, C++ for production
- Need cross-platform (develop on Ubuntu, deploy on embedded Linux)

## Pain Points with Current Solutions

### ROS Navigation Stack

**What**: ROS navstack (move_base, nav2)
- ✅ Production-ready, well-tested
- ✅ Includes global (A*) and local planners
- ❌ Complex to configure (100+ parameters)
- ❌ Heavyweight for simple robots
- ❌ Difficult to customize cost functions

### Custom Planning

**What**: Implement motion planning from research papers
- ✅ Can optimize for specific robot/environment
- ❌ Extremely time-consuming (months of work)
- ❌ Bugs have physical consequences (robot crashes)
- ❌ Must validate extensively

### What Roboticists Want

**Ideal Solution**:
- Drop-in A* that works with ROS
- Easy to customize cost functions (terrain types, safety margins)
- Fast enough for real-time re-planning
- Well-tested (robotics bugs can damage hardware)

## Decision Criteria

### Must-Haves

1. **A* with custom heuristics**: Euclidean, Manhattan, or domain-specific
2. **Weighted graphs**: Different terrain costs (grass vs concrete vs stairs)
3. **Dynamic re-planning**: Update paths when new obstacles detected
4. **3D support**: For drones, multi-floor buildings
5. **Proven correctness**: Bugs cause physical damage

### Nice-to-Haves

1. **Anytime planning**: Return best path so far if time runs out
2. **Multi-resolution**: Coarse planning → fine refinement
3. **Kinematic constraints**: Consider robot turning radius
4. **ROS integration**: Pre-built ROS nodes/messages
5. **Visualization**: Debug paths in RViz (ROS visualizer)

### Deal-Breakers

- ❌ No 3D support (limits to ground robots only)
- ❌ Slow (can't meet real-time constraints)
- ❌ Python-only for production (too slow for tight loops)
- ❌ No obstacle avoidance integration

## Success Metrics

**How They Measure Success**:
1. **Path optimality**: Within 5% of theoretical shortest path
2. **Planning time**: <100ms for typical re-planning
3. **Success rate**: Robot reaches goal >99% of attempts
4. **Safety**: Zero collisions in controlled testing
5. **Battery efficiency**: Minimizes total distance traveled

## Why Python Graph Libraries?

### Prototyping and Research

**Common Workflow**:
1. Develop algorithm in Python (NetworkX for quick testing)
2. Test in simulation (Gazebo, custom simulators)
3. Port to C++ for real robot deployment
4. Or keep Python if performance adequate (simple robots)

**When Python is Production**:
- Low-speed robots (cleaning robots, slow warehouse bots)
- Research platforms (not safety-critical)
- Prototypes and demos
- Offline path planning (pre-compute patrol routes)

### ROS Integration

**ROS 1 & ROS 2**: Python is first-class language
- Many ROS packages written in Python
- NetworkX common in ROS community for graph utilities
- But C++ preferred for performance-critical nodes

## Market Context

**Industry Demand**:
- Global mobile robotics market: $30B+ (2024)
- Motion planning engineers: High demand, $120K-$180K salaries
- Job postings commonly list "path planning algorithms" as requirement

**Common Employers**:
- Amazon Robotics (warehouse automation)
- Boston Dynamics (legged robots)
- iRobot (consumer robots)
- Waymo, Cruise (self-driving cars)
- Hundreds of startups (delivery, agriculture, inspection)

**Alternative Solutions**:
- OMPL (Open Motion Planning Library - C++)
- MoveIt (ROS motion planning framework)
- Custom implementations (very common in research)

## Representative Use Cases

### Example 1: Warehouse Robot Fleet

- **Who**: Logistics automation startup (15 engineers)
- **Need**: 100 robots navigate warehouse, avoid each other
- **Challenge**: Dynamic obstacle avoidance, multi-agent coordination
- **Solution**: A* for global planning + local DWA (dynamic window approach)
- **Library fit**: ROS nav stack (C++), NetworkX for fleet coordination logic

### Example 2: Delivery Robot

- **Who**: Autonomous delivery company (50 engineers)
- **Need**: Navigate sidewalks with pedestrians, cross streets safely
- **Challenge**: Outdoor navigation, dynamic obstacles, weather
- **Solution**: Hierarchical A* on street network + local re-planning
- **Library fit**: Custom C++ (safety-critical), Python for route optimization

### Example 3: Robot Arm Pick-and-Place

- **Who**: Manufacturing robotics integrator (10 engineers)
- **Need**: Plan collision-free paths for 6-DOF arm
- **Challenge**: High-dimensional configuration space
- **Solution**: Sampling-based planning (RRT*) + A* for roadmap graphs
- **Library fit**: OMPL (C++), NetworkX for offline path library generation

### Example 4: Research Robot

- **Who**: University robotics lab (5 graduate students)
- **Need**: Test new planning algorithms, publish papers
- **Challenge**: Rapid prototyping, algorithm comparison
- **Solution**: Implement variants of A* with different heuristics
- **Library fit**: NetworkX for algorithm development, visualization

## Unique Robotics Constraints

### Physical Consequences of Bugs

**Unlike Software**: Pathfinding bugs can:
- Damage robot hardware (collision with wall)
- Injure people (robot moves unexpectedly)
- Cost money (robot gets stuck, needs manual rescue)

**Implication**: Correctness and testing more critical than pure performance

### Energy Efficiency

**Battery Life Critical**:
- Longer paths = more energy = shorter operational time
- Optimal paths = fewer charges needed
- Sub-optimal planning has real operational cost

### Real-Time Constraints

**Must Meet Deadlines**:
- Miss planning deadline → robot stops moving (bad)
- Anytime algorithms valuable (return best-so-far if time runs out)

## Key Takeaway

**Robotics engineers need A* for robot motion planning in physical space.** Python libraries (NetworkX, rustworkx) are valuable for **algorithm prototyping and research**, but production robots often use C++ for safety-critical real-time planning (OMPL, custom implementations). Python shines in **offline planning** (fleet coordination, route optimization) and **ROS integration scripts** where performance is less critical.
