# Use Case: Logistics and Operations Research

## Who Needs This

**Primary Persona**: Operations researchers and logistics engineers optimizing transportation and routing

**Specific Roles**:
- Route optimization engineers (delivery routing, fleet management)
- Supply chain analysts (network optimization, facility location)
- Transportation planners (public transit, airlines)
- Operations researchers (mathematical optimization problems)

**Team Context**:
- Logistics companies (UPS, FedEx, Amazon Logistics)
- Ride-sharing (Uber, Lyft - driver routing)
- Food delivery (DoorDash, Uber Eats)
- Supply chain consulting firms
- Municipal transportation departments

**Common Tools**: Python (optimization libraries), Commercial solvers (Gurobi, CPLEX), R, Excel

## Why They Need Graph Search

### Primary Problem: Find Cost-Optimal Routes

**The Challenge**:
- Plan delivery routes for fleets of vehicles
- Minimize total distance, time, or cost
- Respect constraints (vehicle capacity, time windows, road restrictions)
- Handle dynamic changes (traffic, new orders, cancellations)

**Why Dijkstra/A* Specifically**:
- **Dijkstra**: Guaranteed shortest path when destinations known
- **A***: Faster when heuristic available (straight-line distance to destination)
- **BFS/DFS**: Less common (unweighted networks rare in logistics)

**Real-World Examples**:
- Delivery driver: Visit 50 stops, minimize total drive time
- Food delivery: Get hot food from restaurant to customer fastest
- Emergency services: Ambulance routing to hospital
- Public transit: Find fastest route between two stops

### Specific Optimization Problems

**1. Shortest Path (Point-to-Point)**:
- **What**: Find fastest/cheapest route from A to B
- **Why**: Routing single vehicle, single delivery
- **Method**: Dijkstra or A* on road network graph

**2. Vehicle Routing Problem (VRP)**:
- **What**: Plan routes for multiple vehicles serving many customers
- **Why**: Optimize delivery fleet efficiency
- **Method**: Shortest path as subroutine in VRP algorithm (Dijkstra called 1000s of times)

**3. Facility Location**:
- **What**: Where to place warehouses to minimize distribution costs?
- **Why**: Strategic supply chain design
- **Method**: All-pairs shortest paths to evaluate candidate locations

**4. Network Design**:
- **What**: Which roads/routes to add/remove from network?
- **Why**: Infrastructure investment decisions
- **Method**: Shortest paths to measure network connectivity improvements

## Specific Requirements

### Scale Requirements

**Small Problems** (<1,000 nodes):
- Local delivery (small city)
- Internal factory logistics
- **Library needs**: Ease of implementation, solve quickly

**Medium Problems** (1K-100K nodes):
- Regional delivery networks
- City-scale transportation
- **Library needs**: Good performance, reasonable solve times

**Large Problems** (>100K nodes):
- National road networks (millions of road segments)
- Global supply chain networks
- **Library needs**: High performance critical, custom optimizations

### Real-World Constraints

**Time Windows**:
- Customer available 2pm-4pm only
- Restaurant pickup ready at 6:15pm
- Store closing times

**Capacity Constraints**:
- Truck carries max 5 tons
- Vehicle has 8 seats
- Delivery van fits 50 packages

**Dynamic Updates**:
- New order arrives mid-route
- Traffic accident blocks road
- Customer cancels order

### Platform Constraints

**Deployment**:
- Backend services (REST APIs for routing)
- Mobile apps (driver navigation)
- Desktop tools (planning software)
- Cloud batch jobs (nightly route optimization)

**Integration**:
- Maps APIs (Google Maps, OpenStreetMap)
- Traffic data (real-time road speeds)
- OR tools (OR-Tools, PuLP, Gurobi)

## Pain Points with Current Solutions

### Commercial Routing APIs

