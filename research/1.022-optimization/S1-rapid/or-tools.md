# Google OR-Tools: Industrial-Strength Operations Research

## Overview

OR-Tools is Google's open-source operations research toolkit. It provides high-performance solvers for constraint programming (CP), linear/integer programming (LP/MILP), vehicle routing, and graph algorithms. Written in C++ with Python, Java, and C# bindings.

**Key finding**: With 12.6k GitHub stars, OR-Tools is the most popular open-source optimization framework. Actively maintained by Google with Python 3.13 support as of 2025.

## Installation

```bash
pip install ortools
```

OR-Tools is self-contained with solvers bundled (no external solver installation required).

## Problem Types Supported

| Problem Type | Supported | Solver/Module |
|--------------|-----------|---------------|
| Linear Programming (LP) | ✅ Yes | GLOP (Google's LP solver) |
| Mixed-Integer Linear (MILP) | ✅ Yes | SCIP, GLPK, CBC (bundled) |
| Constraint Programming (CP) | ✅ Yes | CP-SAT (Google's flagship CP solver) |
| Vehicle Routing (VRP) | ✅ Yes | Dedicated routing library |
| Network Flows | ✅ Yes | Min-cost flow, max-flow algorithms |
| Graph Algorithms | ✅ Yes | Shortest paths, assignment |
| Nonlinear Programming (NLP) | ❌ No | Use scipy or Pyomo+IPOPT |
| Convex Optimization | ❌ No | Use CVXPY |

## Basic Example: Linear Programming

```python
from ortools.linear_solver import pywraplp

# Create solver instance
solver = pywraplp.Solver.CreateSolver('GLOP')  # Google's LP solver

# Create variables: 0 <= x <= infinity, 0 <= y <= infinity
x = solver.NumVar(0, solver.infinity(), 'x')
y = solver.NumVar(0, solver.infinity(), 'y')

# Create constraints
# Constraint 1: 2x + y <= 20
solver.Add(2 * x + y <= 20)

# Constraint 2: x + 2y <= 20
solver.Add(x + 2 * y <= 20)

# Objective: maximize x + 2y
solver.Maximize(x + 2 * y)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print(f'Optimal solution found:')
    print(f'x = {x.solution_value()}')
    print(f'y = {y.solution_value()}')
    print(f'Optimal value = {solver.Objective().Value()}')
else:
    print('No optimal solution found.')
```

## Basic Example: Mixed-Integer Programming

```python
from ortools.linear_solver import pywraplp

# Create MILP solver (using SCIP backend)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Integer variables: x, y ∈ {0, 1, 2, ...}
x = solver.IntVar(0, solver.infinity(), 'x')
y = solver.IntVar(0, solver.infinity(), 'y')

# Constraints
solver.Add(2 * x + y <= 20)
solver.Add(x + 2 * y <= 20)

# Objective: maximize x + 2y
solver.Maximize(x + 2 * y)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print(f'x = {x.solution_value()}')  # Integer values
    print(f'y = {y.solution_value()}')
    print(f'Optimal value = {solver.Objective().Value()}')
```

## Basic Example: Constraint Programming (CP-SAT)

CP-SAT is Google's state-of-the-art constraint programming solver, excellent for scheduling and combinatorial problems.

```python
from ortools.sat.python import cp_model

# Create model
model = cp_model.CpModel()

# Variables with domain [0, 10]
x = model.NewIntVar(0, 10, 'x')
y = model.NewIntVar(0, 10, 'y')
z = model.NewIntVar(0, 10, 'z')

# Constraint: x != y (all different)
model.Add(x != y)
model.Add(y != z)
model.Add(x != z)

# Constraint: x + y + z == 15
model.Add(x + y + z == 15)

# Objective: maximize x * y * z
model.Maximize(x * y * z)

# Solve
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print(f'x = {solver.Value(x)}')
    print(f'y = {solver.Value(y)}')
    print(f'z = {solver.Value(z)}')
    print(f'Objective = {solver.ObjectiveValue()}')
```

## Modules and Components

OR-Tools is organized into specialized modules:

### 1. Linear/Integer Programming (`linear_solver`)
- **GLOP**: Google's LP solver (primal/dual simplex)
- **SCIP, CBC, GLPK**: Bundled MILP solvers
- **External**: Can interface with Gurobi, CPLEX if installed

### 2. Constraint Programming (`sat`)
- **CP-SAT**: Modern SAT-based CP solver
- Excellent for scheduling, assignment, sequencing
- Exploits Boolean satisfiability techniques
- Winner of multiple MiniZinc Challenge medals

### 3. Vehicle Routing (`routing`)
- Specialized solvers for VRP variants
- Rich constraint modeling (time windows, capacities, multiple vehicles)
- Metaheuristics tuned for routing

### 4. Graph Algorithms (`graph`)
- Min-cost flow, max-flow
- Shortest paths
- Assignment problems
- Network optimization

## API Design Philosophy

**Object-oriented, solver-specific APIs**: Different modules have different APIs (linear_solver vs CP-SAT vs routing).

**Advantages**:
- High performance (thin Python wrapper over C++)
- Rich features specific to problem type
- Bundled solvers (easy installation)

**Disadvantages**:
- Different APIs for different problem types (less unified than Pyomo)
- More verbose than algebraic modeling
- Harder to switch between solver types

## When to Use OR-Tools

### ✅ Good fit when:
- **Constraint programming**: Scheduling, sequencing, combinatorial problems → CP-SAT
- **Vehicle routing**: Delivery routing, technician dispatch → routing module
- **Production environment**: Stable, high-performance, Google-backed
- **Avoid external dependencies**: Bundled solvers, no license management
- **Integer programming**: Strong MILP capability via SCIP
- **Graph/network problems**: Specialized efficient algorithms

### ❌ Not suitable when:
- **Nonlinear programming**: No NLP support → use scipy, Pyomo+IPOPT, GEKKO
- **Convex optimization**: No specialized convex solvers → use CVXPY
- **Algebraic modeling preference**: More verbose than Pyomo/CVXPY
- **Academic flexibility**: Pyomo supports more solver backends

## Solver Backends Available

### Bundled with OR-Tools:
- **GLOP**: Google's LP solver
- **CP-SAT**: Google's CP solver
- **SCIP**: Open-source MILP (Apache 2.0 since 9.0)
- **GLPK**: GNU Linear Programming Kit
- **CBC**: COIN-OR Branch and Cut

### External (if installed):
- **Gurobi**: Commercial MILP
- **CPLEX**: IBM commercial MILP
- **XPRESS**: FICO commercial MILP

Use `CreateSolver('SOLVER_NAME')` to select backend.

## Community and Maturity

| Metric | Value/Status |
|--------|--------------|
| **GitHub stars** | 12,600 |
| **Maturity** | Mature (10+ years) |
| **Maintenance** | Very active (Google) |
| **Latest release** | Continuous (2025: Python 3.13, muslinux support) |
| **Documentation** | Excellent (developers.google.com/optimization) |
| **License** | Apache 2.0 (open source) |
| **Contributors** | 100+ |
| **Python versions** | 3.8 - 3.13 |

OR-Tools is **production-grade** and used extensively at Google and beyond.

## Key Findings from Research

1. **CP-SAT dominance**: Google's CP-SAT solver wins MiniZinc Challenge medals, competitive with commercial CP solvers. Best-in-class for scheduling.

2. **Self-contained**: All solvers bundled. No license management, no external compilation. Major usability advantage.

3. **Multiple APIs**: Different modules (linear_solver, sat, routing) have distinct APIs. Less unified than Pyomo but more specialized.

4. **Python 3.13 support**: As of 2025, OR-Tools supports latest Python versions, showing active maintenance.

5. **Vehicle routing specialization**: Dedicated routing library with domain-specific constraints (time windows, capacities, precedence). Unique among Python optimization libraries.

## Comparison with Alternatives

| Feature | OR-Tools | Pyomo | scipy.optimize | PuLP |
|---------|----------|-------|----------------|------|
| LP/MILP | ✅ Excellent | ✅ Excellent | LP only | ✅ Good |
| Constraint Programming | ✅ Best-in-class | ⚠️ Via external | ❌ No | ❌ No |
| Nonlinear | ❌ No | ✅ Yes | ✅ Yes | ❌ No |
| Vehicle Routing | ✅ Specialized | ❌ No | ❌ No | ❌ No |
| Bundled solvers | ✅ Yes | ❌ No | Partial | ✅ CBC only |
| Modeling style | Object-oriented | Algebraic | Functional | Algebraic |
| API complexity | Moderate | Moderate | Easy | Easy |

## Example Use Cases (Generic)

### Resource Assignment with Constraints
Assign tasks to workers subject to skill requirements, availability, workload limits.

```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()

# Binary variables: worker_task[w, t] = 1 if worker w assigned to task t
worker_task = {}
for w in workers:
    for t in tasks:
        worker_task[w, t] = model.NewBoolVar(f'worker_{w}_task_{t}')

# Each task assigned to exactly one worker
for t in tasks:
    model.Add(sum(worker_task[w, t] for w in workers) == 1)

# Worker workload limits
for w in workers:
    model.Add(sum(duration[t] * worker_task[w, t] for t in tasks) <= max_workload[w])

# Minimize total cost
model.Minimize(sum(cost[w, t] * worker_task[w, t]
                   for w in workers for t in tasks))

solver = cp_model.CpSolver()
solver.Solve(model)
```

### Scheduling with No-Overlap
Schedule jobs on machines with no time overlap.

```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()

# Interval variables for each job
intervals = []
for j in jobs:
    start = model.NewIntVar(0, horizon, f'start_{j}')
    duration = durations[j]
    end = model.NewIntVar(0, horizon, f'end_{j}')
    interval = model.NewIntervalVar(start, duration, end, f'interval_{j}')
    intervals.append(interval)

# No overlap constraint
model.AddNoOverlap(intervals)

# Minimize makespan (max end time)
makespan = model.NewIntVar(0, horizon, 'makespan')
for j in jobs:
    model.Add(makespan >= intervals[j].EndExpr())

model.Minimize(makespan)
```

### Network Flow Problem
Route flow through network minimizing cost.

```python
from ortools.graph import pywrapgraph

# Create min-cost flow solver
min_cost_flow = pywrapgraph.SimpleMinCostFlow()

# Add arcs: (source, destination, capacity, unit_cost)
for source, dest, capacity, cost in arcs:
    min_cost_flow.AddArcWithCapacityAndUnitCost(source, dest, capacity, cost)

# Set supply/demand at nodes
for node, supply in supplies.items():
    min_cost_flow.SetNodeSupply(node, supply)

# Solve
status = min_cost_flow.Solve()

if status == min_cost_flow.OPTIMAL:
    print(f'Minimum cost: {min_cost_flow.OptimalCost()}')
    for arc in range(min_cost_flow.NumArcs()):
        if min_cost_flow.Flow(arc) > 0:
            print(f'Arc {arc}: flow = {min_cost_flow.Flow(arc)}')
```

## Performance Characteristics

- **LP (GLOP)**: Competitive with open-source solvers (GLPK, CLP), somewhat slower than commercial
- **MILP (SCIP)**: Good performance, especially for structured problems
- **CP-SAT**: Excellent for scheduling and combinatorial problems, award-winning
- **Routing**: Highly optimized metaheuristics for vehicle routing variants

For maximum MILP performance on large instances, commercial solvers (Gurobi, CPLEX) still faster, but OR-Tools competitive for many practical problems.

## References

- Official documentation: https://developers.google.com/optimization
- GitHub repository: https://github.com/google/or-tools (12.6k stars)
- Examples: https://github.com/google/or-tools/tree/stable/examples/python
- CP-SAT: https://developers.google.com/optimization/cp/cp_solver

## Summary

**OR-Tools** is a comprehensive, production-ready optimization toolkit with:
- Best-in-class constraint programming (CP-SAT)
- Specialized vehicle routing solvers
- Bundled MILP solvers (SCIP, CBC, GLPK)
- Google backing and active development

**Choose OR-Tools** for:
- Scheduling, sequencing, combinatorial problems (CP-SAT)
- Vehicle routing and logistics
- Production environments requiring stable, maintained library
- Projects avoiding external solver installation

**Look elsewhere** for nonlinear programming, convex optimization, or algebraic modeling preference.
