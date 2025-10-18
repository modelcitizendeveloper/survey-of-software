# Discrete Event Simulation: Technical Overview

## What is Discrete Event Simulation?

Discrete Event Simulation (DES) models systems where state changes occur at specific points in time (events), not continuously. Unlike differential equation models that track continuous change, DES jumps from event to event.

**Example**: A queueing system has discrete events:
- t=10: Customer arrives
- t=15: Service starts (server was busy 10-15, customer waited)
- t=22: Service completes, customer departs
- t=23: Next customer starts service

The simulation clock jumps 10’15’22’23, not incrementing second-by-second.

## Core DES Concepts

### Entities
Objects that flow through the system and experience events.
- Examples: Customers, vehicles, packets, parts, jobs, patients
- Properties: Arrival time, priority, type, attributes (size, value, urgency)

### Resources
Constrained assets that entities compete for and occupy during processing.
- Examples: Servers, machines, staff, beds, loading docks, network bandwidth
- Capacity: Number of concurrent entities a resource can serve (single server, 3 servers, unlimited)
- State: Idle, busy, broken, blocked

### Events
Points in time when system state changes.
- Examples: Arrival, service start, service complete, departure, breakdown, repair
- Characteristics: Event time (when), event type (what), associated entities (who)

### Queues
Waiting areas where entities wait when resources are unavailable.
- Discipline: FIFO (first-in first-out), LIFO (stack), priority-based
- Characteristics: Length (current count), max length observed, time-average length
- Blocking: Finite capacity (queue fills up, arrivals rejected/balked)

### Processes
Sequences of steps entities follow, often involving resource acquisition and release.
- Example: Arrive ’ Wait in queue ’ Acquire server ’ Get served ’ Release server ’ Depart

## Simulation Paradigms

Three primary approaches exist for building DES models, each with trade-offs:

### 1. Event-Based (Event Scheduling)

**Mechanism**: Explicitly schedule events and process them in chronological order using an event list (priority queue).

**How it works**:
```
Event List (sorted by time):
  t=10: Customer 1 arrives
  t=15: Customer 1 starts service
  t=22: Customer 1 completes service
  t=23: Customer 2 arrives

Process loop:
  1. Pop next event from list
  2. Advance simulation clock to event time
  3. Execute event logic (update state, schedule new events)
  4. Repeat until event list empty or stop condition
```

**Advantages**:
- Fast execution (minimal overhead)
- Full control over event processing
- Efficient for performance-critical simulations

**Disadvantages**:
- Low-level programming (manually manage state, schedule events)
- Code can become complex for multi-step processes
- Harder to read/maintain than process-based code

**When to use**:
- Performance-critical simulations (>millions of events)
- Simple systems where event logic is straightforward
- When you need fine-grained control over scheduling

**Python libraries**: All DES libraries support event-based, but it's typically not the primary API.

### 2. Process-Based

**Mechanism**: Model entities as processes (functions/coroutines) that describe their lifecycle. Processes yield control when waiting for resources or time to pass.

**How it works** (SimPy example conceptually):
```python
def customer_process(env, server):
    arrival_time = env.now
    print(f"Customer arrives at {arrival_time}")

    # Request resource (yields if busy)
    with server.request() as req:
        yield req  # Wait until server available

        print(f"Customer starts service at {env.now}")
        yield env.timeout(service_time)  # Wait for service to complete

    print(f"Customer departs at {env.now}")
```

**Key insight**: The `yield` statement suspends the process. The simulation engine handles scheduling and resumption automatically.

**Advantages**:
- Intuitive code structure (reads like a process description)
- Easy to model multi-step processes
- Natural representation of blocking (waiting for resources)
- Reduced boilerplate compared to event-based

**Disadvantages**:
- Requires understanding generators (Python) or coroutines
- Slight performance overhead vs pure event-based
- Debugging can be tricky (suspended processes)

**When to use**:
- Most DES applications (80% of use cases)
- Systems with entities that have complex lifecycles
- When code readability matters

**Python libraries**: SimPy (generators), salabim (greenlets or yieldless), desmod (builds on SimPy)