**Google Maps Directions API, HERE, Mapbox**:
- ✅ Easy to use, accurate, real-time traffic
- ✅ No need to maintain road network data
- ❌ Cost ($5-$40 per 1000 requests)
- ❌ Usage limits (rate limits, quotas)
- ❌ Black box (can't customize cost function)
- ❌ Vendor lock-in

### Open Source Routing

**OSRM, GraphHopper, Valhalla**:
- ✅ Free, open source
- ✅ Can host yourself (no API costs)
- ✅ Customizable routing profiles
- ❌ Must download/maintain map data
- ❌ Infrastructure overhead (servers, updates)
- ❌ Requires GIS expertise

### OR Tools + Python Graph Libraries

**Current Approach**: Many teams combine
- OR-Tools (Google's optimization library) for VRP
- NetworkX/igraph for shortest path subroutines
- Custom logic to integrate

**Pain Points**:
- Performance bottleneck (NetworkX too slow for large graphs)
- Integration complexity (different APIs, data formats)
- Debugging difficulty (errors span multiple libraries)

### What Logistics Engineers Want

**Ideal Solution**:
- Fast shortest path (milliseconds for typical queries)
- Customizable edge costs (distance, time, tolls, restrictions)
- Dynamic updates (re-route when road blocked)
- Map data integration (OSM, commercial data)
- OR solver integration (use with OR-Tools, Gurobi)

## Decision Criteria

### Must-Haves

1. **Dijkstra/A***: Core shortest path algorithms
2. **Performance**: Sub-second for large road networks
3. **Weighted graphs**: Edge costs represent time, distance, or money
4. **Dynamic updates**: Efficiently update edge weights (traffic changes)
5. **Correctness**: Wrong routes have business cost

### Nice-to-Haves

1. **Turn restrictions**: Model real road constraints
2. **Time-dependent costs**: Edge cost varies by time of day (rush hour)
3. **Multiple objectives**: Optimize time AND distance simultaneously
4. **Map matching**: Snap GPS traces to road network
5. **Isochrones**: Find all locations reachable within X minutes

### Deal-Breakers

- ❌ No Dijkstra/A* (BFS insufficient for weighted networks)
- ❌ Too slow (can't meet latency SLAs for APIs)
- ❌ No dynamic updates (can't handle traffic)
- ❌ License issues (GPL problematic for commercial routing services)

## Success Metrics

**How They Measure Success**:
1. **Cost savings**: % reduction in total distance/time/fuel
2. **Service level**: % of deliveries on-time
3. **Solve time**: Optimization completes in reasonable time (minutes to hours)
4. **API latency**: Routing API responds in <200ms
5. **ROI**: Savings > cost of optimization system

## Why Python Graph Libraries?

### Prototyping and Research

**Common Workflow**:
1. Prototype VRP algorithm with NetworkX (fast development)
2. Test on small instances (prove correctness)
3. Port to faster library (rustworkx, graph-tool) or C++
4. Production system uses custom C++/Rust or commercial solver

### Mid-Scale Production

**When Python is Production**:
- Internal tools (planning software for human operators)
- Non-latency-critical batch jobs (overnight route optimization)
- Data analysis (evaluate network performance)

**Library Choice**:
- **rustworkx**: Good balance (fast enough, permissive license)
- **igraph**: Also good (performance + cross-platform)
- **NetworkX**: Too slow for large-scale production

### Integration Layer

**Graph Library + OR Solver**:
- OR-Tools for VRP optimization
- Graph library for shortest path queries within VRP
- Python as glue code

## Market Context

**Industry Size**:
- Last-mile delivery: $100B+ market
- Route optimization software: $10B+ market
- High-value use case (1% efficiency = millions in savings)

**Job Demand**:
- Operations research roles: $90K-$160K
- "Routing algorithms" common requirement
- Logistics tech companies hiring aggressively

**Alternative Solutions**:
- Commercial: Routific, Onfleet, OptimoRoute ($100-$1000/month)
- Open source: OR-Tools, OSRM, GraphHopper
- Custom: Many large companies build in-house (Amazon, Uber)

## Representative Use Cases

### Example 1: Food Delivery Routing

- **Who**: Engineering team at food delivery startup (30 engineers)
- **Need**: Route drivers to pick up orders, deliver to customers
- **Challenge**: Real-time (orders arrive continuously), minimize delivery time
- **Solution**: A* for single routes, heuristics for driver assignment
- **Library fit**: rustworkx (fast A*, production-ready)

### Example 2: Warehouse Delivery Fleet

- **Who**: Logistics company (5,000 drivers, 200 engineers)
- **Need**: Plan next-day delivery routes for 500 trucks
- **Challenge**: 50,000 deliveries/day, 2-hour time windows
- **Solution**: OR-Tools VRP solver + shortest path subroutines
- **Library fit**: graph-tool (called millions of times, performance critical)

### Example 3: Public Transit Trip Planning

- **Who**: Municipal transportation agency (20 IT staff)
- **Need**: Provide trip planning on website/app
- **Challenge**: Multi-modal (bus, subway, walking), schedules, real-time delays
- **Solution**: Time-expanded graph + Dijkstra
- **Library fit**: Custom C++ (performance), NetworkX (analysis/prototyping)

### Example 4: Supply Chain Network Design

- **Who**: Consulting firm OR team (10 consultants)
- **Need**: Advise client on warehouse locations
- **Challenge**: Evaluate 100s of location combinations, minimize costs
- **Solution**: All-pairs shortest paths on transportation network
- **Library fit**: NetworkX (client work, emphasis on clear code)

## Unique Logistics Constraints

### Business Impact of Performance

**Every Millisecond Counts**:
- Faster routing = more deliveries per hour
- 10% faster algorithm = $1M+ annual savings (at scale)
- Performance is directly tied to revenue

**Implication**: Willingness to invest in performance (C++, custom hardware)

### Real-World Complexity

**Academic vs Industry**:
- Textbooks: Clean graphs, perfect data
- Reality: Missing data, GPS errors, constantly changing

**Need**: Robust algorithms, error handling, practical heuristics

### Regulatory Constraints

**Must Follow Rules**:
- Truck routing (avoid low bridges, weight limits)
- Hazmat restrictions (special routes for dangerous goods)
- Driver hours (can't drive >11 hours/day)

## Why A* vs Dijkstra?

**When A* Wins**:
- Point-to-point routing (known destination)
- Geographic networks (Euclidean heuristic available)
- Latency-critical (API responses)

**When Dijkstra Used**:
- One-to-many (single depot to all customers)
- Need exact shortest paths to many destinations
- Heuristic not available

## Key Takeaway

**Logistics engineers need Dijkstra and A* for route optimization and network analysis.** Python libraries serve two roles: **(1) Prototyping** VRP algorithms and testing ideas (NetworkX), **(2) Production** for mid-scale problems where Python performance is sufficient (rustworkx, igraph). For very large-scale systems (Uber, Amazon), teams eventually build **custom C++/Rust** routing engines, but Python libraries remain valuable for **analysis, tooling, and integration** with OR solvers.
