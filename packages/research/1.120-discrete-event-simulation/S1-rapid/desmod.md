# desmod: Component-Based DES Framework

## Key Research Discovery

**desmod is built on top of SimPy** and adds component-based architecture for large-scale, modular simulations. It's corporately-backed by Western Digital.

## Overview

- **Repository**: https://github.com/westerndigitalcorporation/desmod
- **PyPI**: https://pypi.org/project/desmod/
- **Latest version**: Stable (check PyPI for current)
- **License**: MIT
- **GitHub stars**: <100
- **Corporate backing**: Western Digital Corporation
- **First release**: ~2016
- **Documentation**: https://desmod.readthedocs.io/

## What is Component-Based DES?

Instead of flat processes, desmod organizes simulations into a **hierarchy of components** (Directed Acyclic Graph structure). Each component can:
- Contain child components
- Have processes (SimPy-style)
- Connect to other components
- Encapsulate behavior

**Analogy**: Object-oriented programming for simulations. Components are classes that compose into larger systems.

## When to Use desmod

**Appropriate use cases**:
- Large-scale industrial simulations (manufacturing plants, data centers)
- Modular systems where reusable components matter
- Complex hierarchies (subsystems within systems)
- Systems with many similar components (100s of machines, servers, etc.)

**NOT appropriate for**:
- Small/simple simulations (overhead not worth it)
- Quick prototypes (use SimPy directly)
- Standard queueing systems (use Ciw or SimPy)

**Rule of thumb**: If your simulation has >5-10 distinct subsystems that could be reused, consider desmod. Otherwise, use SimPy.

## Installation

```bash
pip install desmod
```

(desmod installs SimPy as a dependency)

## Minimal Example: Component Hierarchy

```python
from desmod.component import Component
from desmod.simulation import simulate

class Machine(Component):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_process(self.run)
    
    def run(self, env):
        while True:
            print(f"{self.name} processing at {env.now}")
            yield env.timeout(10)  # Processing time

class Factory(Component):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create child components
        self.add_connections('machine1', 'machine2')
        self.machine1 = Machine(self, 'machine1')
        self.machine2 = Machine(self, 'machine2')

# Simulate
config = {
    'sim.duration': 100,
    'sim.log.level': 'INFO'
}
simulate(Factory, config)
```

## Component Lifecycle (Research Finding)

desmod simulations have **three phases**:

### 1. Initialization
`__init__()` methods called, components created.

### 2. Elaboration
Inter-component connections established, processes started.

### 3. Simulation
Discrete event simulation occurs (SimPy engine).

**Why this matters**: Forces clean separation of setup vs runtime, improving large-model maintainability.

## Strengths (Evidence-Based)

1. **Modularity**: Component hierarchy for reusable, composable parts
2. **Scalability**: Designed for large industrial models (corporate use case)
3. **SimPy compatibility**: Builds on proven SimPy foundation
4. **Configuration management**: Built-in config system for parameter sweeps
5. **Simulation monitoring**: Hooks for instrumentation and debugging
6. **Corporate backing**: Western Digital use indicates production-quality

## Limitations (Research Findings)

1. **Smaller community**: <100 GitHub stars, limited ecosystem
2. **Higher learning curve**: Requires SimPy knowledge + component concepts
3. **Overhead for simple models**: Not worth complexity for small simulations
4. **Less documentation**: Good technical docs, but fewer tutorials than SimPy

## When to Choose desmod

**Best for**:
- Large-scale industrial simulations (data centers, factories, supply chains)
- Modular systems with reusable components
- Projects where simulation architecture matters long-term

**Choose SimPy directly if**:
- Small/medium simulations
- Prototyping or one-off analyses
- Flat process structure is sufficient

**Choose salabim instead if**:
- You want built-in stats/animation (desmod inherits SimPy's limitations)

## Learning Resources

- **Official docs**: https://desmod.readthedocs.io/
- **Examples**: Corporate use cases (storage systems, hardware modeling)
- **SimPy knowledge**: Required prerequisite

## Research Gap

No comprehensive benchmarks comparing desmod overhead vs raw SimPy. Corporate backing suggests performance is acceptable for industrial use, but quantitative data is missing.

## Decision Guidance

**Choose desmod if**:
- You're building large-scale simulations that will be maintained/extended over time
- Component reusability is important (simulate 1000 similar machines)
- You need hierarchical organization (factory → production lines → machines)

**Choose SimPy instead if**:
- Simpler, flatter model structure
- You don't need component abstraction
- Smaller team / shorter project timeline

## Summary

desmod is a **specialized framework for large, component-based simulations**. It's built on SimPy, so you get SimPy's maturity plus component architecture. However, it's overkill for small projects.

**Analogy**: desmod is to SimPy as Django is to Flask. More structure, better for large projects, but heavier for simple use cases.

**Corporate validation**: Western Digital's backing indicates production-quality for industrial simulations.

See S3-need-driven/integration-patterns.md for component-based architecture patterns and S4-strategic/academic-vs-industrial.md for corporate vs academic library comparison.
