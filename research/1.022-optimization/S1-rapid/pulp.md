# PuLP: Linear Programming in Python

## Overview

PuLP is a linear and mixed-integer programming modeler written in Python. It is designed to be **simple and accessible** for LP/MILP problems, with an algebraic modeling interface and the CBC solver bundled by default.

**Key finding**: PuLP 3.3.0 (Sept 2025) offers the **easiest entry point** for LP/MILP optimization in Python. Part of COIN-OR project with MIT license. CBC solver included means zero external dependencies for basic use.

## Installation

```bash
pip install pulp
```

The CBC (COIN-OR Branch and Cut) solver is bundled, so you can solve MILP problems immediately without additional installation.

## Problem Types Supported

PuLP is focused exclusively on linear programming:

| Problem Type | Supported | Notes |
|--------------|-----------|-------|
| Linear Programming (LP) | ✅ Yes | Continuous variables only |
| Mixed-Integer Linear (MILP) | ✅ Yes | Integer and binary variables |
| Quadratic Programming (QP) | ❌ No | Use CVXPY or Pyomo |
| Nonlinear Programming (NLP) | ❌ No | Use scipy or Pyomo |
| Constraint Programming | ❌ No | Use OR-Tools |

**Philosophy**: Do one thing well. PuLP targets LP/MILP with simple, clean API.

## Basic Example: Linear Programming

```python
from pulp import *

# Create problem
prob = LpProblem("Example", LpMaximize)

# Variables
x = LpVariable("x", lowBound=0)
y = LpVariable("y", lowBound=0)

# Objective: maximize x + 2y
prob += x + 2*y, "Objective"

# Constraints
prob += 2*x + y <= 20, "Constraint1"
prob += x + 2*y <= 20, "Constraint2"

# Solve with bundled CBC solver
prob.solve()

# Results
print(f"Status: {LpStatus[prob.status]}")
print(f"Optimal value: {value(prob.objective)}")
print(f"x = {value(x)}")
print(f"y = {value(y)}")
```

## Basic Example: Integer Programming

```python
from pulp import *

prob = LpProblem("Integer_Example", LpMaximize)

# Integer variables
x = LpVariable("x", lowBound=0, cat='Integer')
y = LpVariable("y", lowBound=0, cat='Integer')

# Objective
prob += x + 2*y

# Constraints
prob += 2*x + y <= 20
prob += x + 2*y <= 20

# Solve
prob.solve(PULP_CBC_CMD(msg=0))  # msg=0 suppresses solver output

print(f"x = {value(x)}")  # Integer value
print(f"y = {value(y)}")  # Integer value
print(f"Optimal value: {value(prob.objective)}")
```

## Basic Example: Binary Selection Problem

```python
from pulp import *

# Select subset of projects to maximize value subject to budget
projects = ['A', 'B', 'C', 'D']
costs = {'A': 10, 'B': 15, 'C': 12, 'D': 8}
values = {'A': 20, 'B': 30, 'C': 25, 'D': 15}
budget = 30

prob = LpProblem("Project_Selection", LpMaximize)

# Binary variables: select[p] = 1 if project p is selected
select = LpVariable.dicts("select", projects, cat='Binary')

# Objective: maximize total value
prob += lpSum([values[p] * select[p] for p in projects])

# Budget constraint
prob += lpSum([costs[p] * select[p] for p in projects]) <= budget

# Solve
prob.solve()

# Display selected projects
print("Selected projects:")
for p in projects:
    if value(select[p]) == 1:
        print(f"  {p}: value={values[p]}, cost={costs[p]}")
print(f"Total value: {value(prob.objective)}")
```

## Basic Example: Multi-Index Variables

