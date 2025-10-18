# Ciw: Queueing Network Simulation

## Key Research Discovery

**Ciw is specialized for queueing networks**, not general-purpose DES. It excels at queue-server systems but is not designed for arbitrary process flows.

## Overview

- **Repository**: https://github.com/CiwPython/Ciw
- **PyPI**: https://pypi.org/project/Ciw/
- **Latest version**: 3.1.4 (October 2025)
- **License**: MIT
- **GitHub stars**: 128
- **First release**: ~2017
- **Python support**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Documentation**: https://ciw.readthedocs.io/

## What is a Queueing Network?

A system of interconnected queues where entities (customers, jobs, packets) arrive, wait for service, get served, and potentially move to another queue or exit.

**Examples**:
- Call center with routing (sales queue → support queue → exit)
- Multi-stage service (security → check-in → boarding gate)
- Network traffic (router A → router B → router C)

## When to Use Ciw

**Appropriate use cases**:
- Queueing theory applications (M/M/c, G/G/k, etc.)
- Call centers with routing
- Service systems with multiple stages
- Network traffic simulation
- Any system primarily modeled as queues and servers

**NOT appropriate for**:
- Complex process flows beyond queue-server patterns
- Manufacturing with arbitrary routing/rework
- Systems where queueing is incidental, not central

**Rule of thumb**: If you can draw your system as "arrivals → queue → server → departures" (possibly networked), use Ciw. Otherwise, use SimPy or salabim.

## Installation

```bash
pip install ciw
```

## Minimal Example: M/M/3 Queue

```python
import ciw

# Define network (arrivals, service, 3 servers)
network = ciw.create_network(
    arrival_distributions=[ciw.dists.Exponential(rate=0.2)],
    service_distributions=[ciw.dists.Exponential(rate=0.1)],
    number_of_servers=[3]
)

# Run simulation
sim = ciw.Simulation(network)
sim.simulate_until_max_time(100)

# Get results
records = sim.get_all_records()

# Analyze
import pandas as pd
df = pd.DataFrame(records)
df['wait_time'] = df['service_start_date'] - df['arrival_date']
print(f"Average wait: {df['wait_time'].mean():.2f}")
```

## Strengths (Evidence-Based)

1. **Queueing-specific abstractions**: Clean API for queue-server systems
2. **Queueing theory validation**: Easy to validate against analytical models (M/M/1, M/M/c, etc.)
3. **Network support**: Multi-node queueing networks with routing
4. **Distribution library**: Built-in probability distributions
5. **Multiple customer classes**: Priority, different service requirements
6. **Type I blocking**: Queue capacity limits
7. **Academic quality**: Research-backed, published paper

## Limitations (Research Findings)

1. **Specialized scope**: Not general-purpose DES (limited to queueing paradigm)
2. **Less flexible**: Harder to model non-queue processes (manufacturing rework, complex routing)
3. **Smaller community**: 128 GitHub stars vs 3,100 (Mesa) or larger SimPy ecosystem
4. **No built-in animation**: Like SimPy, requires matplotlib integration

## API Features

### Network Definition
```python
network = ciw.create_network(
    arrival_distributions=[
        ciw.dists.Exponential(rate=5),  # Node 1 arrivals
        ciw.dists.NoArrivals()  # Node 2 (no external arrivals)
    ],
    service_distributions=[
        ciw.dists.Uniform(low=0.5, high=1.5),  # Node 1 service
        ciw.dists.Deterministic(value=0.8)  # Node 2 service
    ],
    number_of_servers=[2, 1],  # 2 servers at Node 1, 1 at Node 2
    routing=[
        [0.0, 0.7],  # 70% from Node 1 → Node 2, 30% exit
        [0.0, 0.0]   # Node 2 → exit
    ]
)
```

### Customer Classes
```python
network = ciw.create_network(
    arrival_distributions={
        'Class A': [ciw.dists.Exponential(rate=3)],
        'Class B': [ciw.dists.Exponential(rate=2)]
    },
    service_distributions={
        'Class A': [ciw.dists.Exponential(rate=5)],
        'Class B': [ciw.dists.Exponential(rate=4)]
    },
    number_of_servers=[1],
    priority_classes={'Class A': 0, 'Class B': 1}  # A has priority
)
```

## Use Case: When Ciw Shines

**Problem**: Call center with 3 queues (Sales, Support, Billing). Calls arrive, get routed based on need, some calls transfer between queues.

**Ciw solution**: Define 3-node network with routing matrix.

**Why Ciw over SimPy**:
- Ciw's queueing abstractions are cleaner than building equivalent in SimPy
- Built-in routing, customer classes, priority handling
- Designed for exactly this use case

**When you'd still use SimPy**:
- If process logic is complex (non-standard routing, conditional flows)
- If queueing is small part of larger simulation

## Performance

No comprehensive benchmarks found, but Ciw is built for efficiency in queueing simulations. Smaller scope than SimPy means potentially better performance for queueing-specific problems.

## Learning Resources

- **Official docs**: https://ciw.readthedocs.io/
- **Tutorial series**: Covers basic queue, network, routing, priorities
- **Example notebooks**: https://github.com/CiwPython/Ciw-notebooks

## Community and Maintenance

- **GitHub activity**: Active development, responsive maintainers
- **Community size**: Smaller than SimPy/Mesa, but academic backing
- **Academic focus**: Published research, used in academic settings

## Decision Guidance

**Choose Ciw if**:
- Your system is primarily queueing networks
- You want clean queueing abstractions
- You need to validate against queueing theory (M/M/c, etc.)
- You're modeling call centers, service systems, network traffic

**Choose SimPy/salabim instead if**:
- Your system has complex non-queue logic
- Queueing is part of a larger process
- You need general-purpose DES flexibility

## Summary

Ciw is the **best choice for queueing network simulations** in Python. It provides clean abstractions specifically for queues, servers, and routing. However, it's **not a general-purpose DES library**—use SimPy or salabim for broader applications.

**Analogy**: Ciw is like a specialized tool (torque wrench for queueing). SimPy is like an adjustable wrench (general-purpose). Choose based on your problem.

See S2-comprehensive/modeling-paradigms.md for queueing vs general DES comparison and S3-need-driven/decision-framework.md for selection criteria.
