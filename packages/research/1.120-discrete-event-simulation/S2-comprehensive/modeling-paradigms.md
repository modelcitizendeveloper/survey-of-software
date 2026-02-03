# Modeling Paradigms: Deep Dive

## Four Distinct Paradigms Identified

### 1. Process-Based (Generator Functions)
**Libraries**: SimPy, desmod

**Mechanism**: Python generators with `yield` statements represent processes.

**Example**:
```python
def customer(env, server):
    with server.request() as req:
        yield req  # Suspend until resource available
        yield env.timeout(service_time)  # Suspend during service
```

**Pros**: Intuitive lifecycle representation, natural blocking semantics
**Cons**: Requires understanding Python generators

---

### 2. Process-Based (Yieldless/Greenlets)
**Libraries**: salabim

**Mechanism**: Greenlet coroutines, NO `yield` required.

**Example**:
```python
class Customer(sim.Component):
    def process(self):
        self.request(server)  # No yield!
        self.hold(service_time)  # No yield!
```

**Pros**: Easier for Python beginners, no generator syntax
**Cons**: Dependency on greenlet library, smaller community

---

### 3. Agent-Based Modeling
**Libraries**: Mesa

**Mechanism**: Autonomous agents with behaviors in spatial environments.

**Example**:
```python
class Agent(mesa.Agent):
    def step(self):
        neighbors = self.model.grid.get_neighbors(self.pos)
        # Agent decides based on local state
        if unhappy(neighbors):
            self.model.grid.move_to_empty(self)
```

**Pros**: Natural for social systems, ecology, markets
**Cons**: NOT suitable for operational DES (queueing, manufacturing)

---

### 4. Queueing Network Structures
**Libraries**: Ciw

**Mechanism**: Specialized abstractions for queues, servers, routing.

**Example**:
```python
network = ciw.create_network(
    arrival_distributions=[ciw.dists.Exponential(0.2)],
    service_distributions=[ciw.dists.Exponential(0.25)],
    number_of_servers=[3],
    routing=[[0.7, 0.3]]  # 70% route to next node
)
```

**Pros**: Clean API for queueing problems, validation against queueing theory
**Cons**: Limited flexibility for non-queue processes

## Paradigm Selection Decision Tree

**Is your system based on autonomous agents with emergent behavior?**
→ YES: Agent-Based (Mesa)
→ NO: Continue

**Is your system primarily queue-server networks?**
→ YES: Queueing Network (Ciw)
→ NO: Continue

**Are you comfortable with Python generators?**
→ YES: Process-Based Generator (SimPy, desmod)
→ NO: Process-Based Yieldless (salabim)

## When Paradigms Don't Fit

Some systems don't cleanly fit into one paradigm:
- **Hybrid models**: Manufacturing with worker agents (combine Mesa + SimPy?)
- **Complex routing**: Beyond queue-server patterns but not fully agent-based

**Solution**: Use general-purpose library (SimPy) and implement custom logic.

## Summary

Choose paradigm based on system characteristics, not library popularity. Mesa is NOT a SimPy alternative—it's a different paradigm entirely.