```python
from pulp import *

# Transportation problem: ship products from factories to warehouses
factories = ['F1', 'F2', 'F3']
warehouses = ['W1', 'W2', 'W3', 'W4']

supply = {'F1': 100, 'F2': 150, 'F3': 120}
demand = {'W1': 80, 'W2': 70, 'W3': 90, 'W4': 60}
cost = {  # cost[factory, warehouse]
    ('F1', 'W1'): 2, ('F1', 'W2'): 4, ('F1', 'W3'): 5, ('F1', 'W4'): 3,
    ('F2', 'W1'): 3, ('F2', 'W2'): 1, ('F2', 'W3'): 3, ('F2', 'W4'): 2,
    ('F3', 'W1'): 5, ('F3', 'W2'): 4, ('F3', 'W3'): 2, ('F3', 'W4'): 3,
}

prob = LpProblem("Transportation", LpMinimize)

# Variables: flow[f, w] = amount shipped from factory f to warehouse w
routes = [(f, w) for f in factories for w in warehouses]
flow = LpVariable.dicts("flow", routes, lowBound=0)

# Objective: minimize total transportation cost
prob += lpSum([cost[f, w] * flow[f, w] for (f, w) in routes])

# Supply constraints: don't exceed factory capacity
for f in factories:
    prob += lpSum([flow[f, w] for w in warehouses]) <= supply[f]

# Demand constraints: meet warehouse demand
for w in warehouses:
    prob += lpSum([flow[f, w] for f in factories]) >= demand[w]

# Solve
prob.solve()

print(f"Total cost: {value(prob.objective)}")
for (f, w) in routes:
    if value(flow[f, w]) > 0:
        print(f"Ship {value(flow[f, w])} from {f} to {w}")
```

## API Design Philosophy

**Algebraic modeling with Python syntax**: Use Python operators (+, -, *, <=, >=, ==) naturally.

**Advantages**:
- **Simple to learn**: Minimal concepts (LpProblem, LpVariable, constraints)
- **Pythonic**: Uses Python operators, dictionaries, list comprehensions
- **Bundled solver**: CBC included, works immediately
- **Lightweight**: Focused API, not trying to do everything
- **Readable**: Models look like mathematical formulations

**Disadvantages**:
- **Limited to LP/MILP**: No nonlinear, no constraint programming
- **Less flexible than Pyomo**: Fewer solver options, less extensible
- **Performance**: For maximum MILP performance, commercial solvers (Gurobi) faster

## Solver Backends

PuLP interfaces with multiple LP/MILP solvers:

### Bundled (Included):
- **CBC** (COIN-OR Branch and Cut): Default, good quality open-source MILP solver

### External (if installed):
- **GLPK**: GNU Linear Programming Kit
- **HiGHS**: Modern high-performance LP/MIP solver
- **Gurobi**: Commercial (fast, requires license)
- **CPLEX**: IBM commercial (requires license)
- **XPRESS**: FICO commercial (requires license)
- **SCIP**: Open-source MILP/MINLP
- **MOSEK**: Commercial conic solver

Specify solver: `prob.solve(GLPK())`, `prob.solve(GUROBI())`, etc.

Install solvers via extras: `pip install pulp[gurobi]`, `pip install pulp[highs]`

## When to Use PuLP

### ✅ Good fit when:
- **LP or MILP problems**: Linear objective and constraints with integer variables
- **Getting started**: Learning optimization, simple problems
- **Rapid prototyping**: Quick experiments, proof of concept
- **No external dependencies wanted**: CBC bundled, works immediately
- **Small to medium problems**: Thousands of variables
- **Occasional optimization**: Not building optimization-heavy systems

### ❌ Not suitable when:
- **Nonlinear problems**: No NLP support → use scipy, Pyomo, GEKKO
- **Constraint programming**: Scheduling, sequencing → use OR-Tools CP-SAT
- **Convex optimization**: SOCP, SDP → use CVXPY
- **Need many solvers**: Pyomo supports 20+ solvers, PuLP has fewer
- **Very large MILP**: For maximum performance, use Gurobi/CPLEX directly

## Community and Maturity

| Metric | Value/Status |
|--------|--------------|
| **Latest version** | 3.3.0 (September 2025) |
| **Maturity** | Mature (15+ years) |
| **Part of** | COIN-OR (Computational Infrastructure for Operations Research) |
| **Maintenance** | Active (recent releases) |
| **Documentation** | Good (coin-or.github.io/pulp) |
| **License** | MIT (permissive) |
| **Python versions** | 3.9+ |
| **Repository** | github.com/coin-or/pulp |

