# Mesa: Agent-Based Modeling Framework

## Critical Discovery

**Mesa is NOT a general-purpose discrete event simulation library**. It is specialized for **agent-based modeling (ABM)**, which is a different paradigm from process-based DES.

## Overview

- **Repository**: https://github.com/projectmesa/mesa
- **PyPI**: https://pypi.org/project/Mesa/
- **Latest version**: 3.x (major release 2024-2025)
- **License**: Apache-2.0
- **GitHub stars**: 3,100 (October 2025)
- **First release**: ~2015
- **Python support**: 3.9+
- **JOSS paper**: "Mesa 3: Agent-based modeling with Python in 2025" (published 2025)

## Agent-Based Modeling vs Discrete Event Simulation

| Aspect | Agent-Based Modeling (Mesa) | Process-Based DES (SimPy) |
|--------|----------------------------|---------------------------|
| **Entities** | Autonomous agents with behaviors | Passive entities following processes |
| **Environment** | Explicit spatial grid or network | Implicit (queues, resources) |
| **Decision-making** | Agents make decisions based on local state | Centrally orchestrated processes |
| **Emergence** | System behavior emerges from interactions | System behavior designed explicitly |
| **Use cases** | Social systems, ecology, markets | Operational systems, queueing, manufacturing |

## When to Use Mesa

**Appropriate use cases**:
- Social dynamics (opinion spread, segregation, cooperation)
- Ecological models (predator-prey, population dynamics)
- Market simulations (trader behavior, price formation)
- Spatial phenomena (geographic spread, territory)
- Complex adaptive systems (emergent behaviors)

**NOT appropriate for**:
- Traditional queueing systems (use SimPy, Ciw, salabim)
- Manufacturing process flow (use SimPy, desmod)
- Service operations (use SimPy, Ciw)
- Resource allocation without spatial/behavioral component (use SimPy)

## Installation

```bash
pip install mesa
```

## Minimal Example: Schelling Segregation Model

```python
import mesa

class Agent(mesa.Agent):
    def __init__(self, unique_id, model, agent_type):
        super().__init__(unique_id, model)
        self.type = agent_type
    
    def step(self):
        # Agent behavior: move if unhappy with neighbors
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False
        )
        if len(neighbors) > 0:
            similar = sum(1 for n in neighbors if n.type == self.type)
            if similar / len(neighbors) < 0.3:  # Unhappy threshold
                self.model.grid.move_to_empty(self)

class SegregationModel(mesa.Model):
    def __init__(self, width, height, density, minority_fraction):
        super().__init__()
        self.grid = mesa.space.SingleGrid(width, height, torus=True)
        self.schedule = mesa.time.RandomActivation(self)
        
        # Create agents
        for (x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                agent_type = 0 if self.random.random() < minority_fraction else 1
                agent = Agent(self.next_id(), self, agent_type)
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)
    
    def step(self):
        self.schedule.step()

# Run model
model = SegregationModel(width=20, height=20, density=0.8, minority_fraction=0.5)
for _ in range(100):
    model.step()
```

## Strengths (Research Findings)

1. **Purpose-built for ABM**: Spatial grids, network topologies, agent scheduling
2. **Built-in visualization**: Grid visualizer, charts, interactive server
3. **Academic backing**: JOSS publication, Google Summer of Code participation
4. **Active development**: Version 3.x released 2024-2025
5. **Example models**: Extensive repository of classic ABM models (Schelling, Wolf-Sheep, etc.)

## Limitations

1. **Not general DES**: Designed for agent-based models, not process-based simulation
2. **Performance with large agent counts**: Mesa-frames developed (2024) to address scalability
3. **Different paradigm**: Learning curve if expecting traditional DES

## Performance Note (Research Finding)

Mesa-frames was created in 2024 as a Google Summer of Code project specifically to address Mesa's performance limitations with large numbers of agents. This indicates that vanilla Mesa may struggle with very large-scale models.

## Community and Maintenance

- **GitHub stars**: 3,100 (among highest for Python simulation libraries)
- **Community**: Academic focus, active development
- **Long-term viability**: Strong institutional backing, GSoC participation

## Learning Resources

- **Official docs**: https://mesa.readthedocs.io/
- **Example models**: https://github.com/projectmesa/mesa-examples
- **JOSS paper**: Published in Journal of Open Source Software (2025)

## Decision Guidance

**Choose Mesa if**:
- You need agent-based modeling (autonomous agents, spatial environments)
- Your system exhibits emergent behavior from local interactions
- You're modeling social, ecological, or market systems

**Choose SimPy/Ciw/salabim instead if**:
- You need traditional DES (queueing, process flow, resource allocation)
- Your entities are passive (don't make autonomous decisions)
- You're modeling operational systems (manufacturing, logistics, service)

## Summary

Mesa is excellent for its intended purpose (agent-based modeling) but is **not a general-purpose DES library**. Don't choose Mesa for traditional queueing or process-flow simulations—use SimPy, salabim, or Ciw instead.

See S3-need-driven/use-cases.md for detailed comparison of ABM vs DES paradigms.
