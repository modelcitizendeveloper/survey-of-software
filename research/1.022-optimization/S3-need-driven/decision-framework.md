# S3-Need-Driven: Decision Framework

## Overview

Practical decision framework for selecting Python optimization tools.

## Step-by-Step Selection Process

### Step 1: Identify Problem Type

**Questions to ask**:
1. Are variables continuous or discrete (integer)?
2. Is objective function linear or nonlinear?
3. Are constraints linear or nonlinear?
4. Do you need multiple objectives?
5. Are there logical constraints (scheduling, all-different)?

**Decision tree**: See S1-rapid/approach.md for detailed problem type taxonomy

**Output**: Problem type (LP, MILP, NLP, MINLP, convex, CP, multi-objective)

### Step 2: Assess Problem Size

**Small**: <1000 variables, <100 constraints
**Medium**: 1k-100k variables, 100-10k constraints
**Large**: >100k variables, >10k constraints

**Why it matters**: Some libraries/solvers better for large scale

### Step 3: Determine Priorities

Rank these priorities:
1. **Simplicity**: Easy to learn and use
2. **Solver flexibility**: Try multiple solvers
3. **Performance**: Maximum speed
4. **Cost**: Budget constraints
5. **Production readiness**: Stability, support

### Step 4: Apply Selection Matrix

| Problem Type | Priority: Simplicity | Priority: Flexibility | Priority: Performance | Priority: Cost |
|--------------|---------------------|----------------------|----------------------|----------------|
| **LP** | PuLP | Pyomo | HiGHS (via any) | HiGHS (free) |
| **MILP** | PuLP | Pyomo | Gurobi* | SCIP (free) |
| **NLP** | scipy.optimize | Pyomo | Knitro* | IPOPT (free) |
| **Convex** | CVXPY | CVXPY | MOSEK* | CVXPY+SCS |
| **CP/Scheduling** | OR-Tools | OR-Tools | OR-Tools | OR-Tools (free) |
| **Multi-obj** | pymoo | pymoo | pymoo | pymoo (free) |

*Commercial solver (free academic, paid industry)

## Scenario-Based Recommendations

### Scenario 1: Data Scientist, Prototype LP/MILP
**Profile**: Python fluent, occasional optimization, proof-of-concept
**Recommendation**: **PuLP**
**Rationale**: Simplest learning curve, CBC bundled, adequate performance

### Scenario 2: Operations Researcher, Multiple Solver Experiments
**Profile**: Academic research, need to compare solvers
**Recommendation**: **Pyomo**
**Rationale**: 20+ solver backends, academic standard, excellent docs

### Scenario 3: Software Engineer, Production Scheduling System
**Profile**: Building production service, scheduling core
**Recommendation**: **OR-Tools CP-SAT**
**Rationale**: Production-ready, award-winning CP solver, Google-backed, bundled

### Scenario 4: Quant Finance, Portfolio Optimization
**Profile**: Financial applications, convex optimization
**Recommendation**: **CVXPY**
**Rationale**: DCP verification, designed for finance/ML, Stanford origins

### Scenario 5: Process Engineer, Nonlinear Process Optimization
**Profile**: Chemical/mechanical engineering, nonlinear physics
**Recommendation**: **Pyomo + IPOPT** (or **GEKKO** if dynamic)
**Rationale**: Nonlinear support, IPOPT industry standard open-source, GEKKO for DAE

### Scenario 6: Logistics Company, Large-Scale Routing
**Profile**: Real-world logistics, vehicle routing with constraints
**Recommendation**: **OR-Tools routing module**
**Rationale**: Specialized VRP solvers, time windows support, production-proven

### Scenario 7: ML Researcher, Hyperparameter Tuning
**Profile**: Machine learning, optimize hyperparameters
**Recommendation**: **Optuna** (not general optimization library!)
**Rationale**: Specialized for hyperparameter optimization, TPE algorithm

### Scenario 8: Startup, Large MILP, Limited Budget
**Profile**: Cost-sensitive, need good MILP performance
**Recommendation**: **Pyomo + SCIP**
**Rationale**: SCIP now Apache 2.0 (free), best open-source MILP, Pyomo flexibility

### Scenario 9: Enterprise, Mission-Critical, Budget Available
**Profile**: Large company, optimization-critical, can afford commercial
**Recommendation**: **Pyomo + Gurobi** or **direct Gurobi API**
**Rationale**: Maximum performance, professional support, Pyomo enables open-source dev

### Scenario 10: Student, Learning Optimization
**Profile**: Learning, want to try everything, limited budget
**Recommendation**: Start **PuLP**, then **Pyomo** (with academic Gurobi if available)
**Rationale**: Easy start, graduate to flexibility, free academic licenses

## Migration Decision Framework

### When to Stay with Current Tool
- Meets performance requirements
- Team fluent in tool
- No significant pain points
- Cost of migration > benefit

### When to Migrate
- Performance bottleneck (solver, not formulation)
- Need capabilities current tool lacks (e.g., MILP when using scipy.optimize)
- Open-source → commercial justified by ROI
- Simpler tool available (over-using complex tool for simple problem)

### How to Migrate
**Pyomo makes this easy**:
```python
# Development
solver = SolverFactory('cbc')  # Open-source

# Production (same model!)
solver = SolverFactory('gurobi')  # Commercial
```

**Otherwise**: Rewrite model in new library (cost of migration)

## Red Flags (Don't Select If...)

| Library | Don't Select If... |
|---------|-------------------|
| **scipy.optimize** | Need integer variables, large-scale LP |
| **PuLP** | Need nonlinear, constraint programming |
| **Pyomo** | Simple one-off problem (overhead not worth it) |
| **CVXPY** | Problem is non-convex (DCP will reject) |
| **OR-Tools** | Need nonlinear programming |
| **GEKKO** | Not working with dynamic systems |
| **pymoo** | Single-objective problem |
| **Commercial solver** | Small problem, limited budget, open-source sufficient |

## Decision Checklist

Before finalizing decision, verify:

- [ ] Problem type correctly identified (LP, MILP, NLP, etc.)
- [ ] Library supports problem type
- [ ] Solver availability (free/commercial, license compliance)
- [ ] Team can learn library (documentation, examples available)
- [ ] Performance adequate for problem size
- [ ] Budget allows (commercial solvers $10k-100k/year)
- [ ] Integration with existing codebase feasible
- [ ] Community support available (Stack Overflow, GitHub)

## Quick Reference Card

**Need to solve NOW, minimal research**:
- **LP/MILP**: Use PuLP
- **Continuous NLP**: Use scipy.optimize
- **Convex**: Use CVXPY
- **Scheduling**: Use OR-Tools CP-SAT
- **Multi-objective**: Use pymoo

**Have time to learn, want best tool**:
- Read S1-rapid/recommendation.md
- Apply this decision framework
- Test on small instance before committing

## Key Principle

**Problem type determines library, not domain**. Scheduling is scheduling whether it's manufacturing, healthcare, or transportation. Selection criteria are problem structure, not industry.

## Final Recommendation

**Default path for most users**:
1. Start with PuLP (LP/MILP) or scipy.optimize (NLP)
2. Graduate to Pyomo when complexity justifies (or need solver flexibility)
3. Use specialists (CVXPY, OR-Tools, pymoo) for their domains
4. Consider commercial (Gurobi) only when open-source performance insufficient

This path minimizes learning curve while providing upgrade path as needs grow.