### 3. Activity-Based

**Mechanism**: Focus on activities (time-consuming operations) rather than entities or events. Less common in modern DES.

**Characteristics**:
- Model defines activities and their preconditions
- Scheduler checks which activities can start at each time step
- More declarative than process-based

**Python libraries**: Rare in Python ecosystem; mostly historical (SLAM, GPSS).

### 4. Agent-Based (ABM)

**Mechanism**: Model autonomous agents with behaviors, interacting in an environment. Technically distinct from classical DES, but often grouped together.

**How it differs from process-based DES**:
- **Agents** have internal state, decision rules, and behaviors (not just passive entities)
- **Environment** is explicit (spatial grids, networks, continuous space)
- **Interactions** are peer-to-peer (agents sense and respond to each other)
- **Emergence**: System behavior emerges from agent interactions (not centrally orchestrated)

**Example**: Epidemic model
- Agents: People moving on a grid
- Behaviors: Move randomly, interact with neighbors, infect/recover
- Environment: Grid representing geographic space
- Emergence: Infection spread patterns emerge from local interactions

**When to use ABM vs DES**:
- **Use ABM**: Social systems, ecology, markets, spatial phenomena, decentralized decision-making
- **Use DES**: Operational systems, queueing, resource allocation, centralized processes

**Python libraries**: Mesa (dedicated ABM framework)

## Time Advancement Mechanisms

### Next-Event Time Advancement (Standard DES)
- Jump directly to the next scheduled event
- No wasted computation between events
- Used by SimPy, salabim, Ciw, desmod

### Fixed-Increment Time Advancement
- Advance clock in fixed steps (e.g., ”t = 0.1 seconds)
- At each step, check if any events occur
- Inefficient for sparse events, but simple to implement
- Rarely used in modern DES (more common in system dynamics)

### Real-Time Synchronization
- Sync simulation clock with wall-clock time
- Useful for interactive demonstrations, hardware-in-the-loop, real-time visualization
- Supported by SimPy (`simpy.rt.RealtimeEnvironment`) and salabim

**Example**: If simulation time unit = 1 second and real-time factor = 1.0, advancing simulation by 10 seconds takes 10 wall-clock seconds. Setting factor = 0.1 runs simulation 10x faster than real-time.

## Key DES Terminology

| Term | Definition | Example |
|------|------------|---------|
| **Arrival process** | Pattern of entity arrivals over time | Poisson arrivals (random), scheduled (every 5 min), batch (groups of 10) |
| **Service time** | Duration of processing | Exponential (memoryless), normal, deterministic (constant) |
| **Utilization (Á)** | Fraction of time resource is busy | Á = » / (c × ¼), where »=arrival rate, ¼=service rate, c=# servers |
| **Throughput** | Entities processed per time unit | 100 customers/hour, 50 parts/day |
| **Cycle time** | Total time entity spends in system | Arrival to departure (wait time + service time) |
| **Little's Law** | L = » × W | Average entities in system (L) = arrival rate (») × avg time in system (W) |
| **Warm-up period** | Initial time discarded from statistics | System starts empty; not representative of steady-state behavior |
| **Replication** | Running simulation multiple times | Account for randomness; report mean ± confidence interval |

## Common Probability Distributions in DES

### Arrival Processes
- **Poisson process**: Random arrivals, memoryless. Inter-arrival times follow exponential distribution.
  - Used when arrivals are independent (customers, phone calls)
- **Scheduled**: Deterministic arrivals (bus schedule, appointment system)
- **Time-dependent**: Arrival rate varies over time (rush hour, seasonal patterns)

### Service Times
- **Exponential**: Memoryless (constant hazard rate). Common in theoretical models (M/M/1 queue).
- **Normal/Lognormal**: Symmetric or right-skewed. Use when service times cluster around a mean with variation.
- **Uniform**: Every duration equally likely in range [a, b].
- **Empirical**: Fit distribution to real data (histogram, kernel density estimation).

### Resource Failures
- **Exponential** (time to failure) and **Exponential** (time to repair): Classic reliability model.
- **Weibull**: Captures increasing/decreasing failure rate (wear-out vs infant mortality).

