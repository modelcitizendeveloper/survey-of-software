# Generic Use Case Patterns (Application-Neutral)

## Critical: Application-Neutral Examples

This document uses GENERIC patterns (queues, resources, entities) NOT specific applications (elevators, hospitals, airports).

## Pattern 1: Single-Stage Queue System

**Abstract description**: Entities arrive, wait in queue if resource busy, get served, depart.

**Components**:
- Entities (generic arrivals)
- Single resource (server, processor, handler)
- FIFO queue
- Exponential inter-arrival and service times

**Libraries**: SimPy, salabim, Ciw (all suitable)
**Complexity**: Low
**Learning**: First tutorial for most libraries

---

## Pattern 2: Multi-Stage Process Flow

**Abstract description**: Entities move through multiple processing stages sequentially (Stage 1 → Stage 2 → Stage 3).

**Components**:
- Multiple resources (3+ stages)
- Queues between stages (buffer inventory)
- Variable routing (some entities skip stages based on type)

**Example abstraction**: Part → Machining → Quality Check → Packaging

**Libraries**: SimPy (best flexibility), desmod (if many stages), salabim
**Complexity**: Medium
**Key challenge**: Coordinating handoffs between stages

---

## Pattern 3: Resource Allocation with Priorities

**Abstract description**: Multiple entity types compete for shared resources with priority ordering.

**Components**:
- PriorityResource (high-priority entities preempt low-priority)
- Multiple entity classes (Class A, Class B, Class C)
- Priority-based queueing

**Example abstraction**: Urgent jobs vs standard jobs sharing processing capacity

**Libraries**: SimPy (PriorityResource, PreemptiveResource), salabim
**Complexity**: Medium
**Key challenge**: Modeling preemption and resumption

---

## Pattern 4: Queueing Network with Routing

**Abstract description**: Entities move through network of queues, routing probabilistically to next node.

**Components**:
- Multiple queue-server nodes
- Routing matrix (probabilities of next destination)
- Feedback loops (entities return to earlier nodes)

**Example abstraction**: Multi-departmental service flow with routing

**Libraries**: Ciw (purpose-built), SimPy (manual routing logic)
**Complexity**: Medium-High
**Key challenge**: Routing logic, cycle detection

---

## Pattern 5: Inventory/Buffer Management

**Abstract description**: Entities consume/replenish inventory, blocking when depleted or full.

**Components**:
- Store or Container resource
- Producer processes (add inventory)
- Consumer processes (remove inventory)
- Reorder policies

**Example abstraction**: Warehouse with incoming shipments and outgoing orders

**Libraries**: SimPy (Store, Container), salabim
**Complexity**: Medium
**Key challenge**: Reorder logic, stockout handling

---

## Pattern 6: Resource Breakdowns and Repairs

**Abstract description**: Resources fail randomly, undergo repair, then resume service.

**Components**:
- Resources with failure processes
- MTBF (mean time between failures)
- MTTR (mean time to repair)
- Interrupted entities (resume or restart?)

**Example abstraction**: Processing units with maintenance requirements

**Libraries**: SimPy (Interrupt mechanism), salabim
**Complexity**: High
**Key challenge**: Handling interruptions, resumption logic

---

## Pattern 7: Batch Processing

**Abstract description**: Entities accumulate until batch size reached, then process together.

**Components**:
- Accumulation queue
- Batch size threshold
- Batch processing time (often longer than individual)

**Example abstraction**: Group processing (batch jobs, shipping containers)

**Libraries**: SimPy (custom logic), salabim
**Complexity**: Medium
**Key challenge**: Triggering batch formation

---

## Pattern 8: Rework Loops

**Abstract description**: Entities may fail quality check, return to earlier stage for rework.

**Components**:
- Quality check decision point
- Rework probability or deterministic failure
- Feedback loop to earlier stage
- Maximum rework attempts

**Example abstraction**: Iterative processing with quality gates

**Libraries**: SimPy (routing logic), salabim
**Complexity**: High
**Key challenge**: Cycle detection, infinite loop prevention

---

## Pattern Selection Guide

| Pattern | Complexity | Best Library | Reason |
|---------|-----------|--------------|--------|
| Single queue | Low | Ciw, SimPy, salabim | Any works, Ciw simplest |
| Multi-stage | Medium | SimPy, desmod | Flexible routing |
| Priority | Medium | SimPy | Built-in PriorityResource |
| Network | Medium-High | Ciw | Purpose-built for networks |
| Inventory | Medium | SimPy | Store/Container primitives |
| Breakdowns | High | SimPy | Interrupt mechanism |
| Batching | Medium | SimPy | Custom logic needed |
| Rework | High | SimPy | Routing flexibility |

## Anti-Patterns (What NOT to Do)

### ❌ Using Mesa for Operational Processes
Mesa is agent-based, not for process flows. Don't use for queueing/manufacturing.

### ❌ Using Ciw for Complex Non-Queue Logic
Ciw is specialized for queues. For arbitrary routing/rework, use SimPy.

### ❌ Modeling Everything as Agents
Not all entities need autonomy. Passive entities in process-based DES are simpler.

## Summary

Eight generic patterns cover most DES applications. Choose library based on pattern complexity:
- **Simple queues**: Ciw
- **Complex routing**: SimPy
- **Agent behaviors**: Mesa
- **Modularity**: desmod

See S1-rapid/recommendation.md for library selection and S3-need-driven/decision-framework.md for detailed criteria.