PuLP is a **mature, stable** library with active maintenance. Part of respected COIN-OR project.

## Key Findings from Research

1. **Easiest entry point**: Simplest API among algebraic modeling languages. Good for teaching and learning.

2. **CBC bundled**: Major usability advantage. No solver installation required. CBC is respectable open-source MILP solver.

3. **Version 3.3.0 (Sept 2025)**: Recent release shows active maintenance. Requires Python 3.9+.

4. **HiGHS support**: Can use HiGHS (the rising star open-source solver adopted by SciPy and MATLAB) via `pip install pulp[highs]`.

5. **COIN-OR ecosystem**: Part of mature operations research ecosystem (CBC, CLP, GLPK all COIN-OR projects).

## Comparison with Alternatives

| Feature | PuLP | Pyomo | CVXPY | OR-Tools |
|---------|------|-------|-------|----------|
| Problem types | LP, MILP | LP, MILP, NLP, MINLP | Convex | LP, MILP, CP |
| Simplicity | ⭐⭐⭐ Easy | ⭐⭐ Moderate | ⭐⭐ Moderate | ⭐⭐ Moderate |
| Bundled solver | ✅ CBC | ❌ No | ✅ Multiple | ✅ Multiple |
| Solver flexibility | ⭐⭐ Good | ⭐⭐⭐ Excellent | ⭐⭐ Good | ⭐ Limited |
| Performance | Good | Good | Good | Excellent (CP-SAT) |
| Best for | Simple LP/MILP | Research, multi-solver | Convex problems | Production, CP |

## Example Use Cases (Generic)

### Blending Problem
Mix ingredients to meet requirements at minimum cost.

```python
from pulp import *

# Blend ingredients to meet nutrient requirements
ingredients = ['A', 'B', 'C']
nutrients = ['protein', 'fiber', 'fat']

# Cost per unit
cost = {'A': 2.0, 'B': 3.5, 'C': 1.8}

# Nutrient content per unit
content = {
    ('A', 'protein'): 0.10, ('A', 'fiber'): 0.05, ('A', 'fat'): 0.02,
    ('B', 'protein'): 0.15, ('B', 'fiber'): 0.08, ('B', 'fat'): 0.03,
    ('C', 'protein'): 0.08, ('C', 'fiber'): 0.12, ('C', 'fat'): 0.01,
}

# Minimum nutrient requirements
requirements = {'protein': 10, 'fiber': 6, 'fat': 2}

prob = LpProblem("Blending", LpMinimize)

# Variables: amount of each ingredient
x = LpVariable.dicts("ingredient", ingredients, lowBound=0)

# Objective: minimize cost
prob += lpSum([cost[i] * x[i] for i in ingredients])

# Nutrient constraints
for n in nutrients:
    prob += lpSum([content[i, n] * x[i] for i in ingredients]) >= requirements[n]

prob.solve()

print(f"Minimum cost: {value(prob.objective):.2f}")
for i in ingredients:
    print(f"Ingredient {i}: {value(x[i]):.2f} units")
```

### Cutting Stock Problem
Cut raw materials to required lengths minimizing waste.

```python
from pulp import *

# Cut stock of length 100 into required pieces
stock_length = 100
required_pieces = {30: 5, 40: 3, 50: 2}  # {length: quantity}

# Generate cutting patterns (simplified)
patterns = [
    {30: 3, 40: 0, 50: 0},  # Three 30s
    {30: 1, 40: 1, 50: 0},  # One 30, one 40
    {30: 0, 40: 2, 50: 0},  # Two 40s
    {30: 0, 40: 0, 50: 2},  # Two 50s
    {30: 1, 40: 0, 50: 1},  # One 30, one 50
]

prob = LpProblem("Cutting_Stock", LpMinimize)

# Variables: number of times each pattern is used
use_pattern = LpVariable.dicts("pattern", range(len(patterns)), lowBound=0, cat='Integer')

# Objective: minimize number of stocks used
prob += lpSum([use_pattern[p] for p in range(len(patterns))])

# Meet demand for each piece length
for length, quantity in required_pieces.items():
    prob += lpSum([patterns[p][length] * use_pattern[p]
                   for p in range(len(patterns))]) >= quantity

prob.solve()

print(f"Minimum stocks needed: {value(prob.objective)}")
for p in range(len(patterns)):
    if value(use_pattern[p]) > 0:
        print(f"Pattern {p}: use {value(use_pattern[p])} times - {patterns[p]}")
```