## Generic DES Example: Single Queue, Single Server

**System**: Entities arrive, wait in queue if server busy, get served, depart.

**Components**:
- **Entities**: Arrivals (inter-arrival time ~ Exponential(»=0.2 entities/time unit))
- **Resource**: Server (capacity=1)
- **Queue**: FIFO, unlimited capacity
- **Service time**: ~ Exponential(¼=0.25 time units)

**Process**:
1. Entity arrives at time t
2. If server idle ’ start service immediately
3. If server busy ’ join queue
4. When service completes ’ next entity in queue starts service
5. Entity departs

**Metrics to collect**:
- Average wait time (time in queue)
- Average cycle time (time in system)
- Server utilization (fraction of time busy)
- Time-average queue length

**Queueing theory check** (M/M/1 queue):
- Á = »/¼ = 0.2/0.25 = 0.8 (stable, < 1)
- Expected wait time (W_q) = Á / (¼ - ») = 0.8 / (0.25 - 0.2) = 16 time units
- Expected queue length (L_q) = » × W_q = 0.2 × 16 = 3.2 entities

Run simulation to verify these theoretical predictions or handle cases where theory doesn't apply (multiple servers, priority queues, breakdowns).

## Why Simulation vs Analytical Models?

| Approach | When to Use | Example |
|----------|-------------|---------|
| **Analytical (queueing theory)** | Simple systems with known formulas | M/M/1, M/M/c (exponential arrivals and service, c servers) |
| **Simulation** | Complex systems where formulas don't exist | Priority queues, breakdowns, rework loops, network of queues, non-exponential distributions |

**Simulation advantages**:
- Handles arbitrary complexity (breakdowns, rework, batching, priorities)
- Supports any probability distribution (empirical data)
- Provides visual output (animations, charts)

**Analytical advantages**:
- Instant results (no simulation runtime)
- Exact solutions (no statistical uncertainty)
- Insight into system behavior (sensitivity via calculus)

**Pragmatic approach**: Use analytical models for validation (if simple case exists) and simulation for realistic complexity.

## Data Collection and Analysis

### Metrics to Track
- **Time-average**: Average queue length, average utilization (measured over time)
- **Entity-average**: Average wait time, average cycle time (measured per entity)
- **Extremes**: Max queue length, max wait time, 95th percentile
- **Time-series**: Queue length at each time step (for plots)

### Warm-Up Period
- **Problem**: Simulation starts with empty system (not realistic steady-state)
- **Solution**: Discard initial time period (e.g., first 1000 time units) from statistics
- **How to choose**: Plot metric over time, identify when it stabilizes

### Replication
- **Problem**: Single simulation run is one random outcome
- **Solution**: Run simulation N times with different random seeds (typically N=30-100)
- **Reporting**: Mean ± 95% confidence interval

**Example**: "Average wait time: 4.2 ± 0.3 minutes (95% CI, 50 replications)"

### Variance Reduction
- **Common random numbers**: Use same random stream across scenarios for fair comparison
- **Antithetic variates**: Run pairs of simulations with negatively correlated random numbers
- **Control variates**: Use known theoretical result to reduce variance

## Next Steps

This technical overview provides the conceptual foundation for DES. For specific Python libraries:
- **SimPy**: S1-rapid/simpy.md (process-based, most mature)
- **Mesa**: S1-rapid/mesa.md (agent-based modeling)
- **salabim**: S1-rapid/salabim.md (yieldless API, built-in animation)
- **Ciw**: S1-rapid/ciw.md (queueing networks specialist)
- **desmod**: S1-rapid/desmod.md (component-based, builds on SimPy)

For comprehensive analysis:
- **Performance**: S2-comprehensive/performance-comparison.md
- **Paradigms**: S2-comprehensive/modeling-paradigms.md
- **Real-time**: S2-comprehensive/real-time-vs-batch.md
- **Statistics**: S2-comprehensive/statistics-collection.md
- **Visualization**: S2-comprehensive/visualization-integration.md
