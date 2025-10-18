# Learning Curve Analysis

## Research-Based Time Estimates

### SimPy
**Official claim**: "Learn basics in ~10 minutes"
**Realistic estimate**: 2-4 hours to first working model

**Prerequisites**:
- Python basics (functions, classes)
- Understanding of generators (`yield` statement)
- Familiarity with simulation concepts

**Learning path**:
1. Read 10-minute tutorial (30 min actual)
2. Run bank example (30 min)
3. Modify example for own use case (1-2 hours)
4. Add data collection (30 min)

**Difficulty**: Moderate (generators are unfamiliar to many)

---

### salabim
**Estimate**: 2-3 hours to first model (similar to SimPy)

**Advantage**: Yieldless API (no generators)
**Disadvantage**: Less documentation/tutorials than SimPy

**Learning path**:
1. Read manual introduction (45 min)
2. Run queue example (30 min)
3. Experiment with built-in statistics (30 min)
4. Add animation (optional, 1 hour)

**Difficulty**: Lower API complexity, but smaller community = fewer resources

---

### Mesa
**Estimate**: 4-8 hours (different paradigm)

**Prerequisites**:
- Python basics
- Understanding of agent-based modeling concepts
- Grid/network structures

**Learning path**:
1. Understand ABM vs DES (1 hour)
2. Run Schelling model example (1 hour)
3. Create custom agent class (2 hours)
4. Add visualization (1-2 hours)

**Difficulty**: Higher (new paradigm if coming from DES background)

---

### Ciw
**Estimate**: 1-3 hours (if queueing-focused)

**Advantage**: Simplest API for queueing networks
**Limitation**: Narrow scope (only queues)

**Learning path**:
1. Understand queueing network concepts (30 min)
2. Define simple network (30 min)
3. Run and analyze (1 hour)

**Difficulty**: Low for queueing, but limited applicability

---

### desmod
**Estimate**: 6-10 hours (requires SimPy knowledge)

**Prerequisites**:
- SimPy proficiency
- Component-based architecture understanding
- Larger-scale modeling experience

**Learning path**:
1. Learn SimPy first (4 hours)
2. Understand component hierarchy (2 hours)
3. Build component model (3-4 hours)

**Difficulty**: High (advanced topic)

---

## Documentation Quality (Research Findings)

| Library | Docs Quality | Tutorials | Examples | Community |
|---------|-------------|-----------|----------|-----------|
| SimPy | Excellent | Many | Extensive | Large |
| salabim | Very Good | Moderate | Included | Small |
| Mesa | Excellent | Good | Repo | Medium |
| Ciw | Good | Series | Notebooks | Small |
| desmod | Good | Limited | Corporate | Small |

---

## Recommendation for Beginners

**Fastest path**: Ciw (if problem is queueing)
**Easiest API**: salabim (yieldless)
**Best documented**: SimPy (most resources)
**Different paradigm**: Mesa (if ABM needed)

---

## Summary

Learning curve varies:
- **Ciw**: 1-3 hours (queueing only)
- **salabim**: 2-3 hours (yieldless advantage)
- **SimPy**: 2-4 hours (generator learning curve)
- **Mesa**: 4-8 hours (different paradigm)
- **desmod**: 6-10 hours (SimPy prerequisite)

Choose based on problem fit, not just learning time.
