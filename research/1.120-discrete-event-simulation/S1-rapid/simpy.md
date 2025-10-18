# SimPy: Process-Based Discrete Event Simulation

## Overview

**SimPy** is the most widely-used discrete event simulation framework for Python. It uses process-based modeling where Python generator functions represent entity lifecycles.

- **Repository**: https://gitlab.com/team-simpy/simpy (official), GitHub mirrors exist
- **PyPI**: https://pypi.org/project/simpy/
- **Latest version**: 4.1.1 (as of October 2025)
- **License**: MIT  
- **First release**: 2002 (20+ years of development)
- **Python support**: 3.8+
- **Documentation**: https://simpy.readthedocs.io/

## Key Discovery from Research

SimPy is officially hosted on **GitLab**, not GitHub. This means GitHub stars are not the primary community metric—focus instead on PyPI downloads, documentation quality, and Google Group activity.

## Installation

```bash
pip install simpy
```

## Minimal Example: Single Queue Single Server

```python
import simpy
import random

def customer(env, name, server):
    arrival = env.now
    print(f"{name} arrives at {arrival:.1f}")
    
    with server.request() as req:
        yield req  # Wait for server
        wait = env.now - arrival
        print(f"{name} waited {wait:.1f}, starts service at {env.now:.1f}")
        
        yield env.timeout(random.expovariate(0.25))  # Service time
    
    print(f"{name} departs at {env.now:.1f}")

# Setup
env = simpy.Environment()
server = simpy.Resource(env, capacity=1)

# Create 5 customers
for i in range(5):
    env.process(customer(env, f"Customer{i+1}", server))

env.run()
```

## Strengths (Evidence-Based)

1. **Most mature**: 20+ years of development (since 2002)
2. **Best documentation**: Tutorial, guides, examples, API reference on ReadTheDocs
3. **Largest community**: Active Google Group, extensive Stack Overflow presence
4. **Lightweight**: Minimal dependencies
5. **Real-time capable**: `simpy.rt.RealtimeEnvironment` for wall-clock sync
6. **MIT license**: Permissive for commercial use

## Limitations (Research Findings)

1. **Yield statement required**: Moderate learning curve for Python beginners
2. **No built-in statistics**: Manual data collection (use pandas)
3. **No built-in visualization**: Integrate matplotlib manually
4. **No animation**: Unlike salabim

## When to Choose SimPy

**Best for**:
- General-purpose DES (80% of use cases)
- Production systems (mature, stable)
- Teams familiar with Python generators

**Consider alternatives if**:
- You want built-in stats/animation → salabim
- You're modeling queueing networks specifically → Ciw
- You need agent-based modeling → Mesa

## Learning Time

**Research finding**: Official docs claim "learn basics in ~10 minutes." Realistic estimate: 2-4 hours to first working model for developers comfortable with Python.

See S2-comprehensive/performance-comparison.md for benchmarks and S3-need-driven/decision-framework.md for selection criteria.