### Facility Location
Decide which facilities to open and how to serve customers.

```python
from pulp import *

# Same as earlier example in or-tools.md
# (Facility location with fixed costs and transportation)
# ... (code similar to OR-Tools example but using PuLP syntax)
```

## Advanced Features

### Multiple Objectives (Lexicographic)
Solve for primary objective, then optimize secondary subject to primary being optimal.

```python
# First solve for primary objective
prob.solve()
primary_optimal = value(prob.objective)

# Add constraint that primary stays optimal
prob += primary_objective == primary_optimal

# Change to secondary objective
prob.sense = LpMinimize
prob.setObjective(secondary_objective)

prob.solve()
```

### Constraint Names and Access
```python
# Named constraints for later reference
prob += (x + y <= 10, "capacity_constraint")

# Access constraint
for name, constraint in prob.constraints.items():
    print(f"{name}: {constraint}")
```

### Variable Bounds and Categories
```python
# Different variable types
x = LpVariable("x", lowBound=0)                    # x >= 0
y = LpVariable("y", lowBound=0, upBound=10)        # 0 <= y <= 10
z = LpVariable("z", cat='Integer')                  # Integer
b = LpVariable("b", cat='Binary')                   # Binary (0 or 1)
```

### Writing Problem to File
```python
# Export to LP format for inspection or use with external tools
prob.writeLP("model.lp")
```

## Performance Tips

1. **Use CBC for general MILP**: Bundled, good performance
2. **Use HiGHS for large LP**: Install with `pip install pulp[highs]`, faster than CBC for LP
3. **Use Gurobi for large MILP**: If performance critical and license available
4. **Formulation matters**: Tight formulations solve faster than loose ones
5. **Use appropriate variable types**: Don't use `Integer` if `Continuous` works

## Solver Selection Example

```python
from pulp import *

prob = LpProblem("Example", LpMaximize)
# ... define variables, objective, constraints ...

# Try different solvers
# prob.solve(PULP_CBC_CMD())        # Default bundled CBC
# prob.solve(HiGHS_CMD())           # HiGHS (if installed)
# prob.solve(GUROBI_CMD())          # Gurobi (if licensed)
# prob.solve(CPLEX_CMD())           # CPLEX (if licensed)
# prob.solve(GLPK_CMD())            # GLPK (if installed)

# With options
prob.solve(PULP_CBC_CMD(msg=1, timeLimit=60))  # Show output, 60s limit
```

## References

- Official documentation: https://coin-or.github.io/pulp/
- GitHub repository: https://github.com/coin-or/pulp
- COIN-OR: https://www.coin-or.org/
- Tutorials: https://coin-or.github.io/pulp/CaseStudies/index.html

## Summary

**PuLP** is the **simplest path** to LP/MILP optimization in Python:
- Easy to learn and use
- CBC solver bundled (works immediately)
- Clean algebraic modeling interface
- Mature and stable (COIN-OR project)
- Good for small to medium problems

**Choose PuLP** when:
- Getting started with optimization
- LP or MILP problems (no nonlinear)
- Want bundled solver (no installation hassles)
- Rapid prototyping
- Teaching or learning

**Look elsewhere** for:
- Nonlinear problems (scipy, Pyomo, GEKKO)
- Constraint programming (OR-Tools)
- Convex optimization with verification (CVXPY)
- Maximum solver flexibility (Pyomo's 20+ backends)
- Large-scale performance (direct Gurobi/CPLEX API)

If you're solving LP/MILP and want the easiest path, **start with PuLP**.
